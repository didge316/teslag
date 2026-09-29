# Action Plan — Tesla Magnetic Generator SEO
**Site:** teslamagneticgenerator.com  
**Date:** 2026-05-22  
**Overall Score:** 46/100

---

## CRITICAL — Fix Immediately

### C1. Fix Broken Contact Form
**File:** `website/contact.html:78`  
**Impact:** Trust signal, user experience, Google quality assessment  
**Fix:** Uncomment the `<form>` opening tag and add a working form action (e.g., Formspree or Cloudflare Workers):
```html
<!-- Change this: -->
<!--<form action="https://formspree.io/f/your-form-id" method="POST">-->

<!-- To this: -->
<form action="https://formspree.io/f/YOUR-REAL-FORM-ID" method="POST">
```
Sign up at formspree.io (free tier supports 50 submissions/month), get your form ID, and replace `your-form-id`.

---

### C2. Fix Broken OG Image (Homepage)
**File:** `website/index.html:20`  
**Impact:** Social sharing shows broken image; og:image 404 hurts click-through  
**Fix:** Replace the non-existent file with one that exists:
```html
<!-- Current (404): -->
<meta property="og:image" content="/assets/magnetic-energy-generator-blueprints.jpg" />

<!-- Fix (file exists): -->
<meta property="og:image" content="https://teslamagneticgenerator.com/assets/magnetic-generator-blueprints.webp" />
```
Use an absolute URL for full Open Graph compatibility.

---

### C3. Fix Broken Affiliate Image on Homepage
**File:** `website/index.html:130-131`  
**Impact:** Direct revenue loss — affiliate CTA image is broken/invisible  
**Fix:** Replace the missing `magnetic-generator-video.webp` image. Either:
- Upload a real video thumbnail screenshot to `/assets/`
- Or replace the `<figure>` block with a text CTA or a different existing image
```html
<!-- Current (file missing + double slash): -->
<figure class="mb-4 pt-5"><a href="..."><img src="/assets//magnetic-generator-video.webp" alt="Magnetic Generator Video"/></a></figure>

<!-- Fix — use existing image: -->
<figure class="mb-4 pt-5"><a href="...clickbank..." target="_blank" rel="noopener noreferrer"><img loading="lazy" class="img-fluid rounded" src="/assets/magnetic-generator-free-energy-generator.webp" alt="Watch the magnetic generator video"/></a></figure>
```

---

### C4. Add Schema Markup (All Pages)
**Impact:** +10 points to health score; enables rich results; critical for AI citation  
**Fix:** Add the following to the `<head>` of each content page. Create a template and apply to all 20 content pages.

**Every content page — Article schema:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "COPY H1 TEXT HERE",
  "description": "COPY META DESCRIPTION HERE",
  "url": "COPY CANONICAL URL HERE",
  "datePublished": "2025-12-01",
  "dateModified": "2026-05-22",
  "author": {
    "@type": "Person",
    "name": "Jake Mercer"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Tesla Magnetic Generator",
    "url": "https://teslamagneticgenerator.com"
  },
  "mainEntityOfPage": "COPY CANONICAL URL HERE"
}
</script>
```

**Homepage — also add WebSite schema:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Tesla Magnetic Generator",
  "url": "https://teslamagneticgenerator.com"
}
</script>
```

**Question-format pages — also add FAQPage schema:**  
Apply to: `magnetic-generator-scam.html`, `perpetual-motion-generator.html`, `7-interesting-facts-about-magnets.html`, `How-Much-Noise-Does-a-Free-Energy-Device-Make.html`, `can-I-buy.html`, `is-magnetic-energy-renewable-or-nonrenewable.html`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "QUESTION FROM PAGE H2 OR H3",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "FIRST PARAGRAPH ANSWERING THE QUESTION"
      }
    }
  ]
}
</script>
```

---

### C5. Fix Sitemap.xml
**File:** `website/sitemap.xml`  
**Impact:** Google may index wrong URLs; redirect hop on every crawled URL  
**Fix:** Replace all `.html` URLs with canonical clean URLs AND fix homepage URL:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <url>
    <loc>https://teslamagneticgenerator.com/</loc>
    <lastmod>2025-12-08</lastmod>
    <priority>1.00</priority>
  </url>

  <url>
    <loc>https://teslamagneticgenerator.com/homemade-magnetic-generator</loc>
    <lastmod>2025-12-07</lastmod>
    <priority>0.80</priority>
  </url>

  <!-- etc. — map each .html file to its clean redirect URL from _redirects -->
```

