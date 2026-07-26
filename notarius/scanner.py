# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS v2 — scanner for invisible code points with context and x-ray.

Improvements over v1 (find_invisibles), source — cross-material from
Gemini (docs/vendor_answers/gemini_offprompt_2026-07-21.md) and lessons
from judging the pipeline:

1. Neighbor context: an invisible BETWEEN letters/digits (adm<BOM>in) —
   high suspicion; at a block boundary / after punctuation — likely glue
   or a service artifact. Reduces false positives.
2. X-ray projection: a string with the invisibles made visible
   ("adm[U+FEFF]in") — a human tells sabotage from glue in a second.
3. LIKELY_LEGITIMATE class for variation selectors: C2PA 2.3 embeds text
   manifests via VS (U+FE00–FE0F, U+E0100–E01EF), and VS16 is legitimate
   in emoji — a judging lesson: don't flag the standard as an attack.
4. Advisory mode: the scanner sorts by suspicion and blocks nothing (the
   principle of early Notarius + Gemini's variant 4).
"""

from __future__ import annotations

import unicodedata

VARIATION_SELECTORS = set(range(0xFE00, 0xFE10)) | set(range(0xE0100, 0xE01F0))

SUSPICION_HIGH = "HIGH"          # invisible inside a word
SUSPICION_MEDIUM = "MEDIUM"      # invisible in other positions
SUSPICION_LIKELY_LEGIT = "LIKELY_LEGITIMATE"  # variation selectors


def _is_invisible(ch: str) -> bool:
    return unicodedata.category(ch) == "Cf" or ord(ch) in VARIATION_SELECTORS


def _xray(ch: str) -> str:
    return f"[U+{ord(ch):04X}]"


def scan(text: str) -> dict:
    """Report on invisible code points: findings with context and suspicion
    level (sorted descending) + an x-ray projection of the text."""
    findings = []
    xray_parts = []
    for i, ch in enumerate(text):
        if not _is_invisible(ch):
            xray_parts.append(ch)
            continue
        xray_parts.append(_xray(ch))
        left = text[i - 1] if i > 0 else ""
        right = text[i + 1] if i + 1 < len(text) else ""
        inside_word = left.isalnum() and right.isalnum()
        if ord(ch) in VARIATION_SELECTORS:
            level = SUSPICION_LIKELY_LEGIT
            note = "variation selector: legitimate in emoji and C2PA text manifests"
        elif inside_word:
            level = SUSPICION_HIGH
            note = f"invisible code point INSIDE a word: {left}{_xray(ch)}{right}"
        else:
            level = SUSPICION_MEDIUM
            note = "invisible code point at a boundary / in a service position"
        findings.append({
            "index": i,
            "codepoint": f"U+{ord(ch):04X}",
            "name": unicodedata.name(ch, "UNKNOWN"),
            "suspicion": level,
            "context": f"{left}{_xray(ch)}{right}",
            "note": note,
        })
    order = {SUSPICION_HIGH: 0, SUSPICION_MEDIUM: 1, SUSPICION_LIKELY_LEGIT: 2}
    findings.sort(key=lambda f: (order[f["suspicion"]], f["index"]))
    return {
        "clean": not findings,
        "counts": {lvl: sum(1 for f in findings if f["suspicion"] == lvl)
                   for lvl in (SUSPICION_HIGH, SUSPICION_MEDIUM,
                               SUSPICION_LIKELY_LEGIT)},
        "findings": findings,
        "xray": "".join(xray_parts),
    }


def scan_hardened(text) -> dict:
    """Hardened pass (AD-33, the engine from Vakhter).

    scan() above is our v2: it only flags Cf code points and sorts them by
    suspicion (advisory, without attack context). scan_hardened adds real
    detection from notarius.detect on top:
      - canonicalization (reveals percent/entity/overlong evasion BEFORE reading);
      - ALARM on a proven smuggle (word-split, bidi imbalance
        CVE-2021-42574, tag smuggle, VS carrier, parser desync);
      - OK on legit glue (emoji ZWJ, VS after a base, balanced bidi);
      - WATCH on an unknown invisible.
    Returns the detect.analyze verdict, enriched with the v2 x-ray projection.
    Advisory mode — it blocks nothing.
    """
    from notarius.detect import analyze
    verdict = analyze(text)
    if isinstance(text, str):
        verdict["xray"] = scan(text)["xray"]
        # Homoglyphs (AD-79): a standalone scanner without a reference raises
        # an alarm on a MIX of scripts within a word (Cyr./Lat. in one word).
        from notarius.homoglyph import mixed_script_words
        mixed = mixed_script_words(text)
        if mixed and verdict.get("risk") != "ALARM":
            verdict["risk"] = "ALARM"
            verdict["signature"] = "homoglyph_mixed_script"
            verdict["homoglyph_words"] = mixed
        # Domain/URL context (AD-81): a lookalike/invisible IN THE DOMAIN or a
        # userinfo spoof — more specific and more dangerous than a general mix.
        # It overrides the signature.
        from notarius.urlcontext import scan_url
        uc = scan_url(text)
        if uc["findings"]:
            verdict["url_context"] = uc["findings"]
            if uc["risk"] == "ALARM":
                verdict["risk"] = "ALARM"
                verdict["signature"] = uc["signature"]   # homoglyph_in_host/…
            elif verdict.get("risk") == "OK":
                verdict["risk"] = "WATCH"
                verdict["signature"] = uc["signature"]
    return verdict
