#!/usr/bin/env python3
"""Round 8 — Clean fix script that preserves full HTML structure"""

import re

with open('index.html', 'r') as f:
    html = f.read()

original_len = len(html)
fixes = []

# ─────────────────────────────────────────────────────────────
# FIX 1 — Comment out the entire "Inside the Room" section
# ─────────────────────────────────────────────────────────────
pattern = r'<!-- INSIDE THE ROOM.*?</section>'
m = re.search(pattern, html, re.DOTALL)
if m:
    old_text = m.group(0)
    new_text = '<!-- REMOVED R8: Inside the Room section — deleted entirely per Round 8 spec\n' + old_text + '\n/REMOVED R8 -->'
    html = html.replace(old_text, new_text)
    fixes.append("FIX 1: Inside the Room section commented out")
else:
    print("ERROR: Inside the Room section not found")

# ─────────────────────────────────────────────────────────────
# FIX 5 — Move vibe section to after April 25 section
# ─────────────────────────────────────────────────────────────
# Extract the vibe section (id="vibe")
vibe_pattern = r'<section class="dk grain" id="vibe"[^>]*>.*?</section>'
vibe_match = re.search(vibe_pattern, html, re.DOTALL)
if vibe_match:
    vibe_block = vibe_match.group(0)
    # Remove from current position
    html = html.replace(vibe_block, '<!-- ROUND 8 FIX #5 — vibe section moved below April 25 -->')
    
    # Insert after the events section (April 25)
    # The events section ends with </section> followed by the Inside the Room comment
    events_end_pattern = r'(</section>)\s*\n(<!-- (?:INSIDE THE ROOM|REMOVED R8: Inside the Room))'
    m2 = re.search(events_end_pattern, html, re.DOTALL)
    if m2:
        insert_after = m2.start() + len(m2.group(1))
        vibe_insert = '\n<!-- ROUND 8 FIX #5 — Main video restored directly below April 25 section -->\n' + vibe_block + '\n'
        html = html[:insert_after] + vibe_insert + html[insert_after:]
        fixes.append("FIX 5: Vibe section moved to after April 25 section")
    else:
        print("ERROR: Could not find events section end for vibe insertion")
else:
    print("ERROR: vibe section not found")

# ─────────────────────────────────────────────────────────────
# FIX 4 — Expand April 25 section to 80vh, full-bleed image
# ─────────────────────────────────────────────────────────────
old_events_open = '<section class="dk grain" id="events">'
new_events_open = '<!-- ROUND 8 FIX #4 — April 25 section expanded to 80vh, full-bleed image -->\n<section class="dk grain" id="events" style="padding:0;min-height:80vh;position:relative;overflow:hidden;display:flex;align-items:stretch;">'

if old_events_open in html:
    html = html.replace(old_events_open, new_events_open)
    fixes.append("FIX 4a: events section min-height:80vh added")
else:
    print("ERROR: events section open tag not found")

# Replace the inner event-grid with full-bleed layout
old_events_inner = """  <div class="w event-grid">
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
  </div>"""

