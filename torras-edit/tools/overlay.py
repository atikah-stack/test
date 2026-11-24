"""Generate the transparent motion-graphics layer (RGBA, 1080x1920, 60fps, 1972 frames).
Source footage is never modified: this layer is composited on top by ffmpeg.
Usage: overlay.py SRC TRACKS FONTDIR (stream to stdout) | overlay.py SRC TRACKS FONTDIR --preview OUTDIR t1 t2 ..."""
import sys, json, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SRC, TRACKS, FONTDIR = sys.argv[1:4]
PREVIEW = "--preview" in sys.argv
W, H, FPS, NF = 1080, 1920, 60, 1972
HOOK_END = 313 / 60  # original hook hard-cuts out at ~5.22 s; nothing new appears before this

PINK = (244, 183, 206); ROSE = (216, 162, 184); CREAM = (255, 244, 232); WHITE = (255, 255, 255); SILVER = (216, 221, 227)
SCRIPT = ImageFont.truetype(f"{FONTDIR}/Gaegu-Regular.ttf", 55)  # mandated 55px; free look-alike of CapCut "Ugly Dave"
LABEL = ImageFont.truetype(f"{FONTDIR}/DMSans.ttf", 29)
try: LABEL.set_variation_by_axes([14, 600])
except Exception: pass
TAG = ImageFont.truetype(f"{FONTDIR}/DMSans.ttf", 32)
try: TAG.set_variation_by_axes([14, 600])
except Exception: pass

tracks = json.load(open(TRACKS))

# ---------------------------------------------------------------- easing / helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)

def M_at(name, f):
    tr = tracks[name]; f = min(max(f, tr["f0"]), tr["f1"])
    while str(f) not in tr["M"]: f += 1 if f < tr["anchor"] else -1
    return np.array(tr["M"][str(f)])
def tp(M, x, y): return (M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2])
def tscale(M): return math.hypot(M[0, 0], M[1, 0])
def trot(M): return math.degrees(math.atan2(M[1, 0], M[0, 0]))

class Canvas:
    def __init__(s): s.rgb = np.zeros((H, W, 3), np.float32); s.a = np.zeros((H, W), np.float32)
    def over(s, mask, color, opacity=1.0, bbox=None):
        """mask float [0,1] full-frame (or None-region), straight-alpha 'over' composite of a flat colour."""
        if opacity <= 0: return
        if bbox is None:
            ys, xs = np.nonzero(mask > 0.002)
            if len(xs) == 0: return
            bbox = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        x0, y0, x1, y1 = [int(v) for v in bbox]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        if x1 <= x0 or y1 <= y0: return
        m = mask[y0:y1, x0:x1] * opacity
        c = np.float32(color) / 255.0
        a0 = s.a[y0:y1, x0:x1]; r0 = s.rgb[y0:y1, x0:x1]
        na = m + a0 * (1 - m)
        s.rgb[y0:y1, x0:x1] = np.where(na[..., None] > 1e-6, (c * m[..., None] + r0 * (a0 * (1 - m))[..., None]) / np.maximum(na, 1e-6)[..., None], r0)
        s.a[y0:y1, x0:x1] = na
    def paste_rgba(s, img, x, y, opacity=1.0):
        """img float RGBA (h,w,4) straight alpha, top-left at x,y"""
        h, w = img.shape[:2]; x, y = int(round(x)), int(round(y))
        sx0, sy0 = max(0, -x), max(0, -y); dx0, dy0 = max(0, x), max(0, y)
        dx1, dy1 = min(W, x + w), min(H, y + h)
        if dx1 <= dx0 or dy1 <= dy0: return
        sub = img[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0]
        m = sub[..., 3] * opacity
        a0 = s.a[dy0:dy1, dx0:dx1]; r0 = s.rgb[dy0:dy1, dx0:dx1]
        na = m + a0 * (1 - m)
        s.rgb[dy0:dy1, dx0:dx1] = np.where(na[..., None] > 1e-6, (sub[..., :3] * m[..., None] + r0 * (a0 * (1 - m))[..., None]) / np.maximum(na, 1e-6)[..., None], r0)
        s.a[dy0:dy1, dx0:dx1] = na
    def out(s):
        return np.dstack([np.clip(s.rgb * 255 + .5, 0, 255), np.clip(s.a * 255 + .5, 0, 255)]).astype(np.uint8)

