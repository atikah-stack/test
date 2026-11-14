#!/usr/bin/env python3
"""Finishes the user's partial edit "Pemilik seterusnya" (Abe, Kg Hutan Putih) as a 9:16, 30 fps ad.

The source is the user's edit without transitions (68 s, hard cuts land -> drain -> road ->
neighbourhood), tightened to ~44 s by keeping the segments below (SOURCE seconds of that edit).
Drone B-roll covers the jump
cuts and illustrates location, land, house size and neighbourhood; the 3D lot map is reused at the
close. Safe zone: top 15% (Y < 288) and bottom 18% (Y > 1574) carry nothing.
"""
import json, re

WHT, YEL, INK = "#FFFFFF", "#FFD43B", "#0E141D"
SAFE_TOP, SAFE_BOT = 288, 1574

SEGS = [(0.08, 5.62), (6.40, 10.12), (17.60, 23.40), (23.62, 32.46), (39.50, 42.50),
        (43.88, 46.40), (48.82, 51.12), (54.44, 59.04), (59.04, 67.68)]
SEGS = [SEGS[0], SEGS[1], SEGS[2], SEGS[3], SEGS[4], SEGS[5], SEGS[6], (54.44, 67.68)]
starts, t = [], 0.0
for a, b in SEGS:
    starts.append(round(t, 3)); t += b - a
FILM = round(t, 3)


def T(src):
    for (a, b), st in zip(SEGS, starts):
        if src < a:
            return st
        if src <= b:
            return round(st + src - a, 3)
    return FILM


vids = []
for k, ((a, b), st) in enumerate(zip(SEGS, starts)):
    vids.append(f'      <video id="v{k}" class="clip full" src="assets/video/talent.mp4" data-start="{st}" data-duration="{round(b - a, 3)}" '
                f'data-media-start="{a}" data-track-index="1" playsinline data-has-audio="true" data-volume="1" data-fade-in="0.03" data-fade-out="0.03"></video>')

# drone B-roll: (id, file, film start, film end, media start)
BROLL = [
    ("b-loc", "aerial-C51AA0CC", T(6.40), T(10.12), 0.8),        # "tanah kita ni terletak di Kg Hutan Putih, Machang"
    ("b-size", "drone-0169", T(23.62), T(28.6), 0.5),            # covers the cut; "boleh bina rumah ... 1,400"
    ("b-drain", "aerial-B3AF3D5D", T(43.88), T(45.2), 0.3),      # covers the cut on the road; drain + road from above
    ("b-nb", "aerial-D9D2F1E2", T(48.82), T(51.12), 0.0),        # "tanah ni dah ada kejiranan"
    ("b-mi1", "aerial-BB0FB1E8", T(54.44), T(56.80), 0.8),       # covers the cut; "empat-empat bijik rumah ni"
    ("b-mi2", "aerial-5899E7BB", T(56.80), T(59.04), 0.6),       # "hasil kerja Mahligai Idaman"
]
for bid, f, s, e, m in BROLL:
    vids.append(f'      <div id="{bid}-w" class="bw"><video id="{bid}" class="clip full" src="assets/video/{f}.mp4" data-start="{s}" '
                f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-track-index="2" muted playsinline></video></div>')

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{FILM}" '
       f'data-track-index="4" data-volume="0.09" data-fade-out="1.5"></audio>']


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{5 + len(AUD) % 3}" data-volume="{v}"></audio>')


