# NOTARIUS — Complete Working Compendium
AUTHOR: Ruslan Malyavskiy
COMMERCIAL USE PROHIBITED
DATE: 2026-07-20
STATUS: WORKING DOCUMENT

---

## 1. DEFINITION

**Notarius** is a provenance tracker for data elements:
where it came from, what it passed through, native or inserted.

SHORT FORMULA:
```
ORIGIN + TRACE + CURRENT_STATE
```

---

## 2. ORIGIN OF THE PROJECT

The idea grew out of the MSL/MIP Sign Alphabet.

Key clarification (Ruslan):
> "If this were a cryptography problem, it would have been solved decades ago."

That drew the line between two layers:
```
Cryptography:  was it changed? is the signature valid?
Notarius:      where did the element come from? what did it pass through? native or inserted?

INTEGRITY_LAYER ≠ PROVENANCE_LAYER
```

---

## 3. PROJECT VERTICAL

```
MSL/MIP   → sign identity     → WHAT SIGN IS THIS?
Notarius  → element provenance → WHERE DID THE ELEMENT COME FROM?
SSP       → meaning provenance → WHAT HAPPENED TO THE MEANING?

SIGN
↓
ELEMENT
↓
MEANING

The shared question of all three:
Not just "what is it?" —
but "where did it come from and what happened to it?"
```

---

## 4. DIFFERENCE FROM CRYPTOGRAPHY

| Cryptography | Notarius |
|---|---|
| Is the signature valid? | Where is the element from? |
| Does the hash match? | What did it pass through? |
| Was the file changed? | Native or inserted? |
| Is the key known? | When did the break occur? |
| Container level | Element level |

```
SIGNED ≠ NATIVE
HASH_VALID ≠ CLEAN_ELEMENT
CONTAINER_INTACT ≠ ELEMENT_CLEAN
TRACE_EXISTS ≠ TRACE_CONTINUOUS
```

---

## 5. WHAT NOTARIUS DOES NOT DO

```
Notarius ≠ cryptography
Notarius ≠ replacement for a digital signature
Notarius ≠ court
Notarius ≠ proof of truth
Notarius ≠ automatic seizure
Notarius ≠ asset recovery

VALIDATOR ≠ COURT
TRACE ≠ PROOF
```

---

## 6. PROPERTIES (statuses revised by the conveyor, see AUTHOR_DECISIONS)

DISCIPLINE FOR CHECKING PROPERTIES (AD-12, docs/NOTARIUS_DISCIPLINE_2026-07-22_EN.md):
- a property's status does not change without a concrete check-object (D-2/FO-035);
- before the word "barrier" — run it through the catalog of 7 defects (D-3/FO-018);
- a claim that it "checks X" points to the transition DATA→CLAIM→STATUS→TRUST→ACTION (D-1/FO-015).

### 6.1 SEMANTIC_MANIFEST_KEY
```
STATUS: PROPERTY_CANDIDATE (downgraded by AUTHOR_DECISION AD-1, 2026-07-21:
  conveyor not passed; previously — LOCKED IN)
DATE: 2026-07-06

The sender transmits:
  the packet (blocks in any order)
  + the trace key (semantic manifest)

The receiver:
  key → reassembly → verification of order + meaning

WITHOUT THE KEY:  the blocks are there, the meaning is opaque (semantic obfuscation)
WITH THE KEY:     the full structure

DIFFERENCE FROM BLOCKCHAIN:
  blockchain = cryptographic chain with no block semantics
  Notarius   = semantic_type + origin + state for each block
```

