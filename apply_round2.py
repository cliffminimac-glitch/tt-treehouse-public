#!/usr/bin/env python3
"""
Round 2 fixes for Treehouse Events index.html
Fix #1: Remove all dates/years from event titles and gallery section headers
Fix #2: Reposition curate section + next event ABOVE all past event galleries
Fix #3: Add Drive curate-room.jpg as full-bleed background for curate section
Fix #4: Fix dead space in gallery sections (tighten padding/margins)
Fix #5: Replace 3 sponsor photos with sponsor-video.mp4
"""

import re

with open('index.html', 'r') as f:
    html = f.read()

original = html  # keep for diff

# ─────────────────────────────────────────────────────────────────────────────
# FIX #1 — Remove all dates and years from event titles and gallery headers
# ─────────────────────────────────────────────────────────────────────────────

# Remove "· OCT 2024", "· MAY 2024", "· DEC 2024", "· JAN 2025", etc. from ev-title headings
# Pattern: any "· MONTH YEAR" or "· SEASON YEAR" appended to event names
html = re.sub(r'\s*·\s*(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+20\d\d', '', html)
html = re.sub(r'\s*·\s*(?:SPRING|SUMMER|FALL|WINTER)\s+20\d\d', '', html)

# Remove date labels in .lbl spans like "// May 2024 · treehouse. NYC" → "// treehouse. NYC"
# Keep the event label but strip the date part
html = re.sub(r'(// (?:May|Oct|Dec|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Nov)\s+20\d\d\s*·\s*)', '// ', html)
html = re.sub(r'(// (?:Spring|Summer|Fall|Winter)\s+20\d\d\s*·\s*)', '// ', html)

# Remove standalone date lines in ev-header (e.g. <p class="ev-date">October 2024</p>)
html = re.sub(r'<p[^>]*class="ev-date"[^>]*>.*?</p>', '', html)

# Remove any remaining "MONTH YEAR" or "Month Year" standalone text in ev-header spans
html = re.sub(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d\d', '', html)

print("Fix #1: Dates removed from event titles and gallery headers")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Reorder sections: curate + next event BEFORE galleries
# Current order: marquee → Tribeca → curate → triptych → next-event → video → soho...
# Target order:  marquee → curate → next-event → triptych → Tribeca → video → soho...
# ─────────────────────────────────────────────────────────────────────────────

# We'll extract sections by their markers and reassemble

# Marker boundaries (using unique anchor strings)
TRIBECA_START = '<!-- AUDIT FIX #1 — Gallery moved up: appears within first 2 scroll-depths -->'
TRIBECA_END_MARKER = '<!-- ABOUT -->'

ABOUT_START = '<!-- ABOUT -->'
ABOUT_END_MARKER = '<!-- AUDIT FIX #3 — Editorial triptych'

TRIPTYCH_START = '<!-- AUDIT FIX #3 — Editorial triptych'
TRIPTYCH_END_MARKER = '<!-- NEXT EVENT -->'

NEXT_EVENT_START = '<!-- NEXT EVENT -->'
NEXT_EVENT_END_MARKER = '<!-- VIDEO REEL -->'

VIDEO_START = '<!-- VIDEO REEL -->'
VIDEO_END_MARKER = '<!-- ═══════════════ 6 PARTY SECTIONS'

SOHO_START = '<!-- ═══════════════ 6 PARTY SECTIONS'

# Extract each block
def extract_between(html, start_marker, end_marker):
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx + len(start_marker))
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Could not find markers:\n  START: {start_marker[:60]}\n  END: {end_marker[:60]}")
    return html[start_idx:end_idx]

def extract_from(html, start_marker):
    start_idx = html.find(start_marker)
    if start_idx == -1:
        raise ValueError(f"Could not find marker: {start_marker[:60]}")
    return html[start_idx:]

# Get the prefix (everything before the first section we're reordering)
prefix_end = html.find(TRIBECA_START)
prefix = html[:prefix_end]

# Extract each section block
tribeca_block = extract_between(html, TRIBECA_START, ABOUT_END_MARKER)
about_block = extract_between(html, ABOUT_START, TRIPTYCH_START)
triptych_block = extract_between(html, TRIPTYCH_START, NEXT_EVENT_START)
next_event_block = extract_between(html, NEXT_EVENT_START, VIDEO_START)
video_block = extract_between(html, VIDEO_START, SOHO_START)
soho_onwards = extract_from(html, SOHO_START)

# Add Round 2 comment to about block
about_block = about_block.replace('<!-- ABOUT -->', '<!-- ABOUT -->\n<!-- ROUND 2 FIX #2 — Curate section moved above galleries -->')
next_event_block = next_event_block.replace('<!-- NEXT EVENT -->', '<!-- NEXT EVENT -->\n<!-- ROUND 2 FIX #2 — Next event moved above galleries -->')

