#!/usr/bin/env python3
"""Nav inventory: what the navbar actually contains, and what depends on it.

Item 6 of PLAN-ALT-NAV-OVERFLOW.md. Run this BEFORE editing and again AFTER: the
orphan set must not grow. It answers three questions no eyeball can answer on 53
pages:
  1. how many byte-distinct navbar blocks exist (a single-template replacement
     would destroy the pages that do not match it),
  2. how long the collapsed dropdown is,
  3. which pages are reachable ONLY through that dropdown - trim those and they
     become orphans with no internal links.

Usage: python3 inventory.py            # filesystem only, no browser, fast
"""
import collections
import glob
import hashlib
import os
import re
import sys

SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if "--site" in sys.argv:                      # measure a generated intermediate state
    SITE = os.path.abspath(sys.argv[sys.argv.index("--site") + 1])
print(f"measuring: {SITE}")
if not os.path.exists(os.path.join(SITE, "index.html")):
    sys.exit(f"cannot find site root (tried {SITE})")

NAV = re.compile(r"<nav[^>]*navbar-expand[^>]*>.*?</nav>", re.S)
DROPDOWN = re.compile(r'<ul class="dropdown-menu[^"]*"[^>]*>(.*?)</ul>', re.S)
TOP = re.compile(r'<a class="nav-link[^"]*"[^>]*href="([^"]+)"', re.S)
ANCHOR = re.compile(r'href="(/[^"#?]*|https?://teslamagneticgenerator\.com[^"#?]*)"', re.S)
LOCAL = {"/" + os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SITE, "*.html"))} | {"/"}
# index.html IS the homepage at /; see slug() for the redirect evidence.
LOCAL.discard("/index")


def slug(h):
    """Strip the protocol/host and the .html suffix so /x.html and /x compare
    equal. The absolute form matters more than it looks: /articles links its 33
    cards as https://teslamagneticgenerator.com/<slug>, and while only
    root-relative hrefs were counted that whole hub was invisible to this
    script - which is how a page linked only from the hub could be reported an
    orphan. Same-domain absolute hrefs are internal links.

    /index collapses onto /, because on this host they are the same URL: Cloudflare
    Pages 308-redirects /index to / (measured on the live site:
    `curl -sSI https://teslamagneticgenerator.com/index` -> HTTP/2 308,
    location: /) and index.html's own canonical is
    https://teslamagneticgenerator.com/. Counting them as two pages is what made
    the homepage look like an orphan once the old nav's /index link went away."""
    h = re.sub(r"^https?://teslamagneticgenerator\.com", "", h)
    h = h.split("#")[0].split("?")[0].rstrip("/")
    if h.endswith(".html"):
        h = h[:-5]
    h = h or "/"
    return "/" if h == "/index" else h


def main():
    os.chdir(SITE)
    variants = collections.Counter()
    blocks = {}
    dropdown_sizes = collections.Counter()
    top_links = collections.Counter()
    dropdown_hrefs = set()

    for f in sorted(glob.glob("*.html")):
        html = open(f, encoding="utf-8", errors="replace").read()
        m = NAV.search(html)
        if not m:
            print(f"  no expand-navbar in {f}")
            continue
        block = m.group(0)
        key = hashlib.sha256(block.encode()).hexdigest()[:8]
        variants[key] += 1
        blocks.setdefault(key, (f, block))
        for a in TOP.findall(block):
            top_links[slug(a)] += 1
        dd = DROPDOWN.search(block)
        if dd:
            hrefs = [slug(h) for h in re.findall(r'href="([^"]+)"', dd.group(1))]
            dropdown_sizes[len(hrefs)] += 1
            dropdown_hrefs |= set(hrefs)

    print(f"pages scanned: {len(glob.glob('*.html'))}")
    print(f"distinct navbar blocks: {len(variants)}  (counts: {sorted(variants.values(), reverse=True)})")
    print("  one representative each - expect to hand-check one replacement per variant:")
    for key, (first, block) in blocks.items():
        mods = re.findall(r"navbar-expand-\w+|navbar-dark|navbar-light|sticky-top", block)
        print(f"    {key}  pages using it: {variants[key]:2}  first: {first:42}  flags: {sorted(set(mods))}  len={len(block)}")
    print("  NB: if the flags and lengths match across variants, the difference may be"
          "\n      whitespace or attribute order only - diff two representatives before"
          "\n      assuming you need one hand-authored replacement per variant.")
    print(f"dropdown item counts -> pages: {dict(dropdown_sizes)}")
    print(f"top-level nav hrefs seen: {dict(top_links)}")
    missing = sorted(h for h in dropdown_hrefs if h not in LOCAL)
    print(f"dropdown hrefs with no local page: {missing or 'none'}")

    # Orphans: pages with no inbound internal link outside the nav itself.
    pages = {p for p in LOCAL if p != "/404"}
    linked = set()
    for f in glob.glob("*.html"):
        body = NAV.sub("", open(f, encoding="utf-8", errors="replace").read())
        linked |= {slug(m.group(1)) for m in ANCHOR.finditer(body)}
    nav_top = set(top_links) - {"#"}
    orphans = sorted(p for p in pages if p not in linked and p not in nav_top)
    print(f"\npages reachable ONLY through the nav: {len(orphans)}")
    for p in orphans:
        print("   ", p)
    print("\nAfter the nav change, re-run: this number must not grow, and every"
          "\ndropdown href must still resolve. Both are gates, not observations.")


if __name__ == "__main__":
    main()
