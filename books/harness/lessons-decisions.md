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