for name, f, src, d, v in [
    ("hook", "impact-bass-1", 0.85, 1.6, 0.2), ("hookw", "whoosh-short", 0.75, 0.57, 0.16), ("sub", "click-soft", 2.4, 0.36, 0.18),
    ("loc", "whoosh", 6.38, 0.57, 0.18), ("pin", "pop", 7.25, 0.72, 0.16),
    ("map", "whoosh-cinematic", 17.4, 3.0, 0.14), ("trace", "riser", 18.0, 2.6, 0.12), ("n7244", "impact-bass-2", 19.6, 2.0, 0.18),
    ("size", "whoosh-short", 23.60, 0.57, 0.15), ("n1400", "pop", 27.29, 0.72, 0.17),
    ("price", "whoosh", 28.60, 0.57, 0.17), ("rm", "impact-bass-1", 30.39, 1.6, 0.22),
    ("drain", "whoosh-short", 39.48, 0.57, 0.15), ("ck1", "click", 40.30, 0.36, 0.22),
    ("cut1", "whoosh", 42.30, 0.57, 0.2),                          # hard cut drain -> road
    ("rd", "whoosh-short", 43.86, 0.57, 0.14), ("ck2", "click", 44.75, 0.36, 0.22),
    ("nb", "whoosh-short", 48.80, 0.57, 0.15), ("nbp", "pop", 49.85, 0.72, 0.16),
    ("mi", "whoosh-short", 54.42, 0.57, 0.14), ("mip", "pop", 54.70, 0.72, 0.15), ("mi2", "whoosh-short", 56.78, 0.57, 0.13),
    ("riser", "riser", 62.6 - 2.6, 2.6, 0.12), ("q", "impact-bass-2", 62.67, 2.0, 0.17),
    ("cta", "pop", 64.90, 0.72, 0.18), ("cta2", "impact-bass-1", 65.31, 1.6, 0.18),
]:
    sfx(name, f, T(src), d, v)

push = [(b[0], b[2], b[3]) for b in BROLL]
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
      .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .bw {{ position: absolute; inset: 0; z-index: 2; overflow: hidden; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(10,16,26,.5) 0%, rgba(10,16,26,.3) 30%, rgba(10,16,26,0) 46%, rgba(10,16,26,0) 62%, rgba(10,16,26,.32) 80%, rgba(10,16,26,.42) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <div id="w-tal">
{chr(10).join(vids[:len(SEGS)])}
      </div>
{chr(10).join(vids[len(SEGS):])}
      <div id="shade"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{FILM}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(push)}.forEach(([id, s, e]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18, ease: "power1.out" }}, s);
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.08, duration: e - s, ease: "none" }}, s);
      }});
      // talent segments alternate framing so the jump cuts read as camera moves
      {json.dumps(tal)}.forEach(([k, s, d]) => {{
        const z = k % 2 ? 1.07 : 1.0;
        tl.fromTo("#v" + k, {{ scale: z }}, {{ scale: z + 0.03, duration: d, ease: "none" }}, s);
      }});
      tl.fromTo("#w-tal", {{ scale: 1.1 }}, {{ scale: 1, duration: 0.6, ease: "expo.out" }}, 0);
      tl.fromTo("#w-tal", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.25, ease: "power3.out" }}, {T(30.39)});
      tl.fromTo("#w-tal", {{ scale: 1.08 }}, {{ scale: 1, duration: 0.5, ease: "power2.inOut", immediateRender: false }}, {T(31.6)});
      tl.fromTo("#w-tal", {{ scale: 1 }}, {{ scale: 1.08, duration: 2.5, ease: "sine.inOut", immediateRender: false }}, {T(64.1)});
      tl.to("#root", {{ opacity: 0, duration: 0.35 }}, {FILM - 0.35});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

PIN = f'<svg viewBox="0 0 48 64" width="40" height="52"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
CHECK = f'<svg viewBox="0 0 24 24" width="38" height="38" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path class="ck" d="M5 12.5 10 17 19 7"/></svg>'
H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.5):
    frm = {"up": "{ opacity: 0, y: 28 }", "scale": "{ opacity: 0, scale: 0.86 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def fit(text, size, k, maxw=880):
    lines = re.sub(r"<[^>]+>", "", text.replace("<br/>", "\n")).replace("&amp;", "&").split("\n")
    return int(min(size, maxw / (k * max(len(l) for l in lines))))


def head(hid, s, e, white, yellow, top=330, wsize=56, ysize=106, pre="", post=""):
    BOXES.append((hid, top, 330))
    H.append(f'    <div class="grp clip" id="{hid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px">{pre}'
             f'<div class="hw" id="{hid}-w" style="font-size:{fit(white, wsize, 0.66)}px">{white}</div>'
             f'<div class="hy" id="{hid}-y" style="font-size:{fit(yellow, ysize, 0.72)}px">{yellow}</div>{post}</div>')
    tin(f"#{hid}-w", s); hide(f"#{hid}-y"); tin(f"#{hid}-y", s + 0.2, "scale")
    J.append(f'tl.to("#{hid}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')


def count(sel, to, at, d=1.0, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {round(at, 3)}); }})();')


