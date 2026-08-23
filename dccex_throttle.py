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
    HAVE_SERIAL = True
except ImportError:
    HAVE_SERIAL = False

MAX_FUNCTION = 31             # functMap in <l> is 32 bits, so F0-F31 round-trips
MAX_SPEED = 126
SEND_INTERVAL = 0.08          # seconds between throttle updates while dragging
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

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self._pump)
        self.after(30, self._speed_tick)

    # ---------------- UI construction ----------------
    def _build_ui(self):
        pad = dict(padx=6, pady=4)

        # --- Connection -------------------------------------------------
        conn = ttk.LabelFrame(self, text="Connection")
        conn.pack(fill="x", **pad)

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
        power.pack(fill="x", **pad)
        for i, (label, cmd) in enumerate([
            ("ALL ON", "<1>"), ("ALL OFF", "<0>"),
            ("MAIN ON", "<1 MAIN>"), ("MAIN OFF", "<0 MAIN>"),
            ("PROG ON", "<1 PROG>"), ("PROG OFF", "<0 PROG>"),
        ]):
            ttk.Button(power, text=label, width=10,
                       command=lambda c=cmd: self.send(c)).grid(row=0, column=i, padx=3, pady=5)
        self.power_state = tk.StringVar(value="power: unknown")
        ttk.Label(power, textvariable=self.power_state).grid(
            row=0, column=6, padx=12, sticky="w")

        # --- Loco / throttle ---------------------------------------------
        loco = ttk.LabelFrame(self, text="Locomotive")
        loco.pack(fill="x", **pad)

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
        funcs.pack(fill="x", **pad)
        self.func_vars = {}
        cols = 6
        for n in range(0, MAX_FUNCTION + 1):
            var = tk.IntVar(value=0)
            self.func_vars[n] = var
            label = "F0 (Lights)" if n == 0 else f"F{n}"
            cb = ttk.Checkbutton(funcs, text=label, variable=var,
                                 command=lambda k=n: self._func_toggled(k))
            cb.grid(row=n // cols, column=n % cols, sticky="w", padx=8, pady=3)
        ttk.Button(funcs, text="All Functions Off", command=self._all_funcs_off).grid(
            row=(MAX_FUNCTION // cols) + 1, column=0, columnspan=2,
            sticky="w", padx=8, pady=(4, 6))

        # --- Console --------------------------------------------------------
        console = ttk.LabelFrame(self, text="Console")
        console.pack(fill="both", expand=True, **pad)
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
        if not HAVE_SERIAL:
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
        self.send("<s>")          # forces native protocol mode + returns status
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
        self._log(f"-- {why}", "info")

    # ---------------- outbound ----------------
    def send(self, cmd):
        """True if the command actually reached the wire.

        Callers that flipped a widget before sending must revert it on False,
        or the UI ends up asserting a state the loco was never told about.
        """
        if not self.transport:
            self._log("not connected", "err")
            return False
        try:
            self.transport.send(cmd)
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
        self.send(text)
        self.raw.set("")

    def _send_throttle(self, speed, direction):
        if not self.send(f"<t {self.cab.get()} {speed} {direction}>"):
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
            now = time.monotonic()
            target = (self.pending_speed, self.direction.get())
            if target != self.last_state and (now - self.last_sent) >= SEND_INTERVAL:
                self._send_throttle(*target)
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

    def _request_cab_state(self):
        """<t cab> asks the station to re-broadcast <l> for this address.

        Reply is a normal <l cab reg speedByte functMap> broadcast, so _handle
        does the sync. A reg/slot of -1 means the loco isn't in the reminders
        table yet; the zeroed UI is already the right answer in that case.
        """
        if self.transport:
            self.send(f"<t {self.active_cab}>")

    def _stop(self):
        prior = self.speed.get()
        self._set_quiet(self.speed, 0)
        self.pending_speed = None
        if not self._send_throttle(0, self.direction.get()):
            self._set_quiet(self.speed, prior)   # the loco never got the stop

    def _estop_all(self):
        if not self.send("<!>"):
            return
        self._set_quiet(self.speed, 0)
        self.pending_speed = None
        self.last_state = (0, self.direction.get())

    def _func_toggled(self, n):
        if self.syncing:
            return
        var = self.func_vars[n]
        if not self.send(f"<F {self.cab.get()} {n} {var.get()}>"):
            self._set_quiet(var, 1 - var.get())    # undo the click Tk already applied

    def _all_funcs_off(self):
        for n, var in self.func_vars.items():
            if not var.get():
                continue
            if not self.send(f"<F {self.cab.get()} {n} 0>"):
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

        # <p0> / <p1> / <p1 MAIN>
        elif head.startswith("p") and len(head) == 2 and head[1] in "012":
            track = parts[1] if len(parts) > 1 else "ALL"
            state = {"0": "OFF", "1": "ON", "2": "OVERLOAD"}[head[1]]
            self.power_state.set(f"power: {track} {state}")

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
