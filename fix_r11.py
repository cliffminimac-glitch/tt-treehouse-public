import re

with open('index.html') as f:
    html = f.read()

original_len = len(html)

# ── FIX #1 ── Comment out the why-vis-sub div (two images below video)
old_vis_sub = """      <!-- ROUND 4 FIX #5 — Restored why-vis-sub with 2 curated gallery photos -->
      <div class="why-vis-sub">
        <div style="overflow:hidden;border-radius:4px;aspect-ratio:4/3;">
          <img src="/img/gallery/soho-soiree/soho-004.jpg" alt="Crowd energy at treehouse. SoHo Soiree" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;transition:transform 0.5s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="overflow:hidden;border-radius:4px;aspect-ratio:4/3;">
          <img src="/img/gallery/tribeca-rooftop/tribeca-007.jpg" alt="Crowd dancing at golden hour, Tribeca Rooftop" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;transition:transform 0.5s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
        </div>
      </div>"""

new_vis_sub = """      <!-- REMOVED R11: sponsor section images below video (soho-004.jpg and tribeca-007.jpg in why-vis-sub) -->"""

if old_vis_sub in html:
    html = html.replace(old_vis_sub, new_vis_sub)
    print("✓ FIX #1: why-vis-sub images commented out")
else:
    print("ERROR: why-vis-sub block not found exactly")

# ── FIX #2 ── Update heading from pitch to past-partners
old_heading = """        <span class="lbl reveal-child" style="margin-bottom:1rem">// Why Sponsor</span>
        <h2>Your brand<br>in the<br>right room.</h2>"""

new_heading = """        <!-- ROUND 11 FIX #1 — heading updated to past-partners focus, label updated -->
        <span class="lbl reveal-child" style="margin-bottom:1rem">// Past Partners</span>
        <h2>In Good<br>Company.</h2>"""

if old_heading in html:
    html = html.replace(old_heading, new_heading)
    print("✓ FIX #2: heading updated to 'In Good Company.'")
else:
    print("ERROR: heading block not found exactly")

# ── FIX #3 ── Tone down the four numbered rows to a single credibility line
old_rows = """      <div class="why-rows">
        <div class="why-row" data-a="u">
          <span class="why-n">01</span>
          <p class="why-t">300–400 people per event. Not a mass audience — the right audience. The kind that actually tries new things.</p>
        </div>
        <div class="why-row" data-a="u" data-d="1">
          <span class="why-n">02</span>
          <p class="why-t">Your brand is part of the night, not a banner in the corner. People remember what they experienced, not what they saw.</p>
        </div>
        <div class="why-row" data-a="u" data-d="2">
          <span class="why-n">03</span>
          <p class="why-t">Our crowd documents everything. The photos are good, the reach is real, and the audience isn't bots.</p>
        </div>
        <div class="why-row" data-a="u" data-d="3">
          <span class="why-n">04</span>
          <p class="why-t">One sponsor per category per event. We turn brands away to protect the room. This is a limited slot.</p>
        </div>
      </div>"""

new_rows = """      <!-- ROUND 11 FIX #2 — four pitch-deck rows replaced with single credibility line -->
      <div class="why-rows">
        <div class="why-row" data-a="u">
          <p class="why-t" style="font-size:1.05rem;opacity:0.82;">18 brands across 5 events. Spirits, fashion, wellness, tech. The kind of crowd that actually remembers who sponsored the night.</p>
        </div>
      </div>"""

if old_rows in html:
    html = html.replace(old_rows, new_rows)
    print("✓ FIX #3: four pitch-deck rows replaced with single credibility line")
else:
    print("ERROR: why-rows block not found exactly")

# Sanity checks
assert '</html>' in html, "ERROR: HTML truncated!"
assert 'In Good' in html, "ERROR: new heading missing!"
assert 'why-vis-sub' not in html.replace('REMOVED R11', ''), "ERROR: why-vis-sub still active!"

with open('index.html', 'w') as f:
    f.write(html)

print(f"\nFile: {original_len} -> {len(html)} chars ({len(html)-original_len:+d})")
print(f"HTML complete: {'</html>' in html}")
print(f"Lines: {html.count(chr(10))}")
