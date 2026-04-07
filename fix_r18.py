#!/usr/bin/env python3
"""Round 18 comprehensive fix script"""
import re, os

# ── helpers ──────────────────────────────────────────────────────────────────
def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  SAVED: {path} ({len(content):,} chars)")

def replace_once(content, old, new, label):
    if old not in content:
        print(f"  MISS: {label}")
        return content
    result = content.replace(old, new, 1)
    print(f"  OK: {label}")
    return result

def replace_all(content, old, new, label):
    count = content.count(old)
    if count == 0:
        print(f"  MISS: {label}")
        return content
    result = content.replace(old, new)
    print(f"  OK ({count}x): {label}")
    return result

# ─────────────────────────────────────────────────────────────────────────────
# FIX #7 — Clean up dinner parties section (replace malformed comment block)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #7: Dinner Parties clean comment ===")
idx_html = read('index.html')

party4_start = idx_html.find('<!-- PARTY 4: DINNER PARTIES -->')
party5_start = idx_html.find('<!-- PARTY 5: KNOX DAY -->')
assert party4_start > 0 and party5_start > 0, "Could not find party markers"

old_block = idx_html[party4_start:party5_start]
new_block = '<!-- REMOVED R18: Empty Dinner Parties section — malformed comment fixed -->\n'
idx_html = idx_html[:party4_start] + new_block + idx_html[party5_start:]
print(f"  OK: Replaced {len(old_block)} chars with clean comment")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #6 — Curate video: object-fit:contain, height:auto, dark green bg
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #6: Curate video CSS ===")
css = read('styles.css')

css = replace_once(css,
    """/* ROUND 17 FIX #1 — Curate video section between curate and April 25 */
.curate-video-section {
  width: 100%;
  overflow: hidden;
  line-height: 0;
  display: block;
}
.curate-video {
  width: 100%;
  max-height: 75vh;
  object-fit: cover;
  display: block;
}
@media (max-width: 768px) {
  .curate-video {
    max-height: 50vh;
  }
}""",
    """/* ROUND 17 FIX #1 — Curate video section between curate and April 25 */
/* ROUND 18 FIX #6 — Changed to contain so full frame is visible, no crop */
.curate-video-section {
  width: 100%;
  background: #2D4A1E;
  line-height: 0;
  display: block;
}
.curate-video {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}""",
    "curate-video CSS update"
)

# ─────────────────────────────────────────────────────────────────────────────
# FIX #5 — Update quote in index.html
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #5: Quote update in index.html ===")
idx_html = replace_all(idx_html,
    '"Best activation we\'ve done in New York. The crowd actually tried the product."',
    '"Fantastic exposure for the brand. Excited to see what we can cook up next, always up to get creative in the treehouse."',
    "old quote (variant 1)"
)
idx_html = replace_all(idx_html,
    '<cite>— Brand Partner</cite>',
    '<cite>— Salud from Tequila Cabal</cite>',
    "old attribution"
)

# ─────────────────────────────────────────────────────────────────────────────
# FIX #4 — Comment out why-sponsor, tiers, partners from index.html
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #4: Comment out sponsor sections from index.html ===")

# why-sponsor section
why_start = idx_html.find('<!-- WHY SPONSOR -->')
why_end = idx_html.find('\n<!-- TIERS -->', why_start)
assert why_start > 0 and why_end > 0, f"Could not find why-sponsor boundaries: {why_start}, {why_end}"
old_why = idx_html[why_start:why_end]
new_why = '<!-- REMOVED R18: Moved to sponsor.html — In Good Company / why-sponsor section -->'
idx_html = idx_html[:why_start] + new_why + idx_html[why_end:]
print(f"  OK: Commented out why-sponsor ({len(old_why)} chars)")

# tiers section
tiers_start = idx_html.find('<!-- TIERS -->')
tiers_end = idx_html.find('\n<!-- PAST ACTIVATIONS -->', tiers_start)
assert tiers_start > 0 and tiers_end > 0, f"Could not find tiers boundaries: {tiers_start}, {tiers_end}"
old_tiers = idx_html[tiers_start:tiers_end]
new_tiers = '<!-- REMOVED R18: Moved to sponsor.html — Sponsorship Packages / tiers section -->'
idx_html = idx_html[:tiers_start] + new_tiers + idx_html[tiers_end:]
print(f"  OK: Commented out tiers ({len(old_tiers)} chars)")

