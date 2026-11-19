#!/usr/bin/env python3
"""Build the three intermediate states the plan's commits need, without touching
the working tree.

Why this exists in place of editing files and staging them: the working tree of
this branch contains somebody else's in-flight work as well as mine. Fourteen of
the tracked files are modified by the Electrical Experimenter work in progress
(the untracked page, assets/ee1919/, js/scripts.js +322/-1, _redirects, llms.txt,
sitemap.xml, _headers) and four of the HTML files carry an uncommitted paragraph
linking to that page. A `git add -u '*.html'` would commit their paragraph into
my item 5 commit, which is the kind of thing a commit split is supposed to prevent
and the kind of thing that is invisible in a `--stat`.

So nothing here edits a file. Each intermediate state is generated from
`git show HEAD:<path>` plus my own transformations, and written somewhere else:

  /tmp/item-state/item5/<page>.html   HEAD + the whitespace repair only
  /tmp/item-state/item6/<page>.html   that, plus the nav rewrite
  /tmp/site-shipped/                  the state the branch tip will describe:
                                      the tree, with every HTML file replaced by
                                      the generated one and the other
                                      owner-modified files restored to HEAD

The assertions are the point:

* the whitespace repair may not change a single (tag, attribute, value) triple,
  nor any non-whitespace byte, nor introduce `=" ` (the shape the bad defect
  definition produced on 53 files - see tests/img-alt/glued.py's docstring);
* the nav rewrite may only change the one <nav> region;
* everything the generated state and the working tree disagree about must be the
  owner's paragraph, and every disagreeing line is printed and must mention
  electrical-experimenter, or the script stops. That is what keeps "I did not
  commit their work" a measured claim rather than an intention.
"""
import difflib
import glob
import os
import re
import subprocess
import sys

SITE = os.environ.get("SITE_OVERRIDE", "/home/matt/projects/other/tesla-generator/website")
STAGING = os.path.join(SITE, "tests", ".staging")   # gitignored; see tests/ship/README.md
OUT = os.path.join(STAGING, "item-state")
SHIPPED = os.path.join(STAGING, "site-shipped")
sys.path.insert(0, os.path.join(SITE, "tests", "img-alt"))
sys.path.insert(0, os.path.join(SITE, "tests", "nav"))
import glued  # noqa: E402
import apply_nav  # noqa: E402

OWNER_MARK = re.compile(r"electrical.experimenter|ee1919|email.capture", re.I)


def sh(*a):
    r = subprocess.run(a, cwd=SITE, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(a)}\n{r.stderr[:400]}")
    return r.stdout


def tracked_pages():
    return [p for p in sh("git", "ls-files", "*.html").split()]


def build():
    os.makedirs(os.path.join(OUT, "item5"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "item6"), exist_ok=True)
    foreign = []
    for path in tracked_pages():
        name = os.path.basename(path)
        base = sh("git", "show", f"HEAD:{path}")
        fixed, n = glued.fix(base)
        # proof 1 (on the whitespace repair alone): non-whitespace bytes identical
        assert "".join(fixed.split()) == "".join(base.split()), f"{name}: non-whitespace changed"
        # proof 2 (also the repair alone): the (tag, attribute, value) triples are
        # identical - the check that caught the bad defect definition
        assert glued.attrs(base) == glued.attrs(fixed), f"{name}: an attribute's meaning changed"
        # The malformed-quote tags are the other half of item 5: same family of
        # defect, and a measured consequence on a social card (see glued.py for why
        # this one is repaired rather than only reported). Escaping is *not*
        # whitespace-only, so it gets its own assertion: unescaping the result must
        # give back the text that went in, which is the only sense in which changing
        # a value can still be a mechanical repair. (It is exact unless a value
        # already contained the literal `&quot;` - the assertion would then hold by
        # over-correcting both sides, and that is the caveat rather than the norm.)
        step1, esc = glued.escape_inner_quotes(fixed)
        assert step1.replace("&quot;", '"') == fixed.replace("&quot;", '"'), \
            f"{name}: the escaping did not round-trip"
        # proof 3: the shape the bad defect definition produced must not appear
        # anywhere in the output (HEAD has zero occurrences of either, measured)
        for bad in ('=" ', "=' "):
            assert base.count(bad) == step1.count(bad) == 0, f"{name}: {bad!r} present"
        # item 6: replace the one nav region
        m = apply_nav.NAV.search(step1)
        if m:
            active = tuple(mt.group(1) for mt in
                           re.finditer(r'class="nav-link[^"]*\bactive\b[^"]*"\s+href="([^"]+)"',
                                       m.group(0)))
            step2 = step1[:m.start()] + apply_nav.nav_block(active) + step1[m.end():]
        else:
            step2 = step1
        assert glued.count(step1) == 0, f"{name}: missing separators left after the repair"
        assert glued.quote_defects(step1) == [], f"{name}: malformed quotes left in {name}"
        assert glued.attrs(step2)
        # the nav rewrite must change nothing outside the nav region
        outside = lambda s: apply_nav.NAV.sub("<nav/>", s)
        assert outside(step2) == outside(step1), f"{name}: the nav rewrite changed the body"

        open(os.path.join(OUT, "item5", name), "w", encoding="utf-8").write(step1)
        open(os.path.join(OUT, "item6", name), "w", encoding="utf-8").write(step2)

        # what does the working tree have that the generated state does not?
        cur = open(os.path.join(SITE, path), encoding="utf-8", errors="replace").read()
        if cur != step2:
            for line in difflib.unified_diff(step2.splitlines(), cur.splitlines(), n=0, lineterm=""):
                if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                    if not OWNER_MARK.search(line):
                        sys.exit(f"{name}: an unexplained difference from the generated state:\n"
                                 f"  {line[:200]}\nIt is not the owner's in-flight work and it is not "
                                 "something this script generated - reconcile before committing.")
                    foreign.append((name, line[:80]))
    kinds = {}
    for name, _ in foreign:
        kinds[name] = kinds.get(name, 0) + 1
    print(f"generated {len(tracked_pages())} pages; the only differences from the working tree are "
          f"the owner's in-flight lines in {len(kinds)} files: {sorted(kinds.items())}")


