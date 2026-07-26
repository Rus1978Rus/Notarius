# Methods M1–M5 — external conveyor summary (5 sources)

DATE: 2026-07-22
SOURCES (independent): internal conveyor (6 reviewers), Kimi,
Grok, GPT, Gemini. Copilot EXCLUDED — its answer matched Gemini's
verbatim (FF-003: don't count one vote twice).
BLINDNESS: all blind, without the project/author name. Adversarial-by-instruction.

## Verdict matrix

| Method | Internal | Kimi | Grok | GPT | Gemini | RESULT |
|---|---|---|---|---|---|---|
| M1 Merkle | SOUND | SOUND | SOUND | SOUND | SOUND | **SOUND** (unanimous) |
| M2 word-fingerprint | DISPUTED | SOUND | WEAK | WEAK | WEAK | **WEAK** |
| M3 mod-97+duplicates | WEAK | WEAK | WEAK | BROKEN | BROKEN | **WEAK→BROKEN** |
| M4 event chain | SOUND | WEAK | WEAK | WEAK | WEAK | **WEAK** |
| M5 E1 length | WEAK | WEAK | WEAK | WEAK | WEAK | **WEAK** (unanimous) |
| M5 E2 bracket | — | SOUND | WEAK | WEAK | WEAK | **WEAK/DISPUTED** |

**Reject first: M3 — unanimous across all 5 sources.**

## Converging findings (what ≥3 sources found independently)

1. **M3 is blind to transpositions** (AB==BA, a non-positional sum) — the
   most common manual error; the IBAN mod-97-10 is positional, ours was
   not. + a non-keyed check = zero protection against forgery. "Catches
   tampering" is an internal contradiction with the stated limit. Found by
   ALL 5.
2. **M4 fork/equivocation + truncation** — a signed chain does NOT prove
   the history's uniqueness/currency; a fork and a tail truncation both
   yield valid contradictory histories. This was NOT in my stated limits.
   Found by ALL 4 external vendors independently.
3. **M2's short fingerprint is brute-forceable** — 6 words = 36 bits =
   seconds; a birthday attack of 3N when controlling both messages. "Not
   full strength" is an understatement (Gemini: "a paper door doesn't stop
   an axe"). Found by all 5.
4. **M1 domain separation of leaf/node + leaf position** — without the
   0x00/0x01 prefixes there's a second-preimage attack; without the
   leaf index the proof doesn't pin which instance. Found by
   internal+Kimi+GPT+Gemini.
5. **M5/E1 = a diagnostic, not a barrier** — the length is unauthenticated,
   attacker-controlled; a length-preserving substitution + a homoglyph
   (a→а); a human doesn't count invisibles (only software does).
   Unanimous.
6. **M5/E2 bootstrap** — a reader without the language can't tell a
   delimiter from content without a convention; escaping + a legend +
   a visual distinction are needed ("the Rosetta Stone problem,"
   "[ mistaken for a letter").

## What's missing (Kimi, GPT, Gemini, Grok converged)

- **An external trusted anchor + a re-signing ritual** — distributed
  anchoring of the head (a transparency log / blockchain / replicated
  copies) + algorithm migration over time. One move closes fork+truncation
  (M4), same-carrier (M2), data-availability (M1).
- **Correction codes (Reed-Solomon) / a physical binding (PUF)** —
  recovery on damage and binding of the record to the carrier.
- **Kimi's meta-conclusion:** "all five survive the carrier but not the
  ALGORITHM" — signatures die sooner than stone. Without an update ritual,
  longevity is illusory.

## What was FIXED as a result (AD-22, code + tests)

| Finding | Action |
|---|---|
| M3 transpositions | `mod97_check` → `positional_check` (weight by position); test `test_positional_catches_transposition` |
| M3 overclaim "catches tampering" | removed from the docstring; restated as "random corruption, not authentication" |
| M4 fork/truncation out of scope | added to the honest limits in the docstring; the `expected_head` parameter detects truncation when the head is known; test |
| M4 actor≠identity | last_signer flagged as the key owner (SIGNING_KEY ≠ REAL_ACTOR) |
| M2 short N | default 6→12 words (36→72 bits); a limit note on the cost of attack and BIP39 |
| M1 leaf position | the leaf commits to index+length; `verify_segment` requires the index |
| M1 CVE-2012-2459 | already fixed earlier (AD-21, RFC 6962) |

Left out of local-code scope (candidates, not silently): an external
anchor + transparency log (M4 fork), Reed-Solomon/PUF, a re-signing
ritual; for E2 — an escaping rule and a legend (input to the MSL/MIP
genesis).

## Agreement of the internal and external conveyors

The internal conveyor (before the vendors) and the 4 external vendors
converged on: M3 reject-first, M4 fork, M2 brute-forceability, E1
diagnostic. The only divergence — the internal one rated M4 SOUND (more
optimistic), the vendors WEAK; the vendors are right (fork is a real
hole). This is valuable: the external blind loop corrected the internal
one, exactly as FF-003 prescribes. `REVIEW ≠ VALIDATION` confirmed here
too.

## Honest caveat

The vendor answers are also LLMs (`LLM_OUTPUT ≠ VERIFIED_COPY`). The
strength is in the CONVERGENCE of 5 independent loops on the same breaks,
not in the authority of one. M1 remains SOUND, M3 is practically BROKEN,
the rest are WEAK with (now) honestly drawn limits.
