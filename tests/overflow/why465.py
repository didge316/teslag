#!/usr/bin/env python3
"""Why does WebKit report documentElement.scrollWidth == 465 on 49 pages?

The gate (gate.py) came back 81 of 624 red on webkit only, and the reds have one
shape: scrollWidth 465 at a 320px viewport (+145) AND at a 390px viewport (+75),
at root 48px only, never at 16 or 32px, never at 768/1280, and zero reds in
chromium and firefox on the identical tree. A right edge that does not move when
the viewport moves is one cause, not 49.

What the static tree says before any browser is asked (all of this is `grep`, and
it is the claim this script exists to test rather than to confirm):

  * 50 of the 52 pages load js/exit-popup.js. The two that do not are `404` and
    `privacy`, and neither is red. 49 of the 50 loaders ARE red; the one loader
    that is not red is `articles`. Red-ness tracks that script exactly, and
    nothing else about those pages explains it.
  * exit-popup.js injects `position:fixed; inset:0; display:flex` with a panel of
    `max-width:420px; width:100%; padding:24px 22px` and a bot honeypot inside
    `<div aria-hidden="true" style="position:absolute;left:-9999px;top:-9999px">`.
  * It shows "once per browser session, on exit intent (pointer leaves the top of
    the viewport) or after DWELL_MS = 25000 of reading as a fallback". Every gate
    cell is a fresh context, so sessionStorage is empty and the dwell is the only
    trigger that can fire - which means a cell whose page stays open longer than
    25 seconds measures a page with a revealed popup in it, and a cell that
    finishes faster does not. WebKit on this box is the slow engine.

So there are two candidate stories and they need different fixes:
  (i)  the popup, revealed mid-measurement, owns the 465px - in which case those
       81 cells measured a page state no reader is in, and the instrument has to
       say which state it measured (and the dwell needs pinning);
  (ii) the popup's DOM genuinely overflows at 300% in WebKit and does not in
       Blink, in which case item 7 is incomplete on 50 of 52 pages.

The measurement that separates them, in this order, and each one asserts it is
still looking at the same page it reproduced before it is allowed to say anything:

  1. can the document actually be scrolled right (scrollX after scrollTo(1000,0));
  2. which box is reporting the 465 (documentElement vs body vs the de rect);
  3. is the popup in the DOM, is it revealed, what is its geometry;
  4. bisect <body>'s children by display:none - O(children), no getComputedStyle
     in the loop - to name the subtree that owns the number;
  5. the widest-right element inside that subtree, then its computed styles.

It imports the instrument from gate.py rather than reimplementing it: the same
`route_font` injection (root font inline in the navigation response, the only
mechanism measured to survive navigation), the same `IO_STUB`, the same `QUIESCE`
and the same `measure_cell`, so the numbers below are comparable with the matrix
line for line instead of being "close". --suppress-popup re-runs the same cells
with the popup's own session flag pre-set, which is the paired half: same
instrument, one flag, and the popup cannot appear.

Usage:
  ./why465.py                                   # the reproduced default cell, webkit
  ./why465.py http://127.0.0.1:8200 --page about --width 320 --font 48
  ./why465.py --pages about,articles --suppress-popup   # paired half, per page
  ./why465.py --engine chromium                 # the same probe where it is green
"""
import sys

from playwright.sync_api import sync_playwright

import gate   # the instrument: route_font, measure_cell, QUIESCE, IO_STUB, HEIGHT

BASE = "http://127.0.0.1:8200"
SESSION_FLAG = "tesla_exit_popup_shown"   # exit-popup.js: 'true' == already shown, never shows again

# Runs at document-start, where document.documentElement is null but the origin's
# sessionStorage is not: this is the popup's own "shown once per session" test,
# set before its script runs, so nothing about the site is edited to suppress it.
SUPPRESS_POPUP = f"""
try {{ sessionStorage.setItem({SESSION_FLAG!r}, 'true'); }} catch (e) {{ /* private mode */ }}
"""

