#!/usr/bin/env python3
"""Round 20 fix script — 5 fixes across index.html and sponsor.html"""

import re

# ─── index.html ────────────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

original_idx = idx

# Fix #1 — Swap footer-01 and footer-02
# The footer has 4 photos; swap positions 1 and 2
idx = idx.replace(
    'src="/img/footer-01.jpg"',
    'src="/img/FOOTER_SWAP_PLACEHOLDER.jpg"',
    1  # only first occurrence
)
idx = idx.replace(
    'src="/img/footer-02.jpg"',
    'src="/img/footer-01.jpg"',
    1
)
idx = idx.replace(
    'src="/img/FOOTER_SWAP_PLACEHOLDER.jpg"',
    'src="/img/footer-02.jpg"',
    1
)
print("Fix #1: Footer photos swapped (footer-01 ↔ footer-02)")

# Fix #2 — Comment out all 5 ev-date location spans in gallery headers
# Pattern: <span class="ev-date">..., New York City</span>
ev_date_pattern = re.compile(
    r'(<span class="ev-date">[^<]*New York City</span>)'
)
matches = ev_date_pattern.findall(idx)
print(f"Fix #2: Found {len(matches)} ev-date location spans to comment out")
for match in matches:
    idx = idx.replace(
        match,
        f'<!-- REMOVED R20: location text under gallery header {match} -->',
        1
    )
print(f"Fix #2: All {len(matches)} location spans commented out")

# Verify
remaining = ev_date_pattern.findall(idx)
# Only count ones not inside comments
active = [m for m in remaining if '<!-- REMOVED' not in idx[max(0, idx.find(m)-20):idx.find(m)]]
print(f"Fix #2: Active ev-date spans remaining: {len(active)}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("index.html saved.\n")

# ─── sponsor.html ──────────────────────────────────────────────────────────────
with open('sponsor.html', 'r', encoding='utf-8') as f:
    sp = f.read()

original_sp = sp

# Fix #3 — Fix hero video tag (remove inline comment, update src, remove poster)
# Find the hero video element
hero_video_start = sp.find('<video\n    class="sp-hero-bg"')
if hero_video_start == -1:
    hero_video_start = sp.find('<video\n  class="sp-hero-bg"')
if hero_video_start == -1:
    # Try broader search
    hero_video_start = sp.find('class="sp-hero-bg"')
    hero_video_start = sp.rfind('<video', 0, hero_video_start)

hero_video_end = sp.find('></video>', hero_video_start) + len('></video>')
old_hero_video = sp[hero_video_start:hero_video_end]
print(f"Fix #3: Found hero video tag ({len(old_hero_video)} chars)")
print(f"  Old: {old_hero_video[:200]}...")

new_hero_video = '''<video
    class="sp-hero-bg"
    src="/img/sponsor-hero-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="auto"
  ></video>'''

sp = sp[:hero_video_start] + '<!-- ROUND 20 FIX #3 — hero video fixed: clean tag, correct src, no poster -->\n  ' + new_hero_video + sp[hero_video_end:]
print("Fix #3: Hero video tag fixed")

# Fix #4 — Fix bottom video tag (remove inline comment, update src, remove poster)
bottom_video_start = sp.find('class="sponsor-bottom-video"')
bottom_video_start = sp.rfind('<video', 0, bottom_video_start)
bottom_video_end = sp.find('></video>', bottom_video_start) + len('></video>')
old_bottom_video = sp[bottom_video_start:bottom_video_end]
print(f"\nFix #4: Found bottom video tag ({len(old_bottom_video)} chars)")
print(f"  Old: {old_bottom_video[:200]}...")

new_bottom_video = '''<video
    src="/img/sponsor-bottom-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    class="sponsor-bottom-video"
  ></video>'''

sp = sp[:bottom_video_start] + '<!-- ROUND 20 FIX #4 — bottom video fixed: clean tag, correct src, no poster -->\n  ' + new_bottom_video + sp[bottom_video_end:]
print("Fix #4: Bottom video tag fixed")

# Fix #5 — Comment out standalone Why Sponsor? h2 from sp-stats
# Add Why Sponsor? inline in sp-in-good-company left column above // Past Partners
# Step 5a: Comment out the standalone h2
why_h2_pattern = re.compile(r'<h2 class="sp-why-heading"[^>]*>Why Sponsor\?</h2>')
match_5a = why_h2_pattern.search(sp)
if match_5a:
    sp = sp[:match_5a.start()] + '<!-- REMOVED R20: standalone Why Sponsor? heading moved inline -->' + sp[match_5a.end():]
    print("\nFix #5a: Standalone Why Sponsor? h2 commented out")
else:
    print("\nFix #5a: sp-why-heading not found — checking for it differently")
    idx_why = sp.find('Why Sponsor?')
    if idx_why != -1:
        print(f"  Found 'Why Sponsor?' at char {idx_why}: {sp[max(0,idx_why-50):idx_why+100]}")

# Step 5b: Add Why Sponsor? heading inline in sp-in-good-company left column
# Find the // Past Partners label
past_partners_label = '<span class="ev-label">// Past Partners</span>'
if past_partners_label in sp:
    sp = sp.replace(
        past_partners_label,
        '<!-- ROUND 20 FIX #5 — Why Sponsor? heading added inline -->\n          <h2 class="sp-inline-why" style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);color:#E8E6DF;letter-spacing:0.02em;margin:0 0 0.5rem;line-height:1;">Why Sponsor?</h2>\n          ' + past_partners_label,
        1
    )
    print("Fix #5b: Why Sponsor? heading added inline above // Past Partners")
else:
    print("Fix #5b: // Past Partners label not found — searching...")
    idx_pp = sp.find('Past Partners')
    if idx_pp != -1:
        print(f"  Found at char {idx_pp}: {sp[max(0,idx_pp-100):idx_pp+100]}")

with open('sponsor.html', 'w', encoding='utf-8') as f:
    f.write(sp)
print("\nsponsor.html saved.")

# ─── Final verification ────────────────────────────────────────────────────────
print("\n=== FINAL VERIFICATION ===")

with open('index.html') as f:
    idx_check = f.read()

# Check footer swap
f1_pos = idx_check.find('footer-01.jpg')
f2_pos = idx_check.find('footer-02.jpg')
print(f"Footer: footer-01 at pos {f1_pos}, footer-02 at pos {f2_pos} (02 should come first)")
print(f"  Footer swap correct: {f2_pos < f1_pos}")

# Check ev-date removal
active_ev = len(re.findall(r'<span class="ev-date">', idx_check))
print(f"Active ev-date spans in index.html: {active_ev} (should be 0)")

with open('sponsor.html') as f:
    sp_check = f.read()

# Check hero video
print(f"Hero video src correct: {'/img/sponsor-hero-video.mp4' in sp_check and 'sponsor-hero-video-v2' not in sp_check}")
print(f"Bottom video src correct: {'/img/sponsor-bottom-video.mp4' in sp_check and 'sponsor-bottom-video-v2' not in sp_check}")
print(f"No inline comments in video tags: {'<!-- ROUND 19' not in sp_check}")
print(f"Why Sponsor? inline heading present: {'sp-inline-why' in sp_check}")
print(f"Standalone Why Sponsor? h2 removed: {'sp-why-heading' not in sp_check or 'REMOVED R20' in sp_check}")

print("\nAll checks complete.")
