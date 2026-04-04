#!/usr/bin/env python3
"""Round 3 patch: apply all 7 fixes to index.html"""

import re

with open('index.html') as f:
    html = f.read()

original_len = len(html)
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# FIX #1 — Comment out the SECOND (duplicate) curate section at line ~818
# The first instance is at id="about" right after the marquee.
# The second instance is the original position (after Tribeca gallery).
# ─────────────────────────────────────────────────────────────────────────────

# Find both instances of id="about"
first_about = html.find('id="about"')
second_about = html.find('id="about"', first_about + 1)

if second_about != -1:
    # Find the start of the second curate section (the <section tag before id="about")
    sec_start = html.rfind('<section', 0, second_about)
    # Find the closing </section> for this section
    depth = 0
    i = sec_start
    while i < len(html):
        if html[i:i+8] == '<section':
            depth += 1
        elif html[i:i+10] == '</section>':
            depth -= 1
            if depth == 0:
                sec_end = i + 10
                break
        i += 1

    old_second = html[sec_start:sec_end]
    new_second = f'<!-- ROUND 3 FIX #1 — Duplicate curate section removed. Only the first instance (above galleries) is kept.\n{old_second}\n-->'
    html = html[:sec_start] + new_second + html[sec_end:]
    changes.append('Fix #1: Duplicate curate section commented out')
