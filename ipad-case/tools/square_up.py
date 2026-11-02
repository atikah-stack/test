"""Square up the blue case in a clip: finds its four edges in one frame, then warps the
whole clip so the case is an upright, centred rectangle (fixes tilt and camera keystone).
Usage: python3 tools/square_up.py in.mp4 out.mp4 [frame_time]"""
import subprocess, sys, tempfile, os
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
t = sys.argv[3] if len(sys.argv) > 3 else "1.5"
W, H = 1080, 1920
tmp = os.path.join(tempfile.mkdtemp(), "f.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", src, "-frames:v", "1", tmp], check=True)
im = np.asarray(Image.open(tmp).convert("RGB")).astype(int)
mask = (im[..., 2] - im[..., 0] > 18) & (im[..., 2] > 90)
ys, xs = np.nonzero(mask)
y0, y1 = np.percentile(ys, [3, 97]); x0, x1 = np.percentile(xs, [3, 97])
L, R, T, B = [], [], [], []
for y in range(int(y0 + 0.15 * (y1 - y0)), int(y1 - 0.15 * (y1 - y0)), 3):
    row = np.nonzero(mask[y])[0]
    if len(row) > 50: L.append((y, row[0])); R.append((y, row[-1]))
for x in range(int(x0 + 0.15 * (x1 - x0)), int(x1 - 0.15 * (x1 - x0)), 3):
    col = np.nonzero(mask[:, x])[0]
    if len(col) > 50: T.append((x, col[0])); B.append((x, col[-1]))
fl = lambda P: np.polyfit(np.array(P)[:, 0], np.array(P)[:, 1], 1)
(la, lb), (ra, rb), (ta, tb), (ba, bb) = fl(L), fl(R), fl(T), fl(B)

def meet(va, vb, ha, hb):  # x = va*y + vb  and  y = ha*x + hb
    y = (ha * vb + hb) / (1 - ha * va); return np.array([va * y + vb, y])

tl, tr, bl, br = meet(la, lb, ta, tb), meet(ra, rb, ta, tb), meet(la, lb, ba, bb), meet(ra, rb, ba, bb)
w = (np.linalg.norm(tr - tl) + np.linalg.norm(br - bl)) / 2
h = (np.linalg.norm(bl - tl) + np.linalg.norm(br - tr)) / 2
cx, cy = W / 2, (tl[1] + tr[1] + bl[1] + br[1]) / 4

def homography(s, d):
    A = []
    for (x, y), (u, v) in zip(s, d):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y, -u], [0, 0, 0, x, y, 1, -v * x, -v * y, -v]]
    return np.linalg.svd(np.array(A))[2][-1].reshape(3, 3)

srcq = [tl, tr, bl, br]
for z in np.arange(1.0, 1.6, 0.01):
    d = [(cx - z * w / 2, cy - z * h / 2), (cx + z * w / 2, cy - z * h / 2), (cx - z * w / 2, cy + z * h / 2), (cx + z * w / 2, cy + z * h / 2)]
    Hinv = np.linalg.inv(homography(srcq, d))
    pts = []
    for X, Y in ((0, 0), (W, 0), (0, H), (W, H)):
        p = Hinv @ [X, Y, 1]; pts.append(p[:2] / p[2])
    if all(-1 <= p[0] <= W + 1 and -1 <= p[1] <= H + 1 for p in pts):
        break
print("corners", [tuple(np.round(c)) for c in srcq], "zoom", round(z, 2))
args = ":".join(f"{p[0]:.2f}:{p[1]:.2f}" for p in pts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"perspective={args}:interpolation=cubic",
                "-c:v", "libx264", "-crf", "19", "-preset", "fast", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
