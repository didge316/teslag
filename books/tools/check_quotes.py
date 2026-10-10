#!/usr/bin/env python3
"""Check that every quote in a draft is verbatim in the 1894 OCR, and page-cited.

SERIES-PLAN-1894.md §8 step 2 and §12 ("at least 3 page-cited quotes"). The
risk this tool exists for is an OCR misquote shipping publicly (§14).

    python3 books/tools/check_quotes.py new_content/1894-series/07-*/article.md
    python3 books/tools/check_quotes.py --all-series

For every quoted passage in the prose (headings, figure alt text and captions
are our own words and are skipped):

  1. split it on ellipses, since an elided quote is a sequence of quotations;
  2. require each fragment (>= 12 chars) to match the OCR text word for word,
     using the same OCR normalisation grep_quote.py uses (long s, S-for-8,
     line-end hyphens, running heads). A match that only holds once spaces are
     ignored is allowed and flagged, because the OCR glues words together in
     places ("touse", "formingthe") and the printed scan has the space;
  3. report the PRINTED page(s) the fragment occurs on (scan file - 18);
  4. require a "(1894, p. N)" citation within 400 characters after the quote,
     and require N to be one of those pages.

A fuzzy near-match is a FAIL with the closest real text, because a near-match
is exactly the paraphrase-inside-quotation-marks the rule forbids.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import grep_quote as GQ

TOOLS = Path(__file__).resolve().parent
BOOKS = TOOLS.parent
ROOT = BOOKS.parent
DEFAULT_TXT = BOOKS / "extracted" / "tesla-1894-plain.txt"
SERIES = ROOT / "new_content" / "1894-series"
MIN_FRAGMENT = 12
CITE_WINDOW = 400

BACKTICK_RE = re.compile(r"`([^`']{12,})'")


def quote_spans(body: str, classify):
    """Yield (kind, end_offset, text) for each quoted passage, resynchronising.

    Quotes in this dialect wrap, so pairing is done over the whole body, but the
    quote marks inside headings and figure lines are removed first: a quoted
    heading ("A tale of woe") is our own words, and leaving its marks in would
    mis-pair every quote after it. classify() says whether a candidate is a book
    quote ('quote'), a near-miss ('suspect'), or our own wording ('skip'); on
    'skip' the scanner moves one quote mark on, because the scan uses " for
    inches ("f- inch" on p. 487) and one stray mark would otherwise shift every
    later quote by one.
    """
    blanked = []
    for line in body.split("\n"):
        s = line.strip()
        blanked.append(re.sub(r'"|`', " ", line)
                       if (s.startswith("#") or s.startswith("![")
                           or s.startswith("---")) else line)
    text = "\n".join(blanked)
    qs = [m.start() for m in re.finditer(r'"', text)]
    i = 0
    while i < len(qs) - 1:
        for jump in (1, 2):                       # an inch mark inside the quote
            if i + jump >= len(qs):
                continue
            cand = text[qs[i] + 1:qs[i + jump]]
            if len(cand) < MIN_FRAGMENT:
                continue
            kind = classify(cand)
            if kind != "skip":
                yield kind, qs[i + jump], cand.strip()
                i += jump + 1
                break
        else:
            i += 1
    for m in BACKTICK_RE.finditer(text):
        yield classify(m.group(1)), m.end(), m.group(1).strip()


def fragments(text: str):
    parts = re.split(r"\s*(?:\.\.\.|…)\s*", text)
    return [p.strip(" ,;:.") for p in parts if len(p.strip(" ,;:.")) >= MIN_FRAGMENT]


def build_nospace(pages):
    """A whitespace-free copy of the normalised book, with its own page spans.

    The OCR glues words together in places ("touse", "formingthe"), so a quote
    that is word-perfect can still miss on spaces. Offsets in that stream mean
    nothing in the spaced one, so the spans are rebuilt here.
    """
    parts, spans = [], []
    for fp, pp, itext, _raw, _base in pages:
        n = re.sub(r"\s+", "", GQ.normalise(itext))
        start = sum(len(p) for p in parts)
        parts.append(n)
        spans.append((start, start + len(n), fp, pp))
    return "".join(parts), spans


def locate(index, frag: str):
    """-> (hits, how) with how in {'exact','nospace','fuzzy'} or ([], None)."""
    ntext, spans, words = index[:3]
    n = GQ.normalise(frag)
    hits = [h for h in GQ.find_hits(index[:3], n) if h["ratio"] == 1.0]
    if hits:
        return hits, "exact"
    nospace, nspans = index[3], index[4]
    needle = re.sub(r"\s+", "", n)
    out, pos = [], 0
    while True:
        i = nospace.find(needle, pos)
        if i < 0:
            break
        out.extend(GQ.pages_for(nspans, i, i + len(needle)))
        pos = i + 1
    if out:
        return [{"file_page": fp, "printed_page": pp, "ratio": 1.0}
                for fp, pp in dict.fromkeys(out)], "nospace"
    best = max(GQ.find_hits(index[:3], n), key=lambda h: h["ratio"], default=None)
    return ([best], "fuzzy") if best else ([], None)


def check(md_path: Path, index):
    text = md_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.index("\n---", 3)
        text = text[end + 4:]

    def classify(s):
        """quote = every fragment is in the OCR; suspect = something close;
        skip = our own wording in quotes."""
        frs = fragments(s)
        if not frs:
            return "skip"
        kinds = [locate(index, f)[1] for f in frs]
        if all(k in ("exact", "nospace") for k in kinds):
            return "quote"
        if any(k == "fuzzy" for k in kinds):
            return "suspect"
        return "skip"

    fails, rows = [], []
    for kind, end, q in quote_spans(text, classify):
        if kind == "suspect":
            for frag in fragments(q):
                hits, how = locate(index, frag)
                if how == "fuzzy":
                    fails.append(f"NOT VERBATIM: {frag[:70]!r} (closest "
                                 f"{hits[0]['ratio']} on printed p. "
                                 f"{hits[0]['printed_page']})")
                    rows.append(("FAIL", frag, "-", "near-miss only"))
            continue
        for frag in fragments(q):
            hits, how = locate(index, frag)
            after = text[end:end + CITE_WINDOW]
            cited = []
            for grp in re.findall(r"\(1894, p{1,2}s?\. ([\d,\s]+?)\)", after):
                cited += [int(c) for c in re.findall(r"\d+", grp)]
            pps = sorted({h["printed_page"] for h in hits})
            if how == "exact":
                note = "verbatim"
            elif how == "nospace":
                note = "OCR spacing normalised"
            else:
                hint = (f"closest {hits[0]['ratio']} on printed p. "
                        f"{hits[0]['printed_page']}" if how == "fuzzy"
                        else "no match at all")
                fails.append(f"NOT VERBATIM: {frag[:70]!r} ({hint})")
                rows.append(("FAIL", frag, "-", hint))
                continue
            if not cited:
                fails.append(f"NOT CITED: {frag[:70]!r} is on printed p. {pps}, "
                             f"no (1894, p. N) within {CITE_WINDOW} chars")
                rows.append(("FAIL", frag, ",".join(map(str, pps)), "no citation"))
                continue
            if not set(cited) & set(pps):
                fails.append(f"WRONG PAGE: {frag[:70]!r} cited p. {cited[0]}, "
                             f"OCR says printed p. {pps}")
                rows.append(("FAIL", frag, ",".join(map(str, pps)),
                             "cited " + str(cited[0])))
                continue
            rows.append(("ok", frag, ",".join(map(str, pps)),
                         f"cited p. {cited[0]}, {note}"))
    return fails, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", nargs="?", help="article.md to check")
    ap.add_argument("--all-series", action="store_true",
                    help="check every draft named in index.json")
    ap.add_argument("--txt", default=str(DEFAULT_TXT))
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    args = ap.parse_args()

    targets = []
    if args.all_series:
        for e in json.loads((SERIES / "index.json").read_text()):
            d = ROOT / e["draft"]
            if d.exists():
                targets.append(d)
    elif args.md:
        targets.append(Path(args.md))
    else:
        ap.error("give an article.md or --all-series")

    pages = GQ.load_pages(Path(args.txt))
    index = tuple(GQ.build_index(pages)) + tuple(build_nospace(pages))

    bad = 0
    for t in targets:
        fails, rows = check(t, index)
        n_ok = sum(1 for r in rows if r[0] == "ok")
        print(f"\n=== {t.resolve().relative_to(ROOT)}: {len(rows)} quote fragments, "
              f"{n_ok} verbatim and page-cited ===")
        if not args.quiet:
            for status, frag, pps, note in rows:
                print(f"  [{status}] p.{pps} ({note}) {frag[:72]}")
        for f in fails:
            print("  FAIL:", f)
        bad += len(fails)
    print(f"\n{len(targets)} file(s), {bad} quote problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