### 6.2 SEMANTIC_STRUCTURE_OPACITY (formerly SEMANTIC_LAYERED_DEFENSE)
```
STATUS: PRIVACY_OBSCURITY_PROPERTY / NOT_A_SECURITY_BARRIER
  (AD-11, 2026-07-22: unanimous design-review verdict 3/3;
  grounds — experiments/exp_6_2_reassembly.py;
  previously — PROPERTY_CANDIDATE, before that — LOCKED IN)
DATE: 2026-07-06 / revised 2026-07-22

ARCHITECTURE (a statement of fact, not a strength rating):
  ONE cryptographic barrier (the key)
  + ONE obfuscation layer (schema / typing / order —
    a single kind of secret: knowledge of the layout; their
    "independence" is refuted by experiment:
    one piece of knowledge about the world of formats lifts all three at once)

BOUNDARY PROVEN BY CODE (exp_6_2_reassembly.py:
  1000 trials, 7000 blocks, 60 lines of regex, no key
  and no schema → 100.0% of semantic types recovered):
  for structured business fields (IBAN, amounts, dates,
  currencies, statuses, numbers) structural obfuscation does NOT protect
  semantics — the "meaningless mush" claim is refuted.

WHAT HONESTLY REMAINS:
  1. Friction for a casual observer (privacy, not protection).
  2. Role binding across repeated types (which amount goes with
     which order) — UNVERIFIED, needs a separate experiment
     with a document pool.
  3. Reassembly against a signed manifest — an INTEGRITY property
     (without the manifest you cannot present a correctly assembled
     SIGNED document) — moves to §6.1.

THREAT MODEL:
  works against: a casual observer with no tools;
  does NOT work against: a scripting attacker who knows the world
  (proven) and a motivated adversary.
  Content confidentiality — encryption (the key) ONLY.

NORMATIVELY:
  A weak key is NOT compensated by structural secrecy.
  Kerckhoffs applies to the whole document (this removes the
  contradiction with §8; the question "is Kerckhoffs lifted or
  relocated?" is closed with the answer: not lifted).

FILTER FORMULAS:
  OBFUSCATION ≠ BARRIER
  SHUFFLING ≠ ENCRYPTION
  LAYOUT_SECRET ≠ KEY
  SHUFFLED ≠ CONFIDENTIAL
  TYPE_RECOVERED ≠ ROLE_BOUND
```

### 6.3 DECLARED_CODEPOINT_COUNT (formerly SEMANTIC_INVISIBLE_LENGTH_WITNESS)
```
STATUS: DIAGNOSTIC_METADATA (AUTHOR_DECISION AD-3, 2026-07-21:
  reclassified from a barrier to a diagnostic field inside
  the signed manifest; bypasses proven by tests/test_witness.py)
DATE: 2026-07-07

Each block carries in the manifest a control length in Unicode codepoints.
Any insertion/deletion of a character, including invisible ones (ZWSP U+200B,
ZWJ U+200D, VS16 U+FE0F, BOM, bidi overrides), changes the count
and breaks the check.

CATCHES:
  ZWSP/ZWJ/VS16/BOM inside a block      → len +1
  invisible at the start of a block     → CAUGHT
  invisible at the end of a block       → CAUGHT
  invisible in the middle               → CAUGHT

DOES NOT CATCH:
  an equal-length substitution: "1000" → "2000" (same length)
  → for that you need a separate hash

FORMULA:
  INVISIBLE_INSERTION → CODEPOINT_COUNT_SHIFT → MANIFEST_MISMATCH
  LENGTH_INTACT ≠ CONTENT_INTACT  (both barriers needed)
  KEY_KNOWN ≠ LENGTH_INTACT       (independent layer)

LENGTH_INTACT ∧ CONTENT_INTACT = the full pair

MINIMAL PROTOTYPE (the first working Notarius code):

  def block_with_witness(data: str) -> dict:
      return {"data": data, "cp_len": len(data)}

  def verify_witness(block: dict) -> bool:
      return len(block["data"]) == block["cp_len"]

Three lines. No dependencies. No cryptographic library.
```

---

## 7. FO-CANDIDATE

### MANIPULATION_LEAVES_SUBSTRATE_TRACE
```
STATUS: FO-CANDIDATE / NEEDS_CONVEYOR
DATE: 2026-07-06

CORE_FORMULA:
BEST_VERIFICATION_SYSTEM = SUBSTRATE_RECORDS_MANIPULATION_ITSELF

OBSERVATION:
The best verification systems are those
where the substrate itself records the intervention —
with no external observer.

VERIFIED_CASES:

CASE_1: Punched card (IBM, 1960s)
  Substrate: the physical card
  Manipulation: a hole cannot be patched unnoticed
  Detector: the carrier itself

CASE_2: Photographic film
  Substrate: the chemical layer
  Manipulation: a splice is visible on the frame and at the join
  Detector: the carrier itself

CASE_3: Wax seal
  Substrate: the wax
  Manipulation: opening it destroys the seal
  Detector: the carrier itself

CASE_4: Notarius / semantic tracing
  Substrate: semantic manifest + blocks
  Manipulation: a break in the trace_chain
  Detector: the structure itself

FORMULAS:
  MANIPULATION_VISIBLE ≠ MANIPULATION_PREVENTED
  SUBSTRATE_TRACE = BEST_AVAILABLE_DETERRENT
```

