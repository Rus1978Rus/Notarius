# LIVE COMPETITIVE SCAN: code supply chain

DATE: 2026-07-23
BASIS: §9.0 of the AD-56 dossier. Web search 2025-2026 (links at the bottom). STATUS:
LLM_GENERATED. GOAL of the step: say "no" BEFORE building, if the field is occupied.
VERDICT IN SHORT: **the field is occupied; both of our wedges are already covered by prior
art. A cheap "no" to a standalone product.**

## Coverage matrix (who already does what)

| Capability | Sigstore/cosign | SLSA | TUF | Kyverno/policy-controller | PEP 740/npm |
|---|---|---|---|---|---|
| Detect DELIVERY substitution (hash vs signed record) | ✅ | ✅ | ✅ | ✅ (consumer) | ✅ |
| Public transparency log | ✅ Rekor | — | ✅ | — | ✅ (via Sigstore) |
| **Multi-maintainer threshold (our wedge A)** | root only 3-of-5 | — | **✅ delegations + thresholds** | several signatures org+project | — |
| **Consumer gate policy (our wedge B)** | policy-controller | — | — | **✅ admission verification** | — |
| Protection against MAINTAINER compromise | ❌ (acknowledged threat-model) | ❌ Build; **Source Track in progress** | partial (offline threshold) | ❌ | ❌ |
| Human-readable honest verdict (CONFIRMED/CONTESTED + diagnosis) | pass/fail | — | — | pass/fail | — |

## Our two wedges against prior art

- **Wedge A — threshold release publication.** DIRECT prior art: **TUF** —
  delegations to specific packages + signing thresholds for several people.
  A mature CNCF standard (it also sits under the Sigstore root). → NOT a differentiator.
- **Wedge B — consumer gate verdict.** DIRECT prior art: **Kyverno /
  cosign policy-controller** — verification of signatures/attestations at admission,
  blocking the unsigned, several signatures (org+project). → NOT a differentiator.
- **The "maintainer compromise" gap** — real (SIGNED ≠ NATIVE, acknowledged by
  Sigstore), but **the SLSA Source/Dependencies Track is already plugging it**.

## What honestly REMAINS unoccupied (a thin slice)

Only **a human-readable aggregated honest verdict**: our
diagnose/resolve_full give CONFIRMED/CONTESTED/PROVISIONAL + "why" +
confidence levels, folding HETEROGENEOUS sources (Sigstore + npm provenance +
SLSA + TUF) into one plain-language verdict. Existing tools give
pass/fail. BUT honestly: this is a **feature, not a moat** — it is easily added to an
existing tool and does not stand up as a standalone product.

## Strategic conclusion (honest, no embellishment)

**The CODE supply chain is a red ocean.** It is held by TUF, Sigstore, SLSA,
Kyverno, cosign policy-controller, in-toto, GUAC — CNCF/Linux Foundation/
Google funding. Both of our wedges are already implemented by prior art;
even the acknowledged gap is being actively closed by an incumbent. Entering here = competing
with giants on a narrow UX slice. **High risk, low differentiation.**

**The scan did its job:** it showed this BEFORE building, not after.

## Where this pivots to (two honest paths)

1. **Not standalone, but a contribution-feature.** Give the honest-verdict aggregator to
   an existing tool (Kyverno/cosign/GUAC) — as a feature, not a product.
   A small but real contribution; not a business in itself.
2. **Pivot into a LESS occupied vertical.** Key point: the whole code stack (Sigstore/
   TUF/SLSA) works ONLY with code artifacts. Our general model
   (title/anchor/reconcile/diagnose) works with ANY element —
   documents, data, media. Chain-of-custody for NON-code (legal/forensics/
   finance) is a field where the code stack is NOT present, and "localize the lie +
   a human-readable verdict" has direct value. There our general model
   does not compete with the giants.

## RECOMMENDATION

**Do not build a standalone code-supply-chain product.** The scan is a
cheap, well-reasoned "no." Options: (1) a contribution-feature into an existing tool;
(2) return to the chain-of-custody vertical (non-code), where our general model
has a place. My advice: consider §2 — this is the original "valuable but
long" candidate from the roadmap, but now with actual grounds for WHY
not code supply chains.

## Sources

- TUF (delegations + thresholds): https://theupdateframework.io/docs/faq/
- TUF × Sigstore: https://blog.sigstore.dev/the-update-framework-and-you-2f5cbaa964d5/
- Kyverno verify images (cosign/attestations): https://kyverno.io/docs/policy-types/image-validating-policy/
- Kyverno × Sigstore: https://main.kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/
- SLSA levels (what it does NOT cover): https://slsa.dev/spec/v1.0/levels
- SLSA provenance: https://slsa.dev/spec/v1.0-rc1/provenance
- Sigstore threat model: https://docs.sigstore.dev/about/threat-model/
