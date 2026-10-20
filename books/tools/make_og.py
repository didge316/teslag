#!/usr/bin/env python3
"""Render the 1894 series OG cards: 1200x630 webp, one per series page.

SERIES-PLAN-1894.md section 6.4: "left 60% best engraving on paper tone #efe9dd,
right 40% title + The 1894 File + page cite ... website/assets/og/<slug>.webp,
<= 120 KB" and section 12's visual gate "OG image: title readable at 300 px wide".

    python3 books/tools/make_og.py --all                     # build all 15
    python3 books/tools/make_og.py tesla-cold-flame          # build one
    python3 books/tools/make_og.py --all --preview           # + 300 px PNGs to
        #   books/tmp/og-preview/ for the eyes. The 300 px view is the gate;
        #   this tool cannot pass it, it can only make the thing to look at.

Every card prints its own measured numbers: the title font size that was chosen,
what that size becomes when the card is shown 300 px wide (the legibility rule),
and the byte count against the 120 KB cap. A card whose title drops under
LEG_FLOOR px at 300 px is reported as TOO SMALL, not silently shipped.

Source crops and page cites are the table below, not a guess at runtime: each
entry names a file already committed under website/assets/tesla1894/ and the
printed page it was verified against, so the cite on the card is the same cite
the article uses.

CREDIT for every image used here, recorded in the tool rather than in a comment
on the card: public-domain engravings and scan crops from "Inventions,
Researches and Writings of Nikola Tesla", Century Magazine 1894, accessed as
archive.org item inventionsresear00martiala. Printed page = scan file - 18;
front matter has no printed folio and is cited by scan file.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
WEB = ROOT / "website"
ASSETS = WEB / "assets" / "tesla1894"
OUT = WEB / "assets" / "og"

W, H = 1200, 630
PANEL = 720                       # left 60% per spec 6.4
PAPER = (239, 233, 221)           # #efe9dd, the paper tone spec 6.4 names
INK = (24, 22, 20)               # #181614, the ink tone used in section 6.4
ACCENT = (122, 30, 17)           # #7a1e11, the series accent red
MUTED = (74, 66, 56)             # #4a4238, for the cite line
RULE = (201, 191, 168)           # #c9bfa8, hairline between the panels

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE_MAX, TITLE_MIN = 64, 40    # px at 1200 wide
LEG_FLOOR = 14                   # px the title must still be at 300 wide
MAX_BYTES = 120 * 1024           # spec 6.4 cap

# slug -> (source crop(s) under assets/tesla1894/, cite line, display title).
# A tuple of crops is laid out as a 2x2 grid instead of one image.
# The cite line is what the card prints; it must name the figure or page the
# crop on the card actually comes from, so a card and its page agree.
# Every crop here is verdict=keep, quality=A in assets/tesla1894/manifest_qc.csv
# unless the comment says otherwise; the subject quoted there is why it was chosen.
# Display title defaults to the page's own <title> text; a shorter one is used
# only where the full title cannot be set at a legible size, and the reason is
# in the comment.
CARDS = {
    "tesla-1894": (
        "scan-title-page.webp",
        "(1894, scan file 9: the title page)",
        None),                       # hub: the title page is the honest image
    "tesla-lit-lamps-without-wires": (
        "p179-figs116-117.webp", "(1894, p. 179, Figs. 116-117)", None),
    "tesla-one-wire-power": (
        "p234-fig146.webp", "(1894, p. 234, Fig. 146)", None),
    "tesla-earthquake-machine": (
        "p509-fig1-fig313.webp", "(1894, p. 509, Fig. 313)", None),
    "tesla-wireless-power-1893": (
        "p344-fig184.webp", "(1894, p. 344, Fig. 184)", None),
    "tesla-high-frequency-massage": (
        "p392-fig208.webp", "(1894, p. 392, Fig. 208)", None),
    "tesla-cold-flame": (
        "p165-fig110.webp", "(1894, p. 165, Fig. 110)", None),
    "rotating-magnetic-field-1888": (
        "p016-fig9.webp", "(1894, p. 16, Fig. 9)", None),
    "tesla-weird-inventions-1894": (
        "p410-fig220.webp", "(1894, p. 410, Fig. 220)", None),
    "tesla-worlds-fair-1893": (
        "plate-p478-fig297.webp", "(1894, p. 478, Fig. 297)", None),
    "tesla-free-energy-what-he-said": (
        "p430-fig242.webp", "(1894, p. 430, Fig. 242)", None),
    # Fig. 210 (a bulb drawn in section, 785x939) rather than the Fig. 163/164
    # pair: the pair is two tall narrow tubes and leaves the panel two-thirds
    # empty paper at 300 px. Same subject, verified keep/A, fills the frame.
    "tesla-glowing-tubes-vacuum": (
        "p397-fig210.webp", "(1894, p. 397, Fig. 210)", None),
    "tesla-high-frequency-alternator": (
        "p375-fig199.webp", "(1894, p. 375, Fig. 199)", None),
    # a grid, not one plate: this page is a gallery, and its card must not be
    # the same picture as the World's Fair article's card. Four keep/A crops:
    # Fig. 205 plan view of a machine, Fig. 207 section through one, Fig. 227 a
    # plate stack in section, Fig. 298 a laminated-iron ring field on a plank.
    "tesla-1894-plates": (
        ("p396-fig1-fig205.webp", "p397-fig1-fig207.webp",
         "p418-fig227.webp", "p480-fig298.webp"),
        "(1894, Figs. 205, 207, 227, 298)", None),
    # the volume's own index, top of the left column, ending at the entry
    # "Pyromagnetic Generators" - the word-search page's whole point, in the
    # book's own type. The Ch. XXXVI heading crop is only 1641x240 and reads as
    # a blank card at 300 px, so it is not the card image.
    "tesla-1894-word-search": (
        "scan-p496-index.webp", "(1894, p. 496: the volume's own index)",
        None),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def measure(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, f, width):
    """Greedy word wrap. A word may break after a hyphen it already contains -
    that is normal typography, and "High-Frequency" is the longest token in this
    series' titles, so refusing to break it is what forces a card's type down.
    No hyphen is ever *inserted*: an invented hyphen in a card title reads as a
    typo."""
    pieces = []
    for w_ in text.split():
        parts = w_.split("-")
        for i, p in enumerate(parts):
            if not p:
                continue
            pieces.append(p + ("-" if i < len(parts) - 1 else ""))
    lines, cur = [], ""
    for i, piece in enumerate(pieces):
        glued = piece if (not cur or cur.endswith("-")) else " " + piece
        trial = cur + glued
        if not cur or measure(draw, trial, f)[0] <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = piece
    if cur:
        lines.append(cur)
    return lines


def fit_title(draw, title, box_w, box_h):
    """Largest title size whose wrapped form fits box_h. Returns (size, lines)."""
    for size in range(TITLE_MAX, TITLE_MIN - 1, -2):
        f = font(SERIF_BOLD, size)
        lines = wrap(draw, title, f, box_w)
        lead = round(size * 1.14)
        if len(lines) * lead <= box_h and all(
                measure(draw, ln, f)[0] <= box_w for ln in lines):
            return size, lines, lead, f
    # floor: report it, do not silently ship an unreadable card
    f = font(SERIF_BOLD, TITLE_MIN)
    return TITLE_MIN, wrap(draw, title, f, box_w), round(TITLE_MIN * 1.14), f


def fit_line(draw, text, path, hi, lo, width):
    """Largest size at which text fits one line, down to lo px; below lo it
    wraps. Returns (font, lines)."""
    for size in range(hi, lo - 1, -1):
        f = font(path, size)
        if measure(draw, text, f)[0] <= width:
            return f, [text]
    f = font(path, lo)
    return f, wrap(draw, text, f, width)


def letterspace(draw, text, f, x, y, fill, tracking):
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += measure(draw, ch, f)[0] + tracking
    return x


def contain(im, box_w, box_h, max_up=1.6):
    """Fit an image in a box without distortion. Never upscale more than max_up:
    a blown-up 1894 line scan turns to mush, and the extra paper margin is the
    honest way to show a small crop."""
    scale = min(box_w / im.width, box_h / im.height, max_up)
    return im.resize((max(1, round(im.width * scale)),
                      max(1, round(im.height * scale))), Image.LANCZOS)


def paste_figure(canvas, srcs):
    """Left 60%: the engraving(s) contained in the panel, centred, on paper
    tone. Several crops are laid out 2x2 with a paper gutter."""
    srcs = [srcs] if isinstance(srcs, str) else list(srcs)
    pad = 34
    box_w, box_h = PANEL - 2 * pad, H - 2 * pad
    draw = ImageDraw.Draw(canvas)
    boxes = []
    if len(srcs) == 1:
        boxes.append((pad, pad, box_w, box_h))
    else:
        gut = 18
        cols = 2
        rows = -(-len(srcs) // cols)
        cw = (box_w - (cols - 1) * gut) // cols
        chh = (box_h - (rows - 1) * gut) // rows
        for i in range(len(srcs)):
            r, c = divmod(i, cols)
            boxes.append((pad + c * (cw + gut), pad + r * (chh + gut),
                          cw, chh))
    placed = []
    for (bx, by, bw, bh), src in zip(boxes, srcs):
        im = contain(Image.open(src).convert("RGB"), bw, bh)
        x = bx + (bw - im.width) // 2
        y = by + (bh - im.height) // 2
        canvas.paste(im, (x, y))
        draw.rectangle([x - 1, y - 1, x + im.width, y + im.height],
                       outline=RULE, width=1)
        placed.append((x, y, im.width, im.height))
    return placed[0] if len(placed) == 1 else tuple(placed)


def build(slug, src, cite, title, out_dir=OUT):
    srcs = [src] if isinstance(src, str) else list(src)
    paths = [ASSETS / s for s in srcs]
    for p in paths:
        if not p.exists():
            raise SystemExit(f"{slug}: source crop does not exist: {p}")
    canvas = Image.new("RGB", (W, H), PAPER)
    fig = paste_figure(canvas, paths)

    draw = ImageDraw.Draw(canvas)
    x0 = PANEL + 44
    x1 = W - 44
    text_w = x1 - x0

    # kicker: the series name, letterspaced, in the accent red
    kf = font(SANS_BOLD, 25)
    letterspace(draw, "THE 1894 FILE", kf, x0, 46, ACCENT, 3)
    draw.rectangle([x0, 92, x1, 93], fill=RULE)

    # cite line: the same form the articles use, so a card and its page agree.
    # fit_line, not a fixed size: the longest cite in the table is 40 characters
    # and at 26 px it ran off the card edge in the first build. A clipped cite
    # is worse than a smaller one, but a shrunk cite must still be readable, so
    # the floor is 17 px and below that the line wraps instead.
    cf, cite_lines = fit_line(draw, cite, SANS_BOLD, 26, 17, text_w)
    # credit line: the short form. The full credit, with the archive.org item id,
    # is in this file's docstring and in the series' own "how we cite" box.
    sf, credit_lines = fit_line(draw, CREDIT_ON_CARD, SANS, 19, 14, text_w)
    cite_lead, cred_lead = round(cf.size * 1.25), round(sf.size * 1.3)
    block = len(cite_lines) * cite_lead + 8 + len(credit_lines) * cred_lead

    # title: auto-fit into whatever height the kicker and the cite block leave
    top, bottom = 118, H - 44 - block
    size, lines, lead, tf = fit_title(draw, title, text_w, bottom - top)
    y = top
    for ln in lines:
        draw.text((x0, y), ln, font=tf, fill=INK)
        y += lead
    if y > bottom:
        raise SystemExit(f"{slug}: title block overruns the cite block")

    cy = bottom
    for ln in cite_lines:
        draw.text((x0, cy), ln, font=cf, fill=ACCENT)
        cy += cite_lead
    cy += 8
    for ln in credit_lines:
        draw.text((x0, cy), ln, font=sf, fill=MUTED)
        cy += cred_lead

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug}.webp"
    quality = 82
    while True:
        canvas.save(out, "WEBP", quality=quality, method=6)
        if out.stat().st_size <= MAX_BYTES or quality <= 40:
            break
        quality -= 8
    return dict(slug=slug, out=out, title_size=size, lines=len(lines),
                at300=round(size * 300 / W), bytes=out.stat().st_size,
                quality=quality, fig=fig, cite=cite, src=srcs,
                cite_px=cf.size, credit_px=sf.size)


def page_title(slug):
    """The page's own <title> minus the site suffix, decoded from the HTML."""
    import html
    import re
    p = WEB / f"{slug}.html"
    m = re.search(r"<title>(.*?)</title>", p.read_text(), re.S)
    if not m:
        raise SystemExit(f"{slug}: no <title> in {p}")
    t = html.unescape(m.group(1)).strip()
    for sep in (" | ", " - ", " -"):
        if sep in t:
            t = t.split(sep)[0].strip()
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=
                                argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?", help="one slug, e.g. tesla-cold-flame")
    ap.add_argument("--all", action="store_true", help="all 15 series pages")
    ap.add_argument("--preview", action="store_true",
                    help="also write 300 px-wide PNGs to books/tmp/og-preview/")
    ap.add_argument("--out", default=str(OUT), help="override output dir")
    args = ap.parse_args()

    slugs = ([args.slug] if args.slug else
             list(CARDS) if args.all else None)
    if slugs is None:
        ap.error("give a slug or --all")
    missing = [s for s in slugs if s not in CARDS]
    if missing:
        raise SystemExit(f"no card entry for: {missing}")

    out_dir = Path(args.out)
    rows = []
    for slug in slugs:
        src, cite, display = CARDS[slug]
        title = display or page_title(slug)
        r = build(slug, src, cite, title, out_dir)
        rows.append(r)

    prev = ROOT / "books/tmp/og-preview"
    print(f"credit: {CREDIT}")
    print(f"{'slug':<34} {'src':<34} {'title':>5} {'at300':>5} {'cite':>4} "
          f"{'KB':>5}  verdict")
    bad = []
    for r in rows:
        legible = r["at300"] >= LEG_FLOOR
        size_ok = r["bytes"] <= MAX_BYTES
        verdict = "ok" if legible and size_ok else \
            ("TOO SMALL at 300px" if not legible else "OVER 120KB")
        if not legible or not size_ok:
            bad.append(r["slug"])
        srcname = "+".join(Path(s).stem for s in r["src"])
        print(f"{r['slug']:<34} {srcname:<34} {r['title_size']:>5} "
              f"{r['at300']:>5} {r['cite_px']:>4} {r['bytes'] // 1024:>5}  "
              f"{verdict}")
        if args.preview:
            prev.mkdir(parents=True, exist_ok=True)
            im = Image.open(r["out"])
            im.resize((300, round(300 * H / W)), Image.LANCZOS).save(
                prev / f"{r['slug']}-300.png")
    if args.preview:
        print(f"300 px previews -> {prev} (this is the gate; look at them)")
    if bad:
        print(f"\n{len(bad)} card(s) need a shorter display title or a "
              f"different crop: {bad}")
        return 1
    print(f"\n{len(rows)} cards written to {out_dir}")
    print("still to do by eye: view every card at 300 px wide (spec 12).")
    return 0


CREDIT = ("engravings and scan crops from the 1894 Century volume, archive.org "
          "item inventionsresear00martiala, public domain")
CREDIT_ON_CARD = "public domain, from the 1894 first edition"

if __name__ == "__main__":
    sys.exit(main())
