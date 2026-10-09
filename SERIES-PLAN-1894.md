# The 1894 File — production plan (v2, detailed)

**Series:** *The 1894 File* — 12 flagship articles + hub, built on a first-edition
primary source we hold and nobody else cites.
**Site:** teslamagneticgenerator.com (static Bootstrap 5, 39 pages, `_redirects`)
**Source book:** Martin, T. C. (ed.), *The Inventions, Researches and Writings of
Nikola Tesla, with Special Reference to His Work in Polyphase Currents and High
Potential Lighting.* New York: D. Van Nostrand, 1894 (entered 1893). 518 page
scans, public domain. archive.org item `inventionsresear00martiala`.
**Production assumption:** the producing agent has **vision** (can view images and
screenshots). Every figure-QC and layout-QA step below depends on it.

---

## 0. How to use this document

- §1–§5 = strategy and rules. Read once, then enforce.
- §6–§8 = the machine (figure pipeline, template script, runbook). Build once.
- §9 = the 12 briefs. Each is self-contained: hand one brief to a session and it
  produces one article.
- §10 = the next 40 topics, so we never run dry.
- §11–§15 = scheduling, QA gates, metrics, risks, open decisions.
- Appendices = verified quotes, chapter map, figure shortlists, fact boxes.
  **Nothing ships that is not in Appendix A or freshly re-grepped from the OCR.**

Non-negotiables:

1. **Printed page = scan file page − 18.** Every citation uses the printed page.
2. Every quote is re-grepped from `books/extracted/tesla-1894-plain.txt` and
   pinned to a printed page before it ships.
3. Every figure is a 1894 scan crop or a period patent drawing, credited, with
   `width`/`height`/`alt`/`loading="lazy"`.
4. No new unverified claims about what a generator can do. This series earns
   trust; the money pages spend it.

### 0.1 Session bootstrap (a fresh session starts here)

State as at 2026-10-09: this plan is committed (`cbb7e97`, parent repo); the 200
figure crops + `manifest.csv` are committed in `website/` (`d0122bc`, **not
pushed** — pushing deploys). Everything in §1 exists; nothing there needs
rebuilding.

Prerequisite for the figure QC pass and the visual QA step: a **vision-capable
model**. Without it, run only the non-visual steps (tooling, hub text, drafts).

Read in this order: §0 → §6 figures → §7 `make_article.py` → §8 runbook → §12 QA
gates → `books/extracted/quote-index.md`.

Session 1, in order:

1. `books/tools/contact_sheet.py` → 6 sheets (12 sheets × 18 tiles, 300 px) in
   `website/assets/tesla1894/_qc/`.
2. Figure QC: view each sheet, write `website/assets/tesla1894/manifest_qc.csv`
   (`file,verdict,subject,quality,notes`). Target ≥120 usable.
3. `books/tools/grep_quote.py` — quote verification helper.
4. `books/tools/make_article.py` — §7 spec; test against
   `website/nikola-tesla-inventor-extraordinaire.html` as the donor.
5. `books/tools/qa_page.py` — §12 gates.
6. `books/tools/shot_qa.py` — Playwright screenshots + console check.
7. Hub `website/tesla-1894.html` — §9 brief 00.
8. Article 03 `website/tesla-oscillator-that-cracked-a-building.html` end-to-end
   via §8, including the patent-drawing supplement (US 514,169 — confirm the
   number on patents.google.com before use).

Do not re-run: OCR extraction, figure extraction, quote harvesting, or this spec.

### 0.2 Session 1 result (2026-10-09) — run WITHOUT vision

This session had no vision-capable model (`read` on a .jpg returns "model does not
support images"), so §0.1's fallback applied: non-visual steps only.

| # | Step | Status |
|---|---|---|
| 1 | `contact_sheet.py` | **done** — 12 sheets × 18 tiles, 300 px, in `website/assets/tesla1894/_qc/` |
| 2 | Figure QC | **blocked** — `manifest_qc.csv` scaffold written (200 rows, verdict columns blank). Needs a vision pass. |
| 3 | `grep_quote.py` | **done** — `--verify` re-checks all 31 Appendix A quotes: 30/31 verify on the stated page; the 1 miss is a citation error (see corrections) |
| 4 | `make_article.py` | **done** — §7 spec incl. `--self-test` (all assertions pass) and `--wire` |
| 5 | `qa_page.py` | **done** — 24 numeric gates from §12 |
| 6 | `shot_qa.py` | **done** — 3 viewports + console/404/overflow checks; screenshots to `website/_qa/`. Reviewing them needs vision. |
| 7 | Hub | **drafted** — `new_content/1894-series/00-hub/article.md` (1,188 words) + preview HTML. Not in `website/`: figures unverified, and it links to 12 pages that do not exist yet. |
| 8 | Article 03 | **drafted + rendered** — `new_content/1894-series/03-tesla-earthquake-machine/article.md` (1,619 words) → preview passes **23/24** numeric gates. US 514,169 confirmed on patents.google.com ("Reciprocating Engine", filed 19 Aug 1893, issued 6 Feb 1894); drawing fetched to `assets/tesla1894/patents/us514169-fig1.webp` (740×1087) — **not visually verified**. |

Corrections found by the tooling (applied to this plan and to `books/extracted/quote-index.md`):

- **The "written in pencil" quote is on printed p. 9, not p. 27.** It sits on scan
  file 27; the register had file page and printed page swapped. Appendix A and brief
  07 now say p. 9.
- **MythBusters detail corrected**: bridge test gave "a vibration noticeable 100 ft
  away", verdict busted, aired 30 Aug 2006 — not "hundreds of feet".
- **Appendix D word counts re-run and confirmed**: `free energy` 0, `perpetual` 0,
  `over unity` 0; "magnetic generator" 5, all *pyro*-magnetic (pp. 6, 424 ×1, 429 ×2,
  496).
- **The §9 hub description promised a "free PDF"**, contradicting D4. Rewritten in the draft.
- **§12's "total image weight on page < 400 KB" cannot pass on this site**: the shared
  shell (sidebar ads, popular-page thumbs, news.webp) is ~273 KB on every page. The
  gate is now enforced on the article's own figures; shrinking the shell is a separate
  site-wide task.
- **The donor shell is malformed** (54 `<div>` open / 58 close). `make_article.py`
  strips the surplus so series pages are balanced; legacy pages are untouched.
- **YAML gotcha**: unquoted `tid: 1894_03` parses as the integer 189403.
  `make_article.py` now refuses it — always quote `tid`.
- **§0.1 step 8 names article 03 `tesla-oscillator-that-cracked-a-building.html`**,
  which contradicts the §5.1 URL table (`tesla-earthquake-machine.html`). Drafted to §5.1.

Open sequencing problem (needs a decision, not code): §11 ships the hub in S1, but the
hub links to all 12 articles, so it fails §12's "no broken relative links" until they
exist. Either ship the hub last, or ship it with 03/01/07 and leave the other nine
cards as plain text.

Next session (with vision): fill `manifest_qc.csv` from the 12 contact sheets →
verify the three figures in article 03 → `make_article.py … --wire` into `website/` →
`qa_page.py` + `shot_qa.py` review → commit.

---

## 1. Asset inventory (already built)

| Path | Contents | Status |
|---|---|---|
| `books/pdf-pages-tesla-1894/page-001..518.pdf` | 518 single-page scans, 500 ppi, 1856×3226 | done |
| `books/Tesla Inventions Researches Writings 1894.pdf` | full book, 35.4 MB | local reference only — **not published** (no download; decision D4) |
| `books/extracted/tesla-1894-plain.txt` | 1.01 MB, ~177k words, `<<<<< page-NNN >>>>>` markers | done |
| `books/extracted/tesla-1894-fulltext.txt` | 1.09 MB, `-layout` variant | done |
| `books/extracted/quote-index.md` | 25 verified quotes + chapter→page map | done |
| `books/tools/extract_figures.py` | figure auto-cropper (text-row masking) | done, tested |
| `website/assets/tesla1894/*.webp` | **200 crops, 7.3 MB**, all pass numeric ink check | done, untracked |
| `website/assets/tesla1894/manifest.csv` | `file,file_page,printed_page,book_fig,caption,px_w,px_h` | done |
| `website/nikola-tesla-inventor-extraordinaire.html` | cleanest donor template | done |
| `comments/plan.md` | comment block convention — **not used** on series pages | n/a |

To create: `books/tools/contact_sheet.py`, `books/tools/grep_quote.py`,
`books/tools/make_article.py`, `books/tools/qa_page.py`, `books/tools/shot_qa.py`,
`website/assets/tesla1894/manifest_qc.csv`, `website/assets/tesla1894/_qc/`,
`website/assets/tesla1894/patents/`, `website/assets/og/`,
`new_content/1894-series/` (drafts + `index.json`), the three §16.3 linkable
assets (`tesla-1894-plates.html`, `tesla-1894-word-search.html`,
`tesla-1894-part1-text.html`) and the GitHub `tesla1894` repo.

---

## 2. Strategy

### 2.1 Why not more "magnetic generator" posts

From the site's own exports (`KeywordReport_10_2_2026.csv`,
`PageTrafficReport_10_2_2026.csv`):

- ~4,000 impressions/month across 39 pages.
- The money cluster is exhausted: `tesla magnetic generator` 32 impressions,
  `tesla magnet generator` 10, `tesla magnetic generator plans` 6 — and we already
  rank 3–6 for them. No headroom.
- Traffic is concentrated in 4 pages (~60% of clicks):
  `how-to-build-a-perpetual-motion-generator/` 89 clicks,
  `free-energy-magnet-motor/` 30, home 19, `build-a-perpetual-motion-generator.html` 22.

