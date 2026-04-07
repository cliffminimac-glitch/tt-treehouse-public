import re

with open('index.html') as f:
    content = f.read()

fixes = []

# ─────────────────────────────────────────────────────────────
# FIX #1 — Shift curate photo to show more crowd at bottom
# ─────────────────────────────────────────────────────────────
old_curate = """.curate-section .dj-photo { width:100%; height:55vh; object-fit:cover; object-position:center; display:block; max-height:none; }"""
new_curate = """/* REMOVED R15: object-position:center was cropping the crowd at the bottom */
/* ROUND 15 FIX #1 — shift curate photo down to show crowd at bottom while keeping sky at top */
.curate-section .dj-photo { width:100%; height:55vh; object-fit:cover; object-position:center 70%; display:block; max-height:none; }"""

if old_curate in content:
    content = content.replace(old_curate, new_curate)
    fixes.append('FIX #1: curate object-position changed to center 70%')
else:
    print('ERROR: curate CSS rule not found exactly')
    # Try to find it
    idx = content.find('dj-photo')
    print(f'  dj-photo context: {content[idx-20:idx+120]}')

# ─────────────────────────────────────────────────────────────
# Helper: gallery item markup
# ─────────────────────────────────────────────────────────────
def make_item(src, alt="treehouse. event photo", eager=False):
    loading = 'eager' if eager else 'lazy'
    return f'<div class="gallery-item"><img src="{src}" alt="{alt}" loading="{loading}" onerror="this.onerror=null;this.parentNode.style.display=\'none\'"></div>'

# ─────────────────────────────────────────────────────────────
# FIX #2 — Add 2 photos to Tribeca gallery
# ─────────────────────────────────────────────────────────────
# Find tribeca gallery-visible block
tribeca_start = content.find('id="gallery-visible-tribeca-rooftop"')
tribeca_section_end = content.find('</section>', tribeca_start)
tribeca_block = content[tribeca_start:tribeca_section_end]

# Get all gallery items
items = list(re.finditer(r'<div class="gallery-item">.*?</div>', tribeca_block, re.DOTALL))
print(f'Tribeca items found: {len(items)}')

if len(items) >= 10:
    # Insert tribeca-new-08 after position 4 (0-indexed: after item[4])
    # Insert tribeca-new-09 after position 10 (0-indexed: after item[10])
    # Work backwards to avoid offset issues
    
    new_08 = f'\n    <!-- ROUND 15 FIX #2 — tribeca-new-08 -->\n    {make_item("/img/tribeca-new-08.jpg")}'
    new_09 = f'\n    <!-- ROUND 15 FIX #2 — tribeca-new-09 -->\n    {make_item("/img/tribeca-new-09.jpg")}'
    
    # Insert after item[10] first (higher index, so offset doesn't affect item[4])
    insert_pos_09 = tribeca_start + items[10].end()
    content = content[:insert_pos_09] + new_09 + content[insert_pos_09:]
    
    # Re-find items after insertion
    tribeca_block2 = content[tribeca_start:content.find('</section>', tribeca_start)]
    items2 = list(re.finditer(r'<div class="gallery-item">.*?</div>', tribeca_block2, re.DOTALL))
    
    # Insert after item[4]
    insert_pos_08 = tribeca_start + items2[4].end()
    content = content[:insert_pos_08] + new_08 + content[insert_pos_08:]
    
    fixes.append('FIX #2: tribeca-new-08 at pos 5, tribeca-new-09 at pos 12')
else:
    print(f'ERROR: Not enough Tribeca items ({len(items)})')

# ─────────────────────────────────────────────────────────────
# FIX #3a — Swap SoHo photos 1 and 2
# ─────────────────────────────────────────────────────────────
soho_start = content.find('id="gallery-visible-soho-soiree"')
soho_section_end = content.find('</section>', soho_start)
soho_block = content[soho_start:soho_section_end]

soho_items = list(re.finditer(r'<div class="gallery-item">.*?</div>', soho_block, re.DOTALL))
print(f'SoHo items found: {len(soho_items)}')

if len(soho_items) >= 2:
    item1 = soho_items[0].group()
    item2 = soho_items[1].group()
    
    # Get absolute positions
    abs_start1 = soho_start + soho_items[0].start()
    abs_end1 = soho_start + soho_items[0].end()
    abs_start2 = soho_start + soho_items[1].start()
    abs_end2 = soho_start + soho_items[1].end()
    
    # Swap: replace item1 with item2 and item2 with item1
    # Work from end to start to preserve offsets
    content = content[:abs_start2] + f'<!-- ROUND 15 FIX #3a — swapped: was photo 1, now photo 2 -->\n    ' + item1 + content[abs_end2:]
    # Re-find item1 position (it's still at abs_start1)
    content = content[:abs_start1] + f'<!-- ROUND 15 FIX #3a — swapped: was photo 2, now photo 1 -->\n    ' + item2 + content[abs_end1:]
    
    fixes.append('FIX #3a: SoHo photos 1 and 2 swapped')
else:
    print(f'ERROR: Not enough SoHo items ({len(soho_items)})')

# ─────────────────────────────────────────────────────────────
# FIX #3b — Add 3 new SoHo photos distributed throughout
# ─────────────────────────────────────────────────────────────
soho_start = content.find('id="gallery-visible-soho-soiree"')
soho_section_end = content.find('</section>', soho_start)
soho_block = content[soho_start:soho_section_end]
soho_items = list(re.finditer(r'<div class="gallery-item">.*?</div>', soho_block, re.DOTALL))
print(f'SoHo items after swap: {len(soho_items)}')

