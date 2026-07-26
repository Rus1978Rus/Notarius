# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — minimal product: run it on YOUR OWN document (AD-64).

Three commands, all from the ready-made core, no keys and no setup (pure stdlib):

  python3 -m notarius check REFERENCE INCOMING
        compare your reference with what arrived, and say IN PLAIN TERMS
        where and what was swapped (line number + what exactly + hidden edits).

  python3 -m notarius seal FILE
        take a "receipt" of the original (a fingerprint) → FILE.ntr.

  python3 -m notarius verify FILE
        check a file against its receipt: is it the same or has it been touched.

Boundary (candidly): we show WHERE the swap is, we do not pass a verdict on
intent (TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH).
"""

from __future__ import annotations

import difflib
import hashlib
import json
import sys
from pathlib import Path

from notarius.diagnose import diagnose_change
from notarius.scanner import scan_hardened


def _read_text(path: str) -> tuple[str | None, bytes]:
    raw = Path(path).read_bytes()
    try:
        return raw.decode("utf-8"), raw
    except UnicodeDecodeError:
        return None, raw


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_RECEIPT_FIELDS = ("file", "sha256", "size", "scan_risk", "note")


def _canon(body: dict) -> bytes:
    return json.dumps(body, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


# ── check: where and what was swapped ─────────────────────────────────
def cmd_check(orig_path: str, recv_path: str) -> int:
    o_text, o_raw = _read_text(orig_path)
    r_text, r_raw = _read_text(recv_path)

    print("═" * 64)
    print(f"REFERENCE: {orig_path}")
    print(f"ARRIVED:   {recv_path}")
    print("═" * 64)

    if o_raw == r_raw:
        print("✔ ORIGINAL UNTOUCHED — byte-for-byte identical to the reference.")
        return 0

    if o_text is None or r_text is None:
        print("⚠ BREAK — the files differ (binary, line-by-line parsing does not")
        print(f"  apply). Reference {_sha(o_raw)[:16]}…, arrived {_sha(r_raw)[:16]}…")
        return 1

    o_lines, r_lines = o_text.splitlines(), r_text.splitlines()
    sm = difflib.SequenceMatcher(None, o_lines, r_lines, autojunk=False)
    findings = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                old = o_lines[i1 + k] if i1 + k < i2 else ""
                new = r_lines[j1 + k] if j1 + k < j2 else ""
                findings.append((j1 + k + 1, old, new))
        elif tag == "delete":
            for k in range(i1, i2):
                findings.append((j1 + 1, o_lines[k], "«line deleted»"))
        elif tag == "insert":
            for k in range(j1, j2):
                findings.append((k + 1, "«no such line before»", r_lines[k]))

    print(f"✘ BREAK — changed lines: {len(findings)}\n")
    for lineno, old, new in findings:
        diag = diagnose_change(old, new)
        print(f"  line {lineno}: {diag['category']}  (review: {diag['review']})")
        print(f"      was:  {old!r}")
        print(f"      now:  {new!r}")
        print(f"      → {diag['human']}")
        print()

    scan = scan_hardened(r_text)
    if scan["risk"] == "ALARM":
        print(f"⚑ HIDDEN EDIT: {scan['signature']} — invisible characters are")
        print("  concealed in what arrived (the edit was masked).\n")

    print("─" * 64)
    print("Result: shown WHERE and WHAT differs from your reference.")
    print("The verdict on intent (mistake or swap) is up to a human.")
    return 1


# ── seal / verify: a SIGNED receipt on the original ───────────────────
def cmd_seal(path: str) -> int:
    from nacl.signing import SigningKey            # lazy: check stays stdlib
    raw = Path(path).read_bytes()
    text, _ = _read_text(path)
    scan = scan_hardened(text) if text is not None else {"risk": "n/a", "signature": ""}
    body = {"file": Path(path).name, "sha256": _sha(raw), "size": len(raw),
            "scan_risk": scan["risk"], "note": "NOTARIUS signed receipt v2"}
    sk = SigningKey.generate()                     # a fresh key for this receipt
    receipt = {**body, "pub": bytes(sk.verify_key).hex(),
               "sig": sk.sign(_canon(body)).signature.hex()}
    out = Path(path).with_suffix(Path(path).suffix + ".ntr")
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✔ Receipt taken and SIGNED: {out}")
    print(f"  fingerprint: {body['sha256'][:16]}…  size: {body['size']} B")
    print(f"  receipt key: {receipt['pub'][:16]}… — record it separately, so that on")
    print("     verification you can confirm the key is the same (otherwise the receipt was swapped).")
    if scan["risk"] == "ALARM":
        print(f"  ⚑ warning: hidden characters are already in the original ({scan['signature']})")
    return 0


def cmd_verify(path: str) -> int:
    from nacl.exceptions import BadSignatureError
    from nacl.signing import VerifyKey
    rec_path = Path(path).with_suffix(Path(path).suffix + ".ntr")
    if not rec_path.exists():
        print(f"✘ No receipt {rec_path} — nothing to check against (seal first).")
        return 2
    receipt = json.loads(rec_path.read_text(encoding="utf-8"))
    # 1. Is the RECEIPT ITSELF intact? (N-W1, audit 2026-07-26): earlier the
    # .ntr was unsigned — an attacker edited the file, recomputed the hash in
    # the receipt, and got a false "✔ untouched". Now the receipt's signature
    # catches this.
    body = {k: receipt[k] for k in _RECEIPT_FIELDS if k in receipt}
    try:
        VerifyKey(bytes.fromhex(receipt["pub"])).verify(
            _canon(body), bytes.fromhex(receipt["sig"]))
    except (BadSignatureError, ValueError, KeyError):
        print("✘ RECEIPT FORGED — its signature does not check out (the receipt was edited).")
        return 1
    now = _sha(Path(path).read_bytes())
    print("═" * 64)
    print(f"  receipt key: {receipt['pub'][:16]}… (confirm it is the same as at seal time)")
    if now == receipt["sha256"]:
        print(f"✔ UNTOUCHED — {path} matches the signed receipt.")
        return 0
    print(f"✘ CHANGED — {path} does NOT match the receipt.")
    print(f"  was:  {receipt['sha256'][:16]}…")
    print(f"  now:  {now[:16]}…")
    print(f"  To see WHERE and WHAT: notarius check <reference> {path}")
    return 1


_USAGE = __doc__


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(_USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    try:
        if cmd == "check" and len(rest) == 2:
            return cmd_check(rest[0], rest[1])
        if cmd == "seal" and len(rest) == 1:
            return cmd_seal(rest[0])
        if cmd == "verify" and len(rest) == 1:
            return cmd_verify(rest[0])
    except FileNotFoundError as e:
        print(f"✘ File not found: {e.filename}")
        return 2
    print("Invalid command. Help: python3 -m notarius --help")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
