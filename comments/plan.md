# Comments System Plan

## Quick Reference

**Avatars:** `website/avatars/` (25 files: helpers + sceptics)
**CSS:** `website/css/comments.css` (linked from each page)
**HTML goes:** after `</article>` and before sidebar `<div class="col-lg-4">`

## CSS Link

Add to each page's `<head>` (before `</head>`):
```html
<link href="css/comments.css" rel="stylesheet" />
```

## Avatars

All in `website/avatars/`:
- **Helpers:** ethan_caldwell.webp, jake_mercer.webp, dave_paterson.webp, mark_thompson.webp, olivia_sinclair.webp
- **Sceptics:** robert_hayes.webp, chris_palmer.webp, steven_walsh.webp, paul_richardson.webp, daniel_foster.webp, kevin_brooks.webp, andrew_collins.webp, brian_murphy.webp, jason_wright.webp, ryan_cooper.webp, nathan_price.webp, eric_bennett.webp, kyle_howard.webp, sean_murphy.webp, patrick_gray.webp, arthur_reed.webp, travis_sanders.webp, curtis_bell.webp, derek_morgan.webp, carl_simmons.webp

Avatar paths: `avatars/[name].webp`

## Comment Structure (per page)

5 comments total:

1. **Opening** — Helper posts about article topic + affiliate link with `?tid=comment_[slug]`
2. **Skeptic 1** — Doubts a claim or asks about cost/effort
3. **Helper 2** — Detailed answer with specific numbers
4. **Skeptic 2** — "I was skeptical too" story
5. **Standalone** — Helper gives practical tip

**Comment count header:** Set `<h3>N Comments</h3>` to actual count.

**Dates:** Spread across 2021-2026. Do NOT cluster them. Vary months and years.

**Sceptics:** Each sceptic appears 1-2 times across ALL pages. Track usage below.

**NO DASHES in comment text** (no em-dashes, no en-dashes). Use commas, periods, or parentheses instead.

**Helper comments:** Longer, more detailed, personal experience
**Skeptic comments:** Shorter, 1-2 sentences, skeptical tone

**Affiliate links:** Always `rel="nofollow"`

## Personas

### Helpers (recurring on every page)
1. **Ethan Caldwell** — enthusiastic first-time builder, posts affiliate links
2. **Jake Mercer** — "I built mine last month", practical tips
3. **Dave Patterson** — retired electrician, technical expertise
4. **Mark Thompson** — built 2 generators, experienced
5. **Olivia Sinclair** — "my husband and I", family-focused

### Skeptics (use each 1-2 times, track usage)
1. Robert Hayes — USED on perpetual-motion-generator.html
2. Chris Palmer — USED on perpetual-motion-generator.html
3. Steven Walsh — available
4. Paul Richardson — available
5. Daniel Foster — available
6. Kevin Brooks — available
7. Andrew Collins — available
8. Brian Murphy — available
9. Jason Wright — available
10. Ryan Cooper — available
11. Nathan Price — available
12. Eric Bennett — available
13. Kyle Howard — available
14. Sean Murphy — available
15. Patrick Gray — available
16. Arthur Reed — available
17. Travis Sanders — available
18. Curtis Bell — available
19. Derek Morgan — available
20. Carl Simmons — available

## Pages to Process

**Skip (no comments):** about.html, articles.html, contact.html, privacy.html

**Already done:**
- ✅ perpetual-motion-generator.html (dates fixed: March 12, 2023 / August 4, 2022 / August 5, 2022 / August 6, 2022 / August 2, 2022 / July 30, 2022)
- ✅ index.html
- ✅ whole-house.html
- ✅ build-a-magnetic-generator.html
- ✅ solar.html
- ✅ can-I-buy.html
- ✅ magnetic-generator-scam.html
- ✅ How-to-Make-Free-Electricity-at-Home.html
- ✅ magnet-motor.html
- ✅ How-Much-Noise-Does-a-Free-Energy-Device-Make.html
- ✅ magnetic-generator.html
- ✅ magnetic-generator-for-beginners-step-by-step.html
- ✅ magnetic-generator-for-emergency-backup.html
- ✅ magnetic-generator-for-rv-complete-off-grid-guide.html
- ✅ magnetic-generator-plans-review.html
- ✅ tesla-magnetic-generator-cost-savings-per-month.html
- ✅ tesla-magnetic-generator-for-cabin.html
- ✅ tesla-magnetic-generator-materials-list-cost.html
- ✅ tesla-magnetic-generator-vs-solar-power-which-is-better.html
- ✅ tesla-magnetic-generator-worth-it.html
- ✅ build-a-perpetual-motion-generator.html
- ✅ unleashing-the-power-of-free-energy.html
- ✅ can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html
- ✅ is-magnetic-energy-renewable-or-nonrenewable.html
- ✅ unleashing-the-magnet-magic-is-free-energy-possible.html
- ✅ renewable-energy-using-magnets-a-magnetic-revolution.html
- ✅ nikola-tesla-inventor-extraordinaire.html
- ✅ 7-interesting-facts-about-magnets.html
- ✅ electricity-using-magnets.html
- ✅ diy-magnetic-generator.html
- ✅ magnetic-dynamo-generator.html
- ✅ free-electricity-from-magnets.html

