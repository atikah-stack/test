"""Builds index.html and the text scenes for the Scandinavian O-Shape house tour.

Edit SHOTS / TEXT below and run `python3 build.py`. Every shot is an untouched
original clip from assets/src (iPhone 4K, 15 Oct 2026).
"""
import json

YELLOW = "#F5C518"
GRADE = json.dumps({"preset": "warm-daylight", "intensity": 0.4})

# (duration, file, media start, rate, zoom from, zoom to, note)
DRONE_TOP = "copy_7339E792-E530-4778-BF5A-9BBB19C8734F.mov"    # drone, top-down rise over the O-shape (1080p, 50 fps)
DRONE_FRONT = "copy_F839D845-7E8C-468E-ADD9-0E4E4DE10A2F.mov"  # drone, 45-degree front (1080p, 37.5 fps)

# (duration, file, media start, rate, zoom from, zoom to, note)
# Drone slow-motion rates keep at least 25 source frames a second, so nothing judders.
SHOTS = [
    # 1 Hook 0-5
    (5.0, DRONE_FRONT, 0.0, 0.677, 1.00, 1.06, "drone front, 45 degrees, slow push-in"),
    # 2 O-shape 5-11
    (3.3, DRONE_TOP, 0.0, 0.75, 1.00, 1.03, "drone top-down: the pool inside the O"),
    (2.7, "IMG_9158.MOV", 0.0, 1, 1.00, 1.03, "tilt down from the roof into the courtyard"),
    # 3 Pool 11-18
    (3.2, "IMG_9157.MOV", 0.0, 1, 1.00, 1.04, "pool with the house around it"),
    (2.2, "IMG_9129.MOV", 0.0, 1, 1.00, 1.04, "living room, pool behind the glass wall"),
    (1.6, "IMG_9158.MOV", 3.6, 1, 1.03, 1.06, "pool, closer"),
    # 4 Architecture 18-25
    (1.4, "IMG_9048.MOV", 0.0, 1, 1.00, 1.04, "main door and arched window"),
    (1.6, "IMG_9180.MOV", 0.5, 1, 1.00, 1.04, "round gable window"),
    (2.2, "IMG_9044.MOV", 0.0, 1, 1.00, 1.04, "entrance porch, low angle"),
    (1.8, "IMG_9178.MOV", 4.0, 1, 1.00, 1.04, "side entrance"),
    # 5 Interior 25-34
    (2.0, "IMG_9396.MOV", 3.0, 1, 1.00, 1.04, "living hall pan (60 fps source)"),
    (1.4, "IMG_9174.MOV", 2.0, 1, 1.00, 1.04, "chandelier"),
    (2.0, "IMG_9093.MOV", 0.0, 1, 1.00, 1.04, "kitchen"),
    (1.6, "IMG_9121.MOV", 0.0, 1, 1.00, 1.04, "bedroom"),
    (2.0, "IMG_9147.MOV", 0.5, 1, 1.00, 1.04, "bathroom"),
    # 6 Price 34-39
    (5.0, "IMG_9157.MOV", 5.0, 1, 1.00, 1.06, "pool wide, slow push"),
    # 7 Ending 39-42.5
    (3.5, DRONE_TOP, 2.48, 0.5, 1.00, 1.03, "drone top-down, the whole O with the pool"),
]
ROTATED = set()          # no sideways clip in the cut now (IMG_9045 replaced by the drone front)
DISSOLVE = {1, 15, 16}   # 0-based shot indices that fade in: into the drone top-down, price, ending

starts, t = [], 0.0
for s in SHOTS:
    starts.append(round(t, 2))
    t += s[0]
TOTAL = round(t, 2)

