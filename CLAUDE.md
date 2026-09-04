# DCC-EX Native Throttle — Project Memory

Context file for Claude Code. Read this before touching `dccex_throttle.py`.

---

## 1. Goal

A self-hosted GUI throttle that speaks the **DCC-EX native command protocol**
directly to an EX-CommandStation. No App Store apps, no JMRI, no WiThrottle
bridge. Owner explicitly rejects paywalled throttle apps — everything stays
local and open.

## 2. Hardware

| Item | Detail |
|---|---|
| Command station | DCC-EX **EX-CSB1** ("CS-EXB1") CommandStation/Booster |
| MCU | ESP32, dual-core, built-in 802.11n WiFi |
| Output | Dual DCC/PWM-DC channels, 5 A each, TI DRV8874 H-bridges |
| Power | 12–25 V DC, 2.1 mm barrel |
| Display | OLED (shows AP SSID/password and status at boot) |
| USB | USB-C, serial console at **115200 baud** |
| Network | Native command port **2560**. Ships in AP mode: SSID `DCCEX_xxxxxx`, password `PASS_xxxxxx`, gateway `192.168.4.1`. Can be flipped to STA mode with EX-Installer. |

Per-machine dev environment notes live in `CLAUDE.local.md` (gitignored);
see §4 *Environment* for the rules that travel with the code.

## 3. Protocol facts that matter

- The command station is **bilingual** — it speaks both native and WiThrottle.
  The app sends `<s>` immediately on connect to pull the version banner and
  settle the station into native mode. Note: the first-command-selects-protocol
  behaviour is true of the EX-CS firmware but is *not* documented in the
  offline reference in `Documents/`, so don't cite it as spec.
- **No acquire/release.** There is no session, no loco ownership, no
  disconnect handshake. You just send commands for an address.
- **Everything is broadcast.** Any change to a loco — from *any* throttle on
  the layout — is broadcast to *all* connected clients. A client must handle
  unsolicited traffic, not request/response.
- **Track power starts Unknown.** There is no broadcast for the unknown state,
  so a throttle must flag power as unknown until it either sees a `<p...>` or
  the user commands a change. The app does this.
- Messages are `<...>` delimited. Newline is not required but is harmless and
  helps on serial.

### Commands currently used

```
<s>                       status / version  -> <iDCCEX ver / MCU / motor / build>
                          also emits <H id state> for each defined turnout
<1> <0>                   all track power on / off
<1 MAIN> <0 MAIN>         main district
<1 PROG> <0 PROG>         program district
<t cab>                   request a state re-broadcast for one loco -> <l ...>
<t cab speed dir>         throttle. speed 0-126, -1 = estop. dir 1=fwd 0=rev
<F cab func state>        function. func 0-68, state 1/0
<!>                       emergency stop ALL locos
<c>                       track current -> <c "CurrentMAIN" ...>. Polled 1/s
<R>                       read loco address on prog track -> <r address>
<R cv>                    read CV on prog track -> <v cv value>
<W addr>                  write loco address on prog track -> <w cab> / <w -1>
<W cv val>                write CV on prog track -> <r cv value>
<w cab cv val>            POM write on main. No reply at all
```

Gotchas the reference spells out:

- `<t cab speed dir>` is documented as taking `speed` 0-**127**, but the
  `<l>` encoding table only reaches speed 126. 126 is the real ceiling; the
  0-127 in the parameter list is a doc error. Do not "fix" the app to 127.
