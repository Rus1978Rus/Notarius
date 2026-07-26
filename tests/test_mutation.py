# -*- coding: utf-8 -*-
"""Mutation adequacy + content screening for verify (AD-33).

Discipline from "Vakhter" (gate_selftest): "a gate that cannot be failed
is not a gate". We prove our verifiers can REALLY reject: we mutate every
signed field → verify must catch it. Plus a negative control (unmutated passes).

And we check the wiring of scan_hardened as a CONTENT AXIS: the chain/carrier
may be crypto-valid while the value is poisoned by a zero-width char
(CONTAINER_INTACT ≠ ELEMENT_CLEAN).
"""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey

from notarius import trace as T
from notarius.carrier import issue_carrier, CarrierValidator
from notarius.envelope_v2 import (
    make_envelope_v2, verify_envelope_v2, generate_keypair,
)

ZWSP = "​"
ALICE = bytes(SigningKey.generate())
BOB = bytes(SigningKey.generate())


def _build_trace(value="administrator"):
    tr = T.new_trace("el-1", value, "origin-A", "alice", ALICE,
                     "2026-07-23T10:00:00Z")
    tr = T.append_event(tr, value, "REVIEWED", "bob", BOB,
                        "2026-07-23T11:00:00Z")
    return tr


class TestTraceMutationAdequacy(unittest.TestCase):
    """Every signed field → mutation → verify must catch it."""

    def test_negative_control_intact(self):
        # The gate MUST let clean through — otherwise the test below is meaningless.
        r = T.verify_trace(_build_trace())
        self.assertEqual(r["status"], "INTACT")

    def test_every_signed_field_mutation_caught(self):
        base = _build_trace()
        body_fields = ("element_id", "type", "origin", "actor",
                       "value_hash", "cp_len", "at", "prev_hash")
        other_pub = bytes(SigningKey.generate().verify_key).hex()
        caught, checked = 0, 0
        for idx in range(len(base)):
            for field in body_fields + ("sig", "actor_pub"):
                tr = copy.deepcopy(base)
                cur = tr[idx][field]
                if field == "cp_len":
                    tr[idx][field] = (cur or 0) + 1
                elif field == "value_hash":
                    tr[idx][field] = "0" * 64
                elif field == "sig":
                    tr[idx][field] = "0" * 128
                elif field == "actor_pub":
                    tr[idx][field] = other_pub
                elif field == "prev_hash":
                    tr[idx][field] = "0" * 64 if cur is None else "0" * 64
                else:
                    tr[idx][field] = (cur or "") + "_MUT"
                checked += 1
                r = T.verify_trace(tr)
                if r["status"] == "TRACE_BREAK_DETECTED":
                    caught += 1
                else:
                    self.fail(f"mutation of event[{idx}].{field} NOT caught "
                              f"→ status={r['status']} (falsely-green gate!)")
        self.assertEqual(caught, checked)
        self.assertGreaterEqual(checked, 20)   # 2 events × 10 fields


class TestCarrierMutationAdequacy(unittest.TestCase):
    """Mutation of a signed carrier → validate must NOT return VALID."""

    def _fresh(self):
        key = b"k" * 32
        c = issue_carrier({"to": "CompanyA", "amount": 1000}, key,
                          issued_at=1000, ttl_seconds=60)
        return key, c

    def test_negative_control_valid(self):
        key, c = self._fresh()
        self.assertEqual(CarrierValidator(key).validate(c, now=1010)["status"],
                         "VALID")

    def test_every_signed_field_mutation_rejected(self):
        for field in ("payload", "issued_at", "expires_at", "nonce", "sig"):
            key, c = self._fresh()
            m = copy.deepcopy(c)
            if field == "payload":
                m[field] = {"to": "AttackerB", "amount": 999999}
            elif field in ("issued_at", "expires_at"):
                m[field] = m[field] + 1
            else:
                m[field] = "0" * len(str(m[field]))
            status = CarrierValidator(key).validate(m, now=1010)["status"]
            self.assertNotEqual(status, "VALID",
                                f"mutation of {field} passed as VALID!")


class TestContentScreeningAxis(unittest.TestCase):
    """scan_hardened as a content axis: crypto-valid, but poisoned."""

    def test_trace_intact_but_content_poisoned(self):
        poisoned = "admin" + ZWSP + "istrator"   # zero-width char inside a word
        tr = _build_trace(poisoned)
        r = T.verify_trace(tr, current_value=poisoned)
        # the crypto is clean (signature valid, hash matches) ...
        self.assertEqual(r["status"], "INTACT")
        # ... but the content is poisoned — the axis caught it
        self.assertEqual(r["content_scan"]["risk"], "ALARM")
        self.assertEqual(r["content_scan"]["signature"], "zw_wordsplit")

    def test_trace_clean_content_ok(self):
        tr = _build_trace("administrator")
        r = T.verify_trace(tr, current_value="administrator")
        self.assertEqual(r["content_scan"]["risk"], "OK")

    def test_carrier_valid_but_content_poisoned(self):
        key = b"k" * 32
        c = issue_carrier({"to": "pay" + ZWSP + "pal", "amount": 1000},
                          key, issued_at=1000, ttl_seconds=60)
        res = CarrierValidator(key).validate(c, now=1010)
        self.assertEqual(res["status"], "VALID")           # the carrier is valid ...
        self.assertEqual(res["content_scan"]["risk"], "ALARM")  # ... the payload is poisoned
        self.assertIn("note", res)

    def test_carrier_clean_content_ok(self):
        key = b"k" * 32
        c = issue_carrier({"to": "CompanyA", "amount": 1000}, key,
                          issued_at=1000, ttl_seconds=60)
        res = CarrierValidator(key).validate(c, now=1010)
        self.assertEqual(res["content_scan"]["risk"], "OK")


class TestEnvelopeMutationAdequacy(unittest.TestCase):
    """Mutation of a signed v2 envelope → verify must NOT return VERIFIED."""

    def _env(self):
        priv, _pub = generate_keypair()
        return make_envelope_v2("amount=1000 recipient=CompanyA",
                                priv, "orig-A", "2026-07-23T10:00:00Z")

    def test_negative_control_verified(self):
        self.assertEqual(verify_envelope_v2(self._env())["status"], "VERIFIED")

    def test_top_level_field_mutation_caught(self):
        for field in ("v", "data", "sig", "signer_pub"):
            env = copy.deepcopy(self._env())
            if field == "v":
                env[field] = 999
            elif field == "sig":
                env[field] = "0" * 128
            elif field == "signer_pub":
                env[field] = bytes(SigningKey.generate().verify_key).hex()
            else:
                env[field] = str(env[field]) + "_MUT"
            self.assertNotEqual(verify_envelope_v2(env)["status"], "VERIFIED",
                                f"mutation of {field} passed as VERIFIED!")

    def test_manifest_field_mutation_caught(self):
        for field in ("origin", "created_at", "cp_len", "sha256", "anchor"):
            env = copy.deepcopy(self._env())
            cur = env["manifest"][field]
            if field == "cp_len":
                env["manifest"][field] = (cur or 0) + 1
            elif field == "anchor":
                env["manifest"][field] = "FAKE_ANCHOR"
            else:
                env["manifest"][field] = str(cur) + "_MUT"
            self.assertNotEqual(verify_envelope_v2(env)["status"], "VERIFIED",
                                f"mutation of manifest.{field} passed as VERIFIED!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
