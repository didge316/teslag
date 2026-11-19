#!/usr/bin/env python3
"""Image alt inventory - the keeper check for item 5.

Item 5 came into this repo as "191 malformed alt attributes, screen readers get
nothing". That was asserted and it is false (PLAN §2): the HTML parser recovers
from a missing space after a quoted attribute value, so all 721 <img> tags on
the site hand over their alt text. What is actually true, and what this script
counts, is:

  * alt present on N of M images  - must stay 100% or the commit is wrong;
  * images marked decorative with alt="" - 0 today, and that is the real
    accessibility gap: a decorative thumbnail read out loud is the defect, and
    no script can decide which images are decorative;
  * alt text that is a filename or boilerplate - a cheap proxy for "this was
    written by a template, not by someone looking at the picture";
  * <img> tags with no space before width= - invalid HTML by the validator,
    tolerated by browsers, and a trap for any future XML/XML-parsing toolchain
    or minifier. Cosmetic. Do NOT describe fixing it as an accessibility fix.

The one number this script exists to protect is "missing alt": the space fix must
not change it, and it must not become nonzero because a sed went one character
too far.

Usage: python3 inventory.py [--top N]
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glued as gluedmod  # noqa: E402  (same directory: the ONE shared defect
# definition. Aliased: `glued` is also the name of the per-tag counter further
# down, and shadowing the module with an int is only discovered at runtime.)

SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
IMG = re.compile(r"<img\b[^>]*>", re.I)
BOILER = re.compile(r"^(avatar of )?[\w -]{0,40}$", re.I)


def main():
    global SITE
    top = 6
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])
    # `--site PATH` measures some other checkout with the same code. It exists so
    # the before/after pair the commit quotes comes from one instrument rather
    # than from a number typed into a message: the "before" file in this directory
    # is this same script run against a clean checkout of ad559e9, which is the
    # only honest way to say "254 glued attributes" and "0 glued attributes" in the
    # same breath.
    if "--site" in sys.argv:
        SITE = os.path.abspath(sys.argv[sys.argv.index("--site") + 1])
    if not os.path.exists(os.path.join(SITE, "index.html")):
        sys.exit(f"cannot find site root (tried {SITE})")
    print(f"measuring: {SITE}")
    total = missing = empty = glued = 0
    per_file = collections.Counter()
    alts = collections.Counter()
    avatar = 0
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        html = open(f, encoding="utf-8", errors="replace").read()
        for t in IMG.findall(html):
            total += 1
            m = re.search(r'\balt\s*=\s*"([^"]*)"', t, re.I) or re.search(r"\balt\s*=\s*'([^']*)'", t, re.I)
            if not m:
                missing += 1
                per_file[os.path.basename(f)] += 1
                continue
            value = m.group(1).strip()
            alts[value.lower()] += 1
            if not value:
                empty += 1
            if value.lower().startswith("avatar of "):
                avatar += 1
            if re.search(r'alt="[^"]*"\w+=', t):
                glued += 1

    print(f"<img> tags                : {total}")
    print(f"missing alt attribute     : {missing}    <-- this must be 0, before and after")
    print(f'alt="" (marked decorative): {empty}    <-- the real a11y gap: nothing is marked decorative')
    print(f"glued width= (no space)   : {glued}    <-- source hygiene only, invisible to visitors")
    print(f'"Avatar of X" descriptions : {avatar}')
    # The class, not the instance: the ticket that started this named
    # `alt="..."width=`, but a fix aimed at one attribute pair is a fix aimed at
    # one report. What is actually invalid is any quoted attribute value whose
    # closing quote is followed by a non-whitespace character that is not the end
    # of the tag or its self-closing slash - which is how `alt="x"width="y"`,
    # `src="a.jpg"height="10"` and `alt='x'data-n=2` are all the same mistake.
    # Checked across every start tag on the site, not just <img>, and reported as
    # a hard failure so the pattern cannot come back on another template.
    # One shared definition of the defect class (see glued.py) - asserted across
    # every start tag on the site, not just <img>, so the ticket cannot come back
    # for a different attribute pair.
    glued_all = 0
    quote_all = 0
    # The neighbours of the class, counted on the same pass. Item 5's whole argument
    # is that the *scope* of a check decides what it can find - a check aimed at
    # `alt"..."width=` could not see `style"..."alt=` - so the keeper also counts the
    # other ways a start tag goes wrong that the ticket never mentioned. All three
    # measure 0 on this site, before and after, which is a finding and not an
    # assumption: they are counted, not assumed absent. (`unclosed_quotes` was tried
    # too and deleted: it could not fail. See glued.py.)
    dup_attr = dup_id = 0
    ents = []
    for f in glob.glob(os.path.join(SITE, "*.html")):
        text = open(f, encoding="utf-8", errors="replace").read()
        glued_all += gluedmod.count(text)
        quote_all += len(gluedmod.quote_defects(text))
        dup_attr += len(gluedmod.duplicate_attrs(text))
        dup_id += len(gluedmod.duplicate_ids(text))
        ents += gluedmod.unknown_entities(text)
    glued_samples = []
    print(f"glued attributes, all tags : {glued_all}    <-- the class, site-wide")
    print(f'malformed quotes in tags   : {quote_all}    <-- truncates og:title: visitors see it')
    print(f"duplicate attributes       : {dup_attr}    <-- the parser keeps the first and discards the rest")
    print(f"duplicate ids in a page    : {dup_id}    <-- label for= / aria-labelledby resolve to the first")
    print(f"unknown or loose entities  : {len(ents)}"
          + (f"    <-- text the author did not write: {', '.join(sorted(set(ents))[:6])}" if ents else
             "    <-- counted, not assumed absent"))
    for f, tag, ctx in glued_samples:
        print(f"      {f} <{tag}> ...{ctx}...")
    if per_file:
        print("missing alt by file:", dict(per_file))
    print(f"\ndistinct alt strings: {len(alts)}; most repeated:")
    for value, n in alts.most_common(top):
        print(f"   {n:4}  {value[:70]!r}")
    dupes = sum(n for v, n in alts.items() if n > 1)
    print(f"images whose alt string is used more than once on the site: {dupes} of {total}")
    if missing:
        sys.exit(1)
    if dup_attr or dup_id or ents:
        # Only ever printed when something fired, which is the whole point: these
        # three are counted so that "the site is clean" is a measurement rather than
        # an impression, and when it is not clean this says what is wrong with it.
        print("\nNeighbour classes of the glued-attribute defect, in one sentence each:")
        print("  a duplicate attribute - the parser keeps the first and throws the rest away,")
        print("    so a duplicate href/alt/class is content that silently does not exist;")
        print("  a duplicate id - #anchor, label for= and aria-labelledby resolve to the")
        print("    first match, so the second element can be labelled by the wrong control;")
        print("  an unknown or unterminated entity - printed literally, which is text the")
        print("    author did not write and no test of the rendered page will catch.")
        sys.exit(1)
    if glued_all or quote_all:
        if quote_all:
            print("\nA quoted value containing an unescaped " + '"' + " ends where the browser thinks it")
            print("ends, and the rest of the tag becomes guesswork. Measured, not theoretical: on")
            print("tesla-high-frequency-massage.html og:title and twitter:title both came through as")
            print("'Tesla\'s High-Frequency ' - every social card for that article was truncated")
            print("mid-phrase - while the <title> element was fine, because element text is not an")
            print("attribute. glued.py reports these and does not repair them: an escaping tool")
            print("working on a tag it cannot parse is inventing content.")
        sys.exit(1)


if __name__ == "__main__":
    main()
