#!/usr/bin/env python3
"""Build labelled contact sheets of the 1894 figure crops for the vision QC pass.

SERIES-PLAN-1894.md §6.2 step 1 + §0.1 session-1 step 1.

    python3 books/tools/contact_sheet.py            # 12 sheets x 18 tiles, 300 px
    python3 books/tools/contact_sheet.py --tiles 36 # the §6.2 variant (6 sheets)

Each tile is labelled `file | p<printed> | Fig.<book> | WxH` so a verdict can be
written straight back into manifest_qc.csv by filename.

Also writes an empty manifest_qc.csv scaffold (headers per §6.2) so the QC pass
is a fill-in job rather than a setup job. The verdict columns are left blank on
purpose: they require eyes, and this session has none.
"""

import argparse
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TOOLS = Path(__file__).resolve().parent
ASSETS = TOOLS.parent.parent / "website" / "assets" / "tesla1894"
MANIFEST = ASSETS / "manifest.csv"
QC_DIR = ASSETS / "_qc"
QC_CSV = ASSETS / "manifest_qc.csv"

QC_HEADER = ["file", "verdict", "subject", "quality", "aspect_ok", "caption_ok",
             "notes"]
PAPER = (239, 233, 221)       # #efe9dd, the paper tone used in §6.4
INK = (24, 22, 20)


def font(size):
    for cand in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--out", default=str(QC_DIR))
    ap.add_argument("--tiles", type=int, default=18, help="tiles per sheet")
    ap.add_argument("--px", type=int, default=300, help="tile long edge, px")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--no-scaffold", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.manifest, newline="", encoding="utf-8")))
    if not rows:
        sys.exit(f"no rows in {args.manifest}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    cell = args.px + 20
    f_big, f_small = font(15), font(12)
    sheets = []
    missing = []

    for si in range(0, len(rows), args.tiles):
        group = rows[si:si + args.tiles]
        cols = args.cols
        rows_n = (len(group) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows_n * cell), (250, 248, 244))
        for i, r in enumerate(group):
            path = ASSETS / r["file"]
            if not path.exists():
                missing.append(r["file"])
                continue
            try:
                img = Image.open(path)
            except Exception as e:
                missing.append(f"{r['file']} ({e})")
                continue
            label = (f"{r['file']}\n"
                     f"p{r['printed_page']}  Fig.{r['book_fig']}  "
                     f"{r['px_w']}x{r['px_h']}")
            t = _tile(img, label, (cell, cell), f_big, f_small)
            sheet.paste(t, ((i % cols) * cell, (i // cols) * cell))
        name = out_dir / f"sheet-{si // args.tiles + 1:02d}.png"
        sheet.save(name)
        sheets.append(name)

    if not args.no_scaffold:
        with open(QC_CSV, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(QC_HEADER)
            for r in rows:
                w.writerow([r["file"], "", "", "", "", "", ""])

    print(f"{len(rows)} crops -> {len(sheets)} sheets of {args.tiles} tiles "
          f"({args.px}px) in {out_dir}")
    for s in sheets:
        print("  ", s.name)
    if missing:
        print(f"unreadable/missing: {missing}")
    if not args.no_scaffold:
        print(f"scaffold: {QC_CSV}  (verdict columns blank — needs a vision pass)")
    return 0


def _tile(img, label, box, fnt, small):
    w, h = box
    cell = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(cell)
    pad, label_h = 6, 40
    im = img.convert("RGBA")
    im.thumbnail((w - 2 * pad, h - 2 * pad - label_h), Image.LANCZOS)
    x = (w - im.width) // 2
    y = pad + (h - 2 * pad - label_h - im.height) // 2
    cell.paste(im, (x, y), im)
    d.rectangle([0, h - label_h, w, h], fill=(252, 250, 247))
    d.multiline_text((pad, h - label_h + 4), label, font=fnt, fill=INK, spacing=2)
    d.rectangle([0, 0, w - 1, h - 1], outline=(180, 172, 158))
    return cell


if __name__ == "__main__":
    sys.exit(main())
