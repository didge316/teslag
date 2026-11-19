# WebKit at a 48px root: the EmailOctopus submit button, and why the branch ships the clip

Status: **fixed on this branch** (`.eo-form input[type="submit"] { overflow: hidden; overflow: clip; }`,
`css/styles-custom.css`), **and verified fixed**: the post-fix matrix (2026-11-19, 11:16–12:53,
measured tree on `:8200`, CSS md5 `e6676122ba01` stamped into each artefact) is **624 of 624
green in chromium, firefox and webkit** — webkit's 145 red cells at root 48px are gone, every
run reports `cells green only because of the 1px tolerance: 0`, and every run's negative
control was red by the required margin. None of the reviewer's three revert triggers fired,
so the documented-exception fallback (path A) was not needed and was not taken.

This file exists because the fix is the third remedy tried, the
first two were rejected on measured grounds, and a reader who does not know the failed ones
will re-run them. Six review rounds are in `tests/reviews/hermes-item7-round*.txt`; the
decision to ship the fix rather than document the exception is round six's, and the
reviewer's stopping rules are reproduced below because they are the acceptance criteria.

## The defect, in the numbers

Same committed tree (52 pages), same instrument (`gate.py`), root font injected inline into
the navigation response and read back per cell (10rem probe = 480.0px at root 48px, in every
engine, every cell).

```
                                          doc.scrollWidth / clientWidth   scrollX after scrollTo(1000,0)
about @ 320px  root 48px   chromium                 320 / 320                        0
                           firefox                  320 / 320                        0
                           webkit                   465 / 320                     33 - 49
whole-house @ 1280px root 48px   webkit           1295 / 1280                        15

.eo-form box: left 85, width 150 in every engine.
.eo-form content scrollWidth:      webkit 380, chromium 175, firefox 175.
85 + 380 = 465.  915 + 380 = 1295 at 1280px, where the form sits in the right column.
```

Matrix counts, all three engines, 624 cells each (52 pages x 12 viewport/font cells) — **before**
the fix, and in brackets what the same gate measured after it:

| engine | green | red | where the reds are | negative control |
|---|---|---|---|---|
| chromium | 624 | 0 | — (post-fix: **624**) | red as required (brand 654px, +300) |
| firefox | 624 | 0 | — (post-fix: **624**) | red as required (brand 736px, +382) |
| webkit | 479 | **145** | 49 pages at 320px, 49 at 390px, 47 at 1280px — **all at root 48px**; zero at 16px, zero at 32px (post-fix: **624, zero red**) | red as required (brand 686px, +332) |

So the instrument is live on WebKit: it finds a real 332px defect in the control page. And
WebKit is clean at 16px and 32px on every page.

**Noise, so nobody chases it.** The same cell reads `465` or `477` (about @ 320px) and
`1295` or `1307` (whole-house @ 1280px) run to run, because the EmailOctopus embed is fetched
at runtime and its markup is not identical every load. The *presence* of the overflow is the
finding, not the exact number.

## Mechanism

The EmailOctopus sidebar form's submit control (`<input type="submit" value="Download Now">`,
computed `font-size: 48px`, `width: 150px` after the branch's `max-width: 100%` cap) has a
*preferred* width of about twenty characters. Blink takes that measurement from the default
font metrics and clamps the control's contribution to the page; WebKit measures it in the
**used** font - 20 characters at 48px is ~380px - and aggregates the unclipped descendant's
scrollable overflow into its ancestors and into the document.

