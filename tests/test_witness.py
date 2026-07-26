"""Tests of the coverage boundary of SEMANTIC_INVISIBLE_LENGTH_WITNESS.

Positive tests confirm the claims of §6.3 ("catches").
Negative tests pin down in executable code what used to be only words in
the "does NOT catch" section — including a bypass not mentioned in the
document (insertion+deletion preserving length).
Then the same attacks are run against the signed envelope.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.witness import (  # noqa: E402
    block_with_witness, verify_witness,
    make_envelope, verify_envelope, find_invisibles,
)

ZWSP = "​"
KEY = b"demo-shared-secret"


class TestNaiveWitnessCatches(unittest.TestCase):
    """What the naive witness CATCHES — confirmation of the document's claims."""

    def test_honest_block_passes(self):
        self.assertTrue(verify_witness(block_with_witness("1000")))

    def test_zwsp_start(self):
        b = block_with_witness("1000")
        b["data"] = ZWSP + b["data"]
        self.assertFalse(verify_witness(b))

    def test_zwsp_middle(self):
        b = block_with_witness("1000")
        b["data"] = b["data"][:2] + ZWSP + b["data"][2:]
        self.assertFalse(verify_witness(b))

    def test_zwsp_end(self):
        b = block_with_witness("1000")
        b["data"] = b["data"] + ZWSP
        self.assertFalse(verify_witness(b))

    def test_bom_zwj_vs16(self):
        for ch in ("﻿", "‍", "️"):
            b = block_with_witness("1000")
            b["data"] += ch
            self.assertFalse(verify_witness(b), f"missed {ch!r}")


class TestNaiveWitnessBypassed(unittest.TestCase):
    """What the naive witness does NOT catch — the coverage boundary, in code."""

    def test_naive_witness_bypassed_by_updating_cp_len(self):
        # Self-attestation: the attacker changes data and cp_len in one move.
        b = block_with_witness("1000")
        b["data"] = "9" + ZWSP + "000000"
        b["cp_len"] = len(b["data"])
        self.assertTrue(verify_witness(b))  # the attack passed

    def test_equal_length_substitution_passes(self):
        # "1000" -> "2000": same length, the check stays silent (stated in §6.3).
        b = block_with_witness("1000")
        b["data"] = "2000"
        self.assertTrue(verify_witness(b))

    def test_insert_plus_delete_preserves_length(self):
        # NOT mentioned in §6.3: an invisible inserted, a visible one deleted.
        b = block_with_witness("1000")
        b["data"] = "100" + ZWSP  # length is still 4
        self.assertTrue(verify_witness(b))

    def test_missing_keys_raise(self):
        with self.assertRaises(KeyError):
            verify_witness({"data": "1000"})


class TestSignedEnvelope(unittest.TestCase):
    """The same attacks against the corrected envelope."""

    def test_honest_envelope_verified(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        self.assertEqual(verify_envelope(env, KEY)["status"], "VERIFIED")

    def test_zwsp_insertion_detected_with_length_diagnostic(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        env["data"] = "10" + ZWSP + "00"
        r = verify_envelope(env, KEY)
        self.assertEqual(r["status"], "SIGNATURE_INVALID")
        # Diagnostic value of length: the report names the shift +1.
        self.assertTrue(any("+1" in reason for reason in r["reasons"]))
        self.assertEqual(r["invisibles"][0]["codepoint"], "U+200B")

    def test_cp_len_rewrite_detected(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        env["data"] = "9" + ZWSP + "000000"
        env["manifest"]["cp_len"] = len(env["data"])
        self.assertEqual(verify_envelope(env, KEY)["status"],
                         "SIGNATURE_INVALID")

    def test_equal_length_substitution_detected(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        env["data"] = "2000"
        self.assertEqual(verify_envelope(env, KEY)["status"],
                         "SIGNATURE_INVALID")

    def test_insert_plus_delete_detected(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        env["data"] = "100" + ZWSP
        self.assertEqual(verify_envelope(env, KEY)["status"],
                         "SIGNATURE_INVALID")

    def test_malformed_envelope_no_crash(self):
        self.assertEqual(verify_envelope({"data": "1000"}, KEY)["status"],
                         "MALFORMED")

    def test_nfc_normalization_no_false_positive(self):
        # é in NFD (2 code points) is pinned as NFC (1) before counting —
        # legitimate normalization in transit gives no false alarm.
        env = make_envelope("résumé", KEY, origin="doc_1")
        self.assertEqual(env["manifest"]["cp_len"], 6)
        self.assertEqual(verify_envelope(env, KEY)["status"], "VERIFIED")

    def test_wrong_key_rejected(self):
        env = make_envelope("1000", KEY, origin="invoice_458")
        self.assertEqual(verify_envelope(env, b"other-key")["status"],
                         "SIGNATURE_INVALID")


class TestInvisibleScan(unittest.TestCase):

    def test_clean_text_empty(self):
        self.assertEqual(find_invisibles("Hello 1000"), [])

    def test_reports_position_and_name(self):
        found = find_invisibles("10" + ZWSP + "00")
        self.assertEqual(found, [{"index": 2, "codepoint": "U+200B",
                                  "name": "ZERO WIDTH SPACE"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
