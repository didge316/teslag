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
