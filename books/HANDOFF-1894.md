# 1894 series - session handoff, 2026-10-20

Read `books/PLAN-1894.md` first: §0 (what is finished), §1 (the two commands that tell
you the truth), §2 (the two-repo trap), §8 (owner decisions), §9 (standing rules). This
file only records what changed after that plan was written, and where the work stopped.

Everything below was measured in this session unless a line says otherwise.

Sections 1, 2, 3, 4, 6, 7 and 8 were rewritten at the end of the 2026-10-20 continuation,
which built the hub and the word-search page, fixed the reciprocal gate, and ran the
backlink pass. Section 5 is the earlier session's measurements and still holds; nothing in
it was re-derived.

---

## 1. Repository state

| | branch | HEAD | pushed |
|---|---|---|---|
| parent `~/projects/other/tesla-generator` | `feature/1894-series-flagship` | the commit titled "index.json, the word-search row, the hub row rewritten to describe bytes"; `git log --oneline -1` gives it | no |
| `website/` (separate repo) | `main` | the commit titled "build-a-magnetic-generator.html gains the section 5.2 backlink block (T5, 8 of 8)" | no |

Hashes are not quoted because amending this file moves the parent hash. `git log --oneline`
in either repo lists every commit this session made, each named in its subject line.

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

**T2, the word-search page, and T3, the hub - website `c2e253d`, `e428a4c`, `1dc8c81`; parent
`7bb62c9`, `1169860`, `7f3ca08`, `7ff3ae3`, `47122c0`.** Both pages now exist as bytes and both
pass 30/30. The hub is in the nav dropdown of every page, in `sitemap.xml`, in `llms.txt`, and
has the two `/1894` 301 rules in `_redirects`. The word-search page has an `index.json` row and
no card and no redirect, both deliberate.

**T5, the backlink pass - website `0fda58d` then eight commits, one per page, `(T5, 1 of 8)`
through `(T5, 8 of 8)`.** Six series articles gained the section 5.2 out-links their own briefs
name, and the eight legacy pages section 5.2 names each gained a "Sources and Further Reading"
H2 with two series links, written by `books/tools/backlink_pass.py`.

**Two new checkers - parent, the commit titled "the reciprocal-links gate could not fail" and
the commit titled "the section 5.2 inbound map".** `books/tools/link_map.py` checks both columns
of section 5.2 using links inside `<article>` only. `books/tools/backlink_pass.py` writes the
legacy-page block.

**Gate state as measured at the end of this session:** `run_gates.py` exits 0, 5/5 gates, quote
pass clean in 39s, and the numeric page gates report **18/18 pages passing with zero NOT BUILT
YET lines**. `qa_page.py --all-series` agrees. `link_map.py` reports 14 section 5.2 edges still
open, every one of them deliberate and each one given a reason in §4 below.

**What the earlier runs in this file were measuring, and why they now read wrong.** Every gate
result written before today's `qa_page.py` fix describes a checker that could not fail the
reciprocal gate. The numbers are not wrong about what they measured; they are wrong about what
they proved. The `index.json` rows now carry the current measurement first and the older record
after it, in the same field, so the history is readable without being believed.

---

## 3. What is uncommitted now

Nothing of ours. Every draft, tool, index row and page this session touched is committed in
the repo that owns it. The only untracked files in either repo are not ours to decide:

```
website/  ?? assets/tesla1894/tesla-1894-plates.zip   9.7 MB - owner decision, §6
website/  ?? js/email-capture-widget.html             not ours, leave it
books/tmp/                                           throwaway, safe to delete
```

### 3a. Tool changes, now committed

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

### 3b. The word-search page (T2) and the hub (T3): both built

Both pages exist, are wired, are committed and pass 30/30. The record of what each one
contains, what was measured and what is still open is in the `index.json` rows, which were
rewritten at this task to describe bytes rather than drafts. Read those rows instead of
this file for page-level detail; they carry the sha256 of the committed file.

Two things learned by rendering that are worth repeating here because they apply to every
page in the series:

- **`titlecase_headings.py` after every render is not optional.** `make_article.py` emits
  the FAQ heading in sentence case and the gate wants title case. Every shipped page in
  this series has had its headings retitled by that pass; the count today was 15 to 16
  headings per page.
- **A missing `{{CTA}}` placeholder is invisible until the gate runs.** The word-search
  draft had no `{{CTA}}`, so it rendered with no affiliate link and no disclosure and
  failed 2 of 30 gates. The placeholder order every page uses is `{{FAQ}}`, `{{CTA}}`,
  `{{SOURCES}}`.

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

## 4. Links: what the gate measures, what section 5.2 asks, and the 14 edges still open

**The gate could not fail until today.** `qa_page.py` line 191 read `stem in ib.get(p,
set())`, where `out` is this page's own hrefs and `ib[p]` is the set of pages linking to
`p`; for every `p` in `out`, `stem in ib[p]` is true by construction. The gate was
`len(out) >= 3` in disguise. It also ignored `https://teslamagneticgenerator.com/x` hrefs,
which is how 50 of the 51 HTML files on this site spell an internal link. Both fixed, with
fixtures in `--self-test` (parent, "the reciprocal-links gate could not fail").

**The gate is still weaker than section 5.2, and this is the thing the next session is most
likely to get wrong.** Section 12's numeric rule is "at least 4 internal links, at least 3
of them to pages that link back", and `qa_page.py` counts every href on the page, the
shared nav dropdown included. The hub is now in that dropdown on every page, and the hub
links to all twelve articles, so every page picks up two reciprocal links from the shell
alone: the hub, and `articles.html`. A page can pass the gate with one content link. When
`qa_page.py` says 18/18, it does not mean the link map is closed.

**`books/tools/link_map.py` is the check that means something.** It reads both columns of
the section 5.2 table and uses links inside `<article>` only, so the shell cannot satisfy
it. Run it; it exits non-zero while any named edge is missing. Current state, measured:

| | |
|---|---|
| closed by content links | every article's own out-link list, and 11 of 13 in-link rows |
| still open, 14 edges | 12 article-to-hub body links, `01 -> 02`, `hub -> electrical-experimenter` |

Reasons, because "open" is not the same as "to do":

- **the twelve article-to-hub links.** The hub is in the nav of every page, which is one of
  the four sources that same row names for the hub (nav, `articles.html`, footer, all 12);
  three of the four are in place and the hub has 51 inbound links. Adding a twelfth body
  link to each article would put all twelve articles outside the 4-6 out-link band the
  heading of that same section sets. Not added, deliberately.
- **`01 -> 02`.** Asked by column 2 only; it appears in no column-1 list, and 02 already
  has three in-links. Adding it would take 01 to seven body out-links.
- **`hub -> electrical-experimenter`.** That page does not exist, is named by the spec's
  hub row, and is not a task in `books/PLAN-1894.md`. This is a spec/plan gap, not a
  broken link; the hub draft's link to it was removed rather than the page invented.

**The spec's two columns disagree in three places**: `01 -> 02`, `10 -> 04` and `03 -> 08`
appear in a "must be linked from" cell and in no "links out to" cell. Two of them were
worth writing on their own merits and are in (`10 -> 04`, `03 -> 08`); the third is the
band problem above. `SERIES-PLAN-1894.md` is the spec and was not edited. `link_map.py`
labels these edges ASKED rather than treating them as defects.

**A side effect of the hub's nav entry, found while measuring the legacy pages.**
`qa_page.py` turns its series-furniture gates on for any page containing the string "The
1894 File". The nav dropdown puts that string into every page on the site, so the eight
legacy pages now report two gates they were never built to satisfy (series kicker, affiliate
disclosure). Nothing about those pages changed; the checker's expectation moved. It is
recorded in each of the eight commit messages. If it matters, the gate should key on the
kicker markup rather than on a string that appears in navigation.

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
2. **OG images.** `website/assets/og/` does not exist at all. **Fifteen** pages now point at
   `assets/og/*.webp` files that were never made: the twelve articles, the plates page, the
   hub and the word-search page. `qa_page.py` only checks the tag, so every page passes
   while every share card is broken. This is T4 and it is bigger than the plan's wording
   suggests.
