# PRODUCT DOSSIER: provenance for the code supply chain

DATE: 2026-07-23
BASIS: roadmap AD-54 (case chosen by the author, "we're doing it"); the market
part is GROUNDED in 2025-2026 sources (web search, links at the bottom), not
from memory.
STATUS: LLM_GENERATED, a planning dossier. Not a product — a map by which the
product gets built.
DISCIPLINE: honest boundaries; "green tests ≠ verified ≠ audited."

## 1. The case and the user

**What:** give the consumer of a package/artifact (wheel, npm tarball,
container) confidence that the delivered artifact is AUTHENTIC, produced by the
publisher; catch injection at the delivery layer (AD-53 "on the glass").

**Who (candidate design partners):**
- an enterprise that CONSUMES many third-party packages — an independent
  verification gate in CI/CD;
- a team/registry that PUBLISHES packages and wants a threshold of several
  maintainers (one hijacked account cannot ship a release);
- the regulatorily obligated (US EO 14028, EU Cyber Resilience Act) — provenance
  as a requirement, not a wish. Supply-chain attacks doubled in 2025.

## 2. Threat model (what we protect / what we don't)

**We protect (delivery = the glass):** a poisoned mirror/CDN, MITM, a malicious
build step, artifact substitution — the delivered item has a different hash →
caught by reconciling against an independent append-only anchor.

**We do NOT protect (they draw on the registry):**
- hijack of the publisher's account/key → malicious code in the ORIGINAL. This is
  `SIGNED ≠ NATIVE` — and Sigstore's own threat model admits it directly:
  keyless signing does not guarantee that the signer had the right (hijack), or
  that the artifact is "good";
- dependency confusion (which registry is authoritative) — out-of-band pinning;
- a signed backdoor from the author / under coercion (AD-24/28).

## 3. What we ALREADY have (as-is)

| Our module | Role in the case |
|---|---|
| supply.py (ArtifactRegistry + verify_delivery) | reconcile delivery against the glass → FORGERY_ON_GLASS |
| anchor.py (append-only + reconcile) | "the registry under glass," an independent window |
| cosign.py (witnesses) | multi-attestation of the head |
| custody.py / frost.py | THRESHOLD signing (M-of-N maintainers) |
| title.py resolve_full / diagnose.py | a single human-readable verdict + classification |
| integrations (OTS) | a public Bitcoin anchor (adapter) |
| pyproject + wheel | we are ourselves a pypi/npm artifact (demo on ourselves, AD-53) |

## 4. Market and standards (grounded, 2025-2026)

The market is MATURE and has a strong incumbent:
- **Sigstore** (cosign/Fulcio/Rekor) — Linux Foundation, keyless signing via
  OIDC + a public transparency log. Production, widely adopted.
- **npm provenance** — SLSA Build L2 + Sigstore, public beta.
- **PyPI PEP 740** — digital attestations, 270k+ distributions (Trail of Bits).
- **SLSA** — build/provenance levels (Google/OpenSSF).

**Strategic conclusion (honestly):** we must NOT build our own transparency log
— Sigstore already exists and is free. We either COMPLEMENT it or we don't enter.

## 5. Our GAP (where we don't duplicate)

Sigstore's own threat model admits a hole: **one hijacked publisher OIDC
identity → a malicious release** (Sigstore's threshold is only on the ROOT
3-of-5, not on publishing the package). The answer to "one compromise must not
break the system" is a **threshold/MPC signature** (no one knows the full key),
but it lives in wallets/custody, NOT in mainstream package publishing. Academia
confirms the same (DiVerify: hardening identity-based signing).

**Two candidate wedges (not competition, but a superstructure):**

**A. Threshold release publishing (our differentiator).** A release counts as
authentic only with M-of-N maintainer signatures / independent attestations.
Directly closes the "single hijack." This is our custody/frost/cosign/
convergence. THE PRICE: it needs PRODUCTION FROST (Rust) + ecosystem
participation (network effect) — hard and slow.

**B. A consumer gate verdict (achievable in the near term).** A client in CI
that: (1) checks EXISTING attestations (Sigstore/npm provenance/SLSA) with their
own libraries; (2) adds a THRESHOLD POLICY (require M independent attestations
where available); (3) issues a human-readable verdict CONFIRMED/CONTESTED/
PROVISIONAL + a diagnosis (our resolve_full/diagnose). It complements rather than
argues; our value is the threshold policy + an honest UX verdict.

## 6. What to replace for production (for this case only)

- Our in-memory ArtifactRegistry → a client to a REAL Rekor / PyPI attestations
  (adopt Sigstore libraries), not our own log.
- Threshold: our frost is a reference; for wedge A you need Rust FROST via FFI or
  a signing service (or use existing M-of-N where available).
- The OTS anchor — in an environment with a network (egress is closed here,
  AD-31).
- The wrapper: a CLI/CI plugin + policy, not a demo script.

## 7. Validation (what to prove to be believed)

1. An independent security audit of the verification logic.
2. Real integration against a live Sigstore/Rekor + PyPI attestations (needs a
   network — NOT verified in this environment).
3. A pilot: a real consumer/maintainer, metrics of caught/false positives on
   real artifacts.
4. A comparison with `cosign verify` / `npm audit signatures` — what we ADD.

## 8. What we do NOT promise (in the positioning)

- Not "the code is safe" — only "the publisher's artifact, untouched in
  delivery."
- Not protection against a publisher hijack / a malicious author (only wedge A
  partially: the threshold).
- Reconcile is strong exactly to the extent that the anchor is independent AND
  the consumer actually reconciles (otherwise "eternal glass," FO-005).

## 9. Order of operations

```
0. Live competitive check (exactly what Sigstore/SLSA/PEP 740/npm cover; the
   precise boundary of the wedge) — needs a network run + reading the specs.
1. Choose a wedge: B (gate verdict, faster) or A (threshold, differentiator).
2. Production only for the chosen wedge (Rekor client / Rust FROST).
3. Design partner + a pilot on real artifacts.
4. Audit + license (AGPL/commercial, AD-55) + packaging.
```

## 10. Honest strategic verdict

The case is **viable as a SUPERSTRUCTURE, not as a replacement**. The market is
occupied by Sigstore; there is demand (regulation, rising attacks). Our real edge
is narrow but genuine: **a threshold on publishing** (a hole Sigstore itself
admits) + **an honest aggregated verdict**. The fast entry is wedge B (a consumer
gate on top of ready attestations); the principled but long one is wedge A
(threshold publishing, needs Rust FROST + a network effect). RISK: the space is
crowded and well-funded; without a real design partner who FEELS the pain of the
single hijack, this is research again. THE NEXT CHEAP STEP: §9.0 — a live
competitive check of the specifications.

## Sources

- Sigstore threat model: https://docs.sigstore.dev/about/threat-model/
- Sigstore overview: https://docs.sigstore.dev/about/overview/
- OpenSSF / Sigstore: https://openssf.org/tag/sigstore/
- SLSA blog: https://slsa.dev/blog
- PyPI digital attestations (PEP 740): https://blog.deps.dev/pypi-attestations/
- SLSA + Sigstore + build provenance: https://aquilax.ai/blog/supply-chain-artifact-signing-slsa
- Trail of Bits / SLSA: https://blog.trailofbits.com/2024/10/01/securing-the-software-supply-chain-with-the-slsa-framework/
- DiVerify (identity-based signing hardening): https://arxiv.org/pdf/2406.15596
- Threshold signatures / MPC guide: https://denispopovengineer.medium.com/threshold-signatures-and-multi-party-computation-a-practical-guide-to-secure-shared-control-41936ff1733f