# partners / past activations section
partners_start = idx_html.find('<!-- PAST ACTIVATIONS -->')
# Find the closing </section> after partners_start
partners_section_end = idx_html.find('</section>', idx_html.find('<section', partners_start)) + len('</section>')
assert partners_start > 0 and partners_section_end > partners_start
old_partners = idx_html[partners_start:partners_section_end]
new_partners = '<!-- REMOVED R18: Moved to sponsor.html — Brands That Showed Up / past activations section -->'
idx_html = idx_html[:partners_start] + new_partners + idx_html[partners_section_end:]
print(f"  OK: Commented out partners ({len(old_partners)} chars)")

# Save index.html
write('index.html', idx_html)

# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 + FIX #1 + FIX #3 + FIX #5 — Rebuild sponsor.html
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #2+1+3+5: Rebuild sponsor.html ===")
sp = read('sponsor.html')

# FIX #5 — Update quote in sponsor.html
sp = replace_all(sp,
    '"The best activation we\'ve done in New York. The crowd actually tried the product."',
    '"Fantastic exposure for the brand. Excited to see what we can cook up next, always up to get creative in the treehouse."',
    "old quote (variant 2) in sponsor.html"
)
sp = replace_all(sp,
    '"Best activation we\'ve done in New York. The crowd actually tried the product."',
    '"Fantastic exposure for the brand. Excited to see what we can cook up next, always up to get creative in the treehouse."',
    "old quote (variant 1) in sponsor.html"
)
sp = replace_all(sp,
    '— Past Brand Partner',
    '— Salud from Tequila Cabal',
    "old attribution in sponsor.html"
)

# FIX #2 — Replace hero img with video
old_hero_bg = '''  <div class="sp-hero-bg">
    <img src="/img/curate-room.jpg" alt="Packed rooftop crowd at golden hour — treehouse. NYC" fetchpriority="high" onerror="this.style.display=\'none\'">
  </div>'''
new_hero_bg = '''  <!-- ROUND 18 FIX #2 — Video background for sponsor hero -->
  <video
    class="sp-hero-bg"
    src="/img/sponsor-hero-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="auto"
    poster="/img/hero-new.jpg"
  ></video>'''

if old_hero_bg in sp:
    sp = sp.replace(old_hero_bg, new_hero_bg, 1)
    print("  OK: Hero img replaced with video")
else:
    # Try flexible match
    sp_hero_bg_start = sp.find('<div class="sp-hero-bg">')
    sp_hero_bg_end = sp.find('</div>', sp_hero_bg_start) + len('</div>')
    if sp_hero_bg_start > 0:
        old_block = sp[sp_hero_bg_start:sp_hero_bg_end]
        sp = sp[:sp_hero_bg_start] + new_hero_bg + sp[sp_hero_bg_end:]
        print(f"  OK (flexible): Hero img replaced with video (was: {old_block[:60]}...)")
    else:
        print("  MISS: Could not find sp-hero-bg div")

# Update sp-hero-bg CSS to work as video element (not div)
old_hero_css = '''.sp-hero-bg {'''
new_hero_css = '''/* ROUND 18 FIX #2 — sp-hero-bg is now a video element */
.sp-hero-bg {'''
sp = replace_once(sp, old_hero_css, new_hero_css, "sp-hero-bg CSS comment")

# Also update the CSS rule to remove div-specific properties
old_bg_css = '''.sp-hero-bg {
    position: absolute;
    inset: 0;
    overflow: hidden;
  }
  .sp-hero-bg img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }'''
new_bg_css = '''.sp-hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
  }'''
if old_bg_css in sp:
    sp = sp.replace(old_bg_css, new_bg_css, 1)
    print("  OK: sp-hero-bg CSS updated for video element")
else:
    print("  NOTE: sp-hero-bg CSS not found with exact match — checking alternate")
    # Try to find and update just the img rule
    img_rule_start = sp.find('  .sp-hero-bg img {')
    if img_rule_start > 0:
        img_rule_end = sp.find('}', img_rule_start) + 1
        old_img_rule = sp[img_rule_start:img_rule_end]
        sp = sp[:img_rule_start] + '  /* ROUND 18 FIX #2 — img rule removed, video handles sizing */' + sp[img_rule_end:]
        print(f"  OK: Removed sp-hero-bg img CSS rule")

