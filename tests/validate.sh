#!/usr/bin/env bash
# The runner for everything items 5/6/7 claim, kept in git because "run the tests"
# is not a claim until it is a file. Sequential on purpose: these are geometry
# measurements and CPU contention is how a timing-sensitive one starts lying
# (gate.py's Firefox rows timed out at 30s under load; they now allow 60s and
# retry once, which is a measurement fix and not a tolerance for flakiness).
#
# webkit is run LAST and on its own here. It died twice at ~5 minutes with
# `TargetClosedError` while three engines ran at once; a browser that dies
# silently mid-matrix and a browser that passes one look identical from the
# summary line, which is exactly the failure gate.py now refuses to report (it
# exits 2 and prints no verdicts until its control and canary lines are out).
#
# Nothing here pattern-kills anything. A `pkill -f chrome-headless-shell` of
# mine, issued as tidy-up while two definitive runs were in flight, killed both
# of them and left 76KB of traceback where a result should be.
#
# The stage servers must already be running, and there are two of them because
# they measure two different trees, which is a distinction this branch nearly
# lost:
#   :8199  the working tree           python3 -m http.server 8199 --bind 127.0.0.1   (site root)
#   :8200  what the branch will ship  python3 -m http.server 8200 --bind 127.0.0.1   (from tests/.staging/site-shipped)
# The working tree carries somebody else's unfinished work - among it js/scripts.js
# with the sticky bar, which is in NO commit on this branch - so geometry quoted
# against :8199 is not geometry the branch ships. Step 0 rebuilds the second tree
# from HEAD. The only step that belongs on :8199 is the sticky-CTA suite, because
# the bar it guards does not exist anywhere else.
set -u
SITE=/home/matt/projects/other/tesla-generator/website
BASE=http://127.0.0.1:8199            # working tree: sticky-CTA only, and nav is identical either way
MEASURED=http://127.0.0.1:8200        # the tree the branch will ship: every geometry claim

cd "$SITE" || exit 1
for port in 8199 8200; do
  code=$(curl -sfo /dev/null -w '%{http_code}' "http://127.0.0.1:$port/index.html" || echo 000)
  [ "$code" = 200 ] || { echo "http://127.0.0.1:$port is not serving (got $code). Start both servers (see above); a missing one is not a pass."; exit 2; }
done

cd "$SITE" || exit 1
# The committed page list, from git rather than a file in /tmp: 52 pages as this
# branch was written. The working tree has 53 because an undeleted restore of a
# page deleted in c3232e0 (electrical-experimenter.html) is sitting untracked;
# measuring it is fine, quoting it as part of this branch is not.
PAGES=$(git ls-files '*.html' | xargs -n1 basename | sed 's/\.html$//' | paste -sd, -)
echo "pages from git: $(echo "$PAGES" | tr ',' '\n' | wc -l)"

echo "### 0/9 rebuild the tree the branch will actually ship (from HEAD, not from this tree) ###"
python3 tests/ship/stage.py shipped | tail -3
test -f tests/.staging/site-shipped/index.html || { echo "no measured copy - see tests/ship/README.md"; exit 2; }

# Both servers are checked above and the exit codes below are the instruments' own:
# 0 green, 1 defect, 2 the check could not decide. Do not read a step that printed
# nothing as a pass - and do not read a file whose tail is a traceback as a
# measurement. Twice on this branch a number was already in my notes before the
# artefact was checked.
cd "$SITE/tests/overflow" || exit 1
echo "### 1/9 provenance: does the stylesheet on disk still say what the measured bytes said? ###"
python3 css-comment-only.py

echo "### 2/9 the same gate with item 7's CSS regions cut out (the before half) ###"
python3 gate.py "$MEASURED" --before-css --only "$PAGES" 2>&1 | tee gate-BEFORE-cssregions.txt | tail -4

echo "### 3/9 gate.py chromium, 52 pages x 12 cells ###"
python3 gate.py "$MEASURED" --only "$PAGES" 2>&1 | tee gate-FINAL-chromium.txt | tail -4

echo "### 4/9 gate.py firefox ###"
python3 gate.py "$MEASURED" --engine firefox --only "$PAGES" 2>&1 | tee gate-FINAL-firefox.txt | tail -4

echo "### 5/9 inert-at-100.py: is the CSS inert at root 16px (boxes, ink, lines) ###"
python3 inert-at-100.py "$MEASURED" 2>&1 | tee inert-100.txt | tail -4

echo "### 6/9 sticky-CTA suite, three engines (ON :8199 - the bar is only in the working tree) ###"
cd "$SITE/tests/sticky-cta" || exit 1
for e in chromium webkit firefox; do
  python3 run.py "$BASE" --engine "$e" 2>&1 | tail -3 | sed "s/^/  [$e] /"
done
python3 engines.py "$BASE" 2>&1 | tail -4

echo "### 7/9 nav: template, coverage of destinations, drawer, keyboard, open menus ###"
cd "$SITE" || exit 1
python3 tests/nav/apply_nav.py --check 2>&1 | tail -6
for w in 390 320; do
  echo "  -- DRAWER_W=$w"
  DRAWER_W=$w python3 tests/nav/verify.py "$MEASURED" 2>&1 | grep -E "FAIL|PASS-EXTRA|green" | tail -6
done

echo "### 8/9 img-alt: alt inventory and the glued-attribute class ###"
python3 tests/img-alt/inventory.py 2>&1 | tail -8
python3 tests/img-alt/space-fix.py --dry-run 2>&1 | tail -2

echo "### 9/9 webkit, alone, last ###"
cd "$SITE/tests/overflow" || exit 1
python3 gate.py "$MEASURED" --engine webkit --only "$PAGES" 2>&1 | tee gate-FINAL-webkit.txt | tail -4
echo "QUEUE_DONE"
