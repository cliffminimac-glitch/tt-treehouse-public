#!/usr/bin/env python3
"""
Generate perfect 4-column rectangle gallery HTML for all 6 treehouse. events.
Default visible: 12 photos (4x3 grid). Collapsed: remaining photos in multiples of 4.
"""

import os, re

BASE = "/home/ubuntu/treehouse-audit"

galleries = [
    {
        "id": "tribeca-rooftop",
        "folder": "gallery/tribeca-rooftop",
        "prefix": "tribeca-",
        "total": 50,
        # Best 12 for visible: variety of crowd, DJ, skyline, branding
        "visible": [
            ("gallery/tribeca-rooftop/tribeca-005.jpg", "DJ set, Manhattan skyline at golden hour"),
            ("gallery/tribeca-rooftop/tribeca-001.jpg", "Pumpkins and disco balls, Tribeca rooftop"),
            ("gallery/tribeca-rooftop/tribeca-007.jpg", "Crowd dancing at sunset"),
            ("gallery/tribeca-rooftop/tribeca-003.jpg", "Group of friends on the rooftop"),
            ("gallery/tribeca-rooftop/tribeca-009.jpg", "Candy bar with NYC skyline"),
            ("gallery/tribeca-rooftop/tribeca-011.jpg", "Rooftop crowd at dusk"),
            ("gallery/tribeca-rooftop/tribeca-013.jpg", "Friends with drinks, skyline behind"),
            ("gallery/tribeca-rooftop/tribeca-015.jpg", "Crowd shot, Tribeca rooftop"),
            ("gallery/tribeca-rooftop/tribeca-017.jpg", "Group photo at treehouse. Tribeca"),
            ("gallery/tribeca-rooftop/tribeca-019.jpg", "Rooftop view, city lights"),
            ("gallery/tribeca-rooftop/tribeca-021.jpg", "DJ booth, crowd hands up"),
            ("gallery/tribeca-rooftop/tribeca-023.jpg", "Golden hour, rooftop crowd"),
        ],
        # Collapsed: next 36 in multiples of 4 = 36 photos (photos 024-050 minus 2 = 36)
        "collapsed_range": list(range(24, 51)),  # 27 photos, trim to 24 (multiple of 4)
    },
    {
        "id": "soho-soiree",
        "folder": "gallery/soho-soiree",
        "prefix": "soho-",
        "total": 50,
        "visible": [
            ("gallery/soho-soiree/soho-006.jpg", "Friends on SoHo rooftop, late spring"),
            ("gallery/soho-soiree/soho-002.jpg", "Three guys, NYC skyline and One WTC"),
            ("gallery/soho-soiree/soho-004.jpg", "Knicks jersey energy on the rooftop"),
            ("gallery/soho-soiree/soho-009.jpg", "Champagne on ice, SoHo Soiree"),
            ("gallery/soho-soiree/soho-011.jpg", "Women laughing on rooftop"),
            ("gallery/soho-soiree/soho-013.jpg", "Crowd at the bar"),
            ("gallery/soho-soiree/soho-015.jpg", "Group photo, SoHo rooftop"),
            ("gallery/soho-soiree/soho-017.jpg", "Skyline view at dusk"),
            ("gallery/soho-soiree/soho-019.jpg", "Rooftop crowd, SoHo"),
            ("gallery/soho-soiree/soho-021.jpg", "Friends with drinks"),
            ("gallery/soho-soiree/soho-023.jpg", "DJ set, SoHo Soiree"),
            ("gallery/soho-soiree/soho-025.jpg", "Golden hour, SoHo rooftop"),
        ],
        "collapsed_range": list(range(26, 51)),  # 25 photos, trim to 24
    },
    {
        "id": "christmas-nyc",
        "folder": "gallery/christmas-nyc",
        "prefix": "xmas-",
        "total": 48,
        "visible": [
            ("gallery/christmas-nyc/xmas-003.jpg", "Christmas party, festive crowd"),
            ("gallery/christmas-nyc/xmas-001.jpg", "Holiday costumes, treehouse. Christmas"),
            ("gallery/christmas-nyc/xmas-005.jpg", "Cocktails and costumes"),
            ("gallery/christmas-nyc/xmas-007.jpg", "Christmas crowd, NYC"),
            ("gallery/christmas-nyc/xmas-009.jpg", "Holiday party energy"),
            ("gallery/christmas-nyc/xmas-011.jpg", "Friends at Christmas treehouse."),
            ("gallery/christmas-nyc/xmas-013.jpg", "Festive drinks, holiday party"),
            ("gallery/christmas-nyc/xmas-015.jpg", "Christmas night out, NYC"),
            ("gallery/christmas-nyc/xmas-017.jpg", "Holiday crowd, open bar"),
            ("gallery/christmas-nyc/xmas-019.jpg", "Christmas party group shot"),
            ("gallery/christmas-nyc/xmas-021.jpg", "Festive rooftop, December NYC"),
            ("gallery/christmas-nyc/xmas-023.jpg", "Holiday vibes, treehouse."),
        ],
        "collapsed_range": list(range(24, 49)),  # 25 photos, trim to 24
    },
    {
        "id": "dinner-parties",
        "folder": "gallery/dinner-parties",
        "prefix": "dinner-",
        "total": 31,
        "visible": [
            ("gallery/dinner-parties/dinner-001.jpg", "Intimate dinner, treehouse. NYC"),
            ("gallery/dinner-parties/dinner-002.jpg", "Table setting, dinner party"),
            ("gallery/dinner-parties/dinner-003.jpg", "Friends at dinner, NYC"),
            ("gallery/dinner-parties/dinner-004.jpg", "Dinner crowd, candlelit"),
            ("gallery/dinner-parties/dinner-005.jpg", "Cocktails at dinner"),
            ("gallery/dinner-parties/dinner-006.jpg", "Group dinner, treehouse."),
            ("gallery/dinner-parties/dinner-007.jpg", "Dinner party energy"),
            ("gallery/dinner-parties/dinner-008.jpg", "Table full of friends"),
            ("gallery/dinner-parties/dinner-009.jpg", "Dinner night out, NYC"),
            ("gallery/dinner-parties/dinner-010.jpg", "Intimate dinner setting"),
            ("gallery/dinner-parties/dinner-011.jpg", "Friends laughing at dinner"),
            ("gallery/dinner-parties/dinner-012.jpg", "Dinner party crowd"),
        ],
        "collapsed_range": list(range(13, 32)),  # 19 photos, trim to 16 (multiple of 4)
    },
    {
        "id": "knox-day",
        "folder": "gallery/knox-day",
        "prefix": "knox-",
        "total": 20,
        "visible": [
            ("gallery/knox-day/knox-001.jpg", "Knox Day, daytime rooftop party"),
            ("gallery/knox-day/knox-002.jpg", "Sunlit crowd, Knox Day"),
            ("gallery/knox-day/knox-003.jpg", "Friends in the sun, Knox Day"),
            ("gallery/knox-day/knox-004.jpg", "Daytime drinks, NYC rooftop"),
            ("gallery/knox-day/knox-005.jpg", "Knox Day crowd"),
            ("gallery/knox-day/knox-006.jpg", "Outdoor party, Knox Day"),
            ("gallery/knox-day/knox-007.jpg", "Group shot, Knox Day"),
            ("gallery/knox-day/knox-008.jpg", "Sunlit rooftop, Knox Day"),
            ("gallery/knox-day/knox-009.jpg", "Daytime party energy"),
            ("gallery/knox-day/knox-010.jpg", "Knox Day vibes"),
            ("gallery/knox-day/knox-011.jpg", "Friends at Knox Day"),
            ("gallery/knox-day/knox-012.jpg", "Rooftop crowd, Knox Day"),
        ],
        "collapsed_range": list(range(13, 21)),  # 8 photos = exactly 2 rows of 4
    },
    {
        "id": "west-village",
        "folder": "gallery/west-village",
        "prefix": "westvillage-",
        "total": 50,
        "visible": [
            ("gallery/west-village/westvillage-001.jpg", "West Village night out"),
            ("gallery/west-village/westvillage-003.jpg", "Crowd at West Village treehouse."),
            ("gallery/west-village/westvillage-005.jpg", "Friends, West Village"),
            ("gallery/west-village/westvillage-007.jpg", "Night crowd, West Village"),
            ("gallery/west-village/westvillage-009.jpg", "West Village party energy"),
            ("gallery/west-village/westvillage-011.jpg", "Group shot, West Village"),
            ("gallery/west-village/westvillage-013.jpg", "West Village rooftop"),
            ("gallery/west-village/westvillage-015.jpg", "Night out, West Village"),
            ("gallery/west-village/westvillage-017.jpg", "Friends at treehouse. West Village"),
            ("gallery/west-village/westvillage-019.jpg", "West Village crowd"),
            ("gallery/west-village/westvillage-021.jpg", "Night vibes, West Village"),
            ("gallery/west-village/westvillage-023.jpg", "West Village, treehouse."),
        ],
        "collapsed_range": list(range(24, 51)),  # 27 photos, trim to 24
    },
]

