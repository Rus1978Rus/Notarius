# DOCUMENT_PROVENANCE_REGISTER

Rule basis: PROJECT_WIDE_DOCUMENT_PROVENANCE_RULE (E-Continuity RULES,
item 4) — "every important document must have a DOCUMENT_PROVENANCE_CARD".
Clearing debt AD-15. One register instead of a scatter of small cards
(PERMANENT_RULE_PREFLIGHT_GUARD: a rule protects, it does not paralyze).

ORIGIN legend:
- **AUTHOR_SOURCE** — the author's original/copy (human / past sessions).
- **LLM_GENERATED** — Claude output in this session (`LLM_OUTPUT ≠ VERIFIED_COPY`).
- **EXTERNAL_VENDOR** — third-party AI text, pasted by the author.
- **COPY** — file copied from another package (`COPY ≠ PROVENANCE`).

| Document | ORIGIN | Status | Provenance / note |
|---|---|---|---|
| docs/NOTARIUS_FULL_SESSION.md | AUTHOR_SOURCE + LLM edits | working | uploaded by the author; AI added notes AD-1…AD-12 |
| docs/NOTARIUS_METHODOLOGICAL_AUDIT_2026-07-21_EN.md | LLM_GENERATED | analysis | line-by-line audit, session 2026-07-21 |
| docs/PRIOR_ART_REVIEW_2026-07-21_EN.md | LLM_GENERATED | analysis | web review, sources inside |
| docs/AUTHOR_DECISIONS.md | LLM_GENERATED | journal | records the author's decisions AD-1…AD-92 |
| docs/VENDOR_PROMPT_APPLICATIONS_EN.md | LLM_GENERATED | tool | vendor-survey prompt (ideas) |
| docs/VENDOR_PROMPT_METHODS_REVIEW_EN.md | LLM_GENERATED | tool | blind methods-review prompt (AD-20) |
| docs/VENDOR_PROMPT_UNCOPYABLE_KEY_EN.md | LLM_GENERATED | tool | blind prompt to find an uncopyable key part (AD-25) |
| docs/vendor_answers/*.md | EXTERNAL_VENDOR | data | Copilot/DeepSeek/Qwen/Kimi/Gemini, pasted by the author |
| docs/conveyor_results/*.md | LLM_GENERATED | results | conveyor judge verdicts |
| docs/FOUNDATION_LAYER_ANALYSIS_2026-07-22_EN.md | LLM_GENERATED | analysis | review of the MSL/MIP package |
| docs/foundation_layer/** | AUTHOR_SOURCE / COPY | reference | copy of the Foundation Layer package, not an original |
| docs/NOTARIUS_DISCIPLINE_2026-07-22_EN.md | LLM_GENERATED | discipline | integration of FO-015/035/018 (AD-12) |
| docs/E_CONTINUITY_FRAMING_2026-07-22_EN.md | LLM_GENERATED | roof | ecosystem map (AD-13/14) |
| docs/E_CONTINUITY_ANALYSIS_2026-07-22_EN.md | LLM_GENERATED | analysis | review of the parent (AD-14) |
| docs/MSL_MIP_GENESIS_PROVENANCE_2026-07-22_EN.md | AUTHOR_TESTIMONY + LLM framing | genesis | the birth of MSL/MIP from E-Continuity (AD-16) |
| docs/ALGORITHMS_SIGNING_IDENTIFICATION_2026-07-22_EN.md | LLM_GENERATED | catalog | signing/identification of segments and the whole (AD-18) |
| algorithms/merkle_segments.py | LLM_GENERATED | code | segment/whole signing via Merkle |
| algorithms/human_fingerprint.py | LLM_GENERATED | code | human-verifiable fingerprint + redundant ID |
| docs/SEMANTIC_TRACE_2026-07-22_EN.md | LLM_GENERATED | core | semantic tracing (AD-19) |
| notarius/trace.py | LLM_GENERATED | code | chain of an element's signed events |
| notarius/custody.py | LLM_GENERATED | code | custody enclosure: threshold + heartbeat + epochs (AD-27) |
| notarius/carrier.py | LLM_GENERATED | code | mortal carrier-validator (AD-29) |
| docs/KEY_CUSTODY_BUILD_PLAN_2026-07-23_EN.md | LLM_GENERATED | plan | building the custody enclosure (AD-27) |
| docs/INTEGRATION_DOSSIER_2026-07-23_EN.md | LLM_GENERATED | plan | integration of 5 standards into our modules (AD-30) |
| notarius/integrations.py | LLM_GENERATED | code | Reed-Solomon adapters (working) + OpenTimestamps (network-blocked, AD-31); deps: reedsolo, opentimestamps |
| tests/test_integrations.py | LLM_GENERATED | code | 6 integration tests (RS offline + OTS offline part), AD-31 |
| docs/VAKHTER_AUDIT_2026-07-23_EN.md | LLM_GENERATED | audit | line-by-line review of the sibling vakhter@3763b71 + what was taken (AD-33) |
| notarius/canon.py | LLM_GENERATED (port) | code | canonicalization pre-pass, port of vakhter/canonicalize.py; NOT NFC (AD-33) |
| notarius/detect.py | LLM_GENERATED (port) | code | engine for invisibles/bidi/tag/VS/desync + fail-closed, port of vakhter/range (AD-33) |
| tests/test_canon.py | LLM_GENERATED | code | 7 tests of the canonicalization pre-pass (AD-33) |
| tests/test_detect.py | LLM_GENERATED | code | 13 tests of the detection engine, both outcomes (AD-33) |
| tests/test_mutation.py | LLM_GENERATED | code | mutation-adequacy verify + content axis of trace/carrier (AD-34) |
| scripts/sweep_invisible_class.py | LLM_GENERATED | tool | reproducible measurement of the watched class, 0 silent OK (AD-35) |
| scripts/adversarial_env.py | LLM_GENERATED | tool | signed-through-external-environments (iconv/sed/gzip/NFKC/JSON), verify (AD-41) |
| notarius/cosign.py | LLM_GENERATED | code | witness-cosigning: closing trace fork/truncation M4 (AD-36) |
| tests/test_cosign.py | LLM_GENERATED | code | 11 witness-cosigning tests: fork/truncation/quorum/forgery (AD-36) |
| docs/SEMANTIC_TRACE_CANON_2026-07-23_EN.md | LLM_GENERATED (author-origin roots) | canon | the AUTHORITATIVE definition of semantic tracing — the heart of the product (AD-39/40) |
| notarius/diagnose.py | LLM_GENERATED | code | break diagnostician: classifies WHAT changed + homoglyphs + a unified report (AD-42/79) |
| notarius/homoglyph.py | LLM_GENERATED | code | look-alike detector on UTS#39 data (skeleton); 1861 confusables (AD-79/80) |
| notarius/data/confusables_ascii.txt | EXTERNAL (UTS#39) | data | ASCII-target subset of Unicode 17.0.0 confusables; provenance in the header (AD-80) |
| docs/MSL_MIP_AUDIT_2026-07-25_EN.md | LLM_GENERATED | audit | line-by-line reading of msl_mip: what was taken (UTS#39 + discipline) / left (AD-80) |
| docs/ARCHITECTURE_CORE_AND_READERS_2026-07-25_EN.md | LLM_GENERATED | schema | core + pluggable readers + doors: architecture map (AD-89) |
| tests/test_homoglyph.py | LLM_GENERATED | code | 7 tests of Kimi fixes: homoglyph/time_proven/cosign fail-closed (AD-79) |
| notarius/title.py | LLM_GENERATED | code | seal + convergence + hybrid + earliness weight + a UNIFIED resolve_full (AD-44…51) |
| tests/test_title.py | LLM_GENERATED | code | 23 seal tests: …hybrid/divergence + mirror defense (AD-44/46/47/48) |
| tests/test_diagnose.py | LLM_GENERATED | code | 10 diagnostician tests: value/invisible/normalization/char-loss (AD-42) |
| notarius/frost.py | LLM_GENERATED | code | reference FROST-ED25519: threshold without reassembling the secret, verify unchanged (AD-38) |
| tests/test_frost.py | LLM_GENERATED | code | 8 FROST tests: 2-of-3/5-of-7 verify, envelope accepted by our verify (AD-38) |
| docs/conveyor_results/methods_internal_review_2026-07-22_EN.md | LLM_GENERATED | results | internal methods review (AD-21) |
| docs/conveyor_results/engine_horizons_review1_2026-07-25_EN.md | LLM_GENERATED | results | synthesis of horizons reviewer #1: confirmed/rejected, 7 conditions (AD-75) |
| docs/conveyor_results/engine_horizons_synthesis_2026-07-25_EN.md | LLM_GENERATED | results | cross-synthesis of reviewers #1+#2+#3(Kimi)+#4: documents outside the loop + regulator-mandatory check; 3 Kimi defects (AD-76/77/78) |
| docs/conveyor_results/methods_crossvendor_synthesis_2026-07-22_EN.md | LLM_GENERATED | results | summary of 5 sources on methods (AD-22) |
| docs/EXTERNAL_SOLUTIONS_MAP_2026-07-22_EN.md | LLM_GENERATED | map | open problems → ready-made standards (AD-23) |
| docs/conveyor_results/uncopyable_key_internal_2026-07-22_EN.md | LLM_GENERATED | results | uncopyable-key-part conveyor, partial (AD-25) |
| docs/conveyor_results/uncopyable_key_synthesis_2026-07-23_EN.md | LLM_GENERATED | results | summary of 7 sources on the uncopyable key part (AD-26) |
| docs/vendor_answers/uncopyable_kimi_2026-07-23.md | EXTERNAL_VENDOR | data | Kimi, answer to the AD-25 prompt |
| docs/e_continuity/** | AUTHOR_SOURCE / COPY | reference | copy of the E-Continuity v2.3 text core |
| notarius/witness.py | LLM_GENERATED | code | v1 prototype (HMAC, stdlib) |
| notarius/envelope_v2.py | LLM_GENERATED | code | v2 (Ed25519, PyNaCl) |
| notarius/scanner.py | LLM_GENERATED | code | v2 invisible-character scanner |
| notarius/anchor.py | LLM_GENERATED | code | public append-only anchor "registry under glass" + reconcile + earliness weight (AD-49/50) |
| tests/test_anchor.py | LLM_GENERATED | code | 10 anchor tests: FORGERY_ON_GLASS, integrity, mirror caught by the registry (AD-49) |
| tests/** | LLM_GENERATED | code | 235 tests (…/title/hybrid/mirror-defense); break diagnostician — growth of the semantic center (AD-42) |
| experiments/exp_6_2_reassembly.py | LLM_GENERATED | code | dynamic proof test §6.2 |
| notarius/supply.py | LLM_GENERATED | code | supply-chain: injection into delivery = "onto the glass", reconcile with the registry (AD-53) |
| tests/test_supply.py | LLM_GENERATED | code | 5 supply tests: FORGERY_ON_GLASS, first-wins, registry tampering (AD-53) |
| scripts/supply_chain_demo.py | LLM_GENERATED | tool | demo on a real wheel: injection into delivery exposed (AD-53) |
| LICENSE | AUTHOR_DECISION + LLM | license | PROPRIETARY — all rights reserved; dual AGPL withdrawn (AD-82) |
| notarius/urlcontext.py | LLM_GENERATED | code | domain/URL awareness: look-alike/invisible in a domain = HIGH, userinfo spoofing (AD-81) |
| tests/test_urlcontext.py | LLM_GENERATED | code | 7 domain-context tests: host/userinfo/path/legit (AD-81) |
| pyproject.toml | LLM_GENERATED | packaging | PyPI metadata (setuptools); name=notarius 0.1.0; extra [integrations] (AD-52) |
| notarius/__init__.py | LLM_GENERATED | code | package init: version/author, no heavy imports (AD-52) |
| NOTICE.txt | AUTHOR_SOURCE + LLM | license | author + COMMERCIAL USE PROHIBITED, license TBD (AD-7/52) |
| README.md | LLM_GENERATED | navigation | repository map |
| docs/PRODUCTIZATION_ROADMAP_2026-07-23_EN.md | LLM_GENERATED | roadmap | the research→product path, cases (AD-54) |
| docs/PRODUCT_DOSSIER_SUPPLY_CHAIN_2026-07-23_EN.md | LLM_GENERATED | dossier | supply-chain case plan, grounded in sources (AD-56) |
| docs/COMPETITIVE_SCAN_SUPPLY_CHAIN_2026-07-23_EN.md | LLM_GENERATED | scan | live competitive scan → "no" to a code-supply-chain product (AD-57) |
| docs/POSITIONING_2026-07-23_EN.md | LLM_GENERATED | positioning | a one-pager without crypto jargon: the product = an honest history, not storage (AD-58) |
| docs/PIVOT_CHAIN_OF_CUSTODY_2026-07-23_EN.md | LLM_GENERATED | pivot | pivot to non-code chain-of-custody, grounded; the field is not empty, niche = out-of-band handoff (AD-59) |
| scripts/handoff_demo.py | LLM_GENERATED | demo | inter-org handoff on a concrete object: amount swap exposed (where+what), from the ready stack (AD-60) |
| docs/DEMO_HANDOFF_ONEPAGER_2026-07-24_EN.md | LLM_GENERATED | pitch | a funnel one-pager: hook→simple→complex→"hand off to specialists" (AD-61/62/63) |
| notarius/cli.py | LLM_GENERATED | code | MINIMAL PRODUCT: check/seal/verify — run on your own file, verdict where+what; pure stdlib (AD-64) |
| notarius/__main__.py | LLM_GENERATED | code | entry point python3 -m notarius (AD-64) |
| tests/test_cli.py | LLM_GENERATED | code | 10 CLI checks: check/seal/verify, return codes, binary (AD-64) |
| docs/product_mockup/notarius_ui.html | LLM_GENERATED | mockup | HTML buyer screen: 2 documents + verdict, trust-tuned colors; self-contained (AD-65) |
| docs/CHTO_UMEEM_SEYCHAS_2026-07-24_EN.md | LLM_GENERATED | boundary | in plain text: what we can do now vs will build (text vs photo/video) (AD-66) |
| docs/CHTO_TAKOE_ETALON_2026-07-24_EN.md | LLM_GENERATED | explanation | in plain text: what a reference is, how it appears, why everyone checks against one (AD-67) |
| docs/A_ESLI_PROGRAMMA_TOLKO_U_KLIENTA_2026-07-24_EN.md | LLM_GENERATED | explanation | an honest answer: without a sender mark there's nothing to catch; two touch-points needed (AD-68) |
| docs/KUDA_VSTRAIVAETSYA_2026-07-24_EN.md | LLM_GENERATED | model | distribution: the engine embeds into mail/accounting/CRM/messengers (AD-69) |
| docs/VENDOR_PROMPT_ENGINE_HORIZONS_EN.md | LLM_GENERATED | tool | blind conveyor prompt: application horizons of the engine for external reviewers (AD-73) |
| scripts/two_accounts_demo.py | LLM_GENERATED | demo | two mailboxes on one computer + registry under glass: attachment interception exposed (AD-70) |
| scripts/trace_localize_demo.py | LLM_GENERATED | demo | the engine in pure form: the trace localizes WHOSE link broke, no plumbing (AD-83) |
| notarius/record.py | LLM_GENERATED | code | governed record: fields with keepers + legitimate progression + footnote; folds AD-84/85/86 (AD-87) |
| tests/test_record.py | LLM_GENERATED | code | 8 record tests: keeper/void/progression/violation localization (AD-87) |
| scripts/record_demo.py | LLM_GENERATED | demo | a single record run: a living document, forgeries localized by field (AD-87) |
| scripts/carriers_demo.py | LLM_GENERATED | demo | the core on DIFFERENT carriers (text/image/audio/data): any swap localized (AD-88) |
| scripts/notarius_mail.py | LLM_GENERATED | tool | mail send/recv/selftest (SMTP/IMAP); offline path proven, network blocked in the environment (AD-71) |
| docs/POCHTA_INSTRUKCIYA_2026-07-24_EN.md | LLM_GENERATED | instructions | step by step: a run on two real Gmail accounts (AD-71) |
| docs/WINDOWS_POSHAGOVO_2026-07-24_EN.md | LLM_GENERATED | instructions | Windows step by step to the first success (self-test) for the non-technical author (AD-72) |
| tests/test_audit_fixes.py | LLM_GENERATED | code | external-audit #2 regression: 6 tests reproduce and close N-W1/2/4/5/6/7 (AD-91) |
| notarius/route.py | LLM_GENERATED | code | mandatory-route LAYER: catches a missing step against a role contract (AD-92) |
| tests/test_route.py | LLM_GENERATED | code | 11 route vulnerability probes: omission/role impersonation/order/foreign-subject splice (AD-92) |

BOUNDARY (parent): no LLM_GENERATED document is a human-verified copy.
AUTHOR_SOURCE copies are not physical originals (`COPY ≠ PROVENANCE`).
No external verification was performed.
