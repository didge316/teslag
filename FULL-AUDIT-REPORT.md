# Full SEO Audit — Tesla Magnetic Generator
**Site:** teslamagneticgenerator.com  
**Audit Date:** 2026-05-22  
**Files Audited:** 24 HTML pages + robots.txt + sitemap.xml + _redirects  
**Business Type:** Affiliate marketing (ClickBank) — DIY free energy / magnetic generator niche  
**Platform:** Static HTML on Cloudflare Pages (converted from WordPress)

---

## SEO Health Score: 46/100

| Category | Weight | Score | Weighted |
|----------|--------|-------|---------|
| Technical SEO | 22% | 58/100 | 12.8 |
| Content Quality | 23% | 42/100 | 9.7 |
| On-Page SEO | 20% | 63/100 | 12.6 |
| Schema / Structured Data | 10% | 0/100 | 0.0 |
| Performance (CWV) | 10% | 65/100 | 6.5 |
| AI Search Readiness | 10% | 25/100 | 2.5 |
| Images | 5% | 45/100 | 2.3 |
| **TOTAL** | **100%** | | **46.4/100** |

---

## Executive Summary

The site has solid technical foundations for a static HTML Cloudflare deployment — responsive Bootstrap layout, canonical tags, redirects from the old WordPress URLs, and lazy-loaded images. However it scores poorly on the categories that matter most in 2025/26: **zero structured data, severe E-E-A-T deficiencies, a broken contact form, OG images that 404, and sitemap URLs that don't match canonical page addresses.**

### Top 5 Critical Issues
1. **Zero schema markup** — no Article, WebSite, BreadcrumbList, or FAQPage schema on any page
2. **Contact form is broken** — `<form>` opening tag is commented out, only the `</form>` close tag exists; form is non-functional
3. **OG image 404s** — homepage og:image references `/assets/magnetic-energy-generator-blueprints.jpg` which does not exist in the assets folder
4. **Sitemap lists wrong canonical URLs** — sitemap.xml uses `.html` file URLs (e.g., `index.html`) rather than the canonical root URLs that were authoritative during the WordPress era
5. **E-E-A-T failure** — no named author, no dates, no About page; pseudoscientific claims and conspiracy framing create significant quality signal risk

### Top 5 Quick Wins
1. Add Article schema to all content pages (30 minutes with a template)
2. Fix the contact form (uncomment the `<form>` tag — 1-line fix)
3. Fix OG image references to use existing files
4. Add `lastmod` dates and fix the homepage URL in sitemap.xml
5. Add published/updated dates to all articles (visible on page)

---

## 1. Technical SEO

### 1.1 Crawlability & Indexation

| Item | Status | Detail |
|------|--------|--------|
| robots.txt | ✅ Pass | Allows all, points to sitemap correctly |
| Canonical tags | ✅ Pass | All pages have self-referencing canonicals |
| HTTPS | ✅ Pass | Cloudflare manages SSL |
| Mobile viewport | ✅ Pass | All pages have correct viewport meta |
| Internal links | ✅ Pass | Good cross-linking via nav dropdown and sidebar |
| sitemap.xml | ⚠️ Issues | See 1.2 below |
| URL consistency | ⚠️ Issues | See 1.3 below |
| Contact form | ❌ Broken | Opening `<form>` tag commented out on contact.html:78 |

### 1.2 Sitemap Issues

**Primary sitemap** (`/sitemap.xml` in website folder):
- ❌ Homepage listed as `https://teslamagneticgenerator.com/index.html` — should be `https://teslamagneticgenerator.com/`
- ❌ All URLs use `.html` file extensions, which do not match the WordPress-era canonical URLs that held link equity
- ❌ Missing `<lastmod>`, `<priority>`, and `<changefreq>` on all entries
- ❌ `contact.html` and `privacy.html` are included in sitemap (low-value pages can be excluded)

