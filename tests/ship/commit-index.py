#!/usr/bin/env python3
"""Make the plan's three commits out of a working tree that also contains somebody
else's work, without touching that work.

The mechanism is the git index, not the filesystem. Each intermediate state was
generated from `git show HEAD:<path>` by /tmp/stage.py, hashed with `git
hash-object -w`, and dropped into the index with `git update-index --cacheinfo`;
`git commit` then commits the index, so the working tree is never rewritten and
the owner's in-flight Electrical Experimenter edits (four HTML files' new paragraph,
js/scripts.js, _headers, _redirects, llms.txt, sitemap.xml, the untracked page and
its assets) stay exactly where they were: uncommitted, in the tree, as they were
found.

That distinction is why this script exists. `git add -u '*.html'` here would have
committed four pages' uncommitted paragraph into what is meant to be a whitespace
repair, and nothing about `git add -u` or `git commit -a` would have said so.

Modes:  dry   print what would be staged, stage nothing
        run   stage and commit, then verify

The verification at the end is the interesting part: a worktree is written from
HEAD and compared file-for-file with /tmp/site-shipped, which is the tree the
definitive gate runs measured against. If those two are identical over the site's
HTML, CSS and JS, then the numbers in the commit messages describe the commit. If
they are not, the run measured something else and that has to be found before
anything is pushed.
"""
import glob
import os
import re
import subprocess
import sys

SITE = os.environ.get("SITE_OVERRIDE", "/home/matt/projects/other/tesla-generator/website")
HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(SITE, "tests", ".staging")
STATE = os.path.join(STAGING, "item-state")
SHIPPED = os.path.join(STAGING, "site-shipped")
VERIFY = os.path.join(STAGING, "verify-head")
MESSAGES = os.path.join(HERE, "messages")
sys.path.insert(0, HERE)
import split as splitmod  # noqa: E402  (the CSS cut, with its own assertions)


def sh(*a, **kw):
    r = subprocess.run(a, cwd=SITE, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(a)}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r.stdout


def stage_blob(path, src):
    """Hash `src` as the content of `path` and put it in the index."""
    blob = sh("git", "hash-object", "-w", "--", src).strip()
    sh("git", "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}")
    return blob


def pages():
    return [os.path.basename(p) for p in sh("git", "ls-files", "*.html").split()]


