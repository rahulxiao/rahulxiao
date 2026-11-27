"""
Builds every SVG in this folder. Hand-drawn shapes, no images, system fonts only,
so GitHub renders them crisp and animated.

    python assets/generate.py

Edit the text constants below, re-run, commit.
"""
import random
from pathlib import Path

OUT = Path(__file__).parent

# palette — midnight over a city, power lines, lantern windows
NIGHT = "#0b0a1f"
INK = "#120f2a"
INK2 = "#1a1538"
VIOLET = "#3b2a6b"
DUSK = "#7a2f6e"
SAKURA = "#f9a8d4"
SAKURA_D = "#f472b6"
CYAN = "#67e8f9"
LANTERN = "#ffcf7a"
MOON = "#fff4e0"
MUTED = "#a99fc9"

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SF Mono', Menlo, monospace"
JP = "'Yu Gothic UI', 'Yu Gothic', 'Hiragino Sans', 'Noto Sans JP', Meiryo, sans-serif"

# hero japanese: name, then the vertical line on the right
JP_NAME = "ラフル・ビスワス"
JP_SLEEP = "もう寝る時間"        # "it's already time to sleep"
JP_SLEEP_2 = "でもあと一行だけ"   # "...but just one more line"


def petal_path():
    # one sakura petal with the little notch at the tip
    return "M0,-7 C4,-6 6,-1 4,4 C3,6 1,7 0,5.5 C-1,7 -3,6 -4,4 C-6,-1 -4,-6 0,-7Z"


def petals(rng, n, w, h, colors=(SAKURA, "#fbcfe8", SAKURA_D)):
    out = []
    for i in range(n):
        x = rng.uniform(0, w * 1.15)
        dur = rng.uniform(9, 17)
        delay = -rng.uniform(0, dur)
        drift = rng.uniform(-260, -120)
        s = rng.uniform(0.6, 1.25)
        c = rng.choice(colors)
        op = rng.uniform(0.55, 0.95)
        out.append(
            f'<g transform="translate({x:.0f},0)"><g class="fall" style="--dx:{drift:.0f}px;--h:{h + 40}px;'
            f'animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">'
            f'<path d="{petal_path()}" fill="{c}" opacity="{op:.2f}" transform="scale({s:.2f})" class="spin" '
            f'style="animation-duration:{rng.uniform(2.5, 5):.1f}s"/></g></g>'
        )
    return "\n".join(out)


PETAL_CSS = """
.fall{animation-name:fall;animation-timing-function:linear;animation-iteration-count:infinite}
.spin{transform-box:fill-box;transform-origin:center;animation:spin linear infinite}
@keyframes fall{0%{transform:translate(0,-30px)}25%{transform:translate(calc(var(--dx)*.2),calc(var(--h)*.25)) }
50%{transform:translate(calc(var(--dx)*.55),calc(var(--h)*.5))}75%{transform:translate(calc(var(--dx)*.75),calc(var(--h)*.75))}
100%{transform:translate(var(--dx),var(--h))}}
@keyframes spin{0%{transform:rotate(0) scaleX(1)}50%{transform:rotate(180deg) scaleX(.35)}100%{transform:rotate(360deg) scaleX(1)}}
"""


