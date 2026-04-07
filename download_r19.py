#!/usr/bin/env python3
"""Download all 18 Round 19 assets"""
import urllib.request, os, time

def download_gdrive(file_id, dest, label):
    url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, 'wb') as f:
            f.write(r.read())
        size = os.path.getsize(dest)
        status = 'PASS' if size > 5000 else 'FAIL (too small)'
        print(f"  {status}: {dest} ({size:,} bytes) [{label}]")
        return size
    except Exception as e:
        print(f"  FAIL: {dest} — {e}")
        return 0

# Videos
download_gdrive('1d__o-GgL0T6PqlojgwW_H6VldvbRgml3', 'img/sponsor-hero-video-v2.mp4', 'hero video v2')
# Bottom video — same as current sponsor-bottom-video.mp4 (already downloaded)
# Per spec: "download from this folder" — use same file ID as sponsor-bottom-video
download_gdrive('19UMWx06ChC8xCjnWw82YbbSLnt1Btat8', 'img/sponsor-bottom-video-v2.mp4', 'bottom video v2')

# Brand logos
logos = [
    ('1b7znRKMqiHfk8NY_1ImGvvkbzbawv3-d', 'img/brand-logo-01.png'),
    ('1WEGI-sJvgBEUiZw5RWM8hZcNR7hNk3c6', 'img/brand-logo-02.png'),
    ('1WKVTf8ZSY1gXdrXmxZpy1-u6as0YF1um', 'img/brand-logo-03.png'),
    ('1TkC7srfoii_awSCbZmh4EwjL-rtRUcO9', 'img/brand-logo-04.png'),
    ('1MvqvW2uMXE6SqUGTyko5jV0H1Yqm4qDU', 'img/brand-logo-05.png'),
    ('1aULPtB7F8FH6NKSRRTyNvQ4yC7kNvyV4', 'img/brand-logo-06.png'),
    ('1E_v4uyqZvNoYuhBonTrSsqFw0HkUk9g8', 'img/brand-logo-07.png'),
    ('1ZPsYrUFvJcHhLW8ttiOtgZ6w22LhqHqf', 'img/brand-logo-08.png'),
    ('1y5Z6hmIt5cvwacqVJEi-BFSttM2Z89Cr', 'img/brand-logo-09.png'),
    ('1mCUvxaX123F0-LhoXJKv5h8r6W4bLmBU', 'img/brand-logo-10.png'),
    ('1V0S_Nu0OfIlZteVcoNmbUcdzNKVOrIIj', 'img/brand-logo-11.png'),
    ('1WpPwvI1GcCC7ru_kKM0DJqq0TLCu-tnD', 'img/brand-logo-12.png'),
    ('1Fdq9eNbb8Sh2V-SNXvQG2st5w-72yo7L', 'img/brand-logo-13.png'),
    ('1rc8AjsRnt7AQCOP4Nin3OOOmAf_gWsC9', 'img/brand-logo-14.png'),
    ('1NjzcA7JwDjZXCLC682qvZoDkYEnU3mti', 'img/brand-logo-15.png'),
    ('1XvuzgZFDtq6GswmQ7gFmGpOV82lnAYFQ', 'img/brand-logo-16.png'),
]

for file_id, dest in logos:
    download_gdrive(file_id, dest, 'logo')
    time.sleep(0.3)

print("\nDone.")
