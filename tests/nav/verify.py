#!/usr/bin/env python3
"""Does the new navbar actually work, measured in a browser?

inventory.py proves the structure (group sizes, hrefs resolve, orphan set).
This proves the interaction, on the three things a nav restructure can break:

  1. touch - at 390px the whole menu lives in the collapse drawer. The toggler
     must open it, every entry must be >=44px tall (WCAG 2.5.5 / 2.5.8 target
     size), nothing may hang past the layout viewport and the page must not
     scroll sideways. Dropdowns inside a collapsed Bootstrap navbar reveal
     inline rather than as a floating menu, so each of the three groups is
     opened and measured too.
  2. keyboard - Bootstrap 4 menus were click-only and unusable with a keyboard.
     This site is Bootstrap 5.2.3, so Tab to a toggle, Enter to open, ArrowDown
     to move into the menu and Enter to follow must all work. The same pass asserts
     `aria-expanded` / `aria-haspopup` on the toggle itself, closed and open: that
     attribute pair is the state a screen reader announces, so a hand-styled menu or
     a dropped attribute would leave something that works in a screenshot and lies to
     everyone else. If a future edit
     swaps in a CSS :hover reveal, that breaks touch first and this check
     second, because it drives the real plugin rather than CSS.
  3. desktop width - the old bar carried one dropdown, the new one carries
     three. At the exact lg breakpoint (992px) the row has just 968px inside
     the container, minus the brand, so this measures the nav row at
     992/1024/1280 instead of hoping the labels are short enough.

Narrow/responsive desktop windows, no mobile emulation (PLAN §1).

Usage: python3 verify.py [base-url]        # needs the stage server on :8199
"""
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8199")
# The drawer is measured at 390 by default; 320 is the WCAG 1.4.10 width and the
# place long dropdown labels are most likely to be clipped, so run it twice:
#   DRAWER_W=320 python3 tests/nav/verify.py
import os
DRAWER_W = int(os.environ.get("DRAWER_W", "390"))
# The drawer and the nav row are measured at 100%, 200% and 300% root font, not
# at 16px only. The reason is not thoroughness for its own sake: the fix that made
# the drawer usable is written in rem (`white-space: normal`, 0.75rem of block
# padding), so at 300% those are 24px of padding under 24px type. "Every item is
# at least 44px tall" measured at one size is a claim about a page nobody at that
# zoom is reading - and the overflow gate already caught item 6 regressing item 7
# at 1280x32/48, which is the same interaction seen from the other side.
FONTS = tuple(int(x) for x in os.environ.get("FONTS", "16,32,48").split(","))
PAGE = "index"
fails = []


