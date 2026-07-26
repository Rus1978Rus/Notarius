# Notarius Applications Conveyor — FINAL SUMMARY REPORT

DATE: 2026-07-22
SCOPE: applications of Notarius for (A) bloggers/authors and (B) people working with AI
SOURCES: 5 model families, each polled blind with a single prompt
(docs/VENDOR_PROMPT_APPLICATIONS_EN.md):
the internal Claude conveyor (Sonnet 5 + Opus 4.8, 6 participants),
Microsoft Copilot, DeepSeek, Qwen, Kimi. Plus cross-material from Gemini.
JUDGING: every idea gets 2 independent skeptics (prior-art + viability);
a REJECT from either judge knocks the idea out.

## FINAL SCORE

| Source | Ideas | STRONG | WEAK survivors | REJECT | Not judged |
|---|---|---|---|---|---|
| Claude conveyor | 20 | 0 | 1 | 18 | 1 |
| Copilot | 5 | 0 | 0 | 5 | 0 |
| DeepSeek | 5 | 0 | 1 | 4 | 0 |
| Qwen | 5 | 0 | 0 | 5 | 0 |
| Kimi | 5 | 0 | 0 | 5 | 0 |
| **TOTAL** | **40** | **0** | **2** | **37** | **1** |

**Headline result: zero STRONG out of forty ideas from five independent
model families.** This is not a failed poll — it is the most valuable
outcome possible: the space of "applying element-level provenance for
bloggers and AI workers" closed shut over 2024–2026 under existing
products, and closed tightly.

## The two survivors (both WEAK+WEAK, one cluster)

Both survivors are the same "citation anchor for journalists" niche
(Claude conveyor and DeepSeek arrived at it independently):
a chain of "quote in article ← source/transcript fragment ← original"
with an explainable break. The judges agreed: there is no literal
end-to-end-chain analogue (N3), but demand is weak (D2) — "a journalist
just publishes the audio recording, which is simpler and more convincing
than a hash chain," the audience won't pay, and the HMAC anchor is
self-signed. The judges' conditions for rescue: pivot to publishers /
fact-checking desks (they have money and process) and replace HMAC with
an external trusted anchor.

1 idea was left unjudged ("Element trace in an AI-agent chain," Opus) —
session limit. Candid caveat: its twin, "Field provenance in agent-to-agent
handoff," WAS judged and rejected (DeepMind's CaMeL already does taint-tracking
of value origin; observability writes per-element traces), so the expectation
for the unjudged one is also REJECT.

## Who closed the space (map of the winners)

- **Grammarly Authorship** (2024, free, Google Docs/Word) —
  cited by the judges in 9 write-ups: per-fragment process provenance
  "typed/pasted/AI/AI-edited" with replay and report. Killed the whole
  "human vs AI by fragment" cluster.
- **C2PA 2.3** (Dec. 2025) — text manifests via Unicode
  variation selectors, surviving copy-paste. Killed the "C2PA can't
  handle text" cluster.
- **LLM Guard (InvisibleText), OWASP RAG Security Cheat Sheet, Lakera,
  Prompt Shields, promptfoo** — detecting invisible characters in
  LLM pipelines is a commodity; OWASP officially recommends exactly our
  mechanism (SHA-256 of chunks + scan for invisibles). Killed the
  "Unicode filters for AI" cluster.
- **LangSmith/Langfuse/Arize + Citations API (Anthropic)/Cohere
  grounding + Azure Groundedness** — killed the RAG-provenance cluster.
- **Agent Receipts, Attested Intelligence, Pipelock, CaMeL** — killed
  the "agent journal" cluster.
- **Originality.ai Writer Replay, Turnitin Clarity, GPTZero** — killed
  the "text intake" cluster.
- **StegCloak, Tynt (2010!), zero-width fingerprinting (2017)** — killed
  the "invisible marks against copying" cluster (with the cause of death
  already recorded back in 2010: scrapers take the RSS feed, not Ctrl+C).

## CATALOG OF STRUCTURAL DEFECTS (the conveyor's main haul)

Seven defects that recurred across every source. This is a checklist for
vetting ANY future Notarius idea before it goes through the conveyor:

1. **Self-attestation.** The mark/signature is placed by the interested
   party — this proves the journal is internally consistent, not that the
   content is genuine. Catches only the honest.
2. **HMAC is symmetric.** A shared key = either party can forge the
   other's "signature." Proves nothing to a third party.
   v2 requirement: Ed25519 + an external trusted timestamp.
3. **SIGNED ≠ NATIVE cuts our own way.** A signature at a checkpoint
   proves existence, not authorship: anything inserted BEFORE the first
   checkpoint gets a perfect history.
4. **Cold start.** If the party who must sign has no incentive to
   (a student, a publisher, a quote's source), the scheme is dead.
5. **Pipeline normalization.** A CMS/typography breaks per-fragment
   hashes → a storm of false positives; after canonicalization the
   comparison degenerates into a diff.
6. **Reduction to a diff.** If the user controls both the reference and
   the check, cryptography adds nothing over a free diff.
7. **Marks don't survive the pipeline.** Invisible marks die on
   re-typesetting/sanitizers; data dies in layout. Provenance is
   portable only where the pipeline cooperates.

## WHAT THIS MEANS FOR NOTARIUS (auditor's conclusions)

1. **The project's formulas proved themselves AS A FILTER.** SIGNED ≠ NATIVE
   and "integrity ≠ origin" took down other people's ideas in every round.
   Project discipline (the conveyor, honest limits) worked exactly as
   designed: 40 ideas vetted before a single month of development was
   spent on any of them. The cost of vetting: hours.
2. **The poll covered only bloggers and AI workers.** Direction AD-8
   (critical fields in small-business documents) was NOT tested by ideas
   in this poll and NOT disproven. Of all known directions it remains the
   one least contradicted by the facts — but now it has to be run through
   the same conveyor with the defect catalog in mind (especially #1, #2, #6).
3. **The prototype's role changes.** The demo set (witness + scanner +
   envelope + negative tests) is valuable not as a product but as a
   research/teaching asset: an executable demonstration of where the naive
   barrier ends and the need for trusted infrastructure begins.
4. **If you are looking for a product** — the judges left one door open:
   the "citation anchor" cluster, pivoted to publishers / fact-checking
   desks with an external trusted anchor. Demand is unproven; before any
   development, interview 3–5 real fact-checkers/newsrooms.

## Outcome (AUTHOR_DECISION AD-9, 2026-07-22)

**Author's decision: RESEARCH TRACK.** Notarius proceeds as open research
(methodology, filter-formulas, demo set, defect catalog); the product
search is paused. Held in reserve: direction AD-8 (small business, not
disproven) and the "citation anchor" cluster (with the judges' conditions).
Full record: docs/AUTHOR_DECISIONS.md, AD-9.

## References

- Per-source verdicts: copilot_verdicts_2026-07-21.md,
  kimi_verdicts_2026-07-21.md; full logs — wf_b08440c3-881,
  wf_2c2eb281-bd9, wf_6da04178-8fb, wf_5eee9205-c90, wf_3fa59459-a97.
- Vendor answers: docs/vendor_answers/.
- Gemini cross-material for the scanner: gemini_offprompt_2026-07-21.md.
