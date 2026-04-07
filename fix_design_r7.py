#!/usr/bin/env python3
"""Round 7 Design Fixes — eager loading + all-dark sections"""

import re

with open('index.html', 'r') as f:
    html = f.read()

original_len = len(html)
fixes = []

# ─────────────────────────────────────────────────────────────
# DESIGN FIX 1: Set first 8 Tribeca photos to loading="eager"
# Tribeca gallery items are in the first gallery section
# ─────────────────────────────────────────────────────────────
# Find the tribeca section and change the first 8 gallery-item img tags from lazy to eager
tribeca_start = html.find('id="tribeca-rooftop"')
if tribeca_start == -1:
    tribeca_start = html.find('id="tribeca"')

# Find the next section after tribeca
tribeca_section_end = html.find('<section', tribeca_start + 100)

tribeca_block = html[tribeca_start:tribeca_section_end]

# Replace first 8 loading="lazy" with loading="eager" in tribeca block
count = 0
new_tribeca_block = tribeca_block
for _ in range(8):
    pos = new_tribeca_block.find('loading="lazy"')
    if pos == -1:
        break
    new_tribeca_block = new_tribeca_block[:pos] + 'loading="eager"' + new_tribeca_block[pos+14:]
    count += 1

html = html[:tribeca_start] + new_tribeca_block + html[tribeca_section_end:]
fixes.append(f"DESIGN 1: {count} Tribeca photos set to loading=eager")

# ─────────────────────────────────────────────────────────────
# DESIGN FIX 2: Make all gallery sections dark (remove lt class from christmas and knox)
# ─────────────────────────────────────────────────────────────
# Christmas NYC: class="lt ev-section" -> class="dk ev-section grain"
old_christmas = '<section class="lt ev-section" id="christmas-nyc">'
new_christmas = '<section class="dk ev-section grain" id="christmas-nyc">'
if old_christmas in html:
    html = html.replace(old_christmas, new_christmas)
    fixes.append("DESIGN 2a: Christmas NYC section -> dark (dk grain)")
else:
    print("WARNING: christmas section class not found")

# Knox Day: class="lt ev-section" -> class="dk ev-section grain"
old_knox = '<section class="lt ev-section" id="knox-day">'
new_knox = '<section class="dk ev-section grain" id="knox-day">'
if old_knox in html:
    html = html.replace(old_knox, new_knox)
    fixes.append("DESIGN 2b: Knox Day section -> dark (dk grain)")
else:
    print("WARNING: knox section class not found")

# ─────────────────────────────────────────────────────────────
# DESIGN FIX 3: Also set first 8 SoHo photos to eager
# ─────────────────────────────────────────────────────────────
soho_start = html.find('id="soho-soiree"')
soho_section_end = html.find('<section', soho_start + 100)
soho_block = html[soho_start:soho_section_end]

count = 0
new_soho_block = soho_block
for _ in range(8):
    pos = new_soho_block.find('loading="lazy"')
    if pos == -1:
        break
    new_soho_block = new_soho_block[:pos] + 'loading="eager"' + new_soho_block[pos+14:]
    count += 1

html = html[:soho_start] + new_soho_block + html[soho_section_end:]
fixes.append(f"DESIGN 3: {count} SoHo photos set to loading=eager")

with open('index.html', 'w') as f:
    f.write(html)

print(f"Applied {len(fixes)} design fixes:")
for f in fixes:
    print(f"  ✓ {f}")
print(f"\nFile size: {original_len} -> {len(html)} chars")
