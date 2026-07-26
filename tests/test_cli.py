# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Tests of the minimal product notarius check/seal/verify (AD-64).

Run: python3 tests/test_cli.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.cli import cmd_check, cmd_seal, cmd_verify, main   # noqa: E402

ORIG = "amount to transfer: 1000000 RUB\nbasis: act No. 77\n"
TAMPERED = "amount to trans​fer: 9000000 RUB\nbasis: act No. 77\n"


def _w(d: Path, name: str, text: str) -> str:
    p = d / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def run():
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        o = _w(d, "orig.txt", ORIG)
        r = _w(d, "recv.txt", TAMPERED)
        same = _w(d, "same.txt", ORIG)

        # check: value substitution → break (code 1)
        assert cmd_check(o, r) == 1, "a swap should yield a BREAK"
        # check: identical → untouched (code 0)
        assert cmd_check(o, same) == 0, "identical ones should match"

        # seal → verify of the clean one = 0, verify of the swapped one = 1
        assert cmd_seal(o) == 0
        assert Path(o + ".ntr").exists(), "the receipt should be created"
        assert cmd_verify(o) == 0, "the original should pass verify"

        # swap the file content, the receipt stays the same
        Path(o).write_text(TAMPERED, encoding="utf-8")
        assert cmd_verify(o) == 1, "the changed one should not pass verify"

        # verify with no receipt → code 2
        assert cmd_verify(r) == 2, "no receipt — code 2"

        # main router: an invalid command → 2, help → 0
        assert main(["--help"]) == 0
        assert main(["bogus"]) == 2
        assert main([]) == 0

        # different binary files → break (code 1), without crashing
        b1 = d / "a.bin"; b1.write_bytes(b"\xff\x00\x01")
        b2 = d / "b.bin"; b2.write_bytes(b"\xff\x00\x02")
        assert cmd_check(str(b1), str(b2)) == 1

    print("test_cli: OK (10 checks)")


if __name__ == "__main__":
    run()
