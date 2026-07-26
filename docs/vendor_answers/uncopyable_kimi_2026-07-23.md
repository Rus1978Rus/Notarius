# uncopyable_kimi_2026-07-23

Answer to the blind prompt of 2026-07-22. Vendor: Kimi (Moonshot AI). Answer date: 2026-07-23.
7 ideas (A×2, B×2, C×3), then the rejection and the strongest.

## A) PHYSICS/BIOLOGY

### A1. "Rusty key"

2. **MECHANISM:** part of the key is not a value but the STATE of a physical carrier, which changes irreversibly with every read (wear). The carrier is a strip/chip whose response to a query depends on the accumulated history of reads (read-wear: domain structure, polymer, flash cells with controlled degradation). Computing the signature = f(current state, counter). Each use ages the carrier → yesterday's snapshot of the state expires.
3. **WHY UNCOPYABLE:** to copy the state is to measure it, and measuring it changes it (a macro analogue of the no-cloning theorem). A clone differs in its wear history → it diverges from the original at the very next use, and the divergence is VISIBLE to the verifier: the original and the clone begin to contradict each other by the mere fact of both existing.
4. **THEFT BECOMES:** you have to steal the carrier itself — one at a time, and the owner notices it is gone; or build a physical model of the carrier in a lab — expensive, slow, not mass-scalable, and the model expires with every use of the original.
5. **CANDID LIMIT:** with a small response space a model-clone is possible (full characterization); a manufacturer backdoor; carrier failure = death of the key (a recovery ritual is needed); the degradation must be monotonic and predictable, otherwise false rejections.
6. **MADNESS:** 3.

### A2. "The body as salt"

2. **MECHANISM:** biometrics not as a password but as an uncopyable PARTICIPANT in the computation: the key is reconstructed by a fuzzy extractor from a live measurement (veins, ECG pattern, micro-movements) inside the device's secure enclave; the biometrics and the key never leave the enclave — only the signature result goes outside. The measurement is bound to the moment (challenge-response) so that a recording cannot be replayed.
3. **WHY UNCOPYABLE:** there is no copyable data — there is a living organ in a living body at the moment of signing; a fingerprint mold/photo is static, and does not pass challenge-response and liveness.
4. **THEFT BECOMES:** you need part of the body of a living person and their presence — abduction/coercion, a maximally conspicuous crime; or a presentation attack (a fake organ) — the lab against liveness, one at a time.
5. **CANDID LIMIT:** the presentation-attack vs. liveness arms race; coercion is not closed — only pairing with B2 (the distress heartbeat) saves it; medical changes (injury, illness) break access; a template leak from a weak enclave = biometrics that cannot be revoked.
6. **MADNESS:** 2.

## B) DISTRIBUTION/DEAD MAN'S SWITCH

### B1. "Chorus" (proactive threshold)

2. **MECHANISM:** shares of the key held by N parties (devices, people, independent services); a signature requires only M-of-N (threshold signature; the shares are never gathered in one place). Plus proactive refresh: every epoch the shares are re-dealt from scratch — the old shares turn to garbage.
3. **WHY UNCOPYABLE:** copying one share (even M-1 shares) yields zero; the full key does not exist as data at any point in spacetime — it exists only as a quorum EVENT.
4. **THEFT BECOMES:** you must compromise M independent parties SIMULTANEOUSLY within a single epoch — a coordinated operation against several people/sites, noisy by definition (M victims will notice something odd); after the epoch, everything stolen expires.
5. **CANDID LIMIT:** collusion of M insiders; a shared 0day across all quorum devices (monoculture); social-engineering the quorum — mitigated by different channels, geography, epoch speed. The difficulty of exploitation is real: this is grown-up infrastructure (custodians work exactly this way).
6. **MADNESS:** 2.

### B2. "Dead man's switch" (the key is a subscription to life)

