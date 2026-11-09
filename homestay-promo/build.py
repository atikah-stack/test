#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman
"Pakej Tanah & Bina Rumah (Homestay)" video (1080x1920).

The presenter take (Google Drive original, 720p upscaled to 1080p) plays the whole way
with its own sound. B-roll (drone, lot plan, renders) sits on top, muted. All times are
seconds of the presenter take, from a whisper pass checked against the user's transcript.

Safe zone: the top and bottom 20% (Y < 384 and Y > 1536) carry no text, icons or
graphics. Subtitles sit in a box at Y 1390-1530, which also covers the CapCut captions
that are burned into the source take.
"""
import json

MAR, MAR_D, YEL, WHT, INK = "#7A1530", "#4A0C1C", "#FFD400", "#FFFFFF", "#1A1014"
SAFE_TOP, SAFE_BOT = 384, 1536
TOTAL = 79.45

# ---------------- subtitles (user's transcript text, whisper start times) ----------------
# **word** = yellow highlight
SUBS = [
    (0.15, "Ada ke mana-mana orang sini tengah cari tanah nak buat **homestay**?"),
    (4.00, "Kiranya nak **tambah sumber pendapatan** lah."),
    (6.26, "Ramai deh bila nak buat homestay je, duk pilih nak **Scandinavian** lah."),
    (9.83, "**Bali** lah, ada **kolam** lah, macam-macam."),
    (11.77, "Tapi pemilihan tanah pun kena pilih hok **strategik**, tuan-puan."),
    (15.32, "Contohnya tanah sini deh."),
    (16.93, "Ha, ni tanah ni."),
    (18.00, "Baru bangun pagi tengok **view**-nya dengan comelnya."),
    (20.85, "Dengan **hutan bukit-bukau** gitu."),
    (23.16, "**Lima minit** je dari **Bandar Machang**."),
    (26.04, "Tuan-puan tahu dak?"),
    (26.76, "Tinggal **beberapa lot** je lagi tanah hok kita ada ni."),
    (29.28, "Dan setiap keluasan lot tu kan bermula dengan…"),
    (32.19, "**5,101 kaki persegi.**"),
    (34.24, "Tuan-puan boleh buat rumah pula bermula dengan **1,400 kaki persegi.**"),
    (37.96, "Ha, pastu design pun saya kata saat ni…"),
    (40.08, "Memang boleh **custom**."),
    (41.32, "Nak design lagu mana biar…"),
    (42.47, "Kalau buat tu biar orang kenal."),
    (43.70, "Nak mari **booking** lalu homestay tu."),
    (45.96, "Tengoklah kawasan dia dengan kawasan **bebas banjirnya**."),
    (49.60, "**Lima minit** je nak ke Bandar Machang…"),
    (51.73, "Pastu ha ni kalau buat homestay…"),
    (53.70, "Orang tak takut nak mari."),
    (54.98, "Sebabnya tengok **kawasan kejiranan** dia ada dah."),
    (57.68, "Memang **complete** banyak dah rumah kawasan ni."),
    (60.84, "Harga, aa, untuk setiap lot tu nanti harga dia…"),
    (63.49, "Pakej rumah berserta bina rumah ni bermula dengan harga dia…"),
    (67.86, "**RM390,000.**"),
    (69.95, "**Sahaja.**"),
    (71.12, "Tuan-puan **klik dulu link bawah.**"),
    (72.99, "Kita try buat kira."),
    (74.32, "Yang pasti tuan-puan boleh **buat homestay.**"),
    (76.68, "Boleh **tambah pendapatan.**"),
    (77.75, "**Klik link bawah** selalu deh. Bye-bye!"),
]

# ---------------- B-roll video cutaways: (id, file, start, end, media start, push) ----------------
BROLL = [
    ("b-estate1", "drone-estate", 13.40, 16.90, 0.5, True),
    ("b-hills", "drone-hills", 18.00, 23.10, 1.0, True),
    ("b-lots", "lot-tersedia", 26.70, 31.00, 0.3, False),   # real lot plan with its own labels: no crop
    ("b-top", "drone-top", 31.00, 34.20, 0.3, True),
    ("b-estate2", "drone-estate", 46.60, 49.50, 5.5, True),
    ("b-hills2", "drone-hills", 58.60, 60.80, 6.5, True),
]

vids = [
    '      <div id="w-talent" style="position:absolute; inset:0; z-index:1; overflow:hidden; transform-origin: 50% 45%">'
    f'<video id="v-talent" class="clip" src="assets/video/talent.mp4" data-start="0" data-duration="{TOTAL}" '
    'data-media-start="0" data-track-index="1" playsinline data-has-audio="true" data-volume="1" '
    'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video></div>'
]
for bid, f, s, e, m, _ in BROLL:
    vids.append(
        f'      <div id="{bid}-w" style="position:absolute; inset:0; z-index:2; overflow:hidden">'
        f'<video id="{bid}" src="assets/video/{f}.mp4" data-start="{s}" data-duration="{round(e - s, 3)}" '
        f'data-media-start="{m}" data-track-index="2" class="clip" muted playsinline '
        f'style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video></div>'
    )

# ---------------- sound ----------------
AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{TOTAL}" '
       f'data-track-index="4" data-volume="0.11" data-fade-out="1.5"></audio>']


def sfx(name, file, at, dur, vol):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{file}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{dur}" data-track-index="{5 + len(AUD) % 3}" data-volume="{vol}"></audio>')


W, P, I, PG, C, CL, CH = "whoosh-short", "pop", "impact-bass-1", "ping", "click-soft", "click", "chime"
for name, f, at, d, v in [
    ("h0", W, 0.30, 0.57, 0.26), ("h1", P, 2.31, 0.72, 0.24), ("h2", P, 2.80, 0.72, 0.24), ("h3", I, 3.36, 1.6, 0.34),
    ("inc", W, 4.00, 0.57, 0.24), ("coins", C, 4.30, 0.36, 0.3), ("coins2", C, 4.55, 0.36, 0.3), ("bars", PG, 5.23, 1.0, 0.2),
    ("rnd", "whoosh", 7.24, 0.57, 0.3), ("sc", P, 8.92, 0.72, 0.26), ("bali", P, 9.83, 0.72, 0.26), ("pool", P, 10.40, 0.72, 0.26),
    ("est", W, 13.38, 0.57, 0.26), ("pin", P, 13.84, 0.72, 0.28), ("strat", PG, 14.10, 1.0, 0.18),
    ("hills", "whoosh", 17.98, 0.57, 0.28), ("view", P, 19.30, 0.72, 0.24), ("hutan", C, 21.16, 0.36, 0.3),
    ("route", W, 23.14, 0.57, 0.26), ("car", "whoosh", 23.90, 0.57, 0.2), ("min", P, 24.00, 0.72, 0.26),
    ("lots", W, 26.68, 0.57, 0.26), ("lotsl", I, 27.18, 1.6, 0.3),
    ("top", W, 30.98, 0.57, 0.26), ("kl", P, 31.24, 0.72, 0.24), ("n5101", PG, 32.90, 1.0, 0.24),
    ("r3", W, 34.98, 0.57, 0.26), ("bl", P, 35.75, 0.72, 0.24), ("n1400", PG, 37.25, 1.0, 0.24),
    ("cust", "whoosh", 39.98, 0.57, 0.28), ("custl", P, 40.56, 0.72, 0.28), ("plan", C, 41.0, 0.36, 0.26), ("cita", P, 41.85, 0.72, 0.22),
    ("phone", W, 43.58, 0.57, 0.26), ("book", CL, 44.16, 0.36, 0.32), ("conf", CH, 44.80, 1.6, 0.22),
    ("est2", W, 46.58, 0.57, 0.26), ("flood", CH, 48.39, 1.6, 0.24),
    ("car2", W, 49.60, 0.57, 0.26), ("car2p", P, 49.77, 0.72, 0.24),
    ("r4", W, 52.48, 0.57, 0.26), ("sesuai", P, 53.10, 0.72, 0.26),
    ("kj", P, 55.77, 0.72, 0.24), ("comp", I, 57.92, 1.6, 0.3), ("hills2", W, 58.58, 0.57, 0.24),
    ("pkg", P, 63.49, 0.72, 0.26), ("riser", "riser", 67.86 - 10.03, 10.03, 0.12),
    ("price", "whoosh", 65.76, 0.57, 0.3), ("rm", I, 67.86, 1.6, 0.38), ("sahaja", P, 69.95, 0.72, 0.3),
    ("link", W, 71.10, 0.57, 0.26), ("tap1", CL, 72.30, 0.36, 0.34), ("tap2", CL, 72.80, 0.36, 0.34),
    ("fin", "whoosh", 74.30, 0.57, 0.28), ("fin1", P, 75.85, 0.72, 0.26), ("fin2", PG, 76.68, 1.0, 0.22),
    ("cta", I, 77.75, 1.6, 0.3), ("ctatap", CL, 78.45, 0.36, 0.34),
]:
    sfx(name, f, at, d, v)

PUNCH = [(3.36, 0.9), (32.19, 0.0), (49.60, 1.0), (63.49, 1.4), (77.75, 1.2)]
PUNCH = [p for p in PUNCH if p[1] > 0]
push = [(b[0], b[2], b[3]) for b in BROLL if b[5]]
fades = [(b[0], b[2]) for b in BROLL]

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
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(fades)}.forEach(([id, s]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.16, ease: "power1.out" }}, s);
      }});
      {json.dumps(push)}.forEach(([id, s, e]) => {{
        tl.fromTo("#" + id + "-w", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, s);
        tl.fromTo("#" + id, {{ scale: 1.0 }}, {{ scale: 1.07, duration: e - s, ease: "none" }}, s);
      }});
      // presenter stays unscaled: the subtitle box must keep covering the captions burned into the take
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ================= gfx =================
def svg(body, size=56, stroke=INK, sw=3.6, fill="none", vb="0 0 48 48"):
    return (f'<svg viewBox="{vb}" width="{size}" height="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


ICON = {
    "house": svg('<path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M20 43V31h8v12"/>', 84, WHT, 3.4),
    "pin": f'<svg viewBox="0 0 48 64" width="64" height="84"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}" stroke="{INK}" stroke-width="2"/><circle cx="24" cy="24" r="8.5" fill="{MAR}"/></svg>',
    "pin_s": f'<svg viewBox="0 0 48 64" width="40" height="52"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{MAR}"/><circle cx="24" cy="24" r="8.5" fill="{WHT}"/></svg>',
    "mount": svg('<path d="M2 40 17 18l9 12 6-8 14 18z"/><circle cx="36" cy="10" r="4"/>', 70, WHT, 3.2),
    "lot": svg('<path d="M4 32 24 22l20 10-20 10z"/><path d="M24 22V6"/><path d="M24 6l12 4-12 4" fill="#1A1014"/>', 64),
    "home2": svg('<path d="M4 22 24 6l20 16"/><path d="M9 19v24h30V19"/><path d="M20 43V31h8v12"/>', 64),
    "shield": svg('<path d="M24 4 7 10v12c0 11 7.5 18.5 17 22 9.5-3.5 17-11 17-22V10z"/><path d="M16 24l6 6 10-11"/>', 64),
    "car": svg('<path d="M6 30l4-10c1-3 3-4 6-4h16c3 0 5 1 6 4l4 10"/><rect x="4" y="30" width="40" height="9" rx="3"/><circle cx="13" cy="40" r="3.5" fill="#1A1014"/><circle cx="35" cy="40" r="3.5" fill="#1A1014"/>', 64),
    "bed": svg('<path d="M4 38V12M4 30h40v8M44 30v-6c0-3-2-5-5-5H20v11"/><circle cx="12" cy="24" r="4"/>', 64),
    "homes": svg('<path d="M2 26 14 16l12 10"/><path d="M5 24v18h18V24"/><path d="M22 20 34 10l12 10"/><path d="M26 18v24h17V18"/>', 64),
    "link": svg('<path d="M20 28a8 8 0 0 0 12 1l6-6a8 8 0 0 0-11-11l-3 3"/><path d="M28 20a8 8 0 0 0-12-1l-6 6a8 8 0 0 0 11 11l3-3"/>', 96, INK, 4.2),
}
HAND = f'<svg viewBox="0 0 64 72" width="86" height="96"><path d="M22 6c0-3 2-5 5-5s5 2 5 5v24l3-1c3-1 6 1 6 4l8-2c3 0 5 2 5 5v14c0 10-7 20-19 20h-6c-7 0-11-3-14-8L4 44c-2-3-1-6 2-7 2-1 5 0 6 2l10 10z" fill="{WHT}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/></svg>'

H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.45):
    frm = {"up": "{ opacity: 0, y: 30 }", "scale": "{ opacity: 0, scale: 0.8 }", "fade": "{ opacity: 0 }",
           "flip": "{ opacity: 0, rotationX: -80 }", "pop": "{ opacity: 0, scale: 0.4 }"}[kind]
    ease = "back.out(1.8)" if kind == "pop" else "expo.out"
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, rotationX: 0, duration: {d}, ease: "{ease}" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def tout(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, y: -18, duration: 0.22, ease: "power2.in" }}, {round(at, 3)});')


def block(bid, s, e, inner, top, height, cls="col"):
    BOXES.append((bid, top, height))
    H.append(f'    <div class="grp clip {cls}" id="{bid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" '
             f'style="top:{top}px; height:{height}px">{inner}</div>')


def scene(sid, s, e, inner):
    """a full-frame graphic cutaway (its own background) placed under the labels"""
    H.append(f'    <div class="scn clip" id="{sid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}">{inner}</div>')
    J.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }}, {s});')


def count(sel, to, at, d=0.8, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {at}); }})();')


def hl(text):
    out, on = "", False
    for i, part in enumerate(text.split("**")):
        out += f'<b>{part}</b>' if i % 2 else part
    return out


# --- 1. hook: NAK BUAT HOMESTAY?
block("g-hook", 0.30, 3.95, f'''<div class="ic-house" id="hk-i">{ICON["house"]}</div>
      <div class="lbl mr sm" id="hk0">CARI TANAH?</div>
      <div class="lbl wh lg" id="hk1">NAK BUAT</div>
      <div class="lbl yl xl" id="hk2">HOMESTAY?</div>''', 400, 400)
tin("#hk-i", 0.30, "pop")
J.append('tl.fromTo("#hk-i path", { strokeDasharray: 120, strokeDashoffset: 120 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out" }, 0.35);')
for k, at in [("hk0", 2.31), ("hk1", 2.80), ("hk2", 3.36)]:
    hide(f"#{k}"); tin(f"#{k}", at, "pop", 0.4)
tout("#g-hook", 3.72)

# --- 2. tambah sumber pendapatan: coins + rising bars
bars = "".join(f'<div class="bar" id="bar{i}" style="height:{h}px"></div>' for i, h in enumerate([60, 100, 145, 195]))
coins = "".join(f'<div class="coin" id="coin{i}" style="bottom:{i * 20}px"></div>' for i in range(5))
block("g-inc", 4.00, 6.20, f'''<div class="incw"><div class="coins">{coins}</div><div class="bars">{bars}
      <svg class="arrow" viewBox="0 0 240 200" width="240" height="200"><path id="arr" d="M10 180 L80 120 L130 140 L225 30" fill="none" stroke="{YEL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
      <path id="arrh" d="M190 26 L228 26 L228 64" fill="none" stroke="{YEL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
      <div class="lbl mr md" id="inc-t">TAMBAH <span class="y">SUMBER PENDAPATAN</span></div>''', 400, 360)
tin("#g-inc .incw", 4.0, "fade", 0.3)
for i in range(5):
    J.append(f'tl.fromTo("#coin{i}", {{ y: -260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "bounce.out" }}, {round(4.15 + i * 0.12, 3)});')
for i in range(4):
    J.append(f'tl.fromTo("#bar{i}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "back.out(1.6)" }}, {round(4.6 + i * 0.1, 3)});')
J.append('tl.fromTo("#arr", { strokeDasharray: 330, strokeDashoffset: 330 }, { strokeDashoffset: 0, duration: 0.55, ease: "power2.out" }, 5.0);')
J.append('tl.fromTo("#arrh", { opacity: 0 }, { opacity: 1, duration: 0.15 }, 5.45);')
hide("#inc-t"); tin("#inc-t", 4.45, "up")
tout("#g-inc", 5.98)

# --- 3. homestay concepts: renders montage (chips are the words she says)
rimgs = ["render-1", "render-2", "render-5"]
cards = "".join(f'<div class="rc3d" id="rc{i}"><img src="assets/img/{n}.jpg" alt="" /></div>' for i, n in enumerate(rimgs))
scene("s-concept", 7.24, 11.70, f'''<div class="bgblur"><img src="assets/img/render-2.jpg" alt="" /></div><div class="dim"></div>
      <div class="stage">{cards}</div>''')
step = (11.70 - 7.24) / 3
for i in range(3):
    a = round(7.24 + i * step, 3)
    J.append(f'tl.fromTo("#rc{i}", {{ opacity: 0, rotationY: -35, x: 120 }}, {{ opacity: 1, rotationY: 0, x: 0, duration: 0.6, ease: "expo.out" }}, {a});')
    J.append(f'tl.fromTo("#rc{i} img", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {round(step + 0.4, 2)}, ease: "none" }}, {a});')
    if i < 2:
        J.append(f'tl.to("#rc{i}", {{ opacity: 0, rotationY: 35, x: -120, duration: 0.4, ease: "power2.in" }}, {round(a + step - 0.15, 3)});')
block("g-concept-h", 7.24, 11.70, '<div class="lbl mr sm" id="cc-h">PILIHAN KONSEP HOMESTAY</div>', 410, 80)
block("g-concept", 7.24, 11.70, '''<div class="chips"><div class="chip" id="ch0">SCANDINAVIAN</div><div class="chip" id="ch1">BALI</div>
      <div class="chip" id="ch2">KOLAM RENANG</div></div>''', 1250, 100)
tin("#cc-h", 7.30, "up")
for i, at in enumerate([8.92, 9.83, 10.40]):
    hide(f"#ch{i}"); tin(f"#ch{i}", at, "pop", 0.4)
tout("#g-concept-h", 11.48); tout("#g-concept", 11.48)

# --- 4. pilih lokasi strategik (over drone of the land)
block("g-strat", 13.84, 16.90, f'''<div class="pinw" id="st-pin">{ICON["pin"]}<div class="ring" id="st-ring"></div></div>
      <div class="lbl wh lg" id="st1">PILIH LOKASI</div><div class="lbl yl xl" id="st2">STRATEGIK</div>''', 420, 400)
J.append('tl.fromTo("#st-pin", { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out" }, 13.84);')
J.append('tl.fromTo("#st-ring", { scale: 0.3, opacity: 0.9 }, { scale: 2.2, opacity: 0, duration: 1.0, ease: "power2.out", repeat: 1, immediateRender: false }, 14.3);')
hide("#st1"); tin("#st1", 14.05, "up"); hide("#st2"); tin("#st2", 14.30, "pop")
tout("#g-strat", 16.68)

# --- 5. view cantik (over hills drone)
block("g-view", 19.10, 23.10, f'''<div class="ic-m" id="vw-i">{ICON["mount"]}</div>
      <div class="lbl mr lg" id="vw1">VIEW <span class="y">CANTIK</span> &amp; ALAMI</div>
      <div class="lbl wh md" id="vw2">HUTAN BUKIT-BUKAU</div>''', 420, 360)
tin("#vw-i", 19.10, "pop")
J.append('tl.fromTo("#vw-i path, #vw-i circle", { strokeDasharray: 160, strokeDashoffset: 160 }, { strokeDashoffset: 0, duration: 1.0, ease: "power2.out" }, 19.15);')
hide("#vw1"); tin("#vw1", 19.30, "up"); hide("#vw2"); tin("#vw2", 21.16, "up")
tout("#g-view", 22.88)

# --- 6. 5 minit dari Bandar Machang: diagram card over the aerial still
scene("s-route", 23.16, 26.04, '''<div class="kb"><img id="rt-bg" src="assets/img/aerial-angle.jpg" alt="" /></div><div class="dim l"></div>''')
J.append('tl.fromTo("#rt-bg", { scale: 1.05 }, { scale: 1.15, duration: 2.9, ease: "none" }, 23.16);')
block("g-route", 23.16, 26.04, f'''<div class="route" id="rt">
        <div class="rt-a"><div class="rt-pin">{ICON["pin_s"]}</div><div class="rt-l">BANDAR<br/>MACHANG</div></div>
        <div class="rt-line"><div class="rt-dash" id="rt-dash"></div><div class="rt-car" id="rt-car">{ICON["car"]}</div></div>
        <div class="rt-b"><div class="rt-home">{ICON["home2"]}</div><div class="rt-l">TANAH<br/>KITA</div></div>
      </div>
      <div class="big5" id="rt-5"><span class="y">5 MINIT</span></div><div class="lbl wh md" id="rt-s">DARI BANDAR MACHANG</div>''', 640, 620)
tin("#rt", 23.20, "scale")
J.append('tl.fromTo("#rt-dash", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.out" }, 23.40);')
J.append('tl.fromTo("#rt-car", { x: 0 }, { x: 330, duration: 1.4, ease: "power1.inOut" }, 23.90);')
hide("#rt-5"); tin("#rt-5", 24.00, "pop"); hide("#rt-s"); tin("#rt-s", 24.36, "up")
tout("#g-route", 25.82)

# --- 7. tinggal beberapa lot (over the real lot plan; low so its lot labels stay clear)
block("g-lots", 27.10, 31.00, '''<div class="lbl mr md" id="lt0">TINGGAL</div><div class="lbl yl lg" id="lt1">BEBERAPA LOT</div>
      <div class="lbl wh md" id="lt2">SAHAJA LAGI!</div>''', 1000, 360)
tin("#lt0", 27.10, "up"); hide("#lt1"); tin("#lt1", 27.18, "pop"); hide("#lt2"); tin("#lt2", 28.05, "up")
tout("#g-lots", 30.80)

# --- 8. keluasan lot 5,101 (over top-down drone)
block("g-5101", 31.24, 34.20, f'''<div class="stat" id="ks"><div class="si">{ICON["lot"]}</div><div><div class="sk">KELUASAN LOT BERMULA</div>
      <div class="sv"><span class="y" id="n5101">5,101</span> <small>KPS</small></div></div></div>''', 820, 220)
tin("#ks", 31.24, "scale")
count("#n5101", 5101, 32.19)
tout("#g-5101", 34.0)

# --- 9. bina rumah 1,400 (render)
scene("s-1400", 35.00, 37.90, '''<div class="kb"><img id="r3" src="assets/img/render-3.jpg" alt="" /></div><div class="dim l"></div>''')
J.append('tl.fromTo("#r3", { scale: 1.02 }, { scale: 1.12, duration: 2.9, ease: "none" }, 35.0);')
block("g-1400", 35.75, 37.90, f'''<div class="stat" id="bs"><div class="si">{ICON["home2"]}</div><div><div class="sk">BINA RUMAH BERMULA</div>
      <div class="sv"><span class="y" id="n1400">1,400</span> <small>KPS</small></div></div></div>''', 1030, 220)
tin("#bs", 35.75, "scale")
count("#n1400", 1400, 36.57)
tout("#g-1400", 37.70)

# --- 10. custom design: renders + floor plan drawing
plan = f'''<svg viewBox="0 0 300 220" width="380" height="279" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
        <path class="pl" d="M10 10 H290 V210 H10 Z"/><path class="pl" d="M150 10 V120 M10 120 H200 M200 120 V210 M150 60 H290"/>
        <path class="pl" d="M60 120 v-26 M240 60 v28 M110 210 v-30"/><path class="pl" d="M40 150 h50 v40 h-50 z" stroke-width="3"/></svg>'''
scene("s-custom", 40.00, 43.60, f'''<div class="bgblur"><img src="assets/img/render-4.jpg" alt="" /></div><div class="dim"></div>
      <div class="cst"><div class="rc3d sm" id="cr1"><img src="assets/img/render-4.jpg" alt="" /></div>
      <div class="planc" id="pl">{plan}</div></div>''')
J.append('tl.fromTo("#cr1", { rotationY: -30, opacity: 0, x: -80 }, { rotationY: -8, opacity: 1, x: 0, duration: 0.7, ease: "expo.out" }, 40.05);')
J.append('tl.fromTo("#pl", { rotationY: 30, opacity: 0, x: 80 }, { rotationY: 8, opacity: 1, x: 0, duration: 0.7, ease: "expo.out" }, 40.35);')
J.append('tl.fromTo("#pl .pl", { strokeDasharray: 1000, strokeDashoffset: 1000 }, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut", stagger: 0.12 }, 40.6);')
block("g-custom", 40.56, 43.60, '<div class="lbl yl xl" id="cu1">CUSTOM DESIGN</div>', 420, 140)
block("g-custom2", 41.85, 43.60, '<div class="lbl mr md" id="cu2">MENGIKUT CITA RASA</div>', 1240, 110)
tin("#cu1", 40.56, "pop"); tin("#cu2", 41.85, "up")
tout("#g-custom", 43.40); tout("#g-custom2", 43.40)

# --- 11. mudah untuk booking: phone mockup
scene("s-book", 43.60, 45.96, '''<div class="bgblur"><img src="assets/img/render-5.jpg" alt="" /></div><div class="dim"></div>''')
block("g-book", 43.60, 45.96, f'''<div class="phone" id="ph"><div class="scr">
        <div class="ph-h">Homestay Booking</div>
        <div class="cal" id="cal">{"".join(f'<i class="d{" on" if k == 17 else ""}" id="{"dsel" if k == 17 else ""}"></i>' for k in range(28))}</div>
        <div class="ph-btn" id="ph-btn">TEMPAH</div>
        <div class="ok" id="ok"><div class="okc">{svg('<path d="M10 25l9 9 19-20"/>', 46, WHT, 6)}</div><div>Tempahan<br/>Disahkan</div></div>
      </div><div class="hand ph-hand" id="ph-hand">{HAND}</div></div>''', 420, 760)
J.append('tl.fromTo("#ph", { rotationY: -28, rotationX: 10, opacity: 0, y: 60 }, { rotationY: -10, rotationX: 4, opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, 43.62);')
J.append('tl.fromTo("#ph-hand", { opacity: 0, x: 80, y: 80 }, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }, 43.85);')
J.append('tl.fromTo("#ph-hand", { scale: 1 }, { scale: 0.86, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }, 44.16);')
J.append('tl.fromTo("#dsel", { backgroundColor: "#EADBDF" }, { backgroundColor: "#7A1530", duration: 0.15 }, 44.20);')
J.append('tl.fromTo("#ok", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 44.80);')
block("g-book2", 43.80, 45.96, '<div class="lbl wh md" id="bk1">MUDAH UNTUK <span class="mrt">BOOKING</span></div>', 1250, 110)
tin("#bk1", 43.90, "up")
tout("#g-book", 45.74); tout("#g-book2", 45.74)

# --- 12. bebas banjir (over drone)
block("g-flood", 48.20, 49.50, f'''<div class="shield" id="fl-s">{svg('<path d="M24 4 7 10v12c0 11 7.5 18.5 17 22 9.5-3.5 17-11 17-22V10z" fill="#7A1530" stroke="#FFFFFF"/><path d="M16 24l6 6 10-11" stroke="#FFD400" stroke-width="5"/>', 150, WHT, 3)}</div>
      <div class="lbl wh md" id="fl1">KAWASAN</div><div class="lbl yl xl" id="fl2">BEBAS BANJIR</div>''', 420, 450)
tin("#fl-s", 48.20, "pop"); hide("#fl1"); tin("#fl1", 48.30, "up"); hide("#fl2"); tin("#fl2", 48.39, "pop")
J.append('tl.to("#fl-s", { y: -10, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 48.7);')
tout("#g-flood", 49.32)

# --- 13. hanya 5 minit ke bandar (presenter on the road)
block("g-5min", 49.60, 51.70, f'''<div class="row"><div class="ic-car" id="cr-i">{ICON["car"]}</div><div class="lbl wh md" id="m1">HANYA</div></div>
      <div class="lbl yl xl" id="m2">5 MINIT</div><div class="lbl mr md" id="m3">KE BANDAR</div>''', 400, 340)
J.append('tl.fromTo("#cr-i", { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, 49.60);')
tin("#m1", 49.62, "up"); hide("#m2"); tin("#m2", 49.77, "pop"); hide("#m3"); tin("#m3", 50.85, "up")
tout("#g-5min", 51.50)

# --- 14. sesuai untuk homestay (render)
scene("s-sesuai", 52.50, 54.96, '''<div class="kb"><img id="r4" src="assets/img/render-4.jpg" alt="" /></div><div class="dim l"></div>''')
J.append('tl.fromTo("#r4", { scale: 1.02, x: 0 }, { scale: 1.14, x: -30, duration: 2.5, ease: "none" }, 52.5);')
block("g-sesuai", 52.90, 54.96, f'''<div class="ic-bed" id="sb-i">{ICON["bed"]}</div><div class="lbl wh md" id="sb1">SESUAI UNTUK</div>
      <div class="lbl yl xl" id="sb2">HOMESTAY</div>''', 1000, 360)
tin("#sb-i", 52.90, "pop"); hide("#sb1"); tin("#sb1", 52.95, "up"); hide("#sb2"); tin("#sb2", 53.10, "pop")
tout("#g-sesuai", 54.76)

# --- 15. kawasan kejiranan complete
block("g-kj", 55.77, 60.80, f'''<div class="ic-homes" id="kj-i">{ICON["homes"]}</div><div class="lbl wh md" id="kj1">KAWASAN KEJIRANAN</div>
      <div class="lbl yl xl" id="kj2">COMPLETE</div>''', 400, 340)
tin("#kj-i", 55.77, "pop"); tin("#kj1", 55.80, "up"); hide("#kj2"); tin("#kj2", 57.92, "pop")
tout("#g-kj", 60.58)

# --- 16. pakej tanah berserta bina rumah
block("g-pkg", 63.49, 65.76, '''<div class="lbl mr lg" id="pk1">PAKEJ TANAH</div><div class="lbl wh md" id="pk2">BERSERTA</div>
      <div class="lbl yl xl" id="pk3">BINA RUMAH</div>''', 400, 340)
tin("#pk1", 63.49, "pop"); hide("#pk2"); tin("#pk2", 64.04, "up"); hide("#pk3"); tin("#pk3", 64.43, "pop")
tout("#g-pkg", 65.56)

# --- 17. harga RM390,000 (maroon card over the presenter, blurred)
scene("s-price", 65.78, 71.10, '<div class="pricebg"></div>')
block("g-price", 65.78, 71.10, '''<div class="pk" id="pr0">BERMULA DENGAN</div><div class="pk big" id="pr1">HARGA</div>
      <div class="rm" id="pr2"><span id="nrm">RM390,000</span></div><div class="uline" id="pr-u"></div>
      <div class="pk" id="pr3">SAHAJA</div>''', 560, 700)
tin("#pr0", 65.80, "up"); hide("#pr1"); tin("#pr1", 67.03, "up")
hide("#pr2"); tin("#pr2", 67.86, "pop", 0.5)
count("#nrm", 390000, 67.86, 0.9, "RM")
J.append('tl.fromTo("#pr-u", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, 68.6);')
hide("#pr3"); tin("#pr3", 69.95, "pop")
J.append('tl.fromTo("#pr2", { scale: 1 }, { scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }, 69.95);')
tout("#g-price", 70.90)

# --- 18. klik link di bawah: phone with link
scene("s-link", 71.12, 74.30, '''<div class="bgblur"><img src="assets/img/render-1.jpg" alt="" /></div><div class="dim"></div>''')
block("g-link", 71.12, 74.30, f'''<div class="phone dark" id="lp"><div class="scr dk"><div class="lk" id="lk">{ICON["link"]}</div>
        <div class="lk-t">KLIK<br/>LINK<br/>DI BAWAH</div><div class="tapr" id="lk-r"></div></div>
      <div class="hand ph-hand" id="lk-hand">{HAND}</div></div>''', 420, 760)
J.append('tl.fromTo("#lp", { rotationY: 24, rotationX: 8, opacity: 0, y: 60 }, { rotationY: 8, rotationX: 3, opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, 71.14);')
J.append('tl.fromTo("#lk", { rotation: -20, scale: 0.6 }, { rotation: 0, scale: 1, duration: 0.6, ease: "back.out(2)" }, 71.3);')
J.append('tl.fromTo("#lk-hand", { opacity: 0, x: 80, y: 80 }, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }, 71.8);')
for at in (72.30, 72.80):
    J.append(f'tl.fromTo("#lk-hand", {{ scale: 1 }}, {{ scale: 0.86, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }}, {at});')
    J.append(f'tl.fromTo("#lk-r", {{ scale: 0.2, opacity: 0.9 }}, {{ scale: 1.6, opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }}, {at + 0.08});')
block("g-link2", 71.55, 74.30, '<div class="lbl yl lg" id="lk1">KLIK LINK DI BAWAH</div>', 1250, 120)
tin("#lk1", 71.55, "pop")
tout("#g-link", 74.10); tout("#g-link2", 74.10)

# --- 19. buat homestay + tambah pendapatan (render)
scene("s-fin", 74.32, 77.72, '''<div class="kb"><img id="r5" src="assets/img/render-5.jpg" alt="" /></div><div class="dim l"></div>''')
J.append('tl.fromTo("#r5", { scale: 1.12, x: 30 }, { scale: 1.02, x: 0, duration: 3.4, ease: "none" }, 74.32);')
coins2 = "".join(f'<div class="coin" id="cn{i}" style="bottom:{i * 20}px"></div>' for i in range(4))
block("g-fin", 75.85, 77.72, f'''<div class="lbl wh lg" id="fn1">BUAT HOMESTAY</div><div class="plus" id="fn-p">+</div>
      <div class="row"><div class="coins sm">{coins2}</div><div class="lbl yl lg" id="fn2">TAMBAH PENDAPATAN</div></div>''', 420, 380)
tin("#fn1", 75.85, "pop"); hide("#fn-p"); tin("#fn-p", 76.40, "pop"); hide("#fn2"); tin("#fn2", 76.68, "pop")
for i in range(4):
    J.append(f'tl.fromTo("#cn{i}", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "bounce.out" }}, {round(76.70 + i * 0.1, 3)});')
tout("#g-fin", 77.52)

# --- 20. closing CTA on the presenter
block("g-cta", 77.75, TOTAL, f'''<div class="lbl wh md" id="ct1">KLIK LINK DI BAWAH</div><div class="btnw"><div class="lbl yl xl" id="ct2">SEKARANG!</div>
      <div class="tapr" id="ct-r"></div><div class="hand ct-hand" id="ct-h">{HAND}</div></div>''', 400, 300)
tin("#ct1", 77.75, "pop"); hide("#ct2"); tin("#ct2", 77.95, "pop")
J.append('tl.fromTo("#ct-h", { opacity: 0, x: 60, y: 60 }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power3.out" }, 78.15);')
J.append('tl.fromTo("#ct-h", { scale: 1 }, { scale: 0.86, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }, 78.45);')
J.append('tl.fromTo("#ct2", { scale: 1 }, { scale: 0.95, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }, 78.45);')
J.append('tl.fromTo("#ct-r", { scale: 0.2, opacity: 0.9 }, { scale: 1.6, opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }, 78.53);')

# --- subtitles: one cue per transcript line in a fixed box that also covers the burned-in captions
BOXES.append(("subs", 1390, 140))
cues = []
for i, (s, text) in enumerate(SUBS):
    e = SUBS[i + 1][0] if i + 1 < len(SUBS) else TOTAL
    cues.append(f'      <div class="cue clip" id="cue{i}" data-start="{s}" data-duration="{round(e - s, 3)}"><span>{hl(text)}</span></div>')
    J.append(f'tl.fromTo("#cue{i}", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, {s});')
H.append(f'''    <div class="subbox clip" id="subs" data-start="0" data-duration="{TOTAL}">
{chr(10).join(cues)}
    </div>''')

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Poppins, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 70px; right: 70px; perspective: 1400px; }}
    .col {{ display: flex; flex-direction: column; align-items: center; gap: 14px; }}
    .row {{ display: flex; align-items: center; gap: 18px; }}
    .y {{ color: {YEL}; }} .mrt {{ color: {MAR}; }}
    .lbl {{ font-weight: 800; line-height: 1.02; white-space: nowrap; border-radius: 12px; letter-spacing: .005em;
      box-shadow: 0 16px 36px rgba(0,0,0,.35); text-transform: uppercase; }}
    .lbl.mr {{ background: {MAR}; color: {WHT}; }}
    .lbl.yl {{ background: {YEL}; color: {MAR_D}; }}
    .lbl.wh {{ background: {WHT}; color: {MAR_D}; }}
    .lbl.sm {{ font-size: 34px; letter-spacing: .1em; padding: 14px 26px 13px; font-weight: 700; }}
    .lbl.md {{ font-size: 48px; padding: 16px 32px 14px; }}
    .lbl.lg {{ font-size: 66px; padding: 18px 36px 16px; }}
    .lbl.xl {{ font-size: 96px; padding: 18px 42px 14px; }}
    .ic-house, .ic-m, .ic-homes, .ic-bed {{ width: 130px; height: 130px; border-radius: 26px; background: {MAR}; display: flex;
      align-items: center; justify-content: center; box-shadow: 0 14px 30px rgba(0,0,0,.35); }}
    .ic-homes svg, .ic-bed svg {{ stroke: {WHT}; }}
    .ic-car {{ width: 100px; height: 100px; border-radius: 50%; background: {YEL}; display: flex; align-items: center; justify-content: center; }}
    .incw {{ display: flex; align-items: flex-end; gap: 36px; height: 220px; }}
    .coins {{ position: relative; width: 140px; height: 160px; }}
    .coins.sm {{ width: 96px; height: 110px; transform: scale(.7); }}
    .coin {{ position: absolute; left: 0; width: 140px; height: 46px; border-radius: 50%; background: {YEL};
      border: 5px solid #C9A400; box-shadow: inset 0 -8px 0 #E5BC00; }}
    .bars {{ position: relative; display: flex; align-items: flex-end; gap: 16px; height: 210px; }}
    .bar {{ width: 46px; border-radius: 8px 8px 2px 2px; background: {WHT}; transform-origin: 50% 100%; box-shadow: 0 10px 24px rgba(0,0,0,.3); }}
    .bar:nth-child(4) {{ background: {YEL}; }}
    .arrow {{ position: absolute; left: -10px; top: -14px; }}
    .scn {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; }}
    .bgblur {{ position: absolute; inset: -60px; }} .bgblur img {{ width: 100%; height: 100%; object-fit: cover; filter: blur(26px); }}
    .kb {{ position: absolute; inset: 0; }} .kb img {{ width: 100%; height: 100%; object-fit: cover; }}
    .dim {{ position: absolute; inset: 0; background: rgba(40,8,16,.42); }} .dim.l {{ background: rgba(20,6,10,.18); }}
    .stage {{ position: absolute; left: 70px; right: 70px; top: 540px; height: 640px; perspective: 1600px; }}
    .rc3d {{ position: absolute; inset: 0; border-radius: 22px; overflow: hidden; border: 6px solid {WHT}; opacity: 0;
      box-shadow: 0 30px 70px rgba(0,0,0,.55); transform-style: preserve-3d; }}
    .rc3d img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .chips {{ display: flex; gap: 14px; justify-content: center; }}
    .chip {{ padding: 16px 26px 14px; border-radius: 999px; background: {WHT}; color: {MAR_D}; font-weight: 800; font-size: 40px;
      box-shadow: 0 12px 30px rgba(0,0,0,.35); white-space: nowrap; }}
    .chip:nth-child(2) {{ background: {YEL}; }}
    .pinw {{ position: relative; height: 96px; }}
    .ring {{ position: absolute; left: 50%; bottom: -6px; width: 80px; height: 26px; margin-left: -40px; border-radius: 50%;
      border: 5px solid {YEL}; opacity: 0; }}
    .route {{ position: relative; width: 900px; height: 230px; border-radius: 24px; background: {WHT}; color: {MAR_D};
      display: flex; align-items: center; justify-content: space-between; padding: 0 34px; box-shadow: 0 24px 60px rgba(0,0,0,.45); }}
    .rt-a, .rt-b {{ display: flex; flex-direction: column; align-items: center; gap: 6px; width: 170px; }}
    .rt-home {{ width: 90px; height: 90px; border-radius: 20px; background: {YEL}; display: flex; align-items: center; justify-content: center; }}
    .rt-l {{ font-weight: 800; font-size: 28px; line-height: 1.1; text-align: center; letter-spacing: .02em; }}
    .rt-line {{ position: relative; flex: 1; height: 90px; }}
    .rt-dash {{ position: absolute; left: 0; right: 0; top: 52px; height: 8px; transform-origin: 0 50%;
      background: repeating-linear-gradient(90deg, {MAR} 0 26px, transparent 26px 42px); border-radius: 4px; }}
    .rt-car {{ position: absolute; left: 0; top: 0; width: 76px; height: 64px; }}
    .rt-car svg {{ width: 76px; height: 64px; }}
    .big5 {{ font-weight: 900; font-size: 150px; line-height: 1; margin-top: 18px; text-shadow: 0 10px 34px rgba(0,0,0,.55); }}
    .stat {{ display: flex; align-items: center; gap: 26px; padding: 26px 44px 26px 28px; border-radius: 18px;
      background: rgba(74,12,28,.94); color: {WHT}; box-shadow: 0 20px 50px rgba(0,0,0,.45); border-left: 12px solid {YEL}; }}
    .si {{ width: 120px; height: 120px; border-radius: 16px; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; }}
    .sk {{ font-weight: 700; font-size: 32px; letter-spacing: .1em; }}
    .sv {{ font-weight: 900; font-size: 110px; line-height: 1.0; white-space: nowrap; }}
    .sv small {{ font-size: 46px; }}
    .cst {{ position: absolute; left: 70px; right: 70px; top: 580px; height: 620px; perspective: 1600px; }}
    .rc3d.sm {{ left: 0; right: 360px; top: 30px; bottom: 60px; opacity: 1; }}
    .planc {{ position: absolute; right: 0; top: 120px; width: 440px; height: 330px; border-radius: 20px; background: #FBF7EE;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 26px 60px rgba(0,0,0,.5); border: 6px solid {YEL}; }}
    .phone {{ position: relative; width: 400px; height: 740px; border-radius: 58px; background: #111; padding: 18px;
      box-shadow: 0 40px 80px rgba(0,0,0,.6), inset 0 0 0 4px #333; transform-style: preserve-3d; }}
    .scr {{ width: 100%; height: 100%; border-radius: 42px; background: #FFF8F4; color: {MAR_D}; overflow: hidden;
      display: flex; flex-direction: column; align-items: center; padding: 56px 28px; gap: 26px; position: relative; }}
    .scr.dk {{ background: {MAR}; color: {WHT}; justify-content: center; }}
    .ph-h {{ font-weight: 800; font-size: 34px; }}
    .cal {{ display: grid; grid-template-columns: repeat(7, 34px); gap: 8px; }}
    .cal i {{ display: block; width: 34px; height: 34px; border-radius: 8px; background: #EADBDF; }}
    .ph-btn {{ padding: 14px 40px; border-radius: 999px; background: {MAR}; color: {WHT}; font-weight: 800; font-size: 30px; }}
    .ok {{ display: flex; align-items: center; gap: 16px; font-weight: 800; font-size: 30px; line-height: 1.1; opacity: 0;
      background: {WHT}; border-radius: 18px; padding: 16px 20px; box-shadow: 0 10px 26px rgba(0,0,0,.18); }}
    .okc {{ width: 66px; height: 66px; border-radius: 50%; background: #1E9E5A; display: flex; align-items: center; justify-content: center; }}
    .lk {{ width: 180px; height: 180px; border-radius: 50%; background: {YEL}; display: flex; align-items: center; justify-content: center; }}
    .lk-t {{ font-weight: 900; font-size: 56px; line-height: 1.05; text-align: center; }}
    .hand {{ position: absolute; filter: drop-shadow(0 8px 14px rgba(0,0,0,.45)); opacity: 0; }}
    .ph-hand {{ right: -30px; top: 470px; }}
    .tapr {{ position: absolute; left: 50%; top: 50%; width: 130px; height: 130px; margin: -65px 0 0 -65px; border-radius: 50%;
      border: 5px solid {YEL}; opacity: 0; }}
    .shield {{ filter: drop-shadow(0 16px 30px rgba(0,0,0,.45)); }}
    .pricebg {{ position: absolute; inset: 0; background: linear-gradient(180deg, {MAR_D} 0%, {MAR} 50%, {MAR_D} 100%); }}
    .pk {{ font-weight: 800; font-size: 54px; letter-spacing: .06em; }}
    .pk.big {{ font-size: 92px; }}
    .rm {{ font-weight: 900; font-size: 170px; line-height: 1; color: {YEL}; letter-spacing: -.01em; text-shadow: 0 12px 40px rgba(0,0,0,.4); }}
    .uline {{ width: 760px; height: 12px; border-radius: 6px; background: {YEL}; transform-origin: 0 50%; }}
    .plus {{ font-weight: 900; font-size: 90px; line-height: .8; color: {YEL}; text-shadow: 0 8px 24px rgba(0,0,0,.5); }}
    .btnw {{ position: relative; }}
    .ct-hand {{ right: -40px; top: 70px; }}
    .subbox {{ position: absolute; left: 70px; right: 70px; top: 1390px; height: 140px; border-radius: 18px;
      background: #4A0C1C; border-top: 5px solid {YEL}; box-shadow: 0 22px 40px rgba(0,0,0,.45); }}
    .cue {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; text-align: center;
      padding: 8px 30px; font-weight: 600; font-size: 40px; line-height: 1.22; color: {WHT}; }}
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
print("total", TOTAL, "subs", len(SUBS), "boxes ok")
