#!/usr/bin/env python3
"""Build the 1894 plates gallery: the selection, the page, the thumbnails, the ZIP.

SERIES-PLAN-1894.md §16.3(1) / §10 Tier 6 `tesla-1894-plates`: 60+ engravings,
page-cited, in a lazy-loaded grid, each with printed page, book Fig. number and
chapter, plus a downloadable ZIP and a one-line licence statement.

    plates_gallery.py --select     # write the selection record, print the report
    plates_gallery.py --thumbs     # write the grid thumbnails into website/assets
    plates_gallery.py --zip        # write the 1200 px download ZIP
    plates_gallery.py --build      # render website/tesla-1894-plates.html
    plates_gallery.py --all        # select, thumbs, zip, build

How a plate gets in (the rules are printed on the page itself, because that is
what makes the page citable):

  1. the row in manifest_qc.csv is verdict=keep and quality A or B (§6.2 QC);
  2. the printed figure number is settled: caption_ok=yes, and the row's own
     notes do not say the number was mis-read, contradicted or left unsettled;
  3. the file is one of the book's own figures. Page-scan crops (scan-*.webp)
     and patent sheets (patents/) are not book engravings, so they are out;
  4. one plate per printed figure: where the extractor crop and a later hand
     crop cover the same printed figure, the hand crop wins, because it was cut
     after the page was opened at 400-500 ppi and its notes name the scan;
  5. a per-chapter cap, so the gallery is the volume and not chapter III.

Everything the rules cannot decide is decided by hand in
new_content/1894-series/plates/overrides.json, which names the file and the
reason. The selection record it writes is the audit trail: every plate with its
printed page, printed figure number, chapter, quality grade, the manifest row it
came from, and the caption text the page will carry.

Captions are built from the printed page, never from the extractor filename: the
printed page number (scan file - 18), the figure number as the book prints it,
the chapter the book puts it in (books/extracted/chapters-1894.json, read off
the printed contents pages), and what the plate actually shows, which is the
subject line the §6.2 vision pass wrote while looking at the crop.

A plate only carries a figure number once that number has been read off the page
the plate was cut from. See the caption block below for how that reading works
and what it does when the scan's text layer cannot read the caption line; the
short version is that the number comes from the print, and where the print could
not be read the plate is left out.
"""

import argparse
import csv
import json
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

from PIL import Image

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import make_article as MA            # noqa: E402
import titlecase_headings as TC      # noqa: E402

ROOT = TOOLS.parent.parent                       # tesla-generator/
WEB = ROOT / "website"
ASSETS = WEB / "assets" / "tesla1894"
MANIFEST = ASSETS / "manifest_qc.csv"
CHAPTERS = ROOT / "books" / "extracted" / "chapters-1894.json"
WORK = ROOT / "new_content" / "1894-series" / "plates"
SELECTION = WORK / "selection.json"
OVERRIDES = WORK / "overrides.json"
DRAFT = WORK / "article.md"
OUT = WEB / "tesla-1894-plates.html"
THUMBS = ASSETS / "thumbs"
ZIP = ASSETS / "tesla-1894-plates.zip"
DONOR = WEB / "nikola-tesla-inventor-extraordinaire.html"

PAGE_OFFSET = 18
TARGET = 72          # §16.3 asks for 60; 72 leaves the page honest if a plate is later pulled
PER_CHAPTER_CAP = 6
THUMB_LONG_EDGE = 480
ZIP_LONG_EDGE = 1200

# A row whose own notes say the figure number is not trustworthy cannot carry a
# figure number in its caption. These are the words the QC pass used.
UNSETTLED = re.compile(
    r"number (?:not settled|wrong|contradicted)|not settled|superseded|"
    r"do not (?:trust|cite) that figure|number likely wrong|mis-read of fig|"
    r"number unreliable", re.I)
# ... and the words it used when the description line was wrong and the note
# carries the corrected reading. Those rows need a hand-written caption.
CORRECTED = re.compile(r"subject (?:line )?(?:wrong|contradicted)|wrong comparison",
                       re.I)

# A caption says what the plate shows. The newer subject lines also say where the
# crop came from, because the person writing the row was recording the making of
# the file, and that part is not a caption: 'Fig. 297 re-exported at 400 ppi from
# scan file 496 and rotated to landscape: long table of motors...' and '; printed
# FIG. 208. caption inside the crop' are bookkeeping. The two rules below take the
# provenance clause out and leave the description of the plate standing.
PROV_CLAUSE = re.compile(r"^[^:]{1,200}:\s*", re.I)
PROV_MARK = re.compile(
    r"ppi|scan file|scan-file|re-?export|re-?crop|rotated|brightened|dewarp|"
    r"rescaled|supersede|verified|printed p\.?\s*\d", re.I)
PROV_TAIL = [
    re.compile(r"[,;]?\s*[^,;]*\bcrop\b[^,;]*\.?\s*$", re.I),
    re.compile(r"[,;]?\s*from scan files? \d+[^,;]*\.?\s*$", re.I),
]

NAME_OLD = re.compile(r"^p(\d{3})-fig(\d+)-fig(\d{1,3}[a-z]?)\.webp$")
NAME_RANGE = re.compile(r"^(?:plate-)?p(\d{3})-figs(\d{1,3})-(\d{1,3})\.webp$")
NAME_NEW = re.compile(r"^(?:plate-)?p(\d{3})-fig(\d{1,3}[a-z]?)\.webp$")


