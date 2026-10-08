/*
 * Exit-intent popup for the free 1919 Electrical Experimenter book.
 *
 * The sidebar form is EmailOctopus's own inline form (their embed script).
 * This popup is ours: it posts straight to the same EmailOctopus form
 * endpoint, so both placements feed the same list and the same 3-email
 * automation.
 *
 * Shows once per browser session, on exit intent (pointer leaves the top of
 * the viewport) or after DWELL_MS of reading as a fallback.
 */
(function () {
    'use strict';

    var FORM_ID = 'ca475970-c34a-11f1-9696-9df3578f190e';
    var ENDPOINT = 'https://eocampaign1.com/form/' + FORM_ID;
    var HONEYPOT = 'hpc4b27b6e-eb38-11e9-be00-06b4694bee2a';
    var SESSION_KEY = 'tesla_exit_popup_shown';
    var DWELL_MS = 25000;

    var shown = false;
    var lastX = 0;

    function alreadyShown() {
        try { return sessionStorage.getItem(SESSION_KEY) === 'true'; } catch (e) { return false; }
    }

    function markShown() {
        try { sessionStorage.setItem(SESSION_KEY, 'true'); } catch (e) { /* private mode */ }
    }

    function styles() {
        return [
            '.tesla-popup{position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;',
            'padding:16px;background:rgba(33,37,41,.72);font-family:"Noto sans",sans-serif;color:#212529}',
            '.tesla-popup[hidden]{display:none}',
            '.tesla-popup__panel{position:relative;background:#fff;max-width:420px;width:100%;padding:24px 22px;',
            'border-radius:6px;box-shadow:0 12px 40px rgba(0,0,0,.35);max-height:92vh;overflow:auto}',
            '.tesla-popup__close{position:absolute;top:8px;right:10px;width:30px;height:30px;padding:0;border:0;',
            'background:transparent;font-size:24px;line-height:1;color:#6c757d;cursor:pointer}',
            '.tesla-popup__close:hover{color:#212529}',
            '.tesla-popup__title{margin:0 0 12px;font-size:22px;font-weight:700;text-align:center;line-height:1.25}',
            '.tesla-popup img{display:block;width:100%;max-width:260px;margin:0 auto 14px;height:auto;border-radius:4px}',
            '.tesla-popup__field{margin-bottom:10px}',
            '.tesla-popup__field input{width:100%;padding:9px 12px;font-size:15px;font-family:inherit;color:#212529;',
            'background:#fff;border:1px solid #ced4da;border-radius:4px;box-sizing:border-box}',
            '.tesla-popup__field input:focus{outline:none;border-color:#438424;box-shadow:0 0 0 2px rgba(67,132,36,.2)}',
            '.tesla-popup__submit{display:block;width:100%;padding:10px 12px;margin-top:4px;border:0;border-radius:4px;',
            'background:#438424;color:#fff;font-size:16px;font-weight:700;font-family:inherit;cursor:pointer}',
            '.tesla-popup__submit:hover{background:#376e1e}',
            '.tesla-popup__submit[disabled]{opacity:.65;cursor:default}',
            '.tesla-popup__msg{margin:10px 0 0;font-size:13px;text-align:center;min-height:1em}',
            '.tesla-popup__msg.is-error{color:#b02a37}',
            '.tesla-popup__msg.is-ok{color:#438424;font-weight:700;font-size:15px}',
            '.tesla-popup__fine{margin:10px 0 0;font-size:11px;color:#6c757d;text-align:center}',
            '.tesla-popup__fine a{color:#6c757d}',
            '@media (max-width:575px){.tesla-popup__panel{padding:18px 16px}.tesla-popup__title{font-size:19px}}'
        ].join('');
    }

    function markup() {
        return [
            '<div class="tesla-popup__panel" role="dialog" aria-modal="true" aria-labelledby="tesla-popup-title">',
            '<button type="button" class="tesla-popup__close" aria-label="Close">&times;</button>',
            '<h2 class="tesla-popup__title" id="tesla-popup-title">Don\'t forget your free book!</h2>',
            '<img src="/assets/electrical-experimenter-cover.webp" width="343" height="424" alt="The Electrical Experimenter, 1919 issue cover">',
            '<form class="tesla-popup__form" novalidate>',
            '<div class="tesla-popup__field"><input type="text" name="field_1" placeholder="First name" aria-label="First name" autocomplete="given-name"></div>',
            '<div class="tesla-popup__field"><input type="email" name="field_0" placeholder="Email address" aria-label="Email address" required autocomplete="email"></div>',
            '<div aria-hidden="true" style="position:absolute;left:-9999px;top:-9999px">',
            '<input type="text" name="' + HONEYPOT + '" tabindex="-1" autocomplete="nope" value="">',
            '</div>',
            '<button type="submit" class="tesla-popup__submit">Download Now</button>',
            '<p class="tesla-popup__msg" role="status" aria-live="polite"></p>',
            '</form>',
            '<p class="tesla-popup__fine">The rare 1919 issue, free to download.</p>',
            '</div>'
        ].join('');
    }

    var root = null;

    function show() {
        if (shown || alreadyShown()) { return; }
        shown = true;
        markShown();

        var css = document.createElement('style');
        css.textContent = styles();
        document.head.appendChild(css);

        root = document.createElement('div');
        root.className = 'tesla-popup';
        root.hidden = true;
        root.innerHTML = markup();
        document.body.appendChild(root);

        root.hidden = false;

        var email = root.querySelector('[name="field_0"]');
        if (email) { email.focus({ preventScroll: true }); }

        root.querySelector('.tesla-popup__close').addEventListener('click', dismiss);
        root.addEventListener('click', function (e) { if (e.target === root) { dismiss(); } });
        document.addEventListener('keydown', onKey);
        root.querySelector('form').addEventListener('submit', submit);
    }

    function onKey(e) { if (e.key === 'Escape') { dismiss(); } }

    function dismiss() {
        if (!root) { return; }
        document.removeEventListener('keydown', onKey);
        root.remove();
        root = null;
    }

    function submit(e) {
        e.preventDefault();
        var form = e.target;
        var msg = form.querySelector('.tesla-popup__msg');
        var button = form.querySelector('.tesla-popup__submit');
        var email = form.querySelector('[name="field_0"]');

        msg.className = 'tesla-popup__msg';
        msg.textContent = '';

        if (!email.value || !/@[^@]+\.[^@]+/.test(email.value)) {
            msg.textContent = 'Please enter a valid email address.';
            msg.classList.add('is-error');
            email.focus();
            return;
        }

        button.disabled = true;
        button.textContent = 'Sending...';

        var body = new URLSearchParams();
        body.set('field_0', email.value.trim());
        body.set('field_1', form.querySelector('[name="field_1"]').value.trim());
        body.set(HONEYPOT, '');

        fetch(ENDPOINT, {
            method: 'POST',
            body: body,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            mode: 'cors'
        }).then(function (r) {
            return r.json().catch(function () { return {}; });
        }).then(function (data) {
            if (data && data.success) {
                form.innerHTML = '<p class="tesla-popup__msg is-ok">Check your email and enjoy free gift.</p>';
            } else {
                throw new Error('rejected');
            }
        }).catch(function () {
            button.disabled = false;
            button.textContent = 'Download Now';
            msg.textContent = 'Something went wrong - please use the form in the sidebar.';
            msg.classList.add('is-error');
        });
    }

    function exitIntent(e) {
        if (shown) { return; }
        var to = e.relatedTarget || e.toElement;
        if (to || e.clientY > 5) { return; }
        if (lastX > 0) { show(); }
    }

    function init() {
        if (alreadyShown()) { return; }
        document.addEventListener('mouseout', function (e) {
            lastX = e.clientX;
            exitIntent(e);
        });
        window.setTimeout(function () { show(); }, DWELL_MS);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
