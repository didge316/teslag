# Decisions

<!-- The REVIEW gate wants 100+ characters of real content here. -->

One entry per decision: what was chosen, what was rejected, and why.

## 2026-10-10 — Ship the hub last, not in S1 (resolves SERIES-PLAN-1894 §0.2)

Chosen: render and wire `tesla-1894.html` after all 12 articles exist. Rejected: shipping it
in week 1 with nine cards as plain text, and shipping it early with dead links. The hub's own
brief makes it an index of 12 real cards, and §12 forbids broken relative links; writing it
last removes the conflict instead of excepting a rule. Cost: the hub is the last unit, so any
series-wide defect surfaces late. Mitigated by feature-001, which makes dead links a machine
check on every page from the first article onward.

## 2026-10-10 — O1/O2/O3 taken in autopilot, all cheaply reversible

O1 series name: keep the working name *The 1894 File*. Rejected: a brand-tied name. It appears
in four non-URL places and the plan itself rates a later change as a 10-minute job, so deciding
now buys nothing and a brand-tied name undercuts the neutrality that is the series' wedge.
O2 article 10: option B, the plan's recommendation — keep it, publish after 03/01/07, softer
title. Rejected: week-1 flagship (attacks the product before the reader trusts us) and folding
the evidence into `magnetic-generator-scam.html` (that page needs a rewrite, not an addition).
O3 scarcity widget: leave the donor shell unchanged on every series page. Rejected: per-page
exceptions on 05 and 10 — the shell is out of scope (§4 non-goals) and per-page shell variants
are the kind of change that quietly breaks the shared template.

## 2026-10-10 — Branch the work repo, not the deploy repo

Chosen: `feature/1894-series-flagship` in the work repo; `website/` stays on `main`. Rejected:
branching `website/` too. `website/` is the deploy repo (pushing deploys, D6) and its `main`
is what the owner reviews and pushes; a branch there would hide the review surface without
adding safety. Every series change in `website/` is still a separate named commit so a single
legacy-page edit can be reverted alone.