new_events_inner = """  <!-- ROUND 8 FIX #4 — Full-bleed carousel background with overlay text -->
  <!-- Background carousel (absolute, fills section) -->
  <div class="event-bg-carousel" id="venueCarousel" style="position:absolute;inset:0;z-index:0;">
    <div class="vc-slide active" style="position:absolute;inset:0;"><img src="/img/varick-1.jpg" alt="75 Varick Rooftop — NYC skyline at dusk" loading="eager" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-2.jpg" alt="75 Varick Rooftop — venue interior" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-3.jpg" alt="75 Varick Rooftop — event space" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div class="vc-slide" style="position:absolute;inset:0;"><img src="/img/varick-4.jpg" alt="75 Varick Rooftop — rooftop view" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(to right, rgba(10,28,10,0.85) 0%, rgba(10,28,10,0.55) 55%, rgba(10,28,10,0.1) 100%);z-index:1;pointer-events:none;"></div>
    <button class="vc-btn vc-prev" aria-label="Previous photo" style="z-index:3;">&#8592;</button>
    <button class="vc-btn vc-next" aria-label="Next photo" style="z-index:3;">&#8594;</button>
    <div class="vc-dots" style="z-index:3;">
      <button class="vc-dot active" aria-label="Photo 1"></button>
      <button class="vc-dot" aria-label="Photo 2"></button>
      <button class="vc-dot" aria-label="Photo 3"></button>
      <button class="vc-dot" aria-label="Photo 4"></button>
    </div>
  </div>
  <!-- Event details overlay -->
  <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;padding:clamp(3rem,8vw,6rem) clamp(1.5rem,6vw,5rem);min-height:80vh;max-width:580px;">
    <span class="lbl reveal-child" style="margin-bottom:1.5rem;color:rgba(240,237,232,0.65);">// Next Event</span>
    <h2 class="event-date reveal-child" style="font-size:clamp(3.5rem,8vw,7rem);line-height:0.9;margin-bottom:1.25rem;">April 25th</h2>
    <!-- ROUND 8 FIX #4 — Prominent countdown in this section -->
    <div style="margin-bottom:1.75rem;">
      <span style="font-family:var(--ff-b);font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:rgba(240,237,232,0.5);display:block;margin-bottom:0.5rem;">until doors open</span>
      <div style="display:flex;align-items:baseline;gap:0.1rem;">
        <span class="countdown-num" id="countdown-days-2" style="font-size:clamp(2.8rem,6vw,5rem);line-height:1;">--</span><span style="font-family:var(--ff-b);font-size:0.9rem;letter-spacing:0.1em;color:rgba(240,237,232,0.5);margin-right:0.75rem;align-self:flex-end;padding-bottom:0.3rem;">D</span>
        <span class="countdown-num" id="countdown-hours-2" style="font-size:clamp(2.8rem,6vw,5rem);line-height:1;">--</span><span style="font-family:var(--ff-b);font-size:0.9rem;letter-spacing:0.1em;color:rgba(240,237,232,0.5);margin-right:0.75rem;align-self:flex-end;padding-bottom:0.3rem;">H</span>
        <span class="countdown-num" id="countdown-mins-2" style="font-size:clamp(2.8rem,6vw,5rem);line-height:1;">--</span><span style="font-family:var(--ff-b);font-size:0.9rem;letter-spacing:0.1em;color:rgba(240,237,232,0.5);align-self:flex-end;padding-bottom:0.3rem;">M</span>
      </div>
    </div>
    <p class="event-time reveal-child" style="margin-bottom:0.5rem;">Doors 10:30pm — 3:30am ET</p>
    <div class="venue" style="margin-bottom:1rem;">
      <p class="venue-n">75 Varick Rooftop</p>
      <p class="venue-l">SoHo, New York City</p>
    </div>
    <p class="event-meta" style="margin-bottom:2rem;">300–400 guests · Invite Only · Open Bar</p>
    <a href="#join" class="btn btn-p" style="align-self:flex-start;">request your invite</a>
  </div>"""

if old_events_inner in html:
    html = html.replace(old_events_inner, new_events_inner)
    fixes.append("FIX 4b: April 25 inner layout replaced with full-bleed image + overlay text")
else:
    print("ERROR: events inner content not found")

# ─────────────────────────────────────────────────────────────
# FIX 2 — Expand curate section photo (remove max-height, remove overlay, use contain)
# ─────────────────────────────────────────────────────────────
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
new_curate_after = """/* ROUND 8 FIX #2 — gradient overlay on curate section removed (show full clean photo) */"""

if old_curate_after in html:
    html = html.replace(old_curate_after, new_curate_after)
    fixes.append("FIX 2b: curate-section ::after gradient overlay removed")
else:
    print("ERROR: curate-section ::after not found")

# Fix mobile curate rule
old_mobile_curate = """/* ROUND 7 FIX #4b — mobile curate height */
@media(max-width:768px){ .curate-section { max-height:70vh; min-height:unset; } }"""
new_mobile_curate = """/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */
@media(max-width:768px){ .curate-section { max-height:none; min-height:unset; overflow:visible; } }"""

if old_mobile_curate in html:
    html = html.replace(old_mobile_curate, new_mobile_curate)
    fixes.append("FIX 2c: mobile curate max-height removed")
else:
    print("WARNING: mobile curate rule not found")

# ─────────────────────────────────────────────────────────────
# FIX 3 — Reword curate heading (Option B) and update body copy
# ─────────────────────────────────────────────────────────────
old_heading = '    <h2>We curate<br>the room.</h2>'
new_heading = '    <!-- ROUND 8 FIX #3 — Heading reworded: guest-first, no brand ego (Option B) -->\n    <h2>Some nights<br>stay with you.</h2>'

if old_heading in html:
    html = html.replace(old_heading, new_heading)
    fixes.append("FIX 3a: Curate heading -> 'Some nights stay with you.'")
else:
    print("ERROR: curate heading not found")

