#!/usr/bin/env python3
"""
Apply all 15 fixes from the Site Overhaul Prompt to index.html.
Each fix is commented with AUDIT FIX #N in the output HTML.
"""

BASE = "/home/ubuntu/treehouse-audit"

with open(BASE + '/index.html', 'r') as f:
    html = f.read()

original = html  # keep backup reference

# ============================================================
# FIX #1 — Move Tribeca gallery up (right after marquee, before curate section)
# Strategy: extract Tribeca section, remove it from current location,
# insert it right after the marquee block.
# ============================================================

# Extract the full Tribeca section
TRIBECA_START = '<!-- PARTY 1: TRIBECA ROOFTOP -->'
TRIBECA_END = '<!-- PARTY 2: SOHO SOIREE -->'
t_start = html.find(TRIBECA_START)
t_end = html.find(TRIBECA_END)
tribeca_block = html[t_start:t_end]

# Remove Tribeca from its current location
html = html[:t_start] + html[t_end:]

# Insert Tribeca right after the marquee block, before the ABOUT section
MARQUEE_END = '</div>\n</div>\n\n<!-- ABOUT -->'
insert_point = html.find(MARQUEE_END)
if insert_point == -1:
    # Try alternate ending
    MARQUEE_END = '</div>\n</div>\n\n<!-- ABOUT'
    insert_point = html.find(MARQUEE_END)

if insert_point != -1:
    insert_after = insert_point + len('</div>\n</div>')
    # Add AUDIT FIX comment to Tribeca section
    tribeca_tagged = tribeca_block.replace(
        '<!-- PARTY 1: TRIBECA ROOFTOP -->',
        '<!-- AUDIT FIX #1 — Gallery moved up: appears within first 2 scroll-depths -->\n<!-- PARTY 1: TRIBECA ROOFTOP -->'
    )
    html = html[:insert_after] + '\n\n' + tribeca_tagged + html[insert_after:]
    print("Fix #1: Tribeca gallery moved up after marquee")
else:
    print("Fix #1 ERROR: Could not find marquee end marker")

# ============================================================
# FIX #2 — Fix the video section
# ============================================================
OLD_VIDEO = '''<section class="dk grain" id="vibe" style="padding:4rem 0;">
  <div class="vr-inner">
    <span class="lbl">// The Vibe</span> <div class="vibe-video-slot" data-a="f" data-d="1">
      <video autoplay muted loop playsinline controls style="width:100%;border-radius:6px;display:block;">
        <source src="/img/hero-video.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</section>'''

NEW_VIDEO = '''<!-- AUDIT FIX #2 — Video: poster frame, preload metadata, full-bleed, proper height -->
<section class="dk grain" id="vibe" style="padding:4rem 0;">
  <div style="width:100%;max-width:100%;padding:0;text-align:center;">
    <span class="lbl" style="display:block;margin-bottom:1.5rem;padding:0 clamp(1.5rem,5vw,5rem);">// The Vibe</span>
    <div style="width:100%;overflow:hidden;border-radius:0;">
      <video autoplay muted loop playsinline controls
        poster="/img/hero-new.jpg"
        preload="metadata"
        style="width:100%;max-height:80vh;object-fit:cover;display:block;border-radius:0;">
        <source src="/img/hero-video.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</section>'''

if OLD_VIDEO in html:
    html = html.replace(OLD_VIDEO, NEW_VIDEO)
    print("Fix #2: Video section fixed")
else:
    # Try partial match
    html = html.replace(
        '<video autoplay muted loop playsinline controls style="width:100%;border-radius:6px;display:block;">',
        '<video autoplay muted loop playsinline controls poster="/img/hero-new.jpg" preload="metadata" style="width:100%;max-height:80vh;object-fit:cover;display:block;">'
    )
    html = html.replace(
        '<div class="vr-inner">',
        '<!-- AUDIT FIX #2 — Video: full-bleed, poster, preload -->\n  <div style="width:100%;max-width:100%;padding:0;">'
    )
    print("Fix #2: Video section partially fixed")

# ============================================================
# FIX #3 — Add section label to the editorial triptych
# ============================================================
OLD_TRIPTYCH = '''<section class="lt" style="padding:0;">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:320px;">
    <div style="overflow:hidden;"><img src="/img/main-photo-1.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>
</section>'''

