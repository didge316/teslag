#!/usr/bin/env python3
"""
Click the bar's CTA and see which URL actually leaves the page.

`js/redirect-leave.js` rewrites outbound clicks to the offer under
`?tid=leave_redirect`. It exempts `clickbank.net`, and the bar's CTA host is
`d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net`, so on paper the bar keeps its own
`sticky_*` attribution. That is a reading of a skip list, and a reading of a skip list is
exactly what offer-link.py exists to distrust - it would also be satisfied by the
interceptor being dead, by the listener losing the race, or by the exemption matching on
something other than the hostname.

So the control is the point: the same run clicks a non-clickbank external link on the same
page, and that one *must* be rewritten to `tid=leave_redirect`. If the control shows the
rewrite firing and the bar's click still carries `sticky_article`, the bar's exemption is
proven to be the skip list rather than an absence of interception. If the control shows
nothing either, this run says nothing and has to be re-made to say something.

The offer hosts are aborted by route interception, so the hop and the vendor landing page
are recorded as attempts and never fetched - a claim this file made before the interception
existed, which is why the counter is printed and not just the sentence. `target=_blank`
means the real click opens a new tab, so popups are captured as pages on the context
rather than assumed away; a top-level navigation attempt is captured as a separate
signal, because `redirect-leave.js` navigates the current tab and that is the difference
between the reader losing the article and not losing it.

Run: python3 offer-click.py [base-url]   (needs :8199, the working-tree server)
"""
import os
import re
import sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "offer-click-2026-11-19.txt")
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8199"
SITE_HOST = "127.0.0.1"
SKIP = ("clickbank.net", "eocampaign1.com", "emailoctopus.com", "cdn.jsdelivr.net",
        "teslamagneticgenerator.com", SITE_HOST)

# The module's rule is show = pastThreshold && !footerVisible; walk fractions until it is
# visible rather than trusting one scroll (see offer-link.py's docstring for the mistake
# this replaces).
FRACTIONS = (0.5, 0.35, 0.65, 0.25, 0.75, 0.9, 0.12)


ABORTED = []
OFFER_HOSTS = ("clickbank.net", "ultimateoffgridgenerator.net")


def _gate(route):
    host = route.request.url.split("/")[2]
    if any(host == h or host.endswith("." + h) for h in OFFER_HOSTS):
        ABORTED.append(route.request.url)
        route.abort()
    else:
        route.continue_()


def show_bar(pg):
    for f in FRACTIONS:
        pg.evaluate("""(f) => { const d = document.documentElement;
            window.scrollTo(0, Math.round(f * (d.scrollHeight - d.clientHeight))); }""", f)
        pg.wait_for_timeout(280)
        if pg.evaluate("() => { const b = document.querySelector('.tmg-cta-bar');"
                       "return !!b && b.classList.contains('is-visible'); }"):
            return True
    return False


def run_case(pg, ctx, sel, label, hits, navs, pops):
    """Click whatever `sel` matches and record where the click actually went."""
    box = pg.locator(sel).first
    box.scroll_into_view_if_needed()
    pg.wait_for_timeout(150)
    before = pg.evaluate("() => location.href")
    # A popup is what a `target=_blank` CTA produces; redirect-leave.js instead
    # preventDefault()s and navigates the current tab, so a missing popup is a result and
    # not an error - the first version of this function required one and died on the
    # control case, which is the exact click it was there to observe.
    pop = None
    try:
        with ctx.expect_event("page", timeout=2500) as popinfo:
            box.click(timeout=2500)
        pop = popinfo.value
    except Exception:
        pop = None
    if pop is not None:
        try:
            pop.wait_for_load_state("domcontentloaded", timeout=2500)
        except Exception:
            pass
        pops.append((label, pop.url))
    pg.wait_for_timeout(600)
    try:
        after = pg.evaluate("() => location.href")
    except Exception as e:
        after = f"(page unreadable after click: {type(e).__name__})"
    if after != before:
        navs.append((label, after))
    return pg.evaluate("(s) => { const a = document.querySelector(s); return a ? {href: a.href, rel: a.getAttribute('rel'), target: a.getAttribute('target')} : null; }", sel)


def control_page():
    """Pick a page that can actually prove the rewriter is armed.

    /whole-house.html turned out to have no non-clickbank external anchor at all, so the
    first run of this probe was inconclusive for a reason that had nothing to do with the
    bar - the control click never happened. Rather than guess a page, derive one: a
    tracked page that (a) loads redirect-leave.js and (b) carries an https anchor to a
    host the skip list does not exempt.
    """
    import subprocess
    files = subprocess.run(["git", "-C", os.path.abspath(os.path.join(HERE, "..", "..")),
                            "grep", "-l", "redirect-leave.js", "--", "*.html"],
                           capture_output=True, text=True).stdout.split()
    for f in files:
        src = open(os.path.join(os.path.abspath(os.path.join(HERE, "..", "..")), f)).read()
        for m in re.finditer(r'href="https://([^/"\']+)', src):
            h = m.group(1)
            if not any(h == s or h.endswith("." + s) for s in SKIP):
                return f
    raise SystemExit("no page carries both redirect-leave.js and a non-exempt external link")


