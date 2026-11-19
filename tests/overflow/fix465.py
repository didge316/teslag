#!/usr/bin/env python3
"""Does a candidate CSS rule actually stop the WebKit overflow? One page per rule.

why465.py found the shape on 2026-11-19 and it is not what either the gate's own
diagnosis or the reviewer guessed:

  * The EmailOctopus "Powered by" link (`a`, nowrap, text wider than its 148px
    box, spilling 312px) is measured with *identical numbers in all three
    engines* and its parent `<p>` has `overflow-x: hidden`, so it is clipped
    before it can reach the page. It is a decoy that a rect sweep cannot see and
    an ink sweep finds first. (probe.WORST's own comment already said so.)
  * The number that moves between engines is one level up: the same 150px box
    (`div.eo-form`, `.inline-container`, and the `div` above the form rows)
    reports `scrollWidth` 380 in WebKit and 175 in Blink, on the same tree with
    the same CSS and a root font read back at 48px in every engine. And
    `left(85) + 380 = 465`, which is the document's scrollWidth, exactly.
  * No element *box* reaches 465 in WebKit (a depth-40 rect sweep finds nothing
    past the viewport except the honeypot at left -4915), and yet
    `scrollTo(1000, 0)` lands `scrollX = 49`: a Safari reader at 300% does get a
    horizontal scrollbar, and it reveals nothing they can use.
  * The chain's widest in-flow item is an EmailOctopus form row: computed
    `min-width: 200px` on a 150px column, because **min-width beats max-width**,
    so the branch of the CAP the branch CSS carries today (`.eo-form *` gets
    `max-width: 100% !important`) cannot reach it. An `<input>` with no `size`
    attribute has a preferred width of 20 characters, which is font-metric
    dependent - 20 chars at a 48px root is ~380px in whatever family WebKit
    resolves `"Noto sans, sans-serif"` to, and ~175px in Blink's.

So the candidate fix is the other half of the cap: `min-width: 0`, on the rows and
on the fields. This file exists because "that is the obvious fix" is exactly the
kind of claim this branch has been wrong about twice, so each candidate gets a
fresh page and the gate's own verdict on it.

One rule per page load, deliberately: WebKit's document scrollable overflow area
can go stale once its cause is hidden (a hidden node restored in the same page
does not always bring the number back), so measuring several rules in one page
would let an earlier success contaminate a later reading. `--repeat N` re-runs
the whole set so a candidate that only passes once is visible as a flake.

It reads three things per rule, not one: `documentElement.scrollWidth` (the
verdict line the gate uses), whether the document really scrolls right, and the
form's own `scrollWidth`/`clientWidth` so the mechanism is visible too. A rule
that makes `scrollWidth` lie - by clipping, e.g. `overflow-x: hidden` on an
ancestor of the page - is called out rather than praised: PLAN 4 forbids
`overflow-x: hidden` on html/body for exactly this reason, and the same trap
exists one level lower.

A candidate that passes here still has to go through gate.py over all 52 pages and
all three engines; this only decides which candidate is worth that 30 minutes.

Usage:
  ./fix465.py                                   # webkit, about @ 320px root 48px, all rules
  ./fix465.py http://127.0.0.1:8200 --page whole-house --width 1280 --font 48
  ./fix465.py --engine chromium --rule R3       # does the fix change a green engine?
  ./fix465.py --round 2                          # the intrinsic-width candidates (see RULES2)
"""
import hashlib
import os
import sys

import gate   # the instrument: route_font, measure_cell, IO_STUB, HEIGHT
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8200"
SHOT = bool(os.environ.get("SHOT"))   # SHOT=1 -> screenshot the widget before/after every rule
FOCUS = bool(os.environ.get("FOCUS"))  # FOCUS=1 -> focus the submit first (implies SHOT)
if FOCUS:
    SHOT = True

# The control this fix touches is the only interactive element in the widget, and
# `overflow: clip` on a control can clip its own focus ring - which a screenshot of
# an unfocused page would never show. So the ring is reached with the keyboard (a
# programmatic focus() does not necessarily satisfy :focus-visible, and the UA's
# default ring answers to :focus-visible), the widget is photographed with the ring
# in it before and after the rule, and the computed outline is read back on both
# sides. If the ring is clipped, this fix trades a scrollbar onto nothing for an
# accessibility regression on the one control a reader has to use, and the answer
# stops being D.
FOCUS_JS = """() => {
  const s = document.querySelector('.eo-form input[type=submit]');
  if (!s) return { focused: 'no submit in .eo-form' };
  const cs = getComputedStyle(s), r = s.getBoundingClientRect();
  let pv;
  try { pv = s.matches(':focus-visible'); } catch (e) { pv = 'unsupported'; }
  return {
    isFocused: document.activeElement === s, focusVisible: pv,
    tag: document.activeElement ? document.activeElement.tagName.toLowerCase() : null,
    outlineStyle: cs.outlineStyle, outlineWidth: cs.outlineWidth,
    outlineOffset: cs.outlineOffset, outlineColor: cs.outlineColor,
    boxShadow: cs.boxShadow.slice(0, 70),
    box: { left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width),
           top: Math.round(r.top), h: Math.round(r.height) },
    scrollW: s.scrollWidth, clientW: s.clientWidth,
  };
}"""

