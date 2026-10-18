#!/usr/bin/env python3
"""feature-007/a10-claims - the claims check for this article, as a script.

word_counts.py in this directory measures the five SERIES-PLAN-1894.md Appendix D
rows the page shows. This measures the REST of the evidence the page puts in
front of a reader, and prints PASS or FAIL against the sentence in article.md
that states it:

  numbers()  the Appendix D row itself, read out of the plan and re-measured;
             the corpus sizes the method section names; the counts the 'What the
             Internet Gets Wrong' section prints; the single-occurrence claims;
             the chapter XXXVI scoped counts; the sentence-level claims about
             printed pp. 8 and 236; and the claim written beside pages_used in
             the front matter.
  sources()  the Sources block. make_article.py sources_block() renders it, so a
             chapter range, a chapter title, a footnote quoted with a page cite
             or a site page named by title in that block is a claim in front of a
             reader exactly like a count in the body. The chapter ranges are
             measured against the volume's own chapter headings, not against a
             contents list typed by hand.
  quotes()   every sentence that reports what another page on this site says.
             SERIES-PLAN-1894.md 4.1 lets a series page report a live page's
             claim "in their own words" and forbids it adding a product claim of
             its own. That is only true if each quoted fragment is actually on
             the page it names. No tool in books/tools checks that; this does.

Two rules about how a count is measured, learned the hard way at this task and
built into every check below:

  * A raw substring count cannot cross a line break. 'as rapidly as 400 to 500
    times a minute' is 0 raw and 1 once the OCR's line break is folded, because
    the page ends a line inside it. A quote is therefore checked through
    grep_quote.normalise, the same folding books/tools/check_quotes.py uses, and
    a count the page prints as a raw count is checked raw. Each check says which.
  * A citation regex has to read both forms this site writes, '(1894, p. N)' and
    '(1894, pp. N, M)'. The first version of this script read only the second
    and reported one citation in a body that carries dozens.

Nothing here edits the draft. Exit 0 only if every check passes.

Usage: python3 claims_check.py            # everything
       python3 claims_check.py --numbers  # counts only
       python3 claims_check.py --sources  # the rendered Sources block only
       python3 claims_check.py --quotes   # live-page and cross-page claims only
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                                  # tesla-generator/
TOOLS = ROOT / "books" / "tools"
SITE = ROOT / "website"
sys.path.insert(0, str(TOOLS))
import grep_quote as GQ                                # noqa: E402

TXT = ROOT / "books" / "extracted" / "tesla-1894-plain.txt"
FULL = ROOT / "books" / "extracted" / "tesla-1894-fulltext.txt"
SCANS = ROOT / "books" / "pdf-pages-tesla-1894"
DRAFT = HERE / "article.md"
REGISTER = HERE / "quotes.md"
A08_REGISTER = ROOT / "new_content/1894-series/08-tesla-weird-inventions-1894/quotes.md"
PLAN = ROOT / "SERIES-PLAN-1894.md"

# The one out-link this page carries that does not resolve yet, and who owns the
# page. It is allowed to be missing and is reported as pending; every other .html
# link in the body has to resolve, so a new dead link fails instead of joining it.
PENDING_LINKS = {"tesla-1894-word-search.html": "feature-008/t2"}

# The fragments this page quotes from this site's own commercial pages, keyed by
# the page each is attributed to. Derived from the body below and compared with
# this set, so a fragment added, removed or moved to another page fails here
# rather than shipping.
EXPECTED_COMMERCIAL = {
    "tesla-magnetic-generator-worth-it.html": ["free energy", "requires a prime mover"],
    "free-electricity-from-magnets.html": ["keeps spinning as long as the magnets are in place"],
    "magnetic-generator-scam.html": ["actually produces roughly 5 times more energy "
                                     "than it consumes"],
}

# A unit word beside a number is what makes that number a quantity. Used to test
# the claim that chapter XXXVI states no quantity about any machine.
UNIT_WORDS = (r"°|centigrade|fahrenheit|per cent|volt|ampere|ohm|watt|horse-?power|"
              r"pound|ounce|inch|feet|foot|miles|times a minute|per minute|revolution|"
              r"second|degree|H\. ?p\.|r\.p\.m")

rows = []


def check(label, claimed, measured, where=""):
    ok = str(claimed) == str(measured)
    rows.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    print(f"        claimed   {claimed}\n        measured   {measured}"
          + (f"\n        the draft says: {where}" if where else ""))


def front_matter():
    return DRAFT.read_text(encoding="utf-8").split("\n---\n", 1)[0]


def body():
    return DRAFT.read_text(encoding="utf-8").split("\n---\n", 1)[1]


def raw_pages():
    """[(printed_page, page body as it sits on disk)], nothing normalised."""
    return [(pp, b) for _fp, pp, _i, b, _o in GQ.load_pages(TXT, clean=False)]


def gate_pages():
    """The index books/tools/check_quotes.py builds: running heads and bare
    folios dropped, then normalised. This is the 'index the quote checker
    builds' the method section names."""
    return [(pp, GQ.normalise(b)) for _fp, pp, b, _r, _o in GQ.load_pages(TXT, clean=True)]


RAW = raw_pages()
GATE = gate_pages()
RAW_BY_PAGE = dict(RAW)


def rc(term):
    """Exact substring, case-insensitive, over page bodies as on disk.

    That is the method the page states ('Counts are exact substrings,
    case-insensitive, over the whole volume'), so it is the method every count
    the page prints is measured by - including 'free' and 'unity', which are
    substrings and not words.
    """
    t = term.lower()
    return sum(b.lower().count(t) for _pp, b in RAW)


