#!/usr/bin/env python3
"""WhoopShop PID & Rate Tuning Preset Helper.

Provides curated PID profiles, rate curves, and filter baselines for 1S/2S micro whoops.

Usage:
    python tools/tuning_tool.py --list
    python tools/tuning_tool.py --preset 65mm-indoor-1s --preview
    python tools/tuning_tool.py --preset 75mm-freestyle-1s --apply
"""
import argparse
import sys

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


PRESETS = {
    "65mm-indoor-1s": {
        "description": "Smooth, high D-term damping for tight indoor 65mm Whoops",
        "commands": [
            "set p_pitch = 52",
            "set i_pitch = 85",
            "set d_pitch = 38",
            "set f_pitch = 110",
            "set p_roll = 48",
            "set i_roll = 80",
            "set d_roll = 35",
            "set f_roll = 105",
            "set p_yaw = 55",
            "set i_yaw = 85",
            "set d_yaw = 0",
            "set f_yaw = 100",
            "set dynamic_idle_min_rpm = 30",
            "set anti_gravity_gain = 80",
        ]
    },
    "75mm-freestyle-1s": {
        "description": "Snappy P-term & elevated anti-gravity for outdoor 75mm Whoop acro",
        "commands": [
            "set p_pitch = 64",
            "set i_pitch = 90",
            "set d_pitch = 44",
            "set f_pitch = 130",
            "set p_roll = 60",
            "set i_roll = 85",
            "set d_roll = 40",
            "set f_roll = 125",
            "set p_yaw = 65",
            "set i_yaw = 90",
            "set d_yaw = 0",
            "set f_yaw = 115",
            "set dynamic_idle_min_rpm = 35",
            "set anti_gravity_gain = 120",
        ]
    },
    "cinewhoop-1s": {
        "description": "Linear rate response & heavy filtering for smooth camera recording",
        "commands": [
            "set p_pitch = 45",
            "set i_pitch = 95",
            "set d_pitch = 42",
            "set f_pitch = 90",
            "set p_roll = 42",
            "set i_roll = 90",
            "set d_roll = 38",
            "set f_roll = 85",
            "set dynamic_idle_min_rpm = 28",
            "set anti_gravity_gain = 70",
        ]
    }
}


def list_presets():
    print("Available WhoopShop Tuning Presets:")
    print("-----------------------------------")
    for name, data in PRESETS.items():
        print(f"  • {name:<20} : {data['description']}")
    print()


def apply_preset(name, preview=True, port=None):
    if name not in PRESETS:
        print(f"ERROR: Unknown preset '{name}'. Use `python tools/tuning_tool.py --list` to view options.")
        sys.exit(1)

    preset = PRESETS[name]
    print(f"# Preset: {name} — {preset['description']}\n")

    if preview:
        print("--- CLI Commands Preview (No changes applied) ---")
        for cmd in preset["commands"]:
            print(f"  {cmd}")
        print("  save")
        print("\nTo apply these settings to your FC, run:")
        print(f"  python tools/tuning_tool.py --preset {name} --apply")
    else:
        print("[!] WARNING: Ensure ALL PROPELLERS ARE REMOVED before applying settings.")
        port = find_fc_port(target_port=port)
        print(f"# Applying preset '{name}' to FC on {port}...", file=sys.stderr)
        execute_cli(port, preset["commands"], save=True)
        print(f"\n[+] Preset '{name}' successfully saved to EEPROM!")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop PID & Rate Tuning Preset Helper.")
    parser.add_argument("--list", action="store_true", help="List available tuning presets")
    parser.add_argument("--preset", help="Name of preset to preview or apply")
    parser.add_argument("--preview", action="store_true", help="Print CLI commands without applying to FC")
    parser.add_argument("--apply", action="store_true", help="Apply preset commands and save to FC EEPROM")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.list or not args.preset:
        list_presets()
        if not args.list and not args.preset:
            print("Usage example: python tools/tuning_tool.py --preset 65mm-indoor-1s --preview")
        sys.exit(0)

    if args.preset:
        apply_preset(args.preset, preview=not args.apply, port=args.port)


if __name__ == "__main__":
    main()
