# SEO URL Fix — Plan

Site: `teslamagneticgenerator.com` (Cloudflare Pages, static, `website/` deploy repo)
Trigger: Semrush Site Audit email (70 × "Canonical points to redirect", 34 × "3XX redirect in
sitemap", 2 × "4XX page", 74 × "3XX redirect", 71 × "Redirected page has no incoming internal
links", plus title/meta notices).
Date: 2026-10-12.

---

## 0. Root cause (one sentence)

The repo treats `.html` as the canonical URL (2,224 internal links, 46 canonicals, 43 `og:url`,
43 sitemap `<loc>`, 171 JSON-LD URLs) while Cloudflare Pages treats the **extensionless** URL as
canonical and 308-redirects `/x.html` → `/x`. Every critical item in that email is that one
disagreement.

Two secondary defects found while auditing, both bigger than the email's headline numbers:

1. **Trailing-slash gap.** Every `_redirects` rule is written without a trailing slash. Cloudflare
   treats `/foo` and `/foo/` as different paths; `/foo/` falls through to the SPA fallback and
   serves the **homepage at HTTP 200** (soft 404). **3,188 of 4,174 impressions (76%) and 150 of
   210 clicks** in the GSC export land on those URLs. The site's #1 landing page
   (`/how-to-build-a-perpetual-motion-generator/`, 1,769 imp, position 5.96) serves the homepage.
2. **Dead redirect rules.** Cloudflare resolves static assets *before* `_redirects`. 8 of the 1894
   series rules have a source that matches an existing page, so they never fire — and their
   presence stops Cloudflare from normalising the trailing-slash variant. Result: `/x` and
   `/x.html` both serve 200 (duplicate content), and `/x/` serves the homepage.
   *(Corrected 2026-10-12, after the push: that describes the **pending** deploy, not the live site.
   `origin/main` had no series rules at all, and none of the 8 series pages existed there - every
   one of those URLs was a soft 404 serving the homepage. The defect was real, but as something that
   would have shipped with the new pages, not as something already live. Removing the rules was
   still right: measured after the push, all 8 now normalise `/x/` → 308 → `/x`. §9b.)*

## 1. The target contract (invariants to hold from here on)

1. **Canonical URL = `/slug` with no extension.** `/x` is served by Cloudflare from `x.html`.
2. `rel=canonical`, `og:url`, JSON-LD `url`/`mainEntityOfPage`, sitemap `<loc>` and `llms.txt`
   all use that exact string, self-referentially.
3. **Internal links are root-absolute and extensionless** (`href="/x"`, home is `href="/"`).
   Root-absolute, not relative, so a page served at a trailing-slash base cannot mis-resolve.
4. `_redirects` contains **only** paths that have no matching file (legacy WordPress slugs and
   deliberate aliases). A rule whose source equals an existing page slug is dead weight and is
   actively harmful — it breaks that page's trailing-slash normalisation.
5. Every legacy slug gets **two** rules, `/foo` and `/foo/`, both pointing at the final
   extensionless URL in **one hop**.
6. Unknown paths return a real **404**, never the homepage.
7. `lastmod` = the date the page's **content** last changed. Never a future date.
8. **No year in a URL slug.** Year-free slugs only. A year belongs in a title or the prose, where
   it can be refreshed without moving a URL. The `/magnetic-generator-plans-review-2026` ghost links
   (§6) are exactly what a year-slug costs: the page was renamed, five links were left behind, and
   nobody noticed for a whole audit cycle.
9. **A completed article is a published article.** When a page passes its gates (`qa_page.py` + the
   visual pass) it is wired and deployed in the same session. Drafts do not accumulate in
   `new_content/`. This exists because **40 drafted articles are currently sitting undeployed**
   (§6, E4) — the workflow treated "written" as the end state and the deploy step never came.

---

## 2. Status

**Deploy 1 (W1) is live.** `website/` `8e62498` (`_redirects` + the new `404.html`, 2 files,
+248 / −52) was pushed to `origin/main` on 2026-10-12 and built in about 30 seconds. The full
Phase H matrix was then run against the live site: **0 violations** across 46 pages × 3 URL forms,
every legacy slug one hop, unknown paths a real 404. Results in §9.

One thing the plan got wrong about the deploy, and it matters for attribution: `main` was **16
commits** ahead of `origin/main`, not 1. The push therefore shipped W1 together with 15 earlier
unpushed commits - the 1894 series pages 01, 02, 04, 05, 07, 09, 11, their 200 engravings, and a
`.gitignore` change. Those are all **new URLs**, so they do not touch any existing page's signals,
and the soft-404 fix is still measurable - but only by URL group, and there are now three groups
(legacy slugs, current slugs, brand-new 1894 pages) instead of two. Read §10 step 4 with that in
mind before drawing any conclusion from a week of GSC data.

Deploy 2 is **committed locally and not pushed**: `c3232e0` (W2, the signal change) and `249733b`
(W3, titles, metas, asset links) sit on top of the live `8e62498`. `git status` in `website/` is
clean apart from `js/email-capture-widget.html`, which was already untracked before any of this work.
Pushing stays the owner's action, and per §10 it should either wait for the Deploy 1 observation week
or be accepted explicitly as a second change on top of it.

What Deploy 2 does not contain: no page's URL changes, no `_redirects` rule is added for an existing
page, and no page's prose is rewritten. It changes what the site *says* about its URLs — canonical,
`og:url`, JSON-LD, sitemap, `llms.txt`, titles, descriptions — and removes two pages nobody linked to
or read.

Done in the first session, verified offline. `git diff --shortstat` at that point: 47 files,
+2,469 / −2,420.

| # | Change | Result |
|---|---|---|
| A1 | Internal links `.html` → extensionless | 2,224 `href`, 171 JSON-LD URLs, 43 `og:url` rewritten across 46 files |
| A2 | Canonicals → self-referential extensionless | 46/46 verified correct; `og:url` == canonical on all 46 |
| A3 | Relative links → root-absolute | 1,959 rewritten + 141 `href="./"` → `href="/"` |
| A4 | `_redirects` rewritten | 17 legacy rules retargeted to extensionless finals (1 hop, was 2); both slash forms added; 8 dead series rules + dead `/` → `/index.html` rule removed; `/the-free-energy-magnet-motor` added (33 imp, previously uncovered) |

Offline verification already run:
- Internal links resolve under a Cloudflare emulation (`/x` → `x.html`): **3 unresolved**, all
  deliberate forward references to unpublished pages (§6).
- Canonical/`og:url` self-consistency: **0 problems**.
- No `.html` left in any internal link, canonical, `og:url` or JSON-LD self-URL.

W1 is committed; W2–W4 are not. Per D6 (HANDOFF.md): commit, never push — push deploys and needs
owner sign-off.

Also done in the first session (work repo, docs) — **committed 2026-10-12** alongside this file:
- `books/harness/docs/DOMAIN.md` — glossary updated: new **Canonical URL** and **Published** terms;
  **Wired** no longer implies a `_redirects` rule; **Deployed** records publish-on-completion.
- `books/harness/docs/DECISIONS.md` — dated entry for the three decisions (publish on completion,
  extensionless canonicals, no year in a slug) with the evidence behind each.
- `HANDOFF.md` — entry-point pointer at the top, so a session that starts there is routed to this
  plan, and the current working-tree state stated there rather than here.
- This file.

Phase G3 is done (2026-10-12): `SERIES-PLAN-1894.md` §5.1 rewritten as a canonical-URL table that
says which rows need a rule and why the rest need none, plus its line 535 and its D6 session
checklist restated; `books/specs/prd.md` §3 wired-list wording corrected and its §2.6 tooling item
closed. `DOMAIN.md` and `DECISIONS.md` were already done in `a6169c1`.

Still owed to G3: `HANDOFF.md` — ✅ entry-point pointer and the current state added; the stale
"What's Needed Next" list is marked superseded so the next session does not follow it. Still owed: a
real rewrite of "What's Needed Next" and "Website Status", which treat the 40 keyword articles as
finished work - after the GSC week following Deploy 1 has been read, so the rewrite can state what
changed.

### 2.1 Start here (new session)

**Deploy 1 is live and verified. Deploy 2 is committed locally and not pushed.** The next unit of
work is the GSC read, then the owner's push.

1. `cd /home/matt/projects/other/tesla-generator/website && git log --oneline -3` — expect `249733b`
   (W3), `c3232e0` (W2), `8e62498` (W1, = `origin/main`). `git status` clean except
   `js/email-capture-widget.html`. If `origin/main` has moved past `8e62498`, Deploy 2 has been
   pushed: re-read §9c and start the observation clock from that date instead.
2. **Read the GSC data by URL group** (§10 step 4). Three groups, not two: legacy slugs, current
   slugs, and the brand-new 1894 pages that went live in the same push. Do not read the first week
   of numbers for the new pages as an effect of the URL fix.
3. **Then ask the owner to push Deploy 2**, or accept that it is a second change on top of the first
   and stop attributing the two separately. Both are defensible; not deciding is what makes the data
   unreadable.
4. **W4** (E2, publish the two drafted pages) is content work with its own gates. G1/G2 are done, so
   the pipeline and its gates are already correct — that was the blocker, and it is gone.
5. The year-stamp pass (F2) stays a third change, after Deploy 2 settles.
6. The hub (`tesla-1894.html`) is now the most valuable missing page on the site, not for its own
   traffic but because all 8 live series pages describe it in their structured data and it 404s
   (§2.3 item 11).

Already settled, do not re-litigate: D1-D5 (§12), the two-deploy split (D4), and the §11 fallback,
which turned out not to be needed - removing the dead rules did restore `/x/` → 308 on all 8 series
pages (§9b, measured live).

### 2.2 Deploy 1 — what actually shipped, and what was verified

Committed as `8e62498`. Two files.

**`_redirects`** — 50 rules. Re-checked mechanically before committing:

| check | result |
|---|---|
| rules whose source is an existing page (the dead-rule class that caused the bug) | **0** |
| non-ClickBank rules missing a trailing-slash twin | **0** |
| rule targets that do not resolve to a local file | **0** |
| duplicate rule sources | **0** |

One line beyond the plan: `/nikola_tesla_inventor_extraordinaire.html/` → the same target. It is a
legacy WordPress-era source with an underscore and a `.html`, it predates this plan, and it was the
only rule without a trailing-slash twin — i.e. the one rule still leaving a soft 404 in place.
Adding it is the same fix the deploy exists to make, not new scope.

**`404.html`** — 146 lines, built from the `contact.html` shell (nav and footer copied verbatim, so
the two cannot drift). Per Phase C: `robots: noindex, follow`, **no canonical, no `og:url`, no
JSON-LD `url`**, no sitemap entry, no search box, links to `/articles`, `/magnetic-generator`,
`/about` and `/contact`. Asset paths (`/assets/favicon.ico`, `/css/styles-custom.css`) are
**root-absolute**, which the other 46 pages do not do — a 404 is served at an arbitrary base path,
so a relative asset path there would 404 too. No email-capture widget and no exit-intent scripts:
the plan asks for the shell, not the conversion stack, and an exit popup on an error page is a
place nobody asked to add one.

Verified locally (`shot_qa.py 404`, three viewports — screenshots in gitignored `_qa/`):
no horizontal overflow at 375/768/1280, nav dropdown present with 31 items, exactly one `h1`,
console clean, no failed requests. The two gates it also reported — *sidebar column missing*,
*no affiliate CTA on the page* — are article-page gates and do not apply to an error page; they are
recorded here so the next reader does not try to "fix" them.

Re-checked across all 47 pages including `404.html`: **0** absolute `.html` URLs, **0** canonical or
`og:url` mismatches, and of 2,166 root-absolute internal links, **3 unresolved targets** —
`/magnetic-generator-plans-review-2026` (5 links), `/magnetic-generator-battery-storage` (1),
`/tesla-magnetic-generator-maintenance-requirements` (1) — exactly the forward references in §6.
The `/tesla-1894` hub is referenced only from JSON-LD `BreadcrumbList` `item` values, not from any
`href`, so it is not in that count; it is still a forward reference and still must not be sitemapped
until the hub exists.

**Not verified locally, and now measured on the live site** (2026-10-12, before the push). The claim
that removing the 8 dead rules restores `/x/` → 308 normalisation is supported by the two classes
sitting side by side on the live host, same day, same config - the only difference is whether a
`_redirects` rule exists for the path:

| live URL | today | what it shows |
|---|---|---|
| `/magnetic-generator` | 200 | the canonical form works |
| `/magnetic-generator.html` | **308** → `/magnetic-generator` | Pages' own extension normalisation |
| `/magnetic-generator/` | **308** → `/magnetic-generator` | a page **with no rule** normalises its trailing slash |
| `/tesla-earthquake-machine/` | **200** (homepage) | a page **with a dead rule** does not - the duplicate + soft 404 |
| `/how-to-build-a-perpetual-motion-generator/` | **200** (homepage) | the #1 landing page, 1,769 imp, is a soft 404 |
| `/no-such-page-xyz` | **200** (homepage, `<title>Generate Free Electricity…`) | the implicit SPA fallback |

That is the root cause in §0 reproduced against the live site. It does not replace the post-push
matrix - it makes the expected result predictable.

### 2.3 Deploy 2 — what was committed, and the eleven places this plan turned out to be wrong

Committed 2026-10-12, **not pushed**:

| commit | contents | gate run before committing |
|---|---|---|
| `c3232e0` **W2** | the 44-page link / canonical / `og:url` / JSON-LD rewrite; `sitemap.xml` rewritten (44 entries, real `lastmod`); `llms.txt` rewritten; `opt-in.html` + `electrical-experimenter.html` deleted and replaced by 4 insurance rules; 5 `plans-review-2026` links repointed | the §9 offline list, all green |
| `249733b` **W3** | 10 titles, 4 meta descriptions, 18 `og:description` mirrors, 411 asset links made root-absolute, 3 head-block gaps closed | a 45-page metadata audit: 0 issues |

The plan held up where it mattered — the dead-rule diagnosis in §0, the two-deploy split (D4), the
F title and description strings (used verbatim, all 14), the E3 approach, the B2 deletions. It was
wrong, or incomplete, in these eleven places. Each one was found by running something, not by
reading.

1. **Phase F's stated method does not describe the titles it fixes.** It says "drop the trailing
   brand suffix (`— Tesla Magnetic Generator`)". None of the ten had a brand suffix; they were long
   because of descriptive subtitles ("Complete 2026 Cost Breakdown", "Reliable Power When You Need
   It"). The proposed replacement strings are right and were used as written; the method note was
   describing a different site.
2. **`og:description` is not a duplicate of the meta description.** The plan assumed it mirrored it
   everywhere and needed touching on 4 pages. On **18 pages it is a different string**, and on **15 of
   those it is over 160 characters** (up to 224) — which social platforms truncate anyway. Every
   page's `og:description` is now exactly its meta description; no new copywriting was needed, because
   the shorter string already existed on every page and was the one Google was being shown.
3. **Phase A left the asset links relative.** It made page links root-absolute and stopped. 411
   references to `css/`, `js/`, `assets/` and `avatars/` stayed relative across 44 files. They resolve
   correctly today only because every trailing-slash URL 308s to its canonical before anything renders
   — the exact dependency invariant 1 exists to remove. All 411 are root-absolute now; each target was
   confirmed on disk first.
4. **Three head blocks were incomplete, and no gate would have said so.** `articles.html` — indexable,
   in the sitemap, linked from all 45 pages — had **no Open Graph and no Twitter Card block at all**.
   `contact.html` and `privacy.html` had no `robots` meta (behaviour unchanged; every other page states
   it, and the page gate needs a uniform head shape to assert against). Added.
5. **The `lastmod` range in §3 was wrong, and the old file was worse than stale.** The plan describes
   2026-07-03 → 2026-10-11. No commit in this repo's history touches those 35 pages on 2026-07-03 —
   those values were hand-written. Eight series entries were dated **2026-10-14 to 2026-10-22, in the
   future**. The real git-derived range is 2026-10-02 → 2026-10-11, which is what the sitemap now
   carries.
6. **`llms.txt` lists the free book at the PDF, not at `/electrical-experimenter`.** The plan said to
   keep that page in the list; the page is deleted in the same deploy, so listing it would have meant
   handing a model a URL that 301s. It is listed at `/assets/electrical-experimenter.pdf`, its actual
   location, under a short "Free Download" section.
7. **§9 item 5's assertion was half wrong.** "`assets/electrical-experimenter.pdf` is referenced by
   nothing in `website/`" was true of the PDF; the string that appears in `js/exit-popup.js` is the
   **cover image**, `electrical-experimenter-cover.webp`, and the popup posts an email form rather than
   linking to the deleted page — so deleting the page breaks nothing. The PDF is now referenced by
   `llms.txt` and by the insurance rule, which is the point.
8. **`make_article.py` emitted more of the old convention than G1 listed.** G1 names 8 places. The
   markdown link emitter (`inline()`) also passed `[text](page.html)` straight through as a **relative
   `.html` href** — that is where the 4 forward-reference links in §6 came from — and the head
   template emitted `href="assets/favicon.ico"` and `href="css/styles-custom.css"`. Both fixed; the
   nav and article-card emitters now emit root-absolute extensionless hrefs.
9. **`qa_page.py`'s dead-link gate was not checking the wrong thing, it was checking nothing.** It
   skipped every root-absolute href on the grounds that the deploy root was not this checkout's job.
   Under the new convention nearly every link is root-absolute, so the gate passed every page
   unconditionally. It now resolves root-absolute paths through the same order Cloudflare uses
   (static file, then `x.html`), and the `>= 4 internal links` / `>= 3 reciprocal` gates — which
   matched `href="x.html"` and would have silently counted zero on a migrated page — key on the page
   file instead, accepting both spellings so the tool still runs against pre-migration pages.
10. **G3's claim about which §5.1 rows need a rule was wrong.** It says only 07 and the hub need one.
    Rows 08 (`tesla-weird-inventions-1894.html` vs `/tesla-weird-inventions`) and 12
    (`tesla-glowing-tubes-vacuum.html` vs `/tesla-glowing-tubes-before-tubes`) differ from their
    planned URLs too, which is the same shape that produced the 8 dead rules. §5.1 is now a
    canonical-URL table that states the rule and marks each row; 08 and 12 are flagged as a decision
    to make before writing, with "name the file after the URL you want" as the default.
11. **A live defect this plan did not know about: all 8 series pages describe a 404 in their
    structured data.** Their `BreadcrumbList` carries `"item": "…/tesla-1894"`, and `/tesla-1894`
    returns **404** (measured 2026-10-12; `/1894` too). No `href` points there, so no link gate
    catches it — it is only in JSON-LD. Two ways to close it: ship the hub, or drop the hub crumb
    until it exists. Shipping the hub is better for the series and is now the highest-value missing
    page on the site.

State after Deploy 2, measured offline: 45 pages; 2,114 internal links, 0 unresolved except the 2
deliberate forward references; 0 `.html` links; 0 relative `href`/`src` in html or js; canonical ==
own URL and `og:url` == canonical on all 44 indexable pages; 45 JSON-LD blocks parse; every title
≤60 and every description ≤160; sitemap 44 entries, no `.html`, no future `lastmod`, every `<loc>`
mapping to a real file; no `noindex` page in the sitemap and no indexable page missing from it;
`_redirects` 54 rules, none dead, none missing a trailing-slash twin, every target resolving.

---

## 3. Phase B — `sitemap.xml`


Rewrite the file. Rules:

- **`<loc>` → extensionless.** 43 entries: `https://teslamagneticgenerator.com/magnetic-generator`
  etc. Home stays `https://teslamagneticgenerator.com/`.
- **Add 1 indexable page currently missing:** `/articles` — `robots: index, follow`, linked from
  all 46 pages. It is the article hub and belongs in the sitemap.
- **Do not add:** the 4 unpublished pages in §6, and the two pages deleted in Phase B2.
- **`lastmod` → real dates.** Freeze the last *content* commit date per file, captured **before**
  the migration commit exists, otherwise this mass rewrite makes all 43 pages look freshly updated
  and the signal becomes noise. Captured values range 2026-07-03 → 2026-10-11.
  - The 8 series entries currently read **2026-10-14 … 2026-10-22 — all in the future** (today is
    2026-10-12). Replace with actual file dates. Publish dates belong in
    `article:published_time` in the page, not in `lastmod`.
- Keep `<changefreq>`/`<priority>` as-is (Google ignores them; changing them is churn, not a fix).
- Validate: `python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse('sitemap.xml')"` and
  assert every `<loc>` resolves to a local `x.html`.

## 3b. Phase B2 — delete the two pages that were never used

Owner confirmed: `opt-in.html` and `electrical-experimenter.html` were never used. Verified — both
are live at 200 but nothing points at them:

| | `opt-in.html` | `electrical-experimenter.html` |
|---|---|---|
| Internal links to it | **0** | **0** |
| GSC impressions / clicks | 0 | 0 |
| In sitemap / `llms.txt` | no / no | no / no |
| Robots | `noindex` | none (indexable, but orphaned) |
| Why it exists | built as a standalone opt-in landing page "for ads/SEO" (`list_building/PLAN.md:243`); deliberately excluded from `exit-popup.js` and `redirect-leave.js` (line 385) and given the email capture widget (line 387) | landing page for the free 1919 magazine; its only content is a download button for the PDF |

**Action:** `git rm website/opt-in.html website/electrical-experimenter.html`. Neither is linked
from any other file, so nothing needs editing — the only references are their own canonicals and
`electrical-experimenter.html`'s own download button.

**Insurance redirects (2 rules, added after the files are gone):** once the files are deleted their
slugs no longer collide with an asset, so a rule is both valid and necessary.

```
/opt-in                    /                       301
/opt-in/                   /                       301
/electrical-experimenter   /assets/electrical-experimenter.pdf    301
/electrical-experimenter/  /assets/electrical-experimenter.pdf    301
```

Rationale: we cannot see the backlink report from here, and the site is old enough that a stray
link to either is plausible. Two lines of `_redirects` costs nothing and keeps any residual equity
pointing somewhere useful — for `electrical-experimenter`, the giveaway itself. If the owner would
rather see a clean 404 for both, delete these four lines instead; with zero traffic and zero links
either choice is defensible. Flagged as decision D3.

**Keep the lead magnet.** `assets/electrical-experimenter.pdf` (16,039,670 bytes) is the free book
offered by the email sequence — it is the CTA in email 1 and the P.S. in email 3
(`list_building/email_1_welcome.txt:12`, `email_3_deep_dive.txt:38`) and the image in
`exit-popup.js`. Verified live and correct: `content-type: application/pdf`, byte size identical to
the local file. It is **not** affected by deleting the page.

**Doc correction (part of Phase G):** `list_building/EMAIL_OCTOPUS_SETUP.md:260-261, 292` still
says the PDF and `electrical-experimenter.html` are "not deployed" and return the homepage. That
was true when written; the PDF is now deployed and correct. Strike the PDF line, and change the
`electrical-experimenter.html` line to "deliberately removed - link the PDF directly".

## 4. Phase C — real 404

**Done in W1** (`8e62498`); what shipped and what was checked is in §2.2. The spec below is kept as
the thing to hold to if the page is ever edited.

- **Create `website/404.html`**: the site shell (same nav/footer/CSS as other pages), a short
  "page not found" body, links to `/articles`, `/magnetic-generator`, `/about`, a search-free
  design, `<meta name="robots" content="noindex">`, **no canonical**, and no sitemap entry.
  Cloudflare Pages serves `404.html` with a 404 status automatically.
- **No dashboard action is needed - D5 is withdrawn.** Pages' SPA fallback is not a setting; it is
  what Pages does when there is no top-level `404.html`. Cloudflare's own *Serving Pages* doc
  (updated 2026-10-10): *"If your project does not include a top-level `404.html` file, Pages
  assumes that you are deploying a single-page application … serves the root (`/`) for any incoming
  path that does not correspond to a static asset."* So the `404.html` above **is** the switch.
  Checked on the live account 2026-10-12 (brave-browser-control): the `teslag` project's
  Settings → Production page exposes only Build (git repo, build configuration, build cache, branch
  control, watch paths, build system version, deploy hooks), Variables and secrets, Bindings,
  Runtime and General - no SPA or routing control; the Build configuration dialog has framework
  preset, build command, output directory, root directory and build comments only. The zone also has
  **0 Page Rules** and no configured redirect or cache rules, so nothing outside the repo overrides
  this. Phase C goes live on the push, not after a dashboard edit.
- After both: `curl -o /dev/null -w '%{http_code}' https://teslamagneticgenerator.com/no-such-page`
  must print `404`.

## 5. Phase D — `llms.txt`

30 `.html` URLs in the model-facing index. Rewrite to the extensionless form so the file agrees
with the sitemap and canonicals. Same rule set as the sitemap: include `/articles` and
`/electrical-experimenter`, exclude `/opt-in` and unpublished pages.

## 6. Phase E — the 4 forward-reference links

These are **not** errors — they are promises the live site makes. Audited against `new_content/`:

| Link target | Linked from | What actually exists | Action |
|---|---|---|---|
| `/magnetic-generator-battery-storage` | 1 page | `new_content/.../magnetic-generator-battery-storage/article.md`; `TRACKER.md` #23 ✅ | **publish** (E2) |
| `/tesla-magnetic-generator-maintenance-requirements` | 1 page | `article.md`; `TRACKER.md` #16 ✅ | **publish** (E2) |
| `/magnetic-generator-plans-review-2026` | 5 pages | **no draft and no file anywhere.** It was an AI-written article; the owner then asked for the slug to be changed because it is nearly 2027. The rename was never finished: the page became the year-free `/magnetic-generator-plans-review` (live today) and five links were left pointing at the old year-slug. `SEO-FULL-AUDIT-REPORT.md:627` lists the `-2026` page because it audited that pre-rename state — it is not a WordPress leftover | **repoint the 5 links** to `/magnetic-generator-plans-review` (E3) — this finishes a rename that was already decided and half-done |
| `/tesla-1894` | series pages | the 1894 series hub, planned (feature-005 hub brief) | keep the link; canonical settled in D1 |

All four links are already rewritten to the extensionless form, so they resolve with zero redirects
the moment their pages exist. Until then they are hard 404s (after Phase C) — the honest signal,
better than today's soft 404. Do **not** add any of them to the sitemap while unpublished.

### E2 — publish the two drafted pages (owner decision D2: publish)

1. Read `new_content/magnetic-generator-battery-storage/article.md` and
   `new_content/tesla-magnetic-generator-maintenance-requirements/article.md`.
2. Render into the site shell with `make_article.py` **after** G1, using
   `magnetic-generator-for-emergency-backup.html` as the donor — it is the page that links to both,
   so the shell, sidebar and product block already match the topic.
3. Canonicals `/magnetic-generator-battery-storage` and
   `/tesla-magnetic-generator-maintenance-requirements`. **No `_redirects` rule** — slug equals file
   name (§1.4).
4. Each new page links back to `/magnetic-generator-for-emergency-backup` plus 3 other relevant
   pages, so the reciprocity gate (§5.2) is satisfiable and the new pages are not orphans.
5. `qa_page.py` (after G2) then `shot_qa.py` at 375/768/1280.
6. Wire: `sitemap.xml`, `llms.txt`, `articles.html` card.
7. These ship in **Deploy 2**, not Deploy 1 — new pages change nothing about existing URLs.

### E3 — repoint the 5 `plans-review-2026` links

`magnetic-generator-for-beginners-step-by-step.html`, `magnetic-generator.html`,
`tesla-magnetic-generator-materials-list-cost.html`,
`tesla-magnetic-generator-vs-solar-power-which-is-better.html`,
`tesla-magnetic-generator-worth-it.html` — every one of those five anchors already reads
"Best magnetic generator plans review 2026" or similar, which is what the existing
`/magnetic-generator-plans-review` page delivers. Change the href, keep the anchor text.

Because the year-slug never existed as a file, there is nothing to 301 — the fix is five href
edits. And do not re-add a year to that slug: if the plans review needs a dated refresh, change
the title and the content, not the URL (§1.8).

### E4 — the rest of the backlog (parked, but now visible)

`new_content/` holds **50 unique article slugs; 10 are live, 40 are not.** Only the two above are
linked from live pages, so the other 38 are backlog rather than broken promises — no SEO defect
today. They are recorded here because invariant 8 makes them a queue now instead of a graveyard,
and because several are thin near-variants that would cannibalise if published indiscriminately
(`for-boat` / `for-camper` / `for-van-life`, `for-small-home` / `for-homestead`,
`for-fence` / `for-greenhouse`). Publish those as distinct pages only if each has its own real
answer; otherwise merge them into one page and link it from each use case.

## 7. Phase F — titles and metas

Titles >60 chars (10 to fix — `opt-in.html` and `electrical-experimenter.html` are deleted in
Phase B2, so their over-long titles go with them). Verified ≤60:

| File | Now | Proposed | Len |
|---|---|---|---|
| `magnetic-generator-for-emergency-backup.html` | 85 | `Tesla Magnetic Generator for Emergency Backup (2026)` | 52 |
| `magnetic-generator.html` | 81 | `How Much Does It Cost to Build a Magnetic Generator?` | 52 |
| `tesla-magnetic-generator-cost-savings-per-month.html` | 71 | `Tesla Magnetic Generator Cost Savings Per Month (2026)` | 54 |
| `magnetic-generator-plans-review.html` | 70 | `Magnetic Generator Plans Review 2026: Top 10 Compared` | 53 |
| `magnet-motor.html` | 69 | `Tesla Magnet Motor: How the Free Energy Motor Works` | 51 |
| `tesla-magnetic-generator-materials-list-cost.html` | 69 | `Tesla Magnetic Generator Materials List Cost (2026)` | 51 |
| `magnetic-generator-for-beginners-step-by-step.html` | 65 | `Magnetic Generator for Beginners: Step-by-Step Guide` | 52 |
| `tesla-magnetic-generator-vs-solar-power-which-is-better.html` | 65 | `Tesla Magnetic Generator vs Solar: Which Is Better?` | 51 |
| `tesla-magnetic-generator-for-cabin.html` | 63 | `Tesla Magnetic Generator for Cabin: Off-Grid Guide` | 50 |
| `tesla-magnetic-generator-worth-it.html` | 61 | `Is a Tesla Magnetic Generator Worth It? (2026 Review)` | 53 |

Method: drop the trailing brand suffix (`— Tesla Magnetic Generator`) rather than cut the keyword;
the brand is already in the SERP snippet domain. Keep the `<title>` and `og:title` in sync where
`og:title` currently duplicates it.

Meta descriptions >160 (4). Verified ≤160:

| File | Now | Proposed | Len |
|---|---|---|---|
| `whole-house.html` | 195 | `Can a magnetic generator power your whole home? How DIY builders generate electricity with magnets and go off grid with a Tesla magnetic generator.` | 147 |
| `magnet-motor.html` | 194 | `How the Tesla magnet motor works: free energy magnet motor design, perpetual motion motors, and going off grid with Tesla's magnetic inventions.` | 144 |
| `build-a-magnetic-generator.html` | 182 | `Learn how to build a magnetic generator step by step: tools, materials list, wiring, and how long a Tesla magnetic generator build actually takes.` | 146 |
| `free-electricity-from-magnets.html` | 162 | `Free electricity from magnets: is it real or snake oil? I tested several setups. Here is what works, what does not, and what I would tell a friend.` | 147 |

Also mirror each into `og:description` where it currently duplicates.

Note: Semrush counts these by rendered pixel width, not characters, so its 6/8 counts differ from
the 10/4 found here. Fixing to ≤60/≤160 satisfies both.

## 7b. Phase F2 — year stamps (found while correcting E3; **not** part of either deploy)

The owner's reason for renaming the plans-review slug was that it is nearly 2027. That problem is
site-wide and much bigger than one slug:

| | count |
|---|---|
| Pages containing "2026" | **46 of 46** |
| Total "2026" occurrences | **338** |
| In `<title>` | 10 |
| In `<h1>`/`<h2>` | 11 |
| In meta descriptions | 1 |
| Slugs containing a year | 0 (good — and keep it that way, §1.8) |

Recommendation, deliberately **not** bundled into Deploy 1 or 2:

- **Do not find-and-replace 2026 → 2027.** A year bump with no content change is the exact pattern
  search engines are trained to distrust, and it would make the GSC movement from this plan
  impossible to attribute. That is a third change, on its own, after the two deploys settle.
- **Do a real refresh pass per page** in December/January: update the numbers, prices and dates the
  prose actually claims, then let the year follow the content. 338 occurrences is not a sed-replace
  job; it is 46 pages of reading.
- **Prefer dropping bare years from titles** where the page is evergreen (the 1894 series is
  history — a "2026" in those titles is noise). Keep the year only on the commercial pages where it
  measurably helps CTR (plans review, cost breakdowns, worth-it), and only once the content
  genuinely reflects that year.
- Sequencing matters more than the year: doing this at the same time as the URL change means the
  GSC wiggle can't be attributed to either cause.

## 8. Phase G — the article pipeline (so unpublished articles don't reintroduce this) — **done 2026-10-12**

This is the part that matters for the articles still being written in `books/` /
`new_content/`. Today the tooling emits the old convention.

**Done.** Both tools now emit and enforce the contract, both self-tests pass, and `qa_page.py
--all-series` reports 8/9 live series pages passing 29 gates each — the 9th is the hub, which does
not exist yet. What each tool actually needed is in §2.3 items 8-9; both needed more than this
section described.

### G1 — `books/tools/make_article.py` — **done**

*(The line numbers below refer to the file as it stood when this plan was written; it has changed
since. The implementation is `page_url()` / `page_href()` / `local_href()` / `redirect_rules()` at
the top of the file, and `make_article.py --self-test` is the gate.)*

- Add one helper, `page_url(slug)` → `SITE + "/" + slug[:-5]` (and `SITE + "/"` for `index`), and
  use it at the three places that build `url = f"{SITE}/{slug}"` (lines 243, 289, 410). That single
  change fixes canonical, `og:url`, Twitter, JSON-LD `url`/`mainEntityOfPage`/`BreadcrumbList`
  `item`, sitemap `<loc>` and the `llms.txt` line.
- Line 298: `"url": f"{SITE}/about.html"` → `page_url("about.html")`.
- Line 326 (`related`/`see_also` JSON-LD): `f"{SITE}/{it['file']}"` → `page_url(it["file"])`.
- `_article_card()` (line 477) and `add_nav_entry()` (line 221): emit `href="/{slug-without-.html}"`.
- `wire_updates()` (lines 412-421) — the rule generator:
  - Target the extensionless form: `{pretty} /{slug-without-.html} 301`.
  - Emit **both** `/pretty` and `/pretty/` lines.
  - **Skip the rule entirely when `pretty` == the file slug minus `.html`** — that is what created
    the 8 dead rules. `pretty_slug` should only be set when the URL deliberately differs from the
    file name.
- `--self-test` (if any) and the `--wire` output: assert the generated canonical has no `.html`.

### G2 — `books/tools/qa_page.py` — **done**

*(Same caveat about line numbers. The implementation is `page_key()` / `alive()` /
`redirecting_links()`; `qa_page.py --self-test` runs 8 fixture cases across the three gates.)*

The gates parse links with `href="([A-Za-z0-9._\-]+\.html)"` (lines 39, 87). Under the new
convention that matches nothing, so the "≥4 internal links", "≥3 reciprocal links" and
"no dead relative links (§12)" gates would silently pass on zero links. Fix:

- Match `href="(/[A-Za-z0-9._\-]+)"` (root-absolute, extensionless) and resolve through a
  Cloudflare emulation: `/x` is alive iff `x.html` or `x` exists in `website/`.
- Keep accepting the old `.html` form too, so the tool still runs against pre-migration pages and
  `--self-test` fixtures (lines 203-216) stay meaningful.
- Add a gate: **canonical must be self-referential and extensionless**, and `og:url` must equal it.
  This is the gate whose absence let 46 wrong canonicals ship.
- Add a gate: **no internal link may point at a URL that 308s or 301s** — i.e. no `.html` links.

### G3 — docs that state the old convention — **done**

- `SERIES-PLAN-1894.md` §5.1 (line 348): the table header says "Pretty slug (301 in
  `_redirects`)". Change to "Canonical URL" and mark which rows actually need a rule. Rows where
  slug == file name need **no** rule (01-06, 09, 10 and the already-live 8). Only 07
  (`/tesla-rotating-magnetic-field` → `/rotating-magnetic-field-1888`) and the hub (see D1) need
  one.
- `SERIES-PLAN-1894.md` line 535 ("`_redirects` (pretty slug 301)") and line 1185 (session
  checklist) — restate the rule from §1.4 above.
- `books/harness/docs/DOMAIN.md` line 13 ("Wired — present in … `_redirects`") — redefine *Wired*:
  sitemap + llms.txt + articles card; `_redirects` only when an alias is wanted.
- `books/specs/prd.md` line 52 — same wording change.
- `HANDOFF.md` — ✅ entry-point pointer, live state and a "superseded" marker on the stale list,
  all added 2026-10-12. Remaining: rewrite "What's Needed Next" / "Website Status" so they stop
  treating drafted as finished - after the GSC week following Deploy 1, so the rewrite reports what
  actually happened rather than what was attempted.

## 9. Phase H — verification

Offline (before commit) — **run 2026-10-12 before W2 and again before W3. All green; results in
§2.3.** Two corrections to the list itself, found by running it:
1. Re-run the Cloudflare-emulation link check → expect only the **2** known forward references
   (`/magnetic-generator-battery-storage`, `/tesla-magnetic-generator-maintenance-requirements`).
   The plan said 4; E3 removes one and the hub crumb is JSON-LD, not a link, so it never appeared
   here. Anything else unresolved is a defect.
2. Assert: zero `.html` in internal links / canonicals / `og:url` / JSON-LD self-URLs.
3. Assert: every canonical == its own extensionless URL; `og:url` == canonical.
4. Parse `sitemap.xml`; assert every `<loc>` maps to a real file, no `<loc>` has `.html`, no
   `lastmod` is in the future, and neither `/opt-in` nor `/electrical-experimenter` is present.
5. Assert `assets/electrical-experimenter.pdf` is still committed and is referenced only by
   `llms.txt` and the insurance rule. (Before Deploy 2 it was referenced by nothing in `website/`;
   the string in `js/exit-popup.js` is the **cover image**, not the PDF. Making the PDF discoverable
   is the point of §2.3 item 6.)
6. Run `qa_page.py --self-test` after G2, then `qa_page.py` on the 8 live series pages → gates
   must still pass (this proves the gates didn't just go vacuous).
7. Audit the head block of every page, not just the ones being edited: presence of title,
   description, robots, canonical, the five `og:` tags and the four `twitter:` tags; title ≤60 and
   description ≤160 on **every** page rather than only the ones in F's tables; `og:description` ==
   `description`; every JSON-LD block parses. This is the check that found §2.3 items 2 and 4 — the
   F tables list 14 pages, and the defect was on 18 others.

Online (after the owner pushes — this is the part that cannot be verified locally):
```
# every page: 200 at the canonical URL, one hop from every other form
/x.html  -> 308 -> /x        /x/  -> 308 -> /x        /x -> 200
# every legacy slug: exactly one hop
/how-to-build-a-perpetual-motion-generator/  -> 301 -> /build-a-perpetual-motion-generator
# the 8 series pages must lose their duplicate:
/tesla-earthquake-machine.html -> 308 -> /tesla-earthquake-machine
/tesla-earthquake-machine/     -> 308 -> /tesla-earthquake-machine
# unknown path:
/no-such-page -> 404   (true once 404.html is deployed - that is the switch, §4)
```

Runnable form — every URL the plan changes, in one pass. Expect the three columns to read
`308 /x`, `308 /x`, `200` for every current slug, `301 /<final>` twice for every legacy slug, and
`404` for the unknown path. Anything that reads `200 /` is the soft-404 bug still live.

```bash
# 1. every page on the site, all three forms
cd website
for f in *.html; do s=${f%.html}; [ "$s" = index ] && p=/ || p="/$s"
  for u in "$p" "$p/" "$p.html"; do
    printf '%-58s %s %s\n' "$u" \
      "$(curl -so /dev/null -w '%{http_code}' -H 'accept: text/html' "https://teslamagneticgenerator.com$u")" \
      "$(curl -so /dev/null -w '%{redirect_url}' "https://teslamagneticgenerator.com$u")"
  done; done | column -t

# 2. the 8 series pages specifically — the claim that could not be checked locally
for s in tesla-earthquake-machine tesla-high-frequency-alternator tesla-high-frequency-massage \
         tesla-lit-lamps-without-wires tesla-one-wire-power tesla-wireless-power-1893 \
         tesla-worlds-fair-1893 rotating-magnetic-field-1888; do
  curl -so /dev/null -w "/$s/  ->  %{http_code} %{redirect_url}\n" "https://teslamagneticgenerator.com/$s/"
done

# 3. legacy slugs: exactly one hop, and the #1 landing page by name
curl -so /dev/null -w '%{http_code} -> %{redirect_url}\n' \
  https://teslamagneticgenerator.com/how-to-build-a-perpetual-motion-generator/

# 4. unknown path — 404 once 404.html is deployed (the file itself is the switch)
curl -o /dev/null -w '%{http_code}\n' https://teslamagneticgenerator.com/no-such-page
```

Then re-run the Semrush crawl and confirm the four critical groups go to zero.

### 9b. Phase H online — **run 2026-10-12 after the W1 push. Passed.**

The build landed in ~30 s (no build command, output `/`). Results, from the runnable block above:

| check | expected | measured |
|---|---|---|
| every page, all three URL forms (46 pages × 3 = 138 requests) | `/x` 200; `/x/` and `/x.html` 308 → `/x` | **0 violations.** The only artifacts were `//` and `/.html`, produced by the script itself for `index.html` |
| `/index.html` | 308 → `/` | 308 ✓ |
| the 8 series pages, trailing slash | 308 → `/x` | **all 8 ✓** - `/tesla-earthquake-machine/`, `/rotating-magnetic-field-1888/` and the other six. The §11 fallback was **not needed** |
| legacy slugs, both forms | 301, one hop, extensionless final | `/how-to-build-a-perpetual-motion-generator` and `/…/` → 301 → `/build-a-perpetual-motion-generator`; `/homemade-magnetic-generator/` → `/whole-house`; `/the-free-energy-magnet-motor` → `/magnet-motor`; `/free-energy-generator-real-or-fake` → `/magnetic-generator-scam`; `/tesla-rotating-magnetic-field/` → `/rotating-magnetic-field-1888` ✓ |
| unknown path | 404 | `/no-such-page-xyz` → **404** serving the real 404 page (`<title>Page Not Found…`, `noindex, follow`, no canonical). Both slash forms ✓ |
| the 404 page body | matches the repo | head byte-identical to `404.html` ✓ |
| ClickBank `.php` rules | unchanged | `/wplink.php` → 302 → the hop link ✓ |
| the lead magnet | unchanged | `/assets/electrical-experimenter.pdf` → 200 ✓ |
| the 1894 pages that shipped in this push | real content, not the homepage | `/tesla-earthquake-machine`, `/rotating-magnetic-field-1888`, `/tesla-high-frequency-massage` each serve their own `<title>` ✓ |
| `sitemap.xml` | untouched by Deploy 1 | still 42 `.html` `<loc>` entries - that is W2, unchanged, as designed ✓ |

Two notes, both parked (§13), neither a defect: `/404` is itself reachable at 200 (the page is
`noindex` with no canonical, so it cannot be indexed, and a redirect rule for it would be dead by
§1.4), and `/index.html/` returns 404 rather than 308 → `/` - an odd URL nothing links to.

## 10. Phase I — commit / deploy protocol (**D4: two deploys**, decided)

The two halves have different risk, so they get different deploys. The point of splitting is
attribution: Deploy 1 should move the 76%-of-impressions soft-404 leak and nothing else.

### Deploy 1 — recovery only (no page's own canonical changes) — **pushed and live, 2026-10-12**

1. `website/` commit **W1**: `_redirects` (already rewritten in the working tree) + new `404.html`.
   Stage selectively — `git add _redirects 404.html`. The 46 rewritten HTML files stay unstaged;
   they belong to Deploy 2. **Done 2026-10-12 as `8e62498`**; the split held (2 files staged, 46
   left unstaged).
2. ~~Owner action (D5): turn off the SPA fallback~~ - **withdrawn.** There is no such setting; the
   `404.html` in W1 is what removes the fallback (§4, §12).
3. Owner pushes. Verify the Phase H curl matrix immediately.
4. Watch GSC for ~1 week, comparing **by URL group** (legacy-slug group vs current-slug group), not
   per URL. **Amended after the push:** `main` was 16 commits ahead, so the deploy also carried 15
   previously unpushed commits and the 1894 series pages are a third group - brand-new URLs with no
   history. Do not read their first-week numbers as an effect of this change, and do not read a dip
   in the current-slug group as one until the legacy group is seen moving the other way.

Why this is safe on its own: every new `_redirects` target is an extensionless URL that already
returns 200 today, and `404.html` only affects paths that match nothing. No page's canonical, links
or sitemap entry changes, so no page's ranking signal is touched.

### Deploy 2 — the signal change (after the week) — **committed, not pushed**

- **W2** `c3232e0` — the 44-page link / canonical / `og:url` / JSON-LD rewrite, `sitemap.xml`,
  `llms.txt`, the two page deletions (B2) and the 5 repointed `plans-review-2026` links (E3).
- **W3** `249733b` — titles and metas (F), plus the asset-link and head-block work in §2.3 items 3-4.
- **W4** — the two newly published articles (E2). Content work: its own gates, its own review. Not
  started; G1/G2 were the blocker and are done.
- Work repo: **B1** pipeline tools (G1, G2) and **B2** docs (G3) — **done 2026-10-12**.

**Not pushed.** D6 stands: push deploys, and each push is a separate named owner action. The open
question for the owner is §2.1 step 3: push Deploy 2 after reading the Deploy 1 week, or push it now
and accept that the two effects can no longer be separated. The year-stamp pass (F2) is deliberately
a *third* change, after both of these settle.

## 11. Risks and rollback

- **The one real risk:** 89 clicks currently sit on `/how-to-build-a-perpetual-motion-generator/`
  at position 5.96. Redirecting it means Google has to move that ranking to
  `/build-a-perpetual-motion-generator`. Expect 2-6 weeks of flux on the affected pages. This is a
  temporary dip against a permanently broken status quo — those rankings live on URLs that resolve
  to the homepage, so they cannot compound.
- **Redirects do not leak equity.** Google has said since 2016 that a single 301/308 passes
  equivalent signal. This change *removes* 2,224 redirect hops and shortens 17 chains from 2 hops
  to 1. No backlinked URL changes: external links point at legacy slugs and `.html` URLs, both of
  which keep redirecting to the same final URL they already resolve to today.
- **Rollback:** the whole change is text in git. `git revert` the relevant `website/` commit (W1-W4
  are deliberately separate) and push. `_redirects` is the only file whose rollback changes live
  behaviour immediately.
- **Was "unverifiable locally"; measured after the push and it holds** (§9b): all 8 series pages now
  answer `/x/` → **308** → `/x`. The §11 fallback (explicit `/x/ → /x 301` rules) was **not needed**
  and must not be added - a rule whose source is an existing page is the defect class that caused
  this whole bug (§1.4).

## 12. Decisions — five settled on 2026-10-12; D5 withdrawn the same day

**D1 — 1894 hub slug: keep `tesla-1894.html`, canonical `/tesla-1894`.** Add `/1894` and `/1894/`
as 301 aliases to `/tesla-1894`, for promo use only — nothing on the site links them.
*Why:* the live series pages already link `/tesla-1894`, so this is zero rework; canonical == file
slug keeps every page in the series consistent and avoids re-creating the dead-rule class that
caused this whole bug; the URL keeps "tesla" in it; and the alias still gives the short promo link
without ever creating a second canonical. **Action:** update `SERIES-PLAN-1894.md` §5.1 — the row
becomes "canonical `/tesla-1894`; `/1894` is a promo alias". This is the only series page besides
07 that needs a rule, and it is a deliberate exception, not an accident.

**D2 — publish.** Two of the three promised pages have real drafts and get published (E2). The third
never had a draft — it was an AI-written article mid-rename — so its five links get repointed to
the year-free page that already exists (E3). See §6.

**D3 — keep the four insurance redirects** for the two deleted pages (Phase B2).
*Why:* the backlink report isn't visible from here and the site is old enough that a stray link to
either is plausible; four lines cost nothing, and the `electrical-experimenter` redirect lands on
the giveaway itself, which is a real conversion asset rather than a dead end.

**D4 — two deploys**, as §10.

**D5 — withdrawn the same day it was made.** It read "SPA fallback off in the Cloudflare dashboard;
owner action; not a repo change." There is no such setting to turn off, and the premise was inferred
rather than checked. Cloudflare's *Serving Pages* doc (updated 2026-10-10) states the behaviour
plainly: a Pages project **without** a top-level `404.html` is assumed to be an SPA, and Pages then
serves `/` for any path that matches no static asset. The soft 404 is the *absence* of the file, so
W1's `404.html` is the fix itself, not a prelude to one. Confirmed on the account: no SPA or routing
control anywhere in the `teslag` project settings, and the zone has 0 Page Rules and no configured
redirect/cache rules. **Consequence:** Deploy 1 is one owner action (push), not two, and Phase C is
live the moment that push builds.

## 13. Parked / out of scope

- `_redirects` and `_headers` are publicly fetchable at 200 (Cloudflare serves config files as
  assets). Cosmetic; no rule added.
- **`/404` is reachable at 200** (measured, §9b). The page is `noindex` with no canonical, so it
  cannot enter the index, and a `_redirects` rule for it would be dead by §1.4. Leave it.
- **`/index.html/` returns 404** rather than 308 → `/` (measured, §9b). Pages normalises `/x.html`
  → `/x` but not `/x.html/`. Nothing links that form, and it is now a real 404 rather than a soft
  one. Leave it.
- The ClickBank `.php` affiliate redirects resolve in 3 hops to an external host. Not SEO-relevant
  (no equity passes), and changing them risks breaking tracked affiliate IDs.
- `<changefreq>` / `<priority>` in the sitemap — Google ignores them. Left alone.
- The 404 soft-404 problem may also exist for other Cloudflare projects; out of scope here.
- **The 38 other undeployed drafts** (§6, E4). Not defects today — nothing links to them. They are a
  queue under invariant 9, and several are thin near-variants that should be merged rather than
  published side by side.
- **The year-stamp pass (F2)** — 338 occurrences across all 46 pages, nearly 2027. Real work, own
  change, after both deploys settle. Deliberately not bundled.