**Old sitemap** (`sitemap2.xml` in repo root — NOT served):
- ✅ Has proper `lastmod` dates and priority values
- ✅ Uses WordPress-style clean URLs
- ❌ Not in the website folder, so Cloudflare does not serve it
- ❌ Contains a `sitemap/` page URL that doesn't exist in the new site

**Recommendation:** Update `sitemap.xml` to use clean canonical URLs (matching the `_redirects` file), add lastmod dates, and remove contact/privacy.

### 1.3 URL / Filename Issues

| File | Issue |
|------|-------|
| `How-to-Make-Free-Electricity-at-Home.html` | Uppercase letters in filename — non-standard, case-sensitive on some servers |
| `How-Much-Noise-Does-a-Free-Energy-Device-Make.html` | Uppercase letters in filename |
| `nikola_tesla_inventor_extraordinaire.html` | Underscores instead of hyphens — Google recommends hyphens as word separators |
| `can-I-buy.html` | Capital `I` in filename |
| `7-interesting-facts-about-magnets.html` | Starts with a number — minor, but prefer kebab-case descriptive slug |

### 1.4 Redirect Structure

The `_redirects` file (Cloudflare Pages) correctly maps all old WordPress-style URLs to new `.html` files. However:

- ❌ The `sitemap.xml` still lists the `.html` file URLs, not the clean URLs that were previously canonical and hold backlink equity
- ❌ Any backlinks pointing to the old clean WP URLs will now pass through a 301 redirect before reaching the content, adding a redirect hop

### 1.5 Security

- ✅ HTTPS enforced via Cloudflare
- ❌ No security headers configured (Content-Security-Policy, X-Content-Type-Options, etc.) — these can be set in Cloudflare Pages `_headers` file
- ❌ `.htaccess` file present in website folder — has no effect on Cloudflare Pages; can be removed to avoid confusion

---

## 2. Content Quality (E-E-A-T)

This is the **most significant risk area** for the site. Google's quality rater guidelines treat "miracle health/energy claims" and "suppressed technology" narratives as low-quality content signals.

### 2.1 Experience, Expertise, Authority, Trust

| Signal | Status | Detail |
|--------|--------|--------|
| Named author | ❌ Missing | `meta name="author" content="tesla"` — not a real person |
| Author bio | ❌ Missing | No author information on any page |
| Author credentials | ❌ Missing | No demonstration of expertise |
| Published dates | ❌ Missing | No visible dates on any article |
| Updated dates | ❌ Missing | No last-modified dates shown |
| About page | ❌ Missing | No About/Who We Are page |
| Contact info | ⚠️ Broken form | Contact page exists but form is non-functional |
| Privacy policy | ✅ Present | Privacy page exists |
| External citations | ❌ Missing | No references, studies, or citations |

### 2.2 Content Quality Concerns

The content is first-person, engaging, and covers topics thoroughly. However several patterns create E-E-A-T risk:

- **Pseudoscientific claims**: "produces roughly 8-10x more electricity than it consumes" — violates thermodynamics; similar claims have resulted in manual Google actions against other sites in this niche
- **Conspiracy framing**: "powers that be", "information suppression", "website gets taken down regularly" — creates a distrust signal
- **Fake urgency**: "check back before the site gets taken down again" — a dark pattern that Google's quality raters flag
- **Static fake comments**: The comment sections appear interactive but are hardcoded HTML with no backend — this could be seen as deceptive UX
- **Comment form with no backend**: The comment textarea has no action — submitting it does nothing

### 2.3 Content Strengths

- ✅ Long-form content covering the topic from multiple angles
- ✅ Good internal linking — most pages link to related pages
- ✅ Readable writing style, natural language
- ✅ Covers both informational intent ("what is") and commercial intent ("how to build")
- ✅ Addresses common reader objections (scam page, noise page, can-I-buy page)

---

## 3. On-Page SEO

### 3.1 Title Tags

