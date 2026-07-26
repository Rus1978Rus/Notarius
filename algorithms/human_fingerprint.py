# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Human-verifiable identification — a nonstandard layer.

The deep-time problem (E-Continuity): a signature is useless if a future
verifier cannot RUN the algorithm. HMAC/Ed25519 need software, keys,
libraries. Thousands of years from now, none of those will exist.

The answer: signatures/identifiers a HUMAN can verify without software:

1. word_fingerprint — SHA-256 → a list of short words. A person compares
   the fingerprint across DIFFERENT substrates (screen vs stone vs voice)
   without computing the hash by hand. The PGP word list / visual hash
   principle.

2. positional_check / redundant_id — a self-checking identifier with a
   POSITIONAL check digit (mod 97 weighted by position, like
   ISO 7064 / IBAN), duplicated k times.

LIMITS (after external review AD-22 — candidly, no overclaim):
- Word fingerprint: N words ≈ 6·N bits. For small N (6 words = 36 bits) a
  targeted search is CHEAP (seconds on a laptop); when the attacker
  controls both messages, the threshold is the birthday bound at 3·N bits.
  This protects against ACCIDENTAL divergence, NOT against an attacker.
  Review recommendation: at least 12–16 words, BIP39 wordlist (11 bits).
  The fingerprint must live on an INDEPENDENT substrate, otherwise
  replacing the content together with its fingerprint passes the check.
- mod-97 check: NOT authentication. An attacker knows the algorithm and
  will recompute the check for a forgery — "catches tampering" was an
  overclaim, removed (all 5 review sources, unanimous reject-first). It
  catches ACCIDENTAL corruption, including transpositions (positional
  weight — the old non-positional sum let them through: AB==BA).
- Duplicates: survive only INDEPENDENT damage; a correlated failure (one
  substrate/file/fire) kills every copy at once.
"""

from __future__ import annotations

import hashlib

# 64 short, distinguishable words (6 bits/word). Easy to read and say aloud.
WORDLIST = [
    "arc", "bay", "bell", "bird", "blue", "bone", "book", "cell",
    "clay", "cloud", "coin", "cord", "cube", "dawn", "deep", "disk",
    "dust", "echo", "fern", "fire", "fish", "flag", "fork", "gate",
    "gem", "gold", "hill", "iron", "jade", "key", "lake", "leaf",
    "lens", "lime", "lock", "moon", "moss", "nest", "node", "oak",
    "path", "pearl", "pine", "rain", "reed", "ring", "rock", "root",
    "salt", "sand", "seal", "seed", "ship", "snow", "star", "stone",
    "tide", "tree", "vine", "wave", "well", "wind", "wolf", "wood",
]
assert len(WORDLIST) == 64


def word_fingerprint(data: bytes, words: int = 12) -> list[str]:
    """SHA-256(data) → `words` words from WORDLIST (6 bits/word).
    A fingerprint for human comparison across a substrate boundary.
    Following the review (AD-22), the minimum was raised from 6 to 12 words
    (72 bits): 6 words = 36 bits could be brute-forced in seconds. For
    strength, use the full hash."""
    h = hashlib.sha256(data).digest()
    bits = "".join(f"{b:08b}" for b in h)
    out = []
    for i in range(words):
        chunk = bits[i * 6:(i + 1) * 6]
        out.append(WORDLIST[int(chunk, 2)])
    return out


def fingerprints_match(a: list[str], b: list[str]) -> bool:
    """Compare two fingerprints (for example, from stone and from screen)."""
    return len(a) == len(b) and all(x == y for x, y in zip(a, b))


# --- Self-checking identifier (human-computable) ----------------------

def positional_check(identifier: str) -> int:
    """Positional check digit 00–96: sum((i+1)·code) mod 97.
    Position weighting catches transpositions (AB≠BA) — the old
    non-positional sum let them through (AD-22). NOT authentication: an
    attacker will recompute it. Computable by hand: code·position, sum,
    remainder mod 97."""
    return sum((i + 1) * ord(c) for i, c in enumerate(identifier)) % 97


# Name kept for backward compatibility; behavior is now positional.
mod97_check = positional_check


def make_redundant_id(identifier: str, copies: int = 3) -> str:
    """ID + positional check, duplicated `copies` times.
    Survives INDEPENDENT partial loss (not a correlated one)."""
    tagged = f"{identifier}#{positional_check(identifier):02d}"
    return "|".join([tagged] * copies)


def recover_id(damaged: str) -> str | None:
    """Recover the ID from a damaged string: return the first copy whose
    check digit matches. None if none survived.
    LIMIT (AD-22): the check catches ACCIDENTAL corruption, not forgery —
    an attacker will recompute the check for a substituted id."""
    for copy in damaged.split("|"):
        if "#" not in copy:
            continue
        ident, _, chk = copy.rpartition("#")
        if chk.isdigit() and positional_check(ident) == int(chk):
            return ident
    return None
