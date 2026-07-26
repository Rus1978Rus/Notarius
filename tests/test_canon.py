# -*- coding: utf-8 -*-
"""Tests of the canonicalization pre-pass (AD-33, ported from Vakhter).

We check the real behavior: revealing the transport encoding and a candid
overlong UTF-8 flag. All offline, stdlib only.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.canon import canonicalize, decode_utf8_lenient


class TestCanonicalize(unittest.TestCase):

    def test_clean_text_unchanged(self):
        canon, meta = canonicalize("plain text with no encoding")
        self.assertEqual(canon, "plain text with no encoding")
        self.assertFalse(meta["changed"])
        self.assertEqual(meta["decode_passes"], 0)
        self.assertFalse(meta["overlong_utf8"])

    def test_double_percent_decode(self):
        # %252e%252e%252f -> (pass1) %2e%2e%2f -> (pass2) ../
        canon, meta = canonicalize("%252e%252e%252fboot.ini")
        self.assertEqual(canon, "../boot.ini")
        self.assertEqual(meta["decode_passes"], 2)
        self.assertTrue(meta["changed"])

    def test_html_entity_reveals_zwsp(self):
        # &#8203; is a ZERO WIDTH SPACE, a hidden insertion into a word
        canon, meta = canonicalize("admin&#8203;istrator")
        self.assertIn("​", canon)
        self.assertTrue(meta["changed"])

    def test_overlong_utf8_flagged(self):
        # %c0%af — overlong smuggling of "/". Downstream will see "/",
        # we show that AND raise a flag.
        canon, meta = canonicalize("A%c0%afB")
        self.assertEqual(canon, "A/B")
        self.assertTrue(meta["overlong_utf8"])

    def test_legit_cyrillic_no_false_overlong(self):
        # Legitimate percent-encoded Russian text must NOT be falsely
        # flagged as overlong.
        canon, meta = canonicalize("%d0%bf%d1%80%d0%b8%d0%b2%d0%b5%d1%82")
        self.assertEqual(canon, "привет")
        self.assertFalse(meta["overlong_utf8"])

    def test_numeric_ip_host_normalized(self):
        canon, _ = canonicalize("http://2130706433/")
        self.assertEqual(canon, "http://127.0.0.1/")

    def test_decode_utf8_lenient_direct(self):
        txt, over = decode_utf8_lenient(b"\xc0\xaf")
        self.assertEqual(txt, "/")
        self.assertTrue(over)


if __name__ == "__main__":
    unittest.main(verbosity=2)
