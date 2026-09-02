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

The UI is two tabs -- Run (throttle + functions) and Programming (service-mode
and POM CV access) -- with connection, track power and the console shared
above/below the tabs.

Commands used:
  <s>                     status / version
  <1> <0> <1 MAIN> ...    track power
  <t cab>                 request a state re-broadcast (<l ...>) for one loco
  <t cab speed dir>       throttle   speed 0-126, -1 = estop, dir 1=fwd 0=rev
  <F cab func state>      function   func 0-68 protocol; F1-F8 exposed here as
                                     momentary buttons (1 on press, 0 on release)
  <!>                     emergency stop everything
  <c>                     track current, polled 1/s while connected
  <R> <R cv>              prog track: read loco address / read CV
  <W addr> <W cv val>     prog track: write loco address / write CV
  <w cab cv val>          write CV on main (POM), no reply

Messages parsed:
  <l cab reg speedByte functMap>   loco state (from any throttle on the layout)
  <p0> <p1> <p1 MAIN>              power state (<p2> = overload)
  <c "CurrentMAIN" ...>            track current reply
  <iDCC-EX V-...>                  version banner
  <v cv value>                     CV read result (-1 = failed)
  <r cv value> / <r address>       CV write ack / address read result
  <w cab>                          address write ack (-1 = failed)
