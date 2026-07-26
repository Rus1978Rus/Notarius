# NOTARIUS — Prompt for surveying other AI vendors

DATE: 2026-07-21
PURPOSE: a single brief for GPT / Gemini / Kimi / DeepSeek and any other
models — about the ways and places to apply Notarius. The answer format
matches the conveyor schema (Ideate/Verify), so vendor answers
can be merged with the results of the Claude conveyor and judged by the same judges.

INSTRUCTION: copy everything between the lines, in one message, into another AI.
Save the vendor's answer to the file `docs/vendor_answers/<vendor>_<date>.md`.

---

You are an independent expert reviewer. Answer IN RUSSIAN. Don't flatter,
evaluate strictly. This is a survey of several AI systems; your answers will be
compared with those of other models and checked by judges for
overlap with prior art — so honesty matters more than the number of ideas.

PROJECT CONTEXT.
Notarius is a research project (author: Ruslan Malyavskiy,
an independent researcher with no technical background, working solo,
with AI assistants). The gist: a provenance tracker at the level of the data
ELEMENT — where an element (a field, a paragraph, a quote, a fragment) came
from, what it passed through, native or inserted. Key formulas:
- SIGNED ≠ NATIVE (signed does not mean native)
- container integrity ≠ element provenance
- a break in the chain must be visible and explainable to a HUMAN

Confirmed niche (after a prior-art review, July 2026):
provenance portable across organizational boundaries at the level of a
field/fragment, with a human-readable report of the break, available
to the small user outside closed networks. The character of the niche is composition
of ready blocks (the W3C PROV vocabulary + in-toto chains + a
Sigstore/eIDAS anchor) + our own semantic layer and reports.

ALREADY CLOSED by other systems — do NOT propose such ideas:
- C2PA / Content Credentials: provenance of media and whole texts,
  embedded in the creation pipeline (cameras, editors, platforms);
- BEC antifraud (Trustmi and analogues): checking invoice payment details
  against the supplier's master data;
- OpenTimestamps / eIDAS / RFC 3161: proof of a document's existence
  at a point in time;
- in-toto / SLSA: software supply chains in CI/CD.

WHAT ALREADY EXISTS IN THE PROTOTYPE (Python, stdlib):
- a scanner for invisible Unicode characters (ZWSP, ZWJ, bidi overrides, etc.)
  with positions and codepoint names;
- a signed block envelope: canonical JSON + SHA-256 + HMAC,
  with a control length in codepoints as a diagnostic field
  (the report names the length shift and the position of the invisible insertion).

TASK. Propose EXACTLY 5 applications of Notarius in two areas
(at least 2 ideas per area) and, optionally, 1 idea from any other
area:
A) bloggers, authors, independent media, content creators;
B) people who work with AI: prompt engineers, editors of AI text,
   RAG developers, AI-agent operators, teachers.

FORMAT of each idea (strictly):
1. TITLE: short, in Russian.
2. AUDIENCE: a specific user and their specific pain.
3. MECHANISM: how it works specifically through ELEMENT-level provenance
   (not just signing a whole file).
4. WHY IT'S NOT CLOSED: honestly explain why C2PA / antifraud /
   timestamping / in-toto do not do this. If unsure —
   name the nearest existing analogue.
5. FIRST STEP: a minimal demo doable by one person in 1–2
   weeks with an AI assistant.
6. SELF-ASSESSMENT (1–5 each):
   NOVELTY (1 = closed by existing, 5 = genuinely open space),
   FEASIBILITY (1 = needs a team and years, 5 = solo demo in weeks),
   DEMAND (1 = nobody will use it, 5 = acute pain, users
   are reachable).

AT THE END: name one idea from the list that you would REJECT first,
and why — this is a check on your rigor.

---

## Where to file the answers

`docs/vendor_answers/` — one file per vendor. Then the answers are run
through the same conveyor judges (prior-art skeptic + viability
skeptic) and merged into a common ranking with the results of the
Claude conveyor.
