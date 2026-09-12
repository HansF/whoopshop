---
title: "Betaflight CLI Serial Protocol Guide"
date: 2026-09-12T10:00:00Z
draft: false
---

# Betaflight CLI Serial Protocol Guide

This guide details how **WhoopShop** tools communicate directly with Betaflight Flight Controllers over USB serial without requiring third-party GUI applications or external MCP servers.

---

## 1. The Serial Handshake Protocol

Betaflight CLI mode is entered over virtual COM port (VCP) at 115200 baud.

### The Bare `#` Handshake Rule
To enter CLI mode, the host software **must send a single bare `#` character without any trailing newline or carriage return (`\r` or `\n`)**.

- Sending `#` (bare) -> FC returns `Entering CLI Mode, type 'exit' to reboot...` followed by prompt `# `.
- Sending `#\r\n` -> FC interprets this as an empty command and remains silent.

`tools/bf_cli.py` handles this handshake automatically:

```python
ser.write(b"#") # Bare byte handshake
ser.flush()
```

---

## 2. CLI Exit Discipline

Betaflight only exits CLI mode upon receiving an explicit exit command:

1. `exit noreboot`: Drops out of CLI mode without restarting the flight controller. Returns the board to normal flight mode and enables MSP (MultiWii Serial Protocol) binary telemetry.
2. `save`: Writes modified settings from RAM to EEPROM flash, causing the board to reboot.

> [!WARNING]
> **Stuck in CLI Mode**: If a serial script crashes or disconnects without sending `exit` or `save`, the FC remains locked in CLI mode. While in CLI mode, **all MSP binary requests will time out** and subsequent CLI attempts will fail with `"CLI prompt not received"`.
> 
> **Recovery**: Unplug and replug the USB cable to reset the flight controller firmware state.

---

## 3. Tool Usage Examples

```bash
# Query hardware status and arming disable flags
python tools/bf_cli.py "status"

# Fetch full CLI configuration diff
python tools/bf_cli.py "diff"

# Update craft name and save to EEPROM (reboots FC)
python tools/bf_cli.py --save "set craft_name = MY_WHOOP"
```