def preflight():
    """Every artefact must contain the verdict line it is quoted for.

    A run that was interrupted leaves an artefact with no verdict - that happened
    twice on this branch, once because a cleanup `pkill` of mine shot two live
    measurement runs, and both times the numbers were already in my notes. A file
    whose tail is a traceback is not a result, so the verdict is read back out of
    the artefact, here, before anything is committed.
    """
    print("### preflight")
    # `bad` used to be defined *after* the first block that appends to it, so the
    # failure path raised NameError instead of refusing: a check that cannot report
    # its own failure is the same class as the vacuous green engines.py used to print.
    bad = []
    r = subprocess.run(["python3", os.path.join(SITE, "tests", "overflow", "css-comment-only.py")],
                       capture_output=True, text=True)
    print("  css-comment-only: " + (r.stdout.strip().splitlines()[-1][:100] if r.returncode == 0
                                    else "FAILED - the measured payload does not describe the "
                                         "stylesheet on disk, so no gate number in these "
                                         "messages is quotable"))
    if r.returncode != 0:
        bad.append("css-comment-only")
    for name in ("gate-FINAL-chromium", "gate-FINAL-firefox", "gate-FINAL-webkit",
                 "gate-BEFORE-cssregions",
                 # The item-7 message cites this one by name as the before picture for the
                 # EmailOctopus clip, so it gets the same treatment as the other before
                 # half: 479 of 624, red, kept on purpose. A cited artefact nobody checks
                 # is a citation that can rot.
                 "gate-BEFORE-cssfix-webkit-RED"):
        f = os.path.join(SITE, "tests", "overflow", name + ".txt")
        txt = open(f, encoding="utf-8", errors="replace").read()
        # One rule for a single run and for a chunked one: webkit died three times in
        # one 624-cell pass on this box, so it was run as four solo chunks and the
        # artefact is their concatenation. The claim being checked is the same either
        # way - every cell in the matrix is accounted for - so the verdict lines are
        # parsed and summed rather than matched literally.
        #
        # But "accounted for" points the opposite way in the two kinds of artefact, and
        # getting that backwards is not hypothetical: gate-BEFORE-cssregions is the gate
        # run with item 7's two CSS regions cut out, and it is *supposed* to be red -
        # 311 of 624 green, 313 scroll sideways. If it ever came back green, item 7's
        # own numbers would mean nothing, because the instrument would have no dynamic
        # range. Requiring a complete green matrix of it demanded the one result that
        # would prove the measurement worthless, and a later reader would "fix" it by
        # re-running the before half until it agreed with the after half.
        want_green = name.startswith("gate-FINAL")
        hits = [ln for ln in txt.splitlines() if "engine x page x viewport x root-font" in ln]
        pairs = []
        for ln in hits:
            m = re.search(r"(\d+) of (\d+) engine", ln)
            if m:
                pairs.append((int(m.group(1)), int(m.group(2))))
        if not pairs:
            bad.append(name)
            print(f"  {name}: NO VERDICT LINE ({len(txt)} bytes) - that run did not finish")
            continue
        g = sum(a for a, _ in pairs)
        t = sum(b for _, b in pairs)
        tail = " (four solo chunks, summed)" if len(pairs) > 1 else ""
        if t % 624:
            bad.append(name)
            print(f"  {name}: {g} of {t} across {len(pairs)} verdict line(s) - {t} is not a "
                  f"whole number of 624-cell matrices, so some cells were never measured")
        elif want_green and g != t:
            bad.append(name)
            print(f"  {name}: {g} of {t} green across {len(pairs)} verdict line(s) - "
                  f"not a complete green matrix")
        elif not want_green and g >= t:
            bad.append(name)
            print(f"  {name}: {g} of {t} GREEN across {len(pairs)} verdict line(s) - this is "
                  f"the before half. It must be red or the gate cannot tell a fixed page "
                  f"from an unmeasured one, and every number in the after half is hollow.")
        else:
            print(f"  {name}: {g} of {t} green across {len(pairs)} verdict line(s){tail} - "
                  + ("complete and green" if want_green
                     else f"the before half, red by {t - g} cells exactly as it must be"))
    for f, needles, label in (
        (os.path.join(SITE, "tests", "overflow", "inert-100.txt"),
         ("OK: at root font 16px", "FAIL: the item-7 CSS", "INCONCLUSIVE", "INSTRUMENT FAILED"),
         "inert-100"),
        (os.path.join(SITE, "tests", "nav", "verify-final.txt"),
         ("all nav interaction checks green", "FAIL  ", "INSTRUMENT FAILED"), "nav verify"),
    ):
        if not os.path.exists(f):
            bad.append(label)
            print(f"  {label}: missing artefact {f}")
            continue
        txt = open(f, encoding="utf-8", errors="replace").read()
        hit = next((n for n in needles if n in txt), None)
        # "FAIL" in an artefact is not always a failure. inert-at-100.py exits 1 on
        # exactly this result by design - "either scope the rule tighter, or state
        # plainly that it is a visible change at 100% and say which pages move" - and
        # the item-7 message carries that answer (68 identical, 88 moved, 0 not
        # reproducible, all 88 the scarcity widget at 320/390px). Printing the bare
        # verdict line here made a recognised, expected outcome look like the thing it
        # is warning about, which is how an honest artefact gets "fixed" into a lie.
        expected_fail = (hit == "FAIL: the item-7 CSS")
        print(f"  {label}: verdict {hit.strip()[:70] if hit else 'NOT FOUND'}"
              + (" - recognised and expected; the instrument exits 1 by design on this "
                 "result and the message carries the answer" if expected_fail else ""))
        if not hit:
            bad.append(label)
    # Two documents the item-7 message cites by name. They are prose, not measurements, so
    # all this can ask is that they exist and still contain the claim being cited; the
    # numbers themselves are the artefacts' job. A citation into a document that no longer
    # says the thing is the drift these four messages exist to catch.
    for cite, needle in (("tests/overflow/KNOWN-WEBKIT-300.md",
                          # Prose wraps, so this is a contiguous fragment of the claim
                          # rather than the whole sentence; the point is that the document
                          # still reports the post-fix result, not that it breaks lines
                          # where this file's author expected it to.
                          "green in chromium, firefox and webkit"),
                         ("tests/reviews/hermes-item7-round6-reply.txt", None)):
        p = os.path.join(SITE, cite)
        if not os.path.exists(p):
            bad.append(cite)
            print(f"  cited doc missing: {cite}")
            continue
        size = os.path.getsize(p)
        if needle and needle not in open(cite, encoding="utf-8", errors="replace").read():
            bad.append(cite)
            print(f"  cited doc {cite} ({size} bytes) no longer says {needle!r} - the message "
                  f"quotes a claim that is not in the document it points at")
        else:
            print(f"  cited doc: {cite} ({size} bytes)")
    if bad:
        sys.exit(f"PREFLIGHT FAILED: {bad} - nothing staged, nothing committed")
    return True