old_body = '    <p>Themed parties. Open bar. Good music. The kind of night you text about the next day. Five events in, still selling out.</p>'
new_body = '    <!-- ROUND 8 FIX #3 — Body copy rewritten: guest experience, not brand pitch -->\n    <p>Open bar. Good music. The kind of crowd that makes the night. Five events in, still selling out.</p>'

if old_body in html:
    html = html.replace(old_body, new_body)
    fixes.append("FIX 3b: Body copy rewritten to guest-experience focus")
else:
    print("ERROR: curate body copy not found")

# ─────────────────────────────────────────────────────────────
# FIX 6a — Tribeca: comment out tribeca-022, add 2 new photos
# ─────────────────────────────────────────────────────────────
tribeca_022_pattern = r'    <div class="gallery-item"><img src="/img/gallery/tribeca-rooftop/tribeca-022\.jpg"[^>]+></div>'
m = re.search(tribeca_022_pattern, html)
if m:
    old_t022 = m.group(0)
    new_t022 = """    <!-- REMOVED R8: tribeca-022 replaced by tribeca-new-01 and tribeca-new-02 -->
    <!-- """ + old_t022.strip() + """ -->
    <!-- ROUND 8 FIX #6 — 2 new Tribeca photos added -->
    <div class="gallery-item"><img src="/img/tribeca-new-01.jpg" alt="treehouse. NYC — Tribeca Rooftop" loading="lazy"></div>
    <div class="gallery-item"><img src="/img/tribeca-new-02.jpg" alt="treehouse. NYC — Tribeca Rooftop" loading="lazy"></div>"""
    html = html.replace(old_t022, new_t022)
    fixes.append("FIX 6a: Tribeca — tribeca-022 commented out, 2 new photos added (9 total)")
else:
    print("ERROR: tribeca-022 not found")

# ─────────────────────────────────────────────────────────────
# FIX 6b — SoHo: add 7 new photos distributed throughout
# Use precise string insertion to avoid truncation
# ─────────────────────────────────────────────────────────────
# Find the 13 soho items and insert new ones at specific positions
soho_gallery_id = '<div class="gallery-visible" id="gallery-visible-soho-soiree">'
soho_start = html.find(soho_gallery_id)
soho_end_comment = '  <!-- REMOVED R6: gallery-collapsed-soho-soiree'
soho_end = html.find(soho_end_comment, soho_start)

if soho_start == -1 or soho_end == -1:
    print(f"ERROR: soho gallery bounds not found (start={soho_start}, end={soho_end})")
else:
    soho_block = html[soho_start:soho_end]
    
    # Find all gallery items in soho block
    item_pattern = r'    <div class="gallery-item">.*?</div>'
    items = re.findall(item_pattern, soho_block, re.DOTALL)
    print(f"  Soho items found: {len(items)}")
    
    new_photos = [
        '    <!-- ROUND 8 FIX #6 — soho-new-01 -->\n    <div class="gallery-item"><img src="/img/soho-new-01.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-02 -->\n    <div class="gallery-item"><img src="/img/soho-new-02.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-03 -->\n    <div class="gallery-item"><img src="/img/soho-new-03.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-04 -->\n    <div class="gallery-item"><img src="/img/soho-new-04.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-05 -->\n    <div class="gallery-item"><img src="/img/soho-new-05.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-06 -->\n    <div class="gallery-item"><img src="/img/soho-new-06.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
        '    <!-- ROUND 8 FIX #6 — soho-new-07 -->\n    <div class="gallery-item"><img src="/img/soho-new-07.jpg" alt="treehouse. NYC — SoHo Soiree" loading="lazy"></div>',
    ]
    
    # Distribute: insert after items 1, 3, 5, 7, 9, 11, 12 (0-indexed)
    insert_after_positions = [1, 3, 5, 7, 9, 11, 12]
    
    # Build new soho block by inserting items at correct positions
    new_items = list(items)
    for offset, (pos, new_photo) in enumerate(zip(insert_after_positions, new_photos)):
        new_items.insert(pos + 1 + offset, new_photo)
    
    # Reconstruct soho block
    # Header is everything before the first gallery-item
    first_item_pos = soho_block.find('    <div class="gallery-item">')
    soho_header = soho_block[:first_item_pos]
    # Footer is the closing </div> of gallery-visible
    last_item_end = soho_block.rfind('</div>') + 6
    soho_footer = soho_block[last_item_end:]
    
    new_soho_block = soho_header + '\n'.join(new_items) + '\n' + soho_footer
    
    # Replace in html
    html = html[:soho_start] + new_soho_block + html[soho_end:]
    
    # Verify
    new_soho_check = re.findall(r'<div class="gallery-item">', new_soho_block)
    print(f"  Soho items after insertion: {len(new_soho_check)}")
    fixes.append(f"FIX 6b: SoHo — 7 new photos distributed throughout ({len(new_soho_check)} total)")

