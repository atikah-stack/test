#!/usr/bin/env python3
"""Testimoni Puan Zunaida (IMG_7123) -> 9:16 short. Source: Google Drive original, tone-mapped clips in assets/video.

Talent clips (cut from IMG_7123.mov, audio cleaned):
  w1.mp4 = source 173.4-206.2 (wide shot) · w2.mp4 = 220.4-241.6 (close) · w3.mp4 = 552.0-560.6 (close)
Segments are written in SOURCE seconds and converted to film time.
"""
import json, re

CLIP0 = {"w1": 173.4, "w2": 220.4, "w3": 552.0}
WIDE = {"w1"}
SEGS = [  # id, clip, src_in, src_out
    ("A", "w1", 199.40, 205.45),   # "Terus sign masa itu. Buka file terus. Tak sabar."
    ("B", "w1", 173.95, 178.12),   # "Saya dengan suami, tengoklah di Facebook, cari-cari kan."
    ("C", "w1", 185.38, 188.95),   # "Macam dia punya feedback tu, okey."
    ("D1", "w1", 190.18, 191.32),  # "Satu hari balik tu,"
    ("D2", "w1", 192.38, 198.95),  # "nak pergi dekat MI punya ofis. So nak tanyalah macam mana buat tu kan."
    ("E", "w2", 220.95, 231.65),   # "Dah lah, kita sign teruslah ... so okey lah."
    ("F", "w2", 232.00, 235.55),   # "Maksudnya kita puas hati, rasa confident nak buat dengan MI lah."
    ("G", "w2", 235.62, 240.85),   # "Sebab tu terus sign dia. Tak payah pergi survey lain tempat lagi."
    ("H", "w3", 552.45, 560.05),   # "So yang macam MI ni ... So kita pilih Mahligai lah."
]
CTA = 3.4
start, t = {}, 0.0
for sid, c, a, b in SEGS:
    start[sid] = round(t, 3); t += b - a
TALK = round(t, 3)
TOTAL = round(TALK + CTA, 3)

def src(sid, s):
    _, c, a, b = next(x for x in SEGS if x[0] == sid)
    return round(start[sid] + s - a, 3)

# B-roll over the talent audio: (id, file, film start, dur)
BROLL = [
    ("r1", "b-img_3772", src("E", 227.05), 2.4),   # exterior: "banyak dah buat rumah, dah siap"
    ("r2", "b-img_3757", src("E", 229.45), 2.2),   # porch pillars: "tak ada yang terbengkalai"
    ("r3", "b-img_3555", src("G", 235.62), 2.0),   # dining: covers the F->G jump cut
    ("r4", "b-img_3756", src("H", 552.45), 2.0),   # porch: "dah banyak orang buat rumah"
    ("r5", "b-img_3584", src("H", 554.45), 2.0),   # kitchen
    ("r6", "b-img_3564", src("H", 556.45), 2.0),   # dining -> back to her face for "So kita pilih Mahligai lah"
]

V = []
for sid, c, a, b in SEGS:
    V.append(f'      <div class="vw" id="w-{sid}"><video id="v-{sid}" class="clip" src="assets/video/{c}.mp4" data-start="{start[sid]}" '
             f'data-duration="{round(b - a, 3)}" data-media-start="{round(a - CLIP0[c], 3)}" data-track-index="1" playsinline '
             f'data-has-audio="true" data-volume="1" data-fade-in="0.03" data-fade-out="0.05"></video></div>')
for rid, f, s, d in BROLL:
    V.append(f'      <div class="vw br" id="w-{rid}"><video id="v-{rid}" class="clip" src="assets/video/{f}.mp4" data-start="{s}" '
             f'data-duration="{d}" data-media-start="0.3" data-track-index="2" muted playsinline></video></div>')
V.append(f'      <div class="vw" id="w-cta"><video id="v-cta" class="clip" src="assets/video/b-img_3772.mp4" data-start="{TALK}" '
         f'data-duration="{CTA}" data-media-start="4.0" data-track-index="1" muted playsinline></video></div>')

SFX = []
def sfx(n, f, at, d, v):
    SFX.append(f'      <audio id="sx-{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" data-duration="{d}" '
               f'data-track-index="{5 + len(SFX) % 3}" data-volume="{v}"></audio>')

