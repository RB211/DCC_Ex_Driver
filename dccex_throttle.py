#!/usr/bin/env python3
"""
DCC-EX Native Protocol Throttle
================================
A dependency-light Tkinter throttle that speaks the DCC-EX native command
protocol directly to an EX-CommandStation (EX-CSB1 etc.) over TCP or USB serial.

  TCP    : default port 2560
  Serial : default 115200 baud (requires pyserial; optional)

The command station auto-selects native vs WiThrottle protocol based on the
first command it receives, so this client sends <s> immediately on connect to
lock it into native mode and pull the version/status.

Commands used:
  <s>                     status / version
  <1> <0> <1 MAIN> ...    track power
  <t cab speed dir>       throttle   speed 0-126, -1 = estop, dir 1=fwd 0=rev
  <F cab func state>      function   func 0-68 protocol, 0-31 exposed here
                                     (functMap in <l> is 32 bits), state 1/0
  <!>                     emergency stop everything

Broadcasts parsed:
  <l cab reg speedByte functMap>   loco state (from any throttle on the layout)
  <p0> <p1> <p1 MAIN>              power state
  <iDCC-EX V-...>                  version banner
"""

import queue
import re
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    serial = None
    list_ports = None
HAVE_SERIAL = serial is not None

MAX_FUNCTION = 31             # functMap in <l> is 32 bits, so F0-F31 round-trips
MOMENTARY_FUNCS = {3, 4}      # whistles: on while the button is held, off on release
MAX_SPEED = 126
SEND_INTERVAL = 0.08          # seconds between throttle updates while dragging
CURRENT_POLL_MS = 1000        # how often to ask the station for track current
MSG_RE = re.compile(rb"<([^>]*)>")


# --------------------------------------------------------------------------
# Transports
# --------------------------------------------------------------------------
class TransportError(Exception):
    pass


class BaseTransport:
    """Reads a byte stream, emits complete <...> messages onto a queue."""

    def __init__(self, rx_queue):
        self.rx = rx_queue
        self._buf = b""
        self._stop = threading.Event()
        self._thread = None

    def start_reader(self):
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def _read_loop(self):
        while not self._stop.is_set():
            try:
                data = self._read_some()
            except Exception as exc:
                if not self._stop.is_set():
                    self.rx.put(("error", str(exc)))
                return
            if data is None:          # timeout, nothing to do
                continue
            if data == b"":           # peer closed
                if not self._stop.is_set():
                    self.rx.put(("error", "connection closed by command station"))
                return
            self._buf += data
            for match in MSG_RE.finditer(self._buf):
                self.rx.put(("msg", match.group(1).decode("utf-8", "replace")))
            cut = self._buf.rfind(b">")
            if cut >= 0:
                self._buf = self._buf[cut + 1:]
            if len(self._buf) > 4096:  # runaway garbage guard
                self._buf = b""

    def _read_some(self):
        """Return bytes, None for "nothing yet", or b"" for "link is gone".

        b"" tears the reader down and reports a disconnect, so a subclass must
        only return it for a genuine end-of-stream -- never for a read timeout.
        """
        raise NotImplementedError

    def send(self, text):
        raise NotImplementedError

    def close(self):
        self._stop.set()


class TcpTransport(BaseTransport):
    def __init__(self, rx_queue, host, port, timeout=5.0):
        super().__init__(rx_queue)
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(0.4)
        self.start_reader()

    def _read_some(self):
        try:
            return self.sock.recv(1024)
        except socket.timeout:
            return None

    def send(self, text):
        self.sock.sendall((text + "\n").encode("ascii"))

    def close(self):
        super().close()
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()


class SerialTransport(BaseTransport):
    def __init__(self, rx_queue, port, baud=115200):
        if serial is None:
            raise TransportError("pyserial is not installed (pip install pyserial)")
        super().__init__(rx_queue)
        self.ser = serial.Serial(port, baud, timeout=0.4)
        time.sleep(0.2)
        self.ser.reset_input_buffer()
        self.start_reader()

    def _read_some(self):
        n = self.ser.in_waiting
        data = self.ser.read(n if n else 1)
        # b"" here is just the 0.4 s timeout expiring on an idle link, not EOF.
        # A serial link has no orderly close; the port vanishing surfaces as a
        # SerialException from read()/in_waiting, which _read_loop reports.
        return data if data else None

    def send(self, text):
        self.ser.write((text + "\n").encode("ascii"))

    def close(self):
        super().close()
        try:
            self.ser.close()
        except Exception:
            pass