def parse_name(fname):
    """(printed page, [printed figure numbers], crop kind) for a manifest file.

    Two naming conventions live in the same folder and they do not mean the same
    number, which is the trap here:

      p037-fig1-fig13.webp   the extractor's name: scan file 37, band 1, the
                             caption the OCR read was "FIG. 13."  -> printed 19
      p392-fig208.webp       a hand crop made later, named for the PRINTED page
                             and the figure number read off that page by eye.

    The extractor name carries the scan file, so the offset rule applies to it;
    the hand crop is already named for the printed page.
    """
    f = Path(fname).name
    if (m := NAME_RANGE.match(f)):
        return int(m.group(1)), [m.group(2), m.group(3)], "hand"
    if (m := NAME_NEW.match(f)):
        return int(m.group(1)), [m.group(2)], "hand"
    if (m := NAME_OLD.match(f)):
        return int(m.group(1)) - PAGE_OFFSET, [m.group(3)], "extractor"
    return None


def chapter_of(chapters, page):
    cur = None
    for c in chapters:
        if c["from_page"] > page:
            break
        cur = c
    return cur


def part_of(parts, page):
    cur = None
    for p in parts:
        if p["from_page"] > page:
            break
        cur = p
    return cur


def fig_label(figs):
    """How the caption names the plate's figures, in the order the page sets them.

    The order is the page's, not a sorted one: printed p. 426 sets its three
    captions as 'FIG. 234.', 'FIG. 236.', 'FIG. 235.' across the width of the
    plate, and a caption that quietly re-sorts that is not quoting the page.
    """
    if len(figs) == 1:
        return f"Fig. {figs[0]}"
    if len(figs) == 2:
        # p482-figs300-308.webp is one plate that carries nine printed figures,
        # 300 through 308; a hand crop named for its ends is a range, not a pair.
        try:
            if abs(int(figs[1]) - int(figs[0])) > 1:
                return f"Figs. {figs[0]} to {figs[1]}"
        except ValueError:
            pass
        return f"Figs. {figs[0]} and {figs[1]}"
    return "Figs. " + ", ".join(figs[:-1]) + " and " + figs[-1]


LEAD_MEDIUM = re.compile(
    r"^\s*(engraving|engravings|photograph|photographs|plate|plates|diagram|"
    r"line drawing|line diagrams|halftone)\s*[,:]?\s*", re.I)
# The figure word has to be followed by a separator, not by more of the
# description: 'Fig. 208: a ring marked A' names the plate and then describes it,
# while 'Fig. 163 (left) and Fig. 164 (right), each a tall sealed tube' is the
# description itself and taking its first words out would break the sentence.
LEAD_FIG = re.compile(
    r"^\s*figs?\.?\s*\d+[a-z]?(?:\s*(?:and|to|-)\s*\d+[a-z]?)?\s*[,:]\s*", re.I)
LEAD_PAGE = re.compile(r"^\s*printed\s*p\.?\s*\d+\s*[,:]?\s*", re.I)


def clean_subject(subject, figs):
    """The QC subject line with its own bookkeeping taken out.

    The newer rows begin 'Engraving, Fig. 208:' or 'Fig. 218, printed p.403:'
    because the person writing the row was naming the file. The caption states
    the figure and the page itself, so those prefixes would be said twice. The
    same rows also carry the making of the file inside the sentence ('re-exported
    at 400 ppi from scan file 496 and rotated to landscape') and a tail saying
    the printed caption sits inside the crop; both are about our file, not about
    the plate, and both come out.
    """
    s = re.sub(r"\s+", " ", subject).strip()
    medium = None
    for _ in range(4):
        if (m := LEAD_MEDIUM.match(s)):
            medium = m.group(1).lower()
            s = s[m.end():]
            continue
        if (m := LEAD_FIG.match(s)):
            s = s[m.end():]
            continue
        if (m := LEAD_PAGE.match(s)):
            s = s[m.end():]
            continue
        break
    # A clause that names the making of the file, and a tail that says the
    # printed caption is inside the crop, are both about our file, not about the
    # plate. They come out; what is left is what the plate shows.
    if (m := PROV_CLAUSE.match(s)) and PROV_MARK.search(m.group(0)):
        s = s[m.end():]
    for pat in PROV_TAIL:
        s = pat.sub("", s)
    s = s.strip(" .,:-")
    if s:
        s = s[0].upper() + s[1:]
    return s, medium


def medium_of(row, subject_medium):
    if subject_medium:
        return "photograph" if subject_medium in ("photograph", "halftone", "plate") else "engraving"
    if re.search(r"photograph|halftone", row["subject"] + " " + row["notes"], re.I):
        return "photograph"
    return "engraving"


# ------------------------------------------------- caption verification

