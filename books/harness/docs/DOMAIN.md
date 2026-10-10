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
- **Wired** — present in `sitemap.xml`, `llms.txt`, `_redirects` and the `articles.html` card.
- **Verified figure** — a crop whose subject was read off the printed page in the scan, not from
  the extractor's OCR filename.
- **Deployed** — pushed to `website/` origin, which publishes the site. Only the owner deploys.
- **Shell** — the shared header, nav, sidebar and ads around every page. Out of scope for this
  series; §12 does not gate it.