---

## 8. PRODUCT_CANDIDATE

### PROVENANCE_CARRIER
```
STATUS: MORTAL_CARRIER — prototype exists (AD-29); previously CANDIDATE with no code
DATE: 2026-07-12 / refined 2026-07-23

CLARIFICATION (AD-29): THE CARRIER MUST BE MORTAL.
A short-lived, single-use QR carrier is safe "in the wrong hands"
because a copy is useless:
  SHORT LIFE (expired by time) + SINGLE-USE (burned on first
  presentation) = MORTAL_CARRIER
The carrier holds NOT a key, but a short-lived PROOF signed
by a key (the key lives in the enclave/custody, AD-27). This is the human-readable face
of the "mortal copy" (AD-26): understandable to a cashier without crypto jargon.
Prototype: notarius/carrier.py + tests/test_carrier.py (8, green) —
proven: a copy is either EXPIRED or ALREADY_USED.
The pattern is deployed in the world (TOTP, rotating payment QR codes) — AD-23.
BOUNDARY: within the window the carrier is copyable (it is data); the protection is a short
window + single-use + trusted time at the verifier, not "cannot be
copied."
```

### PROVENANCE_CARRIER (original card v0)
```
STATUS: CANDIDATE_REGISTERED — conveyor not run, no prototype
DATE: 2026-07-12

GIST:
The semantic trace is assembled INSIDE the system.
It has to be verified OUTSIDE — where our code is not present.
The carrier = a compact, self-contained, detachable piece of evidence
that survives leaving the system.

LAYER 1 (REJECTED):
  QR as transport INSIDE the pipeline.
  Blind to a no-show finding. Two extra points of silent failure.
  Capacity ~3KB is too small for traces.

LAYER 2 (CANDIDATE):
  A carrier at the BOUNDARY of the system.
  QR exists in order to carry data out to
  where our code is not present: onto paper, onto a screen, into other hands.
  This is not transport — it is an EXIT.

OPEN TRIANGLE (solve together, not sequentially):
  1. What goes into the carrier AT MINIMUM?
     The full trace won't fit. A fingerprint? Critical seals?
  2. Is Kerckhoffs lifted or relocated?
     Who holds the key? Where does the receiver get the public key?
  3. QR or another carrier?
     The carrier is chosen AFTER answering point 1.

DEPENDENCY:
  First semantic tracing (assemble the trace).
  Then the carrier (carry the trace out).
  You cannot print a route sheet that doesn't exist yet.
```

---

## 9. ELEMENT STATE MODEL

```
Every element has:
  ORIGIN
  TRACE
  TIME
  CURRENT_STATE

Possible states:
  INTACT / MODIFIED / PARTIAL / SEGMENTED / MERGED /
  MIXED / CONVERTED / UNKNOWN / ARCHIVED / DELETED / RECOVERED

Example of a normal element:
  ELEMENT_ID: E-145
  ORIGIN: Sensor_A
  CURRENT_STATE: INTACT
  LAST_CONFIRMED: 2026-06-07 14:35
  TRACE_STATUS: CONTINUOUS

Example of a break:
  ELEMENT_ID: E-145
  CURRENT_STATE: MODIFIED
  MODIFICATION_WINDOW: 14:35 - 14:42
  TRACE_STATUS: BROKEN

FORMULAS:
  PROVENANCE ≠ CURRENT_STATE
  TRACE_BREAK_TIME ≠ EXACT_ATTACK_TIME
  INTERVENTION_TIME ≠ INTERVENTION_CAUSE
```

---

## 10. TRACE LEVELS

```
TRACE_LEVEL_1 — CRITICAL_ONLY
  amounts, statuses, dates, access grants, signatures, commands, coordinates

TRACE_LEVEL_2 — SEMANTIC_UNITS
  intent, claim, value, role, permission, prohibition,
  provenance, authority_status, execution_status

TRACE_LEVEL_3 — FULL_ELEMENT_TRACE
  characters, tokens, structural elements,
  transformation steps, byte representations

PRINCIPLES:
  TRACE_DEPTH_FOLLOWS_RISK
  TRACE_COST must be compared with LOSS_SCALE
  MORE_TRACE ≠ MORE_TRUTH
  MORE_TRACE = MORE_OBSERVABILITY
```

