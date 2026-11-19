#!/usr/bin/env python3
"""Screenshots of the stage site in the user's real Brave, without touching their tabs.

The plan's verification step is "real Brave, your tabs untouched - open a page,
CDP-override the viewport, close the tab". That is what this does: it connects
to the already-running Brave over CDP (:9222) and takes a NEW browser context of
its own, so nothing the user has open is navigated, resized or replaced, and the
context is closed at the end. Playwright's connect_over_cdp is used rather than
playwright-cli's `attach`, because attach drives the existing session.

Root font is set the way the site's own A+/A- control sets it (wp-textsize
writes a :root font-size), so 32px and 48px here are what a visitor who clicked
A+ twice or three times sees - not a browser zoom, and not device emulation
(PLAN §1: mobile emulation lies about the layout viewport).

Usage:
    python3 shots.py --tag item7            # the standard item-7 set
    python3 shots.py --only 390x48          # any subset of the WxHxFONT tags
Writes /home/matt/projects/other/tesla-generator/.verify/<tag>-<page>.png
"""
import os
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8199"
OUT = "/home/matt/projects/other/tesla-generator/.verify"
CDP = "http://localhost:9222"

# (label, width, height, root font px)
SHOTS = [
    ("390x16", 390, 844, 16),
    ("390x32", 390, 844, 32),
    ("390x48", 390, 844, 48),
    ("320x16", 320, 844, 16),
    ("1280x16", 1280, 900, 16),
    ("1280x48", 1280, 900, 48),
    ("768x48", 768, 1000, 48),
]
PAGES = ["index", "contact", "tesla-magnetic-generator-worth-it", "whole-house", "articles"]


def main():
    only = None
    tag = "shot"
    args = sys.argv[1:]
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    if "--tag" in args:
        tag = args[args.index("--tag") + 1]
    if "--pages" in args:
        PAGES[:] = args[args.index("--pages") + 1].split(",")
    ELEMENT = args[args.index("--element") + 1] if "--element" in args else None
    shots = [s for s in SHOTS if only is None or s[0] in only]
    if not shots:
        sys.exit(f"--only matched nothing; available: {[s[0] for s in SHOTS]}")
    os.makedirs(OUT, exist_ok=True)

    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(CDP)
        ctx = b.new_context(viewport={"width": 390, "height": 844})   # our own context, not their tabs
        pg = ctx.new_page()
        for label, w, h, font in shots:
            # One page object per (viewport, root font) row: an style tag added
            # with add_style_tag() re-applies after every navigation for the
            # life of the page, so a 48px row followed by a 16px row would be
            # shot at 48px through an invisible :root override.
            pg = ctx.new_page()
            pg.set_viewport_size({"width": w, "height": h})
            for page in PAGES:
                pg.goto(f"{BASE}/{page}.html", wait_until="load", timeout=30000)
                if font != 16:
                    pg.add_style_tag(content=f":root{{font-size:{font}px !important}}")
                pg.wait_for_timeout(400)
                if ELEMENT:
                    # A viewport shot of the top of the page tells you nothing
                    # about the part being judged (300% comment columns live 12k
                    # px down). Scroll one element into view and shoot that.
                    pg.locator(ELEMENT).first.scroll_into_view_if_needed()
                    pg.wait_for_timeout(150)
                d = pg.evaluate("""() => ({
                    scrollW: document.documentElement.scrollWidth,
                    clientW: document.documentElement.clientWidth,
                    innerW: window.innerWidth,
                    bodyH: document.body.scrollHeight,
                })""")
                path = os.path.join(OUT, f"{tag}-{label}-{page}{('-' + ELEMENT.split()[0][:14]) if ELEMENT else ''}.png")
                pg.screenshot(path=path)
                flag = "OVERFLOW" if d["scrollW"] > d["clientW"] + 1 else "ok"
                print(f"{os.path.basename(path):46} scrollW={d['scrollW']:5} "
                      f"clientW={d['clientW']:4} innerW={d['innerW']:4} {flag}")
            pg.close()   # this row only; the user's own tabs are never touched
        ctx.close()   # only our context; the user's tabs are left exactly as found
    print(f"\nwrote {len(shots) * len(PAGES)} shots into {OUT}")


if __name__ == "__main__":
    main()
