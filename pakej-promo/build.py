#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman package promo.

Talent takes play back to back (with their own sound); B-roll sits on top, muted;
every graphic is timed in clip-local seconds and converted to film time here.
Word times come from aligning each take against the earlier 72 s edit's transcript.
"""
import json

FPS = 25
# (id, file, in, out) — talent takes in script order
SEGS = [
    ("hook", "t9933", 0.30, 8.55),
    ("loc", "t9934", 0.40, 7.00),
    ("size", "t9936", 0.20, 9.83),
    ("custom", "t9937", 0.25, 7.15),
    ("area", "t9939a", 0.00, 5.00),
    ("flood", "t9939b", 0.20, 4.20),
    ("road", "t9941", 0.45, 5.35),
    ("near", "t9944", 0.10, 3.78),
    ("places", "t-drive", 0.15, 13.45),
    ("cta", "t9945", 0.25, 6.27),
]
start = {}
t = 0.0
for sid, f, a, b in SEGS:
    start[sid] = round(t, 3)
    t += b - a
HOLD = 1.0
TOTAL = round(t + HOLD, 3)


def T(sid, local):
    """clip-local time (seconds into the source file) -> film time"""
    a = [s for s in SEGS if s[0] == sid][0][2]
    return round(start[sid] + local - a, 3)


# B-roll cutaways: (id, file, film start, film end, media start)
BROLL = [
    ("b-drone1", "drone", T("hook", 5.70), T("hook", 8.55), 7.8),
    ("b-map", "map-lokasi", T("loc", 4.60), T("loc", 7.00), 0.2),
    ("b-lots", "map-lot", T("size", 1.00), T("size", 5.30), 0.7),
    ("b-drone2", "drone", T("area", 1.00), T("area", 3.40), 5.5),
]

# ---------- index.html ----------
vids = []
for k, (sid, f, a, b) in enumerate(SEGS):
    vids.append(
        f'      <div id="w-{sid}" style="position:absolute; inset:0; z-index:1; overflow:hidden">'
        f'<video id="v-{sid}" class="clip" src="assets/video/{f}.mp4" data-start="{start[sid]}" '
        f'data-duration="{round(b - a, 3)}" data-media-start="{a}" data-track-index="1" playsinline '
        f'data-has-audio="true" data-volume="1" data-fade-in="0.04" data-fade-out="0.06" '
        f'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video></div>'
    )
vids.append(f'      <div id="w-hold" style="position:absolute; inset:0; z-index:1; overflow:hidden"><img id="v-hold" class="clip" src="assets/img/cta-hold.jpg" alt="" data-start="{round(t, 3)}" data-duration="{HOLD}" data-track-index="1" style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover" /></div>')
for bid, f, s, e, m in BROLL:
    vids.append(
        f'      <div id="{bid}-w" style="position:absolute; inset:0; z-index:2; overflow:hidden">'
        f'<video id="{bid}" src="assets/video/{f}.mp4" data-start="{s}" data-duration="{round(e - s, 3)}" '
        f'data-media-start="{m}" data-track-index="2" class="clip" muted playsinline '
        f'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video></div>'
    )

SFX = []
def sfx(name, file, at, dur, vol):
    SFX.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{file}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{dur}" data-track-index="{5 + len(SFX) % 3}" data-volume="{vol}"></audio>')

sfx("hook", "whoosh-short", T("hook", 0.45), 0.57, 0.16)
sfx("title", "whoosh", T("hook", 5.62), 0.57, 0.2)
sfx("titlepop", "pop", T("hook", 5.95), 0.72, 0.16)
sfx("map", "whoosh-short", T("loc", 4.55), 0.57, 0.16)
sfx("locpin", "pop", T("loc", 4.98), 0.72, 0.15)
sfx("lots", "whoosh", T("size", 0.95), 0.57, 0.18)
sfx("land", "pop", T("size", 2.6), 0.72, 0.15)
sfx("house", "pop", T("size", 7.0), 0.72, 0.15)
sfx("renders", "whoosh", T("custom", 4.3), 0.57, 0.18)
sfx("drone2", "whoosh-short", T("area", 0.95), 0.57, 0.16)
sfx("chk1", "click-soft", T("area", 2.1), 0.36, 0.2)
sfx("chk2", "click-soft", T("flood", 2.82), 0.36, 0.2)
sfx("roadpop", "pop", T("road", 4.0), 0.72, 0.15)
for i in range(4):
    sfx(f"li{i}", "click-soft", T("near", 2.05) + i * 0.22, 0.36, 0.16)
sfx("smk", "pop", T("places", 4.65), 0.72, 0.15)
sfx("bandar", "pop", T("places", 8.15), 0.72, 0.15)
sfx("uitm", "pop", T("places", 11.78), 0.72, 0.15)
sfx("lot", "impact-bass-1", T("cta", 0.4), 1.5, 0.22)
sfx("ctapop", "pop", T("cta", 4.4), 0.72, 0.18)

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #101216; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #101216; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(SFX)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // B-roll: a slow push inside each cutaway so the frame keeps moving
      {json.dumps([b[0] for b in BROLL])}.forEach((id, i) => {{
        const s = {json.dumps([b[2] for b in BROLL])}[i], e = {json.dumps([b[3] for b in BROLL])}[i];
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.08, duration: e - s, ease: "none" }}, s);
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18, ease: "power1.out" }}, s);
      }});
      // talent takes: a gentle push-in on each so cuts feel like camera moves
      {json.dumps([s[0] for s in SEGS])}.forEach((id, i) => {{
        const s = {json.dumps([start[s[0]] for s in SEGS])}[i], d = {json.dumps([round(s[3] - s[2], 3) for s in SEGS])}[i];
        tl.fromTo("#v-" + id, {{ scale: 1.0 }}, {{ scale: 1.05, duration: d, ease: "none" }}, s);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------- gfx.html ----------
ICON = {
    "pin": '<svg viewBox="0 0 48 64" width="40" height="54"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="#F6C343"/><circle cx="24" cy="24" r="8.5" fill="#14161B"/></svg>',
    "check": '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#14161B" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5 L10 17 L19 7"/></svg>',
    "hospital": '<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linejoin="round"><rect x="7" y="7" width="34" height="34" rx="6"/><path d="M24 15v18M15 24h18" stroke-linecap="round"/></svg>',
    "mart": '<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9h6l5 22h21l4-15H14"/><circle cx="19" cy="39" r="3"/><circle cx="34" cy="39" r="3"/></svg>',
    "mosque": '<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#14161B" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 42V26c0-7 12-10 12-17 0 7 12 10 12 17v16z"/><path d="M5 42V20M43 42V20M5 20l0-5M43 20v-5"/><path d="M20 42v-8a4 4 0 0 1 8 0v8M2 42h44"/></svg>',
    "school": '<svg viewBox="0 0 48 48" width="52" height="52" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18 24 8l21 10-21 10z"/><path d="M11 22v11c4 4 22 4 26 0V22"/><path d="M45 18v12"/></svg>',
    "road": '<svg viewBox="0 0 48 48" width="70" height="70" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4 6 44M32 4l10 40"/><path d="M24 8v6M24 21v6M24 34v6"/></svg>',
    "area": '<svg viewBox="0 0 48 48" width="70" height="70" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linejoin="round"><path d="M6 44 6 18 24 6l18 12v26z"/><path d="M14 44V28h10v16"/><path d="M28 30h8v6h-8z"/></svg>',
    "size": '<svg viewBox="0 0 48 48" width="70" height="70" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"><path d="M4 32 24 22l20 10-20 10z"/><path d="M24 22V6"/><path d="M24 6l12 4-12 4" fill="#14161B"/></svg>',
    "house": '<svg viewBox="0 0 48 48" width="70" height="70" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"><path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M20 43V31h8v12"/></svg>',
}

H = []   # markup
J = []   # timeline js


def tin(sel, at, kind="up"):
    frm = {"up": "{ opacity: 0, y: 34, filter: 'blur(10px)' }", "scale": "{ opacity: 0, scale: 0.82, filter: 'blur(10px)' }",
           "left": "{ opacity: 0, x: -200, filter: 'blur(10px)' }", "fade": "{ opacity: 0, filter: 'blur(8px)' }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, x: 0, y: 0, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, {round(at, 3)});')


def tout(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {round(at, 3)});')


def block(bid, s, e, inner, top, extra=""):
    H.append(f'    <div class="grp clip" id="{bid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px{extra}">{inner}</div>')


# 1. hook — words land as he says them
s, e = T("hook", 0.40), T("hook", 4.05)
block("g-hook", s, e, '''<div class="hk" style="font-size:88px"><span class="hw" id="hw1">NAK</span> <span class="hw" id="hw2">BINA</span> <span class="hw" id="hw3">RUMAH</span></div>
      <div class="hk y"><span class="hw" id="hw4">TAPI</span> <span class="hw" id="hw5">TAK ADA</span> <span class="hw" id="hw6">TANAH?</span></div>''', 190, "; text-align:center")
for i, at in enumerate([0.50, 0.70, 1.02, 1.62, 1.93, 2.45]):
    J.append(f'tl.fromTo("#hw{i + 1}", {{ opacity: 0, y: 26, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }}, {T("hook", at)});')
tout("#g-hook", e - 0.22)

# 1b. subheadline + package title
s, e = T("hook", 4.50), T("hook", 8.55)
block("g-pkg", s, e, '''<div class="kick" id="pk-k"><b>MAHLIGAI IDAMAN</b> MENYEDIAKAN</div>
      <div class="bigbox" id="pk-b"><div class="l1">PAKEJ BINA RUMAH</div><div class="l2">BERSERTA TANAH</div></div>''', 200, "; display:flex; flex-direction:column; align-items:center")
tin("#pk-k", s, "fade")
tin("#pk-b", T("hook", 5.78), "scale")
J.append(f'tl.fromTo("#pk-b", {{ backgroundPosition: "130% 0, 0 0" }}, {{ backgroundPosition: "-30% 0, 0 0", duration: 0.9, ease: "sine.inOut" }}, {T("hook", 6.4)});')
tout("#g-pkg", e - 0.22)

# 2. location
s, e = T("loc", 4.92), T("loc", 7.00)
block("g-loc", s, e, f'''<div class="chip" id="lc">{ICON["pin"]}<div><div class="ck">LOKASI</div><div class="cv">KAMPUNG WEK MACHANG</div></div></div>''', 210, "; display:flex; justify-content:center")
tin("#lc", s, "up")
tout("#g-loc", e - 0.22)

# 3a. land size (over the lot map, kept low so the lot labels stay clear)
s, e = T("size", 2.30), T("size", 6.45)
block("g-land", s, e, f'''<div class="stat" id="ld"><div class="si">{ICON["size"]}</div><div><div class="sk">KELUASAN LOT BERMULA</div>
      <div class="sv"><span id="n-land">5,101</span> <small>KPS</small></div></div></div>''', 1460, "; display:flex; justify-content:center")
tin("#ld", s, "scale")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 5101, duration: 0.7, ease: "power3.out", onUpdate: () => {{ document.querySelector("#n-land").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {T("size", 2.30)}); }})();')
tout("#g-land", e - 0.22)

# 3b. house size
s, e = T("size", 6.85), T("size", 9.83)
block("g-house", s, e, f'''<div class="stat" id="hs"><div class="si">{ICON["house"]}</div><div><div class="sk">BOLEH BINA RUMAH BERMULA</div>
      <div class="sv"><span id="n-house">1,400</span> <small>KPS KE ATAS</small></div></div></div>''', 200, "; display:flex; justify-content:center")
tin("#hs", s, "scale")
J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: 1400, duration: 0.7, ease: "power3.out", onUpdate: () => {{ document.querySelector("#n-house").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {T("size", 6.85)}); }})();')
tout("#g-house", e - 0.22)

# 4. custom design: the three house renders as framed cards, then the line
s, e = T("custom", 4.35), T("custom", 7.15)
H.append(f'''    <div class="clip" id="g-renders" data-start="{s}" data-duration="{round(e - s, 3)}" style="position:absolute; inset:0">
      <div class="rbg"></div>
      <div class="rcard" id="rc1"><img src="assets/img/house-a.jpg" alt="" /></div>
      <div class="rcard" id="rc2"><img src="assets/img/house-b.jpg" alt="" /></div>
      <div class="rcard" id="rc3"><img src="assets/img/house-c.jpg" alt="" /></div>
      <div class="cust" id="cu"><div class="bigbox sm"><div class="l1">CUSTOM DESIGN</div></div><div class="cs">IKUT CITA RASA ANDA</div></div>
    </div>''')
J.append(f'tl.fromTo("#g-renders .rbg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.out" }}, {s});')
for i in range(3):
    a = s + i * 0.93
    J.append(f'tl.fromTo("#rc{i + 1}", {{ opacity: 0, x: 160, scale: 0.96 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.4, ease: "expo.out" }}, {round(a, 3)});')
    J.append(f'tl.to("#rc{i + 1} img", {{ scale: 1.08, duration: 1.2, ease: "none" }}, {round(a, 3)});')
    if i < 2:
        J.append(f'tl.to("#rc{i + 1}", {{ opacity: 0, x: -160, duration: 0.3, ease: "power2.in" }}, {round(a + 0.78, 3)});')
tin("#cu", T("custom", 4.5), "up")
tout("#g-renders", e - 0.2)

# 5/6. neighbourhood + flood free checklist (one list across both takes)
s, e = T("area", 1.95), T("flood", 4.20)
block("g-list", s, e, f'''<div class="row" id="li1"><div class="ck2">{ICON["check"]}</div><span>KAWASAN KEJIRANAN BANGLO</span></div>
      <div class="row" id="li2"><div class="ck2">{ICON["check"]}</div><span>BEBAS BANJIR</span></div>''', 200, "; display:flex; flex-direction:column; align-items:center; gap:22px")
tin("#li1", s, "left")
J.append('tl.set("#li2", { opacity: 0 }, 0);')
tin("#li2", T("flood", 2.78), "left")
tout("#g-list", e - 0.22)

# 7. tar road
s, e = T("road", 0.95), T("road", 5.35)
block("g-road", s, e, f'''<div class="kick" id="rd-k">KELEBIHAN TANAH DI SINI</div>
      <div class="stat" id="rd"><div class="si">{ICON["road"]}</div><div><div class="sk">AKSES</div><div class="sv">JALAN TAR <small>TERSEDIA</small></div></div></div>''', 200, "; display:flex; flex-direction:column; align-items:center")
tin("#rd-k", s, "fade")
J.append('tl.set("#rd", { opacity: 0 }, 0);')
tin("#rd", T("road", 3.95), "scale")
tout("#g-road", e - 0.22)

# 8. amenities grid — header on "dekat", items one by one, held into the next take
s, e = T("near", 1.80), T("places", 4.30)
items = [("hospital", "HOSPITAL"), ("mart", "PASARAYA"), ("mosque", "MASJID"), ("school", "SEKOLAH")]
grid = "".join(f'<div class="am" id="am{i}"><div class="ai">{ICON[k]}</div><span>{n}</span></div>' for i, (k, n) in enumerate(items))
block("g-near", s, e, f'''<div class="hd" id="nh">KEMUDAHAN BERDEKATAN</div><div class="grid">{grid}</div>''', 170, "; display:flex; flex-direction:column; align-items:center")
tin("#nh", s, "up")
for i in range(4):
    J.append(f'tl.set("#am{i}", {{ opacity: 0 }}, 0);')
    tin(f"#am{i}", T("near", 2.05) + i * 0.22, "scale")
tout("#g-near", e - 0.22)

# 9. real places, as he names them
s, e = T("places", 4.60), T("places", 13.45)
plc = [("smk", "SMK HAMZAH 2", "2 KM | 4 MINIT", "", 4.62), ("bdr", "BANDAR MACHANG", "6 KM | 10 MINIT", "KE KANAN", 8.12),
       ("uitm", "UiTM MACHANG", "6 KM | 10 MINIT", "KE KIRI", 11.75)]
rows = "".join(
    f'<div class="pl" id="pl-{k}">{ICON["pin"]}<div class="pt"><div class="pn">{n}</div><div class="pd"><b>{d}</b>{(" · " + dirn) if dirn else ""}</div></div></div>'
    for k, n, d, dirn, _ in plc)
block("g-places", s, e, f'''<div class="hd sm" id="ph">LOKASI STRATEGIK</div>{rows}''', 170, "; display:flex; flex-direction:column; align-items:center; gap:18px")
tin("#ph", s, "fade")
for k, _, _, _, at in plc:
    J.append(f'tl.set("#pl-{k}", {{ opacity: 0 }}, 0);')
    tin(f"#pl-{k}", T("places", at), "left")
tout("#g-places", e - 0.22)

# 10. closing
s, e = T("cta", 0.35), T("cta", 2.95)
block("g-lot", s, e, '''<div class="bigbox" id="lt"><div class="l1" style="font-size:118px">LOT TERHAD</div></div><div class="cs big" id="lt-s">SIAPA CEPAT, DIA DAPAT</div>''', 200, "; display:flex; flex-direction:column; align-items:center")
tin("#lt", s, "scale")
J.append('tl.set("#lt-s", { opacity: 0 }, 0);')
tin("#lt-s", T("cta", 1.48), "up")
tout("#g-lot", e - 0.22)

s, e = T("cta", 2.95), TOTAL
block("g-cta", s, e, '''<img class="logo" id="ct-l" src="assets/logo.png" alt="" /><div class="kick big" id="ct-k">BERMINAT?</div><div class="btn" id="ct-b">PM KAMI SEGERA</div>''', 150, "; display:flex; flex-direction:column; align-items:center")
tin("#ct-l", s, "scale")
tin("#ct-k", T("cta", 3.02), "up")
J.append('tl.set("#ct-b", { opacity: 0 }, 0);')
tin("#ct-b", T("cta", 4.40), "scale")
J.append(f'tl.fromTo("#ct-b", {{ boxShadow: "0 0 0 0 rgba(246,195,67,.65), 0 18px 44px rgba(0,0,0,.45)" }}, {{ boxShadow: "0 0 0 28px rgba(246,195,67,0), 0 18px 44px rgba(0,0,0,.45)", duration: 0.9, ease: "power1.out", repeat: 1 }}, {T("cta", 4.9)});')

CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: #fff; }
    .grp { position: absolute; left: 80px; right: 80px; }
    .hk { white-space: nowrap; font-weight: 900; font-size: 72px; line-height: 1.02; letter-spacing: -.01em; color: #fff;
      text-shadow: 0 4px 0 rgba(0,0,0,.28), 0 12px 34px rgba(0,0,0,.6); }
    .hk.y { color: #F6C343; }
    .hw { display: inline-block; opacity: 0; }
    .kick { padding: 12px 30px 14px; border-radius: 999px; background: rgba(12,14,18,.78); font-weight: 700; font-size: 36px;
      letter-spacing: .12em; color: #fff; white-space: nowrap; }
    .kick b { color: #F6C343; font-weight: 900; }
    .kick.big { font-size: 52px; padding: 14px 40px 16px; margin-top: 10px; }
    .bigbox { margin-top: 20px; padding: 22px 46px 26px; border-radius: 26px; text-align: center; color: #14161B;
      background: linear-gradient(100deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.5) 50%, rgba(255,255,255,0) 60%) no-repeat, #F6C343;
      background-size: 300% 100%, auto; background-position: 130% 0, 0 0; box-shadow: 0 22px 50px rgba(0,0,0,.42); }
    .bigbox .l1 { font-weight: 900; font-size: 74px; line-height: 1.0; letter-spacing: .01em; white-space: nowrap; }
    .bigbox .l2 { font-weight: 900; font-size: 74px; line-height: 1.0; letter-spacing: .01em; white-space: nowrap; color: #fff;
      margin-top: 8px; display: inline-block; background: #14161B; padding: 6px 22px 10px; border-radius: 14px; }
    .bigbox.sm { margin-top: 0; padding: 18px 40px 22px; }
    .bigbox.sm .l1 { font-size: 70px; }
    .chip { display: flex; align-items: center; gap: 20px; padding: 18px 36px 20px 26px; border-radius: 26px;
      background: rgba(12,14,18,.82); border: 3px solid #F6C343; box-shadow: 0 18px 44px rgba(0,0,0,.4); }
    .ck { font-weight: 800; font-size: 28px; letter-spacing: .24em; color: #F6C343; }
    .cv { font-weight: 900; font-size: 50px; letter-spacing: .02em; white-space: nowrap; }
    .stat { display: flex; align-items: center; gap: 26px; padding: 24px 44px 26px 28px; border-radius: 28px; background: #fff;
      color: #14161B; box-shadow: 0 22px 50px rgba(0,0,0,.42); margin-top: 16px; }
    .stat .si { width: 110px; height: 110px; border-radius: 22px; background: #F6C343; display: flex; align-items: center; justify-content: center; flex: none; }
    .sk { font-weight: 800; font-size: 28px; letter-spacing: .14em; color: #5A5F68; }
    .sv { font-weight: 900; font-size: 84px; line-height: 1.0; white-space: nowrap; }
    .sv small { font-size: 40px; letter-spacing: .03em; color: #B88A0E; }
    .row { display: flex; align-items: center; gap: 22px; padding: 18px 40px 20px 20px; border-radius: 999px; background: rgba(12,14,18,.82);
      border: 3px solid #F6C343; box-shadow: 0 18px 44px rgba(0,0,0,.4); }
    .row span { font-weight: 900; font-size: 46px; letter-spacing: .02em; white-space: nowrap; }
    .ck2 { width: 64px; height: 64px; border-radius: 50%; background: #F6C343; display: flex; align-items: center; justify-content: center; flex: none; }
    .hd { padding: 12px 34px 14px; border-radius: 16px; background: #F6C343; color: #14161B; font-weight: 900; font-size: 50px;
      letter-spacing: .04em; white-space: nowrap; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    .hd.sm { font-size: 36px; letter-spacing: .14em; padding: 10px 28px 12px; }
    .grid { margin-top: 22px; display: grid; grid-template-columns: 410px 410px; gap: 18px; }
    .am { display: flex; align-items: center; gap: 18px; padding: 14px 20px; border-radius: 20px; background: rgba(255,255,255,.95); color: #14161B;
      box-shadow: 0 14px 34px rgba(0,0,0,.35); }
    .am .ai { width: 76px; height: 76px; border-radius: 16px; background: #F6C343; display: flex; align-items: center; justify-content: center; flex: none; }
    .am span { font-weight: 900; font-size: 38px; letter-spacing: .02em; }
    .pl { display: flex; align-items: center; gap: 20px; width: 820px; padding: 16px 30px 18px 24px; border-radius: 22px;
      background: rgba(12,14,18,.84); border-left: 10px solid #F6C343; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    .pn { font-weight: 900; font-size: 46px; letter-spacing: .02em; white-space: nowrap; }
    .pd { font-weight: 700; font-size: 28px; letter-spacing: .08em; color: #fff; margin-top: 2px; white-space: nowrap; }
    .pd b { color: #F6C343; font-weight: 900; }
    .rbg { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse at 50% 45%, #2A2D33 0%, #121418 70%); }
    .rcard { position: absolute; left: 60px; top: 520px; width: 960px; height: 720px; border-radius: 28px; overflow: hidden; opacity: 0;
      border: 4px solid #fff; box-shadow: 0 30px 70px rgba(0,0,0,.6); }
    .rcard img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .cust { position: absolute; left: 0; right: 0; top: 1330px; display: flex; flex-direction: column; align-items: center; opacity: 0; }
    .cs { margin-top: 18px; font-weight: 800; font-size: 44px; letter-spacing: .16em; color: #fff; white-space: nowrap;
      text-shadow: 0 3px 12px rgba(0,0,0,.7); }
    .cs.big { font-size: 50px; color: #fff; }
    .logo { width: 190px; height: auto; filter: drop-shadow(0 8px 18px rgba(0,0,0,.45)); }
    .btn { margin-top: 26px; padding: 26px 64px 28px; border-radius: 999px; background: #F6C343; color: #14161B; font-weight: 900;
      font-size: 64px; letter-spacing: .05em; white-space: nowrap; }
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
