# Treehouse Events — Phase 1 Technical & Design Audit

**Date:** April 6, 2026  
**Auditor:** Manus AI  
**Scope:** `index.html`, `sponsor.html`, `styles.css`, `photos.js`

This document details the findings of a comprehensive Phase 1 audit of the Treehouse Events web properties. The review covers typography, visual design, code quality, performance, SEO, accessibility, and backend architecture. No code changes have been applied during this phase.

---

## 1. Typography & Sizing Inventory

The following tables document the current CSS `font-size` declarations for key text elements across both pages. The site relies heavily on `clamp()` functions for responsive scaling.

### `index.html` (Homepage)

| Element | CSS Selector | Font Family | Size Declaration | Notes |
|---|---|---|---|---|
| Hero "Treehouse" Logo | `.hero-wm img` | N/A | `height: 120px` | Image replacement |
| Next Event Heading | `.curate-copy h2` | `var(--ff-d)` | `clamp(2.5rem, 5vw, 4.5rem)` | |
| Section Headings (e.g. "Some nights") | `.ev-title` | `var(--ff-d)` | `clamp(3.5rem, 8vw, 7rem)` | |
| Section Subtitles | `.ev-desc` | `var(--ff-e)` | `0.92rem` | Italicized |
| Section Labels (e.g. "// The Vibe") | `.lbl` | `var(--ff-b)` | `0.75rem` | |
| Event Dates | `.ev-date` | `var(--ff-b)` | `0.68rem` | |
| Photo Credits | `.ev-credit` | `var(--ff-e)` | `0.62rem` | Italicized |
| How to Get In Headings | `.hiw-t` | `var(--ff-e)` | `1.05rem` | |
| How to Get In Body | `.hiw-d` | `var(--ff-b)` | `0.83rem` | |
| Footer Links | `.foot-links a` | `var(--ff-b)` | `0.68rem` | |

### `sponsor.html` (Sponsor Page)

| Element | CSS Selector | Font Family | Size Declaration | Notes |
|---|---|---|---|---|
| Hero H1 | `.sp-hero-h1` | `var(--ff-d)` | `clamp(3.5rem, 9vw, 8rem)` | |
| Hero Subtitle | `.sp-hero-sub` | `var(--ff-b)` | `clamp(1rem, 2vw, 1.2rem)` | |
| Section Labels | `.sp-stats-label`, `.lbl` | `var(--ff-b)` | `0.9rem` | Increased in Round 39 |
| Stat Numbers | `.sp-stat-num` | `var(--ff-d)` | `clamp(6rem, 11vw, 9rem)` | Increased in Round 39 |
| Stat Descriptions | `.sp-stat-label` | `var(--ff-b)` | `1rem` | Increased in Round 39 |
| Stat Body Text | `.sp-stats-venues p` | `var(--ff-e)` | `1.15rem` | Increased in Round 39 |
| Quote Text | `.sp-stats-quote blockquote` | `var(--ff-e)` | `1.2rem` | Increased in Round 39 |
| Quote Citation | `.sp-stats-quote cite` | `var(--ff-b)` | `0.82rem` | |
| Packages H2 | `.sp-packages-header h2` | `var(--ff-d)` | `clamp(4.5rem, 6vw, 6rem)` | Increased in Round 39 |
| Tier Names | `.sp-tier-name` | `var(--ff-d)` | `clamp(2rem, 4vw, 3.5rem)` | |
| Tier Prices | `.sp-tier-price` | `var(--ff-b)` | `1.75rem` | |
| Tier Descriptions | `.sp-tier-desc` | `var(--ff-e)` | `1.05rem` | Increased in Round 39 |
| Tier Line Items | `.sp-tier-feats li` | `var(--ff-b)` | `1.05rem` | Increased in Round 39 |
| Tier Disclaimer | `.sp-tiers-note` | `var(--ff-b)` | `0.95rem` | Increased in Round 39 |
| Contact H2 | `.sp-contact-inner h2` | `var(--ff-d)` | `clamp(4rem, 5vw, 5.5rem)` | Increased in Round 39 |
| Contact Body | `.sp-contact-body` | `var(--ff-b)` | `1.15rem` | Increased in Round 39 |
| Form Labels | `.sp-form label` | `var(--ff-b)` | `0.85rem` | Increased in Round 39 |
| Form Inputs | `.sp-form input`, etc. | `var(--ff-b)` | `1rem` | Increased in Round 39 (prevents iOS zoom) |

---

## 2. Visual Design Criticism

The design effectively conveys an exclusive, premium nightlife aesthetic through dark backgrounds, film grain textures, and stark typography. However, several inconsistencies and usability issues persist.

**Inconsistent Hierarchy:** The typographic hierarchy is visually striking but structurally inconsistent. `clamp()` values vary wildly between similar semantic elements across the two pages. The recent Round 39 text size increases on the sponsor page have improved readability, but these updates highlight the comparatively smaller text on the homepage.

