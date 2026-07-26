# ROADMAP: prototype → product (honest)

DATE: 2026-07-23
BASIS: the author's request "can we turn it into a product?". A general map WITHOUT choosing
a case — facts for a decision. STATUS: LLM_GENERATED, a plan.
GOVERNING RULE: green tests ≠ verified in the world ≠ passed an audit.

## 0. Where we honestly are

RESEARCH_TRACK (AD-9): the product search is paused — the applications conveyor produced
**0 STRONG** out of 40 ideas. There is a 192-test prototype, packaged into a wheel
(`twine check PASSED`), a coherent value line (element provenance → title →
supply chain), and honest boundaries. This is a FOUNDATION, not a product.

"Make a product" = switch modes: pick ONE narrow case + a real
user + a threat model + validation. This is NOT a continuation of open research.

## 1. The common gap (needed for ANY case)

```
① VALIDATION + AUDIT   an independent security audit; a pilot with a real
                       user; data, not "works on the demo."
② LICENSE + IP         AD-7 is open; COMMERCIAL USE PROHIBITED. Choose before
                       any commerce. Check patent clearance.
③ PRODUCTION not demo  replace the reference/stubs (see the table in §2) for the
                       chosen case — not everything at once.
④ THREAT MODEL         from whom/what we protect in THIS case; what we do NOT promise.
⑤ USER WRAPPER         API/SDK or service, user docs (not
                       AUTHOR_DECISIONS), deploy, ops, support.
⑥ BOUNDARIES IN THE POSITIONING   sell exactly what the mechanism gives (not "unbreakable").
```

## 2. Component readiness (honest)

| Module | Status | What's needed for production |
|---|---|---|
| trace.py (trace core) | PROTOTYPE, tested | external time anchor (OTS), key↔identity binding (PKI) |
| envelope_v2 (Ed25519) | crypto mature (libsodium) | our application — a prototype; wrapper/key storage |
| custody (Shamir threshold) | DEMO (seed in memory) | FROST + proactive SS |
| frost (threshold) | REFERENCE (not audited, not const-time) | Rust-FROST via FFI / signing service |
| carrier (mortal) | DEMO (HMAC) | a real key + external time |
| cosign (witnesses) | PROTOTYPE | a real witness network / transparency log |
| anchor (public registry) | PROTOTYPE | a LIVE log: Sigstore/Rekor or Bitcoin/OTS (needs a network) |
| integrations (RS/OTS) | RS working; OTS network-blocked | an environment with a network for OTS |
| scanner/detect/canon | DRAFT (port of Vakhter), advisory | NOT our subject — the catalog lives with the sibling projects |
| diagnose | PROTOTYPE, advisory | useful as is |
| title (ownership/hybrid) | PROTOTYPE | a live anchor + out-of-band trust + real identities |
| supply (supply chain) | PROTOTYPE | slot into Sigstore/SLSA/PEP 740 (standards ready) |

**Conclusion on the crypto:** our STRONGEST part is the delivery layer (append-only
registry + `reconcile`), and it does NOT require heavy crypto. The WEAKEST by
readiness is a real threshold (FROST) and a live network anchor. The first case
is reasonably chosen for our strength, not for our weakness.

## 3. Criteria for choosing the first case

A good first product:
1. **Slots into an existing market/standard** (lower go-to-market risk).
2. **Leans on our strength** (delivery layer/reconcile/append-only), not on
   not-yet-ready heavy crypto (FROST, network anchor).
3. **A narrow, definable threat model.**
4. **A real first user is reachable** (design partner).
5. **The honest boundaries are acceptable** — the user does NOT need what we do not give
   (content truth, protection against coercion).
6. **A clear legal/revenue path** (compatible with the license choice AD-7).

## 4. Candidates, honestly against the criteria

| Case | Market/standard | Our strength | Path | Risk |
|---|---|---|---|---|
| **Code supply chain** | ✅ Sigstore/SLSA/PEP 740 | ✅ delivery/reconcile | short | market occupied — better to INTEGRATE, not compete |
| **Chain-of-custody (legal/forensics/finance)** | partially (eIDAS, RFC 3161) | ✅ trace+localization of the lie | longer | regulation, needs a network time anchor |
| Ownership title / anti-theft | nothing ready | mixed | long | needs recognized identities + legal recognition of the title |
| Element provenance (general) | diffuse | the core | — | this is the 0-STRONG (too broad) |
| Video/media (C2PA) | ✅ C2PA (industry) | medium | medium | needs hardware capture; better to complement C2PA |

## 5. Recommended sequence (once you pick a case)

```
1. Narrow case + one design partner + threat model
2. Productization dossier for the case (what exists/what to replace/market/validation/boundaries)
3. Replace demo stubs ONLY for this case
4. External security audit
5. Pilot with real data → measured results
6. Decide the license (AD-7) BEFORE commerce
```

## 6. What must NOT be promised (in any product positioning)

- Not "truth/security of content" — only "not touched/localized"
  (SIGNED ≠ NATIVE, TRACE_LOCATES ≠ PROVES_TRUTH).
- Not protection against coercion (AD-28) and not protection of POSSESSION (only the title).
- An anchor without a live public log = words; a network anchor is genuinely needed.
- Not "unbreakable" — hybrid/mirror have an irreducible residual (eternal
  glass, FO-005).

## 7. Decisions needed from the author

1. **Which case** first (§4) — it determines the whole further plan.
2. **License** (AD-7) — before commerce.
3. **Is there a real first user** (design partner) — without one this is
   research again, not a product.

## SUMMARY

A product **is possible** — a foundation built from standards, assembled, packaged. But the path
is specific: a narrow case under our strength (the delivery layer) → dossier → replace
the demo → audit → pilot → license. The shortest entry is the supply
chain (integrate into Sigstore/SLSA), the most valuable-but-long is chain-of-custody
for a vertical. The choice of case is the author's; after that I do the dossier for the chosen one.
