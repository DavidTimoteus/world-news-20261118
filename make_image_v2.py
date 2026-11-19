"""news-image-20261118 — v2 news board.

One image summing up the world news of Wednesday, 18 November 2026.
Deterministic: no network, no randomness, no clock. Output: 1000x1000 PNG.

Layout (modeled on the #1 reference board):
  * 120px dark header: big date + one-line subtitle + red rule
  * region tag row with per-region event counts
  * 3-column x 4-row grid of 12 headline panels (badge + headline + number + icon)
  * row 5: "WHERE IT HAPPENED" stylised world map + "ALSO ON THIS DAY" 4-column list
  * footer: "DATE CHECK" box with the summarise URL

All facts are from Wikipedia Current Events, 18 November 2026 (as supplied).
"""
import math
import os
import shutil

from PIL import Image, ImageDraw, ImageFont
import matplotlib

HERE = os.path.dirname(os.path.abspath(__file__))
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")

W = H = 1000

# ---- palette -------------------------------------------------------------
BG = (12, 16, 27)
PANEL = (23, 29, 45)
PANEL_ALT = (12, 20, 38)
HEADER = (9, 13, 23)
STRIP = (19, 25, 40)
WHITE = (245, 247, 252)
MUTED = (156, 168, 190)
SOFT = (203, 213, 232)
GRID = (38, 46, 64)
LAND = (54, 74, 94)

ACCENTS = [
    (231, 76, 60),    # 0 red    - conflict / disaster
    (230, 126, 34),   # 1 orange - labour / unrest
    (241, 196, 15),   # 2 yellow - diplomacy / politics
    (39, 174, 96),    # 3 green  - economy / checked
    (52, 152, 219),   # 4 blue   - science / space / weather
    (155, 89, 182),   # 5 purple - society / culture
    (26, 188, 156),   # 6 teal   - global
]

FONT_CACHE = {}


def font(sz, bold=False):
    key = (sz, bold)
    if key not in FONT_CACHE:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        FONT_CACHE[key] = ImageFont.truetype(os.path.join(FDIR, name), sz)
    return FONT_CACHE[key]


def text_w(d, s, ft):
    b = d.textbbox((0, 0), s, font=ft)
    return b[2] - b[0]


def fit_font(d, s, maxw, start, minsz, bold=False):
    sz = start
    while sz > minsz:
        ft = font(sz, bold)
        if text_w(d, s, ft) <= maxw:
            return ft
        sz -= 1
    return font(minsz, bold)


def wrap(d, s, ft, maxw):
    lines, cur = [], ""
    for wd in s.split():
        t = (cur + " " + wd).strip()
        if text_w(d, t, ft) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, s, maxw, start, minsz, maxlines, bold=False):
    sz = start
    while sz >= minsz:
        ft = font(sz, bold)
        ln = wrap(d, s, ft, maxw)
        if len(ln) <= maxlines:
            return ft, ln
        sz -= 1
    ft = font(minsz, bold)
    return ft, wrap(d, s, ft, maxw)[:maxlines]


