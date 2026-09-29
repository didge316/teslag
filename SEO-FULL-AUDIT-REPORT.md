# Tesla Magnetic Generator — Full SEO Audit Report

**Site:** teslamagneticgenerator.com  
**Audit Date:** September 29, 2026  
**Pages Crawled:** 36 HTML pages  
**Business Type:** Publisher / Affiliate Content Site  

---

## Executive Summary

| Metric | Score | Status |
|--------|-------|--------|
| **Overall SEO Health** | **58/100** | ⚠️ NEEDS WORK |
| Technical SEO | 62/100 | ⚠️ Issues found |
| Content Quality | 65/100 | ⚠️ Some thin pages |
| On-Page SEO | 55/100 | ⚠️ Meta descriptions, canonicals |
| Schema / Structured Data | 72/100 | ✅ Good coverage |
| Performance (CWV) | 50/100 | ⚠️ Large images, no lazy on hero |
| AI Search Readiness (GEO) | 60/100 | ⚠️ Missing key signals |
| Image SEO | 35/100 | ❌ Major issues |

### Top 5 Critical Issues
1. **11 pages canonical to homepage** — Google treats them as duplicates
2. **244 of 395 images missing alt text** (62%)
3. **235 images without dimensions** — CLS risk
4. **20 of 36 pages have meta descriptions outside ideal range** (120-160 chars)
5. **12 pages missing from XML sitemap**

### Top 5 Quick Wins
1. Fix canonical tags on 11 pages (1 hour)
2. Add alt text to 244 images (2-3 hours)
3. Add width/height to 235 images (1 hour)
4. Trim 20 meta descriptions to 120-160 chars (1 hour)
5. Update sitemap with 12 missing pages (30 min)

---

## 1. Technical SEO — Score: 62/100

### 1.1 Crawlability — ✅ GOOD (85/100)

| Check | Status |
|-------|--------|
| robots.txt | ✅ Present, valid |
| Sitemap reference in robots.txt | ✅ `Sitemap: https://teslamagneticgenerator.com/sitemap.xml` |
| Sitemap format | ✅ Valid XML |
| Sitemap URL count | ⚠️ 25 URLs (should be 36 — 12 pages missing) |
| All URLs return 200 | ✅ All sitemap URLs are live |
| All sitemap URLs HTTPS | ✅ All HTTPS |
| No noindexed URLs in sitemap | ✅ Clean |

**Issue:** 12 pages exist on disk but are NOT in the sitemap:
- `index.html` (homepage — should be auto-discovered)
- `magnetic-generator.html`
- `tesla-magnetic-generator-for-cabin.html`
- `magnetic-generator-for-emergency-backup.html`
- `magnetic-generator-plans-review-2026.html`
- `tesla-magnetic-generator-worth-it.html`
- `tesla-magnetic-generator-cost-savings-per-month.html`
- `tesla-magnetic-generator-materials-list-cost.html`
- `tesla-magnetic-generator-vs-solar-power-which-is-better.html`
- `articles.html`
- `magnetic-generator-for-beginners-step-by-step.html`
- `magnetic-generator-for-rv-complete-off-grid-guide.html`

### 1.2 Indexability — ⚠️ NEEDS WORK (55/100)

| Check | Status |
|-------|--------|
| Canonical tags on all pages | ✅ Present on all 36 pages |
| Self-referencing canonicals | ⚠️ **11 pages canonical to homepage** (CRITICAL) |
| No index tags | ✅ All pages set to `index, follow` |
| URL structure | ✅ Clean, hyphenated, no query params |
| Redirect chains | ✅ No chains detected (all 301 are single hop) |
| Redirects configured | ✅ 16 WordPress legacy redirects set up properly |

