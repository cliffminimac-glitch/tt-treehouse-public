#!/usr/bin/env python3
"""
Patch index.html: replace all 6 gallery-visible + gallery-collapsed sections
with perfect 4x3 rectangle grids (12 visible, rest collapsed in multiples of 4).
"""

import re

BASE = "/home/ubuntu/treehouse-audit"

def gi(path, alt):
    return f'    <div class="gallery-item"><img src="/{path}" alt="{alt}" loading="lazy" onerror="this.onerror=null;this.parentNode.style.display=\'none\'"></div>'

galleries = [
    {
        "id": "tribeca-rooftop",
        "visible": [
            ("img/gallery/tribeca-rooftop/tribeca-005.jpg", "DJ set, Manhattan skyline at golden hour"),
            ("img/gallery/tribeca-rooftop/tribeca-001.jpg", "Pumpkins and disco balls, Tribeca rooftop"),
            ("img/gallery/tribeca-rooftop/tribeca-007.jpg", "Crowd dancing at sunset"),
            ("img/gallery/tribeca-rooftop/tribeca-003.jpg", "Group of friends on the rooftop"),
            ("img/gallery/tribeca-rooftop/tribeca-009.jpg", "Candy bar with NYC skyline"),
            ("img/gallery/tribeca-rooftop/tribeca-011.jpg", "Rooftop crowd at dusk"),
            ("img/gallery/tribeca-rooftop/tribeca-013.jpg", "Friends with drinks, skyline behind"),
            ("img/gallery/tribeca-rooftop/tribeca-015.jpg", "Crowd shot, Tribeca rooftop"),
            ("img/gallery/tribeca-rooftop/tribeca-017.jpg", "Group photo at treehouse. Tribeca"),
            ("img/gallery/tribeca-rooftop/tribeca-019.jpg", "Rooftop view, city lights"),
            ("img/gallery/tribeca-rooftop/tribeca-021.jpg", "DJ booth, crowd hands up"),
            ("img/gallery/tribeca-rooftop/tribeca-023.jpg", "Golden hour, rooftop crowd"),
        ],
        "collapsed_nums": list(range(24, 51)),
        "pfx": "img/gallery/tribeca-rooftop/tribeca-",
        "label": "Tribeca Rooftop",
    },
    {
        "id": "soho-soiree",
        "visible": [
            ("img/gallery/soho-soiree/soho-006.jpg", "Friends on SoHo rooftop, late spring"),
            ("img/gallery/soho-soiree/soho-002.jpg", "Three guys, NYC skyline and One WTC"),
            ("img/gallery/soho-soiree/soho-004.jpg", "Knicks jersey energy on the rooftop"),
            ("img/gallery/soho-soiree/soho-009.jpg", "Champagne on ice, SoHo Soiree"),
            ("img/gallery/soho-soiree/soho-011.jpg", "Women laughing on rooftop"),
            ("img/gallery/soho-soiree/soho-013.jpg", "Crowd at the bar"),
            ("img/gallery/soho-soiree/soho-015.jpg", "Group photo, SoHo rooftop"),
            ("img/gallery/soho-soiree/soho-017.jpg", "Skyline view at dusk"),
            ("img/gallery/soho-soiree/soho-019.jpg", "Rooftop crowd, SoHo"),
            ("img/gallery/soho-soiree/soho-021.jpg", "Friends with drinks"),
            ("img/gallery/soho-soiree/soho-023.jpg", "DJ set, SoHo Soiree"),
            ("img/gallery/soho-soiree/soho-025.jpg", "Golden hour, SoHo rooftop"),
        ],
        "collapsed_nums": list(range(26, 51)),
        "pfx": "img/gallery/soho-soiree/soho-",
        "label": "SoHo Soiree",
    },
    {
        "id": "christmas-nyc",
        "visible": [
            ("img/gallery/christmas-nyc/xmas-003.jpg", "Christmas party, festive crowd"),
            ("img/gallery/christmas-nyc/xmas-001.jpg", "Holiday costumes, treehouse. Christmas"),
            ("img/gallery/christmas-nyc/xmas-005.jpg", "Cocktails and costumes"),
            ("img/gallery/christmas-nyc/xmas-007.jpg", "Christmas crowd, NYC"),
            ("img/gallery/christmas-nyc/xmas-009.jpg", "Holiday party energy"),
            ("img/gallery/christmas-nyc/xmas-011.jpg", "Friends at Christmas treehouse."),
            ("img/gallery/christmas-nyc/xmas-013.jpg", "Festive drinks, holiday party"),
            ("img/gallery/christmas-nyc/xmas-015.jpg", "Christmas night out, NYC"),
            ("img/gallery/christmas-nyc/xmas-017.jpg", "Holiday crowd, open bar"),
            ("img/gallery/christmas-nyc/xmas-019.jpg", "Christmas party group shot"),
            ("img/gallery/christmas-nyc/xmas-021.jpg", "Festive rooftop, December NYC"),
            ("img/gallery/christmas-nyc/xmas-023.jpg", "Holiday vibes, treehouse."),
        ],
        "collapsed_nums": list(range(24, 49)),
        "pfx": "img/gallery/christmas-nyc/xmas-",
        "label": "Christmas NYC",
    },
    {
        "id": "dinner-parties",
        "visible": [
            ("img/gallery/dinner-parties/dinner-001.jpg", "Intimate dinner, treehouse. NYC"),
            ("img/gallery/dinner-parties/dinner-002.jpg", "Table setting, dinner party"),
            ("img/gallery/dinner-parties/dinner-003.jpg", "Friends at dinner, NYC"),
            ("img/gallery/dinner-parties/dinner-004.jpg", "Dinner crowd, candlelit"),
            ("img/gallery/dinner-parties/dinner-005.jpg", "Cocktails at dinner"),
            ("img/gallery/dinner-parties/dinner-006.jpg", "Group dinner, treehouse."),
            ("img/gallery/dinner-parties/dinner-007.jpg", "Dinner party energy"),
            ("img/gallery/dinner-parties/dinner-008.jpg", "Table full of friends"),
            ("img/gallery/dinner-parties/dinner-009.jpg", "Dinner night out, NYC"),
            ("img/gallery/dinner-parties/dinner-010.jpg", "Intimate dinner setting"),
            ("img/gallery/dinner-parties/dinner-011.jpg", "Friends laughing at dinner"),
            ("img/gallery/dinner-parties/dinner-012.jpg", "Dinner party crowd"),
        ],
        "collapsed_nums": list(range(13, 32)),
        "pfx": "img/gallery/dinner-parties/dinner-",
        "label": "Dinner Parties",
    },
    {
        "id": "knox-day",
        "visible": [
            ("img/gallery/knox-day/knox-001.jpg", "Knox Day, daytime rooftop party"),
            ("img/gallery/knox-day/knox-002.jpg", "Sunlit crowd, Knox Day"),
            ("img/gallery/knox-day/knox-003.jpg", "Friends in the sun, Knox Day"),
            ("img/gallery/knox-day/knox-004.jpg", "Daytime drinks, NYC rooftop"),
            ("img/gallery/knox-day/knox-005.jpg", "Knox Day crowd"),
            ("img/gallery/knox-day/knox-006.jpg", "Outdoor party, Knox Day"),
            ("img/gallery/knox-day/knox-007.jpg", "Group shot, Knox Day"),
            ("img/gallery/knox-day/knox-008.jpg", "Sunlit rooftop, Knox Day"),
            ("img/gallery/knox-day/knox-009.jpg", "Daytime party energy"),
            ("img/gallery/knox-day/knox-010.jpg", "Knox Day vibes"),
            ("img/gallery/knox-day/knox-011.jpg", "Friends at Knox Day"),
            ("img/gallery/knox-day/knox-012.jpg", "Rooftop crowd, Knox Day"),
        ],
        "collapsed_nums": list(range(13, 21)),
        "pfx": "img/gallery/knox-day/knox-",
        "label": "Knox Day",
    },
    {
        "id": "west-village",
        "visible": [
            ("img/gallery/west-village/westvillage-001.jpg", "West Village night out"),
            ("img/gallery/west-village/westvillage-003.jpg", "Crowd at West Village treehouse."),
            ("img/gallery/west-village/westvillage-005.jpg", "Friends, West Village"),
            ("img/gallery/west-village/westvillage-007.jpg", "Night crowd, West Village"),
            ("img/gallery/west-village/westvillage-009.jpg", "West Village party energy"),
            ("img/gallery/west-village/westvillage-011.jpg", "Group shot, West Village"),
            ("img/gallery/west-village/westvillage-013.jpg", "West Village rooftop"),
            ("img/gallery/west-village/westvillage-015.jpg", "Night out, West Village"),
            ("img/gallery/west-village/westvillage-017.jpg", "Friends at treehouse. West Village"),
            ("img/gallery/west-village/westvillage-019.jpg", "West Village crowd"),
            ("img/gallery/west-village/westvillage-021.jpg", "Night vibes, West Village"),
            ("img/gallery/west-village/westvillage-023.jpg", "West Village, treehouse."),
        ],
        "collapsed_nums": list(range(24, 51)),
        "pfx": "img/gallery/west-village/westvillage-",
        "label": "West Village",
    },
]