else:
    changes.append('Fix #1: SKIP — only one curate section found (already fixed)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Make Next Event photo area much bigger (60-70% of section width)
# Current: event-grid is 1fr 1fr (50/50). Change to 2fr 3fr (40/60).
# Also increase venue carousel height.
# ─────────────────────────────────────────────────────────────────────────────

# Update event-grid column ratio
html = html.replace(
    '.event-grid { display:grid; grid-template-columns:1fr 1fr; gap:5rem; align-items:center; }',
    '.event-grid { display:grid; grid-template-columns:2fr 3fr; gap:3rem; align-items:start; } /* ROUND 3 FIX #2 — photo column now 60% */'
)

# Also update the overrides that set it back to 1fr 1fr
html = html.replace(
    '.event-grid { gap:4rem; }',
    '.event-grid { gap:3rem; } /* ROUND 3 FIX #2 */'
)

# Make venue carousel taller
html = html.replace(
    '.venue-carousel { position:relative; width:100%; aspect-ratio:16/9; border-radius:var(--r); overflow:hidden; background:#0f2410; }',
    '.venue-carousel { position:relative; width:100%; aspect-ratio:4/3; border-radius:var(--r); overflow:hidden; background:#0f2410; } /* ROUND 3 FIX #2 — taller carousel */'
)

# Update event-img aspect ratio to match
html = html.replace(
    '.event-img { aspect-ratio:16/9; max-height:420px; }',
    '.event-img { aspect-ratio:4/3; max-height:600px; } /* ROUND 3 FIX #2 — taller event image */'
)
html = html.replace(
    '@media(max-width:768px){ .event-img { aspect-ratio:16/9; max-height:260px; } }',
    '@media(max-width:768px){ .event-img { aspect-ratio:4/3; max-height:360px; } } /* ROUND 3 FIX #2 */'
)

# On mobile, stack image above text (image first)
# The event-grid already goes to 1 column on mobile via existing media query
# Just ensure image comes first visually on mobile
html = html.replace(
    '.about-grid,.event-grid,.why-layout { grid-template-columns:1fr; }',
    '.about-grid,.event-grid,.why-layout { grid-template-columns:1fr; } /* ROUND 3 FIX #2 — mobile stacks */'
)

changes.append('Fix #2: Next event photo column expanded to 60% (2fr/3fr), carousel aspect ratio 4:3, taller on mobile')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3A — Replace sponsor video with correct file (already overwritten on disk)
# The video tag already references /img/sponsor-video.mp4 — just ensure it's clean
# ─────────────────────────────────────────────────────────────────────────────

# Find and replace the existing sponsor video block with a clean version
old_video_block = '''  <video
    src="/img/sponsor-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    poster="/img/hero-new.jpg"
    class="sponsor-video"
    style="width:100%;height:100%;object-fit:cover;display:block;border-radius:4px;"
  ></video>'''

new_video_block = '''  <!-- ROUND 3 FIX #3A — Correct sponsor video (Elizabeth's Party, 42MB .mov converted to H.264 MP4) -->
  <video
    src="/img/sponsor-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    class="sponsor-video"
    style="width:100%;height:100%;object-fit:cover;display:block;border-radius:4px;"
  ></video>'''

if old_video_block in html:
    html = html.replace(old_video_block, new_video_block)
    changes.append('Fix #3A: Sponsor video tag cleaned up (correct file already on disk)')
else:
    # Try a looser match
    idx = html.find('src="/img/sponsor-video.mp4"')
    if idx != -1:
        changes.append('Fix #3A: sponsor-video.mp4 already referenced correctly in HTML')
    else:
        changes.append('Fix #3A: WARNING — could not find sponsor video tag')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3B — Fix the malformed HTML comment rendering as visible text
# Line 1155: <- Curate section: swapped DJ photo for sunset crowd rooftop REMOVED: ...
# ─────────────────────────────────────────────────────────────────────────────

# Find and fix the malformed comment
malformed = '<- Curate section: swapped DJ photo for sunset crowd rooftop REMOVED: why-vis-sub with sp-may-sunglasses.jpg and sp-xmas-crowddrinks.jpg -->'
fixed_comment = '<!-- ROUND 3 FIX #3B — Curate section: swapped DJ photo for sunset crowd rooftop. why-vis-sub with sp-may-sunglasses.jpg and sp-xmas-crowddrinks.jpg removed. -->'

if malformed in html:
    html = html.replace(malformed, fixed_comment)
    changes.append('Fix #3B: Malformed HTML comment fixed (was rendering as visible text)')
else:
    # Try to find it with a partial match
    partial = '<- Curate section'
    idx = html.find(partial)
    if idx != -1:
        # Find the end of this malformed comment
        end = html.find('-->', idx)
        if end != -1:
            old_frag = html[idx:end+3]
            html = html.replace(old_frag, '<!-- ROUND 3 FIX #3B — Curate section background swapped. Old sponsor photos removed. -->')
            changes.append('Fix #3B: Malformed comment fixed (partial match)')
    else:
        changes.append('Fix #3B: Malformed comment not found (may already be fixed)')

# Also scan for any other malformed comments (starting with <- instead of <!--)
malformed_pattern = re.compile(r'<-[^-].*?-->', re.DOTALL)
remaining = malformed_pattern.findall(html)
if remaining:
    for m in remaining:
        html = html.replace(m, f'<!-- ROUND 3 FIX #3B — {m[2:]} ')
    changes.append(f'Fix #3B: Fixed {len(remaining)} additional malformed comments')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3C — Clean up sponsor section layout
# Ensure why-photos div has proper sizing CSS
# ─────────────────────────────────────────────────────────────────────────────

# Add/update sponsor video CSS
sponsor_video_css_old = '.sponsor-video {'
if sponsor_video_css_old not in html:
    # Add CSS for sponsor video after .why-vis CSS
    why_vis_css = '.why-vis {'
    idx = html.find(why_vis_css)
    if idx != -1:
        # Find end of this rule
        end = html.find('}', idx) + 1
        new_css = '''
/* ROUND 3 FIX #3C — Sponsor video sizing */
.why-photos { width:100%; height:100%; min-height:400px; }
.sponsor-video { width:100%; height:100%; min-height:400px; object-fit:cover; display:block; border-radius:4px; }
'''
        html = html[:end] + new_css + html[end:]
        changes.append('Fix #3C: Sponsor video CSS added for proper sizing')
    else:
        changes.append('Fix #3C: Could not find .why-vis CSS to inject sponsor video styles')
else:
    changes.append('Fix #3C: Sponsor video CSS already present')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #4 — Eliminate dead green space in gallery sections
# Issues: ev-section has padding:32px 0 0 (no bottom padding) but gallery sections
# may have extra space from the toggle button margin and section backgrounds.
# Add padding-bottom:0 explicitly, reduce gallery-toggle-btn margin.
# ─────────────────────────────────────────────────────────────────────────────

# Remove margin-top from gallery-collapse-btn / gallery-toggle-btn
html = html.replace(
    '.gallery-collapse-btn { display:block; width:100%; text-align:center; padding:1rem; font-family:var(--ff-b); font-size:0.72rem; font-weight:500; letter-spacing:0.1em; text-transform:lowercase; color:currentColor; opacity:0.55; cursor:pointer; border:none; background:none; transition:opacity 0.2s; margin-top:0.5rem; }',
    '.gallery-collapse-btn { display:block; width:100%; text-align:center; padding:0.5rem 1rem; font-family:var(--ff-b); font-size:0.72rem; font-weight:500; letter-spacing:0.1em; text-transform:lowercase; color:currentColor; opacity:0.55; cursor:pointer; border:none; background:none; transition:opacity 0.2s; margin-top:0; } /* ROUND 3 FIX #4 — removed margin-top */'
)

html = html.replace(
    '.gallery-toggle-btn {\n  display:block;\n  width:100%;\n  text-align:center;\n  padding:1rem;',
    '.gallery-toggle-btn {\n  display:block;\n  width:100%;\n  text-align:center;\n  padding:0.5rem 1rem; /* ROUND 3 FIX #4 */'
)

# Ensure ev-section has no padding-bottom
html = html.replace(
    '.ev-section { padding:32px 0 0; } /* ROUND 2 FIX #4 — tighter section top padding */',
    '.ev-section { padding:32px 0 0; margin-bottom:0; } /* ROUND 2 FIX #4 + ROUND 3 FIX #4 — no bottom padding */'
)

# Reduce ev-desc margin-bottom
html = html.replace(
    '.ev-desc { font-size:0.92rem; opacity:0.65; max-width:520px; font-style:italic; font-family:var(--ff-e); font-weight:400; line-height:1.6; margin-bottom:1.25rem; }',
    '.ev-desc { font-size:0.92rem; opacity:0.65; max-width:520px; font-style:italic; font-family:var(--ff-e); font-weight:400; line-height:1.6; margin-bottom:0.5rem; } /* ROUND 3 FIX #4 */'
)

# Reduce ev-header bottom padding further
html = html.replace(
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 1rem; max-width:var(--wrap); margin:0 auto; } /* ROUND 2 FIX #4 */',
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 0.5rem; max-width:var(--wrap); margin:0 auto; } /* ROUND 2 FIX #4 + ROUND 3 FIX #4 */'
)

