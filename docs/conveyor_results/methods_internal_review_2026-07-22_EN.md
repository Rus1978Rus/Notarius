# Internal blind review of methods M1–M5 — result

DATE: 2026-07-22
CONVEYOR: 6 blind reviewers (3 angles × Sonnet/Opus) + a per-method synthesis.
Adversarial-by-instruction (FF-003). Blind: without the project/author name.
STATUS: baseline BEFORE the external vendors (prompt AD-20).

## Summary table

| Method | Consensus | soundness | honesty | Novelty |
|---|---|---|---|---|
| M1 Merkle segments | SOUND | 4.5 | 3.83 | STANDARD |
| M2 word-fingerprint | DISPUTED | 3.5 | 4.17 | KNOWN |
| M3 mod-97 + duplicates | WEAK | 2.67 | 3.33 | STANDARD/KNOWN |
| M4 event chain | SOUND | 3.67 | 4.33 | KNOWN |
| M5 boundary-detector | WEAK | 2.17 | 2.50 | RARE |

## THE HEADLINE: a REAL bug found and fixed in the code (M1)

All 6 reviewers independently pointed at **CVE-2012-2459**: the old code
duplicated an odd node, so that `root([A,B,C]) == root([A,B,C,C])`
— two different sets of segments produced one root. Reproduced in code,
confirmed. **Fixed (AD-21):** rewritten to the RFC 6962 structure
(split by the largest power of two, no duplication). Regression
test test_cve_2012_2459_no_collision. Plus signed_root() was added — a
signature over the pair (root, size) closes the second finding: an
inclusion proof does not prove the completeness of the set.

This is exactly what adversarial review is for: the blind conveyor caught
an error that the internal tests were missing. `REVIEW ≠ VALIDATION`
worked both ways — the review found what the "green tests" concealed.

## By method (agreed findings from ≥2 reviewers)

**M1 SOUND (after the fix).** Novelty — unanimously STANDARD (which is
exactly what we aimed for). Honesty dipped (3.83): the description glossed
over domain separation, tree shape, the trusted channel for the root.
Addressed in the code and docstring.

**M2 DISPUTED.** A 3/3 split, not a single BROKEN. Agreed point: a
fingerprint truncated to fit the carrier (4–6 words = 24–36 bits) is
brute-forceable by grinding; when both messages are controlled, the
threshold is a birthday 3N, not 6N. Reviewers' recommendations: fix a
minimum N, reconcile ALL words and their order, use the 11-bit BIP39
dictionary instead of a 6-bit one, split the dictionary by parity
(like the PGP word list). → a candidate for reworking human_fingerprint.

**M3 WEAK (4/6).** Technical consensus: a non-keyed mod-97 = zero
protection against deliberate tampering (recomputing is trivial);
duplicates save only from INDEPENDENT corruptions (a correlated failure —
one carrier/file/fire — kills all copies); the unweighted sum misses
transpositions (the positional IBAN mod-97 catches them). → strengthen:
positional weighting. The limit is broadly honest (we claimed "not
forgery"), but "human-verifiable" was overstated.

**M4 SOUND (4/6), honesty 4.33 — the best.** All reviewers called the
three self-declared limits (a/b/c) honest — rare good self-criticism. The
agreed attacks lie BEYOND the limits: split-view/fork without an external
anchor; theft of an unrevoked key; rewriting from genesis while holding
the keys; self-declared time. All are known limits of signed chains
without an external anchor/log. → the same open moves as in SEMANTIC_TRACE
(external timestamp, append-only log, PKI).

**M5 WEAK (6/6), honesty 2.50 — the worst.**
- E1 (length-witness): the length is unauthenticated and attacker-
  controlled → any attack reduces to a length-preserving one; a direct
  CONTRADICTION — a human-visible glyph count by definition does not count
  invisible insertions (only a byte count in software catches them). This
  reinforces the already-made decision AD-3 (length-witness → diagnostic).
- E2 (bracket): a bootstrap problem — a reader without the language can't
  establish what is a delimiter and what is content without an agreed
  convention; a delimiter collision without an escaping rule breaks the
  segmentation. → a direct input for MSL/MIP: needed are (1) a visual
  distinction of the delimiter (the cartouche lesson, already in the
  genesis doc) and (2) an escaping rule.

## What was done as a result

1. **Fixed the M1 code** (CVE-2012-2459 → RFC 6962) + signed_root + 3 tests.
2. The other findings — candidates for rework (M2 BIP39/min-N, M3
   positional weighting, M4 external anchor, E2 escaping) — queued,
   not silently dropped.
3. The baseline is ready to be consolidated with the external vendors (AD-20).

## Honest caveat

These are LLM reviews (`LLM_OUTPUT ≠ VERIFIED_COPY`) — a strong signal, not
proof. The external vendors (other models) are an independent check;
consolidating when the answers arrive.