IS_SUBMIT = "() => { const a = document.activeElement; return !!a && a.matches('.eo-form input[type=submit]'); }"

# Named candidates. `css` is injected with add_style_tag after load (a diagnosis,
# not the shipped CSS - the shipped stylesheet can only change in a commit);
# `dom` mutates the page instead, for the question "is this preferred width
# coming from the size attribute at all?"
#
# R4 is not a candidate: it is the mechanism probe. If the 380 shrinks when the
# fields' font shrinks, the width is derived from text metrics and the fix has to
# cap the min-content, not the paint.
RULES1 = [
    ("R1", "row min-width:0",
     ".eo-form .emailoctopus-form-row{min-width:0!important}", None),
    ("R2", "fields min-width:0 + width:100%",
     ".eo-form input,.eo-form select,.eo-form textarea{min-width:0!important;width:100%!important}", None),
    ("R3", "the missing half: R1+R2 together",
     ".eo-form .emailoctopus-form-row{min-width:0!important}"
     ".eo-form input,.eo-form select,.eo-form textarea{min-width:0!important;width:100%!important}", None),
    ("R4", "MECHANISM PROBE: fields font 12px (not a fix)",
     ".eo-form input,.eo-form select,.eo-form textarea{font-size:12px!important}", None),
    ("R5", "DOM: strip the size attribute from fields", None,
     "() => { document.querySelectorAll('.eo-form input').forEach((i) => { i.removeAttribute('size'); }); "
     "return document.querySelectorAll('.eo-form input').length; }"),
    ("R6", "broadest: every field and row and wrapper min-width:0",
     ".eo-form *{min-width:0!important}", None),
    ("R7", "CANDIDATE THAT LIES: clip at the form",
     ".eo-form{overflow-x:hidden!important}", None),
]

# Round two, 2026-11-19 10:05, measured. Round one's `min-width: 0` candidates
# (R1, R2, R3, R6) all failed - the rows and fields went to min-width 0, their
# boxes shrank to 146px, and `.eo-form`'s content stayed at 380. The only rule
# that moved it was R4: shrinking the fields' *font* collapsed 380 to 175, and
# 175 is exactly what Blink reports for the same box at the same 48px root, which
# says an `<input>`'s preferred width is 20 characters and Blink takes that from
# the default font metrics while WebKit takes it from the used ones. So the
# candidates here attack the intrinsic width itself, not the box.
RULES2 = [
    ("S1", "DOM: size=\"1\" on every field (is it really 20 characters?)", None,
     "() => { document.querySelectorAll('.eo-form input').forEach((i) => i.setAttribute('size', '1')); "
     "return document.querySelectorAll('.eo-form input').length; }"),
    ("S2", "field-sizing: fixed (the CSS built for exactly this)",
     ".eo-form input,.eo-form select,.eo-form textarea{field-sizing:fixed!important}", None),
    ("S3", "fields font 16px (works, but stops the form scaling with zoom)",
     ".eo-form input,.eo-form select,.eo-form textarea{font-size:16px!important}", None),
    ("S4", "fields font capped with clamp(16px, 1rem, 24px)",
     ".eo-form input,.eo-form select,.eo-form textarea{font-size:clamp(16px, 1rem, 24px)!important}", None),
    ("S5", "the honest container: .eo-form{overflow-x:auto}",
     ".eo-form{overflow-x:auto!important}", None),
    ("S6", "the honest container, hidden variant, for comparison with S5",
     ".eo-form{overflow-x:hidden!important}", None),
]

