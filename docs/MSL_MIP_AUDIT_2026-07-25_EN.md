# Audit of the sibling project MSL/MIP (line by line) + what was taken

DATE: 2026-07-25. STATUS: LLM_GENERATED (3 parallel agents, read-only).
BASIS: clone of rus1978rus/msl_mip @47809150. THE AUTHOR OF BOTH — Ruslan
Malyavsky.
BOUNDARY: msl_mip was NOT modified; only data/discipline were taken into
NOTARIUS.

## What MSL/MIP is (honestly)

The "Foundation Layer" — a research platform for structural analysis of signs
("what a sign does in context"), witness-not-judge, status WORKING_DRAFT. 220
files, but the detector code is a small part; ~90% is one author's pipeline
scaffolding (CONVEYOR_PACKET_*, AUTHOR_DECISION_*, status trackers).
Architecture: markdown "cards" of signs → matchers → single_sign → sequence →
runtime.

## The key conclusion: NOTARIUS's detection is ALREADY STRONGER

NOTARIUS carries the same author's DNA through the Vakhter port (AD-33).
Comparison:

| Capability | NOTARIUS | MSL/MIP | Who's stronger |
|---|---|---|---|
| Invisible characters/word-split | detect._zw_wordsplit | witness + context | both |
| Bidi (Trojan-Source) | _bidi_imbalance ✅ | no balance check | **NOTARIUS** |
| Tag-smuggle / VS-carrier | _tag_smuggle/_vs_carrier ✅ | only a witness class | **NOTARIUS** |
| Homoglyphs | homoglyph.py (skeleton) | confusables NOT in the runtime | **NOTARIUS** |
| Fail-closed guard | safe_analyze ✅ | fail-open in shadow | **NOTARIUS** |
| Class-138 (Cf∩DI) | _monitored | _monitored_138_set | duplicate |

HONESTLY ABOUT HOMOGLYPHS (the author's main question): MSL/MIP has NO working
homoglyph-detector code. skeleton/UTS#39 is a solution on paper (3 ARCH
decisions + an open CONFUSABLE_FRONT, "no code, the pipeline never ran"); their
runtime catches look-alikes only through manually entered per-card edges
SIGN_RELATIONS, and the classic `paypаl.com` passes through them SILENTLY (their
own measurement confirms it).

## WHAT WAS TAKEN (data + discipline, not code)

1. **UTS#39 confusables — DATA (the main value).** We read through the vendored
   `tools/sources/17.0.0/confusables.txt` (Unicode 17.0.0). From it we derived the
   ASCII-target subset (masquerading as Latin) → notarius/data/
   confusables_ascii.txt, **1861 look-alikes** (it was ~50 by hand). homoglyph.py
   was rewritten to a real `skeleton()` (NFD→replace→NFD). Now Greek/fullwidth/
   mathematical/ligatures and the IDN-homograph `paypаl.com` are caught (it was a
   failure in both projects). Provenance and the Unicode license — in the file
   header.
2. **The "no-auto-escalate" gate — DISCIPLINE (their single best asset).** Ported
   as a test: the layer is ALWAYS advisory, no field carries a blocking/escalating
   action (TestNoAutoEscalate). Previously this was only a principle in a comment —
   now it's fixed by a test.

## WHAT WAS LEFT (someone else's architecture / process)

- The card system (`cards/*.md`, 9 dossiers) — dense machine data is scarce, our
  _CP/_monitored is denser; msl_mip itself admits "scale is not by cards."
- The "homoglyph = relation" model (SIGN_RELATIONS) — hard-wired to their
  matchers/sequence/enum; for our axis (provenance/tracing) it's foreign.
- The pipeline machinery (CONVEYOR_PACKET/AUTHOR_DECISION/HANDOFF/status trackers)
  — a multi-model review ritual, not a portable asset.

## GENUINELY NEW BUT NOT TAKEN NOW (a candidate for the future)

**Domain/URL awareness** — the one thing we don't have at all and that directly
hits the top vertical (BEC / substitution of a payment-detail link):
- `core/public_suffix.py` — public suffixes, three-tier degradation
  (live→cache→embedded) with an honest source signal + a hermetic mode;
- `sequence_engine._detect_context_at` + `_SCOPE_RISK` — distinguishing
  HOST/USERINFO/EMAIL/PATH per RFC 3986; an invisible character/look-alike **in
  the domain** → HIGH, in the path → MEDIUM; unmasking `goog‹ZWSP›le.com →
  google.com`.

RECOMMENDATION: when we take on the finance-document vertical, port this domain
awareness (it gives "a look-alike specifically in the link/domain = high risk").
For now we do NOT drag it in — outside the current step; recorded as a candidate.

## Bottom line

Exactly the right, on-point things were taken: **a real UTS#39 look-alike
database** (a coverage jump of ×37) + **the advisory-invariant discipline**. We
did not borrow detection code — ours is already ahead. Domain awareness is the
honest next candidate for the vertical. 19/19 test files green; msl_mip untouched.
