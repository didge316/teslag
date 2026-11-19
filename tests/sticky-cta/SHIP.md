# Shipping the mobile sticky offer bar

The bar is **JS + CSS only**. It is built at runtime by `js/scripts.js` and styled by the
appended block in `css/styles-custom.css`. No HTML file contains it, so it never enters crawled
HTML and a revert is two appended blocks, not a diff across 53 pages.

`404.html` does not load `scripts.js`, so the bar does not appear there.

## The design, in the two lines that matter

1. Every size in the bar is **capped in CSS**, so its rendered height is fixed per breakpoint and
   the reserved space is a CSS constant. It used to be sized in rem, which meant the site's own
   text-size control (`wp-textsize` sets the root font) could inflate it from 87px to 270px, and the
   bar shed content in JS tiers driven by a **measured viewport budget**.
2. If an engine renders the bar taller than the constant, `growPad()` only ever **grows** the
   reservation, measuring `bar.offsetHeight` — the bar itself, never the viewport.

That restructure exists because there is no iPhone and no Mac on this box. The old design made
correctness depend on `documentElement.clientHeight` staying pinned while iOS Safari's
`innerHeight` swings ~110px with the toolbar — a published behaviour, never measured here, and not
measurable here. Rather than ship something whose safety rests on a number nobody can check, the
dependency was deleted. The only viewport reading left decides a show/hide, where a wrong answer
costs a few dozen pixels of early hiding, never covered content.

## The gates, in order

```bash
# 0. stage server
cd website && python3 -m http.server 8199 --bind 127.0.0.1

# 1. local suite, all three engines - green before any commit
cd website/tests/sticky-cta
python3 run.py                      # chromium (default)
python3 run.py --engine webkit      # the closest instrument to iOS available here
python3 run.py --engine firefox
python3 engines.py                  # 27 cases x 3 engines: height, reservation, reach

# 2. preview deploy - green before merge
./live.sh https://<hash>.<project>.pages.dev

# 3. production - the feature is only "shipped" once this is green
./live.sh https://teslamagneticgenerator.com
```

`run.py` prints **BASELINE DRIFT** with a diff of every changed number rather than only pass/fail.
Baselines are per engine (`baseline.json`, `baseline.webkit.json`, `baseline.firefox.json`) and are
**never comparable across engines** — Firefox is 18px taller than Chromium at the same viewport,
legitimately. A green suite with drift is a change in behaviour; read it, do not wave it through.

Section 10 (LAYOUT_TRACE) is Chromium-only — `Performance.getMetrics` is a CDP call — and prints
`SKIP` elsewhere rather than pretending to have run.

## Why three engines, when the target is an iPhone

Chromium found nothing that Firefox did not find, and Firefox found a real bug in minutes: at a
390px viewport the bar's title fits on one line in Chromium and WebKit (**87px** tall) and wraps to
two in Firefox's DejaVu fallback (**105px**). The CSS constant reserved 92px, so on Firefox the bar
sat **18px on top of real content** — invisible to 300+ Chromium-only assertions. Font fallback
differs per engine, so this class of difference is expected everywhere, including between iOS (SF
Pro) and whatever a given Android is using. WebKit is the closest instrument to Safari that runs on
Linux; it is not Safari, but it is the engine, and it costs nothing to run.

## The emulation trap, so it does not get re-introduced

With Playwright's `is_mobile: true`, Chromium grows the containing block of a `position: fixed`
element out to the page's `scrollWidth` while `documentElement.clientWidth` keeps reporting 390. At
a 48px root font the bar measured **690px wide on a 390px viewport**, and `window.innerWidth`
agreed with the lie (690). Any instrument that trusts `innerWidth` certifies this. So:

- height and width are judged in a **narrow desktop window**, the only context that honours a real
  layout viewport at large text;
- `isDesktop()` uses a coarse-pointer check and `min(innerWidth, clientWidth)` for the same reason.

## Two behaviours worth knowing before reading a dashboard

**The bar retires at exactly the CSS `lg` breakpoint, not at a JS number.** `isDesktop()` asks
`matchMedia('(min-width: 992px)')` — the same rule Bootstrap's grid uses to bring in the sidebar
offer — rather than comparing a width to 992. Comparing one cannot work: `documentElement.clientWidth`
subtracts the scrollbar, so a 1000px window reported 985 and the bar rendered on real desktop Chrome
up to ~1007px. Real Brave caught it at 1000px; the suite had only ever tested 1440px, and now sweeps
991 / 992 / 1000 / 1007 / 1280. Touch devices are never desktop regardless of numbers, because a
reported width on mobile can track overflowing content instead of the viewport.

**Dismissal is per tab, with a 30-minute cookie fallback.** `sessionStorage` is the primary store, so
a new tab offers the bar again. Where storage access throws (some private modes) a cookie takes over
with `Max-Age=1800` — deliberately not a session cookie: measured in Brave, a session cookie is
*browser*-session scoped, so one dismiss kept the bar hidden in freshly opened tabs and only quitting
the browser brought it back. The cookie jar, not `document.cookie`, is what asserts this, because a
misspelled `Max-Age` produces a perfectly present session cookie that a presence-only check passes.

