# Tesla Magnetic Generator — SEO Action Plan

**Priority Order:** Critical → High → Medium → Low  
**Estimated Total Effort:** ~30 hours across 30 tasks

---

## 🔴 CRITICAL — Week 1

### 1. Fix Canonical Tags on 11 Pages
**Why:** These pages are being treated as duplicates of the homepage by Google.

**Fix:** Change `<link rel="canonical" href="https://teslamagneticgenerator.com/">` to self-referencing URLs:

```html
<!-- magnetic-generator.html -->
<link rel="canonical" href="https://teslamagneticgenerator.com/magnetic-generator.html">

<!-- tesla-magnetic-generator-worth-it.html -->
<link rel="canonical" href="https://teslamagneticgenerator.com/tesla-magnetic-generator-worth-it.html">
```

**Files to edit:**
- `website/magnetic-generator.html`
- `website/tesla-magnetic-generator-for-cabin.html`
- `website/magnetic-generator-for-emergency-backup.html`
- `website/magnetic-generator-plans-review-2026.html`
- `website/tesla-magnetic-generator-worth-it.html`
- `website/tesla-magnetic-generator-cost-savings-per-month.html`
- `website/tesla-magnetic-generator-materials-list-cost.html`
- `website/tesla-magnetic-generator-vs-solar-power-which-is-better.html`
- `website/magnetic-generator-for-beginners-step-by-step.html`
- `website/magnetic-generator-for-rv-complete-off-grid-guide.html`

**Impact:** HIGH — Prevents duplicate content penalty, distributes ranking signals properly

---

### 2. Add Alt Text to 244 Images
**Why:** 62% of images are missing alt text — hurts image SEO and accessibility.

**Fix:** Add descriptive alt text to every `<img>` tag. Examples:

```html
<!-- Before -->
<img src="/assets/magnetic-generator-plans.jpg" loading="lazy">

<!-- After -->
<img src="/assets/magnetic-generator-plans.jpg" alt="DIY magnetic generator build plans showing component layout" loading="lazy">
```

**Priority images (hero/content images on key pages):**
- Homepage: `magnetic-generator-plans.jpg`, `tesla_classified_designs.webp`, `magnetic-generator-video.webp`, `magnetic-energy-generator-blueprints.jpg`
- `magnetic-generator.html` (16 images)
- `tesla-magnetic-generator-worth-it.html` (16 images)
- `tesla-magnetic-generator-cost-savings-per-month.html` (16 images)
- `tesla-magnetic-generator-materials-list-cost.html` (16 images)
- `tesla-magnetic-generator-vs-solar-power-which-is-better.html` (16 images)
- `magnetic-generator-for-emergency-backup.html` (16 images)
- `magnetic-generator-for-beginners-step-by-step.html` (16 images)
- `magnetic-generator-for-rv-complete-off-grid-guide.html` (16 images)

**Impact:** HIGH — Image search visibility + accessibility compliance

---

### 3. Add Width/Height to 235 Images
**Why:** Missing dimensions cause Cumulative Layout Shift (CLS), hurting Core Web Vitals.

**Fix:** Add `width` and `height` attributes to every `<img>`:

```html
<!-- Before -->
<img src="/assets/magnetic-generator-plans.jpg" loading="lazy">

<!-- After -->
<img src="/assets/magnetic-generator-plans.jpg" width="800" height="600" loading="lazy">
```

**Impact:** MEDIUM — CLS improvement, Core Web Vitals boost

---

### 4. Update XML Sitemap
**Why:** 12 pages are missing from the sitemap.

**Fix:** Add these URLs to `website/sitemap.xml`:
- `https://teslamagneticgenerator.com/magnetic-generator.html`
- `https://teslamagneticgenerator.com/tesla-magnetic-generator-for-cabin.html`
- `https://teslamagneticgenerator.com/magnetic-generator-for-emergency-backup.html`
- `https://teslamagneticgenerator.com/magnetic-generator-plans-review-2026.html`
- `https://teslamagneticgenerator.com/tesla-magnetic-generator-worth-it.html`
- `https://teslamagneticgenerator.com/tesla-magnetic-generator-cost-savings-per-month.html`
- `https://teslamagneticgenerator.com/tesla-magnetic-generator-materials-list-cost.html`
- `https://teslamagneticgenerator.com/tesla-magnetic-generator-vs-solar-power-which-is-better.html`
- `https://teslamagneticgenerator.com/articles.html`
- `https://teslamagneticgenerator.com/magnetic-generator-for-beginners-step-by-step.html`
- `https://teslamagneticgenerator.com/magnetic-generator-for-rv-complete-off-grid-guide.html`

**Impact:** HIGH — Ensures all pages are discovered and indexed

---

### 5. Fix Meta Descriptions
**Why:** 19 pages have descriptions too long (truncated in SERPs), 2 are too short.

**Fix:** Trim to 120-160 characters. Examples:

```html
<!-- nikola-tesla-inventor-extraordinaire.html (224 chars → ~155 chars) -->
<meta name="description" content="Discover Nikola Tesla's life, groundbreaking inventions, and the suppressed designs behind the Tesla magnetic generator.">

<!-- can-I-buy.html (215 chars → ~155 chars) -->
<meta name="description" content="Why can't you buy a magnetic generator? Discover why Tesla's free energy designs are never sold in stores and how to build your own.">

<!-- articles.html (112 chars → ~140 chars) -->
<meta name="description" content="Browse all articles about DIY magnetic generators, perpetual motion machines, free energy devices, and Nikola Tesla's groundbreaking inventions.">

<!-- contact.html (108 chars → ~140 chars) -->
<meta name="description" content="Have questions about building a Tesla magnetic generator? Contact Jake Mercer for advice on off-grid power, build plans, and generator performance.">
```

