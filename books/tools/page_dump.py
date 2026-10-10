#!/usr/bin/env python3
"""Print the OCR text of a range of PRINTED pages of the 1894 edition.

SERIES-PLAN-1894.md §8 step 1-2: read the chapter, then re-grep every quote.
grep_quote.py pins a known quote; this tool shows the surrounding page so a
writer can find quotes in the first place. Same page rule as everywhere else:

    printed page = scan file page - 18        (§0 non-negotiable 1)

Usage
    page_dump.py 27            # one printed page
    page_dump.py 9-14          # a range
    page_dump.py 8 --grep pencil   # only lines matching a pattern, with context
"""

import argparse
import re
import sys
from pathlib import Path

BOOKS = Path(__file__).resolve().parent.parent
DEFAULT_TXT = BOOKS / "extracted" / "tesla-1894-plain.txt"
PAGE_MARKER = re.compile(r"<+ *page-(\d+) *>+")
PAGE_OFFSET = 18


def pages(text):
    """scan page number -> text, from the page-marker file."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = PAGE_MARKER.match(line.strip())
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = int(m.group(1)), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("range", help="printed page or start-end, e.g. 27 or 9-14")
    ap.add_argument("--txt", default=str(DEFAULT_TXT))
    ap.add_argument("--grep", default="", help="show only matching lines + context")
    ap.add_argument("--context", type=int, default=2)
    args = ap.parse_args()

    if "-" in args.range:
        a, b = args.range.split("-", 1)
    else:
        a = b = args.range
    lo, hi = int(a), int(b)
    if hi < lo or hi - lo > 40:
        sys.exit("bad range (max 40 printed pages)")

    src = pages(Path(args.txt).read_text(encoding="utf-8", errors="ignore"))
    printed = {p - PAGE_OFFSET: t for p, t in src.items()}
    hit = False
    for p in range(lo, hi + 1):
        if p not in printed:
            print(f"--- printed p. {p}: no text layer (scan file {p + PAGE_OFFSET}) ---")
            continue
        lines = printed[p].splitlines()
        print(f"\n===== printed p. {p} (scan file {p + PAGE_OFFSET}) =====")
        if not args.grep:
            print("\n".join(lines))
            hit = True
            continue
        pat = re.compile(args.grep, re.I)
        for i, ln in enumerate(lines):
            if pat.search(ln):
                lo2, hi2 = max(0, i - args.context), min(len(lines), i + args.context + 1)
                print("\n".join(lines[lo2:hi2]))
                print("  ---")
                hit = True
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main())
