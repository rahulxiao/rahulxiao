"""
Checks every image in README.md still loads.
Prints a markdown report; exits 1 if anything is broken.

    python .github/scripts/check_images.py README.md
"""
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

readme = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
root = readme.parent
text = readme.read_text(encoding="utf-8")

srcs = re.findall(r'<img[^>]+src="([^"]+)"', text) + re.findall(r'!\[[^\]]*\]\(([^)\s]+)', text)
seen, broken = set(), []

for src in srcs:
    if src in seen:
        continue
    seen.add(src)
    if src.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "profile-image-check", "Range": "bytes=0-1023"})
            with urllib.request.urlopen(req, timeout=30) as r:
                ctype = r.headers.get("Content-Type", "")
                if not ctype.startswith("image/") and "svg" not in ctype:
                    broken.append((src, f"not an image ({ctype or 'no content type'})"))
        except urllib.error.HTTPError as e:
            broken.append((src, f"HTTP {e.code}"))
        except Exception as e:  # timeouts, DNS, TLS
            broken.append((src, type(e).__name__))
    else:
        if not (root / src).is_file():
            broken.append((src, "file missing in repo"))

print(f"Checked {len(seen)} images.")
if broken:
    print("\n| image | problem |\n|---|---|")
    for src, why in broken:
        print(f"| `{src[:120]}` | {why} |")
    sys.exit(1)
print("All images load.")
