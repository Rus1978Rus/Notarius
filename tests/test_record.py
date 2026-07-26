# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Tests of the managed record notarius/record.py (AD-87): field keepers,
sealed void, legitimate progression, localization of violations.

Run: python3 tests/test_record.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey                                  # noqa: E402

from notarius.record import (create_record, edit_field, rebuild,      # noqa: E402
                             footnotes, audit)


def _kp():
    p = bytes(SigningKey.generate())
    return p, bytes(SigningKey(p).verify_key).hex()


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.a_priv, _ = _kp()
        self.kaz_priv, self.kaz_pub = _kp()      # Treasurer — keeper of the numbers
        self.jur_priv, self.jur_pub = _kp()      # Lawyer — keeper of the deadline
        self.men_priv, self.men_pub = _kp()      # Manager — keeper of the recipient
        self.keepers = {"recipient": "Manager", "amount": "Treasurer",
                        "due_date": "Lawyer"}
        self.keeper_keys = {"Manager": self.men_pub, "Treasurer": self.kaz_pub,
                            "Lawyer": self.jur_pub}
        self.rec = create_record(
            {"recipient": "Contractor LLC", "amount": "1000000 USD", "due_date": ""},
            self.keepers, self.keeper_keys, "Author", self.a_priv, "09:00")

    def _legit(self):
        e1 = edit_field(self.rec, "Lawyer", self.jur_priv, "10:00",
                        "due_date", "until 2026-08-10")  # filled the void (its own keeper)
        e2 = edit_field(e1, "Treasurer", self.kaz_priv, "11:30", "amount", "1050000 USD")
        return [e1, e2]

    def test_legit_progress_clean(self):
        r = audit(self.rec, self._legit(), rebuild(self.rec, self._legit()))
        self.assertTrue(r["intact"], r["findings"])

    def test_non_keeper_edits_numbers(self):
        e1 = edit_field(self.rec, "Manager", self.men_priv, "11:40", "amount", "9000000 USD")
        r = audit(self.rec, [e1])
        kinds = {k for k, _, _ in r["findings"]}
        self.assertIn("EDIT_BY_NON_KEEPER", kinds)

    def test_unsigned_change_localized(self):
        legit = self._legit()
        forged = dict(rebuild(self.rec, legit)); forged["amount"] = "9000000 USD"  # unsigned tamper
        r = audit(self.rec, legit, forged)
        self.assertFalse(r["intact"])
        self.assertTrue(any(k == "UNSIGNED_CHANGE" and f == "amount"
                            for k, f, _ in r["findings"]))

    def test_new_slot_flagged(self):
        legit = self._legit()
        cur = dict(rebuild(self.rec, legit)); cur["hidden_line"] = "to account XX"
        r = audit(self.rec, legit, cur)
        self.assertTrue(any(k == "NEW_SLOT" for k, _, _ in r["findings"]))

    def test_sealed_void_fill_by_keeper_is_legit(self):
        # filling the empty deadline by ITS OWN keeper (the Lawyer) — legitimate
        e1 = edit_field(self.rec, "Lawyer", self.jur_priv, "10:00",
                        "due_date", "until 2026-08-10")
        r = audit(self.rec, [e1], rebuild(self.rec, [e1]))
        self.assertTrue(r["intact"], r["findings"])

    def test_void_fill_by_non_keeper_flagged(self):
        e1 = edit_field(self.rec, "Manager", self.men_priv, "10:00",
                        "due_date", "until yesterday")    # not the deadline's keeper
        r = audit(self.rec, [e1])
        self.assertIn("EDIT_BY_NON_KEEPER", {k for k, _, _ in r["findings"]})

    def test_chain_broken_detected(self):
        e1 = edit_field(self.rec, "Lawyer", self.jur_priv, "10:00", "due_date", "x")
        # the second edit references CREATION, not e1 → the chain breaks
        e2 = edit_field(self.rec, "Treasurer", self.kaz_priv, "11:30", "amount", "2 USD")
        r = audit(self.rec, [e1, e2])
        self.assertIn("CHAIN_BROKEN", {k for k, _, _ in r["findings"]})

    def test_footnotes_render(self):
        fn = footnotes(self.rec, self._legit())
        self.assertTrue(fn[0].startswith("[created]"))
        self.assertTrue(any("amount" in x for x in fn))


if __name__ == "__main__":
    unittest.main(verbosity=2)