def rc_pages(term):
    """Printed pages carrying at least one raw hit, with the per-page count."""
    t = term.lower()
    return [(pp, b.lower().count(t)) for pp, b in RAW if t in b.lower()]


def gc(term):
    """Same term over the index the quote checker builds."""
    t = term.lower()
    return sum(b.count(t) for _pp, b in GATE)


def gc_pages(term):
    t = term.lower()
    return [pp for pp, b in GATE if t in b]


def norm_count(term, page=None):
    """Count through grep_quote.normalise, i.e. across a line break in the print.

    This is the matcher books/tools/check_quotes.py uses for a quote, so it is
    how a quoted sentence is checked. page= pins it to one printed page.
    """
    needle = GQ.normalise(term)
    n = 0
    for pp, b in RAW:
        if page is not None and pp != page:
            continue
        n += GQ.normalise(b).count(needle)
    return n


def appendix_d():
    """The word-search row of SERIES-PLAN-1894.md Appendix D, parsed."""
    text = PLAN.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"## Appendix D.*?Word search of the 1894 volume.*?\n\n", text, re.S)
    if not m:
        return None
    row = m.group(0)
    terms = {}
    for term in re.findall(r"`([^`]+)`", row):
        n = re.search(re.escape(term) + r"[^(]*?\b(\d+)", row)
        if n:
            terms[term] = int(n.group(1))
    pages = [int(x) for grp in re.findall(r"\(pp\.\s*([\d,\s]+)\)", row)
             for x in re.findall(r"\d+", grp)]
    return terms, pages


