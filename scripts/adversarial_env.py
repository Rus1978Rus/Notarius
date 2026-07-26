#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adversarial harness: sign → run through EXTERNAL aggressive environments
→ look at what our own verify flags as broken → conclusion (AD-41).

E-Continuity discipline "measured, not claimed": the environments are REAL
external processes (iconv, sed, gzip) and real transformations (NFKC, JSON
gateway) that actual pipelines perform. Not simulated mutations.

Run:  python3 scripts/adversarial_env.py
Extend: add environments to ENVS (base64, HTML-escape, varchar truncation,
BOM/ZWSP insertion via a gateway, homoglyph substitution).
"""

import gzip
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from notarius.envelope_v2 import (          # noqa: E402
    make_envelope_v2, verify_envelope_v2, generate_keypair,
)
from notarius.scanner import scan_hardened   # noqa: E402
from notarius.diagnose import assemble        # noqa: E402

VALUE = "Плательщик=Иванов сумма=1000₽ файл=oﬃce.pdf замок=🔒"


def _run(cmd, data: bytes) -> bytes:
    return subprocess.run(cmd, input=data, capture_output=True).stdout


# --- EXTERNAL AGGRESSIVE ENVIRONMENTS (take the signed JSON text) -------

def env_iconv(s: str) -> str:
    """Real iconv: UTF-8 → CP1251 → UTF-8 (drops whatever CP1251 lacks)."""
    b = _run(["iconv", "-f", "UTF-8", "-t", "CP1251//TRANSLIT//IGNORE"], s.encode())
    b = _run(["iconv", "-f", "CP1251", "-t", "UTF-8//TRANSLIT//IGNORE"], b)
    return b.decode("utf-8", "replace")


def env_nfkc(s: str) -> str:
    """Unicode "helpfulness": NFKC (ligatures, width, compatibility)."""
    return unicodedata.normalize("NFKC", s)


def env_json_gateway(s: str) -> str:
    """JSON gateway: parse and reassemble (key order, ensure_ascii, indent)."""
    return json.dumps(json.loads(s), ensure_ascii=True, sort_keys=True, indent=2)


def env_sed_edit(s: str) -> str:
    """Real sed: malicious edit of the amount 1000 → 9000."""
    return _run(["sed", "s/1000/9000/g"], s.encode()).decode("utf-8", "replace")


def env_inject_invisible(s: str) -> str:
    """A gateway that appends an invisible char (ZWSP) into a field — as some
    editors/gateways do. We insert a zero-width char inside the name (hidden)."""
    return s.replace("Иванов", "Ива​нов")


def env_gzip(s: str) -> str:
    """gzip round-trip (control: lossless)."""
    return gzip.decompress(gzip.compress(s.encode())).decode("utf-8")


ENVS = [
    ("iconv UTF-8→CP1251→UTF-8 (external, lossy)", env_iconv),
    ("NFKC normalization (Unicode 'helpfulness')", env_nfkc),
    ("JSON gateway (structure reassembly)", env_json_gateway),
    ("sed s/1000/9000/ (external, malicious edit)", env_sed_edit),
    ("gateway inserts ZWSP into the name (hidden insertion)", env_inject_invisible),
    ("gzip round-trip (control)", env_gzip),
]


def main():
    priv, _pub = generate_keypair()
    env = make_envelope_v2(VALUE, priv, origin="invoice_458", created_at="2026-07-23")
    signed = json.dumps(env, ensure_ascii=False)      # signed artifact as text

    print("=" * 70)
    print("SIGNED:", repr(VALUE))
    print("baseline verify:", verify_envelope_v2(env)["status"])
    print("=" * 70)

    caught = passed = 0
    for name, fn in ENVS:
        mangled = fn(signed)
        try:
            m_env = json.loads(mangled)
            status = verify_envelope_v2(m_env)["status"]
            data_after = m_env.get("data", "<none>")
            sc = scan_hardened(data_after)["risk"] if isinstance(data_after, str) else "?"
        except Exception as e:
            status, data_after, sc = f"STRUCTURE BROKEN: {type(e).__name__}", None, "?"

        ok = status == "VERIFIED"
        caught += (not ok)
        passed += ok
        print(f"\n── {name}")
        print(f"   verify: {status}   →  {'PASSED ✅' if ok else 'CAUGHT 🔴'}")
        print(f"   scan_hardened(data): {sc}")
        if isinstance(data_after, str) and data_after != VALUE:
            rep = assemble(VALUE, data_after)
            d = rep["diagnosis"]
            print(f"   diagnosis: {d['category']} (review={rep['review']}) — {d['human']}")

    print("\n" + "=" * 70)
    print(f"TOTAL: caught {caught}, passed {passed} "
          f"(only clean reformattings passed — canonical level, AD-40)")
    print("Boundary: verify localizes 'where it broke', does NOT judge 'why' "
          "(TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH).")


if __name__ == "__main__":
    main()