The consequence is a defect that is invisible to a box sweep: **no element box reaches past
the viewport** (a depth-40 rect walk finds only the form's bot honeypot, at `left: -4915px`),
yet `documentElement.scrollWidth` is 465, and the reader can scroll onto it. `scrollTo(1000,0)`
returns `scrollX` 33-49 and holds for five re-reads across 200ms, so it is not a stale read.
Hermes' hit test of the revealed strip (`elementsFromPoint` after scrolling right) could not be
completed as designed, because scrolling is also how you make WebKit recompute it - the strip
reads `html`/`body`/column containers either way; nothing painted lives there.

Oddity, recorded rather than explained: `scrollWidth` claims 145px of overflow and the engine
only lets you scroll ~40px of it.

## Ruled out, each one measured

| candidate | result (webkit, about@320 root 48 | whole-house@1280 root 48) | verdict |
|---|---|---|
| `min-width:0` on the form rows | 465 → 465 | boxes shrink to 146px, number unmoved |
| `min-width:0` + `width:100%` on the fields | 465 → 467 | no |
| both of the above together (R3) | 465 → 467 | no |
| `.eo-form * { min-width:0 }` | 465 → 467 | no |
| remove `size` attribute / set `size="1"` | 477 → 477 | no field has a `size` to begin with |
| `field-sizing: fixed` | 465 → 465, 1307 → 1307 | unsupported in the WebKit build tested |
| `appearance:none` / `-webkit-appearance:none` on the submit | 465 → 465, 1295 → 1295 | no |
| `display:block` + `inline-size:100%` on the submit | 465 → 465, 1295 → 1295 | no |
| `width:fit-content` + `max-width:100%` on the submit | 465 → 1295 unchanged | no |
| font cap on every field **except** the submit (T2) | 465 → 465, 1295 → 1295 | the fields are innocent |
| font cap on the **submit only** (T1) | 465 → 320, 1295 → 1280 | works, and it is what localised the cause |

Two things that look like the cause and are not:

* **The exit-intent popup.** It was my hypothesis (25s dwell firing in slow cells) and the
  reviewer's (`position:fixed` containing block). Measured: `.tesla-popup` is **absent** at
  measure time in every cell probed, and the `tesla_exit_popup_shown` session flag is `None`.
* **The "Powered by EmailOctopus" link.** `white-space: nowrap`, its 460px of content spilling
  312px past a 148px box - the furthest-reaching ink on the page. And it measures **identical
  numbers in all three engines** (chromium and firefox green with it), because its parent `<p>`
  has `overflow-x: hidden`. It is the decoy an ink sweep finds first; `probe.WORST`'s own
  comment already said so.
* **The honeypot** `div.emailoctopus-form-row-hp`: `left: -4915px` in every engine. It shows up
  in `gate.py`'s offender lines with `over=0` because `probe.OFFENDERS` also reports left-side
  overflow - which is why 80 of the 145 reds printed two non-causes as their diagnosis.
  TODO(noticed, not done here): that filter should label left-only entries instead of listing
  them as offenders on a right-scroll verdict.

## The fix, and what it costs (nothing measured)

```css
.eo-form input[type="submit"] { overflow: hidden; overflow: clip; }
```

`hidden` first so Safari below 16 keeps it; `clip` after, because a button has no use for a
scroll container. Both were tested separately and both work (U3, U6); the cascade (U7) is what
shipped. `contain: content` (U2) also works and was rejected: it additionally creates a
stacking context and a paint clip, and buys nothing here.

Verification, all of it in `fix465.py`, which loads a **fresh page per candidate rule**
(WebKit's document scrollable overflow area can go stale once its cause is hidden, so
same-page mutation tests can under-report a fix; `BISECT` prints a RESTORE WARNING when it
sees this):

* **Green at 320 / 390 / 768 / 1280 px, root 16 / 32 / 48**, webkit and chromium.
* **Widget pixels identical**: sha256 of the `.eo-form` screenshot, before vs after the rule,
  equal in webkit and chromium at all four widths at root 16.
* **Focus ring unchanged** - the gate the reviewer insisted on before the matrix was allowed
  to run. Reached by keyboard (6 Tab presses, `:focus-visible` true), the indicator is a
  `rgba(38, 143, 255, 0.5) 0 0 0 9.6px` spread shadow, and outline, shadow, horizontal geometry
  and the pixels of the *ring region* (button rect + 14px, because the shadow is painted
  outside the border box and an element screenshot would clip it) are all identical with and
  without the rule, at root 48 and root 16, in webkit and chromium.
* **One submit button per page** and geometry inert at root 16 on every page carrying the
  widget: see `fix465-inert-sweep.txt` — 51 pages, chromium, root 16 @ 1280px, one fresh
  page load each: widget pixel hash equal on all 51, no form geometry moved, `scrollWidth`
  1280 → 1280 everywhere, and `submitCount` 1 on 49 pages, 0 on the 2 pages whose form has
  no submit control at all (the rule cannot reach them either).

Rejected remedies, with the reason each was rejected rather than the reason it failed:

1. **Cap the fields' font** (`clamp(16px,1rem,24px)`): works, and it would pin third-party form
   text at 24px for *every* engine at >=250% zoom. That is a text-scaling regression shipped to
   three engines to remove a scrollbar in one. The branch exists to stop doing that.
2. **Clip/auto-scroll at `.eo-form`**: works, and it visibly cuts the form's rows, which stick
   25px out of `.eo-form` in all three engines today (`row L60 R260` vs `form L85 R235`).

## Acceptance, per the reviewer's stopping rules (round six) — and how each one resolved

*Any red cell in chromium or firefox that was green pre-fix → revert.* **Did not fire:** 624/624
in both, same as before, with the same negative-control margins and zero tolerance-only cells.
*Any webkit red at 16px or 32px → revert.* **Did not fire.** *A webkit red surviving only at
48px → "fix partial, see cells", and fall back to path A.* **Did not fire: webkit is 624/624,
so the fix generalised from `about` to the other 51 pages rather than partially landing.**
*All three engines re-run after the CSS change.* **Done** — the pre-fix artefacts were not
reusable, and they are kept anyway (below) because they are the before picture.

The rules themselves, as the reviewer wrote them:

* Any red cell at any root font in chromium or firefox that was green pre-fix → **revert**.
* Any webkit red at 16px or 32px → **revert**.
* A webkit red surviving *only* at 48px → ship the exception, but the record must say
  **"fix partial, see cells"**, not "fix ineffective": it would mean the rule did not
  generalise from `about` to the other pages, which is a different finding.
* **Assert the value, not the verdict**: green at 320px means `scrollWidth == 320`, not
  `<= clientWidth + 1`. A 331-of-320 pass is a second defect hiding behind the tolerance.
  `gate.py`'s own tolerance is 1px and stays there (sub-pixel rounding is real, and a
  zero-tolerance gate has burned runs on it before), so the tolerance is now never silent:
  every run prints `cells green only because of the 1px tolerance: N`, and **N must be 0**
  in a post-fix artefact. Reading a matrix without that line means reading an artefact
  from before 2026-11-19, when the loophole was open.