def numbers():
    # ---- the plan's own row, read out of the plan, then re-measured ----
    ad = appendix_d()
    if ad is None:
        check("Appendix D word-search row found in SERIES-PLAN-1894.md", True, False)
    else:
        terms, ad_pages = ad
        for term in ("free energy", "free-energy", "perpetual", "over unity",
                     "over-unity", "magnetic generator"):
            check(f"Appendix D states '{term}' {terms.get(term)} and the text measures it",
                  terms.get(term), rc(term),
                  "the page prints Appendix D's numbers, so both sides are checked")
        check("Appendix D's 'magnetic generator' 5 is 5, and its page list is the pages "
              "the hits are on", (5, sorted(set(ad_pages))),
              (rc("magnetic generator"), sorted({pp for pp, _n in rc_pages("magnetic generator")})),
              "free energy 0, perpetual 0, over unity 0, magnetic generator 5 (pp. 6, 424, 429, 496)")

    # ---- the corpus sizes the method section names ----
    whole = TXT.read_text(encoding="utf-8", errors="replace")
    check("plain.txt whitespace words", "174,169", f"{len(whole.split()):,}",
          "one text file of 174,169 words")
    check("page bodies in plain.txt", "506", len(RAW), "marked into 506 page bodies")
    check("words inside those page bodies", "172,651",
          f"{sum(len(b.split()) for _pp, b in RAW):,}",
          "the counts below run over those page bodies, which are 172,651 words")
    check("fulltext.txt whitespace words", "176,810",
          f"{len(FULL.read_text(encoding='utf-8', errors='replace').split()):,}",
          "A second text file of the same scan runs 176,810 words")
    check("fulltext.txt is the only file of this scan that rounds to 177,000", True,
          round(len(FULL.read_text(encoding='utf-8', errors='replace').split()), -3) == 177000
          and round(len(whole.split()), -3) != 177000,
          "it is the only file of this scan whose count rounds to the plan's '177,000 words'")
    check("GATE index words", "167,998", f"{sum(len(b.split()) for _pp, b in GATE):,}",
          "it is 167,998 words rather than 174,169")
    check("page images of our scan", "518", len(list(SCANS.glob("*.pdf"))),
          "Our copy is 518 page images")

    # ---- the count list the page prints, against the measurement ----
    body_text = body()
    printed_terms = {}
    for line in body_text.splitlines():
        if not line.startswith("- '") or ":" not in line:
            continue
        head, tail = line.split(":", 1)
        terms = re.findall(r"'([^']+)'", head)
        m = re.search(r"(\d+)", tail)
        if not terms or not m:
            continue
        printed = int(m.group(1))
        for term in terms:
            printed_terms[term] = printed
            check(f"the printed count list says '{term}' {printed}", printed, rc(term),
                  line.strip()[:160])
        # a term quoted after the first colon, e.g. "and the stem 'perpetu' 0"
        for term, n in re.findall(r"'([^']+)'\s*(\d+)", tail):
            printed_terms[term] = int(n)
            check(f"the printed count list says '{term}' {n}", int(n), rc(term),
                  line.strip()[:160])
    check("the count list carries the Appendix D terms and the 'perpetu' stem",
          sorted(["free energy", "free-energy", "perpetual", "perpetu", "over unity",
                  "over-unity", "magnetic generator"]), sorted(printed_terms),
          "the counts the brief asks for, whole volume")

    # The two counts Appendix D does not carry.
    check("'free'", 97, rc("free"), "'free' 97 times")
    check("'free' followed by 'ener' in any form", 0,
          sum(len(re.findall(r"free\s+ener", b, re.I)) for _pp, b in RAW),
          "and not once before the word 'energy'")
    words = {}
    for _pp, b in RAW:
        for m in re.finditer(r"[a-z]*unity", b.lower()):
            words[m.group(0)] = words.get(m.group(0), 0) + 1
    check("'unity'", 9, sum(words.values()), "'unity' 9 times")
    check("'unity' outside community / impunity / opportunity", 0,
          sum(n for w, n in words.items() if w not in ("community", "impunity", "opportunity")),
          f"all 9 inside community, impunity and opportunity; measured {words}")

    # 'magnetic generator' on both indices, which is the paragraph the method
    # section spends its honesty on.
    check("'magnetic generator' raw, on four printed pages", (5, 4),
          (rc("magnetic generator"), len({pp for pp, _n in rc_pages("magnetic generator")})),
          "Over the text as it sits on disk 'magnetic generator' counts 5, on four printed pages")
    check("the raw hits are on printed pp. 6, 424 (twice), 496",
          [(6, 1), (424, 1), (429, 2), (496, 1)], rc_pages("magnetic generator"),
          "'magnetic generator': 5, at printed pp. 6, 424, 429 twice and 496")
    check("'magnetic generator' on the index the quote checker builds, on three pages",
          (4, 3), (gc("magnetic generator"), len(set(gc_pages("magnetic generator")))),
          "over the stripped index it counts 4, on three")
    check("the missing hit is the chapter XXXVI display heading on printed p. 424",
          [6, 429, 496], sorted(set(gc_pages("magnetic generator"))),
          "The missing hit is chapter XXXVI's display heading, which is display type")
    check("that heading is named in the body in single quotes and never inside a double-quoted "
          "passage, so check_quotes never sees it", (1, 0),
          (body_text.count("THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS"),
           sum(1 for q in re.findall(r'"([^"]+)"', body_text)
               if "THERMO-MAGNETIC MOTORS" in q)),
          "named in this article rather than quoted: 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC "
          "GENERATORS' (1894, p. 424)")

    # The magnet/generator regex sentence. Both orders, and the hyphen question.
    fwd = [(pp, m.group(0)) for pp, b in RAW
           for m in re.finditer(r"[a-z-]*magnet[a-z-]*\s+[a-z-]*generat[a-z]*", b, re.I)]
    rev_loose = [(pp, m.group(0)) for pp, b in RAW
                 for m in re.finditer(r"[a-z-]*generat[a-z]*\s+[a-z-]*magnet[a-z-]*", b, re.I)]
    rev_strict = [(pp, m.group(0)) for pp, b in RAW
                  for m in re.finditer(r"\b[a-z]*generat[a-z]*\s+[a-z]*magnet[a-z]*\b", b, re.I)]
    check("a magnet word followed by a generator word, either spelling", 5, len(fwd),
          "Set a regex for a magnet word followed by a generator word and the volume returns 5")
    check("of those, none outside a pyro- compound", 0,
          len([p for p in fwd if "pyro" not in p[1].lower()]),
          "all of them 'pyro-magnetic generator(s)' or 'pyromagnetic generator(s)'")
    check("a generator word followed by a magnet word, word boundaries", 0, len(rev_strict),
          "Reverse the order and the count is 0")
    check("the same order, hyphen tolerated inside the magnet word", 1, len(rev_loose),
          "It stays 0 unless the pattern lets a hyphen stand inside the magnet word, and then the "
          "single hit it produces")
    check("that one hit is the OCR's 'the generator iielcl-magnets' on printed p. 35",
          [(35, "generator iielcl-magnets")], rev_loose,
          "'the generator iielcl-magnets' (1894, p. 35), where 'iielcl' is not a word")
    check("the line it sits in reads 'for exciting the generator iielcl-magnets or for other "
          "purposes'", True,
          "for exciting the generator iielcl-magnets or for other purposes"
          in " ".join(RAW_BY_PAGE[35].split()),
          "the page's own line, which is why the phrase cannot be quoted as a generator name")

    # Single-occurrence claims. Raw where the page prints a raw count, normalised
    # where the claim is about a quoted sentence the print breaks.
    check("'the earth's potential'", 1, rc("the earth's potential"), "it occurs once, here")
    check("'as rapidly as 400 to 500 times a minute' once, on printed p. 424, through the "
          "same folding check_quotes uses", 1,
          norm_count("as rapidly as 400 to 500 times a minute", page=424),
          "vibrating \"as rapidly as 400 to 500 times a minute\" (1894, p. 424)")
    check("that string is 0 as a raw substring, because the page ends a line inside it", 0,
          rc("as rapidly as 400 to 500 times a minute"),
          "the reason no count on this page is taken from a raw substring of a quoted sentence")
    check("'400 to 500'", 1, rc("400 to 500"), "It is one string in 174,169 words")
    check("'inexhaustible'", 1, rc("inexhaustible"),
          "which is the only time that word appears in the volume")
    check("'the generator iielcl-magnets' once, raw, on printed p. 35", 1,
          rc("the generator iielcl-magnets"),
          "'the generator iielcl-magnets' (1894, p. 35)")

    # The phrases the product vocabulary invites, printed as 0 on the page.
    for term in ("512,340", "512340", "512 340", "coil for electromagnets", "bifilar",
                 "free electricity", "magnet motor", "magnetic engine", "magnetic dynamo"):
        check(f"'{term}'", 0, rc(term), "printed as 0 among the phrases the book lacks")

    # 'magnetic motor' is 3 raw and never stands alone, and 4 on the index.
    mm = [(pp, b[max(0, m.start() - 30):m.start()]) for pp, b in RAW
          for m in re.finditer("magnetic motor", b, re.I)]
    check("'magnetic motor' raw", 3, len(mm), "'magnetic motor' is 3, and never stands alone")
    check("on printed pp. 6, 46 and 496", [6, 46, 496], sorted(pp for pp, _pre in mm),
          "two of the three are 'Thermo-Magnetic Motors' in the editor's inventory and in the "
          "volume's own index (1894, pp. 6, 496)")
    check("two of the three are preceded by thermo-, so neither is a bare 'magnetic motor'", 2,
          len([1 for _pp, pre in mm if re.search(r"(thermo|electro)-?\s*$", pre, re.I)]),
          "two of the three are 'Thermo-Magnetic Motors'")
    p46 = [pre for pp, pre in mm if pp == 46]
    check("the third is at p. 46, where the text layer puts two words between 'electro' and "
          "'magnetic motor'", 1,
          len([1 for pre in p46 if re.search(r"electro\S*\s+\S+\s*$", pre, re.I)]),
          "the third sits in a line the OCR has scrambled, where 'electro' and 'magnetic motor' "
          "are split by two words that do not belong between them (1894, p. 46)")
    check("printed p. 46 really reads 'an ordinary form of electroof source magnetic motor'", True,
          "an ordinary form of electroof source magnetic motor"
          in " ".join(RAW_BY_PAGE[46].split()),
          "the body does not say what the print says there, and this is what the text layer says")
    check("'magnetic motor' on the index the quote checker builds", 4, gc("magnetic motor"),
          "That count is 3 on the text as it sits on disk and 4 on the index the quote checker "
          "builds")
    check("the extra index hit is at printed p. 55, joined across a line break",
          [6, 46, 55, 496], sorted(set(gc_pages("magnetic motor"))),
          "which joins 'electro-' to 'magnetic motors' across a line break at printed p. 55")
    check("printed p. 55 sets 'electro-magnetic' at a line end and 'motors' on the next line",
          True, bool(re.search(r"electro-magnetic\s*\n?\s*motors", RAW_BY_PAGE[55], re.I)),
          "the mechanism the method section describes")

    # Chapter XXXVI, scoped to its own pages.
    ch = [(pp, b) for pp, b in RAW if 424 <= pp <= 431]
    check("chapter XXXVI pages in the text index", 8, len(ch),
          "over the chapter's eight printed pages")
    for term in ("test", "per cent", "efficiency"):
        check(f"chapter XXXVI '{term}'", 0,
              sum(b.lower().count(term) for _pp, b in ch), "are all 0")
    check("chapter XXXVI 'output'", 1, sum(b.lower().count("output") for _pp, b in ch),
          "and 'output' is 1")
    out_ctx = [b[max(0, m.start() - 90):m.start() + 20] for _pp, b in ch
               for m in re.finditer("output", b, re.I)]
    check("that one 'output' is a design property with no number on it", True,
          len(out_ctx) == 1 and "meaning larger output" in " ".join(out_ctx[0].split())
          and not re.search(r"\d", out_ctx[0]),
          "'output' is 1, a design property with no number on it")
    for unit in ("watt", "horse-power", "ampere", "volt", "revolutions per", "velocity"):
        check(f"chapter XXXVI '{unit}'", 0,
              sum(b.lower().count(unit) for _pp, b in ch),
              "the chapter gives no machine a rating in any unit")
    qty = [(pp, m.group(0)) for pp, b in ch for m in re.finditer(r"\b\d[\d,.]*\b", b)
           if re.search(UNIT_WORDS, b[max(0, m.start() - 40):m.start() + 60], re.I)]
    check("numbers in the chapter that state a quantity: the rate at p. 424 and the "
          "temperature at p. 429, nothing else",
          [(424, "400"), (424, "500"), (429, "600")], qty,
          "The only other number on those eight pages that states a quantity is a temperature")
    check("the temperature the p. 429 experiment gives is 'about 600° centigrade'", 1,
          norm_count("a temperature of about 600° centigrade", page=429),
          "the page gives its heat as about 600 degrees centigrade")
    check("and it says thin iron loses its magnetic properties at that temperature", 1,
          norm_count("the iron somewhat suddenly loses its magnetic properties, if it be very thin",
                     page=429),
          "says that at that temperature thin iron loses its magnetic properties")

    # The two index entries, on the pages the body puts them on.
    for entry, page in (("Generators, Pyromagnetic", 494), ("Pyromagnetic Generators", 496),
                        ("Thermo-Magnetic Motors", 496)):
        check(f"index entry {entry!r} on printed p. {page}", 1,
              sum(b.count(entry) for pp, b in RAW if pp == page),
              "the body cites the first two, the front matter's read the third")

    # Printed p. 236: how many sentences stand between the wheelwork clause and
    # the insult. The body says 'three sentences early' in one place and used to
    # say 'four sentences later' in another.
    p236 = RAW_BY_PAGE[236]
    anchor = "the very wheelwork of\nnature."
    a = p236.find(anchor)
    b_end = p236.find("most inefficient machine")
    span = p236[a + len(anchor):b_end] if a >= 0 and b_end > a else ""
    n_sent = len(re.findall(r"[.!?]\s", span)) + 1 if span else -1
    check("sentences between 'the very wheelwork of nature.' and the insult on printed p. 236",
          3, n_sent,
          "It is a conditional that ends three sentences later in an insult about a machine's "
          "efficiency / the cut version stops three sentences early")
    check("the circulated cut ends at 'nature' and the page runs on past it", True,
          "the very wheelwork of\nnature. Of all, living or dead, Crookes came nearest" in p236,
          "The version in circulation ends at 'nature'")

    # Printed p. 8: the efficiency figures, and what the page says about who ran
    # the tests. The body used to attach the named tests to the 94-and-95 figure.
    p8 = " ".join(RAW_BY_PAGE[8].split())
    check("printed p. 8 gives 94 and 95 per cent with the three wire system", True,
          "up to as high as 94 and 95 per cent" in p8 and "with the three wire system" in p8,
          "Its top efficiency figure is 94 and 95 per cent, for larger motors on the three-wire "
          "system")
    check("that sentence names no tester of its own", True,
          not re.search(r"94 and 95 per cent[^.]*\b(Anthony|Schmid|Pittsburgh)\b", p8),
          "the body no longer says the named trials ran it")
    check("the tests the page does name come before it, not after", True,
          0 < p8.find("winter of 1887-8") < p8.find("Albert Schmid") < p8.find("94 and 95"),
          "the same page names the tests it is citing: Prof. Anthony's, which it dates to the "
          "winter of 1887-8, and the 1889 Pittsburgh tests made by Tesla and Albert Schmid")
    check("and Appendix D's efficiency row splits them the same way", True,
          "1888 Anthony tests" in PLAN.read_text(encoding="utf-8", errors="replace")
          and "94" in PLAN.read_text(encoding="utf-8", errors="replace"),
          "SERIES-PLAN-1894.md Appendix D, Efficiency record")

    # The claim written beside pages_used: that list is the body's citation set.
    # Both citation forms, '(1894, p. N)' and '(1894, pp. N, M)'.
    text = DRAFT.read_text(encoding="utf-8")
    cite_re = re.compile(r"\(\s*1894,\s*p{1,2}\.\s*([\d,\s]*?\d)\s*\)")
    cited = sorted({int(n) for m in cite_re.finditer(body_text)
                    for n in re.findall(r"\d+", m.group(1))})
    declared = sorted({int(x) for x in
                       re.search(r"pages_used:\s*\[([^\]]+)\]", text).group(1).split(",")})
    check("pages_used equals the body's citation set, both forms read", declared, cited)
    check("the body carries at least 3 page-cited citations, the qa_page gate", True,
          len(cite_re.findall(body_text)) >= 3, "qa_page.py's own gate is >= 3")

    # The claim that the figure captions stay out of that regex.
    caps = " ".join(re.findall(r'caption: "([^"]+)"', text))
    check("figure captions matching the citation regex", 0, len(cite_re.findall(caps)),
          "the figures add nothing to this list")


