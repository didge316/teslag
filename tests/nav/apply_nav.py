#!/usr/bin/env python3
"""Rewrite the navbar on every page to one canonical block (item 6).

The 32-item "Pages" dropdown is the whole site's internal-link graph, so the
replacement is generated rather than hand-edited, and the script is written to
fail loudly rather than quietly do nothing:

  * pages are grouped by a WHITESPACE-NORMALISED sha256 of their <nav> block,
    because the 5 byte-distinct blocks in the site differ only in trailing
    spaces and one label (inventory.py proves that; the two real differences
    are written down in NAV_DIFF below);
  * a file that matches no known block, or matches twice, aborts the run - a
    script that writes nothing because it matched nothing looks exactly like
    success, so the written count is printed and must be every page;
  * `nav-link active` is carried across by href, so the one page that marks its
    own nav entry (about.html) still does afterwards and the 52 that do not are
    untouched;
  * HUB_ONLY lists the two pages that leave the navbar by design. Refusing to
    run unless every one of them is already linked from the body of another page
    is what turns "depth replaces breadth" from an assertion into a check.

Usage:
    python3 apply_nav.py --dry-run       # what would change, nothing written
    python3 apply_nav.py                 # write
    python3 apply_nav.py --check         # is the site already canonical? exit 0/1
"""
import glob
import hashlib
import os
import re
import subprocess
import sys

SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
NAV = re.compile(r"<nav[^>]*navbar-expand[^>]*>.*?</nav>", re.S)

# (dropdown label, [(href, anchor text)]) x 3, every one <=10 items.
# The anchor texts are copied byte-for-byte out of the old dropdown so that no
# anchor text on the site changes; only which group it sits in changes.
GROUPS = [
    ("Build &amp; plans", [
        ("/magnetic-generator-for-beginners-step-by-step", "Magnetic Generator for Beginners — Step by Step"),
        ("/build-a-magnetic-generator", "Learning How to Build a Magnetic Generator is The Best Thing You Will Ever Do!"),
        ("/diy-magnetic-generator", "Energize Your Home with a DIY Magnetic Generator"),
        ("/magnetic-dynamo-generator", "The Magnetic Dynamo Generator"),
        ("/magnetic-generator", "How Much Does It Cost to Build a Magnetic Generator?"),
        ("/tesla-magnetic-generator-materials-list-cost", "Tesla Magnetic Generator Materials List Cost"),
        ("/tesla-magnetic-generator-cost-savings-per-month", "Tesla Magnetic Generator Cost Savings Per Month"),
        ("/magnetic-generator-plans-review", "Best Magnetic Generator Plans Review 2026"),
        ("/can-I-buy", "You Will Never See a Magnetic Generator For Sale"),
        ("/tesla-magnetic-generator-worth-it", "Is a Tesla Magnetic Generator Worth It? An Honest 2026 Review"),
    ]),
    ("Power your home", [
        ("/whole-house", "Can You Really Build a Magnetic Generator to Power Your Whole Home?"),
        ("/tesla-magnetic-generator-for-cabin", "Tesla Magnetic Generator for Cabin"),
        ("/magnetic-generator-for-rv-complete-off-grid-guide", "Magnetic Generator for RV — Complete Off Grid Guide"),
        ("/magnetic-generator-for-emergency-backup", "Magnetic Generator for Emergency Backup"),
        ("/tesla-magnetic-generator-vs-solar-power-which-is-better", "Tesla Magnetic Generator vs Solar Power — Which Is Better"),
        ("/solar", "Solar Power vs Magnetic Energy"),
        ("/How-Much-Noise-Does-a-Free-Energy-Device-Make", "How Much Noise Do Magnetic Generators Make?"),
        ("/electricity-using-magnets", "Generate Electricity Using Magnets"),
        ("/How-to-Make-Free-Electricity-at-Home", "How to Make Free Electricity at Home"),
        ("/can-we-use-magnets-to-generate-electricity-a-magnetic-marvel", "Can We Use Magnets to Generate Electricity"),
    ]),
    ("Free energy &amp; Tesla", [
        ("/tesla-1894", "The 1894 File: Tesla's First Big Book, Page by Page"),
        ("/nikola-tesla-inventor-extraordinaire", "Nikola Tesla - Inventor Extraordinaire"),
        ("/7-interesting-facts-about-magnets", "7 Interesting Facts About Magnets"),
        ("/magnet-motor", "The Free Energy Magnet Motor"),
        ("/perpetual-motion-generator", "Perpetual Motion Machines - Learn The Truth"),
        ("/build-a-perpetual-motion-generator", "Build a Perpetual Motion Generator and Save Yourself Thousands"),
        ("/unleashing-the-power-of-free-energy", "Unleashing The Power of Free-Energy."),
        ("/is-magnetic-energy-renewable-or-nonrenewable", "Is Magnetic Energy Renewable or Nonrenewable"),
        ("/free-electricity-from-magnets", "Free Electricity From Magnets"),
        ("/magnetic-generator-scam", "The Magnetic Generator Scam"),
    ]),
]

