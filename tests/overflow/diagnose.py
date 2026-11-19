#!/usr/bin/env python3
"""Why does a specific element overflow? Print its ancestor chain, measured.

probe.py says *what* sticks out; this says *why*, by walking up from the element
and printing the computed box of every ancestor. Read it together with
probe.py's clipping-ancestor logic: the chain shows which ancestor is refusing
to shrink (min-width:auto in a flex row), which one is padding itself open at
large root font (Bootstrap .p-5 is 3rem), and which one already clips.

Usage: python3 diagnose.py <page> <css-selector> [root-font-px] [width-px]
       python3 diagnose.py tesla-1894-plates 'a[href*="inventionsresear"]' 48 390
       python3 diagnose.py tesla-worlds-fair-1893 --ink 48 390
           -> every element whose text or box leaves the layout viewport,
              deepest-first, which is how an ink overflow (a box that is
              normally sized but whose text sticks out of it, so a rect-only
              sweep cannot see it) gets traced back to the element that needs
              the fix rather than to the six ancestors that merely inherit it.
Narrow desktop window, no mobile emulation (see SHIP.md / PLAN §1).
"""
import os
import sys

import probe  # same directory: WORST
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8199"
HERE = os.path.dirname(os.path.abspath(__file__))

CHAIN = """(sel) => {
  const el = document.querySelector(sel);
  if (!el) return {error: 'no element matched ' + sel};
  const chain = [];
  let node = el, depth = 0;
  while (node && depth++ < 12) {
    const cs = getComputedStyle(node);
    const r = node.getBoundingClientRect();
    chain.push({
      tag: node.tagName.toLowerCase(),
      cls: (typeof node.className === 'string' ? node.className : '').trim().split(/\\s+/).filter(Boolean).join('.'),
      rect: [Math.round(r.left), Math.round(r.width), Math.round(r.right)],
      maxW: cs.maxWidth, minW: cs.minWidth, width: cs.width,
      ovx: cs.overflowX, disp: cs.display, flex: cs.flex, wrap: cs.flexWrap,
      pad: cs.paddingLeft + ' ' + cs.paddingRight,
      fs: cs.fontSize, ws: cs.whiteSpace, ow: cs.overflowWrap, wso: cs.wordSpacing,
      scrollW: node.scrollWidth,
    });
    node = node.parentElement;
  }
  // The longest unbreakable word inside the element, and how wide it is.
  let worstWord = '', worstW = 0;
  const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  for (let t = walk.nextNode(); t; t = walk.nextNode()) {
    for (const w of (t.nodeValue || '').split(/\\s+/)) {
      if (!w) continue;
      range.selectNodeContents(t);
      // measure just this word by isolating it in a temporary span
      const s = document.createElement('span');
      s.style.cssText = 'position:absolute;left:-99999px;white-space:pre;';
      s.textContent = w;
      const cs0 = getComputedStyle(el);
      s.style.font = cs0.font;
      document.body.appendChild(s);
      const wpx = s.getBoundingClientRect().width;
      s.remove();
      if (wpx > worstW) { worstW = wpx; worstWord = w; }
    }
  }
  return {chain, worstWord, worstWordPx: Math.round(worstW)};
}"""


def main():
    page, sel = sys.argv[1], sys.argv[2]
    font = int(sys.argv[3]) if len(sys.argv) > 3 else 48
    width = int(sys.argv[4]) if len(sys.argv) > 4 else 390
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        c = b.new_context(viewport={"width": width, "height": 844})
        pg = c.new_page()
        pg.goto(f"{BASE}/{page}.html", wait_until="load", timeout=30000)
        if font != 16:
            pg.add_style_tag(content=f":root{{font-size:{font}px !important}}")
        pg.wait_for_timeout(200)
        if sel == "--ink":
            w = pg.evaluate(probe.WORST)
            print(f"{page}  root {font}px  viewport {width}px  "
                  f"scrollWidth={w['scrollW']} clientWidth={w['clientW']}")
            # Deepest first: an ancestor inherits its child's ink overflow, so
            # the smallest `over` is the element that actually needs the rule.
            for o in sorted(w["list"], key=lambda o: (o["over"], -o["w"])):
                print(f"  +{o['over']:4} ink={o['ink']:4} {o['w']:4}x{o['h']:<4} L{o['left']:6} "
                      f"{o['sel'][:40]:40} ovx={o['ovx']:8} disp={o['disp']:11} "
                      f"clip={o['clipper'] or '-':18} {o['text'][:28]!r}")
            b.close()
            return
        d = pg.evaluate(CHAIN, sel)
        if "error" in d:
            print(d["error"])
            sys.exit(1)
        print(f"{page}  root {font}px  viewport {width}px  clientWidth={pg.evaluate('document.documentElement.clientWidth')}")
        print(f"longest word inside: {d['worstWord']!r} = {d['worstWordPx']}px")
        for i, n in enumerate(d["chain"]):
            print(f"{'  ' * i}{n['tag']}.{n['cls'][:34]:34} "
                  f"L{n['rect'][0]:5} W{n['rect'][1]:5} R{n['rect'][2]:5} "
                  f"scrollW={n['scrollW']:5} minW={n['minW']:6} maxW={n['maxW']:8} "
                  f"ovx={n['ovx']:8} disp={n['disp']:11} pad={n['pad']}")
            print(f"{'  ' * i}    font={n['fs']:7} white-space={n['ws']:8} overflow-wrap={n['ow']:10} flex={n['flex']}")
        b.close()


if __name__ == "__main__":
    main()
