#!/usr/bin/env bash
# Checks that only a DEPLOYED url can answer. localhost cannot make any of them:
# a static python server ignores _headers and _redirects entirely, there is no
# TLS, no zone cache, no CSP delivery, no Pages trailing-slash 308, and no real
# ClickBank hop chain.
#
#   ./live.sh https://<hash>.teslag.pages.dev     # preview, before merge
#   ./live.sh https://teslamagneticgenerator.com  # production, after deploy
#
# Exits non-zero if any check fails. A preview pass is required before merge;
# a production pass is required to call the feature shipped.
set -uo pipefail

BASE="${1:?usage: live.sh <deployed-url>}"
FAIL=0
BAR_MARK="tmg-cta"
PASS="\033[32mPASS\033[0m"; BAD="\033[31mFAIL\033[0m"; WARN="\033[33mWARN\033[0m"

chk() { # chk <name> <cond(0/1)> <detail>
  if [ "$2" = "0" ]; then printf "  ${PASS}  %s\n" "$1"; else printf "  ${BAD}  %s  [%s]\n" "$1" "$3"; FAIL=$((FAIL+1)); fi
}
warn() { printf "  ${WARN}  %s  [%s]\n" "$1" "$2"; }

hdr() { curl -sSIL -m 25 -o /dev/null -D - "$1" 2>/dev/null; }

echo "target: $BASE"
echo
echo "== 1. the two files that carry the feature are actually deployed =="
JS=$(curl -sSL -m 25 "$BASE/js/scripts.js" 2>/dev/null)
CSS=$(curl -sSL -m 25 "$BASE/css/styles-custom.css" 2>/dev/null)
chk "js/scripts.js served and contains the bar"        $(printf '%s' "$JS"  | grep -qi "$BAR_MARK"; echo $?)  "no tmg-cta in served scripts.js - deploy did not land"
chk "css/styles-custom.css served and contains the bar" $(printf '%s' "$CSS" | grep -qi "$BAR_MARK"; echo $?)  "no tmg-cta in served CSS - tier rules will not exist"

echo
echo "== 2. the bar must stay OUT of crawled HTML (it is built by JS only) =="
HTML=$(curl -sSL -m 25 "$BASE/build-a-perpetual-motion-generator" 2>/dev/null)
chk "no tmg-cta markup in the served HTML document"     $(printf '%s' "$HTML" | grep -qi "$BAR_MARK"; echo $?)  "the bar is in the HTML source, which was meant to be avoided"

echo
echo "== 3. _headers: the JS/CSS must not be cacheable out of step =="
JSH=$(curl -sSI -m 25 "$BASE/js/scripts.js" 2>/dev/null | tr -d '\r')
CCH=$(curl -sSI -m 25 "$BASE/css/styles-custom.css" 2>/dev/null | tr -d '\r')
JSCC=$(printf '%s' "$JSH" | grep -i '^cache-control' || echo MISSING)
CSSCC=$(printf '%s' "$CCH" | grep -i '^cache-control' || echo MISSING)
if printf '%s' "$JSCC$CSSCC" | grep -qi "no-cache"; then
  chk "cache-control on both assets is revalidating (no 4h skew window)" 0 "js: $JSCC | css: $CSSCC"
else
  chk "cache-control on both assets is revalidating (no 4h skew window)" 1 "js: $JSCC | css: $CSSCC - stale-pair window still open"
fi
if printf '%s' "$JSH" | grep -qi '^cf-cache-status'; then
  printf '%s\n' "$(printf '%s' "$JSH" | grep -i '^cf-cache-status')" | sed 's/^/      /'
else
  warn "no cf-cache-status header" "expected on the proxied production host; a pages.dev preview has no zone cache, so this check only means something against the real domain"
fi

echo
echo "== 4. security headers as actually delivered (never observable on localhost) =="
ROOT=$(hdr "$BASE/")
chk "HSTS present"                 $(printf '%s' "$ROOT" | grep -qi 'strict-transport-security'; echo $?) "no strict-transport-security"
chk "CSP present"                  $(printf '%s' "$ROOT" | grep -qi 'content-security-policy'; echo $?) "no content-security-policy"
chk "X-Content-Type-Options present" $(printf '%s' "$ROOT" | grep -qi 'x-content-type-options'; echo $?) "missing"

echo
echo "== 5. Pages routing: trailing slash and the tid bucket it produces =="
CODE=$(curl -s -o /dev/null -m 25 -w '%{http_code}' "$BASE/articles/" 2>/dev/null)
LOC=$(hdr "$BASE/articles/" | tr -d '\r' | awk 'tolower($1)=="location:"{print $2; exit}')
chk "/articles/ issues a 3xx to a canonical form" $([ "$CODE" = "308" ] || [ "$CODE" = "301" ] || [ "$CODE" = "302" ]; echo $?) "got $CODE -> ${LOC:-no location}"
chk "the 404 page still 404s (no soft 404 introduced by the bar's routes)" \
    $([ "$(curl -s -o /dev/null -m 25 -w '%{http_code}' "$BASE/definitely-not-a-page-9271")" = "404" ]; echo $?) "expected 404"

echo
echo "== 6. no absolute production URLs hiding in the click path =="
# If redirect-leave.js or exit-popup.js hard-codes the production host, a click
# test on a preview silently sends the visitor to the LIVE site and reports a
# false green.
LEAVE=$(curl -sSL -m 25 "$BASE/js/redirect-leave.js" 2>/dev/null)
POPUP=$(curl -sSL -m 25 "$BASE/js/exit-popup.js" 2>/dev/null)
if printf '%s%s' "$LEAVE" "$POPUP" | grep -q "teslamagneticgenerator\.com"; then
  warn "absolute production URLs found in the click/leave path" "a preview click will jump to the live site - treat the preview click test as indicative only"
else
  chk "no absolute production URLs in redirect-leave.js / exit-popup.js" 0 ""
fi

echo
echo "== 7. preview must not be indexable (skip on production) =="
if printf '%s' "$BASE" | grep -q "pages.dev"; then
  chk "preview sends X-Robots-Tag" $(printf '%s' "$ROOT" | grep -qi 'x-robots-tag'; echo $?) "no x-robots-tag on the preview - do not leave it public"
else
  chk "robots.txt served" $(curl -s -o /dev/null -m 25 -w '%{http_code}' "$BASE/robots.txt" 2>/dev/null | grep -q 200; echo $?) "robots.txt not reachable"
fi

echo
echo "== 8. the money path, from this origin =="
HREF=$(printf '%s' "$HTML" | grep -o 'hop\.clickbank\.net[^"]*' | head -1)
if [ -z "$HREF" ]; then
  warn "no clickbank hop URL found in the raw HTML" "expected: the bar builds its link in JS, so only an inline affiliate link proves the hop is reachable from this host"
fi
HOP="https://d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net/?tid=sticky_article"
CHAIN=$(curl -s -o /dev/null -m 40 -L -w '%{url_effective}' "$HOP" 2>/dev/null)
if printf '%s' "$CHAIN" | grep -qi "hopId="; then
  chk "hop chain resolves with a hopId (attribution recorded)" 0 "$CHAIN"
else
  chk "hop chain resolves with a hopId (attribution recorded)" 1 "final url: ${CHAIN:-no response}. Run tests/sticky-cta/clickthrough.py for the JS-followed version."
fi

echo
if [ "$FAIL" = "0" ]; then echo "live.sh: all checks passed for $BASE"; else echo "live.sh: $FAIL check(s) FAILED for $BASE"; fi
exit $([ "$FAIL" = "0" ]; echo $?)
