# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS v2 — an envelope on an asymmetric signature (Ed25519).

Closes defect #2 of the catalog (FINAL_APPLICATIONS_REPORT, 2026-07-22):
HMAC is symmetric — both sides can forge each other's "signature", and
nothing is proven to a third party. Ed25519 separates the roles: only the
holder of the private key signs, and anyone with the public key can verify.

The v2 research finding: "stdlib only" and "provable to a third party" are
incompatible — Python's standard library has no asymmetric signature. Real
cryptography requires a real library (here PyNaCl/libsodium). This is not a
weakness of the project but a limit we record candidly.

What v2 still does NOT close (candid limits, defects #1 and #3 of the catalog):
- Self-attestation: the signature proves "this key signed this block in this
  form", but not that the content is truthful nor who owns the key. Binding
  the key to an identity is an external task (PKI/eIDAS/journal).
- Time: without an external trusted timestamp, the created_at field is
  self-declared. The anchor field is reserved for an external anchor
  (OpenTimestamps/RFC 3161) and is not filled automatically in v2.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey


def _canonical(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def generate_keypair() -> tuple[bytes, bytes]:
    """(private, public) — the private key is held only by the signer."""
    sk = SigningKey.generate()
    return bytes(sk), bytes(sk.verify_key)


def make_envelope_v2(data: str, private_key: bytes, origin: str,
                     created_at: str) -> dict:
    """A signed v2 block. created_at is passed explicitly and remains a
    self-declaration until it is bound to an external anchor (the anchor field)."""
    data = unicodedata.normalize("NFC", data)
    manifest = {
        "origin": origin,
        "created_at": created_at,
        "cp_len": len(data),  # diagnostic field (AD-3)
        "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
        "anchor": None,  # slot for an external timestamp (OTS/RFC 3161)
    }
    body = {"v": 2, "data": data, "manifest": manifest}
    sk = SigningKey(private_key)
    sig = sk.sign(_canonical(body)).signature.hex()
    return {**body, "sig": sig, "signer_pub": bytes(sk.verify_key).hex()}


def verify_envelope_v2(env: dict, trusted_pub: bytes | None = None) -> dict:
    """Third-party verification: only the envelope is needed (and, for binding
    to an identity, a trusted public key). Advisory mode."""
    report = {"status": "VERIFIED", "reasons": []}

    required = {"v", "data", "manifest", "sig", "signer_pub"}
    if not isinstance(env, dict) or not required.issubset(env):
        return {"status": "MALFORMED", "reasons": ["missing keys"]}

    body = {"v": env["v"], "data": env["data"], "manifest": env["manifest"]}
    try:
        VerifyKey(bytes.fromhex(env["signer_pub"])).verify(
            _canonical(body), bytes.fromhex(env["sig"]))
    except (BadSignatureError, ValueError):
        report["status"] = "SIGNATURE_INVALID"
        report["reasons"].append("Ed25519 signature does not match body")

    # A valid signature ≠ signed by someone you trust (SIGNED ≠ NATIVE).
    if trusted_pub is not None and env["signer_pub"] != trusted_pub.hex():
        report["status"] = "SIGNER_UNTRUSTED" if report["status"] == "VERIFIED" \
            else report["status"]
        report["reasons"].append(
            "signature is valid but signer key is not the trusted key")

    m, data = env["manifest"], env["data"]
    if len(data) != m.get("cp_len"):
        if report["status"] == "VERIFIED":
            report["status"] = "LENGTH_MISMATCH"
        report["reasons"].append(
            f"cp_len declared {m.get('cp_len')}, actual {len(data)} "
            f"(shift {len(data) - m.get('cp_len', 0):+d})")
    if hashlib.sha256(data.encode("utf-8")).hexdigest() != m.get("sha256"):
        if report["status"] == "VERIFIED":
            report["status"] = "CONTENT_CHANGED"
        report["reasons"].append("sha256 of data does not match manifest")

    if m.get("anchor") is None:
        report["reasons"].append(
            "note: created_at is self-declared (no external time anchor)")
    return report
