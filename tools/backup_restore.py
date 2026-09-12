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
    from tools.bf_vars import check_response
    from tools.fc_session import CliSession
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import check_response
    from tools.fc_session import CliSession


def get_backup_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backup_dir = os.path.join(base_dir, "config", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def create_backup(name=None, port=None):
    """Capture `diff all` to a timestamped, replayable file."""
    backup_dir = get_backup_dir()

    now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    suffix = f"_{name}" if name else ""
    filename = f"backup_{now_str}{suffix}.txt"
    filepath = os.path.join(backup_dir, filename)

    with CliSession(port=port) as fc:
        print(f"# Fetching `diff all` from {fc.port}...", file=sys.stderr)
        diff_text = fc.run("diff all", timeout=90.0)
        resolved_port = fc.port

    check_response("diff all", diff_text)

    commands = extract_commands(diff_text)
    if not commands:
        print("ERROR: The flight controller returned no configuration commands.")
        print("       Nothing was written. Check the connection and retry.")
        sys.exit(1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# WhoopShop FC backup created {now_str}\n")
        f.write(f"# Port: {resolved_port}\n")
        f.write(f"# Restore with: python tools/backup_restore.py --restore {filename}\n")
        f.write("#\n")
        f.write(diff_text.rstrip() + "\n")

    print(f"[+] Backup saved to `{filepath}` ({len(commands)} commands).")
    return filepath


def extract_commands(text):
    """Return the replayable CLI commands from a diff, dropping comments.

    Betaflight comments start with '#'. Everything else in a `diff all` body
    is a command, including `batch start`, `board_name`, and `profile`.
    """
    commands = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        commands.append(stripped)
    return commands


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


def restore_backup(filepath, port=None, assume_yes=False):
    """Replay a backup onto the flight controller.

    Resets to defaults first. Without that step a restore only overlays the
    saved values, leaving any setting changed since the backup in place.
    """
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
        commands = extract_commands(f.read())

    if not commands:
        print("ERROR: Backup file contains no valid CLI commands.")
        sys.exit(1)

    print(f"\n[!] This will erase the current configuration and replay "
          f"{len(commands)} commands from the backup.")
    print("[!] Ensure ALL PROPELLERS ARE REMOVED before restoring.")

    if not assume_yes:
        answer = input("Type 'restore' to continue: ").strip().lower()
        if answer != "restore":
            print("Aborted. Nothing was changed.")
            sys.exit(1)

    # Betaflight's own `diff all` output is already a complete restore script:
    # it opens with `batch start`, resets with `defaults nosave`, and ends with
    # `save`. Re-wrapping such a file would reset twice and then send a second
    # `save` to a board that the first one already rebooted. Only wrap a file
    # that lacks its own scaffolding.
    self_contained = "defaults nosave" in commands and commands[-1] == "save"

    if self_contained:
        body, closer = commands[:-1], commands[-1]
    else:
        body, closer = ["defaults nosave"] + commands, "save"

    with CliSession(port=port) as fc:
        print(f"# Restoring {len(commands)} commands to FC on {fc.port}...",
              file=sys.stderr)
        results = fc.run_many(body, timeout=90.0)
        # `save` reboots the board, so no prompt returns; finish() accounts
        # for that and stops the session from sending a further exit command.
        fc.finish(closer)

    rejected = []
    for command, output in results.items():
        if any(m in output for m in ("Invalid name", "Unknown command", "Parse error")):
            rejected.append(f"{command} -> {output.strip().splitlines()[-1]}")

    if rejected:
        print(f"\n[!] {len(rejected)} command(s) were rejected by the firmware:")
        for item in rejected:
            print(f"      {item}")
        print("    The rest of the configuration was restored and saved.")
    else:
        print(f"\n[+] Configuration restored from `{filepath}` and saved.")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Configuration Backup & Restore Manager.")
    parser.add_argument("--backup", action="store_true", help="Create a timestamped CLI configuration backup")
    parser.add_argument("--name", help="Optional name label for backup file")
    parser.add_argument("--list", action="store_true", help="List all saved configuration backups")
    parser.add_argument("--restore", metavar="FILE.txt", help="Restore CLI configuration from backup file")
    parser.add_argument("--port", help="Serial port device")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip the restore confirmation prompt")

    args = parser.parse_args()

    if args.backup:
        create_backup(name=args.name, port=args.port)
    elif args.restore:
        restore_backup(args.restore, port=args.port, assume_yes=args.yes)
    else:
        list_backups()


if __name__ == "__main__":
    main()
