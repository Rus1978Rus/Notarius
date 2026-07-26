#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""The engine in pure form (AD-83): the semantic trace localizes WHOSE LINK
broke — not "a string changed", but "at whose step in the custody chain".

The document carries OUR signed trace from birth and passes through hands:
  0. Aktiv-Finance CREATED the invoice (CREATED).
  1. Aktiv-Finance TRANSFERRED to Auditor (TRANSFERRED — value must be preserved).
  2. Auditor REVIEWED (REVIEWED — value must be preserved).
  3. Fraudster appended a link with a SUBSTITUTED amount, signing with his own key.

The engine (verify_trace) shows: break_at_step (whose link), last_signer,
and "who last held it INTACT". Channel-independent — no mail/DKIM/headers.

Run: python3 scripts/trace_localize_demo.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nacl.signing import SigningKey                                  # noqa: E402

from notarius import trace as T                                     # noqa: E402

DOC = "INVOICE No.5 / recipient: Contractor LLC / amount: 1000000 USD"
DOC_FORGED = "INVOICE No.5 / recipient: Contractor LLC / amount: 9000000 USD"


def priv():
    return bytes(SigningKey.generate())


def pub(p):
    return SigningKey(p).verify_key.encode()


def line(c="─"):
    print(c * 68)


def main():
    a_priv, b_priv, e_priv = priv(), priv(), priv()     # Aktiv-Finance, Auditor, Fraudster
    trusted = {"Aktiv-Finance": pub(a_priv), "Auditor": pub(b_priv)}   # Fraudster NOT among the trusted

    # ── honest custody chain ───────────────────────────────────────────
    tr = T.new_trace("schet-5", DOC, "orig", "Aktiv-Finance", a_priv, "09:00")
    tr = T.append_event(tr, DOC, "TRANSFERRED", "Aktiv-Finance", a_priv, "09:05")
    tr = T.append_event(tr, DOC, "REVIEWED", "Auditor", b_priv, "10:00")

    line("═")
    print("HONEST CHAIN (created → transferred → reviewed)")
    line("═")
    rep = T.verify_trace(tr, trusted_keys=trusted, current_value=DOC)
    print(f"status: {rep['status']} | last signer: {rep['last_signer']}")
    print(f"→ trace intact, value in place.\n")

    # ── the thief appends a link with a substitution ───────────────────
    tr_forged = T.append_event(tr, DOC_FORGED, "TRANSFERRED", "Fraudster", e_priv, "10:07")

    line("═")
    print("FORGERY: Fraudster appended a link, substituting the amount 1000000 → 9000000")
    line("═")
    rep2 = T.verify_trace(tr_forged, trusted_keys=trusted, current_value=DOC_FORGED)
    bp = rep2["break_at_step"]
    print(f"status: {rep2['status']}")
    print(f"WHOSE LINK BROKE: step {bp} — actor '{tr_forged[bp]['actor']}'")
    if bp is not None and bp > 0:
        print(f"WHO LAST HELD IT INTACT: '{tr_forged[bp-1]['actor']}' (step {bp-1})")
    print("WHY:")
    for r in rep2["reasons"]:
        print(f"   - {r}")
    print(f"\ntime proven: {rep2['time_proven']} (self-declaration without an external anchor)")

    line("═")
    print("POINT: the engine named NOT 'a string changed', but WHOSE LINK in the custody")
    print("chain broke and who last held the document intact —")
    print("channel-independent, without a single mail header line.")
    line("═")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
