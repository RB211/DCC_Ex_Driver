---
title: "DCC-EX Native Command Protocol -- Consolidated Reference"
subtitle: "Compiled from the official DCC-EX documentation (rev 70040c2, 2026-08-02)"
date: "2026-08-23"
---

# About This Document

This is an offline compilation of the DCC-EX EX-CommandStation **native command
protocol** documentation, assembled from the official DCC-EX documentation
source (`github.com/DCC-EX/dcc-ex.github.io`, branch `sphinx`, commit `70040c2`,
dated 2026-08-02). Content is (c) the DCC-EX team and is licensed GPL-3.0.

Source pages included:

* `docs/throttles/protocols.rst`
* `docs/reference/software/withrottle-vs-native-commands.rst`
* `docs/reference/developers/api.rst`
* `docs/throttles/tech-reference.rst`
* `docs/reference/software/command-summary-consolidated.rst`
* `docs/exrail/exrail-command-reference.rst`
* `docs/ex-fastclock/cs-commands.rst`
* `docs/reference/tools/diagnostic-d-command.rst`
* `docs/reference/tools/diagnostic-d-ack-command.rst`

Canonical online versions live at <https://dcc-ex.com/>. Note that DCC-EX
maintains a newer auto-generated command page at
<https://dcc-ex.com/mkdocs-test/reference/serial-commands/> which may list
commands added after this snapshot.

\newpage


\newpage

# WiThrottle Server, Web Server, DCC-EX Native Protocol Explained

There are several competing standards and ways to connect external software such as Throttles (Controllers) to the EX‑CommandStation directly or indirectly through JMRI. These standards are called "protocols" and the definition and instructions for how to implement them is called an API (Application Programming Interface). There is the wiThrottle Protocol API using a wiThrottle Server, the JMRI API using a Web Server, and the DCC-EX API using DCC-EX Native Commands. You need to know that the language your throttle uses will work with how you want to connect to your Command Station.

## The DCC-EX Native Protocol

The first way to connect to EX‑CommandStation is to use our DCC-EX Native Protocol. This is the set of commands that tell the Command Station how to control your trains. EX‑CommandStation understands simple command surrounded by brackets like this: "\<1 MAIN\>". That command turns your main track power on.

Since this is just sending characters back and forth across a serial connection, anything that can connect to an Arduino through a USB cable or one of the other serial ports using WiFi of Bluetooth can send DCC-EX Native Commands to the Command Station. This method is fast, direct, and can take advantage of special features that exist only in EX‑CommandStation. You can even connect using the Arduino IDE Serial Monitor or connect to our WiFi with a terminal program like PuTTY and type DCC-EX Native Commands manually. Our EX‑WebThrottle, JMRI and throttles (controllers) like Engine Driver, *DCCpp CAB* and *DigiTrainsPro* send commands in DCC-EX Native format.

Refer to this list for the Throttles (Controllers) that are known to support the DCC-EX Native Protocol.

## The WiThrottle Server

The wiThrottle Protocol is the proprietary protocol developed by Brett Hoffman at <https://www.WiThrottle.com> . Like the DCC-EX Native Protocol, is consists of messages composed of strings of text characters sent across a serial connection that tell the Command Station how to control your layout. The command "PPA1", for example turns the power on in WiThrottle. It can be confusing, but WiThrottle can refer to the protocol (as in wiThrottle Server or WiThrottle compatible), but it also refers to the iOS throttle App called "WiThrottle" (it stands for WiFi Throttle).

EX‑CommandStation allows you to use the "wiThrottle Server" built into JMRI and other software and have them connect to your Command Station via a USB or serial connection, but EX‑CommandStation also implements a wiThrottle Protocol server in our Command Station software itself. A "server" is just a fancy way of saying that there is software running inside JMRI and EX‑CommandStation that can understand WiThrottle commands and "serve" or "service" clients that want to connect and send WiThrottle commands. The ability of EX‑CommandStation to natively "speak" WiThrottle means you can directly connect a wiThrottle Protocol compatible Throttle (aka CAB) via WiFi or Bluetooth to the Command Station and run trains. But you can still connect to JMRI WiThrottle instead and connect JMRI to EX‑CommandStation with a USB cable. So EX‑CommandStation is bi-lingual, we speak DCC-EX AND wiThrottle Protocol! Apps like Engine Driver and wiThrottle for iOS send commands in the WiThrottle format.

Refer to this list for the Throttles (Controllers) that are known to support the wiThrottle Protocol.

## The JMRI WEB Server

JMRI has two kinds of servers you can connect to built into the JMRI software. We already mentioned the wiThrottle Server, but JMRI also has a WEB Server. Devices can connect to JMRI and send commands like it would to a WEB page. This is yet another protocol and is supported by throttles like DigiTrainsPro. When connecting using a throttle that uses the WEB Server, you connect your throttle to that via WiFi, and then connect to EX‑CommandStation with a USB or Serial connection.

Refer to this list for the Throttles (Controllers) that are known to support the JMRI Web Server Protocol.

## A Note about WiFi Dropped Connections

Phones and laptop like to think they are "smart" and want to connect you to the strongest signal and to a network that has internet capability. If you use the EX‑CommandStation as an Access Point (AP), which doesn't connect to the internet, and you connect to EX‑CommandStation with your throttle, your device may disconnect you from the Command Station without you knowing and without your permission. You should turn off the option to "automatically connect" to your home network. You may even have to "forget" your home network when you are using your wireless device to connect to EX‑CommandStation. If you would rather, you can change settings in your config.h file to connect to your home network as a client instead running as an AP, and then have your throttle devices find the Command Station by its IP Address on your home network. You can find out more about that in Wifi Setup


\newpage

# WiThrottle Protocol VS DCC-EX Native Commands

EX‑CommandStation supports both the **WiThrottle protocol** and the **DCC-EX Native protocol / commands**.

This page describes the difference between the **WitThrottle Protocol** and the **DCC-EX Native protocol / commands**.

## WiThrottle

'WiThrottle' is a trademark owned by Brett Hoffman.

