"""Tests for main.py — Fortune Cookies for Machines.

Written FIRST from RULES.txt, before main.py exists. The gate: /output/entry.txt
must be UTF-8 text of 1-200 characters, not only whitespace, a single line.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import main

FORTUNE = "You will do the impossible today, and be remembered for a typo."


class TestFortuneConstant(unittest.TestCase):
    def test_exact_string(self):
        """The shipped line must be exactly this, word for word."""
        self.assertEqual(main.FORTUNE, FORTUNE)

    def test_length_within_gate(self):
        self.assertGreaterEqual(len(main.FORTUNE), 1)
        self.assertLessEqual(len(main.FORTUNE), 200)
        self.assertEqual(len(main.FORTUNE), 63)

    def test_single_line_no_whitespace_only(self):
        self.assertNotIn("\n", main.FORTUNE)
        self.assertNotIn("\r", main.FORTUNE)
        self.assertTrue(main.FORTUNE.strip())

    def test_utf8_encodable(self):
        main.FORTUNE.encode("utf-8")


class TestValidate(unittest.TestCase):
    def test_valid_passes(self):
        self.assertIsNone(main.validate(FORTUNE))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            main.validate("")

    def test_whitespace_only_rejected(self):
        with self.assertRaises(ValueError):
            main.validate("   \n\t  ")

    def test_too_long_rejected(self):
        with self.assertRaises(ValueError):
            main.validate("x" * 201)

    def test_200_chars_accepted(self):
        self.assertIsNone(main.validate("x" * 200))

    def test_multiline_rejected(self):
        with self.assertRaises(ValueError):
            main.validate("line one\nline two")

    def test_control_character_rejected(self):
        with self.assertRaises(ValueError):
            main.validate("a fortune\x07with a bell")


class TestMainRun(unittest.TestCase):
    def test_writes_exact_bytes_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            self.assertEqual(main.main(str(out)), 0)
            self.assertEqual(out.read_bytes(), FORTUNE.encode("utf-8"))

    def test_creates_missing_parent_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested" / "entry.txt"
            self.assertEqual(main.main(str(out)), 0)
            self.assertEqual(out.read_text(encoding="utf-8"), FORTUNE)

    def test_overwrites_stale_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            out.write_text("stale junk\n", encoding="utf-8")
            self.assertEqual(main.main(str(out)), 0)
            self.assertEqual(out.read_text(encoding="utf-8"), FORTUNE)

    def test_deterministic_two_runs_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = Path(tmp) / "a.txt"
            out2 = Path(tmp) / "b.txt"
            self.assertEqual(main.main(str(out1)), 0)
            self.assertEqual(main.main(str(out2)), 0)
            self.assertEqual(out1.read_bytes(), out2.read_bytes())

    def test_bad_constant_fails_gracefully_no_traceback(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            old = main.FORTUNE
            try:
                main.FORTUNE = "   "
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    self.assertEqual(main.main(str(out)), 1)
                self.assertFalse(out.exists())
                self.assertIn("error", err.getvalue().lower())
                self.assertNotIn("Traceback", err.getvalue())
            finally:
                main.FORTUNE = old

    def test_unwritable_output_fails_gracefully(self):
        with tempfile.TemporaryDirectory() as tmp:
            # A directory where the file should be: open() raises IsADirectoryError.
            out = Path(tmp) / "entry.txt"
            out.mkdir()
            self.assertEqual(main.main(str(out)), 1)

    def test_runs_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parent / "main.py"),
                 "--output", str(out)],
                capture_output=True, text=True, cwd="/",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), FORTUNE)

    def test_direct_execution_shebang(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            script = Path(__file__).resolve().parent / "main.py"
            result = subprocess.run(
                [str(script), "--output", str(out)],
                capture_output=True, text=True, cwd=tmp,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), FORTUNE)


if __name__ == "__main__":
    unittest.main()
