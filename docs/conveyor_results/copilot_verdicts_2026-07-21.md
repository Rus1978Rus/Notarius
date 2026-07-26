# Judges' verdicts: Copilot's ideas

DATE: 2026-07-21
JUDGES: 2 skeptics per idea (prior-art + viability), Claude conveyor
RESULT: **0 of 5 passed** — every idea rejected by at least one judge.

| # | Idea | Verdicts | N | F | D |
|---|------|----------|---|---|---|
| 1 | Fragment-level authorship attribute | REJECT + REJECT | 2 | 4.5 | 2 |
| 2 | Public citation checklist | REJECT + WEAK | 2 | 4.5 | 2 |
| 3 | Prompt-origin indicator | REJECT + REJECT | 1.5 | 3.5 | 2.5 |
| 4 | Per-fragment report of RAG sources | REJECT (prior-art) | 2 | 3 | 2 |
| 5 | Legal fragment-doc | REJECT + REJECT | ~2.5 | ~2.5 | 2 |

## Key reasons for rejection (important for the whole project)

1. **Grammarly Authorship (since August 2024)** — already does per-fragment
   attribution "typed / pasted / AI-generated / AI-edited"
   with a human-readable report. Closes ideas #1 and #3.
2. **C2PA 2.3 (A.7, Jan. 2026)** — embeds manifests in
   unstructured text via Unicode variation selectors; Encypher
   commercializes it. The claim "C2PA doesn't work with text" is out of date.
3. **Anthropic Citations API (Jan. 2025), Cohere grounded generation,
   RAGAS** — span → document → source fragment is already mainstream RAG.
   Closes idea #4 as Copilot framed it.
4. **CLM platforms (Ironclad, Juro)** — clause-level audit trail of "who
   changed what" is a basic feature of the category. Closes idea #5.
5. **Structural critique that hits our prototype too:**
   **HMAC is a symmetric primitive.** A shared key means either party
   can forge the other's "signature"; HMAC proves nothing to a
   third party — it is only self-declaration. Proving authorship across
   an organizational boundary requires an asymmetric signature (Ed25519) +
   a trusted timestamp. → ADD TO THE PROTOTYPE PLAN.
6. **The cold-start problem** (echoing Qwen): the sender must sign
   elements BEFORE handoff; most audiences have no motivation to.

## What follows from this (for the summary report)

- Rejecting Copilot's ideas ≠ death of the directions: the judges hit the
  framings "as claimed," where the vendor underestimated prior art.
- Live remnants per the judges: the invisible-Unicode-insertion scanner
  ("a feature, not a product" — but a real feature) and a human-readable
  layer on top of existing mechanisms.
- Full verdict texts: conveyor log wf_2c2eb281-bd9.
