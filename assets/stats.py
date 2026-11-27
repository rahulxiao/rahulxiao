"""
Draws stats.svg in the profile's own dawn style, from public data only:
the contribution calendar at github.com/users/<user>/contributions and
the public repo list. Runs daily in .github/workflows/snake.yml.

    python assets/stats.py rahulxiao dist/stats.svg
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SF Mono', Menlo, monospace"


def get(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-stats"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def calendar(user):
    html = get(f"https://github.com/users/{user}/contributions")
    dates = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)" id="(contribution-day-component-[\d-]+)"', html))
    dates = {v: k for k, v in dates.items()}  # id -> date
    days = {}
    for cid, txt in re.findall(r'<tool-tip[^>]*for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"(\d+) contribution", txt)
        if cid in dates:
            days[dates[cid]] = int(m.group(1)) if m else 0
    return dict(sorted(days.items()))


def stars(user, token):
    total, page = 0, 1
    while True:
        repos = json.loads(get(f"https://api.github.com/users/{user}/repos?per_page=100&page={page}", token))
        total += sum(r["stargazers_count"] for r in repos if not r["fork"])
        if len(repos) < 100:
            return total
        page += 1


def streaks(days):
    counts = list(days.values())
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    # today may have no contributions yet; that shouldn't break the streak
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    return current, longest


def render(days, star_count):
    W, H = 1200, 330
    total = sum(days.values())
    current, longest = streaks(days)
    items = list(days.items())
    weeks = [sum(c for _, c in items[i:i + 7]) for i in range(0, len(items), 7)]
    peak = max(weeks) or 1
    n = len(weeks)
    x0, cw, base, hmax = 56, (W - 112) / max(n, 1), 286, 92
    bars = "".join(
        f'<rect x="{x0 + i * cw + 1:.1f}" y="{base - max(3, w / peak * hmax):.1f}" width="{cw - 4:.1f}" '
        f'height="{max(3, w / peak * hmax):.1f}" rx="2" fill="{"#ffe7a8" if i == n - 1 else "url(#bar)"}" '
        f'opacity="{1 if w else .35}"/>'
        for i, w in enumerate(weeks)
    )
    blocks = [
        (f"{total:,}", "contributions this year"),
        (f"{current}", "day streak right now"),
        (f"{longest}", "longest streak this year"),
        (f"{star_count}", "stars on my repos"),
    ]
    stat = "".join(
        f'<text x="{56 + i * 280}" y="104" font-family="{SANS}" font-size="50" font-weight="800" fill="#fff">{v}</text>'
        f'<text x="{58 + i * 280}" y="134" font-family="{SANS}" font-size="18" fill="#f3dcff">{label}</text>'
        for i, (v, label) in enumerate(blocks)
    )
    updated = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{total} contributions this year, current streak {current} days, longest streak {longest} days, {star_count} stars.">
<style>.glow{{animation:g 3s ease-in-out infinite}}@keyframes g{{50%{{opacity:.55}}}}</style>
<defs>
  <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1d58"/><stop offset=".65" stop-color="#6b3374"/><stop offset="1" stop-color="#c8607a"/></linearGradient>
  <linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f472b6"/><stop offset="1" stop-color="#ffcf7a"/></linearGradient>
  <radialGradient id="sun"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#sbg)"/>
<circle cx="{W - 80}" cy="{H}" r="220" fill="url(#sun)" class="glow"/>
<text x="56" y="46" font-family="{MONO}" font-size="16" letter-spacing="5" fill="#ffd2e6">THE LAST 12 MONTHS</text>
<text x="{W - 56}" y="46" font-family="{MONO}" font-size="15" fill="#f3dcff" text-anchor="end">updated {updated}</text>
{stat}
<line x1="56" y1="{base + 2}" x2="{W - 56}" y2="{base + 2}" stroke="#fff" stroke-opacity=".25"/>
{bars}
<text x="56" y="{base + 28}" font-family="{MONO}" font-size="14" fill="#f3dcff" opacity=".85">one bar = one week</text>
<text x="{W - 56}" y="{base + 28}" font-family="{MONO}" font-size="14" fill="#ffe7a8" text-anchor="end">this week</text>
</svg>"""


if __name__ == "__main__":
    user, out = sys.argv[1], sys.argv[2]
    days = calendar(user)
    if len(days) < 300:
        sys.exit(f"calendar looks wrong: only {len(days)} days parsed")
    svg = render(days, stars(user, os.environ.get("GITHUB_TOKEN")))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", out)