# FIX #1 — Insert "In Good Company" section and "Brands That Showed Up" after sp-stats
in_good_company_section = '''
<!-- ROUND 18 FIX #1 — In Good Company section moved from index.html -->
<section class="dk grain" id="sp-in-good-company">
  <div class="w" style="max-width:1200px;margin:0 auto;padding:5rem 2rem;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center;" class="sp-igc-grid">
      <!-- Left: copy -->
      <div>
        <span class="lbl reveal-child" style="margin-bottom:1rem">// Past Partners</span>
        <h2 data-a="l" style="font-size:clamp(2rem,4vw,3rem);margin-bottom:1.5rem;color:#E8E6DF;">In Good Company.</h2>
        <div style="margin-bottom:2rem;">
          <p style="font-family:var(--ff-e);font-size:1.05rem;opacity:0.82;line-height:1.7;margin-bottom:1.5rem;">18 brands across 5 events. Spirits, fashion, wellness, tech. The kind of crowd that actually remembers who sponsored the night.</p>
          <blockquote style="border-left:2px solid rgba(232,230,223,0.3);padding-left:1.25rem;font-family:var(--ff-e);font-style:italic;opacity:0.75;line-height:1.6;">"Fantastic exposure for the brand. Excited to see what we can cook up next, always up to get creative in the treehouse."</blockquote>
          <cite style="display:block;margin-top:0.75rem;font-family:var(--ff-b);font-size:0.75rem;letter-spacing:0.08em;opacity:0.55;text-transform:uppercase;">— Salud from Tequila Cabal</cite>
        </div>
        <a href="#sp-contact" class="btn btn-p" style="display:inline-block;">lock in your spot &rarr;</a>
      </div>
      <!-- Right: video -->
      <div style="position:relative;border-radius:4px;overflow:hidden;min-height:400px;">
        <video
          src="/img/sponsor-video.mp4"
          autoplay muted loop playsinline
          preload="metadata"
          style="width:100%;height:100%;min-height:400px;object-fit:cover;display:block;"
        ></video>
      </div>
    </div>
  </div>
</section>

<!-- ROUND 18 FIX #1 — Brands That Showed Up section moved from index.html -->
<section class="dk grain" id="sp-brands">
  <div class="w" style="max-width:1200px;margin:0 auto;padding:5rem 2rem;">
    <span class="lbl reveal-child" data-a="u" style="margin-bottom:1rem">// Past Activations</span>
    <h2 data-a="l" style="margin-bottom:0.75rem;color:#E8E6DF;">Brands that showed up.</h2>
    <p style="font-family:var(--ff-e);font-style:italic;opacity:0.7;margin-bottom:3rem;" data-a="u" data-d="1">18 brands. 5 events. All hand-selected.</p>
    <div class="brands-grid-wrap">
      <img src="/img/logos/07_Zakuska_Vodka.png" alt="Zakuska Vodka" class="brand-logo">
      <img src="/img/logos/08_Friday_Beers.png" alt="Friday Beers" class="brand-logo">
      <img src="/img/logos/09_SURF.png" alt="SURF" class="brand-logo">
      <img src="/img/logos/10_Celsius.png" alt="Celsius" class="brand-logo">
      <img src="/img/logos/11_CLR.png" alt="CLR" class="brand-logo">
      <img src="/img/logos/12_Solento_Organic_Tequila.png" alt="Solento Organic Tequila" class="brand-logo">
      <img src="/img/logos/13_Teremana.png" alt="Teremana" class="brand-logo">
      <img src="/img/logos/14_7th_Street_Burger.png" alt="7th Street Burger" class="brand-logo">
      <img src="/img/logos/15_NightOwl.png" alt="NightOwl" class="brand-logo">
      <img src="/img/logos/16_Bashi.png" alt="Bashi" class="brand-logo">
      <img src="/img/logos/17_Lemon_Perfect.png" alt="Lemon Perfect" class="brand-logo">
      <img src="/img/logos/18_Holiday.png" alt="Holiday" class="brand-logo">
      <img src="/img/logos/01_Tequila_Cabal_Organic.png" alt="Tequila Cabal Organic" class="brand-logo">
      <img src="/img/logos/02_Potro_Tequila.png" alt="Potro Tequila" class="brand-logo">
      <img src="/img/logos/03_Mezcalum.png" alt="Mezcalum" class="brand-logo">
      <img src="/img/logos/04_Mission_Craft_Cocktails.png" alt="Mission Craft Cocktails" class="brand-logo">
      <img src="/img/logos/05_Hampton_Water.png" alt="Hampton Water" class="brand-logo">
      <img src="/img/logos/06_Lucie.png" alt="Lucie" class="brand-logo">
    </div>
    <div style="text-align:center;padding:2.5rem 0;border-top:1px solid var(--ln10);" data-a="u">
      <p style="font-family:var(--ff-e);font-style:italic;opacity:0.72;margin-bottom:1.25rem;">Limited spots available for 2026 events.</p>
      <a href="#sp-packages" class="btn btn-p">see sponsorship packages</a>
    </div>
  </div>
</section>
'''

