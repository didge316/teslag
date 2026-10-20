#!/usr/bin/env python3
"""Build a series page by cloning the donor shell and injecting a markdown draft.

SERIES-PLAN-1894.md §7. Clone, do not rewrite: the navbar, sidebar, scarcity
widget, footer and scripts are lifted verbatim from the donor page; only <head>
metadata, JSON-LD and the <article> body are generated.

    python3 books/tools/make_article.py \
      --md new_content/1894-series/03-tesla-earthquake-machine/article.md \
      --donor website/nikola-tesla-inventor-extraordinaire.html \
      --out website/tesla-earthquake-machine.html \
      --tid 1894_03 --wire

Markdown dialect (deliberately tiny, §7): ##/###, **bold**, *em*, > quote,
- list, ![alt](src "caption"), [text](page.html), {{CTA}}, {{SOURCES}}, {{FAQ}}.
A data page also needs two things the argument pages did not: a fenced code
block (``` ... ```, emitted verbatim and escaped, for the command a reader is
meant to run), a pipe table (| ... | with a |---| row, emitted as the same
Bootstrap table the older pages on this site use) and code spans (`term`, for
the strings a reader is being asked to search for). All three are here because
the word-search page needs them and the alternative was hand-written HTML in a
draft, which is the thing §7's tiny dialect exists to prevent.

Series rules enforced here rather than left to the writer: no comments block, no
css/comments.css, affiliate links carry ?tid= and nofollow, every <img> gets
alt/width/height/loading="lazy", figures wrapped in <figure class="mb-4 pt-5">.
"""

import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path

import yaml

SITE = "https://teslamagneticgenerator.com"
AUTHOR = "Jake Mercer"
PUBLISHER = "Tesla Magnetic Generator"
CB = "https://d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net/"
BOOK = {
    "@type": "Book",
    "name": "The Inventions, Researches and Writings of Nikola Tesla",
    "editor": {"@type": "Person", "name": "Thomas Commerford Martin"},
    "publisher": {"@type": "Organization", "name": "D. Van Nostrand"},
    "datePublished": "1894",
    "url": "https://archive.org/details/inventionsresear00martiala",
}
BOOK_CITE_HTML = ("<em>The Inventions, Researches and Writings of Nikola Tesla</em>, "
                  "ed. Thomas Commerford Martin. New York: D. Van Nostrand, 1894 "
                  "(entered 1893). Scan: archive.org item "
                  "<a href=\"https://archive.org/details/inventionsresear00martiala\" "
                  "target=\"_blank\" rel=\"noopener noreferrer nofollow\">"
                  "inventionsresear00martiala</a>. Public domain.")
KICKER = ("The 1894 File · No. {no} of 12. Every quote below is cited from the "
          "first edition, page numbers included.")
DISCLOSURE = ("We earn a commission if you buy through that link. It does not "
              "change what the 1894 book says.")

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent.parent                     # tesla-generator/
WEB = ROOT / "website"
SERIES = ROOT / "new_content" / "1894-series"


# ------------------------------------------------------------------- urls
# The site's URL contract (SEO-URL-FIX-PLAN.md §1): a page is addressed at
# /<name> with no extension; the .html file is where it is stored, not what it is
# called. index.html is the site root. Everything below goes through these two
# helpers so no emitter can reintroduce the old form.

def page_url(slug):
    """Absolute canonical URL for a site page file name."""
    s = str(slug).strip().strip("/")
    if s in ("", "index", "index.html"):
        return SITE + "/"
    if s.endswith(".html"):
        s = s[:-5]
    return f"{SITE}/{s}"


def page_href(slug):
    """The same URL as a root-absolute link for use inside HTML.

    Root-absolute, not relative: a page reached at a trailing-slash base resolves a
    relative href against that base, and that is how a stylesheet link becomes a 404.
    """
    return "/" + page_url(slug)[len(SITE):].lstrip("/")


def local_href(href):
    """Normalise a link written in markdown to the site's URL form."""
    if href.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:", "//")):
        return href
    return page_href(href)


def redirect_rules(pretty, slug):
    """The _redirects lines for one page, or [] when such a rule would be dead.

    Cloudflare resolves a static page before it consults _redirects, so a rule whose
    source is an existing page never fires - and it blocks the platform's own
    trailing-slash normalisation. That is how 8 dead rules got written (§2.2). A rule
    is wanted only when the URL deliberately differs from the file name, so
    pretty_slug must be set for an alias, never to restate the file name.
    """
    src = str(pretty or "").strip()
    if not src:
        return []
    if not src.startswith("/"):
        src = "/" + src
    target = page_href(slug)
    if src.strip("/") == target.strip("/"):
        return []
    return [f"{s}    {target} 301" for s in (src, src.rstrip("/") + "/")]



