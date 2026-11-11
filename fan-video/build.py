#!/usr/bin/env python3
"""Generate the GOOJODOQ mini fan TikTok edit (1080x1920, ~22.7 s).

Writes index.html (footage, transitions, sound) and compositions/fx.html
(all typography and motion graphics). Run: python3 build.py .
"""
import os, sys

PROJ = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1080, 1920
TOTAL = 22.7
PINK, CREAM = "#F4B7CE", "#FFF4E8"
AIR = "#BFE3FF"
OVERLAP = 0.5  # each clip keeps playing under the next one's transition

# ------------------------------------------------------------------ shots
# (start, end, src, media_start, focus (x, y), transition-in, own-audio volume)
shots = [
    (0.00, 1.20, "f0809", 2.55, (570, 935), "open", 0),
    (1.20, 2.30, "f7657", 4.20, (520, 1400), "circle", 0),
    (2.30, 4.50, "f0804", 1.20, (375, 870), "slide", 0),
    (4.50, 5.70, "f0802", 0.10, (420, 1150), "punch", 0.9),
    (5.70, 7.00, "f0803", 1.60, (420, 1100), "wipe", 0.9),
    (7.00, 9.40, "f0807", 0.50, (510, 1185), "circle", 0),
    (9.40, 11.40, "f0808", 2.60, (415, 1110), "punch", 0),
    (11.40, 12.90, "f7657", 0.30, (520, 1400), "slide", 0),
    (12.90, 14.90, "f7659", 0.50, (560, 1180), "circle", 0.6),
    (14.90, 16.50, "f7660", 1.00, (540, 900), "punch", 0.7),
    (16.50, 18.30, "f0809", 4.70, (520, 1280), "wipe", 0),
    (18.30, 19.50, "f7658", 5.40, (480, 1400), "punch", 0),
    (19.50, 21.20, "f7658", 10.00, (600, 1500), "circle", 0),
    (21.20, TOTAL, "f0809", 9.60, (640, 830), "punch", 0),
]

shot_html, js = [], []
for n, (s, e, src, ms, (fx, fy), tr, vol) in enumerate(shots, 1):
    d = round(min(e + OVERLAP, TOTAL) - s, 3)
    audio = f'data-has-audio="true" data-volume="{vol}"' if vol else "muted"
    org = f"transform-origin:{fx}px {fy}px"
    shot_html.append(
        f'      <div id="pw{n}" class="frame" style="z-index:{n};{org}">\n'
        f'        <div id="sw{n}" class="frame" style="{org}">\n'
        f'          <video id="v{n}" class="clip media" data-start="{s}" data-duration="{d}" data-media-start="{ms}" '
        f'data-track-index="{n % 2}" src="assets/{src}.mp4" {audio} playsinline></video>\n'
        f'        </div>\n      </div>')
    # slow push toward the product for the whole shot
    js.append(f'tl.fromTo("#sw{n}", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {d}, ease: "none" }}, {s});')
    if tr == "open":
        js.append(f'tl.fromTo("#pw{n}", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.8, ease: "power3.out" }}, 0);')
    elif tr == "punch":
        js.append(f'tl.fromTo("#pw{n}", {{ scale: 1.16, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "power3.out" }}, {s - 0.08:.3f});')
    elif tr == "circle":
        js.append(f'tl.fromTo("#pw{n}", {{ clipPath: "circle(0% at {fx}px {fy}px)" }}, {{ clipPath: "circle(140% at {fx}px {fy}px)", duration: 0.5, ease: "power3.in" }}, {s - 0.3:.3f});')
    elif tr == "slide":
        js.append(f'tl.fromTo("#pw{n}", {{ xPercent: 100 }}, {{ xPercent: 0, duration: 0.42, ease: "expo.out" }}, {s - 0.12:.3f});')
    elif tr == "wipe":
        js.append(f'tl.fromTo("#pw{n}", {{ clipPath: "inset(100% 0% 0% 0% round 80px)" }}, {{ clipPath: "inset(0% 0% 0% 0% round 0px)", duration: 0.48, ease: "power3.inOut" }}, {s - 0.3:.3f});')