---

## 11. USE IN FORENSICS

For a court, the difference between:
- "I think it was forged"
- "here is the provenance chain with a break at step 3"

Notarius = a digital chain of custody for data elements.

```
Adoption model:
Banks have historically introduced standards through pain
(SWIFT, ISO 20022, PCI DSS).
No need to lobby ahead of time.
What's needed is for the product to exist and be ready for moment X.
```

---

## 12. ASSET TRACKING

```
ASSET_A = 10 000 000
split →
  A1 = 2 000 000 → account_X
  A2 = 3 000 000 → wallet_Y
  A3 = 5 000 000 → securities_Z

Notarius sees:
  these are not independent pieces —
  they are fragments of a single original provenance.

FORMULAS:
  SPLIT_ASSET ≠ LOST_PROVENANCE
  MIXED_ASSET ≠ CLEAN_ASSET
  UNREACHABLE_ASSET ≠ UNTRACEABLE_ASSET
  TEMPORARY_SAFE_HAVEN ≠ PROVENANCE_RESET
```

---

## 13. PHYSICAL ANALOGY (banknote)

A $100 bill cut into three parts and taped together.
The serial number MF 34567890 C is present on two of the fragments.

```
OBSERVATION:
Physical fragmentation does not destroy provenance
if the identifier is embedded in the substrate, not in the container.

FORMULA:
SPLIT_OBJECT ≠ LOST_PROVENANCE
PROVENANCE_SURVIVES_FRAGMENTATION

ARCHITECTURAL TAKEAWAY:
The provenance identifier must be embedded in the element,
not only in the container.
```

---

## 14. PUNCHED-CARD ANALOGY

IBM EBCDIC punched card, 1960s.
Each character is a unique combination of punches.
Impossible to forge: the hole is either there or it isn't.

```
Punched card:  character → unique physical mark
Notarius:      element   → unique semantic mark

Punched card:  three in one:
  KEY:       the punch combination = the identifier
  CARRIER:   the card itself carries the data
  DETECTOR:  manipulation is physically visible

PRINCIPLE:
  COMPLEXITY ≠ SECURITY
  SIMPLICITY = VERIFIABILITY
  VERIFIABILITY = TRUST
```

---

## 15. NICHE CHECK

```
Web search, 2026-07-06:

WHAT EXISTS:
  Data lineage / data provenance — a real industry
  Academic element-level provenance implementations (medicine, W3C)
  Blockchain-based provenance (patent level)

WHAT DOES NOT EXIST:
  A provider embedded on the transaction path
  Real-time semantic tagging at the element level
  Detection of foreign insertions as an infrastructure product

VERDICT: NICHE_NARROWED / COMPOSITION_PRODUCT /
         MECHANISM_EXISTS_INTEGRATION_MISSING
  (AUTHOR_DECISION AD-8, 2026-07-21, following the prior-art review —
   docs/PRIOR_ART_REVIEW_2026-07-21_EN.md; previously NICHE_CONFIRMED)

THE NICHE (precise formulation):
  provenance that is portable across organizational boundaries
  at the level of a business-document field,
  with a human-readable report of the break,
  available to small businesses outside closed networks.
```

---

## 16. FIRST PROTOTYPE (plan)

```
Plain text provenance demo.

Show:
  1. An element with an origin tag
  2. An element with a normal trace chain
  3. An insertion with no tag
  4. Detection of the break
  5. State: INTACT / INSERTED / UNKNOWN

Example:
  DOCUMENT_A:
  amount = 1000000
  origin = invoice_458
  trace = created → checked → archived
  state = INTACT

  After substitution:
  amount = 9000000
  origin = UNKNOWN
  trace = missing
  state = INSERTED_OR_MODIFIED

  Expected output:
  TRACE_BREAK_DETECTED
  field: amount
  expected_origin: invoice_458
  actual_origin: UNKNOWN
  status: NEEDS_REVIEW
```

---

## 17. CURRENT PRIORITY

