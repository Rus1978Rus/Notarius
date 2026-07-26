# Example test files

A ready-made pair for trying NOTARIUS.

- **`reference.txt`** — the clean original.
- **`received_tampered.txt`** — looks **identical** to the human eye, but two
  **invisible characters** were secretly inserted:
  - line 3: a zero-width space `U+200B` hidden inside the word `payable`
  - line 5: a zero-width no-break space `U+FEFF` hidden inside `billing`

You cannot see the difference by looking — that is the point. NOTARIUS finds it.

## Try it

**Web app:**
1. `py -m notarius web` (Windows) or `python3 -m notarius web` (macOS/Linux)
2. In **Compare two documents**, load `reference.txt` on the left and
   `received_tampered.txt` on the right.
3. Press **Check**. You'll see two `INVISIBLE_INSERTION` findings (line 3 and
   line 5), plus a hidden-manipulation flag.

**Command line:**
```
py -m notarius check examples/reference.txt examples/received_tampered.txt
```

Expected: `line 3 · INVISIBLE_INSERTION (U+200B)` and
`line 5 · INVISIBLE_INSERTION (U+FEFF)`.

You can also try the **Scan one document** tab (or paste just the tampered file)
to catch the hidden characters without needing the original.
