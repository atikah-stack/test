"""Builds index.html and the graphics scenes for the Zunaida testimonial.

Run `python3 build.py` after editing the lists below. See STORYLINE.md.
All dialogue comes from the original interview IMG_7123.mov, cut losslessly
into two sections (stream copy, no re-encode):
  assets/interview/IMG_7123_a_0033.96.mov  starts at source 33.963333 s
  assets/interview/IMG_7123_b_0601.35.mov  starts at source 361.353333 s
"""
import json

YELLOW = "#F5C518"
SEG = {
    "A": ("assets/interview/IMG_7123_a_0033.96.mov", 33.963333),
    "B": ("assets/interview/IMG_7123_b_0601.35.mov", 361.353333),
}
# Face sits about 46% down the frame; zooming from there keeps it in place.
FACE_ORIGIN = "50% 46%"

# Dialogue: (id, segment, source in, source out). Placed back to back.
DIALOGUE = [
    ("d1", "B", 377.80, 379.80),  # Kontrak pun dua tahun lah.
    ("d2", "B", 380.20, 383.00),  # Tapi Alhamdulillah, rumah siap satu tahun setengah.
    ("d3", "B", 383.80, 389.00),  # So okey, cepat. Consider cepat lah. Alhamdulillah.
    ("d4", "B", 363.40, 372.00),  # Sebab dia kata keluasan dia 3,774 kaki persegi, macam bina dua buah rumah dia kata.
    ("d5", "B", 372.00, 377.60),  # So kalau sebuah rumah satu tahun, ... dua tahun.
    ("d6", "A", 36.00, 44.40),    # Sangat gembira ... dapat cepat kunci kan.
    ("d7", "A", 44.80, 49.30),    # So okeylah, balik boleh duduk rumah sendiri.
]

# Shots: (id, out start, duration, kind, source, media start, rate, zoom from, zoom to)
# kind "int" = interview (muted picture; sound comes from DIALOGUE), "broll" = muted B-roll.
SHOTS = [
    ("v01", 0.0, 2.0, "int", "B", 377.80, 1, 1.35, 1.42),
    ("v02", 2.0, 2.8, "int", "B", 380.20, 1, 1.50, 1.72),   # punch-in on "satu tahun setengah"
    ("v03", 4.8, 3.0, "broll", "assets/src/copy_F371EC91-96A0-45F7-9EF7-DBEC5C39D4B7.mov", 0.0, 1, 1.0, 1.06),
    ("v04", 7.8, 2.2, "int", "B", 387.00, 1, 1.40, 1.46),
    ("v05", 10.0, 1.6, "int", "B", 363.40, 1, 1.35, 1.40),
    ("v06", 11.6, 3.4, "broll", "assets/src/copy_94BEB817-F987-4FD8-AC46-D89488E47548.mov", 0.0, 0.99, 1.0, 1.06),
    ("v07", 15.0, 3.6, "broll", "assets/src/IMG_3753.MOV", 0.0, 1, 1.0, 1.05),
    ("v08", 18.6, 3.0, "broll", "assets/src/IMG_3827.MOV", 0.0, 1, 1.0, 1.05),
    ("v09", 21.6, 2.6, "int", "B", 375.00, 1, 1.45, 1.50),
    ("v10", 24.2, 4.0, "int", "A", 36.00, 1, 1.35, 1.45),
    ("v11", 28.2, 2.6, "broll", "assets/src/IMG_7194.MOV", 0.0, 1, 1.0, 1.04),
    ("v12", 30.8, 1.8, "int", "A", 42.60, 1, 1.50, 1.55),
    ("v13", 32.6, 2.6, "broll", "assets/src/IMG_7098.MOV", 1.5, 1, 1.0, 1.04),
    ("v14", 35.2, 1.9, "broll", "assets/src/IMG_3615.MOV", 0.0, 1, 1.0, 1.05),
    ("v15", 37.1, 2.6, "broll", "assets/src/IMG_3749.MOV", 0.0, 0.85, 1.0, 1.04),
]
DISSOLVE_IN = {"v03", "v04", "v06", "v15"}  # 0.2 s dissolves around drone shots and the ending

TOTAL = round(SHOTS[-1][1] + SHOTS[-1][2], 2)

