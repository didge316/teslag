# Tesla Generator Content Research — Handoff Notes

> **Current entry point (2026-10-12): the SEO URL fix.** Start at `SEO-URL-FIX-PLAN.md` §2.1 — it
> is self-contained and supersedes everything below for anything touching URLs, canonicals,
> `sitemap.xml`, `_redirects` or `llms.txt`.
>
> **`website/` Deploy 1 is live.** `8e62498` (`_redirects` + the new `404.html`) was pushed
> 2026-10-12 and verified against the live site: every page 200 at its extensionless URL and 308
> from both other forms, every legacy slug one hop, unknown paths a real 404, and all 8 series
> pages now normalise `/x/` → 308. Full matrix in `SEO-URL-FIX-PLAN.md` §9b.
>
> **The push was not W1 alone.** `main` was 16 commits ahead of `origin/main`, so the 1894 series
> pages 01/02/04/05/07/09/11 and their 200 engravings went out with it. They are new URLs, so no
> existing page's signals changed - but GSC now has three URL groups, not two, and that changes how
> the week of data must be read (plan §10 step 4).
>
> **The extensionless URL rewrite is still uncommitted on purpose** — 46 files, +2,368 / −2,368 —
> and must stay unstaged until it is committed as Deploy 2 (W2); `git add -A` would fold it into a
> Deploy 1 rollback. Do not commit, revert or reformat those files without reading the plan.
>
> The 1894 series workflow below still stands for writing articles, with two changes recorded in
> `books/harness/docs/DECISIONS.md` (2026-10-12) and reflected in the `DOMAIN.md` glossary: canonical
> URLs are extensionless (`/x`, served from `x.html`; no year in a slug), and a **produced article
> is published in the same cycle it is produced** — 40 drafted articles are sitting undeployed in
> `new_content/`, which is what that rule exists to stop.

> **Current work stream (from 2026-10-10): the 1894 book series.**
> Start at `SERIES-PLAN-1894.md` §0.4 — it is self-contained and supersedes the
> keyword-farm workflow below for new content. The 200 figure crops are committed in
> `website/assets/tesla1894/`; the QC pass over them is done (`manifest_qc.csv`, now 203
> rows with six corrected re-exports) but **not yet committed**.
>
> **Standing rule (D6, 2026-10-10): commit every session, never push.** At the end of a
> production session, commit the site repo and the work repo, then stop. `git push` in
> `website/` deploys, so it happens only on explicit owner sign-off and is always a
> separate, named action. Pages stay unpublished until the owner reviews them.
>
> **Session 3 (2026-10-10, with vision):** voice rule now enforced (no em/en dashes,
> curly quotes or ellipses in series prose; `qa_page.py` gates it). Articles **09
> `tesla-worlds-fair-1893.html`** and **11 `tesla-high-frequency-alternator.html`**
> produced, 24/24 and 23/24 numeric gates, wired into sitemap, llms.txt, `_redirects` and
> `articles.html`. Article 03 re-rendered clean, 25/25. Six figure files corrected (the
> OCR had mis-numbered Fig. 199 as 203 and Fig. 206 as 207; the Fig. 297 plate was stored
> upside down). **Committed locally in both repos, not pushed** (D6). Next: `shot_qa.py` on
> 09 and 11, then article 07 (the last dead link in the series points at it), then 01,
> then the hub. Full detail: `SERIES-PLAN-1894.md` §0.4.

## Project Location
- Work repo: `/home/matt/projects/other/tesla-generator/`
- Website deploy repo: `/home/matt/projects/other/tesla-generator/website/`

## What's Done
- 40 keyword folders created in `/home/matt/projects/other/tesla-generator/new_content/`
- `TRACKER.md` tracking file created (all 40 marked ✅ Done)
- Phase 1 Complete: All 40 keywords scraped via web_search — 10 sources each (400 total)
- All `sources.json` files populated with source references (url, title, snippet, domain, relevance_score)
- `TRACKER.md` updated — all 40 keywords marked ✅ Done
- Bootstrap integrity hash fixed and pushed to origin/main
- Popular Pages thumbnails fixed with d-flex alignment and hover underline

## What's Needed Next

> **Superseded — do not follow this list.** It predates the 1894 series and the SEO URL fix, and it
> treats drafted articles as finished work, which invariant 9 of `SEO-URL-FIX-PLAN.md` §1 removes.
> 40 of the articles it calls done are still undeployed. The live next actions are in
> `SEO-URL-FIX-PLAN.md` §2.1 (Deploy 2). This section gets rewritten once the GSC week after
> Deploy 1 has been read, so it can say what actually changed rather than what was attempted.
1. Start writing Phase 1 articles (keywords 1-10, product-adjacent, highest conversion)
2. Each article should:
   - Read the folder's `sources.json` for reference URLs
   - Fetch full article content from those sources
   - Write a 1500-2000 word SEO-optimized article
   - Include internal links to other Phase 1 articles
   - Save as `.md` in the folder alongside `sources.json`
3. Progress through Phase 2 (keywords 11-20) and Phase 3 (keywords 21-40) sequentially
4. Update `TRACKER.md` as articles are written
5. Deploy finished articles to the website repo

## Files to Preserve
- `KEYWORDS-40.md` — master keyword list
- `new_content/TRACKER.md` — tracking file
- `new_content/scrape_sources.py` — scraping script
- `new_content/` — all 40 folders

## Website Status
- Site: teslamagneticgenerator.com
- ClickBank account: didge2009
- Product: Complete Ultimate OFF-GRID Generator
- Last commit pushed: Bootstrap integrity hash fix

## Writing Strategy
- Alternate "Tesla magnetic generator" and "magnetic generator" as primary keywords
- Phase 1 (write first): keywords 1-10 (product-adjacent, highest conversion)
- Phase 2: keywords 11-20 (authority building)
- Phase 3: keywords 21-40 (niche use cases)