# ------------------------------------------------------------------ sfx
def at(t, peak): return round(max(0, t - peak - 0.03), 3)
sfx = []
for k, (s, *_r) in enumerate(shots[1:]):
    sfx.append(("whoosh-short" if k % 2 else "whoosh", at(s, 0.162), 0.45, 0.3))
sfx += [
    ("pop", at(0.40, 0.12), 0.5, 0.45),
    ("click-soft", at(2.55, 0.05), 0.4, 0.5),
    ("pop", at(3.05, 0.12), 0.5, 0.4),
    ("pop", at(7.45, 0.12), 0.5, 0.4),
    ("pop", at(9.90, 0.12), 0.5, 0.5),
    ("click", at(10.50, 0.05), 0.4, 0.5),
    ("click", at(13.25, 0.05), 0.4, 0.55),
    ("click", at(13.85, 0.05), 0.4, 0.55),
    ("click", at(14.45, 0.05), 0.4, 0.6),
    ("pop", at(16.95, 0.12), 0.5, 0.4),
    ("click-soft", at(19.75, 0.05), 0.4, 0.5),
    ("click-soft", at(20.10, 0.05), 0.4, 0.5),
    ("click-soft", at(20.45, 0.05), 0.4, 0.5),
    ("sparkle", at(21.75, 0.027), 0.9, 0.16),
]
track_end, sfx_html = {}, []
for k, (f, s, d, v) in enumerate(sorted(sfx, key=lambda x: x[1]), 1):
    tr = next(t for t in range(10, 40) if track_end.get(t, -1) <= s)
    track_end[tr] = s + d
    sfx_html.append(f'      <audio id="sfx{k}" class="clip" data-start="{s}" data-duration="{d}" '
                    f'data-track-index="{tr}" data-volume="{v}" src="assets/sfx/{f}.mp3"></audio>')

index = f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #141012; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #141012; }}
      .frame {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
      .media {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(shot_html)}

      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0"
        data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:50"></div>

{chr(10).join(sfx_html)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + l for l in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(PROJ, "index.html"), "w").write(index)

# ------------------------------------------------------------------ fx (type + graphics)
X0, TW = 130, 820  # 12% side margins, centered at x = 540
fx_html, fj = [], []

def words(id_, text, cls, top, size, color=None, font="h"):
    """A centered line split into word spans so it can stagger in."""
    style = f"top:{top}px;font-size:{size}px" + (f";color:{color}" if color else "")
    spans = " ".join(f'<span class="w">{w}</span>' for w in text.split(" "))
    return f'<div id="{id_}" class="line {cls} f-{font}" style="{style}">{spans}</div>'

def reveal(sel, t, stagger=0.06):
    fj.append(f'tl.fromTo("{sel} .w", {{ opacity: 0, y: 34, scale: 0.86, filter: "blur(10px)" }}, '
              f'{{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "power3.out", stagger: {stagger} }}, {t});')

def out(sel, t):
    fj.append(f'tl.to("{sel}", {{ opacity: 0, y: -18, duration: 0.25, ease: "power2.in" }}, {t - 0.25:.3f});')
    fj.append(f'tl.set("{sel}", {{ opacity: 0 }}, {t});')

def show(sel, t):
    fj.append(f'tl.set("{sel}", {{ opacity: 1, y: 0 }}, {t});')

def underline(id_, top, width, t, color=PINK):
    fx_html.append(f'<div id="{id_}" class="uline" style="top:{top}px;left:{540 - width // 2}px;width:{width}px;background:{color}"></div>')
    fj.append(f'tl.fromTo("#{id_}", {{ scaleX: 0, opacity: 1 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.inOut" }}, {t});')

def dashed_circle(id_, cx, cy, r, t, dur, to=None):
    size = 2 * r + 20
    fx_html.append(
        f'<div id="{id_}" class="ring" style="left:{cx - size // 2}px;top:{cy - size // 2}px;width:{size}px;height:{size}px">'
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}"><circle cx="{size / 2}" cy="{size / 2}" r="{r}" '
        f'fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="18 14" stroke-linecap="round"/></svg></div>')
    fj.append(f'tl.fromTo("#{id_}", {{ opacity: 0, scale: 0.55, rotation: -60 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }}, {t});')
    fj.append(f'tl.to("#{id_}", {{ rotation: 70, duration: {dur}, ease: "none" }}, {t + 0.5:.3f});')
    if to:
        fj.append(f'tl.to("#{id_}", {{ x: {to[0] - cx}, y: {to[1] - cy}, duration: {to[2]}, ease: "sine.inOut" }}, {t:.3f});')
    fj.append(f'tl.to("#{id_}", {{ opacity: 0, scale: 1.15, duration: 0.25, ease: "power2.in" }}, {t + 0.5 + dur - 0.25:.3f});')

