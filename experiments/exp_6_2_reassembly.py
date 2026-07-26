"""Experiment for design-review §6.2 SEMANTIC_LAYERED_DEFENSE (AD-2).

The §6.2 claim under test:
  "Encryption: break the key → you get everything.
   Notarius: break the key → you get shards with no assembly instructions.
   Even a weak password + an unknown semantic structure =
   the attacker gets meaningless mush."

Setup: a small-business document is split into value blocks, the blocks
are shuffled, and the manifest (the trace key) is unavailable to the
attacker. The attacker does NOT know the schema of the specific document
but knows the world (Kerckhoffs): what IBANs, dates, amounts, currencies,
and statuses look like.

The attacker = 60 lines of format heuristics. If they recover the
semantic types of the blocks, then "meaningless mush" is refuted for
structured data.
"""

from __future__ import annotations

import random
import re

FIELDS = {
    "iban": ["UA213223130000026007233566001", "DE89370400440532013000",
             "PL61109010140000071219812874", "FR1420041010050500013M02606"],
    "amount": ["100000.00", "250.50", "9999.99", "1200000.00"],
    "currency": ["UAH", "EUR", "USD", "PLN"],
    "date": ["2026-07-22", "2026-01-15", "2025-12-31", "2026-03-08"],
    "recipient": ["Company Alpha LLC", "Beta Trading GmbH",
                  "Gamma Logistics Sp. z o.o.", "Delta Services SARL"],
    "status": ["APPROVED", "PENDING", "REJECTED", "DRAFT"],
    "order_id": ["INV-458", "ORD-2214", "INV-9001", "PO-777"],
}

STATUS_VOCAB = {"APPROVED", "PENDING", "REJECTED", "DRAFT", "PAID"}
CURRENCY_VOCAB = {"UAH", "EUR", "USD", "PLN", "GBP", "CHF"}


def classify(block: str) -> str:
    """The attacker: the block type from the value's format alone."""
    if re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", block):
        return "iban"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", block):
        return "date"
    if block in CURRENCY_VOCAB:
        return "currency"
    if block in STATUS_VOCAB:
        return "status"
    if re.fullmatch(r"[A-Z]{2,4}-\d+", block):
        return "order_id"
    if re.fullmatch(r"\d+(\.\d{2})?", block):
        return "amount"
    if re.fullmatch(r"[A-Z][\w.]*(\s+[\w.&-]+)+", block):
        return "recipient"
    return "unknown"


def run_trial(rng: random.Random) -> tuple[int, int]:
    doc = {f: rng.choice(vals) for f, vals in FIELDS.items()}
    blocks = list(doc.values())
    rng.shuffle(blocks)  # a bundle with no manifest
    truth = {v: f for f, v in doc.items()}
    hits = sum(1 for b in blocks if classify(b) == truth[b])
    return hits, len(blocks)


def main(trials: int = 1000, seed: int = 42) -> float:
    rng = random.Random(seed)
    hit_total = n_total = 0
    for _ in range(trials):
        h, n = run_trial(rng)
        hit_total += h
        n_total += n
    rate = hit_total / n_total
    print(f"Trials: {trials}, blocks: {n_total}")
    print(f"Semantic types recovered WITHOUT the key or schema: {rate:.1%}")
    verdict = ("REFUTED: structured business fields self-identify by format "
               "— shuffling without a manifest does not produce "
               "\"meaningless mush\"."
               if rate > 0.9 else
               "The §6.2 claim held up on this set of fields.")
    print(f"Verdict on \"meaningless mush\": {verdict}")
    return rate


if __name__ == "__main__":
    main()
