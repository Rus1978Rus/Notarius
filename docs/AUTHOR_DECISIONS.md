# NOTARIUS — Author's decision journal (AUTHOR_DECISIONS)

AUTHOR: Ruslan Malyavskiy
Format: a decision is recorded after a methodological audit;
a decision is changed only by a new entry — old ones are never erased.

---

## Session 2026-07-21 (following the NOTARIUS_METHODOLOGICAL_AUDIT_2026-07-21_RU audit)

### AD-1. Status of SEMANTIC_MANIFEST_KEY (§6.1)
**DECISION: DOWNGRADE.** LOCKED → PROPERTY_CANDIDATE.
Rationale: it never went through the pipeline (design-review + threat model);
the recording discipline is the same for all properties.

### AD-2. Classification of SEMANTIC_LAYERED_DEFENSE (§6.2)
**DECISION: SETTLE IT THROUGH PIPELINE DISCIPLINE.**
A property is not reclassified by fiat — it goes through the
pipeline (design-review). The audit's objections (Kerckhoffs; the weak-password
conclusion; independence of barriers 2–4 not demonstrated) are a mandatory
input to design-review. Until it clears the pipeline, status:
PROPERTY_CANDIDATE / NEEDS_CONVEYOR.

### AD-3. Role of SEMANTIC_INVISIBLE_LENGTH_WITNESS (§6.3)
**DECISION: RECLASSIFY AS DIAGNOSTIC.**
New name: DECLARED_CODEPOINT_COUNT.
New status: DIAGNOSTIC_METADATA inside the signed manifest.
Rationale: negative tests (`tests/test_witness.py`) proved bypasses
(rewriting cp_len, equal-length substitution, insert+delete).
The diagnostic value remains: the report names the length shift
and the position of the invisible codepoint.

### AD-4. Unicode normalization form in the specification
**DECISION: DEFER** until the threat model.
The prototype (`notarius/witness.py`) uses NFC before counting and
hashing as an implementation choice; the norm is not written into the
specification. Question open: OPEN_UNTIL_THREAT_MODEL.

### AD-5. Verdict on the niche (§15)
**DECISION: ANALYSIS FIRST, VERDICT AFTER.**
The NICHE_CONFIRMED verdict is neither changed nor confirmed — it is
frozen until the comparison document against prior art is ready
(C2PA / Content Credentials, in-toto / SLSA, Sigstore, RFC 3161,
W3C PROV). The verdict decision follows the analysis.
Status: VERDICT_FROZEN / PRIOR_ART_REVIEW_IN_QUEUE.

### AD-6. Priority (§17)
**DECISION: KEEP MSL/MIP.**
ACTIVE_FRONT = MSL/MIP Sign Cards → Modules → Integrators, unchanged.
Notarius stays PARKED; work in this repository
(audit, prototype, tests) is background. The §17 conflict with the
2026-07-21 session is resolved by reaffirming the priority.

### AD-7. License
**DECISION: DEFER.**
The "COMMERCIAL USE PROHIBITED" declaration stands as a statement of the
author's intent. The legal work (choosing a license) comes before the first
release or pilot. Status: OPEN_UNTIL_FIRST_RELEASE.

### AD-8. Verdict on the niche (§15) — following the prior-art analysis
**DECISION: NICHE_NARROWED.**
Analysis: `docs/PRIOR_ART_REVIEW_2026-07-21_EN.md`.
The AD-5 freeze is lifted. New §15 verdict:
`NICHE_NARROWED / COMPOSITION_PRODUCT / MECHANISM_EXISTS_INTEGRATION_MISSING`.
Precise statement of the niche: provenance that is portable across
organizational boundaries, at the field level of a business document, with a
human-readable break report, accessible to small business outside closed networks.
Rationale: the three "does not exist" claims of the original §15 are refuted in
broad form (C2PA 2.3, in-toto, BEC anti-fraud), but the combination of the four
criteria (field + path + break report + portability) is closed by no one.
The character of the niche is a composition of ready-made primitives
(PROV + in-toto + Sigstore/eIDAS) + our own semantic layer.

### AD-9. Outcome of the applications pipeline (2026-07-22)
**DECISION: RESEARCH TRACK.**
Report: `docs/conveyor_results/FINAL_APPLICATIONS_REPORT_2026-07-22_EN.md`
(40 ideas from 5 model families: 0 STRONG, 2 WEAK, 37 REJECT).
Notarius's value at this stage is methodology and a teaching demo set:
filter-formulas (SIGNED ≠ NATIVE, integrity ≠ provenance),
a working prototype with negative tests, a catalog of 7 structural
defects of provenance ideas. The project proceeds as open
research; the product search is paused. The AD-8 direction
(small business) is not refuted and stays in reserve; the surviving
"citation anchor" cluster stays in reserve with the reviewers' conditions
(publishers/fact-checkers, an external anchor instead of HMAC).

### AD-10. Canonical formula on truth (2026-07-22)
**DECISION: RECORD** in §18 of the working document.
Origin: the author's remark "a lie can be signed and hashed too" after the
negative test test_defect1_not_closed_self_attestation (v2).
Formula:
```
A SIGNED LIE REMAINS A LIE, BUT STOPS BEING ANONYMOUS.
INTEGRITY ≠ AUTHENTICITY ≠ TRUTH
SIGNED ≠ TRUE
TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH
```
Meaning: no cryptographic primitive checks truth; a signature makes
a lie attributable and non-repudiable, and the chain localizes the point where
the lie entered. This sharpens Notarius's positioning: not a truth machine, but
a machine of addressable accountability.

### AD-11. Classification of §6.2 — execution of AD-2 by the pipeline (2026-07-22)
**PIPELINE DECISION (AD-2 mandate): RECLASSIFY.**
SEMANTIC_LAYERED_DEFENSE → SEMANTIC_STRUCTURE_OPACITY,
status PRIVACY_OBSCURITY_PROPERTY / NOT_A_SECURITY_BARRIER.
Design-review: 3 independent reviewers (lenses: cryptography/Kerckhoffs,
threat model, internal consistency) — unanimous verdict 3/3.
Rationale: experiments/exp_6_2_reassembly.py — 1000 trials,
7000 shuffled blocks, without key or schema, 60 lines of regex →
100.0% of semantic types recovered; "meaningless mush"
refuted by executable code; the "independence" of barriers 2–4
refuted (one kind of secret — knowledge of the construction).

Edits applied to §6.2 (full list in the property's text):
- renamed to SEMANTIC_STRUCTURE_OPACITY;
- "four independent barriers" → "one key + one obfuscation layer";
- removed the claim "weak password + structure = mush" (it justified a weak
  key — incompatible with project discipline), with no softening;
- Kerckhoffs adopted as an axiom of the whole document (conflict with §8 removed);
- "assembly order" moved to the integrity property §6.1;
- filter-formulas added (OBFUSCATION ≠ BARRIER, SHUFFLED ≠
  CONFIDENTIAL, TYPE_RECOVERED ≠ ROLE_BOUND).

The candid remainder (not a defense): friction for a casual observer;
role binding under recurring types is UNVERIFIED, a separate
experiment with a pool of documents is needed.

Precedent — AD-3: a property bypassed by an executable test is
reclassified, not defended. The §6 registry after three
revisions: 6.1 — PROPERTY_CANDIDATE, 6.2 — privacy/obscurity,
6.3 — diagnostic. All three downgraded from the original "LOCKED".

### AD-12. Integrating the Foundation Layer into Notarius discipline (2026-07-22)
**DECISION: ADOPT** FO-015, FO-035, FO-018 into project discipline.
Document: `docs/NOTARIUS_DISCIPLINE_2026-07-22_EN.md`.
- D-1 (FO-015 DATA→CLAIM→STATUS→TRUST→ACTION): the chain's skeleton; any
  claim "Notarius verifies X" must name the transition; the prototype lives
  on DATA→CLAIM, anything above is out of scope.
- D-2 (FO-035 CONCRETE_OBJECT_QUESTION_TEST): a property's status does not
  change without a run against a concrete object (test/experiment);
  precedents AD-3, AD-11.
- D-3 (FO-018 RITUAL_COMPLIANCE ≠ CAUSAL_MECHANISM): before the word
  "barrier" — a run through the catalog of 7 defects.
NOT adopted: FO-038…044 (the humanities layer), FO-039/040 (general theory) —
the parent registry itself holds them at DEFERRED / DO_NOT_SPIN_OFF_YET.
Contribution back: adversarial-by-instruction closes the FF-003 gap
of the parent project.
Rationale — the analysis FOUNDATION_LAYER_ANALYSIS_2026-07-22_EN.md.

### AD-13. Parent framework E-Continuity (2026-07-22)
**DECISION: RECORD** all projects as branches of one parent —
E-Continuity / the Framework of governed recoverability.
Umbrella document: `docs/E_CONTINUITY_FRAMING_2026-07-22_EN.md`.
Consequence: Notarius and the imported Foundation Layer (MSL/MIP) are
not unrelated projects in one box but siblings under a shared parent;
keeping them together is architecturally correct (`ECOSYSTEM ≠ MONOLITH` with
signed boundaries). The "mush" question is closed: variant 1 (the Foundation Layer
stays in the repository) gets a rationale instead of "tolerable".
Caveat HEAD ≠ SOURCE: the canonical definition of E-Continuity is
the author's to give; in the document the unifying theme of "governed
recoverability" is marked as an INFERENCE, not a fact; the parent's
specification is expected from the author.

### AD-14. E-Continuity definition obtained; the AD-13 inference checked (2026-07-22)
**DECISION: RECORD** the parent's canonical core.
Source: E_CONTINUITY_STRUCTURED_2026_06_05.zip (release v2.3).
Text core → docs/e_continuity/; analysis →
E_CONTINUITY_ANALYSIS_2026-07-22_EN.md.
Results of checking the AD-13 inference (HEAD ≠ SOURCE):
- "governed recoverability" — CONFIRMED verbatim
  (`governed recoverability through time`); the parent itself declares
  itself the proto-father of the ecosystem (the X_EXISTS ≠ X_RECOVERABLE family);
- FACTUAL CORRECTION to the lineage: Notarius is a GRANDCHILD of E-Continuity via
  MSL/MIP, not a direct child; the diagram in the framing is corrected.
Adopt from above into Notarius discipline (candidates):
proof-testing (Static ≠ Dynamic ≠ Mission — our exp_6_2 was
a dynamic test of §6.2); continuity-chain as a layer over FO-015;
the "degradation from absence of an event" risk (provenance without periodic
re-checking quietly rots).
DEBT recorded: the repository does not yet satisfy two of the parent's
governance rules (DOCUMENT_PROVENANCE_CARD, the full PACKAGE_SET) — not urgent
(AD-9 research track), a candidate for a separate decision.
The parent's boundaries (STATUS_LOCK, "what not to do") are respected, untouched.

### AD-15. Closing the debt: the E-Continuity package standard (2026-07-22)
**DECISION: CLOSED.** The repository is brought in line with the parent's
governance rules (RULES_REGISTER items 4 and 5); the AD-14 debt is paid off.
Artifacts created (docs/_package/):
- PACKAGE_PROVENANCE_CARD.prov — the package's provenance passport;
- DOCUMENT_PROVENANCE_REGISTER.md — a card for every important document
  with ORIGIN (AUTHOR_SOURCE / LLM_GENERATED / EXTERNAL_VENDOR / COPY);
- STATUS_AND_LIMITATIONS_NOTE.txt — status and boundaries;
- MANIFEST.tsv + SHA256SUMS.txt — real SHA-256 (52 files,
  sha256sum -c passes);
- scripts/gen_package.sh — reproducible rebuild.
The candid boundaries are honored verbatim per the parent's rules:
HASH_EXISTS ≠ HASH_VERIFIED (computed in the environment, not verified externally);
LLM_OUTPUT ≠ VERIFIED_COPY (all analysis and code marked as AI output);
COPY ≠ PROVENANCE (foundation_layer and e_continuity marked as copies);
the hash was not invented — only a real computation.
The NOT_DONE remainder (not passed off as done): external hash verification,
human validation — remain open per STATUS.

### AD-16. MSL/MIP genesis recorded (2026-07-22)
**DECISION: RECORD** the birth of the MSL/MIP branch.
Document: `docs/MSL_MIP_GENESIS_PROVENANCE_2026-07-22_EN.md`.
The author's primary testimony: the intuition "will descendants thousands of
years from now understand marks on stone / a clay tablet" (pushing the Viking
formula `DATA PRESERVED ≠ READABLE` to the limit of millennia) → the bracket
mechanism `(word)` as the first step of decipherment. The author's fresh layer:
a nesting hierarchy — `( )` closes a word, `[ ]` a sentence
(`[(word)(word)]` = a sentence of words), a self-describing grammar of
containers. LLM framing (marked): the precedent of Champollion's cartouche
(the frame as the historical entry point into deciphering hieroglyphs); the
candid boundaries (the bracket gives "a mark exists + boundaries + structure",
not meaning; the delimiter must be visually distinct from the content). Link
downward: the bracket is the ancestor of Notarius's `chunk + boundary` and
`block_with_witness`. Closes `HEAD ≠ SOURCE` for the branch's birth. Not an
MSL/MIP specification.

### AD-17. A pattern running through three generations (2026-07-22)
**DECISION: RECORD** as a candidate pattern.
Written into E_CONTINUITY_FRAMING. The whole vertical carries one idea:
a meaningful unit is saved by its boundary. E-Continuity — a boundary against
loss of context over time; MSL/MIP — against loss of language; Notarius —
against loss of trust. The mechanism's hereditary line: the bracket `(word)`
→ block_with_witness → length-witness; in all three a boundary break is the
first detectable signal (one canary, three substrates).
Candidate formula: `MEANINGFUL_UNIT_SURVIVES_THROUGH_ITS_BOUNDARY`,
`BOUNDARY_BREAK = FIRST_DETECTABLE_SIGNAL`.
Candid status: RECURRING_PATTERN_CANDIDATE / WORTH_STUDYING /
NOT_UNIVERSAL_LAW (per FO-040: RECURRENCE ≠ VALIDITY, DO_NOT_SPIN_OFF_YET).

### AD-18. Algorithms for signing/identification/confirmation (2026-07-22)
**DECISION: DIRECTION IN PROGRESS.** At the author's request (signing/
identification of segments or the whole across different substrates + confirmation,
+ unconventional). Catalog: ALGORITHMS_SIGNING_IDENTIFICATION_2026-07-22.
Executable demos built (FO-035):
- algorithms/merkle_segments.py — signing the whole + a proof of any
  segment without the rest;
- algorithms/human_fingerprint.py — a word-fingerprint (human verification
  without software across a substrate boundary), mod-97 self-check, redundant ID
  (survives loss of 2 of 3 copies).