sfx("hook", "whoosh-short", 0.1, 0.57, 0.18)
sfx("fb", "pop", src("B", 175.3), 0.72, 0.12)
sfx("fbk", "pop", src("C", 186.4), 0.72, 0.12)
sfx("ofis", "pop", src("D2", 194.0), 0.72, 0.12)
sfx("rumah", "click-soft", src("E", 228.5), 0.36, 0.18)
sfx("yakin", "chime", src("F", 233.8), 1.2, 0.06)
sfx("cta", "whoosh-short", TALK - 0.05, 0.57, 0.18)
sfx("cta2", "sparkle", TALK + 0.6, 1.4, 0.1)

# camera: wide shot is punched in on her face; alternate framing at each same-shot cut
PUNCH = []
for k, (sid, c, a, b) in enumerate(SEGS):
    if c in WIDE:
        s0 = 1.62 if k % 2 == 0 else 1.78
        PUNCH.append((sid, start[sid], round(b - a, 3), s0, s0 + 0.05, "455px 790px"))
    else:
        s0 = 1.0 if k % 2 == 0 else 1.1
        PUNCH.append((sid, start[sid], round(b - a, 3), s0, s0 + 0.04, "500px 840px"))

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0f1012; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #0f1012; }}
      .vw {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; }}
      .vw.br {{ z-index: 2; }}
      .vw video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(V)}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(SFX)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(PUNCH)}.forEach(([id, s, d, a, b, o]) => tl.fromTo("#w-" + id, {{ scale: a, transformOrigin: o }}, {{ scale: b, duration: d, ease: "none" }}, s));
      {json.dumps([(r[0], r[2], r[3]) for r in BROLL])}.forEach(([id, s, d]) => {{
        tl.fromTo("#w-" + id, {{ opacity: 0, scale: 1.06 }}, {{ opacity: 1, scale: 1.0, duration: 0.25, ease: "power2.out" }}, s);
        tl.to("#w-" + id, {{ scale: 1.06, duration: d - 0.25, ease: "none" }}, s + 0.25);
      }});
      tl.fromTo("#w-cta", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {CTA}, ease: "none" }}, {TALK});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------------- captions ----------------
CAP = [
    ("A", 199.40, "Terus sign masa itu."), ("A", 200.90, "Buka file terus."), ("A", 203.30, "Tak sabar."),
    ("B", 173.95, "Saya dengan suami,"), ("B", 175.21, "tengoklah di Facebook,"), ("B", 177.00, "cari-cari kan."),
    ("C", 185.38, "Macam dia punya feedback tu, okey."),
    ("D1", 190.18, "Satu hari balik tu,"),
    ("D2", 192.38, "nak pergi dekat MI punya ofis."), ("D2", 196.10, "So nak tanyalah"), ("D2", 197.24, "macam mana buat tu kan."),
    ("E", 220.95, "Dah lah, kita sign teruslah,"), ("E", 222.56, "kita percayalah kontrak ni,"),
    ("E", 224.90, "sebab dia punya feedback semua okey."), ("E", 227.13, "So banyak dah buat rumah,"),
    ("E", 228.48, "dah siap kan."), ("E", 229.18, "Tak ada yang terbengkalai kan,"), ("E", 231.00, "so okey lah."),
    ("F", 232.00, "Maksudnya kita puas hati,"), ("F", 233.70, "rasa confident nak buat dengan MI lah."),
    ("G", 235.62, "Sebab tu terus sign dia."), ("G", 237.78, "Tak payah pergi survey lain tempat lagi."),
    ("H", 552.45, "So yang macam MI ni,"), ("H", 553.90, "dah banyak orang yang buat rumah dengan dia."),
    ("H", 556.38, "So semua macam berpuas hati."), ("H", 558.50, "So kita pilih Mahligai lah."),
]
HL = ["terus sign", "sign", "Facebook", "feedback", "MI punya ofis", "percayalah", "rumah", "dah siap", "terbengkalai",
      "puas hati", "confident", "survey", "berpuas hati", "Mahligai", "Tak sabar"]