STATE = """() => {
  const de = document.documentElement;
  const box = (sel) => {
    const el = document.querySelector(sel);
    if (!el) return 'absent';
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    return { w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right),
             top: Math.round(r.top), display: cs.display, visibility: cs.visibility,
             opacity: cs.opacity, position: cs.position, zIndex: cs.zIndex,
             maxW: cs.maxWidth, minW: cs.minWidth, boxSizing: cs.boxSizing,
             overflowX: cs.overflowX };
  };
  const hp = [...document.querySelectorAll('div')]
    .filter((d) => typeof d.className === 'string' && d.className.includes('emailoctopus-form-row-hp'))
    .map((d) => {
      const r = d.getBoundingClientRect(), cs = getComputedStyle(d);
      return { w: Math.round(r.width), left: Math.round(r.left), right: Math.round(r.right),
               position: cs.position, inEoForm: !!d.closest('.eo-form'),
               inPopup: !!d.closest('.tesla-popup'),
               parent: d.parentElement ? (d.parentElement.className || d.parentElement.tagName) : null };
    });
  return {
    scrollWidthDE: de.scrollWidth, scrollWidthBody: document.body.scrollWidth,
    deRectW: Math.round(de.getBoundingClientRect().width),
    clientWidth: de.clientWidth, innerWidth: window.innerWidth,
    scrollingElementIsDE: document.scrollingElement === de,
    popup: box('.tesla-popup'), panel: box('.tesla-popup__panel'), honeypots: hp,
    popupFlagInSession: (() => { try { return sessionStorage.getItem(%r); } catch (e) { return 'unreadable'; } })(),
    bodyChildren: [...document.body.children].map((c) => c.tagName + '.' + String(c.className || '').split(' ')[0]),
  };
}""" % SESSION_FLAG

# Hermes' decisive single measurement: if the document cannot be scrolled right,
# nothing a reader can reach is off-screen and the verdict line is describing a
# box, not a defect.
SCROLL_RIGHT = """async () => {
  const raf = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  window.scrollTo(0, 0); await raf();
  const before = window.scrollX;
  window.scrollTo(1000, 0); await raf();
  const after = window.scrollX;
  const maxX = window.scrollX;
  window.scrollTo(0, 0); await raf();
  return { scrollXAfterScrollTo1000: after, scrollXBefore: before, reachedX: maxX };
}"""

# One pass over <body>'s children, hiding each in turn. O(children), no
# getComputedStyle, and every hide is reverted and the number re-read.
BISECT = """() => {
  const de = document.documentElement, out = [];
  const base = de.scrollWidth;
  [...document.body.children].forEach((el, i) => {
    const prev = el.style.display;
    // A script or a style is display:none from the UA sheet, so "did it come back"
    // has to be measured against how it started, not against "not none".
    const wasHidden = getComputedStyle(el).display === 'none';
    el.style.display = 'none';
    const w = de.scrollWidth;
    el.style.display = prev;
    const back = de.scrollWidth;
    const restored = wasHidden || getComputedStyle(el).display !== 'none';
    if (!restored || back !== base) {
      out.push({ warn: `${el.tagName}: restored display=${getComputedStyle(el).display} `
               + `scrollWidth ${base} -> ${w} -> ${back}` });
    }
    if (w !== base) out.push({ i, tag: el.tagName, cls: String(el.className || '').split(' ').slice(0, 2).join('.'), scrollWidth: w });
  });
  return { base: base, changed: out };
}"""