```
ACTIVE_FRONT:
  MSL/MIP Sign Cards → Modules → Integrators
  (confirmed by AUTHOR_DECISION AD-6, 2026-07-21)

PARKED:
  Notarius
  SSP
  Video Trace
  Element Provenance
  Asset Recovery Trace
  PROVENANCE_CARRIER

ORDER:
  1. MSL/MIP core
  2. Notarius tracing (assemble the trace)
  3. PROVENANCE_CARRIER (carry the trace out)
```

---

## 18. CANONICAL PHRASES

```
Cryptography verifies the integrity of the container.
Notarius verifies the provenance of the element.
SSP verifies the state of the meaning.

Notarius does not recover the asset itself.
Notarius makes the asset's provenance hard to erase.

Not every byte. Not just the whole file.
But chunk + boundary.

When internal memory is unreliable — you need an external trace.

The best verification systems are those
where the substrate itself records the intervention.

PRIMITIVE = RELIABLE = AUDITABLE

A SIGNED LIE REMAINS A LIE,
BUT IT STOPS BEING ANONYMOUS.

INTEGRITY ≠ AUTHENTICITY ≠ TRUTH
SIGNED ≠ TRUE
TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH

The chain is needed not to prove the truth —
but to localize where the lie entered and who put it there.
(recorded as AUTHOR_DECISION AD-10, 2026-07-22)

A SIGNATURE DOES NOT STOP LYING —
IT TURNS THE LIE INTO EVIDENCE AGAINST THE SIGNER.

SIGNED_LIE = SELF_PRODUCED_EVIDENCE
  under the CONDITIONS:
    KEY_BOUND_TO_IDENTITY      (otherwise evidence against the key, not the person)
  ∧ RECORD_BEYOND_LIAR_CONTROL (an external anchor — the admission cannot be withdrawn)
  ∧ FORCED_TO_SIGN_IN_SYSTEM   (otherwise the lie is kept off the trace)

Self-attestation (defect №1) + binding to identity + external anchor (AD-23)
= NOT three holes, but ONE condition that turns a signature into evidence.
Notarius does not forbid lying — it makes the lie costly, addressed, self-
produced. Connection: §11 (court, admission against interest), AD-10.
(recorded as AUTHOR_DECISION AD-24, 2026-07-22)

UNSTEALABLE = UNCOPYABLE

Data is always copyable (silently, remotely, endlessly). The "unstealable"
part of the key is NOT data: it is either bound to something physical/biological
that cannot be cloned (PUF, biometric unlock, a hardware non-extractable element),
or SPLIT so that one part is useless (Shamir, M-of-N).
The goal is not "cannot be stolen," but:
  DIGITAL_THEFT (silent, endless, remote)
     → PHYSICAL_THEFT (visible, one at a time, leaves a trace)
This is the same principle as MANIPULATION_LEAVES_SUBSTRATE_TRACE (FO-7):
make the invisible visible. A single point of trust is fatal
(self-attestation AD-24 + fork AD-22 + key theft) — the cure is one:
break it up and distribute it (independence). Connection: PUF/Shamir (AD-23).
(recorded as AUTHOR_DECISION AD-25, 2026-07-22)

RUBBER_HOSE_LIMIT (thermorectal cryptanalysis)

Coercion under threat (rubber-hose, the "fifth iron method," xkcd 538)
is OUTSIDE THE REACH OF ANY CRYPTOGRAPHY. All of our techniques (threshold, heartbeat,
enclave) protect against SILENT theft; the iron is LOUD theft, where the thief is right there
and doesn't care what you know.
  CRYPTO_PROTECTS_AGAINST_SILENT_THEFT ≠ PROTECTS_AGAINST_COERCION
It is not eliminated — only DETERRED organizationally:
  - distributing holders across jurisdictions (the iron on one person doesn't yield
    the key; you'd need N teams in N countries at once — a visible war);
  - a negative quorum / right of veto (under torture you give the alarm, not the key);
  - a duress code (a fake unlock + a silent lockdown and call for help).
No response SAVES the person — it only denies the thief the key.
Final confirmation of AD-24: crypto does not protect the truth and does not protect
the person; it makes the silent LOUD, and beyond that — law, police, society.
Do not sell the AD-27 custody as "unbreakable."
(recorded as AUTHOR_DECISION AD-28, 2026-07-23)
```

---

*COMMERCIAL USE PROHIBITED / Ruslan Malyavskiy / 2026-07-20*