# A published caption needs the caption the page prints under the plate. The
# number in an extractor file name is the number nearest the crop in the scan's
# text layer, which is a different thing: scan 32 (printed p. 14) sets 'FIG. 7.'
# and 'FIG. 7a.' under the plate it cut, while the text layer of that same page
# also contains 'Fig. 9.' inside a body paragraph, and 'fig9' is what the file
# is called. So the check here is positional rather than textual.
#
#   1. Re-derive the ink band the extractor cut for that file: same code, same
#      300 ppi, same order. This reproduces the published crops - measured at
#      this task, 72 of the 73 extractor-named files in the pool match their
#      re-derived band box to the pixel, and the 73rd (p509-fig1-fig313.webp)
#      is 56 px off, which is recorded rather than hidden.
#   2. Read the text lines in the strip between that band and the next figure on
#      the page, and take the figure numbers those lines set as captions. A body
#      paragraph that happens to mention a figure is not a caption line: it has
#      to start with the figure word and say nothing else.
#   3. Where the crop is wider than one figure - the extractor's bands run
#      across two or three figures the page captions separately - the caption
#      strip names them all, and the caption says so: 'Figs. 290 and 291'.
#
# The text layer is unreliable on caption lines, because the book sets them in
# small caps: 'FIG. 1.' comes out as 'Fie. l.', 'FIG. 7a.' as 'FIG. Ta.',
# 'FIGS. 45, 46 and 47.' as 'Fms. 45, 46 and 47.'. The reader normalizes only
# the letter-for-digit confusions this scan actually makes (NORM), and the
# selection record carries the line exactly as the layer gave it, so every
# normalization can be checked against the line it came from.
#
# Where the line under a plate is not in the text layer at all, or is there with
# its number unreadable, the plate is settled by eye against the page render and
# recorded in overrides.json under "verify", which carries the caption as the
# page prints it and the render it was read from. A plate that was neither read
# nor seen is left out: the gallery publishes numbers it can point at.

NORM = {"l": "1", "I": "1", "|": "1", "!": "1", "O": "0", "o": "0", "Q": "0",
        "D": "0", "S": "5", "s": "5", "B": "8", "Z": "2", "z": "2", "T": "7",
        "t": "7", "g": "9", "q": "9"}
FIGWORD = re.compile(r"\bF[A-Za-z]{1,4}\b", re.I)
CAPTION_LEAD = re.compile(r"^[^A-Za-z]{0,8}F[A-Za-z]{1,4}[.\s]", re.I)
CAPTION_NEAR = 120      # px at 300 ppi: a caption sits under its own plate
ADJACENT = 3            # 290 and 291 under one wide band describe that one crop


def norm_number(tok):
    """'Ta' -> '7a', 'l' -> '1', '45' -> '45'; None if the token is not a number."""
    out, i = [], 0
    while i < len(tok) and (tok[i].isdigit() or tok[i] in NORM):
        out.append(NORM.get(tok[i], tok[i]))
        i += 1
    if not out:
        return None
    suffix = tok[i:]
    if suffix and not re.fullmatch(r"[a-z]{1,2}", suffix):
        return None
    return "".join(out) + suffix.lower()


def caption_numbers(line):
    """The figure numbers a caption line sets, in the order the page sets them."""
    m = FIGWORD.search(line)
    if not m:
        return []
    return [n for n in (norm_number(t)
                        for t in re.findall(r"[0-9A-Za-z]{1,6}", line[m.end():]))
            if n]


def is_caption_line(line):
    """True only for a line that is nothing but a figure caption.

    'Fig. 43 shows a somewhat modified arrangement of circuits.' starts with the
    figure word and is still prose. Stripping the figure words, the numbers and
    the separators has to leave nothing behind.
    """
    if not CAPTION_LEAD.match(line) or len(line) > 60:
        return False
    rest = FIGWORD.sub(" ", line)
    rest = re.sub(r"[0-9A-Za-z]{1,6}", " ", rest)
    rest = re.sub(r"[\s.,;:&()andto-]+", "", rest)
    return len(rest) <= 2


_PAGE_CACHE = {}


def page_scan(scan):
    """(ink bands, text lines in pixels) for one scan page, read once."""
    if scan in _PAGE_CACHE:
        return _PAGE_CACHE[scan]
    import extract_figures as EF
    import pymupdf
    pdf = ROOT / "books" / "pdf-pages-tesla-1894" / f"page-{scan:03d}.pdf"
    if not pdf.exists():
        _PAGE_CACHE[scan] = None
        return None
    _, bands = EF.extract(str(pdf), dpi=300)
    scale = 300 / 72.0
    lines = []
    for b in pymupdf.open(str(pdf))[0].get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            s = re.sub(r"\s+", " ", "".join(sp["text"] for sp in l["spans"])).strip()
            if not s:
                continue
            x0, y0, x1, y1 = l["bbox"]
            lines.append((x0 * scale, y0 * scale, x1 * scale, y1 * scale, s))
    _PAGE_CACHE[scan] = (bands, lines)
    return _PAGE_CACHE[scan]


def band_caption(scan, idx):
    """(numbers, caption lines) for the strip of print under one ink band.

    The strip stops at the next figure on the page, so a caption that belongs to
    a lower figure is never read as this plate's.
    """
    p = page_scan(scan)
    if not p or not (0 <= idx < len(p[0])):
        return None, []
    bands, lines = p
    b = bands[idx]
    nxt = min((x["y0"] for x in bands if x["y0"] > b["y1"] + 5), default=None)
    found = []
    for x0, y0, x1, y1, s in lines:
        if y0 < b["y1"] - 25 or y0 > b["y1"] + CAPTION_NEAR:
            continue
        if nxt is not None and y0 > nxt - 25:
            continue
        if x1 < b["x0"] + 0.2 * (b["x1"] - b["x0"]):
            continue
        if is_caption_line(s):
            found.append(s)
    return [n for s in found for n in caption_numbers(s)], found