| Page | Title | Length | Issue |
|------|-------|--------|-------|
| index.html | Generate Your Own Free Electricity - Tesla Magnetic Generator | 61 | ✅ Good |
| whole-house.html | Can You Really Power Your Home? | 32 | ❌ Too short, missing "magnetic generator" keyword |
| build-a-magnetic-generator.html | Learning How to Build a Magnetic Generator is The Best Thing You Will Ever Do! | 78 | ⚠️ Too long, will be truncated in SERPs (55-60 char ideal) |
| magnetic-generator-scam.html | Is The Magnetic Generator Just a Scam? | 40 | ✅ Good |
| diy-magnetic-generator.html | Energize Your Home with a DIY Magnetic Generator for Home Use! | 62 | ✅ Good |

### 3.2 Meta Descriptions

Most are well-written (180-220 chars). All pages have unique descriptions.

- ❌ Homepage description has a trailing space after the final period
- ✅ Descriptions are descriptive and click-worthy

### 3.3 Heading Structure

- ✅ All pages have a single H1
- ❌ Homepage: H1 → H3 (skips H2 entirely inside the article body)
- ❌ `build-a-magnetic-generator.html`: Uses H2 mid-article but leads with H3s — inconsistent hierarchy
- ✅ Other pages generally have logical H1 → H2 → H3 progression

### 3.4 OG / Social Tags

- ✅ All pages have og:title, og:description, og:type, og:url, og:image
- ✅ Twitter Card tags present on all pages
- ❌ `whole-house.html` og:title is "Can You Really Power Your Home?" — different from H1 and misses keywords
- ❌ Homepage og:image: `/assets/magnetic-energy-generator-blueprints.jpg` — **file does not exist** (404)
- ❌ `magnetic-generator-scam.html` og:image: `/assets/perpetual-motion-generator.webp` — needs verification
- ❌ `build-a-magnetic-generator.html` og:image: `/assets/magnetic-generator-free-energy-generator.webp` — needs verification
- ❌ OG images use relative paths — should be absolute URLs for best compatibility

---

## 4. Schema / Structured Data

**Score: 0/100 — No schema markup exists anywhere on the site.**

This is the single highest-ROI fix available. Missing:

| Schema Type | Pages | Priority |
|-------------|-------|---------|
| `Article` | All 20 content pages | Critical |
| `WebSite` | Homepage | High |
| `BreadcrumbList` | All pages | High |
| `FAQPage` | perpetual-motion-generator.html, 7-interesting-facts, magnetic-generator-scam, etc. | High |
| `Organization` | Homepage | Medium |

### Article Schema Template (for each content page)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "PAGE TITLE HERE",
  "description": "META DESCRIPTION HERE",
  "author": {
    "@type": "Person",
    "name": "AUTHOR NAME"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Tesla Magnetic Generator",
    "url": "https://teslamagneticgenerator.com"
  },
  "datePublished": "2025-11-XX",
  "dateModified": "2026-XX-XX",
  "mainEntityOfPage": "PAGE CANONICAL URL"
}
```

### WebSite Schema Template (homepage)
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Tesla Magnetic Generator",
  "url": "https://teslamagneticgenerator.com"
}
```

---

## 5. Performance

### 5.1 Asset Loading

| Asset | Status | Detail |
|-------|--------|--------|
| Cloudflare CDN | ✅ | Good global edge performance |
| Bootstrap JS | ✅ | Loaded from CDN (jsdelivr), cached |
| styles.css | ⚠️ | Contains full Bootstrap bundle (~100KB) — consider splitting custom CSS out |
| Image lazy loading | ✅ | All images use `loading="lazy"` |
| WebP images | ✅ | Most assets in WebP format |
| Preconnect hints | ❌ | No `<link rel="preconnect">` for cdn.jsdelivr.net |
| js/scripts.js | ✅ | File exists at `/js/scripts.js` (previously unclear) |

### 5.2 Estimated CWV

Without live field data (no Google API credentials configured), lab estimates based on asset profile:

| Metric | Estimate | Target |
|--------|---------|--------|
| LCP | ~2.0-2.8s | <2.5s |
| CLS | ~0.05-0.1 | <0.1 |
| INP | ~100-150ms | <200ms |

The large bundled CSS (Bootstrap included in styles.css) is the primary performance concern.

### 5.3 Quick Performance Wins

1. Add `<link rel="preconnect" href="https://cdn.jsdelivr.net">` to `<head>` of all pages
2. Consider splitting Bootstrap out of styles.css and loading it from CDN (avoids double-loading overhead if Bootstrap is loaded both locally and from CDN)
3. Add `width` and `height` attributes to images to prevent CLS

---

## 6. Images

### 6.1 Alt Text Audit

| Issue | Count | Pages |
|-------|-------|-------|
| `alt="..."` (literal dots — meaningless) | 12 | Multiple sidebar images |
| `alt=""` (empty — acceptable for decorative) | 3 | build-a-magnetic-generator.html sidebar |
| Missing alt attribute | 0 | — |

The `alt="..."` pattern is particularly bad — screen readers will read "dot dot dot" and it provides no SEO value.

### 6.2 Broken Image References

| Page | Image URL | Issue |
|------|-----------|-------|
| index.html (OG) | `/assets/magnetic-energy-generator-blueprints.jpg` | File not found in assets folder |
| index.html (OG) | `/assets/magnetic-generator-video.webp` | File referenced in `<img>` src but not in assets |
| index.html | `src="/assets//magnetic-generator-video.webp"` | Double-slash in URL path |

**Note:** The image `magnetic-generator-video.webp` appears to be a video thumbnail that no longer exists. The `<a>` wrapping it links to a ClickBank video page, so this is a broken image wrapping an affiliate CTA.

### 6.3 Image Best Practices

- ✅ Good range of image types (WebP for modern, JPG for older)
- ✅ Float and responsive classes applied correctly
- ❌ No `width` and `height` attributes — Cloudflare can't reserve space, causing layout shift (CLS)
- ❌ Hero/LCP image on homepage is not preloaded (`<link rel="preload">`)

---

## 7. AI Search Readiness

| Signal | Status | Detail |
|--------|--------|--------|
| llms.txt | ❌ Missing | No AI crawler guidance file |
| Structured data | ❌ Missing | Zero schema — AI can't extract structured facts |
| Named author | ❌ Missing | LLMs prefer citable sources with identified authors |
| Factual accuracy | ❌ Risk | Pseudoscientific energy claims won't be cited by LLMs |
| Citation-ready headers | ✅ Partial | Good H2/H3 structure on most pages |
| Content depth | ✅ Pass | Long-form coverage of topics |

AI search engines (Perplexity, ChatGPT, Gemini) are unlikely to cite this site for energy-related queries due to the pseudoscientific framing. The `/magnetic-generator-scam.html` page addressing the "scam" question is actually the best-positioned page for AI citation as it directly addresses a common user question in a structured way.

---

## 8. Internal Linking Analysis

| Finding | Detail |
|---------|--------|
| Navigation | 21 links in the "Pages" dropdown — very comprehensive |
| Sidebar | 5 "Popular Pages" links on every page — consistent |
| In-article links | Good contextual linking to related pages |
| Homepage → About | ❌ No About page to link to |
| Deep linking | Some newer pages (`renewable-energy-using-magnets`, `can-we-use-magnets`) get fewer internal links |
| Anchor text | Mostly descriptive and keyword-rich |

---

## 9. Conversion / Affiliate

All affiliate links use the ClickBank hop URL format with tracking `tid` parameters. This is well-implemented. Each page has:
- At least one in-text affiliate link
- Sidebar ad images linking to ClickBank
- A bottom CTA linking to ClickBank

One issue: the `magnetic-generator-video.webp` image that wraps a ClickBank CTA link on the homepage is broken/missing — this is a **direct conversion impact**.

---
