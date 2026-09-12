---
name: serial-recovery
description: Troubleshoot and recover unresponsive Flight Controller serial links across Windows, macOS, and Linux (stuck CLI modes, busy ports, DFU bootloader, missing device nodes). Use when connection fails, prompt times out, or serial port is unresponsive.
---

# Serial Recovery & Troubleshooting Skill

Use this skill when diagnosing Flight Controller connection failures or unresponsive serial links.

---

## Quick Diagnostic Matrix

| Error / Symptom | Root Cause | Resolution |
| :--- | :--- | :--- |
| **CLI prompt not received / Buffer: "#"** | FC is stuck in CLI mode from an un-exited session | Physical USB replug |
| **Device or resource busy** | Port locked by another process (Configurator, terminal) | Close holding tab/app or run `fuser -k <port>` |
| **No such file or directory** | Re-enumeration assigned a new COM/tty path | Run `python tools/fc_check.py` to re-scan |
| **Zero bytes, no prompt response** | Wrong line ending sent on CLI entry | Use `python tools/bf_cli.py` (sends bare `#`) |
| **USB VID:PID 0483:df11** | FC is stuck in DFU bootloader mode | Replug USB without pressing boot button |
| **MSP times out, CLI works fine** | FC is currently in CLI mode | Run `python tools/bf_cli.py "status"` or replug USB |

---

## 1. Stuck in CLI Mode

### Symptom
MSP requests time out permanently, and CLI attempts fail with `"CLI prompt not received"`. `status` shows `CLI` under `Arming disable flags`.

### Cause
The FC entered CLI mode during a previous session and was not cleanly exited (`exit noreboot` or `save`). While in CLI mode, Betaflight disables MSP telemetry processing and rejects new CLI entry requests.

### Fix
Unplug and replug the USB cable. Host-side port resets do **not** clear firmware CLI state.

---

## 2. Port Locked by Another Process

### Symptom
`SerialException: Could not open port / Permission denied / Device busy`.

### Cause
Another application (e.g. Chrome Betaflight Configurator tab, serial monitor) holds an active lock on the COM/tty port.

### Fix
- **Linux/macOS**:
  ```bash
  fuser /dev/ttyACM*
  lsof /dev/ttyACM*
  ```
  Close the process ID (PID) indicated.
- **Windows**:
  Close Betaflight Configurator or PuTTY/TeraTerm instances in Task Manager.

---

## 3. FC Re-enumeration & Path Changes

On every USB replug, the OS may assign a different port name (`COM3` -> `COM4` on Windows, `/dev/ttyACM0` -> `/dev/ttyACM1` on Linux, `/dev/tty.usbmodem14101` on macOS).

Always use auto-detection:
```bash
python tools/fc_check.py
```
`tools/bf_cli.py` and `tools/bf_msp.py` perform this auto-detection automatically.
