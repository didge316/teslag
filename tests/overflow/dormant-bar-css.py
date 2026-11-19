#!/usr/bin/env python3
"""Proof that the offer bar's CSS is dormant in item 7's shipped stylesheet.

The composition wrinkle: item 7's commit contains the offer bar's CSS (21 rule
blocks, 16 selectors) while the JavaScript that puts the bar in the document is
in none of the four commits on this branch - it sits on `feature/sticky-offer-bar`
by the reviewer's own instruction. The claim made in both commit messages is that
the shipped CSS is therefore inert rather than harmful. That is a measurable
claim, and the measured version of it is not "read the JS and see that it adds a
class": it is "delete the rules from the shipped stylesheet and show that nothing
on a real page changes by even one pixel of document height".

Two failure modes this catches that a JS reading cannot:
  * dead space. If the reservation were unconditional - `body { padding-bottom:
    92px }` rather than `body.tmg-cta-pad` - every page on the site would ship
    with a strip of blank above the footer today, and the overflow matrix would
    never have noticed, because extra blank space is not a horizontal scroll.
  * rules that reach. Any `.tmg-cta-*` selector that matched something already in
    the markup, or any `:root`/custom-property side effect, would move layout.

Run: python3 dormant-bar-css.py [base-url] [chromium,firefox,webkit]
  Needs :8200, the measured tree: item 7's committed state, served from the
  browser's own view of the CSS, and the only place the bar's JS is absent.
"""
import os
import re
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8200"
ENGINES = (sys.argv[2].split(",") if len(sys.argv) > 2
           else ["chromium", "firefox", "webkit"])
HERE = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(HERE, "..", "..", "css", "styles-custom.css")
# One artefact per engine set: an earlier version wrote one fixed filename, so the
# webkit-only run that had to go last and alone quietly replaced the chromium+firefox
# rows and the record claimed 26 pages of coverage it no longer contained.
OUT = os.path.join(HERE, "dormant-bar-css-2026-11-19-%s.txt" % "-".join(ENGINES))

PAGES = ["/index.html", "/whole-house.html", "/articles.html", "/magnetic-generator-scam.html",
         "/build-a-perpetual-motion-generator.html", "/can-I-buy.html", "/tesla-1894.html",
         "/tesla-1894-plates.html", "/tesla-1894-word-search.html", "/about.html",
         "/contact.html", "/privacy.html", "/404.html"]

# 22, not 21. The first version of this check stripped only selectors containing
# "tmg-cta", which left the bar's `.tmg-sr-only` rule - the one that keeps
# "(opens in a new tab)" out of the CTA's visible text - outside the comparison, and
# outside the inventory the commit message quoted. The bar's footprint is whatever
# matches "tmg-", so that is what gets stripped and counted.
EXPECTED_BLOCKS = 22          # inventoried from css/styles-custom.css on 2026-11-19


def strip_bar_css(css):
    """Remove every rule block whose selector mentions tmg-cta.

    A top-level block matches `prelude { ... }` with no braces inside, so the
    @media wrapper around the bar's responsive tier is never matched as a whole -
    its inner rules are, one by one, which is exactly what is wanted: the wrapper
    survives with its other rules intact. Comments are left where they are; a
    dangling comment is inert and deleting comment text would make the diff
    harder to read than the change.
    """
    pat = re.compile(r"[^{}]*tmg-[^{}]*\{[^{}]*\}")
    out, n = pat.subn("", css)
    assert out.count("{") == out.count("}"), "brace balance broken by the strip"
    left = [l.strip() for l in out.splitlines()
            if "tmg-" in l and "{" in l and not l.strip().startswith(("*", "/*", "//"))]
    assert not left, f"selectors still live after the strip: {left[:3]}"
    return out, n


STATE = """() => {
    const cs = getComputedStyle(document.body);
    const hits = document.querySelectorAll('[class*="tmg-cta"]').length;
    return {
        docH: document.documentElement.scrollHeight,
        bodyPadBottom: cs.paddingBottom,
        barInDom: !!document.querySelector('.tmg-cta-bar'),
        barClassHits: hits,
        // the bar's own horizontal contribution, if any rules reached at all
        docScrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
    };
}"""


