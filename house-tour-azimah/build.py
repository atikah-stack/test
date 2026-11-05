#!/usr/bin/env python3
"""House tour edit: Full Review 1 Azimah Kemaman -> 9:16 Mahligai Idaman house tour.

SEGS are the kept talent stretches (source seconds in assets/video/tour.mp4, cut at real
pauses found with silencedetect). BROLL are muted cutaways from the same footage that hide
jump cuts or show the thing being described. Captions and graphics are written against
SOURCE time; src() converts to film time.
"""
import json, re

SEGS = [  # (id, src_in, src_out)
    ("hook", 14.15, 16.45),   # "Besar, tuan-puan. Sangat-sangat mewah."
    ("intro", 0.00, 14.10),   # "Tak tahulah ... Kemaman, Terengganu."
    ("hitam", 16.95, 18.85),  # "Bermain dengan warna hitam"
    ("luar", 20.69, 32.05),   # "menampakkan lagi banglo ni ... imprint."
    ("porch", 40.75, 56.40),  # porch, family gathering, "bahagian dalam lagi menarik"
    ("jom", 56.85, 58.50),    # "Jom kita house tour sama-sama"
    ("pintu", 68.50, 74.95),  # entrance
    ("sekuriti", 75.62, 81.87),
    ("tamu", 88.30, 104.25),
    ("makan", 112.35, 123.50),
    ("meja", 145.70, 157.10),
    ("dapur", 161.70, 243.10),  # pantry -> sliding door -> wet kitchen -> porch door
]
start, t = {}, 0.0
for sid, a, b in SEGS:
    start[sid] = round(t, 3); t += b - a
TOTAL = round(t, 3)


def src(s):
    for sid, a, b in SEGS:
        if a - 0.001 <= s <= b + 0.001:
            return round(start[sid] + s - a, 3)
    raise ValueError(f"source time {s} is not in a kept segment")


def cut(sid):  # film time of a segment's start
    return start[sid]

# cutaways: (id, film start, duration, source media start)
BROLL = [
    ("b1", cut("hitam") - 0.35, 1.5, 33.2),     # exterior walk
    ("b2", cut("porch") - 0.5, 1.6, 36.2),      # exterior / porch
    ("b3", cut("pintu") - 0.5, 1.7, 64.0),      # entrance corridor
    ("b4", cut("tamu") - 0.6, 2.0, 85.6),       # door opens onto the living room
    ("b5", src(97.3), 1.6, 87.0),               # chandelier (out of frame in the talking shot)
    ("b6", cut("makan") - 0.5, 1.7, 107.0),     # living room pan
    ("b7", cut("meja") - 0.5, 1.6, 124.8),      # dining feature wall
    ("b8", cut("dapur") - 0.5, 1.6, 158.2),     # dining -> pantry
]

