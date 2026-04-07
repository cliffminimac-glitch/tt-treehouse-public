#!/usr/bin/env python3
"""Round 8 — All 6 fixes"""

import re

with open('index.html', 'r') as f:
    html = f.read()

original_len = len(html)
fixes = []

# ─────────────────────────────────────────────────────────────
# FIX 1 — Comment out the entire "Inside the Room" section
# ─────────────────────────────────────────────────────────────
old_energy = """<!-- INSIDE THE ROOM — full-bleed photo grid, no gaps, no padding -->
<section class="lt" style="padding:0;" id="the-energy">
  <div style="padding:1.25rem clamp(1.5rem,5vw,5rem) 0.75rem;">
    <span class="lbl reveal-child" style="color:var(--g);">// The Energy</span>
    <h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);">INSIDE THE ROOM</h2>
  </div>
  <!-- Top: full-width hero photo -->
  <div style="width:100%;height:clamp(480px,58vw,800px);overflow:hidden;display:block;">
    <img src="/img/inside-the-room.jpg" alt="Packed rooftop crowd, treehouse. NYC"
      style="width:100%;height:100%;object-fit:cover;object-position:center 40%;display:block;">
  </div>
  <!-- Bottom: two equal photos side by side -->
  <div style="display:flex;height:clamp(260px,30vw,420px);">
    <div style="flex:1;overflow:hidden;">
      <img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere"
        style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
    <div style="flex:1;overflow:hidden;">
      <img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy"
        style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
  </div>
</section>"""

new_energy = """<!-- REMOVED R8: Inside the Room section — deleted entirely per Round 8 spec -->
<!--
<section class="lt" style="padding:0;" id="the-energy">
  <div style="padding:1.25rem clamp(1.5rem,5vw,5rem) 0.75rem;">
    <span class="lbl reveal-child" style="color:var(--g);">// The Energy</span>
    <h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);">INSIDE THE ROOM</h2>
  </div>
  <div style="width:100%;height:clamp(480px,58vw,800px);overflow:hidden;display:block;">
    <img src="/img/inside-the-room.jpg" alt="Packed rooftop crowd, treehouse. NYC"
      style="width:100%;height:100%;object-fit:cover;object-position:center 40%;display:block;">
  </div>
  <div style="display:flex;height:clamp(260px,30vw,420px);">
    <div style="flex:1;overflow:hidden;">
      <img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere"
        style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
    <div style="flex:1;overflow:hidden;">
      <img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy"
        style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
  </div>
</section>
-->
<!-- /REMOVED R8 -->"""

if old_energy in html:
    html = html.replace(old_energy, new_energy)
    fixes.append("FIX 1: Inside the Room section commented out")
else:
    # Try to find it with flexible whitespace
    pattern = r'<!-- INSIDE THE ROOM.*?</section>'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        old_text = m.group(0)
        html = html.replace(old_text, '<!-- REMOVED R8: Inside the Room section -->\n<!-- /REMOVED R8 -->')
        fixes.append("FIX 1: Inside the Room section commented out (regex match)")
    else:
        print("ERROR: Inside the Room section not found")

# ─────────────────────────────────────────────────────────────
# FIX 5 — Move vibe section to after April 25 section
# Current order: curate → vibe → April25 → [the-energy removed] → galleries
# Target order:  curate → April25 → vibe → galleries
# Strategy: extract the vibe section, remove it from current position,
#           insert it after the events section closing tag
# ─────────────────────────────────────────────────────────────

# Extract the vibe section
vibe_start_marker = '<section class="dk grain" id="vibe"'
vibe_end_marker = '</section>\n\n    <span class="marquee-item">'

vibe_start = html.find(vibe_start_marker)
if vibe_start == -1:
    print("ERROR: vibe section start not found")
