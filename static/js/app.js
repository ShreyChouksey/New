/**
 * Babel Universal Image Archive — Client-Side Application
 */

(function() {
    'use strict';

    // =========================================================================
    // Mobile Navigation Toggle
    // =========================================================================

    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('open');
            navToggle.classList.toggle('active');
        });

        // Close nav on link click (mobile)
        navLinks.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                navLinks.classList.remove('open');
                navToggle.classList.remove('active');
            });
        });
    }

    // =========================================================================
    // Image Lazy Loading Enhancement
    // =========================================================================

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        }, { rootMargin: '100px' });

        document.querySelectorAll('.archive-image[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }

    // =========================================================================
    // Keyboard Shortcuts
    // =========================================================================

    document.addEventListener('keydown', function(e) {
        // Don't trigger shortcuts when typing in inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch(e.key) {
            case 'r':
                // R = Random page
                if (!e.ctrlKey && !e.metaKey) {
                    window.location.href = '/random';
                }
                break;
            case 'b':
                // B = Browse
                if (!e.ctrlKey && !e.metaKey) {
                    window.location.href = '/browse';
                }
                break;
            case 's':
                // S = Search
                if (!e.ctrlKey && !e.metaKey) {
                    window.location.href = '/search';
                }
                break;
            case 'g':
                // G = Gallery
                if (!e.ctrlKey && !e.metaKey) {
                    window.location.href = '/gallery';
                }
                break;
        }
    });

    // =========================================================================
    // Address Validation Helper
    // =========================================================================

    const BASE62_REGEX = /^[0-9A-Za-z]+$/;

    window.BabelArchive = {
        isValidAddress: function(address) {
            return address.length > 0 && BASE62_REGEX.test(address);
        },

        copyToClipboard: function(text) {
            return navigator.clipboard.writeText(text);
        },

        fetchRandomAddress: function() {
            return fetch('/api/v1/random?count=1')
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    return data.images[0].address;
                });
        }
    };

    // =========================================================================
    // Toast Notifications
    // =========================================================================

    window.BabelArchive.toast = function(message, duration) {
        duration = duration || 2000;
        var toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(function() {
            toast.classList.add('show');
        });

        setTimeout(function() {
            toast.classList.remove('show');
            setTimeout(function() {
                document.body.removeChild(toast);
            }, 300);
        }, duration);
    };

})();