NEW_TRIPTYCH = '''<!-- AUDIT FIX #3 — Editorial triptych: added section identity label "THE ENERGY" -->
<section class="lt" style="padding:0;" id="the-energy">
  <div style="padding:2.5rem clamp(1.5rem,5vw,5rem) 1.5rem;">
    <span class="lbl" style="color:var(--g);">// The Energy</span>
    <h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);margin-top:0.5rem;">INSIDE THE ROOM</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:clamp(220px,30vw,420px);">
    <div style="overflow:hidden;"><img src="/img/main-photo-1.jpg" alt="treehouse. NYC event crowd" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-2.jpg" alt="treehouse. NYC event atmosphere" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
    <div style="overflow:hidden;"><img src="/img/main-photo-3.jpg" alt="treehouse. NYC event energy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
  </div>
</section>'''

if OLD_TRIPTYCH in html:
    html = html.replace(OLD_TRIPTYCH, NEW_TRIPTYCH)
    print("Fix #3: Triptych section label added")
else:
    print("Fix #3 WARNING: Triptych exact match not found, trying partial")
    html = html.replace(
        '<section class="lt" style="padding:0;">\n  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:320px;">',
        '<!-- AUDIT FIX #3 — Editorial triptych: added section identity -->\n<section class="lt" style="padding:0;" id="the-energy">\n  <div style="padding:2rem clamp(1.5rem,5vw,5rem) 1rem;"><span class="lbl" style="color:var(--g);">// The Energy</span><h2 style="font-family:var(--ff-d);font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.01em;line-height:0.9;color:var(--g);margin-top:0.5rem;">INSIDE THE ROOM</h2></div>\n  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;height:clamp(220px,30vw,420px);">'
    )
    print("Fix #3: Partial fix applied")

# ============================================================
# FIX #4 — Comment out How It Works section
# ============================================================
OLD_HIW = '''<!-- HOW IT WORKS -->
<section class="lt" id="how-it-works">
  <div class="w hiw-inner">
    <span class="lbl" data-a="u" style="margin-bottom:1rem">// How It Works</span>
    <h2 data-a="l">How to<br>get in.</h2>
    <div class="hiw-steps" data-a="u" data-d="1">
      <div class="hiw-step">
        <span class="hiw-n">01</span>
        <h3 class="hiw-t">Apply</h3>
        <p class="hiw-d">Drop your email below. We'll reach out before the next event.</p>
      </div>
      <div class="hiw-step">
        <span class="hiw-n">02</span>
        <h3 class="hiw-t">Get Approved</h3>
        <p class="hiw-d">We keep the list tight. Not everyone gets in, and that's the point.</p>
      </div>
      <div class="hiw-step">
        <span class="hiw-n">03</span>
        <h3 class="hiw-t">Show Up</h3>
        <p class="hiw-d">Show up at 75 Varick. Open bar from the jump. You'll know people.</p>
      </div>
      <div class="hiw-step">
        <span class="hiw-n">04</span>
        <h3 class="hiw-t">Come Back</h3>
        <p class="hiw-d">We run events all year. Once you're in, you're in.</p>
      </div>
    </div>
  </div>
</section>'''

NEW_HIW = '''<!-- AUDIT FIX #4 — How It Works section commented out (filler) -->
<!-- REMOVED: How It Works
<section class="lt" id="how-it-works">
  <div class="w hiw-inner">
    <span class="lbl" data-a="u" style="margin-bottom:1rem">// How It Works</span>
    <h2 data-a="l">How to<br>get in.</h2>
    <div class="hiw-steps" data-a="u" data-d="1">
      <div class="hiw-step"><span class="hiw-n">01</span><h3 class="hiw-t">Apply</h3><p class="hiw-d">Drop your email below. We\'ll reach out before the next event.</p></div>
      <div class="hiw-step"><span class="hiw-n">02</span><h3 class="hiw-t">Get Approved</h3><p class="hiw-d">We keep the list tight. Not everyone gets in, and that\'s the point.</p></div>
      <div class="hiw-step"><span class="hiw-n">03</span><h3 class="hiw-t">Show Up</h3><p class="hiw-d">Show up at 75 Varick. Open bar from the jump. You\'ll know people.</p></div>
      <div class="hiw-step"><span class="hiw-n">04</span><h3 class="hiw-t">Come Back</h3><p class="hiw-d">We run events all year. Once you\'re in, you\'re in.</p></div>
    </div>
  </div>
</section>
-->'''