def skyline(rng, w, base, top_min, top_max, color, win_color, lit=0.18, flicker=0.04, seed_off=0):
    """row of buildings with lantern-coloured windows, a few of them flickering"""
    parts, x = [], -10
    while x < w + 10:
        bw = rng.randint(38, 96)
        bh = rng.randint(top_min, top_max)
        y = base - bh
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh + 200}" fill="{color}"/>')
        if rng.random() < 0.25:  # rooftop water tank / antenna
            if rng.random() < 0.5:
                parts.append(f'<rect x="{x + bw * 0.6:.0f}" y="{y - 12}" width="14" height="12" fill="{color}"/>')
            else:
                parts.append(f'<rect x="{x + bw * 0.3:.0f}" y="{y - 22}" width="2" height="22" fill="{color}"/>')
        for wy in range(y + 8, base + 120, 11):
            for wx in range(x + 6, x + bw - 8, 10):
                r = rng.random()
                if r < lit:
                    cls = ' class="flick"' if r < flicker else ""
                    d = f' style="animation-delay:{rng.uniform(0, 6):.1f}s"' if cls else ""
                    parts.append(f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="{win_color}" opacity="{rng.uniform(.5, .95):.2f}"{cls}{d}/>')
        x += bw + rng.randint(0, 6)
    return "\n".join(parts)


def stars(rng, n, w, h):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.choice([0.6, 0.8, 1, 1.3])
        tw = rng.random() < 0.35
        cls = f' class="tw" style="animation-delay:{rng.uniform(0, 4):.1f}s;animation-duration:{rng.uniform(2.5, 5):.1f}s"' if tw else ""
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{rng.uniform(.3, .9):.2f}"{cls}/>')
    return "\n".join(out)


def pole(x, top, base, color):
    """japanese utility pole: tall post, two crossarms, insulators"""
    return f"""
<g fill="{color}">
  <rect x="{x - 4}" y="{top}" width="8" height="{base - top + 50}"/>
  <rect x="{x - 46}" y="{top + 18}" width="92" height="5"/>
  <rect x="{x - 34}" y="{top + 44}" width="68" height="4"/>
  <rect x="{x - 42}" y="{top + 11}" width="4" height="8"/><rect x="{x - 2}" y="{top + 11}" width="4" height="8"/><rect x="{x + 38}" y="{top + 11}" width="4" height="8"/>
  <rect x="{x - 30}" y="{top + 38}" width="4" height="7"/><rect x="{x + 26}" y="{top + 38}" width="4" height="7"/>
  <rect x="{x - 14}" y="{top + 70}" width="28" height="34" rx="3"/>
  <rect x="{x + 4}" y="{top + 120}" width="22" height="3"/>
</g>"""


# ───────────────────────────── hero ─────────────────────────────
def hero():
    W, H = 1200, 440
    rng = random.Random(7)
    px = 760  # pole x
    pt = 92   # pole top
    wires = [
        (f"M-20,{pt + 60} Q{px / 2:.0f},{pt + 110} {px - 42},{pt + 11}", "w1"),
        (f"M-20,{pt + 92} Q{px / 2:.0f},{pt + 140} {px - 30},{pt + 38}", "w2"),
        (f"M{px + 42},{pt + 11} Q{(px + W) / 2:.0f},{pt + 80} {W + 20},{pt + 30}", "w3"),
        (f"M{px},{pt + 11} Q{(px + W) / 2:.0f},{pt + 105} {W + 20},{pt + 62}", "w4"),
        (f"M{px + 30},{pt + 38} Q{(px + W) / 2:.0f},{pt + 120} {W + 20},{pt + 100}", "w5"),
    ]
    wire_svg = "\n".join(f'<path id="{i}" d="{d}" fill="none" stroke="#06050f" stroke-width="1.6"/>' for d, i in wires)
    # little packets of data running along the lines
    pulses = "".join(
        f'<circle r="2.6" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="{d}s" begin="{b}s" repeatCount="indefinite" keyPoints="{kp}" keyTimes="0;1" calcMode="linear"><mpath href="#{i}"/></animateMotion></circle>'
        for i, d, b, kp in [("w1", 5, 0, "0;1"), ("w4", 6.5, 1.2, "0;1"), ("w2", 7, 3, "1;0"), ("w5", 5.5, 2.2, "0;1")]
    )

    # rooftop + girl-or-guy-in-hoodie silhouette with laptop, plus a cat
    roof_y = 352
    sx = 1010

    def strand(p0, p1, p2, n, delay0):
        # string of rooftop fairy lights hanging along a quadratic curve
        pts = []
        for k in range(1, n + 1):
            t = k / (n + 1)
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            c = [LANTERN, SAKURA, "#fde68a"][k % 3]
            pts.append(f'<circle cx="{x:.1f}" cy="{y + 3:.1f}" r="2.6" fill="{c}" filter="url(#glow)" class="bulb" style="animation-delay:{delay0 + k * .35:.2f}s"/>')
        return (f'<path d="M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="none" stroke="#06050f" stroke-width="1.2"/>'
                + "".join(pts))

    lights = (
        f'<rect x="1190" y="{roof_y - 92}" width="3" height="92" fill="#06050f"/>'
        f'<rect x="896" y="{roof_y - 84}" width="3" height="84" fill="#06050f"/>'
        + strand((1191, roof_y - 90), (1130, roof_y - 40), (1076, roof_y - 42), 7, 0)
        + strand((898, roof_y - 82), (930, roof_y - 40), (966, roof_y - 42), 4, .9)
    )
    sitter = f"""
<g fill="#06050f">
  <rect x="890" y="{roof_y}" width="320" height="120"/>
  <rect x="890" y="{roof_y - 10}" width="320" height="10"/>
  <rect x="900" y="{roof_y - 36}" width="2" height="26"/><rect x="940" y="{roof_y - 36}" width="2" height="26"/>
  <rect x="980" y="{roof_y - 36}" width="2" height="26"/><rect x="1180" y="{roof_y - 36}" width="2" height="26"/>
  <rect x="896" y="{roof_y - 38}" width="290" height="3"/>
  <rect x="896" y="{roof_y - 24}" width="290" height="2"/>
</g>
<!-- laptop light spilling forward -->
<ellipse cx="{sx - 22}" cy="{roof_y - 22}" rx="38" ry="26" fill="url(#screen)" class="glowpulse"/>
<g fill="#06050f" stroke="#7d6bb8" stroke-opacity=".55" stroke-width="1.4" stroke-linejoin="round">
  <!-- hood + head -->
  <path d="M{sx - 13},{roof_y - 70} C{sx - 14},{roof_y - 88} {sx + 12},{roof_y - 92} {sx + 14},{roof_y - 72} C{sx + 15},{roof_y - 62} {sx + 10},{roof_y - 56} {sx},{roof_y - 55} C{sx - 9},{roof_y - 56} {sx - 13},{roof_y - 62} {sx - 13},{roof_y - 70}Z"/>
  <!-- back, hunched toward the screen -->
  <path d="M{sx - 10},{roof_y - 60} C{sx - 26},{roof_y - 52} {sx - 26},{roof_y - 28} {sx - 22},{roof_y - 12} L{sx + 22},{roof_y - 12} C{sx + 26},{roof_y - 30} {sx + 22},{roof_y - 54} {sx + 10},{roof_y - 60}Z"/>
  <!-- legs hanging over the edge -->
  <path d="M{sx - 20},{roof_y - 14} L{sx - 30},{roof_y - 10} L{sx - 34},{roof_y + 16} L{sx - 27},{roof_y + 17} L{sx - 23},{roof_y - 2}Z"/>
  <path d="M{sx - 6},{roof_y - 14} L{sx - 14},{roof_y - 10} L{sx - 16},{roof_y + 18} L{sx - 9},{roof_y + 18} L{sx - 6},{roof_y}Z"/>
  <!-- laptop -->
  <path d="M{sx - 44},{roof_y - 13} L{sx - 18},{roof_y - 13} L{sx - 24},{roof_y - 34} L{sx - 46},{roof_y - 30}Z"/>
</g>
<path d="M{sx - 43},{roof_y - 15} L{sx - 26},{roof_y - 15} L{sx - 30},{roof_y - 31} L{sx - 44.5},{roof_y - 28.5}Z" fill="{CYAN}" opacity=".9" class="glowpulse"/>
<!-- cat -->
<g fill="#06050f" stroke="#7d6bb8" stroke-opacity=".55" stroke-width="1.2" transform="translate({sx + 58},{roof_y - 10})">
  <path d="M-10,0 C-12,-14 -6,-22 2,-22 C10,-22 14,-14 12,0Z"/>
  <path d="M-4,-20 L-6,-34 L2,-26 L8,-34 L8,-20Z" transform="translate(0,4)"/>
  <circle cx="1" cy="-24" r="8"/>
  <path d="M-6,-30 L-8,-38 L-1,-32Z"/><path d="M3,-32 L9,-38 L8,-30Z"/>
  <path class="tail" d="M10,-2 C22,-2 26,6 22,18" fill="none" stroke="#06050f" stroke-width="3.2" stroke-linecap="round"/>
</g>
<!-- the cat is asleep even if I'm not -->
<g font-family="{SANS}" font-weight="700" fill="{MUTED}">
  <text x="{sx + 66}" y="{roof_y - 40}" font-size="11" class="zz" style="animation-delay:0s">z</text>
  <text x="{sx + 66}" y="{roof_y - 40}" font-size="14" class="zz" style="animation-delay:1.3s">z</text>
  <text x="{sx + 66}" y="{roof_y - 40}" font-size="17" class="zz" style="animation-delay:2.6s">Z</text>
</g>
<!-- mug of something warm -->
<g transform="translate({sx + 30},{roof_y - 12})">
  <rect x="-5" y="-11" width="10" height="11" rx="2" fill="#06050f" stroke="#7d6bb8" stroke-opacity=".6"/>
  <path d="M5,-8 q5,0 5,4 q0,3 -5,3" fill="none" stroke="#06050f" stroke-width="2"/>
  <path class="steam" d="M-2,-14 q-3,-5 0,-9 q3,-4 0,-9" fill="none" stroke="#e9e3ff" stroke-width="1.4" stroke-linecap="round"/>
  <path class="steam" style="animation-delay:1.2s" d="M2,-14 q3,-5 0,-9 q-3,-4 0,-9" fill="none" stroke="#e9e3ff" stroke-width="1.4" stroke-linecap="round"/>
</g>
{lights}
"""

    back = skyline(rng, W, 400, 60, 170, INK2, "#ffcf7a", lit=0.10, flicker=0.02)
    front = skyline(rng, 900, 420, 30, 110, INK, LANTERN, lit=0.2, flicker=0.05)

    # vertical japanese, written top to bottom one character at a time
    vertical = "".join(
        f'<text x="1160" y="{62 + i * 30}" font-family="{JP}" font-size="24" font-weight="600" fill="{SAKURA}" '
        f'text-anchor="middle" class="jp" style="animation-delay:{.6 + i * .18:.2f}s">{c}</text>'
        for i, c in enumerate(JP_SLEEP)
    ) + "".join(
        f'<text x="1124" y="{82 + i * 24}" font-family="{JP}" font-size="18" fill="#cbbff0" opacity=".8" '
        f'text-anchor="middle" class="jp" style="animation-delay:{1.9 + i * .14:.2f}s">{c}</text>'
        for i, c in enumerate(JP_SLEEP_2)
    ) + '<rect x="1143" y="58" width="1.5" height="226" fill="#f472b6" opacity=".35"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rahul Biswas — full-stack developer building apps, web and systems, coding on a rooftop at midnight">
<style>
{PETAL_CSS}
.tw{{animation:tw ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.15}}to{{opacity:1}}}}
.flick{{animation:flick 6s steps(1) infinite}}@keyframes flick{{0%,100%{{opacity:.9}}40%{{opacity:.15}}43%{{opacity:.9}}70%{{opacity:.2}}72%{{opacity:.9}}}}
.glowpulse{{animation:gp 3.2s ease-in-out infinite}}@keyframes gp{{0%,100%{{opacity:.75}}50%{{opacity:1}}}}
.tail{{transform-box:fill-box;transform-origin:0 0;animation:tail 2.8s ease-in-out infinite}}@keyframes tail{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-14deg)}}}}
.cursor{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.rise{{animation:rise 1.2s cubic-bezier(.2,.8,.2,1) both}}@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.zz{{animation:zz 3.9s ease-out infinite;opacity:0}}@keyframes zz{{0%{{opacity:0;transform:translate(0,0)}}20%{{opacity:.9}}100%{{opacity:0;transform:translate(14px,-34px)}}}}
.steam{{animation:steam 2.4s ease-out infinite;opacity:0}}@keyframes steam{{0%{{opacity:0;transform:translateY(4px)}}30%{{opacity:.6}}100%{{opacity:0;transform:translateY(-10px)}}}}
.bulb{{animation:bulb 2.6s ease-in-out infinite alternate}}@keyframes bulb{{from{{opacity:.35}}to{{opacity:1}}}}
.shoot{{animation:shoot 9s ease-out infinite;opacity:0}}@keyframes shoot{{0%{{opacity:0;transform:translate(0,0)}}2%{{opacity:1}}9%{{opacity:0;transform:translate(-230px,84px)}}100%{{opacity:0;transform:translate(-230px,84px)}}}}
.plane{{animation:plane 48s linear infinite}}@keyframes plane{{from{{transform:translateX(0)}}to{{transform:translateX(-1320px)}}}}
.strobe{{animation:blink 1.2s steps(1) infinite}}
.haze{{animation:haze 22s ease-in-out infinite alternate}}@keyframes haze{{to{{transform:translateX(-70px)}}}}
.jp{{animation:jp .8s ease-out both}}@keyframes jp{{from{{opacity:0;transform:translateY(-8px)}}to{{opacity:1;transform:none}}}}
</style>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NIGHT}"/><stop offset=".45" stop-color="#1d1642"/>
    <stop offset=".78" stop-color="#4a2462"/><stop offset="1" stop-color="{DUSK}"/>
  </linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="{MOON}" stop-opacity=".45"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
  <radialGradient id="screen"><stop offset="0" stop-color="{CYAN}" stop-opacity=".5"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="2.5"/></filter>
  <linearGradient id="trail" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars(rng, 90, W, 260)}
