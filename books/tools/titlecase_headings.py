#!/usr/bin/env python3
"""Title-case the <h2>/<h3> headings of the 1894 series pages.

The site's standing heading style is title case (APA-ish): every word of four
letters or more is capitalised, as are verbs and pronouns of any length; only
articles, coordinating conjunctions and prepositions of three letters or fewer
stay lowercase, and never in the first or last position.

<h1> is left alone -- it is already title case and is mirrored into <title>,
og:title and twitter:title, which were tuned to the 60-char limit in Deploy 2.

Usage:
  titlecase_headings.py [--check] [file.html ...]
    no args  -> the 1894 series pages in ../website
    --check  -> report only, exit 1 if any heading is not title case
"""
import argparse
import html
import re
import sys
from pathlib import Path

WEBSITE = Path(__file__).resolve().parents[2] / "website"

# Words that stay lowercase when they are neither first nor last.
LOWER = {
    # articles
    "a", "an", "the",
    # coordinating conjunctions
    "and", "or", "but", "nor", "for", "yet", "so",
    # prepositions of three letters or fewer
    "at", "by", "in", "of", "on", "to", "up", "per", "via", "vs", "vs.",
}

# Capitalise the word after these, since a colon or dash starts a new unit.
FORCE_CAP_AFTER = (":", "-", "--", "\u2014", "\u2013")

# A quotation inside a heading is the source's wording, not ours, so its case is
# left alone. An opening quote only opens a span when it is not stuck to a word,
# which is what keeps Tesla's and Don't from reading as quotations, and the span
# has to close at whitespace, sentence punctuation or the end of the heading.
QUOTE_SPAN = re.compile(
    r'(?<![\w])(["\u201c])[^"\u201c]{1,300}?["\u201d](?=[\s).,;:!?]|$)'
    r"|(?<![\w])(['\u2018])[^'\u2019\s][^'\u2019]{0,300}?['\u2019](?=[\s).,;:!?]|$)"
)


def _split_token(tok: str):
    """Return (leading punctuation, core word, trailing punctuation).

    The trailing run is searched for in what the leading run did not take, so a
    token that is nothing but punctuation (a lone em dash) is not counted twice.
    """
    lead = re.match(r'^[^\w\'"\u2018\u201c]*', tok).group(0)
    rest = tok[len(lead):]
    trail = re.search(r'[^\w\'"\u2018\u201c]*$', rest).group(0)
    core = rest[: len(rest) - len(trail)] if trail else rest
    return lead, core, trail


def _cap(word: str) -> str:
    """Capitalise the first letter, leaving acronyms, years and initials alone."""
    if not word:
        return word
    if re.match(r"^(?:\d|[A-Z]{2,}|[A-Z]\.)", word):  # 1893, AC, N. Y.
        return word
    if word.lower() in ("ac", "dc", "og", "seo", "ii", "iii", "iv"):
        return word.upper()
    if word[0].isalpha():
        return word[0].upper() + word[1:]
    return word


def _quoted_spans(text: str):
    """Character ranges in this heading that are quotations, not our wording."""
    return [(m.start(), m.end()) for m in QUOTE_SPAN.finditer(text)]


def titlecase(text: str) -> str:
    text = html.unescape(text)
    spans = _quoted_spans(text)
    toks = list(re.finditer(r"\S+", text))
    out = []
    prev = ""
    for i, m in enumerate(toks):
        tok = m.group(0)
        if any(s < m.end() and m.start() < e for s, e in spans):
            # a quoted source term: verbatim from the print, case included
            out.append(tok)
            prev = tok
            continue
        lead, core, trail = _split_token(tok)
        is_last = i == len(toks) - 1
        force_cap = (
            is_last
            or i == 0
            or any(prev.endswith(f) for f in FORCE_CAP_AFTER)
        )
        # A hyphenated compound is title-cased element by element.
        parts = re.split(r"(-)", core)
        cored = ""
        for j, p in enumerate(parts):
            if p == "-":
                cored += p
                continue
            if not p:
                cored += p
                continue
            # The first element follows the normal rule; later elements of a
            # compound are never "minor" words on their own.
            minor_first = j == 0
            if not force_cap and minor_first and p.lower().rstrip(".,;:") in LOWER:
                cored += p.lower()
            else:
                cored += _cap(p)
        out.append(lead + cored + trail)
        prev = cored + trail
    return " ".join(out)


HEAD_RE = re.compile(r"(<h([23])\b[^>]*>)(.*?)(</h\2>)", re.S)

# The FAQPage JSON-LD question names must match the visible <h3> text, so they
# move with the headings. Only Question names appear inside a FAQPage block.
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
NAME_RE = re.compile(r'("name"\s*:\s*")((?:[^"\\]|\\.)*)(")')


def check_headings(path: Path):
    """Headings on this page that are not title case, without touching the file.

    Returns [(kind, current, expected), ...] where kind is "2", "3" or "faq".
    qa_page.py's heading-case gate calls this, so --check mode and the gate are
    the same code and cannot drift apart.
    """
    return process(path, True)


def process(path: Path, check: bool):
    src = path.read_text(encoding="utf-8")
    changes = []

    def sub(m):
        open_tag, level, inner, close = m.groups()
        if "<" in inner:  # headings with markup inside are left to a human
            return m.group(0)
        want = titlecase(html.unescape(inner))
        if want == inner:
            return m.group(0)
        changes.append((level, inner, want))
        return open_tag + html.escape(want, quote=False) + close

    new = HEAD_RE.sub(sub, src)

    def sub_ld(m):
        open_tag, body, close = m.groups()
        if '"FAQPage"' not in body:
            return m.group(0)

        def sub_name(mn):
            val = mn.group(2).replace('\\"', '"').replace("\\'", "'")
            want = titlecase(val)
            if want == val:
                return mn.group(0)
            changes.append(("faq", val, want))
            want = want.replace('"', '\\"')
            return mn.group(1) + want + mn.group(3)

        return open_tag + NAME_RE.sub(sub_name, body) + close

    new = LD_RE.sub(sub_ld, new)
    if not check and new != src:
        path.write_text(new, encoding="utf-8")
    return changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()

    if args.files:
        files = [Path(f) for f in args.files]
    else:
        files = sorted(
            p for p in WEBSITE.glob("*.html")
            if "1894 File \u00b7 No" in p.read_text(encoding="utf-8", errors="replace")
        )

    bad = 0
    for f in files:
        changes = process(f, args.check)
        if not changes:
            continue
        bad += len(changes)
        print(f"{f.name}: {len(changes)} heading(s)")
        for level, old, new in changes:
            tag = "h2   " if level == "2" else "h3   " if level == "3" else "schema"
            print(f"  {tag}  - {old}")
            print(f"         + {new}")
    verb = "not title case" if args.check else "retitled"
    print(f"\n{len(files)} page(s) scanned, {bad} heading(s) {verb}")
    return 1 if (args.check and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
