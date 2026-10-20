#!/usr/bin/env python3
"""Add the section 5.2 backlink block to the eight legacy pages it names.

SERIES-PLAN-1894.md section 5.2 ends with: "Backlink pass (week 6): add a `Sources &
further reading` line with 1-2 series links to these 8 existing pages". books/PLAN-1894.md
T5 turns that into a task with hard rules: one named commit per page in the website repo,
no em dash, en dash, curly quote or ellipsis, and nothing else on the page changes.

This tool does the insertion so that "nothing else changes" is a property of the tool
rather than of whoever is editing, and so a reverted page can be redone identically.

What it does:
  - inserts one H2 and one paragraph immediately before the closing </article> tag
  - the H2 is title case, because titlecase_headings.py would insist on it
  - the paragraph is plain ASCII, and the tool refuses to write anything else
  - a marker comment names the tool and the date, so the block is findable and the
    insertion is idempotent: running it twice does nothing
  - prints what changed: bytes, links added, H2 count before and after

What it does not do: it does not touch index.json, it does not commit, and it cannot
check the visual half of T5's criteria ("still renders clean at three widths"), which is
T7. Run books/tools/link_map.py afterwards to see whether section 5.2's map closed.

Usage:
  python3 books/tools/backlink_pass.py --page magnetic-generator-scam
  python3 books/tools/backlink_pass.py --all
  python3 books/tools/backlink_pass.py --check          # report only, writes nothing
"""
import argparse
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[2] / "website"
MARK = "1894-backlinks-2026-10-20"

# legacy page -> (target stem, exact H1 of the target, one sentence of plain English that
# says why the two pages belong together). Sentences are the deliverable; the links are
# only good if the sentence is true of both pages.
BLOCKS = {
    "nikola-tesla-inventor-extraordinaire": [
        ("rotating-magnetic-field-1888", "The Paper Tesla Scribbled in Pencil: How AC Won",
         "the 1888 paper that made the alternating current system work, and the efficiency "
         "figures that were measured in public between 1888 and 1893"),
        ("tesla-free-energy-what-he-said", "What Tesla Actually Wrote About Free Energy",
         "the 1894 book that collected his lectures, read page by page, and what a word "
         "search of that exact printing returns"),
    ],
    "magnetic-generator-scam": [
        ("tesla-free-energy-what-he-said", "What Tesla Actually Wrote About Free Energy",
         "we searched our copy of Tesla's own 1894 book for the phrases this market sells, "
         "and printed the counts"),
        ("tesla-weird-inventions-1894", "9 Tesla Inventions From 1894 That Never Caught On",
         "the only machine in that book with 'magnetic generator' in its name is a heat "
         "engine with a flame under it"),
    ],
    "magnetic-dynamo-generator": [
        ("rotating-magnetic-field-1888", "The Paper Tesla Scribbled in Pencil: How AC Won",
         "where the rotating field that a generator like this depends on was demonstrated, "
         "and how the machines that used it were tested"),
        ("tesla-high-frequency-alternator", "30,000 Alternations a Second: Tesla's Lost Generator",
         "a generator whose poles and frequency had to be built to a number, and why "
         "building one of them was so hard that the 1894 book prints the difficulties"),
    ],
    "perpetual-motion-generator": [
        ("tesla-earthquake-machine", "Tesla's Earthquake Machine: What the 1893 Record Says",
         "a machine that ran at a constant period by resonance, which is why it kept good "
         "time and why it was never a source of energy"),
        ("tesla-free-energy-what-he-said", "What Tesla Actually Wrote About Free Energy",
         "what Tesla actually put in print about drawing energy from the environment, in the "
         "1894 first edition, with the page numbers"),
    ],
    "magnet-motor": [
        ("tesla-weird-inventions-1894", "9 Tesla Inventions From 1894 That Never Caught On",
         "the only 'magnetic generator' printed in Tesla's own 1894 book is a heat engine, "
         "and it is one of nine machines that other people did not go on building"),
        ("tesla-free-energy-what-he-said", "What Tesla Actually Wrote About Free Energy",
         "the phrase 'free energy' does not appear in that book at all, and the search that "
         "shows it is printed with its counts"),
    ],
    "7-interesting-facts-about-magnets": [
        ("rotating-magnetic-field-1888", "The Paper Tesla Scribbled in Pencil: How AC Won",
         "the rotating magnetic field, which is the trick that lets an alternating current "
         "motor turn without any contact to the rotor"),
        ("tesla-cold-flame", "The Flame That Doesn't Burn: Tesla's Cold Fire",
         "what a brush discharge is, and the one place in the 1894 book where a magnet held "
         "some way off changes what a glowing bulb does"),
    ],
    "electricity-using-magnets": [
        ("tesla-free-energy-what-he-said", "What Tesla Actually Wrote About Free Energy",
         "does Tesla's own book ever describe generating electricity with magnets? We "
         "searched the text of our copy and printed what came back"),
        ("tesla-weird-inventions-1894", "9 Tesla Inventions From 1894 That Never Caught On",
         "the one machine in that book whose name claims magnetism makes electricity runs on "
         "heat, with a spirit lamp under it"),
    ],
    "build-a-magnetic-generator": [
        ("rotating-magnetic-field-1888", "The Paper Tesla Scribbled in Pencil: How AC Won",
         "how long it took a real alternating current machine to reach the nineties, with "
         "the tests and the dates"),
        ("tesla-high-frequency-alternator", "30,000 Alternations a Second: Tesla's Lost Generator",
         "a machine built to a frequency rather than to a weight of copper, and the limits "
         "that stopped it"),
    ],
}

