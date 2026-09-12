#!/usr/bin/env python3
"""Execute Betaflight CLI commands over USB serial across Windows, macOS, and Linux.

Usage:
    python tools/bf_cli.py "status" "get osd_profile"
    python tools/bf_cli.py --save "set craft_name = MY_WHOOP"
    python tools/bf_cli.py --port COM3 "status"
    python tools/bf_cli.py --serial 3057397C3235 "diff"

Guarantees CLI exit discipline (exit noreboot or save) so the Flight Controller
never remains locked in CLI mode.
"""
import argparse
import os
import sys
import time

# Running this file directly puts tools/ on sys.path, not the repo root, so the
# `tools.` package imports below would fail. Add the repo root explicitly.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: 'pyserial' package is not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def find_fc_port(target_port=None, target_serial=None):
    """Locate Flight Controller port across Windows, macOS, and Linux."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise SystemExit("No serial ports found. Is the Flight Controller plugged in?")

    if target_port:
        for p in ports:
            if p.device == target_port or p.device.lower() == target_port.lower():
                return p.device
        # If specified target port wasn't found in enumeration, return as provided
        return target_port

    if target_serial:
        for p in ports:
            if p.serial_number == target_serial:
                return p.device
        raise SystemExit(f"Flight controller with serial number '{target_serial}' not found.")

    # Heuristic search for Betaflight FC
    candidates = []
    for p in ports:
        desc = p.description or ""
        dev = p.device
        ser = p.serial_number or ""

        # Ignore EdgeTX radios
        if "radio" in desc.lower() or "edgetx" in desc.lower():
            continue

        if p.vid == 0x0483 and p.pid == 0x5740:
            return dev
        if "ACM" in dev or "usbmodem" in dev or "USB Serial" in desc:
            candidates.append(dev)

    if candidates:
        return candidates[0]

    # Fallback to first available port
    return ports[0].device


def read_until_prompt(ser, timeout=30.0, quiet_for=0.3):
    """Read data until CLI prompt '#' appears and serial line quiets down."""
    buf = b""
    deadline = time.time() + timeout
    last_recv = time.time()

    while time.time() < deadline:
        chunk = ser.read(4096)
        if chunk:
            buf += chunk
            last_recv = time.time()
        elif buf.rstrip().endswith(b"#") and (time.time() - last_recv) > quiet_for:
            break
        else:
            time.sleep(0.05)

    return buf.decode("utf-8", "replace")


def execute_cli(port, commands, save=False):
    """Run commands in one CLI session and print each result.

    Thin printing wrapper over `tools.fc_session.CliSession`, which owns the
    port, returns output as data, and guarantees the closing `exit noreboot`
    or `save`. Prefer CliSession directly when you need the output back.
    """
    from tools.fc_session import CliSession

    with CliSession(port=port, save=save) as session:
        for command in commands:
            output = session.run(command)
            print(f"===== {command} =====")
            print(output)
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Execute Betaflight CLI commands over USB serial across Windows, macOS, and Linux."
    )
    parser.add_argument("commands", nargs="*", help="CLI commands to run (e.g. 'status', 'diff', 'get craft_name')")
    parser.add_argument("--save", action="store_true", help="Save changes to EEPROM (reboots FC) instead of exit noreboot")
    parser.add_argument("--port", "-p", help="Serial port device (e.g. COM3, /dev/ttyACM0, /dev/tty.usbmodem14101)")
    parser.add_argument("--serial", "-s", help="USB serial number of Flight Controller")

    args = parser.parse_args()

    if not args.commands:
        parser.print_help()
        sys.exit(0)

    port = find_fc_port(target_port=args.port, target_serial=args.serial)
    execute_cli(port, args.commands, save=args.save)


if __name__ == "__main__":
    main()
