# How to run it on two real email accounts

Step by step, in plain words. The tool: `scripts/notarius_mail.py` (standard
Python, nothing to install except our package).

---

## First — a check with no network and no passwords

You can confirm everything works with a single command (no mail needed — a shared
folder stands in for it):

```
python3 scripts/notarius_mail.py selftest
```

The sender prints an invoice → the "mailman" edits the amount in the attachment →
the recipient reconciles → **BREAK, line 3, 1000000→9000000**. If you see this,
the logic works, and you can move on to real mail.

---

## Now — two real accounts on one machine

**What you'll need:** two mailboxes (for example, two Gmail accounts — alpha and
beta) and an **app password** for each (not the main password!). In Gmail: Account
→ Security → App passwords.

**The shared registry "under glass"** — one folder visible to both sides. On one
machine this is just a shared folder, for example `~/reestr`. (Between different
machines — a shared cloud folder / network drive.)

### Step 1. The sender (alpha) prints and sends

```
NOTARIUS_REGISTRY=~/reestr \
NOTARIUS_USER=alpha@gmail.com \
NOTARIUS_PASS=alpha-app-password \
NOTARIUS_SMTP=smtp.gmail.com:587 \
python3 scripts/notarius_mail.py send schet.txt --to beta@gmail.com
```

The reference landed in `~/reestr` (by a different road), the letter went to beta.

### Step 2. Play the interceptor (otherwise there's nothing to catch)

Real mail doesn't corrupt the attachment. To see the catch — imagine the
interception: open the received letter and **save the attachment, edit the amount
in it** by hand (or swap the file before reconciliation). This imitates "reworked
along the way."

### Step 3. The recipient (beta) fetches and reconciles

```
NOTARIUS_REGISTRY=~/reestr \
NOTARIUS_USER=beta@gmail.com \
NOTARIUS_PASS=beta-app-password \
NOTARIUS_IMAP=imap.gmail.com:993 \
python3 scripts/notarius_mail.py recv --save-dir ~/vhodyashchie
```

The program pulls the attachment from the inbox, finds the reference in the
registry, and shows: **where and what was swapped** — or "untouched," if delivery
was honest.

---

## Three honest subtleties

1. **We play the interceptor ourselves.** Mail doesn't change the attachment on
   its own — the substitution has to be staged, otherwise the chain honestly says
   "untouched."
2. **No reference in the registry → nothing to reconcile against.** If the sender
   did NOT print the document (step 1), the recipient will see "no reference." This
   is not a failure — it's the law: without a mark at the source there's nothing to
   catch with.
3. **The registry is by a DIFFERENT road, not in the letter.** The fingerprint is
   placed in a shared folder that the mail interceptor can't reach. That's the
   whole defense.

---

_The folders and environment variables here are a thin adapter. The logic (print
→ delivery → reconcile) is already proven by the selftest and the demo
two_accounts_demo.py._
