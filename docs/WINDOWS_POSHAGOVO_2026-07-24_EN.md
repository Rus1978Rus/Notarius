# Windows: how to run it, step by step (to start — the self-test)

Nothing to figure out on your own. Do it in order. It'll take ~10 minutes.

---

## Step 1. Install Python (once)

1. Open in your browser: **https://www.python.org/downloads/**
2. Click the big **"Download Python"** button (version 3.x).
3. Run the downloaded file.
4. **IMPORTANT:** at the bottom of the first window, check the box
   **"Add python.exe to PATH"**, then click **"Install Now"**.
5. Wait for the "Setup was successful" message and close the window.

---

## Step 2. Download the program

1. Open the link (a .zip archive will download):
   **https://github.com/Rus1978Rus/desktop-tutorial/archive/refs/heads/claude/semantic-invisible-length-witness-4dezte.zip**
2. Find the file in your "Downloads" folder.
3. Right-click it → **"Extract All…"** → **"Extract"**.
4. A folder will open. Go inside — you should see folders `scripts`,
   `docs`, `notarius` and others. This is the folder you need.

---

## Step 3. Open this folder in the command line

1. You're in the folder from step 2 (where you can see `scripts`, `docs`, `notarius`).
2. Click in the **address bar** at the top of Explorer (where the folder path is).
3. Type the three letters **`cmd`** and press **Enter**.
4. A black window will open — already in the right folder.

---

## Step 4. Run the self-test

In the black window, type the command and press **Enter**:

```
python scripts\notarius_mail.py selftest
```

*(If it says "python is not recognized… as a command" — try `py` instead of
`python`: `py scripts\notarius_mail.py selftest`.)*

---

## What you should see

The program will play out the sender, the mail, and the receiver on its own. At the end —
roughly this:

```
✘ BREAK — changed lines: 1
  line 3: VALUE_SUBSTITUTION
      was:  amount due: 1000000 USD
      now:  amount due: 9000000 USD
```

That means: the amount substitution in the "letter" was caught and it showed exactly where.
**Everything works.**

---

## Next — two real mailboxes

Once the self-test passes — we move on to two real mailboxes
(instructions: `docs/POCHTA_INSTRUKCIYA_2026-07-24_EN.md`). The commands there
are longer; if they look complicated — just ask, and I'll make a simple settings
file so you don't have to type the long lines.
