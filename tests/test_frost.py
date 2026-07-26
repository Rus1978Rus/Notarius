# -*- coding: utf-8 -*-
"""Tests of FROST-ED25519 (AD-38): a real threshold, the verify side does NOT change.

The nail (proof of AD-30): a 2-of-3 threshold signature is accepted by an
UNMODIFIED verify_envelope_v2 and an ordinary PyNaCl VerifyKey. Plus
negatives: one share (< threshold) and tampering do not pass.
"""

import hashlib
import sys
import unicodedata
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import VerifyKey

from notarius import frost
from notarius.envelope_v2 import verify_envelope_v2, _canonical

MSG = b"element=amount value=1000000 recipient=CompanyA"


class TestThresholdSignature(unittest.TestCase):

    def test_any_two_of_three_verify(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        for pair in ((0, 1), (0, 2), (1, 2)):
            sig = frost.sign([shares[pair[0]], shares[pair[1]]], MSG, A)
            VerifyKey(A).verify(MSG, sig)   # raises on failure
            self.assertEqual(len(sig), 64)

    def test_all_three_over_threshold_verify(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        VerifyKey(A).verify(MSG, frost.sign(shares, MSG, A))

    def test_single_share_below_threshold_fails(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        sig = frost.sign([shares[0]], MSG, A)
        with self.assertRaises(Exception):
            VerifyKey(A).verify(MSG, sig)

    def test_wrong_message_fails(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        sig = frost.sign([shares[0], shares[1]], MSG, A)
        with self.assertRaises(Exception):
            VerifyKey(A).verify(b"element=amount value=2 recipient=X", sig)

    def test_tampered_signature_fails(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        sig = bytearray(frost.sign([shares[0], shares[1]], MSG, A))
        sig[40] ^= 0xFF
        with self.assertRaises(Exception):
            VerifyKey(A).verify(MSG, bytes(sig))

    def test_threshold_five_of_seven(self):
        shares, A = frost.keygen_dealer(n=7, t=5)
        VerifyKey(A).verify(MSG, frost.sign(shares[:5], MSG, A))
        with self.assertRaises(Exception):      # 4 < 5 — not enough
            VerifyKey(A).verify(MSG, frost.sign(shares[:4], MSG, A))


class TestVerifySideUnchanged(unittest.TestCase):
    """AD-30: a FROST signature drops into OUR verify_envelope_v2 with no edits."""

    def _frost_envelope(self, data, signers, group_pub):
        data = unicodedata.normalize("NFC", data)
        manifest = {"origin": "orig", "created_at": "2026-07-23",
                    "cp_len": len(data),
                    "sha256": hashlib.sha256(data.encode()).hexdigest(),
                    "anchor": None}
        body = {"v": 2, "data": data, "manifest": manifest}
        sig = frost.sign(signers, _canonical(body), group_pub)
        return {**body, "sig": sig.hex(), "signer_pub": group_pub.hex()}

    def test_frost_envelope_accepted_by_unmodified_verify(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        env = self._frost_envelope("сумма=1000 получатель=CompanyA",
                                   [shares[0], shares[1]], A)
        self.assertEqual(verify_envelope_v2(env)["status"], "VERIFIED")

    def test_frost_envelope_tamper_detected(self):
        shares, A = frost.keygen_dealer(n=3, t=2)
        env = self._frost_envelope("сумма=1000 получатель=CompanyA",
                                   [shares[0], shares[1]], A)
        env["data"] = "сумма=9999 получатель=Attacker"   # content substitution
        self.assertNotEqual(verify_envelope_v2(env)["status"], "VERIFIED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
