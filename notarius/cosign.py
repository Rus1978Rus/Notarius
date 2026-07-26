# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — witness co-signing: an external witness for the trace head (AD-36).

Closes the ONE candid hole in the trace (AD-22, defect M4): FORK and
TRUNCATION. An actor with a valid key can sign TWO continuations from
the same point (a fork) and show them to different recipients, or present
a valid PREFIX (truncation). Both branches are internally valid — a
single Merkle/hash chain does NOT tell them apart (verify_trace without
expected_head is blind).

SOLUTION (C2SP tlog-witness / RFC 6962 consistency): the trace head
(checkpoint = size + head) is CO-SIGNED by external witnesses that check
consistency (a new checkpoint is a forward extension of the previous one,
the prefix is not rewritten). A witness stores O(1) (the last checkpoint
per log) and REFUSES to co-sign an inconsistent one. Because the verifier
requires a quorum of co-signatures:
  - a forked branch will not get co-signatures (the witness has already
    seen a head of the same height with a different head) → the fork is
    detected;
  - a truncated prefix will not match the witnessed head (expected_head
    from the witness) → the truncation is detected.

CANDID LIMITS:
  - Catches fork/truncation ONLY if the verifier actually requires a
    quorum of co-signatures. Whoever ignores them is vulnerable again.
  - Witnesses must be online and INDEPENDENT; an M-of-N collusion still
    deceives — the threshold raises the bar, it does not make it impossible.
  - The witness sees the HEAD and consistency, NOT the content/truth
    (SIGNED ≠ NATIVE): it proves "everyone sees ONE log", not "the log is
    truthful".
  - Does not close coercion (AD-28) or self-attestation (AD-24): an actor
    can write a signed lie into the ONE witnessed log — but can no longer
    show DIFFERENT lies to different parties (no equivocation). That is the
    value: an "unnoticed fork" → ONE accountable trace (it strengthens
    AD-10 TRACE_LOCATES_THE_LIE — the trace is now singular).
  - The demo passes the witness the WHOLE trace to check the prefix; in
    production this is a compact O(log n) consistency proof (RFC 6962),
    not the whole log.