def page_text(name):
    t = (SITE / name).read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def page_title(name):
    m = re.search(r"<title>([^<]*)</title>",
                  (SITE / name).read_text(encoding="utf-8", errors="replace"), re.I)
    return m.group(1).strip() if m else ""


# --------------------------------------------------------------- sources -----
# make_article.py sources_block() renders the Sources block, so a chapter range,
# a chapter title, a footnote quoted with a page cite, or one of this site's own
# pages named by title in that block is a claim in front of a reader in exactly
# the way a count in the body is. Nothing else in this repo checks any of it.

CHAP_HEAD = re.compile(r"CH[AP][A-Z]{0,2}T[ERK][A-Z]?\b")   # CHAPTER / CHAPTEE / CHAPTEK
ROMAN = r"[IVXLCDM]{1,8}"


def chapter_starts():
    """(printed page, roman) for every chapter opening in the text layer.

    The OCR sets the word CHAPTER every which way - CHAPTEE, CHAPTEK, CHAPTE R -
    and on some pages interleaves the chapter number into the display heading
    ('CHAPTEK THERMO-MAGNETIC XXXVI. MOTORS...'), so the number is looked for in
    the 200 characters after the heading word rather than right after it. A real
    heading puts a period after the number; a prose cross-reference does not.
    Front matter (printed page < 3) is the volume's own contents list, which
    names every chapter on one page, so it is excluded.
    """
    out = []
    for pp, page_body in RAW:
        if pp < 3:
            continue
        head = page_body[:400]
        for m in CHAP_HEAD.finditer(head):
            r = re.search(r"\s*\b(" + ROMAN + r")\s*\.", head[m.end():m.end() + 200])
            if r:
                out.append((pp, r.group(1)))
                break
    return out


