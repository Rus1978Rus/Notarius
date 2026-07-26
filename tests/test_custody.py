"""Tests of the custody envelope: threshold + mortal heartbeat + expiry.

Demonstrates the working core of AD-26 executably:
the single point of trust is removed, and share theft is piecemeal and temporary.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import VerifyKey  # noqa: E402
from notarius.custody import KeyCustody, _split, _reconstruct  # noqa: E402

MSG = b"amount=1000000|recipient=CompanyA"


class TestShamirCore(unittest.TestCase):

    def test_reconstruct_roundtrip(self):
        secret = 123456789012345678901234567890
        pts = _split(secret, 3, 5)
        self.assertEqual(_reconstruct(pts[:3]), secret)

    def test_any_m_subset_reconstructs(self):
        secret = 42
        pts = _split(secret, 3, 5)
        self.assertEqual(_reconstruct([pts[0], pts[2], pts[4]]), secret)


class TestThreshold(unittest.TestCase):

    def setUp(self):
        self.kc = KeyCustody(m=3, n=5)

    def test_m_shares_sign_and_verify(self):
        shares = self.kc.issue_shares()
        r = self.kc.sign(MSG, shares[:3])
        self.assertTrue(r["ok"])
        VerifyKey(self.kc.public_key).verify(MSG, bytes.fromhex(r["sig"]))

    def test_m_minus_1_fails(self):
        shares = self.kc.issue_shares()
        self.assertFalse(self.kc.sign(MSG, shares[:2])["ok"])

    def test_single_share_is_useless(self):
        shares = self.kc.issue_shares()
        self.assertFalse(self.kc.sign(MSG, shares[:1])["ok"])


class TestStaleShares(unittest.TestCase):
    """Expiry: shares from a past epoch are useless (proactive refresh)."""

    def test_stolen_old_shares_die_after_refresh(self):
        kc = KeyCustody(m=3, n=5)
        stolen = kc.issue_shares()[:3]     # the thief copied the epoch-0 shares
        kc.heartbeat()                     # the owner refreshed the epoch → 1
        r = kc.sign(MSG, stolen)
        self.assertFalse(r["ok"])
        self.assertIn("expired", r["reason"])
        # fresh shares of the current epoch — they work:
        self.assertTrue(kc.sign(MSG, kc.issue_shares()[:3])["ok"])


class TestMortalPulse(unittest.TestCase):
    """Mortal heartbeat (Kimi B2): silence kills the key and all copies."""

    def test_no_heartbeat_kills_key(self):
        kc = KeyCustody(m=3, n=5, max_missed_beats=2)
        shares = kc.issue_shares()
        kc.tick(); kc.tick()               # 2 misses — still alive
        self.assertTrue(kc.alive)
        kc.tick()                          # 3rd miss — death
        self.assertFalse(kc.alive)
        # even with M shares signing is impossible — the copy inherits mortality:
        r = kc.sign(MSG, shares[:3])
        self.assertFalse(r["ok"])
        self.assertIn("KEY_DEAD", r["reason"])

    def test_heartbeat_keeps_alive(self):
        kc = KeyCustody(m=3, n=5, max_missed_beats=2)
        for _ in range(10):
            kc.tick(); kc.heartbeat()      # a heartbeat every tick
        self.assertTrue(kc.alive)
        self.assertTrue(kc.sign(MSG, kc.issue_shares()[:3])["ok"])

    def test_dead_key_issues_no_shares(self):
        kc = KeyCustody(m=2, n=3, max_missed_beats=0)
        kc.tick()                          # dead immediately
        self.assertEqual(kc.issue_shares(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