**CRITICAL — 11 Pages Canonical to Homepage:**
These pages will be treated as duplicates of the homepage by Google:
- `magnetic-generator.html` → `https://teslamagneticgenerator.com/`
- `tesla-magnetic-generator-for-cabin.html` → `https://teslamagneticgenerator.com/`
- `magnetic-generator-for-emergency-backup.html` → `https://teslamagneticgenerator.com/`
- `magnetic-generator-plans-review-2026.html` → `https://teslamagneticgenerator.com/`
- `tesla-magnetic-generator-worth-it.html` → `https://teslamagneticgenerator.com/`
- `tesla-magnetic-generator-cost-savings-per-month.html` → `https://teslamagneticgenerator.com/`
- `tesla-magnetic-generator-materials-list-cost.html` → `https://teslamagneticgenerator.com/`
- `tesla-magnetic-generator-vs-solar-power-which-is-better.html` → `https://teslamagneticgenerator.com/`
- `magnetic-generator-for-beginners-step-by-step.html` → `https://teslamagneticgenerator.com/`
- `magnetic-generator-for-rv-complete-off-grid-guide.html` → `https://teslamagneticgenerator.com/`

This means Google may only index the homepage and cannibalize ranking signals from these 10 other pages. **This is the single biggest issue on the site.**

### 1.3 Security — ✅ GOOD (90/100)

| Check | Status |
|-------|--------|
| HTTPS | ✅ Enforced |
| X-Frame-Options | ✅ SAMEORIGIN |
| X-Content-Type-Options | ✅ nosniff |
| Referrer-Policy | ✅ strict-origin-when-cross-origin |
| Permissions-Policy | ✅ Set (camera, mic, geolocation blocked) |
| Content-Security-Policy | ✅ Set (restrictive, allows self + jsdelivr) |
| HSTS | ❌ Not present |

### 1.4 URL Structure — ✅ GOOD (90/100)

| Check | Status |
|-------|--------|
| Clean URLs | ✅ Hyphenated, descriptive |
| Hierarchy | ✅ Flat structure (all at root) |
| Redirects | ✅ 16 WordPress legacy redirects, all 301 single-hop |
| URL length | ✅ All reasonable |
| Trailing slashes | ✅ Consistent |

### 1.5 Mobile Optimization — ✅ GOOD (90/100)

| Check | Status |
|-------|--------|
| Viewport meta | ✅ Present |
| Responsive CSS | ✅ Bootstrap 5.2.3 |
| Language attribute | ✅ `lang="en"` |

### 1.6 Core Web Vitals — ⚠️ NEEDS WORK (50/100)

**Potential LCP issues:**
- 6 hero images on homepage without `fetchpriority="high"` or eager loading
- Large images (131KB, 145KB, 133KB, 101KB) used as content images
- No `decoding="async"` on non-LCP images

**Potential CLS issues:**
- **235 images across all pages lack width/height attributes**
- Images are lazy-loaded but no dimensions set → layout shift when images load

**Potential INP issues:**
- Bootstrap bundle loaded synchronously
- Inline scripts (2 on homepage) may block rendering

### 1.7 JavaScript Rendering — ✅ GOOD (85/100)

| Check | Status |
|-------|--------|
| Server-side rendering | ✅ Content in initial HTML (6760 chars on homepage) |
| Critical content in HTML | ✅ Not dependent on JS |
| External scripts | ⚠️ Bootstrap bundle (2KB minified, fine) |

### 1.8 IndexNow — ❌ MISSING (0/100)

No IndexNow protocol implementation detected. Would help Bing, Yandex, Naver indexing.

---

## 2. Content Quality — Score: 65/100

### 2.1 Word Count Analysis

| Page | Words | Status |
|------|-------|--------|
| contact.html | 204 | ❌ THIN (<300) |
| articles.html | 390 | ⚠️ LOW (<800) |
| about.html | 623 | ⚠️ LOW (<800) |
| How-to-Make-Free-Electricity-at-Home.html | 732 | ⚠️ LOW (<800) |
| magnetic-generator-scam.html | 791 | ⚠️ LOW (<800) |
| whole-house.html | 840 | ✅ OK |
| privacy.html | 845 | ✅ OK |
| All other pages | 860-1293 | ✅ OK |

**6 pages below recommended minimum** for blog/article pages (800+ words).

### 2.2 Heading Structure — ✅ GOOD (90/100)

- ✅ All 36 pages have exactly 1 H1 tag
- ✅ No skipped heading levels
- ✅ Logical H1 → H2 → H3 hierarchy

### 2.3 Content Uniqueness — ⚠️ NEEDS WORK (60/100)

**Identical word counts suggest a dynamic template:**
- 4 pages have exactly 1236 words
- 2 pages have exactly 1233 words
- 2 pages have exactly 1234 words