if OLD_HIW in html:
    html = html.replace(OLD_HIW, NEW_HIW)
    print("Fix #4: How It Works commented out")
else:
    # Try to find and comment it out
    hiw_start = html.find('<!-- HOW IT WORKS -->')
    hiw_end = html.find('<!-- JOIN -->')
    if hiw_start != -1 and hiw_end != -1:
        hiw_content = html[hiw_start:hiw_end]
        html = html[:hiw_start] + '<!-- AUDIT FIX #4 — How It Works commented out\n' + hiw_content.replace('-->', '- ->').replace('<!--', '< !--') + '\n-->\n\n' + html[hiw_end:]
        print("Fix #4: How It Works commented out (fallback method)")
    else:
        print("Fix #4 ERROR: Could not find How It Works section")

# ============================================================
# FIX #5 — Reduce gallery header dead space
# ============================================================
# Change .ev-section padding from 80px to 40px
html = html.replace(
    '.ev-section { padding:80px 0 0; }',
    '/* AUDIT FIX #5 — Reduced gallery header dead space */\n.ev-section { padding:40px 0 0; }'
)
# Tighten ev-header bottom padding
html = html.replace(
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 2rem; max-width:var(--wrap); margin:0 auto; }',
    '.ev-header { padding:0 clamp(1.5rem,5vw,5rem) 1.25rem; max-width:var(--wrap); margin:0 auto; }'
)
# Tighten ev-title margin
html = html.replace(
    '.ev-title { font-family:var(--ff-d); font-size:clamp(3.5rem,8vw,7rem); letter-spacing:-0.02em; line-height:0.88; margin-bottom:1rem; }',
    '.ev-title { font-family:var(--ff-d); font-size:clamp(3.5rem,8vw,7rem); letter-spacing:-0.02em; line-height:0.88; margin-bottom:0.5rem; }'
)
# Tighten ev-desc margin
html = html.replace(
    '.ev-desc { font-size:0.92rem; opacity:0.65; max-width:520px; font-style:italic; font-family:var(--ff-e); font-weight:400; line-height:1.6; margin-bottom:2rem; }',
    '.ev-desc { font-size:0.92rem; opacity:0.65; max-width:520px; font-style:italic; font-family:var(--ff-e); font-weight:400; line-height:1.6; margin-bottom:1.25rem; }'
)
print("Fix #5: Gallery header dead space reduced")

# ============================================================
# FIX #6 — Comment out stats section
# ============================================================
OLD_STATS = '''<!-- STATS -->
<section class="dk">
  <div class="stats-band reveal">
    <div class="stat" data-a="u"><span class="stat-v" data-count="1500">0</span><span class="stat-l">people in the room</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="1"><span class="stat-v" data-count="5">0</span><span class="stat-l">events, all sold out</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="2"><span class="stat-v">NYC</span><span class="stat-l">invite only</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="3"><span class="stat-v">Apr 25</span><span class="stat-l">next event</span></div>
  </div>
</section>'''

NEW_STATS = '''<!-- AUDIT FIX #6 — Stats section commented out (update numbers before restoring) -->
<!-- REMOVED: Stats section
<section class="dk">
  <div class="stats-band reveal">
    <div class="stat" data-a="u"><span class="stat-v" data-count="1500">0</span><span class="stat-l">people in the room</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="1"><span class="stat-v" data-count="5">0</span><span class="stat-l">events, all sold out</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="2"><span class="stat-v">NYC</span><span class="stat-l">invite only</span></div>
    <div class="stat-div"></div>
    <div class="stat" data-a="u" data-d="3"><span class="stat-v">Apr 25</span><span class="stat-l">next event</span></div>
  </div>
</section>
-->'''

if OLD_STATS in html:
    html = html.replace(OLD_STATS, NEW_STATS)
    print("Fix #6: Stats section commented out")
else:
    print("Fix #6 WARNING: Stats exact match not found")