def hl(text):
    marks = [0] * len(text)
    for h in sorted(HL, key=len, reverse=True):
        m = re.search(re.escape(h), text, flags=re.I)
        if m and not any(marks[m.start():m.end()]):
            for k in range(m.start(), m.end()): marks[k] = 1
    out, on = "", False
    for ch, mk in zip(text, marks):
        if mk and not on: out += '<span class="y">'; on = True
        if not mk and on: out += "</span>"; on = False
        out += ch
    return out + ("</span>" if on else "")

caps = []
for i, (sid, s, txt) in enumerate(CAP):
    seg = next(x for x in SEGS if x[0] == sid)
    nxt = [c[1] for c in CAP if c[0] == sid and c[1] > s]
    e = min(nxt) if nxt else seg[3]
    caps.append((src(sid, s), round(src(sid, e) - 0.03, 3), hl(txt)))

H, J = [], []
def el(h): H.append("    " + h)
def js(s): J.append("    " + s)
for i, (s, e, txt) in enumerate(caps):
    el(f'<div class="cw clip" id="cp{i}" data-start="{s}" data-duration="{round(e - s, 3)}"><div class="cap" id="ct{i}">{txt}</div></div>')
    js(f'tl.fromTo("#ct{i}", {{ opacity: 0, y: 12, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "power3.out" }}, {s});')

def badge(gid, s, e, icon, line1, line2=""):
    l2 = f'<div class="b2">{line2}</div>' if line2 else ""
    el(f'<div class="gw clip" id="{gid}" data-start="{s}" data-duration="{round(e - s, 2)}"><div class="badge" id="{gid}-b">'
       f'<div class="bi">{icon}</div><div><div class="b1">{line1}</div>{l2}</div></div></div>')
    js(f'tl.fromTo("#{gid}-b", {{ opacity: 0, y: -24, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, {s});')
    js(f'tl.fromTo("#{gid}-b .bi", {{ scale: 0.4, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, {round(s + 0.1, 2)});')
    js(f'tl.to("#{gid}-b", {{ opacity: 0, y: -16, duration: 0.22, ease: "power2.in" }}, {round(e - 0.22, 2)});')

FB = '<svg viewBox="0 0 48 48" width="62" height="62"><circle cx="24" cy="24" r="22" fill="#1877F2"/><path d="M26.6 38V25.8h4.1l.6-4.8h-4.7v-3c0-1.4.4-2.3 2.4-2.3h2.5v-4.3a33 33 0 0 0-3.7-.2c-3.6 0-6.1 2.2-6.1 6.3V21h-4.1v4.8h4.1V38z" fill="#fff"/></svg>'
PIN = '<svg viewBox="0 0 48 64" width="46" height="62"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="#FFC845"/><circle cx="24" cy="24" r="9" fill="#14161B"/></svg>'
BUB = '<svg viewBox="0 0 48 48" width="60" height="60" fill="none" stroke="#FFC845" stroke-width="3.6" stroke-linejoin="round"><path d="M6 9h36v24H20l-9 8v-8H6z"/><path d="M14 18h20M14 25h13" stroke-linecap="round"/></svg>'
HOUSE = '<svg viewBox="0 0 48 48" width="62" height="62" fill="none" stroke="#FFC845" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"><path d="M5 22 24 7l19 15"/><path d="M10 19v23h28V19"/><circle cx="34" cy="34" r="9" fill="#1FA34A" stroke="#fff" stroke-width="2.5"/><path d="M30 34l3 3 5-6" stroke="#fff" stroke-width="2.8"/></svg>'
STAR = '<svg viewBox="0 0 48 48" width="60" height="60"><path d="M24 4l6 13 14 1.5-10.5 9.5 3 14L24 35l-12.5 7 3-14L4 18.5 18 17z" fill="#FFC845"/></svg>'

badge("g-fb", src("B", 175.25), src("C", 185.38), FB, "KENAL DI", "FACEBOOK")
badge("g-fbk", src("C", 186.40), src("D1", 191.32), BUB, "FEEDBACK", "PELANGGAN")
badge("g-ofis", src("D2", 193.95), src("D2", 198.95), PIN, "DATANG KE", "OFIS")
badge("g-rumah", src("E", 227.10), src("E", 231.65), HOUSE, "BANYAK RUMAH", "DAH SIAP")
badge("g-yakin", src("F", 233.75), src("G", 237.0), STAR, "YAKIN", "PILIH MI")