def pulse(id_, cx, cy, r, t, reps=2, color="#fff"):
    fx_html.append(f'<div id="{id_}" class="pulse" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-color:{color}"></div>')
    fj.append(f'tl.fromTo("#{id_}", {{ opacity: 0.85, scale: 0.6 }}, {{ opacity: 0, scale: 1.7, duration: 0.8, ease: "power2.out", repeat: {reps}, immediateRender: false }}, {t});')

def sparkle(id_, x, y, s, t):
    fx_html.append(f'<svg id="{id_}" class="spark" style="left:{x - s // 2}px;top:{y - s // 2}px" width="{s}" height="{s}" viewBox="0 0 20 20">'
                   f'<path d="M10 0 C11 7 13 9 20 10 C13 11 11 13 10 20 C9 13 7 11 0 10 C7 9 9 7 10 0Z" fill="{CREAM}"/></svg>')
    fj.append(f'tl.fromTo("#{id_}", {{ opacity: 0, scale: 0, rotation: -45 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(3)" }}, {t});')
    fj.append(f'tl.to("#{id_}", {{ opacity: 0, scale: 0.4, rotation: 45, duration: 0.35, ease: "power2.in" }}, {t + 0.7:.3f});')

# ---- scene 1+2: hook (0 - 2.3)
fx_html.append('<div id="g1" class="grp">')
fx_html.append(words("g1a", "EH, KIPAS MINI NI", "", 420, 66))
fx_html.append(words("g1b", "CUCUK TERUS JE?! 👀", "", 506, 70, PINK))
fx_html.append('</div>')
underline("u1", 600, 220, 0.55)
show("#g1", 0)
fj.append('tl.fromTo("#g1a .w", { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power3.out", stagger: 0.05 }, 0.02);')
fj.append('tl.fromTo("#g1b .w", { opacity: 0, y: 26, scale: 1.25 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)", stagger: 0.07 }, 0.22);')
dashed_circle("c1", 570, 935, 215, 0.35, 0.6)
pulse("p1", 570, 935, 150, 0.45, 0)
fj.append('tl.fromTo("#g1", { y: 0 }, { y: -12, duration: 1.7, ease: "none" }, 0.3);')
out("#g1", 2.3)
fj.append('tl.to("#u1", { scaleX: 0, transformOrigin: "100% 50%", duration: 0.25 }, 2.05);')

# ---- scene 3: brand intro (2.3 - 4.5)
fx_html.append('<div id="g2" class="grp">')
fx_html.append('<div id="g2a" class="line brand f-h" style="top:1330px;font-size:76px">' + "".join(f'<span id="gc{i}" class="w">{c}</span>' for i, c in enumerate("GOOJODOQ")) + '</div>')
fx_html.append(words("g2b", "USB TYPE-C MINI FAN", "sub", 1430, 42, PINK, "b"))
fx_html.append('</div>')
show("#g2", 2.45)
for i in range(8):
    fj.append(f'tl.fromTo("#gc{i}", {{ opacity: 0, x: {(i - 3.5) * 46:.0f}, y: 10 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.75, ease: "power3.out" }}, {2.5 + abs(i - 3.5) * 0.03:.3f});')
reveal("#g2b", 2.85, 0.07)
underline("u2", 1500, 180, 3.15, CREAM)
fx_html.append(f'<svg id="arc2" class="arc" style="left:175px;top:670px" width="400" height="400" viewBox="0 0 400 400">'
               f'<path d="M 60 290 A 160 160 0 1 1 330 300" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" '
               f'stroke-dasharray="820" stroke-dashoffset="820"/></svg>')
