# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Signing a SEGMENT or the WHOLE via a Merkle tree (RFC 6962 structure).

A direct answer to the task "sign/identify segments of information OR the
information as a WHOLE":
  - ONE root is signed (the identity of the whole) — cheap;
  - membership of ANY segment is proven via an inclusion proof of size
    O(log n), WITHOUT revealing the other segments and WITHOUT having them.

FIXED 2026-07-22 following a blind adversarial review (AD-21): the previous
version duplicated an odd node (Bitcoin-style) and gave
root([A,B,C]) == root([A,B,C,C]) — the CVE-2012-2459 vulnerability.
Rewritten to RFC 6962 (Certificate Transparency): the tree is built by
splitting at the largest power of two < n, with no duplication — the tree
shape is unambiguous for each n, and the collision is gone (regression
test test_cve_2012_2459_no_collision).

Second-preimage protection (leaf ≠ node) via the domain prefixes 0x00/0x01.

LIMIT (no overclaim, confirmed by review):
  - an inclusion proof does NOT prove the COMPLETENESS of the set (that the
    shown segments are all n). So the pair (root, size) must be
    signed/checked; signed_root() returns size.
  - the root and the signer's public key must arrive over a trusted channel
    independent of the data — otherwise compromising the source bypasses
    the check.
  - this is identification and integrity, not proof of the truth of a value
    (SIGNED ≠ TRUE, AD-10).

stdlib-only (hashlib).
"""

from __future__ import annotations

import hashlib

LEAF = b"\x00"   # leaf prefix
NODE = b"\x01"   # internal-node prefix


def _leaf_hash(index: int, segment: bytes) -> bytes:
    # The leaf commits to POSITION and LENGTH (AD-22, Kimi+GPT): otherwise the
    # proof does not bind WHICH instance of an identical segment was confirmed.
    return hashlib.sha256(LEAF + index.to_bytes(8, "big")
                          + len(segment).to_bytes(8, "big") + segment).digest()


def _node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(NODE + left + right).digest()


def _largest_pow2_below(n: int) -> int:
    """The largest power of two strictly less than n (n >= 2)."""
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def _mth(segments: list[bytes], base: int) -> bytes:
    """Merkle Tree Hash per RFC 6962. base is the absolute index of the
    subtree's first segment (to bind the position in the leaf)."""
    if len(segments) == 1:
        return _leaf_hash(base, segments[0])
    k = _largest_pow2_below(len(segments))
    return _node_hash(_mth(segments[:k], base), _mth(segments[k:], base + k))


def root(segments: list[bytes]) -> bytes:
    """Identifier of the WHOLE (Merkle root, RFC 6962, with position binding)."""
    if not segments:
        raise ValueError("at least one segment is required")
    return _mth(segments, 0)


def signed_root(segments: list[bytes]) -> tuple[bytes, int]:
    """The pair (root, segment count) — sign THIS, not the root alone: size
    closes the set-completeness attack (see the limit)."""
    return root(segments), len(segments)


def inclusion_proof(segments: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """RFC 6962 audit path for segment index.
    A list of (sibling_hash, sibling_is_left) from the bottom up."""
    if not 0 <= index < len(segments):
        raise IndexError("segment index out of range")

    def build(segs: list[bytes], idx: int, base: int) -> list[tuple[bytes, bool]]:
        if len(segs) == 1:
            return []
        k = _largest_pow2_below(len(segs))
        if idx < k:  # we are in the left subtree; the sibling is the right's hash
            return build(segs[:k], idx, base) + [(_mth(segs[k:], base + k), False)]
        else:        # we are in the right; the sibling is the left's hash
            return build(segs[k:], idx - k, base + k) + [(_mth(segs[:k], base), True)]

    return build(segments, index, 0)


def verify_segment(segment: bytes, index: int, proof: list[tuple[bytes, bool]],
                   expected_root: bytes) -> bool:
    """Confirmation: the segment at position index belongs to the whole with
    the given root. The other segments are NOT needed — only the segment, its
    index, and the proof. The index is mandatory: the leaf commits to the
    position (AD-22)."""
    h = _leaf_hash(index, segment)
    for sib, sib_is_left in proof:
        h = _node_hash(sib, h) if sib_is_left else _node_hash(h, sib)
    return h == expected_root
