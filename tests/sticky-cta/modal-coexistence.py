#!/usr/bin/env python3
"""Does the offer bar stay reachable while the exit popup is open?

The reviewer raised this as the thing this commit *newly contributes*: the popup
renders `role="dialog" aria-modal="true"` (js/exit-popup.js:63) and does not mark
the rest of the page inert, and the bar is appended to `<body>`
(js/scripts.js:311). `aria-modal` is a declaration to an assistive technology,
not a wall - it does not remove anything from the tab ring - so on a page where
both are up there may be a focusable affiliate link sitting behind a modal that
claims to be the only thing on the screen. Whether that is true is a measurement.

The popup appears two ways, and both are exercised because they are different
code paths: a real 25s dwell (DWELL_MS, the path every visitor who lingers hits)
and the exit-intent mouseout (the path a mouse user hits first).

Run: python3 modal-coexistence.py [base-url] [chromium,webkit]
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8199"
ENGINES = (sys.argv[2].split(",") if len(sys.argv) > 2 else ["chromium", "webkit"])
PAGE = BASE + "/build-a-perpetual-motion-generator.html"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "modal-coexistence-2026-11-19.txt")

# What the popup itself says about what is on screen, and what is still in the
# tab ring outside it. offsetParent is the cheap visibility proxy; a fixed element
# has offsetParent null, so the bar is asked about directly instead.
STATE = """() => {
    const dialog = document.querySelector('[role="dialog"][aria-modal="true"]');
    const bar = document.querySelector('.tmg-cta-bar');
    const outside = [...document.querySelectorAll(
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])')]
        .filter(el => !el.closest('[role="dialog"]'))
        .filter(el => (el.offsetParent !== null || getComputedStyle(el).position === 'fixed')
                   && getComputedStyle(el).visibility !== 'hidden'
                   && el.getBoundingClientRect().width > 0);
    return {
        popupOpen: !!dialog,
        popupLabelledby: dialog ? dialog.getAttribute('aria-labelledby') : null,
        barInDom: !!bar,
        barVisible: !!bar && bar.classList.contains('is-visible'),
        // which of the stragglers are the bar's own controls
        barControlsOutside: outside.filter(el => el.closest('.tmg-cta-bar'))
                                 .map(el => el.className || el.tagName.toLowerCase()),
        stragglersOutside: outside.length,
        stragglerSample: outside.slice(0, 6).map(
            el => (el.closest('.tmg-cta-bar') ? '[bar] ' : '') +
                  (el.className || el.tagName.toLowerCase())),
    };
}"""

# one synthetic mouseout that satisfies the shipped guard in one event:
# the handler stores lastX from clientX, then exitIntent requires a null
# relatedTarget and clientY <= 5, so clientX=300/clientY=0/relatedTarget=null
# walks the same branch a real cursor leaving the top edge walks.
EXIT_INTENT = """() => {
    document.dispatchEvent(new MouseEvent('mouseout',
        {clientX: 300, clientY: 0, relatedTarget: null, bubbles: true}));
}"""

ACTIVE = """() => {
    const a = document.activeElement;
    if (!a) return {tag: null};
    const bar = a.closest ? a.closest('.tmg-cta-bar') : null;
    const dlg = a.closest ? a.closest('[role="dialog"]') : null;
    return {tag: a.tagName.toLowerCase(), cls: a.className || null,
            text: (a.textContent || a.value || '').trim().slice(0, 24),
            inBar: !!bar, inDialog: !!dlg};
}"""


def run(engine, results):
    with sync_playwright() as pw:
        b = getattr(pw, engine).launch()
        for how in ("dwell", "exit-intent"):
            ctx = b.new_context(viewport={"width": 390, "height": 844},
                                has_touch=True, is_mobile=True)
            pg = ctx.new_page()
            pg.goto(PAGE, wait_until="load")
            pg.evaluate("() => window.scrollTo(0, 1400)")
            pg.wait_for_timeout(900)
            before = pg.evaluate(STATE)
            if how == "dwell":
                # the real path: sit on the page for DWELL_MS + change
                pg.wait_for_timeout(26500)
            else:
                pg.evaluate(EXIT_INTENT)
                pg.wait_for_timeout(700)
            after = pg.evaluate(STATE)
            steps = []
            if after["popupOpen"]:
                # start inside the dialog, then walk out of it in both directions
                pg.evaluate("""() => { const i = document.querySelector(
                    '[role="dialog"] input:not([type=hidden])'); if (i) i.focus(); }""")
                inside = pg.evaluate(ACTIVE)
                pg.keyboard.press("Shift+Tab")
                pg.wait_for_timeout(120)
                steps.append(("shift-tab back from the dialog's first field", pg.evaluate(ACTIVE)))
                pg.evaluate("""() => { const i = document.querySelector(
                    '[role="dialog"] input:not([type=hidden])'); if (i) i.focus(); }""")
                pg.keyboard.press("Tab")
                pg.wait_for_timeout(120)
                # several presses: the ring may take a couple of stops to get out
                landed = None
                for _ in range(6):
                    a = pg.evaluate(ACTIVE)
                    if a.get("inBar"):
                        landed = a
                        break
                    pg.keyboard.press("Tab")
                    pg.wait_for_timeout(120)
                steps.append(("tab forward from the dialog's first field, up to 6 stops",
                              landed or pg.evaluate(ACTIVE)))
                pg.keyboard.press("Escape")
                pg.wait_for_timeout(300)
                esc = pg.evaluate(STATE)
            else:
                inside, esc = None, None
            results.append({"engine": engine, "how": how, "before_popup": before,
                            "after_popup": after, "focus_inside_dialog": inside,
                            "tab_walk": steps, "after_escape": esc})
            ctx.close()
        b.close()


results = []
for e in ENGINES:
    run(e, results)

lines = ["# bar reachability while the exit popup is open - the modal the site declares with",
         "# role=dialog aria-modal=true and does not make the rest of the page inert.",
         "# Generated 2026-11-19; page /build-a-perpetual-motion-generator at 390x844 mobile.", ""]
bad = []
for r in results:
    a = r["after_popup"]
    lines.append(f"== {r['engine']} / {r['how']} trigger ==")
    lines.append(f"   bar visible before the popup : {r['before_popup']['barVisible']}")
    lines.append(f"   popup open                   : {a['popupOpen']}")
    lines.append(f"   bar still visible behind it  : {a['barVisible']}")
    lines.append(f"   focusables outside the dialog: {a['stragglersOutside']} "
                 f"(of which the bar's own: {len(a['barControlsOutside'])} -> "
                 f"{', '.join(a['barControlsOutside']) or 'none'})")
    lines.append(f"   first six in the ring        : {'; '.join(a['stragglerSample'])}")
    if r.get("focus_inside_dialog"):
        f = r["focus_inside_dialog"]
        lines.append(f"   focus parked in the dialog   : {f.get('inDialog')} "
                     f"({f.get('tag')}.{f.get('cls')})")
    for label, a2 in r["tab_walk"]:
        lines.append(f"   {label}: {'THE BAR' if a2.get('inBar') else a2.get('cls') or a2.get('tag')}"
                     f" (inBar={a2.get('inBar')})")
    if r.get("after_escape") is not None:
        e = r["after_escape"]
        lines.append(f"   after Escape: popup open={e['popupOpen']}, "
                     f"bar visible={e['barVisible']}")
    if a["popupOpen"] and a["barVisible"] and len(a["barControlsOutside"]):
        bad.append(f"{r['engine']}/{r['how']}: {len(a['barControlsOutside'])} bar control(s) "
                   f"tabbable behind an aria-modal dialog")
    lines.append("")

lines.append("verdict")
if bad:
    lines.append("  REACHABLE BEHIND THE MODAL: " + "; ".join(bad))
    lines.append("  -> aria-modal is not a focus wall, and nothing else on the page is inerted,")
    lines.append("     so the bar's affiliate link is in the tab ring while the dialog claims")
    lines.append("     to be the only thing present. Decide whether paint() hides the bar while")
    lines.append("     a dialog is open, or the dialog gets a real focus trap.")
else:
    lines.append("  not reachable behind the modal in the paths exercised")
open(OUT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
print(f"\nwrote {OUT}")