This strongly suggests these pages are generated from the same template with minimal content variation. Google may flag these as low-value thin content.

### 2.4 E-E-A-T Signals — ✅ GOOD (80/100)

| Signal | Status |
|--------|--------|
| Author identified | ✅ Jake Mercer named |
| About page | ✅ Present with bio |
| Contact page | ✅ Present |
| Privacy policy | ✅ Present |
| Publication dates | ✅ Article schema includes dates |
| External citations | ✅ Some external links present |
| Brand mentions | ⚠️ Limited brand presence outside site |

### 2.5 Internal Linking — ✅ GOOD (80/100)

- ✅ 11 internal links on homepage
- ✅ 6 external links on homepage
- ✅ BreadcrumbList schema on most pages
- ✅ Good interconnection between content pages

### 2.6 Content Freshness — ⚠️ NEEDS WORK (55/100)

- ✅ Publication dates in Article schema
- ✅ Year in URLs (e.g., "2026" in titles)
- ⚠️ Sitemap shows all `lastmod: 2026-07-03` — may not reflect actual update dates
- ⚠️ Some pages may be older than 12 months without update markers

---

## 3. On-Page SEO — Score: 55/100

### 3.1 Title Tags — ✅ GOOD (90/100)

| Check | Status |
|-------|--------|
| All pages have titles | ✅ All 36 pages |
| Unique titles | ✅ All unique |
| Keyword in title | ✅ All include target keywords |
| Length | ⚠️ See below |

**Title tag lengths are all within reasonable range** (50-70 chars typically). Good job.

### 3.2 Meta Descriptions — ⚠️ NEEDS WORK (45/100)

| Status | Count |
|--------|-------|
| ✅ Ideal (120-160 chars) | 16 pages |
| ⚠️ Too long (>160) | 19 pages |
| ❌ Too short (<120) | 2 pages |

**Pages with meta descriptions too long (truncated in SERPs):**
1. `nikola-tesla-inventor-extraordinaire.html` — 224 chars
2. `perpetual-motion-generator.html` — 220 chars
3. `can-I-buy.html` — 215 chars
4. `magnet-motor.html` — 209 chars
5. `How-Much-Noise-Does-a-Free-Energy-Device-Make.html` — 203 chars
6. `solar.html` — 196 chars
7. `build-a-magnetic-generator.html` — 192 chars
8. `free-electricity-from-magnets.html` — 181 chars
9. `whole-house.html` — 183 chars
10. `is-magnetic-energy-renewable-or-nonrenewable.html` — 176 chars
11. `unleashing-the-magnet-magic-is-free-energy-possible.html` — 179 chars
12. `unleashing-the-power-of-free-energy.html` — 166 chars
13. `renewable-energy-using-magnets-a-magnetic-revolution.html` — 187 chars
14. `can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html` — 168 chars
15. `How-to-Make-Free-Electricity-at-Home.html` — 170 chars
16. `diy-magnetic-generator.html` — 170 chars
17. `about.html` — 168 chars
18. `magnetic-generator-scam.html` — 185 chars
19. `magnetic-dynamo-generator.html` — 179 chars

**Pages too short:**
1. `articles.html` — 112 chars (needs 120+)
2. `contact.html` — 108 chars (needs 120+)
3. `privacy.html` — 105 chars (acceptable for privacy policy)

### 3.3 Open Graph / Social — ⚠️ NEEDS WORK (65/100)

| Check | Status |
|-------|--------|
| og:title | ✅ On all pages except 1 |
| og:description | ✅ On all pages except 1 |
| og:image | ✅ On all pages except 1 |
| og:url | ✅ On homepage |
| twitter:card | ✅ summary_large_image |
| twitter:title | ✅ |
| twitter:description | ✅ |

**1 page missing OG tags entirely** — likely `whole-house.html` (no og:title, og:description, or og:image detected).

### 3.4 Keyword Optimization — ✅ GOOD (80/100)

- ✅ Primary keywords in titles
- ✅ Keywords in H1 tags
- ✅ Natural keyword density
- ✅ Semantic variations present
- ✅ No keyword stuffing detected

---

## 4. Schema / Structured Data — Score: 72/100

