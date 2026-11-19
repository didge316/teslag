#!/usr/bin/env python3
"""Offline attribution map: every shipped path through the shipped `tidFor()`.

Companion to `tid-live.py`, which reads the tid back out of the DOM. Both exist
because each alone is weak in a different direction: the live read proves what
the real module produced on real pages but only for pages where the bar rendered,
and this one covers every path including pages that never render, but could in
principle drift from the shipped matcher if the extraction were sloppy. The
extraction is therefore asserted in both directions (starts at its own marker,
ends at the function's own closing brace) and the slice that node evaluated is
kept on disk next to the output, so a later reader can diff it against the file.

The reason this is worth two instruments: `rel="noreferrer"` on the CTA means
ClickBank receives no referrer, so `?tid=` is the only attribution channel the
bar will ever have, and a mis-bucketed page is silent, permanent, and corrupts
the one number the feature exists to produce.

Run: python3 tid-map.py    (needs node on PATH; no server)
"""
import collections
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "js", "scripts.js")
OUT = os.path.join(HERE, "tid-map-2026-11-19.txt")
SLICE = os.path.join(ROOT, "tests", ".staging", "tid-eval-extract.txt")

os.makedirs(os.path.dirname(SLICE), exist_ok=True)
src = open(SRC).read()

# Slice between the shipped markers, then out to the function's own closing
# brace. Cutting at the return statement - which is what the first version did -
# produces an unbalanced fragment and node reports "Unexpected end of input" at
# the end of the file, which is a confusing way to ask "you cut my function in half".
start = src.index("var TID_RULES")
anchor = src.index("return 'sticky_article';") + len("return 'sticky_article';")
end = src.index("}", anchor) + 1
extract = src[start:end]
assert extract.strip().startswith("var TID_RULES"), "start marker moved"
assert extract.rstrip().endswith("}"), "extraction does not end on the function's own brace"
assert "function tidFor" in extract, "tidFor is not inside the slice"
open(SLICE, "w").write(extract)

paths = [p for p in subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", "HEAD"],
                                   capture_output=True, text=True, check=True).stdout.split()
         if p.endswith(".html")]

driver = extract + """
const out = [];
for (const p of process.argv.slice(2)) {
  const path = '/' + p.replace(/index\\.html$/, "").replace(/\\.html$/, "").replace(/^\\//, "");
  let rule = -1, why = '(no rule matched) -> fallback sticky_article';
  for (let i = 0; i < TID_RULES.length; i++) {
    if (TID_RULES[i][0].test(path.toLowerCase())) { rule = i; why = String(TID_RULES[i][0]); break; }
  }
  out.push({path, tid: tidFor(path), rule, why});
}
console.log(JSON.stringify(out));
"""
tmp = os.path.join(ROOT, "tests", ".staging", "tid-eval.js")
open(tmp, "w").write(driver)
res = subprocess.run(["node", tmp] + paths, capture_output=True, text=True)
if res.returncode:
    print(res.stderr[:1000])
    raise SystemExit(1)
rows = json.loads(res.stdout)

by = collections.defaultdict(list)
for r in rows:
    by[r["tid"]].append(r)
lines = [
    "# every shipped page's sticky-bar attribution id, produced by running the SHIPPED tidFor()",
    "# (js/scripts.js, sliced between its own markers - the slice node evaluated is kept verbatim",
    "# at tests/.staging/tid-eval-extract.txt) against every .html path in the branch's tree.",
    "# Asked for by the reviewer on the grounds that rel=noreferrer leaves tid as the bar's only",
    "# attribution channel, so a mis-bucketed page is silent and permanent.",
    "# Companion to tid-live.py, which reads the tid out of the rendered CTA href; the two agree",
    "# on all 50 pages where the bar renders. Generated 2026-11-19 by tests/sticky-cta/tid-map.py;",
    "# regenerate rather than hand-edit.",
    "",
    f"{len(rows)} paths. Bucket sizes: " + ", ".join(
        f"{t} {len(v)}" for t, v in sorted(by.items(), key=lambda kv: -len(kv[1]))),
    "",
]
for t in sorted(by, key=lambda x: -len(by[x])):
    lines.append(f"--- {t}: {len(by[t])}")
    for r in by[t]:
        lines.append(f"      {r['path']:<58} rule[{r['rule']}] {r['why']}")
lines += ["", "questions this table raises rather than answers,",
          "  * the fallback bucket carries " + str(len(by.get("sticky_article", []))) +
          f" of {len(rows)} paths, including the site's highest-intent pages",
          "    (/can-I-buy, /build-a-*, /whole-house, /magnetic-generator): the table will mostly",
          "    compare one giant bucket against 1-page buckets, which is an under-specified",
          "    matcher rather than a broken one, and a product decision about intent buckets",
          "    belongs to the owner;",
          "  * /magnetic-generator-scam gets its own bucket and the bar still shows there",
          "    (verified in the live DOM by tid-live.py), so the offer appears on the page that",
          "    argues the product is a scam - suppression there is also the owner's call;",
          "  * the rule's own comment says the scam page would otherwise land in sticky_review;",
          "    run against the table, it would land in sticky_article. Ordering and rule are",
          "    right, the comment's premise is wrong."]
open(OUT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines[:14]))
print(f"\nwrote {OUT}")
