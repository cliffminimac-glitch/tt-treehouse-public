with open('index.html') as f:
    content = f.read()

fixes = []

# FIX #1a — Curate photo taller: 55vh to 72vh, object-position back to center center
old1 = '.curate-section .dj-photo { width:100%; height:55vh; object-fit:cover; object-position:center 70%; display:block; max-height:none; }'
new1 = '/* ROUND 17 FIX #1 -- taller curate photo: 72vh, object-position reset to center center so both sky and crowd visible */\n.curate-section .dj-photo { width:100%; height:72vh; object-fit:cover; object-position:center center; display:block; max-height:none; }'

if old1 in content:
    content = content.replace(old1, new1)
    fixes.append('FIX #1a: dj-photo height 55vh to 72vh, object-position center 70% to center center')
else:
    print('ERROR: dj-photo rule not found exactly')
    idx = content.find('height:55vh')
    print(f'Context: {content[idx-50:idx+80]}')

# FIX #1b — Mobile override: 45vh to 55vh
old1m = '.curate-section .dj-photo { height:45vh; }'
new1m = '.curate-section .dj-photo { height:55vh; } /* ROUND 17 FIX #1 -- mobile curate 45vh to 55vh */'
if old1m in content:
    content = content.replace(old1m, new1m)
    fixes.append('FIX #1b: mobile dj-photo height 45vh to 55vh')
else:
    print('ERROR: mobile dj-photo rule not found')
    idx = content.find('height:45vh')
    if idx >= 0:
        print(f'Context: {content[idx-80:idx+60]}')

# FIX #2a — Add ::before radial gradient to .curate-copy
old2a = '.curate-section .curate-copy { position:absolute; top:clamp(3rem,12vw,8rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }'
new2a = ('/* ROUND 17 FIX #2 -- curate-copy: add position:relative for ::before pseudo-element */\n'
         '.curate-section .curate-copy { position:absolute; top:clamp(3rem,12vw,8rem); left:50%; transform:translateX(-50%); text-align:center; color:#f0ede8; max-width:640px; padding:0 24px; width:100%; z-index:2; }\n'
         '/* ROUND 17 FIX #2 -- localized radial gradient behind text cluster only, not full image */\n'
         '.curate-copy::before { content:""; position:absolute; inset:-50px -80px; background:radial-gradient(ellipse at center, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0) 70%); border-radius:50%; z-index:-1; pointer-events:none; }')

if old2a in content:
    content = content.replace(old2a, new2a)
    fixes.append('FIX #2a: added ::before radial gradient to .curate-copy')
else:
    print('ERROR: curate-copy rule not found exactly')
    idx = content.find('.curate-section .curate-copy')
    print(f'Context: {content[idx:idx+200]}')

# FIX #2b — text-shadow on h2
old2b = ".curate-copy h2 { font-size:clamp(2rem,5vw,3.5rem); font-weight:700; margin-bottom:16px; color:#f0ede8; font-family:'Playfair Display',serif; }"
new2b = ("/* ROUND 17 FIX #2 -- text-shadow on heading for contrast */\n"
         ".curate-copy h2 { font-size:clamp(2rem,5vw,3.5rem); font-weight:700; margin-bottom:16px; color:#f0ede8; font-family:'Playfair Display',serif; text-shadow:0 2px 10px rgba(0,0,0,0.65); }")
if old2b in content:
    content = content.replace(old2b, new2b)
    fixes.append('FIX #2b: text-shadow added to curate-copy h2')
else:
    print('ERROR: curate-copy h2 rule not found exactly')
    idx = content.find('.curate-copy h2')
    print(f'Context: {content[idx:idx+150]}')

# FIX #2c — text-shadow on p
old2c = '.curate-copy p { font-size:1rem; line-height:1.7; color:rgba(240,237,232,0.85); margin-bottom:0; }'
new2c = ('/* ROUND 17 FIX #2 -- text-shadow on body copy */\n'
         '.curate-copy p { font-size:1rem; line-height:1.7; color:rgba(240,237,232,0.85); margin-bottom:0; text-shadow:0 1px 6px rgba(0,0,0,0.55); }')
if old2c in content:
    content = content.replace(old2c, new2c)
    fixes.append('FIX #2c: text-shadow added to curate-copy p')
else:
    print('ERROR: curate-copy p rule not found exactly')

# FIX #2d — darker tag background
old2d = '.curate-copy .tag { background:rgba(26,58,26,0.4); border-color:rgba(240,237,232,0.2); color:#f0ede8; }'
new2d = ('/* ROUND 17 FIX #2 -- darker tag background for legibility */\n'
         '.curate-copy .tag { background:rgba(0,0,0,0.35); border-color:rgba(240,237,232,0.3); color:#f0ede8; }')
if old2d in content:
    content = content.replace(old2d, new2d)
    fixes.append('FIX #2d: tag background darkened for contrast')
else:
    print('ERROR: curate-copy .tag rule not found exactly')

# FIX #3 — Remove hero tagline
old3 = '<p class="hero-sub" data-a="u" data-d="3">you already know someone who\'s been.</p>'
new3 = '<!-- REMOVED R17: hero tagline -- "you already know someone who\'s been." -->'
if old3 in content:
    content = content.replace(old3, new3)
    fixes.append('FIX #3: hero tagline commented out')
else:
    print('ERROR: hero tagline not found exactly')
    idx = content.find('you already know')
    print(f'Context: {content[idx-50:idx+80]}')

# VERIFY
assert '</html>' in content, 'ERROR: HTML truncated!'
assert 'height:72vh' in content, 'ERROR: 72vh missing!'
assert '::before' in content, 'ERROR: ::before missing!'
assert 'text-shadow:0 2px 10px' in content, 'ERROR: h2 text-shadow missing!'
assert 'REMOVED R17' in content, 'ERROR: hero tagline removal missing!'

print(f'\nFixes applied ({len(fixes)}):')
for f in fixes:
    print(f'  OK {f}')

with open('index.html', 'w') as f:
    f.write(content)
print('Saved.')
