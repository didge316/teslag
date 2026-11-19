#!/usr/bin/env python3
"""
Is the sticky bar's CTA the same affiliate link the rest of the site uses?

The attribution work checked the `?tid=` and nothing else, which left a hole shaped like
the more important half of the question: nothing on this branch asserted that the href the
bar generates points at the offer at all. A wrong host, a missing trailing slash before
the query, a double slash from string concatenation, or a different hop from the one the
page's own buttons use would have passed every committed check, because each of them only
looks at the substring after `?tid=`.

So this does not hard-code a "correct" URL and grade the bar against it, which would only
prove the test agrees with itself. It compares the bar's href against the affiliate
anchors **already on that same page**, read from the live DOM: for a page whose own links
go to hop X, the bar's link must be hop X plus a tid and nothing else. The site's own
links are the specification. `CONFIG.OFFER_BASE`, parsed out of js/scripts.js rather than
retyped, is the third leg; if the bar's href, the page's own anchors and the constant do
not agree three ways, that is printed rather than averaged.

`rel`, `target` and the disclosure label are read in the same pass because a CTA that
laundered its affiliate status, or opened in the same tab over the article, is the same
class of defect as a wrong URL, and it costs nothing to check while the page is open.

The scroll driver is the trap this probe had. The module's own rule is
`show = pastThreshold && !footerVisible`, so a single scroll either to the trigger or to
the bottom can read "no bar" on a page that shows it fine in between - the first version
of tid-live.py made exactly that mistake on 50 pages at once. It therefore walks a set of
fractions of the scrollable range and stops at the first where the bar is visible,
re-reading scrollHeight each time because lazy-loaded images make the page taller under
it. A page that shows nothing at any position is reported with its measurements rather
than skipped, and is expected only when it is too short to reach the trigger at all.

Run: python3 offer-link.py [base-url]   (needs :8199, the working-tree server; the bar's
JS is in no commit on this branch except its own)
"""
import os
import re
import subprocess
import sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", ".."))
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8199"
OUT = os.path.join(HERE, "offer-link-2026-11-19.txt")

PROBE = """() => {
    const btn = document.querySelector('.tmg-cta-btn');
    const bar = document.querySelector('.tmg-cta-bar');
    const own = [...document.querySelectorAll('a[href*="hop.clickbank.net"]')]
        .filter(a => !a.classList.contains('tmg-cta-btn'))
        .map(a => a.href.split('?')[0]);
    const lab = document.querySelector('.tmg-cta-label');
    const d = document.documentElement;
    const f = document.querySelector('footer');
    return {
        visible: !!bar && bar.classList.contains('is-visible'),
        href: btn ? btn.href : null,
        rel: btn ? btn.getAttribute('rel') : null,
        target: btn ? btn.getAttribute('target') : null,
        label: btn ? btn.textContent.replace(/\\s+/g, ' ').trim() : null,
        disclosure: lab ? lab.textContent.replace(/\\s+/g, ' ').trim() : null,
        ownPrefixes: [...new Set(own)],
        docH: d.scrollHeight,
        clientH: d.clientHeight || Math.round(innerHeight),
        scrollY: Math.round(scrollY),
        footerTop: f ? Math.round(f.getBoundingClientRect().top) : null,
    };
}"""

FRACTIONS = (0.5, 0.35, 0.65, 0.25, 0.75, 0.9, 0.12)


