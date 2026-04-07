import requests
import os

def gdrive_download(file_id, dest_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
    session = requests.Session()
    resp = session.get(url, stream=True, timeout=120)
    # Handle virus scan warning page
    for key, val in resp.cookies.items():
        if 'download_warning' in key:
            url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={val}"
            resp = session.get(url, stream=True, timeout=120)
            break
    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content(32768):
            if chunk:
                f.write(chunk)
    size = os.path.getsize(dest_path)
    return size

assets = [
    ("1CroRIOIQF_3Lz9iTD9O0gJnUowH82uvC", "img/curate-video.mp4"),
    ("1zTQIU1SB4wFCGwjgGsk-Yiw0Rqq7zxWh", "img/footer-01.jpg"),
    ("1ajmWwsmg2J7VK7pk8aG6YTbZaTSYK4d3", "img/footer-02.jpg"),
    ("1t8NyXknPfKe5WvXKHx-ioyZzJW0IlgtP", "img/footer-03.jpg"),
    ("1Z7HPt8_cnKLzMdPAw3BkczJ906x-W-Uj", "img/footer-04.jpg"),
]

all_ok = True
for file_id, dest in assets:
    print(f"Downloading {dest}...", end=" ", flush=True)
    try:
        size = gdrive_download(file_id, dest)
        print(f"OK — {size:,} bytes")
        if size < 10000:
            print(f"  WARNING: file may be too small (possible download error)")
            all_ok = False
    except Exception as e:
        print(f"FAILED: {e}")
        all_ok = False

if all_ok:
    print("\nAll 5 assets downloaded successfully.")
else:
    print("\nERROR: One or more downloads failed. Stopping.")
