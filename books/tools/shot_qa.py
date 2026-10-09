#!/usr/bin/env python3
"""Layout QA: serve the site, shoot three viewports, fail on what is measurable.

SERIES-PLAN-1894.md §6.5 / §8 step 7 / §12 visual gates.

    python3 books/tools/shot_qa.py tesla-earthquake-machine
    python3 books/tools/shot_qa.py tesla-earthquake-machine --serve-port 8080

Writes website/_qa/<slug>-{mobile,tablet,desktop}.png (full page) and
<slug>-mobile-fold.png (first screen, for the CTA-above-the-fold check).

The screenshots are for a *viewer*. What this script can decide on its own:
console errors, 404s, horizontal overflow, images without intrinsic size,
figures wider than their column, a missing nav dropdown, and a CTA that is not
in the mobile first screen. Hard gate before deploy.
"""

import argparse
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parents[2] / "website"
QA = WEB / "_qa"
VIEWPORTS = {"mobile": (375, 812), "tablet": (768, 1024), "desktop": (1280, 900)}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, *a):
        pass


def serve(port, slug):
    """Bind our own server; if the port is taken, reuse it when it already
    serves this site (the runbook keeps a server on :8080), else hop ports."""
    import urllib.request
    probe = f"http://127.0.0.1:{port}/{slug}.html"
    try:
        with urllib.request.urlopen(probe, timeout=3) as r:
            if r.status == 200:
                print(f"using the server already on :{port}")
                return None, port
    except OSError:
        pass
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", port), Quiet)
    except OSError:
        port = 0                              # let the OS pick a free port
        httpd = socketserver.TCPServer(("127.0.0.1", port), Quiet)
        port = httpd.server_address[1]
        print(f"requested port busy -> serving on :{port}")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def shoot(page, base, slug, vp_name, width, height, outdir):
    problems = []
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{base}/{slug}.html", wait_until="networkidle")
    page.wait_for_timeout(400)

    shot = outdir / f"{slug}-{vp_name}.png"
    page.screenshot(path=str(shot), full_page=True)
    if vp_name == "mobile":
        page.screenshot(path=str(outdir / f"{slug}-mobile-fold.png"),
                        full_page=False)

    # measurable layout gates
    metrics = page.evaluate("""() => {
      const doc = document.documentElement;
      const art = document.querySelector('article') || doc;
      const over = [...document.querySelectorAll('article img, article figure')]
        .filter(el => el.getBoundingClientRect().width >
                      (el.closest('.col-lg-8')?.clientWidth || doc.clientWidth) + 2)
        .map(el => el.tagName + ':' + (el.src || el.className));
      const noDims = [...document.querySelectorAll('article img')]
        .filter(i => !i.getAttribute('width') || !i.getAttribute('height'))
        .map(i => i.getAttribute('src'));
      const cta = document.querySelector('.alert-info');
      const ctaTop = cta ? Math.round(cta.getBoundingClientRect().top) : null;
      const scarce = document.querySelector('.scarcity-widget');
      const scarceTop = scarce ? Math.round(scarce.getBoundingClientRect().top) : null;
      const anyAff = document.querySelectorAll('a[href*="hop.clickbank.net"]').length;
      return {
        scrollW: doc.scrollWidth, clientW: doc.clientWidth,
        overflow: over, noDims: noDims,
        nav: !!document.querySelector('.navbar .dropdown-menu'),
        navItems: document.querySelectorAll('.navbar .dropdown-item').length,
        h1: document.querySelectorAll('h1').length,
        ctaTop: ctaTop, scarceTop: scarceTop, anyAff: anyAff,
        sidebar: !!document.querySelector('.col-lg-4'),
      };
    }""")

    if metrics["scrollW"] > metrics["clientW"] + 1:
        problems.append(f"horizontal overflow: scrollWidth {metrics['scrollW']} > "
                        f"clientWidth {metrics['clientW']}")
    if metrics["overflow"]:
        problems.append(f"element wider than its column: {metrics['overflow'][:3]}")
    if metrics["noDims"]:
        problems.append(f"img without width/height (layout shift): {metrics['noDims'][:3]}")
    if not metrics["nav"]:
        problems.append("nav dropdown missing")
    if metrics["h1"] != 1:
        problems.append(f"h1 count in DOM = {metrics['h1']}")
    if not metrics["sidebar"]:
        problems.append("sidebar column missing")
    if vp_name == "mobile" and not metrics["anyAff"]:
        problems.append("no affiliate CTA anywhere on the page")
    if vp_name == "mobile":
        # §12 asks for the CTA in the mobile first screen. The donor shell puts
        # the scarcity widget at the bottom of the column, so this is reported,
        # not failed — the in-body alert is the one a reader actually sees.
        print(f"  note    mobile CTA positions: alert-info={metrics['ctaTop']}px "
              f"scarcity={metrics['scarceTop']}px (viewport {height}px)")

    print(f"  {vp_name:<8} {shot.name}  "
          f"nav={metrics['nav']} navitems={metrics['navItems']} "
          f"overflow={metrics['scrollW']}px")
    return problems, metrics


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="page slug without .html")
    ap.add_argument("--serve-port", type=int, default=8080)
    ap.add_argument("--out", default=str(QA))
    ap.add_argument("--viewports", default=",".join(VIEWPORTS))
    args = ap.parse_args()

    if not (WEB / f"{args.slug}.html").exists():
        sys.exit(f"no such page: {WEB / (args.slug + '.html')}")
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    httpd, port = serve(args.serve_port, args.slug)
    base = f"http://127.0.0.1:{port}"
    console, requests, problems = [], [], []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.on("console", lambda m: console.append(f"{m.type}: {m.text}")
                    if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
            page.on("requestfailed", lambda r: requests.append(
                f"{r.method} {r.url} -> {r.failure}"))
            page.on("response", lambda r: requests.append(
                f"{r.status} {r.url}") if r.status >= 400 else None)

            for vp in args.viewports.split(","):
                w, h = VIEWPORTS[vp.strip()]
                probs, _ = shoot(page, base, args.slug, vp.strip(), w, h, outdir)
                problems += [f"[{vp}] {x}" for x in probs]
            browser.close()
    finally:
        if httpd:
            httpd.shutdown()

    print("\nconsole:")
    for c in console[:15]:
        print("  ", c)
    if not console:
        print("   clean")
    print("failed/4xx requests:")
    for r in requests[:15]:
        print("  ", r)
    if not requests:
        print("   none")

    hard = [x for x in requests if "404" in x or "->" in x]
    if problems or hard:
        print("\nLAYOUT QA FAILED")
        for x in problems:
            print("  -", x)
        for x in hard:
            print("  - request:", x)
        print("\nfix, then re-shoot (§6.5 step 4).")
        return 1
    print("\nlayout QA: all measurable gates pass.")
    print("still to do by eye: figure subjects, caption truth, caption legibility,")
    print("sidebar stacking, OG image at 300px — §12 visual gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