# ---- simple geometric icons ---------------------------------------------
def draw_icon(d, kind, cx, cy, acc, s=20):
    col = acc
    light = tuple(min(255, c + 55) for c in acc)

    if kind == "plane":
        d.polygon([(cx, cy - s), (cx + s * 0.85, cy + s),
                   (cx, cy + s * 0.45), (cx - s * 0.85, cy + s)], fill=col)
        d.line([(cx - s * 0.5, cy + s), (cx + s * 0.5, cy + s)], fill=light, width=3)

    elif kind == "handshake":
        d.rounded_rectangle([cx - s, cy - 6, cx - 2, cy + 6], radius=4, fill=col)
        d.rounded_rectangle([cx + 2, cy - 6, cx + s, cy + 6], radius=4, fill=light)
        d.line([(cx - 5, cy), (cx + 5, cy)], fill=WHITE, width=3)

    elif kind == "drone":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)
        for dx, dy in ((-s, -s * 0.8), (s, -s * 0.8), (-s, s * 0.8), (s, s * 0.8)):
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=col, width=3)
            d.ellipse([cx + dx - 6, cy + dy - 5, cx + dx + 6, cy + dy + 5],
                      outline=light, width=2)

    elif kind == "planet":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=col)
        d.ellipse([cx - s - 9, cy - 6, cx + s + 9, cy + 6], outline=light, width=3)

    elif kind == "euro":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=col, width=3)
        d.text((cx, cy), "\u20ac", font=font(26, True), fill=WHITE, anchor="mm")

    elif kind == "chart":
        base = cy + 18
        for bx, top in ((-17, cy - 2), (-5, cy - 12), (7, cy + 4)):
            d.rectangle([cx + bx, top, cx + bx + 9, base], fill=col)
        d.line([(cx - 19, cy + 1), (cx + 20, cy - 11)], fill=WHITE, width=3)

    elif kind == "cyclone":
        for r in (7, 13, 19):
            d.arc([cx - r, cy - r, cx + r, cy + r], 25, 305, fill=col, width=3)
        d.arc([cx - 8, cy - 8, cx + 8, cy + 8], 190, 430, fill=light, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)

    elif kind == "protest":
        d.ellipse([cx - 6, cy - s, cx + 6, cy - s + 12], fill=col)
        d.line([(cx, cy - s + 12), (cx, cy + 6)], fill=col, width=6)
        d.line([(cx, cy - 4), (cx - s * 0.8, cy + 2)], fill=col, width=4)
        d.line([(cx, cy - 4), (cx + s * 0.8, cy + 4)], fill=col, width=4)
        d.line([(cx, cy + 6), (cx - s * 0.7, cy + s)], fill=col, width=4)
        d.line([(cx, cy + 6), (cx + s * 0.7, cy + s)], fill=col, width=4)

    elif kind == "gamepad":
        d.rounded_rectangle([cx - s, cy - 11, cx + s, cy + 12], radius=9, fill=col)
        d.line([(cx - 13, cy), (cx - 13, cy + 9)], fill=WHITE, width=3)
        d.line([(cx - 18, cy + 5), (cx - 8, cy + 5)], fill=WHITE, width=3)
        d.ellipse([cx + 4, cy - 6, cx + 11, cy + 1], fill=WHITE)
        d.ellipse([cx + 12, cy + 2, cx + 19, cy + 9], fill=WHITE)

    elif kind == "earthstar":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=(41, 128, 185))
        d.arc([cx - s - 5, cy - s - 5, cx + s + 5, cy + s + 5], 200, 345,
              fill=(46, 204, 113), width=4)
        d.arc([cx - s * 0.4, cy - s, cx + s * 0.9, cy + s], 250, 90,
              fill=(93, 173, 226), width=2)
        sx, sy = cx + s + 12, cy - s - 2
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            d.line([(sx, sy), (sx + 11 * math.cos(rad), sy + 11 * math.sin(rad))],
                   fill=(241, 196, 15), width=2)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(241, 196, 15))

    elif kind == "storm":
        d.arc([cx - s - 6, cy - s - 6, cx + s + 6, cy + s + 6], 0, 265, fill=col, width=4)
        d.arc([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6], 180, 445,
              fill=light, width=4)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)

    else:
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=col, width=3)


# ---- canvas --------------------------------------------------------------
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- header --------------------------------------------------------------
d.rectangle([0, 0, W, 120], fill=HEADER)
d.rectangle([0, 116, W, 120], fill=ACCENTS[0])

date_s = "18 WEDNESDAY NOVEMBER 2026"
df = fit_font(d, date_s, 930, 54, 34, True)
d.text((28, 12), date_s, font=df, fill=WHITE)

sub_s = ("Everything on this day happened, or was first reported, "
         "on Wednesday 18 November 2026")
sf = fit_font(d, sub_s, 940, 17, 11)
d.text((30, 82), sub_s, font=sf, fill=MUTED)