def blank(): return np.zeros((H, W), np.uint8)
def tofloat(m): return m.astype(np.float32) / 255.0
SS = 4  # cv2 sub-pixel shift bits
def P(p): return (int(round(p[0] * (1 << SS))), int(round(p[1] * (1 << SS))))

def stroke_arc(c, r, a0, a1, th, rot=0.0):
    m = blank()
    if abs(a1 - a0) < 0.3: return tofloat(m)
    cv2.ellipse(m, P(c), (int(r * (1 << SS)), int(r * (1 << SS))), rot, a0, a1, 255, th, cv2.LINE_AA, SS)
    return tofloat(m)
def stroke_poly(pts, th, closed=False):
    m = blank(); cv2.polylines(m, [np.int32([[p[0] * 16, p[1] * 16] for p in pts])], closed, 255, th, cv2.LINE_AA, 4); return tofloat(m)
def disc(c, r):
    m = blank(); cv2.circle(m, P(c), int(r * (1 << SS)), 255, -1, cv2.LINE_AA, SS); return tofloat(m)
def glow(mask, sigma): return cv2.GaussianBlur(mask, (0, 0), sigma)

def sparkle_mask(c, size, rot=0.0):
    """four-point star"""
    pts = []
    for k in range(8):
        ang = math.radians(rot + k * 45); rr = size if k % 2 == 0 else size * 0.22
        pts.append((c[0] + rr * math.sin(ang), c[1] - rr * math.cos(ang)))
    m = blank(); cv2.fillPoly(m, [np.int32([[p[0] * 16, p[1] * 16] for p in pts])], 255, cv2.LINE_AA, 4)
    return tofloat(m)

def draw_sparkle(cv, c, size, opacity, rot=0.0, color=WHITE):
    if opacity <= 0 or size < 1: return
    m = sparkle_mask(c, size, rot)
    cv.over(glow(m, size * 0.35), color, opacity * 0.55)
    cv.over(m, color, opacity)

def rounded_rect_path(x0, y0, x1, y1, r, n=12):
    pts = []
    for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            ang = math.radians(a + 90 * k / n); pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts
def partial_path(pts, frac):
    """first `frac` of polyline by arc length"""
    if frac <= 0: return []
    d = [0.0]
    for a, b in zip(pts, pts[1:]): d.append(d[-1] + math.dist(a, b))
    L = d[-1] * min(frac, 1.0); out = [pts[0]]
    for i in range(1, len(pts)):
        if d[i] <= L: out.append(pts[i])
        else:
            u = (L - d[i - 1]) / (d[i] - d[i - 1]); a, b = pts[i - 1], pts[i]
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)); break
    return out

# ---------------------------------------------------------------- handwriting headlines
def heart_poly(cx, cy, s):
    pts = []
    for k in range(64):
        t = 2 * math.pi * k / 64
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * s, cy - y * s))
    return pts

