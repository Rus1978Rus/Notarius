# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — supply-chain: a code injection lands "on the glass" (AD-53).

The author's idea: the hacker thinks they are inserting their code into
SOMEONE ELSE's (authentic) code, but really they are inserting it ONTO
THE GLASS — into the delivered copy/channel. Pull the registry (the
authentic signed hash of the artifact), compare — the injection on the
glass is exposed, the original is clean. This is exactly the §13
"registry under glass" principle applied to CODE (adopt: code signing +
transparency logs, Sigstore/SLSA/PEP 740).

WHAT IT CATCHES (delivery = the glass): a swapped archive, a poisoned
mirror/CDN, an evil build, MITM — the delivered artifact has a different
hash → FORGERY_ON_GLASS.

WHAT IT DOES NOT CATCH (drawn on the REGISTRY, not on the glass):
  - a hijacked maintainer key/account → evil code into the ORIGINAL
    (SIGNED ≠ NATIVE): the check passes, the registry is poisoned. Remedy —
    a THRESHOLD (custody/frost: M maintainers), PUBLICITY (cosign/append-only
    makes the evil commit visible), a reproducible build + audit;
  - a WRONG registry is slipped in (dependency confusion) — a mirror
    (AD-48); which index is authoritative is decided out-of-band;
  - a signed backdoor by the author / under coercion — provenance proves
    "the author's code, untouched in delivery", NOT "the code is safe"
    (AD-24/28).
"""

from __future__ import annotations

import hashlib

from notarius.trace import _canonical


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class ArtifactRegistry:
    """Append-only registry of authentic artifacts: package_id → authentic sha256.
    The first = the original (a later one does not displace it); the hash chain
    means the past cannot be rewritten. Publicity (for a real pilot): cosign +
    OTS/Bitcoin, PEP 740/SLSA."""

    def __init__(self):
        self._log: list[dict] = []
        self._first: dict[str, dict] = {}

    def register(self, package_id: str, artifact: bytes, publisher: str,
                 at: str) -> dict:
        prev = self._log[-1] if self._log else None
        prev_hash = hashlib.sha256(_canonical(prev)).hexdigest() if prev else None
        entry = {"package_id": package_id, "artifact_sha256": _sha(artifact),
                 "publisher": publisher, "at": at,
                 "seq": len(self._log), "prev_hash": prev_hash}
        self._log.append(entry)
        self._first.setdefault(package_id, entry)   # the first wins
        return entry

    def authentic_hash(self, package_id: str) -> str | None:
        e = self._first.get(package_id)
        return e["artifact_sha256"] if e else None

    def verify_integrity(self) -> bool:
        for i, e in enumerate(self._log):
            if i == 0:
                if e["prev_hash"] is not None:
                    return False
            elif e["prev_hash"] != hashlib.sha256(_canonical(self._log[i - 1])).hexdigest():
                return False
        return True


def verify_delivery(registry: ArtifactRegistry, package_id: str,
                    delivered: bytes) -> dict:
    """Compare the delivered artifact (the glass) with the registry's authentic
    hash. delivered ≠ registry → an injection on the glass, exposed."""
    if not registry.verify_integrity():
        return {"status": "REGISTRY_TAMPERED",
                "note": "the registry was rewritten — cannot be trusted"}
    auth = registry.authentic_hash(package_id)
    if auth is None:
        return {"status": "UNKNOWN_PACKAGE",
                "note": "the package is not in the registry — nothing to rely on"}
    got = _sha(delivered)
    if got == auth:
        return {"status": "MATCH", "hash": got}
    return {"status": "FORGERY_ON_GLASS", "registry_hash": auth,
            "delivered_hash": got,
            "note": "the delivered artifact did not match the registry — an injection on the glass"}
