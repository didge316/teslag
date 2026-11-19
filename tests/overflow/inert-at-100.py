#!/usr/bin/env python3
"""Proves the item-7 CSS is inert at 100%: every box, and every box's ink, in
the same place with and without the stylesheet change.

The claim this repo keeps making - "every cap is min(<rem>, <the px that rem
already is at 16px>, so nothing moves at 100%" - is arithmetic, and arithmetic
about CSS is a claim, not a measurement (PLAN §1). This measures it.

Method: serve one page twice through the same browser and compare geometry.

  before   the current styles-custom.css with the two item-7 regions cut out
           (CUTS below pins the regions; the derivation is asserted, so if the
           boundaries move the script refuses rather than silently comparing a
           stylesheet to itself)
  after    the file as it stands

The before-CSS is supplied by intercepting the request for that one URL and
fulfilling it with the derived text (ctx.route), so the change is never written
to disk and no second copy of the site is made to test against.

What is compared, and why not pixels: the page has two regions that are never in
the same place twice - the rotating scarcity spinner, which has an infinite CSS
animation, and the EmailOctopus iframe, which is a third-party frame that arrives
when it arrives. A pixel diff therefore needs those masked before it can mean
anything. Geometry does not, provided it is not blind to the failure being
tested: the defect this change exists to fix is a heading that grew
documentElement.scrollWidth by 122px of ink while its own box stayed 318px wide,
and a bounding-rect-only diff would have called that clean. So each box is
captured as [tag, classes, x, y, w, h] plus its scrollWidth/clientWidth/
scrollHeight/clientHeight, which is where ink overflow shows up (scrollWidth >
clientWidth on a box that is not itself a scroll container). Rects to locate a
change, ink to detect it.

Determinism, because three renders are not one measurement: each flavour is
captured TWICE and the two must agree, or the page is reported as not
reproducible and the change is not exonerated either - the instrument is the
thing that failed. Before capture the page is scrolled top-to-bottom and back
(so loading="lazy" images have all been loaded in both runs), and animations are
switched off with one injected rule that is applied identically to both flavours
and touches no layout property.

Pages: 14, chosen to cover each template shape rather than each count - home,
contact (the only p-5 nest and the only btn-lg), privacy (a bare card-body p-5),
404, the articles hub (the only gx-5 row), an article with comments
(tesla-magnetic-generator-worth-it, the +176px comment offender), a 1894 page
(tesla-1894-plates, the sources-link offender), tesla-worlds-fair-1893 (the ink
offender and the deliberate positive control: its 300% rendering must change and
its 100% rendering must not), electrical-experimenter (the heaviest page, 170
images), magnet-motor (one of the twelve `fs-5 ... p-5` blocks), about, and
can-I-buy.

Three things were added after the first version of this file was accepted, each
because a reviewer (Hermes, round 3) refused to accept the claim it made:

* **Lines, not just boxes.** A diff of boxes and of scroll ink is blind to the one
  failure mode that `overflow-wrap: break-word` and `white-space: normal` - two of
  the levers item 7 actually pulls - can cause: a word that breaks one character
  earlier moves the glyphs while every box keeps the same width and height, so
  every number this file used to compare is unchanged. It now also captures, for
  every text node, the rectangle of each *line* the browser laid out (Range
  .getClientRects() over the node's contents), keyed by the node's position in the
  document. That is the difference between "the boxes are the same size" and
  "nothing moved", which is the claim being made.
* **The payload, hashed.** A stylesheet diff can silently become "the same
  stylesheet twice" - it happened to this branch's gate, which reported three
  engines agreeing because the before text never reached the browser. Both
  flavours are now served through the same route handler, the bytes handed to the
  page are hashed per load, printed, and the run exits 2 if the two hashes match
  or if a flavour served anything other than the text it was given.
* **The injected sticky bar, excluded and the exclusion counted.** `#tmg-sticky-cta`
  is written into the document by scripts.js; its own subtree is fixed in px by a
  different feature entirely and its arrival time is not a CSS fact. Its elements
  are excluded from the comparison - and the excluded count is printed for both
  loads and must agree, because an exclusion whose size nobody checks is a way to
  hide a regression rather than a way to avoid a false alarm.

Usage: python3 inert-at-100.py [base-url] [--only a,b] [--widths 390,1280]
Exit 0 = every box, every ink number and every text line identical; 1 = something
moved; 2 = the instrument could not decide (page not reproducible, payload not
distinguished, sticky-bar exclusion disagreeing).
"""
import hashlib
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

