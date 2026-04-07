#!/usr/bin/env python3
"""Restore text overlay on curate section big picture (Round 7 Fix)"""

with open('index.html', 'r') as f:
    html = f.read()

# 1. Replace the CSS: make curate-copy absolute over the image again, add gradient overlay
old_css = """/* ROUND 5 FIX #2B — removed height:85vh, min-height, overflow:hidden so image shows at full natural size */
.curate-section { position:relative; width:100%; }
/* ROUND 5 FIX #2C — image at full natural size, no cropping, no position offset */
.curate-section .dj-photo { width:100%; height:auto; display:block; } /* ROUND 2 FIX #3 */
/* ROUND 5 FIX #2D — REMOVED dark gradient overlay so photo colors are fully visible */
/* REMOVED R5: .curate-section .curate-overlay { position:absolute; inset:0; background:linear-gradient(...) } */
/* ROUND 5 FIX #2E — curate-copy now flows below the image (not absolute positioned over it) */
.curate-section .curate-copy { position:relative; text-align:center; color:#f0ede8; max-width:640px; padding:2rem 24px; width:100%; margin:0 auto; }"""

new_css = """/* ROUND 7 FIX — restore text overlay on curate section big picture */
.curate-section { position:relative; width:100%; overflow:hidden; }
.curate-section .dj-photo { width:100%; height:auto; display:block; }
/* Dark gradient so text is legible over the photo */
.curate-section::after { content:''; position:absolute; inset:0; background:linear-gradient(to top, rgba(10,28,10,0.82) 0%, rgba(10,28,10,0.45) 50%, rgba(10,28,10,0.15) 100%); pointer-events:none; }
/* Text positioned absolutely over the image, bottom-anchored */
.curate-section .curate-copy { position:absolute; bottom:clamp(2rem,5vw,4rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }"""

if old_css in html:
    html = html.replace(old_css, new_css)
    print("CSS updated")
else:
    print("ERROR: CSS block not found")
    exit(1)

with open('index.html', 'w') as f:
    f.write(html)

print(f"Done. File size: {len(html)} chars")
