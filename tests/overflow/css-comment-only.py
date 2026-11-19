#!/usr/bin/env python3
"""Prove that a stylesheet whose bytes changed since a measurement still says the
same thing as the bytes that were measured.

Why this exists, specifically: the definitive gates (gate-FINAL-chromium.txt,
gate-FINAL-firefox.txt, gate-FINAL-webkit.txt, gate-BEFORE-cssregions.txt) were run
against a copy of the tree served on 127.0.0.1:8200, and the gate prints the sha256
of the stylesheet it served - `322b32b3533a`. After those runs I went back and
improved the comments in the same file, which changes the hash, which would have
made the numbers in the commit messages describe bytes that no longer exist. Re-running
three 30-minute matrices for prose is one way to handle that; the other is to say
precisely what changed and prove it does not reach the CSSOM.

So the measured bytes are kept in this directory as
`payload-measured-322b32b3533a.css` - the exact file the browser parsed - and this
script compares it to the stylesheet on disk: strip comments, collapse whitespace, and
the two must be byte-identical. The hash of the kept payload is also asserted to start
with the hex prefix the artefacts quote, so the chain is: artefact prints a hash, the
hash belongs to this file, this file says what the committed file says.

What this cannot prove, stated because the temptation is to over-read it: identity of
rule *text* is not a semantic equivalence argument about CSS in general. It is exactly
enough here, because "identical rule text" is the claim being made - the only thing
that moved is commentary - and if a rule had been edited, renamed, reordered or
reformatted-with-a-difference it would show up. It is a provenance check, not a CSS
equivalence prover, and it is not a substitute for re-measuring anything that depends
on rules.

Usage: python3 css-comment-only.py [measured.css] [committed.css]
Exit 0 = same rules, 1 = the rules differ (the measurement no longer describes the
file), 2 = the instrument could not run.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def newest_payload_snapshot():
    """The snapshot that the *current* gates' artefacts quote, picked by mtime.

    More than one can exist, and that is the point: each is the bytes a particular set
    of artefacts served, and the pre-fix runs keep theirs forever (the EmailOctopus
    submit fix of 2026-11-19 changed rule text, so 322b32b3533a now belongs to
    gate-BEFORE-cssfix-* and gate-BEFORE-cssregions, not to the numbers in the commit
    message). Pointing this script at an arbitrary pair is still supported - two
    arguments - which is how you audit an old artefact.
    """
    cands = sorted((os.path.join(HERE, f) for f in os.listdir(HERE)
                    if f.startswith("payload-measured-") and f.endswith(".css")),
                   key=os.path.getmtime)
    if not cands:
        return os.path.join(HERE, "payload-measured-322b32b3533a.css")   # the usual error path
    if len(cands) > 1:
        print(f"note: {len(cands)} payload snapshots here; using the newest. Each one pairs "
              "with the artefacts that quote its hash: "
              + ", ".join(os.path.basename(c) for c in cands))
    return cands[-1]


MEASURED = sys.argv[1] if len(sys.argv) > 1 else newest_payload_snapshot()
COMMITTED = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "..", "css", "styles-custom.css")


def strip_comments(text):
    """Remove /* */ comments and collapse runs of whitespace.

    No regex: the CSS here contains no strings, but a regex over comment markers is a
    parser wearing a hat, and this one has to agree with what a CSS parser does.
    """
    out, i = [], 0
    while True:
        a = text.find("/*", i)
        if a < 0:
            out.append(text[i:])
            break
        out.append(text[i:a])
        b = text.find("*/", a + 2)
        if b < 0:
            sys.exit("INSTRUMENT FAILED: unterminated /* in the input - not going to guess")
        i = b + 2
    return re.sub(r"\s+", " ", "".join(out)).strip()


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    for p in (MEASURED, COMMITTED):
        if not os.path.exists(p):
            sys.exit(f"INSTRUMENT FAILED: no such file {p}")
    h_m, h_c = sha(MEASURED), sha(COMMITTED)
    base = os.path.basename(MEASURED)
    # The filename carries the hash the artefacts quote, so it can be checked; when
    # this script is pointed at an arbitrary pair there is no claim to check and the
    # rule comparison still means what it says.
    prefix = base.split("payload-measured-")[1].split(".")[0] if "payload-measured-" in base else None
    t_m, t_c = strip_comments(open(MEASURED, encoding="utf-8").read()), strip_comments(open(COMMITTED, encoding="utf-8").read())
    print(f"measured payload : {h_m[:12]}  {MEASURED}  ({os.path.getsize(MEASURED)} bytes)")
    print(f"committed file   : {h_c[:12]}  {COMMITTED}  ({os.path.getsize(COMMITTED)} bytes)")
    if prefix and not h_m.startswith(prefix):
        print(f"FAIL: the kept payload hashes {h_m[:12]}, but its filename claims the "
              f"gates served {prefix} - one of the two is not what it says it is")
        sys.exit(1)
    print(f"filename prefix matches the hash it claims: {prefix}" if prefix
          else "filename makes no hash claim (arbitrary pair): comparing rules only")
    print(f"rule text after stripping comments and whitespace: "
          f"{len(t_m)} vs {len(t_c)} chars, sha256 {hashlib.sha256(t_m.encode()).hexdigest()[:12]} "
          f"vs {hashlib.sha256(t_c.encode()).hexdigest()[:12]}")
    rules_m, rules_c = t_m.count("{"), t_c.count("{")
    print(f"rule blocks: {rules_m} measured, {rules_c} committed")
    if t_m == t_c:
        print(f"OK: the two stylesheets are identical once comments are stripped - the "
              f"only difference between the bytes the gates served ({h_m[:12]}) and the "
              f"bytes in this commit ({h_c[:12]}) is commentary, which cannot reach the "
              f"CSSOM. The measured numbers describe this file.")
        sys.exit(0)
    import difflib
    print("FAIL: the rules themselves differ, so this measurement does NOT describe this file.")
    print("      If the rules changed on purpose, that is not a reason to edit this script: the "
          "gates must be re-run against the new bytes, and the CSS the new run served must be "
          "saved here as payload-measured-<its printed hash prefix>.css. The snapshot above is "
          "not stale - it is the evidence for the artefacts that quote it, and it stays.")
    for d in list(difflib.unified_diff(t_m.split("; "), t_c.split("; "), n=0, lineterm=""))[:20]:
        print("  " + d[:160])
    sys.exit(1)


if __name__ == "__main__":
    main()
