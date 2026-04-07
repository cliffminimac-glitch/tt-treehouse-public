with open('index.html') as f:
    content = f.read()

original_len = len(content)

# =====================================================================
# FIX #1 — Insert curate-video section between curate and April 25
# =====================================================================
curate_video_section = '''
<!-- ROUND 17 FIX #1 — Video between curate section and April 25 next event -->
<section class="dk curate-video-section">
  <video
    src="/img/curate-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    poster="/img/hero-new.jpg"
    class="curate-video"
  ></video>
</section>

'''

# Insert after the curate section closing tag and before the events section
old_transition = '</section>\n\n<section class="dk grain" id="events"'
new_transition = '</section>\n' + curate_video_section + '<section class="dk grain" id="events"'

if old_transition in content:
    content = content.replace(old_transition, new_transition, 1)
    print("PASS: Fix #1 — curate-video section inserted")
else:
    print("FAIL: Fix #1 — could not find insertion point")

# =====================================================================
# FIX #2 — Replace footer photos in index.html
# =====================================================================
old_footer_photos = '''    <div style="overflow:hidden;"><img src="/img/gallery/tribeca-rooftop/tribeca-005.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/soho-soiree/soho-006.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/christmas-nyc/xmas-003.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/knox-day/knox-001.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>'''

new_footer_photos = '''    <!-- REMOVED R17: old footer photos — tribeca-005, soho-006, xmas-003, knox-001 -->
    <!-- ROUND 17 FIX #2 — New footer photos -->
    <div style="overflow:hidden;"><img src="/img/footer-01.jpg" alt="Treehouse event" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/footer-02.jpg" alt="Treehouse event" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/footer-03.jpg" alt="Treehouse event" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/footer-04.jpg" alt="Treehouse event" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>'''

if old_footer_photos in content:
    content = content.replace(old_footer_photos, new_footer_photos, 1)
    print("PASS: Fix #2 — footer photos replaced")
else:
    print("FAIL: Fix #2 — could not find footer photos block")

# =====================================================================
# FIX #3 — Update guest count from 300/400 to 500 in index.html
# =====================================================================
replacements_index = [
    ('300\u2013400 guests \u00b7 Invite Only \u00b7 Open Bar', '500 guests \u00b7 Invite Only \u00b7 Open Bar'),
    ('300\u2013400 guests \xb7 Invite Only \xb7 Open Bar', '500 guests \xb7 Invite Only \xb7 Open Bar'),
    ('300-400 guests \u00b7 Invite Only \u00b7 Open Bar', '500 guests \u00b7 Invite Only \u00b7 Open Bar'),
    ('April 25 \u00b7 75 Varick Rooftop \u00b7 300 guests \u00b7 Waitlist open', 'April 25 \u00b7 75 Varick Rooftop \u00b7 500 guests \u00b7 Waitlist open'),
]

for old, new in replacements_index:
    if old in content:
        content = content.replace(old, new)
        print(f"PASS: Fix #3 index — replaced: {old[:60]}")
    else:
        # Try ASCII hyphen variant
        old2 = old.replace('\u2013', '-').replace('\u00b7', '\xb7')
        if old2 in content:
            content = content.replace(old2, new)
            print(f"PASS: Fix #3 index (ascii variant) — replaced: {old[:60]}")
        else:
            print(f"WARN: Fix #3 index — not found: {old[:60]}")

# Final check for any remaining 300 guest references in index
remaining = [l.strip() for l in content.split('\n') if '300' in l and 'guest' in l.lower()]
if remaining:
    print(f"WARN: Still found 300+guest in index.html: {remaining}")

# =====================================================================
# VERIFY and SAVE index.html
# =====================================================================
checks = [
    ('curate-video.mp4 present', 'curate-video.mp4'),
    ('footer-01.jpg present', 'footer-01.jpg'),
    ('footer-02.jpg present', 'footer-02.jpg'),
    ('footer-03.jpg present', 'footer-03.jpg'),
    ('footer-04.jpg present', 'footer-04.jpg'),
    ('500 guests in event-meta', '500 guests \u00b7 Invite Only'),
    ('500 guests in scarcity line', '500 guests \u00b7 Waitlist open'),
    ('HTML not truncated', '</html>'),
]
all_pass = True
for name, check in checks:
    found = check in content
    print(f"{'PASS' if found else 'FAIL'}: {name}")
    if not found:
        all_pass = False

if all_pass:
    with open('index.html', 'w') as f:
        f.write(content)
    print(f"\nindex.html saved. Length: {len(content)} chars (was {original_len})")
else:
    print("\nERROR: Not saving index.html due to failures")