import cssregions   # same directory: CUTS + before_css(), shared with gate.py

CSS = cssregions.CSS
CSS_URL_PART = "/css/styles-custom.css"

SAMPLE = [
    "index", "contact", "privacy", "404", "articles", "about", "can-I-buy",
    "magnet-motor",                                     # fs-5 ... p-5 block
    "tesla-1894-plates",                                # sources-link offender
    "tesla-worlds-fair-1893",                           # ink offender / control
    "tesla-magnetic-generator-worth-it",                 # comment rows offender
    "whole-house",             # the Popular Pages widget: a.d-flex > span
    "electrical-experimenter",                          # heaviest page
]
WIDTHS = [390, 320, 1280]
HEIGHT = {320: 844, 390: 844, 1280: 900}

# x, y, w, h in the first six fields - where every box is; scrollWidth/
# clientWidth/scrollHeight/clientHeight in the last four - where ink is. A box
# whose text overflows its own padding box shows up as scrollWidth > clientWidth
# here even though its rect never left the viewport, which is the class of change
# a rect-only diff is blind to.
#
# `lines` is the other half: for every text node, the rectangle of every line the
# browser laid out inside it. Boxes can be identical while the words move.
GEOM = """() => {
  // Document coordinates, not viewport coordinates. The first version of this
  // instrument recorded "this page does not repeat within one stylesheet" on 41 of
  // 39 combinations - and reading the diffs gave it away immediately: every box the
  // same size, every ink width the same, y off by a small constant, HTML itself at
  // y=-4 one load and y=-6 the next. That is not layout, that is where the page
  // happened to be scrolled when the rectangles were read (SETTLE scrolls the document
  // to force lazy content and returns to 0, and the return is not always finished).
  // getBoundingClientRect() is viewport-relative by definition, so a scroll delta
  // translates the entire document and every "unstable" verdict was the instrument
  // describing its own timing. Adding scrollX/scrollY makes the comparison invariant
  // to it, which is the property the claim needs: `moved` should mean the CSS moved
  // something, never where the wheel happened to be. (`position: fixed` boxes are
  // viewport-anchored by nature and this makes them document-anchored in the diff;
  // the one fixed subtree that matters, the injected CTA bar, is excluded below and
  // its exclusion is counted.)
  const sx = Math.round(window.scrollX), sy = Math.round(window.scrollY);
  const path = (e) => {
    const p = [];
    for (let n = e; n && n.tagName !== 'HTML'; n = n.parentElement) {
      p.unshift(n.tagName + ':' + [...n.parentElement.children].filter(c => c.tagName === n.tagName).indexOf(n) +
                (typeof n.className === 'string' && n.className ? '.' + n.className.trim().split(/ +/).join('.') : ''));
    }
    return p.join('>');
  };
  const sticky = document.getElementById('tmg-sticky-cta');
  const inSticky = (e) => !!sticky && sticky.contains(e);
  const boxes = [...document.querySelectorAll('*')].filter((e) => !inSticky(e)).map((e) => {
    const r = e.getBoundingClientRect();
    // Elements with no box at all - everything in <head>, anything display:none -
    // have no position, so they get zeros and no scroll offset. Without this the
    // scroll compensation above lands on `getBoundingClientRect()` of a <meta>,
    // which in Chromium is [0, 0, 0, 0] in viewport space, and the diff then reports
    // "the page does not repeat" because <META> sat at y=7 one load and y=14 the
    // next: a scroll reading on an element that has no place to be.
    const unrendered = e.getClientRects().length === 0;
    return [e.tagName, typeof e.className === 'string' ? e.className : '',
            unrendered ? 0 : Math.round(r.x) + sx,
            unrendered ? 0 : Math.round(r.y) + sy,
            Math.round(r.width), Math.round(r.height),
            e.scrollWidth, e.clientWidth, e.scrollHeight, e.clientHeight];
  });
  const lines = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const host = n.parentElement;
    if (!host || inSticky(host) || !n.textContent.trim()) continue;
    const rg = document.createRange();
    rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].map((q) => [Math.round(q.x) + sx, Math.round(q.y) + sy,
                                                       Math.round(q.width), Math.round(q.height)]);
    if (rects.length) lines.push([path(host) + '#' + n.textContent.trim().slice(0, 24), rects]);
  }
  return {boxes, lines, scroll: [sx, sy],
          sticky: sticky ? sticky.querySelectorAll('*').length + 1 : 0,
          root: getComputedStyle(document.documentElement).fontSize};
}"""