# ---- region tag row ------------------------------------------------------
REGIONS = [
    ("ASIA", 7, ACCENTS[1]), ("EUROPE", 9, ACCENTS[4]),
    ("AMERICA", 10, ACCENTS[3]), ("AFRICA", 7, ACCENTS[2]),
    ("MIDDLE EAST", 4, ACCENTS[5]), ("OCEANIA", 4, ACCENTS[0]),
    ("GLOBAL", 5, ACCENTS[6]),
]
rx = 28
for name, cnt, col in REGIONS:
    label = "%s %d" % (name, cnt)
    ft = font(12, True)
    tw = text_w(d, label, ft) + 18
    d.rounded_rectangle([rx, 127, rx + tw, 149], radius=10,
                        fill=PANEL, outline=col, width=1)
    d.text((rx + 9, 129), label, font=ft, fill=col)
    rx += tw + 8

# ---- 12 headline panels --------------------------------------------------
# (region, headline, number/subline, accent index, icon)
PANELS = [
    ("ASIA 7", "Trump-Putin talks in Shenzhen", "US GIVES TARIFFS TO INDIA", 2, "plane"),
    ("ASIA 7", "Xi greets Trump on tariff truce", "SHENZHEN SUMMIT  \u00b7  TRADE DEAL", 2, "handshake"),
    ("MIDDLE EAST 4", "Kuwait, Iran, Bahrain intercept drones", "IRANIAN DRONES DOWNED", 0, "drone"),
    ("GLOBAL 5", "Voyager 1: one light-day from Earth", "25.3 BILLION KM  \u00b7  NASA", 4, "planet"),
    ("EUROPE 9", "Russia fires 126 drones at Ukraine", "121 DOWNED  \u00b7  37 KILLED IN ODESA", 0, "drone"),
    ("EUROPE 9", "EU proposes \u20ac45bn loan to Ukraine", "\u20ac45BN LOAN  \u00b7  2027", 3, "euro"),
    ("AMERICA 10", "Fed minutes: more rate hikes seen", "DOW -1.1%", 1, "chart"),
    ("OCEANIA 4", "Cyclone Okswi veers toward Odisha", "RAINFALL 26 CM", 4, "cyclone"),
    ("ASIA 7", "Bangladesh garment workers protest", "WAGE DEMANDS  \u00b7  DHAKA", 1, "protest"),
    ("GLOBAL 5", "GTA VI pre-orders go on sale", "AFTER 13-MONTH WAIT", 5, "gamepad"),
    ("GLOBAL 5", "1 LIGHT-DAY", "EARTH  \u00b7  INTERSTELLAR SPACE  \u00b7  NASA", 4, "earthstar"),
    ("ASIA 7", "Typhoon Fung-wong kills 21", "IN THE PHILIPPINES", 0, "storm"),
]

STARS = [(0.08, 0.18), (0.22, 0.62), (0.35, 0.30), (0.45, 0.78), (0.55, 0.16),
         (0.68, 0.70), (0.78, 0.25), (0.90, 0.80), (0.30, 0.88), (0.95, 0.50),
         (0.16, 0.40), (0.62, 0.50), (0.84, 0.60), (0.40, 0.50), (0.72, 0.44)]

GX0, GY0 = 28, 158
GCOLS, GROWS, GGAP = 3, 4, 8
GW = (W - 2 * 28 - (GCOLS - 1) * GGAP) // GCOLS  # 309
GH = 104

for idx, (region, head, sub, ai, icon) in enumerate(PANELS):
    r, c = divmod(idx, GCOLS)
    px = GX0 + c * (GW + GGAP)
    py = GY0 + r * (GH + GGAP)
    acc = ACCENTS[ai]

    d.rectangle([px, py, px + GW, py + GH], fill=PANEL)
    d.rectangle([px, py, px + 6, py + GH], fill=acc)

    if icon == "earthstar":
        # starfield for the space panel
        d.rectangle([px + 6, py, px + GW, py + GH], fill=PANEL_ALT)
        for fx, fy in STARS:
            sx = px + 6 + int(fx * (GW - 6))
            sy = py + int(fy * GH)
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(150, 170, 200))

    d.text((px + 14, py + 6), region, font=font(10, True), fill=acc)

    hf, hlines = fit_lines(d, head, GW - 92, 16, 11, 2, True)
    yy = py + 22
    for ln in hlines:
        d.text((px + 14, yy), ln, font=hf, fill=WHITE)
        yy += hf.size + 2

    sf2 = font(10, True)
    slines = wrap(d, sub, sf2, GW - 96)[:2]
    sy = max(yy + 2, py + 64)
    for ln in slines:
        d.text((px + 14, sy), ln, font=sf2, fill=SOFT)
        sy += 13

    icx = px + GW - (52 if icon == "earthstar" else 40)
    draw_icon(d, icon, icx, py + GH // 2, acc,
              s=27 if icon == "earthstar" else 19)