def main():
    hits, navs, pops, requests = [], [], [], []
    rows = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 390, "height": 844},
                            has_touch=True, is_mobile=True)
        ctx.on("request", lambda r: requests.append(r.url) if "clickbank" in r.url else None)
        # Abort the offer hosts for real. This file claimed "nothing left this box" before
        # this line existed, and the claim was false: the first run fetched the hop and the
        # vendor landing page over the network. Recording is not blocking.
        ctx.route("**/*", _gate)

        pg = ctx.new_page()
        pg.goto(BASE_URL + "/whole-house.html", wait_until="networkidle")
        assert show_bar(pg), "bar never showed on /whole-house.html; instrument is wrong"
        anchor = run_case(pg, ctx, ".tmg-cta-btn", "bar-cta", hits, navs, pops)
        rows.append(("bar CTA anchor", anchor))

        # Control: the same page's own non-clickbank external link. redirect-leave.js
        # MUST rewrite this one, or the bar's clean result proves nothing.
        cpage = control_page()
        pg2 = ctx.new_page()
        pg2.goto(BASE_URL + "/" + cpage, wait_until="networkidle")
        ctrl = pg2.evaluate("""(skip) => {
            const a = [...document.querySelectorAll('a[href^="https://"]')].find(x => {
                const h = new URL(x.href).hostname;
                return !skip.some(s => h === s || h.endsWith('.' + s));
            });
            if (!a) return null;
            a.setAttribute('data-ctrl', '1');
            return {href: a.href, host: new URL(a.href).hostname, page: location.pathname};
        }""", list(SKIP))
        if ctrl:
            run_case(pg2, ctx, 'a[data-ctrl="1"]', "control-external", hits, navs, pops)

        # Third leg: the page's own clickbank anchor, to show a site link behaves the same
        pg3 = ctx.new_page()
        pg3.goto(BASE_URL + "/whole-house.html", wait_until="networkidle")
        pg3.evaluate("""() => { const a = [...document.querySelectorAll('a[href*="hop.clickbank.net"]')]
                .find(x => !x.classList.contains('tmg-cta-btn')); if (a) a.setAttribute('data-site','1'); }""")
        if pg3.locator('a[data-site="1"]').count():
            run_case(pg3, ctx, 'a[data-site="1"]', "site-own-clickbank", hits, navs, pops)

        b.close()

    bar_reqs = [u for u, lab in pops if lab == "bar-cta"] + [
        u for u in requests if "tid=sticky_" in u]
    ctrl_reqs = [u for u in requests if "tid=leave_redirect" in u]
    lines = [
        "# Where does a click on the bar's CTA actually go?",
        f"# generated by: offer-click.py {BASE_URL}  (chromium 390x844 mobile, :8199 working tree)",
        f"# the offer hosts ({', '.join(OFFER_HOSTS)}) are route-aborted: {len(ABORTED)} request(s) blocked,"
        f"# so no click-through left this box; the hop and vendor pages below are the URLs the browser"
        f"# attempted, never bytes it received.",
        "# redirect-leave.js rewrites external clicks to ?tid=leave_redirect but exempts clickbank.net;",
        "# the control click on a non-clickbank link proves the rewriter is alive, so the bar's clean",
        "# result is the exemption and not an absence of interception.",
        "",
        f"bar CTA anchor: {rows[0][1]}",
        f"bar CTA request(s): {sorted(set(u for u in requests if 'tid=sticky_' in u)) or 'NONE RECORDED'}",
        f"site's own clickbank CTA request(s): "
        f"{sorted(set(u for u in requests if re.search(r'tid=(?!sticky_|leave_redirect)[a-z0-9_]+', u))) or 'none'}",
        f"control page: {ctrl['page'] if ctrl else 'NONE FOUND'} -> "
        f"{ctrl['href'] if ctrl else 'no non-exempt external anchor on any page'}",
        f"leave_redirect requests (the control's rewrite): {len(ctrl_reqs)} {sorted(set(ctrl_reqs))[:1]}",
        "# `chrome-error://chromewebdata/` below is what an aborted navigation lands on, and it is",
        "# expected: the navigation was attempted and blocked on purpose. The tid each click attempted",
        "# is in 'tids requested, live', which is what is actually being graded here.",
        f"new tabs opened by clicks: {[(l, u) for l, u in pops]}",
        f"top-level navigations away from the article: {[(l, u) for l, u in navs] or 'none'}",
        f"all clickbank requests seen: {len(requests)}",
        "",
    ]
    seen = {}
    for u in requests:
        m = re.search(r"tid=([A-Za-z0-9_]+)", u)
        seen[m.group(1) if m else "?"] = seen.get(m.group(1) if m else "?", 0) + 1
    lines.append("tids requested, live: " + " ".join(f"{k}={v}" for k, v in sorted(seen.items())))
    ok_bar = any("tid=sticky_" in u for u in requests)
    ok_ctrl = len(ctrl_reqs) > 0
    lines += [
        "",
        f"bar click carried its own sticky_* tid: {ok_bar}",
        f"control (non-clickbank) click was rewritten to leave_redirect: {ok_ctrl}",
        f"bar click was itself rewritten to leave_redirect: "
        f"{any('tid=sticky_' not in u and 'leave_redirect' in u for u in bar_reqs)}",
        "",
        "verdict: " + ("PASS - the bar's CTA reaches ClickBank with its own tid, and the rewriter is demonstrably armed"
                       if ok_bar and ok_ctrl else
                       "INCONCLUSIVE - control did not fire" if ok_bar and not ok_ctrl else
                       "FAIL - the bar's click did not carry its own tid"),
    ]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if "PASS" in lines[-1] else 1


if __name__ == "__main__":
    sys.exit(main())
