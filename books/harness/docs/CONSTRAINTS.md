# Constraints

What this project may not do, and what it must always do.

## Heading case: series-page headings are title case (2026-10-16, feature-001/heading-case-gate)

Every `<h2>` and `<h3>` on a 1894-series page — and every `FAQPage` `mainEntity[].name`,
which must match the visible `<h3>` text — is title case. This is the owner's standing
house rule, not a style preference, and it is machine-enforced: `books/tools/qa_page.py`
gates it on every page (`--all-series` included) by calling
`books/tools/titlecase_headings.py`, the same tool that fixes them. Write the heading in
the target case and the tool leaves it alone.

The rule, as the tool implements it:

- capitalise every word of four letters or more, and every verb and pronoun of any length;
- leave lowercase only articles (`a`, `an`, `the`), coordinating conjunctions (`and`, `or`,
  `but`, `nor`, `for`, `yet`, `so`) and prepositions of three letters or fewer (`at`, `by`,
  `in`, `of`, `on`, `to`, `up`, `per`, `via`, `vs`) — and never in the first or last position;
- capitalise the first word after a colon or a dash;
- title-case both elements of a hyphenated compound (`High-Frequency`, `Constant-Period`);
- leave acronyms, years and initials as they are (`AC`, `DC`, `OG`, `SEO`, `1893`, `N. Y.`).

Two exemptions, both deliberate:

1. **`<h1>` is not touched.** It is mirrored into `<title>`, `og:title` and
   `twitter:title`, which were sized to the 60-character title gate in Deploy 2, so
   retitling an h1 can fail that gate. The h1s on the shipped pages are already title case.
2. **A quoted source term keeps the case the printed book has it** — `'massage'`,
   `"a tale of woe"`. `check_quotes.py` checks quotations against the print, so
   title-casing the inside of a quotation breaks the quote it is quoting. Only the quoted
   span is exempt: the rest of the heading is still title-cased, and a heading that opens
   with a quotation still capitalises the word after the closing colon
   (`"a tale of woe": Why the Machine Was Hard`).

Fixing a page: `python3 books/tools/titlecase_headings.py <page.html>` rewrites the
headings and the matching schema names in place; add `--check` to report without writing,
which exits 1 if anything is out of case.

Where the rule actually bites is the draft, not the page. `make_article.py` renders from
`article.md`, so a sentence-case `##` in a draft returns as a sentence-case `<h2>` the next
time that page is rendered, and the gate fails a page that passed last week. The nine
shipped pages were retitled by hand in the retrofit; their drafts were not — 72 `##`/`###`
lines across the ten drafts under `new_content/1894-series/` are still sentence case. Check
a draft's headings before rendering from it, not after.
