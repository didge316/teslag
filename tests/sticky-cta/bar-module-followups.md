# Sticky bar — what the module review produced

Owner-facing. Everything below cites evidence that exists on the branch or in `tests/`;
anything not verified first-hand is marked UNVERIFIED rather than softened. Nine items,
none of them a push blocker unless the line says so. Roughly ten lines of code between
them, plus three decisions only the owner can make.

**Component footprint.** 22 rule blocks over 17 distinct selectors: 16 `tmg-cta-*` plus
`.tmg-sr-only` (`css/styles-custom.css:431`). An earlier count of "21 blocks, 16
selectors" in the commit message came from a `tmg-cta`-scoped inventory describing a
`tmg-` footprint, so it could not see `.tmg-sr-only`, which `buildBar()` depends on for
the CTA's text alternative. Recounted; `tests/overflow/dormant-bar-css.py` now strips the
`tmg-` namespace and asserts 22, so the dormancy proof covers the `sr-only` rule too.

## 1. Dismissal is browser-wide for 30 minutes, not per-tab
- Where: `js/scripts.js:256` `rememberDismissal()`, cookie write at `:262`,
  `DISMISS_COOKIE_TTL: 1800` at `:178`.
- Evidence, measured: dismissed the bar on `/whole-house.html`, then opened a second tab
  in the same browser (new page, same context: shared cookies, fresh `sessionStorage` —
  which is what a second tab is). Second tab: bar not shown, **its own `sessionStorage`
  flag `None`**, cookie present. Only the cookie is suppressing it there.
- Fix: none required — this is a decision, not a defect.
- Cost: none to leave as is; ~3 lines to change.
- Blocker: no.
- The open question, deliberately not answered here: browser-wide 30 minutes (fewer repeat
  impressions, no nag) versus per-tab semantics, which is what CONFIG gives as the reason
  `sessionStorage` is primary. Per-tab would mean writing the cookie only inside the
  `setItem` catch. The comment describes the second; the code does the first.

## 2. Comment contradicts the code: "remembered permanently"
- Where: `js/scripts.js:158`.
- Evidence: "remembered permanently rather than nagging on the next page", 104 lines above
  a cookie write at :262 with `Max-Age=1800` that item 1 shows is always written.
- Fix: say what happens — "remembered for the rest of this browser session's pages, or
  for half an hour where the cookie can be set", or whatever the owner decides in item 1.
- Cost: one line. Blocker: no.

## 3. `wp-textsize` attribution is fiction, and it is pre-existing
- Where: `js/scripts.js:184`, `css/styles-custom.css:312`, `css/styles-custom.css:528`,
  plus a copy in `tests/overflow/payload-measured-322b32b3533a.css:276`.
- Evidence: **zero HTML files on the branch mention `wp-textsize`.** Four files mention it
  at all and all four do so in comments. It also appears in the pre-fix payload snapshot,
  so item 7 shipped a stylesheet already claiming a control that does not exist, and the
  module inherited the claim. The behaviour the deterministic-height design guards against
  is real — root font grows under reader zoom and browser font settings, which is what the
  1,872-cell overflow matrix drove — only the attribution is wrong.
- Fix: attribute the behaviour to reader zoom and user font settings; strike the control
  from all three comments. A comment-only CSS edit is provably rule-text-neutral:
  `tests/overflow/css-comment-only.py` is the check that exists for that claim (currently
  passing: 90 rule blocks, rule text `881ac2e2f1fb` on both sides), and it must pass
  before such an edit lands.
- Cost: three comments and one check run. Blocker: no.

## 4. Dismissal cookie has no `Secure`
- Where: `js/scripts.js:262`.
- Evidence: the write is `KEY + '=1; path=/; SameSite=Lax; Max-Age=' + TTL`. Nothing in
  `_headers` or `_redirects` references an `http://` origin, and the site is served over
  HTTPS on Cloudflare Pages, so an unsecured cookie is only ever a downgrade risk.
- Fix: append `; Secure`.
- Cost: nine characters. Blocker: no.

## 5. Dismiss removes three listeners and leaves a fourth
- Where: `js/scripts.js:440-442` removes `scroll`, `resize` and the bar's `focusout`;
  `js/scripts.js:457` adds `resize → growPad`, which survives the dismissal.
- Evidence: `growPad`'s first line returns unless the bar is `is-visible`, so it is inert
  afterwards. Asymmetric, not a leak.
- Fix: remove it in the same handler, or say in one line why it stays.
- Cost: one line. Blocker: no.

## 6. The bar is tabbable behind an `aria-modal="true"` dialog
- Where: `buildBar()` appends the bar to `<body>`; `js/exit-popup.js:63` renders
  `role="dialog" aria-modal="true"` and nothing makes the rest of the page inert.
- Evidence: `/build-a-perpetual-motion-generator`, 390x844, chromium and webkit, popup
  raised both by the real 25s dwell (`DWELL_MS`) and by a synthetic exit-intent
  `mouseout`: bar visible behind the dialog and its two controls — including the paid
  link — in the tab ring. `tests/sticky-cta/modal-coexistence-2026-11-19.txt`.
  The number that scopes the fix: **21 focusables outside the dialog, 19 of them the
  page's own**, so the popup has never had a trap and this branch adds 2.
