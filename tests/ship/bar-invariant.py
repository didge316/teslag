#!/usr/bin/env python3
"""
Hermes' bar-extraction invariant, verbatim from tests/reviews/hermes-stickybar-round8-ask.txt:

    git log --oneline <harness-tip>..feature/sticky-offer-bar
        exactly one commit. If the extraction is more than one commit the invariant is
        about the branch as a whole, not its tip.
    git diff --name-status <harness-tip> feature/sticky-offer-bar
        every line starts M or A, none starts D. Allowlist, not denylist: only
        js/scripts.js, js/sticky-cta.js if you rename, and test artifacts under
        tests/... Anything outside that set is contamination even if it looks inert.
    git diff <harness-tip> feature/sticky-offer-bar -- js/scripts.js
        +N/-1 where the single removed line is `})();` and the surviving bytes before
        the hunk are byte-identical.
    Compare `git rev-parse <bar-commit>:js/scripts.js` against `git hash-object
    js/scripts.js`, and quote the hash in the commit message and in the round-8 reply.
    ...
    and add to the same message the output of:
        git ls-tree <harness-tip> -- _headers _redirects llms.txt sitemap.xml
        git ls-tree feature/sticky-offer-bar -- _headers _redirects llms.txt sitemap.xml
    which must be byte-identical between the two commits while those four stay dirty in
    the working tree.

NOT "git add -u .", not a denylist, and nothing outside js/scripts.js and tests/.
Written by the assistant, run against the real commits, output committed as evidence.

ONE CORRECTION TO THE Wording, made after this script had already been run a
half-dozen times: this repository stores objects by **sha1**
(`git rev-parse --show-object-format` says so), so `da605e24...` - the value printed
under "blob sha256" in early runs of this script and quoted in two commit messages - is
the sha256 of the file's raw bytes, which is what `sha256sum` produces and is not a git
object id at all. The blob id is `ec37ac5d59c2...`. Both are identity checks and the
conclusion was never wrong (the bytes were the same in every version of the extraction),
but a number quoted as a blob hash has to be one, so both are printed and labelled now.

The extraction's content identity is a strong claim, and the version of this check that
only compared the two hashes would also have been satisfied by a tree where the file had
changed on both sides together. It cannot be satisfied by a commit containing a *deleted*
file (that would fail the M/A rule and the +/-hunk rule as well).
"""

import subprocess
import hashlib
import sys

SITE = "/home/matt/projects/other/tesla-generator/website/"
BLOB_ALLOW = ("js/scripts.js", "js/sticky-cta.js")
# Relative, like the paths `git diff --name-status` prints. An absolute prefix here
# can never match, and the allowlist check would then report every tests/ artifact as
# contamination - a loud failure, which is better than the reverse mistake.
OUT_DIR = "tests/"

# Spelled as paths, not as a substring. A bare `electrical-experimenter` also matches
# assets/electrical-experimenter.pdf and assets/electrical-experimenter-cover.webp,
# both legitimately tracked since 73904ae (the lead-magnet assets), and a denylist that
# reports "0 in-flight paths" because it swallowed two tracked files into its pattern is
# reporting an artifact of the pattern rather than the state of the tree.
INFLIGHT = ["electrical-experimenter.html", "assets/ee1919",
            "assets/og/electrical-experimenter.webp", "js/email-capture-widget.html",
            "_headers", "_redirects", "llms.txt", "sitemap.xml"]


def sh(*a):
    return subprocess.run(a, cwd=SITE, capture_output=True, text=True).stdout


