# Signing, identification, and confirmation algorithms — a catalog

DATE: 2026-07-22
BASIS: the author's request — "options for signing and identifying segments of
information, or information as a whole, on different carriers + ways to confirm;
look for non-standard solutions."
CONNECTION: E-Continuity (carrier across time) → MSL/MIP (a mark on stone) →
Notarius (element provenance). DISCIPLINE: LLM_OUTPUT ≠ VERIFIED_COPY; honest
statuses; executable demos are marked.

## Three axes of the problem

```
WHAT we sign:        SEGMENT ↔ WHOLE
ON WHAT:             digital / paper / stone / film / DNA / metal
WHO confirms:        software with a key / a human without software / the carrier itself
```

The central principle (from E-Continuity): **a signature is useless if the
verifier cannot run the algorithm.** Hence the split below into
"machine-verifiable" and "human/carrier-verifiable."

---

## A. SEGMENT or WHOLE (machine verification)

| Method | Segment/Whole | Confirmation | Status |
|---|---|---|---|
| SHA-256 | whole | recompute + compare | standard |
| HMAC | whole | shared key (symmetric — not for a third party) | v1 prototype |
| Ed25519 | whole | public key, anyone | v2 prototype |
| **Merkle root + inclusion proof** | **both** | O(log n) proof per segment | **demo: algorithms/merkle_segments.py** |
| Vector commitment / Verkle | segment | O(1) proof (2025, Reckle/Verkle) | prior art, not built |
| Redactable signatures | segment | the whole's signature survives removing a segment | prior art (Johnson 2002) |
| Aggregate (BLS) | many→one | one signature over N segments | prior art, not built |

**The key answer to the request:** Merkle removes the false dilemma "signing
every segment is expensive / signing only the whole means you can't reference a
segment." ONE root is signed (the identity of the whole), and the membership of
ANY segment is proven by a short proof — **without revealing or possessing the
other segments**. Verified by test test_proof_without_other_segments. External
use: MerkleSpeech (2026) — chunk-localised speech provenance via Merkle
commitments — exactly this pattern in production.

## B. Human-verifiable (without software, for deep time) — NON-STANDARD

| Method | Idea | Confirmation | Status |
|---|---|---|---|
| **Word fingerprint** | hash → short words | a human compares the words on stone vs screen vs voice | **demo: algorithms/human_fingerprint.py** |
| Visual hash (identicon) | hash → mosaic/pattern | the eye compares the picture on two carriers | prior art (hash-viz), not built |
| **mod-97 / redundant ID** | check digit + duplicates | computed BY HAND; survives partial damage | **demo: human_fingerprint.py** |
| Check digit (Luhn/ISBN/IBAN) | a number's self-check | manual computation | standard |

Rationale for B: the PGP word list and visual hash are real practice for humans
verifying keys across carrier boundaries (screen↔printed card↔voice). This is a
direct tool for the MSL/MIP scenario "will a descendant be able to read it": a
word fingerprint survives the loss of software, and words are readable and
pronounceable. The boundary (no overclaim): N words ≈ 6·N bits — protection
against accidental divergence and a convenient check, NOT full resistance to
brute force.

## C. The carrier confirms itself (substrate-as-detector) — NON-STANDARD

From the E-Continuity FO-canon "the best systems are those where the substrate
itself records tampering" (§7 NOTARIUS):

| Method | Carrier | Mechanism | Status |
|---|---|---|---|
| PUF (physically unclonable function) | silicon, paper, optics | random microvariations = an unclonable fingerprint; opening changes it | prior art (industrial), not built |
| Random paper/fiber pattern | paper | scan of the unique pattern as an ID (banknotes, 1980s) | prior art |
| Punch card | cardboard | hole present/absent, forgery is physically visible (§14) | historical |
| Wax seal | wax | opening destroys it | historical |
| Serial number in the substrate | banknote | ID on both torn halves → provenance survives the tear (§13) | historical |
| Length-witness / canary | digital/text | an extra code point is visible from the shifted count | Notarius §6.3 |

