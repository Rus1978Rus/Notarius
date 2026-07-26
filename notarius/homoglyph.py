# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — lookalike-character (homoglyph) detector on UTS#39 data, AD-79/80.

History: AD-79 closed Kimi's defect with a hand map of ~50 characters. AD-80 —
a line-by-line audit of the sibling rus1978rus/msl_mip showed: there is no
working homoglyph-detector code there (skeleton is a paper solution), BUT there
is valuable DATA — the UTS#39 confusables.txt (Unicode 17.0.0). We took the data
(not the code): notarius/data/confusables_ascii.txt — 1861 lookalikes with an
ASCII prototype (Cyrillic/Greek/fullwidth/mathematical/ligatures). msl_mip itself
was NOT modified.

A lookalike is a character from another script that LOOKS like ASCII ("аdmin" =
Cyr. а + Lat. dmin; "paypаl.com" = an IDN homograph). Functions:
  skeleton(s)       — UTS#39 skeleton: NFD → replace lookalikes → NFD (two
                      visually identical texts yield ONE skeleton);
  deconfuse(s)      — replace lookalikes with their ASCII appearance (no NFD,
                      for comparison);
  confusables_in(s) — which lookalikes are present;
  mixed_script_word(s) — words where ASCII Latin is mixed with a LETTER lookalike
                      (a signal of smuggling without a reference).

BOUNDARY (candidly): coverage is the ASCII-target subset of UTS#39 17.0.0
(masquerading as Latin), NOT the whole confusables.txt. Legitimate
single-script text (purely Cyrillic/Greek) is NOT flagged — the alarm fires
only on a MIX of scripts.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

_DATA = Path(__file__).with_name("data") / "confusables_ascii.txt"


def _load() -> dict[str, str]:
    m: dict[str, str] = {}
    try:
        for line in _DATA.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ";" not in line:
                continue
            src_hex, tgt_hexes = line.split(";", 1)
            try:
                src = chr(int(src_hex, 16))
                tgt = "".join(chr(int(h, 16)) for h in tgt_hexes.split())
            except ValueError:
                continue
            m[src] = tgt
    except OSError:
        # candid fallback: a minimal set of common attacking lookalikes
        for cp, a in {0x0430: "a", 0x0435: "e", 0x043E: "o", 0x0440: "p",
                      0x0441: "c", 0x0445: "x", 0x0456: "i", 0x03BF: "o"}.items():
            m[chr(cp)] = a
    return m


CONFUSABLES = _load()
# Only lookalikes whose ASCII appearance is a LETTER: for the script-mix alarm
# (space/punctuation lookalikes are excluded, to avoid false positives).
_LETTER_CONFUSABLES = {s: t for s, t in CONFUSABLES.items()
                       if t.isascii() and t.isalpha()}


def deconfuse(s: str) -> str:
    """Reduce known lookalikes to their ASCII appearance (no NFD)."""
    return "".join(CONFUSABLES.get(ch, ch) for ch in s)


def skeleton(s: str) -> str:
    """UTS#39 skeleton: NFD → replace lookalikes → NFD. Two visually identical
    texts yield one skeleton (the basis for a "looks the same" comparison)."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(CONFUSABLES.get(ch, ch) for ch in s)
    return unicodedata.normalize("NFD", s)


def confusables_in(s: str) -> list[str]:
    """List of lookalike characters present (in order of occurrence)."""
    return [ch for ch in s if ch in CONFUSABLES]


def _is_ascii_latin(ch: str) -> bool:
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


def _wordish(ch: str) -> bool:
    return ch.isalnum() or ch in CONFUSABLES


def mixed_script_words(s: str) -> list[str]:
    """Words where ASCII Latin is MIXED with a letter lookalike — a signal of
    smuggling without a reference (a purely Cyrillic/Greek word is NOT counted
    as mixed)."""
    out, cur = [], []
    for ch in s + " ":
        if _wordish(ch):
            cur.append(ch)
        else:
            w = "".join(cur)
            if (any(_is_ascii_latin(c) for c in w)
                    and any(c in _LETTER_CONFUSABLES for c in w)):
                out.append(w)
            cur = []
    return out
