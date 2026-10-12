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

## 2026-10-12 — Publish on completion; canonical URLs move to extensionless

Three decisions forced by one site audit. Full plan: `SEO-URL-FIX-PLAN.md` at the work-repo root.

**Publish on completion.** Chosen: a *produced* article is deployed in the same cycle it is
produced. D6 stands — only the owner pushes, and pushing remains a named action — but "unpublished
until the owner gets to it" is no longer a valid end state for a page that has passed its gates.
Rejected: the standing default as written. Evidence: `new_content/` holds 50 unique article slugs;
10 are live, **40 are not**. `TRACKER.md` marks 40 keyword articles ✅ Done while the site never
carried them, and two of those 40 are pages the live site links to — the site has been shipping
links to articles that exist only as markdown. "Written" had quietly become the end state of the
workflow, which is also why 40 drafted articles carry no deploy-time defects anyone has seen.

**Extensionless canonicals.** Chosen: `/x` is the canonical URL, served by Cloudflare from
`x.html`; canonical, `og:url`, JSON-LD, sitemap `<loc>`, `llms.txt` and every internal link use
that string, root-absolute. Rejected: keeping `.html` as canonical. Cloudflare resolves static
assets *before* `_redirects`, so a redirect rule cannot override it — proven by the eight 1894-series
rules that never fired, which left `/x` and `/x.html` both live at 200 and `/x/` serving the
homepage at 200. That trailing-slash gap carried 76% of all impressions in the GSC export. The
glossary follows in DOMAIN.md (**Canonical URL**, **Wired**, **Published**, **Deployed**).

**No year in a slug.** Chosen: year-free slugs; a year lives in a title or the prose, where it can
be refreshed without moving a URL. Rejected: dated slugs. `magnetic-generator-plans-review-2026` was
an AI-written article the owner asked to rename because it is nearly 2027; the rename half-happened,
the file became the year-free page, and five live pages have linked at a dead slug ever since. Two
of the three pages the site links to are published from their existing drafts; the third is that
mid-rename article, so its five links are repointed to the year-free page that already exists.
