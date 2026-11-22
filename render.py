"""Render the front page for Saturday 21 November 2026 (round 5).

Round 5 is a polish pass on round 4, which had converged the page
onto the composition of the current top entry of this competition:
red banner strips inside every scene, a micro-fact chip under each
hero banner, a source strip along the bottom-left of each hero
scene, dark fact chips on the small scenes, a tall dark-navy world
map with the ALSO list running beside it, and denser, grain-textured
scene drawings. Round 5 redraws the map with denser, more accurate
coastlines and island chains, gives the ten small scenes the same
background layer the hero row has, and nudges the headline type
closer to the top entry's proportions. Facts, figures, story choice
and layout grammar follow the day's verified reporting; every
headline and summary is this page's own wording.

The day's leads are COP31 running into overtime in Antalya, five
Houthi missiles downed over Saudi Arabia and the magnitude 6.7 quake
in Peru. The missile that landed in Poland belongs to Friday
20 November and is named only in the DATE CHECK box. PIL only,
fully deterministic.
"""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H = 1024, 1024
M = 10
CW = W - 2 * M

PAPER = (250, 246, 236)
INK = (22, 20, 18)
RED = (176, 22, 22)
DARKRED = (148, 30, 24)
NAVY = (17, 32, 56)
GREY = (96, 90, 80)
FAINT = (203, 196, 182)
WHITE = (255, 255, 255)
CHIPDARK = (22, 24, 30)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if d.textlength(text, font=fnt) <= max_w:
        return text
    while text and d.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def vgrad(d, x, y, w, h, top, bottom):
    """Vertical colour gradient, drawn as one line per row."""
    for i in range(h):
        t = i / max(1, h - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        d.line([x, y + i, x + w, y + i], fill=col)


def speckle(d, count=12000):
    """Deterministic paper grain: hash-scattered single pixels."""
    for i in range(count):
        px = (i * 7919 + 104729) % W
        py = (i * 6271 + 31337) % H
        shade = 240 + (i * 31) % 8
        d.point((px, py), fill=(shade, shade - 4, shade - 18))


def grain(img, box, amp=6, seed=7):
    """Deterministic luminance grain pasted over one rectangle."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    rng = random.Random(seed)
    raw = rng.randbytes(w * h)
    lut = bytes(128 - amp + (i % (2 * amp + 1)) for i in range(256))
    noise = Image.frombytes("L", (w, h), raw.translate(lut))
    nrgb = Image.merge("RGB", (noise, noise, noise))
    region = img.crop(box)
    img.paste(ImageChops.add(region, nrgb, 1.0, -128), (x0, y0))


def wrap(d, text, fnt, max_w, max_lines=None):
    """Word-wrap text by measured width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit(d, lines[-1], fnt, max_w)
    return lines


# ---------------------------------------------------------------- data
# (num, place, field, banner, chip, chip_dark, source strip,
#  headline, summary, scene)
LEADS = [
    (1, "ANTALYA, TÜRKIYE", "CLIMATE", "COP31: OVERTIME",
     "No deal on day 13", False, "Talks still open · AFP, Al Jazeera",
     "Climate talks run into Saturday with no deal in sight",
     "On day 13, a draft that never mentions fossil fuels has split "
     "almost 200 countries; a third text is promised. (AFP, Al Jazeera)",
     "cop31"),
    (2, "RIYADH · JIZAN", "WAR", "SAUDI: MISSILES",
     "5 shot down", False, "Coalition tally · AFP",
     "Five Houthi missiles downed before dawn",
     "Three were destroyed over Riyadh and two over Jizan, a day "
     "after the coalition bombed Hodeidah port. (AFP)",
     "missiles"),
    (3, "JUNÍN, PERU", "EARTHQUAKE", "PERU: QUAKE 6.7",
     "00:09 UTC · 108 km deep", True, "USGS · IGP",
     "Magnitude 6.7 quake shakes central Peru",
     "Struck near Carhuamayo at 00:09 UTC, 108 km deep; felt in "
     "Lima, with no deaths and no tsunami risk. (USGS, IGP)",
     "quake"),
]

# (num, place, field, banner, chip, headline, summary, scene)
PANELS = [
    (4, "KYIV", "WAR", "KYIV: WARNING", "NBC interview",
     "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "He warns of more double-tap strikes to come.", "bridge"),
    (5, "STRAIT OF HORMUZ", "WAR", "HORMUZ: DRONE", "Claim · IRIB",
     "Iran says it shot down a US drone",
     "No confirmation from Washington.", "hormuz"),
    (6, "TEHRAN", "DIPLOMACY", "IRAN: URANIUM", "Minister · ToI",
     "Iran: uranium stock stays in the country",
     "The minister still sees a \u201cfair solution\u201d.", "atom"),
    (7, "WASHINGTON", "TECHNOLOGY", "TRUMP: AI TAX", "ABC briefing",
     "Trump vows tax on data centres abroad",
     "A \u201ctremendous\u201d penalty; no details yet.", "aitax"),
    (8, "BEIJING", "DIPLOMACY", "CHINA\u2013JAPAN", "Ministry · AFP",
     "China tells Japan to \u201ccorrect\u201d Taiwan words",
     "Tokyo says its stance is unchanged.", "flags"),
    (9, "DAVAO", "AVIATION", "DAVAO: 146 SAFE", "Airline · AP",
     "Jet lands safely after engine fire alert",
     "All 146 safe; the flight diverted after midnight.", "jet"),
    (10, "CANBERRA", "DIPLOMACY", "CANBERRA: AI TALKS", "Agreed · ABC",
     "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip.", "talks"),
    (11, "WORLD", "MARKETS", "BITCOIN: $58,983", None,
     "Bitcoin trades below $59,000 on Saturday",
     "Down 3.9% in a day; ether at $1,625.", "bitcoin"),
    (12, "LAS VEGAS", "FORMULA 1", "RUSSELL: P1", "Timing · Formula 1",
     "Russell fastest in final practice",
     "1:34.041 in a damp, messy session.", "f1"),
    (13, "WELLINGTON", "CRICKET", "RAHUL: 124*", "Tea, day 3 · AFP",
     "Rahul's 124 not out puts India on top",
     "India 344 for 2 at tea, replying to 368.", "cricket"),
]

ALSO = [
    (14, "Kryvyi Rih: double strike kills 2, injures 42", "Kyiv Independent"),
    (15, "Copenhagen: Russian attach\u00e9 expelled over a plot", "Al Jazeera"),
    (16, "Antalya: EU warns of a \u201cfossil summit\u201d", "Al Jazeera"),
    (17, "Antalya: Panama threatens to block the climate text", "Al Jazeera"),
    (18, "Antalya: PLN signs six clean-power deals", "Antara"),
    (19, "Yemen: Houthis threaten Jeddah and Red Sea ports", "Al Jazeera"),
    (20, "Washington: Vance \u2014 Iran strikes were Trump's call", "Reuters"),
    (21, "Washington: lawmaker threatens SpaceX funding", "CNN"),
    (22, "Texas: execution of a man of 70 takes 63 minutes", "ABC"),
    (23, "Los Angeles: jury convicts Palisades fire starter", "AFP"),
    (24, "Missouri: $7.25bn Roundup deal approved", "AFP"),
    (25, "Vancouver: Canada rests defence in climate trial", "AFP"),
    (26, "Pyongyang: Kim tours factories after no Trump meeting", "AFP"),
    (27, "Sejong: freight train derails; no one hurt", "Korea Herald"),
    (28, "Taipei: budget and a cash payout are passed", "Taipei Times"),
    (29, "Bangkok: six-point plan on arsenic in two rivers", "Nation"),
    (30, "New Delhi: Pakistani minister joins SCO forum", "Dawn"),
    (31, "Eastern India: rain alerts as Akvan fades inland", "ETV"),
    (32, "Myanmar: rights groups urge sanctions after ruling", "AP"),
    (33, "Port Louis: rating agency talks to 15 states", "AP"),
    (34, "Melbourne: Cummins keeps the Australia captaincy", "ABC"),
    (35, "Las Vegas: Verstappen sent to stewards after contact", "Autosport"),
]

STATS = [
    ("Day 13", "of COP31, due to close on day 12"),
    ("5", "missiles downed over Riyadh and Jizan"),
    ("6.7", "size of the earthquake in Jun\u00edn, Peru"),
    ("146", "people safe after the Davao jet landing"),
    ("$58,983", "bitcoin on Saturday, off 3.9% in a day"),
    ("124*", "K L Rahul, not out, at tea in Wellington"),
]

REGIONS = [("Europe", 4, (36, 84, 150)), ("Asia", 10, (176, 22, 22)),
           ("Middle East", 5, (168, 128, 32)), ("Africa", 1, (52, 128, 74)),
           ("Americas", 11, (96, 62, 148)), ("Oceania", 3, (30, 120, 160)),
           ("Global", 1, (110, 110, 110))]

DATE_CHECK = (
    "Left out as Friday 20 November news: Wall Street's fall into "
    "correction, the Russian barrage on Kyiv's bridges, the missile "
    "that landed in Poland, the UK\u2013EU deal and Cyclone Akvan's "
    "landfall. Older still: Voyager 1's light-day (18 Nov). "
    "Unconfirmed as this page was drawn: BepiColombo entering Mercury "
    "orbit; a final COP31 text.")


# -------------------------------------------------------------- scenes
def burst(d, cx, cy, r):
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)],
               fill=(255, 214, 90), width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=WHITE)