# Contribution, all the way down. A rect sweep came back empty while hiding the
# container moved the number, which is the signature of overflow that has no
# border box of its own: an inline run wider than its line box, or a margin.
# So bisect by hiding instead of by measuring rects: at each level hide each child
# in turn, re-read documentElement.scrollWidth, and descend into whichever child
# lowers it, until no single child does. That leaf is where the contribution
# lives, and at that point it is cheap to be expensive about it: computed styles,
# the Range rect of every text node, and every candidate fix applied and reverted
# in place, each with the number read before and after. No getComputedStyle in the
# descent loop, because the last sweep died in the renderer and not in the logic.
DESCEND = """() => {
  const de = document.documentElement, sw = () => de.scrollWidth;
  const name = (el) => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
    ? '.' + el.className.trim().split(/\\s+/).slice(0, 3).join('.') : '');
  const path = [];
  let lastEffects = [];
  let node = document.body;
  for (let hop = 0; hop < 30; hop++) {
    const withNode = sw();
    const effects = [];
    let worst = null;
    for (const k of [...node.children]) {
      const prev = k.style.display;
      k.style.display = 'none';
      const w = sw();
      k.style.display = prev;
      effects.push({ sel: name(k).slice(0, 34), without: w });
      if (w < withNode && (!worst || w < worst.w)) worst = { k: k, w: w };
    }
    if (!worst) { lastEffects = effects; break; }
    path.push({ hop: hop, via: name(worst.k), without: worst.w, with: withNode });
    node = worst.k;
  }
  const cs = getComputedStyle(node), r = node.getBoundingClientRect();
  const texts = [];
  for (const c of node.childNodes) {
    if (c.nodeType === 3 && c.textContent.trim()) {
      const rg = document.createRange(); rg.selectNodeContents(c);
      const rr = rg.getBoundingClientRect();
      texts.push({ left: Math.round(rr.left), right: Math.round(rr.right),
                   w: Math.round(rr.width), text: c.textContent.trim().slice(0, 60) });
    }
  }
  const kids = [...node.children].map((k) => {
    const kr = k.getBoundingClientRect();
    return { sel: name(k).slice(0, 40), left: Math.round(kr.left), right: Math.round(kr.right),
             w: Math.round(kr.width), scrollW: k.scrollWidth, clientW: k.clientWidth };
  });
  const iv = [];
  const probeFix = (label, css) => {
    const before = sw();
    const saved = {};
    for (const prop in css) { saved[prop] = node.style.getPropertyValue(prop); node.style.setProperty(prop, css[prop], 'important'); }
    const after = sw();
    for (const prop in css) { node.style.setProperty(prop, saved[prop]); }
    iv.push({ label: label, before: before, after: after });
  };
  probeFix('overflow-wrap:anywhere', { 'overflow-wrap': 'anywhere' });
  probeFix('word-break:break-all', { 'word-break': 'break-all' });
  probeFix('white-space:normal', { 'white-space': 'normal' });
  probeFix('width:100%;max-width:100%', { 'width': '100%', 'max-width': '100%' });
  probeFix('min-width:0', { 'min-width': '0' });
  probeFix('position:static', { 'position': 'static' });
  probeFix('float:none', { 'float': 'none' });
  return {
    scrollWidth: sw(), clientWidth: de.clientWidth,
    path: path, lastEffects: lastEffects.slice(0, 10),
    leaf: { sel: name(node), html: node.outerHTML.slice(0, 240),
            left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width),
            scrollW: node.scrollWidth, clientW: node.clientWidth,
            position: cs.position, display: cs.display, whiteSpace: cs.whiteSpace,
            overflowX: cs.overflowX, overflowWrap: cs.overflowWrap, wordBreak: cs.wordBreak,
            width: cs.width, maxWidth: cs.maxWidth, minWidth: cs.minWidth,
            marginLeft: cs.marginLeft, marginRight: cs.marginRight, float: cs.float,
            fontSize: cs.fontSize, fontFamily: cs.fontFamily.slice(0, 30) },
    texts: texts.slice(0, 6), kids: kids.slice(0, 8), fixes: iv,
  };
}"""

# Widest right edge in the document. Rects only - no getComputedStyle in the loop,
# because the last sweep we ran died in the renderer, not in the logic. The depth
# cap here is 40 and the node budget is generous on purpose: the first version of
# this walk stopped at depth 12, which on this site is *above* the EmailOctopus
# form rows, so it reported "no box crosses the viewport line" on a page whose
# whole overflow lives three levels deeper. A sweep that silently misses the
# culprit is worse than one that crashes, because it argues for a conclusion.
WIDEST = """() => {
  const vw = document.documentElement.clientWidth;
  const rows = [], self = [];
  let seen = 0, truncated = false;
  const walk = (el, depth) => {
    if (seen > 6000) { truncated = true; return; }
    seen++;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      rows.push({ depth, sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
                    ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.') : ''),
                  left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width),
                  over: Math.round(r.right - vw), cls: String(el.className || '').slice(0, 40) });
    }
    if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX === 'visible') {
      self.push({ depth, sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
                    ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.') : ''),
                  scrollW: el.scrollWidth, clientW: el.clientWidth });
    }
    if (depth < 40) for (const c of el.children) walk(c, depth + 1);
  };
  walk(document.body, 0);
  rows.sort((a, b) => b.right - a.right);
  self.sort((a, b) => (b.scrollW - b.clientW) - (a.scrollW - a.clientW));
  return { vw: vw, scrollWidth: document.documentElement.scrollWidth, seen: seen,
           truncated: truncated, top: rows.slice(0, 12), selfOverflowing: self.slice(0, 8) };
}"""

