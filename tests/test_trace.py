"""Tests of semantic tracing (Notarius core, §9/§16/§17).

Positive: an honest trace → INTACT.
Negative: a chain break, an unexpected value change, a foreign key, a
forged event — all localized with the step and the last signer. Plus a
candid-limit test: a signed false event passes the signature check
(self-attestation is not closed — only localized).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.envelope_v2 import generate_keypair  # noqa: E402
from notarius.trace import (  # noqa: E402
    new_trace, append_event, verify_trace, human_report,
)

T0, T1, T2 = "2026-07-22T10:00:00Z", "2026-07-22T11:00:00Z", "2026-07-22T12:00:00Z"


class TestSemanticTrace(unittest.TestCase):

    def setUp(self):
        self.a_priv, self.a_pub = generate_keypair()   # accountant
        self.b_priv, self.b_pub = generate_keypair()   # checker
        self.trusted = {"accountant-17": self.a_pub, "checker-3": self.b_pub}

    def _honest_trace(self):
        tr = new_trace("amount", "1000", "invoice_458",
                       "accountant-17", self.a_priv, T0)
        tr = append_event(tr, "1000", "REVIEWED", "checker-3", self.b_priv, T1)
        return tr

    def test_honest_trace_intact(self):
        r = verify_trace(self._honest_trace(), self.trusted, current_value="1000")
        self.assertEqual(r["status"], "INTACT")
        self.assertEqual(r["state"], "INTACT")

    def test_legit_transformation_ok(self):
        tr = new_trace("amount", "1000", "invoice_458",
                       "accountant-17", self.a_priv, T0)
        tr = append_event(tr, "1200", "TRANSFORMED", "accountant-17",
                          self.a_priv, T1)  # the value may change on TRANSFORMED
        r = verify_trace(tr, self.trusted, current_value="1200")
        self.assertEqual(r["status"], "INTACT")

    def test_unexpected_change_on_review_detected(self):
        tr = new_trace("amount", "1000", "invoice_458",
                       "accountant-17", self.a_priv, T0)
        # REVIEWED must not change the value — but the checker signed a new one
        tr = append_event(tr, "9000", "REVIEWED", "checker-3", self.b_priv, T1)
        r = verify_trace(tr, self.trusted, current_value="9000")
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")
        self.assertEqual(r["state"], "MODIFIED")
        self.assertEqual(r["break_at_step"], 1)

    def test_chain_break_detected(self):
        tr = self._honest_trace()
        tr[0]["value_hash"] = "deadbeef"  # corrupting the first event breaks the link
        r = verify_trace(tr, self.trusted)
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")

    def test_untrusted_key_flagged(self):
        tr = self._honest_trace()
        r = verify_trace(tr, trusted_keys={"accountant-17": self.a_pub})  # no checker-3
        self.assertEqual(r["state"], "ORIGIN_UNKNOWN")

    def test_current_value_mismatch(self):
        r = verify_trace(self._honest_trace(), self.trusted, current_value="9000")
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")
        self.assertEqual(r["state"], "MODIFIED")

    def test_forged_event_signature_fails(self):
        tr = self._honest_trace()
        tr[1]["value_hash"] = _tamper = "0" * 64  # body changed, signature unchanged
        r = verify_trace(tr, self.trusted)
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")

    def test_self_attestation_not_closed(self):
        # Candid limit: an actor signs THEIR OWN lie — the signature is valid,
        # the trace does NOT refute it, it only records WHO signed.
        tr = new_trace("amount", "amount understated", "invoice_fake",
                       "accountant-17", self.a_priv, T0)
        r = verify_trace(tr, self.trusted, current_value="amount understated")
        self.assertEqual(r["status"], "INTACT")   # a lie with a valid signature passes
        self.assertEqual(r["last_signer"], "accountant-17")  # but who — is known

    def test_truncation_detected_with_expected_head(self):
        # AD-22: truncation is caught ONLY with an independently known head.
        from notarius.trace import _event_digest
        full = self._honest_trace()
        full = append_event(full, "1000", "TRANSFERRED", "accountant-17",
                            self.a_priv, T2)
        head = _event_digest(full[-1])
        truncated = full[:2]  # cut off the tail
        # without expected_head the truncated prefix looks valid:
        self.assertEqual(verify_trace(truncated, self.trusted)["status"], "INTACT")
        # with expected_head — it is detected:
        r = verify_trace(truncated, self.trusted, expected_head=head)
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")

    def test_intact_warns_without_head(self):
        r = verify_trace(self._honest_trace(), self.trusted)
        self.assertTrue(any("expected_head" in x for x in r["reasons"]))

    def test_human_report_renders(self):
        r = verify_trace(self._honest_trace(), self.trusted)
        text = human_report(r)
        self.assertIn("element: amount", text)
        self.assertIn("status: INTACT", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