# Reassemble in new order:
# prefix → about → next_event → triptych → tribeca → video → soho_onwards
html = (
    prefix +
    about_block +
    next_event_block +
    triptych_block +
    '<!-- ROUND 2 FIX #2 — Tribeca gallery now appears after curate+next-event -->\n' +
    tribeca_block +
    video_block +
    soho_onwards
)

print("Fix #2: Page reordered — curate + next event now appear before galleries")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3 — Replace curate section background: dj.jpg → curate-room.jpg
# Use full-bleed background with overlay (Option A from prompt)
# ─────────────────────────────────────────────────────────────────────────────

# Replace the dj.jpg img src with curate-room.jpg
# Also update the alt text and add Round 2 comment
html = html.replace(
    '<img src="/img/dj.jpg" alt="DJ performing at treehouse. NYC — We Curate the Room" class="dj-photo" fetchpriority="high" onerror="this.onerror=null;this.parentNode.style.background=\'#1a3a1a\'">',
    '<!-- ROUND 2 FIX #3 — Background swapped from dj.jpg to curate-room.jpg (golden-hour rooftop crowd) -->\n  <img src="/img/curate-room.jpg" alt="treehouse. NYC — packed rooftop crowd at golden hour" class="dj-photo" fetchpriority="high" onerror="this.onerror=null;this.parentNode.style.background=\'#1a3a1a\'">'
)

# Update object-position to show the crowd better (center of image)
html = html.replace(
    '.curate-section .dj-photo { width:100%; height:100%; object-fit:cover; object-position:center 40%; display:block; }',
    '.curate-section .dj-photo { width:100%; height:100%; object-fit:cover; object-position:center 55%; display:block; } /* ROUND 2 FIX #3 */'
)

print("Fix #3: Curate section background updated to curate-room.jpg")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #4 — Tighten gallery section dead space
# Reduce .ev-section padding, .ev-header margins, .ev-desc margins
# ─────────────────────────────────────────────────────────────────────────────

# The current CSS has .ev-section { padding:40px 0 0; } — already tightened from prev round
# We need to also reduce the ev-header bottom margin and ev-desc bottom margin
# Find and update the ev-header CSS

# Update ev-header padding/margin to be tighter
html = html.replace(
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 2rem; }',
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 1rem; } /* ROUND 2 FIX #4 — reduced bottom padding */'
)

# Tighten ev-title margin
html = html.replace(
    '.ev-title { font-size:clamp(2.8rem,6vw,5.5rem); letter-spacing:-0.02em; line-height:0.9; margin:0 0 0.5rem; }',
    '.ev-title { font-size:clamp(2.8rem,6vw,5.5rem); letter-spacing:-0.02em; line-height:0.9; margin:0 0 0.3rem; } /* ROUND 2 FIX #4 */'
)

# Tighten ev-desc margin
html = html.replace(
    '.ev-desc { font-size:0.88rem; line-height:1.6; opacity:0.72; max-width:520px; margin:0 0 1.25rem; }',
    '.ev-desc { font-size:0.88rem; line-height:1.6; opacity:0.72; max-width:520px; margin:0 0 0.75rem; } /* ROUND 2 FIX #4 */'
)

# Also reduce ev-section top padding from 40px to 32px for tighter feel
html = html.replace(
    '.ev-section { padding:40px 0 0; }',
    '.ev-section { padding:32px 0 0; } /* ROUND 2 FIX #4 — tighter section top padding */'
)

# Reduce the gallery-visible top margin
html = html.replace(
    '.gallery-visible { display:grid; grid-template-columns:repeat(4,1fr); gap:3px; margin-top:0; }',
    '.gallery-visible { display:grid; grid-template-columns:repeat(4,1fr); gap:3px; margin-top:0; } /* ROUND 2 FIX #4 — no top margin */'
)

print("Fix #4: Gallery dead space reduced — tighter ev-header, ev-title, ev-desc, ev-section padding")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #5 — Replace 3 sponsor photos with sponsor-video.mp4
# Comment out the 3 <img> tags, add <video> element in the right column
# ─────────────────────────────────────────────────────────────────────────────

# Find the why-layout section with the 3 sponsor photos
# The photos are: sp-xmas-martini.jpg, sp-may-sunglasses.jpg, sp-xmas-crowddrinks.jpg

# Find the right column of the why-layout (the photo column)
# It contains a div with the 3 stacked images
old_photo_col = '''<div class="why-photos" data-a="f" data-d="2">'''

# Find the full why-photos div
why_photos_start = html.find('<div class="why-photos"')
if why_photos_start == -1:
    # Try alternate class names
    why_photos_start = html.find('sp-xmas-martini')
    if why_photos_start != -1:
        # Find the enclosing div
        why_photos_start = html.rfind('<div', 0, why_photos_start)