# Kill it and see whether the number goes away: the popup root hidden, the panel
# only, the honeypot only. Reverted after each, and the number re-read each time.
EXPERIMENTS = """() => {
  const de = document.documentElement;
  const read = () => de.scrollWidth;
  const tryIt = (label, sel) => {
    const els = [...document.querySelectorAll(sel)];
    if (!els.length) return { label, hit: 0, scrollWidth: read() };
    const prev = els.map((e) => e.style.display);
    els.forEach((e) => { e.style.display = 'none'; });
    const w = read();
    els.forEach((e, i) => { e.style.display = prev[i]; });
    return { label, hit: els.length, scrollWidth: w };
  };
  const base = read();
  const out = [base,
    tryIt('hide .eo-form', '.eo-form'),
    tryIt('hide form.emailoctopus-form', 'form.emailoctopus-form'),
    tryIt('hide .emailoctopus-form-wrapper', '.emailoctopus-form-wrapper'),
    tryIt('hide .scarcity-widget', '.scarcity-widget'),
    tryIt('hide .tesla-popup', '.tesla-popup'),
    tryIt('hide .tesla-popup__panel', '.tesla-popup__panel'),
    tryIt('hide div.emailoctopus-form-row-hp', 'div.emailoctopus-form-row-hp'),
    tryIt('hide .eo-form + .scarcity-widget', '.eo-form, .scarcity-widget'),
    read()];
  return { base: base, after: out[5], steps: out.slice(1, 5) };
}"""


# Name the ink overflow, deepest-first, and try the fixes on it.
# A rect sweep cannot see this class at all: the box is a normal width and sits
# well inside the viewport, but its text is wider than the box, `overflow-x` is
# visible, and that ink escapes through every visible ancestor into the page's
# scrollable area. So rank elements by how far their ink actually lands
# (rect.right + scrollWidth - clientWidth), name the furthest, print the chain
# that is letting it escape, then apply each candidate fix to that element and
# re-read documentElement.scrollWidth - which of them collapses the number is the
# fix, and on which element it has to live.
INK = """() => {
  const de = document.documentElement, vw = de.clientWidth;
  let best = null, seen = 0, truncated = false;
  const nm = (el) => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
    ? '.' + el.className.trim().split(/\\s+/).slice(0, 3).join('.') : '');
  for (const el of document.querySelectorAll('body *')) {
    if (++seen > 6000) { truncated = true; break; }
    if (el.scrollWidth - el.clientWidth <= 1) continue;
    if (getComputedStyle(el).overflowX !== 'visible') continue;
    const r = el.getBoundingClientRect();
    const spill = el.scrollWidth - el.clientWidth;
    const reach = Math.round(r.right + spill);
    if (!best || reach > best.reach) best = { el, reach, spill, r };
  }
  if (!best) return { seen, truncated, none: true };
  const chain = [];
  for (let n = best.el; n && n !== document.body; n = n.parentElement) {
    const cs = getComputedStyle(n), r = n.getBoundingClientRect();
    chain.push({ sel: nm(n).slice(0, 42), left: Math.round(r.left), right: Math.round(r.right),
                 w: Math.round(r.width), scrollW: n.scrollWidth, clientW: n.clientWidth,
                 overflowX: cs.overflowX, whiteSpace: cs.whiteSpace, overflowWrap: cs.overflowWrap,
                 wordBreak: cs.wordBreak, width: cs.width, minW: cs.minWidth, maxW: cs.maxWidth,
                 pos: cs.position, disp: cs.display, flex: cs.flexShrink + '/' + cs.flexBasis });
  }
  const el = best.el;
  const apply = (label, css) => {
    const before = de.scrollWidth, saved = {};
    for (const p in css) { saved[p] = el.style.getPropertyValue(p); el.style.setProperty(p, css[p], 'important'); }
    const after = de.scrollWidth;
    for (const p in css) el.style.setProperty(p, saved[p]);
    return { label, before, after };
  };
  const fixes = [
    apply('overflow-wrap:anywhere', { 'overflow-wrap': 'anywhere' }),
    apply('word-break:break-all', { 'word-break': 'break-all' }),
    apply('white-space:normal', { 'white-space': 'normal' }),
    apply('max-width:100%', { 'max-width': '100%' }),
    apply('width:100%', { 'width': '100%' }),
    apply('min-width:0', { 'min-width': '0' }),
    apply('overflow-x:hidden', { 'overflow-x': 'hidden' }),
  ];
  const r = best.r;
  return {
    seen, truncated, vw, scrollWidth: de.scrollWidth,
    ink: { sel: nm(el), reach: best.reach, spill: best.spill,
           left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width),
           scrollW: el.scrollWidth, clientW: el.clientWidth,
           href: el.getAttribute && (el.getAttribute('href') || '').slice(0, 60),
           text: (el.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 80),
           html: el.outerHTML.slice(0, 200) },
    chain: chain.slice(0, 10), fixes,
  };
}"""


