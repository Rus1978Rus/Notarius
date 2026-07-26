# NOTARIUS — Project discipline (Foundation Layer integration)

DATE: 2026-07-22
BASIS: AUTHOR_DECISION AD-12 — integrating FO-015, FO-035, FO-018 from the
parent MSL/MIP Foundation Layer project into Notarius discipline.
SOURCE: docs/foundation_layer/, analysis — FOUNDATION_LAYER_ANALYSIS_2026-07-22_EN.md
STATUS: working project discipline (not a standard, open to patches — modeled on
the parent project's REGISTRY_GOVERNANCE_POLICY)

The three ported elements are not decoration but working tools. Below, each with
its formula, its role in Notarius, and its mandatory application.

---

## D-1. The chain skeleton: FO-015 EVIDENCE_ADMISSIBILITY_LAYER

FORMULA:
```
DATA → CLAIM → STATUS → TRUST → ACTION
At every transition a classification error is possible.
```

ROLE IN NOTARIUS. This is a map of WHAT exactly the provenance chain checks. The
Notarius prototype today closes only the first transition:

```
DATA ──(Notarius verify)──> CLAIM      ← the prototype is here
       SIGNATURE_INVALID / CONTENT_CHANGED / LENGTH_MISMATCH
CLAIM ─────────────────────> STATUS    ← out of the prototype's scope
STATUS ────────────────────> TRUST     ← out of scope (needs PKI/identity)
TRUST ─────────────────────> ACTION    ← out of scope (the recipient's policy)
```

MANDATORY APPLICATION. Any claim that "Notarius checks X" must state at WHICH
transition of the chain it operates. The prototype honestly lives on DATA →
CLAIM; the transitions STATUS → TRUST → ACTION require external mechanisms (key
identity, trusted time, policy). This is a built-in scope boundary, not a
shortcoming.

CONNECTION: AD-10 (TRACE_LOCATES_THE_LIE) — localizing the lie is precisely
pointing to the transition where the chain broke.

---

## D-2. Method for checking a property: FO-035 CONCRETE_OBJECT_QUESTION_TEST

FORMULA:
```
YOU OWN THE OBJECT → YOU CAN TEST THE THEORY
OWNING THE OBJECT ≠ OWNING THE TERM
FAIL_TO_ANSWER_CONCRETE_OBJECT = DIAGNOSTIC_SIGNAL (not an automatic refutation)
```

ROLE IN NOTARIUS. This is a method we already used implicitly; now it is
mandatory. Precedents in the project:
- §6.3 length-witness: instead of arguing — a concrete block with a ZWSP and the
  question "does it catch it?" → tests/test_witness.py → requalified as a
  diagnostic (AD-3).
- §6.2 structure-opacity: instead of arguing — a shuffled IBAN and the question
  "is the type recoverable?" → exp_6_2_reassembly.py → 100% → reclassified as
  privacy/obscurity (AD-11).

MANDATORY APPLICATION. A Notarius property/barrier does NOT change status (up or
down) without running through a concrete object: an executable test or an
experiment on a real value. A beautiful formula that did not withstand a concrete
case is not promoted. If a property "escapes into terms" instead of contacting
the object — that is a warning signal (by FO-035, not yet a verdict: incompleteness
is possible, the object may be out of scope, a different level may be needed).

RULE: any AUTHOR_DECISION about a property's status references a concrete
object-check (a test/experiment file), like AD-3 and AD-11.

---

## D-3. Anti-cargo-cult guard: FO-018 RITUAL_COMPLIANCE ≠ CAUSAL_MECHANISM

FORMULA:
```
FORM_OF_SUCCESS ≠ CAUSE_OF_SUCCESS
CORRECT_FORMAT ≠ WORKING_ARTIFACT
```

ROLE IN NOTARIUS. A direct defense against the risk the vendor ideas kept hitting
in the applications pipeline: a correct signature, a correct manifest format, a
correct report — on top of a mechanism that proves nothing. Our catalog of 7
structural defects is an operational special case of FO-018 (each defect = a
place where the form diverges from the causal mechanism).

MANDATORY APPLICATION. Before calling anything a "barrier" or "defense," ask the
FO-018 question: does the artifact reproduce the causal mechanism, or only its
form? Concretely for Notarius — run it through the catalog of 7 defects
(FINAL_APPLICATIONS_REPORT_2026-07-22_EN.md): self-attestation, key symmetry,
SIGNED ≠ NATIVE, cold start, pipeline normalization, reduction to a diff, mortality
of marks.

---

## What is deliberately NOT brought in (the integration boundary)

From the Foundation Layer, the following are NOT ported into Notarius discipline:
- **FO-038…FO-044** — the humanitarian/political layer (sacred status, identity,
  layering under pressure). Out of scope for a technical provenance tool; the
  parent registry itself keeps them in LAYER_3/DEFERRED under the guard
  `STRUCTURAL_PATTERN_ONLY`.
- **FO-039 / FO-040** — a claim to a general theory of statuses. The registry
  marks it `NOT_GENERAL_THEORY / DO_NOT_SPIN_OFF_YET`. Notarius does not become an
  illustration of a general theory — that would weaken both projects
  (INTERESTING_IDEA ≠ WORKING_TOOL).

## Notarius's reverse contribution to the parent project

The recorded gap **FF-003** (`MULTI_MODEL_REVIEW ≠ ADVERSARIAL_PROCESS` —
several LLM reviews do not constitute contestation, the models agree) is
partially closed by Notarius practice: **adversarial-by-instruction** — the
pipeline's judges were instructed to REFUTE (skeptic lenses of prior-art /
viability), not to "evaluate." This is portable back into the MSL/MIP pipeline as
a strengthening of Controlled Provocation.

---

The discipline is open to patches. Changes go in as a new entry in
AUTHOR_DECISIONS.md, old ones are not erased (modeled on FO-046 HEAD ≠ SOURCE:
every patch with a traceable provenance).