fj.append('tl.set("#arc2", { opacity: 1 }, 2.95);')
fj.append('tl.fromTo("#arc2 path", { attr: { "stroke-dashoffset": 820 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.7, ease: "power2.inOut" }, 2.95);')
fj.append('tl.to("#arc2", { opacity: 0, duration: 0.25 }, 4.2);')
sparkle("s2", 590, 690, 34, 3.4)
out("#g2", 4.5)
fj.append('tl.to("#u2", { opacity: 0, duration: 0.2 }, 4.25);')

# ---- scene 4: unboxing (4.5 - 7.0)
fx_html.append(words("g3", "unboxing this mini fan ♡", "soft", 400, 60, CREAM, "b"))
show("#g3", 4.6)
reveal("#g3", 4.6, 0.08)
underline("u3", 488, 300, 5.05)
fj.append('tl.to("#u3", { scaleX: 0.3, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 5.8);')
out("#g3", 7.0)
fj.append('tl.to("#u3", { opacity: 0, duration: 0.2 }, 6.8);')

# ---- scene 5: pink reveal (7.0 - 9.4)
fx_html.append(words("g4", "Pink edition is so cute ♡", "", 790, 62))
show("#g4", 7.15)
reveal("#g4", 7.15, 0.07)
fj.append('tl.fromTo("#g4 .w:last-child", { color: "#fff" }, { color: "' + PINK + '", duration: 0.3 }, 7.7);')
underline("u4", 872, 260, 7.6)
fx_html.append('<svg id="ol4" class="arc" style="left:240px;top:925px" width="540" height="520" viewBox="0 0 540 520">'
               '<ellipse cx="270" cy="260" rx="255" ry="245" fill="none" stroke="#fff" stroke-width="4" '
               'stroke-dasharray="1580" stroke-dashoffset="1580" stroke-linecap="round"/></svg>')
fj.append('tl.set("#ol4", { opacity: 1 }, 7.45);')
fj.append('tl.fromTo("#ol4 ellipse", { attr: { "stroke-dashoffset": 1580 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.9, ease: "power2.inOut" }, 7.45);')
fj.append('tl.to("#ol4", { opacity: 0, scale: 1.08, transformOrigin: "50% 50%", duration: 0.35 }, 8.7);')
sparkle("s4a", 800, 960, 30, 8.0)
sparkle("s4b", 250, 1380, 24, 8.2)
out("#g4", 9.4)
fj.append('tl.to("#u4", { opacity: 0, duration: 0.2 }, 9.15);')

# ---- scene 6+7: USB-C (9.4 - 12.9)
fx_html.append('<div id="g5" class="grp">')
fx_html.append(words("g5a", "USB TYPE-C", "", 400, 76))
fx_html.append(words("g5b", "Plug &amp; Play ⚡", "sub", 495, 44, PINK, "b"))
fx_html.append('</div>')
show("#g5", 9.5)
reveal("#g5a", 9.5, 0.08)
reveal("#g5b", 9.75, 0.08)
# connector moves from (420,1155) to (405,1035) between media 3.0 and 3.8 -> 9.8..10.6 in the edit
dashed_circle("c5", 420, 1170, 120, 9.75, 1.0, to=(405, 1040, 0.9))
pulse("p5", 420, 1170, 90, 9.9, 1)
fj.append('tl.to("#p5", { x: -15, y: -130, duration: 0.9, ease: "sine.inOut" }, 9.9);')
fx_html.append('<svg id="ptr5" class="arc" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">'
               '<path d="M 540 585 C 560 760 520 880 470 960" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" '
               'stroke-dasharray="460" stroke-dashoffset="460"/><circle cx="470" cy="960" r="9" fill="#fff" opacity="0"/></svg>')
