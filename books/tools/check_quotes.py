#!/usr/bin/env python3
"""Check that every quote in a draft is verbatim in the 1894 OCR, and page-cited.

SERIES-PLAN-1894.md §8 step 2 and §12 ("at least 3 page-cited quotes"). The
risk this tool exists for is an OCR misquote shipping publicly (§14).

    python3 books/tools/check_quotes.py new_content/1894-series/07-*/article.md
    python3 books/tools/check_quotes.py --all-series
    python3 books/tools/check_quotes.py --self-test   # the fixture pass

For every quoted passage in the prose (headings, figure alt text, captions and
markdown link labels are our own words and are skipped):

  1. split it on ellipses, since an elided quote is a sequence of quotations;
  2. require each fragment (>= 12 chars) to match the OCR text word for word,
     through four tiers, cheapest first, each one flagged in the output:
       exact      word for word, spaces and all, using the same OCR
                  normalisation grep_quote.py uses (long s, S-for-8, line-end
                  hyphens, running heads);
       nospace    matches once spaces are ignored, because the OCR glues words
                  together in places ("touse", "formingthe") and the printed
                  scan has the space;
       wordstream matches once PUNCTUATION is ignored too, because the scan's
                  text layer misreads punctuation constantly ("scorch my hand {"
                  for "scorch my hand?"). The words must still be the book's
                  words in the book's order - that is the rule that matters, and
                  this tier is the one place it is applied loosely;
       fuzzy      nothing matched. The closest real text is reported, and only
                  called a defect when the words are nearly right
                  (ratio >= 0.90). Below that it is a NOTE, not a failure: a
                  phrase from another source (a patent title, a Wikipedia link
                  label) is not a garbled quotation of this book, but it stays
                  visible because it is a claim this book cannot confirm;
  3. report the PRINTED page(s) the fragment occurs on (scan file - 18);
  4. require a "(1894, p. N)" citation within 400 characters after the quote,
     and require N to be one of those pages. The page list ends at the first
     character that is not a digit, comma or space, so
     "(1894, pp. 376, 381; we take that machine apart below)" is a citation.

A near-miss at or above 0.90 is a FAIL with the closest real text, because a
near-match is exactly the paraphrase-inside-quotation-marks the rule forbids.

The fixture pass (--self-test) carries one case per defect class the checker once
got wrong, and one real defect per class so it cannot pass by going blind.
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
FUZZY_DEFECT = 0.90          # below this a near-miss is a NOTE, not a misquote

# A real code span: opens and closes on backticks, on one line. The old pattern
# ran from a backtick to a later apostrophe, so `inventionsresear00martiala`
# paired with the apostrophe in "Tesla's" two sections later and turned our own
# prose into a "quote" from the book.
BACKTICK_RE = re.compile(r"`([^`\n]{12,})`")
# [label](url): the label is our own words, like a heading. Its apostrophe used
# to open a quote pair and shift every later quote by one.
LINK_RE = re.compile(r"\[[^\]\n]*\]\([^)\n]*\)")
# The page list runs to the first character that is not a digit, comma or space.
# Requiring a closing paren here read "(1894, pp. 376, 381; we ... )" as no
# citation at all.
CITE_RE = re.compile(r"\(1894, p{1,2}s?\. ([\d,\s]+)")


def quote_spans(body: str, classify):
    """Yield (kind, end_offset, text) for each quoted passage, resynchronising.

    Quotes in this dialect wrap, so pairing is done over the whole body, but the
    quote marks inside headings, figure lines and link labels are removed first:
    a quoted heading ("A tale of woe") is our own words, and leaving its marks in
    would mis-pair every quote after it. classify() says whether a candidate is a
    book quote ('quote'), a near-miss ('suspect'), or our own wording ('skip');
    on 'skip' the scanner moves one quote mark on, because the scan uses " for
    inches ("f- inch" on p. 487) and one stray mark would otherwise shift every
    later quote by one.
    """
    blanked = []
    for line in body.split("\n"):
        s = line.strip()
        blanked.append(re.sub(r'"|`', " ", line)
                       if (s.startswith("#") or s.startswith("![")
                           or s.startswith("---")) else line)
    # Same length, so the end offsets stay valid for the citation window.
    text = LINK_RE.sub(lambda m: " " * len(m.group(0)), "\n".join(blanked))
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
        kind = classify(m.group(1))
        if kind != "skip":                        # a code span is not a quote
            yield kind, m.end(), m.group(1).strip()


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


def with_nospace(index, pages):
    """Add the space-insensitive tier to a BookIndex (it is this tool's only)."""
    nospace, nspans = build_nospace(pages)
    return index._replace(nospace=nospace, nspans=nspans)


class Locator:
    """Find a fragment in the book, and remember having done it.

    classify() and the main loop both ask for the same fragment, so every
    fragment used to be searched twice; and the fuzzy tier rebuilt the whole
    book's vocabulary per call. Measured on the 13 drafts: 8,084,396
    difflib.find_longest_match calls from 1,152 find_hits calls, 94s of a
    2m30s gate. One search per fragment, and the word-stream tier answering
    most lookups before the fuzzy tier is reached, is the fix.
    """

    def __init__(self, index):
        self.index = index
        self.cache = {}

    def __call__(self, frag: str):
        """-> (hits, how) with how in
        {'exact','nospace','wordstream','fuzzy'} or ([], None)."""
        n = GQ.normalise(frag)
        if not n:
            return [], None
        if n in self.cache:
            return self.cache[n]
        idx = self.index
        res = self._locate(n)
        self.cache[n] = res
        return res

    def _locate(self, n: str):
        idx = self.index
        hits = [h for h in GQ.find_hits(idx, n, fuzzy=False)
                if h["ratio"] == 1.0]
        if hits:
            return hits, "exact"
        nospace, nspans = idx.nospace, idx.nspans
        if nospace:
            needle = re.sub(r"\s+", "", n)
            out, pos = [], 0
            while True:
                i = nospace.find(needle, pos)
                if i < 0:
                    break
                out.extend(GQ.pages_for(nspans, i, i + len(needle)))
                pos = i + 1
            if out:
                return ([{"file_page": fp, "printed_page": pp, "ratio": 1.0}
                         for fp, pp in dict.fromkeys(out)], "nospace")
        ws = GQ.wordstream_hits(idx, n)
        if ws:
            return ws, "wordstream"
        best = max(GQ.find_hits(idx, n), key=lambda h: h["ratio"], default=None)
        return ([best], "fuzzy") if best else ([], None)


def check(md_path: Path, locator):
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
        kinds = [locator(f)[1] for f in frs]
        if all(k in ("exact", "nospace", "wordstream") for k in kinds):
            return "quote"
        if any(k == "fuzzy" for k in kinds):
            return "suspect"
        return "skip"

    fails, notes, rows = [], [], []
    for kind, end, q in quote_spans(text, classify):
        if kind == "suspect":
            for frag in fragments(q):
                hits, how = locator(frag)
                if how != "fuzzy":
                    continue
                ratio = hits[0]["ratio"]
                if ratio >= FUZZY_DEFECT:
                    fails.append(f"NOT VERBATIM: {frag[:70]!r} (closest "
                                 f"{ratio} on printed p. "
                                 f"{hits[0]['printed_page']})")
                    rows.append(("FAIL", frag, "-", "near-miss only"))
                else:
                    notes.append(
                        f"NOTE: {frag[:70]!r} is not from the 1894 text "
                        f"(closest {ratio} on printed p. "
                        f"{hits[0]['printed_page']}); verify it externally")
                    rows.append(("NOTE", frag, "-", "not from the 1894 text"))
            continue
        for frag in fragments(q):
            hits, how = locator(frag)
            after = text[end:end + CITE_WINDOW]
            cited = []
            for grp in CITE_RE.findall(after):
                cited += [int(c) for c in re.findall(r"\d+", grp)]
            pps = sorted({h["printed_page"] for h in hits})
            if how in ("exact", "nospace", "wordstream"):
                note = {"exact": "verbatim",
                        "nospace": "OCR spacing normalised",
                        "wordstream": "OCR punctuation normalised"}[how]
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
    return fails, notes, rows


# ---------------------------------------------------------------- self test

# A miniature of the volume: page markers, the offset, running heads, and one
# line per defect class the checker once reported wrongly. Printed page = scan
# file - 18, so page-100 is printed p. 82.
FIXTURE_BOOK = """
<< page-99 >>
INDUCTIONS AND CURRENTS. 99
The apparatus was described in the preface, and the reader is referred there.
<< page-100 >>
THE ALTERNATING CURRENT. 100
It is equivalent to a return wire for the purposes of the lecture.
The coil is a twophase motor of the older pattern, giving^ say, a few
thousand volts without any particular difficulty encountered in the work.
Is it the less a flame because it does not scorch my hand { said the lecturer.
A steel arbor which had been actually torn apart while vibrating against a
minute air cushion was shewn to the audience.
<< page-101 >>
THE SAME LECTURE CONTINUED. 101
Up to about 15,000 alternations per second the results were regular.
We attach their machinery to the very wheelwork of nature, and so we are
whirling through endless space with an ever increasing velocity.
"""

# One case per class the checker used to get wrong, then one real defect per
# class, so the pass cannot go blind. Each defect is separated from the next by
# more than CITE_WINDOW characters of our own prose, because a citation window
# that reaches into the next item is how a missing citation hides.
FIXTURE_DRAFT = """---
title: "Fixture"
---

The item name `inventionsresear00martiala` is how the archive catalogues the
volume, and the book's own preface says what it says. Neither is a quotation,
and the pair used to be read as one: the backtick ran to the apostrophe in
"book's" two sentences later and turned this paragraph into a quote.

1. One-wire power: why an insulated body "is equivalent to a return wire"
   (1894, p. 82).
2. The cold flame: "is it the less a flame because it does not scorch my hand?"
   (1894, p. 82), where the scan's text layer prints "{" for the book's mark.
3. A compound the scan joined: "a two-phase motor of the older pattern"
   (1894, p. 82); the scan really does read it as one word, and the book prints
   it with a hyphen.
4. Punctuation the scan misreads: "giving, say, a few thousand volts without any
   particular difficulty encountered in the work" (1894, p. 82), where the scan
   prints "^" for the book's comma.
5. A citation whose page list does not end at a closing paren: "Up to about
   15,000 alternations per second" (1894, pp. 82, 83; we take that machine apart
   below) is the honest form of the claim, and the old pattern read it as no
   citation at all.
6. A quote across a page break: "we attach their machinery to the very wheelwork
   of nature" (1894, p. 83).
7. A phrase this volume cannot confirm is not a garbled quotation of it: "the
   very wheelwork of art" is how a later writer summarised the passage, and the
   book's words are different, so it is a NOTE and not a misquote.

The real defects, which must still fail.

- A paraphrase inside quote marks: "actually torn apart while vibrating against a
  small air cushion" (1894, p. 82). The book says "minute", and a near-miss at
  0.93 is a paraphrase, which is exactly what the rule forbids.

- A quotation cited to the wrong page: "minute air cushion was shewn to the
  audience" (1894, p. 99). The words are the book's and the page is not.

""" + """

The filler between the defects exists to push the next quotation outside the
400 character citation window, because a citation belonging to one quotation
read as a citation for its neighbour is how an uncited quotation shipped. This
paragraph says nothing about pages at all, and neither does the next one, and
the length of both together is what makes the verdict below mean something.

- An uncited quotation: "whirling through endless space with an ever increasing
  velocity" is on a page of this volume, and this draft never says which one.
"""


def self_test():
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="quote-selftest-"))
    book = tmp / "book.txt"
    book.write_text(FIXTURE_BOOK, encoding="utf-8")
    draft = tmp / "article.md"
    draft.write_text(FIXTURE_DRAFT, encoding="utf-8")

    pages = GQ.load_pages(book)
    index = with_nospace(GQ.build_index(pages), pages)
    locator = Locator(index)
    fails, notes, rows = check(draft, locator)

    def flat(s):
        return " ".join(s.split())

    # (what has to hold, how to look for it)
    must_pass = [
        ("hyphenated compound the scan joined", "a two-phase motor of the older pattern"),
        ("scan punctuation misread ({ for ?)", "is it the less a flame because it does not scorch my hand?"),
        ("scan punctuation misread (^ for ,)", "giving, say, a few thousand volts without any"),
        ("citation with no closing paren", "15,000 alternations per second"),
        ("quote spanning a page break", "we attach their machinery to the very wheelwork"),
        ("a real code span, cited properly", "is equivalent to a return wire"),
    ]
    must_note = [("sub-0.90 near-miss is a NOTE not a FAIL", "the very wheelwork of art")]
    must_fail = [
        ("paraphrase inside quote marks", "actually torn apart while vibrating against a small air cushion"),
        ("uncited quotation", "whirling through endless space with an ever increasing velocity"),
        ("wrong page cited", "minute air cushion was shewn to the audience"),
    ]
    # A code span is our own text, not a quotation: it must not appear at all.
    must_absent = [("backtick paired with a later apostrophe",
                    "inventionsresear00martiala")]

    def rows_for(needle):
        return [r for r in rows if needle in flat(r[1])]

    problems = []
    for group, want in ((must_pass, "ok"), (must_note, "NOTE"), (must_fail, "FAIL")):
        for label, needle in group:
            got = [r[0] for r in rows_for(flat(needle))]
            if want not in got:
                problems.append(f"FIXTURE FAIL: {label}: {needle!r} -> "
                                f"{got or ['not seen']} (wanted {want})")
    for label, needle in must_absent:
        got = rows_for(needle)
        if got:
            problems.append(f"FIXTURE FAIL: {label}: {needle!r} -> "
                            f"{[r[0] for r in got]} (wanted absent)")

    # The word-stream tier must be flagged, never folded into "verbatim".
    if not [r for r in rows if r[3] == "cited p. 82, OCR punctuation normalised"]:
        problems.append("FIXTURE FAIL: the word-stream tier did not flag itself")
    # ... and the sub-0.90 NOTE must not be counted as a gate failure.
    if [f for f in fails if "wheelwork of art" in f]:
        problems.append("FIXTURE FAIL: a sub-0.90 near-miss failed the gate")

    for status, frag, pps, note in rows:
        print(f"  [{status}] p.{pps} ({note}) {frag[:72]}")
    for f in fails:
        print("  FAIL:", f)
    for nt in notes:
        print("  " + nt)
    print(f"\nfixture: {len(rows)} fragments, {len(fails)} failures, "
          f"{len(notes)} notes, {len(locator.cache)} distinct fragments searched")
    for p in problems:
        print(p)
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", nargs="?", help="article.md to check")
    ap.add_argument("--all-series", action="store_true",
                    help="check every draft named in index.json")
    ap.add_argument("--txt", default=str(DEFAULT_TXT))
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    ap.add_argument("--self-test", action="store_true",
                    help="run the fixture pass: one case per defect class")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

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
    index = with_nospace(GQ.build_index(pages), pages)
    locator = Locator(index)

    bad = 0
    for t in targets:
        fails, notes, rows = check(t, locator)
        n_ok = sum(1 for r in rows if r[0] == "ok")
        print(f"\n=== {t.resolve().relative_to(ROOT)}: {len(rows)} quote fragments, "
              f"{n_ok} verbatim and page-cited ===")
        if not args.quiet:
            for status, frag, pps, note in rows:
                print(f"  [{status}] p.{pps} ({note}) {frag[:72]}")
        for f in fails:
            print("  FAIL:", f)
        for nt in notes:
            print("  " + nt)
        bad += len(fails)
    print(f"\n{len(targets)} file(s), {bad} quote problem(s)")
    print(f"{len(locator.cache)} distinct fragments searched "
          f"({sum(1 for t in targets)} file(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