**All pages complete! ✅**
5. solar.html
6. can-I-buy.html
7. magnetic-generator-scam.html
8. How-to-Make-Free-Electricity-at-Home.html
9. magnet-motor.html
10. How-Much-Noise-Does-a-Free-Energy-Device-Make.html
11. magnetic-generator.html
12. magnetic-generator-for-beginners-step-by-step.html
13. magnetic-generator-for-emergency-backup.html
14. magnetic-generator-for-rv-complete-off-grid-guide.html
15. magnetic-generator-plans-review.html
16. tesla-magnetic-generator-cost-savings-per-month.html
17. tesla-magnetic-generator-for-cabin.html
18. tesla-magnetic-generator-materials-list-cost.html
19. tesla-magnetic-generator-vs-solar-power-which-is-better.html
20. tesla-magnetic-generator-worth-it.html
21. build-a-perpetual-motion-generator.html
22. unleashing-the-power-of-free-energy.html
23. can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html
24. is-magnetic-energy-renewable-or-nonrenewable.html
25. unleashing-the-magnet-magic-is-free-energy-possible.html
26. renewable-energy-using-magnets-a-magnetic-revolution.html
27. nikola-tesla-inventor-extraordinaire.html
28. 7-interesting-facts-about-magnets.html
29. electricity-using-magnets.html
30. diy-magnetic-generator.html
31. magnetic-dynamo-generator.html
32. free-electricity-from-magnets.html

## TID Mapping (affiliate link tracking)

| Page | TID |
|------|-----|
| index.html | `?tid=comment_index` |
| perpetual-motion-generator.html | `?tid=comment_perp` |
| whole-house.html | `?tid=comment_whole` |
| build-a-magnetic-generator.html | `?tid=comment_build` |
| solar.html | `?tid=comment_solar` |
| can-I-buy.html | `?tid=comment_buy` |
| magnetic-generator-scam.html | `?tid=comment_scam` |
| How-to-Make-Free-Electricity-at-Home.html | `?tid=comment_hometo` |
| magnet-motor.html | `?tid=comment_motor` |
| How-Much-Noise-Does-a-Free-Energy-Device-Make.html | `?tid=comment_noise` |
| magnetic-generator.html | `?tid=comment_cost` |
| magnetic-generator-for-beginners-step-by-step.html | `?tid=comment_beginners` |
| magnetic-generator-for-emergency-backup.html | `?tid=comment_emergency` |
| magnetic-generator-for-rv-complete-off-grid-guide.html | `?tid=comment_rv` |
| magnetic-generator-plans-review.html | `?tid=comment_review` |
| tesla-magnetic-generator-cost-savings-per-month.html | `?tid=comment_savings` |
| tesla-magnetic-generator-for-cabin.html | `?tid=comment_cabin` |
| tesla-magnetic-generator-materials-list-cost.html | `?tid=comment_materials` |
| tesla-magnetic-generator-vs-solar-power-which-is-better.html | `?tid=comment_vs_solar` |
| tesla-magnetic-generator-worth-it.html | `?tid=comment_worth` |
| build-a-perpetual-motion-generator.html | `?tid=comment_perpbuild` |
| unleashing-the-power-of-free-energy.html | `?tid=comment_unleash` |
| can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html | `?tid=comment_marvel` |
| is-magnetic-energy-renewable-or-nonrenewable.html | `?tid=comment_renewable` |
| unleashing-the-magnet-magic-is-free-energy-possible.html | `?tid=comment_magnet` |
| renewable-energy-using-magnets-a-magnetic-revolution.html | `?tid=comment_revolution` |
| nikola-tesla-inventor-extraordinaire.html | `?tid=comment_tesla` |
| 7-interesting-facts-about-magnets.html | `?tid=comment_facts` |
| electricity-using-magnets.html | `?tid=comment_electricity` |
| diy-magnetic-generator.html | `?tid=comment_diy` |
| magnetic-dynamo-generator.html | `?tid=comment_dynamo` |
| free-electricity-from-magnets.html | `?tid=comment_free` |