def make_gallery_item(path, alt, extra_class=""):
    cls = f"gallery-item{' ' + extra_class if extra_class else ''}"
    return f'    <div class="{cls}"><img src="/{path}" alt="{alt}" loading="lazy" onerror="this.onerror=null;this.parentNode.style.display=\'none\'"></div>'

def make_visible_grid(g):
    gid = g['id']
    lines = ['  <div class="gallery-visible" id="gallery-visible-' + gid + '">']
    for path, alt in g['visible']:
        lines.append(make_gallery_item(path, alt))
    lines.append('  </div>')
    return '\n'.join(lines)

def make_collapsed_grid(g):
    gid = g['id']
    prefix_map = {
        'tribeca-rooftop': ('gallery/tribeca-rooftop/tribeca-', '.jpg'),
        'soho-soiree': ('gallery/soho-soiree/soho-', '.jpg'),
        'christmas-nyc': ('gallery/christmas-nyc/xmas-', '.jpg'),
        'dinner-parties': ('gallery/dinner-parties/dinner-', '.jpg'),
        'knox-day': ('gallery/knox-day/knox-', '.jpg'),
        'west-village': ('gallery/west-village/westvillage-', '.jpg'),
    }
    pfx, ext = prefix_map[gid]
    
    nums = g['collapsed_range']
    trim = len(nums) - (len(nums) % 4)
    nums = nums[:trim]
    
    lines = ['  <div class="gallery-collapsed" id="gallery-collapsed-' + gid + '">']
    for n in nums:
        path = pfx + '%03d' % n + ext
        alt = 'treehouse. ' + gid.replace('-', ' ').title() + ' photo ' + str(n)
        lines.append(make_gallery_item(path, alt))
    lines.append('  </div>')
    count = len(nums)
    return '\n'.join(lines), count

# Generate all gallery HTML blocks
for g in galleries:
    visible_html = make_visible_grid(g)
    collapsed_html, count = make_collapsed_grid(g)
    print(f"\n{'='*60}")
    print(f"GALLERY: {g['id']} | visible=12 (4x3) | collapsed={count} ({count//4}x4)")
    print(f"{'='*60}")
    print(visible_html)
    print(collapsed_html)
    print(f'  <div style="text-align:center;padding:1.5rem 0;">')
    print(f'    <button class="gallery-toggle btn btn-s" data-target="gallery-collapsed-{g["id"]}" data-count="{count}" style="font-size:0.65rem;">view all {12+count} photos</button>')
    print(f'  </div>')
