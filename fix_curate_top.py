#!/usr/bin/env python3
"""Move curate text overlay to the upper/sky portion of the image"""

with open('index.html', 'r') as f:
    html = f.read()

# Change bottom-anchored to top-anchored (sky is in the upper portion of the image)
old_css = """.curate-section .curate-copy { position:absolute; bottom:clamp(2rem,5vw,4rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }"""

new_css = """/* ROUND 7 FIX #2 — text positioned in upper sky area of the image */
.curate-section .curate-copy { position:absolute; top:clamp(3rem,12vw,8rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }"""

# Also update the gradient to darken the top (sky) instead of the bottom
old_gradient = """.curate-section::after { content:''; position:absolute; inset:0; background:linear-gradient(to top, rgba(10,28,10,0.82) 0%, rgba(10,28,10,0.45) 50%, rgba(10,28,10,0.15) 100%); pointer-events:none; }"""

new_gradient = """/* Gradient darkens the sky at top for text legibility */
.curate-section::after { content:''; position:absolute; inset:0; background:linear-gradient(to bottom, rgba(10,28,10,0.65) 0%, rgba(10,28,10,0.3) 45%, rgba(10,28,10,0.05) 100%); pointer-events:none; }"""

if old_css in html:
    html = html.replace(old_css, new_css)
    print("curate-copy position updated")
else:
    print("ERROR: curate-copy CSS not found")
    exit(1)

if old_gradient in html:
    html = html.replace(old_gradient, new_gradient)
    print("gradient updated")
else:
    print("ERROR: gradient CSS not found")
    exit(1)

# Also fix the mobile rule - bottom:32px should become top:2rem
old_mobile = """  .curate-copy { bottom:32px; }"""
new_mobile = """  .curate-copy { top:2rem; bottom:auto; }"""
if old_mobile in html:
    html = html.replace(old_mobile, new_mobile)
    print("mobile rule updated")

with open('index.html', 'w') as f:
    f.write(html)

print(f"Done. File size: {len(html)} chars")