"""

import queue
import re
import socket
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    serial = None
    list_ports = None
HAVE_SERIAL = serial is not None

FUNCTIONS = range(1, 9)       # F1-F8, all momentary: on while held, off on release
MAX_SPEED = 126
SEND_INTERVAL = 0.08          # seconds between throttle updates while dragging
CURRENT_POLL_MS = 1000        # how often to ask the station for track current
MSG_RE = re.compile(rb"<([^>]*)>")

# Common NMRA S-9.2.2 CV names for the Programming tab's live lookup.
CV_NAMES = {
    1: "Primary (short) address",
    2: "Vstart -- motor start voltage",
    3: "Acceleration rate",
    4: "Deceleration rate",
    5: "Vhigh -- top speed voltage",
    6: "Vmid -- mid speed voltage",
    7: "Manufacturer version, read-only",
    8: "Manufacturer ID -- writing it resets many decoders",
    17: "Extended address high byte",
    18: "Extended address low byte",
    19: "Consist address",
    21: "Consist functions F1-F8",
    22: "Consist functions FL, F9-F12",
    23: "Acceleration adjustment",
    24: "Deceleration adjustment",
    28: "RailCom configuration",
    29: "Configuration data #1",
    30: "Error information",
    65: "Kick start",
    66: "Forward trim",
    95: "Reverse trim",
    105: "User ID #1",
    106: "User ID #2",
}


def cv_name(cv):
    """Best-effort NMRA name for a CV number, or None if unremarkable."""
    if cv in CV_NAMES:
        return CV_NAMES[cv]
    if 33 <= cv <= 46:
        return "Function output mapping"
    if 67 <= cv <= 94:
        return f"Speed table entry {cv - 66}/28"
    if 112 <= cv <= 256:
        return "Manufacturer-specific"
    return None


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
        self.cv29_high = 0             # CV29 bits 6-7, preserved from last read

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self._pump)
        self.after(30, self._speed_tick)
        self.after(CURRENT_POLL_MS, self._current_tick)

    # ---------------- UI construction ----------------
    def _build_ui(self):
        # ONE text size everywhere. The named fonts carry every widget --
        # labels, entries, buttons, tabs, radios, checks -- so nothing can
        # mismatch. Buttons are kept compact with tight padding, never with
        # a smaller font.
        for name in ("TkDefaultFont", "TkTextFont", "TkHeadingFont"):
            tkfont.nametofont(name).configure(size=16)
        tkfont.nametofont("TkFixedFont").configure(size=13)   # console log
        style = ttk.Style(self)
        style.configure("TButton", padding=(6, 3))
        style.configure("Func.TButton", font=("TkDefaultFont", 16, "bold"),
                        padding=(8, 6))
        style.configure("Stop.TButton", font=("TkDefaultFont", 16, "bold"),
                        padding=(8, 4))

        # Vertical bands: row 0 (connection + track power) hugs its content;
        # rows 1 (tabs) and 2 (console) split the remaining space equally.
        self.grid_columnconfigure(0, weight=1)
        for r in (1, 2):
            self.grid_rowconfigure(r, weight=1, uniform="band")
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="new", padx=6, pady=(4, 0))

        # --- Connection -------------------------------------------------
        conn = ttk.LabelFrame(top, text="Connection")
        conn.pack(fill="x", pady=(0, 4))

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
        power = ttk.LabelFrame(top, text="Track Power")
        power.pack(fill="x")
        for i, (label, cmd) in enumerate([
            ("ALL ON", "<1>"), ("ALL OFF", "<0>"),
            ("MAIN ON", "<1 MAIN>"), ("MAIN OFF", "<0 MAIN>"),
            ("PROG ON", "<1 PROG>"), ("PROG OFF", "<0 PROG>"),
        ]):
            ttk.Button(power, text=label, width=9,
                       command=lambda c=cmd: self.send_cmd(c)).grid(row=0, column=i, padx=3, pady=5)
        self.power_state = tk.StringVar(value="power: unknown")
        ttk.Label(power, textvariable=self.power_state).grid(
            row=0, column=6, padx=12, sticky="w")

        # --- Current draw ---------------------------------------------------
        ttk.Label(power, text="Current:").grid(
            row=1, column=0, padx=(6, 2), pady=(0, 6), sticky="e")
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

        # --- Tabs: Run / Programming -------------------------------------
        # Connection, track power and the console stay global; everything
        # loco-specific lives on one of the two tabs.
        nb = ttk.Notebook(self)
        nb.grid(row=1, column=0, sticky="nsew", padx=6, pady=4)
        run_tab = ttk.Frame(nb)
        prog_tab = ttk.Frame(nb)
        nb.add(run_tab, text="Run")
        nb.add(prog_tab, text="Programming")

        # --- Loco / throttle ---------------------------------------------
        loco = ttk.LabelFrame(run_tab, text="Locomotive")
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
        # One big toggle instead of radio buttons: click flips direction.
        # tk.Button, not ttk -- the colour is the state indicator.
        self.dir_btn = tk.Button(loco, width=16, fg="white",
                                 activeforeground="white",
                                 font=("TkDefaultFont", 16, "bold"),
                                 command=self._dir_toggled)
        self.dir_btn.grid(row=0, column=2, columnspan=2, padx=(18, 4), pady=4,
                          sticky="ew")
        self._refresh_dir()

        ttk.Button(loco, text="STOP", width=10, style="Stop.TButton",
                   command=self._stop).grid(row=0, column=4, padx=(18, 4))
        estop = tk.Button(loco, text="E-STOP ALL", width=12, bg="#c62828", fg="white",
                          activebackground="#e53935", activeforeground="white",
                          font=("TkDefaultFont", 16, "bold"),
                          command=self._estop_all)
        estop.grid(row=0, column=5, padx=4, pady=4)

        self.speed = tk.IntVar(value=0)
        self.scale = tk.Scale(loco, from_=0, to=MAX_SPEED, orient="horizontal",
                              variable=self.speed, length=880, tickinterval=21,
                              width=45, sliderlength=70,
                              resolution=1, command=self._speed_moved)
        self.scale.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 8), sticky="ew")
        loco.columnconfigure(5, weight=1)

        # --- Functions -----------------------------------------------------
        funcs = ttk.LabelFrame(run_tab, text="Functions")
        funcs.pack(fill="both", expand=True, padx=6, pady=4)
        self.func_vars = {}
        cols = 4
        for i, n in enumerate(FUNCTIONS):
            # All momentary: <F 1> on press, <F 0> on release. No variable --
            # the widget's pressed look is the feedback, and func_vars[n]
            # still tracks the real state via the <l> broadcast.
            var = tk.IntVar(value=0)
            self.func_vars[n] = var
            w = ttk.Button(funcs, text=f"F{n}", style="Func.TButton")
            w.bind("<ButtonPress-1>", lambda e, k=n: self._func_momentary(k, 1))
            w.bind("<ButtonRelease-1>", lambda e, k=n: self._func_momentary(k, 0))
            w.grid(row=i // cols, column=i % cols, sticky="nsew", padx=6, pady=5)
        func_rows = (len(FUNCTIONS) + cols - 1) // cols
        for c in range(cols):
            funcs.columnconfigure(c, weight=1)
        for r in range(func_rows):
            funcs.rowconfigure(r, weight=1)
        ttk.Button(funcs, text="All Functions Off", command=self._all_funcs_off).grid(
            row=func_rows, column=0, columnspan=2, sticky="w", padx=6, pady=(4, 6))

        # --- Programming tab ------------------------------------------------
        svc = ttk.LabelFrame(prog_tab, text="Programming Track (service mode)")
        svc.pack(fill="x", padx=6, pady=4)
        ttk.Label(svc, text="Loco must be alone on the PROG track. "
                            "Locos do not move in service mode.").grid(
            row=0, column=0, columnspan=6, sticky="w", padx=6, pady=(4, 2))

        ttk.Button(svc, text="Read Address", command=self._read_address).grid(
            row=1, column=0, padx=6, pady=4, sticky="w")
        ttk.Label(svc, text="Address:").grid(row=1, column=1, sticky="e")
        self.prog_addr = tk.StringVar()
        ttk.Entry(svc, textvariable=self.prog_addr, width=7).grid(
            row=1, column=2, sticky="w", padx=(2, 6))
        ttk.Button(svc, text="Write Address", command=self._write_address).grid(
            row=1, column=3, padx=4, pady=4, sticky="w")

        ttk.Label(svc, text="CV:").grid(row=2, column=0, sticky="e", padx=(6, 0))
        self.prog_cv = tk.StringVar()
        ttk.Entry(svc, textvariable=self.prog_cv, width=6).grid(
            row=2, column=1, sticky="w", padx=(2, 6), columnspan=2)
        ttk.Label(svc, text="Value:").grid(row=2, column=2, sticky="e")
        self.prog_val = tk.StringVar()
        ttk.Entry(svc, textvariable=self.prog_val, width=5).grid(
            row=2, column=3, sticky="w", padx=(2, 6))
        ttk.Button(svc, text="Read CV", command=self._read_cv).grid(
            row=2, column=4, padx=4, pady=4)
        ttk.Button(svc, text="Write CV", command=self._write_cv).grid(
            row=2, column=5, padx=4, pady=4)
        self.prog_cv_name = tk.StringVar()
        ttk.Label(svc, textvariable=self.prog_cv_name, foreground="#888").grid(
            row=2, column=6, sticky="w", padx=6)
        self.prog_cv.trace_add("write", lambda *_: self._cv_name_changed(
            self.prog_cv, self.prog_cv_name))

        self.prog_result = tk.StringVar(value="result: --")
        ttk.Label(svc, textvariable=self.prog_result).grid(
            row=3, column=0, columnspan=6, sticky="w", padx=6, pady=(2, 6))

        # --- CV29 bit editor -------------------------------------------------
        cv29 = ttk.LabelFrame(prog_tab, text="CV29 Bit Editor (prog track)")
        cv29.pack(fill="x", padx=6, pady=4)
        self.cv29_bits = {}
        for i, (bit, label) in enumerate([
            (0, "Reverse direction"), (1, "28/128 speed steps"),
            (2, "Analog (DC) mode"), (3, "RailCom"),
            (4, "Custom speed table"), (5, "Long address (CV17/18)"),
        ]):
            var = tk.IntVar(value=0)
            self.cv29_bits[bit] = var
            # Toggling only updates the preview; nothing is sent until Write.
            ttk.Checkbutton(cv29, text=f"{label} (b{bit})", variable=var,
                            command=self._cv29_edited).grid(
                row=i // 3, column=i % 3, sticky="w", padx=6, pady=2)
        self.cv29_text = tk.StringVar(value="CV29 = --")
        ttk.Label(cv29, textvariable=self.cv29_text).grid(
            row=2, column=0, sticky="w", padx=6, pady=(2, 4))
        ttk.Button(cv29, text="Read CV29", command=self._cv29_read).grid(
            row=2, column=1, sticky="e", padx=4, pady=(2, 4))
        ttk.Button(cv29, text="Write CV29", command=self._cv29_write).grid(
            row=2, column=2, sticky="w", padx=4, pady=(2, 4))
        ttk.Label(cv29, text="Bit 5 only selects which address is used -- "
                             "change addresses with Write Address, not here.").grid(
            row=3, column=0, columnspan=3, sticky="w", padx=6, pady=(0, 6))

        pom = ttk.LabelFrame(prog_tab, text="Program on Main (POM)")
        pom.pack(fill="x", padx=6, pady=4)
        ttk.Label(pom, text="Writes to the loco selected on the Run tab. "
                            "No reply from the station -- watch the loco.").grid(
            row=0, column=0, columnspan=5, sticky="w", padx=6, pady=(4, 2))
        ttk.Label(pom, text="CV:").grid(row=1, column=0, sticky="e", padx=(6, 0))
        self.pom_cv = tk.StringVar()
        ttk.Entry(pom, textvariable=self.pom_cv, width=6).grid(
            row=1, column=1, sticky="w", padx=(2, 6))
        ttk.Label(pom, text="Value:").grid(row=1, column=2, sticky="e")
        self.pom_val = tk.StringVar()
        ttk.Entry(pom, textvariable=self.pom_val, width=5).grid(
            row=1, column=3, sticky="w", padx=(2, 6))
        ttk.Button(pom, text="Write on Main", command=self._pom_write).grid(
            row=1, column=4, padx=4, pady=(2, 6), sticky="w")
        self.pom_cv_name = tk.StringVar()
        ttk.Label(pom, textvariable=self.pom_cv_name, foreground="#888").grid(
            row=1, column=5, sticky="w", padx=6)
        self.pom_cv.trace_add("write", lambda *_: self._cv_name_changed(
            self.pom_cv, self.pom_cv_name))

        # --- Console --------------------------------------------------------
        console = ttk.LabelFrame(self, text="Console")
        console.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 4))
        # height=5 is only the minimum -- the console's third of the window
        # is what actually sizes it. TkFixedFont, not "Menlo": Menlo only
        # exists on macOS and silently falls back on Linux.
        self.log = tk.Text(console, height=5, wrap="none", state="disabled",
                           font="TkFixedFont", background="#101418", foreground="#d8dee9")
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

    def _refresh_dir(self):
        """Paint the direction toggle from self.direction.

        Plain ASCII on purpose: U+25B6/25C0 arrows go through font fallback
        (often a double-width color-emoji glyph on Linux) and render far
        wider than tkfont measures, clipping the label. Colour carries the
        state; the text stays plain.
        """
        if self.direction.get() == 1:
            self.dir_btn.configure(text="FORWARD", bg="#2e7d32",
                                   activebackground="#388e3c")
        else:
            self.dir_btn.configure(text="REVERSE", bg="#ef6c00",
                                   activebackground="#f57c00")

    def _dir_toggled(self):
        """The toggle flips direction; a failed send flips it back."""
        new = 1 - self.direction.get()
        self._set_quiet(self.direction, new)
        self._refresh_dir()
        if not self._send_throttle(self.speed.get(), new):
            self._set_quiet(self.direction, 1 - new)
            self._refresh_dir()

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
        self._refresh_dir()
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

    def _func_momentary(self, n, state):
        """Press/release for the momentary function buttons. Nothing to revert
        on a failed send: the button has no latched state, and a release lost
        with the link leaves func_vars[n] to be corrected by the next <l>
        broadcast."""
        self.send_cmd(f"<F {self.cab.get()} {n} {state}>")

    def _all_funcs_off(self):
        for n, var in self.func_vars.items():
            if not var.get():
                continue
            if not self.send_cmd(f"<F {self.cab.get()} {n} 0>"):
                return          # link is down; leave the rest showing their real state
            self._set_quiet(var, 0)

    # ---------------- programming ----------------
    def _prog_int(self, var, lo, hi, name):
        """Parse an entry as an int in [lo, hi]; log and return None if not."""
        try:
            val = int(var.get().strip())
            if not lo <= val <= hi:
                raise ValueError
        except ValueError:
            self._log(f"{name} must be {lo}-{hi}", "err")
            return None
        return val

    def _read_address(self):
        if self.send_cmd("<R>"):
            self.prog_result.set("reading address...")

    def _write_address(self):
        addr = self._prog_int(self.prog_addr, 1, 10293, "address")
        if addr is not None and self.send_cmd(f"<W {addr}>"):
            self.prog_result.set("writing address...")

    @staticmethod
    def _cv_desc(cv):
        """'CV 3 (Acceleration rate)', or plain 'CV 3' for a nameless one."""
        try:
            name = cv_name(int(cv))
        except (TypeError, ValueError):
            name = None
        return f"CV {cv} ({name})" if name else f"CV {cv}"

    def _cv_name_changed(self, var, out):
        """Live lookup label beside a CV entry (traced on its StringVar)."""
        try:
            name = cv_name(int(var.get().strip()))
        except ValueError:
            name = None
        out.set(name or "")

    def _read_cv(self):
        cv = self._prog_int(self.prog_cv, 1, 1024, "CV")
        if cv is not None and self.send_cmd(f"<R {cv}>"):
            self.prog_result.set(f"reading {self._cv_desc(cv)}...")

    def _write_cv(self):
        cv = self._prog_int(self.prog_cv, 1, 1024, "CV")
        if cv is None:
            return
        val = self._prog_int(self.prog_val, 0, 255, "value")
        if val is not None and self.send_cmd(f"<W {cv} {val}>"):
            self.prog_result.set(f"writing {self._cv_desc(cv)}...")

    def _pom_write(self):
        cv = self._prog_int(self.pom_cv, 1, 1024, "CV")
        if cv is None:
            return
        val = self._prog_int(self.pom_val, 0, 255, "value")
        if val is not None:
            self.send_cmd(f"<w {self.cab.get()} {cv} {val}>")

    def _cv29_value(self):
        """Compose CV29 from the checkboxes plus the preserved high bits."""
        val = self.cv29_high
        for bit, var in self.cv29_bits.items():
            if var.get():
                val |= 1 << bit
        return val

    def _cv29_edited(self):
        self.cv29_text.set(f"CV29 = {self._cv29_value()} (not written)")

    def _cv29_read(self):
        if self.send_cmd("<R 29>"):
            self.prog_result.set("reading CV 29...")

    def _cv29_write(self):
        val = self._cv29_value()
        if self.send_cmd(f"<W 29 {val}>"):
            self.prog_result.set(f"writing CV 29 = {val}...")

    def _cv29_sync(self, value):
        """Mirror a confirmed CV29 (from <v 29 x> or <r 29 x>) into the editor.

        Bits 6-7 aren't editable (reserved / accessory-decoder flag) but are
        preserved so a later write doesn't clobber them. var.set() does not
        fire Checkbutton commands, so no syncing guard is needed here.
        """
        self.cv29_high = value & 0xC0
        for bit, var in self.cv29_bits.items():
            var.set(1 if value & (1 << bit) else 0)
        self.cv29_text.set(f"CV29 = {value}")

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
            self._refresh_dir()
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

        # <v cv value> -- CV read result from the prog track, -1 = failed
        elif head == "v" and len(parts) >= 3:
            cv, value = parts[1], parts[2]
            if value == "-1":
                self.prog_result.set(f"{self._cv_desc(cv)} read FAILED")
            else:
                self.prog_result.set(f"{self._cv_desc(cv)} = {value}")
                self.prog_val.set(value)   # prime for a read-modify-write
                if cv == "29" and value.isdigit():
                    self._cv29_sync(int(value))

        # <r cv value> -- CV write ack; <r address> -- address read result
        elif head == "r":
            if len(parts) >= 3:
                cv, value = parts[1], parts[2]
                self.prog_result.set(
                    f"{self._cv_desc(cv)} write FAILED" if value == "-1"
                    else f"{self._cv_desc(cv)} written: {value}")
                if cv == "29" and value.isdigit():
                    self._cv29_sync(int(value))
            elif len(parts) == 2:
                addr = parts[1]
                if addr == "-1":
                    self.prog_result.set("address read FAILED")
                else:
                    self.prog_result.set(f"loco address = {addr}")
                    self.prog_addr.set(addr)

        # <w cab> -- address write ack (the POM <w cab cv val> has no reply)
        elif head == "w" and len(parts) == 2:
            addr = parts[1]
            self.prog_result.set("address write FAILED" if addr == "-1"
                                 else f"address written: {addr}")

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