def build_shipped():
    """A copy of the tree that is what the branch tip will contain."""
    # Regenerate item 7's cut stylesheet from the same snapshot this tree is built from,
    # every time. gate.py's BEFORE cells are served css-item7.css and
    # css-comment-only.py calls it item 7's state, so a css-item7.css cut from an old
    # snapshot measures a stylesheet nobody is shipping - and does it with a green
    # verdict. See split.py's step_css7 for the incident that put this line here.
    import split  # noqa: E402  (tests/ship/split.py, same directory as this file)
    f, i7 = split.step_css7()
    print(f"  item 7's CSS regenerated: {f} -> {i7} chars ({f - i7} navbar CSS)")
    subprocess.run(["rm", "-rf", SHIPPED], check=True)
    os.makedirs(SHIPPED, exist_ok=True)
    # The measured copy now lives *inside* the site (a reboot took the /tmp version
    # of this tree, and with it the only copy of what the numbers were measured
    # against), so a plain `cp -a SITE SHIPPED` is a copy of a directory into
    # itself. Stream it instead, skipping the staging tree — copying last night's
    # measured copy into tonight's is how a stale page ends up inside the one
    # artefact that is supposed to prove the pages are current — and skipping .git,
    # which the measured copy never needed.
    r = subprocess.run(
        f'tar -C "{SITE}" --exclude=./tests/.staging --exclude=./.git -cf - . '
        f'| tar -C "{SHIPPED}" -xf -', shell=True)
    if r.returncode != 0:
        sys.exit("streaming the tree into the measured copy failed")
    subprocess.run(["rm", "-rf", os.path.join(SHIPPED, ".git")], check=True)
    for name in os.listdir(os.path.join(OUT, "item6")):
        src = os.path.join(OUT, "item6", name)
        dst = os.path.join(SHIPPED, name)
        if os.path.exists(dst):
            with open(src, encoding="utf-8") as f:
                text = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write(text)
    # The owner's other work-in-progress: restored to HEAD so the measured site is
    # the committed site and not a mixture of both.
    for path in [p for p in sh("git", "diff", "--name-only", "HEAD").split()
                 if not p.endswith(".html") and p != "css/styles-custom.css"]:
        dst = os.path.join(SHIPPED, path)
        if os.path.exists(dst):
            with open(dst, "w", encoding="utf-8") as f:
                f.write(sh("git", "show", f"HEAD:{path}"))
            print(f"  restored to HEAD in the measured copy: {path}")
    # the untracked page and its assets are not in the committed tree either
    for extra in ("electrical-experimenter.html", "js/email-capture-widget.html",
                  "assets/ee1919", "assets/og/electrical-experimenter.webp", ".pi"):
        p = os.path.join(SHIPPED, extra)
        if os.path.exists(p):
            subprocess.run(["rm", "-rf", p], check=True)
    n = len(glob.glob(os.path.join(SHIPPED, "*.html")))
    print(f"measured copy at {SHIPPED}: {n} pages (the committed tree has {len(tracked_pages())})")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "build"
    if what == "build":
        build()
    elif what == "shipped":
        build()
        build_shipped()
    else:
        sys.exit("usage: stage.py build | shipped")