"""

from __future__ import annotations

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

from notarius.trace import _canonical, _event_digest


def log_head(trace: list) -> str | None:
    """The log head = digest of the last event. The hash chain
    transitively commits the whole prefix via prev_hash, so head is a
    commitment to the entire trace (the chain's analog of a Merkle root)."""
    return _event_digest(trace[-1]) if trace else None


def _chain_ok(trace: list) -> bool:
    """Internal consistency of the hash-chain links."""
    for i, ev in enumerate(trace):
        if i == 0:
            if ev.get("prev_hash") is not None:
                return False
        elif ev.get("prev_hash") != _event_digest(trace[i - 1]):
            return False
    return True


def _cp_body(checkpoint: dict) -> bytes:
    return _canonical({k: checkpoint[k] for k in ("log_id", "size", "head")})


def make_checkpoint(trace: list, log_id: str, log_priv: bytes) -> dict:
    """A head signed by the log: {log_id, size, head} + the log's signature."""
    body = {"log_id": log_id, "size": len(trace), "head": log_head(trace)}
    sk = SigningKey(log_priv)
    sig = sk.sign(_canonical(body)).signature.hex()
    return {**body, "log_sig": sig, "log_pub": bytes(sk.verify_key).hex()}


class Witness:
    """External witness: co-signs a head if it is a consistent extension of
    the one previously seen for this log. Stores O(1) per log."""

    def __init__(self, priv: bytes):
        self._sk = SigningKey(priv)
        self.pub = bytes(self._sk.verify_key)
        self._seen: dict[tuple, tuple] = {}   # (log_id, log_pub) -> (size, head)
        # BOUNDARY (N-W3, audit 2026-07-26): the fork-protection memory is
        # keyed by (log_id, log_pub). Changing the log's key (rotation OR
        # substitution) starts a NEW record — the history of the previous key
        # is not carried over, and the witness will not catch a fork "through
        # rotation". This is a deliberate trade-off: only an EXTERNAL rotation
        # registry (who succeeds whom) can link key epochs, and that is beyond
        # the scope of a single witness. Bottom line: trust only those log_pub
        # whose rotation such a registry confirms.

    def cosign(self, checkpoint: dict, trace: list) -> dict | None:
        """Co-sign a head, having CHECKED consistency with the trace and with
        what was seen before. Returns a co-signature or None (REFUSAL = fork /
        truncation / rewritten prefix / tampering)."""
        # 1. the log's signature on the head itself
        try:
            VerifyKey(bytes.fromhex(checkpoint["log_pub"])).verify(
                _cp_body(checkpoint), bytes.fromhex(checkpoint["log_sig"]))
        except (BadSignatureError, ValueError, KeyError):
            return None
        # 2. the head matches the presented trace
        if checkpoint["size"] != len(trace) or checkpoint["head"] != log_head(trace):
            return None
        # 3. internal consistency of the chain
        if not _chain_ok(trace):
            return None
        # 4. consistency with what was seen before, by (log_id, log_pub)
        key = (checkpoint["log_id"], checkpoint["log_pub"])
        prev = self._seen.get(key)
        if prev is not None:
            old_size, old_head = prev
            if checkpoint["size"] < old_size:
                return None                       # rollback/truncation
            if checkpoint["size"] == old_size:
                if checkpoint["head"] != old_head:
                    return None                   # FORK at the same height
            elif _event_digest(trace[old_size - 1]) != old_head:
                return None                       # rewritten prefix / fork
        # 5. consistent → co-sign and remember
        cosig = self._sk.sign(_cp_body(checkpoint)).signature.hex()
        self._seen[key] = (checkpoint["size"], checkpoint["head"])
        return {"witness_pub": self.pub.hex(), "cosig": cosig,
                "size": checkpoint["size"], "head": checkpoint["head"]}


def verify_checkpoint(checkpoint: dict, cosignatures: list,
                      witness_keys: set, threshold: int = 1) -> dict:
    """Verifier: does the head carry a quorum of valid co-signatures?
    witness_keys — hex keys of trusted witnesses. Returns
    {ok, cosigners, reasons}."""
    msg = _cp_body(checkpoint)
    valid = set()
    for cs in cosignatures:
        pub = cs.get("witness_pub")
        if pub not in witness_keys:
            continue
        if cs.get("size") != checkpoint["size"] or cs.get("head") != checkpoint["head"]:
            continue
        try:
            VerifyKey(bytes.fromhex(pub)).verify(msg, bytes.fromhex(cs["cosig"]))
            valid.add(pub)
        except (BadSignatureError, ValueError, KeyError):
            continue
    ok = len(valid) >= threshold
    reasons = [] if ok else [f"witness quorum not reached ({len(valid)}/{threshold})"]
    return {"ok": ok, "cosigners": sorted(valid), "reasons": reasons}


def verify_witnessed_trace(trace: list, checkpoint: dict, cosignatures: list,
                           witness_keys: set, threshold: int = 1,
                           **trace_kwargs) -> dict:
    """Full check (closing M4): (1) the head is witnessed by a quorum → a
    trusted expected_head; (2) trace.verify_trace with that head. A fork
    yields a branch with no quorum; truncation — head ≠ witnessed."""
    from notarius.trace import verify_trace
    wc = verify_checkpoint(checkpoint, cosignatures, witness_keys, threshold)
    trusted_head = checkpoint["head"] if wc["ok"] else None
    rep = verify_trace(trace, expected_head=trusted_head, **trace_kwargs)
    rep["witness"] = {"quorum_ok": wc["ok"], "cosigners": wc["cosigners"],
                      "threshold": threshold}
    if not wc["ok"]:
        # FAIL-CLOSED (AD-79, defect surfaced by Kimi): previously, on a
        # failed quorum, it returned INTACT + a textual warning — an API
        # consumer checking status == INTACT got a false "green". Now the
        # status is downgraded to UNWITNESSED_HEAD; the chain result is kept.
        rep["chain_status"] = rep.get("status")
        rep["status"] = "UNWITNESSED_HEAD"
        rep["state"] = "UNVERIFIED"
        rep.setdefault("reasons", []).append(
            "FAIL-CLOSED: head not witnessed by a quorum — fork/truncation "
            "not ruled out; status is NOT INTACT (M4, AD-22; fix AD-79)")
    return rep


if __name__ == "__main__":  # compact demonstration
    from notarius import trace as T
    a_priv = bytes(SigningKey.generate())
    log_priv = bytes(SigningKey.generate())
    w = Witness(bytes(SigningKey.generate()))
    wkeys = {w.pub.hex()}

    tr = T.new_trace("el", "v0", "orig", "alice", a_priv, "t0")
    cp = make_checkpoint(tr, "log-1", log_priv)
    cs = w.cosign(cp, tr)
    print("legit cosign:", "OK" if cs else "REFUSED")

    # fork: a different event at the same height
    fork = T.new_trace("el", "v0-EVIL", "orig", "alice", a_priv, "t0")
    cpf = make_checkpoint(fork, "log-1", log_priv)
    print("fork cosign:  ", "OK" if w.cosign(cpf, fork) else "REFUSED (fork caught)")

    # the verifier sees the fork branch with no quorum
    r = verify_witnessed_trace(fork, cpf, [], wkeys, threshold=1)
    print("verify fork:  ", r["status"], "| quorum:", r["witness"]["quorum_ok"])
