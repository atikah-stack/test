#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman
"Pakej Tanah Beserta Bina Rumah - 1 Lot Terakhir di Machang" video (1080x1920).

The presenter take is cut into segments (pauses and fillers removed). Every time below is
in SOURCE seconds of the presenter take and is mapped to film time with T(). B-roll from
the Google Drive folder sits on top, muted. Safe zone: top 15% (Y < 288) and bottom 20%
(Y > 1536) carry nothing; headings live in the upper middle, subtitles at Y 1350-1520.
"""
import json

WHT, YEL, INK = "#FFFFFF", "#F5C542", "#10151D"
SAFE_TOP, SAFE_BOT = 288, 1536

# kept presenter segments (source in, out): removes pauses and the "aa ... okey" filler
SEGS = [(0.05, 11.16), (11.42, 14.02), (14.36, 34.86), (35.18, 41.20), (41.98, 52.68), (52.92, 54.40), (57.05, 60.30)]
starts, t = [], 0.0
for a, b in SEGS:
    starts.append(round(t, 3)); t += b - a
TOTAL = round(t, 3)


def T(src):
    """source second -> film second (a time inside a removed gap snaps to the next segment)"""
    for (a, b), st in zip(SEGS, starts):
        if src < a:
            return st
        if src <= b:
            return round(st + src - a, 3)
    return TOTAL


# ---------------- presenter segments ----------------
vids = []
for k, ((a, b), st) in enumerate(zip(SEGS, starts)):
    vids.append(f'      <video id="v{k}" class="clip tal" src="assets/video/talent.mp4" data-start="{st}" data-duration="{round(b - a, 3)}" '
                f'data-media-start="{a}" data-track-index="1" playsinline data-has-audio="true" data-volume="1" '
                f'data-fade-in="0.03" data-fade-out="0.03"></video>')

# ---------------- B-roll: (id, kind, src, start, end, media start / focus) ----------------
BROLL = [
    ("b-loc", "video", "aerial-C51AA0CC", T(11.30), T(15.40), 1.0),       # covers two cuts; "lokasi ... Machang"
    ("b-map", "map", "lot-map", T(19.90), T(22.06), None),               # verified lot map (red boundary, 7,244 KPS)
    ("b-lot", "video", "drone-0169", T(22.06), T(26.30), 0.8),            # "satu lot yang luas"
    ("b-road", "video", "road", T(34.70), T(36.30), 6.0),                 # covers the cut before "akses jalan tar"
    ("b-nb", "video", "aerial-5899E7BB", T(41.10), T(43.70), 0.6),        # covers the cut; "kejiranan"
    ("b-mi", "video", "aerial-BB0FB1E8", T(46.10), T(49.50), 1.0),        # "rumah banglo hasil kerja MI"
    ("b-last", "video", "aerial-D084B064", T(52.40), T(57.40), 0.2),      # covers two cuts; "lot terakhir"
]
for bid, kind, f, s, e, m in BROLL:
    if kind == "video":
        vids.append(f'      <div id="{bid}-w" class="bw"><video id="{bid}" class="clip full" src="assets/video/{f}.mp4" data-start="{s}" '
                    f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-track-index="2" muted playsinline></video></div>')

# ---------------- sound ----------------
AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{TOTAL}" '
       f'data-track-index="4" data-volume="0.09" data-fade-out="1.5"></audio>']


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{5 + len(AUD) % 3}" data-volume="{v}"></audio>')


for name, f, src, d, v in [
    ("h1", "whoosh-short", 2.60, 0.57, 0.16), ("h2", "pop", 3.30, 0.72, 0.14),
    ("loc", "whoosh-short", 11.30, 0.57, 0.15), ("pin", "pop", 14.40, 0.72, 0.15),
    ("lot", "whoosh", 15.80, 0.57, 0.15), ("n7244", "ping", 20.70, 1.0, 0.12), ("map", "whoosh-short", 19.88, 0.57, 0.13),
    ("lotcut", "whoosh-short", 22.04, 0.57, 0.13), ("n1400", "pop", 25.70, 0.72, 0.15), ("n1400b", "ping", 27.30, 1.0, 0.11),
    ("price", "whoosh", 28.85, 0.57, 0.15), ("rm", "impact-bass-1", 29.75, 1.6, 0.17),
    ("road", "whoosh-short", 34.68, 0.57, 0.13), ("akses", "pop", 36.14, 0.72, 0.15), ("drain", "pop", 39.50, 0.72, 0.15),
    ("nb", "whoosh-short", 41.08, 0.57, 0.13), ("kj", "pop", 42.30, 0.72, 0.14),
    ("c1", "click-soft", 43.80, 0.36, 0.2), ("c2", "click-soft", 44.21, 0.36, 0.2), ("c3", "click-soft", 45.04, 0.36, 0.2), ("c4", "click-soft", 45.64, 0.36, 0.2),
    ("mi", "whoosh", 46.08, 0.57, 0.14), ("mi2", "pop", 46.60, 0.72, 0.14),
    ("tinggal", "impact-bass-1", 50.72, 1.6, 0.16), ("last", "whoosh-short", 52.38, 0.57, 0.12),
    ("cta", "whoosh", 57.85, 0.57, 0.15), ("cta2", "pop", 58.50, 0.72, 0.15),
]:
    sfx(name, f, T(src), d, v)

push = [(b[0], b[3], b[4]) for b in BROLL if b[1] == "video"]
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
      #w-tal {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 50% 42%; }}
      .tal, .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
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
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18, ease: "power1.out" }}, s);
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.08, duration: e - s, ease: "none" }}, s);
      }});
      // each presenter segment: alternate gentle push sizes so the jump cuts read as camera moves
      {json.dumps(tal)}.forEach(([k, s, d]) => {{
        const z = k % 2 ? 1.08 : 1.0;
        tl.fromTo("#v" + k, {{ scale: z }}, {{ scale: z + 0.035, duration: d, ease: "none" }}, s);
      }});
      // opening punch-in, and a slow zoom on the closing call to action
      tl.fromTo("#w-tal", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.6, ease: "expo.out" }}, 0);
      tl.fromTo("#w-tal", {{ scale: 1 }}, {{ scale: 1.08, duration: {round(TOTAL - T(57.05), 3)}, ease: "sine.inOut", immediateRender: false }}, {T(57.05)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ================= gfx =================
def svg(body, size=64, stroke=INK, sw=3.6, vb="0 0 48 48", fill="none"):
    return (f'<svg viewBox="{vb}" width="{size}" height="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


PIN = f'<svg viewBox="0 0 48 64" width="58" height="76"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
ICON = {
    "road": svg('<path d="M16 4 6 44M32 4l10 40"/><path d="M24 8v6M24 21v6M24 34v6"/>', 58, WHT, 3.4),
    "drain": svg('<path d="M4 14h8v20h24V14h8"/><path d="M12 34c4 4 20 4 24 0"/><path d="M18 22c2 2 4 2 6 0s4-2 6 0"/>', 58, WHT, 3.4),
    "homes": svg('<path d="M2 26 14 16l12 10"/><path d="M5 24v18h18V24"/><path d="M22 20 34 10l12 10"/><path d="M26 18v24h17V18"/>', 58, WHT, 3.2),
}

H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.5):
    frm = {"up": "{ opacity: 0, y: 26 }", "scale": "{ opacity: 0, scale: 0.9 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def tout(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(at, 3)});')


def head(hid, s, e, white, yellow, top=330, extra="", ysize=""):
    """the standard Mahligai Idaman heading: white line over a bigger golden-yellow line"""
    BOXES.append((hid, top, 330))
    ys = f' style="font-size:{ysize}px"' if ysize else ""
    H.append(f'    <div class="grp clip" id="{hid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px">'
             f'{extra}<div class="hw" id="{hid}-w">{white}</div><div class="hy" id="{hid}-y"{ys}>{yellow}</div></div>')
    tin(f"#{hid}-w", s, "up")
    hide(f"#{hid}-y")
    tin(f"#{hid}-y", s + 0.22, "scale")
    tout(f"#{hid}", e - 0.25)


def count(sel, to, at, d=0.9, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {round(at, 3)}); }})();')


# 1. hook
head("g-hook", T(2.65), T(7.70), "PAKEJ TANAH BESERTA", "BINA RUMAH")

# 2. location (over the aerial)
head("g-loc", T(14.36), T(15.40), "LOKASI PILIHAN ANDA", "MACHANG, KELANTAN",
     extra=f'<div class="pin" id="pin">{PIN}<div class="ring" id="ring"></div></div>', ysize=92)
J.append(f'tl.fromTo("#pin", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {T(14.36)});')
J.append(f'tl.fromTo("#ring", {{ scale: 0.3, opacity: 0.8 }}, {{ scale: 1.8, opacity: 0, duration: 0.9, ease: "power2.out", immediateRender: false }}, {T(14.7)});')

# 3. land reveal: heading on the presenter, then the verified lot map (it carries its own 7,244 KPS label)
head("g-lot", T(15.83), T(19.90), "1 LOT BANGLO TERAKHIR", '<span id="n7244">7,244</span> KPS', ysize=130)
count("#n7244", 7244, T(15.83) + 0.22, 1.2)
H.append(f'    <div class="clip scn" id="s-map" data-start="{T(19.90)}" data-duration="{round(T(22.06) - T(19.90), 3)}"><div class="mapbg"></div>'
         f'<img id="map" src="assets/img/lot-map.jpg" alt="" /></div>')
J.append(f'tl.fromTo("#s-map", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {T(19.90)});')
J.append(f'tl.fromTo("#map", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {round(T(22.06) - T(19.90), 3)}, ease: "none" }}, {T(19.90)});')

# 4. house size, then price (one group at a time)
head("g-1400", T(25.66), T(28.50), "BINA RUMAH BERMULA", '<span id="n1400">1,400</span> KPS', ysize=130)
count("#n1400", 1400, T(25.66) + 0.22)
head("g-price", T(28.88), T(32.10), "HARGA PAKEJ BERMULA", '<span id="nrm">RM420,000</span>', ysize=128)
count("#nrm", 420000, T(28.88) + 0.22, 1.0, "RM")

# 5. infrastructure (the presenter's own camera shows the road and the drain)
head("g-road", T(36.14), T(39.30), "AKSES", "JALAN TAR", extra=f'<div class="ic" id="ic-road">{ICON["road"]}</div>')
head("g-drain", T(39.50), T(41.20), "KEMUDAHAN", "SALIRAN LONGKANG", extra=f'<div class="ic" id="ic-drain">{ICON["drain"]}</div>', ysize=84)

# 6. neighbourhood: count the four MI bungalows with their own photos
head("g-kj", T(42.30), T(43.70), "KEJIRANAN", "SEDIA ADA", extra=f'<div class="ic" id="ic-kj">{ICON["homes"]}</div>')
counts = [43.78, 44.21, 45.04, 45.64]
H.append(f'    <div class="clip scn" id="s-count" data-start="{T(43.70)}" data-duration="{round(T(46.10) - T(43.70), 3)}">'
         + "".join(f'<img class="hp" id="hp{i}" src="assets/img/house-{i + 1}.jpg" alt="" />' for i in range(4))
         + '<div class="cnt" id="cnt"><span id="cntn">1</span><small>/4</small></div></div>')
BOXES.append(("cnt", 1180, 150))
for i, c in enumerate(counts):
    a = T(c) if i else T(43.70)
    J.append(f'tl.fromTo("#hp{i}", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "power2.out" }}, {a});')
    J.append(f'tl.set("#cntn", {{ textContent: "{i + 1}" }}, {T(c)});')
    J.append(f'tl.fromTo("#cnt", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {T(c)});')
hide("#cnt"); tin("#cnt", T(43.75), "scale", 0.3)
head("g-mi", T(46.20), T(49.50), "4 BANGLO HASIL KERJA", "MAHLIGAI IDAMAN", ysize=96)

# 7. scarcity and CTA
head("g-last", T(50.72), T(54.40), "TINGGAL", "1 LOT TERAKHIR!", ysize=120)
head("g-cta", T(57.87), TOTAL + 0.3, "BERMINAT?", "HUBUNGI KAMI SEKARANG", ysize=70)

# ---------------- subtitles: white, soft shadow, max two lines, Y 1350-1520 ----------------
SUBS = [
    (0.13, "Tuan-puan tahu dak yang **Mahligai Idaman** ni"),
    (2.46, "ada **pakej tanah dan bina rumah**?"),
    (4.78, "Bagi sesiapa hok nak bina rumah tapi **tak ada tanah**,"),
    (7.82, "kita akan carikan lokasi yang diinginkan lah oleh kalian-kalian itu."),
    (11.42, "So, antara salah satu lokasi ni adalah di **Machang** ni."),
    (15.46, "Ada **satu lot banglo**, tuan-puan, di belakang saya ni,"),
    (18.26, "berkeluasan **7,244 kaki persegi**."),
    (22.06, "Satu lot yang luas, tuan-puan, di mana tuan-puan boleh bina rumah di atas ni"),
    (25.66, "bermula size **1,400 kaki persegi**,"),
    (28.58, "dengan harga bermula **RM420,000** ke atas."),
    (32.12, "Tuan-puan, salah satunya yang berada di sini adalah, tuan-puan boleh tengok,"),
    (35.18, "dan ada dah **akses jalan tar**"),
    (37.44, "dekat sini, rapat ke **jalan besar**."),
    (39.42, "Kita dah ada **saliran longkang** kat sini."),
    (41.98, "Dan lagi kita ada **kejiranan**, tuan-puan:"),
    (43.78, "satu, dua, tiga, empat"),
    (46.16, "**rumah banglo** hasil kerja **Mahligai Idaman**, tuan-puan."),
    (49.58, "Dan kita nak cari satu lagi **lot terakhir** ni,"),
    (51.62, "pemilik untuk lot terakhir ni untuk bina rumah kat sini, tuan-puan."),
    (57.12, "Kalau tuan-puan **berminat**,"),
    (58.50, "boleh **contact saya sekarang**."),
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
    .grp {{ position: absolute; left: 40px; right: 40px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 800; font-size: 64px; line-height: 1.04; letter-spacing: -.005em; white-space: nowrap; text-transform: uppercase; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; font-size: 110px; line-height: 1.0; letter-spacing: -.02em; white-space: nowrap; text-transform: uppercase; color: {YEL}; {SH} }}
    .pin {{ position: relative; height: 84px; margin-bottom: 8px; filter: drop-shadow(0 6px 12px rgba(0,0,0,.5)); }}
    .ring {{ position: absolute; left: 50%; bottom: -4px; width: 70px; height: 22px; margin-left: -35px; border-radius: 50%; border: 4px solid {YEL}; opacity: 0; }}
    .ic {{ width: 92px; height: 92px; border-radius: 50%; border: 3px solid {YEL}; background: rgba(16,21,29,.55); display: flex;
      align-items: center; justify-content: center; margin-bottom: 14px; box-shadow: 0 8px 20px rgba(0,0,0,.35); }}
    .scn {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; }}
    .mapbg {{ position: absolute; inset: 0; background: {INK}; }}
    #map {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; transform-origin: 30% 64%; }}
    .hp {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
    .cnt {{ position: absolute; left: 0; right: 0; top: 1180px; text-align: center; font-weight: 900; font-size: 140px; line-height: 1; color: {YEL}; {SH} }}
    .cnt small {{ font-size: 64px; color: {WHT}; }}
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
print("total", TOTAL, "segments", list(zip(starts, SEGS)))
