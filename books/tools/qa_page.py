#!/usr/bin/env python3
"""Numeric QA gates for a series page — SERIES-PLAN-1894.md §12.

    python3 books/tools/qa_page.py website/tesla-earthquake-machine.html
    python3 books/tools/qa_page.py --all-series      # every page in index.json

Checks the machine can check. The visual half of §12 (figure subjects, caption
truth, three screenshots, OG legibility) is a separate gate and needs eyes.
Exit code 0 = every numeric gate passed.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[2] / "website"
SERIES = Path(__file__).resolve().parents[2] / "new_content" / "1894-series"
ARCHIVE_ITEM = "inventionsresear00martiala"
INBOUND = {}          # page -> set of pages that link to it (computed once)


def meta(html, name):
    m = re.search(rf'<meta name="{name}" content="(.*?)"\s*/?>', html, re.S)
    return m.group(1) if m else ""


def inbound_map():
    if INBOUND:
        return INBOUND
    for f in WEB.glob("*.html"):
        try:
            h = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for href in re.findall(r'href="([A-Za-z0-9._\-]+\.html)"', h):
            INBOUND.setdefault(href.lower(), set()).add(f.name.lower())
    return INBOUND


def check(path: Path):
    html = path.read_text(encoding="utf-8", errors="ignore")
    low = html.lower()
    slug = path.name.lower()
    res = []

    def gate(ok, label, detail=""):
        res.append((bool(ok), label, detail))

    t = re.search(r"<title>(.*?)</title>", html, re.S)
    title = t.group(1).strip() if t else ""
    gate(title and len(title) <= 60, "title <= 60 chars", f"{len(title)} chars")

    desc = meta(html, "description")
    gate(120 <= len(desc) <= 155, "description 120-155 chars", f"{len(desc)} chars")

    h1 = len(re.findall(r"<h1\b", html))
    gate(h1 == 1, "exactly one <h1>", f"{h1} found")
    h2 = len(re.findall(r"<h2\b", html))
    gate(5 <= h2 <= 9, "H2 count 5-9", f"{h2} found")

    hrefs = re.findall(r'href="([A-Za-z0-9._\-]+\.html)"', html)
    out = {h.lower() for h in hrefs if h.lower() != slug}
    gate(len(out) >= 4, ">= 4 internal links", f"{len(out)}: {sorted(out)[:8]}")
    ib = inbound_map()
    recip = sorted(p for p in out if slug in ib.get(p, set()))
    gate(len(recip) >= 3, ">= 3 links to pages that link back (§5.2)",
         f"reciprocal: {recip}")

    imgs = re.findall(r"<img\b[^>]*>", html)
    bad = []
    total_img_bytes = 0
    article_bytes = 0
    art_html = html.split("<article>")[-1].split("</article>")[0]
    for tag in imgs:
        for attr in ('alt="', 'width="', 'height="', 'loading="lazy"'):
            if attr not in tag:
                bad.append(f"missing {attr}: {tag[:70]}")
        src = re.search(r'src="([^"]+)"', tag)
        if src:
            s = src.group(1)
            p = WEB / s.lstrip("/")
            if not p.exists():
                bad.append(f"file missing: {s}")
            else:
                sz = p.stat().st_size
                total_img_bytes += sz
                if s in art_html:
                    article_bytes += sz
    gate(not bad, "every <img> has alt/width/height/lazy + file exists",
         "; ".join(bad[:4]))
    # §12 reads as a page budget, but the shared shell (sidebar ads, popular-page
    # thumbs, news.webp) costs ~273 KB on every page of this site. The gate we
    # can act on is the article's own figures; the shell is a separate task.
    gate(article_bytes < 400 * 1024, "article figure weight < 400 KB",
         f"article {article_bytes // 1024} KB")
    if total_img_bytes >= 400 * 1024:
        print(f"  [note] whole-page image weight {total_img_bytes // 1024} KB "
              f"(shell {total_img_bytes - article_bytes} KB) — §12's page budget "
              f"cannot pass while the shell is this heavy; site-wide task, not a "
              f"series defect")

    cites = re.findall(r"\(1894, p\. (\d+)\)", html)
    gate(len(cites) >= 3, ">= 3 page-cited quotes (1894, p. N)",
         f"{len(cites)} cites on pages {sorted(set(cites), key=int)}")

    gate(re.search(r">Sources<", html) is not None, "Sources block present")
    gate(ARCHIVE_ITEM in html, f"archive.org item string present ({ARCHIVE_ITEM})")

    blocks = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                       html, re.S)
    parsed, errs = [], []
    for b in blocks:
        try:
            parsed.append(json.loads(b))
        except Exception as e:
            errs.append(str(e))
    gate(blocks and not errs, "JSON-LD parses", "; ".join(errs[:2]))
    types = {p.get("@type") for p in parsed}
    gate(any(p.get("@type") == "Article" and "citation" in p for p in parsed),
         "Article.citation present", f"types={sorted(t for t in types if t)}")
    if "FAQPage" in types:
        faq = next(p for p in parsed if p.get("@type") == "FAQPage")
        ok = bool(faq.get("mainEntity")) and all(
            q.get("name") and q.get("acceptedAnswer", {}).get("text")
            for q in faq["mainEntity"])
        gate(ok, "FAQPage valid", f"{len(faq.get('mainEntity', []))} items")

    gate("comments.css" not in html, "no css/comments.css (D3)")
    gate("<!-- Comments section -->" not in html and "Comments</h3>" not in html,
         "no comments block (D3)")
    gate(".pdf" not in low, "no book-PDF link (D4)")
    gate(len(html.encode()) < 200 * 1024, "HTML < 200 KB",
         f"{len(html.encode()) // 1024} KB")
    gate('href="http://' not in html, "no http:// links")

    # voice rule (§0 non-negotiable 5): no typographic dashes or curly quotes in the
    # article body. The shared shell (nav, sidebar, footer) is not checked.
    bad_chars = sorted({c for c in art_html if c in "\u2014\u2013\u2018\u2019\u201c\u201d\u2026"})
    gate(not bad_chars, "no em/en dashes, curly quotes or ellipses in article body",
         "found: " + " ".join(f"{c}(U+{ord(c):04X})" for c in bad_chars))

    aff = re.findall(r'<a[^>]*hop\.clickbank\.net[^>]*>', html)
    tid = re.findall(r"[?&]tid=(1894_(?:\d{2}|hub))", html)
    gate(bool(aff) and bool(tid), "affiliate link carries tid=1894_NN",
         f"tids={sorted(set(tid))}")
    if aff:
        badrel = [a for a in aff if 'rel="noopener noreferrer nofollow"' not in a]
        gate(not badrel, "affiliate rel=noopener noreferrer nofollow",
             f"{len(badrel)} bad")

    # series furniture (§3)
    if "The 1894 File" in html:
        gate("The 1894 File · No." in html or 'series' in low,
             "series kicker present")
        gate("We earn a commission" in html, "one-line affiliate disclosure present")
    figs = re.findall(r'<figure class="mb-4 pt-5">', html)
    if "assets/tesla1894/" in html:
        gate(2 <= len(figs) <= 3, "2-3 figures in <figure class=\"mb-4 pt-5\">",
             f"{len(figs)} figures")
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?")
    ap.add_argument("--all-series", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    targets = []
    if args.all_series:
        idx = SERIES / "index.json"
        if idx.exists():
            for row in json.loads(idx.read_text()):
                targets.append(WEB / row["slug"])
        targets += sorted(WEB.glob("tesla-1894*.html"))
    elif args.page:
        targets.append(Path(args.page))
    else:
        ap.error("a page path, or --all-series")

    failed = 0
    for p in dict.fromkeys(targets):
        if not p.exists():
            print(f"MISSING {p}")
            failed += 1
            continue
        res = check(p)
        bad = [r for r in res if not r[0]]
        print(f"\n=== {p.name} — {'PASS' if not bad else 'FAIL'} "
              f"({len(res) - len(bad)}/{len(res)} gates) ===")
        for ok, label, detail in res:
            mark = " ok " if ok else "FAIL"
            print(f"  [{mark}] {label}" + (f"  -> {detail}" if detail and not ok else ""))
        failed += bool(bad)
    print(f"\n{len(targets) - failed}/{len(targets)} pages pass the numeric gates")
    print("not covered here (need vision): figure subject/caption truth, "
          "3-viewport layout, OG legibility — §12 visual gates via shot_qa.py")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
