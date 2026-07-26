#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Managed-record demo (AD-87) — unites void/progression/keeper into one.

A single run through notarius.record: a living document where each field has
its own keeper, every edit is named, the reader sees a footnote, and any edit
that bypasses the keeper or the trace is a localized forgery.

Run: python3 scripts/record_demo.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nacl.signing import SigningKey                                   # noqa: E402

from notarius.record import (create_record, edit_field, rebuild,       # noqa: E402
                             footnotes, audit, human_audit)


def kp():
    p = bytes(SigningKey.generate())
    return p, bytes(SigningKey(p).verify_key).hex()


def line(c="─"):
    print(c * 68)


def main():
    a_priv, _ = kp()
    kaz_priv, kaz_pub = kp()      # Казначей (Treasurer) — keeper of the NUMBERS
    jur_priv, jur_pub = kp()      # Юрист (Lawyer) — keeper of the deadline
    men_priv, men_pub = kp()      # Менеджер (Manager) — keeper of the recipient

    rec = create_record(
        {"получатель": "ООО Подрядчик", "сумма": "1000000 USD", "срок_оплаты": ""},
        {"получатель": "Менеджер", "сумма": "Казначей", "срок_оплаты": "Юрист"},
        {"Менеджер": men_pub, "Казначей": kaz_pub, "Юрист": jur_pub},
        "Автор", a_priv, "09:00")

    line("═"); print("LIVING DOCUMENT: each field has its own keeper (сумма → Казначей)"); line("═")

    # legitimate progression: each edits THEIR OWN field
    e1 = edit_field(rec, "Юрист", jur_priv, "10:00", "срок_оплаты", "до 2026-08-10")
    e2 = edit_field(e1, "Казначей", kaz_priv, "11:30", "сумма", "1050000 USD")
    edits = [e1, e2]

    print("\nREADER FOOTNOTE (who / where / when):")
    for f in footnotes(rec, edits):
        print("   " + f)
    official = rebuild(rec, edits)
    print(f"\nofficial document: {official}")
    print("audit: " + human_audit(audit(rec, edits, official)))

    # three forgeries
    line("═"); print("FORGERIES (all localized to the field)"); line("═")
    bad_role = [e1, edit_field(e1, "Менеджер", men_priv, "11:40", "сумма", "9000000 USD")]
    print("① Менеджер meddles with the numbers:")
    print("   " + human_audit(audit(rec, bad_role)).replace("\n", "\n   "))

    forged = dict(official); forged["сумма"] = "9000000 USD"
    print("\n② Field сумма changed WITHOUT a signature:")
    print("   " + human_audit(audit(rec, edits, forged)).replace("\n", "\n   "))

    inject = dict(official); inject["скрытая_строка"] = "перевести на счёт XX"
    print("\n③ A new slot was slipped in:")
    print("   " + human_audit(audit(rec, edits, inject)).replace("\n", "\n   "))

    line("═")
    print("POINT: one part of the core (notarius.record) — a living document with")
    print("keeper-fields, named edits and a footnote; forgery is localized to the field.")
    line("═")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