# Graphics scenes: (id, start, duration)
G = {
    "hook": (0.0, 4.7),
    "timeline": (5.0, 2.75),
    "kps": (13.9, 2.6),
    "tempoh": (18.8, 5.3),
    "awal": (28.6, 3.6),
    "closing": (37.2, TOTAL - 37.2),
    "subs": (0.0, 37.1),
}

SFX = [  # (id, file, start, duration, volume)
    ("x-hook", "impact-bass-1.mp3", 2.8, 2.0, 0.22),
    ("x-drone", "whoosh-short.mp3", 4.75, 0.6, 0.15),
    ("x-tl", "click-soft.mp3", 5.6, 0.4, 0.25),
    ("x-kps", "impact-bass-1.mp3", 13.9, 2.0, 0.14),
    ("x-t1", "click-soft.mp3", 18.8, 0.4, 0.22),
    ("x-t2", "click-soft.mp3", 22.2, 0.4, 0.22),
    ("x-end", "chime.mp3", 37.3, 2.0, 0.2),
]

# Subtitles: (start, end, text with **keyword** marks)
SUBS = [
    (0.0, 2.0, "Kontrak pun **dua tahun** lah."),
    (2.0, 4.8, "Tapi Alhamdulillah, rumah siap **satu tahun setengah**."),
    (4.8, 7.8, "So okey, cepat. Consider cepat lah."),
    (7.8, 10.0, "Alhamdulillah."),
    (10.0, 16.6, "Sebab dia kata keluasan dia **3,774 kaki persegi**,"),
    (16.6, 18.6, "macam bina **dua buah rumah** dia kata."),
    (18.6, 21.9, "So kalau sebuah rumah satu tahun,"),
    (21.9, 24.2, "sebab yang ni macam dua buah rumah, **dua tahun**."),
    (24.2, 26.6, "**Sangat gembira** sebab dah lama tunggu,"),
    (26.6, 28.2, "setahun setengah tunggu."),
    (28.2, 32.6, "Sebenarnya dua tahun kontrak, tapi **dapat cepat kunci** kan."),
    (32.6, 37.1, "So okeylah, balik boleh **duduk rumah sendiri**."),
]

# ---------------------------------------------------------------- root
rows = []
for i, (vid, start, dur, kind, src, ms, rate, z0, z1) in enumerate(SHOTS):
    if kind == "int":
        path, off = SEG[src]
        ms = round(ms - off, 3)
        style = f"z-index:{i + 1};transform-origin:{FACE_ORIGIN}"
    else:
        path = src
        style = f"z-index:{i + 1}"
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1 else ""
    rows.append(
        f'      <video id="{vid}" class="shot clip" src="{path}" muted playsinline data-start="{start}" '
        f'data-duration="{dur}" data-media-start="{ms}"{rate_attr} data-track-index="{i % 2}" style="{style}"></video>'
    )

t = 0.0
for did, seg, a, b in DIALOGUE:
    path, off = SEG[seg]
    d = round(b - a, 2)
    rows.append(
        f'      <audio id="{did}" class="clip" src="{path}" data-start="{round(t, 2)}" data-duration="{d}" '
        f'data-media-start="{round(a - off, 3)}" data-volume="1" data-track-index="10"></audio>'
    )
    t += d
assert abs(t - SHOTS[-1][1]) < 0.01, f"dialogue ends at {t}, ending shot starts at {SHOTS[-1][1]}"
rows.append(
    f'      <audio id="a-amb" class="clip" src="assets/src/IMG_3749.MOV" data-start="37.1" data-duration="{round(TOTAL - 37.1, 2)}" '
    f'data-media-start="0" data-volume="0.35" data-track-index="11"></audio>'
)
for sid, f, s, d, v in SFX:
    rows.append(
        f'      <audio id="{sid}" class="clip" src="assets/sfx/{f}" data-start="{s}" data-duration="{d}" '
        f'data-volume="{v}" data-track-index="{12 + (sid == "x-drone")}"></audio>'
    )
for n, (gid, (s, d)) in enumerate(G.items()):
    kind = "captions" if gid == "subs" else "graphics"
    z = 70 if gid == "subs" else 60 + n
    rows.append(
        f'      <div id="{gid}" data-composition-id="{gid}" data-composition-src="compositions/{gid}.html" '
        f'data-start="{round(s, 2)}" data-duration="{round(d, 2)}" data-track-index="{5 + n}" data-track-kind="{kind}" '
        f'data-width="1080" data-height="1920" style="z-index:{z}"></div>'
    )

