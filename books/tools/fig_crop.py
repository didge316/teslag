#!/usr/bin/env python3
"""Crop a figure out of a 1894 scan page, with the printed figure number in it.

SERIES-PLAN-1894.md §6.6 / §0.4: read the figure number off the printed page in
the scan, never from the caption the extractor put in the filename. So the crop
must include the printed "FIG. N." line. Same page rule as everywhere:

    printed page = scan file page - 18

Two modes:

    # 1. look at a whole page first (writes books/tmp/scan-p<NNN>.png)
    fig_crop.py --scan 30 --view

    # 2. crop it. --box is in pixels of the --ppi render used for looking
    fig_crop.py --scan 30 --box 120,300,1500,900 \
                --out website/assets/tesla1894/p012-figs3-4a.webp --ppi 400

The tool prints the output size and the printed page it came from, and refuses
to write outside website/assets/tesla1894/ unless --out is under books/tmp/.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]           # tesla-generator/
SCANS = ROOT / "books" / "pdf-pages-tesla-1894"
TMP = ROOT / "books" / "tmp"
ASSETS = ROOT / "website" / "assets" / "tesla1894"
PAGE_OFFSET = 18


def render(scan: int, ppi: int) -> Path:
    pdf = SCANS / f"page-{scan:03d}.pdf"
    if not pdf.exists():
        sys.exit(f"no scan page {pdf}")
    TMP.mkdir(parents=True, exist_ok=True)
    out = TMP / f"scan-p{scan:03d}-{ppi}ppi.png"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", str(ppi), "-png", "-singlefile",
                        str(pdf), str(out.with_suffix(""))], check=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--scan", type=int, help="scan file page number")
    g.add_argument("--printed", type=int, help="printed page number (scan = +18)")
    ap.add_argument("--view", action="store_true", help="render the whole page for looking")
    ap.add_argument("--box", help="x0,y0,x1,y1 in pixels of the --ppi render")
    ap.add_argument("--out")
    ap.add_argument("--ppi", type=int, default=400)
    ap.add_argument("--view-ppi", type=int, default=100)
    ap.add_argument("--autocontrast", action="store_true",
                    help="stretch levels (for dark plates, cf. p480-fig298)")
    args = ap.parse_args()

    scan = args.scan if args.scan else args.printed + PAGE_OFFSET
    printed = scan - PAGE_OFFSET

    if args.view:
        png = render(scan, args.view_ppi)
        print(f"scan {scan} (printed p. {printed}) -> {png} at {args.view_ppi} ppi")
        print("box coordinates for --box are in pixels of a --ppi render; "
              f"scale the box you read off this preview by {args.ppi / args.view_ppi:g}")
        return 0

    if not (args.box and args.out):
        sys.exit("--box and --out are required in crop mode")

    png = render(scan, args.ppi)
    from PIL import Image
    im = Image.open(png)
    x0, y0, x1, y1 = (int(v) for v in args.box.split(","))
    if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
        sys.exit(f"box {args.box} outside the {im.width}x{im.height} render")
    crop = im.crop((x0, y0, x1, y1))
    if args.autocontrast:
        from PIL import ImageOps
        crop = ImageOps.autocontrast(crop)
    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    if not (str(out).startswith(str(ASSETS)) or str(out).startswith(str(TMP))):
        sys.exit(f"refusing to write {out}; must be under {ASSETS} or {TMP}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in (".webp", ".jpg", ".jpeg"):
        crop.save(out, quality=92)
    else:
        crop.save(out)
    print(f"wrote {out}  {crop.width}x{crop.height}  "
          f"from scan {scan} = printed p. {printed}  ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
