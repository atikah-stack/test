# Skin-only brightening: per-frame HSV skin key (excludes pink iPad / pink case / dark seat), feathered,
# temporally smoothed; lifts lightness and softens saturation inside the mask only.
import cv2, numpy as np
def skin_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    def band(x, lo, hi, soft):
        return np.clip(np.minimum((x - lo) / soft + 1, (hi - x) / soft + 1), 0, 1)
    m = band(h, 8, 23, 3) * band(s, 78, 190, 14) * band(v, 58, 235, 16)
    hard = (m > 0.35).astype(np.uint8)
    hard = cv2.morphologyEx(hard, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(hard)
    keep = np.zeros_like(hard)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 3000 and st[i, cv2.CC_STAT_HEIGHT] > 45: keep[lab == i] = 1
    keep = cv2.dilate(keep, np.ones((9, 9), np.uint8))
    keep = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 5)
    m = m * keep
    return cv2.GaussianBlur(m, (0, 0), 6)
def apply(bgr, m, lift=0.24, desat=0.2):
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    L2 = L + m * lift * (255 - L) * 0.9
    A2 = 128 + (A - 128) * (1 - m * desat); B2 = 128 + (B - 128) * (1 - m * desat * 1.2)
    out = np.dstack([L2, A2, B2]).clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(out, cv2.COLOR_LAB2BGR)
