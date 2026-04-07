import requests
import os

def download_gdrive(file_id, dest_path):
    """Download a Google Drive file by ID."""
    session = requests.Session()
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = session.get(url, stream=True)
    
    # Handle virus scan warning page
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
            response = session.get(url, stream=True)
            break
    
    # Also try with confirm=t
    if response.status_code == 200 and len(response.content) < 10000:
        url = f"https://drive.google.com/uc?export=download&confirm=t&id={file_id}"
        response = session.get(url, stream=True)
    
    if response.status_code != 200:
        return False, f"HTTP {response.status_code}"
    
    content = response.content
    if len(content) < 5000:
        return False, f"Too small ({len(content)} bytes) — likely an error page"
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(content)
    return True, len(content)

photos = [
    ("1rrx7w9G4incmOp6ngj99Nn25CdpfDSiG", "img/knox-new-01.jpg"),
    ("106usl9cPimsCx5PnCohpniN_kl9z8nGS", "img/knox-new-02.jpg"),
    ("1fbowsG3MFZ-FK4y3cc_zPt66zOJbyi9c", "img/tribeca-new-03.jpg"),
    ("1TbQ4uvXAUDZqvMfO92PjKmQRx0CgsgXu", "img/tribeca-new-04.jpg"),
    ("1cJPX0Sgy6KBHX1dCRJsV3fI1xE7Bx2uQ", "img/tribeca-new-05.jpg"),
    ("1RfYovzxHBtoLDrpLmz3RKZr9Q7gtfH1M", "img/tribeca-new-06.jpg"),
    ("1CcszY6gWuPFhKvrwXr7KnQNZsFnnC9TA", "img/tribeca-new-07.jpg"),
]

print("Downloading 7 photos...")
all_ok = True
for file_id, dest in photos:
    ok, result = download_gdrive(file_id, dest)
    if ok:
        print(f"  ✓ {dest} — {result:,} bytes")
    else:
        print(f"  ✗ {dest} — FAILED: {result}")
        all_ok = False

print()
if all_ok:
    print("All 7 downloads successful.")
else:
    print("SOME DOWNLOADS FAILED — do not proceed with code changes.")
