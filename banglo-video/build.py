#!/usr/bin/env python3
"""Generate the Banglo Split Level HyperFrames project files (1080x1920)."""
import json, sys, html, os

PROJ = sys.argv[1]
W, H = 1080, 1920
OUTRO_START = 62.56
TOTAL = 71.0

GOLD = "#FFC83D"
RED = "#E3262C"

# ---------------------------------------------------------------- transcript
words = json.load(open(os.path.join(PROJ, "assets/transcript.json")))
fix = {17: "design", 81: "design", 123: "design", 139: "design",
       25: "Mahligai", 75: "Mahligai", 112: "Mahligai", 153: "Mahligai",
       26: "Idaman", 76: "Idaman,", 113: "Idaman", 154: "Idaman.",
       29: "Kemaman,", 30: "Terengganu", 46: "aras", 47: "lantai", 52: "atur",
       105: "Melayu", 136: "pening", 149: "Kelantan", 151: "Terengganu?",
       7: "level,", 19: "mana!"}
for i, t in fix.items():
    words[i]["text"] = t

def glen(ws): return len(" ".join(w["text"] for w in ws))
# subtitle groups, hand-picked at phrase boundaries (index of each group's first word)
STARTS = [0, 8, 13, 20, 27, 32, 39, 41, 46, 50, 54, 60, 64, 70, 74, 77, 84, 89, 95, 100, 104,
          110, 112, 118, 123, 127, 133, 137, 143, 148, 152]
groups = [words[a:b] for a, b in zip(STARTS, STARTS[1:] + [len(words)])]

# ---------------------------------------------------------------- shots
# (start, end, kind, src, media_start, motion)
shots = [
    (0.00, 5.19, "p", "c2.mp4", 0.0, ("in", 1.18, 1.0)),
    (5.19, 8.30, "p", "c3.mp4", 0.0, ("in", 1.25, 1.08)),
    (8.30, 12.75, "p", "n1.mp4", 0.5, ("in", 1.12, 1.0)),
    (12.75, 16.55, "p", "n3.mp4", 4.0, ("in", 1.12, 1.0)),
    (16.55, 20.80, "p", "c6.mp4", 0.0, ("in", 1.12, 1.0)),
    (20.80, 25.70, "p", "c7.mp4", 0.0, ("in", 1.15, 1.03)),
    (25.70, 30.98, "p", "c8.mp4", 0.0, ("in", 1.12, 1.0)),
    (30.98, 35.85, "collage", None, 0, None),
    (35.85, 38.05, "l", "style-tropical.jpg", 0, ("pan", -1500, -900)),
    (38.05, 40.52, "l", "style-muji.jpg", 0, ("pan", -650, -1250)),
    (40.52, 42.95, "l", "style-english.jpg", 0, ("pan", -1500, -800)),
    (42.95, 44.85, "l", "style-nordic.jpg", 0, ("pan", -650, -1350)),
    (44.85, 47.75, "l", "style-melayu.jpg", 0, ("pan", -1550, -800)),
    (47.75, 49.00, "p", "c8.mp4", 6.0, ("in", 1.12, 1.0)),
    (49.00, 52.60, "plan", "plan-ground.png", 0, (515, 1148, 760)),
    (52.60, 55.65, "plan", "plan-upper.png", 0, (515, 1180, 800)),
    (55.65, 58.89, "p", "n4.mp4", 2.0, ("in", 1.12, 1.0)),
    (58.89, OUTRO_START, "p", "c2.mp4", 2.5, ("in", 1.25, 1.05)),
]

