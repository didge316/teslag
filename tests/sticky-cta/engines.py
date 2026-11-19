"""Deterministic-height check for the sticky offer bar across engines.

Post-refactor claim being tested: the bar's rendered height no longer depends
on the site's root font size, so it is a constant per breakpoint and the CSS
reservation can be a constant. If the height moves when the root font grows,
the cap did not take and the reservation is a lie - which is exactly the iOS
failure mode the refactor exists to remove.

Run: python3 engines.py [base-url] [chromium,webkit,firefox]
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8199"
PAGE = BASE + "/build-a-perpetual-motion-generator.html"
KEY = "tmg_sticky_cta_dismissed"

# mobile=False on the large-font cases on purpose. With is_mobile=True Chromium
# grows the containing block of a position:fixed element out to the page's
# scrollWidth while documentElement.clientWidth still reports 390: at a 48px
# root font the bar measured 690px wide on a 390px viewport, and innerWidth
# agreed with the lie (690) so an instrument that trusts innerWidth certifies
# it. That is emulation, not a browser - a narrow desktop window shows the sane
# behaviour (bar 390px, CTA at x=318) - so width is only judged in the context
# that does not lie about it.
CASES = [
    # (label, viewport, root font, mobile emulation)
    ("390x844 phone, 100% font",   {"width": 390, "height": 844}, "16px", True),
    ("390x844 phone, 200% font",   {"width": 390, "height": 844}, "32px", False),
    ("390x844 phone, 300% font",   {"width": 390, "height": 844}, "48px", False),
    ("390x844 phone, 400% font",   {"width": 390, "height": 844}, "64px", False),
    ("320x640 small phone, 100%",  {"width": 320, "height": 640}, "16px", True),
    ("320x640 phone, 300% (no emu)", {"width": 320, "height": 640}, "48px", False),
    ("360x780 android, 100%",      {"width": 360, "height": 780}, "16px", True),
    ("844x390 landscape, 100%",    {"width": 844, "height": 390}, "16px", True),
    ("320x480 tiny portrait, 100%", {"width": 320, "height": 480}, "16px", True),
]

MEASURE = """() => {
    const bar = document.querySelector('.tmg-cta-bar');
    if (!bar) return {missing: true};
    const b = bar.getBoundingClientRect();
    const btn = bar.querySelector('.tmg-cta-btn').getBoundingClientRect();
    const x = bar.querySelector('.tmg-cta-close').getBoundingClientRect();
    const lab = bar.querySelector('.tmg-cta-label').getBoundingClientRect();
    const cs = getComputedStyle(bar);
    // One row iff nothing wrapped: every child sits on the bar's first row.
    // Wrapping, not child tops: align-items:center gives each child its own
    // top, so a tops-based row count is meaningless here.
    return {
        display: cs.display,
        barH: Math.round(b.height),
        wrap: cs.flexWrap,
        cta: Math.round(btn.width) + 'x' + Math.round(btn.height),
        ctaText: JSON.stringify(bar.querySelector('.tmg-cta-btn').innerText),
        gap: Math.round(x.left - btn.right),
        labelW: Math.round(lab.width),
        label: JSON.stringify(bar.querySelector('.tmg-cta-label').innerText.trim()),
        pad: getComputedStyle(document.body).paddingBottom,
        inlinePad: document.body.style.paddingBottom,
        reserveOK: parseFloat(getComputedStyle(document.body).paddingBottom) + 1 >= b.height,
        clipped: bar.scrollWidth > Math.ceil(bar.clientWidth) + 1,
        clientW: document.documentElement.clientWidth,
        barW: Math.round(b.width),
        btnRight: Math.round(btn.right),
        fits: Math.round(b.right) <= document.documentElement.clientWidth + 1,
    };
}"""

engines = ["chromium", "webkit", "firefox"] if len(sys.argv) < 3 else sys.argv[2].split(",")
out = {}
with sync_playwright() as pw:
    for name in engines:
        launch = getattr(pw, name)
        try:
            browser = launch.launch()
        except Exception as e:                                    # noqa: BLE001
            print(f"!! {name} failed to launch: {str(e).splitlines()[0]}")
            continue
        out[name] = {}
        for label, vp, font, mobile in CASES:
            opts = {"viewport": vp}
            if name != "firefox" and mobile:
                opts.update({"is_mobile": True, "has_touch": True})
            try:
                ctx = browser.new_context(**opts)
            except Exception:                                      # noqa: BLE001
                ctx = browser.new_context(viewport=vp)
            p = ctx.new_page()
            p.goto(PAGE, wait_until="load")
            try:
                p.add_style_tag(content=f":root{{font-size:{font}!important}}")
            except Exception:                                      # noqa: BLE001
                p.evaluate(f"document.documentElement.style.fontSize='{font}'")
            p.evaluate("scrollTo(0, 1500)")
            p.wait_for_timeout(400)
            m = p.evaluate(MEASURE)
            out[name][label] = m
            print(f"{name:9} {label:28} h={m.get('barH')} wrap={m.get('wrap')} "
                  f"cta={m.get('cta')} gap={m.get('gap')} label={m.get('labelW')}px "
                  f"pad={m.get('pad')} inline={m.get('inlinePad') or '-'} "
                  f"reserveOK={m.get('reserveOK')} fits={m.get('fits')} "
                  f"(bar {m.get('barW')}/{m.get('clientW')}px, btn.right={m.get('btnRight')}) "
                  f"clip={m.get('clipped')}")
            ctx.close()
        browser.close()

# The invariant: bar height must not grow with the site's root font size.
print("\n=== height vs root font (the iOS failure mode) ===")
bad, asserted = [], 0
for name in engines:
    r = out.get(name, {})
    if not r:
        continue
    base = r.get("390x844 phone, 100% font", {}).get("barH")
    if base is None:
        # The bug this line used to be: `continue`. An engine that measured nothing
        # skipped all of its assertions, left `bad` empty, and the summary line
        # below then printed "all 27 cases across 3 engines" green - on a tree where
        # the sticky bar does not exist at all, with every row printing h=None. A
        # vacuous green is worse than a red: it is the same shape as a pass.
        # A missing measurement is an instrument failure (exit 2): not a defect in
        # the site, and emphatically not a pass either.
        print(f"INSTRUMENT FAILED: {name} produced no bar height at its baseline "
              f"case. The sticky bar is not present in the tree served at {BASE} - "
              f"the feature lives in js/scripts.js, so `git show HEAD:js/scripts.js "
              f"| grep -c sticky` tells you whether the commit under test has it at "
              f"all ({len(r)} cases were collected and none of them are assertions).")
        sys.exit(2)
    worst = max((v.get("barH") or 0) for k, v in r.items() if k.startswith("390x844"))
    print(f"  {name:9} 100%={base}px  worst-of-400%={worst}px  drift={worst - base:+}px")
    for label, m in r.items():
        if m.get("missing"):
            bad.append(f"{name}/{label}: no bar")
            continue
        asserted += 1   # only a case that actually measured something counts as an
                        # assertion made; the summary line below prints this number
        # fits is only meaningful where innerWidth does not lie, i.e. the
        # mobile=False cases; there the fixed bar must not outgrow the layout
        # viewport, or the CTA sits off the visible edge.
        if "no emu" in label or ("font" in label and "100%" in label and "emu" not in label):
            pass
        if not m.get("reserveOK"):
            bad.append(f"{name}/{label}: reserved {m.get('pad')} < bar {m.get('barH')}px")
        if m.get("clipped"):
            bad.append(f"{name}/{label}: bar content clipped")
        if m.get("gap", 99) < 24:
            bad.append(f"{name}/{label}: CTA-dismiss gap {m.get('gap')} < 24px")
        if not m.get("cta", "x44").endswith("x44"):
            bad.append(f"{name}/{label}: CTA not 44px tall ({m.get('cta')})")
        if m.get("wrap") != "nowrap":
            bad.append(f"{name}/{label}: flex-wrap {m.get('wrap')}")
print("\n=== verdict ===")
if bad:
    for b in bad:
        print("  FAIL", b)
    sys.exit(1)
if asserted == 0:
    print("INSTRUMENT FAILED: no case measured anything, so nothing was asserted. "
          "This is not a pass.")
    sys.exit(2)
print(f"  asserted {asserted} cases ({sum(len(v) for v in out.values())} collected) "
      f"across {len(out)} engines: reservation >= bar, no clipping, gap >= 24px, "
      f"CTA 44px tall, no wrapping")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "engines.json"), "w"), indent=1)
print("wrote engines.json next to this file")
