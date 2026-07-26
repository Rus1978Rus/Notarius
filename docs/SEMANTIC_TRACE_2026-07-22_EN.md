# Semantic tracing — the Notarius core (built)

DATE: 2026-07-22
BASIS: the author's request "semantic tracing?"; an implementation of what the
document described but had not built — §16 "first prototype," §17 "Notarius
tracing (assemble the trace)," §9 the state model.
CODE: notarius/trace.py; TESTS: tests/test_trace.py (9, green).

## What it is

The semantic trace of a data element — a **chain of signed events**:

```
CREATED → TRANSFORMED → TRANSFERRED → REVIEWED → ...
  each event: value_hash + cp_len + actor + Ed25519 signature
              + prev_hash (link to the previous one)
```

This brings together everything built in the session:
- Ed25519 (envelope_v2) — "who did it," verifiable by a third party;
- the prev_hash hash chain — continuity (`TRACE_EXISTS ≠ TRACE_CONTINUOUS`, §4);
- the §9 state model — INTACT / MODIFIED / BROKEN / ORIGIN_UNKNOWN;
- a human-readable break report — the AD-8 niche.

## What it gives (verified by code)

Verification walks the trace and answers in the §16 form:
```
element: amount
status: TRACE_BREAK_DETECTED
state: MODIFIED
last_signer: checker-3
break_at_step: 1
  - step 1: the actual value does not match the trace's last event
```

Catches (tests):
- a chain break (corrupting an event breaks prev_hash);
- an unexpected value change during REVIEWED/TRANSFERRED (which should be
  preserved) — but allows it during CREATED/TRANSFORMED;
- a foreign/untrusted actor key → ORIGIN_UNKNOWN;
- a forged event (body changed, signature unchanged);
- a mismatch of the actual value with the trace's last event.

## Where exactly the break is localized

The report names the **step** and the **last signer** — that is
`TRACE_LOCATES_THE_LIE` (AD-10). Not "someone forged it," but "the trace is
continuous up to step 2, at step 3 the value changed, the last signer
was checker-3." The forensic thesis of §11 in working form.

## Honest boundaries (the catalog of 7 defects — not overclaim)

1. **Self-attestation (№1) is NOT closed.** An actor signs THEIR OWN event;
   an actor with a valid key can write a false-but-signed event
   — the test test_self_attestation_not_closed shows it: a lie with a valid
   signature passes as INTACT. The trace LOCALIZES responsibility
   (who signed), but does not prove truthfulness (`SIGNED ≠ NATIVE`).
2. **Time (№3).** The `at` field is self-declared without an external anchor
   (OpenTimestamps/RFC 3161). MODIFICATION_WINDOW is unprovable without it.
3. **Silent omission.** The chain proves the continuity of the
   RECORDED events, not that all real events were recorded.
   This is the direct lesson of the grandfather E-Continuity (Viking): "a system degrades
   from the absence of an event." An actor who simply does NOT record a step
   leaves a silent hole — the trace does not see it.
4. **Advisory mode.** The report does not block (the principle of early
   Notarius); the decision is the receiver's/the policy's.

## The vertical link along E-Continuity

The semantic trace is the parent's continuity chain, brought down to
the element level:
```
E-Continuity: Object→Metadata→…→Custody→Institution→Mission
FO-015:       DATA→CLAIM→STATUS→TRUST→ACTION
Notarius:     CREATED→TRANSFORMED→TRANSFERRED→REVIEWED (element event)
```
Each link is a boundary that survives the handoff (pattern AD-17). A break in the
event chain = `BOUNDARY_BREAK = FIRST_DETECTABLE_SIGNAL`.

## What remains open (for AUTHOR_DECISION)

- Bind `at` to an external timestamp (close defect №3).
- A Merkle root over the set of a document's elements (algorithms/) →
  a signature of the whole document with a single signature + a trace per element.
- Binding actor_pub to an identity (PKI/eIDAS) — close ORIGIN_UNKNOWN
  with a real trusted set of keys.
- Against silent omission — periodic re-checking of the trace
  (proof-testing from AD-14: "degradation from the absence of an event").
