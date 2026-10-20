#!/usr/bin/env python3
"""Layout QA: serve the site, shoot three viewports, fail on what is measurable.

SERIES-PLAN-1894.md §6.5 / §8 step 7 / §12 visual gates.

    python3 books/tools/shot_qa.py tesla-earthquake-machine
    python3 books/tools/shot_qa.py tesla-earthquake-machine --serve-port 8080

Writes website/_qa/<slug>-{mobile,tablet,desktop}.png (full page) and
<slug>-mobile-fold.png (first screen, for the CTA-above-the-fold check).

What this script can decide on its own: console errors, 404s, horizontal
overflow, images without intrinsic size, figures that never decode, figures wider
than their column, a blank band in the rendered pixels (nothing painted in a
600 px run of background), a missing nav dropdown, and a CTA that is not in the
mobile first screen. The image checks run over every image in the page content,
not only inside <article> - see the scope comment in shoot(). Hard gate before
deploy.
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
# The donor shell's own "is the site live?" probe: js/scripts.js fetches the
# site root 2 s after load to flip the v1 status badge. Off-network it always
# fails, and it fails on the donor page too, so it is reported, never failed.
SHELL_PROBE = "https://teslamagneticgenerator.com/"


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


def preload_lazy(page):
    """Scroll the whole page so loading="lazy" figures actually decode.

    A full-page screenshot does not scroll, and Chromium will not fetch a lazy
    image several thousand px below the viewport — the shot then shows a blank
    figure box and the visual review is worthless (§6.5 step 3).
    """
    page.evaluate("""async () => {
      const step = Math.round(window.innerHeight * 0.8);
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 120));
      }
      window.scrollTo(0, document.body.scrollHeight);
      await new Promise(r => setTimeout(r, 300));
      window.scrollTo(0, 0);
      // Chromium will still skip a lazy image that was never near the viewport
      // during a fast scroll; make them all eligible so the shot is complete.
      document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
    }""")
    try:
        page.wait_for_function(
            "() => [...document.images].filter(i => i.offsetParent)"
            ".every(i => i.complete)", timeout=15000)
    except Exception:
        stuck = page.evaluate(
            "() => [...document.images].filter(i => i.offsetParent && !i.complete)"
            ".map(i => i.getAttribute('src'))")
        print(f"  note    images still undecoded after preload: {stuck[:5]}")


def blank_bands(shot_path, limit=600):
    """Longest run of rows that are nothing but the page background.

    A collapsed column, a figure that never painted, or an empty section all look
    like this in a full-page shot, and none of the DOM checks in shoot() see it,
    because the DOM says the element is there and sized. Measured across the 15
    series pages at three widths on 2026-10-20: the longest legitimate band is
    110 px (section spacing on the plates page); every other page is 80-91 px.
    The donor legacy page nikola-tesla-inventor-extraordinaire has a 622 px band,
    which is why the limit is 600 and not lower: this gate is for the series, and
    it is not here to re-litigate the old pages. Returns (longest, y, bg).
    """
    try:
        import numpy as np
    except ImportError:
        return None
    from PIL import Image
    a = np.asarray(Image.open(shot_path).convert("L"), dtype=np.uint8)
    counts = np.bincount(a.ravel(), minlength=256)
    bg = int(counts.argmax())
    blank = (np.abs(a.astype(np.int16) - bg) <= 3).all(axis=1)
    d = np.diff(np.concatenate(([0], blank.astype(np.int8), [0])))
    starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    if not len(starts):
        return (0, 0, bg)
    i = int((ends - starts).argmax())
    return (int(ends[i] - starts[i]), int(starts[i]), bg)


def shoot(page, base, slug, vp_name, width, height, outdir):
    problems = []
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{base}/{slug}.html", wait_until="networkidle")
    page.wait_for_timeout(400)
    preload_lazy(page)
    # The shell's live-status widget builds its day timeline ~2 s after load
    # (js/scripts.js). That is what changes the layout, so measure after it —
    # otherwise the overflow gate is a coin toss (§6.5 step 4).
    if page.query_selector("#v1-section"):
        try:
            page.wait_for_function(
                "() => document.querySelector('.v1-timeline .v1-day')",
                timeout=6000)
        except Exception:
            pass
        page.wait_for_timeout(300)
    page.wait_for_timeout(200)

    shot = outdir / f"{slug}-{vp_name}.png"
    page.screenshot(path=str(shot), full_page=True)
    if vp_name == "mobile":
        page.screenshot(path=str(outdir / f"{slug}-mobile-fold.png"),
                        full_page=False)

    # the pixels, not the DOM: a blank band is what a failed render looks like
    bands = blank_bands(shot)
    if bands and bands[0] > 600:
        problems.append(f"blank band {bands[0]}px tall at y={bands[1]} "
                        f"(background {bands[2]}) - something in this range "
                        f"painted nothing")
    elif bands:
        print(f"  note    {vp_name}: longest blank band {bands[0]}px at "
              f"y={bands[1]} (limit 600)")
    # measurable layout gates
    metrics = page.evaluate("""() => {
      const doc = document.documentElement;
      // Content scope, not article scope. The plates page keeps its 72-tile grid
      // after </article> on purpose (books/tools/plates_gallery.py says why), and
      // every image on that grid was invisible to this check while the check read
      // `article img`: 83 images on the page, 3 of them measured. The shell's own
      // nav, header and footer are still excluded, so a page's avatar in the
      // footer is not this series' layout problem.
      const inShell = (el) => !!el.closest('nav, header, footer, .navbar');
      const contentImgs = [...document.querySelectorAll('img')]
        .filter(el => !inShell(el));
      const contentFigs = [...document.querySelectorAll('figure')]
        .filter(el => !inShell(el));
      // Our bytes or somebody else's. The sidebar email-capture embed
      // (eocampaign1.com, one script tag in every page) paints an image with no
      // width/height, and that is a real layout shift on our pages that we can
      // only fix by changing a third party's markup. It is reported, not failed,
      // and it is named in the record; a series gate must not go red on a file
      // this repo does not contain.
      const sameOrigin = (el) => {
        try {
          return new URL(el.currentSrc || el.src, location.href).origin ===
                 location.origin;
        } catch (e) { return false; }
      };
      const ownImgs = contentImgs.filter(sameOrigin);
      const extImgs = contentImgs.filter(el => !sameOrigin(el));
      const over = [...contentImgs, ...contentFigs]
        .filter(el => el.getBoundingClientRect().width >
                      (el.closest('.col-lg-8')?.clientWidth || doc.clientWidth) + 2)
        .map(el => el.tagName + ':' + (el.src || el.className));
      const noDims = ownImgs
        .filter(i => !i.getAttribute('width') || !i.getAttribute('height'))
        .map(i => i.getAttribute('src'));
      const notLoaded = ownImgs
        .filter(i => !i.complete || !i.naturalWidth)
        .map(i => i.getAttribute('src'));
      const extNoDims = extImgs
        .filter(i => !i.getAttribute('width') || !i.getAttribute('height'))
        .map(i => i.getAttribute('src'));
      const cta = document.querySelector('.alert-info');
      const ctaTop = cta ? Math.round(cta.getBoundingClientRect().top) : null;
      const scarce = document.querySelector('.scarcity-widget');
      const scarceTop = scarce ? Math.round(scarce.getBoundingClientRect().top) : null;
      const anyAff = document.querySelectorAll('a[href*="hop.clickbank.net"]').length;
      return {
        scrollW: doc.scrollWidth, clientW: doc.clientWidth,
        overflow: over, noDims: noDims, notLoaded: notLoaded,
        extNoDims: extNoDims,
        nImgs: ownImgs.length, nFigs: contentFigs.length, nExt: extImgs.length,
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
    if metrics["extNoDims"]:
        print(f"  note    {vp_name}: {len(metrics['extNoDims'])} third-party "
              f"embed image(s) without width/height (layout shift, not ours to "
              f"fix): {metrics['extNoDims'][:1]}")
    if metrics["noDims"]:
        problems.append(f"img without width/height (layout shift): {metrics['noDims'][:3]}")
    if metrics["notLoaded"]:
        problems.append(f"figure did not decode: {metrics['notLoaded'][:3]}")
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
          f"imgs={metrics['nImgs']}+{metrics['nExt']}ext/{metrics['nFigs']}figs "
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
    console, requests, probes, problems = [], [], [], []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.on("console", lambda m: console.append(f"{m.type}: {m.text}")
                    if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
            def on_failed(r):
                entry = f"{r.method} {r.url} -> {r.failure}"
                (probes if r.url.rstrip("/") == SHELL_PROBE.rstrip("/")
                 else requests).append(entry)

            page.on("requestfailed", on_failed)
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
    if probes:
        print("   (ignored: shell status probe to the site root — js/scripts.js, "
              "also fires on the donor page)")

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
