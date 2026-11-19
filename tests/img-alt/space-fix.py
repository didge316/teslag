#!/usr/bin/env python3
"""Item 5: put the missing space back before 191 `width=` attributes, and prove
the rewrite changed nothing but whitespace.

PLAN §2 killed the framing this item arrived with. The claim was "191 malformed
alt attributes, screen readers get nothing"; measured, all 721 <img> tags on the
site have an alt attribute and the HTML parser recovers from a missing space
after a quoted attribute value, so what a screen reader announces is identical
before and after. What is true is narrower and worth saying plainly:

    alt="Close-up of a permanent magnet"width="754" height="227"/>

is invalid HTML, browsers tolerate it, and anything that parses this source with
a strict XML toolchain (a minifier, a static generator, an EPUB build) does not.
So this is source hygiene with a future-proofing rationale, and the commit
message must not describe it as an accessibility fix.

The keeper check is the whitespace claim, because the sed is the dangerous part
of a change like this: a pattern one character too greedy swallows a quote or a
word, and every rendering test in the repo would still pass while a caption went
missing. So this script does not just write the files, it proves afterwards that
each file's whitespace-normalised bytes are identical to what it read - which is
the strongest statement available: the change is invisible to the parser by
construction, not by inspection.

Usage:
    python3 space-fix.py --dry-run      # count what would change
    python3 space-fix.py                # write, then prove equivalence
Exit 0 = every file rewritten is whitespace-identical to what it read.
"""
import glob
import os
import re
import sys

SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# One definition of the defect, shared with inventory.py, which asserts the same
# thing. It found 18 with its own hand-written walker while the fixer's regex saw
# 63 - two definitions of a class is how a repair ships believing the class is
# empty - so both of them now import glued.py and there is nothing left to drift.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glued  # noqa: E402  (same directory: count(), fix(), GLUED, TAG)


def main():
    dry = "--dry-run" in sys.argv
    if not os.path.exists(os.path.join(SITE, "index.html")):
        sys.exit(f"cannot find site root (tried {SITE})")
    touched = skipped = total_glued = 0
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        before = open(f, encoding="utf-8").read()
        after, n = glued.fix(before)
        if not n:
            skipped += 1
            continue
        total_glued += n
        # The proof, in two parts, because the first version of this file had one
        # part and it was not enough. (a) The non-whitespace bytes, in order, are
        # unchanged. (b) The parsed (tag, attribute, value) triples are identical.
        #
        # (a) is necessary and, on its own, blind. It reads "a space was inserted",
        # which is what this tool intends and also what a defect does when the space
        # goes *inside* a value: the shared defect definition at the time matched a
        # quoted span that was not a value at all (`" content="`, running from one
        # attribute's closing quote to the next attribute's opening one), so
        # `content="width=device-width..."` became `content=" width=device-width..."`
        # in 53 files and the byte proof passed on every single one of them, because
        # a space inside a value is a whitespace byte.
        #
        # (b) asks the question that matters - did the meaning of any attribute
        # change - and it is the check that found the bug when the run was diffed
        # against HEAD. Both are kept: (a) catches text damage, (b) catches semantic
        # damage, and neither catches the other's failure.
        nospace = lambda s: "".join(s.split())
        if nospace(before) != nospace(after):
            sys.exit(f"REFUSING: {os.path.basename(f)} changed by more than whitespace; "
                     "nothing was written for this file and the run aborted")
        if glued.attrs(before) != glued.attrs(after):
            k = next(i for i, (x, y) in enumerate(zip(glued.attrs(before), glued.attrs(after)))
                     if x != y)
            sys.exit(f"REFUSING: {os.path.basename(f)} changed an attribute's value at triple "
                     f"#{k}: {glued.attrs(before)[k]} -> {glued.attrs(after)[k]}. A repair that "
                     "moves a space inside someone's value is not a whitespace repair.")
        # img count and alt count are the two numbers a reader cares about here
        for pat, label in ((r"<img\b", "<img>"), (r"\balt=", "alt=")):
            a, c = len(re.findall(pat, before, re.I)), len(re.findall(pat, after, re.I))
            if a != c:
                sys.exit(f"REFUSING: {os.path.basename(f)} {label} count {a} -> {c}")
        if not dry:
            open(f, "w", encoding="utf-8").write(after)
        touched += 1
    print(f"fixed {total_glued} glued attributes in {touched} files "
          f"({skipped} files had none)")
    print("proof: every rewritten file has an identical non-whitespace byte sequence AND identical "
          "(tag, attribute, value) triples to what it read, and <img>/alt= counts are unchanged")
    if dry:
        print("DRY RUN, nothing written.")


if __name__ == "__main__":
    main()
