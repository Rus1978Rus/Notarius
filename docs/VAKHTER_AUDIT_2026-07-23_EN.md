# Audit of the sibling project Vakhter → what was taken into NOTARIUS

DATE: 2026-07-23
SOURCE: rus1978rus/vakhter @ 3763b71 (same author — Ruslan Malyavskiy)
BASIS: the author's request "read it line by line, maybe there's something worth
taking."
METHOD: 4 parallel readers (core/docs, canonization+engine, invariant-engine+
applications, sign cards), line by line; ~460 per-sign cards — 18 classes in
full + a representative sample (honestly).
DISCIPLINE: LLM_GENERATED. Everything ported into code is covered by our tests;
we do not pass off someone else's metrics as our own.

## The main discovery: two branches of one seed

Inside Vakhter lies `docs/NOTARIUS.md` (dated 2026-07-20 — the same source as
our `NOTARIUS_FULL_SESSION.md`): §6.3 SEMANTIC_INVISIBLE_LENGTH_WITNESS (the
parent of our `witness.py`), invisible-character handling (the parent of
`scanner.py`), the chain-manifest (the parent of `trace.py`). And
`applications/notarius_data/notarius_ledger.py` is a working MVP of the same idea
(4 barriers: hash + cp_len witness + signed lineage + a hash-chain log).

Conclusion: Vakhter and our NOTARIUS are **two halves of one whole**:

| Layer | Vakhter | Our NOTARIUS |
|---|---|---|
| Detection (invisible characters, homoglyph, bidi, canonization) | **mature** — engine + 129 cards | was a naïve `scanner.py`, 77 lines |
| Cryptography (signature, threshold, time, recovery) | weak — only HMAC (symmetric) | **mature** — Ed25519, custody, carrier, OTS, RS |

We took their detection — kept our cryptography. Both repositories are by the
same author; there is no licensing barrier to moving code between one's own
projects (the "COMMERCIAL USE PROHIBITED" mark is about third parties).

## What Vakhter is

A structural gatekeeper in front of an LLM: it reads incoming text BEFORE the
model, catching hidden commands, look-alike domains, invisible characters,
encoding tricks. The principle: "what is real is what survives transformation"
(invariance). Two axis-engines: MSL (what a sign does in context) + ERG (does the
structure survive coarsening of scale). The status is honest: `WORKING_DRAFT`, "a
prototype of the principle, not a certified product."

## What was TAKEN into the code (AD-33)

Ported verbatim, with the source cited, covered by our own tests:

1. **`notarius/canon.py`** ← `code/canonicalization/canonicalize.py`. A pre-pass
   against encoding evasion: percent (including double), HTML entities, `\u/\x`,
   **overlong UTF-8** (`%c0%af`→`/` with a flag), numeric IP hosts. Pure stdlib.
   Tests: `tests/test_canon.py` (7, green). ⚠️ **NOT Unicode normalization, does
   NOT close AD-4** — an orthogonal thing, placed alongside. Known false positive:
   prose with a literal "%2f" will get decoded (fine for advisory, not for a
   "silent" block).

2. **`notarius/detect.py`** ← `code/range/{invisible_cards,canonical_view,
   fail_closed}.py` + `Finding` from `invariant_engine/core.py`. Real detection we
   didn't have:
   - ALARM (conclusive): word-split by an invisible character, bidi imbalance
     (Trojan-Source CVE-2021-42574), tag-smuggle without a flag base, VS-carrier,
     parser desync (raw ≠ canonical reading of the token);
   - OK: legitimate joining (emoji ZWJ, VS after a base, tag after a flag,
     balanced bidi) — against false alarms;
   - WATCH: an invisible character is present, but neither a smuggle nor a
     provable joining;
   - fail-closed: non-string / detector error → block, never OK.
   Tests: `tests/test_detect.py` (13, green — both what is caught and what isn't).

3. **`notarius/scanner.py::scan_hardened()`** — a façade: `scan()` (v2, X-ray)
   stays as it was; `scan_hardened()` adds canonization + the `detect` engine on
   top. Returns a risk/signature verdict + the X-ray projection.

## What was taken as discipline (not code, for the future)

- Vakhter's **`provenance.py`** confirms our cp_len witness as a witness of
  insertion inside a signed record (the role from AD-3) — our design is right,
  no change needed.
- **mutation-adequacy** (`gate_selftest.py`, "a gate you can't fail is not a
  gate"): our verify functions should add a check "mutate a signed event → verify
  must reject." CANDIDATE.
- **r>g admission filter** — a rubric for decisions "add code or structure" on
  future modules.
- **honest-eval** (seed/held split, per-subclass recall, naming the false
  positives) — how to evaluate any of our detectors if it comes to metrics.

## What was NOT taken and why

- **The sign_cards library (129 code points EN+RU + 14 classes)** — we did NOT
  copy 258 files over: it's a draft reference, it lives in Vakhter. We took the
  engine logic from it and pointed RISK/SAFE vectors as test seeds. The link to
  the source is here.
- **Vakhter's cryptography (HMAC)** — weaker than ours; here we are ahead
  (Ed25519).
- **product.py / behavioral.py / range_*.py demo** — hard-depend on an external
  `msl_mip_runtime.py` (not in the repository), they won't run for us.

## Vakhter's honest problems (carried as a caution)

- **The MSL core is not in the repository** (external, `MSL_MIP_HOME`) → the loud
  coverage figures from there are not verifiable.
- The impressive "100%" figures are on draft **simulators**, not on real cards;
  the BASELINE ≈ 0.5% of the plan. Batteries of 7–15 cases, where one author wrote
  both the threats and the detectors (self-selection).
- The Foundation Layer claims are grandiose/unfalsifiable ("69,826 years of
  proof," "0 hallucinations," post-hoc "predicted the bugs"); circularity — the
  project enters itself into the registry it uses to justify itself.
- **A real bug was found by running** `notarius_ledger.py`: the label
  `INVISIBLE_INSERT` is returned on ANY change of length (a visible
  `1000000`→`500` is marked "invisible insertion"). Our `trace.py` does not do
  this.
- Of the 14 card classes, only 4 are wired into the real `product.py`; the
  `range/` engine has no auto-tests (print-demos, zero assert).
  → The moral for us: **we take ideas and primitives; we do not accept someone
  else's figures as validated.** The ported code lives here under our own tests
  and with honest labels "a port of draft logic, behavior, not security."

## The boundary

The port moves our detection layer from a "naïve scanner" to "an assembly of a
relative's verified logic under our own tests." Human validation of the detection
still does NOT exist; this is an advisory tool, not a certified filter. AD-4
(Unicode normalization) remains open — `canon.py` does not close it.
