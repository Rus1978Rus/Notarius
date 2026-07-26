# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — the mandatory ROUTE: catch a missing step (AD-92).

A new LAYER (not plumbing, per rule AD-83): it is born from our own
semantic tracing and pulls in nothing borrowed.

The trace chain (trace.py) proves that what is RECORDED is continuous and
untouched. But it does NOT see what is absent from the record: a missing
step is not forgery but an ABSENCE, and a whole chain stays silent about
it (silent omission — the only real gap from both external audits, AD-90
"C" and AD-91).

This layer checks the trace against a MANDATORY ROUTE (the contract):

    route = [
        {"step": "CREATED",    "by": "Production"},
        {"step": "CHECKED",    "by": "Warehouse"},
        {"step": "RELEASED",   "by": "Dispatch"},
    ]

and localizes the violation by step:
  MISSING_STEP  — a mandatory step never appeared at all (omission);
  WRONG_SIGNER  — the step is there but signed by the WRONG party (role
                  spoofing: you cannot "self-sign" a check and slip through);
  OUT_OF_ORDER  — the step exists under the right party, but out of order
                  (e.g. RELEASED before CHECKED);
  UNKNOWN_ROLE  — the route names a role with no known key (contract error);
  CHAIN_BROKEN  — the trace itself is broken (verify_trace) → the route
                  cannot be judged.

REPEATS = a counter: "5 inspection rounds" is described by five identical
route entries; greedy in-order matching requires exactly that many correctly
signed steps, otherwise the missing ones → MISSING_STEP.

LIMITS (candidly):
  - The contract (route + authorized_keys) is a TRUSTED policy input
    (from the client/regulator, out-of-band), NOT from whoever presents the
    trace: otherwise an attacker would declare an empty route. Like trusted_keys.
  - SIGNED ≠ NATIVE (defect #1): a matched step proves that the AUTHORIZED
    party signed a "check done" event, NOT that the check actually happened
    in the world. The layer catches OMISSION and ROLE SPOOFING and localizes
    responsibility — it does not judge physical truth.
  - Fail closed: a missing step (including from tail truncation) → NOT
    complete, not a false "complete". Dangerous truncation that hides LATER
    steps is closed by expected_head/cosign, not here.
  - Time is self-declared (defect #3): the route checks the ORDER OF THE
    RECORD, not the absolute real time of the steps.
"""

from __future__ import annotations

from notarius.trace import verify_trace, _canonical  # same canon, no drift

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def _sig_ok(ev: dict) -> bool:
    """Independent signature check of a single trace event (the same body
    field set as in trace.verify_trace) — so the layer stays sound even
    when verify_chain=False."""
    try:
        body = {k: ev[k] for k in ("element_id", "type", "origin", "actor",
                                   "value_hash", "cp_len", "at", "prev_hash")}
        VerifyKey(bytes.fromhex(ev["actor_pub"])).verify(
            _canonical(body), bytes.fromhex(ev["sig"]))
        return True
    except (BadSignatureError, ValueError, KeyError):
        return False


def check_route(trace: list, route: list, authorized_keys: dict,
                verify_chain: bool = True) -> dict:
    """Check the trace against the mandatory route. Localizes by step.

    trace            — a trace from trace.py (list of signed events);
    route            — [{"step": TYPE, "by": role}, ...] in order;
    authorized_keys  — {role: actor_pub_hex} the trusted role contract;
    verify_chain     — run verify_trace first (default yes): on a broken
                       trace the route cannot be judged.

    Returns: {"complete": bool, "findings": [(kind, step, human)],
              "matched": [{"step","by","at_step"}]}."""
    findings: list[tuple[str, str | None, str]] = []

    # 0. Integrity of the trace itself — the foundation. Fail closed.
    if verify_chain:
        rep = verify_trace(trace)
        if rep["status"] != "INTACT":
            why = rep["reasons"][0] if rep["reasons"] else "break"
            findings.append(("CHAIN_BROKEN", None,
                             f"trace is broken ({why}) — the route cannot be judged"))
            return {"complete": False, "findings": findings, "matched": []}

    # 0b. Continuity of the SUBJECT — ALWAYS, even with verify_chain=False.
    # Otherwise a genuinely signed step of ANOTHER subject (e.g. a real
    # warehouse check of someone else's batch) gets spliced into this trace
    # and reads as a completed step. The layer must not depend on whether the
    # caller enabled the chain check. (N-W4 at the route level.)
    if trace:
        eid = trace[0].get("element_id")
        for k, ev in enumerate(trace):
            if ev.get("element_id") != eid:
                findings.append(("CHAIN_BROKEN", None,
                                 f"step {k}: subject changed "
                                 f"({ev.get('element_id')!r} ≠ {eid!r}) — "
                                 f"a step of a foreign subject spliced in"))
                return {"complete": False, "findings": findings, "matched": []}

    n = len(trace)
    used: set[int] = set()        # trace events already matched

    def unused_correct(t: str, key: str | None) -> list[int]:
        """Events of type t correctly signed by the right key, not yet
        counted (otherwise repeat-steps would falsely read as OUT_OF_ORDER)."""
        if key is None:
            return []
        return [j for j, ev in enumerate(trace)
                if j not in used and ev.get("type") == t
                and ev.get("actor_pub") == key and _sig_ok(ev)]

    def wrong_signer_exists(t: str, key: str | None) -> bool:
        return any(ev.get("type") == t and ev.get("actor_pub") != key
                   and _sig_ok(ev) for ev in trace)

    matched: list[dict] = []
    ptr = 0                       # greedy IN-ORDER matching
    for req in route:
        t, role = req["step"], req["by"]
        key = authorized_keys.get(role)

        found_at = None
        if key is not None:
            j = ptr
            while j < n:
                ev = trace[j]
                if (j not in used and ev.get("type") == t
                        and ev.get("actor_pub") == key and _sig_ok(ev)):
                    found_at = j
                    break
                j += 1

        if found_at is not None:
            matched.append({"step": t, "by": role, "at_step": found_at})
            used.add(found_at)
            ptr = found_at + 1
            continue

        # Diagnosing a miss — the most precise localization.
        if key is None:
            findings.append(("UNKNOWN_ROLE", t,
                             f"the route names role «{role}» with no known key"))
        elif unused_correct(t, key):   # the right party exists, but earlier
            findings.append(("OUT_OF_ORDER", t,
                             f"step «{t}» ({role}) exists, but out of order"))
        elif wrong_signer_exists(t, key):
            findings.append(("WRONG_SIGNER", t,
                             f"step «{t}» signed by NOT «{role}» — role spoofing "
                             f"(a self-signed step is not counted)"))
        else:
            findings.append(("MISSING_STEP", t,
                             f"mandatory step «{t}» ({role}) is missing"))

    return {"complete": not findings, "findings": findings, "matched": matched}


def human_route(result: dict) -> str:
    """Human-readable verdict on the route."""
    if result["complete"]:
        steps = " → ".join(m["step"] for m in result["matched"])
        return f"ROUTE COMPLETE: all mandatory steps present, in order " \
               f"and by their responsible parties ({steps})."
    lines = ["ROUTE INCOMPLETE (localized by step):"]
    for kind, step, human in result["findings"]:
        lines.append(f"  • {kind}  [{step}] — {human}")
    return "\n".join(lines)
