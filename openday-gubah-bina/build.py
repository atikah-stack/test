#!/usr/bin/env python3
"""Mahligai Idaman x Gubah Bina - Open Day paving block offer (1080x1920, 30 fps, ~51 s).

The presenter take plays whole (no fillers to cut); overlay footage from the Drive folder covers
the lines it illustrates (muted). The Open Day poster appears on "rujuk poster ni" and again as
the outro after "bye". Safe zone: top 15% (Y < 288) and bottom 20% (Y > 1536) carry nothing.
"""
import json, re

WHT, YEL, INK = "#FFFFFF", "#FFD54A", "#15171B"
SAFE_TOP, SAFE_BOT = 288, 1536
TALK = 48.85
OUTRO = 2.6
FILM = round(TALK + OUTRO, 2)

# overlays: (clip, film start, film end, media start, speed)
OV = [
    ("IMG_1937", 6.55, 7.95, 0.0, 0.75),    # "apa kata kita lengkapkan sekali" - paving pallets
    ("IMG_1884", 14.45, 16.35, 1.0, 1.0),   # "kerjasama dengan Gubah Bina" - Gubah Bina logo wall
    ("IMG_2083", 16.35, 17.40, 0.0, 0.95),  # signboard
    ("IMG_1885", 18.90, 20.40, 0.6, 1.0),   # "pemasangan paving block" - sample
    ("IMG_1886", 20.40, 21.60, 0.8, 1.0),   # sample shelves
    ("IMG_1894", 21.60, 23.00, 0.8, 1.0),   # hexagon sample
    ("IMG_1906", 23.00, 25.10, 0.5, 1.0),   # "melalui kerjasama ni, pelanggan MI" - consultation
    ("IMG_1902", 28.00, 30.00, 1.0, 1.4),   # "pemasangan paving block" - project photos
    ("IMG_1936", 30.00, 32.20, 1.0, 1.3),   # "halamannya lebih luas" - stock
    ("IMG_1898", 32.20, 33.55, 0.0, 1.0),   # display wall
    ("IMG_1907", 33.55, 35.00, 0.8, 1.0),   # "menarik serta lengkap" - catalogue
    ("IMG_1883", 43.00, 44.50, 0.0, 1.0),   # "MI x Gubah Bina" - logo
    ("IMG_1925", 44.50, 46.00, 0.5, 1.0),   # "jumpa anda dekat sana" - awards
]
vids = [f'      <video id="tal" class="clip full" src="assets/video/talent.mp4" data-start="0" data-duration="{TALK}" data-media-start="0" '
        f'data-track-index="1" playsinline data-has-audio="true" data-volume="1" data-fade-out="0.2"></video>']