# 3D lot map (traced on the top-down drone photo; no subdivision layout was supplied)
k = 1080 / 1449
P = [(round(x * k), round(y * k)) for x, y in [(450, 1010), (990, 1010), (990, 1540), (450, 1540)]]
pts = " ".join(f"{x},{y}" for x, y in P)
cx = round(sum(x for x, _ in P) / 4); cy = round(sum(y for _, y in P) / 4)
layers = "".join(f'<svg class="lotsvg" viewBox="0 0 1080 1920" width="1080" height="1920" style="transform: translateZ({z}px)">'
                 f'<polygon points="{pts}" fill="{YEL}" fill-opacity="0.07" stroke="{YEL}" stroke-opacity="0.35" stroke-width="2"/></svg>'
                 for z in range(4, 34, 5))


def mapscene(sid, s, e, tag, label):
    H.insert(0, f'''    <div class="clip scn3" id="{sid}" data-start="{s}" data-duration="{round(e - s, 3)}">
      <div class="tilt" id="{tag}-tilt"><img src="assets/img/lot-top.jpg" alt="" />
        <svg class="lotsvg" viewBox="0 0 1080 1920" width="1080" height="1920"><polygon class="shadow" points="{pts}" fill="#000" fill-opacity=".35"/></svg>
        <div class="extw" id="{tag}-ext">{layers}</div>
        <svg class="lotsvg" viewBox="0 0 1080 1920" width="1080" height="1920" style="transform: translateZ(34px)">
          <polygon id="{tag}-fill" points="{pts}" fill="{YEL}" fill-opacity="0.18"/>
          <polygon id="{tag}-line" points="{pts}" fill="none" stroke="{YEL}" stroke-width="8" stroke-linejoin="round"/>
        </svg>
        <div class="lotpin" id="{tag}-pin" style="left:{cx}px; top:{cy}px">{label}</div>
      </div>
    </div>''')
    J.append(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {s});')


# 01 hook
head("g1", T(0.75), T(5.40), "SAYA NAK CARI", "SEORANG JE LAGI<br/>PEMBELI!", ysize=104,
     post='<div class="rule" id="g1r"></div><div class="hs" id="g1s">PAKEJ BINA RUMAH BESERTA TANAH</div>')
J.append(f'tl.fromTo("#g1r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, {T(2.2)});')
hide("#g1s"); tin("#g1s", T(2.4))

# 02 location
head("g2", T(7.20), T(10.12), "KG HUTAN PUTIH", "MACHANG, KELANTAN", ysize=96,
     pre=f'<div class="pinw" id="g2p">{PIN}<div class="ring" id="g2r"></div></div>')
J.append(f'tl.fromTo("#g2p", {{ y: -50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {T(7.20)});')
J.append(f'tl.fromTo("#g2r", {{ scale: 0.3, opacity: 0.8 }}, {{ scale: 1.8, opacity: 0, duration: 0.9, ease: "power2.out", immediateRender: false }}, {T(7.6)});')

# 03 3D land mapping: tilt, trace, extrude, label
s3, e3 = T(17.60), T(23.40)
mapscene("s-map", s3, e3, "m", "7,244 KPS")
J.append(f'tl.fromTo("#m-tilt", {{ rotationX: 0, rotationZ: 0, scale: 1.05, y: 0 }}, {{ rotationX: 46, rotationZ: -6, scale: 1.34, y: -70, duration: 2.0, ease: "power2.inOut" }}, {s3 + 0.1});')
J.append(f'tl.to("#m-tilt", {{ rotationZ: 3, duration: {round(e3 - s3 - 2.1, 2)}, ease: "sine.inOut" }}, {s3 + 2.1});')
J.append(f'tl.fromTo("#m-line", {{ strokeDasharray: 1900, strokeDashoffset: 1900 }}, {{ strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }}, {s3 + 0.6});')
J.append(f'tl.fromTo("#m-ext", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power3.out" }}, {T(19.57)});')
J.append(f'tl.fromTo("#m-fill", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {T(19.57)});')
J.append(f'tl.fromTo("#m-pin", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {T(19.9)});')
head("g3", T(18.60), T(23.40), "KELUASAN TANAH", '<span id="n7244">7,244</span> KPS', ysize=124)
count("#n7244", 7244, T(19.57), 1.2)

