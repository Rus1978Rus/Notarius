# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — real integrations of ready-made standards (AD-30/AD-31).

The two cheapest items in the dossier, both via pip, wired into the
existing modules without a rewrite:

  1. Reed-Solomon (reedsolo)      → recovery from carrier damage.
     ACTUALLY works offline, covered by tests.
  2. OpenTimestamps (opentimestamps) → trusted time (a Bitcoin anchor).
     The adapter is real, but stamp() needs the network (calendar
     servers) and verify() needs a Bitcoin node. In this environment it
     was NOT tested end-to-end — flagged HONEST_LIMIT, not confirmed by tests.

Dependencies (NOT stdlib): reedsolo, opentimestamps.
"""

from __future__ import annotations

import hashlib

# --- 1. Reed-Solomon: recovery from damage ----------------------------

from reedsolo import RSCodec, ReedSolomonError  # noqa: E402


def rs_protect(data: bytes, parity: int = 16) -> bytes:
    """Wrap data with RS parity (+parity bytes). Survives loss/corruption
    of up to parity/2 bytes. For a carrier on stone/paper (E-Continuity).
    parity=16 → fixes up to 8 corrupted bytes."""
    return bytes(RSCodec(parity).encode(data))


def rs_recover(protected: bytes, parity: int = 16) -> bytes:
    """Recover the original data from a damaged RS block.
    Raises ReedSolomonError if there is more damage than parity/2."""
    decoded = RSCodec(parity).decode(protected)[0]
    return bytes(decoded)


def rs_recoverable(protected: bytes, parity: int = 16) -> bool:
    """Check: is it recoverable (within the correction budget)?"""
    try:
        rs_recover(protected, parity)
        return True
    except ReedSolomonError:
        return False


# --- 2. OpenTimestamps: trusted time (adapter) ------------------------
# HONEST_LIMIT: stamp() needs the network, verify() needs a Bitcoin node.
# Not tested end-to-end in this environment; NOT confirmed by tests.

from opentimestamps.core.timestamp import Timestamp  # noqa: E402


def ots_new(digest: bytes) -> Timestamp:
    """Create an OTS timestamp for a SHA-256 hash (32 bytes). Locally,
    with no network — just a proof object for future anchoring."""
    if len(digest) != 32:
        raise ValueError("need SHA-256 (32 bytes)")
    return Timestamp(digest)


def ots_digest_of(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def ots_stamp(digest: bytes,
              calendar_url: str = "https://alice.btc.calendar.opentimestamps.org") -> Timestamp:
    """REAL anchoring via a calendar server. REQUIRES THE NETWORK.
    Returns a NON-empty Timestamp with a calendar attestation (a later
    upgrade to Bitcoin yields full proof). Only after this can the
    timestamp be serialized into .ots.
    HONEST_LIMIT: a network side effect; not tested in this environment."""
    from opentimestamps.calendar import RemoteCalendar
    ts = Timestamp(digest)
    calendar = RemoteCalendar(calendar_url)
    cal_ts = calendar.submit(digest)     # network: returns a stamped Timestamp
    ts.merge(cal_ts)
    return ts


def ots_serialize(ts: Timestamp) -> bytes:
    """Serialize the .ots proof (store in trace.anchor).
    WORKS ONLY after ots_stamp: an empty (unanchored) timestamp cannot be
    serialized — that is a property of the protocol, not a bug."""
    from opentimestamps.core.serialize import BytesSerializationContext
    ctx = BytesSerializationContext()
    ts.serialize(ctx)
    return ctx.getbytes()