<circle cx="960" cy="118" r="150" fill="url(#halo)"/>
<circle cx="960" cy="118" r="54" fill="{MOON}"/>
<circle cx="944" cy="104" r="9" fill="#f1e3c8" opacity=".6"/><circle cx="975" cy="134" r="6" fill="#f1e3c8" opacity=".5"/><circle cx="982" cy="100" r="4" fill="#f1e3c8" opacity=".5"/>
<!-- thin clouds sliding across the moon -->
<g class="haze" fill="#2a2052" opacity=".7" filter="url(#soft)">
  <rect x="890" y="128" width="190" height="9" rx="5"/><rect x="930" y="140" width="120" height="6" rx="3"/>
  <rect x="980" y="92" width="130" height="6" rx="3"/>
</g>
<!-- shooting stars -->
<g class="shoot"><path d="M660,34 l70,-26" stroke="url(#trail)" stroke-width="2" stroke-linecap="round"/><circle cx="660" cy="34" r="1.8" fill="#fff"/></g>
<g class="shoot" style="animation-delay:4.6s"><path d="M1120,40 l60,-22" stroke="url(#trail)" stroke-width="1.6" stroke-linecap="round"/><circle cx="1120" cy="40" r="1.5" fill="#fff"/></g>
<!-- a late flight crossing the sky -->
<g class="plane"><g transform="translate(1240,54)">
  <path d="M0,0 l14,-1 l4,-3 l2,0 l-2,4 l6,0 l0,2 l-24,0z" fill="#3b2a6b"/>
  <circle cx="0" cy="1" r="1.4" fill="#f87171" class="strobe"/><circle cx="22" cy="-3" r="1.2" fill="#fff" class="strobe" style="animation-delay:.6s"/>
</g></g>
{back}
{pole(px, pt, 400, "#06050f")}
{wire_svg}
{pulses}
<!-- crow on the wire -->
<path d="M352,207 c2,-6 8,-8 12,-6 l6,-3 l-2,5 c3,2 3,6 0,8 l-14,1z" fill="#06050f"/>
{front}
{sitter}
{petals(rng, 26, W, H)}
<rect width="{W}" height="{H}" fill="none" stroke="{SAKURA}" stroke-opacity=".25" stroke-width="2" rx="18"/>
</g>
<g class="rise">
  <text x="72" y="72" font-family="{MONO}" font-size="17" letter-spacing="5" fill="{MUTED}">00:00 · MIDNIGHT</text>
  <text x="72" y="118" font-family="{JP}" font-size="24" font-weight="600" letter-spacing="7" fill="{SAKURA}">{JP_NAME}</text>
  <text x="70" y="190" font-family="{SANS}" font-size="72" font-weight="800" letter-spacing="1" fill="#fff">Rahul Biswas</text>
  <rect x="72" y="208" width="64" height="4" rx="2" fill="{SAKURA_D}"/>
  <text x="72" y="246" font-family="{SANS}" font-size="26" fill="#e9e3ff">full-stack developer · apps, web &amp; systems</text>
  <text x="72" y="284" font-family="{MONO}" font-size="20" fill="{CYAN}">&gt; up late building something new<tspan class="cursor">_</tspan></text>