if len(soho_items) >= 15:
    new_s08 = f'\n    <!-- ROUND 15 FIX #3b — soho-new-08 -->\n    {make_item("/img/soho-new-08.jpg")}'
    new_s09 = f'\n    <!-- ROUND 15 FIX #3b — soho-new-09 -->\n    {make_item("/img/soho-new-09.jpg")}'
    new_s10 = f'\n    <!-- ROUND 15 FIX #3b — soho-new-10 -->\n    {make_item("/img/soho-new-10.jpg")}'
    
    # Insert at positions 15, 10, 5 (backwards)
    ins15 = soho_start + soho_items[14].end()
    content = content[:ins15] + new_s10 + content[ins15:]
    
    soho_block2 = content[soho_start:content.find('</section>', soho_start)]
    soho_items2 = list(re.finditer(r'<div class="gallery-item">.*?</div>', soho_block2, re.DOTALL))
    ins10 = soho_start + soho_items2[9].end()
    content = content[:ins10] + new_s09 + content[ins10:]
    
    soho_block3 = content[soho_start:content.find('</section>', soho_start)]
    soho_items3 = list(re.finditer(r'<div class="gallery-item">.*?</div>', soho_block3, re.DOTALL))
    ins5 = soho_start + soho_items3[4].end()
    content = content[:ins5] + new_s08 + content[ins5:]
    
    fixes.append('FIX #3b: soho-new-08 at pos 5, soho-new-09 at pos 11, soho-new-10 at pos 17')
else:
    print(f'ERROR: Not enough SoHo items for 3b ({len(soho_items)})')

# ─────────────────────────────────────────────────────────────
# FIX #4 — Add 3 photos to Christmas gallery
# ─────────────────────────────────────────────────────────────
xmas_start = content.find('id="gallery-visible-christmas-nyc"')
xmas_section_end = content.find('</section>', xmas_start)
xmas_block = content[xmas_start:xmas_section_end]
xmas_items = list(re.finditer(r'<div class="gallery-item">.*?</div>', xmas_block, re.DOTALL))
print(f'Christmas items found: {len(xmas_items)}')

if len(xmas_items) >= 13:
    new_x02 = f'\n    <!-- ROUND 15 FIX #4 — xmas-new-02 near top for visual impact -->\n    {make_item("/img/xmas-new-02.jpg")}'
    new_x03 = f'\n    <!-- ROUND 15 FIX #4 — xmas-new-03 mid gallery -->\n    {make_item("/img/xmas-new-03.jpg")}'
    new_x04 = f'\n    <!-- ROUND 15 FIX #4 — xmas-new-04 near end -->\n    {make_item("/img/xmas-new-04.jpg")}'
    
    # Insert at positions 13, 8, 2 (backwards)
    ins13 = xmas_start + xmas_items[12].end()
    content = content[:ins13] + new_x04 + content[ins13:]
    
    xmas_block2 = content[xmas_start:content.find('</section>', xmas_start)]
    xmas_items2 = list(re.finditer(r'<div class="gallery-item">.*?</div>', xmas_block2, re.DOTALL))
    ins8 = xmas_start + xmas_items2[7].end()
    content = content[:ins8] + new_x03 + content[ins8:]
    
    xmas_block3 = content[xmas_start:content.find('</section>', xmas_start)]
    xmas_items3 = list(re.finditer(r'<div class="gallery-item">.*?</div>', xmas_block3, re.DOTALL))
    ins2 = xmas_start + xmas_items3[1].end()
    content = content[:ins2] + new_x02 + content[ins2:]
    
    fixes.append('FIX #4: xmas-new-02 at pos 2, xmas-new-03 at pos 9, xmas-new-04 at pos 15')
else:
    print(f'ERROR: Not enough Christmas items ({len(xmas_items)})')

# ─────────────────────────────────────────────────────────────
# VERIFY
# ─────────────────────────────────────────────────────────────
assert '</html>' in content, 'ERROR: HTML truncated!'
assert 'object-position:center 70%' in content, 'ERROR: curate fix missing!'
assert 'tribeca-new-08' in content, 'ERROR: tribeca-new-08 missing!'
assert 'tribeca-new-09' in content, 'ERROR: tribeca-new-09 missing!'
assert 'soho-new-08' in content, 'ERROR: soho-new-08 missing!'
assert 'xmas-new-02' in content, 'ERROR: xmas-new-02 missing!'

# Final counts
def count_gallery(section_id):
    start = content.find(f'id="{section_id}"')
    end = content.find('</section>', start)
    block = content[start:end]
    return len(re.findall(r'<div class="gallery-item">', block))

t = count_gallery('gallery-visible-tribeca-rooftop')
s = count_gallery('gallery-visible-soho-soiree')
x = count_gallery('gallery-visible-christmas-nyc')
print(f'\nFinal gallery counts: Tribeca={t}, SoHo={s}, Christmas={x}')
print(f'Expected:             Tribeca=17, SoHo=22, Christmas=19')

print(f'\nFixes applied ({len(fixes)}):')
for f in fixes:
    print(f'  ✓ {f}')

with open('index.html', 'w') as f:
    f.write(content)
print('Saved.')
