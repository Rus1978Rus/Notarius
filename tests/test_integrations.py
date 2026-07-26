"""Tests of the real integrations (AD-31).

Reed-Solomon — fully offline, ACTUALLY tested.
OpenTimestamps — only the offline part (creating the object); anchoring
and verification need the network / a Bitcoin node and are NOT tested here
(candidly).

Skipped entirely if the libraries are not installed (pip install
reedsolo opentimestamps).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from notarius.integrations import (
        rs_protect, rs_recover, rs_recoverable, ots_new, ots_digest_of,
    )
    _HAVE = True
except ImportError:
    _HAVE = False

DATA = b"element=amount value=1000000 recipient=CompanyA"


@unittest.skipUnless(_HAVE, "reedsolo/opentimestamps not installed")
class TestReedSolomon(unittest.TestCase):

    def test_roundtrip_undamaged(self):
        self.assertEqual(rs_recover(rs_protect(DATA)), DATA)

    def test_recovers_within_budget(self):
        # parity=16 → fixes up to 8 corrupted bytes; we corrupt 6.
        prot = bytearray(rs_protect(DATA, parity=16))
        for i in (2, 5, 9, 14, 20, 25):
            prot[i] ^= 0xFF
        self.assertEqual(rs_recover(bytes(prot), 16), DATA)

    def test_fails_beyond_budget(self):
        # corrupt 10 bytes (> 8) — candidly not recoverable.
        prot = bytearray(rs_protect(DATA, parity=16))
        for i in range(0, 20, 2):
            prot[i] ^= 0xFF
        self.assertFalse(rs_recoverable(bytes(prot), 16))

    def test_parity_size(self):
        self.assertEqual(len(rs_protect(DATA, parity=16)), len(DATA) + 16)


@unittest.skipUnless(_HAVE, "reedsolo/opentimestamps not installed")
class TestOpenTimestampsOffline(unittest.TestCase):

    def test_object_carries_digest(self):
        d = ots_digest_of(DATA)
        ts = ots_new(d)
        self.assertEqual(ts.msg, d)

    def test_rejects_non_sha256(self):
        with self.assertRaises(ValueError):
            ots_new(b"short")

    # ANCHORING (ots_stamp) and VERIFICATION are not tested: they need the
    # network and a Bitcoin node (HONEST_LIMIT). We don't pass the untested off as working.


if __name__ == "__main__":
    unittest.main(verbosity=2)