def dashed_arc(d, x0, y0, x1, y1, lift, color, width=2):
    pts = []
    for i in range(41):
        t = i / 40.0
        pts.append((x0 + (x1 - x0) * t,
                    y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)))
    for i in range(0, 40, 2):
        d.line([pts[i], pts[i + 1]], fill=color, width=width)


def cloud(d, cx, cy, s=1.0):
    d.ellipse([cx, cy, cx + 26 * s, cy + 9 * s], fill=(252, 252, 250))
    d.ellipse([cx + 8 * s, cy - 5 * s, cx + 24 * s, cy + 6 * s],
              fill=(252, 252, 250))


def scene_cop31(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (203, 227, 210), (228, 241, 230))
    d.rectangle([x, y + h - 11, x + w, y + h], fill=(186, 212, 188))
    cloud(d, x + 16, y + 30, 0.8)
    cloud(d, x + w - 52, y + 26, 0.7)
    # globe with continent blobs
    cx, cy, r = x + 74, y + 62, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(94, 154, 206),
              outline=NAVY, width=2)
    d.polygon([(cx - 20, cy - 14), (cx - 6, cy - 20), (cx - 2, cy - 8),
               (cx - 10, cy - 2), (cx - 20, cy - 6)], fill=(66, 140, 78))
    d.polygon([(cx - 8, cy + 4), (cx + 1, cy + 2), (cx + 2, cy + 16),
               (cx - 4, cy + 24), (cx - 9, cy + 12)], fill=(66, 140, 78))
    d.polygon([(cx + 8, cy - 16), (cx + 20, cy - 14), (cx + 22, cy - 4),
               (cx + 12, cy - 2), (cx + 7, cy - 8)], fill=(66, 140, 78))
    d.polygon([(cx + 10, cy + 6), (cx + 19, cy + 8), (cx + 16, cy + 17),
               (cx + 9, cy + 13)], fill=(80, 152, 84))
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 250, fill=(70, 120, 180), width=1)
    # thermometer
    tx = x + 158
    d.rounded_rectangle([tx, y + 26, tx + 14, y + 76], 7,
                        fill=WHITE, outline=INK, width=2)
    d.rectangle([tx + 3, y + 44, tx + 11, y + 74], fill=RED)
    d.ellipse([tx - 5, y + 70, tx + 19, y + 94], fill=RED, outline=INK, width=2)
    for k in range(4):
        d.line([tx + 18, y + 34 + k * 11, tx + 25, y + 34 + k * 11],
               fill=INK, width=2)
    d.text((tx + 28, y + 40), "1.5\u00b0", font=font(SANS_B, 11), fill=RED)
    # clock
    kx, ky, kr = x + w - 58, y + 60, 27
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE, outline=INK, width=2)
    for k in range(12):
        a = k * math.pi / 6
        r1 = kr - 4 if k % 3 else kr - 7
        d.line([kx + r1 * math.cos(a), ky + r1 * math.sin(a),
                kx + (kr - 2) * math.cos(a), ky + (kr - 2) * math.sin(a)],
               fill=INK, width=1)
    d.line([kx, ky, kx - 4, ky - 17], fill=INK, width=3)
    d.line([kx, ky, kx + 13, ky - 9], fill=INK, width=3)
    d.line([kx, ky, kx + 15, ky + 10], fill=RED, width=1)
    d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=RED)


def scene_missiles(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (8, 12, 30), (36, 46, 86))
    for i in range(46):
        sx = x + (i * 61) % int(w)
        sy = y + 22 + (i * 37) % int(h * 0.5)
        d.point((sx, sy), fill=(200, 210, 235))
    base = y + h
    # far skyline
    for bx, bw, bh in [(0, 30, 34), (36, 22, 42), (64, 34, 30), (150, 26, 38),
                       (182, 38, 28), (250, 24, 40), (280, 34, 30), (318, 20, 36)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(46, 56, 94))
    # near skyline with lit windows
    for bx, bw, bh in [(0, 34, 20), (40, 26, 30), (72, 40, 16), (150, 30, 24),
                       (190, 44, 18), (250, 28, 28), (286, 36, 15)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 11, 24))
        for wy in range(5, bh - 3, 6):
            for wx in range(4, bw - 4, 8):
                if (wx * 7 + wy * 13 + bx) % 3 == 0:
                    d.rectangle([x + bx + wx, base - bh + wy,
                                 x + bx + wx + 2, base - bh + wy + 2],
                                fill=(255, 205, 90))
    dashed_arc(d, x + 18, base - 16, x + w - 70, y + 30, 34, (255, 160, 80))
    dashed_arc(d, x + 60, base - 14, x + w - 130, y + 22, 40, (255, 190, 110))
    dashed_arc(d, x + 120, base - 18, x + w - 30, y + 44, 26, (255, 140, 70))
    burst(d, x + w - 70, y + 30, 11)
    burst(d, x + w - 130, y + 22, 9)
    burst(d, x + w - 30, y + 44, 8)


