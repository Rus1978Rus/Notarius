# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Tests of domain/URL awareness (AD-81): a lookalike/invisible in the DOMAIN → HIGH,
userinfo spoofing, in the path → MEDIUM, a legit URL → clean.

Run: python3 tests/test_urlcontext.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.urlcontext import scan_url, find_url_context_risks   # noqa: E402
from notarius.scanner import scan_hardened                         # noqa: E402

CYR_A = "а"       # Cyr. а
ZWSP = "​"


class TestUrlContext(unittest.TestCase):
    def test_homoglyph_in_host_high(self):
        r = scan_url("payp" + CYR_A + "l.com")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "homoglyph_in_host")

    def test_invisible_in_host_high(self):
        r = scan_url("goog" + ZWSP + "le.com")
        self.assertEqual(r["signature"], "invisible_in_host")
        self.assertEqual(r["risk"], "ALARM")

    def test_userinfo_spoof(self):
        r = scan_url("paypal.com@evil.ru")
        self.assertEqual(r["signature"], "userinfo_spoof")
        self.assertEqual(r["risk"], "ALARM")

    def test_path_only_medium(self):
        r = scan_url("https://example.com/p" + CYR_A + "th")
        self.assertEqual(r["risk"], "WATCH")

    def test_legit_url_clean(self):
        self.assertEqual(scan_url("https://github.com/user/repo")["risk"], "OK")
        self.assertEqual(scan_url("user@example.com")["risk"], "OK")
        self.assertEqual(scan_url("just text with no links")["risk"], "OK")

    def test_scan_hardened_uses_context(self):
        # the general smuggle is overridden by the specific domain signature
        r = scan_hardened("payp" + CYR_A + "l.com")
        self.assertEqual(r["risk"], "ALARM")
        self.assertEqual(r["signature"], "homoglyph_in_host")
        self.assertIn("url_context", r)

    def test_scan_hardened_legit_stays_ok(self):
        self.assertEqual(scan_hardened("https://github.com/x")["risk"], "OK")


if __name__ == "__main__":
    unittest.main(verbosity=2)
