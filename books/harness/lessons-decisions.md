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