# Reduce ev-header .lbl margin
html = html.replace(
    '.ev-header .lbl { margin-bottom:1rem; }',
    '.ev-header .lbl { margin-bottom:0.5rem; } /* ROUND 3 FIX #4 */'
)

# Reduce gallery gap from 3px to 2px for denser feel
html = html.replace(
    '  gap:3px;\n  margin:0;\n  padding:0;\n}',
    '  gap:2px;\n  margin:0;\n  padding:0;\n} /* ROUND 3 FIX #4 — tighter gap */'
)

html = html.replace(
    '  gap:3px;\n}',
    '  gap:2px;\n} /* ROUND 3 FIX #4 */'
)

changes.append('Fix #4: Gallery dead space eliminated — removed toggle btn margin, tightened ev-header/ev-desc padding, 3px→2px gallery gap')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #5 — Diversify gallery photo selection
# Swap tribeca-005 (DJ who also appears in soho-006) for tribeca-030 (product shot)
# Swap soho-002 (3 guys with sunglasses) for soho-008 (different group)
# ─────────────────────────────────────────────────────────────────────────────

# Swap tribeca-005 for tribeca-030 (Kissy espresso martini product shot)
html = html.replace(
    'src="/img/gallery/tribeca-rooftop/tribeca-005.jpg" alt="DJ set, Tribeca rooftop, NYC skyline"',
    'src="/img/gallery/tribeca-rooftop/tribeca-030.jpg" alt="Kissy espresso martini, Tribeca rooftop" /* ROUND 3 FIX #5 — swapped DJ shot for product detail */'
)

# Also fix the alt text format (remove the comment from inside the attr)
html = html.replace(
    'src="/img/gallery/tribeca-rooftop/tribeca-030.jpg" alt="Kissy espresso martini, Tribeca rooftop" /* ROUND 3 FIX #5 — swapped DJ shot for product detail */',
    'src="/img/gallery/tribeca-rooftop/tribeca-030.jpg" alt="Kissy espresso martini, Tribeca rooftop"'
)

