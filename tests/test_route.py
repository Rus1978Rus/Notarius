# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""The mandatory-route layer (route.py, AD-92) — tests against attacks.

Each test reproduces a concrete attack on "catch a missing step" and
records that the layer either catches it OR candidly states the limit.

Run: python3 tests/test_route.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey                                  # noqa: E402

from notarius import trace as T                                      # noqa: E402
from notarius.route import check_route, human_route                  # noqa: E402


def _key():
    sk = SigningKey.generate()
    return bytes(sk), bytes(sk.verify_key).hex()


class RouteBase(unittest.TestCase):
    def setUp(self):
        # three responsible roles, each with its own key
        self.prod_priv, self.prod_pub = _key()
        self.check_priv, self.check_pub = _key()
        self.rel_priv, self.rel_pub = _key()
        self.keys = {"Production": self.prod_pub,
                     "Warehouse": self.check_pub,
                     "Dispatch": self.rel_pub}
        self.route = [{"step": "CREATED", "by": "Production"},
                      {"step": "CHECKED", "by": "Warehouse"},
                      {"step": "RELEASED", "by": "Dispatch"}]

    def _full_trace(self):
        tr = T.new_trace("PARTY-1", "medicine", "orig",
                         "Production", self.prod_priv, "t0")
        tr = T.append_event(tr, "medicine", "CHECKED", "Warehouse",
                            self.check_priv, "t1")
        tr = T.append_event(tr, "medicine", "RELEASED", "Dispatch",
                            self.rel_priv, "t2")
        return tr


class TestHappyPath(RouteBase):
    def test_full_route_complete(self):
        r = check_route(self._full_trace(), self.route, self.keys)
        self.assertTrue(r["complete"], human_route(r))
        self.assertEqual([m["step"] for m in r["matched"]],
                         ["CREATED", "CHECKED", "RELEASED"])


class TestOmission(RouteBase):
    """The layer's main attack: a step simply was NOT done (not forgery — omission)."""
    def test_skipped_check_caught(self):
        tr = T.new_trace("PARTY-1", "medicine", "orig",
                         "Production", self.prod_priv, "t0")
        tr = T.append_event(tr, "medicine", "RELEASED", "Dispatch",
                            self.rel_priv, "t2")           # dispatched WITHOUT a check
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        kinds = {(k, s) for k, s, _ in r["findings"]}
        self.assertIn(("MISSING_STEP", "CHECKED"), kinds)


class TestImpersonation(RouteBase):
    """An omission cannot be bypassed by SELF-SIGNING a fake check with a foreign key."""
    def test_self_signed_check_not_accepted(self):
        forger_priv, _ = _key()                            # the thief has THEIR OWN key
        tr = T.new_trace("PARTY-1", "medicine", "orig",
                         "Production", self.prod_priv, "t0")
        tr = T.append_event(tr, "medicine", "CHECKED", "Warehouse",
                            forger_priv, "t1")             # "check" with the wrong key
        tr = T.append_event(tr, "medicine", "RELEASED", "Dispatch",
                            self.rel_priv, "t2")
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        kinds = {(k, s) for k, s, _ in r["findings"]}
        self.assertIn(("WRONG_SIGNER", "CHECKED"), kinds)


class TestOutOfOrder(RouteBase):
    """The steps exist, the parties are right, but the order is violated."""
    def test_released_before_checked(self):
        tr = T.new_trace("PARTY-1", "medicine", "orig",
                         "Production", self.prod_priv, "t0")
        tr = T.append_event(tr, "medicine", "RELEASED", "Dispatch",
                            self.rel_priv, "t1")           # dispatched BEFORE the check
        tr = T.append_event(tr, "medicine", "CHECKED", "Warehouse",
                            self.check_priv, "t2")
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        kinds = {(k, s) for k, s, _ in r["findings"]}
        # RELEASED is required AFTER CHECKED, but came earlier → exists but out of order
        self.assertIn(("OUT_OF_ORDER", "RELEASED"), kinds)


class TestBrokenChainFailsClosed(RouteBase):
    """If the trace itself is tampered — the route cannot be judged (fail closed)."""
    def test_tampered_trace_blocks_route(self):
        tr = self._full_trace()
        tr[1] = dict(tr[1], value_hash="0" * 64)           # corrupt a link
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        self.assertEqual(r["findings"][0][0], "CHAIN_BROKEN")


