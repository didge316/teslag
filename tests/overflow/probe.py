#!/usr/bin/env python3
"""Which elements actually overflow, on every page, at large text.

Item 7 of PLAN-ALT-NAV-OVERFLOW.md starts here. Do not fix overflow before
running this: the tempting fix (overflow-x:hidden on body) hides the symptom,
breaks position:fixed and focus handling, and leaves the offender in place.

Usage: python3 probe.py [base-url] [root-font-px ...]
Writes overflow-report.json next to this file.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

# BASE/FONTS are parsed inside main(): importing this module for OFFENDERS and
# PAGES (gate.py does) must not swallow the importer's argv.
WIDTH, HEIGHT = 390, 844
HERE = os.path.dirname(os.path.abspath(__file__))

# This file lives at website/tests/overflow/, so the site root is two levels up.
SITE = os.path.abspath(os.path.join(HERE, "..", ".."))
if not os.path.exists(os.path.join(SITE, "index.html")):
    sys.exit(f"cannot find site root from {HERE} (tried {SITE})")
PAGES = sorted(
    f[:-5] for f in os.listdir(SITE)
    if f.endswith(".html") and f != "404.html"
)

OFFENDERS = """() => {
  const vw = document.documentElement.clientWidth;
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right <= vw + 1 && r.left >= -1) continue;
    // An ancestor that clips is doing its job; report the clipper instead.
    let clipped = false, node = el.parentElement, depth = 0;
    while (node && node !== document.body && depth++ < 8) {
      const cs = getComputedStyle(node);
      if (cs.overflowX !== 'visible') { clipped = true; break; }
      node = node.parentElement;
    }
    if (clipped) continue;
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\\s+/).slice(0, 3).join('.') : '';
    out.push({
      sel: el.tagName.toLowerCase() + cls,
      w: Math.round(r.width),
      over: Math.round(Math.max(0, r.right - vw)),
      text: (el.innerText || '').trim().slice(0, 40),
    });
  }
  out.sort((a, b) => b.over - a.over);
  return {
    scrollW: document.documentElement.scrollWidth,
    clientW: vw,
    innerW: window.innerWidth,   // reported, never trusted (see SHIP.md)
        offenders: out.slice(0, 4),
    count: out.length,
  };
}"""


# The same sweep with the two deliberate filters switched off, for the case
# where scrollWidth says something overflows but OFFENDERS names nothing that
# sticks out to the right: the only things OFFENDERS drops are zero-box
# elements and descendants of an ancestor that already clips, and either can
# still be the thing that grew the document's scroll area. Nothing here is a
# verdict - it is a shortlist for diagnose.py.
WORST = """() => {
  const vw = document.documentElement.clientWidth;
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    // Ink overflow: a block whose box is inside the viewport but whose text
    // sticks out of it (a long unbreakable word, a nowrap run) never shows up
    // in a rect-only sweep, yet it is exactly what grows documentElement
    // .scrollWidth. scrollWidth-clientWidth is how much of it went past the
    // right edge in a left-to-right document.
    // Only a box that lets its own content spill contributes ink to the page:
    // an input or a hidden wrapper clips its overflow instead (EmailOctopus's
    // "Powered by" line is measured spilling 312px inside a box with
    // overflow-x: hidden, and it costs the document nothing).
    const cs = getComputedStyle(el);
    const ink = cs.overflowX === 'visible' ? Math.max(0, el.scrollWidth - el.clientWidth) : 0;
    if (r.right + ink <= vw + 1 && r.left >= -1) continue;
    let clipper = '', node = el.parentElement, depth = 0;
    while (node && node !== document.body && depth++ < 8) {
      if (getComputedStyle(node).overflowX !== 'visible') {
        clipper = node.tagName.toLowerCase() + '.' + String(node.className || '').trim().split(/\\s+/)[0];
        break;
      }
      node = node.parentElement;
    }
    out.push({
      sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
        ? '.' + el.className.trim().split(/\\s+/).slice(0, 3).join('.') : ''),
      w: Math.round(r.width), h: Math.round(r.height),
      left: Math.round(r.left), right: Math.round(r.right),
      over: Math.round(Math.max(0, r.right + ink - vw)), ink,
      pos: cs.position, disp: cs.display, ovx: cs.overflowX, clipper,
      text: (el.innerText || el.src || '').trim().slice(0, 40),
    });
  }
  out.sort((a, b) => b.over - a.over || b.w - a.w);
  const outside = [...document.children].filter(n => n.tagName !== 'BODY' && n.tagName !== 'HEAD' && n.tagName !== 'SCRIPT')
    .map(n => n.tagName + '.' + (n.className || ''));
  // 14, not 4: gate.py wants the top few by how far they stick out,
  // diagnose.py wants the bottom few, which is where the element that actually
  // needs the rule lives (ancestors only inherit their child's ink).
  return { scrollW: document.documentElement.scrollWidth, clientW: vw, outsideBody: outside, list: out.slice(0, 14) };
}"""


def main():
    base = (sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8199")
    fonts = [int(a) for a in sys.argv[2:]] or [16, 32, 48]
    report = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for font in fonts:
            per = {}
            for p in PAGES:
                c = b.new_context(viewport={"width": WIDTH, "height": HEIGHT})
                pg = c.new_page()
                pg.goto(f"{base}/{p}.html", wait_until="load", timeout=30000)
                if font != 16:
                    pg.add_style_tag(content=f":root{{font-size:{font}px !important}}")
                pg.wait_for_timeout(150)
                d = pg.evaluate(OFFENDERS)
                if d["scrollW"] > d["clientW"] + 1:
                    per[p] = d
                c.close()
            report[font] = per
            worst = sorted(per.items(), key=lambda kv: -kv[1]["scrollW"])[:6]
            print(f"\n== root font {font}px: {len(per)} of {len(PAGES)} pages overflow at {WIDTH}px ==")
            for name, d in worst:
                top = d["offenders"][0] if d["offenders"] else {"sel": "?", "over": d["scrollW"] - d["clientW"]}
                print(f"  {name[:44]:44} scrollW={d['scrollW']:5} +{d['scrollW'] - d['clientW']:4}  "
                      f"{d['count']:3} offenders  worst={top['sel']} +{top.get('over')}")
        b.close()
    json.dump(report, open(os.path.join(HERE, "overflow-report.json"), "w"), indent=1)
    print(f"\nwrote overflow-report.json ({sum(len(v) for v in report.values())} page-font combinations)")
    print("NOTE: innerWidth is reported for contrast only. It can differ from the layout")
    print("      viewport; clientWidth is the number fixed positioning uses.")


if __name__ == "__main__":
    main()
