"""Tests of the algorithms for signing/identifying segments and the whole."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algorithms.merkle_segments import (  # noqa: E402
    root, inclusion_proof, verify_segment, signed_root,
)
from algorithms.human_fingerprint import (  # noqa: E402
    word_fingerprint, fingerprints_match,
    make_redundant_id, recover_id, positional_check,
)

SEGMENTS = [b"amount=1000", b"iban=UA123", b"recipient=CompanyA",
            b"date=2026-07-22", b"status=APPROVED"]


class TestMerkleSegments(unittest.TestCase):

    def test_segment_proof_verifies(self):
        r = root(SEGMENTS)
        for i, seg in enumerate(SEGMENTS):
            proof = inclusion_proof(SEGMENTS, i)
            self.assertTrue(verify_segment(seg, i, proof, r), f"seg {i}")

    def test_tampered_segment_fails(self):
        r = root(SEGMENTS)
        proof = inclusion_proof(SEGMENTS, 0)
        self.assertFalse(verify_segment(b"amount=9000", 0, proof, r))

    def test_proof_without_other_segments(self):
        # The verifier has ONLY segment 2 and its proof — not the whole set.
        r = root(SEGMENTS)
        proof = inclusion_proof(SEGMENTS, 2)
        self.assertTrue(verify_segment(SEGMENTS[2], 2, proof, r))

    def test_whole_identity_changes_if_any_segment_changes(self):
        r1 = root(SEGMENTS)
        altered = list(SEGMENTS)
        altered[3] = b"date=1999-01-01"
        self.assertNotEqual(r1, root(altered))

    def test_single_segment(self):
        r = root([b"solo"])
        self.assertTrue(verify_segment(b"solo", 0, inclusion_proof([b"solo"], 0), r))

    def test_cve_2012_2459_no_collision(self):
        # Regression: duplicating the last segment must NOT yield the same
        # root (a bug of the previous version, found in a blind review).
        self.assertNotEqual(root([b"A", b"B", b"C"]),
                            root([b"A", b"B", b"C", b"C"]))

    def test_odd_counts_all_segments_verify(self):
        for n in (3, 5, 7, 9):
            segs = [f"s{i}".encode() for i in range(n)]
            r = root(segs)
            for i, seg in enumerate(segs):
                self.assertTrue(verify_segment(seg, i, inclusion_proof(segs, i), r),
                                f"n={n} i={i}")

    def test_signed_root_binds_size(self):
        # Completeness: signing the pair (root, size) distinguishes sets of different size.
        self.assertNotEqual(signed_root([b"A", b"B", b"C"]),
                            signed_root([b"A", b"B", b"C", b"C"]))


class TestHumanFingerprint(unittest.TestCase):

    def test_deterministic(self):
        self.assertEqual(word_fingerprint(b"hello"), word_fingerprint(b"hello"))

    def test_cross_substrate_match(self):
        # The same content on the "screen" and on "stone" → the fingerprints match.
        on_screen = word_fingerprint(b"amount=1000")
        on_stone = word_fingerprint(b"amount=1000")
        self.assertTrue(fingerprints_match(on_screen, on_stone))

    def test_change_flips_fingerprint(self):
        self.assertFalse(fingerprints_match(
            word_fingerprint(b"amount=1000"), word_fingerprint(b"amount=2000")))

    def test_fingerprint_words_from_list(self):
        from algorithms.human_fingerprint import WORDLIST
        for w in word_fingerprint(b"x", words=6):
            self.assertIn(w, WORDLIST)


class TestRedundantId(unittest.TestCase):

    def test_roundtrip(self):
        self.assertEqual(recover_id(make_redundant_id("E-145")), "E-145")

    def test_survives_partial_damage(self):
        rid = make_redundant_id("E-145", copies=3)
        parts = rid.split("|")
        damaged = "XXcorruptedXX|" + parts[2]  # two copies destroyed
        self.assertEqual(recover_id(damaged), "E-145")

    def test_all_copies_destroyed_returns_none(self):
        self.assertIsNone(recover_id("garbage|more#99garbage"))

    def test_checksum_catches_altered_id(self):
        rid = make_redundant_id("E-145")
        forged = rid.replace("E-145", "E-999")  # id changed, checksum not recomputed
        self.assertIsNone(recover_id(forged))

    def test_positional_manual(self):
        # The positional check is computable by hand: sum((i+1)*code) mod 97.
        self.assertEqual(positional_check("AB"), (1 * 65 + 2 * 66) % 97)

    def test_positional_catches_transposition(self):
        # The key fix AD-22: AB and BA are now DISTINGUISHED.
        self.assertNotEqual(positional_check("AB"), positional_check("BA"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