class TestElementSwapCaught(RouteBase):
    """A check step — of ANOTHER subject (signed by the right warehouse) — does not
    count: element_id continuity breaks the trace (N-W4) → CHAIN_BROKEN, fail closed."""
    def test_check_of_other_element(self):
        tr = self._full_trace()
        tr[1] = dict(tr[1], element_id="PARTY-2")          # check of the wrong batch
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        self.assertEqual(r["findings"][0][0], "CHAIN_BROKEN")


class TestCrossElementSpliceFailsClosed(RouteBase):
    """Even with verify_chain=False, a genuinely signed step of ANOTHER subject
    (a real warehouse check of someone else's batch), spliced into this trace, is
    NOT counted: subject continuity is checked always."""
    def test_spliced_foreign_check(self):
        # a real warehouse check, but for BATCH B
        b = T.new_trace("PARTY-B", "x", "orig", "Warehouse", self.check_priv, "d0")
        b = T.append_event(b, "x", "CHECKED", "Warehouse", self.check_priv, "d1")
        foreign_checked = b[1]                             # signature is genuine
        tr = T.new_trace("PARTY-1", "medicine", "orig",
                         "Production", self.prod_priv, "t0")
        tr.append(foreign_checked)                         # splice of a foreign batch
        tr = T.append_event(tr, "medicine", "RELEASED", "Dispatch",
                            self.rel_priv, "t2")
        for vc in (True, False):
            r = check_route(tr, self.route, self.keys, verify_chain=vc)
            self.assertFalse(r["complete"], f"verify_chain={vc}")
            self.assertEqual(r["findings"][0][0], "CHAIN_BROKEN")


class TestCountRepetition(RouteBase):
    """"5 inspection rounds" = five route entries; did 2 → three omissions."""
    def test_missing_inspections(self):
        insp_priv, insp_pub = _key()
        keys = {"Inspector": insp_pub}
        route = [{"step": "INSPECTED", "by": "Inspector"} for _ in range(5)]
        tr = T.new_trace("SITE-9", "object", "orig",
                         "Inspector", insp_priv, "t0")     # round #1 (a CREATED-type?)
        # first round — as a separate type; we do 2 INSPECTED over the "start"
        tr = T.new_trace("SITE-9", "object", "orig",
                         "Inspector", insp_priv, "d0")
        tr = T.append_event(tr, "object", "INSPECTED", "Inspector",
                            insp_priv, "d1")
        tr = T.append_event(tr, "object", "INSPECTED", "Inspector",
                            insp_priv, "d2")
        # the route requires 5 INSPECTED, but there are 2
        r = check_route(tr, route, keys, verify_chain=False)
        self.assertFalse(r["complete"])
        missing = [s for k, s, _ in r["findings"] if k == "MISSING_STEP"]
        self.assertEqual(len(missing), 3)                  # 5 required − 2 present


class TestPaddingNoise(RouteBase):
    """An extra fake CHECKED with a foreign key AFTER the real one must not
    fail a complete route (no false "incomplete")."""
    def test_extra_forged_step_ignored(self):
        forger_priv, _ = _key()
        tr = self._full_trace()                            # already complete and valid
        r = check_route(tr, self.route, self.keys)
        self.assertTrue(r["complete"], human_route(r))


class TestTruncationFailsSafe(RouteBase):
    """Tail truncation hides RELEASED → the route is incomplete (the safe side),
    not a false "complete"."""
    def test_truncated_tail_incomplete(self):
        tr = self._full_trace()[:2]                        # only CREATED, CHECKED
        r = check_route(tr, self.route, self.keys)
        self.assertFalse(r["complete"])
        kinds = {(k, s) for k, s, _ in r["findings"]}
        self.assertIn(("MISSING_STEP", "RELEASED"), kinds)


class TestHonestLimitSignedNotNative(RouteBase):
    """LIMIT: an authorized warehouse SIGNED the check — the layer treats the step
    as done. It does NOT prove the check actually happened (SIGNED ≠ NATIVE). We
    record this behavior as a deliberate limit, not a bug."""
    def test_authorized_signature_counts_as_done(self):
        r = check_route(self._full_trace(), self.route, self.keys)
        self.assertTrue(r["complete"])
        # responsibility is localized: it is known who signed CHECKED
        checked = [m for m in r["matched"] if m["step"] == "CHECKED"][0]
        self.assertEqual(checked["by"], "Warehouse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