shot_html, shot_js = [], []
for n, (s, e, kind, src, ms, mot) in enumerate(shots, 1):
    d = round(e - s, 3)
    if kind == "collage":
        styles = ["tropical", "muji", "english", "nordic", "melayu"]
        pos = ["50% 55%", "45% 60%", "50% 55%", "45% 60%", "55% 55%"]
        strips = "\n".join(
            f'          <div id="cs{n}-{k}" class="strip" style="top:{k * 386}px">'
            f'<img id="ci{n}-{k}" class="strip-img" src="assets/style-{st}.jpg" style="object-position:{pos[k]}" alt="" /></div>'
            for k, st in enumerate(styles))
        shot_html.append(f'      <div id="sw{n}" class="shot" style="left:0;top:0;width:{W}px;height:{H}px;z-index:{n}">\n'
                         f'        <div id="v{n}" class="clip collage" data-start="{s}" data-duration="{d}" data-track-index="0">\n{strips}\n        </div>\n      </div>')
        for k in range(5):
            t0 = round(s + 0.05 + 0.3 * k, 3)
            shot_js.append(f'tl.fromTo("#cs{n}-{k}", {{ x: {-W if k % 2 == 0 else W} }}, {{ x: 0, duration: 0.5, ease: "power3.out" }}, {t0});')
            shot_js.append(f'tl.fromTo("#ci{n}-{k}", {{ scale: 1.18 }}, {{ scale: 1.0, duration: {round(e - t0, 3)}, ease: "power1.out" }}, {t0});')
        continue
    if kind == "plan":
        top, iw, ih = mot
        dh = 540
        dw = round(iw * dh / ih)
        shot_html.append(f'      <div id="sw{n}" class="shot" style="left:0;top:0;width:{W}px;height:{H}px;z-index:{n}">\n'
                         f'        <div id="v{n}" class="clip blueprint" data-start="{s}" data-duration="{d}" data-track-index="0">\n'
                         f'          <div id="pw{n}" class="plan-wrap" style="left:{(W - dw) // 2}px;top:{top}px;width:{dw}px;height:{dh}px">\n'
                         f'            <img id="pi{n}" class="plan-img" src="assets/{src}" alt="" />\n'
                         f'            <div id="pp{n}" class="plan-pen"></div>\n'
                         f'          </div>\n        </div>\n      </div>')
        shot_js.append(f'tl.fromTo("#pi{n}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 1.5, ease: "power2.inOut" }}, {s + 0.1:.3f});')
        shot_js.append(f'tl.fromTo("#pp{n}", {{ x: 0, opacity: 1 }}, {{ x: {dw}, duration: 1.5, ease: "power2.inOut" }}, {s + 0.1:.3f});')
        shot_js.append(f'tl.to("#pp{n}", {{ opacity: 0, duration: 0.2 }}, {s + 1.6:.3f});')
        shot_js.append(f'tl.fromTo("#pw{n}", {{ scale: 0.97 }}, {{ scale: 1.02, duration: {d}, ease: "none" }}, {s});')
        continue
    if kind == "p":
        size = f"left:0;top:0;width:{W}px;height:{H}px"
    else:
        size = f"left:0;top:0;width:3413px;height:{H}px"
    if src.endswith(".mp4"):
        media = (f'<video id="v{n}" class="clip media" data-start="{s}" data-duration="{d}" '
                 f'data-media-start="{ms}" data-track-index="0" src="assets/{src}" muted playsinline></video>')
    else:
        media = (f'<img id="v{n}" class="clip media" data-start="{s}" data-duration="{d}" '
                 f'data-track-index="0" src="assets/{src}" alt="" />')
    shot_html.append(f'      <div id="sw{n}" class="shot" style="{size};z-index:{n}">\n        {media}\n      </div>')
    if mot[0] == "in":
        a, b = mot[1], mot[2]
        mid = a - (a - b) * 0.55
        shot_js.append(f'tl.fromTo("#sw{n}", {{ scale: {a} }}, {{ scale: {mid:.3f}, duration: 0.6, ease: "power3.out" }}, {s});')
        shot_js.append(f'tl.to("#sw{n}", {{ scale: {b}, duration: {round(d - 0.6, 3)}, ease: "none" }}, {s + 0.6:.3f});')
    else:
        a, b = mot[1], mot[2]
        shot_js.append(f'tl.fromTo("#sw{n}", {{ x: {a} }}, {{ x: {b}, duration: {d}, ease: "power1.inOut" }}, {s});')

# white flash on the style montage cuts + outro
flash_times = [35.85, 38.05, 40.52, 42.95, 44.85, OUTRO_START]
flash_js = "\n".join(
    f'tl.fromTo("#flash", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {t});'
    for i, t in enumerate(flash_times))

