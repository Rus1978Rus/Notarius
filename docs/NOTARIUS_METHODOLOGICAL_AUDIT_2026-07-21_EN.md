# NOTARIUS — Methodological audit (line-by-line review)

AUDIT_DATE: 2026-07-21
AUDITED_DOCUMENT: `docs/NOTARIUS_FULL_SESSION.md` (version 2026-07-20)
AUTHOR OF PROJECT: Ruslan Malyavskiy
AUDITOR: Claude (Anthropic), session 2026-07-21
STATUS OF AUDIT: WORKING DOCUMENT — accepted for follow-up ("taken into work")

Verdict markers used for each claim:

- ✅ **CORRECT** — the claim holds up as currently worded.
- ⚠️ **OVERCLAIM** — the core is right, but the wording promises more than is proven.
- ❌ **WRONG** — the claim is factually mistaken and needs correcting.
- 🔬 **NOT VERIFIED** — the claim is testable, but no check was run.
- 📌 **NEEDS DEFINITION** — a term/mechanism is used but defined nowhere.

---

## SUMMARY VERDICT

The document has a **workable conceptual core** (separating container integrity
from element provenance) and a **systematic methodological discipline**
(statuses, honest scope boundaries, a property-fixing pipeline) — strengths that
are rare in early-stage documents.

There are three critical problems, and they recur throughout the text:

1. **Self-attestation.** Almost all of the document's defensive mechanisms
   (control length, manifest, typing) are stored next to the very data they
   protect, and are not bound to a secret or a signature. An attacker who can
   change the data can change the "witness" too. Without a trusted anchor
   (key/signature/external log), no property is a barrier — only a diagnostic.
2. **Obfuscation counted as protection.** Sections 6.1 and 6.2 record the
   opacity of structure/schema/semantics as "barriers." This violates
   Kerckhoffs's principle: a system's strength must not rest on the secrecy of
   its design. The document itself acknowledges this principle in section 8
   ("Is Kerckhoffs removed or relocated?") but does not apply it to sections
   6.1–6.2 — an internal contradiction.
3. **The niche check is incomplete.** The NICHE_CONFIRMED verdict is issued
   without considering the closest existing analogues: C2PA / Content
   Credentials (per-component provenance of media, built into the pipeline),
   in-toto / SLSA / Sigstore (signed provenance chains for artifacts),
   Certificate Transparency (logs with provable continuity), W3C PROV-O (a
   provenance ontology). The niche may exist, but in a narrower formulation than
   claimed.

Recommended project status (unchanged from the previous audit):

```
RESEARCH_HYPOTHESIS
ARCHITECTURE_DRAFT
NOT_SECURITY_VALIDATED
PROTOTYPE_IN_PROGRESS   ← updated: first code in this repository
PRIOR_ART_REVIEW_REQUIRED
```

---

## LINE-BY-LINE BREAKDOWN BY SECTION

### Header (lines 1–5)

- "COMMERCIAL USE PROHIBITED" — ⚠️ legally, a declaration with no chosen license
  has no clear force. If the goal is to protect authorship and prohibit
  commercial use, a specific license must be chosen (e.g. CC BY-NC 4.0 for text;
  for code — a separate decision, since CC is not recommended for code).
- "STATUS: WORKING DOCUMENT" — ✅ honest.

### §1. Definition (lines 9–17)

- "Notarius — a provenance tracker for data elements" — ✅ as a statement of a
  hypothesis. 📌 Not defined: what an "element" is (a field? a character? a
  block? a byte range?), who creates a provenance record and on what basis, who
  trusts it.
- The formula `ORIGIN + TRACE + CURRENT_STATE` — ✅ as a frame. 📌 CURRENT_STATE
  is not derivable from ORIGIN+TRACE without transition rules (see §9).

### §2. Origin of the project (lines 21–34)

- The quote "If the problem were cryptographic, it would have been solved many
  decades ago" — ⚠️ rhetorically strong, factually imprecise. Cryptography has
  long dealt with provenance specifically: signed audit logs, transparency logs,
  attestation schemes (in-toto), timestamping (RFC 3161). The correct boundary is
  different: cryptography provides the **mechanisms**, while Notarius offers a
  **semantic model and policy** on top of them. That is both more honest and
  stronger as positioning.
