#!/usr/bin/env python3
"""Testimonial 01: Peace of Mind — Mahligai Idaman. 9:16, 1080x1920, 30 fps.

Talent clips (from the raw 11:34 interview, burned-in captions wiped with delogo, audio cleaned):
  t1.mp4 = source 22.0-45.8 (neutral grade) · t2.mp4 = source 376.0-424.4 (warm grade)
Segments are in SOURCE seconds; src() converts to film time.
"""
import json, re

CLIP0 = {"t1": 22.0, "t2": 376.0}
SEGS = [
    ("S1", "t1", 39.12, 45.45),    # Kalau harga murah pun ... terus tak ada poin.
    ("S2a", "t1", 22.44, 27.98),   # Sebab kita duduk jauh. Nak balik, orang kata nak memantau
    ("S2b", "t1", 28.58, 31.70),   # perjalanan projek tu pun
    ("S2c", "t1", 32.45, 33.30),   # agak sukar.
    ("S3a", "t2", 376.24, 378.98), # Daripada start, kita nak
    ("S3b", "t2", 379.70, 381.95), # ukur tanah semua,
    ("S4a", "t2", 384.55, 385.82), # boleh katakan
    ("S4b", "t2", 386.45, 388.60), # Mahligai yang uruskan segala-galanya.
    ("S4c", "t2", 389.45, 390.90), # Jadi kita macam
    ("S4d", "t2", 391.60, 393.60), # tenang. Tak payah nak fikir apa.
    ("S5", "t2", 404.80, 417.55),  # Kita cuma tenang ... Benda-benda tu semua tak ada.
    ("S6a", "t2", 417.90, 419.70), # Jadi memang orang kata
    ("S6b", "t2", 420.15, 424.00), # pilihan tu tepat. Alhamdulillah, pilihan tu tepat.
]
start, t = {}, 0.0
for sid, c, a, b in SEGS:
    start[sid] = round(t, 3); t += b - a
TALK = round(t, 3)
HOLD, OUTRO = 1.6, 1.6
TOTAL = round(TALK + HOLD + OUTRO, 3)

def src(sid, s):
    _, c, a, b = next(x for x in SEGS if x[0] == sid)
    return round(start[sid] + s - a, 3)

# B-roll over the talent audio: id, file, film start, dur, media start
BROLL = [
    ("r-dji", "b-dji", src("S2a", 26.40), 2.55, 0.0),         # "nak memantau" — site from above
    ("r-b1", "img:build-1", src("S2b", 28.58) - 0.1, 3.3, 0),  # construction site, pavers
    ("r-dji2", "b-dji", src("S3b", 379.70), 2.25, 0.3),       # "ukur tanah semua"
    ("r-b2", "img:build-2", src("S4b", 386.45), 2.15, 0),     # "Mahligai yang uruskan segala-galanya" — build in progress
    ("r-key", "b-7124", src("S4c", 389.45), 3.45, 4.0),       # handover: "Jadi kita macam tenang"
    ("r-liv", "b-3534", src("S5", 406.30), 2.3, 0.6),         # living room
    ("r-din", "b-3615", src("S5", 408.60), 2.0, 0.4),         # dining / living
    ("r-kit", "b-3580", src("S5", 410.60), 2.4, 1.0),         # kitchen in daylight
    ("r-kit2", "b-3787", src("S5", 413.00), 2.2, 2.0),        # kitchen cabinets, warm light
    ("r-ext", "b-3753", src("S5", 415.20), 2.35, 0.6),        # porch exterior
    ("r-hero", "b-94beb817", src("S6b", 420.15) + 0.35, 3.05, 0.2),  # drone hero
]
HERO2 = ("r-hero2", "b-f371ec91", TALK, 3.05, 0.0)  # runs to the end          # strongest wide shot into the outro

def vtag(rid, f, s, d, m, z, extra=""):
    if f.startswith("img:"):
        return (f'      <div class="vw br" id="w-{rid}" style="z-index:{z}"><img id="v-{rid}" class="clip" src="assets/img/{f[4:]}.jpg" alt="" '
                f'data-start="{round(s, 3)}" data-duration="{d}" data-track-index="2" /></div>')
    return (f'      <div class="vw br" id="w-{rid}" style="z-index:{z}"><video id="v-{rid}" class="clip" src="assets/video/{f}.mp4" '
            f'data-start="{round(s, 3)}" data-duration="{d}" data-media-start="{m}" data-track-index="2" muted playsinline{extra}></video></div>')

