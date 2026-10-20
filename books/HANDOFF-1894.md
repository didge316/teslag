# 1894 series - session handoff, 2026-10-20

Read `books/PLAN-1894.md` first: §0 (what is finished), §1 (the two commands that tell
you the truth), §2 (the two-repo trap), §8 (owner decisions), §9 (standing rules). This
file only records what changed after that plan was written, and where the work stopped.

Everything below was measured in this session unless a line says otherwise.

---

## 1. Repository state

| | branch | HEAD | pushed |
|---|---|---|---|
| parent `~/projects/other/tesla-generator` | `feature/1894-series-flagship` | the commit titled "1894 word-search page drafted (T2)"; `git log --oneline -1` gives it | no |
| `website/` (separate repo) | `main` | `ab37502` | no |

Nothing in either repo has been pushed. Pushing deploys the site (D6), so nothing is
deployed. `website/` is a nested repo: `git status` in the parent shows it as `? website`
and tells you nothing about it. Always check both.

## 2. Committed this session

**T1, the quote gate - parent `6f6e7d6`.** `check_quotes.py` rewritten (tiered matching:
exact, nospace, wordstream, fuzzy; sub-0.90 near-misses became NOTEs instead of failures;
citation regex now reads `(1894, pp. 376, 381; ...)`; code spans and link labels blanked
before quote pairing; a `--self-test` fixture covering each fixed class), `grep_quote.py`
given a `BookIndex` built once per run plus symmetric hyphen folding, and
`run_gates.py` running the self-test as a step. Three real uncited quotes in
`00-hub/article.md` were given citations (pp. 184, 394, 258). Measured: findings went from
10 to 3, and the 3 are real; the quote pass went from 134s to about 32s.

**T0, the plates page - website `2980d9a` then `a71530c`, parent `fa8c3cf`.**
`tesla-1894-plates.html` plus its 72 grid thumbnails committed; the 9.7 MB ZIP deliberately
left out (§6 below). A 14th row added to `new_content/1894-series/index.json`; the plates
draft, notes and `selection.json` committed; `plates_gallery.py --wire` added; the page
wired into `sitemap.xml` and `llms.txt`. Not added to `articles.html` (asset pages are not
in the grid, per the plates draft) and no `_redirects` rule (its `pretty_slug` is its own
URL).

**Gate state as measured after those commits:** `run_gates.py` exits 0, `run_gates.py
--quick` exits 0, and the numeric page gates report 14 of 15 pages passing. The one
failing line is `tesla-1894.html` being **not built yet**, which the runner reports as a
warning, not a defect. That is T3 and it is still the only unbuilt page.

**Re-run at the end of this session, with the word-search draft in the tree:** full
`run_gates.py` PASS, quote pass clean in 33s, 14/15 pages, the only unbuilt page still
`tesla-1894.html`. The new draft is picked up by the quote pass and adds no findings.

---

## 3. What is uncommitted now, and what was committed at the end of the session

Committed before the handoff was written, so the tree is clean for these:

- parent: the commit titled "1894 word-search page drafted (T2), and the tools it needed"
  (its hash moves whenever this file is amended into it, so it is named by title). It holds
  `books/tools/count_terms.py`, `books/tools/make_article.py`,
  `new_content/1894-series/word-search/article.md`, this file and `books/PLAN-1894.md`
- website `ab37502`: the two word-search figures

Still uncommitted, and not ours to decide:

```
website/  ?? assets/tesla1894/tesla-1894-plates.zip   9.7 MB - owner decision, §6
website/  ?? js/email-capture-widget.html             not ours, leave it
```

### 3a. Tool changes, uncommitted

`books/tools/count_terms.py`, rewritten:
- reports **whole-word** and **substring** counts separately, and says in its own output
  header what each means
- `--keep-furniture` indexes running heads, bare folios and short display lines too; the
  default drops them, which is what makes a chapter title count differently from a sentence
- `--json`, per-page hit counts, and a three-line provenance header (the command it was
  run with, the file it read, the furniture mode, and `printed page = scan file - 18`)

