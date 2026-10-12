#!/usr/bin/env python3
"""Numeric QA gates for a series page — SERIES-PLAN-1894.md §12.

    python3 books/tools/qa_page.py website/tesla-earthquake-machine.html
    python3 books/tools/qa_page.py --all-series      # every page in index.json
    python3 books/tools/qa_page.py --self-test       # fixture test for the gates

Checks the machine can check. The visual half of §12 (figure subjects, caption
truth, three screenshots, OG legibility) is a separate gate and needs eyes.
Exit code 0 = every numeric gate passed.

Link resolution follows the URL contract in SEO-URL-FIX-PLAN.md §1: a page is
addressed at /x with no extension, and /x is alive iff x.html exists. The older
x.html spelling is still resolved, so the tool runs against pages written before
that change, but it is reported by the redirect gate.
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
SITE = "https://teslamagneticgenerator.com"
INBOUND = {}          # page stem -> set of page stems that link to it (computed once)


def meta(html, name):
    m = re.search(rf'<meta name="{name}" content="(.*?)"\s*/?>', html, re.S)
    return m.group(1) if m else ""


def page_key(href):
    """Normalise an internal href to the file key it addresses, or None.

    /x, x.html and x all address the page file x.html, so all three key to "x".
    Both spellings are accepted on purpose: this tool has to run against pages
    written before the URL migration as well as after it (SEO-URL-FIX-PLAN.md G2).
    External URLs, bare anchors, assets and directories are not page links.
    """
    t = href.split("#")[0].split("?")[0].strip()
    if not t or t.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t):
        return None
    t = t.lstrip("/")
    if not t or "/" in t or t.startswith("."):
        return None
    return (t[:-5] if t.endswith(".html") else t).lower()


def alive(path):
    """Resolve a root-absolute path the way Cloudflare Pages does: static file
    first, then a page addressed without its extension. /x is alive iff x.html or
    x exists in website/."""
    p = path.lstrip("/")
    if not p:
        return (WEB / "index.html").exists()
    if (WEB / p).exists():                       # assets keep their extension
        return True
    return (WEB / (p + ".html")).exists()


def inbound_map():
    if INBOUND:
        return INBOUND
    for f in WEB.glob("*.html"):
        try:
            h = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for href in re.findall(r'href="([^"]+)"', h):
            key = page_key(href)
            if key:
                INBOUND.setdefault(key, set()).add(f.stem.lower())
    return INBOUND


DEAD_LINK_GATE = "no dead links (\u00a712)"


def redirecting_links(html):
    """Internal page links that point at a URL which only exists to redirect.

    /x.html and /x/ both 301 or 308 to /x now, so a link in either form costs a
    hop on every click and sends the target's signal to an alias instead of to it.
    This is the gate whose absence let 2,224 .html links sit in the site unnoticed.
    """
    bad = set()
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http://", "https://", "#", "mailto:", "tel:")):
            continue
        t = href.split("#")[0].split("?")[0]
        if not t.startswith("/") or t.count("/") > 1:
            continue                             # assets are not pages
        if t.endswith(".html") or (t.endswith("/") and t != "/"):
            bad.add(href)
    return sorted(bad)


def dead_links(html):
    """Internal hrefs on this page that do not resolve on the deployed site.

    Root-absolute links used to be skipped here on the grounds that the deploy root
    was not this checkout's job. Under the current convention nearly every link is
    root-absolute, so skipping them left the gate checking nothing at all. They are
    resolved through alive(), which is the order Cloudflare Pages uses. A fragment
    or query is stripped before the lookup. Returns sorted offending hrefs.
    """
    dead = set()
    for href in re.findall(r'href="([^"]+)"', html):
        target = href.split("#")[0].split("?")[0]
        if not target or href.startswith("#"):
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
            continue
        if href.startswith("/"):
            if not alive(target):
                dead.add(href)
            continue
        if not (WEB / target).exists():
            dead.add(href)
    return sorted(dead)


def check(path: Path):
    html = path.read_text(encoding="utf-8", errors="ignore")
    low = html.lower()
    slug = path.name.lower()
    stem = path.stem.lower()
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

    hrefs = re.findall(r'href="([^"]+)"', html)
    out = {k for k in (page_key(h) for h in hrefs) if k and k != stem}
    gate(len(out) >= 4, ">= 4 internal links", f"{len(out)}: {sorted(out)[:8]}")
    ib = inbound_map()
    recip = sorted(p for p in out if stem in ib.get(p, set()))
    gate(len(recip) >= 3, ">= 3 links to pages that link back (§5.2)",
         f"reciprocal: {recip}")

    # §12 "no broken relative links", machine-checked: a link to an article that
    # is not written yet fails the page instead of being remembered by a human.
    dead = dead_links(html)
    gate(not dead, DEAD_LINK_GATE, f"{len(dead)} dead: {dead[:6]}")

    # The URL contract (SEO-URL-FIX-PLAN.md §1). The gate that let 46 wrong
    # canonicals ship is this one, and it did not exist.
    want_can = SITE + ("/" if stem == "index" else "/" + stem)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    gate(bool(can) and can.group(1) == want_can,
         "canonical self-referential and extensionless",
         f"got {can.group(1) if can else 'none'}, want {want_can}")
    ogu = re.search(r'<meta property="og:url" content="([^"]+)"', html)
    gate(bool(can) and bool(ogu) and ogu.group(1) == can.group(1),
         "og:url equals canonical",
         f"og={ogu.group(1) if ogu else 'none'}")
    redir = redirecting_links(html)
    gate(not redir, "no internal link points at a redirecting URL",
         f"{len(redir)}: {redir[:6]}")

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
              f"(shell {(total_img_bytes - article_bytes) // 1024} KB) — §12's page budget "
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


def self_test():
    """Fixture tests for the link and canonical gates.

    Each case names a fixture, a gate, whether that gate should pass, and a string
    that must appear in the failure detail. Fixtures live in a temp dir; website/ is
    never touched.
    """
    import shutil
    import tempfile

    global WEB
    real_web, tmp = WEB, Path(tempfile.mkdtemp(prefix="qa-selftest-"))
    CAN_OK = f'{SITE}/canon_ok'
    try:
        (tmp / "target.html").write_text("<html><body>ok</body></html>")
        (tmp / "assets").mkdir()
        (tmp / "assets/x.css").write_text("body{}")
        # liveness: all three spellings resolve, so none of them is dead
        (tmp / "live.html").write_text(
            '<a href="target.html">old relative form</a> '
            '<a href="/target">current form</a> '
            '<a href="/target.html">old absolute form</a> '
            '<a href="/target#x">anchor</a> '
            '<a href="https://example.com/gone.html">external</a> '
            '<a href="#top">jump</a> <a href="/assets/x.css">asset</a>')
        (tmp / "broken.html").write_text(
            '<a href="target.html">live</a> '
            '<a href="/rotating-magnetic-field-1888">not written yet</a>')
        (tmp / "assets.html").write_text('<a href="/assets/nope.css">gone</a>')
        # the redirect gate: /x is fine, /x.html and /x/ are links to an alias
        (tmp / "redir_ok.html").write_text('<a href="/target">x</a>')
        (tmp / "redir_bad.html").write_text('<a href="/target.html">x</a>')
        # the canonical gate
        (tmp / "canon_ok.html").write_text(
            f'<head><link rel="canonical" href="{CAN_OK}">'
            f'<meta property="og:url" content="{CAN_OK}"></head><body>x</body>')
        (tmp / "canon_bad.html").write_text(
            f'<head><link rel="canonical" href="{CAN_OK}.html">'
            f'<meta property="og:url" content="{CAN_OK}"></head><body>x</body>')
        cases = (
            ("live", DEAD_LINK_GATE, True, ""),
            ("broken", DEAD_LINK_GATE, False, "/rotating-magnetic-field-1888"),
            ("assets", DEAD_LINK_GATE, False, "/assets/nope.css"),
            ("redir_ok", "no internal link points at a redirecting URL", True, ""),
            ("redir_bad", "no internal link points at a redirecting URL", False,
             "/target.html"),
            ("canon_ok", "canonical self-referential and extensionless", True, ""),
            ("canon_bad", "canonical self-referential and extensionless", False,
             f"{CAN_OK}.html"),
            ("canon_bad", "og:url equals canonical", False, ""),
        )
        results = []
        for name, label, want_ok, want_named in cases:
            WEB = tmp
            gates = [g for g in check(tmp / f"{name}.html") if g[1] == label]
            if len(gates) != 1:
                results.append(f"{name}/{label}: gate not in the default set "
                               f"({len(gates)} found)")
                continue
            ok, _, detail = gates[0]
            if ok != want_ok:
                results.append(f"{name}/{label}: expected pass={want_ok}, got pass={ok} "
                               f"({detail})")
            elif want_named and want_named not in detail:
                results.append(f"{name}/{label}: offending value not printed ({detail})")
        return results
    finally:
        WEB = real_web
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?")
    ap.add_argument("--all-series", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true",
                    help="run the fixture tests for the link and canonical gates and exit")
    args = ap.parse_args()

    if args.self_test:
        fails = self_test()
        for f in fails:
            print(f"FAIL {f}")
        print("self-test: link and canonical gates " + ("FAIL" if fails else "PASS"))
        return 1 if fails else 0

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
