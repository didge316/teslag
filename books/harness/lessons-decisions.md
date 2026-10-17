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
