#!/usr/bin/env python3
"""
Convert article.md files to fully-formatted HTML pages.
Uses whole-house.html as the template structure.
"""

import json
import re
from pathlib import Path

SITE_URL = "https://teslamagneticgenerator.com"
BASE = Path(__file__).parent

# Read the template
with open(Path(__file__).parent.parent.parent / "website" / "whole-house.html", "r") as f:
    TEMPLATE = f.read()

def extract_title(markdown):
    """Extract the H1 title from markdown."""
    m = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    return m.group(1).strip() if m else "Tesla Magnetic Generator Article"

def extract_description(markdown, title):
    """Generate a meta description from the first paragraph or title."""
    # Get first paragraph after the title
    lines = markdown.split('\n')
    in_content = False
    sentences = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            in_content = True
            continue
        if in_content and stripped and not stripped.startswith('#') and not stripped.startswith('---'):
            # Remove markdown formatting for description
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
            clean = re.sub(r'!\[.*?\]\(.*?\)', '', clean)
            clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
            clean = clean.replace('|', ' ').strip()
            if clean:
                sentences.append(clean)
    
    desc = ' '.join(sentences[:3])
    if len(desc) > 160:
        desc = desc[:157] + '...'
    return desc

def extract_keywords(title, markdown):
    """Generate keyword list from title and content."""
    base_keywords = "Tesla magnetic generator, DIY magnetic generator, free energy generator, off grid electricity"
    # Add specific keywords from title
    specific = re.sub(r'^#\s+', '', title)
    specific = re.sub(r'[?\.!,]', '', specific)
    return f"{base_keywords}, {specific}"

def markdown_to_html(md):
    """Convert markdown to HTML with proper heading hierarchy."""
    lines = md.split('\n')
    html_parts = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # H1 — skip it, already rendered in the page header
        if re.match(r'^#\s+', line):
            i += 1
            continue
        
        # H2
        elif re.match(r'^##\s+', line):
            text = re.sub(r'^##\s+', '', line)
            text = clean_markdown(text)
            html_parts.append(f'<h2 class="fw-bolder mt-5">{text}</h2>')
            i += 1
            continue
        
        # H3
        elif re.match(r'^###\s+', line):
            text = re.sub(r'^###\s+', '', line)
            text = clean_markdown(text)
            html_parts.append(f'<h3 class="fw-bolder mt-4">{text}</h3>')
            i += 1
            continue
        
        # H4
        elif re.match(r'^####\s+', line):
            text = re.sub(r'^####\s+', '', line)
            text = clean_markdown(text)
            html_parts.append(f'<h4 class="fw-bolder mt-4">{text}</h4>')
            i += 1
            continue
        
        # Tables — detect header row by looking ahead for separator
        elif re.match(r'^\|.*\|', line):
            cells = [clean_markdown(c.strip()) for c in line.split('|')[1:-1]]
            if not any(cells):
                i += 1
                continue
            
            # Look ahead for separator row
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            
            is_header = j < len(lines) and re.match(r'^\|[\s\-:]+\|', lines[j])
            
            html_parts.append('<div class="table-responsive mb-4"><table class="table table-striped table-bordered">')
            if is_header:
                html_parts.append('<thead><tr>')
                for cell in cells:
                    html_parts.append(f'<th scope="col">{cell}</th>')
                html_parts.append('</tr></thead><tbody>')
                # Read remaining rows starting after separator
                i = j + 1
            else:
                html_parts.append('<tbody>')
                # This row is data
                html_parts.append('<tr>')
                for cell in cells:
                    html_parts.append(f'<td>{cell}</td>')
                html_parts.append('</tr>')
                i = i + 1
            
            # Read remaining table rows
            while i < len(lines):
                row_line = lines[i]
                if re.match(r'^\|.*\|', row_line) and not re.match(r'^\|[\s\-:]+\|', row_line):
                    cells = [clean_markdown(c.strip()) for c in row_line.split('|')[1:-1]]
                    if any(cells):
                        html_parts.append('<tr>')
                        for cell in cells:
                            html_parts.append(f'<td>{cell}</td>')
                        html_parts.append('</tr>')
                    i += 1
                else:
                    break
            html_parts.append('</tbody></table></div>')
            continue
        
        # Unordered lists
        elif re.match(r'^[-*]\s+', line):
            html_parts.append('<ul class="mb-4">')
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i]):
                item = re.sub(r'^[-*]\s+', '', lines[i])
                item = clean_markdown(item)
                html_parts.append(f'<li>{item}</li>')
                i += 1
            html_parts.append('</ul>')
            continue
        
        # Ordered lists
        elif re.match(r'^\d+\.\s+', line):
            html_parts.append('<ol class="mb-4">')
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                item = re.sub(r'^\d+\.\s+', '', lines[i])
                item = clean_markdown(item)
                html_parts.append(f'<li>{item}</li>')
                i += 1
            html_parts.append('</ol>')
            continue
        
        # Horizontal rule
        elif re.match(r'^-{3,}$', line.strip()):
            html_parts.append('<hr class="my-4">')
            i += 1
            continue
        
        # Bold standalone text (like "Winner: ..." or "Yes, if you want:")
        elif re.match(r'^\*\*[^*]+\*\*', line) and not line.startswith('##'):
            text = clean_markdown(line)
            html_parts.append(f'<p class="fw-bold fs-5 mb-3">{text}</p>')
            i += 1
            continue
        
        # Regular paragraph
        else:
            text = clean_markdown(line)
            if text.strip():
                html_parts.append(f'<p class="fs-5 mb-4">{text}</p>')
            i += 1
    
    return '\n'.join(html_parts)