Use the `_redirects` file as the source of truth for the canonical clean URL for each page. The key mappings are:
- `whole-house.html` → `/homemade-magnetic-generator`
- `build-a-magnetic-generator.html` → `/how-to-build-a-magnetic-generator`
- `perpetual-motion-generator.html` → `/perpetual-motion-machines`
- `magnetic-generator-scam.html` → `/tesla-generator-scam`
- etc.

---

## HIGH — Fix Within 1 Week

### H1. Add Article Dates (Published / Updated) Visibly On Page
**All content pages**  
**Impact:** E-E-A-T signal; Google uses visible dates for freshness assessment  
**Fix:** Add a date line below each H1:
```html
<h1 class="fw-bolder mb-1 pb-3">What is a Tesla Generator and Should You Build One?</h1>
<p class="text-muted small mb-4">Published: December 1, 2025 &nbsp;|&nbsp; Updated: May 2026</p>
```

---

### H2. Create an About Page
**File:** Create `website/about.html`  
**Impact:** Critical E-E-A-T signal; Google manual reviewers look for this  
**Fix:** Add a page introducing the site author (can use a pen name like "Jake Mercer") with:
- Why they got interested in DIY generators
- Their DIY background/experience
- How long they've been researching this topic
- Photo (can be stock/generated)

Add "About" to the navigation and footer.

---

### H3. Fix `whole-house.html` Title Tag
**File:** `website/whole-house.html:9`  
**Impact:** Significant — "Can You Really Power Your Home?" misses primary keyword  
**Fix:**
```html
<!-- Current: -->
<title>Can You Really Power Your Home?</title>

<!-- Fixed: -->
<title>Can You Really Build a Magnetic Generator to Power Your Whole Home?</title>
```
Also update the og:title and twitter:title to match.

---

### H4. Fix `alt="..."` on All Sidebar Images
**Impact:** Accessibility compliance; marginal SEO benefit  
**Files:** Multiple — all pages with sidebar images  
**Fix:** Replace `alt="..."` with either:
- A descriptive alt if the image conveys meaning: `alt="Magnetic generator in home workshop"`
- An empty `alt=""` if purely decorative

Run this across all files:
```bash
# Review and manually update each instance
grep -rn 'alt="..."' website/*.html
```
There are 12 instances across the site.

---

### H5. Fix URL Casing & Underscores
**Impact:** Consistency and crawlability  
**Files:** See list below  
- Rename `nikola_tesla_inventor_extraordinaire.html` → `nikola-tesla-inventor-extraordinaire.html` and update `_redirects`, sitemap, all nav links
- Update `_redirects` to handle the old underscore URL with a 301
- Mixed-case files (`How-to-Make...`, `How-Much-Noise...`, `can-I-buy.html`) should ideally be lowercase. Add redirect rules if you rename them.

---

### H6. Add preconnect Hint for CDN
**All pages — `<head>` section**  
**Fix:** Add before the CSS link:
```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
```

---

### H7. Add Width/Height to Images
**Impact:** Reduces CLS (Cumulative Layout Shift)  
**Fix:** Add explicit `width` and `height` attributes to all `<img>` tags to let browsers reserve space before images load. For example:
```html
<img loading="lazy" src="/assets/magnetic-generator-plans.jpg" 
     width="300" height="200" class="img-fluid float-end me-2 mb-2" style="max-width: 30%;">
```

---

### H8. Fix Heading Hierarchy on Homepage
**File:** `website/index.html`  
**Impact:** Structural SEO signal  
**Fix:** The article goes H1 → H3 (skipping H2). Change the first H3 to H2:
```html
<!-- Current: -->
<h3 class="fw-bolder mt-5">Anyone Can Learn How to Build a Tesla Magnetic Generator</h3>

<!-- Fixed: -->
<h2 class="fw-bolder mt-5">Anyone Can Learn How to Build a Tesla Magnetic Generator</h2>
```
Then change subsequent H3s to maintain a logical H1 → H2 → H3 hierarchy.

---

## MEDIUM — Fix Within 1 Month

### M1. Fix OG Images to Use Absolute URLs
**All pages**  
OG images should use absolute URLs for best compatibility with social platforms and WhatsApp.
```html
<!-- Change: -->
<meta property="og:image" content="/assets/image.webp" />
<!-- To: -->
<meta property="og:image" content="https://teslamagneticgenerator.com/assets/image.webp" />
```

---