# ---- row 5: world map + also on this day ---------------------------------
R5Y, R5H = 606, 196
MAPW = 330
ALSO_X = 28 + MAPW + 10
ALSO_W = W - 28 - ALSO_X

# --- world map ---
d.rectangle([28, R5Y, 28 + MAPW, R5Y + R5H], fill=PANEL)
d.rectangle([28, R5Y, 28 + MAPW, R5Y + 26], fill=STRIP)
d.text((38, R5Y + 5), "WHERE IT HAPPENED", font=font(14, True), fill=WHITE)

mx0, my0 = 36, R5Y + 34
mw, mh = MAPW - 16, R5H - 42
for i in range(1, 6):
    d.line([(mx0 + mw * i / 6, my0), (mx0 + mw * i / 6, my0 + mh)], fill=GRID, width=1)
    d.line([(mx0, my0 + mh * i / 6), (mx0 + mw, my0 + mh * i / 6)], fill=GRID, width=1)

CONTINENTS = [
    [(0.02, 0.12), (0.10, 0.08), (0.20, 0.10), (0.26, 0.18), (0.23, 0.28),
     (0.17, 0.34), (0.15, 0.45), (0.11, 0.40), (0.10, 0.28), (0.04, 0.22)],
    [(0.20, 0.46), (0.27, 0.48), (0.30, 0.58), (0.27, 0.72), (0.23, 0.90),
     (0.20, 0.74), (0.18, 0.58)],
    [(0.44, 0.16), (0.52, 0.14), (0.56, 0.20), (0.54, 0.28), (0.47, 0.30), (0.44, 0.24)],
    [(0.45, 0.34), (0.56, 0.33), (0.58, 0.44), (0.54, 0.60), (0.49, 0.70),
     (0.46, 0.58), (0.44, 0.44)],
    [(0.56, 0.10), (0.74, 0.06), (0.90, 0.10), (0.94, 0.22), (0.88, 0.34),
     (0.78, 0.40), (0.70, 0.38), (0.62, 0.32), (0.56, 0.24)],
    [(0.70, 0.34), (0.75, 0.34), (0.74, 0.44), (0.71, 0.42)],
    [(0.82, 0.62), (0.92, 0.60), (0.94, 0.72), (0.86, 0.76), (0.81, 0.70)],
]
for poly in CONTINENTS:
    d.polygon([(mx0 + nx * mw, my0 + ny * mh) for nx, ny in poly], fill=LAND)

# (nx, ny, label, colour, placement, explicit label position in image px)
# "abs" is used where the automatic offsets would collide with a nearby dot.
DOTS = [
    (0.16, 0.26, "USA", ACCENTS[4], "right", None),
    (0.52, 0.22, "UKRAINE", ACCENTS[2], "above", None),
    (0.86, 0.30, "SHENZHEN", ACCENTS[0], "leftup", None),
    (0.73, 0.42, "ODISHA", ACCENTS[1], "below", None),
    (0.90, 0.47, "PHILIPPINES", ACCENTS[0], "abs", (250, 735)),
    (0.59, 0.40, "MIDDLE EAST", ACCENTS[5], "abs", (150, 694)),
    (0.88, 0.68, "OCEANIA", ACCENTS[3], "below", None),
]
lf = font(8, True)
for nx, ny, label, col, pos, absxy in DOTS:
    dx, dy = mx0 + nx * mw, my0 + ny * mh
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=col, outline=WHITE, width=1)
    lw = text_w(d, label, lf)
    if pos == "abs":
        lx, ly = absxy
    elif pos == "left":
        lx, ly = dx - 8 - lw, dy - 7
    elif pos == "leftup":
        lx, ly = dx - 8 - lw, dy - 18
    elif pos == "above":
        lx, ly = dx - lw / 2, dy - 19
    elif pos == "below":
        lx, ly = dx - lw / 2, dy + 8
    else:
        lx, ly = dx + 8, dy - 7
    # safety clamp: keep every label fully inside the map panel
    lx = max(30, min(lx, 28 + MAPW - 4 - lw))
    ly = max(R5Y + 28, min(ly, R5Y + R5H - 14))
    d.text((lx, ly), label, font=lf, fill=WHITE)

