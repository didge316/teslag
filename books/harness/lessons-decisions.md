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
