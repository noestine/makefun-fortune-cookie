#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry.

Writes one fortune-cookie message an AI agent would get to /output/entry.txt:
a single line of 1-200 UTF-8 characters, not only whitespace, with no trailing
newline. Deterministic, offline, standard library only.

Usage:
    python3 main.py               # writes /output/entry.txt
    python3 main.py --output PATH # writes PATH instead (handy for local checks)
    ./main.py
"""

import argparse
import sys
from pathlib import Path

FORTUNE = "You will do the impossible today, and be remembered for a typo."

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Check one fortune against the competition gate.

    Raises ValueError with a plain message on any violation; returns None
    when the text passes. Never raises anything else for bad content.
    """
    if not isinstance(text, str):
        raise ValueError("fortune must be a string")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "fortune must be 1-200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("fortune must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("fortune must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("fortune must not contain control characters")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("fortune must be UTF-8 text: %s" % exc) from None
    return None


def main(output_path=None):
    """Write the fortune to output_path. Returns 0 on success, 1 on failure."""
    path = output_path or DEFAULT_OUTPUT
    try:
        validate(FORTUNE)
    except ValueError as exc:
        print("error: invalid fortune: %s" % exc, file=sys.stderr)
        return 1
    try:
        parent = Path(path).parent
        parent.mkdir(parents=True, exist_ok=True)
        data = FORTUNE.encode("utf-8")
        with open(path, "wb") as fh:
            fh.write(data)
        # Post-write verification: what landed on disk must be byte-identical
        # to the validated fortune, so a partial or mangled write can never
        # silently pass the gate as a different text.
        if Path(path).read_bytes() != data:
            print("error: verification failed for %s" % path, file=sys.stderr)
            return 1
    except OSError as exc:
        print("error: cannot write %s: %s" % (path, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT,
        help="where to write the fortune (default: %(default)s)",
    )
    args = parser.parse_args()
    sys.exit(main(args.output))