# Text scenes: id -> (start, duration, top px, [(text, colour, size px)], extra)
TEXT = {
    "hook": (0.15, 4.75, 560, [("BANGLO SCANDINAVIAN<br>BERBENTUK O", "w", 62), ("SIAP ADA KOLAM<br>DI TENGAH!", "y", 80)], None),
    "oshape": (5.3, 5.4, 620, [("REKA BENTUK O\u2011SHAPE", "w", 70)], None),
    "pool": (11.3, 6.4, 620, [("KOLAM RENANG", "w", 76), ("DI TENGAH RUMAH", "y", 76)], None),
    "konsep": (18.2, 3.1, 620, [("KONSEP SCANDINAVIAN", "w", 70)], None),
    "lokasi": (21.4, 3.5, 620, [("LOKASI:", "w", 48), ("MACHANG, KELANTAN", "y", 70)], None),
    "kps": (25.2, 4.3, 620, [("KELUASAN", "w", 52), ("2,031 KPS", "y", 110)], None),
    "bilik": (29.6, 4.3, 620, [("4 BILIK TIDUR | 3 BILIK AIR", "w", 58)], None),
    "harga": (34.3, 4.6, 600, [("HARGA ASAS BERMULA", "w", 66), ("BAWAH RM400K", "y", 104)],
              "*Harga asas sahaja. Kolam & spesifikasi dalam video tertakluk pakej."),
    "ending": (39.3, TOTAL - 39.3, 380, [("MAHLIGAI IDAMAN", "w", 78), ("BINA RUMAH ATAS TANAH SENDIRI", "y", 50)], "logo"),
}

SFX = [  # (id, file, start, duration, volume)
    ("x-open", "whoosh-cinematic.mp3", 0.0, 2.5, 0.18),
    ("x-court", "whoosh-short.mp3", 8.05, 0.6, 0.18),
    ("x-pool", "impact-bass-1.mp3", 11.0, 2.0, 0.16),
    ("x-price", "riser.mp3", 31.0, 3.2, 0.12),
    ("x-price-hit", "impact-bass-1.mp3", 34.3, 2.0, 0.18),
    ("x-end", "chime.mp3", 39.4, 2.0, 0.18),
]

# ---------------------------------------------------------------- root
rows = []
for i, ((dur, f, ms, rate, z0, z1, note), st) in enumerate(zip(SHOTS, starts)):
    vid = f"s{i + 1:02d}"
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1 else ""
    cls = "rot clip" if f in ROTATED else "shot clip"
    tag = (f'<video id="{vid}" class="{cls}" src="assets/src/{f}" muted playsinline data-start="{st}" '
           f'data-duration="{dur}" data-media-start="{ms}"{rate_attr} data-track-index="{i % 2}" '
           f'data-color-grading=\'{GRADE}\' style="z-index:{i + 1}"></video>')
    if f in ROTATED:
        tag = f'<div id="{vid}-turn" class="turn" style="z-index:{i + 1}">{tag}</div>'
    rows.append(f"      <!-- {note} -->\n      {tag}")

for sid, f, s, d, v in SFX:
    rows.append(f'      <audio id="{sid}" class="clip" src="assets/sfx/{f}" data-start="{s}" data-duration="{d}" '
                f'data-volume="{v}" data-track-index="{12 + (sid in ("x-court", "x-price-hit"))}"></audio>')

rows.append(f'      <div id="fade" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-layout-ignore></div>')
for n, (cid, (s, d, *_)) in enumerate(TEXT.items()):
    rows.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                f'data-start="{s}" data-duration="{round(d, 2)}" data-track-index="{5 + n % 2}" data-track-kind="graphics" '
                f'data-width="1080" data-height="1920" style="z-index:{60 + n}"></div>')

js = json.dumps([[f"s{i + 1:02d}", st, s[0], s[4], s[5], i in DISSOLVE, s[1] in ROTATED]
                 for i, (s, st) in enumerate(zip(SHOTS, starts))])