# ---------------- captions (source start, text) ----------------
CAP = [
    (14.19, "Besar, tuan-puan."), (15.28, "Sangat-sangat mewah."),
    (0.00, "Tak tahulah nak gambarkan"), (1.58, "macam mana betapa bahagianya"), (3.75, "tuan rumah ini"),
    (4.68, "apabila mendapat"), (6.05, "banglo idaman beliau, tuan-puan."),
    (8.32, "Banglo yang berkonsep split level ini"), (10.23, "telah siap dibina oleh Mahligai Idaman"),
    (12.60, "di Kemaman, Terengganu."),
    (16.97, "Bermain dengan warna hitam"),
    (20.69, "menampakkan lagi banglo ni"), (21.97, "sangat-sangat premium."),
    (23.24, "Di bahagian luar dia dah pun,"), (25.21, "dah cukup tertawan."),
    (27.16, "Lengkap adanya landscape macam ni"), (29.49, "dan kekemasan lantai"), (30.91, "menggunakan imprint."),
    (40.78, "Dekat bahagian luar ni ada satu"), (42.19, "ruang porch yang sangat besar,"),
    (43.50, "boleh memuatkan sehingga"), (44.81, "empat kenderaan."),
    (46.54, "Dan sesuai juga untuk mereka"), (48.26, "yang berkeluarga besar"),
    (49.26, "untuk membuat family gathering"), (51.14, "dekat bawah ni."),
    (52.27, "Okey, bahagian luar kita dah tengok,"), (54.27, "di bahagian dalam lagi menarik."),
    (56.88, "Jom kita house tour sama-sama!"),
    (68.51, "Bahagian pintu ni sangat-sangat cantik"), (70.93, "dan inilah masa yang ditunggu-tunggu,"),
    (73.17, "kita nak ke bahagian dalam."),
    (75.66, "Tengoklah pintu sekuriti dia,"), (78.00, "sangat-sangat tertawan, tuan-puan,"),
    (80.39, "menggunakan warna hitam."),
    (88.34, "Inilah dia bahagian ruang yang pertama."), (91.70, "Ruang tamu yang mana berkeluasan"),
    (93.87, "15 x 17 kaki persegi,"), (97.22, "lengkap dengan lampu chandelier,"),
    (99.55, "ceiling double layer"), (100.87, "dan susun atur sofa"), (102.13, "yang cukup-cukup sempurna."),
    (112.37, "Okey, seterusnya ini pun"), (114.91, "adalah bahagian ruang makan."),
    (117.41, "Ruang makan ini kan,"), (118.82, "yang paling menarik"), (120.47, "adalah di bahagian lantai ini."),
    (145.76, "Dengan keluasan"), (147.34, "16 x 8 kaki persegi sahaja,"),
    (150.21, "boleh memuatkan meja makan macam ni"), (152.90, "yang mempunyai 6, 7, 8 seater."),
    (161.73, "Okey, sebelum kita pergi"), (163.20, "ke bahagian ruangan dapur, kan?"),
    (165.69, "Kita dah ada di bahagian sini,"), (168.25, "macam pantry pun ya,"), (169.55, "ataupun dapur kering"),
    (170.91, "yang sangat-sangat cantik."), (173.51, "Dan ia berdekatan dengan ruang makan."),
    (176.11, "Jadi senang kalau nak ambil makanan ke,"), (178.31, "nak hidang makanan ke,"),
    (179.38, "semua diletakkan di bahagian sini sahaja."),
    (182.51, "Untuk memasak di mana?"), (184.36, "Di sini. Jom kita tengok."),
    (185.51, "Okey, dipisahkan dengan"), (187.16, "satu pintu sliding macam ini,"), (189.36, "sangat estetik."),
    (190.36, "Jom kita tengok."),
    (193.81, "Inilah dia, tuan-puan,"), (196.01, "dapur basah yang berkeluasan"), (198.10, "10 x 10 kaki je,"),
    (199.96, "tak besar sangat,"), (200.81, "tapi sungguh menawan,"), (202.86, "sungguh cantik"),
    (204.08, "dengan pemilihan warna putih."), (205.81, "Warna putih,"), (206.77, "walaupun ruangnya sangat kecil,"),
    (209.38, "tapi menampakkan ia lebih luas"), (211.89, "dan sangat menenangkan warnanya."),
    (214.81, "Dan ini pintu sekuriti"), (216.38, "yang mana kita boleh akses"), (218.25, "ke bahagian ruangan porch"),
    (220.05, "yang saya cerita awal tadi, tuan-puan."), (222.81, "Jadi senang kalau ada"),
    (224.28, "family gathering ke apa,"), (225.91, "segala makanan ataupun barang"),
    (228.06, "boleh dibawa melalui pintu ini sahaja."), (231.02, "Betul tak?"), (231.81, "Siapa setuju,"),
    (232.95, "rumah yang konsep split level ini"), (235.85, "lebih senang kalau kita letak"),
    (238.43, "satu pintu di bahagian sini,"), (240.48, "akses untuk keluar rumah."),
]
HL = ["banglo idaman", "split level", "Mahligai Idaman", "Kemaman, Terengganu", "hitam", "premium", "imprint", "porch",
      "empat kenderaan", "family gathering", "house tour", "pintu sekuriti", "15 x 17", "chandelier", "double layer",
      "ruang makan", "lantai", "16 x 8", "8 seater", "pantry", "dapur kering", "sliding", "dapur basah", "10 x 10",
      "putih", "lebih luas", "akses", "sangat-sangat mewah", "landscape"]