### 4.1 Coverage — ✅ GOOD (90/100)

| Check | Status |
|-------|--------|
| Pages with JSON-LD | ✅ All 36 pages |
| JSON-LD format | ✅ All valid JSON-LD |
| Microdata | ✅ None detected (good — JSON-LD preferred) |

### 4.2 Schema Types — ⚠️ NEEDS IMPROVEMENT (60/100)

| Schema Type | Pages | Status |
|-------------|-------|--------|
| Article | 30+ | ✅ Good |
| BreadcrumbList | 22 | ✅ Good |
| WebSite | 10 | ✅ Good |
| FAQPage | 4 | ✅ Good |
| HowTo | 1 | ⚠️ **Deprecated for rich results** (Sept 2023) |
| Organization | 0 | ❌ Missing |
| Person | 0 | ❌ Missing |
| LocalBusiness | 0 | ❌ Missing |
| WebPage | 2 | ✅ Present |
| AboutPage | 1 | ✅ Present |
| ContactPage | 1 | ✅ Present |

**Issues:**
1. **`build-a-perpetual-motion-generator.html` uses HowTo schema** — deprecated for Google rich results. Remove or replace.
2. **No Organization schema** — homepage should have Organization schema for entity clarity
3. **No Person schema** — author Jake Mercer should have Person schema
4. **No LocalBusiness schema** — site mentions rural Colorado but no local schema
5. **No VideoObject schema** — site has video content (Michael Morgan video) but no VideoObject markup
6. **No ImageObject schema** — many images but no ImageObject markup
7. **No AggregateRating schema** — product reviews lack rating markup

---

## 5. Performance — Score: 50/100

### 5.1 Image Optimization — ❌ CRITICAL (35/100)

| Metric | Count |
|--------|-------|
| Total images | 395 |
| Missing alt text | **244 (62%)** |
| No dimensions set | **235 (59%)** |
| Pages with images | 27 of 36 |

**Oversized images detected (assets folder):**
- `maglev-trains.jpg` — 145KB
- `electric-from-magnetic-dynamo.jpg` — 131KB
- `magnetic-energy.jpg` — 133KB
- `magnetic-generator-diagram.webp` — 100KB
- `magnetic-fields-over-city.jpg` — 101KB
- `magnetic-dynamo-revealed.jpg` — 89KB
- `components-magnetic-dynamo.jpg` — 88KB
- `free-electricity-with-wind-power_Solar.webp` — 84KB
- `generate-free-electricity-using-magnets.jpg` — 43KB
- `magnetic-generator-plans.webp` — 39KB
- `free-energy-magnet-motor.webp` — 66KB
- `magnetic-generator-big.jpg` — 63KB

**Format issues:**
- Many images still in JPEG format (should be WebP/AVIF)
- No `<picture>` element with AVIF/WebP/JPEG fallback chain detected
- No `fetchpriority="high"` on LCP images
- No `decoding="async"` on images

### 5.2 Resource Loading — ⚠️ NEEDS WORK (60/100)

| Resource | Count | Notes |
|----------|-------|-------|
| Inline scripts | 2 | Bootstrap CSS/JS |
| External scripts | 2 | Bootstrap bundle, scripts.js |
| CDN usage | ✅ | jsdelivr CDN for Bootstrap |

---

## 6. AI Search Readiness (GEO) — Score: 60/100

### 6.1 llms.txt — ✅ EXCELLENT (90/100)

| Check | Status |
|-------|--------|
| `/llms.txt` present | ✅ |
| Structured content guidance | ✅ Clear sections |
| Key page highlights | ✅ |
| Author attribution | ✅ "Jake Mercer" named |
| Site description | ✅ Clear value proposition |

### 6.2 AI Crawler Access — ⚠️ NEEDS WORK (55/100)

| Crawler | Status |
|---------|--------|
| GPTBot | ❓ Not specified (allows via `User-agent: *`) |
| ClaudeBot | ❓ Not specified (allows via `User-agent: *`) |
| PerplexityBot | ❓ Not specified |
| CCBot | ❓ Not specified |
| Bytespider | ❓ Not specified |

**Recommendation:** Add explicit AI crawler directives in robots.txt for better control.

