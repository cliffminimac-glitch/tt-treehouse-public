import re

with open('index.html') as f:
    content = f.read()

fixes = []

# ─────────────────────────────────────────────────────────────
# FIX #1 — Rename Knox Day to Party on Perry St
# ─────────────────────────────────────────────────────────────

# 1a. Marquee ticker text (2 instances)
old_marquee = '<span class="marquee-item">Knox Day<span class="marquee-dot"></span></span>'
new_marquee = '<!-- ROUND 16 FIX #1 — renamed Knox Day to Party on Perry St --><span class="marquee-item">Party on Perry St<span class="marquee-dot"></span></span>'
count = content.count(old_marquee)
content = content.replace(old_marquee, new_marquee)
fixes.append(f'FIX #1a: marquee "Knox Day" → "Party on Perry St" ({count} instances)')

# 1b. Section id
old_section_id = '<section class="dk ev-section grain" id="knox-day">'
new_section_id = '<!-- ROUND 16 FIX #1 — section id renamed from knox-day to perry-st -->\n        <section class="dk ev-section grain" id="perry-st">'
if old_section_id in content:
    content = content.replace(old_section_id, new_section_id)
    fixes.append('FIX #1b: section id="knox-day" → id="perry-st"')
else:
    print(f'ERROR: section id not found exactly')

# 1c. Gallery heading h2
old_h2 = 'KNOX DAY</h2>'
new_h2 = '<!-- ROUND 16 FIX #1 — heading renamed -->PARTY ON PERRY ST</h2>'
if old_h2 in content:
    content = content.replace(old_h2, new_h2)
    fixes.append('FIX #1c: h2 "KNOX DAY" → "PARTY ON PERRY ST"')
else:
    print(f'ERROR: h2 KNOX DAY not found')

# 1d. Gallery visible div id
old_gv_id = 'id="gallery-visible-knox-day"'
new_gv_id = '<!-- ROUND 16 FIX #1 — gallery id renamed -->id="gallery-visible-perry-st"'
if old_gv_id in content:
    content = content.replace(old_gv_id, new_gv_id)
    fixes.append('FIX #1d: gallery-visible id "knox-day" → "perry-st"')
else:
    print(f'ERROR: gallery-visible-knox-day id not found')

# 1e. Alt text on knox-new-01 and knox-new-02
old_alt = 'alt="Knox Day treehouse. NYC"'
new_alt = 'alt="Party on Perry St treehouse. NYC"'
count_alt = content.count(old_alt)
content = content.replace(old_alt, new_alt)
fixes.append(f'FIX #1e: alt text "Knox Day" → "Party on Perry St" ({count_alt} instances)')

# ─────────────────────────────────────────────────────────────
# FIX #2 — Add 3 photos to Perry St gallery
# ─────────────────────────────────────────────────────────────

def make_item(src, alt="Party on Perry St treehouse. NYC"):
    return f'<div class="gallery-item"><img src="{src}" alt="{alt}" loading="lazy" onerror="this.onerror=null;this.parentNode.style.display=\'none\'"></div>'

# Find the gallery block using the new ID
perry_start = content.find('id="gallery-visible-perry-st"')
perry_section_end = content.find('</section>', perry_start)
perry_block = content[perry_start:perry_section_end]

items = list(re.finditer(r'<div class="gallery-item">.*?</div>', perry_block, re.DOTALL))
print(f'Perry St gallery items found: {len(items)}')

if len(items) >= 10:
    new_p01 = f'\n    <!-- ROUND 16 FIX #2 — perry-new-01 at position 4 -->\n    {make_item("/img/perry-new-01.jpg")}'
    new_p02 = f'\n    <!-- ROUND 16 FIX #2 — perry-new-02 at position 8 -->\n    {make_item("/img/perry-new-02.jpg")}'
    new_p03 = f'\n    <!-- ROUND 16 FIX #2 — perry-new-03 near end -->\n    {make_item("/img/perry-new-03.jpg")}'

    # Insert perry-new-03 after item[11] (near end), then perry-new-02 after item[7], then perry-new-01 after item[3]
    # Work backwards to preserve offsets

    # After item[11] (position 12)
    ins12 = perry_start + items[11].end()
    content = content[:ins12] + new_p03 + content[ins12:]

    # Re-find items
    perry_block2 = content[perry_start:content.find('</section>', perry_start)]
    items2 = list(re.finditer(r'<div class="gallery-item">.*?</div>', perry_block2, re.DOTALL))

    # After item[7] (position 8)
    ins8 = perry_start + items2[7].end()
    content = content[:ins8] + new_p02 + content[ins8:]

    # Re-find items
    perry_block3 = content[perry_start:content.find('</section>', perry_start)]
    items3 = list(re.finditer(r'<div class="gallery-item">.*?</div>', perry_block3, re.DOTALL))

    # After item[3] (position 4)
    ins4 = perry_start + items3[3].end()
    content = content[:ins4] + new_p01 + content[ins4:]

    fixes.append('FIX #2: perry-new-01 at pos 4, perry-new-02 at pos 9, perry-new-03 at pos 13')
else:
    print(f'ERROR: Not enough Perry St items ({len(items)})')

# ─────────────────────────────────────────────────────────────
# VERIFY
# ─────────────────────────────────────────────────────────────
assert '</html>' in content, 'ERROR: HTML truncated!'
assert 'PARTY ON PERRY ST' in content, 'ERROR: heading rename missing!'
assert 'id="perry-st"' in content, 'ERROR: section id rename missing!'
assert 'gallery-visible-perry-st' in content, 'ERROR: gallery id rename missing!'
assert 'perry-new-01' in content, 'ERROR: perry-new-01 missing!'
assert 'perry-new-02' in content, 'ERROR: perry-new-02 missing!'
assert 'perry-new-03' in content, 'ERROR: perry-new-03 missing!'
assert 'KNOX DAY</h2>' not in content, 'ERROR: old h2 still present!'

# Final count
perry_start2 = content.find('id="gallery-visible-perry-st"')
perry_end2 = content.find('</section>', perry_start2)
perry_block_final = content[perry_start2:perry_end2]
final_count = len(re.findall(r'<div class="gallery-item">', perry_block_final))
print(f'Final Perry St gallery count: {final_count} (expected 15)')

print(f'\nFixes applied ({len(fixes)}):')
for f in fixes:
    print(f'  ✓ {f}')

with open('index.html', 'w') as f:
    f.write(content)
print('Saved.')
