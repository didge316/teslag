#!/usr/bin/env python3
"""Crop the parts of a shot_qa screenshot that §12 asks a human to look at.

shot_qa.py decides what is measurable (overflow, undecoded figures, figures wider
than the column, a missing nav dropdown). The rest of §12's visual half is by
eye: caption legibility, figure subjects, sidebar stacking, nav dropdown intact.
A 1280x11000 full-page PNG is useless for that, so this tool finds the boxes in
the live DOM and cuts them out of the screenshot shot_qa already wrote.

    python3 books/tools/shot_crops.py rotating-magnetic-field-1888
    python3 books/tools/shot_crops.py tesla-worlds-fair-1893 --viewport mobile

Writes website/_qa/<slug>-<viewport>-crops/<n>-<what>.png and prints the list.
Coordinates come from the same page at the same viewport, so they line up with
the full-page screenshot pixel for pixel (deviceScaleFactor is 1 in shot_qa).
"""

import argparse
import http.server
import socketserver
import threading
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parents[2] / "website"
QA = WEB / "_qa"
VIEWPORTS = {"mobile": (375, 812), "tablet": (768, 1024), "desktop": (1280, 900)}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, *a):
        pass


def serve(slug):
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


BOXES = """() => {
  const out = [];
  const push = (what, el) => {
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    out.push({what,
              x: r.x + window.scrollX, y: r.y + window.scrollY,
              w: r.width, h: r.height});
  };
  push('head', document.querySelector('article > h1')?.closest('div')
       || document.querySelector('article h1'));
  document.querySelectorAll('article figure').forEach(
    (f, i) => push('figure-' + (i + 1), f));
  const dd = document.querySelector('.navbar .dropdown-menu');
  if (dd) { dd.classList.add('show'); push('nav-dropdown', dd); }
  const cta = document.querySelector('article .alert-info')
           || document.querySelector('.alert-info');
  push('cta', cta);
  const src = document.querySelector('article .card, article section');
  const sources = [...document.querySelectorAll('article h2')]
      .find(h => /sources/i.test(h.textContent));
  if (sources) {
    const r = sources.getBoundingClientRect();
    let bottom = r.bottom, el = sources.nextElementSibling;
    while (el && el.tagName !== 'H2') {
      bottom = Math.max(bottom, el.getBoundingClientRect().bottom);
      el = el.nextElementSibling;
    }
    out.push({what: 'sources', x: r.x, y: r.y + window.scrollY,
              w: r.width, h: bottom - r.y});
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--viewport", default="desktop", choices=sorted(VIEWPORTS))
    ap.add_argument("--pad", type=int, default=14)
    args = ap.parse_args()

    shot = QA / f"{args.slug}-{args.viewport}.png"
    if not shot.exists():
        raise SystemExit(f"run shot_qa.py first: {shot} does not exist")
    img = Image.open(shot)
    width, height = img.size
    vw, vh = VIEWPORTS[args.viewport]
    if width != vw:
        raise SystemExit(f"{shot} is {width}px wide, expected {vw} for {args.viewport}")

    httpd, port = serve(args.slug)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": vw, "height": vh})
            page.goto(f"http://127.0.0.1:{port}/{args.slug}.html",
                      wait_until="networkidle")
            page.evaluate("""async () => {
              const step = Math.round(window.innerHeight * 0.8);
              for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 80));
              }
              window.scrollTo(0, 0);
              document.querySelectorAll('img[loading="lazy"]')
                .forEach(i => { i.loading = 'eager'; });
            }""")
            page.wait_for_timeout(600)
            boxes = page.evaluate(BOXES)
            browser.close()
    finally:
        httpd.shutdown()

    outdir = QA / f"{args.slug}-{args.viewport}-crops"
    outdir.mkdir(exist_ok=True)
    written = []
    for b in boxes:
        x0 = max(0, int(b["x"]) - args.pad)
        y0 = max(0, int(b["y"]) - args.pad)
        x1 = min(width, int(b["x"] + b["w"]) + args.pad)
        y1 = min(height, int(b["y"] + b["h"]) + args.pad)
        if y1 - y0 < 20 or x1 - x0 < 20:
            continue
        name = f"{b['what']}.png"
        img.crop((x0, y0, x1, y1)).save(outdir / name)
        written.append((str(outdir / name), (x1 - x0, y1 - y0)))
    for path, size in written:
        print(f"  {path}  {size[0]}x{size[1]}")
    print(f"{len(written)} crops from {shot.name} "
          f"(page {width}x{height}) -> review these, not the full shot")


if __name__ == "__main__":
    main()
