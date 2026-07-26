#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Verifying the core on DIFFERENT carriers, not just text (AD-88).

Substrate-independence (FO-013): the core works on any element. One managed
set (notarius.record), but the fields carry DIFFERENT carriers:
  - сумма            — text/number
  - печать_директора — image (PNG)
  - аудио_согласие   — sound (WAV)
  - реестр_позиций   — data (JSON)

Each field stores the FINGERPRINT of its file (sha256) and has its own keeper.
Substituting ANY carrier changes the fingerprint → the core catches it and
binds it to the field — with the same machine as text. HONEST BOUNDARY: we
catch "this carrier was touched / by the wrong keeper", but NOT "where inside
the image/sound" (for that you need a media reader — separate, outside the core).

Run: python3 scripts/carriers_demo.py
"""

import base64
import hashlib
import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nacl.signing import SigningKey                                   # noqa: E402

from notarius.record import (create_record, rebuild, audit,           # noqa: E402
                             human_audit)

# 1×1 PNG (a real image carrier)
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
    "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")


def tiny_wav() -> bytes:
    """Minimal valid WAV (sound carrier): header + silence."""
    data = b"\x00\x00" * 8
    return (b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE"
            + b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, 8000, 16000, 2, 16)
            + b"data" + struct.pack("<I", len(data)) + data)


def fp(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kp():
    p = bytes(SigningKey.generate())
    return p, bytes(SigningKey(p).verify_key).hex()


def line(c="─"):
    print(c * 68)


def main():
    ws = Path(tempfile.mkdtemp(prefix="carriers_"))
    files = {
        "сумма": ws / "amount.txt",
        "печать_директора": ws / "stamp.png",
        "аудио_согласие": ws / "consent.wav",
        "реестр_позиций": ws / "items.json",
    }
    files["сумма"].write_text("1000000 USD", encoding="utf-8")
    files["печать_директора"].write_bytes(PNG)
    files["аудио_согласие"].write_bytes(tiny_wav())
    files["реестр_позиций"].write_text('{"позиций": 3, "итог": 1000000}', encoding="utf-8")

    a_priv, _ = kp()
    keepers = {"сумма": "Казначей", "печать_директора": "Нотариус",
               "аудио_согласие": "Секретарь", "реестр_позиций": "Бухгалтер"}
    kk = {}
    kprivs = {}
    for role in set(keepers.values()):
        kprivs[role], kk[role] = kp()

    # field values = file FINGERPRINTS (carrier-agnostic)
    fields = {name: fp(path) for name, path in files.items()}
    rec = create_record(fields, keepers, kk, "Автор", a_priv, "09:00")

    line("═"); print("A SET OF DIFFERENT CARRIERS (each with its own keeper):"); line("═")
    for name, path in files.items():
        kind = {"txt": "text", "png": "image", "wav": "sound", "json": "data"}[path.suffix[1:]]
        print(f"   {name:20} [{kind:8}] fingerprint {fp(path)[:16]}…  keeper '{keepers[name]}'")

    # ── original: compare current file fingerprints against the seal ────
    current = {name: fp(path) for name, path in files.items()}
    print("\n① ORIGINAL:", human_audit(audit(rec, [], current)))

    # ── IMAGE substitution: flip one byte in the PNG ───────────────────
    b = bytearray(files["печать_директора"].read_bytes())
    b[-5] ^= 0x01                              # 1 bit in the image body
    files["печать_директора"].write_bytes(bytes(b))
    current2 = {name: fp(path) for name, path in files.items()}
    line("═"); print("② IMAGE SUBSTITUTION (director's stamp, 1 byte):"); line("═")
    print("   " + human_audit(audit(rec, [], current2)).replace("\n", "\n   "))

    # ── SOUND substitution: change a sample in the WAV ─────────────────
    w = bytearray(files["аудио_согласие"].read_bytes())
    w[-1] ^= 0xFF
    files["аудио_согласие"].write_bytes(bytes(w))
    current3 = {name: fp(path) for name, path in files.items()}
    line("═"); print("③ SOUND SUBSTITUTION (audio consent) + image still tampered:"); line("═")
    print("   " + human_audit(audit(rec, [], current3)).replace("\n", "\n   "))

    line("═")
    print("POINT: the core (notarius.record) governs image, sound, data and text")
    print("with ONE machine — via a fingerprint not tied to the carrier. Substituting")
    print("any carrier is localized to the FIELD and bound to its keeper.")
    print("BOUNDARY: we catch 'the carrier was touched', NOT 'where inside the image/sound'")
    print("(for that you need a separate media reader, outside the core).")
    print(f"\nsandbox (safe to delete): {ws}")
    line("═")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