def check(ok, label, *detail):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  [{', '.join(map(str, detail))}]" if detail else ""))
    if not ok:
        fails.append(label)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()

        def open_page(width, height, font=16):
            """Context + page navigated with the root font already in the document.

            The only way that has been measured to work: a style tag added before
            navigation does not survive it, and one added after load lays the page
            out twice (tests/overflow/gate.py documents both, expensively). The
            root font is then read back off the page, because an instrument that
            asks for 48px and gets 16px reports green about nothing.
            """
            ctx = b.new_context(viewport={"width": width, "height": height})
            inject = (f"<style>html{{font-size:{font}px !important}}"
                      f"/* verify.py root font */</style>")

            def serve(route):
                resp = route.fetch()
                body = resp.text()
                route.fulfill(status=resp.status,
                              headers={"content-type": "text/html; charset=utf-8"},
                              body=body.replace("</head>", inject + "</head>", 1))

            ctx.route("**/*.html", serve)
            pg = ctx.new_page()
            pg.goto(f"{BASE}/{PAGE}.html", wait_until="load", timeout=60000)
            got = pg.evaluate("() => getComputedStyle(document.documentElement).fontSize")
            if got != f"{font}px":
                sys.exit(f"INSTRUMENT FAILED: asked for root {font}px at {width}px wide, "
                         f"the page reports {got}. No results.")
            return ctx, pg

        # --- structure: dropdown sizes straight from the DOM -----------------
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        pg.goto(f"{BASE}/{PAGE}.html", wait_until="load")
        sizes = pg.eval_on_selector_all(
            "nav .dropdown-menu", "els => els.map(e => e.querySelectorAll('a').length)")
        print("== structure ==")
        check(bool(sizes) and all(s <= 10 for s in sizes), "every dropdown <=10 items", sizes)
        hrefs = pg.eval_on_selector_all(
            "nav a[href]",
            "els => els.filter(e => e.getAttribute('role') !== 'button')"
                       "         .map(e => e.getAttribute('href'))")
        dupes = {h for h in hrefs if hrefs.count(h) > 1 and h != "/"}
        check(not dupes, "no duplicate href in the nav (brand->/ excepted)", sorted(dupes))
        # The three dropdown toggles are href="#" with role="button", which is
        # Bootstrap 5.2's own navbar example, and they are deliberately not
        # counted above: the point of this check is that two real links do not
        # collide, and a button that happens to live on an <a> is not a
        # destination. verify's keyboard section drives those toggles through the
        # real plugin instead of trusting the href, which is the thing that could
        # actually rot.

        # --- 3. desktop: the nav row must fit at and above the lg breakpoint --
        for font in FONTS:
            print(f"== desktop row width, root font {font}px (992 is the collapse breakpoint) ==")
            for w in (992, 1024, 1280):
                ctx, pg = open_page(w, 900, font)
                d = pg.evaluate("""() => {
                  const nav = document.querySelector('nav .container');
                  const links = [...document.querySelectorAll('nav .navbar-nav > li')];
                  const row = document.querySelector('nav .navbar-nav');
                  return {scrollW: nav.scrollWidth, clientW: nav.clientWidth,
                          rowRight: Math.round(row.getBoundingClientRect().right),
                          brandW: Math.round(document.querySelector('.navbar-brand').getBoundingClientRect().width),
                          rowW: Math.round(row.getBoundingClientRect().width),
                          wrapped: links.length > 1 && Math.abs(links[0].getBoundingClientRect().top - links[links.length-1].getBoundingClientRect().top) > 4,
                          toggler: getComputedStyle(document.querySelector('.navbar-toggler')).display};
                }""")
                # At 100% the row must fit on one line: a nav that wraps at 16px is
                # a regression this change introduced. Above 100% wrapping is the
                # fix, so what is asserted there is only that it never overflows.
                if font == 16:
                    check(d["scrollW"] <= d["clientW"] + 1 and d["toggler"] == "none"
                          and not d["wrapped"],
                          f"nav fits at {w}px: one row, no sideways scroll, toggler hidden", d)
                else:
                    check(d["scrollW"] <= d["clientW"] + 1 and d["toggler"] == "none",
                          f"nav fits at {w}px root {font}px: no sideways scroll, toggler hidden",
                          f"wrapped={d['wrapped']} rowW={d['rowW']} brandW={d['brandW']}")
                pg.close(); ctx.close()

        # --- 3b. open desktop dropdowns at and above the breakpoint -----------
        # A closed menu is what the overflow gate measures, and an absolutely
        # positioned menu that hangs off the right edge does not move
        # documentElement.scrollWidth either, so nothing else in the suite could
        # see this: at a 32px root the three menus are 574/521/478px wide and the
        # third starts at x=825 in a 1280px viewport, putting part of every label
        # off screen with no scrollbar to reach it.
        #
        # At 16px this is asserted (it is green and must stay green). At 32/48 the
        # rules in styles-custom.css shrink the menus by letting their labels wrap,
        # which is a large improvement but does not close it - CSS cannot know
        # where the toggle sits, and the fix that would (Popper's viewport
        # boundary, already shipped inside bootstrap.bundle) is a JS change to the
        # nav rather than a stylesheet, so it is an owner decision. Those lines are
        # printed as FAIL-KNOWN and deliberately do not count towards the exit
        # code: a gap that only exists as a paragraph in a commit message is a gap
        # that will not survive the commit.
        for font in FONTS:
            worst = []
            for w in (992, 1280):
                ctx, pg = open_page(w, 900, font)
                n = pg.locator("nav .dropdown-toggle").count()
                for i in range(n):
                    pg.locator("nav .dropdown-toggle").nth(i).click()
                    pg.wait_for_timeout(250)
                    m = pg.eval_on_selector_all(
                        "nav .dropdown-menu",
                        """(els,i) => { const r = els[i].getBoundingClientRect();
                           return {w: Math.round(r.width), L: Math.round(r.left),
                                   R: Math.round(r.right)}; }""", i)
                    m["vw"] = w
                    worst.append(m)
                    pg.locator("nav .dropdown-toggle").nth(i).click()
                    pg.wait_for_timeout(150)
                pg.close(); ctx.close()
            bad = [m for m in worst if m["R"] > m["vw"] + 1 or m["L"] < -1]
            label = f"open desktop menus inside the viewport, root {font}px"
            if font == 16:
                check(not bad, label, [[m["w"], m["L"], m["R"], m["vw"]] for m in bad][:3])
            elif bad:
                over = max(m["R"] - m["vw"] for m in bad)
                print(f"  FAIL-KNOWN  {label}: {len(bad)} of {len(worst)} menus past the edge, "
                      f"worst +{over}px {sorted({(m['vw'], m['w']) for m in bad})[:4]}")
            else:
                print(f"  PASS-EXTRA  {label}")

        # --- 1. touch: the drawer at DRAWER_W, at every root font in FONTS -----
        for font in FONTS:
            ctx, pg = open_page(DRAWER_W, 844, font)
            print(f"== touch drawer at {DRAWER_W}px, root font {font}px ==")
            closed = pg.eval_on_selector("#navbarSupportedContent", "e => getComputedStyle(e).display")
            check(closed == "none", "drawer starts closed", closed)
            pg.click(".navbar-toggler")
            pg.wait_for_selector("#navbarSupportedContent", state="visible")
            opened = pg.eval_on_selector("#navbarSupportedContent", "e => getComputedStyle(e).display")
            check(opened != "none", "toggler opens the drawer", opened)
            m = pg.evaluate("""() => {
              const vw = document.documentElement.clientWidth;
              const links = [...document.querySelectorAll('#navbarSupportedContent a')]
                            // A closed .dropdown-menu is display:none, so its ten
                            // items measure 0px tall and would fail a target-size
                            // check they cannot answer. Each group is opened and
                            // measured on its own below; this pass measures only
                            // what is actually rendered right now.
                            .filter(a => a.getBoundingClientRect().height > 0);
              const small = links.filter(a => a.getBoundingClientRect().height < 44)
                                 .map(a => a.textContent.trim().slice(0, 24) + ':' + Math.round(a.getBoundingClientRect().height));
              const wide = links.filter(a => a.getBoundingClientRect().right > vw + 1)
                                .map(a => a.textContent.trim().slice(0, 24));
              return {n: links.length, small, wide,
                      scrollW: document.documentElement.scrollWidth, clientW: vw};
            }""")
            check(not m["small"], "every drawer link >=44px tall", m["small"][:4])
            check(not m["wide"], "no drawer link past the layout viewport", m["wide"][:4])
            check(m["scrollW"] <= m["clientW"] + 1, "no horizontal scroll with the drawer open",
                  f"scrollW={m['scrollW']} clientW={m['clientW']}")
            for i in range(3):
                tog = pg.locator("#navbarSupportedContent .dropdown-toggle").nth(i)
                tog.click()
                pg.wait_for_timeout(250)
                st = pg.evaluate("""(i) => {
                  const m = document.querySelectorAll('#navbarSupportedContent .dropdown-menu')[i];
                  const cs = getComputedStyle(m);
                  const links = [...m.querySelectorAll('a')];
                  const vw = document.documentElement.clientWidth;
                  return {shown: cs.display !== 'none', pos: cs.position,
                          items: links.length,
                          small: links.filter(a => a.getBoundingClientRect().height < 44).length,
                          wide: links.filter(a => a.getBoundingClientRect().right > vw + 1).map(a => a.textContent.trim().slice(0, 20)),
                          scrollW: document.documentElement.scrollWidth, clientW: vw};
                }""", i)
                label = pg.locator("#navbarSupportedContent .dropdown-toggle").nth(i).inner_text().strip()
                check(st["shown"], f"dropdown '{label}' opens on tap in the drawer", f"pos={st['pos']}")
                check(not st["small"], f"dropdown '{label}': all {st['items']} items >=44px tall", st["small"])
                check(not st["wide"] and st["scrollW"] <= st["clientW"] + 1,
                      f"dropdown '{label}': nothing past the viewport", st["wide"][:3])
            pg.close(); ctx.close()

        # --- 2. keyboard at 1280px -------------------------------------------
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        pg.goto(f"{BASE}/{PAGE}.html", wait_until="load")
        print("== keyboard at 1280px (Bootstrap 5.2.3 dropdown plugin) ==")
        n = pg.locator("nav .dropdown-toggle").count()
        for i in range(n):
            pg.goto(f"{BASE}/{PAGE}.html", wait_until="load")
            tog = pg.locator("nav .dropdown-toggle").nth(i)
            label = tog.inner_text().strip()
            tog.focus()
            # The announced state, not just the rendered one: `aria-expanded` is what
            # a screen reader says when the button is pressed, and Bootstrap's plugin
            # maintains it - which means a future edit that styled the menu by hand,
            # or a template that dropped the attribute, would leave a menu that works
            # for sighted users and lies to everyone else. Asserted closed and open,
            # on the element itself, not inferred from the menu being visible.
            exp0, pop0 = tog.get_attribute("aria-expanded"), tog.get_attribute("aria-haspopup")
            check(exp0 == "false" and pop0 == "true",
                  f"'{label}': announces aria-expanded=false, aria-haspopup=true while closed",
                  f"expanded={exp0} haspopup={pop0}")
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(250)
            exp1 = tog.get_attribute("aria-expanded")
            check(exp1 == "true",
                  f"'{label}': aria-expanded flips to true while open (the state a screen "
                  f"reader announces, not the state a screenshot shows)", f"expanded={exp1}")
            shown = pg.eval_on_selector_all(
                "nav .dropdown-menu",
                f"(els,i) => getComputedStyle(els[i]).display !== 'none'", i)
            check(shown, f"'{label}': Enter on the focused toggle opens it")
            pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(150)
            act = pg.evaluate("() => document.activeElement.tagName + ':' + document.activeElement.textContent.trim().slice(0,22)")
            check(act.startswith("A:") and pg.evaluate("document.activeElement.closest('.dropdown-menu') !== null"),
                  f"'{label}': ArrowDown moves focus to the first item", act)
            href = pg.evaluate("document.activeElement.getAttribute('href')")
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(600)
            check(pg.url.endswith(href.rstrip('/')) or pg.url == BASE + href,
                  f"'{label}': Enter follows the focused item", f"{href} -> {pg.url}")
            pg.keyboard.press("Escape")
        pg.close(); ctx.close()
        b.close()

    print(f"\n{len(fails)} failed" if fails else "\nall nav interaction checks green")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
