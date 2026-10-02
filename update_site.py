#!/usr/bin/env python3
"""
Add Phase 1 articles to sitemap and navigation.
"""

import re
from pathlib import Path

WEBSITE = Path("/home/matt/projects/other/tesla-generator/website")
SITE_URL = "https://teslamagneticgenerator.com"

# Phase 1 articles to add
PHASE1_ARTICLES = [
    ("magnetic-generator.html", "How Much Does It Cost to Build a Magnetic Generator?"),
    ("magnetic-generator-for-beginners-step-by-step.html", "Magnetic Generator for Beginners — Step by Step"),
    ("magnetic-generator-for-emergency-backup.html", "Magnetic Generator for Emergency Backup"),
    ("magnetic-generator-for-rv-complete-off-grid-guide.html", "Magnetic Generator for RV — Complete Off Grid Guide"),
    ("magnetic-generator-plans-review.html", "Best Magnetic Generator Plans Review 2026"),
    ("tesla-magnetic-generator-cost-savings-per-month.html", "Tesla Magnetic Generator Cost Savings Per Month"),
    ("tesla-magnetic-generator-for-cabin.html", "Tesla Magnetic Generator for Cabin"),
    ("tesla-magnetic-generator-materials-list-cost.html", "Tesla Magnetic Generator Materials List Cost"),
    ("tesla-magnetic-generator-vs-solar-power-which-is-better.html", "Tesla Magnetic Generator vs Solar Power — Which Is Better"),
    ("tesla-magnetic-generator-worth-it.html", "Is a Tesla Magnetic Generator Worth It? An Honest 2026 Review"),
]

def update_sitemap():
    """Add Phase 1 articles to sitemap.xml."""
    sitemap_path = WEBSITE / "sitemap.xml"
    with open(sitemap_path, 'r') as f:
        content = f.read()
    
    # Find all existing URLs in sitemap
    existing_urls = set(re.findall(r'<loc>(.*?)</loc>', content))
    
    # Build new URL entries
    new_entries = []
    for filename, title in PHASE1_ARTICLES:
        url = f"{SITE_URL}/{filename}"
        if url not in existing_urls:
            new_entries.append(f"""
  <url>
    <loc>{url}</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
    
    if new_entries:
        # Insert before the closing </urlset>
        insert_point = content.rfind('  </urlset>')
        if insert_point > 0:
            new_content = content[:insert_point] + ''.join(new_entries) + content[insert_point:]
            with open(sitemap_path, 'w') as f:
                f.write(new_content)
            print(f"  ✅ Added {len(new_entries)} entries to sitemap.xml")
        else:
            print("  ⚠️  Could not find insertion point in sitemap")
    else:
        print("  ℹ️  All articles already in sitemap")

def add_to_nav():
    """Add Phase 1 articles to the 'Pages' dropdown in all HTML files."""
    # Build the dropdown items
    nav_items = []
    for filename, title in PHASE1_ARTICLES:
        nav_items.append(f'                                <li><a class="dropdown-item" href="{filename}">{title}</a></li>')
    
    new_nav_block = '\n'.join(nav_items)
    
    updated_count = 0
    for html_file in WEBSITE.glob("*.html"):
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Check if this file has the Pages dropdown
        if 'Pages' not in content or 'dropdown-menu' not in content:
            continue
        
        # Check if any Phase 1 article is already in this file's nav
        has_any = any(f'href="{fn}"' in content for fn, _ in PHASE1_ARTICLES)
        if has_any:
            continue
        
        # Find the dropdown-menu closing tag and insert before it
        # We want to add items to the existing dropdown
        dropdown_match = re.search(r'(<!-- Pages dropdown -->)?\s*<ul class="dropdown-menu">\s*(.*?)(\s*</ul>)', content, re.DOTALL)
        if dropdown_match:
            # Insert at the beginning of the dropdown items
            before_items = dropdown_match.group(2)
            after_items = dropdown_match.group(3)
            new_items = new_nav_block + '\n' + before_items
            new_content = content.replace(before_items + after_items, new_items + after_items)
            with open(html_file, 'w') as f:
                f.write(new_content)
            updated_count += 1
        else:
            # Try alternate pattern — insert right before </ul> of dropdown-menu
            # Find the dropdown <ul> and its closing </ul>
            pattern = r'(Pages.*?<ul class="dropdown-menu">)(.*?)(</ul>)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                before_items = match.group(2)
                after_items = match.group(3)
                new_items = new_nav_block + '\n' + before_items
                new_content = content.replace(before_items + after_items, new_items + after_items)
                with open(html_file, 'w') as f:
                    f.write(new_content)
                updated_count += 1
    
    print(f"  ✅ Updated navigation in {updated_count} HTML files")

def update_popular_pages():
    """Add Phase 1 articles to the 'Popular Pages' sidebar widget."""
    for html_file in WEBSITE.glob("*.html"):
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Skip if no Popular Pages widget
        if 'Popular Pages' not in content:
            continue
        
        # Check if any Phase 1 article is already in this file's popular pages
        has_any = any(f'href="{fn}"' in content for fn, _ in PHASE1_ARTICLES)
        if has_any:
            continue
        
        # Add first 3 Phase 1 articles to the popular pages list
        new_items = ""
        for filename, title in PHASE1_ARTICLES[:3]:
            new_items += f'''
                            <li class="pt-2">
                                <a href="{filename}" class="d-flex align-items-center text-dark link-underline link-underline-opacity-0 link-underline-opacity-100-hover">
                                    <span class="text-dark">{title}</span>
                                </a>
                            </li>'''
        
        # Insert after the first existing list item in Popular Pages
        pattern = r'(Popular Pages.*?<ul class="list-unstyled mb-0">)(.*?)('
        match = re.search(pattern, content, re.DOTALL)
        if match:
            before_items = match.group(2)
            new_content = content.replace(before_items, new_items + '\n' + before_items)
            with open(html_file, 'w') as f:
                f.write(new_content)

def main():
    print("=== Updating sitemap ===")
    update_sitemap()
    
    print("\n=== Updating navigation ===")
    add_to_nav()
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