def hl(text):
    for h in sorted(HL, key=len, reverse=True):
        text = re.sub(re.escape(h), lambda m: f"\x01{m.group(0)}\x02", text, flags=re.I)
    return text.replace("\x01", '<span class="y">').replace("\x02", "</span>")

# film-time caption windows: end at the next caption in the same segment, else the segment end
caps = []
for i, (s, txt) in enumerate(CAP):
    seg = next(x for x in SEGS if x[1] - 0.001 <= s <= x[2] + 0.001)
    nxt = [c[0] for c in CAP if seg[1] <= c[0] <= seg[2] and c[0] > s]
    e = min(nxt) if nxt else seg[2]
    caps.append((src(s), round(src(min(e, seg[2])) - 0.04, 3), hl(txt)))

# ---------------- index.html ----------------
V = []
for k, (sid, a, b) in enumerate(SEGS):
    V.append(f'      <div class="vw" id="w-{sid}"><video id="v-{sid}" class="clip" src="assets/video/tour.mp4" data-start="{start[sid]}" '
             f'data-duration="{round(b - a, 3)}" data-media-start="{a}" data-track-index="1" playsinline data-has-audio="true" '
             f'data-volume="1" data-fade-in="0.03" data-fade-out="0.05"></video></div>')
for bid, s, d, m in BROLL:
    V.append(f'      <div class="vw br" id="w-{bid}"><video id="v-{bid}" class="clip" src="assets/video/tour.mp4" data-start="{round(s, 3)}" '
             f'data-duration="{d}" data-media-start="{m}" data-track-index="2" muted playsinline></video></div>')

SFX = []
def sfx(name, f, at, dur, vol):
    SFX.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" data-duration="{dur}" '
               f'data-track-index="{5 + len(SFX) % 3}" data-volume="{vol}"></audio>')

sfx("hook", "whoosh-short", 0.12, 0.57, 0.14)
sfx("title", "whoosh-short", src(8.85), 0.57, 0.12)
sfx("loc", "pop", src(12.62), 0.72, 0.1)
sfx("hitam", "whoosh-short", src(18.15), 0.57, 0.12)
for i in range(4):
    sfx(f"car{i}", "click-soft", src(44.85) + i * 0.22, 0.36, 0.16)
sfx("cars", "chime", src(45.75), 1.2, 0.07)
sfx("family", "pop", src(50.1), 0.72, 0.1)
sfx("door", "whoosh-short", src(76.3), 0.57, 0.12)
sfx("tamu", "click-soft", src(93.9), 0.36, 0.18)
sfx("chand", "chime", src(97.95), 1.2, 0.06)
sfx("ceil", "whoosh-short", src(99.55), 0.57, 0.1)
sfx("floor", "whoosh-short", src(122.0), 0.57, 0.1)
sfx("meja", "click-soft", src(147.4), 0.36, 0.18)
sfx("seat", "chime", src(156.45), 1.2, 0.07)
sfx("kering", "whoosh-short", src(169.6), 0.57, 0.12)
sfx("basah", "whoosh-short", src(192.4), 0.57, 0.12)
sfx("ten", "click-soft", src(198.15), 0.36, 0.18)
sfx("putih", "whoosh-short", src(205.85), 0.57, 0.1)
sfx("porchdoor", "whoosh-short", src(217.7), 0.57, 0.12)
sfx("food", "pop", src(226.45), 0.72, 0.1)

