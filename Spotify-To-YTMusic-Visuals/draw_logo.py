#!/usr/bin/env python3
"""Spotify-To-YTMusic logo: one white stripe of a zebra crossing viewed from directly
above, a long rectangle with chipped edges and a hairline crack, on near black
tarmac. A second, shorter stripe crosses its lower third at a right angle to
suggest the kerb. Ballroom teal tints the tarmac at the edges, walnut brown warms
the crack, cream is the stripe. Four small black shoe prints walk left to right
across the stripe. Below, Spotify-To-YTMusic in Annapurna SIL in cream, letterspaced
like kerbside stencilling. At 64 pixels only the cream stripe on black with one
shoe print remains, still readable as a crossing."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W = H = 1024
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
CREAM = (240, 234, 212); TARMAC = (22, 22, 24); TEAL = (26, 92, 94); WALNUT = (110, 76, 48)
img = Image.new("RGB", (W, H), TARMAC); d = ImageDraw.Draw(img, "RGBA")
for x in range(W):  # teal tint at the tarmac edges
    if x < 130: d.line([(x, 0), (x, H)], fill=(22 + (130 - x) // 9, 22 + (130 - x) // 4, 24 + (130 - x) // 4))
    if x > W - 130: d.line([(x, 0), (x, H)], fill=(22 + (x - (W - 130)) // 9, 22 + (x - (W - 130)) // 4, 24 + (x - (W - 130)) // 4))
# the long stripe, chipped edges
sx0, sy0, sx1, sy1 = 150, 300, 874, 470
d.polygon([(sx0 + 12, sy0), (sx1 - 20, sy0), (sx1, sy0 + 26), (sx1 - 8, sy1 - 18), (sx1 - 40, sy1), (sx0 + 24, sy1), (sx0, sy1 - 30), (sx0, sy0 + 22)], fill=CREAM)
for _ in range(14):  # scuffs
    import random; random.seed(4)
    x, y = random.randint(sx0 + 20, sx1 - 40), random.randint(sy0 + 12, sy1 - 12)
    d.ellipse([x, y, x + random.randint(8, 26), y + 4], fill=(120, 116, 104))
# hairline crack warmed in walnut
d.line([(sx0 + 70, sy0 + 96), (sx0 + 128, sy0 + 84), (sx0 + 168, sy0 + 104), (sx0 + 236, sy0 + 92)], fill=WALNUT, width=2)
# the shorter kerb stripe crossing the lower third
d.polygon([(560, 408), (636, 408), (644, 640), (552, 640)], fill=(228, 222, 198))
d.polygon([(560, 408), (636, 408), (640, 470), (556, 470)], fill=(208, 202, 178))
# four shoe prints walking left to right across the stripe: horizontal soles, heel behind
def shoe(cx, cy, up):
    dy = -12 if up else 12
    d.polygon([(cx - 24, cy + dy - 9), (cx + 14, cy + dy - 11), (cx + 27, cy + dy - 2), (cx + 22, cy + dy + 8), (cx - 14, cy + dy + 10), (cx - 25, cy + dy + 2)], fill=(16, 16, 18))
    d.ellipse([cx - 37, cy + dy - 7, cx - 20, cy + dy + 7], fill=(16, 16, 18))  # heel print, touching the sole
for i, (px, py) in enumerate(((272, 380), (424, 388), (576, 380), (724, 388))):
    shoe(px, py, i % 2 == 0)
if v != "v1":
    f = ImageFont.truetype("fonts/AnnapurnaSIL.ttf", 54)
    txt = "Spotify-To-YTMusic"
    # letterspaced, stencilled at a kerbside
    total = sum(d.textlength(ch, font=f) + 7 for ch in txt) - 7
    x = (W - total) / 2
    for ch in txt:
        d.text((x, 760), ch, font=f, fill=CREAM); x += d.textlength(ch, font=f) + 7
rng = np.random.default_rng(19); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out); print(out)
img.resize((64, 64), Image.LANCZOS).save(f"scratch/logo64-{v}.png"); print("64px saved")
