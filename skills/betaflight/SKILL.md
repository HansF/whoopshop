---
name: betaflight
description: Interact with Betaflight flight controllers over USB serial using native Python tools (CLI diffs, settings updates, live MSP telemetry). Use when reading FC status, configuring PIDs/rates/OSD, checking motor protocols, or reading live RC channel values.
---

# Betaflight FC Interaction Skill

Use this skill to communicate directly with connected Betaflight Flight Controllers across Windows, macOS, and Linux without external MCP dependencies.

## 1. Verify Connection & Environment

Before attempting CLI or MSP commands, detect the connected Flight Controller:

```bash
python tools/fc_check.py
```

This identifies:
- Connected serial device path (`COMx`, `/dev/ttyACM*`, `/dev/tty.usbmodem*`).
- USB serial numbers and whether the device is an FC or an EdgeTX radio handset.
- Whether the port is free or busy.

---

## 2. CLI Operations (`tools/bf_cli.py`)

### Safe Read Operations (Non-destructive)

Read system status, current CLI diff, or specific configuration variables:

```bash
# Read hardware status, arming flags, and CPU load
python tools/bf_cli.py "status"

# Fetch full non-default configuration diff
python tools/bf_cli.py "diff"

# Inspect specific variables
python tools/bf_cli.py "get osd_profile" "get blackbox_sample_rate"
```

### Applying Configuration Changes

> [!WARNING]
> Always ask the user to **REMOVE ALL PROPELLERS** before applying settings that affect motor protocols, DShot, or arming behavior.

To save changes to EEPROM (reboots FC):

```bash
python tools/bf_cli.py --save "set craft_name = TINYWHOOP" "set osd_vbat_pos = 2433"
```

### Essential CLI Discipline Rules
1. **Bare `#` Handshake**: The script handles sending a bare `#` to trigger CLI mode.
2. **Auto-Exit**: The tool guarantees `exit noreboot` (or `save`) execution.
3. **If CLI stalls**: If the prompt times out, the FC may be stuck in CLI mode from an interrupted session. Unplug and replug the USB cable.

---

## 3. Live Telemetry & MSP Reads (`tools/bf_msp.py`)

Use MSP (MultiWii Serial Protocol) to observe live RC channel data and FC telemetry without putting the board into CLI mode:

```bash
# Single MSP status and RC channel snapshot
python tools/bf_msp.py

# Record 10 continuous samples at 0.2s intervals
python tools/bf_msp.py --samples 10 --interval 0.2
```

> [!NOTE]
> The Flight Controller must **not** be in CLI mode when running MSP requests. If MSP times out, run `python tools/bf_cli.py "status"` to return the board to normal flight mode, or replug USB.
