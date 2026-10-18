# Lessons and Decisions

Append as you go: what surprised you, what you would do differently.

## 2026-10-10 — feature-001: make the rule machine-checked before writing more pages

`qa_page.py` now fails any page with a relative href that does not resolve, prints the
offending href, and runs under `--all-series`. On today's three pages it finds exactly one
dead link (09 -> rotating-magnetic-field-1888.html) and no false positives, which is the
proof the rule was only being remembered before. Lesson: the check was cheap and had been
left out twice; any §12 rule that can be decided from the file belongs in the tool, not in
the prose. `--self-test` covers it with temp fixtures so the deploy repo is never touched.
Also fixed the shell-weight note, which printed bytes as KB (280170 KB for a 273 KB shell);
an evidence line that lies is worse than no evidence line.

## 2026-10-10 — feature-004/t2: a task only closes when the plan row is written

feature-004/t2 was retried three times with the figure work already done. Cause: nothing in
`infinity_validate` or the loop writes a task status. `checkTaskCriteria` (gates.ts) *reads*
`task.status` and fails unless it already says `complete`; the only writer is `infinity_plan`.
The loop's progress fingerprint is `git status --porcelain` plus every `task.id:task.status`
(loop.ts), so an unwritten row reads as "the working tree has not moved" and the phase gate
keeps reporting `tasks-complete: N task(s) still open`.

Two traps to repeat by accident: `findTask` returns the FIRST task matching the needle, so
`infinity_validate task="t2"` validates `feature-001/t2` (already complete) and returns a
meaningless PASS - always scope with the full key, `task="feature-004/t2"`. And `infinity_plan`
treats `tasks` as authoritative: omit a key and it is deleted, so submit all 66 keys (bare
`{"key": ...}` entries inherit subject/status/dependsOn from the stored row) and put the status
only on the row being closed.

Working pattern, as used at plan revs 13-20: do the work -> `infinity_plan` with `baseRevision`
and the full key list, target row `status: "complete"` -> `infinity_validate` scoped with the
full task key -> stop. Lesson: if a gate keeps failing on a count, read the check that produces
the count before doing the work again.

## 2026-10-11 — feature-004/t4: `--wire` writes a truncated llms.txt line, so wire by hand

`make_article.py wire_updates()` builds the llms.txt entry as
`(standfirst or description)[:150]`, which cuts mid-sentence. Article 01's entry shipped that
way ("...the tests he ran to") and nobody noticed, because nothing reads llms.txt back and no
gate checks it. Lesson: a wiring helper that silently truncates is worse than doing the four
edits by hand; the entry was written out in full for 02 and 01's line was completed. If `--wire`
is used again, check the llms.txt line it writes.

Two visual-QA limits worth recording so they are not mistaken for passes:
`shot_crops.py`'s `nav-dropdown` crop is the page region *under* a closed dropdown (the shot was
taken before the menu was opened), so the dropdown is only covered by `shot_qa.py`'s
`nav=True / navitems=31` measurement, never by that crop. And the in-body affiliate alert sits
below the mobile first screen on every series page (16,747 px on 02) because the donor shell puts
it after the article body, and the sidebar stacks below the column on mobile, so §12's "CTA
visible on mobile first screen" is not met on any series page. `shot_qa.py` prints the position
and deliberately does not fail on it; closing that gap is a shell change, not a per-article one,
and belongs to the owner. The mobile fold was still reviewed (title, standfirst, first H2 render
cleanly at 375 px).

## 2026-10-11 — feature-004/t5: the unscoped BUILD gate cannot be made to pass mid-build

The same check failed five times in a row with the same text, `tasks-complete: 46 task(s)
still open`, while the article it was being blamed for was already written and verified. Read
the check instead of doing the work again: `tasks-complete` counts every open row in the plan,
so at 20/66 it reports 46 open no matter what any one task ships. It is a phase gate, not a
task gate. The task gate is scoped: `infinity_validate feature="feature-004"
task="feature-004/t5"` (full key, never a bare `t5` — `findTask` returns the first match).
`gateHistory` in config.json shows the pattern plainly: every row with a feature/task pair
passes, every bare row is the loop's own whole-plan check and is expected to fail until the
last task closes.

The trap is the same one written up at feature-004/t2 and repeated here: nothing in the loop
writes `task.status`; only `infinity_plan` does. A finished draft with an unwritten row reads
to the loop as no progress. Working pattern, unchanged and still the only one that works:
do the work -> `infinity_plan` with `baseRevision` and all 66 keys, status on the one row
being closed -> scoped `infinity_validate` -> commit -> stop.

Two things noticed while verifying the 04 draft, recorded rather than fixed:
`check_quotes.py` reports 0 problems on it (41 page-cited quotes, all verbatim), but the draft
is 2,899 words against §9 brief 04's 1,600. Nothing in §12, `qa_page.py` or the evaluator
rubric measures length, and every shipped sibling runs over its brief (01 +32%, 02 +38%,
07 +19%, 09 0%, 11 +10%), so 04 is an outlier inside a habit, not a gate failure. Trimming
1,300 words of sourced, page-pinned prose at draft stage, unasked, is a bigger risk than
leaving the number on the record: the review phase should decide with the count in hand.
Also still open for t7/t8: §5.2 requires 04 to be linked from 10, and 10 is not written yet,
so the `>= 3 links to pages that link back` gate on 04 depends on 10 existing and linking back.

## 2026-10-11 — feature-004/t7: two things the numeric gates cannot see, recorded while rendering 04

`qa_page.py`'s `>= 3 links to pages that link back (§5.2)` gate is vacuous as written:
`inbound_map()` maps target -> files that link to it, so `slug in ib[p]` asks "does this page
link to p", which is true for every out-link by construction. On 04 it prints ok while 04 has
zero inbound links. The real §5.2 in-links (02, 10, hub) are still open and are closed by
feature-009/t2, which is the task that names them; the gate is left alone here because changing
it would fail pages that already passed and that is a decision for the owner, not a drive-by fix.
Lesson: read the check before trusting an ok, the same lesson as the `tasks-complete` count.

Second: every series page's `og:image` points at `assets/og/<slug>.webp` and that directory does
not exist in the site repo, on all seven shipped pages (legacy pages use real `assets/*.webp`).
Nothing in `qa_page.py` or `make_article.py` looks at the og file, and §12's "OG legibility" is a
vision gate over a file that was never made. feature-010 already owns this (OG images for all 13
pages), so it is left to that feature rather than fixed as a per-article side fix.

## 2026-10-11 — feature-004/t8: the wiring half of a task has no test, and a page-scan figure is not legible on mobile

shot_qa.py passes on 04 at 375/768/1280 (console clean, no 404s, no overflow, nav intact, all
three figures decode and fit the column) and the shot_crops.py desktop + mobile crops were
reviewed by eye: Fig. 184 (printed p. 344), Fig. 125 (p. 188) and the p. 346 page crop each show
what their alt and caption say, with the printed captions inside the first two. Nothing to fix.
Two limits worth recording:

A page-scan figure is a different object from a figure crop. At 1280 the p. 346 crop is readable
as type; at 375 the printed body text is about the size of a footnote and the labels inside
Fig. 184 (G, L, L1, II, I, C1) drop below readable. §12's "caption legibility" is about the HTML
caption, which holds at both widths, so this is not a gate failure — but it means a page-crop
figure must never be the only place a claim appears. 04's caption quotes the sentence in full and
the body quotes it again, which is why the crop is acceptable. Any future page-crop figure needs
the same, and should be sized against the 375 px column, not the desktop one.

Second: `articles.html` has no QA tool at all. shot_qa.py and shot_crops.py both work from
`article figure` and the series-page DOM, so the card that "wired" requires is added blind. Wrote
books/tmp/card_shot_04.py (throwaway, gitignored) to shoot just that card and its grid row at
1280 and 375 and measure clipping, column width and page overflow — all clean. Lesson: five more
articles and the hub each add a card, so if that check is done twice more it belongs in
books/tools/, not in tmp/.

Also still true and left alone: three llms.txt entries in The 1894 File section (07, 09, 11) are
still in the truncated `--wire` form, ending mid-word ("the man w", "It al", "give a paper ").
01, 02 and 04 are written out in full. Nothing reads llms.txt back and no gate checks it, so the
only way these get fixed is someone noticing. Not fixed here because those are not this task's
pages; the fix is three sentences of standfirst, whenever someone is in there.

## 2026-10-11 — feature-005/t1: re-run the draft's own evidence lines, they are claims too

The 05 draft was already on disk when this task was retried. `check_quotes.py` reports 27/27
fragments verbatim and page-cited, so the quotes were never the problem. What was wrong were the
*counts the draft asserts about the volume* — the same class of claim Appendix D exists to pin down,
and nothing re-checks them mechanically:

- The draft said the word 'massage' is "printed three times". Re-running the whole-word search over
  `books/extracted/tesla-1894-plain.txt` gives 4: chapter heading (printed p. 394), table of
  contents (front matter), and **two** index entries (printed pp. 494 and 495 — the index lists the
  paper twice). Fixed in the body and in the sources entry. The "not used once in the running text"
  half was right, so the sentence's point survived; only the number was wrong.
- The other counts in the draft check out as written: 'cure' 0, 'curing' 0, 'cured' 1 (p. 69,
  polyphase armatures), 'disease' 1 (p. 395), 'violet ray' 0, 'electric bath' 0, 'electrotherapy' 0,
  'diathermy' 0, 'physiotherapy' 0, 'violet' 2 (pp. 163, 218, both colour of a discharge). The index
  really does file 162 and 394 under one heading, Physiological Effects (printed p. 495), and the
  Ch. XXX footnote verifies verbatim on p. 392 while the Ch. XXXI footnote is garbled in this scan
  ("Tlie EUctrical Engineer of Deo. 23d, 1891"), which is why the date is paraphrased not quoted.
