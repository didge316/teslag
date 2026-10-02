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