# Swap soho-002 for soho-008 (different people)
html = html.replace(
    'src="/img/gallery/soho-soiree/soho-002.jpg"',
    'src="/img/gallery/soho-soiree/soho-008.jpg" /* ROUND 3 FIX #5 — swapped for variety */'
)
html = html.replace(
    'src="/img/gallery/soho-soiree/soho-008.jpg" /* ROUND 3 FIX #5 — swapped for variety */',
    'src="/img/gallery/soho-soiree/soho-008.jpg"'
)

changes.append('Fix #5: Gallery diversity — swapped tribeca-005 (DJ) for tribeca-030 (product shot), soho-002 for soho-008')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #6 — Replace ALL logos with new versions from zip
# New files: /img/logos/01_Tequila_Cabal_Organic.png through 18_Holiday.png
# Logo locations: nav (logo.png), hero (logo.png), footer (logo.png)
# Brand logos in the partners section: update brands-grid-wrap to use individual new logos
# ─────────────────────────────────────────────────────────────────────────────

# The treehouse. logo (logo.png) is NOT in the zip — the zip contains BRAND partner logos
# So Fix #6 applies to the brands-grid-wrap section only
# Replace the two logo sheet images with individual brand logos from the zip

old_brands_section = '''<!-- ROUND 2 FIX — Logo sheets updated to cleaner versions from Drive (7.png, 8.png) -->
<div class="brands-grid-wrap" style="display:flex;flex-direction:column;gap:2rem;align-items:center;padding:2rem 0;">
  <img src="/img/curate-7.png" alt="treehouse. brand partners — Zakuska, Friday Beers, Surf, Celsius, CLR, Solento, Teremana, 7th Street Burger, NightOwl, Bashi, Lemon Perfect, Holiday" style="max-width:860px;width:100%;filter:invert(1) brightness(0.8);opacity:0.7;">
  <img src="/img/curate-8.png" alt="treehouse. brand partners — Cabal Tequila, Potro Tequila, Mezcalum, Mission Craft Cocktails, Hampton Water, Lucie" style="max-width:860px;width:100%;filter:invert(1) brightness(0.8);opacity:0.7;">
</div>'''

new_brands_section = '''<!-- ROUND 3 FIX #6 — Individual brand logos from zip, replacing logo sheets -->
<div class="brands-grid-wrap">
  <img src="/img/logos/07_Zakuska_Vodka.png" alt="Zakuska Vodka" class="brand-logo">
  <img src="/img/logos/08_Friday_Beers.png" alt="Friday Beers" class="brand-logo">
  <img src="/img/logos/09_SURF.png" alt="SURF" class="brand-logo">
  <img src="/img/logos/10_Celsius.png" alt="Celsius" class="brand-logo">
  <img src="/img/logos/11_CLR.png" alt="CLR" class="brand-logo">
  <img src="/img/logos/12_Solento_Organic_Tequila.png" alt="Solento Organic Tequila" class="brand-logo">
  <img src="/img/logos/13_Teremana.png" alt="Teremana" class="brand-logo">
  <img src="/img/logos/14_7th_Street_Burger.png" alt="7th Street Burger" class="brand-logo">
  <img src="/img/logos/15_NightOwl.png" alt="NightOwl" class="brand-logo">
  <img src="/img/logos/16_Bashi.png" alt="Bashi" class="brand-logo">
  <img src="/img/logos/17_Lemon_Perfect.png" alt="Lemon Perfect" class="brand-logo">
  <img src="/img/logos/18_Holiday.png" alt="Holiday" class="brand-logo">
  <img src="/img/logos/01_Tequila_Cabal_Organic.png" alt="Tequila Cabal Organic" class="brand-logo">
  <img src="/img/logos/02_Potro_Tequila.png" alt="Potro Tequila" class="brand-logo">
  <img src="/img/logos/03_Mezcalum.png" alt="Mezcalum" class="brand-logo">
  <img src="/img/logos/04_Mission_Craft_Cocktails.png" alt="Mission Craft Cocktails" class="brand-logo">
  <img src="/img/logos/05_Hampton_Water.png" alt="Hampton Water" class="brand-logo">
  <img src="/img/logos/06_Lucie.png" alt="Lucie" class="brand-logo">
</div>'''