- The two modern medical sources were fetched, not trusted: Cureus 16:4 e57427 (Amani et al., 2024)
  does say the FDA "recognizes diathermy as a therapeutic method that produces profound heating under
  the skin, muscles, and joints", and RMHP 16 (2023) 1171-1185 (Almalty et al.) does say use of SWD
  fell in some countries "due to the lack of empirical evidence". Both §4.1 modern claims stand.
- One sentence described our own live page wrongly: it called
  `How-Much-Noise-Does-a-Free-Energy-Device-Make.html` "a quantity that can be measured with a phone
  at three metres". That page contains no measurement method and no phone; it gives decibel figures
  and a comparison. Rewritten to describe what the target page actually does. Lesson: when a bridge
  sentence characterises another page on the site, read that page — a wrong description of our own
  content is a trust defect the numeric gates cannot see.

Deferred, on the record rather than in the file: §5.2 requires 05 to link out to 10
(`tesla-free-energy-what-he-said.html`). Article 10 is feature-007, which runs after this feature, so
the file does not exist in `website/` and linking now would fail qa_page.py's dead-link gate at t3.
The deferral is written as a comment above `cta:` in the draft; feature-009/t2 is the task whose
criteria name it ("every deferred §5.2 out-link now points at an existing page"). Body out-links as
drafted: 4 (01, 11, scam, noise), inside §5.2's 4-6 band.

Length, recorded not fixed: 2,672 body words against §9 brief 05's 1,300. Same situation as 04 at
t5 — every shipped sibling runs over, nothing in §12 or qa_page.py measures length, and the review
phase should decide with the counts in hand.

## 2026-10-11 — feature-005/t4: `--wire` cannot write an articles.html card at all, and a patent sheet is not legible at 375 px either

shot_qa.py passes on 05 at 375/768/1280 (console clean, no 404s, no horizontal overflow, nav=True
31 items, all three figures decode, carry width/height and stay in the column) and the
shot_crops.py desktop + mobile crops were reviewed by eye: Fig. 208 (printed p. 392) and Fig. 209
(printed p. 393) each show the parts their alt and caption name, with the printed `FIG. 208.` /
`FIG. 209.` inside the crop; the US 568,176 sheet carries its own header line, so the number and
the date are legible in the figure itself, which is what §6.3's "number confirmed" needs on the
page and not only in the sources list. Nothing to fix on the page.

Two things worth recording:

`make_article.py --wire` can never add the articles.html card. `wire_updates()` looks for
`class="list-unstyled"` in articles.html and inserts a 40×40-thumbnail `<li>` there; articles.html
has no `list-unstyled` block (it is a `col-md-6` card grid), so `_card_anchor()` returns None and
the function reports "articles.html: no card anchor found — add by hand". That is why 02, 04 and 05
were each wired by hand, and it is the correct outcome, not a workaround — but it means the
"wire with the tool" instinct is wrong for the card specifically, and the card is the one wiring
edit a human has to see. Also: the front-matter `card_image` / `card_alt` fields are used only by
that dead `_article_card()` path, so no series card on the live site has a thumbnail. Left alone:
making the tool write the grid card is a tool change with its own QA, not a per-article fix.

