#!/usr/bin/env python3
"""WhoopShop VTX & OSD Configuration Tool.

Inspects and configures Video Transmitter (SmartAudio/Tramp) band, channel,
power levels, pit mode, and On-Screen Display (OSD) positions.

Usage:
    python tools/vtx_osd_tool.py --info
    python tools/vtx_osd_tool.py --band RACEBAND --channel 8 --power 25
"""
import argparse
import sys

try:
    from tools.bf_vars import assert_valid, check_responses
    from tools.fc_session import CliSession
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import assert_valid, check_responses
    from tools.fc_session import CliSession


def get_vtx_info(port=None):
    print("# Querying VTX & OSD configuration...", file=sys.stderr)
    with CliSession(port=port) as fc:
        results = fc.run_many([
            "get vtx_band",
            "get vtx_channel",
            "get vtx_power",
            "get vtx_pit_mode",
            "get osd_vbat_pos",
            "get osd_craft_name_pos",
        ])
    check_responses(results)

    for command, output in results.items():
        print(f"===== {command} =====")
        print(output)
        print()


def set_vtx(band=None, channel=None, power=None, pitmode=None, port=None):
    cmds = []
    if band:
        cmds.append(f"set vtx_band = {band.upper()}")
    if channel:
        cmds.append(f"set vtx_channel = {channel}")
    if power:
        cmds.append(f"set vtx_power = {power}")
    if pitmode:
        cmds.append(f"set vtx_pit_mode = {pitmode.upper()}")

    if not cmds:
        print("No VTX parameters specified. Use --info to view settings.")
        return

    assert_valid(cmds)
    with CliSession(port=port, save=True) as fc:
        print(f"# Applying VTX parameters on {fc.port}...", file=sys.stderr)
        results = fc.run_many(cmds)
    check_responses(results)
    print("\n[+] VTX configuration saved to EEPROM!")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop VTX & OSD Configuration Tool.")
    parser.add_argument("--info", action="store_true", help="Query current VTX & OSD settings")
    parser.add_argument("--band", help="VTX Band (e.g. RACEBAND, FATSHARK, BOSCAM_A)")
    parser.add_argument("--channel", type=int, choices=range(1, 9), help="VTX Channel (1-8)")
    parser.add_argument("--power", type=int, help="VTX Power index (e.g. 1=25mW, 2=100mW, 3=400mW)")
    parser.add_argument("--pitmode", choices=["ON", "OFF"], help="Enable/disable VTX pit mode")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.band or args.channel or args.power or args.pitmode:
        set_vtx(band=args.band, channel=args.channel, power=args.power, pitmode=args.pitmode, port=args.port)
    else:
        get_vtx_info(args.port)


if __name__ == "__main__":
    main()