STARTS = chapter_starts()


def measured_range(roman):
    """The range the volume's own chapter headings give one chapter."""
    starts = [pp for pp, r in STARTS if r == roman]
    if not starts:
        return None, None
    a = starts[0]
    nxt = [pp for pp, _r in STARTS if pp > a]
    return a, (min(nxt) - 1) if nxt else None


def chapter_of(pp):
    """Which chapter opening a printed page falls after, if any."""
    prior = [(s, r) for s, r in STARTS if s <= pp]
    return max(prior)[1] if prior else None


def sources_rows():
    m = re.search(r"^sources:\n((?:  - .*\n?)+)", front_matter(), re.M)
    return re.findall(r'^  - text: "(.*)"$', m.group(1), re.M) if m else []


def cited_quote_pages():
    """Printed pages carrying a quoted 1894 passage and its citation together.

    body_sentences() cannot be used here: it splits on every period followed by a
    space, and '(1894, p. 236)' has one inside it, which cuts the citation away
    from the quote it belongs to. This split keeps 'p.' and 'pp.' from ending a
    sentence, and keeps the three dots of an ellipsis inside a quotation from
    ending one either; those are the only differences, and they are what makes the
    voice and coverage checks below able to see a citation at all.
    """
    out = set()
    for para in body().split("\n\n"):
        para = " ".join(para.split())
        for s in re.split(r"(?<=[.!?])(?<!p\.)(?<!\.\.)\s+", para):
            if re.search(r'"[^"]{12,}"', s):
                for m in re.finditer(r"\(\s*1894,\s*p{1,2}\.\s*([\d,\s]*?\d)\s*\)", s):
                    out.update(int(n) for n in re.findall(r"\d+", m.group(1)))
    return sorted(out)


