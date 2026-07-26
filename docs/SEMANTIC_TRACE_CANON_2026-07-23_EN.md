# SEMANTIC TRACING — THE CANON (the heart of Notarius)

STATUS: CANONICAL / AUTHORITATIVE
DATE: 2026-07-23
AUTHOR: Ruslan Malyavskiy
BASIS (product origins): NOTARIUS_FULL_SESSION.md (2026-07-20) §1–5, §9–10,
§16–18; AD-10 (localizing the lie), AD-19 (core implementation), AD-22
(fork/truncation boundaries), AD-34 (the content axis), AD-36 (witnesses).
PURPOSE: a single, authoritative statement of what semantic tracing is. This
is the CENTER of the product; signature/key/threshold/witnesses are plumbing
in service of that center, not ends in themselves.

---

## 0. THE CANONICAL DEFINITION

**A semantic trace is the honest story of a single data element: where it came
from, what it passed through, and whether it belongs here or was inserted.**

The canonical formula (§1):
```
ORIGIN + TRACE + CURRENT_STATE
```
An element's three questions (§3): **where did it come from? what did it pass
through? is it native or inserted?**

---

## 1. WHICH LAYER IT LIVES IN

This is not about cryptography (§2, the author's key caveat: "if the problem
were cryptographic, it would have been solved decades ago"). Tracing is a layer
ABOVE integrity:

```
INTEGRITY_LAYER ≠ PROVENANCE_LAYER          (§2)

Cryptography:  was it changed? is the signature valid?   (CONTAINER level)
Notarius:      from where? through what? native/inserted? where's the break?  (ELEMENT level)
```

A signature answers "the container is intact." Tracing answers "and the element
inside — is it native or slipped in?" These are different questions; the second
one is the product.

---

## 2. THE VERTICAL (place in the ecosystem) (§3)

```
MSL/MIP   → sign identity      → WHAT IS THIS SIGN?
Notarius  → element provenance → WHERE DID THE ELEMENT COME FROM?     ← we are here
SSP       → meaning provenance → WHAT HAPPENED TO THE MEANING?
```
The question shared by all three is not "what is this?" but "where did it come
from and what happened to it."

---

## 3. THE CANONICAL LAWS (invariants)

From §4 and §18 — the non-removable distinctions that tracing stands on:

```
SIGNED ≠ NATIVE                       signed ≠ native
HASH_VALID ≠ CLEAN_ELEMENT            hash matched ≠ element clean
CONTAINER_INTACT ≠ ELEMENT_CLEAN      container intact ≠ element clean   (the AD-34 axis)
TRACE_EXISTS ≠ TRACE_CONTINUOUS       a trace exists ≠ the trace is continuous
PROVENANCE ≠ CURRENT_STATE            provenance ≠ current state
INTEGRITY ≠ AUTHENTICITY ≠ TRUTH      integrity ≠ authenticity ≠ truth
SIGNED ≠ TRUE                         signed ≠ true
TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH   the trace LOCATES, it does not PROVE
MORE_TRACE ≠ MORE_TRUTH               more trace ≠ more truth
MORE_TRACE = MORE_OBSERVABILITY       more trace = more observability
TRACE_BREAK_TIME ≠ EXACT_ATTACK_TIME  break time ≠ exact attack time
```

The overarching law of purpose (AD-10, §18):
> **The chain is not there to prove the truth — it is there to localize where
> the lie entered and who introduced it. A signature does not stop anyone from
> lying — it turns the lie into evidence against the signer.**

---

## 4. THE OBJECT: THE ELEMENT (§9)

Every element carries four things:
```
ORIGIN         — where it arose (Sensor_A, invoice_458, …)
TRACE          — the chain of events, what was done to it
TIME           — when (self-declared until anchored — see §10)
CURRENT_STATE  — where it is now
```

---

## 5. THE STATE MODEL (§9)

```
Possible element states:
  INTACT / MODIFIED / PARTIAL / SEGMENTED / MERGED /
  MIXED / CONVERTED / UNKNOWN / ARCHIVED / DELETED / RECOVERED

TRACE_STATUS: CONTINUOUS | BROKEN

Implemented in trace.py (a subset, AD-19):
  INTACT · MODIFIED · BROKEN · ORIGIN_UNKNOWN
  + INSERTED_OR_MODIFIED as the §16 outcome
```
A normal element: `ORIGIN=Sensor_A, STATE=INTACT, TRACE=CONTINUOUS`.
A break: `STATE=MODIFIED, MODIFICATION_WINDOW=14:35–14:42, TRACE=BROKEN`.

---

## 6. IMPLEMENTATION: A CHAIN OF SIGNED EVENTS (§16, AD-19)

A semantic trace = an append-only chain of an element's events:
```
CREATED → TRANSFORMED → TRANSFERRED → REVIEWED → …

each event carries:
  value_hash   — SHA-256 of the element's value at this point (NFC)
  cp_len       — length in code points (insertion diagnostic, AD-3)
  actor        — who did it (Ed25519 signature = binds the "who")
  prev_hash    — link to the previous event (append-only; tampering breaks the link)
  content_scan — the content axis: native/inserted via invisible characters (AD-34)
```
CREATED/TRANSFORMED are allowed to change the value; TRANSFERRED/REVIEWED must
preserve it (otherwise MODIFIED).

BUILD STATUS: `notarius/trace.py` + `tests/test_trace.py`, green. The sealing
(signature/threshold/witnesses/recovery) is PLUMBING that makes every line of
the story unforgeable: envelope_v2 (who), cosign (fork/truncation, M4/AD-36),
custody/frost (threshold without reassembling the key), carrier (the mortal
carrier), integrations (RS recovery, OTS time). All of it is in service of the
trace, not the other way around.

---

## 7. TRACING LEVELS (§10)

```
L1 CRITICAL_ONLY    — amounts, statuses, dates, access, signatures, commands
L2 SEMANTIC_UNITS   — intent, claim, value, role, permission, provenance,
                      authority_status, execution_status
L3 FULL_ELEMENT     — characters, tokens, transformation steps, bytes

PRINCIPLE:  TRACE_DEPTH_FOLLOWS_RISK
            weigh TRACE_COST against LOSS_SCALE
            MORE_TRACE = observability, NOT truth
```

---

## 8. WHAT IT GIVES YOU: LOCALIZATION (§11, §16, AD-10)

Not "someone forged it," but a human-readable breakdown:
```
element: amount
status:  TRACE_BREAK_DETECTED
state:   MODIFIED
last_signer: checker-3
break_at_step: 3
  - step 3: value changed on REVIEWED (should have been preserved)
```
For a court, this is the difference between "I think it was forged" and "here is
the chain of provenance with a break at step 3." Notarius = a digital **chain of
custody for data elements** (§11).

---

## 9. WHAT NOTARIUS DOES NOT DO (§5)

```
≠ cryptography        ≠ proof of truth
≠ signature replacement  ≠ automatic seizure
≠ a court             ≠ asset recovery

VALIDATOR ≠ COURT     TRACE ≠ PROOF
```
Notarius does not recover the asset — it makes **provenance hard to erase**
(§18).

---

## 10. HONEST BOUNDARIES (no overclaim)

1. **Self-attestation (not closed).** An actor signs THEIR OWN event — and can
   write down a signed lie. The trace LOCALIZES responsibility; it does not
   prove the truth (`SIGNED ≠ NATIVE`). But: a signed lie stops being anonymous
   (§18) — it becomes evidence against the signer (AD-24).
2. **Time.** The `at` field is a self-declaration with no external anchor; the
   modification window is unprovable without OpenTimestamps/RFC 3161 (adapter
   AD-31).
3. **Silent omission.** The chain proves the continuity of the RECORDED events,
   not that every real event was recorded (the Viking/E-Continuity lesson:
   degradation FROM THE ABSENCE of an event). The remedy is periodic re-checking.
4. **Fork/truncation (M4).** A single chain doesn't catch it; closed by an
   external witness of the head (cosign.py, AD-36) — only if the verifier
   requires a quorum.
5. **Coercion.** Outside the reach of any cryptography (AD-28).
6. **Advisory mode.** The report does not block — the decision belongs to policy.

---

## 11. CANONICAL PHRASES (§18, verbatim)

> Cryptography checks the integrity of the container.
> Notarius checks the provenance of the element.
> SSP checks the state of the meaning.
>
> Notarius does not recover the asset itself.
> Notarius makes the asset's provenance hard to erase.
>
> Not every byte. Not just the whole file. But chunk + boundary.
>
> When internal memory is unreliable — you need an external trace.
>
> The best verification systems are those where the substrate itself records tampering.
>
> PRIMITIVE = RELIABLE = AUDITABLE
>
> A SIGNED LIE REMAINS A LIE, BUT STOPS BEING ANONYMOUS.
>
> The chain is not there to prove the truth — it is there to localize
> where the lie entered and who introduced it.

---

## 12. THE MINIMAL UNFORGEABLE SEGMENT · SUBSTRATE INDEPENDENCE

An extension of §18's "chunk + boundary" and the author's question about video
(Video Trace, the parked item in §17). Generalization: the law is the same for
ANY kind of information.

**THE LAW:**
```
MINIMAL UNFORGEABLE SEGMENT = CHUNK + BOUNDARY + BINDING AT BIRTH
```
- **chunk** — the smallest meaningful part (frame, field, reading, paragraph);
- **boundary** — the coupling to the neighboring chunk (prev_hash), where an
  edit shows up;
- **binding at birth** — hash + source signature + time anchor, at the moment
  the element comes into being.

**WHY IT GENERALIZES:** unforgeability lives NOT in the content but in the
BINDING (hash + coupling + signature + anchor). The binding does not depend on
the kind of information — bytes are bytes. This is substrate independence (the
parent's FO-013; Vakhter: what is real is what survives transformation).
Provenance is about STRUCTURE and BINDING, not about content. There is no
unforgeable PIECE OF CONTENT (pixels/bytes) — any can be repainted; only the
binding is unforgeable, and the forger doesn't have it.

**ONE MODEL — DIFFERENT FORMS:**
```
Kind             Chunk              Boundary           Binding at birth
video            frame/block        neighboring frame  camera signs the capture (C2PA)
audio            sample window      neighboring window mic/recorder
text/document    sentence/field     chunk coupling     author/editor
finance          transaction/field  ledger link        bank/counterparty
sensors/IoT      reading            time-ordered chain sensor at the source
software/supply  file/build         dependency link    build signature (sigstore/SLSA)
med/science      measurement/scan   chain              instrument/clinician
law/property     record/clause      chain of transfers notary/registry
```
Video Trace, finance, telemetry are PARTICULAR FORMS of one layer, not separate
products.

**ALREADY IN THE CODE:** we commit at the CANONICAL level, not per byte —
canonical JSON of the event + NFC normalization. Resilient to legal
reformattings (whitespace, field order), it breaks only on a real edit. This is
exactly "chunk + boundary," not "every byte."

**THE HONEST BOUNDARIES ARE UNIVERSAL TOO** (about the method, not about video):
- `SIGNED ≠ NATIVE` / the "analog hole" is everywhere: a camera films a fake
  screen; a registry carries an honestly-signed fraudulent record; a sensor is
  fed a false reading. It proves "not edited after birth," not "the content is
  true."
- No retroactive binding — bind at the moment of birth, not after the fact.
- Theft of the source's key → forgeable (whoever holds the key is the source).
- Coercion — out of scope (AD-28).
- Legal transformations change the bytes → commit at the canonical level (hence
  "chunk + boundary," not "every byte").

**BOTTOM LINE:** the minimal unforgeable segment is not pixels/bytes, but a
coupled, signed chunk with a boundary, bound at birth; and it is unforgeable
exactly to the extent that (a) it was bound from the first second and (b) the
key was not stolen. One law for any information.

---

## 13. SEAL OF OWNERSHIP · OWNERSHIP ≠ POSSESSION

The author's move: signature/encryption are mature and "have hit the ceiling";
if a break-in is only a matter of time, we need a mechanism where BREAK-IN ≠
APPROPRIATION. The answer — raise provenance from "the element's history" to the
element's TITLE.

**THE LAW:**
```
OWNERSHIP (title) ≠ POSSESSION
```
- **possession** — I hold the bytes in hand (this breaks: steal the key/cipher
  and you hold them);
- **ownership** — I am the rightful owner (this survives a break-in).

Cryptography guards POSSESSION (badly, it breaks). **The owner's seal guards
OWNERSHIP.** A break-in gets you the BYTES, but not the TITLE.

**WHY THE SEAL IS ON THE OUTSIDE:** there is no unremovable seal inside the data
(the same ceiling as video, §12: bytes get repainted, watermarks get stripped).
The seal = an EXTERNAL, witnessed, dated-BEFORE-the-theft registration that
"this data (its hash) is mine," bound to a recognized IDENTITY.

**MECHANISM (assembly of bricks, notarius/title.py, AD-44):**
```
brand()          the owner seals: hash of data + identity + time, owner's signature
TitleRegistry    witnesses co-sign the FIRST seal on a hash, refuse a
                 conflicting/later one → first witnessed = owner
resolve_title()  title goes to the seal with a quorum of witnesses; a bare claim is rejected
transfer()       agreed TWO-SIDED transfer (both sign)
```
PROVEN BY CODE (test_title.py): the thief cracked the cipher, copied the data,
seals it with his own key → the witnesses refuse (the owner is already witnessed)
→ title stays with the owner, thief rejected. **Reading ≠ ownership.** Replaying
someone else's co-signatures doesn't work (a co-signature over the owner's body
does not validate the thief's body).

**HONEST BOUNDARIES:**
- Guards OWNERSHIP, NOT POSSESSION: the thief holds and uses the bytes but does
  not become the owner (like a stolen painting — held, not owned, and it will
  surface).
- Full theft of the owner's KEY allows forging a transfer in his name — a
  residual; removed by a THRESHOLD (custody/frost: the "owner" = M-of-N, one key
  can't sign) + revocation + fork detection by a witness (cosign, §10). The seal
  alone does not save you from key theft.
- The strength of the seal = how EARLY + how DISTRIBUTED + how tightly bound to a
  REAL identity.
- Does not close coercion (AD-28).

**DIGITAL INK ≠ SEMANTIC ROOT (a refinement, AD-45):**
The seal-signature and the quorum of witnesses are DIGITAL INK: they rest on the
SECRECY of keys, and so inherit the same ceiling (break the key, forge it). Real
resistance to a break-in lives in the SEMANTIC ROOT: the COHERENCE of a
distributed history. To forge ownership semantically is not "break one key" but
rewrite a history that many INDEPENDENT sources already recorded earlier and in
agreement (you cannot make witnesses "not see" an early truth, you cannot age
your own marks).
```
                    Digital ink            Semantic root
protection rests on secret of one key      coherence of history across many
point of failure    one (break it, you're in)  none: needs a quorum ACROSS TIME
strength grows with key length             number of INDEPENDENTS + earliness + corroboration
```
Resolution by CONVERGENCE (title.converge, AD-46): title goes to whoever the
most independent records converge on; a partial break-in (k broken keys) does
not flip the title if the owner has more independent sources. This is the
parent's CONVERGENCE_TEST (FO-100) and how real provenance works (art,
registries) — a web of mutually-corroborating records, not one key. HONESTLY:
convergence measures COHERENCE (the cost of forgery), NOT truth (FF-005
RECURRENCE ≠ VALIDITY); it is strong exactly to the extent that the sources are
REALLY independent (Sybil bypasses it); cryptography remains the INK of the
record (a total break-in is treated with crypto-agility AD-23, not with an
"unbreakable key").

**HYBRID OF TWO AXES (title.resolve_hybrid, AD-47):** the digital axis (seal
quorum — strong against forgery-without-a-key, weak to a break-in) + the
semantic axis (convergence — strong against a break-in, weak to Sybil). In the
hybrid the attacker must beat BOTH. The main value: if the axes DIVERGE (digital
says A, semantics says B) — that is ITSELF a signal (likely key theft OR Sybil):
the hybrid flags CONTESTED and calls in a human, instead of QUIETLY handing over
the title. Pure digital would have handed it to the thief; the hybrid catches it.
```
CONFIRMED   both axes agree     — the attacker must break BOTH
PROVISIONAL one for, the other silent — weaker
CONTESTED   axes diverge        — key theft/Sybil, a human decides (NOT quietly)
```
Proven by code (test_title.py): a break-in of the digital axis (a fake seal)
with the semantics alive → CONTESTED, not a quiet handover; Sybil (fake
convergence) with the seal alive → also CONTESTED. Residual: breaking BOTH axes
consistently — costlier and noisier than either alone.

**ATTACK ON THE CROSS-CHECK: THE MIRROR (AD-48).** The cross-check is beaten if
the thief SUBSTITUTES one axis with a mirror that agrees with the already-forged
one — then both "agree" (CONFIRMED), and the divergence signal never fires. This
is not two axes but one puppet show. The defense lives NOT in "two axes" but in:
```
1. DIFFERENT roots of trust  — witness ∩ source = ∅ (one hand doesn't hold both axes)
2. AN INDEPENDENT channel     — the verifier takes the axis not from the presenter's hands
3. A LOCKED past              — a public append-only anchor; a mirror has no early trace
4. OUT-OF-BAND trust          — witnesses/sources from a PRE-ESTABLISHED set
```
In the code (title.resolve_hybrid): witness_keys/source_keys are pre-established
(the thief's fake sources don't count); an intersection of roots → independence
undermined, CONFIRMED downgraded to CONTESTED; external_anchor contradicts →
CONTESTED. THE IRREDUCIBLE RESIDUAL: if the thief controls ALL of the verifier's
channels AND there is no early external anchor — the mirror wins. You cannot
bootstrap trust from nothing: the verifier needs at least ONE independent,
trustworthy view of reality that the thief never touched (FO-005 INTERFACE ≠
REALITY).

**THE REGISTRY UNDER GLASS (AD-49, the author's metaphor).** The public anchor
hangs under glass. The thief draws only ON THE GLASS (on the presented
copy/channel), not on the registry itself. Take the registry out — it is clean,
the added marks stayed on the glass. The defense against the mirror is
operationally = DON'T trust the glass, TAKE OUT the registry and RECONCILE
(reconcile: MATCH / FORGERY_ON_GLASS). The registry (notarius/anchor.py):
append-only (a hash chain — the past can't be rewritten), the first seal on a
hash = authority, pull() takes the record from the REGISTRY, not from the
presenter's hands. Publicness: cosign (a distributed copy) + OTS/Bitcoin (an
indelible dated notebook; stamp a network block in this medium, AD-31). Proven
(test_anchor.py): "Thief" is presented, the registry holds "Ruslan" →
FORGERY_ON_GLASS; a full mirror on both axes is exposed by the EXTRACTED registry
(external_anchor from pull → CONTESTED); a secret edit of the past breaks the
hash chain (verify_integrity). The boundary (the metaphor shows it too): it works
AS LONG AS the registry can be extracted; if the thief holds all channels + there
is no early record → you see the glass forever.

**WEIGHT BY EARLINESS (AD-50).** The thief fabricates ONLY after the theft → all
his records are LATE. Give an old record more weight — and a thousand fresh fakes
won't outweigh a few of the owner's old records. CRITICAL: the weight is taken
from the ANCHORED rank (order in the public append-only registry, AD-49), NOT
from the claimed date — otherwise the thief backdates his fakes. Geometric decay
(0.5**rank) makes flooding powerless: the sum of all late records is bounded, the
early ones dominate. Code: anchor.source_ranks + title.converge_weighted. Proven
(test_title.py): 2 of the owner's early sources beat 20 of the thief's late fakes;
a backdated claimed-date doesn't help (weight comes from rank); an unanchored
source = 0. It is precisely the public anchor (idea 1) that PROVES earliness
(idea 2) — without it "I recorded earlier" is just words. HONESTLY: earliness ≠
truth (FF-005); an early lie is possible; the residual is a thief who planted
many GENUINELY early records in advance (expensive foresight — the past is not
cheap to forge).

**BOTTOM LINE:** a break-in can be made meaningless for APPROPRIATION, but not
for POSSESSION. The owner's seal is an external, witnessed registration of title
that a break-in does not rewrite; the resistance lives in the semantic ROOT
(coherence of a distributed history), not in the secret of one key. Best of all
is the HYBRID: digital ink + semantic root, where the divergence of the axes
itself raises the alarm. The thief will get the bytes but will not become the
owner.

---

## REFINEMENTS FROM THE EXTERNAL AUDIT (2026-07-26, AD-90)

An external reviewer (working from the docs, without the code) raised three
points. Checked against the code:

**A. Hashing order (removes the AD-4 ambiguity).** FIXED:
`Raw Input → NFC → canonical JSON → hash → sign`. The `value_hash` in trace.py
is computed AFTER NFC (`_value_hash = sha256(NFC(value))`). So **AD-4 IS CLOSED
for hash integrity**: `é` and `e`+`´` give ONE hash. IMPORTANT: NFC does NOT
remove invisible/zero-width characters — that is an ORTHOGONAL content axis
(scan_hardened/detect), not the hash. That is, AD-4 is closed for computing the
hash, but does NOT substitute for detecting hidden code points.

**B. The witness pool is closed (Sybil).** Title convergence is counted ONLY
over a PRE-ESTABLISHED, out-of-band-verified set of keys (`trusted_sources` in
converge / anchored `source_ranks` in converge_weighted). Dynamically discovered
witnesses are NOT counted — otherwise Sybil (fake sources planted in advance)
bypasses the weighting. THE BOUNDARY (honestly): even with a pool, convergence is
strong exactly to the extent that the identities are REALLY independent; genuine
independence comes from PKI/out-of-band, not from the engine itself.

**C. Silent omission — an open item (gap acknowledged).** The reviewer is right:
"periodic re-checking" does NOT catch a non-event without an external model of
expectation. Honestly: detecting a silent omission requires a DECLARATIVE SCHEMA
OF EXPECTED TRANSITIONS (a state-machine contract) — e.g. after CREATED there
must be a TRANSFORMED; a CREATED→ARCHIVED transition skipping TRANSFORMED triggers
an alert; or a heartbeat oracle of frequency. This is a NEW LAYER (through the
trace, by the AD-83 rule), a candidate for implementation. In the current core it
is NOT implemented — the boundary stays honest.

---

## PROVENANCE OF THE CANON

ORIGIN: Ruslan Malyavskiy's own work (NOTARIUS_FULL_SESSION.md, 2026-07-20) +
decisions AD-10/19/22/34/36. This document is a CANONIZATION: bringing scattered
origins into a single authoritative form. LLM_GENERATED (assembly and phrasing),
the sources are the author's. Status of the center: semantic tracing is the
PRODUCT; the sealing is plumbing in service of it.
