# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — mortal carrier validator (PROVENANCE_CARRIER, §8 + AD-29).

A short-lived, single-use carrier (a QR receipt) that carries a signature
"into someone else's hands" and is safe there because:
  1. SHORT LIFE — it expires after ttl seconds (time-based expiry);
  2. SINGLE-USE — the server marks it "used" on first presentation, and a
     second one → refusal ("burned on use").
Together = a copy is useless: photograph the QR → it is already dead or burned.

The carrier does NOT contain a key: it contains a short-lived PROOF signed
by the key (the key stays in the enclave/custody). Steal the carrier — you
stole a one-minute receipt, not the key.

This is the human-readable face of the "mortal copy" (AD-26): clear to a
cashier, with no crypto jargon. The pattern is deployed in the wild (TOTP,
rotating payment QR codes) — adopt-don't-invent (AD-23).

LIMITS (candidly):
  - Within the ttl window the carrier is copyable (it is data); the defense
    is only the short window + single-use, not "cannot be copied".
  - A trusted TIME SOURCE is needed at the verifier (otherwise the window lies).
  - This is an HMAC demo; production uses a signature by a key from custody
    (AD-27) and an external timestamp (AD-23) for absolute time.

Stdlib only.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets


_RISK_ORDER = {"OK": 0, "WATCH": 1, "ALARM": 2}


def _screen_payload(payload) -> dict:
    """Screen the CONTENT of the carrier (AD-33, the engine from Vakhter):
    recursively run all payload strings through scan_hardened and return the
    worst verdict. A separate axis from the signature: the carrier may be
    valid while the payload is poisoned by a zero-width char
    (CONTAINER_INTACT ≠ ELEMENT_CLEAN)."""
    from notarius.scanner import scan_hardened
    worst = {"risk": "OK", "signature": ""}

    def walk(v):
        nonlocal worst
        if isinstance(v, str):
            sc = scan_hardened(v)
            if _RISK_ORDER[sc["risk"]] > _RISK_ORDER[worst["risk"]]:
                worst = {"risk": sc["risk"], "signature": sc["signature"]}
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x)

    walk(payload)
    return worst


def issue_carrier(payload: dict, key: bytes, issued_at: int,
                  ttl_seconds: int = 60) -> dict:
    """Issue a mortal carrier: payload + life window + single-use nonce +
    signature. issued_at — the moment of issuance (seconds)."""
    body = {
        "payload": payload,
        "issued_at": issued_at,
        "expires_at": issued_at + ttl_seconds,
        # RANDOM nonce (N-W6, audit 2026-07-26): a deterministic
        # sha256(issued_at:payload) rejected a LEGITIMATE reissue of the same
        # payload within the same second as ALREADY_USED (a DoS on yourself).
        # A random nonce is always unique; the signature covers it.
        "nonce": secrets.token_hex(16),
    }
    sig = hmac.new(key, json.dumps(body, sort_keys=True,
                   separators=(",", ":")).encode(), hashlib.sha256).hexdigest()
    return {**body, "sig": sig}


class CarrierValidator:
    """Verifier at the system boundary. Keeps only the set of already
    redeemed nonces (O(1) per carrier), not the carriers themselves."""

    def __init__(self, key: bytes):
        self._key = key
        self._spent: set[str] = set()

    def validate(self, carrier: dict, now: int) -> dict:
        """now — the current trusted time (seconds). Advisory report:
        VALID / EXPIRED / ALREADY_USED / SIGNATURE_INVALID."""
        required = {"payload", "issued_at", "expires_at", "nonce", "sig"}
        if not isinstance(carrier, dict) or not required.issubset(carrier):
            return {"status": "MALFORMED"}

        body = {k: carrier[k] for k in
                ("payload", "issued_at", "expires_at", "nonce")}
        expected = hmac.new(self._key, json.dumps(body, sort_keys=True,
                            separators=(",", ":")).encode(),
                            hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, carrier["sig"]):
            return {"status": "SIGNATURE_INVALID"}

        if now > carrier["expires_at"]:
            return {"status": "EXPIRED",
                    "note": f"carrier expired ({now - carrier['expires_at']}s ago)"}
        if now < carrier["issued_at"]:
            return {"status": "NOT_YET_VALID"}

        if carrier["nonce"] in self._spent:
            return {"status": "ALREADY_USED",
                    "note": "carrier already redeemed — a copy is useless"}
        self._spent.add(carrier["nonce"])          # burn on first presentation
        result = {"status": "VALID", "payload": carrier["payload"]}
        sc = _screen_payload(carrier["payload"])   # content axis (AD-33)
        result["content_scan"] = sc
        if sc["risk"] != "OK":
            result["note"] = (f"CONTENT: {sc['risk']} ({sc['signature']}) — "
                              f"the carrier is valid, but the payload carries a "
                              f"hidden manipulation (CONTAINER_INTACT ≠ ELEMENT_CLEAN)")
        return result
