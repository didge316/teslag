#!/usr/bin/env python3
"""Can a comment actually be read at 300% root font, or has it merely stopped scrolling?

gate.py answers "does the page scroll sideways". That is a different claim from
"is the text usable", and at 390px with a 48px root font the two come apart on the
comment sections: `min-width: 0` on .d-flex > .ms-3 stops the page scrolling by
letting the column get very narrow, and a narrow column is exactly where "no
scroll" and "readable" part company.

So measure the column rather than argue about it. For the first comment rows of a
page, at three root fonts:

  col      the width the comment body actually got
  lines    how many line boxes its first paragraph set (Range.getClientRects)
  chars    characters per line, which is the number a screen is judged by
  wide     words whose own measured width exceeds the column, i.e. words that
           MUST be broken mid-word for the column to hold - the failure mode a
           human notices first

Then the same numbers with one rule injected: `.d-flex:has(> .ms-3) { flex-wrap:
wrap }`, the suggestion on the table for making 300% comments readable (avatar on
its own line, comment body across the full width). It is cheap to test and it has
a failure mode of its own worth catching before it goes anywhere near the
stylesheet: flex items size by content, so a text column is enormous before
anything shrinks it, and a wrap rule may therefore break the row apart at 100%
root font too - which would change the site's normal look, the one thing this
change promised not to do.

Usage: python3 comment-row.py [page] [--widths 390,320] [--roots 16,32,48]
"""
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8199"

JS = """(needle) => {
  const rows = [...document.querySelectorAll('.d-flex')].filter(r => r.querySelector(':scope > .ms-3'));
  const probe = document.createElement('span');
  probe.style.cssText = 'position:absolute;left:-9999px;top:0;white-space:nowrap';
  document.body.appendChild(probe);
  const cs = getComputedStyle(document.body);
  probe.style.font = cs.font;
  const out = rows.slice(0, needle).map(row => {
    const col = row.querySelector(':scope > .ms-3');
    const r = col.getBoundingClientRect();
    const p = col.querySelector('p') || col;
    const range = document.createRange();
    range.selectNodeContents(p);
    const rects = [...range.getClientRects()].filter(x => x.width > 1);
    const text = (p.textContent || '').replace(/\\s+/g, ' ').trim();
    const words = text.split(' ').filter(Boolean);
    let wide = 0, longest = '';
    for (const w of words) {
      probe.textContent = w;
      const wd = probe.getBoundingClientRect().width;
      if (wd > r.width + 0.5) { wide++; if (w.length > longest.length) longest = w; }
    }
    const av = row.querySelector(':scope > img, :scope > .avatar');
    return {
      rowW: Math.round(row.getBoundingClientRect().width),
      colW: Math.round(r.width), colX: Math.round(r.x),
      avatar: av ? Math.round(av.getBoundingClientRect().width) : null,
      lines: rects.length,
      chars: rects.length ? Math.round(text.length / rects.length) : 0,
      wide, longest: longest.slice(0, 24),
      // how the column's own font-size and the row's gap scale with the root font
      fs: Math.round(parseFloat(getComputedStyle(p).fontSize) * 10) / 10,
      gap: getComputedStyle(col).marginLeft,
    };
  });
  probe.remove();
  return out;
}"""


def main():
    args = sys.argv[1:]
    page = next((a for a in args if not a.startswith("--")), "tesla-magnetic-generator-worth-it")
    widths = [390, 320]
    roots = [16, 32, 48]
    if "--widths" in args:
        widths = [int(x) for x in args[args.index("--widths") + 1].split(",")]
    if "--roots" in args:
        roots = [int(x) for x in args[args.index("--roots") + 1].split(",")]

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for variant in ("shipped CSS", "+ .d-flex:has(> .ms-3){flex-wrap:wrap}"):
            print(f"\n=== /{page} - {variant} ===")
            for w in widths:
                pg = b.new_context(viewport={"width": w, "height": 900}).new_page()
                if variant.startswith("+"):
                    pg.add_init_script("""(() => {
                        const add = () => { const s = document.createElement('style');
                          s.textContent = '.d-flex:has(> .ms-3){flex-wrap:wrap}';
                          document.head.appendChild(s); };
                        document.readyState === 'loading'
                          ? document.addEventListener('DOMContentLoaded', add) : add();
                    })()""")
                for font in roots:
                    pg.goto(f"{BASE}/{page}.html", wait_until="load", timeout=30000)
                    if font != 16:
                        pg.add_style_tag(content=f":root{{font-size:{font}px !important}}")
                    pg.wait_for_timeout(200)
                    rows = pg.evaluate(JS, 3)
                    if not rows:
                        print(f"  {w}px root {font}px: no comment rows on this page")
                        continue
                    for i, r in enumerate(rows):
                        print(f"  {w}px root {font}px  row{i}: row {r['rowW']:4}  avatar {str(r['avatar']):>4} "
                              f"gap {r['gap']:>6}  column {r['colW']:4} at x{r['colX']:4}  "
                              f"text {r['fs']}px  {r['lines']:3} lines  ~{r['chars']:3} chars/line  "
                              f"{r['wide']:3} words too wide{' (' + r['longest'] + ')' if r['wide'] else ''}")
                pg.context.close()
        b.close()


if __name__ == "__main__":
    main()
