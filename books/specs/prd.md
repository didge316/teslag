# PRD — Finish *The 1894 File* flagship series

**Goal:** finish every unfinished production task in `SERIES-PLAN-1894.md` §8–§12 for the
12 flagship articles + hub, so the whole series sits in `website/` passing its own QA
gates, committed and not pushed.
**Spec of record:** `SERIES-PLAN-1894.md` (this PRD bounds it; it does not restate it).
**Repos:** work repo `/home/matt/projects/other/tesla-generator` (branch
`feature/1894-series-flagship`), deploy repo `website/` (stays on `main`, never pushed).

## 1. State at DEFINE (verified, not assumed)

Produced and wired in `website/`: **03** `tesla-earthquake-machine.html` (24/24 gates),
**09** `tesla-worlds-fair-1893.html` (23/23), **11** `tesla-high-frequency-alternator.html`
(24/24). Hub **drafted only** (`new_content/1894-series/00-hub/article.md`, not rendered).
Tooling exists and works: `contact_sheet.py`, `grep_quote.py`, `make_article.py`,
`qa_page.py`, `shot_qa.py`. Figure QC done: `manifest_qc.csv`, 203 rows, 198 usable.
Known open defect: **09 links to `rotating-magnetic-field-1888.html` (07), which does not
exist** — the only dead relative link in the series. *(Closed since 2026-10-11: 07 is live, and
`qa_page.py` now resolves root-absolute links too, so a link like this fails the page instead of
being remembered.)* `shot_qa.py` has never been run on
09 or 11.

## 2. In scope (the contract)

1. The nine remaining flagship articles, in the order §0.4 sets: **07, 01, 02, 04, 05, 06,
   08, 10, 12**, each produced end-to-end by the §8 runbook (draft → re-grepped quotes →
   visually verified figures → `make_article.py --wire` → `qa_page.py` → `shot_qa.py`).
2. The hub `tesla-1894.html`, rendered and wired **last**, once all 12 cards are real links.
3. Visual QA pass (`shot_qa.py` + screenshot review at 375/768/1280) over **every** series
   page, including the outstanding 09 and 11.
4. OG images for all 12 + hub (§6.4), and the reciprocal backlink pass on the 8 existing
   pages named in §5.2.
5. The §16.3 linkable assets: `tesla-1894-plates.html`, `tesla-1894-word-search.html`,
   `tesla-1894-part1-text.html`, a public `tesla1894` GitHub repo, and a first batch of 20
   outreach emails **drafted** (sending is the owner's).
6. Tooling gap the plan flags twice: `qa_page.py` must fail a page with a dead link, so "no
   broken links" is machine-checked rather than remembered. *(Done 2026-10-12: the gate now
   resolves root-absolute links through the same order Cloudflare uses, and a new gate rejects any
   internal link pointing at a URL that only exists to redirect.)*

## 3. Definition of done for one article (applies to every article feature)

- draft at `new_content/1894-series/<NN>-<slug>/article.md`, front matter per §7 with `tid`
  quoted (`"1894_NN"`), body per that article's §9 brief (word target, structure, FAQ if the
  brief has one).
- every quote appears verbatim in `books/extracted/tesla-1894-plain.txt` inside the marker
  for **scan file = printed page + 18**, and is cited `(1894, p. N)`; `grep_quote.py` shows
  it.
- 2–3 figures, each **viewed against the printed page** before use; figure number read off
  the scan, never from the extractor filename; ≤1 patent plate per 2 book engravings; every
  `<img>` has real `alt` (describes the apparatus), `width`, `height`, `loading="lazy"`.
- `python3 books/tools/qa_page.py website/<slug>.html` exits 0 (all §12 numeric gates,
  including the no-dashes voice rule and the no-comments/no-PDF rules).
- `python3 books/tools/shot_qa.py` measurable gates pass at 375/768/1280 **and** the three
  screenshots are reviewed by a vision pass.
- wired: `sitemap.xml`, `llms.txt`, `articles.html` card, and a `_redirects` rule **only** for an
  alias from §5.1 - never for a page's own URL, which is the file name without `.html`;
  card; out-links and in-links per §5.2 with ≥3 reciprocal.
- `new_content/1894-series/index.json` updated (`figures[].verified`, `numeric_gates`,
  `visual_gates`, `wired`, `committed: true`); both repos committed; **nothing pushed**.

## 4. Non-goals

- Tier 2–6 backlog (§10, the next 40 topics) and S7+ throughput — after the flagship set.
- Any `git push` in `website/` (D6: pushing deploys; owner sign-off only).
- Shared-shell changes: the 3 legacy nav titles carrying em dashes, the ~280 KB shell image
  weight that makes §12's page-weight line un-passable, CTA above the mobile fold. All are
  owner calls; §12 exempts the shell.
- Re-running OCR, figure extraction, quote harvesting, or rewriting `SERIES-PLAN-1894.md`.
- New commercial claims about what the product does (§4.1).

## 5. Success criteria (whole run)

- `python3 books/tools/qa_page.py --all-series` exits 0 for 13 pages (12 articles + hub).
- Zero dead relative links across the series, enforced by the new `qa_page.py` check.
- `shot_qa.py` screenshots for all 13 pages reviewed; no figure outside the column, no
  undecoded figure, no horizontal overflow at 375 px.
- `index.json` shows 13 entries with `deployed: false, committed: true`; `git status` clean
  in both repos; `git log` shows a commit per session; no push.
- 0 em/en dashes, curly quotes or unicode ellipses in any series body (tool-checked).

## 6. Decisions taken in autopilot (owner may reverse any of them, cheaply)

- **O1 series name:** keep the working name *The 1894 File*. It appears in 4 non-URL places;
  the plan itself says changing it later is a 10-minute job, so deciding now buys nothing.
- **O2 article 10:** option **B**, the plan's recommendation — keep it as a flagship, publish
  it after 03/01/07, slightly softer title. `tesla-1894-word-search.html` ships regardless.
- **O3 scarcity widget:** keep the donor shell unchanged on all series pages (no per-page
  exception). Fewer moving parts; the shell is out of scope per §4 non-goals.
- **Hub sequencing (§0.2 open problem):** ship the hub **last**, not in S1. Its 12 cards are
  real links, so §12's no-broken-links rule passes without a plain-text exception.
- **Branching:** work repo gets `feature/1894-series-flagship`; `website/` stays on `main`
  because it is the deploy repo and its branch is what the owner reviews and pushes.

## 7. Self-grill (autopilot interview record)

- *Q: is "finish the plan" the goal, or is "ship the series"?* A: finish the production
  tasks. Publishing is the owner's (D6); `deployed` stays false.
- *Q: does 12 articles + hub fit one run?* A: it is 13 units of one repeatable runbook; the
  plan's own cadence is 4–5 per session. The harness clears sessions between tasks, so the
  unit of work is one article, not one session.
- *Q: what would make a "done" article still wrong?* A: a figure whose subject is wrong
  (OCR caption lies), a quote pinned to the wrong page, a dead out-link. Those three are why
  the criteria name the tool and the visual check explicitly.
- *Q: what is tempting but out?* A: fixing the shell (nav dashes, page weight, CTA fold),
  starting Tier 2, editing legacy pages. Parked in §4.
