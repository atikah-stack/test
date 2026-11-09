#!/usr/bin/env python3
"""Mahligai Idaman — Pakej Tanah Beserta Bina Rumah, Kg Wek Machang. 30 s, 1080x1920, 30 fps.

Drone shots (source seconds in assets/video/drone.mp4; the file has no audio):
  0.0-5.4 low oblique over houses · 5.4-10.8 top-down · 10.8-13.8 wide with hills
  13.8-18.0 oblique · 18.0-22.1 oblique · 22.1-28.0 high wide with mountains · 28.0-30.0 top-down
"""
import json

TOTAL = 30.0
# (id, film start, film dur, media start, playback rate)
SHOTS = [
    ("s-hook", 0.0, 4.2, 22.1, 1.0),
    ("s-top", 4.0, 1.9, 5.4, 1.0),
    ("s-loc", 9.0, 4.2, 10.8, 0.72),
    ("s-lm1", 13.0, 4.6, 13.8, 0.9),
    ("s-lm2", 17.4, 4.8, 7.0, 0.78),
    ("s-nbh", 22.0, 4.2, 0.6, 1.0),
    ("s-cta", 26.0, 4.0, 18.0, 1.0),
]
LAYOUT = (5.6, 3.6)  # film start, dur of the subdivision insert

V = []
for sid, s, d, m, r in SHOTS:
    V.append(f'      <div class="vw" id="w-{sid}"><video id="{sid}" class="clip" src="assets/video/drone.mp4" data-start="{s}" '
             f'data-duration="{d}" data-media-start="{m}" data-playback-rate="{r}" data-track-index="1" muted playsinline></video></div>')

SFX = []
def sfx(name, f, at, dur, vol):
    SFX.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 2)}" data-duration="{dur}" '
               f'data-track-index="{5 + len(SFX) % 3}" data-volume="{vol}"></audio>')

sfx("hook", "impact-bass-2", 0.32, 2.5, 0.55)
sfx("hook2", "whoosh-short", 0.95, 0.57, 0.3)
sfx("t1", "whoosh", 3.85, 0.57, 0.35)
sfx("lay", "whoosh-cinematic", 5.45, 1.6, 0.3)
sfx("head2", "impact-bass-1", 5.9, 2.0, 0.4)
for i in range(6):
    sfx(f"lot{i}", "click-soft", 6.55 + i * 0.32, 0.36, 0.35)
sfx("t2", "whoosh", 8.85, 0.57, 0.35)
sfx("pin", "notification", 9.6, 1.2, 0.25)
for i, t in enumerate([13.05, 16.55, 19.55]):
    sfx(f"card{i}", "whoosh-short", t - 0.05, 0.57, 0.3)
    sfx(f"pop{i}", "pop", t + 0.35, 0.72, 0.3)
sfx("t4", "whoosh", 21.85, 0.57, 0.35)
sfx("nbh", "sparkle", 22.45, 1.4, 0.22)
sfx("rise", "riser", 24.6, 1.5, 0.28)
sfx("cta", "impact-bass-1", 26.15, 2.0, 0.5)
sfx("wa", "notification", 27.35, 1.2, 0.3)

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0d1210; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #0d1210; }}
      .vw {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 50% 50%; }}
      .vw video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(V)}
      <div id="lay" data-composition-id="lay" data-composition-src="compositions/lay.html" data-start="{LAYOUT[0]}" data-duration="{LAYOUT[1]}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(SFX)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // slow cinematic push in every shot; a short scale settle on entry so cuts feel like camera moves
      {json.dumps([(s[0], s[1], s[2]) for s in SHOTS])}.forEach(([id, s, d], i) => {{
        tl.fromTo("#w-" + id, {{ scale: 1.12 }}, {{ scale: 1.03, duration: 0.6, ease: "expo.out" }}, s);
        tl.to("#w-" + id, {{ scale: i === 0 || i === 6 ? 1.13 : 1.09, duration: d - 0.6, ease: "none" }}, s + 0.6);
      }});
      tl.to("#w-s-cta", {{ opacity: 0, duration: 0.6, ease: "power1.in" }}, {TOTAL - 0.6});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------------- subdivision layout insert ----------------
K = 1080 / 941  # layout.jpg is 941x1672
LOTS = [("9", 620, 428, 700, 580, "5,200"), ("11", 778, 428, 852, 580, "5,200"), ("18", 567, 642, 643, 780, "5,103"),
        ("27", 468, 784, 535, 917, "5,101"), ("36", 403, 987, 483, 1120, "5,512"), ("38", 565, 987, 640, 1120, "5,512")]
