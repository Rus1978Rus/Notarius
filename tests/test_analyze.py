# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Tests of the shared analysis engine notarius/analyze.py (AD-93) — the one
engine behind both the CLI and the local web app.

Run: python3 tests/test_analyze.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.analyze import analyze_documents, analyze_files, scan_document  # noqa: E402


class TestCompare(unittest.TestCase):
    def test_identical(self):
        r = analyze_documents("amount: 1000\n", "amount: 1000\n")
        self.assertTrue(r["identical"])
        self.assertEqual(r["findings"], [])

    def test_amount_swap_localized(self):
        r = analyze_documents("amount: 1 000 000 USD", "amount: 9 000 000 USD")
        self.assertFalse(r["identical"])
        self.assertEqual(len(r["findings"]), 1)
        f = r["findings"][0]
        self.assertEqual(f["line"], 1)
        self.assertEqual(f["category"], "VALUE_SUBSTITUTION")

    def test_invisible_char_flagged(self):
        r = analyze_documents("terms: payable", "terms: pay​able")
        self.assertEqual(r["hidden"]["risk"], "ALARM")
        self.assertTrue(any(f["category"] == "INVISIBLE_INSERTION" for f in r["findings"]))

    def test_homoglyph_domain_flagged(self):
        # Cyrillic 'а' (U+0430) in the host — a look-alike domain, INTRODUCED
        r = analyze_documents("reply-to: paypal.com", "reply-to: paypаl.com")
        self.assertTrue(r["url_risks"])
        self.assertEqual(r["url_risks"][0]["issue"], "homoglyph_in_host")

    def test_preexisting_manipulation_not_reflagged(self):
        # a mixed-script token already in the ORIGINAL (legit bilingual / pre-existing)
        # must NOT be reported as manipulation — only what the transfer INTRODUCED.
        ref = "user: аdmin\namount: 1000"     # 'аdmin' with a Cyrillic 'а' already here
        rcv = "user: аdmin\namount: 2000"     # same token; only the amount changed
        r = analyze_documents(ref, rcv)
        self.assertFalse(r["identical"])
        self.assertEqual(r["hidden"]["risk"], "OK")   # not introduced → no false alarm
        self.assertTrue(any(f["category"] == "VALUE_SUBSTITUTION" for f in r["findings"]))


class TestScanOne(unittest.TestCase):
    def test_clean(self):
        r = scan_document("just a plain sentence with no tricks")
        self.assertEqual(r["hidden"]["risk"], "OK")
        self.assertFalse(r["url_risks"])

    def test_invisible(self):
        r = scan_document("admin​istrator")
        self.assertEqual(r["hidden"]["risk"], "ALARM")
        self.assertIn("ALARM", r["summary"])


class TestFiles(unittest.TestCase):
    def test_identical_bytes(self):
        r = analyze_files(b"same bytes", b"same bytes")
        self.assertEqual(r["kind"], "identical")
        self.assertTrue(r["identical"])

    def test_text_file_gets_full_analysis(self):
        # JSON is text → full where+what analysis, catches the value swap
        r = analyze_files(b'{"amount": 1000}', b'{"amount": 9000}')
        self.assertEqual(r["kind"], "text")
        self.assertTrue(any(f["category"] == "VALUE_SUBSTITUTION" for f in r["findings"]))

    def test_binary_gets_honest_fingerprint_verdict(self):
        # PNG-like bytes (invalid UTF-8) → fingerprint verdict + honest boundary
        png_a = b"\x89PNG\r\n\x1a\n\x00\x01\x02\xff\xfe"
        png_b = b"\x89PNG\r\n\x1a\n\x00\x01\x02\xff\x00"
        r = analyze_files(png_a, png_b)
        self.assertEqual(r["kind"], "binary")
        self.assertFalse(r["identical"])
        self.assertNotEqual(r["ref_sha"], r["recv_sha"])
        self.assertIn("not WHERE inside", r["boundary"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