</g>
{vertical}
</svg>"""
    (OUT / "hero.svg").write_text(svg, encoding="utf-8")



import textwrap


def lines(txt, x, y, width=36, size=16, gap=24, color="#ddd6fe"):
    out = "".join(
        f'<text x="{x}" y="{y + i * gap}" font-family="{SANS}" font-size="{size}" fill="{color}">{l}</text>'
        for i, l in enumerate(textwrap.wrap(txt, width))
    )
    return out.replace("&", "&amp;")


# ───────────── time headers: the sky gets lighter as you scroll ─────────────
# (file name, clock, title, subtitle, left colour, right colour, progress 0→1)
HEADERS = [
    ("t0100", "01:00", "Who's this?", "the short version", 0.06),
    ("t0230", "02:30", "What keeps me up", "three things I'd do for free", 0.19),
    ("t0315", "03:15", "Late-night thoughts", "things I say when I should be asleep", 0.32),
    ("t0400", "04:00", "What I build with", "the tools in my bag", 0.45),
    ("t0445", "04:45", "Quest log", "cleared, in progress, and still locked", 0.58),
    ("t0530", "05:30", "Next stop", "the part where I leave the desk", 0.72),
    ("t0615", "06:15", "Training log", "commits, a 3D skyline, and two hungry arcade games", 0.88),
]


def mix(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def header(fname, clock, title, sub, t):
    c1 = mix("#0d0b24", "#2a1d58", t)
    c2 = mix("#1b1640", "#e0866f", t ** 1.4)
    W, H = 1200, 110
    rng = random.Random(fname)
    sky_top = mix("#0b0a1f", "#6aa8e8", t ** 1.6)
    sky_low = mix("#2a1d52", "#ffb88a", t)
    moon = (960 + t * 170, 34 + t * 78)
    sun = (1110, 108 - t * 62)
    star_op = max(0, 1 - t * 1.4)
    sx = "".join(
        f'<circle cx="{rng.uniform(905, 1165):.0f}" cy="{rng.uniform(22, 70):.0f}" r=".8" fill="#fff" opacity="{star_op * rng.uniform(.4, 1):.2f}"/>'
        for _ in range(14)
    )
    city = "".join(
        f'<rect x="{x}" y="{88 - h}" width="{w}" height="{h + 10}" fill="{mix("#06050f", "#5b5f9a", t)}"/>'
        for x, w, h in [(900, 22, 14), (920, 16, 24), (934, 28, 10), (960, 18, 20), (976, 30, 8), (1004, 14, 28),
                        (1016, 26, 12), (1040, 20, 18), (1058, 34, 9), (1090, 16, 22), (1104, 28, 14), (1130, 20, 26), (1148, 30, 11)]
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{clock} — {title}">
<style>
.in{{animation:in 1s .3s ease-out both}}@keyframes in{{from{{opacity:0;transform:translateX(-16px)}}to{{opacity:1;transform:none}}}}
.wipe{{animation:wipe 1.4s cubic-bezier(.7,0,.2,1) both}}@keyframes wipe{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.breathe{{animation:br 4s ease-in-out infinite}}@keyframes br{{50%{{opacity:.6}}}}
</style>
<defs>
  <linearGradient id="bg{fname}"><stop offset="0" stop-color="{c1}"/><stop offset=".55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <linearGradient id="sk{fname}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_top}"/><stop offset="1" stop-color="{sky_low}"/></linearGradient>
  <linearGradient id="ln{fname}"><stop offset="0" stop-color="{SAKURA_D}"/><stop offset=".7" stop-color="{mix(CYAN, LANTERN, t)}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <radialGradient id="sg{fname}"><stop offset="0" stop-color="#ffd27a" stop-opacity=".8"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
  <clipPath id="cl{fname}"><rect x="896" y="18" width="274" height="74" rx="10"/></clipPath>
</defs>
<rect x="0" y="12" width="{W}" height="86" rx="14" fill="url(#bg{fname})"/>
<rect x="0" y="12" width="8" height="86" rx="4" fill="{SAKURA_D}"/>
<rect x="8" y="94" width="{W - 8}" height="3" fill="url(#ln{fname})"/>
<text x="38" y="66" font-family="{MONO}" font-size="26" font-weight="700" fill="{SAKURA}">{clock}</text>
<line x1="138" y1="34" x2="138" y2="80" stroke="#fff" stroke-opacity=".2"/>
<text x="160" y="58" font-family="{SANS}" font-size="34" font-weight="800" fill="#fff">{title}</text>
<text x="161" y="84" font-family="{SANS}" font-size="19" font-style="italic" fill="#d6cff2">{sub}</text>
<g clip-path="url(#cl{fname})">
  <rect x="896" y="18" width="274" height="74" fill="url(#sk{fname})"/>
  {sx}
  <circle cx="{sun[0]}" cy="{sun[1]:.0f}" r="34" fill="url(#sg{fname})" class="breathe"/>
  <circle cx="{sun[0]}" cy="{sun[1]:.0f}" r="10" fill="#ffe7a8"/>
  <circle cx="{moon[0]:.0f}" cy="{moon[1]:.0f}" r="9" fill="{MOON}" opacity="{max(.15, 1 - t):.2f}"/>
  {city}
</g>
<rect x="896" y="18" width="274" height="74" rx="10" fill="none" stroke="#fff" stroke-opacity=".15"/>
</svg>"""
    (OUT / f"{fname}.svg").write_text(svg, encoding="utf-8")


# ───────────────────────── 02:30 — what I love ─────────────────────────
LOVES = [
    ("APPS & WEB", "Idea to real thing",
     "Websites, mobile apps and small tools. When something annoys me, I'd rather build the fix than wait for one."),
    ("SYSTEMS", "Under the hood",
     "APIs, databases, servers and deploys. I like making the invisible parts fast, reliable and easy to maintain."),
    ("TRAVELING", "Somewhere new",
     "New places, new food, new people. It's the best reset button I know, and I come back full of ideas."),
]