- tests/test_algorithms.py — 14 tests green.
Unconventional finding: the diagonal "stone × human without software" is a zone
where cryptography does not work; it is closed by the word-fingerprint, the
self-checking ID, and the self-describing MSL/MIP bracket. Prior art
(Merkle/MerkleSpeech, PGP words, visual hash, PUF, Reed-Solomon, DNA stego)
is annotated by status. Candid boundaries: identification ≠ proof of truth;
the human forms are truncated (not full strength); the physics/exotica are not
implemented. What to bring into the core is open for AUTHOR_DECISION.

### AD-19. Semantic tracing built (2026-07-22)
**DECISION: CORE IMPLEMENTED.** At the author's request, we built what the
document described but never built (§16/§17/§9).
Code: notarius/trace.py; tests: tests/test_trace.py (9, green).
Mechanism: a chain of signed events of an element (CREATED→TRANSFORMED→
TRANSFERRED→REVIEWED), each = value_hash + the actor's Ed25519 signature +
prev_hash; verification produces the §16 report (TRACE_BREAK_DETECTED, break_at_step,
last_signer, state per §9). It brings the session together: Ed25519 + hash chain
+ state model + human-readable report (the AD-8 niche).
Live demo: substituting 1000000→9000000 after approval → MODIFIED,
break_at_step, last_signer. TRACE_LOCATES_THE_LIE (AD-10) in working form.
Candid boundaries: self-attestation (#1) is NOT closed (the actor signs their
own lie — the test shows it; the trace localizes, it does not refute); time is
self-declared (#3); silent omission is not visible (the Viking lesson).
Open: external timestamp, Merkle over the document, binding the key to an
identity, periodic re-checking of the trace (proof-testing).

### AD-20. Blind prompt for method review (2026-07-22)
**DECISION: PREPARED.** At the author's request — run the AD-18/19 methods
through an external vendor pipeline, adversarially and blind.
Document: docs/VENDOR_PROMPT_METHODS_REVIEW_EN.md.
Blindness: no project/author name, no indication of the preferred
method. Adversarial-by-instruction (closes FF-003): the reviewer is required to
BREAK it, to look for a failure scenario and hidden overclaim, not to praise.
Methods M1–M5 are presented neutrally (Merkle segments, word-fingerprint,
manual control + duplicates, event chain, boundary detector), each with
mechanism/property/boundary. The response format is for synthesis through the
same reviewers. Vendor answers → docs/vendor_answers/methods_*.

### AD-21. Internal method review + fixing a real bug (2026-07-22)
**DECISION: FIXED PER THE RESULT.** An internal blind adversarial
pipeline (6 reviewers) on methods M1–M5. Result:
methods_internal_review_2026-07-22_EN.md.
KEY POINT: all 6 reviewers independently found CVE-2012-2459 in the M1 code —
duplicating an odd node gave root([A,B,C])==root([A,B,C,C]).
Reproduced, FIXED: algorithms/merkle_segments.py rewritten to
RFC 6962 (no duplication); signed_root() added (a root+size pair
against the completeness attack); a regression test + tests for odd sets.
All 4 suites green (17 algorithm tests).
Verdicts: M1 SOUND(4.5), M2 DISPUTED(3.5), M3 WEAK(2.67), M4 SOUND(3.67,
honesty 4.33 — the best self-criticism), M5 WEAK(2.17). Findings on M2/M3/M4/E2
— queued for rework (not silently). E1 reinforces AD-3 (diagnostics),
E2 is an entry point for MSL/MIP (visual delimiter distinction + escaping).
Lesson: REVIEW ≠ VALIDATION in both directions — the review found what the green
tests were hiding. A baseline for synthesis with external vendors (AD-20).

### AD-22. Synthesis of the external method pipeline + fixes (2026-07-22)
**DECISION: SYNTHESIZED AND FIXED.** 5 independent sources (internal
+ Kimi, Grok, GPT, Gemini; Copilot excluded as a duplicate of Gemini — FF-003).
Synthesis: methods_crossvendor_synthesis_2026-07-22_EN.md.
Verdicts: M1 SOUND (unanimous), M2 WEAK, M3 WEAK→BROKEN (reject-first
unanimous), M4 WEAK, M5 E1 WEAK / E2 WEAK-DISPUTED.
Fixed in code (findings → fixes, as in AD-21):
- M3: a non-positional sum → positional_check (catches transpositions AB≠BA);
  removed the overclaim "catches tampering" (this is random corruption, not authentication);
- M4: fork+truncation added to the candid boundaries; the expected_head
  parameter detects truncation when the head is known; last_signer = the key's
  owner (SIGNING_KEY ≠ REAL_ACTOR);
- M2: default 6→12 words (36→72 bits); a boundary on attack cost + BIP39;
- M1: the leaf commits index+length (position binding), verify_segment with index.
All 4 suites green. Out of scope of the local code (candidates, not silently):
an external anchor + transparency log (M4 fork), Reed-Solomon/PUF, the
re-signing ritual (Kimi's meta-conclusion: "they outlive the carrier, not the
algorithm"); E2 — escaping + legend (an entry into MSL/MIP genesis).
Key point: the external blind loop corrected the internal one (M4 SOUND→WEAK) —
FF-003 worked, REVIEW ≠ VALIDATION confirmed.

### AD-23. Map of ready-made solutions: adopt-don't-invent (2026-07-22)
**DECISION: DIRECTION RECORDED.** In response to the author's question "why
reinvent the wheel". Document: EXTERNAL_SOLUTIONS_MAP_2026-07-22_EN.md.
Checked against sources: almost all of AD-22's open tasks are solved
standards in adjacent fields.
- "A signature lives as long as its algorithm" → RFC 4998 Evidence Record Syntax
  (re-timestamp before weakening) + *AdES-LTA + crypto-agility + hash-based
  signatures (XMSS/SPHINCS+). The re-signing ritual has been standardized since 2007.
- The M4 fork → witness cosigning (Certificate Transparency, Sigsum);
  truncation → RFC 6962 consistency proof; time → RFC 3161/OpenTimestamps;
  corruption → Reed-Solomon; longevity → OAIS (E-Continuity stands on it).
- Self-attestation (#1) is NOT solved cryptographically by ANYONE — a universal
  limit; adjacent fields contain it through independence (M-of-N,
  separation of duties), they do not "solve" it.
Conclusion: we take the crypto plumbing ready-made; the project's value is not new
crypto but the SEMANTIC layer + human-readable assembly (this confirms
the AD-8 niche). AD-22's open items are reframed from "invent" to
"integrate a standard".

### AD-24. A signed lie = evidence against the signer (2026-07-22)
**DECISION: RECORD** in §18 of the canonical phrases.
The author's insight: "an author, by writing down their own lie, creates
material evidence against themselves, for the court, with their own hands." It
flips defect #1 (self-attestation) from a WEAKNESS into a STRENGTH: the signature
does not stop lying, but it makes the lie non-repudiable evidence (in law, an
admission against one's own interest). It deepens AD-10 (not just "not anonymous"
but "incriminating and self-produced").
Formula:
```
A SIGNATURE DOES NOT STOP LYING — IT TURNS THE LIE INTO EVIDENCE AGAINST THE SIGNER.
SIGNED_LIE = SELF_PRODUCED_EVIDENCE
  given: KEY_BOUND_TO_IDENTITY ∧ RECORD_BEYOND_LIAR_CONTROL
       ∧ FORCED_TO_SIGN_IN_SYSTEM
```
Candid conditions (not an overclaim): (1) key↔identity, otherwise the evidence is
against the key, not the person (SIGNING_KEY ≠ REAL_ACTOR, GPT); (2) the record
beyond the liar's control — the external anchor of AD-23, otherwise the admission
is withdrawn; (3) the liar is forced to sign in the system, otherwise they keep
the lie outside the trace.
Key point: self-attestation #1 + binding to an identity + the AD-23 anchor are not
three separate holes but ONE condition for turning a signature into evidence. Link:
§11 (court), AD-10, AD-23.

### AD-25. UNSTEALABLE = UNCOPYABLE + a search pipeline (2026-07-22)
**DECISION: RECORD the formula + PIPELINE LAUNCHED.**
The author's insight: "part of the key must be such that it methodologically
cannot be stolen." Refined: data is always copyable → the "unstealable"
part = NOT data (physics/biology/PUF) OR split (Shamir/M-of-N).
Formula in §18: `UNSTEALABLE = UNCOPYABLE`; the goal is to turn DIGITAL_THEFT
(silent) into PHYSICAL_THEFT (visible) — the same principle as FO-7
MANIPULATION_LEAVES_SUBSTRATE_TRACE. A single point of trust is fatal
(self-attestation AD-24 + fork AD-22 + key theft) — there is one cure:
shatter and distribute.
A blind pipeline launched (wf_850eefa8) for unconventional/wild ideas for
part of the key, inspired by "Perimeter" / "Dead Hand" (capturing the point does
not give control). The central test criterion: does the idea turn silent
digital theft into visible physical theft. Blind prompt for external vendors:
docs/VENDOR_PROMPT_UNCOPYABLE_KEY_EN.md.

### AD-26. Synthesis of "an uncopyable part of the key" — 7 sources (2026-07-23)
**DECISION: SYNTHESIZED.** Document: uncopyable_key_synthesis_2026-07-23_EN.md.
7 independent sources (internal + Copilot, DeepSeek, Gemini, GPT,
Qwen, Kimi); the GPT×2 and Qwen=DeepSeek duplicates excluded (FF-003).
FOUR axes emerged: (1) a distributed M-of-N threshold — the most frequent
(3 favorites); (2) destruction-on-read; (3) a biological dead hand;
(4) NEW — the "mortal copy" (Kimi): not protecting bits, but a copy that dies
without the owner's heartbeat (link to Viking + AD-24).
Converging filter (≥5 sources): "read-once = copyable
if reading does not destroy" — rejects half of the "physical" ideas.
The tension pole: human-in-the-loop (robust to theft, coercible) vs
removing the human (usable, coercion moves to the device).
Mature synthesis (Kimi+GPT): a composite system — threshold (never assemble the
key) + mortal heartbeat + secure enclave + external timestamp. Pragmatic
minimum: a non-extractable key in the phone's enclave + a server heartbeat + logging.
THE AUTHOR'S ORIGINAL INSTINCT "Perimeter" is CONFIRMED by 7 sources:
distribution is the practical answer; the exotica are unreachable poles.
Recommendation (candidate): a threshold signature + enclave + mortal heartbeat +
OpenTimestamps — all ready-made standards (AD-23). Link: FO-7, AD-24, AD-25.

### AD-27. Build plan for the key custody boundary (2026-07-23)
**DECISION: PLAN + CORE DEMO.** At the author's request a concrete
plan was laid out. Document: KEY_CUSTODY_BUILD_PLAN_2026-07-23_EN.md.
A boundary of 4 layers (along the AD-26 axes): an M-of-N threshold + mortal
heartbeat + hardware anchor (secure enclave/passkey) + external timestamp. All
from ready-made standards (FROST/threshold-Ed25519, proactive SS, FIDO2/WebAuthn,
OpenTimestamps/RFC 3161, RFC 4998) — no in-house crypto is written (AD-23).
6 stages: threat-model → threshold → heartbeat → hardware → timestamp → ceremony.
The core demo is executable: notarius/custody.py + tests/test_custody.py (9,
green) — proven in code: M-of-N, M-1 useless, old shares expire,
no heartbeat → the key and its copies are dead. Candid boundaries: the seed is
assembled in memory (FROST is not), refresh is dealer-based (production — proactive SS),
enclave/timestamp are integration points, coercion is not eliminated.
Pragmatic minimum (Kimi): an enclave phone + a server share with a heartbeat
+ 2-of-2 + OpenTimestamps. The join with trace.py: the boundary signs the trace's
events → closing the three AD-24 conditions (key↔identity, record beyond control,
non-copyability).

### AD-28. Rubber-hose limit — coercion is out of crypto's scope (2026-07-23)
**DECISION: RECORD** as a candid boundary in §18.
The author's insight: "the most reliable cracker is thermorectal cryptanalysis."
True and important: rubber-hose (coercion under threat, xkcd 538) is out of
the scope of ANY cryptography. All the AD-25/26/27 techniques (threshold, heartbeat,
enclave) protect against SILENT theft; coercion is LOUD theft.
Formula: `CRYPTO_PROTECTS_AGAINST_SILENT_THEFT ≠ PROTECTS_AGAINST_COERCION`.
It is not eliminated, only contained: distribution across jurisdictions
(you need N teams in N countries at once — visible), a negative quorum (under
torture you give an alarm, not the key), a duress code (fake opening + alarm).
No answer saves the person — it only denies the thief the key. A final
confirmation of AD-24: crypto does not protect truth or the person — it makes the
silent loud, and beyond that lies law/police/society. GUARD: do not sell the AD-27
boundary as "unbreakable".

### AD-29. A mortal carrier-validator (§8 PROVENANCE_CARRIER) (2026-07-23)
**DECISION: RECORD + DEMO.** The author's insight: "my QR code as
a validator lives only a short while." It refines §8: the carrier must be MORTAL.
A short life (time expiry) + single-use (burning on first presentation) = a copy
is useless. The carrier carries not the key but a short-lived proof, signed by
the key (the key in the enclave / custody AD-27). The human-readable face of the
"mortal copy" of AD-26 (clear to a cashier). Demo: notarius/carrier.py +
tests/test_carrier.py (8, green) — a copy → EXPIRED or ALREADY_USED. The pattern
is widespread (TOTP, rotating payment QR codes) — AD-23 adopt-don't-invent.
Boundary: within the window the carrier is copyable; the protection is the window
+ single-use + trusted time, not "cannot be copied". §8 updated (STATUS:
MORTAL_CARRIER, a prototype exists).

### AD-30. Integration dossier of 5 standards (2026-07-23)
**DECISION: INTEGRATION PLAN READY.** At the author's request "take on FROST,
enclave, OpenTimestamps, witness-cosigning, Reed-Solomon" — without new
demos. Document: INTEGRATION_DOSSIER_2026-07-23_EN.md. For each:
the library (checked against 2026 sources), the join point in our code,
what it closes, the candid boundary, the effort.
Key findings: FROST is finalized as RFC 9591, and the FROST-ED25519
ciphersuite emits an ORDINARY Ed25519 signature → our verification side
(envelope_v2/trace) does NOT change, the threshold is only on signing — a clean
integration. OpenTimestamps (opentimestamps-client) + RFC 3161
(rfc3161-client) → the anchor field in trace (AD-19). Witness cosigning
(C2SP tlog-witness) → closes the M4 fork via expected_head (AD-22).
Reed-Solomon (reedsolo) → carrier corruption (carrier, redundant_id).
FIDO2/passkey → a share in the enclave.
Priority for the pilot: OTS+Reed-Solomon (low effort, cheap) →
FIDO2 → FROST → witness. Boundaries: FROST/witness — code in another language /
infra, not pip; enclave — hardware; nothing closes coercion (AD-28).

### AD-31. First two standards wired in: Reed-Solomon + OpenTimestamps (2026-07-23)
**DECISION: INTEGRATED (partially, candidly).** At the author's request
"OpenTimestamps + Reed-Solomon, how do we wire these in?" — the two
LOW-effort items from the AD-30 dossier are implemented. Module:
notarius/integrations.py (not stdlib; `pip install reedsolo opentimestamps`).
Tests: tests/test_integrations.py (6, green).
— **Reed-Solomon (reedsolo): WORKS, verified offline.** rs_protect/
  rs_recover/rs_recoverable. parity=16 → corrects up to 8 corrupted bytes.
  Both outcomes proven by tests: 6 corrupted bytes are recovered, 10 corrupted
  bytes (over budget) are candidly NOT recovered. The join point is
  carrier.py (the durable carrier) and redundant_id (human_fingerprint):
  real correction instead of plain duplicates.
— **OpenTimestamps (opentimestamps): the adapter is real, but NOT verified
  end-to-end.** ots_new/ots_digest_of/ots_stamp/ots_serialize — real
  code against the lib's API, not a stub. BOUNDARY (HONEST_LIMIT): ots_stamp()
  requires the network (a calendar server) — in this environment the proxy gives
  403; verify requires a Bitcoin node. The offline part (creating the object,
  binding to SHA-256) is tested; anchoring and verification are NOT. We do not
  pass off the unverified as working: the OTS tests cover only what actually ran.
GUARD: integration ≠ validation. Reed-Solomon is a genuinely working recovery
layer; OpenTimestamps is a ready-to-enable adapter awaiting an environment with
network + node. Both are assembly of the ready-made (AD-23 adopt-don't-invent),
no new crypto. README updated (section "Integrations of ready-made standards").

### AD-32. The phone chip's role: a "lock/safe", the Ed25519 signature in the app (2026-07-23)
**DECISION: RECORD a single path for iPhone and Android.** Analysis of
the author's question "FIDO2/enclave on a phone — will it be somehow different
on an iPhone?".
FACTS (checked against 2026 platform docs):
- The iPhone Secure Enclave computes ONLY on P-256; there is no Ed25519 in
  hardware (software only) — Apple Developer docs.
- Android 13+ (KeyMint v2) added Curve25519 to the hardware keystore →
  Ed25519 in hardware is possible, but device-dependent (TEE/StrongBox).
DECISION: the phone plays NOT the role of signer but two roles —
(A) **a presence gate** (passkey/WebAuthn: "this phone + biometrics") and
(B) **a safe for the share** (the chip locks the Ed25519 share; unlocked only on
the device after biometrics). For (A)/(B) the iPhone is fully suitable: P-256
key-agreement (`SecureEnclave.P256.KeyAgreement`) locks the share, and the
Ed25519 signature itself is computed in the app. This means **the verification
side does not change, the chip's curve does not matter** — a single codebase for
iPhone and Android, with no platform lock-in. Role (C) "the chip = a real
FROST-Ed25519 share" is available only on Android 13+ and belongs to the
"serious tier" (requires FROST, AD-30) — we do NOT build it now.
GUARD (important, against self-deception): the P-256/Ed25519 difference is
COMPATIBILITY, NOT a security wall. "Security through incompatibility" is
forbidden: incompatibility is fixed with an adapter, a wall is not. The phone's
real walls are: (1) a non-extractable key in the chip, (2) biometrics on
every use, (3) an M-of-N threshold (AD-27), (4) a mortal carrier + heartbeat
(AD-29). The curve is not on this list. Coercion is not closed (AD-28). ENVIRONMENT
BOUNDARY: the real enclave cannot be touched here (hardware is not emulated) — in
a build this will be a labeled SIMULATION of the contract, and the swap to the
chip is mechanical.

### AD-33. Vakhter audit + porting the detection layer (2026-07-23)
**DECISION: RECORD THE AUDIT + TAKEN INTO CODE.** At the author's request
"read the kindred project rus1978rus/vakhter line by line, maybe there's
something to take." Read line by line by 4 parallel readers (@ 3763b71).
Document: VAKHTER_AUDIT_2026-07-23_EN.md.
KEY DISCOVERY: Vakhter and our NOTARIUS are two branches of one seed
(it contains `docs/NOTARIUS.md` from 2026-07-20 = our source, and a working
`notarius_ledger.py`). Division of labor: Vakhter has a mature DETECTION
layer (zero-width chars/homoglyph/bidi/canonicalization), we have mature CRYPTO
(Ed25519/custody/carrier/OTS/RS). We took their detection, kept our crypto.
Both repositories are by the same author — no licensing barrier.
TAKEN INTO CODE (verbatim port, our own tests):
- `notarius/canon.py` ← canonicalize.py: a pre-pass against encoding
  evasion (percent/entity/`\u\x`/overlong-UTF-8/numeric IPs). Tests
  test_canon.py (7). BOUNDARY: NOT NFC, does NOT close AD-4 — orthogonal.
- `notarius/detect.py` ← invisible_cards/canonical_view/fail_closed +
  Finding: ALARM on smuggling (word-split, bidi imbalance CVE-2021-42574,
  tag-smuggle, VS-carrier, parser-desync), OK on legitimate joining, WATCH on
  the unknown, fail-closed. Tests test_detect.py (13, both outcomes).
- `scanner.py::scan_hardened()` — a facade: the old scan() as it was + on top
  canonicalization + engine.
TAKEN AS DISCIPLINE (for the future, not code): mutation-adequacy for our
verify (candidate), the r>g admission filter, the honest-eval template. Vakhter's
provenance.py confirmed our cp_len witness (AD-3) — the design is right.
NOT TAKEN: 258 sign cards (a draft reference, lives on its own; we took the logic
+ seed vectors); HMAC crypto (our Ed25519 is stronger); product/range_*
demos (they depend on the missing msl_mip_runtime).
CANDID about the source: the MSL core is not in the repository → its coverage
figures are not verifiable; "100%" is on draft simulators / small self-authored
batteries; the Foundation-Layer claims are grandiose/unfalsifiable. A real bug was
found in their notarius_ledger (an INVISIBLE_INSERT label on any change of length) —
our trace.py does not do that. GUARD: we take ideas and primitives under OUR OWN
tests; we do not accept others' metrics as validated. The port is advisory,
not a certified filter; there is no human validation of the detection; AD-4
is open.

### AD-34. scan_hardened → trace/carrier (the content axis) + mutation-adequacy (2026-07-23)
**DECISION: WIRED IN + AD-33 CANDIDATE CLOSED.** At the author's request
"wire scan_hardened into trace.py/carrier.py, add a mutation test to
verify".
WIRING (the CONTENT axis, separate from the crypto state):
- `trace.verify_trace`: given a current_value, runs scan_hardened,
  puts report["content_scan"]={risk,signature} and adds a reason when
  risk≠OK. It does NOT touch the crypto state/status.
- `carrier.CarrierValidator.validate`: on the VALID path it recursively screens
  the payload (_screen_payload), puts result["content_scan"] + a note on risk.
WHY THIS MATTERS: NFC (in _value_hash) does NOT remove zero-width → the value
`admin<ZWSP>istrator` gives a stable hash, a valid signature, an INTACT chain —
but it is NOT "administrator". A direct implementation of the §4 principle
CONTAINER_INTACT ≠ ELEMENT_CLEAN: the chain is intact, but the element is poisoned.
Proven by tests (test_mutation.py::TestContentScreeningAxis): trace
INTACT + content_scan ALARM at the same time; carrier VALID + payload ALARM.
MUTATION-ADEQUACY (Vakhter's discipline gate_selftest — "a gate that
cannot be failed is not a gate"): test_mutation.py mutates EVERY signed
field (2 events × 10 fields = 20 mutations for trace + 5 for carrier) → verify
MUST catch it; + a negative control (clean passes). It proves that the
verifiers can genuinely reject, and are not "false green". All caught.
BOUNDARY: screening is advisory (Notarius does not block); it catches hidden
content manipulation, not coercion (AD-28) or self-attestation (an actor
can sign the poisoned content deliberately — the trace LOCALIZES it, AD-10).
111 tests green, package rebuilt.

### AD-35. Generalizing to the whole monitored class — no silent passes (2026-07-23)
**DECISION: SYSTEMIC FIX (variant C), not "finish off the cards".** The author
loaded the parent Foundation Layer registry (v11.5 + the 2026-07-05 package) and
ran a measurement sweep. The finding (a reframing of the AD-33 hole):
the problem is NOT in 4 characters but SYSTEMIC — characters without an explicit
"card" gave verdict=OK (a silent pass), even though a zero-width char in a
token/host is never legitimate. The pass/escalate asymmetry is purely a matter of
who happens to have a card.
MEASUREMENT (our detect.py, scripts/sweep_invisible_class.py, 404 characters):
BEFORE — in a host, 14 silent OKs (the _CF_NOT_DI family: U+0600-0605 et al.), between
spaces 36 silent OKs. AFTER — 0 and 0.
FIX in notarius/detect.py:
- `_monitored(ch)` = Cf ∪ default-ignorable ∪ VS (the whole class, not 6 characters);
- `_any_monitored_wordsplit` — a generalization of zw_wordsplit: ANY monitored
  character breaking a token between alphanumerics → ALARM (host_break);
- the present-set invisible_cards is extended to `_monitored` → any such
  character is at least WATCH (does not stay silent) even outside a token.
This closes 135-of-138 at once. The specific signatures (zw_wordsplit,
bidi_imbalance, tag_smuggle, vs_carrier, parser_desync) are kept —
the generalized check runs last. Tests: test_detect.py +5
(TestMonitoredClassNoSilentPass: sweep 0 silent in both positions + a list of
SIGN_EXAMINER 12 characters + math operators 2061-2064 + a homoglyph out-of-scope).
CANDID BOUNDARIES (from the author's measurement, preserved):
- Within the class of 138 there were no truly silent passes before either — all were
  witnessed; the hole was in verdict=pass, and anyone looking only at the action would
  miss it. Now it is at least WATCH/queue.
- HOMOGLYPHS (visible look-alikes: Cyrillic o, Greek omicron, NFKC
  ligatures) are a DIFFERENT family, a truly silent pass, NOT covered by this
  fix (Vakhter confusable_cards is not ported) → a separate front,
  recorded by a test as out-of-scope, not passed off as coverage.
- Percent-encoded (pay%E2%80%8Bpal.com): our canon.py unfolds and catches it
  (we are more aggressive than a host that passes it at the raw level) — a divergence
  of philosophies, left as is.
- Extending the class = more advisory-WATCH on legitimate multilingual text
  (Arabic number signs and the like); a deliberate choice: "the monitored does not
  stay silent" matters more than silence. Notarius is advisory — it does not block.
116 tests green, package rebuilt.

### AD-36. Witness-cosigning: the trace fork/truncation hole (M4) closed (2026-07-23)
**DECISION: IMPLEMENTED.** The only candidly-uncovered trace defect
(AD-22, M4) is closed: fork/equivocation and truncation. Module notarius/cosign.py.
MECHANISM (C2SP tlog-witness / RFC 6962 consistency): the trace's head
(checkpoint = size + head, head = the digest of the last event =
a commitment to the entire prefix via prev_hash) is co-signed by external
witnesses. Witness.cosign checks: the log's signature, correspondence to the trace,
the chain's internal consistency, and consistency with what was seen before
(same height + a different head → FORK → refusal; extension → the old_size prefix
must hash to old_head, otherwise it was rewritten → refusal; smaller →
truncation → refusal). verify_witnessed_trace: a quorum of M-of-N co-signatures gives
a TRUSTED expected_head → verify_trace catches truncation (head ≠
witnessed) and a fork (a branch without quorum). A witness stores O(1) per log.
Tests test_cosign.py (11): a legitimate extension is co-signed; a fork is
refused at co-signing AND caught by the check against the witnessed
head; truncation is caught; a rewritten prefix is refused; quorum-threshold;
forgery / untrusted co-signature / a broken log signature are rejected.
CANDID BOUNDARIES: it catches ONLY if the verifier requires a quorum; collusion of
M witnesses will deceive it (the threshold raises the bar); a witness sees the head,
NOT the content/truth (SIGNED ≠ NATIVE) — it proves "everyone sees ONE log",
not "the log is truthful"; it does not close coercion (AD-28) or self-attestation
(AD-24) — but it removes equivocation: you cannot show a DIFFERENT lie to different
parties, the trace is one and accountable (this reinforces AD-10). The demo sends the
whole trace; in production — an O(log n) consistency proof (RFC 6962). adopt-don't-invent (AD-23).

### AD-37. Mutation-adequacy for envelope_v2 (2026-07-23)
**DECISION: ADDED.** At the author's request — extend the mutation-adequacy
discipline (AD-34, "a gate that cannot be failed") to the third
verifier, verify_envelope_v2. tests/test_mutation.py +3
(TestEnvelopeMutationAdequacy): every signed field is mutated —
top-level (v/data/sig/signer_pub) and manifest (origin/created_at/
cp_len/sha256/anchor) → verify must return NOT VERIFIED; + a negative
control. All caught (the signature covers the whole body {v,data,manifest}).
Now all three verifiers (trace/carrier/envelope) demonstrably can
reject. 130 tests green, package rebuilt.

### AD-38. FROST-ED25519: a real threshold, the verify side unchanged (2026-07-23)
**DECISION: REFERENCE IMPLEMENTATION (candidly labeled).** The heaviest item
of the AD-30 dossier ("the serious tier"). Checked in the environment: there is NO
pip-FROST (adopt impossible), BUT libsodium via PyNaCl provides all the ed25519
arithmetic (crypto_core_ed25519_add/scalar_add/mul/sub/invert/reduce, scalarmult).
So a REFERENCE FROST-ED25519 (RFC 9591) was built on top of libsodium's proven
primitives — we do NOT roll our own curve (AD-23), we compose the protocol.
Module notarius/frost.py: keygen_dealer (Shamir over the scalar field),
two-round sign (commitments D/E, binding factor ρ, group R,
challenge c=SHA512(R‖A‖M) mod L per RFC 8032, partial z_i, aggregation z=Σz_i).
KEY POINT PROVEN IN CODE: the secret s is NOT reassembled during signing (each
z_i from its own share, the coordinator sums them) — this removes the custody.py
boundary "the seed is assembled in memory". And the AD-30 claim: the output is an
ORDINARY Ed25519 signature, accepted by an UNMODIFIED verify_envelope_v2 and a PyNaCl VerifyKey.
Tests test_frost.py (8): 2-of-3 (all pairs), 3-of-3, 5-of-7 verify;
1 share < threshold and forgery / a foreign message do not pass; a FROST envelope
is accepted by our verify, data tampering is caught.
CANDID BOUNDARIES (loudly, in the module): REFERENCE, NOT production, NOT audited,
NOT guaranteed constant-time at the level of the Python composition (libsodium's
primitives — yes); production = Zcash Rust FROST via FFI or a signing service.
Keygen is a trusted DEALER (during distribution it briefly holds s, as in Shamir;
real FROST is DKG without a dealer); the improvement over custody.py is precisely
in the SIGNING (s is not reassembled). The nonce is single-use (reuse reveals the
share) — freshly random, but single-use storage is not enforced. It does not
close coercion (AD-28) / self-attestation (AD-24). custody.py is kept
as a demo of threshold+heartbeat; frost.py is the threshold itself without assembly. 138 tests green.

### AD-39. Canonizing semantic tracing — a return to the center (2026-07-23)
**DECISION: CANON RECORDED.** Per the author's correction: "semantic
tracing is the main thing; the key is a byproduct; go back to it, search the
origins, canonize it." An acknowledged drift of focus in recent sessions toward the
PLUMBING (threshold/FROST/witnesses/bitcoin) — that is plumbing, not the product.
A single authoritative document docs/SEMANTIC_TRACE_CANON_2026-07-23_EN.md was
assembled from the product's origins (NOTARIUS_FULL_SESSION.md 2026-07-20 §1–5, §9–10,
§16–18 + AD-10/19/22/34/36): the canonical definition (ORIGIN+TRACE+
CURRENT_STATE; three questions — from where / through what / native-or-inserted), the layer
(INTEGRITY ≠ PROVENANCE), the vertical (MSL→Notarius→SSP), the canonical
law-invariants (SIGNED≠NATIVE, TRACE_LOCATES_THE_LIE≠TRACE_PROVES_TRUTH
et al.), the object-element (ORIGIN/TRACE/TIME/STATE), the state model,
the implementation (a chain of signed events), levels L1–L3, what it does NOT do,
the candid boundaries, the canonical phrases of §18 verbatim.
THE HIERARCHY IS FIXED: semantic tracing = the PRODUCT; signature/threshold/
witnesses/recovery = plumbing in the service of the trace, not an end in itself.
The key is a byproduct of the requirement "a step of history cannot be forged".
No code changed (canonization is a documentation matter); 138 tests green.

### AD-40. The minimal unforgeable segment · substrate independence (2026-07-23)
**DECISION: LAW RECORDED IN THE CANON (§12).** In the author's train of thought:
video is easy to forge, it is made of parts — is there a minimal unforgeable
segment, and does this apply to other kinds of information.
A GENERAL LAW STATED: `THE MINIMAL UNFORGEABLE SEGMENT = CHUNK +
BOUNDARY + BINDING AT BIRTH`. Key: unforgeability lives NOT in
the content (pixels/bytes are repainted — there is no unforgeable PIECE),
but in the BINDING (hash + chaining + source signature + time anchor). The binding does
not depend on the kind of information → substrate independence (FO-013; Vakhter:
what survives transformation). A development of §18 "chunk+boundary" and Video Trace
(§17). Table of forms: video/audio/text/finance/sensors/software/medical/law — one
model, particular forms. In code it is already so: canonical JSON + NFC = a commit
at the canonical level (not per byte). The ready-made standard for video/photo is
C2PA/Content Credentials (AD-23 adopt). THE BOUNDARIES ARE UNIVERSAL: SIGNED≠NATIVE
/ the analog hole (an honestly-signed fake) — everywhere; there is no retroactive binding;
theft of the source's key; coercion (AD-28); legal transformations →
the canonical level. Video Trace went from "parked" to a recorded
special case of the general law. No code changed; 138 tests green.

### AD-41. Adversarial experiment: the signed passed through external environments (2026-07-23)
**DECISION: A REPRODUCIBLE HARNESS + FINDINGS SAVED.** At the author's request:
sign → run through an aggressive external environment → look at what
broke → draw conclusions. scripts/adversarial_env.py: 5 REAL external environments
(iconv/sed/gzip processes, NFKC, a JSON gateway) over a signed envelope.
MEASURED: 3 caught (iconv losses, NFKC normalization, sed 1000→9000),
2 passed (a JSON reassembly gateway, gzip — pure reformatting).
FINDINGS:
1. Everything that touched the CONTENT was caught without misses — the thief (9000),
   the encoding loss, and "helpful" NFKC.
2. What touched only the FORM passed (the JSON gateway, gzip): a real test
   confirmed AD-40 — the commit is at the CANONICAL level (JSON+NFC), not per byte.
3. KEY POINT: verify localizes "where it broke", but does NOT judge "why" —
   iconv/NFKC/the thief gave ONE verdict SIGNATURE_INVALID. This is verbatim
   TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH; intent is the human layer.
4. Both axes are needed (the §6.3 origin confirmed): scan_hardened returned OK on
   everything broken — it catches hidden insertion of invisible chars, not value
   substitution; "9000 instead of 1000" was caught ONLY by the signature.
5. The fragility is candid: an exact canonical commit catches even innocent
   re-encoding — both a plus (you learn of the loss) and a cost (legitimate pipelines
   trip it); the answer is the right canonical level for the domain.
No core code changed; 138 tests green. The harness is extensible (base64, HTML-
escape, gateway insertion of BOM/ZWSP, varchar truncation, homoglyph substitution).

### AD-42. A break diagnostician + an inserting environment + a unified report (2026-07-23)
**DECISION: BUILT — growing the CENTER.** Following AD-41 (verify localizes
"where", does not describe "what"): the semantic assembly is strengthened.
① notarius/diagnose.py — diagnose_change(original, current) CLASSIFIES the
change as EVIDENCE, not a verdict on intent (TRACE_LOCATES_THE_LIE):
VALUE_SUBSTITUTION (numbers, 1000→9000, high) · INVISIBLE_INSERTION (invisible chars,
high) · NORMALIZATION_EQUIVALENT (NFKC-equal, low) · CHAR_LOSS (loss on
re-encoding, medium) · CONTENT_CHANGED · IDENTICAL. Each with a review level.
③ assemble() — a unified human-readable report: the signature axis (did the bytes match?)
+ the content axis (scan_hardened) + the diagnostician in one verdict.
② scripts/adversarial_env.py augmented with an inserting environment (the gateway appends
a ZWSP) and prints a diagnosis for each environment.
MEASURED by the harness: the identical SIGNATURE_INVALID was decomposed —
iconv→CHAR_LOSS(low-medium), NFKC→NORMALIZATION_EQUIVALENT(low),
sed→VALUE_SUBSTITUTION(high), ZWSP→INVISIBLE_INSERTION(high) + both axes ALARM.
Tests test_diagnose.py (10). Candidly: the diagnostician DESCRIBES, it does not judge —
intent remains with the human/policy; it works when both the original and the
current are available (the trace stores only a hash, so the diagnostician's home is
the element level / the harness, not verify_trace itself). 148 tests green.

### AD-43. Canon §13: OWNERSHIP ≠ POSSESSION (the seal of ownership) (2026-07-23)
**DECISION: PRINCIPLE CANONIZED.** The author's train of thought: signing/encryption
are mature, "a ceiling"; if a break is a matter of time, a BREAK ≠ APPROPRIATION
mechanism is needed; it leads to "the data owner sealing it". Canon §13: provenance is
raised from "the element's history" to TITLE. LAW: OWNERSHIP (title) ≠ POSSESSION
(possession) — crypto guards possession (it breaks), the owner's seal guards
ownership (it survives a break). The seal is OUTSIDE the data (there is no
indelible spot inside, §12), witnessed, dated BEFORE the theft, bound to an identity.
The candid boundary: it guards title, NOT possession (the thief holds the bytes but
is not the owner); key theft is residual (threshold + revocation + fork detection).

### AD-44. A working mechanism for the seal of ownership (2026-07-23)
**DECISION: BUILT (philosophy → code).** At the author's request "how to
turn this into a working mechanism". notarius/title.py — an assembly of bricks:
brand() (the owner seals hash + identity + time), TitleRegistry.witness()
(witnesses co-sign the FIRST seal on a hash, refuse a conflicting one),
resolve_title() (title goes to the quorum, a bare claim is rejected), transfer()
(a two-sided agreed transfer — both sign). PROVEN IN CODE
(test_title.py, 9): a thief broke into / copied the data, seals with their own key →
witnesses refuse → title stays with the owner, the thief is rejected (READING ≠ OWNERSHIP);
replaying others' co-signatures does not pass; a two-sided transfer is valid,
a one-sided/forged one is not. Demo in __main__. Candidly: it guards title,
not possession; theft of the owner's key is residual (custody/frost threshold + revocation +
cosign fork). 157 tests green.

### AD-45. Clarification: digital ink ≠ the semantic root (2026-07-23)
**DECISION: CANON §13 CLARIFIED.** The author's pointed question: is the seal digital or
semantic? Candidly: title.py is digital at its ROOT (signatures + keys), semantic in its
LOGIC (first-wins, consent, resolution by history).
The digital root inherits the same ceiling (break the key — forge it). A distinction
recorded: DIGITAL INK (rests on the key's secret, a single point of failure) ≠
THE SEMANTIC ROOT (coherence of a distributed history, no single point,
strength from the number of independent sources + earliness + corroboration). Real
resistance to a break lies in the semantic root, not in key length.

### AD-46. Title resolution by convergence (the semantic root in code) (2026-07-23)
**DECISION: BUILT.** title.py augmented: attest() (an independent record
source→owner), converge() (title goes to the owner with the greater number of INDEPENDENT
agreeing sources, and earlier; a tie → dispute). Proven in code
(test_title.py +5): a partial break (the thief broke 1 key) does NOT flip
the title given 3 independent records for the owner; a tie → contested; one source
counts once; min_sources enforced; a broken record does not count. This is
the parent's CONVERGENCE_TEST (FO-100), like real provenance (a network of
mutually-confirming records). CANDIDLY: convergence measures coherence
(the cost of forgery), NOT truth (FF-005 RECURRENCE ≠ VALIDITY); it is as strong
as the sources are genuinely independent (Sybil bypasses it); crypto is the ink
of the record (crypto-agility AD-23). 162 tests green.

### AD-47. Hybrid: digital axis + semantic axis; divergence = a signal (2026-07-23)
**DECISION: BUILT.** The author's question: can a hybrid be made from the two axes.
title.resolve_hybrid — title by BOTH axes (a digital quorum of the seal +
semantic convergence), each closing the other's weakness (the digital is
weak to a break, the semantic to Sybil; an attacker must defeat both).
CONFIRMED (both agree) / PROVISIONAL (one in favor, the other silent) / CONTESTED
(the axes diverge) / NONE. THE MAIN VALUE: the divergence of the axes IS ITSELF a signal —
if the digital says A and the semantic says B (probable key theft OR Sybil),
the hybrid marks CONTESTED and calls a human INSTEAD of silently handing over the title.
Proven in code (test_title.py +6): a break of the digital axis (a forged seal)
with a live semantic → CONTESTED (a pure digital would have handed it to the thief); Sybil with
a live seal → CONTESTED; one axis silent → PROVISIONAL. Residual: breaking
BOTH axes consistently is more expensive and noisier than either one. 168 tests green.

### AD-48. The "mirror" attack on the hybrid cross-check and its defense (2026-07-23)
**DECISION: HOLE ACKNOWLEDGED + DEFENSE BUILT.** The author's pointed finding: during
a break one axis can be SUBSTITUTED with a mirror one that agrees with the already
forged one — then both "agree" (CONFIRMED), and the divergence signal stays silent.
That is not two axes but one puppet theater. Acknowledged: the defense lives NOT in "two
axes", but in (1) DIFFERENT roots of trust, (2) an INDEPENDENT channel for obtaining an axis,
(3) a LOCKED past (an external anchor without an early trace of the mirror),
(4) OUT-OF-BAND pre-established trust.
Code (title.py): converge gained trusted_sources (ONLY
pre-established sources count — the thief's fakes do not); resolve_hybrid gained
source_keys + external_anchor + a check of root independence (witness ∩
source ≠ ∅ → independence undermined → CONFIRMED downgraded to CONTESTED;
contradiction of the external anchor → CONTESTED). Proven (test_title.py +3):
a mirror with new fake sources is repelled by the out-of-band set; a shared root of the axes
is flagged; a full mirror is caught by the external anchor.
IRREDUCIBLE RESIDUAL (candidly): if the thief controls ALL of the verifier's
channels AND there is no early external anchor — the mirror wins. Trust cannot be
bootstrapped from nothing: you need at least ONE independent trustworthy view that
the thief never touched (FO-005 INTERFACE ≠ REALITY). 171 tests green.

### AD-49. A public anchor, the "registry under glass" — an independent window (2026-07-23)
**DECISION: BUILT (idea 1).** At the author's request, bind an axis to a public
append-only anchor as an "independent view". The author's metaphor: the thief draws
only ON THE GLASS (the presented copy/channel), not on the registry; pull out the registry —
it is clean, and what was drawn stays on the glass. notarius/anchor.py: PublicAnchor (append-only,
a hash chain — the past cannot be rewritten; the first seal on a hash = authority; pull() —
pull a record from the REGISTRY, not from the presenter's hands; verify_integrity — a covert
edit of the past breaks the chain); reconcile() = reconciling the glass with the registry →
MATCH / FORGERY_ON_GLASS / NOT_ANCHORED. Publicness: cosign (a distributed
copy) + OTS/Bitcoin (anchor_ots_digest → stamp; network block, HONEST_LIMIT as in
AD-31). Proven (test_anchor.py, 10): a forgery on the glass is exposed by
reconciliation; a FULL mirror (both axes on the thief) is caught by the PULLED registry
(external_anchor from pull → resolve_hybrid CONTESTED); a covert edit of the past
is detected. BOUNDARY (the metaphor itself shows it): it works AS LONG AS the registry can
be pulled; the thief holds all channels + there is no early record → you see the glass forever
(FO-005). Weighting by earliness (idea 2) is a separate step. 181 tests green.

### AD-50. Weighting by earliness: the old beats a fresh flood (idea 2) (2026-07-23)
**DECISION: BUILT.** The thief fabricates only AFTER the theft → their records are
late; giving an old record more weight — a flood of fresh fakes will not outweigh it.
CRITICAL (and this ties to idea 1): the weight comes from the ANCHORED rank
(the order in the public append-only registry), NOT from the claimed date — otherwise the thief
backdates. anchor.source_ranks(data) → {source_pub: rank,
0=earliest}, append-only ⇒ the rank cannot be understated. title.converge_weighted:
weight 0.5**rank (a geometric decay — the sum of the late is bounded, the early
dominate). Proven (test_title.py +3): 2 early sources for the owner beat
20 late fakes; a backdated claimed_at does not help (the weight is from the rank);
a non-anchored source = 0 (earliness not proven). The public anchor (AD-49)
PROVES earliness — without it "I recorded it earlier" is just words. CANDIDLY:
earliness ≠ truth (FF-005); the residual is REALLY early fakes planted in advance
(expensive foresight). 184 tests green.

### AD-51. A unified resolve_full + a robustness stress test + a verdict (2026-07-23)
**DECISION: ASSEMBLED, TESTED, VERDICT HUMAN-READABLE.** At the author's
request "assemble everything, stress-test it against external resources, then
a human-readable verdict".
ASSEMBLY: title.resolve_full — 4 signals in one call (the digital axis + weighting by
earliness + the public anchor pull + mirror protection) → confidence
ANCHORED_CONFIRMED/ANCHORED/PROVISIONAL/CONTESTED/TAMPERED/NONE +
human_verdict (human-readable: to whom the title goes, how confidently, why).
TEST (scripts/stress_title.py, actually measured):
(1) FUZZ 500 random scenarios (flood 0–200, break of the digital axis, backdating)
    → THE THIEF GOT THE TITLE 0 of 500; the break of the digital axis actually happened 169 times
    and was caught by the anchor as CONTESTED 169/169.
(2) EXTERNAL PROCESS: SHA-256 reconciled with openssl (an independent implementation) —
    0 discrepancies out of 50.
(3) EXTERNAL NETWORK: a probe of 10 public anchors (blockchain/TSA/OTS) → egress
    closed by policy (000/403); candidly marked unavailable, NOT faked.
Unit tests test_title.py (+3): clean→ANCHORED_CONFIRMED, mirror→CONTESTED,
registry edit→TAMPERED. Verdict document: TITLE_ROBUSTNESS_VERDICT_2026-07-23.
BOUNDARIES: not truth / not possession / not coercion; the residual is the forever glass
(the thief holds all channels + there is no early record); the network anchor requires an
environment with the network. 187 tests green. A prototype-principle with MEASURED robustness.

### AD-52. Package build (PyPI format), WITHOUT publishing (2026-07-23)
**DECISION: AN INSTALLABLE PACKAGE BUILT; PUBLISHING IS THE AUTHOR'S.** At the
request "pypi/npm, package it into a package registry". npm is not applicable (there is no JS) →
the target is the PyPI format. Created: pyproject.toml (setuptools; name=notarius,
0.1.0, author Ruslan Malyavskiy, dep pynacl; extra [integrations]=reedsolo+
opentimestamps; license-files=[] for compatibility), notarius/__init__.py
(version + author, WITHOUT heavy imports — installs without optional dependencies),
NOTICE.txt (license TBD/AD-7, COMMERCIAL USE PROHIBITED), py.typed.
VERIFIED: python -m build → sdist+wheel; twine check PASSED (ready for
a registry); installation into a clean venv + import of the core (pynacl only) OK; the extra
[integrations] OK; 187 tests green (package mode did not break it).
BOUNDARY (important): I do NOT publish to the PUBLIC PyPI — the project is private,
COMMERCIAL USE PROHIBITED, publishing is irreversible and requires the author's token.
The dist/ artifacts are in .gitignore (not in git); the wheel was handed to the author. Publishing
(twine upload) is under the author's token and decision, to a private
index if desired. Choose the license (AD-7) BEFORE any publishing.

### AD-53. Supply-chain: a code injection lands "on the glass" (2026-07-23)
**DECISION: BUILT + DEMO ON OUR WHEEL.** The author's train of thought: a hacker thinks they are
inserting code into the ORIGINAL (the genuine one), but they are actually inserting it ONTO THE GLASS (into
the delivered copy). The §13 principle "the registry under glass", applied to CODE
(adopt: code signing + transparency logs Sigstore/SLSA/PEP 740).
notarius/supply.py: ArtifactRegistry (append-only, the first seal on a
package_id = the original, a hash chain) + verify_delivery → MATCH /
FORGERY_ON_GLASS / UNKNOWN_PACKAGE / REGISTRY_TAMPERED. Proven
(test_supply.py, 5): an injection into delivery is exposed by reconciliation; a late
re-registration by the thief does not displace the original; a registry edit is detected.
DEMO ON A REAL ARTIFACT (scripts/supply_chain_demo.py, our wheel of 62601
bytes): the original→MATCH, the injection→FORGERY_ON_GLASS (the hashes diverge) — it tied
the AD-52 packaging to the defense with one live example.
CANDID BOUNDARIES: it catches an injection into DELIVERY (the glass: mirror/CDN/build/MITM);
it does NOT catch an edit of the SOURCE itself (a hijack of the maintainer's key → SIGNED ≠ NATIVE,
the registry is poisoned, reconciliation passes) — the cure is a THRESHOLD (custody/frost) +
PUBLICNESS (cosign); dependency-confusion = a mirror (AD-48); a signed
backdoor = not "safe", but "the author's code was not touched in delivery" (AD-24/28).
192 tests green.

### AD-54. Prototype→product roadmap (general, candid) (2026-07-23)
**DECISION: MAP READY; THE CASE CHOICE IS THE AUTHOR'S.** At the request "can we
turn it into a product?" + the author's choice "a general roadmap first". Document
PRODUCTIZATION_ROADMAP_2026-07-23_EN.md: where we are (RESEARCH_TRACK, 0 STRONG,
the prototype packaged), the general prototype→product gap (validation/audit,
license AD-7, replacing demos with production, threat model, user-facing
plumbing, a candid position), a component-readiness table (what is production / what is
reference / what is demo / what is network-blocked), case-selection criteria, candidates
against the criteria, a recommended sequence, what CANNOT be promised.
KEY CONCLUSION: our strength is the delivery layer (append-only + reconcile, without
heavy crypto); the readiness weakness is a real threshold (FROST) and a live
network anchor. Choose the first case TO FIT THE STRENGTH. The shortest entry is the supply
chain (integrate into Sigstore/SLSA/PEP 740), the most valuable-but-longest
is chain-of-custody for a vertical. Decisions are needed from the author: the case, the license
(AD-7), a real first user. No code; 192 tests green.

### AD-55. License: dual AGPL-3.0-or-later + commercial (CLOSES AD-7) (2026-07-23)
**AUTHOR'S DECISION: DUAL LICENSE.** Open — AGPL-3.0-or-later; commercial
— a separate author license for proprietary/closed use.
IMPORTANT CORRECTION: this LIFTS the earlier "COMMERCIAL USE PROHIBITED" — under AGPL
commerce is ALLOWED with copyleft (§13: a network service opens its sources);
control is now through the copyleft barrier + selling commercial licenses, not
through a ban. Set up: LICENSE (dual + the standard AGPL notice; the canonical
674-line text is NOT embedded — egress is closed, I do not type legal text by hand, a
command `curl ... agpl-3.0.txt` is given for insertion before publishing),
COMMERCIAL-LICENSE.md, NOTICE updated, pyproject license="AGPL-3.0-or-later
OR Commercial" + the AGPLv3+ classifier, SPDX headers in 19 sources
(notarius/+algorithms/). Dependency compatibility: pynacl (Apache-2.0),
reedsolo (MIT), opentimestamps (LGPL-3.0) — all compatible with AGPL-3.0.
The wheel was rebuilt, twine check PASSED, 192 tests green.
I AM NOT A LAWYER: commerce requires legal review (patent clearance, the form of
the commercial license). BEFORE a public release: (1) insert the canonical
AGPL text into LICENSE, (2) legal review. The choice is reversible now (not publicly released).

### AD-56. Product dossier: the code supply chain (grounded in sources) (2026-07-23)
**DECISION: DOSSIER READY.** The case is chosen (the one recommended in AD-54 + the author's
impulse AD-53). PRODUCT_DOSSIER_SUPPLY_CHAIN_2026-07-23_EN.md; the market part
is checked by 2025-2026 web search (not from memory). KEY FACTS: the market is mature,
the incumbent is Sigstore (Linux Foundation, cosign/Fulcio/Rekor), npm provenance
(SLSA L2+Sigstore), PyPI PEP 740 (270k+ attestations); building our own log is not an option.
OUR GAP (confirmed by Sigstore's threat model): keyless does not guarantee that the
signer had the right (OIDC hijack) or that the artifact is "good" — SIGNED ≠ NATIVE;
Sigstore's threshold is only on the root, 3-of-5, NOT on package publication. Two wedges:
A — threshold PUBLICATION of a release (M-of-N maintainers; our custody/frost/
cosign/convergence; the cost — Rust-FROST + a network effect, slow); B —
a consumer gate-verdict on top of ready-made attestations (verify Sigstore/
npm/SLSA + a threshold policy + a human-readable CONFIRMED/CONTESTED from
resolve_full/diagnose; faster). VERDICT: viable as an OVERLAY, not a
replacement; the risk is a crowded field, and without a real design-partner this is again
research. The cheap next step is a live competitive comparison of specifications.
No code; 192 tests green. Sources in the dossier.

### AD-57. Live competitive comparison → "no" to the code-supply-chain product (2026-07-23)
**DECISION: A CHEAP, JUSTIFIED "NO".** §9.0 of the dossier — a comparison against live
sources (2025-2026). COMPETITIVE_SCAN_SUPPLY_CHAIN_2026-07-23_EN.md.
FINDINGS (grounded): both of our wedges are already covered by prior art —
(A) threshold multi-maintainer publication = **TUF** (delegations + thresholds,
CNCF); (B) the consumer gate = **Kyverno / cosign policy-controller**
(admission verification). The acknowledged gap "maintainer compromise" is being
**plugged by the SLSA Source/Dependencies Track already**. Only a thin
slice remains — a human-readable aggregated honest verdict (our diagnose/
resolve_full), but that is a FEATURE, not a moat. CONCLUSION: the code supply chain is a red ocean
(TUF/Sigstore/SLSA/Kyverno/in-toto/GUAC, CNCF/LF/Google), and entry = competing
with giants over narrow UX. The comparison did its job: it showed this BEFORE building.
PIVOT: (1) a feature contribution to something existing, OR (2) a pivot into a NON-code
vertical (chain-of-custody: legal/forensics/finance) — the code stack is not
present there, and our GENERAL model (title/anchor/diagnose) has a place. Advice:
consider §2 — the "valuable-but-long" candidate from the roadmap now with a factual
justification for WHY not the code supply chain. No code; 192 tests green.

### AD-58. Positioning without crypto jargon: the product = an honest history, not storage (2026-07-23)
**AUTHOR'S DECISION: "yes, I agree, do it".** A course correction: we stumbled over
code (doors/inputs/outputs, supply-chain) and buried the product under crypto plumbing; in
that form a client will take NOTARIUS for "yet another cloud storage". The author: the main
thing is **semantic tracing**; signing/identification are needed, but they are not the pitch;
let the integrations ("doors") be written by whoever buys it. POSITIONING_2026-07-23_EN.md
— a one-pager WITHOUT crypto jargon, with only the meaning brought to the top and all the tech
under the hood. THE ESSENCE: the product sells the **honest HISTORY of a piece of information**
(where it came from, what was done to it, where it is native / slipped in, what exactly changed,
how much to worry), NOT storage/cipher/safe. The contrast: "they guard WHERE
it lies and whether it is locked; we tell WHAT happened — and find the place of the
substitution". Analogies: a black box / a medical record / a chain of custody
(not a safe). The product boundary: ours = the trace + signature/identification +
a human-readable analysis; the buyer's = the doors/integrations for their industry.
The candid boundaries are preserved (the trace finds the lie ≠ proves the truth; sealed
≠ genuine inside). No code; a document + a record. The prior 192 tests are green.

### AD-59. Pivot into the chain-of-custody vertical (non-code), grounded in sources (2026-07-23)
**AUTHOR'S DECISION: "option 2".** We took the AD-57 §2 recommendation (a pivot out of the red
ocean of code supply) and checked it with a live comparison BEFORE building.
PIVOT_CHAIN_OF_CUSTODY_2026-07-23_EN.md. THE MAIN CORRECTION TO AD-57: the field
turned out NOT empty — digital evidence management ~$8.6→21.5 bn (CAGR 12%),
digital forensics ~$13.8→35 bn; giants OpenText/Cellebrite/Magnet/Exterro/
MSAB (~38% of revenue) + Motorola/Tyler/Veritone. Law enforcement/forensics is also
a red ocean, we do not go head-on. WHAT the incumbents do NOT do: they manage
storage / log WHO-touched-it (where it is locked), blockchain CoC gives tamper
DETECTION yes/no; NO ONE gives tamper LOCALIZATION (what exactly changed —
our diagnose) + an honest aggregate verdict over heterogeneous witnesses
(CONFIRMED/CONTESTED — resolve_full) + reconcile protection against the mirror +
substrate-independence. OUR EDGE lands in an acknowledged gap: blockchain
records "it-was-at-T", but does NOT have legal recognition (eIDAS is needed; the court
needs to be shown WHAT was substituted). CANDIDLY: an edge of a FEATURE, not a moat; narrow. THE UNOCCUPIED
NICHE — sub-vertical #1: document/IP/inter-organizational handoff OUTSIDE the badge,
where heavy forensic suites are overkill, and "localize the lie + a human-readable
verdict" has direct value; there we are a diagnostics layer over someone else's
storage, not a replacement. The form is as in AD-58: an engine of honest history, the buyer writes
the doors. THE CHEAP STEP: run ONE real scenario (a contract/report between
two parties) through the ready-made stack end-to-end as a demo (FO-035), then a
design-partner. No code; the prior 192 tests are green. Sources in the document.

### AD-60. Demo of sub-vertical #1: an inter-organizational handoff on a concrete object (2026-07-24)
**AUTHOR'S DECISION: "do this demo".** The cheap next step from AD-59 —
check the fit on a CONCRETE object (FO-035), not on a slide.
scripts/handoff_demo.py: Party A ("Aktiv-Finance") sends Party B
("the Auditor") a payment report; along the way a compromised channel changes the amount
1000000→9000000 and masks the edit with an invisible ZWSP inside a word. An end-to-end
run through the READY-MADE stack, WITHOUT new core code: brand + two witnesses
(TitleRegistry) + attest + PublicAnchor → resolve_full/human_verdict;
on receipt assemble (diagnose) + reconcile. RESULT (reproducible):
(1) the original → ANCHORED_CONFIRMED, the honest sender's title stands;
(2) what was received → A BREAK: diagnose gives VALUE_SUBSTITUTION 1000000→9000000
(review=high) + scan ALARM/zw_wordsplit (the concealment exposed), reconcile →
NOT_ANCHORED (this is NOT the anchored artifact); (3) the thief seals the original
retroactively → witnesses 0/2 (the first-seal is taken), reconcile → FORGERY_ON_GLASS
(the registry remembers Aktiv-Finance). Crypto under the hood, and at the top a human result
(as in AD-58). The boundaries are preserved (TRACE_LOCATES_THE_LIE ≠ PROVES_THE_TRUTH; it does not
replace legal expertise). The core is untouched; 16/16 test files green.
CONCLUSION: the product's edge (localization + an honest aggregate verdict + protection against
the mirror) works on a real non-code scenario out of the box — the next step is no longer
code but the search for a design-partner who feels this pain.

### AD-61. A one-page demo scenario to show a partner (2026-07-24)
**AUTHOR'S DECISION: "a one-page demo scenario to show a partner".**
DEMO_HANDOFF_ONEPAGER_2026-07-24_EN.md — a partner-facing retelling of the AD-60
run WITHOUT running Python and WITHOUT crypto jargon (as in AD-58): the pain in the
partner's words ("is this what was sent to you?"), the scenario (Aktiv-Finance→Auditor,
amount 1000000→9000000 + a hidden edit), what the receiving side sees (CONFIRMED /
A BREAK where+what / appropriation EXPOSED), a "not yet another safe" table, the candid
boundary (not a verdict on intent, does not replace legal expertise), and an explicit
request to the partner: give ONE real handoff scenario to run on their
data. Crypto under the hood; the buyer writes the doors. No code; a document.

### AD-62. The one-pager failed the 4-line test → radical simplification (2026-07-24)
**AUTHOR'S FEEDBACK: "read it and understood nothing; a person reads 4 lines, doesn't
get it, throws it in the trash".** The author — the source of the idea himself — did not understand HIS OWN
one-pager (AD-61). The disciplinary conclusion: the text is at fault, not the reader; the
scaffolding (the table, "title", "the registry under glass", the meta-frame "the pain we
take on") stood IN FRONT OF the essence. Rewrote DEMO_HANDOFF_ONEPAGER from scratch: one
live scene + a number-punch in the first 4 lines ("an invoice for 1,000,000 → along the way
9,000,000, an extra zero, invisible to the eye, you pay nine instead of one"),
then one phrase of what we do ("here is the line — here is what was substituted"), one question
in large type ("is what arrived the real thing?"), and one candid boundary line
at the bottom. Removed EVERYTHING: tables, mechanics, crypto words, product terms.
The acceptance criterion — understandable from 4 lines. No code; 1 document rewritten.

### AD-63. One-pager → funnel: hook → simple → complex → "hand off to specialists" (2026-07-24)
**AUTHOR'S DIRECTION:** the hook (AD-62) catches — keep it; then lay it out in
LAYERS: simple first, then complex, so that the investor, reading down to the
complex part, understands that what comes next is for his technical specialists. Built
DEMO_HANDOFF_ONEPAGER out into a descending funnel: (0) the hook about the extra zero without
changes; (1) "If put very simply" — what we do in one phrase, for whom;
(2) "What it is as a product" — history vs storage, three things (we confirm /
catch-and-name / expose appropriation), who feels the pain, the boundary "the engine is ours —
the doors are yours", a candid line about the market; (3) an EXPLICIT divider "↓ next —
for your technical specialists" → the mechanism (three pillars: Ed25519 +
a witness quorum + an append-only registry), localization of the substitution, an aggregate
verdict, substrate-independence, candid boundaries for due diligence, where
to look at the code. The investor gets a clean off-ramp to his people. No code;
1 document rewritten.

### AD-64. Minimal product: run it on YOUR OWN file (notarius check/seal/verify) (2026-07-24)
**AUTHOR'S DECISION: "we need a product, to run something of our own on it, then we
will understand what it is and what it is not".** Enough carrying paper — we need a working
minimum that the author himself will run on his own document. notarius/cli.py +
__main__.py: a thin shell over the READY-MADE core (diagnose/scanner), without keys
or installs, pure stdlib. Three commands: `check REFERENCE ARRIVED` — compare
and say in plain terms WHERE (line number, difflib) and WHAT (diagnose:
VALUE_SUBSTITUTION etc.) was substituted + expose a hidden edit (scan_hardened);
`seal FILE` — take a receipt-fingerprint (.ntr); `verify FILE` — same/touched.
Run on real files (the 1000000→9000000 scenario + an invisible ZWSP):
check pointed to line 3, the category, the concealment; verify distinguished clean/changed;
binaries do not crash it. The console script `notarius` in pyproject (AD-52). Test
tests/test_cli.py — 10 checks; 17/17 test files green. The boundaries are
preserved (we show where, not a verdict on intent). This is the FIRST time the
project has something that runs on user input; next — learn
from the runs "what it is and what it is not", not build blind.

### AD-65. HTML mockup of the product: the buyer's screen, colors tuned for trust (2026-07-24)
**AUTHOR'S DECISION: "we need an HTML drawing with buttons of what the buyer
will see; tune the colors so it inspires trust".** docs/product_mockup/
notarius_ui.html — an interactive mockup of the "Check" screen: two documents side by side
(reference → arrived), a "Check" button, three example scenarios (Genuine /
Amount substituted / Retroactive forgery), and below them a verdict with a colored severity
bar. DESIGN FOR TRUST (not a bright startup but notarial-banking
restraint): petrol-navy as ink + a brass hairline as a seal;
the semantics calm (forest/clay/brass, not shouting); headings — a serif
(gravitas), the interface — system-ui, the document reader — mono with tabular
figures; deliberately without the purple-gradient cliche. Both themes via tokens,
a toggle. In the "substitution" scenario you see exactly the product value: line
3, 1,000,000→9,000,000 in red, the invisible char marked "invis." The bottom — the candid
boundary + "the engine is ours, the doors are yours". Published as an artifact for showing.
Self-contained HTML (CSP-safe, system fonts, no CDN). It does not touch the core.

### AD-66. Record in plain text "what we can do now vs. what we'll build" (text vs. photo/video) (2026-07-24)
**AUTHOR'S DECISION: "this needs to be captured somewhere in plain text like this".**
In response to the author's question "can you upload video and photos this way too?" — a candid answer
at two levels, now recorded: CHTO_UMEEM_SEYCHAS_2026-07-24_EN.md. Two
different questions: (1) "same/touched" — coarse, ALREADY works for anything
(text, photo, video, archive — the fingerprint catches a byte change); (2) "where and what
exactly was substituted" — fine, RIGHT NOW only for text (there are lines/words/numbers
to compare; a photo has pixels, a video has frames — a separate "reader" is needed for
media). Matrix: same/touched ✅✅; where-and-what ✅ text / ⛔ media. The good
news: the model is not tied to text (substrate-independence, FO-013), only the
media "reader" is missing — that is the next piece, not today's button.
Simple language, for showing a buyer; the candid boundary is preserved. No code.

### AD-67. In plain words: what a reference is and why everyone reconciles against one (2026-07-24)
**AUTHOR'S DECISION: explain simply what "your own reference" is, how it
appears, and how the counterparty works with THAT ONE — not with their own, not with a shared
editable one, not with an outside one.** CHTO_TAKOE_ETALON_2026-07-24_EN.md — the most
important trust question of the product, laid out without jargon on top of the ready-made mechanism
(seal + anchor "the registry under glass", AD-49/50/64). THE ESSENCE: the reference = the fingerprint
of the original, taken at the moment of birth by the one who created it (not a copy in a drawer);
it appears on "Seal" — the fingerprint is written into a shared open registry
(one document / fingerprint / moment); it lies NOT with the parties but under glass (everyone can
look, no one can rewrite, first-wins, forward only); the counterparty reconciles
what arrived not with its own and not with the sent copy (that one could have been substituted in transit), but
with the fingerprint in the registry. A table of four "references" — only one is real
(the author's, early, immutable). Why an outside one cannot be slipped in: append-only +
first-wins → a late forgery lands "on the glass" and is exposed. Language
for the buyer; the mechanism is not new, only the explanation is. No code.

### AD-68. A candid answer: "what if the program is only on the client's side?" (2026-07-24)
**AUTHOR'S QUESTION (point-blank):** I write an invoice in Word, send it by email, along the way the number
is altered — how does the client learn that I wrote something else, if the program is only on
their side? A_ESLI_PROGRAMMA_TOLKO_U_KLIENTA_2026-07-24_EN.md — a CANDID "NO" with
a condition. PLAINLY: if the sender made ONLY the letter — the client CANNOT
learn it, there is nothing to reconcile against; this is not a weakness but a law (you cannot notice a substitution
without an untouched original to compare with). WHY: catching a substitution = two things
over two roads (the document + an independent mark); the interceptor owns the postal
road, so a mark on the same road is useless. THE FIX: the sender must perform
ONE action — "seal" the invoice at the moment of creation; the fingerprint goes to the registry
"under glass" (a different road, out of the interceptor's reach). Then the client reconciles
what arrived with the registry → the substitution is exposed with "where/what". The interceptor does not
substitute the mark (append-only, first-wins, written at birth before them).
THE MAIN CONCLUSION: the program CANNOT be only on the client's side — it is two touches
(the sender marks, the client reconciles); the mark = one button or automatic inside
billing (this is the buyer's "door"). It closes the conceptual before-fact hole
(echoes AD-9 "self-declaration" / earliness AD-50). No code.

### AD-69. Distribution model: the engine is embedded in other people's programs (2026-07-24)
**AUTHOR'S REALIZATION:** our program can be embedded into mail agents, accounting
programs, messengers, CRMs, and other means of exchange. Confirmed — this is the correct
model. KUDA_VSTRAIVAETSYA_2026-07-24_EN.md. THE ESSENCE: not a standalone application but an
embeddable ENGINE; the two touches live inside familiar programs — the mark where
the document is BORN (accounting/billing/1C/ERP/CRM, on the "Send" button,
invisibly), the reconciliation where it is RECEIVED (mail/messenger/CRM inbox/EDI).
Ours = the engine (mark/reconcile/the where-and-what verdict); not ours = the "door" (an Outlook
plugin, a 1C module, a bot, a CRM app) — written by whoever embeds it. Business model:
license the embeddable engine, do not sell a box (matches AD-58
"the engine is ours, the doors are yours" + AD-55 dual-license). CANDID EDGES (not to hide):
(1) the mark is needed on BOTH sides — distribution is two-sided, a network effect;
(2) the registry "under glass" must be accessible to both (within a company it is simple,
between companies — an agreed shared/public one); (3) the mark must be applied
invisibly; (4) "where and what" is still text (AD-66). No code; a record of the model.

### AD-70. A check "on one computer, two mail accounts" (2026-07-24)
**AUTHOR'S QUESTION:** can it essentially be checked on a computer — two different
mail accounts, run it? YES. scripts/two_accounts_demo.py: three roads on
one computer — glass_registry (the reference under glass, the sender puts it there at
birth, out of the interceptor's reach), alpha_outbox (the sender), beta_inbox
(the recipient, where the mailman operates). The transport is folders (the network is closed in the environment),
but the run is through the REAL product (cmd_seal/cmd_check). RUN: the sender
prints the invoice (the mark into the registry), "the mail" delivers to beta's inbox, the mailman
edits the attachment (1,000,000→9,000,000 + an invisible char), the recipient reconciles the incoming
with the reference under glass → A BREAK, line 3, VALUE_SUBSTITUTION, zw_wordsplit;
the HONEST-DELIVERY CONTROL → "not touched", with no false alarm. Candid subtleties:
(1) real mail does NOT corrupt the attachment itself — the interceptor is played deliberately;
(2) folders→SMTP/IMAP = a thin adapter; (3) the mark goes over a DIFFERENT road (the registry),
not in the letter — otherwise the interceptor would change it too. The demo returns 0 (rc=1
"the break was caught" — expected). The core is untouched; the prior 17/17 test files.

### AD-71. A working tool for real mail (SMTP/IMAP) + a self-test (2026-07-24)
**AUTHOR'S DECISION: "I want it" (a working script for real mail).**
scripts/notarius_mail.py — the "folders→SMTP/IMAP" adapter from AD-70, brought up to a
tool; standard Python (smtplib/imaplib/email) + our seal/check, without
extra dependencies. Commands: send (prints the reference into the shared registry over a DIFFERENT
road + sends a letter with an attachment), recv (fetches over IMAP, extracts the attachment,
reconciles with the reference → a where/what verdict), selftest (a full loop WITHOUT the network through
a mail-yard folder). The registry — the NOTARIUS_REGISTRY variable (a shared folder "under
glass"); credentials via env (an app-password, not hardcoded). A BUG caught on
the self-test: the interceptor edited the raw .eml bytes, but the attachment is in base64 →
the substitution did not reach it, and the reconciliation candidly said "not touched"; FIXED — it edits
the DECODED attachment (email.policy.default + set_content). After the fix,
selftest: A BREAK line 3, 1000000→9000000 through a full email round-trip
(the same code that will go to a real SMTP/IMAP). Instructions for two real
Gmail accounts — docs/POCHTA_INSTRUKCIYA_2026-07-24_EN.md. Candid subtleties: mail
does not corrupt the attachment itself (the interception is simulated), no reference → nothing to reconcile against
(AD-68), the registry over a different road. In this environment the network is closed — a real
SMTP/IMAP was NOT run, only the offline path is proven. The core is untouched.

### AD-72. Step-by-step Windows instructions for a non-technical author (2026-07-24)
**AUTHOR'S FEEDBACK (typed in the wrong keyboard layout): "I didn't understand how to do this
step by step".** The author is on Windows, not a programmer — commands with env variables
are too complex. WINDOWS_POSHAGOVO_2026-07-24_EN.md: the simplest possible steps
to the first success — the self-test (no mail/passwords): (1) install Python with
the Add to PATH box checked; (2) download the branch ZIP from GitHub, extract it; (3) in the address
bar of Explorer type cmd; (4) `python scripts\notarius_mail.py selftest`
(+ fallback `py`). Shown what will appear (A BREAK line 3). The real two-mailbox setup is
the next step, with an offer to make a settings file if the long commands
are hard. Nothing in the code; pure accessibility. Lesson: even a ready-made tool is
useless if the author cannot run it — the first success comes first.

### AD-73. A blind pipeline prompt: the engine's application horizons (2026-07-24)
**AUTHOR'S DECISION: "prepare a prompt for the pipeline for external reviewers".** After
a brainstorm of wild applications (VPN/sensors/AI/laws) — check our
view with an independent external signal, like the VENDOR_PROMPT series (AD-20/25).
VENDOR_PROMPT_ENGINE_HORIZONS_EN.md — a blind prompt to send to several
models (Copilot/DeepSeek/Qwen/Kimi/Gemini). THE BLINDNESS DESIGN: the engine is described
NEUTRALLY and technically (a seal at birth + an append-only log + localization of
the substitution + an invisible-char detector + a human-readable verdict + substrate-
independence + candid boundaries), WITHOUT our conclusions/marketing; blocks 1-4
(applications / prior art / ranking / adversarial) are answered
BEFORE reading block 5; our 4 candidates (invoices / prompt-injection / integrity-VPN
/ sensor-signature) are given only in block 5 for critique, so as not to anchor
the independent list. We ask for concrete names, distinguishing the new from the prior,
a candid "no", no flattery; a structured format for synthesis. The technical
description (not crypto-under-the-hood, as in the buyer one-pager AD-58) is deliberate:
the reviewer audience must recognize the primitive to name TUF/Sigstore/C2PA.
No code; a survey instrument.
ADDENDUM (same AD): at the author's request "what can the engine do NOT as
identification" the prompt was extended with a blind block 5 — the engine decomposed into FOUR
general-purpose machines (a discriminator / a cleaner / a fingerprinter /
an orderer) with a request to find NON-identification applications (understanding/
cleaning/organization/coordination/transfer); the former critic block became block 6, with
our non-identification candidates added to it (a summary of edits, invisible-char hygiene,
dedup/content-addressing, a first-wins lock, portable
metadata). The format was updated.

### AD-74. Preparing for going public: a clean license structure (2026-07-24)
**AUTHOR'S DECISION: "how to make the project public" → chose "insert the AGPL license
text" before opening it.** A candid environment boundary: the canonical
AGPL-3.0 text is NOT obtainable in this sandbox (gnu.org 403, WebFetch 403, the full
text is not on the system), and one must not type/paraphrase a license — only
verbatim. DECISION: let the verbatim official SPDX text be inserted by GitHub ITSELF
via its license template (100% authoritative). To that end the structure is brought to
convention: the dual-license explanation moved to LICENSING.md, the LICENSE name
freed up (git rm) for the GitHub template → the user inserts
the canonical AGPL as LICENSE in 5 clicks. README and the registry are updated. The rest of the
preparation for going public (merging the branch into main / a review of what will be opened) is at the author's
choice later; a reminder about the irreversibility of publishing was given. No code.

### AD-75. First horizons reviewer: a synthesis of what is confirmed/rejected (2026-07-25)
**EVENT:** the first external reviewer came back on the AD-73 prompt (the author pasted
the answer). engine_horizons_review1_2026-07-25_EN.md — a synthesis. It CONFIRMED
INDEPENDENTLY our framing: the value = field-aware + transformation-tolerant +
cross-channel provenance + an explainable localized verdict, NOT "sign a
document". TOP-3 bets: (A) financial critical fields 5/5 — a sharpening:
sign the STRUCTURE (a supplier record), not the PDF hash; (B) Agent Configuration
Provenance 5/5 — NEW, we underrated it, the field is not settled; (C) laboratory/
industrial field-level chain of custody (our AD-59). REJECTED with justification:
Integrity-VPN (already TLS; endpoints), a universal prompt-injection firewall,
camera/deepfake (C2PA), a universal signature / a new Git/IPFS/blockchain/world
name registry, signature=truth. THE STRONGEST COUNTERARGUMENT: the primitives exist,
the bottleneck is the trusted input point / keys / adoption / uptake; localization
is NOT valuable everywhere (a binary/certificate/command → any mismatch = do not
run); horizontally = a library, a product only with a vertical
contract (7 conditions) + a minimal experiment (100–500 objects, FP/FN, the share of
"disputed", whether it reduces manual review). The reviewer's caveat: his web search 401 →
competitors from memory, not a fresh scan. RECOMMENDATION: narrow to one vertical
(A financial — sellable; B agent-config — unoccupied), add 1–2
reviewers for triangulation. No code; synthesis 1 of N.

### AD-76. Second reviewer + cross-synthesis: focus on financial fields (2026-07-25)
**EVENT:** reviewer #2 came back (the AD-73 prompt). engine_horizons_synthesis_
2026-07-25_RU.md — a cross-synthesis of #1+#2. STRONG CONVERGENCE (both independently):
(1) the differentiator = LOCALIZATION of the type of change, not the signature; (2) AI/agent
inputs — the hottest zone; (3) documents — taken by the signature, the niche is in forensic
localization; (4) THE DECIDING RISK — there is value ONLY if the consumer actually
reconciles against an INDEPENDENT log, otherwise it degrades to a free hash+diff;
(5) a shared kill-list: VPN/camera/universal signature/Git/IPFS/ledger/
a standalone cleaner; (6) the engine makes a substitution visible, not impossible, and does not
prove truth. DIVERGENCES: AI-Unicode as a product (#2) vs a feature (#1) → the pilot decides;
the code supply-chain is in #2's top-3, but our live scan AD-57 = a red ocean
→ we trust the scan, we do NOT go. CONVERGING WILD CARDS (a signal): the integrity of an
AI agent's memory, attestation of "what the agent saw", the archaeology of artifacts. THE MAIN CONCLUSION:
choose a vertical by the presence of a NATURAL mandatory check, where
the verifier is ANOTHER motivated party with a blocking action. By this
criterion the BEST of all is FINANCIAL CRITICAL FIELDS (the payer is motivated
to check before paying — this removes the deciding risk for both). Recommendation: focus on
financial fields, AI-Unicode as a second track, do not touch the kill-list. Both reviewers'
web checks failed → competitors are indicative. No code; 2 of N.

### AD-77. Third reviewer (Kimi, with code access) → triple convergence + 3 defects (2026-07-25)
**EVENT:** reviewer #3 (Kimi) had access to the repository and VERIFIED the claims
BY EXECUTION. The synthesis is updated to three (engine_horizons_synthesis_2026-07-25_RU).
TRIPLE CONVERGENCE: the differentiator = localization; the vertical = documents between
parties; the deciding risk = "who actually reconciles"; the shared kill-list (VPN/camera-
C2PA-in-hardware/supply-chain/universal signature/blockchain notarization). KIMI ABOVE
THE OTHERS: (A) 3 REAL DEFECTS, verified in code — a homoglyph is not
classified (only CONTENT_CHANGED); backdating → INTACT (anti-backdate
only with an external anchor, README defect #3); cosign fail-open (INTACT+warning
where fail-closed is needed); (B) a sharpening — documents OUTSIDE the EDI perimeter (EDI is closed,
it does not reach the gray channels where BEC lives); (C) a new empty niche "version
handshake" (reconciling versions between orgs without a shared platform); (D) a bridge —
the word-fingerprint (human_fingerprint.py already exists) for reconciliation "without installing
software"; (E) a hard counterargument — the market pays for BEING EMBEDDED in the workflow, not for
byte identity (the engine = 5% of the value). RESOLUTIONS by vote: AI-Unicode =
a component, not a product (2:1); the code supply-chain — do not go (3:1 + AD-57). THE MAIN
CONCLUSION: the vertical = documents/details outside closed perimeters, ONLY embedded
in mail/messenger (not standalone) — this connects to the AD-69 model. DEBT BEFORE
THE PILOT: fix Kimi's 3 defects. A 4th reviewer is not required. No code; 3 of N.

### AD-78. Fourth reviewer (PDF) — an outlier on the ratings, a 4th confirmation of the risk (2026-07-25)
**EVENT:** reviewer #4 (PDF, with references to C2PA/TUF/ipfs-log). The synthesis is updated
to four. #4 is the LEAST CRITICAL, a marketing tone. HIS TOP-3 CONTRADICTS
the other three: he puts prompt-injection / camera-IoT / Integrity-VPN, and
calls documents/finance "a trap". BUT the VPN/camera justification is a naive "our
engine is more universal/lighter", already dismantled by Kimi's specifics (C2PA in hardware;
VPN=TLS/zkTLS) → we weight #4's ratings low. His "documents=a trap" is about GENERAL
e-signature (everyone agrees), he missed the narrow niche of field-localization outside
the perimeter. THE VALUABLE FROM #4 (a 4th independent confirmation of the risk): "a tool of
exposure, not of trust"; "investigation after, not prevention"; three
limitations — trust in the log, the need for an active consumer (people ignore
warnings), WHAT-not-WHY. A USEFUL SHARPENING: viable where an audit is a
legislative/regulatory REQUIREMENT (legal/finance/public administration): regulation
FORCES reconciliation, removing the problem of indiscipline. UPSHOT: the conclusion did not change,
it was reinforced — the first vertical = documents/details outside a perimeter WHERE the check is
mandated by regulation. Adding reviewers is not needed. No code; 4 of N.

### AD-79. Fixing the three defects found by Kimi through execution (2026-07-25)
**AUTHOR'S DECISION: "systematize everything, do the analysis, the conclusions, and take up the
fixing too".** The systematization of the 4 reviews is in engine_horizons_synthesis (AD-76/77/78);
here — the FIXING of the three defects exposed by Kimi THROUGH EXECUTION (AD-77). FIXING:
(1) HOMOGLYPH — a new notarius/homoglyph.py (a map of look-alikes Cyr./Gr.→Lat.,
deconfuse/confusables_in/mixed_script_words); diagnose gained the category
HOMOGLYPH_SUBSTITUTION (review=high): "admin"→"аdmin" is no longer CONTENT_CHANGED;
scan_hardened gives an ALARM homoglyph_mixed_script on MIXING of scripts within a word
(a purely single-language one does not alarm, verified "привет"→OK). (2) BACKDATING —
verify_trace gained the flag time_proven (True only if EVERY event has an external
anchor) + a candid line "TIME IS SELF-DECLARED": INTACT refers to the chain,
not to time (a time forgery without an anchor cannot be prevented — we made the boundary
explicit). (3) COSIGN FAIL-OPEN — verify_witnessed_trace on a failed quorum
NO LONGER returns INTACT: the status is downgraded to UNWITNESSED_HEAD (fail-closed),
the chain result is preserved in chain_status; an API consumer checking
status==INTACT now gets a candid negative. TESTS: tests/test_homoglyph.py
(7 checks) lock all three; 18/18 test files green; the demos (two_accounts/mail
selftest/handoff) work. The boundary is candid: the homoglyph map is not the whole TR#39.

### AD-80. Line-by-line audit of msl_mip → UTS#39 data + discipline taken (2026-07-25)
**AUTHOR'S DECISION: "do a line-by-line reading of rus1978rus/msl_mip, there are useful
things there on homoglyphs too, take what's needed, don't edit".** 3 parallel agents (read-
only) read through the project. MSL_MIP_AUDIT_2026-07-25_EN.md. THE MAIN CONCLUSION: NOTARIUS's
detection is ALREADY STRONGER (bidi/tag/VS/homoglyphs/fail-closed — the parent is weaker;
via the Vakhter port, the DNA of the same author). CANDIDLY ON HOMOGLYPHS: msl_mip has NO
working code (skeleton is paper; `paypаl.com` passes silently for them). TAKEN (data +
discipline, NOT code): (1) UTS#39 confusables.txt (Unicode 17.0.0, vendored in
msl_mip) → an ASCII-target subset derived, notarius/data/confusables_ascii.txt
= 1861 look-alikes (was ~50 manual, a ×37 jump); homoglyph.py rewritten to a real
skeleton() (NFD→replace→NFD); now Greek/fullwidth/mathematical/
ligatures are caught + the IDN-homograph paypаl.com (a failure for both before); provenance + the Unicode
license in the header. (2) The "no-auto-escalate" gate (their best asset) → the test
TestNoAutoEscalate: the layer is always advisory, no field blocks. LEFT BEHIND:
the card system, "homoglyph=a relation" (SIGN_RELATIONS), the pipeline scaffolding —
someone else's architecture/process. NOT TAKEN, but a CANDIDATE for the future under the finance vertical:
domain/URL awareness (public_suffix.py + _detect_context_at/_SCOPE_RISK —
"a look-alike in a domain = HIGH"). 19/19 test files green; msl_mip was NOT changed.

### AD-81. Domain/URL awareness: a look-alike/invisible char in a domain = HIGH (2026-07-25)
**AUTHOR'S DECISION: "take it on" (a candidate from the msl_mip audit AD-80).** The
IDEA (not the code) `_detect_context_at`/`_SCOPE_RISK` was ported: notarius/urlcontext.py — our own
lightweight implementation without a PSL. An invisible char/look-alike IN A DOMAIN (host) → HIGH (never
legitimate), in a path → MEDIUM; userinfo spoofing "brand@foreign-host" (paypal.com@evil.ru)
→ HIGH. Wired into scan_hardened: it overrides the general homoglyph_mixed_script
with a specific signature (homoglyph_in_host/invisible_in_host/userinfo_spoof), legitimate
URLs stay OK. It hits the reviewers' top vertical (BEC / substitution of a payment-detail link):
paypаl.com, goog‹ZWSP›le.com. tests/test_urlcontext.py — 7 checks. Boundary:
a "looks like a domain" heuristic, NOT a public-suffix check; advisory. The msl_mip code
was NOT copied. 20/20 test files green.

### AD-82. License reversal: proprietary "all rights reserved" (2026-07-25)
**AUTHOR'S DECISION: "insert this license, just adapt it to yourself"** (sent the text
of maximum restriction from msl_mip). The former dual AGPL+commercial
(AD-55/74) is LIFTED. LICENSE rewritten: NOTARIUS — PROPRIETARY, ALL RIGHTS RESERVED
(EN+RU): the repository is for VIEWING only, no rights are granted;
use/execution/copying/modification/distribution — only by written
permission; a platform-fork exception (grants no rights); no-contribution-grant;
no-warranty; a temporary license of maximum restriction. Adapted for NOTARIUS
(semantic tracing instead of "an alphabet of signs"). RECONCILIATION: deleted
LICENSING.md and COMMERCIAL-LICENSE.md (the dual artifacts); SPDX in all 28 .py
files changed AGPL-3.0-or-later → LicenseRef-Proprietary; README/NOTICE/pyproject
(license + the classifier Other/Proprietary) updated. A CAVEAT on third-party data:
notarius/data/confusables_ascii.txt remains under the Unicode License (UTS#39) — the
proprietary license does not extend to it. The code is not touched functionally.

### AD-83. The "layer vs plumbing" rule + a demo of localizing a link by the trace (2026-07-25)
**AUTHOR'S PRINCIPLE (a governing rule):** if a NEW way of SEALING at some stage/process of
semantic tracing ITSELF is born from the conclusions — that is a LAYER
(core). If OTHER known/used identification or security
measures are pulled in (DKIM, Received, TLS, PSL, someone else's MSL/Vakhter maps) — that is PLUMBING.
CONTEXT: the author caught that reading a letter's DKIM/Received headers = plumbing
(a door for one channel + others' signals), and returned the focus to the core. CONCLUSION: "where
the forgery happened" is answered by the engine with ITS OWN trace, not by the mail. Demo (pure core,
without plumbing): scripts/trace_localize_demo.py — a document carries our signed
trace from birth, passes through hands (Aktiv-Finance CREATED → TRANSFERRED → the Auditor
REVIEWED → the Fraudster appended a link with an amount substitution, signing with their own key).
verify_trace localizes: break_at_step=3 (the "Fraudster" link), the last intact one —
"the Auditor" (step 2), WHY (the key is not in the trusted set + the value changed at
TRANSFERRED, where it must be preserved). Channel-independent, without a single mail
line. The difference from the mail's "where" (a server, evidence, forgeable): our "where" is
WHOSE LINK of the chain (signed, a proof), in any channel, if the document
carried the trace from birth. time_proven=False candidly (self-declaration). I did not touch the core
code; the demo runs on the ready-made trace API. 20/20 test files green.

### AD-84. The seal of the VOID — a new sealing layer through tracing (2026-07-25)
**AUTHOR'S QUESTION: "can we seal empty places?".** YES — and by the AD-83 rule this is
a LAYER (a new way of sealing through tracing itself), not plumbing. Prototype:
scripts/void_clamp_demo.py. THE IDEA: an ordinary fingerprint catches a change of what
IS THERE; the seal of the void makes ABSENCE a signed assertion ("this slot is deliberately
empty, there are exactly this many slots"). brand_with_voids signs the slot structure with
an empty flag; verify_voids localizes BY the slot's NAME: SEALED_VOID_FILLED
(a sealed void was filled), NEW_SLOT (an unsealed one slipped in), MISSING_SLOT,
VALUE_CHANGED. RUN: the original (2 deliberately-empty slots) → intact;
a fraudster filled "an addendum" (+8m bonus) and slipped in "hidden_line" → the engine
named EXACTLY these two places (not a blind "diff"). It closes the attack class "insertion into
NOTHING" (appending a line, filling a box, adding a recipient/clause after
the signature). The seal's signature is Ed25519 (ours). A prototype-concept, NOT wired into the core
(the integration decision is the author's). The core is untouched; 19 test files green.

### AD-85. Legitimate progression of a document + a reader footnote-provenance (2026-07-25)
**AUTHOR'S IDEA:** a document/information can be not static but LEGITIMATELY
progressive; a legitimate addition layer is needed — the editor leaves THEIR OWN
semantic trace, and the reader, through the program, sees in a FOOTNOTE who/where/
when edited. By the AD-83 rule — a LAYER (sealing through tracing + rendering
the provenance for a human), not plumbing. Prototype: scripts/progressive_trace_demo.py.
THE MODEL: create (the basis, signed by the author) + a chain of signed EDIT events (each:
who/field/new-value/when, chained by prev_hash, Ed25519). rebuild = the basis + all
the SIGNED edits. footnotes() renders for the reader: "[created] Author 09:00; [edit]
field payment_due entered by the Lawyer 10:00; [edit] field amount entered by the Accountant 11:30".
audit() separates LEGITIMATE progression (a signed event by a trusted party) from
FORGERY (a change WITHOUT a signature): the run — 3 signed edits = CLEAN;
then amount 1050000→9000000 without an event → localized "field amount: NO SIGNATURE".
It closes the model: an edit is lawful ⇔ it left a trace; the trace is visible to a human via a footnote.
A prototype-concept, not wired into the core. The core is untouched; 19 test files green.

### AD-86. A field has its own KEEPER — a zone of responsibility at the field level (2026-07-25)
**AUTHOR'S IDEA: "the numbers had their own keeper".** A critical field (amount/detail)
has an assigned keeper: ONLY they may lawfully change it, even if the
editor is otherwise trusted. By AD-83 — a layer. Prototype: scripts/
field_keeper_demo.py. THE MODEL: the creator's seal fixes both the values and the KEEPER
MAP {field→keeper} (it cannot be reassigned on the fly). audit checks, for each
edit: editor == keepers[field] AND the key matches the keeper's key.
OUTCOMES: EDIT_BY_NON_KEEPER (a non-keeper edited the field — role forgery),
KEEPER_KEY_MISMATCH, UNSIGNED_CHANGE (a change without an event), CHAIN_BROKEN.
RUN: "amount" has the keeper the Treasurer; ① the Treasurer edits the amount + the Lawyer the due date →
CLEAN; ② the Manager edits the amount → EDIT_BY_NON_KEEPER (not the keeper of the numbers);
③ amount 1050000→9000000 without an event → UNSIGNED_CHANGE. This is the third sealing
layer (after the link AD-83, the void AD-84, the progression AD-85): the NUMBERS have
a personal guard. A prototype-concept, not wired into the core. The core is untouched.

### AD-87. Consolidating three prototypes into one core part: notarius/record.py (2026-07-25)
**AUTHOR'S DECISION: "let's not complicate the engine [with new layers]; with tests, so that
it is not four demos but one working core part. Assemble it".** Consolidated the
prototypes AD-84 (the void) + AD-85 (legitimate progression/footnote) + AD-86
(the field keeper) into ONE module notarius/record.py. API: create_record
(fixes the field values, the map {field→keeper}, the keepers' keys),
edit_field (a signed chain of edits), rebuild (the official state),
footnotes (a reader footnote who/where/when), audit (localization by field:
EDIT_BY_NON_KEEPER / KEEPER_KEY_MISMATCH / UNSIGNED_CHANGE / NEW_SLOT /
MISSING_SLOT / CHAIN_BROKEN / BAD_SIG), human_audit. It complements trace.py, it does not
duplicate it (there — the chain of an element's value; here — the field structure). tests/
test_record.py — 8 tests (legitimate progression / non-keeper / unsigned / a new slot /
filling a void with one's own and another's key / a chain break / the footnote). A single demo scripts/
record_demo.py; the three prototype demos (void_clamp/progressive_trace/field_keeper)
were DELETED (consolidated). The AD-83 link stays in trace.py as is. README extended.
20 test files green; trace.py/title.py/anchor.py untouched.

### AD-88. Testing the core on different substrates (substrate-independence) (2026-07-25)
**AUTHOR'S DECISION: "let's check how the core sits on other substrates, not just
text in correspondence".** scripts/carriers_demo.py: one governed set
(notarius.record), but the fields carry DIFFERENT substrates — amount (text), director's_
seal (a PNG image), audio_consent (a WAV sound), line_item_register (JSON
data); each with its own keeper. A field's value = the file's FINGERPRINT (sha256),
substrate-agnostic. RUN: the original → CLEAN; substituting the image (1 byte) →
UNSIGNED_CHANGE [director's_seal]; substituting the sound → both substrates localized
by field. CONCLUSION: the core governs image/sound/data/text with ONE machine (via
the fingerprint), FO-013 confirmed on concrete substrates. THE CANDID BOUNDARY (in
the demo and the code): we catch "the substrate was touched / by the wrong keeper", NOT "where inside
the image/sound" — for "where inside media" a separate media reader is needed (outside
the core, a raw-material candidate like the MSL/Vakhter maps for text). I did not touch the core code;
the demo runs on the ready-made record API. 20 test files green.

### AD-89. Architecture diagram: CORE + pluggable READERS + DOORS (2026-07-25)
**AUTHOR'S DECISION: "record the 'core + pluggable readers' picture as a separate
short diagram document".** ARCHITECTURE_CORE_AND_READERS_2026-07-25_EN.md —
a one-page ASCII diagram of three rings: (1) the CORE (ours, substrate-agnostic, on
the fingerprint: trace/record/title/anchor/cosign/frost/Ed25519 — whose link, the field
keeper, the footnote, native/inserted); (2) the substrate READERS (raw material, pluggable: text —
detect/canon/homoglyph/url + the MSL/Vakhter maps; media — a candidate; they answer "what is
inside the substrate"); (3) the DOORS (the buyer's integrations: mail/messenger/CRM/EDI).
Plus the governing rule AD-83 (layer vs plumbing) and the candid boundaries. It brings the
session's results together into one map: the engine at the center, plumbing and raw material at the edges.
No code; a record of the architecture.

### AD-90. Response to external audit #1: 2 already closed, 1 real gap (2026-07-26)
**EVENT:** the author sent the project for an external audit (an MSL/MIP reviewer, by the DOCS, without
code); sent finding #1 (#2 pending). The audit is friendly, the maturity rating
high. Three remarks were VERIFIED AGAINST THE CODE (the reviewer had no code): (A) NFC/hash
AD-4 — ALREADY correct: trace._value_hash = sha256(NFC(value)), order Raw→NFC→
JSON→hash→sign; AD-4 is closed for hash integrity, NFC does not touch invisible chars
(a separate axis) — clarified in the canon. (B) Sybil / the witness pool — ALREADY supported and
candidly noted: converge.trusted_sources / anchored source_ranks; only
the pre-established pool, dynamic ones do not count — clarified in the canon. (C) Silent
omission — THE REVIEWER IS RIGHT, a real gap: "periodic re-checking" does not catch
what did NOT happen without a schema of expected transitions (a state-machine contract); candidly
acknowledged, NOT implemented; by AD-83 — a new LAYER, a candidate. DECISION: A and B —
cheap clarifications of the canon (we described what the code already does); C — kept as
the real next layer, to build after audit #2 (close both at once). I did not touch the
code (clarifications only in SEMANTIC_TRACE_CANON). 20 test files green.

### AD-91. Response to external audit #2: 6 findings closed in code, 2 in docs (2026-07-26)
**EVENT:** finding #2 arrived (docx). Unlike #1, the reviewer RAN THE CODE (212
tests + 28 adversarial probes) and exposed REAL holes in the implementation, not in
the docs. Analyzed, reproduced each attack, fixed the priority ones, left a candid
list of the deferred.

**CLOSED IN CODE (with regression tests, tests/test_audit_fixes.py, 6 tests):**
- N-W1 — cli.py: the .ntr receipt was UNSIGNED. An attacker edited the file,
  recomputed the sha256 in the receipt → a false "✔ not touched". Now the receipt body is
  signed with a fresh Ed25519 key, and verify checks the signature FIRST: editing
  the receipt → "✘ RECEIPT FORGED" (rc=1). check stays stdlib (nacl lazily).
- N-W2 — custody.py: sign() did not check the integrity of the shares; a corrupt share silently
  gave a bad assembly. A VerifyKey self-check added → {ok:False,
  SHARE_CORRUPT} on a mismatch.
- N-W4 — trace.py: a foreign element_id with a valid signature in the middle of the chain
  passed (trace "A" silently continued as "B"). A continuity check of
  element_id against trace[0] added.
- N-W5 — trace.py: the chain could begin NOT with CREATED (the lifecycle §9).
  Step 0 must be CREATED, otherwise BROKEN.
- N-W6 — carrier.py: a deterministic nonce = sha256(issued_at:payload)
  rejected a LAWFUL re-issue of the same payload in the same second as ALREADY_USED
  (a self-DoS). Replaced with secrets.token_hex(16).
- N-W7 — record.py: the value of a forged (non-keeper) edit made it into
  official; a consumer reading only official got the forgery. Now
  official is assembled ONLY from edits that passed all checks.

**CLOSED IN DOCS (the boundary made explicit, requires no code):**
- N-W3 — cosign.py: the witness's fork protection is bound to (log_id, log_pub); a change
  of the log key starts a new record, so a fork "via rotation" is not caught. A deliberate
  compromise (only an external rotation registry can link key epochs) —
  documented in the _seen docstring.
- N-W16 — title.py: earliest in the converge sort is NOT a tie-break (equal
  sources → still contested). The docstring is corrected so it does not read as
  "earliness resolves a tie".

**CANDID DEBT (not fixed, recorded):**
- N-W8/N-W9 — balanced bidi, a homoglyph in a non-ASCII TLD: this is detector
  COVERAGE = raw material (the MSL/Vakhter maps), by AD-83 not the core.
- N-W10–N-W14 — robustness/exceptions on malformed input: not a priority.
- N-W18 — registries without a signature on the record itself: mitigated by cosign/OTS.
- Silent omission (a state-machine contract) — matches gap C of audit
  #1; the real next LAYER, held until the consolidation of both audits.

**DOC HONESTY:** along the way I corrected the stale test count "31" → 224 in 21
files (README, STATUS_AND_LIMITATIONS_NOTE) — the figure had lagged many sessions behind.

UPSHOT: 21 test files green (was 20 + the new test_audit_fixes.py). Code touched in
cli/custody/trace/carrier/record; docs — cosign/title/README/STATUS.

### AD-92. A new LAYER: the mandatory route — catching a skipped step (2026-07-26)
**AUTHOR'S DECISION: "assemble it and test for vulnerabilities with the new layer in mind".**
Built the one genuinely open gap of both audits (AD-90 "C" +
AD-91 "silent omission"): the trace chain proves that what is RECORDED is intact, but
does not see ABSENCE — a skipped step is not a forgery but a void, and the whole chain stays
silent about it.

**notarius/route.py** — reconciles the trace (trace.py) against a MANDATORY ROUTE
(the contract: ordered steps "type → responsible role"), localizes by step:
MISSING_STEP (a skip), WRONG_SIGNER (a step self-signed with the wrong key — a skip cannot
be slipped past by role forgery), OUT_OF_ORDER (order broken), UNKNOWN_ROLE (a contract
hole), CHAIN_BROKEN (the trace is broken → the route cannot be judged). Repeats =
a counter ("5 inspection rounds" = five items; did 2 → three MISSING_STEP).

By the AD-83 rule this is a LAYER, not plumbing: it is born from our semantic
tracing (checking role signatures + the order of events), it pulls in nothing external. Key point:
the contract (route + authorized_keys) is a TRUSTED policy input
from the customer, NOT from the presenter of the trace (otherwise they would declare an empty route) —
like trusted_keys.

**VULNERABILITY TEST (tests/test_route.py, 11 probes):** happy-path; skipping
a check → MISSING_STEP; self-signing with the wrong key → WRONG_SIGNER (the point being —
a skip is not bypassed by forgery); order violated → OUT_OF_ORDER; a broken
trace → CHAIN_BROKEN (fail closed); the inspection-round counter; noise/extra steps do not give
a false "incomplete"; tail truncation → incomplete (the safe side).

**A HOLE FOUND INDEPENDENTLY IN THE PROCESS AND CLOSED:** with verify_chain=False,
a genuinely signed step of ANOTHER object (a real warehouse check of a different
batch), spliced into the trace, read as completed. A continuity check of
element_id was added ALWAYS, regardless of the chain flag (N-W4 at the route
level); closed by a test in both modes.

**THE CANDID BOUNDARY (in the code and the doc):** a matched step proves that an AUTHORIZED party
signed "done", NOT that the action actually happened (SIGNED ≠ NATIVE, defect
#1) — the layer catches a SKIP and a ROLE SUBSTITUTION and localizes accountability, it does not judge
physical truth. Time is self-declared (the order of RECORDING, not the real time).

UPSHOT: 22 test files green. Code: the new notarius/route.py (the core is untouched).

### AD-93. A real working program: shared engine + local web app (2026-07-26)
**AUTHOR'S DECISION: "let's build a working program" — start free (CLI + local web).**
After the English port, presentation and Pages, the author asked for one actual
usable program on the engine (not more mockups), and — after a plain-language
cost breakdown — chose the free path: a command-line tool plus a local web app,
skipping the paid signed-.exe route until there is a concrete reason to
distribute to strangers.

Built:
- notarius/analyze.py — ONE shared analysis engine (analyze_documents /
  scan_document). Both `notarius check` (CLI) and the web app call it, so they
  can never drift. Returns structured findings: per-line category/review
  (value substitution / invisible char / homoglyph / loss / rewrite), a
  content scan (hidden invisibles), and look-alike-domain risks.
- notarius/webapp.py — a stdlib local web app (`python3 -m notarius web`, also
  `python3 -m notarius.webapp`). Serves a self-contained UI (paste or drop two
  documents → real verdict from the engine, plus a single-document scan tab).
  Binds to 127.0.0.1 ONLY — local, offline, no outbound calls, no telemetry;
  the compare/scan path is pure stdlib.
- cli.py refactored so `check` uses the shared engine (return codes unchanged);
  added the `web` subcommand and help.
- tests/test_analyze.py (6) + tests/test_webapp.py (5, a real ephemeral-port
  server hit over HTTP). Suite: 24 files, 246 tests, all green.
- docs/assets/notarius_app.png — screenshot of the running app, in the README.

BOUNDARY (kept): the app shows WHERE and WHAT changed and flags hidden
manipulation; it does not judge intent (TRACE_LOCATES_THE_LIE ≠
TRACE_PROVES_THE_TRUTH). Privacy is structural: localhost-only bind.

COST: $0. Paid options (code-signing ~$100–500/yr for a no-Python installer, or
hosting for a public URL) are deferred until a real distribution need appears.

---

Recorded by: Claude (Anthropic), sessions 2026-07-21/22/23/24/25/26, per the author's responses.