# ---------------------------------------------------------------- sfx
WH, WS, WC = "whoosh.mp3", "whoosh-short.mp3", "whoosh-cinematic.mp3"
def at_peak(t, peak): return round(max(0, t - peak - 0.03), 3)
sfx = [  # (file, start, duration, volume, media_start)
    ("impact-bass-1.mp3", 0.0, 2.0, 0.22, 0),
]
cut_whoosh = [(5.19, WS), (8.30, WH), (12.75, WS), (16.55, WH), (20.80, WS), (25.70, WH),
              (35.85, WS), (38.05, WH), (40.52, WS), (42.95, WH), (44.85, WS),
              (31.05, WS), (31.95, WS), (49.00, WH), (52.60, WS), (55.65, WH), (58.89, WH)]
for t, f in cut_whoosh:
    sfx.append((f, at_peak(t, 0.162), 0.45, 0.45, 0))
for t in (30.98, 47.75):
    sfx.append((WC, at_peak(t, 2.503), 4.2, 0.22, 0))
# pops on the style labels and the location chip
for t in (11.30, 36.10, 38.30, 40.77, 43.20, 45.10):
    sfx.append(("pop.mp3", at_peak(t, 0.12), 0.6, 0.55, 0))
# outro: riser into reveal, pins, impact + sparkle on the CTA
sfx += [
    ("riser.mp3", at_peak(OUTRO_START, 3.47), 3.9, 0.12, 0),
    ("whoosh-cinematic.mp3", round(OUTRO_START - 0.05, 3), 2.2, 0.18, 2.2),
    ("ping.mp3", at_peak(64.20, 0.324), 1.0, 0.9, 0),
    ("ping.mp3", at_peak(64.86, 0.324), 1.0, 0.9, 0),
    ("impact-bass-1.mp3", at_peak(66.60, 0.073), 2.0, 0.2, 0),
    ("sparkle.mp3", at_peak(66.70, 0.027), 1.8, 0.3, 0),
]
sfx_html = []
track_end = {}
for k, (f, s, d, v, ms) in enumerate(sorted(sfx, key=lambda x: x[1]), 1):
    tr = next(t for t in range(11, 30) if track_end.get(t, -1) <= s)
    track_end[tr] = s + d
    extra = f' data-media-start="{ms}"' if ms else ""
    sfx_html.append(f'      <audio id="sfx{k}" class="clip" data-start="{s}" data-duration="{d}"{extra} '
                    f'data-track-index="{tr}" data-volume="{v}" src="assets/sfx/{f}"></audio>')

# ---------------------------------------------------------------- index.html
index = f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --gold: {GOLD};
        --red: {RED};
        --ink: #ffffff;
        --ground: #0b1712;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ground); }}
      .shot {{ position: absolute; transform-origin: 50% 50%; }}
      .collage {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: #0b1712; }}
      .strip {{ position: absolute; left: 0; width: {W}px; height: 380px; overflow: hidden; }}
      .strip-img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
      .blueprint {{
        position: absolute; left: 0; top: 0; width: 100%; height: 100%;
        background-color: #0e2a47;
        background-image: linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);
        background-size: 54px 54px;
      }}
      .plan-wrap {{ position: absolute; transform-origin: 50% 50%; }}
      .plan-img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
      .plan-pen {{
        position: absolute; left: 0; top: -20px; width: 6px; height: calc(100% + 40px); margin-left: -3px;
        background: {GOLD}; box-shadow: 0 0 24px {GOLD}, 0 0 8px #fff; opacity: 0;
      }}
      .shot .media {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
      #topshade {{
        position: absolute; left: 0; top: 0; width: {W}px; height: 820px; z-index: 40; pointer-events: none;
        background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.28) 55%, rgba(0,0,0,0) 100%);
      }}
      #midshade {{
        position: absolute; left: 0; top: 960px; width: {W}px; height: 520px; z-index: 40; pointer-events: none;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.22) 45%, rgba(0,0,0,0) 100%);
      }}
      #flash {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; z-index: 90; background: #fff; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(shot_html)}

      <div id="topshade" data-layout-ignore></div>
      <div id="midshade" data-layout-ignore></div>

      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html"
        data-start="{OUTRO_START}" data-duration="{round(TOTAL - OUTRO_START, 3)}" data-track-index="1"
        data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:30"></div>

      <div id="titles" data-composition-id="titles" data-composition-src="compositions/titles.html"
        data-start="0" data-duration="{OUTRO_START}" data-track-index="2"
        data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:60"></div>

      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{TOTAL}" data-track-index="3"
        data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:80"></div>

      <div id="flash" data-layout-ignore></div>

      <audio id="vo" class="clip" data-start="0" data-duration="67.82" data-track-index="10" data-volume="1" src="assets/vo-norm.mp3"></audio>
{chr(10).join(sfx_html)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + l for l in shot_js)}
      // shades fade away for the outro card
      tl.to(["#topshade", "#midshade"], {{ opacity: 0, duration: 0.3, ease: "power2.out" }}, {OUTRO_START});
{chr(10).join("      " + l for l in flash_js.splitlines())}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(PROJ, "index.html"), "w").write(index)