### M2. Add BreadcrumbList Schema
**All pages except homepage**  
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://teslamagneticgenerator.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "PAGE TITLE",
      "item": "PAGE CANONICAL URL"
    }
  ]
}
```

---

### M3. Create llms.txt
**File:** Create `website/llms.txt`  
**Impact:** AI search readiness; guides LLM crawlers  
```
# Tesla Magnetic Generator
> A resource site about DIY magnetic generator projects, free energy experiments, and Nikola Tesla's electrical inventions.

## Key Pages
- [Homepage](https://teslamagneticgenerator.com/) - Overview and introduction to magnetic generators
- [How to Build a Magnetic Generator](https://teslamagneticgenerator.com/how-to-build-a-magnetic-generator) - Step-by-step guide
- [Magnetic Generator Scam?](https://teslamagneticgenerator.com/tesla-generator-scam) - Honest assessment
- [Nikola Tesla](https://teslamagneticgenerator.com/nikola_tesla_inventor_extraordinaire.html) - Tesla's life and inventions
```

---

### M4. Add Cloudflare Security Headers
**File:** Create `website/_headers`  
```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

### M5. Remove .htaccess
**File:** `website/.htaccess`  
Cloudflare Pages ignores `.htaccess`. Remove it to avoid confusion and reduce the chance of accidentally relying on it.

---

### M6. Improve Homepage Meta Description
**File:** `website/index.html:13`  
Current description has a trailing space and is weak:
> "Thousands of People Have Already Gone Off Grid Thanks to This DIY Generator. "

Replace with:
> "Learn how to build a Tesla magnetic generator at home using step-by-step blueprints. Thousands are already off-grid — discover if a DIY magnetic energy generator is right for you."

---

### M7. Add Structured Comments with Dates
The static comment sections look fake without dates. Add a visible date to each comment:
```html
<div class="fw-bold">Ethan Caldwell <small class="text-muted fw-normal">— January 14, 2026</small></div>
```

---

## LOW — Backlog

### L1. Consolidate Bootstrap Loading
The full Bootstrap CSS (~100KB) is bundled inside `styles.css`. If Bootstrap JS is loaded from CDN, also load Bootstrap CSS from CDN and keep only custom styles in `styles.css`. This reduces page weight and leverages CDN caching.

### L2. Shorten Long Titles
- `build-a-magnetic-generator.html` title is 78 chars — trim to under 60.  
  Suggest: "How to Build a Magnetic Generator at Home — Step-by-Step Plans"

### L3. Add "Popular Posts" Image Thumbnails
The sidebar "Popular Pages" widget is text-only. Adding small thumbnail images next to each link would improve CTR.

### L4. Add Pagination / Date Archive
For the article listing, consider an `articles.html` index page with all posts listed with dates — this supports E-E-A-T and helps users discover content beyond the nav dropdown.

### L5. Consider Clean URL Adoption
The current `.html` file extension URLs create a 301 redirect hop whenever old backlinks hit the site. Consider updating the Cloudflare Pages configuration to serve content at the clean URLs (e.g., `/how-to-build-a-magnetic-generator`) as the primary URL without a redirect.

---

## Priority Matrix

| # | Task | Impact | Effort | Priority |
|---|------|--------|--------|---------|
| C1 | Fix contact form | Medium | 15 min | Critical |
| C2 | Fix OG image (homepage) | Medium | 10 min | Critical |
| C3 | Fix broken affiliate image | High | 15 min | Critical |
| C4 | Add schema markup | Very High | 2-3 hrs | Critical |
| C5 | Fix sitemap URLs | High | 1 hr | Critical |
| H1 | Add article dates | High | 2 hrs | High |
| H2 | Create About page | Very High | 3 hrs | High |
| H3 | Fix whole-house title | Medium | 5 min | High |
| H4 | Fix alt="..." images | Medium | 1 hr | High |
| H5 | Fix URL casing | Medium | 1 hr | High |
| H6 | Add preconnect hint | Low | 15 min | High |
| H7 | Add image width/height | Medium | 2 hrs | High |
| H8 | Fix heading hierarchy | Low | 30 min | High |
| M1 | Absolute OG image URLs | Medium | 1 hr | Medium |
| M2 | BreadcrumbList schema | Medium | 1 hr | Medium |
| M3 | Create llms.txt | Low | 30 min | Medium |
| M4 | Security headers | Low | 15 min | Medium |
| M5 | Remove .htaccess | Low | 5 min | Medium |
| M6 | Improve homepage description | Low | 10 min | Medium |
| L1 | Consolidate Bootstrap | Low | 2 hrs | Low |
| L2 | Shorten long titles | Low | 30 min | Low |