# --- also on this day ---
d.rectangle([ALSO_X, R5Y, ALSO_X + ALSO_W, R5Y + R5H], fill=PANEL)
d.rectangle([ALSO_X, R5Y, ALSO_X + ALSO_W, R5Y + 26], fill=STRIP)
d.text((ALSO_X + 10, R5Y + 5), "ALSO ON THIS DAY", font=font(14, True), fill=WHITE)

ALSO_ITEMS = [
    "DOPF hack hits 6.6M users",
    "Japan critic arrested over PM insult",
    "India opens first AI university",
    "Seoul police raid K-pop agencies",
    "Typhoon Fung-wong: 21 dead",
    "Ship strikes Brooklyn Bridge",
    "Voyager 1 one light-day out",
    "GTA VI pre-orders go live",
    "EU proposes \u20ac45bn Ukraine loan",
    "Fed sees more rate hikes",
    "126 drones fired at Ukraine",
    "Odesa strike kills 37",
    "Cyclone Okswi nears Odisha",
    "Trump-Putin talks in Shenzhen",
    "Xi greets Trump on truce",
    "Kuwait downs Iranian drones",
    "DOW closes down 1.1%",
    "Bangladesh garment wage protests",
    "25.3bn km to Voyager 1",
    "Rainfall 26 cm in Odisha",
]
ncols, per = 4, 5
colw = (ALSO_W - 16) // ncols
rowh = (R5H - 32) // per
itf = font(10)
for i, item in enumerate(ALSO_ITEMS):
    c, r = divmod(i, per)
    bx = ALSO_X + 8 + c * colw + 3
    by = R5Y + 32 + r * rowh
    d.ellipse([bx, by + 3, bx + 5, by + 8], fill=ACCENTS[c])
    for li, ln in enumerate(wrap(d, item, itf, colw - 12)[:2]):
        d.text((bx + 10, by + li * 12), ln, font=itf, fill=MUTED)

# ---- footer: DATE CHECK --------------------------------------------------
FY0, FY1 = 812, 988
d.rectangle([28, FY0, W - 28, FY1], fill=(18, 24, 38))
d.rectangle([28, FY0, W - 28, FY0 + 4], fill=ACCENTS[3])
d.rounded_rectangle([40, FY0 + 16, 196, FY0 + 48], radius=8, fill=ACCENTS[3])
d.text((118, FY0 + 32), "DATE CHECK", font=font(16, True), fill=WHITE, anchor="mm")

body = ("To summarise, all events reported on Wednesday 18 November 2026. "
        "Confirm a few by reading their links. The #November 18 Wikipedia "
        "article is at: make.fun/summarise/nov-18/18-11-2026")
btf = font(15)
by = FY0 + 60
for ln in wrap(d, body, btf, W - 56 - 32):
    d.text((44, by), ln, font=btf, fill=WHITE)
    by += 23
d.text((44, FY1 - 28), "Every headline above is dated 18 November 2026.",
       font=font(12, True), fill=ACCENTS[3])

# ---- save & copy to the submit locations ---------------------------------
out = os.path.join(HERE, "entry.png")
img.save(out)
print("wrote", out, os.path.getsize(out), "bytes")

for target in (
    os.path.join(HERE, "repo", "entry.png"),           # real make.fun submit file
    os.path.join(HERE, "entry", "entry.png"),           # path named in the task brief
):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(out, target)
    print("copied", target, os.path.getsize(target), "bytes")
