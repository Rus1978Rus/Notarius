# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — a minimal prototype of SEMANTIC_INVISIBLE_LENGTH_WITNESS.

Two implementations side by side, on purpose:

1. A naive witness (exactly as in NOTARIUS_FULL_SESSION.md §6.3) —
   demonstrates both what the barrier catches and what it does NOT.
   Status per the 2026-07-21 audit: DIAGNOSTIC_METADATA, not a barrier.

2. SignedEnvelope — the corrected envelope: canonical JSON + SHA-256
   + HMAC. The control length is kept as a diagnostic field inside the
   signed manifest. Standard library only.

HMAC with a shared key is chosen for the prototype to stay free of
external dependencies; in a product the sender and receiver must not
share a secret — that requires an asymmetric signature (Ed25519).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import unicodedata

# --- 1. Naive witness (verbatim from the document) ---------------------


def block_with_witness(data: str) -> dict:
    return {"data": data, "cp_len": len(data)}  # len = code points


def verify_witness(block: dict) -> bool:
    return len(block["data"]) == block["cp_len"]


# --- Diagnostics of invisible code points -----------------------------

# Common invisible/formatting code points from §6.3 (not the exhaustive
# Default_Ignorable list, but enough for the demo and the tests).
INVISIBLE_CODEPOINTS = {
    "​",  # ZWSP
    "‌",  # ZWNJ
    "‍",  # ZWJ
    "⁠",  # WORD JOINER
    "️",  # VS16
    "﻿",  # BOM / ZWNBSP
    "‪", "‫", "‬", "‭", "‮",  # bidi embed/override
    "⁦", "⁧", "⁨", "⁩",            # bidi isolate
    "­",  # SOFT HYPHEN
}


def find_invisibles(data: str) -> list[dict]:
    """List of invisible code points with positions — for a human-readable report."""
    found = []
    for i, ch in enumerate(data):
        if ch in INVISIBLE_CODEPOINTS or unicodedata.category(ch) == "Cf":
            found.append({"index": i, "codepoint": f"U+{ord(ch):04X}",
                          "name": unicodedata.name(ch, "UNKNOWN")})
    return found


# --- 2. Corrected envelope: signed envelope ---------------------------


def _canonical(payload: dict) -> bytes:
    """Canonical JSON: sorted keys, no whitespace, UTF-8."""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def make_envelope(data: str, key: bytes, origin: str) -> dict:
    """A signed block. The spec pins the normal form NFC BEFORE counting
    length and hashing (see audit §6.3: otherwise legitimate normalization
    in transit produces false positives)."""
    data = unicodedata.normalize("NFC", data)
    manifest = {
        "origin": origin,
        "cp_len": len(data),  # diagnostic field, not a barrier
        "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
    }
    body = {"data": data, "manifest": manifest}
    sig = hmac.new(key, _canonical(body), hashlib.sha256).hexdigest()
    return {**body, "sig": sig}


def verify_envelope(env: dict, key: bytes) -> dict:
    """Advisory mode: a report with reasons, no exceptions."""
    report = {"status": "VERIFIED", "reasons": [], "invisibles": []}

    if not isinstance(env, dict) or "data" not in env \
            or "manifest" not in env or "sig" not in env:
        return {"status": "MALFORMED", "reasons": ["missing keys"],
                "invisibles": []}

    body = {"data": env["data"], "manifest": env["manifest"]}
    expected = hmac.new(key, _canonical(body), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, env["sig"]):
        report["status"] = "SIGNATURE_INVALID"
        report["reasons"].append("signature does not match body")

    m = env["manifest"]
    data = env["data"]
    actual_len = len(data)
    if actual_len != m.get("cp_len"):
        report["status"] = report["status"] if report["status"] != "VERIFIED" \
            else "LENGTH_MISMATCH"
        report["reasons"].append(
            f"cp_len declared {m.get('cp_len')}, actual {actual_len} "
            f"(shift {actual_len - m.get('cp_len', 0):+d})")

    if hashlib.sha256(data.encode("utf-8")).hexdigest() != m.get("sha256"):
        if report["status"] == "VERIFIED":
            report["status"] = "CONTENT_CHANGED"
        report["reasons"].append("sha256 of data does not match manifest")

    report["invisibles"] = find_invisibles(data)
    return report