def band_index(fname):
    """1-based ink-band number the extractor put in its own file name."""
    m = NAME_OLD.match(Path(fname).name)
    return int(m.group(2)) if m else None


def adjacent(claim, nums):
    """The caption numbers that describe the same plate as the claimed one.

    A band can run across two figures the page captions separately, and then the
    strip under it names both: 'FIG. 290.' and 'FIG. 291.' under one wide crop.
    Those are the extras worth putting in the caption. A number that is nowhere
    near the claimed one is not: printed p. 38 carries a stray 'FIG. 81.' under
    the plate that is Fig. 30, and Fig. 81 is on printed p. 98.
    """
    def stem(n):
        return int(re.match(r"\d+", n).group())
    keep, base = [], stem(claim)
    for n in nums:
        if n == claim:
            continue
        if stem(n) == base or abs(stem(n) - base) <= ADJACENT:
            keep.append(n)
    return keep


def candidate_stub(fname):
    """Just enough of a candidate to put one plate on a contact sheet."""
    row = next((r for r in load_manifest() if Path(r["file"]).name == fname), None)
    page, figs, _kind = parse_name(fname)
    return {"file": fname, "printed_page": page, "figs": list(figs),
            "subject": (row or {}).get("subject", "")}


def caption_sheet(cands, outdir, per_sheet=12, dpi=300):
    """Contact sheet: each plate beside the strip of print under it. Returns files."""
    import extract_figures as EF
    from PIL import ImageDraw
    outdir.mkdir(parents=True, exist_ok=True)
    tiles = []
    for c in cands:
        scan = c["printed_page"] + PAGE_OFFSET
        pdf = ROOT / "books" / "pdf-pages-tesla-1894" / f"page-{scan:03d}.pdf"
        if not pdf.exists():
            continue
        page_img, bands = EF.extract(str(pdf), dpi=dpi)
        bi = band_index(c["file"])
        if bi and 1 <= bi <= len(bands):
            b = bands[bi - 1]
            # the printed caption sits under the plate, and the extractor's own
            # row is the band above it, so the strip has to reach to the next
            # band rather than a fixed distance
            nxt = next((x["y0"] for x in bands if x["y0"] > b["y1"]), None)
            stop = min(page_img.height, nxt if nxt else b["y1"] + int(0.6 * dpi),
                       b["y1"] + int(0.6 * dpi))
            below = page_img.crop((b["x0"], max(0, b["y0"] - 8), b["x1"], stop))
        else:
            below = page_img.resize((page_img.width // 3, page_img.height // 3))
        thumb = page_img.crop((0, 0, page_img.width, page_img.height))
        tiles.append((c, below))
    sheets = []
    for n in range(0, len(tiles), per_sheet):
        chunk = tiles[n:n + per_sheet]
        cell_w, label_h = 760, 34
        rows = []
        for c, img in chunk:
            s = min(1.0, (cell_w - 20) / img.width)
            img = img.resize((int(img.width * s), int(img.height * s)))
            h = max(img.height, 120) + label_h
            cell = Image.new("RGB", (cell_w, h), (250, 247, 240))
            d = ImageDraw.Draw(cell)
            lab = (f"printed p.{c['printed_page']}  claimed {fig_label(c['figs'])}"
                   f"  {c['file']}")
            d.text((6, 8), lab, fill=(20, 20, 20))
            cell.paste(img, (6, label_h))
            rows.append(cell)
        cols = 2
        grid = []
        for i in range(0, len(rows), cols):
            row = rows[i:i + cols]
            rh = max(r.height for r in row)
            strip = Image.new("RGB", (cell_w * cols, rh), (255, 255, 255))
            x = 0
            for r in row:
                strip.paste(r, (x, 0))
                x += cell_w
            grid.append(strip)
        total_h = sum(g.height for g in grid)
        sheet = Image.new("RGB", (cell_w * cols, total_h), (255, 255, 255))
        y = 0
        for g in grid:
            sheet.paste(g, (0, y))
            y += g.height
        p = outdir / f"captions-{n // per_sheet + 1}.png"
        sheet.save(p)
        sheets.append(p)
    return sheets


def load_manifest():
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh)]


def load_overrides():
    if OVERRIDES.exists():
        return json.loads(OVERRIDES.read_text())
    return {"exclude": {}, "caption": {}, "alt": {}, "include": []}


