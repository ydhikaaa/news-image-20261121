"""Render the front page for Saturday 21 November 2026 (round 3).

Round 3 fixes the measured defect of round 1: its lead story was the
missile that landed in Poland, which belongs to Friday 20 November.
This page leads with the day's verified top stories instead (COP31 in
overtime, five missiles downed over Saudi Arabia, the Peru quake) and
names the Poland missile in the DATE CHECK box as 20-November news.

Layout follows the classic one-day front page: cream paper, a giant
serif date headline, a stats strip, a region-count bar, thirteen drawn
story panels with red banner labels, numbered kickers, serif headlines,
short summaries, source tags and verification badges, a world map with
numbered pins, a numbered ALSO list of the day's other stories, and a
DATE CHECK footer. PIL only, fully deterministic.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16
CW = W - 2 * M

PAPER = (250, 246, 236)
INK = (22, 20, 18)
RED = (176, 22, 22)
NAVY = (16, 32, 64)
GREY = (96, 90, 80)
FAINT = (203, 196, 182)
WHITE = (255, 255, 255)

BADGE_COLORS = {"CONFIRMED": (26, 118, 64), "OFFICIAL": (16, 32, 64),
                "REPORTED": (172, 116, 18)}

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


def speckle(d, count=26000):
    """Deterministic paper grain: hash-scattered single pixels."""
    for i in range(count):
        px = (i * 7919 + 104729) % W
        py = (i * 6271 + 31337) % H
        shade = 238 + (i * 31) % 10
        d.point((px, py), fill=(shade, shade - 4, shade - 18))


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
# (num, place, field, banner, headline, summary, source, badge, scene)
LEADS = [
    (1, "ANTALYA, TÜRKIYE", "CLIMATE", "COP31: OVERTIME",
     "Climate talks run into Saturday with no deal in sight",
     "On day 13, a draft that never mentions fossil fuels has split "
     "almost 200 countries; a third text is promised.",
     "AFP · Al Jazeera", "OFFICIAL", "cop31"),
    (2, "RIYADH · JIZAN", "WAR", "SAUDI: FIVE MISSILES DOWN",
     "Five Houthi missiles downed before dawn",
     "Three were destroyed over Riyadh and two over Jizan, a day "
     "after the coalition bombed Hodeidah port.",
     "AFP", "OFFICIAL", "missiles"),
    (3, "JUNÍN, PERU", "EARTHQUAKE", "PERU: QUAKE 6.7",
     "Magnitude 6.7 quake shakes central Peru",
     "Struck near Carhuamayo at 00:09 UTC, 108 km deep; felt in "
     "Lima, with no deaths and no tsunami risk.",
     "USGS · IGP", "CONFIRMED", "quake"),
]

PANELS = [
    (4, "KYIV", "WAR", "KYIV: WARNING",
     "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "He warns of more double-tap strikes to come.",
     "NBC", "REPORTED", "bridge"),
    (5, "STRAIT OF HORMUZ", "WAR", "HORMUZ: DRONE",
     "Iran says it shot down a US drone",
     "No confirmation from Washington.",
     "IRIB", "REPORTED", "hormuz"),
    (6, "TEHRAN", "DIPLOMACY", "IRAN: URANIUM",
     "Iran: uranium stock stays in the country",
     "The minister still sees a \u201cfair solution\u201d.",
     "Times of Israel", "OFFICIAL", "atom"),
    (7, "WASHINGTON", "TECHNOLOGY", "TRUMP: AI TAX",
     "Trump vows tax on data centres abroad",
     "A \u201ctremendous\u201d penalty; no details yet.",
     "ABC", "REPORTED", "aitax"),
    (8, "BEIJING", "DIPLOMACY", "CHINA\u2013JAPAN",
     "China tells Japan to \u201ccorrect\u201d Taiwan words",
     "Tokyo says its stance is unchanged.",
     "AFP", "OFFICIAL", "flags"),
    (9, "DAVAO", "AVIATION", "DAVAO: 146 SAFE",
     "Jet lands safely after engine fire alert",
     "All 146 safe; the flight diverted after midnight.",
     "AP", "OFFICIAL", "jet"),
    (10, "CANBERRA", "DIPLOMACY", "CANBERRA: AI TALKS",
     "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip.",
     "ABC", "OFFICIAL", "talks"),
    (11, "WORLD", "MARKETS", "BITCOIN: $58,983",
     "Bitcoin trades below $59,000 on Saturday",
     "Down 3.9% in a day; ether at $1,625.",
     "CoinGecko", "CONFIRMED", "bitcoin"),
    (12, "LAS VEGAS", "FORMULA 1", "RUSSELL: P1",
     "Russell fastest in final practice",
     "1:34.041 in a damp, messy session.",
     "Formula 1", "OFFICIAL", "f1"),
    (13, "WELLINGTON", "CRICKET", "RAHUL: 124*",
     "Rahul's 124 not out puts India on top",
     "India 344 for 2 at tea, replying to 368.",
     "AFP", "OFFICIAL", "cricket"),
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
    ("Day 13", "of COP31 in", "Antalya"),
    ("5", "missiles downed", "over Saudi Arabia"),
    ("6.7", "magnitude of", "the Peru quake"),
    ("146", "people safe after", "the Davao landing"),
    ("$58,983", "bitcoin early", "Sat, down 3.9%"),
    ("124*", "Rahul's score", "at tea, Wellington"),
]

REGIONS = [("Europe", 4, (176, 22, 22)), ("Asia", 10, (16, 32, 64)),
           ("Middle East", 5, (176, 132, 24)), ("Africa", 1, (40, 120, 80)),
           ("Americas", 11, (90, 60, 140)), ("Oceania", 3, (200, 90, 40)),
           ("Global", 1, (30, 120, 160))]

DATE_CHECK = (
    "Left out, because they belong to Friday 20 November: Wall Street's "
    "fall into correction, the Russian barrage on Kyiv's bridges, the "
    "missile that came down in Poland, the UK\u2013EU deal and Cyclone "
    "Akvan's landfall. Older still: Voyager 1's light-day (18 Nov). "
    "Not confirmed as this page was drawn: BepiColombo entering Mercury "
    "orbit, and any final COP31 text.")


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


def scene_cop31(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (204, 228, 211), (224, 240, 228))
    cx, cy, r = x + 66, y + h // 2 + 4, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 156, 208),
              outline=NAVY, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(52, 122, 62), width=5)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(52, 122, 62), width=5)
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 250, fill=(52, 122, 62), width=4)
    tx = x + 150
    d.rounded_rectangle([tx, y + 12, tx + 13, y + h - 24], 6,
                        fill=WHITE, outline=INK, width=2)
    d.rectangle([tx + 2, y + 34, tx + 11, y + h - 26], fill=RED)
    d.ellipse([tx - 4, y + h - 30, tx + 17, y + h - 9], fill=RED, outline=INK, width=2)
    for k in range(3):
        d.line([tx + 17, y + 22 + k * 14, tx + 24, y + 22 + k * 14], fill=INK, width=2)
    d.text((tx + 30, y + h - 32), "1.5\u00b0 LIMIT", font=font(SANS_B, 10), fill=RED)
    kx, ky, kr = x + w - 52, y + h // 2 + 4, 27
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE, outline=INK, width=2)
    d.line([kx, ky, kx, ky - 16], fill=INK, width=3)
    d.line([kx, ky, kx + 12, ky + 8], fill=INK, width=3)
    d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=RED)
    d.text((kx - 20, ky + kr + 3), "DAY 13", font=font(SANS_B, 9), fill=INK)


def scene_missiles(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (9, 13, 32), (34, 44, 84))
    for i in range(34):
        sx = x + (i * 61) % int(w)
        sy = y + (i * 37) % int(h * 0.55)
        d.point((sx, sy), fill=(200, 210, 235))
    base = y + h
    for bx, bw, bh in [(0, 34, 20), (40, 26, 30), (72, 40, 16), (150, 30, 24),
                       (190, 44, 18), (250, 28, 28), (286, 36, 15)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 11, 24))
        for wy in range(6, bh - 4, 7):
            for wx in range(4, bw - 4, 9):
                if (wx * 7 + wy * 13 + bx) % 3 == 0:
                    d.point((x + bx + wx, base - bh + wy), fill=(255, 205, 90))
    dashed_arc(d, x + 18, base - 16, x + w - 70, y + 26, 34, (255, 160, 80))
    dashed_arc(d, x + 60, base - 14, x + w - 130, y + 16, 40, (255, 190, 110))
    dashed_arc(d, x + 120, base - 18, x + w - 30, y + 40, 26, (255, 140, 70))
    burst(d, x + w - 70, y + 26, 11)
    burst(d, x + w - 130, y + 16, 9)
    burst(d, x + w - 30, y + 40, 8)


def scene_quake(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (238, 228, 204), (224, 208, 174))
    d.rectangle([x + 10, y + 16, x + 196, y + h - 16], fill=WHITE, outline=GREY, width=1)
    pts = []
    px = x + 16
    py = y + h // 2
    for dx, dy in [(14, 0), (10, -6), (8, 10), (8, -22), (8, 26), (8, -30),
                   (8, 18), (8, -8), (10, 4), (14, 0), (16, -3), (20, 0)]:
        px += dx
        py += dy
        pts.append((px, py))
    d.line([(x + 16, y + h // 2)] + pts, fill=RED, width=2, joint="curve")
    d.text((x + 14, y + 20), "6.7", font=font(SERIF_B, 15), fill=RED)
    for hx, tilt in [(x + 222, 0), (x + 272, 3)]:
        d.rectangle([hx, y + 44 + tilt, hx + 34, y + 72], fill=(206, 178, 138),
                    outline=INK, width=1)
        d.polygon([(hx - 4, y + 46 + tilt), (hx + 17, y + 26 + tilt),
                   (hx + 38, y + 46 + tilt)], fill=(150, 74, 52))
        d.rectangle([hx + 13, y + 56 + tilt, hx + 21, y + 72], fill=(90, 60, 40))
    d.line([x + 210, y + 78, x + 236, y + 84, x + 258, y + 79, x + 320, y + 86],
           fill=(120, 90, 60), width=2)


def scene_bridge(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (58, 78, 118), (102, 124, 164))
    d.rectangle([x, y + h - 9, x + w, y + h], fill=(38, 62, 104))
    deck = y + h - 14
    for tx in (x + w * 0.32, x + w * 0.68):
        d.rectangle([tx - 2, y + 3, tx + 2, deck], fill=(24, 30, 44))
    d.line([x + 4, y + 10, x + w * 0.32, y + 4, x + w * 0.68, y + 4, x + w - 4, y + 10],
           fill=(220, 226, 238), width=2)
    for i in range(1, 8):
        hx = x + i * w / 8
        d.line([hx, y + 8, hx, deck], fill=(160, 172, 196), width=1)
    d.line([x, deck, x + w, deck], fill=(16, 20, 30), width=3)


def scene_hormuz(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (34, 98, 120), (62, 138, 156))
    for i in range(5):
        wy = y + h - 6 - i * 3
        d.line([x + (i * 23) % 40, wy, x + (i * 23) % 40 + 26, wy],
               fill=(120, 190, 205), width=1)
    hx, hy = x + 26, y + h - 12
    d.polygon([(hx, hy - 8), (hx + 96, hy - 8), (hx + 84, hy), (hx + 10, hy)],
              fill=(30, 34, 44))
    for i, col in enumerate([(196, 70, 50), (60, 130, 190), (220, 160, 60)]):
        d.rectangle([hx + 12 + i * 24, hy - 19, hx + 32 + i * 24, hy - 9], fill=col)
    d.rectangle([hx + 82, hy - 24, hx + 94, hy - 9], fill=(225, 228, 232))
    dx, dy = x + w - 34, y + 10
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(20, 20, 20))
    for ox, oy in [(-9, -6), (9, -6), (-9, 6), (9, 6)]:
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
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 234))
    cx, cy = x + w // 2, y + h // 2
    _orbit(img, cx, cy, w // 3, h // 3, 0, (70, 90, 160))
    _orbit(img, cx, cy, w // 3, h // 3, 60, (70, 90, 160))
    _orbit(img, cx, cy, w // 3, h // 3, -60, (70, 90, 160))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def scene_aitax(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 35, 51))
    for i, rx in enumerate((x + 12, x + 40)):
        d.rectangle([rx, y + 6, rx + 22, y + h - 6], fill=(48, 58, 80),
                    outline=(90, 104, 132), width=1)
        for r in range(4):
            for c in range(2):
                col = (90, 210, 120) if (r + c + i) % 3 else (255, 180, 70)
                d.ellipse([rx + 4 + c * 10, y + 10 + r * 7, rx + 7 + c * 10,
                           y + 13 + r * 7], fill=col)
    gx, gy = x + w - 52, y + h // 2
    d.rectangle([gx - 13, gy - 13, gx + 13, gy + 13], fill=(70, 130, 180),
                outline=(200, 220, 240), width=1)
    d.rectangle([gx - 6, gy - 6, gx + 6, gy + 6], outline=(220, 235, 245), width=1)
    for k in range(-1, 2):
        d.line([gx + 16, gy + k * 8, gx + 22, gy + k * 8], fill=(200, 220, 240), width=2)
        d.line([gx - 22, gy + k * 8, gx - 16, gy + k * 8], fill=(200, 220, 240), width=2)
    d.text((x + 76, y + h - 13), "AI", font=font(SANS_B, 10), fill=(160, 200, 235))


def scene_flags(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 240))
    for px, fx, kind in [(x + 34, x + 36, "cn"), (x + w - 76, x + w - 74, "jp")]:
        d.line([px, y + 4, px, y + h - 3], fill=(70, 70, 70), width=2)
        fw, fh = 52, 24
        if kind == "cn":
            d.rectangle([fx, y + 5, fx + fw, y + 5 + fh], fill=(206, 32, 40),
                        outline=(150, 20, 28), width=1)
            d.ellipse([fx + 5, y + 9, fx + 11, y + 15], fill=(255, 214, 60))
            for ox, oy in [(13, 3), (15, 8), (13, 13), (10, 16)]:
                d.point((fx + ox, y + 5 + oy), fill=(255, 214, 60))
        else:
            d.rectangle([fx, y + 5, fx + fw, y + 5 + fh], fill=WHITE,
                        outline=(150, 150, 150), width=1)
            d.ellipse([fx + fw // 2 - 6, y + 11, fx + fw // 2 + 6, y + 23],
                      fill=(206, 32, 40))


def scene_jet(d, img, x, y, w, h):
    vgrad(d, x, y, w, h, (146, 190, 230), (196, 224, 246))
    cy = y + h // 2 + 2
    d.rounded_rectangle([x + 18, cy - 8, x + w - 34, cy + 7], 7, fill=WHITE,
                        outline=(120, 140, 165), width=1)
    d.polygon([(x + w - 34, cy - 8), (x + w - 14, cy - 2), (x + w - 14, cy + 3),
               (x + w - 34, cy + 7)], fill=WHITE, outline=(120, 140, 165))
    d.polygon([(x + 22, cy - 8), (x + 34, cy - 22), (x + 46, cy - 22),
               (x + 44, cy - 8)], fill=RED)
    d.polygon([(x + 78, cy + 5), (x + 104, cy + 16), (x + 118, cy + 16),
               (x + 104, cy + 5)], fill=(150, 165, 185))
    for i in range(9):
        d.ellipse([x + 34 + i * 12, cy - 4, x + 38 + i * 12, cy], fill=(70, 110, 160))
    d.rectangle([x + 84, cy + 12, x + 98, cy + 16], fill=(90, 100, 115))


def scene_talks(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 239, 224))
    d.rounded_rectangle([x + 18, y + 6, x + 84, y + 26], 6, fill=WHITE, outline=INK, width=1)
    d.polygon([(x + 30, y + 26), (x + 38, y + 26), (x + 30, y + 33)], fill=WHITE, outline=INK)
    d.rounded_rectangle([x + w - 84, y + 12, x + w - 18, y + 32], 6, fill=WHITE,
                        outline=INK, width=1)
    d.polygon([(x + w - 38, y + 32), (x + w - 30, y + 32), (x + w - 30, y + 38)],
              fill=WHITE, outline=INK)
    for bx in (x + 32, x + 48, x + 64):
        d.ellipse([bx, y + 13, bx + 5, y + 18], fill=(90, 140, 200))
    for bx in (x + w - 64, x + w - 48, x + w - 32):
        d.ellipse([bx, y + 19, bx + 5, y + 24], fill=(200, 90, 80))


def scene_bitcoin(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(21, 25, 39))
    tops = [10, 14, 20, 26]
    for i, tp in enumerate(tops):
        cx = x + 14 + i * 20
        col = (235, 80, 70) if i % 2 else (90, 190, 110)
        d.line([cx + 4, y + tp - 4, cx + 4, y + tp + 13], fill=col, width=1)
        d.rectangle([cx, y + tp, cx + 8, y + tp + 9], fill=col)
    d.line([x + 12, y + 8, x + 92, y + 30], fill=(235, 80, 70), width=2)
    cx, cy = x + w - 34, y + h // 2
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(240, 150, 40))
    d.text((cx - 5, cy - 8), "B", font=font(SANS_B, 13), fill=WHITE)


def scene_f1(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(118, 118, 124))
    d.line([x, y + h - 7, x + w, y + h - 7], fill=(70, 70, 74), width=2)
    by = y + h - 12
    d.polygon([(x + 30, by - 6), (x + 66, by - 10), (x + 118, by - 8),
               (x + 140, by - 3), (x + 140, by), (x + 30, by)], fill=(178, 24, 24))
    d.rectangle([x + 26, by - 16, x + 32, by - 4], fill=(40, 40, 44))
    d.rectangle([x + 20, by - 17, x + 44, by - 14], fill=(40, 40, 44))
    d.rectangle([x + 128, by - 5, x + 150, by - 2], fill=(40, 40, 44))
    d.arc([x + 74, by - 16, x + 98, by - 2], 180, 360, fill=(30, 30, 34), width=3)
    for wx in (x + 44, x + 122):
        d.ellipse([wx - 8, by - 8, wx + 8, by + 8], fill=(15, 15, 15))
        d.ellipse([wx - 3, by - 3, wx + 3, by + 3], fill=(150, 150, 155))


def scene_cricket(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(66, 148, 78))
    d.rectangle([x + 30, y + h - 12, x + w - 30, y + h - 4], fill=(206, 182, 132))
    sx = x + w - 44
    for k in range(3):
        d.line([sx + k * 6, y + 12, sx + k * 6, y + 27], fill=(240, 230, 190), width=2)
    d.line([sx, y + 11, sx + 5, y + 13], fill=(240, 230, 190), width=2)
    d.line([sx + 7, y + 11, sx + 12, y + 13], fill=(240, 230, 190), width=2)
    d.polygon([(x + 40, y + 26), (x + 46, y + 24), (x + 66, y + 6), (x + 60, y + 4)],
              fill=(228, 198, 148), outline=(150, 116, 70))
    d.line([x + 63, y + 5, x + 70, y - 1 + 5], fill=(110, 78, 44), width=3)
    d.ellipse([x + 96, y + 8, x + 106, y + 18], fill=RED, outline=WHITE, width=1)


SCENES = {"cop31": scene_cop31, "missiles": scene_missiles, "quake": scene_quake,
          "bridge": scene_bridge, "hormuz": scene_hormuz, "atom": scene_atom,
          "aitax": scene_aitax, "flags": scene_flags, "jet": scene_jet,
          "talks": scene_talks, "bitcoin": scene_bitcoin, "f1": scene_f1,
          "cricket": scene_cricket}


# --------------------------------------------------------------- panels
def banner(d, x, y, w, text, fh, fs):
    d.rectangle([x, y, x + w, y + fh], fill=RED)
    d.text((x + 5, y + fh // 2 - fs // 2 - 1), text, font=font(SANS_B, fs), fill=WHITE)


def badge_chip(d, x_right, y, text):
    f = font(SANS_B, 8)
    tw = d.textlength(text, font=f)
    d.rectangle([x_right - tw - 8, y, x_right, y + 12], fill=BADGE_COLORS[text])
    d.text((x_right - tw - 4, y + 2), text, font=f, fill=WHITE)


def source_chip(d, x_right, y, text):
    f = font(SANS_B, 8)
    tw = d.textlength(text, font=f)
    d.rectangle([x_right - tw - 8, y, x_right, y + 13], fill=(28, 28, 28))
    d.text((x_right - tw - 4, y + 2), text, font=f, fill=WHITE)


def lead_panel(d, img, x, y, w, story):
    num, place, field, ban, head, summ, src, badge, scene = story
    SCENES[scene](d, img, x, y, w, 88)
    d.rectangle([x, y, x + w, y + 88], outline=FAINT, width=1)
    banner(d, x, y, w, ban, 17, 11)
    source_chip(d, x + w, y + 88 - 13, src)
    ky = y + 94
    d.ellipse([x, ky, x + 14, ky + 14], fill=RED)
    d.text((x + 7 - d.textlength(str(num), font=font(SANS_B, 9)) / 2, ky + 2),
           str(num), font=font(SANS_B, 9), fill=WHITE)
    d.text((x + 19, ky + 2), "%s · %s" % (place, field), font=font(SANS_B, 9), fill=RED)
    badge_chip(d, x + w, ky + 1, badge)
    hy = ky + 18
    for line in wrap(d, head, font(SERIF_B, 16), w, 2):
        d.text((x, hy), line, font=font(SERIF_B, 16), fill=INK)
        hy += 19
    sy = y + 152
    for line in wrap(d, summ, font(SANS, 10), w, 3):
        d.text((x, sy), line, font=font(SANS, 10), fill=(52, 50, 46))
        sy += 13


def small_panel(d, img, x, y, w, story):
    num, place, field, ban, head, summ, src, badge, scene = story
    SCENES[scene](d, img, x, y, w, 36)
    d.rectangle([x, y, x + w, y + 36], outline=FAINT, width=1)
    banner(d, x, y, w, ban, 11, 8)
    ky = y + 40
    kick = "%d · %s · %s" % (num, place, field)
    d.text((x, ky), fit(d, kick, font(SANS_B, 8), w), font=font(SANS_B, 8), fill=RED)
    hy = ky + 11
    for line in wrap(d, head, font(SERIF_B, 11), w, 2):
        d.text((x, hy), line, font=font(SERIF_B, 11), fill=INK)
        hy += 13
    sy = hy + 2
    for line in wrap(d, summ, font(SANS, 8), w, 2):
        d.text((x, sy), line, font=font(SANS, 8), fill=(52, 50, 46))
        sy += 10
    by = y + 106
    d.text((x, by), "(%s)" % src, font=font(SANS, 8), fill=GREY)
    bw = d.textlength(badge, font=font(SANS_B, 8))
    d.text((x + w - bw, by), badge, font=font(SANS_B, 8), fill=BADGE_COLORS[badge])


# ----------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    vgrad(d, x, y, w, h, (186, 210, 229), (210, 227, 241))

    def proj(lon, lat):
        return (x + (lon + 170) / 360.0 * w, y + (75 - lat) / 130.0 * h)

    continents = [
        [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 62),
         (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 26),
         (-105, 30), (-117, 33), (-125, 40), (-125, 49), (-140, 60),
         (-155, 58), (-168, 66)],
        [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -22),
         (-48, -28), (-58, -35), (-65, -41), (-70, -30), (-77, -12),
         (-80, 0), (-80, 10)],
        [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55),
         (18, 56), (21, 55), (24, 59), (30, 60), (28, 71), (40, 68),
         (32, 60), (28, 45), (23, 40), (19, 42), (12, 44), (3, 43),
         (-2, 37), (-10, 36)],
        [(30, 31), (35, 36), (43, 41), (48, 42), (52, 46), (60, 46),
         (68, 44), (75, 40), (80, 35), (90, 30), (97, 28), (100, 20),
         (105, 10), (108, 2), (104, -5), (100, 5), (98, 16), (94, 17),
         (91, 22), (88, 22), (85, 19), (80, 15), (77, 8), (73, 16),
         (68, 23), (62, 25), (57, 26), (52, 26), (50, 29), (48, 30),
         (44, 29), (39, 21), (35, 28), (30, 31)],
        [(113, -22), (129, -15), (136, -12), (142, -11), (147, -19),
         (153, -27), (150, -37), (140, -38), (130, -32), (120, -34),
         (114, -30), (113, -22)],
        [(-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
         (35, 28), (38, 22), (43, 12), (48, 11), (51, 12), (48, 5),
         (42, -2), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35),
         (16, -29), (12, -18), (9, -2), (9, 4), (4, 6), (-8, 5),
         (-13, 8), (-17, 15), (-17, 21), (-16, 28), (-10, 31), (-6, 35)],
        [(167, -45), (170, -43), (173, -39), (176, -37), (178, -37),
         (175, -40), (172, -42), (169, -46), (167, -45)],  # New Zealand
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(148, 188, 128),
                  outline=(92, 132, 92))
    # (story number, lon, lat, dx, dy) — offsets declutter Europe/Asia.
    pins = [(1, 30.7, 36.9, -3, 7), (2, 46.7, 24.6, 5, 6), (3, -75.9, -10.9, 0, 0),
            (4, 30.5, 50.4, -4, -5), (5, 56.3, 26.6, 9, -3), (6, 51.4, 35.7, 7, -7),
            (7, -77.0, 38.9, 0, 0), (8, 116.4, 39.9, 0, -3), (9, 125.6, 7.1, 2, 5),
            (10, 149.1, -35.3, 0, 0), (11, -25.0, 26.0, 0, 0),
            (12, -115.1, 36.2, -2, 2), (13, 174.8, -41.3, -3, 0)]
    for num, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE, width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=font(SANS_B, 8)) / 2, py - 4), t,
               font=font(SANS_B, 8), fill=WHITE)


# --------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    speckle(d)

    # Top strip
    d.rectangle([0, 0, W, 3], fill=RED)
    d.text((M, 8), "THE WORLD IN ONE DAY", font=font(SANS_B, 11), fill=RED)
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 10)), 9), right,
           font=font(SANS_B, 10), fill=INK)
    d.rectangle([M, 25, W - M, 27], fill=INK)

    # Giant date headline, fitted to the content width
    size = 78
    while size > 20 and d.textlength("Saturday 21 November 2026",
                                     font=font(SERIF_B, size)) > CW:
        size -= 2
    d.text((M, 31), "Saturday 21 November 2026", font=font(SERIF_B, size), fill=INK)

    # Italic subline naming the three leads
    sub = ("Climate summit runs past its deadline \u00b7 Five missiles shot "
           "down over Saudi Arabia \u00b7 A strong quake shakes Peru")
    d.text((M, 102), fit(d, sub, font(SERIF_I, 15), CW), font=font(SERIF_I, 15),
           fill=(70, 64, 56))

    # Stats strip
    sy = 124
    d.rectangle([M, sy, W - M, sy + 42], outline=FAINT, width=1)
    colw = CW / len(STATS)
    for i, (num, cap1, cap2) in enumerate(STATS):
        cx = M + colw * i
        d.rectangle([cx, sy + 5, cx + 3, sy + 37], fill=RED)
        nf = font(SERIF_B, 23)
        d.text((cx + 8, sy + 9), num, font=nf, fill=INK)
        tx = cx + 12 + d.textlength(num, font=nf)
        d.text((tx, sy + 8), cap1, font=font(SANS, 8), fill=GREY)
        d.text((tx, sy + 19), cap2, font=font(SANS, 8), fill=GREY)

    # Region-count bar
    by = 174
    total = sum(c for _, c, _ in REGIONS)
    bx = M
    for name, cnt, col in REGIONS:
        seg = CW * cnt / total
        d.rectangle([bx, by, bx + seg, by + 12], fill=col)
        bx += seg
    lx = M
    for name, cnt, col in REGIONS:
        d.rectangle([lx, by + 16, lx + 9, by + 25], fill=col)
        label = "%s %d" % (name, cnt)
        d.text((lx + 12, by + 15), label, font=font(SANS, 9), fill=INK)
        lx += 12 + d.textlength(label, font=font(SANS, 9)) + 14

    # Three lead panels
    ly = 210
    for i, story in enumerate(LEADS):
        lead_panel(d, img, M + i * 335, ly, 322, story)

    # Ten smaller panels, five across in two rows
    py = 418
    xs = [M, M + 201, M + 402, M + 603, M + 804]
    for idx, story in enumerate(PANELS):
        row, col = divmod(idx, 5)
        small_panel(d, img, xs[col], py + row * 130, 188, story)

    # Badge legend
    legend = ("HOW WE CHECKED \u2014 CONFIRMED: two or more outlets \u00b7 "
              "OFFICIAL: on the record \u00b7 REPORTED: one outlet's account")
    d.text(((W - d.textlength(legend, font=font(SANS, 9))) / 2, 682), legend,
           font=font(SANS, 9), fill=GREY)

    # World map
    d.text((M, 698), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    cap = "Pins match the numbered stories 1\u201313."
    d.text((W - M - d.textlength(cap, font=font(SANS, 9)), 700), cap,
           font=font(SANS, 9), fill=GREY)
    draw_map(d, M, 714, CW, 78)

    # ALSO list, stories 14-35 in two columns
    ay = 802
    d.text((M, ay), "ALSO ON SATURDAY 21 NOVEMBER 2026 \u2014 22 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.rectangle([M, ay + 16, W - M, ay + 17], fill=RED)
    iy = ay + 24
    for col in range(2):
        cx = M + col * 504
        for i in range(11):
            num, head, src = ALSO[col * 11 + i]
            y = iy + i * 11
            d.text((cx, y), "%d" % num, font=font(SANS_B, 9), fill=RED)
            nx = cx + d.textlength("35 ", font=font(SANS_B, 9))
            line = "%s (%s)" % (head, src)
            d.text((nx, y), fit(d, line, font(SANS, 9), 504 - (nx - cx) - 8),
                   font=font(SANS, 9), fill=INK)

    # DATE CHECK box
    dy = 950
    d.rectangle([M, dy, W - M, dy + 46], outline=RED, width=2, fill=(255, 243, 240))
    d.text((M + 8, dy + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=font(SANS_B, 10), fill=RED)
    ty = dy + 19
    for line in wrap(d, DATE_CHECK, font(SANS, 8), CW - 16, 2):
        d.text((M + 8, ty), line, font=font(SANS, 8), fill=(64, 44, 40))
        ty += 10

    # Closing line
    close = ("Every story here happened, or was first reported, on Saturday "
             "21 November 2026. Sources are named beside each story; the "
             "pictures are original drawings.")
    d.text(((W - d.textlength(close, font=font(SANS, 9))) / 2, 1004), close,
           font=font(SANS, 9), fill=GREY)
    return img


if __name__ == "__main__":
    img = render()
    img.save("frontpage.png", optimize=True)
    print("saved frontpage.png", img.size)
