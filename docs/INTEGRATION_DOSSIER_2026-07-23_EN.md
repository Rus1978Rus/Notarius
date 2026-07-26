# Integration dossier: 5 standards → our modules

DATE: 2026-07-23
BASIS: AD-23 (adopt-don't-invent), AD-26/27 (key custody), the author's request
"take on FROST, secure enclave, OpenTimestamps, witness-cosigning,
Reed-Solomon." NOT a demo — a plan for real integration.
DISCIPLINE: LLM_GENERATED; the current state of the standards is checked against
2026 sources (links at the bottom), not from memory.

## Summary map

| Standard | Our module | What it closes | Effort | Maturity |
|---|---|---|---|---|
| OpenTimestamps / RFC 3161 | trace.py (`at`/`anchor`), carrier.py | self-declared time (№3), backdating (AD-24) | LOW | pip, ready |
| Reed-Solomon | carrier.py, human_fingerprint | carrier damage (E-Continuity/stone) | LOW | pip, ready |
| FIDO2 / passkey (enclave) | custody.py (one share) | silent copying of a share (AD-26) | MEDIUM | hardware |
| FROST (RFC 9591) | custody.py (replaces Shamir) | key assembly in memory (demo boundary) | HIGH | RFC+libs (not Python) |
| Witness cosigning | trace.py (`expected_head`) | fork/split-view (M4, AD-22) | HIGH | infra |

Recommended order: **the two LOW-effort items first** (time,
correction) — cheap, and they close real holes; then the enclave; FROST and
witness are the "serious tier" (they need libs in another language / external infra).

---

## 1. OpenTimestamps / RFC 3161 — trusted time (FIRST)

**What:** bind the hash of an event/carrier to external time.
- OpenTimestamps: anchor in Bitcoin, free, decentralized. Library:
  `opentimestamps-client` (PyPI). BOUNDARY: VERIFICATION needs a Bitcoin node
  (a pruned one works); the proof format is stable forever.
- RFC 3161: a trusted timestamp server (TSA). Libraries: `rfc3161-client`
  (Trail of Bits), `rfc3161ng`. Simpler, but you trust a single TSA.

**Point of contact:** `notarius/trace.py`, the `anchor` field (reserved in
AD-19, empty). After an event is signed — `stamp(sha256(canonical(event)))`
→ write the proof into `anchor`. `verify_trace` additionally checks the anchor.
Similarly the time field in `carrier.py`.

**What it closes:** defect №3 (time is self-declared); the AD-24 condition
"a record beyond the liar's control" (backdating impossible). Longevity —
RFC 4998 re-timestamp on top (AD-23).

**Candidly:** OTS proves "existed no later than T," not "created at T";
not "who" and not "the truth." Confirmation takes minutes-to-hours (a Bitcoin block).

---

## 2. Reed-Solomon — recovery from damage (SECOND)

**What:** error-correction codes: +t symbols → corrects loss up to t/2
(the Singleton optimum). Libraries: `reedsolo` (pure Python), `zfec`.

**Point of contact:** `notarius/carrier.py` — wrap the carrier in RS parity
→ it survives partial damage (a smudge on paper, a chip on stone).
QR ALREADY contains RS internally (up to ~30% loss) — a QR carrier gets this
for free; explicit RS is needed for non-QR carriers and for `redundant_id`
(reinforce the duplicates from human_fingerprint with real correction).

**What it closes:** physical damage to the carrier over time —
the "stone/deep time" axis of E-Continuity (Viking). It complements the "mortal
carrier" (AD-29): the mortal one carries the short-lived, the RS carrier — the long-lived.

**Candidly:** RS is about DATA RECOVERY, not about signing/authenticity;
it is an orthogonal layer (sign first, then wrap in RS).

---

## 3. FIDO2 / passkey — a share in a hardware anchor (THIRD)

**What:** a non-extractable key in the secure enclave of a phone/token; mass-market,
phishing-resistant. Libraries: `python-fido2` (Yubico) on the server (WebAuthn),
passkeys on the device. TPM 2.0 / HSM / Cloud KMS for server-side shares.

**Point of contact:** `notarius/custody.py` — one of the N shares is held not as
a Shamir point, but as a hardware participant: the device confirms
presence (a WebAuthn assertion) and takes part in signing. Stealing the share =
stealing the device = physics (AD-26 anchor axis).

**What it closes:** silent copying of a single share (it cannot be extracted from
the enclave). Kimi's pragmatic minimum: enclave phone = the 1st share.

**Candidly:** a WebAuthn assertion is not in itself a FROST share — the composition
"hardware confirms presence + releases/participates" requires
careful coupling with §4 (FROST). A real device is needed; it cannot be
emulated in Python.

---

## 4. FROST (RFC 9591) — a real threshold (CORE, replaces Shamir)

**What:** Flexible Round-Optimized Schnorr Threshold — a two-round
threshold signature. **The key is NOT assembled at any single point.** Ciphersuite
**FROST-ED25519** (edwards25519 + SHA-512). Libraries: Zcash Foundation
(Rust), bytemare (Go), TypeScript.

**Point of contact:** `notarius/custody.py` — replaces the Shamir stub.
CRITICALLY IMPORTANT: FROST-ED25519 produces an **ordinary Ed25519 signature**, the
same one our `envelope_v2` / `trace` verifies. So **the verification side
does not change at all** — only the signing changes (it becomes
threshold). This is the cleanest possible integration: the verify code stays as is.

**What it closes:** the demo boundary of custody.py "the seed is assembled in memory"
(GPT: "don't assemble it in memory on a single device") — FROST eliminates it by
construction. A fork requires compromising M participants.

**Candidly:** there is no mature pure-Python FROST; production means a Rust library via
FFI (PyO3) or a separate signing service. This is the heaviest item in
engineering terms, but the most fundamental (a real threshold, not a stub).

---

## 5. Witness cosigning — against forks (SERIOUS TIER)

**What:** external witnesses co-sign a log checkpoint, having verified a
consistency proof (RFC 6962); the client sees the co-signature → is confident it is
not being shown a split-view. Spec: **C2SP tlog-witness**; networks:
**ArmoredWitness**, transparency.dev. A witness stores O(1) (the last
checkpoint) and provides an O(log N) consistency proof.

**Point of contact:** `notarius/trace.py` — the trace becomes an append-only log
with a signed head; `expected_head` (added in AD-22) is taken from
the witnessed checkpoint. Then both truncation AND forks are detected
externally.

**What it closes:** the M4 fork/equivocation — the one honest hole
we recorded as uncovered (AD-22). "A single Merkle chain does not catch a
fork — witness cosigning does" (a direct quote from the source).

**Candidly:** it requires running/joining a transparency log +
a witness network — that is infrastructure, not a library. For "serious"
use (court, large sums), not for the pragmatic minimum.

---

## What changes in our modules (diff-level summary)

- `trace.py`: `anchor` ← OpenTimestamps proof; `expected_head` ← witness
  checkpoint. The verify logic is extended, not rewritten.
- `custody.py`: Shamir stub → FROST (the verify side is untouched);
  one share → FIDO2/enclave.
- `carrier.py`: RS wrapper for durable carriers; time ← OTS/TSA.
- `human_fingerprint.py`: `redundant_id` → real RS instead of simple
  duplicates.

## Priority for a real pilot (by Kimi + effort)

1. **OpenTimestamps** in trace/carrier — cheap, closes time+backdating.
2. **Reed-Solomon** in carrier — cheap, closes damage.
3. **FIDO2/passkey** — the 1st share in the enclave (pragmatic minimum).
4. **FROST** — when a real threshold is needed (replace the Shamir stub).
5. **Witness** — when a court/large sums are involved (close the fork).

## Honest overall boundary

No item requires new cryptography — only assembling what is ready.
But: (1) FROST and witness require code in another language / external infra —
not "pip install"; (2) the enclave requires hardware; (3) none of this
closes coercion (AD-28, the iron) — only silent theft. The integration
moves the prototype from "demo stubs" to "an assembly of proven
standards," but human validation is still absent.

## Sources

- FROST: [RFC 9591](https://www.rfc-editor.org/rfc/rfc9591.html), [Zcash FROST (Rust)](https://github.com/ZcashFoundation/frost), [bytemare/frost (Go)](https://github.com/bytemare/frost)
- Time: [opentimestamps-client (PyPI)](https://pypi.org/project/opentimestamps-client/), [rfc3161-client (Trail of Bits)](https://github.com/trailofbits/rfc3161-client), [rfc3161ng](https://github.com/trbs/rfc3161ng)
- Witness: [C2SP tlog-witness](https://github.com/C2SP/C2SP/blob/main/tlog-witness.md), [transparency.dev witness network](https://blog.transparency.dev/can-i-get-a-witness-network)
- Reed-Solomon: [reedsolo (PyPI)](https://pypi.org/project/reedsolo/), [zfec](https://github.com/tahoe-lafs/zfec)
- Enclave: [python-fido2 (Yubico)](https://github.com/Yubico/python-fido2), WebAuthn/FIDO2, TPM 2.0
