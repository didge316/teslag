/*!
* Start Bootstrap - Blog Post v5.0.9 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

/* Status Checker (scarcity widget) - Version 1 */
(function () {
    'use strict';
    var SITE_URL = 'https://teslamagneticgenerator.com/';
    var DOWNTIME_DAYS = 12;

    function formatDate(date) {
        return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    }
    function formatDateShort(date) {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
    function getToday() {
        var d = new Date();
        d.setHours(0, 0, 0, 0);
        return d;
    }
    function daysAgo(n) {
        var d = new Date();
        d.setDate(d.getDate() - n);
        d.setHours(0, 0, 0, 0);
        return d;
    }

    function renderV1(today) {
        var timeline = document.getElementById('v1-timeline');
        var caption = document.getElementById('v1-caption');
        if (!timeline || !caption) return;
        timeline.innerHTML = '';

        var offlineEnd = daysAgo(2);
        var offlineStart = new Date(offlineEnd);
        offlineStart.setDate(offlineStart.getDate() - DOWNTIME_DAYS + 1);

        var d = new Date(offlineStart);
        while (d <= offlineEnd) {
            var dayEl = document.createElement('div');
            dayEl.className = 'v1-day';
            var dot = document.createElement('div');
            dot.className = 'v1-dot red';
            var label = document.createElement('span');
            label.className = 'v1-day-label';
            label.textContent = d.getDate();
            dayEl.appendChild(dot);
            dayEl.appendChild(label);
            timeline.appendChild(dayEl);
            d.setDate(d.getDate() + 1);
        }

        var yesterdayEl = document.createElement('div');
        yesterdayEl.className = 'v1-day';
        var yesterdayDot = document.createElement('div');
        yesterdayDot.className = 'v1-dot green';
        var yesterdayLabel = document.createElement('span');
        yesterdayLabel.className = 'v1-day-label';
        yesterdayLabel.textContent = daysAgo(1).getDate();
        yesterdayEl.appendChild(yesterdayDot);
        yesterdayEl.appendChild(yesterdayLabel);
        timeline.appendChild(yesterdayEl);

        var todayEl = document.createElement('div');
        todayEl.className = 'v1-day';
        var todayDot = document.createElement('div');
        todayDot.className = 'v1-dot green';
        var todayLabel = document.createElement('span');
        todayLabel.className = 'v1-day-label';
        todayLabel.textContent = today.getDate();
        todayEl.appendChild(todayDot);
        todayEl.appendChild(todayLabel);
        timeline.appendChild(todayEl);

        caption.textContent = 'Offline for ' + DOWNTIME_DAYS + ' days — came back online ' + formatDateShort(daysAgo(1));
    }

    function showOnline(vNum, today) {
        var section = document.getElementById('v' + vNum + '-section');
        if (!section) return;
        var bar = section.querySelector('.v1-status-bar');
        if (bar) {
            var badge = bar.querySelector('.v6-live-badge');
            if (badge) {
                badge.className = 'v6-live-badge online';
                var badgeDot = badge.querySelector('.v6-live-dot');
                if (badgeDot) badgeDot.className = 'v6-live-dot online';
            }
            var text = bar.querySelector('.v-status-badge-text');
            if (text) text.textContent = 'The Tesla generator website has been back online for the last 2 days';
        }
        if (vNum === 1) renderV1(today);
    }

    function showOffline(vNum, today) {
        var section = document.getElementById('v' + vNum + '-section');
        if (!section) return;
        var bar = section.querySelector('.v1-status-bar');
        if (bar) {
            var badge = bar.querySelector('.v6-live-badge');
            if (badge) {
                badge.className = 'v6-live-badge offline';
                var badgeDot = badge.querySelector('.v6-live-dot');
                if (badgeDot) badgeDot.className = 'v6-live-dot offline';
            }
            var text = bar.querySelector('.v-status-badge-text');
            if (text) text.textContent = 'Offline Today';
        }
        if (vNum === 1) renderV1(today);
    }

    function runChecker(versionNum) {
        var section = document.getElementById('v' + versionNum + '-section');
        if (!section) return;
        var spinner = section.querySelector('.v-spinner');
        var result = document.getElementById('v' + versionNum + '-result');
        if (!spinner || !result) return;

        setTimeout(function () {
            spinner.style.display = 'none';
            result.style.display = 'block';

            var today = getToday();
            var dateEl = document.getElementById('v' + versionNum + '-date');
            if (dateEl) dateEl.textContent = formatDate(today);

            fetch(SITE_URL, { mode: 'no-cors' })
                .then(function () { showOnline(versionNum, today); })
                .catch(function () { showOffline(versionNum, today); });
        }, 2000);
    }

    function initStatusChecker() {
        if (!document.getElementById('v1-section')) return;
        runChecker(1);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initStatusChecker);
    } else {
        initStatusChecker();
    }
})();