# 04 house size (drone) then price (talent)
head("g4a", T(26.45), T(28.60), "KELUASAN RUMAH BERMULA", '<span id="n1400">1,400</span> KPS', ysize=124)
count("#n1400", 1400, T(27.29), 0.8)
head("g4b", T(28.95), T(32.46), "HARGA BERMULA", '<span id="nrm">RM420,000</span>', ysize=150, wsize=60,
     post='<div class="rule wide" id="g4r"></div>')
count("#nrm", 420000, T(30.39), 1.1, "RM")
J.append(f'tl.fromTo("#g4r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {T(31.2)});')

# 05 infrastructure (talent stands at the drain, then on the tar road)
for gid, s, e, w, y in [("g5a", 40.27, 42.10, "SISTEM SALIRAN LONGKANG", "LENGKAP"), ("g5b", 44.70, 46.40, "AKSES JALAN", "TAR")]:
    BOXES.append((gid, 330, 230))
    H.append(f'    <div class="grp clip" id="{gid}" data-start="{T(s)}" data-duration="{round(T(e) - T(s), 3)}" style="top:330px">'
             f'<div class="ckh"><div class="ckb" id="{gid}-c">{CHECK}</div><div class="hw" id="{gid}-w" style="font-size:{fit(w, 54, 0.66, 760)}px">{w}</div></div>'
             f'<div class="hy" id="{gid}-y" style="font-size:118px">{y}</div><div class="rule" id="{gid}-r"></div></div>')
    tin(f"#{gid}-w", T(s)); tin(f"#{gid}-c", T(s), "scale", 0.4)
    J.append(f'tl.fromTo("#{gid}-c .ck", {{ strokeDasharray: 30, strokeDashoffset: 30 }}, {{ strokeDashoffset: 0, duration: 0.35 }}, {T(s) + 0.15});')
    hide(f"#{gid}-y"); tin(f"#{gid}-y", T(s) + 0.2, "scale")
    J.append(f'tl.fromTo("#{gid}-r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.out" }}, {T(s) + 0.45});')
    J.append(f'tl.to("#{gid}", {{ opacity: 0, y: -14, duration: 0.22, ease: "power2.in" }}, {round(T(e) - 0.22, 3)});')

# 06 neighbourhood
head("g6", T(49.82), T(51.12), "KEJIRANAN", "SEDIA ADA", ysize=124)
head("g6b", T(54.60), T(59.04), "4 BUAH RUMAH DIBINA", "MAHLIGAI IDAMAN", ysize=100)

# 07 closing: the mapped lot for the question, then the CTA on Abe
s7, e7 = T(62.40), T(64.12)
mapscene("s-end", s7, e7, "e", "LOT TERAKHIR")
J.append(f'tl.fromTo("#e-tilt", {{ rotationX: 46, rotationZ: -4, scale: 1.3, y: -60 }}, {{ rotationX: 46, rotationZ: 3, scale: 1.4, y: -80, duration: {round(e7 - s7, 2)}, ease: "sine.inOut" }}, {s7});')
head("g7", T(62.60), T(64.12), "ADAKAH ANDA", "PEMILIK SETERUSNYA?", ysize=96)
head("g8", T(64.18), FILM, "BERMINAT?", "PM ABE SEKARANG!", ysize=112, post='<div class="rule" id="g8r"></div>')
J.append(f'tl.fromTo("#g8r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, {T(65.5)});')

