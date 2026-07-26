# Build plan for the key custody perimeter

DATE: 2026-07-23
BASIS: AD-26 (summary of 7 sources) + AD-23 (adopt-don't-invent).
GOAL: a signing key where theft is physical, visible, and temporary. Everything
from ready standards; we write no cryptography of our own.
DEMO: notarius/custody.py + tests/test_custody.py (9 tests) — the core of the
architecture (threshold + heartbeat + expiry) is executable.

## The perimeter (4 layers, each closing its own axis from AD-26)

```
LAYER 1  THRESHOLD M-of-N       → no single point (a stolen share = zero)
LAYER 2  MORTAL HEARTBEAT        → a copy dies without the owner's heartbeat
LAYER 3  HARDWARE ANCHOR         → the share is unextractable (secure enclave)
LAYER 4  EXTERNAL TIMESTAMP      → time can't be forged (fork/backdate)
```

## Build stages (solo researcher → production)

### Stage 0. Threat model and spec (before code)
- Parameters: M, N, epoch length, heartbeat window, who holds the shares
  (people/devices/services), geography, channel.
- Recovery ceremony on key death (a quorum reassembles).
- Output: a 1-page threat model. STANDARD: NIST SP 800-57 (key management) as a
  checklist.

### Stage 1. Threshold M-of-N  ✅ DEMO READY
- NOW (demo): notarius/custody.py — Shamir split of the seed, M-of-N, expiry by
  epochs. BOUNDARY: the seed is reassembled in memory at signing time.
- PRODUCTION: **FROST** (threshold Schnorr, CFRG draft) or **threshold-Ed25519**
  — the key is NOT reassembled at any point, and the output is an ordinary single
  signature. Libraries: ZF FROST (Rust), frost-ed25519. This is how custodians
  work (Fireblocks, Coinbase MPC).
- Demo achievement: a share / M-1 shares = zero (tests).

### Stage 2. Mortal heartbeat  ✅ DEMO READY
- NOW: heartbeat()/tick() — without a heartbeat longer than the window the key is
  DEAD, signing is impossible even with M shares; old shares expire.
- PRODUCTION: **proactive secret sharing** (Herzberg 1995) — shares are re-dealt
  every epoch WITHOUT revealing the secret (in the demo the refresh is dealer-
  based). The heartbeat = a signed heartbeat from the owner's hardware anchor
  (Stage 3). A hierarchy of windows for availability (hospital/expedition).
- Demo achievement: "a copy inherits mortality" (test).

### Stage 3. Hardware anchor (real hardware)
- The MASS-MARKET answer: **passkeys / FIDO2 / WebAuthn** — the key in the secure
  enclave of a phone/laptop, unextractable, phishing-resistant. Theft = device
  theft = physics. This is ready infrastructure (Apple/Google/1Password).
- Server: **TPM 2.0 / HSM / Cloud KMS** for server-side shares.
- Solo demo: WebAuthn integration (browser) as one of the N shares.
- BOUNDARY: not emulated in Python; this is the point of integration with
  hardware.

### Stage 4. External timestamp anchor
- Bind every event/signature to external time → fork and backdate are closed
  (AD-22, AD-24).
- STANDARD: **OpenTimestamps** (Bitcoin, free) or **RFC 3161 TSA**. Python:
  opentimestamps-client. The `anchor` field in trace.py is the joint.
- Longevity: **RFC 4998** re-timestamp (AD-23) — a re-signing ritual before the
  algorithm ages.

### Stage 5. Recovery ceremony
- The key's death (no heartbeat) is not a loss but a transition: a live quorum
  (M-of-N holders) assembles a new epoch.
- STANDARD: custodian shard-recovery practices; social recovery (as in Argent/
  Safe wallets).

## What is already proven by code (the demo)

| Property | Test |
|---|---|
| M-of-N signature is valid | test_m_shares_sign_and_verify |
| M-1 and a single share are useless | test_m_minus_1_fails, test_single_share_is_useless |
| Stolen old shares expire | test_stolen_old_shares_die_after_refresh |
| No heartbeat → key dead, copies too | test_no_heartbeat_kills_key |
| A dead key issues no shares | test_dead_key_issues_no_shares |

## The joint with the Notarius core

The perimeter signs the events of the semantic trace (trace.py):
```
element event → threshold signature of the perimeter (custody) →
  external timestamp (anchor) → the trace chain
```
Then AD-24 "a signed lie = evidence" gets all three conditions: key↔identity
(enclave), a record outside the liar's control (timestamp), and, on top, the key
can't be stolen quietly (threshold + heartbeat).

## The pragmatic minimum (Kimi) — what to build FIRST

For a real pilot, at minimum:
1. The key in the phone's secure enclave (passkey) — 1 share, unextractable.
2. A server share with heartbeat/attestation — the 2nd share.
3. A 2-of-2 threshold (phone + server) to start, accounting on the server.
4. OpenTimestamps on every signature.
Phone theft = physics (noticeable); server theft without the phone = zero;
heartbeat silence = freeze. All with ready components, without our own
cryptography.

## Honest boundaries

- The custody.py demo reassembles the seed in memory (FROST does not; marked).
- The demo refresh is dealer-based (production — proactive SS without a dealer).
- Coercion of the owner under pressure (rubber-hose, "thermorectal cryptanalysis,"
  xkcd 538) is closed by NO scheme — AD-28. The perimeter protects against QUIET
  theft, not against LOUD (a thief standing next to you with a hot iron). It is
  only deterred: distribution across jurisdictions (N crews in N countries at once
  = visible war), a negative quorum (under torture — an alarm, not the key), a
  duress code (a fake opening + a call for help). No answer saves the person — it
  only keeps the key from the thief. Do NOT sell the perimeter as "unbreakable."
- Pole ideas (quantum/bio/destruction) are NOT part of the plan — unattainable;
  here only what is buildable from ready standards.
