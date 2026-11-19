#!/usr/bin/env python3
"""Stage the three commits the plan asks for out of one working tree.

The tree already holds all three items, and two of them (the nav rewrite and the
whitespace fix) touch the same 48 files, so the split cannot be done by `git add`
on whole files. It is done by rebuilding each intermediate state deterministically
and checking the last one is byte-identical to what was measured:

  A  css/styles-custom.css with the two navbar blocks cut  ->  item 7
  B  every *.html with its nav region put back the way it was at ad559e9
     (space fix kept, nav rewrite undone)                    ->  item 5
  C  apply_nav.py re-applied + the css restored             ->  item 6, tip == measured

Nothing here guesses at the old nav: it is read out of the detached worktree at
/tmp/nav-before, which is a checkout of the same commit the branch started from.
If a page's nav does not match what apply_nav.py would write in step C, the script
says so instead of producing a commit that does not rebuild the measured tree.
"""
import glob
import os
import re
import shutil
import subprocess
import sys

SITE = os.environ.get("SITE_OVERRIDE", "/home/matt/projects/other/tesla-generator/website")
# Nothing here writes to /tmp any more: a scratch tree in /tmp was where this file
# lived until a reboot deleted it (see tests/ship/README.md). Generated states are
# throwaway, but they are throwaway *inside the repo*, next to the checks that read them.
STAGING = os.path.join(SITE, "tests", ".staging")
os.makedirs(STAGING, exist_ok=True)
OLD = os.path.join(STAGING, "nav-before")
CSS = os.path.join(SITE, "css", "styles-custom.css")
CSS_FINAL = os.path.join(STAGING, "css-final.css")
NAV = re.compile(r"<nav[^>]*navbar-expand[^>]*>.*?</nav>", re.S)
NAV_BLOCKS = [                                    # the two navbar rule blocks in item 7's tail
    ("/* Below the lg breakpoint the whole menu lives in the toggler's drawer",
     "/* ...and the same menu at the other side of the breakpoint"),
    # This second one does NOT run to end of file, and it used to, which is a bug
    # of the quietest kind: item 7's own `.btn` cap - the rule that closes the
    # last red cell on /contact at 320px / 300% - sits AFTER the desktop navbar
    # block, so cutting "to EOF" would have shipped item 7's commit without item
    # 7's button rule. The gate cannot catch it either, because the gate's
    # before-flavour is supposed to cut all of item 7 and so does run to EOF: the
    # two cuts look identical and mean opposite things. The end marker below is
    # the comment that begins the button block, and the balance and lost-rule
    # checks in step_a_css are what turn "I hoped these markers were block
    # boundaries" into a measured fact.
    ("/* ...and the same menu at the other side of the breakpoint",
     "/* Bootstrap 5.2 sets .btn sizes through these custom properties"),
]


def sh(*a, **kw):
    print("$", *a)
    r = subprocess.run(a, cwd=SITE, **kw)
    if r.returncode != 0:
        sys.exit(f"failed: {a}")


def _cut_nav_css(text, final):
    """The stylesheet text minus item 7's two navbar rule blocks, with the checks.

    The assertions are the interesting part of a split like this, and they are only
    worth anything if they can be run before the tree is committed, which is why the
    cut lives here and both callers (the tree-writing mode and the CSS7-only mode)
    go through it.
    """
    for start, end in NAV_BLOCKS:
        i = text.find(start)
        assert i > 0, f"nav CSS marker gone: {start[:40]!r}"
        assert end is not None, f"refusing to cut a CSS block to end of file: {start[:40]!r}"
        j = text.find(end, i)
        assert j > i, f"nav CSS end marker gone: {end[:40]!r}"
        text = text[:i] + text[j:]
    assert "navbar-nav" not in text, "navbar CSS still present after cutting"
    # A cut that lands inside a block leaves broken CSS, and broken CSS fails in
    # the browser silently rather than here loudly, so the cut is only accepted if
    # it balances and if everything that is not the navbar's survived it.
    bal = text.count("{") - text.count("}")
    assert bal == 0, f"cut leaves {bal:+d} unbalanced braces - a marker is inside a block"
    lost = [k for k in (".btn.btn-lg", "--bs-btn", "min(1rem, 16px)", ".v1-status-bar",
                        "overflow-wrap") if k in final and k not in text]
    assert not lost, f"the cut removed item 7's own rules, not just the navbar's: {lost}"
    return text