def stated_ranges(row):
    """[(roman, first, last)] for the ranges one Sources row states.

    Paired by order of appearance: 'Chapter I, ... printed pp. 3 to 6, and
    chapter II, ... printed pp. 7 to 8' states two, and the non-greedy gap stops
    at the nearest range, which is the one that follows that chapter's name.
    """
    out, pos = [], 0
    while True:
        m = re.search(r"[Cc]hapter (" + ROMAN + r").{0,220}?printed pp\. (\d+) to (\d+)",
                      row[pos:], re.S)
        if not m:
            return out
        out.append((m.group(1), int(m.group(2)), int(m.group(3))))
        pos += m.end()


def sources():
    rows = sources_rows()
    check("the Sources block parses as rows", 11, len(rows),
          "sources_block() renders every one of them onto the page")

    # (1) every chapter range the block states, against the volume's own headings
    stated = {}
    for row in rows:
        for roman, a, b in stated_ranges(row):
            stated.setdefault(roman, []).append((a, b))
    for roman, ranges in sorted(stated.items()):
        ma, mb = measured_range(roman)
        check(f"chapter {roman} runs printed pp. {ma} to {mb}, the volume's own headings",
              ranges, [(ma, mb)],
              "the Sources block states the range; the heading on the next chapter's "
              "opening page sets the end")

    # (2) every other page a chapter row points at is inside a range that row
    # states, or is a chapter opening that row is describing as a boundary.
    for row in rows:
        ranges = stated_ranges(row)
        if not ranges:
            continue
        outside = []
        for n in (int(x) for x in re.findall(r"printed p\. (\d+)", row)):
            if not any(a <= n <= b for _r, a, b in ranges) and n not in {s for s, _r in STARTS}:
                outside.append(n)
        check(f"every 'printed p. N' in the row for "
              f"{', '.join(r for r, _a, _b in ranges)} is inside a range that row states",
              [], outside, row[:70] + "...")

    # (3) footnotes the block quotes with a page cite: the quote has to be on
    # the page it cites. check_quotes.py reads the body, not this block.
    block = "\n".join(rows)
    quoted = re.findall(r"'([^']{25,400})'[^'\n]{0,20}?\(1894, p\. (\d+)\)", block)
    check("the Sources block quotes four footnotes with a page cite", 4, len(quoted),
          "the two lecture footnotes, the compiler's review sentence, and the "
          "interview footnote in chapter XXXVI")
    for q, page in quoted:
        n = int(page)
        check(f"the Sources block's quote {q[:44]!r} is on printed p. {n}", 1,
              norm_count(q, page=n), "sources_block() renders it with that page cite")

    # (4) the claim that the volume's own contents pages carry the two lecture
    # titles, with the dates and the opening pages this article cites. Front
    # matter pages are printed page < 3; the index the quote checker builds
    # drops those lines as furniture, so this is read from the raw text.
    front = "\n".join(b for pp, b in RAW if pp < 3)
    for title, page, date in (("NEW YORK LECTURE", "145", "MAY 20"),
                              ("LONDON LECTURE", "198", "FEBRUARY")):
        hit = re.search(re.escape(title) + r".{0,400}?" + re.escape(page), front, re.S)
        check(f"the contents pages carry {title!r} with the opening page {page}", True,
              bool(hit), "the Sources block says the contents pages list both lectures by "
                         "title, with the opening pages this article cites")
        hit2 = re.search(re.escape(title) + r".{0,400}?" + re.escape(date), front, re.S)
        check(f"and {title!r} with the date {date} the Sources block cites", True, bool(hit2),
              "the dates the contents pages give, which are the dates the chapter footnotes give")

    # (5) the heading claims. Each is stated in the block as a reason the heading
    # had to be read off the print rather than taken from the text layer.
    p145 = RAW_BY_PAGE.get(145, "")
    for mis in ("EXPEEIMENTS", "WlTH", "HlGH"):
        check(f"the text layer of printed p. 145 sets {mis!r}", True, mis in p145,
              "the Sources block names the mis-settings as the reason the heading "
              "does not grep there")
    check("the chapter XXVI heading does not grep as one string on printed p. 145", 0,
          norm_count("EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY "
                     "AND THEIR APPLICATION TO METHODS OF ARTIFICIAL ILLUMINATION",
                     page=145),
          "so the block quotes it from the print of scan file 163")
    p198 = RAW_BY_PAGE.get(198, "")
    for mis in ("CHAPTEE", "HlGH"):
        check(f"the text layer of printed p. 198 sets {mis!r}", True, mis in p198,
              "the Sources block says exactly this, and it is what the page holds")
    p424 = RAW_BY_PAGE.get(424, "")
    order = [p424.find(t) for t in ("THERMO-MAGNETIC", "XXXVI.",
                                    "MOTORS AND PYRO-MAGNETIC GENERATORS.")]
    check("printed p. 424 interleaves the chapter number into its own heading, "
          "in the order the block states", True,
          all(i >= 0 for i in order) and order == sorted(order),
          "'THERMO-MAGNETIC' then 'XXXVI.' then 'MOTORS AND PYRO-MAGNETIC GENERATORS.'")

    # (6) this site's own pages named by title in the block. A wrong title is a
    # dead reference: the reader cannot find the page it describes.
    named = re.findall(r"(?<![A-Za-z])'([^']{10,120})'", "\n".join(
        r for r in rows if "this site" in r and "article reads" in r))
    live_titles = {page_title(s): s for s in ("magnetic-generator-scam.html",
                                              "tesla-magnetic-generator-worth-it.html",
                                              "free-electricity-from-magnets.html")}
    check("the Sources block names three of this site's pages by title", 3, len(named),
          "the three commercial pages the article reads")
    for t in named:
        check(f"a live page's <title> is exactly {t!r}", True, t in live_titles,
              f"the live titles are: {sorted(live_titles)}")

    # (7) the paragraph that says whose words the article is quoting has to name
    # every chapter the article actually quotes from, and no chapter it does not.
    # (8) every page the body quotes from is covered by the Sources block: inside
    # a range it states, or named in it (the volume's index is not a chapter).
    quote_pages = cited_quote_pages()
    check("the body quotes 1894 passages on 16 printed pages", 16, len(quote_pages),
          "the same 16 pages check_quotes.py reports the 27 fragments on")
    index_named = [int(x)
                   for grp in re.findall(r"printed pp\. (\d+) and (\d+)", block) for x in grp]
    head = re.search(r"## What He Did Claim, and in Whose Voice\n+(.*?)(?=\n##|\Z)",
                     body(), re.S)
    para = next((p for p in (head.group(1) if head else "").split("\n\n")
                 if "chapter" in p.lower()), "")
    check("the voice paragraph is present", True, bool(para),
          "the paragraph under 'What He Did Claim, and in Whose Voice'")
    if para:
        named_ch = set()
        for m in re.finditer(r"[Cc]hapters?\b", para):
            named_ch.update(re.findall(r"\b(" + ROMAN + r")\b", para[m.end():m.end() + 60]))
        want = sorted({chapter_of(pp) for pp in quote_pages
                       if pp not in index_named and chapter_of(pp)})
        check("the voice paragraph names every chapter the body quotes from", want,
              sorted(named_ch),
              f"the body quotes from printed pp. {quote_pages}; the index pages "
              f"{index_named} are the volume's index, not a chapter")

    # (9) the voice paragraph names a person, and says where he calls himself the
    # compiler. Both are in the volume: the title page and printed p. 6.
    front_all = "\n".join(b for pp, b in RAW if pp < 3)
    title_page = next((b for pp, b in RAW if pp == -9), "")
    tokens = [t in title_page.upper() for t in ("THOMAS", "COMMERFORD", "MARTIN", "EDITOR")]
    check("the title page carries the editor's name, as tokens, because its display "
          "type interleaves it", [True, True, True, True], tokens,
          "the volume's editor, named on its own title page; the text layer sets "
          "'THOMAS Editor THE ELKCTHICAL COMMERFORD ENGiNEtR ; ... MARTIN', so the "
          "name is not one string there and the check reads the four tokens")
    check("the copyright page is his", True, "T. C. MARTIN" in front_all,
          "Entered according to Act of Congress ... by T. C. MARTIN")
    check("printed p. 6 is where he calls himself the compiler of this volume", 1,
          norm_count("led the compiler of this volume", page=6),
          "who calls himself its compiler on printed p. 6")

    covered = [rng for rngs in stated.values() for rng in rngs]
    uncovered = [pp for pp in quote_pages
                 if not any(a <= pp <= b for a, b in covered) and pp not in index_named]
    check("every page the body quotes from is covered by the Sources block", [], uncovered,
          "the block states chapter ranges and names the index pages directly")