else:
    # Find the closing </section> of the vibe section
    # The vibe section ends before the marquee items
    vibe_section_end = html.find('</section>', vibe_start)
    vibe_section_end += len('</section>')
    
    vibe_block = html[vibe_start:vibe_section_end]
    
    # Remove vibe from current position (including surrounding newlines)
    # Find the comment before it
    vibe_comment_start = html.rfind('\n', 0, vibe_start)
    
    # Remove the vibe block from current position
    html_without_vibe = html[:vibe_start].rstrip('\n') + '\n' + html[vibe_section_end:]
    
    # Now insert vibe after the events section (April 25)
    events_end = html_without_vibe.find('</section>\n<!-- INSIDE THE ROOM')
    if events_end == -1:
        # The-energy is now commented out, find the events section end differently
        events_end = html_without_vibe.find('</section>\n<!-- REMOVED R8: Inside the Room')
    if events_end == -1:
        # Find the events section end by looking for the closing of #events
        events_section_start = html_without_vibe.find('<section class="dk grain" id="events">')
        if events_section_start != -1:
            events_end = html_without_vibe.find('</section>', events_section_start)
    
    if events_end != -1:
        insert_pos = events_end + len('</section>')
        # Add ROUND 8 comment to vibe section
        vibe_block_r8 = '\n<!-- ROUND 8 FIX #5 — Main video moved to directly below April 25 section -->\n' + vibe_block
        html = html_without_vibe[:insert_pos] + '\n' + vibe_block_r8 + '\n' + html_without_vibe[insert_pos:]
        fixes.append("FIX 5: Vibe section moved to after April 25 section")
    else:
        print("ERROR: Could not find events section end for vibe insertion")
        html = html_without_vibe  # at least remove from old position

# ─────────────────────────────────────────────────────────────
# FIX 4 — Expand April 25 section to 80vh, image-dominant layout
# ─────────────────────────────────────────────────────────────
old_events_section = """<section class="dk grain" id="events">
  <div class="w event-grid">
    <div data-a="l">
      <span class="lbl reveal-child" style="margin-bottom:1.25rem">// Next Event</span>
      <h2 class="event-date">April 25th</h2>
      <p class="event-time">Doors 10:30pm — 3:30am ET</p>
      <div class="venue">
        <p class="venue-n">75 Varick Rooftop</p>
        <p class="venue-l">SoHo, New York City</p>
      </div>
      <p class="event-meta">300–400 guests · Invite Only · Open Bar</p>
      <a href="#join" class="btn btn-p">request your invite</a>
    </div>
    <div class="event-img" data-a="f" data-d="2" style="aspect-ratio:16/9;overflow:hidden;border-radius:var(--r);">
      <div class="venue-carousel" id="venueCarousel">
        <div class="vc-slide active"><img src="/img/varick-1.jpg" alt="75 Varick Rooftop — NYC skyline at dusk" loading="lazy"></div>
        <div class="vc-slide"><img src="/img/varick-2.jpg" alt="75 Varick Rooftop — venue interior" loading="lazy"></div>
        <div class="vc-slide"><img src="/img/varick-3.jpg" alt="75 Varick Rooftop — event space" loading="lazy"></div>
        <div class="vc-slide"><img src="/img/varick-4.jpg" alt="75 Varick Rooftop — rooftop view" loading="lazy"></div>
        <button class="vc-btn vc-prev" aria-label="Previous photo">&#8592;</button>
        <button class="vc-btn vc-next" aria-label="Next photo">&#8594;</button>
        <div class="vc-dots">
          <button class="vc-dot active" aria-label="Photo 1"></button>
          <button class="vc-dot" aria-label="Photo 2"></button>
          <button class="vc-dot" aria-label="Photo 3"></button>
          <button class="vc-dot" aria-label="Photo 4"></button>
        </div>
      </div>
    </div>
  </div>
</section>"""

