#!/usr/bin/env python3
"""The word-search table for article 10, re-run on demand.

SERIES-PLAN-1894.md 9 brief 10 item 2 says the table is "re-run at publish time,
show the counts", and 12 prints the counts rather than describing them. So the
numbers in article.md are not typed by hand: they come from this file, which is
run again at feature-007/t3 and again before any push.

Three indices, the same three that new_content/1894-series/10-tesla-free-energy-what-he-said/quotes.md
records under "THE THREE WAYS TO COUNT", and for the same reason. They disagree,
and the disagreement is the chapter XXXVI heading:

  RAW   case-insensitive substring count over the page bodies of
        books/extracted/tesla-1894-plain.txt exactly as they sit on disk, nothing
        normalised. This is what a reader reproducing a count with grep -c gets,
        and it is the index Appendix D's numbers come from.
  GATE  the index books/tools/check_quotes.py builds and books/tools/grep_quote.py
        builds by default: running heads and bare folios dropped, then the text
        lower-cased, a hyphen at a line break folded, whitespace collapsed.
  KEEP  the same normalised index with the furniture kept (load_pages(clean=False)),
        which is the only one of the three that contains the display heading of
        chapter XXXVI and so the only one that returns 5 for "magnetic generator".

Printed page = scan file page - 18 (SERIES-PLAN 0). Every page list this script
prints is a printed page.

Usage: python3 word_counts.py            # the two tables article 10 prints
       python3 word_counts.py term ...   # one or more terms, same three indices
Exit 0 always; the point is the measurement, not a verdict.
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "books" / "tools"
sys.path.insert(0, str(TOOLS))
import grep_quote as GQ  # noqa: E402

TXT = TOOLS.parent / "extracted" / "tesla-1894-plain.txt"

# The Appendix D rows: the table 9 brief 10 item 2 asks the page to show.
TABLE = [
    ("free energy", "free energy / free-energy"),
    ("free-energy", "free energy / free-energy"),
    ("perpetual", "perpetual"),
    ("over unity", "over unity / over-unity"),
    ("over-unity", "over unity / over-unity"),
    ("magnetic generator", "magnetic generator"),
]

# The phrases the site's own vocabulary invites, and the ones a reader might type.
# Brief 10 item 6 says "Tesla magnetic generator" is a product name, not a Tesla
# term; that sentence is a count, so it needs these rows.
EXTRA = [
    ("magnetic gener", "the stem a reader types"),
    ("magnetic generators", "the plural"),
    ("pyromagnetic", "unhyphenated"),
    ("pyro-magnetic", "hyphenated"),
    ("thermo-magnetic", "the other half of chapter XXXVI's title"),
    ("magnetic motor", "the phrase the product vocabulary invites"),
    ("magnet motor", "the site's other product phrase"),
    ("magnetic engine", "a plausible-sounding nineteenth-century phrase"),
    ("magnetic dynamo", "ditto"),
    ("free electricity", "the site's phrase, and a live page's title"),
    ("free energ", "any inflected free-energy form"),
    ("perpetu", "any perpetual form"),
    ("unity", "what a reader searching 'over unity' by halves finds"),
    ("wheelwork", "the phrase everyone posts"),
    ("wheelwork of nature", "the phrase as quoted"),
    ("radiometer", "Crookes' instrument, named on printed p. 236"),
    ("inexhaustible", "the one such word in the volume"),
    ("bifilar", "a word a live page uses for the device it sells"),
    ("512,340", "a patent number a live page cites"),
    ("coil for electromagnets", "a patent title a live page cites"),
]

# Whether chapter XXXVI (printed pp. 424 to 431) reports a trial of the machine.
CHAPTER = ("magnetic generator", "test", "experiment", "result", "per cent",
           "efficiency", "output", "free energy", "perpetual")
CH_LO, CH_HI = 424, 431


def raw_pages():
    """Page bodies exactly as they sit on disk: (printed_page, text)."""
    return [(pp, body) for _fp, pp, _i, body, _o in GQ.load_pages(TXT, clean=False)]


def norm_pages(clean):
    """The normalised index check_quotes.py uses, per page.

    clean=True drops running heads and bare folios first (the GATE index);
    clean=False keeps them (KEEP). The normalisation itself is grep_quote's, so
    this script cannot invent a rule the gate does not use.
    """
    return [(pp, GQ.normalise(body))
            for _fp, pp, body, _raw, _o in GQ.load_pages(TXT, clean=clean)]


def count(term, pages):
    """Hits and the printed pages they are on, over a normalised index.

    The term goes through grep_quote.normalise() too, so a phrase the print breaks
    at a line end still counts on the index that folds it. That is why 'wheelwork
    of nature' is 0 on RAW and 1 on GATE and KEEP.
    """
    t = GQ.normalise(term)
    total, hits = 0, {}
    for pp, body in pages:
        n = body.count(t)
        if n:
            hits[pp] = hits.get(pp, 0) + n
            total += n
    return total, sorted(hits.items())


def raw_count(term, pages):
    t = term.lower()
    total, hits = 0, {}
    for pp, body in pages:
        n = body.lower().count(t)
        if n:
            hits[pp] = hits.get(pp, 0) + n
            total += n
    return total, sorted(hits.items())


def row(term, raw, gate, keep):
    return (f"| `{term}` | {raw[0]} | {gate[0]} | {keep[0]} | "
            f"{', '.join(f'{p}({n})' if n > 1 else str(p) for p, n in raw[1]) or '-'} |")


def main():
    terms = sys.argv[1:] or [t for t, _ in TABLE + EXTRA]
    rp = raw_pages()
    gp = norm_pages(True)
    kp = norm_pages(False)
    print(f"source: {TXT}  (printed page = scan file - {GQ.PAGE_OFFSET})")
    print(f"page bodies: {len(rp)}   terms: {len(terms)}\n")
    print("| search term | RAW | GATE | KEEP | printed pages (RAW) |")
    print("|---|---|---|---|---|")
    for t in terms:
        print(row(t, raw_count(t, rp), count(t, gp), count(t, kp)))
    print(f"\nchapter XXXVI only, printed pp. {CH_LO} to {CH_HI} (RAW):")
    ch = [(pp, b) for pp, b in rp if CH_LO <= pp <= CH_HI]
    print(f"  pages in scope: {len(ch)}")
    for t in CHAPTER:
        n, pgs = raw_count(t, ch)
        print(f"  {t}: {n} {pgs if n else ''}")


if __name__ == "__main__":
    main()