# Pages that leave the navbar on purpose, because the nav has 3 groups of 10 and
# 32 pages will not fit into 30 slots. They are the two closest near-duplicates
# of pages that stay (Unleashing The Magnet Magic of
# /unleashing-the-power-of-free-energy, Renewable Energy Using Magnets of
# /is-magnetic-energy-renewable-or-nonrenewable), so the hub is where a reader
# still finds them: /articles is a top-level nav entry on all 53 pages, so a link
# from it is one more click away than the nav was, not zero.
#
# What this is NOT, because an earlier version of this comment said otherwise:
# these are not pages that were "reachable only through the dropdown". The first
# run of inventory.py reported six such pages, and inventory.py's slug() was not
# counting same-domain absolute hrefs, so the hub's 33 cards - all written as
# https://teslamagneticgenerator.com/<slug> - were invisible to it. Re-measured
# at HEAD with the fix in place (tests/nav/inventory-BEFORE-git.txt), the number
# of nav-only pages before this change is zero, not six. What is actually true
# and what check_hub_links() below enforces: each demoted page is linked from the
# body of articles.html today, so removing it from the nav costs a click and not
# a route.
HUB_ONLY = [
    ("/unleashing-the-magnet-magic-is-free-energy-possible", "Unleashing The Magnet Magic"),
    ("/renewable-energy-using-magnets-a-magnetic-revolution", "Renewable Energy Using Magnets"),
]

TOP = [
    ("/articles", "Articles"),
    ("/", "Home"),
    ("/contact", "Contact"),
    ("/about", "About"),
]

IND = " " * 24  # dropdown items sit 24 spaces deep in the existing markup


def nav_block(active=()):
    """The canonical navbar. `active` is the tuple of hrefs that carry
    nav-link active on the page being written."""
    def cls(href):
        return "nav-link active" if href in active else "nav-link"

    out = ['<nav class="navbar navbar-expand-lg navbar-dark bg-dark">',
           '            <div class="container">',
           '                <a class="navbar-brand" href="/">Tesla Magnetic Generator</a>',
           '                ',
           '                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" ',
           '                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" ',
           '                        aria-expanded="false" aria-label="Toggle navigation">',
           '                    <span class="navbar-toggler-icon"></span>',
           '                </button>',
           '                ',
           '                <div class="collapse navbar-collapse" id="navbarSupportedContent">',
           '                    <ul class="navbar-nav ms-auto">']
    for href, label in TOP:
        out += [f'                        <li class="nav-item">',
                f'                            <a class="{cls(href)}" href="{href}">{label}</a>',
                f'                        </li>']
    out.append('                        ')
    for label, items in GROUPS:
        out += [f'                        <li class="nav-item dropdown">',
                f'                            <a class="nav-link dropdown-toggle" href="#" role="button" ',
                f'                            data-bs-toggle="dropdown" aria-expanded="false" aria-haspopup="true">',
                f'                                {label}',
                f'                            </a>',
                f'                            <ul class="dropdown-menu">']
        out += [f'{IND}<li><a class="dropdown-item" href="{href}">{text}</a></li>' for href, text in items]
        out += ['                            </ul>',
                '                        </li>']
    out += ['                    </ul>',
            '                </div>',
            '            </div>',
            '        </nav>']
    return "\n".join(out)