# Insert after sp-stats section closes
sp_stats_end = sp.find('</section>', sp.find('<section class="sp-stats"')) + len('</section>')
if sp_stats_end > len('</section>'):
    sp = sp[:sp_stats_end] + '\n' + in_good_company_section + sp[sp_stats_end:]
    print("  OK: Inserted In Good Company + Brands sections after sp-stats")
else:
    print("  MISS: Could not find sp-stats section end")

# FIX #3 — Add bottom video above footer
bottom_video = '''
<!-- ROUND 18 FIX #3 — Bottom video on sponsor page -->
<section class="dk sponsor-bottom-video-section">
  <video
    src="/img/sponsor-bottom-video.mp4"
    autoplay
    muted
    loop
    playsinline
    preload="metadata"
    poster="/img/hero-new.jpg"
    class="sponsor-bottom-video"
  ></video>
</section>

'''

# Insert before the footer
footer_start = sp.find('<!-- EXPANSION FIX #10 — footer')
if footer_start > 0:
    sp = sp[:footer_start] + bottom_video + sp[footer_start:]
    print("  OK: Inserted bottom video before footer")
else:
    print("  MISS: Could not find footer marker")

# Add CSS for bottom video and mobile grid fix
bottom_video_css = '''
/* ROUND 18 FIX #3 — Sponsor page bottom video */
.sponsor-bottom-video-section {
  width: 100%;
  line-height: 0;
  overflow: hidden;
}
.sponsor-bottom-video {
  width: 100%;
  max-height: 70vh;
  object-fit: cover;
  display: block;
}
/* ROUND 18 FIX #1 — In Good Company grid responsive */
@media (max-width: 768px) {
  .sp-igc-grid {
    grid-template-columns: 1fr !important;
    gap: 2rem !important;
  }
  .sponsor-bottom-video {
    max-height: 50vh;
  }
}
'''

# Add CSS before closing </style>
style_close = sp.rfind('</style>')
if style_close > 0:
    sp = sp[:style_close] + bottom_video_css + sp[style_close:]
    print("  OK: Added bottom video + mobile grid CSS")
else:
    print("  MISS: Could not find </style> in sponsor.html")

write('sponsor.html', sp)
write('styles.css', css)

print("\n=== ALL FIXES COMPLETE ===")

# Quick verification
idx_final = read('index.html')
sp_final = read('sponsor.html')
print(f"\nVerification:")
checks = [
    ('index.html why-sponsor removed', 'id="why-sponsor"' not in idx_final),
    ('index.html tiers removed', 'id="tiers"' not in idx_final),
    ('index.html partners removed', 'id="partners"' not in idx_final),
    ('index.html dinner parties removed', 'id="dinner-parties"' not in idx_final),
    ('index.html old quote gone', 'Best activation' not in idx_final),
    ('sponsor.html old quote gone', 'best activation' not in sp_final.lower()),
    ('sponsor.html new quote present', 'Fantastic exposure' in sp_final),
    ('sponsor.html hero video', 'sponsor-hero-video.mp4' in sp_final),
    ('sponsor.html bottom video', 'sponsor-bottom-video.mp4' in sp_final),
    ('sponsor.html In Good Company', 'sp-in-good-company' in sp_final),
    ('sponsor.html Brands section', 'sp-brands' in sp_final),
    ('curate video contain', 'object-fit: contain' in read('styles.css')),
]
for label, result in checks:
    print(f"  {'PASS' if result else 'FAIL'}: {label}")