def main(bar, parent=None):
    parent = parent or sh("git", "rev-parse", bar + "^").strip()
    print(f"bar commit    : {bar}")
    print(f"parent (harness tip): {parent}")
    ok = True

    def check(label, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        print(f"  {'PASS' if passed else 'FAIL'}  {label}{('  ' + detail) if detail else ''}")

    print("\n1. exactly one commit between the harness tip and the branch tip")
    count = len([l for l in sh("git", "log", "--oneline", f"{parent}..{bar}").splitlines() if l.strip()])
    check("git log --oneline <harness-tip>..feature/sticky-offer-bar",
          count == 1, f"commit count: {count}")

    print("\n2. allowlist, not denylist - only these may appear in the diff")
    ns = sh("git", "diff", "--name-status", parent, bar).strip().splitlines()
    outside, dels = [], []
    for line in ns:
        st, path = line.split("\t")[0], line.split("\t")[-1]
        allowed = path.startswith(BLOB_ALLOW) or path.startswith(OUT_DIR)
        if not allowed:
            outside.append(f"{st} {path}")
        if st.startswith("D") or path not in ("js/scripts.js",) and st not in ("A", "M"):
            dels.append(f"{st} {path}")
    check("every path in js/scripts.js or tests/...", not outside,
          f"{len(ns)} path(s), outside the allowlist: {outside if outside else 0}")
    check("no line starts with D, no mode change",
          not [d for d in ns if d.split("\t")[0].startswith("D")]
          and not [d for d in ns if not d.split("\t")[0][0].isdigit() and d.split("\t")[0] not in ("A", "M")],
          "statuses seen: " + ",".join(sorted({l.split("\t")[0] for l in ns})))

    print("\n3. the blob, both ways of naming it")
    blob_id = sh("git", "rev-parse", f"{bar}:js/scripts.js").strip()
    wt_blob = sh("git", "hash-object", "js/scripts.js").strip()
    check("`git rev-parse <bar-commit>:js/scripts.js` == `git hash-object js/scripts.js`",
          blob_id == wt_blob, f"blob id: {blob_id}")
    content = subprocess.run(f"git -C {SITE} show {bar}:js/scripts.js", shell=True,
                             capture_output=True).stdout
    sha256 = hashlib.sha256(content).hexdigest()
    wt_sha = hashlib.sha256(open(SITE + "js/scripts.js", "rb").read()).hexdigest()
    check("content sha256 of the committed blob == the worktree file",
          sha256 == wt_sha, f"content sha256: {sha256}")
    check("the file in the bar commit is not the harness one",
          blob_id != sh("git", "rev-parse", f"{parent}:js/scripts.js").strip(),
          f"parent blob: {sh('git', 'rev-parse', parent + ':js/scripts.js').strip()}")

    print("\n4. the hunk - the only deletion is the `})();` the module is appended after")
    diff = sh("git", "diff", parent, bar, "--", "js/scripts.js").strip().splitlines()
    removed = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]
    check("+N/-1 and the single removed line is `})();`",
          len(removed) == 1 and removed[0].strip() == "})();",
          f"removed line(s): {removed!r}")
    plus = len([l for l in diff if l.startswith("+") and not l.startswith("+++")])
    print(f"        +{plus}/-{len(removed)}")
    parent_bytes = sh("git", "show", f"{parent}:js/scripts.js").encode()
    marker = b"})();"
    cut = parent_bytes.rindex(marker) + len(marker)
    check("bytes before the hunk are byte-identical",
          content[:cut] == parent_bytes[:cut],
          f"identical over the first {cut} bytes, the hunk starts after the parent's final `{marker.decode()}`")

    print("\n5. the in-flight set must never reach the branch")
    hits = [p for p in sh("git", "diff", "--name-only", parent, bar).splitlines()
            if p in INFLIGHT or p.startswith("assets/ee1919")]
    check(f"none of {len(INFLIGHT)} in-flight paths in the bar diff", not hits,
          f"leaked: {hits if hits else 0}")
    wt = sh("git", "status", "--porcelain", "--untracked-files=all").splitlines()
    wt_hits = [l for l in wt if any(p.strip("/").rstrip("*") in l or l.split()[-1].startswith(p)
                                    for p in INFLIGHT if not p.startswith("assets/ee1919"))
               or "assets/ee1919" in l]
    check("the working tree still carries them uncommitted", len(wt_hits) > 0,
          f"{len(wt_hits)} path(s) uncommitted")

    print("\n6. parent-owned files identical between parent and bar, while dirty in the tree")
    pa = sh("git", "ls-tree", parent, "--", "_headers", "_redirects", "llms.txt", "sitemap.xml")
    pb = sh("git", "ls-tree", bar, "--", "_headers", "_redirects", "llms.txt", "sitemap.xml")
    wt_state = {l.split()[-1]: l[:2] for l in wt}
    print("        parent:  " + pa.replace("\n", "\n        parent:  ").strip())
    print("        bar:     " + pb.replace("\n", "\n        bar:     ").strip())
    check("byte-identical between the two commits", pa == pb and pa.strip() != "",
          "4 blobs")
    dirty = [p for p in ("_headers", "_redirects", "llms.txt", "sitemap.xml")
             if wt_state.get(p, "").strip() not in ("", "??")]
    check("and still dirty in the working tree (they are the owner's)", len(dirty) == 4,
          f"{len(dirty)}/4")

    print(f"\nverdict: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:] or ["feature/sticky-offer-bar"])))
