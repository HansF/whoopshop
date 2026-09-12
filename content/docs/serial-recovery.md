---
title: "Serial Recovery & Troubleshooting Guide"
date: 2026-09-12T10:00:00Z
draft: false
---

# Serial Recovery & Troubleshooting Guide

This guide covers troubleshooting procedures for unresponsive Flight Controller serial links across Windows, macOS, and Linux.

---

## Diagnostic Matrix

| Error Text / Symptom | Primary Cause | Resolution |
| :--- | :--- | :--- |
| `Error: CLI prompt not received... Buffer: "#"` | FC left locked in CLI mode | Physical USB replug |
| `Device or resource busy / Permission denied` | Port held by another application | Run `fuser` / close holding tab |
| `No such file or directory` | Port re-enumerated to new device path | Run `python tools/fc_check.py` |
| Zero bytes returned, no prompt | Invalid line ending on CLI entry | Use `python tools/bf_cli.py` (sends bare `#`) |
| USB VID:PID `0483:df11` | FC in DFU bootloader mode | Replug USB without pressing boot button |

---

## 1. Stuck in CLI Mode

If a serial tool disconnects without calling `exit noreboot` or `save`, the FC remains in CLI mode. While in CLI mode, binary MSP reads fail and subsequent CLI attempts stall.

**Fix**: Unplug and replug the USB cable to reset the flight controller firmware.

---

## 2. Port Locked by Another Process

On Linux and macOS, only one application can hold a serial device node at a time. If Betaflight Configurator (or a browser WebSerial tab) is open, CLI scripts will fail with `Device or resource busy`.

**Fix (Linux/macOS)**:
```bash
fuser /dev/ttyACM*
```
Close the indicated process ID (PID).
