# Design review §6.2 SEMANTIC_LAYERED_DEFENSE — result (AD-2 → AD-11)

DATE: 2026-07-22
MANDATE: AUTHOR_DECISION AD-2 ("classification decided by the conveyor")
METHOD: executable experiment → 3 independent reviewers → synthesis
VERDICT: unanimous 3/3 — PRIVACY_OBSCURITY_PROPERTY /
NOT_A_SECURITY_BARRIER (recorded as AD-11)

## The experiment (reviewers' input)

`experiments/exp_6_2_reassembly.py`: a document of 7 typical business
fields is split into blocks, the blocks are shuffled, the manifest is
unavailable. The attacker (60 lines of regex) knows only the world's
formats (IBAN/dates/amounts), not the document's schema. Result:
**1000 trials, 7000 blocks, 100.0% of semantic types recovered without
a key and without a schema.**

## Three reviewers — unanimous

| Lens | Classification | Barrier? |
|---|---|---|
| Cryptography / Kerckhoffs | PRIVACY_OBSCURITY | no |
| Threat model | PRIVACY_OBSCURITY | no |
| Internal consistency | PRIVACY_OBSCURITY | no |

**Cryptographer:** "shuffled blocks without a manifest" is a transposition
cipher over plaintext values; broken by format analysis since the 19th
century. Barriers 2–4 are one secret (the design), which by Kerckhoffs
does not count. A layer with a non-quantifiable work factor counts as zero
in cryptography.

**Threat model:** works against a random observer; fails against a
scripted attacker with knowledge of the world (proven) and against a
motivated adversary. The only thing to survive the experiment was linkage
(tying roles together on repeating types) — and even that is UNVERIFIED,
needing a separate test.

**Consistency:** §6.2 conflicted with §8 (Kerckhoffs), with the project's
filter-formulas (AD-10), and with precedent AD-3. There is only one
resolution: Kerckhoffs applies everywhere; the property is reclassified,
like §6.3.

## The most dangerous thesis — removed

"Even a weak password + an unknown structure = meaningless mush" —
unanimously flagged for unconditional deletion: it inverts the economics
of security (it proposes compensating for the one real barrier with zero
layers — classic security through obscurity).

## Applied (AD-11)

All edits made to §6.2 of the working document and to the decision journal.
The §6 registry after three revisions: 6.1 PROPERTY_CANDIDATE,
6.2 privacy/obscurity, 6.3 diagnostic — all downgraded from "LOCKED."

## The property's honest remainder

Not a defense, but real: (1) friction for a random observer
(privacy); (2) integrity via a signed manifest — moves to §6.1;
(3) linkage obfuscation on repeating types — a candidate for a separate
experiment (a document pool, an attack on the links, not on the types).
