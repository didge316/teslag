#!/usr/bin/env python3
"""Extract engraving/figure crops from the 1894 Tesla page scans.

Strategy: render each page, mask out every row that the PDF text layer says
contains text, then keep the remaining ink bands (figures have no OCR text in
them). Each band is cropped to its ink bounding box, padded, and written as a
webp plus a row in manifest.csv.

Usage:
  ./extract_figures.py --pages 20-518 --out ../website/assets/tesla1894
  ./extract_figures.py --pages 100,102,392 --dry-run
"""
import argparse
import csv
import glob
import os
import re
import sys

import numpy as np
import pymupdf

BOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf-pages-tesla-1894")
# file page N == printed page N - 18 (verified against running headers)
PAGE_OFFSET = 18


def parse_pages(spec):
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(part))
    return sorted(pages)


def page_pdf(n):
    return os.path.join(BOOK_DIR, f"page-{n:03d}.pdf")


def caption_near(pdf_text_blocks, y0, y1):
    """Nearest 'Fig. NN' style caption above or below the figure band."""
    best = None
    for x0, ty0, x1, ty1, text, *_ in pdf_text_blocks:
        t = re.sub(r"\s+", " ", text).strip()
        m = re.search(r"F[II]?G\.?\s*([0-9]{1,3})", t, re.I)
        if not m:
            continue
        d = min(abs(ty1 - y0), abs(ty0 - y1))
        if best is None or d < best[0]:
            best = (d, m.group(1), t[:120])
    return best[1:] if best else (None, None)


def extract(pdf_path, dpi=300, min_h=110, min_w=220, min_area=45000, pad=14):
    doc = pymupdf.open(pdf_path)
    pg = doc[0]
    pix = pg.get_pixmap(dpi=dpi)
    arr = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    ink = arr.mean(axis=2) < 175
    scale = dpi / 72.0

    textrows = np.zeros(pix.height, bool)
    blocks = pg.get_text("blocks")
    for x0, y0, x1, y1, *_ in blocks:
        textrows[int(y0 * scale): int(y1 * scale) + 1] = True

    has_ink = ink.any(axis=1)
    bands, y = [], 0
    while y < pix.height:
        if has_ink[y] and not textrows[y]:
            y0 = y
            while y < pix.height and has_ink[y] and not textrows[y]:
                y += 1
            if y - y0 >= min_h:
                bands.append((y0, y))
        else:
            y += 1

    out = []
    for y0, y1 in bands:
        cols = ink[y0:y1].any(axis=0)
        xs = np.flatnonzero(cols)
        if xs.size == 0:
            continue
        x0, x1 = int(xs[0]), int(xs[-1])
        w, h = x1 - x0, y1 - y0
        if w < min_w or h < min_h or w * h < min_area:
            continue
        # reject page-edge junk (headers/footers/decorative rules)
        if x0 < 20 or x1 > pix.width - 20:  # page-edge junk / rules
            continue
        fig_no, cap = caption_near(blocks, y0, y1)
        out.append({
            "x0": max(0, x0 - pad), "y0": max(0, y0 - pad),
            "x1": min(pix.width, x1 + pad), "y1": min(pix.height, y1 + pad),
            "w": w, "h": h, "fig": fig_no, "caption": cap,
        })
    from PIL import Image
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="20-518")
    ap.add_argument("--out", default=os.path.join(BOOK_DIR, "..", "assets-out"))
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-gap-pages", type=int, default=0,
                    help="keep at most N figures per page (0 = all)")
    args = ap.parse_args()

    pages = parse_pages(args.pages)
    os.makedirs(args.out, exist_ok=True)
    manifest = os.path.join(args.out, "manifest.csv")
    rows = []
    total = 0

    for n in pages:
        pdf = page_pdf(n)
        if not os.path.exists(pdf):
            continue
        try:
            im, figs = extract(pdf, dpi=args.dpi)
        except Exception as e:                                  # noqa: BLE001
            print(f"page {n}: ERROR {e}", file=sys.stderr)
            continue
        if args.min_gap_pages:
            figs = figs[: args.min_gap_pages]
        for i, f in enumerate(figs, 1):
            name = f"p{n:03d}-fig{i}"
            if f["fig"]:
                name += f"-fig{f['fig']}"
            rows.append({
                "file": f"{name}.webp", "file_page": n, "printed_page": n - PAGE_OFFSET,
                "book_fig": f["fig"] or "", "caption": f["caption"] or "",
                "px_w": f["x1"] - f["x0"], "px_h": f["y1"] - f["y0"],
            })
            if not args.dry_run:
                im.crop((f["x0"], f["y0"], f["x1"], f["y1"])).save(
                    os.path.join(args.out, f"{name}.webp"), "WEBP", quality=88)
            total += 1
        if figs:
            print(f"page {n} (printed {n - PAGE_OFFSET}): {len(figs)} figure(s) "
                  + ", ".join(f"{f['w']}x{f['h']}" + (f" Fig.{f['fig']}" if f['fig'] else "") for f in figs))

    if not args.dry_run:
        with open(manifest, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["file"])
            w.writeheader()
            w.writerows(rows)
    print(f"\n{total} figure(s) from {len(pages)} page(s)"
          f"{' [dry run]' if args.dry_run else ' -> ' + args.out}")


if __name__ == "__main__":
    main()
