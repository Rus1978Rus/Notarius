# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — engine for detecting invisibles/bidi/confusables (AD-33).

PORTED from the sibling project Vakhter (rus1978rus/vakhter @ 3763b71;
same author — Ruslan Malyavskiy). Carried over verbatim:
  - Finding                     (invariant_engine/core.py)
  - invisible_cards_reader      (code/range/invisible_cards.py)
  - canonical_view + reader     (code/range/canonical_view.py)
  - safe_reader / safe_analyze  (code/range/fail_closed.py)

WHY (vs our naive scanner.scan()): our v2 scanner only flags Cf code
points and sorts them by suspicion — it does NOT tell a Trojan-Source RLO
from an emoji ZWJ, does not catch bidi imbalance, does not decode a tag
block, does not see parser desync. This engine can do that:
  ALARM (conclusive): word-split by an invisible, bidi imbalance
    (CVE-2021-42574), tag smuggle with no flag base, VS carrier, parser desync.
  OK (clean): all invisibles are legitimate glue (emoji ZWJ, VS after a
    base, tag after a flag, balanced bidi).
  WATCH: an invisible is present, but it is neither a proven smuggle nor a
    provable glue.

CANDID BOUNDARY: this is a port of Vakhter's DRAFT logic (marked there as
a "SIMULATOR of a draft", without pipeline validation). Here it is covered
by our OWN tests (tests/test_detect.py) — behavior is checked, not
"security". We do not pass it off as a certified detector. Advisory mode
(like all of Notarius); it blocks nothing automatically.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from notarius.canon import canonicalize


# --- Finding (port of invariant_engine/core.py) ----------------------

@dataclass
class Finding:
    """What a "reader" returns about ONE input (its nature)."""
    label: str          # "clean" | "suspect"
    strength: float     # 0..1 — how strongly / clearly
    reason: str         # human-readable explanation
    conclusive: bool = False   # damning on its own
    signature: str = ""        # stable key


def risk_of(f: Finding) -> str:
    """clean→OK; suspect+conclusive→ALARM; suspect→WATCH."""
    if f.label == "clean":
        return "OK"
    return "ALARM" if f.conclusive else "WATCH"


def _severity(f: Finding) -> int:
    if f.label == "clean":
        return 0
    return 2 if f.conclusive else 1


def combine(*findings: Finding) -> Finding:
    """Severity-max, add-only: the map can only RAISE suspicion."""
    real = [f for f in findings if f is not None]
    if not real:
        return Finding("clean", 0.0, "no findings")
    return max(real, key=_severity)


# --- inventory of invisible code points ------------------------------

ZERO_WIDTH = {0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x00AD}   # zwsp zwnj zwj wj bom shy
BIDI_OPEN = {0x202A, 0x202B, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068}  # LRE RLE LRO RLO LRI RLI FSI
BIDI_CLOSE = {0x202C, 0x2069}                                   # PDF PDI
TAG = range(0xE0000, 0xE0080)                                   # tag characters
VS = set(range(0xFE00, 0xFE10)) | set(range(0xE0100, 0xE01F0))  # variation selectors
FLAG_BASE = 0x1F3F4                                             # black flag (legit tag-seq base)


def _wordish(ch):
    return bool(ch) and ch.isalnum()


def _emoji_ish(ch):
    if not ch:
        return False
    return ord(ch) >= 0x1F000 or unicodedata.category(ch).startswith("S")


def _is_invisible(ch):
    o = ord(ch)
    return o in ZERO_WIDTH or o in BIDI_OPEN or o in BIDI_CLOSE or o in TAG or o in VS


def _monitored(ch):
    """The WHOLE monitored class, not just our 6 characters (AD-35, a
    generalization). Measurement showed: characters without an explicit card
    had a SILENT pass (verdict=OK), even though an invisible in a token/host
    is never legitimate. The fix is not to "add more cards" but to widen the
    class: Cf (format) ∪ default-ignorable ∪ VS. Then any monitored character
    is at least witnessed (does not stay silent)."""
    return (_is_invisible(ch) or _default_ignorable(ch)
            or unicodedata.category(ch) == "Cf")


# --- conclusive smuggle checks ---------------------------------------

def _zw_wordsplit(text):
    for i, ch in enumerate(text):
        if ord(ch) in ZERO_WIDTH:
            prev = text[i - 1] if i > 0 else ""
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if _emoji_ish(prev) or _emoji_ish(nxt):
                continue
            if _wordish(prev) and _wordish(nxt):
                return Finding("suspect", 0.85,
                    f"zero-width U+{ord(ch):04X} splits a word "
                    f"('{prev}‹zw›{nxt}') — invisible smuggle",
                    conclusive=True, signature="zw_wordsplit")
    return None


