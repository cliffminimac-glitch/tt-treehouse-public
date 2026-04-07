#!/usr/bin/env python3
"""Round 19 fix script"""

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

sp = read('sponsor.html')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #1 — Swap hero video src
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #1: Swap hero video ===")
sp = replace_once(sp,
    'src="/img/sponsor-hero-video.mp4"',
    '<!-- ROUND 19 FIX #1 — Swapped to v2 -->\n    src="/img/sponsor-hero-video-v2.mp4"',
    "hero video src swap"
)

# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Swap bottom video src
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #2: Swap bottom video ===")
sp = replace_once(sp,
    'src="/img/sponsor-bottom-video.mp4"',
    '<!-- ROUND 19 FIX #2 — Swapped to v2 -->\n    src="/img/sponsor-bottom-video-v2.mp4"',
    "bottom video src swap"
)

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3 — Add "Why Sponsor?" heading above stats grid
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #3: Add Why Sponsor? heading ===")
sp = replace_once(sp,
    '<span class="sp-stats-label">// Why Treehouse</span>\n    <div class="sp-stats-grid">',
    '''<span class="sp-stats-label">// Why Treehouse</span>
    <!-- ROUND 19 FIX #3 — Why Sponsor? heading -->
    <h2 class="sp-why-heading">Why Sponsor?</h2>
    <div class="sp-stats-grid">''',
    "Why Sponsor heading insertion"
)

# Add CSS for the heading — find the closing </style> in sponsor.html
style_close = sp.rfind('</style>')
why_heading_css = '''
  /* ROUND 19 FIX #3 — Why Sponsor? heading */
  .sp-why-heading {
    font-family: var(--ff-d);
    font-size: clamp(2.5rem, 5vw, 4rem);
    color: var(--g);
    margin-bottom: 2.5rem;
    letter-spacing: 0.02em;
    line-height: 1;
  }
'''
if style_close > 0:
    sp = sp[:style_close] + why_heading_css + sp[style_close:]
    print("  OK: Why Sponsor CSS added")
else:
    print("  MISS: Could not find </style>")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #4 — Update brand logos (keep Celsius + Lucie, replace all others)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #4: Update brand logos ===")

old_logos_block = '''    <div class="brands-grid-wrap">
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
    </div>'''

new_logos_block = '''    <!-- REMOVED R19: Old brand logos (keeping Celsius and Lucie) -->
    <!-- ROUND 19 FIX #4 — Updated brand logos: Celsius + Lucie kept, 16 new logos added -->
    <div class="brands-grid-wrap brands-grid-r19">
      <!-- KEPT: Celsius and Lucie -->
      <img src="/img/logos/10_Celsius.png" alt="Celsius" class="brand-logo" loading="lazy">
      <img src="/img/logos/06_Lucie.png" alt="Lucie" class="brand-logo" loading="lazy">
      <!-- 16 new brand logos -->
      <img src="/img/brand-logo-01.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-02.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-03.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-04.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-05.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-06.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-07.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-08.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-09.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-10.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-11.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-12.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-13.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-14.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-15.png" alt="Brand partner" class="brand-logo" loading="lazy">
      <img src="/img/brand-logo-16.png" alt="Brand partner" class="brand-logo" loading="lazy">
    </div>'''

sp = replace_once(sp, old_logos_block, new_logos_block, "brand logos block replacement")

# Add CSS for the new logo grid
logo_css = '''
  /* ROUND 19 FIX #4 — Updated brand logo grid with consistent sizing */
  .brands-grid-r19 {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem 3rem;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 0;
  }
  .brands-grid-r19 .brand-logo {
    height: 48px;
    width: auto;
    max-width: 140px;
    object-fit: contain;
    opacity: 0.75;
    filter: brightness(0) invert(1);
    transition: opacity 0.2s;
  }
  .brands-grid-r19 .brand-logo:hover {
    opacity: 1;
  }
  @media (max-width: 768px) {
    .brands-grid-r19 {
      gap: 1.5rem 2rem;
    }
    .brands-grid-r19 .brand-logo {
      height: 36px;
      max-width: 100px;
    }
  }
  @media (max-width: 480px) {
    .brands-grid-r19 {
      gap: 1.25rem 1.5rem;
    }
    .brands-grid-r19 .brand-logo {
      height: 30px;
      max-width: 80px;
    }
  }
'''
style_close = sp.rfind('</style>')
if style_close > 0:
    sp = sp[:style_close] + logo_css + sp[style_close:]
    print("  OK: Brand logo CSS added")

# ─────────────────────────────────────────────────────────────────────────────
# FIX #5 — Remove dead space: reduce padding on sp-brands inner div
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== FIX #5: Remove dead space ===")

# Reduce padding on the sp-brands inner div
sp = replace_once(sp,
    '<div class="w" style="max-width:1200px;margin:0 auto;padding:5rem 2rem;">\n    <span class="lbl reveal-child" data-a="u" style="margin-bottom:1rem">// Past Activations</span>',
    '<!-- ROUND 19 FIX #5 — Reduced padding to remove dead space -->\n  <div class="w" style="max-width:1200px;margin:0 auto;padding:3rem 2rem 1.5rem;">\n    <span class="lbl reveal-child" data-a="u" style="margin-bottom:1rem">// Past Activations</span>',
    "sp-brands padding reduction"
)

# Remove the bottom CTA row padding (the "Limited spots" row)
sp = replace_once(sp,
    '<div style="text-align:center;padding:2.5rem 0;border-top:1px solid var(--ln10);" data-a="u">\n      <p style="font-family:var(--ff-e);font-style:italic;opacity:0.72;margin-bottom:1.25rem;">Limited spots available for 2026 events.</p>\n      <a href="#sp-packages" class="btn btn-p">see sponsorship packages</a>\n    </div>',
    '<!-- ROUND 19 FIX #5 — Reduced bottom CTA padding -->\n    <div style="text-align:center;padding:1rem 0 0;border-top:1px solid var(--ln10);margin-top:2rem;" data-a="u">\n      <p style="font-family:var(--ff-e);font-style:italic;opacity:0.72;margin-bottom:1rem;">Limited spots available for 2026 events.</p>\n      <a href="#sp-packages" class="btn btn-p">see sponsorship packages</a>\n    </div>',
    "sp-brands CTA row padding reduction"
)

write('sponsor.html', sp)

# ─────────────────────────────────────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== VERIFICATION ===")
sp_final = read('sponsor.html')
checks = [
    ('Hero video v2', 'sponsor-hero-video-v2.mp4' in sp_final),
    ('Old hero video gone', 'src="/img/sponsor-hero-video.mp4"' not in sp_final),
    ('Bottom video v2', 'sponsor-bottom-video-v2.mp4' in sp_final),
    ('Old bottom video gone', 'src="/img/sponsor-bottom-video.mp4"' not in sp_final),
    ('Why Sponsor heading', 'sp-why-heading' in sp_final),
    ('Celsius logo kept', '10_Celsius.png' in sp_final),
    ('Lucie logo kept', '06_Lucie.png' in sp_final),
    ('16 new logos present', 'brand-logo-16.png' in sp_final),
    ('Old logos commented out', 'Zakuska Vodka' not in sp_final or '<!-- REMOVED R19' in sp_final),
    ('brands-grid-r19 class', 'brands-grid-r19' in sp_final),
    ('Reduced sp-brands padding', 'padding:3rem 2rem 1.5rem' in sp_final),
    ('HTML complete', '</html>' in sp_final),
]
for label, result in checks:
    print(f"  {'PASS' if result else 'FAIL'}: {label}")
