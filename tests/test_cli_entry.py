#!/usr/bin/env python
"""Tests for the `python -m spotify2ytmusic` entry point.

The module runs its dispatch at import time from sys.argv, so I run it
in a subprocess. ytmusicapi is not installed in every environment, so
the subprocess gets a stub ytmusicapi module on PYTHONPATH; the entry
point only needs the import to succeed, because these tests stop at
the usage and unknown command paths, before any command runs.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def run_module(args, stub_dir):
    env = dict(os.environ)
    env["PYTHONPATH"] = stub_dir + os.pathsep + os.path.abspath(REPO_ROOT)
    return subprocess.run(
        [sys.executable, "-m", "spotify2ytmusic"] + args,
        capture_output=True,
        text=True,
        env=env,
        cwd=REPO_ROOT,
        timeout=60,
    )


class TestCliEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stub_dir = tempfile.mkdtemp()
        with open(os.path.join(cls.stub_dir, "ytmusicapi.py"), "w") as f:
            f.write("class YTMusic:\n    pass\n")

    def test_no_arguments_prints_usage_and_exits_1(self):
        result = run_module([], self.stub_dir)
        self.assertEqual(result.returncode, 1)
        self.assertIn("usage: spotify2ytmusic", result.stdout)
        self.assertIn("copy_playlist", result.stdout)

    def test_unknown_command_is_named_and_exits_1(self):
        result = run_module(["coppy_playlist"], self.stub_dir)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unknown command 'coppy_playlist'", result.stdout)
        self.assertIn("copy_playlist", result.stdout)

    def test_imported_names_are_not_commands(self):
        # backend is a module cli imports; sys is a module __main__
        # imports. Neither is a command, and neither may be dispatched.
        for name in ("backend", "sys"):
            result = run_module([name], self.stub_dir)
            self.assertEqual(result.returncode, 1, name)
            self.assertIn(f"Unknown command '{name}'", result.stdout)


if __name__ == "__main__":
    unittest.main()