2. **MECHANISM:** the key lives only as long as it receives a periodic "heartbeat" — a signed heartbeat from an independent loop (the owner's watch/phone, their daily activity + server attestations). No N heartbeats in a row → the key material is wiped (or frozen until a quorum recovery ceremony). Copies of the key inherit the same mortality: without heartbeats any copy dies, wherever it lies.
3. **WHY UNCOPYABLE:** you can copy bits, but you cannot copy a SUBSCRIPTION to someone else's life: the thief does not produce a heartbeat (it is issued by the owner's living loop), so their copy is a corpse on a delay. The owner, noticing the theft, simply stops the heartbeats — and ALL copies die globally, wherever they are.
4. **THEFT BECOMES:** keeping the victim's life-support infrastructure running and silent — a continuous, visible, prolonged crime (holding a person or their devices), not a one-off silent dump.
5. **CANDID LIMIT:** availability (hospital, airplane, a hike — the key must not die from life itself: wide windows and a hierarchy of heartbeats); a DoS on the heartbeats = killing the key without theft (degradation instead of death for gray cases); the heartbeat loop itself must be uncopyable (a hardware anchor in the watch/phone — otherwise the circle closes on itself).
6. **MADNESS:** 4.

## C) MADNESS

### C1. "Shared memory"

2. **MECHANISM:** part of the key is the living collective memory of a small group: activation requires M-of-N members to answer a fresh question whose answer exists only in the group's recently lived context ("which wording did we choose on Tuesday, and why did we reject the second one?"). The key is not a phrase (that gets written down and copied) but a continuous social protocol.
3. **WHY UNCOPYABLE:** you can copy a recording, but the question is fresh every time — the answer does not yet exist anywhere except in the heads of those who lived it; the "key" is reborn every week and dies there too.
4. **THEFT BECOMES:** months-long infiltration of the group, living its life — visible social work, does not scale, not remote.
5. **CANDID LIMIT:** people write things down (and the protocol becomes data — a failure of the criterion); a mole from day one; group turnover = loss of the key; recovery after a quarrel/burnout is hell; usability is catastrophic.
6. **MADNESS:** 5.

### C2. "Single-use print run"

2. **MECHANISM:** the key exists as N physical single-use copies: a print on a carrier that is destroyed on reading (flash paper, a chemical layer, glowing once; or a sealed cell — open = read = burn). A signature = the ritual of destroying a copy on camera.
3. **WHY UNCOPYABLE:** a copy = a new physical print run (a printing press, chemistry, time); reading without destruction is impossible — the carrier gives up the data at the cost of its life.
4. **THEFT BECOMES:** stealing paper — one at a time, noticeable (a sheet missing from the stack); forging a run — the print shop against the owner, the traces are material.
5. **CANDID LIMIT:** a photo BEFORE destruction (ritual discipline: read and burn alone, the camera records it); printer/print-file memory — the file must be destroyed after printing, and that is digital again; the logistics of replenishing the run.
6. **MADNESS:** 5.

### C3. "Kinetics" (a gesture as the key)

2. **MECHANISM:** the signature = performing a personal physical pattern (the trajectory of a hand holding a phone, the rhythm of typing a phrase, micro-tremor) — behavioral biometrics + a challenge (a new phrase/trajectory each time).
3. **WHY UNCOPYABLE:** the skill is in the body, not in a file; a copy = teaching a person/machine to perform someone else's pattern — a transfer of skill, not of data.
4. **THEFT BECOMES:** physically reproducing someone else's performance — either a trained double or a robot with recorded kinematics.
5. **CANDID LIMIT — FATAL for the criterion:** a sensor recording of past performances is a DIGITAL copy, replayed by ML/a robot silently and remotely; theft returns to the digital domain. Plus behavioral drift (injury, stress, age).
6. **MADNESS:** 3.

## IN THE END

1. **FIRST TO REJECT: C3 "Kinetics."** The only one that fails the CENTRAL CRITERION outright: a sensor recording is a silent digital copy, the replay is remote and scalable. C1 is madder, but its theft is honestly physical (social work); C3 merely disguises the digital as the physical.

2. **GENUINELY STRONG: B2 "Dead man's switch."** It inverts the problem: not "protect the bits from copying" (unsolvable) but "make any copy mortal." Theft is guaranteed to become physical: keeping the victim's living loop running and silent is a prolonged, visible crime that can be neither automated, nor scaled, nor pulled off remotely. A mature integration: the heartbeat is signed by a threshold quorum (B1) on hardware anchors (A-class/secure enclave) — the composite system closes both availability and the uncopyability of the heartbeat. For a mass application, the pragmatic minimum: the key in the phone's secure enclave (non-extractable — theft = stealing the phone = physics) + a server heartbeat/attestation + token accounting on the server (the balance cannot be stolen by copying the key).