# subtitles from the audio, cleaned (Abe's dialect kept)
SUBS = [
    (0.11, "Tuan-puan, saya nak cari seorang je lagi **pembeli**"),
    (2.99, "untuk bina rumah di atas tanah kita ni."),
    (6.46, "Tanah kita ni terletak di **Kampung Hutan Putih, Machang**."),
    (17.65, "Tapi tanah ni berkeluasan **7,244 kaki persegi**, tuan-puan."),
    (22.25, "Besar, tuan-puan!"),
    (23.66, "Tuan-puan boleh bina rumah di atas tanah ni"),
    (25.56, "berkeluasan bermula **1,400 kaki persegi**"),
    (29.02, "dengan harga bermula **RM420,000**."),
    (39.57, "Kita siap bagi **sistem saliran longkang** lagi, tuan-puan."),
    (43.93, "Kita siap bagi **akses jalan tar** lagi, tuan-puan."),
    (48.88, "Tanah ni dah ada **kejiranan**, tuan-puan."),
    (54.49, "Keempat-empat bijik rumah ni, tuan-puan,"),
    (56.83, "ialah hasil kerja **Mahligai Idaman**."),
    (59.06, "Jadi kami nak cari **sebijik lagi** untuk dibina dekat sini."),
    (62.67, "Adakah anda **pemiliknya**?"),
    (64.18, "Siapa berminat, boleh **PM Abe sekarang**!"),
]
BOXES.append(("subs", 1380, 170))
cues = []
for i, (s, text) in enumerate(SUBS):
    fs = max(0.0, T(s) - 0.05)
    fe = T(SUBS[i + 1][0]) - 0.05 if i + 1 < len(SUBS) else FILM
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
    .hw {{ font-weight: 800; line-height: 1.06; text-align: center; white-space: nowrap; text-transform: uppercase; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; line-height: 1.0; letter-spacing: -.02em; text-align: center; white-space: nowrap; text-transform: uppercase; color: {YEL}; {SH} }}
    .hs {{ margin-top: 10px; font-weight: 700; font-size: 34px; letter-spacing: .08em; color: {WHT}; {SH} }}
    .rule {{ width: 280px; height: 6px; margin-top: 14px; border-radius: 3px; background: {YEL}; box-shadow: 0 4px 14px rgba(0,0,0,.4); }}
    .rule.wide {{ width: 620px; }}
    .pinw {{ position: relative; height: 60px; margin-bottom: 6px; filter: drop-shadow(0 6px 12px rgba(0,0,0,.5)); }}
    .ring {{ position: absolute; left: 50%; bottom: -6px; width: 64px; height: 20px; margin-left: -32px; border-radius: 50%; border: 4px solid {YEL}; opacity: 0; }}
    .ckh {{ display: flex; align-items: center; gap: 16px; }}
    .ckb {{ width: 58px; height: 58px; border-radius: 50%; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; box-shadow: 0 6px 14px rgba(0,0,0,.4); }}
    .scn3 {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; perspective: 1600px; }}
    .tilt {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 62%; transform-style: preserve-3d; }}
    .tilt img {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    .lotsvg {{ position: absolute; inset: 0; }}
    .shadow {{ filter: blur(14px); transform: translate(10px, 14px); }}
    .extw {{ position: absolute; inset: 0; transform-style: preserve-3d; }}
    .lotpin {{ position: absolute; transform: translate(-50%, -50%) translateZ(60px) rotateX(-46deg); white-space: nowrap; font-weight: 900; font-size: 56px;
      color: {WHT}; padding: 8px 22px; border-radius: 12px; background: rgba(14,20,29,.7); border: 3px solid {YEL}; }}
    .subs {{ position: absolute; left: 60px; right: 60px; top: 1380px; height: 170px; }}
    .cue {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; text-align: center; }}
    .cue span {{ display: block; max-width: 940px; font-weight: 700; font-size: 46px; line-height: 1.22; color: {WHT};
      text-shadow: 0 2px 4px rgba(0,0,0,.75), 0 6px 18px rgba(0,0,0,.55); }}
    .cue b {{ color: {YEL}; font-weight: 800; }}
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
print("film", FILM, list(zip(starts, SEGS)))