# ============================================================
# FIX #7 — Eager-load first 8 Tribeca + 8 SoHo gallery images
# ============================================================
# Find the Tribeca gallery-visible section and change first 8 loading="lazy" to eager
# We'll do this by counting occurrences within the Tribeca visible block

def fix_eager_loading(html_content, section_id, count_eager, count_fetchpriority):
    """Change first N images in a gallery-visible section to eager loading."""
    vis_id = 'gallery-visible-' + section_id
    start_marker = '<div class="gallery-visible" id="' + vis_id + '">'
    end_marker = '</div>\n  <div class="gallery-collapsed"'
    
    start = html_content.find(start_marker)
    end = html_content.find(end_marker, start)
    if start == -1 or end == -1:
        print(f"  WARNING: Could not find {vis_id}")
        return html_content
    
    block = html_content[start:end]
    
    # Replace first count_eager instances of loading="lazy"
    replaced = 0
    new_block = block
    while replaced < count_eager:
        idx = new_block.find('loading="lazy"')
        if idx == -1:
            break
        new_block = new_block[:idx] + 'loading="eager"' + new_block[idx+14:]
        replaced += 1
    
    # Add fetchpriority="high" to first count_fetchpriority images
    fp_added = 0
    temp = new_block
    while fp_added < count_fetchpriority:
        idx = temp.find('<img src=')
        if idx == -1:
            break
        temp = temp[:idx] + '<img fetchpriority="high" src=' + temp[idx+9:]
        fp_added += 1
    new_block = temp
    
    return html_content[:start] + new_block + html_content[end:]

# Add AUDIT FIX comment before applying
html = html.replace(
    '<div class="gallery-visible" id="gallery-visible-tribeca-rooftop">',
    '<!-- AUDIT FIX #7 — First 8 Tribeca images eager-loaded, first 4 fetchpriority=high -->\n  <div class="gallery-visible" id="gallery-visible-tribeca-rooftop">'
)
html = html.replace(
    '<div class="gallery-visible" id="gallery-visible-soho-soiree">',
    '<!-- AUDIT FIX #7 — First 8 SoHo images eager-loaded -->\n  <div class="gallery-visible" id="gallery-visible-soho-soiree">'
)

html = fix_eager_loading(html, 'tribeca-rooftop', 8, 4)
html = fix_eager_loading(html, 'soho-soiree', 8, 0)
print("Fix #7: Eager loading applied to first 8 Tribeca + 8 SoHo images")

# ============================================================
# FIX #8 — Make sponsor photos larger in Why Sponsor section
# ============================================================
OLD_WHY_VIS = '''    <div class="why-vis" data-a="f" data-d="1" aria-hidden="true">
      <div class="why-vis-main">
        <img src="/img/dj.jpg" alt="DJ set at treehouse. NYC event — premium brand experience" loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
        <div class="if">treehouse.</div>
      </div>
      <div class="why-vis-sub">
        <div class="why-vs-item">
          <img src="/img/sp-may-sunglasses.jpg" alt="Golden hour couple with drinks at treehouse." loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">treehouse.</div>
        </div>
        <div class="why-vs-item">
          <img src="/img/sp-xmas-crowddrinks.jpg" alt="Crowd drinks raised at treehouse. holiday party" loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">treehouse.</div>
        </div>
      </div>
    </div>'''

NEW_WHY_VIS = '''    <!-- AUDIT FIX #8 — Sponsor photos enlarged: 55% width desktop, full-width mobile -->
    <div class="why-vis" data-a="f" data-d="1" aria-hidden="true">
      <div class="why-vis-main" style="aspect-ratio:3/2;">
        <img src="/img/sp-xmas-martini.jpg" alt="Sponsor product at treehouse. NYC event" loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
        <div class="if">treehouse.</div>
      </div>
      <div class="why-vis-sub" style="margin-top:6px;">
        <div class="why-vs-item" style="aspect-ratio:3/2;">
          <img src="/img/sp-may-sunglasses.jpg" alt="Golden hour couple with drinks at treehouse." loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">treehouse.</div>
        </div>
        <div class="why-vs-item" style="aspect-ratio:3/2;">
          <img src="/img/sp-xmas-crowddrinks.jpg" alt="Crowd drinks raised at treehouse. holiday party" loading="lazy" onerror="this.onerror=null;this.parentNode.classList.add('fail')">
          <div class="if">treehouse.</div>
        </div>
      </div>
    </div>'''

