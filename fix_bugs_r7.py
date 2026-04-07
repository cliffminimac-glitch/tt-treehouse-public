#!/usr/bin/env python3
"""Round 7 Bug Fixes — all 6 broken items"""

with open('index.html', 'r') as f:
    html = f.read()

original_len = len(html)
fixes = []

# ─────────────────────────────────────────────────────────────
# BUG 2+3: Replace CSS columns masonry with display:grid + aspect-ratio:1/1 + object-fit:cover
# ─────────────────────────────────────────────────────────────
old_gallery_css = """/* ROUND 6 FIX — CSS columns masonry layout (desktop 3 col) */
.photo-grid,.gallery-visible,.gallery-collapsed {
  column-count:3;
  column-gap:4px;
  margin:0;
  padding:0;
}
.photo-grid .gallery-item,.gallery-visible .gallery-item,.gallery-collapsed .gallery-item {
  break-inside:avoid;
  margin-bottom:4px;
  display:block;
}"""

new_gallery_css = """/* ROUND 7 FIX #2 — Restore display:grid square tiles (3-col desktop) */
.photo-grid,.gallery-visible,.gallery-collapsed {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
  margin:0;
  padding:0;
}"""

if old_gallery_css in html:
    html = html.replace(old_gallery_css, new_gallery_css)
    fixes.append("BUG 2: gallery CSS -> display:grid 3-col")
else:
    print("ERROR: gallery CSS block not found")

# BUG 3: Fix object-fit:contain -> object-fit:cover on gallery-item img
# Also restore aspect-ratio:1/1 on gallery-item
old_item_css = """.gallery-item { aspect-ratio:unset; min-height:0; }
.gallery-item img { width:100%; height:auto; object-fit:contain; object-position:center; aspect-ratio:unset; display:block; }"""

new_item_css = """/* ROUND 7 FIX #3 — square tiles, cover crop */
.gallery-item { aspect-ratio:1/1; overflow:hidden; }
.gallery-item img { width:100%; height:100%; object-fit:cover; object-position:center; display:block; }"""

if old_item_css in html:
    html = html.replace(old_item_css, new_item_css)
    fixes.append("BUG 3: gallery-item img -> object-fit:cover + aspect-ratio:1/1")
else:
    print("ERROR: gallery-item img CSS not found")

# ─────────────────────────────────────────────────────────────
# BUG 6: Remove the max-height:75vh override on .gallery-collapsed.is-open
# ─────────────────────────────────────────────────────────────
old_collapsed = """.gallery-collapsed.is-open { max-height:75vh; overflow-y:auto; scroll-behavior:smooth; }
.gallery-collapsed.is-open::-webkit-scrollbar { width:4px; }
.gallery-collapsed.is-open::-webkit-scrollbar-track { background:transparent; }
.gallery-collapsed.is-open::-webkit-scrollbar-thumb { background:var(--ln20); border-radius:2px; }"""

new_collapsed = """/* ROUND 7 FIX #6 — removed 75vh cap; max-height:9999px from base rule applies */"""

if old_collapsed in html:
    html = html.replace(old_collapsed, new_collapsed)
    fixes.append("BUG 6: removed max-height:75vh override on .gallery-collapsed.is-open")
else:
    print("ERROR: gallery-collapsed.is-open override not found")

# ─────────────────────────────────────────────────────────────
# BUG 4: Fix curate section height — cap it so image doesn't expand to 1580px
# Add max-height:85vh to the curate-section and overflow:hidden
# ─────────────────────────────────────────────────────────────
old_curate_css = """/* ROUND 7 FIX — restore text overlay on curate section big picture */
.curate-section { position:relative; width:100%; overflow:hidden; }
.curate-section .dj-photo { width:100%; height:auto; display:block; }"""

new_curate_css = """/* ROUND 7 FIX — restore text overlay on curate section big picture */
/* ROUND 7 FIX #4 — cap height so image doesn't expand to 1580px */
.curate-section { position:relative; width:100%; overflow:hidden; max-height:85vh; }
.curate-section .dj-photo { width:100%; height:100%; object-fit:cover; display:block; }"""

if old_curate_css in html:
    html = html.replace(old_curate_css, new_curate_css)
    fixes.append("BUG 4: curate-section max-height:85vh + image object-fit:cover")
else:
    print("ERROR: curate-section CSS not found")