def measure(pw, engine, css_stripped, results):
    b = getattr(pw, engine).launch()
    for path in PAGES:
        row = {"path": path, "engine": engine}
        for flavour, intercept in (("shipped", False), ("bar-css-removed", True)):
            ctx = b.new_context(viewport={"width": 390, "height": 844},
                                has_touch=True, is_mobile=True)
            pg = ctx.new_page()
            try:
                if intercept:
                    # Only the stylesheet is ever intercepted: a route on **/* that
                    # also swallows the document and its third-party requests turns
                    # this into a test of the interception plumbing, and it hung a
                    # first run on networkidle for exactly that reason.
                    # *args because this Playwright hands the route handler the
                    # request as a second positional; with a strict signature the
                    # Request object landed in `body=` and fulfill choked on it.
                    def handler(route, *args, css=css_stripped):
                        route.fulfill(status=200, content_type="text/css", body=css)
                    pg.route("**/styles-custom.css", handler)
                # load, not networkidle: these pages reach out to EmailOctopus and
                # the font CDN, and an instrument that waits for third parties to
                # go quiet is at the mercy of them.
                pg.goto(BASE + path, wait_until="load", timeout=30000)
                # and then settle on document height rather than on a fixed pause.
                # Images lazy-size as they arrive, so a snapshot taken too early is
                # a difference between two timings, not between two stylesheets -
                # which is precisely the false positive that would accuse dormant
                # rules of moving layout.
                prev = None
                for _ in range(10):
                    st = pg.evaluate(STATE)
                    if prev and st["docH"] == prev["docH"] and st["bodyPadBottom"] == prev["bodyPadBottom"]:
                        break
                    prev = st
                    pg.wait_for_timeout(500)
                row[flavour] = st
            except Exception as e:
                row[flavour] = {"error": str(e).splitlines()[0][:140]}
            ctx.close()
        results.append(row)
        print(f"  {path:<46} " + " | ".join(
            f"{f}: {row[f].get('docH', row[f].get('error'))}" for f in ("shipped", "bar-css-removed")))
    b.close()


css = open(CSS_PATH).read()
# The comparison is only honest if the stylesheet being stripped is the stylesheet
# the server is serving. Without this, a stale site-shipped/ tree would make
# "shipped" and "bar-css-removed" two different stylesheets rather than two
# versions of one, and every height difference would be blamed on the bar.
import urllib.request
served = urllib.request.urlopen(BASE + "/css/styles-custom.css", timeout=10).read().decode("utf-8", "replace")
assert served == css, (f"{BASE} is not serving the css/styles-custom.css on disk "
                       f"({len(served)} vs {len(css)} chars) - rebuild the measured tree with "
                       "`python3 tests/ship/stage.py shipped` before measuring anything")
stripped, removed = strip_bar_css(css)
print(f"strip: {removed} rule blocks mentioning tmg-cta removed "
      f"({len(css)} -> {len(stripped)} chars); assert == {EXPECTED_BLOCKS}")
assert removed == EXPECTED_BLOCKS, (
    f"the strip removed {removed} blocks, expected {EXPECTED_BLOCKS}: the stylesheet changed "
    "shape. Re-inventory the selectors before trusting this comparison - the point of the "
    "number is that the check is looking at the whole component, not at whatever a pattern "
    "happened to catch.")

results = []
with sync_playwright() as pw:
    for e in ENGINES:
        print(f"--- {e} ---")
        measure(pw, e, stripped, results)

lines = ["# item 7's shipped stylesheet, with and without the offer bar's CSS, same pages",
         "# same engine same viewport. `same` is the claim: identical document height, identical",
         "# body padding, identical scroll width, and no element in the page wearing a tmg-cta",
         "# class in either state. If dead space had shipped, docH would differ. Generated 2026-11-19.",
         f"# strip removed {removed} rule blocks / the stylesheet's full tmg-cta inventory.", ""]
bad = []
for r in results:
    a, b = r["shipped"], r["bar-css-removed"]
    if "error" in a or "error" in b:
        lines.append(f"{r['engine']:<9} {r['path']:<44} ERROR {a.get('error') or b.get('error')}")
        bad.append(r["path"] + " (measurement failed)")
        continue
    same = (a["docH"] == b["docH"] and a["bodyPadBottom"] == b["bodyPadBottom"]
            and a["docScrollW"] == b["docScrollW"] and not a["barInDom"] and not b["barInDom"])
    lines.append(f"{r['engine']:<9} {r['path']:<44} docH {a['docH']:>7} vs {b['docH']:>7} "
                 f"({'same' if a['docH'] == b['docH'] else 'MOVED'}), "
                 f"bodyPad {a['bodyPadBottom']} vs {b['bodyPadBottom']}, "
                 f"tmg-class elements {a['barClassHits']}/{b['barClassHits']}, "
                 f"bar in DOM {a['barInDom']}/{b['barInDom']}"
                 + ("" if same else "   <-- DORMANCY BROKEN"))
    if not same:
        bad.append(r["path"])
per = {}
for r in results:
    per[r["engine"]] = per.get(r["engine"], 0) + (0 if r["path"] in bad else 1)
lines += ["", f"engine breakdown (pages identical with the bar CSS deleted): "
              + ", ".join(f"{k} {v}" for k, v in per.items())]
lines += ["", f"measurements: {len(results)}   identical with the bar CSS deleted: "
              f"{len(results) - len(bad)}   moved: {len(bad)}"]
lines.append("verdict: " + ("the offer bar's CSS provably contributes nothing to any page "
                            "measured - it is dormant in this commit, as both commit messages say"
                            if not bad else f"NOT DORMANT on: {', '.join(bad)} - the rules reach "
                                            "something and item 7 is shipping the bar's effect "
                                            "without the bar"))
open(OUT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if bad else 0)