if OLD_WHY_VIS in html:
    html = html.replace(OLD_WHY_VIS, NEW_WHY_VIS)
    print("Fix #8: Sponsor photos enlarged")
else:
    print("Fix #8 WARNING: Why Sponsor vis block not found exactly")

# Also update the why-layout CSS to give more space to the visual column
html = html.replace(
    '.why-layout { display:grid; grid-template-columns:1fr 1fr; gap:6rem; align-items:start; }',
    '/* AUDIT FIX #8 — Sponsor section: visual column gets more width */\n.why-layout { display:grid; grid-template-columns:1fr 1.2fr; gap:4rem; align-items:start; }'
)

# ============================================================
# FIX #9 — Add scarcity line above email input
# ============================================================
OLD_JOIN_FORM = '''    <form class="join-form" action="https://formspree.io/f/xwpbkqod" method="POST" novalidate data-a="u" data-d="2">'''

NEW_JOIN_FORM = '''    <!-- AUDIT FIX #9 — Scarcity line above email form -->
    <p class="scarcity-line">April 25 · 75 Varick Rooftop · 300 guests · Waitlist open</p>
    <form class="join-form" action="https://formspree.io/f/xwpbkqod" method="POST" novalidate data-a="u" data-d="2">'''

if OLD_JOIN_FORM in html:
    html = html.replace(OLD_JOIN_FORM, NEW_JOIN_FORM)
    print("Fix #9: Scarcity line added above form")
else:
    print("Fix #9 WARNING: Join form start not found")

# Add scarcity-line CSS
SCARCITY_CSS = '''
/* AUDIT FIX #9 — Scarcity line */
.scarcity-line {
  font-family: var(--ff-b);
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.58;
  text-align: center;
  margin-bottom: 0.75rem;
  color: var(--accent);
}
'''
html = html.replace('/* ── JOIN ── */', SCARCITY_CSS + '\n/* ── JOIN ── */')

# ============================================================
# FIX #10 — Simplify nav to 3 links
# ============================================================
OLD_NAV_LINKS = '''  <div class="nav-links">
    <a href="#tribeca-rooftop">tribeca</a>
    <a href="#soho-soiree">soho</a>
    <a href="#christmas-nyc">christmas</a>
    <a href="#dinner-parties">dinner</a>
    <a href="#knox-day">knox</a>
    <a href="#west-village">west village</a>
    <a href="#tiers" class="hi">sponsor</a>
    <a href="#join">get tickets</a>
  </div>'''

NEW_NAV_LINKS = '''  <!-- AUDIT FIX #10 — Nav simplified to 3 links: Past Events | Sponsor | Get Tickets -->
  <div class="nav-links">
    <a href="#tribeca-rooftop">past events</a>
    <a href="#tiers" class="hi">sponsor</a>
    <a href="#join">get tickets</a>
  </div>'''

if OLD_NAV_LINKS in html:
    html = html.replace(OLD_NAV_LINKS, NEW_NAV_LINKS)
    print("Fix #10: Nav simplified to 3 links")
else:
    print("Fix #10 WARNING: Nav links block not found exactly")

# Also simplify mobile nav
OLD_MOB_NAV = '''  <nav>
    <a href="#tribeca-rooftop">tribeca</a>
    <a href="#soho-soiree">soho</a>
    <a href="#christmas-nyc">christmas</a>
    <a href="#dinner-parties">dinner</a>
    <a href="#knox-day">knox</a>
    <a href="#west-village">west village</a>
    <a href="#tiers">sponsor</a>
    <a href="#join">get tickets</a>
  </nav>'''

NEW_MOB_NAV = '''  <!-- AUDIT FIX #10 — Mobile nav simplified -->
  <nav>
    <a href="#tribeca-rooftop">past events</a>
    <a href="#tiers">sponsor</a>
    <a href="#join">get tickets</a>
  </nav>'''

if OLD_MOB_NAV in html:
    html = html.replace(OLD_MOB_NAV, NEW_MOB_NAV)
    print("Fix #10: Mobile nav simplified")

# ============================================================
# FIX #11 — Unify all gallery sections to dark theme
# ============================================================
# Change lt ev-section to dk ev-section for all gallery sections
import re