def body_sentences():
    """Body sentences, whole. A quote is checked in the sentence that uses it, so
    that a fragment quoted from a page in one sentence is not credited to another
    sentence in the same paragraph."""
    out = []
    for para in body().split("\n\n"):
        para = " ".join(para.split())
        if para:
            out.extend(s.strip() for s in re.split(r"(?<=[.!?])\s+", para) if s.strip())
    return out


# Sentences that report what another page on this site says, and the page each
# names. Matched on the sentence's subject, not on the whole paragraph.
SITE_SUBJECTS = {
    "tesla-magnetic-generator-worth-it.html": (
        "review of whether one is worth buying",
        "review of what a Tesla magnetic generator is",
    ),
    "free-electricity-from-magnets.html": ("free-electricity page",),
    "magnetic-generator-scam.html": ("scam page",),
}

# Prose pointers - 'the site's X article' - with no link in the draft, and the
# page each one can only mean.
PROSE_POINTERS = {
    "the site's article on one-wire power": "tesla-one-wire-power.html",
    "the site's rotating-magnetic-field article": "rotating-magnetic-field-1888.html",
    "the site's cold-flame article": "tesla-cold-flame.html",
    "the site's article on Tesla's high-frequency": "tesla-high-frequency-massage.html",
    "the site's list of nine inventions that did not catch on": "tesla-weird-inventions-1894.html",
}


