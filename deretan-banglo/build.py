#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman
"Deretan banglo - 1 lot terakhir, Kg Hutan Putih, Machang" video (1080x1920, 33 s).

The presenter take plays whole (no pauses worth cutting); B-roll from the Drive folder
sits on top, muted. Times are seconds of the take. Safe zone: top 15% (Y < 288) and
bottom 20% (Y > 1536) carry nothing.
"""
import json, re

WHT, YEL, INK = "#FFFFFF", "#F5C542", "#10151D"
SAFE_TOP, SAFE_BOT = 288, 1536
TOTAL = 33.15

# B-roll: (id, kind, file, start, end, media start)
BROLL = [
    ("b-row1", "video", "aerial-BB0FB1E8", 2.60, 5.20, 0.6),   # "tengoklah deretan ni, rumah-rumah"
    ("b-row2", "video", "aerial-5899E7BB", 5.20, 7.95, 0.5),   # "semuanya dibina di bawah MI"
    ("b-land", "video", "drone-0169", 12.40, 17.40, 0.5),      # "tanah ni berkeluasan 7,244"
    ("b-area", "video", "aerial-C51AA0CC", 17.40, 19.30, 2.0), # "lokasi juga strategik"
    ("b-map", "img", "lot-map", 19.30, 23.62, None),           # mosque / clinic / Bandar Machang on the verified map
    ("b-wide", "video", "aerial-D9D2F1E2", 23.62, 26.95, 0.0), # "boleh juga nak bina rumah ni"
]
vids = ['      <video id="v-tal" class="clip full" src="assets/video/talent.mp4" data-start="0" '
        f'data-duration="{TOTAL}" data-media-start="0" data-track-index="1" playsinline data-has-audio="true" data-volume="1"></video>']
for bid, kind, f, s, e, m in BROLL:
    if kind == "video":
        vids.append(f'      <div id="{bid}-w" class="bw"><video id="{bid}" class="clip full" src="assets/video/{f}.mp4" data-start="{s}" '
                    f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-track-index="2" muted playsinline></video></div>')
    else:
        vids.append(f'      <div id="{bid}-w" class="bw clip" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="2">'
                    f'<img id="{bid}" class="full" src="assets/img/{f}.jpg" alt="" /></div>')

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{TOTAL}" '
       f'data-track-index="4" data-volume="0.09" data-fade-out="1.2"></audio>']


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{5 + len(AUD) % 3}" data-volume="{v}"></audio>')


for a in [
    ("row1", "whoosh-short", 2.58, 0.57, 0.15), ("hd1", "pop", 2.75, 0.72, 0.14), ("row2", "whoosh-short", 5.18, 0.57, 0.13),
    ("lot", "whoosh", 7.93, 0.57, 0.16), ("lotimp", "impact-bass-1", 8.43, 1.6, 0.16),
    ("land", "whoosh-short", 12.38, 0.57, 0.13), ("n7244", "ping", 14.85, 1.0, 0.12),
    ("area", "whoosh-short", 17.38, 0.57, 0.13), ("strat", "pop", 17.50, 0.72, 0.14),
    ("masjid", "pop", 19.45, 0.72, 0.15), ("klinik", "pop", 20.65, 0.72, 0.15), ("bandar", "pop", 21.69, 0.72, 0.15),
    ("wide", "whoosh-short", 23.60, 0.57, 0.12), ("n1400", "ping", 25.92, 1.0, 0.12),
    ("cta", "whoosh", 28.75, 0.57, 0.15), ("cta2", "pop", 31.32, 0.72, 0.15),
]:
    sfx(*a)

push = [(b[0], b[3], b[4]) for b in BROLL]
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
      #w-tal {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 50% 45%; }}
      .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .bw {{ position: absolute; inset: 0; z-index: 2; overflow: hidden; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(12,18,28,.5) 0%, rgba(12,18,28,.32) 30%, rgba(12,18,28,0) 46%, rgba(12,18,28,0) 64%, rgba(12,18,28,.38) 80%, rgba(12,18,28,.45) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="w-tal">
{vids[0]}
      </div>
{chr(10).join(vids[1:])}
      <div id="shade"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(push)}.forEach(([id, s, e]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18, ease: "power1.out" }}, s);
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.08, duration: e - s, ease: "none" }}, s);
      }});
      // presenter is framed wide: open on a punch-in, slow push through, closer push on the CTA
      tl.fromTo("#w-tal", {{ scale: 1.25 }}, {{ scale: 1.12, duration: 2.6, ease: "power2.out" }}, 0);
      tl.fromTo("#w-tal", {{ scale: 1.12 }}, {{ scale: 1.3, duration: {round(TOTAL - 26.95, 2)}, ease: "sine.inOut", immediateRender: false }}, 26.95);
      tl.to("#root", {{ opacity: 0, duration: 0.4 }}, {TOTAL - 0.4});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

PIN = f'<svg viewBox="0 0 48 64" width="46" height="60"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.5):
    frm = {"up": "{ opacity: 0, y: 26 }", "scale": "{ opacity: 0, scale: 0.88 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def fit(text, size, k, maxw=860):
    lines = re.sub(r"<[^>]+>", "", text.replace("<br/>", "\n")).replace("&amp;", "&").split("\n")
    return int(min(size, maxw / (k * max(len(l) for l in lines))))


def head(hid, s, e, white, yellow, top=330, ysize=104, extra=""):
    BOXES.append((hid, top, 330))
    H.append(f'    <div class="grp clip" id="{hid}" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:{top}px">{extra}'
             f'<div class="hw" id="{hid}-w" style="font-size:{fit(white, 56, 0.66)}px">{white}</div>'
             f'<div class="hy" id="{hid}-y" style="font-size:{fit(yellow, ysize, 0.72)}px">{yellow}</div></div>')
    tin(f"#{hid}-w", s)
    J.append(f'tl.set("#{hid}-y", {{ opacity: 0 }}, 0);')
    tin(f"#{hid}-y", s + 0.2, "scale")
    J.append(f'tl.to("#{hid}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')


def count(sel, to, at, d=1.0):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, {at}); }})();')


# Scene 1: credibility over the bungalow aerials
head("g-row", 2.75, 7.95, "DERETAN BANGLO INI", "HASIL KERJA<br/>MAHLIGAI IDAMAN", ysize=96)

# Scene 2: 3D land map of the last lot (top-down drone photo, tilted, empty lot outlined)
k = 1080 / 1449
poly = [(450, 1010), (990, 1010), (990, 1540), (450, 1540)]
pts = " ".join(f"{round(x * k)},{round(y * k)}" for x, y in poly)
cx = round(sum(x for x, _ in poly) / 4 * k); cy = round(sum(y for _, y in poly) / 4 * k)
s3, e3 = 7.95, 12.40
H.append(f'''    <div class="clip scn3" id="s-lot3d" data-start="{s3}" data-duration="{round(e3 - s3, 3)}">
      <div class="tilt" id="tilt"><img src="assets/img/lot-top.jpg" alt="" />
        <svg class="lotsvg" viewBox="0 0 1080 1920" width="1080" height="1920">
          <polygon id="lotfill" points="{pts}" fill="{YEL}" fill-opacity="0.28"/>
          <polygon id="lotline" points="{pts}" fill="none" stroke="{YEL}" stroke-width="7" stroke-linejoin="round"/>
        </svg>
        <div class="lotpin" id="lotpin" style="left:{cx}px; top:{cy}px">LOT TERAKHIR</div>
      </div>
    </div>''')
J.append(f'tl.fromTo("#s-lot3d", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {s3});')
J.append(f'tl.fromTo("#tilt", {{ rotationX: 0, scale: 1.0, y: 0 }}, {{ rotationX: 42, scale: 1.32, y: -60, duration: 1.4, ease: "power2.inOut" }}, {s3 + 0.1});')
J.append(f'tl.to("#tilt", {{ rotationZ: -4, duration: {round(e3 - s3 - 1.5, 2)}, ease: "sine.inOut" }}, {s3 + 1.5});')
J.append(f'tl.fromTo("#lotline", {{ strokeDasharray: 1900, strokeDashoffset: 1900 }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }}, {s3 + 0.9});')
J.append(f'tl.fromTo("#lotfill", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {s3 + 1.6});')
J.append(f'tl.fromTo("#lotpin", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {s3 + 1.8});')
head("g-last", 8.43, 12.40, "TINGGAL", "1 LOT TERAKHIR!", ysize=100)

# Scene 3: land size
head("g-land", 12.60, 17.40, "KELUASAN TANAH", '<span id="n7244">7,244</span> KPS', ysize=124)
count("#n7244", 7244, 12.80, 1.2)

# Scene 4: location, then the three nearby points one by one on the verified map
head("g-loc", 17.50, 19.30, "LOKASI STRATEGIK", "KG HUTAN PUTIH, MACHANG", ysize=80)
BOXES.append(("near", 330, 150))
for i, (txt, at) in enumerate([("MASJID BERDEKATAN", 19.45), ("KLINIK BERDEKATAN", 20.65), ("BERHAMPIRAN<br/><em>BANDAR MACHANG</em>", 21.69)]):
    end = [20.65, 21.69, 23.62][i]
    H.append(f'    <div class="clip chip" id="ch{i}" data-start="{at}" data-duration="{round(end - at, 3)}">{PIN}<span>{txt}</span></div>')
    tin(f"#ch{i}", at, "up", 0.4)

# Scene 5: house size
head("g-1400", 25.16, 28.56, "BINA RUMAH BERMULA", '<span id="n1400">1,400</span> KPS', ysize=124)
count("#n1400", 1400, 25.36)

# Scene 6: CTA
head("g-cta", 28.77, TOTAL, "BERMINAT DENGAN LOT INI?", "HUBUNGI KAMI<br/>SEKARANG!", ysize=108)

# subtitles (user's CapCut transcript, checked against the audio)
SUBS = [
    (0.21, "**Mahligai Idaman** ni mana buat perumahan,"),
    (2.32, "tapi tengoklah deretan ni, rumah-rumah ni,"),
    (5.27, "semuanya adalah dibina di bawah **Mahligai Idaman**."),
    (7.95, "Tapi kita ada **satu lot terakhir** untuk tuan-puan"),
    (10.20, "yang nak bina rumah tapi tak dak tanah."),
    (12.44, "Kita ada tanah ni berkeluasan **7,244 kaki persegi**."),
    (17.47, "Lokasi juga adalah **strategik** lah."),
    (19.29, "Ada **masjid**,"),
    (20.42, "ada **klinik** dan juga berdekatan dengan **Bandar Machang**."),
    (23.62, "Boleh juga nak bina rumah ni"),
    (25.16, "berkeluasan **1,400 kaki persegi** ke atas lah."),
    (28.77, "Jadi, sesiapa yang berkenan dengan tanah ni,"),
    (31.32, "cepat-cepat **hubungi kami sekarang**."),
]
BOXES.append(("subs", 1350, 170))
cues = []
for i, (s, text) in enumerate(SUBS):
    fs = max(0.0, s - 0.05)
    fe = SUBS[i + 1][0] - 0.05 if i + 1 < len(SUBS) else TOTAL
    html = "".join(f"<b>{p}</b>" if j % 2 else p for j, p in enumerate(text.split("**")))
    cues.append(f'      <div class="cue clip" id="cue{i}" data-start="{round(fs, 3)}" data-duration="{round(fe - fs, 3)}"><span>{html}</span></div>')
    J.append(f'tl.fromTo("#cue{i} span", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.15, ease: "power2.out" }}, {round(fs, 3)});')
H.append('    <div class="subs" id="subs">\n' + "\n".join(cues) + '\n    </div>')

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

SH = "text-shadow: 0 3px 6px rgba(0,0,0,.5), 0 10px 28px rgba(0,0,0,.55);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 800; line-height: 1.04; white-space: nowrap; text-transform: uppercase; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; line-height: 1.0; letter-spacing: -.02em; white-space: nowrap; text-align: center; text-transform: uppercase; color: {YEL}; {SH} }}
    .scn3 {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; perspective: 1500px; }}
    .tilt {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 62%; transform-style: preserve-3d; }}
    .tilt img {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    .lotsvg {{ position: absolute; inset: 0; }}
    .lotpin {{ position: absolute; transform: translate(-50%, -50%) rotateX(-42deg); white-space: nowrap; font-weight: 900; font-size: 54px; color: {WHT}; {SH} }}
    .chip {{ position: absolute; left: 0; right: 0; top: 340px; display: flex; align-items: center; justify-content: center; gap: 16px; }}
    .chip span {{ font-weight: 800; font-size: 52px; color: {WHT}; white-space: nowrap; {SH} }}
    .chip span em {{ font-style: normal; color: {YEL}; }}
    .chip span {{ text-align: center; line-height: 1.08; }}
    .chip svg {{ filter: drop-shadow(0 4px 8px rgba(0,0,0,.5)); }}
    .subs {{ position: absolute; left: 60px; right: 60px; top: 1350px; height: 170px; }}
    .cue {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; text-align: center; }}
    .cue span {{ display: block; max-width: 940px; font-weight: 700; font-size: 46px; line-height: 1.22; color: {WHT};
      text-shadow: 0 2px 4px rgba(0,0,0,.75), 0 6px 18px rgba(0,0,0,.55); }}
    .cue b {{ color: {YEL}; font-weight: 800; }}
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
print("ok", TOTAL)