new_events_section = """<!-- ROUND 8 FIX #4 — April 25 section expanded to 80vh, image-dominant layout -->
<section class="dk grain" id="events" style="padding:0;min-height:80vh;position:relative;overflow:hidden;display:flex;align-items:stretch;">
  <!-- Background carousel image (full-bleed) -->
  <div class="event-bg-carousel" id="venueCarousel" style="position:absolute;inset:0;z-index:0;">
    <div class="vc-slide active" style="position:absolute;inset:0;"><img src="/img/varick-1.jpg" alt="75 Varick Rooftop — NYC skyline at dusk" loading="eager" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-2.jpg" alt="75 Varick Rooftop — venue interior" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-3.jpg" alt="75 Varick Rooftop — event space" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-4.jpg" alt="75 Varick Rooftop — rooftop view" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <!-- Dark gradient overlay for text legibility -->
    <div style="position:absolute;inset:0;background:linear-gradient(to right, rgba(10,28,10,0.82) 0%, rgba(10,28,10,0.55) 50%, rgba(10,28,10,0.15) 100%);z-index:1;pointer-events:none;"></div>
    <button class="vc-btn vc-prev" aria-label="Previous photo" style="z-index:3;">&#8592;</button>
    <button class="vc-btn vc-next" aria-label="Next photo" style="z-index:3;">&#8594;</button>
    <div class="vc-dots" style="z-index:3;">
      <button class="vc-dot active" aria-label="Photo 1"></button>
      <button class="vc-dot" aria-label="Photo 2"></button>
      <button class="vc-dot" aria-label="Photo 3"></button>
      <button class="vc-dot" aria-label="Photo 4"></button>
    </div>
  </div>
  <!-- Event details overlay (left-aligned, on top of image) -->
  <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;padding:clamp(3rem,8vw,6rem) clamp(1.5rem,6vw,5rem);min-height:80vh;max-width:560px;">
    <span class="lbl reveal-child" style="margin-bottom:1.5rem;color:rgba(240,237,232,0.65);">// Next Event</span>
    <h2 class="event-date reveal-child" style="font-size:clamp(3.5rem,8vw,7rem);line-height:0.9;margin-bottom:1rem;">April 25th</h2>
    <!-- ROUND 8 FIX #4 — Countdown moved into this section for prominence -->
    <div style="margin-bottom:1.5rem;">
      <span style="font-family:var(--ff-b);font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(240,237,232,0.55);display:block;margin-bottom:0.5rem;">countdown</span>
      <div style="display:flex;align-items:baseline;gap:0.25rem;">
        <span class="countdown-num" id="countdown-days-2" style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);line-height:1;color:var(--ln);">--</span><span style="font-family:var(--ff-b);font-size:1rem;letter-spacing:0.1em;color:rgba(240,237,232,0.55);margin-right:0.75rem;">D</span>
        <span class="countdown-num" id="countdown-hours-2" style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);line-height:1;color:var(--ln);">--</span><span style="font-family:var(--ff-b);font-size:1rem;letter-spacing:0.1em;color:rgba(240,237,232,0.55);margin-right:0.75rem;">H</span>
        <span class="countdown-num" id="countdown-mins-2" style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);line-height:1;color:var(--ln);">--</span><span style="font-family:var(--ff-b);font-size:1rem;letter-spacing:0.1em;color:rgba(240,237,232,0.55);">M</span>
      </div>
    </div>
    <p class="event-time reveal-child" style="margin-bottom:0.5rem;">Doors 10:30pm — 3:30am ET</p>
    <div class="venue" style="margin-bottom:1rem;">
      <p class="venue-n">75 Varick Rooftop</p>
      <p class="venue-l">SoHo, New York City</p>
    </div>
    <p class="event-meta" style="margin-bottom:2rem;">300–400 guests · Invite Only · Open Bar</p>
    <a href="#join" class="btn btn-p" style="align-self:flex-start;">request your invite</a>
  </div>
</section>"""

if old_events_section in html:
    html = html.replace(old_events_section, new_events_section)
    fixes.append("FIX 4: April 25 section expanded to 80vh full-bleed image layout")
else:
    print("ERROR: events section not found for FIX 4")

# ─────────────────────────────────────────────────────────────
# FIX 2 — Expand curate section photo (remove max-height, remove overlay, use contain)
# ─────────────────────────────────────────────────────────────