class Headline:
    """Script text rendered once; revealed with a pen-following stroke wipe."""
    def __init__(s, parts, icon=None):
        # parts: list of (text, colour)
        s.icon = icon
        dummy = ImageDraw.Draw(Image.new("L", (1, 1)))
        asc, desc = SCRIPT.getmetrics()
        widths = [dummy.textlength(t, font=SCRIPT) for t, _ in parts]
        tw = sum(widths); pad = 40
        icon_w = 44 if icon else 0
        Wd = int(tw + icon_w + 2 * pad); Hd = asc + desc + 2 * pad
        img = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        x = pad
        for (t, col), w in zip(parts, widths):
            d.text((x, pad), t, font=SCRIPT, fill=col + (255,)); x += w
        s.text_end = x
        arr = np.asarray(img).astype(np.float32) / 255.0
        s.baseline = pad + asc
        xh = pad + asc - 24  # approx x-height centre
        s.icon_c = (x + 24, xh - 2)
        s.img = arr; s.w, s.h = Wd, Hd; s.pad = pad
        # pen path: mean ink y per column
        a = arr[..., 3]; cols = a.sum(0); ys = (a * np.arange(Hd)[:, None]).sum(0) / np.maximum(cols, 1e-6)
        ys[cols < 0.5] = np.nan
        idx = np.arange(Wd); valid = ~np.isnan(ys)
        ys = np.interp(idx, idx[valid], ys[valid]) if valid.any() else np.full(Wd, Hd / 2)
        s.pen_y = cv2.GaussianBlur(ys.reshape(1, -1).astype(np.float32), (0, 0), 6).ravel()
        ink = np.nonzero(cols > 0.5)[0]; s.ink0, s.ink1 = int(ink.min()), int(ink.max())
        sh = np.clip(cv2.GaussianBlur(a, (0, 0), 3) * 0.75 + cv2.GaussianBlur(a, (0, 0), 12) * 0.9, 0, 0.62)
        s.shadow = np.dstack([np.zeros((Hd, Wd, 3), np.float32), sh])

    def draw(s, cv, t, t_in, t_out, cy, write=0.7):
        if t < t_in or t > t_out: return
        x0 = W / 2 - s.w / 2; y0 = cy - s.h / 2
        fade = 1 - ease_io(seg(t, t_out - 0.3, t_out))
        p = ease_io(seg(t, t_in, t_in + write))
        front = s.ink0 + (s.text_end - s.ink0 + 8) * p
        feather = 26.0
        xs = np.arange(s.w, dtype=np.float32)
        reveal = np.clip((front - xs) / feather + 0.5, 0, 1)
        fadein = ease_out(seg(t, t_in, t_in + 0.25))
        img = s.img.copy(); img[..., 3] *= reveal[None, :]
        shd = s.shadow.copy(); shd[..., 3] *= cv2.GaussianBlur(reveal.reshape(1, -1), (0, 0), 6).ravel()[None, :]
        cv.paste_rgba(img, x0, y0, fade * fadein)
        # pen nib glow follows the letters while writing
        if 0 < p < 1:
            fx = int(np.clip(front, 0, s.w - 1)); pc = (x0 + front, y0 + s.pen_y[fx])
            cv.over(glow(disc(pc, 5), 7), WHITE, 0.55 * fade)
            cv.over(disc(pc, 2.2), WHITE, 0.9 * fade)
        tw_end = t_in + write
        # icon (heart / sparkles) drawn after the words
        ic = (x0 + s.icon_c[0], y0 + s.icon_c[1])
        if s.icon == "heart":
            k = ease_out(seg(t, tw_end - 0.05, tw_end + 0.3))
            if k > 0:
                hp = heart_poly(ic[0], ic[1], 1.05 * (0.6 + 0.4 * k))
                m = blank(); cv2.fillPoly(m, [np.int32([[q[0] * 16, q[1] * 16] for q in hp])], 255, cv2.LINE_AA, 4)
                m = tofloat(m); cv.over(m, PINK, k * fade)
        elif s.icon == "sparkle":
            k = ease_out(seg(t, tw_end - 0.05, tw_end + 0.35))
            tw = 0.8 + 0.2 * math.sin((t - tw_end) * 9)
            draw_sparkle(cv, (ic[0] - 4, ic[1] + 2), 17 * k * tw, k * fade, color=PINK)
            draw_sparkle(cv, (ic[0] + 13, ic[1] - 16), 8 * k, k * fade * 0.9, rot=20, color=WHITE)
        # handwritten underline swash
        u = ease_io(seg(t, tw_end - 0.1, tw_end + 0.35))
        if u > 0:
            ux0 = x0 + s.ink0 + (s.text_end - s.ink0) * 0.08; ux1 = x0 + s.text_end - 6
            uy = y0 + s.baseline + 14
            pts = [(ux0 + (ux1 - ux0) * k / 40, uy + 3.5 * math.sin(k / 40 * math.pi) - 2 * k / 40) for k in range(41)]
            pp = partial_path(pts, u)
            if len(pp) > 1:
                m = stroke_poly(pp, 3); cv.over(m, PINK, 0.95 * fade)
            # sparkle at stroke completion
            sp = ease_out(seg(t, tw_end + 0.25, tw_end + 0.6)) * (1 - seg(t, tw_end + 0.9, tw_end + 1.3))
            if sp > 0: draw_sparkle(cv, (ux1 + 10, uy - 6), 11 * sp, sp * fade, rot=(t - tw_end) * 40)

