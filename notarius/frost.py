# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — FROST-ED25519: a real signing threshold (AD-38).

Replaces the Shamir stand-in of custody.py in the MAIN path: there the
seed is REASSEMBLED in memory to sign (a candid demo boundary). FROST
(RFC 9591) removes this by construction — the secret is NEVER
reconstructed: each participant computes its partial signature z_i from
its own share, and the coordinator merely sums them. The key never
exists in full at any single point during signing.

KEY PROPERTY (AD-30): the FROST-ED25519 ciphersuite emits an ORDINARY
Ed25519 signature (R‖S). So our VERIFY side (envelope_v2/trace, PyNaCl
VerifyKey) does NOT change at all — proven by test_frost.py: a 2-of-3
signature is accepted by an unmodified verify_envelope_v2.

WHAT IT STANDS ON: all ed25519 arithmetic (point addition, scalars,
base-mul) comes from libsodium via PyNaCl (nacl.bindings.crypto_core_ed25519_*).
We do NOT roll our OWN curve (AD-23) — we compose the protocol on top of
vetted primitives.

CANDID LIMITS (loudly):
  - REFERENCE, NOT PRODUCTION, NOT audited. The Python-level composition
    is NOT guaranteed constant-time (the libsodium primitives are; the
    branching and byte-handling of scalars are not). Production: Zcash's
    Rust FROST via FFI (PyO3) or a separate signing service.
  - Keygen is a TRUSTED DEALER: during the DEALING STAGE the dealer
    briefly holds s (as in Shamir custody). Real FROST uses DKG — s never
    exists anywhere at any time. The improvement over custody.py is
    precisely in SIGNING: s is NOT reassembled (in custody.py it is).
  - The nonce is SINGLE-USE: reusing a nonce between signings leaks a
    share. Here the nonce is freshly random per call, but single-use
    storage is NOT enforced (demo).
  - Does not close coercion (AD-28) or self-attestation (AD-24).
