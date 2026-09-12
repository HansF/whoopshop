#!/usr/bin/env python3
"""WhoopShop FC Diagnostic & Port Scanner Tool.

Detects connected Betaflight Flight Controllers across Windows, macOS, and Linux.
Checks for serial port availability, process locks, and system tools.

Usage:
    python tools/fc_check.py
"""
import os
import platform
import shutil
import sys

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: 'pyserial' package is not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


# Known Betaflight USB IDs
# Note: EdgeTX radios also use 0483:5740 (STM32 VCP). We inspect description/serial number to distinguish.
STM32_VCP_VID = 0x0483
STM32_VCP_PID = 0x5740
STM32_DFU_PID = 0xDF11
STM32_MSC_PID = 0x5720


def scan_serial_ports():
    ports = serial.tools.list_ports.comports()
    fc_candidates = []
    other_ports = []

    for p in ports:
        desc = p.description or ""
        hwid = p.hwid or ""
        ser = p.serial_number or "N/A"
        vid = p.vid
        pid = p.pid

        is_fc = False
        notes = []

        # Check USB IDs
        if vid == STM32_VCP_VID:
            if pid == STM32_DFU_PID:
                notes.append("DFU Bootloader mode (Flash via Betaflight Configurator)")
            elif pid == STM32_MSC_PID:
                notes.append("USB Mass Storage mode (Blackbox Flash access)")
            elif pid == STM32_VCP_PID:
                # Distinguish FC from EdgeTX handset
                if "radio" in desc.lower() or "edgetx" in desc.lower() or "opentx" in desc.lower():
                    notes.append("EdgeTX Radio Handset")
                else:
                    is_fc = True
                    notes.append("Flight Controller (VCP)")

        # Fallback heuristic for generic ttyACM / tty.usbmodem / COM ports
        if not is_fc and ("ACM" in p.device or "usbmodem" in p.device or "USB Serial" in desc):
            is_fc = True
            notes.append("Likely Serial Flight Controller")

        port_info = {
            "device": p.device,
            "description": desc,
            "serial_number": ser,
            "vid_pid": f"{vid:04x}:{pid:04x}" if vid and pid else "Unknown",
            "is_fc": is_fc,
            "notes": ", ".join(notes) if notes else "Generic Serial Device",
        }

        if is_fc:
            fc_candidates.append(port_info)
        else:
            other_ports.append(port_info)

    return fc_candidates, other_ports


def check_system_tools():
    tools = {
        "blackbox_decode": shutil.which("blackbox_decode"),
        "udisksctl (Linux)": shutil.which("udisksctl"),
        "diskutil (macOS)": shutil.which("diskutil"),
    }
    return tools


def main():
    os_name = platform.system()
    python_ver = platform.python_version()

    print("==================================================")
    print(f"  WhoopShop Diagnostics — {os_name} ({platform.machine()})")
    print(f"  Python: {python_ver} | PySerial: {serial.__version__}")
    print("==================================================\n")

    fc_candidates, other_ports = scan_serial_ports()

    if fc_candidates:
        print(f"Found {len(fc_candidates)} Flight Controller candidate(s):")
        for idx, fc in enumerate(fc_candidates, 1):
            print(f"  [{idx}] Device       : {fc['device']}")
            print(f"      Description  : {fc['description']}")
            print(f"      Serial No    : {fc['serial_number']}")
            print(f"      USB VID:PID  : {fc['vid_pid']}")
            print(f"      Notes        : {fc['notes']}")
            print()
    else:
        print("NO Flight Controller detected.")
        print("  - Check USB cable (ensure it supports data, not power-only).")
        print("  - Ensure FC is powered or plugged directly into host.")
        print()

    if other_ports:
        print(f"Other Serial Devices detected ({len(other_ports)}):")
        for p in other_ports:
            print(f"  - {p['device']} ({p['description']}) [VID:PID {p['vid_pid']}] — {p['notes']}")
        print()

    print("System Utilities Check:")
    tools = check_system_tools()
    for name, path in tools.items():
        status = f"Available ({path})" if path else "Not Found (Optional)"
        print(f"  - {name:<20}: {status}")

    print("\nNext Steps:")
    if fc_candidates:
        dev = fc_candidates[0]['device']
        print(f"  - Test CLI query : python tools/bf_cli.py \"status\"")
        print(f"  - Read live MSP  : python tools/bf_msp.py")
    else:
        print("  - Connect Flight Controller over USB and rerun `python tools/fc_check.py`.")


if __name__ == "__main__":
    main()
