#!/usr/bin/env python3
"""Keeper gate for item 7: no page may scroll sideways at large text.

Asserts documentElement.scrollWidth <= clientWidth + 1 on every page (cells that pass only
thanks to that 1px are counted and printed in the summary, so a fix that leaves a 1px leak
cannot hide inside a green verdict), at
  * root 32px (200%), which is the WCAG 1.4.4 number, root 48px (300%), which is
    the grace case above it, and root 16px, which is the control proving the fix
    did not simply resize the site;
  * width 320px, the WCAG 1.4.10 reflow contract - and the 320x48 corner is the
    tightest cell in the grid by the rem-ratio argument (320/48*16 ~ 107 rem
    units against 130 at 390x48);
  * width 768px and 1280px, which are not filler: at 1280 the navbar is a row
    instead of a toggler and the article columns go 3-up, so a 48px root font
    there is a different layout configuration rather than a wider phone. 16px at
    those widths is the control, so a pass at 32px or 48px there is a comparison
    and not a guess.
That is the whole 4 widths x 3 roots grid = 12 cells, 12 x 53 pages = 636
combinations per engine.

The root font is the number a reader changes when they zoom or turn on text
scaling, and 200% / 300% of it is what inflates every rem on the site. Note for
the record: PLAN §4 says the site has its own A+/A- control (wp-textsize) that
sets the root font, so this would be "a supported user action, not a browser-zoom
curiosity". Measured, no such control exists - nothing in the 53 pages or the
four scripts sets the root font, and the string survives only in a comment
inherited from the WordPress template this was ported off. The requirement is
unaffected: WCAG 1.4.4 is about the reader's own zoom, which no site can remove.

WHY THIS GATE CARRIES SO MUCH PROOF MACHINERY, AND WHAT IT IS FOR
--------------------------------------------------------------------------------
This instrument has been wrong twice, in the same direction, in one day. Both
times it reported a clean green while measuring something other than the thing
under test, and neither produced an error line.

 1. It measured a third-party widget mid-reveal, 75px to the right of where it
    ends up, and reported a page-wide overflow on pages that are clean. WebKit
    only, 148 cells, all of them invented. (Fix: finish the animations instead of
    racing them, and force the reveal instead of scrolling to it - see REVEAL and
    QUIESCE below, and the TRANSIENT classification, which reports the transient
    state rather than silently discarding it.)
 2. It applied the root font in a way that does not survive navigation, so every
    32px and 48px cell silently measured 16px rendering - where the site was
    always clean. chromium, webkit and firefox each then reported 636/636 green,
    and so did the BEFORE run, which is the only reason anyone noticed. Three
    engines agreeing is not evidence when all three are measuring the wrong thing.

So the gate no longer reports a verdict it cannot substantiate. Every run carries:
  * a NEGATIVE CONTROL inside the run: one pinned page x cell served with this
    change's CSS cut out must be RED with a named offender at a named magnitude
    (or, in a --before-css run, served with the shipped CSS and must be green).
    If the control does not behave, the run exits 2 and prints no summary. This is
    the answer to "can this measurement distinguish a good page from a bad one",
    which no amount of input canarying answers: an assertion with no dynamic
    range is not an assertion.
  * canaries read in the SAME evaluate() as the verdict, so they describe the same
    layout state: the computed root font, a 10rem probe element measured in
    device-independent pixels (the cascade accepting a declaration is not the same
    fact as the layout engine laying out at that size), whether Bootstrap's
    stylesheet is applied at all (an unstyled page never overflows, so a CSS load
    failure is indistinguishable from a fix), and the flavour marker
    (.navbar-brand white-space, which differs between the two payloads).
  * a per-navigation injection counter and a served-payload counter: if the route
    interception did not run, the run is void rather than green.
  * payload hashes and a structural diff of the two stylesheets, printed at
    startup, so "before" cannot be a malformed stylesheet that is red for the
    wrong reason, and "identical payloads" cannot pass as a comparison.
  * a stability re-read: any cell whose geometry moves between two reads is
    UNSTABLE and the run is void, because an unstable cell that happened to look
    green is the same failure class with better manners.
  * a row count asserted against the matrix it claims to have measured.
Exit codes are distinct on purpose: 0 green, 1 a real defect, 2 the instrument.
A defect and a broken harness need different humans.

WHAT THIS GATE STRUCTURALLY CANNOT SEE, stated here so the next reader does not
have to rediscover it: documentElement.scrollWidth does not include a
position:fixed subtree, so the mobile drawer, the sticky offer bar and the exit
popup are invisible to it by construction. The gate counts and prints fixed
subtrees that clip their own content (scrollWidth > clientWidth) instead, because
that is the defect class found there by eye (a 62-character dropdown label
clipped with no page scroll to betray it) and it is reported rather than
silently allowed. The drawer's own geometry, and whether its items reach 44px,
is tests/nav/verify.py's job, at 16/32/48 root fonts.

Contexts are plain narrow desktop viewports: NO mobile emulation. With is_mobile
set, Chromium grows the containing block of a position:fixed element to the
page's scrollWidth and innerWidth agrees with it, which is how the old "green"
runs hid a real overflow (SHIP.md / PLAN §1). innerWidth is printed for contrast
only; clientWidth is the number fixed positioning and the scroll container
actually use.

Note on the comparison itself: clientWidth excludes a classic scrollbar, so a
page that grows a vertical scrollbar at one of these settings reports a 15px
narrower clientWidth and can fail for a reason that is not a horizontal offender.
The +1 tolerance does not cover that; the offender list does, because the element
that grew is printed with its overflow. Read the offender line, not just number.

Usage: python3 gate.py [base-url] [--only name,name] [--pages N]
                       [--engine chromium|firefox|webkit|all] [--widths 320,390]
                       [--roots 32,48] [--no-track] [--no-io-stub]
                       (needs the stage server, :8199)
Exit 0 = green, 1 = defect, 2 = the instrument failed and there are no results.

Engines: chromium by default. Firefox matters here for the same reason it
mattered to the sticky bar - DejaVu Sans is wider per character than the
Liberation/Helvetica fallback Chromium picks, and at a 48px root font the wrap
points are exactly what decides whether a line fits (tests/sticky-cta/SHIP.md:
same mechanism, and it made Firefox 18px taller and moved a button a row
earlier). A Chromium-only overflow gate is the kind of instrument that missed
that once already.
"""
import hashlib
import re
import sys
import time