# hook
el(f'<div class="gw clip" id="g-hook" data-start="0.05" data-duration="3.8"><div class="hk">'
   f'<div class="hk1" id="hk1">DATANG OFIS,</div><div class="hk2" id="hk2">TERUS SIGN?!</div></div></div>')
js('tl.fromTo("#hk1", { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "expo.out" }, 0.1);')
js('tl.fromTo("#hk2", { opacity: 0, scale: 1.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.4);')
js('tl.to("#g-hook", { opacity: 0, y: -20, duration: 0.25, ease: "power2.in" }, 3.6);')

# CTA
el(f'<div class="clip" id="g-cta" data-start="{TALK}" data-duration="{CTA}" style="position:absolute; inset:0">'
   f'<div class="ctabg" id="ctabg"></div><div class="ctaw"><img class="logo" id="cta-l" src="assets/img/logo.png" alt="" />'
   f'<div class="c1" id="cta1">Nak bina rumah atas<br><span class="y">tanah sendiri?</span></div>'
   f'<div class="c2" id="cta2">Jom konsultasi dengan<br><b>Mahligai Idaman</b></div></div></div>')
js(f'tl.fromTo("#ctabg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power1.out" }}, {TALK});')
js(f'tl.fromTo("#cta-l", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {round(TALK + 0.1, 2)});')
js(f'tl.fromTo("#cta1", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {round(TALK + 0.3, 2)});')
js(f'tl.fromTo("#cta2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {round(TALK + 0.85, 2)});')

CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: Poppins, sans-serif; color: #fff; }
    .y { color: #FFC845; }
    .cw { position: absolute; left: 80px; right: 80px; top: 1300px; display: flex; justify-content: center; }
    .cap { max-width: 920px; padding: 12px 28px 14px; border-radius: 20px; background: rgba(10,12,16,.58); text-align: center;
      font-weight: 800; font-size: 54px; line-height: 1.18; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.35); opacity: 0; }
    .gw { position: absolute; left: 80px; right: 80px; top: 300px; display: flex; justify-content: center; }
    .badge { display: flex; align-items: center; gap: 20px; padding: 16px 36px 18px 18px; border-radius: 24px; background: rgba(10,12,16,.72);
      border: 3px solid #FFC845; box-shadow: 0 16px 40px rgba(0,0,0,.35); opacity: 0; }
    .bi { width: 88px; height: 88px; border-radius: 20px; background: rgba(255,255,255,.08); display: flex; align-items: center; justify-content: center; flex: none; }
    .b1 { font-weight: 700; font-size: 32px; letter-spacing: .1em; color: #fff; line-height: 1.1; white-space: nowrap; }
    .b2 { font-weight: 800; font-size: 58px; line-height: 1.02; color: #FFC845; white-space: nowrap; text-shadow: 0 3px 10px rgba(0,0,0,.35); }
    .hk { text-align: center; padding: 22px 40px 28px; border-radius: 28px; background: rgba(10,12,16,.55); }
    .hk1, .hk2 { font-weight: 800; line-height: 1.02; white-space: nowrap; text-shadow: 0 5px 18px rgba(0,0,0,.4), 0 2px 4px rgba(0,0,0,.35); opacity: 0; }
    .hk1 { font-size: 92px; color: #fff; }
    .hk2 { font-size: 118px; color: #FFC845; }
    .ctabg { position: absolute; inset: 0; background: rgba(8,10,12,.62); opacity: 0; }
    .ctaw { position: absolute; left: 80px; right: 80px; top: 520px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 30px; }
    .logo { width: 230px; height: auto; filter: drop-shadow(0 8px 18px rgba(0,0,0,.45)); opacity: 0; }
    .c1 { font-weight: 800; font-size: 80px; line-height: 1.06; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.4); opacity: 0; }
    .c2 { padding: 18px 40px 22px; border-radius: 24px; background: #FFC845; color: #14161B; font-weight: 600; font-size: 44px; line-height: 1.2; opacity: 0;
      box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    .c2 b { font-weight: 800; font-size: 54px; }
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
print("TOTAL", TOTAL, start)