# ---------------------------------------------------------------- titles
# safe zone: left 10% (108px) .. right 18% (194px); headline box left 130, width 756 (70%)
HL_LEFT, HL_W, HL_TOP = 130, 756, 300
def fs(text, cap):  # Montserrat 900 uppercase ~0.74em per char
    return int(min(cap, HL_W / (0.74 * max(len(text), 1))))

pin_svg = ('<svg viewBox="0 0 24 24" width="34" height="34"><path fill="' + RED + '" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.6A2.6 2.6 0 1 1 12 6.4a2.6 2.6 0 0 1 0 5.2z"/></svg>')

heads = [  # id, start, end, line1, line2, chip(top), extra
    ("h1", 0.0, 5.10, "RUMAH", "SPLIT LEVEL", None, None),
    ("h2", 5.19, 8.22, "DESIGN DEKAT", "MANA?", None, None),
    ("h3", 8.30, 12.70, "PROJEK", "MAHLIGAI IDAMAN", None, "loc"),
    ("h4", 12.75, 16.50, "NAMPAK GAH", "DARI LUAR", None, None),
    ("h5", 16.55, 20.75, "ARAS LANTAI", "BERBEZA", None, None),
    ("h6", 20.80, 25.65, "UNIK & ADA", "KARAKTER", None, None),
    ("h7", 25.70, 27.30, "KORANG", "TAHU TAK?", None, None),
    ("h8", 27.35, 30.93, "SPLIT LEVEL", "BUKAN SATU STYLE JE", None, None),
    ("h9", 30.98, 35.80, "PELBAGAI KOLEKSI", "DESIGN SPLIT LEVEL", None, None),
    ("h10", 35.97, 38.00, "MODERN", "TROPICAL", "KATALOG 01 / 05", None),
    ("h11", 38.09, 40.47, "MUJI", "STYLE", "KATALOG 02 / 05", None),
    ("h12", 40.65, 42.90, "ENGLISH", "STYLE", "KATALOG 03 / 05", None),
    ("h13", 42.97, 44.80, "NORDIC", "STYLE", "KATALOG 04 / 05", None),
    ("h14", 45.00, 47.70, "MELAYU", "TRADISIONAL", "KATALOG 05 / 05", None),
    ("h15", 47.80, 52.55, "PELUKIS PELAN", "SENDIRI", None, None),
    ("h16", 52.60, 58.84, "IKUT CITA RASA", "& KESESUAIAN TANAH", None, None),
    ("h17", 58.89, 62.50, "TAK PERLU", "PENING LAGI!", None, None),
]
t_html, t_js = [], []
for hid, s, e, l1, l2, chip, extra in heads:
    f1 = fs(l1, 96 if chip is None else 120)
    f2 = fs(l2, 104 if chip is None else 120)
    inner = []
    if chip:
        inner.append(f'<div id="{hid}-chip" class="chip">{chip}</div>')
    inner.append(f'<div id="{hid}-a" class="l1" style="font-size:{f1}px">{html.escape(l1)}</div>')
    inner.append(f'<div id="{hid}-b" class="l2" style="font-size:{f2}px">{html.escape(l2)}</div>')
    if extra == "loc":
        inner.append(f'<div id="{hid}-loc" class="loc">{pin_svg}<span>KEMAMAN, TERENGGANU</span></div>')
    vis = ' style="opacity:1"' if s == 0 else ""
    t_html.append(f'    <div id="{hid}" class="hl"{vis}>\n      ' + "\n      ".join(inner) + "\n    </div>")
    parts = ([f'"#{hid}-chip"'] if chip else []) + [f'"#{hid}-a"', f'"#{hid}-b"']
    if s == 0:
        t_js.append(f'tl.fromTo([{", ".join(parts)}], {{ scale: 1.14 }}, {{ scale: 1, duration: 0.6, ease: "power3.out" }}, 0);')
    else:
        t_js.append(f'tl.set("#{hid}", {{ opacity: 1 }}, {s});')
        t_js.append(f'tl.fromTo([{", ".join(parts)}], {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", stagger: 0.08 }}, {s});')
    if extra == "loc":
        t_js.append(f'tl.fromTo("#{hid}-loc", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, 11.30);')
    t_js.append(f'tl.to("#{hid}", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {round(e - 0.18, 3)});')
    t_js.append(f'tl.set("#{hid}", {{ opacity: 0 }}, {e});')

