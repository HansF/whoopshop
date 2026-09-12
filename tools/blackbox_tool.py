#!/usr/bin/env python3
"""WhoopShop Blackbox Log Manager & Helper Tool.

Handles onboard SPI Flash operations, USB mass-storage (`msc`) mode, log copying,
and decoding across Windows, macOS, and Linux.

Usage:
    python tools/blackbox_tool.py --info          # Check flash capacity & usage
    python tools/blackbox_tool.py --erase         # Erase blackbox SPI flash
    python tools/blackbox_tool.py --msc           # Reboot FC into Mass Storage mode
    python tools/blackbox_tool.py --copy          # Copy .bbl logs from mounted BETAFLT drive to logs/
    python tools/blackbox_tool.py --decode log.bbl # Decode .bbl file to CSV
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import time

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    # Handle direct script invocation from tools/ dir
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


def get_flash_info(port=None):
    """Query flash_info over CLI."""
    port = find_fc_port(target_port=port)
    print("# Querying flash_info...", file=sys.stderr)
    execute_cli(port, ["flash_info"])


def erase_flash(port=None):
    """Erase onboard flash memory."""
    port = find_fc_port(target_port=port)
    print("# WARNING: Erasing onboard flash memory...", file=sys.stderr)
    execute_cli(port, ["flash_erase"], save=True)


def trigger_msc_mode(port=None):
    """Put FC into USB Mass-Storage Mode."""
    port = find_fc_port(target_port=port)
    print("# Rebooting FC into USB Mass Storage Mode (msc)...", file=sys.stderr)
    try:
        execute_cli(port, ["msc"])
    except SystemExit:
        pass  # FC disconnects immediately on msc, so exit is expected

    print("\n[!] Flight Controller rebooted into Mass Storage Mode.")
    print("    - The FC now acts as a USB flash drive labelled 'BETAFLT'.")
    print("    - CLI/MSP commands will not work until USB is physically replugged.")
    print("    - Run `python tools/blackbox_tool.py --copy` to pull log files.")


def find_betaflt_mount():
    """Detect BETAFLT drive path on Windows, macOS, and Linux."""
    system = platform.system()

    if system == "Linux":
        # Check standard Linux mount points
        user = os.environ.get("USER", "")
        search_paths = [
            f"/run/media/{user}/BETAFLT",
            "/media/BETAFLT",
            f"/media/{user}/BETAFLT",
        ]
        for p in search_paths:
            if os.path.exists(p):
                return p

        # Check via udisksctl / mount command if present
        try:
            out = subprocess.check_output(["lsblk", "-o", "NAME,LABEL,MOUNTPOINT"], text=True)
            for line in out.splitlines():
                if "BETAFLT" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        return parts[-1]
        except Exception:
            pass

    elif system == "Darwin":  # macOS
        mac_path = "/Volumes/BETAFLT"
        if os.path.exists(mac_path):
            return mac_path

    elif system == "Windows":
        # Check drive letters A: to Z: for volume label BETAFLT
        try:
            import string
            from ctypes import kernel32, create_unicode_buffer

            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    vol_name = create_unicode_buffer(1024)
                    if kernel32.GetVolumeInformationW(drive, vol_name, 1024, None, None, None, None, 0):
                        if vol_name.value.upper() == "BETAFLT":
                            return drive
        except Exception:
            pass

    return None


def copy_logs():
    """Copy .bbl log files from mounted BETAFLT drive into local logs/ directory."""
    mount_point = find_betaflt_mount()
    if not mount_point:
        print("ERROR: BETAFLT volume not found.")
        print("Ensure FC is in `msc` mode and the USB drive is mounted.")
        if platform.system() == "Linux":
            print("Tip: Run `udisksctl mount -b /dev/sdX1` if unmounted.")
        sys.exit(1)

    print(f"Found BETAFLT drive at: {mount_point}")
    target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(target_dir, exist_ok=True)

    copied = 0
    for root, _, files in os.walk(mount_point):
        for file in files:
            # Copy numbered btfl_*.bbl files, ignore btfl_all.bbl and padding.txt
            if file.startswith("btfl_") and file.endswith(".bbl") and file != "btfl_all.bbl":
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)
                print(f"Copying {file} -> {dst}")
                shutil.copy2(src, dst)
                copied += 1

    if copied > 0:
        print(f"\n[+] Successfully copied {copied} log file(s) to `{target_dir}`.")
        print("    Remember to physically replug the USB cable to exit Mass Storage mode.")
    else:
        print("No new `.bbl` files found on BETAFLT drive.")


def decode_log(bbl_filename):
    """Decode a .bbl file into CSV using blackbox_decode if available."""
    decoder = shutil.which("blackbox_decode")
    if not decoder:
        print("ERROR: `blackbox_decode` utility is not installed on this system.")
        print("Install `blackbox-tools` package (e.g. `paru -S blackbox-tools-git` on Arch or build from source).")
        sys.exit(1)

    if not os.path.exists(bbl_filename):
        # Try looking inside logs/ directory
        target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        in_logs = os.path.join(target_dir, bbl_filename)
        if os.path.exists(in_logs):
            bbl_filename = in_logs
        else:
            print(f"ERROR: File not found: {bbl_filename}")
            sys.exit(1)

    print(f"Decoding '{bbl_filename}' with {decoder}...")
    subprocess.run([decoder, bbl_filename])


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Blackbox Log Manager Tool.")
    parser.add_argument("--info", action="store_true", help="Query flash_info capacity and usage")
    parser.add_argument("--erase", action="store_true", help="Erase onboard SPI flash memory")
    parser.add_argument("--msc", action="store_true", help="Reboot FC into USB Mass Storage Mode")
    parser.add_argument("--copy", action="store_true", help="Copy .bbl files from BETAFLT drive to logs/")
    parser.add_argument("--decode", metavar="FILE.bbl", help="Decode a .bbl file to CSV format")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.info:
        get_flash_info(args.port)
    elif args.erase:
        erase_flash(args.port)
    elif args.msc:
        trigger_msc_mode(args.port)
    elif args.copy:
        copy_logs()
    elif args.decode:
        decode_log(args.decode)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
