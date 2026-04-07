with open('index.html') as f:
    content = f.read()

original_len = len(content)
fixes = []

# ─────────────────────────────────────────────────────────────
# FIX #1a — Comment out Round 7 display:grid rule (L211-217)
# ─────────────────────────────────────────────────────────────
old_grid = """/* ROUND 7 FIX #2 — Restore display:grid square tiles (3-col desktop) */
.photo-grid,.gallery-visible,.gallery-collapsed {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
  margin:0;
  padding:0;
}"""

new_grid = """/* REMOVED R13: Round 7 display:grid rule replaced by CSS columns masonry (see ROUND 13 FIX #1 below) */
/* ROUND 7 FIX #2 — Restore display:grid square tiles (3-col desktop) */
/* .photo-grid,.gallery-visible,.gallery-collapsed {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
  margin:0;
  padding:0;
} */"""

if old_grid in content:
    content = content.replace(old_grid, new_grid)
    fixes.append('FIX #1a: Round 7 display:grid rule commented out')
else:
    print('ERROR: Round 7 grid rule not found exactly')

# ─────────────────────────────────────────────────────────────
# FIX #1b — Comment out Round 12 Block C (L550-553)
# ─────────────────────────────────────────────────────────────
old_r12 = """/* ── GALLERY EXPANDED FIX (Task 5) ── */
/* ROUND 7 FIX #6 — removed 75vh cap; max-height:9999px from base rule applies */
/* ROUND 7 FIX #3 — square tiles, cover crop */
/* ROUND 12 FIX #3 — removed aspect-ratio:1/1 so photos show at natural height, no cropping */
.gallery-item { overflow:hidden; }
/* ROUND 12 FIX #3 — height:auto + object-fit:unset so full photo always visible */
.gallery-item img { width:100%; height:auto; object-fit:unset; display:block; }"""

new_r12 = """/* ── GALLERY EXPANDED FIX (Task 5) ── */
/* ROUND 7 FIX #6 — removed 75vh cap; max-height:9999px from base rule applies */
/* ROUND 7 FIX #3 — square tiles, cover crop */
/* REMOVED R13: Round 12 FIX #3 standalone gallery-item rules replaced by ROUND 13 FIX #1 consolidated block */
/* ROUND 12 FIX #3 — removed aspect-ratio:1/1 so photos show at natural height, no cropping */
/* .gallery-item { overflow:hidden; } */
/* ROUND 12 FIX #3 — height:auto + object-fit:unset so full photo always visible */
/* .gallery-item img { width:100%; height:auto; object-fit:unset; display:block; } */"""

if old_r12 in content:
    content = content.replace(old_r12, new_r12)
    fixes.append('FIX #1b: Round 12 standalone gallery-item rules commented out')
else:
    print('ERROR: Round 12 gallery-item block not found exactly')

# ─────────────────────────────────────────────────────────────
# FIX #1c — Add consolidated CSS columns gallery rule
# ─────────────────────────────────────────────────────────────
# Insert after the commented-out Round 7 grid rule
insert_after = """/* REMOVED R13: Round 7 display:grid rule replaced by CSS columns masonry (see ROUND 13 FIX #1 below) */
/* ROUND 7 FIX #2 — Restore display:grid square tiles (3-col desktop) */
/* .photo-grid,.gallery-visible,.gallery-collapsed {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:2px;
  margin:0;
  padding:0;
} */"""

consolidated = """
/* ROUND 13 FIX #1 — consolidated gallery CSS: CSS columns masonry, natural aspect ratios, tight 6px gaps */
.photo-grid,
.gallery-visible,
.gallery-collapsed {
  display: block;
  column-count: 3;
  column-gap: 6px;
  margin: 0;
  padding: 0;
}
.photo-grid .gallery-item,
.gallery-visible .gallery-item,
.gallery-collapsed .gallery-item {
  break-inside: avoid;
  margin-bottom: 6px;
  overflow: hidden;
  background: #1a3a1a;
  cursor: zoom-in;
  position: relative;
  display: block;
}
.photo-grid .gallery-item img,
.gallery-visible .gallery-item img,
.gallery-collapsed .gallery-item img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}"""

if insert_after in content:
    content = content.replace(insert_after, insert_after + consolidated)
    fixes.append('FIX #1c: Consolidated CSS columns gallery rule added')
else:
    print('ERROR: insert_after anchor not found')

# ─────────────────────────────────────────────────────────────
# FIX #1d — Fix tablet media query (768px): grid -> column-count:2
# ─────────────────────────────────────────────────────────────
old_tablet = """  /* REMOVED R6: .photo-grid { grid-template-columns:repeat(2,1fr); gap:4px; padding:0 4px 4px; } */
  .photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:repeat(2,1fr); }
  .photo-grid .gallery-item,.gallery-visible .gallery-item,.gallery-collapsed .gallery-item { margin-bottom:4px; }"""

