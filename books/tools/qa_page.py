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

Heading case is not a number, but it is decided from the file, so it is gated too.
That gate delegates to books/tools/titlecase_headings.py -- the tool that also
fixes the headings -- so the rule lives in one place and cannot drift.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

# The heading-case gate calls its sibling tool; make the import work however this
# file is invoked (as a script, from another cwd, or imported by another tool).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import titlecase_headings  # noqa: E402

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
    A same-origin absolute href (SITE + "/x") is an internal link too and keys to
    "x": 50 of the 51 pages in website/ carry such hrefs (the articles.html cards
    and every canonical), and keying them None made inbound_map() blind to every
    link that arrives that way. External URLs, bare anchors, assets and
    directories are not page links.
    """
    t = href.split("#")[0].split("?")[0].strip()
    if not t or t.startswith("#"):
        return None
    if t.lower().startswith(SITE.lower() + "/"):
        t = t[len(SITE) + 1:]
    elif re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t):
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
HEADING_CASE_GATE = "h2/h3 and FAQ names are title case"
OG_IMAGE_GATE = "og:image and twitter:image point at files that exist"


def heading_case(path):
    """Headings on this page that are not title case: [(kind, current, expected)].

    The check is titlecase_headings.check_headings(), the same call its --check
    mode makes, so the gate and the tool that fixes the headings are one rule.
    <h1> is exempt there on purpose: it is mirrored into <title>, og:title and
    twitter:title, which the 60-char gate above is sized to, so retitling it can
    fail that gate. A quoted source term keeps the print's case for the same
    reason check_quotes.py needs the quotation verbatim.
    """
    try:
        found = titlecase_headings.check_headings(path)
    except Exception as e:                 # unreadable page is a failed gate, not a pass
        return [("error", str(e), "")]
    label = {"2": "h2", "3": "h3", "faq": "faq-name"}
    return [(label.get(kind, kind), cur, want) for kind, cur, want in found]



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


def asset_path(url):
    """Local file a meta content URL addresses, or None for anything that is not
    this site's or a local path. Same-origin absolute, root-absolute and relative
    spellings all resolve, as they do in dead_links()."""
    t = url.split("#")[0].split("?")[0].strip()
    if not t:
        return None
    if t.lower().startswith(SITE.lower() + "/"):
        t = t[len(SITE) + 1:]
    elif re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t):
        return None
    return WEB / t.lstrip("/")


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


def series_rows():
    """The rows of new_content/1894-series/index.json, in file order.

    index.json is the authoritative list of series pages: it is what carries the
    tid, the figure manifest and the gate record for each page. Series membership
    is read from it, never inferred from page content. It used to be inferred from
    the string "The 1894 File" appearing in the page, and the hub's entry in the
    shared nav dropdown puts that string on all 51 pages of the site, so every
    legacy page was suddenly held to two series gates it was never built to
    satisfy (measured 2026-10-20, HANDOFF-1894.md section 4).
    """
    p = SERIES / "index.json"
    if not p.exists():
        return []
    return json.loads(p.read_text())


def series_files():
    """Every page file the series owns: the index.json rows plus any tesla-1894*
    page on disk that has no row yet, so a page can never escape the gates by
    being forgotten."""
    files = {WEB / row["slug"] for row in series_rows()}
    files |= set(WEB.glob("tesla-1894*.html"))
    return {f.name.lower(): f for f in files}


def check(path: Path, series=None):
    html = path.read_text(encoding="utf-8", errors="ignore")
    low = html.lower()
    slug = path.name.lower()
    stem = path.stem.lower()
    if series is None:
        series = slug in series_files()
    hub = any(r["slug"].lower() == slug and r.get("no") == "hub"
              for r in series_rows())
    res = []

    def gate(ok, label, detail=""):
        res.append((bool(ok), label, detail))

    def gate_series(ok, label, detail=""):
        """A SERIES-PLAN section 12 rule that binds a series page only.

        Reported as skipped, not passed, on a page the series does not own: the
        record has to say which rules were actually applied.
        """
        if not series:
            res.append((None, label, "not a series page (no index.json row)"))
        else:
            gate(ok, label, detail)

    t = re.search(r"<title>(.*?)</title>", html, re.S)
    title = t.group(1).strip() if t else ""
    gate(title and len(title) <= 60, "title <= 60 chars", f"{len(title)} chars")

    desc = meta(html, "description")
    gate(120 <= len(desc) <= 155, "description 120-155 chars", f"{len(desc)} chars")

    h1 = len(re.findall(r"<h1\b", html))
    gate(h1 == 1, "exactly one <h1>", f"{h1} found")
    h2 = len(re.findall(r"<h2\b", html))
    gate_series(5 <= h2 <= 9, "H2 count 5-9", f"{h2} found")

    # The house style for this series is title-case headings (harness/docs/
    # CONSTRAINTS.md). It was prose until now, which is why 9 shipped pages had to
    # be retitled by hand afterwards rather than caught before they shipped.
    bad_head = heading_case(path)
    gate_series(not bad_head, HEADING_CASE_GATE,
         f"{len(bad_head)} not title case: "
         + " | ".join(f"{k}: {cur!r} -> {want!r}" for k, cur, want in bad_head[:3]))

    hrefs = re.findall(r'href="([^"]+)"', html)
    out = {k for k in (page_key(h) for h in hrefs) if k and k != stem}
    gate(len(out) >= 4, ">= 4 internal links", f"{len(out)}: {sorted(out)[:8]}")
    # §5.2: at least three of the pages this page links to have to link back.
    # ib[p] is the set of pages that link TO p, so "p links back to me" is
    # `p in ib[stem]`, not `stem in ib[p]`. The old predicate was the latter, and
    # since `out` is built from this page's own hrefs, `stem in ib[p]` is true for
    # every p in `out` by construction: the gate could not fail, and reported ok on
    # a page with zero inbound links anywhere on the site (measured 2026-10-20 on
    # tesla-1894-word-search.html: 0 inbound, gate ok). The fixture pass covers it.
    ib = inbound_map()
    recip = sorted(p for p in out if p in ib.get(stem, set()))
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
    # A share card only exists if the bytes it points at exist. Until 2026-10-20
    # every page in this series pointed og:image and twitter:image at
    # assets/og/<slug>.webp and the directory did not exist: 15 pages passed a
    # gate that had only ever looked at the tag, and every share of every article
    # in the series went out imageless. This reads the file, not the tag.
    share = re.findall(
        r'<meta (?:property|name)="(?:og|twitter):image" content="([^"]+)"',
        html)
    missing = sorted({u for u in share if not (asset_path(u) or
                                               Path("/")).exists()})
    gate(bool(share) and not missing, OG_IMAGE_GATE,
         f"{len(share)} tag(s), missing: {missing[:4]}")
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
    gate_series(len(cites) >= 3, ">= 3 page-cited quotes (1894, p. N)",
         f"{len(cites)} cites on pages {sorted(set(cites), key=int)}")

    gate_series(re.search(r">Sources<", html) is not None, "Sources block present")
    gate_series(ARCHIVE_ITEM in html, f"archive.org item string present ({ARCHIVE_ITEM})")

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
    gate_series(any(p.get("@type") == "Article" and "citation" in p for p in parsed),
                "Article.citation present",
                f"types={sorted(t for t in types if t)}")
    if "FAQPage" in types:
        faq = next(p for p in parsed if p.get("@type") == "FAQPage")
        ok = bool(faq.get("mainEntity")) and all(
            q.get("name") and q.get("acceptedAnswer", {}).get("text")
            for q in faq["mainEntity"])
        gate(ok, "FAQPage valid", f"{len(faq.get('mainEntity', []))} items")

    gate_series("comments.css" not in html, "no css/comments.css (D3)")
    gate_series("<!-- Comments section -->" not in html and "Comments</h3>" not in html,
                "no comments block (D3)")
    gate_series(".pdf" not in low, "no book-PDF link (D4)")
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
    gate_series(bool(aff) and bool(tid), "affiliate link carries tid=1894_NN",
                f"tids={sorted(set(tid))}")
    if aff:
        badrel = [a for a in aff if 'rel="noopener noreferrer nofollow"' not in a]
        gate_series(not badrel, "affiliate rel=noopener noreferrer nofollow",
                    f"{len(badrel)} bad")

    # Series furniture (section 3). The kicker is the element make_article.py emits
    # from the `kicker:` field, so the gate reads the furniture, not any text that
    # happens to mention the series. The hub is exempt and says so: it is the
    # series landing page, and its furniture is the ItemList, not a "No. N of 12".
    kicker = re.search(r'<p class="text-muted small mb-2">[^<]*The 1894 File', html)
    itemlist = '"@type": "ItemList"' in html or '"@type":"ItemList"' in html
    gate_series(bool(kicker) or (hub and itemlist), "series kicker present",
                "hub landing page: ItemList in place of a kicker" if hub else
                "no kicker element")
    gate_series("We earn a commission" in html, "one-line affiliate disclosure present")
    figs = re.findall(r'<figure class="mb-4 pt-5">', html)
    if "assets/tesla1894/" in html:
        gate_series(2 <= len(figs) <= 3, "2-3 figures in <figure class=\"mb-4 pt-5\">",
                    f"{len(figs)} figures")
    return res


def self_test():
    """Fixture tests for the link, canonical and heading-case gates.

    Each case names a fixture, a gate, whether that gate should pass, and a string
    that must appear in the failure detail. Fixtures live in a temp dir; website/ is
    never touched.
    """
    import shutil
    import tempfile

    global WEB, INBOUND
    real_web, real_inbound, tmp = WEB, INBOUND, Path(tempfile.mkdtemp(prefix="qa-selftest-"))
    INBOUND = {}      # inbound_map() caches over WEB; it has to be built over the fixtures
    CAN_OK = f'{SITE}/canon_ok'
    try:
        (tmp / "target.html").write_text("<html><body>ok</body></html>")
        (tmp / "assets").mkdir()
        (tmp / "assets/x.css").write_text("body{}")
        (tmp / "assets/og").mkdir()
        (tmp / "assets/og/og_ok.webp").write_bytes(b"RIFFxxxxWEBP")
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
        # the heading-case gate. FAQPage names are checked because they must match
        # the visible <h3> text, so schema drift is the same defect in another file.
        FAQ_OK = ('<script type="application/ld+json">{"@type":"FAQPage","mainEntity":'
                  '[{"@type":"Question","name":"What Did the Coil Do?","acceptedAnswer":'
                  '{"@type":"Answer","text":"It rang."}}]}</script>')
        FAQ_BAD = FAQ_OK.replace('What Did the Coil Do?', 'What did the coil do?')
        (tmp / "case_ok.html").write_text(
            '<h1>The Coil That Ran All Night</h1>'
            '<h2>The Coil That Ran All Night</h2>'
            '<h3>What Did the Coil Do?</h3>' + FAQ_OK)
        # <h1> is exempt: it is mirrored into <title>/og:title, sized to 60 chars
        (tmp / "case_h1_exempt.html").write_text(
            '<h1>the coil that ran all night</h1>'
            '<h2>The Coil That Ran All Night</h2>' + FAQ_OK)
        # a quoted source term keeps the print's case; the rest of the heading does not
        (tmp / "case_quote_ok.html").write_text(
            '<h1>The Machine Was Hard</h1>'
            '<h2>"a tale of woe": Why the Machine Was Hard</h2>' + FAQ_OK)
        (tmp / "case_bad.html").write_text(
            '<h1>The Machine Ran at Full Power</h1>'
            '<h2>the machine ran at full power</h2>'
            '<h3>What Did the Coil Do?</h3>' + FAQ_OK)
        (tmp / "case_faq_bad.html").write_text(
            '<h1>What Did the Coil Do?</h1>'
            '<h2>What Did the Coil Do?</h2>'
            '<h3>What Did the Coil Do?</h3>' + FAQ_BAD)
        (tmp / "case_quote_partial_bad.html").write_text(
            '<h1>The Machine Was Hard</h1>'
            '<h2>"a tale of woe": why the machine was hard</h2>' + FAQ_OK)
        # §5.2 reciprocal links. Three partners that all link back, in the three
        # href spellings page_key accepts (same-origin absolute, root-absolute,
        # relative-with-extension), and three strangers that never link back. The
        # old predicate (`stem in ib[p]`) reported ok for recip_none, because that
        # predicate is true for every page in `out` by construction.
        for n in ("recip_a", "recip_b", "recip_c"):
            (tmp / f"{n}.html").write_text(f'<a href="{SITE}/recip_ok">back</a>')
        for n in ("recip_stranger1", "recip_stranger2", "recip_stranger3"):
            (tmp / f"{n}.html").write_text("<p>nothing links out of here</p>")
        (tmp / "recip_ok.html").write_text(
            f'<a href="{SITE}/recip_a">a</a> <a href="/recip_b">b</a> '
            '<a href="recip_c.html">c</a> <a href="/recip_stranger1">d</a>')
        (tmp / "recip_none.html").write_text(
            '<a href="/recip_stranger1">a</a> <a href="/recip_stranger2">b</a> '
            '<a href="recip_stranger3.html">c</a>')
        # the share-card gate: the tag is not the file. og_bad names a file that
        # is not there, in both the same-origin absolute and the root-absolute
        # spelling; og_none has no share image at all.
        (tmp / "og_ok.html").write_text(
            f'<meta property="og:image" content="{SITE}/assets/og/og_ok.webp">'
            '<meta name="twitter:image" content="/assets/og/og_ok.webp">')
        (tmp / "og_bad.html").write_text(
            f'<meta property="og:image" content="{SITE}/assets/og/nope.webp">')
        (tmp / "og_none.html").write_text("<p>no share image</p>")
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
            ("case_ok", HEADING_CASE_GATE, True, ""),
            ("case_h1_exempt", HEADING_CASE_GATE, True, ""),
            ("case_quote_ok", HEADING_CASE_GATE, True, ""),
            ("case_bad", HEADING_CASE_GATE, False, "the machine ran at full power"),
            ("case_faq_bad", HEADING_CASE_GATE, False, "What did the coil do?"),
            ("case_quote_partial_bad", HEADING_CASE_GATE, False,
             "why the machine was hard"),
            ("recip_ok", ">= 3 links to pages that link back (\u00a75.2)", True, ""),
            ("recip_none", ">= 3 links to pages that link back (\u00a75.2)", False, ""),
            ("og_ok", OG_IMAGE_GATE, True, ""),
            ("og_bad", OG_IMAGE_GATE, False, "assets/og/nope.webp"),
            ("og_none", OG_IMAGE_GATE, False, "0 tag"),
        )
        results = []
        for name, label, want_ok, want_named in cases:
            WEB = tmp
            gates = [g for g in check(tmp / f"{name}.html", series=True)
                     if g[1] == label]
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

        # Series membership comes from index.json, never from page content. The hub's
        # entry in the shared nav dropdown puts the string "The 1894 File" into every
        # page of this site, and the old content-based trigger then held 50 legacy
        # pages to a kicker gate and a disclosure gate they were never built to
        # satisfy (measured 2026-10-20, HANDOFF-1894.md section 4). A page that only
        # mentions the series in its nav must have those gates skipped; a real series
        # page with no kicker must still fail one.
        (tmp / "nav_mention.html").write_text(
            '<nav><a class="dropdown-item" href="/tesla-1894">The 1894 File: '
            "Tesla's First Big Book, Page by Page</a></nav>")
        (tmp / "kicker_ok.html").write_text(
            '<p class="text-muted small mb-2">The 1894 File &middot; No. 6 of 12. '
            "Every quote below is cited.</p>")
        membership = (
            # (fixture, series arg, expected ok)
            ("nav_mention", None, None),      # inferred: not a series page -> skipped
            ("nav_mention", True, False),    # a series page with no kicker still fails
            ("kicker_ok", True, True),
        )
        for name, series_arg, want in membership:
            got = [g for g in check(tmp / f"{name}.html", series=series_arg)
                   if g[1] == "series kicker present"]
            if len(got) != 1:
                results.append(f"{name}: kicker gate missing ({len(got)})")
            elif got[0][0] != want:
                results.append(f"{name}: series={series_arg} expected ok={want}, "
                               f"got ok={got[0][0]} ({got[0][2]})")
        return results
    finally:
        WEB = real_web
        INBOUND = real_inbound
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
        print("self-test: link, canonical and heading-case gates "
              + ("FAIL" if fails else "PASS"))
        return 1 if fails else 0

    targets = []
    if args.all_series:
        targets = sorted(series_files().values())
    elif args.page:
        targets.append(Path(args.page))
    else:
        ap.error("a page path, or --all-series")

    failed = skipped_total = 0
    for p in dict.fromkeys(targets):
        if not p.exists():
            print(f"MISSING {p}")
            failed += 1
            continue
        res = check(p)
        applied = [r for r in res if r[0] is not None]
        skipped = [r for r in res if r[0] is None]
        skipped_total += len(skipped)
        bad = [r for r in applied if not r[0]]
        print(f"\n=== {p.name} — {'PASS' if not bad else 'FAIL'} "
              f"({len(applied) - len(bad)}/{len(applied)} gates"
              + (f", {len(skipped)} series-only skipped" if skipped else "") + ") ===")
        for ok, label, detail in res:
            mark = {True: " ok ", False: "FAIL", None: "skip"}[ok]
            print(f"  [{mark}] {label}" + (f"  -> {detail}" if detail and ok is not True else ""))
        failed += bool(bad)
    print(f"\n{len(targets) - failed}/{len(targets)} pages pass the numeric gates"
          + (f" ({skipped_total} series-only gates skipped on non-series pages)"
             if skipped_total else ""))
    print("not covered here (need vision): figure subject/caption truth, "
          "3-viewport layout, OG legibility — §12 visual gates via shot_qa.py")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
