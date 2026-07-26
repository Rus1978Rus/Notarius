"""Tests of the mortal carrier validator (PROVENANCE_CARRIER, AD-29).

Proves executably: a copy of the carrier is useless — either expired
(short life) or already redeemed (single-use).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.carrier import issue_carrier, CarrierValidator  # noqa: E402

KEY = b"demo-carrier-key"
PAYLOAD = {"element": "amount", "value": "1000000", "trace_ok": True}
T0 = 1_000_000  # moment of issuance (seconds)


class TestMortalCarrier(unittest.TestCase):

    def setUp(self):
        self.v = CarrierValidator(KEY)

    def test_valid_within_window(self):
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        r = self.v.validate(c, now=T0 + 30)
        self.assertEqual(r["status"], "VALID")
        self.assertEqual(r["payload"], PAYLOAD)

    def test_expired_copy_is_useless(self):
        # The thief photographed the QR, presented it 2 minutes later — expired.
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        r = self.v.validate(c, now=T0 + 120)
        self.assertEqual(r["status"], "EXPIRED")

    def test_second_use_rejected(self):
        # Single-use: the copy is presented twice in the window — the second is refused.
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        self.assertEqual(self.v.validate(c, now=T0 + 5)["status"], "VALID")
        r = self.v.validate(c, now=T0 + 6)
        self.assertEqual(r["status"], "ALREADY_USED")

    def test_tampered_payload_fails(self):
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        c["payload"]["value"] = "9000000"          # amount swapped in the carrier
        self.assertEqual(self.v.validate(c, now=T0 + 5)["status"],
                         "SIGNATURE_INVALID")

    def test_not_yet_valid(self):
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        self.assertEqual(self.v.validate(c, now=T0 - 10)["status"],
                         "NOT_YET_VALID")

    def test_wrong_key_rejected(self):
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        other = CarrierValidator(b"other-key")
        self.assertEqual(other.validate(c, now=T0 + 5)["status"],
                         "SIGNATURE_INVALID")

    def test_malformed(self):
        self.assertEqual(self.v.validate({"payload": {}}, now=T0)["status"],
                         "MALFORMED")

    def test_copy_useless_both_ways(self):
        # Full demonstration: the copy either expires or burns.
        c = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        stolen = dict(c)                            # the thief copied the carrier
        self.v.validate(c, now=T0 + 10)             # the owner used it
        # the copy is in the window — already redeemed:
        self.assertEqual(self.v.validate(stolen, now=T0 + 11)["status"],
                         "ALREADY_USED")
        # a fresh copy, but outside the window — expired:
        fresh_stolen = issue_carrier(PAYLOAD, KEY, issued_at=T0, ttl_seconds=60)
        self.assertEqual(self.v.validate(fresh_stolen, now=T0 + 200)["status"],
                         "EXPIRED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
