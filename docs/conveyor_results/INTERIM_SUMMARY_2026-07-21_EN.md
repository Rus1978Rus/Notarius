# Notarius Applications Conveyor — interim summary

DATE: 2026-07-21
STATUS: PARTIAL — the session limit cut judging off midway;
unjudged ideas are marked PENDING and get finished on a re-run
(the conveyor cache retains verdicts already produced).

## Work completed

| Idea source | Ideas | Judging |
|---|---|---|
| Internal conveyor (6 participants Sonnet/Opus, blind) | 20 unique (from ~30 raw) | 3 judged, ~10 PENDING |
| Copilot | 5 | 5/5 judged |
| DeepSeek | 5 | 3/5 judged, #4 #5 PENDING |
| Qwen | 5 | 1/5 judged, #2–#5 PENDING |
| Gemini | — (answer off-prompt, see below) | — |

Judges: pairs of skeptics (prior-art + viability) per idea,
a REJECT from either judge knocks the idea out.

## Verdicts delivered

**REJECT (out):**
- Copilot #1–#5 — all five. Reasons: Grammarly Authorship (per-fragment
  "human/AI" attribution has existed since 2024), C2PA 2.3 text manifests,
  Anthropic Citations API / Cohere grounded generation (span-level RAG
  citations are mainstream), CLM platforms Ironclad/Juro (clause-level audit
  trail), Web Annotation/Hypothes.is/archive.today (quotes and snapshots).
- DeepSeek #2 (guest post) — sanitizable/redactable signatures
  (academia since 2005), XML-DSig, Google Docs version history; the vendor
  itself also rejected it.
- DeepSeek #3 (RAG provenance for a regulator) — already taken: academia
  (Proof-Carrying Answers ACSAC 2025, ProvenAI, RAG Sign, ZKPROV) and
  commercial (EQTY Lab for the EU AI Act). Plus a fundamental hole: the
  "claim→chunk" link is a heuristic, LLM inference is unsignable;
  SIGNED ≠ DERIVED.
- Qwen #1 (silent tampering in publications) — reduces to a diff against
  your own copy; CMS typography normalization would cause a storm of false
  positives; changedetection.io/Visualping exist.

**Survived (both judges WEAK — no enthusiasm):**
- DeepSeek #1 "Direct speech under the microscope" (quote ← transcript ←
  audio): no literal end-to-end-chain analogue, but Trint +
  ProofMode cover pieces of it, demand is weak (D2).
- Internal conveyor: "Source-quote anchor" — same niche, same judges'
  conclusion: a fresh fragment = a diff of the quote through editing, but
  a self-signed HMAC anchor proves nothing to a third party.

**PENDING (not judged due to the limit):**
- Qwen #3 "RAG context-poisoning auditor" (invisible characters in
  chunks) — the least-covered candidate pre-judging.
- Qwen #4 (AI vs human + detector evasion), Qwen #5 (tampering with
  contract terms), Qwen #2 (clean quote; the vendor itself rejected it).
- DeepSeek #4 "Prompt detective," #5 "Reviews auditor."
- ~10 internal-conveyor ideas (including "RAG chunk provenance,"
  "Origin journal of human+AI paragraphs," "Forensics of prompt assembly
  by an AI-agent operator").

## Cross-cutting judging lessons (more important than individual verdicts)

1. **The prototype's HMAC architecture proves nothing to a third party.**
   A symmetric key = both parties can forge each other's "signature";
   this is self-declaration. The judges repeated this in EVERY write-up.
   → PROTOTYPE V2 REQUIREMENT: asymmetric signature (Ed25519) +
   an external trusted timestamp. HMAC stays for the demo only.
2. **C2PA 2.3 embeds text manifests via Unicode variation
   selectors** — the very "invisible characters" channel our scanner
   treats as a threat, the standard uses legitimately.
   → The scanner must distinguish a C2PA manifest from a malicious
   insertion, or it will false-positive on legitimate content.
3. **Pipeline normalization (CMS, typography)** breaks naive
   per-fragment hashes → without canonicalization any "tampering
   detector" drowns in false alarms. (This confirms decision AD-4 to defer
   the normalization question to the threat model — the threat model must
   account for it.)
4. **Cold start** — ideas requiring the OTHER party to sign elements in
   advance are non-viable for a solo launch. The live candidates are
   one-sided tools (the user controls both the reference and the check).
5. **The most robust uncovered line** (not yet judged, but no judge laid
   a finger on it): detecting invisible Unicode insertions as an INPUT
   FILTER for AI pipelines (RAG-base poisoning, hidden prompt
   injections). Here the canary works in its original role — the attacker
   does not control the recipient's counter.

## Gemini — off the conveyor, but useful

Gemini's answer turned out to be off-prompt (an analysis of "BOM inside a
token" from the MSL/MIP project). Kept as cross-material: its "Variant 5 —
X-ray projection of adm[U+FEFF]in" and "Variant 2 — BOM between
alphanumerics = suspicion, BOM at a paragraph boundary = a splice" are
ready-made improvements for our invisible-character scanner (fewer false
positives + visualization for a human). See
docs/vendor_answers/gemini_offprompt_2026-07-21.md.

## Next steps

1. Judge the PENDING ideas after the limit resets (re-running the
   conveyors — finished verdicts come from the cache).
2. Compile the final ranking and take it to AUTHOR_DECISION.
3. Add the Ed25519+timestamp requirement to the prototype v2 plan.