fj.append('tl.set("#ptr5", { opacity: 1 }, 10.0);')
fj.append('tl.fromTo("#ptr5 path", { attr: { "stroke-dashoffset": 460 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out" }, 10.0);')
fj.append('tl.to("#ptr5 circle", { opacity: 1, duration: 0.15 }, 10.45);')
fj.append('tl.to("#ptr5", { opacity: 0, duration: 0.25 }, 11.15);')
# USB-C badge
fx_html.append('<div id="usb5" class="badge" style="left:640px;top:1070px">'
               '<svg width="64" height="30" viewBox="0 0 64 30"><rect x="3" y="3" width="58" height="24" rx="12" fill="none" stroke="#fff" stroke-width="4"/>'
               '<rect x="16" y="12" width="32" height="6" rx="3" fill="#fff"/></svg><span>USB-C</span></div>')
fj.append('tl.fromTo("#usb5", { opacity: 0, scale: 0.4, x: -30 }, { opacity: 1, scale: 1, x: 0, duration: 0.45, ease: "back.out(2.2)" }, 10.45);')
fj.append('tl.to("#usb5", { y: -90, duration: 0.8, ease: "sine.inOut" }, 10.5);')
fj.append('tl.to("#usb5", { opacity: 0, duration: 0.2 }, 11.25);')
# scene 7 note: power comes from the connected device
fx_html.append(words("n7", "Guna kuasa dari device USB-C", "note", 590, 36, CREAM, "b"))
show("#n7", 11.55)
reveal("#n7", 11.55, 0.04)
fx_html.append('<svg id="bolt7" class="arc" style="left:505px;top:1190px" width="70" height="70" viewBox="0 0 24 24">'
               f'<path d="M13 2 L4 14 H11 L10 22 L20 9 H13 Z" fill="{PINK}"/></svg>')
fj.append('tl.fromTo("#bolt7", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, 11.75);')
fj.append('tl.to("#bolt7", { scale: 1.15, duration: 0.3, yoyo: true, repeat: 2, ease: "sine.inOut" }, 12.15);')
fj.append('tl.to("#bolt7", { opacity: 0, duration: 0.2 }, 12.7);')
out("#n7", 12.9)
out("#g5", 12.9)

# ---- scene 8+9: wind levels (12.9 - 16.5)
fx_html.append('<div id="g6" class="grp">')
fx_html.append(words("g6a", "3 WIND LEVELS", "", 400, 74))
fx_html.append(f'<div id="g6b" class="line sub f-b" style="top:494px;font-size:40px">'
               f'<span id="lv1" class="lv">Soft</span><span class="dot">•</span><span id="lv2" class="lv">Comfortable</span>'
               f'<span class="dot">•</span><span id="lv3" class="lv">Turbo</span></div>')
fx_html.append('</div>')
show("#g6", 12.95)
reveal("#g6a", 12.95, 0.08)
fj.append('tl.fromTo("#g6b", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 13.15);')
# level meter
bars = []
for i, h in enumerate((44, 76, 108)):
    bars.append(f'<div id="bar{i + 1}" class="bar" style="left:{i * 46}px;height:{h}px"></div>')
fx_html.append(f'<div id="meter" class="meter" style="left:{540 - 66}px;top:600px">{"".join(bars)}</div>')
fj.append('tl.fromTo("#meter", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 13.1);')
for i, t in enumerate((13.25, 13.85, 14.45), 1):
    fj.append(f'tl.fromTo("#bar{i}", {{ scaleY: 0, background: "rgba(255,255,255,0.35)" }}, {{ scaleY: 1, background: "{PINK}", duration: 0.35, ease: "back.out(2)" }}, {t});')
    fj.append(f'tl.to("#lv{i}", {{ color: "{PINK}", scale: 1.12, duration: 0.2 }}, {t});')
    if i < 3:
        fj.append(f'tl.to("#lv{i}", {{ color: "#fff", scale: 1, duration: 0.2 }}, {t + 0.6:.3f});')
fj.append('tl.fromTo("#meter", { scale: 1 }, { scale: 1.18, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 14.45);')
# airflow: ripples + waves from the fan front (scene 8), streams toward the tissue (scene 9)
for k in range(3):
    fx_html.append(f'<div id="rip{k}" class="pulse air" style="left:{560 - 150}px;top:{1180 - 150}px;width:300px;height:300px"></div>')
    fj.append(f'tl.fromTo("#rip{k}", {{ opacity: 0.8, scale: 0.5 }}, {{ opacity: 0, scale: 2.2, duration: 0.9, ease: "power1.out", immediateRender: false }}, {13.3 + k * 0.35:.2f});')
