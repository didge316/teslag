#!/usr/bin/env python3
"""Test candidate quote fragments through the exact matcher check_quotes.py uses.

This is the gate article 12 will be judged by (books/tools/check_quotes.py in
feature-006/t7), run fragment by fragment before the draft is written, so a
fragment that will not verify is caught here and not in the gate. It imports
check_quotes.fragments() and check_quotes.locate() and builds the same index,
including the whitespace-free one that lets an OCR spacing defect pass.

Usage: python3 frag_test.py "fragment" PAGE [-PAGE]
       python3 frag_test.py --file candidates.txt   # one "fragment<TAB>pages" per line
Exit 0 if every fragment matches exact or nospace, 1 otherwise.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "books" / "tools"
sys.path.insert(0, str(TOOLS))
import check_quotes as CQ  # noqa: E402
import grep_quote as GQ  # noqa: E402

TXT = TOOLS.parent / "extracted" / "tesla-1894-plain.txt"


def main():
    args = sys.argv[1:]
    if args and args[0] == "--file":
        items = []
        for line in Path(args[1]).read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            frag, pages = line.split("\t")
            lo, _, hi = pages.partition("-")
            items.append((frag.strip(), int(lo), int(hi or lo)))
    else:
        frag = args[0]
        lo, _, hi = args[1].partition("-")
        items = [(frag, int(lo), int(hi or lo))]

    pages = GQ.load_pages(TXT)
    index = tuple(GQ.build_index(pages)) + tuple(CQ.build_nospace(pages))
    bad = 0
    for frag, lo, hi in items:
        for f in CQ.fragments(frag):
            hits, how = CQ.locate(index, f)
            pps = sorted({h["printed_page"] for h in hits})
            on_page = any(lo <= p <= hi for p in pps)
            if how in ("exact", "nospace") and on_page:
                print(f"OK   {how:8s} p.{pps} :: {f[:70]}")
            else:
                bad += 1
                ratio = hits[0]["ratio"] if hits else None
                print(f"FAIL {str(how):8s} pages={pps[:6]} ratio={ratio} "
                      f"want p.{lo}-{hi} :: {f[:70]}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
