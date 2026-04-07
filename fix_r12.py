import re

with open('index.html') as f:
    content = f.read()

original_len = len(content)
fixes_applied = []

# ─────────────────────────────────────────────────────────────
# FIX #3 — Remove aspect-ratio:1/1 from gallery-item, fix img
# ─────────────────────────────────────────────────────────────
# Current (lines 548-549):
# .gallery-item { aspect-ratio:1/1; overflow:hidden; }
# .gallery-item img { width:100%; height:100%; object-fit:cover; object-position:center; display:block; }

old_gi = '.gallery-item { aspect-ratio:1/1; overflow:hidden; }'
new_gi = '/* ROUND 12 FIX #3 — removed aspect-ratio:1/1 so photos show at natural height, no cropping */\n.gallery-item { overflow:hidden; }'

if old_gi in content:
    content = content.replace(old_gi, new_gi)
    fixes_applied.append('FIX #3a: gallery-item aspect-ratio removed')
else:
    print(f'ERROR: gallery-item rule not found: {repr(old_gi[:60])}')

old_gi_img = '.gallery-item img { width:100%; height:100%; object-fit:cover; object-position:center; display:block; }'
new_gi_img = '/* ROUND 12 FIX #3 — height:auto + object-fit:unset so full photo always visible */\n.gallery-item img { width:100%; height:auto; object-fit:unset; display:block; }'

if old_gi_img in content:
    content = content.replace(old_gi_img, new_gi_img)
    fixes_applied.append('FIX #3b: gallery-item img changed to height:auto, object-fit:unset')
else:
    print(f'ERROR: gallery-item img rule not found: {repr(old_gi_img[:60])}')

# ─────────────────────────────────────────────────────────────
# FIX #4 — Video: 65vh -> 85vh
# ─────────────────────────────────────────────────────────────
old_video_block = '''.vibe-reel { padding:0 !important; overflow:hidden; max-height:65vh; position:relative; }
.vr-inner { padding:0; max-width:100%; position:relative; }
.vr-inner video { width:100%; display:block; max-height:65vh; object-fit:cover; }'''

new_video_block = '''/* ROUND 12 FIX #4 — video height increased from 65vh to 85vh so people aren't cut off */
.vibe-reel { padding:0 !important; overflow:hidden; max-height:85vh; position:relative; }
.vr-inner { padding:0; max-width:100%; position:relative; }
.vr-inner video { width:100%; display:block; max-height:85vh; object-fit:cover; }'''

if old_video_block in content:
    content = content.replace(old_video_block, new_video_block)
    fixes_applied.append('FIX #4: video max-height changed from 65vh to 85vh')
else:
    print(f'ERROR: video block not found')
    # Try partial match
    if 'max-height:65vh; position:relative; }' in content:
        content = content.replace('max-height:65vh; position:relative; }', 'max-height:85vh; position:relative; } /* ROUND 12 FIX #4 */')
        content = content.replace('.vr-inner video { width:100%; display:block; max-height:65vh; object-fit:cover; }',
                                   '.vr-inner video { width:100%; display:block; max-height:85vh; object-fit:cover; } /* ROUND 12 FIX #4 */')
        fixes_applied.append('FIX #4 (partial): video max-height patched to 85vh')

# Fix mobile video too
old_mob_video = '@media(max-width:768px){ .vibe-reel { max-height:65vw; } .vr-inner video { max-height:65vw; } }'
new_mob_video = '/* ROUND 12 FIX #4 mobile — 65vw -> 85vw */\n@media(max-width:768px){ .vibe-reel { max-height:85vw; } .vr-inner video { max-height:85vw; } }'

if old_mob_video in content:
    content = content.replace(old_mob_video, new_mob_video)
    fixes_applied.append('FIX #4 mobile: video max-height changed from 65vw to 85vw')
else:
    print('ERROR: mobile video rule not found')

