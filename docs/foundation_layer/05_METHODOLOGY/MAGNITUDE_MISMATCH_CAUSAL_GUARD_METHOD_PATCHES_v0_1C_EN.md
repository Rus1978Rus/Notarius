# MAGNITUDE_MISMATCH_CAUSAL_GUARD_METHOD_PATCHES_v0_1C_RU

PRIVATE AUTHORIAL PROJECT / COMMERCIAL USE PROHIBITED  
Author / owner: Ruslan Malyavskiy

DOCUMENT_TYPE:
METHOD_PATCH_SET / CONVEYOR_INTEGRATED_PATCHED_DRAFT

DATE:
2026-06-04

CREATED_AT_UTC:
2026-06-04T18:31:02.158721+00:00

SOURCE:
Conveyor review of `MAGNITUDE_MISMATCH_CAUSAL_GUARD_METHOD_PATCHES_v0_1B_RU` by Kimi, Gemini, GPT-4-style methodological review.

CONVEYOR_VERDICT:
ACCEPT_WITH_PATCHES

CURRENT_STATUS:
MULTI_DOMAIN_CAUSAL_METHOD_CANDIDATE  
CONVEYOR_ACCEPT_WITH_PATCHES  
PATCHES_INTEGRATED_IN_THIS_DRAFT  
READY_FOR_MATRIX_FILE_REBUILD  
NOT_FO_YET  
NOT_WORKING_METHOD_YET  
NOT_FINAL_GUARD  
NOT_VALIDATED_METHOD  

---

## 0. What changed since v0_1B

The conveyor's mandatory patches have been integrated:

```text
PATCH_04A_EXPECTED_MAX_OPERATIONALIZATION
PATCH_05A_TIER_REVOCATION_RULE
PATCH_03A_LIMITED_COUNTEREXAMPLE_CLAIM
PATCH_RISK_01_CYCLIC_CAUSALITY_WARNING
PATCH_01A_MARGINAL_UTILITY_ACTION_TEST
PATCH_07A_SYSTEM_CAPABILITY_CHECK
```

Key refinement:

```text
EXPECTED_MAX_EFFECT is no longer eyeballed.
It must be tied to an empirical base:
historical analogues, statistics, engineering scenarios,
worst known case for trigger class.
```

---

## 1. CORE DEFECT ADDRESSED

```text
DEPTH_IS_NOT_AUTOMATIC
```

Main finding:

```text
DEEPER_CAUSE_CLAIM ≠ VALID_CAUSAL_DEPTH
APPEARANCE_OF_DEPTH ≠ REAL_DEPTH
```

Kin to FO-001:

```text
FORM ≠ STATUS
CLAIM ≠ PROOF
```

For causality:

```text
DEPTH_IS_NOT_AUTOMATIC ≠ DEPTH_IS_ALWAYS_PRESENT
```

---

## 2. CORE METHOD

`MAGNITUDE_MISMATCH_CAUSAL_GUARD` checks:

```text
whether the visible cause is sufficient
for the observed magnitude of the effect.
```

If:

```text
magnitude(OBSERVED_EFFECT) >> EXPECTED_MAX_EFFECT(VISIBLE_TRIGGER)
```

then:

```text
VISIBLE_TRIGGER is insufficient as a full cause,
and a search for the connected causal organism is required.
```

If there is no mismatch:

```text
the method does not activate.
```

---

## 3. CAUSAL ORGANISM

```text
FULL_CAUSE ≠ SINGLE_CAUSE
ROOT_CAUSE ≠ SINGLE_ORIGIN_POINT
```

The relevant cause of a large event is not a single point but the minimal connected system of causes:

```text
TRIGGER
+
AMPLIFIER
+
ENABLER
+
ROOT_STRUCTURE
=
MINIMUM_CAUSAL_ORGANISM
```

Formula:

```text
An event of magnitude S is usually produced not by a single cause
but by the minimal connected system of causes
sufficient for S.
```

---

## 4. PATCH_01: STOP_RULE

Problem:

```text
The method reaches for depth,
but without a stopping criterion it can slide into infinite regress.
```

### STOP_RULE_v0_1C

FOR EACH NEW_LAYER:

```text
CHECK_01:
Mechanistic link.
Does the next layer explain why the previous layer had that effect?
IF NO -> STOP

CHECK_02:
Explanatory power.
Does the next layer add new understanding?
IF NO -> STOP

CHECK_03:
Relevant responsibility.
Is the next layer within an actor / system
that could have acted, designed, prevented, or responded?
IF NO -> STOP

CHECK_04:
Controllability / preventability.
Does the next layer give a new point of prevention?
IF NO -> STOP

CHECK_05:
Controllability threshold.
Does the next layer no longer add any new controllability?
IF YES -> STOP
```

### PATCH_01A_MARGINAL_UTILITY_ACTION_TEST

So that `MARGINAL_UTILITY > 0` does not remain subjective:

```text
MARGINAL_UTILITY > 0
=
the new layer yields a new action,
a new control,
a new point of prevention,
a new check,
a new responsibility,
or a new design/organizational change
that the previous layer did not provide.
```

If the new layer merely restates an already-known action:

```text
MARGINAL_UTILITY = 0
→ STOP
```

Formula:

```text
NEXT_LAYER = RELEVANT ONLY IF:
MECHANISTIC_LINK = TRUE
EXPLANATORY_GAIN = TRUE
RELEVANT_RESPONSIBILITY = TRUE
NEW_PREVENTABILITY = TRUE
MARGINAL_UTILITY_ACTION > 0
```

---

## 5. PATCH_02: CAUSAL_LINK_TEST

Problem:

```text
Layers may sit side by side without being causally linked.
```

### CAUSAL_LINK_TEST_v0_1C

FOR EACH TRANSITION:

```text
LAYER_N -> LAYER_N+1
```

Question:

```text
Could LAYER_N have produced EFFECT without LAYER_N+1?
```

If YES:

```text
LAYER_N+1 is not necessary.
Check: is LAYER_N+1 an amplifier of sufficiency?
If NO -> remove or reformulate the layer.
```

If NO:

```text
LAYER_N+1 is necessary.
Check the mechanistic link.
```

Formula:

```text
LAYER_N+1 IS VALID IF:
NECESSITY = TRUE
OR
SUFFICIENCY_UPGRADE = TRUE
```

### Failed-link example

```text
Cold Fusion old transition:
TRIGGER = error in the calculations
OLD AMPLIFIER = expedited peer review

Problem:
the calculation error could have existed without expedited peer review.

Result:
transition QUESTIONABLE.

More connected formulation:
AMPLIFIER = absence of independent verification of the calculations before the public announcement.
```

---

## 6. PATCH_03: FALSIFICATION_ATTEMPT

Problem:

```text
The method is good at seeking depth,
but it must be able to test for its absence.
```

### FALSIFICATION_ATTEMPT_v0_1C

Look for cases where:

```text
VISIBLE_TRIGGER = ADEQUATE_FULL_CAUSE
NO_DEEPER_LAYER_REQUIRED
```

Tested boundary candidates:

```text
1. A single road accident
2. The Chelyabinsk meteor, 2013
3. A student's calculation error
4. A lone tree falling in a field
5. Chicxulub impact / dinosaur extinction
```

Result:

```text
the method did not manufacture false depth.
```

### PATCH_03A_LIMITED_COUNTEREXAMPLE_CLAIM

Permitted formulation:

```text
NO_COUNTEREXAMPLE_FOUND_IN_TESTED_BOUNDARY_CASES_N5
```

or, more broadly:

```text
NO_COUNTEREXAMPLE_FOUND_IN_SELECTED_CASES
```

Forbidden formulation:

```text
NO_COUNTEREXAMPLES_EXIST
```

Status:

```text
FALSIFICATION_ATTEMPT_COMPLETED
BOUNDARY_BEHAVIOUR_CONFIRMED
NOT_VALIDATION
```

---

## 7. PATCH_04: MAGNITUDE_CALIBRATION_RULE

Problem:

```text
magnitude(E) >> M may be too intuitive a judgment.
```

### PATCH_04A_EXPECTED_MAX_OPERATIONALIZATION

`EXPECTED_MAX_EFFECT(VISIBLE_TRIGGER)` must be determined not intuitively but through one or more grounding anchors:

```text
1. HISTORICAL_ANALOGUES
What usually happened with such a trigger in comparable systems?

2. STATISTICAL_BASELINE
What range of consequences is typical for the event class?

3. DESIGN_BASIS / SAFETY_CASE
What worst-case was the system designed against?

4. WORST_KNOWN_CASE_FOR_TRIGGER_CLASS
What is the maximum known effect for such a trigger?

5. DOMAIN_EXPERT_JUDGMENT
Only if items 1–4 are insufficient,
and flagged with EXPERT_JUDGMENT_USED.
```

Rule:

```text
EXPECTED_MAX_EFFECT
=
EMPIRICAL_OR_DESIGN_BASELINE_MAX_FOR_TRIGGER_CLASS
```

Decision:

```text
IF OBSERVED_EFFECT >> EXPECTED_MAX_EFFECT:
MAGNITUDE_MISMATCH = TRUE

IF OBSERVED_EFFECT ≈ EXPECTED_MAX_EFFECT:
MAGNITUDE_MISMATCH = FALSE

IF EXPECTED_MAX_EFFECT cannot be grounded:
MAGNITUDE_STATUS = UNCERTAIN
→ DO_NOT_ACTIVATE_FULL_DEPTH_SEARCH
→ REQUEST_SOURCE_OR_DOMAIN_BASELINE
```

---

## 8. PATCH_05: SOURCE_TIER_SYSTEM

Problem:

```text
Mixing sources of differing quality.
```

### SOURCE_TIER_SYSTEM_v0_1C

```text
TIER_1:
PRIMARY_SOURCE
Official commission reports
Court documents
Archival materials
Official investigations
Peer-reviewed scientific papers
STATUS: SOURCE_VERIFIED

TIER_2:
SECONDARY_ANALYSIS
Academic reviews
Journalistic investigations backed by documents
Documentary material with verifiable references
STATUS: SOURCE_PARTIALLY_VERIFIED

TIER_3:
INTERPRETIVE_MODEL
Educational modules
Popular books
Wikipedia only for navigation
STATUS: INTERPRETIVE_ONLY

TIER_4:
NOT_LOCATED
STATUS: SOURCE_NOT_YET_LOCATED
```

Rule:

```text
TIER_3 and TIER_4 cannot be the sole source for ROOT_STRUCTURE.

ROOT_STRUCTURE requires TIER_1
or TIER_1 + TIER_2.
```

### PATCH_05A_TIER_REVOCATION_RULE

Problem:

```text
A TIER_1 document may later be refuted,
revised, or replaced by a stronger TIER_1.
```

Rule:

```text
IF TIER_1_SOURCE is contradicted, superseded, or legally/officially overturned
BY later TIER_1_SOURCE:

old_source_status =
TIER_1_REVOKED
or
TIER_1_SUPERSEDED
or
TIER_1_CONTESTED

newer_source becomes controlling source
for the disputed claim.
```

Important:

```text
TIER_1_REVOKED does not mean "delete the source".
It remains as evidence of initial framing,
but not as controlling evidence for truth claim.
```

---

## 9. PATCH_06: ACTIVATION_THRESHOLD

Problem:

```text
The method could be perceived as an "always dig" tool.
```

### ACTIVATION_THRESHOLD_v0_1C

