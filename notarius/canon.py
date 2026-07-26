# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — transport-encoding canonicalization pre-pass (AD-33).

PORTED from the sibling project Vakhter (rus1978rus/vakhter @ 3763b71,
code/canonicalization/canonicalize.py; same author — Ruslan Malyavskiy).
Pure stdlib, carried over almost verbatim; candid labels added.

WHAT IT DOES: reveals text hidden behind a transport encoding BEFORE the
invisibles scanner reads it:
  - percent-encoding (%2e, %2f), including double (%252e);
  - HTML entities (&#46;, &#x2f;, &#8203;);
  - \\u / \\x escapes;
  - OVERLONG UTF-8 — the classic evasion: a "/" is smuggled as %c0%af
    (2 bytes) or %e0%80%af (3 bytes). A strict decoder rejects them, a
    vulnerable downstream accepts them and sees "/". We show what the
    downstream would see AND raise an overlong flag.
  - numeric IP hosts (http://2130706433/ → http://127.0.0.1/).

CANDID BOUNDARY (important, don't confuse it):
  This is NOT Unicode normalization (NFC/NFD) and does NOT close AD-4. It
  is an ORTHOGONAL thing — against encoding evasion, not against canonical
  character equivalence. It sits ALONGSIDE the scanner, not in place of a
  decision on AD-4. Our NFC is already done by witness.make_envelope.

  Known false positive (inherited from the source): explanatory prose that
  literally mentions "%2f" or "../" will be decoded and may raise suspicion.
  Acceptable for advisory mode, NOT for "silent" blocking. There is no
  positional context (Q3) here; decode depth is bounded by max_depth
  (protection against a decode loop).
"""

from __future__ import annotations

import re
import html
import socket
import struct
import urllib.parse

_ESC = re.compile(r"\\u([0-9a-fA-F]{4})|\\x([0-9a-fA-F]{2})")
_PCT_RUN = re.compile(r"(?:%[0-9a-fA-F]{2})+")


def _decode_escapes(s: str) -> str:
    return _ESC.sub(lambda m: chr(int(m.group(1) or m.group(2), 16)), s)


def decode_utf8_lenient(bs: bytes):
    """Decode bytes as UTF-8, but ACCEPTING overlong forms; raise a flag if
    any are encountered. Shows what a lenient downstream would render (the
    target of the attack). Returns (text, overlong)."""
    out, over, i, n = [], False, 0, len(bs)
    while i < n:
        b = bs[i]
        if b < 0x80:
            out.append(chr(b)); i += 1
        elif 0xC0 <= b <= 0xDF and i + 1 < n:
            cp = ((b & 0x1F) << 6) | (bs[i + 1] & 0x3F)
            if cp < 0x80:                       # overlong 2-byte
                over = True
            out.append(chr(cp)); i += 2
        elif 0xE0 <= b <= 0xEF and i + 2 < n:
            cp = ((b & 0x0F) << 12) | ((bs[i + 1] & 0x3F) << 6) | (bs[i + 2] & 0x3F)
            if cp < 0x800:                      # overlong 3-byte
                over = True
            out.append(chr(cp)); i += 3
        elif 0xF0 <= b <= 0xF4 and i + 3 < n:
            cp = ((b & 0x07) << 18) | ((bs[i + 1] & 0x3F) << 12) | \
                 ((bs[i + 2] & 0x3F) << 6) | (bs[i + 3] & 0x3F)
            if cp < 0x10000:                    # overlong 4-byte
                over = True
            out.append(chr(cp) if cp <= 0x10FFFF else "�"); i += 4
        else:
            out.append(chr(b) if b < 0x100 else "�"); i += 1   # lone byte
    return "".join(out), over


def _decode_pct_runs(s: str):
    """Replace each %XX run with its LENIENT-UTF8 decoding.
    Returns (s, overlong)."""
    seen = {"over": False}

    def repl(m):
        txt, over = decode_utf8_lenient(urllib.parse.unquote_to_bytes(m.group(0)))
        if over:
            seen["over"] = True
        return txt

    return _PCT_RUN.sub(repl, s), seen["over"]


def _one_pass(s: str):
    s = _decode_escapes(s)             # \\u002e  \\x2f
    s, over = _decode_pct_runs(s)      # %2e %2f  AND overlong %c0%af
    s = html.unescape(s)               # &#46; &#x2f; &#8203;
    return s, over


def decode_layers(text: str, max_depth: int = 3):
    """Iteratively peel encoding layers to a fixed point or max_depth.
    Returns (canon, passes, overlong)."""
    cur, passes, overlong = text, 0, False
    for _ in range(max_depth):
        nxt, over = _one_pass(cur)
        overlong = overlong or over
        if nxt == cur:
            break
        cur, passes = nxt, passes + 1
    return cur, passes, overlong


def _int_to_ip(n):
    return socket.inet_ntoa(struct.pack("!I", n)) if 0 <= n <= 0xFFFFFFFF else None


def normalize_ip_hosts(text: str) -> str:
    """A numeric host in a URL (decimal/hex) → dotted-quad, so that an IP
    map (if one appears) can see it. Normalization only, not a verdict."""
    def repl(m):
        scheme, host = m.group(1), m.group(2)
        try:
            n = int(host, 16) if host.lower().startswith("0x") else \
                int(host) if host.isdigit() else None
        except ValueError:
            n = None
        ip = _int_to_ip(n) if n is not None else None
        return f"{scheme}{ip}" if ip else m.group(0)
    return re.sub(r"(https?://)([^/\s:?#]+)", repl, text, flags=re.I)


def canonicalize(text: str, max_depth: int = 3):
    """Reveal the transport encoding. Returns (canon, meta), where
    meta = {decode_passes, overlong_utf8, changed}. NOT Unicode normalization."""
    decoded, passes, overlong = decode_layers(text, max_depth)
    canon = normalize_ip_hosts(decoded)
    return canon, {"decode_passes": passes, "overlong_utf8": overlong,
                   "changed": canon != text}
