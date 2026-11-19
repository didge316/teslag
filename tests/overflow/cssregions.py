#!/usr/bin/env python3
"""The two regions item 7 added to css/styles-custom.css, in one place.

gate.py and inert-at-100.py both need the same thing: the stylesheet as it was
BEFORE this change, derived by cutting the regions the change added. Duplicating
that derivation in two scripts is how one of them silently starts measuring the
change against itself, so it lives here and both import it.

The cut is pinned to text, not line numbers, and refuses rather than guessing:
if a marker has been edited away, before_css() exits with instructions, because a
"before" stylesheet that quietly failed to lose the change makes every gate
result below it meaningless.

Region 1 is body's overflow-wrap safety net plus the table carve-out. The prose
rule above it (`article p, article li, article code`) predates this change and is
untouched by it, so it is not in the cut. Region 2 is the large-text block at the
end of the file - which by now also carries the navbar-drawer media query, because
that fix belongs to the same diff and the same reasoning about being inert at
100% applies to it (below 992px it changes drawer link heights by design; above
992px it is inert).
"""
import os
import sys

CSS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "..", "css", "styles-custom.css"))

CSS_URL_PART = "/css/styles-custom.css"

CUTS = [
    ("/* Item 7's safety net, on body",
     "/* ---------------------------------------------------------------------------\n   Mobile sticky offer bar"),
    ("/* ==========================================================================\n   Large text",
     None),  # None -> to end of file
]


def before_css(css=None):
    """The stylesheet with item 7's regions removed. Exits if a boundary moved."""
    text = open(css or CSS, encoding="utf-8").read()
    for start, end in CUTS:
        i = text.find(start)
        if i < 0:
            sys.exit(f"marker vanished from {css or CSS}: {start[:40]!r}\n"
                     "The pre-item-7 stylesheet can only be derived while the region "
                     "boundaries are findable; re-derive them by hand and update CUTS "
                     "in tests/overflow/cssregions.py.")
        j = len(text) if end is None else text.find(end, i)
        if end is not None and j < 0:
            sys.exit(f"end marker vanished from {css or CSS}: {end[:40]!r}")
        text = text[:i] + text[j + len(end):] if end is not None else text[:i]
    if "Large text" in text or "overflow-wrap: break-word" in text:
        print("NB: item-7 text still present after cutting; check CUTS in cssregions.py.")
    return text