waves = []
for k, (y0, amp) in enumerate(((-90, 26), (0, 32), (90, 26))):
    waves.append(f'<path class="wv" d="M 0 {200 + y0} Q 60 {200 + y0 - amp} 120 {200 + y0} T 240 {200 + y0} T 360 {200 + y0}" '
                 f'fill="none" stroke="{AIR}" stroke-opacity="0.75" stroke-width="7" stroke-linecap="round" stroke-dasharray="70 40"/>')
fx_html.append(f'<svg id="wav8L" class="arc" style="left:20px;top:980px" width="360" height="400" viewBox="0 0 360 400">{"".join(waves)}</svg>')
fx_html.append(f'<svg id="wav8R" class="arc" style="left:740px;top:980px;transform:scaleX(-1)" width="360" height="400" viewBox="0 0 360 400">{"".join(waves)}</svg>')
for sid in ("wav8L", "wav8R"):
    fj.append(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 13.5);')
    fj.append(f'tl.fromTo("#{sid} .wv", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": 440 }}, duration: 1.4, ease: "none" }}, 13.5);')
    fj.append(f'tl.to("#{sid}", {{ opacity: 0, duration: 0.25 }}, 14.65);')
fx_html.append(f'<svg id="wav9" class="arc" style="left:330px;top:640px;transform:scaleX(-1)" width="480" height="520" viewBox="0 0 360 400">{"".join(waves)}</svg>')
fj.append('tl.fromTo("#wav9", { opacity: 0 }, { opacity: 0.9, duration: 0.3 }, 15.0);')
fj.append('tl.fromTo("#wav9 .wv", { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": 660 }, duration: 1.5, ease: "none" }, 15.0);')
fj.append('tl.to("#wav9", { opacity: 0, duration: 0.25 }, 16.2);')
fj.append('tl.to("#meter", { opacity: 0, duration: 0.25 }, 16.25);')
out("#g6", 16.5)

# ---- scene 10+11: compact (16.5 - 19.5)
fx_html.append('<div id="g7" class="grp">')
fx_html.append(words("g7a", "SMALL BUT USEFUL ♡", "", 640, 70))
fx_html.append(f'<div id="g7b" class="chip f-b" style="top:740px">Lightweight • Compact</div>')
fx_html.append('</div>')
show("#g7", 16.6)
reveal("#g7a", 16.6, 0.08)
fj.append('tl.fromTo("#g7b", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 16.95);')
fx_html.append('<svg id="cv10" class="arc" style="left:250px;top:1000px" width="580" height="560" viewBox="0 0 580 560">'
               '<path d="M 40 380 C 30 150 250 40 420 110" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" '
               'stroke-dasharray="560" stroke-dashoffset="560"/><path d="M 400 90 L 430 112 L 398 132" fill="none" stroke="#fff" '
               'stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>')
fj.append('tl.set("#cv10", { opacity: 1 }, 17.05);')
fj.append('tl.fromTo("#cv10 path:first-child", { attr: { "stroke-dashoffset": 560 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.7, ease: "power2.inOut" }, 17.05);')
fj.append('tl.to("#cv10 path:last-child", { opacity: 1, duration: 0.15 }, 17.7);')
fj.append('tl.to("#cv10", { opacity: 0, duration: 0.3 }, 18.1);')
sparkle("s10", 860, 700, 30, 17.3)
fj.append('tl.to("#g7", { y: -40, duration: 0.9, ease: "sine.inOut" }, 18.3);')
out("#g7", 19.5)

# ---- scene 12+13: hero + CTA (19.5 - 22.7)
fx_html.append('<div id="g8" class="grp">')
fx_html.append(f'<div id="g8a" class="line f-h" style="top:860px;font-size:68px">'
               f'<span id="k1" class="w">KECIL.</span> <span id="k2" class="w" style="color:{PINK}">COMEL.</span></div>')