import probe        # same directory: OFFENDERS, SITE, PAGES
import cssregions  # same directory: before_css(), CSS, CSS_URL_PART, REGION_MARKERS
from playwright.sync_api import sync_playwright

WIDTHS_FONTS = [(320, [16, 32, 48]), (390, [16, 32, 48]),
                (768, [16, 32, 48]), (1280, [16, 32, 48])]
HEIGHT = {320: 844, 390: 844, 768: 1024, 1280: 900}
ENGINES = ("chromium", "firefox", "webkit")

# The negative control: one page, one cell, where the defect this change fixes is
# large, named and stable. /tesla-1894-plates carries the widest single-word
# token in the site, and at 390x48 the pre-change navbar brand measured 654px
# wide, +300px, on 53 of 53 pages - so a run whose control comes back green is
# not measuring the thing it claims to be measuring, at any tolerance.
CONTROL_PAGE = "index"
CONTROL_WIDTH, CONTROL_FONT = 390, 48
CONTROL_OFFENDER = "navbar-brand"
CONTROL_MIN_W = 400          # px; the measured value with the CSS cut is ~654

# Installed as an init script, so it exists before any page script runs. Every
# reveal-on-scroll element in the site uses IntersectionObserver, and a stub that
# reports "intersecting" on observe() puts all of them in their revealed state
# with no scrolling and no waiting - including the ones in the middle of a
# 123,000px page, which a single scroll jump does not reliably reveal (and
# crawling a viewport at a time costs 5s a page). This is deliberately
# conservative in one direction: the gate then measures the WORST revealed state,
# not the state at a reader's current scroll position. That is the right
# direction for an overflow gate, and it is why the run prints how many elements
# it revealed: the number is the proof the stub actually applied, because an init
# script that silently did nothing is exactly the failure mode this file has
# already been written twice over to survive.
IO_STUB = """
window.__ioCount = 0;
window.__ioStubbed = true;
window.IntersectionObserver = class {
  constructor(cb) { this.cb = cb; }
  observe(el) {
    window.__ioCount++;
    try { this.cb([{ isIntersecting: true, intersectionRatio: 1, target: el,
                     boundingClientRect: el.getBoundingClientRect(),
                     time: performance.now() }], this); } catch (e) {}
  }
  unobserve() {} disconnect() {} takeRecords() { return []; }
};
"""

