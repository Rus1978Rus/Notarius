# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — semantic tracing of an element (the project core).

Implements what the document described but never built (§16 "first
prototype", §17 "Notarius tracing (assemble the trace)", §9 the state
model). An element's semantic trace is a CHAIN of signed events:

    CREATED → TRANSFORMED → TRANSFERRED → REVIEWED → ...

Each event:
  - carries value_hash (SHA-256 of the element's value at this point) and
    cp_len (diagnostic, AD-3);
  - is signed by an actor (Ed25519) — the "who did it" binding;
  - is linked to the previous one via prev_hash — an append-only chain,
    any tampering breaks the link (TRACE_EXISTS ≠ TRACE_CONTINUOUS, §4).

Verification yields a human-readable report: where the break is, who
signed last, what state (§9: INTACT / MODIFIED / BROKEN /
ORIGIN_UNKNOWN). Advisory mode — it does not block.

CANDID LIMITS (catalog of 7 defects + external review AD-22):
  - Self-attestation (#1): an actor signs THEIR OWN event; an actor with
    a valid key can write a false-but-signed event. The trace LOCALIZES
    responsibility (AD-10: TRACE_LOCATES_THE_LIE), but does not prove
    truthfulness (SIGNED ≠ NATIVE).
  - Time (#3): at — self-declared, with no external anchor.
  - Silent omission: the chain proves continuity of the RECORDED events,
    not that every real event was recorded (E-Continuity Viking:
    "degradation from a missing event").
  - FORK / equivocation (all 4 external vendors found it, AD-22): an actor
    with a valid key signs TWO continuations from one point and shows them
    to different recipients. Both branches are internally valid — without
    an EXTERNAL witness (append-only log / shared anchor) the fork is not
    detected. verify_trace does NOT detect a fork.
  - TRUNCATION (valid-prefix truncation): presenting a prefix of the chain
    looks valid. Detected ONLY if the verifier INDEPENDENTLY knows the
    current head (expected_head parameter). Otherwise — not.
  - actor ≠ identity: the signature identifies the KEY HOLDER, not the
    person (GPT: SIGNING_KEY ≠ REAL_ACTOR). last_signer is the claimed
    actor of the key, not a proven identity.
Review conclusion: the only complete answer to fork+truncation is an
external trusted head anchor (transparency log / distributed anchoring)
plus key rotation/revocation. That is outside the scope of a local trace.

M4 CLOSURE (AD-36): witness-cosigning is implemented in notarius/cosign.py —
external witnesses co-sign the head after checking consistency;
verify_witnessed_trace() catches forks (a branch without quorum / head ≠
the witnessed one) and truncation. It is an external layer over verify_trace.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

# Event types and their effect on the element's value.
VALUE_CHANGING = {"CREATED", "TRANSFORMED"}      # changing value_hash is legitimate
VALUE_PRESERVING = {"TRANSFERRED", "REVIEWED"}   # the value must NOT change


def _canonical(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _value_hash(value: str) -> str:
    return hashlib.sha256(unicodedata.normalize("NFC", value).encode()).hexdigest()


def _event_digest(event: dict) -> str:
    """Hash of the whole event (signature included) — the link for the next one."""
    return hashlib.sha256(_canonical(event)).hexdigest()


def _make_event(element_id: str, value: str, event_type: str, origin: str,
                actor_id: str, actor_priv: bytes, at: str, prev_hash: str | None) -> dict:
    value = unicodedata.normalize("NFC", value)
    body = {
        "element_id": element_id,
        "type": event_type,
        "origin": origin,
        "actor": actor_id,
        "value_hash": _value_hash(value),
        "cp_len": len(value),
        "at": at,                 # self-declared (no external anchor)
        "prev_hash": prev_hash,   # None for the first event
    }
    sk = SigningKey(actor_priv)
    sig = sk.sign(_canonical(body)).signature.hex()
    return {**body, "sig": sig, "actor_pub": bytes(sk.verify_key).hex()}


def new_trace(element_id: str, value: str, origin: str,
              actor_id: str, actor_priv: bytes, at: str) -> list[dict]:
    """Start a trace: the CREATED event."""
    return [_make_event(element_id, value, "CREATED", origin,
                        actor_id, actor_priv, at, prev_hash=None)]


def append_event(trace: list[dict], value: str, event_type: str,
                 actor_id: str, actor_priv: bytes, at: str,
                 origin: str | None = None) -> list[dict]:
    """Append an event to the trace, linking it to the previous by hash."""
    prev = trace[-1]
    ev = _make_event(prev["element_id"], value, event_type,
                     origin or prev["origin"], actor_id, actor_priv, at,
                     prev_hash=_event_digest(prev))
    return trace + [ev]


def verify_trace(trace: list[dict], trusted_keys: dict[str, bytes] | None = None,
                 current_value: str | None = None,
                 expected_head: str | None = None) -> dict:
    """Walk the trace and return a human-readable report on any break.
    trusted_keys: actor_id -> public key (opt. — binding to an identity).
    current_value: the actual value right now (opt.).
    expected_head: the independently known hash of the current head (opt.) —
    the ONLY local defense against truncation (AD-22); without it,
    truncation of a valid prefix is not detected. A fork is not detected at
    all."""
    report = {"element_id": trace[0]["element_id"] if trace else None,
              "status": "INTACT", "state": "INTACT",
              "break_at_step": None, "last_signer": None, "reasons": []}

    def flag(state, step, reason):
        report["state"] = state
        report["status"] = "TRACE_BREAK_DETECTED"
        if report["break_at_step"] is None:
            report["break_at_step"] = step
        report["reasons"].append(f"step {step}: {reason}")

    prev = None
    for step, ev in enumerate(trace):
        body = {k: ev[k] for k in ("element_id", "type", "origin", "actor",
                                   "value_hash", "cp_len", "at", "prev_hash")}
        # 1. event signature
        try:
            VerifyKey(bytes.fromhex(ev["actor_pub"])).verify(
                _canonical(body), bytes.fromhex(ev["sig"]))
            report["last_signer"] = ev["actor"]
        except (BadSignatureError, ValueError, KeyError):
            flag("BROKEN", step, f"signature of actor {ev.get('actor')} is invalid")
        # 2. binding key to identity (if a trusted set is given)
        if trusted_keys is not None:
            exp = trusted_keys.get(ev["actor"])
            if exp is None or exp.hex() != ev["actor_pub"]:
                flag("ORIGIN_UNKNOWN", step,
                     f"key of actor {ev['actor']} is not in the trusted set")
        # 2b. element_id continuity (N-W4, audit 2026-07-26): a foreign
        # element_id mid-chain (valid signature) must NOT pass — otherwise
        # the trace of "element A" silently continues as element B.
        if trace and ev.get("element_id") != trace[0].get("element_id"):
            flag("BROKEN", step,
                 f"element_id changed: expected {trace[0].get('element_id')!r}, "
                 f"event has {ev.get('element_id')!r}")
        # 3. chain link
        if step == 0:
            # the first must be CREATED (N-W5, §9 lifecycle)
            if ev.get("type") != "CREATED":
                flag("BROKEN", step,
                     f"first event is not CREATED but {ev.get('type')!r} "
                     f"(the lifecycle begins with CREATED)")
            if ev["prev_hash"] is not None:
                flag("BROKEN", step, "first event has a prev_hash")
        else:
            if ev["prev_hash"] != _event_digest(prev):
                flag("BROKEN", step, "prev_hash does not match — the chain is broken")
            # 4. value continuity
            if ev["type"] in VALUE_PRESERVING and ev["value_hash"] != prev["value_hash"]:
                flag("MODIFIED", step,
                     f"value changed on {ev['type']} (it must be preserved)")
        prev = ev

    # 5. reconcile against the actual current value
    if current_value is not None and trace:
        if _value_hash(current_value) != trace[-1]["value_hash"]:
            flag("MODIFIED", len(trace) - 1,
                 "the actual value does not match the trace's last event")

    # 5b. screening the CONTENT of the current value (AD-33, engine from "Vakhter").
    # A separate axis from the crypto state: the chain may be INTACT while the
    # value is POISONED by a zero-width char. NFC (in _value_hash) does NOT strip
    # zero-width — the hash is stable, the signature valid, yet
    # "admin<ZWSP>istrator" ≠ "administrator". This is the §4 principle:
    # CONTAINER_INTACT ≠ ELEMENT_CLEAN. Advisory; it does not change
    # state/status — it reports separately.
    report["content_scan"] = None
    if current_value is not None:
        from notarius.scanner import scan_hardened
        sc = scan_hardened(current_value)
        report["content_scan"] = {"risk": sc["risk"], "signature": sc["signature"]}
        if sc["risk"] != "OK":
            report["reasons"].append(
                f"CONTENT: {sc['risk']} ({sc['signature']}) — the value is "
                f"signed and valid, but carries a hidden manipulation "
                f"(CONTAINER_INTACT ≠ ELEMENT_CLEAN)")

    # 6. truncation defense — only with an independently known head (AD-22)
    if expected_head is not None and trace:
        if _event_digest(trace[-1]) != expected_head:
            flag("BROKEN", len(trace) - 1,
                 "head does not match the expected one — truncation or fork "
                 "(TRUNCATED_OR_FORKED)")

    # 7. Time is self-declared if any event lacks an external anchor.
    # Backdating CANNOT be ruled out without an anchor (OTS/witness quorum) —
    # INTACT applies to the CHAIN, not to TIME (defect #3, exposed by Kimi's
    # run, AD-77/79). It does not change status (time forgery cannot be
    # prevented), but it makes the limit explicit so INTACT is not read as
    # "time is proven".
    report["time_proven"] = bool(trace) and all(ev.get("anchor") for ev in trace)
    if not report["time_proven"]:
        report["reasons"].append(
            "TIME IS SELF-DECLARED: 'at' is not confirmed by an external anchor "
            "(OTS/quorum) — backdating is NOT ruled out; INTACT applies to the "
            "chain, not to time (defect #3)")

    report["steps"] = len(trace)
    if report["status"] == "INTACT":
        note = "trace is continuous, all events signed"
        if expected_head is None:
            note += "; NOTE: without expected_head, truncation/fork are not checked"
        report["reasons"].append(note)
    return report


def human_report(report: dict) -> str:
    """Report in the §16 form — for a human, not a machine."""
    lines = [f"element: {report['element_id']}",
             f"status: {report['status']}",
             f"state: {report['state']}",
             f"last_signer: {report['last_signer']}"]
    if report["break_at_step"] is not None:
        lines.append(f"break_at_step: {report['break_at_step']}")
    for r in report["reasons"]:
        lines.append(f"  - {r}")
    return "\n".join(lines)