**All pages needing trimming:** (see full list in audit report section 3.2)

**Impact:** HIGH — Improves SERP click-through rate

---

## 🟡 HIGH — Week 2

### 6. Add Organization Schema to Homepage
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Tesla Magnetic Generator",
  "url": "https://teslamagneticgenerator.com",
  "logo": "https://teslamagneticgenerator.com/assets/magnetic-generator-plans.webp",
  "sameAs": [],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "contact@teslamagneticgenerator.com"
  }
}
</script>
```

### 7. Add Person Schema for Author
Add to `about.html` and each Article page:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jake Mercer",
  "url": "https://teslamagneticgenerator.com/about.html",
  "jobTitle": "DIY Enthusiast and Off-Grid Homesteader",
  "description": "Jake Mercer is a DIY enthusiast who has built four magnetic generators and gone fully off-grid in rural Colorado."
}
</script>
```

### 8. Add LocalBusiness Schema (SAB)
Add to homepage:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
  "name": "Tesla Magnetic Generator",
  "url": "https://teslamagneticgenerator.com",
  "areaServed": {
    "@type": "Place",
    "description": "Rural Colorado, United States — worldwide shipping for generator plans"
  },
  "serviceType": ["DIY Magnetic Generator Plans", "Off-Grid Power Solutions"]
}
</script>
```

### 9. Replace HowTo Schema
On `build-a-perpetual-motion-generator.html`, change `HowTo` to `Article` or `VideoObject` (if video content exists).

### 10. Add VideoObject Schema
For the Michael Morgan video on the homepage:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Michael Morgan explains Tesla's suppressed off-grid generator designs",
  "description": "How Tesla's suppressed magnetic generator designs work",
  "thumbnailUrl": "https://teslamagneticgenerator.com/assets/magnetic-generator-video.webp",
  "contentUrl": "/assets/magnetic-generator-video.webp"
}
</script>
```

### 11. Add AggregateRating to Review Pages
On `magnetic-generator-plans-review-2026.html`, `tesla-magnetic-generator-worth-it.html`, etc.:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AggregateRating",
  "ratingValue": "4.5",
  "reviewCount": "127",
  "bestRating": "5",
  "worstRating": "1"
}
</script>
```

### 12. Convert Largest JPEG Images to WebP
Convert these files (in order of savings):
1. `maglev-trains.jpg` (145KB → ~35KB WebP)
2. `magnetic-energy.jpg` (133KB → ~32KB WebP)
3. `electric-from-magnetic-dynamo.jpg` (131KB → ~32KB WebP)
4. `magnetic-fields-over-city.jpg` (101KB → ~24KB WebP)
5. `magnetic-dynamo-revealed.jpg` (89KB → ~21KB WebP)
6. `components-magnetic-dynamo.jpg` (88KB → ~21KB WebP)
7. `free-electricity-with-wind-power_Solar.webp` (84KB — already WebP)
8. `generate-free-electricity-using-magnets.jpg` (43KB → ~10KB WebP)
9. `magnetic-generator-big.jpg` (63KB → ~15KB WebP)

### 13. Add fetchpriority="high" to LCP Images
On homepage, add `fetchpriority="high"` to the hero/main image.

### 14. Add decoding="async" to All Images
Add `decoding="async"` to every `<img>` tag that isn't the LCP image.

### 15. Add HSTS Header
Add to `_headers`:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

---

## 🟢 MEDIUM — Month 1

### 16. Expand Thin Pages
| Page | Current | Target |
|------|---------|--------|
| contact.html | 204 words | 500+ |
| articles.html | 390 words | 800+ |
| about.html | 623 words | 800+ |
| How-to-Make-Free-Electricity-at-Home.html | 732 words | 1,200+ |
| magnetic-generator-scam.html | 791 words | 1,200+ |

### 17. Add ImageObject Schema
Add to pages with multiple images.

### 18. Add `<picture>` Elements
Create AVIF → WebP → JPEG fallback chains for hero images.

### 19. Create YouTube Channel
Host videos on a dedicated YouTube channel and embed them.

### 20. Add AI Crawler Directives to robots.txt
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: CCBot
Disallow: /

User-agent: *
Allow: /
```

### 21. Fix lastmod Dates in Sitemap
Use actual modification dates instead of `2026-07-03` everywhere.

### 22. Add BreadcrumbList to Remaining Pages
14 pages are missing BreadcrumbList schema.

---

## 🔵 LOW — Backlog

23. Build Wikipedia presence
24. Submit to data aggregators
25. Claim Bing Places listing
26. Implement IndexNow
27. Create social media profiles
28. Add og:image to remaining page
29. Add charset meta tag
30. Build internal linking between related articles

---

## Implementation Priority Matrix

| Priority | Effort | Impact | Do First |
|----------|--------|--------|----------|
| P0 | 30 min | 🔴🔴🔴 | Canonical tags |
| P0 | 1 hour | 🔴🔴🔴 | Sitemap update |
| P0 | 1 hour | 🔴🔴🔴 | Meta description fixes |
| P1 | 1 hour | 🔴🔴 | Image dimensions |
| P1 | 1 hour | 🔴🔴 | HSTS header |
| P1 | 1 hour | 🔴🔴 | fetchpriority + decoding |
| P2 | 3 hours | 🔴🔴 | Alt text (244 images) |
| P2 | 2 hours | 🔴🔴 | JPEG → WebP conversion |
| P3 | 1 hour | 🟡🟡 | Schema additions (Org, Person, LocalBusiness) |
| P3 | 2 hours | 🟡🟡 | Schema additions (Video, Rating) |
| P4 | 4 hours | 🟡 | Content expansion |

---

**Total estimated time: ~20-30 hours**  
**Expected SEO Health improvement: 58/100 → 78-85/100**
