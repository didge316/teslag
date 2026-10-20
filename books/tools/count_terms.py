#!/usr/bin/env python3
"""Re-run the volume word counts a draft asserts, whole-word and substring.

Every "X occurs N times in the volume" claim in a series draft must be re-run
before the draft is committed — a count is its regex, and one such claim in the
05 draft was wrong when it was first written down. For each term this prints:
whole-word count, substring count, and the printed pages of the substring hits.

This is also the tool behind the word-search data page (PLAN-1894.md T2): the
counts that page states must come from this script's output, not from
SERIES-PLAN-1894.md Appendix D.

    python3 books/tools/count_terms.py "free energy" "perpetual" "magnetic generator"
"""
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
import grep_quote as GQ  # noqa: E402

pages = GQ.load_pages(GQ.DEFAULT_TXT)
index = GQ.build_index(pages)          # (ntext, spans, words, vocab, ...)
ntext, spans = index[0], index[1]

for term in sys.argv[1:]:
    n = GQ.normalise(term)
    sub = [m for m in re.finditer(re.escape(n), ntext)]
    whole = [m for m in re.finditer(r"(?<![\w])" + re.escape(n) + r"(?![\w])", ntext)]
    pps_sub = sorted({pp for m in sub
                      for _, pp in GQ.pages_for(spans, m.start(), m.end())})
    print(f"{term!r}: whole-word={len(whole)} substring={len(sub)} pages={pps_sub}")
