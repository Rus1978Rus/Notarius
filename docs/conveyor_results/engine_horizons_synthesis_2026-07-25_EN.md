# Cross-synthesis: engine application horizons (reviewers #1 + #2 + #3/Kimi + #4)

DATE: 2026-07-25. STATUS: LLM_GENERATED (consolidating FOUR independent
answers to prompt AD-73). The raw answers are EXTERNAL_VENDOR, inserted by
the author into vendor_answers. 4 of N. SPECIAL: reviewer #3 (Kimi) had
access to the repository and VERIFIED the claims BY EXECUTION — he found
real defects (see below). #1 and #2 worked from the description, web search
failed → their "taken/empty" calls are indicative; Kimi named competitors
more precisely; #4 (PDF, with references to C2PA/TUF/ipfs-log) is the
LEAST critical, prone to a marketing tone (see the block on him).

## CONVERGENCE OF THREE (independently, the same thing)

1. **The differentiator is LOCALIZING the type of change**, not the
   signature (all three).
2. **Documents between parties** — the strongest vertical for all three.
3. **THE DECIDING RISK — "who actually reconciles, and why?"** There is
   value only if the consumer reconciles against an INDEPENDENT journal;
   otherwise it's a free hash+diff.
4. **Shared kill-list:** Integrity-VPN (TLS/zkTLS), camera/deepfake (C2PA
   is already in silicon: Leica/Sony/Canon/Pixel 10), code supply-chain
   (Sigstore/SLSA — "don't go there"), universal signature/Git/IPFS/ledger/
   blockchain-notary (Guardtime — "corpses along the road"), a standalone
   Unicode cleaner.
5. **The engine makes tampering visible, not impossible; it does not prove
   truth.**

## WHAT KIMI ADDED BEYOND #1/#2 (the most valuable)

**A. Verified by execution — 3 REAL DEFECTS (engineering debt):**
1. **Homoglyph** (Cyrillic "а" in "admin") passes as OK in the standalone
   scanner; in check it is caught only as "CONTENT_CHANGED, not
   classified."
   → homoglyph detection is weaker than claimed.
2. **Backdating:** a trace event with a past date is accepted and verify →
   INTACT. "Backdating is impossible" holds ONLY with an external anchor
   (OTS/witness quorum). The README honestly admits this as defect #3.
3. **cosign fail-open:** verify_witnessed_trace on an unwitnessed head →
   INTACT + a textual warning (which an API consumer will ignore).
   Where fail-closed is needed, it's a soft fail-open.

**B. Sharpening the vertical:** documents between parties **OUTSIDE the EDM
perimeter** (email/messengers). Why it's a moat: EDM (Diadoc/DocuSign) is
by definition closed onto its own perimeter and structurally CANNOT reach
the gray channels where invoice-fraud/BEC actually lives.

**C. A new empty niche — "Version handshake":** provable agreement on
versions (a spec / a mockup / a contract revision) between organizations
WITHOUT a shared platform (our trace with break detection). No direct
product on the market.

**D. A friction-reducing bridge — a word-fingerprint across the carrier
boundary** (human_fingerprint.py, already built): "dictate a contract
version over the phone and reconcile it." No one has a ready
implementation (PGP word list/BIP-39 are adjacent). It removes the main
objection: "I don't want to install software for a single reconciliation."

**E. The sharpest counterargument:** inside a perimeter (EDM/bank),
immutability is delivered by an ordinary operator journal for pennies —
crypto is unneeded for someone you already trust with money. Outside the
perimeter the value hinges on the human: BEC survives precisely because
people DON'T reconcile. The market pays not for "yet another way to prove
bit-identity" but for BEING EMBEDDED in the workflow (the engine = 5% of
the cost).

## REVIEWER #4 — an outlier on ratings, but a 4th confirmation of the risk

