# Sprint contract — finish *The 1894 File* flagship series

**Sprint:** 2026-10-10 → series complete (13 pages: 12 articles + hub)
**Spec:** `SERIES-PLAN-1894.md` (unchanged, authoritative) · **PRD:** `books/specs/prd.md`
**Branch:** work repo `feature/1894-series-flagship`; `website/` stays on `main`, never pushed.

## In

Produce, to the §8 runbook and the §12 gates, in this order:
**07 → 01 → 02 → 04 → 05 → 06 → 08 → 10 → 12**, then the hub `tesla-1894.html`.
Plus: `shot_qa.py` + screenshot review for every series page including the already-produced
03, 09, 11; OG images for all 13; the §5.2 backlink pass on the 8 named existing pages; the
§16.3 linkable assets (`tesla-1894-plates`, `tesla-1894-word-search`,
`tesla-1894-part1-text`, public `tesla1894` repo) and 20 outreach emails drafted; one
tooling fix so `qa_page.py` fails any page with a dead relative link.

## Out

Tier 2–6 backlog (§10) and S7+ cadence. Any `git push` in `website/` (D6 — pushing deploys;
owner sign-off only). Shared-shell work: the three legacy nav titles with em dashes, the
~280 KB shell image weight, CTA above the mobile fold. Re-running OCR / figure extraction /
quote harvesting. Rewriting `SERIES-PLAN-1894.md`. New product claims.

## How we know it is done

- `python3 books/tools/qa_page.py --all-series` exits 0 across 13 pages.
- The new dead-relative-link check reports zero dead links.
- `shot_qa.py` measurable gates pass at 375/768/1280 for all 13, and the screenshots were
  reviewed with vision (figures in column, captions legible, nav intact, nothing undecoded).
- `new_content/1894-series/index.json`: 13 entries, `figures[].verified: true`,
  `committed: true`, `deployed: false`.
- Both repos clean and committed per session; no push anywhere.

## Standing rules that override convenience

Printed page = scan file − 18. Quotes re-grepped, never recalled. Figure numbers read off
the printed page, never the extractor filename. No em/en dashes, curly quotes or ellipses in
series prose. Commit every session, push only on named owner sign-off.

## Decisions taken in this sprint (owner may reverse)

O1 keep *The 1894 File* · O2 = option B (article 10 kept, published after 03/01/07) ·
O3 keep the shell's scarcity widget everywhere · hub ships last so its 12 cards are real.