html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0b; }}
      #root {{ width: 100%; height: 100%; background: #0b0b0b; font-family: "Montserrat", sans-serif; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      /* Sideways source: a portrait box turned a quarter-turn left fills the frame upright. */
      .turn {{ position: absolute; left: -420px; top: -747px; width: 1920px; height: 3414px; transform: rotate(-90deg); }}
      .rot {{ position: absolute; left: 0; top: 0; width: 1920px; height: 3414px; object-fit: cover; }}
      #fade {{ position: absolute; inset: 0; z-index: 90; background: #0b0b0b; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="25" data-width="1080" data-height="1920">
{chr(10).join(rows)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const shots = {js};
      shots.forEach(([id, s, d, z0, z1, dissolve, rotated]) => {{
        if (rotated) {{
          // local y is screen x after the quarter turn: drift slowly across the facade
          tl.fromTo("#" + id, {{ y: 160, scale: z0 }}, {{ y: -160, scale: z1, duration: d, ease: "none" }}, s);
        }} else {{
          tl.fromTo("#" + id, {{ scale: z0 }}, {{ scale: z1, duration: d, ease: "none" }}, s);
        }}
        if (dissolve) tl.fromTo("#" + id, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "sine.inOut" }}, s);
      }});
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8, ease: "sine.in" }}, {round(TOTAL - 0.8, 2)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)

# ---------------------------------------------------------------- text scenes
SHADOW = "0 6px 24px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.5)"
for cid, (s, d, top, lines, extra) in TEXT.items():
    d = round(d, 2)
    line_html, line_js = [], []
    for k, (txt, col, size) in enumerate(lines):
        lid = f"{cid}-{k + 1}"
        colour = "#FFFFFF" if col == "w" else YELLOW
        line_html.append(f'      <div id="{lid}" class="ln" style="color:{colour};font-size:{size}px">{txt}</div>')
        line_js.append(f'    tl.fromTo("#{lid}", {{ opacity:0, y:24, scale:0.96 }}, '
                       f'{{ opacity:1, y:0, scale:1, duration:0.7, ease:"power2.out" }}, {0.18 * k});')
    extra_css = extra_html = ""
    if extra == "logo":
        extra_css = """
    #logo-card { position:absolute; left:390px; top:1250px; width:300px; padding:22px 24px; border-radius:24px; background:#FFFFFF;
      box-shadow:0 14px 40px rgba(0,0,0,.3); }
    #logo-img { display:block; width:252px; height:auto; }"""
        extra_html = (f'\n    <div id="logo-card" class="clip" data-start="0" data-duration="{d}" data-track-index="1">'
                      '<img id="logo-img" src="assets/brand/logo-mi.png" alt="Mahligai Idaman" /></div>')
        line_js.append('    tl.fromTo("#logo-card", { opacity:0, y:16 }, { opacity:1, y:0, duration:0.7, ease:"power2.out" }, 0.5);')
    elif extra:
        line_html.append(f'      <div id="{cid}-note" class="note">{extra}</div>')
        line_js.append(f'    tl.fromTo("#{cid}-note", {{ opacity:0 }}, {{ opacity:1, duration:0.5 }}, 0.6);')
    if cid != "ending":
        line_js.append(f'    tl.to("#{cid}-blk", {{ opacity:0, duration:0.35, ease:"sine.in" }}, {round(d - 0.4, 2)});')
    html = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; font-family:"Montserrat",sans-serif; }}
    /* the soft shade behind the words lets white text read on white walls and bright sky */
    .blk {{ position:absolute; left:0; right:0; padding:110px 60px; margin-top:-110px; display:flex; flex-direction:column;
      align-items:center; text-align:center; gap:6px;
      background:radial-gradient(ellipse 60% 50% at 50% 50%, rgba(0,0,0,.44) 0%, rgba(0,0,0,.22) 45%, rgba(0,0,0,0) 78%); }}
    .ln {{ white-space:nowrap; font-weight:800; text-transform:uppercase; line-height:1.08; letter-spacing:0.01em; text-shadow:{SHADOW}; }}
    .note {{ margin-top:14px; color:#FFFFFF; font-weight:500; font-size:28px; letter-spacing:0.01em; opacity:.92;
      text-shadow:0 2px 8px rgba(0,0,0,.7); }}
    #{cid}-blk {{ top:{top}px; }}{extra_css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-blk" class="blk clip" data-start="0" data-duration="{d}" data-track-index="0">
{chr(10).join(line_html)}
    </div>{extra_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(line_js)}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    open(f"compositions/{cid}.html", "w").write(html)
print("total", TOTAL, "shots", len(SHOTS))
