# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — domain/URL awareness (AD-81).

The idea comes from the msl_mip audit (AD-80): an invisible/lookalike in
DIFFERENT parts of a URL carries different risk. In the DOMAIN (host) an
invisible/lookalike is ALWAYS illegitimate → HIGH; in the path/query →
MEDIUM. Plus userinfo spoofing "brand@other-host" (`paypal.com@evil.ru`) —
the eye anchors on the brand BEFORE the @. msl_mip's code was NOT copied
(there it uses public_suffix + _detect_context_at); here is our own light
implementation without a PSL.

Hits the reviewers' top vertical (BEC / swapped payment link): `paypаl.com`
(Cyr. а), `goog‹ZWSP›le.com`, `paypal.com@evil.ru`.

Boundary: a "looks like a domain" heuristic (label.label, TLD ≥2 letters),
NOT a public-suffix check; advisory, blocks nothing.
"""

from __future__ import annotations

import re

from notarius.detect import _monitored
from notarius.homoglyph import confusables_in, deconfuse

_DOMAINISH = re.compile(r"[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+")
_SCHEME = re.compile(r"^([A-Za-z][A-Za-z0-9+.\-]*)://(.*)$")


def _canon(tok: str) -> str:
    """Strip invisibles and reduce lookalikes — "how it actually looks"."""
    return deconfuse("".join(c for c in tok if not _monitored(c)))


def _looks_domain(tok: str) -> bool:
    c = _canon(tok)
    if not _DOMAINISH.fullmatch(c):
        return False
    last = c.rsplit(".", 1)[-1]
    return len(last) >= 2 and last.isalpha()


def _issues(part: str) -> tuple[list[str], list[str]]:
    """(lookalikes, invisibles) in a part of the string."""
    conf = [f"U+{ord(c):04X}" for c in confusables_in(part)]
    inv = [f"U+{ord(c):04X}" for c in part if _monitored(c)]
    return conf, inv


def find_url_context_risks(text: str) -> list[dict]:
    """Find suspicious URL/domain/email tokens tied to their context.
    Returns a list of findings {token, context, issue, chars, risk}."""
    out: list[dict] = []
    if not isinstance(text, str):
        return out
    for tok in text.split():
        core = tok
        m = _SCHEME.match(tok)
        if m:
            core = m.group(2)
        userinfo, hostpart = None, core
        if "@" in core:
            userinfo, hostpart = core.rsplit("@", 1)
        host = re.split(r"[/:?#]", hostpart, 1)[0]
        rest = hostpart[len(host):]

        is_url = bool(m) or _looks_domain(host) or (
            userinfo is not None and _looks_domain(host))
        if not is_url:
            continue

        # 1) userinfo spoof: the part before @ itself looks like a domain (brand@host)
        if userinfo and _looks_domain(userinfo):
            out.append({"token": tok, "context": "USERINFO", "issue": "userinfo_spoof",
                        "chars": [userinfo], "risk": "HIGH"})

        # 2) lookalike/invisible IN THE DOMAIN → always HIGH
        h_conf, h_inv = _issues(host)
        if h_conf:
            out.append({"token": tok, "context": "HOST", "issue": "homoglyph_in_host",
                        "chars": h_conf, "risk": "HIGH"})
        if h_inv:
            out.append({"token": tok, "context": "HOST", "issue": "invisible_in_host",
                        "chars": h_inv, "risk": "HIGH"})

        # 3) in the path/query → MEDIUM (not a silent pass, but not the domain)
        r_conf, r_inv = _issues(rest)
        if r_conf or r_inv:
            out.append({"token": tok, "context": "PATH", "issue": "homoglyph_or_invisible_in_path",
                        "chars": r_conf + r_inv, "risk": "MEDIUM"})
    return out


def scan_url(text: str) -> dict:
    """Summary: worst URL-context risk + signature + findings."""
    f = find_url_context_risks(text)
    if not f:
        return {"risk": "OK", "signature": "", "findings": []}
    high = [x for x in f if x["risk"] == "HIGH"]
    top = high[0] if high else f[0]
    return {"risk": "ALARM" if high else "WATCH",
            "signature": top["issue"], "findings": f}
