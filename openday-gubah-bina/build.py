#!/usr/bin/env python3
"""Mahligai Idaman x Gubah Bina - Open Day paving block offer (1080x1920, 60 fps, ~51 s).
Overlays play at 1x or 0.5x only, so every output frame maps to a whole source frame (no judder).

The presenter take is trimmed of its silent lead-in, four empty pauses and the tail after "bye"
(SEGS, source seconds); every time below is written in SOURCE seconds and mapped with T(). Overlay footage from the Drive folder covers
the lines it illustrates (muted). The Open Day poster appears on "rujuk poster ni" and again as
the outro after "bye". Safe zone: top 15% (Y < 288) and bottom 20% (Y > 1536) carry nothing.
"""
import json, re

WHT, YEL, INK = "#FFFFFF", "#FFD54A", "#15171B"
SAFE_TOP, SAFE_BOT = 288, 1536
SEGS = [(1.52, 5.87), (6.02, 8.30), (8.61, 34.95), (35.17, 42.72), (42.87, 47.95)]
starts, t = [], 0.0
for a, b in SEGS:
    starts.append(round(t, 3)); t += b - a
TALK = round(t, 3)
OUTRO = 2.6
FILM = round(TALK + OUTRO, 2)


def T(src):
    """source second -> film second (inside a removed gap snaps to the next segment)"""
    for (a, b), st in zip(SEGS, starts):
        if src < a:
            return st
        if src <= b:
            return round(st + src - a, 3)
    return TALK

# overlays: (clip, film start, film end, media start, speed)
OV = [
    ("IMG_1937", 6.55, 8.30, 0.0, 0.5),    # "apa kata kita lengkapkan sekali" - paving pallets
    ("IMG_1884", 14.45, 16.35, 1.0, 1.0),   # "kerjasama dengan Gubah Bina" - Gubah Bina logo wall
    ("IMG_2083", 16.35, 17.40, 0.0, 0.5),  # signboard
    ("IMG_1885", 18.90, 20.40, 0.6, 1.0),   # "pemasangan paving block" - sample
    ("IMG_1886", 20.40, 21.60, 0.8, 1.0),   # sample shelves
    ("IMG_1894", 21.60, 23.00, 0.8, 1.0),   # hexagon sample
    ("IMG_1906", 23.00, 25.10, 0.5, 1.0),   # "melalui kerjasama ni, pelanggan MI" - consultation
    ("IMG_1902", 28.00, 30.00, 1.0, 1.0),   # "pemasangan paving block" - project photos
    ("IMG_1936", 30.00, 32.20, 1.0, 1.0),   # "halamannya lebih luas" - stock
    ("IMG_1898", 32.20, 33.55, 0.0, 1.0),   # display wall
    ("IMG_1907", 33.55, 34.95, 0.8, 1.0),   # "menarik serta lengkap" - catalogue
    ("IMG_1883", 43.00, 44.50, 0.0, 1.0),   # "MI x Gubah Bina" - logo
    ("IMG_1925", 44.50, 46.00, 0.5, 1.0),   # "jumpa anda dekat sana" - awards
]
vids = [f'      <video id="t{k}" class="clip full tal" src="assets/video/talent.mp4" data-start="{st}" data-duration="{round(b - a, 3)}" '
        f'data-media-start="{a}" data-track-index="1" playsinline data-has-audio="true" data-volume="1" data-fade-in="0.03" data-fade-out="0.03"></video>'
        for k, ((a, b), st) in enumerate(zip(SEGS, starts))]
OV = [(c, T(s), T(e), m, r) for c, s, e, m, r in OV]
for i, (c, s, e, m, r) in enumerate(OV):
    vids.append(f'      <div id="w{i}" class="bw"><video id="o{i}" class="clip full" src="assets/video/{c}.mp4" data-start="{s}" '
                f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-playback-rate="{r}" data-track-index="2" muted playsinline></video></div>')
# fade out only when the next overlay does not start right away (contiguous ones cross-fade)
push = [(i, s, round(e - s, 3), 0 if i + 1 < len(OV) and abs(OV[i + 1][1] - e) < 0.05 else 1) for i, (c, s, e, m, r) in enumerate(OV)]
talz = [(k, st, round(b - a, 3)) for k, ((a, b), st) in enumerate(zip(SEGS, starts))]

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{FILM}" data-track-index="7" data-volume="0.07" data-fade-out="1.5"></audio>']


def sfx(name, f, at, d, v, film=False):
    at = at if film else T(at)
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
          ]:
    sfx(*a)