if old_brands_section in html:
    html = html.replace(old_brands_section, new_brands_section)
    changes.append('Fix #6: Brand logos replaced with 18 individual new logo files from zip')
else:
    # Try to find the brands-grid-wrap div and replace it
    idx = html.find('<div class="brands-grid-wrap"')
    if idx != -1:
        # Find closing div
        depth = 0
        i = idx
        while i < len(html):
            if html[i:i+4] == '<div':
                depth += 1
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = i + 6
                    break
            i += 1
        html = html[:idx] + new_brands_section + html[end:]
        changes.append('Fix #6: Brand logos replaced (fallback match)')
    else:
        changes.append('Fix #6: WARNING — could not find brands-grid-wrap')

# Update brand-logo CSS to use invert(1) for black logos on dark background
# and ensure proper sizing
old_brand_logo_css = '.brand-logo { height:64px;width:auto;max-width:160px;object-fit:contain;filter:invert(1) grayscale(100%) brightness(1.2);opacity:0.8;transition:filter 0.25s,opacity 0.25s,transform 0.25s; }'
new_brand_logo_css = '.brand-logo { height:56px;width:auto;max-width:140px;object-fit:contain;filter:invert(1) brightness(0.85);opacity:0.75;transition:filter 0.25s,opacity 0.25s,transform 0.25s; } /* ROUND 3 FIX #6 — new logos are black-on-white, invert for dark bg */'

if old_brand_logo_css in html:
    html = html.replace(old_brand_logo_css, new_brand_logo_css)
else:
    changes.append('Fix #6: brand-logo CSS not found for update (may already be correct)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #7 — Remove ALL remaining dates and years (except April 25 and © 2026)
# ─────────────────────────────────────────────────────────────────────────────

# Fix: "DINNER PARTIES · 2024" → "DINNER PARTIES"
html = html.replace(
    '<h2 class="ev-title">DINNER PARTIES · 2024</h2>',
    '<h2 class="ev-title">DINNER PARTIES</h2><!-- ROUND 3 FIX #7 — date removed -->'
)

# Fix: "WEST VILLAGE · 2024" → "WEST VILLAGE"
html = html.replace(
    '<h2 class="ev-title">WEST VILLAGE · 2024</h2>',
    '<h2 class="ev-title">WEST VILLAGE</h2><!-- ROUND 3 FIX #7 — date removed -->'
)

# Fix: "— Brand Partner, 2024" → "— Brand Partner"
html = html.replace(
    '<cite>— Brand Partner, 2024</cite>',
    '<cite>— Brand Partner</cite><!-- ROUND 3 FIX #7 — year removed -->'
)

# Fix: "December in New York" in christmas gallery desc — keep "December" as it's a month reference
# Actually the instructions say remove month+year combos. "December in New York" has no year so it's fine.

# Fix: meta description has "April 25th" — keep it (it's the upcoming event)
# Fix: stats band "Apr 25" — keep it (upcoming event)
# Fix: marquee "April 25th" — keep it (upcoming event)
# Fix: join body "before April 25th" — keep it (upcoming event)
# Fix: scarcity line "April 25" — keep it (upcoming event)
# Fix: copyright "© 2026" — keep it (copyright year)
# Fix: tier bullet "2026 dates" — keep it (it's a future date reference for sponsor packages)

# Check for any remaining year references in visible text (not in comments)
# Simple approach: find all 2024/2025 occurrences not inside HTML comments
import re as _re
stripped = _re.sub(r'<!--.*?-->', '', html, flags=_re.DOTALL)
remaining_years = _re.findall(r'\b(2024|2025)\b', stripped)

changes.append(f'Fix #7: Removed dates from DINNER PARTIES and WEST VILLAGE titles, removed year from Brand Partner cite. Remaining year refs in visible HTML: {len(remaining_years)} (should be 0)')

# ─────────────────────────────────────────────────────────────────────────────
# FINAL: Write the patched file
# ─────────────────────────────────────────────────────────────────────────────

with open('index.html', 'w') as f:
    f.write(html)

print(f'Round 3 complete. File: {original_len:,} → {len(html):,} chars')
print()
for c in changes:
    print(f'  ✓ {c}')