def run(dry):
    # A rehearsal against a scratch clone skips the preflight: its artefacts are the
    # real ones, and the rehearsal exists to exercise index surgery, not to re-litigate
    # whether the measurements are finished.
    if not os.environ.get("SKIP_PREFLIGHT"):
        preflight()
    else:
        print("### preflight SKIPPED (SKIP_PREFLIGHT=1) - rehearsal mode")
    os.makedirs(STAGING, exist_ok=True)
    css7 = os.path.join(STAGING, "css-item7.css")
    os.environ["SPLIT_DRY_OUT"] = css7
    if os.path.exists(splitmod.CSS_FINAL):
        os.remove(splitmod.CSS_FINAL)        # re-snapshot the CSS as it is now
    cut = splitmod.step_a_css(dry=True)
    print(f"\nitem-7 stylesheet (navbar rules cut, asserted): {cut} chars vs "
          f"{os.path.getsize(splitmod.CSS_FINAL)} final")
    if dry:
        print(f"dry: would stage css/styles-custom.css -> {css7}, "
              f"{len(pages())} pages -> {STATE}/item5 then item6, and tests/")
        return

    commits = []
    # Recorded before the first commit so a scope failure can name the exact command to
    # undo with: after four commits exist this is not a nothing-happened situation, and
    # "just reset" without the sha is how somebody's work gets lost.
    head_before = sh("git", "rev-parse", "HEAD").strip()
    # The owner's in-flight set, spelled exactly. Two assets whose names contain
    # "electrical-experimenter" are NOT in it and never were: assets/electrical-experimenter.pdf
    # and assets/electrical-experimenter-cover.webp have been tracked since 73904ae (the
    # EmailOctopus lead magnet) and are in ad559e9, which is the state this branch started
    # from - checked, not assumed, because the first version of this tuple used the bare
    # substring and a later reader touching the lead-magnet PDF would have been told they
    # were smuggling somebody else's page in. The in-flight ones are the page, its asset
    # directory, and its OG card.
    forbidden = ("electrical-experimenter.html", "assets/ee1919",
                 "assets/og/electrical-experimenter.webp",
                 "js/email-capture-widget.html",
                 "_headers", "_redirects", "llms.txt", "sitemap.xml")

    def verify_commit(label, prefixes, sha=None, bar_expected=False):
        """The contamination invariant, applied to each commit as it lands.

        `sha` defaults to HEAD, which is what the commit sequence wants; VERIFY_ONLY
        passes explicit shas, so the same check can be re-run over commits that already
        exist (see the block right after this function).

        Reviewer's addition in round 7 (tests/reviews/hermes-decisions-round7-reply.txt):
        "assert the contamination invariant per commit, not at HEAD - a last commit that
        removes what an earlier one carried leaves HEAD clean and history dirty." Checking
        only the tip is the same mistake as checking only `git status`: the working tree
        says nothing about what commit 2 contained.

        Checked as an ALLOWLIST of the paths a commit may change, not as a denylist of the
        nine paths we happened to think of - a denylist catches what somebody remembered,
        and there are 52 pages here to forget. The denylist is still reported, because when
        the allowlist trips it is genuinely useful to know whether what tripped it is the
        owner's work. It fails fast: item 6 must not get to land on top of a contaminated
        item 5, which is why this runs per commit and not once at the end.
        """
        sha = sha or sh("git", "rev-parse", "HEAD").strip()
        changed = [n for n in sh("git", "show", "--name-only", "--pretty=format:", sha).split() if n]
        # `git show --name-only` prints a rename as "old => new". No rename is expected in
        # any of these four, so a '>' is itself a finding, not something to parse around.
        surprise = [n for n in changed if ">" in n or not n.startswith(prefixes)]
        hits = [n for n in changed if any(f in n for f in forbidden)]
        sticky = sum(1 for line in sh("git", "show", f"{sha}:js/scripts.js").splitlines()
                     if "sticky" in line.lower())
        # Inverted on purpose for the bar's own commit. "no sticky in scripts.js" is the
        # claim the four item commits make - the bar is not in them - and demanding it of
        # the commit whose whole job is the bar would demand the one result that would
        # prove it empty. Same shape as the gate's BEFORE rule: the assertion is about
        # which side of the line a commit is supposed to be on, not about a number.
        bar_bad = (sticky == 0) if bar_expected else (sticky > 0)
        churn = [l.strip() for l in sh("git", "diff-tree", "--summary", sha).splitlines()
                 if " delete " in l or " mode change " in l]
        print(f"  verified {label:<16} {sha[:8]}  {len(changed):>3} path(s) | outside allowlist: "
              f"{len(surprise)} | owner's paths: {len(hits)} | deletes/mode-changes: "
              f"{len(churn)} | 'sticky' lines in js/scripts.js: {sticky}"
              + (" (this commit IS the bar)" if bar_expected else ""))
        for n in surprise[:8]:
            print(f"      NOT ALLOWED in this commit: {n}")
        for n in hits[:8]:
            print(f"      OWNER'S WORK IN THIS COMMIT: {n}")
        if surprise or hits or churn or bar_bad:
            print(f"\nSCOPE BROKEN by {label}. The commit already exists locally, so this is "
                  f"not a nothing-happened situation: do not push, and undo with "
                  f"`git reset --hard {head_before[:12]}`.")
            sys.exit(2)
        return sha

    if os.environ.get("VERIFY_ONLY") or "--verify-only" in sys.argv:
        # Re-check the commits without making any. A check that only ever runs inside the
        # commit path cannot be re-run after an amend, a rebase, or a second pair of hands
        # on the branch - which is exactly when the invariant matters most.
        #
        # Labelled by each commit's subject rather than by its position, because position
        # is a lie the moment anything is amended, fixup-rebased or cherry-picked: this
        # file checked the last four commits by position, and the moment the sticky-bar
        # commit landed on top of them the "last four" were the wrong four.
        allow = [("Item 7:", ("css/styles-custom.css", "tests/overflow/"), False),
                 ("Item 5:", tuple(pages()) + ("tests/img-alt/",), False),
                 ("Item 6:", tuple(pages()) + ("css/styles-custom.css", "tests/nav/"), False),
                 ("Tests,", ("tests/", ".gitignore"), False),
                 # The sticky offer bar's own commit, allowlisted by the reviewer's
                 # round-8 wording (tests/reviews/hermes-stickybar-round8-reply.txt):
                 # the bar's CSS and JS and its suite, and nothing else. The CSS is here
                 # because the rule allows it, not because the commit needs it - the CSS
                 # shipped with item 7, and the commit that lands has scripts.js alone.
                 ("Sticky offer bar:", ("css/styles-custom.css", "js/scripts.js",
                                        "tests/sticky-cta/"), True)]
        # Exactly as many commits as there are entries in the table: walk further back and you
        # reach somebody's unrelated old commit, and "I don't know what this commit was
        # supposed to contain" is the right answer about *them*, not about us.
        n = len(allow)
        for sha in reversed(sh("git", "rev-list", f"-n", str(n), "HEAD").split()):
            subject = sh("git", "log", "-1", "--format=%s", sha)
            hit = next(((lab, px, bar) for lab, px, bar in allow if subject.startswith(lab)), None)
            if not hit:
                print(f"  {sha[:8]}  {subject[:52]!r} - NOT IN THE ALLOWLIST TABLE; refusing "
                      f"to guess what it was supposed to contain")
                sys.exit(2)
            verify_commit(hit[0], hit[1], sha, hit[2])
        touched = [x for x in sh("git", "show", "--name-only", "--pretty=format:", "HEAD").split() if x]
        offsite = [x for x in touched if not x.startswith("tests/") and x != ".gitignore"]
        print(f"  tip ({sh('git', 'rev-parse', '--short', 'HEAD')}) touches only tests/: "
              + ("yes" if not offsite else f"NO -> {', '.join(offsite[:6])}"))
        print("\n### left uncommitted")
        for line in sh("git", "status", "--porcelain").splitlines():
            print("  " + line)
        if offsite:
            sys.exit(2)
        return

    # ---- 1. item 7: the stylesheet without the navbar rules + the overflow suite
    stage_blob("css/styles-custom.css", css7)
    files = ["gate.py", "probe.py", "diagnose.py", "cssregions.py", "inert-at-100.py",
             "comment-row.py", "gate-FINAL-chromium.txt", "gate-FINAL-firefox.txt",
             "gate-FINAL-webkit.txt", "gate-BEFORE-cssregions.txt", "inert-100.txt",
             "css-comment-only.py",
             # The WebKit-at-300% investigation: the two diagnostic harnesses, the
             # document of record (mechanism, the eleven remedies that did not work,
             # the two that worked and were rejected, the acceptance rules), and the
             # pre-fix pictures the fix was measured against.
             "why465.py", "fix465.py", "KNOWN-WEBKIT-300.md",
             "gate-BEFORE-cssfix-webkit-RED.txt", "gate-BEFORE-cssfix-chromium.txt",
             "gate-BEFORE-cssfix-firefox.txt"]
    # Globbed, on purpose: every payload snapshot pairs with the artefacts that quote its
    # hash (the pre-fix ones are cited in KNOWN-WEBKIT-300.md as the before picture), and
    # every run log the two harnesses produced. A commit message that cites "the run logs"
    # should ship all of them, not the ones whoever edited this list remembered.
    for pattern in ("payload-measured-*.css", "fix465-*.txt", "why465-*.txt"):
        files += sorted(os.path.basename(p) for p in
                        glob.glob(os.path.join(SITE, "tests/overflow", pattern)))
    for f in files:
        p = os.path.join("tests", "overflow", f)
        if os.path.exists(os.path.join(SITE, p)):
            sh("git", "add", "--", p)
    sh("git", "commit", "-q", "-F", os.path.join(MESSAGES, "item7.txt"))
    commits.append("item 7")
    verify_commit("item 7", ("css/styles-custom.css", "tests/overflow/"))

    # ---- 2. item 5: whitespace and escaping only, old nav still in place
    for name in pages():
        stage_blob(name, os.path.join(STATE, "item5", name))
    for f in ("glued.py", "inventory.py", "space-fix.py",
              "inventory-BEFORE-ad559e9.txt", "inventory-AFTER.txt"):
        sh("git", "add", "--", os.path.join("tests", "img-alt", f))
    sh("git", "commit", "-q", "-F", os.path.join(MESSAGES, "item5.txt"))
    commits.append("item 5")
    verify_commit("item 5", tuple(pages()) + ("tests/img-alt/",))

    # ---- 3. item 6: the nav rewrite, and the navbar CSS item 7 left out
    for name in pages():
        stage_blob(name, os.path.join(STATE, "item6", name))
    stage_blob("css/styles-custom.css", splitmod.CSS_FINAL)
    sh("git", "add", "--", "tests/nav")
    sh("git", "commit", "-q", "-F", os.path.join(MESSAGES, "item6.txt"))
    commits.append("item 6")
    verify_commit("item 6", tuple(pages()) + ("css/styles-custom.css", "tests/nav/"))

    # ---- 4. the suites and the review transcripts the three items were argued with
    # tests/ship is in this commit because it is the harness the three commits above
    # were built with, and it lived in /tmp until a reboot proved the plan's own rule.
    sh("git", "add", "--", "tests/sticky-cta", "tests/reviews", "tests/shots.py",
       "tests/validate.sh", "tests/ship", ".gitignore")
    sh("git", "commit", "-q", "-F", os.path.join(MESSAGES, "tests.txt"))
    commits.append("tests")
    verify_commit("tests", ("tests/", ".gitignore"))
    print("  all four commits inside their own allowlist, none of them carrying a path of "
          "the owner's, and none of them carrying the sticky bar - js/scripts.js is HEAD's "
          "in all four, which is the claim the working-tree check below could not make.")

    print("\n### committed")
    print(sh("git", "log", "--oneline", "-4"))

    # ---- verification 1: what is left uncommitted must be exactly the owner's work
    print("\n### left uncommitted (must be the owner's in-flight work and nothing else)")
    status = sh("git", "status", "--porcelain")
    for line in status.splitlines():
        print("  " + line)

    # ---- verification 2: HEAD must equal the tree the gates measured
    subprocess.run(["rm", "-rf", VERIFY], check=True)
    sh("git", "worktree", "add", "--detach", VERIFY, "HEAD")
    differ = []
    for root in ("*.html",):
        for f in glob.glob(os.path.join(SITE, root)):
            name = os.path.basename(f)
            a = os.path.join(VERIFY, name)
            b = os.path.join(SHIPPED, name)
            if os.path.exists(a) and os.path.exists(b):
                if open(a, "rb").read() != open(b, "rb").read():
                    differ.append(name)
            elif os.path.exists(a) != os.path.exists(b):
                differ.append(name + " (present in only one)")
    # CSS is compared by rule text, not bytes: the gates serve a
    # payload-measured-<hash>.css snapshot, the committed file is a later state of the
    # same stylesheet, and css-comment-only.py is what proves the difference between them
    # is commentary. Its default is the newest snapshot, and it prints all of them.
    # (An earlier version of this comment named the two hashes; naming them here meant
    # this line went stale the first time the stylesheet changed, which it now has.)
    for rel in ("js/scripts.js", "_headers", "_redirects",
                "llms.txt", "sitemap.xml", "index.html"):
        a, b = os.path.join(VERIFY, rel), os.path.join(SHIPPED, rel)
        if os.path.exists(a) and os.path.exists(b) and open(a, "rb").read() != open(b, "rb").read():
            differ.append(rel)
    r = subprocess.run(["python3", os.path.join(VERIFY, "tests/overflow/css-comment-only.py"),
                        os.path.join(SHIPPED, "css/styles-custom.css"),
                        os.path.join(VERIFY, "css/styles-custom.css")],
                       capture_output=True, text=True)
    print("  css provenance vs the measured tree: " + r.stdout.strip().splitlines()[-1][:110])
    if r.returncode != 0:
        differ.append("css/styles-custom.css (rule text differs)")
    if differ:
        print(f"\nHEAD AND THE MEASURED TREE DIFFER: {differ}")
        sys.exit(1)
    print("\nHEAD == the measured tree, file for file (HTML, CSS, JS, headers/redirects/sitemap)")
    print("### diffstat against ad559e9")
    print(sh("git", "diff", "--stat", "ad559e9..HEAD", "--", ".").splitlines()[-1])
    print("COMMITS_OK")


if __name__ == "__main__":
    run("--dry" in sys.argv)