# Read the same number five times around one scroll, with no rule applied at all.
# The hit test accidentally found this: in webkit, `scrollWidth` reads 465 on a
# fresh page, and reads clientWidth after the document has been scrolled once. If
# that is true it is the mechanism in one sentence - the engine reports a
# scrollable overflow area it discards the first time anything uses it - and it is
# also the reason a hit test of "the empty strip" is impossible to run: scrolling
# to look at the strip is what makes it not exist.
SEQUENCE = """async () => {
  const de = document.documentElement;
  const raf = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const reads = [];
  const snap = (tag) => reads.push([tag, de.scrollWidth, de.clientWidth, window.scrollX]);
  snap('fresh');
  await raf(); await raf();
  snap('after two frames');
  await new Promise((r) => setTimeout(r, 200));
  snap('after 200ms');
  window.scrollTo(1000, 0); await raf();
  snap('scrollTo(1000,0)');
  window.scrollTo(0, 0); await raf();
  snap('back to 0');
  snap('scrollWidth now');
  de.scrollLeft = 50; await raf();
  snap('scrollLeft=50');
  return reads;
}"""


def cell(pw, engine, base, page, width, font, suppress):
    b = pw[engine].launch()
    c = b.new_context(viewport={"width": width, "height": gate.HEIGHT[width]})
    if suppress:
        c.add_init_script(SUPPRESS_POPUP)
    if IO_STUB_ON[0]:
        pg = c.new_page()
        pg.add_init_script(gate.IO_STUB)
    else:
        pg = c.new_page()
    injected = gate.route_font(c, font, page)
    pg.goto(f"{base}/{page}.html", wait_until="load", timeout=60000)
    return b, c, pg, injected


IO_STUB_ON = [True]


