# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — managed record: fields with keepers + legitimate progression (AD-87).

Brings three prototypes together into ONE part of the core:
  - sealed void (AD-84): a field with value "" — intentionally empty;
  - legitimate progression (AD-85): an edit is lawful if the editor signed the
    event; the reader is shown a footnote "who / where (field) / when";
  - field keeper (AD-86): a critical field (e.g. the numbers) has its own keeper —
    ONLY they may lawfully change it.

Complements trace.py (there — the event chain of an ELEMENT's value; here —
the structure of FIELDS with zones of responsibility). Signature — Ed25519.

Model: the creator's seal (create_record) fixes the field values, the keeper
map {field→keeper} and the keeper keys — they cannot be reassigned on the fly.
Edits (edit_field) — a signed chain. audit() localizes PER FIELD:
  EDIT_BY_NON_KEEPER  — a field was edited by someone other than its keeper (role forgery);
  KEEPER_KEY_MISMATCH — the editor's key did not match the keeper's key;
  UNSIGNED_CHANGE     — a field in the document differs from the signed history;
  NEW_SLOT            — an unsealed field appeared (insertion into the structure);
  MISSING_SLOT        — a sealed field vanished;
  CHAIN_BROKEN / BAD_SIG / BAD_CREATE_SIG / NO_KEEPER.

Limit (candidly): it proves "an edit without the keeper's signature = forgery"
and localizes the field; it does NOT prove the value's truthfulness and does
not judge intent.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey


def _canon(body: dict) -> bytes:
    return json.dumps(body, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def _body(ev: dict) -> dict:
    return {k: ev[k] for k in ev if k not in ("pub", "sig")}


def _sign(body: dict, priv: bytes) -> dict:
    sk = SigningKey(priv)
    return {**body, "pub": bytes(sk.verify_key).hex(),
            "sig": sk.sign(_canon(body)).signature.hex()}


def _verify(ev: dict) -> bool:
    try:
        VerifyKey(bytes.fromhex(ev["pub"])).verify(_canon(_body(ev)),
                                                   bytes.fromhex(ev["sig"]))
        return True
    except (BadSignatureError, ValueError, KeyError):
        return False


def _digest(ev: dict) -> str:
    """Hash of the whole event (signature included) — the link for the next one."""
    return hashlib.sha256(_canon(ev)).hexdigest()


# ── creation and editing ──────────────────────────────────────────────
def create_record(fields: dict, keepers: dict, keeper_keys: dict,
                  author_id: str, author_priv: bytes, at: str) -> dict:
    """The creator's seal: field values ("" = sealed void), the map
    {field→keeper} and the keeper keys {keeper→pub_hex}."""
    body = {"kind": "RECORD", "author": author_id, "at": at,
            "fields": dict(fields), "keepers": dict(keepers),
            "keeper_keys": dict(keeper_keys)}
    return _sign(body, author_priv)


def edit_field(prev: dict, editor_id: str, editor_priv: bytes, at: str,
               field: str, new_value: str) -> dict:
    """A signed edit of a single field, linked to the previous event."""
    body = {"kind": "EDIT", "editor": editor_id, "at": at, "field": field,
            "new": new_value, "prev_hash": _digest(prev)}
    return _sign(body, editor_priv)


def rebuild(create_ev: dict, edits: list) -> dict:
    """Official state = base + signed edits of SEALED fields."""
    doc = dict(create_ev["fields"])
    for e in edits:
        if e["field"] in doc:          # edit only a declared field
            doc[e["field"]] = e["new"]
    return doc


def footnotes(create_ev: dict, edits: list) -> list[str]:
    """Reader footnote: who / where (field) / when — in plain terms."""
    fn = [f"[created]  «{create_ev['author']}», {create_ev['at']}  "
          f"(fields: {len(create_ev['fields'])})"]
    for e in edits:
        fn.append(f"[edit]  field «{e['field']}» → «{e['new']}»  "
                  f"— by «{e['editor']}», {e['at']}")
    return fn


def audit(create_ev: dict, edits: list, claimed_current: dict | None = None) -> dict:
    """Legitimacy of the progression + localization of violations by field."""
    findings: list[tuple[str, str | None, str]] = []
    if not _verify(create_ev):
        findings.append(("BAD_CREATE_SIG", None, "creator's seal is invalid"))
    keepers = create_ev.get("keepers", {})
    kk = create_ev.get("keeper_keys", {})

    prev = create_ev
    verified: list = []          # ONLY clean edits make it into official (N-W7)
    for e in edits:
        f = e["field"]
        who = e.get("editor")
        bad = False
        if not _verify(e):
            findings.append(("BAD_SIG", f, "edit signature is invalid")); bad = True
        keeper = keepers.get(f)
        if keeper is None:
            findings.append(("NO_KEEPER", f, f"the field has no keeper (edited by «{who}»)")); bad = True
        elif who != keeper:
            findings.append(("EDIT_BY_NON_KEEPER", f,
                             f"the field was edited by «{who}», but the keeper is «{keeper}»")); bad = True
        elif e.get("pub") != kk.get(keeper):
            findings.append(("KEEPER_KEY_MISMATCH", f,
                             f"the key of «{who}» did not match the keeper's key")); bad = True
        if e.get("prev_hash") != _digest(prev):
            findings.append(("CHAIN_BROKEN", f, "the chain of edits is broken")); bad = True
        if not bad:
            verified.append(e)   # a clean edit — into the official state
        prev = e

    # official is assembled ONLY from verified edits (N-W7, audit 2026-07-26):
    # previously a forged edit's value entered official, and a consumer reading
    # only official got the forgery. Now it does not enter.
    official = rebuild(create_ev, verified)
    if claimed_current is not None:
        for k in set(official) | set(claimed_current):
            if official.get(k) == claimed_current.get(k):
                continue
            if k not in official:
                findings.append(("NEW_SLOT", k,
                                 f"an unsealed slot was slipped in: {claimed_current[k]!r}"))
            elif k not in claimed_current:
                findings.append(("MISSING_SLOT", k, "a sealed field vanished"))
            else:
                findings.append(("UNSIGNED_CHANGE", k,
                                 f"officially {official[k]!r} → in the document "
                                 f"{claimed_current[k]!r} (no keeper's signature)"))

    return {"intact": not findings, "findings": findings, "official": official}


def human_audit(result: dict) -> str:
    """Human-readable audit verdict."""
    if result["intact"]:
        return "CLEAN: structure and edits are legitimate (each field — by its own keeper)."
    lines = ["VIOLATIONS (localized by field):"]
    for kind, field, human in result["findings"]:
        lines.append(f"  • {kind}  [{field}] — {human}")
    return "\n".join(lines)
