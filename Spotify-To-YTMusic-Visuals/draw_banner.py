#!/usr/bin/env python3
"""Spotify-To-YTMusic wordmark banner: a London street in flat morning light, framed
wide and low from the opposite kerb. The crossing takes the lower half: four broad
white stripes worn thin in the middle. The crossing guard stands on the second
stripe with a stop lollipop raised, hi vis vest over a dark coat. Left, a queue of
pedestrians waits at the kerb with shopping bags and a pram. Right, held back, a
black cab and a red bus idle. Behind: a high brick wall, plane trees, and the gate
of a recording studio, musicians with instrument cases going in. The lollipop
carries Spotify-To-YTMusic painted round its rim in cream capitals in Annapurna SIL.
Teal appears only in shop awnings further up the road; walnut in the wall brick."""
import sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W, H = 2560, 640
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
CREAM = (240, 234, 212)
img = Image.new("RGB", (W, H), (172, 176, 168)); d = ImageDraw.Draw(img, "RGBA")
# plane trees and sky
for cx, cy, r in ((200, 40, 260), (700, 20, 280), (1250, 36, 270), (1800, 16, 280), (2300, 44, 260)):
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(84, 104, 70))
# brick wall in walnut, studio gate set back
d.rectangle([980, 130, 2560, 330], fill=(128, 88, 64))
for ry in range(142, 330, 24):
    for bx in range(990 + (ry % 48), 2560, 96):
        d.rectangle([bx, ry, bx + 88, ry + 18], outline=(104, 70, 50), width=2)
d.rectangle([1440, 168, 1610, 330], fill=(52, 50, 50))  # studio gate opening
d.line([(1448, 168), (1448, 330)], fill=(26, 26, 28), width=6); d.line([(1602, 168), (1602, 330)], fill=(26, 26, 28), width=6)
for mx, col in ((1484, (60, 60, 64)), (1546, (76, 66, 58))):  # musicians with cases going in
    d.ellipse([mx - 11, 218, mx + 11, 240], fill=(216, 186, 152))
    d.rectangle([mx - 13, 240, mx + 13, 292], fill=col)
    d.rectangle([mx - 12, 292, mx - 2, 330], fill=(34, 32, 32)); d.rectangle([mx + 3, 292, mx + 13, 330], fill=(34, 32, 32))
    d.polygon([(mx + 14, 252), (mx + 44, 262), (mx + 40, 306), (mx + 12, 296)], fill=(40, 34, 28))  # instrument case
# shop awnings further up the road, the only teal
for ax in (120, 330, 540):
    d.polygon([(ax, 150), (ax + 170, 150), (ax + 150, 196), (ax + 20, 196)], fill=(26, 92, 94))
    d.rectangle([ax + 16, 196, ax + 154, 300], fill=(196, 188, 170))
    d.rectangle([ax + 60, 226, ax + 110, 300], fill=(70, 66, 60))
# tarmac and the crossing, lower half
d.rectangle([0, 330, 2560, 640], fill=(36, 35, 36))
stripes = [(180, 380, 1500, 380, 1560, 424, 120, 424), (140, 452, 1540, 452, 1620, 508, 60, 508), (90, 536, 1580, 536, 1690, 606, 0, 606)]
for (x1, y1, x2, y2, x3, y3, x4, y4) in stripes:
    d.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=CREAM)
    for wx in range(x1 + 200, x2 - 100, 260):  # worn thin in the middle
        d.ellipse([wx, y1 + 14, wx + 90, y1 + 26], fill=(120, 116, 108))
d.line([(0, 330), (2560, 330)], fill=(150, 148, 142), width=8)  # kerb line
# queue at the left kerb: figures with shopping bags and a pram
for qx, col in ((210, (88, 70, 84)), (300, (64, 78, 92)), (392, (96, 84, 62))):
    d.ellipse([qx - 13, 236, qx + 13, 262], fill=(216, 186, 152))
    d.rectangle([qx - 16, 262, qx + 16, 330], fill=col)
    d.rectangle([qx + 18, 296, qx + 44, 330], fill=(206, 196, 168))  # shopping bag