```text
METHOD_ACTIVATES_ONLY_IF:
magnitude(OBSERVED_EFFECT) > EXPECTED_MAX_EFFECT(VISIBLE_TRIGGER)
```

If:

```text
magnitude_mismatch = FALSE
```

then:

```text
METHOD_NOT_REQUIRED
NO_CAUSAL_DEPTH_SEARCH
STOP_AT_TRIGGER / STOP_BEFORE_TRIGGER
```

If:

```text
magnitude_mismatch = TRUE
```

then:

```text
METHOD_ACTIVATES
DEPTH_SEARCH_BEGINS
APPLY_PATCHES_01_05
```

Formula:

```text
NO_MISMATCH = NO_CAUSAL_DEPTH_SEARCH
TRIVIAL_EFFECT -> METHOD_NOT_REQUIRED
ORDINARY_LOCAL_ADEQUATE_EFFECT -> METHOD_NOT_REQUIRED
LARGE_SCALE_FAILURE -> METHOD_ACTIVATES
```

---

## 10. PATCH_07: SYSTEM_SCOPE_CHECK

Problem:

```text
Some events may be natural,
with no agent,
with no institutional or technical system of responsibility.
The method must not artificially manufacture a root structure
where no relevant system exists.
```

### SYSTEM_SCOPE_CHECK_v0_1C

Before depth search ask:

```text
IS THERE A RELEVANT HUMAN / TECHNICAL / INSTITUTIONAL SYSTEM
WITH RESPONSIBILITY, CONTROL, DESIGN, PREVENTION, OR RESPONSE ROLE?
```

If NO:

```text
NO_SYSTEM_SCOPE
METHOD_NOT_REQUIRED
STOP_AT_TRIGGER
```

If YES:

```text
CONTINUE TO MAGNITUDE_MISMATCH AND CAUSAL_LAYER_ANALYSIS
```

### PATCH_07A_SYSTEM_CAPABILITY_CHECK

The presence of a system is not enough on its own.

You must check:

```text
DID THE SYSTEM HAVE A REALISTIC TECHNICAL / ORGANIZATIONAL CAPABILITY
TO PREVENT, REDUCE, DETECT, WARN, RESPOND, OR CONTAIN THE EFFECT?
```

If NO:

```text
SYSTEM_SCOPE_WEAK
DEPTH_SEARCH_LIMITED
DO_NOT_ASSIGN_SYSTEM_FAILURE_WITHOUT_CAPABILITY
```

If YES:

```text
DEPTH_SEARCH_ALLOWED
```

Formulas:

```text
NATURAL_EVENT_ALONE ≠ AUTOMATIC_DEPTH_SEARCH

NATURAL_EVENT + HUMAN_OR_TECHNICAL_SYSTEM_EXPOSURE = POSSIBLE_DEPTH_SEARCH

DEPTH_SEARCH_REQUIRES_SYSTEM_SCOPE

SYSTEM_SCOPE_REQUIRES_CAPABILITY_FOR_STRONG_FAILURE_CLAIM
```

---

## 11. PATCH_RISK_01: CYCLIC_CAUSALITY_WARNING

Problem:

```text
Layers can start referencing one another:
A explains B, B explains C, C explains A again.
```

Rule:

```text
IF causal stack contains circular dependency:
A -> B -> C -> A

THEN:
CYCLIC_CAUSALITY_RISK
STACK_INVALID_UNTIL_REWRITTEN
```

Valid stack must be:

```text
directional
non-circular
mechanistically traceable
```

---

## 12. Zones of method application

### ZONE_1: LARGE_SCALE_FAILURE

Condition:

```text
magnitude(EFFECT) >> EXPECTED_MAX(TRIGGER)
SYSTEM_SCOPE = TRUE
CAPABILITY = TRUE or PARTIAL
```

Behaviour:

```text
METHOD_ACTIVATES
```