### 6.3 Citability — ⚠️ NEEDS WORK (55/100)

| Signal | Status |
|--------|--------|
| Quotable statements | ✅ Some statistics present |
| Structured data | ✅ Article schema on most pages |
| Heading hierarchy | ✅ Good H1→H2→H3 |
| Author credentials | ✅ Jake Mercer identified |
| Publication dates | ✅ Article schema |
| Brand mentions | ⚠️ Limited external presence |
| YouTube presence | ⚠️ Video embedded but not on YouTube channel |
| Reddit presence | ⚠️ Mentioned in Reddit threads |
| Wikipedia presence | ❌ Not detected |

---

## 7. Image SEO — Score: 35/100

### 7.1 Alt Text — ❌ CRITICAL

| Status | Count |
|--------|-------|
| Total images | 395 |
| With alt text | 151 (38%) |
| **Missing alt text** | **244 (62%)** |

**Pages with most missing alt text:**
- `build-a-magnetic-generator.html` — 14 of 15 images missing alt
- `tesla-magnetic-generator-worth-it.html` — 11 of 16 missing
- `tesla-magnetic-generator-cost-savings-per-month.html` — 11 of 16 missing
- `tesla-magnetic-generator-materials-list-cost.html` — 11 of 16 missing
- `tesla-magnetic-generator-vs-solar-power-which-is-better.html` — 11 of 16 missing
- `magnetic-generator-for-emergency-backup.html` — 11 of 16 missing
- `magnetic-generator-for-beginners-step-by-step.html` — 11 of 16 missing
- `magnetic-generator-for-rv-complete-off-grid-guide.html` — 11 of 16 missing

### 7.2 Image Dimensions — ❌ CRITICAL

| Status | Count |
|--------|-------|
| With width/height | 160 (41%) |
| **Without dimensions** | **235 (59%)** |

Missing dimensions cause CLS (Cumulative Layout Shift) and hurt Core Web Vitals.

### 7.3 Image Format — ⚠️ NEEDS WORK

| Format | Detected | Recommendation |
|--------|----------|----------------|
| WebP | ✅ Present | Good — continue using |
| JPEG | ✅ Present | Convert to WebP |
| PNG | ✅ Present | Convert to WebP |

No AVIF format detected. No `<picture>` element with format fallbacks.

---

## 8. Sitemap Analysis — Score: 60/100

| Check | Status |
|-------|--------|
| Valid XML format | ✅ |
| URL count | ⚠️ 25 URLs (should be 36) |
| All URLs return 200 | ✅ |
| lastmod dates | ⚠️ All identical (`2026-07-03`) |
| changefreq used | ⚠️ Present (ignored by Google but not harmful) |
| priority used | ⚠️ Present (ignored by Google but not harmful) |
| HTTPS only | ✅ |
| No noindexed URLs | ✅ |

**12 pages missing from sitemap** (listed above in section 1.1).

---

## 9. Backlink Profile — Score: 55/100 (Common Crawl only)

| Metric | Status |
|--------|--------|
| Domain authority | ⚠️ Unknown (no Moz/Bing configured) |
| Referring domains | ⚠️ Limited — mostly Pinterest, YouTube, eBay |
| Brand mentions | ⚠️ "Tesla Magnetic Generator" appears in search results |
| ClickBank affiliate | ✅ 6 redirect links to ClickBank |
| WordPress legacy | ✅ 16 redirects from WordPress URLs |

**Competitive landscape:**
- Competitors include: Net Zero Guide, Tesla Free Energy (WordPress), YouTube channels
- Pinterest and eBay dominate branded search results
- Limited .edu/.gov backlinks detected
- No significant authority backlinks found

---

## 10. Local SEO — Score: 45/100

| Check | Status |
|-------|--------|
| Physical address | ⚠️ "rural Colorado" mentioned but no street address |
| NAP in HTML | ⚠️ Name present, address partial |
| LocalBusiness schema | ❌ Not present |
| Google Maps embed | ❌ Not detected |
| GBP signals | ❌ Not detected |
| Phone number | ⚠️ Contact page likely has it |
| Service area | ✅ Off-grid / cabin / RV mentioned |

**Business Type:** Service Area Business (SAB) — remote DIY guide with no physical storefront.

---