# ─────────────────────────────────────────────────────────────
# FIX #5 — Curate section photo: add max-height:45vh
# ─────────────────────────────────────────────────────────────
old_curate_img = '.curate-section .dj-photo { width:100%; height:auto; object-fit:contain; display:block; max-height:none; }'
new_curate_img = '/* ROUND 12 FIX #5 — curate photo reduced to 45vh desktop (was max-height:none), full image still visible via object-fit:contain */\n.curate-section .dj-photo { width:100%; height:auto; object-fit:contain; display:block; max-height:45vh; }'

if old_curate_img in content:
    content = content.replace(old_curate_img, new_curate_img)
    fixes_applied.append('FIX #5: curate photo max-height set to 45vh')
else:
    print(f'ERROR: curate img rule not found')

# Also add mobile curate override
old_mob_curate = '/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */\n@media(max-width:768px){ .curate-section { max-height:none; min-height:unset; overflow:visible; } }'
new_mob_curate = '/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */\n/* ROUND 12 FIX #5 mobile — curate photo max-height on mobile */\n@media(max-width:768px){ .curate-section { max-height:none; min-height:unset; overflow:visible; } .curate-section .dj-photo { max-height:55vw; } }'

if old_mob_curate in content:
    content = content.replace(old_mob_curate, new_mob_curate)
    fixes_applied.append('FIX #5 mobile: curate photo max-height set to 55vw on mobile')
else:
    print('NOTE: mobile curate block not found exactly, skipping mobile override')

# ─────────────────────────────────────────────────────────────
# FIX #1 — Add 2 Knox Day photos
# ─────────────────────────────────────────────────────────────
# Find the Knox Day gallery-visible div and insert photos at positions 2 and 8
# First, find the Knox gallery block
knox_start = content.find('id="gallery-visible-knox-day"')
if knox_start == -1:
    # Try alternate ID format
    knox_start = content.find('knox-day')
    print(f'Knox gallery-visible not found by ID, searching by name at {knox_start}')