SETTLE = """() => {
  // Load everything loading="lazy" would defer, both times, then come back.
  return new Promise((resolve) => {
    const h = document.body.scrollHeight;
    let y = 0;
    const step = () => {
      y += Math.max(300, window.innerHeight - 100);
      window.scrollTo(0, y);
      if (y < h) setTimeout(step, 60);
      else { window.scrollTo(0, 0); setTimeout(() => resolve(true), 250); }
    };
    step();
  });
}"""

# Applied to both flavours, before any layout, so it cannot be the thing that
# makes them agree. Only animation and transition are touched; no layout property.
FREEZE = "*,*::before,*::after{animation:none!important;transition:none!important}"


def capture(pg, url):
    """One page, one load, one record. `served` is filled by the route handler."""
    pg.goto(url, wait_until="load", timeout=60000)
    pg.add_style_tag(content=FREEZE)
    try:
        # The sticky bar is injected by scripts.js; whether it has landed by
        # capture time is a race, and a missing 96px bar moves the document and
        # every box below it. Wait for it (it is legitimately absent on contact,
        # privacy and 404, and on any page with no H1).
        pg.wait_for_selector("#tmg-sticky-cta", timeout=2000, state="attached")
    except Exception:                                            # noqa: BLE001
        pass
    pg.evaluate(SETTLE)
    root = pg.evaluate("() => getComputedStyle(document.documentElement).fontSize")
    if root != "16px":
        raise Instrument(f"this file measures 100% only, but the page reports root {root}")
    return pg.evaluate(GEOM)


class Instrument(Exception):
    """The check could not decide, which is not the same as the CSS failing."""


def summarise_lines(a, b, limit=6):
    """Line-level diff: where a text node's laid-out lines differ between loads.

    Keyed by the node's document path plus its first 24 characters, so a node that
    changes *content* between loads (a rotating spinner) shows as a missing key and
    is reported as unreproducible rather than as movement - and a node whose content
    is the same but whose words broke differently shows up here, which is the whole
    reason this function exists.
    """
    ka = dict(a)
    kb = dict(b)
    out = []
    for k in sorted(ka):
        if k not in kb:
            out.append(f"LINE-GONE {k}")
        elif ka[k] != kb[k]:
            out.append(f"REWRAPPED {k}: {ka[k][:3]} -> {kb[k][:3]}")
        if len(out) >= limit:
            break
    extra = [k for k in kb if k not in ka]
    if extra:
        out.append(f"LINE-NEW x{len(extra)} e.g. {extra[0]}")
    return out