/* ---------------------------------------------------------------------------
 * Mobile sticky offer bar
 *
 * Mobile only. On lg+ the sidebar already carries the offer (square ad,
 * tower ad, email form), so a fixed bar there would only steal viewport.
 *
 * Deliberately non-intrusive: it does not appear until the reader is past the
 * intro, it hides itself once the footer is on screen, and dismissal is
 * remembered permanently rather than nagging on the next page.
 *
 * Appended to scripts.js so it ships to every page without touching the HTML.
 * ------------------------------------------------------------------------- */
(function () {
    'use strict';

    var CONFIG = {
        OFFER_BASE: 'https://d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net/',
        DISMISS_KEY: 'tmg_sticky_cta_dismissed',
        SHOW_AFTER_PX: 700,
        LG_BREAKPOINT: 992,
        // Lifetime of the dismissal fallback cookie, in seconds. Measured in
        // real Brave: a session cookie is browser-session scoped, not tab
        // scoped, so dismissing in one tab kept the bar hidden in a brand-new
        // tab of the same browser and only quitting the browser brought it back.
        // Half an hour outlasts every page view a visitor actually strings
        // together - the whole job of the fallback - while a mis-tap costs half
        // an hour of the offer instead of the rest of a browsing session.
        // sessionStorage still carries the per-tab semantics where it works.
        DISMISS_COOKIE_TTL: 1800,
        // No height budget, no tiers, no measured reserved height. Every size
        // in the bar is capped in CSS, so its rendered height is deterministic
        // per breakpoint and styles-custom.css reserves it as a constant. The bar
        // used to be sized in rem and to shed content in JS tiers driven by a
        // measured viewport budget, because the site's own text-size control
        // (wp-textsize sets the root font) could inflate it from 87px to 270px.
        // That design made correctness depend on the one measurement no desktop
        // instrument can be trusted for: on iOS Safari innerHeight swings ~110px
        // with the toolbar, and documentElement.clientHeight staying pinned is a
        // published assumption we have never measured, and there is no iPhone or
        // Mac here to measure it on. So the dependency is deleted rather than
        // verified harder.
        BAR_ID: 'tmg-sticky-cta'
    };

    // One tid across 53 pages would tell us that the bar works but never where.
    // Derive the template from the pathname so no HTML has to be touched.
    var TID_RULES = [
        // Trailing slash is optional on every anchored rule: Cloudflare Pages
        // 308-redirects /x/ to /x, but a rule that only accepts one form leaves
        // /articles/ to fall through into the article bucket.
        [/^\/(index\.html)?\/?$/,                        'sticky_home'],
        [/^\/articles(\.html)?\/?$/,                     'sticky_hub'],
        // The scam page is the site's least commercial, most trust-building URL.
        // Filed under sticky_review it would be the worst-converting row in that
        // bucket and would drag its EPC down for reasons unrelated to the bar.
        [/scam/,                                          'sticky_scam'],
        [/(worth-it|review|plans|vs-|cost|materials)/,   'sticky_review'],
        [/(for-|guide|how-to|diy|beginner|step)/,        'sticky_guide']
        // Rule order decides overlaps on purpose: review-style terms win over
        // guide-style ones, so a slug like /diy-cost-guide counts as a review.
    ];

    function tidFor(path) {
        var p = path.toLowerCase();
        for (var i = 0; i < TID_RULES.length; i++) {
            if (TID_RULES[i][0].test(p)) return TID_RULES[i][1];
        }
        return 'sticky_article';
    }

    // sessionStorage is the primary store on purpose: a dismissal must not
    // outlive the visit. At ~210 clicks a month the site cannot afford to kill
    // the offer permanently because one mis-tap landed on the dismiss control
    // sitting 24px from the CTA.
    //
    // Access can throw in some private-mode configurations, and a throw used to
    // mean isDismissed() returned false for the whole session so the bar
    // reappeared on every page - the exact nag the flag exists to prevent. A
    // cookie makes the fallback real instead of decorative.
    //
    // Max-Age rather than a session cookie, deliberately. A session cookie is
    // browser-session scoped, not tab scoped: measured in real Brave, dismissing
    // the bar in one tab kept it hidden in a freshly opened tab of the same
    // browser, and the only way back was to quit the browser. Half an hour is
    // long enough to outlast every page view a visitor actually strings together
    // - which is the whole job of the fallback - and short enough that a
    // mis-tap costs half an hour of the offer, not the rest of a browsing
    // session. sessionStorage still carries the per-tab semantics where it works.
    function store() {
        try {
            return window.sessionStorage || null;
        } catch (e) {
            return null;
        }
    }

    function isDismissed() {
        var s = store();
        if (s) {
            try {
                if (s.getItem(CONFIG.DISMISS_KEY) === '1') return true;
            } catch (e) { /* unreadable; fall through to the cookie */ }
        }
        return ('; ' + document.cookie).indexOf('; ' + CONFIG.DISMISS_KEY + '=') >= 0;
    }

    function rememberDismissal() {
        var s = store();
        if (s) {
            try { s.setItem(CONFIG.DISMISS_KEY, '1'); } catch (e) { /* quota/private */ }
        }
        try {
            document.cookie = CONFIG.DISMISS_KEY + '=1; path=/; SameSite=Lax; Max-Age=' +
                CONFIG.DISMISS_COOKIE_TTL;
        } catch (e) { /* cookies blocked outright; this page load still honors it */ }
    }

    function isDesktop() {
        // (pointer: coarse) first: a touch device is never desktop, whatever the
        // numbers say. On mobile the reported width can track overflowing
        // content rather than the viewport - at 300% root font on this site
        // documentElement.clientWidth stayed 390 while innerWidth reported 690 -
        // so a width-only test risks the bar deciding it is on a desktop and
        // never rendering at all, silently, for exactly the large-text users the
        // feature is most exposed to.
        if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) return false;
        // The same media query Bootstrap's grid uses to switch on the lg
        // columns, so the bar retires at exactly the width the sidebar offer
        // appears - which is the whole reason the bar is mobile-only. Comparing
        // a JS pixel width against 992 cannot reproduce that: clientWidth
        // excludes the scrollbar, so a 1000px window reports 985 and the bar
        // showed on real desktop Chrome up to ~1007px (measured in Brave at
        // 1000px; the suite missed it because it only tested 1440px).
        if (window.matchMedia) return window.matchMedia('(min-width: 992px)').matches;
        // No matchMedia at all: fall back to the layout viewport, never innerWidth.
        return document.documentElement.clientWidth >= CONFIG.LG_BREAKPOINT;
    }

    function buildBar() {
        var bar = document.createElement('div');
        bar.id = CONFIG.BAR_ID;
        bar.className = 'tmg-cta-bar';
        bar.setAttribute('role', 'complementary');
        bar.setAttribute('aria-label', 'Recommended generator plans');

        bar.innerHTML =
            '<div class="tmg-cta-copy">' +
                '<span class="tmg-cta-label">Ad &middot; affiliate</span>' +
                '<span class="tmg-cta-title">The plans we recommend</span>' +
                '<span class="tmg-cta-meta">~$47 &middot; instant download &middot; 60-day money-back guarantee</span>' +
                '<span class="tmg-cta-meta-sm">~$47 &middot; 60-day guarantee</span>' +
            '</div>' +
                '<a class="tmg-cta-btn" href="' + CONFIG.OFFER_BASE +
                    '?tid=' + tidFor(window.location.pathname) + '" target="_blank" ' +
                    'rel="noopener noreferrer sponsored nofollow">See the plans &rarr;' +
                    // Announced, not shown: WCAG 3.2.5 asks that a new tab be
                    // warned about in advance. Free, and it leaves the visual
                    // design untouched.
                    '<span class="tmg-sr-only"> (opens in a new tab)</span></a>' +
            '<button class="tmg-cta-close" type="button" aria-label="Dismiss this bar">&times;</button>';

        document.body.appendChild(bar);
        return bar;
    }

    function init() {
        if (document.getElementById(CONFIG.BAR_ID)) return;   // double-init guard
        if (isDismissed()) return;
        if (document.querySelector('.tmg-cta-btn')) return;   // never double up

        var bar = buildBar();
        var footer = document.querySelector('footer');
        var pastThreshold = false;
        var footerVisible = false;
        var ticking = false;
        var wasShown = false;
        // paint() is driven by scroll, resize, the observer and focusout, and
        // none of those triggers know about the user's choice. Without this
        // flag, dismissing the bar blurs the close button, that blur fires
        // focusout, and paint() cheerfully puts the bar straight back - so the
        // dismiss button appears broken. Measured: three dismissal assertions
        // failed the moment the focusout trigger was added.
        var dismissed = false;

        function footerInView() {
            // documentElement.clientHeight, the layout viewport, not innerHeight:
            // on iOS innerHeight is ~110px smaller while the toolbar is
            // expanded, which would make the footer 'arrive' early and release
            // its reserved padding sooner than it should, on the trigger that
            // produces the visible jump. Either reading is now survivable, and
            // that is the point: this decides a show/hide, never a layout
            // dimension, so a wrong iOS reading costs a few dozen pixels of
            // early hiding instead of content covered by a bad reservation.
            var vh = document.documentElement.clientHeight || window.innerHeight;
            // With no footer to key off, the bar would never hide and would
            // permanently cover the bottom of the document. Fall back to the
            // end of the document so a footerless page still releases it.
            if (!footer) {
                return (vh + window.scrollY) >= document.documentElement.scrollHeight - 4;
            }
            var rect = footer.getBoundingClientRect();
            return rect.top < vh;
        }


        // The bar never hides itself while it holds focus, so the only paths
        // here are exits the user did not choose: a resize to desktop, or the
        // dismiss control. Nothing needs to be focus()-ed afterwards: the
        // invariant above means no control is ever pulled out from under a
        // keyboard user, and parking focus on the h1 would dump a screen
        // reader's virtual cursor at the top of the document, which is the
        // exact failure this was meant to avoid.
        function releaseFocus() {
            var a = document.activeElement;
            if (!a || a === document.body || !bar.contains(a)) return;
            a.blur();
        }

        // The CSS constant reserves the space the bar needs. This only ever
        // GROWS it, and it measures the bar itself (bar.offsetHeight) rather
        // than any viewport dimension, because that is the one number every
        // engine gets right. Font fallback differs per engine, so at a 390px
        // viewport the title lays out on one line in Chromium and WebKit (bar
        // 87px) and on two in Firefox's DejaVu fallback (bar 105px) - measured
        // across all three. Sizing the CSS constant for the median engine left
        // Firefox with the bar sitting 18px on top of real content; sizing it
        // for the worst engine puts a blank band under the footer for everybody
        // else. So the constant stays tight and this nets the difference, in one
        // direction only, so it cannot oscillate.
        //
        // It deliberately never reads the viewport. The design this replaces
        // derived a layout dimension from a viewport reading, and on iOS Safari
        // that reading is the one number there is no trustworthy instrument for
        // here; a bar's own height is not one of those numbers.
        function setPad(show) {
            document.body.classList.toggle('tmg-cta-pad', show);
            if (!show) document.body.style.paddingBottom = '';
        }

        function growPad() {
            if (!bar.classList.contains('is-visible')) return;
            var h = bar.offsetHeight;
            if (!h) return;
            var cur = parseFloat(window.getComputedStyle(document.body).paddingBottom);
            if (isNaN(cur)) cur = 0;
            if (h > cur + 0.5) document.body.style.paddingBottom = h + 'px';
        }

        function paint() {
            // Clear the frame flag first: a dismissal can leave an rAF already
            // queued, and returning above the reset would latch ticking true for
            // the rest of the page's life.
            ticking = false;
            if (dismissed) return;
            // Desktop: never render, regardless of scroll position.
            if (isDesktop()) {
                if (wasShown) releaseFocus();
                bar.classList.remove('is-visible');
                setPad(false);
                wasShown = false;
                return;
            }
            var show = pastThreshold && !footerVisible;
            // Never pull the control out from under a keyboard user.
            if (!show && bar.contains(document.activeElement)) show = true;
            if (wasShown && !show) releaseFocus();   // before display:none
            bar.classList.toggle('is-visible', show);
            setPad(show);
            // Growing the reservation on the reveal is the point of growPad():
            // one layout read on a transition, never one per scroll frame.
            if (show && !wasShown) growPad();
            wasShown = show;
        }

        function onScroll() {
            pastThreshold = (window.scrollY || window.pageYOffset) > CONFIG.SHOW_AFTER_PX;
            footerVisible = footerInView();
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(paint);
            }
        }

        bar.querySelector('.tmg-cta-close').addEventListener('click', function () {
            releaseFocus();          // move focus out before the control vanishes
            rememberDismissal();
            dismissed = true;
            bar.classList.remove('is-visible');
            setPad(false);
            wasShown = false;
            window.removeEventListener('scroll', onScroll);
            window.removeEventListener('resize', onScroll);
            bar.removeEventListener('focusout', onScroll);
        });

        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll);
        // The focus invariant holds the bar up while it contains focus, but
        // nothing re-ran paint() when focus left: tabbing out of the CTA with
        // the footer in view left the bar sitting on top of the footer links
        // until the user's next scroll.
        bar.addEventListener('focusout', onScroll);
        // Exactly three things can change the bar's rendered height: the reveal
        // (handled above), a resize, and the site webfont settling in after
        // first paint - a wider face can push the title onto a second line. Not
        // scroll: the bar does not change height while you scroll, and measuring
        // it on a scroll frame is how this feature got its first perf bug.
        window.addEventListener('resize', growPad);
        if (document.fonts && document.fonts.ready && document.fonts.ready.then) {
            document.fonts.ready.then(growPad);
        }
        onScroll();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
