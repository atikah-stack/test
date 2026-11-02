"""Measure how tilted the blue case is in a frame: fits lines to its four edges.
Usage: python3 tools/measure_tilt.py frame.png"""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
mask = (b - r > 18) & (b > 90)
ys, xs = np.nonzero(mask)
y0, y1 = np.percentile(ys, [3, 97]); x0, x1 = np.percentile(xs, [3, 97])

def fit(a, b_):
    k, c = np.polyfit(a, b_, 1)
    return np.degrees(np.arctan(k))

L, R, T, B = [], [], [], []
for y in range(int(y0 + 0.15 * (y1 - y0)), int(y1 - 0.15 * (y1 - y0)), 4):
    row = np.nonzero(mask[y])[0]
    if len(row) > 50: L.append((y, row[0])); R.append((y, row[-1]))
for x in range(int(x0 + 0.15 * (x1 - x0)), int(x1 - 0.15 * (x1 - x0)), 4):
    col = np.nonzero(mask[:, x])[0]
    if len(col) > 50: T.append((x, col[0])); B.append((x, col[-1]))
L, R, T, B = map(np.array, (L, R, T, B))
# vertical edges: x as a function of y; positive = bottom leans right (object turned counter-clockwise)
print("left  edge", round(fit(L[:, 0], L[:, 1]), 2))
print("right edge", round(fit(R[:, 0], R[:, 1]), 2))
# horizontal edges: y as a function of x; positive = right side lower (object turned clockwise)
print("top   edge", round(fit(T[:, 0], T[:, 1]), 2))
print("bottom edge", round(fit(B[:, 0], B[:, 1]), 2))
print("bbox", int(x0), int(y0), int(x1), int(y1), "centre", int((x0 + x1) / 2), int((y0 + y1) / 2))