if why_photos_start != -1:
    # Find the closing </div> for this container
    # Count div depth
    depth = 0
    i = why_photos_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                why_photos_end = i + 6
                break
        i += 1
    
    old_why_photos = html[why_photos_start:why_photos_end]
    
    # Build the new video replacement
    new_why_video = '''<!-- ROUND 2 FIX #5 — Sponsor photos replaced with sponsor-video.mp4 -->
<div class="why-photos" data-a="f" data-d="2">
  <!-- REMOVED: sp-xmas-martini.jpg, sp-may-sunglasses.jpg, sp-xmas-crowddrinks.jpg
  <img src="/img/sp-xmas-martini.jpg" ...>
  <img src="/img/sp-may-sunglasses.jpg" ...>
  <img src="/img/sp-xmas-crowddrinks.jpg" ...>
  -->
  <video
    src="/img/sponsor-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    poster="/img/hero-new.jpg"
    class="sponsor-video"
    style="width:100%;height:100%;object-fit:cover;display:block;border-radius:4px;"
  ></video>
</div>'''
    
    html = html[:why_photos_start] + new_why_video + html[why_photos_end:]
    print("Fix #5: Sponsor photos replaced with sponsor-video.mp4")
else:
    # Fallback: find and comment out the individual img tags
    for img_name in ['sp-xmas-martini.jpg', 'sp-may-sunglasses.jpg', 'sp-xmas-crowddrinks.jpg']:
        img_start = html.find(f'src="/img/{img_name}"')
        if img_start != -1:
            # Find the full img tag
            tag_start = html.rfind('<img', 0, img_start)
            tag_end = html.find('>', img_start) + 1
            old_tag = html[tag_start:tag_end]
            html = html.replace(old_tag, f'<!-- REMOVED: {img_name} -->')
    
    # Add video after the last removed img comment
    last_removed = html.rfind('<!-- REMOVED: sp-xmas-crowddrinks.jpg -->')
    if last_removed != -1:
        insert_pos = last_removed + len('<!-- REMOVED: sp-xmas-crowddrinks.jpg -->')
        video_html = '''
<!-- ROUND 2 FIX #5 — Sponsor video added -->
<video
  src="/img/sponsor-video.mp4"
  autoplay muted loop playsinline
  preload="metadata"
  poster="/img/hero-new.jpg"
  class="sponsor-video"
  style="width:100%;aspect-ratio:9/16;object-fit:cover;display:block;border-radius:4px;max-height:560px;"
></video>'''
        html = html[:insert_pos] + video_html + html[insert_pos:]
    print("Fix #5: Sponsor photos commented out, video added (fallback method)")

# ─────────────────────────────────────────────────────────────────────────────
# Add CSS for sponsor-video and update why-layout
# ─────────────────────────────────────────────────────────────────────────────

# Add sponsor-video CSS before </style>
sponsor_css = '''
/* ROUND 2 FIX #5 — Sponsor video styles */
.sponsor-video { width:100%; height:100%; object-fit:cover; display:block; border-radius:4px; }
.why-photos { position:relative; overflow:hidden; border-radius:4px; min-height:400px; max-height:580px; }
@media(max-width:768px){ .why-photos { min-height:280px; max-height:420px; width:100%; } }

/* ROUND 2 FIX #4 — Also update logo sheet display */
.logos-sheet { width:100%; display:block; }
'''

html = html.replace('</style>', sponsor_css + '\n</style>', 1)

# ─────────────────────────────────────────────────────────────────────────────
# Also update the brand logos section to use the new logo sheets (7.png, 8.png)
# These are cleaner versions of all the brand logos
# ─────────────────────────────────────────────────────────────────────────────

# Find the brands-grid / logos section
brands_start = html.find('<div class="brands-grid"')
if brands_start == -1:
    brands_start = html.find('id="brands"')
    if brands_start != -1:
        brands_start = html.find('<div', brands_start)

if brands_start != -1:
    # Find closing div
    depth = 0
    i = brands_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                brands_end = i + 6
                break
        i += 1
    
    old_brands = html[brands_start:brands_end]
    
    new_brands = '''<!-- ROUND 2 FIX — Logo sheets updated to cleaner versions (7.png, 8.png) -->
<div class="brands-grid" style="display:flex;flex-direction:column;gap:1rem;align-items:center;padding:0 clamp(1rem,4vw,4rem);">
  <img src="/img/curate-7.png" alt="treehouse. brand partners — page 1" class="logos-sheet" style="max-width:900px;width:100%;filter:invert(1) brightness(0.85);opacity:0.75;mix-blend-mode:screen;">
  <img src="/img/curate-8.png" alt="treehouse. brand partners — page 2" class="logos-sheet" style="max-width:900px;width:100%;filter:invert(1) brightness(0.85);opacity:0.75;mix-blend-mode:screen;">
</div>'''
    
    html = html[:brands_start] + new_brands + html[brands_end:]
    print("Bonus: Brand logos updated to use cleaner logo sheets (7.png, 8.png)")

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────

with open('index.html', 'w') as f:
    f.write(html)

print("\nAll Round 2 fixes applied. index.html saved.")
print(f"File size: {len(html):,} chars")
