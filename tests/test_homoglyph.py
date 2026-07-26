# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Tests of the defect fixes found by Kimi through execution (AD-79):
  1. a homoglyph is classified (diagnose) and alarms the standalone scanner;
  2. time is self-declared without an external anchor (trace.time_proven);
  3. cosign fail-CLOSED on a failed quorum (not INTACT).

Run: python3 tests/test_homoglyph.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey                                # noqa: E402

from notarius.diagnose import diagnose_change                     # noqa: E402
from notarius.homoglyph import (deconfuse, confusables_in,          # noqa: E402
                                mixed_script_words, skeleton, CONFUSABLES)
from notarius.scanner import scan_hardened                         # noqa: E402
from notarius import trace as T                                    # noqa: E402
from notarius.cosign import (verify_witnessed_trace,                # noqa: E402
                             make_checkpoint, Witness)

CYR_A = "а"   # Cyrillic "а", a lookalike of the Latin a


class TestHomoglyph(unittest.TestCase):
    def test_deconfuse_and_list(self):
        self.assertEqual(deconfuse(CYR_A + "dmin"), "admin")
        self.assertEqual(confusables_in(CYR_A + "dmin"), [CYR_A])
        self.assertEqual(confusables_in("admin"), [])

    def test_diagnose_classifies_homoglyph(self):
        d = diagnose_change("admin", CYR_A + "dmin")
        self.assertEqual(d["category"], "HOMOGLYPH_SUBSTITUTION")
        self.assertEqual(d["review"], "high")

    def test_scanner_alarms_mixed_script(self):
        s = scan_hardened(CYR_A + "dmin")
        self.assertEqual(s["risk"], "ALARM")
        self.assertEqual(s["signature"], "homoglyph_mixed_script")

    def test_pure_cyrillic_not_flagged(self):
        # a purely Cyrillic word — not a mix, there should be no false alarm
        self.assertEqual(mixed_script_words("привет"), [])
        self.assertEqual(scan_hardened("привет")["risk"], "OK")

    def test_identical_still_identical(self):
        self.assertEqual(diagnose_change("x", "x")["category"], "IDENTICAL")


class TestUTS39Coverage(unittest.TestCase):
    """AD-80: expansion to UTS#39 data (1861 lookalikes instead of ~50)."""

    def test_data_map_loaded(self):
        self.assertGreater(len(CONFUSABLES), 1000)   # a real dataset, not a hand-made one

    def test_skeleton_collapses_lookalikes(self):
        self.assertEqual(skeleton("admin"), skeleton("а" + "dmin"))

    def test_greek_and_idn_caught(self):
        # a Greek omicron in login
        d = diagnose_change("login", "lοgin")
        self.assertEqual(d["category"], "HOMOGLYPH_SUBSTITUTION")
        # IDN homograph: paypal.com with a Cyr. а
        d2 = diagnose_change("paypal.com", "paypаl.com")
        self.assertEqual(d2["category"], "HOMOGLYPH_SUBSTITUTION")
        self.assertEqual(scan_hardened("paypаl.com")["risk"], "ALARM")


class TestNoAutoEscalate(unittest.TestCase):
    """Borrowed msl_mip discipline (AD-80): the layer is ALWAYS advisory —
    it never emits a blocking/auto-escalating action."""

    _ADVISORY = {"OK", "WATCH", "ALARM"}

    def test_scanner_only_advisory_risk(self):
        battery = ["чистый текст", "admin", "а" + "dmin", "adm​in",
                   "paypаl.com", "‮abc", "a\U000e0041b", ""]
        for t in battery:
            r = scan_hardened(t)
            self.assertIn(r["risk"], self._ADVISORY,
                          f"non-advisory risk {r['risk']!r} on {t!r}")
            # no field carries a blocking action
            for v in r.values():
                self.assertNotIn(v, ("block", "escalate_to_human", "reject"))


class TestTimeProven(unittest.TestCase):
    def test_selfdeclared_time_flagged(self):
        a = bytes(SigningKey.generate())
        tr = T.new_trace("el", "v0", "orig", "alice", a, "2020-01-01T00:00Z")
        rep = T.verify_trace(tr)
        self.assertEqual(rep["status"], "INTACT")       # the chain is intact
        self.assertFalse(rep["time_proven"])            # but time is not proven
        self.assertTrue(any("TIME IS SELF-DECLARED" in r for r in rep["reasons"]))


class TestCosignFailClosed(unittest.TestCase):
    def test_unwitnessed_head_not_intact(self):
        a = bytes(SigningKey.generate())
        log = bytes(SigningKey.generate())
        w = Witness(bytes(SigningKey.generate()))
        tr = T.new_trace("el", "v0", "orig", "alice", a, "t0")
        cp = make_checkpoint(tr, "log-1", log)
        r = verify_witnessed_trace(tr, cp, [], {w.pub.hex()}, threshold=1)
        self.assertNotEqual(r["status"], "INTACT")      # fail-closed
        self.assertEqual(r["status"], "UNWITNESSED_HEAD")
        self.assertFalse(r["witness"]["quorum_ok"])
        self.assertEqual(r["chain_status"], "INTACT")   # the chain result is kept


if __name__ == "__main__":
    unittest.main(verbosity=2)