# Fix the curate-section CSS: remove max-height:85vh, remove ::after gradient
old_curate_css = """/* ROUND 7 FIX — restore text overlay on curate section big picture */
/* ROUND 7 FIX #4 — cap height so image doesn't expand to 1580px */
.curate-section { position:relative; width:100%; overflow:hidden; max-height:85vh; }
.curate-section .dj-photo { width:100%; height:100%; object-fit:cover; display:block; }"""

new_curate_css = """/* ROUND 7 FIX — restore text overlay on curate section big picture */
/* ROUND 8 FIX #2 — show full photo, no cropping, no max-height cap */
.curate-section { position:relative; width:100%; overflow:visible; }
.curate-section .dj-photo { width:100%; height:auto; object-fit:contain; display:block; max-height:none; }"""

if old_curate_css in html:
    html = html.replace(old_curate_css, new_curate_css)
    fixes.append("FIX 2a: curate-section CSS — removed max-height, switched to object-fit:contain")
else:
    print("ERROR: curate-section CSS not found")

# Remove the ::after gradient overlay
old_curate_after = """.curate-section::after { content:''; position:absolute; inset:0; background:linear-gradient(to bottom, rgba(10,28,10,0.65) 0%, rgba(10,28,10,0.3) 45%, rgba(10,28,10,0.05) 100%); pointer-events:none; }"""
new_curate_after = """/* ROUND 8 FIX #2 — removed gradient overlay on curate section (show full clean photo) */
/* .curate-section::after was: gradient overlay — removed R8 */"""

if old_curate_after in html:
    html = html.replace(old_curate_after, new_curate_after)
    fixes.append("FIX 2b: curate-section ::after gradient overlay removed")
else:
    print("ERROR: curate-section ::after not found")

# Fix mobile curate rule too
old_mobile_curate = """/* ROUND 7 FIX #4b — mobile curate height */
@media(max-width:768px){ .curate-section { max-height:70vh; min-height:unset; } }"""
new_mobile_curate = """/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */
@media(max-width:768px){ .curate-section { max-height:none; min-height:unset; overflow:visible; } }"""

if old_mobile_curate in html:
    html = html.replace(old_mobile_curate, new_mobile_curate)
    fixes.append("FIX 2c: mobile curate max-height removed")
else:
    print("WARNING: mobile curate rule not found")

# Also fix the curate-copy position — since image is now natural height,
# the copy should flow below the image rather than be absolutely positioned over it
old_curate_copy_css = """.curate-section .curate-copy { position:absolute; top:clamp(3rem,12vw,8rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }"""
new_curate_copy_css = """/* ROUND 8 FIX #2d — curate-copy repositioned: overlays top of image */
.curate-section .curate-copy { position:absolute; top:clamp(2rem,8vw,5rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }"""

if old_curate_copy_css in html:
    html = html.replace(old_curate_copy_css, new_curate_copy_css)
    fixes.append("FIX 2d: curate-copy position adjusted for natural-height image")
else:
    print("WARNING: curate-copy CSS not found exactly")

# ─────────────────────────────────────────────────────────────
# FIX 3 — Reword curate heading (Option B) and update body copy
# ─────────────────────────────────────────────────────────────
old_heading = """    <h2>We curate<br>the room.</h2>
    <p>Themed parties. Open bar. Good music. The kind of night you text about the next day. Five events in, still selling out.</p>"""

new_heading = """    <!-- ROUND 8 FIX #3 — Heading reworded (Option B): guest-first, no brand ego -->
    <h2>Some nights<br>stay with you.</h2>
    <p>Open bar. Good music. The kind of crowd that makes the night. Five events in, still selling out.</p>"""

if old_heading in html:
    html = html.replace(old_heading, new_heading)
    fixes.append("FIX 3: Curate heading reworded to 'Some nights stay with you.'")
else:
    print("ERROR: curate heading not found")

