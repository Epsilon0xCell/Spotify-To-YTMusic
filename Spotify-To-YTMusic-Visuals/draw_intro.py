#!/usr/bin/env python3
"""Spotify-To-YTMusic intro banner: the Abbey Road crossing at dawn, scenery only.
No lettering, no signage text, no logos, no screen elements anywhere. Rain darkened
tarmac fills the foreground, the nearest white stripe runs out of the picture at
both ends, paint scuffed, a drain grate at the kerb, fallen plane leaves stuck to
the wet surface. The remaining stripes cross in perspective, empty of feet and
wheels, a traffic island midway with a belisha beacon unlit, bollards chipped.
Across the road: far kerb, low garden wall, iron railings, a Georgian house front
with a blue door, a studio entrance with swept steps and a milk bottle on them.
Plane tree crowns meet over the road, light landing in patches on the stripes.
The detail: a crossing guard lollipop leans against the island post, its blank
round face catching the first patch of sun while everything else stays in shade."""
import sys, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
random.seed(97)
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
CREAM = (238, 232, 210)
img = Image.new("RGB", (W, H), (96, 104, 96)); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):  # grey dawn sky through trees
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(168 - 40 * t), int(172 - 38 * t), int(162 - 32 * t)))
# plane tree crowns meeting over the road
for cx, cy, r in ((120, 90, 240), (430, 60, 260), (760, 84, 250), (1080, 56, 260), (1400, 88, 250), (1620, 70, 220)):
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(74, 96, 62))
    d.ellipse([cx - r // 2, cy - r // 3, cx + r // 2, cy + r // 2 + 30], fill=(86, 108, 70))
for tx in (200, 560, 920, 1280, 1520):  # trunks at the edges
    d.line([(tx, 130), (tx - 14, 330)], fill=(70, 60, 48), width=16)
# Georgian house front, far side
d.rectangle([880, 250, 1330, 470], fill=(168, 152, 132))
d.polygon([(868, 250), (1342, 250), (1300, 208), (910, 208)], fill=(84, 74, 66))
for wx in (930, 1020, 1150, 1240):
    for wy in (286, 368):
        d.rectangle([wx, wy, wx + 52, wy + 62], fill=(44, 46, 50), outline=(210, 204, 188), width=3)
d.rectangle([1088, 386, 1136, 452], fill=(38, 62, 110))  # the blue door
d.ellipse([1128, 428, 1136, 436], fill=(190, 170, 100))
# studio entrance to one side: steps swept clean, milk bottle on them
d.rectangle([420, 330, 640, 470], fill=(120, 108, 94))
d.rectangle([486, 356, 574, 470], fill=(40, 40, 42))
for si in range(3):
    d.rectangle([462 - si * 10, 442 - si * 4, 600 + si * 10, 452 - si * 4], fill=(150, 140, 124))
d.rectangle([548, 404, 564, 440], fill=(236, 236, 230)); d.rectangle([552, 392, 560, 406], fill=(200, 60, 48))  # milk bottle on the studio steps
# garden wall and iron railings
d.rectangle([120, 420, 1580, 452], fill=(104, 92, 78))
for rx in range(140, 1580, 36):
    d.line([(rx, 356), (rx, 420)], fill=(30, 30, 32), width=4)
    d.polygon([(rx - 5, 356), (rx + 5, 356), (rx, 342)], fill=(30, 30, 32))
d.line([(120, 356), (1580, 356)], fill=(30, 30, 32), width=5)
# tarmac in perspective, rain darkened
d.polygon([(0, 470), (1600, 470), (1600, 900), (0, 900)], fill=(34, 33, 34))
for _ in range(260):  # patched and repatched tarmac
    x, y = random.randint(0, 1590), random.randint(480, 890)
    g = random.randint(40, 62)
    d.ellipse([x, y, x + random.randint(14, 60), y + random.randint(4, 12)], fill=(g, g, g + 2))
# stripes crossing in perspective, worn thin in the middle
stripes = [(486, 500, 1114, 522, 1180, 560, 420, 560), (452, 592, 1148, 592, 1230, 646, 370, 646), (408, 686, 1192, 686, 1290, 762, 310, 762), (330, 800, 1270, 800, 1420, 900, 180, 900)]
for (x1, y1, x2, y2, x3, y3, x4, y4) in stripes:
    d.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=CREAM)
    for _ in range(16):  # scuffs and tyre wear
        x, y = random.randint(min(x1, x4), max(x2, x3)), random.randint(y1, y3)
        d.ellipse([x, y, x + random.randint(8, 30), y + 4], fill=(52, 50, 50))
# traffic island midway, belisha beacon unlit, chipped bollards
d.polygon([(700, 528), (900, 528), (924, 560), (676, 560)], fill=(90, 88, 84))
d.rectangle([792, 452, 808, 528], fill=(36, 36, 38))
d.ellipse([778, 414, 822, 458], fill=(203, 199, 186))  # beacon globe, dull and unlit in the early hour
d.ellipse([786, 422, 814, 450], outline=(130, 126, 114), width=3)
for bxx in (700, 884):
    d.rectangle([bxx, 500, bxx + 18, 532], fill=(52, 52, 54))
    d.rectangle([bxx, 500, bxx + 18, 508], fill=(214, 208, 196))
    d.polygon([(bxx + 2, 512), (bxx + 10, 508), (bxx + 8, 520)], fill=(24, 24, 26))  # chip knocked out
# first patch of sun landing on the stripes
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
ld.polygon([(240, 130), (560, 130), (760, 700), (420, 700)], fill=(255, 226, 160, 34))
ld.polygon([(900, 130), (1140, 130), (1240, 640), (1020, 640)], fill=(255, 226, 160, 28))
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(18))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# the lollipop leaning ready against the island post, blank face catching the sun
d.line([(812, 470), (872, 560)], fill=(226, 224, 216), width=9)
sun = (255, 214, 130) if v != "v1" else (214, 200, 168)
d.ellipse([838, 402, 918, 482], fill=sun, outline=(160, 140, 96), width=4)
d.ellipse([846, 410, 910, 474], outline=(206, 176, 110), width=2)
# kerb, drain grate, fallen plane leaves stuck to the wet surface
d.rectangle([0, 862, 1600, 900], fill=(96, 94, 90))
for gx in range(96, 268, 28):
    d.rectangle([gx, 868, gx + 12, 892], fill=(30, 30, 32))
for _ in range(30):
    x, y = random.randint(20, 1560), random.randint(700, 856)
    col = random.choice(((150, 118, 62), (128, 106, 58), (160, 132, 70)))
    d.polygon([(x, y), (x + 11, y - 6), (x + 20, y - 1), (x + 12, y + 7), (x + 2, y + 6)], fill=col)
    d.line([(x + 2, y + 6), (x - 4, y + 11)], fill=col, width=2)
rng = np.random.default_rng(17); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
img.save(out); print(out)
