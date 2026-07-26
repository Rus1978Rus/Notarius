# -*- coding: utf-8 -*-
"""Tests of the detection engine (AD-33, ported from Vakhter).

Project discipline: negative tests are mandatory — we pin down BOTH what
is caught (ALARM) AND what is candidly NOT caught / cleared (OK/WATCH).
The BEHAVIOR of the logic is checked, not "security".
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.detect import (
    analyze, combine, Finding,
    invisible_cards_reader, canonical_view_reader,
)

ZWSP = "​"
ZWJ = "‍"
RLO = "‮"
PDF = "‬"
MAN = chr(0x1F468)
LAPTOP = chr(0x1F4BB)
TAGA = chr(0xE0041)      # tag 'A' (an invisible ASCII carrier)
VS0 = chr(0xFE00)


class TestSmuggleAlarms(unittest.TestCase):
    """Proven smuggles → ALARM (conclusive)."""

    def test_zero_width_wordsplit(self):
        r = analyze(f"pay{ZWSP}pal")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "zw_wordsplit")

    def test_bidi_imbalance_trojan_source(self):
        r = analyze(f"file{RLO}gnp.js")     # RLO with no PDF
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "bidi_imbalance")

    def test_tag_smuggle_no_flag_base(self):
        r = analyze(f"hello{TAGA}")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "tag_smuggle")

    def test_vs_carrier_run(self):
        r = analyze("abc" + VS0 * 3)
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "vs_carrier")

    def test_parser_desync_inside_token(self):
        # ZWSP between 'l' and '.' — not a word split, but a parser desync
        r = analyze(f"paypal{ZWSP}.com")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "parser_desync")


class TestLegitGlueOK(unittest.TestCase):
    """Legitimate glue → OK (we don't raise a false alarm)."""

    def test_clean_text(self):
        self.assertEqual(analyze("перевод 1000 USD компании А")["risk"], "OK")

    def test_emoji_zwj_is_glue(self):
        r = analyze(f"{MAN}{ZWJ}{LAPTOP}")     # person+ZWJ+laptop
        self.assertEqual(r["risk"], "OK")

    def test_balanced_bidi_is_glue(self):
        r = analyze(f"{RLO}текст{PDF}")         # RLO...PDF balanced
        self.assertEqual(r["risk"], "OK")


class TestWatch(unittest.TestCase):
    """An invisible is present, but neither smuggle nor glue → WATCH (not OK, not ALARM)."""

    def test_lone_zwsp_between_spaces(self):
        r = analyze(f"amount = 1000 {ZWSP} USD")
        self.assertEqual(r["risk"], "WATCH")
        self.assertEqual(r["signature"], "invisible_watch")


class TestCanonIntegration(unittest.TestCase):
    """Canonicalization + detection together (end-to-end pass)."""

    def test_entity_encoded_zwsp_revealed_then_alarmed(self):
        # &#8203; = ZWSP; canonicalization reveals it, the detector catches the word-split
        r = analyze("admin&#8203;istrator")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "zw_wordsplit")
        self.assertTrue(r["canon_meta"]["changed"])

    def test_overlong_utf8_alarmed(self):
        r = analyze("A%c0%afB")                 # overlong "/"
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "overlong_utf8")


class TestFailClosed(unittest.TestCase):
    """Fail-closed: a non-string / error → block, never OK."""

    def test_non_string_blocks(self):
        r = analyze(12345)
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "invalid_input")


class TestCombine(unittest.TestCase):
    """combine = severity-max (the map only raises suspicion)."""

    def test_severity_max(self):
        clean = Finding("clean", 0.0, "ok")
        watch = Finding("suspect", 0.4, "watch")
        alarm = Finding("suspect", 0.9, "alarm", conclusive=True)
        self.assertEqual(combine(clean, watch, alarm), alarm)
        self.assertEqual(combine(clean, watch), watch)
        self.assertEqual(combine(clean, clean).label, "clean")


class TestMonitoredClassNoSilentPass(unittest.TestCase):
    """AD-35: generalization to the whole monitored class — NOT A SINGLE silent OK.

    Measurement (FL SIGN_EXAMINER) showed: the hole was not in 4 characters
    but systemic — characters without a card gave verdict=OK. The fix widened
    the class (Cf ∪ DI ∪ VS).
    """

    def _monitored(self):
        import unicodedata as u
        cps = []
        for cp in list(range(0, 0x10000)) + list(range(0xE0000, 0xE0200)):
            ch = chr(cp)
            if (u.category(ch) == "Cf" or 0xFE00 <= cp <= 0xFE0F
                    or 0xE0100 <= cp <= 0xE01EF):
                cps.append(cp)
        return cps

    def test_no_silent_pass_in_host(self):
        silent = [f"U+{cp:04X}" for cp in self._monitored()
                  if analyze(f"pay{chr(cp)}pal.com")["risk"] == "OK"]
        self.assertEqual(silent, [], f"silent pass in host: {silent[:8]}")

    def test_no_silent_pass_between_spaces(self):
        silent = [f"U+{cp:04X}" for cp in self._monitored()
                  if analyze(f"a {chr(cp)} b")["risk"] == "OK"]
        self.assertEqual(silent, [], f"silent pass between spaces: {silent[:8]}")

    def test_sign_examiner_gap_list_all_flagged(self):
        # the "uncovered invisibles" list from SIGN_EXAMINER (FL 2026-07-05)
        gap = [0x200B, 0x200C, 0x200D, 0xFEFF, 0x2060,
               0x2061, 0x2062, 0x2063, 0x2064, 0x202A, 0x202B, 0x202C]
        for cp in gap:
            self.assertNotEqual(analyze(f"2{chr(cp)}3")["risk"], "OK",
                                f"U+{cp:04X} passed silently")

    def test_invisible_math_ops_both_positions(self):
        for cp in (0x2061, 0x2062, 0x2063, 0x2064):
            self.assertEqual(analyze(f"2{chr(cp)}3")["risk"], "ALARM")   # in a token
            self.assertNotEqual(analyze(f"2 {chr(cp)} 3")["risk"], "OK")  # ≥ WATCH

    def test_homoglyph_is_out_of_scope(self):
        # Candid boundary: homoglyphs (VISIBLE lookalikes) are a DIFFERENT
        # family, NOT covered by this fix (Vakhter confusable_cards not ported).
        # We pin the current behavior, we don't claim coverage.
        self.assertEqual(analyze("paypоl.com")["risk"], "OK")  # Cyrillic 'о'


if __name__ == "__main__":
    unittest.main(verbosity=2)