# ------------------------------------------------------------- front matter

def split_front_matter(text):
    if not text.startswith("---"):
        sys.exit("article.md must start with YAML front matter (---)")
    end = text.index("\n---", 3)
    return yaml.safe_load(text[3:end]), text[end + 4:].lstrip("\n")


def is_hub(fm):
    return str(fm.get("series_no", "")).lower() in ("0", "00", "h", "hub")


# a pipe table's second line: |---|:---:| (the renderer has no other table form)
_SEP_ROW = re.compile(r"^\|[:\- ]+\|[|:\- ]*$")


# ----------------------------------------------------------------- markdown

def img_tag(src, alt, caption, figmap, base_dir):
    meta = figmap.get(src, {})
    w, h = meta.get("width"), meta.get("height")
    if not w or not h:
        w, h = real_dims(src, base_dir)
    alt = alt or meta.get("alt", "")
    if not alt:
        sys.exit(f"figure {src}: alt text is required (§4.2)")
    if not w or not h:
        sys.exit(f"figure {src}: no pixel dimensions and file not found (§6.6)")
    return (f'<img loading="lazy" class="img-fluid rounded" src="{src}" '
            f'alt="{alt}" width="{w}" height="{h}"/>')


def real_dims(src, base_dir):
    for cand in (WEB / src.lstrip("/"), base_dir / src):
        if cand.exists():
            try:
                from PIL import Image
                with Image.open(cand) as im:
                    return im.width, im.height
            except Exception:
                return None, None
    return None, None


def inline(s, figmap, base_dir):
    # code spans first, so a * or ** inside a term name is not eaten by the
    # emphasis rules below. check_quotes.py blanks the same spans when it reads a
    # draft, so a term written in backticks is never mistaken for a quote.
    s = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)

    def img(m):
        return img_tag(m.group(2), m.group(1), (m.group(3) or "").strip(),
                       figmap, base_dir)
    s = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', img, s)

    def link(m):
        txt, href = m.group(1), m.group(2)
        if href.startswith("http"):
            return (f'<a href="{href}" target="_blank" '
                    f'rel="noopener noreferrer nofollow">{txt}</a>')
        return f'<a href="{local_href(href)}">{txt}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)


