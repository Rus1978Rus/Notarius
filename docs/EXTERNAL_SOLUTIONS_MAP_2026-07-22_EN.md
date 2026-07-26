# Open problems → ready solutions in adjacent disciplines

DATE: 2026-07-22
BASIS: the author's question — "why reinvent the wheel? how is this solved in
hashing and other systems?". Discipline: the parent's EXTERNAL_METHODOLOGY_LIBRARY
(`RECURRENCE = WORTH_STUDYING`, `STRUCTURAL_ANALOGY ≠
NORMATIVE_BORROWING`, cross-domain transfer FO-013).
MAIN CONCLUSION: almost all our "open" problems are SOLVED,
standardized problems in mature fields. There is no need to invent —
we need to adopt what is ready (adopt-don't-invent).

---

## Direct answer to the question: "the signature lives as long as the algorithm lives"

This is **long solved and standardized**. The field is long-term
archival signing (LTANS).

**RFC 4998 Evidence Record Syntax (2007)** and **RFC 4810**: signed
data that must be kept 30+ years is protected via **Archive
Timestamp renewal** — BEFORE the hash/algorithm weakens, the record is
re-hashed with a stronger algorithm and re-timestamped, and the
proof chain is preserved. That is, a long-term signature is
not a single act forever, but a **renewal process** (exactly the "re-signing
ritual" that we called open — it was standardized 18 years
ago).

Industrial formats on top of this: **CAdES / XAdES / PAdES-LTA**
(eIDAS, legally recognized in the EU). Plus:
- **Crypto-agility** — design the system so the algorithm can
  be replaced without rebuilding everything.
- **Post-quantum hash signatures** (XMSS — RFC 8391; SLH-DSA/SPHINCS+ —
  FIPS 205, 2024): their strength relies ONLY on the strength of the hash, which
  is ideal for the long term.

**Conclusion:** Kimi's meta-finding ("they outlive the carrier, not the
algorithm") is correct as a problem, but the solution is ready: re-timestamp per RFC 4998 +
crypto-agility + hash signatures. Our `envelope_v2` / `trace` should
simply be able to re-sign — not invent a mechanism.

---

## Map: problem → discipline → ready solution → what to take

| Our open problem | Who already solved it | Standard / technique | What to take |
|---|---|---|---|
| The algorithm dies before the carrier | Long-term archive (LTANS) | RFC 4998 ERS, RFC 4810, *AdES-LTA | re-timestamp before weakening; crypto-agility; hash signatures |
| **Fork / split-view** (M4) | Transparency logs | **Witness cosigning** (Certificate Transparency, Sigsum, C2SP tlog-witness, ArmoredWitness) | external witnesses co-sign a checkpoint; a single Merkle chain does NOT catch a fork — witnesses do |
| **Tail truncation** (M4) | Transparency logs | signed tree head + **consistency proof** (RFC 6962) | publish the signed head; check the consistency proof |
| Whom to trust the key across centuries | PKI / key transparency | CONIKS / Key Transparency, WKD, distributed archives | anchor the key in a witnessed log or several independent archives, don't send a "bare" key |
| Recovery from carrier damage | Coding theory | **Reed-Solomon**, erasure/fountain codes, QR (up to 30% loss), PAR2 | add correction redundancy; don't invent |
| Binding a record to a physical object | Anti-counterfeit / hardware | PUF, DNA taggant, hologram, fiber pattern | it exists, but is expensive/complex — candidly stays semi-open for the cheap case |
| Trusted time (not self-declared, №3) | Timestamping | **RFC 3161 TSA**, **OpenTimestamps** (anchor in Bitcoin), Roughtime | bind the `at` field to a TSA/blockchain, don't declare it |
| Self-attestation: the actor signs their own lie (№1) | Law, accounting, distributed systems | chain of custody + witnesses; the "four eyes" principle / separation of duties; BFT — M-of-N signers | require SEVERAL independent signers; truth is outside crypto's reach (`SIGNED ≠ TRUE`) |
| Meaning across thousands of years (the whole stack) | Archival science | **OAIS (ISO 14721)**, LOCKSS, format migration | E-Continuity already stands on OAIS — build on it further |

---

## What this changes for the project (honestly)

1. **We take the crypto plumbing ready, we don't invent it.** Merkle, Ed25519,
   RFC 4998 re-signing, witness-cosigning, RFC 3161 time,
   Reed-Solomon — all standardized and deployed. Our prototype
   should INTEGRATE them, not rewrite them.
2. **Where the project's real value is** (confirms the AD-8 niche): NOT in
   new crypto — all the crypto is someone else's and mature — but in the **semantic layer
   and human-readable assembly**: "which FIELD, who, where is the break, explain it to a
   human." The ready systems (CT, Sigsum) don't give this — they are about
   certificates and artifacts, not the meaning of a business element.
3. **The M4 fork — not our wheel to fix.** Witness cosigning solves it
   in a standard way; you just plug in an external witness, rather than
   inventing consensus.
4. **Self-attestation (№1) is solved by NO ONE cryptographically** — and that is
   an honest universal limit, not our defect. The adjacent fields
   (law, accounting) don't "solve" it, they RESTRAIN it with independence
   (several witnesses, separation of duties). That is our path too.

## Recommended next step (candidate for AUTHOR_DECISION)

Rewrite the open items of AD-22 from "invent" to "integrate a
standard":
- M4 fork → witness cosigning (a Sigsum-like external witness);
- M4 truncation → RFC 6962 consistency proof + signed head;
- time → OpenTimestamps/RFC 3161;
- longevity → RFC 4998 re-timestamp + hash signatures;
- damage → Reed-Solomon over the carrier;
- self-attestation → M-of-N independent signers (separation of duties).
No item requires a new invention — only assembly.

## Sources

- Long-term signing: [RFC 4998 ERS](https://www.rfc-editor.org/rfc/rfc4998), [RFC 4810 LTA Requirements](https://datatracker.ietf.org/doc/html/rfc4810)
- Fork/witnesses: [transparency.dev: witness network](https://blog.transparency.dev/can-i-get-a-witness-network), [C2SP tlog-witness](https://github.com/C2SP/C2SP/blob/main/tlog-witness.md), [Witness Cosigning (UCL)](https://discovery.ucl.ac.uk/10116629/1/Jovanovic_cosi.pdf)
- Hash signatures (post-quantum): XMSS RFC 8391; SLH-DSA FIPS 205.
- Time: RFC 3161; OpenTimestamps.
- Correction: Reed-Solomon; RFC 6962 (Merkle consistency).
- Archive: OAIS ISO 14721; LOCKSS.
