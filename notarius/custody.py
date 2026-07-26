# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — key custody envelope (architecture demo, AD-26).

Assembles a working core of four axes from the 7-source summary:
  THRESHOLD (M-of-N)  +  MORTAL HEARTBEAT  +  EXPIRY OF OLD SHARES.

Demonstrates the PROPERTIES, not production crypto:
  1. M-of-N: no single share (and not even M-1) reconstructs the key.
  2. Mortal heartbeat (Kimi B2): with no heartbeat past the window the
     key is DEAD, signing is impossible even with M shares; "a copy
     inherits mortality".
  3. Expiry (proactive refresh, GPT/Kimi): shares from a past epoch are
     invalid — a set stolen last week is useless.

CANDID LIMITS (we don't pass the demo off as production):
  - Here Shamir REASSEMBLES the seed in memory when signing. Production
    uses a threshold signature (FROST/threshold-Ed25519): the key is
    NEVER assembled at any single point (GPT: "don't assemble it in the
    memory of one device"). The in-memory reassembly is flagged and is a
    boundary of the demo.
    → LIFTED by the reference implementation notarius/frost.py (AD-38):
    FROST-ED25519 signs WITHOUT reconstructing the secret and emits an
    ordinary Ed25519 signature (the verify side is unchanged). custody.py
    is left as is (a demo of threshold + heartbeat + expiry); frost.py is
    the threshold itself, with no in-memory assembly.
  - Refresh here is dealer-based (for clarity). Production uses proactive
    secret sharing WITHOUT a dealer (shares are refreshed without
    revealing the secret).
  - Secure enclave and an external timestamp are integration points (see
    the plan); they are not emulated here.

Stdlib + PyNaCl only.
"""

from __future__ import annotations

import secrets

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

# 13th Mersenne prime, > 2^256 — the Shamir field for a 32-byte seed.
_PRIME = 2 ** 521 - 1


def _eval_poly(coeffs: list[int], x: int) -> int:
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % _PRIME
    return acc


def _split(secret: int, m: int, n: int) -> list[tuple[int, int]]:
    """Shamir: secret = constant term; threshold m; n shares (x=1..n)."""
    if not 1 <= m <= n:
        raise ValueError("need 1 <= M <= N")
    coeffs = [secret] + [secrets.randbelow(_PRIME) for _ in range(m - 1)]
    return [(x, _eval_poly(coeffs, x)) for x in range(1, n + 1)]


def _reconstruct(points: list[tuple[int, int]]) -> int:
    """Lagrange at x=0 mod P. Reassembles the secret — a demo boundary."""
    secret = 0
    for i, (xi, yi) in enumerate(points):
        num = den = 1
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = (num * (-xj)) % _PRIME
            den = (den * (xi - xj)) % _PRIME
        secret = (secret + yi * num * pow(den, -1, _PRIME)) % _PRIME
    return secret % _PRIME


class KeyCustody:
    """Custody envelope: threshold share issuance + heartbeat + epochs."""

    def __init__(self, m: int, n: int, max_missed_beats: int = 2):
        self.m, self.n = m, n
        self.max_missed = max_missed_beats
        self._seed = secrets.token_bytes(32)          # demo: the dealer knows the seed
        self.public_key = bytes(SigningKey(self._seed).verify_key)
        self.epoch = 0
        self.last_beat = 0
        self._alive = True

    def issue_shares(self) -> list[dict]:
        """Shares for the current epoch. Each is stamped with its epoch (expires)."""
        if not self._alive:
            return []
        pts = _split(int.from_bytes(self._seed, "big"), self.m, self.n)
        return [{"x": x, "y": y, "epoch": self.epoch} for x, y in pts]

    def heartbeat(self) -> None:
        """Heartbeat from the living owner: new epoch + refresh (old shares
        expire). Production uses proactive refresh without revealing the seed."""
        if not self._alive:
            return
        self.epoch += 1
        self.last_beat = self.epoch

    def tick(self) -> None:
        """Passage of time with no heartbeat. Silence past the window kills the key."""
        self.epoch += 1
        if self.epoch - self.last_beat > self.max_missed:
            self._die()

    def _die(self) -> None:
        self._alive = False
        self._seed = b"\x00" * 32   # wiped (a mortal copy)

    @property
    def alive(self) -> bool:
        return self._alive

    def sign(self, message: bytes, shares: list[dict]) -> dict:
        """Threshold signature. Requires M live shares of the CURRENT epoch."""
        if not self._alive:
            return {"ok": False, "reason": "KEY_DEAD (no heartbeat — the copy is dead)"}
        fresh = [s for s in shares if s.get("epoch") == self.epoch]
        if len(fresh) < self.m:
            stale = len(shares) - len(fresh)
            reason = f"not enough live shares: {len(fresh)}/{self.m}"
            if stale:
                reason += f"; {stale} share(s) expired (not the current epoch)"
            return {"ok": False, "reason": reason}
        seed_int = _reconstruct([(s["x"], s["y"]) for s in fresh[:self.m]])
        seed = seed_int.to_bytes(32, "big")            # BOUNDARY: in-memory assembly
        sig_bytes = SigningKey(seed).sign(message).signature
        seed = b"\x00" * 32                            # immediate wipe
        # SELF-CHECK (N-W2, audit 2026-07-26): a corrupted share yields a
        # wrong seed → an invalid signature. The envelope knows public_key —
        # reject the defect BEFORE handing it out, instead of returning
        # {"ok": True} with a broken signature.
        try:
            VerifyKey(self.public_key).verify(message, sig_bytes)
        except BadSignatureError:
            return {"ok": False,
                    "reason": "SHARE_CORRUPT (share damaged — signature did not check out)"}
        return {"ok": True, "sig": sig_bytes.hex(), "epoch": self.epoch,
                "quorum": self.m}
