'use strict';

/* ============================================================
   SA4 — JAVASCRIPT
   treehouse. events | treehouseevents.cliffeliz.ai
   Vanilla JS only. No jQuery. No external libraries.
   ============================================================ */

/* ────────────────────────────────────────────────────────────
   CUSTOM CURSOR
   Only runs on pointer/mouse devices (not touch)
   ──────────────────────────────────────────────────────────── */
function initCursor() {
  // Skip on touch devices
  if (!window.matchMedia('(hover: hover)').matches) { return; }

  var cursor     = document.getElementById('cursor');
  var cursorRing = document.getElementById('cursor-ring');

  if (!cursor || !cursorRing) { return; }

  var cursorX = 0;
  var cursorY = 0;
  var ringX   = 0;
  var ringY   = 0;
  var rafId   = null;

  // Track mouse position
  document.addEventListener('mousemove', function(e) {
    cursorX = e.clientX;
    cursorY = e.clientY;

    cursor.style.left = cursorX + 'px';
    cursor.style.top  = cursorY + 'px';

    if (!rafId) {
      rafId = requestAnimationFrame(animateRing);
    }
  }, { passive: true });

  // Smooth ring follow via rAF
  function animateRing() {
    ringX += (cursorX - ringX) * 0.18;
    ringY += (cursorY - ringY) * 0.18;

    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top  = ringY + 'px';

    rafId = requestAnimationFrame(animateRing);
  }

  // Hover state on interactive elements
  var interactiveEls = document.querySelectorAll(
    'a, button, input, textarea, select, [role="button"], .gallery-item, .tab, .event-type-card'
  );

  interactiveEls.forEach(function(el) {
    el.addEventListener('mouseenter', function() {
      document.body.classList.add('cursor-hover');
    });
    el.addEventListener('mouseleave', function() {
      document.body.classList.remove('cursor-hover');
    });
  });

  // Inverted state on light sections
  var lightSections = document.querySelectorAll('.section-light');

  lightSections.forEach(function(section) {
    section.addEventListener('mouseenter', function() {
      document.body.classList.add('cursor-inverted');
    });
    section.addEventListener('mouseleave', function() {
      document.body.classList.remove('cursor-inverted');
    });
  });

  // Hide cursor when leaving window
  document.addEventListener('mouseleave', function() {
    cursor.style.opacity = '0';
    cursorRing.style.opacity = '0';
  });

  document.addEventListener('mouseenter', function() {
    cursor.style.opacity = '1';
    cursorRing.style.opacity = '0.7';
  });
}

/* ────────────────────────────────────────────────────────────
   STICKY NAV
   Adds .nav-scrolled class after 80px scroll
   ──────────────────────────────────────────────────────────── */
function initNav() {
  var nav = document.getElementById('nav');
  if (!nav) { return; }

  function onScroll() {
    if (window.scrollY > 80) {
      nav.classList.add('nav-scrolled');
    } else {
      nav.classList.remove('nav-scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
}

/* ────────────────────────────────────────────────────────────
   HAMBURGER MENU
   ──────────────────────────────────────────────────────────── */
function initMobileMenu() {
  var btn   = document.getElementById('hamburger-btn');
  var menu  = document.getElementById('mobile-menu');
  var close = document.getElementById('mobile-close');

  if (!btn || !menu) { return; }

  function openMenu() {
    menu.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    menu.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', openMenu);

  if (close) {
    close.addEventListener('click', closeMenu);
  }

  // Close on link click
  menu.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', closeMenu);
  });

  // Close on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !menu.hidden) {
      closeMenu();
      btn.focus();
    }
  });
}

/* ────────────────────────────────────────────────────────────
   SMOOTH SCROLL
   Intercepts anchor clicks and scrolls with nav offset
   ──────────────────────────────────────────────────────────── */
function initSmoothScroll() {
  var navHeight = parseInt(
    getComputedStyle(document.documentElement).getPropertyValue('--nav-height')
  ) || 72;

  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var hash = link.getAttribute('href');
      if (hash === '#') { return; }

      var target = document.querySelector(hash);
      if (!target) { return; }

      e.preventDefault();

      var targetTop = target.getBoundingClientRect().top + window.scrollY - navHeight;

      window.scrollTo({
        top: targetTop,
        behavior: 'smooth'
      });
    });
  });
}

/* ────────────────────────────────────────────────────────────
   SCROLL ANIMATIONS
   IntersectionObserver watches [data-animate] elements.
   Adds .visible on intersection. Disconnects after trigger.
   ──────────────────────────────────────────────────────────── */
