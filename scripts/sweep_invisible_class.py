#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A measured sweep across the monitored class of invisible chars (AD-35).

A reproducible measurement (E-Continuity: "measured, not claimed"):
runs the WHOLE Cf class + VS + default-ignorable through scan_hardened in
two positions (in the host `pay◌pal.com` and between spaces `a ◌ b`) and
prints the verdict distribution. The invariant is pinned by the test
tests/test_detect.py::TestMonitoredClassNoSilentPass: silent OKs — zero.

Run:  python3 scripts/sweep_invisible_class.py
"""

import sys
import unicodedata as u
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from notarius.scanner import scan_hardened   # noqa: E402


def monitored_codepoints():
    cps = []
    for cp in list(range(0x0, 0x10000)) + list(range(0xE0000, 0xE0200)) + \
            list(range(0x1D170, 0x1D18A)):
        ch = chr(cp)
        if (u.category(ch) == "Cf" or 0xFE00 <= cp <= 0xFE0F
                or 0xE0100 <= cp <= 0xE01EF):
            cps.append(cp)
    return cps


def sweep(cps, template):
    dist = {"OK": 0, "WATCH": 0, "ALARM": 0}
    silent = []
    for cp in cps:
        risk = scan_hardened(template.format(chr(cp)))["risk"]
        dist[risk] += 1
        if risk == "OK":
            silent.append(cp)
    return dist, silent


def main():
    cps = monitored_codepoints()
    print(f"Monitored characters (Cf ∪ VS ∪ DI): {len(cps)}\n")
    for label, tmpl in (("in HOST  pay◌pal.com", "pay{}pal.com"),
                        ("between SPACES  a ◌ b", "a {} b")):
        dist, silent = sweep(cps, tmpl)
        print(f"[{label}]  silent OK={dist['OK']}  "
              f"WATCH={dist['WATCH']}  ALARM={dist['ALARM']}")
        if silent:
            print("   silent pass:", ", ".join(f"U+{c:04X}" for c in silent[:16]))
    print("\nInvariant (AD-35): silent OK == 0 in both positions.")


if __name__ == "__main__":
    main()