# Finish what is animating instead of racing it. `finish()` throws on animations
# with infinite iterations - the sidebar card's `grow` scale cycle is one, and it
# was making scrollWidth vary by the phase it was sampled at - so those are
# paused at a fixed time, which makes them deterministic too. Then fonts, then a
# mutation-quiescence window with a hard bound: if the page will not go quiet,
# that is reported, and a cell that changes between reads is UNSTABLE (see the
# stability re-read in measure_cell).
QUIESCE = """async () => {
  const nudge = () => { window.scrollTo(0, 0); window.scrollTo(0, 200); window.scrollTo(0, 0); };
  nudge();
  for (let i = 0; i < 2; i++) {
    for (const a of document.getAnimations()) {
      try { a.finish(); } catch (e) { try { a.pause(); a.currentTime = 0; } catch (e2) {} }
    }
    await new Promise(r => setTimeout(r, 120));
  }
  nudge();
  try { await document.fonts.ready; } catch (e) {}
  const images = [...document.images];
  const pending = () => images.filter(i => !i.complete).map(i => i.currentSrc || i.src);
  let waits = 0, late = [];
  while (waits++ < 20) {
    late = pending();
    if (!late.length) break;
    await new Promise(r => setTimeout(r, 100));
  }
  let quiet = 0;
  const mu = new MutationObserver(() => { quiet = 0; });
  mu.observe(document.documentElement, {childList: true, subtree: true, attributes: true});
  const deadline = Date.now() + 1500;
  while (Date.now() < deadline && quiet < 3) {
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    quiet++;
  }
  mu.disconnect();
  return { quiesced: quiet >= 3, imagesPending: late.slice(0, 3), reveals: window.__ioCount || 0 };
}"""

# The early read, taken before QUIESCE: the state a reader who has just arrived
# and not yet scrolled is in. A cell that overflows here and not in the settled
# read is TRANSIENT - an animation-state artefact, not a layout defect - and gets
# listed rather than discarded, so the thing the old settle used to hide is
# named in the output instead of trusted away.
EARLY = """() => ({ scrollW: document.documentElement.scrollWidth,
          clientW: document.documentElement.clientWidth })"""

# Everything about the state of the page that a verdict depends on, plus the
# verdict itself, in ONE round trip: reading the root font at t=0 and scrollWidth
# 800ms later pairs a number with a layout state that may no longer exist.
MEASURE = f"""() => {{
  const de = document.documentElement, body = document.body;
  const cs = getComputedStyle(de);
  const rootPx = parseFloat(cs.fontSize);
  const brand = document.querySelector('.navbar-brand') || body;
  const bcs = getComputedStyle(brand);
  const probeEl = document.createElement('div');
  probeEl.style.cssText = 'width:10rem;height:1px;position:absolute;left:-9999px;top:0';
  body.appendChild(probeEl);
  const probeW = probeEl.getBoundingClientRect().width;   // forces layout
  probeEl.remove();
  let fixedClip = [];
  for (const el of document.querySelectorAll('body *')) {{
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' || s.display === 'none' || s.visibility === 'hidden') continue;
    if (el.scrollWidth > el.clientWidth + 1)
      fixedClip.push([el.tagName, String(el.className).slice(0, 24),
                      el.scrollWidth - el.clientWidth, (el.innerText || '').trim().slice(0, 20)]);
  }}
  const off = ({probe.OFFENDERS})()
  return {{ off,
           root: cs.fontSize, rootPx, probeW,
           brandWS: bcs.whiteSpace, brandDisplay: bcs.display,
           bootstrap: cs.getPropertyValue('--bs-body-font-family').trim() !== '',
           reveals: window.__ioCount || 0, stubbed: !!window.__ioStubbed,
           imagesPending: [...document.images].filter(i => !i.complete).length,
           fixedClip: fixedClip.slice(0, 4), fixedClipCount: fixedClip.length,
           viewport: {{ cw: de.clientWidth, iw: innerWidth }} }};
}}"""


class Instrument(Exception):
    """The harness could not establish what it measured. There are no results."""


def selectors(css):
    """Top-level selector lists of a stylesheet, best effort but good enough to
    prove that cutting a region out of a stylesheet removed rules and left the
    rest of the file structurally intact (balanced braces, no empty rule)."""
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if body.count("{") != body.count("}"):
        raise Instrument(f"stylesheet is not brace-balanced: {body.count('{')} open "
                         f"vs {body.count('}')} close")
    return [s.strip() for s in re.findall(r"}\s*([^{}@]+?)\s*\{", "}" + body)
            if s.strip() and not s.strip().startswith("@")]


