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
import sys
import time

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
    """Connect to FC, send commands, and cleanly exit CLI mode."""
    print(f"# Connecting to Flight Controller on {port}...", file=sys.stderr)

    try:
        ser = serial.Serial(port, 115200, timeout=0.2)
    except serial.SerialException as err:
        raise SystemExit(f"Failed to open port {port}: {err}\nEnsure no other program (Betaflight Configurator, terminal) is using the port.")

    with ser:
        ser.dtr = True
        time.sleep(0.4)
        ser.reset_input_buffer()

        # Step 1: Send bare '#' without line endings to initiate CLI handshake
        ser.write(b"#")
        ser.flush()

        prompt_output = read_until_prompt(ser, timeout=6.0)
        if "#" not in prompt_output:
            raise SystemExit(
                "No CLI prompt received from FC.\n"
                "Possible causes:\n"
                "  1. FC is stuck in CLI mode from a previous session -> Unplug and replug USB.\n"
                "  2. FC is in DFU or Mass Storage mode -> Replug FC.\n"
                "  3. Serial port speed mismatch."
            )

        # Step 2: Run commands
        for cmd in commands:
            ser.reset_input_buffer()
            ser.write((cmd + "\r\n").encode("utf-8"))
            ser.flush()
            out = read_until_prompt(ser, timeout=60.0)

            print(f"===== {cmd} =====")
            print(out.strip())
            print()

        # Step 3: Guaranteed CLI exit discipline
        exit_cmd = b"save\r\n" if save else b"exit noreboot\r\n"
        ser.write(exit_cmd)
        ser.flush()
        time.sleep(1.5 if save else 0.5)

        if save:
            print("# Saved settings to EEPROM. FC rebooting.", file=sys.stderr)
        else:
            print("# Exited CLI mode cleanly (no reboot). FC ready for MSP / normal operation.", file=sys.stderr)


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
