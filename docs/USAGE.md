# How to use NOTARIUS

A short, practical guide. NOTARIUS runs on your own machine and shows **where**
and **what** changed between your original and a received copy — a swapped
number, a hidden invisible character, a look-alike domain, changed whitespace.
It locates the lie; it does not judge intent.

---

## 1. Start it

- **Easiest:** double-click **`start.bat`** (Windows) or **`start.sh`** (macOS/Linux).
- **Or by command** (from inside the project folder):
  - Windows: `py -m notarius web`
  - macOS/Linux: `python3 -m notarius web`

A browser opens at `http://127.0.0.1:8788`. Everything is local — nothing leaves
your machine. To stop, close the console window (or press `Ctrl+C`).

> First run on Windows may show *“Windows protected your PC”* (the launcher is
> not code-signed). Click **More info → Run anyway**. If a firewall prompt
> appears, you can **decline** — the app only talks to your own computer.

---

## 2. The two tabs

### Compare two documents  *(the main mode)*
Put the **same document** in both boxes: your trusted **original** on the left,
the **received copy** on the right. Press **Check**. NOTARIUS lists every line
that differs, with what changed.

- Quick start: press **“Load a demo example”**.
- Ready test files: [`examples/`](../examples/) — `reference.txt` and
  `received_tampered.txt` look identical but the second hides invisible
  characters. Load one on each side and press Check.

> Tip: comparing two **different** documents (e.g. an invoice vs some code) is
> meaningless — everything differs. Compare two versions of the *same* document.
> And after you change a box, press **Check** again.

### Scan one document
Paste or load a **single** document to check it on its own for invisible
characters and look-alike domains. Useful when you have no original to compare
against.

> Note: a legitimately **bilingual** document (e.g. Russian text with Latin
> terms) may raise a mixed-script flag here — that is expected, not an attack.
> Compare mode does **not** have this issue: it only flags manipulation that was
> *introduced* between the original and the received copy.

---

## 3. Reading the results

Each changed line shows a **line number**, a **category**, a **review level**
(high / medium / low) and a `was → now` diff.

| Category | Meaning | Level |
|---|---|---|
| `VALUE_SUBSTITUTION` | a number changed (e.g. 1000 → 9000) | high |
| `INVISIBLE_INSERTION` | a hidden zero-width character was inserted | high |
| `HOMOGLYPH_SUBSTITUTION` | a letter swapped for a look-alike from another script | high |
| `WHITESPACE_CHANGED` | only spaces/tabs/indentation differ (text is the same) | low |
| `NORMALIZATION_EQUIVALENT` | bytes differ but are Unicode-equivalent | low |
| `CHAR_LOSS` | characters were lost (e.g. bad transcoding) | medium |
| `CONTENT_CHANGED` | changed, not one of the specific cases above | medium |

A red banner may also report **hidden manipulation introduced** (invisible
characters) or a **suspicious domain** (a look-alike host).

**The boundary (honest):** NOTARIUS shows *where* the difference is and flags
hidden manipulation. It does **not** prove intent — an honest mistake vs.
deliberate fraud is a human judgment.

---

## 4. Command line (optional)

```
py -m notarius check REFERENCE RECEIVED   # where and what was swapped
py -m notarius seal  FILE                 # take a signed receipt-fingerprint (.ntr)
py -m notarius verify FILE                # is it the same, or was it touched
```
(`seal`/`verify` use signatures and need PyNaCl: `py -m pip install pynacl`.
`check` and the web app work with plain Python.)

---

## 5. Keeping it up to date

Double-click **`update.bat`** (Windows) / run `update.sh` (macOS/Linux) — it
downloads the latest version over your folder. Stop the app first (`Ctrl+C`).

---

## Troubleshooting

- **Typing `python` opens the Microsoft Store** → use **`py`** instead.
- **“No module named notarius”** → run the command from **inside** the project
  folder (the one that contains the `notarius` subfolder), or just use `start.bat`.
- **This is the right project:** `github.com/Rus1978Rus/Notarius`. (The older
  `desktop-tutorial` repository is not this program.)
- **Invisible-character test files must be *saved*, not copy-pasted** — copying
  text with the mouse drops the invisible characters.