- `INTEGRITY_LAYER ≠ PROVENANCE_LAYER` — ✅ a correct and valuable distinction.
  This is the core of the project.

### §3. The project vertical (lines 38–54)

- MSL/MIP → Notarius → SSP — ✅ as a roadmap. 🔬 None of the three steps has
  reached a prototype; the vertical is so far declarative. "The question shared
  by all three" is well put.

### §4. Difference from cryptography (lines 58–73)

- The table — ⚠️ the "Cryptography" column describes only primitives (signature,
  hash), ignoring cryptographic **protocols** for provenance (see §2). The table
  is right against "naïve cryptography" but not against the real state of the
  field.
- `SIGNED ≠ NATIVE` — ✅ a strong formula, keep it.
- `HASH_VALID ≠ CLEAN_ELEMENT` — ✅ correct (a container hash does not localize
  a change to an element).
- `TRACE_EXISTS ≠ TRACE_CONTINUOUS` — ✅ correct and important.

### §5. What Notarius does NOT do (lines 77–89)

- ✅ An entirely correct section. `VALIDATOR ≠ COURT`, `TRACE ≠ PROOF` — the
  right self-discipline, keep verbatim.

### §6.1 SEMANTIC_MANIFEST_KEY (lines 95–113)

- "STATUS: FIXED" — ❌ premature. The property has passed neither a threat model
  nor a prototype. By the document's own discipline (§6.3 requires a pipeline for
  a candidate), fixing it without the pipeline violates its own rules.
  Recommendation: downgrade to PROPERTY_CANDIDATE.
- "WITHOUT THE KEY: blocks exist, meaning unclear (semantic obfuscation)" — ❌ as
  a security barrier. Obfuscation is not protection: against statistical
  analysis, known field formats (IBAN, amounts, dates), and partial knowledge the
  structure is recoverable. The term "obfuscation" in the text is honest — but
  then the property cannot be counted as a defensive layer in §6.2.
- "DIFFERENCE FROM BLOCKCHAIN" — ⚠️ it is true that blockchain does not carry the
  block's semantics, but the comparison is incomplete: blockchain provides what
  Notarius lacks — provable immutability of history. The honest formula: Notarius
  adds semantics but must get its immutability from somewhere (a signature, a log).

### §6.2 SEMANTIC_LAYERED_DEFENSE (lines 115–135)

- "FOUR INDEPENDENT BARRIERS" — ❌ independence is not shown. Barriers 2–4
  (schema, typing, order) are knowledge of how the system is built, i.e. the same
  kind of secret. By Kerckhoffs they cannot be counted as barriers: for a serious
  attacker the design of the system is assumed known. There is really one
  independent barrier here — the key.
- "Even a weak password + unknown semantic structure = meaningless mush" — ❌ a
  dangerous conclusion: it justifies a weak password. This is a direct path to
  insecure operation. Remove or invert it: "an unknown structure does NOT
  compensate for a weak key."
- Recommendation: rename the property from "defense" to
  SEMANTIC_STRUCTURE_OPACITY and classify it as a **privacy / analysis-hindrance**
  property, not a security one.

### §6.3 SEMANTIC_INVISIBLE_LENGTH_WITNESS (lines 137–173)

The central section — a detailed breakdown.

- "STATUS: PROPERTY_CANDIDATE → requires a pipeline" — ✅ discipline observed,
  the status is honest.
- "Any insertion/deletion… changes the counter and breaks the check" — ⚠️ true
  ONLY on the condition that the counter is stored where the attacker cannot
  reach it. In the prototype the counter lives in the same dict as the data: the
  attacker changes `data` and `cp_len` in one move, and the check passes.
  **Proven by code in this repository**: `tests/test_witness.py::
  test_naive_witness_bypassed_by_updating_cp_len`.
- "CATCHES: ZWSP/ZWJ/VS16/BOM… at the start/end/middle" — ✅ confirmed by tests
  (`test_zwsp_*`). Against **accidental** corruption and **unaware** tampering,
  it works.
- A missed case in the "DOES NOT CATCH" list: **insertion + deletion preserving
  the counter** (replace a visible character with an invisible one, same length).
  Confirmed by test `test_insert_plus_delete_preserves_length`. Add it to the
  scope boundary.