def label(cv, text, x, y, opacity, color=CREAM, font=LABEL, anchor="lm"):
    if opacity <= 0: return
    d = ImageDraw.Draw(Image.new("L", (1, 1))); bb = d.textbbox((0, 0), text, font=font, anchor=anchor)
    w, h = bb[2] - bb[0] + 24, bb[3] - bb[1] + 24
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dd = ImageDraw.Draw(img)
    dd.text((12 - bb[0], 12 - bb[1]), text, font=font, fill=color + (255,), anchor=anchor)
    a = np.asarray(img).astype(np.float32) / 255.0
    sh = np.dstack([np.zeros((h, w, 3), np.float32), np.clip(cv2.GaussianBlur(a[..., 3], (0, 0), 2.5) * 0.8 + cv2.GaussianBlur(a[..., 3], (0, 0), 8) * 0.6, 0, 0.7)])
    X, Y = x + bb[0] - 12, y + bb[1] - 12
    X = min(max(X, W * 0.12), W * 0.88 - w + 24)  # keep inside safe margins
    cv.paste_rgba(a, X, Y, opacity)

def light_sweep(cv, poly, prog, width=150, strength=0.30, angle=-28):
    """soft diagonal light band crossing a (tracked) polygon"""
    if prog <= 0 or prog >= 1: return
    m = blank(); cv2.fillPoly(m, [np.int32(poly)], 255, cv2.LINE_AA)
    pm = glow(tofloat(m), 6)
    xs = np.array([p[0] for p in poly]); ys = np.array([p[1] for p in poly])
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    span = (x1 - x0) + (y1 - y0) * 0.6 + 2 * width
    cx = x0 - width + span * prog
    X, Y = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    d = (X - cx) + (Y - (y0 + y1) / 2) * math.tan(math.radians(angle))
    band = np.exp(-(d / (width * 0.45)) ** 2) + 0.5 * np.exp(-((d + width * 0.9) / (width * 0.12)) ** 2)
    env = math.sin(math.pi * prog)
    cv.over(np.clip(band, 0, 1) * pm, WHITE, strength * env, bbox=(x0 - 5, y0 - 5, x1 + 5, y1 + 5))

def tracked_poly(M, pts): return [tp(M, *p) for p in pts]

# ---------------------------------------------------------------- cue sheet
HL = {
    "unbox":   Headline([("Unboxing my favourite", WHITE)], "heart"),
    "crystal": Headline([("Crystal Clear", WHITE)], "heart"),
    "yellow":  Headline([("Anti-Yellowing Design", WHITE)]),
    "camera":  Headline([("Everyday Protection", WHITE)], "heart"),
    "stand":   Headline([("360° Rotating Stand", WHITE)], "sparkle"),
    "slim":    Headline([("Slim & Comfortable", WHITE)]),
    "magnet":  Headline([("Magnetic Compatible", WHITE)], "heart"),
    "hands":   Headline([("Hands-Free Viewing", WHITE)], "heart"),
    "worth":   Headline([("Worth it", WHITE)], "heart"),
}
Y38, Y40, Y62 = H * 0.38, H * 0.40, H * 0.62
CUES = [  # key, t_in, t_out, centre-y, write duration
    ("unbox", 6.00, 8.40, Y38, 0.80), ("crystal", 16.10, 17.90, Y38, 0.60), ("yellow", 18.00, 19.35, Y38, 0.75),
    ("camera", 22.80, 23.85, Y62, 0.65), ("stand", 23.90, 25.50, Y38, 0.70), ("slim", 27.20, 28.45, Y40, 0.65),
    ("magnet", 28.62, 30.00, Y62, 0.70), ("hands", 30.15, 31.50, Y38, 0.70), ("worth", 31.60, 32.80, Y38, 0.45),
]
assert all(c[1] > HOOK_END + 0.3 for c in CUES)