def scene_quake(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (239, 229, 205), (226, 210, 176))
    # seismograph panel
    px0, py0, px1, py1 = x + 8, y + 28, x + 188, y + 90
    d.rectangle([px0, py0, px1, py1], fill=WHITE, outline=GREY, width=1)
    for gx in range(px0 + 12, px1, 12):
        d.line([gx, py0 + 2, gx, py1 - 2], fill=(232, 228, 218), width=1)
    for gy in range(py0 + 10, py1, 10):
        d.line([px0 + 2, gy, px1 - 2, gy], fill=(232, 228, 218), width=1)
    mid = (py0 + py1) // 2
    pts = [(px0 + 4, mid)]
    px, py = px0 + 4, mid
    for dx, dy in [(14, 0), (9, -5), (7, 9), (7, -20), (7, 24), (7, -28),
                   (7, 16), (7, -7), (9, 3), (13, 0), (15, -2), (20, 0)]:
        px += dx
        py += dy
        pts.append((px, py))
    d.line(pts, fill=RED, width=2, joint="curve")
    d.text((px0 + 5, py0 + 3), "6.7", font=font(SERIF_B, 15), fill=RED)
    # ground and houses
    gy = y + 92
    d.line([x + 196, gy, x + w - 4, gy], fill=(120, 90, 60), width=2)
    for hx, tilt, crack in [(x + 210, 0, False), (x + 268, 3, True)]:
        d.rectangle([hx, y + 58 + tilt, hx + 36, gy], fill=(206, 178, 138),
                    outline=INK, width=1)
        d.polygon([(hx - 4, y + 60 + tilt), (hx + 18, y + 42 + tilt),
                   (hx + 40, y + 60 + tilt)], fill=(150, 74, 52))
        d.rectangle([hx + 14, y + 72 + tilt, hx + 22, gy], fill=(90, 60, 40))
        d.rectangle([hx + 4, y + 64 + tilt, hx + 10, y + 70 + tilt],
                    fill=(240, 230, 200), outline=INK, width=1)
        if crack:
            d.line([hx + 26, y + 60, hx + 22, y + 70, hx + 28, y + 80,
                    hx + 24, gy], fill=(90, 60, 40), width=1)
    d.line([x + 198, gy + 3, x + 224, gy + 6, x + 246, gy + 2, x + 272,
            gy + 6, x + 320, gy + 3], fill=(100, 74, 48), width=2)
    d.ellipse([x + 292, y + 46, x + 306, y + 53], fill=(196, 186, 168))
    d.ellipse([x + 302, y + 40, x + 318, y + 48], fill=(204, 194, 176))


def scene_bridge(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (56, 76, 116), (104, 126, 166))
    for i in range(26):
        sx = x + (i * 53) % int(w)
        sy = y + 3 + (i * 29) % 15
        d.point((sx, sy), fill=(215, 224, 240))
    d.ellipse([x + 9, y + 4, x + 19, y + 14], fill=(238, 240, 244))
    d.ellipse([x + 13, y + 3, x + 23, y + 13], fill=(59, 79, 118))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(36, 60, 102))
    for i in range(4):
        d.line([x + 14 + i * 47, y + h - 5, x + 34 + i * 47, y + h - 5],
               fill=(150, 175, 205), width=1)
    deck = y + h - 13
    for tx in (x + w * 0.32, x + w * 0.68):
        d.rectangle([tx - 2, y + 16, tx + 2, deck], fill=(24, 30, 44))
    d.line([x + 4, y + 22, x + w * 0.32, y + 17, x + w * 0.68, y + 17,
            x + w - 4, y + 22], fill=(220, 226, 238), width=2)
    for i in range(1, 8):
        hx = x + i * w / 8
        d.line([hx, y + 20, hx, deck], fill=(160, 172, 196), width=1)
    d.line([x, deck, x + w, deck], fill=(16, 20, 30), width=3)
    d.rectangle([x + w * 0.44, deck - 5, x + w * 0.44 + 13, deck - 1],
                fill=(240, 200, 80))
    d.rectangle([x + w * 0.44 + 2, deck - 8, x + w * 0.44 + 9, deck - 5],
                fill=(200, 60, 50))


def scene_hormuz(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (32, 96, 118), (64, 140, 158))
    d.polygon([(x + 92, y + 32), (x + 118, y + 26), (x + 148, y + 30),
               (x + 176, y + 27), (x + w, y + 30), (x + w, y + 35),
               (x + 92, y + 35)], fill=(42, 100, 120))
    cloud(d, x + 128, y + 19, 0.45)
    for row in range(3):
        for i in range(6):
            ax = x + 8 + i * 32 + (row % 2) * 14
            ay = y + h - 16 + row * 5
            d.arc([ax, ay - 3, ax + 16, ay + 3], 180, 360,
                  fill=(130, 198, 212), width=1)
    d.ellipse([x + 12, y + 22, x + 22, y + 32], fill=(250, 226, 150))
    hx, hy = x + 22, y + h - 12
    d.polygon([(hx, hy - 9), (hx + 100, hy - 9), (hx + 87, hy), (hx + 11, hy)],
              fill=(30, 34, 44))
    for i, col in enumerate([(196, 70, 50), (60, 130, 190), (220, 160, 60)]):
        d.rectangle([hx + 12 + i * 24, hy - 20, hx + 33 + i * 24, hy - 10],
                    fill=col, outline=(20, 22, 30), width=1)
        d.rectangle([hx + 12 + i * 24, hy - 28, hx + 33 + i * 24, hy - 21],
                    fill=col, outline=(20, 22, 30), width=1)
    d.rectangle([hx + 84, hy - 26, hx + 96, hy - 10], fill=(225, 228, 232))
    d.rectangle([hx + 87, hy - 23, hx + 93, hy - 19], fill=(70, 110, 160))
    dx, dy = x + w - 32, y + 26
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(20, 20, 20))
    for ox, oy in [(-10, -6), (10, -6), (-10, 6), (10, 6)]:
        d.line([dx, dy, dx + ox, dy + oy], fill=(20, 20, 20), width=1)
        d.ellipse([dx + ox - 3, dy + oy - 3, dx + ox + 3, dy + oy + 3],
                  outline=(20, 20, 20), width=1)


