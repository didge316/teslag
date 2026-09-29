#!/usr/bin/env python3
"""
Scrape 10 relevant articles for each keyword folder.
Saves results to each folder as sources.json
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path('/home/matt/projects/other/tesla-generator/new_content')

# Read the keywords from KEYWORDS-40.md
with open('/home/matt/projects/other/tesla-generator/KEYWORDS-40.md', 'r') as f:
    content = f.read()

# Extract folder names and keywords
folders = []
for line in content.split('\n'):
    stripped = line.strip()
    if re.match(r'^\d+\.\s+\*\*', stripped):
        m = re.search(r'\*\*"([^"]+)"\*\*', stripped)
        if m:
            title = m.group(1)
            slug = title.lower()
            slug = re.sub(r'^is a\s+', '', slug)
            slug = re.sub(r'^(how much does it cost to build a)\s+', '', slug)
            slug = re.sub(r'^(best)\s+', '', slug)
            slug = re.sub(r'^(how to build a)\s+', '', slug)
            slug = re.sub(r'^(Tesla magnetic generator)\s+', 'tesla-magnetic-generator-', slug)
            slug = re.sub(r'^(magnetic generator)\s+', 'magnetic-generator-', slug)
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            slug = re.sub(r'-+', '-', slug)
            slug = slug.strip('-')
            folders.append((slug, title))

# Search queries per keyword
def get_search_queries(keyword):
    """Generate 3-4 search queries for a keyword."""
    kw = keyword.lower()
    queries = [
        kw,
        kw + " review",
        kw + " pros cons",
        kw + " real or fake",
    ]
    return queries

# Search using web_search via subprocess (we'll use curl + Brave/Google)
def search_keyword(keyword):
    """Search for a keyword and return top results."""
    queries = get_search_queries(keyword)
    all_results = []
    
    for query in queries[:3]:  # limit to 3 queries to stay fast
        try:
            result = subprocess.run(
                ['web-search', query, '--json'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for source in data.get('results', []):
                    all_results.append({
                        'url': source.get('url', ''),
                        'title': source.get('title', ''),
                        'snippet': source.get('snippet', ''),
                        'source': source.get('source', ''),
                    })
        except Exception as e:
            pass
    
    # Deduplicate by URL
    seen = set()
    unique = []
    for r in all_results:
        if r['url'] and r['url'] not in seen:
            seen.add(r['url'])
            unique.append(r)
    
    return unique[:10]

# Process each folder
for idx, (slug, keyword) in enumerate(folders):
    folder_path = BASE / slug
    
    if not folder_path.exists():
        print(f"⏳ Skipping {slug} (folder missing)")
        continue
    
    print(f"[{idx+1}/40] Searching: {keyword[:60]}...")
    
    sources = search_keyword(keyword)
    
    output = {
        'keyword': keyword,
        'folder': slug,
        'source_count': len(sources),
        'sources': sources,
    }
    
    sources_file = folder_path / 'sources.json'
    with open(sources_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    status = f"✅ {len(sources)} sources" if sources else "⚠️ no results"
    print(f"  {status}")
    
    time.sleep(0.5)  # brief pause between searches

print("\nDone! Check each folder's sources.json")