## What localhost cannot check, and `live.sh` exists for

A static `python -m http.server` ignores `_headers` and `_redirects` entirely, so every local run
leaves these untested:

1. `_headers` actually applied — the `no-cache` pair on `/js/scripts.js` and
   `/css/styles-custom.css`. Live responses were measured at
   `cache-control: public, max-age=14400, must-revalidate`, which lets a returning visitor hold new
   JS and stale CSS for up to four hours.
2. `_redirects` and Pages' trailing-slash 308. The tid rules accept `/?`, and `/articles/` resolves
   differently locally (filesystem) than at the edge.
3. TLS and security headers as delivered (HSTS, CSP, `X-Content-Type-Options`).
4. `X-Robots-Tag` on preview hosts, `robots.txt` on production.
5. The real ClickBank chain: `?tid=sticky_article` → hop scripts → vendor page carrying a `hopId`,
   and that `redirect-leave.js` does not rewrite the hop.
6. Whether `redirect-leave.js` / `exit-popup.js` hard-code the production host — if they do, a click
   test on a preview jumps to the live site and reports a **false green**.

## Preview deploys

Production is the `main` branch of `didge316/teslag` behind Cloudflare Pages; a push to `main`
deploys. Preview = push any other branch, and Pages builds `https://<hash>.<project>.pages.dev`.
`main` is not touched, so the live site is unchanged.

Build the commit from a worktree so the working tree (which carries unrelated uncommitted work) is
not disturbed:

```bash
cd /home/matt/projects/other/tesla-generator/website
git worktree add ../tsg-preview -b feat/sticky-cta
cd ../tsg-preview
cp ../website/js/scripts.js js/scripts.js
cp ../website/css/styles-custom.css css/styles-custom.css
cp ../website/_headers _headers
cp -r ../website/tests tests
git add -A && git commit -m "mobile sticky offer bar: JS+CSS only, with the suite that gates it"
git push -u origin feat/sticky-cta        # <- owner's call: this makes a public URL
```

After merge: `git worktree remove ../tsg-preview && git branch -d feat/sticky-cta`.

A preview is a **different origin and a different pipeline**. Zone-level config (WAF, Bot Fight,
zone cache, HSTS at the zone) does not apply on `*.pages.dev`, so **the `no-cache` fix is only
verifiable after a production deploy**:

```bash
curl -sI https://teslamagneticgenerator.com/js/scripts.js | grep -iE 'cache-control|cf-cache-status'
```

## What still needs a real iPhone, and what no longer does

No longer needs one, because it is now engine-independent: whether the reserved space covers the
bar; whether the bar can grow into a third of the screen; whether the CTA stays inside the layout
viewport; whether the bar wraps. All four are asserted on three engines.

Still needs one, and the honest list is short:

- **Which side of 87px vs 105px iOS lands on.** SF Pro's metrics decide it. `growPad()` makes both
  answers safe, so this is a cosmetic question now, not a correctness one.
- **`env(safe-area-inset-bottom)`** — currently inert, because the site does not set
  `viewport-fit=cover`. If anyone adds it, re-check that the reservation does not over-reserve.
- **Whether the bar fights Safari's bottom toolbar or share sheet**, and whether the × is mistaken
  for the CTA by an actual thumb.
- Flicker on scroll, thumb reach, general "does this feel right".

The five-minute version: push the preview branch, type the `pages.dev` URL into whatever iPhone is
in the house, scroll to the middle of `/build-a-perpetual-motion-generator`, and look. Because the
preview is public, there is no tunnel, no certificate warning, no Mac.

## Known residuals at time of writing

- **No analytics.** Without a dismissal rate the bar is unauditable. Cloudflare Web Analytics can be
  enabled at the zone with the automatic beacon — no HTML edit, so the no-HTML rule survives.
- **Site-wide horizontal overflow at large text.** `a.navbar-brand` measures ~654px at 300% root
  font; at 390px / 100% font **0 of 53 pages overflow**, so this is a large-text-only WCAG 1.4.4
  problem, pre-existing, and independent of the bar. Worth its own fix, not part of this one.
- The bar's own type deliberately does **not** scale with the site's text-size control. The CTA is
  never below 44px tall or 13px of type; page content still scales. This is a deliberate trade: a
  bar that scales without limit is the failure the tier system was invented to paper over.

## What `recalc60` is, and why it is not evidence

`run.py` step 10 counts style recalculations collected over 60s of scripted
scrolling (`recalc60`) alongside forced layouts (`layouts60`). The layout number
is an assertion with a band. The recalc count is not: it moves with machine load,
and measured on a box running the overflow gate's four-browser matrix at the same
time it moved 705 -> 698 with no CSS change to account for it. A number that
moves for noise, printed next to numbers that move for fixes, teaches the reader
that all of them are noise. So it is kept as a gauge and deliberately not quoted
in SHIP.md, in a commit message, or as a pass/fail: the layout-cost claim this
suite actually makes is that the cached `shape()` produces **zero class
mutations and zero forced layouts per scroll frame** (`layouts=+0`), which is a
threshold rather than an absolute.