# Find the first gallery-item in Knox to insert after
knox_block_start = content.find('<div class="gallery-item">', knox_start)
if knox_block_start != -1:
    # Insert knox-new-01 after the first gallery-item's closing tag
    # Find end of first gallery-item
    depth = 0
    pos = knox_block_start
    while pos < len(content):
        if content[pos:pos+4] == '<div':
            depth += 1
        elif content[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                first_item_end = pos + 6
                break
        pos += 1
    
    knox_new_01 = '''
        <!-- ROUND 12 FIX #1 — knox-new-01.jpg added to Knox Day gallery -->
        <div class="gallery-item">
          <img src="/img/knox-new-01.jpg" alt="Knox Day treehouse. NYC" loading="lazy" style="width:100%;height:auto;display:block;" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">knox</div>
        </div>'''
    
    content = content[:first_item_end] + knox_new_01 + content[first_item_end:]
    fixes_applied.append('FIX #1a: knox-new-01.jpg inserted at position 2 in Knox Day gallery')
    
    # Now find position 8 (after 7 more gallery-items from where we are)
    # Re-find Knox start after modification
    knox_start2 = content.find('id="gallery-visible-knox-day"')
    items_found = 0
    pos2 = content.find('<div class="gallery-item">', knox_start2)
    while pos2 != -1 and items_found < 7:
        next_pos = content.find('<div class="gallery-item">', pos2 + 1)
        if next_pos == -1:
            break
        pos2 = next_pos
        items_found += 1
    
    # Find end of the 8th item
    depth = 0
    pos3 = pos2
    while pos3 < len(content):
        if content[pos3:pos3+4] == '<div':
            depth += 1
        elif content[pos3:pos3+6] == '</div>':
            depth -= 1
            if depth == 0:
                eighth_item_end = pos3 + 6
                break
        pos3 += 1
    
    knox_new_02 = '''
        <!-- ROUND 12 FIX #1 — knox-new-02.jpg added to Knox Day gallery -->
        <div class="gallery-item">
          <img src="/img/knox-new-02.jpg" alt="Knox Day treehouse. NYC" loading="lazy" style="width:100%;height:auto;display:block;" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">knox</div>
        </div>'''
    
    content = content[:eighth_item_end] + knox_new_02 + content[eighth_item_end:]
    fixes_applied.append('FIX #1b: knox-new-02.jpg inserted at position 9 in Knox Day gallery')
else:
    print('ERROR: Knox gallery-item not found')

# ─────────────────────────────────────────────────────────────
# FIX #2 — Add 5 Tribeca photos
# ─────────────────────────────────────────────────────────────
tribeca_photos = [
    ('tribeca-new-03.jpg', 2, 'position 2'),
    ('tribeca-new-04.jpg', 4, 'position 4'),
    ('tribeca-new-05.jpg', 7, 'position 7'),
    ('tribeca-new-06.jpg', 10, 'position 10'),
    ('tribeca-new-07.jpg', 13, 'position 13'),
]

def insert_after_nth_gallery_item(html_content, section_id, n, new_item_html):
    """Insert new_item_html after the nth gallery-item in the section with given id."""
    sec_start = html_content.find(f'id="{section_id}"')
    if sec_start == -1:
        return html_content, False
    
    items_found = 0
    pos = html_content.find('<div class="gallery-item">', sec_start)
    while pos != -1:
        items_found += 1
        # Find end of this item
        depth = 0
        p = pos
        while p < len(html_content):
            if html_content[p:p+4] == '<div':
                depth += 1
            elif html_content[p:p+6] == '</div>':
                depth -= 1
                if depth == 0:
                    item_end = p + 6
                    break
            p += 1
        
        if items_found == n:
            return html_content[:item_end] + new_item_html + html_content[item_end:], True
        
        pos = html_content.find('<div class="gallery-item">', pos + 1)
    
    # If n > total items, append at end
    # Find the closing of the gallery-visible div
    return html_content, False

# Insert tribeca photos one by one, adjusting positions as we insert
# We insert in reverse order of position to avoid index shifting
# Actually insert in forward order but recalculate each time
offset = 0
for fname, pos_n, pos_label in tribeca_photos:
    new_item = f'''
        <!-- ROUND 12 FIX #2 — {fname} added to Tribeca gallery at {pos_label} -->
        <div class="gallery-item">
          <img src="/img/{fname}" alt="Tribeca Rooftop treehouse. NYC" loading="lazy" style="width:100%;height:auto;display:block;" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">tribeca</div>
        </div>'''
    
    actual_pos = pos_n + offset
    new_content, ok = insert_after_nth_gallery_item(content, 'gallery-visible-tribeca-rooftop', actual_pos, new_item)
    if ok:
        content = new_content
        offset += 1
        fixes_applied.append(f'FIX #2: {fname} inserted after item {actual_pos} in Tribeca gallery')
    else:
        print(f'ERROR: Could not insert {fname} at position {actual_pos}')

# ─────────────────────────────────────────────────────────────
# FINAL CHECKS
# ─────────────────────────────────────────────────────────────
assert '</html>' in content, "ERROR: HTML truncated!"

# Count final gallery items
import re as re2
def count_gallery_items(html, section_id):
    start = html.find(f'id="{section_id}"')
    if start == -1:
        return -1
    # Find next section end
    end = html.find('</section>', start)
    block = html[start:end] if end != -1 else html[start:start+20000]
    return len(re2.findall(r'<div class="gallery-item">', block))

tribeca_count = count_gallery_items(content, 'gallery-visible-tribeca-rooftop')
knox_count = count_gallery_items(content, 'gallery-visible-knox-day')

print(f'\nFixes applied ({len(fixes_applied)}):')
for f in fixes_applied:
    print(f'  ✓ {f}')

print(f'\nGallery counts:')
print(f'  Tribeca: {tribeca_count} (target: 15)')
print(f'  Knox Day: {knox_count} (target: 12)')
print(f'\nFile: {original_len} -> {len(content)} chars ({len(content)-original_len:+d})')

with open('index.html', 'w') as f:
    f.write(content)
print('Saved.')
