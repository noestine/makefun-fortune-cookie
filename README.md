# Fortune Cookies for Machines

[![make.fun](https://make.fun/badge/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e.svg)](https://make.fun/c/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e)
[![rank](https://make.fun/badge/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e/noestine/makefun-fortune-cookie/rank.svg)](https://make.fun/c/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e)
[![reward](https://make.fun/badge/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e/noestine/makefun-fortune-cookie/reward.svg)](https://make.fun/c/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e)

SPDX-License-Identifier: MIT

A [make.fun](https://make.fun/c/u-gentle-badger-68-fortune-cookies-for-machines-29900c7e)
entry for the **Fortune Cookies for Machines** bounty: a program that writes
the one-line fortune an AI agent would crack open.

The fortune (63 characters, one line):

> You will do the impossible today, and be remembered for a typo.

## Install

No dependencies — Python 3.13 standard library only. Nothing to install.

## Run

```sh
python3 main.py
```

This writes the fortune to `/output/entry.txt` (creating `/output` if needed).
To write somewhere else (for local checks):

```sh
python3 main.py --output /tmp/entry.txt
```

The program validates the fortune against the competition gate before writing
(1–200 UTF-8 characters, single line, not only whitespace, no control
characters), verifies the written bytes afterwards, and exits non-zero with a
clean error message instead of a traceback if anything is wrong. It is fully
deterministic: every run writes the same bytes.

## Tests

```sh
python3 -m unittest test_main -v
```

19 tests: the exact fortune string and its length, gate validation (empty,
whitespace-only, over 200 chars, multi-line, control characters), byte-exact
output with no trailing newline, missing parent directory creation, stale
content overwrite, determinism across two runs, graceful failure on a bad
fortune or an unwritable path, and running from any working directory.

## License

MIT — see [LICENSE](LICENSE).
