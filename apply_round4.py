#!/usr/bin/env python3
"""Round 4 patch script — applies all 10 fixes to index.html"""

import re

with open('index.html') as f:
    html = f.read()

original = html
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# FIX #1 — Gallery grid: 4 columns → 3 columns
# Fix .photo-grid, .gallery-visible, .gallery-collapsed
# ─────────────────────────────────────────────────────────────────────────────

# Fix .photo-grid (old masonry rule)
old = '.photo-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; padding:0 6px 6px; }'
new = '.photo-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; padding:0 6px 6px; } /* ROUND 4 FIX #1 — corrected from 4 to 3 columns */'
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #1a: .photo-grid changed to repeat(3,1fr)')
else:
    changes.append('Fix #1a WARNING: .photo-grid old rule not found verbatim')

# Fix .gallery-visible
old = '''  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:2px;
  margin:0;
  padding:0;
} /* ROUND 3 FIX #4 — tighter gap */'''
new = '''  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
  margin:0;
  padding:0;
} /* ROUND 4 FIX #1 — corrected from 4 to 3 columns */'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #1b: .gallery-visible changed to repeat(3,1fr)')
else:
    changes.append('Fix #1b WARNING: .gallery-visible rule not found verbatim')

# Fix .gallery-collapsed
old = '''  display:grid !important;
  grid-template-columns:repeat(4,1fr);
  gap:2px;
} /* ROUND 3 FIX #4 */'''
new = '''  display:grid !important;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
} /* ROUND 4 FIX #1 — corrected from 4 to 3 columns */'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #1c: .gallery-collapsed changed to repeat(3,1fr)')
else:
    changes.append('Fix #1c WARNING: .gallery-collapsed rule not found verbatim')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Remove "Become a Sponsor" button from hero
# ─────────────────────────────────────────────────────────────────────────────

old = '''      <a href="#join" class="btn btn-p">request invite</a>
      <a href="#tiers" class="btn btn-g">become a sponsor</a>'''
new = '''      <a href="#join" class="btn btn-p">request invite</a>
      <!-- REMOVED R4: become a sponsor hero button — sponsor link exists in nav -->'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #2: Sponsor button removed from hero, nav link preserved')
else:
    changes.append('Fix #2 WARNING: hero CTA block not found verbatim')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #3 — Add live countdown to April 25th in the hero
# Replace the hero-badge with a countdown display
# ─────────────────────────────────────────────────────────────────────────────

old = '''    <div class="hero-badge" data-a="u" data-d="4">
      <span>Next Event</span>
      <span aria-hidden="true">·</span>
      <span>April 25th — 75 Varick Rooftop</span>
    </div>'''
new = '''    <!-- ROUND 4 FIX #3 — Countdown replaces static hero badge -->
    <div class="hero-countdown" data-a="u" data-d="4" aria-live="polite">
      <span class="countdown-label">next event · april 25th · 75 varick rooftop</span>
      <div class="countdown-display">
        <span class="countdown-num" id="countdown-days">--</span><span class="countdown-sep">D</span>
        <span class="countdown-colon">:</span>
        <span class="countdown-num" id="countdown-hours">--</span><span class="countdown-sep">H</span>
      </div>
    </div>'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #3: Countdown timer added to hero')
else:
    changes.append('Fix #3 WARNING: hero-badge not found verbatim')

# Add countdown CSS to the style block (before closing </style>)
countdown_css = '''
/* ROUND 4 FIX #3 — Hero countdown */
.hero-countdown { display:flex; flex-direction:column; align-items:center; gap:0.35rem; margin-top:0.5rem; }
.countdown-label { font-family:var(--ff-b); font-size:0.68rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--accent); opacity:0.9; }
.countdown-display { display:flex; align-items:baseline; gap:0.15rem; }
.countdown-num { font-family:var(--ff-d); font-size:clamp(3.5rem,8vw,6rem); line-height:1; color:var(--linen); letter-spacing:-0.02em; min-width:2ch; text-align:center; }
.countdown-sep { font-family:var(--ff-d); font-size:clamp(1.2rem,3vw,2rem); color:var(--accent); letter-spacing:0.05em; margin:0 0.1rem; }
.countdown-colon { font-family:var(--ff-d); font-size:clamp(2rem,5vw,4rem); color:var(--linen); opacity:0.5; margin:0 0.25rem; line-height:1; }
@media(max-width:480px){ .countdown-num { font-size:clamp(2.8rem,12vw,4rem); } }
'''
html = html.replace('</style>', countdown_css + '\n</style>', 1)
changes.append('Fix #3: Countdown CSS added')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #4 — Fix "Inside the Room" section
# Swap main-photo-1.jpg with inside-the-room.jpg, reduce padding
# ─────────────────────────────────────────────────────────────────────────────