def payload_proof(after, before):
    """Print the two payloads' identity and prove they differ the way this change
    claims, so a 'before' that is red because it is malformed, or two payloads
    that are secretly the same file, cannot produce a number."""
    ha, hb = hashlib.sha256(after.encode()).hexdigest()[:12], hashlib.sha256(before.encode()).hexdigest()[:12]
    sa, sb = set(selectors(after)), set(selectors(before))
    removed, added = sorted(sb - sa), sorted(sa - sb)
    print(f"payloads: shipped {ha} ({len(after)} bytes, {len(sa)} rule sets) | "
          f"cut {hb} ({len(before)} bytes, {len(sb)} rule sets) | identical: {ha == hb}")
    print(f"  rules present only in shipped: {added or 'none'}")
    print(f"  rules present only in cut    : {removed or 'none'}")
    if ha == hb:
        raise Instrument("the two payloads are byte-identical; there is no before/after pair")
    if len(after) - len(before) < 4000:
        raise Instrument(f"the cut removed only {len(after) - len(before)} bytes; item 7's "
                         f"regions are ~22KB, so the cut is not doing what the label says")
    if not added:
        raise Instrument("the shipped payload adds no rule sets over the cut one; the "
                         "comparison would be measuring the same stylesheet twice")
    return ha, hb


def route_font(c, font, label):
    """Register the root-font injection on a context, and return a counter the
    caller asserts was non-zero. Used by the matrix AND the negative control,
    because a control that forgets it measures 16px rendering and comes back
    green - which is precisely the bug the control exists to catch, and the first
    version of this control did exactly that."""
    inject = (f"<style>html{{font-size:{font}px !important}}"
              f"/* gate.py root font under test */</style>")
    seen = {"n": 0}

    def serve(route):
        try:
            resp = route.fetch()
            body = resp.text()
            if "</head>" not in body:
                raise Instrument(f"{route.request.url} has no </head>; the root font could "
                                 f"not be injected")
            seen["n"] += 1
            body = body.replace("</head>", inject + "</head>", 1)
            route.fulfill(status=resp.status,
                          headers={"content-type": "text/html; charset=utf-8"}, body=body)
        except Exception as exc:                                            # noqa: BLE001
            print(f"\nINSTRUMENT FAILED: root-font injection failed for "
                  f"{route.request.url}: {exc}\nNO RESULTS.")
            raise

    c.route("**/*.html", serve)
    return seen


def control(pw, engine, base, after_css, before_css, flavour):
    """One page, one cell, the payload flipped: the run's dynamic-range proof.
    Returns the offender width it saw, so the run line can carry the number."""
    ctx_css = after_css if flavour == "shipped-in-before-run" else before_css
    want_red = flavour == "shipped-run"
    b = getattr(pw, engine).launch()
    try:
        c = b.new_context(viewport={"width": CONTROL_WIDTH, "height": HEIGHT[CONTROL_WIDTH]})
        served = {"n": 0}

        def cut(route):
            served["n"] += 1
            try:
                route.fulfill(status=200, content_type="text/css", body=ctx_css)
            except Exception:                                       # noqa: BLE001
                pass

        c.route("**" + cssregions.CSS_URL_PART, cut)
        seen = route_font(c, CONTROL_FONT, "control")
        pg = c.new_page()
        pg.goto(f"{base}/{CONTROL_PAGE}.html", wait_until="load", timeout=60000)
        if seen["n"] == 0:
            raise Instrument(f"{engine} negative control: the root-font injection route never "
                             f"fired, so the control measured 16px rendering - the exact bug "
                             f"this gate was rewritten to catch")
        pg.evaluate(QUIESCE)
        m = pg.evaluate(MEASURE)
        over = m["off"]["scrollW"] - m["off"]["clientW"]
        widest = next((o["w"] for o in m["off"]["offenders"] if CONTROL_OFFENDER in o["sel"]), 0)
        c.close()
    finally:
        b.close()
    if served["n"] == 0:
        raise Instrument(f"{engine} negative control: the stylesheet route never fired, "
                         f"so the control measured the on-disk CSS and proves nothing")
    if want_red and (over <= 1 or widest < CONTROL_MIN_W):
        raise Instrument(
            f"{engine} negative control FAILED: {CONTROL_PAGE} @ {CONTROL_WIDTH}px root "
            f"{CONTROL_FONT}px served with item 7's CSS cut out came back with "
            f"scrollWidth over by {over}px and {CONTROL_OFFENDER} at {widest}px. This gate "
            f"cannot tell a fixed page from an unmeasured one, so its verdict on the other "
            f"{len(probe.PAGES)} pages means nothing.")
    if not want_red and over > 1:
        raise Instrument(
            f"{engine} negative control FAILED: {CONTROL_PAGE} @ {CONTROL_WIDTH}px root "
            f"{CONTROL_FONT}px served with the SHIPPED CSS came back with +{over}px inside a "
            f"run labelled BEFORE, so the interception is not serving what the label says.")
    return widest, over