Growth = **adjacent Tesla-history demand** + **credibility that lifts the domain**.

### 2.2 The wedge

Competitors (teslauniverse.com, kroneckerwallis.com, teslasciencecenter.org,
waveguide.blog, rexresearch.com) paraphrase Tesla's lectures. None cite the 1894
first edition by page; none show the original engravings at readable size. We hold
the scan, the OCR, the page numbers and 200 extracted engravings.

**Promise, one line:** *every claim carries a page number from an 1894 book, and
every article shows an engraving nobody else is showing.*

### 2.3 Targets at 12 weeks

| Metric | Now | Target |
|---|---|---|
| Pages on site | 39 | 52 (39 + hub + 12) |
| Monthly impressions | ~4,000 | 12,000+ |
| Tracked queries with ≥1 impression | ~130 | 400+ |
| Pages in top 10 on a Tesla-history query | ~0 | 8 |
| ClickBank sales attributed to `tid=1894_*` | n/a | ≥ 3 |
| Answer-engine citations (5 probe questions) | 0 | ≥ 1 |

---

## 3. Series furniture and format rules

Every article ships with the same furniture, in this order:

1. **H1** (≤ 60 chars where possible; primary query phrased naturally).
2. **Kicker:** `The 1894 File · No. 3 of 12 — every quote below is cited from the
   first edition, page numbers included.`
3. **Published / updated line** (existing site format).
4. **Standfirst** — 2–3 concrete sentences, no throat-clearing.
5. Body: 1,200–1,800 words flagship; H2s (H3 sparingly); paragraphs ≤ 60 words;
   `fs-5 mb-4` paragraphs to match the site.
6. **2–3 figures**, each in `<figure class="mb-4 pt-5">` with caption:
   `Engraving from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 154 — public domain.`
7. **One "what the internet gets wrong" H2** (the shareable beat).
8. **Sources block**: full book citation + archive.org item, the specific pages
   used, patent numbers, any modern source.
9. **One CTA block** (existing `alert alert-info` pattern) with ClickBank link
   carrying `?tid=1894_NN`, plus one sentence of disclosure:
   *We earn a commission if you buy through that link — it does not change what the
   1894 book says.*
10. **No comments block on series pages** (decision D3). `css/comments.css` is not
    linked; the donor template's comments section is stripped.

Quote style: `Tesla wrote in 1892: "…" (1894, p. 236).` Ellipses for cuts; never
re-word inside quotation marks; `[sic]` where the 1894 text is odd. Long-s and
`S`-for-`8` OCR artefacts are normalised silently (policy in Appendix A).

Word counts by tier: flagship 1,200–1,800 · Tier 2 1,000–1,400 · Tier 3 800–1,200 ·
Tier 4 900–1,300 · Tier 6 300–800. **Do not pad.** The `thicken*.py` habit is
banned for this series.

---

## 4. Guardrails (accuracy, legal, affiliate)

### 4.1 Claims

- Historical claim → page cite. Modern technical claim → datasheet/standard/study
  cite, or cut it.
- This series adds **no** new "free energy / perpetual motion works" assertions.
  Practical reasons: unverifiable claims make a 39-page domain look cheap to human
  reviewers and answer engines; the affiliate network and payment processors care;
  and the real 1894 material (30,000 alternations per second, 94–95% motor
  efficiency, a steel arbor torn apart by resonance) is better copy than the myth.
- Where older site pages overstate, series pages link to them as *our take on what
  you can actually build*, without repeating the claim.
- Every "Tesla predicted X" states what he actually said **and** what happened to
  the idea.
- No invented anecdotes, dates, or "historians say". A brief marked
  `⚠ needs source` must be sourced or cut before publish.
- Safety: never imply readers should replicate high-voltage experiments.

### 4.2 Images

- Book engravings/scans: US public domain (1894 imprint). Credit line on each.
- Patent drawings: public domain (USPTO). Credit `US patent NNN,NNN (year), Nikola Tesla.`
- Never hotlink. Everything lives under `website/assets/tesla1894/`.
- Alt text describes the apparatus, includes the year, e.g.
  `1894 engraving of Tesla's high-frequency alternator, cross-section, p. 375`.

### 4.3 Affiliate

Existing footer disclosure on every page with a `hop.clickbank.net` link, plus the
one-line disclosure above the CTA (§3.9). New `tid` namespace `1894_NN` so
ClickBank reporting isolates the series.

---

## 5. Information architecture

```
                     tesla-1894.html  (HUB: index + "how we cite" trust box)
                              |
     +--------------+---------+----------+--------------+-------------+
     |              |                    |              |             |
 01 Lamps      02 One-wire         03 Earthquake     04 Wireless   10 "Free energy"
     |              |                machine          power          myth-check
 06 Cold flame  12 Glowing tubes      |                |              |
     |                             09 World's Fair   11 HF altern.  08 Weird inventions
     +-- 05 Massage                      |                             |
                                     07 Rotating field ----------------+
```

### 5.1 URL and redirect table

| # | File | Pretty slug (301 in `_redirects`) |
|---|---|---|
| H | `tesla-1894.html` | `/1894` |
| 01 | `tesla-lit-lamps-without-wires.html` | `/tesla-lit-lamps-without-wires` |
| 02 | `tesla-one-wire-power.html` | `/tesla-one-wire-power` |
| 03 | `tesla-earthquake-machine.html` | `/tesla-earthquake-machine` |
| 04 | `tesla-wireless-power-1893.html` | `/tesla-wireless-power-1893` |
| 05 | `tesla-high-frequency-massage.html` | `/tesla-high-frequency-massage` |
| 06 | `tesla-cold-flame.html` | `/tesla-cold-flame` |
| 07 | `rotating-magnetic-field-1888.html` | `/tesla-rotating-magnetic-field` |
| 08 | `tesla-weird-inventions-1894.html` | `/tesla-weird-inventions` |
| 09 | `tesla-worlds-fair-1893.html` | `/tesla-worlds-fair-1893` |
| 10 | `tesla-free-energy-what-he-said.html` | `/tesla-free-energy-what-he-said` |
| 11 | `tesla-high-frequency-alternator.html` | `/tesla-high-frequency-alternator` |
| 12 | `tesla-glowing-tubes-vacuum.html` | `/tesla-glowing-tubes-before-tubes` |

### 5.2 Internal link map (each article: 4–6 out-links, ≥3 in-links)

| Article | Links out to | Must be linked from |
|---|---|---|
| Hub | all 12, `magnetic-generator-plans-review.html`, `electrical-experimenter.html` | nav "Pages", `articles.html`, footer, all 12 |
| 01 Lamps | `magnetic-dynamo-generator.html`, `electricity-using-magnets.html`, 06, 12 | 04, 06, 12, hub |
| 02 One-wire | `diy-magnetic-generator.html`, `can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html`, 11 | 01, 04, 11, hub |
| 03 Earthquake | `perpetual-motion-generator.html`, `magnet-motor.html`, 09, 11 | 09, 11, hub |
| 04 Wireless | `whole-house.html`, `solar.html`, 02, 11 | 02, 10, hub |
| 05 Massage | `magnetic-generator-scam.html`, `How-Much-Noise-Does-a-Free-Energy-Device-Make.html`, 10 | 10, hub |
| 06 Cold flame | `7-interesting-facts-about-magnets.html`, 01, 12 | 01, 12, hub |
| 07 Rotating field | `magnetic-dynamo-generator.html`, `magnetic-generator-plans-review.html`, `tesla-magnetic-generator-worth-it.html`, 11 | 03, 11, hub, `nikola-tesla-inventor-extraordinaire.html` |
| 08 Weird inventions | `magnet-motor.html`, `perpetual-motion-generator.html`, 10 | 03, 10, hub |
| 09 World's Fair | `build-a-magnetic-generator.html`, `magnetic-generator-plans-review.html`, 03, 07 | 03, 07, hub |
| 10 Free energy | `magnetic-generator-scam.html`, `tesla-magnetic-generator-worth-it.html`, `free-electricity-from-magnets.html`, 05, 08 | 04, 05, 08, hub, `magnetic-generator-scam.html` |
| 11 HF alternator | `magnetic-generator-plans-review.html`, `magnetic-dynamo-generator.html`, 02, 03 | 02, 03, 07, hub |
| 12 Glowing tubes | `free-electricity-from-magnets.html`, `electricity-using-magnets.html`, 01, 06 | 01, 06, hub |

Backlink pass (week 6): add a `Sources & further reading` line with 1–2 series
links to these 8 existing pages: `nikola-tesla-inventor-extraordinaire.html`,
`magnetic-dynamo-generator.html`, `perpetual-motion-generator.html`,
`magnet-motor.html`, `magnetic-generator-scam.html`,
`7-interesting-facts-about-magnets.html`, `electricity-using-magnets.html`,
`build-a-magnetic-generator.html`.

---

## 6. Figure pipeline (vision-enabled)

### 6.1 Extraction (done)

```bash
cd books/tools
python3 extract_figures.py --pages 20-518 --out ../../website/assets/tesla1894
# 200 crops + manifest.csv ; printed_page = file_page - 18
```

Detection: render at 300 ppi → mask rows the PDF text layer says contain text →
keep remaining ink bands ≥ 110 px tall / 220 px wide → crop to ink bbox + 14 px →
reject page-edge junk.

Verified gaps: Ch. XLIII (oscillator, pp. 486–495) yields **1** engraving
(Fig. 313, p. 491); Ch. XXXI ("massage", pp. 394–395) yields **0**; Ch. XXV
(pp. 119–144) yields 0 (text-only introduction).

