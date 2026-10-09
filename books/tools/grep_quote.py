#!/usr/bin/env python3
"""Re-grep a quote from the 1894 OCR and pin it to a PRINTED page.

SERIES-PLAN-1894.md §8 step 2 / §0 non-negotiable 2: every quote is re-grepped
from books/extracted/tesla-1894-plain.txt and pinned to a printed page before it
ships.

    printed page = scan file page - 18        (§0 non-negotiable 1)

OCR artefacts (long-s, ligatures, S-for-8, soft hyphens, line-end hyphen
breaks) are normalised for MATCHING ONLY. The text we print back is the raw OCR
line, so you can see exactly what the scan says before you decide how to
normalise it for publication (§3 quote policy).

Usage
    grep_quote.py "attach their machinery"
    grep_quote.py "torn apart while vibrating" --context 400
    grep_quote.py "30,000 alternations" --page 375-385      # printed pages
    grep_quote.py "free energy" --count                    # hit count only
    grep_quote.py "the tube in my hand" --json             # machine-readable
    grep_quote.py --verify appendix-a                      # check Appendix A list
"""

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
BOOKS = TOOLS.parent
DEFAULT_TXT = BOOKS / "extracted" / "tesla-1894-plain.txt"
PAGE_MARKER = re.compile(r"<+ *page-(\d+) *>+")

# Scan-file page -> printed page offset (SERIES-PLAN §0).
PAGE_OFFSET = 18


