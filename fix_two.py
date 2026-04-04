#!/usr/bin/env python3
"""Fix two issues:
1. Nested HTML comment breaking the duplicate curate section comment block
2. inside-the-room.jpg needs to span full width (not 1/3 of a 3-col grid)
"""

with open('index.html') as f:
    html = f.read()

original_len = len(html)
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: Remove the duplicate curate section entirely (don't rely on comments)
# The nested <!-- --> inside the outer comment breaks HTML parsing.
# Solution: delete the entire block from <!-- ABOUT --> to --> before <!-- VIDEO REEL -->
# ─────────────────────────────────────────────────────────────────────────────

old_block = '''<!-- ABOUT -->
<!-- ROUND 3 FIX #1 — Duplicate curate section removed. Only the first instance (above galleries) is kept.
<section class="curate-section" id="about">
  <!-- ROUND 2 FIX #3 — Background swapped from dj.jpg to curate-room.jpg (golden-hour rooftop crowd) -->
  <img src="/img/curate-room.jpg" alt="treehouse. NYC — packed rooftop crowd at golden hour" class="dj-photo" fetchpriority="high" onerror="this.onerror=null;this.parentNode.style.background='#1a3a1a'">
  <div class="curate-overlay"></div>
  <div class="curate-copy reveal">
    <span class="lbl reveal-child" style="color:rgba(240,237,232,0.55);margin-bottom:1rem;display:block;">// Who We Are</span>
    <h2>We curate<br>the room.</h2>
    <p>Themed parties. Open bar. Good music. The kind of night you text about the next day. Five events in, still selling out.</p>
    <div class="tags" style="justify-content:center;margin-top:1.5rem;">
      <span class="tag">Rooftop Parties</span>
      <span class="tag">Holiday Events</span>
      <span class="tag">Dinner Nights</span>
      <span class="tag">Brand Nights</span>
    </div>
  </div>
</section>
-->'''

new_block = '<!-- ABOUT: duplicate removed (nested comment caused rendering bug) -->'

if old_block in html:
    html = html.replace(old_block, new_block)
    changes.append('Fix 1: Duplicate curate section fully removed (nested comment bug fixed)')
else:
    changes.append('Fix 1 WARNING: exact block not found — trying partial match')
    # Try to find and remove it by finding the markers
    start = html.find('<!-- ABOUT -->')
    end = html.find('<!-- VIDEO REEL -->')
    if start != -1 and end != -1 and end > start:
        html = html[:start] + '<!-- ABOUT: duplicate removed -->\n' + html[end:]
        changes.append('Fix 1: Duplicate curate section removed via marker search')
    else:
        changes.append('Fix 1 FAILED: Could not locate the duplicate block')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: Make inside-the-room.jpg span the full width of the triptych
# Change the 3-column grid to show inside-the-room.jpg as a full-width hero
# with main-photo-2 and main-photo-3 stacked on the right in a 2:1 layout
# OR simply make inside-the-room.jpg full-width on its own row
# ─────────────────────────────────────────────────────────────────────────────

old_grid = '''  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:clamp(240px,32vw,460px);">
    <div style="overflow:hidden;"><img src="/img/inside-the-room.jpg" alt="Packed rooftop crowd, treehouse. NYC" style="width:100%;height:100%;object-fit:cover;object-position:center 30%;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>'''

# New layout: inside-the-room.jpg full-width top row, then 2 photos side-by-side below
new_grid = '''  <!-- FIX: inside-the-room.jpg full width, then 2 photos below -->
  <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:clamp(200px,28vw,420px) clamp(140px,18vw,260px);gap:0;">
    <div style="grid-column:1/-1;overflow:hidden;">
      <img src="/img/inside-the-room.jpg" alt="Packed rooftop crowd, treehouse. NYC" style="width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block;">
    </div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>'''

if old_grid in html:
    html = html.replace(old_grid, new_grid)
    changes.append('Fix 2: inside-the-room.jpg now spans full width (grid-column:1/-1), 2 photos below')
else:
    changes.append('Fix 2 WARNING: grid block not found verbatim')

# ─────────────────────────────────────────────────────────────────────────────
# Also make the curate section taller / full-size
# The curate section has height:70vh — increase to 85vh for more impact
# ─────────────────────────────────────────────────────────────────────────────

old_curate_h = 'height:70vh; min-height:500px;'
new_curate_h = 'height:85vh; min-height:560px; /* FIX: full-size curate section */'

if old_curate_h in html:
    html = html.replace(old_curate_h, new_curate_h)
    changes.append('Fix 3: Curate section height increased to 85vh (full-size)')
else:
    # Try alternative format
    old_curate_h2 = 'height:70vh;min-height:500px;'
    new_curate_h2 = 'height:85vh;min-height:560px;'
    if old_curate_h2 in html:
        html = html.replace(old_curate_h2, new_curate_h2)
        changes.append('Fix 3: Curate section height increased to 85vh (full-size)')
    else:
        changes.append('Fix 3 WARNING: curate section height rule not found verbatim')

with open('index.html', 'w') as f:
    f.write(html)

print(f'Done. File: {original_len:,} → {len(html):,} chars')
for c in changes:
    prefix = 'PASS' if 'WARNING' not in c and 'FAILED' not in c else 'WARN'
    print(f'  [{prefix}] {c}')