def md_to_html(md, fm, base_dir):
    figmap = {f["src"]: f for f in fm.get("figures", [])}
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
        elif s.startswith("### "):
            out.append(f'<h3 class="fw-bolder mb-2 pt-4">'
                       f'{inline(s[4:], figmap, base_dir)}</h3>')
            i += 1
        elif s.startswith("## "):
            out.append(f'<h2 class="fw-bolder mb-1 pt-5">'
                       f'{inline(s[3:], figmap, base_dir)}</h2>')
            i += 1
        elif s.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip())
                i += 1
            i += 1                                   # the closing fence
            out.append('<pre class="bg-light p-3 mb-4 fs-6"><code>'
                       + html.escape("\n".join(buf)) + "</code></pre>")
        elif s.startswith("|") and i + 1 < len(lines) and _SEP_ROW.match(lines[i + 1].strip()):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip().strip("|")
                rows.append([c.strip() for c in row.split("|")])
                i += 1
            head, body = rows[0], rows[2:]     # rows[1] is the --- separator
            thead = "".join(f"<th scope=\"col\">{inline(c, figmap, base_dir)}</th>"
                            for c in head)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{inline(c, figmap, base_dir)}</td>" for c in r)
                + "</tr>" for r in body)
            out.append('<div class="table-responsive mb-4">'
                       '<table class="table table-striped table-bordered">'
                       f'<thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody>'
                       "</table></div>")
        elif s.startswith("{{") and s.endswith("}}"):
            out.append(s)                       # resolved after, keeps order
            i += 1
        elif s.startswith("!["):
            m = re.match(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', s)
            if not m:
                out.append(f'<p class="fs-5 mb-4">{inline(s, figmap, base_dir)}</p>')
                i += 1
                continue
            alt, src, cap = m.group(1), m.group(2), (m.group(3) or "").strip()
            cap = cap or figmap.get(src, {}).get("caption", "")
            tag = img_tag(src, alt, cap, figmap, base_dir)
            caphtml = (f'<figcaption class="figure-caption">'
                       f'{inline(cap, figmap, base_dir)}</figcaption>') if cap else ""
            out.append(f'<figure class="mb-4 pt-5">{tag}{caphtml}</figure>')
            i += 1
        elif s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append('<blockquote class="mb-4"><p class="fs-5 fst-italic mb-0">'
                       f'{inline(" ".join(buf), figmap, base_dir)}</p></blockquote>')
        elif s.startswith(("- ", "* ")):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                buf.append(lines[i].strip()[2:])
                i += 1
            items = "".join(f"<li>{inline(b, figmap, base_dir)}</li>" for b in buf)
            out.append(f'<ul class="mb-4 fs-5">{items}</ul>')
        elif re.match(r"^1[.)]\s+\S", s):
            # Ordered lists, added 2026-10-20 because the hub's twelve-article
            # index was being rendered as one run-on paragraph: the tool had no
            # ordered-list branch, so "1. ... 2. ..." fell into the paragraph
            # branch and swallowed the whole list (found by looking at the page,
            # books/tmp/review/tesla-1894-desktop-boxes-3of7.png).
            # The first marker must be 1, as in CommonMark: that is what keeps a
            # paragraph that opens "1892. Three of the four passages..." a
            # paragraph. Later markers may be any number.
            buf = [s[2:].strip()]
            while (i + 1 < len(lines) and
                   re.match(r"^\s*\d+[.)]\s+\S", lines[i + 1].strip())):
                i += 1
                buf.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i].strip()))
            items = "".join(f"<li>{inline(b, figmap, base_dir)}</li>" for b in buf)
            out.append(f'<ol class="mb-4 fs-5">{items}</ol>')
            i += 1        # the look-ahead loop above stops *on* the last item
        else:
            buf = [s]
            while i + 1 < len(lines) and lines[i + 1].strip() and \
                    not re.match(r"^\s*(#|>|[-*]\s|1[.)]\s|!\[|\{|\||`)", lines[i + 1]):
                i += 1
                buf.append(lines[i].strip())
            out.append(f'<p class="fs-5 mb-4">{inline(" ".join(buf), figmap, base_dir)}</p>')
            i += 1
    return "\n".join(out)


# -------------------------------------------------------------- donor shell

def slice_between(d, start_marker, end_marker, name):
    a = d.find(start_marker)
    b = d.find(end_marker, a)
    if a < 0 or b < 0:
        sys.exit(f"donor shell: cannot find {name} ({start_marker!r} .. {end_marker!r})")
    return d[a:b]


def load_shell(donor_path):
    d = Path(donor_path).read_text(encoding="utf-8")
    shell = {
        "nav": slice_between(d, '<nav class="navbar', "</nav>", "navbar") + "</nav>",
        "container_open": slice_between(d, "<!-- Page content-->",
                                        '<div class="col-lg-8">', "container open"),
        "sidebar": slice_between(d, "<!-- Side widgets -->", "<footer", "sidebar"),
        "footer": slice_between(d, "<footer", "</body>", "footer + scripts"),
    }
    sc = slice_between(d, "<!-- Status Checker (scarcity widget) -->",
                       "<!-- Side widgets -->", "scarcity widget").rstrip()
    k = sc.rfind("</div>")      # the last one closes col-lg-8; we close it ourselves
    shell["scarcity"] = sc[:k].rstrip()
    _trim_stray_divs(shell)
    return shell


def _trim_stray_divs(shell):
    """The legacy pages carry stray closing </div>s (donor: 54 open / 58 close).

    Browsers ignore them, but a series page should not ship malformed, and §12
    asserts balance. Strip the surplus from the tail of the sidebar fragment.
    """
    blob = "".join(shell.values())
    surplus = blob.count("</div>") - blob.count("<div")
    if surplus <= 0:
        return
    tail = shell["sidebar"]
    for _ in range(surplus):
        k = tail.rfind("</div>")
        if k < 0:
            break
        tail = tail[:k] + tail[k + len("</div>"):]
    shell["sidebar"] = tail.rstrip()


def add_nav_entry(nav, slug, title):
    href = page_href(slug)
    if f'href="{href}"' in nav:
        return nav
    marker = '<ul class="dropdown-menu">'
    k = nav.find(marker)
    if k < 0:
        return nav
    entry = ('\n                                <li><a class="dropdown-item" '
             f'href="{href}">{title}</a></li>')
    return nav[:k + len(marker)] + entry + nav[k + len(marker):]


