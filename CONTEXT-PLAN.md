# Tesla Generator — Rebuild Context & Action Plan

## Context Reset Instructions
> Clear this agent's context and load this plan fresh. All working files are preserved on disk.

---

## What Exists on Disk (Safe)

### Project Structure
```
/home/matt/projects/other/tesla-generator/
├── KEYWORDS-40.md                    # Master keyword list + strategy (READ-ONLY)
├── HANDOFF.md                        # Original handoff notes (READ-ONLY)
├── REBUILD-PLAN.md                   # This plan
├── new_content/
│   ├── TRACKER.md                    # All 40 keywords marked ✅ Done
│   ├── scrape_sources.py             # Scraping script (Google search, currently broken)
│   └── [40 keyword folders]/
│       └── sources.json              # 3 intact, 37 empty
├── website/                          # Deployed site (git repo)
│   └── .git/
└── /tmp/
    └── all_transcripts.txt           # 58 YouTube video transcripts (15,000+ lines)
```

### 3 Intact Folders (sources.json preserved)
| Folder | Sources | YouTube URLs |
|--------|---------|--------------|
| `tesla-magnetic-generator-for-garden` | 10 | 5 |
| `tesla-magnetic-generator-for-truck` | 10 | 4 |
| `tesla-magnetic-generator-for-patio` | 10 | 1 |

### 37 Empty Folders (need repopulating)
All 40 keyword folders exist. These 37 have `sources.json` with `source_count: 0` and empty `sources: []`:

**Phase 1 (Product-Adjacent, highest priority):**
1. `tesla-magnetic-generator-worth-it` — "is a Tesla magnetic generator worth it"
2. `magnetic-generator` — "how much does it cost to build a magnetic generator"
3. `tesla-magnetic-generator-vs-solar-power-which-is-better` — "Tesla magnetic generator vs solar power which is better"
4. `tesla-magnetic-generator-cost-savings-per-month` — "Tesla magnetic generator cost savings per month"
5. `magnetic-generator-for-rv-complete-off-grid-guide` — "magnetic generator for RV"
6. `tesla-magnetic-generator-for-cabin` — "Tesla magnetic generator for cabin"
7. `magnetic-generator-for-emergency-backup` — "magnetic generator for emergency backup"
8. `tesla-magnetic-generator-materials-list-cost` — "Tesla magnetic generator materials list cost"
9. `magnetic-generator-plans-review-2026` — "best magnetic generator plans review 2026"
10. `magnetic-generator-for-beginners-step-by-step` — "magnetic generator for beginners"

**Phase 2 (Authority Building):**
11. `tesla-magnetic-generator-bifilar-pancake-coil-explained`
12. `how-much-electricity-does-a-magnetic-generator-produce`
13. `tesla-magnetic-generator-for-home-how-it-works`
14. `free-energy-magnetic-generator-real-or-fake`
15. `magnetic-generator-noise-level`
16. `tesla-magnetic-generator-maintenance-requirements`
17. `magnetic-generator-for-small-home`
18. `tesla-magnetic-generator-for-workshop`
19. `magnetic-generator-lifespan`
20. `tesla-magnetic-generator-vs-wind-turbine`

**Phase 3 (Niche Use Cases):**
21. `magnetic-generator-for-boat`
22. `tesla-magnetic-generator-for-shed`
23. `magnetic-generator-battery-storage`
24. `tesla-magnetic-generator-inverter-setup`
25. `magnetic-generator-wiring-diagram`
26. `tesla-magnetic-generator-for-chicken-coop`
27. `magnetic-generator-for-greenhouse`
28. `tesla-magnetic-generator-for-garage`
29. `magnetic-generator-for-fence`
30. `tesla-magnetic-generator-for-water-pump`
31. `magnetic-generator-for-well-pump`
32. `tesla-magnetic-generator-for-fridge`
33. `magnetic-generator-for-lights`
34. `tesla-magnetic-generator-for-phone-charging`
35. `magnetic-generator-for-van-life`
36. `tesla-magnetic-generator-for-tiny-house`
37. `magnetic-generator-for-camper`
38. `tesla-magnetic-generator-for-shed-workshop`
39. `magnetic-generator-for-homestead`
40. `tesla-magnetic-generator-for-preppers`

### YouTube Transcripts
- File: `/tmp/all_transcripts.txt` (15,464 lines, 58 videos)
- Each transcript is timestamped: `[0:02] text here`
- 6 videos had no captions available
- Transcript fetcher: `/home/matt/.pi/agent/skills/youtube-transcript/transcript.js`

### Search Tools
- **SearXNG**: `/home/matt/.pi/agent/skills/searxng/search.sh "query" -n 10` (works, localhost:8080)
- **scrape_sources.py**: Google search based (currently returns empty — likely cookie/auth issue)

### Website
- Domain: `teslamagneticgenerator.com`
- Deployed from: `/home/matt/projects/other/tesla-generator/website/`
- Git repo: `website/.git`
- Product: ClickBank "Complete Ultimate OFF-GRID Generator" (account: didge2009)

