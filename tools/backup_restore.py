#!/usr/bin/env python3
"""WhoopShop Configuration Backup & Restore Manager.

Creates timestamped CLI `diff all` configuration backups, lists stored backups,
and restores known-good configurations.

Usage:
    python tools/backup_restore.py --backup
    python tools/backup_restore.py --list
    python tools/backup_restore.py --restore config/backups/2026-09-12_100000.txt
"""
import argparse
import datetime
import os
import sys

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


def get_backup_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backup_dir = os.path.join(base_dir, "config", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def create_backup(name=None, port=None):
    port = find_fc_port(target_port=port)
    backup_dir = get_backup_dir()

    now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    suffix = f"_{name}" if name else ""
    filename = f"backup_{now_str}{suffix}.txt"
    filepath = os.path.join(backup_dir, filename)

    print(f"# Fetching CLI diff all from {port}...", file=sys.stderr)

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            execute_cli(port, ["diff all"])
    except Exception as err:
        print(f"ERROR: Failed to fetch diff from FC: {err}")
        sys.exit(1)

    diff_text = buf.getvalue()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# WhoopShop FC Backup created on {now_str}\n")
        f.write(f"# Port: {port}\n\n")
        f.write(diff_text)

    print(f"[+] Backup successfully saved to: `{filepath}`")
    return filepath


def list_backups():
    backup_dir = get_backup_dir()
    files = sorted([f for f in os.listdir(backup_dir) if f.endswith(".txt")], reverse=True)

    print("==================================================")
    print("  WhoopShop Saved Configuration Backups")
    print("==================================================")
    if not files:
        print("  No backups found in config/backups/.")
    else:
        for f in files:
            size = os.path.getsize(os.path.join(backup_dir, f))
            print(f"  • {f:<35} ({size} bytes)")
    print("==================================================\n")


def restore_backup(filepath, port=None):
    if not os.path.exists(filepath):
        backup_dir = get_backup_dir()
        alt_path = os.path.join(backup_dir, filepath)
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            print(f"ERROR: Backup file not found: {filepath}")
            sys.exit(1)

    print(f"# Reading backup file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Filter comments and empty lines, keep CLI commands
    commands = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

    if not commands:
        print("ERROR: Backup file contains no valid CLI commands.")
        sys.exit(1)

    port = find_fc_port(target_port=port)
    print(f"[!] Restoring {len(commands)} CLI commands to FC on {port}...", file=sys.stderr)
    execute_cli(port, commands, save=True)
    print(f"\n[+] Configuration successfully restored from `{filepath}` and saved!")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Configuration Backup & Restore Manager.")
    parser.add_argument("--backup", action="store_true", help="Create a timestamped CLI configuration backup")
    parser.add_argument("--name", help="Optional name label for backup file")
    parser.add_argument("--list", action="store_true", help="List all saved configuration backups")
    parser.add_argument("--restore", metavar="FILE.txt", help="Restore CLI configuration from backup file")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.backup:
        create_backup(name=args.name, port=args.port)
    elif args.restore:
        restore_backup(args.restore, port=args.port)
    else:
        list_backups()


if __name__ == "__main__":
    main()