sfx("out", "whoosh", TALK - 0.25, 0.57, 0.2, True); sfx("out2", "sparkle", TALK + 0.4, 1.6, 0.18, True)

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
      #wt {{ position: absolute; inset: 0; overflow: hidden; z-index: 1; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(12,14,18,.55) 0%, rgba(12,14,18,.35) 28%, rgba(12,14,18,0) 46%, rgba(12,14,18,0) 64%, rgba(12,14,18,.3) 82%, rgba(12,14,18,.38) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <div id="wt">
{chr(10).join(vids[:len(SEGS)])}
      </div>
{chr(10).join(vids[len(SEGS):])}
      <div id="shade" class="clip" data-start="0" data-duration="{TALK}"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{FILM}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // overlays: soft 0.3 s dissolve in (over the previous shot), slow push, dissolve out to the presenter
      {json.dumps(push)}.forEach(([i, s, d, fo]) => {{
        tl.fromTo("#w" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "sine.inOut" }}, s);
        tl.fromTo("#o" + i, {{ scale: 1.06 }}, {{ scale: 1.0, duration: d, ease: "none" }}, s);
        if (fo) tl.to("#w" + i, {{ opacity: 0, duration: 0.3, ease: "sine.inOut" }}, s + d - 0.3);
      }});
      // presenter segments alternate framing so each tightened cut reads as a camera move
      {json.dumps(talz)}.forEach(([k, s, d]) => {{
        const z = k % 2 ? 1.07 : 1.0;
        tl.fromTo("#t" + k, {{ scale: z }}, {{ scale: z + 0.03, duration: d, ease: "none" }}, s);
      }});
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
    s, e = T(s), T(e)
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
# Open Day info card (facts from the poster) before the poster itself
PIN = f'<svg viewBox="0 0 48 64" width="34" height="45"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
BOXES.append(("g7", 320, 1000))
H.append(f'''    <div class="grp clip" id="g7" data-start="{T(35.17)}" data-duration="{round(T(38.95) - T(35.17), 3)}" style="top:320px">
      <div class="hw" id="g7h" style="font-size:66px">JOM HADIR</div><div class="hy" id="g7y" style="font-size:92px">OPEN DAY 2026!</div>
      <div class="ic" id="g7a">{PIN}<div><div class="ict">GRAND RIVERVIEW HOTEL, KOTA BHARU</div><div class="icd">10 DISEMBER 2026 (KHAMIS)</div></div></div>
      <div class="ic" id="g7b">{PIN}<div><div class="ict">DUYONG MARINA &amp; RESORT, K. TERENGGANU</div><div class="icd">19 DISEMBER 2026 (SABTU)</div></div></div>
      <div class="ip" id="g7c">YURAN <b>RM49</b> · BOLEH BAWA PASANGAN · <b>100 SLOT</b> SETIAP LOKASI</div>
    </div>''')
tin("#g7h", T(35.17)); hide("#g7y"); tin("#g7y", T(35.4), "scale")
for sel, at in [("#g7a", 35.9), ("#g7b", 36.6), ("#g7c", 37.3)]:
    hide(sel); tin(sel, T(at), "up")
J.append(f'tl.to("#g7", {{ opacity: 0, duration: 0.2 }}, {T(38.75)});')
head("g8", 43.30, 46.00, "MAHLIGAI IDAMAN × GUBAH BINA", "JUMPA ANDA DI SANA!", 54, 96)

# poster on "rujuk poster ni" and as the outro
for pid, s, e in [("p1", T(38.95), T(42.95)), ("p2", round(TALK - 0.2, 3), FILM)]:
    H.append(f'    <div class="clip poster" id="{pid}" data-start="{s}" data-duration="{round(e - s, 3)}"><div class="pbg"></div>'
             f'<img class="pimg" id="{pid}i" src="assets/img/poster.jpg" alt="" /></div>')
    J.append(f'tl.fromTo("#{pid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {s});')
    J.append(f'tl.fromTo("#{pid}i", {{ scale: 1.12, y: 40 }}, {{ scale: 1.0, y: 0, duration: 0.7, ease: "expo.out" }}, {s});')
    J.append(f'tl.to("#{pid}i", {{ scale: 1.03, duration: {round(e - s - 0.7, 2)}, ease: "none" }}, {s + 0.7});')

# CTA on the outro poster
BOXES.append(("cta", 1400, 120))
H.append(f'    <div class="clip cta" id="cta" data-start="{TALK + 0.4}" data-duration="{round(FILM - TALK - 0.4, 3)}"><span>DAFTAR SEKARANG, SLOT TERHAD!</span></div>')
J.append(f'tl.fromTo("#cta", {{ opacity: 0, y: 30, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {TALK + 0.4});')
J.append(f'tl.fromTo("#cta span", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {TALK + 0.9});')

# subtitles: white text in a dark rounded box
WORDS = json.load(open("words.json")); WORDS = WORDS if isinstance(WORDS, list) else WORDS.get("words", WORDS)
SUBS = [
    (1.52, "Rumah dah siap cantik dah,"), (3.44, "tapi halaman tu kan macam kurang menyerlah."),
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
    e = SUBS[i + 1][0] if i + 1 < len(SUBS) else 47.95
    if s < 39.0 <= e: e = 38.95                         # no subtitle over the poster
    s, e = T(s), T(e)
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
    .ic {{ display: flex; align-items: center; gap: 16px; width: 960px; margin-top: 18px; padding: 18px 24px; border-radius: 16px; background: rgba(21,23,27,.86); border-left: 8px solid {YEL}; }}
    .ict {{ font-weight: 800; font-size: 34px; color: {WHT}; white-space: nowrap; }}
    .icd {{ font-weight: 900; font-size: 40px; color: {YEL}; margin-top: 4px; }}
    .ip {{ margin-top: 18px; padding: 14px 22px; border-radius: 999px; background: {YEL}; color: {INK}; font-weight: 800; font-size: 26px; white-space: nowrap; }}
    .ip b {{ font-weight: 900; }}
    .cta {{ position: absolute; left: 0; right: 0; top: 1400px; display: flex; justify-content: center; }}
    .cta span {{ display: inline-block; padding: 22px 44px; border-radius: 999px; background: {YEL}; color: {INK}; font-weight: 900; font-size: 46px; white-space: nowrap; box-shadow: 0 10px 30px rgba(0,0,0,.45); }}
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
