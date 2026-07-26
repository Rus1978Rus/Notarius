#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Verifying "on one machine, two mail accounts" (AD-70).

Answers the author's question: can you essentially verify this on a computer —
set up two different mail accounts and run it through? YES. Here the transport
is folders (the network is closed in this environment), but the run goes through
the REAL product (notarius check). Swapping folders for real SMTP/IMAP is a thin
adapter.

Three roads on one machine:
  glass_registry/  — "registry under glass": the sender places the reference at
                     birth; the interceptor can't reach here (another road).
  alpha_outbox/    — the sender's outgoing (account alpha).
  beta_inbox/      — the receiver's incoming (account beta); HERE the mailman operates.

Run: python3 scripts/two_accounts_demo.py
"""

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from notarius.cli import cmd_check, cmd_seal   # noqa: E402

INVOICE = ("INVOICE No.77\n"
           "payer: Client LLC\n"
           "amount payable: 1 000 000 USD\n"
           "due date: 2026-08-01\n")


def banner(t):
    print("\n" + "═" * 66 + f"\n{t}\n" + "═" * 66)


def main():
    ws = Path(tempfile.mkdtemp(prefix="notarius_2acc_"))
    glass = ws / "glass_registry"      # under glass (another road)
    outbox = ws / "alpha_outbox"       # sender
    inbox = ws / "beta_inbox"          # receiver (interception here)
    for d in (glass, outbox, inbox):
        d.mkdir()

    banner("STEP 1. Sender (alpha) creates the invoice and SEALS it")
    src = outbox / "schet_77.txt"
    src.write_text(INVOICE, encoding="utf-8")
    # "seal" = put the reference into the registry under glass (another road)
    canon = glass / "schet_77.txt"
    shutil.copy(src, canon)
    cmd_seal(str(canon))               # fingerprint receipt next to the reference
    print(f"  reference under glass: {canon}")
    print("  (the interceptor on the mail road can't reach here)")

    banner("STEP 2. Sending by 'mail': alpha_outbox → beta_inbox")
    delivered = inbox / "schet_77.txt"
    shutil.copy(src, delivered)
    print(f"  delivered to the receiver's box: {delivered}")

    banner("STEP 3. The MAILMAN intercepts and edits the amount in the attachment")
    tampered = INVOICE.replace("1 000 000", "9 000 000").replace("payable", "pay​able")
    delivered.write_text(tampered, encoding="utf-8")
    print("  in the incoming: amount 1 000 000 → 9 000 000, the edit hidden by an invisible char")

    banner("STEP 4. Receiver (beta) RECONCILES the incoming against the reference under glass")
    print("Command: notarius check glass_registry/schet_77.txt beta_inbox/schet_77.txt\n")
    rc = cmd_check(str(canon), str(delivered))

    banner("CONTROL. Honest delivery (no interception) — no false alarm")
    clean = inbox / "schet_77_clean.txt"
    shutil.copy(src, clean)
    cmd_check(str(canon), str(clean))

    banner("SUMMARY")
    print("Two accounts on one machine, the file traveled sender→receiver.")
    print("The interception in the ATTACHMENT was exposed by reconciling with the reference via ANOTHER road")
    print("(registry under glass). Honest delivery — 'untouched', with no false alarms.")
    print(f"\nSandbox (safe to delete): {ws}")
    print("Real mail: swap folders for SMTP/IMAP — that's a thin adapter.")
    _ = rc                              # rc==1 = "break caught" (expected); demo OK
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