def settle_caption(f, item, row, ov):
    """Read the printed caption for this plate and settle its figure numbers.

    Returns (state, why, evidence). The figure numbers the item carries are what
    the caption says, which is not always what the file name claims; the claim
    is kept in figs_claimed and the line of print the change came from is kept
    in the evidence, so a corrected number can be checked against the page.
    """
    claim = [str(x).lower() for x in item["figs"]]
    ev = {"how": None, "lines": [], "claim": claim}
    if item["crop"] == "hand":
        if re.search(r"verified|viewed against|settled visually|printed caption",
                     row["notes"], re.I):
            ev["how"] = ("hand crop: the QC row records the page being opened at "
                         "400-500 ppi and the printed caption read off it")
            return "settled by row", None, ev
        return None, ("hand crop, but its QC row does not record the printed "
                      "caption being read"), ev
    if (v := ov.get("verify", {}).get(f)):
        item["figs"] = [str(x).lower() for x in v["figs"]]
        ev["lines"] = [v["saw"]]
        ev["how"] = v["method"]
        if v.get("note"):
            ev["note"] = v["note"]
        if item["figs"] != claim:
            ev["corrected_from"] = claim
        return "settled by eye", None, ev
    nums, lines = band_caption(item["printed_page"] + PAGE_OFFSET,
                               band_index(f) - 1)
    ev["lines"] = lines
    if not lines:
        return None, ("no caption line in the strip of print under this plate, "
                      "and the plate was not read by eye at this task"), ev
    if not nums:
        return None, ("the caption line under this plate is in the scan, but its "
                      f"number is not legible in the text layer ({lines[0]!r})"), ev
    ev["how"] = ("the caption line under the plate, read from the scan's text "
                 "layer at the band's own position")
    if claim[0] in nums:
        if extra := adjacent(claim[0], nums):
            item["figs"] = [claim[0]] + extra
            ev["widened"] = extra
        return "settled", None, ev
    item["figs"] = nums
    ev["corrected_from"] = claim
    return "settled from the print", None, ev


def build_candidates():
    ch = json.loads(CHAPTERS.read_text())
    chapters, parts = ch["chapters"], ch["parts"]
    ov = load_overrides()
    rows = load_manifest()
    cands, rejected = [], []
    for row in rows:
        f = Path(row["file"]).name
        parsed = parse_name(f)
        if not parsed:
            continue                       # page scans, patent sheets, uncatalogued
        page, figs, kind = parsed
        c = chapter_of(chapters, page)
        p = part_of(parts, page)
        desc, subj_medium = clean_subject(row["subject"], figs)
        med = medium_of(row, subj_medium)
        item = {
            "file": f, "printed_page": page, "figs": list(figs), "crop": kind,
            "quality": row["quality"], "medium": med,
            "chapter": c["no"] if c else None,
            "chapter_title": c["short_title"] if c else None,
            "part": p["part"] if p else None,
            "part_title": p["short_title"] if p else None,
            "subject": desc,
            "qc_note": row["notes"],
            "flag": bool(CORRECTED.search(row["notes"])),
            "verified": kind == "hand" or bool(
                re.search(r"verified|viewed against|settled visually", row["notes"], re.I)),
        }
        why = None
        if row["verdict"] != "keep":
            why = f"verdict={row['verdict']}"
        elif row["quality"] not in ("A", "B"):
            why = f"quality={row['quality']}"
        elif row["caption_ok"] != "yes":
            why = "printed figure number not read correctly (caption_ok=no)"
        elif UNSETTLED.search(row["notes"]):
            why = "the QC row itself leaves the figure number unsettled"
        elif f in ov["exclude"]:
            why = f"ruled out by hand: {ov['exclude'][f]}"
        elif not (ASSETS / f).exists():
            why = "file not on disk"
        else:
            state, cap_why, ev = settle_caption(f, item, row, ov)
            item["caption_state"] = state
            item["caption_evidence"] = ev
            why = cap_why
        if why and f not in ov.get("include", []):
            rejected.append((f, why))
            continue
        # The caption is written after the caption has been read, because the
        # figure numbers it names are what it read, not what the file is called.
        caption = ov["caption"].get(f) or (
            f"{fig_label(item['figs'])} - printed p. {page} - "
            f"Ch. {c['no'] if c else '?'} - {desc}")
        alt = ov["alt"].get(f) or (
            f"1894 {med}, {fig_label(item['figs']).lower()}, printed p. {page}: {desc}")
        item["caption"], item["alt"] = caption, alt
        cands.append(item)
    return cands, rejected, ov