titles = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Montserrat", sans-serif; }}
    #root .hl {{
      position: absolute; left: {HL_LEFT}px; top: {HL_TOP}px; width: {HL_W}px;
      text-align: center; opacity: 0;
      display: flex; flex-direction: column; align-items: center; gap: 6px;
    }}
    #root .l1, #root .l2 {{
      font-weight: 900; line-height: 1.02; letter-spacing: -0.01em; white-space: nowrap;
      text-shadow: 0 4px 0 rgba(0,0,0,0.35), 0 6px 28px rgba(0,0,0,0.55);
    }}
    #root .l1 {{ color: #ffffff; }}
    #root .l2 {{ color: {GOLD}; }}
    #root .chip {{
      font-weight: 800; font-size: 30px; letter-spacing: 0.12em; color: #1a1a1a;
      background: {GOLD}; border-radius: 999px; padding: 8px 22px; margin-bottom: 10px;
    }}
    #root .loc {{
      margin-top: 22px; display: flex; align-items: center; gap: 10px;
      background: #ffffff; color: #1a1a1a; border-radius: 999px; padding: 12px 28px 12px 18px;
      font-weight: 800; font-size: 32px; letter-spacing: 0.04em; opacity: 0;
      box-shadow: 0 8px 26px rgba(0,0,0,0.35);
    }}
  </style>
  <div id="root" data-composition-id="titles" data-width="{W}" data-height="{H}">
{chr(10).join(t_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + l for l in t_js)}
    window.__timelines["titles"] = tl;
  </script>