for i, (c, s, e, m, r) in enumerate(OV):
    vids.append(f'      <div id="w{i}" class="bw"><video id="o{i}" class="clip full" src="assets/video/{c}.mp4" data-start="{s}" '
                f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-playback-rate="{r}" data-track-index="2" muted playsinline></video></div>')
push = [(i, s, round(e - s, 3)) for i, (c, s, e, m, r) in enumerate(OV)]

AUD = []


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{4 + len(AUD) % 3}" data-volume="{v}"></audio>')


for a in [("hook", "impact-bass-1", 0.2, 1.6, 0.2), ("hk2", "pop", 1.6, 0.72, 0.18),
          ("o1", "whoosh-short", 6.5, 0.57, 0.15), ("od", "whoosh", 8.9, 0.57, 0.17), ("odp", "pop", 9.6, 0.72, 0.18),
          ("gb", "whoosh-short", 14.4, 0.57, 0.15), ("gbp", "impact-bass-2", 14.6, 2.0, 0.18),
          ("pv", "whoosh-short", 18.85, 0.57, 0.15), ("pvp", "pop", 19.4, 0.72, 0.17),
          ("hi", "whoosh", 26.8, 0.57, 0.17), ("hip", "impact-bass-1", 26.97, 1.6, 0.22),
          ("ls", "whoosh-short", 29.95, 0.57, 0.14), ("lsp", "pop", 32.65, 0.72, 0.16),
          ("jg", "whoosh", 35.2, 0.57, 0.16), ("jgp", "pop", 35.7, 0.72, 0.17),
          ("ps", "whoosh", 38.95, 0.57, 0.2), ("psp", "impact-bass-2", 39.1, 2.0, 0.18),
          ("x", "whoosh-short", 42.95, 0.57, 0.15), ("xp", "pop", 43.3, 0.72, 0.18),
          ("out", "whoosh", TALK - 0.25, 0.57, 0.2), ("out2", "sparkle", TALK + 0.4, 1.6, 0.18)]:
    sfx(*a)

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {INK}; }}
      .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .bw {{ position: absolute; inset: 0; overflow: hidden; z-index: 2; }}
      #tal {{ z-index: 1; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(12,14,18,.55) 0%, rgba(12,14,18,.35) 28%, rgba(12,14,18,0) 46%, rgba(12,14,18,0) 64%, rgba(12,14,18,.3) 82%, rgba(12,14,18,.38) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="shade" class="clip" data-start="0" data-duration="{TALK}"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{FILM}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(push)}.forEach(([i, s, d]) => {{
        tl.fromTo("#w" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, s);
        tl.fromTo("#o" + i, {{ scale: 1.0 }}, {{ scale: 1.07, duration: d, ease: "none" }}, s);
      }});
      tl.fromTo("#tal", {{ scale: 1.08 }}, {{ scale: 1.0, duration: 0.6, ease: "expo.out" }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.45):
    frm = {"up": "{ opacity: 0, y: 26 }", "scale": "{ opacity: 0, scale: 0.86 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def fit(text, size, k=0.62, maxw=920):
    lines = re.sub(r"<[^>]+>", "", text.replace("<br/>", "\n")).replace("&amp;", "&").split("\n")
    return int(min(size, maxw / (k * max(len(l) for l in lines))))


def head(gid, s, e, white, yellow, wsize=72, ysize=104, top=330, extra=""):
    BOXES.append((gid, top, 330))
    H.append(f'    <div class="grp clip" id="{gid}" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:{top}px">'
             f'<div class="hw" id="{gid}w" style="font-size:{fit(white, wsize)}px">{white}</div>'
             f'<div class="hy" id="{gid}y" style="font-size:{fit(yellow, ysize)}px">{yellow}</div>{extra}</div>')
    tin(f"#{gid}w", s); hide(f"#{gid}y"); tin(f"#{gid}y", s + 0.25, "scale")
    J.append(f'tl.to("#{gid}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')


head("g1", 0.20, 6.45, "RUMAH DAH SIAP,", "HALAMAN BELUM<br/>LENGKAP?", 80, 104)
head("g2", 9.55, 14.30, "OPEN DAY", "MAHLIGAI IDAMAN", 80, 100)
head("g3", 14.55, 18.80, "MAHLIGAI IDAMAN", "× GUBAH BINA", 70, 112)
head("g4", 19.30, 23.00, "PAKAR PEMASANGAN", "PAVING BLOCK", 70, 112)
head("g5", 26.90, 30.00, "HARGA ISTIMEWA", "UNTUK PELANGGAN MI", 80, 92)
head("g6", 32.60, 35.00, "HALAMAN LEBIH", "LUAS &amp; MENARIK", 80, 108)
head("g7", 35.55, 38.95, "JANGAN LEPASKAN", "PELUANG!", 76, 130)
head("g8", 43.30, 46.00, "MAHLIGAI IDAMAN × GUBAH BINA", "JUMPA ANDA DI SANA!", 54, 96)

# poster on "rujuk poster ni" and as the outro
for pid, s, e in [("p1", 38.95, 42.95), ("p2", TALK - 0.2, FILM)]:
    H.append(f'    <div class="clip poster" id="{pid}" data-start="{s}" data-duration="{round(e - s, 3)}"><div class="pbg"></div>'
             f'<img class="pimg" id="{pid}i" src="assets/img/poster.jpg" alt="" /></div>')
    J.append(f'tl.fromTo("#{pid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {s});')
    J.append(f'tl.fromTo("#{pid}i", {{ scale: 1.12, y: 40 }}, {{ scale: 1.0, y: 0, duration: 0.7, ease: "expo.out" }}, {s});')
    J.append(f'tl.to("#{pid}i", {{ scale: 1.03, duration: {round(e - s - 0.7, 2)}, ease: "none" }}, {s + 0.7});')

# subtitles: white text in a dark rounded box
WORDS = json.load(open("words.json")); WORDS = WORDS if isinstance(WORDS, list) else WORDS.get("words", WORDS)
SUBS = [
    (0.00, "Rumah dah siap cantik dah,"), (3.44, "tapi halaman tu kan macam kurang menyerlah."),
    (6.22, "Apa kata kita lengkapkan sekali?"), (8.00, "Bersempena dengan Open Day Mahligai Idaman,"),
    (11.11, "kami akan membawakan sesuatu yang istimewa buat pelanggan kami,"),
    (14.00, "yang mana Mahligai Idaman bakal menjalinkan kerjasama"), (17.00, "dengan Gubah Bina,"),
    (18.00, "iaitu pakar pemasangan paving block untuk halaman rumah anda."),
    (23.00, "Melalui kerjasama ni, pelanggan Mahligai Idaman"), (25.97, "bakal menikmati harga istimewa"),
    (28.01, "untuk pemasangan paving block."), (30.00, "Maka banglo tuan-puan semua,"),
    (31.89, "halamannya lebih luas, menarik serta lengkap."), (35.00, "Jadi jangan lepaskan peluang"),
    (36.75, "untuk hadir ke Open Day Mahligai Idaman."), (43.00, "Mahligai Idaman x Gubah Bina,"),
    (44.62, "jumpa anda dekat sana."), (46.00, "Bye!"),
]
BOXES.append(("subs", 1340, 180))
cues = []
for i, (s, t) in enumerate(SUBS):
    e = SUBS[i + 1][0] if i + 1 < len(SUBS) else TALK - 0.3
    if s < 39.0 <= e: e = 38.95                         # no subtitle over the poster
    cues.append(f'      <div class="cue clip" id="c{i}" data-start="{s}" data-duration="{round(e - s, 3)}"><span>{t}</span></div>')
    J.append(f'tl.fromTo("#c{i} span", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.14 }}, {s});')
H.append('    <div class="subs">\n' + "\n".join(cues) + '\n    </div>')

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

SH = "text-shadow: 0 2px 4px rgba(0,0,0,.35), 0 4px 18px rgba(0,0,0,.45);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 900; line-height: 1.02; letter-spacing: -.01em; text-align: center; white-space: nowrap; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; line-height: 1.0; letter-spacing: -.02em; text-align: center; white-space: nowrap; color: {YEL}; {SH} }}
    .poster {{ position: absolute; inset: 0; overflow: hidden; }}
    .pbg {{ position: absolute; inset: 0; background: {INK}; }}
    .pimg {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: contain; }}
    .subs {{ position: absolute; left: 70px; right: 70px; top: 1340px; height: 180px; }}
    .cue {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; text-align: center; }}
    .cue span {{ display: inline; font-weight: 700; font-size: 42px; line-height: 1.6; color: {WHT}; background: rgba(22,22,24,.86);
      padding: 8px 20px; border-radius: 12px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
'''
gfx = f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="gfx" data-width="1080" data-height="1920" data-duration="{FILM}">
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
print("film", FILM)