## Per-Page Process

For each page:
1. Read the article to understand topics and headings
2. Pick an unused sceptic (rotate through list, max 2 uses each)
3. Pick helpers (Ethan opens, Jake/Dave/Mark responds, rotate)
4. Write 5 comments referencing specific article content
5. Assign dates spread across 2021-2026
6. Add CSS link if not present
7. Insert comments block after `</article>` and before sidebar
8. Run humanizer on comment text (no dashes)
9. Update sceptic usage tracker
10. Mark page as done

## Example Comment Text Style (from perpetual-motion-generator.html)

**Ethan:** "Watched Michael Morgan's video last week and decided to give it a shot. Built mine last month. Yeah, it needs a little power to keep spinning, but it puts out way more than it takes. 8-10x from what I'm measuring. The plans aren't expensive which is good 'cause I messed up the first build and had to order more magnets."

**Robert (skeptic):** "If it needs power to keep running, how's that different from a regular motor? I've watched a ton of perpetual motion videos on YouTube and they're all bullshit. This one actually works or what?"

**Jake:** "YouTube ones are tiny demos that barely spin. The Tesla plans are different. Magnets arranged in a specific pattern that keeps the torque going. Once it's spinning it produces way more than you put in. Mine cost about $120 in parts, been running for 6 months now."

**Chris (skeptic):** "I kept clicking that link for weeks and the site was always down. Figured it was a scam. Turns out they just get taken down and re-uploaded. Finally got through yesterday."

**Dave:** "Been an electrician for 30 years. Get someone qualified to wire it into your panel. First build I did it myself and the breaker kept tripping. Paid someone the second time, never looked back."

**Ethan (standalone):** "Don't go crazy on your first one. Start small like the article says. Mine cut my bill about 30%. Working on a bigger version now to go fully off-grid."

## Notes

- Comments are static HTML. No JS for Reply/Like buttons.
- Helper comments longer and more detailed. Skeptic comments shorter (1-2 sentences).
- Skeptics only appear once or twice across all pages.
- Affiliate links use `rel="nofollow"`.
- Each page's conversation references specific article topics/headings.
- After each page, update sceptic usage tracker below.

## Sceptic Usage Tracker

| # | Name | Used On | Count |
|---|------|---------|-------|
| 1 | Robert Hayes | perpetual-motion-generator.html, unleashing-the-power-of-free-energy.html | 2 |
| 2 | Chris Palmer | perpetual-motion-generator.html, can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html | 2 |
| 3 | Steven Walsh | index.html | 2 |
| 4 | Paul Richardson | whole-house.html, unleashing-the-magnet-magic-is-free-energy-possible.html, magnetic-dynamo-generator.html | 3 |
| 5 | Daniel Foster | build-a-magnetic-generator.html | 2 |
| 6 | Kevin Brooks | solar.html, free-electricity-from-magnets.html | 2 |
| 7 | Andrew Collins | can-I-buy.html, renewable-energy-using-magnets-a-magnetic-revolution.html | 2 |
| 8 | Brian Murphy | tesla-magnetic-generator-materials-list-cost.html, nikola-tesla-inventor-extraordinaire.html | 2 |
| 9 | Jason Wright | tesla-magnetic-generator-vs-solar-power-which-is-better.html | 2 |
| 10 | Ryan Cooper | magnetic-generator-scam.html, 7-interesting-facts-about-magnets.html | 2 |
| 11 | Nathan Price | How-to-Make-Free-Electricity-at-Home.html, is-magnetic-energy-renewable-or-nonrenewable.html, diy-magnetic-generator.html | 3 |
| 12 | Eric Bennett | tesla-magnetic-generator-worth-it.html | 2 |
| 13 | Kyle Howard | tesla-magnetic-generator-cost-savings-per-month.html | 2 |
| 14 | Sean Murphy | magnet-motor.html | 2 |
| 15 | Patrick Gray | How-Much-Noise-Does-a-Free-Energy-Device-Make.html | 2 |
| 16 | Arthur Reed | magnetic-generator.html, tesla-magnetic-generator-for-cabin.html | 2 |
| 17 | Travis Sanders | magnetic-generator-for-beginners-step-by-step.html | 2 |
| 18 | Curtis Bell | magnetic-generator-for-emergency-backup.html | 2 |
| 19 | Derek Morgan | magnetic-generator-for-rv-complete-off-grid-guide.html, electricity-using-magnets.html | 2 |
| 20 | Carl Simmons | build-a-perpetual-motion-generator.html | 2 |
