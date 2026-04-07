#!/usr/bin/env python3
"""Download all 10 new photos for Round 8 from Google Drive"""

import requests
import os

# Map of Google Drive file IDs to target filenames
photos = [
    ("14IZKULC_sdKkPsk5ro6HX_FGdtYT5eaW", "tribeca-new-01.jpg"),
    ("1VGNlb3TPb7pzn2dIMkA_a11lmxD-YTFH", "tribeca-new-02.jpg"),
    ("1fKhhif5yL7BiUE6wwONVaU9d-UKsPB6Y", "soho-new-01.jpg"),
    ("1uxHyXt4iUFEd_0Dd0gL8dKrgGdMyDQdw", "soho-new-02.jpg"),
    ("1RMT2gDouA0QlmlRbZ-tOL12V3ycaPR7w", "soho-new-03.jpg"),
    ("1lPJkWbqp0lSTZ9HGoK-opN8--Plr_zcn", "soho-new-04.jpg"),
    ("1Jfjkzyqes0pz6pkk5a5XQgnEOxv9qkW0", "soho-new-05.jpg"),
    ("18PrgF4eXCuyfgEUMhjC-69CHiqS85PHW", "soho-new-06.jpg"),
    ("1ep4dUCFMU4Jbk7ujE1PUBPdGIUvjljnk", "soho-new-07.jpg"),
    ("1wkIyjrQ8AhAZik4E6LsYkt7r9d_NekKb", "xmas-new-01.jpg"),
]

save_dir = "/home/ubuntu/tt-treehouse-public/img"
os.makedirs(save_dir, exist_ok=True)

session = requests.Session()
results = []

for file_id, filename in photos:
    save_path = os.path.join(save_dir, filename)
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        # First request to get the confirmation token for large files
        resp = session.get(url, stream=True, timeout=60)
        
        # Check for virus scan warning / confirmation page
        content_type = resp.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            # Need to follow the confirmation link
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Try to find the download form or direct link
            form = soup.find('form', id='download-form')
            if form:
                action = form.get('action', '')
                # Get all hidden inputs
                params = {}
                for inp in form.find_all('input'):
                    if inp.get('name'):
                        params[inp['name']] = inp.get('value', '')
                resp = session.get(action, params=params, stream=True, timeout=60)
            else:
                # Try direct download with confirm parameter
                resp = session.get(url + "&confirm=t", stream=True, timeout=60)
        
        # Save the file
        with open(save_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        
        size = os.path.getsize(save_path)
        if size < 5000:
            # Likely got an HTML error page, not an image
            with open(save_path, 'rb') as f:
                preview = f.read(200)
            results.append((filename, "FAIL", f"File too small ({size} bytes), likely HTML: {preview[:100]}"))
        else:
            results.append((filename, "OK", f"{size:,} bytes"))
    except Exception as e:
        results.append((filename, "FAIL", str(e)))

print("Download results:")
all_ok = True
for filename, status, info in results:
    print(f"  [{status}] {filename}: {info}")
    if status != "OK":
        all_ok = False

if all_ok:
    print("\nAll 10 photos downloaded successfully.")
else:
    print("\nSOME DOWNLOADS FAILED — stopping.")