# --------------------------------------------------------------------------
# Application
# --------------------------------------------------------------------------
class ThrottleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DCC-EX Native Throttle")
        self.minsize(720, 640)

        self.rx = queue.Queue()
        self.transport = None
        self.syncing = False           # suppress outbound sends while updating UI
        self.pending_speed = None
        self.last_sent = 0.0
        self.last_state = (None, None)  # (speed, dir) actually sent
        self.active_cab = 3            # address _cab_changed last acted on
        self.current_ma = None         # last reading from <c>; None = unknown
        self.max_ma = None             # motor driver capability
        self.trip_ma = None            # software circuit breaker limit
        self.overload = False          # latched by <p2>, cleared by <p0>/<p1>

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self._pump)
        self.after(30, self._speed_tick)
        self.after(CURRENT_POLL_MS, self._current_tick)

    # ---------------- UI construction ----------------
    def _build_ui(self):
        # --- Connection -------------------------------------------------
        conn = ttk.LabelFrame(self, text="Connection")
        conn.pack(fill="x", padx=6, pady=4)

        self.mode = tk.StringVar(value="tcp")
        ttk.Radiobutton(conn, text="TCP", variable=self.mode, value="tcp",
                        command=self._mode_changed).grid(row=0, column=0, padx=4, pady=4)
        ttk.Label(conn, text="Host:").grid(row=0, column=1, sticky="e")
        self.host = tk.StringVar(value="192.168.4.1")
        ttk.Entry(conn, textvariable=self.host, width=16).grid(row=0, column=2)
        ttk.Label(conn, text="Port:").grid(row=0, column=3, sticky="e")
        self.port = tk.StringVar(value="2560")
        ttk.Entry(conn, textvariable=self.port, width=7).grid(row=0, column=4)

        ttk.Radiobutton(conn, text="Serial", variable=self.mode, value="serial",
                        command=self._mode_changed).grid(row=1, column=0, padx=4, pady=4)
        self.serial_port = tk.StringVar()
        self.port_combo = ttk.Combobox(conn, textvariable=self.serial_port, width=28)
        self.port_combo.grid(row=1, column=1, columnspan=3, sticky="w", padx=(4, 0))
        self.refresh_btn = ttk.Button(conn, text="Refresh", width=8,
                                      command=self._refresh_ports)
        self.refresh_btn.grid(row=1, column=4)
        ttk.Label(conn, text="Baud:").grid(row=1, column=5, sticky="e")
        self.baud = tk.StringVar(value="115200")
        ttk.Entry(conn, textvariable=self.baud, width=8).grid(row=1, column=6)

        self.connect_btn = ttk.Button(conn, text="Connect", command=self._toggle_connect)
        self.connect_btn.grid(row=0, column=5, columnspan=2, sticky="ew", padx=6)

        self.status = tk.StringVar(value="Disconnected")
        ttk.Label(conn, textvariable=self.status, foreground="#888").grid(
            row=2, column=0, columnspan=7, sticky="w", padx=6, pady=(0, 4))

        self._refresh_ports()
        self._mode_changed()

        # --- Track power ------------------------------------------------
        power = ttk.LabelFrame(self, text="Track Power")
        power.pack(fill="x", padx=6, pady=4)
        for i, (label, cmd) in enumerate([
            ("ALL ON", "<1>"), ("ALL OFF", "<0>"),
            ("MAIN ON", "<1 MAIN>"), ("MAIN OFF", "<0 MAIN>"),
            ("PROG ON", "<1 PROG>"), ("PROG OFF", "<0 PROG>"),
        ]):
            ttk.Button(power, text=label, width=10,
                       command=lambda c=cmd: self.send_cmd(c)).grid(row=0, column=i, padx=3, pady=5)
        self.power_state = tk.StringVar(value="power: unknown")
        ttk.Label(power, textvariable=self.power_state).grid(
            row=0, column=6, padx=12, sticky="w")

        # --- Current draw ---------------------------------------------------
        ttk.Label(power, text="Current:").grid(row=1, column=0, padx=(6, 2),
                                               pady=(0, 6), sticky="e")
        self.current_bar = ttk.Progressbar(power, orient="horizontal",
                                           mode="determinate", length=300)
        self.current_bar.grid(row=1, column=1, columnspan=4, pady=(0, 6),
                              sticky="ew")
        self.current_text = tk.StringVar()
        # tk.Label, not ttk: the aqua theme ignores foreground on ttk.Label,
        # and the overload colour is the whole point of this readout.
        self.current_label = tk.Label(power, textvariable=self.current_text,
                                      anchor="w", width=24)
        self.current_label.grid(row=1, column=5, columnspan=2, padx=12,
                                pady=(0, 6), sticky="w")
        # Remember the theme's own colour: Tk 9 rejects foreground="" as a
        # reset, so restoring after an overload needs the real default.
        self.fg_normal = self.current_label.cget("foreground")
        self.poll_current = tk.IntVar(value=1)
        ttk.Checkbutton(power, text="Poll", variable=self.poll_current).grid(
            row=1, column=7, padx=(0, 8), pady=(0, 6), sticky="w")
        self._refresh_current()

        # --- Loco / throttle ---------------------------------------------
        loco = ttk.LabelFrame(self, text="Locomotive")
        loco.pack(fill="x", padx=6, pady=4)

        ttk.Label(loco, text="Address:").grid(row=0, column=0, padx=(6, 2), pady=6, sticky="e")
        self.cab = tk.IntVar(value=3)
        spin = ttk.Spinbox(loco, from_=1, to=10293, textvariable=self.cab, width=8,
                           command=self._cab_changed)
        spin.grid(row=0, column=1, sticky="w")
        # command= only fires on the arrows; catch typed addresses too
        spin.bind("<Return>", self._cab_changed)
        spin.bind("<FocusOut>", self._cab_changed)

        self.direction = tk.IntVar(value=1)
        ttk.Radiobutton(loco, text="Forward", variable=self.direction, value=1,
                        command=self._dir_changed).grid(row=0, column=2, padx=(18, 4))
        ttk.Radiobutton(loco, text="Reverse", variable=self.direction, value=0,
                        command=self._dir_changed).grid(row=0, column=3, padx=4)

        ttk.Button(loco, text="STOP", width=10,
                   command=self._stop).grid(row=0, column=4, padx=(18, 4))
        estop = tk.Button(loco, text="E-STOP ALL", width=12, bg="#c62828", fg="white",
                          activebackground="#e53935", activeforeground="white",
                          command=self._estop_all)
        estop.grid(row=0, column=5, padx=4)

        self.speed = tk.IntVar(value=0)
        self.scale = tk.Scale(loco, from_=0, to=MAX_SPEED, orient="horizontal",
                              variable=self.speed, length=640, tickinterval=21,
                              resolution=1, command=self._speed_moved)
        self.scale.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 8), sticky="ew")
        loco.columnconfigure(5, weight=1)

        # --- Functions -----------------------------------------------------
        funcs = ttk.LabelFrame(self, text="Functions")
        funcs.pack(fill="x", padx=6, pady=4)
        self.func_vars = {}
        cols = 6
        for n in range(0, MAX_FUNCTION + 1):
            var = tk.IntVar(value=0)
            self.func_vars[n] = var
            label = "F0 (Lights)" if n == 0 else f"F{n}"
            if n in MOMENTARY_FUNCS:
                # Momentary: <F 1> on press, <F 0> on release. No variable --
                # the widget's pressed look is the feedback, and func_vars[n]
                # still tracks the real state via the <l> broadcast.
                w = ttk.Button(funcs, text=f"{label} (Whistle)")
                w.bind("<ButtonPress-1>", lambda e, k=n: self._func_momentary(k, 1))
                w.bind("<ButtonRelease-1>", lambda e, k=n: self._func_momentary(k, 0))
            else:
                w = ttk.Checkbutton(funcs, text=label, variable=var,
                                    command=lambda k=n: self._func_toggled(k))
            w.grid(row=n // cols, column=n % cols, sticky="w", padx=8, pady=3)
        ttk.Button(funcs, text="All Functions Off", command=self._all_funcs_off).grid(
            row=(MAX_FUNCTION // cols) + 1, column=0, columnspan=2,
            sticky="w", padx=8, pady=(4, 6))

        # --- Console --------------------------------------------------------
        console = ttk.LabelFrame(self, text="Console")
        console.pack(fill="both", expand=True, padx=6, pady=4)
        self.log = tk.Text(console, height=10, wrap="none", state="disabled",
                           font=("Menlo", 11), background="#101418", foreground="#d8dee9")
        self.log.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.log.tag_config("tx", foreground="#88c0d0")
        self.log.tag_config("rx", foreground="#a3be8c")
        self.log.tag_config("err", foreground="#bf616a")
        self.log.tag_config("info", foreground="#ebcb8b")

        entry_row = ttk.Frame(console)
        entry_row.pack(fill="x", padx=4, pady=(0, 6))
        ttk.Label(entry_row, text="Raw:").pack(side="left")
        self.raw = tk.StringVar()
        e = ttk.Entry(entry_row, textvariable=self.raw)
        e.pack(side="left", fill="x", expand=True, padx=6)
        e.bind("<Return>", self._send_raw)
        ttk.Button(entry_row, text="Send", command=self._send_raw).pack(side="left")

    # ---------------- connection ----------------
    def _mode_changed(self):
        serial_ok = HAVE_SERIAL and self.mode.get() == "serial"
        state = "normal" if serial_ok else "disabled"
        self.port_combo.configure(state="readonly" if serial_ok else "disabled")
        self.refresh_btn.configure(state=state)

    def _refresh_ports(self):
        if list_ports is None:
            self.port_combo["values"] = ["pyserial not installed"]
            return
        ports = [p.device for p in list_ports.comports()]
        self.port_combo["values"] = ports
        if ports and not self.serial_port.get():
            guess = next((p for p in ports if "usb" in p.lower()), ports[0])
            self.serial_port.set(guess)

    def _toggle_connect(self):
        if self.transport:
            self._disconnect("Disconnected")
            return
        try:
            if self.mode.get() == "tcp":
                self.transport = TcpTransport(self.rx, self.host.get().strip(),
                                              int(self.port.get()))
                where = f"{self.host.get()}:{self.port.get()}"
            else:
                if not HAVE_SERIAL:
                    raise TransportError("pyserial is not installed (pip install pyserial)")
                self.transport = SerialTransport(self.rx, self.serial_port.get(),
                                                 int(self.baud.get()))
                where = f"{self.serial_port.get()} @ {self.baud.get()}"
        except Exception as exc:
            messagebox.showerror("Connection failed", str(exc))
            self.transport = None
            return

        self.connect_btn.configure(text="Disconnect")
        self.status.set(f"Connected to {where}")
        self._log(f"-- connected to {where}", "info")
        # Anything the slider did while offline is not a command the user meant
        # to issue now, and we know nothing about the loco until <l> arrives.
        self.pending_speed = None
        self.last_state = (None, None)
        self.send_cmd("<s>")          # forces native protocol mode + returns status
        self._request_cab_state()  # sync the selected loco instead of guessing

    def _disconnect(self, why):
        if self.transport:
            try:
                self.transport.close()
            except Exception:
                pass
        self.transport = None
        self.connect_btn.configure(text="Connect")
        self.status.set(why)
        self.power_state.set("power: unknown")
        self._reset_current()      # a stale reading is worse than no reading
        self._log(f"-- {why}", "info")

    # ---------------- outbound ----------------
    # Named send_cmd, not send: tk.Misc already defines send() (Tk's
    # inter-interpreter send) and overriding it with this signature clashes.
    def send_cmd(self, cmd, quiet=False):
        """True if the command actually reached the wire.

        Callers that flipped a widget before sending must revert it on False,
        or the UI ends up asserting a state the loco was never told about.
        quiet suppresses the console echo for polled traffic.
        """
        if not self.transport:
            if not quiet:
                self._log("not connected", "err")
            return False
        try:
            self.transport.send(cmd)
            if not quiet:
                self._log(f">> {cmd}", "tx")
            return True
        except Exception as exc:
            self._disconnect(f"Send failed: {exc}")
            return False

    def _set_quiet(self, var, value):
        """Write a widget var without tripping its own callback."""
        self.syncing = True
        var.set(value)
        self.syncing = False

    def _send_raw(self, *_):
        text = self.raw.get().strip()
        if not text:
            return
        if not text.startswith("<"):
            text = f"<{text}>"
        self.send_cmd(text)
        self.raw.set("")

    def _send_throttle(self, speed, direction):
        if not self.send_cmd(f"<t {self.cab.get()} {speed} {direction}>"):
            return False
        self.last_state = (speed, direction)
        self.last_sent = time.monotonic()
        return True

    def _speed_moved(self, _value):
        if self.syncing:
            return
        self.pending_speed = self.speed.get()

    def _speed_tick(self):
        """Rate-limited send so dragging the slider doesn't flood the station."""
        if self.transport and self.pending_speed is not None:
            target = (self.pending_speed, self.direction.get())
            if target == self.last_state:
                # Slider landed back where the station already is (a nudge and
                # an undo inside one SEND_INTERVAL). Nothing to send -- retire
                # the request instead of re-testing it every 30 ms forever.
                self.pending_speed = None
            elif (time.monotonic() - self.last_sent) >= SEND_INTERVAL:
                self._send_throttle(*target)
                # Cleared even on a failed send: the transport is gone, and a
                # stale value must not be replayed at the loco on reconnect.
                self.pending_speed = None
        self.after(30, self._speed_tick)

    def _dir_changed(self):
        if self.syncing:
            return
        if not self._send_throttle(self.speed.get(), self.direction.get()):
            self._set_quiet(self.direction, 1 - self.direction.get())

    def _cab_changed(self, *_):
        try:
            cab = self.cab.get()
        except tk.TclError:        # mid-edit / non-numeric text in the spinbox
            return
        if cab == self.active_cab:
            return
        self.active_cab = cab
        self.syncing = True
        self.speed.set(0)
        self.direction.set(1)
        for var in self.func_vars.values():
            var.set(0)
        self.syncing = False
        self.pending_speed = None
        self.last_state = (None, None)
        self._log(f"-- loco {cab} selected", "info")
        self._request_cab_state()

    def _current_tick(self):
        """Poll <c> while connected. Quiet: this would otherwise own the log."""
        if self.transport and self.poll_current.get():
            self.send_cmd("<c>", quiet=True)
        self.after(CURRENT_POLL_MS, self._current_tick)

    def _handle_current(self, parts):
        """<c "CurrentMAIN" current C "Milli" "0" max_ma "1" trip_ma>

        Pulled out by position of the *bare* integers rather than fixed index:
        the fixed fields are quoted ("0", "1"), so the unquoted numbers are
        exactly current, max, trip in that order. That also tolerates the
        shorter <c current> some older builds emit.
        """
        nums = [int(p) for p in parts[1:] if p.lstrip("-").isdigit()]
        if not nums:
            return
        self.current_ma = nums[0]
        if len(nums) >= 3:
            self.max_ma, self.trip_ma = nums[1], nums[2]
        self._refresh_current()

    def _refresh_current(self):
        limit = self.trip_ma or self.max_ma
        if self.overload:
            self.current_text.set("OVERLOAD")
            self.current_label.configure(foreground="#bf616a")
            self.current_bar.configure(value=self.current_bar["maximum"])
            return
        self.current_label.configure(foreground=self.fg_normal)
        if self.current_ma is None:
            self.current_text.set("current: --")
            self.current_bar.configure(value=0)
            return
        if limit:
            self.current_bar.configure(maximum=limit,
                                       value=min(self.current_ma, limit))
            self.current_text.set(f"{self.current_ma} mA / {limit} mA trip")
        else:
            self.current_bar.configure(value=0)
            self.current_text.set(f"{self.current_ma} mA")

    def _reset_current(self):
        self.current_ma = self.max_ma = self.trip_ma = None
        self.overload = False
        self._refresh_current()

    def _request_cab_state(self):
        """<t cab> asks the station to re-broadcast <l> for this address.

        Reply is a normal <l cab reg speedByte functMap> broadcast, so _handle
        does the sync. A reg/slot of -1 means the loco isn't in the reminders
        table yet; the zeroed UI is already the right answer in that case.
        """
        if self.transport:
            self.send_cmd(f"<t {self.active_cab}>")

    def _stop(self):
        prior = self.speed.get()
        self._set_quiet(self.speed, 0)
        self.pending_speed = None
        if not self._send_throttle(0, self.direction.get()):
            self._set_quiet(self.speed, prior)   # the loco never got the stop

    def _estop_all(self):
        if not self.send_cmd("<!>"):
            return
        self._set_quiet(self.speed, 0)
        self.pending_speed = None
        self.last_state = (0, self.direction.get())

    def _func_toggled(self, n):
        if self.syncing:
            return
        var = self.func_vars[n]
        if not self.send_cmd(f"<F {self.cab.get()} {n} {var.get()}>"):
            self._set_quiet(var, 1 - var.get())    # undo the click Tk already applied

    def _func_momentary(self, n, state):
        """Press/release for MOMENTARY_FUNCS. Nothing to revert on a failed
        send: the button has no latched state, and a release lost with the
        link leaves func_vars[n] to be corrected by the next <l> broadcast."""
        self.send_cmd(f"<F {self.cab.get()} {n} {state}>")

    def _all_funcs_off(self):
        for n, var in self.func_vars.items():
            if not var.get():
                continue
            if not self.send_cmd(f"<F {self.cab.get()} {n} 0>"):
                return          # link is down; leave the rest showing their real state
            self._set_quiet(var, 0)

    # ---------------- inbound ----------------
    def _pump(self):
        try:
            while True:
                kind, payload = self.rx.get_nowait()
                if kind == "error":
                    self._disconnect(f"Disconnected: {payload}")
                else:
                    # A polled <c> reply every second would drown the console.
                    # Only hide it while we are the one asking -- a hand-typed
                    # <c> with polling off still prints.
                    if not (self.poll_current.get() and payload.startswith("c ")):
                        self._log(f"<< <{payload}>", "rx")
                    self._handle(payload)
        except queue.Empty:
            pass
        self.after(50, self._pump)

    def _handle(self, body):
        parts = body.split()
        if not parts:
            return
        head = parts[0]

        # <l cab reg speedByte functMap>
        if head == "l" and len(parts) >= 5:
            try:
                cab, speed_byte, func_map = int(parts[1]), int(parts[3]), int(parts[4])
            except ValueError:
                return
            if cab != self.cab.get():
                return
            direction = 1 if speed_byte & 0x80 else 0
            raw = speed_byte & 0x7F
            speed = 0 if raw in (0, 1) else raw - 1
            self.syncing = True
            self.speed.set(speed)
            self.direction.set(direction)
            for n, var in self.func_vars.items():
                var.set(1 if func_map & (1 << n) else 0)
            self.syncing = False
            self.last_state = (speed, direction)
            self.pending_speed = None

        # <c "CurrentMAIN" mA C "Milli" "0" max "1" trip>
        elif head == "c":
            self._handle_current(parts)

        # <p0> / <p1> / <p1 MAIN>
        elif head.startswith("p") and len(head) == 2 and head[1] in "012":
            track = parts[1] if len(parts) > 1 else "ALL"
            state = {"0": "OFF", "1": "ON", "2": "OVERLOAD"}[head[1]]
            self.power_state.set(f"power: {track} {state}")
            # p2 latches the overload colour; any later p0/p1 is the all-clear.
            self.overload = head[1] == "2"
            self._refresh_current()

        # <iDCC-EX V-5.x.x ...>
        elif head.startswith("i"):
            self.status.set(body.lstrip("i").strip())

    def _log(self, text, tag="rx"):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n", tag)
        if float(self.log.index("end-1c").split(".")[0]) > 500:
            self.log.delete("1.0", "100.0")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _on_close(self):
        if self.transport:
            try:
                self.transport.send("<0>")
            except Exception:
                pass
            self.transport.close()
        self.destroy()


if __name__ == "__main__":
    ThrottleApp().mainloop()