def build_visible(g):
    gid = g['id']
    lines = ['  <div class="gallery-visible" id="gallery-visible-' + gid + '">']
    for path, alt in g['visible']:
        lines.append(gi(path, alt))
    lines.append('  </div>')
    return '\n'.join(lines)

def build_collapsed(g):
    gid = g['id']
    nums = g['collapsed_nums']
    trim = len(nums) - (len(nums) % 4)
    nums = nums[:trim]
    lines = ['  <div class="gallery-collapsed" id="gallery-collapsed-' + gid + '">']
    for n in nums:
        path = g['pfx'] + '%03d' % n + '.jpg'
        alt = 'treehouse. ' + g['label'] + ' photo ' + str(n)
        lines.append(gi(path, alt))
    lines.append('  </div>')
    total = 12 + len(nums)
    btn = '  <div style="text-align:center;padding:1.5rem 0;">\n    <button class="gallery-toggle btn btn-s" data-target="gallery-collapsed-' + gid + '" data-count="' + str(len(nums)) + '" style="font-size:0.65rem;">view all ' + str(total) + ' photos</button>\n  </div>'
    return '\n'.join(lines), btn

# Read the HTML
with open(BASE + '/index.html', 'r') as f:
    html = f.read()

for g in galleries:
    gid = g['id']
    
    # Build replacement blocks
    new_visible = build_visible(g)
    new_collapsed, new_btn = build_collapsed(g)
    
    # Replace gallery-visible block
    vis_pattern = r'  <div class="gallery-visible" id="gallery-visible-' + re.escape(gid) + r'">[^<]*(?:<div[^>]*>.*?</div>\s*)*</div>'
    html = re.sub(vis_pattern, new_visible, html, flags=re.DOTALL)
    
    # Replace gallery-collapsed block
    col_pattern = r'  <div class="gallery-collapsed" id="gallery-collapsed-' + re.escape(gid) + r'">[^<]*(?:<div[^>]*>.*?</div>\s*)*</div>'
    html = re.sub(col_pattern, new_collapsed, html, flags=re.DOTALL)
    
    # Replace the toggle button div
    btn_pattern = r'  <div style="text-align:center;padding:1\.5rem 0;">\s*<button class="gallery-toggle btn btn-s" data-target="gallery-collapsed-' + re.escape(gid) + r'"[^>]*>[^<]*</button>\s*</div>'
    html = re.sub(btn_pattern, new_btn, html, flags=re.DOTALL)
    
    print(f"Patched: {gid}")

with open(BASE + '/index.html', 'w') as f:
    f.write(html)

print("Done! index.html updated.")
