# Blind prompt for an external review of signing/identification methods

DATE: 2026-07-22
PURPOSE: run the methods (Merkle segments, word-fingerprint, redundant
ID, semantic tracing, non-standard ones) through external AI vendors
adversarially and blind. The answer format is for merging via the same
judges as the previous rounds.
BLINDNESS: the prompt does NOT contain the project name, the author, or any hint of which
method is preferred (protection against the halo effect and flattery).
DISCIPLINE: closes FF-003 (`MULTI_MODEL_REVIEW ≠ ADVERSARIAL_PROCESS`)
via adversarial-by-instruction.

INSTRUCTION: copy everything between the lines into another AI. Save the answer
to docs/vendor_answers/methods_<vendor>_<date>.md.

---

You are an independent technical reviewer in cryptography and data-integrity
systems. Answer IN RUSSIAN. Your task is NOT to praise, but to
BREAK. By default treat each method as overrated until
proven otherwise. You do not know who the author of the methods is or which one is
preferred — evaluate blind and hard. Some of the methods may be
standard (then say so — "this is known, not new"), some —
naive, some — with an honest or DISHONEST boundary of coverage.

You are given a set of methods for signing, identifying, and confirming
SEGMENTS of information or information IN WHOLE on various carriers
(digital, paper, stone, metal — down to being read across thousands of years).
For each method you are given the MECHANISM, the CLAIMED PROPERTY, and the CLAIMED
BOUNDARY (what the method supposedly does NOT do).

Your job for each method:
1. Check whether the mechanism delivers the claimed property. If not —
   provide a CONCRETE input/scenario where it breaks.
2. Find the HIDDEN overclaim: is the boundary declared honestly, or is
   there a bigger hole hiding under it than admitted?
3. Assess novelty: STANDARD (known for decades) / KNOWN
   (analogues exist) / RARE / NEW. Name the nearest analogue, if any.
4. Verdict: SOUND / WEAK / BROKEN.
5. Scores 1–5: soundness (the mechanism does what is claimed),
   honesty (the boundary is admitted honestly), usefulness (someone actually needs it).

=== METHODS ===

M1. ROOT + INCLUSION PROOF.
MECHANISM: a set of segments is folded into a binary hash tree;
ONE root is signed; membership of any segment is proven by
a chain of neighboring hashes of length log(n).
PROPERTY: one segment can be confirmed without having or revealing
the others; changing any segment changes the root.
BOUNDARY: this is identification and integrity, not proof of the truthfulness
of a value; signing the root binds the author, but not truthfulness.

M2. WORD-FINGERPRINT.
MECHANISM: the SHA-256 of the content is mapped to a short list of ordinary
words (6 bits per word from a fixed dictionary of 64 words).
PROPERTY: a human reconciles the fingerprint across DIFFERENT carriers (screen vs
stone vs spoken aloud) without software and without manually computing the hash.
BOUNDARY: N words ≈ 6·N bits — protection against accidental divergence and convenient
reconciliation, NOT full resistance to a targeted collision search.

M3. MANUAL CHECK DIGIT + DUPLICATES.
MECHANISM: a check number is added to the identifier (sum of character
codes mod 97, computed by hand), the string is duplicated k times.
PROPERTY: survives partial carrier damage (one surviving
copy whose check adds up is enough); catches id substitution without
recomputing the check; verifiable by a human without a computer.
BOUNDARY: a mod-97 check detects random corruption, but does NOT protect
against deliberate forgery (an attacker will recompute the check).

M4. CHAIN OF SIGNED EVENTS (element trace).
MECHANISM: a chain of events is kept over the element (CREATED / TRANSFORMED
/ TRANSFERRED / REVIEWED); each event carries a hash of the value, the actor's
(asymmetric) signature, and a hash of the previous event; on verification the chain
is walked and a human-readable report is emitted with the step number of the break and
the last signer.
PROPERTY: localizes WHERE and WHO — "the trace is intact up to step 2, at step 3
the value changed during an operation that should not change it,
the last signer was actor X."
BOUNDARY (admitted): (a) an actor with a valid key can write a
false-but-signed event — the trace localizes responsibility, but does not
prove truthfulness; (b) the event time is self-declared without an external
anchor; (c) if an actor simply does NOT record a step, the chain does not see the silent hole.

M5. THE BOUNDARY AS A DETECTOR (two non-standard offerings).
E1: a visible control quantity of the block (character count), declared in
the manifest; any insertion/deletion, including invisible characters, breaks the
length check. BOUNDARY: does not catch an equal-length substitution.
E2: self-describing delimiters that close units of meaning — a bracket
around a word, a different bracket around a sentence — such that a future
reader WITHOUT knowledge of the language finds the boundaries of words and sentences and
the reading direction. BOUNDARY: gives "here is a unit + its boundaries +
structure," but NOT the meaning; the delimiter itself must visually differ
from the content.

=== ANSWER FORMAT (for each M1–M5) ===
- METHOD: Mn
- VERDICT: SOUND / WEAK / BROKEN
- BREAK SCENARIO: a concrete input/situation (or "not found")
- HIDDEN OVERCLAIM: what is claimed beyond the real (or "boundary is honest")
- NOVELTY: STANDARD/KNOWN/RARE/NEW + nearest analogue
- SCORES: soundness _/5, honesty _/5, usefulness _/5

=== AT THE END (rigor check) ===
1. Which method would you REJECT first and why.
2. One method/approach missing from the set for "signing on
   various carriers + confirmation."
3. Is there among the five even one boundary that is admitted DISHONESTLY (the real
   hole is bigger than declared)? Name it.

---

## Where to file the answers

`docs/vendor_answers/methods_<vendor>_<date>.md`. Then — through the same
conveyor judges (soundness-skeptic + prior-art-skeptic) for merging with the
internal evaluation.