def _bidi_imbalance(text):
    opens = sum(1 for c in text if ord(c) in BIDI_OPEN)
    closes = sum(1 for c in text if ord(c) in BIDI_CLOSE)
    if opens and opens != closes:
        return Finding("suspect", 0.9,
            f"unbalanced bidi controls (open={opens}, close={closes}) — "
            f"Trojan-Source-style reordering (CVE-2021-42574)",
            conclusive=True, signature="bidi_imbalance")
    return None


def _tag_smuggle(text):
    tags = [c for c in text if ord(c) in TAG]
    if tags and FLAG_BASE not in (ord(c) for c in text):
        return Finding("suspect", 0.9,
            f"{len(tags)} tag character(s) U+E00xx with no flag base — "
            f"invisible ASCII smuggle", conclusive=True, signature="tag_smuggle")
    return None


def _vs_carrier(text):
    run = best = 0
    for c in text:
        if ord(c) in VS:
            run += 1
            best = max(best, run)
        else:
            run = 0
    if best >= 3 or (text and ord(text[0]) in VS):
        return Finding("suspect", 0.8,
            f"a run of variation selectors (max {best}) as a data carrier",
            conclusive=True, signature="vs_carrier")
    return None


def _any_monitored_wordsplit(text):
    """GENERALIZATION of zw_wordsplit to the WHOLE monitored class (AD-35,
    variant C). Any monitored character (not only our 6 zero-width ones) that
    splits a token/host between two alphanumerics is a bypass of a byte
    comparison, and never legitimate. Closes 135-of-138 at once, not 4 cards.
    ZERO_WIDTH excluded — already caught by _zw_wordsplit (its own signature)."""
    for i, ch in enumerate(text):
        if not _monitored(ch) or ord(ch) in ZERO_WIDTH:
            continue
        prev = text[i - 1] if i > 0 else ""
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if _emoji_ish(prev) or _emoji_ish(nxt):
            continue
        if _wordish(prev) and _wordish(nxt):
            return Finding("suspect", 0.8,
                f"monitored invisible U+{ord(ch):04X} "
                f"({unicodedata.name(ch, '?')}) splits a token "
                f"('{prev}<inv>{nxt}') — byte-comparison bypass",
                conclusive=True, signature="host_break")
    return None


def _first_smuggle(text):
    # Specific checks first (their own signatures), then the generalized one.
    for chk in (_zw_wordsplit, _bidi_imbalance, _tag_smuggle, _vs_carrier,
                _any_monitored_wordsplit):
        f = chk(text)
        if f:
            return f
    return None


# --- legit glue (vouch) ----------------------------------------------

def _legit_glue(text, i):
    o = ord(text[i])
    prev = text[i - 1] if i > 0 else ""
    if o == 0x200D:                        # ZWJ — emoji glue
        nxt = text[i + 1] if i + 1 < len(text) else ""
        return _emoji_ish(prev) or _emoji_ish(nxt)
    if o in VS:                            # variation selector — after an emoji base
        return _emoji_ish(prev)
    if o in TAG:                           # tag — after a flag base earlier
        return FLAG_BASE in (ord(x) for x in text[:i])
    if o in BIDI_OPEN or o in BIDI_CLOSE:  # bidi — only if the whole string is balanced
        opens = sum(1 for x in text if ord(x) in BIDI_OPEN)
        closes = sum(1 for x in text if ord(x) in BIDI_CLOSE)
        return opens == closes
    return False                           # ZWSP/ZWNJ/BOM/WJ/SHY never vouch


def invisible_cards_reader(text):
    """The invisibles pass: ALARM smuggle / OK legit glue / WATCH unknown."""
    smug = _first_smuggle(text)
    if smug:
        return smug
    # the present-set is the WHOLE monitored class (AD-35), not only our 6:
    # any such character is at least WATCH (does not stay silent), even
    # outside a token.
    pos = [i for i, c in enumerate(text) if _monitored(c)]
    if not pos:
        return Finding("clean", 0.0, "invisible: no invisibles")
    if all(_legit_glue(text, i) for i in pos):
        return Finding("clean", 0.0,
                       "invisible: all invisibles are legit emoji/bidi glue")
    return Finding("suspect", 0.45,
                   "uncarded invisible with no legitimate context",
                   signature="invisible_watch")


