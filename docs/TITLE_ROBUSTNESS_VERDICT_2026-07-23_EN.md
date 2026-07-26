# ROBUSTNESS VERDICT: the unified title breakdown (resolve_full)

DATE: 2026-07-23
BASIS: AD-44…AD-51 (seal of ownership → convergence → hybrid → mirror → anchor →
earliness → unified verdict). Test: scripts/stress_title.py.
STATUS: LLM_GENERATED; the results were actually measured in the environment.

## What is assembled into one call

`title.resolve_full(data, seals, records, witnesses, anchor, …)` joins FOUR
independent signals and issues a human-readable verdict:

```
① DIGITAL axis     — the witnessed seal (quorum M-of-N)
② SEMANTIC axis    — convergence of independent records, WEIGHTED BY EARLINESS
③ PUBLIC ANCHOR    — the registry "under glass": pull() = the authoritative window
④ MIRROR DEFENSE   — different roots for the axes + registry integrity
```

Confidence levels:
```
ANCHORED_CONFIRMED  anchor + both axes agree     (strongest)
ANCHORED            anchor is authoritative, the axes don't contradict
PROVISIONAL         no anchor, the axes agree     (no independent window)
CONTESTED           contradiction/mirror/independence undermined
TAMPERED            the registry was secretly rewritten
NONE                not a single support
```

## Stress-test results (actually measured)

**1. Fuzz — 500 randomized scenarios** (random flood 0–200 fakes, break-in of the
digital axis, backdated records):
| Metric | Result |
|---|---|
| **THE THIEF GOT THE TITLE** | **0 of 500** (the invariant holds) |
| A break-in of the digital axis actually occurred | 169 times |
| …and caught by the anchor as CONTESTED | **169 of 169** |
| Clean case → title to the owner | always |

**2. External process — reconciling SHA-256 with `openssl`** (an independent
implementation):
| Metric | Result |
|---|---|
| openssl available | yes |
| Hash divergences | **0 of 50** |

**3. External network — public anchors (honestly):** probes of blockstream,
mempool, the OTS calendar, freetsa, digicert → **000/403, egress closed by
policy**. A network anchor (Bitcoin/TSA) is **unavailable** in this environment —
not forged, honestly marked as a limitation (like AD-31). For a real pilot the
anchor is placed in an environment with a network.

## The human-readable verdict — examples

**Clean (owner early + seal + anchor):**
```
TITLE: Ruslan · CONFIDENCE: ANCHORED_CONFIRMED
  anchor + digital + semantic — all for Ruslan
```

**The thief breaks the digital axis (2 compromised witnesses), but the anchor
holds:**
```
TITLE: — not awarded — · CONFIDENCE: CONTESTED
  digital axis: ['Ruslan','Thief'] · anchor: Ruslan
  ANCHOR=Ruslan contradicts the claimed ['Thief'] — drawn on the glass
```

**The thief floods 150 fakes later:**
```
TITLE: Ruslan · CONFIDENCE: ANCHORED_CONFIRMED
  (the flood is late, weighting by earliness did not outweigh the owner's old records)
```

## Honest boundaries (no overclaim)

- Robustness is proven AGAINST: a flood of fakes, a full break-in of the digital
  axis, backdating, a one-axis mirror, a secret edit of the registry.
- It does NOT prove the truth of the content (SIGNED ≠ NATIVE), doesn't save from
  coercion (AD-28), doesn't protect POSSESSION (the thief holds the bytes but not
  the title).
- The irreducible residual: a thief who controls ALL channels + the absence of an
  early record in the registry → "eternal glass" (FO-005). And: genuinely early
  fakes planted in advance (expensive foresight).
- The network public anchor is not tested here (egress) — real publicness
  (Bitcoin/OTS) requires an environment with a network.

## BOTTOM LINE

**ROBUST within what was tested:** out of 500 attacks the thief did not get the
title once; every real break-in of the digital axis was caught by the independent
anchor; our hash matches the external openssl. The mechanism honestly knows its
boundaries (possession, coercion, eternal glass, the network anchor). This is a
prototype-principle with measured robustness, not a certified product.