V = []
for sid, c, a, b in SEGS:
    V.append(f'      <div class="vw" id="w-{sid}"><video id="v-{sid}" class="clip" src="assets/video/{c}.mp4" data-start="{start[sid]}" '
             f'data-duration="{round(b - a, 3)}" data-media-start="{round(a - CLIP0[c], 3)}" data-track-index="1" playsinline '
             f'data-has-audio="true" data-volume="1" data-fade-in="0.03" data-fade-out="0.05"></video></div>')
for rid, f, s, d, m in BROLL:
    V.append(vtag(rid, f, s, d, m, 2))
V.append(vtag(*HERO2, 2))

SFX = []
def sfx(n, f, at, d, v, extra=""):
    SFX.append(f'      <audio id="sx-{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" data-duration="{d}" '
               f'data-track-index="{5 + len(SFX) % 3}" data-volume="{v}"{extra}></audio>')

sfx("hook", "impact-bass-1", 0.12, 1.8, 0.32)
sfx("pom", "whoosh-short", 3.4, 0.57, 0.14)
sfx("jauh", "whoosh-short", src("S2a", 22.44) + 0.15, 0.57, 0.14)
sfx("q1", "click-soft", src("S2a", 26.40) + 0.3, 0.36, 0.16)
for i, tt in enumerate([src("S3b", 379.75), src("S4a", 385.0), src("S4b", 386.6), src("S4c", 389.6)]):
    sfx(f"tick{i}", "click-soft", tt, 0.36, 0.18)
sfx("rise", "riser", src("S4b", 386.45) - 0.3, 2.2, 0.12, ' data-media-start="1.2" data-fade-out="0.4"')
sfx("q2", "click-soft", src("S5", 411.98), 0.36, 0.16)
sfx("strike", "whoosh-short", src("S5", 414.68), 0.57, 0.12)
sfx("peace", "sparkle", src("S5", 415.2), 1.4, 0.1)
sfx("hero", "whoosh", src("S6b", 420.15) + 0.3, 0.57, 0.16)
sfx("swell", "chime", TALK + 0.2, 1.2, 0.08)

MUSIC = '''      <audio id="mu-a" class="clip" src="assets/audio/music.mp3" data-start="0" data-duration="{talk}" data-media-start="0" data-track-index="9" data-volume="0.13" data-fade-in="0.6"></audio>
      <audio id="mu-b" class="clip" src="assets/audio/music.mp3" data-start="{talk}" data-duration="{tail}" data-media-start="{talk}" data-track-index="9" data-volume="0.42" data-fade-in="0.25" data-fade-out="1.2"></audio>'''.format(
    talk=TALK, tail=round(TOTAL - TALK, 3))