The feature-004/t8 finding about page-scan figures generalises to patent sheets. At 1280 the
US 568,176 drawing is readable; at 375 the header line and number still read, but the part labels
inside Fig. 1 (A, B, C, H, K, L, L') are marginal, and the same is true of the labels inside
Fig. 208 and Fig. 209. The HTML captions hold at both widths and name the parts in words, so the
claim never lives only inside the drawing. Rule for the remaining articles: any figure whose point
is a labelled part must have that part named in the caption text, and the figure must be sized
against the 375 px column.

Card QA is now a script, still in books/tmp/ (gitignored) as card_shot_04.py was:
`python3 books/tmp/card_shot.py <slug>` shoots the card and its grid row at 1280/375 and fails on
clipping, unequal grid columns or page overflow. On 05's card: 498×335 in a 546 px column at 1280,
279×474 in a 327 px column at 375, no clipping, columns equal, no overflow. This is the second
time it has been run, so by the feature-004/t8 rule it goes into books/tools/ on the next use —
not moved here, because a tool in tools/ is a tool the gate may come to depend on and that is the
owner's call.

Also checked rather than assumed: sitemap.xml still parses (43 `<url>` entries, no duplicates,
05's lastmod 2026-10-22 matches the front matter), the llms.txt entry is the full standfirst and
not the 150-character form, and qa_page.py still exits 0 on 05 after the wiring (26/26). The
mobile CTA position is unchanged in kind: alert-info at 21,150 px, scarcity at 25,329 px — still
below the first screen on every series page, still a shell issue, still reported not failed.

## 2026-10-12 — feature-005/a06-figrec: a WIP commit in `website/` is only half committed until the gitlink moves

The 06 index.json entry exists now. The figure record it carries was already on disk (draft
front matter plus the five evidence crops under `06-tesla-cold-flame/figures/`), so this task
restated it instead of re-deriving it, which is what §6.6 asks for. Two gaps found while writing
it, both recorded in the entry rather than fixed as drive-bys:

- The site-repo WIP commit `7b32754` (the three published crops) was never recorded in the work
  repo: the gitlink still pointed at `249733b`. Lesson: the pattern at feature-004/t6 and
  feature-005/t2 was one work-repo commit carrying `index.json` **plus** the gitlink; a WIP commit
  that touches only the site repo leaves the record broken until someone moves it. Moved here, and
  said so in the commit message.
- `manifest_qc.csv` has no rows for the three published crops; the file still ends at rows 214-216
  (article 05). Every earlier figure task wrote rows for the crops it shipped. Named in
  `blocked_on` for feature-005/t6 instead of written here: the rows belong with the figure work, and
  writing them means a second site-repo commit inside a logging task.

Checking rather than assuming paid for itself once. The three published `.webp` files hash to the
sha256s in `figures/README.md` and their pixel sizes match the front-matter `width`/`height`, so the
files on disk are the plates the record describes; opening them confirmed each carries its printed
`FIG.` line inside the crop and nothing else from the page. That is also what turned the Fig. 141
globe label from a hypothetical into a fact: the published crop shows an italic `L` at the right of
the globe where the OCR prints `Z`, and the p. 228 sentence "grasp the globe L with the hand" is
verbatim in `check_quotes.py`, so the OCR is the wrong one. Settling it against the 500 ppi print,
and narrowing the front-matter claim that the part letters are "too degraded to read even at
500 ppi", stays with feature-005/t6; the alt text naming shapes rather than part letters is
unaffected either way.

Three different word counts were in circulation for the same draft (5,113 in the front matter,
9,280 in the plan row, 5,471 measured now, 4,930 excluding figure alt and caption copy). The entry
records the method and the variants. Lesson: a count without its method is a claim, and the
`words_draft` numbers in `index.json` are snapshots of one particular measure, not comparable to
anything counted a different way.

## 2026-10-12 — feature-005/a06-figrec (rework pass): the Fig. 141 globe label was settled here, not at t6

The entry above says settling the label and narrowing the front-matter claim "stays with
feature-005/t6". That is superseded: the task went to rework (the previous attempt died on a
turn timeout with the tree modified and uncommitted), and in this pass the label was settled and
the front-matter sentence narrowed. What the record now says, and how it was proved:

- The globe label is an italic `L`, the text layer's `Z` is the mis-read. Two reads, both against
  the print of the same page: the printed line that introduces the plate (cropped from the text
  layer's own bbox for the word it renders `Z,` — x 245.088–252.351 pt × 6.9444 px/pt at 500 ppi —
  ends `…lamp globe L,`), and the plate glyph itself, which has the same three strokes as that
  printed italic `L`. The clean body text agrees: `When the globe L (Figs. 141 and 142)` (p. 227)
  and the p. 228 sentence the page already quotes verbatim.
- A 23 px glyph read from a 4x LANCZOS upscale reads as a `7`; interpolation smears the serif bar
  into a top bar and the rising foot into a flat one. The read was made from a native-pixel map.
  Lesson: for a label this small, print the pixels, do not upscale them.
- The two label crops were re-cut from the boxes now recorded in `figures/README.md` and came out
  byte-identical to the committed files. The five t6 crops cannot be re-cut at all — their boxes
  were never written down. Lesson: record the `--box` with the crop, or the crop is evidence only
  for as long as the working directory lives.
- Two incidental numbers in the record were wrong and are corrected: the 500 ppi page size, given
  as 1856 x 3226 in the front matter and the README, is 1856 x 3227 on all four renders; and the
  README's account of its own provenance ("seven of eight" from t6) is five from t6 and three cut
  at this task.
- Still open and still not this task's: `manifest_qc.csv` has no rows for the three published
  crops (the file still ends at rows 214-216), which belongs with feature-005/t6.

Closing `feature-005/t6` at this task. Its plan row was still `pending` when no commit has its
name: the reading was done 2026-10-11/12 and its output (the front-matter record and the five
`books/tmp/f05t6*` crops, copied out and committed) went in under `feature-005/a06-wipcommit`,
so the row was never closed and `a06-figrec` could not be marked complete while it was open —
the plan tool refuses a `complete` task with an incomplete dependency. Checked against t6's three
criteria rather than assumed: the record was read before anything was re-opened; only the figure
whose evidence contradicted itself was re-opened at 500 ppi; and every read is written into the
front matter and `figures/README.md`, not left in gitignored `books/tmp/`. All three hold, so the
row is closed here. What is genuinely still open, and is now t7's and t8's and a06-wirecommit's
rather than t6's: the `manifest_qc.csv` rows for the three published crops. Lesson: a task whose
work landed in someone else's commit still needs its own row closed, or the next task inherits a
dependency it cannot satisfy.

## 2026-10-12 — feature-005/a06-wirecommit: wiring an unwritten page is not wiring

The task was handed to me while `feature-005/t7` (render) and `t8` (visual QA) were still
`pending`: the rework pass replays the impacted chain ahead of its own dependencies, so
`a06-wirecommit` came before the tasks it `dependsOn`. Its four criteria are all pointers at
`website/tesla-cold-flame.html`, which did not exist. Wiring it anyway would have put a 404 in
`sitemap.xml`, in `llms.txt` and in the `articles.html` card, and `qa_page.py`'s dead-link gate
does not run over `articles.html`, so nothing would have caught it. The render was done here —
the exact command t7 names, run once — and the fact that a prerequisite was done outside its own
row is written into `render_note` rather than left for the next reader to infer. Lesson: when a
task's criteria are all references to an artifact, the artifact is part of the task; do the
prerequisite and say so, and do not commit a link to nothing.

`make_article.py --wire` under-wires silently. It exits 0 having done two of four: it writes the
`sitemap.xml` entry, truncates the `llms.txt` line at 150 characters (the feature-004/t4 lesson),
skips `_redirects`, and fails to write the card at all — `wire_updates()` looks for
`class="list-unstyled`, and `articles.html` has not had one since the SEO URL fix rebuilt the card
grid as Bootstrap `col-md-6` cards. The card failure is only a printed note, not a nonzero exit.
Lesson: `--wire`'s exit code does not mean wired; either teach `wire_updates()` the current card
markup (a `books/tools/` fix, not a drive-by at a wiring task) or stop calling it and wire by
hand as 04 and 05 did.

One of the four criteria is correctly satisfied by an absence. `_redirects` needs no rule for
`/tesla-cold-flame`: the slug is the canonical URL, Cloudflare resolves the static file before it
consults `_redirects`, and a self-referential rule never fires while blocking trailing-slash
normalisation (SEO-URL-FIX-PLAN §1.4, and the comment in `_redirects` itself). Checked against the
file rather than against the earlier index entry — and the 05 entry in `index.json` still claims
`_redirects (/tesla-high-frequency-massage 301)`, a rule site commit `8e62498` (Deploy 1) removed
as one of the eight dead rules. That stale claim is left alone (not this task's page) and named in
05's face so the next reader of that entry knows the file disagrees with it. Lesson: a criterion
that names an artifact can be met by its documented absence, but only if the absence is verified
from the file and the reason is written down.

The card was verified with `books/tmp/card_shot.py` at 1280 and 375 and both crops reviewed —
that is the card this task added, so it belongs here; the page-level `shot_qa.py` run and the
screenshot review stay with t8.

The row could not be closed from the work alone: `infinity_plan` refuses
`a06-wirecommit = complete` while `feature-005/t8`, one of its `dependsOn`, is still `pending`.
The gate then fails on `task-criteria: ... is "rework", not complete`, and the same brief is
re-issued — a task handed out of dependency order cannot be closed until its dependency is, so the
loop would have spun on it. `t8` (`shot_qa.py` at 375/768/1280 plus the screenshot review) was
unblocked by the render, so it was done in this session and both rows closed. Lesson: when the plan
refuses a `complete` on a dependency, that is a signal about the plan's order, not a reason to stop;
finish the dependency if it is genuinely unblocked and say so in the record, or the row stays
`rework` and burns retries. `t7` was closed the same way — its two criteria (the page renders,
`qa_page.py` exits 0) were both measured here, and leaving it open would have handed the next task a
dependency it could only re-run.

Found while reading the rendered page, not fixed: the Sources block says the quote register is
"52 quotes across 18 printed pages", `quotes.md`'s own header says "53 quotes (58 fragments)", and
`check_quotes.py` on the draft counts 56 fragments. Three numbers for one register and the smallest
is the one the public reads. It is in the draft's front matter (feature-005/t5's artifact), so it is
named in `blocked_on` rather than patched at a wiring task. Lesson: a count that travels from a
register into a page copy drifts, because nothing re-checks it at render time; if the number is on
the page it belongs in the render-time check, not in prose.

## feature-006/t0 (2026-10-12) — article 08 quote pin, batch 1 (entries 1-3)

`new_content/1894-series/08-tesla-weird-inventions-1894/quotes.md` + `gen_quotes.py`:
29 quotes verified across 12 printed pages (pp. 6, 409, 410, 412, 413, 416, 417, 418,
419, 420, 422, 423), 16 rejected with the reason each one fails. The generator is the
same shape as article 06's: it imports `check_quotes.fragments`/`locate`, so a quote
that passes here passes in the draft, and it exits non-zero and writes nothing if any
quote misses. Batches 2 and 3 append to the lists in the script and re-run; the file is
generated, so the header counts never drift (the article 06 lesson about three
different counts for one register is the reason this one is not hand-written).

Three findings that outlive this task.

1. **A §9 brief hook can be wrong about the print, and the pin is where that gets
   caught.** Brief 08 calls entry 3 "an amp-hour meter that counts bubbles": the
   chapter (printed pp. 420-423) registers a change in *resistance* caused by metal
   plating on and off two conductors, names the unit as the **lamp-hour** (1 hit in the
   volume, p. 422), and praises reading it off an ohm-meter "without resorting to
   weighing the deposit" (p. 423). `bubble` occurs 9 times in the volume and never in
   that chapter. Brief 08's entry-2 hook ("the reason your capacitor is not in air") is
   a modern claim about a modern object, and the 1894 text is about high-frequency,
   high-potential apparatus only. Lesson: the hooks in §9 are prompts, not sources —
   grep the hook's own words before writing the entry, and if the print contradicts the
   hook the print wins. Where a hook cannot be grepped at all it goes into Rejected
   with the counts that show why, so the next task does not meet it as new.

2. **Appendix D's word counts are not all re-greppable.** It records `magnetic
   generator` as 5 hits at pp. 6, 424, 429, 496. Re-grepped: 4 hits, at pp. 6, 429,
   496. The fifth is the chapter XXXVI heading on printed p. 424, which this scan OCRs
   as "MOTORS AND PYRO-MAGNETIC RATORS" because "GENE-" is cut at the foot of the page
   — so it exists in the print and cannot be re-grepped. The claim itself holds (every
   occurrence is *pyro*-magnetic), which is what article 08's closing beat and article
   10 both rest on. Batch 2 (entry 4, pp. 424-431) must state the beat from pp. 429 and
   496 and treat the heading as a page-scan detail, not a quote. Lesson: when a fact box
   in SERIES-PLAN-1894.md cannot be reproduced by the tool, write down which half is
   greppable and which half is a scan-reading, rather than quietly repeating the number.

3. **Part III is the editor's prose about Tesla, in the third person, and a listicle
   about "his weird inventions" blurs two third-persons into one.** Chs. XXXIII-XXXV
   say "Mr. Tesla divides such circuit", "attributable to Mr. Tesla". Same trap the
   article 06 pin flags for ch. XXIX. The pin carries the evidence as two quotes (the
   editor's own inventory of the "Miscellaneous" section at printed p. 6, which is
   almost item for item brief 08's nine entries — so the list is the book's, not ours)
   and a flag telling the draft to say once, early, that Part III is the editor's
   writing.

Also recorded for the figure task (feature-006/t2), so it does not re-open settled
work: crops for entries 1 and 3 already exist and are QCd `keep`/A (scan files
428-434, 439, 440); entry 2's engravings (Figs. 227, 228, printed p. 418 = scan 436)
have **no** crop and no manifest row, and `books/pdf-pages-tesla-1894/page-436.pdf` is
there to cut them from. Two of the existing `manifest_qc.csv` subject lines describe
those engravings wrongly (the meter figures are called a coherer; Fig. 220 is called a
lamp loop), which is the standing reason captions come from the prose and figure numbers
from the printed page, never from the extractor filename or the QC note.

## 2026-10-16 — feature-006/t0 (rework pass): a suspect row is re-proved by re-running it, not by rewriting it

The rework came from `feature-005/a06-wipcommit` exhausting its retry budget
(`harness/rework.json`, `maxImpactDepth: 3`), which dragged `feature-006/t0` down with it.
Nothing in the pin had failed, so the pass was a re-proof, not a rewrite:

- `gen_quotes.py` re-run — exits 0, 29 quotes / 29 fragments / 12 printed pages /
  0 failures / 16 rejected, and it reproduced the committed pin (347e8b5) **byte for
  byte**. A generated pin that regenerates identically is the whole test; the article 06
  lesson about three different counts for one register is exactly why this file is
  generated and why "identical output" is a meaningful result.
- Seven quotes re-grepped a second time through the independent CLI (`grep_quote.py
  --page N-N`), one per entry plus the awkward ones: the ASCII ` - ` form that folds to
  the print's em dash (p. 410), the form that starts after the print's doubled `it`
  (p. 419), the lamp-hour sentence (p. 422), the editor's verdict on electrolytic
  meters (p. 423). Each returned exactly one hit on its stated page.
- The OCR artefacts the pin relies on were counted in the raw text again: `isvaried` 1,
  `bychanges` 1, `should -be changed` 1, `for a -given time` 1, `what may termed` 1.
  The doubled `it` at p. 419 is **not** greppable as `it it has been` — the OCR puts a
  line break between the two words — so only the pinned form, which starts after it,
  matches. Lesson: a rejected item's *reason* has to be re-checked too; a claim about the
  scan written in prose can be as stale as a quote.

New finding, recorded in the pin header for batches 2 and 3: **`check_quotes.py` is not a
gate for a pin file.** Run on `quotes.md` it reads the apostrophes in the `- why:`
annotations and the struck-through Rejected items as quotation marks and reports ~40
false failures around 30 real matches. A session that reaches for the draft checker at a
pin task will spend its budget explaining a red run that means nothing. The pin gate is
`gen_quotes.py` — it imports `check_quotes.fragments`/`locate` over the same index, so a
quote that passes there passes in the draft, and it writes nothing if one misses.
`check_quotes.py` belongs to `article.md` (feature-006/t3).

Closing a `rework` row still needs the plan row set to `complete` through `infinity_plan`
before the gate will pass — the gate check *is* the status field
(`task-criteria: ... is "rework", not complete`). Submitting 91 rows is safe with
`{key, status}` only: `applyTaskList` inherits every omitted field from the stored task
(`src/taskList.ts`, "merge onto the stored task so unknown fields survive"), so subjects,
`dependsOn`, criteria and subtasks survive untouched and there is nothing to mistype.

## 2026-10-16 — feature-001/heading-case-gate: a gate is only as good as the code it delegates to

Heading case is now a `qa_page.py` gate. `check()` calls
`titlecase_headings.check_headings()` — the same call the tool's own `--check` mode makes —
so the gate and the fixer are one rule and cannot drift apart. `--self-test` grew seven
fixture cases for it, both directions on the same gate (a gate that always passes fails the
`False` cases, one that always fails the `True` ones), and they cover the two exemptions the
rule claims: an `<h1>` in sentence case must pass, and a quoted source term keeps the print's
case while the rest of its heading is still title-cased. The rule itself is written into
`harness/docs/CONSTRAINTS.md`, which was an empty stub until now, so a drafting session meets
it before writing rather than in a red gate afterwards.

Measured, not asserted: the nine shipped pages go from 29/29 to 30/30 gates, all pass;
`titlecase_headings.py --check` still reports 0 on all nine; `--all-series` still exits 1 for
one reason only, the unwritten hub (`MISSING website/tesla-1894.html`, feature-012), which is
what it did before this change. `--self-test` passes.

Two defects found in the tool the gate now leans on, both fixed here because a gate that
proposes a wrong fix is a gate nobody trusts:

1. **The quoted-source-term exemption was in the task description and not in the code.**
   `titlecase('"a tale of woe": why the machine was hard')` returned
   `'"a Tale of Woe": Why the Machine Was Hard'` — the leading quote blocked capitalisation of
   the first word (`_cap` only touches tokens that start with a letter) while the interior
   words were capitalised, so the output was neither the print's case nor title case. That is
   not a style nit: `check_quotes.py` checks quotations against the printed text, so a
   title-cased quotation stops being the quote it is quoting. The retrofit shows the cost —
   article 11's draft heading is `## "A tale of woe": why the machine was hard` and the shipped
   page reads `"A Tale of Woe"`. Fixed with `QUOTE_SPAN`: a quotation is left verbatim, and
   only the quotation. An opening quote counts only when it is not stuck to a word, which is
   what keeps `Tesla's` and `Don't` from reading as quotations.
2. **`_split_token` doubled a token that is nothing but punctuation** (a lone em dash came back
   as two), because the trailing-punctuation run was searched for in the whole token instead of
   in what the leading run had not taken. Unreachable on a series page — `qa_page.py` already
   forbids em/en dashes anywhere in the article body, headings included — but the gate prints
   the tool's proposed replacement, so the fix went in with the gate.

**Open, named rather than fixed: the retrofit stopped at the rendered pages.** The nine pages
were retitled by hand; the ten drafts under `new_content/1894-series/` were not — 72 `##`/`###`
lines still sentence case (counted at this task with the tool's own `titlecase()` over the
draft headings; none of those headings contains inline markup, so the count is clean).
`make_article.py` renders from `article.md`, so the next re-render puts sentence case back and
the new gate fails a page that passed last week — and a re-render is already planned:
feature-009/t2 re-renders 02 and 04 to close the reciprocal pair. This needs its own row, not
a drive-by at a gate task: the enforcement point for a generator-written page is the artifact
the generator writes from, or the check has to run after every render. Lesson: when a brief
says "the rule as implemented", read the implementation — the brief described an exemption the
code did not have, and the description of a rule and the code that applies it drift exactly the
way a page copy and its register do.

## 2026-10-16 — feature-006/a08-qp2: a count without its method is a claim the draft will copy wrong

Article 08's quote pin, batch 2 (entries 4-6, printed pp. 424-447) was already written to the
working tree when this task picked it up: 35 quotes, 38 fragments, 17 printed pages, and
`gen_quotes.py` exited 0 on a byte-identical re-run. What it was not was checked. Four claims
in its prose did not survive a re-check against the tools, and all four were about numbers:

1. **"'Curie' is 0 hits in the whole volume."** It is 0 *exact* hits. `grep_quote.py --count`
   returns 4, every one a fuzzy match on the words 'cured' and 'curved' (printed pp. 69, 453).
   The substance was right — the volume never names the effect — and the number was wrong,
   because `--count` is substring matching with a fuzzy fallback and nobody had read the page
   list. A pin's counts are the numbers the draft is allowed to print, so a count stated
   without its method is a claim that will be copied into a public page.
2. **"the fifth 'magnetic gener' hit is the ch. XXXVI heading mis-OCRd as 'PYRO-MAGNETIC
   RATORS'".** The heading on scan file 442 is complete; it is the *contents-page* line at scan
   file 17 that the OCR truncates. The heading is missing from the tool's default count only
   because `load_pages()` strips page-opening display type as furniture — `--keep-furniture`
   returns 5 hits and names printed p. 424, which is exactly what Appendix D reports. Appendix D
   was right and the tool's default index was not. Lesson for anyone citing a count as a
   rebuttal to the plan: check which index the tool used before calling the plan wrong.
3. **"a quote beginning at 'a pyromagnetic generator of electricity' does not verify"** — it
   verifies exactly, through the pin's own matcher, because the footnote digit the print hangs
   on 'electricity' does not break a substring match. A guessed failure is as bad as a guessed
   quote: it silently removes material the article could have used.
4. **Six notes pointed at Rejected rows and flags that had not been written** ("see Rejected",
   "see the flag"). In a hand-written file that is a TODO; in a generated file it is a
   contradiction, because the file claims to be complete. The rows and flags are written now
   (#17-#22 and six batch-2 flags), and the header's own claim about `check_quotes.py` on a pin
   file was measured rather than remembered (107 problems on this file, 84 of them the scanner
   reading apostrophes in the annotations as quote marks).

The correction is recorded inside the generator (`BATCH2_CORRECTED`), not bolted onto the
rendered file, so the next batch inherits it and the pin still regenerates byte for byte.
`gen_quotes.py` remains the gate for a pin; `check_quotes.py` is not, and the file now says why
with numbers. Lesson: when a task arrives with the work already done in the tree, the work is
the re-check — re-grep a sample through the independent CLI, re-run every count the file prints,
and follow every internal reference the file makes to itself.

## 2026-10-17 — feature-006/t1 (article 08 draft batch 1): a word count and a page cite pull in opposite directions

`new_content/1894-series/08-tesla-weird-inventions-1894/article.md` now exists: entries 1-3, front
matter with the two modern sources the register demands, and 17 quote fragments taken only from
`quotes.md`. `check_quotes.py` on the draft: 17 fragments, 17 verbatim and page-cited, 0 problems
(one through the space-ignoring index, the glued 'isvaried' the register already annotates). Three
findings that outlive the three entries.

1. **`titlecase_headings.py` lowercases an article in the second position, so a numbered heading
   that opens with one fails the gate the series just built.** The number is the first token, so
   "The" in `3. The Electrolytic Registering Meter` is a middle word, and a middle-word article
   goes lowercase: `titlecase()` returns `3. the Electrolytic Registering Meter`. Verified against
   the tool, not from its docstring. The fix is to write numbered headings without a leading
   article — `3. Electrolytic Registering Meter`, which is also the book's own chapter name — and
   to check every heading against `titlecase_headings.py` **while drafting**, which is what
   feature-006/a08-titlecase exists to stop needing. Applies to the six remaining entries of this
   page and to any numbered heading on any page in the series.
2. **The brief's ~130 words per entry and the rule that every quoted run must be verbatim and
   page-cited fight each other.** Three quotes, their three `(1894, p. N)` citations and the
   connective prose come to roughly 145 words before a single word of argument. The entries landed
   at 150/149/148, and the overage is not padding: entry 1's "why it lost" *is* the synchronism
   sentence (printed p. 412), entry 2's honesty *is* the book's own hedge on its novelty (printed
   p. 419), entry 3's *is* the reversal step and the editor's verdict (printed p. 423). Cutting to
   130 means dropping a quote, and with it the page cite the entry exists to carry. So the choice
   is written into the draft's frontmatter with the two pinned quotes that were left out, rather
   than resolved silently by shipping a thinner draft — same shape as the article 06 length flag,
   and `qa_page.py` has no word-count gate to catch any of it.
3. **Two of the nine entries cannot be written from the 1894 text alone, and a modern source has
   two rules attached.** Rejected #7 requires a modern source for any sentence putting entry 1 in a
   history of rectifiers; the flag ENTRY 2 IS THE ENTRY THAT DID NOT LOSE requires one for the
   claim that the principle won. Both were fetched (Blalock, *IEEE Power and Energy Magazine*,
   Nov/Dec 2013; Jonsson and Johansson, *ABB Review* 3/2009) and each is listed in the front
   matter beside the sentence it supports. Rule one: a modern source is paraphrased, never quoted —
   `check_quotes.py` matches every double-quoted run in the body against the 1894 text, so a modern
   quotation in quotation marks is a FAIL by construction, which is why article 06 paraphrases its
   ASU and *Scientific Reports* sources too. Rule two: the modern claim is scoped to what the
   source says. The ABB article supports oil-impregnated paper's share of the high-voltage bushing
   market and the void-free reason for vacuum impregnation; it says nothing about a household
   capacitor, so the draft makes no claim about one, and the brief's hook "the reason your
   capacitor is not in air" stays out of the entry.

One deferral, written down where the next batch will read it: the register's flag PART III IS NOT
ALL THE COMPILER'S PROSE requires the page to say once and early that chs. XXXIII-XXXVIII are the
compiler's third-person prose. Entry 1 was written without that sentence to stay near the length,
and the draft's front matter names the intro (feature-006/a08-draft3) as the place it goes and
lists the quotes that prove it. A deferral is only safe when it is written down; an unwritten one
is indistinguishable from a forgotten one.

## 2026-10-17 — feature-006/a08-draft2 (article 08 draft batch 2): the quote tool can fail a sentence whose quote is right

Entries 4 to 6 are in `new_content/1894-series/08-tesla-weird-inventions-1894/article.md`, written
from the register's batch-2 rows (chs. XXXVI, XXXVII, XXXVIII, printed pp. 424-447). All three
passed `check_quotes.py` and `titlecase_headings.py` on the first run; the things worth recording
are the three places where a tool or a count disagreed with what the draft had written.

- **A short quoted run in front of a long one breaks the long one.** Entry 6 first read
  `he writes of himself as "the writer": "as far as records go, ..."`. `check_quotes.py` pairs
  double quotes in order, so the 10-character `the writer` fell under its 12-character fragment
  floor, consumed one quote mark, and then paired the *closing* mark of that phrase with the closing
  mark of the p. 390 quote. The fragment it tested therefore began with a quotation mark, scored
  0.995, and FAILED - on a sentence that greps at ratio 1.0 through the CLI
  (`grep_quote.py 'as far as records go, he seems to have been the first who has successfully
  regulated machines' --page 390-390`, and the full sentence, both 1.0). Two rules came out of it.
  First: when the tool fails a quote, run the same string through `grep_quote.py` before touching
  the source; a FAIL can be a pairing artifact, and `check_quotes.py`'s own docstring warns against
  rewriting a source to satisfy it. Second: when the source is right and the pairing is the problem,
  the fix is our punctuation, not the print's - a short quoted term in front of a long quote has to
  use single quotes, or none. The register's rule that a quote cut by ` ... ` must be cut over a
  corrupt scan and not over a real word also got a working example: the p. 390 cut skips over the
  mechanism the entry has just paraphrased, which is the shape the rule means.
- **A substring count is not a word count, and the register said so before I found it.** The
  register's flag WORD COUNTS ARE SUBSTRING COUNTS, SO AN ABSENCE SENTENCE HAS TO RE-RUN ITS OWN
  COUNT AT DRAFT TIME predicted the failure on the first re-run
  (`books/tmp/f06a08d2/counts_rerun.out`): `output` and `trial` are not 0 in printed pp. 424-431 -
  one each, both at p. 429, `meaning larger output` about a design and `earlier trials` about
  somebody else's work - so entry 4 says *neither machine is reported built, run or measured, and no
  efficiency figure appears in the chapter*, which is a claim about what the chapter reports and not
  about which words occur in it; and `test` is 1 in pp. 432-437 only because `greatest` contains it. Absence
  sentences are ours, never the 1894's (Rejected #21 and #22), and their scope has to be the scope
  the count actually covered.
- **A cheap scan is worth running before a "no other" sentence.** Entry 6 says the 1885 date is the
  only year in the six chapters entries 1 to 6 come from. That was measured, not recalled: split the
  extracted text on its page markers, take scan files 427-465 (printed pp. 409-447), list every
  four-digit year (`books/tmp/f06a08d2/years_scan.out`) - exactly one, 1885, at printed p. 438.
  Three lines of Python turn a sentence that would otherwise be a hunch into one with a method.
- **The brief's hooks are leads; the register's flags are what makes them safe to use.** The §9
  brief 08 hooks for entries 4 and 5 were both wrong in ways the register had already written down:
  "400 to 500 times a minute" is the compiler's footnote about a horseshoe-magnet bench experiment,
  not a machine's speed, and the same footnote says the chapter's own devices vibrate "very slow";
  and "the problem every DC motor had" describes a commutator fault that the print places in
  high-EMF direct-current dynamos used for arc lighting. Both hooks are now in the article, in the
  form the print supports, because the flag told the draft which form that was.
- **A cross-chapter quote drags the front matter with it.** Entry 6's priority claim is at printed
  p. 390, in ch. XXIX - the author's own chapter, writing about himself in the third person, with
  both of his own hedges ("as far as records go", "seems") inside the marks. That made p. 390 a
  page the page cites, so `pages_used` and the `sources:` block had to grow to cover a Part II
  chapter, and the sources row says plainly that it is not Part III. Article 11 (feature-007) is
  built on the same chapter and says nothing about that voice, so the two pages do not contradict
  each other today; the front matter records that if either page ever describes the voice, both have
  to be checked together. A quote borrowed across an article boundary is fine; the metadata boundary
  has to move with it, or the Sources block stops describing the page it sits on.

Deferred, written where the next task will read it: entry 4's 600 degrees centigrade stays out until
a modern source is carried beside it (the register's flag THE BOOK'S 600° IS NOT THE CURIE POINT);
entry 5's devices get no year, because the chapter prints none and §6.3 needs a patent record; and
the six entries now run 148-156 words against the brief's "roughly 130", which is the same length
flag article 06 carries into VERIFY. `check_quotes.py` reports 27 fragments, 27 verbatim, 0 problems
for the whole draft (`books/tmp/f06a08d2/cq_final.out`, exit 0) - batch 1's 13 plus this batch's 14,
which is the arithmetic the sentence above it gives; the 26 first written here was a miscount of the
same output, and it is corrected rather than left as an example of the thing this lesson warns about.

## 2026-10-17 — feature-006/a08-draft3 (article 08 draft batch 3): a nine-entry listicle does not fit the H2 gate

Entries 7 to 9, the Part III provenance paragraph and the closing beat are in
`new_content/1894-series/08-tesla-weird-inventions-1894/article.md`, written from the register's
batch-3 rows (chs. XXXIX, XL, XLI, printed pp. 448-474). `check_quotes.py` reports 45 fragments, 45
verbatim and page-cited, 0 problems for the whole draft (`books/tmp/f06a08d3/cq_final.out`, exit 0):
batch 1's 13, batch 2's 14, this batch's 18. The finding worth carrying to the next listicle is a
structural one, and it only showed up because the draft was rendered before it was handed on.

- **Nine entries cannot be nine H2s.** §9 brief 08 asks for nine entries; §12 asks for `H2 count
  5-9`; `qa_page.py` counts `<h2>` in the whole rendered page (line 177) and the donor shell
  contributes none, so the draft's own headings are the entire count - and `make_article.py` adds
  one more for the Sources block. Eleven draft H2s rendered as twelve and failed. Nine entry H2s
  cannot fit whatever the intro and closer do, so the brief and the gate cannot both be honoured by
  nine H2s, and the gate is the referee. The fix is grouping, not cutting: three H2s that are the
  volume's own chapter blocks (chs. XXXIII-XXXV, XXXVI-XXXVIII, XXXIX-XLI), nine numbered H3 entries
  under them, intro and closer as H2 - six H2s rendered, inside the band, with all nine entries and
  their order intact. Article 09 is the precedent: its brief lists nine structure items and it
  shipped with six H2s and four H3s. The grouping follows the book's chapter blocks so it is the
  book's structure, not an invention, and the intro says so in one sentence rather than leaving a
  reader to infer why the headings change level. Lesson: render the draft before handing it to the
  render task. `make_article.py --out books/tmp/...` (the `--out` basename has to match the front
  matter slug) plus `qa_page.py` on the output costs two minutes and found a failure that would
  otherwise have arrived as a t3 rework.
- **A numbered heading must not open with an article.** `titlecase_headings.py` treats `7.` as
  punctuation around a numeral token, so the word after it is not in first position: it wanted
  `7. a Dynamo Frame Cast in Two Identical Halves` and `9. the Disc That Makes Direct Current
  Without a Commutator`. Rather than ship headings that read wrong and let the tool lowercase an
  article on the page, the two headings were reworded in the draft to say the same thing without an
  opening article (`7. One Frame Pattern, Cast in Two Identical Halves`, `9. Discs That Make Direct
  Current Without a Commutator`). CONSTRAINTS.md already says the rule bites in the draft, not the
  page - `make_article.py` renders from it - and `titlecase_headings.py --check` on the rendered
  smoke page now reports 0, which is what feature-006/a08-titlecase has to confirm.
- **A scope sentence has to name the whole set.** The intro's voice disclosure first read "six of the
  nine chapters, printed pp. 409 to 447, are the editor writing about his subject in the third
  person". That is true of the six it named and misleading about the other three: the register's own
  chapter list calls ch. XXXIX "the compiler's prose again" and ch. XL "the compiler's prose", and
  only ch. XLI changes voice, partway down printed p. 467. Entries 7 and 8 are third-person prose
  about Tesla too, so an intro about whose words these are had to say eight, not six. Same shape as
  batch 3's correction to the pin: the quotes were right, the scope was wrong.
- **A source URL can fail a gate it was never meant for.** §12's "no book-PDF link" is implemented
  as a substring test for `.pdf` anywhere in the page, and the ABB Review citation batch 1 added for
  entry 2 ends in `.pdf`. The page fails D4 on a journal PDF that is not the book. That is an owner
  call - drop the URL, or find a non-`.pdf` location for the same article - so it is recorded in the
  front matter with both options and not fixed by quietly deleting a citation.
- **A count belongs to its method.** The per-entry counts are unchanged by the H2/H3 change (150,
  149, 148, 156, 153, 156, 173, 180, 176), but the script that produced them split on `##` and had
  to split on `##` and `###`. The new script reproduces batch 1's and batch 2's numbers unchanged,
  and that reproduction is the check that the new method measures the same thing
  (`books/tmp/f06a08d3/len_check.py`, output at `len_check.out`). The body measured 2,034 words at
  that point, 2,003 after the length pass below,
  against the brief's 1,500 - the same length flag article 06 carries into VERIFY, larger by the
  provenance paragraph and the closing beat, which are not in the brief's per-entry budget and are
  where the register's voice disclosure and §9's closing beat live.
- **A draft batch is measured against the batches before it, not only against the brief.** Batch 3
  handed over entries at 173, 180 and 176 while the six already in the file ran 148 to 156. Every
  entry misses the brief's "roughly 130", and that flag goes to VERIFY as article 06's did; the
  nearer complaint is this task's own criterion, "the same length", and 11 to 15 percent over the
  band the earlier batches set is a different thing from 14 to 20 percent over a brief. A pass over
  this batch's connective prose - ours, not the volume's - brought the three to 165, 162 and 171, 4
  to 10 percent over that band: "and closes by widening the claim" and "It also says the frame
  suits" gone, "the polyphase machinery of" reduced to "set out in" over the same article 07 link,
  a comma turned into a colon, and the p. 464 lamp quote taken as its first clause only. The p. 474
  belt-contact sentence was not touched: the closing beat's "until their inventor ran out of time"
  rests on that sentence, so cutting it there would unmoor a claim the page makes, and the full
  p. 464 run stays in quotes.md for whoever wants it back. What did not move is the proof: the same
  `check_quotes.py` on the new bytes reports the same 45 fragments, 45 verbatim and page-cited, 0
  problems (`books/tmp/f06a08d3b/cq_final.out`, exit 0), `pages_used` still equals the set of pages
  the body cites, and the smoke render still reports 26 of 28 with the same two deferred failures
  (`books/tmp/f06a08d3b/tesla-weird-inventions-1894.html`, `qa_smoke.out`). Lesson: cut your own
  words before you cut a quote, then re-run the quote tool, because a shortened quotation is a
  different quotation and a shorter entry is only safe if the page cites still land where the tool
  can see them.

Deferred, written where the next task will read it: the CTA sentence is front matter and this file
has no `cta:` key, so `{{CTA}}` renders an empty alert box and no plan task owns it (`qa_page.py`
does not look for a CTA, so t3 will not catch it); §9 brief 08 asks for no FAQ, as brief 09's did,
so `faq: []` is the brief as written; the reciprocal-links gate fails because nothing links to this
page yet, which is feature-006/a08-wirecommit's in-link work; and the ABB `.pdf` URL above. The
smoke render reports 26 of 28 gates with only those two failures
(`books/tmp/f06a08d3/tesla-weird-inventions-1894.html`, `books/tmp/f06a08d3/qa_smoke.out`).

## 2026-10-17 — feature-006/t2 (article 08 figure evidence): a record that says it did a thing is not the doing

The figure work was already on disk when this task was picked up: four 500 ppi renders, three
published crops, eight evidence crops, and a front-matter record in article 08 that reads like a
closed task. Three things that record asserted were not true, and each was found by checking the
file it names instead of re-reading the prose.

- **"All three notes are corrected in `manifest_qc.csv` at this task, in the site repo."** That file
  had not been touched: `git status` clean, mtime Oct 11. The three corrections (row 149's Fig. 220
  subject line, row 156's "coherer" comparison for a meter figure, row 157's incomplete description
  of the meter plate) existed only as prose in the article. Written now, each note naming the read
  that corrects it, plus two more rows this task turned up while checking: row 158's "Figure number
  281 is genuine for p.425", which that page's own three printed captions contradict without anything
  settling it, and row 161's description of the p.430 two-figure band. Rows 217-219 now carry the
  three published crops with their box, sha256, the evidence crop that carries the read, and the row
  each supersedes — the pattern feature-004/t6 and feature-005/t2 set, and the omission
  feature-005/a06-figrec noticed for article 06's three and never closed. Article 08's three are in;
  article 06's three still are not, and that is still open.
- **"A crop exists and is keep/A (row 176)"** for the p.430 band. Row 176 is `p464-fig1-fig266.webp`
  on printed p.446. The band is row 161 of both manifest files. Every other row reference in that
  record (149, 156, 157, 158, 163) is a line number in `manifest_qc.csv` and is right, which is
  precisely why the one wrong number would not be caught by anyone who had learned to trust the
  others. The record now names the row and says what row 176 actually is. Lesson: a row number is a
  pointer, and a pointer gets re-resolved, not re-used.
- **"the same 3-for-8 confusion this scan makes on printed p. 425 ('Fig. 281' for 231)"** was stated
  as fact in one block of the same record and hedged as "says which is likely" in another. Neither
  page was re-opened, so neither is settled; the disagreement on p.425 is internal to one page (three
  printed captions against one body line), which is a reason to flag it and not a reason to publish a
  verdict. Both places now hedge the same way and say why — §6.6 re-opens a figure whose evidence is
  missing or contradicted, and this one is neither.

What checking rather than trusting bought, beyond the corrections: **every crop in this record
re-derives.** All eight evidence crops re-cut from the boxes in `figures/README.md` are pixel-identical
to the committed files, and all three published `.webp` re-encode byte for byte at
`quality=88, method=4` (21,236 / 40,390 / 73,692 bytes, sha256s matching the table). That is more
than article 06's record claims — five of its eight evidence crops have no recorded box. Opening the
four caption crops confirmed `FIG. 220.`, `FIG. 227.`/`FIG. 228.`, `FIG. 230.` and
`FIG. 242.`/`FIG. 243.`; the three published crops each carry their printed caption inside the crop;
and the Fig. 230 plate shows the R' and R'' coils, the round instrument G in the line conductors L L
and the seven-contact bank T that row 157's subject line omits — which is how that row's note got
written from the plate and not from the earlier note. Lesson: a box and a hash are only worth
anything if someone re-runs them; the re-run is the test, and it costs one script.

Two tool facts worth carrying:

- **`manifest_qc.csv` is CRLF.** Reading it in Python text mode and rejoining with `\n` rewrote all
  216 lines and buried a five-row change in a 435-line diff. Read and write with `newline=""` and
  split on `\r\n`; the diff is then 8 insertions and 5 deletions, which is what a reviewer can
  actually read. Lesson: check the line endings of any file you regenerate, especially a CSV another
  script writes.
- **`extract_figures.py` returns 0 figures for a page whose engraving sits inside a claimed text
  block** — scan 436 / printed p.418 at both 300 and 500 dpi, because the tool masks every row the
  text layer claims. A zero from that tool is not evidence that a page has no plate. It is why entry
  2 had no crop and no row: the gap in the record was a tool limit, not a lost file, and the caption
  band crop is the only proof the plates were ever there.

Re-rendered after the front-matter edits, because a front-matter comment block is still front matter:
`make_article.py` → `books/tmp/f06t2b/tesla-weird-inventions-1894.html`, 1 h1 / 6 h2 / 9 h3, 3 series
figures; `qa_page.py` 27 of 29 with only the two already-deferred failures (reciprocal links, which
is feature-006/a08-wirecommit's in-link work, and the ABB `.pdf` url, an owner call at t3);
`check_quotes.py` 0 problems; `pages_used` still exactly the 27 pages the body cites. The earlier
"26 of 28" in the draft record is not comparable to this "27 of 29": `qa_page.py` line 304 only
adds the `2-3 figures in <figure class="mb-4 pt-5">` gate when the page references
`assets/tesla1894/`, so the figure-less draft was scored against 28 gates and this page against 29.
Same two failures, one new gate that passes. Lesson: a gate count is a function of the page, not a
constant of the tool — quote the count with what the page contains, or re-measure it before writing
it down.

## 2026-10-17 — feature-006/t3 (article 08 render + numeric gates): a gate that reads the site graph changes when the page moves into it

The same bytes scored 27 of 29 at the `feature-006/t2` smoke render
(`books/tmp/f06t2b/tesla-weird-inventions-1894.html`) and 29 of 29 at this task, in
`website/`. Nothing about the page changed between those two measurements except where it
lives. Two of the three deferred failures the earlier record named were wrong as predictions:

- **The reciprocal-links gate.** The smoke render reported `reciprocal: []`; the real page
  reports 36 reciprocal links and passes. `qa_page.py`'s `inbound_map()` walks `website/`, and
  once the page is inside `website/` it is in its own inbound set — the shared shell links to
  `/about`, `/contact`, `/articles` and the rest on every page of the site, and the page under
  test carries that same shell, so it satisfies the gate against itself. Measured directly:
  `tesla-weird-inventions` is in its own inbound set for `about`. This is the vacuity
  `feature-004/t7` already recorded, and it is left alone for the reason that record gives:
  fixing it would fail 01, 02 and 04 too, and that is an owner call. Lesson: **a gate that
  reads the site graph is not measured by a render outside the site graph.** A deferred failure
  carried forward from a smoke render has to be re-measured at render time, not copied — and a
  gate that *passes* is not a gate that is satisfied. The truth for this page is unchanged:
  three out-links placed and resolving, zero in-links from anywhere, and §5.2 is still
  `feature-006/a08-wirecommit`'s work and the hub's.
- **D4, `no book-PDF link`,** did fail, and not for the reason its name gives. It is a plain
  substring test for `.pdf` anywhere in the page, and what tripped it was a journal article:
  the ABB Review source row carries a url ending in `.pdf`. The draft left the choice to this
  task — drop the url, or find a non-`.pdf` address — and the second was measured before it was
  rejected: `curl` returns 200 for the `.pdf` itself, 403 for the `library.e.abb.com` public
  path with the file name removed, 403 for a guessed `66-70.html` at the end of that path. So
  there is no non-`.pdf` location for that article, and inventing one was the one thing not to
  do. The url line is off the row; the citation keeps authors, title, journal, issue and pages;
  the `.pdf` address stays in a front-matter comment so the source is still findable.
  `qa_page.py`'s D4 is left exactly as it is — narrowing a substring test to "the book PDF" is
  a tool change, and a page render is not where to make it. Lesson: **when a gate's test is
  broader than its name, the page passing is not the gate being right.** Say which one was
  worked around, or the next page inherits the same trap with a clean bill of health.
- **The empty CTA block is the one defect on this page that no tool sees.** `cta_block()` emits
  `c.get("text","")` unchecked, so a draft with no `cta:` key renders an empty
  `<p class="mb-2">` inside the alert box; `qa_page.py` has no CTA gate, so 29/29 says nothing
  about it. It was flagged at `a08-draft3` and again at `a08-figrec`, both times writing that it
  needs a plan row rather than a drive-by, and no row was ever added — which is how a defect
  survives three tasks. Lesson: **a flag that needs an owner is not filed until it has a row.**
  `feature-006/a08-cta` was added at this task, after t3 and before `a08-wirecommit`; the CTA
  sentence itself was not written here, and no other page's CTA was copied.

Measured and recorded rather than fixed, because none of it is this task's: the length overrun
(the draft's own `len_check.py` method gives 2,003 words against brief 08's 1,500, and
`qa_page.py` has no word gate, so 29/29 does not mean the length is right), the date ordering
question `a08-figrec` raised, the missing `assets/og/` file (`feature-010/t2`), and the §5.2
in-links. `--wire` was deliberately not run: the sitemap entry, the llms.txt line, the
`_redirects` pair for the `/tesla-weird-inventions` alias and the articles.html card belong to
`feature-006/a08-wirecommit`, which has two known tool defects waiting for it there.

Two facts worth keeping about the render itself: `make_article.py`'s "internal links: 1" line is
not the page's link count — it subtracts every href the donor shell carries, and two of this
page's three body out-links are also in that shell's sidebar. And the render is reproducible:
re-run to `books/tmp/f06t3/` and `cmp` says byte-identical to the committed page, which is the
check to run after editing front matter, since a front-matter comment is still front matter.

## 2026-10-17 — feature-006/a08-wirecommit (article 08 wiring and final commit): a wiring task is mostly a decision about where the page sits

The four artifacts this task names are small. The two decisions under them are not, and
neither was in the task text.

- **The publish date, settled by measuring the invariant rather than by picking a date.**
  `a08-figrec` wrote that the draft's `date_published: 2026-10-17` would make "the card
  grid read out of order" and left it here. Before choosing, the order was read off the
  nine rendered pages: 03 10-14, 09 10-16, 11 10-17, 07 10-18, 01 10-19, 02 10-20,
  04 10-21, 05 10-22, 06 10-23, and `articles.html` in exactly that order. So the grid
  has two properties, not one: dates ascend, **and** card order is wiring order. Keeping
  10-17 and inserting the card between the 11 and 07 cards satisfies the first (it is
  also inside §11's "never more than 2 in a day"), and breaks the second. Taking the
  next date, 10-24, satisfies both, and this page is the tenth wired, so the arithmetic
  picks it. Lesson: **when a record says "X would read out of order", go and measure
  what order it is actually in.** A vague worry about ordering becomes a decision the
  moment the invariant is written down; without it, both options look defensible and the
  task just passes the problem on again.
- **A front-matter change at a wiring task is only safe because the render was proved
  reproducible first.** Before editing anything, `make_article.py` was run on the draft
  exactly as `feature-006/t3` left it, into `books/tmp/f06wire/`, and `cmp` came out
  clean against the committed page at 45,641 B. That is what let a date be changed here
  rather than re-opening `feature-006/t3`. After the edit the diff is five lines (two
  `article:*_time` metas, two JSON-LD date fields, one visible date line) and the byte
  count is unchanged, which is the proof that no layout moved and that the t4 visual
  record still describes the page. Lesson: **a text-only change can be proven, not
  assumed, not to invalidate a visual record: diff it and compare byte counts.** Re-run
  the expensive gate when the diff says the pixels can move; do not re-run it, and do
  not ignore it, when the diff says they cannot.
- **The `_redirects` pair is the first rule this series has ever needed, and the order of
  writing it matters.** Articles 01 to 06 set `pretty_slug` to their own file name, so
  `redirect_rules()` returns `[]` and there is nothing to write; that is why eight dead
  rules were deleted once and never re-added. Here the alias differs from the file name,
  which is the only condition on which a rule fires. The pair was written by hand, with
  the section comment rewritten to name the two rows of the §5.1 table that need a rule,
  **before** `--wire` ran, so `wire_updates()` reported "already present" for both
  instead of appending them under the removed-pages block. Then the whole file was
  checked mechanically: 56 rules, 0 duplicate sources, 0 rules whose source is an
  existing page. Lesson: **a config file's correctness is a measurement, not a claim**,
  and hand-editing before the tool runs is how you keep the tool's idempotence check
  doing your placement work for you.
- **A workaround applied four times is a defect with no row.** `--wire` wrote the
  `llms.txt` entry cut at 150 characters, as it has on every page since `feature-004/t4`
  named it, and the line was rewritten by hand for the fourth time (01 to 06 and now 08);
  07, 09 and 11 still ship truncated lines. Lesson: **counting how often a workaround is
  applied is how you decide it is a tool task**, and saying "still unfixed" in three
  entries is not filing it. It is named in `blocked_on` with the count, because no row
  owns it and this task is not the place to change the tool.
- **Before patching a gap, check whether it is local or graph-wide.** This page has no
  body in-link, which is what §5.2 says it needs. Measured across every series page that
  exists: `tesla-wireless-power-1893.html` and `tesla-cold-flame.html` have zero too, and
  several want in-links from pages that have never been written. Placing the 03 to 08
  link here would have meant re-opening `feature-003`'s draft, re-rendering a page whose
  visual record describes it, and re-running its gates, to fix one edge of a graph-wide
  gap on my own initiative. It is recorded with the numbers and named to `feature-009`,
  whose own description is the in-link requirement. Lesson: **the measurement is what
  turns "not my scope" from an excuse into a finding.** An unowned gap that is graph-wide
  belongs to the row that owns the graph; a gap that is only yours is yours to fix.
- **A pending row can already be met, and that is worth saying without closing it.**
  `feature-006/a08-titlecase` is still open. `titlecase_headings.py --check` on the draft
  reports 0 headings not title case, exit 0, and the rendered page passes
  `qa_page.py`'s heading-case gate. It is recorded in `blocked_on` with the command, and
  not marked complete, because it is not this task's row. Lesson: **measure a pending
  row's criterion before anyone does its work**, and leave the closing to the row that
  owns it.
- **The card grid's order is checkable, so "the card is in the right place" is not an
  opinion.** `books/tmp/f06wire/card_order.py` lists all 31 cards on `articles.html` in
  DOM order with their date lines at 1280 and 375: the ten series cards read October 14
  through 24 ascending, this card is index 9 of 31, immediately after `tesla-cold-flame`
  and immediately before the first legacy card. `card_shot.py` measured the card itself
  (no clipping, no horizontal overflow, equal columns) and both crops were read, plus the
  row crop, which is where the grid actually shows. Lesson: **a layout claim about an
  index page should come with the DOM order and the two widths**, the same way a figure
  claim comes with a crop.

Re-measured rather than carried: `qa_page.py` on the new bytes, 29/29 exit 0;
`--all-series` 10 of 11, exit 1, the 11th MISSING the unwritten hub, and the other nine
pages unchanged at their own counts, which is the check `feature-006/t3`'s lesson says to
re-run whenever a page moves into a gate that reads the site graph. Carried forward
unchanged and still not this task's: the length overrun, the missing OG image, the empty
CTA block and the wrong figure alt (both `feature-006/a08-cta`, re-checked here: line 226
still renders an empty paragraph, the draft still has no `cta:` key, "three dark vertical
strips" still appears once), the nav-dropdown overflow on all 39 pages, and
`shot_qa.py`'s `-mobile-fold.png` not being the first screen. No push in either repo.

## 2026-10-17 — feature-006/a08-titlecase: a page-level check does not prove the draft is clean

This row was already met before it was picked up — `feature-006/a08-wirecommit` measured that
and said so without closing it. It was re-measured, not redone, and nothing on the page or in
the draft body changed: `titlecase_headings.py --check` reports 0 headings on
`website/tesla-weird-inventions-1894.html`, exit 0, and the same on a fresh render of the
current draft bytes. All three commands and their exit codes are at
`books/tmp/f06a08tc/titlecase_check_final.out`. Three things outlive the row.

- **A rendered page can pass a heading gate while the artifact that generates it still fails
  it, and the tool cannot even see the artifact.** `titlecase_headings.py` matches `<h2>` and
  `<h3>` tags; a markdown draft has `##`/`###` lines, so pointing the tool at `article.md`
  scans nothing and reports success. The only honest draft check imports the tool's own
  `titlecase()` (one rule, no second implementation to drift) and applies it to the draft's
  heading lines — `books/tmp/f06a08tc/draft_titlecase_check.py`, which also compares the
  draft's heading strings to the page's h2/h3 text so the two records are shown to be the
  same list, and `cmp`s a fresh render against the committed page to show the page is what the
  current tool makes from those bytes today. Article 08: 14 draft headings, 14 title case,
  page = those 14 plus the `Sources` H2 `sources_block()` adds. Lesson: **check the rule at
  the place the generator reads from**, and if the tool cannot read that place, say what you
  actually ran.
- **The open item `feature-001/heading-case-gate` left on 2026-10-16 is still open, and it now
  has a count.** That entry closed with "the retrofit stopped at the rendered pages: the ten
  drafts were not retitled", and nothing has touched them since. The same `titlecase()` over
  every draft in `new_content/1894-series/` returns 11 drafts, 87 h2/h3 lines, **72 not title
  case** (`books/tmp/f06a08tc/other_drafts_titlecase_scan.out`) — the same 72 that lesson
  counted, unchanged. Article 08 is the only clean draft in the series, because its batches
  wrote to the rule from the start. Every other series page was retitled on the rendered page
  only, so any re-render puts sentence case back and fails `qa_page.py`'s heading-case gate on
  a page that passed last week. Named, not fixed: it belongs to `feature-009/t2` (whose §5.2
  out-link work re-renders 02 and 04, 7 lines each) and `feature-012/t1` (the hub draft, 8 of
  its 9 lines); the other 50 lines sit in drafts no row re-renders today. Fixing it is one
  command per draft — `titlecase_headings.py` cannot do it, because of the tag problem above,
  so whoever owns it needs the draft-level pass written once. Lesson: **an open item with no
  row is a number waiting to be re-measured**, and the second measurement is what turns it
  into a finding nobody can call stale.
- **A conditional acceptance criterion still needs a measurement, not a shrug.** "every FAQPage
  `mainEntity` name matches its visible h3 exactly" is vacuously true on this page: `faq: []`
  in front matter, 0 `FAQPage` blocks in the page, 0 names, 0 findings — which is what §9 brief
  08 asks for (§7 emits `FAQPage` only "when `faq` present", and article 09 shipped the same
  way). Recorded with the count rather than as "n/a", because a criterion written as a
  universal is indistinguishable from an unmet one until something counts the set. The h1 half
  was measured the same way: h1 and its `title`/`og:title`/`twitter:title` mirrors are four
  identical strings, and this task changed none of them — the register edit is front-matter
  comment only, and the re-render after it is byte-identical, which is the proof that claim
  carries rather than asserts.

## 2026-10-18 — feature-007/a10-wirecommit (article 10 wiring and final commit): a wiring step can undo a fix you already made

The task was four config files and a date. What it actually produced was one new failure
mode of a tool line this series has named twice already, and a rule about when a re-render
owes a re-shoot.

- **`make_article.py --wire` re-renders the page, and that silently reverted a fix I had
  already applied.** The render was clean: `titlecase_headings.py` retitled the
  sentence-case `Frequently asked questions` H2 that `faq_block()` (line 420) emits, and
  `qa_page.py` on the page reported 30/30, exit 0. Then `--wire` ran, wrote the same page
  out again from the draft, and put the sentence-case heading back. The single-page gate run
  was not wrong when it ran — it described the bytes that existed then — and it could not
  see a change that happened after it. `qa_page.py --all-series` found it afterwards: this
  page FAIL 29/30, naming the heading-case gate. Retitled, `--check` 0 findings, 30/30 exit
  0, and `--all-series` 11/12 with the unwritten hub the only failure. Lesson: **a gate
  result describes bytes, not a file name, so the order of operations is part of the
  result.** Either wire first and never render without it, or re-run the gate on the bytes
  the wiring step left behind. This is the second distinct failure of one tool line: the
  first was "the generator emits a heading that fails the gate" (feature-007/t3, pages 03,
  05, 07, 10 each needed a post-render retitle), this one is "the generator can undo the
  fix after you made it". Articles 11, 12 and the hub are still coming, so the count is
  going up while nobody owns the line.
- **A caption edit is a pixel edit; the diff says which changes are, and that decides what
  gets re-run.** feature-006/a08-wirecommit proved a date-only change could be shown not to
  move the layout (five lines, byte count unchanged) and skipped the expensive gate on that
  evidence. Here the diff was five date lines *plus* 58 bytes of running text inside a
  `figcaption`, which re-wraps, so `shot_qa.py` was re-run on the final bytes and
  `books/tmp/f07wire/page_measure.py` re-measured the geometry feature-007/t4 had recorded:
  page 30,808 / 18,503 / 16,488 px (was 30,787 / 18,503 / 16,467), figure 3's caption box
  462 px at 375 (was 441), CTA band 22,082 px (was 22,061). The arithmetic closes: the CTA
  moved by exactly the 21 px the caption grew, and every figure box and ratio is unchanged,
  which is how "nothing else moved" is a measurement rather than a hope. Lesson: **the same
  rule as last time, applied honestly, points the other way this time.** Prove which half of
  a diff can move the pixels, then re-run the gates that half invalidates and say why the
  other half does not need them.
- **A count in a caption is a claim a reader cannot check unless the caption names the thing
  it counts.** The defect feature-007/t4 left for this task was "ten more entries" where the
  column has eleven. Changing the number alone would have left an unverifiable assertion, so
  the caption now also names the entry the column ends on ("Streaming Discharges of High
  Tension Coil"), which is what t4's own two measurements (a 500 ppi render of scan 514 and
  the scan's text layer) established. It cost 58 bytes and one line of caption at phone
  width, and it turns a number a reader must trust into one they can check against printed
  p. 496. Lesson: **when a QA record hands a wrong count to a later task, the fix is the
  count plus the evidence that makes it checkable**, not the count alone.
- **Before believing your own number differs from an old record, measure the old bytes and
  the new bytes in the same run.** The citation count read one short of feature-007/t4's
  (50 body-form markers where that record says 51), which looked like the caption edit had
  dropped a citation. It had not: `git show HEAD:<page>` measured with the same regex gives
  the same 50, and the missing marker is a third form the page carries, `(1894, pp. 6, 496)`,
  which the body-form regex does not match and t4's did. Counted in its own form, t4's
  numbers reproduce exactly: 54 markers inside `<article>`, 58 body-form whole-file, 61
  total, 21 distinct printed pages. Lesson: **a count is its regex; when a number and a
  record disagree, diff the regexes before suspecting the page**, and keep the old bytes
  around to diff against.
- **A workaround applied seven times is a tool defect with a count, and the count has to be
  measured, not remembered.** `wire_updates()` still cuts the `llms.txt` entry at 150
  characters. Read the section rather than the last three records: of the eleven entries in
  `## The 1894 File`, 3 are cut at exactly 150 characters (09, 11, 07) and 8 are full,
  because the line was rewritten by hand on 01, 02, 04, 05, 06, 08 and now 10. (03's entry
  is full too, but its standfirst was short enough that the tool's cut never bit.) That is
  the seventh hand rewrite in the series. Named in `blocked_on` with both numbers; the
  one-line tool change and the three stale lines belong to whoever owns `books/tools`, not
  to this task.
- **The card grid has two invariants, and a wiring task has to check both after, not just
  place the card.** Dates ascend, and card order is wiring order. `card_order.py` re-read
  all 32 cards in DOM order with their date lines and boxes at 1280 and 375 after the edit:
  the eleven series cards read October 14 through 25 ascending, this card is index 10 of 32
  between article 08 and the first legacy card, columns equal width, `scrollWidth ==
  clientWidth` at both widths. `wiring_check.py` does the same for the other three files:
  56 `_redirects` rules with 0 duplicates and 0 shadowing an existing page and 0 mentioning
  this slug (which is what §5.1 row 10 requires, not an omission), 47 unique sitemap locs
  with `lastmod` equal to the page's own published date, and the llms.txt section in wiring
  order. Lesson: **"the card is in the right place" is a layout claim, so it ships with DOM
  order, two widths, and the crop.**
- **A pending row's criterion measured before its own task can save the next one a trap.**
  `feature-006/a08-titlecase` is still open and still says what it said: every series page
  except 08 was retitled on the rendered page only, so any re-render puts sentence case
  back. This task is the first re-render of a series page since that was written, and it
  found the same thing from the other direction — the re-render did put it back, and the
  gate that had passed could not see it. The row is not closed here (it is not this task's
  row), but the measurement is in its `blocked_on` with the command and the exit codes.
