# Judges' verdicts: Kimi's ideas (Moonshot AI)

DATE: 2026-07-21
JUDGES: 2 skeptics per idea (prior-art + viability)
RESULT: **0 of 5 passed** — all rejected by at least one judge,
despite Kimi being the only one that checked prior art via web search.

| # | Idea | Verdicts | N | F | D |
|---|------|----------|---|---|---|
| 1 | Intake (contractual text provenance) | REJECT + REJECT | 2 | 4 | 2 |
| 2 | Your own trace (invisible marks against aggregators) | REJECT + WEAK | 1.5 | 4.5 | 2 |
| 3 | The human layer (edits to AI text) | REJECT + WEAK | 2 | 3.5 | 2 |
| 4 | Grounding a RAG answer | REJECT + REJECT (matched the vendor's own recusal) | 1.5 | 2.5 | 2 |
| 5 | Agent journal | REJECT + WEAK | 2 | 3.5 | 2 |

## Prior art that even Kimi didn't find

- #1: **Originality.ai Writer Replay** (keystroke-level replay, marketed
  specifically at businesses with freelancers), **Turnitin Clarity**
  (draft checkpoints + playback), Grammarly Authorship.
- #2: **StegCloak** (KuroLabs, open source: zero-width watermarks with
  password/AES/HMAC), Aissan's zero-width fingerprinting (2017),
  **Tynt Tracer** — productized "blogger vs re-posting" back in
  2010 ($3.9M Series A) — and the cause of death recorded even then:
  scrapers take the RSS/HTML, not Ctrl+C.
- #3: Grammarly Authorship + Turnitin Clarity already produce an
  "AI/pasted/human" report; C2PA text-provenance via variation
  selectors survives copy-paste (Kimi's claim disproven).
- #5: **Agent Receipts** (Ed25519 receipts as W3C Verifiable
  Credentials), **Attested Intelligence** (signed receipts for every
  MCP call, patent application Dec. 2025), Pipelock
  ("verifiable offline by any third party" — word for word),
  Signet, arXiv "Notarized Agents." Agent receipts are becoming a
  framework commodity.

## Two structural defects that recurred across every idea

1. **Self-attestation by the interested party.** The signature is placed
   by whoever benefits from the result (a consultant on his own journal,
   an editor on his own declaration, a freelancer on his own checkpoints).
   This proves the internal consistency of the records, but not their
   genuineness. This is now the third round of judging running into the
   same wall: without an external trusted anchor (an independent log, a
   second signature, a TEE), "portable proof" does not port.
2. **SIGNED ≠ NATIVE hits the ideas themselves.** A signature at a
   checkpoint proves existence at a point in time, not authorship:
   AI text inserted BEFORE the first checkpoint gets a "perfect
   history." The project's own formula refutes half the candidates —
   which confirms its value as a filter.

## Significance for the summary report

Kimi gave the most honest answer — and still scored 0/5. This is not a
failure of Kimi's but a calibration: the provenance-tooling market over
2024–2026 closed faster than even web-search-equipped models can update.
Surviving directions must be sought not in "new products" but in
(a) composition for a specific paying user and
(b) places where the attacker does not control the verifying party
(input filters).
