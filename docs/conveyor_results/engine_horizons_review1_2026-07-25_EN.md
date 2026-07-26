# Synthesis: review of engine application horizons #1

DATE: 2026-07-25. STATUS: LLM_GENERATED (a digest of an external
reviewer's answer to prompt AD-73). The reviewer's raw answer is
EXTERNAL_VENDOR, inserted by the author into docs/vendor_answers/. This is
1 of N; the synthesis is preliminary.

IMPORTANT REVIEWER CAVEAT: his web search returned 401 → competitor names
are given from memory, NOT a fresh market scan. Treat as indicative, not
final.

## What the reviewer CONFIRMED (independently of us)

The most valuable part: he independently arrived at our own framing. The
engine's value is not "sign a document" but:
> **prove the origin and localize the change of a few critical fields
> AFTER permissible transformations and a transition between incompatible
> systems**, with an explainable verdict for a non-cryptographer.
This is direct external confirmation of the "tampering localizer" (our
brick #1).

## His top 3 bets

1. **Financial critical fields (5/5).** Supplier details (IBAN/BIC/
   payee) across the transition email→PDF→portal→ERP→bank. KEY SHARPENING:
   sign the **structured object** (supplier record), NOT the PDF hash.
   Otherwise we lose to the existing signature. There is a blocking action
   (don't pay until an out-of-band confirmation).
2. **Agent Configuration Provenance (5/5, field NOT yet settled).**
   Evidence of which system-instructions / tool-schemas / endpoints /
   permissions actually reached the agent's runtime, and localization of
   changes. NEW — we underrated it.
   Call it "Agent Configuration Provenance," NOT "AI firewall."
3. **Lab/industrial field-level chain of custody.** Matches
   our pivot AD-59. Strong, but long sales cycles + certification.

## What the reviewer SHOT DOWN (we accept it honestly)

- **Integrity-VPN — NO.** TLS/QUIC/IPsec already prove integrity in
  session; if the endpoint is compromised, a transport signature won't
  help. (Directly refutes my "wild" bet on a VPN.)
- **A universal prompt-injection firewall — NO** (Unicode is a small part).
- **Camera/deepfake — a red ocean** (C2PA/CAI are already building it).
- **Universal signature / a new Git / IPFS / blockchain proof /
  a shared global registry of first publication — NO** (a governance trap).
- **"First wins" as a name registry — NO** (squatting, disputes, revocation).
- **Signature = truth — categorically NO** (we knew this ourselves).

## The strongest counterargument (block 4) — keep it in mind

All four primitives have long existed; the bottleneck is NOT the
comparison/hash but the **trusted point of entry, key management,
embedding the check, and the parties accepting the verdict**. And:
**localization is not valuable everywhere** — for a binary/certificate/
command, any mismatch = "don't run," and localization is unneeded.
It is valuable where a human resolves a dispute or a policy distinguishes
fields. This narrows the market. Horizontally, the engine remains a
**library/research**; a product appears only under a vertical contract
with 7 conditions:

1. a trusted moment of capture is defined;
2. the data structure is known;
3. the permissible transformations are specified;
4. the critical fields are singled out;
5. there is a mandatory checkpoint;
6. the verdict triggers a concrete action;
7. it is defined who pays for the risk reduction.

## Non-identification (block 5)

Almost everything already exists as classes of products; there is no new
general primitive. What's promising is not a single machine but a
**combination**: canonicalization → structural fingerprint → domain
classification of changes → machine action (e.g.
a "RAG-corpus regression analyzer," not a "Unicode normalizer").

## Wild cards worth attention

- **#11 "contract on silence"** — catch not the changed events but the ones
  that **DIDN'T appear** — a mandatory event that's missing (a skipped
  report/heartbeat/warning). Fresh.
- **#1 "decision archaeology"** — record the facts/rules of a decision, then
  show which original fact made an old decision no longer reproducible.
- **#12 "canonical clipboard"** for critical values (IBAN, wallet
  address, shell command, dose) — provenance before the paste.
- **#10 "what the agent saw"** — record the RAG selection/DOM/tool results.

## Our reaction and recommendation

The review did its disciplined job: it sharpened #1, produced a new strong
candidate (agent-config), honestly killed the weak bets (VPN etc.), and
gave a testable product criterion (7 conditions + pilot metrics).
CONCLUSION: narrow to ONE vertical and test it against the 7 conditions
and a minimal experiment (100–500 real objects; FP/FN; the share of
"disputable"; whether localization cuts manual review several-fold;
whether the customer is willing to block the process on a verdict).

FOCUS CANDIDATES: (A) financial fields — acute monetary pain, a clear
buyer, a blocking action; (B) agent-config provenance — fresh, unoccupied
field, growing demand. Advice: A as the most "sellable," B as the most
"unoccupied." Before focusing — gather 1–2 more reviewers for
triangulation.