# ------------------------------------------------------------------ assembly

def fmt_date(d):
    try:
        return datetime.date.fromisoformat(str(d)).strftime("%B %d, %Y").replace(" 0", " ")
    except Exception:
        return str(d)


def build_head(fm, slug):
    url = page_url(slug)
    title, desc = fm["title"], fm["description"]
    og = fm.get("og_image", "") or ""
    og_url = og if og.startswith("http") else (f"{SITE}/{og.lstrip('/')}" if og else "")
    kw = ", ".join(fm.get("keywords", []))
    pub = fm.get("date_published", "")
    mod = fm.get("date_modified", pub)
    return f"""    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    <!-- SEO meta tags -->
    <title>{title}</title>
    <meta name="author" content="{AUTHOR}" />
    <meta name="keywords" content="{kw}">
    <meta name="robots" content="index, follow" />
    <meta name="description" content="{desc}"/>

    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{og_url}" />
    <meta property="article:published_time" content="{pub}" />
    <meta property="article:modified_time" content="{mod}" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{og_url}" />

    <!-- Canonical URL -->
    <link rel="canonical" href="{url}" />

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico" />

    <!-- CSS -->
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous" /><link href="/css/styles-custom.css" rel="stylesheet" />
"""


def build_jsonld(fm, slug):
    url = page_url(slug)
    art = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": fm["title"],
        "description": fm["description"],
        "url": url,
        "datePublished": fm.get("date_published"),
        "dateModified": fm.get("date_modified", fm.get("date_published")),
        "author": {"@type": "Person", "name": AUTHOR, "url": page_url("about.html")},
        "publisher": {"@type": "Organization", "name": PUBLISHER, "url": SITE + "/"},
        "mainEntityOfPage": url,
        "about": {"@type": "Thing", "name": "Nikola Tesla"},
        # `citation:` in front matter for a page whose source is not the 1894 book.
        # The 1919 magazine page is the one case: naming the 1894 volume as its
        # citation would be a schema lie, and the default keeps all 15 series pages
        # byte-identical.
        "citation": fm.get("citation") or dict(BOOK),
    }
    blocks = [art]
    if is_hub(fm):
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": fm["title"], "item": url}]
    else:
        parent = fm.get("breadcrumb_parent") or {
            "name": "The 1894 File", "item": page_url("tesla-1894.html")}
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": parent["name"],
                   "item": parent["item"]},
                  {"@type": "ListItem", "position": 3, "name": fm["title"], "item": url}]
    blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                   "itemListElement": crumbs})
    if fm.get("faq"):
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q["q"],
                                       "acceptedAnswer": {"@type": "Answer",
                                                          "text": q["a"]}}
                                      for q in fm["faq"]]})
    if is_hub(fm) and fm.get("series_items"):
        blocks.append({"@context": "https://schema.org", "@type": "ItemList",
                       "name": "The 1894 File",
                       "numberOfItems": len(fm["series_items"]),
                       "itemListElement": [{"@type": "ListItem", "position": n + 1,
                                           "url": page_url(it["file"])}
                                           for n, it in enumerate(fm["series_items"])]})
    return "\n".join('    <script type="application/ld+json">\n'
                     + json.dumps(b, indent=2).replace("\n", "\n    ")
                     + "\n    </script>" for b in blocks)


def cta_block(fm, tid):
    c = fm.get("cta", {}) or {}
    href = f"{CB}?tid={c.get('href_suffix', tid)}"
    return ('<div class="alert alert-info mb-4" role="alert">'
            f'<p class="mb-2">{c.get("text", "")}</p>'
            '<p class="mb-2"><a href="' + href + '" target="_blank" '
            'rel="noopener noreferrer nofollow" class="alert-link">'
            'See the generator plans</a></p>'
            f'<p class="mb-0 small text-muted">'
            f'{fm.get("disclosure", DISCLOSURE)}</p></div>')


