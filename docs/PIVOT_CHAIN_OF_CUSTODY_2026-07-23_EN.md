# PIVOT INTO A VERTICAL: chain-of-custody for NON-code

DATE: 2026-07-23. STATUS: LLM_GENERATED. BASIS: the AD-57 recommendation (§2 —
pivot out of the red ocean of code supply chains into a vertical where the code
stack is not present). The market part is GROUNDED in a 2025-2026 web search (links
at the bottom), not from memory. DISCIPLINE: honest boundaries; "the field isn't empty ≠
hopeless," but also "not a blue ocean." Positioning — as in AD-58:
meaning on top, crypto under the hood.

---

## 0. Why this document

AD-57 closed code supply chains as a red ocean and advised pivoting
into **chain-of-custody for NON-code** (legal/forensics/finance), where our GENERAL
model (title/anchor/reconcile/diagnose) does not compete with the code giants
(Sigstore/TUF/SLSA). This document tests that advice against live sources —
**before building**, with the same cheap "no/yes before construction."

## 1. What the check showed (candidly, with figures)

**The field is big AND occupied — it is NOT an empty clearing.**

- Digital evidence management market: ~$8.63B (2024) → ~$21.5B (2032),
  CAGR ~12%. Digital forensics: ~$13.8B (2025) → ~$35B (2032).
- Top incumbents: **OpenText, Cellebrite, Magnet Forensics, Exterro, MSAB**
  (~38% of 2025 revenue), plus Motorola, Tyler Technologies, Veritone.
- The driver is law enforcement (41% share): body-cam, dashcam, mobile forensics.

**Conclusion №1 (sober):** law-enforcement forensics is also a red ocean,
with its own giants. Entering there as a startup = a second Sigstore, only in
uniform. We do NOT go in head-on.

## 2. WHAT exactly the incumbents do — and what they do NOT do

| Their strength | What it is | Their boundary |
|---|---|---|
| Acquisition (Cellebrite/MSAB) | pull data off a device "forensically sound" | this is the GRAB, not the history after |
| Management (OpenText/Exterro/Tyler) | case storage, access, workflow, an audit log of WHO-touched | guards WHERE + the access log |
| Blockchain-CoC (academia, growing) | hash/timestamp anchor = was-at-moment-T | **tamper-DETECTION: yes/no** |

None of them provides what we provide:

- **tamper-LOCALIZATION** — not "touched/not," but *what exactly* changed
  (value substitution / insertion of an invisible / loss of a piece / rewritten) —
  our diagnose.py;
- **an honest aggregated verdict** over HETEROGENEOUS independent
  witnesses — CONFIRMED / CONTESTED / PROVISIONAL + "why" — our
  resolve_full;
- **protection against the mirror** (glass vs registry reconcile) — anything drawn onto
  the delivery "glass" is exposed by reconciling with an independent anchor;
- **substrate-independence (FO-013)** — the model works on ANY element
  (document, record, data, media), not only on a file-of-evidence.

## 3. OUR narrow but real edge

Blockchain-CoC answers "the file existed at moment T" — and that's the end of it:
the sources honestly note that it **records existence, but has NO
standardized legal recognition** in most jurisdictions; courts
require frameworks like **eIDAS**. A precedent exists (Marseille, March 2025:
a blockchain timestamp accepted as proof of authorship of a design) — but only
when the evidence passes an authentication and integrity procedure.

**Our edge lands exactly in this gap:** the court needs not "yes/no touched," but
**a finger pointed at WHAT changed and the integrity of heterogeneous
testimony protected in human words**. Management stores and logs; the anchor
gives "was-at-T"; **nobody gives localization + an honest summary verdict**. That is
our diagnose + resolve_full + reconcile.

**BUT candidly (as in AD-57): this is the edge of a FEATURE, not a moat.** It is narrow.
Its value is real where heavy forensic suites are overkill.

## 4. Where we do NOT compete with the giants (ranking of sub-verticals)

The giants sit in law-enforcement + enterprise forensics. Past them:

1. **Document/IP provenance and inter-organizational transfer** (NOT uniforms):
   a contract/report/dataset travels between parties; the question is not "where is it locked," but
   "is this the same thing the counterparty sent, and what changed." A heavy
   forensic suite is overkill here; our lightweight history engine — just right. **Best
   fit.**
2. **Financial/audit trail** — the chain of "who changed what in a record";
   localization of the edit + a summary verdict have direct value, forensic
   acquisition is not needed.
3. **Forensics/law enforcement** — the strongest demand, but the densest incumbents;
   realistic only as an EMBEDDED diagnostic layer UNDER their management,
   not as a replacement. Not the first entry.

## 5. Product form (consistent with AD-58)

Not a "box for everything," but an **engine of honest history** + an honest verdict:
- ours: trace + signature/identification + localization of the substitution + a human-readable
  breakdown (CONFIRMED/CONTESTED/FORGED-where);
- the buyer's: the doors — how to embed it into their process (case system, audit
  platform, DMS). Whoever buys writes the industry wrapper.

As an add-on/layer, not a second Cellebrite.

## 6. Honest boundaries (what we do NOT promise)

- We do not replace forensic acquisition and do not guarantee legal admissibility —
  that is eIDAS/jurisdiction, not us (`INTERFACE ≠ REALITY`, FO-005).
- "the trace finds the lie ≠ the trace proves the truth": we show WHERE the substitution is, not
  the sanctity of the rest.
- `SIGNED ≠ NATIVE`, `sealed ≠ authentic inside` — carry over here without
  change.
- Reconcile is strong exactly to the degree that the anchor is independent AND the consumer
  actually reconciles.
- The field is big, but with giants: without a real design partner who
  FEELS the pain of "show me what exactly was substituted," this is research again.

## 7. Strategic verdict

**The pivot is justified, but with a correction to AD-57.** The advice "non-code chain-of-
custody" is right in direction, BUT the field turned out not to be empty: forensics/
law enforcement is a red ocean with its own giants. The real unoccupied niche is
**sub-vertical №1 (document/IP/inter-org transfer, out of uniform)**, where our
edge (localization + honest summary verdict + substrate-independence) has
direct value, and heavy suites are overkill. There we are a diagnostic layer
on top of someone else's storage, not a replacement.

**The check did its job again:** it refined "where exactly" BEFORE building —
not "non-code in general," but specifically out-of-uniform document/data
transfer.

## 8. The cheapest next step

NOT code. Find/model ONE real scenario for sub-vertical №1
(a contract/report/dataset between two parties) and run it through our ready
stack (title/anchor/diagnose/resolve_full) end-to-end as a demo: "sent →
a line substituted en route → we show WHERE and WHAT, emit CONTESTED." This will
test the fit on a concrete object (FO-035), not on a slide. Next — find a
design partner who feels this pain.

## Sources

- Digital Evidence Management market: https://www.skyquestt.com/report/digital-evidence-management-market
- Key DEM companies 2025: https://www.researchandmarkets.com/articles/key-companies-in-digital-evidence-management
- Digital Forensics market: https://www.psmarketresearch.com/market-analysis/digital-forensics-market-report
- Blockchain evidence court-admissibility (eIDAS, precedents): https://truescreen.io/articles/blockchain-evidence-court-admissibility-standards/
- Admissibility of digital evidence 2026 guide: https://truescreen.io/articles/admissibility-digital-evidence-guide/
- Blockchain-based chain of custody (design/evaluation): https://www.mdpi.com/2813-5288/3/4/11