def select():
    cands, rejected, ov = build_candidates()
    # one plate per printed figure; a hand crop beats the extractor crop of it
    best = {}
    for c in cands:
        key = (c["printed_page"], tuple(c["figs"]))
        cur = best.get(key)
        if cur is None or (c["crop"] == "hand" and cur["crop"] != "hand"):
            best[key] = c
    uniq = list(best.values())
    dupes = len(cands) - len(uniq)

    order = {"hand": 0, "extractor": 1}
    uniq.sort(key=lambda c: (c["printed_page"], c["figs"][0]))
    by_chapter = {}
    for c in uniq:
        by_chapter.setdefault(c["chapter"], []).append(c)

    chosen = []
    for chno, items in by_chapter.items():
        items.sort(key=lambda c: (order[c["crop"]], 0 if c["quality"] == "A" else 1,
                                  c["printed_page"]))
        chosen.extend(items[:PER_CHAPTER_CAP])
    chosen.sort(key=lambda c: (c["printed_page"], c["figs"][0]))

    # If the cap leaves us short of the target, take the rest by chapter breadth
    # rather than piling more onto the chapters that already have six.
    if len(chosen) < TARGET:
        rest = [c for c in uniq if c not in chosen]
        count = {c: len([x for x in chosen if x["chapter"] == c]) for c in by_chapter}
        rest.sort(key=lambda c: (count.get(c["chapter"], 0), order[c["crop"]],
                                 0 if c["quality"] == "A" else 1, c["printed_page"]))
        for c in rest:
            if len(chosen) >= TARGET:
                break
            chosen.append(c)
            count[c["chapter"]] = count.get(c["chapter"], 0) + 1
        chosen.sort(key=lambda c: (c["printed_page"], c["figs"][0]))

    rec = {
        "generated": date.today().isoformat(),
        "source_manifest": str(MANIFEST.relative_to(ROOT)),
        "chapter_map": str(CHAPTERS.relative_to(ROOT)),
        "rules": {
            "verdict": "keep", "quality": ["A", "B"], "caption_ok": "yes",
            "figure_number": (
                "read from the caption the page prints under the plate: the "
                "extractor's own ink band re-derived at 300 ppi, the text lines "
                "in the strip under it, the figure numbers those lines set; "
                "plates whose caption line the text layer cannot read are "
                "settled by eye against the page render and recorded in "
                "overrides.json under verify, and plates that were neither read "
                "nor seen are left out"),
            "one_plate_per_printed_figure": True,
            "per_chapter_cap": PER_CHAPTER_CAP,
            "target": TARGET,
        },
        "counts": {
            "manifest_rows": len(load_manifest()),
            "passed_rules": len(cands),
            "duplicate_crops_dropped": dupes,
            "unique_printed_figures": len(uniq),
            "selected": len(chosen),
            "quality_A": sum(1 for c in chosen if c["quality"] == "A"),
            "quality_B": sum(1 for c in chosen if c["quality"] == "B"),
            "hand_cropped": sum(1 for c in chosen if c["crop"] == "hand"),
            "chapters_covered": len({c["chapter"] for c in chosen}),
            "caption_from_text_layer": sum(
                1 for c in chosen
                if str(c.get("caption_state", "")).startswith("settled")
                and "text layer" in (c["caption_evidence"]["how"] or "")),
            "caption_by_eye": sum(1 for c in chosen
                                  if c.get("caption_state") == "settled by eye"),
            "caption_from_qc_row": sum(1 for c in chosen
                                       if c.get("caption_state") == "settled by row"),
            "figure_number_corrected": sum(
                1 for c in chosen
                if c["caption_evidence"].get("corrected_from")),
            "caption_names_more_than_one_figure": sum(
                1 for c in chosen if len(c["figs"]) > 1),
        },
        "plates": chosen,
        "rejected": rejected,
    }
    return rec


# ------------------------------------------------------------------ assets

def thumb_path(item):
    return THUMBS / item["file"]


def make_thumbs(plates):
    THUMBS.mkdir(parents=True, exist_ok=True)
    made = 0
    for it in plates:
        src = ASSETS / it["file"]
        dst = thumb_path(it)
        im = Image.open(src).convert("RGB")
        s = min(1.0, THUMB_LONG_EDGE / max(im.size))
        if s < 1.0:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=82, method=6)
        it["thumb_width"], it["thumb_height"] = im.width, im.height
        it["thumb_bytes"] = dst.stat().st_size
        made += 1
    return made


def make_zip(plates):
    """The §16.3 download: every plate at up to 1200 px, plus a README."""
    names = []
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for it in plates:
            im = Image.open(ASSETS / it["file"]).convert("RGB")
            s = min(1.0, ZIP_LONG_EDGE / max(im.size))
            if s < 1.0:
                im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            q = im.quantize(colors=256, method=Image.MEDIANCUT)
            arc = f"{Path(it['file']).stem}.png"
            z.writestr(arc, _png_bytes(q))
            it["zip_name"], it["zip_px"] = arc, f"{im.width}x{im.height}"
            names.append(f"{arc}\t{fig_label(it['figs'])}\tprinted p. {it['printed_page']}"
                         f"\tCh. {it['chapter']}")
        z.writestr("README.txt", zip_readme(plates, names))
    return ZIP.stat().st_size


def _png_bytes(im):
    import io
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def zip_readme(plates, names):
    return (
        "Nikola Tesla plates - 1894 first edition\n"
        "=========================================\n\n"
        "The Inventions, Researches and Writings of Nikola Tesla, edited by\n"
        "Thomas Commerford Martin, New York: D. Van Nostrand, 1894 (entered 1893).\n"
        "Scanned copy: archive.org item inventionsresear00martiala\n"
        f"{len(plates)} plates, each at up to {ZIP_LONG_EDGE} px on its long edge, PNG.\n\n"
        "Page rule: the scan runs 18 leaves ahead of the printed page number, so\n"
        "printed page = scan file page - 18. Every file name in the source manifest\n"
        "and every caption on the page states the PRINTED page, the number the book\n"
        "prints in its own corner.\n\n"
        "Licence: public domain (1894 imprint). Reuse freely; a credit line is\n"
        "appreciated: 'Plate, Martin (ed.), The Inventions, Researches and Writings\n"
        "of Nikola Tesla (1894), p. N.'\n\n"
        "Page of origin: https://teslamagneticgenerator.com/tesla-1894-plates\n\n"
        "Contents (file, book figure number, printed page, chapter):\n"
        + "\n".join(names) + "\n")


# ------------------------------------------------------------------- page