# Round three: which field leaks? The submit button's intrinsic width is its
# `value` text, a text field's is its character area, and only one of those is
# worth a rule. If T1 alone collapses it, the fix can be scoped to the button
# instead of capping the font of every field on the page.
RULES3 = [
    ("T1", "only input[type=submit] at 16px (is it the button's value text?)",
     ".eo-form input[type=submit]{font-size:16px!important}", None),
    ("T2", "only text/email inputs at 16px (is it a field's character area?)",
     ".eo-form input:not([type=submit]){font-size:16px!important}", None),
    ("T3", "submit at 24px - the narrowest honest-looking cap",
     ".eo-form input[type=submit]{font-size:clamp(16px,1rem,24px)!important}", None),
    ("T4", "everything but the submit capped, to see what S4 really needed",
     ".eo-form input:not([type=submit]){font-size:clamp(16px,1rem,24px)!important}", None),
]

# Round four, after round three localised the leak to the submit button's font.
# These are the candidates that would kill the *intrinsic contribution* without
# touching how anything looks: appearance, containment, clipping the button's own
# ink, and forcing it to fill its line. If one of these works it is strictly
# better than a font cap, because it costs a reader nothing.
RULES4 = [
    ("U1", "appearance:none on the submit (UA intrinsic sizing off)",
     ".eo-form input[type=submit]{-webkit-appearance:none;appearance:none!important}", None),
    ("U2", "contain:content on the submit",
     ".eo-form input[type=submit]{contain:content!important}", None),
    ("U3", "overflow:clip on the submit itself",
     ".eo-form input[type=submit]{overflow:clip!important}", None),
    ("U4", "display:block + inline-size:100% on the submit",
     ".eo-form input[type=submit]{display:block;inline-size:100%!important}", None),
    ("U5", "width:fit-content + max-width:100% on the submit",
     ".eo-form input[type=submit]{width:fit-content;max-width:100%!important}", None),
    ("U6", "overflow:hidden on the submit (works everywhere, 2005-era)",
     ".eo-form input[type=submit]{overflow:hidden!important}", None),
    ("U7", "THE CANDIDATE: hidden then clip, so old Safari keeps the fix",
     ".eo-form input[type=submit]{overflow:hidden!important;overflow:clip!important}", None),
]

REPORT = """() => {
  const de = document.documentElement;
  const f = document.querySelector('.eo-form');
  const rows = [...document.querySelectorAll('.eo-form .emailoctopus-form-row')].slice(0, 4)
    .map((r) => { const b = r.getBoundingClientRect(), cs = getComputedStyle(r);
      const inp = r.querySelector('input');
      const ib = inp ? inp.getBoundingClientRect() : null, ics = inp ? getComputedStyle(inp) : null;
      return { row: { w: Math.round(b.width), left: Math.round(b.left), right: Math.round(b.right),
                      minW: cs.minWidth, maxW: cs.maxWidth, scrollW: r.scrollWidth, clientW: r.clientWidth },
               input: inp ? { w: Math.round(ib.width), right: Math.round(ib.right), size: inp.getAttribute('size'),
                              minW: ics.minWidth, width: ics.width, fs: ics.fontSize,
                              scrollW: inp.scrollWidth, clientW: inp.clientWidth } : null }; });
  return {
    docScrollW: de.scrollWidth, docClientW: de.clientWidth,
    submitCount: document.querySelectorAll('.eo-form input[type=submit]').length,
    submits: [...document.querySelectorAll('.eo-form input[type=submit], .eo-form button')]
      .map((s) => { const b = s.getBoundingClientRect(), cs = getComputedStyle(s);
        return { tag: s.tagName.toLowerCase(), type: s.type, value: (s.value || s.innerText || '').trim().slice(0, 30),
                 w: Math.round(b.width), right: Math.round(b.right), fs: cs.fontSize, ff: cs.fontFamily.split(',')[0],
                 scrollW: s.scrollWidth, clientW: s.clientWidth, width: cs.width, minW: cs.minWidth, maxW: cs.maxWidth };
      }),
    form: f ? { w: Math.round(f.getBoundingClientRect().width),
                left: Math.round(f.getBoundingClientRect().left),
                scrollW: f.scrollWidth, clientW: f.clientWidth } : 'absent',
    rows: rows,
  };
}"""

# Is the scroll region empty? Hermes' point: say so with evidence, not assertion.
# Scroll as far right as the document will go, then hit-test the strip that used
# to be off-screen. If every probe comes back html/body (or the page's own
# background element), the scrollbar a Safari reader gets reveals nothing they can
# read, click, or use - which is the whole difference between "a defect" and
# "an empty region".
HIT = """() => {
  const de = document.documentElement;
  de.scrollLeft = de.scrollWidth;
  const band = Math.min(de.scrollWidth, Math.max(80, de.scrollLeft));
  const out = [];
  for (const x of [1, 10, 25, 45, 70]) {
    if (x > band) continue;
    for (const y of [200, 600, 1200]) {
      const els = document.elementsFromPoint(x, y).slice(0, 3).map((e) => e.tagName.toLowerCase()
        + (e.className && typeof e.className === 'string' && e.className.trim()
           ? '.' + e.className.trim().split(/\\s+/)[0] : ''));
      out.push({ x, y, els });
    }
  }
  return { scrollX: window.scrollX, scrollWidth: de.scrollWidth, probes: out };
}"""