PUSH = []
# talent shots are punched in ~1.5x from the top so the wiped burned-in caption band (y 1415-1605) sits below the frame
for k, (sid, c, a, b) in enumerate(SEGS):
    s0 = 1.48 if k % 2 == 0 else 1.56
    if sid == "S1":
        PUSH.append((sid, start[sid], 0.5, 1.62, 1.5, "expo.out"))
        PUSH.append((sid, start[sid] + 0.5, round(b - a - 0.5, 3), 1.5, 1.55, "none"))
    else:
        PUSH.append((sid, start[sid], round(b - a, 3), s0, s0 + 0.03, "none"))

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0c0d0f; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #0c0d0f; }}
      .vw {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 520px 1500px; }}
      .vw.br {{ transform-origin: 50% 50%; }}
      .vw video, .vw img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; display: block; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(V)}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{MUSIC}
{chr(10).join(SFX)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(PUSH)}.forEach(([id, s, d, a, b, e]) => tl.fromTo("#w-" + id, {{ scale: a, transformOrigin: "540px 400px" }}, {{ scale: b, transformOrigin: "540px 400px", duration: d, ease: e, immediateRender: false }}, s));
      {json.dumps([(r[0], round(r[2], 3), r[3]) for r in BROLL + [HERO2]])}.forEach(([id, s, d]) => {{
        tl.fromTo("#w-" + id, {{ opacity: 0, scale: 1.05 }}, {{ opacity: 1, scale: 1.0, duration: 0.3, ease: "power2.out" }}, s);
        tl.to("#w-" + id, {{ scale: 1.07, duration: d - 0.3, ease: "none" }}, s + 0.3);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------------- captions ----------------
CAP = [
    ("S1", 39.14, "Kalau harga murah pun,"), ("S1", 40.55, "tapi kita tak ada ketenangan,"),
    ("S1", 42.24, "tak ada peace of mind,"), ("S1", 43.38, "terus tak ada poin."),
    ("S2a", 22.44, "Sebab kita duduk jauh."), ("S2a", 24.45, "Nak balik, orang kata"), ("S2a", 26.66, "nak memantau"),
    ("S2b", 28.58, "perjalanan projek tu pun"), ("S2c", 32.45, "agak sukar."),
    ("S3a", 376.24, "Daripada start, kita nak"), ("S3b", 379.75, "ukur tanah semua,"),
    ("S4a", 384.59, "boleh katakan"), ("S4b", 386.52, "Mahligai yang uruskan segala-galanya."),
    ("S4c", 389.49, "Jadi kita macam"), ("S4d", 391.67, "tenang. Tak payah nak fikir apa."),
    ("S5", 404.91, "Kita cuma tenang."), ("S5", 406.30, "Tak ada kerisauan kata,"),
    ("S5", 410.23, "“Eh, ni dah siap ke kat sini,"), ("S5", 411.98, "dah sampai stage mana” semua."),
    ("S5", 414.68, "Benda-benda tu semua tak ada."),
    ("S6a", 417.98, "Jadi memang orang kata"), ("S6b", 420.22, "pilihan tu tepat."), ("S6b", 422.31, "Alhamdulillah, pilihan tu tepat."),
]
HL = ["harga murah", "ketenangan", "peace of mind", "duduk jauh", "memantau", "agak sukar", "ukur tanah", "Mahligai", "uruskan",
      "tenang", "stage", "tak ada", "pilihan tu tepat"]

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
for sid, s, txt in CAP:
    seg = next(x for x in SEGS if x[0] == sid)
    nxt = [c[1] for c in CAP if c[0] == sid and c[1] > s]
    e = min(nxt) if nxt else seg[3]
    caps.append((src(sid, s), round(src(sid, e) - 0.03, 3), txt))
# hold the last line of a segment over the next segment's start if the gap is a micro-cut
for i in range(len(caps) - 1):
    if caps[i + 1][0] - caps[i][1] < 0.2:
        caps[i] = (caps[i][0], round(caps[i + 1][0] - 0.02, 3), caps[i][2])

def srt_t(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
with open("testimonial-01-peace-of-mind.srt", "w") as f:
    for i, (s, e, txt) in enumerate(caps, 1):
        f.write(f"{i}\n{srt_t(s)} --> {srt_t(e)}\n{txt}\n\n")

H, J = [], []
def el(h): H.append("    " + h)
def js(s): J.append("    " + s)
for i, (s, e, txt) in enumerate(caps):
    el(f'<div class="cw clip" id="cp{i}" data-start="{s}" data-duration="{round(e - s, 3)}"><div class="cap" id="ct{i}"><div class="cin">{hl(txt)}</div></div></div>')
    js(f'tl.fromTo("#ct{i}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {s});')

def kin(gid, s, e, l1, l2="", top=330, size2=108):
    l2h = f'<div class="k2" id="{gid}-2" style="font-size:{size2}px">{l2}</div>' if l2 else ""
    el(f'<div class="gw clip" id="{gid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px">'
       f'<div class="k1" id="{gid}-1">{l1}</div>{l2h}</div>')
    js(f'tl.fromTo("#{gid}-1", {{ opacity: 0, y: 40, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "expo.out" }}, {round(s + 0.05, 3)});')
    if l2:
        js(f'tl.fromTo("#{gid}-2", {{ opacity: 0, scale: 1.3, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, {round(s + 0.28, 3)});')
    js(f'tl.to("#{gid}", {{ opacity: 0, y: -18, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')

# Scene 1 — hook headline, then PEACE OF MIND as he says it
kin("g-hook", 0.1, 3.35, "BINA RUMAH DARI JAUH,", "TAPI LANGSUNG<br>TAK RISAU!", top=280, size2=104)
kin("g-pom1", src("S1", 42.55), src("S1", 45.45), "TAK ADA", "PEACE OF MIND", top=330, size2=112)

# Scene 2 — distance visualisation on "Sebab kita duduk jauh"
s, e = src("S2a", 22.44), src("S2a", 26.40)
el(f'<div class="gw clip" id="g-dist" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:280px">'
   '<div class="k2" id="dj" style="font-size:104px">DUDUK JAUH</div>'
   '<svg id="dmap" viewBox="0 0 760 230" width="760" height="230">'
   '<path id="droute" d="M120 140 C 260 40, 500 40, 640 140" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 18"/>'
   '<g id="dpa"><circle cx="120" cy="140" r="44" fill="rgba(10,12,16,.65)" stroke="#FFD230" stroke-width="4"/>'
   '<path d="M98 146 120 128l22 18M104 143v18h32v-18" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></g>'
   '<g id="dpb"><circle cx="640" cy="140" r="44" fill="rgba(10,12,16,.65)" stroke="#FFD230" stroke-width="4"/>'
   '<path d="M618 160h44M624 160v-22h32v22M624 138l16-14 16 14" fill="none" stroke="#FFD230" stroke-width="5" stroke-linejoin="round"/></g>'
   '<text x="120" y="218" text-anchor="middle" class="dl">ANDA</text><text x="640" y="218" text-anchor="middle" class="dl">TAPAK RUMAH</text></svg></div>')
js(f'tl.fromTo("#dj", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {round(s + 0.1, 3)});')
js(f'tl.fromTo("#dpa", {{ opacity: 0, scale: 0.4, transformOrigin: "120px 140px" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {round(s + 0.5, 3)});')
js(f'tl.fromTo("#droute", {{ strokeDashoffset: 600, opacity: 0 }}, {{ strokeDashoffset: 0, opacity: 1, duration: 1.4, ease: "power2.inOut" }}, {round(s + 0.8, 3)});')
js(f'tl.fromTo("#dpb", {{ opacity: 0, scale: 0.4, transformOrigin: "640px 140px" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {round(s + 1.9, 3)});')
js(f'tl.fromTo("#g-dist svg text", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(s + 2.1, 3)});')
js(f'tl.to("#g-dist", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')

# Scene 2 — pain point
def ask(gid, s, e, text, strike_at=None):
    el(f'<div class="gw clip" id="{gid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:360px">'
       f'<div class="q" id="{gid}-q"><span class="qm">?</span><span class="qt">{text}<i class="st" id="{gid}-st"></i></span></div></div>')
    js(f'tl.fromTo("#{gid}-q", {{ opacity: 0, y: 30, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "expo.out" }}, {round(s, 3)});')
    if strike_at:
        js(f'tl.fromTo("#{gid}-st", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power3.inOut" }}, {round(strike_at, 3)});')
        js(f'tl.to("#{gid}-q", {{ opacity: 0.55, duration: 0.3 }}, {round(strike_at + 0.3, 3)});')
    js(f'tl.to("#{gid}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')

ask("g-q1", src("S2a", 26.66), src("S2c", 33.30) - 0.05, "MACAM MANA NAK<br>PANTAU PROGRES?")

# Scenes 3–4 — construction journey timeline
STEPS = [("UKUR TANAH", src("S3b", 379.75)), ("REKA BENTUK", src("S4a", 385.0)), ("PEMBINAAN", src("S4b", 386.6)), ("SERAHAN KUNCI", src("S4c", 389.6))]
ICON = [
    '<path d="M6 30h36M10 30V18m8 12V22m8 8V18m8 12V22m6 8V18" stroke-linecap="round"/>',
    '<path d="M8 40 30 18l6 6-22 22H8z M28 20l8-8 6 6-8 8" stroke-linejoin="round"/>',
    '<path d="M6 40h36M10 40V22h28v18M16 22v-8h16v8M20 30h8" stroke-linejoin="round"/>',
    '<circle cx="16" cy="24" r="8"/><path d="M24 24h18m-6 0v7m-6-7v5" stroke-linecap="round"/>',
]
s, e = src("S3b", 379.40), src("S4d", 393.6)
steps_html = "".join(
    f'<div class="st-item" id="stp{i}"><div class="st-ic"><svg viewBox="0 0 48 48" width="50" height="50" fill="none" stroke="#FFD230" stroke-width="3.4">{ICON[i]}</svg>'
    f'<div class="st-ok" id="ok{i}"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12.5 10 17 19 7" fill="none" stroke="#14161B" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>'
    f'<div class="st-lb">{n}</div></div>' for i, (n, _) in enumerate(STEPS))
el(f'<div class="gw clip" id="g-time" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:300px">'
   f'<div class="tl"><div class="tl-line"><div class="tl-fill" id="tlf"></div></div>{steps_html}</div></div>')
js(f'tl.fromTo("#g-time .tl", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {s});')
for i, (_, tt) in enumerate(STEPS):
    js(f'tl.fromTo("#stp{i}", {{ opacity: 0.28 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {round(tt, 3)});')
    js(f'tl.fromTo("#stp{i} .st-ic", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(tt, 3)});')
    js(f'tl.fromTo("#ok{i}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {round(tt + 0.2, 3)});')
    js(f'tl.to("#tlf", {{ scaleX: {round(i / 3, 3)}, duration: 0.4, ease: "power2.out" }}, {round(tt, 3)});')
js(f'tl.set("#tlf", {{ scaleX: 0 }}, 0);')
js(f'tl.to("#g-time", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')
kin("g-urus", src("S4b", 386.55), src("S4b", 388.6) - 0.02, "MAHLIGAI", "URUSKAN", top=760, size2=118)

# Scene 5 — pain point crossed out, then PEACE OF MIND
ask("g-q2", src("S5", 410.2), src("S5", 415.3), "DAH SAMPAI<br>STAGE MANA?", strike_at=src("S5", 414.7))
s, e = src("S5", 415.35), src("S6a", 417.90) + 0.05
el(f'<div class="gw clip" id="g-pom2" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:560px">'
   '<div class="pm" id="pm1">PEACE OF MIND</div><div class="pmr" id="pmr"></div>'
   '<div class="pms" id="pm2">Ketenangan sepanjang perjalanan membina rumah.</div></div>')
js(f'tl.fromTo("#pm1", {{ opacity: 0, scaleX: 1.22, filter: "blur(8px)" }}, {{ opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 1.4, ease: "power3.out" }}, {round(s + 0.05, 3)});')
js(f'tl.fromTo("#pmr", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.inOut" }}, {round(s + 0.5, 3)});')
js(f'tl.fromTo("#pm2", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }}, {round(s + 0.8, 3)});')
js(f'tl.to("#g-pom2", {{ opacity: 0, duration: 0.3, ease: "power1.in" }}, {round(e - 0.3, 3)});')

# Scene 6 — the choice
kin("g-tepat", src("S6b", 420.2), TALK + HOLD - 0.1, "PILIHAN", "YANG TEPAT", top=360, size2=118)

# Scene 7 — logo only over the drone hero, then fade to black
s = TALK + HOLD
el(f'<div class="clip" id="g-out" data-start="{round(s - 0.2, 3)}" data-duration="{round(TOTAL - s + 0.2, 3)}" style="position:absolute; inset:0">'
   '<div class="ow"><img class="ologo" id="olg" src="assets/img/logo.png" alt="" /></div><div class="obg" id="obg"></div></div>')
js(f'tl.fromTo("#olg", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }}, {round(s - 0.2, 3)});')
js(f'tl.fromTo("#obg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power1.in" }}, {round(TOTAL - 0.5, 3)});')

CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: #fff; }
    .y { color: #FFD230; }
    .cw { position: absolute; left: 90px; right: 150px; top: 1395px; display: flex; justify-content: center; }
    .cap { width: 840px; min-height: 130px; display: flex; align-items: center; justify-content: center; padding: 0 20px;
      text-align: center; font-weight: 800; font-size: 54px; line-height: 1.16; color: #fff;
      -webkit-text-stroke: 1.5px rgba(0,0,0,.55); paint-order: stroke fill;
      text-shadow: 0 3px 0 rgba(0,0,0,.45), 0 4px 16px rgba(0,0,0,.65), 0 0 2px rgba(0,0,0,.8); opacity: 0; }
    .gw { position: absolute; left: 90px; right: 150px; display: flex; flex-direction: column; align-items: center; text-align: center; }
    .k1 { font-weight: 800; font-size: 62px; line-height: 1.04; color: #fff; white-space: nowrap; letter-spacing: .01em;
      text-shadow: 0 5px 18px rgba(0,0,0,.5), 0 2px 4px rgba(0,0,0,.4); opacity: 0; }
    .k2 { font-weight: 800; line-height: 1.0; color: #FFD230; white-space: nowrap; letter-spacing: .005em;
      text-shadow: 0 6px 22px rgba(0,0,0,.55), 0 2px 5px rgba(0,0,0,.45); opacity: 0; }
    .dl { font-family: Montserrat, sans-serif; font-weight: 800; font-size: 26px; letter-spacing: .14em; fill: #fff; }
    #dmap { margin-top: 14px; overflow: visible; filter: drop-shadow(0 4px 10px rgba(0,0,0,.45)); }
    .q { display: flex; align-items: center; gap: 22px; padding: 22px 40px 24px 24px; border-radius: 26px; background: rgba(10,12,16,.6);
      border: 3px solid rgba(255,210,48,.9); opacity: 0; }
    .qm { width: 84px; height: 84px; border-radius: 50%; background: #FFD230; color: #14161B; font-weight: 800; font-size: 60px; line-height: 84px; flex: none; }
    .qt { position: relative; font-weight: 800; font-size: 54px; line-height: 1.1; text-align: left; color: #fff; white-space: nowrap; }
    .st { position: absolute; left: -6px; right: -6px; top: 50%; height: 8px; margin-top: -4px; background: #FFD230; border-radius: 4px;
      transform: scaleX(0); transform-origin: 0 50%; }
    .tl { position: relative; width: 840px; display: flex; justify-content: space-between; opacity: 0; }
    .tl-line { position: absolute; left: 100px; right: 100px; top: 46px; height: 4px; background: rgba(255,255,255,.35); border-radius: 2px; }
    .tl-fill { position: absolute; inset: 0; background: #FFD230; transform-origin: 0 50%; border-radius: 2px; }
    .st-item { position: relative; width: 200px; display: flex; flex-direction: column; align-items: center; gap: 12px; opacity: 0.28; }
    .st-ic { position: relative; width: 96px; height: 96px; border-radius: 50%; background: rgba(10,12,16,.75); border: 3px solid #FFD230;
      display: flex; align-items: center; justify-content: center; }
    .st-ok { position: absolute; right: -6px; bottom: -6px; width: 36px; height: 36px; border-radius: 50%; background: #FFD230;
      display: flex; align-items: center; justify-content: center; opacity: 0; }
    .st-lb { font-weight: 800; font-size: 22px; letter-spacing: .03em; color: #fff; white-space: nowrap; text-shadow: 0 3px 10px rgba(0,0,0,.6); }
    .pm { font-weight: 800; font-size: 92px; letter-spacing: .12em; color: #FFD230; white-space: nowrap;
      text-shadow: 0 6px 24px rgba(0,0,0,.55), 0 2px 5px rgba(0,0,0,.45); opacity: 0; }
    .pmr { width: 560px; height: 3px; margin: 18px 0 16px; background: rgba(255,255,255,.85); transform: scaleX(0); }
    .pms { font-weight: 600; font-size: 36px; color: #fff; letter-spacing: .03em; text-shadow: 0 3px 12px rgba(0,0,0,.6); opacity: 0; }
    .obg { position: absolute; inset: 0; background: #000; opacity: 0; }
    .ow { position: absolute; left: 90px; right: 150px; top: 330px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 22px; }
    .ologo { width: 230px; height: auto; opacity: 0; filter: drop-shadow(0 6px 16px rgba(0,0,0,.55)); }
    .o1 { letter-spacing: .06em; font-weight: 800; font-size: 50px; color: #fff; white-space: nowrap; opacity: 0; }
    .o2 { letter-spacing: .06em; font-weight: 800; font-size: 50px; color: #FFD230; white-space: nowrap; opacity: 0; }
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
print("TOTAL", TOTAL, "TALK", TALK)
print(json.dumps(start))