### 6.2 Vision QC pass (once, ~1 session)

1. **Contact sheets** — `books/tools/contact_sheet.py` builds labelled montages,
   36 thumbnails per sheet, label = `filename | printed page | book Fig. no. | px`
   → `website/assets/tesla1894/_qc/sheet-01.png` … (6 sheets).
2. **Visual verdict per crop** → `manifest_qc.csv`:
   `file, verdict, subject, quality, aspect_ok, caption_ok, notes`
   - `verdict`: `keep | keep-tight | keep-wide | merge-with:<file> | drop`
   - `subject`: plain-English description (seeds the `alt` text)
   - `quality`: `A` clean line art · `B` light/uneven scan · `C` partial/fragment
3. **Repair recipes** where flagged: split figure → `merge-with`; caption
   bleeding in → re-crop with tighter band bounds and `--pad 4`; two figures in one
   band → column split at the whitespace gutter; faint scan →
   `magick in.webp -level 15%,85% -sharpen 0x1 out.webp`.
4. **Full-page plates** (pages with < 300 chars of text, e.g. file 496 / printed
   478, a 960×1707 plate in the World's Fair chapter) exported at 200 ppi as
   `tesla1894-plate-p478.webp`.
5. **Naming (final):** `tesla1894-p<printed>-fig<bookfig>.webp`,
   `tesla1894-plate-p<printed>.webp`, `patents/us514169-fig2.webp`.
6. Target after QC: **120–150 usable figures**, ≥ 8 candidates per flagship range.

### 6.3 Patent-drawing supplement (fills the gaps)

Tesla's patents are public domain and scan far better than 1894 book art. Fetch
from patents.google.com, verify visually, store in
`website/assets/tesla1894/patents/`.

| Article | Patent | Why |
|---|---|---|
| 03 Earthquake | **US 514,169** "Reciprocating Engine", Feb 6 1894 | the oscillator; the book has one engraving only |
| 07 Rotating field | the 1888 polyphase set (US 381,968 / 382,279 / 382,280) | the motor drawings behind the pencil-written paper |
| 11 HF alternator | Tesla high-frequency alternator family | clearer than Figs. 199–203 |
| 05 Massage | a 1890s–1900s high-frequency electrode patent | chapter has zero figures |
| 02 One-wire | US 454,622 / 464,666 (electrical transmission system) | single-conductor system |

Each number must be confirmed on patents.google.com at production time; never ship
an unverified number.

### 6.4 OG images and quote cards

- **OG image** 1200×630: left 60% best engraving on paper tone `#efe9dd`, right
  40% title + `The 1894 File` + page cite. Built with ImageMagick, then **viewed**
  before shipping. `website/assets/og/<slug>.webp`, ≤ 120 KB.
- **Quote card** 1080×1080: scan texture + quote + `(1894, p. NN)`. One per
  article; used for Pinterest and as OG fallback.

### 6.5 Layout QA with screenshots

`books/tools/shot_qa.py <slug>`:
1. serve `website/` on `:8080` via the process tool,
2. Playwright screenshots at 375×812, 768×1024, 1280×900 →
   `website/_qa/<slug>-{mobile,tablet,desktop}.png`,
3. visual review: nav dropdown not clipped, figures not overflowing, captions
   readable, sidebar stacking, no shift from missing `width`/`height`, CTA visible
   on mobile first screen,
4. fail → fix → re-shoot. Hard gate before deploy.

### 6.6 Image insertion policy (what goes where)

Every article ships with **2–3 images placed in the body**, each adjacent to the
paragraph it illustrates. No image dumps at the top, no decorative images.

Sourcing order:

1. **1894 engraving from the same chapter/page range** as the passage (default).
2. **1894 engraving from a neighbouring chapter** if the topic is discussed
   without art (e.g. Ch. XXX "electrostatic induction apparatus" Figs. 208–09 for
   the massage article).
3. **Public-domain patent drawing** if the book has nothing for that device.
4. **Page-scan crop** of the 1894 page itself when the words are the artefact
   (used in 05 p. 394 and 10 p. 236).

Placement rules:

- Figure 1 sits within the first three H2s; figure 2 mid-article; figure 3 (if
  used) near the closing section.
- Caption always states what is shown **and** the source page: `Engraving from
  Martin (ed.), … (1894), p. 154 — public domain.`
- `alt` describes the apparatus as actually seen, not as the OCR caption claims.
- Width: full column width on mobile, max 740 px desktop; `width`/`height`
  attributes always set from the real pixel dimensions.
- Never reuse the same engraving on two articles unless the caption differs —
  duplicate images across the series look thin.

**Verification step (needs vision, which is enabled for production):** before an
image is inserted I open the crop and confirm it shows what the surrounding text
says. The manifest's OCR caption is a hint, never the truth — the extractor
mis-reads some captions (one on printed p. 484 came out as "Fig. 811"). If the
crop does not match the passage, it is replaced, not re-captioned.

---

## 7. `make_article.py` spec (build in session 1)

```
python3 books/tools/make_article.py \
  --md new_content/1894-series/03-tesla-earthquake-machine/article.md \
  --donor website/nikola-tesla-inventor-extraordinaire.html \
  --out website/tesla-earthquake-machine.html \
  --tid 1894_03 --wire
```

**YAML front matter:** `title`, `slug`, `description`, `keywords`,
`date_published`, `date_modified`, `og_image`, `series_no`, `primary_query`,
`internal_links[]`, `figures[{src,alt,width,height,caption}]`,
`cta{text,href_suffix}`, `faq[{q,a}]`, `sources[]`.

**Markdown dialect (deliberately tiny):** `##`/`###`, `**bold**`, `*em*`,
`> blockquote`, `- list`, `![alt](src "caption")`, `[text](page.html)`,
`{{CTA}}`, `{{SOURCES}}`, `{{FAQ}}`.

**Assembly (clone, do not rewrite):**
- `<head>`: title, description, keywords, robots, OG, Twitter card, canonical,
  favicon, Bootstrap CDN **with the existing integrity hash**,
  `css/styles-custom.css` only (no `css/comments.css` on series pages).
- JSON-LD: `Article`, `BreadcrumbList`, `Article.citation` → `Book` (the 1894
  volume), `Article.about` → `{"@type":"Thing","name":"Nikola Tesla"}`, `FAQPage`
  when `faq` present; hub additionally gets `ItemList` (12) + `Book` + `Offer` price 0.
- Body: navbar (new page added to the "Pages" dropdown), `<article>` with H1 +
  kicker + published line, converted body, figures in
  `<figure class="mb-4 pt-5">`, **no comments section**, scarcity widget (kept for
  shell consistency — see §15 open item O3), sidebar (square ad, email capture,
  Popular Pages, news, tower ad), footer.
- Affiliate links get `?tid=<tid>` and `rel="noopener noreferrer nofollow"`.

**`--wire` also updates:** `articles.html` (card), nav dropdown, `sitemap.xml`
(`<url>` + `lastmod`), `_redirects` (pretty slug 301), `llms.txt` (series list).

**Safety:** writes only the target file; refuses to overwrite anything not listed
in `new_content/1894-series/index.json` unless `--force`; prints a diff summary
(bytes, internal links, images, headings).

**Self-test:** fixture md → assert valid HTML (balanced tags), exactly one `<h1>`,
every `<img>` has `alt`/`width`/`height`/`loading`, JSON-LD parses, ≥ 4 internal
links, no `http://` links, no `localhost`.

---

## 8. Per-article runbook (~45–60 min each, with vision)

1. Read the brief (§9) + Appendix A quotes for that page range.
2. **Re-grep every quote** you will use:
   `python3 books/tools/grep_quote.py "attach their machinery"` → printed page +
   context. Normalise OCR, record the page.
3. **Pick figures** from `manifest_qc.csv` (`verdict=keep*`, `quality A|B`, right
   page range) → 2–3. If short: patent drawing (§6.3) or a page-scan crop.
4. **Draft** `new_content/1894-series/NN-slug/article.md` against the outline.
5. **Render:** `make_article.py … --wire`.
6. **Numeric QA:** `python3 books/tools/qa_page.py website/<slug>.html` →
   title ≤ 60, description ≤ 155, one H1, images complete, ≥ 4 internal links,
   JSON-LD parses, HTML < 200 KB, images < 400 KB total, no broken relative links.
7. **Visual QA:** `shot_qa.py <slug>` → review 3 screenshots + every figure crop.
8. **Commit** (site repo): page + assets + sitemap/redirects/nav/llms.txt.
9. **Log** in `new_content/1894-series/index.json`: slug, date, word count,
   figures used, quotes with pages, internal links, `tid`.

---

## 9. The 12 flagship briefs

Common to all: `tid=1894_NN`, donor template, series kicker, Sources block,
comments block, one OG image. Word counts are targets, not floors. Figure
filenames are the shortlist from Appendix C — confirm the subject visually before
using.

---

### HUB — `tesla-1894.html`
**Title (50):** The 1894 File: Tesla's First Big Book, Page by Page
**Description:** We hold a scan of the 1894 first edition of Tesla's great book, read it page by page and cite it. Twelve articles, 120 original engravings, free PDF.
**OG:** `assets/og/tesla-1894.webp` (title page + plate p. 478)

Purpose: index + credibility proof. **No book download** (decision D4).

1. What this book is — imprint: Van Nostrand, entered 1893, printed 1894, editor
   T. C. Martin (editor of *The Electrical Engineer*, past-president AIEE);
   dedication "to his countrymen in Eastern Europe". Cite files 5–10.
2. Why a series off it — we have the scan and the OCR (177,000 words), we cite
   printed pages, we show the engravings.
3. The 12 articles as cards (ItemList schema).
4. "How we cite" trust box — the page-offset rule, the OCR-correction policy, and
   the word-search method (links to `tesla-1894-word-search.html`).
5. Figure gallery teaser → `tesla-1894-plates.html` (Tier 6, 60 engravings).
6. Where to go next — one paragraph bridging to the money pages, standard CTA.

The archive.org item is linked (they host the scan; we do not mirror 35 MB). No
`Book`/`Offer` schema, no PDF asset, no download button.

Figures: title-page crop, `tesla1894-plate-p478.webp`, 3 article thumbnails.
Links: all 12 + `magnetic-generator-plans-review.html` + `electrical-experimenter.html`.

---

### 01 — `tesla-lit-lamps-without-wires.html`
**Title (46):** Tesla Lit Lamps by Holding Them: The 1891 Proof
**Queries:** tesla light bulb in hand · tesla lamp without wires · tesla 1891
lecture · how did tesla light bulbs without wires
**Words:** 1,400 · **tid:** `1894_01`

1. **What he did on stage** — p. 200: "Here is a simple glass tube from which the
   air has been partially exhausted. I take hold of it… the tube in my hand is
   brilliantly lighted."
2. **The trick is not a trick** — electrostatic induction plus capacitance, with
   his body as one electrode. p. 184: the insulated body "serves to give off the
   energy into the surrounding space, and is equivalent to a return wire."
3. **He could wipe the light out with his hand** — p. 186: "the singular effect of
   wiping out the light of the tube may be produced by passing the hand quickly
   along the tube"; and a distant tube lit "by simply stepping between it and the
   coil."
4. **Why he opened and closed with this** — p. 288: "the most fascinating for an
   audience… the best an unskilled lecturer can do is to begin and finish with"
   these effects.
5. **What the internet gets wrong** — it is not energy from the aether; it is a
   resonant high-voltage supply using the room as return path. Include the safety
   fact from p. 125 (the coil shock was so mild you got only "a small burn") and
   state plainly: do not try this.
6. **Where you meet this today** — neon transformers, touch lamps, the physics of
   capacitance coupling → `magnetic-dynamo-generator.html`.
7. Sources.

Figures: `tesla1894-p154-fig99`, `tesla1894-p153-fig97`, `tesla1894-p179-fig117`.
Links out: `magnetic-dynamo-generator.html`, `electricity-using-magnets.html`, 06, 12.
⚠ needs source: audience size. The book gives venue and society, not headcount.

---

### 02 — `tesla-one-wire-power.html`
**Title (52):** Tesla's One-Wire Power: The Experiment Textbooks Skip
**Queries:** one wire circuit · does electricity need a return path · tesla single
wire · power a lamp with one wire
**Words:** 1,500 · **tid:** `1894_02`

1. **The rule you were taught**, and the exception Tesla exploited.
2. **His statement** — p. 232: "A most curious feature of alternate currents of
   high frequencies and potentials is that they enable us to perform many
   experiments by the use of one wire only."
3. **What he actually did with it** — p. 236: an insulated line carrying an
   "inappreciable current" on which "on any point of the same we are able to obtain
   a heavy current, capable of fusing a thick copper wire"; single-pole
   electrolysis; lighting a lamp or exhausted tube from the line.
4. **Why it is not magic** — displacement current through the capacitance of the
   line and the room; the return path is there, it is just not a copper wire.
   Quote p. 184 ("equivalent to a return wire").
5. **Tesla's own economic case for one wire** — p. 267: high frequency makes
   conductor loss worse, so "economical reasons will make it advisable to use only
   one wire, especially if the distances are great."
6. **What the internet gets wrong** — single-wire distribution is real physics and
   still not a free-energy loophole; the missing conductor is the environment, and
   the losses are real.
7. **Bridge** — what this means for a home wiring project (you still need a return
   conductor at 50/60 Hz) → `diy-magnetic-generator.html`.
8. Sources.

Figures: `tesla1894-p263-fig153`, `tesla1894-p247-fig151`, `tesla1894-p228-fig144`
+ patent US 454,622 or 464,666 (verify number).
Links out: `diy-magnetic-generator.html`,
`can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html`, 11, hub.

---

### 03 — `tesla-earthquake-machine.html`
**Title (52):** Tesla's Earthquake Machine: What the 1893 Record Says
**Queries:** tesla earthquake machine · tesla mechanical oscillator · tesla
oscillator 1893 · tesla resonance machine
**Words:** 1,700 · **tid:** `1894_03` · **FAQ schema:** yes

1. **The 1893 account, first-hand** — World's Fair, Electrical Congress, Friday
   Aug 25 1893, introduced by Elisha Gray (p. 486).
2. **What the machine was** — piston in a cylinder, air spring, isochronous
   vibration independent of pressure; "a steel arbor… actually torn apart while
   vibrating against a minute air cushion" (p. 486).
3. **The numbers** — ~20 lb weight at ~80 vibrations per second, ~3/8 in stroke,
   "many hundred times" with a shorter stroke (p. 487); behaviour like a stretched
   string with fixed nodes (p. 487); a clock driven by it keeping correct time
   (p. 488).
4. **Why it mattered then** — a constant-period alternator without spark gaps;
   superseded by the steam turbine (state as context, cite a modern source).
5. **The earthquake story, dated properly** — Tesla told it in 1935 at age 79;
   first printed in O'Neill's *Prodigal Genius* (1944), pp. 162–164; the 1893–94
   record says nothing of the kind. Patent US 514,169 (Feb 6 1894).
6. **What the internet gets wrong** — the sledgehammer/police/multi-ton basement
   details are variants of a late-life anecdote; *MythBusters* ep. 60 (2006) built
   one: real vibrations felt hundreds of feet away, no earthquake on the bridge
   tested.
7. **Resonance is not over-unity** — the honest physics bridge →
   `perpetual-motion-generator.html`, `magnet-motor.html`.
8. Sources.

Figures: `tesla1894-p491-fig313` (only book engraving), `patents/us514169-*.webp`,
plus a page-scan crop of p. 486 (drop-cap lecture report).
Links out: `perpetual-motion-generator.html`, `magnet-motor.html`, 09, 11.
⚠ needs source: the steam-turbine replacement claim and the MythBusters result —
cite Carlson (2013) and mythresults.com respectively.

---

### 04 — `tesla-wireless-power-1893.html`
**Title (51):** Tesla's Wireless Power Plan, In His Own Words (1893)
**Queries:** tesla wireless transmission of energy · did tesla invent wireless
power · tesla world system · tesla earth conduction
**Words:** 1,600 · **tid:** `1894_04` · **FAQ schema:** yes

1. **The paragraph nobody quotes** — p. 138, in full: "Experiments of this kind
   seem to bring it within possibility to operate a motor at any point of the
   earth's surface from a central source, without any connection to the same except
   through the earth… The experiment, which would be one of great scientific
   interest, would probably best succeed on a ship at sea."
2. **The apparatus behind the claim** — the high-potential coil, the insulated
   plate, the rotating disc experiment described on the same page.
3. **His transmission arithmetic** — p. 151: at "a few thousand volts there is no
   particular difficulty encountered in conveying currents from a machine giving,
   say, 20,000 alternations per second, to quite a distance. This number of
   alternations, however, is by far too small for many purposes."
4. **The ambition, in his own rhetoric** — pp. 196–197: "the time has come when
   one may utter such words before an enlightened audience without being
   considered a visionary. We are whirling through endless space… everywhere is
   energy."
5. **What the internet gets wrong** — the 1893–94 record is a *proposal with
   conditions*, not a demonstrated power system; the later Wardenclyffe episode is
   a different, better-documented story (cite a modern source, do not invent).
6. **Why it did not happen** — frequency-dependent loss, insulation limits
   (Tesla says so himself, p. 151), and the economics of 50/60 Hz copper.
7. **Bridge** — what a realistic off-grid setup looks like today →
   `whole-house.html`, `solar.html`.
8. Sources.

Figures: `tesla1894-p154-fig99`, `tesla1894-p179-fig117`, one elevation/earth-current
engraving from pp. 183–190 (pick visually).
Links out: `whole-house.html`, `solar.html`, 02, 11.

---

### 05 — `tesla-high-frequency-massage.html`
**Title (45):** Tesla's High-Frequency "Massage" Cure of 1891
**Queries:** tesla high frequency current therapy · violet ray history ·
electrotherapy 1890s · tesla electrotherapy
**Words:** 1,300 · **tid:** `1894_05`

1. **The paper, and its defensive opening** — *The Electrical Engineer*, Dec 23
   1891; p. 394: "I trust that the present brief communication will not be
   interpreted as an effort on my part to put myself on record as a 'patent
   medicine' man, for a serious worker cannot despise anything more than the misuse
   and abuse of electricity which we have frequent occasion to witness."
2. **The mechanism he described** — heating of an insulated body in contact with a
   source of rapidly alternating high potential, by "bombardment" of the air;
   "the human body is, in such a case, a fine conductor" (p. 394).
3. **The North Pole thought experiment** — p. 395: "it is conceivable that a
   person entirely nude at the North Pole might keep himself comfortably warm in
   this manner."
4. **What he explicitly did not claim** — "Without vouching for all the results,
   which must, of course, be determined by experience and observation" (p. 395).
   This is the whole point of the piece: Tesla hedged; the market did not.
5. **What the internet gets wrong** — modern "Tesla frequency healing" products
   sell what Tesla explicitly refused to vouch for. Note the later legitimate
   descendant (short-wave diathermy in medicine) **with a modern source**, and
   keep it clearly separate from the wellness claims.
6. **Bridge** — how to spot a modern overclaim, and how our own pages handle it →
   `magnetic-generator-scam.html`.
7. Sources.

Figures: no book engravings in Ch. XXXI. Use a page-scan crop of p. 394 (the
"patent medicine" paragraph) + one high-frequency electrode patent drawing
(verify number) + `tesla1894-p392-fig208` (electrostatic induction apparatus,
Ch. XXX, adjacent chapter).
Links out: `magnetic-generator-scam.html`,
`How-Much-Noise-Does-a-Free-Energy-Device-Make.html`, 10.

---

### 06 — `tesla-cold-flame.html`
**Title (46):** The Flame That Doesn't Burn: Tesla's Cold Fire
**Queries:** electric flame · corona discharge flame · cold fire physics ·
tesla flame without combustion
**Words:** 1,200 · **tid:** `1894_06`

1. **The stage moment** — p. 258: "The brush was a flame, a source of heat and
   light. It did not emit much perceptible heat, nor did it glow with an intense
   light; but is it the less a flame because it does not scorch my hand?"
2. **What a brush actually is** — corona: ionised air, photon emission, very little
   energy per unit area. Explain in plain English, no hand-waving.
3. **Tesla's bigger idea** — p. 167: "a veritable flame, which would give light and
   heat without any material being consumed, without any chemical process taking
   place… we only need to perfect methods of producing enormous frequencies and
   potentials."
4. **Why he never got it** — he says why himself: the potential and frequency
   needed were beyond the machinery of 1893 (cross-ref Ch. XXIX, article 11).
5. **What the internet gets wrong** — "cold fire" videos today are ordinary corona
   or plasma; nothing violates combustion physics; and Tesla's "flame without
   chemical process" is about the light source, not about free energy.
6. **Where you see it now** — corona rings on high-voltage lines, ozone generators,
   plasma globes → `7-interesting-facts-about-magnets.html`.
7. Sources.

Figures: `tesla1894-p247-fig151`, `tesla1894-p228-fig144`, `tesla1894-p179-fig117`
(verify which show brush discharge visually).
Links out: `7-interesting-facts-about-magnets.html`, 01, 12.

---

### 07 — `rotating-magnetic-field-1888.html`
**Title (47):** The Paper Tesla Scribbled in Pencil: How AC Won
**Queries:** tesla rotating magnetic field explained · how does an ac induction
motor work · tesla 1888 paper aiee · tesla polyphase system history
**Words:** 1,700 · **tid:** `1894_07` · **FAQ schema:** yes

1. **The anecdote nobody tells** — Martin, who was chairman of the AIEE papers
   committee, had "great difficulty in inducing Mr. Tesla to give the Institute any
   paper at all"; Tesla was "overworked and ill" and "manifested the greatest
   reluctance"; the paper "was written the night previous to the meeting, in pencil,
   very hastily" (p. 27).
2. **What the paper actually contained** — the rotating field, motors with closed
   conductors, synchronising motors, rotating-field transformers (Ch. III, p. 9).
3. **The idea in one paragraph, drawn properly** — a field that travels in a
   circle; a caged conductor that chases it forever. Use the book's own diagrams.
4. **The efficiency climb, in public** — p. 8: Prof. Anthony's 1888 tests, ~50% and
   "a little over sixty per cent"; 1889 Pittsburgh tests with Albert Schmid, motors
   up to 10 HP at ~850 lb, "nearly 90 per cent"; larger three-wire machines "as high
   as 94 and 95 per cent".
5. **Why that table matters** — this is the honest benchmark for any "build it at
   home" claim: real AC machines took five years and industrial tooling to reach
   90%+.
6. **What the internet gets wrong** — the "Tesla magnetic generator" phrase does
   not appear in the 1894 book; what is in it is an induction motor and transformer
   system, measured in public.
7. **Bridge** — what a real home generator can and cannot do →
   `magnetic-dynamo-generator.html`, `magnetic-generator-plans-review.html`,
   `tesla-magnetic-generator-worth-it.html`.
8. Sources.

Figures: `tesla1894-p28-fig23`, `tesla1894-p27-fig24`, `tesla1894-p16-fig9`,
`tesla1894-p19-fig13` + one 1888 patent plate (US 381,968 family, verify).
Links out: `magnetic-dynamo-generator.html`, `magnetic-generator-plans-review.html`,
`tesla-magnetic-generator-worth-it.html`, 11.

---

### 08 — `tesla-weird-inventions-1894.html`
**Title (49):** 9 Tesla Inventions From 1894 That Never Caught On
**Queries:** tesla lesser known inventions · weird tesla inventions · tesla facts
list · tesla failed inventions
**Words:** 1,500 (listicle) · **tid:** `1894_08`

Nine entries, each ~130 words: what it was, one page-cited detail, why it lost.

| # | Invention | Page | The hook |
|---|---|---|---|
| 1 | Getting DC directly from AC | 409 | before solid-state rectifiers |
| 2 | Condensers with the plates in oil | 418 | the reason your capacitor is not in air |
| 3 | Electrolytic registering meter | 420 | an amp-hour meter that counts bubbles |
| 4 | Thermo-magnetic motor / pyromagnetic generator | 424–431 | a spirit lamp under an L-shaped iron strip, "oscillating as rapidly as 400 to 500 times a minute" (p. 424) |
| 5 | Anti-sparking brush and commutator | 432 | the problem every DC motor had |
| 6 | Auxiliary-brush regulation of DC dynamos | 438 | |
| 7 | Improvement in dynamo and motor construction | 448 | |
| 8 | Tesla's DC arc lighting system | 451 | |
| 9 | Unipolar (homopolar) generators | 465 | the disc that spins without commutation |

Closing beat: the only "…magnetic generator" in the whole 1894 volume is the
**pyro**magnetic generator (pp. 424–431) — heat-driven, not magnet-driven. Nobody
selling "Tesla magnetic generators" has ever mentioned it. Bridge →
`magnet-motor.html`, `perpetual-motion-generator.html`, 10.

Figures: one engraving per entry (candidates in App. C: `p422-fig230`,
`p434-fig247`, `p446-fig266`, `p457-fig281`, `p460-fig283`, `p466-fig290`).

---

### 09 — `tesla-worlds-fair-1893.html`
**Title (49):** Tesla's 1893 World's Fair Exhibit, Walked Through
**Queries:** tesla 1893 world's fair chicago · westinghouse alternating current
world's fair · tesla exhibit 1893 · tesla white city
**Words:** 1,500 · **tid:** `1894_09`

Structure: a walk through the exhibit, item by item, as Martin describes it
(Ch. XLII, pp. 477–485).

1. Where the exhibit sat — "part of the space of the Westinghouse Company" (p. 477).
2. Item A/B: the rings, plus a rotating magnet on bearings demonstrating "the
   identity between a rotating field and a rotating magnet" (p. 479).
3. Item C: one model that is simultaneously a two-phase motor, an induction motor
   and a transformer — two superimposed separated windings; as an induction motor
   "the motor operated with only two wires" (p. 479).
4. Item D/E: earliest rotating-field motors, one regulating an arc lamp, with one
   set of coils in German silver and the other in copper to get different
   self-inductions (p. 479).
5. Item F: the magnetic-lag motor — field and armature "repel each other and
   rotation is produced in this way" (p. 479).
6. The full-page plate (printed p. 478) reproduced large.
7. **What the internet gets wrong** — the Fair is usually told as the AC/DC PR
   war; the exhibit itself was a lecture in hardware, and this chapter is a
   contemporary walkthrough, which is rarer than any photo.
8. **Bridge** — the same machine, 130 years later, in your workshop →
   `build-a-magnetic-generator.html`, `magnetic-generator-plans-review.html`.
9. Sources.

Figures: `tesla1894-plate-p478`, `tesla1894-p480-fig298`, `tesla1894-p481-fig297`,
`tesla1894-p484-fig*` (verify visually; the OCR mis-reads one caption as "Fig. 811").
Links out: `build-a-magnetic-generator.html`, `magnetic-generator-plans-review.html`, 03, 07.
⚠ needs source: any claim about lighting the Fair itself (not in this chapter).

---

### 10 — `tesla-free-energy-what-he-said.html`
**Title (48):** We Read Tesla's 1894 Book Looking for Free Energy
**Queries:** did tesla invent free energy · tesla free energy machine true or
false · tesla wheelwork of nature · tesla magnetic generator real or fake
**Words:** 1,800 · **tid:** `1894_10` · **FAQ schema:** yes · **the trust piece**
**Slot depends on O2** — default is 4th published, with the softer title *What
Tesla Actually Wrote About Free Energy* (43). If O2 = C, this brief becomes a
rewrite of `magnetic-generator-scam.html` instead, and the data itself moves to
`tesla-1894-word-search.html`.

1. **The method, stated up front** — we hold the 1894 first edition as 518 page
   scans and 177,000 words of text; here is what a word search returns.
2. **The table** (re-run at publish time, show the counts):

   | search term | hits |
   |---|---|
   | "free energy" / "free-energy" | 0 |
   | "perpetual" | 0 |
   | "over unity" / "over-unity" | 0 |
   | "magnetic generator" | 5 — all of them **pyro**magnetic (pp. 6, 424, 429, 496) |

3. **The quote everyone posts, uncut** — p. 236: "Throughout space there is
   energy… attach their machinery to the very wheelwork of nature" — followed
   immediately by Crookes' radiometer, "the most interesting" and "the most
   inefficient machine ever invented!" Tesla is warning, not promising.
4. **What he did claim** — energy from the medium (pp. 196–197), one-wire
   transmission (pp. 232, 267), earth-potential motors (p. 138), a flame without
   combustion (p. 167). For each: what he said, what he demonstrated, what
   happened.
5. **The pyromagnetic twist** — the only "…magnetic generator" in the book is a
   heat engine (pp. 424–431).
6. **What the internet gets wrong** — the phrase "Tesla magnetic generator" is a
   21st-century product name, not a Tesla term.
7. **The honest pivot** — what actually works off-grid, what the plans on this
   site are and are not → `magnetic-generator-scam.html`,
   `tesla-magnetic-generator-worth-it.html`, `free-electricity-from-magnets.html`.
8. Sources + a link to the appendix page that proves the word search (Tier 6).

Figures: page-scan crop of p. 236 (the radiometer passage), `tesla1894-p424-fig*`
(pyromagnetic), title page.

---

### 11 — `tesla-high-frequency-alternator.html`
**Title (51):** 30,000 Alternations a Second: Tesla's Lost Generator
**Queries:** tesla alternator frequency · high frequency alternator · how many
hertz does a tesla coil use · tesla high frequency machine
**Words:** 1,400 · **tid:** `1894_11` · **FAQ schema:** yes

1. **Why he needed it** — arc lamps on AC "emit a pronounced sound" from rapid
   heating and cooling of the arc gases, and small arcs are impracticable at low
   frequency; high frequency gives arcs "the advantages of silence and
   persistency" (p. 374).
2. **The machine** — annular magnetic frame, many small poles, field wire wound
   zigzag through grooves (Ch. XXIX, pp. 374–376; Figs. 199–203).
3. **The numbers** — "Up to about 15,000 alternations per second in an experimental
   machine…" (p. 376); "the field had 480 polar projections on each side, and from
   this machine it was possible to obtain 30,000 alternations per second" (p. 381);
   eddy-current limits forcing "very thin wires or sheets" (p. 381).
4. **What it bought him** — p. 391: two bare wires twenty feet long, 2 mm
   diameter, one end to the machine, the other to a condenser; and p. 151 on
   conveying 20,000 alternations per second "to quite a distance" at a few thousand
   volts.
5. **Why it died** — rotating machines at 30,000 Hz fight the mechanical limits of
   iron and balance; spark gaps and, later, electronics won. State with a modern
   source.
6. **What the internet gets wrong** — "Tesla coil frequency" is usually quoted as
   a single number; Tesla's own machines ran from a few hundred to 30,000
   alternations per second, and he says the low end was "by far too small for many
   purposes" (p. 151).
7. **Bridge** → `magnetic-generator-plans-review.html`, `magnetic-dynamo-generator.html`.
8. Sources.

Figures: `tesla1894-p375-fig203`, `tesla1894-p376-fig200`, `tesla1894-p379-fig207`,
`tesla1894-p378-fig205`.

---

### 12 — `tesla-glowing-tubes-vacuum.html`
**Title (48):** Glowing Glass in Tesla's Bare Hand: 1894's Tubes
**Queries:** tesla vacuum tube experiment · geissler tube tesla · why does a bulb
glow without wires · tesla phosphorescence
**Words:** 1,300 · **tid:** `1894_12` · **FAQ schema:** yes

1. **The strangest demo** — p. 288: "I take a tube in my hand and move it about,
   and it is lighted wherever I may hold it… I may put it away for a few weeks or
   months, still it retains the faculty of being excited. What change have I
   produced in the tube?"
2. **Why a tube lights with no wires** — gas discharge, mean free path, striae,
   phosphorescent coatings; the tube is one plate of a capacitor.
3. **Tesla's lamp research** — p. 255: carborundum filaments, "thin threads or
   sticks of carborundum", and buttons made of diamond dust that "came in
   durability nearest to those prepared of carborundum".
4. **The vacuum problem** — p. 288: a tube with too good a vacuum will not light
   until "excited" by a disruptive discharge coil.
5. **What the internet gets wrong** — these are not "light without energy"; the
   energy is capacitively coupled from the coil, and the persistent excitation is
   a charge/ionisation state, not stored free power.
6. **Bridge** → `free-electricity-from-magnets.html`, `electricity-using-magnets.html`.
7. Sources.

Figures: `tesla1894-p400-fig215`, `tesla1894-p403-fig218`, `tesla1894-p398-fig212`,
`tesla1894-p397-fig210`.
⚠ needs source: any X-ray/Röntgen connection — do not assert without a citation.

---

## 10. Backlog: the next 40 topics (so we never run dry)

Mined from all 43 chapters. **60 distinct topics exist; ship ~40** (12 flagship +
the 28 below), then stop before cannibalisation.

### Tier 2 — engineering explainers (Part I, pp. 9–118, 60 figures) — 10

| Slug | Topic | Anchor pages |
|---|---|---|
| `tesla-rotating-field-diagrams` | The rotating magnetic field, drawn the way Tesla drew it | 9–25 |
| `why-induction-motors-need-closed-conductors` | the squirrel-cage origin story | 9–25 |
| `synchronizing-vs-torque-motors-1890s` | the Victorian stepper-vs-induction split | 50–57 |
| `capacitors-single-phase-motors` | condensers were the original single-phase fix | 101–108 |
| `magnetic-lag-and-shielding` | Tesla's phase-shift hacks | 67–75 |
| `motor-speed-is-poles-not-effort` | frequency/pole arithmetic | 36–44 |
| `rotary-converters-dc-to-polyphase` | getting polyphase from a DC plant | 31–35 |
| `tesla-polyphase-transformer` | Ch. XXIII | 109–112 |
| `constant-current-transformer` | the regulator that ran street lighting | 113–118 |
| `ac-efficiency-1888-1893` | the measured climb 50% → 95% | 8 |

### Tier 3 — one demo per article (the lectures, pp. 145–373, 71 figures) — 14

`tesla-radiometer-light-mill` (p. 236) · `tesla-earth-as-conductor` (p. 138) ·
`tesla-silent-arcs` (p. 374) · `tesla-phosphorescent-colours` (Ch. XXXII) ·
`tesla-electrostatic-induction-coil` (Ch. XXX, p. 392) ·
`tesla-one-wire-electrolysis` (p. 236) · `tesla-fusing-copper-wire` (p. 236) ·
`tesla-stepping-a-tube-into-light` (p. 186) · `tesla-screening-effects` (p. 186) ·
`tesla-insulation-problems` (pp. 164, 169) · `tesla-carborundum-lamps` (p. 255) ·
`tesla-diamond-dust-electrodes` (p. 255) · `tesla-telephone-hum` (p. 189) ·
`tesla-lecture-showmanship` (p. 288).

### Tier 4 — the forgotten inventions (Part III, pp. 409–476) — 9

`tesla-dc-from-ac` (409) · `tesla-oil-condensers` (418) ·
`tesla-electrolytic-meter` (420) · `tesla-pyromagnetic-generator` (424–431) ·
`tesla-anti-sparking-brush` (432) · `tesla-auxiliary-brush-regulation` (438) ·
`tesla-dynamo-construction` (448) · `tesla-dc-arc-lighting` (451) ·
`tesla-unipolar-generator` (465).

### Tier 5 — biography, provenance, exhibits — 6

`tesla-biography-1894` (pp. 1–8, as Martin wrote it; note it says born 1857, which
is why sources disagree — handle explicitly) ·
`tesla-dedication-eastern-europe` (front matter) ·
`who-was-thomas-commerford-martin` · `tesla-worlds-fair-exhibit-detail` (477–485,
deep dive beyond flagship 09) · `tesla-oscillator-lecture-1893` (486–495,
transcript-style) · `how-the-1894-book-was-made` (imprint, copyright 1893,
Van Nostrand, press of McIlroy & Emmet).

### Tier 6 — galleries, listicles, hubs, resources — 9

`tesla-1894-plates` (60 engravings, page-cited; §16.3 linkable asset) ·
`tesla-1894-word-search` (the proof/data page; §16.3) ·
`tesla-1894-part1-text` (Part I, pp. 1–118, clean HTML; §16.3) ·
`tesla-quotes-with-page-numbers` (12 quotes) · `tesla-1894-page-scans` (the
lecture climax, pp. 196–197) · `tesla-1894-reading-list` (hub-adjacent resource) ·
`tesla-1894-vs-1919` (book vs the *Electrical Experimenter* issue we already give
away) · `tesla-1888-1894-timeline` · `tesla-1894-glossary` (alternations,
electro-dynamic inductive effect, displacement, magnification, etc.).

Plus one non-HTML asset: the **GitHub `tesla1894` repo** (§16.3).

### What we deliberately do not write

- Any variant of "how to build a free energy device".
- Three near-identical "Tesla induction motor variant" posts.
- Anything that needs a claim we cannot page-cite or datasheet-cite.

---

## 11. Sessions and throughput (with vision)

| Mode | Per session | Notes |
|---|---|---|
| Drafts only | 10–12 | markdown + re-grepped quotes + figure shortlist |
| **Fully produced (default)** | **4–5** | runbook §8 end-to-end, incl. visual QA |
| Session 1 (build the machine) | 2 | `make_article.py`, `qa_page.py`, `shot_qa.py`, `contact_sheet.py`, figure QC pass, then hub + 10 |

**Session plan**

| Session | Output |
|---|---|
| S1 | tooling (`make_article.py`, `qa_page.py`, `shot_qa.py`, `contact_sheet.py`, `grep_quote.py`) + figure QC (contact sheets, `manifest_qc.csv`) + hub + article 03 |
| S2 | 01, 07 + patent-drawing supplement (US 514,169, 1888 polyphase family) |
| S3 | 02, 04, 11 |
| S4 | 10 (if O2 = A/B), 09, 08 |
| S5 | 12, 05, 06 + OG images for all 12 + backlink pass on 8 existing pages |
| S6 | linkable assets: `tesla-1894-plates`, `tesla-1894-word-search`, `tesla-1894-part1-text`, GitHub `tesla1894` repo + first outreach batch (20 sends) |
| S7+ | Tier 2/3/4 at 4–5 per session, 2 shipped per week; outreach continues |

Ship cadence: **2 per week**, flagship first, never more than 2 in a day —
publishing velocity itself looks spammy. If O2 = A, article 10 moves to S1
alongside the hub; if O2 = C, S4 gains 05 and `magnetic-generator-scam.html` gets
a rewrite session instead.

---

## 12. QA gates (all must pass before deploy)

**Numeric (`qa_page.py`)**
- title ≤ 60 chars; description 120–155; exactly one `<h1>`; H2 count 5–9
- ≥ 4 internal links, ≥ 3 of them to pages that link back (per §5.2)
- every `<img>`: `alt`, `width`, `height`, `loading="lazy"`, file exists
- ≥ 3 page-cited quotes matching regex `\(1894, p\. \d+\)`
- Sources block present; archive.org item string present
- JSON-LD parses; `Article.citation` present; `FAQPage` valid when used
- **no comments block and no `css/comments.css` link** on series pages
- no book-PDF link anywhere in the series
- HTML < 200 KB; total image weight on page < 400 KB; no `http://` links
- affiliate link has `tid=1894_NN` and `rel="noopener noreferrer nofollow"`

**Visual (me, with vision)**
- each figure crop: subject correct, no page-edge junk, no caption bleeding in,
  lines sharp, aspect not distorted
- captions match what the engraving actually shows (never trust the OCR caption)
- desktop/tablet/mobile screenshots: nav dropdown intact, figures inside column,
  captions legible, sidebar stacking, CTA visible on mobile first screen
- OG image: title readable at 300 px wide

**Human (you)**
- approve the figure set per article (3 thumbnails, ~1 min)
- approve any sentence that touches what the product can do

---

## 13. Measurement

- **GSC per page** at day 14 / 30 / 60: distinct queries with impressions, median
  position. Pass = ≥ 10 queries and median < 15 by day 30.
- **Cluster lift:** does domain-wide `tesla *` query coverage grow from ~130 terms?
- **Money:** ClickBank `tid=1894_NN` per article; GA4 event on internal link click
  (series → money page), target ≥ 5% of readers; ≥ 3 attributed sales in 60 days.
- **Answer engines:** monthly probe set — "did Nikola Tesla invent free energy",
  "tesla earthquake machine real", "tesla one wire experiment", "tesla 1894 book",
  "how many hertz tesla coil" — log whether we are cited and with which page.
- **Kill switch:** any article at median position > 30 after 60 days gets one
  rewrite (title + first 200 words + one new figure + one new section), never a
  thin sibling post.
- **Log:** `new_content/1894-series/index.json` + a monthly note in `PROGRESS.md`.

---

## 14. Risks

| Risk | Mitigation |
|---|---|
| Figure crops turn out to be fragments or wrong subjects | vision QC pass (§6.2) before any article uses them; patent-drawing fallback (§6.3) |
| OCR misquote ships publicly | every quote re-grepped at write time (`grep_quote.py`); Appendix A is the only approved source |
| Series cannibalises the money pages | link map §5.2 forces series → money links; monitor money-page impressions weekly |
| Trust piece (10) hurts conversions | measure `tid=1894_10` and money-page CTR; if it drops, reframe the pivot section, do not delete the page |
| Publishing velocity looks spammy | 2/week cap |
| Affiliate/FTC exposure | disclosure line above every CTA; no new performance claims |
| OCR text layer missing on 12 pages | those pages are covers/blanks/plates; use them as plate images, never as text |
| Book PDF not published (D4) → hub has no lead magnet | hub leans on the "how we cite" trust box; capture stays on the sidebar widget; §16.3 assets carry the traffic/citation load |
| Someone builds the satellite-link idea later | §16.2 states the policy: no owned-domain links to the money site, no shared infrastructure |

---

## 15. Decision log

### Decided (2026-10-09)

**D3 — No comments on series pages.** Applied in §3.10, §7 (head and body
assembly), §12 (QA gate now asserts their absence). Side benefit: no fabricated
endorsements on the evidence-led pages. Existing pages keep their current comment
blocks untouched.

**D4 — No book download.** The hub becomes index + "how we cite" trust box; we
link the archive.org item instead of mirroring 35 MB. Applied in §1, §5 diagram,
§9 hub brief. Consequences: no `gs` rebuild, no `Book`/`Offer` schema, no PDF
asset, and the hub loses its lead-magnet role — capture falls back to the standard
sidebar widget, and §16.3 becomes the traffic/citation engine instead.

**D5 — Image sourcing.** Every article gets 2–3 relevant images placed in the
body. Primary source is our own 200 crops from the 1894 scans. Where a topic has
no book illustration (Ch. XXXI "massage" has none; Ch. XLIII oscillator has one),
we supplement with public-domain Tesla patent drawings. Rules: confirm the patent
number on patents.google.com before use; credit `US patent NNN,NNN (year), Nikola
Tesla.`; store in `website/assets/tesla1894/patents/`; keep the book visually
dominant — at most one patent plate per two 1894 engravings on a page. Last
resort is a page-scan crop of the relevant 1894 page (authentic, and useful when
the words themselves are the artefact, e.g. p. 236 or p. 394).

### Open

**O1 — Series name** (decide by end of S1; it appears in exactly 4 places: the
kicker string, the hub H1 + meta, `llms.txt`, the GitHub README — never in a URL,
so changing it later is a 10-minute job).

| Option | For | Against |
|---|---|---|
| **The 1894 File** (working name) | short, memorable, reads well as a kicker and a hub title, makes no commercial claim | no search demand for the phrase (irrelevant — series names are not queries) |
| Tesla Magnetic Generator Archives | brand-tied, reinforces the product name | long; attaches a product name to pages whose value is neutrality; and it collides with the fact that the 1894 book never uses that phrase |
| The Van Nostrand Papers / First Edition Files | scholarly flavour, distinctive | less memorable, harder to say out loud |

**O2 — Article 10 (the free-energy word search).** Three options:

| Option | Trust / answer-engine value | Conversion risk | Note |
|---|---|---|---|
| A. Flagship, published week 1 | high | small negative | strongest, but it is the page most likely to be read as attacking the product before the reader trusts us |
| **B. Keep it, publish 4th** (after 03, 01, 07), slightly softer title | high | smaller | recommended: the reader has already enjoyed three excellent history pieces first |
| C. Fold the evidence into `magnetic-generator-scam.html`, no new page | medium | none | that page is thin and currently framed wrong; we would be rewriting it, not adding to it |

Whichever you pick, `tesla-1894-word-search.html` (Tier 6) ships regardless — it
is the citable data asset, and it is what article 10 links to.

**O3 — Scarcity widget on series pages.** It is part of the donor shell. Keep it
on 01–09 and 11–12 for consistency and clicks; consider dropping it on 05 and 10,
where the whole article is about not being sold hype. Say which you prefer.

---

## 16. Distribution and link strategy

### 16.1 Verdict

The series lives on **teslamagneticgenerator.com**. Reasons:

- The site has no backlinks problem it can perceive: it already ranks 3–6 on its
  target terms, and those terms are worth 6–32 impressions. The ceiling is query
  coverage and trust, both of which are on-site properties.
- Internal links from series → money pages are the strongest, cheapest, most
  certain signal available to a 39-page site. Off-site hosting trades that
  certainty for a hoped-for link.
- The first-hand-sourcing advantage compounds on the domain that already has the
  money pages, the schema graph and the sitemap.

### 16.2 What we do not do

- No second WordPress/blog domain whose function is to link to the money site.
  Links you own are treated as self-created and discounted; the affiliate-plus-
  satellite pattern is the textbook example in Google's link-spam and
  site-reputation-abuse guidance, and a manual action would cost the 89-click and
  30-click pages we already have.
- No cross-linking between owned properties, no shared templates/host/registrant
  across domains, no expired-domain recycling, no syndication carrying affiliate
  links.
- Same writing effort, discounted signal, real downside risk. That is the whole
  argument against it.

### 16.3 Linkable assets (on-site) — the only link strategy worth having

Nobody links to an affiliate review. People link to primary sources.

1. **`tesla-1894-plates.html`** — 60 engravings, page-cited, in a lazy-loaded
   grid, each with printed page, book Fig. number and chapter, plus a
   downloadable ZIP (1200 px, ~15 MB) and a one-line licence statement:
   *Public domain (1894 imprint). Reuse freely; a credit line is appreciated.*
   Schema: `ImageObject` per item. This is the page teachers, heritage blogs and
   newsletters actually link.
2. **`tesla-1894-word-search.html`** — the data page: method, the counts table
   (Appendix D), and the exact command so anyone can reproduce it. Citable by
   anyone making Tesla-myth content.
3. **`tesla-1894-part1-text.html`** — Part I (pp. 1–118) as clean, readable HTML.
   Proof of every citation in the series, and a rare thing on the web.
4. **GitHub repo `tesla1894`** — the OCR text, `manifest_qc.csv`, and
   `extract_figures.py`, MIT-licensed, README linking to the hub. Researchers and
   developers link to working data; this is the one off-site property that earns
   links by being useful rather than by wanting them.

### 16.4 Outreach (offer-first, ~20 sends/week, no affiliate links in the mail)

| Target | The offer |
|---|---|
| Tesla Museum (Belgrade), Tesla Science Center at Wardenclyffe, nikolatesla.org | the plates ZIP + our page cites for anything they publish |
| History-of-science outlets (The Public Domain Review, Open Culture, The Online Books Page, IEEE Spectrum history) | engravings + the word-search data page |
| YouTube makers covering Tesla myths | free high-res engravings and page-cited quotes, credit line included |
| Reddit: r/HistoryOfScience, r/electricians, r/DIY, r/oldbooks | post the gallery or the word-search page, never a money page; obey each sub's self-promotion rules |
| Educators (physics-history pages, department resource lists) | the Part I text page + plates, with a citation block |

Pitch shape (3 sentences): what we made → what they can take and reuse for free →
link to the asset. No pitch, no affiliate link, no follow-up chain.

### 16.5 Owned distribution (traffic, not links)

- **YouTube:** the earthquake machine, lamps-in-hand, and one-wire stories are
  cheap video because the engravings are the visuals. `tid=social_yt`.
- **Pinterest:** quote cards and the plates gallery; vintage technical art
  performs well there. `tid=social_pin`.
- **Medium/Substack:** excerpt + canonical back to the main article, no affiliate
  links. Treat as discovery only — expect zero SEO link value.
- **Newsletter mentions** in adjacent newsletters (in-kind, not paid).

### 16.6 If you ever want the hedge property

Legitimate version: an independent archive domain (full text, figures, metadata,
search), **no affiliate links, no ClickBank, no monetisation at all**, one natural
footer link to the commentary on the main site. Different registrant, host and
analytics; no shared templates; no reciprocal links. It has to be a real public
utility, which means it is a second product, not a tactic. Defer until the main
domain is past ~20k impressions/month.

### 16.7 Measurement

- GA4: new referring domains/sessions; goal = 10 referring domains by week 12.
- GSC "most linked pages" + a weekly external-link check
  (`link:teslamagneticgenerator.com -site:teslamagneticgenerator.com` in a link
  tool) to confirm outreach is producing links, not just traffic.
- Answer-engine probes (monthly, 5 questions) — which of our pages get cited.
- Sales by `tid=1894_NN`, `tid=social_*`, `tid=outreach_*`.

---

## Appendix A — verified quote register

Full register with context: `books/extracted/quote-index.md`. Approved quotes and
their printed pages (re-grep before use):

| Page | Quote (truncated) |
|---|---|
| 8 | efficiency: ~50% and "a little over sixty per cent" (1888); "nearly 90 per cent" (1889); "as high as 94 and 95 per cent" |
| 8 | "An invention is none the less beautiful because it may lack utility…" |
| 27 | "The paper was written the night previous to the meeting, in pencil, very hastily…" |
| 125 | the coil shock "can be supported without any inconvenience, except perhaps a small burn" |
| 138 | "operate a motor at any point of the earth's surface… best succeed on a ship at sea" |
| 151 | "conveying currents from a machine giving, say, 20,000 alternations per second, to quite a distance" |
| 167 | "a veritable flame, which would give light and heat without any material being consumed" |
| 184 | the insulated body "is equivalent to a return wire" |
| 186 | "wiping out the light of the tube… by passing the hand quickly along the tube" |
| 196–197 | "We are whirling through endless space… everywhere is energy" |
| 200 | "the tube in my hand is brilliantly lighted" |
| 232 | "they enable us to perform many experiments by the use of one wire only" |
| 236 | "attach their machinery to the very wheelwork of nature" + "the most inefficient machine ever invented!" |
| 236 | "a heavy current, capable of fusing a thick copper wire" |
| 255 | carborundum filaments; "buttons of diamond dust" |
| 258 | "is it the less a flame because it does not scorch my hand?" |
| 267 | "economical reasons will make it advisable to use only one wire" |
| 288 | "I take a tube in my hand and move it about… still it retains the faculty of being excited" |
| 293 | "I shall never forget" (closing of the London lecture) |
| 374 | arcs "the advantages of silence and persistency" at high frequency |
| 376 | "Up to about 15,000 alternations per second in an experimental machine" |
| 381 | "480 polar projections on each side… 30,000 alternations per second" |
| 391 | "two bare wires about twenty feet long and two millimetres in diameter" |
| 394 | "a 'patent medicine' man… the misuse and abuse of electricity" |
| 395 | "a person entirely nude at the North Pole might keep himself comfortably warm" |
| 424 | spirit lamp under sheet iron, "oscillating as rapidly as 400 to 500 times a minute" |
| 486 | "a steel arbor which had been actually torn apart while vibrating against a minute air cushion" |
| 487 | "a weight of approximately 20 pounds at the rate of about 80 per second" |

## Appendix B — chapter → scan page → figure map

| Ch | Printed pp. | Scan files | Figures |
|---|---|---|---|
| I–II | 1–8 | 19–26 | 0 |
| III | 9–25 | 27–43 | 13 |
| IV–VI | 26–44 | 44–62 | 7 |
| VII–XIV | 45–78 | 63–96 | 20 |
| XV–XXIV | 79–118 | 97–136 | 21 |
| XXV | 119–144 | 137–162 | 0 |
| XXVI (NY lecture 1891) | 145–197 | 163–215 | 26 |
| XXVII (London lecture 1892) | 198–293 | 216–311 | 24 |
| XXVIII (Philly/St Louis 1893) | 294–373 | 312–391 | 21 |
| XXIX–XXXII | 374–408 | 392–426 | 14 |
| XXXIII–XLI | 409–476 | 427–494 | 28 |
| XLII–XLIII | 477–495 | 495–513 | 1 |

## Appendix C — figure candidate shortlists (top by area, one per page)

| Article | Candidates (file, printed page, px, book Fig.) |
|---|---|
| 01 Lamps | p172-fig99 p.154 834×739 · p171-fig97 p.153 752×758 · p197-fig117 p.179 860×660 · p212-fig12 p.194 592×816 · p206-fig125 p.188 790×609 · p200-fig121 p.182 613×765 |
| 02 One-wire | p281-fig153 p.263 1042×792 · p288-fig147 p.270 1029×648 · p265-fig151 p.247 948×652 · p246-fig144 p.228 942×629 · p263-fig149 p.245 976×587 |
| 03 Oscillator | p509-fig313 p.491 796×666 (only one) + patent US 514,169 + page scan p.486 |
| 04 Wireless | p172-fig99 p.154 · p197-fig117 p.179 · p206-fig125 p.188 · p200-fig121 p.182 |
| 05 Massage | p410-fig208 p.392 680×665 · p411-fig208 p.393 645×639 + page scan p.394 + electrode patent |
| 06 Cold flame | p265-fig151 p.247 · p246-fig144 p.228 · p263-fig149 p.245 · p197-fig117 p.179 · p225-fig13 p.207 789×717 |
| 07 Rotating field | p046-fig23 p.28 857×996 · p045-fig24 p.27 914×863 · p037-fig13 p.19 · p034-fig9 p.16 908×384 · p031-fig6 p.13 |
| 08 Weird inventions | p440-fig230 p.422 1001×663 · p452-fig247 p.434 971×616 · p478-fig283 p.460 · p484-fig290 p.466 · p464-fig266 p.446 · p475-fig281 p.457 |
| 09 World's Fair | p496 plate p.478 960×1707 · p502-fig p.484 812×642 (OCR caption mis-read "811") · p498-fig298 p.480 · p499-fig297 p.481 |
| 11 HF alternator | p397-fig207 p.379 720×684 · p394-fig200 p.376 840×576 · p396-fig205 p.378 831×570 · p393-fig203 p.375 806×514 |
| 12 Vacuum tubes | p418-fig215 p.400 1034×505 · p421-fig218 p.403 775×652 · p416-fig212 p.398 · p415-fig210 p.397 · p420-fig216 p.402 |

## Appendix D — verified fact boxes

**Word search of the 1894 volume** (`books/extracted/tesla-1894-plain.txt`,
re-run before publish): `free energy` 0 · `free-energy` 0 · `perpetual` 0 ·
`over unity` / `over-unity` 0 · `magnetic generator` 5, all **pyro**magnetic
(pp. 6, 424, 429, 496).

**Earthquake machine claim table** (article 03)

| Claim | Status | Source |
|---|---|---|
| Steam/air-driven reciprocating generator patented | true | US 514,169, "Reciprocating Engine", Feb 6 1894 |
| Demonstrated at the 1893 Chicago World's Fair | true, first-hand | Martin 1894, Ch. XLIII, p. 486 (lecture of Aug 25 1893, introduced by Elisha Gray) |
| A small version shook his Houston Street lab / caused an earthquake | Tesla's own story, told 1935 at age 79; no 1898 record | first printed in O'Neill, *Prodigal Genius* (1944), pp. 162–164 |
| It could produce a real earthquake | tested, busted | *MythBusters* ep. 60 (2006): vibrations felt hundreds of feet away, no earthquake on the bridge tested |

**Efficiency record** (article 07, p. 8): 1888 Anthony tests, ~50% and just over
60% · 1889 Pittsburgh tests (Tesla & Albert Schmid), up to 10 HP at ~850 lb,
nearly 90% · larger three-wire machines, 94–95%.

**High-frequency machine record** (article 11): 15,000 alternations/s experimental
(p. 376) · 480 polar projections per side, 30,000 alternations/s (p. 381) ·
20,000 alternations/s used for a 20 ft two-wire line experiment (p. 391).
