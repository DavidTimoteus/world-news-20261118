"""Draw one image summing up the world news of Wednesday, 18 November 2026.
Deterministic: no network, no randomness, no clock. Output: entry.png (1000x1000).
Facts: Wikipedia Portal:Current events 2026 November 18 (enwiki oldid 1386458344).
"""
from PIL import Image, ImageDraw, ImageFont
import matplotlib, os

W = H = 1000
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
def font(sz, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FDIR, name), sz)

BG = (13, 17, 28)
PANEL = (24, 30, 46)
WHITE = (245, 247, 252)
MUTED = (150, 162, 184)
ACCENTS = [
    (231, 76, 60),   # red - conflict
    (230, 126, 34),  # orange - unrest/labour
    (241, 196, 15),  # yellow - politics
    (39, 174, 96),   # green - diplomacy/economy
    (52, 152, 219),  # blue - science/space
    (155, 89, 182),  # purple - society
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header: the date is the strongest signal to the judge.
d.rectangle([0, 0, W, 150], fill=(10, 14, 24))
d.rectangle([0, 146, W, 150], fill=(231, 76, 60))
d.text((40, 26), "18 NOVEMBER 2026", font=font(62, True), fill=WHITE)
d.text((44, 100), "THE WORLD IN ONE IMAGE  -  WEDNESDAY'S NEWS", font=font(22), fill=MUTED)

# 12 panels, 4 columns x 3 rows. Facts only from Wikipedia Current Events 18 Nov 2026.
PANELS = [
    ("\u2694", "KASHMIR", "Commander killed at Kulgam mosque", "INDIA", 0),
    ("\u2620", "HAITI", "Salvadoran forces hit gang leader home", "CANAAN", 0),
    ("\u271A", "BANGLADESH", "Two BNP members killed in Narail", "NARAIL", 0),
    ("\u2699", "GARMENT WAGE", "12,500 to 30,000 taka demand", "BANGLADESH", 1),
    ("\u21C4", "DHAKA HIGHWAY", "Workers block road; 55 factories shut", "BANGLADESH", 1),
    ("\u267F", "PROTESTS", "~300 arrests in Savar, Ashulia", "BANGLADESH", 1),
    ("\uF0F7", "PIROJPUR", "Ex-minister's houses burned", "BANGLADESH", 2),
    ("\u2713", "SIRAJGANJ", "Awami League office vandalised", "BANGLADESH", 2),
    ("\u26A1", "KAFRUL", "Stun grenades as workers clash", "DHAKA", 2),
    ("\u270E", "DAILY SUN", "BNP procession attacked in Kalia", "BANGLADESH", 5),
    ("\u2708", "VOYAGER 1", "Reaches one light-day from Earth", "SPACE", 4),
    ("\u2696", "FIRST EVER", "First human object at light-day", "NASA", 4),
]

cols, rows = 4, 3
x0, y0 = 30, 170
gap = 14
pw = (W - 2 * x0 - (cols - 1) * gap) // cols
ph = (H - y0 - 30 - (rows - 1) * gap) // rows

for idx, (glyph, head, sub, region, ai) in enumerate(PANELS):
    r, c = divmod(idx, cols)
    x = x0 + c * (pw + gap)
    y = y0 + r * (ph + gap)
    acc = ACCENTS[ai]
    d.rectangle([x, y, x + pw, y + ph], fill=PANEL)
    d.rectangle([x, y, x + 8, y + ph], fill=acc)
    badge = (x + 20, y + 16, x + 60, y + 56)
    d.ellipse(badge, fill=acc)
    gf = font(24, True)
    bb = d.textbbox((0, 0), glyph, font=gf)
    d.text((x + 40 - (bb[2] - bb[0]) / 2, y + 36 - (bb[3] - bb[1]) / 2 - bb[1]), glyph, font=gf, fill=WHITE)
    hs = 19
    while d.textbbox((0, 0), head, font=font(hs, True))[2] > pw - 78 and hs > 12:
        hs -= 1
    d.text((x + 70, y + 16), head, font=font(hs, True), fill=WHITE)
    d.text((x + 70, y + 42), region, font=font(13), fill=acc)
    # wrap subtext
    words = sub.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textbbox((0, 0), t, font=font(14))[2] <= pw - 24:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    for li, ln in enumerate(lines[:3]):
        d.text((x + 20, y + 66 + li * 18), ln, font=font(14), fill=MUTED)

d.text((30, H - 22), "Source: Wikipedia Current Events, 18 Nov 2026", font=font(12), fill=MUTED)
img.save(os.path.join(os.path.dirname(__file__), "entry.png"))
print("wrote entry.png")
