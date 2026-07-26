# Foundation Layer — methodological analysis and cross-transfer into Notarius

DATE: 2026-07-22
SOURCE: FOUNDATION_LAYER_STRUCTURED_2026_06_05.zip (the MSL/MIP project,
author Ruslan Malyavskiy), stored in docs/foundation_layer/
METHOD: line-by-line read + check against the Notarius catalog of 7 defects +
a cross-transfer section (what is applicable to the current Notarius core)

## 0. What this package is

Foundation Layer is a registry of "fundamental observations" (FO-001…FO-046)
of the parent MSL/MIP project: 46 observations about how systems
assign status, verify it, and get it wrong. Plus a collection of formulas
(FF), external methodological parallels (law, aviation, science),
a Kimi screening, and prioritization layers. Notarius in this ecosystem is
one of the branches (see 07_ARCHITECTURE/ECOSYSTEM_MAP).

Overall discipline rating: **very high and compatible with Notarius**.
The registry is itself built on the same principles we applied these two
days: `REVIEWED ≠ VALIDATED`, honest statuses, a boundary on each property,
a ban on overclaim, an open registry with entry discipline. This is not raw
material — it is a mature methodological frame.

## 1. Direct kinship with Notarius (one root)

Notarius and Foundation Layer grow from a common trunk. The overlaps are not
analogies — they are the same thought in different places:

| Foundation Layer | Notarius |
|---|---|
| FO-001 FORM ≠ STATUS | SIGNED ≠ NATIVE |
| FO-002 CLAIM ≠ PROOF | TRACE ≠ PROOF (§5) |
| FO-003 RECOGNITION ≠ TRUST | HASH_VALID ≠ CLEAN_ELEMENT |
| FO-004 REVIEW ≠ VALIDATION | discipline of the applications conveyor |
| FO-015 EVIDENCE_ADMISSIBILITY_LAYER: DATA→CLAIM→STATUS→TRUST→ACTION | element provenance chain |
| FO-016 PROVENANCE_PATH ≠ VISIBLE_CARRIER | the Notarius core, verbatim |
| FO-046 HEAD ≠ SOURCE / UNEXPLAINED_PATCH ≠ VALID_PATCH | requirement of traceable provenance (AD-6 traceability) |

**Conclusion:** AD-10 from Notarius ("a signed lie remains a lie, but
stops being anonymous") is a direct continuation of the line FO-001 →
FO-015. Foundation Layer gives Notarius the missing top layer:
a formal model of WHAT exactly the provenance chain verifies
(the transition CLAIM → STATUS in FO-015).

## 2. What is acceptable and useful to transfer into Notarius

Three things pass our own filter and strengthen the project:

### 2.1 FO-015 as the frame of the Notarius chain (adopt)
`DATA → CLAIM → STATUS → TRUST → ACTION` — these are exactly the transitions on
which Notarius localizes the break. Our report statuses (VERIFIED /
SIGNATURE_INVALID / CONTENT_CHANGED / LENGTH_MISMATCH) are detectors of a
classification error on the DATA → CLAIM transition. Foundation Layer
shows that above there are three more transitions that Notarius does not yet
touch (STATUS → TRUST → ACTION) — an honest map of where the prototype's
coverage ends.

### 2.2 FO-035 CONCRETE_OBJECT_QUESTION_TEST (adopt as a method)
"You own the object → you can test the theory." This is the same method that
gave us the exp_6_2 experiment: instead of arguing about §6.2 — a concrete object
(a shuffled IBAN) and the question "does the type recover?" The 100% answer
closed the discussion. FO-035 formalizes what we did intuitively.
→ Worth entering into the Notarius discipline as a mandatory step before
classifying a property.

### 2.3 FO-018 RITUAL_COMPLIANCE ≠ CAUSAL_MECHANISM (adopt as a guard)
Anti-cargo-cult: the right format ≠ a working artifact. This is direct
protection against the risk that the vendors' ideas nearly fell into: a beautiful
signature over an empty mechanism. Our catalog of 7 defects is a special
case of FO-018.

## 3. What passes with a caveat (transfer under a boundary)

- **FF-001 CONFIDENCE_WITHIN_SYSTEM ≠ CORRESPONDENCE_WITH_REALITY** —
  the strongest formula in the package, an exact twin of our SIGNED ≠ TRUE
  (AD-10). Adopt as a shared formula of both projects. It passed the triad
  of reviewers (phlogiston/ether/eugenics as examples).
- **FO-037 PROCESS_OVER_TIME_PRINCIPLE** — "validation depth =
  a function of process quality, not of time." This matches what we
  did: 40 ideas checked in hours through the conveyor, rather than months
  of development. Adopt.
- **FO-013 substrate-independence** — the permission to transfer observations
  between domains. It is precisely this that legitimizes our cross-transfer of Gemini's
  point (BOM in a token → invisible-character scanner). Useful as an explicit basis.

## 4. What NOT to transfer into Notarius (honest boundary)

- **FO-038…FO-044** (sacred status, identity, layering under
  pressure, Marranos/Pomaks) — politically and historically loaded
  observations. The registry itself correctly keeps them in LAYER_3/DEFERRED with
  a hard guard `STRUCTURAL_PATTERN_ONLY / NOT_MORAL_JUDGMENT`. For
  Notarius (a technical provenance tool) they are out of scope — do not
  drag them into code and product documents. The registry itself prescribes this.
- **FO-039 DEEP_PATTERN_FORMATION / FO-040 STATUS_SYSTEMS_CONVERGENCE**
  — the registry honestly marks them `NOT_GENERAL_THEORY / DO_NOT_SPIN_OFF_YET`.
  Observe this: do not turn Notarius into an illustration of a "general theory
  of statuses" — that would weaken both projects (the risk INTERESTING_IDEA ≠
  WORKING_TOOL, which FO-039 names itself).

## 5. Checking the package against the Notarius catalog of 7 defects

The registry on the whole does NOT contain the defects — on the contrary, it
independently describes many of them:
- defect №1 (self-attestation) ↔ FO-038 ABSENCE_OF_RESISTANCE ≠ CONSENT;
- defect №6 (reduction to a diff) ↔ FF-002 PROCESS_EVIDENCE_ONLY ≠ VALIDATION;
- defect №2 (symmetry/trust) ↔ FO-003 RECOGNITION ≠ TRUST.

The single methodological remark on the package (not a defect, but a growth point):
**FF-003 MULTI_MODEL_REVIEW ≠ ADVERSARIAL_PROCESS** — the registry itself
honestly records that several LLM reviews do not amount to genuine mutual
contestation (models are motivated to agree). Our applications
conveyor is a partial closure of this gap: the judges got an EXPLICIT
instruction to refute (skeptic lenses), not "evaluate." This is a concrete
strengthening that Notarius can return to the parent project:
**adversarial-by-instruction instead of consensus-by-default.**

## 6. Summary (input for AUTHOR_DECISION AD-12)

Foundation Layer is not raw material but a mature frame from which Notarius already
implicitly grows. Useful and acceptable to transfer: FO-015 (chain frame),
FO-035 (concrete-object method), FO-018 (anti-cargo-cult guard),
FF-001 and FO-037 (twin formulas of AD-10). Do NOT transfer:
the humanities-political layer FO-038…044 and the claim to a general theory
(FO-039/040) — the registry itself prescribes this. Notarius's return
contribution to the parent project: adversarial-by-instruction as an answer to
the recorded gap FF-003.

The decision on actual integration (entering FO-015/035/018 into the Notarius
discipline) is the author's.
