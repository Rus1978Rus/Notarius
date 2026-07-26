# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Regression tests for external audit #2 (2026-07-26), AD-91.
Each test reproduces a reviewer's finding and pins its closure.

Run: python3 tests/test_audit_fixes.py
"""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey                                  # noqa: E402

from notarius.cli import cmd_seal, cmd_verify                       # noqa: E402
from notarius.custody import KeyCustody                             # noqa: E402
from notarius.carrier import issue_carrier                          # noqa: E402
from notarius.record import create_record, edit_field, audit        # noqa: E402
from notarius import trace as T                                     # noqa: E402


class TestNW1SignedReceipt(unittest.TestCase):
    def test_tampered_receipt_caught(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "d.txt"
            f.write_text("amount=1000", encoding="utf-8")
            self.assertEqual(cmd_seal(str(f)), 0)
            self.assertEqual(cmd_verify(str(f)), 0)          # clean
            # attack: edit the file + recompute the hash in the receipt WITHOUT re-signing
            f.write_text("amount=9000", encoding="utf-8")
            ntr = Path(str(f) + ".ntr")
            rec = json.loads(ntr.read_text(encoding="utf-8"))
            rec["sha256"] = hashlib.sha256(f.read_bytes()).hexdigest()
            ntr.write_text(json.dumps(rec), encoding="utf-8")
            self.assertEqual(cmd_verify(str(f)), 1)          # FORGED (was a false 0)


class TestNW2CustodySelfVerify(unittest.TestCase):
    def test_corrupt_share_refused(self):
        ck = KeyCustody(m=2, n=3)
        sh = ck.issue_shares()
        self.assertTrue(ck.sign(b"m", sh[:2])["ok"])         # honest shares — ok
        bad = [dict(sh[0]), dict(sh[1])]
        bad[0]["y"] ^= 0xDEAD
        r = ck.sign(b"m", bad)
        self.assertFalse(r["ok"])
        self.assertIn("SHARE_CORRUPT", r["reason"])


class TestNW6RandomNonce(unittest.TestCase):
    def test_reissue_same_second_ok(self):
        c1 = issue_carrier({"x": 1}, b"k" * 32, issued_at=100)
        c2 = issue_carrier({"x": 1}, b"k" * 32, issued_at=100)
        self.assertNotEqual(c1["nonce"], c2["nonce"])        # not a self-inflicted DoS


class TestNW7RecordNoLeak(unittest.TestCase):
    def test_forged_edit_not_in_official(self):
        ap = bytes(SigningKey.generate())
        kp = bytes(SigningKey.generate())
        kpub = bytes(SigningKey(kp).verify_key).hex()
        xp = bytes(SigningKey.generate())
        rec = create_record({"amount": "1000"}, {"amount": "Treasurer"},
                            {"Treasurer": kpub}, "A", ap, "t0")
        res = audit(rec, [edit_field(rec, "Outsider", xp, "t1", "amount", "9000")])
        self.assertFalse(res["intact"])
        self.assertEqual(res["official"]["amount"], "1000")  # forgery NOT in official


class TestNW45Trace(unittest.TestCase):
    def setUp(self):
        self.a = bytes(SigningKey.generate())

    def test_element_id_continuity(self):
        tr = T.new_trace("A", "v", "orig", "alice", self.a, "t0")
        tr = T.append_event(tr, "v", "TRANSFERRED", "alice", self.a, "t1")
        tr2 = [tr[0], dict(tr[1], element_id="B")]
        self.assertEqual(T.verify_trace(tr2)["status"], "TRACE_BREAK_DETECTED")

    def test_first_must_be_created(self):
        full = T.append_event(
            T.new_trace("A", "v", "orig", "alice", self.a, "t0"),
            "v", "TRANSFERRED", "alice", self.a, "t1")
        self.assertEqual(T.verify_trace([full[1]])["status"], "TRACE_BREAK_DETECTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
