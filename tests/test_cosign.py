# -*- coding: utf-8 -*-
"""Tests of witness co-signing (AD-36): closing fork/truncation (M4, AD-22).

Negative-test discipline: both what the witness CO-SIGNS (a legit
extension) and what it REFUSES (fork/truncation/rewritten prefix), and
how the verifier catches a fork against the witnessed head.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey

from notarius import trace as T
from notarius.cosign import (
    Witness, make_checkpoint, verify_checkpoint, verify_witnessed_trace,
)

ALICE = bytes(SigningKey.generate())
LOG = bytes(SigningKey.generate())


def _trace3():
    tr = T.new_trace("el", "v0", "orig", "alice", ALICE, "t0")
    tr = T.append_event(tr, "v0", "TRANSFORMED", "alice", ALICE, "t1")
    tr = T.append_event(tr, "v0", "REVIEWED", "alice", ALICE, "t2")
    return tr


class TestConsistentExtension(unittest.TestCase):

    def test_legit_cosign_and_verify(self):
        w = Witness(bytes(SigningKey.generate()))
        tr = _trace3()
        cp = make_checkpoint(tr, "log", LOG)
        cs = w.cosign(cp, tr)
        self.assertIsNotNone(cs)
        r = verify_witnessed_trace(tr, cp, [cs], {w.pub.hex()}, threshold=1)
        self.assertEqual(r["status"], "INTACT")
        self.assertTrue(r["witness"]["quorum_ok"])

    def test_extension_cosigned(self):
        w = Witness(bytes(SigningKey.generate()))
        tr2 = T.new_trace("el", "v0", "orig", "alice", ALICE, "t0")
        tr2 = T.append_event(tr2, "v0", "TRANSFORMED", "alice", ALICE, "t1")
        self.assertIsNotNone(w.cosign(make_checkpoint(tr2, "log", LOG), tr2))
        tr3 = T.append_event(tr2, "v0", "REVIEWED", "alice", ALICE, "t2")
        # a consistent extension — the witness co-signs
        self.assertIsNotNone(w.cosign(make_checkpoint(tr3, "log", LOG), tr3))


class TestForkDetection(unittest.TestCase):

    def _fork(self):
        base = T.new_trace("el", "v0", "orig", "alice", ALICE, "t0")
        a = T.append_event(base, "v0", "REVIEWED", "alice", ALICE, "t1")
        b = T.append_event(base, "v0-EVIL", "REVIEWED", "alice", ALICE, "t1")
        return a, b

    def test_witness_refuses_fork_at_same_height(self):
        w = Witness(bytes(SigningKey.generate()))
        a, b = self._fork()
        self.assertIsNotNone(w.cosign(make_checkpoint(a, "log", LOG), a))
        # a second branch of the same height with a different head → REFUSAL
        self.assertIsNone(w.cosign(make_checkpoint(b, "log", LOG), b))

    def test_verifier_catches_fork_against_witnessed_head(self):
        w = Witness(bytes(SigningKey.generate()))
        a, b = self._fork()
        cp_a = make_checkpoint(a, "log", LOG)
        cs_a = w.cosign(cp_a, a)                       # branch A is witnessed
        # the verifier takes the witnessed head of A and sees branch B
        r = verify_witnessed_trace(b, cp_a, [cs_a], {w.pub.hex()}, threshold=1)
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")

    def test_fork_branch_without_quorum_flagged(self):
        w = Witness(bytes(SigningKey.generate()))
        a, b = self._fork()
        w.cosign(make_checkpoint(a, "log", LOG), a)
        cp_b = make_checkpoint(b, "log", LOG)
        # branch B with its own head, but WITHOUT co-signatures → quorum not reached
        r = verify_witnessed_trace(b, cp_b, [], {w.pub.hex()}, threshold=1)
        self.assertFalse(r["witness"]["quorum_ok"])


class TestTruncationAndRewrite(unittest.TestCase):

    def test_truncation_detected_against_witnessed_head(self):
        w = Witness(bytes(SigningKey.generate()))
        tr = _trace3()
        cp3 = make_checkpoint(tr, "log", LOG)          # head at size 3
        cs3 = w.cosign(cp3, tr)
        # a valid PREFIX of size 2 is presented against the witnessed head at 3
        r = verify_witnessed_trace(tr[:2], cp3, [cs3], {w.pub.hex()}, threshold=1)
        self.assertEqual(r["status"], "TRACE_BREAK_DETECTED")

    def test_witness_refuses_rewritten_prefix(self):
        w = Witness(bytes(SigningKey.generate()))
        a2 = T.new_trace("el", "v0", "orig", "alice", ALICE, "t0")
        a2 = T.append_event(a2, "v0", "TRANSFORMED", "alice", ALICE, "t1")
        w.cosign(make_checkpoint(a2, "log", LOG), a2)  # remembered the head at size 2
        # a different prefix of size 2 (rewritten) → extend to 3 → REFUSAL
        b2 = T.new_trace("el", "v0-EVIL", "orig", "alice", ALICE, "t0")
        b2 = T.append_event(b2, "v0", "TRANSFORMED", "alice", ALICE, "t1")
        b3 = T.append_event(b2, "v0", "REVIEWED", "alice", ALICE, "t2")
        self.assertIsNone(w.cosign(make_checkpoint(b3, "log", LOG), b3))


class TestQuorumAndTamper(unittest.TestCase):

    def test_threshold_quorum(self):
        w1 = Witness(bytes(SigningKey.generate()))
        w2 = Witness(bytes(SigningKey.generate()))
        keys = {w1.pub.hex(), w2.pub.hex()}
        tr = _trace3()
        cp = make_checkpoint(tr, "log", LOG)
        cs1, cs2 = w1.cosign(cp, tr), w2.cosign(cp, tr)
        self.assertTrue(verify_checkpoint(cp, [cs1, cs2], keys, threshold=2)["ok"])
        self.assertFalse(verify_checkpoint(cp, [cs1], keys, threshold=2)["ok"])

    def test_tampered_cosignature_rejected(self):
        w = Witness(bytes(SigningKey.generate()))
        tr = _trace3()
        cp = make_checkpoint(tr, "log", LOG)
        cs = dict(w.cosign(cp, tr))
        cs["cosig"] = "0" * len(cs["cosig"])           # forged co-signature
        self.assertFalse(verify_checkpoint(cp, [cs], {w.pub.hex()}, threshold=1)["ok"])

    def test_untrusted_witness_not_counted(self):
        w = Witness(bytes(SigningKey.generate()))
        tr = _trace3()
        cp = make_checkpoint(tr, "log", LOG)
        cs = w.cosign(cp, tr)
        # the witness key is NOT in the trusted set → not counted
        self.assertFalse(verify_checkpoint(cp, [cs], set(), threshold=1)["ok"])

    def test_bad_log_signature_refused(self):
        w = Witness(bytes(SigningKey.generate()))
        tr = _trace3()
        cp = dict(make_checkpoint(tr, "log", LOG))
        cp["log_sig"] = "0" * len(cp["log_sig"])       # the log signature is broken
        self.assertIsNone(w.cosign(cp, tr))


if __name__ == "__main__":
    unittest.main(verbosity=2)