# ─────────────────────────────────────────────────────────────
# FIX 6c — Christmas: add xmas-new-01 at position 2
# ─────────────────────────────────────────────────────────────
xmas_gallery_id = '<div class="gallery-visible" id="gallery-visible-christmas-nyc">'
xmas_start = html.find(xmas_gallery_id)
xmas_end_comment = '  <!-- REMOVED R6: gallery-collapsed-christmas-nyc'
xmas_end = html.find(xmas_end_comment, xmas_start)

if xmas_start == -1 or xmas_end == -1:
    print(f"ERROR: christmas gallery bounds not found (start={xmas_start}, end={xmas_end})")
else:
    xmas_block = html[xmas_start:xmas_end]
    item_pattern = r'    <div class="gallery-item">.*?</div>'
    xmas_items = re.findall(item_pattern, xmas_block, re.DOTALL)
    print(f"  Christmas items found: {len(xmas_items)}")
    
    new_xmas_item = '    <!-- ROUND 8 FIX #6 — xmas-new-01 added at position 2 -->\n    <div class="gallery-item"><img src="/img/xmas-new-01.jpg" alt="treehouse. NYC — Christmas in NYC" loading="lazy"></div>'
    
    new_xmas_items = list(xmas_items)
    new_xmas_items.insert(2, new_xmas_item)
    
    first_item_pos = xmas_block.find('    <div class="gallery-item">')
    xmas_header = xmas_block[:first_item_pos]
    last_item_end = xmas_block.rfind('</div>') + 6
    xmas_footer = xmas_block[last_item_end:]
    
    new_xmas_block = xmas_header + '\n'.join(new_xmas_items) + '\n' + xmas_footer
    html = html[:xmas_start] + new_xmas_block + html[xmas_end:]
    
    new_xmas_check = re.findall(r'<div class="gallery-item">', new_xmas_block)
    print(f"  Christmas items after insertion: {len(new_xmas_check)}")
    fixes.append(f"FIX 6c: Christmas — xmas-new-01 added ({len(new_xmas_check)} total)")

# ─────────────────────────────────────────────────────────────
# Add countdown JS sync for secondary IDs
# Find the countdown update in photos.js (it's in a separate file)
# Instead, add inline script at end of body
# ─────────────────────────────────────────────────────────────
old_script_ref = '<script src="/photos.js"></script>'
new_script_ref = '''<script src="/photos.js"></script>
<!-- ROUND 8 FIX #4 — Sync secondary countdown IDs in April 25 section -->
<script>
(function(){
  function syncCountdown2(){
    var d=document.getElementById('countdown-days');
    var h=document.getElementById('countdown-hours');
    var d2=document.getElementById('countdown-days-2');
    var h2=document.getElementById('countdown-hours-2');
    var m2=document.getElementById('countdown-mins-2');
    if(d&&d2) d2.textContent=d.textContent;
    if(h&&h2) h2.textContent=h.textContent;
    if(m2){
      var now=new Date();
      var event=new Date('2026-04-25T22:30:00-04:00');
      var diff=Math.max(0,Math.floor((event-now)/1000));
      var mins=Math.floor((diff%3600)/60);
      m2.textContent=String(mins).padStart(2,'0');
    }
  }
  setInterval(syncCountdown2, 1000);
  setTimeout(syncCountdown2, 500);
})();
</script>'''

if old_script_ref in html:
    html = html.replace(old_script_ref, new_script_ref)
    fixes.append("FIX 4c: Secondary countdown sync script added")
else:
    print("WARNING: photos.js script tag not found")

# ─────────────────────────────────────────────────────────────
# Verify HTML is complete
# ─────────────────────────────────────────────────────────────
assert '</html>' in html, "ERROR: HTML is missing closing tag!"
assert html.count('<html') == 1, "ERROR: Multiple <html> tags!"

with open('index.html', 'w') as f:
    f.write(html)

print(f"\nApplied {len(fixes)} fixes:")
for fix in fixes:
    print(f"  ✓ {fix}")
print(f"\nFile size: {original_len} -> {len(html)} chars ({len(html)-original_len:+d})")
print(f"HTML complete: {'</html>' in html}")
print(f"Line count: {html.count(chr(10))}")
