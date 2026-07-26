"""Tests of the v2 core: the Ed25519 envelope and the context-aware scanner.

The negative tests record that v2 closes defect #2 of the catalog (forgery
of a "signature" by the other side) and candidly does NOT close #1 and #3
(self-attestation of content, self-declaration of time).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.envelope_v2 import (  # noqa: E402
    generate_keypair, make_envelope_v2, verify_envelope_v2,
)
from notarius.scanner import scan  # noqa: E402

ZWSP = "​"
VS16 = "️"
T = "2026-07-22T12:00:00Z"


class TestEnvelopeV2(unittest.TestCase):

    def setUp(self):
        self.priv, self.pub = generate_keypair()

    def test_honest_envelope_verified(self):
        env = make_envelope_v2("1000", self.priv, "invoice_458", T)
        r = verify_envelope_v2(env, trusted_pub=self.pub)
        self.assertEqual(r["status"], "VERIFIED")

    def test_tamper_detected_by_any_third_party(self):
        # The verifier needs only the envelope — no private key.
        env = make_envelope_v2("1000", self.priv, "invoice_458", T)
        env["data"] = "9000"
        self.assertEqual(verify_envelope_v2(env)["status"],
                         "SIGNATURE_INVALID")

    def test_receiver_cannot_forge_senders_signature(self):
        # Defect #2 is closed: the receiver has only the public key and
        # cannot re-sign the altered data with the sender's key.
        env = make_envelope_v2("1000", self.priv, "invoice_458", T)
        attacker_priv, _ = generate_keypair()
        forged = make_envelope_v2("9000", attacker_priv, "invoice_458", T)
        r = verify_envelope_v2(forged, trusted_pub=self.pub)
        self.assertEqual(r["status"], "SIGNER_UNTRUSTED")  # SIGNED != NATIVE

    def test_zwsp_insertion_detected_with_length_diagnostic(self):
        env = make_envelope_v2("1000", self.priv, "invoice_458", T)
        env["data"] = "10" + ZWSP + "00"
        r = verify_envelope_v2(env)
        self.assertEqual(r["status"], "SIGNATURE_INVALID")
        self.assertTrue(any("+1" in x for x in r["reasons"]))

    def test_defect1_not_closed_self_attestation(self):
        # Candid limit: the signer can sign a LIE — the envelope proves
        # integrity and signature authorship, not truthfulness.
        env = make_envelope_v2("amount 1000000", self.priv,
                               "origin_fake", T)
        self.assertEqual(verify_envelope_v2(env, self.pub)["status"],
                         "VERIFIED")  # a lie with a valid signature passes

    def test_defect3_time_is_self_declared(self):
        env = make_envelope_v2("1000", self.priv, "invoice_458",
                               "1999-01-01T00:00:00Z")  # false date
        r = verify_envelope_v2(env, self.pub)
        self.assertEqual(r["status"], "VERIFIED")
        self.assertTrue(any("self-declared" in x for x in r["reasons"]))

    def test_malformed_no_crash(self):
        self.assertEqual(verify_envelope_v2({"data": "x"})["status"],
                         "MALFORMED")


class TestScannerV2(unittest.TestCase):

    def test_clean_text(self):
        r = scan("Привет 1000")
        self.assertTrue(r["clean"])
        self.assertEqual(r["xray"], "Привет 1000")

    def test_inside_word_is_high_with_xray(self):
        r = scan("adm" + "﻿" + "in")  # BOM inside a word
        f = r["findings"][0]
        self.assertEqual(f["suspicion"], "HIGH")
        self.assertEqual(f["context"], "m[U+FEFF]i")
        self.assertEqual(r["xray"], "adm[U+FEFF]in")

    def test_boundary_is_medium(self):
        r = scan("абзац." + ZWSP + " Далее")
        self.assertEqual(r["findings"][0]["suspicion"], "MEDIUM")

    def test_variation_selector_not_flagged_as_attack(self):
        r = scan("☂" + VS16)  # emoji with VS16 — legitimate
        self.assertEqual(r["findings"][0]["suspicion"], "LIKELY_LEGITIMATE")
        self.assertEqual(r["counts"]["HIGH"], 0)

    def test_sorting_high_first(self):
        text = "x." + ZWSP + " y adm" + ZWSP + "in"
        r = scan(text)
        self.assertEqual(r["findings"][0]["suspicion"], "HIGH")
        self.assertEqual(r["findings"][1]["suspicion"], "MEDIUM")


if __name__ == "__main__":
    unittest.main(verbosity=2)