js = json.dumps([[s[0], s[1], s[2], s[7], s[8], s[0] in DISSOLVE_IN] for s in SHOTS])
html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0b; }}
      #root {{ width: 100%; height: 100%; background: #0b0b0b; font-family: "Poppins", sans-serif; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="25" data-width="1080" data-height="1920">
{chr(10).join(rows)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const shots = {js};
      shots.forEach(([id, s, d, z0, z1, dissolve]) => {{
        tl.fromTo("#" + id, {{ scale: z0 }}, {{ scale: z1, duration: d, ease: "none" }}, s);
        if (dissolve) tl.fromTo("#" + id, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "sine.inOut" }}, s);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)

# ---------------------------------------------------------------- scenes
SHADOW = "0 6px 22px rgba(0,0,0,.55), 0 2px 5px rgba(0,0,0,.5)"
BASE = f"""
    #root {{ position:absolute; inset:0; font-family:"Poppins",sans-serif; }}
    .blk {{ position:absolute; left:60px; right:60px; display:flex; flex-direction:column; align-items:center; text-align:center; }}
    .w, .y {{ font-weight:900; text-transform:uppercase; line-height:1.02; letter-spacing:0.005em; text-shadow:{SHADOW}; }}
    .w {{ color:#FFFFFF; }}
    .y {{ color:{YELLOW}; }}
"""


def scene(cid, dur, css, body, js):
    return f"""<template>
  <style>{BASE}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def rise(sel, at, dur=0.6):
    return (f'    tl.fromTo("{sel}", {{ opacity:0, y:26, scale:0.95 }}, '
            f'{{ opacity:1, y:0, scale:1, duration:{dur}, ease:"power2.out" }}, {at});')


def out(sel, at):
    return f'    tl.to("{sel}", {{ opacity:0, duration:0.35, ease:"sine.in" }}, {round(at, 2)});'


scenes = {}
d = G["hook"][1]
scenes["hook"] = scene("hook", d, """
    #hk { top:380px; }
    #hk-1 { font-size:86px; }
    #hk-2 { font-size:104px; margin-top:6px; }""",
    f"""    <div id="hk" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="hk-1" class="w">KONTRAK 2 TAHUN</div>
      <div id="hk-2" class="y">SIAP 18 BULAN!</div>
    </div>""",
    "\n".join([rise("#hk-1", 0.1, 0.5), rise("#hk-2", 2.8, 0.45), out("#hk", d - 0.4)]))

d = G["timeline"][1]
scenes["timeline"] = scene("timeline", d, f"""
    #tlb {{ top:470px; }}
    #tl-row {{ display:flex; align-items:center; gap:28px; }}
    #tl-24, #tl-18 {{ font-size:84px; }}
    #tl-arrow {{ font-size:72px; }}
    #tl-bar {{ position:relative; width:820px; height:16px; margin-top:28px; border-radius:8px; background:rgba(255,255,255,.35); }}
    #tl-fill {{ position:absolute; left:0; top:0; bottom:0; width:615px; border-radius:8px; background:{YELLOW}; transform-origin:0 50%; }}
    #tl-mark {{ position:absolute; left:613px; top:-14px; width:4px; height:44px; background:#FFFFFF; border-radius:2px; }}""",
    f"""    <div id="tlb" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="tl-row"><div id="tl-24" class="w">24 BULAN</div><div id="tl-arrow" class="w">→</div><div id="tl-18" class="y">18 BULAN</div></div>
      <div id="tl-bar"><div id="tl-fill"></div><div id="tl-mark"></div></div>
    </div>""",
    "\n".join([rise("#tl-24", 0, 0.45), rise("#tl-arrow", 0.35, 0.4), rise("#tl-18", 0.6, 0.45),
               rise("#tl-bar", 0.2, 0.4),
               '    tl.fromTo("#tl-fill", { scaleX:0 }, { scaleX:1, duration:1.1, ease:"power2.inOut" }, 0.5);',
               out("#tlb", d - 0.4)]))

