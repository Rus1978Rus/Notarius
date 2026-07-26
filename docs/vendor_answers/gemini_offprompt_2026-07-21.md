# Gemini — off-prompt answer (cross-material from MSL/MIP)

DATE: 2026-07-21
STATUS: NOT an answer to VENDOR_PROMPT_APPLICATIONS_RU — Gemini sent
an analysis of the "BOM inside a token" problem (cell BOM × BYTE_EXACT_TOKEN,
layer O1) from the author's adjacent MSL/MIP project. Kept because it is
directly applicable to the Notarius invisible-character scanner.

## Gist of Gemini's answer (5 ways to handle a BOM inside a token)

1. **Keep it MEDIUM/queue** — do not escalate; the review queue already
   guarantees the attack is not missed; 67% of BOM cases are harmless
   file-concatenation, and escalating to a hold would destroy trust in the
   system.
2. **Narrow lexical predicate** — escalate only if the BOM is wedged
   between two alphanumerics (`adm<BOM>in`), not at a paragraph
   boundary/after a period/after a line break. Expectation: TP 100%, FP <10%.
3. **Dictionary heuristic** — raise the level if the token without the BOM
   matches a critical word (admin, root). Gemini itself ranks this option
   last: it turns a structural witness into a "semantic
   antivirus."
4. **Weight in the queue, not escalation** — a suspicion_score pushes the
   incident to the top of the queue without false holds.
5. **X-ray projection (Gemini's top-ranked option)** — the machine does not
   decide at all: the interface shows the human the string with the byte
   made visible, `adm[U+FEFF]in` — the human eye instantly tells sabotage
   from the legitimate concatenation `paragraph[U+FEFF]Next`.

Gemini's recommendation: measure the FP of option 2 on realistic corpora;
if FP does not drop below 5% — adopt option 1 + invest in option 5.

## Carrying it over to Notarius (invisible-character scanner)

Directly applicable to `find_invisibles()` and the future input filter
for AI pipelines:

1. **Neighbor context** — the scanner must report not only the position and
   codepoint name but also the surroundings: an invisible character INSIDE a
   word (between alphanumerics) = high suspicion; at a block boundary =
   probable concatenation/service artifact. This sharply reduces the noise.
2. **X-ray report** — human-readable output of the form `adm[U+FEFF]in`
   (a visible projection of the invisible) instead of a plain position table.
   It fits perfectly with the Notarius principle "a break must be visible and
   explainable to a human."
3. **Advisory mode** — the scanner does not block, but sorts by
   suspiciousness (an echo of option 4) — matching the already-adopted
   principle of early Notarius, "advisory mode, no auto-block."
4. Lesson from the conveyor judging: the scanner must recognize legitimate
   invisible sequences (C2PA 2.3 embeds text manifests via Unicode variation
   selectors) and not flag them as an attack.

## Action

If Gemini is to be included in the applications survey — send it the
prompt docs/VENDOR_PROMPT_APPLICATIONS_EN.md and submit the answer.
