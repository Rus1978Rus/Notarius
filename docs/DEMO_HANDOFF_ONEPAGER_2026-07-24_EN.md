# Someone added a zero to your invoice. Would you notice?

You're sent an invoice for **1,000,000 ₽**.
On its way to you it was swapped — now it reads **9,000,000 ₽**.
One extra zero. Invisible to the eye.

You pay nine million instead of one.

---

## In the simplest terms

Our program looks at the document that arrived and says, in plain terms:

> "There was an amount of 1,000,000 here; it became 9,000,000.
>  This is a substitution. The real document is a different one."

Not "the file is safe." Not "access is locked."
But plainly: **here is the line — here is what was swapped in it.**

This is about any document that reaches you from another party: an invoice, an
acceptance certificate, a contract, a statement, a report, a data table. The
question is always the same:

**is what arrived genuine? or was it edited along the way?**
We answer — and we point a finger at where.

---

## A bit more detail — what this is as a product

Every piece of information has a **history**: where it came out of, what was done
to it along the way, whether it arrived untouched. Ordinary security tools guard
*where* the document is stored and whether it is locked. We keep its **history**
and reconcile it on receipt — and we do three things:

1. **Confirm the original** — yes, this is exactly what the source sent.
2. **Catch the substitution and name it** — what exactly was changed (the amount,
   a word), even if the edit was hidden so as to be invisible to the eye.
3. **Expose appropriation** — if someone declares another party's document their
   own after the fact, it shows.

**Who this hurts already today:** receiving documents from counterparties,
financial control, compliance, audit — anywhere paper moves between parties and
an extra zero costs money or reputation.

**What we sell, and what we don't.** We give the **engine of the honest history**:
signature, identification, the breakdown of "where the substitution is." Wiring
it into your specific process (buttons, reports, integration with your systems) is
written by you or your contractor. We are the motor; each person builds the body
for their own road.

**Honestly about the market.** The field is not empty: there are large players in
document storage and management. But they answer the question "*where* it is
stored and whether the file was stolen." None answers "*what exactly* in the line
was swapped." That is our unoccupied corner.

---

> ↓ **Below — material for your technical specialists.**
> If you understand up to this point why it's needed, below is what's worth
> handing to your people for verification.

## How it works (for specialists)

**Three independent supports** that must converge:

- **Digital signature** (Ed25519 / libsodium) — the source signs the document; a
  stranger without the key won't forge the signature.
- **Independent witnesses** — external nodes co-sign the *first* seal on a
  document by quorum (M-of-N); a conflicting claim on the same hash is refused.
  One hijacked key doesn't flip the picture.
- **A public append-only registry** ("the registry under glass") — a hash chain,
  the "first-wins" rule, not rewritable after the fact. You can only draw "on the
  glass" of delivery — reconciliation against the registry exposes it
  (`FORGERY_ON_GLASS`).

**Localizing the substitution (our center).** We don't issue a "yes/no touched."
The diagnostic module classifies the change: value substitution
(1000000→9000000), insertion of an invisible code point, loss of characters on
re-encoding, rewritten content — and shows **what exactly** and where.

**A summary verdict.** The three supports converge into one human-readable
outcome: `ANCHORED_CONFIRMED` (original, everything converged) · `CONTESTED`
(divergence / suspicion of a mirror substitution) · `FORGERY_ON_GLASS`
(appropriation exposed) — with an explanation of "why."

**Works on any element.** Not just on a code file: a document, a record, a data
field, media — the model is one.

**Honest boundaries (important for due diligence):**
- Signed ≠ genuine in meaning (`SIGNED ≠ NATIVE`): a signature under coercion or
  with a hijacked key is outside the crypto guarantee.
- We show **where** the lie is — we don't prove the sanctity of the rest ("the
  trace finds the lie ≠ proves the truth"); a human decides on intent.
- The strength of reconciliation = how **independent** the registry is and whether
  receipt actually reconciles.
- Threshold signing (FROST) is a reference for us, not production (production =
  Rust FFI). We do not replace legal expertise and admissibility in court.

**Where to look:** the demo run `scripts/handoff_demo.py`; the core
`notarius/{title,anchor,diagnose,cosign,frost}.py`; the definition of the approach
`docs/SEMANTIC_TRACE_CANON_2026-07-23_EN.md`.

---

_Give us one of your own real handoff documents — we'll run the same thing on it
and show, on your data, where and what we catch._
