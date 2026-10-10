# Architecture

One production line, two repositories. The **work repo** holds the inputs and the machine;
the **deploy repo** (`website/`, a separate git repo) holds what the public sees.

Data flow for one article:

1. **Source** — `books/extracted/tesla-1894-plain.txt` (OCR of the 1894 first edition, page
   markers `<<<<< page-NNN >>>>>`) and `books/pdf-pages-tesla-1894/` (518 scans). Printed page
   = scan file − 18.
2. **Figures** — `books/tools/extract_figures.py` → `website/assets/tesla1894/` (200 crops) +
   `manifest.csv`; `contact_sheet.py` → `_qc/` sheets; the vision QC pass → `manifest_qc.csv`
   (verdict, subject, quality, notes). Patent supplements in `assets/tesla1894/patents/`.
3. **Draft** — `new_content/1894-series/<NN>-<slug>/article.md` with §7 front matter; quotes
   pinned by `books/tools/grep_quote.py`; state of every page tracked in
   `new_content/1894-series/index.json` (the series' own ledger: figures verified, gates,
   wiring, committed).
4. **Render + wire** — `books/tools/make_article.py` assembles the draft into the donor shell
   and writes `website/<slug>.html`; `--wire` updates `sitemap.xml`, `llms.txt`, `_redirects`.
   `articles.html` cards are added by hand (the shell has no anchor for them).
5. **Gates** — `books/tools/qa_page.py` (numeric §12 gates, `--all-series` over index.json,
   exit 0 = pass) and `books/tools/shot_qa.py` (Playwright at 375/768/1280: console errors,
   404s, overflow, undecoded figures; screenshots to `website/_qa/` for a vision pass).
6. **Commit** — both repos, every session, never push (D6). `git push` in `website/` deploys.

Ownership: the tools own structure and the numeric gates; the vision pass owns truth about
figures and layout; the owner owns publishing and any change to the shared shell.
