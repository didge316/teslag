// Redirect on leave — sends external clicks to ClickBank offer
(function() {
    'use strict';
    
    var CLICKBANK_REDIRECT = 'https://d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net/?tid=leave_redirect';
    var SITE_HOST = window.location.hostname;
    
    // Don't redirect if already on ClickBank or the ESP
    var skipDomains = [
        SITE_HOST,
        'clickbank.net',
        'eocampaign1.com',
        'emailoctopus.com'
    ];
    
    document.addEventListener('click', function(e) {
        var target = e.target.closest('a');
        if (!target) return;
        
        var href = target.getAttribute('href');
        if (!href) return;
        
        // Skip internal links, mailto, tel, #
        if (href.startsWith('#') || href.startsWith('mailto:') || 
            href.startsWith('tel:') || href.startsWith('javascript:')) return;
        
        // Check if external
        try {
            var url = new URL(href, window.location.origin);
            var isExternal = url.hostname !== SITE_HOST;
            
            if (isExternal) {
                // Check if domain should be skipped
                var shouldSkip = false;
                for (var i = 0; i < skipDomains.length; i++) {
                    if (url.hostname === skipDomains[i] || url.hostname.endsWith('.' + skipDomains[i])) {
                        shouldSkip = true;
                        break;
                    }
                }
                
                if (!shouldSkip) {
                    e.preventDefault();
                    window.location.href = CLICKBANK_REDIRECT;
                }
            }
        } catch(err) {
            // Protocol-relative or relative URLs — skip
        }
    });
})();