# Also update the lbl text
old_lbl = '    <span class="lbl reveal-child" style="color:rgba(240,237,232,0.55);margin-bottom:1rem;display:block;">// Who We Are</span>'
new_lbl = '    <!-- ROUND 8 FIX #3 — label kept as-is -->\n    <span class="lbl reveal-child" style="color:rgba(240,237,232,0.55);margin-bottom:1rem;display:block;">// Who We Are</span>'
if old_lbl in html:
    html = html.replace(old_lbl, new_lbl)

# ─────────────────────────────────────────────────────────────
# FIX 6 — Add new photos to gallery sections
# ─────────────────────────────────────────────────────────────

# TRIBECA: Comment out tribeca-022, add 2 new photos in its place
old_tribeca_022 = '    <div class="gallery-item"><img src="/img/gallery/tribeca-rooftop/tribeca-022.jpg" alt="treehouse. event photo" loading="eager"></div>'
new_tribeca_022 = """    <!-- REMOVED R8: tribeca-022 replaced by tribeca-new-01 and tribeca-new-02 -->
    <!-- <div class="gallery-item"><img src="/img/gallery/tribeca-rooftop/tribeca-022.jpg" alt="treehouse. event photo" loading="eager"></div> -->
    <!-- ROUND 8 FIX #6 — 2 new Tribeca photos added -->
    <div class="gallery-item"><img src="/img/tribeca-new-01.jpg" alt="treehouse. NYC — Tribeca Rooftop" loading="lazy"></div>
    <div class="gallery-item"><img src="/img/tribeca-new-02.jpg" alt="treehouse. NYC — Tribeca Rooftop" loading="lazy"></div>"""

if old_tribeca_022 in html:
    html = html.replace(old_tribeca_022, new_tribeca_022)
    fixes.append("FIX 6a: Tribeca — tribeca-022 commented out, tribeca-new-01 and -02 added (9 total)")
else:
    print("ERROR: tribeca-022 gallery item not found")

# SOHO: Add 7 new photos distributed throughout the existing 13
# Find the soho gallery-visible div and insert new photos at positions 3,5,7,9,11,13,15
soho_gallery_start = html.find('<div class="gallery-visible" id="gallery-visible-soho-soiree">')
soho_gallery_end = html.find('</div>', soho_gallery_start)
# Find the actual end (closing of gallery-visible)
soho_section_end = html.find('<!-- REMOVED R6: gallery-collapsed-soho-soiree', soho_gallery_start)

if soho_gallery_start == -1:
    print("ERROR: soho gallery-visible not found")
else:
    soho_block = html[soho_gallery_start:soho_section_end]
    
    # Split into individual gallery items
    items = re.findall(r'    <div class="gallery-item">.*?</div>', soho_block, re.DOTALL)
    print(f"  Found {len(items)} soho gallery items")
    
    new_soho_items = [
        '    <!-- ROUND 8 FIX #6 — soho-new-01 added -->\n    <div class="gallery-item"><img src="/img/soho-new-01.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-02 added -->\n    <div class="gallery-item"><img src="/img/soho-new-02.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-03 added -->\n    <div class="gallery-item"><img src="/img/soho-new-03.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-04 added -->\n    <div class="gallery-item"><img src="/img/soho-new-04.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-05 added -->\n    <div class="gallery-item"><img src="/img/soho-new-05.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-06 added -->\n    <div class="gallery-item"><img src="/img/soho-new-06.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-07 added -->\n    <div class="gallery-item"><img src="/img/soho-new-07.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
    ]
    
    # Distribute: insert after items at positions 2, 4, 6, 8, 10, 12, 13 (0-indexed)
    insert_positions = [2, 4, 6, 8, 10, 12, 13]
    
    # Build new item list with insertions
    new_items_list = list(items)
    for offset, (pos, new_item) in enumerate(zip(insert_positions, new_soho_items)):
        new_items_list.insert(pos + offset, new_item)
    
    # Reconstruct the soho block header and footer
    soho_header = soho_block[:soho_block.find('    <div class="gallery-item">')]
    new_soho_block = soho_header + '\n'.join(new_items_list) + '\n  '
    
    html = html[:soho_gallery_start] + new_soho_block + html[soho_section_end:]
    fixes.append("FIX 6b: SoHo — 7 new photos distributed throughout gallery (20 total)")