def sources_block(fm):
    # `book_cite:` replaces the first Sources line; an empty book_cite: omits it.
    # A page about a different source than the 1894 volume must not open its Sources
    # block with the 1894 volume.
    head = BOOK_CITE_HTML if "book_cite" not in fm else str(fm.get("book_cite") or "")
    lis = ([f"<li>{head}</li>"] if head else [])
    for s in fm.get("sources", []) or []:
        if isinstance(s, dict):
            t = s.get("text", "")
            if s.get("url"):
                t = (f'<a href="{s["url"]}" target="_blank" '
                     f'rel="noopener noreferrer nofollow">{t}</a>')
            lis.append(f"<li>{t}</li>")
        else:
            lis.append(f"<li>{s}</li>")
    pages = fm.get("pages_used") or []
    if pages:
        lis.append("<li>"
                   + str(fm.get("pages_label",
                                "Pages of the 1894 edition used here")) + ": "
                   + ", ".join(f"p. {p}" for p in pages) + "</li>")
    return ('<h2 class="fw-bolder mb-1 pt-5">Sources</h2>\n<ul class="mb-4 fs-5">'
            + "".join(lis) + "</ul>")


def faq_block(fm):
    if not fm.get("faq"):
        return ""
    parts = ['<h2 class="fw-bolder mb-1 pt-5">Frequently asked questions</h2>']
    for q in fm["faq"]:
        parts.append(f'<h3 class="fw-bolder mb-2 pt-3">{q["q"]}</h3>'
                     f'<p class="fs-5 mb-4">{q["a"]}</p>')
    return "\n".join(parts)


def build(fm, body_md, shell, tid, base_dir):
    slug = fm["slug"]
    kicker = str(fm.get("kicker", "")).strip() or \
        ("" if is_hub(fm) else KICKER.format(no=fm.get("series_no")))
    header = [f'<h1 class="fw-bolder mb-1">{fm["title"]}</h1>']
    if kicker:
        header.append(f'<p class="text-muted small mb-2">{kicker}</p>')
    header.append(f'<p class="text-muted small mb-3">Published: '
                  f'{fmt_date(fm.get("date_published"))} &nbsp;|&nbsp; '
                  f'Updated: {fmt_date(fm.get("date_modified", fm.get("date_published")))}</p>')

    body = md_to_html(body_md, fm, base_dir)
    body = (body.replace("{{CTA}}", cta_block(fm, tid))
                .replace("{{SOURCES}}", sources_block(fm))
                .replace("{{FAQ}}", faq_block(fm)))
    article = ('<article>\n                        <section class="mb-5">\n'
               + "\n".join(header) + "\n" + body + "\n                        </section>\n"
               + "                    </article>")

    nav = add_nav_entry(shell["nav"], slug, fm["title"]) if fm.get("nav") else shell["nav"]
    scarcity = shell["scarcity"] if fm.get("scarcity", True) else ""

    return ('<!DOCTYPE html>\n<html lang="en">\n    <head>\n'
            + build_head(fm, slug) + build_jsonld(fm, slug) + "\n</head>\n    <body>\n\n"
            + "        <!-- Responsive navbar -->\n        " + nav + "\n"
            + "        " + shell["container_open"]
            + '            <div class="col-lg-8">\n                    <!-- Post content-->\n'
            + "                    " + article + "\n\n"
            + ("                    " + scarcity + "\n" if scarcity else "")
            + "                </div>\n            " + shell["sidebar"] + "\n"
            + shell["footer"] + "\n    </body>\n</html>\n")


# --------------------------------------------------------------------- wire

