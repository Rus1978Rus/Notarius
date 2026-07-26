# E-Continuity — methodological analysis of the parent (checking the AD-13 conclusion)

DATE: 2026-07-22
SOURCE: E_CONTINUITY_STRUCTURED_2026_06_05.zip (release v2.3, former name
Template E), author Ruslan Malyavskiy. The text core is docs/e_continuity/
(heavy PDF/DOCX editions kept outside the repository).
METHOD: line-by-line reading + checking my inference from AD-13 against the
facts + cross-porting into Notarius.
DISCIPLINE: this file is LLM output; by the framework's own rule
`LLM_OUTPUT ≠ VERIFIED_COPY`; it is not a verified copy but an analysis.

---

## 0. What E-Continuity is (from the source, not from memory)

An engineering framework for analyzing and managing the **long-term
recoverability** of objects, systems, documentation, skills, technologies, and
mission (intended purpose).

The central thesis (MIGRATION, pp. 17–21):
```
Storing an object is NOT the same as preserving its function.
A system is preserved only when its target mission
can be recovered across time, changes of people,
technologies, and institutions.

Continuity = governed recoverability through time.
```

The main case is the **Viking Mission 1976**: 56,000 images, 40 years of
storage, 2 years spent reading 3,000. `DATA PRESERVED ≠ DATA READABLE`. The
Viking rule: "a system degrades not from an event but from the absence of an
event" — without periodic checking, the fading is imperceptible.

## 1. Checking my inference from AD-13 (HEAD ≠ SOURCE)

In AD-13 I recorded the unifying theme of "governed recoverability" as a
**conclusion, not a fact**, and marked the definition as pending from the
author. Checked against the source:

**THE CONCLUSION IS CONFIRMED VERBATIM.** The framework is literally called
"governed recoverability" and its thesis is `governed recoverability through
time`. More than that, the source **explicitly declares itself the proto-father
of the ecosystem** (MIGRATION, pp. 263–271):
```
E-Continuity:  OBJECT_PRESERVED ≠ MISSION_RECOVERABLE
MSL/MIP:       SIGN_EXISTS ≠ MEANING_RECOVERABLE
AI Conveyor:   REVIEW_COMPLETED ≠ VALIDATED
Foundation FO: HEAD ≠ SOURCE
```
This is exactly the family of formulas `X_EXISTS ≠ X_RECOVERABLE` that I
hypothesized. The inference is closed as CONFIRMED_BY_SOURCE.

## 2. CORRECTING the lineage (fact vs my diagram)

In E_CONTINUITY_FRAMING I drew Notarius as a **direct** child of E-Continuity.
The source clarifies: the direct children are MSL/MIP, AI Conveyor, Foundation
FO. Notarius descended from MSL/MIP (NOTARIUS_FULL_SESSION: "The idea arose out
of MSL/MIP"). So:
```
E-Continuity (proto-father)
   └── MSL/MIP
          ├── Notarius   → element provenance
          └── SSP        → meaning provenance
```
**Notarius is a GRANDCHILD of E-Continuity via MSL/MIP, not a direct child.**
The diagram in the framing document is corrected (AD-14).

## 3. Direct ancestors of Notarius's constructs (parent → grandchild)

These matches are not analogies — they are inheritance:

| E-Continuity (parent) | Notarius (grandchild) |
|---|---|
| OBJECT_PRESERVED ≠ MISSION_RECOVERABLE | SIGNED ≠ NATIVE |
| INTERFACE_STATE ≠ RECOVERABILITY_STATE | INTERFACE ≠ REALITY; integrity ≠ provenance |
| CONTINUITY CHAIN: Object→Metadata→…→Mission | the element's chain of provenance; FO-015 DATA→…→ACTION |
| PROOF TESTING: Static ≠ Dynamic ≠ Mission | design-review §6.2/§6.3: test on a concrete object |
| "degrades from the absence of an event" | without periodic verify-provenance it silently rots |
| CONTENT ≠ SOURCE; COPY ≠ PROVENANCE | the Notarius core verbatim |
| LLM_OUTPUT ≠ VERIFIED_COPY | the honest-boundaries discipline of all our documents |

**The key discovery:** our experiment exp_6_2_reassembly.py is, in the parent's
language, a **Dynamic Proof Test** of the §6.2 property. "Static proof" (the
manifest looks like protection) ≠ "Dynamic proof" (it withstood a format
attack). We independently applied the parent's proof-testing without knowing it
was called that. That is strong confirmation of both the method and the kinship.

## 4. What the parent gives Notarius from above (to adopt)

### 4.1 PROOF TESTING as an explicit discipline (adopt on top of D-2)
The three levels — Static / Dynamic / Mission — are more precise than our
FO-035 "test on a concrete object." Proposal: extend Notarius discipline D-2 —
a property is not promoted above the proof level it has actually passed (§6.2
passed a dynamic refutation → downgraded; §6.3 too).

### 4.2 CONTINUITY CHAIN as a superstructure over FO-015
The parent's chain `Object→Metadata→Format→Infrastructure→Operators→Custody→
Institution→Capability→Mission` is a macro-level above the Notarius micro-chain
(a data element). Notarius closes the first links (Object→Metadata); the parent
shows that above them are Custody and Institution — where Notarius provenance one
day plugs in.

### 4.3 "Degradation from the absence of an event" (adopt as a risk note)
A direct consequence for Notarius: a signed envelope without **periodic
re-checking** gives a false sense of preservation (INTERFACE_STATE ≠
RECOVERABILITY_STATE). The display "verify passed a year ago" ≠ "the provenance
is alive today." A discipline candidate.

## 5. The parent's governance rules that Notarius now falls under

Since Notarius is a descendant, the ecosystem's rules apply (RULES_REGISTER):
- **DOCUMENT_PROVENANCE_CARD** on every important document — we don't have one.
- **PROJECT_PACKAGE_RULE**: README_RU/map + MANIFEST + PROVENANCE + STATUS_NOTE +
  SHA256SUMS — we have it partly (there's a README, not the rest).
- **PROJECT_LANGUAGE_LAYER**: a Russian layer + English terms with a gloss — we
  observe this.
- **PERMANENT_RULE_PREFLIGHT_GUard**: "a rule protects the project, it does not
  paralyze it" — compatible with our discipline.
- **PROJECT_NAME_LOCK / OLD_FOLDER_RULE** — taken into account.

HONEST GAP: the Notarius repository does not yet satisfy two of the parent's
rules (provenance-card, full package-set). This is not urgent (research track
AD-9) but is recorded as a debt — a candidate for AUTHOR_DECISION if you decide
to bring Notarius up to the E-Continuity package standard.

## 6. What NOT to touch (the parent's boundaries, honored)

The parent itself sets hard STATUS_LOCKs and "what not to do": don't claim Gold
Master without artifacts; don't invent hashes; don't mix interface and
recoverability; v2.3.1 is a rename only, contents unchanged. These are not our
decisions — we don't touch them, only record that Notarius does not contradict
them.

## 7. Bottom line (input for AD-14)

The parent's definition has been obtained and read. My inference from AD-13 is
confirmed by the source verbatim (`governed recoverability`). One factual
correction: Notarius is a grandchild via MSL/MIP, not a direct child. To adopt
from above: proof-testing (4.1), the continuity-chain superstructure (4.2), the
"degradation from the absence of an event" risk (4.3). To record as a debt: the
parent's provenance-card and package-set rules. The parent's boundaries —
honored, untouched.