def icon_gamepad():
    return f"""
<path d="M-62,-18 Q-62,-34 -46,-34 H46 Q62,-34 62,-18 L70,22 Q74,42 54,42 Q42,42 34,26 H-34 Q-42,42 -54,42 Q-74,42 -70,22Z" fill="{INK2}" stroke="{SAKURA_D}" stroke-width="2"/>
<rect x="-46" y="-10" width="26" height="8" rx="2" fill="{SAKURA}"/><rect x="-37" y="-19" width="8" height="26" rx="2" fill="{SAKURA}"/>
<circle cx="36" cy="-16" r="6" fill="{CYAN}" class="press" style="animation-delay:0s"/>
<circle cx="48" cy="-4" r="6" fill="{SAKURA_D}" class="press" style="animation-delay:.4s"/>
<circle cx="24" cy="-4" r="6" fill="{LANTERN}" class="press" style="animation-delay:.8s"/>
<circle cx="36" cy="8" r="6" fill="#a78bfa" class="press" style="animation-delay:1.2s"/>
<rect x="-10" y="-14" width="8" height="4" rx="2" fill="{MUTED}"/><rect x="2" y="-14" width="8" height="4" rx="2" fill="{MUTED}"/>
<g class="up" style="animation-delay:0s"><rect x="58" y="-52" width="5" height="5" fill="{LANTERN}"/></g>
<g class="up" style="animation-delay:1.1s"><rect x="-70" y="-48" width="4" height="4" fill="{CYAN}"/></g>
<g class="up" style="animation-delay:2s"><rect x="10" y="-58" width="4" height="4" fill="{SAKURA}"/></g>"""


def icon_terminal():
    code = [(0, 54, SAKURA), (12, 72, CYAN), (12, 40, "#ddd6fe"), (24, 60, LANTERN), (0, 30, SAKURA)]
    rows = "".join(
        f'<rect x="{-58 + ind}" y="{-14 + i * 11}" width="{w}" height="5" rx="2" fill="{c}" class="type" style="animation-delay:{i * .5:.1f}s"/>'
        for i, (ind, w, c) in enumerate(code)
    )
    return f"""
<rect x="-72" y="-44" width="144" height="92" rx="9" fill="{NIGHT}" stroke="{CYAN}" stroke-width="2"/>
<rect x="-72" y="-44" width="144" height="18" rx="9" fill="{INK2}"/><rect x="-72" y="-32" width="144" height="6" fill="{INK2}"/>
<circle cx="-60" cy="-35" r="3" fill="#f87171"/><circle cx="-50" cy="-35" r="3" fill="{LANTERN}"/><circle cx="-40" cy="-35" r="3" fill="#4ade80"/>
{rows}
<rect x="-58" y="41" width="8" height="2" fill="{CYAN}" class="blink"/>"""


def icon_server():
    units = "".join(
        f'<rect x="-54" y="{-40 + k * 28}" width="108" height="22" rx="4" fill="{INK2}" stroke="{VIOLET}" stroke-width="1.5"/>'
        f'<rect x="-44" y="{-32 + k * 28}" width="40" height="3" rx="1.5" fill="#4c3d85"/>'
        f'<rect x="-44" y="{-26 + k * 28}" width="28" height="3" rx="1.5" fill="#4c3d85"/>'
        f'<circle cx="30" cy="{-29 + k * 28}" r="3.2" fill="#4ade80" class="led" style="animation-delay:{k * .45:.2f}s"/>'
        f'<circle cx="42" cy="{-29 + k * 28}" r="3.2" fill="{CYAN}" class="led" style="animation-delay:{.2 + k * .3:.2f}s"/>'
        for k in range(3)
    )
    return f"""
{units}
<path d="M-54,46 H54" stroke="{SAKURA}" stroke-width="2" stroke-dasharray="4 6" class="route"/>"""


def icon_map():
    return f"""
<path d="M-72,-32 L-24,-42 L24,-32 L72,-42 L72,38 L24,48 L-24,38 L-72,48Z" fill="{INK2}" stroke="{VIOLET}" stroke-width="2"/>
<path d="M-24,-42 L-24,38 M24,-32 L24,48" stroke="{VIOLET}" stroke-width="2"/>
<path d="M-56,-10 q10,-14 22,-6" fill="none" stroke="#4c3d85" stroke-width="2"/>
<path d="M30,20 q14,6 30,-4" fill="none" stroke="#4c3d85" stroke-width="2"/>
<path d="M-52,30 C-30,10 -10,34 6,8 S40,-8 46,-18" fill="none" stroke="{SAKURA}" stroke-width="2.5" stroke-dasharray="6 6" class="route"/>
<circle cx="-52" cy="30" r="4" fill="{CYAN}"/>
<g class="bob"><path d="M46,-20 c-9,0 -14,-7 -14,-13 a14,14 0 0 1 28,0 c0,6 -5,13 -14,13z" transform="translate(0,-8)" fill="{SAKURA_D}"/><circle cx="46" cy="-41" r="4.5" fill="{NIGHT}"/></g>"""


