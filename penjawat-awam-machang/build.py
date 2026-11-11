#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman
"Penjawat awam - 1 lot terakhir, Kg Hutan Putih, Machang" video (1080x1920).

Presenter (Aisyah) is the storyteller; her take is cut into segments (a repeated
"tuan-puan", the "ha deh, pas tu sini kan" filler and "sekarang lagilah" removed).
All times below are SOURCE seconds of her take, mapped to film time with T().
B-roll from the two Google Drive folders sits on top, muted.
Safe zone: top 15% (Y < 288) and bottom 20% (Y > 1536) carry nothing.
"""
import json

WHT, YEL, INK = "#FFFFFF", "#F5C542", "#10151D"
SAFE_TOP, SAFE_BOT = 288, 1536

SEGS = [(0.05, 14.00), (14.88, 31.40), (34.03, 44.19), (44.94, 74.98)]
starts, t = [], 0.0
for a, b in SEGS:
    starts.append(round(t, 3)); t += b - a
TOTAL = round(t, 3)


def T(src):
    for (a, b), st in zip(SEGS, starts):
        if src < a:
            return st
        if src <= b:
            return round(st + src - a, 3)
    return TOTAL


vids = []
for k, ((a, b), st) in enumerate(zip(SEGS, starts)):
    vids.append(f'      <video id="v{k}" class="clip tal" src="assets/video/talent.mp4" data-start="{st}" data-duration="{round(b - a, 3)}" '
                f'data-media-start="{a}" data-track-index="1" playsinline data-has-audio="true" data-volume="1" '
                f'data-fade-in="0.03" data-fade-out="0.03"></video>')

# B-roll: (id, kind, file, film start, film end, media start)
BROLL = [
    ("b-lot", "video", "drone-0169", T(8.50), T(12.00), 0.3),          # "tinggal satu lot ni jah, 4 km"
    ("b-loc", "video", "aerial-C51AA0CC", T(14.88), T(19.15), 1.5),     # covers the cut; "tanah dia ... sedia untuk bina rumah"
    ("b-wide", "video", "aerial-D9D2F1E2", T(19.15), T(22.10), 0.0),    # "pakej bina rumah berserta dengan tanah"
    ("b-lot2", "video", "drone-0169", T(22.10), T(25.95), 4.0),         # "keluasan lot ni ... 7,244"
    ("b-map", "img", "lot-map", T(25.95), T(27.05), None),              # the verified lot map (red boundary, 7,244 KPS)
    ("b-town", "img", "aerial-town", T(31.00), T(38.20), None),         # covers the cut; "strategik, dekat Bandar Machang"
    ("b-road", "video", "road", T(38.20), T(40.60), 5.0),               # "rezab jalan"
    ("b-drain", "img", "drain", T(40.60), T(44.10), None),              # "sistem aliran longkang" (covers the cut)
    ("b-nb1", "video", "aerial-5899E7BB", T(46.10), T(49.00), 0.8),     # "untuk siapa-siapa beli tanah ni ... jackpot"
    ("b-nb2", "video", "aerial-BB0FB1E8", T(55.15), T(59.95), 0.8),     # "semuanya rumah telah siap dibina oleh MI"
]
for bid, kind, f, s, e, m in BROLL:
    if kind == "video":
        vids.append(f'      <div id="{bid}-w" class="bw"><video id="{bid}" class="clip full" src="assets/video/{f}.mp4" data-start="{s}" '
                    f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-track-index="2" muted playsinline></video></div>')
    else:
        vids.append(f'      <div id="{bid}-w" class="bw clip" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="2">'
                    f'<img id="{bid}" class="full {"contain" if f == "lot-map" else ""}" src="assets/img/{f}.jpg" alt="" /></div>')

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{TOTAL}" '
       f'data-track-index="4" data-volume="0.09" data-fade-out="1.5"></audio>']


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{5 + len(AUD) % 3}" data-volume="{v}"></audio>')


for name, f, src, d, v in [
    ("h1", "whoosh-short", 0.40, 0.57, 0.15), ("h2", "pop", 4.70, 0.72, 0.14),
    ("lot", "whoosh-short", 8.48, 0.57, 0.15), ("lot2", "impact-bass-1", 8.60, 1.6, 0.16),
    ("loc", "whoosh-short", 14.86, 0.57, 0.14), ("pin", "pop", 15.10, 0.72, 0.15),
    ("wide", "whoosh-short", 19.13, 0.57, 0.12), ("land", "whoosh", 22.08, 0.57, 0.14), ("n7244", "ping", 24.64, 1.0, 0.12),
    ("map", "whoosh-short", 25.93, 0.57, 0.12), ("n1400", "pop", 27.10, 0.72, 0.15),
    ("town", "whoosh-short", 30.98, 0.57, 0.13), ("strat", "pop", 34.60, 0.72, 0.14),
    ("road", "whoosh-short", 38.18, 0.57, 0.13), ("kemudahan", "pop", 40.64, 0.72, 0.15),
    ("nb", "whoosh-short", 46.08, 0.57, 0.13), ("jackpot", "ping", 48.58, 1.0, 0.12), ("kj", "pop", 49.10, 0.72, 0.14),
    ("mi", "whoosh-short", 55.13, 0.57, 0.13),
    ("price", "whoosh", 63.20, 0.57, 0.15), ("rm", "impact-bass-1", 63.80, 1.6, 0.17),
    ("cta", "whoosh", 70.05, 0.57, 0.15), ("cta2", "pop", 70.45, 0.72, 0.15),
]:
    sfx(name, f, T(src), d, v)

push = [(b[0], b[3], b[4]) for b in BROLL]
tal = [(k, st, round(b - a, 3)) for k, ((a, b), st) in enumerate(zip(SEGS, starts))]
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
      #w-tal {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 50% 40%; }}
      .tal, .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .full.contain {{ object-fit: contain; background: {INK}; }}
      .bw {{ position: absolute; inset: 0; z-index: 2; overflow: hidden; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(12,18,28,.5) 0%, rgba(12,18,28,.32) 30%, rgba(12,18,28,0) 46%, rgba(12,18,28,0) 64%, rgba(12,18,28,.38) 80%, rgba(12,18,28,.45) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="w-tal">
{chr(10).join(vids[:len(SEGS)])}
      </div>
{chr(10).join(vids[len(SEGS):])}
      <div id="shade"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(push)}.forEach(([id, s, e]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "power1.out" }}, s);
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.08, duration: e - s, ease: "none" }}, s);
      }});
      {json.dumps(tal)}.forEach(([k, s, d]) => {{
        const z = k % 2 ? 1.08 : 1.0;
        tl.fromTo("#v" + k, {{ scale: z }}, {{ scale: z + 0.035, duration: d, ease: "none" }}, s);
      }});
      tl.fromTo("#w-tal", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.6, ease: "expo.out" }}, 0);
      tl.fromTo("#w-tal", {{ scale: 1 }}, {{ scale: 1.08, duration: {round(TOTAL - T(66.15), 3)}, ease: "sine.inOut", immediateRender: false }}, {T(66.15)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)


def svg(body, size=58, stroke=WHT, sw=3.4):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


PIN = f'<svg viewBox="0 0 48 64" width="58" height="76"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
ICON = {
    "road": svg('<path d="M16 4 6 44M32 4l10 40"/><path d="M24 8v6M24 21v6M24 34v6"/>'),
    "homes": svg('<path d="M2 26 14 16l12 10"/><path d="M5 24v18h18V24"/><path d="M22 20 34 10l12 10"/><path d="M26 18v24h17V18"/>', sw=3.2),
    "tag": svg('<path d="M4 24 24 4h18v18L22 42z"/><circle cx="33" cy="15" r="3.5"/>'),
    "click": svg('<path d="M14 6v6M6 14h6M8 8l4 4"/><path d="M20 18l20 8-8 3-3 8z"/>'),
}

H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.5):
    frm = {"up": "{ opacity: 0, y: 26 }", "scale": "{ opacity: 0, scale: 0.9 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def head(hid, s, e, white, yellow, top=330, extra="", ysize="", sub=""):
    BOXES.append((hid, top, 400))
    ys = f' style="font-size:{ysize}px"' if ysize else ""
    sb = f'<div class="hs" id="{hid}-s">{sub}</div>' if sub else ""
    H.append(f'    <div class="grp clip" id="{hid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px">'
             f'{extra}<div class="hw" id="{hid}-w">{white}</div><div class="hy" id="{hid}-y"{ys}>{yellow}</div>{sb}</div>')
    tin(f"#{hid}-w", s, "up")
    hide(f"#{hid}-y"); tin(f"#{hid}-y", s + 0.22, "scale")
    if sub:
        hide(f"#{hid}-s"); tin(f"#{hid}-s", s + 0.5, "up")
    J.append(f'tl.to("#{hid}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')


def count(sel, to, at, d=1.0, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {round(at, 3)}); }})();')


# Scene 1: hook, then the remaining lot (over the drone)
head("g-hook", T(0.40), T(6.00), "KHAS UNTUK PENJAWAT AWAM", "NAK BINA RUMAH<br/>DI MACHANG?", ysize=104)
head("g-last", T(8.60), T(12.00), "TINGGAL", "1 LOT TERAKHIR!", ysize=110)
# Scene 2: location
head("g-loc", T(15.10), T(19.10), "LOKASI STRATEGIK", "KG HUTAN PUTIH, MACHANG", ysize=80,
     extra=f'<div class="pin" id="pin">{PIN}<div class="ring" id="ring"></div></div>', sub="4 KM DARI BANDAR MACHANG")
J.append(f'tl.fromTo("#pin", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {T(15.10)});')
J.append(f'tl.fromTo("#ring", {{ scale: 0.3, opacity: 0.8 }}, {{ scale: 1.8, opacity: 0, duration: 0.9, ease: "power2.out", immediateRender: false }}, {T(15.5)});')
# Scene 3: land size
head("g-land", T(22.20), T(25.95), "KELUASAN TANAH", '<span id="n7244">7,244</span> KPS', ysize=130)
count("#n7244", 7244, T(22.42), 1.2)
# Scene 4: house size
head("g-1400", T(27.10), T(31.40), "BINA RUMAH BERMULA", '<span id="n1400">1,400</span> KPS', ysize=130)
count("#n1400", 1400, T(27.32))
# Scene 5: location + infrastructure
head("g-strat", T(34.40), T(38.20), "LOKASI STRATEGIK", "4 KM KE BANDAR MACHANG", ysize=80)
head("g-infra", T(40.64), T(44.10), "KEMUDAHAN SEDIA ADA", "REZAB JALAN &amp; SALIRAN", ysize=80,
     extra=f'<div class="ic" id="ic-road">{ICON["road"]}</div>')
# Scene 6: neighbourhood (over Aisyah while she points, then over the aerial of the MI houses)
head("g-kj", T(49.10), T(54.90), "KEJIRANAN SEDIA ADA", "BANGLO HASIL KERJA MI", ysize=72,
     extra=f'<div class="ic" id="ic-kj">{ICON["homes"]}</div>')
head("g-mi", T(55.50), T(59.95), "SIAP DIBINA OLEH", "MAHLIGAI IDAMAN", ysize=96)
# Scene 7: price
head("g-price", T(63.27), T(66.10), "HARGA PAKEJ BERMULA", '<span id="nrm">RM420,000</span>', ysize=128)
count("#nrm", 420000, T(63.49), 1.0, "RM")
# Scene 8: CTA
head("g-cta", T(70.10), TOTAL + 0.3, "NAK BINA RUMAH DI MACHANG?", "KLIK LINK<br/>SEKARANG!", ysize=116)

# subtitles (CapCut lines checked by the user; start times from the word pass)
SUBS = [
    (0.15, "Kalau tuan-puan **penjawat awam** dan nak bina rumah di Kelantan,"),
    (4.66, "spesifik di **Machang**,"),
    (6.08, "Aisyah nak cerita ada satu tanah"),
    (8.56, "tinggal **satu lot** ni jah, **4 km** je dari **Bandar Machang**."),
    (12.00, "Tanah dia ni, tuan-puan."),
    (14.92, "Tengoklah, tanah dia ni memang **sedia untuk bina rumah** dah."),
    (19.21, "Ha, kita nak buat **pakej bina rumah berserta dengan tanah**,"),
    (22.15, "yang mana keluasan lot ni adalah **7,244 kaki persegi**."),
    (27.07, "Tuan-puan boleh bina rumah dengan minimum keluasan rumah tu **1,400 kaki** je."),
    (34.07, "Tanah dia ni, tuan-puan, memang **strategik**, kat dengan **Bandar Machang**."),
    (38.24, "Ada **rezab jalan**, tuan-puan."),
    (40.64, "Lepas tu ada **sistem aliran longkang**."),
    (43.05, "Memang **complete** lah kita kata."),
    (44.94, "Tuan-puan tahu dak,"),
    (46.10, "untuk siapa-siapa beli tanah ni kan, memang **jackpot**,"),
    (49.05, "sebabnya dia ada **kejiranan yang baik** dak."),
    (51.15, "Rumah paling hujung, yang ni, alik ni juga, alik kiri ni kan,"),
    (55.15, "memang semuanya rumah telah pun **siap dibina oleh Mahligai Idaman**, tuan-puan."),
    (60.01, "Okey, untuk harga ni, kalau tuan-puan beli **lot terakhir** ni,"),
    (63.27, "harganya bermula **RM420,000** sahaja."),
    (66.15, "Jadi untuk **penjawat awam** hok mana-mana nak bina rumah di Machang,"),
    (70.11, "boleh **klik link** deh."),
    (71.15, "Kita adjust untuk **pakej bina rumah berserta dengan tanah**."),
]


def hl(text):
    return "".join(f"<b>{p}</b>" if i % 2 else p for i, p in enumerate(text.split("**")))


BOXES.append(("subs", 1350, 170))
cues = []
for i, (s, text) in enumerate(SUBS):
    fs = max(0.0, T(s) - 0.05)
    fe = T(SUBS[i + 1][0]) - 0.05 if i + 1 < len(SUBS) else TOTAL
    cues.append(f'      <div class="cue clip" id="cue{i}" data-start="{round(fs, 3)}" data-duration="{round(fe - fs, 3)}"><span>{hl(text)}</span></div>')
    J.append(f'tl.fromTo("#cue{i} span", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.15, ease: "power2.out" }}, {round(fs, 3)});')
H.append('    <div class="subs" id="subs">\n' + "\n".join(cues) + '\n    </div>')

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

SH = "text-shadow: 0 3px 6px rgba(0,0,0,.5), 0 10px 28px rgba(0,0,0,.55);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 800; font-size: 56px; line-height: 1.04; letter-spacing: -.005em; white-space: nowrap; text-transform: uppercase; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; font-size: 110px; line-height: 1.0; letter-spacing: -.02em; white-space: nowrap; text-align: center; text-transform: uppercase; color: {YEL}; {SH} }}
    .hs {{ margin-top: 14px; font-weight: 700; font-size: 38px; letter-spacing: .06em; color: {WHT}; {SH} }}
    .pin {{ position: relative; height: 84px; margin-bottom: 8px; filter: drop-shadow(0 6px 12px rgba(0,0,0,.5)); }}
    .ring {{ position: absolute; left: 50%; bottom: -4px; width: 70px; height: 22px; margin-left: -35px; border-radius: 50%; border: 4px solid {YEL}; opacity: 0; }}
    .ic {{ width: 92px; height: 92px; border-radius: 50%; border: 3px solid {YEL}; background: rgba(16,21,29,.55); display: flex;
      align-items: center; justify-content: center; margin-bottom: 14px; box-shadow: 0 8px 20px rgba(0,0,0,.35); }}
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
print("total", TOTAL, list(zip(starts, SEGS)))
