# -*- coding: utf-8 -*-
"""Tests of the seal of ownership (AD-44): title survives a breach.

The main point: whoever breached/copied the DATA but holds no owner's key
does not obtain a witnessed title — reading ≠ ownership.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nacl.signing import SigningKey

from notarius.title import (
    brand, brand_valid, brand_witnessed, resolve_title,
    transfer, transfer_valid, TitleRegistry,
    attest, attest_valid, converge, resolve_hybrid, converge_weighted,
    resolve_full, human_verdict,
)
from notarius.anchor import PublicAnchor


def _src():
    p = bytes(SigningKey.generate())
    return p, bytes(SigningKey(p).verify_key).hex()

DATA = b"contract=deed-42 asset=painting secret-content"
OWNER = bytes(SigningKey.generate())
THIEF = bytes(SigningKey.generate())


def _witnesses(n=2):
    ws = [TitleRegistry(bytes(SigningKey.generate())) for _ in range(n)]
    return ws, {w.pub.hex() for w in ws}


class TestBrandAndWitness(unittest.TestCase):

    def test_brand_valid(self):
        self.assertTrue(brand_valid(brand(DATA, "Ruslan", OWNER, "t0")))

    def test_witness_signs_first_refuses_conflict(self):
        ws, _ = _witnesses(1)
        w = ws[0]
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        self.assertIsNotNone(w.witness(b_owner))              # first seal — ok
        b_thief = brand(DATA, "Thief", THIEF, "t1")           # same hash, different owner
        self.assertIsNone(w.witness(b_thief))                 # → REFUSE

    def test_quorum_threshold(self):
        ws, keys = _witnesses(2)
        b = brand(DATA, "Ruslan", OWNER, "t0")
        cs = [ws[0].witness(b), ws[1].witness(b)]
        self.assertTrue(brand_witnessed(b, cs, keys, threshold=2))
        self.assertFalse(brand_witnessed(b, cs[:1], keys, threshold=2))

    def test_invalid_brand_not_witnessed(self):
        ws, _ = _witnesses(1)
        b = brand(DATA, "Ruslan", OWNER, "t0")
        b["sig"] = "0" * 128                                  # forgery of the owner's signature
        self.assertIsNone(ws[0].witness(b))


class TestReadingIsNotOwnership(unittest.TestCase):
    """Core: breach/copy of the data ≠ title."""

    def test_thief_with_bytes_only_loses_title(self):
        ws, keys = _witnesses(2)
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        cs_owner = [ws[0].witness(b_owner), ws[1].witness(b_owner)]

        # the THIEF breached the cipher, copied DATA, seals it with their own key
        b_thief = brand(DATA, "Thief", THIEF, "t1")
        cs_thief = [w.witness(b_thief) for w in ws]           # witnesses refused → None
        cs_thief = [c for c in cs_thief if c]

        r = resolve_title(DATA, [(b_owner, cs_owner), (b_thief, cs_thief)], keys, threshold=2)
        self.assertEqual(r["title_holders"], ["Ruslan"])
        self.assertIn("Thief", r["refuted"])

    def test_thief_cannot_replay_owner_cosignatures(self):
        # the thief takes THEIR OWN seal but slips in the co-signatures issued to the owner
        ws, keys = _witnesses(2)
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        cs_owner = [ws[0].witness(b_owner), ws[1].witness(b_owner)]
        b_thief = brand(DATA, "Thief", THIEF, "t1")
        # co-signatures over the owner's body do not validate the thief's body
        self.assertFalse(brand_witnessed(b_thief, cs_owner, keys, threshold=1))


class TestConsentedTransfer(unittest.TestCase):

    def test_two_sided_transfer_valid(self):
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        buyer = bytes(SigningKey.generate())
        self.assertTrue(transfer_valid(transfer(b_owner, OWNER, "Buyer", buyer, "t2")))

    def test_forged_transfer_invalid(self):
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        buyer = bytes(SigningKey.generate())
        t = transfer(b_owner, OWNER, "Buyer", buyer, "t2")
        t["from_sig"] = "0" * 128                             # the giver's side is forged
        self.assertFalse(transfer_valid(t))

    def test_one_sided_missing_acceptance_invalid(self):
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        buyer = bytes(SigningKey.generate())
        t = transfer(b_owner, OWNER, "Buyer", buyer, "t2")
        t["to_sig"] = "0" * 128                               # no consent from the receiver
        self.assertFalse(transfer_valid(t))


class TestSemanticConvergence(unittest.TestCase):
    """AD-46: title by the COHERENCE of a distributed history, not by 1 signature."""

    def _sources(self, n):
        return [bytes(SigningKey.generate()) for _ in range(n)]

    def test_partial_key_break_does_not_flip_title(self):
        # the owner has 3 independent records; the thief broke 1 key and forged 1
        srcs = self._sources(3)
        atts = [attest(DATA, "Ruslan", srcs[i], f"src-{i}", f"2026-07-2{i}") for i in range(3)]
        atts.append(attest(DATA, "Thief", bytes(SigningKey.generate()), "evil", "2026-07-25"))
        c = converge(DATA, atts, min_sources=2)
        self.assertEqual(c["title_holder"], "Ruslan")
        self.assertEqual(c["scores"]["Ruslan"]["independent_sources"], 3)

    def test_tie_is_contested(self):
        so, st = self._sources(2), self._sources(2)
        atts = [attest(DATA, "Ruslan", so[i], f"o{i}", "t0") for i in range(2)]
        atts += [attest(DATA, "Thief", st[i], f"e{i}", "t0") for i in range(2)]
        c = converge(DATA, atts, min_sources=1)
        self.assertTrue(c["contested"])
        self.assertIsNone(c["title_holder"])

    def test_same_source_counts_once(self):
        s = self._sources(1)[0]
        atts = [attest(DATA, "Ruslan", s, "src-0", f"t{i}") for i in range(5)]
        c = converge(DATA, atts, min_sources=1)
        self.assertEqual(c["scores"]["Ruslan"]["independent_sources"], 1)

    def test_min_sources_enforced(self):
        s = self._sources(1)[0]
        c = converge(DATA, [attest(DATA, "Ruslan", s, "src-0", "t0")], min_sources=2)
        self.assertIsNone(c["title_holder"])

    def test_invalid_attestation_not_counted(self):
        s = self._sources(1)[0]
        a = attest(DATA, "Ruslan", s, "src-0", "t0")
        a["sig"] = "0" * 128
        self.assertFalse(attest_valid(a))
        c = converge(DATA, [a], min_sources=1)
        self.assertEqual(c["scores"], {})


class TestHybrid(unittest.TestCase):
    """AD-47: hybrid of two axes; divergence of the axes = a signal (not a quiet handover)."""

    def _setup(self, n_src=3):
        ws, keys = _witnesses(2)
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        cs_owner = [w.witness(b_owner) for w in ws]
        srcs = [bytes(SigningKey.generate()) for _ in range(n_src)]
        owner_atts = [attest(DATA, "Ruslan", srcs[i], f"src-{i}", f"t{i}") for i in range(n_src)]
        return ws, keys, b_owner, cs_owner, owner_atts

    def test_both_axes_agree_confirmed(self):
        ws, keys, b, cs, atts = self._setup()
        h = resolve_hybrid(DATA, [(b, cs)], atts, keys, brand_threshold=2, converge_min=2)
        self.assertEqual(h["confidence"], "CONFIRMED")
        self.assertEqual(h["holder"], "Ruslan")

    def test_digital_break_caught_as_contested(self):
        # the thief broke the digital axis (their own witnessed seal),
        # but the semantics holds the owner → CONTESTED, not a quiet handover to the thief
        _, _, _, _, owner_atts = self._setup()
        evil_reg = TitleRegistry(bytes(SigningKey.generate()))
        b_evil = brand(DATA, "Thief", THIEF, "t9")
        cs_evil = [evil_reg.witness(b_evil)]
        h = resolve_hybrid(DATA, [(b_evil, cs_evil)], owner_atts,
                           {evil_reg.pub.hex()}, brand_threshold=1, converge_min=2)
        self.assertEqual(h["confidence"], "CONTESTED")
        self.assertIsNone(h["holder"])

    def test_sybil_caught_as_contested(self):
        # the thief fabricates many records (semantics=Thief), but the owner has the seal
        ws, keys, b_owner, cs_owner, _ = self._setup()
        sybil = [attest(DATA, "Thief", bytes(SigningKey.generate()), f"fake-{i}", "t0")
                 for i in range(4)]
        h = resolve_hybrid(DATA, [(b_owner, cs_owner)], sybil, keys,
                           brand_threshold=2, converge_min=2)
        self.assertEqual(h["confidence"], "CONTESTED")

    def test_digital_only_provisional(self):
        ws, keys, b, cs, _ = self._setup()
        h = resolve_hybrid(DATA, [(b, cs)], [], keys, brand_threshold=2, converge_min=2)
        self.assertEqual(h["confidence"], "PROVISIONAL")
        self.assertEqual(h["holder"], "Ruslan")

    def test_semantic_only_provisional(self):
        _, keys, _, _, atts = self._setup()
        h = resolve_hybrid(DATA, [], atts, keys, brand_threshold=2, converge_min=2)
        self.assertEqual(h["confidence"], "PROVISIONAL")
        self.assertEqual(h["holder"], "Ruslan")

    def test_nothing_is_none(self):
        _, keys, _, _, _ = self._setup()
        h = resolve_hybrid(DATA, [], [], keys, brand_threshold=2, converge_min=2)
        self.assertEqual(h["confidence"], "NONE")


class TestMirrorDefense(unittest.TestCase):
    """AD-48: cross-check defense against a mirror substitution of an axis."""

    def test_out_of_band_trust_rejects_fake_mirror_sources(self):
        # the verifier trusts IN ADVANCE: 2 witnesses + 3 owner sources
        ws, wkeys = _witnesses(2)
        b_owner = brand(DATA, "Ruslan", OWNER, "t0")
        cs_owner = [w.witness(b_owner) for w in ws]
        osrc = [bytes(SigningKey.generate()) for _ in range(3)]
        owner_atts = [attest(DATA, "Ruslan", osrc[i], f"o{i}", f"t{i}") for i in range(3)]
        skeys = {a["source_pub"] for a in owner_atts}
        # the thief mirrors the semantics with 9 NEW fake sources for Thief
        fake = [attest(DATA, "Thief", bytes(SigningKey.generate()), f"fake{i}", "t9")
                for i in range(9)]
        h = resolve_hybrid(DATA, [(b_owner, cs_owner)], owner_atts + fake, wkeys,
                           brand_threshold=2, converge_min=2, source_keys=skeys)
        # the fake sources are not in the preset set → not counted → the owner
        self.assertEqual(h["holder"], "Ruslan")

    def test_shared_root_flags_independence(self):
        # one identity — both witness and source (a shared root of the axes)
        shared = bytes(SigningKey.generate())
        reg = TitleRegistry(shared)
        root = reg.pub.hex()
        b = brand(DATA, "X", OWNER, "t0")
        cs = [reg.witness(b)]
        att = [attest(DATA, "X", shared, "s0", "t0")]
        h = resolve_hybrid(DATA, [(b, cs)], att, {root}, brand_threshold=1,
                           converge_min=1, source_keys={root})
        self.assertFalse(h["independence_ok"])
        self.assertEqual(h["confidence"], "CONTESTED")

    def test_external_anchor_catches_full_mirror(self):
        # the thief aligned BOTH axes on Thief (a full mirror), but the external anchor=Ruslan
        ws, _ = _witnesses(1)
        reg = ws[0]
        b_t = brand(DATA, "Thief", THIEF, "t0")
        cs_t = [reg.witness(b_t)]
        tsrc = [bytes(SigningKey.generate()) for _ in range(2)]
        t_atts = [attest(DATA, "Thief", tsrc[i], f"t{i}", "t0") for i in range(2)]
        skeys = {a["source_pub"] for a in t_atts}
        h = resolve_hybrid(DATA, [(b_t, cs_t)], t_atts, {reg.pub.hex()},
                           brand_threshold=1, converge_min=2, source_keys=skeys,
                           external_anchor="Ruslan")
        self.assertEqual(h["confidence"], "CONTESTED")


class TestEarliness(unittest.TestCase):
    """AD-50: weight by ANCHORED earliness — the old beats a fresh flood."""

    def test_earliness_beats_flood(self):
        anchor = PublicAnchor()
        osrc = [_src() for _ in range(2)]                  # owner: 2 EARLY
        for i, (_p, pub) in enumerate(osrc):
            anchor.append(DATA, "Ruslan", f"t{i}", source_pub=pub)
        owner_atts = [attest(DATA, "Ruslan", p, f"o{i}", f"t{i}")
                      for i, (p, _) in enumerate(osrc)]
        tsrc = [_src() for _ in range(20)]                 # thief: 20 LATER (flood)
        for _p, pub in tsrc:
            anchor.append(DATA, "Thief", "late", source_pub=pub)
        thief_atts = [attest(DATA, "Thief", p, f"t{i}", "late")
                      for i, (p, _) in enumerate(tsrc)]
        c = converge_weighted(DATA, owner_atts + thief_atts, anchor.source_ranks(DATA))
        self.assertEqual(c["title_holder"], "Ruslan")

    def test_backdated_claim_still_loses(self):
        anchor = PublicAnchor()
        op, opub = _src(); anchor.append(DATA, "Ruslan", "t0", source_pub=opub)
        owner_atts = [attest(DATA, "Ruslan", op, "o", "t0")]
        # the thief BACKDATES the claimed at, but is written into the registry LATER
        tp, tpub = _src(); anchor.append(DATA, "Thief", "2000-01-01", source_pub=tpub)
        thief_atts = [attest(DATA, "Thief", tp, "t", "2000-01-01")]
        c = converge_weighted(DATA, owner_atts + thief_atts, anchor.source_ranks(DATA))
        self.assertEqual(c["title_holder"], "Ruslan")      # weight from the rank, not the date

    def test_unanchored_source_not_counted(self):
        anchor = PublicAnchor()
        op, opub = _src(); anchor.append(DATA, "Ruslan", "t0", source_pub=opub)
        owner_atts = [attest(DATA, "Ruslan", op, "o", "t0")]
        tp, _ = _src()                                     # the thief's source is NOT in the registry
        thief_atts = [attest(DATA, "Thief", tp, "t", "t0")]
        c = converge_weighted(DATA, owner_atts + thief_atts, anchor.source_ranks(DATA))
        self.assertNotIn("Thief", c["scores"])
        self.assertEqual(c["title_holder"], "Ruslan")


class TestResolveFull(unittest.TestCase):
    """AD-51: a single verdict — all axes + anchor + human-readability."""

    def _clean(self):
        anchor = PublicAnchor()
        ws, wkeys = _witnesses(2)
        osrc = [_src() for _ in range(2)]
        for _p, pub in osrc:
            anchor.append(DATA, "Ruslan", "early", source_pub=pub)
        b = brand(DATA, "Ruslan", OWNER, "t0")
        cs = [w.witness(b) for w in ws]
        atts = [attest(DATA, "Ruslan", p, f"o{i}", "t0") for i, (p, _) in enumerate(osrc)]
        skeys = {pub for _p, pub in osrc}
        return anchor, [(b, cs)], atts, wkeys, skeys

    def test_clean_anchored_confirmed(self):
        anchor, bc, atts, wkeys, skeys = self._clean()
        v = resolve_full(DATA, bc, atts, wkeys, anchor, source_keys=skeys, brand_threshold=2)
        self.assertEqual(v["confidence"], "ANCHORED_CONFIRMED")
        self.assertEqual(v["holder"], "Ruslan")
        self.assertIn("TITLE: Ruslan", human_verdict(v))

    def test_glass_forgery_contested(self):
        anchor, bc, atts, wkeys, skeys = self._clean()
        # the thief compromised the digital axis: their seal is in the trusted keys
        reg = TitleRegistry(bytes(SigningKey.generate()))
        b_t = brand(DATA, "Thief", THIEF, "t9")
        cs_t = [reg.witness(b_t)]
        v = resolve_full(DATA, bc + [(b_t, cs_t)], atts, wkeys | {reg.pub.hex()},
                         anchor, source_keys=skeys, brand_threshold=1)
        self.assertEqual(v["confidence"], "CONTESTED")   # the anchor contradicts the thief
        self.assertNotEqual(v["holder"], "Thief")

    def test_tampered_registry(self):
        anchor, bc, atts, wkeys, skeys = self._clean()
        anchor._log[0]["owner_id"] = "Thief"             # a secret edit of the registry
        v = resolve_full(DATA, bc, atts, wkeys, anchor, source_keys=skeys, brand_threshold=2)
        self.assertEqual(v["confidence"], "TAMPERED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