function initScrollAnimations() {
  if (!('IntersectionObserver' in window)) {
    // Fallback: make everything visible immediately
    document.querySelectorAll('[data-animate]').forEach(function(el) {
      el.classList.add('visible');
    });
    return;
  }

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -40px 0px'
  });

  document.querySelectorAll('[data-animate]').forEach(function(el) {
    observer.observe(el);
  });
}

/* ────────────────────────────────────────────────────────────
   STAGGERED CHILDREN
   For elements with [data-stagger], auto-assign animation-delay
   to each direct child with 100ms increments
   ──────────────────────────────────────────────────────────── */
function initStagger() {
  document.querySelectorAll('[data-stagger]').forEach(function(parent) {
    Array.from(parent.children).forEach(function(child, i) {
      child.style.animationDelay = (i * 100) + 'ms';
    });
  });
}

/* ────────────────────────────────────────────────────────────
   GALLERY COLLECTION TABS
   Filters .gallery-item by data-collection attribute.
   Active tab gets .tab-active class.
   ──────────────────────────────────────────────────────────── */
function initGalleryTabs() {
  var tabs    = document.querySelectorAll('.gallery-tabs .tab');
  var items   = document.querySelectorAll('.gallery-item');

  if (!tabs.length || !items.length) { return; }

  function filterGallery(collection) {
    items.forEach(function(item) {
      if (collection === 'all' || item.getAttribute('data-collection') === collection) {
        item.classList.remove('hidden');
      } else {
        item.classList.add('hidden');
      }
    });
  }

  tabs.forEach(function(tab) {
    tab.addEventListener('click', function() {
      // Update active tab
      tabs.forEach(function(t) {
        t.classList.remove('tab-active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('tab-active');
      tab.setAttribute('aria-selected', 'true');

      // Filter items
      filterGallery(tab.getAttribute('data-collection') || 'all');
    });
  });
}

/* ────────────────────────────────────────────────────────────
   IMAGE ERROR HANDLING
   Global onerror fallback that adds .img-failed to parent
   (Inline onerror on each img tag handles individual images,
   this catches any that slip through)
   ──────────────────────────────────────────────────────────── */
function initImageFallbacks() {
  document.querySelectorAll('img').forEach(function(img) {
    if (img.complete && img.naturalWidth === 0) {
      img.parentNode.classList.add('img-failed');
    }

    img.addEventListener('error', function() {
      img.parentNode.classList.add('img-failed');
    });
  });
}

/* ────────────────────────────────────────────────────────────
   JOIN FORM
   Email validation + inline confirmation. No page reload.
   ──────────────────────────────────────────────────────────── */
function initJoinForm() {
  var form         = document.querySelector('.join-form');
  var emailInput   = document.getElementById('join-email');
  var confirmation = document.getElementById('join-confirmation');

  if (!form || !emailInput || !confirmation) { return; }

  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  form.addEventListener('submit', function(e) {
    e.preventDefault();

    var email = emailInput.value.trim();

    if (!emailRegex.test(email)) {
      emailInput.focus();
      emailInput.style.borderColor = 'var(--accent)';
      setTimeout(function() {
        emailInput.style.borderColor = '';
      }, 1500);
      return;
    }

    // Show confirmation
    confirmation.hidden = false;
    confirmation.classList.add('visible');
    emailInput.value    = '';

    // Optionally hide after 6 seconds
    setTimeout(function() {
      confirmation.classList.remove('visible');
      setTimeout(function() {
        confirmation.hidden = true;
      }, 400);
    }, 6000);
  });
}

/* ────────────────────────────────────────────────────────────
   HERO PARALLAX
   Subtle translateY on hero bg image via scroll.
   Max 80px movement. Pure JS, no libraries.
   ──────────────────────────────────────────────────────────── */
function initParallax() {
  var heroBg = document.querySelector('.hero-bg img');
  if (!heroBg) { return; }

  // Only run on larger screens (skip on mobile for performance)
  if (window.innerWidth < 768) { return; }

  function onScroll() {
    var scrollY = window.scrollY;
    var offset  = Math.min(scrollY * 0.3, 80);
    heroBg.style.transform = 'translateY(' + offset + 'px)';
  }

  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ────────────────────────────────────────────────────────────
   PAGE LOAD SEQUENCE
   Adds .page-loaded to <body> on DOMContentLoaded
   Triggers hero stagger animations via CSS
   ──────────────────────────────────────────────────────────── */
function initPageLoad() {
  document.body.classList.add('page-loaded');
}

/* ────────────────────────────────────────────────────────────
   INIT — run all modules on DOMContentLoaded
   ──────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function() {
  initPageLoad();
  initCursor();
  initNav();
  initMobileMenu();
  initSmoothScroll();
  initScrollAnimations();
  initStagger();
  initGalleryTabs();
  initImageFallbacks();
  initJoinForm();
  initParallax();
});
