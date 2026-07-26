# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — the seal of ownership: title survives a breach (AD-44).

OWNERSHIP (title) ≠ POSSESSION. Crypto guards possession and breaks; the
owner's seal guards OWNERSHIP and survives a breach. A breach yields BYTES
(possession), but not TITLE.

MECHANISM (assembling existing bricks around the owner's identity):
  1. brand()    — the owner seals the data: {hash of data + identity + time},
                  signed by the owner. The seal is OUTSIDE the data (inside,
                  nothing is unremovable, AD-40), bound to an identity.
  2. TitleRegistry.witness() — external witnesses co-sign the FIRST seal on
                  a given hash and REFUSE conflicting/later ones.
                  The first witnessed seal = the owner.
  3. resolve_title() — given the data and competing claims: the title goes to
                  whoever's seal is witnessed by a quorum; a bare claim
                  (without quorum) is rejected.
  4. transfer() — a consented TWO-SIDED transfer (both sign: the giver
                  "agree to give" + the receiver "I accept").

WHAT IT PROVES: whoever BREACHED the cipher and read/copied the data but
holds no owner's key CANNOT obtain a witnessed seal (the owner already holds
it, witnesses refuse the latecomer) → their claim to ownership is refutable.
Reading ≠ title.

CANDID LIMITS:
  - Guards OWNERSHIP (title), NOT POSSESSION: a thief holds and uses the
    bytes but does not become the owner (like a stolen painting).
  - A full theft of the owner's KEY lets a transfer be forged in their name —
    this is residual, addressed by a threshold (custody/frost: "owner" = M-of-N
    keys, one stolen key does not sign) + revocation + fork detection by a
    witness (cosign). The seal alone does not save you from key theft.
  - The strength of a seal = how EARLY it was placed + how DISTRIBUTED it is
    (one breach does not rewrite it) + how bound it is to a REAL identity.
  - Does not close coercion (AD-28).