holes, rects, ljs = [], [], []
for i, (n, x0, y0, x1, y1, a) in enumerate(LOTS):
    X0, Y0, W, H = round(x0 * K, 1), round(y0 * K, 1), round((x1 - x0) * K, 1), round((y1 - y0) * K, 1)
    holes.append(f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="4" fill="black"/>')
    rects.append(f'<rect class="lr" id="lr{i}" x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="4" pathLength="100"/>'
                 f'<rect class="lg" id="lg{i}" x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="4"/>')
    t = round(0.95 + i * 0.32, 2)
    ljs.append(f'tl.fromTo("#lr{i}", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }}, {t});')
    ljs.append(f'tl.fromTo("#lg{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {round(t + 0.2, 2)});')
    ljs.append(f'tl.to("#lg{i}", {{ opacity: 0.35, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: {3 - (i // 3)} }}, {round(t + 0.55, 2)});')
lay = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #0d1210; }}
    #l-cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 600px 700px; }}
    #l-img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1919px; display: block; }}
    #l-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #l-svg .dim {{ fill: rgba(6,10,8,.55); }}
    #l-svg .lr {{ fill: none; stroke: #FFC845; stroke-width: 6; stroke-linejoin: round; stroke-dasharray: 100 120; stroke-dashoffset: 100; }}
    #l-svg .lg {{ fill: rgba(255,200,69,.28); stroke: #FFE7A6; stroke-width: 2; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="lay" data-width="1080" data-height="1920" data-duration="{LAYOUT[1]}">
    <div id="l-cam" data-layout-allow-overflow>
      <img id="l-img" src="assets/img/layout.jpg" alt="" />
      <svg id="l-svg" viewBox="0 0 1080 1920">
        <defs><mask id="l-holes"><rect x="0" y="0" width="1080" height="1920" fill="white"/>{"".join(holes)}</mask></defs>
        <rect class="dim" id="l-dim" x="0" y="0" width="1080" height="1920" mask="url(#l-holes)"/>
        {"".join(rects)}
      </svg>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#root", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power1.inOut" }}, 0);
    tl.fromTo("#l-cam", {{ scale: 1.22, rotation: 0 }}, {{ scale: 1.04, duration: 1.0, ease: "power3.out" }}, 0);
    tl.to("#l-cam", {{ scale: 1.1, duration: 2.6, ease: "none" }}, 1.0);
    tl.fromTo("#l-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power1.inOut" }}, 0.6);
    {chr(10).join("    " + j for j in ljs).lstrip()}
    window.__timelines["lay"] = tl;
  </script>