</template>
'''
open(os.path.join(PROJ, "compositions/titles.html"), "w").write(titles)

# ---------------------------------------------------------------- captions
# subtitle zone: 55%–72% of height; width 720 (≈67%), left 140 → right margin 220 (≈20%)
c_html, c_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.15, g[0]["start"] - 0.05)
    nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else None
    last_end = g[-1]["end"]
    ge = nxt if (nxt is not None and nxt - last_end < 0.6) else last_end + 0.35
    ge = round(min(ge, TOTAL - 0.05), 3)
    gid = f"cg{gi}"
    brk = None
    is_outro = g[0]["start"] >= OUTRO_START
    if glen(g) > 22 and not is_outro:
        best = None
        for k in range(1, len(g)):
            m = max(glen(g[:k]), glen(g[k:]))
            if best is None or m < best: best, brk = m, k
    spans = " ".join(("<br/>" if k == brk else "") + f'<span id="{gid}w{k}" class="w">{html.escape(w["text"])}</span>' for k, w in enumerate(g))
    c_html.append(f'    <div id="{gid}" class="cg{" outro" if is_outro else ""}"><div class="cg-in">{spans}</div></div>')
    c_js.append(f'tl.fromTo("#{gid}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.16, ease: "power2.out" }}, {gs:.3f});')
    for k, w in enumerate(g):
        c_js.append(f'tl.set("#{gid}w{k}", {{ color: "{GOLD}" }}, {w["start"]:.3f}); tl.set("#{gid}w{k}", {{ color: "#ffffff" }}, {min(w["end"], ge):.3f});')
    c_js.append(f'tl.to("#{gid}", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {ge - 0.12:.3f});')
    c_js.append(f'tl.set("#{gid}", {{ opacity: 0 }}, {ge:.3f});')

captions = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Montserrat", sans-serif; }}
    #root .cg {{
      position: absolute; left: 140px; top: 1075px; width: 720px;
      text-align: center; opacity: 0; overflow: visible;
    }}
    #root .cg-in {{
      display: inline; font-weight: 800; font-size: 50px; line-height: 1.42; color: #ffffff;
      background: rgba(0,0,0,0.42); padding: 4px 16px; border-radius: 14px;
      -webkit-box-decoration-break: clone; box-decoration-break: clone;
      text-shadow: 0 2px 6px rgba(0,0,0,0.6);
    }}
    #root .cg.outro {{ top: 1035px; }}
    #root .cg.outro .cg-in {{ font-size: 40px; white-space: nowrap; background: rgba(0,0,0,0.6); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join(c_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + l for l in c_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open(os.path.join(PROJ, "compositions/captions.html"), "w").write(captions)

# ---------------------------------------------------------------- outro
o = lambda t: round(t - OUTRO_START, 3)  # absolute -> local
# image is 720x1280 -> scale 1.5. pin heads ~ (318,582) and (496,660) in source
PIN1 = (477, 873); PIN2 = (744, 990)
outro = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #06231a; }}
    #root .o-zoom {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; transform-origin: 50% 50%; }}
    #root .o-img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    #root .ring {{
      position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
      border: 6px solid {GOLD}; box-shadow: 0 0 24px {GOLD}; opacity: 0;
    }}
    #root .cta-glow {{
      position: absolute; left: 92px; top: 1440px; width: 898px; height: 96px; border-radius: 60px;
      border: 5px solid {GOLD}; box-shadow: 0 0 40px {GOLD}, inset 0 0 22px rgba(255,200,61,0.6); opacity: 0;
    }}
    #root .shine {{
      position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; mix-blend-mode: screen;
      background: linear-gradient(105deg, rgba(255,255,255,0) 38%, rgba(255,255,255,0.55) 50%, rgba(255,255,255,0) 62%);
    }}
  </style>
  <div id="root" data-composition-id="outro" data-width="{W}" data-height="{H}">
    <div id="o-zoom" class="o-zoom">
      <img id="o-img" class="o-img" src="assets/outro.jpg" alt="" />
      <div id="o-ring1" class="ring" style="left:{PIN1[0]}px;top:{PIN1[1]}px" data-layout-ignore></div>
      <div id="o-ring2" class="ring" style="left:{PIN2[0]}px;top:{PIN2[1]}px" data-layout-ignore></div>
      <div id="o-cta" class="cta-glow" data-layout-ignore></div>
    </div>
    <div id="o-shine" class="shine" data-layout-ignore></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // push in on the map and the two branches
    tl.fromTo("#o-zoom", {{ scale: 1.12, y: 40 }}, {{ scale: 1, y: 0, duration: 0.9, ease: "power3.out" }}, 0);
    // pin pulses on "Kelantan" and "Terengganu"
    tl.fromTo("#o-ring1", {{ scale: 0.3, opacity: 1 }}, {{ scale: 2.1, opacity: 0, duration: 1.0, ease: "power2.out", repeat: 5 }}, {o(64.17)});
    tl.fromTo("#o-ring2", {{ scale: 0.3, opacity: 1 }}, {{ scale: 2.1, opacity: 0, duration: 1.0, ease: "power2.out", repeat: 5 }}, {o(64.83)});
    // "Hubungi" -> pull back to reveal the full CTA card
    tl.to("#o-zoom", {{ scale: 0.97, duration: 0.25, ease: "power2.out" }}, {o(65.80)});
    tl.to("#o-zoom", {{ scale: 1, duration: 0.5, ease: "back.out(3)" }}, {o(66.05)});
    // light sweep + glowing CTA button
    tl.fromTo("#o-shine", {{ xPercent: -110 }}, {{ xPercent: 110, duration: 0.9, ease: "power2.inOut" }}, {o(66.65)});
    tl.fromTo("#o-shine", {{ xPercent: -110 }}, {{ xPercent: 110, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {o(69.2)});
    tl.fromTo("#o-cta", {{ opacity: 0, scale: 1 }}, {{ opacity: 1, scale: 1.035, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {o(66.8)});
    window.__timelines["outro"] = tl;
  </script>
</template>
'''
open(os.path.join(PROJ, "compositions/outro.html"), "w").write(outro)

print("groups:")
for g in groups:
    print(f'  {g[0]["start"]:6.2f}-{g[-1]["end"]:6.2f}  ' + " ".join(w["text"] for w in g))