def step_css7():
    """Rewrite tests/.staging/css-item7.css from the snapshot, touching nothing else.

    `a-css --write-tree` produces CSS7 too, but only as a side effect of rewriting the
    working stylesheet, and nothing outside a scratch clone should do that. Without a
    mode of its own, CSS7 rots: found on 2026-11-19, when the EmailOctopus submit fix
    went into the stylesheet and css-item7.css still described the pre-fix file - and
    CSS7 is what every BEFORE-flavour cell is served and what the payload comparison
    in css-comment-only.py calls item 7's state. A stale CSS7 does not fail loudly; it

    quietly measures a stylesheet nobody is shipping. stage.py now calls this on every
    build for that reason.
    """
    dst = os.path.join(STAGING, "css-item7.css")
    final = open(CSS_FINAL, encoding="utf-8").read()
    work = open(CSS, encoding="utf-8").read()
    assert work == final, ("the working stylesheet is not the snapshot: the measured tree ships "
                           "the working file, so a CSS7 cut from the snapshot describes something "
                           "nobody ships. If the snapshot is what you mean, cp the file deliberately.")
    text = _cut_nav_css(final, final)
    open(dst, "w", encoding="utf-8").write(text)
    return len(final), len(text)


def step_a_css(dry=False):
    """item 7's commit gets the stylesheet without the navbar rules.

    `SPLIT_DRY_OUT=path` runs the whole cut - markers, brace balance, lost-rule
    check - and writes the result somewhere else instead of overwriting the tree.
    The assertions are the interesting part of a split like this, and they are only
    worth anything if they can be run before the tree is committed.
    """
    if dry:
        # Used to be os.environ["SPLIT_DRY_OUT"], which turned a rehearsal into a
        # KeyError traceback. The default destination is inside the staging tree, so a
        # dry run can never touch css/styles-custom.css by accident.
        dst = os.environ.get("SPLIT_DRY_OUT", os.path.join(STAGING, "a-css-dry-out.css"))
        if not os.path.exists(CSS_FINAL):
            shutil.copy(CSS, CSS_FINAL)
    elif not os.path.exists(CSS_FINAL):
        shutil.copy(CSS, CSS_FINAL)
    text = open(CSS, encoding="utf-8").read()
    assert text == open(CSS_FINAL).read(), "css changed since the snapshot; re-snapshot deliberately"
    text = _cut_nav_css(text, open(CSS_FINAL, encoding="utf-8").read())
    open(dst if dry else CSS, "w", encoding="utf-8").write(text)
    return len(text)


def step_b_html():
    """item 5's commit gets every page with its old nav back."""
    n = 0
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        name = os.path.basename(f)
        cur = open(f, encoding="utf-8").read()
        oldf = os.path.join(OLD, name)
        if not os.path.exists(oldf):
            print(f"  (new page, no old nav to restore: {name})")
            continue
        old = open(oldf, encoding="utf-8", errors="replace").read()
        mc, mo = NAV.search(cur), NAV.search(old)
        assert mc and mo, f"nav not found in {name}"
        if mc.group(0) == mo.group(0):
            continue                      # already the old nav (404 and friends)
        if not os.access(f, os.W_OK):
            sys.exit(f"{name} is not writable (mode {oct(os.stat(f).st_mode)}); refusing to skip it")
        open(f, "w", encoding="utf-8").write(cur[:mc.start()] + mo.group(0) + cur[mc.end():])
        n += 1
    return n


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    # Three of the four modes rewrite the working tree (a cut stylesheet, 52 pages'
    # nav regions, or the CSS restored). That is what a rehearsal in a scratch clone
    # wants and what the real tree must never get by accident: commit-index.py builds
    # every commit out of `git show HEAD:<path>` and blobs, and only ever calls
    # step_a_css(dry=True). So the writing modes now say so out loud.
    if what in ("a-css", "b-html", "c-restore") and "--dry" not in sys.argv \
            and "--write-tree" not in sys.argv:
        sys.exit(f"{what} writes the working tree. Run it in a scratch clone (SITE_OVERRIDE), "
                 "or pass --write-tree if you meant it here. commit-index.py needs neither: "
                 "it consumes step_a_css(dry=True) output.")
    if what == "a-css":
        print(f"nav CSS removed for the item-7 commit: {step_a_css(dry="--dry" in sys.argv)} chars vs "
              f"{len(open(CSS_FINAL).read())} final")
    elif what == "b-html":
        print(f"old nav restored in {step_b_html()} pages")
    elif what == "c-restore":
        shutil.copy(CSS_FINAL, CSS)
        print("css restored to the measured final version")
    elif what == "css7":
        # The only mode here that writes a generated state and no part of the tree.
        f, i7 = step_css7()
        print(f"css-item7.css regenerated from css-final.css: {f} -> {i7} "
              f"({f - i7} chars of navbar CSS cut)")
    elif what == "check":
        # after apply_nav.py: every nav must equal the one the measured tree had
        want = {}
        for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
            m = NAV.search(open(f, encoding="utf-8", errors="replace").read())
            want[os.path.basename(f)] = re.sub(r"\s+", " ", m.group(0)).strip() if m else None
        bad = [k for k, v in want.items() if v is None]
        print(f"pages: {len(want)}, nav missing: {bad or 'none'}")
        print(f"distinct navs now: {len(set(want.values()))}")
    else:
        sys.exit("usage: split.py a-css | b-html | c-restore | css7 | check")


if __name__ == "__main__":
    main()