def pages():
    out = subprocess.run(["git", "-C", SITE, "ls-tree", "-r", "--name-only", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.split()
    return [p for p in out if p.endswith(".html")]


def offer_base():
    src = open(os.path.join(SITE, "js", "scripts.js")).read()
    m = re.search(r"OFFER_BASE:\s*'([^']+)'", src)
    assert m, "no OFFER_BASE constant in js/scripts.js"
    return m.group(1)


def drive(pg):
    """Walk the scrollable range; return the first probe where the bar is visible."""
    best = None
    for f in FRACTIONS:
        pg.evaluate("""(f) => { const d = document.documentElement;
            window.scrollTo(0, Math.round(f * (d.scrollHeight - d.clientHeight))); }""", f)
        pg.wait_for_timeout(280)
        r = pg.evaluate(PROBE)
        if best is None or (best["docH"] < r["docH"]):
            best = r
        if r["visible"]:
            return r, f
    return best, None


def main():
    base = offer_base()
    rows, anomalies = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in pages():
            ctx = b.new_context(viewport={"width": 390, "height": 844},
                                has_touch=True, is_mobile=True)
            pg = ctx.new_page()
            try:
                pg.goto(BASE_URL + "/" + p, wait_until="networkidle", timeout=30000)
            except Exception as e:
                anomalies.append(f"{p}: LOAD FAILED {type(e).__name__}")
                ctx.close()
                continue
            r, f = drive(pg)
            ctx.close()
            row = {"p": p, "visible": r["visible"], "f": f}
            if not r["visible"]:
                row.update(docH=r["docH"], clientH=r["clientH"], footerTop=r["footerTop"])
                rows.append(row)
                if r["docH"] - r["clientH"] > 700:
                    anomalies.append(f"{p}: long enough to trigger "
                                     f"(scrollable {r['docH'] - r['clientH']}px) but no bar at any position")
                continue
            href, tid = r["href"], None
            q = href.count("?")
            if href.startswith(base + "?tid="):
                tid = href[len(base + "?tid="):]
            scheme = re.sub(r"^https?://", "", href)
            problems = []
            if not href.startswith(base + "?tid="):
                problems.append(f"href is not OFFER_BASE + '?tid=': {href}")
            if q != 1:
                problems.append(f"{q} '?' characters")
            if "//" in scheme:
                problems.append(f"double slash after the scheme: {scheme}")
            if not tid or not re.fullmatch(r"sticky_[a-z]+", tid or ""):
                problems.append(f"tid not a sticky_* token: {tid!r}")
            if r["ownPrefixes"]:
                bad = [x for x in r["ownPrefixes"] if x.rstrip("/") != base.rstrip("/")]
                if bad:
                    problems.append(f"page's own hop differs from the bar's: {bad[0]}")
            elif r["ownPrefixes"] == []:
                row["noPageAffiliate"] = True
            rel = set((r["rel"] or "").split())
            for need in ("noopener", "noreferrer", "sponsored"):
                if need not in rel:
                    problems.append(f"rel missing {need}: {r['rel']!r}")
            if r["target"] != "_blank":
                problems.append(f"target={r['target']!r}")
            if not r["disclosure"] or "affiliate" not in r["disclosure"].lower():
                problems.append(f"disclosure label: {r['disclosure']!r}")
            row.update(tid=tid, href=href, rel=r["rel"], target=r["target"],
                       own=len(r["ownPrefixes"]), disclosure=r["disclosure"],
                       problems=problems)
            rows.append(row)
            if problems:
                anomalies.append(f"{p}: " + "; ".join(problems))

    shown = [r for r in rows if r.get("visible")]
    hidden = [r for r in rows if not r.get("visible")]
    tids = {}
    for r in shown:
        tids[r["tid"]] = tids.get(r["tid"], 0) + 1
    with_anchor = [r for r in shown if r.get("own")]
    no_anchor = [r for r in shown if r.get("noPageAffiliate")]

    lines = [
        "# Is the bar's CTA the same affiliate link the page itself already uses?",
        f"# generated by: offer-link.py {BASE_URL}   (live DOM, chromium, 390x844 mobile, :8199 working tree)",
        f"# CONFIG.OFFER_BASE parsed from js/scripts.js: {base}",
        "# The bar's href is not graded against a hard-coded 'right answer'; it is graded against",
        "# the hop the anchors on that same page point at, so the site's own links are the spec.",
        "# The scroll driver walks fractions of the scrollable range and stops where the bar is",
        "# visible, because the module hides it when the footer is in view (see this file's docstring).",
        "",
        f"pages checked: {len(rows)}",
        f"bar rendered: {len(shown)}   not rendered: {len(hidden)}",
        f"bar href == OFFER_BASE + '?tid=' + one sticky_* token: "
        f"{len(shown) - len([r for r in shown if r['problems']])} of {len(shown)}",
        f"pages that also carry their own clickbank anchors: {len(with_anchor)} "
        f"- of those, identical hop to the bar's: "
        f"{len([r for r in shown if r.get('own') and not r['problems']])}",
        f"pages showing the bar while carrying no affiliate link of their own: {len(no_anchor)}",
        f"distinct tids emitted: {len(tids)}  " + " ".join(f"{k}={v}" for k, v in sorted(tids.items())),
        f"rel on every CTA: {sorted({r['rel'] for r in shown})}",
        f"target on every CTA: {sorted({r['target'] for r in shown})}",
        f"disclosure on every CTA: {sorted({r['disclosure'] for r in shown})}",
        "",
    ]
    if no_anchor:
        lines.append("showing the offer with no page-level affiliate link of their own:")
        lines += [f"  {r['p']}  tid={r['tid']}" for r in no_anchor]
        lines.append("")
    if hidden:
        lines.append("no bar at any scroll position (expected only where the page cannot reach the 700px trigger):")
        lines += [f"  {r['p']}  docH={r['docH']} clientH={r['clientH']} footerTop={r['footerTop']}" for r in hidden]
        lines.append("")
    lines.append("anomalies:")
    lines += [f"  {a}" for a in anomalies] or ["  none"]
    lines.append("")
    lines.append("verdict: " + ("the bar's CTA is the page's own affiliate link on every rendering page"
                                if not anomalies else f"{len(anomalies)} anomaly(ies) - read them before shipping"))
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[:14]))
    print("\n".join(lines[-8:]))
    return 1 if anomalies else 0


if __name__ == "__main__":
    sys.exit(main())