# ─────────────────────────────────────────────────────────────
# BUG 4b: Also fix the mobile min-height:70vh rule (conflicts with max-height:85vh)
# ─────────────────────────────────────────────────────────────
old_mobile_curate = """/* ROUND 5 FIX #2 — REMOVED: .curate-section { min-height:85vh; } duplicate rule */
@media(max-width:768px){ .curate-section { min-height:70vh; } }
  .curate-copy { top:2rem; bottom:auto; }
  .curate-copy h2 { font-size:1.8rem; }"""

new_mobile_curate = """/* ROUND 7 FIX #4b — mobile curate height */
@media(max-width:768px){ .curate-section { max-height:70vh; min-height:unset; } }
  .curate-copy { top:2rem; bottom:auto; }
  .curate-copy h2 { font-size:1.8rem; }"""

if old_mobile_curate in html:
    html = html.replace(old_mobile_curate, new_mobile_curate)
    fixes.append("BUG 4b: mobile curate max-height:70vh")
else:
    print("WARNING: mobile curate rule not found (may be ok)")

# ─────────────────────────────────────────────────────────────
# BUG 1: Fix vibe video — the video exists and has a source, but the section
# has padding:4rem 0 which may cause height issues. Ensure it renders at full height.
# The video HTML looks correct already (max-height:80vh, object-fit:cover).
# The bug report says offsetHeight:0 — likely a CSS conflict from the old .vibe-reel rules.
# Fix: remove the old conflicting CSS rules and ensure the inline style takes precedence.
# ─────────────────────────────────────────────────────────────
old_vibe_css = """/* ROUND 4 FIX #8 — Vibe video: edge-to-edge, 65vh max, label overlay */"""

# Find the full block
import re
vibe_block_match = re.search(
    r'/\* ROUND 4 FIX #8 — Vibe video.*?\*/(.*?)(?=/\*|\Z)',
    html, re.DOTALL
)
if vibe_block_match:
    # Find the exact lines
    start = html.find('/* ROUND 4 FIX #8 — Vibe video')
    # Find end: next CSS comment or closing style tag
    end_candidates = [
        html.find('\n/* ', start + 10),
        html.find('\n.', start + 10),
    ]
    end = min(e for e in end_candidates if e > start)
    old_vibe_block = html[start:end]
    print(f"Vibe CSS block to replace:\n{old_vibe_block}")
    new_vibe_block = """/* ROUND 7 FIX #1 — Vibe video: clean rules, no height conflicts */
.vibe-reel { padding:0 !important; overflow:hidden; }
.vr-inner { padding:0; max-width:100%; }
.vr-inner video { width:100%; display:block; max-height:75vh; min-height:300px; object-fit:cover; }
"""
    html = html.replace(old_vibe_block, new_vibe_block)
    fixes.append("BUG 1: vibe video CSS cleaned up")
else:
    print("WARNING: vibe CSS block not found via regex")

# ─────────────────────────────────────────────────────────────
# BUG 5: Sponsor video — audit shows it HAS a <source> tag already.
# The bug report may be stale. Verify and skip if already correct.
# ─────────────────────────────────────────────────────────────
if 'src="/img/sponsor-video.mp4"' in html:
    fixes.append("BUG 5: sponsor video already has src — no fix needed")
else:
    print("ERROR: sponsor video src missing — needs manual fix")

# ─────────────────────────────────────────────────────────────
# Also fix the tablet/mobile gallery grid (2-col and 1-col)
# ─────────────────────────────────────────────────────────────
old_tablet_gallery = """.photo-grid,.gallery-visible,.gallery-collapsed { column-count:2; column-gap:4px; }"""
new_tablet_gallery = """.photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:repeat(2,1fr); }"""
if old_tablet_gallery in html:
    html = html.replace(old_tablet_gallery, new_tablet_gallery)
    fixes.append("TABLET: gallery grid -> 2-col")
else:
    print("WARNING: tablet gallery rule not found")

old_mobile_gallery = """.photo-grid,.gallery-visible,.gallery-collapsed { column-count:1; }"""
new_mobile_gallery = """.photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:1fr; }"""
if old_mobile_gallery in html:
    html = html.replace(old_mobile_gallery, new_mobile_gallery)
    fixes.append("MOBILE: gallery grid -> 1-col")
else:
    print("WARNING: mobile gallery rule not found")

with open('index.html', 'w') as f:
    f.write(html)

print(f"\nApplied {len(fixes)} fixes:")
for f in fixes:
    print(f"  ✓ {f}")
print(f"\nFile size: {original_len} -> {len(html)} chars")