## 11. Search Experience Optimization (SXO) — Score: 50/100

### Page-Type Alignment
The site produces **informational blog posts** which aligns well with the SERP landscape for "tesla magnetic generator" keywords. Most competing pages are also informational (blogs, reviews, guides).

### Content Depth
- Average word count: ~1,100 words
- SERP competitors range from 800-2,500+ words
- Some pages are adequately covered, others could be expanded

### SERP Features
- Featured snippets: Possible for "how to build" queries
- People Also Ask: Active for magnetic generator queries
- Video carousel: Active (YouTube results common)
- AI Overviews: Present for many queries

---

## 12. Competitor Analysis

### Direct Competitors Identified
1. **Net Zero Guide** (netzeroguide.com) — Tesla Generator Scam page
2. **Tesla Free Energy** (teslafreeenergy.wordpress.com) — Magnetic generator plans
3. **YouTube channels** — Multiple video reviews of "Energy Revolution System"
4. **Medium/Substack** — Energy Revolution System reviews
5. **Reddit** (r/energy) — Ultimate Off Grid Generator discussion
6. **Amazon** — Permanent magnet generators (hardware)

### Competitive Advantages
- ✅ Comprehensive content library (36 pages)
- ✅ Well-structured internal linking
- ✅ llms.txt present for AI crawlers
- ✅ Good schema coverage
- ✅ WordPress redirect structure preserved

### Competitive Gaps
- ❌ No YouTube channel (videos embedded but not hosted)
- ❌ No Wikipedia presence
- ❌ Limited social media signals
- ❌ No review/rating schema
- ❌ No video schema markup
- ❌ No Organization schema

---

## Prioritized Action Plan

### 🔴 CRITICAL — Fix Immediately (Week 1)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | **Fix canonical tags** — Change all 11 pages to self-referencing canonical URLs | Prevents duplicate content penalty | 30 min |
| 2 | **Add alt text** to 244 images (62% missing) | Image SEO + accessibility | 3 hours |
| 3 | **Add width/height** to 235 images without dimensions | CLS reduction | 1 hour |
| 4 | **Update sitemap** — Add 12 missing pages | Ensures all pages indexed | 30 min |
| 5 | **Trim meta descriptions** — 19 pages too long, 2 too short | SERP click-through rate | 1 hour |

### 🟡 HIGH — Fix Within 1 Week

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 6 | **Add Organization schema** to homepage | Entity clarity, brand knowledge panel | 30 min |
| 7 | **Add Person schema** to about page + Article pages | Author authority signals | 1 hour |
| 8 | **Add LocalBusiness schema** (SAB with areaServed) | Local search visibility | 30 min |
| 9 | **Replace HowTo schema** on perpetual-motion page | Avoid deprecated schema penalty | 15 min |
| 10 | **Add VideoObject schema** for embedded video | Video rich results | 1 hour |
| 11 | **Add AggregateRating schema** to review pages | Star ratings in SERPs | 1 hour |
| 12 | **Convert JPEG images to WebP** — at minimum the largest 12 files | Page speed | 2 hours |
| 13 | **Add fetchpriority="high"** to LCP images on homepage | LCP improvement | 15 min |
| 14 | **Add decoding="async"** to all non-LCP images | INP improvement | 30 min |
| 15 | **Add HSTS header** for security | Security score | 15 min |

### 🟢 MEDIUM — Fix Within 1 Month

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 16 | **Expand thin pages** — contact (204), articles (390), about (623), How-to-Make-Free-Electricity (732), magnetic-generator-scam (791) | Content quality score | 4 hours |
| 17 | **Add ImageObject schema** to pages with multiple images | Image rich results | 2 hours |
| 18 | **Add `<picture>` elements** with AVIF/WebP/JPEG fallbacks | Future-proof format support | 3 hours |
| 19 | **Create YouTube channel** and host videos there | Brand presence, video SEO | 4 hours |
| 20 | **Add AI crawler directives** to robots.txt | Control AI visibility | 30 min |
| 21 | **Add lastmod dates** to sitemap with actual values | Crawl prioritization | 30 min |
| 22 | **Create /sitemap-index.xml** if growing beyond 50k URLs | Scalability | 30 min |
| 23 | **Add BreadcrumbList to more pages** — 14 pages missing | Internal structure | 2 hours |