**Button Styles:** Primary calls-to-action use `.btn-p`, but overrides (like `.btn-explore-r26`) create fragmentation. The "explore partnerships" button on the sponsor page is now a massive block element, while the homepage "request invite" button remains inline-flex.

**Alignment:** The Round 41 fix utilizing `100vw` successfully resolved the scrollbar-induced asymmetry for the sponsor page inner wrappers. However, this fix was applied via an inline `<style>` block rather than integrated into the core `styles.css`, continuing a pattern of architectural fragmentation.

**Color Palette:** The audit revealed 22 unique hex colors in use. While most align with the dark green/cream brand identity, there are slight variations (e.g., `#E8E6DF` vs `#f0ede8`) that should be consolidated into CSS variables.

---

## 3. Code Quality & Technical Debt

The codebase shows significant signs of "patch-on-patch" development, characteristic of rapid iteration without periodic refactoring.

**CSS Fragmentation:** 
- `styles.css` contains approximately 428 rules, while `sponsor.html` houses an inline `<style>` block with another 137 rules.
- There are 22 `!important` declarations across the CSS, with 17 of them concentrated in the `sponsor.html` inline styles. This indicates a struggle with specificity and overrides.
- Approximately 46 CSS classes defined in `styles.css` appear to be dead code, unused in either HTML file.

**HTML Clutter:**
- Both HTML files are littered with commented-out blocks marked `<!-- REMOVED RXX -->`. `index.html` contains 35 such blocks, and `sponsor.html` contains 13. This bloats the document size and makes maintenance difficult.
- The `sponsor.html` file contains 65 instances of comments nested within visible content areas or other tags, which can cause rendering anomalies.

**JavaScript Sprawl:**
- The `photos.js` file acts as a massive asset manifest rather than a functional script, hardcoding image paths for the masonry galleries.
- Inline scripts handle complex logic like the countdown timer and intersection observers. Notably, the countdown target date is hardcoded in two separate places (`index.html` uses `20:00:00` for the hero and `22:30:00` for the secondary display; `sponsor.html` uses `22:30:00`).

---

## 4. Performance

The site relies heavily on large media assets, which impacts load times.

**Asset Weight:**
- Several images in the `/img/` directory exceed 4MB, with `tribeca-new-07.jpg` reaching 6.1MB.
- Background videos are massive: `sponsor-hero-bg.mp4` is 42MB, and `sponsor-igc-video.mp4` is 31MB.
- While some images use `loading="lazy"`, `index.html` eager-loads 34 images. 

**Caching Strategy:**
- The `vercel.json` configuration correctly applies aggressive caching (`public,max-age=31536000,immutable`) to the `/img/` directory.
- HTML files are set to `public,max-age=0,must-revalidate`, ensuring users receive the latest content.

---

## 5. SEO (Search Engine Optimization)

The SEO implementation is basic and lacks essential metadata.

**Missing Elements:**
- Neither page includes a `<link rel="canonical">` tag.
- Neither page specifies a favicon.
- `index.html` lacks Open Graph and Twitter Card meta tags (these are present on `sponsor.html`).
- `index.html` lacks JSON-LD structured data (present on `sponsor.html`).

**Heading Structure:**
- The heading hierarchy is illogical. `index.html` jumps from an `H2` ("Some nights stay with you") to an `H1` ("NEXT EVENT: SPRINGTIME OPENER"), then back to `H2`s. 

---

## 6. Accessibility (a11y)

The site requires significant accessibility improvements to meet WCAG standards.

**Form Accessibility:**
- The contact form in `sponsor.html` uses proper `<label>` associations, but the contrast ratio of the placeholder text (`rgba(240,237,232,0.25)`) against the dark background fails WCAG AA requirements.

**Navigation & Structure:**
- Neither page contains a "Skip to content" link for keyboard users.
- `sponsor.html` lacks a `<footer role="contentinfo">` landmark.

**Motion:**
- The site makes extensive use of scroll-triggered reveal animations and autoplaying videos. However, there is no implementation of the `prefers-reduced-motion` media query to disable these effects for users with vestibular disorders.

---

## 7. Form Backend Architecture

The site currently lacks a functional production form backend.

**Current State:**
- The "Get on the list" form in `index.html` posts to a Formspree endpoint (`https://formspree.io/f/xwpbkqod`).
- The sponsorship inquiry form in `sponsor.html` uses a `mailto:events@tigertracks.ai` action, which relies on the user's local email client and is not a robust lead capture mechanism.

**Local Server Discovery:**
- The `server.js` file implements a basic Node HTTP server for local development. It includes a `POST /save-img` endpoint that accepts base64-encoded image data and writes it to the local `/img` directory. This is a local utility and does not process form submissions.

**Recommendation:**
The `sponsor.html` form must be connected to a proper backend service (e.g., Formspree, Netlify Forms, or a custom API) to reliably capture sponsorship leads.

---

*End of Phase 1 Audit Report.*