* All three engines are re-run after this CSS change, because every prior artefact was produced
  against the pre-fix stylesheet.

## Re-running this

```sh
cd tests/overflow
./fix465.py http://127.0.0.1:8200 --round 4 --rule U7              # the candidate, one page per rule
SHOT=1 ./fix465.py http://127.0.0.1:8200 --round 4 --rule U7        # + widget pixel hash
FOCUS=1 ./fix465.py http://127.0.0.1:8200 --round 4 --rule U7       # + keyboard focus ring test
python3 why465.py http://127.0.0.1:8200 --page about --width 320 --font 48 --engine webkit
python3 gate.py http://127.0.0.1:8200 --engine chromium --only "$(cat ../.staging/tracked-pages.txt)"
python3 gate.py http://127.0.0.1:8200 --engine firefox   --only "$(cat ../.staging/tracked-pages.txt)"
python3 gate.py http://127.0.0.1:8200 --engine webkit    --only "$(cat ../.staging/tracked-pages.txt)"
```

Before any of it, rebuild the measured tree with `python3 tests/ship/stage.py shipped` — not
`stage.py` alone, which regenerates the page states and leaves the measured tree pointing at
the last build. Then save the stylesheet the run served as
`tests/overflow/payload-measured-<the hash the run prints>.css`, or `css-comment-only.py` will
(not quite fairly) call the numbers orphans.

`:8200` serves the measured tree (`tests/.staging/site-shipped`), rebuilt from HEAD by
`tests/ship/stage.py`; `:8199` serves the working tree and is used only by the sticky-CTA
suite. **Run WebKit last and alone** - it has died under load and under `TargetClosedError`
when another browser shares the box, and one diagnostic call must never be able to end a
matrix (that is what the try/except around `probe.WORST` in `gate.py` is for).

Evidence retained: `gate-BEFORE-cssfix-webkit-RED.txt` (the pre-fix 479/624 run, including its
red negative control and the 80 lost-diagnosis lines), plus `gate-BEFORE-cssfix-chromium.txt`
and `-firefox.txt` for the two engines that were already green. The post-fix artefacts are the
ones `commit-index.py` quotes: `gate-FINAL-{chromium,firefox,webkit}.txt`, each stamped at the
top with the md5 of the `css/styles-custom.css` the measured tree served, so an artefact can
never be read against the wrong stylesheet again.

## If you disagree with this decision

Start with the failed-fixes table above: the fix was chosen over a documented exception
because it is pixel-identical and scoped to one control, and over two working alternatives
because both of those regress something a reader can see. The argument against shipping it at
all was: WebKit's reds are all at a root font no conformance bar requires (1.4.4 is 200% -
green here - and 1.4.10 is 320 CSS px at default zoom - green here), from a third-party
widget, onto empty space. That argument won in round five and lost in round six, when a fix
that touches nothing visible turned up. To re-litigate it, re-run the matrix and the three
checks above; they take about 90 minutes and every number in this file will be regenerated.