# gentle push in each kept stretch; same-shot jump cuts get a small punch so they read as intended
pushes = []
for k, (sid, a, b) in enumerate(SEGS):
    s0 = 1.0 if k % 2 == 0 else 1.06
    pushes.append((sid, start[sid], round(b - a, 3), s0, s0 + 0.04))

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
      .vw {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; transform-origin: 50% 45%; }}
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
      {json.dumps(pushes)}.forEach(([id, s, d, a, b]) => tl.fromTo("#w-" + id, {{ scale: a }}, {{ scale: b, duration: d, ease: "none" }}, s));
      {json.dumps([(b[0], round(b[1], 3), b[2]) for b in BROLL])}.forEach(([id, s, d]) => {{
        tl.fromTo("#w-" + id, {{ opacity: 0, scale: 1.04 }}, {{ opacity: 1, scale: 1.0, duration: 0.2, ease: "power2.out" }}, s);
        tl.to("#w-" + id, {{ scale: 1.06, duration: d - 0.2, ease: "none" }}, s + 0.2);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------------- gfx.html ----------------
H, J = [], []
def el(html): H.append("    " + html)
def js(s): J.append("    " + s)
def win(sel, s, e, kind="up", out=True):
    frm = {"up": "{ opacity: 0, y: 30, filter: 'blur(8px)' }", "pop": "{ opacity: 0, scale: 0.7 }",
           "left": "{ opacity: 0, x: -160, filter: 'blur(8px)' }", "fade": "{ opacity: 0 }"}[kind]
    js(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, x: 0, y: 0, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, {round(s, 3)});')
    if out: js(f'tl.to("{sel}", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')
def grp(gid, s, e, inner, style):
    el(f'<div class="g clip" id="{gid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="{style}">{inner}</div>')

PIN = '<svg viewBox="0 0 48 64" width="36" height="48"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="#F6C343"/><circle cx="24" cy="24" r="8.5" fill="#14161B"/></svg>'
CAR = '<svg viewBox="0 0 64 40" width="104" height="66" fill="#F6C343"><path d="M10 26 15 12c1-3 3-4 6-4h22c3 0 5 1 6 4l5 14h2c2 0 4 2 4 4v4c0 1-1 2-2 2h-4a6 6 0 0 1-12 0H22a6 6 0 0 1-12 0H6c-1 0-2-1-2-2v-4c0-2 2-4 4-4z"/><path d="M19 14h26l3 10H16z" fill="#14161B" opacity=".55"/><circle cx="16" cy="34" r="4" fill="#14161B"/><circle cx="48" cy="34" r="4" fill="#14161B"/></svg>'
FAM = '<svg viewBox="0 0 64 48" width="92" height="70" fill="#14161B"><circle cx="18" cy="10" r="7"/><circle cx="46" cy="10" r="7"/><circle cx="32" cy="22" r="5"/><path d="M6 46V30c0-6 5-10 12-10s12 4 12 10v16z"/><path d="M34 46V30c0-6 5-10 12-10s12 4 12 10v16z"/><path d="M24 46V36c0-4 3-7 8-7s8 3 8 7v10z" fill="#F6C343" stroke="#14161B" stroke-width="2"/></svg>'
CHAIR = '<svg viewBox="0 0 48 56" width="62" height="72" fill="#14161B"><rect x="12" y="2" width="24" height="26" rx="10"/><rect x="8" y="30" width="32" height="7" rx="3"/><rect x="10" y="37" width="5" height="17" rx="2"/><rect x="33" y="37" width="5" height="17" rx="2"/></svg>'
DISH = '<svg viewBox="0 0 64 44" width="80" height="56" fill="none" stroke="#14161B" stroke-width="4" stroke-linecap="round"><path d="M8 34h48"/><path d="M12 34a20 20 0 0 1 40 0"/><path d="M32 10V6"/><path d="M4 40h56"/></svg>'

# --- captions
for i, (s, e, txt) in enumerate(caps):
    grp(f"cp{i}", s, e, f'<div class="cap" id="ct{i}">{txt}</div>', "left:90px; right:90px; top:1330px; display:flex; justify-content:center")
    js(f'tl.fromTo("#ct{i}", {{ opacity: 0, y: 14, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "power3.out" }}, {s});')

# --- hook
s, e = 0.05, cut("intro") + 0.6
grp("g-hook", s, e, '<div class="hk w" id="hk1">PORCH MUAT</div><div class="hk y" id="hk2">4 KERETA?!</div>',
    "left:60px; right:60px; top:300px; text-align:center")
js(f'tl.fromTo("#hk1", {{ opacity: 0, y: 40, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "expo.out" }}, 0.1);')
js(f'tl.fromTo("#hk2", {{ opacity: 0, scale: 1.5, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, 0.55);')
js(f'tl.to("#g-hook", {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, {round(e - 0.25, 3)});')

# --- 1. exterior: title + location, then HITAM • PREMIUM
s, e = src(8.85), src(14.1)
grp("g-title", s, e, f'<div class="tag" id="tg1">BANGLO <span class="y">SPLIT LEVEL</span></div>'
    f'<div class="loc" id="lc1">{PIN}<span>KEMAMAN, TERENGGANU</span></div>',
    "left:90px; right:90px; top:250px; display:flex; flex-direction:column; align-items:center; gap:16px")
win("#tg1", s, e, "up", out=False); js('tl.set("#lc1", { opacity: 0 }, 0);'); win("#lc1", src(12.6), e, "up", out=False)
js(f'tl.to("#g-title", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')
s, e = src(18.2), src(23.1)
grp("g-hitam", s, e, '<div class="pill"><span class="dot k"></span>HITAM <span class="sep">•</span> <span class="y">PREMIUM</span></div>',
    "left:90px; right:90px; top:270px; display:flex; justify-content:center")
win("#g-hitam .pill", s, e, "pop")

# --- 2. porch: four cars one by one, then family gathering
s, e = src(44.80), src(49.9)
cars = "".join(f'<div class="car" id="car{i}">{CAR}</div>' for i in range(4))
grp("g-cars", s, e, f'<div class="cars">{cars}</div><div class="tag sm" id="cartx">MUAT <span class="y">4 KENDERAAN</span></div>',
    "left:90px; right:90px; top:240px; display:flex; flex-direction:column; align-items:center; gap:14px")
for i in range(4):
    js(f'tl.fromTo("#car{i}", {{ opacity: 0, y: -30, scale: 0.6 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(s + i * 0.22, 3)});')
js('tl.set("#cartx", { opacity: 0 }, 0);'); win("#cartx", s + 0.9, e, "up", out=False)
js(f'tl.to("#g-cars", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')
s, e = src(50.05), src(52.2)
grp("g-fam", s, e, f'<div class="card"><div class="ic">{FAM}</div><div class="ct">RUANG BERKUMPUL<br><span class="dk">KELUARGA</span></div></div>',
    "left:90px; right:90px; top:260px; display:flex; justify-content:center")
win("#g-fam .card", s, e, "pop")

# --- 3. security door (door is the right half of the frame here)
s, e = src(76.3), src(80.3)
el(f'<div class="g clip" id="g-door" data-start="{s}" data-duration="{round(e - s, 3)}" style="inset:0">'
   '<svg class="ln" viewBox="0 0 1080 1920"><path id="dl" d="M700 470 L800 700" pathLength="100"/><circle id="dd" cx="800" cy="700" r="12"/></svg>'
   '<div class="lbl" id="dlb" style="left:430px; top:360px">PINTU SEKURITI</div></div>')
win("#dlb", s, e, "up", out=False)
js(f'tl.fromTo("#dl", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, {round(s + 0.15, 3)});')
js(f'tl.fromTo("#dd", {{ scale: 0, transformOrigin: "800px 700px" }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(s + 0.4, 3)});')
js(f'tl.to("#g-door", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')

# --- 4. living room: size card, chandelier (on the cutaway), ceiling
s, e = src(93.85), src(97.2)
grp("g-tamu", s, e, '<div class="size"><div class="sk">RUANG TAMU</div><div class="sv">15 × 17 <small>KAKI</small></div></div>',
    "left:90px; right:90px; top:250px; display:flex; justify-content:center")
win("#g-tamu .size", s, e, "pop")
s, e = src(97.95), src(98.9)
el(f'<div class="g clip" id="g-chand" data-start="{s}" data-duration="{round(e - s, 3)}" style="inset:0">'
   '<svg class="ln" viewBox="0 0 1080 1920"><path id="chl" d="M540 560 L560 380" pathLength="100"/><circle id="chd" cx="560" cy="380" r="12"/></svg>'
   '<div class="lbl" id="chb" style="left:340px; top:580px">CHANDELIER</div></div>')
win("#chb", s, e, "up", out=False)
js(f'tl.fromTo("#chl", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {round(s + 0.1, 3)});')
js(f'tl.fromTo("#chd", {{ scale: 0, transformOrigin: "560px 380px" }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {round(s + 0.3, 3)});')
s, e = src(99.55), src(101.9)
el(f'<div class="g clip" id="g-ceil" data-start="{s}" data-duration="{round(e - s, 3)}" style="inset:0">'
   '<svg class="ln" viewBox="0 0 1080 1920"><path id="cel" d="M540 400 L540 230" pathLength="100"/><circle id="ced" cx="540" cy="230" r="12"/></svg>'
   '<div class="lbl" id="ceb" style="left:250px; top:420px">CEILING DOUBLE LAYER</div></div>')
win("#ceb", s, e, "up", out=False)
js(f'tl.fromTo("#cel", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {round(s + 0.1, 3)});')
js(f'tl.fromTo("#ced", {{ scale: 0, transformOrigin: "540px 230px" }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {round(s + 0.3, 3)});')
js(f'tl.to("#g-ceil", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')

# --- 5. dining: floor emphasis, size, seats
s, e = src(122.0), src(123.45)
el(f'<div class="g clip" id="g-floor" data-start="{s}" data-duration="{round(e - s, 3)}" style="inset:0">'
   '<div class="sweep" id="fsw"></div>'
   '<svg class="ln" viewBox="0 0 1080 1920"><path id="fl" d="M150 1250 L110 1640" pathLength="100"/><circle id="fd" cx="110" cy="1640" r="12"/></svg>'
   '<div class="lbl" id="flb" style="left:70px; top:1150px">LANTAI</div></div>')
js(f'tl.fromTo("#fsw", {{ opacity: 0, x: -500 }}, {{ opacity: 1, x: 700, duration: 1.2, ease: "sine.inOut" }}, {s});')
win("#flb", s, e, "up", out=False)
js(f'tl.fromTo("#fl", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {round(s + 0.1, 3)});')
js(f'tl.fromTo("#fd", {{ scale: 0, transformOrigin: "110px 1640px" }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {round(s + 0.3, 3)});')
s, e = src(147.35), src(152.85)
grp("g-meja", s, e, '<div class="size"><div class="sk">RUANG MAKAN</div><div class="sv">16 × 8 <small>KAKI</small></div></div>',
    "left:90px; right:90px; top:250px; display:flex; justify-content:center")
win("#g-meja .size", s, e, "pop")
s, e = src(156.40), src(157.10) + 0.0
grp("g-seat", s, cut("dapur") + 1.2, f'<div class="card"><div class="ic">{CHAIR}</div><div class="ct"><span class="dk">8</span> TEMPAT DUDUK</div></div>',
    "left:90px; right:90px; top:260px; display:flex; justify-content:center")
win("#g-seat .card", s, cut("dapur") + 1.2, "pop")

# --- 6. pantry
s, e = src(169.55), src(176.0)
grp("g-kering", s, e, '<div class="tag" id="kg1">DAPUR <span class="y">KERING</span></div><div class="pill sm" id="kg2">DEKAT DENGAN RUANG MAKAN</div>',
    "left:90px; right:90px; top:250px; display:flex; flex-direction:column; align-items:center; gap:16px")
win("#kg1", s, e, "up", out=False); js('tl.set("#kg2", { opacity: 0 }, 0);'); win("#kg2", src(173.75), e, "up", out=False)
js(f'tl.to("#g-kering", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')

# --- 7. wet kitchen: title as the sliding door swings open, then size, then white
s, e = src(192.35), src(198.0)
grp("g-basah", s, e, '<div class="tag" id="bs1">DAPUR <span class="y">BASAH</span></div>',
    "left:90px; right:90px; top:250px; display:flex; justify-content:center")
win("#bs1", s, e, "left")
s, e = src(198.10), src(203.5)
grp("g-ten", s, e, '<div class="size"><div class="sk">DAPUR BASAH</div><div class="sv">10 × 10 <small>KAKI</small></div></div>',
    "left:90px; right:90px; top:250px; display:flex; justify-content:center")
win("#g-ten .size", s, e, "pop")
s, e = src(205.85), src(213.9)
grp("g-putih", s, e, '<div class="pill"><span class="dot w"></span>PUTIH <span class="sep">•</span> <span class="y">NAMPAK LEBIH LUAS</span></div>',
    "left:90px; right:90px; top:270px; display:flex; justify-content:center")
win("#g-putih .pill", s, e, "pop")

# --- 8. door to the porch: thin yellow outline on the real door, label, food icon
s, e = src(217.75), src(222.6)
el(f'<div class="g clip" id="g-pdoor" data-start="{s}" data-duration="{round(e - s, 3)}" style="inset:0">'
   '<svg class="ln" viewBox="0 0 1080 1920"><rect id="pdo" x="424" y="575" width="476" height="1180" rx="6" class="ol"/></svg>'
   '<div class="lbl big" id="pdl" style="left:0; right:0; top:300px; margin:0 auto; width:max-content">AKSES TERUS KE <span class="y2">PORCH</span></div></div>')
js(f'tl.fromTo("#pdo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {s});')
# measured door frame (left, width) at film times on the rendered frames
KF = [(154.21, 424, 476), (154.5, 424, 476), (155.3, 465, 465), (156.1, 471, 437), (156.9, 424, 477), (157.7, 397, 438), (158.5, 412, 417), (159.06, 412, 417)]
js(f'tl.set("#pdo", {{ attr: {{ x: {KF[0][1]}, width: {KF[0][2]} }} }}, {KF[0][0]});')
for (t0, x0, w0), (t1, x1, w1) in zip(KF, KF[1:]):
    js(f'tl.to("#pdo", {{ attr: {{ x: {x1}, width: {w1} }}, duration: {round(t1 - t0, 3)}, ease: "sine.inOut" }}, {t0});')
win("#pdl", s + 0.1, e, "up", out=False)
js(f'tl.to("#g-pdoor", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, {round(e - 0.2, 3)});')
s, e = src(226.4), src(231.0)
grp("g-food", s, e, f'<div class="card"><div class="ic">{DISH}</div><div class="ct">MAKANAN &amp; BARANG<br><span class="dk">TERUS KE PORCH</span></div></div>',
    "left:90px; right:90px; top:260px; display:flex; justify-content:center")
win("#g-food .card", s, e, "pop")

CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: #fff; }
    .g { position: absolute; }
    .y { color: #F6C343; }
    .cap { max-width: 900px; padding: 14px 28px 16px; border-radius: 22px; background: rgba(10,12,16,.62); text-align: center;
      font-weight: 800; font-size: 50px; line-height: 1.18; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.35); opacity: 0; }
    .hk { font-weight: 900; font-size: 128px; line-height: 1.02; letter-spacing: -.01em; white-space: nowrap; opacity: 0;
      text-shadow: 0 6px 0 rgba(0,0,0,.25), 0 14px 40px rgba(0,0,0,.6); }
    .hk.w { color: #fff; } .hk.y { color: #F6C343; font-size: 140px; }
    .tag { padding: 14px 34px 16px; border-radius: 18px; background: rgba(10,12,16,.72); font-weight: 900; font-size: 62px;
      letter-spacing: .02em; white-space: nowrap; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.35); text-shadow: 0 3px 10px rgba(0,0,0,.4); }
    .tag.sm { font-size: 52px; }
    .loc { display: flex; align-items: center; gap: 14px; padding: 12px 30px 14px 20px; border-radius: 999px; background: #fff; color: #14161B;
      font-weight: 900; font-size: 40px; letter-spacing: .06em; white-space: nowrap; opacity: 0; box-shadow: 0 14px 34px rgba(0,0,0,.35); }
    .pill { display: flex; align-items: center; gap: 14px; padding: 16px 36px 18px; border-radius: 999px; background: rgba(10,12,16,.75);
      border: 3px solid #F6C343; font-weight: 900; font-size: 50px; letter-spacing: .04em; white-space: nowrap; opacity: 0;
      box-shadow: 0 16px 40px rgba(0,0,0,.35); }
    .pill.sm { font-size: 36px; letter-spacing: .1em; padding: 12px 30px 14px; border-width: 2px; }
    .pill .sep { color: #F6C343; }
    .dot { width: 30px; height: 30px; border-radius: 50%; border: 3px solid #fff; }
    .dot.k { background: #0B0C0E; } .dot.w { background: #fff; border-color: #F6C343; }
    .cars { display: flex; gap: 22px; padding: 18px 26px; border-radius: 24px; background: rgba(10,12,16,.7); }
    .car { opacity: 0; }
    .card { display: flex; align-items: center; gap: 22px; padding: 18px 40px 20px 20px; border-radius: 26px; background: #F6C343; color: #14161B;
      opacity: 0; box-shadow: 0 18px 44px rgba(0,0,0,.4); }
    .card .ic { width: 116px; height: 116px; border-radius: 22px; background: #fff; display: flex; align-items: center; justify-content: center; flex: none; }
    .card .ct { font-weight: 900; font-size: 46px; line-height: 1.08; white-space: nowrap; }
    .card .dk { color: #fff; background: #14161B; padding: 0 12px 4px; border-radius: 10px; }
    .size { padding: 18px 42px 22px; border-radius: 26px; background: #fff; color: #14161B; text-align: center; opacity: 0;
      box-shadow: 0 18px 44px rgba(0,0,0,.4); border-bottom: 10px solid #F6C343; }
    .size .sk { font-weight: 800; font-size: 30px; letter-spacing: .2em; color: #6B6F76; }
    .size .sv { font-weight: 900; font-size: 104px; line-height: 1.0; white-space: nowrap; }
    .size .sv small { font-size: 46px; color: #B88A0E; letter-spacing: .06em; }
    .ln { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
    .ln path { fill: none; stroke: #F6C343; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 100;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,.5)); }
    .ln circle { fill: #F6C343; stroke: #fff; stroke-width: 4; }
    .lbl { position: absolute; padding: 12px 28px 14px; border-radius: 16px; background: #F6C343; color: #14161B; font-weight: 900;
      font-size: 44px; letter-spacing: .04em; white-space: nowrap; opacity: 0; box-shadow: 0 14px 34px rgba(0,0,0,.4); }
    .lbl.big { font-size: 50px; background: rgba(10,12,16,.78); color: #fff; border: 3px solid #F6C343; }
    .lbl .y2 { color: #F6C343; }
    .sweep { position: absolute; left: 0; top: 1520px; width: 420px; height: 400px; opacity: 0;
      background: linear-gradient(100deg, rgba(246,195,67,0), rgba(246,195,67,.28) 50%, rgba(246,195,67,0)); }
    .ln rect.ol { fill: none; stroke: #F6C343; stroke-width: 5; filter: drop-shadow(0 0 8px rgba(246,195,67,.6)); opacity: 0; }
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
print("TOTAL", TOTAL, "captions", len(caps))
print({k: v for k, v in start.items()})