def measure_cell(pg):
    """Navigate-ready page -> (verdict dict, early read). Raises Instrument."""
    early = pg.evaluate(EARLY)
    q = pg.evaluate(QUIESCE)
    m = pg.evaluate(MEASURE)
    if not m["stubbed"]:
        raise Instrument("the IntersectionObserver stub is not on the page, so nothing was "
                         "revealed and every reveal-on-scroll element was measured hidden")
    if m["probeW"] < 0.98 * 10 * m["rootPx"] or m["probeW"] > 1.02 * 10 * m["rootPx"]:
        raise Instrument(f"the 10rem dimension probe measured {m['probeW']:.1f}px at a computed "
                         f"root of {m['root']}: the layout engine is not laying out at that size")
    if not m["bootstrap"]:
        raise Instrument("Bootstrap is not applied (--bs-body-font-family is absent). An "
                         "unstyled page never overflows, so every cell would read green.")
    if m["brandDisplay"] in ("inline", ""):
        raise Instrument(".navbar-brand computes to display:inline: the site's stylesheet is "
                         "not being applied, so this page cannot overflow")
    # Stability: the same read twice. An unstable cell that happened to look green
    # is the same failure class as the two this file documents, wearing better
    # manners, and the sticky bar and the sidebar spinner have both already made
    # geometry nondeterministic on this site. The gap is a sample rather than a
    # wait - by here every animation is finished or paused, so anything still
    # moving a box is a page that cannot be measured, not a page that is slow.
    time.sleep(0.15)
    again = pg.evaluate(MEASURE)["off"]
    if (again["scrollW"], again["clientW"]) != (m["off"]["scrollW"], m["off"]["clientW"]):
        raise Instrument(f"UNSTABLE: scrollWidth/clientWidth moved between two reads "
                         f"({m['off']['scrollW']}/{m['off']['clientW']} -> "
                         f"{again['scrollW']}/{again['clientW']}); a cell that wobbles cannot "
                         f"be scored green")
    m["quiesced"] = q["quiesced"]
    m["imagesPending"] = max(m["imagesPending"], len(q["imagesPending"]))
    m["early"] = early
    return m, q