# CHRISTMAS: Add xmas-new-01 at position 2 (early, visually strong)
xmas_gallery_start = html.find('<div class="gallery-visible" id="gallery-visible-christmas-nyc">')
xmas_section_end = html.find('<!-- REMOVED R6: gallery-collapsed-christmas-nyc', xmas_gallery_start)

if xmas_gallery_start == -1:
    print("ERROR: christmas gallery-visible not found")
else:
    xmas_block = html[xmas_gallery_start:xmas_section_end]
    xmas_items = re.findall(r'    <div class="gallery-item">.*?</div>', xmas_block, re.DOTALL)
    print(f"  Found {len(xmas_items)} christmas gallery items")
    
    # Insert xmas-new-01 at position 2 (after the 2nd item)
    new_xmas_item = '    <!-- ROUND 8 FIX #6 — xmas-new-01 added at position 2 -->\n    <div class="gallery-item"><img src="/img/xmas-new-01.jpg" alt="treehouse. NYC — Christmas in NYC" loading="lazy"></div>'
    
    xmas_items_new = list(xmas_items)
    xmas_items_new.insert(2, new_xmas_item)
    
    xmas_header = xmas_block[:xmas_block.find('    <div class="gallery-item">')]
    new_xmas_block = xmas_header + '\n'.join(xmas_items_new) + '\n  '
    
    html = html[:xmas_gallery_start] + new_xmas_block + html[xmas_section_end:]
    fixes.append("FIX 6c: Christmas — xmas-new-01 added at position 2 (16 total)")

# ─────────────────────────────────────────────────────────────
# Add countdown sync JS for the new countdown-days-2 / countdown-hours-2 / countdown-mins-2 IDs
# ─────────────────────────────────────────────────────────────
old_countdown_js = "// ── COUNTDOWN ──"
new_countdown_js = """// ── COUNTDOWN ──
// ROUND 8 FIX #4 — sync secondary countdown in April 25 section"""

# Find the countdown JS and add syncing for the new IDs
countdown_pattern = r"(function updateCountdown\(\)\s*\{.*?)(const days = Math\.floor\(diff / 86400\);.*?)(document\.getElementById\('countdown-days'\)\.textContent = String\(days\)\.padStart\(2,'0'\);)"
m = re.search(countdown_pattern, html, re.DOTALL)
if m:
    # Find the countdown update block and add the secondary IDs
    old_cd_update = "document.getElementById('countdown-days').textContent = String(days).padStart(2,'0');\n        document.getElementById('countdown-hours').textContent = String(hours).padStart(2,'0');"
    new_cd_update = """document.getElementById('countdown-days').textContent = String(days).padStart(2,'0');
        document.getElementById('countdown-hours').textContent = String(hours).padStart(2,'0');
        // ROUND 8 FIX #4 — sync secondary countdown display
        const d2 = document.getElementById('countdown-days-2');
        const h2 = document.getElementById('countdown-hours-2');
        const m2 = document.getElementById('countdown-mins-2');
        if(d2) d2.textContent = String(days).padStart(2,'0');
        if(h2) h2.textContent = String(hours).padStart(2,'0');
        if(m2) m2.textContent = String(mins).padStart(2,'0');"""
    if old_cd_update in html:
        html = html.replace(old_cd_update, new_cd_update)
        fixes.append("FIX 4b: Secondary countdown IDs synced in JS")
    else:
        print("WARNING: countdown update JS not found exactly")
else:
    print("WARNING: countdown function not found via regex")

with open('index.html', 'w') as f:
    f.write(html)

print(f"\nApplied {len(fixes)} fixes:")
for fix in fixes:
    print(f"  ✓ {fix}")
print(f"\nFile size: {original_len} -> {len(html)} chars ({len(html)-original_len:+d})")
