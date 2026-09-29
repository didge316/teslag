# Tesla Generator — Rebuild Plan

## Current State
- 40 keyword folders exist in `new_content/`
- Only 3 folders have intact `sources.json` (garden, truck, patio — these were Phase 3 keywords)
- 37 folders have empty `sources.json` (lost during JSON fix script)
- 58 YouTube video transcripts saved in `/tmp/all_transcripts.txt`
- 1 YouTube transcript script at `/home/matt/.pi/agent/skills/youtube-transcript/`
- `scrape_sources.py` exists but Google search returns empty (likely cookie/auth issue)
- SearXNG at `localhost:8080` works for web search

## Root Cause of Data Loss
The transcript-saving script had a JSON fix loop that processed ALL files, not just ones with YouTube URLs. When `jsonWasFixed` was true, it wrote back the entire file — but the fix loop only preserved lines matching a specific pattern, dropping array brackets and non-string-value lines like `"sources": [`.

## What We Have (Safe to Preserve)
- `/tmp/all_transcripts.txt` — 58 video transcripts (15,000+ lines)
- `/home/matt/.pi/agent/skills/youtube-transcript/transcript.js` — working transcript fetcher
- `KEYWORDS-40.md` — master keyword list with strategy
- `TRACKER.md` — tracking file (all 40 marked Done)
- `scrape_sources.py` — scraping script
- Website repo at `website/` — deployed site

## What We Need (37 folders to repopulate)

### Step 1: Deep-search all 37 empty folders (10 sources each = 370 sources)
- Use SearXNG search for each keyword
- Pick the best 10 sources per keyword
- Save as `sources.json` with proper structure
- **Key: write files with `fs.writeFileSync` directly, not via a fix loop**

### Step 2: Fetch YouTube transcripts for any YouTube URLs found
- Use the transcript script for each YouTube URL
- Save transcript data into the `sources.json` files
- **Key: only write files that actually have YouTube URLs**

### Step 3: Write Phase 1 articles (keywords 1-10)
- Read each folder's `sources.json`
- Fetch full article content from top sources
- Write 1500-2000 word SEO articles
- Include internal links
- Save as `.md` in the folder

### Step 4: Deploy to website

## Safety Rules for This Run
1. **Never** do a "fix JSON" pass that could overwrite files — always parse first, fix in-memory, write only if needed
2. **Never** write back a file unless it actually changed (compare before/after)
3. **Always** verify JSON validity after writing
4. **Always** verify source count after writing
5. Keep transcript data in `/tmp/` as backup throughout
6. Commit to git after each major step

## Keyword Priority Order (from KEYWORDS-40.md)
### Phase 1 (write first):
1. is a Tesla magnetic generator worth it
2. how much does it cost to build a magnetic generator
3. Tesla magnetic generator vs solar power which is better
4. Tesla magnetic generator cost savings per month
5. magnetic generator for RV
6. Tesla magnetic generator for cabin
7. magnetic generator for emergency backup
8. Tesla magnetic generator materials list cost
9. best magnetic generator plans review 2026
10. magnetic generator for beginners

### Phase 2:
11-20: bifilar pancake coil, electricity production, home how it works, real or fake, noise level, maintenance, small home, workshop, lifespan, vs wind turbine

### Phase 3:
21-40: boat, shed, battery storage, inverter, wiring, chicken coop, greenhouse, garage, fence, water pump, well pump, fridge, lights, phone charging, van life, tiny house, camper, shed workshop, homestead, preppers