def main():
    base = "http://127.0.0.1:8199"
    args = [a for a in sys.argv[1:]]

    def flag(name, default=None, cast=str):
        if name in args:
            i = args.index(name)
            val = cast(args[i + 1])
            del args[i:i + 2]
            return val
        return default

    before = "--before-css" in args
    if before:
        args.remove("--before-css")
    no_track = "--no-track" in args
    if no_track:
        args.remove("--no-track")
    no_io = "--no-io-stub" in args
    if no_io:
        args.remove("--no-io-stub")
    limit = flag("--pages", 0, int)
    only = flag("--only")
    only = set(only.split(",")) if only else None
    eng = flag("--engine", "chromium")
    widths_sel = flag("--widths")
    roots_sel = flag("--roots")
    if args:
        base = args[0].rstrip("/")

    widths = list(WIDTHS_FONTS)
    if widths_sel:
        keep = {int(x) for x in widths_sel.split(",")}
        widths = [(w, fs) for w, fs in widths if w in keep]
    if roots_sel:
        keep = {int(x) for x in roots_sel.split(",")}
        widths = [(w, [f for f in fs if f in keep]) for w, fs in widths]
        widths = [(w, fs) for w, fs in widths if fs]
    if not widths:
        sys.exit("--widths x --roots selected no cells")
    engines = list(ENGINES) if eng == "all" else eng.split(",")
    bad = [e for e in engines if e not in ENGINES]
    if bad:
        sys.exit(f"--engine: unknown {bad}; valid: {', '.join(ENGINES)}, or all")

    pages = probe.PAGES if not limit else probe.PAGES[:limit]
    # 404.html is skipped by probe.py's page list but is a real page with the
    # same navbar, so the gate covers it too.
    pages = pages + (["404"] if "404" not in pages else [])
    if only is not None:
        pages = [p for p in pages if p in only]
        if not pages:
            sys.exit(f"--only matched no page (try one of {probe.PAGES[:5]} ...)")

    after_css = open(cssregions.CSS, encoding="utf-8").read()
    before_css = cssregions.before_css() if before else None
    hashes = payload_proof(after_css, before_css) if before else (
        hashlib.sha256(after_css.encode()).hexdigest()[:12], None)
    flavour = "before-run" if before else "shipped-run"
    print(f"flavour: {flavour} | served CSS per cell: "
          f"{'the CUT payload (item 7 regions removed)' if before else 'the on-disk CSS, unrouted'}")

    fails, transient, unstable_note, checked, quiesced_n, fixed_clip = [], [], 0, 0, 0, 0
    # Cells that pass only because of the 1px float tolerance. The reviewer's rule on
    # 2026-11-19: "a 331-of-320 pass is a second defect hiding behind the tolerance",
    # which is fair, and the answer is not to drop the tolerance (sub-pixel rounding is
    # real and this gate has already burned a run on it) - it is to never let it be
    # silent. Counted here, printed in the summary, so a fix that leaves a 1px leak is
    # visible in the artefact instead of living inside a green verdict.
    near_miss = []
    controls = {}
    with sync_playwright() as pw:
        for engine in engines:
            # The control runs first and per engine: an engine whose control is
            # green has no results worth collecting, and burning 636 navigations
            # to find that out at the end is how the last three runs got wasted.
            controls[engine] = control(pw, engine, base, after_css, before_css,
                                       "shipped-in-before-run" if before else "shipped-run")
            b = getattr(pw, engine).launch()
            for width, fonts in widths:
                for font in fonts:
                    for p in pages:
                        # One context per cell: a style tag or route registered on a
                        # context that is reused leaks into the next cell, which is
                        # how a 48px run once measured the next 16px run at 48px
                        # through an invisible override.
                        #
                        # If the engine's process died, relaunch and carry on: webkit's
                        # page process takes itself out on these pages at a 48px root on
                        # a box with 1.9GB free, and a matrix that stops dead at cell 1
                        # measures nothing. What keeps this honest is the arithmetic at
                        # the end - `checked != expected` is an instrument failure with
                        # the shortfall named - so a relaunch costs a cell that has to be
                        # re-run, never a silent gap inside a green-looking denominator.
                        if not b.is_connected():
                            print(f"  relaunching {engine} before {p}: its process died. Any "
                                  f"cell lost to that death is missing from `checked`, and "
                                  f"the run cannot call that a pass.")
                            b = getattr(pw, engine).launch()
                        c = b.new_context(viewport={"width": width, "height": HEIGHT.get(width, 900)})
                        if before:
                            # Same gate, same matrix, stylesheet without the two regions
                            # this change added: the before/after pair is then the same
                            # instrument run twice, not two instruments, which is the only
                            # version of this number worth quoting.
                            served = {"n": 0}

                            def cut(route):
                                served["n"] += 1
                                try:      # the page may close mid-request; see inert-at-100.py
                                    route.fulfill(status=200, content_type="text/css", body=before_css)
                                except Exception:                                       # noqa: BLE001
                                    pass

                            c.route("**" + cssregions.CSS_URL_PART, cut)
                        pg = c.new_page()
                        if not no_io:
                            pg.add_init_script(IO_STUB)
                        # The root font goes into the navigation response itself.
                        # Three obvious ways of doing this are each wrong in a way
                        # that reports success, and one of them cost a whole day:
                        #   * add_style_tag() BEFORE goto() does not survive the
                        #     navigation (measured: computed root stays 16px), so
                        #     every 32px/48px cell silently measures 16px;
                        #   * add_init_script() runs at document-start, where
                        #     document.documentElement is null - the script throws
                        #     and Playwright does not mention it;
                        #   * add_style_tag() AFTER load works but lays the page out
                        #     twice, and the second pass restarts the widget's
                        #     entrance animation, which is what produced the
                        #     phantom +75px overflow this file now classifies
                        #     instead of hiding.
                        # Inline in <head> is one layout pass, at the size under
                        # test, before first paint - and the dimension probe reads
                        # it back rather than assuming it landed.
                        injected = route_font(c, font, p)
                        try:
                            r = None
                            for attempt in (1, 2):
                                try:
                                    r = pg.goto(f"{base}/{p}.html", wait_until="load",
                                                 timeout=60000)
                                    break
                                except Exception as exc:                                   # noqa: BLE001
                                    # Firefox on a loaded box takes well over 30s for
                                    # one of these pages; one attempt turns a slow
                                    # engine into a fake failure that looks like a CSS bug.
                                    if attempt == 2:
                                        raise
                                    print(f"  retry {p} @ {width}px root {font} "
                                          f"({str(exc).splitlines()[0][:60]})")
                            # WHY THIS CHECK EXISTS, and it is not paranoia: the page
                            # list comes from the working tree (probe.PAGES lists SITE)
                            # while the tree being served is built separately, so a page
                            # that exists in one and not the other is a standing
                            # possibility. http.server answers such a request with a 404
                            # body of its own, whose width fits any viewport, so every
                            # cell for a missing page came back green. The injection and
                            # CSS-route checks below prove a navigation happened; only the
                            # status proves what was actually measured. Found while
                            # measuring the February 1919 page, which had never been in a
                            # served tree at all.
                            if r is None or r.status != 200:
                                raise Instrument(
                                    f"{p} @ {width}px root {font}px: {base}/{p}.html answered "
                                    f"HTTP {getattr(r, 'status', None)} - this cell would have "
                                    f"measured a 404 page, not {p}.html")
                            if injected["n"] == 0:
                                raise Instrument(f"{p} @ {width}px: the injection route never "
                                                 f"fired for this navigation, so the root font "
                                                 f"is whatever the file on disk says")
                            if before and served["n"] == 0:
                                raise Instrument(f"{p} @ {width}px: the CSS route never fired, "
                                                 f"so a run labelled BEFORE measured the shipped "
                                                 f"stylesheet")
                            m, q = measure_cell(pg)
                        except Instrument as exc:
                            print(f"\nINSTRUMENT FAILED [{engine} {p} @ {width}px root {font}px]: "
                                  f"{exc}\nNO RESULTS. Anything printed above this line is "
                                  f"void, including any FAIL lines: a broken harness is not a "
                                  f"defect report.")
                            c.close(); b.close()
                            sys.exit(2)
                        except Exception as exc:                                    # noqa: BLE001
                            # The engine's page process died inside this cell. That is
                            # neither a pass nor a defect: it is a cell this harness never
                            # measured. Counted and named, so the arithmetic at the bottom
                            # (checked != expected) is what stops the run calling itself a
                            # complete matrix - a lost cell can only ever surface as a
                            # shortfall, never as silence.
                            lost += 1
                            lost_where.append(f"{engine} {p} @ {width}px root {font}px: "
                                              f"{str(exc).splitlines()[0][:70]}")
                            print(f"LOST  {engine[:4]} {p} @ {width}px root {font}px: engine "
                                  f"process gone ({str(exc).splitlines()[0][:70]}); the next "
                                  f"cell relaunches")
                            continue
                        finally:
                            try:
                                c.close()
                            except Exception:                                              # noqa: BLE001
                                pass
                        if m["brandWS"] != ("nowrap" if before else "normal"):
                            print(f"\nINSTRUMENT FAILED [{engine} {p} @ {width}px root {font}px]: "
                                  f".navbar-brand renders white-space:{m['brandWS']}, expected "
                                  f"{'nowrap' if before else 'normal'} for the "
                                  f"{'BEFORE' if before else 'SHIPPED'} payload - the route "
                                  f"interception is not doing what the label says.\nNO RESULTS.")
                            b.close()
                            sys.exit(2)
                        checked += 1
                        quiesced_n += 1 if m["quiesced"] else 0
                        fixed_clip += m["fixedClipCount"]
                        over = m["off"]["scrollW"] - m["off"]["clientW"]
                        if over == 1:
                            near_miss.append(f"{engine[:4]} {p}@{width}x{font}")
                        early_over = m["early"]["scrollW"] - m["early"]["clientW"]
                        if not no_track:
                            if over <= 1 and early_over > 1:
                                transient.append((engine, width, font, p, early_over))
                        if over > 1:
                            fails.append((engine, width, font, p, m))
                            print(f"FAIL  {engine[:4]} {p} @ {width}px root {font}px: "
                                  f"scrollWidth {m['off']['scrollW']} > clientWidth "
                                  f"{m['off']['clientW']} (+{over}); innerWidth={m['viewport']['iw']}")
                            for o in m["off"]["offenders"]:
                                print(f"        +{o['over']:4} w={o['w']:4} {o['sel'][:46]:46} "
                                      f"{o['text'][:30]!r}")
                            if not any(o["over"] > 1 for o in m["off"]["offenders"]):
                                # scrollWidth grew but nothing survived OFFENDERS' two
                                # filters: ask the unfiltered sweep instead (zero-size and
                                # clipped boxes, elements outside <body>).
                                #
                                # Best effort, and it has to be said why, with the real cost
                                # rather than the one this comment used to claim (it said
                                # "client rects and every Range rect"; there are no Ranges and
                                # no rect arrays here, and the next person sizes this sweep from
                                # that sentence, so it gets the truth). On webkit the sweep is
                                # the heaviest thing this file asks a page to do: one
                                # getBoundingClientRect and one getComputedStyle for every
                                # element in `body *`, then for each survivor an ancestor walk
                                # of up to eight further getComputedStyle calls plus innerText,
                                # which flushes layout and serialises text. Tens of thousands
                                # of style resolutions on a 15,000px page at a 48px root, in a
                                # renderer with no memory to hand back, and under that pressure
                                # it takes the page process with it: four chunked webkit runs
                                # it takes the page process with it: four chunked webkit runs
                                # today died at this line, on the first failing cell, each
                                # one leaving the same 2KB artefact and a verdict of nothing
                                # at all, because one diagnostic call could end the matrix.
                                # The cell's own verdict was already in hand by then, which
                                # is the only reason this is a fix and not a workaround.
                                try:
                                    w = pg.evaluate(probe.WORST)
                                except Exception as exc:                            # noqa: BLE001
                                    print(f"        unfiltered sweep unavailable: "
                                          f"{str(exc).splitlines()[0][:90]} - the cell's "
                                          f"verdict stands, the diagnosis is lost")
                                    continue
                                print("        unfiltered (zero-size / clipped / outside body):")
                                for o in w["list"][:6]:
                                    print(f"        +{o['over']:4} {o['w']:4}x{o['h']:<4} "
                                          f"L{o['left']:6} ink={o['ink']:4} {o['sel'][:34]:34} "
                                          f"pos={o['pos']:9} disp={o['disp']:10} "
                                          f"clip={o['clipper'] or '-':20} {o['text'][:24]!r}")
                                if w["outsideBody"]:
                                    print(f"        children of <html> outside <body>: {w['outsideBody']}")
            b.close()

    # ---- two-phase output: nothing above this line is a verdict. --------------
    cells = [f"{w}px x {f}px" for w, fs in widths for f in fs]
    expected = len(engines) * len(pages) * len(cells)
    if checked != expected:
        print(f"\nINSTRUMENT FAILED: {checked} rows measured, matrix says {expected} "
              f"({len(engines)} engines x {len(pages)} pages x {len(cells)} cells). "
              f"A skipped page shrinks the denominator and the summary still reads "
              f"like a full matrix.\nNO RESULTS.")
        sys.exit(2)
    ctl = " | ".join(f"{e}: cut-CSS {CONTROL_PAGE}@{CONTROL_WIDTH}x{CONTROL_FONT}px "
                     f"over by {o}px, {CONTROL_OFFENDER} {w}px"
                     + ("" if before else " (red as it must be)")
                     + (" (green as it must be)" if before else "")
                     for e, (w, o) in controls.items())
    print(f"\nnegative control: {ctl}")
    print(f"canaries (read in the same evaluate as the verdict, all {checked} cells): "
          f"root font read back, 10rem dimension probe, Bootstrap applied, "
          f"{CONTROL_OFFENDER} white-space per flavour | "
          f"payload hashes {hashes[0]}/{hashes[1] or 'n/a'}")
    print(f"reveals forced by the IntersectionObserver stub: "
          f"{'off (--no-io-stub)' if no_io else 'on'} | cells quiesced: {quiesced_n} of {checked}"
          f" | fixed subtrees clipping their own content: {fixed_clip} "
          f"(invisible to documentElement.scrollWidth; see the module docstring)")
    print(f"cells green only because of the 1px tolerance: {len(near_miss)}"
          + ("" if not near_miss else " (" + ", ".join(near_miss[:8])
             + (" ...)" if len(near_miss) > 8 else ")"))
          + " | 0 means every green cell reads scrollWidth == clientWidth exactly")
    if transient and not no_track:
        print(f"TRANSIENT (overflowed at first paint, clean once settled - animation state, "
              f"not layout; {len(transient)} cells): "
              + ", ".join(f"{p}@{w}/{f}" for e, w, f, p, o in transient[:8])
              + (" ..." if len(transient) > 8 else ""))
    print(f"\n{checked - len(fails)} of {checked} engine x page x viewport x root-font "
          f"combinations green  ({len(pages)} pages x {len(cells)} cells [{', '.join(cells)}] "
          f"x engines {engines})")
    if fails:
        by = {}
        for e, w, f, p, m in fails:
            by.setdefault((e, w, f), []).append(p)
        for (e, w, f), names in sorted(by.items()):
            print(f"   {e} @ {w}px root {f}px: {len(names)} pages, e.g. {', '.join(names[:4])}")
        print(f"FAIL: {len(fails)} combinations still scroll sideways. Fix the elements above; "
              f"do NOT put overflow-x:hidden on html/body (PLAN \u00a74).")
        sys.exit(1)
    print("OK: no horizontal scroll at 200% or 300% root font, and none at 320px "
          "(WCAG 1.4.4 / 1.4.10).")


if __name__ == "__main__":
    main()