def features(cv, t, f, frame):
    # A/C. Crystal clear: tracked edge trace + light sweep (16.10-17.90)
    if 16.10 <= t <= 17.90:
        M = M_at("crystal", f); fade = 1 - seg(t, 16.95, 17.18)
        rr = rounded_rect_path(330, 700, 640, 1292, 46)
        pts = tracked_poly(M, rr)
        tr = ease_io(seg(t, 16.20, 16.80))
        pp = partial_path(pts, tr)
        if len(pp) > 1:
            m = stroke_poly(pp, 3); cv.over(glow(m, 5), WHITE, 0.35 * fade); cv.over(m, WHITE, 0.85 * fade)
            draw_sparkle(cv, pp[-1], 9, 0.9 * fade * (tr < 1))
        light_sweep(cv, pts, seg(t, 16.30, 17.10), strength=0.32 * fade)
        k = ease_out(seg(t, 16.75, 16.95)) * fade
        draw_sparkle(cv, tp(M, 630, 712), 16 * k, k, rot=(t - 17) * 60)
    # F. Anti-yellowing: clean-glass sweep + minimal line (18.00-19.35)
    if 18.00 <= t <= 19.35:
        M = M_at("yellow", f); fade = 1 - seg(t, 19.05, 19.35)
        pts = tracked_poly(M, rounded_rect_path(400, 510, 800, 1340, 50))
        light_sweep(cv, pts, seg(t, 18.15, 19.05), width=190, strength=0.26 * fade, angle=-35)
        ln = ease_io(seg(t, 18.2, 18.75))
        a, b = tp(M, 440, 540), tp(M, 760, 540)
        if ln > 0:
            m = stroke_poly([a, (a[0] + (b[0] - a[0]) * ln, a[1] + (b[1] - a[1]) * ln)], 2)
            cv.over(glow(m, 4), WHITE, 0.4 * fade); cv.over(m, WHITE, 0.85 * fade)
        for i, (px, py, t0) in enumerate(((470, 760, 18.4), (720, 980, 18.6), (560, 1180, 18.8))):
            k = math.sin(math.pi * seg(t, t0, t0 + 0.5))
            draw_sparkle(cv, tp(M, px, py), 10 * k, k * fade, rot=i * 25)
    # E. Camera protection: dashed circle + pointer (22.80-23.85)
    if 22.80 <= t <= 23.85:
        M = M_at("camera", f); s = tscale(M); fade = 1 - seg(t, 23.55, 23.85)
        c = tp(M, 418, 752); r = 118 * s
        prog = ease_io(seg(t, 22.85, 23.30)); spin = (t - 22.8) * 25
        m = blank(); n = 28
        for k in range(int(n * prog)):
            a0 = -90 + spin + k * 360 / n
            cv2.ellipse(m, P(c), (int(r * 16), int(r * 16)), 0, a0, a0 + 360 / n * 0.55, 255, 3, cv2.LINE_AA, SS)
        m = tofloat(m); cv.over(glow(m, 4), WHITE, 0.35 * fade); cv.over(m, WHITE, 0.9 * fade)
        pk = ease_io(seg(t, 23.15, 23.45))
        if pk > 0:
            p0 = (c[0] + r * 0.72, c[1] - r * 0.70); p1 = (p0[0] + 95, p0[1] - 80); p2 = (p1[0] + 150, p1[1])
            pp = partial_path([p0, p1, p2], pk)
            cv.over(disc(p0, 5), WHITE, fade)
            if len(pp) > 1: cv.over(stroke_poly(pp, 2), WHITE, 0.9 * fade)
            label(cv, "Raised camera edge", p1[0] + 6, p1[1] - 24, ease_out(seg(t, 23.3, 23.5)) * fade)
    # B. 360 stand: circular arrow, 360 tag, magnified inset (23.90-25.50)
    if 23.90 <= t <= 25.50:
        M = M_at("stand", f); s = tscale(M); fade = 1 - seg(t, 25.2, 25.5)
        c = tp(M, 440, 1150); r = 78 * s
        g = ease_out(seg(t, 23.95, 24.25))
        cv.over(glow(disc(c, 26 * s), 14), WHITE, 0.45 * g * fade)
        draw_in = ease_io(seg(t, 24.0, 24.45)); spin = 360 * ease_io(seg(t, 24.0, 25.4))
        sweep = 290 * draw_in
        if sweep > 1:
            a0 = -90 + spin; a1 = a0 + sweep
            m = stroke_arc(c, r, a0, a1, 3); cv.over(glow(m, 4), WHITE, 0.35 * fade); cv.over(m, WHITE, 0.92 * fade)
            # arrow head at the leading end
            ang = math.radians(a1); tip = (c[0] + r * math.cos(ang), c[1] + r * math.sin(ang))
            tang = (-math.sin(ang), math.cos(ang)); nrm = (math.cos(ang), math.sin(ang))
            hl = 14
            pa = (tip[0] - tang[0] * hl + nrm[0] * hl * 0.6, tip[1] - tang[1] * hl + nrm[1] * hl * 0.6)
            pb = (tip[0] - tang[0] * hl - nrm[0] * hl * 0.6, tip[1] - tang[1] * hl - nrm[1] * hl * 0.6)
            cv.over(stroke_poly([pa, tip, pb], 3), WHITE, 0.92 * fade * draw_in)
        tg = ease_out(seg(t, 24.3, 24.6))
        label(cv, "360°", c[0] - 38, c[1] - r - 34, tg * fade, color=WHITE, font=TAG)
        # magnified inset of the real hinge (zoom only inside the overlay)
        ik = ease_out(seg(t, 24.35, 24.7)) * fade
        if ik > 0 and frame is not None:
            R = 108; ic = (838, 1000); zoom = 1.9
            src_r = R / zoom
            x0, y0 = int(c[0] - src_r), int(c[1] - src_r)
            crop = frame[max(0, y0):y0 + int(2 * src_r), max(0, x0):x0 + int(2 * src_r)]
            if crop.size and crop.shape[0] > 10 and crop.shape[1] > 10:
                crop = cv2.resize(crop, (2 * R, 2 * R), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255.0
                cm = np.zeros((2 * R, 2 * R), np.uint8); cv2.circle(cm, (R, R), R - 1, 255, -1, cv2.LINE_AA)
                rr = R * (0.85 + 0.15 * ik)
                img = np.dstack([crop, tofloat(cm)])
                img = cv2.resize(img, (int(2 * rr), int(2 * rr)), interpolation=cv2.INTER_AREA)
                cv.over(glow(disc(ic, rr), 10), (0, 0, 0), 0.30 * ik)
                cv.paste_rgba(img, ic[0] - rr, ic[1] - rr, ik)
                cv.over(stroke_arc(ic, rr, 0, 360, 3), WHITE, 0.95 * ik)
                # connector
                v = (ic[0] - c[0], ic[1] - c[1]); dl = math.hypot(*v) or 1
                a = (c[0] + v[0] / dl * (r + 6), c[1] + v[1] / dl * (r + 6)); b = (ic[0] - v[0] / dl * (rr + 4), ic[1] - v[1] / dl * (rr + 4))
                cv.over(stroke_poly([a, b], 2), WHITE, 0.7 * ik)
    # D. Slim: edge highlight + pointer (27.20-28.45)
    if 27.20 <= t <= 28.45:
        M = M_at("slim", f); fade = 1 - seg(t, 28.15, 28.45)
        a, b = tp(M, 196, 1384), tp(M, 662, 1402)
        e = ease_io(seg(t, 27.25, 27.75))
        if e > 0:
            q = (a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e)
            m = stroke_poly([a, q], 3); cv.over(glow(m, 6), WHITE, 0.45 * fade); cv.over(m, WHITE, 0.9 * fade)
            for pnt in (a, q):
                cv.over(stroke_poly([(pnt[0], pnt[1] - 12), (pnt[0], pnt[1] + 12)], 2), WHITE, 0.8 * fade)
        pk = ease_io(seg(t, 27.6, 27.9))
        if pk > 0:
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            p1 = (mid[0] + 120, mid[1] + 95); p2 = (p1[0] + 140, p1[1])
            pp = partial_path([mid, p1, p2], pk)
            cv.over(disc(mid, 5), WHITE, fade)
            if len(pp) > 1: cv.over(stroke_poly(pp, 2), WHITE, 0.9 * fade)
            label(cv, "Slim profile", p1[0] + 6, p1[1] + 26, ease_out(seg(t, 27.8, 28.0)) * fade)
    # A. Magnetic: pulses around the real mount the phone snaps onto (28.62-30.00)
    if 28.62 <= t <= 30.00:
        M = M_at("mount", f); s = tscale(M); fade = 1 - seg(t, 29.7, 30.0)
        c = tp(M, 324, 745); r = 96 * s
        o = ease_io(seg(t, 28.68, 29.2))
        if o > 0:
            m = stroke_arc(c, r, -90, -90 + 360 * o, 3); cv.over(glow(m, 5), WHITE, 0.4 * fade); cv.over(m, WHITE, 0.9 * fade)
            ang = math.radians(-90 + 360 * o)
            if o < 1: cv.over(glow(disc((c[0] + r * math.cos(ang), c[1] + r * math.sin(ang)), 6), 6), WHITE, 0.9 * fade)
        for k, t0 in enumerate((28.75, 29.1, 29.45)):
            u = seg(t, t0, t0 + 0.7)
            if 0 < u < 1:
                cv.over(stroke_arc(c, r + 10 + 90 * ease_out(u), 0, 360, 2), PINK, (1 - u) * 0.85 * fade)
    # Hands-free: stand foot glow + label (30.15-31.50)
    if 30.15 <= t <= 31.50:
        M = M_at("dash1", f); fade = 1 - seg(t, 31.25, 31.5)
        c = tp(M, 529, 1276)
        g = ease_out(seg(t, 30.3, 30.6))
        cv.over(glow(disc(c, 22), 12), WHITE, 0.45 * g * fade)
        o = ease_io(seg(t, 30.35, 30.8))
        if o > 0: cv.over(stroke_arc(c, 46, -90, -90 + 360 * o, 2), WHITE, 0.9 * fade)
        pk = ease_io(seg(t, 30.7, 30.95))
        if pk > 0:
            p0 = (c[0] + 46 * 0.7, c[1] + 46 * 0.7); p1 = (p0[0] + 80, p0[1] + 70); p2 = (p1[0] + 130, p1[1])
            pp = partial_path([p0, p1, p2], pk)
            if len(pp) > 1: cv.over(stroke_poly(pp, 2), WHITE, 0.9 * fade)
            label(cv, "Built-in stand", p1[0] + 6, p1[1] + 26, ease_out(seg(t, 30.85, 31.05)) * fade)
    # A. Final: clockwise ring trace with light trail (31.60-32.80)
    if 31.60 <= t <= 32.866:
        M = M_at("dash2", f); s = tscale(M); fade = 1 - seg(t, 32.55, 32.86)
        c = tp(M, 432, 1046); r = 100 * s
        o = ease_io(seg(t, 31.65, 32.3))
        if o > 0:
            a1 = -90 + 360 * o
            m = stroke_arc(c, r, -90, a1, 3); cv.over(glow(m, 5), WHITE, 0.4 * fade); cv.over(m, WHITE, 0.9 * fade)
            for k in range(6):  # comet light trail
                aa = math.radians(a1 - k * 6)
                cv.over(glow(disc((c[0] + r * math.cos(aa), c[1] + r * math.sin(aa)), 5 - k * 0.6), 5), WHITE, (0.9 - k * 0.14) * fade * (o < 1))
        u = seg(t, 32.3, 32.85)
        if 0 < u < 1: cv.over(stroke_arc(c, r + 8 + 60 * ease_out(u), 0, 360, 2), PINK, (1 - u) * 0.8)

def render(f, frame):
    t = f / FPS; cv = Canvas()
    if t < HOOK_END: return None  # original hook untouched: fully transparent
    features(cv, t, f, frame)
    for key, a, b, cy, wd in CUES:
        HL[key].draw(cv, t, a, b, cy, wd)
    return cv.out()

def need_frame(t): return 24.3 <= t <= 25.55

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                        "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
EMPTY = bytes(W * H * 4)
if PREVIEW:
    outdir = sys.argv[sys.argv.index("--preview") + 1]
    want = {round(float(x) * FPS) for x in sys.argv[sys.argv.index("--preview") + 2:]}
out = sys.stdout.buffer
for f in range(NF):
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3: raw = None
    if PREVIEW:
        if f not in want: continue
        frame = np.frombuffer(raw, np.uint8).reshape(H, W, 3) if raw else None
        ov = render(f, frame)
        base = frame.astype(np.float32)
        if ov is not None:
            a = ov[..., 3:4].astype(np.float32) / 255; base = base * (1 - a) + ov[..., :3] * a
        cv2.imwrite(f"{outdir}/p_{f/FPS:06.2f}.jpg", cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
        want.discard(f)
        if not want: break
        continue
    t = f / FPS
    frame = np.frombuffer(raw, np.uint8).reshape(H, W, 3) if (raw and need_frame(t)) else None
    ov = render(f, frame)
    out.write(EMPTY if ov is None or not ov[..., 3].any() else ov.tobytes())
    if f % 120 == 0: print(f"overlay {f}/{NF}", file=sys.stderr, flush=True)
dec.stdout.close(); dec.wait()
