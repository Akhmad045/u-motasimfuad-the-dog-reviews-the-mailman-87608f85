#!/usr/bin/env python3
"""The Dog Reviews the Mailman — make.fun one-liner sprint entry.

Writes one funny one-line review a dog gives the mailman to
/output/entry.txt (the competition gate: UTF-8 text, 1-200 characters,
not only whitespace, a single line).

The pick: a dog's formal grievance against the mailman — he knocks once,
shoves paper through the slot and runs, and the dog has filed 412
complaints, all of them barking. Dog voice (slot, barking, guarding the
door), the mailman's visit (knock, slot, flee), and the turn at the end
(the complaints were barking) earn the laugh from this dog and this
mailman, not from a pun that would fit any stranger at the door.
"""

import argparse
import hashlib
import os
import sys

PICK = (
    "He knocks once, shoves paper through my slot, and runs. "
    "I have filed 412 complaints. All of them were barking."
)

# The 12 lines drafted for this bounty; the pick won the internal pairwise
# comparison against the judge brief (dog voice first, then the mailman's
# visit, then the punchline, then a turn that only this dog and this
# mailman could earn). Kept here so the choice is auditable, not hidden.
CONTENDERS = [
    "He knocks once, shoves paper through my slot, and runs. I have filed 412 complaints. All of them were barking.",
    "I gave him five stars once. Then he delivered a parcel to the cat. The cat. Never again.",
    "One star. He comes every day, never rings twice, and still acts surprised when I answer the door with my whole chest.",
    "Two stars. Great uniform, terrible manners — he puts his hand through my slot every day and expects me not to notice.",
    "He delivers to everyone on the street except me. I have no mail, no parcels, and a grudge the size of the garden.",
    "One star. He teases me with the gate, delivers nothing for me, and leaves smelling of every dog on the street.",
    "He rings the bell, I sprint, he leaves. Every day. I have started reviewing him the way he reviews my barking: harshly.",
    "Five stars: he brings the postman smell, the parcel rustle, and leaves before I can ask about the treats in his bag.",
    "One star. The mailman brings letters for the humans and nothing for the dog who guards the door. Unacceptable. I barked.",
    "He walks up like he owns the path, drops paper in my slot, and flees. I give the visit five stars. The fleeing, one.",
    "Review of the mailman: punctual, polite, and cowardly. He has never once stayed to discuss the parcel. I remain furious and loyal.",
    "He knocked, I barked, he left. I have kept his score at one star for six years. He has never once asked why.",
]

OUTPUT_PATH = "/output/entry.txt"


def write_entry(path=OUTPUT_PATH):
    """Write the pick to the gate path and verify it back byte for byte."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = PICK.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        back = handle.read()
    if back != data:
        raise SystemExit("round-trip mismatch: written bytes differ from pick")
    return data


def self_test():
    """Check the pick against the gate and the judging brief."""
    data = PICK.encode("utf-8")
    text = PICK
    errors = []
    if not (1 <= len(text) <= 200):
        errors.append(f"gate: {len(text)} chars, must be 1-200")
    if text.strip() != text:
        errors.append("gate: leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        errors.append("gate: must be one line")
    if not text.strip():
        errors.append("gate: only whitespace")
    if len(data) != len(text):
        errors.append("pick must be ASCII-only (bytes == chars)")
    if not (62 <= len(data) <= 140):
        errors.append(f"size: {len(data)} bytes, winning band is 62-140")
    if len(set(CONTENDERS)) != len(CONTENDERS):
        errors.append("contenders must be distinct")
    if PICK not in CONTENDERS:
        errors.append("pick must be one of the drafted contenders")
    if not any(ch.isdigit() for ch in text):
        errors.append("pick needs a concrete specific marker (a digit)")
    if "mailman" not in text.lower() and "slot" not in text.lower():
        errors.append("pick must name the mailman's visit")
    if "bark" not in text.lower():
        errors.append("pick must keep the dog's voice (barking)")
    if "  " in text:
        errors.append("pick must have no double spaces")
    crowded = ("good boy", "who's a good", "fetch", "treats, please")
    if any(trope in text.lower() for trope in crowded):
        errors.append("pick uses a crowded field trope")
    # Revision: the turn must sit in the final sentence (the judge weighs
    # the punchline last), and every drafted contender must itself pass
    # the 200-char gate, so a resubmit of any of them stays valid.
    last_sentence = text.rsplit(". ", 1)[-1]
    if "bark" not in last_sentence.lower():
        errors.append("punchline must carry the dog's voice in the last sentence")
    over = [c for c in CONTENDERS if not (1 <= len(c) <= 200)]
    if over:
        errors.append(f"{len(over)} contender(s) break the 200-char gate")
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"self-test OK: {len(text)} chars, {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    print(f"entry: {text}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="check the pick against the gate and brief")
    parser.add_argument("--out", default=OUTPUT_PATH,
                        help="where to write entry.txt")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    data = write_entry(args.out)
    sys.stdout.write(PICK + "\n")
    sys.stdout.write(f"wrote {len(data)} bytes to {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