def normalise(text: str) -> str:
    """Fold OCR noise so a typed quote matches the scan. Matching only."""
    t = unicodedata.normalize("NFKD", text)          # ﬁ -> fi, ſ stays
    subs = {
        "\u017f": "s",   # ſ long s
        "\u00df": "s",   # ß
        "\u0160": "8",   # Š  (S-for-8 artefact)
        "\u0161": "8",   # š
        "\u00ad": "",    # soft hyphen
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2014": "-", "\u2013": "-", "\u2012": "-",
        "\u2026": "...",
    }
    for k, v in subs.items():
        t = t.replace(k, v)
    t = t.lower()
    # Un-hyphenate line breaks: "alter- nations" -> "alternations", and also
    # allow the query to be written either way.
    t = re.sub(r"-\s+", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def strip_furniture(text: str) -> str:
    """Drop running heads / bare folios so prose is contiguous for MATCHING.

    The OCR interleaves running heads into sentences, e.g. the p.196 quote
    "we are whirling through … endless space" has "moil FREQUENCY AND HIGH
    POTENTIAL CURRENTS. 197" sitting in the middle of it. Display still uses the
    raw page text; only the search index is cleaned.
    """
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            out.append(line)
            continue
        if re.fullmatch(r"[ivxlcdmIVXLCDM]{1,5}|\d{1,4}", s):
            continue                                  # bare folio
        letters = [c for c in s if c.isalpha()]
        caps = sum(c.isupper() for c in letters)
        if not letters:
            continue
        ratio = caps / len(letters)
        nwords = len(s.split())
        if (len(s) < 140 and nwords <= 9 and ratio > 0.7) or \
           (len(s) < 60 and nwords <= 6 and ratio > 0.6):
            continue                                  # running head
        out.append(line)
    return "\n".join(out)


def load_pages(path: Path, clean: bool = True):
    """-> list of (file_page, printed_page, index_text, raw_text, start_offset)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    marks = list(PAGE_MARKER.finditer(raw))
    if not marks:
        sys.exit(f"no page markers found in {path}")
    for i, m in enumerate(marks):
        fp = int(m.group(1))
        end = marks[i + 1].start() if i + 1 < len(marks) else len(raw)
        body = raw[m.end():end]
        pages.append((fp, fp - PAGE_OFFSET,
                      strip_furniture(body) if clean else body, body, m.end()))
    return pages


def build_index(pages):
    """One normalised stream over the whole book + a norm-offset -> page map.

    Searching the whole stream (not page by page) is deliberate: Appendix A
    quotes span page breaks, e.g. "we are whirling through endless space"
    runs from file 214 / printed 196 onto file 215 / printed 197.
    """
    parts, spans = [], []
    for fp, pp, itext, _raw, base in pages:
        n = normalise(itext)
        start = sum(len(p) + 1 for p in parts)
        parts.append(n)
        spans.append((start, start + len(n), fp, pp))
    ntext = " ".join(parts)
    words = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", ntext)]
    return ntext, spans, words


def pages_for(spans, a, b):
    return [(fp, pp) for (s, e, fp, pp) in spans if s < b and e > a]


def find_hits(index, needle_norm, page_lo=None, page_hi=None):
    """Exact + fuzzy hits over the whole book. Cross-page aware."""
    ntext, spans, _words = index
    hits, seen = [], set()

    def emit(a, b, ratio):
        for fp, pp in pages_for(spans, a, b):
            if page_lo is not None and not (page_lo <= pp <= page_hi):
                continue
            if (fp, a) in seen:
                continue
            seen.add((fp, a))
            hits.append({"file_page": fp, "printed_page": pp,
                         "ratio": round(ratio, 3), "offset": a,
                         "spans_pages": [pp for _, pp in pages_for(spans, a, b)]})

    for m in re.finditer(re.escape(needle_norm), ntext):
        emit(m.start(), m.end(), 1.0)
    if hits:
        return hits

    # fuzzy: only score windows that start on a word close to the needle's
    # first word — a full 177k-word SequenceMatcher sweep is far too slow.
    nwords = len(needle_norm.split())
    words = index[2]
    if len(words) < nwords:
        return hits
    vocab = sorted({w for _, _, w in words})
    near = set(difflib.get_close_matches(needle_norm.split()[0], vocab,
                                         n=12, cutoff=0.72))
    starts = [i for i, (_, _, w) in enumerate(words) if w in near]
    for i in starts:
        if i + nwords > len(words):
            continue
        win = " ".join(w for _, _, w in words[i:i + nwords])
        r = difflib.SequenceMatcher(None, needle_norm, win).ratio()
        if r >= 0.80:
            emit(words[i][0], words[i + nwords - 1][1], r)
    return hits


def context(raw: str, offset: int, span: int) -> str:
    a = max(0, offset - span)
    b = min(len(raw), offset + span)
    left = "…" if a > 0 else ""
    right = "…" if b < len(raw) else ""
    return left + " ".join(raw[a:b].split()) + right


def raw_context(hit, ntext, raw_by_page, span):
    """Locate the match inside the RAW OCR page text and show it un-normalised,
    so you can see what the scan actually says before choosing a house style."""
    raw = raw_by_page[hit["file_page"]]
    start = hit["offset"]
    first = ntext[start:start + 60].split()[0] if start >= 0 else ""
    pos = raw.find(first) if first else -1
    if pos < 0:
        # long-s / ligature fold: try a shortened anchor
        for n in (24, 12, 6):
            frag = ntext[start:start + n].split()[0] if start >= 0 else ""
            pos = raw.find(frag) if frag else -1
            if pos >= 0:
                break
    if pos < 0:
        pos = 0
    return context(raw, pos, span)


APPENDIX_A = {
    8: ["a little over sixty per cent", "as high as 94 and 95 per cent",
        "An invention is none the less beautiful because it may lack utility"],
    27: ["written the night previous to the meeting, in pencil"],
    125: ["supported without any inconvenience, except perhaps a small burn"],
    138: ["best succeed on a ship at sea"],
    151: ["20,000 alternations per second"],
    167: ["give light and heat without any material being consumed"],
    184: ["is equivalent to a return wire"],
    186: ["wiping out the light of the tube"],
    196: ["whirling through endless space"],
    200: ["the tube in my hand is brilliantly lighted"],
    232: ["by the use of one wire only"],
    236: ["attach their machinery to the very wheelwork of nature",
          "the most inefficient machine ever invented",
          "capable of fusing a thick copper wire"],
    255: ["buttons of diamond dust"],
    258: ["is it the less a flame because it does not scorch my hand"],
    267: ["advisable to use only one wire"],
    288: ["still it retains the faculty of being excited"],
    293: ["I shall never forget"],
    374: ["the advantages of silence and persistency"],
    376: ["Up to about 15,000 alternations per second"],
    381: ["480 polar projections", "30,000 alternations per second"],
    391: ["twenty feet long and two millimetres in diameter"],
    394: ["the misuse and abuse of electricity"],
    395: ["a person entirely nude at the North Pole"],
    424: ["oscillating as rapidly as 400 to 500 times a minute"],
    486: ["actually torn apart while vibrating against a minute air cushion"],
    487: ["weight of approximately 20 pounds at the rate of about 80 per second"],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("quote", nargs="?", help="quote or phrase to find")
    ap.add_argument("--txt", default=str(DEFAULT_TXT))
    ap.add_argument("--context", type=int, default=240, help="chars each side")
    ap.add_argument("--page", help="restrict to printed pages, e.g. 486 or 480-495")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--count", action="store_true", help="hit counts only")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verify", nargs="?", const="appendix-a", default=None,
                    choices=["appendix-a"],
                    help="re-check every Appendix A quote and its page")
    ap.add_argument("--keep-furniture", action="store_true",
                    help="do not strip running heads/bare folios from the index")
    args = ap.parse_args()

    pages = load_pages(Path(args.txt), clean=not args.keep_furniture)
    index = build_index(pages)
    raw_by_page = {fp: body for fp, pp, itext, body, _ in pages}

    if args.verify:
        out, bad = [], 0
        for pp, quotes in sorted(APPENDIX_A.items()):
            for q in quotes:
                hits = find_hits(index, normalise(q), pp, pp)
                if not hits:  # widen: the register page may be off by one
                    hits = find_hits(index, normalise(q), pp - 1, pp + 1)
                out.append({"printed_page": pp, "quote": q,
                            "found": bool(hits),
                            "found_on": sorted({h["printed_page"] for h in hits})})
                if not bool(hits):
                    bad += 1
        print(json.dumps(out, indent=2) if args.json else
              "\n".join(f"{'OK ' if r['found'] else 'MISS'} p{r['printed_page']:>3} "
                        f"{r['found_on']} :: {r['quote'][:70]}" for r in out))
        print(f"\n{len(out) - bad}/{len(out)} verified on the stated page "
              f"(+/-1 tolerated)")
        return 0 if bad == 0 else 1

    if not args.quote:
        ap.error("a quote is required (or --verify appendix-a)")

    page_lo = page_hi = None
    if args.page:
        if "-" in args.page:
            a, b = args.page.split("-", 1)
            page_lo, page_hi = int(a), int(b)
        else:
            page_lo = page_hi = int(args.page)

    needle = normalise(args.quote)
    hits = find_hits(index, needle, page_lo, page_hi)
    hits.sort(key=lambda h: h["file_page"])

    if args.count:
        print(json.dumps({"query": args.quote, "hits": len(hits),
                          "printed_pages": sorted({h["printed_page"] for h in hits})},
                         indent=2) if args.json else
              f"{len(hits)} hits; printed pages: "
              f"{sorted({h['printed_page'] for h in hits})}")
        return 0

    if args.json:
        print(json.dumps([{**h, "context": raw_context(h, index[0], raw_by_page,
                                                      args.context)}
                          for h in hits[:args.limit]], indent=2))
        return 0

    if not hits:
        print(f"NOT FOUND: {args.quote!r}")
        print("Try a shorter fragment, or check OCR spelling with --count.")
        return 1

    for h in hits[:args.limit]:
        flag = "" if h["ratio"] > 0.999 else f"  [fuzzy {h['ratio']}]"
        span = "" if len(h["spans_pages"]) < 2 else f" -> continues p. {'/'.join(map(str, h['spans_pages']))}"
        print(f"--- printed p. {h['printed_page']}  (scan file {h['file_page']}){flag}{span}")
        print(raw_context(h, index[0], raw_by_page, args.context))
        print()
    if len(hits) > args.limit:
        print(f"({len(hits)} hits total; showing {args.limit})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
