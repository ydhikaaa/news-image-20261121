"""Render the front page for Saturday 21 November 2026.

Draws a newspaper front page with PIL only: masthead, giant date
headline, lead stories, four drawn visual panels, a stats strip, a
region-count bar, a simplified world map with numbered pins, and 36
numbered stories (headline + one-line summary + source each). Every
story was verified against real reporting dated 21 November 2026.
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
STORIES = [
    (1, "Europe", "Russian missiles land in Poland",
     "Two missiles and a suspected drone come down; drills held nearby.", "SCMP"),
    (2, "Europe", "Eight killed as Russia strikes Ukraine",
     "Strikes hit Kyiv and Kryvyi Rih; a child and a paramedic die.", "NDTV"),
    (3, "Europe", "Denmark foils plot to kill Ukrainian rapper",
     "Two arrested; Russian diplomat expelled over assassination plan.", "NYT / AFP"),
    (4, "Europe", "Estonia shuts border crossings to Russia",
     "Tallinn closes road crossings after a suspected arson attack.", "AP"),
    (5, "Europe", "France seeks UN Security Council meeting",
     "Paris calls the Council after strikes kill eight in Kyiv.", "Reuters"),
    (6, "Europe", "EU earmarks \u20ac45bn in aid for Ukraine",
     "Provisional loan opens the way to using Russian assets.", "EU Commission"),
    (7, "Europe", "UK to send Ukraine 1,000 drones",
     "London pledges the drones in a \u00a3260m package for winter.", "UK Govt"),
    (8, "Asia", "Cyclone Akvan crosses India's east coast",
     "Storm makes landfall near Gopalpur with heavy rain, strong winds.", "IMD / TOI"),
    (9, "Asia", "World reacts to ICJ ruling on Myanmar",
     "Rights groups demand action after the court finds Myanmar liable.", "ICJ / AP"),
    (10, "Asia", "Sensex rallies nearly 898 points",
     "Indian shares close at 83,919.71; Nifty rises 286 to 25,800.60.", "BSE"),
    (11, "Asia", "NSE becomes world's 5th-largest exchange",
     "India's NSE passes Nasdaq and Hong Kong in market value.", "NSE / TOI"),
    (12, "Asia", "Indonesia fires may cost $30bn",
     "Losses from the fires are among the highest on record.", "Copernicus"),
    (13, "Asia", "Suicide bombing kills five in Pakistan",
     "Car bomb at a security checkpoint kills five, injures 13.", "AP"),
    (14, "Asia", "Nepal PM to visit India on 22-23 Nov",
     "Balendra Shah's first visit to Delhi is announced ahead of it.", "MEA"),
    (15, "Asia", "Malaysia to resettle 10,000 Rohingya",
     "Kuala Lumpur plans to move refugees to T\u00fcrkiye.", "Bernama"),
    (16, "Middle East", "Israeli strikes kill six in Gaza",
     "Strikes hit Bureij camp and central Gaza despite the ceasefire.", "AFP"),
    (17, "Middle East", "Blasts heard in Riyadh; missiles intercepted",
     "Saudi Arabia says it shot down three Houthi missiles.", "AFP"),
    (18, "Middle East", "Trump: Iran wants a deal, rejects my terms",
     "President says Tehran seeks a deal to end the war, not on his terms.", "White House"),
    (19, "Middle East", "US sanctions four Iranians over oil money",
     "Treasury adds four men linked to handling Iranian oil revenues.", "US Treasury"),
    (20, "Middle East", "Tanker struck and ablaze in Strait of Hormuz",
     "UKMTO reports a strike and fire north of Khasab, Oman.", "UKMTO"),
    (21, "Middle East", "Israel hits Hezbollah site in Lebanon",
     "Jets strike in eastern Lebanon; olive trees uprooted near Khiam.", "NNA / IDF"),
    (22, "Middle East", "22,000+ children killed in Gaza, officials say",
     "Gaza officials put the child death toll past 22,000.", "Gaza officials"),
    (23, "Africa", "Sudanese army strike kills 13 in West Kordofan",
     "Rights group says women and children are among the dead.", "Emergency Lawyers"),
    (24, "Africa", "UN warns of growing global hunger",
     "WFP says funding gaps may cut food aid for millions in 2027.", "WFP"),
    (25, "Africa", "UN gives $52m for children in crisis",
     "Fund backs schooling for children in war-hit countries.", "UN"),
    (26, "Africa", "Rabada ruled out of India Test",
     "South Africa's spearhead misses Guwahati with a rib injury.", "Cricket SA"),
    (27, "N. America", "Trump threatens tax on overseas data centres",
     "US firms building AI centres abroad face a 'tremendous tax'.", "Reuters"),
    (28, "N. America", "Trump attacks Fed, cites India's 7% growth",
     "President says US growth could hit 15-20% if rates were lower.", "White House"),
    (29, "N. America", "Banks report cyberattacks on vendors",
     "JPMorgan, Visa and Mastercard say providers were hit; networks safe.", "JPMorgan"),
    (30, "N. America", "Trump pardons baseball star Pete Rose",
     "Posthumous pardon for the late hits leader is announced.", "White House"),
    (31, "N. America", "Trump: bring back Nvidia chief Huang",
     "President says the ousted Nvidia CEO should return to his job.", "Reuters"),
    (32, "S. America", "Bolsonaro taken to hospital in pain",
     "Brazil's jailed ex-president hospitalised with severe abdominal pain.", "TOI / AP"),
    (33, "S. America", "Bukele seeks a third term in El Salvador",
     "President pushes another term bid while hitting gangs in Haiti.", "AP"),
    (34, "Oceania", "Ashes: Starc takes 7 for 58 at Perth",
     "England 172 all out; Stokes hits back with 5 for 23.", "ESPNcricinfo"),
    (35, "Oceania", "India fight back in Wellington Test",
     "Jaiswal and Rahul lift India to 159/1, trailing by 209 runs.", "ESPNcricinfo"),
    (36, "Oceania", "Women's Big Bash: Hobart hosts Thunder",
     "Hurricanes meet Sydney Thunder in the WBBL's 29th match.", "Cricket Aus"),
]

REGION_COUNTS = [("Europe", 7), ("Asia", 8), ("Middle East", 7),
                 ("Africa", 4), ("N. America", 5), ("S. America", 2),
                 ("Oceania", 3)]

STATS = [("2", "missiles land\nin Poland"),
         ("8", "killed in\nUkraine strikes"),
         ("42", "injured in\nKryvyi Rih"),
         ("898", "points gained\nby the Sensex"),
         ("7/58", "Starc's Ashes\nfigures at Perth"),
         ("$30bn", "cost of\nIndonesia fires")]


def draw_panel_a(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 70))
    for bx, bw, bh in [(8, 40, 30), (56, 30, 42), (94, 46, 24), (148, 34, 38),
                       (190, 40, 26), (238, 30, 34), (276, 44, 22), (328, 36, 32)]:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + bw, y + h - 14],
                    fill=(70, 80, 110))
        d.rectangle([x + bx + 5, y + h - 12 - bh, x + bx + 9, y + h - 8 - bh],
                    fill=(255, 220, 120))
    cx, cy = x + w - 70, y + 24
    for r, col in [(24, (255, 200, 60)), (16, (255, 120, 30)), (9, (255, 240, 200))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(16, 32, 64))


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
    d.rectangle([x, y, x + w, y + h], fill=(180, 205, 225))
    cx, cy = x + 70, y + h // 2 + 4
    for k in range(3):
        rr = 8 + k * 9
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], k * 40, k * 40 + 220,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=NAVY)
    for i in range(14):
        rx = x + 150 + (i * 23) % (w - 170)
        ry = y + 8 + (i * 13) % (h - 20)
        d.line([rx, ry, rx - 4, ry + 9], fill=(60, 100, 160), width=2)
    d.polygon([(x + 130, y + h), (x + w, y + h), (x + w, y + h - 22),
               (x + 220, y + h - 16), (x + 170, y + h - 8)], fill=(60, 120, 70))


def draw_panel_d(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
    d.rectangle([x + 150, y + 5, x + 340, y + h - 5], fill=(210, 190, 140))
    for sx in (x + 168, x + 174, x + 180):
        d.line([sx, y + 14, sx, y + 30], fill=(255, 230, 150), width=3)
    for sx in (x + 316, x + 322, x + 328):
        d.line([sx, y + h - 30, sx, y + h - 14], fill=(255, 230, 150), width=3)
    d.polygon([(x + 60, y + 18), (x + 78, y + 14), (x + 96, y + 48),
               (x + 80, y + 54)], fill=(190, 140, 80))
    d.line([x + 66, y + 16, x + 52, y + 8], fill=(120, 80, 40), width=5)
    d.ellipse([x + 250, y + 28, x + 264, y + 42], fill=RED)
    d.rectangle([x + w - 118, y + 6, x + w - 10, y + 30], fill=NAVY)
    d.text((x + w - 112, y + 10), "ENG 172", font=font(SANS_B, 13), fill=(255, 255, 255))


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
    pins = [(1, 19, 52, 8, 0), (2, 31, 49, 10, -2), (3, 10, 56, -12, -4),
            (6, 15, 50, 0, 12), (8, 85, 21, 0, 0), (16, 34, 31, 0, 0),
            (17, 47, 25, 0, 0), (23, 30, 13, 0, 0)]
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
    d.rectangle([0, 0, W, 42], fill=NAVY)
    d.text((16, 6), "THE WORLD TODAY", font=font(SERIF_B, 26), fill=(255, 255, 255))
    tag = "ONE DAY  •  ONE PAGE  •  36 STORIES"
    d.text((W - 16 - d.textlength(tag, font=font(SANS_B, 12)), 13), tag,
           font=font(SANS_B, 12), fill=(200, 210, 230))

    # Giant date headline
    d.text((16, 48), "SATURDAY 21 NOVEMBER 2026",
           font=font(SERIF_B, 38), fill=INK)
    d.rectangle([16, 92, W - 16, 96], fill=RED)
    d.text((16, 100), "The world in one page: war, climate, markets, sport — as reported on 21 November 2026.",
           font=font(SANS, 12), fill=GREY)

    # Lead story
    d.text((16, 120), "RUSSIAN MISSILES LAND IN POLAND",
           font=font(SERIF_B, 28), fill=INK)
    d.text((16, 150), "Two missiles come down in Poland as Russia's biggest strikes in weeks kill eight in Ukraine.",
           font=font(SANS, 13), fill=(40, 40, 40))

    # Second headline
    d.text((16, 172), "TRUMP: PUTIN IS MY FRIEND — AND FIRMS FACE TAX IF THEY BUILD ABROAD",
           font=font(SERIF_B, 16), fill=INK)
    d.text((16, 192), "After his Asia trip, the president praises Putin and Xi, attacks the Fed and threatens a tax on US firms building data centres overseas.",
           font=font(SANS, 11), fill=(40, 40, 40))

    # 2x2 visual panels
    panels = [
        (16, 212, "1  POLAND: MISSILES LAND", "War spills over the border; Kyiv hit too."),
        (524, 212, "COP31: TALKS RUN INTO OVERTIME", "Fossil fuels left out of the draft text."),
        (16, 300, "8  CYCLONE AKVAN HITS INDIA", "Storm crosses the Odisha coast in heavy rain."),
        (524, 300, "34  ASHES: STARC TAKES 7 FOR 58", "England 172 all out on day one at Perth."),
    ]
    draw_fns = [draw_panel_a, draw_panel_b, draw_panel_c, draw_panel_d]
    for (px, py, cap, sub), fn in zip(panels, draw_fns):
        fn(d, px, py, 484, 56)
        d.text((px, py + 58), cap, font=font(SANS_B, 12), fill=INK)
        d.text((px, py + 73), sub, font=font(SANS, 11), fill=GREY)

    # Stats strip
    d.rectangle([16, 392, W - 16, 444], fill=NAVY)
    sw = (W - 32) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = 16 + sw * i
        d.text((cx + sw / 2 - d.textlength(num, font=font(SERIF_B, 22)) / 2, 398),
               num, font=font(SERIF_B, 22), fill=(255, 210, 90))
        for j, line in enumerate(label.split("\n")):
            d.text((cx + sw / 2 - d.textlength(line, font=font(SANS, 10)) / 2,
                    422 + j * 12), line, font=font(SANS, 10), fill=(220, 225, 235))
        if i:
            d.line([cx, 400, cx, 438], fill=(70, 90, 130), width=1)

    # Region-count bar
    d.text((16, 452), "STORIES BY REGION:", font=font(SANS_B, 12), fill=INK)
    rx = 16 + d.textlength("STORIES BY REGION:  ", font=font(SANS_B, 12))
    total = sum(c for _, c in REGION_COUNTS)
    bar_w = W - 16 - rx - 90
    bx = rx
    colors = [(178, 24, 24), (16, 32, 64), (176, 132, 24), (40, 120, 80),
              (90, 60, 140), (200, 90, 40), (30, 120, 160)]
    for (name, cnt), col in zip(REGION_COUNTS, colors):
        seg = bar_w * cnt / total
        d.rectangle([bx, 454, bx + seg, 468], fill=col)
        bx += seg
    d.text((W - 86, 454), "36 stories", font=font(SANS_B, 12), fill=INK)
    lx = rx
    for (name, cnt), col in zip(REGION_COUNTS, colors):
        d.rectangle([lx, 474, lx + 10, 484], fill=col)
        d.text((lx + 13, 473), "%s %d" % (name, cnt), font=font(SANS, 10), fill=INK)
        lx += 13 + d.textlength("%s %d" % (name, cnt), font=font(SANS, 10)) + 12

    # World map panel
    d.text((16, 492), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    draw_map(d, 16, 508, W - 32, 66)
    d.text((16, 578), "Pins match the numbered stories below.",
           font=font(SANS, 10), fill=GREY)

    # Numbered stories, two columns, two lines each
    d.rectangle([16, 594, W - 16, 598], fill=NAVY)
    col_w = 484
    for col in range(2):
        cx = 16 + col * 508
        for i in range(18):
            s = STORIES[col * 18 + i]
            y = 606 + i * 21
            num_txt = "%d." % s[0]
            d.text((cx, y), num_txt, font=font(SANS_B, 10), fill=RED)
            nx = cx + d.textlength("36. ", font=font(SANS_B, 10)) + 2
            head = fit(d, s[2], font(SANS_B, 10), col_w - (nx - cx))
            d.text((nx, y), head, font=font(SANS_B, 10), fill=INK)
            summ = fit(d, s[3], font(SANS, 9), col_w - (nx - cx))
            d.text((nx, y + 11), summ, font=font(SANS, 9), fill=(60, 60, 60))
            d.text((W - 16 - d.textlength(s[4], font=font(SANS, 8)) if col == 1
                    else cx + col_w - d.textlength(s[4], font=font(SANS, 8)), y),
                   s[4], font=font(SANS, 8), fill=GREY)

    # Footer
    d.rectangle([16, 992, W - 16, 994], fill=NAVY)
    d.text((16, 998), "ALSO ON SATURDAY: India U17s reach the AFC Asian Cup  •  Hyundai unveils the 2027 Elantra in Los Angeles  •  WPL auction lists 277 players",
           font=font(SANS, 10), fill=GREY)
    return img


if __name__ == "__main__":
    img = render()
    img.save("frontpage.png", optimize=True)
    print("saved frontpage.png", img.size)