H2 = '<h2 class="fw-bolder mb-1 pt-5">Sources and Further Reading</h2>'


def build_page_links(items):
    parts = [f'<p class="fs-5 mb-4">This site has two longer pieces of evidence for the '
             f'claims on this page, both built from one 1894 printing and both cited to '
             f'printed pages of it.</p>']
    for stem, title, why in items:
        parts.append(f'<p class="fs-5 mb-4"><a href="/{stem}">{title}</a>: {why}.</p>')
    return "\n                            ".join(parts)


def block(stem):
    return (f'<!-- {MARK}: books/tools/backlink_pass.py, the backlink pass named in the '
            f'plan at section 5.2, task T5 of books/PLAN-1894.md -->\n'
            f'                    {H2}\n'
            f'                    {build_page_links(BLOCKS[stem])}\n                ')


def check_ascii(text):
    bad = sorted({c for c in text if ord(c) > 127})
    if bad:
        raise SystemExit(f"refusing to write non-ASCII: {[hex(ord(c)) for c in bad]}")


def run(stem, write):
    p = WEB / f"{stem}.html"
    if not p.exists():
        print(f"  [skip] {stem}: no such page")
        return 1
    h = p.read_text(encoding="utf-8", errors="ignore")
    art = re.search(r"<article\b.*?</article>", h, re.S)
    if not art:
        print(f"  [skip] {stem}: no <article> element")
        return 1
    if MARK in h:
        print(f"  [ok ] {stem}: block already present, nothing written")
        return 0
    ins = block(stem)
    check_ascii(ins)
    prefix = h[:art.end()]
    i = prefix.rfind("</article>")
    new = prefix[:i] + ins + prefix[i:] + h[art.end():]
    before_h2 = len(re.findall(r"<h2\b", art.group(0)))
    after_h2 = len(re.findall(r"<h2\b", re.search(r"<article\b.*?</article>", new, re.S).group(0)))
    added = [f"/{s}" for s, _, _ in BLOCKS[stem]]
    if write:
        p.write_text(new, encoding="utf-8")
    print(f"  [{'write' if write else 'check'}] {stem}: {p.stat().st_size} -> {len(new.encode())} bytes, "
          f"H2 in article {before_h2} -> {after_h2}, links added {added}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    targets = [a.page] if a.page else (list(BLOCKS) if (a.all or a.check) else [])
    if not targets:
        raise SystemExit(__doc__)
    rc = 0
    for t in targets:
        if t not in BLOCKS:
            print(f"  [skip] {t}: not one of the eight pages section 5.2 names")
            rc = 1
            continue
        rc |= run(t, write=not a.check)
    return rc


if __name__ == "__main__":
    sys.exit(main())