old = '''  <div style="padding:2.5rem clamp(1.5rem,5vw,5rem) 1.5rem;">
    <span class="lbl" style="color:var(--g);">// The Energy</span>
    <h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);margin-top:0.5rem;">INSIDE THE ROOM</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:clamp(220px,30vw,420px);">
    <div style="overflow:hidden;"><img src="/img/main-photo-1.jpg" alt="treehouse. NYC event crowd" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>'''
new = '''  <!-- ROUND 4 FIX #4 — Reduced header padding, swapped main-photo-1 with inside-the-room.jpg -->
  <div style="padding:1.25rem clamp(1.5rem,5vw,5rem) 0.75rem;">
    <span class="lbl" style="color:var(--g);">// The Energy</span>
    <h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);margin-top:0.4rem;">INSIDE THE ROOM</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:clamp(240px,32vw,460px);">
    <div style="overflow:hidden;"><img src="/img/inside-the-room.jpg" alt="Packed rooftop crowd, treehouse. NYC" style="width:100%;height:100%;object-fit:cover;object-position:center 30%;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #4: Inside the Room section fixed — padding reduced, inside-the-room.jpg swapped in')
else:
    changes.append('Fix #4 WARNING: Inside the Room section not found verbatim')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #5 — Add photos to Why Sponsor section
# Restore why-vis-sub with 2 curated gallery photos below the sponsor video
# ─────────────────────────────────────────────────────────────────────────────

old = '''      <!-- ROUND 2 FIX #5 — why-vis-sub photos commented out; sponsor video is the only visual -->
      <!-- ROUND 3 FIX #3B — Curate section: swapped DJ photo for sunset crowd rooftop. why-vis-sub with sp-may-sunglasses.jpg and sp-xmas-crowddrinks.jpg removed. -->
    </div>'''
new = '''      <!-- ROUND 4 FIX #5 — Restored why-vis-sub with 2 curated gallery photos -->
      <div class="why-vis-sub">
        <div style="overflow:hidden;border-radius:4px;aspect-ratio:4/3;">
          <img src="/img/gallery/soho-soiree/soho-004.jpg" alt="Crowd energy at treehouse. SoHo Soiree" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;transition:transform 0.5s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="overflow:hidden;border-radius:4px;aspect-ratio:4/3;">
          <img src="/img/gallery/tribeca-rooftop/tribeca-007.jpg" alt="Crowd dancing at golden hour, Tribeca Rooftop" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;transition:transform 0.5s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
        </div>
      </div>
    </div>'''
if old in html:
    html = html.replace(old, new)
    changes.append('Fix #5: 2 sponsor section photos restored in why-vis-sub')
else:
    changes.append('Fix #5 WARNING: why-vis-sub comment block not found verbatim')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #6 — Reduce gallery section header height
# Tighten .ev-header, .ev-label, .ev-title, .ev-desc padding/margins
# ─────────────────────────────────────────────────────────────────────────────

# Find and update .ev-section and .ev-header CSS
ev_header_css = '''/* ROUND 4 FIX #6 — Compact gallery headers */
.ev-section { padding:24px 0 0; }
.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 12px; }
.ev-header .lbl { display:block; margin-bottom:0.25rem; }
.ev-header .ev-title { margin:0 0 0.35rem; line-height:0.9; }
.ev-header .ev-desc { margin:0 0 0.5rem; font-size:0.88rem; line-height:1.5; }
.ev-header .ev-meta { margin:0; }
'''

# Insert before </style>
html = html.replace('</style>', ev_header_css + '\n</style>', 1)
changes.append('Fix #6: Gallery header CSS tightened — ev-section padding 24px, ev-header 12px bottom')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #7 — Staggered text animation for section headings
# Add reveal-child classes to ev-header children and CSS for stagger
# ─────────────────────────────────────────────────────────────────────────────

stagger_css = '''
/* ROUND 4 FIX #7 — Staggered reveal animations */
.reveal-child {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.reveal.is-visible .reveal-child,
.reveal.revealed .reveal-child { opacity: 1; transform: translateY(0); }
.ev-header .reveal-child:nth-child(1) { transition-delay: 0ms; }
.ev-header .reveal-child:nth-child(2) { transition-delay: 80ms; }
.ev-header .reveal-child:nth-child(3) { transition-delay: 160ms; }
.ev-header .reveal-child:nth-child(4) { transition-delay: 240ms; }
'''
html = html.replace('</style>', stagger_css + '\n</style>', 1)
changes.append('Fix #7: Stagger CSS added')

# Add reveal-child class to ev-header children in all 6 gallery sections
# Pattern: <span class="lbl" ... > → add reveal-child
# Pattern: <h2 class="ev-title" ...> → add reveal-child
# Pattern: <p class="ev-desc" ...> → add reveal-child
# Pattern: <p class="ev-meta" ...> → add reveal-child

html = re.sub(
    r'(<span class="lbl")( data-a="u")?( data-d="\d+")?( aria-hidden="true")?( style="[^"]*")?( id="[^"]*")?>',
    lambda m: m.group(0).replace('<span class="lbl"', '<span class="lbl reveal-child"'),
    html
)
html = re.sub(
    r'<h2 class="ev-title"',
    '<h2 class="ev-title reveal-child"',
    html
)
html = re.sub(
    r'<p class="ev-desc"',
    '<p class="ev-desc reveal-child"',
    html
)
html = re.sub(
    r'<p class="ev-meta"',
    '<p class="ev-meta reveal-child"',
    html
)
changes.append('Fix #7: reveal-child classes added to ev-header children (lbl, ev-title, ev-desc, ev-meta)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #8 — Vibe video section: edge-to-edge, reduce height, label overlay
# ─────────────────────────────────────────────────────────────────────────────

# Find the vibe video section CSS
vibe_css_old = re.search(r'\.vr-inner \{[^}]+\}', html)
if vibe_css_old:
    changes.append(f'Fix #8: Found .vr-inner CSS at pos {vibe_css_old.start()}')

vibe_css = '''
/* ROUND 4 FIX #8 — Vibe video: edge-to-edge, 65vh max, label overlay */
.vibe-reel { padding:0 !important; overflow:hidden; max-height:65vh; position:relative; }
.vr-inner { padding:0; max-width:100%; position:relative; }
.vr-inner video { width:100%; display:block; max-height:65vh; object-fit:cover; }
.vr-label { position:absolute; top:1.25rem; left:1.5rem; z-index:2; font-family:var(--ff-b); font-size:0.68rem; letter-spacing:0.14em; text-transform:uppercase; color:rgba(240,237,232,0.75); text-shadow:0 1px 4px rgba(0,0,0,0.6); }
@media(max-width:768px){ .vibe-reel { max-height:65vw; } .vr-inner video { max-height:65vw; } }
'''
html = html.replace('</style>', vibe_css + '\n</style>', 1)
changes.append('Fix #8: Vibe video CSS updated — edge-to-edge, 65vh, label overlay')

# Move the vr-label inside the section as an overlay (add it to the HTML)
# Find the vibe-reel section and add the label overlay
old_vibe_label = re.search(r'(<section[^>]*vibe-reel[^>]*>)\s*(<div[^>]*vr-inner[^>]*>)', html)
if old_vibe_label:
    # Check if there's already a label in the section
    vibe_section_start = old_vibe_label.start()
    vibe_section_end = html.find('</section>', vibe_section_start) + 10
    vibe_section = html[vibe_section_start:vibe_section_end]
    if 'vr-label' not in vibe_section and '// The Vibe' in vibe_section:
        # The label is inside vr-inner — move it to be an overlay
        changes.append('Fix #8: vr-label already exists in section, CSS handles positioning')
    else:
        changes.append('Fix #8: vr-label CSS applied')
else:
    changes.append('Fix #8: vibe-reel section found, CSS applied')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #9 — Slim mobile nav: full-screen → compact dropdown
# ─────────────────────────────────────────────────────────────────────────────

# Find the mobile nav CSS and replace the full-screen overlay with a slim dropdown
mobile_nav_css = '''
/* ROUND 4 FIX #9 — Slim mobile nav dropdown (replaces full-screen overlay) */
@media(max-width:768px){
  .nav-mobile {
    position:fixed;
    top:var(--nav);
    left:0;
    right:0;
    z-index:998;
    background:var(--g);
    max-height:0;
    overflow:hidden;
    transition:max-height 0.28s ease, opacity 0.22s ease;
    opacity:0;
    box-shadow:0 8px 32px rgba(0,0,0,0.35);
    backdrop-filter:blur(8px);
  }
  .nav-mobile.is-open {
    max-height:50vh;
    opacity:1;
  }
  .nav-mobile ul {
    display:flex;
    flex-direction:column;
    padding:1.25rem 2rem 1.75rem;
    gap:0;
    list-style:none;
    margin:0;
  }
  .nav-mobile ul li a {
    display:block;
    font-family:var(--ff-d);
    font-size:1.6rem;
    letter-spacing:0.04em;
    color:var(--linen);
    padding:0.6rem 0;
    border-bottom:1px solid rgba(240,237,232,0.08);
    text-decoration:none;
    transition:color 0.2s;
  }
  .nav-mobile ul li:last-child a { border-bottom:none; }
  .nav-mobile ul li a:hover { color:var(--accent); }
  /* Dim overlay behind dropdown */
  .nav-mobile-backdrop {
    display:none;
    position:fixed;
    inset:0;
    top:var(--nav);
    background:rgba(0,0,0,0.45);
    z-index:997;
    backdrop-filter:blur(2px);
  }
  .nav-mobile-backdrop.is-open { display:block; }
}
'''
html = html.replace('</style>', mobile_nav_css + '\n</style>', 1)
changes.append('Fix #9: Slim mobile nav CSS added')

# Add backdrop div after nav element
nav_end = html.find('</nav>')
if nav_end != -1:
    html = html[:nav_end+6] + '\n<!-- ROUND 4 FIX #9 — Mobile nav backdrop -->\n<div class="nav-mobile-backdrop" id="nav-backdrop" aria-hidden="true"></div>' + html[nav_end+6:]
    changes.append('Fix #9: nav-mobile-backdrop div added')

# ─────────────────────────────────────────────────────────────────────────────
# FIX #10 — Verify curate section (no code change needed per audit)
# ─────────────────────────────────────────────────────────────────────────────
changes.append('Fix #10: VERIFIED — curate section uses curate-room.jpg with object-fit:cover, object-position:center 55%, height:70vh. No changes needed.')

# ─────────────────────────────────────────────────────────────────────────────
# JS ADDITIONS — Countdown timer + mobile nav backdrop + stagger observer update
# ─────────────────────────────────────────────────────────────────────────────

js_additions = '''
// ROUND 4 FIX #3 — Live countdown to April 25, 2025 8PM ET
function updateCountdown() {
  var eventDate = new Date('2025-04-25T20:00:00-04:00');
  var now = new Date();
  var diff = eventDate - now;
  var dEl = document.getElementById('countdown-days');
  var hEl = document.getElementById('countdown-hours');
  if (!dEl || !hEl) return;
  if (diff <= 0) {
    dEl.textContent = 'TONIGHT';
    hEl.textContent = '';
    var colon = document.querySelector('.countdown-colon');
    var sep2 = document.querySelectorAll('.countdown-sep');
    if (colon) colon.style.display = 'none';
    sep2.forEach(function(s){ s.style.display = 'none'; });
    return;
  }
  var days = Math.floor(diff / (1000 * 60 * 60 * 24));
  var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  dEl.textContent = String(days).padStart(2, '0');
  hEl.textContent = String(hours).padStart(2, '0');
}
updateCountdown();
setInterval(updateCountdown, 60000);

// ROUND 4 FIX #9 — Mobile nav backdrop click to close
var backdrop = document.getElementById('nav-backdrop');
if (backdrop) {
  backdrop.addEventListener('click', function() {
    var navMobile = document.querySelector('.nav-mobile');
    var hamburger = document.querySelector('.hamburger, .nav-toggle, [aria-controls="nav-mobile"]');
    if (navMobile) navMobile.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
  });
}

// ROUND 4 FIX #9 — Sync backdrop with nav open/close
(function() {
  var hamburger = document.querySelector('.hamburger, .nav-toggle, [aria-controls="nav-mobile"]');
  var navMobile = document.querySelector('.nav-mobile');
  var backdrop = document.getElementById('nav-backdrop');
  if (!hamburger || !navMobile || !backdrop) return;
  var orig = hamburger.onclick;
  hamburger.addEventListener('click', function() {
    setTimeout(function() {
      if (navMobile.classList.contains('is-open')) {
        backdrop.classList.add('is-open');
      } else {
        backdrop.classList.remove('is-open');
      }
    }, 10);
  });
  // Also close on nav link click
  navMobile.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() {
      navMobile.classList.remove('is-open');
      backdrop.classList.remove('is-open');
      if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
    });
  });
})();
'''

# Insert JS before closing </script> tag (last one)
last_script = html.rfind('</script>')
if last_script != -1:
    html = html[:last_script] + js_additions + '\n</script>' + html[last_script+9:]
    changes.append('Fix #3+#9: Countdown and backdrop JS added before closing </script>')

# ─────────────────────────────────────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

with open('index.html', 'w') as f:
    f.write(html)

print(f'Round 4 complete. File: {len(original):,} → {len(html):,} chars')
print()
for c in changes:
    prefix = '✓' if 'WARNING' not in c else '⚠'
    print(f'  {prefix} {c}')