`books/tools/make_article.py`, four additions, all of them because the word-search page
needed them and the alternative was hand-written HTML in a draft:
- pipe tables (`| a | b |` with a `|---|` row) rendered as the same
  `<div class="table-responsive mb-4"><table class="table table-striped table-bordered">`
  the older pages on this site use
- fenced code blocks, escaped, `<pre class="bg-light p-3 mb-4 fs-6">`
- code spans, `x` to `<code>`, done before the emphasis rules
- a `kicker:` front-matter field, so an asset page does not print "No. None of 12"

Verified with `books/tmp/tbl-test.md`: renders, the table and code block come out well
formed, and no backticks survive in the body.

**No-op on existing pages, proved rather than assumed.** Re-rendering article 10 to
`books/tmp/a10-recheck/` with the changed tool differs from the committed page by exactly
4 diff lines, one of which is the pre-existing FAQ heading case: `make_article.py` emits
`<h2>Frequently asked questions</h2>` and the shipped page reads "Frequently Asked
Questions" because `titlecase_headings.py` fixed it after rendering. So the table/code/
code-span changes change nothing, and **the title-case pass is a required step after every
render, not an optional one.**

### 3b. The word-search page (T2), exactly where it stands

Draft: `new_content/1894-series/word-search/article.md`. Unnumbered directory, like
`plates/`, because it is an asset page in the hub's family: `tid: "1894_hub"`, no
`series_no`, a custom `kicker:`.

What is done:
- front matter: title 50 chars, description 143 chars, 4 FAQ entries, 3 figures, sources
  block naming the archive.org item, `pages_used: [6, 424, 429, 496]`
- body: 6 content H2s plus `{{FAQ}}` and `{{SOURCES}}` = 8 H2s, inside the 5-9 gate
- `check_quotes.py` on the draft: **4 quote fragments, 4 verbatim and page-cited, 0
  problems** (pp. 6, 424, 429, 429)
- three figures cut at 500 ppi with `fig_crop.py`, placed in `website/assets/tesla1894/`,
  with their boxes, ink profiles and sha256 recorded in the draft's front-matter comments

What is **not** done: not rendered, not wired, not committed, no `index.json` row, no
`titlecase_headings.py --check` run, no `qa_page.py` run.

To finish it:

```bash
python3 books/tools/make_article.py \
  --md new_content/1894-series/word-search/article.md \
  --donor website/nikola-tesla-inventor-extraordinaire.html \
  --out website/tesla-1894-word-search.html --tid 1894_hub --wire
python3 books/tools/titlecase_headings.py website/tesla-1894-word-search.html   # fixes in place
python3 books/tools/titlecase_headings.py --check website/tesla-1894-word-search.html
python3 books/tools/qa_page.py website/tesla-1894-word-search.html
python3 books/tools/run_gates.py
```

The fix pass is not optional: `make_article.py` emits the FAQ heading in sentence case and
the gate wants title case, which is how every shipped page in this series got its heading
fixed after rendering.

Expect two failures on first run and do **not** fix them by deleting the links:
- **dead link** to `tesla-1894.html`, because the hub is not built (T3)
- **reciprocal links** (`>= 3 links to pages that link back`), because nothing links to
  this page yet. See §4.

### 3c. Why the draft uses single quotes, and double quotes only for book text

`check_quotes.py` treats a backtick code span whose content is verbatim in the book as a
quotation that needs a page citation. On a data page that is wrong - `'pyro-magnetic'` in a
counts table is a search term, not a quotation - but the checker cannot tell, and loosening
it would weaken the gate that catches real misquotes. So the draft follows the convention
the other twelve articles already use: single quotes for terms and for strings from the
book, double quotes only for actual quotations carrying `(1894, p. N)`, backticks only for
file paths, item ids, flags and code. First draft of this page produced 25 false
"NOT CITED" findings; this is why it was rewritten that way.

---

## 4. The reciprocal-link chain (the thing most likely to confuse the next session)

`qa_page.py` requires a page to link to at least 3 pages that link back to it. Today
**zero** pages link to `tesla-1894-word-search`. Article 10 mentions it in prose twice and
deliberately does not link to it, because it did not exist:

- `10-*/article.md` line ~595, a sources entry ending "...is planned and is not on the
  site yet" - its own note says RESTORE THE LINK AT feature-008/t2, which is this task
- `10-*/article.md` line ~817, body: "A standing word-search page for these counts is
  planned and is not on the site yet."

So the three inbound links come from:
1. **article 10** - restore both places above, re-render, re-gate, commit
2. **article 06** (`tesla-cold-flame.html`) - its body already runs a whole-word search of
   this same text layer (line ~194); one added sentence linking to the method page is
   natural. Re-render, re-gate, commit
3. **the hub** - `00-hub/article.md` already links to it; it starts linking when T3 renders

The word-search page itself links to the hub, article 10, article 06 and the plates page,
which gives 3 reciprocal once 1-3 are done.

Re-rendering 06 and 10 changes their bytes, and their `index.json` `visual_gates` records
describe the old hashes. Either re-run `shot_qa.py` for them as part of this work, or say
in the row that T7 must. Do not leave the record claiming a pass for bytes that no longer
exist.

---

## 5. Facts measured this session - do not re-derive them

**The counts.** Two runs of `count_terms.py`, 2026-10-20, default index and
`--keep-furniture`. Format: whole-word / prose-only / everything-kept.

- `free energy` 0/0/0, `free-energy` 0/0/0, `free energ` 0/0/0
- `perpetual` 0/0/0, `perpetu` 0/0/0, `over unity` 0/0/0, `over-unity` 0/0/0
- `unity` 9/9/9 on pp. 3, 4, 119, 142, 143, 156, 193, 327, 477
- `free` 49/97/97 on 73 pages; `energy` 242/243/243 on 119 pages
- `generator` 203/231/243 on 91/98 pages; `magnetic` 215/273/288 on 140/144 pages
- `magnetic generator` **0/4/5**, pages 6, 424, 429 twice, 496
- `pyro-magnetic` 5/5/7; `thermo-magnetic` 3/3/5; `magneto` 1 (p. 448); `dynamo`
  42/60/66; `radiometer` 4 (pp. 126, 232 twice, 236); `inexhaustible` 1 (p. 197)

**The five occurrences of `magnetic generator`, read in context** (this is the part a
regex cannot do):

| printed p. | scan | what it is | text layer |
|---|---|---|---|
| 6 | 24 | editors' preface, list of contents | `pyro-magnetic generators,` |
| 424 | 442 | display heading of chapter XXXVI | `MOTORS AND PYRO-MAGNETIC GENERATORS.` |
| 429 | 447 | running text | `a pyromagnetic generator of electricity1` |
| 429 | 447 | running text | `the pyromagnetic generator, treated in this chapter` |
| 496 | 514 | the volume's own index entry | `Pyromagnetic Generators` |

Two are prose, one a chapter title, one a preface list, one an index entry. All five are
inside a compound; the phrase never stands alone.

**The hyphen.** The book is not consistent. The print on pp. 6 and 424 hyphenates
("PYRO-MAGNETIC GENERATORS." is legible in the crop of scan 442); the print on p. 429 and
p. 496 sets "pyromagnetic" closed up (both legible in crops). Over the raw text layer with
no normalisation: `pyro-magnetic` 3, `pyromagnetic` 4, seven in all. `grep_quote.normalise`
folds letter-joined hyphens, which is what makes one query find both forms.

**The offset rule, verified not assumed.** 402 body pages carry a bare page number in the
text layer; 367 equal scan minus 18; the other 35 are text-layer misreads (scan 226 is
printed p. 208 and reads "308"; scan 446 is p. 428 and reads "438"). Chapter opening pages
carry no folio at all - scan 442 / printed p. 424 is one, which is what the rule is for.
Through the cited chapter: scans 441, 447, 448, 449, 451 all agree with the offset.

