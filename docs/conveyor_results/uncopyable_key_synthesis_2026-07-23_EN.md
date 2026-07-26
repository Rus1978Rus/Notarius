# The uncopyable part of the key — summary of 7 sources

DATE: 2026-07-23
SOURCES (independent, 7): internal conveyor (partial) + vendors
Copilot, DeepSeek, Gemini, GPT, Qwen, Kimi.
DUPLICATES EXCLUDED (FF-003): GPT was submitted twice; the first "Qwen" =
DeepSeek verbatim. Not counted again.
CRITERION: does the idea turn silent DIGITAL theft into visible PHYSICAL
theft (UNSTEALABLE = UNCOPYABLE, AD-25).

## Each source's favorite

| Source | Strongest idea | Axis |
|---|---|---|
| Internal | Distributed cluster (flag) | threshold |
| Copilot | Social threshold (M-of-N) | threshold |
| GPT | Moving constellation (proactive threshold, never assemble the key) | threshold |
| Kimi | Dead-man's hand (mortal copy) + a threshold+heartbeat+enclave assembly | mortal copy / synthesis |
| DeepSeek | EEG dead-man's hand (5 people) | biology |
| Gemini | Sacrificial porcelain (destruction on signing) | destruction-on-read |
| Qwen | Photobleaching PUF (scar on read) | destruction-on-read |

## Four axes that emerged from the 7 sources

**Axis 1. DISTRIBUTED THRESHOLD** (M-of-N, proactive refresh) — the most
frequent: Copilot, GPT, Kimi (Choir), internal, Qwen (social threshold).
A copy of one share = zero; the full key exists as data at no single
point — only as a quorum EVENT. GPT: never assemble the key in one
device's memory at all.

**Axis 2. DESTRUCTION-ON-READ** (read = damage / single-use) —
Gemini (porcelain), Qwen (photobleaching), Kimi (rusty+print-run), internal
(a wearing token, a glass capsule). Reading leaves a scar → the clone
diverges from the original and it's VISIBLE.

**Axis 3. BIOLOGICAL DEAD-MAN'S HAND** (a living participant) — DeepSeek
(EEG), internal (metabolic implant), Kimi (body as salt). Theft =
kidnapping a living person, a maximally conspicuous crime.

**Axis 4. MORTAL COPY** (new, Kimi) — not "protect the bits" but "make any
copy mortal": the key lives while a heartbeat flows from the owner's living
loop; noticed theft → stopped the heartbeat → all copies died globally.
Direct link: the E-Continuity "Viking" forebear ("degrades from the
absence of an event") + AD-24 (a record beyond the liar's control).

## THE CONVERGING FILTER (found ≥5 times independently) — the main haul

**"Readable once = copyable, if reading doesn't destroy."**
A physical factor is uncopyable ONLY while it is consumed/destroyed on
every signature. Once "frozen into a number," it's ordinary data, and the
protection reduces to an ordinary HSM. Found by: the internal skeptic,
Gemini, Qwen, Kimi, GPT (chip emulation from the outside). This is the
filter that culls half the "physical" ideas (radioisotope-TRNG,
diamond-readable, etc.).

## TWO POLES OF TENSION (the real vendor split)

- **HUMAN-IN-THE-LOOP** (DeepSeek/EEG, bio): robust against silent theft,
  but coercible (kidnapping) and unusable.
- **NO HUMAN** (Qwen/degradation, threshold): usable and free of the human
  factor, but coercion moves onto the device.
Neither pole is absolute — both admit it in their "honest limits."

## THE MATURE SYNTHESIS (Kimi + GPT converge)

No single axis wins alone. A composite system:
```
THRESHOLD (M-of-N, never assemble the key)  ← axis 1: no single point
  + MORTAL HEARTBEAT (copies die)            ← axis 4: theft is temporary
  + HARDWARE ANCHOR (secure enclave,         ← axis 2: non-extractable/scar
    non-extractable key / degradation)
  + EXTERNAL TIMESTAMP (OpenTimestamps)       ← AD-23: time can't be forged
```
The pragmatic minimum for mass use (Kimi): a non-extractable key in a
phone's secure enclave (theft = theft of the phone = physical) + a
server-side heartbeat/attestation + server-side accounting (a balance
can't be stolen with a copy of the key).

## What of this is BUILDABLE today (adopt-don't-invent, AD-23)

- M-of-N threshold + proactive refresh — **ready standards** (threshold
  signatures, proactive secret sharing; this is how custodians work).
- Secure enclave — in every phone.
- Heartbeat — trivial.
- External timestamp — OpenTimestamps, free.
The exotica (quantum, bio, destruction) are unreachable POLES for
comparison, not for building. Your original "Perimeter" instinct is
confirmed by 7 sources: distribution is the practical answer.

## Connection to the project core

- "Make theft visible" = FO-7 MANIPULATION_LEAVES_SUBSTRATE_TRACE.
- "Mortal copy" = E-Continuity Viking + AD-24.
- "Never a single point" = a cross-cutting diagnosis (self-attestation
  AD-24 + fork AD-22 + key theft AD-25) — one cure: fragment and
  distribute.

## Recommendation (candidate for an AUTHOR_DECISION)

For Notarius signing keys: **a threshold signature (M-of-N) + secure
enclave + an optional mortal heartbeat + an external timestamp anchor**.
In one loop it closes: key theft (no single point), coercion
(distributed), fork (threshold), and it makes theft physical + visible +
temporary. All from ready standards.

## Honest caveat

The ideas are LLM output (`LLM_OUTPUT ≠ VERIFIED_COPY`); the strength is in
the CONVERGENCE of 7 independent loops on the axes and the filter, not in
the authority of one. 13 internal ideas were left unjudged (limit) —
thematically covered by the vendors along the same 4 axes, so a separate
check would not have changed the picture.

---

## Appendix: all vendor ideas (data preservation)

**Copilot** (8): Crystal fingerprint; Biofluid key; Radioactive
marker; Social threshold★; Self-destruct timer with triggers; Geofencing;
Group ritual fingerprint; Community memory. Discarded: radioactive.
**DeepSeek** (8): NV diamond; Sweaty key; Barkhausen grains; Thermal barcode;
Living chain (GPS jitter); EEG dead-man's hand★; Ritual key; Paper decay.
Discarded: diamond.
**Gemini** (6): Entropic dissipative token; Quantum-Darwinian
signature of the environment; A council of semantic agents; Kinetic
resonance; Sacrificial porcelain★; Bio-cryptographic herd. Discarded: herd.
**GPT** (8): Ceramic scar (PUF); Living co-key; Atomic matches;
Moving constellation★; A ring of sentries; Negative quorum; Choir (memory);
Chameleon key (canary shares). Discarded: living co-key.
**Qwen** (7): Photobleaching PUF★; Microbiome reagent;
Social dead-man's hand (Shamir 3-of-5); Melting key (IoT mesh); Performance key;
Mnemonic trap; Graffiti anchor. Discarded: mnemonic.
**Kimi** (7): Rusty key (wear); Body as salt (enclave); Choir (threshold);
Dead-man's hand★ (mortal heartbeat); Group shared memory; Single-use print run;
Kinetics (gesture). Discarded: kinetics.
**Internal** (30 raw, 2 STRONG checked): Quantum memory★,
Metabolic implant★; the rest across the 4 axes, 13 left unjudged.

★ = strongest per the source.
