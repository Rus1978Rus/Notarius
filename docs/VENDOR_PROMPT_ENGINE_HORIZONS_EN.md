# Conveyor: engine application horizons (blind prompt to external reviewers)

PURPOSE: send to several independent models/experts (Copilot,
DeepSeek, Qwen, Kimi, Gemini, etc.), collect answers, synthesize.
DISCIPLINE: blind — blocks 1-4 without our conclusions; our candidates are given in
block 5 FOR CRITIQUE ONLY. We ask for specifics and an honest "no," not flattery.

Copy everything below the line as is.

────────────────────────────────────────────────────────────────────────

You are an independent technical and product reviewer. You have no connection to the
authors and no obligation to please them. Your value is sobriety: specific
names of existing solutions, an honest "this already exists," and a well-reasoned "this
won't fly" are worth more than enthusiasm.

## Clarifications (frequent questions — read before starting)

- **Level of detail.** The applications themselves — at the CONCEPTUAL level
  (breadth and surprise are what's needed, not specifications). BUT "prior art" and
  "what similar exists" — with SPECIFIC names (TUF, Sigstore, C2PA, IPFS,
  git, etc.), not "there are solutions." For the top 3 — one line on "where it plugs in";
  full APIs/data formats are not needed.
- **Domain for the "wild cards."** NO preferences — the more cross-disciplinary and
  unexpected, the better (bioinformatics, decentralized social networks, offline
  physical systems, law, games — anything). The only requirement: tie each
  wild idea to one of the four machines, so it is a fantasy built on the engine.
- **External sources.** Answer ONLY from this prompt. Do NOT go into other people's
  repositories/articles for ready conclusions about this engine — we need your
  INDEPENDENT view; the list in block 6 is the complete set of others' hypotheses for critique.

## What is being evaluated (neutral description of the capability)

There is a working engine with the following properties:

1. At the moment a piece of information is created, it takes an IMMUTABLE fingerprint
   (a "seal") bound to the creator's identity and to time.
2. The fingerprint is published to a shared log that is append-only forward,
   where "the first record wins" and backdating is impossible (it cannot be
   rewritten retrospectively).
3. At any later moment the engine reconciles the received version against the reference
   and LOCALIZES the change — not "yes/no touched," but which specific element and
   how it was changed (value substitution / insertion of invisible characters / loss of
   characters / rewritten content).
4. It separately catches hidden text manipulation: invisible codepoints
   (zero-width), bidi tricks, look-alike characters (homoglyphs), tag characters.
5. It emits a human-readable verdict (authentic / disputed / forged) with
   an explanation of "why."
6. In principle it is not tied to text (it works on any element of information;
   today it is implemented for text).
7. It works over any channel: the mark is set at the source, the reconciliation happens at the
   consumer, regardless of the delivery method.

Built-in honest boundaries (take them into account): the engine LOCALIZES a substitution, but does NOT
judge intent; a signature does not prove semantic truth; the strength of the reference
depends on the log being independent AND the consumer actually reconciling; the engine
does not PREVENT substitution, it makes it visible and points to the place.

## The task

Answer blocks 1-5 ON YOUR OWN, before reading block 6 (it shows
others' hypotheses — don't let them influence your independent list).

CROSS-CUTTING REQUEST (in addition to everything listed below): SEPARATELY look for
NON-STANDARD, unexpected applications for everything else — those that don't
fall into any of the named roles and categories. The boldest, wildest,
most improbable ideas are welcome; collect them in a separate list and mark them
"wild card."

**Block 1. Applications.** Come up with applications of this capability — including
non-obvious, non-standard, "embed into X" ones (into pipes, devices, protocols,
chains). For each: (a) who exactly feels the pain; (b) why it hurts
right now; (c) a rough value estimate. Don't limit yourself to 3-4 — give a
broad list.

**Block 2. Prior art.** For each application name the SPECIFIC
existing solutions/standards/products that already do this or come close
(with names). Note where the field is crowded ("red ocean") and where it is genuinely
empty.

**Block 3. Ranking.** Name the 3 STRONGEST applications by the combination of
value × feasibility × difference from what exists — and justify it. Separately
name the "traps": applications that seem attractive but are held by
giants or unrealistic.

**Block 4. Adversarial.** What is the STRONGEST argument that this engine will
fundamentally never become a product? What is its fundamental limitation? Where does
"we localize the substitution" have no value to a paying customer?

**Block 5. NON-identification applications.** So far the engine has been described in
the role of a "witness" (is it authentic, what was substituted). But underneath it lie FOUR
general-purpose machines:
  - **The Differ** — compares two versions and CLASSIFIES the change
    (what exactly changed and of what kind);
  - **The Cleaner** — finds hidden/invisible characters and brings text to
    a single canonical form;
  - **The Fingerprinter** — compresses a piece of information into a compact immutable
    content key;
  - **The Orderer** — a log that is "forward-only, first record wins."

Come up with applications of these four machines that are NOT about authenticity
verification/identification, but about something ELSE (for example: understanding, cleaning,
organization, coordination, transfer — but don't limit yourself to these words).
For each: which machine, what work, who it helps, and what already exists that is
similar (with a name).

**Block 6. Critique of others' hypotheses (read AFTER blocks 1-5).** Below are
directions others have already considered. For each, give an honest
verdict: is it new or does it already exist (with a name)? is the field crowded?
would you bet on it?
  Identification:
  - checking for substitution in documents between parties (invoices/acts/contracts);
  - protecting AI from hidden instructions in input text (prompt injection
    via invisible Unicode characters);
  - an "Integrity-VPN" / transport that stamps the payload so the endpoints
    can prove "what was sent = what arrived";
  - a camera/sensor that signs the reading at the moment of capture (against
    deepfakes and "did that really happen" disputes).
  Non-identification:
  - the differ as a human SUMMARY of edits (understand the changes, not catch a
    substitution);
  - the invisible-character cleaner as text HYGIENE (dedup/search/antispam normalization);
  - the fingerprint as a DEDUPLICATION/content-addressing key (git/IPFS-like);
  - the "first-wins" registry as a LOCK/reservation of a name-resource and ordering
    of events;
  - the mark as a portable layer of METADATA (confidentiality/retention),
    riding with the data over any channel.

## Answer format

Structured, so answers from several reviewers can be merged:
- Block 1 — table: application | who feels the pain | why now | value.
- Block 2 — table: application | existing solutions (names) | empty/occupied.
- Block 3 — top 3 with justification + list of traps.
- Block 4 — 1-3 paragraphs.
- Block 5 — table: application | which machine | work | who it helps | what similar exists.
- Block 6 — one verdict per item (new/prior + bet).
- "Wild cards" — a separate list at the very end (the cross-cutting request above).

Requirements: specific names, not "there are solutions"; distinguish "new" from
"already exists"; a well-reasoned "not viable" is welcome; no flattery.

────────────────────────────────────────────────────────────────────────