def quotes():
    text = DRAFT.read_text(encoding="utf-8")
    body_text = body()
    found = {}

    # (1) The sentences that report what this site's commercial pages claim.
    for sent in body_sentences():
        for page, subjects in SITE_SUBJECTS.items():
            if not any(s in sent for s in subjects):
                continue
            for frag in re.findall(r"'([^']{4,200})'", sent):
                found.setdefault(page, []).append(frag)
    for page, want in EXPECTED_COMMERCIAL.items():
        got = found.get(page, [])
        check(f"the body attributes to {page} exactly the fragments this check knows about",
              sorted(want), sorted(got),
              "the sentence that names that page, and the fragments inside it")
        t = page_text(page).lower()
        for frag in want:
            check(f"{page} carries {frag!r}", True, frag.lower() in t,
                  "4.1: a series page may report a live page's claim in that page's own words")
    check("commercial-page quotes checked", sum(len(v) for v in EXPECTED_COMMERCIAL.values()),
          sum(len(v) for v in found.values()),
          "three sentences name three live pages and quote four fragments")

    # The un-quoted half of the same claim: the review page does attribute the
    # device to a patent number, and that number is 0 in the book (numbers()).
    worth = page_text("tesla-magnetic-generator-worth-it.html")
    check("the review page states a patent number and a grant year", True,
          "Patent No. 512,340" in worth and "granted in 1894" in worth,
          "attributes the device to a Tesla patent granted in 1894")

    # (2) The CTA is a product sentence, so it may only say what a live page says.
    cta = re.search(r'cta:\s*\n\s*text: "([^"]+)"', text).group(1)
    banned = sorted({m.group(0).lower() for m in re.finditer(
        r"free energy|perpetual|infinite|guarantee|zero emission|clean", cta, re.I)})
    check("CTA adds no capability claim of its own", "none", banned and ", ".join(banned) or "none",
          "4.1: this series adds no new free-energy or perpetual-motion assertion")
    plans = page_text("magnetic-generator-plans-review.html").lower()
    for frag in ("parts list", "output"):
        check(f"magnetic-generator-plans-review.html carries {frag!r}", True, frag in plans,
              "the CTA says the plans come with a parts list and a straight answer about output")
    for frag in ("shed", "workshop", "off-grid"):
        hits = sorted(p.name for p in SITE.glob("*.html") if frag in page_text(p.name).lower())
        check(f"'{frag}' is a use case this site already writes about", True, bool(hits),
              f"{len(hits)} live pages, first few: {hits[:6]}")

    # (3) Cross-page claims about this series' own pages.
    a08 = page_text("tesla-weird-inventions-1894.html")
    check("article 08's live page prints the count this page says it prints", True,
          "four hits on three printed pages" in a08,
          "The second number is the one this site's own article on nine lost inventions prints today")
    check("article 08's live page carries the footnote this page links it for", True,
          "400 to 500" in a08, "carries the same footnote for a different purpose")
    reg = A08_REGISTER.read_text(encoding="utf-8", errors="replace")
    lines = [ln for ln in reg.splitlines()
             if re.search(r"magnetic gener", ln) and "4" in ln and "5" in ln]
    check("article 08's own register records 4 and 5 side by side", True, bool(lines),
          "both counts are in that article's own quote register")

    # (4) Prose pointers must name pages that exist.
    for phrase, page in PROSE_POINTERS.items():
        if phrase in body_text:
            check(f"prose pointer {phrase!r} names a page that exists", True,
                  (SITE / page).exists(), f"-> {page}")

    # (5) Every .html link in the body resolves on disk, except the one pending
    # link this page's own front matter names with its owner.
    for slug in sorted(set(re.findall(r"\]\(([^)]+\.html)\)", body_text))):
        if slug in PENDING_LINKS:
            print(f"PENDING  link target {slug} does not exist yet; owned by {PENDING_LINKS[slug]}")
            continue
        check(f"link target {slug} exists on disk", True, (SITE / slug).exists())
    for slug, owner in PENDING_LINKS.items():
        print(f"         the one allowed dead link is {slug}, owned by {owner}, and it is "
              f"named in the draft's LINKS block and in this page's index.json row")

    # (6) The register the front matter says the draft was written from.
    head = REGISTER.read_text(encoding="utf-8", errors="replace")[:6000]
    m = re.search(r"Verified:\s*(\d+)\s*quotes.*?Rejected[^.]*?(\d+)\.", head, re.S)
    check("register header reports 72 verified / 26 rejected as the front matter says",
          ("72", "26"), (m.group(1), m.group(2)) if m else ("?", "?"),
          "which is the accepted output of feature-007/t0")

    # (7) The draft's own rule: a quote that is not in the register is not in
    # the draft. Checked the other way this time - every double-quoted 1894
    # passage in the body has to be a fragment of a pinned quote.
    pinned = set()
    for m in re.finditer(r'^> "([^"]+)"', REGISTER.read_text(encoding="utf-8"), re.M):
        for frag in [f.strip().lower() for f in m.group(1).split("...")]:
            if len(frag) >= 12:
                pinned.add(frag)
    unpinned = []
    for para in body_text.split("\n\n"):
        for q in re.findall(r'"([^"]{12,})"', " ".join(para.split())):
            for frag in [f.strip().lower() for f in q.split(" ... ")]:
                if len(frag) < 12:
                    continue
                if not any(frag in p or p in frag for p in pinned):
                    unpinned.append(frag[:70])
    check("every quoted 1894 passage in the body is a fragment of a pinned quote", [], unpinned,
          "quotes.md: 'a quote that is not here does not go in the draft'")


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    if only not in ("--quotes", "--sources"):
        numbers()
    if only not in ("--numbers", "--sources"):
        quotes()
    if only not in ("--numbers", "--quotes"):
        sources()
    passed, total = sum(rows), len(rows)
    print(f"\n{passed}/{total} checks pass")
    sys.exit(0 if passed == total else 1)