The least critical. HIS TOP 3 CONTRADICTS the other three: it puts
prompt-injection, camera/IoT, and **Integrity-VPN** on top, and calls
documents/finance a "trap" (the DocuSign red ocean). BUT his rationale for
VPN/camera is exactly the naive "our engine is more universal and lighter"
that Kimi already demolished with specifics (C2PA in Leica/Sony/Canon/
Pixel 10 silicon; VPN closed off by TLS/zkTLS). So we weight his ratings
LOW. Caveat: his "documents = a trap" is about GENERAL e-signature
(everyone agrees with that); he did NOT single out the narrow niche of
field-localization outside the perimeter that #1/Kimi praise — so he
doesn't refute it, he misses it.

VALUABLE FROM #4 (agreeing with all — a 4th independent confirmation):
- "A tool for EXPOSURE, not for trust"; "for the after-the-fact
  investigation of attacks, not their prevention."
- Three limitations (the same ones): (1) trust in the journal itself — if
  the journal is under the attacker, it simply won't record; (2) an ACTIVE
  consumer is needed — people ignore warnings; (3) WHAT, not WHY — it
  doesn't judge intent.
- A USEFUL SHARPENING: the product is viable where audit/provability is a
  **legislative/regulatory REQUIREMENT** (legal/finance/government).
  This refines "who actually reconciles": regulation COMPELS
  reconciliation, removing the problem of human indiscipline.

## DIVERGENCES

- **AI-Unicode:** #2 — a hot product; #1 and Kimi — only a component/OSS
  (Context Guard already sells exactly "invisible Unicode"; Lakera/MS/Meta
  do the rest). Result 2:1 → a feature/component, NOT a standalone product.
- **Code supply-chain:** #2 has it in the top 3, but #1, Kimi, and our live
  scan AD-57 → a red ocean. Result 3:1 → we don't go there.
- **Financial fields vs documents-outside-EDM:** essentially the same
  thing (BEC/detail tampering = documents in gray channels); Kimi merges
  them and adds the deciding condition — being embedded in email/messenger.

## CONVERGING WILD CARDS (named independently — a strong signal)

- **Integrity/provenance of AI answers and memory** (all three touch on
  it): sealing LLM answers + proof of inclusion in a training dataset
  (rightsholders' lawsuits hinge on exactly this) + "anti silent re-write"
  of an agent's memory.
- **Attestation of "what the agent saw"** (#1, #2).
- **Archaeology of artifacts/decisions** (#1, #2).
- **An incorruptible draw / a neutral queue** (#1 mentions it, Kimi
  develops it).

## MAIN CONCLUSION (after three)

Triple convergence: **the vertical is verifying documents/details between
parties OUTSIDE closed perimeters**, and it works ONLY as a product
**embedded in the workflow** (an email plugin/bot), not a standalone
utility — otherwise it dies of human reconciliation indiscipline. This
connects directly to our own distribution model AD-69 ("the engine is
sewn into email/CRM") and explains WHY that was the right intuition.

The cheap bridge to adoption — the **word-fingerprint** (already in the
code): it lets you reconcile "without installing software."

## WHAT TO FIX BEFORE ANY PILOT (debt found by Kimi)

1. Homoglyphs — bring to a classified verdict, not "CONTENT_CHANGED."
2. Anti-backdating — make an external anchor (OTS/quorum) mandatory for
   the claim "date is proven," otherwise don't promise it.
3. cosign — fail-CLOSED on an unwitnessed head (not INTACT+warning).

## RECOMMENDATION

Focus — **documents/details outside EDM, embedded in email/messenger**
(merges #1's financial fields and #1-Kimi's documents). AI-Unicode — as an
OSS component, not a product. Don't touch the kill-list. Before a pilot,
close Kimi's 3 defects.

Of the FOUR reviewers: #4's ratings (for VPN/camera) don't pass — his
rationale is already demolished by Kimi's specifics. But ALL FOUR
independently converged on the deciding risk ("who actually reconciles" +
trust in the journal). #4 added the key to that risk: **regulatorily
mandatory verification** — the most natural home, where reconciliation is
COMPELLED (legal/finance/government) rather than hoped for through
discipline. This narrows the first vertical even more precisely:
documents/details outside the perimeter THERE, WHERE verification is
prescribed by regulation/law. The 4th reviewer didn't change the
conclusion but reinforced it and sharpened the "where." Gathering further
reviewers is unnecessary.