d.polygon([(452, 300), (540, 300), (532, 330), (460, 330)], fill=(52, 54, 60))  # pram body
d.ellipse([466, 326, 486, 346], fill=(24, 24, 26)); d.ellipse([508, 326, 528, 346], fill=(24, 24, 26))
d.line([(452, 300), (430, 282)], fill=(24, 24, 26), width=4)
# held traffic right: black cab and red bus
d.polygon([(1700, 268), (1730, 226), (1900, 226), (1936, 268), (1936, 330), (1700, 330)], fill=(20, 20, 22))
d.rectangle([1746, 236, 1820, 264], fill=(150, 168, 178)); d.rectangle([1832, 236, 1892, 264], fill=(150, 168, 178))
d.ellipse([1750, 316, 1786, 344], fill=(10, 10, 12)); d.ellipse([1850, 316, 1886, 344], fill=(10, 10, 12))
d.rectangle([1760, 282, 1782, 296], fill=(255, 214, 120))  # headlamp, idling
d.rectangle([2020, 190, 2400, 330], fill=(168, 40, 36))  # red bus
d.rectangle([2040, 208, 2380, 252], fill=(170, 186, 196))
for wx in range(2056, 2360, 62):
    d.rectangle([wx, 262, wx + 48, 300], fill=(150, 168, 178))
d.ellipse([2080, 316, 2120, 348], fill=(12, 12, 14)); d.ellipse([2300, 316, 2340, 348], fill=(12, 12, 14))
# traffic island and beacon between guard and traffic
d.rectangle([1330, 300, 1420, 330], fill=(92, 90, 86))
d.rectangle([1368, 226, 1382, 300], fill=(30, 30, 32))
d.ellipse([1352, 196, 1398, 242], fill=(232, 178, 84), outline=(120, 96, 40), width=3)
# the guard on the second stripe, lollipop raised
gx, gy = 800, 336
d.rectangle([gx - 20, gy + 84, gx - 4, gy + 196], fill=(30, 30, 34)); d.rectangle([gx + 5, gy + 84, gx + 21, gy + 196], fill=(30, 30, 34))
d.rectangle([gx - 32, gy, gx + 32, gy + 92], fill=(44, 44, 48))  # dark coat
d.polygon([(gx - 32, gy + 8), (gx + 32, gy + 8), (gx + 24, gy + 86), (gx - 24, gy + 86)], fill=(206, 196, 60))  # hi vis vest
d.line([(gx - 24, gy + 46), (gx + 24, gy + 46)], fill=(196, 200, 204), width=6)  # reflective band
d.ellipse([gx - 18, gy - 40, gx + 18, gy - 4], fill=(216, 186, 152))
d.polygon([(gx - 19, gy - 42), (gx + 19, gy - 42), (gx + 19, gy - 33), (gx - 19, gy - 33)], fill=(36, 36, 40))  # cap brim
d.line([(gx + 26, gy + 22), (gx + 92, gy - 52)], fill=(40, 40, 44), width=9)  # raised arm
d.line([(gx + 92, gy - 52), (gx + 118, gy - 128)], fill=(232, 230, 222), width=8)  # lollipop stick
lx, ly, lr = gx + 148, gy - 152, 88
d.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=(244, 240, 226), outline=(178, 52, 34), width=9)
if v != "v1":
    f = ImageFont.truetype("fonts/AnnapurnaSIL.ttf", 23)
    top = "SPOTIFY-TO-"
    for i, ch in enumerate(top):
        a = math.radians(196 + i * 15.5)
        px, py = lx + (lr - 20) * math.cos(a), ly + (lr - 20) * math.sin(a)
        d.text((px - 7, py - 10), ch, font=f, fill=(30, 30, 32))
    bot = "YTMUSIC"
    for i, ch in enumerate(bot):
        a = math.radians(150 - i * 20)
        px, py = lx + (lr - 20) * math.cos(a), ly + (lr - 20) * math.sin(a)
        d.text((px - 7, py - 10), ch, font=f, fill=(30, 30, 32))
d.ellipse([lx - 23, ly - 23, lx + 23, ly + 23], fill=(178, 52, 34))  # stop face centre
rng = np.random.default_rng(23); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)