## D. Recoverability under damage (not a signature — but confirmation survives)

| Method | Idea | Status |
|---|---|---|
| Reed-Solomon | +t check symbols → corrects t/2 errors; optimal (Singleton) | prior art, for archives |
| Redundant ID (duplicates) | k copies of ID+check; one survives | demo: human_fingerprint.py |
| Fountain/erasure codes | recovery from any k of n parts | prior art, not built |

## E. Exotic (honestly marked as speculative)

| Method | Idea | Status |
|---|---|---|
| DNA steganography | a signature/message in junk DNA, extraction by PCR + sequencing | research (MDPI 2021/2025) |
| Acrostic / positional signature | a signature in the first letters/positions of characters | linguistic stego |
| Parallel carrier (Rosetta) | one content in N scripts → mutual cross-check | historical principle |
| MSL/MIP bracket grammar | `(word)`/`[sentence]` — a boundary as a self-describing ID | genesis candidate (AD-16) |

## The "carrier × verifier" map (a non-standard conclusion)

```
                 software+key   human without software   carrier itself
digital          Ed25519        word-fingerprint         length-witness
paper            —              mod97+duplicates          PUF/fiber pattern
stone/tablet     — (no software) word-fingerprint,       punch principle,
                                  bracket (MSL/MIP)        carving-visible
```
The diagonal "stone × human without software" is the very E-Continuity zone
where standard cryptography does not work, and where the non-standard methods
live: word fingerprint, self-checking ID, self-describing boundary (the
bracket). This is the answer to "different carriers."

## What is built (FO-035: the mechanism = the object, not the description)

- `algorithms/merkle_segments.py` — signing the whole + proof of any segment
  without the rest. Tests: the segment is confirmed, tampering breaks it, the
  identity of the whole changes from any segment.
- `algorithms/human_fingerprint.py` — word fingerprint (verification across
  carriers), mod-97 self-check, redundant ID (survives the loss of 2 of 3 copies,
  catches ID substitution).
- `tests/test_algorithms.py` — 14 tests.

## Honest boundaries (project discipline)

- Merkle / word-fingerprint / redundant-ID are IDENTIFICATION and confirmation of
  INTEGRITY, not proof of truth (`SIGNED ≠ TRUE`, AD-10).
- The human-verifiable forms are truncated → protection against accidental
  divergence, not against motivated brute force. For strength — a full signature.
- Physical/exotic methods (PUF, DNA) are prior art / speculation, NOT
  implemented; marked by status, not passed off as ready.
- All of this is input for AUTHOR_DECISION on what to take into the core.

## Sources

- Merkle/segments: [Reckle Trees (CCS 2024)](https://dl.acm.org/doi/10.1145/3658644.3670354), [MerkleSpeech (2026)](https://arxiv.org/pdf/2602.10166), [IETF COSE Merkle proofs](https://datatracker.ietf.org/doc/draft-ietf-cose-merkle-tree-proofs/), [Redactable signatures (IACR 2022)](https://eprint.iacr.org/2022/1485.pdf)
- Human-verifiable: [Human Distinguishable Visual Key Fingerprints (USENIX 2020)](https://www.usenix.org/system/files/sec20summer_azimpourkivi_prepub.pdf), [Word-based Key Fingerprints](https://arxiv.org/pdf/2106.01131), [Hash visualization](https://fietkau.science/hash_visualization_password_validation)
- Carrier: [PUF state of the art (arXiv 2024)](https://arxiv.org/pdf/2402.09386), [Physical unclonable functions (Nature Electronics)](https://www.nature.com/articles/s41928-020-0372-5)
- Recoverability: [Reed-Solomon for archival (OSTI)](https://www.osti.gov/servlets/purl/1121988), [pure-python reedsolomon](https://github.com/tomerfiliba-org/reedsolomon)
- Exotic: [DNA steganography (MDPI 2021)](https://www.mdpi.com/2078-2489/12/6/253), [Steganography+DNA framework (MDPI 2025)](https://www.mdpi.com/2079-8954/13/5/341)