def main():
    args = sys.argv[1:]
    base = args[0] if args and not args[0].startswith("--") else BASE
    page, width, font, engine = "about", 320, 48, "webkit"
    suppress = "--suppress-popup" in args
    pages = None
    if "--engine" in args:
        engine = args[args.index("--engine") + 1]
    if "--page" in args:
        page = args[args.index("--page") + 1]
    if "--pages" in args:
        pages = args[args.index("--pages") + 1].split(",")
    if "--width" in args:
        width = int(args[args.index("--width") + 1])
    if "--font" in args:
        font = int(args[args.index("--font") + 1])
    if "--no-io-stub" in args:
        IO_STUB_ON[0] = False

    todo = pages or [page]
    with sync_playwright() as pw:
        for pg_name in todo:
            print(f"\n=== {pg_name} @ {width}px root {font}px, {engine}, popup "
                  f"{'SUPPRESSED (session flag pre-set)' if suppress else 'live (dwell 25s can reveal it)'} ===")
            b, c, pg, injected = cell(pw, engine, base, pg_name, width, font, suppress)
            m, q = gate.measure_cell(pg)          # the gate's own verdict on this cell
            off = m["off"]
            # measure_cell() has already raised Instrument if the 10rem probe, the computed
            # root font, or Bootstrap are wrong, so these are printed for the record rather
            # than asserted here - but the root font is re-checked because everything below
            # depends on the page being laid out at the size under test.
            print(f"  reproduced: scrollWidth {off['scrollW']} clientWidth {off['clientW']} "
                  f"(+{off['scrollW'] - off['clientW']}) | quiesced={q['quiesced']} "
                  f"| root read back {m['root']} (probe says {m['probeW']:.1f}px per 10rem, "
                  f"want {10 * font:.0f}) | bootstrap {m['bootstrap']} "
                  f"| injection fired {injected['n']}x")
            if abs(m["rootPx"] - font) > 0.5:
                print("  INSTRUMENT FAILURE: the root font the page is rendering is not the one "
                      "asked for, so nothing printed below describes the cell under test")
                b.close()
                continue

            st = pg.evaluate(STATE)
            print(f"  boxes: de.scrollWidth {st['scrollWidthDE']} | body.scrollWidth "
                  f"{st['scrollWidthBody']} | de rect width {st['deRectW']} | clientWidth "
                  f"{st['clientWidth']} | innerWidth {st['innerWidth']} | scrollingElement is de: "
                  f"{st['scrollingElementIsDE']}")
            print(f"  sessionStorage[{SESSION_FLAG}] at measure time = {st['popupFlagInSession']!r}")
            print(f"  popup: {st['popup']}")
            print(f"  panel: {st['panel']}")
            for h in st["honeypots"]:
                print(f"  honeypot: w={h['w']} left={h['left']} right={h['right']} "
                      f"pos={h['position']} in .eo-form={h['inEoForm']} in popup={h['inPopup']} "
                      f"parent={h['parent']!r}")
            print(f"  body children: {st['bodyChildren']}")

            w = pg.evaluate(WIDEST)
            print(f"  rect sweep over {w['seen']} elements{'' if not w['truncated'] else ' (TRUNCATED)'}, "
                  f"scrollWidth {w['scrollWidth']}, viewport {w['vw']}px:")
            if not w["top"]:
                print("    no element box reaches past the viewport on either side")
            for r in w["top"]:
                print(f"    d{r['depth']:2} right={r['right']:5} +{r['over']:4} w={r['w']:4} "
                      f"left={r['left']:6} {r['sel'][:44]}")
            if w["selfOverflowing"]:
                print("    boxes whose own content overflows them while overflow-x is visible "
                      "(that overflow escapes upwards, which is how a box inside the viewport "
                      "grows the document's scrollable area):")
                for s in w["selfOverflowing"]:
                    print(f"    d{s['depth']:2} {s['sel'][:40]:40} scrollWidth {s['scrollW']:5} "
                          f"vs clientWidth {s['clientW']}")

            ink = pg.evaluate(INK)
            print(f"  ink sweep over {ink['seen']} elements{'' if not ink['truncated'] else ' (TRUNCATED)'}:")
            if ink.get("none"):
                print("    no box whose own content spills while overflow-x is visible")
            else:
                i = ink["ink"]
                print(f"    furthest-reaching ink: {i['sel']}  box left={i['left']} right={i['right']} "
                      f"w={i['w']} | its own content scrollWidth {i['scrollW']} vs clientWidth {i['clientW']} "
                      f"-> spills {i['spill']}px, reaching x={i['reach']} against a {ink['vw']}px viewport "
                      f"and a document scrollWidth of {ink['scrollWidth']}")
                if i["href"]:
                    print(f"      href={i['href']!r}")
                print(f"      text={i['text']!r}")
                print(f"      html={i['html']}")
                print("    chain letting it escape (nearest first):")
                for n in ink["chain"]:
                    print(f"      {n['sel']:40} L{n['left']:6} R{n['right']:6} w={n['w']:5} "
                          f"scroll/client {n['scrollW']}/{n['clientW']} ox={n['overflowX']:8} "
                          f"ws={n['whiteSpace']:8} ow={n['overflowWrap']:10} w={n['width']:8} "
                          f"min={n['minW']:8} max={n['maxW']:8} {n['pos']}/{n['disp']} flex={n['flex']}")
                print("    candidate fixes applied to that element and reverted:")
                for f in ink["fixes"]:
                    verdict = "COLLAPSES IT" if f["after"] <= ink["vw"] else (f"reduced by {f['before'] - f['after']}" if f["after"] < f["before"] else "no effect")
                    print(f"      {f['label']:22} {f['before']} -> {f['after']:5}   {verdict}")

            sc = pg.evaluate(SCROLL_RIGHT)
            print(f"  CAN A READER SCROLL RIGHT? scrollTo(1000,0) -> scrollX "
                  f"{sc['scrollXAfterScrollTo1000']} (was {sc['scrollXBefore']}, reached {sc['reachedX']})")
            print("    => " + ("real: a reader can scroll to a place they cannot use; this is a defect"
                               if sc["scrollXAfterScrollTo1000"] > 0 else
                               "phantom: the document does not scroll right at all, so no reader can "
                               "reach the region the verdict line is measuring"))

            # Runs after every read-only measurement, because scrolling the page is what
            # changes the number it is investigating.
            seq = pg.evaluate(SEQUENCE)
            print("  the same number, five times around one scroll (no rule applied):")
            for tag, sw, cw, sx in seq:
                print(f"    {tag:18} scrollWidth {sw:5} clientWidth {cw:5} scrollX {sx}")

            bi = pg.evaluate(BISECT)
            warn = [x for x in bi["changed"] if "warn" in x]
            for x in warn:
                print("    RESTORE WARNING " + x["warn"] + "  (WebKit's document scrollable"
                      " overflow area can go stale once its cause is hidden; this is why the"
                      " read-only sweeps above run before anything mutates the page)")
            bi["changed"] = [x for x in bi["changed"] if "warn" not in x]
            print(f"  bisect <body> children (base scrollWidth {bi['base']}): "
                  + (", ".join(f"{x['tag']}.{x['cls']} -> {x['scrollWidth']}" for x in bi["changed"])
                     or "none of them changes it"))
            dn = pg.evaluate(DESCEND)
            print("  descent by contribution (each step is the child whose absence lowers "
                  "documentElement.scrollWidth):")
            for p in dn["path"]:
                print(f"    hop {p['hop']}: hiding {p['via'][:40]:40} -> {p['without']:5} "
                      f"(with it {p['with']})")
            if not dn["path"]:
                print("    body itself: no single child accounts for it")
            if dn["lastEffects"]:
                # The single-child hide is a sound bisect only where nothing reflows: in a
                # Bootstrap row, removing one column lets its sibling move into the same
                # overflow, so "no child changes it" can also mean "more than one does".
                # Printing every child's effect is what makes that visible instead of
                # silently stopping the descent at the wrong node.
                print("    no single child lowered it; each child's own effect: "
                      + ", ".join(f"{e['sel']}->{e['without']}" for e in dn["lastEffects"]))
            lf = dn["leaf"]
            print(f"  LEAF {lf['sel']}  box left={lf['left']} right={lf['right']} w={lf['w']} "
                  f"| its own scrollWidth {lf['scrollW']} vs clientWidth {lf['clientW']}")
            print(f"       position={lf['position']} display={lf['display']} white-space={lf['whiteSpace']} "
                  f"overflow-x={lf['overflowX']} overflow-wrap={lf['overflowWrap']} word-break={lf['wordBreak']}")
            print(f"       width={lf['width']} max-width={lf['maxWidth']} min-width={lf['minWidth']} "
                  f"margins={lf['marginLeft']}/{lf['marginRight']} float={lf['float']} font={lf['fontSize']} {lf['fontFamily']!r}")
            print(f"       html: {lf['html']}")
            for t in dn["texts"]:
                print(f"       text run: left={t['left']} right={t['right']} w={t['w']} "
                      f"against a {dn['clientWidth']}px viewport: {t['text']!r}")
            for k in dn["kids"]:
                flag = "  <-- self-overflowing" if k["scrollW"] > k["clientW"] else ""
                print(f"       child {k['sel']:38} left={k['left']:6} right={k['right']:6} "
                      f"w={k['w']:5} scrollW/clientW {k['scrollW']}/{k['clientW']}{flag}")
            print(f"  candidate fixes applied to the leaf and reverted (scrollWidth before {dn['scrollWidth']}):")
            for f in dn["fixes"]:
                arrow = "FIXED" if f["after"] <= dn["clientWidth"] else ("less" if f["after"] < f["before"] else "no change")
                print(f"    {f['label']:26} {f['before']} -> {f['after']:5}   {arrow}")
            if bi["changed"]:
                who = bi["changed"][0]["i"]
                print(f"  (hiding body.children[{who}] alone changes the number; see the "
                      f"rect sweep and descent above for what is inside it)")
            ex = pg.evaluate(EXPERIMENTS)
            print(f"  hide-and-see (base {ex['base']}, re-read after all restores "
                  f"{ex['steps'][-1]['scrollWidth']}):")
            for s in ex["steps"]:
                print(f"    {s['label']:42} hit={s['hit']:2} -> scrollWidth {s['scrollWidth']}")
            b.close()


if __name__ == "__main__":
    main()
