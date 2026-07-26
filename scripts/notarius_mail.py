#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS for real mail: two accounts, real verification (AD-71).

A thin "folders → SMTP/IMAP" adapter from the AD-70 demo, taken to a working
tool. Standard Python (smtplib/imaplib/email) + our product (seal/check).
No extra dependencies.

TWO SIDES:
  send  — sender: SEALS the document (puts the reference into a shared registry
          via ANOTHER road) and mails the attachment over SMTP.
  recv  — receiver: pulls incoming mail over IMAP, extracts the attachment and
          RECONCILES it against the reference in the registry → human-readable
          where/what verdict.

KEY POINT (why this honestly works):
  The reference travels NOT in the email but into a shared registry (REGISTRY_DIR)
  — a folder both sides see (on one machine — just a folder; across machines — a
  shared cloud folder / network drive / small share). An interceptor edits the
  email but can't reach the registry.

SETUP (environment variables; do NOT hardcode passwords):
  NOTARIUS_REGISTRY   path to the shared registry "under glass" (required)
  NOTARIUS_USER       account address/login
  NOTARIUS_PASS       app password (app password!), not your main password
  NOTARIUS_SMTP       host:port (e.g. smtp.gmail.com:587)
  NOTARIUS_IMAP       host:port (e.g. imap.gmail.com:993)
  NOTARIUS_SMTP_SEC   starttls (default) | ssl

EXAMPLES:
  # sender (account alpha):
  NOTARIUS_REGISTRY=~/reestr NOTARIUS_USER=alpha@x NOTARIUS_PASS=app-pass \\
  NOTARIUS_SMTP=smtp.x:587 python3 scripts/notarius_mail.py send schet.txt --to beta@y

  # receiver (account beta):
  NOTARIUS_REGISTRY=~/reestr NOTARIUS_USER=beta@y NOTARIUS_PASS=app-pass \\
  NOTARIUS_IMAP=imap.y:993 python3 scripts/notarius_mail.py recv

  # test the logic WITHOUT network or passwords (a shared folder instead of mail):
  python3 scripts/notarius_mail.py selftest