new_tablet = """  /* REMOVED R6: .photo-grid { grid-template-columns:repeat(2,1fr); gap:4px; padding:0 4px 4px; } */
  /* REMOVED R13: grid-template-columns tablet rule replaced by column-count */
  /* .photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:repeat(2,1fr); } */
  /* ROUND 13 FIX #1 tablet — 2 columns */
  .photo-grid,.gallery-visible,.gallery-collapsed { column-count:2; }
  .photo-grid .gallery-item,.gallery-visible .gallery-item,.gallery-collapsed .gallery-item { margin-bottom:4px; }"""

if old_tablet in content:
    content = content.replace(old_tablet, new_tablet)
    fixes.append('FIX #1d: Tablet media query updated to column-count:2')
else:
    print('ERROR: tablet media query not found exactly')

# ─────────────────────────────────────────────────────────────
# FIX #1e — Fix mobile media query (480px): grid -> column-count:1
# ─────────────────────────────────────────────────────────────
old_mobile = """  /* REMOVED R6: .photo-grid { grid-template-columns:1fr 1fr; } */
  /* ROUND 6 FIX — 1 col small mobile */
  .photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:1fr; }"""

new_mobile = """  /* REMOVED R6: .photo-grid { grid-template-columns:1fr 1fr; } */
  /* REMOVED R13: grid-template-columns mobile rule replaced by column-count */
  /* .photo-grid,.gallery-visible,.gallery-collapsed { grid-template-columns:1fr; } */
  /* ROUND 13 FIX #1 mobile — 1 column */
  .photo-grid,.gallery-visible,.gallery-collapsed { column-count:1; }"""

if old_mobile in content:
    content = content.replace(old_mobile, new_mobile)
    fixes.append('FIX #1e: Mobile media query updated to column-count:1')
else:
    print('ERROR: mobile media query not found exactly')

# ─────────────────────────────────────────────────────────────
# FIX #2 — Curate photo: full-bleed, cover, 55vh
# ─────────────────────────────────────────────────────────────
old_curate_img = """/* ROUND 12 FIX #5 — curate photo reduced to 45vh desktop (was max-height:none), full image still visible via object-fit:contain */
.curate-section .dj-photo { width:100%; height:auto; object-fit:contain; display:block; max-height:45vh; }"""

new_curate_img = """/* REMOVED R13: Round 12 FIX #5 curate contain/45vh replaced by full-bleed cover */
/* ROUND 13 FIX #2 — curate photo full-bleed cinematic strip: cover, 55vh, no side gutters */
.curate-section .dj-photo { width:100%; height:55vh; object-fit:cover; object-position:center; display:block; max-height:none; }"""

if old_curate_img in content:
    content = content.replace(old_curate_img, new_curate_img)
    fixes.append('FIX #2: Curate photo changed to full-bleed cover 55vh')
else:
    print('ERROR: curate img rule not found exactly')

# ─────────────────────────────────────────────────────────────
# FIX #3 — Curate section: add padding + overflow:hidden
# ─────────────────────────────────────────────────────────────
old_curate_section = """.curate-section { position:relative; width:100%; overflow:visible; }"""

new_curate_section = """/* ROUND 13 FIX #3 — curate section: 60px padding above/below for breathing room, overflow:hidden for full-bleed */
.curate-section { position:relative; width:100%; overflow:hidden; padding:60px 0; }"""

if old_curate_section in content:
    content = content.replace(old_curate_section, new_curate_section)
    fixes.append('FIX #3: Curate section padding:60px 0 added, overflow:hidden')
else:
    print('ERROR: curate section rule not found exactly')

# Also update mobile curate to remove the 55vw max-height (now using cover)
old_mob_curate = """/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */
/* ROUND 12 FIX #5 mobile — curate photo max-height on mobile */
@media(max-width:768px){ .curate-section { max-height:none; min-height:unset; overflow:visible; } .curate-section .dj-photo { max-height:55vw; } }"""

new_mob_curate = """/* ROUND 8 FIX #2c — mobile curate: natural height, full photo */
/* REMOVED R13: Round 12 mobile curate max-height replaced by cover approach */
/* ROUND 13 FIX #3 mobile — curate photo 45vh on mobile, full-bleed cover */
@media(max-width:768px){ .curate-section { padding:40px 0; } .curate-section .dj-photo { height:45vh; } }"""

if old_mob_curate in content:
    content = content.replace(old_mob_curate, new_mob_curate)
    fixes.append('FIX #3 mobile: Mobile curate updated to 45vh cover')
else:
    print('ERROR: mobile curate block not found exactly')

# ─────────────────────────────────────────────────────────────
# FINAL CHECKS
# ─────────────────────────────────────────────────────────────
assert '</html>' in content, 'ERROR: HTML truncated!'
assert 'column-count: 3' in content, 'ERROR: column-count:3 missing!'
assert 'height:55vh' in content or 'height: 55vh' in content, 'ERROR: curate 55vh missing!'
assert 'padding:60px 0' in content, 'ERROR: curate padding missing!'

print(f'Fixes applied ({len(fixes)}):')
for f in fixes:
    print(f'  ✓ {f}')
print(f'\nFile: {original_len} -> {len(content)} chars ({len(content)-original_len:+d})')

with open('index.html', 'w') as f:
    f.write(content)
print('Saved.')
