#!/usr/bin/env python3
"""Re-run the volume word counts a draft asserts, whole-word and substring.

Every "X occurs N times in the volume" claim in a series draft must be re-run
before the draft is committed — a count is its regex, and one such claim in the
05 draft was wrong when it was first written down. For each term this prints:
whole-word count, substring count, and the printed pages of the substring hits
with a count per page, because "appears on 3 pages" and "appears 5 times" are
different claims and a table that does not say which it is stating cannot be
checked against either.

This is also the tool behind the word-search data page (PLAN-1894.md T2): the
counts that page states come from this script's output, and the page prints the
command so a reader can run it.

    python3 books/tools/count_terms.py "free energy" "perpetual" "magnetic generator"
    python3 books/tools/count_terms.py --keep-furniture "magnetic generator"

What the two counts mean, and why they differ:

  whole-word   the term stands alone, with a non-word character either side.
               "pyro-magnetic" is NOT a whole-word hit inside "thermopyro-
               magnetic"; it is a substring hit.
  substring    the term appears anywhere inside a longer word or compound.

Both counts run against the same normalised text grep_quote.py uses for quote
matching: ligatures folded, long-s folded, the S-for-8 artefact folded, curly
punctuation folded, line-end hyphens and letter-joined hyphenated compounds
un-hyphenated, whitespace collapsed, everything lower case. That is why
"free-energy" is searched as "freeenergy": the scan breaks the word at the end
of a line, and a count that missed those would be a count of a different string
than the one the book prints.

By default the index also DROPS running heads and bare folios (grep_quote.py
strip_furniture), because they interleave into sentences and break quote
matching. That rule is width- and case-based, and it also drops short display
lines: a chapter title like "MOTORS AND PYRO-MAGNETIC GENERATORS." on printed
p. 424 is not in the default index. --keep-furniture keeps everything, and the
difference between the two numbers is a fact about the page, not a bug: it says
the only occurrence on that page is a title, not a sentence.

Printed page = scan file page - 18 (SERIES-PLAN §0). A hit reported at printed
page -1 or 0 is in front matter, which carries no printed folio and must be
cited by scan file instead.
"""
import argparse
import re
import shlex
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
import grep_quote as GQ  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                            formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("terms", nargs="+", help="term to count, exactly as it would be quoted")
ap.add_argument("--txt", default=str(GQ.DEFAULT_TXT))
ap.add_argument("--keep-furniture", action="store_true",
                help="index running heads, bare folios and short display lines too "
                     "(default: they are dropped, which is what makes a chapter "
                     "title count differently from a sentence)")
ap.add_argument("--json", action="store_true")
args = ap.parse_args()

pages = GQ.load_pages(Path(args.txt), clean=not args.keep_furniture)
index = GQ.build_index(pages)
ntext, spans = index.ntext, index.spans

if args.json:
    out = {"command": shlex.join(sys.argv),
           "text": str(Path(args.txt).relative_to(GQ.BOOKS.parent)),
           "furniture": "kept" if args.keep_furniture else "dropped",
           "normalisation": "grep_quote.normalise: ligatures, long-s, S-for-8, "
                            "curly punctuation, line-end and letter-joined "
                            "hyphens folded; whitespace collapsed; lower case",
           "page_offset": GQ.PAGE_OFFSET,
           "terms": {}}
else:
    print("# command: " + shlex.join(sys.argv))
    print(f"# text: {Path(args.txt).relative_to(GQ.BOOKS.parent)}   "
          f"running heads and display lines: "
          f"{'kept' if args.keep_furniture else 'dropped'}   "
          f"printed page = scan file - {GQ.PAGE_OFFSET}")
    print("# whole-word = the term stands alone; substring = the term inside a "
          "longer word or compound; both run on the normalised text")

for term in args.terms:
    n = GQ.normalise(term)
    sub = list(re.finditer(re.escape(n), ntext))
    whole = [m for m in re.finditer(r"(?<![\w])" + re.escape(n) + r"(?![\w])", ntext)]
    per_page = {}
    for m in sub:
        for _fp, pp in GQ.pages_for(spans, m.start(), m.end()):
            per_page[pp] = per_page.get(pp, 0) + 1
    if args.json:
        out["terms"][term] = {"whole_word": len(whole), "substring": len(sub),
                              "pages": {str(k): v for k, v in
                                        sorted(per_page.items())}}
    else:
        pages_txt = ", ".join(f"{p} x{c}" if c > 1 else str(p)
                              for p, c in sorted(per_page.items())) or "-"
        print(f"{term!r}: whole-word={len(whole)} substring={len(sub)} "
              f"pages=[{pages_txt}]")

if args.json:
    print(__import__("json").dumps(out, indent=2))
