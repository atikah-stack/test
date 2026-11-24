"""Track rigid product regions with LK optical flow + RANSAC similarity.
Outputs per-frame 2x3 matrices mapping anchor-frame coords -> frame coords."""
import cv2, numpy as np, json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
SC = 0.5  # work at half res
# name: (anchor_t, roi x0,y0,x1,y1 in full-res anchor frame, t_start, t_end)
CUES = {
    "crystal": (16.6, (330, 700, 640, 1290), 16.05, 17.95),
    "yellow":  (18.6, (400, 510, 800, 1340), 17.95, 19.40),
    "camera":  (23.0, (330, 655, 645, 1330), 22.75, 23.90),
    "stand":   (24.6, (330, 615, 685, 1355), 23.85, 25.55),
    "slim":    (27.6, (190, 910, 700, 1420), 27.15, 28.50),
    "mount":   (28.9, (230, 640, 420, 860), 28.60, 30.05),
    "dash1":   (30.5, (360, 600, 650, 1360), 30.10, 31.53),
    "dash2":   (32.0, (315, 630, 800, 1280), 31.56, 32.87),
}
NF = 1972
need = set()
for a, roi, t0, t1 in CUES.values():
    need.update(range(max(0, round(t0 * 60) - 1), min(NF, round(t1 * 60) + 2)))
cap = cv2.VideoCapture(SRC); frames = {}; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i in need:
        frames[i] = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), None, fx=SC, fy=SC)
    i += 1

def feats(g, poly):
    m = np.zeros_like(g); cv2.fillPoly(m, [np.int32(poly)], 255)
    return cv2.goodFeaturesToTrack(g, 300, 0.01, 5, mask=m)

def step(ga, gb, poly):
    p = feats(ga, poly)
    if p is None or len(p) < 6: return np.float64([[1, 0, 0], [0, 1, 0]])
    q, st, _ = cv2.calcOpticalFlowPyrLK(ga, gb, p, None, winSize=(21, 21), maxLevel=3)
    good = st.ravel() == 1
    M, inl = cv2.estimateAffinePartial2D(p[good], q[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return M if M is not None else np.float64([[1, 0, 0], [0, 1, 0]])

def h(M): return np.vstack([M, [0, 0, 1]])

out = {}
for name, (ta, roi, t0, t1) in CUES.items():
    fa, f0, f1 = round(ta * 60), round(t0 * 60), min(NF - 1, round(t1 * 60))
    x0, y0, x1, y1 = [v * SC for v in roi]
    poly0 = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    T = {fa: np.eye(3)}
    for direction in (1, -1):
        cur = np.eye(3); k = fa
        while (k < f1 if direction > 0 else k > f0):
            n = k + direction
            poly = cv2.transform(poly0[None], cur[:2])[0]
            M = step(frames[k], frames[n], poly)
            cur = h(M) @ cur; T[n] = cur.copy(); k = n
    res = {}
    for k, Mt in T.items():
        A = Mt.copy(); A[:2, 2] /= SC  # translation back to full res (similarity scale invariant)
        res[k] = A[:2].tolist()
    out[name] = {"anchor": fa, "f0": f0, "f1": f1, "M": res}
    s = [np.hypot(*np.array(v)[0, :2]) for v in res.values()]
    print(name, f0, f1, "scale range %.2f-%.2f" % (min(s), max(s)))
json.dump(out, open(OUT, "w"))