3. **T6, Part I as readable text.** In scope or not; if it is, split across 2-3 pages or
   add a documented exemption in `qa_page.py`.
4. **`electrical-experimenter.html`.** The spec's hub row asks for a link to it; no such
   page exists and no task in `books/PLAN-1894.md` would create one. Either write it, drop
   the row from the spec, or accept the gap permanently. It is the only section 5.2 edge
   that cannot be closed by editing.
5. **Which word count, if any, the series may print.** Four defensible counts of the same
   text layer disagree: 174,169 words in the raw extracted file, 172,651 across the 506 page
   bodies, 168,438 in the furniture-stripped index, 167,998 in the count article 10 prints.
   The spec's own hub brief says "177,000 words", which matches none of them. The hub page
   no longer prints a number; the word-search page prints counts only with the command and
   the furniture rule attached. If any page ever wants a total, that is the decision.
6. **Whether `qa_page.py` should keep keying the series-furniture gates on the string "The
   1894 File".** Since the hub entered the nav, that string is on every page, so the kicker
   and disclosure gates now fire on 50 legacy pages that were never built to satisfy them.
   See §4.

---

## 7. Suggested order for the next session

T0 through T5 are done. What is left in `books/PLAN-1894.md` is T6, T7, T8 and the owner
items in §6. In the order that costs least to do badly and most to do well:

1. **T7, visual sign-off.** This is now the only gate class with nothing measured, and it
   is the one that needs vision. `shot_qa.py <slug>` at 375 / 768 / 1280 for every page
   this series touched: the hub, the word-search page, the plates page (72-image grid), the
   twelve articles, and the Pages dropdown open at 375 px on one representative page, which
   now carries 32 items including the hub. Record each result into that page's
   `index.json` `visual_gates` row as it is measured, naming the command. Every such row
   currently says STALE or "not run" and names the sha256 it would describe if it were run.
2. **T4, the OG images.** Fifteen files, none of them exist, and no page can be shared
   sanely until they do. Blocked on nothing; it is a rendering job with a legibility check
   at 300 px.
3. **T8, close-out**, once the above is measured: the `index.json` rows are already written
   to the current bytes, so close-out is mostly re-reading them against the visual results.
4. **The push.** Nothing in either repo has been pushed and pushing deploys (D6). When the
   owner decides, the deploy commit is a separate named action, and the site repo is ahead
   of its remote by every commit in this session.
5. **T6 only if the owner asks for it.** It is a day of work and it forces decision 3 above.

Two things not to re-do: the numeric gates are green as of the last run today, and the
section 5.2 map is closed except for the 14 edges in §4, each with a stated reason. If a
page is re-rendered, re-run `titlecase_headings.py`, then `qa_page.py`, then
`link_map.py`, and update that row's sha256 - a gate result describes bytes, not a file
name.

## 8. Files this session touched

Parent, committed: `books/tools/qa_page.py` (the reciprocal predicate, `page_key()` for
absolute hrefs, two fixtures), `books/tools/link_map.py` (new),
`books/tools/backlink_pass.py` (new), `new_content/1894-series/word-search/article.md`,
`new_content/1894-series/00-hub/article.md`, the drafts for 01, 02, 03, 04, 05, 06, 08, 09,
10, 11, `new_content/1894-series/plates/article.md`, `new_content/1894-series/index.json`
(a row for the word-search page, the hub row rewritten to describe bytes, and every row's
`numeric_gates` refreshed to the current sha256 with the older record kept below it), and
this file.

Website, committed: `tesla-1894.html` and `tesla-1894-word-search.html` (new),
`tesla-1894-plates.html` (rebuilt link paragraph), the twelve articles (re-rendered at some
point today), the eight legacy pages named by section 5.2, `sitemap.xml`, `llms.txt`,
`_redirects`, and the nav dropdown line in every other page.

Throwaway, safe to delete: `books/tmp/*` including `PROGRESS-1894.md`, `gatefail.py`, the
`before-*`/`after-*` gate captures, `tbl-test.*`, `ws-figs/`, `a10-recheck/`.
