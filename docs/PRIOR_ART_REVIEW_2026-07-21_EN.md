# NOTARIUS — Prior Art Review

DATE: 2026-07-21
BASIS: AUTHOR_DECISION AD-5 ("review first, verdict after")
METHOD: web check of the current state (July 2026) of five systems from
the AD-5 list + the market for business-document protection (a sixth
direction, added as the nearest commercial neighbor of the niche)
PURPOSE: input for the author's decision on the §15 verdict
(currently: VERDICT_FROZEN)

Each system is scored against the three Notarius criteria:
- **E** — element level (field/component, not container)
- **P** — embedded in the pipeline (creation/editing/transfer)
- **R** — human-readable report of provenance/break

---

## 1. C2PA / Content Credentials

**Current state (verified):** specification 2.3 (December 2025 /
January 2026), a conformance-certification program launched in 2026.
Key point: v2.3 added manifests for **unstructured text**
and live video streams — C2PA moved beyond media files.

**What it COVERS relative to the Notarius claims:**
- Per-component provenance via the **ingredients** mechanism: each
  ingredient carries its own history and relation to the asset
  (parentOf / componentOf / inputTo) — this is exactly "an element inside
  a container with its own history." [E: yes, for asset components]
- Embedded in the creation and editing pipeline (cameras, editors,
  publishing platforms). [P: yes]
- Signed manifests, cryptographic binding. An industry
  standard with real adoption.

**What it does NOT cover:**
- The semantics of business fields: amount, IBAN, payee. C2PA answers
  "what content is assembled from," not "is the value of this invoice field
  legitimate."