- Fix, in order: (a) one condition in `paint()` holding the bar away while a
  `[role="dialog"]` is open — ~3 lines, ships and reverts with the bar; (b) `inert` on the
  page wrapper while the dialog is up — one attribute, supported by every engine still in
  use, fixes all 21 and makes `aria-modal="true"` stop being a lie. Do not hand-roll a
  focus trap; `inert` is less code and strictly more correct.
- Cost: ~10 lines across two commits. Blocker: no — before this commit the bar did not
  exist, so it cannot have made the popup worse.

## 7. Attribution: split `/can-I-buy` out of the fallback bucket
- Where: `TID_RULES` at `js/scripts.js:196`.
- Evidence: 50 of 52 pages render the bar; the fallback `sticky_article` holds 36 of them
  — 72% — including `/can-I-buy`, `/build-a-magnetic-generator`,
  `/build-a-perpetual-motion-generator`, `/whole-house` and `/magnetic-generator`. The
  offline map (`tests/sticky-cta/tid-map.py`) and the live DOM read of `?tid=`
  (`tests/sticky-cta/tid-live.py`) agree on every rendering page, so this is not a broken
  matcher; it is an under-specified rule set. No mis-buckets were found in either run.
- Fix: minimum viable is one anchored rule for `/can-I-buy`, because bottom-of-funnel EPC
  is the thesis. Otherwise split the intent pages properly, or collapse to two tids and
  stop presenting a breakdown that isn't one.
- Cost: one regex. Blocker: no, but it decides whether the bar's numbers can ever say
  anything.

## 8. `/magnetic-generator-scam` still shows the offer
- Where: `buildBar()` / `init()`: there is no suppression path.
- Evidence: measured in the live DOM — the bar renders 700px down the page that argues the
  product is a scam, attributed `sticky_scam`.
- Fix: suppress the bar on that path. One condition.
- Cost: two lines. Blocker: no — owner's call, and worth making before a push rather than
  measuring after one.

## 9. Price and guarantee are assertions no test can falsify
- Where: `js/scripts.js:299-300`, both string constants.
- Evidence: `~$47 · instant download · 60-day money-back guarantee`, and the sub-390px
  short variant `~$47 · 60-day guarantee`. Claims about a third-party product, shown to an
  audience that includes `/magnetic-generator-scam`.
- Fix: the owner's dated yes, plus a date for the next check.
- Cost: a decision. Blocker: no, but it is the only item here that can be true today and
  false next quarter with nothing on the site changing.

## 10. The six `sticky_*` tids may not exist in the ClickBank account
- Where: `TID_RULES` at `js/scripts.js:196`; the tid reaches ClickBank as the only
  differentiator, since `rel=noreferrer` removes the referrer.
- Evidence: `curl -L` on the hop with `tid=side_tower`, `tid=sticky_article`,
  `tid=sticky_scam` and `tid=zzz_not_registered_xyz` all return 200 after 2 redirects to
  `ultimateoffgridgenerator.net/index_ultimate_mobile.html?hopId=<fresh uuid>`. A live
  click through the bar's CTA behaves identically (`offer-click-2026-11-19.txt`). The hop
  therefore accepts **any** tid, registered or not, so nothing about the redirect
  distinguishes a template ClickBank will report from one it will drop.
- Fix: check the account's template-id list; create the six if they are missing.
- Cost: a dashboard visit. Blocker: no — but if they are unregistered, the buckets this
  branch produces exist only in the code, and every conclusion drawn from them later will
  be drawn from an empty report.

## 11. `rel` on the bar's CTA is *more* correct than the site's, which is its own problem
- Where: `js/scripts.js:304` — `rel="noopener noreferrer sponsored nofollow"`. The site's
  **213** other affiliate anchors carry `rel="noopener noreferrer nofollow"`, without
  `sponsored`.
- Evidence: counted across tracked HTML; `offer-link-2026-11-19.txt` prints the rel set the
  live DOM actually renders.
- Fix: bring the 213 into line, in a separate commit that runs the page gates — it is an
  SEO-visible change to shipped pages, and item 5's commit is what showed how easily a
  bulk attribute edit goes wrong.
- Cost: 213 attributes by script. Blocker: no, and the bar is not the thing to change.

## 12. Two pages show the offer while carrying no affiliate link of their own
- Where: `contact.html`, `privacy.html` — measured: bar visible, zero `hop.clickbank.net`
  anchors on the page (`offer-link-2026-11-19.txt`).
- Evidence: both fall into the `sticky_article` fallback bucket. Every other affiliate
  placement on the site was written into the page by hand; on these two the bar is the
  only path to the offer, and on `/privacy` that is a $47 offer on the page that explains
  how visitor data is handled.
- Related, pre-existing: `js/redirect-leave.js` rewrites every non-clickbank external click
  on 50 pages to `?tid=leave_redirect` — measured, and the bar is correctly exempt. Recorded
  here because it means on those pages the bar's `sticky_*` clicks are the only affiliate
  signal that has not been re-attributed by another script.
- Fix: a suppression path (the same one item 8 needs), or a decision that these pages
  should carry the offer.
- Cost: shares the fix with item 8. Blocker: no.