---

## Action Plan (Execute in Order)

### STEP 1: Deep-Search All 37 Empty Folders

**Goal:** Create `sources.json` with 10 sources per folder for all 37 empty folders.

**Process per folder:**
1. Read the keyword from `KEYWORDS-40.md` (or the folder's existing `sources.json` keyword field)
2. Run SearXNG search: `/home/matt/.pi/agent/skills/searxng/search.sh "<keyword>" -n 10 --content`
3. From results, pick the 10 best sources (mix of YouTube, articles, forums, videos)
4. For each source, include: url, title, snippet, domain, relevance_score (0.50-0.95)
5. Write to `new_content/<folder>/sources.json`

**sources.json format:**
```json
{
  "keyword": "exact keyword phrase",
  "folder": "folder-name",
  "source_count": 10,
  "sources": [
    {
      "url": "https://...",
      "title": "Source Title",
      "snippet": "Relevant snippet from the source...",
      "domain": "example.com",
      "relevance_score": 0.90
    }
  ]
}
```

**IMPORTANT:** Write files directly with `write` tool. Do NOT run a JSON fix loop. Do NOT parse-then-write-back. Just write the complete JSON.

**Execution order:** Phase 1 first (1-10), then Phase 2 (11-20), then Phase 3 (21-37).

**SearXNG usage pattern:**
```bash
/home/matt/.pi/agent/skills/searxng/search.sh "Tesla magnetic generator worth it" -n 10 --content
```

### STEP 2: Fetch YouTube Transcripts

**Goal:** Attach transcript data to all YouTube sources across ALL 40 folders.

**Process:**
1. Find all YouTube URLs: `grep -roh '"url": "https://www.youtube.com/watch?v=[^"]*"' new_content/ -r`
2. Extract video IDs and fetch transcripts using `/home/matt/.pi/agent/skills/youtube-transcript/transcript.js`
3. For each YouTube source in every `sources.json`, add:
   - `hasTranscript: true/false`
   - If true: `transcript: [{timestamp, text}, ...]`
   - If false: `transcriptError: "reason"`

**IMPORTANT:** Only write a `sources.json` file if it actually has YouTube URLs. Don't write files that don't need changes.

### STEP 3: Write Phase 1 Articles (10 articles)

**Goal:** Write 1,500-2,000 word SEO articles for Phase 1 keywords.

**Process per article:**
1. Read the folder's `sources.json` for reference URLs
2. Fetch full content from top 3-5 sources using SearXNG `--content` flag
3. Write a 1,500-2,000 word article that:
   - Uses the keyword naturally (alternate "Tesla magnetic generator" / "magnetic generator")
   - Includes data from multiple sources
   - Has proper headings (H2, H3)
   - Includes internal links to other Phase 1 articles
   - Has a clear conclusion with Call-to-Action
4. Save as `<folder>/article.md`
5. Update `TRACKER.md` with article status

**Phase 1 keywords (in write order):**
1. is a Tesla magnetic generator worth it
2. how much does it cost to build a magnetic generator
3. Tesla magnetic generator vs solar power which is better
4. Tesla magnetic generator cost savings per month
5. best magnetic generator plans review 2026
6. magnetic generator for beginners
7. Tesla magnetic generator materials list cost
8. magnetic generator for RV
9. Tesla magnetic generator for cabin
10. magnetic generator for emergency backup

### STEP 4: Deploy to Website

**Goal:** Deploy finished articles to the live site.

**Process:**
1. Copy `.md` files from `new_content/` to appropriate location in `website/`
2. Commit and push to `website/.git`
3. Verify site is live at `teslamagneticgenerator.com`

---

## Safety Rules (DO NOT VIOLATE)

1. **Never** run a "fix JSON" loop that iterates all files and writes them back
2. **Always** write complete JSON files — don't parse, modify a single field, and re-write the whole file
3. **Always** verify JSON validity after writing: `node -e "JSON.parse(require('fs').readFileSync('file'))"`
4. **Always** verify source count after writing: count `"url"` occurrences
5. **Always** backup `/tmp/all_transcripts.txt` before any major operation
6. **Never** overwrite a folder's `sources.json` unless you've just populated it
7. **Commit to git** after completing each major step (especially after Step 1)

## Files to Preserve (Never Overwrite)
- `KEYWORDS-40.md`
- `HANDOFF.md`
- `REBUILD-PLAN.md`
- `new_content/TRACKER.md`
- `new_content/scrape_sources.py`
- `/tmp/all_transcripts.txt`

## Quick Reference
- Work dir: `/home/matt/projects/other/tesla-generator/`
- Content dir: `/home/matt/projects/other/tesla-generator/new_content/`
- Website dir: `/home/matt/projects/other/tesla-generator/website/`
- Search tool: `/home/matt/.pi/agent/skills/searxng/search.sh`
- Transcript tool: `/home/matt/.pi/agent/skills/youtube-transcript/transcript.js`
- Transcript data: `/tmp/all_transcripts.txt`