- A break report in business-process terms ("the field was changed after
  the accountant approved it") — its model speaks of the provenance of
  content, not of authority over a field. [R: partial]

**Conclusion:** the §15 claim that "no provider of real-time
per-component provenance embedded in the pipeline exists" is
**REFUTED** for media and (as of v2.3) for text. For structured
business fields — not refuted.

## 2. in-toto / SLSA

**Current state:** in-toto is a general-purpose framework of signed
attestations (CNCF); arbitrary predicate types (SBOM, SCAI, runtime
traces); the community adopts new types. The Witness tool
(TestifySec) — pluggable custom predicates. SLSA — supply-chain
maturity levels on top of in-toto.

**Covers:** the model where "each transformation step is signed by its
own executor, and the chain is verifiable" — this is the skeleton of the Notarius TRACE,
already formalized and working. The framework is applicable beyond
CI/CD via custom predicates. [P: yes; E: at the level of the step's artifact]

**Does NOT cover:** there is no ready product for business documents;
granularity is the artifact, not the document field; reports are for engineers,
not for an accountant. [R: no]

**Conclusion:** the provenance-chain mechanism **exists and is open**;
what remains unoccupied is its application to document fields + a human-readable
layer.

## 3. Sigstore

**Current state:** keyless signing (Fulcio: a short-lived
certificate bound to an OIDC identity), the Rekor transparency
log (Rekor v2 — GA, cheaper to run), `cosign sign-blob` —
signing **arbitrary files**, a bundle with proof of inclusion
in the log.

**Covers:** the trusted-anchor infrastructure for document
provenance is ready: signing of any blob + a public immutable
log with a timestamp. It removes the §8 question "where does the receiver get the
public key" (identity = OIDC, log = Rekor). [P: as a service]

**Does NOT cover:** no semantics at all — neither elements, nor fields,
nor reports; identity is email/CI, not a business role. [E: no; R: no]

## 4. RFC 3161 / eIDAS / eIDAS 2.0

**Current state:** qualified timestamps (eIDAS) have
legal force in the EU; **eIDAS 2.0 (Reg. 2024/1183) introduces
Qualified Electronic Ledgers — a legal framework for ledger-based
evidence, full application by December 2026**. OpenTimestamps —
free anchoring of hashes in Bitcoin, courts accept it as proof
of existence.

**Covers:** trusted time (closes the §9 audit hole:
MODIFICATION_WINDOW is unprovable without external time) — with ready,
legally recognized means.

**Does NOT cover:** granularity is the container (whole document/hash);
provenance and authority are outside the model. [E: no; R: no]

## 5. W3C PROV (PROV-DM / PROV-O)

**Current state:** a standard provenance vocabulary (Entity/Activity/
Agent); real deployments — data science, healthcare
(ProvCaRe, G-Prov), GDPR compliance (GDPRov); recent 2025 work —
mapping onto BFO (ISO/IEC).

**Covers:** a ready, recognized **vocabulary** for Notarius records —
ORIGIN/TRACE/STATE can be expressed in PROV without inventing our own ontology.

**Does NOT cover:** PROV is a data model, not a mechanism: no tamper
protection, no trust, no product. [P: no; R: no]

## 6. The business-document protection market (nearest neighbor of the niche)

**E-invoicing:** EN 16931 — a semantic invoice model (mandatory
fields, machine-readable); Peppol eDelivery — integrity and non-repudiation
in transit; commercial implementations fix an issued invoice
with **immutable field snapshots + a hash of the tax payload** and
re-check before export. E-invoicing mandates are expanding in the EU
in 2026.

**Antifraud (BEC/invoice fraud):** commercial tools (Trustmi
and others) **check the IBAN of every incoming invoice against the supplier's
master record** and flag changes to payment details — that is, "detection
of a foreign insertion into a critical field" as a product exists, but
it is implemented as statistics/AI on top of master data, not as a provenance
chain.

**Conclusion:** the §15 claim that "detection of foreign insertions as an
infrastructure product does not exist" is **REFUTED** for
invoices (antifraud checking of details). It is NOT refuted for: portable
proof of a field's provenance across organizational boundaries
("who created this IBAN value, who changed it, where is the break") and for
documents outside networks like Peppol.

---

## SUMMARY MATRIX

| System | Element level | Embedded in pipeline | Human-readable break report | Trust mechanism |
|---|---|---|---|---|
| C2PA 2.3 | ✅ asset components (media+text) | ✅ | ⚠️ content, not business fields | signatures + certification |
| in-toto/SLSA | ⚠️ step artifact | ✅ CI/CD; extensible | ❌ | step signatures |
| Sigstore | ❌ | ✅ as a service | ❌ | OIDC + Rekor log |
| RFC 3161 / eIDAS 2.0 | ❌ container | ⚠️ | ❌ | legally recognized |
| W3C PROV | ✅ model | ❌ (not a mechanism) | ❌ | none |
| EN 16931 / Peppol | ✅ invoice fields | ✅ network | ⚠️ compliance reports | network + QES |
| BEC antifraud | ✅ payment fields | ✅ invoice stream | ⚠️ flag, not a chain | statistics/AI, not provenance |

**No single row closes all four columns at once — but
each column individually is closed by someone.**

---

## INPUT FOR THE VERDICT (the decision is the author's, AD-5)

1. The three "does not exist" claims from §15, in their original generality, are **not confirmed**:
   per-component provenance embedded in the pipeline exists (C2PA),
   provenance chains with step signatures exist (in-toto),
   detection of insertions into critical invoice fields exists (BEC antifraud).
2. What genuinely remains open (the narrow formulation):
   **portable provenance, verifiable across organizational boundaries,
   at the field level of an arbitrary business document, with a human-readable
   report of the break, available to small businesses outside closed networks.**
3. The character of the niche changes: it is a niche of **composition and product**
   (assemble it from ready primitives: PROV vocabulary + in-toto predicates +
   Sigstore/eIDAS anchor + our own semantic layer and reports), not a niche of a
   new security mechanism. For the project this is good news:
   there is less to build than assumed, and it is built on proven blocks.

RECOMMENDED VERDICT: `NICHE_NARROWED / COMPOSITION_PRODUCT /
MECHANISM_EXISTS_INTEGRATION_MISSING`

---

## Sources

- C2PA: [Explainer 2.4](https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html), [Implementation Guidance](https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html), [Content Credentials WP](https://c2pa.org/wp-content/uploads/sites/33/2025/10/content_credentials_wp_0925.pdf), [Wikipedia: Content Credentials](https://en.wikipedia.org/wiki/Content_Credentials), [c2paviewer: What is C2PA (2026)](https://c2paviewer.com/articles/what-is-c2pa)
- in-toto: [in-toto.io](https://in-toto.io/), [Attestation Framework](https://github.com/in-toto/attestation), [CNCF: Unleashing in-toto](https://www.cncf.io/blog/2023/08/17/unleashing-in-toto-the-api-of-devsecops/), [SLSA and in-toto](https://slsa.dev/blog/2023/05/in-toto-and-slsa), [Palantir on in-toto](https://blog.palantir.com/how-palantir-mastered-in-toto-b8a7107371bb)
- Sigstore: [Signing overview](https://docs.sigstore.dev/cosign/signing/overview/), [Signing blobs](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/), [Rekor v2 GA](https://blog.sigstore.dev/rekor-v2-ga/), [Rekor](https://github.com/sigstore/rekor)
- Timestamping/eIDAS: [SCRIPTed: Blockchain timestamps and eIDAS](https://script-ed.org/article/blockchain-based-electronic-time-stamps-and-the-eidas-regulation-the-best-of-both-worlds/), [eIDeasy Timestamping](https://www.eideasy.com/features/timestamping), [MDPI: Blockchain anchoring for timestamp tokens](https://www.mdpi.com/2076-3417/15/23/12722), [ProofSnap: OpenTimestamps](https://getproofsnap.com/posts/blockchain-timestamping.html)
- W3C PROV: [PROV-O](https://www.w3.org/TR/prov-o/), [Nature Sci Data 2025: PROV-O↔BFO](https://www.nature.com/articles/s41597-025-04580-1), [FAIR Cookbook: Provenance](https://fairplus.github.io/the-fair-cookbook/content/recipes/reusability/provenance.html)
- E-invoicing/antifraud: [Invoxo EN 16931](https://invoxo.eu/en-16931), [Peppol BIS Billing](https://docs.peppol.eu/poacc/billing/3.0/bis/), [Axway: Government e-invoicing](https://blog.axway.com/product-insights/b2b-integration/einvoicing/government-mandate-e-invoicing), [Arratech: EN 16931 update mid-2026](https://www.arratech.com/blog/en-16931-update-mid-2026-what-it-means-for-your-e-invoicing-infrastructure), [Trustmi: B2B fraud tools 2026](https://trustmi.ai/resource/best-b2b-fraud-detection-tools-software/), [Phacet: Invoice fraud detection AI](https://www.phacetlabs.com/blog/invoice-fraud-detection-ai)