def gallery_html(plates):
    """The grid. One section per part, one h3 per chapter, cards in a responsive grid.

    The grid sits after </article>, not inside it. §12's figure-weight gate is
    written as the article's own figures (books/tools/qa_page.py measures the
    bytes inside <article> for exactly that reason, and notes the shared shell
    separately); a 70-plate gallery is not an article's figure set, and putting
    it inside the article would read as if the article had 70 figures.

    The cards go inside a Bootstrap row-cols grid, one row per chapter, because a
    .col outside a .row is not a column at all: it is a block, and seventy-two
    blocks is a page of full-width pictures stacked one under another.
    """
    out = ['<section class="plate-gallery mb-5">']
    cur_part = cur_ch = None
    row = False
    for it in plates:
        if it["part"] != cur_part:
            if row:
                out.append("</div>")
                row = False
            cur_part, cur_ch = it["part"], None
            out.append(f'<h2 class="fw-bolder mb-1 pt-5">'
                       f'{TC.titlecase(f"Part {it["part"]}: {it["part_title"]}")}</h2>')
            out.append(f'<p class="text-muted small mb-3">Plates the volume prints in '
                       f'this part, in printed page order.</p>')
        if it["chapter"] != cur_ch:
            if row:
                out.append("</div>")
                row = False
            cur_ch = it["chapter"]
            out.append(f'<h3 class="fw-bolder mb-1 pt-4">'
                       f'{TC.titlecase(f"Chapter {it["chapter"]}: {it["chapter_title"]}")}</h3>')
            out.append(f'<p class="text-muted small mb-3">Chapter {it["chapter"]}, '
                       f'beginning at printed p. {_chapter_page(it["chapter"])}.</p>')
        if not row:
            out.append('<div class="row g-4 row-cols-1 row-cols-sm-2 row-cols-xl-3">')
            row = True
        out.append(card_html(it))
    if row:
        out.append("</div>")
    out.append("</section>")
    return "\n".join(out)


_CHAPTER_PAGES = {}


def _chapter_page(chno):
    return _CHAPTER_PAGES[chno]


def card_html(it):
    t = thumb_path(it)
    src = f"/assets/tesla1894/thumbs/{t.name}"
    full = f"/assets/tesla1894/{it['file']}"
    cap = (f'{fig_label(it["figs"])} &middot; printed p. {it["printed_page"]} &middot; '
           f'Ch. {it["chapter"]} &middot; {it["medium"]}')
    return (
        '<div class="col d-flex"><figure class="h-100 w-100 mb-0">'
        f'<a href="{full}" class="d-block">'
        f'<img src="{src}" alt="{it["alt"]}" width="{it["thumb_width"]}" '
        f'height="{it["thumb_height"]}" loading="lazy" class="img-fluid rounded"/></a>'
        '<figcaption class="pt-2">'
        f'<p class="small mb-1">{cap}</p>'
        f'<p class="small text-muted mb-0">{it["subject"]}</p>'
        '</figcaption></figure></div>')


def jsonld_images(plates):
    items = []
    for it in plates:
        items.append({
            "@type": "ImageObject",
            "name": f'{fig_label(it["figs"])}, printed p. {it["printed_page"]}',
            "caption": it["caption"],
            "contentUrl": f"{MA.SITE}/assets/tesla1894/{it['file']}",
            "thumbnailUrl": f"{MA.SITE}/assets/tesla1894/thumbs/{it['file']}",
            "license": "http://creativecommons.org/publicdomain/mark/1.0/",
            "acquireLicensePage": MA.page_url("tesla-1894-plates.html"),
            "creditText": ("Martin (ed.), The Inventions, Researches and Writings of "
                           f"Nikola Tesla (1894), p. {it['printed_page']}"),
            "provider": {"@type": "Organization", "name": "Internet Archive",
                         "sameAs": "https://archive.org/details/inventionsresear00martiala"},
        })
    block = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "The 1894 plates: engravings from the first edition, page by page",
        "numberOfItems": len(plates),
        "itemListElement": [{"@type": "ListItem", "position": n + 1, "image": im}
                            for n, im in enumerate(items)],
    }
    return ('    <script type="application/ld+json">\n'
            + json.dumps(block, indent=2).replace("\n", "\n    ") + "\n    </script>")


