#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman
"PAKEJ BINA RUMAH BERSERTA TANAH" promo (1080x1920).

Talent takes play back to back with their own sound; B-roll sits on top, muted.
Every graphic is timed in clip-local seconds (word times from a whisper pass on
each take) and converted to film time here.

Safe zone: every graphic lives inside Y 320-1520 with >= 100 px side margins,
including while it animates in or out (only fades, small vertical moves and
scales are used, all of which stay inside the box).
"""
import json

YEL, WHT, CHR = "#FFD400", "#FFFFFF", "#171717"
SAFE_TOP, SAFE_BOT, SIDE = 320, 1520, 100

# (id, file, in, out, volume) — talent takes in script order
SEGS = [
    ("hook", "t9933", 0.30, 8.55, 1.0),
    ("loc", "t9934", 0.40, 7.00, 1.0),
    ("size", "t9936", 0.20, 9.83, 1.0),
    ("custom", "t9937", 0.25, 7.15, 1.0),
    ("area", "t9939a", 0.00, 5.00, 1.0),
    ("flood", "t9939b", 0.20, 4.20, 1.0),
    ("road", "t9941", 0.45, 5.35, 1.2),
    ("near", "t9944", 0.10, 3.78, 1.0),
    ("places", "t-drive", 0.15, 13.45, 1.0),
    ("cta", "t9945", 0.25, 6.27, 1.0),
]
start = {}
t = 0.0
for sid, f, a, b, _ in SEGS:
    start[sid] = round(t, 3)
    t += b - a
TOTAL = round(t, 3)   # no outro: the film ends with the last line of dialogue


def T(sid, local):
    """clip-local time (seconds into the source file) -> film time"""
    a = [s for s in SEGS if s[0] == sid][0][2]
    return round(start[sid] + local - a, 3)


# B-roll cutaways: (id, file, film start, film end, media start, push-in?)
BROLL = [
    ("b-drone1", "drone-a", T("hook", 5.70), T("hook", 8.55), 0.5, True),
    ("b-drone0", "drone-b", T("loc", 4.75), T("loc", 7.00), 3.5, True),
    ("b-lots", "lot-tersedia", T("size", 1.00), T("size", 5.30), 0.7, False),  # lot labels near edges: no crop
    ("b-drone2", "drone-a", T("area", 1.00), T("area", 3.40), 8.0, True),
    ("b-road", "road", T("road", 2.55), T("road", 5.35), 0.8, True),
    # location map: shown whole and uncropped (its own cards are the overlay)
    ("b-map", "map-lokasi", T("places", 1.40), T("places", 8.90), 0.0, False),
]

# ---------- index.html ----------
vids = []
for sid, f, a, b, vol in SEGS:
    vids.append(
        f'      <div id="w-{sid}" style="position:absolute; inset:0; z-index:1; overflow:hidden; transform-origin: 50% 46%">'
        f'<video id="v-{sid}" class="clip" src="assets/video/{f}.mp4" data-start="{start[sid]}" '
        f'data-duration="{round(b - a, 3)}" data-media-start="{a}" data-track-index="1" playsinline '
        f'data-has-audio="true" data-volume="{vol}" data-fade-in="0.04" data-fade-out="0.06" '
        f'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video></div>'
    )
for bid, f, s, e, m, _ in BROLL:
    vids.append(
        f'      <div id="{bid}-w" style="position:absolute; inset:0; z-index:2; overflow:hidden">'
        f'<video id="{bid}" src="assets/video/{f}.mp4" data-start="{s}" data-duration="{round(e - s, 3)}" '
        f'data-media-start="{m}" data-track-index="2" class="clip" muted playsinline '
        f'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:contain"></video></div>'
    )

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{TOTAL}" '
       f'data-track-index="4" data-volume="0.10" data-fade-out="1.2"></audio>']


def sfx(name, file, at, dur, vol):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{file}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{dur}" data-track-index="{5 + len(AUD) % 3}" data-volume="{vol}"></audio>')


# hook
sfx("hook", "whoosh-short", T("hook", 0.40), 0.57, 0.12)
sfx("hk2", "pop", T("hook", 1.22), 0.72, 0.10)
sfx("tanah", "impact-bass-1", T("hook", 2.38), 1.6, 0.16)
# package
sfx("kick", "whoosh-short", T("hook", 4.15), 0.57, 0.10)
sfx("kk2", "click-soft", T("hook", 4.45), 0.36, 0.12)
sfx("title", "whoosh", T("hook", 5.70), 0.57, 0.14)
sfx("pk1", "impact-bass-2", T("hook", 5.95) - 0.35, 1.8, 0.14)
sfx("pk2", "pop", T("hook", 6.95), 0.72, 0.12)
sfx("pk3", "click-soft", T("hook", 7.60), 0.36, 0.12)
# location
sfx("loccut", "whoosh-short", T("loc", 4.73), 0.57, 0.12)
sfx("locpin", "pop", T("loc", 4.95), 0.72, 0.12)
sfx("locping", "ping", T("loc", 5.45), 1.0, 0.08)
# land + house size
sfx("lotcut", "whoosh-short", T("size", 0.98), 0.57, 0.11)
sfx("land", "pop", T("size", 2.55), 0.72, 0.12)
sfx("landn", "ping", T("size", 3.20), 1.0, 0.08)
sfx("house", "pop", T("size", 6.15), 0.72, 0.12)
sfx("housen", "ping", T("size", 7.85), 1.0, 0.08)
# custom design
sfx("renders", "whoosh", T("custom", 4.00), 0.57, 0.13)
sfx("cu1", "pop", T("custom", 4.08), 0.72, 0.11)
sfx("rc2", "whoosh-short", T("custom", 4.98), 0.57, 0.09)
sfx("cu2", "click-soft", T("custom", 5.30), 0.36, 0.12)
sfx("rc3", "whoosh-short", T("custom", 5.96), 0.57, 0.09)
# neighbourhood / flood / road
sfx("nbcut", "whoosh-short", T("area", 0.98), 0.57, 0.11)
sfx("nb", "pop", T("area", 2.05), 0.72, 0.11)
sfx("flood", "chime", T("flood", 2.85), 1.6, 0.10)
sfx("roadcut", "whoosh-short", T("road", 2.53), 0.57, 0.11)
sfx("road", "pop", T("road", 3.38), 0.72, 0.12)
# facilities checklist
sfx("nh", "whoosh-short", T("near", 1.80), 0.57, 0.10)
for i in range(4):
    sfx(f"li{i}", "click-soft", T("near", 2.30) + i * 0.28, 0.36, 0.13)
    sfx(f"tk{i}", "click", T("near", 2.48) + i * 0.28, 0.36, 0.07)
# location map: one pop per card as it appears in the map clip (3.5 / 4.4 / 5.3 s)
sfx("map", "whoosh-short", T("places", 1.38), 0.57, 0.10)
sfx("mapzoom", "whoosh", T("places", 3.65), 0.57, 0.09)
for i, m in enumerate([3.5, 4.4, 5.3]):
    sfx(f"mc{i}", "pop", T("places", 1.40 + m), 0.72, 0.11)
sfx("kanan", "whoosh-short", T("places", 8.92), 0.57, 0.10)
sfx("kanan2", "pop", T("places", 8.98), 0.72, 0.10)
sfx("kiri", "pop", T("places", 10.30), 0.72, 0.11)
sfx("uitm", "ping", T("places", 11.76), 1.0, 0.07)
# call to action
sfx("lot", "impact-bass-1", T("cta", 0.30), 1.5, 0.16)
sfx("siapa", "pop", T("cta", 1.23), 0.72, 0.11)
sfx("berminat", "whoosh-short", T("cta", 3.06), 0.57, 0.10)
sfx("ctapop", "pop", T("cta", 4.20), 0.72, 0.13)
sfx("tap1", "click", T("cta", 4.85), 0.36, 0.14)
sfx("tap2", "click", T("cta", 5.45), 0.36, 0.14)

push = [(b[0], b[2], b[3]) for b in BROLL if b[5]]
# quick punch-in on the talent at the key words, then ease back (scaled on the wrapper)
PUNCH = [("hook", T("hook", 2.38), 0.95), ("size", T("size", 7.20), 1.1), ("flood", T("flood", 2.85), 1.1),
         ("road", T("road", 2.40), 0.0), ("near", T("near", 2.30), 1.2), ("cta", T("cta", 0.30), 0.95), ("cta", T("cta", 4.20), 1.6)]
PUNCH = [p for p in PUNCH if p[2] > 0]
fades = [(b[0], b[2]) for b in BROLL]
index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {CHR}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {CHR}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // B-roll: quick dissolve in; drone shots also get a slow push
      {json.dumps(fades)}.forEach(([id, s]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18, ease: "power1.out" }}, s);
      }});
      {json.dumps(push)}.forEach(([id, s, e]) => {{
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.06, duration: e - s, ease: "none" }}, s);
      }});
      // punch-ins: snap closer on the key word, settle back
      {json.dumps(PUNCH)}.forEach(([id, s, h]) => {{
        tl.fromTo("#w-" + id, {{ scale: 1 }}, {{ scale: 1.1, duration: 0.28, ease: "power3.out" }}, s);
        tl.fromTo("#w-" + id, {{ scale: 1.1 }}, {{ scale: 1, duration: 0.45, ease: "power2.inOut", immediateRender: false }}, s + h);
      }});
      // drone / road cutaways enter with a short zoom settle
      {json.dumps(push)}.forEach(([id, s]) => {{
        tl.fromTo("#" + id + "-w", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, s);
      }});
      // talent takes: a gentle push-in so cuts feel like camera moves
      {json.dumps([(s[0], start[s[0]], round(s[3] - s[2], 3)) for s in SEGS])}.forEach(([id, s, d]) => {{
        tl.fromTo("#v-" + id, {{ scale: 1.0 }}, {{ scale: 1.04, duration: d, ease: "none" }}, s);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------- gfx.html ----------
def svg(body, size=56, stroke=CHR, sw=3.6, fill="none"):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


HAND = f'<svg viewBox="0 0 64 72" width="78" height="88"><path d="M22 6c0-3 2-5 5-5s5 2 5 5v24l3-1c3-1 6 1 6 4l8-2c3 0 5 2 5 5v14c0 10-7 20-19 20h-6c-7 0-11-3-14-8L4 44c-2-3-1-6 2-7 2-1 5 0 6 2l10 10z" fill="{WHT}" stroke="{CHR}" stroke-width="3.5" stroke-linejoin="round"/></svg>'
TICK = f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="{CHR}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5 10 17 19 7"/></svg>'
ICON = {
    "pin": f'<svg viewBox="0 0 48 64" width="44" height="58"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{CHR}"/></svg>',
    "hospital": svg('<rect x="7" y="7" width="34" height="34" rx="6"/><path d="M24 15v18M15 24h18"/>'),
    "mart": svg('<path d="M5 9h6l5 22h21l4-15H14"/><circle cx="19" cy="39" r="3"/><circle cx="34" cy="39" r="3"/>'),
    "mosque": svg('<path d="M12 42V26c0-7 12-10 12-17 0 7 12 10 12 17v16z"/><path d="M5 42V20M43 42V20M5 20v-5M43 20v-5"/><path d="M20 42v-8a4 4 0 0 1 8 0v8M2 42h44"/>', sw=3.4),
    "school": svg('<path d="M3 18 24 8l21 10-21 10z"/><path d="M11 22v11c4 4 22 4 26 0V22"/><path d="M45 18v12"/>'),
    "road": svg('<path d="M16 4 6 44M32 4l10 40"/><path d="M24 8v6M24 21v6M24 34v6"/>', 68),
    "lot": svg('<path d="M4 32 24 22l20 10-20 10z"/><path d="M24 22V6"/><path d="M24 6l12 4-12 4" fill="#171717"/>', 68),
    "house": svg('<path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M20 43V31h8v12"/>', 68),
    "shield": svg('<path d="M24 4 7 10v12c0 11 7.5 18.5 17 22 9.5-3.5 17-11 17-22V10z"/><path d="M16 24l6 6 10-11"/>', 68),
    "homes": svg('<path d="M2 26 14 16l12 10"/><path d="M5 24v18h18V24"/><path d="M22 20 34 10l12 10"/><path d="M26 18v24h17V18"/>', 68),
}

H = []   # markup
J = []   # timeline js
BOXES = []  # (id, top, height) for the safe-zone self check


def tin(sel, at, kind="up", d=0.45):
    frm = {"up": "{ opacity: 0, y: 28 }", "scale": "{ opacity: 0, scale: 0.86 }",
           "fade": "{ opacity: 0 }", "down": "{ opacity: 0, y: -20 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "expo.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def tout(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, y: -16, duration: 0.22, ease: "power2.in" }}, {round(at, 3)});')


def block(bid, s, e, inner, top, height, cls=""):
    """A timed group pinned to the safe box. `height` is the reserved height, checked against the box."""
    BOXES.append((bid, top, height))
    H.append(f'    <div class="grp clip {cls}" id="{bid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" '
             f'style="top:{top}px; height:{height}px">{inner}</div>')


def wipe(sel, at):
    """yellow highlight bar wiping in behind a word"""
    J.append(f'tl.fromTo("{sel}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power3.out" }}, {round(at, 3)});')


# SCENE 1 — hook: words land as he says them
s, e = T("hook", 0.40), T("hook", 4.10)
block("g-hook", s, e, '''<div class="lbl dk xl" id="hk1"><span class="hw" id="hw1">NAK</span> <span class="hw" id="hw2">BINA</span> <span class="hw" id="hw3">RUMAH</span></div>
      <div class="lbl dk xl" id="hk2"><span class="hw" id="hw4">TAPI</span> <span class="hw" id="hw5">TAK ADA</span></div>
      <div class="lbl yl xxl" id="hk3"><span class="hw" id="hw6">TANAH?</span></div>''', 370, 380, "col")
tin("#hk1", T("hook", 0.42), "scale", 0.35)
hide("#hk2"); tin("#hk2", T("hook", 1.22), "scale", 0.35)
hide("#hk3"); tin("#hk3", T("hook", 2.38), "scale", 0.4)
for i, at in enumerate([0.45, 0.62, 0.90, 1.25, 1.62, 2.40]):
    J.append(f'tl.fromTo("#hw{i + 1}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }}, {T("hook", at)});')
tout("#g-hook", e - 0.22)

# SCENE 2 — introduce the package
s, e = T("hook", 4.15), T("hook", 5.72)
block("g-kick", s, e, f'''<div class="lbl dk md" id="kk">MAHLIGAI IDAMAN</div><div class="lbl wh sm" id="kk2">MENYEDIAKAN</div>''', 390, 200, "col")
tin("#kk", s, "up")
tin("#kk2", T("hook", 4.45), "up", 0.35)
tout("#g-kick", e - 0.12)

s, e = T("hook", 5.75), T("hook", 8.55)
block("g-pkg", s, e, '''<div class="lbl yl lg" id="pk1">PAKEJ BINA RUMAH</div>
      <div class="lbl dk lg" id="pk2"><span class="y">BERSERTA</span> TANAH</div>
      <div class="lbl wh sm" id="pk3">MAHLIGAI IDAMAN</div>''', 400, 400, "col")
tin("#pk1", T("hook", 5.95), "scale")
hide("#pk2"); tin("#pk2", T("hook", 6.95), "scale")
hide("#pk3"); tin("#pk3", T("hook", 7.60), "up", 0.35)
tout("#g-pkg", e - 0.2)

# SCENE 3 — location (over drone footage of the land)
s, e = T("loc", 4.95), T("loc", 7.00)
block("g-loc", s, e, f'''<div class="chip" id="lc"><div class="pin" id="lc-pin"><div class="ripple" id="lc-rip"></div>{ICON["pin"]}</div><div><div class="ck">LOKASI TANAH</div><div class="cv">KAMPUNG WEK, MACHANG</div></div></div>''', 400, 170, "col")
tin("#lc", s, "scale")
J.append(f'tl.fromTo("#lc-pin", {{ y: -26 }}, {{ y: 0, duration: 0.55, ease: "bounce.out" }}, {T("loc", 5.0)});')
J.append(f'tl.fromTo("#lc-rip", {{ scale: 0.2, opacity: 0.9 }}, {{ scale: 1.6, opacity: 0, duration: 0.9, ease: "power2.out", repeat: 1, immediateRender: false }}, {T("loc", 5.3)});')
tout("#g-loc", e - 0.22)

# SCENE 4 — land size (over the lot plan, low in the safe box so the lot labels stay clear)
s, e = T("size", 2.55), T("size", 5.30)
block("g-land", s, e, f'''<div class="stat dkc" id="ld"><div class="si">{ICON["lot"]}</div><div><div class="sk">KELUASAN LOT BERMULA</div>
      <div class="sv"><span class="y" id="n-land">5,101</span> <small>KPS</small></div></div></div>''', 1300, 200, "col")
tin("#ld", s, "up")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 5101, duration: 0.7, ease: "power3.out", onUpdate: () => {{ document.querySelector("#n-land").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {s}); }})();')
tout("#g-land", e - 0.22)

# SCENE 5 — house size
s, e = T("size", 6.15), T("size", 9.83)
block("g-house", s, e, f'''<div class="stat" id="hs"><div class="si">{ICON["house"]}</div><div><div class="sk">BINA RUMAH BERMULA</div>
      <div class="sv"><span id="n-house">1,400</span> <small>KPS KE ATAS</small></div></div></div>''', 390, 200, "col")
tin("#hs", s, "up")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 1400, duration: 0.7, ease: "power3.out", onUpdate: () => {{ document.querySelector("#n-house").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {T("size", 7.2)}); }})();')
tout("#g-house", e - 0.22)

# SCENE 6 — custom design: the house designs as framed cards
s, e = T("custom", 4.00), T("custom", 7.15)
imgs = ["house-a", "house-b", "house-c"]
H.append(f'''    <div class="clip" id="g-renders" data-start="{s}" data-duration="{round(e - s, 3)}" style="position:absolute; inset:0">
''' + "".join(f'      <div class="rbg" id="rb{i + 1}"><img src="assets/img/{n}.jpg" alt="" /></div>\n' for i, n in enumerate(imgs)) + '''      <div class="rdim"></div>
''' + "".join(f'      <div class="rcard" id="rc{i + 1}"><img src="assets/img/{n}.jpg" alt="" /></div>\n' for i, n in enumerate(imgs)) + '''    </div>''')
BOXES.append(("rcard", 560, 660))
block("g-cust-h", s, e, '<div class="lbl yl lg" id="cu1">CUSTOM DESIGN</div>', 380, 130, "col")
block("g-cust-s", s, e, '<div class="lbl dk md" id="cu2">IKUT CITA RASA <span class="y">ANDA</span></div>', 1270, 110, "col")
J.append(f'tl.fromTo("#g-renders", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.22, ease: "power1.out" }}, {s});')
step = (e - s - 0.2) / 3
for i in range(3):
    a = round(s + i * step, 3)
    J.append(f'tl.fromTo(["#rc{i + 1}", "#rb{i + 1}"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {a});')
    J.append(f'tl.fromTo("#rc{i + 1}", {{ scale: 0.94 }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, {a});')
    J.append(f'tl.fromTo("#rc{i + 1} img", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {round(step + 0.3, 3)}, ease: "none" }}, {a});')
    if i < 2:
        J.append(f'tl.to(["#rc{i + 1}", "#rb{i + 1}"], {{ opacity: 0, duration: 0.3, ease: "power1.in" }}, {round(a + step, 3)});')
tin("#cu1", T("custom", 4.08), "scale")
hide("#cu2"); tin("#cu2", T("custom", 5.30), "up")
for g in ("#g-renders", "#g-cust-h", "#g-cust-s"):
    tout(g, e - 0.2)

# SCENE 7 — existing neighbourhood
s, e = T("area", 2.05), T("area", 5.00)
block("g-nb", s, e, f'''<div class="card" id="nb"><div class="si">{ICON["homes"]}</div><div><div class="sk">KEJIRANAN</div><div class="cv2">BANGLO <span class="y">SEDIA ADA</span></div></div></div>''', 390, 190, "col")
tin("#nb", s, "up")
tout("#g-nb", e - 0.22)

# SCENE 8 — flood free
s, e = T("flood", 2.85), T("flood", 4.20)
block("g-flood", s, e, f'''<div class="card wcard" id="fl"><div class="si">{ICON["shield"]}</div><div><div class="sk">KAWASAN</div><div class="cv2">BEBAS BANJIR</div></div></div>''', 390, 190, "col")
tin("#fl", s, "scale")
tout("#g-flood", e - 0.2)

# SCENE 9 — tar road access
s, e = T("road", 3.38), T("road", 5.35)
block("g-road", s, e, f'''<div class="card" id="rd"><div class="si">{ICON["road"]}</div><div><div class="sk">AKSES</div><div class="cv2"><span class="y">JALAN TAR</span> TERSEDIA</div></div></div>''', 390, 190, "col")
tin("#rd", s, "up")
tout("#g-road", e - 0.2)

# SCENE 10 — nearby facilities (held until the map)
s, e = T("near", 1.80), T("places", 1.40)
items = [("hospital", "HOSPITAL"), ("mart", "PASARAYA"), ("mosque", "MASJID"), ("school", "SEKOLAH")]
grid = "".join(f'<div class="am" id="am{i}"><div class="ai">{ICON[k]}</div><span>{n}</span><div class="tick" id="tk{i}">{TICK}</div></div>' for i, (k, n) in enumerate(items))
block("g-near", s, e, f'''<div class="lbl yl md" id="nh">KEMUDAHAN BERDEKATAN</div><div class="grid">{grid}</div>''', 360, 360, "col")
tin("#nh", s, "up")
for i in range(4):
    hide(f"#am{i}")
    tin(f"#am{i}", T("near", 2.30) + i * 0.28, "scale", 0.4)
    J.append(f'tl.fromTo("#tk{i}", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.4)" }}, {round(T("near", 2.48) + i * 0.28, 3)});')
tout("#g-near", e - 0.18)

# SCENE 11 — landmarks: the location map carries SMK Hamzah 2 (and all three cards) uncropped;
# back on Abe, the two directions he points to
s, e = T("places", 8.90), T("places", 13.45)
plc = [("kiri", '<span class="ar" id="ar-kiri">◀</span> KE KIRI', "UiTM MACHANG", "6 KM | 10 MINIT"), ("kanan", 'KE KANAN <span class="ar" id="ar-kanan">▶</span>', "BANDAR MACHANG", "6 KM | 10 MINIT")]
cards = "".join(f'<div class="dir" id="d-{k}"><div class="dk2">{a}</div><div class="dn">{n}</div><div class="dd">{d}</div></div>' for k, a, n, d in plc)
block("g-dir", s, e, f'<div class="dirs">{cards}</div>', 380, 200, "col")
tin("#d-kanan", s + 0.05, "up")
hide("#d-kiri"); tin("#d-kiri", T("places", 10.30), "up")
J.append(f'tl.fromTo("#d-kiri .dn", {{ color: "{WHT}" }}, {{ color: "{YEL}", duration: 0.25 }}, {T("places", 11.76)});')
J.append(f'tl.fromTo("#ar-kanan", {{ x: 0 }}, {{ x: 10, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {round(s + 0.4, 3)});')
J.append(f'tl.fromTo("#ar-kiri", {{ x: 0 }}, {{ x: -10, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {T("places", 10.6)});')
tout("#g-dir", e - 0.2)

# SCENE 12 — call to action (no outro after the last line)
s, e = T("cta", 0.28), T("cta", 3.05)
block("g-lot", s, e, '''<div class="lbl yl xxl" id="lt">LOT TERHAD!</div><div class="lbl dk md" id="lt-s">SIAPA CEPAT, <span class="y">DIA DAPAT</span></div>''', 380, 280, "col")
tin("#lt", s, "scale")
hide("#lt-s"); tin("#lt-s", T("cta", 1.23), "up")
tout("#g-lot", e - 0.18)

s, e = T("cta", 3.08), TOTAL
block("g-cta", s, e, f'''<div class="lbl dk lg" id="ct-k">BERMINAT?</div><div class="btnw"><div class="lbl yl lg" id="ct-b">PM KAMI SEGERA</div>
      <div class="tapr" id="tap-r"></div><div class="hand" id="hand">{HAND}</div></div>''', 380, 300, "col")
tin("#ct-k", s, "up")
hide("#ct-b"); tin("#ct-b", T("cta", 4.20), "scale")
hide("#hand")
J.append(f'tl.fromTo("#hand", {{ opacity: 0, x: 60, y: 50 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.4, ease: "power3.out" }}, {T("cta", 4.45)});')
for k, at in enumerate([4.85, 5.45]):
    J.append(f'tl.fromTo("#hand", {{ scale: 1 }}, {{ scale: 0.86, duration: 0.1, ease: "power2.in", yoyo: true, repeat: 1 }}, {T("cta", at)});')
    J.append(f'tl.fromTo("#ct-b", {{ scale: 1 }}, {{ scale: 0.95, duration: 0.1, ease: "power2.in", yoyo: true, repeat: 1 }}, {T("cta", at)});')
    J.append(f'tl.fromTo("#tap-r", {{ scale: 0.2, opacity: 0.9 }}, {{ scale: 1.5, opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }}, {T("cta", at + 0.1)});')

# safe-zone self check on reserved boxes (scale-in from 0.86 stays inside its box)
for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: {SIDE}px; right: {SIDE}px; }}
    .col {{ display: flex; flex-direction: column; align-items: center; gap: 14px; }}
    .y {{ color: {YEL}; }}
    .lbl {{ font-weight: 900; line-height: 1; white-space: nowrap; border-radius: 10px; letter-spacing: .01em;
      box-shadow: 0 14px 34px rgba(0,0,0,.35); max-width: 880px; }}
    .lbl.dk {{ background: rgba(23,23,23,.9); color: {WHT}; }}
    .lbl.yl {{ background: {YEL}; color: {CHR}; }}
    .lbl.wh {{ background: {WHT}; color: {CHR}; }}
    .lbl.sm {{ font-size: 34px; letter-spacing: .14em; padding: 14px 26px 15px; }}
    .lbl.md {{ font-size: 46px; padding: 18px 32px 19px; }}
    .lbl.lg {{ font-size: 66px; padding: 22px 36px 23px; }}
    .lbl.xl {{ font-size: 76px; padding: 20px 36px 21px; }}
    .lbl.xxl {{ font-size: 104px; padding: 22px 44px 24px; }}
    .hw {{ display: inline-block; opacity: 0; }}
    .chip {{ display: flex; align-items: center; gap: 20px; padding: 22px 36px 24px 28px; border-radius: 12px;
      background: rgba(23,23,23,.9); border-left: 10px solid {YEL}; box-shadow: 0 16px 40px rgba(0,0,0,.4); }}
    .pin {{ flex: none; }}
    .ck {{ font-weight: 800; font-size: 28px; letter-spacing: .2em; color: {YEL}; }}
    .cv {{ font-weight: 900; font-size: 50px; letter-spacing: .01em; white-space: nowrap; margin-top: 6px; }}
    .stat, .card {{ display: flex; align-items: center; gap: 26px; padding: 24px 40px 26px 26px; border-radius: 14px; background: {WHT};
      color: {CHR}; box-shadow: 0 18px 44px rgba(0,0,0,.38); max-width: 880px; }}
    .stat.dkc, .card {{ background: rgba(23,23,23,.92); color: {WHT}; }}
    .card.wcard {{ background: {WHT}; color: {CHR}; }}
    .si {{ width: 110px; height: 110px; border-radius: 12px; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; }}
    .sk {{ font-weight: 800; font-size: 28px; letter-spacing: .16em; opacity: .85; }}
    .stat .sk {{ color: inherit; }}
    .sv {{ font-weight: 900; font-size: 92px; line-height: 1.0; white-space: nowrap; margin-top: 4px; }}
    .sv small {{ font-size: 40px; letter-spacing: .03em; }}
    .stat:not(.dkc) .sv small {{ background: {YEL}; padding: 4px 12px 6px; border-radius: 6px; vertical-align: middle; }}
    .cv2 {{ font-weight: 900; font-size: 58px; line-height: 1.05; white-space: nowrap; margin-top: 6px; }}
    .card.wcard .cv2 {{ font-size: 70px; }}
    .grid {{ display: grid; grid-template-columns: 432px 432px; gap: 16px; }}
    .am {{ display: flex; align-items: center; gap: 18px; padding: 14px 18px; border-radius: 12px; background: {WHT}; color: {CHR};
      box-shadow: 0 12px 30px rgba(0,0,0,.32); }}
    .am .ai {{ width: 80px; height: 80px; border-radius: 10px; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; }}
    .am span {{ font-weight: 900; font-size: 40px; letter-spacing: .02em; }}
    .dirs {{ display: grid; grid-template-columns: 432px 432px; gap: 16px; }}
    .dir {{ padding: 20px 22px 22px; border-radius: 12px; background: rgba(23,23,23,.92); border-top: 8px solid {YEL};
      box-shadow: 0 14px 34px rgba(0,0,0,.38); text-align: center; }}
    .dk2 {{ font-weight: 800; font-size: 28px; letter-spacing: .14em; color: {YEL}; }}
    .dn {{ font-weight: 900; font-size: 44px; white-space: nowrap; margin-top: 8px; color: {WHT}; }}
    .dd {{ display: inline-block; margin-top: 10px; font-weight: 800; font-size: 28px; letter-spacing: .05em; color: {CHR};
      background: {YEL}; padding: 6px 14px 7px; border-radius: 6px; }}
    .ripple, .tapr {{ position: absolute; border-radius: 50%; border: 4px solid {YEL}; opacity: 0; pointer-events: none; }}
    .pin {{ position: relative; }}
    .ripple {{ left: -18px; top: -14px; width: 80px; height: 80px; }}
    .am {{ position: relative; }}
    .tick {{ position: absolute; right: 14px; top: 50%; margin-top: -21px; width: 42px; height: 42px; border-radius: 50%; background: {YEL};
      display: flex; align-items: center; justify-content: center; transform: scale(0); }}
    .ar {{ display: inline-block; }}
    .btnw {{ position: relative; }}
    .tapr {{ left: 50%; top: 50%; width: 120px; height: 120px; margin: -60px 0 0 -60px; }}
    .hand {{ position: absolute; right: -34px; top: 62px; opacity: 0; filter: drop-shadow(0 8px 14px rgba(0,0,0,.4)); }}
    .rbg {{ position: absolute; inset: 0; opacity: 0; }}
    .rbg img {{ width: 100%; height: 100%; object-fit: cover; filter: blur(28px); transform: scale(1.15); }}
    .rdim {{ position: absolute; inset: 0; background: rgba(23,23,23,.45); }}
    .rcard {{ position: absolute; left: {SIDE}px; top: 560px; width: 880px; height: 660px; border-radius: 16px; overflow: hidden; opacity: 0;
      border: 6px solid {WHT}; box-shadow: 0 26px 60px rgba(0,0,0,.5); }}
    .rcard img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
'''
gfx = f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="gfx" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{chr(10).join(H)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in J).lstrip()}
    window.__timelines["gfx"] = tl;
  </script>
</template>
'''
open("compositions/gfx.html", "w").write(gfx)
print("total", TOTAL, {k: v for k, v in start.items()})
