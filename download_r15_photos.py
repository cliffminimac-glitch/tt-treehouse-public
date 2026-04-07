import requests
import os

def gdrive_direct(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"

photos = [
    ("1TjzLjEZaaZbRwG6r_GUp0oEn7cqFY4fn", "img/tribeca-new-08.jpg"),
    # tribeca-new-09 from folder: 1CMMyzNvWUwdMBZeXED29NXHKDkFgOSJu — try first file in folder
    ("1VFNzZ0C9XuIakw13A1q0zhOOYWLq8ZKl", "img/soho-new-08.jpg"),
    ("1Sx-9Zpf3edm5dKAx7IvQTQyh4ZQrX7e0", "img/soho-new-09.jpg"),
    ("1G5BXEt2J45p_z5orS2vRvmNvo4gxH4Fs", "img/soho-new-10.jpg"),
    ("1btOEYVjU40bG5rQ62k1rl1QJfjDBNxP6", "img/xmas-new-02.jpg"),
    ("1RbZQOOZJK_mjVvJSpkU1QWrO1cSlLLEE", "img/xmas-new-03.jpg"),
    ("1SUoT6_VLyz2AiGudMQv00lAYFyAdpF-S", "img/xmas-new-04.jpg"),
]

session = requests.Session()
results = []

for file_id, dest in photos:
    url = gdrive_direct(file_id)
    try:
        r = session.get(url, stream=True, timeout=60, allow_redirects=True)
        r.raise_for_status()
        content = r.content
        # Check for Google Drive virus scan page
        if b'<!DOCTYPE html>' in content[:100]:
            # Try with confirm token
            import re
            token = re.search(rb'confirm=([0-9A-Za-z_\-]+)', content)
            if token:
                url2 = url + f"&confirm={token.group(1).decode()}"
                r = session.get(url2, stream=True, timeout=60)
                content = r.content
        
        with open(dest, 'wb') as f:
            f.write(content)
        size = os.path.getsize(dest)
        results.append((dest, size, 'OK'))
        print(f"  OK  {dest}  ({size:,} bytes)")
    except Exception as e:
        results.append((dest, 0, f'FAIL: {e}'))
        print(f"  FAIL {dest}: {e}")

print(f"\nDownloaded {sum(1 for _,_,s in results if s=='OK')}/{len(results)} files")