def build_page(rec):
    plates = rec["plates"]
    fm, body = MA.split_front_matter(DRAFT.read_text())
    slug = OUT.name
    if fm.get("slug") != slug:
        sys.exit(f"draft slug {fm.get('slug')!r} != {slug!r}")
    n = len(plates)
    # A count in the title or description is a claim the page makes about itself,
    # so it is checked against the selection rather than trusted.
    for key in ("title", "description"):
        for claimed in re.findall(r"\b(\d{2,3})\s+(?:plates|engravings)", fm[key]):
            if int(claimed) != n:
                sys.exit(f"front matter {key} claims {claimed} plates, the selection has {n}")
    shell = MA.load_shell(DONOR)
    body_html = MA.md_to_html(body, fm, DRAFT.parent)
    if "{{GALLERY}}" not in body_html:
        sys.exit("draft must carry a {{GALLERY}} marker where the grid belongs")
    pre, post = body_html.split("{{GALLERY}}", 1)
    cta = MA.cta_block(fm, str(fm["tid"]))
    post = post.replace("{{CTA}}", cta).replace("{{SOURCES}}", MA.sources_block(fm))
    for marker in ("{{CTA}}", "{{SOURCES}}", "{{FAQ}}"):
        if marker in pre or marker in post:
            sys.exit(f"unresolved marker {marker}")

    header = [f'<h1 class="fw-bolder mb-1">{fm["title"]}</h1>',
              ('<p class="text-muted small mb-2">The 1894 File &middot; a linkable asset. '
               'Every plate below is cited to the page the book prints it on.</p>'),
              (f'<p class="text-muted small mb-3">Published: '
               f'{MA.fmt_date(fm.get("date_published"))} &nbsp;|&nbsp; Updated: '
               f'{MA.fmt_date(fm.get("date_modified", fm.get("date_published")))}</p>')]
    article = ('<article>\n                        <section class="mb-5">\n'
               + "\n".join(header) + "\n" + pre.rstrip() +
               "\n                        </section>\n                    </article>")

    html = ('<!DOCTYPE html>\n<html lang="en">\n    <head>\n'
            + MA.build_head(fm, slug) + MA.build_jsonld(fm, slug) + "\n"
            + jsonld_images(plates) + "\n</head>\n    <body>\n\n"
            "        <!-- Responsive navbar -->\n        " + shell["nav"] + "\n"
            "        " + shell["container_open"]
            + '            <div class="col-lg-8">\n                    <!-- Post content-->\n'
            + "                    " + article + "\n\n"
            + "                    " + gallery_html(plates) + "\n\n"
            + '                    <section class="mb-5">\n' + post.strip() +
            "\n                    </section>\n\n"
            + "                    " + shell["scarcity"] + "\n"
            + "                </div>\n            " + shell["sidebar"] + "\n"
            + shell["footer"] + "\n    </body>\n</html>\n")
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--select", action="store_true")
    ap.add_argument("--thumbs", action="store_true")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--show", type=int, default=0,
                    help="print the first N selected plates and stop")
    ap.add_argument("--sheet", action="store_true",
                    help="write the caption contact sheet for plates the text layer "
                         "does not settle, and stop")
    ap.add_argument("--report", action="store_true",
                    help="print the caption-state report and stop")
    ap.add_argument("--only",
                    help="with --sheet: just these file names, comma separated")
    ap.add_argument("--out", default=str(ROOT / "books" / "tmp" / "f08t1" / "captions"),
                    help="with --sheet: where to write the sheets")
    args = ap.parse_args()

    ch = json.loads(CHAPTERS.read_text())
    _CHAPTER_PAGES.update({c["no"]: c["from_page"] for c in ch["chapters"]})

    if args.report or args.sheet:
        cands, rejected, _ = build_candidates()
        cands.sort(key=lambda c: (c["printed_page"], c["figs"][0]))
        settled = lambda c: str(c.get("caption_state", "")).startswith("settled")
        if args.report:
            for st in ("settled", "settled from the print", "settled by eye",
                       "settled by row"):
                group = [c for c in cands if c.get("caption_state") == st]
                print(f"{st}: {len(group)}")
                if st != "settled":
                    for c in group:
                        claim = "/".join(c["caption_evidence"].get("corrected_from", []))
                        print(f"  p{c['printed_page']:>3} {fig_label(c['figs']):<18}"
                              f"was {claim:<8} {c['file']}")
            print("rejected for the caption:")
            for f, why in rejected:
                if "caption" in why:
                    print(f"  {f}: {why}")
            return 0
        if args.only:
            want = [x.strip() for x in args.only.split(",") if x.strip()]
            need = [candidate_stub(f) for f in want]
        else:
            need = [c for c in cands if not settled(c)]
            need += [candidate_stub(f) for f, why in rejected if "caption" in why]
            need.sort(key=lambda c: (c["printed_page"], c["file"]))
        sheets = caption_sheet(need, Path(args.out))
        print(f"caption sheet: {len(need)} plates -> "
              + ", ".join(str(s.relative_to(ROOT)) for s in sheets))
        return 0
    if args.show:
        rec = select()
        for it in rec["plates"][:args.show]:
            print(f"p{it['printed_page']:>3} {fig_label(it['figs']):<16} {it['quality']} "
                  f"Ch{it['chapter']:<6} {it['crop']:<9} {it['file']}")
        print(json.dumps(rec["counts"], indent=1))
        return 0
    if not (args.select or args.thumbs or args.zip or args.build or args.all):
        ap.error("choose --select / --thumbs / --zip / --build / --all")

    rec = select()

    WORK.mkdir(parents=True, exist_ok=True)
    if args.select or args.all:
        SELECTION.write_text(json.dumps(rec, indent=2) + "\n")
        print(f"selection: {rec['counts']}")
        print(f"  -> {SELECTION.relative_to(ROOT)}")
        print(f"  rejected by the rules: {len(rec['rejected'])} rows "
              f"(listed in the record)")
    if args.thumbs or args.all:
        n = make_thumbs(rec["plates"])
        kb = sum(thumb_path(i).stat().st_size for i in rec["plates"]) // 1024
        print(f"thumbnails: {n} files in {THUMBS.relative_to(WEB)} "
              f"({THUMB_LONG_EDGE} px long edge, {kb} KB total)")
    if args.zip or args.all:
        size = make_zip(rec["plates"])
        print(f"zip: {ZIP.relative_to(WEB)} {size / 1e6:.1f} MB, "
              f"{len(rec['plates'])} plates at up to {ZIP_LONG_EDGE} px + README.txt")
    if args.build or args.all:
        if not (rec["plates"][0].get("thumb_width")):
            make_thumbs(rec["plates"])       # need real pixel dims for the img tags
        html = build_page(rec)
        OUT.write_text(html)
        print(f"wrote {OUT.relative_to(ROOT)} ({len(html.encode())} bytes, "
              f"{len(rec['plates'])} plates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