- `<F>` accepts func **0-68** (RCN-212). The old 0-28 limit belongs to the
  deprecated `<f cab byte1 byte2>` form. But `functMap` in the `<l>` broadcast
  is only 32 bits, so **F0-F31 is the practical ceiling** for anything that
  needs to stay in sync. The app exposes **F0-F28**
  (`FUNCTIONS = range(0, 29)`) as buttons **per loco tab**: each loco's
  Setup… dialog picks which functions its tab shows and gives each button a
  label. Unlabelled layouts flow ten per decade row; as soon as any visible
  button is labelled the flow drops to six per row (`_reflow_funcs`). All 29
  buttons exist per panel — hidden ones still track state from `<l>`, so
  All Functions Off covers them too. Each button is
  **per-button momentary or toggle**, flipped by right-click
  (`_func_mode_flip`; `<Button-3>` and `<Button-2>` both bound for aqua).
  Everything is persisted per loco to `~/.config/dccex-throttle.json`
  (`CONFIG_PATH`, schema `{"locos": [{name, address, toggle_funcs,
  show_funcs, labels}]}`; the pre-multi-loco `{"toggle_funcs": [...]}` file
  migrates to a single loco via `load_loco_cfgs`, and an unreadable/garbled
  file falls back to one default loco with `TOGGLE_FUNCS = {3}` — F3 is the
  owner's short whistle).
  Momentary buttons send `<F 1>` / `<F 0>` on press/release
  (`_func_momentary`); toggle buttons send one command per press,
  alternating 1/0 (`_func_toggle`, release ignored) — right for latched
  functions like lights, and the only single-toot option for sounds:
  the decoder sounds on *every* edge, so both the press/release pair and
  a timed on/off pulse tooted twice. Toggle mode shows as **underlined**
  button text (`FuncToggle.TButton`) — a font attribute, because aqua
  ignores foreground colour on ttk buttons.
  There is no latched widget state to revert on a failed
  send; `func_vars` mirrors the true state from `<l>` broadcasts, and it is
  what `_all_funcs_off` consults. Going past F31 means accepting write-only
  functions that no broadcast can ever correct.
- Functions are transmitted in NMRA groups. The station remembers previous
  settings within a group, but *"if you have never set F2, then changing F1
  WILL unset F2."* First `<F>` after power-on can clobber untouched siblings.

### Commands not yet wired into the GUI

```
<T id 1|0>                turnout throw / close
<JA> <JR> <JT>            roster / turnout / route lists (v4.2+)
<= A DCC>                 TrackManager: set track mode (DCC/DC/PROG/AUTO)
<D CABS>                  diagnostics
<#>                       max cab slots the station supports (typ. 20/30/50)
<- [cab]>                 forget one / all locos, freeing reminder slots
<m cab accel [decel]>     per-loco momentum
<JI> <JG>                 per-track current / trip lists -> <jI ...> <jG ...>
```

`<JI>`/`<JG>` are the TrackManager-era alternative to `<c>`: they report every
track (A-H) rather than MAIN only, which suits the EX-CSB1's two channels. The
catch is that the replies are bare numbers in track order with no letters, so
they only mean anything alongside a `<=>` config query. `<c>` was the simpler
starting point; `<JI>` is the upgrade path if per-channel readout is wanted.

Full reference: https://dcc-ex.com/reference/software/command-summary-consolidated.html
Offline copy with more detail: `Documents/dccex-native-protocol.md` (see §6).

### Broadcasts parsed

- `<l cab reg speedByte functMap>` — loco state. Emitted for *any* loco command
  from *any* client, and on demand via `<t cab>`.
  - `speedByte` bit 7 = direction (1 = forward).
  - Low 7 bits: `0` = stop, `1` = emergency stop, `2..127` → speed `1..126`.
  - `functMap` is a 32-bit mask, bit *n* = F*n*.
  - `reg` is the reminder-table slot, unused by the app. **`-1` means the loco
    isn't in the reminders table**; `<t cab>` does not reserve a slot until the
    loco is actually throttled.
- `<p0>` / `<p1>` / `<p2>` optionally followed by track name — power off / on /
  overload. The track field can also be `JOIN`, which the app prints verbatim.
- `<c "CurrentMAIN" current C "Milli" "0" max_ma "1" trip_ma>` — reply to `<c>`.
  A *reply*, not a broadcast: it only arrives when asked. All three useful
  numbers are in mA — reading, motor-driver capability, and the software
  circuit-breaker trip. Parse by pulling the **bare** integers rather than by
  fixed index: the filler fields (`"0"`, `"1"`) are quoted, so unquoted numbers
  are exactly `current, max, trip` in order, and the short `<c current>` form
  some builds emit still parses.
- `<iDCC-EX V-...>` — version banner.
- `<v cv value>` — prog-track CV read result (reply to `<R cv>`); value -1 =
  failed. A good read also primes the Programming tab's Value entry for
  read-modify-write.
- `<r cv value>` / `<r address>` — prog-track CV write ack / address read
  result (-1 = failed). Same opcode, disambiguated **purely by argument
  count** (2 vs 1); a good address read fills the Address entry. The legacy
  pipe-delimited `<r callbacknum|callbacksub|cv value>` form only answers the
  deprecated commands, which the app never sends.
- `<w cab>` — address write ack (reply to `<W addr>`, -1 = failed). Only the
  one-argument form is treated as an ack, so nothing collides with the
  reply-less POM `<w cab cv val>` command.

Not yet parsed, in rough order of usefulness:

- `<H id [DCC|SERVO|VPIN|LCN] ... 0|1>` — turnout state. Arrives unprompted and
  as a burst after every `<s>`.
- `<q id>` / `<Q id>` — sensor deactivated / activated.
- `<m "text">` — EXRAIL message to all throttles (5.4.0+).
- `<i id position moving>` — turntable/traverser state (5.4.0+).
- `<jA>` / `<jR>` / `<jT>` / `<jO>` / `<jP>` — replies to the `<J*>` list
  queries. Note the reply opcode is **lowercase**.
- `<* ... *>` — diagnostic text.

## 4. Current implementation

Single file, `dccex_throttle.py`. **Stdlib only** — `pyserial` is the sole
third-party import, and an optional one at that (the Serial radio button
disables itself if it's absent).

### Environment

Per-machine specifics (interpreter choices, editor config, machine list)
live in `CLAUDE.local.md`, which is gitignored and loaded automatically by
Claude Code. The rules that travel with the code:

- Run via a project `.venv` with pyserial installed
  (`python3 -m venv .venv && .venv/bin/pip install pyserial`). Any
  python3 with tkinter also runs the app, just without serial support.
- **Tk version, not Python version, decides layout correctness.** Apple's
  Tcl/Tk 8.5.9 renders at the wrong scale on modern macOS; Tk 9 lays out
  correctly. Check `tkinter.Tcl().call('info', 'patchlevel')` before
  blaming layout code.
- UI metrics are keyed off `tk windowingsystem` (`aqua` vs `x11`) in
  `_build_ui`, not off the OS: x11 gets the 16 pt fonts, the 880x45 slider
  and the `uniform="band"` row group; aqua gets 13 pt (its native widget
  size), the stock slider, and **no** uniform group — uniform makes rows 1
  and 2 *request* the taller row's height, which pushed the requested
  window (1307x1365) past a MacBook screen. A tiling WM imposes the window
  size so x11 never notices.
- Under a tiling WM the window is stretched to fill its tile, so judge
  layout by `winfo_reqwidth()`/`winfo_reqheight()`, never by actual
  window size.

### Release packaging

One-file standalone binary via PyInstaller, published as a GitHub release.
Same commands on both platforms:

```
.venv/bin/pip install pyinstaller
.venv/bin/pyinstaller --onefile --windowed --name dccex-throttle dccex_throttle.py
```

Output lands in `dist/` (gitignored along with `build/` and `*.spec`).

- **Linux** (asset `dccex-throttle-linux-x86_64`, since v0.1.0): ship the
  bare `dist/dccex-throttle`. It links the build machine's glibc, so an
  Arch-built one needs a comparably recent distro — rebuild from source
  for older systems.
- **macOS** (asset `dccex-throttle-macos-arm64.app.zip`, since v0.1.1):
  `--windowed` also emits `dist/dccex-throttle.app`; ship that, zipped with
  `ditto -c -k --keepParent` (plain `zip` loses bundle metadata). Unsigned,
  so first launch needs right-click → Open or
  `xattr -d com.apple.quarantine`. Apple Silicon only.

### Structure

- `BaseTransport` — owns a daemon reader thread. Accumulates bytes, extracts
  complete `<...>` frames with `MSG_RE`, pushes `("msg", body)` or
  `("error", text)` tuples onto a `queue.Queue`. 4 KB runaway-buffer guard.
- `TcpTransport` — `socket.create_connection`, 0.4 s recv timeout so the
  reader thread can notice the stop flag.
- `SerialTransport` — pyserial, same contract.
- `LocoPanel(ttk.Frame)` — one locomotive tab. Owns everything specific to
  a single address: the throttle widgets, function buttons, and the
  per-loco send/sync state that used to be app-global (`syncing`,
  `pending_speed`, `last_state`, `last_sent`, `active_cab`). Panels never
  touch the transport, only `app.send_cmd()`.
- `LocoSetupDialog(tk.Toplevel)` — per-loco Setup: loco name, a show
  checkbox + label entry per function, Remove This Loco. The **name
  applies live** (a trace on `name_var` renames the panel and retitles the
  tab per keystroke — owner requirement after apply-on-close read as "can't
  rename"); everything else applies on close (`apply_setup`), which also
  saves the config. **Placed over the throttle window** by the
  withdraw → build → `update_idletasks` → `geometry(WxH+x+y)` → `deiconify`
  sequence, clamped to the screen. The position has to travel with the
  *initial* map: mapping first and moving afterwards worked about one time
  in three on Hyprland (a ConfigureRequest that lands between the map and
  the surface's first frame is dropped), and the rest of the time the
  dialog sat at the monitor's top-left, where the panel bar hid the name
  row and the owner concluded renaming didn't exist. Verified 12/12 with
  `hyprctl clients -j`; don't reorder those steps. Opened by
  the panel's Setup… button, and automatically by `_add_loco` so a new
  "Loco <addr>" tab is offered a name at once (the
  double-click-on-tab shortcut was removed at owner request — it stacked
  accidental duplicates), always through **`app._open_setup`**, which
  enforces **one window per loco** (`panel.setup_dialog`; a second request
  re-focuses the existing window's name entry). Never construct one
  directly: a stale duplicate closing last re-applies its old values —
  the bug that silently reverted renames. Non-modal (no `grab_set`) so
  several locos can each have a window open; the name entry takes focus on
  open. Every close path goes through `_close()`, which frees the slot;
  `_done` skips `apply_setup` if the panel is already destroyed so an
  orphaned window can still close. `_remove_loco` refuses a panel whose
  Setup window is open (the dialog's own Remove button closes itself
  first).
- `ThrottleApp(tk.Tk)` — transport, shared UI, and the loco tab roster.
  The window is three vertical
  bands on a root grid: (0) Connection + Track Power/Current, sized to hug
  its content — no stretch, no filler whitespace; (1) a `ttk.Notebook` with
  a **Run** tab and a **Programming** tab
  (service-mode address/CV read-write, a CV29 bit editor, POM write);
  (2) the Console. Rows 1
  and 2 split the remaining height equally (`weight=1, uniform="band"`).
  Connection, power and console are deliberately outside the notebook —
  PROG power and the log matter on both tabs.
  The Run tab holds an inner notebook (`loco_nb`) of `LocoPanel`s plus a
  trailing **"+" tab**; selecting "+" creates a loco on the next free
  address (`_add_loco`). `_remove_loco` selects a neighbour *before*
  `forget()` — otherwise ttk auto-selects the next tab, which for the
  rightmost loco is "+", spawning a phantom loco. `self.active_panel`
  (updated on `<<NotebookTabChanged>>`) is what POM targets; it is tracked
  because `loco_nb.select()` still points at a loco tab even while the
  Programming tab is in front, but a widget-level attribute is simpler.
  Font policy (owner requirement): **one text size everywhere — 16 pt via
  the named fonts** (`TkDefaultFont`/`TkTextFont`/`TkHeadingFont`;
  `TkFixedFont` 13 for the console log). Every widget inherits it: labels,
  entries, buttons, tabs, radios, checks. Buttons are kept compact with
  tight style *padding*, never with a smaller font — mixed text sizes are
  exactly what the owner rejected. Func/Stop/E-STOP are the same 16 pt,
  just bold. Don't set per-widget fonts. Two `after()` loops:
  - `_pump()` every 50 ms drains the RX queue into `_handle()`.
  - `_speed_tick()` every 30 ms flushes a pending slider value, rate-limited
    by `SEND_INTERVAL` (80 ms) so dragging doesn't flood the ESP32.

### Key invariants — do not break these

All four state flags below live **per `LocoPanel`**, not on the app — each
loco tab syncs and sends independently.

- **`panel.syncing`** is set while a panel's UI is being updated from an
  inbound broadcast. Every widget callback must return early when it's true,
  or you get an infinite echo loop between the app and the command station.
- **`panel.last_state`** holds the `(speed, dir)` tuple actually transmitted.
  The speed tick compares against it to avoid duplicate sends. Only
  `_send_throttle()` commits it, and only after a successful send. `(None,
  None)` means "the loco's state is unknown", which forces the next slider
  move to transmit.
- **`panel.pending_speed` is a one-shot request, not a mirror of the slider.**
  `None` means nothing is owed to the station. Lifecycle:
  - *Armed* only by `_speed_moved()`, on real user input (it returns early
    when `syncing`).
  - *Retired* by `panel.tick()` (driven from the app's single 30 ms
    `_speed_tick` loop) on all three of its exits — sent, redundant
    (`target == last_state`), or send failed. *Every* path out must clear it.
    Leaving it armed is the bug that made the tick re-test the same value
    every 30 ms forever.
  - *Discarded* wherever the slider's intent stops being meaningful:
    `_cab_changed()` (different loco), `_stop()` / `estop_zero()` (an explicit
    stop outranks a queued speed), `sync_from_broadcast()` on an inbound `<l>`
    (the station just told us the truth), and `reset_link_state()`, which
    `_toggle_connect()` runs on every panel before `<s>`.
  The connect-time one is the subtle one. Dragging the slider while
  disconnected arms the flag with no transport to consume it, so without the
  clear, the first tick after Connect would issue `<t cab speed dir>` and the
  loco would take off with the user having touched nothing since connecting.
  **Never let a value survive from one connection into the next.**
- **`panel.active_cab`** is the address `_cab_changed` last acted on, and the
  address every send uses (never a mid-edit `cab.get()`). The
  spinbox is bound to `<FocusOut>` as well as `<Return>` and `command=`, so
  without this guard every focus change would re-zero the UI and re-request
  state. The `<l>` handler fans each broadcast out to **every** panel whose
  `active_cab` matches — two tabs on one address both stay in sync.
- **`send_cmd()` returns True only if the command reached the wire.** (Named
  `send_cmd` because `tk.Misc` already owns `send()` — Tk's inter-interpreter
  send — and overriding it trips Pylance and risks confusion.) Tk applies a
  click to the widget *before* the callback runs, so any callback that flips a
  widget and then sends must revert it on False — otherwise the UI asserts a
  state the loco was never told about, and since a failed send also tears down
  the transport, no broadcast will ever arrive to correct it. `_set_quiet()`
  does the revert under the `syncing` guard. Applies to `_all_funcs_off`,
  `_dir_toggled`, `_stop` and `_estop_all`; the last two
  also refuse to zero the slider or `last_state` on a failed send.
  `_func_momentary` is exempt: the buttons latch nothing, so there is nothing
  to revert — a release lost with the link is corrected by the next `<l>`.
- **`_read_some()` has a three-way return** and each value means something
  different to `_read_loop`:
  - `bytes` — data, append to the buffer.
  - `None` — nothing arrived before the read timed out. Keep looping.
  - `b""` — end of stream. Tears the reader down and reports a disconnect.

  So a transport must **never return `b""` for a read timeout**. This is easy
  to get wrong because the two stream types disagree about what empty means:
  `socket.recv` returns `b""` only on a real FIN (timeouts raise
  `socket.timeout`), but `serial.read` returns `b""` on *every* idle timeout.
  `SerialTransport` therefore maps empty to `None`. A serial link has no
  orderly close — the port disappearing raises `SerialException`, which
  `_read_loop`'s `except` already turns into an error event.

  This was a live bug: serial connections dropped ~0.4 s after the station
  went quiet, which is most of the time.
- All socket/serial I/O happens on the reader thread; all Tk widget access
  happens on the main thread via the queue. Never touch widgets from the
  reader thread.

### Deliberate behaviours

- Changing a panel's loco address zeroes that panel, then calls
  `panel.request_state()`
  to send `<t cab>` — the station re-broadcasts `<l>` for that address, and
  the normal inbound path syncs the widgets. The same call runs for **every**
  panel after `<s>` on connect (and for a freshly added loco tab) so each
  syncs without guessing. If the loco isn't in
  the reminders table the reply carries slot `-1` and the zeroed UI is already
  correct, so the slot field is ignored.
- A loco tab's name lives only in the config. A named tab shows **just the
  name, no address suffix** (owner requirement — the earlier "Name (addr)"
  form was rejected); a blank name shows "Loco <addr>", and an address
  change retitles only that form. Config saves happen at the
  point of every mutation (mode flip, Setup close, add/remove tab, address
  change), plus one save in `_on_close` — needed because a live-typed
  rename only reaches the file when its Setup window closes.
- The spinbox `command=` callback only fires on the arrow buttons, which is
  why the typed-address path needs the explicit `<Return>`/`<FocusOut>`
  bindings. Don't remove them.
- `STOP` sends `<t cab 0 dir>`. `E-STOP ALL` sends `<!>` — layout-wide.
- Closing the window sends `<0>` to drop track power. Remove from
  `_on_close()` if unwanted.
- The raw command box wraps bare input in angle brackets, so `D CABS` works.
- Direction is a single colour-coded toggle (green "FORWARD" / orange
  "REVERSE"), not radio buttons — an owner requirement. **Plain ASCII
  labels only**: the U+25B6/25C0 arrows went through font fallback (Noto
  Color Emoji renders them double-width on Linux), drawing far wider than
  tkfont measures and clipping the label while every measurement said it
  fit. Colour carries the state. Click flips it;
  `_refresh_dir()` paints it, and must be called after every code path that
  writes `self.direction` (`_dir_toggled`, `_cab_changed`, the `<l>`
  handler). A failed send flips it back. tk.Button, not ttk, because the
  background colour is the state indicator.
- Programming entries are validated client-side before anything hits the wire
  (`_prog_int`: CV 1-1024, value 0-255, address 1-10293); a bad entry logs an
  error and sends nothing. The result label shows "...ing" while a reply is
  outstanding and is overwritten by the parsed `<v>`/`<r>`/`<w>` reply.
- POM ("Write on Main") targets the selected **loco tab**
  (`self.active_panel.active_cab`), read at click time. It gets no reply by design — the label
  says to watch the loco.
- CV entries have a live name lookup: `CV_NAMES` (common NMRA S-9.2.2 CVs)
  plus range rules in `cv_name()` (33-46 function mapping, 67-94 speed table,
  112-256 manufacturer-specific). A grey label beside each CV entry updates
  via `trace_add` on the StringVar, and `_cv_desc()` weaves the name into
  the result line ("CV 3 (Acceleration rate) = 24"). Unknown CVs show
  nothing — no guessing.
- The CV29 bit editor exposes bits 0-5 as checkboxes; toggling only updates
  the preview label ("(not written)") — nothing is sent until Write CV29.
  **Bits 6-7 are not editable but are preserved** (`self.cv29_high`, taken
  from the last confirmed value) so a write can't clobber the
  accessory-decoder flag; before any read they default to 0, which is
  correct for loco decoders. Any `<v 29 x>` or `<r 29 x>` — including one
  from the plain CV read/write fields — re-syncs the checkboxes.
  `var.set()` doesn't fire Checkbutton commands, so the sync needs no
  `syncing` guard.

### Current display

- Polled by `_current_tick()` every `CURRENT_POLL_MS` (1 s) while connected and
  while the **Poll** checkbox is ticked. Unticking stops asking the ESP32 at
  all, not just the display updating.
- Polled traffic is **quiet in both directions** — one `<c>` per second would
  own the console. Suppression is conditional on the checkbox, so a hand-typed
  `<c>` with polling off still prints. That's the only reason `send_cmd()` has a
  `quiet` argument.
- **The bar scales to `trip_ma`, not `max_ma`.** Trip is the software circuit
  breaker; how close you are to cutting out is the number that matters, not the
  driver's theoretical ceiling. Readings above trip clamp the bar but the text
  still shows the true value.
- **`<p2>` latches `self.overload`; only a later `<p0>`/`<p1>` clears it.** Do
  not let a `<c>` reply clear it — after a trip the station often reports a low
  current, which would repaint the display as healthy while the track is dead.
- Disconnecting calls `_reset_current()`. A frozen last reading looks live.
- `self.fg_normal` caches the theme's own label colour at construction because
  **Tk 9 rejects `foreground=""`** as a reset (`TclError: unknown color name
  ""`) where Tk 8.5 accepted it. Watch for that idiom elsewhere.
- Verified against the documented reply format, not yet against real CS-EXB1
  hardware.

## 5. Likely next steps

1. ~~Multi-loco~~ — done: loco tabs (`LocoPanel`) with per-tab names,
   function subsets and labels. Still open from this item: `<#>` reports how
   many slots the station has and `<- cab>` frees them — the app never
   forgets a loco on the station side when a tab is removed.
2. Consist support — use the **CSConsist** command-station consists, not the
   deprecated in-throttle consists.
3. Programming tab polish: long-address read/write helpers built on CV17/18.
   Basic read/write/POM plumbing, reply parsing, the CV29 bit editor and the
   CV name lookup exist; `<V cv value>` verify-with-guess reads would speed
   up slow service-mode reads.
4. Turnout/accessory panel driven by `<JT>` discovery.
5. Auto-reconnect with backoff; currently a dropped link just reports and stops.
6. mDNS/bonjour discovery of the command station instead of a typed IP.
7. Parse `<H id state>` so the turnout burst after `<s>` isn't wasted.
8. Per-track current via `<JI>`/`<JG>` + `<=>` instead of MAIN-only `<c>`,
   which would show both EX-CSB1 channels separately.

## 6. Documents/ — offline protocol reference

`Documents/dccex-native-protocol.md` (~216 KB) is a consolidated offline copy
of the DCC-EX native protocol docs, compiled from the official Sphinx source
(`github.com/DCC-EX/dcc-ex.github.io`, branch `sphinx`) at the commit stamped
in its front matter. **This is the authority for protocol questions** — prefer
it over guessing, and over §3 above if the two ever disagree.

Chapters: protocol overview, WiThrottle-vs-native, API reference and parsing
rules, throttle-developer guide, the full command summary, EXRAIL, FastClock,
and the `<D>` / `<D ACK>` diagnostics.

### Build toolchain

`build.sh` → per page: `prep.py` (flatten Sphinx directives, roles and
substitutions into pandoc-friendly RST) → `pandoc -f rst -t gfm` → concatenate
→ `post.py` (rebuild the parameter lists that `|br|` collapsing flattened) →
`pandoc` → xelatex PDF.

Caveats if you ever regenerate:

- `build.sh` has hardcoded `/home/claude` paths and needs the doc repo cloned
  plus pandoc + xelatex + DejaVu fonts. It does **not** run as-is on macOS.
- `build.sh:58` assigns `title=` and never uses it — the `|Title` half of every
  `FILES` entry is dead, and headings come from each RST's own title instead.
  This is why the FastClock page renders as "Controlling EXRAIL by Time".
- `out/pandoc-warnings.log` is appended, never truncated; `parts/` is never
  cleaned.
- `prep.py`'s substitution regex runs document-wide, including over literal
  blocks. An upstream substitution whose name collides with pipe-delimited
  protocol syntax (e.g. `<r callbacknum|callbacksub|cv value>`) would be
  silently rewritten. Currently safe by luck, not design.
- `post.py` distinguishes a `\>` list marker from an escaped closing bracket by
  tracking `\<`/`\>` pairs across the line. Don't simplify that back to a
  whitespace-only regex — it corrupts literals like `<t >` and `"<1 MAIN>"`.
  Running `post.py` over the current .md is a verified no-op.
- DCC-EX also maintains a newer auto-generated command page at
  <https://dcc-ex.com/mkdocs-test/reference/serial-commands/> which may list
  commands added after this snapshot.

## 7. Working preferences

- Direct, technically precise answers. No over-explanation.
- Stay inside the stated problem — no unrequested scope creep.
- Prefer complete files as downloads over patch fragments or long terminal
  recipes when a drag-and-drop equivalent exists.
- Owner has deep embedded C/C++, ESP32, and Python background. Skip the
  beginner framing.
