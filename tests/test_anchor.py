# -*- coding: utf-8 -*-
"""Tests of the public anchor "registry under glass" (AD-49).

The author's metaphor: the thief draws on the GLASS (the presented copy),
not on the registry. Pull the registry out, reconcile — the drawing on the
glass is exposed.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey

from notarius.anchor import PublicAnchor, reconcile, anchor_ots_digest
from notarius.title import (
    brand, attest, resolve_hybrid, TitleRegistry,
)

DATA = b"contract=deed-42 asset=painting"
OWNER = bytes(SigningKey.generate())
THIEF = bytes(SigningKey.generate())


class TestPublicAnchor(unittest.TestCase):

    def test_append_and_pull_first(self):
        a = PublicAnchor()
        a.append(DATA, "Ruslan", "t0")
        self.assertEqual(a.pull(DATA)["owner_id"], "Ruslan")

    def test_first_wins_later_does_not_overwrite(self):
        a = PublicAnchor()
        a.append(DATA, "Ruslan", "t0")
        a.append(DATA, "Thief", "t9")           # later on the same hash
        self.assertEqual(a.pull(DATA)["owner_id"], "Ruslan")

    def test_pull_missing_is_none(self):
        self.assertIsNone(PublicAnchor().pull(DATA))

    def test_integrity_intact(self):
        a = PublicAnchor()
        a.append(DATA, "Ruslan", "t0")
        a.append(b"other", "Bob", "t1")
        self.assertTrue(a.verify_integrity())

    def test_integrity_broken_by_secret_edit(self):
        a = PublicAnchor()
        a.append(DATA, "Ruslan", "t0")
        a.append(b"other", "Bob", "t1")
        a._log[0]["owner_id"] = "Thief"         # a secret edit of the past
        self.assertFalse(a.verify_integrity())

    def test_ots_digest_size(self):
        a = PublicAnchor()
        a.append(DATA, "Ruslan", "t0")
        self.assertEqual(len(anchor_ots_digest(a)), 32)


class TestGlassVsRegistry(unittest.TestCase):
    """Reconciling the glass with the registry: forgery on the glass is exposed."""

    def test_match(self):
        a = PublicAnchor(); a.append(DATA, "Ruslan", "t0")
        self.assertEqual(reconcile("Ruslan", DATA, a)["status"], "MATCH")

    def test_forgery_on_glass_caught(self):
        a = PublicAnchor(); a.append(DATA, "Ruslan", "t0")
        r = reconcile("Thief", DATA, a)          # the thief presents «Thief» (the glass)
        self.assertEqual(r["status"], "FORGERY_ON_GLASS")
        self.assertEqual(r["registry_owner"], "Ruslan")

    def test_not_anchored(self):
        self.assertEqual(reconcile("Anyone", DATA, PublicAnchor())["status"],
                         "NOT_ANCHORED")


class TestAnchorDefeatsFullMirror(unittest.TestCase):
    """The pulled registry catches a FULL mirror (both axes on the thief)."""

    def test_pulled_registry_overrides_mirror(self):
        # the registry (written early) holds the owner
        anchor = PublicAnchor(); anchor.append(DATA, "Ruslan", "2020-01-01")
        # the thief aligned BOTH axes on Thief (a full mirror)
        reg = TitleRegistry(bytes(SigningKey.generate()))
        b_t = brand(DATA, "Thief", THIEF, "2026")
        cs_t = [reg.witness(b_t)]
        tsrc = [bytes(SigningKey.generate()) for _ in range(2)]
        t_atts = [attest(DATA, "Thief", tsrc[i], f"t{i}", "2026") for i in range(2)]
        skeys = {x["source_pub"] for x in t_atts}
        # the verifier PULLS the registry out and supplies it as the external anchor
        pulled = anchor.pull(DATA)["owner_id"]
        h = resolve_hybrid(DATA, [(b_t, cs_t)], t_atts, {reg.pub.hex()},
                           brand_threshold=1, converge_min=2, source_keys=skeys,
                           external_anchor=pulled)
        self.assertEqual(h["confidence"], "CONTESTED")   # the mirror is exposed by the registry


if __name__ == "__main__":
    unittest.main(verbosity=2)