def loves():
    W, H = 1200, 452
    rng = random.Random(230)
    cw, gap = 360, 24
    icons = [icon_terminal(), icon_server(), icon_map()]
    cards = []
    for i, ((kick, title, body), ic) in enumerate(zip(LOVES, icons)):
        x = 24 + i * (cw + gap)
        cards.append(f"""
<g transform="translate({x},24)"><g>
  <rect width="{cw}" height="404" rx="16" fill="#110d2a" fill-opacity=".85" stroke="#3b2a6b"/>
  <rect x="1" y="1" width="{cw - 2}" height="150" rx="15" fill="#1a1440"/>
  <g transform="translate({cw / 2},84)">{ic}</g>
  <text x="28" y="194" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{SAKURA}">{kick.replace("&", "&amp;")}</text>
  <text x="28" y="228" font-family="{SANS}" font-size="27" font-weight="800" fill="#fff">{title}</text>
  {lines(body, 28, 266, width=28, size=19, gap=27)}
</g></g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="What I love: apps and web, systems, and traveling.">
<style>
.press{{transform-box:fill-box;transform-origin:center;animation:press 1.6s ease-in-out infinite}}@keyframes press{{0%,70%,100%{{transform:scale(1)}}80%{{transform:scale(.7)}}}}
.up{{animation:up 3s linear infinite}}@keyframes up{{from{{transform:translateY(10px);opacity:0}}30%{{opacity:1}}to{{transform:translateY(-26px);opacity:0}}}}
.type{{transform-box:fill-box;transform-origin:left;animation:type 4s steps(8) infinite}}@keyframes type{{0%{{transform:scaleX(0)}}25%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
.blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.led{{animation:led 1.1s steps(1) infinite}}@keyframes led{{60%{{opacity:.25}}}}
.route{{animation:route 1.5s linear infinite}}@keyframes route{{to{{stroke-dashoffset:-24}}}}
.bob{{animation:bob 1.8s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-6px)}}}}
.tw{{animation:tw 3s ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.1}}}}
</style>
<defs><linearGradient id="lbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120f2c"/><stop offset="1" stop-color="#2b1f56"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#lbg)"/>
{stars(rng, 40, W, H)}
{''.join(cards)}
</svg>"""
    (OUT / "loves.svg").write_text(svg, encoding="utf-8")


# ───────────────────────── 05:30 — the dawn train ─────────────────────────
def journey():
    W, H = 1200, 360
    rng = random.Random(530)
    ground = 286
    cars = []
    for c in range(4):
        cx = c * 158
        win = "".join(
            f'<rect x="{cx + 14 + k * 22}" y="{ground - 36}" width="13" height="11" rx="2" fill="{LANTERN}" opacity="{rng.uniform(.6, 1):.2f}"/>'
            for k in range(6)
        )
        cars.append(f'<rect x="{cx}" y="{ground - 46}" width="150" height="36" rx="5" fill="#140b22"/>{win}'
                    f'<rect x="{cx + 150}" y="{ground - 32}" width="8" height="10" fill="#140b22"/>')
    nose = (f'<path d="M{4 * 158 - 8},{ground - 46} h26 q26,0 32,36 h-58z" fill="#140b22"/>'
            f'<path d="M{4 * 158 + 18},{ground - 42} q16,2 22,18 h-22z" fill="{LANTERN}" opacity=".9"/>')
    train = "".join(cars) + nose
    poles = "".join(
        f'<rect x="{x}" y="{ground - 120}" width="5" height="120" fill="#1a0f2a"/><rect x="{x - 14}" y="{ground - 112}" width="33" height="4" fill="#1a0f2a"/>'
        for x in range(60, W, 220)
    )
    wires = "".join(
        f'<path d="M{x + 2},{ground - 110} Q{x + 112},{ground - 92} {x + 222},{ground - 110}" stroke="#1a0f2a" stroke-width="1.4" fill="none"/>'
        for x in range(60 - 220, W, 220)
    )
    sleepers = "".join(f'<rect x="{x}" y="{ground - 4}" width="14" height="3" fill="#2a1a40"/>' for x in range(0, W, 26))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A night train crossing the hills at dawn. Next stop: somewhere I have not been yet.">
<style>
{PETAL_CSS}
.train{{animation:train 18s linear infinite}}@keyframes train{{from{{transform:translateX(-720px)}}to{{transform:translateX(1260px)}}}}
.sun{{animation:sun 6s ease-in-out infinite alternate}}@keyframes sun{{from{{opacity:.75}}to{{opacity:1}}}}
.tw{{animation:tw 3s ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.05}}}}
.drift{{animation:drift 40s linear infinite alternate}}@keyframes drift{{to{{transform:translateX(60px)}}}}
.rise{{animation:rise 1.2s cubic-bezier(.2,.8,.2,1) both}}@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
</style>
<defs>
  <linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1d1642"/><stop offset=".45" stop-color="#5b2f73"/><stop offset=".72" stop-color="#c2577f"/><stop offset="1" stop-color="#f6a173"/>
  </linearGradient>
  <radialGradient id="sunglow"><stop offset="0" stop-color="#ffe0a3" stop-opacity=".9"/><stop offset=".35" stop-color="#ffb37a" stop-opacity=".45"/><stop offset="1" stop-color="#ff8a7a" stop-opacity="0"/></radialGradient>
  <clipPath id="jc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#jc)">
<rect width="{W}" height="{H}" fill="url(#dawn)"/>
{stars(rng, 30, W, 110)}
<circle cx="840" cy="250" r="230" fill="url(#sunglow)" class="sun"/>
<circle cx="840" cy="250" r="54" fill="#ffe7b0"/>
<g class="drift" fill="#f9b6c8" opacity=".35">
  <rect x="560" y="196" width="220" height="5" rx="3"/><rect x="620" y="207" width="160" height="4" rx="2"/>
  <rect x="900" y="178" width="240" height="5" rx="3"/><rect x="960" y="189" width="120" height="4" rx="2"/>
</g>
<path d="M0,250 L90,200 L170,232 L270,180 L380,228 L470,196 L560,236 L700,214 L800,240 L930,198 L1040,232 L1130,206 L1200,226 L1200,{H} L0,{H}Z" fill="#6a2f66" opacity=".75"/>
<path d="M0,268 L120,236 L240,262 L360,230 L500,264 L640,244 L760,266 L900,240 L1040,264 L1200,246 L1200,{H} L0,{H}Z" fill="#3a1d4a"/>
{wires}
{poles}
<g class="train">{train}</g>
<rect x="0" y="{ground - 10}" width="{W}" height="4" fill="#0f0818"/>
<rect x="0" y="{ground - 6}" width="{W}" height="{H}" fill="#1c0f2c"/>
{sleepers}
{petals(rng, 12, W, H)}
</g>
<g>
  <text x="64" y="90" font-family="{MONO}" font-size="20" letter-spacing="6" fill="#ffd2e6">NEXT STOP</text>
  <text x="62" y="146" font-family="{SANS}" font-size="44" font-weight="800" fill="#fff">somewhere I haven&#8217;t been yet</text>
</g>
</svg>"""
    (OUT / "journey.svg").write_text(svg, encoding="utf-8")


# ───────────────────────── 07:00 — good morning ─────────────────────────
def morning():
    W, H = 1200, 280
    rng = random.Random(700)
    rays = "".join(
        f'<path d="M0,0 L-7,-150 L7,-150Z" transform="rotate({a})" fill="#fff6cf"/>' for a in range(0, 360, 24)
    )
    birds = "".join(
        f'<g class="bird" style="animation-duration:{d}s;animation-delay:{dl}s"><g transform="translate(0,{y})">'
        f'<path class="flap" d="M-9,0 Q-4,-6 0,0 Q4,-6 9,0" fill="none" stroke="#3b3570" stroke-width="2" stroke-linecap="round"/></g></g>'
        for y, d, dl in [(70, 22, 0), (92, 26, -8), (60, 30, -15), (110, 24, -4)]
    )
    clouds = "".join(
        f'<g class="cloud" style="animation-duration:{d}s;animation-delay:{dl}s" fill="#fff" opacity=".85">'
        f'<ellipse cx="0" cy="{y}" rx="{r * 2.2:.0f}" ry="{r * .7:.0f}"/><circle cx="{-r * .6:.0f}" cy="{y - r * .4:.0f}" r="{r * .7:.0f}"/><circle cx="{r * .5:.0f}" cy="{y - r * .5:.0f}" r="{r * .85:.0f}"/></g>'
        for y, r, d, dl in [(70, 22, 70, 0), (120, 16, 90, -40), (50, 14, 80, -60)]
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Good morning. See you in the next commit.">
<style>
{PETAL_CSS}
.rays{{transform-box:view-box;transform-origin:960px 96px;animation:rays 60s linear infinite}}@keyframes rays{{to{{transform:rotate(360deg)}}}}
.cloud{{animation:cloud linear infinite}}@keyframes cloud{{from{{transform:translateX(-150px)}}to{{transform:translateX(1350px)}}}}
.bird{{animation:bird linear infinite}}@keyframes bird{{from{{transform:translateX(-40px)}}to{{transform:translateX(1260px)}}}}
.flap{{transform-box:fill-box;transform-origin:center;animation:flap .5s ease-in-out infinite alternate}}@keyframes flap{{to{{transform:scaleY(-.6)}}}}
.rise{{animation:rise 1.2s cubic-bezier(.2,.8,.2,1) both}}@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
</style>
<defs>
  <linearGradient id="am" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8cc8f7"/><stop offset=".6" stop-color="#cfe3f7"/><stop offset="1" stop-color="#ffdcb0"/></linearGradient>
  <radialGradient id="amsun"><stop offset="0" stop-color="#fff7d6"/><stop offset="1" stop-color="#fff7d6" stop-opacity="0"/></radialGradient>
  <clipPath id="mc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#mc)">
<rect width="{W}" height="{H}" fill="url(#am)"/>
<g class="rays" opacity=".35"><g transform="translate(960,96)">{rays}</g></g>
<circle cx="960" cy="96" r="120" fill="url(#amsun)"/>
<circle cx="960" cy="96" r="42" fill="#fff3c4"/>
{clouds}
{birds}
{skyline(rng, W, H - 40, 30, 120, "#a9b3e0", "#fff", lit=0)}
{skyline(rng, W, H, 20, 80, "#7b84c2", "#fff", lit=0)}
{petals(rng, 12, W, H)}
</g>
<g>
  <text x="64" y="84" font-family="{MONO}" font-size="20" letter-spacing="6" fill="#7a3a8c">07:00 · GOOD MORNING</text>
  <text x="62" y="140" font-family="{SANS}" font-size="44" font-weight="800" fill="#1a1538">see you in the next commit<tspan fill="{SAKURA_D}" dx="14">&#10140;</tspan></text>
</g>
<rect width="{W}" height="{H}" rx="18" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="2"/>
</svg>"""
    (OUT / "morning.svg").write_text(svg, encoding="utf-8")