</template>
'''
open("compositions/lay.html", "w").write(lay)

# ---------------- graphics ----------------
H, J = [], []
def el(h): H.append("    " + h)
def js(s): J.append("    " + s)

def head(gid, s, e, l1, l2, sub=None, top=560, extra="", h2=108):
    sub_html = f'<div class="sub" id="{gid}-s">{sub}</div>' if sub else ""
    el(f'<div class="g clip" id="{gid}" data-start="{s}" data-duration="{round(e - s, 2)}" style="top:{top}px; --h2:{h2}px">'
       f'<div class="h1" id="{gid}-1">{l1}</div><div class="h2" id="{gid}-2"><span class="hl" id="{gid}-hl"></span><span class="ht">{l2}</span></div>{sub_html}{extra}</div>')
    js(f'tl.fromTo("#{gid}-1", {{ opacity: 0, y: 50, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "expo.out" }}, {round(s + 0.05, 2)});')
    js(f'tl.fromTo("#{gid}-2", {{ opacity: 0, scale: 1.25, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.55, ease: "expo.out" }}, {round(s + 0.25, 2)});')
    js(f'tl.fromTo("#{gid}-hl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.inOut" }}, {round(s + 0.6, 2)});')
    if sub:
        js(f'tl.fromTo("#{gid}-s", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(s + 0.75, 2)});')
    js(f'tl.to("#{gid}", {{ opacity: 0, y: -24, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 2)});')

PIN = '<svg viewBox="0 0 48 64" width="52" height="70"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="#FFC845"/><circle cx="24" cy="24" r="9" fill="#14161B"/></svg>'
HOUSE = '<svg viewBox="0 0 48 48" width="64" height="64" fill="none" stroke="#14161B" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"><path d="M5 22 24 7l19 15"/><path d="M10 19v23h28V19"/><path d="M20 42V30h8v12"/></svg>'
WA = '<svg viewBox="0 0 32 32" width="64" height="64"><circle cx="16" cy="16" r="16" fill="#25D366"/><path d="M16 6.5a9.4 9.4 0 0 0-8.1 14.2L6.6 25.5l4.9-1.3A9.4 9.4 0 1 0 16 6.5zm0 17.2a7.8 7.8 0 0 1-4-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A7.8 7.8 0 1 1 16 23.7zm4.3-5.8c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.8.9-.3.2-.5.1a6.4 6.4 0 0 1-3.2-2.8c-.2-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.7-1.7c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3z" fill="#fff"/></svg>'

# 1. hook
head("h-hook", 0.25, 4.0, "PAKEJ TANAH BESERTA", "BINA RUMAH", "KHAS UNTUK ORANG KELANTAN!", top=600)
# 2. lots (over the drone top-down, then the layout insert)
head("h-lot", 4.15, 9.0, "TINGGAL BEBERAPA", "LOT SAHAJA!", None, top=1360)
# 3. location
head("h-loc", 9.1, 13.0, "LOKASI STRATEGIK", "KG WEK, MACHANG", "MUDAH AKSES KE KEMUDAHAN SEKITAR", top=640, h2=92,
     extra=f'<div class="pinw" id="h-pin">{PIN}<div class="pulse" id="h-pu1"></div><div class="pulse" id="h-pu2"></div></div>')
js('tl.fromTo("#h-pin", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.5, ease: "bounce.out" }, 9.45);')
js('tl.fromTo(["#h-pu1", "#h-pu2"], { opacity: 0.9, scale: 0.3 }, { opacity: 0, scale: 2.4, duration: 1.2, ease: "power2.out", stagger: 0.4, repeat: 1 }, 9.9);')
# 4. landmark cards
CARDS = [("smk", 13.05, 16.45, "5 MINIT", "SMK HAMZAH 2", "assets/img/smk.jpg", "50% 58%"),
         ("bdr", 16.55, 19.45, "10 MINIT", "BANDAR MACHANG", "assets/img/bandar.jpg", "50% 45%"),
         ("uitm", 19.55, 22.0, "10 MINIT", "UiTM MACHANG", "assets/img/uitm.jpg", "50% 42%")]
el('<div class="g clip" id="h-lmk" data-start="13.0" data-duration="9.0" style="top:330px"><div class="kick" id="lmk-k">LOKASI <span class="y">BERDEKATAN</span></div></div>')
js('tl.fromTo("#lmk-k", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 13.05);')
js('tl.to("#h-lmk", { opacity: 0, duration: 0.25, ease: "power2.in" }, 21.75);')
for k, s, e, tm, name, img, pos in CARDS:
    el(f'<div class="g clip" id="c-{k}" data-start="{s}" data-duration="{round(e - s, 2)}" style="top:500px">'
       f'<div class="card" id="cd-{k}"><div class="ph"><img src="{img}" alt="" style="object-position:{pos}" /></div>'
       f'<div class="cb"><div class="ic">{PIN}</div><div><div class="tm">{tm}</div><div class="nm">{name}</div></div></div></div></div>')
    js(f'tl.fromTo("#cd-{k}", {{ opacity: 0, x: 220, scale: 0.94 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.55, ease: "expo.out" }}, {s});')
    js(f'tl.fromTo("#cd-{k} .ph img", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {round(e - s, 2)}, ease: "none" }}, {s});')
    js(f'tl.to("#cd-{k}", {{ opacity: 0, x: -200, duration: 0.3, ease: "power2.in" }}, {round(e - 0.3, 2)});')
# 5. neighbourhood
head("h-nbh", 22.1, 26.0, "KAWASAN KEJIRANAN", "SEDIA ADA", "LOKASI STRATEGIK &amp; MUDAH AKSES", top=600,
     extra=f'<div class="hic" id="h-house">{HOUSE}</div>')
js('tl.fromTo("#h-house", { opacity: 0, scale: 0.4, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2)" }, 22.45);')
# 6. CTA
head("h-cta", 26.1, 29.95, "ANDA BERMINAT?", "HUBUNGI SEGERA!", "PAKEJ TANAH BESERTA BINA RUMAH", top=600, h2=100,
     extra=f'<div class="wa" id="h-wa">{WA}<span>WHATSAPP KAMI</span></div>')
js('tl.fromTo("#h-wa", { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, 27.3);')
js('tl.to("#h-wa svg", { scale: 1.12, rotation: -8, duration: 0.18, ease: "sine.inOut", yoyo: true, repeat: 5 }, 27.9);')

CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: Poppins, sans-serif; color: #fff; }
    .g { position: absolute; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center; }
    .y { color: #FFC845; }
    .h1 { font-weight: 800; font-size: 70px; line-height: 1.05; letter-spacing: -.005em; color: #FFFFFF; white-space: nowrap;
      text-shadow: 0 4px 14px rgba(0,0,0,.35), 0 2px 3px rgba(0,0,0,.35); opacity: 0; }
    .h2 { position: relative; margin-top: 6px; opacity: 0; }
    .h2 .ht { position: relative; font-weight: 800; font-size: var(--h2, 108px); line-height: 1.02; letter-spacing: -.01em; color: #FFC845; white-space: nowrap;
      text-shadow: 0 5px 18px rgba(0,0,0,.35), 0 2px 4px rgba(0,0,0,.35); }
    .h2 .hl { position: absolute; left: -14px; right: -14px; bottom: 10px; height: 26px; background: rgba(255,200,69,.22); border-radius: 6px;
      transform-origin: 0 50%; }
    .sub { margin-top: 18px; padding: 12px 30px 14px; border-radius: 14px; background: rgba(8,10,12,.45); font-weight: 600; font-size: 38px;
      letter-spacing: .04em; color: #fff; white-space: nowrap; text-shadow: 0 2px 8px rgba(0,0,0,.35); opacity: 0; }
    .chips { display: grid; grid-template-columns: repeat(3, 286px); gap: 14px; }
    .chip { padding: 10px 14px 12px; border-radius: 16px; background: rgba(8,10,12,.72); border: 2px solid #FFC845; opacity: 0; }
    .chip b { display: block; font-weight: 800; font-size: 38px; color: #FFC845; line-height: 1.05; }
    .chip span { display: block; font-weight: 600; font-size: 28px; color: #fff; }
    .pinw { position: relative; margin-top: 26px; width: 60px; height: 76px; display: flex; justify-content: center; opacity: 0; }
    .pulse { position: absolute; left: 50%; bottom: -6px; width: 70px; height: 26px; margin-left: -35px; border-radius: 50%; border: 4px solid #FFC845; opacity: 0; }
    .kick { padding: 10px 30px 12px; border-radius: 999px; background: rgba(8,10,12,.6); font-weight: 800; font-size: 40px; letter-spacing: .1em; white-space: nowrap; opacity: 0; }
    .card { width: 860px; border-radius: 30px; overflow: hidden; background: rgba(8,10,12,.72); border: 3px solid rgba(255,200,69,.9);
      box-shadow: 0 24px 60px rgba(0,0,0,.45); opacity: 0; }
    .card .ph { width: 860px; height: 560px; overflow: hidden; }
    .card .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .card .cb { display: flex; align-items: center; gap: 26px; padding: 22px 34px 26px; text-align: left; }
    .card .ic { width: 96px; height: 96px; border-radius: 22px; background: rgba(255,200,69,.16); display: flex; align-items: center; justify-content: center; flex: none; }
    .card .tm { font-weight: 800; font-size: 84px; line-height: 1; color: #FFC845; text-shadow: 0 3px 10px rgba(0,0,0,.35); }
    .card .nm { font-weight: 600; font-size: 50px; line-height: 1.1; color: #fff; margin-top: 4px; white-space: nowrap; }
    .hic { margin-top: 24px; width: 104px; height: 104px; border-radius: 26px; background: #FFC845; display: flex; align-items: center; justify-content: center;
      box-shadow: 0 14px 34px rgba(0,0,0,.35); opacity: 0; }
    .wa { margin-top: 30px; display: flex; align-items: center; gap: 18px; padding: 14px 40px 14px 16px; border-radius: 999px; background: rgba(8,10,12,.62);
      border: 3px solid #25D366; font-weight: 800; font-size: 42px; letter-spacing: .04em; white-space: nowrap; opacity: 0; }
'''
gfx = f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="gfx" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{chr(10).join(H)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(J)}
    window.__timelines["gfx"] = tl;
  </script>
</template>
'''
open("compositions/gfx.html", "w").write(gfx)
print("ok")
