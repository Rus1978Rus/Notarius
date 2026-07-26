# Architecture: CORE + pluggable READERS + DOORS

DATE: 2026-07-25. STATUS: LLM_GENERATED. The short scheme we arrived at:
the engine is a carrier-agnostic CORE at the center; around it — pluggable READERS for
each carrier (raw material); on the outside — DOORS (the buyer's integrations).

## Scheme

```
┌───────────────── DOORS (integrations) ─────────────────┐
│   mail · messenger · CRM · EDI · accounting             │
│   written by the BUYER (not us)                         │
│                                                         │
│   ┌──────── CARRIER READERS (RAW MATERIAL) ────────┐    │
│   │  text:  detect/canon/homoglyph/url             │    │
│   │         + MSL/Vakhter maps                     │    │
│   │  image / audio / video:  ⛔ needs              │    │
│   │         a media reader (candidate)             │    │
│   │  "what CHANGED inside the carrier"             │    │
│   │                                                │    │
│   │   ┌───────────── CORE (ours) ──────────────┐   │    │
│   │   │  carrier-AGNOSTIC, on the FINGERPRINT   │   │    │
│   │   │  • trace   — event chain                │   │    │
│   │   │  • record  — fields+keepers+footnote    │   │    │
│   │   │  • title/anchor/cosign — seal,          │   │    │
│   │   │    registry "under glass", witnesses    │   │    │
│   │   │  • Ed25519 signature / FROST threshold  │   │    │
│   │   └─────────────────────────────────────────┘   │    │
│   └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Three rings

**CORE (ours, carrier-agnostic).** Works on the FINGERPRINT — any carrier.
Answers: whose chain, whose link broke, who keeps the field, who edited it
(the footnote), native/inserted, clean/forged. Modules: trace, record, title,
anchor, cosign, frost, Ed25519 signature. This is precisely what we build and defend.

**CARRIER READERS (RAW MATERIAL, pluggable).** They answer "what CHANGED INSIDE
the carrier": for text — detect/canon/homoglyph/urlcontext + MSL/Vakhter maps
(raw-material suppliers); for image/audio/video — a media reader is needed (not yet
here, a candidate). They plug into the core's content axis and are replaceable. Without them the core
still gives "touched/not" and "whose link" — the reader adds "where inside."

**DOORS (integrations, the buyer's).** How the core embeds into a channel: a mail
plugin, a bot, a 1C/CRM/EDI module. The BUYER writes it for their process, not us.

## Governing rule (AD-83)

- **LAYER (core):** a new way of SEALING through semantic
  tracing itself (link, void, progression, field keeper) — we build it ourselves.
- **PLUMBING:** pulling in others' known identification/security measures
  (DKIM, Received, TLS, PSL, others' maps) — not the core.

## What has been proven live

- The core localizes WHOSE link broke (trace) — channel-independent.
- record: fields with keepers, legitimate progression, a footnote of who/where/when,
  a forgery localized by field (20 test files green).
- Works on DIFFERENT carriers: text, image (PNG), audio (WAV), data
  (JSON) — with a single machine via the fingerprint (carriers_demo).

## Honest boundaries

- The core makes substitution VISIBLE, not impossible; it does not prove the truth; it does not
  judge intent.
- "where INSIDE the image/audio" the core does not give — that is the reader's work (raw material).
- The strength of the reconciliation is exactly as strong as the reference is independent AND the consumer
  actually reconciles.