"""

from __future__ import annotations

import hashlib

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

from notarius.trace import _canonical


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _verify(pub_hex: str, body: dict, sig_hex: str) -> bool:
    try:
        VerifyKey(bytes.fromhex(pub_hex)).verify(_canonical(body), bytes.fromhex(sig_hex))
        return True
    except (BadSignatureError, ValueError, KeyError):
        return False


# --- 1. THE SEAL -------------------------------------------------------

def brand(data: bytes, owner_id: str, owner_priv: bytes, at: str) -> dict:
    """The owner seals the data: bind the hash of the data to an identity and time."""
    body = {"kind": "BRAND", "data_sha256": _sha(data), "owner_id": owner_id, "at": at}
    sk = SigningKey(owner_priv)
    return {**body, "owner_pub": bytes(sk.verify_key).hex(),
            "sig": sk.sign(_canonical(body)).signature.hex()}


def _brand_body(b: dict) -> dict:
    return {k: b[k] for k in ("kind", "data_sha256", "owner_id", "at")}


def brand_valid(b: dict) -> bool:
    return b.get("kind") == "BRAND" and _verify(b.get("owner_pub", ""), _brand_body(b),
                                                 b.get("sig", ""))


# --- 2. TITLE WITNESS (first seal on a hash = the owner) ---------------

class TitleRegistry:
    """An external witness: co-signs the FIRST seal on a given hash, refuses a
    conflicting owner on the same hash. Stores O(1) per hash."""

    def __init__(self, priv: bytes):
        self._sk = SigningKey(priv)
        self.pub = bytes(self._sk.verify_key)
        self._seen: dict[str, tuple] = {}   # data_sha256 -> (owner_id, owner_pub, at)

    def witness(self, b: dict) -> dict | None:
        if not brand_valid(b):
            return None
        key = b["data_sha256"]
        prev = self._seen.get(key)
        if prev is not None:
            if (b["owner_id"], b["owner_pub"]) != (prev[0], prev[1]):
                return None                 # conflicting owner on the same hash → REFUSE
        else:
            self._seen[key] = (b["owner_id"], b["owner_pub"], b["at"])
        return {"witness_pub": self.pub.hex(), "data_sha256": key,
                "cosig": self._sk.sign(_canonical(_brand_body(b))).signature.hex()}


def brand_witnessed(b: dict, cosigs: list, witness_keys: set, threshold: int = 1) -> bool:
    body = _brand_body(b)
    valid = {cs["witness_pub"] for cs in cosigs
             if cs.get("witness_pub") in witness_keys
             and cs.get("data_sha256") == b["data_sha256"]
             and _verify(cs["witness_pub"], body, cs.get("cosig", ""))}
    return len(valid) >= threshold


# --- 3. TITLE RESOLUTION -----------------------------------------------

def resolve_title(data: bytes, claims: list, witness_keys: set,
                  threshold: int = 1) -> dict:
    """claims: [(brand, cosigs)]. Title goes to the claim with a valid witness
    quorum on the hash of THESE data. A bare claim (without quorum) is rejected."""
    h = _sha(data)
    holders, refuted = [], []
    for b, cs in claims:
        ok = (b.get("data_sha256") == h and brand_valid(b)
              and brand_witnessed(b, cs, witness_keys, threshold))
        (holders if ok else refuted).append(b.get("owner_id"))
    return {"data_sha256": h, "title_holders": sorted(set(holders)),
            "refuted": sorted(set(refuted) - set(holders))}


# --- 4. CONSENTED TWO-SIDED TRANSFER -----------------------------------

def transfer(prev: dict, from_priv: bytes, to_id: str, to_priv: bytes,
             at: str) -> dict:
    """Transfer the title: BOTH sign — the giver and the receiver. A thief with
    the BYTES alone cannot sign the giver's side (no owner's key)."""
    prev_hash = hashlib.sha256(_canonical(prev)).hexdigest()
    from_sk, to_sk = SigningKey(from_priv), SigningKey(to_priv)
    body = {"kind": "TRANSFER", "prev": prev_hash, "to_id": to_id,
            "from_pub": bytes(from_sk.verify_key).hex(),
            "to_pub": bytes(to_sk.verify_key).hex(), "at": at}
    return {**body,
            "from_sig": from_sk.sign(_canonical(body)).signature.hex(),
            "to_sig": to_sk.sign(_canonical(body)).signature.hex()}


def transfer_valid(t: dict) -> bool:
    """Both signatures must check out — otherwise the transfer is not consented."""
    body = {k: t[k] for k in ("kind", "prev", "to_id", "from_pub", "to_pub", "at")}
    return (t.get("kind") == "TRANSFER"
            and _verify(t.get("from_pub", ""), body, t.get("from_sig", ""))
            and _verify(t.get("to_pub", ""), body, t.get("to_sig", "")))


# --- 5. SEMANTIC ROOT: resolution by CONVERGENCE (AD-46) --------------
# A digital seal/quorum rests on the SECRET of the keys (break it — forge it).
# The semantic root rests on the COHERENCE of a distributed history:
# the title goes to whoever more INDEPENDENT records converge on (and earlier).
# A partial breach (k keys broken) does not flip the title if the owner has
# more independent sources. This is closer to real provenance (a network of
# mutually corroborating records) than to "one unbreakable signature".

def attest(data: bytes, owner_id: str, source_priv: bytes, source_id: str,
           at: str) -> dict:
    """An independent record: source source_id attests that the data belongs
    to owner_id at time at. One of many in a corroboration network."""
    body = {"kind": "ATTEST", "data_sha256": _sha(data), "owner_id": owner_id,
            "source_id": source_id, "at": at}
    sk = SigningKey(source_priv)
    return {**body, "source_pub": bytes(sk.verify_key).hex(),
            "sig": sk.sign(_canonical(body)).signature.hex()}


def attest_valid(a: dict) -> bool:
    body = {k: a[k] for k in ("kind", "data_sha256", "owner_id", "source_id", "at")}
    return a.get("kind") == "ATTEST" and _verify(a.get("source_pub", ""), body,
                                                 a.get("sig", ""))


def converge(data: bytes, attestations: list, min_sources: int = 1,
             trusted_sources: set | None = None) -> dict:
    """Semantic title resolution by CONVERGENCE: count how many INDEPENDENT
    sources converge (data → owner). Title goes to the owner with the dominant
    convergence. A tie in the NUMBER of sources → dispute (contested), a human
    decides — earliness is NOT the tie-breaker here (N-W16, audit 2026-07-26:
    earliest in the sort only orders the output on ties, but the outcome is
    still "dispute"). Weighting by earliness is a separate function,
    converge_weighted below.

    trusted_sources — if given (an out-of-band set of source public keys the
    verifier trusts IN ADVANCE), ONLY records from them are counted. This is
    a defense against a mirror/Sybil: new fake sources presented by a thief are
    NOT counted because they are not in the preset set.

    CANDIDLY: convergence measures COHERENCE/corroboration (the cost of forgery),
    NOT truth (FF-005 RECURRENCE ≠ VALIDITY). It is strong exactly as far as the
    sources are TRULY independent (Sybil — fake sources — bypasses it; real
    independence of identities is required). It does not close stolen provenance."""
    h = _sha(data)
    by_owner: dict[str, dict] = {}          # owner_id -> {source_key: earliest_at}
    for a in attestations:
        if trusted_sources is not None and a.get("source_pub") not in trusted_sources:
            continue                        # not from the preset trusted set
        if a.get("data_sha256") == h and attest_valid(a):
            src = (a["source_id"], a["source_pub"])   # independence = a distinct source
            d = by_owner.setdefault(a["owner_id"], {})
            if src not in d or a["at"] < d[src]:
                d[src] = a["at"]
    scores = {owner: {"independent_sources": len(srcs),
                      "earliest": min(srcs.values())}
              for owner, srcs in by_owner.items()}
    ranked = sorted(scores.items(),
                    key=lambda kv: (-kv[1]["independent_sources"], kv[1]["earliest"]))
    holder, contested = None, False
    if ranked and ranked[0][1]["independent_sources"] >= min_sources:
        if len(ranked) > 1 and ranked[1][1]["independent_sources"] == ranked[0][1]["independent_sources"]:
            contested = True                # equal weight of history → dispute, a human decides
        else:
            holder = ranked[0][0]
    return {"data_sha256": h, "scores": scores,
            "title_holder": holder, "contested": contested}


# --- 5b. WEIGHT BY EARLINESS: the old beats a fresh flood (AD-50) ------
# A thief fabricates ONLY after the theft → all their records are LATE. Give
# the owner's old record greater weight — and a thousand fresh fakes won't
# outweigh it.
# CRITICAL: the weight comes from the ANCHORED rank (append-only registry, AD-49),
# NOT from a claimed date — otherwise the thief backdates the fakes. Geometric
# decay 0.5**rank makes the flood powerless: the sum of all late records is bounded.

def converge_weighted(data: bytes, attestations: list, source_ranks: dict,
                      min_weight: float = 0.0) -> dict:
    """Convergence weighted by ANCHORED earliness. source_ranks: source_pub →
    rank in the public registry (0 = earliest of all). Weight 0.5**rank: the
    early ones dominate, a flood of late fakes is bounded and cannot outweigh."""
    h = _sha(data)
    by_owner: dict[str, dict] = {}
    for a in attestations:
        if a.get("data_sha256") == h and attest_valid(a):
            sp = a["source_pub"]
            if sp not in source_ranks:        # not anchored → earliness unproven → 0
                continue
            r = source_ranks[sp]
            d = by_owner.setdefault(a["owner_id"], {})
            if sp not in d or r < d[sp]:
                d[sp] = r
    scores = {o: {"weight": round(sum(0.5 ** r for r in srcs.values()), 6),
                  "sources": len(srcs), "earliest_rank": min(srcs.values())}
              for o, srcs in by_owner.items()}
    ranked = sorted(scores.items(), key=lambda kv: -kv[1]["weight"])
    holder, contested = None, False
    if ranked and ranked[0][1]["weight"] > min_weight:
        if len(ranked) > 1 and abs(ranked[1][1]["weight"] - ranked[0][1]["weight"]) < 1e-9:
            contested = True
        else:
            holder = ranked[0][0]
    return {"data_sha256": h, "scores": scores,
            "title_holder": holder, "contested": contested}


# --- 6. HYBRID: digital axis + semantic axis (AD-47) ------------------
# Each axis closes the other's weakness:
#   digital (seal quorum) — strong against forgery-without-key, weak to a breach;
#   semantic (convergence) — strong against a breach, weak to Sybil.
# In the hybrid the attacker must beat BOTH. The main value: if the axes
# DIVERGE (digital says A, semantics says B) — that is ITSELF a signal
# (key theft OR Sybil is likely): the hybrid flags CONTESTED instead of
# quietly handing over the title. A pure digital axis would hand it over;
# the hybrid catches it.

def resolve_hybrid(data: bytes, brand_claims: list, attestations: list,
                   witness_keys: set, brand_threshold: int = 1,
                   converge_min: int = 2, source_keys: set | None = None,
                   external_anchor: str | None = None) -> dict:
    """Title by BOTH axes. confidence:
       CONFIRMED   — both axes agree (the attacker must break both);
       PROVISIONAL — one axis in favor, the other silent (weaker);
       CONTESTED   — axes diverge → key theft/Sybil/mirror likely;
       NONE        — neither axis.

    MIRROR DEFENSE (AD-48):
    - witness_keys and source_keys — PRESET (out-of-band) trusted roots;
      new fakes presented by a thief are not counted;
    - the axes' roots must be DIFFERENT: an intersection witness_keys ∩
      source_keys → independence undermined (one hand holds both axes) → not
      CONFIRMED;
    - external_anchor (if given) — a data→owner binding known to the verifier
      OUT of channel; a contradiction → CONTESTED (a mirror with no external trace)."""
    digital = resolve_title(data, brand_claims, witness_keys, brand_threshold)
    semantic = converge(data, attestations, converge_min, trusted_sources=source_keys)
    d = set(digital["title_holders"])
    s = semantic["title_holder"]
    reasons = []

    # independence of roots: one hand must not hold both axes
    independence_ok = not (source_keys is not None and (witness_keys & source_keys))

    if not d and not s and not semantic["contested"]:
        holder, conf = None, "NONE"
        reasons.append("neither a digital nor a semantic footing")
    elif s and d == {s}:
        holder, conf = s, "CONFIRMED"
        reasons.append("both axes agree: witnessed seal + convergence")
    elif d == set() and s and not semantic["contested"]:
        holder, conf = s, "PROVISIONAL"
        reasons.append("semantic axis only (no witnessed seal) — weaker")
    elif len(d) == 1 and not s and not semantic["contested"]:
        holder, conf = next(iter(d)), "PROVISIONAL"
        reasons.append("digital axis only (semantics silent) — weaker")
    else:
        holder, conf = None, "CONTESTED"
        reasons.append(f"AXES DIVERGE: digital={sorted(d)}, semantic={s}"
                       f"{' (dispute)' if semantic['contested'] else ''} — "
                       f"key theft/Sybil/mirror likely; a human decides")

    # mirror #1: a shared root of the axes — "agreement" is worthless
    if conf == "CONFIRMED" and not independence_ok:
        holder, conf = None, "CONTESTED"
        reasons.append("AXIS INDEPENDENCE UNDERMINED: a shared trusted root "
                       "(witness ∩ source) — the agreement may be a mirror")

    # mirror #2: contradiction with an external anchor the thief does not have
    if external_anchor is not None and holder is not None and holder != external_anchor:
        reasons.append(f"EXTERNAL ANCHOR={external_anchor} contradicts {holder} — "
                       f"a mirror with no external trace")
        holder, conf = None, "CONTESTED"

    return {"holder": holder, "confidence": conf, "reasons": reasons,
            "independence_ok": independence_ok,
            "digital": digital, "semantic": semantic}


# --- 7. SINGLE VERDICT: all together + human-readable (AD-51) -----------

def resolve_full(data: bytes, brand_claims: list, attestations: list,
                 witness_keys: set, anchor, source_keys: set | None = None,
                 brand_threshold: int = 1) -> dict:
    """A single title resolution: the DIGITAL axis (seal quorum) + the SEMANTIC
    one (convergence weighted by earliness from the anchor) + the PUBLIC ANCHOR
    (registry under glass, an authoritative window) + mirror defense (different
    roots, integrity).

    confidence:
      ANCHORED_CONFIRMED — anchor + both axes agree (strongest)
      ANCHORED           — the anchor is authoritative, the axes do not contradict
      PROVISIONAL        — no anchor, the axes agree (weaker — no window)
      CONTESTED          — contradiction/mirror/independence undermined
      TAMPERED           — the registry was secretly rewritten
      NONE               — no footing at all"""
    digital = resolve_title(data, brand_claims, witness_keys, brand_threshold)
    ranks = anchor.source_ranks(data)
    semantic = converge_weighted(data, attestations, ranks)
    registry = anchor.pull(data)
    A = registry["owner_id"] if registry else None
    D = set(digital["title_holders"])
    s = semantic["title_holder"]
    integrity_ok = anchor.verify_integrity()
    independence_ok = not (source_keys is not None and (witness_keys & source_keys))
    reasons = []

    def sig():
        return {"digital": sorted(D), "semantic": s, "anchor": A,
                "integrity_ok": integrity_ok, "independence_ok": independence_ok}

    if not integrity_ok:
        reasons.append("REGISTRY REWRITTEN: the hash-chain is broken — cannot be trusted")
        return _verdict(None, "TAMPERED", reasons, sig())

    if A is not None:
        contra = [x for x in (list(D) + ([s] if s else [])) if x and x != A]
        if contra:
            reasons.append(f"ANCHOR={A} contradicts the claimed {sorted(set(contra))} "
                           f"— drawn onto the glass (a mirror)")
            return _verdict(None, "CONTESTED", reasons, sig())
        if D == {A} and s == A and independence_ok:
            reasons.append(f"anchor + digital + semantic — all in favor of {A}")
            return _verdict(A, "ANCHORED_CONFIRMED", reasons, sig())
        if not independence_ok:
            reasons.append("axis independence undermined (shared root) — the agreement "
                           "may be a mirror")
            return _verdict(None, "CONTESTED", reasons, sig())
        reasons.append(f"anchor is authoritative for {A}; the axes do not contradict (one may be silent)")
        return _verdict(A, "ANCHORED", reasons, sig())

    # no anchor — hybrid of the two axes (no independent window)
    reasons.append("NO REGISTRY ENTRY (no independent window) — weaker footing")
    if not D and not s:
        return _verdict(None, "NONE", reasons + ["no axis at all"], sig())
    if s and D == {s} and independence_ok:
        return _verdict(s, "PROVISIONAL", reasons + [f"both axes for {s}"], sig())
    if len(D) == 1 and not s:
        return _verdict(next(iter(D)), "PROVISIONAL", reasons + ["digital axis only"], sig())
    if s and not D:
        return _verdict(s, "PROVISIONAL", reasons + ["semantic axis only"], sig())
    return _verdict(None, "CONTESTED", reasons + [f"axes diverge: digital={sorted(D)}, "
                    f"semantic={s}"], sig())


def _verdict(holder, confidence, reasons, signals):
    return {"holder": holder, "confidence": confidence,
            "reasons": reasons, "signals": signals}


def human_verdict(v: dict) -> str:
    """Human-readable verdict: who gets the title, how confidently, why."""
    s = v["signals"]
    lines = [
        f"TITLE: {v['holder'] or '— not awarded —'}",
        f"CONFIDENCE: {v['confidence']}",
        f"  digital axis (seal+quorum): {s['digital'] or '—'}",
        f"  semantic axis (weight by earliness): {s['semantic'] or '—'}",
        f"  public anchor (registry): {s['anchor'] or '— no entry —'}",
        f"  registry intact: {'yes' if s['integrity_ok'] else 'NO (rewritten)'}",
        f"  axis independence: {'yes' if s['independence_ok'] else 'NO (shared root)'}",
        "WHY:",
    ]
    lines += [f"  - {r}" for r in v["reasons"]]
    return "\n".join(lines)


if __name__ == "__main__":   # demonstration of "reading ≠ title"
    DATA = b"contract=deed-42 asset=painting owner-secret-content"
    owner = bytes(SigningKey.generate())
    w1, w2 = TitleRegistry(bytes(SigningKey.generate())), TitleRegistry(bytes(SigningKey.generate()))
    wkeys = {w1.pub.hex(), w2.pub.hex()}

    # the owner seals, two witnesses co-sign
    b_owner = brand(DATA, "Ruslan", owner, at="2026-07-23T10:00Z")
    cs_owner = [w1.witness(b_owner), w2.witness(b_owner)]

    # the THIEF breached the cipher, COPIED the data, seals it with their own key
    thief = bytes(SigningKey.generate())
    b_thief = brand(DATA, "Thief", thief, at="2026-07-23T11:00Z")
    cs_thief = [w1.witness(b_thief), w2.witness(b_thief)]   # witnesses will REFUSE

    r = resolve_title(DATA, [(b_owner, cs_owner), (b_thief, [c for c in cs_thief if c])],
                      wkeys, threshold=2)
    print("title:", r["title_holders"], "| refuted:", r["refuted"])
    print("conclusion: the thief copied the BYTES, but the title stayed with the owner — reading ≠ ownership")

    # consented transfer owner → buyer
    buyer = bytes(SigningKey.generate())
    t = transfer(b_owner, owner, "Buyer", buyer, at="2026-07-24T09:00Z")
    print("two-sided transfer valid:", transfer_valid(t))

    # SEMANTIC ROOT: convergence of independent records.
    # The owner has 3 independent sources; the thief BROKE 1 key and forged 1 record.
    srcs = [bytes(SigningKey.generate()) for _ in range(3)]
    atts = [attest(DATA, "Ruslan", srcs[i], f"src-{i}", f"2026-07-2{i}") for i in range(3)]
    atts.append(attest(DATA, "Thief", bytes(SigningKey.generate()), "src-evil", "2026-07-25"))
    c = converge(DATA, atts, min_sources=2)
    print("convergence:", {o: s["independent_sources"] for o, s in c["scores"].items()},
          "→ title:", c["title_holder"])
    print("conclusion: 1 broken key did not outweigh the owner's 3 independent records")

    # HYBRID: the norm — both axes agree → CONFIRMED
    owner_atts = [attest(DATA, "Ruslan", srcs[i], f"src-{i}", f"2026-07-2{i}") for i in range(3)]
    h1 = resolve_hybrid(DATA, [(b_owner, cs_owner)], owner_atts, wkeys,
                        brand_threshold=2, converge_min=2)
    print("hybrid (norm):", h1["confidence"], "→", h1["holder"])

    # HYBRID: the thief broke the DIGITAL axis (forged a witnessed seal),
    # but the semantics (independent history) holds the owner → CONTESTED, caught
    evil_reg = TitleRegistry(bytes(SigningKey.generate()))
    b_evil = brand(DATA, "Thief", thief, at="2026-07-25T00:00Z")
    cs_evil = [evil_reg.witness(b_evil)]
    h2 = resolve_hybrid(DATA, [(b_evil, cs_evil)], owner_atts, {evil_reg.pub.hex()},
                        brand_threshold=1, converge_min=2)
    print("hybrid (digital axis breached):", h2["confidence"], "—", h2["reasons"][0])