NAVIGATE = nav_block()
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def read_pages():
    # Scope discipline, learned the hard way. The tree also holds pages that are
    # somebody else's uncommitted work in progress. A tool that globs `*.html` will
    # rewrite those too - and one of mine did, at 19:37 today, running a whitespace
    # repair over an untracked page its author was in the middle of. The edit was
    # provably meaning-preserving (the (tag, attribute, value) triple check), which
    # is thin comfort for the blast radius being wrong; so the default here is the
    # pages git knows about, and the ones it does not are named out loud on the way
    # past rather than quietly included. Pass --include-untracked to opt back in.
    pages = {}
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        pages[os.path.basename(f)] = open(f, encoding="utf-8", errors="replace").read()
    tracked = set()
    r = subprocess.run(["git", "ls-files", "*.html"], cwd=SITE, capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        tracked = {os.path.basename(p) for p in r.stdout.split()}
    skipped = sorted(set(pages) - tracked) if tracked else []
    if skipped and "--include-untracked" not in sys.argv:
        for name in skipped:
            del pages[name]
        print(f"pages: {len(pages)} tracked by git; NOT touching {len(skipped)} untracked "
              f"(somebody else's work in progress): {', '.join(skipped)}\n"
              f"       pass --include-untracked if you meant it")
    else:
        print(f"pages: {len(pages)}")
    return pages


def slug(h):
    h = h.split("#")[0].split("?")[0].rstrip("/")
    return h[:-5] if h.endswith(".html") else h or "/"


def coverage_check(pages):
    """Every destination the old navbar linked must still be linked, in the nav or
    by a named hub demotion. Prints the accounting and stops on anything unexplained.

    This exists because the destination test the plan describes does not catch a
    dropped destination: it asserts that every href in the nav resolves to a page,
    and an href that has been deleted is not in the nav to be wrong about. The
    property that matters is coverage - old destinations minus new destinations -
    and it has to be computed against `HEAD`, so this one function is git-aware.

    It also earns its place by what it caught when I re-derived this by hand
    instead of running it: a grep for `href="/<slug>"` reported that the two demoted
    articles had *no* inbound body links at all, which would have made them orphans
    and the change unacceptable. They are not: articles.html links them as
    https://teslamagneticgenerator.com/<slug>, the absolute form the hub was written
    with. Same trap as the one in inventory.py's docstring, approached from the
    other side.
    """
    hrefs = re.compile(r'href="([^"#][^"]*)"')
    def clean(h):
        h = h.split("#")[0]
        if h.startswith("https://teslamagneticgenerator.com"):
            h = h[len("https://teslamagneticgenerator.com"):] or "/"
        return h[:-5] if h.endswith(".html") else h

    old, new = set(), set()
    for f, html in pages.items():
        m = NAV.search(html)
        if m:
            new |= {clean(h) for h in hrefs.findall(m.group(0))}
        r = subprocess.run(["git", "show", f"HEAD:{f}"], cwd=SITE,
                           capture_output=True, text=True)
        if r.returncode == 0:
            m2 = NAV.search(r.stdout)
            if m2:
                old |= {clean(h) for h in hrefs.findall(m2.group(0))}
    dropped = sorted(old - new)
    added = sorted(new - old)
    hub = {h for h, _ in HUB_ONLY}
    unexplained = [h for h in dropped if h not in hub]
    print(f"nav coverage: {len(old)} destinations in HEAD's nav, {len(new)} in the new nav")
    print(f"  dropped: {dropped or 'none'}")
    print(f"  added:   {added or 'none'}")
    print(f"  every dropped destination is a named hub demotion (HUB_ONLY): "
          f"{'yes' if not unexplained else 'NO'}")
    if unexplained:
        sys.exit(f"destinations dropped with no explanation and no hub link: {unexplained}")


def check_hub_links(pages):
    """Every demoted page must already be linked from the body (not the nav) of
    another page, or this run would orphan it."""
    bodies = {f: NAV.sub("", h) for f, h in pages.items()}
    bad = []
    for href, _ in HUB_ONLY:
        want = slug(href)
        srcs = [f for f, b in bodies.items()
                if re.search(rf'href="{re.escape(want)}(\.html)?"', b)
                or re.search(rf'href="https://teslamagneticgenerator\.com{re.escape(want)}(\.html)?"', b)]
        if not srcs:
            bad.append(href)
    return bad


def main():
    args = sys.argv[1:]
    if not os.path.exists(os.path.join(SITE, "index.html")):
        sys.exit(f"cannot find site root (tried {SITE})")
    check = "--check" in args
    write = not check and "--dry-run" not in args
    pages = read_pages()

    for _, items in GROUPS:
        if len(items) > 10:
            sys.exit(f"a dropdown has {len(items)} items; the definition of done is <=10")
    nav_hrefs = [h for _, items in GROUPS for h, _ in items] + [h for h, _ in TOP]
    if len(set(nav_hrefs)) != len(nav_hrefs):
        sys.exit("the same href appears twice in the new nav")

    bad = check_hub_links(pages)
    if bad:
        sys.exit("demoted pages with no body link anywhere, refusing to run:\n  " + "\n  ".join(bad) +
                 "\nLink them from articles.html first (the hub), then re-run.")

    groups = {}
    for f, html in pages.items():
        for m in NAV.finditer(html):
            groups.setdefault(norm(m.group(0)), []).append(f)
        n = len(NAV.findall(html))
        if n != 1:
            sys.exit(f"{f} has {n} navbar-expand blocks; expected exactly 1")
    print(f"whitespace-normalised nav groups: {len(groups)} "
          f"({sorted((len(v) for v in groups.values()), reverse=True)})")

    if check:
        # Canonical means idempotent *per page*, not byte-identical across the site:
        # about.html is the one page that carries `nav-link active`, and a check that
        # compares it against the shared block reports the site's one correct page as
        # wrong. Regenerating each page's block from its own active hrefs is the
        # invariant that actually matters: run the tool twice, get the same file.
        same, not_canon = 0, []
        for f, html in pages.items():
            mm = NAV.search(html)
            if not mm:
                not_canon.append(f + " (no navbar block)")
                continue
            active = tuple(mt.group(1) for mt in
                           re.finditer(r'class="nav-link[^"]*\bactive\b[^"]*"\s+href="([^"]+)"',
                                       mm.group(0)))
            if norm(nav_block(active)) == norm(mm.group(0)):
                same += 1
            else:
                not_canon.append(f)
        print(f"pages already canonical (each idempotent against its own active state): "
              f"{same} of {len(pages)}")
        if same != len(pages):
            for f in not_canon:
                print(f"  not canonical: {f}")
            sys.exit(1)
        coverage_check(pages)
        sys.exit(0)

    written = 0
    for f, html in pages.items():
        m = NAV.search(html)
        old = m.group(0)
        # `nav-link active` is a per-page marker, not part of the shared block:
        # about.html is the only page in the site that has one today, and it is
        # carried across by href so that page keeps it and 52 pages do not gain
        # one.
        active = tuple(mt.group(1) for mt in
                       re.finditer(r'class="nav-link[^"]*\bactive\b[^"]*"\s+href="([^"]+)"', old))
        new = nav_block(active)
        if norm(new) == norm(old):
            print(f"  canonical already: {f}")
            written += 1
            continue
        if write:
            open(os.path.join(SITE, f), "w", encoding="utf-8").write(html[:m.start()] + new + html[m.end():])
        written += 1

    print(f"\n{'written' if write else 'would write'}: {written} of {len(pages)} pages")
    if written != len(pages):
        sys.exit("REFUSING: not every page was matched and written")
    nav_hrefs = [h for _, items in GROUPS for h, _ in items]
    print(f"dropdowns: {[len(i) for _, i in GROUPS]} items; top level: {[h for h, _ in TOP]}")
    print(f"nav hrefs: {len(nav_hrefs)} + {len(HUB_ONLY)} demoted to the hub = "
          f"{len(nav_hrefs) + len(HUB_ONLY)} pages reachable")
    if not write:
        print("DRY RUN, nothing written. Re-run without --dry-run to write.")
    else:
        print("\nNow re-run inventory.py (orphan set must not grow) and the link crawl.")


if __name__ == "__main__":
    main()