'WiThrottle' is also an [iOS app](https://www.withrottle.com/html/home.html) developed by Brett Hoffman which has similar capabilities to Engine Driver.

The 'WiThrottle protocol' is a communications protocol developed by Brett Hoffman. It is used by JMRI, Engine Driver, the WiThrottle app and a number of other apps and DCC Command Stations.

### WiThrottle Servers

WiThrottle stands for 'WiFi Throttle', and a 'WiThrottle Server' is just software running on your JMRI computer, DCC-EX EX-CommandStation, or dedicated device. It's called a 'Server' because it allows you to connect to it and it 'serves', or services, requests from another application. That application is called a 'Client'.

The wiThrottle Protocol itself is a standard for how WiFi throttles can communicate with the WiThrottle Server, much like the DCC standard is a standard for how data packets communicate with decoders. What this means for you, is that Engine Driver and other apps can talk to any WiThrottle compatible server, which in turn can talks to your DCC encoders in your locos.

## DCC-EX Native protocol / commands

When the DCC-EX team designed the **DCC-EX** EX‑CommandStation they found the wiThrottle Protocol too limiting and came up with a new protocol referred to originally as **DCC++** but later as DCC-EX Native Protocol or DCC-EX Native Commands.

Engine Driver, EX‑WebThrottle, JMRI and a few other apps can use the more powerful **DCC-EX Native Protocol** when connecting to a **DCC-EX** EX‑CommandStation.

Engine Driver can also use the **DCC-EX Native Protocol** to connect to a **DCC-EX** EX‑CommandStation via JMRI but you need to enable the **'DCC++ over TCP Server'** in the **'DCC++'**' menu in **Decoder-Pro**.

------------------------------------------------------------------------

## Which Should You Use?

The **WiThrottle Protocol** is adequate for running trains, throwing turnouts/points and selecting Routes.

What the **WiThrottle Protocol** can't do is *CV programming*, *Track Manager changes*, and *system configuration*.

The **DCC-EX Native Commands** can do these and more.

So if you have the option to use a controller that uses the **DCC-EX Native Commands** it is worthwhile doing so. However if you can't then the **WiThrottle protocol** is just fine for running the average layout.

You can refer the throttle/controller table to see which controllers support **DCC-EX Native Commands**.


\newpage

# DCC-EX Native API Reference

This page documents the API syntax and usage for EX‑CommandStation.

The current API has resulted from a mix of new commands and commands inherited from the original DCC++ code base, and therefore there are some noted exceptions to the syntax, however all new commands and responses must conform to the correct syntax.

<div class="note">

<div class="title">

Note

</div>

Legacy commands and responses that do not comply with this documented syntax will be deprecated in future versions.

</div>

If you are looking for information on the WiThrottle protocol, you will find that documented on the [JMRI website](https://www.jmri.org/help/en/package/jmri/jmrit/withrottle/Protocol.shtml) .

For detailed information on the various commands and responses available with EX‑CommandStation, refer to the Command summary consolidated page.

## 1. API Client definition

This API reference applies to any API client that makes use of these commands and responses.

API clients may include:

- Throttles (both wired and wireless)
- JMRI
- Other integrations (e.g. RedHat)

## 2. Serial port and WiFi/Ethernet monitoring

The input collectors must monitor the serial ports on a byte by byte basis, look for a beginning `<` with ending `>`, and ignore anything outside that before passing commands in for parsing.

The WiFI or ethernet collectors work on a per-transmission basis and the first byte of input determines whether the transmitted block gets sent for parsing as an API or WiThrottle command or response.

**Any input received that an API client does not understand must be discarded and ignored.**

## 3. General API command usage and responses

API commands are to be sent using the message format outlined below, with responses conforming to the same format.

Due to the nature of EX‑CommandStation being able to be operated by multiple API clients concurrently combined with the fact there is no unique client identifier, there is no guarantee that a response received directly after a command is sent is related. Care must be taken to take this into account.

To repeat from above, any input received that an API client does not understand should be discarded and ignored.

### 3.1. Command responses

Command responses should conform to the syntax standard to ensure they are processed correctly by API clients.

### 3.2. Broadcast responses

Broadcast information is sent to all API clients along with WiThrottle responses on the understanding that API clients will discard and ignore any responses they do not understand.

It is mandatory that an API client accepts and ignores a broadcast it doesn't understand.

### 3.3. Diagnostics and other responses

If diagnostic commands are enabled, these are sent to the USB serial port.

If you connect an API client to the USB serial port, you will get these correctly wrapped but do not expect to understand them.

If, however, WiFi debug is enabled, or the `<+>` command is used, then the wrapping can no longer be guaranteed as the wifi traffic may contain `*>`.

## 4. General Message Format

A DCC-EX API message consists of a leading `<` symbol, a single character OPCODE, zero to n parameters separated by spaces, and a terminating `>` symbol:

`<OPCODE Param1 Param2 … ParamX>`

Messages cannot be nested, and a second `<` inside a message constitutes a syntax error.

## 5. Error and empty responses

A command sent that is invalid has a response of `<X>`.

Memory limitations prohibit more detailed error messages.

## 6. Parameter values

There are three types of parameters in use:

### 6.1. Keyword

These are a consecutive sequence of one or more non-blank characters consisting of `a-z`, `A-Z`, `0-9`, or `_`, e.g. "JOIN", "WIFI", "ON", "SPEED28".

Keyword parameters are internally hashed to created integers and may start with any of these characters. The EX‑CommandStation code does not differentiate between keywords and numbers internally.

For example, a keyword of "3RAIL" would be valid if it were to be implemented.

### 6.2. Numeric

These are a consecutive sequence of one or more digits, with an optional leading `-` to indicate a negative value. Unless noted in [a.1. parameter values](#a.1.-parameter-values), these numbers are base10.

### 6.3. String

These are surrounded by a leading and trailing `"` and may contain text including spaces e.g. "This is a turnout description".

## Appendix A. Exceptions

### A.1. Parameter values

Due to legacy code and backwards compatibility requirements, there are two OPCODES that expect hexadecimal parameter values.

These are the `<M>` and `<P>` commands documented in the Write direct dcc packet section of the Command Reference.

## Appendix B. Suggested parameter parsing sequence

To obtain the parameters:

### B.1. Obtain the OPCODE

The first level of parsing is to obtain the single character, case sensitive OPCODE which is preceded by a `<` character.

### B.2. Obtain the parameters

The second level of parsing takes the next non-blank parameter along with each blank separated parameter and turns them into integers. There are no decimal point or float inputs. A prefix `-` may be used.

### B.3. Example command and response

A simple example is sending an API command to retrieve the list of defined turnouts.

The command to retrieve the list of defined turnouts is `<JT>`.

Using our syntax standard, "J" is the OPCODE, and "T" is the parameter.

The response for this command will look something like `<jT 1 17>`.

Using our parsing sequence, we obtain the OPCODE "j", with the subsequent parameters being "T", "1", and "17".

## Appendix C. Further information

### C.1. Keyword parameters are not case sensitive

Unlike OPCODES, keyword parameters are not case sensitive.

As noted, parameters containing `a-z`, `A-Z`, or `_` are hashed to create integers which results in commands such as `<D WIFI ON>` being treated identically to `<D wifi on>`.


\newpage

# Technical Reference for Throttle Developers

This page is intended to capture relevant information to assist those who develop throttles compatible with EX‑CommandStation using the DCC-EX Native Protocol, not the wiThrottle Protocol.

This page should be read in conjunction with the Api in order to understand how to send and parse DCC-EX API commands correctly, and ignore any irrelevant commands.

## Considerations for throttle developers

For anyone developing a throttle or controller application, these considerations should be taken into account:

- Refer to the Api
- Refer to the Command summary consolidated
- A throttle/controller MUST accept and ignore anything it does not understand
- Track power state has three possible states: On, Off, and Unknown
- There is no concept of a throttle 'acquiring' a loco. Simply, commands for a loco are sent to the Command Station, and the Command Station 'broadcasts' the status of any/every loco to every throttle any time a change is made to a loco.
- There is no concept of the throttle disconnecting from the Command Station.

## DCC-EX Native command library - DCCEXProtocol

For throttle developers that want to focus on throttle features and functionality, the DCC-EX team have now released an Arduino library that communicates with EX‑CommandStation via the native DCC-EX commands.

This library exposes numerous methods to interact with the EX‑CommandStation and the various objects including locos, turnouts/points, routes, and turntables.

For further information, refer to the [DCC-EX Native command library - DCCEXProtocol](https://dcc-ex.com/DCCEXProtocol/index.html) documentation.

## Responding to appropriate information

In addition to understanding the specific throttle commands details on this page, throttles/controllers also must understand and respond appropriately to **broadcasts** sent from the DCC-EX API.

These are the *key* broadcast responses that should be understood:

- `<p X [MAIN|PROG|JOIN]>` - When a throttle issues a track power command, this response is sent as a broadcast (see Power management)
- `<r address>` - When a loco address is read on the programming track, the address is sent as a broadcast (see Reading/writing configuration variables (cvs) - programming track)
- `<l cabid slot speed/dir func>` - When throttles send loco commands, this is sent as a broadcast (see Cab (loco) commands)

These broadcast responses should be understood if your controller deals with turnouts/points and sensors:

- `<H id [DCC|SERVO|VPIN|LCN] ... [0|1]>` - When turnouts are closed/thrown, this response is broadcast (see Turnouts/points)
- `<[q|Q] id>` - When sensors are deactivated/activated, this response is broadcast (see Sensors)
- `<m "text">` - **New in 5.4.0** - A message can be sent to all throttles using EXRAIL (see MESSAGE( "msg" ) - Writes a message to all clients)
- `<i id position moving>` - **New in 5.4.0** - Broadcasts if the new turntable/traverser objects are implemented (see Turntables/traversers).

### Working with track power states

Track power can be On, Off, or Unknown. There is no broadcast of an Unknown power state though, meaning a throttle/controller must start with track power flagged as Unknown.

The throttle should only flag the power state as On or Off when either:

- A power broadcast is received from the EX‑CommandStation `<p...>`
- The throttle user selects to turn track power on or off

### Key Throttle commands

Key throttle specific commands are summarised here, refer below for elaboration on the details with examples. Refer to the Command summary consolidated for detailed information.

| Command                 | Response                                                    | Description                                                                                                              |
|-------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `<t cabid speed dir>`   | `<l cabid slot speedbyte functionMap>` (Broadcast)          | Sets a cab (loco) speed and direction. (See below for the response)                                                      |
| `<t cabid>`             | `<l cabid slot speedbyte functionMap>` (Broadcast)          | Requests a deliberate update of cab (loco) speed/functions                                                               |
| `<F cabid funct state>` | `<l cabid slot speedbyte functionMap>` (Broadcast)          | Turns cab (loco) decoder functions ON and OFF (See below for the response.)                                              |
| `<JT>`                  | `<jT id1 id2 id3 ...>`                                      | Returns the defined turnout IDs                                                                                          |
| `<JT id>`               | `<jT id state "[description]">`                             | Returns the ID, state, and description of the specified turnout ID                                                       |
| `<JA>`                  | `<jA id1 id2 id3 ...>`                                      | Returns the defined automation and route IDs                                                                             |
| `<JA id>`               | `<jA id type "[description]">`                              | Returns the ID, type (A=automation or R=route), and description of the specified automation/route ID                     |
| `<JR>`                  | `<jR id1 id2 id3 ...>`                                      | Returns the defined roster entry IDs                                                                                     |
| `<JR id>`               | `<jR id "description" "function1/function2/function3/...">` | Returns the ID, description, and function map of the specified roster entry ID                                           |
| `<JO>`                  | `<jO id1 id2 id3 ...>`                                      | Returns the defined turntable IDs                                                                                        |
| `<JO id>`               | `<jO id type position position_count "[description]">`      | Returns the ID, type (0=DCC or 1=EXTT), current position, position count, and description of the specified turntable ID  |
| `<JP id>`               | `<jP id index angle "[description]">`                       | Returns the turntable ID, position index, angle, and description of each defined position for the specified turntable ID |

------------------------------------------------------------------------

### Additional Details

Refer to the Command summary consolidated for detailed information on these commands.

#### Setting cab (loco) status

`<t cabid speed dir>` - Sets a cab (loco) speed and direction. (See below for the response.)

`<F cab funct state>` - Turns cab (loco) decoder functions ON and OFF. (See below for the response.)

#### Obtaining loco (cab) status

`<t cabid>` - Requests a deliberate update on the cab speed/functions in the same format as the cab broadcast.

> Example response:
>
> - `<l cabid slot speedbyte functionMap>` - Note that a slot of -1 indicates that the cab is not in the reminders table and this command will not reserve a slot until such time as the cab is throttled.
>
> Where:
>
> - cabid = Loco's DCC address
>
> - slot = Position in the reminders table (for the convenience of slot managers later)
>
> - speedbyte = The DCC packet speed bye including the direction bit (NOT the same as the DCC-EX speed)
>
>   > - reverse - 2-127 = speed 1-126, 0 = stop
>   > - forward - 130-255 = speed 1-126, 128 = stop
>
> - functionMap = Binary map of which functions are ON ( 1=F0, 2=F1, 3=F0&F1 etc.)
>
> The above is not a direct response, but rather as a broadcast that will be triggered as a result of any throttle command being issued by any device for the cab(loc) in question.

#### Turnouts/Points

The conventional turnout definition commands and the `<H>` responses do not contain information about the turnout description which may have been provided in an EXRAIL script. A turnout description is much more user friendly than the identifier (e.g. T123), and having a list helps the throttle UI build a suitable set of buttons.

`<JT>` - Returns a list of turnout IDs. The throttle should be uninterested in the turnout technology used but needs to know the IDs it can throw/close and monitor the current state.

> Example response:
>
> - `<jT 1 17 22 19>` - Turnout IDS 1, 17, 22, and 19 are defined.

`<JT 17>` - Returns the description for turnout ID 17, and the status of T=thrown or C=closed.

> Example responses:
>
> - `<jT 17 T "Coal yard exit">` - Description "Coal yard exit" plus state is thrown.
> - `<jT 17 C "Coal yard exit">` - Description "Coal yard exit" plus state is closed.
> - `<jT 17 C "">` - Indicates turnout description not defined, and state is closed.
> - `<jT 17 X>` - Indicates turnout unknown (or possibly hidden.)

<div class="note">

<div class="title">

Note

</div>

It is still the throttles responsibility to monitor the status broadcasts. Also note that turnouts marked in EXRAIL with the HIDDEN keyword instead of a "description" will NOT show up in these commands.

</div>

<div class="note">

<div class="title">

Note

</div>

*Note from the author:* The existing broadcast is messy and needs cleaning up, however, I'm not keen on dynamically created/deleted turnouts so I have no intention of providing a command that indicates the turnout list has been updated since the throttle started. - Chris Harlow

</div>

#### Automations/Routes

A throttle needs to know which EXRAIL Automations and Routes it can show the user.

`<JA>` - Returns a list of Automations/Routes.

> Example response:
>
> - `<jA 13 16 23>` - Indicates route/automation ids 13, 16, and 23 are defined.

`<JA 13>` - Returns information for route/automation ID 13 including the description, and if it is a route (R) or automation (A).

> Example responses:
>
> - `<jA 13 R "description">` - Returns the description for ID 13, and that it is a route.
> - `<jA 13 A "description">` - Returns the description for ID 13, and that it is an automation.
> - `<jA 13 X>` - Indicates ID 13 is not found.

New in version 5.4

Route states can now also be broadcast via EXRAIL, allowing throttles to respond when they are active/inactive or hidden. Throttle developers should now respond to (or ignore if not implemented) the `<jB ...>` broadcasts.

This broadcast is in the format:

`<jB id param>` where:

- <span class="title-ref">id</span> is the ID of the route or automation (obtained via the `<JA>` commands above)

- <span class="title-ref">param</span> is one of the following:

  - 0 - indicates the route/automation is currently inactive
  - 1 - indicates the route/automation is currently active
  - 2 - indicates the route/automation should be hidden/unavailable
  - "text" - some text that should be display to the user

  Example broadcasts:

  - `<jB 13 0>` - indicates route/automation ID 13 is inactive
  - `<jB 13 1>` - indicates route/automation ID 13 is active
  - `<jB 13 2>` - indicates route/automation ID 13 should be hidden
  - `<jB 13 "Route 13">` - indicates route/automation ID 13's label/description should be set to "Route 13"

To see how these are implemented in EXRAIL, refer to Flow control.

##### What's the difference?

A **ROUTE** is just a call to an EXRAIL ROUTE, traditionally to set some turnouts or signals but can be used to perform any kind of EXRAIL function, but is not expecting to know the loco ID.

- A route can be triggered by sending, for example, `</START 13>`.

An **AUTOMATION** is a handoff of the last accessed loco ID to an EXRAIL AUTOMATION which would typically drive the loco away.

- An automation expects a start command with a cab ID, for example `</START 13 3>`.

#### Roster Information

`<JR>` - Requests a list of cab IDs from the roster.

> Example responses:
>
> - `<jR 3 200 6336>` - Returns the roster entry IDs 3, 200, and 6336 are defined.
> - `<jR>` - Indicates no roster entries are defined.

`<JR 200>` - Returns the roster name function map for roster ID 200.

> Example response:
>
> - `<jR 200 "Thomas" "whistle/*bell/squeal/panic">` - Returns the defined description "Thomas" with each defined function's name. Refer to the EXRAIL ROSTER command for function map format.

#### Turntables/Traversers

A new feature has been added to support control of turntables/traversers from throttles, including the ability for throttles to "draw" turntable positions as defined to support graphical operation. If EXRAIL commands are used to define turntables and their associated positions, a description for the turntable as well as each position is able to be defined.

Note that to obtain a complete definition for a turntable/traverser, the turntable object needs to be queried first (`<JO id>`) followed by the position query (`<JP id>`) to obtain all defined positions for the object.

`<JO>` - Returns a list of turntable IDs.

> Example response:
>
> - `<jT 1 2>` - Turntable IDs 1 and 2 are defined.

`<JO 1>` - Returns details of turntable ID 1.

> Example responses:
>
> - `<jO 1 0 1 5 "DCC Turntable">` - DCC turntable type currently at position 1, with 5 defined positions and a description "DCC Turntable".
> - `<jO 1 1 0 11 "EX-Turntable">` - EX-Turntable type currently at the home position (0), with 11 defined positions and a description "EX-Turntable"

`<JP 1>` - Returns all positions for turntable ID 1.

> Example responses (will return all positions):
>
> - `<jP 1 0 0 "">` - Position 0, unused for DCC turntables, "home" for EX-Turntable
> - `<jP 1 1 100 "Turntable position 1">` - Position 1, 10 degrees from home
> - `<jP 1 2 1800 "Turntable position 2">` - Position 2, 180 degrees from home

## Commands to avoid

- `<f cab func1 func2>` - Use `<F cab function 1/0>` instead
- `<t  slot cab speed dir>` - Just drop the slot number
- `<T commands>` - other than `<T id 0/1>`
- `<D>` - If the throttle developer sees the need to obtain info which is \<D\> only please contact us to get a better way to do it


\newpage

# DCC-EX Native Commands Summary Reference

This page describes all the DCC-EX Native Commands that the EX‑CommandStation supports.

<div class="seealso">

Also refer to our new, currently incomplete, web site for additional information on the commands described here: [DCC-EX Command Station Native Commands](https://dcc-ex.com/mkdocs-test/reference/serial-commands/) . Some commands that have only been added recently *may not be covered on this page*, but may be included on the new web site page as the process is automated directly from the code.

</div>

## Conventions used on this page

- `<` and `>` - All DCC-EX commands are surrounded by these characters to indicate the beginning and end, these must always be included
- First letter or number - These are called OPCODES, are case sensitive, and must be specified as directed, e.g. `1`, `c`, or `-`
- CAPITALISED words - These are parameters referred to as keywords, and should be specified as directed, e.g. `MAIN` (note these are not case sensitive, however capitalising makes them easier to distinguish from other parameters)
- lowercase words - These are parameters that must be provided or are returned, with multiple parameters separated by a space " ", e.g. `cab`
- Square brackets `[]` - Parameters within square brackets `[]` are optional and may be omitted, and if specifying these parameters, do not include the square brackets themselves
- \| - Use of the \| character means you need to provide one of the provided options only, for example `<0|1 MAIN|PROG|JOIN>` becomes either `<0 MAIN>` or `<1 MAIN>`
- `0|1` DIRECTION: 1=forward, 0=reverse.

## Common Elements / Parameters

The following are element / parameters that are common across multiple commands and are described here for ease of reference.

<table>
<thead>
<tr class="header">
<th>Parameter</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>cab</strong> or <strong>loco</strong></td>
<td>The short (1-127) or long (128-10293) address of the engine decoder. (This has to be already programmed in the decoder.) Note: DCC-EX commands do not distinguish between short and long DCC addresses, so you can use the same command format for both.</td>
</tr>
<tr class="even">
<td><strong>speed</strong></td>
<td>0-127 or -1 for Emergency Stop</td>
</tr>
<tr class="odd">
<td><strong>dir</strong> or <strong>direction</strong></td>
<td>One of
<ul>
<li>1=forward</li>
<li>0=reverse</li>
</ul></td>
</tr>
<tr class="even">
<td><strong>speedByte</strong></td>
<td>Speed in DCC speedstep format. This is an encoded (1-7 bits) byte. The single value incorporates both speed and direction, with the following values:
<ul>
<li>reverse - 2-127 = speed 1-126, 0 = stop, 1 = Emergency Stop</li>
<li>forward - 130-255 = speed 1-126, 128 = stop, 129 = Emergency Stop</li>
</ul></td>
</tr>
<tr class="odd">
<td><strong>id</strong></td>
<td>The numeric ID (0-32767) assigned to an element to control. <em>ids</em> are generally unique within the element type, but not across element types. (NOTE: <em>ids</em> are shared between Turnouts/Points, Sensors and Outputs)</td>
</tr>
<tr class="even">
<td><strong>vpin</strong></td>
<td>Generally, the pin number of the physical input or output GPIO to receive information from or to control. <em>vpins</em> are normally assigned to an <em>id</em> to use in subsequent commands. For GPIOs on the microcontroller, this is the same as the pin number. For servo outputs and I/O expanders, it is the pin number defined for the HAL device (if present), for example 100-115 for servos attached to the first PCA9685 Servo Controller module, 200-215 for the second PCA9685 Servo Controller module, 300-315 for the first PCA9685 I/O Expander module, and 400-415 for the second PCA9685 I/O Expander module.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

## Controlling the EX-CommandStation

### Power Management

Also see [System Information](#system-information) for retrieve command station power information.

#### `<onOff [track]>` - Turn power on or off to all or specific tracks

Also allows joining the MAIN and PROG tracks together.

> *Parameters:*  
>
> - **onOff:** one of
> - 1 = on
> - 0 = off
>
> - **track:** one of
> - blank = Both Main and Programming Tracks
>
> - MAIN = Main track
>
> - PROG = Programming Track
>
> - JOIN = Join the Main and Programming tracks temporarily  
>   Note: While `<1 JOIN>` is valid, `<0 JOIN>` is not.
>
> - A = Track A
>
> - B = Track B
>
> - C = Track C
>
> - D = Track D
>
> - E = Track E
>
> - F = Track F
>
> - G = Track G
>
> - H = Track H
>
> *Response:*
>
> > The following is not a direct response, but rather a broadcast that will be triggered as a result of any power state changes.
> >
> > `<pOnOFF [track]>`
>
> *Notes:*
>
> - The use of the JOIN function allows the DCC signal for the MAIN track to also be sent to the PROG track. This allows the prog track to act as a siding (or similar) in the main layout even though it is isolated electrically and connected to the programming track output.
>
>   However, it is important that the prog track wiring be in the same phase as the main track i.e. when the left rail is high on MAIN, it is also high on PROG. You may have to swap the wires to your prog track to make this work.
>
> - If you drive onto a programming track that is "joined" and enter a programming command, the track will automatically switch to a programming track. If you use a compatible Throttle, you can then send the join command again and drive off the track onto the rest of your layout!
>
> - In some split Motor Shield (also referred to as a 'Motor Controller', 'Motor Driver' or Motor Board') hardware configurations JOIN will not be able to work.
>
> - While `<1 JOIN>` is valid, `<0 JOIN>` is not.
>
> *Examples:*  
> all tracks off: `<0>` all tracks on `<1>` join: `<1 JOIN>`
>
> *Example Responses:*  
> all tracks off: `<p0>` all tracks on `<p1>` join: `<p1 JOIN>`

#### `<D RESET>` - Re-boot the command Station

> *Response:* N/A

#### `<J I> <JI>` - Request current values list

> *Response:*  
> `<jI [cA cB cC ...]>`
>
> - **c:** Raw current value for each defined Track, in milliAmps

#### `<J G> <JG>` - Request max current list

> *Response:*  
> `<jG [mA mB mC ...]>`
>
> - **m:** Raw current trip value for each defined Track, in milliAmps

------------------------------------------------------------------------

### Track Manager

Note: Previously referred to as 'DC-District'.

#### `<= trackletter mode [cab]>` - Configure Track Manager

<div class="important">

<div class="title">

Important

</div>

Whenever the track mode is changed, track power is automatically turned off.

*Parameters:*

- **trackletter:** 'A' through 'H' represent one of the outputs of the/a Motor Shield (also referred to as a 'Motor Controller', 'Motor Driver' or Motor Board').
- **mode:** one of
  - `MAIN`
  - `MAIN_INV`
  - `MAIN_AUTO`
  - `PROG`
  - `DC`
  - `DC_INV` = DC reversed polarity
  - `DCX` = DC reversed polarity (same as DC_INV)
  - `NONE`
- **id:** the cab (loco) ID. *Required when specifying DC or DC_INV / DCX*

<!-- -->

*Response:*  
(for each track/channel that has changed) `<= trackletter state cab>`

- **trackletter:** A-H
- **state:** 'PROG', 'MAIN', 'MAIN_INV', 'MAIN A', 'DC', 'DCX', 'NONE'
- **cab:** cab(loco) equivalent to a fake DCC Address for DC and DCX only

*Notes:*

- Since only one channel can be PROG, changing a second channel to PROG, will force the other to `NONE`
- The response to `DC_INV` is `DCX`
- The response to `DCC_MAIN` is `MAIN A`

</div>

#### `<=>` - Request the current Track Manager configuration

> *Response:*  
> for each track/channel supported by the Motor Shield (also referred to as a 'Motor Controller', 'Motor Driver' or Motor Board') `<= trackletter state cab>`
>
> - **trackletter:** A-H
> - **state:** 'PROG', 'MAIN', 'MAIN_INV', 'MAIN A', 'DC', 'DCX', 'NONE'
> - **cab:** cab(loco) equivalent to a fake DCC Address for DC and DCX only
>
> *Notes:*
>
> - A track set to `DC_INV` (DC inverted) will respond with `DCX`
> - A track set to `MAIN_AUTO` (DCC Auto reverser) will respond with `MAIN A`

#### `<onOff [track]>` - Turn power on or off to the requested TrackManager track

> *Parameters:*  
>
> - **onOff:** one of
> - 1 = on
> - 0 = off
>
> - **track:** one of tracks A - H
>
> *Response:*  
> The following is not a direct response, but rather a broadcast that will be triggered as a result of any power state changes. `<pOnOFF [track]>`

#### Change Frequency on DC or DC_INV/DCX TrackManager track

When running in DC mode certain locomotives can be unresponsive at certain DC frequencies, a situation that is not found when running in DCC mode. When in DC or DC_INV / DCX mode it is now possible to set different frequencies using Functions F29, F30 & F31.

The settings achievable vary slightly depending upon the processor running the Command Station but broadly follow the following:

> - **No Functions:** Default - low frequency 131Hz
> - **F29:** Mid frequency - 490Hz
> - **F30:** High frequency - 3400Hz
> - **F31:** Supersonic - 62500Hz

**Notes:**

- These functions are not cumulative - setting F30 overrides F29 and setting F31 overrides F29 & F30.
- You need to activate the functions above once you have acquired the loco address that have assigned to the output. Specifically:
  1)  Set the output/track to DC mode with a specified loco address
  2)  Acquire that loco address in your throttle app
  3)  Make sure the loco is stopped
  4)  Set the frequency by activating one of the functions above

- You need to stop the loco (throttle to zero) before changing the frequency using the function buttons.

For details on setting F keys see "Turn Loco decoder functions ON or OFF" in [Cab (Loco) Commands](#cab-loco-commands) below.

For ease of changing these functions within EXRAIL an EXRAIL command SET_FREQ is available to select the frequency within automations/routes.

------------------------------------------------------------------------

### Cab (Loco) Commands

#### `<t cab>` - Request a deliberate update on the cab (loco) speed/functions

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco
>
> *Response:*  
> The following is not a direct response, but rather as a broadcast that will be triggered as a result of any throttle command being issued by any device for the cab(loc) in question.
>
> `<l cab reg speedByte functMap>`
>
> - **cab:** DCC Address of the decoder/loco. The short (1-127) or long (128-10293) address of the engine decoder (this has to be already programmed in the decoder)
> - **reg:** not used. We no longer use this but need something here for compatibility with legacy systems. Enter any single digit.
> - **speedbyte:** Speed in DCC speedstep format
>   - reverse - 2-127 = speed 1-126, 0 = stop, 1 = Emergency Stop
>   - forward - 130-255 = speed 1-126, 128 = stop, 129 = Emergency Stop
> - **FunctiMap:** individual function states represented by the bits in a byte
>
> *Notes:*
>
> > The *speedbyte* value is different to the *speed* sent, as it is an encoded (1,7 bits) byte. This starts a reminder process for any external updates to the cab's (loco's) status.

#### `<t cab speed dir>` - Set Cab (Loco) Speed

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco
> - **speed:** 0-127 or -1 for Emergency Stop
> - **dir:** one of
>   - 1=forward
>   - 0=reverse
>
> *Response:*  
> The following is not a direct response, but rather as a broadcast that will be triggered as a result of any throttle command being issued by any device for the cab(loc) in question.
>
> `<l cab reg speedByte functMap>`
>
> - **cab:** DCC Address of the decoder/loco
> - **speedbyte:** Speed in DCC speedstep format
>   - reverse - 2-127 = speed 1-126, 0 = stop, 1 = Emergency Stop
>   - forward - 130-255 = speed 1-126, 128 = stop, 129 = Emergency Stop
> - **FunctiMap:** individual function states represented by the the bits in a byte
>
> *Notes:*
>
> > The *speedbyte* value is different to the *speed* sent, as it is an encoded (1,7 bits) byte. This starts a reminder process for any external updates to the cab's (loco's) status.

#### `<!>` - Emergency Stop

> *Response:*  
> Repeated for each loco in the reminders list `<l cab reg speedByte functMap>` Refer to the `<t ..>` command for details on this response.

#### `<F cab funct state>` - Turn loco decoder functions ON or OFF

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco (short (1-127) or long (128-10293))
> - **funct:** 0-68 (Support for the RCN-212 Functions))
> - **state:**
>   - 1=on
>   - 0=off
>
> *Response:*  
> The following is not a direct response, but rather as a broadcast that will be triggered as a result of any throttle command being issued by any device for the cab(loc) in question.
>
> `<l cab reg speedByte functMap>` refer to the \<t \> command above for details
>
> *Notes:*
>
> > Setting requests are transmitted directly to mobile loco decoder. Current state of loco functions (as known by commands issued since power on) is stored by the CommandStation - All functions within a group get set all at once per NMRA DCC standards. The command station knows about the previous settings in the same group and will not, for example, unset F2 because you change F1. If, however, you have never set F2, then changing F1 WILL unset F2.
>
> **Examples: (click to show)**
>
> > - `<F 3 0 1>` Turns the headlight ON for CAB (loco address) 3
> > - `<F 126 0 0>` Turns the headlight OFF for CAB 126
> > - `<F 1330 1 1>` Turns the horn ON for CAB 1330

#### `<f cab byte1 [byte2]>` - Decoder Functions - Legacy command Deprecated

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco
> - **byte1 byte2:** DCC function bytes as sent to decoders (up to F28)
>
> *Response:*  
> Success: nothing Fail: `<X>`
>
> *Notes:*
>
> > Used by the sniffer
>
> **Additional Information for byte1: (click to show)**
>
> > To make "byte1" add the values of what you want ON together, the ones that you want OFF do not get added to the base value of 128.
> >
> > - F0 (Light)=16, F1 (Bell)=1, F2 (Horn)=2, F3=4, F4=8
> > - All off = 128
> > - Light on 128 + 16 = 144
> > - Light and bell on 128 + 16 + 1 = 145
> > - Light and horn on 128 + 16 + 2 = 146
> > - Just horn 128 + 2 = 130
> >
> > If light is on (144), Then you turn on bell with light (145), Bell back off but light on (144)
>
> **Examples: (click to show)**
>
> > **Breakdown for this example:** `<f 3265 144>`
> >
> > - **f** = (lower case f) This command is for a CAB,s function i.e.: Lights, horn, bell
> > - **3265** = CAB: the short (1-127) or long (128-10293) address of the engine decoder
> > - **144** = Turn on headlight
> >
> > **To set functions F5-F8 on=(1) or off=(0):** `<f cab byte1 [byte2]>`
> >
> > - **f** = (lower case f) This command is for a CAB,s function.
> > - **byte1** = 176 + F5\*1 + F6\*2 + F7\*4 + F8\*8
> >   - ADD 176 + the ones you want ON together
> >   - Add 1 for F5 ON
> >   - Add 2 for F6 ON
> >   - Add 4 for F7 ON
> >   - Add 8 for F8 ON
> >   - 176 Alone Turns OFF F5-F8
> > - **byte2** = omitted
> >
> > **To set functions F9-F12 on=(1) or off=(0):** <span class="title-ref">\<f cab byte1 \[byte2\]\></span>\`
> >
> > - f = (lower case f) This command is for a CAB,s function.
> >
> > - **byte1** = 160 + F9\*1 +F10\*2 + F11\*4 + F12\*8
> >
> >   ADD 160 + the ones you want ON together Add 1 for F9 ON Add 2 for F10 ON Add 4 for F11 ON Add 8 for F12 ON 160 Alone Turns OFF F9-F12
> >
> > **byte2** = omitted
> >
> > **To set functions F13-F20 on=(1) or off=(0):** `<f cab byte1 [byte2]>`
> >
> > - **f** = (lower case f) This command is for a CAB,s function.
> > - **byte1** = 222
> > - **byte2** = F13\*1 + F14\*2 + F15\*4 + F16\*8 + F17\*16 + F18\*32 + F19\*64 + F20\*128
> >   - ADD the ones you want ON together
> >   - Add 1 for F13 ON
> >   - Add 2 for F14 ON
> >   - Add 4 for F15 ON
> >   - Add 8 for F16 ON
> >   - Add 16 for F17 ON
> >   - Add 32 for F18 ON
> >   - Add 64 for F19 ON
> >   - Add 128 for F20 ON
> >   - 0 Alone Turns OFF F13-F20
> >
> > **To set functions F21-F28 on=(1) or off=(0):** `<f cab byte1 [byte2]>`
> >
> > - **f** = (lower case f) This command is for a CAB (loco) function.
> > - **byte1** = 223
> > - **byte2** = F21\*1 + F22\*2 + F23\*4 + F24\*8 + F25\*16 + F26\*32 + F27\*64 + F28\*128
> >   - ADD the ones you want ON together
> >   - Add 1 for F21 ON
> >   - Add 2 for F22 ON
> >   - Add 4 for F23 ON
> >   - Add 8 for F24 ON
> >   - Add 16 for F25 ON
> >   - Add 32 for F26 ON
> >   - Add 64 for F27 ON
> >   - Add 128 for F28 ON
> >   - 0 Alone Turns OFF F21-F28

#### `<t reg cab speed dir>` - Set Cab (Loco) Speed - Legacy command Deprecated

> *Parameters:*  
>
> - **reg:** not used
> - **cab:** DCC Address of the decoder/loco
> - **speed:** 0-127
> - **dir:** one of
>   - 1=forward
>   - 0=reverse
>
> *Response:* The following is not a direct response, but rather as a broadcast that will be triggered as a result of any throttle command being issued by any device for the cab(loc) in question. `<l cab reg speedByte functMap>` refer to the \<t \> command above for details
>
> Legacy response: Deprecated  
> `<T reg speed dir>` - do not rely on this response
>
> *Version Deprecated: 4.1.1*
>
> *Notes:*
>
> > The *speedbyte* value is different to the *speed* sent, as it is an encoded (1,7 bits) byte. This starts a reminder process for any external updates to the cab's (loco's) status.

#### `<- [cab]>` - Remove one or all locos from reminders

> *Parameters:*  
>
> - **cab:** one of
> - blank = all locos
> - No. = Cab (loco) to forget
>
> *Response:* N/A
>
> *Notes:*
>
> > Forgets one or all locos. The "cab" parameter is optional.
> >
> > Once you send a throttle command to any loco, throttle commands to that loco will continue to be sent to the track. If you remove the loco, or for testing purposes need to clear the loco from repeating messages to the track, you can use this command. Sending **\<- cab\>** will forget/clear that loco. Sending **\<-\>** will clear all the locos. This doesn't do anything destructive or erase any loco settings, it just clears the speed reminders from being sent to the track. As soon as a controller sends another throttle command, it will go back to repeating those commands.
>
> *Examples:*
>
> > `<- 74>` - Forgets loco at address 74 `<->` - Forgets all locos

#### `<D speedsteps>` - Switch between 28 and 128 speed steps

> *Parameters:*  
>
> - **speedsteps:**
> - SPEED28 = use 28 speed steps
> - SPEED128 = use 128 speed steps
>
> *Response:*  
> Response sent to the Serial Monitor only (not wifi clients). One of:
>
>   - *28 Speedsteps*
>   - *128 Speedsteps*

#### `<m [type] | [cab acceleration [deceleration]]>` - set the momentum of a loco

> *Parameters:*  
> either  
>
> - **cab:** DCC Address
> - **acceleration:**
> - **decelertaion:**
>
> or  
>
> - **type:**
> One of:  
>
> - <span class="title-ref">LINEAR</span>
> - <span class="title-ref">POWER</span>
>
> *Response:*  
> none
>
> The momentum calculation is based on the difference in throttle setting and actual speed. For example, the time taken to reach speed 50 from a standing start would be less if the throttle were set to speed 100, thus increasing the acceleration.
>
> *Notes:*
>
> > Setting Momentum 7,14,21 etc is similar in effect to setting a decoder CV03/CV04 to 1,2,3.
>
> *Examples:*
>
> > <span class="title-ref">\<m 3 0\></span> sets loco 3 to no momentum. <span class="title-ref">\<m 3 21\></span> sets loco 3 to 21 mS/step. <span class="title-ref">\<m 3 21 42\></span> sets loco 3 to 21 mS/step accelerating and 42 mS/step when decelerating.
> >
> > <span class="title-ref">\<m LINEAR\></span> - acceleration is uniform up to selected throttle speed. <span class="title-ref">\<m POWER\></span> - acceleration depends on difference between loco speed and selected throttle speed.

------------------------------------------------------------------------

### Roster Commands

#### `<J R>` `<JR>` - Request the list defined Roster Entry IDs

> *Parameters:* N/A
>
> *Response:*  
> `<jR [id1 id2 id3 ...]>`
>
> - **id?:** unique id of the Cab/s (Loco/s) in the roster
>
> *Example Responses:*  
> Response (roster exists): `<jR id1 id2 id3 ...>` Response (no roster exists): `<jR>`

#### `<J R id>` `<JR id>` - Request details of a specific Roster Entry

> *Parameters:*  
>
> - **id:** unique id of the Cab/s (Loco/s) in the roster
>
> *Response:*  
> `<jR id ""|"desc" ""|"funct1/funct2/funct3/...">`  
>
> - **id:** unique id of the Cab/s (Loco/s) in the roster
> - **desc:** description of the Loco
> - **funct?:** Label for each function 0-28
>
> *Example Responses:*  
> Response (id is in Roster): `<jR id "desc" "funct1/funct2/funct3/...">` Response (id is not in Roster): `<jR id "" "">`

------------------------------------------------------------------------

### Turnouts/Points

For details on how to configure turnouts/points see: Turnouts/points (configuring the ex-commandstation)

#### `<T>` - Request a list all defined turnouts/Points

> *Response:*  
> Repeated for each defined Turnout/Point  
> Response: `<H id state>`
>
> Response (fail): N/A Response (no defined turnouts/points): `X`
>
> - **id** - The numeric ID (0-32767) of the turnout to control.
> - **state:** one of
>   - 1 = Thrown,
>   - 0 = Closed

#### `<T id state>` - Throw or Close a defined turnout/point

> *Parameters:*  
>
> - **id:** identifier of the Turnout/Point
> - **state:** one of
>   - 1 = Throw,
>   - T = Throw,
>   - 0 = Close,
>   - C = Close,
>   - X = eXamine
>
> *Response:*  
> `<H id state>`
>
> - **id:** one of
>   - identifier of the Turnout/Point, or
>   - X if the command fails
> - **state:** one of
>   - 1 = Thrown,
>   - 0 = Closed
>   - blank = command failed
>
> *Example Responses:* Response on throw/close: Response (successful): `<H id state>` Response (fail): `<X>` Response on eXamine: Response (DCC Accessories): `<H id DCC address subaddress state>` Response (Servos): `<H id SERVO vpin thrown_position closed_position profile state>` Response (VPIN): `<H id VPIN vpin state>` Response (LCN): `<H id LCN state>` Response (fail/no such turnout): `<X>`
>
> **Response - Additional Details: (click to show)**
>
> > - `id` : The numeric ID (0-32767) of the turnout to control. (NOTE: IDs are shared between Turnouts/Points, Sensors and Outputs)
> > - `address` : the primary address of a DCC accessory decoder controlling a turnout/point (0-511)
> > - `subaddress` : the subaddress of a DCC accessory decoder controlling a turnout/point (0-3)
> > - `vpin` : the pin number of the output to be controlled by the turnout/point object. For Arduino output pins, this is the same as the digital pin number. For servo outputs and I/O expanders, it is the pin number defined for the HAL device (if present), for example 100-115 for servos attached to the first PCA9685 Servo Controller module, 116-131 for the second PCA9685 module, 164-179 for pins on the first MCP23017 GPIO expander module, and 180-195 for the second MCP23017 module.
> > - `state` : 0 = closed. 1 = thrown.
> > - `thrown_position` : the PWM value corresponding to the servo position for THROWN state, normally in the range 102 to 490.
> > - `closed_position` : the PWM value corresponding to the servo position for CLOSED state, normally in the range 102 to 490.
> > - `profile` : the profile for the transition between states. 0=Immediate, 1=Fast (0.5 sec), 2=Medium (1 sec), 3=Slow (2 sec), 3=Bounce (for semaphore signals).

#### `<J T id>` `<JT id>` - Request details of a specific Turnout/Point

> *Parameters:*  
>
> - **id:** unique id of the Turnout/Point
>
> *Response:*  
> `<jT id X|state |"[desc]">`
>
> - **id:** unique id of the Turnout/Point
> - **state:** one of
>   - C = Closed
>   - T = Thrown
>   - X = unknown id
> - **desc:** one of
>   - "desc" = description of the Turnout(Point) (including surrounding quotes)
>   - blank = unknown id
>
> *Example Responses:* Response (id is defined): `<jT id state "[desc]">` Response (id not defined): `<jT id X>`

#### `<J T>` `<JT>` - Request the list of defined turnout/Point IDs

> *Response:*  
> `<jT [id1 id2 id3 ...]>`
>
> - **id:** unique id of the Turnout/s(Point/s)
>
> *Example Responses:* Response (has defined Turnouts/Points): `<jT id1 id2 id3 ...>` Response (no defined Turnouts/Points): `<jT>`

------------------------------------------------------------------------

### Turntables/Traversers

For details on how to configure turntables/traversers see: Turntables/traversers (configuring the ex-commandstation)

#### `<I>` - Request a list all defined turntables/traversers

> *Response:*  
> Repeated for each defined Turtable/traverser  
> Response: `<I id position>`
>
> Response (fail): N/A Response (no defined turntables/traversers): `X`
>
> - **id** - The numeric ID (1-32767) of the turntable to control
> - **position** - The current position of the turntable

#### `<I id>` - Request position of the specified turntable/traverser

> *Response:*  
> Response: `<I id position>` Response (fail): N/A Response (no defined turntables/traversers): `X`
>
> - **id** - The numeric ID (1-32767) of the turntable to control
> - **position** - The current position of the turntable

#### `<I id position>` - Rotate a DCC turntable

> *Parameters:*  
>
> - **id:** - Identifier of the Turntable/traverser
> - **position:** - Position to rotate to
>
> *Response:*  
> `<I id position moving>`
>
> - **id:** one of
>   - identifier of the Turntable/traverser, or
>   - X if the command fails
> - **position:** one of
>   - position rotating to, or
>   - blank = command failed
> - **moving:** one of
>   - 0 (no feedback can be returned from a DCC turntable), or
>   - blank = command failed
>
> *Example Responses:* Response on rotate: Response (successful): `<I id position moving>` Response (fail): `<X>`
>
> *Further information:*  
> When a DCC accessory turntable is rotated or moved, no feedback is sent to EX‑CommandStation, and therefore the **moving** variable will always be '0', and a second response will therefore never be sent to indicate the completion of a rotation or move, unlike how EX‑Turntable operates.

#### `<I id position activity>` - Rotate EX-Turntable

> *Parameters:*  
>
> - **id:** - Identifier of the Turntable/traverser
> - **position:** - Position to rotate to
> - **activity:** - The activity for EX-Turntable to perform (refer Ex-turntable activity reference)
>
> *Response:*  
> `<I id position moving>`
>
> - **id:** one of
>   - identifier of the Turntable/traverser, or
>   - X if the command fails, or a rotation/move is in progress
> - **position:** one of
>   - position rotating to, or
>   - blank = command failed
> - **moving:** one of
>   - 1 - turntable is moving, or
>   - 0 - turntable is not moving, or
>   - blank = command failed
>
> *Example Responses:* Response on rotate: Response (successful): `<I id position moving>` Response (fail): `<X>`
>
> *Further information:*  
> When EX-Turntable commences rotating/moving, the device driver flags this using the **moving** variable above in the response (1 indicates moving, 0 indicates stationary), and when a rotation or move is complete, it will generate an additional response broadcast to indicate that the rotation or move has completed. Further to this, a new rotate/move command will error when a rotation or move is currently in progress.

#### `<J O>` `<JO>` - Request the list of defined turntables/traversers

> *Response:*  
> `<jO [id1 id2 id3 ...]>`
>
> - **id:** unique id of the turntable(s)/traverser(s)
>
> *Example Responses:* Response (has defined Turnouts/Points): `<jO id1 id2 id3 ...>` Response (no defined Turnouts/Points): `<jO>`

#### `<J O id>` `<JO id>` - Request details of the specific turntable/traverser

> *Parameters:*  
>
> - **id:** unique id of the turntable/traverser
>
> *Response:*  
> `<jO id type position position_count "[desc]">`
>
> - **id:** unique id of the turntable/traverser
> - **type:** one of
>   - 0 = DCC
>   - 1 = EX-Turntable
>   - X = unknown id or hidden
> - **position:** one of
>   - index of the current position (0 - 48)
>   - blank = unknown or hidden id
> - **position_count:** one of
>   - 0 = number of defined positions, including home (0)
>   - blank = unknown or hidden id
> - **desc:** one of
>   - "desc" = description of the turntable or traverser (including surrounding quotes)
>   - blank = unknown or hidden id
>
> *Example Responses:* Response (id is defined): `<jO id type position position_count "[desc]">` Response (id not defined): `<jO id X>`
>
> *Further information:*  
> The turntable or traverser information does not include the list of defined positions, and this must be requested separated as outlined in the following section.

#### `<J P id> <JP id>` - Request all position details of the specified turntable/traverser

> *Parameters:*  
>
> - **id:** unique id of the Turnout/Point
>
> *Response:*  
> `<jP id index angle "[desc]">`
>
> - **id:** unique id of the turntable/traverser
> - **index:** one of
>   - the position index (0 - 48)
>   - X = unknown or hidden id
> - **angle:** one of
>   - the angle from home for the position (0 - 3600 to allow for partial angles)
>   - blank = unknown or hidden id
> - **desc:** one of
>   - "desc" = description of the position (including surrounding quotes)
>   - blank = unknown or hidden id
>
> *Example Responses:* Response (id is defined): `<jO id index angle "[desc]">` Response (id not defined): `<jO id X>`

#### `<D TT vpin steps [activity]>` - Test turntable

> *Parameters:*  
>
> - **vpin:**
> - **steps:** ???
> - **activity** optional - ???
>
> *Response:*  
> TBA

------------------------------------------------------------------------

### Routes/Automations

For details on how to configure routes/automations see: Exrail command reference

Also see the <span class="title-ref">EXRAIL</span> section below for activating routes.

#### `<J A>` - Request a list of Automations/Routes

> *Response:*  
> `<jA [id0 id1 id2 ..]>`
>
> - **id?:** identifier of the Route/Automation(s)
>
> *Example Responses:* Response (successful - turnouts/points exist): `<jA id0 id1 id2 ..>` Response (successful - turnouts/points don't exist): `<jA>` Response (fail): ???

#### `<J A id> <JA id>` - Request information for a route/automation

> *Parameters:*  
>
> - **id:** identifier of the Route/Automation
>
> *Response:*  
> `<jA id X|type |"desc">`
>
> - **id:** identifier of the Route/Automation
> - **type:** one of
>   - 'R'= Route
>   - 'A'=Automation
> - **"desc":** Textual description of the route/automation always surrounded in quotes (")
>
> *Example Responses:* Response (successful): `<jA id type "desc">` Response (fail - is not defined): `<jA id X>`

#### `</ START [cab] id>` - Start an EXRAIL Sequence

> Start an EXRAIL sequence (route or automation).
>
> *Parameters:*  
>
> - **cab** Optional. DCC address of the cab (loco) to 'send' on the automation
> - **id:** Id of the Sequence
>
> *Response:*  
> none

#### `</ KILL id>` - Kill an EXRAIL Sequence

> Stop the execution of one or all EXRAIL sequences (route or automation).
>
> *Parameters:*  
>
> - **id:** Either:
> The id of the Sequence, or `ALL` = Kill all sequences
>
> *Response:*  
> none

------------------------------------------------------------------------

### System Information

#### `<c>`- Request Current on the Track(s)

> *Response:*  
> `<c "CurrentMAIN" current C "Milli" "0" max_ma "1" trip_ma>`
>
> - **"CurrentMAIN":** Static text for software like JMRI
> - **current**: Current in MilliAmps
> - **C**: Designator to signify this is a current meter (V would be for voltage)
> - **"Milli"**: Unit of measure for external software with a meter like JMRI (Milli, Kilo, etc.)
> - **"0":** numbered parameter for external software (1,2,3, etc.)
> - **max_ma**: The maximum current handling of the Motor Driver (also referred to as a 'Motor Controller', 'Motor Shield' or 'Motor Board') in MilliAmps
> - **"1"**: number parameter for external software (we use 2 parameters here, 0 and 1)
> - **trip_ma** - The overcurrent limit that will trip the software circuit breaker in mA

#### `<s>` - Request the DCC-EX version and hardware info, along with listing defined turnouts

> *Response:*  
> `<iDCCEX version / microprocessorType / MotorControllerType / buildNumber>` (repeated for each defined Turnout/Point): **\<H id state\>**
>
> - **version:** Command Station version
> - **microprocessorType:** microprocessor type (e.g. MEGA)
> - **MotorControllerType:** Motor Driver (also referred to as a 'Motor Controller', 'Motor Shield' or 'Motor Board') type (e.g. STANDARD_MOTOR_SHIELD)
> - **buildNumber:** Command Station build number
> - **id:** unique identifier for the Turnout/Point
> - **state:** one of
>   - 1=thrown
>   - 0=Closed

#### `<#>` - Request the number of supported cabs(locos)

> *Response:*  
> `<# noCabs>`
>
> - **noCabs:** maximum number of Cabs(Locos) supported by the command station
>
> *Notes:*
>
> > This will display the number of available cab (loco) slots. This will typically be **\<# 20\>**, **\<# 30\>**, or **\<# 50\>** depending on how much memory your EX‑CommandStation has available.
> >
> > This is a design limit based on the memory limitations of the particular hardware and a compromise with other features that require memory such as WiFI. If you need more slots and are comfortable with code changes you can adjust this by changing MAX_LOCOS in "DCC.h", knowing that each new slot will take approximately 8 bytes of memory. The **\<D RAM\>** command will display the amount of free memory. If you fill the available slots, the "Forget Locos" command (**\<- \[CAB\]\>**) will free up unused locos. Currently there is no automatic purging of unused locos.

------------------------------------------------------------------------

### DCC Accessories

EX‑CommandStation can keep track of the direction of any turnout that is controlled by a DCC stationary accessory decoder once its Defined (Set Up).

All decoders that are not in an engine are accessory decoders including turnouts.

Any DCC Accessory Decoder based turnouts, as well as any other DCC accessories connected in this fashion, can always be operated using the DCC COMMAND STATION Accessory command:

There are two interchangeable commands for controlling Accessory Decoders, the Address/Subaddress method (aka “Dual-Coil” method) and linear addressing method. You can either specify an address and its subaddress (Addresses 0-511 with Subaddresses from 0-3) or the straight linear address (Addresses from 1-2044).

In the mapping used by EX-CS\|, linear addresses range from linear address 1, which is address 1 subaddress 0, up to linear address 2040 which is address 510 subaddress 3. Decoder address 511 (linear addresses 2041-2044) is reserved for use as a broadcast address and should not be used for decoders. Decoder address 0 does not have a corresponding linear address. This seems strange, but it is the mapping used by many, but not all, commercial manufacturers. If your decoder does not respond on the expected linear address, try adding and subtracting 4 to see if it works. Or use the address/subaddress versions of the commands.

Here is a spreadsheet in .XLSX format to help you: Stationary decoder address table (xlsx spreadsheet).

NOTE: Both the following commands do the same thing. Pick the one that works for your needs.

#### `<a addr subaddr activate>` - Control an Accessory Decoder with Address and Subaddress

> *Parameters:*  
>
> - **addr:** the primary address of the decoder controlling the turnout (0-511)
> - **subaddr:** the subaddress of the decoder controlling this turnout (0-3)
> - **activate:** one of
>   - 0=off, deactivate, straight or Closed
>   - 1=on, activate, turn or thrown
>
> *Response:* ???

#### `<a linear_addr activate>` - Control an Accessory Decoder with linear address

> *Parameters:*  
>
> - **linear_addr:** linear address of the decoder controlling this turnout (1-2044)
> - **activate:** one of
>   - 0=off, deactivate, straight or Closed
>   - 1=on, activate, turn or thrown
>
> *Response:* ???

#### `<A address aspect>` - Command for DCC Extended Accessories.

This command sends an extended accessory packet to the track, normally used to set a signal aspect. Aspect numbers are undefined as sdtandards except for 0 which is always considered a stop.

> *Note*
>
> > These general commands simply send the appropriate DCC instruction packet to the main tracks to operate connected accessories. It does not store or retain any information regarding the current status of that accessory.

------------------------------------------------------------------------

### Sensors

#### `<Q>` - Lists Status of all sensors

> *Response:*  
> Repeated for each defined sensor: `<q id>` or `<Q id>`
>
> e.g. Response (successful) Repeated for each inactive defined sensor: `<q id>` Response (successful) Repeated for each active defined sensor: `<Q id>` Response (fail): N/A

#### `<S>` - Request a list of all defined sensors

> *Response:*  
> Repeated for each defined sensor: `<Q id vpin pullup>`
>
> - **id:** identifier of the Sensor. (0-32767)
> - **vpin:** pin number of the input to be controlled by the sensor object
> - **pullup:** one of
>   - 1=Use pull-up resistor ACTIVE=LOW
>   - 0=don't use pull-up resistor ACTIVE=HIGH
>
> e.g. Response (successful) Repeated for each defined sensor: `<Q id vpin pullup>` Response (fail): `<X>`

------------------------------------------------------------------------

### Signals

#### `</ RED signalId>` \</ AMBER signalId\> \</ GREEN signalId\> - Control a signal

> *Parameters:*  
>
> - **signalId:** defined red Vpin of the signal to control
>
> *Response:* N/A

------------------------------------------------------------------------

### WiFi Control

#### `<+X>` - Force the Command Station into "WiFi Connected" mode

> A special command to force the "connected" flag (WiFi Connected Mode) to on inside the Command Station so that our loop will start seeing network traffic. If your code creates a connection outside of our normal WiFi code, this provides a way for you to notify the Command Station that it needs to process commands on a connection you created and so you can send your own AT commands.
>
> *Response:* ???
>
> *Examples:*
>
> > \<+GMR\> - Sends the "AT+GMR" command that prints version information from the WiFi device. \<+CIFSR\> - Gets the local IP Address.
>
> *Notes:*
>
> > DCC-EX WiFi Configuration
> >
> > [Espressif AT Command Set PDF File (Exressif makes the ESP8266)](https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf)

#### `<+command>` - Sends AT+ commands to the WiFi board (ESP8266, ESP32, etc.)

> *Parameters:*  
>
> - **command:** what you want to append after AT+ and send to the AT processor.
>
> *Response:* ???
>
> *Example:* `<+X>` would send AT+X to the ESP
>
> *Notes:*
>
> > Users familiar with the AT Command Set of WiFi board may enter commands directly into the Serial Monitor in real-time or as setup commands in the mySetup.h file. This allows users to override the default WiFi connect sequence or to send any command to change a WiFi device setting.

#### `<+>` - Switch to direct communication with WiFi AT processor

> *Response:*  
> All input and output from this point is the direct communication with the WiFi AT software this mode is ended by typing ! (exclamation mark).

#### `<C WIFI "ssid" "password">` - Connects to an existing WIFI network in STA mode

> *Parameters:*  
>
> - **ssid:** network to connect to
> - **password:** password to use
>
> *Response:* ???
>
> *Example:* ???
>
> *Notes:*
>
> > Valid only for ESP32 microcontrollers only (including the EX‑CSB1)

------------------------------------------------------------------------

### EXRAIL

Refer to the Exrail command reference for these.

### EX-FastClock

These commands require the optional EX‑FastClock hardware to the installed along with the EX‑CommandStation to function.

#### `<JC minutes speed>` - Start the fast clock with a specified time

> *Parameters:*  
> **minutes:** = time in minutes since midnight. i.e. (hours \* 60) + mins **speed:** = the perceived speed factor
>
> *Response:* `<jC minutes>`  
> where **minutes:** = time in minutes since midnight. i.e. (hours \* 60) + mins
>
> *Example:*
>
> > `<JC 375 4>` Will set the fast clock time as 6:15am with the percieved speed factor of 1 minute every 15 seconds (4 times actual).

#### `<JC>` - Request the fast clock current time

> *Response:* `<jC minutes>`  
> where **minutes:** = time in minutes since midnight. i.e. (hours \* 60) + mins

------------------------------------------------------------------------

## Writing Configuration Variable (CVs)

### Writing CVs - Program on the main

#### `<b cab cv bit value>` - Write Configuration Variable (CV) bit on main track

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco. The short (1-127) or long (128-10293) address of the engine decoder
> - **cv:** The number of the Configuration Variable memory location in the decoder to write to (1-1024)
> - **bit:** ???
> - **value:** The value to be written to the Configuration Variable memory location (0-255)
>
> *Response:* N/A

#### `<w cab cv value>` - Write Configuration Variable (CV) on main track

> *Parameters:*  
>
> - **cab:** DCC Address of the decoder/loco. The short (1-127) or long (128-10293) address of the engine decoder
> - **cv:** The number of the Configuration Variable memory location in the decoder to write to (1-1024)
> - **value:** The value to be written to the Configuration Variable memory location (0-255)
>
> *Response:* N/A

------------------------------------------------------------------------

### Reading/Writing Configuration Variables (CVs) - Programming track

**Note**

By design, for safety reasons, the NMRA specification prevents locos from responding to throttle or function commands while on the service track. A loco WILL NOT MOVE on the service track! Don't let the little 'jumps' you may see when you are programming a CV confuse you. The loco pulses the motor to give a jump in current that we read as an 'ACK' (acknowledgment), that causes some locos to stutter ahead slightly every time you read or write a CV.

#### `<R cv>` - Read Configuration Variables (CVs)

> *Parameters:*  
>
> - **cv:** CV number
>
> *Response:*  
> `<v cv value>`
>
> - **cv:** The number of the Configuration Variable memory location in the decoder (1-1024)
> - **value:** one of
>   - value of the CV
>   - -1: if the write failed
>
> *Example:* `<v 1 3>` shows that the value `3` is stored in CV `1`. *Example:* `<v 1 -1>` shows that reading the value stored in CV `1` failed.

#### `<R>` - Read DCC decoder (cab) address

> *Response:*  
> `<r address>`
>
> - **address:**
>   - DCC Address of the decoder/loco. The short (1-127) or long (128-10293) address of the engine decoder
>   - -1 = failed read
>
> *Example Responses:* Response (successful): **\<r 3\>** Response (fail): **\<r -1\>**
>
> *Notes:*
>
> > **IMPORTANT:** If the loco is in a consist (CV19), the address returned will be the consist address.
> >
> > When combined with the `<D ACK ON>` Command, the `<R>` Command (with or without parameters) can be used for diagnostics, for example when you get a "-1" response. (See [Diagnosing Issues](https://github.com/DCC-EX/CommandStation-EX/wiki/Diagnosing-Issues)\*\* for more help)

#### `<R LOCOID>` - Read DCC decoder (cab) address

> *Response:*  
> `<r LOCOID address>`
>
> - **address:**
>   - DCC Address of the decoder/loco. The short (1-127) or long (128-10293) address of the engine decoder
>   - -1 = failed read
>
> *Example Responses:* Response (successful): **\<r LOCOID 3\>** Response (fail): **\<r LOCOID -1\>**
>
> *Notes:*
>
> > **IMPORTANT:** Unlike <span class="title-ref">\<R\></span> If the loco is in a consist, the address returned will be the actual address.

#### `<R CONSIST>` - Read DCC decoder consist (CV19) address

> *Response:*  
> `<r CONSIST address>`
>
> - **address:**
>   - DCC Consost (CV19)Address of the decoder/loco.
>   - -1 = failed read
>
> *Example Responses:* Response (successful): **\<r CONSIST 3\>** Response (fail): **\<r CONSIST -1\>**

#### `<V cv bit onOff>` - Verify/Read bit of Configuration Variable (CV) with guessed value

> *Parameters:*  
>
> - **cv:** CV number
> - **bit:** bit to verify in the CV
> - **onOff:** one of
>   - 1=on
>   - 0=off
>
> *Response:*  
> `<v cv bit onOff>`
>
> - **cv:** CV number
> - **bit:** bit to verify in the CV
> - **onOff:** one of
>   - 1=on
>   - 0=off
>   - -1=error
>
> *Example:* `<v 1 3 1>` shows that the value `1` is stored in bit `3` of CV `1`. *Example:* `<v 1 3 -1>` shows verifying the value stored in bit `3` of CV `1` failed.
>
> *Notes:*
>
> > This command is designed to offer faster verification of the value held in a CV and can be used instead of the `<R>` commands. Instead of reading a bit value, it compares the bit to an expected value. It will attempt to verify the value first, an if it is successful, will return the value as if it was simply “read”. If the verify fails, it will perform a read bit command (see above) and return the value read.

#### `<V cv value>` - Verify/Read of Configuration Variable (CV) with guessed value

> *Parameters:*  
>
> - **cv:** CV number
> - **value:** value to verify
>
> *Response:*  
> `<v cv value>`
>
> - **cv:** CV number
> - **value:** one of
>   - actual value of the CV
>   - -1: if the verify failed
>
> *Example:* `<v 1 3>` shows that the value `3` is stored in CV `1`. *Example:* `<v 1 -1>` shows verifying the value stored in CV `1` failed.
>
> *Notes:*
>
> > This command is designed to offer faster verification of the value held in a CV and can be used instead of the `<R>` commands. Instead of reading a byte value or looking at each bit, it compares the byte to an expected value. It will attempt to verify the value first, and if it is successful, will return the value as if it was simply “read”. If the verify fails, it will perform a read byte command (see above) and return the value read.

#### `<B cv bit onOff>` - Write bit to Configuration Variable (CV)

> *Parameters:*  
>
> - **cv:** CV number
> - **bit:** bit to change in the CV
> - **onOff:** one of
>   - 1=on
>   - 0=off
>
> *Response:*  
> `<r0|0|cv bit onOff>`
>
> - **cv:** CV number
> - **bit:** bit changed
> - **onOff:** one of
>   - 0BR\|
>   - -1: if the write failed
>
> *Example:* `<r0|0|1 3 1>` shows that the value `1` was written to bit `3` of CV `1`. *Example:* `<r0|0|1 3 -1>` shows that writing to bit `3` of CV `1` failed.
>
> *Notes:*
>
> > The response is a legacy DCC++ formatted response that is hard to parse, and it is recommended to write full CVs where possible.

#### `<W cv value>` - Write Configuration Variable (CV)

> *Parameters:*  
>
> - **cv:** CV number
> - **value:** value to change the CV to
>
> *Response:*  
> `<r cv value>`
>
> - **cv:** CV number
> - **value:** one of
>   - value CV was changed to
>   - -1: if the write failed
>
> *Example:* `<r 1 3>` shows that the value `3` was written to CV `1`. *Example:* `<r 1 -1>` shows writing a value to CV `1` failed.

#### `<W address>` - Write DCC address to cab (loco)

> *Parameters:*  
>
> - **address:** DCC Address of the decoder/loco
>
> *Response:*  
> `<w address>`
>
> - **address:** one of
>   - DCC Address of the decoder/loco
>   - -1 = failed read
>
> Response (successful): **\<w cab\>** Response (fail): **\<w -1\>**
>
> *Notes:*
>
> > Writes, and then verifies, the address to decoder of an engine on the programming track. This involves clearing any consist and automatically setting a long or short address. This is an easy way to put a loco in a known state to test for issues like not responding to throttle commands when it is on the main track.

#### `<P register hex1 hex2 [hex3 [hex4 [hex5]]]>` - Writes a DCC packet to the PROG track

> Writes a DCC packet of two, three, four, or five hexadecimal bytes to a register driving the selected track.
>
> *Parameters:*  
>
> - **register:** ignored
> - **byte1:** first hexadecimal byte in the packet
> - **byte2:** second hexadecimal byte in the packet
> - **byte3:** optional third hexadecimal byte in the packet
> - **byte4:** optional fourth hexadecimal byte in the packet
> - **byte5:** optional fifth hexadecimal byte in the packet
>
> *Response:*  
> N/A
>
> *Notes:*
>
> > register for backwards compat (can not be removed because number of arguments is unknown)

#### `<B cv bit value callbacknum callbacksub>` - Deprecated, please use \<W cv value\> instead

> *Parameters:*  
>
> - **cv:** The number of the Configuration Variable memory location in the decoder to write to (1-1024 ).
> - **bit:** The bit number of the Configuration Variable memory location to write (0-7)
> - **value:** The value to be written to the Configuration Variable memory location (0-255)
> - **callbacknum:** An arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs that call this function.
> - **callbacksub:** a second arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs (e.g. DCC-EX Interface) that call this function.
>
> *Response:* `<r callbacknum|callbacksub|cv value>`

#### `<W cv value callbacknum callbacksub>` - Deprecated, please use \<w cv value\> instead

> *Parameters:*  
>
> - **cv:** The number of the Configuration Variable memory location in the decoder to write to (1-1024 ).
> - **value:** The value to be written to the Configuration Variable memory location (0-255)
> - **callbacknum:** An arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs that call this function.
> - **callbacksub:** a second arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs (e.g. DCC-EX Interface) that call this function.
>
> *Response:* `<r callbacknum|callbacksub|cv value>`

#### `<R cv callbacknum callbacksub>` - Read Configuration variable byte

> *Parameters:*  
>
> - **cv:** The number of the Configuration Variable memory location in the decoder to write to (1-1024 ).
> - **callbacknum:** An arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs that call this function.
> - **callbacksub:** a second arbitrary integer (0-32767) that is ignored by the Command Station and is simply echoed back in the output - useful for external programs (e.g. DCC-EX Interface) that call this function.
>
> *Response:* `<r callbacknum|callbacksub|cv value>`
>
> *Notes:*
>
> > If specified with parameters, reads a Configuration Variable from the decoder of an engine on the programming track. If no parameters are specified, it returns the Address of the loco on the programming track.

------------------------------------------------------------------------

### Write direct DCC packet

<div class="warning">

<div class="title">

Warning

</div>

THESE ARE FOR DEBUGGING AND TESTING PURPOSES ONLY. DO NOT USE UNLESS YOU KNOW HOW TO CONSTRUCT NMRA DCC PACKETS - YOU CAN INADVERTENTLY RE-PROGRAM YOUR ENGINE DECODER

</div>

#### `<M register hex1 hex2 [hex3 [hex4 [hex5]]]>` - Write a DCC packet the MAIN track

> Writes a DCC packet of two, three, four, or five hexadecimal bytes to a register driving the selected track.
>
> *Parameters:*  
>
> - **register:** ignored
> - **byte1:** first hexadecimal byte in the packet
> - **byte2:** second hexadecimal byte in the packet
> - **byte3:** optional third hexadecimal byte in the packet
> - **byte4:** optional fourth hexadecimal byte in the packet
> - **byte5:** optional fifth hexadecimal byte in the packet
>
> *Response:*  
> N/A
>
> *Notes:*
>
> > register for backwards compat (can not be removed because number of arguments is unknown)

------------------------------------------------------------------------

### Programming track - Tuning

#### `<D ACK LIMIT mA>` - Sets the ACK limit

> Use this command to override the minimum milliamps (mA) required to detect the ACK pulse, e.g. `<D ACK LIMIT 30>` means a minimum 30mA pulse would be accepted.
>
> *Parameters:*  
>
> - **mA:** currently limit in milliamps
>
> *Response:* N/A
>
> *Notes:*
>
> > The Ack current limit is set according to the DCC standard(s) of 60mA. Most decoders send a quick back and forth current pulse to the motor to generate this ACK. However, some modern motors (N and Z scales) may not be able to draw that amount of current. You can adjust down this limit. Or, if for some reasons your acks seem to be too "trigger happy" you can make it less sensitive by raising this limit.

#### `<D ACK MIN µS>` - Sets the ACK pulse minimum

> As above, however overriding the maximum amount of time for a pulse, e.g. `<D ACK MAX 20000>` means a pulse up to 20ms would be accepted.
>
> *Parameters:*  
>
> - **µS:** ACK pulsedureation in milliseconds lower bound
>
> *Response:* N/A
>
> *Notes:*
>
> > The NMRA specifies that the ACK pulse duration should be 6 milliseconds, which is 6000 microseconds (µS), give or take 1000 µS. That means the minimum pulse duration is 5000 µS and the maximum is 7000 µS. There are many poorly designed decoders in existence so DCC-EX extends this range from 4000 to 8500 µS. If you have any decoders that still do not function within this range, you can adjust the ACK MIN and ACK MAX parameters.

#### `<D ACK MAX µS>` - Sets the ACK pulse maximum

> Use this command to override the minimum amount of time in microseconds (uS) the pulse needs to be active for, e.g. `<D ACK MIN 2000>` means a pulse of 2ms or more would be accepted.
>
> *Parameters:*  
>
> - **µS:** ACK pulse duration in milliseconds upper bound
>
> *Response:*  
> N/A *Notes:* see MIN

#### `<D ACK RETRY num>` - Adjust ACK retries

> When reading/writing CVs, the program will try again upon failure. The default is `<D ACK RETRY 2>`, which means 3 attempts before a failure is reported. Each of the unsuccessful attempts is reported in the Serial Monitor or JMRI monitor log. The last unsuccessful attempt remains on the display if in use. To reset the running total, send the command manually: `<D ACK RETRY 2>`.
>
> *Parameters:*  
>
> - **num:** Number of times to retry
>
> *Response:* N/A
>
> *Notes:*
>
> > When combined with the `<D ACK ON>` Command, the `<R>` Command (with or without parameters) can be used for diagnostics, for example when you get a "-1" response. (See [Diagnosing Issues](https://github.com/DCC-EX/CommandStation-EX/wiki/Diagnosing-Issues)\*\* for more help)

#### `<D PROGBOOST>` - Override prog track limit while idle

> By default, the programming track has a current limit enabled of 250mA, so any programming activities requiring more than this value will cause power to the programming track to be cut for 100ms. Run this command to override this if programming decoders trigger current limiting on the programming track.
>
> *Response:* N/A
>
> *Notes:*
>
> > When the programming track is switched on with **\<1\>** or **\<1 PROG\>** it will normally be restricted to 250mA according to NMRA standards. Some loco decoders require more than this, especially sound versions. **\<D PROGBOOST\>** temporarily removes this limit to allow the decoder to use more power. The normal limit will be re-imposed when the programming track is switched off with **\<0\>** or **\<0 PROG\>** or the Command Station is reset.

------------------------------------------------------------------------

## Configuring the EX-CommandStation

### Turnouts/Points (Configuring the EX-CommandStation)

The Turnout/Point commands provide a more flexible and more functional way of operating turnouts/points. It requires that the turnout/point be pre-defined through the `<T ...>` commands, described below.

Turnouts may be in either of two states: Closed or Thrown. The turnout/point commands below use the values `1` for `Throw` or `Thrown` and `0` for `Close` or `Closed`.

*General notes:*

> **vpin** is the pin number of the output to be controlled by the turnout/point object. For Arduino output pins, this is the same as the digital pin number. For servo outputs and I/O expanders, it is the pin number defined for the HAL device (if present), for example 100-115 for servos attached to the first PCA9685 Servo Controller module, 116-131 for the second PCA9685 module, 164-179 for pins on the first MCP23017 GPIO expander module, and 180-195 for the second MCP23017 module.

#### `<T id DCC addr subaddr>` - Define turnout/point on a DCC Accessory Decoder with the specified address and subaddress

> *Parameters:*  
>
> - **id:** identifier of the Turnout/Point
> - **addr:** ranges from 0 to 511
> - **subaddr:** ranges from 0 to 3
>
> *Response:* ???
>
> **Examples: (click to show)**
>
> > *Example:* `<T 23 DCC 5 0>`
> >
> > *Example:* You have a turnout on your main line going to warehouse industry. The turnout is controlled by an accessory decoder with a address of 123 and is wired to output 3. You want it to have the ID of 10. You would send the following command to the CommandStation: `<T 10 DCC 123 3>`
> >
> > This Command means:
> >
> > > - **T** = (Upper case T) Define a Turnout
> > > - **DCC** = The turnout is DCC Accessory Decoder based
> > > - **10** = ID number I am setting to use this turnout
> > > - **123** = The accessory decoders address
> > > - **3** = The turnout is wired to output 3
> >
> > Next you would send the following command to the EX-CS: `<E>`
> >
> > This Command means:
> >
> > - E : (Upper case E) Store (save) this definition to EEPROM

#### `<T id DCC linearAddr>` - Define turnout/point on a DCC Accessory Decoder with the specified linear address

> *Parameters:*  
>
> - **id:** identifier of the Turnout/Point
> - **linearAddr:** ranges from 1 (address 1/subaddress 0) to 2044 (address 511/subaddress 3).
>
> *Response:* ???
>
> *Example:* `<T 23 DCC 44>` (corresponds to address 11 subaddress 3)

#### `<T id VPIN vpin>` - Define turnout/point output on specified vpin

> *Parameters:*  
>
> - **id:** unique Id for the servo
> - **vpin:** vpin to which the servo is attached
>
> *Response:*  
> Successful: `<O>` Fail: `<X>`
>
> *Example:* `<T 25 VPIN 30>` defines a turnout/point that operates Arduino digital output pin D30. *Example:* `<T 26 VPIN 164>` defines a turnout/point that operates the first pin on the first MCP23017 GPIO expander (if present).
>
> *Notes:*
>
> > See vpin notes above.
> >
> > This may be used for controlling Arduino digital output pins or pins on an I/O Extender.

#### `<T id SERVO vpin thrownPos closedPos profile>` - Define turnout/point servo (PWM) on specified vpin

> *Parameters:*  
>
> - **id:** unique Id for the servo
> - **vpin:** vpin to which the servo is attached
> - **thrownPos:** the PWM value corresponding to the servo position for THROWN state, normally in the range 102 to 490
> - **closedPos:** the PWM value corresponding to the servo position for CLOSED state, normally in the range 102 to 490
> - **profile:** one of
>   - 0=Instant,
>   - 1=Fast (0.5 sec),
>   - 2=Medium (1 sec),
>   - 3=Slow (2 sec) and
>   - 4=Bounce (subject to revision)
>
> *Response:*  
> Successful: `<O>` Fail: `<X>`
>
> *Example:* \<`T 24 SERVO 100 410 205 2>` defines a servo turnout/point on the first PCA9685 pin, moving at medium speed between positions 205 and 410.
>
> *Notes:*
>
> > *Servos are not supported on the minimal HAL (Uno or Nano target).*
> >
> > See vpin notes above.
> >
> > The active and inactive positions are defined in terms of the PWM parameter (0-4095 corresponds to 0-100% PWM). The limits for an SG90 servo are about 102 to 490. The standard range of 1ms to 2ms pulses correspond to values 205 to 409. Profile defines the speed and style of movement: 0=Instant, 1=Fast (0.5 sec), 2=Medium (1 sec), 3=Slow (2 sec) and 4=Bounce (subject to revision).

#### `<T id> - Deletes a turnout by Id`

> *Parameters:*  
>
> - **id:** unique Id for the servod
>
> *Response:*  
> Successful: `<O>` Fail: `<X>` (Id does not exist)

#### `<D SERVO vpin value [profile]>` - Set servo position to value on pin vpin

> *Parameters:*  
>
> - **vpin:** vpin to which the servo is attached
> - **value:** position to mve the servo to
> - **profile:** one of
>   - 0 = instant
>   - 1 = fast
>   - 2 = medium
>   - 3 = slow
>   - 4 = bounce
>
> *Response:* N/A
>
> *Notes:*
>
> > See vpin notes above.

#### `<T id addr subaddr>` - Define a turnout on a DCC Accessory Decoder with the specified address and subaddress - Legacy command Deprecated

> *Parameters:*  
>
> - **id:** identifier of the Turnout/Point
> - **addr:** ???
> - **subaddr:** ???
>
> *Response:* ???
>
> *Version Deprecated:* ???

#### `<T id vpin activePos inactivePos>` - Define a turnout/point servo on specified vpin - Legacy command Deprecated

> *Parameters:*  
>
> - **id:** identifier of the Turnout/Point
> - **vpin:** vpin of the input to be controlled by the sensor object
> - **activePos:** ???
> - **inactivePos:** ???
>
> *Response:* ???
>
> *Version Deprecated: ???*
>
> *Notes:*
>
> > See vpin notes above.
> >
> > The positions are the same as for the turnout/point servo command above. Note: Servos are not supported on the minimal HAL (Uno or Nano target).

Once all turnouts have been properly defined, Use the `<E>` command to store their definitions to EEPROM. If you later make edits/additions/deletions to the turnout definitions, you must invoke the `<E>` command if you want those new definitions updated in the EEPROM. You can also ERASE everything; (turnouts, sensors, and outputs) stored in the EEPROM by invoking the `<e>` (lower case e) command. WARNING: (There is no Un-Delete)

If turnout definitions are stored in EEPROM, the turnout thrown/closed state is also written to EEPROM whenever the turnout is switched. Consequently, when the EX‑CommandStation is restarted the turnout outputs may be set to their last known state (applicable for Servo and VPIN turnouts). This is intended so that the servos don't perform a sweep on power-on when their physical position does not match initial position in the CommandStation.

------------------------------------------------------------------------

### Turntables/Traversers (Configuring the EX-CommandStation)

The Turntable/Traverser commands provide a more flexible and functional way of operating turntables/traversers. These require that the turntable/traverser be pre-defined through the `<I ...>` commands, described below.

Note that a turntable/traverser object must be created using the appropriate `<I ...>` command, and then each desired position must be added using the `<I id ADD ...>` command.

Turntables/traversers may be located at positions from 0 (also known as home) through 48. A common angle of separation for tracks radiating out from the turntable is 7.5 degrees, hence the need for allowing up to 48 positions to be defined.

It is anticipated that throttle developers will be able to "draw" turntables with a visual representation of the location of the home and various defined positions, hence the reason for including an **angle** or **home** variable when defining turntables and positions below. Valid angles are from 0 to 3600, where 3600 = the full 360 degrees, allowing for a single decimal place to be used if partial angles are required. Throttle developers simply need to divide by 10 to obtain the appropriate angle.

*General notes:*

> If there is no desire for throttles to know or understand a position's angle from home, simple set any instance of the **angle** or **home** variable to 0 (zero).

#### `<I id DCC home>` - Define a DCC accessory turntable/traverser

> *Parameters:*  
>
> - **id:** unique Id for the turntable/traverser (1 - 32767)
> - **home:** angle of the home position (0 - 3600)
>
> *Response:*  
> Successful: `<I>` Fail: `<X>`
>
> *Example:* `<I 1 DCC 0>` defines a DCC accessory turntable/traverser with a 0 degree home angle. *Example:* `<I 2 DCC 50>` defines a DCC accessory turntable/traverser with a 5 degree home angle.

#### `<I id EXTT vpin home>` - Define an EX-Turntable turntable/traverser

> *Parameters:*  
>
> - **id:** unique Id for the turntable/traverser (1 - 32767)
> - **vpin:** the Vpin of the EX-Turntable device (must exist and be operational)
> - **home:** angle of the home position (0 - 3600)
>
> *Response:*  
> Successful: `<I>` Fail: `<X>`
>
> *Example:* `<I 1 EXTT 600 0>` defines an EX-Turntable turntable/traverser at Vpin 600 with a 0 degree home angle. *Example:* `<I 2 EXTT 600 50>` defines an EX-Turntable turntable/traverser at Vpin 600 with a 5 degree home angle.

#### `<I id ADD position value angle>` - Add a position to a turntable/traverser

> *Parameters:*  
>
> - **id:** id of the turntable/traverser the position is being added to
> - **position:** position index (1 - 48)
> - **value:** either the number of steps from home for EX-Turntable (1 - 32767), or the linear DCC address for a DCC accessory turntable/traverser
> - **angle:** angle from home for the position (0 - 3600)
>
> *Response:*  
> Successful: `<I>` Fail: `<X>`
>
> *Example:* This example defines a DCC accessory device, with 3 positions:
>
> ``` cpp
> <I 1 DCC 0>          // defines a DCC accessory turntable/traverser with a 0 degree home angle.
> <I 1 ADD 1 201 100>  // adds position 1, which is at linear DCC address 201, and 10 degrees from home.
> <I 1 ADD 2 202 450>  // adds position 2, which is at linear DCC address 202, and 45 degrees from home.
> <I 1 ADD 3 203 1900> // adds position 3, which is at linear DCC address 203, and 190 degrees from home.
> ```
>
> *Example:* This example defines an EX-Turntable device, with 3 positions:
>
> ``` cpp
> <I 2 EXTT 50>         // defines an EX-Turntable turntable/traverser with a 5 degree home angle.
> <I 2 ADD 1 200 100>   // adds position 1, which is 200 steps from home, and 10 degrees from home.
> <I 2 ADD 2 1500 450>  // adds position 2, which is 1500 steps from home, and 45 degrees from home.
> <I 2 ADD 3 8000 1900> // adds position 3, which is 8000 steps from home, and 190 degrees from home.
> ```

------------------------------------------------------------------------

### Sensors (Configuring the EX-CommandStation)

EX‑CommandStation supports Sensor inputs that can be connected to any Arduino Pin not in use by this program, as well as pins on external I/O expanders and other devices. Physical sensors can be of any type (infrared, magnetic, mechanical…). They may be configured to pull-up or not. When configured for pull-up, the input is connected (within the CS) to +5V via a resistor. This sort of input is suited to sensors that have two wires (a switch or relay contacts, or a device with an 'open collector' or 'open drain' output. Some sensors may be sensitive to the pull-up resistor and not operate as expected - in this case you can turn off the pull-up.

The sensor is considered INACTIVE when at +5V potential, and ACTIVE when the pin is pulled down to 0V.

To ensure proper voltage levels, some part of the Sensor circuitry MUST be tied back to the same ground as used by the Arduino.

The Sensor code utilises debouncing logic to eliminate contact 'bounce' generated by mechanical switches on transitions. This avoids the need to create smoothing circuitry for each sensor. You may need to change the parameters in Sensor.cpp through trial and error for your specific sensors, but the default parameters protect against contact bounces for up to 20 milliseconds, which should be adequate for almost all mechanical switches and all electronic sensors.

To monitor one or more Arduino pins for sensor triggers, first define/edit/delete sensor definitions using the following variation of the `<S>` command:

#### `<S id vpin pullup>` - Create a new sensor ID

> *Parameters:*  
>
> - **id:** identifier of the Sensor (0-32767) (You pick the ID & they are shared between Turnouts, Sensors and Outputs)
> - **vpin:** vpin of the input to be controlled by the sensor object For Arduino input pins, this is the same as the digital pin number. For servo inputs and I/O expanders, it is the pin number defined for the HAL device (if present), for example 164-179 for pins on the first MCP23017 GPIO expander module, and 180-195 for the second MCP23017 module.
> - **pullup:** one of
>   - 1=Use pull-up resistor ACTIVE=LOW
>   - 0=don't use pull-up resistor ACTIVE=HIGH
>
> *Response:*  
> Successful: **\<O\>** Fail: **\<X\>** (e.g. out of memory)
>
> *Notes:*
>
> > Once defined, the EX-CS will send a `<Q id>` response anytime the sensor is activated, and a `<q id>` response when deactivated.
> >
> > It is worthwhile creating new IDs to define sensors, for JMRI, using vpin=id. It will simplify your life.

#### `<S id>` - Delete defined sensor

> *Parameters:*  
>
> - **id:** identifier of the Sensor (0-32767)
>
> *Response:*  
> Successful: `<O>` Fail: `<X>` (e.g. ID does not exist)

Once all sensors have been properly defined, use the `<E>` (upper case E) command to store their definitions to EEPROM. If you later make edits/additions/deletions to the sensor definitions, you must invoke the `<E>` (upper case E) command if you want those new definitions updated in the EEPROM. You can also clear everything (turnouts, sensors, and outputs) stored in the EEPROM by invoking the `<e>` (lower case e) command. (There is NO UN-Delete)

All sensors defined as per above are repeatedly and sequentially checked within the main loop of this sketch. If a Sensor Pin is found to have transitioned from one state to another, one of the following serial messages are generated:

- `<Q id>` - for transition of Sensor ID from INACTIVE state to ACTIVE state (i.e. the sensor is triggered)
- `<q id>` - for transition of Sensor ID from ACTIVE state to INACTIVE state (i.e. the sensor is no longer triggered)

Depending on whether the physical sensor is acting as an "event-trigger" or a "detection-sensor", you may decide to ignore the `<q id>` return and only react to `<Q id>` triggers.

#### `</ LATCH vpin>` - Lock sensor ON, preventing external influence

Lock sensor ON, preventing external influence, valid IDs are in the range 0 - 255.

> *Parameters:*  
>
> - **vpin:** identifier of the Sensor (0-255)
>
> *Response:*  
> Successful: ? Fail: ?

#### `</ UNLATCH vpin>` - Unlock sensor, returning to current external state

Unlock sensor, returning to current external state, valid IDs are in the range 0 - 255.

> *Parameters:*  
>
> - **vpin:** identifier of the Sensor (0-255)
>
> *Response:*  
> Successful: ? Fail: ?

Refer to the LATCH/UNLATCH commands in the Sensors/inputs - reading and responding section below for further details.

------------------------------------------------------------------------

### Outputs (Configuring the EX-CommandStation)

EX‑CommandStation supports optional OUTPUT control of any unused Arduino Pins for custom purposes. Pins can be activated or de-activated. The default is to set ACTIVE pins HIGH and INACTIVE pins LOW. However, this default behaviour can be inverted for any pin in which case ACTIVE=LOW and INACTIVE=HIGH.

Definitions and state (ACTIVE/INACTIVE) for pins are retained in EEPROM and restored on power-up. The default is to set each defined pin to active or inactive according to its restored state. However, the default behaviour can be modified so that any pin can be forced to be either active or inactive upon power-up regardless of its previous state before power-down.

To have EX‑CommandStation utilise one or more Arduino pins as custom outputs, first define/edit/delete output definitions using the following variation of the `<Z>` command, or the lowercase `<z>` command can be used with no pre-definition required.

#### `<z vpin> or <z -vpin>` - Control an output pin; no setup required

> *Parameters for the lowercase z command:*  
>
> - **vpin:** the pin or vpin number of the output
> - positive vpin = ACTIVE/HIGH
> - negative vpin = INACTIVE/LOW
>
> *Response:* N/A

#### `<Z id vpin iflag>` - Creates a new output ID, with specified PIN and IFLAG values

> *Parameters:*  
>
> - **id:** identifier of the output
> - **vpin:** the pin number of the output to be controlled by the output object. For Arduino output pins, this is the same as the digital pin number. For servo outputs and I/O expanders, it is the pin number defined for the HAL device (if present), for example 100-115 for servos attached to the first PCA9685 Servo Controller module, 116-131 for the second PCA9685 module, 164-179 for pins on the first MCP23017 GPIO expander module, and 180-195 for the second MCP23017 module.
> - **iflag:** see below
>
> iflag, bit 0:  
>
> - 0 = forward operation (ACTIVE=HIGH / INACTIVE=LOW)
> - 1 = inverted operation (ACTIVE=LOW / INACTIVE=HIGH)
>
> iflag, bit 1:  
>
> - 0 = state of pin restored on power-up to either ACTIVE or INACTIVE depending on state before power-down.
> - 1 = state of pin set on power-up, or when first created, to either ACTIVE of INACTIVE depending on IFLAG, bit 2
>
> iflag, bit 2:  
>
> - 0 = state of pin set to INACTIVE upon power-up or when first created
> - 1 = state of pin set to ACTIVE upon power-up or when first created
>
> *Response:*  
> Successful: `<O>` Fail: `<X>` (e.g. out of memory).
>
> *Notes:*
>
> > if output ID already exists, it is updated with specified vpin and iflag.
> >
> > Output state will be immediately set to ACTIVE/INACTIVE and pin will be set to HIGH/LOW according to iflag value specified (see below).

#### `<Z id>` - Deletes definition of output ID

> *Parameters:*  
>
> - **id:** identifier of the output to delete
>
> *Response:*  
> Successful: `<O>` Fail: `<X>` (e.g. ID does not exist)

#### `<Z>` -Lists all defined output pins

> *Response:*  
> Successful: `<Y id vpin iflag state>` repeated for each defined output pin Fail: `<X>` (e.g. ID does not exist)

#### `<Z id state>` - Sets output ID to either INACTIVE or ACTIVE state

> *Parameters:*  
>
> - **id:** identifier of the output
> - **state:** one of
>   - 0= INACTIVE
>   - 1= INACTIVE
>
> *Response:*  
> Successful: `<Y id state>` Fail: `<X>` if output ID does not exist
>
> *Notes:*
>
> > When controlled as such, the Arduino updates and stores the direction of each output in EEPROM so that it is retained even without power. A list of the current states of each output in the form `<Y id state>` is generated by EX‑CommandStation whenever the `<s>` status command is invoked. This provides an efficient way of initializing the state of any outputs being monitored or controlled by a separate interface or GUI program.

Once all outputs have been properly defined, use the `<E>` Upper Case "E" command to store their definitions to EEPROM. If you later make edits/additions/deletions to the output definitions, you must invoke the `<E>` command if you want those new definitions updated in the EEPROM. You can also **ERASE everything (turnouts, sensors, and outputs)** stored in the EEPROM by invoking the `<e>` (lower case e) command. **(There is no Un-Delete)**

------------------------------------------------------------------------

### EEPROM Management (Configuring the EX-CommandStation)

#### `<D EEPROM>` - Diagnostic dump EEPROM contents

> *Response:* ???

#### `<e>` - Erase ALL (turnouts, sensors, and outputs) from EEPROM

> *Response:*  
> `<O>`

#### `<E>` - Store definitions to EEPROM

> *Response:*  
> `<O>`

------------------------------------------------------------------------

### Diagnostic Programming Commands (Configuring the EX-CommandStation)

#### `<D ACK state>` - Enables ACK diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:*  
> "Ack diag on" or "Ack diag off" Displayed on the serial monitor only.
>
> *Notes:*
>
> > This will turn ACK diagnostics ON and then try to read the appropriate CVs to determine your loco address.

#### `<D ACK LIMIT value>` - Set ACK detection limit mA

> *Parameters:*  
>
> - **value:** in mA
>
> *Response:*  
> TBA

#### `<D ACK minmax value [MS]>` - Set ACK minimum or maximum duration

> *Parameters:*  
>
> - **minmax:** one of
> - `MIN`
> - `MAX`
>
> - **value:** in microseconds unless "MS" is specified
> - **MS:** optional keyword to specify milliseconds
>
> *Response:*  
> TBA

#### `<D ACK RETRY value>` - Set ACK retry count

> *Parameters:*  
>
> - **value:** Retry count
>
> *Response:*  
> TBA

#### `<D CABS>` - Shows cab (loco) numbers and speed in reminder tables

> *Response:*  
> "Used=xxx, max=yyy" Displayed on the serial monitor only.

#### `<D CMD state>` - Enables Command Parser diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A
>
> *Notes:*
>
> > When enabled, diagnostic messages will be shown on the the Serial Monitor.

#### `<D ETHERNET state>` - Enables Ethernet diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A
>
> *Notes:*
>
> > When enabled, diagnostic messages will be shown on the the Serial Monitor.

#### `<D LCN state>` - Enables LCN interface diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A

#### `<D WIFI state>` - Enables WiFi diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A
>
> *Notes:*
>
> > When enabled, diagnostic messages will be shown on the the Serial Monitor.

#### `<D WIT state>` - Enables WiThrottle diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A
>
> *Notes:*
>
> > When enabled, diagnostic messages will be shown on the the Serial Monitor.

#### `<DWEBSOCKET state>` - Enable Websocket diagnostics

> *Parameters:*  
>
> - **state:** one of
> - ON
> - OFF
>
> *Response:* N/A

#### `<D HAL SHOW>` - Shows configured servo board and GPIO extender board config and used pins

> *Response:*  
> List the configured I/O drivers in the Hardware Abstraction Layer (HAL). This command is available from Version 3.2.0.
>
> *Examples*
>
> > Example output showing a connected PCA9685 Servo controller and an MCP23017 I/O expander: \<\* PARSING:D HAL SHOW \*
>
> - \<\* Arduino Vpins:2-69 \*
> - \<\* PCA9685 I2C:x40 Configured on Vpins:100-115 \*
> - \<\* PCA9685 I2C:x41 Configured on Vpins:116-131 OFFLINE \*
> - \<\* MCP23017 I2C:x20 Configured on Vpins:164-179 \*
> - \<\* MCP23017 I2C:x21 Configured on Vpins:180-195 \* \>

#### `<D HAL RESET>` - Reset all HAL devices

> *Response:*  
> TBA

#### `<D RAM>` - Shows remaining RAM (Free Memory)

> *Response:*  
> "Free memory=xxxx" Displayed on the Serial Monitor only.

------------------------------------------------------------------------

### I/O (HAL) Diagnostics

#### `<D ANIN vpin>` - Read and display pin vpin's analogue value

> *Parameters:*  
>
> - **vpin:** ??
>
> *Response:* ???

#### `<D ANOUT vpin value [param2]>` - Write value to analogue vpin

Write value to analogue pin vpin, supplying param2 to the driver.

> *Parameters:*  
>
> - **vpin:** ??
> - **value:** ??
> - **param2:** ??
>
> *Response:* ???

------------------------------------------------------------------------

## Other

### Other Commands

#### `<U cmd>` - Is reserved for user commands (through user filter)

> *Parameters:*  
>
> - **cmd:** user defined command
>
> *Response:* N/A

---

### Broadcasts with no equivalent commands

#### `<m message>` - Broadcast message to all connected native protocol clients

> *Response:*  
> `<m message>`
>
> *Examples*
>
> > \<m This is a message to display\>


\newpage

# EXRAIL Command Reference

EX‑CommandStation provides full automation and accessory control through the Extended Railroad Automation Instruction Language (EXRAIL).

This page includes a reference for most available EXRAIL commands.

<div class="seealso">

Also refer to our new, currently incomplete, web site for additional information on the commands described here: [DCC-EX Command Station Native Commands](https://dcc-ex.com/mkdocs-test/products/ex-commandstation/exrail/command-list/) . Some commands that have only been added recently *may not be covered on this page*, but may be included on the new web site page.

</div>

See Also:

- Introduction to EXRAIL
- Examples
- [DCC-EX Command Station Native Commands](https://dcc-ex.com/mkdocs-test/products/ex-commandstation/exrail/command-list/)

<div class="warning">

<div class="title">

Warning

</div>

Do not waste your time asking ChatGPT, Copilot or Gemini to create EXRAIL scripts. They do not understand EXRAIL and will get it wrong 100% of the time.

</div>

------------------------------------------------------------------------

## Introductory Information

### Conventions used on this page

- CAPITALISED words - These are EXRAIL commands and are case sensitive
- lowercase words within brackets/braces `()` - These are EXRAIL parameters that must be provided, with multiple parameters separated by a comma `,`, for example `SEQUENCE(id)` or `DELAYRANDOM(min_delay, max_delay)`
- Quoted `"text"` - Text within quote marks `""` are used as descriptions, and must include the quote characters, for example `ROUTE(id, "description")` becomes `ROUTE(1, "This is the route description")`
- Square brackets `[]` - Parameters within square brackets `[]` are optional and may be omitted. If specifying these parameters, do not include the square brackets themselves, for example `ALIAS(name[, value])` becomes `ALIAS(MY_ALIAS)` or `ALIAS(MY_ALIAS, 3)`
- `|` - Use of the `|` character means you need to provide one of the provided options only, for example `<D POWER ON|OFF>` becomes either `<D POWER ON>` or `<D POWER OFF>`

### Handy information

- COMMANDS are case sensitive. i.e. they must be in uppercase. Text parameters that you provide (aliases, descriptions) are not
- *AUTOMATION*, *ROUTE*, and *SEQUENCE* use the same ID number space, so a `FOLLOW(n)` command can be used for any of them
- Sensors and outputs used by AT/AFTER/SET/RESET/LATCH/UNLATCH/SERVO/IF/IFNOT refer directly to Arduino pins, and those handled by I2C expansion (as virtual pins or vpins).
- Signals also refer directly to pins, and the signal ID (for RED/AMBER/GREEN) is always the same as the RED signal pin
- It's OK to use sensor IDs that have no physical item in the layout. These can only be LATCHed, tested (IF/IFNOT), or UNLATCHed in the sequences. If a sensor is latched by the sequence, it can only be unlatched by the sequence so `AT(35) LATCH(35)` for example, effectively latches sensor 35 on when detected once
- All IDs used in commands and functions will be numbers, or an ALIAS name if configured
- Most IDs simply need to be unique, however RESERVE/FREE and LATCH/UNLATCH must be in the range 0 - 255

<div class="warning">

<div class="title">

Warning

</div>

You must avoid using these characters in all descriptions: `<`, `>`, `"` as these are part of the DCC-EX protocol and are likely to prevent descriptions showing up in JMRI and other throttle software/clients.

</div>

<div class="warning">

<div class="title">

Warning

</div>

**Do not use leading zeros for any numbers!**

Any number with a leading zero will be treated as an octal number, so for example `ALIAS(MY_ALIAS, 010)` will assign the value of `8` to MY_ALIAS, not `10`. This is a common mistake that can lead to very confusing behavior if you don't know about it. Always use numbers without leading zeros, for example `ALIAS(MY_ALIAS, 10)` to assign the value of 10 to MY_ALIAS.

</div>

<div class="note">

<div class="title">

Note

</div>

There are four uses of ID numbers in EXRAIL:

- AUTOMATION, ROUTE, and SEQUENCE IDs
- Turnout/Point IDs
- Vpins - Includes physical pins on the EX-CommandStation, virtual pins (Vpins) on I/O expander modules, and virtual pins that have no physical presence
- Virtual block IDs as used in RESERVE/FREE

Therefore, you can have an AUTOMATION, a turnout/point, a Vpin, and a virtual block all defined with the same ID without issue as these will not relate to each other. This is probably a great reason to consider aliases to avoid confusion.

</div>

### Correct use of DONE, ENDIF, and FOLLOW() statements

Every EXRAIL automation/route/sequence, event handler, and conditional statement should\* be terminated by one of these three directives.

On this page, you will see various references to the use of `DONE`, `ENDIF`, and `FOLLOW()` which can be confusing, so refer to this quick list to help understand the context in which each of these should be used:

- Every conditional statement (all directives starting with the word `IF`) must be terminated by `ENDIF`
- Every group of commands within a ROUTE, AUTOMATION, or SEQUENCE must be terminated by either `DONE` or `FOLLOW(id)`
- Every event handler (all directives starting with the word `ON`) must be terminated by `DONE`

<div class="note">

<div class="title">

Note

</div>

\* There are exceptions to this rule.

EXRAIL is not a block structured language except for `IF`/`ELSE`/`ENDIF`. Therefor a `SEQUENCE` can be used without a `DONE` statement in certain situations.

For example when using `FOLLOW` to continuously loop back to a `SEQUENCE`. In this case the `FOLLOW` is being used like an old fashioned 'GOTO' statement to create a continuous loop.

</div>

**For example: (click to show)**

> ``` cpp
> // Valid use of a ROUTE with a nested IF statement
> ROUTE(1)
>   IF(46)
>     // Things to be done when sensor ID 46 is active
>   ELSE
>     // Things to be done when sensor ID 46 is inactive
>   ENDIF
>   DONE
>
> // Validate use of a sequence that needs to run continuously
> // DONE is not required in this instance
> SEQUENCE(2)
>   IF(46)
>     // Things to be done when sensor ID 46 is active
>   ELSE
>     // Things to be done when sensor ID 46 is inactive
>   ENDIF
>   FOLLOW(2)
>
> // Validate use of a turnout event handler for turnout ID 200
> ONCLOSE(200)
>   // Things to be done when turnout 200 is closed
>   DONE
> ```

### AT(vpin) or AFTER(vpin \[,debounceTime\]) versus IF(vpin)

When defining conditions, the behavior of `AT()` and `AFTER()` is quite different to using conditional `IF()` statements.

This applies to all directives starting with `AT`, `AFTER`, and `IF`.

When using `AT()` or `AFTER()`, this is a blocking activity, meaning the sequence of activities will not progress beyond this particular directive unless the condition is met.

When using `IF` conditional statements, these will not block if the condition is not met, allowing the sequence of activities to continue.

Note: A negative value for a `vpin` can be used for an active high sensor.

**For example: (click to show)**

> ``` cpp
> // Use of AT() to prevent doing anything until a sensor is activated
> // This sequence will continue to run until the sensor is activated, in which case those activities will be performed, and it will end
> SEQUENCE(1)
>   AT(46)
>     // Things to do when sensor 46 is activated
>   DONE
>
> // Use of IF() to continuously monitor a number of sensors
> // This sequence will continually loop to monitor the sensors, meaning the activities related to each sensor are not blocked by the state of other sensors
> SEQUENCE(2)
>   IF(46)
>     // Things to do if sensor 46 is activated
>   ENDIF
>   IF(47)
>     // Things to do if sensor 47 is activated
>   ENDIF
>   IF(48)
>     // Things to do if sensor 48 is activated
>   ENDIF
>   FOLLOW(2)
> ```

------------------------------------------------------------------------

### Interactive diagnostics and control

Various diagnostic and control commands have been added to control and interact with EXRAIL, including the various sequences and objects once they have been defined in myAutomation.h and uploaded to the EX‑CommandStation.

These commands can be run interactively via the serial console or over Ethernet/WiFi if using a throttle or client that provides a suitable interface for sending native DCC-EX commands.

#### `<D EXRAIL state>` - Enable or disable EXRAIL sequence logging

When the EX‑CommandStation is connected to a Serial Monitor, EXRAIL sequence logging can be turned on or off (Enabled or Disabled).

> **For example: (click to show)**
>
> > Example output from Point to Point Shuttle running SEQUENCE(13) with loco ID 18:
> >
> > ``` cpp
> > <D EXRAIL ON>
> > <p1 MAIN>
> > PPA1
> > <1 18 0 178 0>
> > <* EXRAIL Sensor 42 hit *>
> > <* EXRAIL Sensor 42 hit *>
> > <* EXRAIL drive 18 0 1 *>
> > <1 18 0 128 0>
> > <* EXRAIL drive 18 20 0 *>
> > <1 18 0 20 0>
> > <* EXRAIL Sensor 41 hit *>
> > <* EXRAIL Sensor 41 hit *>
> > <* EXRAIL drive 18 0 0 *>
> > <1 18 0 0 0>
> > <* EXRAIL begin(13) *>
> > <* EXRAIL begin(13) *>
> > <* EXRAIL drive 18 50 1 *>
> > <1 18 0 178 0>
> > ```

#### `</PAUSE>` - Pause ALL EXRAIL automation activities

Pauses **ALL** EXRAIL automation activities, including sending an E-STOP to all locos.

#### `</RESUME>` - Resume **ALL** EXRAIL automation activities

Resume **ALL** EXRAIL automation activities, and resumes all locos at the same speed at which they were paused.

#### `</>` - Display EXRAIL running task information

**For example: (click to show)**

> Example outputs also using Point to Point Shuttle:
>
> - Leaving right side of the shuttle sequence with speed 50F (forward):
>
> ``` cpp
> </>
> <1 18 0 178 0>
> <* EXRAIL STATUS
> ID=0,PC=12,LOCO=0 ,SPEED=0F
> ID=1,PC=12,LOCO=18 ,SPEED=50F *>
> ```

#### `</ START [loco_addr] route_id>` - Start route, optionally using specified loco

Starts a new task to send a loco onto a Route, or activate a non-loco Animation or Sequence.

#### `</ KILL task_id>` - Kills a currently running process

Kills a currently running process by ID

<div class="note">

<div class="title">

Note

</div>

\- task_id is an internally generated ID separate from any of the user defined IDs - the KILL command should only be used when you understand the internals of the exrail task system. It is not designed to be used in normal running.

</div>

#### `</ RESERVE block_id>` - Manually reserves a virtual track Block

Manually reserves a virtual track Block, valid IDs are in the range 0 - 255

#### `</ FREE block_id>` - Manually frees a virtual track Block

Manually frees a virtual track Block, valid IDs are in the range 0 - 255.

#### `</ LATCH vpin>` - Lock sensor ON, preventing external influence

Lock sensor ON, preventing external influence, valid IDs are in the range 0 - 255.

#### `</ UNLATCH vpin>` - Unlock sensor, returning to current external state

Unlock sensor, returning to current external state, valid IDs are in the range 0 - 255.

Refer to the LATCH/UNLATCH commands in the Sensors/inputs - reading and responding section below for further details.

------------------------------------------------------------------------

### Aliases

#### `ALIAS( name[, value] )` - Assigns name to a value

Aliases assigns names to values. They can go anywhere in the sequence. If a value is not assigned, a unique ID will be assigned based on the alias "name" text.

This is a simple substitution that lets you have readable names for things in your sequence. For example, instead of having to remember the VPin a turnout/point is connected to, give the pin number an alias and refer to it by that name. You can use this to name routes, values, pin numbers, or anything you need.

If you simply need a unique identifier for an object used internally to the sequence, such as a turnout/point, route, automation, or sequence, you don't even need to provide an ID, EXRAIL will generate one automatically when you omit the value parameter. We recommend using this for all your routes, sequences, and other internal objects so you don't have to try to remember or keep a list of numbers you've used. This also prevents you from assigning the same number to more than one object.

REMEMBER: IDs for RESERVE/FREE, LATCH/UNLATCH, and pins must be explicitly defined.

To put this another way, if you connect an LED to pin 23 and want to turn it on and off, you have to explicitly set its pin number, so <span class="title-ref">ALIAS(TOWER_LED, 23)</span> lets you equate "23" to TOWER_LED. But if you created a route to run your train around an oval, you don't really need to set the number or even know it. Just use <span class="title-ref">ALIAS(OVAL)</span> and let EX assign a number internally. If you ever wanted to know what number it assigns, you can enter <span class="title-ref">\<? OVAL\></span> from the serial monitor with the EX‑CommandStation running and it will tell you next to "Opcode=". Since this "hash", as it is called, is generated by the alias name word, it is always unique and always the same for that word even if you have not created the alias yet. Fun fact, "OVAL" will always equal 27500.

Alias naming rules:

- **Must not** be an existing EXRAIL command name or other reserved word.
- **Should be** reasonably short but descriptive.
- **Must start** with letters A-Z, a-z, or underscore \_ (case sensitive!).
- **May then** also contain numbers.
- **Must not** contain spaces or special characters.

*Parameters:*

- **name** - name for the Alias. See rules above
- **value** - value to insert in place of the Alias

> **For example: (click to show)**
>
> > Defining a pin turnout/point without an alias:
> >
> > ``` cpp
> > PIN_TURNOUT(1, 25, "Coal Yard")
> > ```
> >
> > Defining a pin turnout/point with aliases:
> >
> > ``` cpp
> > ALIAS(COAL_YARD)
> > ALIAS(COAL_YARD_PIN, 25)
> > PIN_TURNOUT(COAL_YARD, COAL_YARD_PIN, "Coal Yard")
> > ```
> >
> > Note that you could have used the command <span class="title-ref">ALIAS(COAL_YARD, 1)</span> in the example above to explicitly set the number, but unless you have a reason to use specific numbers, let the EX‑CommandStation do it for you.
> >
> > In this simple example, aliases seem like overkill, however consider the case where you need to have the "Coal Yard" turnout/point closed or thrown in various different automation sequences, and you will soon see why it's easier to understand you're throwing the COAL_YARD turnout/point rather than turnout/point ID 12345.

------------------------------------------------------------------------

## Alphabetic Command List

<div class="seealso">

Also refer to our new, currently incomplete, web site for additional information on the commands described here: [DCC-EX Command Station Native Commands](https://dcc-ex.com/mkdocs-test/products/ex-commandstation/exrail/command-list/) . Some commands that have only been added recently *may not be covered on this page*, but may be included on the new web site page.

</div>

**Full Alphabetic list of commands: (click to show)**

> - ACOF
> - ACON
> - ACTIVATE
> - ACTIVATEL
> - AFTER
> - AFTEROVERLOAD
> - ALIAS
> - AMBER
> - ANOUT
> - ASPECT
> - AT
> - ATGTE
> - ATLT
> - ATTIMEOUT
> - ATTIMEOUT1
> - ATTIMEOUT2
> - AUTOMATION
> - AUTOSTART
> - BLINK
> - BROADCAST
> - CALL
> - CLEAR ALL STASH
> - CLEAR STASH
> - CLOSE
> - CONFIG SERVO
> - DCCACTIVATE
> - DCCEX SIGNAL
> - DCC SIGNAL
> - DCC TURNTABLE
> - DEACTIVATE
> - DEACTIVATEL
> - DELAY
> - DELAYMINS
> - DELAYMS
> - DELAYRANDOM
> - DISABLE PROG
> - DONE
> - DRIVE
> - ELSE
> - ENDEXRAIL
> - ENDIF
> - ENDTASK
> - EXRAIL
> - EXRAIL WITHROTTLE
> - ESTOP
> - EXTT TURNTABLE
> - FADE
> - FOFF
> - FOLLOW
> - FON
> - FORGET
> - FREE
> - FTOGGLE
> - FWD
> - GREEN
> - EXRAIL HAL
> - HAL IGNORE DEFAULTS
> - IF
> - IFAMBER
> - IFCLOSED
> - IFGREEN
> - IFGTE
> - IFLOCO
> - IFLT
> - IFNOT
> - IFRANDOM
> - IFRE
> - IFRED
> - IFRESERVE
> - IFTHROWN
> - IFTIMEOUT
> - IFTTPOSITION
> - INVERT DIRECTION
> - IO NO HAL
> - JMRI SENSOR
> - JOIN
> - KILLALL
> - LATCH
> - LCC
> - LCCX
> - LCD
> - LCN
> - MESSAGE
> - MOMENTUM
> - MOVETT
> - NEOPIXEL
> - NEOPIXEL SIGNAL
> - ONACOF
> - ONACON
> - ONACTIVATE
> - ONACTIVATEL
> - ONAMBER
> - ONBUTTON
> - ONCHANGE
> - ONCLOCKMINS
> - ONCLOCKTIME
> - ONCLOSE
> - ONDEACTIVATE
> - ONDEACTIVATEL
> - ONGREEN
> - ONLCC
> - ONOVERLOAD
> - ONRED
> - ONROTATE
> - ONSENSOR
> - ONTHROW
> - ONTIME
> - PAD
> - PARSE
> - PAUSE
> - PICKUP STASH
> - PIN TURNOUT
> - PLAYSOUND
> - POM
> - POWEROFF
> - POWERON
> - PRINT
> - RANDWAIT
> - READ LOCO
> - RED
> - RESERVE
> - RESET
> - RESUME
> - RETURN
> - REV
> - ROSTER
> - ROTATE
> - ROTATE DCC
> - ROUTE
> - ROUTE ACTIVE
> - ROUTE CAPTION
> - ROUTE DISABLED
> - ROUTE HIDDEN
> - ROUTE INACTIVE
> - SCREEN
> - SENDLOCO
> - SEQUENCE
> - SERIAL
> - SERIAL1
> - SERIAL2
> - SERIAL3
> - SERIAL4
> - SERIAL5
> - SERIAL6
> - SERVO
> - SERVO2
> - SERVO SIGNAL
> - SERVO TURNOUT
> - SET
> - SETFREQ
> - SETLOCO
> - SET POWER
> - SET TRACK
> - SIGNAL
> - SIGNALH
> - SPEED
> - START
> - START SEND
> - START SHARED
> - STASH
> - STEALTH
> - STEALTH GLOBAL
> - STOP
> - THROW
> - TOGGLE TURNOUT
> - TT ADDPOSITION
> - TURNOUT
> - TURNOUTL
> - UNJOIN
> - UNLATCH
> - VIRTUAL SIGNAL
> - VIRTUAL TURNOUT
> - WAITFOR
> - WAITFORTT
> - XFOFF
> - XFON
> - XFTOGGLE
> - XFWD
> - XPOM
> - XREV
> - XRESTORE SPEED
> - XSAVE SPEED

------------------------------------------------------------------------

## Flow Control

### Scripts/Sequences - Types and Control

#### `AUTOSTART` - Automatically start sequence at this point during EX-CommandStation startup

A sequence is automatically started at this point during startup.

If you have previously relied on the implied AUTOSTART to run things immediately, as of Version 5.0 you must now add this explicitly to the beginning of myAutomation.h

*Parameters:*

- none

There are three options to define EXRAIL scripts or sequences:

- AUTOMATION
- ROUTE
- SEQUENCE

#### `AUTOMATION( id, "description" )` - Define an automation, advertised to throttles/clients

Define an automation sequence that is advertised to throttles/clients to send a train along.

See Stopping at a Station (simple loop) for a simple example.

*Parameters:*

- **id** - id for the sequence/route/automation
- **description** - description for the sequence/route/automation

#### `ROUTE( id, "description" )` - Define a route, advertised to throttles/clients

Define a route that is advertised to throttles/clients. This can be used to initiate automation sequences such as setting turnouts/points and signals to allow a train to be driven through a specific route on the layout. See Creating routes for various examples.

*Parameters:*

- **id** - id for the sequence/route/automation
- **description** - description for the sequence/route/automation

#### `SEQUENCE( id )` - A general purpose sequence, not advertised to throttles/clients

A general purpose automation sequence that is not advertised to throttles/clients. This may be triggered automatically on startup, or be called by other sequences or activities. See Automating various non-track items, Point to Point Shuttle, and Multiple inter-connected trains for further examples.

*Parameters:*

- **id** - id for the sequence/route/automation
- **description** - description for the sequence/route/automation

All of these sequence types must be terminated by either a `DONE`, `FOLLOW(id)`, or `RETURN` statement. If you use `FOLLOW(id)` or `RETURN`, you do not also need a `DONE` statement as any of these terms will tell EXRAIL that the sequence of events has ended.

#### `DONE` - Completes a Sequence/Route/Animation/Event, or any other automation

Completes a Sequence/Route/Animation/Event handler, and any other automation definition as shown in the various examples on this page and elsewhere in the EXRAIL documentation.

*Parameters:*

- none

<div class="note">

<div class="title">

Note

</div>

You do not need to use `DONE` if you are using `FOLLOW(id)` or `RETURN` to end the sequence, as these also indicate the end of the sequence.

The currently selected loco will stop moving unless you have used a `FOLLOW(id)` or `RETURN` to pass control to another sequence. To prevent this use `SETLOCO(0)` before the `DONE` statement to deselect the current loco.

</div>

#### `ENDTASK` - Completes a Sequence/Route/Animation/Event, or any other automation

Identical to `DONE`.

Completes a Sequence/Route/Animation/Event handler, and any other automation definition as shown in the various examples on this page and elsewhere in the EXRAIL documentation.

*Parameters:*

- none

#### `CALL( id )` - Branch to a separate sequence

Branch to a separate sequence, which will need to <span class="title-ref">RETURN</span> when complete. The current sequence is paused until the called sequence has completed.

*Parameters:*

- **id** - id for the sequence/route/automation to branch to

#### `RETURN` - Return to the calling sequence when completed

Return to the calling sequence when completed (no DONE required).

*Parameters:*

- none

**For example: (click to show)**

> For example, you have an AUTOMATION which you initiate that sends a train through your layout with multiple station stops, and you want to do the same things at each station.
>
> You could write a very long AUTOMATION sequence to do this, or you could write the sound SEQUENCE once, then call it at each station:
>
> ``` cpp
> AUTOMATION(21, "Station loop")    // Our station loop sequence
>   FWD(30)
>   AT(101)                         // At station 1 entrance sensor, call our "Station sequence"
>   CALL(22)
>   AT(102)                         // At station 2 entrance sensor, call our "Station sequence"
>   CALL(22)
>   AT(103)                         // At station 3 entrance sensor, call our "Station sequence"
>   CALL(22)
>   AT(104)                         // At station 4 entrance sensor, call our "Station sequence"
>   CALL(22)
>   FOLLOW(21)                      // Keep looping through the "Station loop" automation (see FOLLOW command reference below)
>
> SEQUENCE(22, "Station sequence")  // Our station sequence
>   FON(2)                         // Blow the horn
>   FON(3)                         // Break squeal
>   STOP                            // Stop at the station
>   FON(4)                         // Let out a hiss from the air breaks for a second
>   DELAY(1000)
>   FOFF(4)
>   DELAYRANDOM(2000, 10000)        // Wait between 2 and 10 seconds for passengers
>   FON(2)                         // Blow the horn again
>   FWD(30)                         // On our way to the next station
>   RETURN                          // Return to the calling sequence
> ```

#### `FOLLOW( sequence_id )` - Branch or Follow a specified sequence

Branch or Follow a specified sequence. The current sequence ends and control is passed to the specified sequence.

This lets us do clever things like performing a different sequence depending on whether a turnout/point is CLOSED or THROWN, as well as simple things such as the example above where we keep looping through the same sequence.

*Parameters:*

- **sequence_id** - id for the sequence/route/automation to branch to

**For example: (click to show)**

> ``` cpp
> AUTOMATION(23, "Choose your own adventure") // This let's someone control the sequence by throwing a turnout/point (or not)
>   FWD(30)
>   AFTER(105)
>   IFTHROWN(106)
>     FOLLOW(24)
>   ELSE
>     FOLLOW(25)
>   ENDIF
>   DONE
>
> SEQUENCE(24, "Adventure 1")                 // Quite a boring adventure to stop in a siding after sensor 106 has activated/deactivated
>   AFTER(106)
>   FON(2)
>   FON(3)
>   STOP
>   DONE
>
> SEQUENCE(25, "Adventure 2")                 // If we don't throw the turnout/point, let's do our station loop from the example above
>   FOLLOW(21)
> ```

#### `PAUSE` - E-STOP all locos and PAUSE all other EXRAIL tasks

E-STOP all locos and PAUSE all other EXRAIL tasks until RESUMEd.

*Parameters:*

- none

#### `RESUME` - Resume all paused tasks, including loco movement

Resume all paused tasks, including loco movement.

*Parameters:*

- none

#### `START( id )` - Execute a route or sequence

Start a new task to execute a route or sequence.

*Parameters:*

- **id** - id for the sequence/route/automation to branch to

#### `START_SEND( id )` - Execute a route or sequence and send the current loco

Starts a new task at the given route/animation/sequence and send the current loco to it. Remove loco from current task.

*Parameters:*

- **id** - id for the sequence/route/automation to branch to

#### `START_SHARED( id )` - Execute a route or sequence and pass the current loco

Starts a new task at the given route/animation/sequence and share the current loco with it.

*Parameters:*

- **id** - id for the sequence/route/automation to branch to

#### `SENDLOCO( loco, route )` - Start route/sequence with a specified loco

Start a new task send a specified loco along a specified route/sequence.

The sequence is started in parallel to the current sequence, so the current sequence continues immediately after the SENDLOCO() command, without waiting for the new sequence to complete.

*Parameters:*

- **loco** - DCC address of your loco
- **route** - route to execute using the specified loco

#### `DELAY( delay )` - Delay the sequence a number of milliseconds

Delay the current sequence a number of milliseconds.

*Parameters:*

- **delay** - period to delay in milliseconds

#### `DELAYMS( delay )` - Delay the sequence a number of milliseconds

Same as `DELAY()`

Delay the current sequence a number of milliseconds.

*Parameters:*

- **delay** - period to delay in milliseconds

#### `DELAYMINS( delay )` - Delay the sequence a number of minutes

Delay the current sequence a number of minutes.

*Parameters:*

- **delay** - period to delay in minutes

#### `DELAYRANDOM( min_delay, max_delay )` - Delay a random period of time

Delay the current sequence a random time between min and max milliseconds.

See Multiple inter-connected trains for good examples.

*Parameters:*

- **min_delay** - minimum period to delay in milliseconds
- **max_delay** - maximum period to delay in milliseconds

**Delay examples: (click to show)**

> ``` cpp
> ONCLOSE(102)      // When turnout 102 closed, wait 2 seconds, then set signal 101 green.
>   DELAY(2000)
>   GREEN(101)
>   DONE
>
> AT(123)           // When sensor 123 is activated, set signal 102 red, wait 1 minute, then set signal 102 green.
>   RED(102)
>   DELAYMINS(1)
>   GREEN(102)
>   DONE
> ```

#### `RANDWAIT( ??? )` - TBA

*Parameters:*

- **???** - ???
- **???** - ???

#### `IFRANDOM( percent )` - Run commands a random percentage of the time

Runs commands in IF block a random percentage of the time. This is handy for more realism by enabling automations that don't have to run on a schedule.

*Parameters:*

- **percent** - percentage to test against (0-100)

**For example: (click to show)**

> ``` cpp
> AT(165)           // When sensor 165 is activated, set a lineside merry-go-round in action for 1 minute 50% of the time.
>   IFRANDOM(50)
>     SET(166)
>     DELAYMINS(1)
>     RESET(166)
>   ENDIF
>   DONE
> ```

#### `ROUTE_CAPTION( route_id, "caption" )` - Change the label of the Route button

Dynamically change the label of the Route button.

*Parameters:*

- **route_id** - id of the route to change
- **caption** - text to replace on the route 'button' label

**For example: (click to show)**

> ``` cpp
> // setup 4 'routes' to switch between tracks/districts between PROG, MAIN and DC
> ROUTE(500,"1.Trk: A main, B prog")
>     SET_TRACK(A,MAIN)
>     SET_TRACK(B,PROG)
>     ROUTE_CAPTION(500,"Active")
>     ROUTE_CAPTION(501,"Inactive")
>     ROUTE_CAPTION(502,"Inactive")
>     ROUTE_CAPTION(503,"Inactive")
>     ROUTE_ACTIVE(500)
>     ROUTE_INACTIVE(501)
>     ROUTE_INACTIVE(502)
>     ROUTE_INACTIVE(503)
> DONE
> ROUTE(501,"2.Trk: A dc10, B dc11") 
>     SETLOCO(10) SET_TRACK(A,DC)
>     SETLOCO(11) SET_TRACK(B,DC)
>     ROUTE_CAPTION(500,"Inactive")
>     ROUTE_CAPTION(501,"Active")
>     ROUTE_CAPTION(502,"Inactive")
>     ROUTE_CAPTION(503,"Inactive")
>     ROUTE_INACTIVE(500)
>     ROUTE_ACTIVE(501)
>     ROUTE_INACTIVE(502)
>     ROUTE_INACTIVE(503)
> DONE
> ROUTE(502,"3.Trk: A dc10, B DCC main") 
>     SETLOCO(10) SET_TRACK(A,DC)
>     SETLOCO(11) SET_TRACK(B,MAIN)
>     ROUTE_CAPTION(500,"Inactive")
>     ROUTE_CAPTION(501,"Inactive")
>     ROUTE_CAPTION(502,"Active")
>     ROUTE_CAPTION(503,"Inactive")
>     ROUTE_INACTIVE(500)
>     ROUTE_INACTIVE(501)
>     ROUTE_ACTIVE(502)
>     ROUTE_INACTIVE(503)
> DONE
> ROUTE(503,"4.Trk: A DCC main, B dc10") 
>     SETLOCO(10) SET_TRACK(A,DC)
>     SETLOCO(11) SET_TRACK(B,MAIN)
>     ROUTE_CAPTION(500,"Inactive")
>     ROUTE_CAPTION(501,"Inactive")
>     ROUTE_CAPTION(502,"Inactive")
>     ROUTE_CAPTION(503,"Active")
>     ROUTE_INACTIVE(500)
>     ROUTE_INACTIVE(501)
>     ROUTE_INACTIVE(502)
>     ROUTE_ACTIVE(503)
> DONE
> ```

#### `ROUTE_ACTIVE( route_id )` - Activate a Route

Dynamically flag a Route as active.

See example in ROUTE_CAPTION.

*Parameters:*

- **route_id** - id of the route to activate

#### `ROUTE_INACTIVE( route_id )` - Deactivate a Route

Dynamically flag a Route as inactive.

See example in ROUTE_CAPTION.

*Parameters:*

- **route_id** - id of the route to deactivate

#### `ROUTE_HIDDEN( route_id )` - Hide a Route from display

Dynamically hide a Route.

*Parameters:*

- **route_id** - id of the route to hide

#### `ROUTE_DISABLED( route_id )` - disable a Route

Dynamically disable a Route.

*Parameters:*

- **route_id** - id of the route to disable

#### `STASH( stash_id )` - Stashes the current loco/invert

*Parameters:*

- **stash_id** - id of the stash location to store the value (0-???)

Stashes/Stores the current loco/invert in the specified stash location.

<div class="note">

<div class="title">

Note

</div>

EXRAIL has the ability to switch the DCC direction meaning of FWD and REV so that it can, for example, use the same sequence to drive a normal train or one where the loco is pulling in reverse. If invert=1 in the stash then the loco needs to be moved in reverse in order for the train to move forward.

</div>

#### `CLEAR_STASH( stash_id )` - Zeroes the specified stash

Zeroes/Empties the specified stash location.

*Parameters:*

- **stash_id** - id of the stash location to store the value (0-???)

#### `CLEAR_ALL_STASH` - Zeroes all stashes

Zeroes/Empties all stash locations.

*Parameters:*

- none

#### `PICKUP_STASH( stash_id )` - Retrieves and sets the loco/invert from the specified stash

Retrieves and sets the loco/invert from the specified stash location.

*Parameters:*

- **stash_id** - id of the stash location to store the value (0-???)

------------------------------------------------------------------------

### Conditional Statements

There are numerous conditional statements available to influence activities based on the states of sensors, signals, turnouts/points, and other items.

Any directive on this page starting with `IF` must have an associated `ENDIF` statement, and optionally an `ELSE` statement if an alternative activity is to be performed.

If a conditional statement is part of an automation sequence, the sequence still needs to be terminated with a `DONE`, `FOLLOW()`, or `RETURN` statement.

This include `IFNOT()`, `IFRED()`, `IFAMBER()`, `IFGREEN()`,

Refer also to Correct use of done, endif, and follow() statements.

#### `IF ( vpin )` ... ELSE ... ENDIF - Execute commands if the conditions are met

Perform the following block of commands if the specified sensor is active.

Optionally be followed by an `ELSE` somewhere in the following commands. Must be followed by an `ENDIF` somewhere in the following commands.

Note: A negative value for a `vpin` can be used for an active high sensor.

*Parameters:*

- **vpin** - vpin (or alias) of the sensor to check
A negative value for a `vpin` can be used for an active high sensor.

Also see `IFNOT()`, `IFRED()`, `IFAMBER()`, `IFGREEN()`, `IFCLOSED()`, `IFTHROWN()`, `IFRANDOM()`, `IFTTPOSITION()`, `IFRE()`, `IFTIMEOUT()`, `IFGTE()`, `IFLT()`, `IFLOCO()`, `IFRESERVE()`

#### `IFNOT ( vpin )` ... ELSE ... ENDIF - Execute commands if the conditions are NOT met

Perform the following block of commands if the specified sensor is not active.

Optionally be followed by an `ELSE` somewhere in the following commands. Must be followed by an `ENDIF` somewhere in the following commands.

Note: A negative value for a `vpin` can be used for an active high sensor.

*Parameters:*

- **vpin** - vpin (or alias) of the sensor to check
A negative value for a `vpin` can be used for an active high sensor.

#### `ELSE` - Alternate logic to any IF related command returning False

Provides alternative logic to any IF related command returning False.

Must be proceeded by an `IF()` somewhere in the preceding commands. Must be followed by an `ENDIF` somewhere in the following commands.

*Parameters:*

- none

#### `ENDIF` - Required to end an IF/IFNOT/etc.

Required to end an IF/IFNOT/etc. (Used in all IF.. functions).

Optionally be proceeded by an `ELSE` somewhere in the preceding commands. Must be proceeded by an `IF()` somewhere in the preceding commands.

*Parameters:*

- none

#### `AT( vpin )` - Halt command execution until the sensor is set

Halt the execution of the current block of commands until the sensor is set.

*Parameters:*

- **vpin** - pin/vpin of the sensor to check
A negative value for a `vpin` can be used for an active high sensor.

#### `AFTER( vpin [,debounce_time] )` - Halt command execution until the sensor is cleared

Halt the execution of the current block of commands until the sensor is cleared.

*Parameters:*

- **vpin** - pin/vpin of the sensor to check
A negative value for a `vpin` can be used for an active high sensor.

- **debounce_time** - optional debounce time (default 500mS)

------------------------------------------------------------------------

## Objects - Definition and Control

### Create and manage HAL device objects

#### `HAL( device, parameters )` - Create a HAL device in myAutomation.h

Create a HAL device in myAutomation.h rather than needing to use myHal.cpp

*Parameters:*

- **device** - device
- **parameters** - as needed

**For example: (click to show)**

> ``` cpp
> // Define a third PCA9685 device following the first two default devices at Vpin 132 and I2C address 0x42
> HAL(PCA9685, 132, 16, 0x42)
>
> // Define a third MCP23017 device following the first two default devices at Vpin 196 and I2C address 0x22
> HAL(MCP23017, 196, 16, 0x22)
>
> // Define a Mega2560 based EX-IOExpander device starting at Vpin 800 at the default I2C address of 0x65
> HAL(EXIOExpander, 800, 62, 0x65)
>
> // Define an EX-Turntable device at the default Vpin 600 and I2C address of 0x60
> HAL(EXTurntable, 600, 1, 0x60)
> ```

#### `HAL_IGNORE_DEFAULTS` - Disable default MCP23017 and PCA9685 HAL devices

Disable default MCP23017 and PCA9685 HAL devices

*Parameters:*

- none

------------------------------------------------------------------------

### Signal Objects - Definition and Control

#### `SIGNAL( red_pin, amber_pin, green_pin )` - Define a pin based signal

Define a pin based signal, which requires three active low pins to be defined to correspond with red, amber, and green lights. Active low means they are activated when the associated pins are set to 0V or ground.

*Parameters:*

- **red_pin** - pin/vpin of the red LED. Also defines the signal_id.
- **amber_pin** - pin/vpin of the amber LED
- **green_pin** - pin/vpin of the green LED

#### `SIGNALH( red_pin, amber_pin, green_pin )` - Define a pin based signal with active high pins

As above to define a pin based signal, but with active high pins instead. Active high means they are activated when the associated pins are set to 5V (or 3.3V if using a 3.3V device).

For both the SIGNAL/SIGNALH commands, signal colour is set using the pin defined for the red pin. If the signal only has two colours (e.g. RED/GREEN), set the unused colour's pin to 0.

*Parameters:*

- **red_pin** - pin/vpin of the red LED. Also defines the signal_id.
- **amber_pin** - pin/vpin of the amber LED
- **green_pin** - pin/vpin of the green LED

#### `SERVO_SIGNAL( vpin, red_pos, amber_pos, green_pos )` - Define a servo based signal

Define a servo based signal, such as semaphore signals. Each position is an angle to turn the servo to, similar to the SERVO/SERVO2 commands, and SERVO_TURNOUT

*Parameters:*

- **vpin** - pin/vpin of the servo
A negative value for a `vpin` can be used for an active high sensor.

- **red_pos** - position to move the servo to for a red signal
- **amber_pos** - position to move the servo to for a amber signal
- **green_pos** - position to move the servo to for a green signal

#### `DCC_SIGNAL( id, addr, sub_addr )` - Define a DCC accessory signal

Define a DCC accessory signal. Control the colour or aspect of these via the defined `id`

#### `DCCX_SIGNAL( Address, redAspect, amberAspect, greenAspect )` - Defines a signal (with id as dcc address)

This defines a signal (with id same as dcc address) that can be operated by the RED/AMBER/GREEN commands. In each case the command uses the signal address to refer to the signal and the aspect chosen depends on the use of the RED AMBER or GREEN command sent. Other aspects may be sent but will require the direct use of the ASPECT command.

The IFRED/IFAMBER/IFGREEN and ONRED/ONAMBER/ONGREEN commands continue to operate as for any other signal type. It is important to be aware that use of the ASPECT (see below) or \<A\> commands will correctly set the IF flags and call the ON handlers if ASPECT is used to set one of the three aspects defined in the DCCX_SIGNAL command.

Direct use of other aspects does not affect the signal flags. ASPECT and \<A\> can be used without defining any signal if the flag management or ON event handlers are not required.

#### `VIRTUAL_SIGNAL( id )` - Define a virtual signal

Define a virtual signal, which is backed by another automation sequence

*Parameters:*

- **id** - id of the virtual signal

#### `IFRED( signal_id )` - Test if signal is red

Test if signal is red.

*Parameters:*

- **signal_id** - id of the virtual signal to test

#### `IFAMBER( signal_id )` - Test if signal is amber

Test if signal is amber

*Parameters:*

- **signal_id** - id of the virtual signal to test

#### `IFGREEN( signal_id )` - Test if signal is green

Test if signal is green

*Parameters:*

- **signal_id** - id of the virtual signal to test

#### `GREEN( signal_id )` - Set a defined signal to GREEN

Set a defined signal to GREEN (see SIGNAL).

*Parameters:*

- **signal_id** - id of the virtual signal to set

#### `AMBER( signal_id )` - Set a defined signal to Amber

Set a defined signal to Amber (See SIGNAL).

*Parameters:*

- **signal_id** - id of the virtual signal to set

#### `RED( signal_id )` - Set defined signal to Red

Set defined signal to Red (See SIGNAL).

*Parameters:*

- **signal_id** - id of the virtual signal to set

#### `ASPECT( address, aspect )` - Command for DCC Extended Accessories

This command sends an extended accessory packet to the track, normally used to set a signal aspect. Aspect numbers are undefined as standards except for 0 which is always considered a stop. The exact aspect codes to be used must be determined from the documentation for the accessory decoder in use.

#### `ONGREEN( signal_id)` - Define event handler for when a signal is set to the green

Define an event handler for when a signal is set to the green aspect.

*Parameters:*

- **signal_id** - id of the virtual signal to set

#### `ONAMBER( signal_id)` - Define event handler for when a signal is set to the amber

Define an event handler for when a signal is set to the amber aspect.

*Parameters:*

- **signal_id** - id of the virtual signal to set

#### `ONRED( signal_id)` - Define event handler for when a signal is set to the red aspect

Define an event handler for when a signal is set to the red aspect.

*Parameters:*

- **signal_id** - id (or alias) of the virtual signal to set

**Signal example: (click to show)**

> ``` cpp
> SIGNAL(25, 26, 27)                // Active low red/amber/green signal using pins 25/26/27 directly on the EX-CommandStation.
> SIGNALH(164 ,0, 165)              // Active high red/green signal using the first two pins of an MCP23017 I/O expander module.
> SERVO_SIGNAL(101, 100, 250, 400)  // Servo based signal using the first PCA9685 servo module.
>
> GREEN(25)                         // Sets our active low signal to green.
> GREEN(164)                         // Sets our active high signal to green.
> GREEN(101)                        // Sets our servo based signal to green.
> ```

------------------------------------------------------------------------

### Turnout/Point Objects - Definition and Control

All the below turnout/point definitions will define turnouts/points that are advertised to wiThrottle Protocol apps, Engine Driver, and JMRI, unless the HIDDEN keyword is used.

"description" is an optional parameter, and must be enclosed in quotes "". If you don't wish this turnout/point to be advertised to throttles, then substitute the word HIDDEN (with no "") instead of the description.

#### `TURNOUT( turnout_id, addr, sub_addr [, "description"]|HIDDEN )` - Define a DCC accessory turnout/point

Define a DCC accessory turnout/point. Note that DCC linear addresses are not supported, and must be converted to address/subaddress in order to be defined. Refer to the Stationary decoder address table (xlsx spreadsheet) for help on these conversions. (or see TURNOUTL below).

*Parameters:*

- **turnout_id** - identifier of the Turnout/Point
- **addr** - ranges from 0 to 511
- **subaddr** - ranges from 0 to 3
- **description** - The description that will be assigned to the turnout/point, or
- *HIDDEN* - keyword - if used instead of the "description" the Turnout/point will not appear in the lists sent to throttle/controllers

#### `TURNOUTL( turnout_id, addr [, "description"]|HIDDEN )` - Define a DCC accessory turnout/point

Define a DCC accessory turnout/point. This command will convert a linear address to the address/subaddress format using the TURNOUT command above.

Note when providing the name of the profile the profile names are case sensitive, and must be written exactly as they appear (e.g. Bounce, not bounce or BOUNCE).

#### `PIN_TURNOUT( turnout_id, pin [, "description"]|HIDDEN )` - Define a pin operated turnout

Define a pin operated turnout. When sending a CLOSE command, the pin will be HIGH, and a THROW command will set the pin LOW.

*Parameters:*

- **turnout_id** - unique Id for the turnout/point servo
- **pin** - pin/vpin to which the servo is attached
- **description** - The description that will be assigned to the turnout/point, or
- *HIDDEN* - keyword - if used instead of the "description" the Turnout/point will not appear in the lists sent to throttle/controllers

#### `SERVO_TURNOUT( turnout_id, pin, active_angle, inactive_angle, profile [, "description"]|HIDDEN )` - Define a servo turnout/point

Define a servo turnout/point. "active_angle" is for THROW, "inactive_angle" is for CLOSE, and profile is one of Instant, Fast, Medium, Slow or Bounce (although clearly we don't recommend Bounce for turnouts/points!).

*Parameters:*

- **turnout_id** - unique Id for the turnout/point servo
- **pin** - vpin to which the servo is attached
- **active_angle** - the PWM value corresponding to the servo position for THROWN state, normally in the range 102 to 490
- **inactive_angle** - the PWM value corresponding to the servo position for CLOSED state, normally in the range 102 to 490
- **profile** - one of
  - `Instant` = Instant,
  - `Fast` = Fast (0.5 sec),
  - `Medium` = Medium (1 sec),
  - `Slow` = Slow (2 sec) and
  - `Bounce` = Bounce (subject to revision)
- **description** - The description that will be assigned to the turnout/point, or
- *HIDDEN* - keyword - if used instead of the "description" the Turnout/point will not appear in the lists sent to throttle/controllers

Refer to Servo module for more information.

#### `VIRTUAL_TURNOUT( turnout_id [, "description"]|HIDDEN )` - Define a virtual turnout, which is backed by another automation sequence

Define a virtual turnout, which is backed by another automation sequence.

For a good example of this refer to Realistic turnout sequences.

*Parameters:*

- **turnout_id** - The id of the turnout/point
- **description** - The description that will be assigned to the turnout/point, or
- *HIDDEN* - keyword - if used instead of the "description" the Turnout/point will not appear in the lists sent to throttle/controllers

**For example: (click to show)**

> ``` cpp
> TURNOUT(100, 26, 0, "Coal Yard")                  // DCC accessory turnout at linear address 101.
> PIN_TURNOUT(101, 164, "Switching Yard")           // Pin turnout on an MCP23017 I/O expander module.
> SERVO_TURNOUT(102, 102, 400, 100, Slow, HIDDEN)   // A servo turnout on a PCA9685 servo module that is hidden from throttles.
> VIRTUAL_TURNOUT(103, "Lumber Yard")               // A virtual turnout which will trigger an automation sequence when CLOSE or THROW is sent.
> ```

#### `IFCLOSED( turnout_id )` - Test if a turnout/point is closed

*Parameters:*

- **turnout_id** - The id of the turnout/point to test

#### `IFTHROWN( turnout_id )` - Test if a turnout/point is thrown

Test if a turnout is thrown

*Parameters:*

- **turnout_id** - The id of the turnout/point to test

#### `ONCLOSE( turnout_id )` - Event handler for when a turnout/point is closed

Event handler for when a turnout/point is sent a close command. Note that there can be only one defined ONCLOSE event for a specific turnout/point.

*Parameters:*

- **turnout_id** - The id of the turnout/point

#### `ONTHROW( turnout_id )` - Event handler for when a turnout/point is thrown

Event handler for when a turnout/point is sent a throw command. Note that there can be only one defined ONTHROW event for a specific turnout/point.

*Parameters:*

- **turnout_id** - The id of the turnout/point

#### `CLOSE( turnout_id )` - Close a turnout/point

Closes a defined turnout/point.

*Parameters:*

- **turnout_id** - The id of the turnout/point to close

#### `THROW( turnout_id )` - Throw a turnout/point

Throws a defined turnout/point.

*Parameters:*

- **turnout_id** - The id of the turnout/point to throw

#### `TOGGLE_TURNOUT( turnout_id )` - Toggle a defined turnout/point between CLOSE/THROW

Toggles the state of the specified turnout/point between closed and thrown.

*Parameters:*

- **turnout_id** - The id of the turnout/point to throw

------------------------------------------------------------------------

### Turntable/Traverser Objects - Definition and Control

Also refer to Exrail definition and control.

<div id="movett">

`MOVETT( id, steps, activity )` - Move a EX‑Turntable to a step position and perform an activity ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

</div>

Move the specified EX‑Turntable to the provided step position and perform the specified activity.

*Parameters:*

- **id** - The id of the turntable
- **steps** - The step position to move to
- **activity** - The activity to perform

<div class="note">

<div class="title">

Note

</div>

From version 5.4.0, we highly recommend using our new turntable/traverser commands which allow turntables/traversers to be advertised to throttles similarly to how turnout/point objects are advertised and operated. Refer to Turntable features.

</div>

#### `IFRE ( vpin, value )` - Test if a rotary encoder has been set to a value

Test if a rotary encoder has been set to the specified value

*Parameters:*

- **vpin** - The VPin the encoder is connected to
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test

#### `ONCHANGE( vpin )` - Detects a rotary encoder has changed position

Detects a rotary encoder has changed position

*Parameters:*

- **vpin** - The VPin the encoder is connected to
A negative value for a `vpin` can be used for an active high sensor.

**For example: (click to show)**

> ``` cpp
> ONCHANGE(700)     // If rotary encoder ID 700 change state do this sequence
>   IFRE(700, 1)    // If rotary encoder ID 700 is at position 1, start ROUTE ID 123
>     START(123)
>   ENDIF
>   IFRE(700, 2)    // If rotary encoder ID 700 is at position 2, start ROUTE ID 124
>     START(124)
>   ENDIF
>   DONE
> ```

#### Turntable features

All the below turntable/traverser definitions will define turntables/traversers that are advertised to throttles that understand them, unless the HIDDEN keyword is used.

To fully define a turntable/traverser object, you need to define the object first, and then one or more positions.

"description" is an optional parameter, and must be enclosed in quotes "". If you don't wish this turntable/traverser to be advertised to throttles, then substitute the word HIDDEN (with no "") instead of the description.

#### `DCC_TURNTABLE( id, home_angle, [, "description"] )` - Define a DCC accessory turntable/traverser

Define a DCC accessory turntable/traverser at the specified **id** and the **home_angle** angle.

*Parameters:*

- **id** - id of the turntable/traverser, valid IDs are 1 - 32767
- **home_angle** - the angle of the home position, valid angles are 0 - 3600

#### `EXTT_TURNTABLE( id, vpin, home_angle, [, "description"] )` - Define an EX-Turntable turntable/traverser

Define an EX-Turntable turntable/traverser at the specified **id** and **vpin** with a **home_angle** angle.

This statement will create the EX‑Turntable turntable/traverser object only, so you will need a separate `HAL()` statement for an EX‑Turntable device to create the HAL device. It is not recommended to create it via "myHal.cpp".

The HAL creation will require the **vpin** and **i2c_address** parameters.

*Parameters:*

- **id** - id of the turntable/traverser, valid IDs are 1 - 32767
- **vpin** - id of the vpin where the EX‑Turntable device is located
- **i2c_address** - the I2C address of the EX‑Turntable device
- **home_angle** - the angle of the home position, valid angles are 0 - 3600

Example creation and definition:

``` cpp
HAL(EXTurntable,600,1,0x60)            // Create your EX-Turntable device driver
EXTT_TURNTABLE(1,600,45,"My EX-Turntable")  // Create your EX-Turntable object to enable control
```

#### `TT_ADDPOSITION( id, position_id, value, angle [, "description"] )` - Add a turntable position

Add a position to a turntable/traverser object **turntable_id** with position index **position_id**, step or DCC address **value**, **angle** degrees from home.

*Parameters:*

- **id** - id of the turntable/traverser, which must be created prior to adding positions
- **position_id** - index of the position to add, valid positions are (1 - 48)
- **value** - either steps from home for EX-Turntable, or the linear DCC address for a DCC accessory turntable, valid values are (1 - 32767)
- **angle** - angle of the position from the home position, valid angles are (0 - 3600)

#### `IFTTPOSITION( id, position )` - Test if turntable/traverser is at a position

Tests if the turntable/traverser at the specified **id** is at the specified **position**.

*Parameters:*

- **id** - id of the turntable/traverser to test. (1 - 32767)
- **position** - position to rotate to. (1 - 48)

#### `ONROTATE( id )` - Event handler for when a turntable/traverser is rotated

Triggers the event handling mechanism for turntable/traverser **id** if configured. Note that there can be only one defined ONROTATE event for a specific turntable/traverser.

*Parameters:*

- **id** - id of the turntable/traverser to test (1 - 32767)

#### `ROTATE( id, position, activity )` - Rotate an EX-Turntable turntable/traverser

Rotate an EX-Turntable turntable/traverser at the specified **id** to the specified **position**, and perform **activity**.

*Parameters:*

- **id** - id of the turntable/traverser, valid IDs are (1 - 32767)
- **position** - position to rotate to, valid positions are (1 - 48)
- **activity** - refer to Ex-turntable activity reference, using the "EXRAIL activity" column

#### `ROTATE_DCC( id, position )` - Rotate a DCC accessory turntable/traverser

Rotate a DCC accessory turntable/traverser at the specified **id** to the specified **position**.

*Parameters:*

- **id** - id of the turntable/traverser, valid IDs are (1 - 32767)
- **position** - position to rotate to, valid positions are (1 - 48)

#### `WAITFORTT( id )` - Wait for EX-Turntable turntable/traverser to complete a rotation

Wait for the EX-Turntable turntable/traverser at **id** to complete a rotation. As no feedback can be received from DCC accessory turntables, this is only valid for EX-Turntable.

*Parameters:*

- **id** - id of the turntable to test

------------------------------------------------------------------------

### Sensors/Inputs - Reading and Responding

#### `JMRI_SENSOR(vpin [,count])` - Creates \<S\> type sensors visible to JMRI

This command causes the creation of JMRI \<S\> type sensors in a way that is simpler than repeating lines of \<S\> commands in mySetup.h.

- JMRI_SENSOR(100) is equivalent to \<S 100 100 1\>
- JMRI_SENSOR(100,16) will create \<S\> type sensors for vpins 100-115.

*Parameters:*

- **vpin** - vpin to create
- **count** - optional. Number of sensors to create. Inclusive on vpin. Default is one (1)

#### `AT( vpin )` - Causes a sequence to wait until a sensor is active/triggered

A sequence will not progress until a sensor has been triggered.

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

#### `AFTER( vpin )` - Causes a sequence to wait until after a sensor has been triggered

A sequence will not progress until after a sensor has been triggered and then is off for 0.5 seconds.

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

#### `ATTIMEOUT( vpin, timeout_ms )` - Causes a sequence to wait until either a sensor is active/triggered, or if the timer runs out

A sequence will not progress until either a sensor is active/triggered, or if the timer runs out. It then continues and sets a testable "timed out" flag (see `IFTIMEOUT`).

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **timeout_ms** - time/duration to wait for in milliseconds

#### `IF( vpin )` - If sensor activated or latched, continue

If sensor activated or latched, continue. Otherwise skip to ELSE or matching ENDIF.

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

See the Conditional Statements section for more information on IF ... ELSE ... ENDIF commands.

#### `IFNOT( vpin )` - If sensor NOT activated and NOT latched, continue

If sensor NOT activated and NOT latched, continue. Otherwise skip to ELSE or matching ENDIF.

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

See the Conditional Statements section for more information on IF ... ELSE ... ENDIF commands.

#### `IFTIMEOUT` - Tests if "timed out" flag has been set by an ATTIMEOUT() sensor reading attempt

Tests if "timed out" flag has been set by an ATTIMEOUT() sensor reading attempt.

*Parameters:*

- none

Note that with the sensor commands <span class="title-ref">IF()</span>, <span class="title-ref">IFNOT()</span>, <span class="title-ref">IFTIMEOUT()</span>, <span class="title-ref">AT()</span>, <span class="title-ref">ATTIMEOUT()</span>, and <span class="title-ref">AFTER()</span>, you can use negative values to enable the use of active HIGH sensors.

**For example: (click to show)**

> ``` cpp
> AT(40)        // Wait for pin 40 to go low.
> AT(-40)       // Wait for pin 40 to go high.
> ```

#### `ATGTE( vpin, value )` - Waits for an analog pin to reach a value

Waits for an analog pin to reach the specified value.

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

#### `ATLT ( vpin, value )` - Waits for an analog pin to go below a value

Waits for an analog pin to go below the specified value.

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

#### `IFGTE( vpin, value )` - Test if analog pin reading is greater than or equal to value

Test if analog pin reading is greater than or equal to value (\>=).

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

#### `IFLT( vpin, value )` - Test if analog pin reading is less than value

Test if analog pin reading is less than value (\<).

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

> All the <span class="title-ref">IFGTE()</span>, <span class="title-ref">IFLT()</span>, <span class="title-ref">ATGTE()\`and \`ATLT()</span> commands read the analog value from an analog input pin (A0 - A5 on an Arduino Mega) or an analog input from an I/O expander module. Valid values are defined by the capability of the analog to digital converter in use.

**Sensor examples: (click to show)**

> ``` cpp
> IF(25)          // If sensor on the EX-CommandStation pin 25 is activated, set a signal red, wait 10 seconds, then close a turnout/point.
>   RED(101)
>   DELAY(10)
>   CLOSE(200)
> ENDIF
>
> IFNOT(26)       // If sensor on the EX-CommandStation pin 26 is not activated, keep our pedestrian crossing light at 102 green, else set it red.
>   GREEN(102)
> ELSE
>   RED(102)
> ENDIF
>
> IFGTE(A2, 512)  // If reading the analog input from a photoelectric light sensor exceeds 512, it's bright enough to turn the street lights off.
>   RESET(164)
> ENDIF
>
> IFLT(A3, 10)   // If current sensing from an analog occupancy detector had dropped below the threshold, turn off our mimic panel light, otherwise turn it on.
>   RESET(165)
> ELSE
>   SET(165)
> ENDIF
> ```

#### `ATTIMOUT1 ( vpin, value )` - TBA

Waits for ???.

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

#### `ATTIMOUT2 ( vpin, value )` - TBA

Waits for ???.

*Parameters:*

- **vpin** - analogue pin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

- **value** - value to test against

#### `DRIVE ( vpin )` - TBA

???

*Parameters:*

- **vpin** - analogue pin of the sensor to ???
A negative value for a `vpin` can be used for an active high sensor.

#### `LATCH( vpin )` - Latches a sensor on

Latches a sensor on (Sensors 0-255 only).

*Parameters:*

- **vpin** - pin/vpin of the sensor to latch

See UNLATCH() for examples.

#### `UNLATCH( vpin )` - Remove LATCH on sensor

Remove LATCH on sensor.

*Parameters:*

- **vpin** - pin/vpin of the sensor to unlatch

**For example: (click to show)**

> In this example, LATCH/UNLATCH is used to toggle between two different activities each time the ROUTE is selected in a WiThrottle:
>
> ``` cpp
> TURNOUT(17, 30, 1, "Bay to Shed") // DCC turnout/point with linear address 117
>
> ALIAS(BayExitStarter, 107)        // Starter Signal with Route board
> ALIAS(ROUTE_TOGGLE, 11)           // State flag to toggle
>
> ROUTE(11, "Bay to Shed")
>   IF(ROUTE_TOGGLE)             // If ROUTE_TOGGLE is active, reset the route
>     DEACTIVATEL(BayExitStarter)
>     DELAY(20)
>     CLOSE(17)
>     UNLATCH(ROUTE_TOGGLE)           // UNLATCH (Clear) ROUTE_TOGGLE
>   ELSE                            // LATCH is not active, so set route and LATCH
>     THROW(17)
>     DELAY(20)
>     ACTIVATEL(BayExitStarter)
>     LATCH(ROUTE_TOGGLE)         // LATCH ROUTE_TOGGLE to indicate route set
>   ENDIF
> DONE
> ```

**For example: (click to show)**

> In this example, LATCH/UNLATCH is used to start/stop a separate running sequence.
>
> ``` cpp
> ROUTE(1,"Shuttle")
>   SETLOCO(3)
>   IF(99) 
>     UNLATCH(99) 
>     DONE 
>   ENDIF
>   LATCH(99)
> FOLLOW(2)   // this line is not actully needed
>
> SEQUENCE(2)
>   .... move loco etc
>   IF(99) 
>     FOLLOW(2) 
>   ENDIF
> DONE // will also stop loco
> ```

LATCH/UNLATCH can be used to maintain the state of a sensor, or can also be used to trigger a virtual sensor to act as a state flag for EXRAIL. As this effects the state of a sensor, it can be tested via IF/IFNOT and will also work with AT/AFTER.

#### `ONBUTTON( vpin )` - Event handler for debounced button presses

This new event handler is handy for mimic panel and other buttons that need to perform an action when a button is pressed, rather than having to create a sequence with a combination of `AFTER` and `IF` statements to debounce a button which quickly becomes very complicated.

Note that this works for active low buttons only.

*Parameters:*

- **vpin** - pin/vpin to test
A negative value for a `vpin` can be used for an active high sensor.

#### `ONSENSOR( vpin )` - Event handler for sensors

A new event handler to perform actions when a sensor is activated. Like the other sensor triggers such as `IF`, `AT`, and `AFTER`, a negative value can be used for an active high sensor.

*Parameters:*

- **vpin** - pin/vpin of the sensor to test
A negative value for a `vpin` can be used for an active high sensor.

------------------------------------------------------------------------

### Output and LED control

#### `SET( vpin [,count] )` - Set an output pin HIGH

Set output pin (set to HIGH)

*Parameters:*

- **vpin** - The first pin number connected that you which to change
- **count** - optional number of pins to change, starting from and including **pin**. Default is one

#### `RESET( vpin [,count] )` - Reset output pin

Reset output pin (set to LOW)

*Parameters:*

- **vpin** - The first pin number connected that you which to change
- **count** - optional number of pins to change, starting from and including **pin**. Default is one

#### `FADE( vpin, value, ms )` - Fade an LED

Fade an LED on a servo driver to specified value taking specified time.

*Parameters:*

- **vpin** - pin of the LED
- **value** - value to fade the pin to
- **ms** - duration taken to get to the value in milliseconds

#### `BLINK( vpin, onMs, offMs )` - Blink an output pin

This will start a pin/Vpin blinking until such time as it is `SET`, `RESET`, or set via a signal operation.

*Parameters:*

- **vpin** - pin of the LED
- **onMs** - time/duration for the pin to be on in milliseconds
- **offMs** - off time/duration in milliseconds

> ``` cpp
> BLINK(22, 500, 500) // Blink pin 22 at half second intervals
> ```

#### `LCN( "msg" )` - Send message to LCN Accessory Network

Send message to LCN Accessory Network.

*Parameters:*

- **msg** - message to write

#### `CONFIGURE_SERVO(vpin, pos1, pos2, profile)` - Define LED's connected to PCA9685 boards

This command offers a more convenient way of defining an LED connected to a PCA9685 pin, instead of performing the HAL call in halSetup.h

*Parameters:*

- **vpin** - The VPin the LED is connected to, e.g. 101 for the second pin on the first PCA9685 servo module
- **pos1** - The desired intensity (brightness) of the LED when turned on, with 0 being off, and 4095 being 100%)
- **pos2** - The desired intensity (brightness) of the LED when turned off
- **profile** - the required profile

*Examples:*  
previously in mySetup.h you would have used: IODevice::configureServo(112,2437,0,PCA9685::NoPowerOff); Now in myAutomation.h use: CONFIGURE_SERVO(111, 2437, 0, PCA9685::NoPowerOff)

#### `NEOPIXEL( vpin, red, green, blue [,count] )` - Controls the colour of attached Neopixel LEDs

Controls the colour of one or more attached Neopixel LEDs

*Parameters:*

- **vpin** - The VPin the first Neopixel connected that you which to change
- **red** - The desired red colour value (0-255)
- **green** - The desired red colour value (0-255)
- **blue** - The desired red colour value (0-255)
- **count** - number of Neopixels to change, starting from and including **vpin**. Default is one

*Examples:*  
NEOPIXEL(100,255,255,255,10) // set 10 Neopixels LEDs to white starting at vpin 100

#### `NEOPIXEL_SIGNAL( signalid, red, green, blue )` - Controls the colour of attached Neopixel LED

Controls the colour of one attached Neopixel LED

*Parameters:*

- **signalid** - The VPin the first Neopixel connected that you which to change
- **red** - The desired red colour value (0-255)
- **green** - The desired red colour value (0-255)
- **blue** - The desired red colour value (0-255)

*Examples:*  
NEOPIXEL_SIGNAL(100,255,255,255) // set one Neopixel LED to white

#### `ANOUT( vpin, value, param1, param2)` - Analog output ??

*Parameters:*

- **vpin** - first VPIN allocated
- **value** - ???
- **param1** - ???
- **param2** - ???

*Examples:*  
ANOUT(10000,23,0,0) // will play the 23rd mp3 file. ANOUT(10000,23,30,0) // will do the same thing, as well as setting the volume to 30 (maximum value).

**For example: (click to show)**

> ``` cpp
> //=======================================================================
> // Play mp3 files from a Micro-SD card, using a DFPlayer MP3 Module.
> //=======================================================================
> // Parameters: 
> //   10000 = first VPIN allocated.
> //   10 = number of VPINs allocated.
> //   Serial1 = name of serial port (usually Serial1 or Serial2).
> // With these parameters, up to 10 files may be played on pins 10000-10009.
> // Play is started from EXRAIL with SET(10000) for first mp3 file, SET(10001)
> // for second file, etc.  Play may also be initiated by writing an analogue
> // value to the first pin, e.g. ANOUT(10000,23,0,0) will play the 23rd mp3 file.
> // ANOUT(10000,23,30,0) will do the same thing, as well as setting the volume to 
> // 30 (maximum value).
> // Play is stopped by RESET(10000) (or any other allocated VPIN).
> // Volume may also be set by writing an analogue value to the second pin for the player, 
> // e.g. ANOUT(10001,30,0,0) sets volume to maximum (30).
> // The EXRAIL sequence may check for completion of play by calling WAITFOR(pin), which will only proceed to the
> // following line when the player is no longer busy.
> // E.g.
> //    SEQUENCE(1)
> //      AT(164)           // Wait for sensor attached to pin 164 to activate
> //      SET(10003)        // Play fourth MP3 file
> //      LCD(4, "Playing") // Display message on LCD/OLED
> //      WAITFOR(10003)    // Wait for playing to finish
> //      LCD(4, "")       // Clear LCD/OLED line 
> //      FOLLOW(1)         // Go back to start
>
> // in myHAL.cpp file use
>  // DFPlayer::create(10000, 10, Serial1);
> // or within myAutomation.h file use
>  // HAL (DFPlayer, 10000, 10, Serial1)
> ```

#### `PLAYSOUND( vpin, fileNumber, volume )` - Play mp3 files from a Micro-SD card

EXRAIL Function to Play mp3 files from a Micro-SD card, using a DFPlayer MP3 Module.

Alias of ANOUT.

*Parameters:*

- **vpin** - VPIN allocated as DFPLayer
- **fileNumber** - Play the File#
- **volume** - volume (0-30)

------------------------------------------------------------------------

### Servo Control

#### `SERVO( id, position, profile )` - Move an animation servo

Move an animation servo. *Do NOT use for Turnouts/points.*

*Parameters:*

- **id** - id of the servo to move
- **position** - position to move to
- **profile** - one of
  - **Instant** = Instant,
  - **Fast** = Fast (0.5 sec),
  - **Medium** = Medium (1 sec),
  - **Slow** = Slow (2 sec) and
  - **Bounce** = Bounce (subject to revision)

#### `SERVO2( id, position, duration )` - Move an animation servo taking duration

Move an animation servo taking duration in milliseconds. *Do NOT use for Turnouts/points*

*Parameters:*

- **id** - id of the servo to move
- **position** - position to move to
- **duration** - duration of the move in milliseconds

#### `WAITFOR( pin )` - Wait for a servo motion to complete prior to continuing

The WAITFOR() command instructs EXRAIL to wait for a servo motion to complete prior to continuing.

*Parameters:*

- **pin** - vpin to test

**A couple of examples: (click to show)**

> ``` cpp
> // First example defines a servo turnout/point for the coal yard and a signal for the main line.
> TURNOUT(100, 26, 0, "Coal Yard")
> SIGNAL(25, 26, 27)
>
> // When our turnout/point is closed, the main line is open, so the signal is green.
> ONCLOSE(100)
>   GREEN(25)
> DONE
>
> // When our turnout is closed, the main line is interrupted, so the signal is red.
> ONTHROW(100)
>   RED(25)
> DONE
>
> // This example triggers an automation sequence when a DCC accessory decoder is activated, including waiting for SERVO motions to complete.
> ONACTIVATEL(100)            // Activating DCC accessory decoder with linear address 100 commences the sequence.
>   SERVO(101, 400, Slow)     // Move the first servo and wait.
>   WAITFOR(101)
>   SERVO(102, 300, Medium)   // Move the second servo and wait.
>   WAITFOR(102)
>   SET(165)                  // Activate a Vpin to turn an LED on.
>   SET(166)                  // Activate a second Vpin to turn a second LED on.
> DONE
> ```

------------------------------------------------------------------------

### DCC Accessory Decoder Control

#### `ONACTIVATE( addr, sub_addr )` - Event handler for 2 part DCC accessory packet value 1

Event handler for 2 part DCC accessory packet value 1

All these "ON" commands are event handlers that trigger a sequence of commands to run when the event occurs. These can vary from the most basic tasks such as setting signals when turnouts are closed or thrown, to triggering complete automation sequences via a DCC accessory decoder.

*Parameters:*

- **addr** - DCC address ???
- **Sub_addr** - sub-address ???

#### `ONACTIVATEL( linear )` - Event handler for linear DCC accessory packet value 1

Event handler for linear DCC accessory packet value 1

All these "ON" commands are event handlers that trigger a sequence of commands to run when the event occurs. These can vary from the most basic tasks such as setting signals when turnouts are closed or thrown, to triggering complete automation sequences via a DCC accessory decoder.

*Parameters:*

- **linear** - ???

#### `ONDEACTIVATE( addr, sub_addr )` - Event handler for 2 part DCC accessory packet value 0

Event handler for 2 part DCC accessory packet value 0

All these "ON" commands are event handlers that trigger a sequence of commands to run when the event occurs. These can vary from the most basic tasks such as setting signals when turnouts are closed or thrown, to triggering complete automation sequences via a DCC accessory decoder.

*Parameters:*

- **addr** - DCC address ???
- **Sub_addr** - sub-address ???

#### `ONDEACTIVATEL( linear )` - Event handler for linear DCC accessory packet value 0

Event handler for linear DCC accessory packet value 0.

*Parameters:*

- **linear** - ???

#### `ACTIVATE( addr, sub_addr )` - Sends a DCC accessory packet with value 1

Sends a DCC accessory packet with value 1.

*Parameters:*

- **addr** - DCC address ???
- **Sub_addr** - sub-address ???

#### `ACTIVATEL( linear )` - Sends a DCC accessory packet with value 1 to a linear address

Sends a DCC accessory packet with value 1 to a linear address.

*Parameters:*

- **linear** - ???

#### `DEACTIVATE( addr, sub_addr )` - Sends a DCC accessory packet with value 0

Sends a DCC accessory packet with value 0.

*Parameters:*

- **addr** - DCC address ???
- **Sub_addr** - sub-address ???

#### `DEACTIVATEL( addr )` - Sends a DCC accessory packet with value 0 to a linear address

Sends a DCC accessory packet with value 0 to a linear address

*Parameters:*

- **addr** - DCC address ???

#### `DCCACTIVATE( addr, sub_addr )` - TBA

*Parameters:*

- **addr** - DCC address ???
- **Sub_addr** - sub-address ???

------------------------------------------------------------------------

### EX-FastClock Event Handlers

Also refer to Controlling exrail by time.

#### `ONTIME( value )` - Event handler for when the specified time is reached

Event handler for when the specified time is reached

*Parameters:*

- **value** - value to test against

#### `ONCLOCKTIME( hours, mins )` - Event handler for when the specified clock time is reached

Event handler for when the specified clock time is reached

*Parameters:*

- **hour** - hour to test against
- **minute** - minute to test against

#### `ONCLOCKMINS( mins )` - Event handler to be repeated the same time every hour

Event handler to be repeated the same time every hour

*Parameters:*

- **minute** - minute to test against

------------------------------------------------------------------------

## Locos and Tracks

### Locos - Definition and Control

#### `ESTOP` - Emergency stops all locomotives

Emergency stops all locomotives.

*Parameters:*

- none

#### `SETLOCO( loco )` - Set the loco address for this task

Set the loco address for this sequence.

*Parameters:*

- **loco** - DCC address of your loco

#### `READ_LOCO` - Read loco ID from prog track

Read the loco ID from prog track.

*Parameters:*

- none

#### `FWD( speed )` - Drive loco forward at DCC speed

Drive loco forward at DCC speed 0-127 (1=ESTOP)

*Parameters:*

- **speed** - DCC speed (0-127)
- 2-127 = speed 1-126
- 0 = stop
- 1 = Estop

#### `REV( speed )` - Drive loco in reverse at DCC speed

Drive current loco in reverse at DCC speed 0-127 (1=ESTOP)

*Parameters:*

- **speed** - DCC speed (0-127)
- 2-127 = speed 1-126
- 0 = stop
- 1 = Estop

#### `SPEED( speed )` - Drive loco in current direction at DCC speed

Drive loco in current direction at DCC speed

*Parameters:*

- **speed** - DCC speed (0-127)
- 2-127 = speed 1-126
- 0 = stop
- 1 = Estop

#### `STOP` - Set loco speed to 0

Set the current loco speed to 0 (same as SPEED(0))

*Parameters:*

- none

#### `MOMENTUM( accel [,decel])` - Set loco momentum

Set the current loco's momentum.

*Parameters:*

- **accel** - acceleration (in milliseconds)
- **accel** - acceleration (in milliseconds)
  - if decel is not specified, it will be set to the same value as accel

Setting Momentum 7,14,21 etc is similar in effect to setting a decoder CV03/CV04 to 1,2,3.

As an additional option, the momentum calculation is based on the difference in throttle setting and actual speed. For example, the time taken to reach speed 50 from a standing start would be less if the throttle were set to speed 100, thus increasing the acceleration.

#### `FON( func )` - Turn on loco function

Turn on the specified function for the current loco.

*Parameters:*

- **func** - Function number (0-31)

#### `FOFF( func )` - Turn off loco function

Turn off the specified function for the current loco.

*Parameters:*

- **func** - Function number (0-31)

#### `FTOGGLE( func )` - Toggle the state of a loco's function

Toggle off the specified function for the current loco. i.e. Turn off if on, or on if off.

*Parameters:*

- **func** - Function number (0-31)

#### `INVERT_DIRECTION` - Switches FWD/REV meaning for loco

Switches FWD/REV meaning for the current loco.

*Parameters:*

- none

#### `ROSTER( loco, "name", "func_map" )` - Provide roster info for a specified loco

*Parameters:*

- **loco** - DCC address of your loco
- **name** - the name of this loco that will appear in the throttle apps. Enclosed in quotes (")
- **funct_map** - the names that you want to see for the functions specific to this loco separated by forward slashes ("/"). All enclosed in quotes (") Note that if the function is 'momentary' rather than 'latching' (On/Off) then start the function label with a asterisk (\*). The most common example of this is the Horn/Whistle which is commonly on F2.

*Examples:*  
ROSTER ( 3,"Eng 3", "F0/F1/\*F2/\*F3/F4/F5/F6/F7/Mute/F9//") // Address 3, Eng 3, Function keys F0-F10 ROSTER(1224,"PE 1224","") // Motor Only Decoder ROSTER(1225,"PE 1225","Lights/Bell/\*Whistle/\*Short Whistle/Steam/On-Time/FX6 Bell Whistle/Dim Light/Mute") ROSTER(4468,"LNER 4468","//Snd On/\*Whistle/\*Whistle2/Brake/F5 Drain/Coal Shvl/Guard-Squeal/Loaded/Coastng/Injector/Shunt-Door ~Opn-Cls/Couplng/BrakeVlv/Sfty Vlv/Shunting/BrkSql Off/No Momentm/Aux3/Fade Out/F22 Res/F23/Res//Aux 5/Aux6/Aux7/Aux 8")

#### `POM( cv, value )` - Program CV value on main

Program CV value on main, must be proceeded by setting the loco ID with `SETLOCO( loco )`

#### `IFLOCO( loco )` - perform commands if the specified loco ID is defined for this sequence

If the specified loco ID is defined for this sequence, perform the defined activities

*Parameters:*

- **loco** - DCC Address of the loco to test against

**For example: (click to show)**

> ``` cpp
> // A defined automation sequence that will do activities only if loco ID 123 is in use
> AUTOSTART AUTOMATION(1, "Do stuff for loco 123")
>   IFLOCO(123)
>     // Define activities here e.g. blow horn or whistle
>   ENDIF
>   DONE
> ```

#### `XFWD( loco, speed )` - Sends DCC speed to a loco in forward direction

Sends DCC speed to an abritary loco in forward direction

*Parameters:*

- **loco** - DCC address of your loco
- **speed** - DCC speed (0-127)
  - 2-127 = speed 1-126
  - 0 = stop
  - 1 = Estop

#### `XREV( loco, speed )` - Sends DCC speed to a loco in reverse direction

Sends DCC speed to an abritary loco in reverse direction

*Parameters:*

- **loco** - DCC address of your loco
- **speed** - DCC speed (0-127)
  - 2-127 = speed 1-126
  - 0 = stop
  - 1 = Estop

#### `XFON( cab, func )`\` - Send DCC function ON to specific cab

Send DCC function ON to specific cab (e.g. coach lights) *Not for Loco use - use FON instead!*

*Parameters:*

- **cab** - DCC address of your loco
- **func** - Function number (0-31)

#### `XFOFF( cab, func )` - Send DCC function OFF to specific cab

Send DCC function OFF to specific cab (e.g. coach lights) Not for Loco use - use FON instead!

*Parameters:*

- **cab** - DCC address of your loco
- **func** - Function number (0-31)

#### `XFTOGGLE( loco, func )` - Toggle DCC function on specific loco

Toggle DCC function on loco with the specified DCC address.

*Parameters:*

- **loco** - DCC address of your loco
- **func** - Function number (0-31)

#### `XPOM( loco, cv, value )` - Write CV value to specified loco on main

Write CV value to specified loco on main. (PoM)

*Parameters:*

- **loco** - DCC address of your loco
- **cv** - cv to change
- **value** - value to write

#### `XSAVE_SPEED( loco )` - Saves the current speed of a loco

Saves the current speed of a loco.

*Parameters:*

- **loco** - DCC address of your loco

#### `XRESTORE_SPEED( loco )` - Restores the saved speed of a loco

Restores the saved speed of a loco

*Parameters:*

- **loco** - DCC address of your loco

#### `FORGET` - Forget the loco in the running automation/sequence

Forget the loco in the running automation/sequence

*Parameters:*

- none

------------------------------------------------------------------------

### TrackManager Control

#### `SET_TRACK( track, mode )` - Configures the mode of a track

Configures the mode of the selected track, refer also to Index

*Parameters:*

- **track** - - The track to configure, valid options are A to H
- **mode** - - The mode to set the track to, valid options for DCC are:
  - `MAIN` or
  - `MAIN_INV` or
  - `MAIN_AUTO` or
  - `PROG`, and valid options for DC are:
  - `DC` or
  - `DC_INV` or
  - `DCX` (same as DC_INV). If a track is unused, it can be set to:
  - `NONE`, If the EX‑CommandStation is confgured as a Booster (ESP32 Microcontrollers only), it can be set to:
  - `BOOST` or
  - `BOOST_INV` or
  - `BOOST_AUTO`.

| Option  | \_INV | \_AUTO | Notes |
|---------|-------|--------|-------|
| `MAIN`  | Yes     | Yes      | Yes[^1] |
| `PROG`  | Yes     |        |       |
| `DC`    | Yes     | Yes[^2]  | Yes     |
| `BOOST` | Yes     | Yes      | Yes     |
| `EXT`   | Yes     |        |       |
| `NONE`  | Yes     |        |       |

When setting at track mode to either `DC` or `DC_INV` / `DCX`, you must use the `SETLOCO( loco )` command first to specify the loco ID that will be used for the DC track then SET_TRACK()

**For example: (click to show)**

> ``` cpp
> // Set both tracks A and B to be main DCC tracks
> AUTOSTART
> SET_TRACK(A, MAIN)
> SET_TRACK(B, MAIN)
> DONE
>
> // Set track A to be a DC track with loco ID 1, and track B to be a DCC programming track
> AUTOSTART
> SETLOCO(1) SET_TRACK(A, DC)
> SET_TRACK(B, PROG)
> DONE
> ```

#### `SET_POWER( track, ON/OFF )` - Enable/Disable power on a track

Configures the power setting of the selected track, refer also to Index

*Parameters:*

- **track** - - The track to configure, valid options are A to H
- **ON/OFF** - - Turn the power ON or OFF for this track

**For example: (click to show)**

> ``` cpp
> // Set track A to be a DC track with loco ID 1 and power on, and track B to be a DCC programming track
> AUTOSTART
> SETLOCO(1) SET_TRACK(A, DC)
> SET_TRACK(B, PROG)
> SET_POWER(A, ON)
> DONE
> ```

#### `SETFREQ( frequency )` - Enable a specific frequency

`DC` or `DC_INV` / `DCX` track settings only.

Configures the frequency setting of the selected loco.

The settings achievable vary slightly depending upon the processor running the EX‑CommandStation but broadly follow the following:

*Parameters:*

- **frequency** - - The frequency to set for the current loco
\>valid options are:

- **0** - Default - low frequency 131Hz
- **1** - Mid frequency - 490Hz
- **2** - High frequency - 3400Hz
- **3** - Supersonic - 62500Hz

Trial and error will be needed for specific locos that do not respond well to the defaults (low) frequency setting.

**For example: (click to show)**

> ``` cpp
> // Set track A to be a DC track with loco ID 1 and power on, and track B to be a DCC programming track
> ROUTE(504, "DC loco 10 to DCFREQ 1")
>   SETLOCO(10) SETFREQ(1)
> DONE
> ROUTE(505, "DC loco 10 to DCFREQ 2")
>   SETLOCO(10) SETFREQ(2)
> DONE
> ROUTE(506, "DC loco 10 to DCFREQ 3")
>   SETLOCO(10) SETFREQ(3)
> DONE
> ```

------------------------------------------------------------------------

### Controlling Overload/Shorts

#### `ONOVERLOAD( track )` - Event handler for when an Overload occurs

> Creates an event handler for the selected track, to be executed when the MotorDriver routines detect and overload. Refer also to Index

*Parameters:*

- **track** - - The track to configure, valid options are A to H

#### `AFTEROVERLOAD( track )` - Event handler for when an Overload clears

Creates a complementary event handler for the selected track, to be executed when the MotorDriver routines indicate the overload is cleared. Refer also to Index

Note: AFTEROVERLOAD is only relevant when used within and ONOVERLOAD.... DONE structure.

*Parameters:*

- **track** - - The track to configure, valid options are A to H

The power calculation routines within DCC-EX will check for shorts and overloads and will change the state of the power produced by the MotorDriver board to protect both it and locos from damage. This is usually evident by the LED's on the MotorDriver board flashing. However some users may wish to see some physical notification of these events. This can now be achieved with EXRAIL and the ONOVERLOAD event.

**For example: (click to show)**

> This first example shows a warning message to an attached screen with an LED being illuminated to warn the user of the overload. Once the overload is cleared the AFTEROVERLOAD code is run automatically.
>
> ``` cpp
> ONOVERLOAD(A)       // the EXRAIL statement to control the event.
>   SCREEN(2,0, "OVERLOAD ON TRACK A")     // A message to the second screen
>   PRINT("Overload Detected on Track A")   // Message to system moniter
>   SET(27)                                 // Turn on an LED perhaps
>   AFTEROVERLOAD(A)
>       SCREEN(2,0, "RESTORE A POWER ON")
>       PRINT("Overload Cleared on A - Power Restored")
>       RESET(27)                           // Turn off the LED
>       DELAY(2000)
>       SCREEN(2,0, "                  ")   // Clear the screen message
> DONE
> ```
>
> If the user wishes to turn off power whilst he/she investigates the problem, then this can be achieved using the second example below. POWEROFF can be used, but this will turn off power to all tracks. Power to the track with the problem can be turned off with a TrackManager command. However in order to execute the AFTEROVERLOAD routine it is necessary to have a reset routine.
>
> ``` cpp
> // This is the event triggered by an overload.  AFTEROVERLOAD cannot be triggered whilst power is OFF.
> ONOVERLOAD(A)
>   SCREEN(2,0, "OVERLOAD A POWEROFF")
>   PRINT("Overload Detected on A - Turn Off Power")
>   SET_TRACK(A, NONE)   // Unsets the TrackManager assignment and turns off power.
>   SET(27)              // Light the LED
>   AFTEROVERLOAD(A)
>       SCREEN(2,0, "RESTORE A POWER ON")
>       PRINT("Overload Cleared on A - Power Restored")
>       RESET(27)
>       DELAY(2000)
>       SCREEN(2,0, "                  ")
> DONE
>
> // The following turns the power on and allows the AFTEROVERLOAD to run
> // This could also be achieved with a physical button and AFTER(pin) in place of ROUTE()
> ROUTE(12,"Reset A")
>   SCREEN(2,0,"                  ")
>   SET_TRACK(A, MAIN)
>   POWERON
> DONE
> ```

------------------------------------------------------------------------

### Virtual Block Control

#### `RESERVE( block_id )` - Reserve a block

Reserve a block (0-255). If already reserved, current loco will STOP and sequence waits for block to become free

*Parameters:*

- **block_id** - Block to reserve (0-255)

#### `FREE( block_id )` - Free block

Free previously reserved block.

*Parameters:*

- **block_id** - Block to free (0-255)

#### `IFRESERVE( block_id )` - Execute commands if block is NOT reserved

If block is NOT reserved, reserve it and run commands in the IF block. Otherwise, skip to matching ENDIF

*Parameters:*

- **block_id** - Block to test (0-255)

------------------------------------------------------------------------

## System

### Communication and Display Functions

#### `LCD( row, "msg" )` - Write message on LCD/OLED

Write message on LCD/OLED, if fitted.

*Parameters:*

- **row** - row of the LED/OLD to write the message
- **msg** - message to write

#### `SCREEN( display, row, "msg" )` - Writes a message to a display

Writes a message to the specified display on the specified row.

*Parameters:*

- **display** - which display to write to ???
- **row** - row of the LED/OLD to write the message
- **msg** - message to write

#### `BROADCAST( "msg" )` - Broadcast to all throttles/JMRI on serial and WiFi

Broadcast to all throttles/JMRI on serial and WiFi

*Parameters:*

- **msg** - message to broadcast

#### `PRINT( "msg" )` - Print diagnostic message to Serial Monitor

Write a diagnostic message to the Serial Monitor.

*Parameters:*

- **msg** - message to write

#### `SERIAL( "msg" )` - Writes direct to Serial

Writes direct to Serial (Serial0/USB)

*Parameters:*

- **msg** - message to write

#### `SERIAL1( "msg" )` - Writes direct to Serial1

Writes direct to Serial1.

*Parameters:*

- **msg** - message to write

#### `SERIAL2( "msg" )` - Writes direct to Serial2

Writes direct to Serial2.

*Parameters:*

- **msg** - message to write

#### `SERIAL3( "msg" )` - Writes direct to Serial3

Writes direct to Serial3.

*Parameters:*

- **msg** - message to write

#### `SERIAL4( "msg" )` - Writes direct to Serial4

Writes direct to Serial4.

*Parameters:*

- **msg** - message to write

#### `SERIAL5( "msg" )` - Writes direct to Serial5

Writes direct to Serial5.

*Parameters:*

- **msg** - message to write

#### `SERIAL6( "msg" )` - Writes direct to Serial6

Writes direct to Serial6.

*Parameters:*

- **msg** - message to write

#### `WITHROTTLE( "msg" )` - Writes a message to WiThrottle clients

Writes a message to WiThrottle clients (alias of `PRINT`)

A WiThrottle controller will receive `Hmmsg`.

*Parameters:*

- **msg** - message to write

#### `MESSAGE( "msg" )` - Writes a message to all clients<span id="exrail_message"></span>

Writes a message to all serial throttles and all WiThrottle Clients.

A DCC-EX throttle will receive a broadcast `<m "text">`, and a WiThrottle throttle will receive `Hmtext`.

*Parameters:*

- **msg** - message to write

------------------------------------------------------------------------

### EX-CommandStation Functions

#### `POWERON` - Power on track and UNJOIN

Turn the track power on and UNJOIN if currently joined.

*Parameters:*

- none

#### `POWEROFF` - Power off track

Turn the track power off.

*Parameters:*

- none

#### `JOIN` - Join PROG and MAIN track outputs

Join PROG and MAIN track outputs to send the same MAIN DCC signal.

*Parameters:*

- none

#### `UNJOIN` - Disconnect prog track from main

Disconnect PROG output from MAIN output.

*Parameters:*

- none

#### `ENDEXRAIL` - Deprecated - Do not use

Deprecated - Do not use

#### `EXRAIL` - Deprecated - Do not use

Deprecated - Do not use

#### `KILLALL` - Kills all running EXRAIL activities

Kills all running EXRAIL activities

*Parameters:*

- none

#### `PARSE( "msg" )` - Allows parsing of a DCC-EX API command via myAutomation.h

Allows parsing of a DCC-EX API command via myAutomation.h. This allows you to include Native DCC-EX Cammands in myAutomation.h where there is no equivalent EXRAIL command.

*Parameters:*

- **msg** - message to parse

#### `DISABLE_PROG` - Disable programming to save RAM/Flash

Disable programming to save RAM/Flash.

*Parameters:*

- none

#### `IO_NO_HAL` - Reduce FLASH footprint when HAL features not required

To reduce FLASH footprint when HAL features not required.

Note: The HAL is disabled by default on Nano and Uno platforms, because of limited flash space.

*Parameters:*

- none

------------------------------------------------------------------------

### Layout Command Control (LCC)

The following commands have been introduced to support Layout Command Control (LCC) / CBUS.

#### `ONLCC(sender, eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - ONLCC

</div>

*Parameters:*

- **sender** - TBA
- **eventid** - TBA

#### `LCC(eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - LCC

</div>

*Parameters:*

- **eventid** - TBA

#### `LCCX(senderid,eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - LCCX

</div>

*Parameters:*

- **senderid** - TBA
- **eventid** - TBA

#### `ACON(eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - ACON

</div>

*Parameters:*

- **eventid** - TBA

#### `ACOF(eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - ACOF

</div>

*Parameters:*

- **eventid** - TBA

#### `ONACON(eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - OACON

</div>

*Parameters:*

- **eventid** - TBA

#### `ONACOF(eventid)` - TBA

<div class="todo">

LOW - EXRAIL doco - ONACOF

</div>

*Parameters:*

- **eventid** - TBA

------------------------------------------------------------------------

## Advanced (Engineers only)

### Caution required!

Any commands in this section are intended for level users that have advanced knowledge of how EXRAIL works, and likely some understanding of C++ coding as well.

If you are unsure on the impacts using anything in this section may have, please reach out to the DCC-EX team via the methods listed on our Contact us page.

#### `STEALTH( code )` - include some C++ code in a ROUTE/SEQUENCE

**SERIOUS ENGINEERS and ADVANCED C++ USERS ONLY**

Permits a certain level of C++ code to be embedded as a single step in an EXRAIL sequence.

Please use this option with great care. If in doubt ask for assistance.

Syntax:  
STEALTH( .. C++ code ..)

**For example: (click to show)**

> ``` cpp
> // run a routine to free any LATCHES that are left on.
> SEQUENCE(999)
>       STEALTH(  //RESET ANY LATCHES WE TURNED ON
>       for (int i = 1; i <= 255; i++) {
>         if (getFlag(i,LATCH_FLAG)) {    //IF LATCH ON
>         setFlag(i,0,LATCH_FLAG);      //RESET LATCH
>           }
>         }  
>       )
> RETURN
>
> then
> CALL(999) inside your onthrow/onclose sections.
> ```

#### `STEALTH_GLOBAL( code )`

**SERIOUS ENGINEERS and ADVANCED C++ USERS ONLY**

Inserts code such as static variables and functions that may be utilized by multiple `STEALTH` operations.

Please use this option with great care, and you will need to be an advanced C++ user to make use of this command. If in doubt ask for assistance.

[^1]: Deprecated alias of `AUTO` but only when preceded by a separate `MAIN` command.

[^2]: With special alias of `DCX` for `DC_INV`


\newpage

# Controlling EXRAIL by Time

## Time Command

The additional commands added to EXRAIL allow events to be controlled by the clock. The basic form of the new clock command is:

``` cpp
ONCLOCKTIME( hour, mins)
```

This is an event based command and will activate a sequence of commands until a DONE command is reached. An example of how this might be used is as follows:

``` cpp
ONCLOCKTIME(06,15) 
  SETLOCO(7309) 
  ....
  .... Do some stuff
  ....
  DONE
```

Sequences built this way can only be run via a clock command. If it was required to have a sequence that could be run for Engine Driver for example, then this could be operated by a clock command as below:

``` cpp
ONCLOCKTIME(06,15) SENDLOCO(7309,10) DONE

SEQUENCE(10)
    PRINT("Go Somewhere")
    FON(1)
    DELAY(500)
    FWD(50)
    DELAY(20000)
    FWD(0)
    DELAY(2000)
    FON(4)
    DELAY(3000)
    FOFF(4)
    PRINT("You have arrived")
    FOFF(1)
DONE
```

This event could either be run by the clock or could be selected at will from Engine Driver. To stop the EX‑CommandStation from running timed commands to switch to manual running, simply pause the clock.

## Repeating Time events

Some users may wish to repeat an event at the same time every hour - e.g. to play a recording of a clock chime. It is possible to achieve this as follows:

``` cpp
ONCLOCKMINS( mins )
```

This is an event based command that will activate at the same time each hour as in the example below:

``` cpp
ONCLOCKMINS(15) 

  SET(1000)             // Start playing first MP3 file
  AT(-1000)             // Wait for playing to finish

  RESET(1000)           // Stop player 
  ....
  .... Do some other stuff
  ....
  DONE
```

The sequence above will repeat at 15 munites past the hour per FastClock time. It would also be possible to make these routines be selectable from Engine Driver by configuring them as follows:

> ``` cpp
> ONCLOCKMINS(15) FOLLOW(10) DONE
>
> SEQUENCE(10)
>   SET(1000)             // Start playing first MP3 file
>   AT(-1000)             // Wait for playing to finish
>
>   RESET(1000)           // Stop player 
>   ....
>   .... Do some other stuff
>   ....
> DONE
> ```

In that way the Sequence 10 can either be run by the clock, or if the clock is not running may be selected manually from Engine Driver.

NB: See the following page for details on running sound files.

Hal config

## Testing Timed Sequences

If one is testing out a sequence using a timed command it can be done quickly without using the clock. The following command can be entered from the System Monitor:

> ``` cpp
> <JC mmmm ss> 
> ```

where mmmm is the time in minutes since midnight. This is (hours \* 60) + mins and is how the time is held within EX‑CommandStation. So for the time in the example above (6:15) the following:

> ``` cpp
> <JC 375 4>
> ```

would execute the command immediately (4 being the perceived speed factor i.e. 1 minutes every 15 seconds). The EX‑CommandStation would respond with:

> ``` cpp
> <jC 375>
> ```

And would then display any messages generated by the SEQUENCE 10.

The final command available is:

> ``` cpp
> <JC>
> ```

which requests the latest time from EX‑CommandStation which responds with:

> ``` cpp
> <jC 375>
> ```


\newpage

# Diagnostics `<D>` Command

These commands either enable diagnostics or allow settings to be changed. There are a number of diagnostic facilities under the `<D>` command, most are harmless but caution is advised.

**The** `<D>` **commands are intended for diagnostics only which means that their behaviour can change from one release to another without warning**

These commands can be entered directly via the USB serial console or through a WiFi connection to the command station with a tool such as Telnet or Putty. JMRI includes the DCC++ traffic monitor which lets you insert serial DCC-EX Native Commands as well. (links required)

## Speed Step Configuration

`<D SPEED28|SPEED128>` By default, the Command Station sends speed commands in 128 steps. You can change to 28 speed steps and back again with this command. If speed steps are set to 28, you can still use 128 speed step locos, they will just have a resolution of 28 steps also instead of 128.

`<D CABS>` Lists the locomotives which the command station is currently managing.

`<D RAM>` Displays the free RAM on your Arduino.

## The following commands turn ON(1) or OFF(0) various diagnostic traces

`<D ACK ON|OFF>` trace DCC ACK processing when reading/writing on the prog track. See Diagnostic d ack command.

`<D CMD ON|OFF>` trace received commands.

`<D WIFI ON|OFF>` trace WiFi protocol AT command conversation between Arduino and WiFi hardware.

`<D ETHERNET ON|OFF>` trace Ethernet conversation between Arduino and Ethernet hardware.

`<D WIT ON|OFF>` trace WiThrottle protocol conversation of Engine Driver (or other WiThrottle device).

`<D HAL SHOW>` display information about configured HAL devices (servo controllers, GPIO Extenders) including address and pins used

## The following commands might help in exceptional circumstances

`<D PROGBOOST>` When the programming track is switched on with `<1>` or `<1 PROG>` it will normally be restricted to 250mA according to NMRA standards. Some loco decoders require more than this, especially sound versions. `<D PROGBOOST>` temporarily removes this limit to allow the decoder more power. The normal limit will be re-imposed when the programming track is switched off with `<0>` or `<0 PROG>`.


\newpage

# Diagnostics `<D ACK>` Command

- reference/tools/diagnostic-d-ack-command:- Turn on Loco acknowledgement diagnostics
- reference/tools/diagnostic-d-ack-command:- Override ACK processing mA pulse size
- reference/tools/diagnostic-d-ack-command:- Override ACK processing minimum pulse width
- reference/tools/diagnostic-d-ack-command:- Override ACK processing max pulse width
- reference/tools/diagnostic-d-ack-command:- Override 250mA prog track limit while idle.

## \<D ACK ON\>

If you encounter problems with ACKs from the Decoder (Reading or Writing CVs) and you want help, the DCC-EX support team will ask you to provide a log. This is a very simple diagnostic test to provide us with the proper information. With your loco on the PROG track, and using a Serial Monitor like the one in the Arduino IDE, enter each of these two commands followed by pressing "send":

`<D ACK ON>`  
`<R>`

This will turn ACK diagnostics ON and then try to read the appropriate CVs to determine your loco address. If you don't see your loco address at the end of the report (it could be incorrect or \<r -1\>), send us the log (see below for an example), and we can help you diagnose the problem.

### More Detail

When the ACK processing on the prog track does not work as expected, you may want to use the `<D ACK ON>` command in a serial command window. This is an example how to read CV8 with diagnostics on. You enter the first 2 lines, `<D ACK ON>` followed by `send`, then `<R 8 1 1>` followed by `send`. DCC-EX does not echo what you write, but your serial command window may. With diag on you get the extra 11 lines of output compared to if you just entered the command with diagnostics off. The last line is the answer, CV8=145:

``` none
<D ACK ON>
<R 8 1 1>
ACK-BASELINE 33/98mA
V0 cv=8 bit=7 NO-ACK after 143mS max=12/35mA pulse=0uS
V1 cv=8 bit=7 ACK-OK after 34mS max=646/1931mA pulse=6852uS
V0 cv=8 bit=6 ACK-OK after 34mS max=583/1743mA pulse=6844uS
V0 cv=8 bit=5 ACK-OK after 34mS max=646/1931mA pulse=6800uS
V0 cv=8 bit=4 NO-ACK after 144mS max=12/35mA pulse=0uS
V0 cv=8 bit=3 ACK-OK after 34mS max=563/1683mA pulse=6792uS
V0 cv=8 bit=2 ACK-OK after 34mS max=647/1934mA pulse=6800uS
V0 cv=8 bit=1 ACK-OK after 34mS max=573/1713mA pulse=6844uS
V0 cv=8 bit=0 NO-ACK after 145mS max=14/41mA pulse=0uS
VB cv=8 value=145 ACK-OK after 34mS max=639/1910mA pulse=6848uS
Callback(145)
<r1|1|8 145>
```

Your output may show different formatting with respect to linefeeds. Here the decoder reports that bits 7, 4 and 0 are **NOT** Zero. That gives the value of `10010001 = 145` which is the manufacturer ID for Zimo. That value is checked in the `VB` line. For a successful read, the result of the verify bit and verify byte commands have to match, otherwise the value can not be read. If you have problems reading decoders, you can compare the received values with the expected values. The format is:

``` none
OPERATION cv=n bit=b NO-ACK/OK after WAITTIME mS max=INTERNALVAL / CURRENT mA pulse= PULSELENGTH µS
```

The CURRENT should be over 60mA for a successful ACK and the length should be 6000µS +-1000µS but because of Decoder variations from the standard, DCC-EX has some extra pulse length margin.

In this example, we are checking CV 8, which is the manufacturer ID for your decoder. We then check each of the 8 "bits" in the "byte" that holds the value in that CV.

The first test, `ACK-BASELINE` gets a baseline reading of the current on your programming track with the loco just sitting there.

Since most bits will be 0, we check that first to save time. `V0` means `Verify zero`. If do not get a zero, we then try to verify a 1 - `V1` means "Verify one". If we don't get either, we display an error. A bit must be either a 0 or a 1 so the test will fail, but the data returned can help us see why.

If we succeed on the first bit, we check each of the remaining 7 bits. `NO-ACK` means we did not see the bit value we were testing for, `ACK-OK` tells us we received an ACK. After each bit test, we show how long it took to receive the ACK (or the timeout value if we detected none), the Arduino raw pin reading being sent by your Motor Driver (also referred to as a 'Motor Controller', 'Motor Shield' or 'Motor Board')'s current sense circuit, and what that translates to in milliAmps. Finally, we report the duration of the ACK Pulse, if detected.

We do one final test at the end to `Verify Byte`, you see that as `VB`. This does a double-check to see if the byte contains what we found by checking it one bit at a time. The must match for a successful read.

Other than when using the "decoder address test", `<R>` with no parameters, you need to enter CV read commands with all 3 parameters. The format is `<R CV x y>` where R stands for read and CV is the CV number you want to check. The X and Y values can be anything, but must be entered. They are an advanced feature for programmers whose software can work with DCC-EX (like JMRI). So you would enter `<R 8 55 55>` or `R 8 1 1>` to try and read CV 8. The response is `<r CV x y>` where "x" and "y" are whatever numbers you entered after the CV value.

To turn off the ack diagnostics use any parameter that is not "ON" or "LIMIT".

``` cpp
<D ACK NOPE>, <D ACK OFF>, etc.
```

Diag messages off.

## \<D ACK LIMIT mA\>

The Ack current limit is set according to the DCC standard(s) of 60mA. Most decoders send a quick back and forth current pulse to the motor to generate this ACK. However, some modern motors (N and Z scales) may not be able to draw that amount of current. You can adjust down this limit. Or, if for some reasons your acks seem to be too "trigger happy" you can make it less sensitive by raising this limit.

``` cpp
<D ACK LIMIT 30>
```

would set the ack limit to 30mA (more sensitive).

``` cpp
<D ACK LIMIT 100>
```

would set the limit to 100mA (less sensitive).

The custom ack limit will be effective until you restart the Command Station (it will not "stick" in EEPROM). If you wish to permanently set the ACK LIMIT, you may enter it as a command in the mySetup.h file.

## \<D ACK MIN µS\><span id="D ACK MIN"></span>

## \<D ACK MAX µS\>

The NMRA specifies that the ACK pulse duration should be 6 milliseconds, which is 6000 microseconds (µS), give or take 1000 µS. That means the minimum pulse duration is 5000 µS and the maximum is 7000 µS. There are many poorly designed decoders in existence so DCC-EX extends this range from 4000 to 8500 µS. If you have any decoders that still do not function within this range, you can adjust the ACK MIN and ACK MAX parameters.

Example 1: You use the \<D ACK ON\> and \<R\> commands described above to generate a test log from a loco on your programming track. You see that there are ACK pulses but that their durations are less than 4000 microseconds. The log shows the shortest one was 3450. You might then choose a setting a little bit lower than your lowest reading:

``` cpp
<D ACK MIN 3300>
```

Example 2: You use the \<D ACK ON\> and \<R\> commands described above to generate a test log from a loco on your programming track. You see that some of the ACK pulses are longer than 8500 µS. The longest one is 10350 µS. Pick a setting a little bit higher than your highest reading like this:

``` cpp
<D ACK MAX 10500>
```

## \<D PROGBOOST\>

`<D PROGBOOST>` - Override 250mA prog track limit while idle.

When the programming track is switched on with `<1>` or `<1 PROG>` it will normally be restricted to 250mA according to NMRA standards. Some loco decoders require more than this, especially sound versions. `<D PROGBOOST>` temporarily removes this limit to allow the decoder to use more power. The normal limit will be re-imposed when the programming track is switched off with `<0>` or `<0 PROG>` or the Command Station is reset.

## Making the Changes Permanent

To make these settings permanent, you can create a Startup Configuration by adding or editing an existing *mySetup.h*. You simply add the appropriate commands in the correct format and upload the Command Station software again. Click on the link in this paragraph for detailed instructions.

