# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — public append-only anchor: the "registry under glass" (AD-49).

The author's metaphor: a public registry hangs under glass. An attacker can
draw only ON THE GLASS (on the presented copy/channel), not on the registry
itself. Take the registry out — it is clean, the drawing stayed on the glass.

→ Mirror defense (AD-48): do not trust the GLASS (what is presented), but PULL
OUT THE REGISTRY (the authoritative source) and RECONCILE. Forgery lives on
the glass and is exposed by reconciliation.

The registry here:
  - append-only (only append; a hash-chain — past entries cannot be rewritten);
  - the first seal on a hash = authority (a later one does not displace it);
  - "pulled out" by the pull() operation — taken from the registry, NOT from
    the presenter's hands;
  - reconcile() = reconcile the glass with the registry → MATCH / FORGERY_ON_GLASS.

Publicity (the harder the registry is to rewrite, the more valuable it is):
  - cosign (our witnesses) — a distributed copy in many hands;
  - OTS (Bitcoin) — a public indelible ledger with a date. The adapter is real,
    but stamp requires the network (in this environment it is blocked,
    HONEST_LIMIT, like AD-31).

CANDID LIMIT (the metaphor shows it too): the defense works AS LONG AS the
registry can be pulled out. If the thief holds ALL channels and there is no
registry (it was not written early) — you see the glass forever (FO-005
INTERFACE ≠ REALITY).
"""

from __future__ import annotations

import hashlib

from notarius.trace import _canonical


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PublicAnchor:
    """A public append-only registry ("under glass"). A hash-chain makes the
    past non-rewritable; the first seal on a hash = authority."""

    def __init__(self):
        self._log: list[dict] = []
        self._first: dict[str, dict] = {}     # data_sha256 -> the first entry

    def append(self, data: bytes, owner_id: str, at: str,
               source_pub: str | None = None) -> dict:
        """Append an entry (forward only). The past is untouched. source_pub —
        who wrote it (for the weight by earliness)."""
        h = _sha(data)
        prev = self._log[-1] if self._log else None
        prev_hash = hashlib.sha256(_canonical(prev)).hexdigest() if prev else None
        entry = {"data_sha256": h, "owner_id": owner_id, "at": at,
                 "seq": len(self._log), "prev_hash": prev_hash, "source_pub": source_pub}
        self._log.append(entry)
        self._first.setdefault(h, entry)      # the first wins; not rewritable
        return entry

    def source_ranks(self, data: bytes) -> dict:
        """{source_pub: rank of first appearance for this data} (0 = earliest of all).
        Append-only → the rank CANNOT be lowered after the fact. The basis for the
        weight by earliness: not the claimed at (a thief backdates), but the REAL
        order in the public registry."""
        h = _sha(data)
        ranks: dict[str, int] = {}
        for e in self._log:                   # in seq order (append-only)
            sp = e.get("source_pub")
            if e["data_sha256"] == h and sp is not None and sp not in ranks:
                ranks[sp] = len(ranks)
        return ranks

    def pull(self, data: bytes) -> dict | None:
        """PULL OUT the authoritative entry from the registry (not from the presenter's hands)."""
        return self._first.get(_sha(data))

    def head(self) -> str | None:
        """The registry head — commits the whole append-only log (for cosign/OTS)."""
        return hashlib.sha256(_canonical(self._log[-1])).hexdigest() if self._log else None

    def verify_integrity(self) -> bool:
        """The registry was not quietly rewritten: the hash-chain of links is intact."""
        for i, e in enumerate(self._log):
            if i == 0:
                if e["prev_hash"] is not None:
                    return False
            elif e["prev_hash"] != hashlib.sha256(_canonical(self._log[i - 1])).hexdigest():
                return False
        return True


def reconcile(presented_owner: str, data: bytes, anchor: PublicAnchor) -> dict:
    """GLASS versus REGISTRY: reconcile the presented owner with the registry's
    authoritative entry. presented ≠ registry → forgery on the glass, exposed."""
    real = anchor.pull(data)
    if real is None:
        return {"status": "NOT_ANCHORED",
                "note": "no entry in the registry — nothing to rely on (write it early)"}
    if presented_owner == real["owner_id"]:
        return {"status": "MATCH", "registry_owner": real["owner_id"],
                "registry_at": real["at"]}
    return {"status": "FORGERY_ON_GLASS", "registry_owner": real["owner_id"],
            "presented": presented_owner,
            "note": "the presented one did not match the registry — drawn onto the glass"}


# --- OTS: make the registry as public as possible (Bitcoin) ------------
# HONEST_LIMIT: stamp requires the network (in this environment it is blocked, like AD-31).

def anchor_ots_digest(anchor: PublicAnchor) -> bytes:
    """32-byte digest of the registry head — what gets anchored in Bitcoin."""
    head = anchor.head()
    if head is None:
        raise ValueError("empty registry")
    return hashlib.sha256(head.encode()).digest()