# ───────────────────── 03:15 — visual-novel dialogue box ─────────────────────
DIALOGUE = [
    "It's 3 AM. The bug is gone. I have no idea what I changed.",
    "One more feature, one more fix, one more deploy. Then I'll sleep.",
    "It works on my machine. Shipping my machine is the next feature.",
]


def dialogue():
    W, H = 1200, 330
    rng = random.Random(315)
    slot = 5  # seconds each line stays on screen
    total = slot * len(DIALOGUE)
    box = "#120d2b"
    groups = []
    for i, line in enumerate(DIALOGUE):
        d = -((total - i * slot) % total)
        groups.append(f"""
<g class="slot" style="animation-delay:{d}s">
  <text x="96" y="262" font-family="{SANS}" font-size="25" fill="#f5f0ff">{line.replace("&", "&amp;")}</text>
  <rect x="80" y="232" width="1060" height="44" fill="{box}" class="cover" style="animation-delay:{d}s"/>
</g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A visual-novel dialogue box. Rahul says: {' / '.join(DIALOGUE).replace("'", "&#39;")}">
<style>
.slot{{animation:slot {total}s linear infinite}}
@keyframes slot{{0%,31%{{opacity:1}}33.4%,100%{{opacity:0}}}}
.cover{{animation:cover {total}s steps(40) infinite}}
@keyframes cover{{0%{{transform:translateX(0)}}14%,100%{{transform:translateX(1080px)}}}}
.next{{animation:next 1s ease-in-out infinite}}@keyframes next{{50%{{transform:translateY(5px)}}}}
.curtain{{transform-box:fill-box;transform-origin:top;animation:curtain 6s ease-in-out infinite}}@keyframes curtain{{50%{{transform:skewX(3deg)}}}}
.lamp{{animation:lamp 4s ease-in-out infinite}}@keyframes lamp{{50%{{opacity:.7}}}}
.tw{{animation:tw 3s ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.1}}}}
.glowpulse{{animation:gp 3.2s ease-in-out infinite}}@keyframes gp{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
</style>
<defs>
  <linearGradient id="room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#17123a"/><stop offset="1" stop-color="#241848"/></linearGradient>
  <linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a1f"/><stop offset="1" stop-color="#3a1f5c"/></linearGradient>
  <radialGradient id="lampg"><stop offset="0" stop-color="{LANTERN}" stop-opacity=".45"/><stop offset="1" stop-color="{LANTERN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="face"><stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <clipPath id="dc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="wc"><rect x="120" y="34" width="300" height="160" rx="4"/></clipPath>
</defs>
<g clip-path="url(#dc)">
<rect width="{W}" height="{H}" fill="url(#room)"/>
<!-- window to the night outside -->
<g clip-path="url(#wc)">
  <rect x="120" y="34" width="300" height="160" fill="url(#win)"/>
  {''.join(f'<circle cx="{rng.uniform(125, 415):.0f}" cy="{rng.uniform(40, 150):.0f}" r=".9" fill="#fff" class="tw" style="animation-delay:{rng.uniform(0, 3):.1f}s"/>' for _ in range(26))}
  <circle cx="350" cy="80" r="22" fill="{MOON}"/>
  {''.join(f'<rect x="{x}" y="{194 - h}" width="{w}" height="{h}" fill="#0d0a1f"/>' for x, w, h in [(120, 40, 40), (158, 30, 62), (190, 46, 30), (238, 26, 54), (266, 50, 36), (318, 34, 70), (354, 66, 44)])}
</g>
<rect x="120" y="34" width="300" height="160" rx="4" fill="none" stroke="#3b2a6b" stroke-width="6"/>
<rect x="267" y="34" width="6" height="160" fill="#3b2a6b"/><rect x="120" y="111" width="300" height="6" fill="#3b2a6b"/>
<path class="curtain" d="M92,26 L150,26 Q140,110 152,206 L100,206 Q86,110 92,26Z" fill="#4a2462"/>
<path class="curtain" style="animation-delay:-3s" d="M390,26 L448,26 Q454,110 440,206 L388,206 Q400,110 390,26Z" fill="#4a2462"/>
<rect x="84" y="20" width="372" height="8" rx="4" fill="#2a1d52"/>
<!-- desk lamp glow -->
<circle cx="640" cy="120" r="170" fill="url(#lampg)" class="lamp"/>
<path d="M610,70 L670,70 L690,104 L590,104Z" fill="#2a1d52"/><rect x="637" y="104" width="6" height="60" fill="#2a1d52"/>
<!-- me, a little sleepy -->
<ellipse cx="930" cy="150" rx="110" ry="90" fill="url(#face)" class="glowpulse"/>
<g fill="#0a0818" stroke="#7d6bb8" stroke-opacity=".6" stroke-width="1.6">
  <path d="M860,230 C860,180 890,160 930,160 C970,160 1000,180 1000,230Z"/>
  <path d="M895,118 C895,84 915,66 932,66 C952,66 972,84 970,118 C969,140 952,156 932,156 C912,156 896,140 895,118Z"/>
</g>
<path d="M914,120 q8,4 16,0 M944,120 q8,4 16,0" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" opacity=".8"/>
<!-- dialogue box -->
<rect x="40" y="200" width="{W - 80}" height="108" rx="14" fill="{box}" stroke="{SAKURA_D}" stroke-width="2"/>
<rect x="46" y="206" width="{W - 92}" height="96" rx="10" fill="none" stroke="#fff" stroke-opacity=".08"/>
<g transform="translate(70,186)">
  <rect width="128" height="30" rx="8" fill="{SAKURA_D}"/>
  <text x="64" y="21" font-family="{SANS}" font-size="16" font-weight="800" letter-spacing="3" fill="#fff" text-anchor="middle">RAHUL</text>
</g>
{''.join(groups)}
<g class="next"><path d="M1128,282 l12,0 l-6,8z" fill="{SAKURA}"/></g>
<text x="{W - 52}" y="44" font-family="{MONO}" font-size="16" letter-spacing="3" fill="#cbbff0" text-anchor="end">03:15 · STILL AWAKE</text>
</g>
</svg>"""
    (OUT / "dialogue.svg").write_text(svg, encoding="utf-8")


# ─────────────────────────── 04:45 — quest log ───────────────────────────
# status: done / active (with progress 0–1) / locked. Edit to taste.
MAIN_QUESTS = [
    ("done", "Ship a full-stack app from scratch", 1),
    ("done", "Build my first mobile app", 1),
    ("active", "Run a system real users rely on", .6),
    ("locked", "Build something a million people use", 0),
]
SIDE_QUESTS = [
    ("active", "Go somewhere new every year", .5),
    ("active", "Learn one new tool every month", .7),
    ("active", "Fix one bug without making three more", .3),
    ("locked", "Ride a night train through a new country", 0),
]


def quest_rows(quests, x0, y0, delay0):
    out = []
    for i, (st, name, prog) in enumerate(quests):
        y = y0 + i * 60
        d = delay0 + i * .25
        if st == "done":
            box = (f'<rect x="0" y="-16" width="22" height="22" rx="5" fill="{SAKURA_D}"/>'
                   f'<path d="M5,-5 l5,5 l8,-10" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
            label = f'<text x="38" y="1" font-family="{SANS}" font-size="19" fill="#cbbff0" text-decoration="line-through" opacity=".85">{name}</text>'
            extra = f'<text x="512" y="1" font-family="{MONO}" font-size="14" letter-spacing="1" fill="{SAKURA}" text-anchor="end">CLEAR</text>'
        elif st == "active":
            box = f'<rect x="1" y="-15" width="20" height="20" rx="5" fill="none" stroke="{CYAN}" stroke-width="2"/><circle cx="11" cy="-5" r="4" fill="{CYAN}" class="pulse"/>'
            label = f'<text x="38" y="1" font-family="{SANS}" font-size="19" fill="#fff">{name}</text>'
            extra = (f'<rect x="38" y="14" width="300" height="6" rx="3" fill="#2b1f56"/>'
                     f'<rect x="38" y="14" width="{300 * prog:.0f}" height="6" rx="3" fill="url(#qbar)"/>'
                     f'<text x="512" y="1" font-family="{MONO}" font-size="14" letter-spacing="1" fill="{CYAN}" text-anchor="end">{round(prog * 100)}%</text>')
        else:
            box = (f'<rect x="1" y="-15" width="20" height="20" rx="5" fill="none" stroke="#4c3d85" stroke-width="2"/>'
                   f'<rect x="6" y="-7" width="10" height="8" rx="1.5" fill="#6b5aa8"/><path d="M8,-7 v-3 a3,3 0 0 1 6,0 v3" fill="none" stroke="#6b5aa8" stroke-width="1.6"/>')
            label = f'<text x="38" y="1" font-family="{SANS}" font-size="19" fill="#9d93c4" font-style="italic">{name}</text>'
            extra = f'<text x="512" y="1" font-family="{MONO}" font-size="14" letter-spacing="1" fill="#6b5aa8" text-anchor="end">LOCKED</text>'
        out.append(f'<g transform="translate({x0},{y})"><g>{box}{label}{extra}</g></g>')
    return "".join(out).replace("I've", "I&#39;ve")


def quests():
    W, H = 1200, 420
    rng = random.Random(445)
    done = sum(1 for q in MAIN_QUESTS + SIDE_QUESTS if q[0] == "done")
    total = len(MAIN_QUESTS) + len(SIDE_QUESTS)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Quest log. {done} of {total} quests cleared.">
<style>
.pulse{{animation:pulse 1.6s ease-in-out infinite}}@keyframes pulse{{50%{{opacity:.25}}}}
.shine{{animation:shine 3s linear infinite}}@keyframes shine{{from{{transform:translateX(-200px)}}to{{transform:translateX(1300px)}}}}
.tw{{animation:tw 3s ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.05}}}}
</style>
<defs>
  <linearGradient id="qbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1440"/><stop offset="1" stop-color="#3a1d55"/></linearGradient>
  <linearGradient id="qbar"><stop offset="0" stop-color="{SAKURA_D}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  <linearGradient id="qshine"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="qc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#qc)">