**Why 4 and 5 differ.** `grep_quote.strip_furniture` drops a line if it is a bare folio,
or `len < 140 and words <= 9 and caps > 0.7`, or `len < 60 and words <= 6 and caps > 0.6`.
On scan 442 that removes exactly four lines: `CHAPTEK` (7 chars, 1 word),
`THERMO-MAGNETIC` (15, 1), `XXXVI.` (6, 1), `MOTORS AND PYRO-MAGNETIC GENERATORS.`
(36, 4). All caps 1.0. That is the whole difference.

**A discrepancy not resolved, so do not print either number without naming the method.**
The text file is 174,169 words; the 506 page bodies are 172,651; the furniture-stripped
index measured with `len(strip_furniture(page).split())` is 168,438. Article 10 prints
167,998 for the stripped index. The two differ because article 10's `word_counts.py` counts
a different tokenisation. The word-search page deliberately prints no word counts.

**Figure cutting method worth keeping.** `fig_crop.py` boxes set from text-layer bboxes
clip glyph ink (the four fragments of the p. 424 heading overlap). The working method:
render at 500 ppi, compute the row-ink profile (`(im < 140).sum(axis=1)`), and put the box
in the whitespace gaps. On scan 447 the ink bands are 245-307, 314-377, 380-443, 450-512;
the published crop is y240-379, two complete lines, no partial line. Four earlier boxes
each carried a sliver of the next line and were thrown away.

---

## 6. Open owner decisions - do not invent these

1. **The 9.7 MB `assets/tesla1894/tesla-1894-plates.zip`.** Not committed, so the download
   link the plates page states is live locally and dead in git. Options: commit the blob,
   git-lfs, generate on demand, or drop the link. Unchanged since T0.
2. **OG images.** `website/assets/og/` does not exist at all. Thirteen pages, including
   all twelve articles and the plates page, point at `assets/og/*.webp` files that were
   never made. `qa_page.py` only checks the tag, so every page passes while every share
   card is broken. This is T4 and it is bigger than the plan's wording suggests.
3. **T6, Part I as readable text.** In scope or not; if it is, split across 2-3 pages or
   add a documented exemption in `qa_page.py`.

---

## 7. Suggested order for the next session

1. Prove the renderer change is a no-op on existing pages - already done once, see 3a, so
   re-run it only if `make_article.py` changes again.
2. Prove the renderer change is a no-op on existing pages: render one article to a temp
   path, diff against the committed file.
2. Render and wire the word-search page; run `titlecase_headings.py` (it will want the FAQ
   heading), then `qa_page.py`; expect the two known open gates; add the `index.json` row
   recording them as open, in the same style as the plates row.
3. Restore article 10's two deferred references as links; add article 06's link. Re-render
   both, re-gate, commit both repos.
4. T3, the hub. It needs an `faq:` block (front matter is `faq: []` today, and the gate
   wants FAQPage JSON-LD with >= 3 questions) and it will reference the missing OG file.
   Render it, wire it, then re-gate the word-search page - that is the point where its
   gates close.
5. T7 visual sign-off: plates page (never run), word-search page (never run), hub (never
   run), plus re-runs for 06 and 10 if they were re-rendered.
6. T8 close-out.

## 8. Files this session touched

Parent, committed: `books/tools/check_quotes.py`, `grep_quote.py`, `run_gates.py`,
`new_content/1894-series/00-hub/article.md`, `new_content/1894-series/index.json`,
`new_content/1894-series/plates/*` (added), `books/tools/plates_gallery.py`,
`books/tools/make_article.py` (`include_card=False`), `books/PLAN-1894.md`.

Parent, in the commit titled "1894 word-search page drafted (T2)":
`books/tools/count_terms.py`, `books/tools/make_article.py`,
`new_content/1894-series/word-search/article.md`, `books/HANDOFF-1894.md`,
`books/PLAN-1894.md`.

Website, committed: `tesla-1894-plates.html`, `assets/tesla1894/thumbs/*`, `sitemap.xml`,
`llms.txt`.

Website, committed at `ab37502`: `assets/tesla1894/scan-p424-chapter-heading.webp`,
`assets/tesla1894/scan-p429-pyromagnetic-line.webp`.

Throwaway, safe to delete: `books/tmp/tbl-test.*`, `books/tmp/ws-figs/*`.
