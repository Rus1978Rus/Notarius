# Blind prompt: the search for an "unstealable" (uncopyable) part of a key

DATE: 2026-07-22
PURPOSE: generating non-standard/crazy ideas for a part of a signing key that
methodologically cannot be quietly copied. Blind, without the project/author
name. The answer format is for merging with the internal pipeline.

INSTRUCTION: copy everything between the lines into another AI. Save the answer
to docs/vendor_answers/uncopyable_<vendor>_<date>.md.

---

Answer IN RUSSIAN. You are an inventor at a brainstorm; you do NOT need to be
realistic, what's wanted is non-standard and even crazy ideas. At the end you'll
weed out the weak ones yourself.

THE PROBLEM. A digital signing key is data, and data is copied silently,
remotely, endlessly: stealing a key = making a quiet copy, and the owner never
knows. We need a PART of the key (or a factor of its activation) that
METHODOLOGICALLY cannot be quietly copied.

THE CENTRAL CRITERION (judge each idea by it): an idea is good if it turns theft
from DIGITAL (quiet, endless, remote, imperceptible) into PHYSICAL/VISIBLE
(one-at-a-time, leaves a trace, gets noticed, doesn't scale). The formula:
UNSTEALABLE = UNCOPYABLE.

INSPIRATION. The "Perimeter" / "Dead Hand" system: control is arranged so that
seizing one point (even a central one) does not grant power, because the decision
is distributed and/or conditional and/or fires autonomously. Think about the key
the same way: so that seizing one part / person / device does NOT give the thief a
working key.

Known standard answers (you may lean on them, but don't limit yourself): PUF (a
physically unclonable function), biometrics as an unlock, a hardware
unextractable key, Shamir secret sharing, M-of-N multisignature, a threshold
signature.

THE TASK. Propose 6-8 ideas in three directions (at least 2 per direction):
A) PHYSICS/BIOLOGY — binding to an unclonable substance/organism/quantum state/
   decay/wear;
B) DISTRIBUTION / DEAD HAND — the key is alive only while a distributed
   configuration of people/devices/conditions is alive;
C) MADNESS — anything non-standard: behavior, a group's shared memory, a ritual,
   a self-destroying carrier.

FORMAT for each idea:
1. NAME.
2. MECHANISM: how the key part / activation factor works.
3. WHY UNCOPYABLE: why a quiet copy cannot be made.
4. THEFT BECOMES: what the thief must physically do and how it's noticeable.
5. HONEST BOUNDARY: how it can still be bypassed/broken after all.
6. MADNESS 1-5.

AT THE END:
1. Which idea you'd weed out first and why.
2. One idea you consider genuinely strong (theft definitely becomes physical),
   with a justification.

---

## Where to put the answers

`docs/vendor_answers/uncopyable_<vendor>_<date>.md`. Then — merging with the
internal pipeline (the same central criterion).