fx_html.append(f'<div id="g8b" class="line f-h" style="top:946px;font-size:68px"><span id="k3" class="w">PRAKTIKAL. 🤍</span></div>')
fx_html.append('</div>')
show("#g8", 19.6)
for i, t in enumerate((19.75, 20.1, 20.45), 1):
    fj.append(f'tl.fromTo("#k{i}", {{ opacity: 0, y: 40, scale: 1.3, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "back.out(2)" }}, {t});')
underline("u8", 1042, 260, 20.75, CREAM)
# move the hero line up out of the way for the last shot, then the CTA lands under it
fj.append('tl.to(["#g8", "#u8"], { y: -470, duration: 0.6, ease: "power3.inOut" }, 21.05);')
sparkle("s8a", 820, 400, 32, 21.75)
sparkle("s8b", 270, 470, 24, 21.95)

fx = f'''<template>
  <style>
    @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-800.woff2") format("woff2"); font-weight: 600 800; }}
    @font-face {{ font-family: "DM Sans"; src: url("assets/fonts/DMSans-500.woff2") format("woff2"); font-weight: 500; }}
    #root {{ position: absolute; inset: 0; color: #fff; }}
    #root .grp {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; opacity: 0; }}
    #root .line {{
      position: absolute; left: {X0}px; width: {TW}px; text-align: center; white-space: nowrap; line-height: 1.12;
      text-shadow: 0 3px 14px rgba(20,14,16,0.75), 0 1px 2px rgba(20,14,16,0.9);
    }}
    #root > .line {{ opacity: 0; }}
    #root .f-h {{ font-family: "Manrope", sans-serif; font-weight: 800; letter-spacing: -0.01em; }}
    #root .f-b {{ font-family: "DM Sans", sans-serif; font-weight: 500; }}
    #root .w {{ display: inline-block; }}
    #root .brand {{ letter-spacing: 0.16em; }}
    #root .uline {{ position: absolute; height: 7px; border-radius: 4px; transform: scaleX(0); transform-origin: 0% 50%; box-shadow: 0 2px 10px rgba(0,0,0,0.35); }}
    #root .ring, #root .arc, #root .spark {{ position: absolute; opacity: 0; overflow: visible; }}
    #root .ring svg {{ filter: drop-shadow(0 2px 8px rgba(0,0,0,0.45)); overflow: visible; }}
    #root .pulse {{ position: absolute; border-radius: 50%; border: 4px solid #fff; opacity: 0; }}
    #root .pulse.air {{ border-color: {AIR}; border-width: 5px; }}
    #root .badge {{
      position: absolute; display: flex; align-items: center; gap: 12px; opacity: 0;
      padding: 12px 22px; border-radius: 999px; background: rgba(20,14,16,0.55); border: 2px solid rgba(255,255,255,0.7);
      font-family: "DM Sans", sans-serif; font-weight: 500; font-size: 34px;
    }}
    #root .lv {{ display: inline-block; padding: 0 10px; }}
    #root .dot {{ color: rgba(255,255,255,0.6); }}
    #root .meter {{ position: absolute; width: 132px; height: 108px; opacity: 0; }}
    #root .bar {{ position: absolute; bottom: 0; width: 34px; border-radius: 10px; transform-origin: 50% 100%; box-shadow: 0 2px 10px rgba(0,0,0,0.35); }}
    #root .chip {{
      position: absolute; left: {540 - 220}px; width: 440px; text-align: center; padding: 12px 0; border-radius: 999px;
      background: rgba(244,183,206,0.92); color: #3a2630; font-size: 38px; opacity: 0;
    }}
    #root .cta {{
      position: absolute; left: {540 - 330}px; width: 660px; text-align: center; padding: 22px 0; border-radius: 999px;
      background: {CREAM}; color: #3a2630; font-size: 44px; opacity: 0; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
  </style>
  <div id="root" data-composition-id="fx" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
    {(chr(10) + "    ").join(fx_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(fj)}
    window.__timelines["fx"] = tl;
  </script>
</template>
'''
os.makedirs(os.path.join(PROJ, "compositions"), exist_ok=True)
open(os.path.join(PROJ, "compositions/fx.html"), "w").write(fx)
print("written index.html and compositions/fx.html")