# Tribeca is lt, others may vary
html = html.replace('<section class="lt ev-section" id="tribeca-rooftop">', '<!-- AUDIT FIX #11 — Gallery unified to dark theme -->\n<section class="dk ev-section" id="tribeca-rooftop">')
html = html.replace('<section class="lt ev-section grain" id="christmas-nyc">', '<section class="dk ev-section grain" id="christmas-nyc">')
html = html.replace('<section class="lt ev-section" id="dinner-parties">', '<section class="dk ev-section" id="dinner-parties">')
html = html.replace('<section class="lt ev-section grain" id="knox-day">', '<section class="dk ev-section grain" id="knox-day">')
html = html.replace('<section class="lt ev-section" id="west-village">', '<section class="dk ev-section" id="west-village">')
# Also fix the btn-s color for dark sections (gallery "See Full Gallery" buttons)
# They already work on dk sections since btn-s uses currentColor
print("Fix #11: All gallery sections unified to dark theme")

# ============================================================
# FIX #12 — Add dates to event titles
# ============================================================
date_map = {
    'TRIBECA ROOFTOP': 'TRIBECA ROOFTOP · OCT 2024',
    'SOHO SOIREE': 'SOHO SOIREE · MAY 2024',
    'CHRISTMAS IN NYC': 'CHRISTMAS IN NYC · DEC 2024',
    'DINNER PARTIES': 'DINNER PARTIES · 2024',
    'KNOX DAY': 'KNOX DAY · JUL 2024',
    'WEST VILLAGE': 'WEST VILLAGE · 2024',
}

# Add AUDIT FIX comment before the first one
html = html.replace(
    '    <h2 class="ev-title">TRIBECA ROOFTOP</h2>',
    '    <!-- AUDIT FIX #12 — Dates added to all event titles -->\n    <h2 class="ev-title">TRIBECA ROOFTOP · OCT 2024</h2>'
)
html = html.replace('    <h2 class="ev-title">SOHO SOIREE</h2>', '    <h2 class="ev-title">SOHO SOIREE · MAY 2024</h2>')
html = html.replace('    <h2 class="ev-title">CHRISTMAS IN NYC</h2>', '    <h2 class="ev-title">CHRISTMAS IN NYC · DEC 2024</h2>')
html = html.replace('    <h2 class="ev-title">DINNER PARTIES</h2>', '    <h2 class="ev-title">DINNER PARTIES · 2024</h2>')
html = html.replace('    <h2 class="ev-title">KNOX DAY</h2>', '    <h2 class="ev-title">KNOX DAY · JUL 2024</h2>')
html = html.replace('    <h2 class="ev-title">WEST VILLAGE</h2>', '    <h2 class="ev-title">WEST VILLAGE · 2024</h2>')
print("Fix #12: Dates added to all event titles")

# ============================================================
# FIX #13 — Beef up footer
# ============================================================
OLD_FOOTER = '''<!-- FOOTER -->
<footer class="dk" role="contentinfo">
  <div class="foot-top">
    <a href="#hero" class="foot-logo" aria-label="treehouse. — back to top" title="Back to top">
      <img src="/img/logo.png" alt="treehouse. Events | New York City" height="80" style="filter:brightness(0) invert(1);">
    </a>
    <p class="foot-tag">Events · New York City</p>
  </div>
  <nav class="foot-links" aria-label="Footer links">
    <a href="https://www.instagram.com/treehouseevents.nyc" target="_blank" rel="noopener noreferrer" aria-label="Instagram @treehouseevents.nyc">@treehouseevents.nyc</a>
    <a href="mailto:events@tigertracks.ai" target="_blank" rel="noopener">events@tigertracks.ai</a>
    <a href="tel:+13016467758">(301) 646-7758</a>
  </nav>
  <div class="foot-btm">
    <p class="foot-copy">&copy; 2026 treehouse. events — new york city</p>
  </div>
</footer>'''