- "NFKC/NFD normalization does not remove them — verified" — ⚠️ partly. For ZWSP
  (U+200B) and ZWJ (U+200D) — true. But NFKC expands ligatures and compatibility
  forms (ﬁ → fi: 1 code point → 2), CHANGING the counter with no tampering at all.
  The flip side matters more: **legitimate** normalization in the pipeline (NFC at
  one intermediary) changes the code-point count for composed characters (é = 1
  code point in NFC vs 2 in NFD) → **false positive**. Conclusion: the spec must
  fix the normal form (recommendation: NFC on input, before counting) — otherwise
  the barrier is noisy.
- "Three lines. No dependencies." — ✅ as demonstration value; ❌ as "the first
  working Notarius code" in a defensive sense. Code defects: (1) self-attestation
  — see above; (2) KeyError on missing keys; (3) no type checks (`cp_len="5"`
  gives False silently, `data=None` gives TypeError).
- VERDICT ON THE PROPERTY: reclassify as **DECLARED_CODEPOINT_COUNT — a
  diagnostic field inside a signed manifest**. In that role it is meaningful:
  cheap, human-explainable ("length changed from 12 to 13"), it localizes the
  kind of tampering that a hash only asserts. As a standalone barrier — no.

### §7. FO-candidate MANIPULATION_LEAVES_SUBSTRATE_TRACE (lines 179–217)

- The idea "the substrate itself records tampering" — ✅ a productive frame.
- CASE_1 punch card: "you can't patch a hole unnoticed" — ⚠️ against a cursory
  glance — yes; against a motivated attacker — no: forging/repunching cards and
  swapping decks have happened historically. The detector is not the card but the
  reconciliation procedure (deck checksums).
- CASE_2 film: "a splice is visible" — ⚠️ retouching and montage have existed
  throughout the history of photography; expertise was always required.
- CASE_3 wax seal: "opening destroys the seal" — ⚠️ forging seals is a craft with
  a thousand-year history.
- CASE_4 Notarius — ❌ the key difference is hidden by the analogy: for the punch
  card, film, and wax seal, the substrate is **physical**, and copying/swapping is
  expensive. A digital "substrate" is copied for free and indistinguishably. The
  digital analogue of "the substrate remembers" is signed append-only logs (Merkle
  trees, transparency logs), and this must be acknowledged as prior art, not
  reinvented.
- `MANIPULATION_VISIBLE ≠ MANIPULATION_PREVENTED` — ✅ correct.

### §8. PROVENANCE_CARRIER (lines 223–257)

- The CANDIDATE_REGISTERED status without a pipeline — ✅ discipline observed.
- Dropping QR-as-transport and rethinking it as "an exit at the system boundary"
  — ✅ an architecturally mature decision.
- "Capacity ~3KB is small for traces" — ✅ factually correct (QR v40 byte mode
  ≈ 2953 bytes).
- The "open triangle" with the question about Kerckhoffs — ✅ the right questions.
  ❌ But a contradiction: here Kerckhoffs is acknowledged as a problem, while in
  §6.1–6.2 the secrecy of structure is counted as defense. It's one or the other.
  The audit recommends: Kerckhoffs applies everywhere.
- "You can't print a routing sheet that doesn't yet exist" — ✅ a correct
  ordering of dependencies.

### §9. The element state model (lines 263–291)

- The set of states (INTACT…RECOVERED) — 📌 states are listed but not defined:
  no assignment criteria, no matrix of allowed transitions, no answer to "who is
  entitled to change the state." Without this the validator is not implementable.
- `MODIFICATION_WINDOW: 14:35–14:42` — 📌 requires trusted time. A node's clock
  is forged along with the data. You need external timestamping (RFC 3161 / a log)
  — otherwise the window is unprovable.
- The formulas `PROVENANCE ≠ CURRENT_STATE`, `TRACE_BREAK_TIME ≠
  EXACT_ATTACK_TIME` — ✅ honest limits, keep them.

### §10. Tracing levels (lines 297–314)

- Three levels + `TRACE_DEPTH_FOLLOWS_RISK` — ✅ a sensible design principle.
- `MORE_TRACE ≠ MORE_TRUTH` / `= MORE_OBSERVABILITY` — ✅ correct.
- 🔬 The cost of the levels is never estimated (metadata volume per element,
  pipeline overhead). For TRACE_LEVEL_3 (per character) the cost may exceed the
  payload by orders of magnitude — this has to be computed before the level goes
  into the spec.