"""

from __future__ import annotations

import hashlib
import os

import nacl.bindings as _b

# --- scalars and points on top of libsodium (vetted primitives) --------


def _sc_reduce(b64: bytes) -> bytes:
    return _b.crypto_core_ed25519_scalar_reduce(b64)


def _sc_int(n: int) -> bytes:
    return _sc_reduce((n % (1 << 512)).to_bytes(64, "little"))


def _sc_add(a, x): return _b.crypto_core_ed25519_scalar_add(a, x)
def _sc_sub(a, x): return _b.crypto_core_ed25519_scalar_sub(a, x)
def _sc_mul(a, x): return _b.crypto_core_ed25519_scalar_mul(a, x)
def _sc_inv(a): return _b.crypto_core_ed25519_scalar_invert(a)
def _rand_sc(): return _sc_reduce(os.urandom(64))


def _base(scalar): return _b.crypto_scalarmult_ed25519_base_noclamp(scalar)
def _pmul(scalar, P): return _b.crypto_scalarmult_ed25519_noclamp(scalar, P)
def _padd(P, Q): return _b.crypto_core_ed25519_add(P, Q)


def _H(tag: bytes, *parts: bytes) -> bytes:
    """Internal FROST hash → scalar (for the binding factor)."""
    return _sc_reduce(hashlib.sha512(tag + b"".join(parts)).digest())


def _challenge(R: bytes, A: bytes, msg: bytes) -> bytes:
    """RFC 8032 challenge: c = SHA-512(R‖A‖M) mod L. It is EXACTLY this form
    that makes the output a valid ordinary Ed25519 signature (the verify
    side is unchanged)."""
    return _sc_reduce(hashlib.sha512(R + A + msg).digest())


# --- Shamir over the scalar field + Lagrange --------------------------


def _poly_eval(coeffs, x):
    acc = coeffs[-1]
    for c in reversed(coeffs[:-1]):
        acc = _sc_add(_sc_mul(acc, x), c)
    return acc


def _lagrange0(i: int, signer_ids) -> bytes:
    """Lagrange coefficient of participant i at x=0 for a signer set."""
    xi = _sc_int(i)
    num, den = _sc_int(1), _sc_int(1)
    for j in signer_ids:
        if j == i:
            continue
        xj = _sc_int(j)
        num = _sc_mul(num, xj)
        den = _sc_mul(den, _sc_sub(xj, xi))
    return _sc_mul(num, _sc_inv(den))


# --- Keygen (trusted dealer) ------------------------------------------


def keygen_dealer(n: int, t: int):
    """Deal n shares with threshold t. Returns (shares, group_pubkey).
    shares: [(id, share_scalar)]. The dealer holds s ONLY here, at dealing
    time (a candid boundary vs DKG); during SIGNING s never appears."""
    if not 1 <= t <= n:
        raise ValueError("need 1 <= t <= n")
    s = _rand_sc()
    coeffs = [s] + [_rand_sc() for _ in range(t - 1)]
    shares = [(i, _poly_eval(coeffs, _sc_int(i))) for i in range(1, n + 1)]
    group_pub = _base(s)
    del s, coeffs                      # secret discarded (symbolic, for the demo)
    return shares, group_pub


# --- Signing (two rounds, the secret is NOT reassembled) --------------


def _commitments(signer_ids):
    """Round 1: each participant has fresh nonces (d,e) and commitments
    (D,E)=(d·B,e·B). The secret nonces stay with the participant."""
    nonces, commits = {}, []
    for i in signer_ids:
        d, e = _rand_sc(), _rand_sc()
        nonces[i] = (d, e)
        commits.append((i, _base(d), _base(e)))
    commits.sort()
    return nonces, commits


def _binding(i, msg, commits):
    enc = b"".join(_sc_int(idx) + D + E for idx, D, E in commits)
    return _H(b"FROST-ED25519-rho", _sc_int(i), msg, enc)


def sign(signers, msg: bytes, group_pub: bytes) -> bytes:
    """Threshold signature over msg by a subset signers=[(id,share)].
    The secret s is NOT reassembled: each z_i is computed from its own
    share s_i, and the coordinator sums them. Output is an ORDINARY
    Ed25519 signature (R‖S, 64 bytes).
    """
    ids = [i for i, _ in signers]
    nonces, commits = _commitments(ids)

    # group commitment R = Σ (D_i + ρ_i·E_i)
    rho, R = {}, None
    for i, D, E in commits:
        rho[i] = _binding(i, msg, commits)
        term = _padd(D, _pmul(rho[i], E))
        R = term if R is None else _padd(R, term)

    c = _challenge(R, group_pub, msg)

    # partial signatures z_i = d_i + e_i·ρ_i + λ_i·s_i·c ; z = Σ z_i
    z = None
    for i, s_i in signers:
        d, e = nonces[i]
        lam = _lagrange0(i, ids)
        z_i = _sc_add(_sc_add(d, _sc_mul(e, rho[i])),
                      _sc_mul(_sc_mul(lam, s_i), c))
        z = z_i if z is None else _sc_add(z, z_i)

    return R + z                        # 32 + 32 = a standard Ed25519 signature


if __name__ == "__main__":              # demonstration: "verify does not change"
    from nacl.signing import VerifyKey
    shares, A = keygen_dealer(n=3, t=2)
    m = b"element=amount value=1000000 recipient=CompanyA"
    sig = sign([shares[0], shares[1]], m, A)      # 2 of 3
    VerifyKey(A).verify(m, sig)                    # ordinary Ed25519 verify
    print("2-of-3 FROST → standard Ed25519 verify: OK")
    try:
        VerifyKey(A).verify(m, sign([shares[0]], m, A))   # 1 share
        print("ERROR: one share should not sign")
    except Exception:
        print("one share (< threshold) fails verify: OK")