def _orbit(img, cx, cy, rx, ry, angle, color):
    layer = Image.new("RGBA", (rx * 2 + 8, ry * 2 + 8), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([4, 4, rx * 2 + 4, ry * 2 + 4], outline=color + (255,), width=1)
    layer = layer.rotate(angle, resample=Image.BILINEAR, center=(rx + 4, ry + 4))
    img.paste(layer, (cx - rx - 4, cy - ry - 4), layer)


def scene_atom(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (243, 245, 239), (229, 232, 222))
    for gx in range(x + 14, x + w, 18):
        for gy in range(y + 20, y + h, 14):
            d.point((gx, gy), fill=(214, 218, 208))
    cx, cy = x + w // 2, y + h // 2 + 4
    _orbit(img, cx, cy, w // 3, h // 3, 0, (70, 90, 160))
    _orbit(img, cx, cy, w // 3, h // 3, 60, (70, 90, 160))
    _orbit(img, cx, cy, w // 3, h // 3, -60, (70, 90, 160))
    for ex, ey in [(cx - w // 3, cy), (cx + 20, cy - 12), (cx + 8, cy + 13)]:
        d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(50, 90, 180))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for sx, sy in [(x + 22, y + 24), (x + w - 26, y + 30),
                   (x + 30, y + h - 14)]:
        d.line([sx - 3, sy, sx + 3, sy], fill=(148, 158, 138), width=1)
        d.line([sx, sy - 3, sx, sy + 3], fill=(148, 158, 138), width=1)


def scene_aitax(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 34, 50))
    d.line([x, y + h - 5, x + w, y + h - 5], fill=(52, 62, 84), width=2)
    for i in range(5):
        lx = x + 14 + i * 38
        d.ellipse([lx, y + 5, lx + 5, y + 10], fill=(206, 222, 240))
    d.ellipse([x + w - 27, y + 5, x + w - 13, y + 19],
              outline=(255, 190, 90), width=1)
    d.text((x + w - 23, y + 8), "%", font=font(SANS_B, 8),
           fill=(255, 190, 90))
    for i, rx in enumerate((x + 8, x + 33, x + 58)):
        d.rectangle([rx, y + 18, rx + 20, y + h - 7], fill=(48, 58, 80),
                    outline=(90, 104, 132), width=1)
        for r in range(4):
            for c in range(2):
                col = (90, 210, 120) if (r + c + i) % 3 else (255, 180, 70)
                d.ellipse([rx + 4 + c * 9, y + 22 + r * 7, rx + 7 + c * 9,
                           y + 25 + r * 7], fill=col)
    gx, gy = x + w - 62, y + h // 2 + 3
    d.rectangle([gx - 14, gy - 14, gx + 14, gy + 14], fill=(70, 130, 180),
                outline=(200, 220, 240), width=1)
    d.rectangle([gx - 6, gy - 6, gx + 6, gy + 6], outline=(220, 235, 245), width=1)
    for k in range(-1, 2):
        d.line([gx + 17, gy + k * 8, gx + 24, gy + k * 8],
               fill=(200, 220, 240), width=2)
        d.line([gx - 24, gy + k * 8, gx - 17, gy + k * 8],
               fill=(200, 220, 240), width=2)
    d.text((x + w - 26, y + h - 15), "AI", font=font(SANS_B, 11),
           fill=(160, 200, 235))


def scene_flags(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (198, 220, 240), (216, 233, 247))
    d.ellipse([x + 96, y + 17, x + 107, y + 28], fill=(250, 214, 90),
              outline=(240, 190, 70), width=1)
    cloud(d, x + 130, y + 24, 0.55)
    d.line([x, y + h - 3, x + w, y + h - 3], fill=(120, 160, 110), width=2)
    for px, kind in [(x + 38, "cn"), (x + w - 84, "jp")]:
        d.line([px, y + 16, px, y + h - 3], fill=(70, 70, 70), width=2)
        fw, fh = 54, 24
        fx, fy = px + 2, y + 17
        if kind == "cn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(206, 32, 40),
                        outline=(150, 20, 28), width=1)
            d.ellipse([fx + 5, fy + 4, fx + 11, fy + 10], fill=(255, 214, 60))
            for ox, oy in [(14, 2), (16, 7), (14, 12), (11, 15)]:
                d.point((fx + ox, fy + oy), fill=(255, 214, 60))
        else:
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=WHITE,
                        outline=(150, 150, 150), width=1)
            d.ellipse([fx + fw // 2 - 6, fy + 6, fx + fw // 2 + 6, fy + 18],
                      fill=(206, 32, 40))


def scene_jet(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (146, 190, 230), (198, 226, 247))
    d.ellipse([x + 14, y + 16, x + 26, y + 28], fill=(250, 220, 120),
              outline=(240, 195, 80), width=1)
    cloud(d, x + 8, y + 38, 0.7)
    cloud(d, x + w - 60, y + 22, 0.6)
    cy = y + h // 2 + 4
    d.line([x + 4, cy - 6, x + 20, cy - 4], fill=(240, 246, 252), width=2)
    d.line([x + 4, cy + 3, x + 20, cy + 3], fill=(240, 246, 252), width=2)
    d.rounded_rectangle([x + 20, cy - 8, x + w - 36, cy + 7], 7, fill=WHITE,
                        outline=(120, 140, 165), width=1)
    d.polygon([(x + w - 36, cy - 8), (x + w - 15, cy - 2), (x + w - 15, cy + 3),
               (x + w - 36, cy + 7)], fill=WHITE, outline=(120, 140, 165))
    d.polygon([(x + 24, cy - 8), (x + 36, cy - 22), (x + 48, cy - 22),
               (x + 46, cy - 8)], fill=RED)
    d.polygon([(x + 80, cy + 5), (x + 106, cy + 16), (x + 120, cy + 16),
               (x + 106, cy + 5)], fill=(150, 165, 185))
    for i in range(9):
        d.ellipse([x + 36 + i * 12, cy - 4, x + 40 + i * 12, cy],
                  fill=(70, 110, 160))
    d.rectangle([x + 86, cy + 12, x + 100, cy + 16], fill=(90, 100, 115))


def scene_talks(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (236, 242, 226), (221, 229, 204))
    d.line([x + 10, y + h - 6, x + w - 10, y + h - 6], fill=(170, 178, 150),
           width=2)
    for i, cxx in enumerate(range(x + 14, x + w - 10, 13)):
        ccol = (120, 130, 105) if i % 2 else (105, 118, 128)
        d.ellipse([cxx, y + h - 15, cxx + 5, y + h - 10], fill=ccol)
        d.arc([cxx - 2, y + h - 12, cxx + 7, y + h - 4], 180, 360,
              fill=ccol, width=2)
    for hx, col in [(x + 34, (70, 110, 170)), (x + w - 46, (180, 80, 70))]:
        d.ellipse([hx, y + h - 20, hx + 12, y + h - 8], fill=col)
        d.arc([hx - 3, y + h - 13, hx + 15, y + h + 2], 180, 360, fill=col,
              width=3)
    d.rounded_rectangle([x + 16, y + 17, x + 82, y + 35], 6, fill=WHITE,
                        outline=INK, width=1)
    d.polygon([(x + 28, y + 35), (x + 36, y + 35), (x + 28, y + 41)],
              outline=INK, fill=WHITE)
    d.rounded_rectangle([x + w - 82, y + 21, x + w - 16, y + 39], 6, fill=WHITE,
                        outline=INK, width=1)
    d.polygon([(x + w - 36, y + 39), (x + w - 28, y + 39), (x + w - 28, y + 45)],
              outline=INK, fill=WHITE)
    for bx in (x + 30, x + 45, x + 60):
        d.ellipse([bx, y + 23, bx + 5, y + 28], fill=(90, 140, 200))
    for bx in (x + w - 62, x + w - 47, x + w - 32):
        d.ellipse([bx, y + 27, bx + 5, y + 32], fill=(200, 90, 80))


def scene_bitcoin(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 24, 38))
    for gx in range(x + 10, x + 96, 14):
        d.line([gx, y + 17, gx, y + h - 3], fill=(36, 42, 60), width=1)
    for gy in range(y + 22, y + h - 2, 9):
        d.line([x + 4, gy, x + 96, gy], fill=(36, 42, 60), width=1)
    tops = [22, 25, 30, 33, 39, 43]
    for i, tp in enumerate(tops):
        cx = x + 10 + i * 14
        col = (235, 80, 70) if i % 2 else (90, 190, 110)
        d.line([cx + 3, y + tp - 4, cx + 3, y + tp + 11], fill=col, width=1)
        d.rectangle([cx, y + tp, cx + 7, y + tp + 8], fill=col)
    d.line([x + 8, y + 24, x + 92, y + 46], fill=(235, 80, 70), width=2)
    d.polygon([(x + 93, y + 47), (x + 85, y + 46), (x + 90, y + 40)],
              fill=(235, 80, 70))
    # data inset, bottom-right
    ix0, iy0, ix1, iy1 = x + w - 88, y + 20, x + w - 3, y + h - 3
    d.rectangle([ix0, iy0, ix1, iy1], fill=(26, 18, 22), outline=(96, 64, 64),
                width=1)
    d.text((ix0 + 5, iy0 + 3), "BTC", font=font(SANS_B, 8), fill=WHITE)
    d.text((ix0 + 30, iy0 + 3), "-3.9%", font=font(SANS_B, 8), fill=(255, 110, 95))
    d.text((ix0 + 5, iy0 + 13), "ETH", font=font(SANS_B, 8), fill=WHITE)
    d.text((ix0 + 30, iy0 + 13), "-6.1%", font=font(SANS_B, 8), fill=(255, 110, 95))
    d.text((ix0 + 5, iy0 + 24), "CoinGecko", font=font(SANS, 7),
           fill=(170, 170, 175))
    d.text((ix0 + 48, iy0 + 24), "02:08 UTC", font=font(SANS, 7),
           fill=(170, 170, 175))


def scene_f1(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(116, 116, 122))
    d.rectangle([x, y + 17, x + w, y + 21], fill=(104, 104, 110))
    for i in range(16):
        ccol = [(228, 92, 82), (96, 142, 220), (240, 200, 92),
                (232, 232, 232)][i % 4]
        d.ellipse([x + 6 + i * 12, y + 18, x + 8 + i * 12, y + 20],
                  fill=ccol)
    for i in range(9):
        d.rectangle([x + 6 + i * 22, y + h - 9, x + 17 + i * 22, y + h - 6],
                    fill=(228, 228, 230))
    for i in range(9):
        kcol = (196, 40, 40) if i % 2 else (238, 238, 238)
        d.rectangle([x + 4 + i * 21, y + h - 13, x + 15 + i * 21, y + h - 11],
                    fill=kcol)
    by = y + h - 14
    d.polygon([(x + 28, by - 5), (x + 64, by - 9), (x + 116, by - 7),
               (x + 138, by - 2), (x + 138, by + 1), (x + 28, by + 1)],
              fill=(178, 24, 24))
    d.rectangle([x + 24, by - 15, x + 30, by - 3], fill=(40, 40, 44))
    d.rectangle([x + 17, by - 16, x + 42, by - 13], fill=(40, 40, 44))
    d.rectangle([x + 126, by - 4, x + 148, by - 1], fill=(40, 40, 44))
    d.arc([x + 72, by - 15, x + 96, by - 1], 180, 360, fill=(30, 30, 34), width=3)
    for wx in (x + 42, x + 120):
        d.ellipse([wx - 8, by - 7, wx + 8, by + 9], fill=(15, 15, 15))
        d.ellipse([wx - 3, by - 2, wx + 3, by + 4], fill=(150, 150, 155))
    # chequered flag, top-right
    fx, fy = x + w - 22, y + 20
    for r in range(3):
        for c in range(4):
            col = (20, 20, 20) if (r + c) % 2 else (240, 240, 240)
            d.rectangle([fx + c * 4, fy + r * 4, fx + c * 4 + 4, fy + r * 4 + 4],
                        fill=col)
    d.line([fx, fy, fx, fy + 18], fill=(60, 60, 60), width=1)


def scene_cricket(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(64, 146, 76))
    for i in range(4):
        if i % 2:
            d.rectangle([x + i * w // 4, y, x + (i + 1) * w // 4, y + h],
                        fill=(58, 136, 70))
    d.rectangle([x, y + 15, x + w, y + 21], fill=(52, 126, 64))
    for i in range(17):
        ccol = [(240, 220, 150), (220, 230, 240), (235, 170, 160),
                (200, 220, 190)][i % 4]
        d.ellipse([x + 5 + i * 11, y + 17, x + 7 + i * 11, y + 19],
                  fill=ccol)
    d.rectangle([x + 28, y + h - 12, x + w - 28, y + h - 4],
                fill=(206, 182, 132))
    d.line([x + 34, y + h - 12, x + 34, y + h - 4], fill=WHITE, width=1)
    d.line([x + w - 34, y + h - 12, x + w - 34, y + h - 4], fill=WHITE, width=1)
    sx = x + w - 46
    for k in range(3):
        d.line([sx + k * 6, y + h - 24, sx + k * 6, y + h - 10],
               fill=(240, 230, 190), width=2)
    d.line([sx - 1, y + h - 25, sx + 5, y + h - 23], fill=(240, 230, 190), width=2)
    d.line([sx + 6, y + h - 25, sx + 12, y + h - 23], fill=(240, 230, 190), width=2)
    d.polygon([(x + 38, y + h - 15), (x + 43, y + h - 17), (x + 62, y + 24),
               (x + 57, y + 22)], fill=(228, 198, 148), outline=(150, 116, 70))
    d.line([x + 60, y + 23, x + 67, y + 28], fill=(110, 78, 44), width=3)
    d.ellipse([x + 100, y + 24, x + 110, y + 34], fill=RED, outline=WHITE, width=1)
    d.arc([x + 102, y + 25, x + 108, y + 33], 300, 60, fill=WHITE, width=1)


SCENES = {"cop31": scene_cop31, "missiles": scene_missiles, "quake": scene_quake,
          "bridge": scene_bridge, "hormuz": scene_hormuz, "atom": scene_atom,
          "aitax": scene_aitax, "flags": scene_flags, "jet": scene_jet,
          "talks": scene_talks, "bitcoin": scene_bitcoin, "f1": scene_f1,
          "cricket": scene_cricket}


# --------------------------------------------------------------- panels
def banner(d, x, y, w, text, fh, fs):
    d.rectangle([x, y, x + w, y + fh], fill=RED)
    d.text((x + 6, y + fh // 2 - fs // 2 - 1), fit(d, text, font(SANS_B, fs), w - 10),
           font=font(SANS_B, fs), fill=WHITE)


def hero_chip(d, x, y, text, dark):
    f = font(SANS_B, 10)
    tw = d.textlength(text, font=f)
    fill = DARKRED if dark else (252, 252, 248)
    d.rectangle([x, y, x + tw + 12, y + 18], fill=fill)
    d.text((x + 6, y + 3), text, font=f, fill=WHITE if dark else INK)


def source_strip(d, x, y_bottom, text):
    f = font(SANS_B, 8)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y_bottom - 16, x + tw + 12, y_bottom], fill=(24, 24, 24))
    d.text((x + 6, y_bottom - 12), text, font=f, fill=WHITE)


def kicker(d, x, y, num, place, field, fs=10, r=7):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    t = str(num)
    tf = font(SANS_B, 9 if num < 10 else 8)
    d.text((x + r - d.textlength(t, font=tf) / 2, y + r - 5), t, font=tf, fill=WHITE)
    d.text((x + 2 * r + 5, y + r - fs // 2 - 1), "%s · %s" % (place, field),
           font=font(SANS_B, fs), fill=RED)


def hero_panel(d, img, x, y, w, story, seed):
    num, place, field, ban, chip, chip_dark, strip, head, summ, scene = story
    sh = 100
    SCENES[scene](d, img, x, y, w, sh)
    grain(img, (x, y, x + w, y + sh), amp=6, seed=seed)
    d = ImageDraw.Draw(img)
    banner(d, x, y, w, ban, 20, 13)
    if chip:
        hero_chip(d, x + 6, y + 26, chip, chip_dark)
    source_strip(d, x, y + sh, strip)
    d.rectangle([x, y, x + w, y + sh], outline=FAINT, width=1)
    kicker(d, x, y + sh + 5, num, place, field)
    hy = y + sh + 23
    lines = wrap(d, head, font(SERIF_B, 22), w, 2)
    for line in lines:
        d.text((x, hy), line, font=font(SERIF_B, 22), fill=INK)
        hy += 25
    sy = hy + 3
    for line in wrap(d, summ, font(SANS, 10), w, 3):
        d.text((x, sy), line, font=font(SANS, 10), fill=(52, 50, 46))
        sy += 14


def small_panel(d, img, x, y, w, story, seed):
    num, place, field, ban, chip, head, summ, scene = story
    sh = 58
    SCENES[scene](d, img, x, y, w, sh)
    grain(img, (x, y, x + w, y + sh), amp=6, seed=seed)
    d = ImageDraw.Draw(img)
    banner(d, x, y, w, ban, 15, 10)
    if chip:
        f = font(SANS_B, 8)
        tw = d.textlength(chip, font=f)
        d.rectangle([x + w - tw - 10, y + sh - 15, x + w, y + sh], fill=CHIPDARK)
        d.text((x + w - tw - 5, y + sh - 11), chip, font=f, fill=WHITE)
    d.rectangle([x, y, x + w, y + sh], outline=FAINT, width=1)
    kicker(d, x, y + sh + 4, num, place, field, fs=9, r=6)
    hy = y + sh + 20
    lines = wrap(d, head, font(SERIF_B, 15), w, 2)
    for line in lines:
        d.text((x, hy), line, font=font(SERIF_B, 15), fill=INK)
        hy += 17
    sy = hy + 2
    for line in wrap(d, summ, font(SANS, 9), w, 2):
        d.text((x, sy), line, font=font(SANS, 9), fill=(52, 50, 46))
        sy += 12


# ----------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    vgrad(d, x, y, w, h, (19, 36, 62), (14, 27, 48))

    def proj(lon, lat):
        return (x + 8 + (lon + 170) / 360.0 * (w - 16),
                y + 8 + (80 - lat) / 140.0 * (h - 16))

    continents = [
        [(-168, 66), (-162, 70), (-156, 71), (-148, 70), (-141, 70),
         (-135, 69), (-128, 70), (-120, 71), (-112, 68), (-104, 68),
         (-97, 69), (-93, 67), (-90, 69), (-87, 66), (-89, 62), (-90, 58),
         (-88, 54), (-85, 52), (-82, 51), (-79, 53), (-78, 57), (-77, 60),
         (-79, 63), (-72, 62), (-66, 60), (-64, 58), (-60, 55), (-56, 52),
         (-56, 49), (-60, 46), (-64, 44), (-66, 44), (-68, 44), (-70, 43),
         (-70, 41), (-72, 41), (-73, 40), (-74, 39), (-75, 37), (-76, 35),
         (-75, 34), (-77, 33), (-79, 31), (-80, 28), (-80, 26), (-81, 25),
         (-82, 27), (-84, 29), (-86, 30), (-89, 30), (-91, 29), (-94, 29),
         (-97, 27), (-97, 25), (-96, 22), (-94, 19), (-91, 19), (-90, 20),
         (-88, 21), (-88, 18), (-86, 16), (-83, 14), (-83, 10), (-79, 9),
         (-81, 8), (-83, 10), (-85, 12), (-87, 13), (-90, 14), (-92, 15),
         (-95, 16), (-97, 17), (-100, 19), (-103, 21), (-105, 22),
         (-107, 24), (-109, 24), (-110, 26), (-112, 29), (-114, 31),
         (-117, 33), (-120, 34), (-121, 36), (-122, 38), (-124, 41),
         (-124, 46), (-126, 48), (-128, 51), (-131, 54), (-133, 57),
         (-136, 59), (-141, 60), (-147, 60), (-152, 59), (-156, 57),
         (-160, 56), (-162, 58), (-165, 60), (-167, 63), (-168, 66)],
        [(-46, 60), (-42, 61), (-38, 64), (-32, 68), (-24, 70), (-20, 74),
         (-22, 78), (-30, 80), (-42, 79), (-50, 75), (-53, 70), (-53, 65),
         (-50, 61), (-46, 60)],
        [(-79, 9), (-77, 6), (-77, 3), (-79, 0), (-80, -3), (-81, -5),
         (-79, -8), (-77, -11), (-75, -14), (-72, -17), (-70, -18),
         (-70, -21), (-70, -24), (-70, -28), (-70, -31), (-71, -34),
         (-71, -37), (-72, -40), (-73, -44), (-73, -48), (-74, -51),
         (-73, -54), (-70, -55), (-67, -55), (-66, -52), (-65, -48),
         (-64, -44), (-63, -41), (-60, -38), (-57, -35), (-52, -32),
         (-49, -29), (-46, -26), (-41, -23), (-39, -20), (-37, -15),
         (-35, -10), (-35, -8), (-36, -6), (-38, -4), (-41, -2),
         (-44, -2), (-48, 0), (-51, 2), (-54, 4), (-57, 6), (-60, 8),
         (-63, 10), (-66, 10), (-69, 11), (-71, 12), (-74, 11), (-76, 9),
         (-78, 8), (-79, 9)],
        [(-9, 37), (-9, 40), (-9, 43), (-6, 44), (-2, 44), (-1, 46),
         (-4, 48), (-1, 49), (0, 50), (2, 51), (4, 52), (6, 53), (8, 54),
         (8, 56), (8, 57), (7, 58), (6, 59), (5, 60), (5, 62), (8, 63),
         (11, 65), (14, 67), (17, 68), (20, 69), (24, 70), (28, 71),
         (31, 70), (34, 69), (37, 67), (41, 66), (45, 67), (49, 68),
         (54, 69), (59, 69), (64, 69), (68, 70), (68, 66), (63, 64),
         (58, 62), (54, 60), (50, 57), (47, 54), (44, 51), (42, 49),
         (40, 47), (38, 47), (35, 45), (33, 46), (31, 46), (28, 45),
         (28, 43), (26, 42), (25, 41), (23, 40), (23, 38), (22, 37),
         (23, 36), (24, 37), (25, 39), (23, 40), (20, 41), (19, 42),
         (16, 43), (14, 45), (13, 45), (12, 44), (14, 43), (15, 42),
         (17, 40), (18, 40), (17, 38), (16, 38), (15, 39), (14, 41),
         (12, 43), (10, 44), (8, 44), (7, 44), (6, 43), (3, 43), (3, 42),
         (1, 40), (0, 39), (-1, 38), (-2, 37), (-6, 36), (-9, 36)],
        [(-5, 50), (-3, 51), (-1, 52), (-1, 54), (-2, 56), (-4, 58),
         (-6, 58), (-7, 57), (-6, 55), (-5, 53), (-4, 51), (-5, 50)],
        [(36, 31), (34, 28), (35, 24), (37, 21), (39, 18), (40, 15),
         (42, 13), (43, 12), (45, 12), (47, 13), (49, 14), (51, 15),
         (54, 16), (56, 18), (58, 20), (59, 22), (57, 24), (56, 26),
         (53, 26), (51, 25), (50, 27), (49, 29), (48, 30), (45, 29),
         (43, 30), (41, 31), (39, 32), (37, 34), (36, 36), (33, 36),
         (30, 36), (28, 37), (27, 39), (28, 41), (31, 41), (34, 42),
         (37, 42), (39, 41), (41, 43), (43, 42), (46, 42), (48, 42),
         (50, 44), (49, 46), (52, 46), (55, 48), (58, 50), (62, 53),
         (66, 56), (70, 60), (73, 64), (76, 67), (80, 70), (85, 71),
         (90, 72), (95, 73), (100, 73), (105, 74), (110, 74), (115, 73),
         (120, 73), (125, 72), (130, 72), (135, 72), (140, 72),
         (145, 71), (150, 71), (155, 70), (160, 70), (165, 69),
         (170, 67), (175, 66), (178, 66), (176, 64), (172, 62),
         (169, 60), (166, 60), (162, 61), (160, 57), (158, 53),
         (156, 51), (157, 54), (159, 58), (161, 60), (156, 59),
         (152, 60), (148, 59), (144, 57), (142, 54), (141, 51),
         (142, 48), (140, 47), (138, 46), (136, 45), (134, 44),
         (132, 43), (131, 42), (129, 40), (127, 39), (129, 37),
         (129, 35), (127, 34), (124, 34), (122, 36), (122, 38),
         (124, 39), (122, 37), (120, 34), (119, 32), (121, 29),
         (119, 26), (117, 24), (114, 22), (111, 21), (109, 19),
         (108, 17), (109, 15), (109, 13), (107, 11), (105, 8), (104, 5),
         (103, 1), (101, 3), (100, 6), (99, 9), (98, 12), (98, 15),
         (96, 16), (94, 17), (92, 22), (90, 22), (88, 21), (86, 20),
         (84, 19), (82, 17), (80, 15), (80, 13), (78, 10), (77, 8),
         (76, 11), (74, 14), (73, 17), (72, 20), (70, 22), (68, 23),
         (66, 24), (63, 25), (61, 25), (58, 26), (56, 27), (54, 27),
         (52, 28), (50, 29), (48, 30)],
        [(113, -22), (114, -26), (115, -31), (115, -34), (118, -35),
         (124, -33), (129, -32), (132, -32), (135, -35), (137, -35),
         (139, -37), (140, -38), (144, -38), (147, -38), (149, -37),
         (150, -36), (151, -33), (153, -30), (153, -27), (151, -24),
         (149, -20), (146, -19), (143, -15), (142, -11), (142, -13),
         (141, -17), (140, -18), (139, -17), (136, -15), (136, -12),
         (135, -12), (133, -11), (130, -12), (126, -14), (122, -17),
         (118, -20), (114, -21), (113, -22)],
        [(-6, 35), (-9, 32), (-13, 28), (-16, 24), (-17, 20), (-17, 16),
         (-16, 13), (-14, 10), (-12, 8), (-8, 5), (-5, 5), (-1, 5),
         (3, 6), (6, 4), (8, 4), (9, 2), (9, -1), (10, -4), (12, -6),
         (13, -10), (13, -14), (14, -18), (15, -22), (16, -26), (17, -29),
         (18, -32), (19, -34), (20, -35), (25, -34), (28, -33), (30, -31),
         (32, -29), (33, -26), (35, -23), (35, -20), (36, -17), (37, -14),
         (38, -11), (39, -8), (40, -5), (41, -2), (42, 0), (45, 4),
         (48, 8), (51, 10), (51, 12), (49, 12), (46, 11), (43, 12),
         (42, 13), (40, 15), (39, 18), (37, 21), (35, 23), (34, 26),
         (33, 28), (34, 29), (32, 31), (30, 31), (27, 31), (24, 32),
         (21, 32), (18, 32), (15, 32), (13, 33), (11, 34), (11, 36),
         (10, 37), (8, 37), (6, 37), (3, 37), (0, 36), (-2, 35),
         (-5, 35), (-6, 35)],
        [(44, -13), (46, -14), (48, -15), (50, -17), (50, -20), (48, -23),
         (46, -25), (44, -25), (43, -22), (43, -18), (44, -15), (44, -13)],
        [(167, -45), (170, -43), (173, -39), (176, -37), (178, -37),
         (175, -40), (172, -42), (169, -46), (167, -45)],
        [(95, 5), (97, 5), (99, 3), (101, 1), (103, -2), (105, -4),
         (106, -6), (104, -6), (102, -4), (100, -1), (98, 2), (96, 4),
         (95, 5)],
        [(109, 1), (110, 3), (113, 4), (116, 6), (118, 4), (119, 1),
         (117, -2), (114, -3), (111, -2), (109, 0), (109, 1)],
        [(106, -6), (108, -6), (111, -7), (114, -7), (114, -8), (111, -8),
         (108, -7), (106, -7), (106, -6)],
        [(119, 0), (120, 1), (121, 0), (120, -1), (121, -3), (120, -5),
         (119, -3), (119, -1), (119, 0)],
        [(131, -1), (134, -2), (137, -2), (140, -3), (143, -4), (146, -6),
         (148, -8), (150, -10), (148, -10), (145, -8), (142, -8),
         (139, -7), (136, -6), (133, -4), (131, -2), (131, -1)],
        [(117, 18), (119, 18), (121, 18), (122, 16), (121, 14), (122, 12),
         (123, 10), (125, 8), (126, 7), (124, 6), (122, 8), (121, 10),
         (120, 12), (119, 14), (118, 16), (117, 18)],
        [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
         (141, 38), (141, 40), (141, 42), (142, 43), (143, 44), (144, 44),
         (143, 42), (142, 41), (140, 39), (139, 37), (137, 35), (135, 34),
         (133, 33), (131, 32), (130, 31)],
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(203, 179, 133),
                  outline=(168, 146, 103))
    pins = [(1, 30.7, 36.9, -2, 2), (2, 46.7, 24.6, -5, 2),
            (3, -75.9, -10.9, 0, 0), (4, 30.5, 50.4, -3, -2),
            (5, 56.3, 26.6, 6, -3), (6, 51.4, 35.7, 5, -3),
            (7, -77.0, 38.9, 0, 0), (8, 116.4, 39.9, 0, -2),
            (9, 125.6, 7.1, 3, 2), (10, 149.1, -35.3, 0, 0),
            (11, -25.0, 26.0, 0, 0), (12, -115.1, 36.2, -2, 2),
            (13, 174.8, -41.3, -2, 0)]
    for num, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE, width=1)
        t = str(num)
        tf = font(SANS_B, 8 if num < 10 else 7)
        d.text((px - d.textlength(t, font=tf) / 2, py - 4), t, font=tf, fill=WHITE)


# --------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    speckle(d)

    # Top strip: red brand left, black facts right, black rule under
    d.rectangle([0, 0, W, 2], fill=RED)
    d.text((M, 6), "THE WORLD IN ONE DAY", font=font(SANS_B, 12), fill=RED)
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 10)), 7), right,
           font=font(SANS_B, 10), fill=INK)
    d.rectangle([M, 22, W - M, 25], fill=INK)

    # Giant date headline, fitted to the content width
    size = 80
    while size > 20 and d.textlength("Saturday 21 November 2026",
                                     font=font(SERIF_B, size)) > CW:
        size -= 2
    d.text((M, 27), "Saturday 21 November 2026", font=font(SERIF_B, size), fill=INK)

    # Italic subline naming the three leads
    sub = ("Climate summit runs past its deadline \u00b7 Five missiles shot "
           "down over Saudi Arabia \u00b7 A strong quake shakes Peru")
    d.text((M, 107), fit(d, sub, font(SERIF_I, 15), CW), font=font(SERIF_I, 15),
           fill=(70, 64, 56))

    # Stats strip: red dividers, serif numbers, small wrapped captions
    sy = 130
    colw = CW / len(STATS)
    for i, (num, cap) in enumerate(STATS):
        cx = M + colw * i
        d.rectangle([cx, sy + 4, cx + 3, sy + 40], fill=RED)
        nf = font(SERIF_B, 27)
        d.text((cx + 9, sy + 7), num, font=nf, fill=INK)
        nw = d.textlength(num, font=nf)
        tx = cx + 15 + nw
        ty = sy + 3
        for line in wrap(d, cap, font(SANS, 8), colw - (tx - cx) - 4, 3):
            d.text((tx, ty), line, font=font(SANS, 8), fill=GREY)
            ty += 11

    # Region-count bar with coloured labels under each segment
    by = 182
    total = sum(c for _, c, _ in REGIONS)
    bx = M
    seg_x = []
    for name, cnt, col in REGIONS:
        seg = CW * cnt / total
        d.rectangle([bx, by, bx + seg, by + 12], fill=col)
        seg_x.append(bx)
        bx += seg
    lx = M
    for (name, cnt, col), sx0 in zip(REGIONS, seg_x):
        label = "%s %d" % (name, cnt)
        f = font(SANS_B, 10)
        tw = d.textlength(label, font=f)
        px = max(sx0, lx)
        if px + tw > W - M:
            px = W - M - tw
        d.text((px, by + 15), label, font=f, fill=col)
        lx = px + tw + 9

    # Three lead panels
    ly = 216
    for i, story in enumerate(LEADS):
        hero_panel(d, img, M + i * 339, ly, 325, story, seed=101 + i)
        d = ImageDraw.Draw(img)

    # Ten smaller panels, five across in two rows
    xs = [M, M + 203, M + 406, M + 609, M + 812]
    for idx, story in enumerate(PANELS):
        row, col = divmod(idx, 5)
        small_panel(d, img, xs[col], 434 + row * 146, 192, story, seed=211 + idx)
        d = ImageDraw.Draw(img)

    # World map, bottom-left; ALSO list beside it
    d.text((M, 732), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    draw_map(d, M, 748, 336, 172)
    grain(img, (M, 748, M + 336, 748 + 172), amp=5, seed=307)
    d = ImageDraw.Draw(img)
    cap = "The number in each pin is the story numbered the same above."
    d.text((M, 924), fit(d, cap, font(SANS, 8), 336), font=font(SANS, 8), fill=GREY)

    ax = M + 352
    d.text((ax, 748), "ALSO ON SATURDAY 21 NOVEMBER 2026 \u2014 22 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    iy = 772
    for col in range(2):
        cx = ax + col * 328
        for i in range(11):
            num, head, src = ALSO[col * 11 + i]
            y = iy + i * 14
            d.text((cx, y), "%d" % num, font=font(SANS_B, 9), fill=RED)
            nx = cx + d.textlength("35 ", font=font(SANS_B, 9))
            line = "%s (%s)" % (head, src)
            d.text((nx, y), fit(d, line, font(SANS, 9), 328 - (nx - cx) - 6),
                   font=font(SANS, 9), fill=INK)

    # DATE CHECK box
    dy = 944
    d.rectangle([M, dy, W - M, dy + 40], outline=RED, width=2, fill=(253, 243, 238))
    d.text((M + 8, dy + 4), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
    ty = dy + 17
    for line in wrap(d, DATE_CHECK, font(SANS, 9), CW - 16, 2):
        d.text((M + 8, ty), line, font=font(SANS, 9), fill=(64, 44, 40))
        ty += 12

    # Closing line, left and right
    close_l = ("All 35 stories happened, or were first reported, on Saturday "
               "21 November 2026; official counts are credited to their sources.")
    d.text((M, 1000), close_l, font=font(SANS, 9), fill=GREY)
    close_r = "Every story names its source \u00b7 all pictures drawn for this page"
    d.text((W - M - d.textlength(close_r, font=font(SANS, 9)), 1000), close_r,
           font=font(SANS, 9), fill=GREY)
    return img


if __name__ == "__main__":
    img = render()
    img.save("frontpage.png", optimize=True)
    print("saved frontpage.png", img.size)