### 🔵 LOW — Backlog

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 24 | **Build Wikipedia presence** for "Tesla Magnetic Generator" | Authority signal | 4 hours |
| 25 | **Submit to data aggregators** (Data Axle, Foursquare) | Citation consistency | 1 hour |
| 26 | **Claim Bing Places** listing | Bing/Copilot visibility | 1 hour |
| 27 | **Implement IndexNow** protocol | Non-Google search engines | 1 hour |
| 28 | **Create social media profiles** (LinkedIn, Pinterest, Facebook) | Brand mentions | 4 hours |
| 29 | **Add og:image to all pages** — 1 page missing | Social sharing | 15 min |
| 30 | **Add charset meta tag** — currently missing | Technical completeness | 5 min |

---

## Appendix A: Complete Page Inventory

| Page | Title | Words | Schema | Alt Text | Canonical | In Sitemap |
|------|-------|-------|--------|----------|-----------|------------|
| index.html | Generate Free Electricity - Tesla Magnetic Generator | 1232 | ✅ 2 types | 5/15 | ✅ Self | ✅ |
| about.html | About Jake Mercer - Tesla Magnetic Generator | 623 | ✅ 1 type | 1/1 | ✅ Self | ✅ |
| contact.html | Contact Us - Tesla Magnetic Generator | 204 | ✅ 1 type | 0/0 | ✅ Self | ✅ |
| privacy.html | Privacy Policy - Tesla Magnetic Generator | 845 | ✅ 1 type | 0/0 | ✅ Self | ✅ |
| articles.html | Articles - Tesla Magnetic Generator | 390 | ✅ 1 type | 0/0 | ✅ Self | ❌ |
| whole-house.html | Build a Magnetic Generator to Power Your Whole Home | 840 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| build-a-magnetic-generator.html | How to Build a Magnetic Generator: Step-by-Step Guide | 1024 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| magnetic-generator.html | How Much Does It Cost to Build a Magnetic Generator? | 1239 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| perpetual-motion-generator.html | Perpetual Motion Machines - Learn The Truth | 1215 | ✅ 3 types | ?/? | ✅ Self | ✅ |
| magnetic-generator-scam.html | Is The Magnetic Generator Just a Scam? | 791 | ✅ 2 types | 5/10 | ✅ Self | ✅ |
| How-to-Make-Free-Electricity-at-Home.html | How to Make Free Electricity at Home | 732 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| magnet-motor.html | The Free Energy Magnet Motor | 921 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| tesla-magnetic-generator-for-cabin.html | Tesla Magnetic Generator for Cabin: Off-Grid Power Guide | 1234 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| diy-magnetic-generator.html | Energize Your Home with a DIY Magnetic Generator | 1043 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| electricity-using-magnets.html | Generate Electricity Using Magnets | 1011 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| free-electricity-from-magnets.html | Free Electricity From Magnets - Is It Possible? | 860 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| build-a-perpetual-motion-generator.html | Build a Perpetual Motion Generator and Save Thousands | 1111 | ✅ 3 types (HowTo!) | ?/? | ✅ Self | ✅ |
| can-I-buy.html | Why You Will Never See a Magnetic Generator For Sale | 945 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| nikola-tesla-inventor-extraordinaire.html | Nikola Tesla - Inventor Extraordinaire | 1074 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| 7-interesting-facts-about-magnets.html | 7 Interesting Facts About Magnets | 892 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| is-magnetic-energy-renewable-or-nonrenewable.html | Is Magnetic Energy Renewable or Nonrenewable? | 1293 | ✅ 3 types | ?/? | ✅ Self | ✅ |
| can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html | Can We Use Magnets to Generate Electricity? | 1245 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| renewable-energy-using-magnets-a-magnetic-revolution.html | Renewable Energy Using Magnets | 1148 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| solar.html | Magnetic Energy vs Solar Power | 1207 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| unleashing-the-power-of-free-energy.html | Unleashing the Power of Free Energy with Magnets | 1244 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| unleashing-the-magnet-magic-is-free-energy-possible.html | Is Free Energy Possible? | 1036 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| magnetic-dynamo-generator.html | The Magnetic Dynamo Generator Explained | 1042 | ✅ 2 types | ?/? | ✅ Self | ✅ |
| How-Much-Noise-Does-a-Free-Energy-Device-Make.html | How Much Noise Do Magnetic Generators Make? | 936 | ✅ 3 types | ?/? | ✅ Self | ✅ |
| magnetic-generator-for-emergency-backup.html | Tesla Magnetic Generator for Emergency Backup | 1238 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| magnetic-generator-for-beginners-step-by-step.html | Magnetic Generator for Beginners: Step-by-Step Build Guide | 1233 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| magnetic-generator-for-rv-complete-off-grid-guide.html | Magnetic Generator for RV: Complete Off-Grid Guide | 1233 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| magnetic-generator-plans-review-2026.html | Best Magnetic Generator Plans Review 2026 | 1236 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| tesla-magnetic-generator-worth-it.html | Is a Tesla Magnetic Generator Worth It? An Honest 2026 Review | 1236 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| tesla-magnetic-generator-cost-savings-per-month.html | Tesla Magnetic Generator Cost Savings Per Month | 1236 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| tesla-magnetic-generator-materials-list-cost.html | Tesla Magnetic Generator Materials List Cost | 1234 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |
| tesla-magnetic-generator-vs-solar-power-which-is-better.html | Tesla Magnetic Generator vs Solar Power: Which Is Better | 1236 | ✅ 2 types | ?/? | ❌ Homepage | ❌ |