NEW_FOOTER = '''<!-- AUDIT FIX #13 — Footer beefed up: larger logo, thumbnail photos, scarcity line, Instagram icon -->
<!-- FOOTER -->
<footer class="dk" role="contentinfo">
  <!-- Thumbnail photo strip -->
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0;height:clamp(120px,15vw,200px);overflow:hidden;">
    <div style="overflow:hidden;"><img src="/img/gallery/tribeca-rooftop/tribeca-005.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/soho-soiree/soho-006.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/christmas-nyc/xmas-003.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
    <div style="overflow:hidden;"><img src="/img/gallery/knox-day/knox-001.jpg" alt="treehouse. NYC event" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.7;"></div>
  </div>
  <div class="foot-top" style="padding-top:3rem;">
    <a href="#hero" class="foot-logo" aria-label="treehouse. — back to top" title="Back to top">
      <img src="/img/logo.png" alt="treehouse. Events | New York City" height="120" style="filter:brightness(0) invert(1);">
    </a>
    <p class="foot-tag">Events · New York City</p>
    <!-- Next event scarcity line -->
    <p style="font-family:var(--ff-b);font-size:0.78rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent);opacity:0.85;margin-top:0.5rem;">April 25 · 75 Varick Rooftop · 300 guests · Waitlist open</p>
  </div>
  <nav class="foot-links" aria-label="Footer links">
    <!-- Instagram icon link -->
    <a href="https://www.instagram.com/treehouseevents.nyc" target="_blank" rel="noopener noreferrer" aria-label="Instagram @treehouseevents.nyc" style="display:inline-flex;align-items:center;gap:0.4rem;">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>
      @treehouseevents.nyc
    </a>
    <a href="mailto:events@tigertracks.ai" target="_blank" rel="noopener">events@tigertracks.ai</a>
    <a href="tel:+13016467758">(301) 646-7758</a>
  </nav>
  <div class="foot-btm">
    <p class="foot-copy">&copy; 2026 treehouse. events — new york city</p>
  </div>
</footer>'''

if OLD_FOOTER in html:
    html = html.replace(OLD_FOOTER, NEW_FOOTER)
    print("Fix #13: Footer beefed up")
else:
    print("Fix #13 WARNING: Footer exact match not found, trying partial")
    html = html.replace(
        '<footer class="dk" role="contentinfo">',
        '<!-- AUDIT FIX #13 — Footer beefed up -->\n<footer class="dk" role="contentinfo">'
    )
    html = html.replace(
        '      <img src="/img/logo.png" alt="treehouse. Events | New York City" height="80" style="filter:brightness(0) invert(1);">',
        '      <img src="/img/logo.png" alt="treehouse. Events | New York City" height="120" style="filter:brightness(0) invert(1);">'
    )
    print("Fix #13: Partial footer fix applied")

# ============================================================
# FIX #14 — Fix DJ section height: 85vh desktop, object-position center 40%
# ============================================================
# Find curate-section CSS and update
html = html.replace(
    '.curate-section { height:60vh; min-height:400px; }',
    '/* AUDIT FIX #14 — DJ section height: 85vh desktop, 70vh mobile */\n.curate-section { min-height:85vh; }\n@media(max-width:768px){ .curate-section { min-height:70vh; } }'
)
# Also update the dj-photo object-position
html = html.replace(
    'object-position:center bottom',
    'object-position:center 40%'
)
print("Fix #14: DJ section height set to 85vh, object-position center 40%")

# ============================================================
# FIX #15 — Font loading: confirm display=swap is in Google Fonts URL
# ============================================================
# The Google Fonts link already has &display=swap in it (line 19)
# Add font-display:swap to any inline @font-face if present
if '@font-face' in html:
    html = html.replace('@font-face {', '/* AUDIT FIX #15 */\n@font-face { font-display:swap;')
    print("Fix #15: font-display:swap added to @font-face declarations")
else:
    # Just confirm the Google Fonts URL has display=swap
    if 'display=swap' in html:
        html = html.replace(
            '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue',
            '<!-- AUDIT FIX #15 — font-display:swap confirmed via Google Fonts URL -->\n  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue'
        )
        print("Fix #15: Google Fonts display=swap confirmed")
    else:
        html = html.replace(
            'display=swap" rel="stylesheet">',
            'display=swap&display=swap" rel="stylesheet">'
        )
        print("Fix #15: display=swap added to Google Fonts URL")

# ============================================================
# Write output
# ============================================================
with open(BASE + '/index.html', 'w') as f:
    f.write(html)

print("\nAll fixes applied. index.html saved.")
