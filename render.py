"""Render the front page for Saturday 21 November 2026 (round 2).

Draws a newspaper front page with PIL only: masthead, giant date
headline, lead stories, three drawn visual panels, a stats strip, a
region-count bar, nine medium drawn story cards, a simplified world map
with numbered pins, 36 numbered stories (headline + one-line summary +
source each), and a DATE CHECK box naming the 19/20-November near-misses
deliberately left out. Every story was verified against real reporting
dated 21 November 2026.
"""

import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (16, 32, 64)
RED = (178, 24, 24)
INK = (18, 18, 18)
GREY = (90, 90, 90)
PAPER = (252, 250, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


# (number, region, headline, summary, source)
# DATE DISCIPLINE (round 2): every story below happened, or was first
# reported, on Saturday 21 November 2026. The 19/20-November near-misses
# (Poland missiles, Kyiv bridges, Shenzhen declaration, ICJ Myanmar,
# Akvan landfall, Anthropic IPO, Denmark plot, UFO files, AI chips,
# H5N1 vaccine) are NOT stories here: they are listed, by name, in the
# DATE CHECK box at the foot of the page.
STORIES = [
    (1, "Europe", "COP31 still no deal as talks run into Saturday",
     "Third draft due Saturday morning; fossil fuels still out of the text.", "Reuters"),
    (2, "N. America", "Wall Street enters correction as AI rout deepens",
     "Nasdaq -5.28%; S&P -3.7%; Dow -950 as the AI sell-off wipes out 2026 gains.", "CNN"),
    (3, "Oceania", "Head's 123 seals Ashes opener in two days",
     "Australia chase 205 in 28.2 overs; Starc takes 10 wickets in the match.", "AP"),
    (4, "Europe", "US offers Ukraine NATO path for land",
     "Kushner floats membership for territory, WSJ reports.", "WSJ"),
    (5, "Europe", "NATO chief Rutte flies to Warsaw",
     "Poland seeks more Eastern Sentry forces.", "AP"),
    (6, "Africa", "ANC scrambles after worst-ever result",
     "Party holds 31% and a majority in one province.", "AP"),
    (7, "Middle East", "Israeli strikes kill six in Gaza",
     "Strikes hit Bureij camp and central Gaza.", "AFP"),
    (8, "Asia", "Sensex rallies nearly 898 points",
     "Indian shares close at 83,919.71; Nifty up 286.", "BSE"),
    (9, "Asia", "NSE now world's 5th-largest exchange",
     "India's NSE passes Nasdaq and Hong Kong.", "NSE / TOI"),
    (10, "Asia", "Indonesia fires may cost $30bn",
     "Losses among the highest on record.", "Copernicus"),
    (11, "Asia", "Pakistan beat Sri Lanka by 8 wickets",
     "Pakistan seal the series 1-0, first win in two years.", "The Nation"),
    (12, "Asia", "Cheetah gives birth to four cubs",
     "Four cubs born at Kuno National Park.", "TOI"),
    (13, "Europe", "France seeks UN Security Council meeting",
     "Paris calls the Council over the war in Ukraine.", "Reuters"),
    (14, "Europe", "EU earmarks \u20ac45bn in aid for Ukraine",
     "Provisional loan opens the way to using Russian assets.", "EU Commission"),
    (15, "Europe", "UK to send Ukraine 1,000 drones",
     "London pledges the drones in a \u00a3260m package for winter.", "UK Govt"),
    (16, "Europe", "UK retail sales strengthen",
     "Shoppers return as sales beat forecasts in October.", "Equiti"),
    (17, "Asia", "Malaysia to resettle 10,000 Rohingya",
     "Kuala Lumpur plans to move refugees to T\u00fcrkiye.", "Bernama"),
    (18, "Asia", "Pakistan climate minister arrives in Delhi",
     "Musadik Malik leads the delegation to the SCO dialogue forum.", "APP"),
    (19, "Asia", "Suicide bombing kills five in Pakistan",
     "Car bomb at a security checkpoint kills five, injures 13.", "AP"),
    (20, "Asia", "IFFI 2026 adds a new animation section",
     "Five international films in the festival's 57th edition.", "IFFI"),
    (21, "Asia", "South Korea probes top exam scorer",
     "Inquiry after an AI cheating confession in the national exam.", "Yonhap"),
    (22, "Middle East", "US sanctions four Iranians over oil money",
     "Treasury adds four men linked to handling Iranian oil revenues.", "US Treasury"),
    (23, "Middle East", "Tanker struck and ablaze in Strait of Hormuz",
     "UKMTO reports a strike and fire north of Khasab, Oman.", "UKMTO"),
    (24, "Middle East", "Israel hits Hezbollah site in Lebanon",
     "Jets strike in eastern Lebanon; olive trees uprooted near Khiam.", "NNA / IDF"),
    (25, "Middle East", "22,000+ children killed in Gaza, officials say",
     "Gaza officials put the child death toll past 22,000.", "Gaza officials"),
    (26, "Middle East", "Houthis threaten Saudi airspace",
     "Rebels say Saudi skies will become a 'scene of operations'.", "Daily Mail PK"),
    (27, "Africa", "Sudanese army strike kills 13 in West Kordofan",
     "Rights group says women and children are among the dead.", "Emergency Lawyers"),
    (28, "Africa", "UN warns of growing global hunger",
     "WFP says funding gaps may cut food aid for millions in 2027.", "WFP"),
    (29, "Africa", "UN gives $52m for children in crisis",
     "Fund backs schooling for children in war-hit countries.", "UN"),
    (30, "N. America", "Trump threatens tax on overseas data centres",
     "US firms building AI centres abroad face a 'tremendous tax'.", "Reuters"),
    (31, "N. America", "Trump attacks Fed, cites India's 7% growth",
     "President says US growth could hit 15-20% if rates were lower.", "White House"),
    (32, "N. America", "Banks report cyberattacks on vendors",
     "JPMorgan, Visa and Mastercard say providers were hit; networks safe.", "JPMorgan"),
    (33, "N. America", "Canadian retail sales strengthen",
     "Sales rise as shoppers spend despite the market rout.", "Equiti"),
    (34, "S. America", "Bolsonaro taken to hospital in pain",
     "Brazil's jailed ex-president hospitalised with severe abdominal pain.", "TOI / AP"),
    (35, "S. America", "Bukele seeks a third term in El Salvador",
     "President pushes another term bid while hitting gangs in Haiti.", "AP"),
    (36, "Oceania", "Women's Big Bash: Hobart hosts Thunder",
     "Hurricanes meet Sydney Thunder in the WBBL's 29th match.", "Cricket Aus"),
]

REGION_COUNTS = [("Europe", 7), ("Asia", 10), ("Middle East", 6),
                 ("Africa", 4), ("N. America", 5), ("S. America", 2),
                 ("Oceania", 2)]

STATS = [("5.28%", "Nasdaq's fall\nas AI rout bites"),
         ("123", "Head's runs\noff 83 balls"),
         ("31%", "ANC vote\nshare"),
         ("898", "Sensex points\ngained"),
         ("$30bn", "cost of\nIndonesia fires"),
         ("205", "runs chased\nat Perth")]

# Near-misses deliberately left out of the numbered stories, with the
# day they actually belong to. Two columns of five for the DATE CHECK box.
DATE_CHECK = [
    "Russian missiles in Poland — Fri 20 Nov",
    "Kyiv bridges hit — Fri 20 Nov",
    "Shenzhen 3-leader declaration — Thu 19 Nov",
    "ICJ ruling on Myanmar — Thu 19 Nov",
    "Cyclone Akvan landfall — Fri 20 Nov",
    "Anthropic IPO debut — Thu 19 Nov",
    "Denmark 'assassination plot' revealed — Fri 20 Nov",
    "Pentagon UFO files released — Fri 20 Nov",
    "US clears 900,000 AI chips for China — Thu 19 Nov",
    "H5N1 chicken vaccine launched — Fri 20 Nov",
]


def draw_panel_a(d, x, y, w, h):
    """Wall Street: a plunging red chart on a dark trading-floor board."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    for gy in range(1, 4):
        d.line([x + 8, y + gy * h // 4, x + w - 8, y + gy * h // 4],
               fill=(48, 56, 84), width=1)
    pts = [(x + 10, y + 14), (x + 60, y + 18), (x + 110, y + 12),
           (x + 160, y + 26), (x + 210, y + 34), (x + 250, y + 30),
           (x + 290, y + 52), (x + w - 12, y + h - 12)]
    d.line(pts, fill=(255, 70, 60), width=3, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 200, 90))
    d.rectangle([x + w - 92, y + 6, x + w - 8, y + 24], fill=(178, 24, 24))
    d.text((x + w - 87, y + 9), "-5.28%", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    for i, (bx, bh) in enumerate([(30, 18), (70, 14), (110, 22), (150, 12)]):
        d.rectangle([x + bx, y + h - 10 - bh, x + bx + 12, y + h - 10],
                    fill=(90, 160, 90) if i % 2 == 0 else (200, 60, 60))


def draw_panel_b(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 222))
    cx, cy, r = x + 60, y + h // 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 200),
              outline=NAVY, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(60, 120, 60), width=4)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(60, 120, 60), width=4)
    sx, sy = x + w - 60, y + 22
    d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=(255, 190, 40))
    for k in range(8):
        a = k * math.pi / 4
        d.line([sx + 17 * math.cos(a), sy + 17 * math.sin(a),
                sx + 24 * math.cos(a), sy + 24 * math.sin(a)],
               fill=(255, 190, 40), width=3)
    d.rectangle([x + 170, y + h - 26, x + w - 90, y + h - 12], fill=(120, 80, 50))
    for i, col in enumerate([(200, 40, 40), (40, 90, 200), (40, 160, 80)]):
        fx = x + 200 + i * 80
        d.line([fx, y + h - 26, fx, y + h - 50], fill=INK, width=2)
        d.polygon([(fx, y + h - 50), (fx + 30, y + h - 44), (fx, y + h - 38)], fill=col)


def draw_panel_c(d, x, y, w, h):
    """Ashes at Perth: green outfield, tan pitch, stumps and a red ball."""
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
    d.rectangle([x + 120, y + 4, x + w - 120, y + h - 4], fill=(205, 180, 130))
    d.ellipse([x + w - 60, y + 10, x + w - 20, y + 50], fill=(255, 210, 90),
              outline=(200, 150, 40), width=2)
    for sx in (x + 150, x + 158, x + 166):
        d.line([sx, y + h - 30, sx, y + h - 12], fill=(255, 240, 190), width=3)
    d.rectangle([x + 148, y + h - 32, x + 170, y + h - 30], fill=(160, 110, 60))
    d.ellipse([x + 240, y + h - 34, x + 252, y + h - 22], fill=RED,
              outline=(255, 255, 255), width=1)
    d.rectangle([x + 8, y + h - 24, x + 108, y + h - 6], fill=NAVY)
    d.text((x + 13, y + h - 21), "AUS 205/2", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    d.line([x + 200, y + 8, x + 260, y + 40], fill=(255, 255, 255), width=2)
    d.polygon([(x + 200, y + 8), (x + 214, y + 6), (x + 208, y + 20)],
              fill=(180, 140, 80))


def draw_icon(d, x, y, w, h, kind):
    """Small flat icon tile for a medium story card."""
    bg = {"flag": (16, 32, 64), "ballot": (40, 120, 80),
          "blast": (120, 40, 40), "chart": (24, 28, 44),
          "globe": (30, 110, 140), "flame": (180, 80, 20),
          "bat": (60, 140, 70), "cub": (150, 110, 60),
          "building": (90, 90, 110)}.get(kind, NAVY)
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    if kind == "flag":
        d.line([cx - 12, cy - 14, cx - 12, cy + 14], fill=(255, 255, 255), width=2)
        d.polygon([(cx - 12, cy - 14), (cx + 12, cy - 9), (cx - 12, cy - 4)],
                  fill=(255, 210, 90))
    elif kind == "ballot":
        d.rectangle([cx - 13, cy - 6, cx + 13, cy + 14], fill=(255, 255, 255))
        d.rectangle([cx - 13, cy - 6, cx + 13, cy - 1], fill=RED)
        d.line([cx - 8, cy + 5, cx - 2, cy + 11, cx + 10, cy - 3],
               fill=(40, 120, 80), width=3)
    elif kind == "blast":
        for k in range(8):
            a = k * math.pi / 4
            d.line([cx, cy, cx + 16 * math.cos(a), cy + 16 * math.sin(a)],
                   fill=(255, 220, 100), width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    elif kind == "chart":
        for i, bh in enumerate([8, 16, 12, 22]):
            d.rectangle([cx - 16 + i * 9, cy + 12 - bh, cx - 9 + i * 9, cy + 12],
                        fill=(90, 200, 120) if i % 2 == 0 else (255, 90, 80))
    elif kind == "globe":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(120, 190, 220),
                  outline=(255, 255, 255), width=2)
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 200, 340,
              fill=(40, 120, 60), width=3)
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 20, 160,
              fill=(40, 120, 60), width=3)
    elif kind == "flame":
        d.polygon([(cx, cy - 16), (cx + 10, cy - 2), (cx + 6, cy + 12),
                   (cx - 6, cy + 12), (cx - 10, cy - 2)], fill=(255, 210, 60))
        d.ellipse([cx - 4, cy + 2, cx + 4, cy + 12], fill=(255, 120, 30))
    elif kind == "bat":
        d.polygon([(cx - 4, cy - 16), (cx + 4, cy - 16), (cx + 4, cy + 2),
                   (cx - 4, cy + 2)], fill=(230, 200, 150))
        d.line([cx, cy + 2, cx, cy + 14], fill=(120, 80, 40), width=3)
        d.ellipse([cx + 10, cy + 8, cx + 18, cy + 16], fill=RED)
    elif kind == "cub":
        d.ellipse([cx - 8, cy - 2, cx + 8, cy + 14], fill=(255, 220, 160))
        for ox, oy in [(-10, -10), (0, -14), (10, -10)]:
            d.ellipse([cx + ox - 3, cy + oy - 3, cx + ox + 3, cy + oy + 3],
                      fill=(255, 220, 160))
    else:  # building: parliament / HQ columns
        d.rectangle([cx - 14, cy - 12, cx + 14, cy - 8], fill=(255, 255, 255))
        for i in range(4):
            d.rectangle([cx - 13 + i * 7, cy - 8, cx - 8 + i * 7, cy + 12],
                        fill=(255, 255, 255))
        d.rectangle([cx - 15, cy + 12, cx + 15, cy + 15], fill=(255, 255, 255))


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))

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
         (44, 29), (39, 21), (35, 28), (30, 31)],  # Asia
        [(113, -22), (129, -15), (136, -12), (142, -11), (147, -19),
         (153, -27), (150, -37), (140, -38), (130, -32), (120, -34),
         (114, -30), (113, -22)],  # Australia
        [(-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
         (35, 28), (38, 22), (43, 12), (48, 11), (51, 12), (48, 5),
         (42, -2), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35),
         (16, -29), (12, -18), (9, -2), (9, 4), (4, 6), (-8, 5),
         (-13, 8), (-17, 15), (-17, 21), (-16, 28), (-10, 31), (-6, 35)],
    ]
    for poly in continents:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(150, 190, 130),
                  outline=(90, 130, 90))
    # pins: (story no, lon, lat, display dx, dy) — offsets keep the
    # clustered European pins from overlapping each other.
    pins = [(1, 30, 36, 16, 10), (2, -74, 41, 0, 0), (3, 115, -32, 0, 0),
            (5, 19, 52, -4, -8), (6, 28, -26, 0, 0), (7, 34, 31, 12, -8),
            (8, 72, 19, 0, 0), (10, 113, -2, 0, 0)]
    for num, lon, lat, dx, dy in pins:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 6), str(num), font=font(SANS_B, 10),
               fill=(255, 255, 255))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 40], fill=NAVY)
    d.text((16, 5), "THE WORLD IN ONE DAY", font=font(SERIF_B, 25),
           fill=(255, 255, 255))
    tag = "36 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - 16 - d.textlength(tag, font=font(SANS_B, 11)), 13), tag,
           font=font(SANS_B, 11), fill=(200, 210, 230))

    # Giant date headline
    d.text((16, 44), "SATURDAY 21 NOVEMBER 2026",
           font=font(SERIF_B, 36), fill=INK)
    d.rectangle([16, 86, W - 16, 89], fill=RED)
    try:
        tick_f = font("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 12)
    except OSError:
        tick_f = font(SANS, 12)
    d.text((16, 93),
           "COP31 still deadlocked  •  Wall Street in correction  •  Rutte in Warsaw  •  Head's 123 wins the Ashes",
           font=tick_f, fill=GREY)

    # Lead story: COP31, a genuine Saturday story
    d.text((16, 112), "COP31 STILL NO DEAL AS TALKS RUN INTO SATURDAY",
           font=font(SERIF_B, 25), fill=INK)
    d.text((16, 140), "Third draft due Saturday morning in Antalya; fossil fuels still missing from the text as nearly 200 nations haggle on.",
           font=font(SANS, 12), fill=(40, 40, 40))

    # Second headline: Wall Street
    d.text((16, 158), "WALL STREET IN CORRECTION AS AI ROUT WIPES OUT THE YEAR'S GAINS",
           font=font(SERIF_B, 15), fill=INK)
    d.text((16, 176), "Nasdaq -5.28%; S&P -3.7%; Dow -950 as Nvidia sinks 14% and Anthropic falls 8.5%.",
           font=font(SANS, 11), fill=(40, 40, 40))

    # Three big visual panels
    panels = [
        (16, 190, "1  COP31: NO DEAL IN ANTALYA",
         "Talks spill into Saturday with no fossil-fuel language.", draw_panel_b),
        (346, 190, "2  WALL STREET: AI ROUT",
         "Nasdaq -5.28% in its worst week since 2020.", draw_panel_a),
        (676, 190, "3  ASHES: HEAD'S 123 WINS IT",
         "Australia chase 205 in 28.2 overs to win in two days.", draw_panel_c),
    ]
    for px, py, cap, sub, fn in panels:
        fn(d, px, py, 322, 70)
        d.text((px, py + 74), cap, font=font(SANS_B, 11), fill=INK)
        d.text((px, py + 88), sub, font=font(SANS, 10), fill=GREY)

    # Stats strip
    d.rectangle([16, 292, W - 16, 340], fill=NAVY)
    sw = (W - 32) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = 16 + sw * i
        d.text((cx + sw / 2 - d.textlength(num, font=font(SERIF_B, 22)) / 2, 296),
               num, font=font(SERIF_B, 22), fill=(255, 210, 90))
        for j, line in enumerate(label.split("\n")):
            d.text((cx + sw / 2 - d.textlength(line, font=font(SANS, 9)) / 2,
                    320 + j * 11), line, font=font(SANS, 9), fill=(220, 225, 235))
        if i:
            d.line([cx, 298, cx, 334], fill=(70, 90, 130), width=1)

    # Region-count bar
    d.text((16, 344), "STORIES BY REGION:", font=font(SANS_B, 12), fill=INK)
    rx = 16 + d.textlength("STORIES BY REGION:  ", font=font(SANS_B, 12))
    total = sum(c for _, c in REGION_COUNTS)
    bar_w = W - 16 - rx - 90
    bx = rx
    colors = [(178, 24, 24), (16, 32, 64), (176, 132, 24), (40, 120, 80),
              (90, 60, 140), (200, 90, 40), (30, 120, 160)]
    for (name, cnt), col in zip(REGION_COUNTS, colors):
        seg = bar_w * cnt / total
        d.rectangle([bx, 346, bx + seg, 360], fill=col)
        bx += seg
    d.text((W - 86, 344), "36 stories", font=font(SANS_B, 12), fill=INK)
    lx = rx
    for (name, cnt), col in zip(REGION_COUNTS, colors):
        d.rectangle([lx, 364, lx + 10, 374], fill=col)
        d.text((lx + 13, 363), "%s %d" % (name, cnt), font=font(SANS, 10), fill=INK)
        lx += 13 + d.textlength("%s %d" % (name, cnt), font=font(SANS, 10)) + 12

    # Nine medium drawn story cards (stories 4-12), 3x3 grid
    d.text((16, 378), "MORE FROM SATURDAY", font=font(SANS_B, 12), fill=INK)
    d.rectangle([16, 392, W - 16, 393], fill=NAVY)
    icons = ["flag", "building", "ballot", "blast", "chart", "globe",
             "flame", "bat", "cub"]
    for idx, s in enumerate(STORIES[3:12]):
        row, col = divmod(idx, 3)
        cx = 16 + col * 330
        cy = 396 + row * 58
        draw_icon(d, cx, cy, 54, 56, icons[idx])
        tx = cx + 60
        tw = 322 - 60 - 6
        d.text((tx, cy + 3), s[1].upper(), font=font(SANS_B, 9), fill=RED)
        d.text((tx + tw - d.textlength(s[4], font=font(SANS, 8)), cy + 4),
               s[4], font=font(SANS, 8), fill=GREY)
        d.text((tx, cy + 16), fit(d, s[2], font(SANS_B, 11), tw),
               font=font(SANS_B, 11), fill=INK)
        d.text((tx, cy + 31), fit(d, s[3], font(SANS, 9), tw),
               font=font(SANS, 9), fill=(60, 60, 60))
        d.text((tx, cy + 44), "%d." % s[0], font=font(SANS_B, 9), fill=RED)
        d.line([cx, cy + 55, cx + 322, cy + 55], fill=(220, 220, 210), width=1)

    # World map panel
    d.text((16, 570), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    draw_map(d, 16, 586, W - 32, 62)
    d.text((16, 650), "Pins match the numbered stories below.",
           font=font(SANS, 10), fill=GREY)

    # "Also on Saturday" — the remaining 24 numbered stories, two columns
    d.text((16, 664), "ALSO ON SATURDAY 21 NOVEMBER — 24 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.rectangle([16, 680, W - 16, 681], fill=NAVY)
    col_w = 484
    for col in range(2):
        cx = 16 + col * 508
        for i in range(12):
            s = STORIES[12 + col * 12 + i]
            y = 686 + i * 20
            num_txt = "%d." % s[0]
            d.text((cx, y), num_txt, font=font(SANS_B, 10), fill=RED)
            nx = cx + d.textlength("36. ", font=font(SANS_B, 10)) + 2
            head = fit(d, s[2], font(SANS_B, 10), col_w - (nx - cx) - 70)
            d.text((nx, y), head, font=font(SANS_B, 10), fill=INK)
            summ = fit(d, s[3], font(SANS, 9), col_w - (nx - cx))
            d.text((nx, y + 10), summ, font=font(SANS, 9), fill=(60, 60, 60))
            d.text((cx + col_w - d.textlength(s[4], font=font(SANS, 8)), y),
                   s[4], font=font(SANS, 8), fill=GREY)

    # DATE CHECK box: the near-misses we deliberately left out
    d.rectangle([16, 926, W - 16, 1002], outline=RED, width=2,
                fill=(255, 242, 240))
    d.text((24, 930), "DATE CHECK — WHAT WE LEFT OUT: THESE ARE NOT 21 NOVEMBER NEWS",
           font=font(SANS_B, 11), fill=RED)
    for i, item in enumerate(DATE_CHECK):
        col = i // 5
        row = i % 5
        d.text((24 + col * 500, 948 + row * 11), "× " + item,
               font=font(SANS, 9), fill=(60, 40, 40))

    # Footer
    d.text((16, 1006),
           "Every story here happened, or was first reported, on Saturday 21 November 2026. Claims are attributed, not stated as fact.",
           font=font(SANS, 10), fill=GREY)
    return img

if __name__ == "__main__":
    img = render()
    img.save("frontpage.png", optimize=True)
    print("saved frontpage.png", img.size)