SCROLLS = """async () => {
  const raf = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  window.scrollTo(0, 0); await raf();
  window.scrollTo(1000, 0); await raf();
  const x = window.scrollX;
  window.scrollTo(0, 0); await raf();
  return x;
}"""


def run(pw, engine, base, page, width, font, only, rules):
    b = pw[engine].launch()
    for rid, label, css, dom in rules:
        if only and rid not in only:
            continue
        c = b.new_context(viewport={"width": width, "height": gate.HEIGHT[width]})
        pg = c.new_page()
        pg.add_init_script(gate.IO_STUB)
        injected = gate.route_font(c, font, page)
        pg.goto(f"{base}/{page}.html", wait_until="load", timeout=60000)
        if injected["n"] == 0:
            print(f"  {rid}: INSTRUMENT - the injection route never fired")
            c.close()
            continue
        before = pg.evaluate(REPORT)
        ring_before, presses = None, 0
        if FOCUS:
            while presses < 40 and not pg.evaluate(IS_SUBMIT):
                pg.keyboard.press("Tab")
                presses += 1
            ring_before = pg.evaluate(FOCUS_JS)
        def shot():
            """Pixels of the ring region, not of the widget.

            The focus indicator on this control is a box-shadow (Bootstrap's
            .form-control:focus sets outline:0 and paints a shadow ring) drawn outside
            the button's border box, so an element screenshot of the button - or of
            .eo-form, which is the same width - clips it away on both sides and proves
            nothing either way. Photograph the ring region instead: the button's rect
            plus a margin, clamped into the viewport.
            """
            if FOCUS:
                box = pg.evaluate(FOCUS_JS).get("box") or {}
                x = max(0, box.get("left", 0) - 14)
                y = max(0, box.get("top", 0) - 14)
                return hashlib.sha256(pg.screenshot(clip={
                    "x": x, "y": y,
                    "width": min(width - x, box.get("w", 200) + 28),
                    "height": box.get("h", 40) + 28})).hexdigest()
            if pg.locator(".eo-form").count() == 0:
                # Two of the 52 pages carry no form at all; waiting 30s for an element
                # that will never appear turns a sweep into a hang.
                return "no-widget"
            return hashlib.sha256(pg.locator(".eo-form").screenshot()).hexdigest()

        if FOCUS and ring_before is not None:
            # Settle, then centre the control: `top` is viewport-relative, and a read
            # taken while the focus scroll is still moving compares the scroll with the
            # control rather than the control with itself.
            pg.wait_for_timeout(350)          # Bootstrap transitions box-shadow over .15s
            pg.evaluate("() => document.querySelector('.eo-form input[type=submit]')"
                        ".scrollIntoView({block: 'center'})")
            pg.wait_for_timeout(250)
            ring_before = pg.evaluate(FOCUS_JS)
        shot_before = None
        if SHOT:
            try:
                shot_before = shot()
            except Exception as exc:                                    # noqa: BLE001
                print(f"      (no before screenshot: {str(exc).splitlines()[0][:60]})")
        if css:
            pg.add_style_tag(content=css)
        n = pg.evaluate(dom) if dom else None
        after = pg.evaluate(REPORT)
        if FOCUS and ring_before is not None:
            ring_after = pg.evaluate(FOCUS_JS)

            def flat(d):
                return {k: ({kk: vv for kk, vv in v.items() if kk != "top"} if k == "box" else v)
                        for k, v in d.items()}

            a, b = flat(ring_before), flat(ring_after)
            print(f"      after {presses} Tab presses: focused={ring_after.get('isFocused')} "
                  f":focus-visible={ring_after.get('focusVisible')} "
                  f"outline={ring_after.get('outlineStyle')} {ring_after.get('outlineWidth')} "
                  f"offset={ring_after.get('outlineOffset')} shadow={ring_after.get('boxShadow')}")
            print(f"      control box, no rule {a.get('box')} | with the rule {b.get('box')}")
            print("      ring as measured: "
                  + ("unchanged (focus-visible, outline, shadow and geometry all identical)"
                     if a == b else f"CHANGED {a} -> {b}"))
        if SHOT and shot_before:
            try:
                shot_after = shot()
                what = "ring region" if FOCUS else "widget"
                print(f"      {what} pixels: "
                      + ("IDENTICAL before/after (the rule changes nothing a reader can see)"
                         if shot_after == shot_before
                         else f"DIFFERS ({shot_before[:8]} -> {shot_after[:8]})"))
            except Exception as exc:                                    # noqa: BLE001
                print(f"      (no after screenshot: {str(exc).splitlines()[0][:60]})")
        scrolls = pg.evaluate(SCROLLS)
        hit = pg.evaluate(HIT)
        verdict = ("GREEN" if after["docScrollW"] <= after["docClientW"] + 1
                   else f"still {after['docScrollW'] - after['docClientW']}px over")
        lies = ""
        if css and "overflow-x:hidden" in css:
            lies = "  <-- clipping, not fixing: the number went down because the page stopped " \
                   "reporting its own overflow"
        elif css and "overflow-x:auto" in css:
            lies = "  <-- a scroll container: the overflow is still there and now reachable " \
                   "inside the form, so the page stops scrolling but the form starts"
        elif before["docScrollW"] == after["docScrollW"] and after["docScrollW"] > after["docClientW"]:
            lies = ""
        print(f"  {rid} {label}")
        print(f"      doc.scrollWidth {before['docScrollW']} -> {after['docScrollW']} "
              f"of {after['docClientW']} | the document "
              f"{'DOES scroll to x=' + str(scrolls) if scrolls > 0 else 'does not scroll'} "
              f"| {verdict}{lies}")
        if n is not None:
            print(f"      (stripped size= from {n} fields)")
        empt = {tuple(sorted(p["els"])) for p in hit["probes"]}
        print(f"      scrolled to x={hit['scrollX']} and hit-tested the revealed strip "
              f"(scrollWidth {hit['scrollWidth']}): "
              + ("only " + " / ".join(", ".join(e) for e in sorted(empt)) if len(empt) == 1 and
                 all(set(e) <= {'html', 'body'} for e in empt) else
                 "; ".join(f"({p['x']},{p['y']})={''.join(p['els'])}" for p in hit["probes"])))
        if isinstance(after["form"], dict):
            print(f"      .eo-form: box w={after['form']['w']} left={after['form']['left']} "
                  f"content scrollWidth {before['form']['scrollW']} -> {after['form']['scrollW']} "
                  f"of {after['form']['clientW']}")
        print(f"      submit buttons in .eo-form on this page: {after.get('submitCount')}")
        for s in (after.get("submits") or [])[:2]:
            print(f"      submit <{s['tag']} value={s['value']!r}> w={s['w']} R{s['right']} "
                  f"font={s['fs']} {s['ff']} width={s['width']} minW={s['minW']} maxW={s['maxW']} "
                  f"scroll/client {s['scrollW']}/{s['clientW']}")
        for r in after["rows"][:2]:
            row, inp = r["row"], r["input"]
            print(f"      row w={row['w']} L{row['left']} R{row['right']} minW={row['minW']} "
                  f"maxW={row['maxW']} scroll/client {row['scrollW']}/{row['clientW']}"
                  + (f" | input w={inp['w']} R{inp['right']} size={inp['size']} minW={inp['minW']} "
                     f"width={inp['width']} font={inp['fs']} scroll/client {inp['scrollW']}/{inp['clientW']}"
                     if inp else ""))
        c.close()
    b.close()


def main():
    args = sys.argv[1:]
    base = args[0] if args and not args[0].startswith("--") else BASE
    engine, page, width, font = "webkit", "about", 320, 48
    for flag, cast in (("--engine", str), ("--page", str), ("--width", int), ("--font", int)):
        if flag in args:
            v = cast(args[args.index(flag) + 1])
            if flag == "--engine":
                engine = v
            elif flag == "--page":
                page = v
            elif flag == "--width":
                width = v
            else:
                font = v
    only = set(args[args.index("--rule") + 1].split(",")) if "--rule" in args else None
    rnd = args[args.index("--round") + 1] if "--round" in args else "1"
    rules = {"1": RULES1, "2": RULES2, "3": RULES3, "4": RULES4,
             "all": RULES1 + RULES2 + RULES3 + RULES4}[rnd]
    reps = int(args[args.index("--repeat") + 1]) if "--repeat" in args else 1
    with sync_playwright() as pw:
        for i in range(reps):
            print(f"\n=== {page} @ {width}px root {font}px, {engine}"
                  + (f", pass {i + 1} of {reps}" if reps > 1 else "") + " ===")
            run(pw, engine, base, page, width, font, only, rules)


if __name__ == "__main__":
    main()
