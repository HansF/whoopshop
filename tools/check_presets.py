#!/usr/bin/env python3
"""Validate every canned command list in this workspace against bf_vars.

Runs in CI with no flight controller attached. It exists because a wrong
variable name is invisible at runtime: Betaflight prints `Invalid name` and
carries on, so a preset can appear to apply while silently doing nothing.

Usage:
    python -m tools.check_presets
"""
import sys

try:
    from tools.bf_vars import validate
    from tools.tuning_tool import PRESETS
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import validate
    from tools.tuning_tool import PRESETS


def collect():
    """Return {source label: [commands]} for every hard-coded command list."""
    groups = {}
    for name, preset in PRESETS.items():
        groups[f"tuning_tool preset '{name}'"] = list(preset["commands"])
    return groups


def main():
    failures = 0
    for label, commands in sorted(collect().items()):
        problems = validate(commands)
        if problems:
            failures += 1
            print(f"FAIL  {label}")
            for problem in problems:
                print(f"        {problem}")
        else:
            print(f"ok    {label} ({len(commands)} commands)")

    if failures:
        print(f"\n{failures} command list(s) contain names the flight controller will reject.")
        return 1

    print("\nAll command lists use valid Betaflight variable names.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
