# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — shared document analysis (one engine behind CLI and the web app).

Both `notarius check` (cli.py) and the local web app (webapp.py) call the same
functions here, so they can never drift apart. Nothing here prints; it returns
plain structured data.

Boundary (candidly): it shows WHERE and WHAT differs, and flags hidden
manipulation of the content — it does not judge intent
(TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH).
"""

from __future__ import annotations

import difflib
import hashlib

from notarius.diagnose import diagnose_change
from notarius.scanner import scan_hardened
from notarius.urlcontext import find_url_context_risks


def analyze_documents(orig_text: str, recv_text: str) -> dict:
    """Compare a reference with what arrived. Returns:
      {
        "identical": bool,
        "findings": [ {line, category, review, was, now, human} ],
        "hidden":   {risk, signature},        # content scan of what arrived
        "url_risks":[ {token, host, issues, ...} ],
        "summary":  str,
      }
    """
    if orig_text == recv_text:
        # nothing was introduced by the transfer → no "manipulation" to report
        return {"identical": True, "findings": [], "hidden": {"risk": "OK", "signature": ""},
                "url_risks": [], "summary": "Identical to the reference — untouched."}

    o_lines, r_lines = orig_text.splitlines(), recv_text.splitlines()
    sm = difflib.SequenceMatcher(None, o_lines, r_lines, autojunk=False)
    findings: list[dict] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                was = o_lines[i1 + k] if i1 + k < i2 else ""
                now = r_lines[j1 + k] if j1 + k < j2 else ""
                findings.append(_line_finding(j1 + k + 1, was, now))
        elif tag == "delete":
            for k in range(i1, i2):
                findings.append(_line_finding(j1 + 1, o_lines[k], "«line deleted»"))
        elif tag == "insert":
            for k in range(j1, j2):
                findings.append(_line_finding(k + 1, "«no such line before»", r_lines[k]))

    # "Manipulation" = what the transfer INTRODUCED, not the document's own
    # nature. A legitimately bilingual document (Russian + Latin terms) trips the
    # mixed-script detector, but if the SAME signature is already in the
    # reference, nothing was introduced — do not raise a false alarm.
    recv_scan = scan_hardened(recv_text)
    orig_scan = scan_hardened(orig_text)
    introduced = (recv_scan.get("risk") == "ALARM"
                  and recv_scan.get("signature") != orig_scan.get("signature"))
    hidden = recv_scan if introduced else {"risk": "OK", "signature": ""}

    orig_url_tokens = {u["token"] for u in find_url_context_risks(orig_text)}
    url_risks = [u for u in find_url_context_risks(recv_text)
                 if u["token"] not in orig_url_tokens]      # only newly-introduced ones

    summary = f"{len(findings)} changed line(s)."
    if hidden.get("risk") == "ALARM":
        summary += f" Hidden manipulation introduced ({hidden.get('signature')})."
    if url_risks:
        summary += f" {len(url_risks)} suspicious domain/URL(s)."
    return {"identical": False, "findings": findings, "hidden": hidden,
            "url_risks": url_risks, "summary": summary}


def _line_finding(line: int, was: str, now: str) -> dict:
    diag = diagnose_change(was, now)
    return {"line": line, "category": diag["category"], "review": diag["review"],
            "was": was, "now": now, "human": diag["human"]}


def analyze_files(orig: bytes, recv: bytes) -> dict:
    """Compare ANY two files (bytes). Substrate-independent (AD-88, AD-95):
      - identical bytes           → untouched;
      - both decode as UTF-8 text → full text analysis (where + what changed),
        which covers documents, JSON, CSV, XML, config, logs;
      - otherwise (image/audio/PDF/binary) → an HONEST fingerprint verdict:
        we can say IF the file was tampered, NOT where inside it (that needs a
        format-specific media reader, which this tool does not include).
    """
    so = hashlib.sha256(orig).hexdigest()
    sr = hashlib.sha256(recv).hexdigest()
    if orig == recv:
        return {"kind": "identical", "identical": True, "findings": [],
                "hidden": {"risk": "OK", "signature": ""}, "url_risks": [],
                "ref_sha": so, "recv_sha": sr,
                "summary": "Identical — byte-for-byte the same file."}
    try:
        ot, rt = orig.decode("utf-8"), recv.decode("utf-8")
    except UnicodeDecodeError:
        return {
            "kind": "binary", "identical": False, "findings": [],
            "ref_sha": so, "recv_sha": sr,
            "ref_size": len(orig), "recv_size": len(recv),
            "summary": "The file was CHANGED — its fingerprint differs from the reference.",
            "boundary": ("For images, audio, video and other binary files NOTARIUS "
                         "tells you IF the file was tampered (the fingerprint changed), "
                         "not WHERE inside it — that needs a format-specific reader, "
                         "which this tool does not include."),
        }
    res = analyze_documents(ot, rt)          # text-based: full where+what analysis
    res["kind"] = "text"
    res["ref_sha"], res["recv_sha"] = so, sr
    return res


def scan_document(text: str) -> dict:
    """Scan a single document (no reference): hidden characters, homoglyphs,
    suspicious domains. Returns {hidden:{risk,signature}, url_risks:[...], summary}."""
    hidden = scan_hardened(text)
    url_risks = find_url_context_risks(text)
    if hidden.get("risk") == "ALARM":
        summary = f"ALARM — hidden manipulation ({hidden.get('signature')})."
    elif hidden.get("risk") == "WATCH" or url_risks:
        summary = "WATCH — something worth a look."
    else:
        summary = "OK — no hidden characters or look-alike domains found."
    return {"hidden": hidden, "url_risks": url_risks, "summary": summary}