BOUNDARY (candidly): real mail doesn't corrupt the attachment by itself — to see
a catch, the substitution must be staged (edit the received file). No reference in
the registry → nothing to compare against (AD-68): the sender must SEAL at the source.
"""

import argparse
import email
import imaplib
import os
import shutil
import smtplib
import ssl
import sys
import tempfile
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from notarius.cli import cmd_check, cmd_seal   # noqa: E402


# ── shared registry "under glass" ─────────────────────────────────────
def registry_dir() -> Path:
    p = os.environ.get("NOTARIUS_REGISTRY")
    if not p:
        sys.exit("✘ set NOTARIUS_REGISTRY — path to the shared registry")
    d = Path(p).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    return d


def seal_into_registry(doc: Path) -> Path:
    """Seal at the source: put the reference into the registry (first-wins)."""
    reg = registry_dir()
    canon = reg / doc.name
    if canon.exists():
        print(f"⚠ registry already has a reference for {doc.name} — first-wins, "
              f"the new one does NOT overwrite")
    else:
        shutil.copy(doc, canon)
        cmd_seal(str(canon))
    return canon


def build_message(sender: str, to: str, subject: str, doc: Path) -> EmailMessage:
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = sender, to, subject
    msg.set_content("The document is attached. Verified by NOTARIUS (reconcile with the registry).")
    data = doc.read_bytes()
    msg.add_attachment(data, maintype="application", subtype="octet-stream",
                       filename=doc.name)
    return msg


# ── transport: real mail ──────────────────────────────────────────────
def smtp_send(msg: EmailMessage) -> None:
    host, _, port = os.environ.get("NOTARIUS_SMTP", "").partition(":")
    if not host:
        sys.exit("✘ set NOTARIUS_SMTP=host:port")
    user, pw = os.environ["NOTARIUS_USER"], os.environ["NOTARIUS_PASS"]
    port = int(port or 587)
    sec = os.environ.get("NOTARIUS_SMTP_SEC", "starttls")
    ctx = ssl.create_default_context()
    if sec == "ssl":
        with smtplib.SMTP_SSL(host, port, context=ctx) as s:
            s.login(user, pw); s.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as s:
            s.starttls(context=ctx); s.login(user, pw); s.send_message(msg)
    print(f"✔ sent to {msg['To']} via {host}:{port}")


def imap_fetch(save_dir: Path) -> list[Path]:
    host, _, port = os.environ.get("NOTARIUS_IMAP", "").partition(":")
    if not host:
        sys.exit("✘ set NOTARIUS_IMAP=host:port")
    user, pw = os.environ["NOTARIUS_USER"], os.environ["NOTARIUS_PASS"]
    saved = []
    with imaplib.IMAP4_SSL(host, int(port or 993)) as m:
        m.login(user, pw); m.select("INBOX")
        typ, data = m.search(None, "UNSEEN")
        for num in data[0].split():
            _, msg_data = m.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            saved += _extract_attachments(msg, save_dir)
    return saved


def _extract_attachments(msg, save_dir: Path) -> list[Path]:
    out = []
    for part in msg.walk():
        fn = part.get_filename()
        if fn and part.get_content_disposition() == "attachment":
            dest = save_dir / fn
            dest.write_bytes(part.get_payload(decode=True))
            out.append(dest)
    return out


# ── transport: folder (dry-run / across machines via a shared drive) ───
def folder_send(msg: EmailMessage, maildrop: Path) -> None:
    maildrop.mkdir(parents=True, exist_ok=True)
    n = len(list(maildrop.glob("*.eml")))
    (maildrop / f"msg_{n:04d}.eml").write_bytes(bytes(msg))
    print(f"✔ message dropped into the mail yard: {maildrop}")


def folder_fetch(maildrop: Path, save_dir: Path) -> list[Path]:
    saved, seen = [], maildrop / ".seen"
    seen.mkdir(exist_ok=True)
    for eml in sorted(maildrop.glob("*.eml")):
        msg = email.message_from_bytes(eml.read_bytes())
        saved += _extract_attachments(msg, save_dir)
        shutil.move(str(eml), seen / eml.name)
    return saved


# ── reconcile incoming against the registry reference ──────────────────
def verify_incoming(received: list[Path]) -> int:
    reg = registry_dir()
    if not received:
        print("— no new attachments"); return 0
    worst = 0
    for got in received:
        canon = reg / got.name
        print("\n" + "#" * 66)
        print(f"# INCOMING: {got.name}")
        print("#" * 66)
        if not canon.exists():
            print(f"⚠ NO REFERENCE in the registry for '{got.name}' — nothing to compare against.")
            print("  The sender did NOT seal the document at the source (AD-68).")
            worst = max(worst, 2); continue
        rc = cmd_check(str(canon), str(got))
        worst = max(worst, rc)
    return worst


# ── commands ──────────────────────────────────────────────────────────
def cmd_send(args) -> int:
    doc = Path(args.file).expanduser()
    if not doc.exists():
        sys.exit(f"✘ file not found: {doc}")
    seal_into_registry(doc)                       # seal at the source
    sender = os.environ.get("NOTARIUS_USER", "sender@local")
    subject = args.subject or f"[NOTARIUS] {doc.name}"
    msg = build_message(sender, args.to, subject, doc)
    if args.maildrop:
        folder_send(msg, Path(args.maildrop).expanduser())
    else:
        smtp_send(msg)
    return 0


def cmd_recv(args) -> int:
    save = Path(args.save_dir).expanduser() if args.save_dir else Path(tempfile.mkdtemp(prefix="ntr_in_"))
    save.mkdir(parents=True, exist_ok=True)
    if args.maildrop:
        got = folder_fetch(Path(args.maildrop).expanduser(), save)
    else:
        got = imap_fetch(save)
    return verify_incoming(got)


def cmd_selftest(_args) -> int:
    """Full run WITHOUT network: shared folder instead of mail, attachment intercept."""
    ws = Path(tempfile.mkdtemp(prefix="ntr_selftest_"))
    reg, drop, inbox = ws / "reestr", ws / "maildrop", ws / "inbox"
    os.environ["NOTARIUS_REGISTRY"] = str(reg)
    doc = ws / "schet_77.txt"
    doc.write_text("INVOICE No.77\npayer: Client LLC\namount due: 1000000 USD\n",
                   encoding="utf-8")
    print("== 1. Sender seals and sends ==")
    cmd_send(argparse.Namespace(file=str(doc), to="beta@local", subject=None,
                                maildrop=str(drop)))
    print("\n== 2. The MAILMAN edits the attachment in the mail yard ==")
    import email.policy
    for eml in drop.glob("*.eml"):
        msg = email.message_from_bytes(eml.read_bytes(), policy=email.policy.default)
        for part in msg.iter_attachments():
            fn = part.get_filename()
            data = part.get_payload(decode=True).replace(b"1000000", b"9000000")
            part.set_content(data, maintype="application", subtype="octet-stream",
                             filename=fn)
        eml.write_bytes(msg.as_bytes())
    print("  amount in attachment: 1000000 → 9000000")
    print("\n== 3. Receiver pulls and reconciles ==")
    rc = cmd_recv(argparse.Namespace(save_dir=str(inbox), maildrop=str(drop)))
    print(f"\nSelftest OK (rc={rc}: 1 = break caught). Sandbox: {ws}")
    return 0 if rc in (0, 1, 2) else rc


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="notarius_mail", description="NOTARIUS over mail")
    sub = p.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("send", help="seal and send")
    ps.add_argument("file"); ps.add_argument("--to", required=True)
    ps.add_argument("--subject"); ps.add_argument("--maildrop")
    ps.set_defaults(fn=cmd_send)
    pr = sub.add_parser("recv", help="fetch and reconcile")
    pr.add_argument("--save-dir"); pr.add_argument("--maildrop")
    pr.set_defaults(fn=cmd_recv)
    pt = sub.add_parser("selftest", help="full run without network")
    pt.set_defaults(fn=cmd_selftest)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