### §11. Forensics (lines 318–332)

- "here is the chain of provenance with a break at step 3" — ✅ as a value
  proposition. ⚠️ But for a court the chain is probative only if the chain itself
  is authenticated (node signatures, admissibility under the rules of procedural
  law). A Notarius record without a cryptographic anchor is, for a court, the same
  "I think," just structured.
- The adoption model "banks introduced standards through pain" — ✅ as an
  observation; 🔬 as a strategy, not verifiable in advance. The sound part: "the
  product must exist and be ready." (The real entry, per the 2026-07-21 discussion
  — small business, not banks.)

### §12. Asset tracking (lines 336–354)

- ⚠️ The section describes desired behavior ("Notarius sees"), not a mechanism.
  To "see" fragments of one provenance across accounts/wallets/papers requires the
  cooperation of every intermediate system — this is the strongest assumption in
  the whole document, and it is not flagged as an assumption.
- Prior art not considered: blockchain-transaction analysis (Chainalysis and the
  like) does exactly "SPLIT_ASSET ≠ LOST_PROVENANCE" within the bounds of public
  ledgers.
- The formulas by themselves (`UNREACHABLE ≠ UNTRACEABLE` and others) — ✅ as
  postulates of the goal.

### §13. The banknote analogy (lines 358–375)

- "The identifier must be embedded in the element, not just in the container" —
  ✅ the document's best architectural conclusion; it directly yields a format
  requirement: a provenance mark at the field level.
- ⚠️ Limit of the analogy: a banknote's serial number is backed by the physical
  unforgeability of the carrier; a digital ID without a signature is copied along
  with the element. The conclusion holds, but only paired with a signature.

### §14. The punch card analogy (lines 379–398)

- "Impossible to forge: the hole is either there or not" — ❌ factually wrong
  (see §7) and internally contradicts §7, where the same card is described more
  weakly ("can't patch a hole unnoticed"). Two places — two different levels of
  claim about one object. Bring both to the weak (honest) form.
- `COMPLEXITY ≠ SECURITY`, `SIMPLICITY = VERIFIABILITY` — ⚠️ the first formula is
  correct; the second is a heuristic, not an identity (something simple can be
  simply verifiable and also simply bypassable — the §6.3 prototype is proof).

### §15. Niche check (lines 402–418)

- "WHAT DOES NOT EXIST" — ❌ does not hold up in the claimed generality:
  - C2PA / Content Credentials — per-component provenance metadata (media) built
    into the creation/editing pipeline — an industry standard, working in real
    time.
  - in-toto / SLSA — a provenance chain for artifacts with signatures at every
    step, "built into the CI/CD pipeline."
  - ISO 20022 itself carries structured fields, and bank anti-fraud systems detect
    anomalous insertions in the pipeline.
- What really does look like open space (narrow the verdict): **element
  provenance for arbitrary small-business documents, outside media and outside
  CI/CD, with a human-readable break report**. Replace the verdict with:
  `NICHE_NARROWED / PRIOR_ART_REVIEW_REQUIRED`.
- 🔬 The claim about "$1.36 billion after the Panama Papers" (from the session
  transcript) — the order of magnitude matches public data from the ICIJ (>$1.3
  billion by 2021), but include it in a working document only with a precise
  citation and year.

### §16. First prototype, the plan (lines 422–453)

- The demo scenario (origin tag → insertion without a tag → detection) — ✅ as a
  teaching demonstration.
- ❌ A hole in the detection logic: the demo catches an insertion **without a
  tag** (`origin = UNKNOWN`). An attacker who knows the format will insert a
  forgery **with a tag** (`origin = invoice_458` copied from the neighboring
  field) — and the demo stays silent. Detection must check not the presence of a
  tag but its **cryptographic binding** to the field and to the chain of events.
- The expected output `TRACE_BREAK_DETECTED / NEEDS_REVIEW` (not an auto-block) —
  ✅ the correct advisory mode.

### §17. Current priority (lines 459–475)

- ✅ Internally consistent. ⚠️ The one thing: the ordering "MSL/MIP core first"
  conflicts with the 2026-07-21 session decision to go into small business via a
  Notarius document validator. The priority must be re-affirmed explicitly
  (AUTHOR_DECISION).

### §18. Canonical phrases (lines 481–498)