Examples:

```text
Chernobyl
Fukushima
Challenger
Boeing 737 MAX
GFC 2008
COVID-19
Iraq WMD
```

### ZONE_2: ORDINARY / LOCAL / ADEQUATE EFFECT

Condition:

```text
magnitude(EFFECT) ≈ EXPECTED_MAX(TRIGGER)
```

Behaviour:

```text
METHOD_NOT_REQUIRED / STOP_AT_TRIGGER
```

Examples:

```text
single car accident
student calculation error
ordinary local failure
```

### ZONE_3: NON_AGENT_EVENT WITHOUT RELEVANT SYSTEM_SCOPE

Condition:

```text
natural / non-agent event
no relevant human / technical / institutional system
```

Behaviour:

```text
METHOD_NOT_REQUIRED / STOP_AT_TRIGGER
```

Examples:

```text
tree falling in empty field
Chicxulub asteroid impact
```

---

## 13. Current status after conveyor patch integration

```text
MAGNITUDE_MISMATCH_CAUSAL_GUARD

STATUS:
MULTI_DOMAIN_CAUSAL_METHOD_CANDIDATE
CONVEYOR_ACCEPT_WITH_PATCHES
PATCH_04A_INTEGRATED
PATCH_05A_INTEGRATED
PATCH_07A_INTEGRATED
PATCH_RISK_01_INTEGRATED
READY_FOR_MATRIX_FILE_REBUILD
NOT_FO_YET
NOT_WORKING_METHOD_YET
NOT_FINAL_GUARD
NOT_VALIDATED_METHOD
```

---

## 14. Rules for MATRIX_FILE_v0_2 rebuild

For every case:

```text
1. Identify VISIBLE_TRIGGER.
2. Ground EXPECTED_MAX_EFFECT using:
   - historical analogue;
   - statistics;
   - design basis;
   - worst known case;
   - expert judgment only if marked.
3. Decide MAGNITUDE_MISMATCH:
   TRUE / FALSE / UNCERTAIN.
4. Check SYSTEM_SCOPE:
   TRUE / FALSE / WEAK.
5. Check SYSTEM_CAPABILITY:
   TRUE / PARTIAL / FALSE / UNKNOWN.
6. If mismatch TRUE and system scope exists:
   build causal organism.
7. For each layer:
   apply STOP_RULE.
8. For each transition:
   apply CAUSAL_LINK_TEST.
9. For each claim:
   assign SOURCE_TIER.
10. If source was superseded:
   apply TIER_REVOCATION_RULE.
11. Check for cyclic causality.
12. Mark:
   SOURCE_VERIFIED / PARTIALLY_VERIFIED / NOT_LOCATED.
```

---

## 15. Status lock

```text
EMERGENT_FINDING ≠ FO
METHOD_PATCH_SET_CANDIDATE ≠ WORKING_METHOD
CONVEYOR_ACCEPT_WITH_PATCHES ≠ VALIDATED_METHOD
NO_COUNTEREXAMPLE_FOUND_IN_SELECTED_CASES ≠ NO_COUNTEREXAMPLES_EXIST
READY_FOR_MATRIX_FILE_REBUILD ≠ READY_FOR_FINALIZATION
```

---

## 16. Next action

Create:

```text
MAGNITUDE_MISMATCH_CAUSAL_GUARD_MULTI_DOMAIN_MATRIX_v0_2_RU.md
```

The matrix must apply this v0_1C patch set to selected cases and explicitly mark:

```text
ZONE
EXPECTED_MAX_EFFECT_GROUNDING
MAGNITUDE_MISMATCH
SYSTEM_SCOPE
SYSTEM_CAPABILITY
CAUSAL_ORGANISM
SOURCE_TIER
TIER_REVOCATION_STATUS
CYCLIC_CAUSALITY_CHECK
FINAL_CASE_STATUS
```

END_OF_DOCUMENT