# --- parser-desync (port of canonical_view.py) -----------------------

def _default_ignorable(ch):
    o = ord(ch)
    if unicodedata.category(ch) == "Cf":
        return o not in _CF_NOT_DI
    if 0xFE00 <= o <= 0xFE0F or 0xE0100 <= o <= 0xE01EF:   # variation selectors
        return True
    return o in _OTHER_DI


_CF_NOT_DI = ({0x600, 0x601, 0x602, 0x603, 0x604, 0x605, 0x6DD, 0x70F, 0x890,
               0x891, 0x8E2, 0x110BD, 0x110CD} | set(range(0xFFF9, 0xFFFC)) |
              set(range(0x13430, 0x13440)))
_OTHER_DI = ({0x034F, 0x115F, 0x1160, 0x17B4, 0x17B5, 0x180B, 0x180C, 0x180D,
              0x180F, 0x2065, 0x3164, 0xFFA0})


def canonical_view(text):
    """Canonical reading: default-ignorables removed. Returns
    (canon, offmap), where offmap[i] is the raw index of canon[i]."""
    canon, offmap = [], []
    for i, ch in enumerate(text):
        if not _default_ignorable(ch):
            canon.append(ch)
            offmap.append(i)
    return "".join(canon), offmap


def _tokenish(ch):
    return bool(ch) and (ch.isalnum() or ch in ".-_@")   # domain/identifier characters


def canonical_view_reader(text):
    """Flags parser-desync: an invisible removed FROM INSIDE a token → two
    components read the string differently (allowlist clean, fetcher not)."""
    canon, _ = canonical_view(text)
    if canon == text:
        return Finding("clean", 0.0, "canonical_view: raw == canonical")
    for i, ch in enumerate(text):
        if _default_ignorable(ch):
            prev = text[i - 1] if i > 0 else ""
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if _tokenish(prev) and _tokenish(nxt):
                return Finding("suspect", 0.9,
                    f"parser-desync: U+{ord(ch):04X} removed from inside a token "
                    f"('{prev}<di>{nxt}') — raw and canonical readings diverge",
                    conclusive=True, signature="parser_desync")
    return Finding("clean", 0.0,
                   "canonical_view: invisibles present, but outside tokens (readings agree)")


# --- fail-closed wrappers (port of fail_closed.py) -------------------

def safe_reader(name, fn, text):
    """One detector crashed → WATCH, never silently clean; the rest run on."""
    try:
        return fn(text)
    except Exception as e:  # noqa: BLE001 — intentionally broad: the guard must not stay silent
        return Finding("suspect", 0.4,
            f"detector '{name}' could not evaluate ({type(e).__name__}) — "
            f"we hold, we do not clear", conclusive=False, signature="component_error")


def safe_analyze(text, pipeline):
    """Fail-CLOSED for the whole guard: a non-string or any error → block, not OK."""
    if not isinstance(text, str):
        return Finding("suspect", 0.7,
            f"non-text input ({type(text).__name__}) — analysis impossible, block",
            conclusive=True, signature="invalid_input")
    try:
        return pipeline(text)
    except Exception as e:  # noqa: BLE001
        return Finding("suspect", 0.8,
            f"analysis crashed ({type(e).__name__}) — block (fail-closed)",
            conclusive=True, signature="analysis_error")


# --- facade: canonicalization → detectors → severity-max -------------

def _pipeline(text):
    canon, meta = canonicalize(text)
    parts = [
        safe_reader("invisible", invisible_cards_reader, canon),
        safe_reader("parser_desync", canonical_view_reader, canon),
    ]
    if meta["overlong_utf8"]:
        parts.append(Finding("suspect", 0.9,
            "overlong UTF-8 revealed by canonicalization — proven encoding evasion",
            conclusive=True, signature="overlong_utf8"))
    return combine(*parts)


def analyze(text) -> dict:
    """Full pass: canonicalization (reveal the encoding) → detectors for
    invisibles/bidi/tag/VS/desync → the harshest verdict. Advisory.
    Returns a dict with risk/label/reason/signature + canon and meta."""
    finding = safe_analyze(text, _pipeline)
    canon, meta = (canonicalize(text) if isinstance(text, str) else (text, {}))
    return {
        "risk": risk_of(finding),
        "label": finding.label,
        "reason": finding.reason,
        "conclusive": finding.conclusive,
        "signature": finding.signature,
        "strength": finding.strength,
        "canonicalized": canon,
        "canon_meta": meta,
    }