- "Cryptography checks the integrity of the container" — ⚠️ imprecise
  (cryptography can sign both elements and events); the phrase canonizes the §4
  error. Replace with: "A container's signature does not check the provenance of
  the element."
- "Notarius makes the asset's provenance hard to erase" — 🔬 a goal, not a
  property; the mechanism is not built.
- "Not every byte. Not just the whole file. But chunk + boundary" — ✅ a good
  working formula for the granularity level.
- "PRIMITIVE = RELIABLE = AUDITABLE" — ❌ as an identity. The §6.3 prototype is
  primitive, auditable — and bypassed in one line. The honest form: "PRIMITIVE IS
  EASIER TO AUDIT; reliability is proven separately."

---

## REGISTER OF INTERNAL CONTRADICTIONS

| # | Where | Contradiction |
|---|-----|--------------|
| 1 | §6.1–6.2 vs §8 | Secrecy of structure counted as a barrier, but in §8 Kerckhoffs is acknowledged as an open problem |
| 2 | §7 vs §14 | Punch card: "can't patch a hole unnoticed" vs "impossible to forge" |
| 3 | §6.1 "FIXED" vs §6.3 "requires a pipeline" | Different requirements for fixing properties; the pipeline applied to some but not all |
| 4 | §17 vs the 2026-07-21 session | Priority MSL/MIP vs the decision to go into small business via Notarius |
| 5 | §5 "Notarius ≠ proof of truth" vs §11 | In §11 the trace is presented as a court argument without the caveat about authenticating the trace itself |

---

## WHAT IS CONFIRMED BY CODE (this repository)

Prototype: `notarius/witness.py`, tests: `tests/test_witness.py`.

Catches (positive tests):
- ZWSP/ZWJ/VS16/BOM at start / middle / end → LENGTH_MISMATCH ✅

Does not catch — and this is now fixed by executable negative tests, not only
words:
- attacker updates `cp_len` together with `data` → the naïve check passes;
- equal-length substitution `1000 → 2000` → passes;
- inserting an invisible + deleting a visible (length preserved) → passes.

The fixed path (in the same file, stdlib-only): `SignedEnvelope` — canonical JSON
+ SHA-256 + HMAC signature. The same three attacks against the signed envelope →
detected (`SIGNATURE_INVALID` / `CONTENT_CHANGED`). The control length is kept as
a diagnostic field: on a mismatch the report says not only "changed" but also
"length changed by N code points" — localizing the kind of tampering the property
was meant for.

---

## AUTHOR'S DECISIONS (AUTHOR_DECISION — taken 2026-07-21)

Full log: `docs/AUTHOR_DECISIONS.md`. Outcomes:

1. §6.1 SEMANTIC_MANIFEST_KEY — **ACCEPTED**: downgraded to PROPERTY_CANDIDATE
   (AD-1).
2. §6.2 SEMANTIC_LAYERED_DEFENSE — **TO THE PIPELINE**: classification is decided
   by design-review; until it passes — PROPERTY_CANDIDATE / NEEDS_CONVEYOR; the
   audit's objections are the pipeline's input (AD-2).
3. §6.3 — **ACCEPTED**: renamed to DECLARED_CODEPOINT_COUNT, status
   DIAGNOSTIC_METADATA (AD-3).
4. Unicode normal form — **DEFERRED** until the threat model; in the prototype
   NFC remains an implementation choice (AD-4).
5. The §15 verdict — **FROZEN**: first a review of the analogues (C2PA,
   in-toto/SLSA, Sigstore, RFC 3161, W3C PROV), then a decision (AD-5).
6. The §17 priority — **UNCHANGED**: ACTIVE_FRONT = MSL/MIP; Notarius PARKED,
   background work (AD-6).
7. License — **DEFERRED** until the first publication/pilot (AD-7).

---

## THE HONEST TRAJECTORY (unchanged)

```
INTUITION → HYPOTHESIS → THREAT MODEL → FORMAL INVARIANTS
→ MINIMAL PROTOTYPE → NEGATIVE TESTS → COMPARISON WITH ANALOGUES
→ CONFIRMED PROPERTY
```

The project's current position on the trajectory: **MINIMAL PROTOTYPE + NEGATIVE
TESTS** (this repository). The next step — a threat model for the "small
business: critical document fields" scenario and a comparison with the analogues
from decision item 5.
