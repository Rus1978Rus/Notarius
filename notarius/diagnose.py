# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — break diagnostician: WHAT exactly changed (AD-42).

Following the adversarial experiment (AD-41): verify localizes "where it
broke", but does NOT describe "what" — the thief (1000→9000), an iconv
loss, and NFKC all gave ONE verdict. The diagnostician compares original
and current and CLASSIFIES the change — as a CLUE for a human, NOT as a
verdict on intent (TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH). This
is growth of the CENTER — a human-readable assembly of the history, not
plumbing.

Categories (in priority order):
  VALUE_SUBSTITUTION      — numeric values changed (1000→9000)       [review]
  INVISIBLE_INSERTION     — invisible code points inserted           [review]
  HOMOGLYPH_SUBSTITUTION  — letters swapped for lookalikes (Cyr/Grk)  [review]
  NORMALIZATION_EQUIVALENT— bytes differ, but NFKC-equivalent        [low]
  CHAR_LOSS               — characters lost during transcoding       [medium]
  CONTENT_CHANGED         — changed, not classified                  [medium]
  IDENTICAL               — no change                                [none]
"""

from __future__ import annotations

import re
import unicodedata

from notarius.detect import _monitored
from notarius.homoglyph import confusables_in, deconfuse

_DIGITS = re.compile(r"\d+")

_REVIEW = {
    "IDENTICAL": "none",
    "NORMALIZATION_EQUIVALENT": "low",
    "CHAR_LOSS": "medium",
    "CONTENT_CHANGED": "medium",
    "INVISIBLE_INSERTION": "high",
    "HOMOGLYPH_SUBSTITUTION": "high",
    "VALUE_SUBSTITUTION": "high",
}

_INTENT_NOTE = ("a clue, not a verdict: intent (attack or an innocent "
                "environment) is decided by a human/policy — TRACE_LOCATES_THE_LIE")


def _invisibles(s: str) -> list[str]:
    return [c for c in s if _monitored(c)]


def diagnose_change(original: str, current: str) -> dict:
    """Classify the change original→current. Returns
    {category, review, changed, details, human, intent_note}."""
    if original == current:
        return _mk("IDENTICAL", {}, "no change", changed=False)

    # 1. Numeric value substitution — the most important for review.
    nums_o, nums_c = _DIGITS.findall(original), _DIGITS.findall(current)
    if sorted(nums_o) != sorted(nums_c):
        return _mk("VALUE_SUBSTITUTION",
                   {"before": nums_o, "after": nums_c},
                   f"numbers changed {nums_o}→{nums_c} — FOR REVIEW")

    # 2. Invisibles inserted (content axis).
    inv_o, inv_c = _invisibles(original), _invisibles(current)
    if len(inv_c) > len(inv_o):
        gained = sorted({f"U+{ord(c):04X}" for c in inv_c}
                        - {f"U+{ord(c):04X}" for c in inv_o})
        return _mk("INVISIBLE_INSERTION", {"inserted": gained},
                   f"invisible code points inserted {gained} — hidden insertion")

    # 2.5. Lookalike characters (homoglyph): same appearance, different script.
    # "admin" → "аdmin" (Cyr. а): no numbers, no invisibles, NFKC does NOT
    # reduce it. Caught if lookalikes appeared in current AND the appearance
    # (deconfuse) matched.
    conf_o, conf_c = confusables_in(original), confusables_in(current)
    if len(conf_c) > len(conf_o) and deconfuse(current) == deconfuse(original):
        got = sorted({f"U+{ord(c):04X}({c})" for c in conf_c}
                     - {f"U+{ord(c):04X}({c})" for c in conf_o})
        return _mk("HOMOGLYPH_SUBSTITUTION", {"lookalikes": got},
                   f"letters swapped for lookalikes {got} — looks like the "
                   f"original, but the characters are from another script")

    # 3. NFKC-equivalent → probably innocent normalization.
    if unicodedata.normalize("NFKC", original) == unicodedata.normalize("NFKC", current):
        return _mk("NORMALIZATION_EQUIVALENT", {},
                   "bytes differ, but NFKC-equivalent (ligatures/width/"
                   "compatibility) — probably innocent normalization")

    # 4. Character loss (transcoding/gateway): unrepresentable ones dropped.
    lost = sorted({c for c in original if ord(c) > 127} - set(current))
    if lost or "�" in current or ("?" in current and "?" not in original):
        show = [f"U+{ord(c):04X}" for c in lost] or ["<replacement/�>"]
        return _mk("CHAR_LOSS", {"lost": show},
                   f"characters lost during transcoding {show} — "
                   f"check whether anything important was lost")

    # 5. Changed, but not classified.
    return _mk("CONTENT_CHANGED", {}, "content changed (not classified)")


def _mk(category: str, details: dict, human: str, changed: bool = True) -> dict:
    return {"category": category, "review": _REVIEW[category], "changed": changed,
            "details": details, "human": human, "intent_note": _INTENT_NOTE}


def assemble(original: str, current: str) -> dict:
    """③ A single human-readable report: signature axis (bytes matched?) +
    content axis (scan) + diagnostician. Assembles what we have into one verdict."""
    from notarius.scanner import scan_hardened
    diag = diagnose_change(original, current)
    scan = scan_hardened(current)
    bytes_match = original == current
    return {
        "bytes_match": bytes_match,                    # signature axis: would the hash match?
        "content_scan": {"risk": scan["risk"], "signature": scan["signature"]},
        "diagnosis": diag,
        "review": diag["review"],
        "human": (f"[{'MATCH' if bytes_match else 'BREAK'}] "
                  f"{diag['category']} ({diag['review']}): {diag['human']}"),
    }
