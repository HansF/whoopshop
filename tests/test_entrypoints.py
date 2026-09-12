"""Every tool must be runnable the way the documentation says to run it.

The docs all use `python tools/<name>.py ...`, which puts `tools/` on sys.path
rather than the repo root. A tool that only imports correctly as part of the
`tools` package works in these tests but fails for the user. This module runs
each tool as a subprocess, exactly as a reader of the README would.
"""
import ast
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")


def tool_scripts():
    return sorted(
        name for name in os.listdir(TOOLS_DIR)
        if name.endswith(".py") and not name.startswith("_")
    )


class EntryPointTest(unittest.TestCase):

    def test_every_tool_runs_as_a_script(self):
        """`python tools/<name>.py --help` must exit cleanly from the repo root."""
        failures = []
        for name in tool_scripts():
            result = subprocess.run(
                [sys.executable, os.path.join("tools", name), "--help"],
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                failures.append(f"{name}: {result.stderr.strip().splitlines()[-1:]}")
        self.assertEqual(failures, [], "tools that fail when run as scripts")

    def test_no_tool_imports_tools_package_without_a_path_bootstrap(self):
        """Guards the specific regression: a lazy `from tools.x import y`.

        A module-level try/except ImportError bootstrap, or an explicit sys.path
        insert, must be present in any file that imports from `tools.`.
        """
        offenders = []
        for name in tool_scripts():
            path = os.path.join(TOOLS_DIR, name)
            with open(path, encoding="utf-8") as handle:
                source = handle.read()

            tree = ast.parse(source, filename=name)
            # Real import statements only. Docstrings and comments showing
            # example usage are not imports and must not be flagged.
            imports_tools = any(
                (isinstance(node, ast.ImportFrom)
                 and (node.module or "").startswith("tools"))
                or (isinstance(node, ast.Import)
                    and any(alias.name.startswith("tools") for alias in node.names))
                for node in ast.walk(tree)
            )
            if imports_tools and "sys.path.insert" not in source:
                offenders.append(name)
        self.assertEqual(offenders, [],
                         "tools importing the tools package with no sys.path bootstrap")


if __name__ == "__main__":
    unittest.main()