def clean_markdown(text):
    """Remove markdown formatting from text."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" class="img-fluid rounded" loading="lazy">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" rel="noopener">\1</a>', text)
    return text

def build_sidebar(phase_name):
    """Build the sidebar with popular articles from the same phase."""
    phase_dir = BASE / phase_name
    articles = []
    if phase_dir.exists():
        for d in phase_dir.iterdir():
            if d.is_dir():
                md_file = d / "article.md"
                if md_file.exists():
                    with open(md_file, 'r') as f:
                        title = extract_title(f.read())
                    slug = d.name
                    html_name = f"{slug}.html"
                    articles.append((html_name, title, slug))
    
    # Sort by title
    articles.sort(key=lambda x: x[1])
    
    sidebar_items = ""
    for html_name, title, slug in articles[:5]:
        sidebar_items += f'''
                            <li class="pt-2">
                                <a href="{html_name}" class="d-flex align-items-center text-dark link-underline link-underline-opacity-0 link-underline-opacity-100-hover">
                                    <span class="text-dark">{title}</span>
                                </a>
                            </li>'''
    
    return sidebar_items

def build_phase_nav(phase_name):
    """Build navigation links for related phase articles."""
    phase_dir = BASE / phase_name
    links = ""
    if phase_dir.exists():
        for d in phase_dir.iterdir():
            if d.is_dir():
                slug = d.name
                html_name = f"{slug}.html"
                links += f'                                <li><a class="dropdown-item" href="{html_name}">{slug.replace("-", " ").title()}</a></li>\n'
    return links

def convert_article(folder_path, phase_name, phase_dir):
    """Convert a single article.md to HTML."""
    md_file = folder_path / "article.md"
    if not md_file.exists():
        print(f"  ⚠️  No article.md in {folder_path.name}")
        return
    
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    title = extract_title(md_content)
    description = extract_description(md_content, title)
    keywords = extract_keywords(title, md_content)
    slug = folder_path.name
    slug = slug.replace('-2026', '')  # Keep evergreen
    html_filename = f"{slug}.html"
    
    # Convert markdown to HTML
    body_html = markdown_to_html(md_content)
    
    # Build the full page
    page = TEMPLATE.replace(
        '<title>Build a Magnetic Generator to Power Your Whole Home</title>',
        f'<title>{title}</title>'
    )
    
    # SEO description
    page = page.replace(
        'meta name="description" content="Can a magnetic generator power an entire house? I\'ve seen it done, here\'s how DIY builders are going off-grid with Tesla plans."/>',
        f'meta name="description" content="{description}"/>'
    )
    
    # Keywords
    page = page.replace(
        'meta name="keywords" content="build a magnetic generator to power your home, DIY magnetic generator, off grid electricity, Tesla magnetic generator, free energy generator, generate electricity with magnets, power your house off grid" />',
        f'meta name="keywords" content="{keywords}" />'
    )
    
    # OG title
    page = page.replace(
        'meta property="og:title" content="Build a Magnetic Generator to Power Your Whole Home" />',
        f'meta property="og:title" content="{title}" />'
    )
    
    # OG description
    page = page.replace(
        'meta property="og:description" content="Can you really build a magnetic generator to power your whole house? Discover how people are going completely off grid using DIY Tesla magnetic generators and step-by-step blueprints." />',
        f'meta property="og:description" content="{description}" />'
    )
    
    # Twitter title
    page = page.replace(
        'meta name="twitter:title" content="Build a Magnetic Generator to Power Your Whole Home" />',
        f'meta name="twitter:title" content="{title}" />'
    )
    
    # Twitter description
    page = page.replace(
        'meta name="twitter:description" content="Can you really build a magnetic generator to power your whole house? Discover how people are going completely off grid using DIY Tesla magnetic generators and step-by-step blueprints." />',
        f'meta name="twitter:description" content="{description}" />'
    )
    
    # Canonical URL
    page = page.replace(
        'canonical',
        f'canonical'
    )
    page = page.replace(
        'href="https://teslamagneticgenerator.com/whole-house.html"',
        f'href="{SITE_URL}/{html_filename}"'
    )
    
    # OG URL
    page = page.replace(
        'og:url" content="https://teslamagneticgenerator.com/whole-house.html" />',
        f'og:url" content="{SITE_URL}/{html_filename}" />'
    )
    
    # Schema headline
    page = page.replace(
        '"headline": "Can You Really Power Your Home With a Magnetic Generator?"',
        f'"headline": "{title}"'
    )
    
    # Schema description
    page = page.replace(
        '"description": "Can you really build a magnetic generator to power your whole house? Discover how people are going completely off grid using DIY Tesla magnetic generators and step-by-step blueprints."',
        f'"description": "{description}"'
    )
    
    # Schema URL
    page = page.replace(
        '"url": "https://teslamagneticgenerator.com/whole-house.html"',
        f'"url": "{SITE_URL}/{html_filename}"'
    )
    
    # Schema mainEntity
    page = page.replace(
        '"mainEntityOfPage": "https://teslamagneticgenerator.com/whole-house.html"',
        f'"mainEntityOfPage": "{SITE_URL}/{html_filename}"'
    )
    
    # Breadcrumb URL
    page = page.replace(
        '"item": "https://teslamagneticgenerator.com/whole-house.html"',
        f'"item": "{SITE_URL}/{html_filename}"'
    )
    
    # H1 title
    page = page.replace(
        '<h1 class="fw-bolder">Can You Really Power Your Home With a Magnetic Generator?</h1>',
        f'<h1 class="fw-bolder">{title}</h1>'
    )
    
    # Post content - replace the existing content section
    # Find the section class="mb-5" and replace its content
    section_match = re.search(r'(<!-- Post header-->.*?</header>)(.*?)(<section class="mb-5">.*?</section>)', page, re.DOTALL)
    if section_match:
        header = section_match.group(1)
        old_section = section_match.group(3)
        
        # Build new section with converted content
        new_section = f'<section class="mb-5">\n{body_html}\n</section>'
        
        page = page.replace(old_section, new_section)
    
    # Write output at phase level
    output_path = phase_dir / html_filename
    with open(output_path, 'w') as f:
        f.write(page)
    
    print(f"  ✅ {html_filename}")

def main():
    phases = [
        "phase-1-foundation",
        "phase-2-home-applications", 
        "phase-3-off-grid-mobile",
        "phase-4-technical-authority",
        "phase-5-niche-applications",
    ]
    
    for phase_name in phases:
        phase_dir = BASE / phase_name
        if not phase_dir.exists():
            print(f"⏳ Skipping {phase_name} (not found)")
            continue
        
        print(f"\n=== {phase_name} ===")
        for folder in sorted(phase_dir.iterdir()):
            if folder.is_dir():
                convert_article(folder, phase_name, phase_dir)
    
    print("\n✅ Conversion complete!")

if __name__ == "__main__":
    main()