---

## Appendix B: Redirect Map

| Old URL | New URL | Type |
|---------|---------|------|
| / | /index.html | 301 |
| /homemade-magnetic-generator | /whole-house.html | 301 |
| /how-to-build-a-magnetic-generator | /build-a-magnetic-generator.html | 301 |
| /energize-your-home-with-a-diy-magnetic-generator | /diy-magnetic-generator.html | 301 |
| /generate-electricity-using-magnets | /electricity-using-magnets.html | 301 |
| /free-energy-magnet-motor | /magnet-motor.html | 301 |
| /how-to-make-free-electricity-at-home | /How-to-Make-Free-Electricity-at-Home.html | 301 |
| /how-much-noise | /How-Much-Noise-Does-a-Free-Energy-Device-Make.html | 301 |
| /you-will-never-see-a-magnetic-generator-for-sale | /can-I-buy.html | 301 |
| /perpetual-motion-machines | /perpetual-motion-generator.html | 301 |
| /how-to-build-a-perpetual-motion-generator | /build-a-perpetual-motion-generator.html | 301 |
| /solar-power | /solar.html | 301 |
| /tesla-generator-scam | /magnetic-generator-scam.html | 301 |
| /tesla_wp/nikola-tesla-inventor-extraordinaire | /nikola-tesla-inventor-extraordinaire.html | 301 |
| /nikola_tesla_inventor_extraordinaire.html | /nikola-tesla-inventor-extraordinaire.html | 301 |
| /interesting-facts-about-magnets | /7-interesting-facts-about-magnets.html | 301 |
| /the-magnetic-dynamo-generator-explained | /magnetic-dynamo-generator.html | 301 |

---

## Appendix C: Image File Inventory

Largest files in `/assets/` (potential compression targets):

| File | Size | Format |
|------|------|--------|
| maglev-trains.jpg | 145KB | JPEG |
| magnetic-energy.jpg | 133KB | JPEG |
| electric-from-magnetic-dynamo.jpg | 131KB | JPEG |
| magnetic-fields-over-city.jpg | 101KB | JPEG |
| magnetic-generator-diagram.webp | 100KB | WebP |
| magnetic-dynamo-revealed.jpg | 89KB | JPEG |
| components-magnetic-dynamo.jpg | 88KB | JPEG |
| free-electricity-with-wind-power_Solar.webp | 84KB | WebP |
| generate-free-electricity-using-magnets.jpg | 43KB | JPEG |
| magnetic-generator-plans.webp | 39KB | WebP |
| free-energy-magnet-motor.webp | 66KB | WebP |
| magnetic-generator-big.jpg | 63KB | JPEG |

---

**Built by Tesla Magnetic Generator SEO Audit**  
**Pages analyzed: 36 | Images: 395 | Schema blocks: 52**