<rect width="{W}" height="{H}" fill="url(#qbg)"/>
{stars(rng, 24, W, 120)}
<rect class="shine" x="0" y="0" width="160" height="{H}" fill="url(#qshine)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{SAKURA_D}" stroke-opacity=".35" stroke-width="2"/>
<text x="56" y="62" font-family="{SANS}" font-size="26" font-weight="800" letter-spacing="5" fill="#fff">QUEST LOG</text>
<text x="{W - 56}" y="62" font-family="{MONO}" font-size="18" fill="#cbbff0" text-anchor="end">{done} / {total} cleared</text>
<rect x="{W - 256}" y="74" width="200" height="4" rx="2" fill="#2b1f56"/>
<rect x="{W - 256}" y="74" width="{200 * done / total:.0f}" height="4" rx="2" fill="{SAKURA_D}"/>
<line x1="56" y1="92" x2="{W - 56}" y2="92" stroke="#3b2a6b"/>
<text x="56" y="128" font-family="{MONO}" font-size="16" letter-spacing="4" fill="{SAKURA}">MAIN QUESTS</text>
<text x="634" y="128" font-family="{MONO}" font-size="16" letter-spacing="4" fill="{CYAN}">SIDE QUESTS</text>
<line x1="604" y1="112" x2="604" y2="{H - 36}" stroke="#3b2a6b" stroke-dasharray="3 6"/>
{quest_rows(MAIN_QUESTS, 56, 180, .2)}
{quest_rows(SIDE_QUESTS, 634, 180, .5)}
</svg>"""
    (OUT / "quests.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    hero()
    for h in HEADERS:
        header(*h)
    loves()
    dialogue()
    quests()
    journey()
    morning()
    print("built:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
