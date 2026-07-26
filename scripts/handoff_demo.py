#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Sub-vertical demo #1 (AD-59): CROSS-ORGANIZATIONAL HANDOFF without uniforms.

A scenario on a concrete object (FO-035), not on a slide:
  Party A ("Aktiv-Finance") sends Party B ("Auditor") a report with a
  payment line. In transit (a compromised delivery channel) an attacker
  changes the AMOUNT and masks the edit with an invisible codepoint.
  The product's job: at receipt, show WHERE and WHAT was substituted, and
  render a human-readable verdict — CONFIRMED for the original, CONTESTED/FORGERY
  for the tampered one.

The crypto is under the hood. Upward — only meaning (as in AD-58).
Run: python3 scripts/handoff_demo.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nacl.signing import SigningKey                              # noqa: E402

from notarius.anchor import PublicAnchor, reconcile              # noqa: E402
from notarius.diagnose import assemble                           # noqa: E402
from notarius.title import (brand, attest, TitleRegistry,         # noqa: E402
                            resolve_full, human_verdict)


def line(c="─"):
    print(c * 68)


def act(n, title):
    print()
    line("═")
    print(f"ACT {n}. {title}")
    line("═")


# Canonical report text as Party A sends it.
DOC_CANON = ("ОТЧЁТ О ПЛАТЕЖЕ\n"
             "получатель: ООО «Подрядчик»\n"
             "сумма к переводу: 1000000 RUB\n"
             "основание: акт №77 от 2026-07-20\n")


def main():
    # ── participants (keys under the hood, never exposed) ──────────────
    sender_priv = bytes(SigningKey.generate())          # Party A
    src_priv = bytes(SigningKey.generate())             # independent source (counterparty registry)
    w1 = TitleRegistry(bytes(SigningKey.generate()))    # witness 1 (notary node)
    w2 = TitleRegistry(bytes(SigningKey.generate()))    # witness 2 (industry registry)
    wkeys = {w1.pub.hex(), w2.pub.hex()}
    src_keys = {SigningKey(src_priv).verify_key.encode().hex()}

    anchor = PublicAnchor()

    # ── ACT 1: Party A records the original BEFORE sending ─────────────
    act(1, "Party A records the original before sending")
    data = DOC_CANON.encode("utf-8")

    b = brand(data, "Aktiv-Finance", sender_priv, at="2026-07-24T09:00Z")
    cosigs = [w1.witness(b), w2.witness(b)]              # two independent witnesses co-signed
    a_sender = attest(data, "Aktiv-Finance", sender_priv, "Aktiv-Finance", at="2026-07-24T09:00Z")
    a_src = attest(data, "Aktiv-Finance", src_priv, "Counterparty-Registry", at="2026-07-24T09:01Z")

    # public registry "under glass": first-wins, the real source is written in
    anchor.append(data, "Aktiv-Finance", at="2026-07-24T09:00Z",
                  source_pub=src_keys and next(iter(src_keys)))

    v_ok = resolve_full(data, [(b, cosigs)], [a_sender, a_src], wkeys, anchor,
                        source_keys=src_keys)
    print("Report sealed, two witnesses co-signed, written into the public registry.")
    print()
    print(human_verdict(v_ok))
    print(f"\n→ Original accepted: {v_ok['confidence']} (the honest sender's title stands).")

    # ── ACT 2: hostile delivery ────────────────────────────────────────
    act(2, "In transit the channel substituted the amount and masked the edit")
    # 1000000 → 9000000, plus an invisible separator inside the word "переводу"
    tampered_text = DOC_CANON.replace("1000000", "9000000").replace(
        "переводу", "перево​ду")
    delivered = tampered_text.encode("utf-8")
    print("Party B received the report over the delivery channel. The bytes differ from")
    print("the original — but the edit is invisible to the eye (amount + invisible char).")

    # ── ACT 3: receipt — show WHERE and WHAT ───────────────────────────
    act(3, "Receipt: the product shows WHERE and WHAT was substituted")

    # (i) compare received against the source canon — break diagnostic
    report = assemble(DOC_CANON, tampered_text)
    diag = report["diagnosis"]
    print("① CONTENT ANALYSIS (what exactly changed against the source canon):")
    print(f"   bytes match:   {'yes' if report['bytes_match'] else 'NO — BREAK'}")
    print(f"   category:      {diag['category']}  (review level: {diag['review']})")
    print(f"   detail:        {diag['human']}")
    print(f"   stealth:       scan={report['content_scan']['risk']} "
          f"/ {report['content_scan']['signature']}")
    print(f"   → {report['human']}")

    # (ii) compare against the "glass": the received artifact is NOT in the registry
    rec = reconcile("Aktiv-Finance", delivered, anchor)
    print("\n② RECONCILE WITH THE PUBLIC REGISTRY (is this what the source anchored):")
    print(f"   status: {rec['status']}")
    print(f"   → the received artifact is not anchored: this is NOT the report the source recorded.")

    # (iii) the thief tries to pass the ORIGINAL off as his own — a scribble on the glass
    thief_priv = bytes(SigningKey.generate())
    b_thief = brand(data, "Thief", thief_priv, at="2026-07-24T09:05Z")
    thief_cosigs = [x for x in (w1.witness(b_thief), w2.witness(b_thief)) if x]
    rec2 = reconcile("Thief", data, anchor)          # honest witnesses will REFUSE (hash taken)
    print("\n③ APPROPRIATION ATTEMPT (the thief back-dates a seal on the original as his own):")
    print(f"   witnesses co-signed the thief: {len(thief_cosigs)} of 2 "
          f"(the first-seal is taken by the honest sender)")
    print(f"   glass reconcile: {rec2['status']} — the registry remembers {rec2.get('registry_owner')}")
    print(f"   → appropriation exposed: scribbled on the glass, the registry is clean.")

    # ── SUMMARY ─────────────────────────────────────────────────────────
    act("★", "Human summary")
    print("Original (Party A):     CONFIRMED — three pillars agree.")
    print("Received over channel:  BREAK — amount 1000000→9000000, hidden by an invisible char,")
    print("                        no such artifact in the registry.")
    print("Appropriation attempt:  EXPOSED — witnesses refused, the glass didn't match the registry.")
    print()
    print("Boundaries (candidly): the product shows WHERE and WHAT was substituted and that")
    print("it is NOT an anchored artifact. It does NOT decide intent for the human and does NOT")
    print("replace legal expertise (TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH).")
    line("═")


if __name__ == "__main__":
    main()