d = G["kps"][1]
scenes["kps"] = scene("kps", d, """
    #kp { top:330px; }
    #kp-n { font-size:150px; }
    #kp-u { font-size:58px; margin-top:2px; letter-spacing:0.08em; }""",
    f"""    <div id="kp" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="kp-n" class="y">3,774</div>
      <div id="kp-u" class="w">KAKI PERSEGI</div>
    </div>""",
    "\n".join([rise("#kp-n", 0, 0.55), rise("#kp-u", 0.2, 0.5), out("#kp", d - 0.4)]))

d = G["tempoh"][1]
scenes["tempoh"] = scene("tempoh", d, """
    #tp { top:400px; }
    #tp-1, #tp-2 { font-size:54px; }
    #tp-2 { margin-top:14px; }""",
    f"""    <div id="tp" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="tp-1" class="w">TEMPOH KONTRAK: 24 BULAN</div>
      <div id="tp-2" class="y">TEMPOH SIAP: 18 BULAN</div>
    </div>""",
    "\n".join([rise("#tp-1", 0, 0.5), rise("#tp-2", 3.4, 0.5), out("#tp", d - 0.4)]))

d = G["awal"][1]
scenes["awal"] = scene("awal", d, """
    #aw { top:400px; }
    #aw-1 { font-size:70px; }
    #aw-2 { font-size:92px; margin-top:4px; }""",
    f"""    <div id="aw" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="aw-1" class="w">SIAP 6 BULAN</div>
      <div id="aw-2" class="y">LEBIH AWAL</div>
    </div>""",
    "\n".join(['    tl.fromTo("#aw", { opacity:0 }, { opacity:1, duration:0.5, ease:"sine.out" }, 0);',
               out("#aw", d - 0.4)]))

d = round(G["closing"][1], 2)
scenes["closing"] = scene("closing", d, """
    #cl { top:430px; }
    #cl-1 { font-size:96px; }
    #cl-2 { font-size:96px; margin-top:4px; }
    #cl-logo { position:absolute; left:380px; top:1110px; width:320px; padding:24px 26px; border-radius:24px; background:#FFFFFF;
      box-shadow:0 14px 40px rgba(0,0,0,.3); }
    #cl-img { display:block; width:268px; height:auto; }""",
    f"""    <div id="cl" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="cl-1" class="w">IMPIAN</div>
      <div id="cl-2" class="y">JADI KENYATAAN</div>
    </div>
    <div id="cl-logo" class="clip" data-start="0" data-duration="{d}" data-track-index="1">
      <img id="cl-img" src="assets/brand/logo-mi.png" alt="Mahligai Idaman" />
    </div>""",
    "\n".join([rise("#cl-1", 0, 0.5), rise("#cl-2", 0.18, 0.5),
               '    tl.fromTo("#cl-logo", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.6, ease:"power2.out" }, 0.45);']))


def mark(text):
    parts = text.split("**")
    return "".join(f'<span class="k">{p}</span>' if i % 2 else p for i, p in enumerate(parts))


sub_rows, sub_js = [], []
for i, (s, e, text) in enumerate(SUBS, 1):
    sid = f"sub{i:02d}"
    sub_rows.append(f'    <div id="{sid}" class="cap clip" data-start="{s}" data-duration="{round(e - s, 2)}" '
                    f'data-track-index="0"><div class="line">{mark(text)}</div></div>')
    sub_js.append(f'    tl.fromTo("#{sid} .line", {{ opacity:0, y:8 }}, {{ opacity:1, y:0, duration:0.15, ease:"power1.out" }}, {s});')
scenes["subs"] = scene("subs", G["subs"][1], f"""
    .cap {{ position:absolute; left:90px; right:90px; top:1150px; height:180px; display:flex; align-items:flex-end; justify-content:center; }}
    .line {{ max-width:900px; text-align:center; color:#FFFFFF; font-weight:700; font-size:48px; line-height:1.22;
      text-shadow:0 3px 12px rgba(0,0,0,.7), 0 1px 3px rgba(0,0,0,.7); }}
    .k {{ color:{YELLOW}; }}""",
    "\n".join(sub_rows), "\n".join(sub_js))

for name, body in scenes.items():
    open(f"compositions/{name}.html", "w").write(body)
print("total", TOTAL)