def summarise(a, b, limit=6):
    """First few differences: boxes in a are missing from b, or moved."""
    out = []
    seen = {}
    for t in b:
        seen.setdefault((t[0], t[1]), []).append(t)
    for t in a:
        m = seen.get((t[0], t[1]))
        u = m.pop(0) if m else None
        if u is None:
            out.append(f"MISSING {t[0]}.{t[1][:30]} {t[2:]}")
        elif u != t:
            out.append(f"{t[0]}.{t[1][:22]} {t[2:6]} ink{t[6:8]} -> {u[2:6]} ink{u[6:8]}")
        if len(out) >= limit:
            break
    return out


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def drift(x, y):
    """Everything that differs between two captures of the same page.

    Returns (box_diffs, line_diffs, sticky_pair, missing_boxes) where sticky_pair
    is the excluded-element counts, reported rather than assumed: an exclusion of
    unknown size is a place a regression can hide.
    """
    return (summarise(x["boxes"], y["boxes"]),
            summarise_lines(x["lines"], y["lines"]),
            (x["sticky"], y["sticky"]))


def main():
    args = sys.argv[1:]
    base = next((a for a in args if not a.startswith("--")), "http://127.0.0.1:8199").rstrip("/")
    # The page list comes from git, not from SAMPLE, unless SAMPLE was asked for by
    # name with --only: a hard-coded list quietly describes a tree that no longer
    # exists, and in the last run it produced `the page was served 0 copies of the
    # before CSS` for a page the measured tree does not contain (it is the untracked
    # work-in-progress page, present in the working directory and absent from the
    # commit) - which reads like a defect and is really a stale fixture.
    pages = SAMPLE
    widths = WIDTHS
    if "--only" not in args:
        r = subprocess.run(["git", "ls-files", "*.html"], cwd=SITE_ROOT,
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            pages = sorted(os.path.basename(x)[:-5] for x in r.stdout.split())
            print(f"pages from git: {len(pages)} (the committed tree; SAMPLE not used)")
        else:
            print(f"pages: {len(pages)} from SAMPLE - git ls-files unavailable, "
                  f"so a stale fixture is possible and the run knows it")
    if "--only" in args:
        pages = args[args.index("--only") + 1].split(",")
    if "--widths" in args:
        widths = [int(x) for x in args[args.index("--widths") + 1].split(",")]

    shipped = open(CSS, encoding="utf-8").read()
    text_before = cssregions.before_css()
    hs, hb = sha(shipped), sha(text_before)
    print(f"payloads: shipped {hs} ({len(shipped)} bytes) | derived pre-item-7 {hb} "
          f"({len(text_before)} bytes)")
    if hs == hb:
        print("INSTRUMENT FAILED: the two flavours are the same bytes; this run would compare "
              "a stylesheet with itself and report the difference as inertness.")
        sys.exit(2)

    moved = unstable = ok = 0
    stage = {"captures_ok": 0, "captures_bad": 0}   # the two-stage tally: the flavour
                                                    # loop and the comparison loop both
                                                    # add to `unstable`, so the old
                                                    # summary line could not add up
                                                    # (11 + 2 + 73 against 39 pages)
    seen_sticky = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w in widths:
            # Rebuilt per width on purpose: a key without the width would let a
            # page that failed to capture at one width be compared against its
            # capture at another one, which is a silent cross-width diff.
            cache = {}
            for flavour, css in (("before", text_before), ("after", shipped)):
                h = sha(css)
                ctx = b.new_context(viewport={"width": w, "height": HEIGHT.get(w, 900)})
                # Both flavours go through the same handler: an interception that
                # only exists on one side is how a "before" run ends up measuring
                # the shipped file and every difference vanishing into agreement.
                served = []

                def handler(route):
                    try:
                        route.fulfill(status=200, content_type="text/css", body=css)
                        served.append(h)
                    except Exception:                                           # noqa: BLE001
                        served.append("FAILED")

                ctx.route(f"**{CSS_URL_PART}", handler)
                pg = ctx.new_page()
                for p in pages:
                    url = f"{base}/{p}.html"
                    try:
                        recs = []
                        for _ in range(2):                     # twice: reproducibility first
                            served.clear()
                            rec = capture(pg, url)
                            if served.count(h) != 1:
                                raise Instrument(f"the page was served {served.count(h)} copies of "
                                                 f"the {flavour} CSS (expected exactly 1)")
                            recs.append(rec)
                    except Instrument as exc:
                        unstable += 1
                        stage["captures_bad"] += 1
                        print(f"  INSTRUMENT {p} @ {w}px {flavour}: {exc}")
                        continue
                    except Exception as exc:                                    # noqa: BLE001
                        moved += 1
                        print(f"  FAIL     {p} @ {w}px {flavour}: {str(exc).splitlines()[0]}")
                        continue
                    if recs[0]["sticky"] != recs[1]["sticky"]:
                        unstable += 1
                        stage["captures_bad"] += 1
                        print(f"  UNSTABLE {p} @ {w}px {flavour}: the injected sticky bar contributed "
                              f"{recs[0]['sticky']} elements one load and {recs[1]['sticky']} the next "
                              "- it is excluded from the comparison, but an exclusion whose size "
                              "changes between loads is not a controlled exclusion")
                        continue
                    d_box = summarise(recs[0]["boxes"], recs[1]["boxes"])
                    d_line = summarise_lines(recs[0]["lines"], recs[1]["lines"])
                    if d_box or d_line:
                        unstable += 1
                        stage["captures_bad"] += 1
                        print(f"  UNSTABLE {p} @ {w}px {flavour}: this page does not repeat within one "
                              f"stylesheet (boxes {d_box[:2]}, lines {d_line[:2]}) - the instrument, "
                              "not the CSS, is what cannot be reproduced")
                        continue
                    cache[(p, flavour)] = recs[0]
                    stage["captures_ok"] += 1
                    seen_sticky = max(seen_sticky, recs[0]["sticky"])
                ctx.close()

            # both flavours for this width are in `cache`: compare them
            for p in pages:
                x, y = cache.get((p, "before")), cache.get((p, "after"))
                if not x or not y:
                    unstable += 1
                    print(f"  NO RESULT {p} @ {w}px: one flavour never produced a capture - "
                          "absence of evidence is not inertness")
                    continue
                db = summarise(x["boxes"], y["boxes"])
                dl = summarise_lines(x["lines"], y["lines"])
                if db or dl:
                    moved += 1
                    parts = []
                    if db:
                        parts.append("boxes " + " | ".join(db[:3]))
                    if dl:
                        parts.append(f"{len(dl)} text nodes rewrapped, e.g. " + " | ".join(dl[:2]))
                    print(f"  MOVED    {p} @ {w}px: " + " ; ".join(parts))
                else:
                    ok += 1
                    print(f"  ok       {p} @ {w}px: {len(x['boxes'])} boxes in the same place, same ink, "
                          f"and {sum(len(v) for _, v in x['lines'])} laid-out text lines identical "
                          f"(sticky bar excluded: {x['sticky']} elements)")
        b.close()

    total = len(pages) * len(widths)
    print(f"\n{total} page x width combinations at root font 16px: {ok} identical, {moved} moved, "
          f"{unstable} not reproducible (this total spans both stages, so it can exceed "
          f"{total}: flavour-stage {stage['captures_ok']} usable captures, "
          f"{stage['captures_bad']} rejected; sticky-bar exclusion observed up to "
          f"{seen_sticky} elements)")
    if unstable:
        print("INCONCLUSIVE: fix the instrument first (what moves between two identical loads?), "
              "then decide what it says about the CSS.")
        sys.exit(2)
    if moved:
        print("FAIL: the item-7 CSS changes 100% rendering, which contradicts the reason it was "
              "accepted as inert. Either scope the rule tighter or state plainly that it is a "
              "visible improvement at 100% and say which pages change.")
        sys.exit(1)
    if not ok:
        print("INSTRUMENT FAILED: NO RESULTS")
        sys.exit(2)
    print("OK: at root font 16px the change is inert - identical geometry, identical ink, "
          "identical line layout.")


if __name__ == "__main__":
    main()
