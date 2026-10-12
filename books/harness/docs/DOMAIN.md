# Domain

Glossary only. One line per term, in the words the users of this system use.

- **The 1894 File** — the series: 12 flagship articles plus a hub, all built on one 1894 first
  edition. Never in a URL.
- **Printed page** — the page number printed on the scan. Scan file = printed page + 18. Every
  citation uses the printed page.
- **Brief** — one article's self-contained spec in SERIES-PLAN-1894 §9 (title, queries, word
  target, sections, figure shortlist). The brief is the contract for that unit.
- **Produced** — draft, quotes re-grepped, figures visually verified, rendered into `website/`,
  wired, and passing `qa_page.py` plus the visual pass. Drafted is not produced.
- **Published** — a produced page that is live on the site. Publishing is part of producing, not a
  later phase: a produced article is deployed in the same cycle (DECISIONS 2026-10-12). "Written but
  not live" is not a valid end state.
- **Wired** — present in `sitemap.xml`, `llms.txt` and the `articles.html` card. A `_redirects`
  rule is added **only** when the URL differs from the file name (an alias such as
  `/tesla-rotating-magnetic-field`, or the hub's promo alias `/1894`). A rule whose source equals an
  existing page never fires — Cloudflare resolves assets before `_redirects` — and its presence
  stops that page's trailing-slash variant from normalising.
- **Canonical URL** — the extensionless `/slug`; Cloudflare serves it from `slug.html`. Canonical,
  `og:url`, JSON-LD, sitemap `<loc>`, `llms.txt` and every internal link use that exact string.
  Never a year in a slug.
- **Verified figure** — a crop whose subject was read off the printed page in the scan, not from
  the extractor's OCR filename.
- **Deployed** — pushed to `website/` origin, which publishes the site. Only the owner pushes, and
  pushing stays a separate named action (D6). What changed on 2026-10-12: a produced article is
  staged for deployment in the same cycle it is produced, so "held back indefinitely for review" is
  no longer the default.
- **Shell** — the shared header, nav, sidebar and ads around every page. Out of scope for this
  series; §12 does not gate it.
