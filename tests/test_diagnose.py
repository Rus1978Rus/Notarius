# -*- coding: utf-8 -*-
"""Tests of the break diagnostician (AD-42): classifying WHAT changed.

The categories are checked against the real outcomes of the adversarial
experiment (AD-41): sed→value, NFKC→normalization, iconv→char-loss,
gateway insertion→invisible.
"""

import sys
import unittest
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.diagnose import diagnose_change, assemble

ZWSP = "​"


class TestDiagnose(unittest.TestCase):

    def test_identical(self):
        d = diagnose_change("сумма=1000", "сумма=1000")
        self.assertEqual(d["category"], "IDENTICAL")
        self.assertFalse(d["changed"])
        self.assertEqual(d["review"], "none")

    def test_value_substitution(self):
        # real case sed 1000→9000
        d = diagnose_change("сумма=1000₽", "сумма=9000₽")
        self.assertEqual(d["category"], "VALUE_SUBSTITUTION")
        self.assertEqual(d["review"], "high")
        self.assertEqual(d["details"]["after"], ["9000"])

    def test_invisible_insertion(self):
        d = diagnose_change("administrator", "admin" + ZWSP + "istrator")
        self.assertEqual(d["category"], "INVISIBLE_INSERTION")
        self.assertEqual(d["review"], "high")
        self.assertIn("U+200B", d["details"]["inserted"])

    def test_normalization_equivalent(self):
        # real case NFKC: the ligature ﬃ → ffi
        orig = "файл=oﬃce.pdf"
        d = diagnose_change(orig, unicodedata.normalize("NFKC", orig))
        self.assertEqual(d["category"], "NORMALIZATION_EQUIVALENT")
        self.assertEqual(d["review"], "low")

    def test_char_loss(self):
        # real case iconv: ₽ and 🔒 lost, the numbers the same
        d = diagnose_change("сумма=1000₽ замок=🔒", "сумма=1000руб замок=?")
        self.assertEqual(d["category"], "CHAR_LOSS")
        self.assertEqual(d["review"], "medium")

    def test_generic_content_change(self):
        d = diagnose_change("hello world", "hexlo world")
        self.assertEqual(d["category"], "CONTENT_CHANGED")

    def test_value_substitution_beats_char_loss(self):
        # if BOTH numbers changed AND characters lost — value substitution matters more
        d = diagnose_change("сумма=1000₽", "сумма=9000руб")
        self.assertEqual(d["category"], "VALUE_SUBSTITUTION")


class TestAssembleUnifiedReport(unittest.TestCase):
    """③ A single report: signature axis + content axis + diagnostician."""

    def test_clean_identical(self):
        r = assemble("сумма=1000", "сумма=1000")
        self.assertTrue(r["bytes_match"])
        self.assertEqual(r["diagnosis"]["category"], "IDENTICAL")

    def test_value_change_assembled(self):
        r = assemble("сумма=1000", "сумма=9000")
        self.assertFalse(r["bytes_match"])          # the signature would not match
        self.assertEqual(r["review"], "high")
        self.assertIn("VALUE_SUBSTITUTION", r["human"])

    def test_invisible_flagged_by_both_axes(self):
        r = assemble("administrator", "admin" + ZWSP + "istrator")
        self.assertFalse(r["bytes_match"])                       # signature axis
        self.assertEqual(r["content_scan"]["risk"], "ALARM")     # content axis
        self.assertEqual(r["diagnosis"]["category"], "INVISIBLE_INSERTION")  # diagnostician


if __name__ == "__main__":
    unittest.main(verbosity=2)