def wire_updates(fm, slug, include_card=True):
    """§7: articles.html card, nav dropdown, sitemap.xml, _redirects, llms.txt.

    include_card=False is for the asset pages (plates, word search, Part I text):
    the draft for the plates page says so itself - "the asset pages are not in
    the articles.html grid" - so they get the sitemap, the alias and llms.txt,
    and not a card in the article list.
    """
    changed, notes = [], []
    url = page_url(slug)
    href = page_href(slug)

    rules = redirect_rules(fm.get("pretty_slug"), slug)
    if fm.get("pretty_slug") and not rules:
        notes.append("_redirects: skipped - pretty_slug equals the page's own URL, so a "
                     "rule here would never fire and would block trailing-slash "
                     "normalisation (see SEO-URL-FIX-PLAN.md §1.4)")
    p = WEB / "_redirects"
    for rule in rules:
        lines = p.read_text().splitlines()
        src = rule.split()[0]
        if any(l.split()[0] == src for l in lines if l.strip() and not l.startswith("#")):
            notes.append(f"_redirects: {src} already present")
            continue
        p.write_text("\n".join(lines).rstrip("\n") + "\n" + rule + "\n")
        if "_redirects" not in changed:
            changed.append("_redirects")

    sm = WEB / "sitemap.xml"
    txt = sm.read_text()
    if url not in txt:
        entry = (f'\n  <url>\n    <loc>{url}</loc>\n'
                 f'    <lastmod>{fm.get("date_modified", fm.get("date_published"))}</lastmod>\n'
                 f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
        k = txt.rfind("</urlset>")
        sm.write_text(txt[:k] + entry + txt[k:])
        changed.append("sitemap.xml")
    else:
        notes.append("sitemap.xml: already listed")

    art = WEB / "articles.html"
    if not include_card:
        notes.append("articles.html: skipped - not an article page, so no card "
                     "(the plates draft states this rule itself)")
    elif f'href="{href}"' not in (html := art.read_text()):
        k = _card_anchor(html)
        if k:
            art.write_text(html[:k] + _article_card(fm, slug) + html[k:])
            changed.append("articles.html")
        else:
            notes.append("articles.html: no card anchor found — add by hand")
    else:
        notes.append("articles.html: card already present")

    ll = WEB / "llms.txt"
    txt = ll.read_text()
    if url not in txt:
        line = (f"- [{fm['title']}]({url}): "
                f"{(fm.get('standfirst') or fm['description'])[:150]}")
        head = "## The 1894 File"
        if head in txt:
            end = txt.find("\n##", txt.index(head) + len(head))
            end = len(txt) if end < 0 else end
            txt = txt[:end].rstrip("\n") + "\n" + line + "\n" + txt[end:]
        else:
            txt = txt.rstrip("\n") + f"\n\n{head}\n\n{line}\n"
        ll.write_text(txt)
        changed.append("llms.txt")
    else:
        notes.append("llms.txt: already listed")

    if fm.get("nav"):
        touched = 0
        for f in sorted(WEB.glob("*.html")):
            h = f.read_text()
            if '<ul class="dropdown-menu">' not in h or f'href="{href}"' in h:
                continue
            f.write_text(add_nav_entry(h, slug, fm["title"]))
            touched += 1
        if touched:
            changed.append(f"nav dropdown in {touched} pages")
    return changed, notes


def _article_card(fm, slug):
    img = fm.get("card_image") or fm.get("og_image") or ""
    src = f"/{img.lstrip('/')}" if img and not img.startswith("http") else img
    pic = (f'<img src="{src}" width="40" height="40" loading="lazy" '
           f'class="rounded me-2 flex-shrink-0" alt="{fm.get("card_alt", fm["title"])}">'
           if src else "")
    return ('                                    <li class="pt-2">\n'
            '                                        <a href="' + page_href(slug) + '" class="d-flex align-items-center text-dark link-underline link-underline-opacity-0 link-underline-opacity-100-hover">'
            + pic + '<span class="text-dark">' + fm["title"] + '</span></a>\n'
            '                                    </li>\n')


def _card_anchor(html):
    """Insert after the last <li> of the first list-unstyled block (the card list)."""
    start = html.find('class="list-unstyled')
    if start < 0:
        return None
    end = html.find("</ul>", start)
    if end < 0:
        return None
    return end


# ----------------------------------------------------------------- self test

FIXTURE = """---
title: "Fixture: Tesla's Earthquake Machine"
slug: _selftest-fixture.html
description: "A fixture description long enough to clear the twelve to one hundred fifty five character QA gate for series pages."
keywords: [tesla earthquake machine, tesla oscillator]
date_published: "2026-10-09"
date_modified: "2026-10-09"
series_no: 3
primary_query: tesla earthquake machine
figures: []
cta: {text: "Fixture CTA sentence.", href_suffix: "1894_03"}
faq: [{q: "Did Tesla build an earthquake machine?", a: "He built a small mechanical oscillator in 1893; the earthquake story came later."}]
sources: [{text: "Carlson 2013", url: "https://example.org"}]
pages_used: [486, 487]
---

Intro paragraph with a **bold** claim and an *emphasis*, cited (1894, p. 486).

## The 1893 account

Second paragraph with enough words to be a paragraph, citing (1894, p. 487).
See [perpetual motion](perpetual-motion-generator.html),
[magnet motor](magnet-motor.html), [plans](magnetic-generator-plans-review.html)
and [the hub](tesla-1894.html).

> a steel arbor which had been actually torn apart while vibrating against a
> minute air cushion (1894, p. 486)

- one point
- another point

## The three things, in order

1. the first thing, cited (1894, p. 486).
2. the second thing.
3. the third zebra thing.

1892. A paragraph that opens with a year must stay a paragraph. CommonMark's own
rule is what decides this: a list only starts at 1.

## What the internet gets wrong

Third paragraph, citing (1894, p. 486) again so the citation gate is exercised.

## Resonance is not over-unity

Fourth paragraph to make the H2 count realistic for a flagship piece (1894, p. 487).

{{FAQ}}

{{CTA}}

{{SOURCES}}
"""


def self_test(donor):
    import html.parser

    tmp = SERIES / "_selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    fm, body = split_front_matter(FIXTURE)
    shell = load_shell(donor)
    out = build(fm, body, shell, "1894_03", tmp)
    (tmp / "fixture.html").write_text(out)

    fails = []

    class Checker(html.parser.HTMLParser):
        VOID = {"img", "br", "meta", "link", "hr", "input", "source"}

        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack, self.bad = [], []

        def handle_starttag(self, tag, attrs):
            if tag not in self.VOID:
                self.stack.append(tag)

        def handle_endtag(self, tag):
            if tag in self.VOID:
                return
            if not self.stack or self.stack[-1] != tag:
                self.bad.append(f"{tag} closes {self.stack[-1] if self.stack else 'nothing'}")
            else:
                self.stack.pop()

    c = Checker()
    c.feed(out)
    if c.bad or c.stack:
        fails.append(f"unbalanced tags: {c.bad[:5]} open={c.stack[:5]}")
    if out.count("<h1") != 1:
        fails.append(f"h1 count = {out.count('<h1')}")
    for m in re.finditer(r"<img\b[^>]*>", out):
        tag = m.group(0)
        for attr in ('alt="', 'width="', 'height="', 'loading="lazy"'):
            if attr not in tag:
                fails.append(f"img missing {attr}: {tag[:80]}")
    for m in re.finditer(r'<script type="application/ld\+json">\n(.*?)\n    </script>',
                         out, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            fails.append(f"JSON-LD does not parse: {e}")
    if not re.search(r'"citation"', out):
        fails.append("Article.citation missing")
    # Content links must come out root-absolute and extensionless. This check used to
    # match href="x.html" only, so against a migrated page it passed on zero links -
    # the same silent-pass failure mode qa_page.py had (SEO-URL-FIX-PLAN.md G2).
    want = {"/perpetual-motion-generator", "/magnet-motor",
            "/magnetic-generator-plans-review", "/tesla-1894"}
    got = set(re.findall(r'href="(/[A-Za-z0-9._\-]+)"', out))
    missing = sorted(want - got)
    if missing:
        fails.append(f"content links not emitted in the canonical form: {missing}")
    if re.search(r'href="[^"]*\.html["\s]', out):
        fails.append("a .html href was emitted")
    if re.search(r'(?:href|src)="(?!https?:|#|/|mailto:|tel:|data:|javascript:)[^"]+"', out):
        fails.append("a relative href/src was emitted")
    can = re.search(r'<link rel="canonical" href="([^"]+)"', out)
    if not can or can.group(1) != page_url(fm["slug"]):
        fails.append(f"canonical is not self-referential and extensionless: "
                     f"{can.group(1) if can else None}")
    if can and can.group(1).endswith(".html"):
        fails.append("canonical carries .html")
    ogu = re.search(r'<meta property="og:url" content="([^"]+)"', out)
    if not ogu or (can and ogu.group(1) != can.group(1)):
        fails.append("og:url does not equal canonical")
    # The dead-rule rule, checked directly: --wire is not run by the self-test, and a
    # rule that restates a page's own URL is what put 8 dead rules in _redirects.
    if redirect_rules("/_selftest-fixture", "_selftest-fixture.html"):
        fails.append("a rule restating the page's own URL was not skipped")
    alias = redirect_rules("/tesla-rotating-magnetic-field",
                           "rotating-magnetic-field-1888.html")
    if len(alias) != 2 or not all(r.endswith(" 301") for r in alias) \
            or not any(r.startswith("/tesla-rotating-magnetic-field/ ") for r in alias):
        fails.append(f"alias rule wrong: {alias}")
    if re.search(r'href="http://', out):
        fails.append("http:// link present")
    if "localhost" in out:
        fails.append("localhost present")
    if "comments.css" in out or "<!-- Comments section-->" in out:
        fails.append("comments block / comments.css present — forbidden (D3)")
    if "?tid=1894_03" not in out:
        fails.append("affiliate tid missing")
    # Ordered lists. Added 2026-10-20: the tool had no ordered-list branch, so the
    # hub's twelve-article index came out as one run-on paragraph, and the first
    # version of the fix duplicated the last item (the look-ahead loop stopped on
    # it instead of past it). Both halves are checked here.
    ol = re.search(r'<ol class="mb-4 fs-5">(.*?)</ol>', out, re.S)
    if not ol:
        fails.append('ordered list did not become <ol class="mb-4 fs-5">')
    else:
        n = len(re.findall(r"<li>", ol.group(1)))
        if n != 3:
            fails.append(f"ordered list has {n} items, expected 3")
        if "third zebra thing" in out[ol.end():]:
            fails.append("the last ordered-list item was emitted twice")
    if '<p class="fs-5 mb-4">1892.' not in out:
        fails.append("a paragraph opening with a year became a list item")
    if 'rel="noopener noreferrer nofollow"' not in out:
        fails.append("affiliate rel missing")
    if len(out.encode()) > 200_000:
        fails.append(f"HTML {len(out.encode())} bytes > 200 KB")
    return fails, out, tmp / "fixture.html"


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--md")
    ap.add_argument("--donor", default=str(WEB / "nikola-tesla-inventor-extraordinaire.html"))
    ap.add_argument("--out")
    ap.add_argument("--tid")
    ap.add_argument("--wire", action="store_true",
                    help="also update sitemap/_redirects/articles.html/llms.txt (+ nav if front matter says nav: true)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an output file not listed in index.json")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        fails, out, path = self_test(args.donor)
        print(f"fixture -> {path}  ({len(out.encode())} bytes)")
        if fails:
            print("SELF-TEST FAILED:")
            for f in fails:
                print("  -", f)
            return 1
        print("self-test: all §7 assertions pass")
        return 0

    if not (args.md and args.out):
        ap.error("--md and --out are required (or --self-test)")

    md_path = Path(args.md)
    fm, body = split_front_matter(md_path.read_text())
    slug = Path(args.out).name
    if fm.get("slug") != slug:
        sys.exit(f"front matter slug {fm.get('slug')!r} != --out {slug!r}")
    tid = args.tid or fm.get("tid") or (
        "1894_hub" if is_hub(fm) else f"1894_{int(fm['series_no']):02d}")
    tid = str(tid)
    if not re.fullmatch(r"1894_(\d{2}|hub)", tid):
        # YAML 1.1 reads an unquoted 1894_03 as the integer 189403.
        sys.exit(f'tid must be quoted in front matter, e.g. tid: "1894_03" '
                 f"(got {tid!r})")

    out_path = Path(args.out)
    if out_path.exists() and not args.force:
        known = []
        if SERIES.joinpath("index.json").exists():
            try:
                known = json.loads(SERIES.joinpath("index.json").read_text())
            except Exception:
                known = []
        slugs = {k.get("slug") for k in known} if isinstance(known, list) else set()
        if slug not in slugs:
            sys.exit(f"refusing to overwrite {out_path} (not in index.json; "
                     f"use --force if this is a deliberate rebuild)")

    shell = load_shell(args.donor)
    html = build(fm, body, shell, tid, md_path.parent)
    before = out_path.read_bytes() if out_path.exists() else b""
    out_path.write_text(html)

    imgs = re.findall(r"<img\b[^>]*>", html)
    figs = [i for i in imgs if 'src="/assets/tesla1894/' in i or 'assets/tesla1894/' in i]
    shell_links = set()
    for v in shell.values():
        shell_links |= set(re.findall(r'href="(/[A-Za-z0-9._\-]+)"', v))
    links = ({u for u in re.findall(r'href="(/[A-Za-z0-9._\-]+)"', html)}
             - shell_links - {page_href(slug)})
    print(f"wrote {out_path}  ({len(before)} -> {len(html.encode())} bytes)")
    print(f"  headings: {html.count('<h1')} h1, {html.count('<h2')} h2, "
          f"{html.count('<h3')} h3")
    print(f"  images: {len(figs)} series figures / {len(imgs)} total")
    print(f"  internal links: {len(links)}")
    if re.search(r'href="[^"]*\.html["\s]', html):
        print("  WARNING: a .html href is present - the page will point at a redirect")
    print(f"  tid: {tid}")
    if args.wire:
        changed, notes = wire_updates(fm, slug)
        print("  wired:", ", ".join(changed) if changed else "(nothing to change)")
        for n in notes:
            print("   note:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
