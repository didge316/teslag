#!/usr/bin/env python3
"""Check the internal link map in SERIES-PLAN-1894.md section 5.2 against the built pages.

qa_page.py enforces a weaker rule than section 5.2 states. The gate in section 12 is
"at least 4 internal links, at least 3 of them to pages that link back", and qa_page.py
counts every href on the page, including the shared nav dropdown and footer. Because the
hub is in the nav of every page and the hub links to every article, every page picks up
two reciprocal links from the shell alone. A page can pass that gate with one content
link.

Section 5.2 is the actual contract, and it is a table with two columns: what each
article links out to, and what must link to it. This script checks both columns using
only links inside <article>, so the shared shell cannot satisfy it.

The map is transcribed from SERIES-PLAN-1894.md section 5.2. That file is the spec and
is not edited; if the table changes, change OUT and NEED here and say so in the commit.

Two things this script will show you that the spec does not say:
  - the two columns disagree. Three edges appear in a page's "must be linked from"
    column and in no page's "links out to" column (01 -> 02, 10 -> 04, 03 -> 08). The
    script reports those as ASKED, not as defects, and says which column asked for them.
  - the "4-6 out-links" band in the section heading is a design limit, not a gate. The
    script prints each page's body out-link count so an edit that pushes a page past 6
    is visible rather than silent.

Usage:
  python3 books/tools/link_map.py            # report
  python3 books/tools/link_map.py --json     # machine readable
Exit code: 0 if every edge in both columns is present, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[2] / "website"

# section 5.2 row keys -> page stems
S = {
    "hub": "tesla-1894",
    "01": "tesla-lit-lamps-without-wires",
    "02": "tesla-one-wire-power",
    "03": "tesla-earthquake-machine",
    "04": "tesla-wireless-power-1893",
    "05": "tesla-high-frequency-massage",
    "06": "tesla-cold-flame",
    "07": "rotating-magnetic-field-1888",
    "08": "tesla-weird-inventions-1894",
    "09": "tesla-worlds-fair-1893",
    "10": "tesla-free-energy-what-he-said",
    "11": "tesla-high-frequency-alternator",
    "12": "tesla-glowing-tubes-vacuum",
}
# pages that are not part of the series but appear in the map's "must be linked from"
# column, because section 5.2's backlink pass names them as legacy pages to edit.
LEGACY = {
    "nikola-tesla-inventor-extraordinaire": "nikola-tesla-inventor-extraordinaire",
    "magnetic-generator-scam": "magnetic-generator-scam",
}

# column 1: "Links out to"
OUT = {
    "hub": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
            "magnetic-generator-plans-review", "electrical-experimenter"],
    "01": ["magnetic-dynamo-generator", "electricity-using-magnets", "06", "12"],
    "02": ["diy-magnetic-generator", "can-we-use-magnets-to-generate-electricity-a-magnetic-marvel", "11"],
    "03": ["perpetual-motion-generator", "magnet-motor", "09", "11"],
    "04": ["whole-house", "solar", "02", "11"],
    "05": ["magnetic-generator-scam", "How-Much-Noise-Does-a-Free-Energy-Device-Make", "10"],
    "06": ["7-interesting-facts-about-magnets", "01", "12"],
    "07": ["magnetic-dynamo-generator", "magnetic-generator-plans-review", "tesla-magnetic-generator-worth-it", "11"],
    "08": ["magnet-motor", "perpetual-motion-generator", "10"],
    "09": ["build-a-magnetic-generator", "magnetic-generator-plans-review", "03", "07"],
    "10": ["magnetic-generator-scam", "tesla-magnetic-generator-worth-it", "free-electricity-from-magnets", "05", "08"],
    "11": ["magnetic-generator-plans-review", "magnetic-dynamo-generator", "02", "03"],
    "12": ["free-electricity-from-magnets", "electricity-using-magnets", "01", "06"],
}
# column 2: "Must be linked from"
NEED = {
    "hub": ["nav", "articles", "footer", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    "01": ["04", "06", "12", "hub"],
    "02": ["01", "04", "11", "hub"],
    "03": ["09", "11", "hub"],
    "04": ["02", "10", "hub"],
    "05": ["10", "hub"],
    "06": ["01", "12", "hub"],
    "07": ["03", "11", "hub", "nikola-tesla-inventor-extraordinaire"],
    "08": ["03", "10", "hub"],
    "09": ["03", "07", "hub"],
    "10": ["04", "05", "08", "hub", "magnetic-generator-scam"],
    "11": ["02", "03", "07", "hub"],
    "12": ["01", "06", "hub"],
}

# edges the second column asks for that no first column places anywhere.
# Derived, not hand-kept: computed below and labelled ASKED.
SHELL_ONLY = ("nav", "articles", "footer")


def page_key(href):
    m = re.match(r"https?://teslamagneticgenerator\.com/([a-zA-Z0-9._-]+?)(?:[/?#]|$)", href)
    if m:
        return m.group(1).removesuffix(".html")
    m = re.match(r"/([a-zA-Z0-9._-]+?)(?:[/?#]|$)", href)
    if m:
        return m.group(1).removesuffix(".html")
    m = re.match(r"([a-zA-Z0-9._-]+)\.html$", href)
    if m:
        return m.group(1)
    return None


def body_links(stem):
    """Targets linked from inside <article> only. None if the page does not exist."""
    p = WEB / f"{stem}.html"
    if not p.exists():
        return None
    h = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<article\b.*?</article>", h, re.S)
    if not m:
        return set()
    return {k for k in (page_key(x) for x in re.findall(r'href="([^"]+)"', m.group(0))) if k}


def resolve(key):
    if key in S:
        return S[key]
    if key in LEGACY:
        return LEGACY[key]
    return key  # a money page, named by its own stem


def main():
    as_json = "--json" in sys.argv
    stems = [resolve(k) for k in list(S) + list(LEGACY)]
    links = {s: body_links(s) for s in stems}
    out_names = {k: {resolve(t) for t in v} for k, v in OUT.items()}

    asked_only = []
    for tgt, srcs in NEED.items():
        for s in srcs:
            if s in SHELL_ONLY:
                continue
            if resolve(tgt) not in out_names.get(s, set()):
                asked_only.append((s, tgt))

    report, missing = {}, []
    for tgt, srcs in NEED.items():
        got, gap, shell = [], [], []
        for s in srcs:
            if s in SHELL_ONLY:
                # The hub is in the nav dropdown of every page and in articles.html, which
                # is two of the four sources section 5.2 names for it. Those are shell
                # links, not body links, so they are reported separately and not counted
                # as satisfied or missing here.
                shell.append(s)
                continue
            bl = links.get(resolve(s))
            if bl is None:
                gap.append(f"{s} (no such page)")
            elif resolve(tgt) in bl:
                got.append(s)
            else:
                gap.append(s)
        report[tgt] = {"have": len(got), "need": len(srcs), "missing": gap, "shell": shell}
        missing += [f"{s} -> {tgt}" for s in gap]

    out_report = {}
    for art, targets in OUT.items():
        bl = links.get(resolve(art))
        if bl is None:
            out_report[art] = {"page": resolve(art), "missing": ["PAGE NOT BUILT"]}
            continue
        gap = sorted(t for t in targets if resolve(t) not in bl)
        out_report[art] = {"page": resolve(art), "body_out": len(bl), "missing": gap}
        missing += [f"{art} -> {t}" for t in gap]

    if as_json:
        print(json.dumps({"in_links": report, "out_links": out_report,
                          "asked_by_col2_only": asked_only, "missing_edges": missing}, indent=1))
    else:
        print("section 5.2 column 2, 'Must be linked from', body links only")
        for tgt in NEED:
            r = report[tgt]
            flag = "ok " if not r["missing"] else "MISS"
            sh = f"  (shell, not counted: {r['shell']})" if r["shell"] else ""
            print(f"  [{flag}] {resolve(tgt):34s} {r['have']}/{r['need']}  {r['missing']}{sh}")
        print("\nsection 5.2 column 1, 'Links out to', body links only")
        for art in OUT:
            r = out_report[art]
            flag = "ok " if not r["missing"] else "MISS"
            band = "" if 4 <= r.get("body_out", 0) <= 6 else "  <- outside the 4-6 band in the section heading"
            print(f"  [{flag}] {r['page']:34s} out={r.get('body_out', '-')}  {r['missing']}{band}")
        print("\nedges the second column asks for that no first column places:")
        for s, t in asked_only:
            print(f"  {s} -> {t}   (asked by 'must be linked from' for {resolve(t)}; "
                  f"not in any 'links out to' list)")
        print(f"\nmissing edges total: {len(missing)}")
        for e in missing:
            print(f"  {e}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
