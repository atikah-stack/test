"""Builds index.html and every scene for the 5-bedroom / 2,289 sq ft house tour intro.

Run `python3 build.py`. Timeline = the presenter's own speech (assets/audio/presenter-voice.wav,
cleaned and levelled from copy_CCA2C574...mov); pictures change on top of it (J/L cuts).
Floor-plan room shapes are traced from the real plan (assets/plan/rooms.json, checked by overlay
on IMG_2028.jpg); the plan picture is that same drawing, inverted to white lines on charcoal.
"""
import json

W, Y = "#FFFFFF", "#FFD43B"          # brand white, golden yellow
BLUE = "#6FB6FF"                     # bathrooms only (function marker)
GRADE = json.dumps({"preset": "warm-daylight", "intensity": 0.3})
PRESENTER = "assets/src/copy_CCA2C574-92FF-472F-A582-F8CD267A0344.mov"
PILLARS = "assets/src/copy_EC564B66-8B16-45F2-8E32-A048F72B7754.MOV"
WIDE = "assets/src/IMG_1405.mov"
FACE = "50% 40%"
TOTAL = 22.75
ROOMS = json.load(open("assets/plan/rooms.json"))

# (id, start, duration, src, media start, rate, zoom from, zoom to, fade-in)
SHOTS = [
    ("v1", 0.0, 1.95, PILLARS, 2.6, 1, 1.00, 1.07, 0),       # low pillars along the porch
    ("v2", 1.95, 1.45, PRESENTER, 1.95, 1, 1.00, 1.03, 0),   # presenter, medium
    ("v3", 5.6, 1.9, PRESENTER, 5.6, 1, 1.00, 1.03, 0),
    ("v4", 7.5, 2.9, PRESENTER, 7.5, 1, 1.16, 1.20, 0),      # jump to closer framing
    ("v5", 10.4, 1.0, PRESENTER, 10.4, 1, 1.00, 1.30, 0),    # punch-in on "Tapi tuan-puan"
    ("v6", 11.4, 4.5, WIDE, 0.0, 0.83, 1.00, 1.05, 0),       # wide house, ground-locked 2,289 KPS
    ("v7", 20.5, 2.25, PRESENTER, 20.5, 1, 1.00, 1.04, 0),   # presenter walks to the house
]
PRESENTER_SHOTS = {"v2", "v3", "v4", "v5", "v7"}

# Scenes: id -> (start, duration, kind)
SCENES = {
    "hook": (0.12, 3.28, "graphics"),
    "planq": (3.4, 2.2, "graphics"),
    "recom": (7.6, 2.75, "graphics"),
    "ground": (11.55, 4.3, "graphics"),
    "planrooms": (15.9, 5.0, "graphics"),
    "endlogo": (21.2, 1.55, "graphics"),
    "subs": (0.0, 22.2, "captions"),
}

SUBS = [  # (start, end, text) — loghat kept, numbers and keywords marked **
    (0.00, 1.95, "Biasanya kalau client tanya Abe, “Abe,"),
    (2.20, 5.45, "berapa keluasan rumah hok dapat kalau dengan **5 bilik**, Abe?”"),
    (5.60, 7.15, "Ha, biasanya Abe akan advise ke dia,"),
    (7.45, 10.35, "saiz **2,500 kaki persegi** ke atas hok selesa."),
    (10.45, 11.35, "Tapi tuan-puan,"),
    (11.40, 15.80, "rumah di belakang Abe ni berkeluasan **2,289 kaki persegi** sahaja,"),
    (15.95, 17.68, "tapi boleh dapat **5 bilik tidur**,"),
    (17.75, 19.20, "**3 bilik air**, tuan-puan."),
    (19.30, 20.85, "Nak tengok apa yang ada kat dalam?"),
    (21.00, 22.20, "Jom Abe tunjuk!"),
]

SFX = [  # (id, file, start, duration, volume)
    ("x-hook", "impact-bass-1.mp3", 0.15, 2.0, 0.22),
    ("x-cut1", "whoosh-short.mp3", 1.9, 0.6, 0.12),
    ("x-plan", "whoosh-cinematic.mp3", 3.3, 2.0, 0.14),
    ("x-q", "sparkle.mp3", 4.2, 1.4, 0.10),
    ("x-c1", "click-soft.mp3", 7.75, 0.4, 0.18),
    ("x-c2", "click-soft.mp3", 8.05, 0.4, 0.18),
    ("x-c3", "click-soft.mp3", 8.35, 0.4, 0.18),
    ("x-rise", "riser.mp3", 10.2, 1.3, 0.14),
    ("x-2289", "impact-bass-2.mp3", 13.55, 2.4, 0.24),
    ("x-b1", "pop.mp3", 16.35, 0.6, 0.12), ("x-b2", "pop.mp3", 16.6, 0.6, 0.12),
    ("x-b3", "pop.mp3", 16.85, 0.6, 0.12), ("x-b4", "pop.mp3", 17.1, 0.6, 0.12),
    ("x-b5", "pop.mp3", 17.35, 0.6, 0.12),
    ("x-w1", "click-soft.mp3", 17.8, 0.4, 0.18), ("x-w2", "click-soft.mp3", 18.05, 0.4, 0.18),
    ("x-w3", "click-soft.mp3", 18.3, 0.4, 0.18),
    ("x-spec", "whoosh-short.mp3", 19.15, 0.6, 0.12),
    ("x-zoom", "whoosh-cinematic.mp3", 20.1, 2.0, 0.12),
    ("x-end", "chime.mp3", 21.3, 1.4, 0.14),
]

# ---------------------------------------------------------------- root
rows = []
for i, (vid, st, d, src, ms, rate, z0, z1, _) in enumerate(SHOTS):
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1 else ""
    origin = f";transform-origin:{FACE}" if vid in PRESENTER_SHOTS else ""
    rows.append(f'      <video id="{vid}" class="shot clip" src="{src}" muted playsinline data-start="{st}" '
                f'data-duration="{d}" data-media-start="{ms}"{rate_attr} data-track-index="{i % 2}" '
                f'data-color-grading=\'{GRADE}\' style="z-index:{i + 1}{origin}"></video>')
rows.append(f'      <audio id="voice" class="clip" src="assets/audio/presenter-voice.wav" data-start="0" '
            f'data-duration="{TOTAL}" data-media-start="0" data-volume="1" data-track-index="10"></audio>')
for n, (sid, f, s, d, v) in enumerate(SFX):
    rows.append(f'      <audio id="{sid}" class="clip" src="assets/sfx/{f}" data-start="{s}" data-duration="{d}" '
                f'data-volume="{v}" data-fade-out="0.2" data-track-index="{11 + n % 4}"></audio>')
rows.append(f'      <div id="fade" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-layout-ignore></div>')
for n, (cid, (s, d, kind)) in enumerate(SCENES.items()):
    z = 80 if kind == "captions" else 40 + n
    rows.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                f'data-start="{s}" data-duration="{d}" data-track-index="{3 + n % 3}" data-track-kind="{kind}" '
                f'data-width="1080" data-height="1920" style="z-index:{z}"></div>')

js = json.dumps([[s[0], s[1], s[2], s[6], s[7]] for s in SHOTS])
html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #17181a; }}
      #root {{ width: 100%; height: 100%; background: #17181a; font-family: "Montserrat", sans-serif; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #fade {{ position: absolute; inset: 0; z-index: 90; background: #0b0b0b; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="30" data-width="1080" data-height="1920">
{chr(10).join(rows)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {js}.forEach(([id, s, d, z0, z1]) => tl.fromTo("#" + id, {{ scale: z0 }}, {{ scale: z1, duration: d, ease: "none" }}, s));
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "sine.in" }}, {TOTAL - 0.5});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)

# ---------------------------------------------------------------- scene helpers
SHADOW = "0 6px 24px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.5)"
BASE = f"""
    #root {{ position:absolute; inset:0; font-family:"Montserrat",sans-serif; }}
    .ln {{ white-space:nowrap; font-weight:800; text-transform:uppercase; line-height:1.06; letter-spacing:0.01em; text-shadow:{SHADOW}; }}
    .shade {{ position:absolute; left:0; right:0; padding:100px 162px 100px 60px; margin-top:-100px; display:flex; flex-direction:column;
      align-items:center; text-align:center; gap:4px;
      background:radial-gradient(ellipse 60% 50% at 46% 50%, rgba(0,0,0,.42) 0%, rgba(0,0,0,.2) 45%, rgba(0,0,0,0) 78%); }}
"""


import re
PLAN_NAMES = re.compile(r"\b(pbox|bg|side|scan|pimg|psvg|bed\d|bath\d|living|num\d|bed|bath|liv|num|c\d|bl|ba-m|ba|s1u|s1|s2|s3|q1|q2|q3)\b")


def scene(cid, dur, css, body, js):
    if cid.startswith("plan"):  # both plan scenes share element names; keep each scene's selectors its own
        css, body, js = (PLAN_NAMES.sub(lambda m: f"{cid}-{m.group(0)}", x) for x in (css, body, js))
    open(f"compositions/{cid}.html", "w").write(f"""<template>
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
""")


def rise(sel, at, d=0.6, y=24):
    return f'    tl.fromTo("{sel}", {{ opacity:0, y:{y}, scale:0.95 }}, {{ opacity:1, y:0, scale:1, duration:{d}, ease:"power2.out" }}, {at});'


def out(sel, at, d=0.35):
    return f'    tl.to("{sel}", {{ opacity:0, duration:{d}, ease:"sine.in" }}, {round(at, 2)});'


# ---------------------------------------------------------------- hook
d = SCENES["hook"][1]
scene("hook", d, """
    #hk { top:330px; }
    #hk-1 { color:#FFFFFF; font-size:54px; }
    #hk-2, #hk-3 { color:""" + Y + """; font-size:76px; }""",
      f"""    <div id="hk" class="shade clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="hk-1" class="ln">RUMAH BAWAH 2,300 KPS</div>
      <div id="hk-2" class="ln">SIAP ADA</div>
      <div id="hk-3" class="ln">5 BILIK TIDUR!</div>
    </div>""",
      "\n".join([rise("#hk-1", 0, 0.5), rise("#hk-2", 0.22, 0.5), rise("#hk-3", 0.34, 0.5), out("#hk", d - 0.35)]))

# ---------------------------------------------------------------- recommended size (generic icon, not this house's plan)
d = SCENES["recom"][1]
scene("recom", d, f"""
    #rc {{ top:330px; }}
    #rc-1 {{ color:#FFFFFF; font-size:38px; letter-spacing:0.04em; }}
    #rc-n {{ color:{Y}; font-size:112px; }}
    #rc-rule {{ position:relative; width:560px; height:30px; margin-top:6px; }}
    #rc-line {{ position:absolute; left:0; right:0; top:14px; height:3px; background:{Y}; transform-origin:50% 50%; }}
    .tick {{ position:absolute; top:2px; width:3px; height:26px; background:{Y}; }}""",
      f"""    <div id="rc" class="shade clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="rc-1" class="ln">KELUASAN YANG DISARANKAN</div>
      <div id="rc-n" class="ln">0 KPS</div>
      <div id="rc-rule"><div id="rc-line"></div><div id="rc-t1" class="tick" style="left:0"></div><div id="rc-t2" class="tick" style="right:0"></div></div>
    </div>""",
      "\n".join([rise("#rc-1", 0, 0.5), rise("#rc-n", 0.1, 0.5),
                 '    const n = { v: 0 };',
                 '    tl.to(n, { v: 2500, duration: 0.9, ease: "power2.out", onUpdate: () => {',
                 '      document.querySelector("#rc-n").textContent = Math.round(n.v).toLocaleString("en-US") + (n.v >= 2499.5 ? "+ KPS" : " KPS"); } }, 0.15);',
                 '    tl.fromTo("#rc-line", { scaleX:0 }, { scaleX:1, duration:0.7, ease:"power2.out" }, 0.3);',
                 '    tl.fromTo(["#rc-t1","#rc-t2"], { opacity:0 }, { opacity:1, duration:0.3 }, 0.8);',
                 out("#rc", d - 0.35)]))

# ---------------------------------------------------------------- ground-locked 2,289 KPS + comparison
d = SCENES["ground"][1]
reveal = 2.0  # local time of "2,289" (global 13.55)
scene("ground", d, f"""
    #gw {{ position:absolute; left:0; right:100px; top:1100px; height:430px; perspective:900px; perspective-origin:50% -60%; }}
    #gp {{ position:absolute; left:0; right:0; bottom:0; display:flex; flex-direction:column; align-items:center; transform-origin:50% 100%; }}
    #g-n {{ font-weight:900; font-size:168px; color:{Y}; line-height:1; letter-spacing:-0.01em;
      text-shadow:0 26px 30px rgba(0,0,0,.55), 0 4px 10px rgba(0,0,0,.45); white-space:nowrap; }}
    #g-u {{ font-weight:800; font-size:56px; color:#FFFFFF; letter-spacing:0.3em; margin-top:4px; white-space:nowrap;
      text-shadow:0 14px 20px rgba(0,0,0,.55); }}
    #g-rule {{ position:relative; width:760px; height:30px; margin-top:16px; }}
    #g-line {{ position:absolute; left:0; right:0; top:14px; height:4px; background:{Y}; transform-origin:50% 50%; }}
    .gt {{ position:absolute; top:0; width:4px; height:30px; background:{Y}; }}
    #cmp {{ top:330px; }}
    .lbl {{ font-weight:600; font-size:28px; color:#FFFFFF; letter-spacing:0.12em; opacity:.9; text-shadow:{SHADOW}; }}
    #cmp-row {{ display:flex; align-items:flex-end; gap:30px; }}
    .cell {{ display:flex; flex-direction:column; align-items:center; gap:2px; }}
    #c-a {{ color:#FFFFFF; font-size:56px; }}
    #c-b {{ color:{Y}; font-size:56px; }}
    #c-arrow {{ color:#FFFFFF; font-size:52px; }}""",
      f"""    <div id="cmp" class="shade clip" data-start="0" data-duration="{d}" data-track-index="1">
      <div id="cmp-row">
        <div class="cell"><div class="lbl">DISARANKAN</div><div id="c-a" class="ln">2,500+ KPS</div></div>
        <div id="c-arrow" class="ln">→</div>
        <div class="cell"><div class="lbl">RUMAH INI</div><div id="c-b" class="ln">2,289 KPS</div></div>
      </div>
    </div>
    <div id="gw" class="clip" data-start="0" data-duration="{d}" data-track-index="0">
      <div id="gp">
        <div id="g-n">2,289</div>
        <div id="g-u">KPS</div>
        <div id="g-rule"><div id="g-line"></div><div class="gt" style="left:0"></div><div class="gt" style="right:0"></div></div>
      </div>
    </div>""",
      "\n".join([
          # the number stands up out of the ground, then settles lying on it
          f'    tl.fromTo("#gp", {{ rotationX:88, opacity:0, scale:0.9 }}, {{ rotationX:64, opacity:1, scale:1, duration:0.9, ease:"power3.out" }}, {reveal});',
          f'    tl.fromTo("#g-line", {{ scaleX:0 }}, {{ scaleX:1, duration:0.8, ease:"power2.out" }}, {reveal + 0.35});',
          f'    tl.to("#gp", {{ y:6, duration:{d - reveal - 0.2}, ease:"none" }}, {reveal + 0.9});',
          '    tl.set("#cmp", { opacity:0 }, 0);',
          f'    tl.to("#cmp", {{ opacity:1, duration:0.4 }}, {reveal + 0.5});',
          rise("#c-a", reveal + 0.5, 0.45), rise("#c-arrow", reveal + 0.75, 0.4), rise("#c-b", reveal + 0.95, 0.45),
          out("#gw", d - 0.35), out("#cmp", d - 0.35)]))

# ---------------------------------------------------------------- floor plan scenes
VB = (60, 380, 940, 1565)                 # plan crop, display coords of IMG_2028
BOX = dict(left=220, top=400, w=640)      # on screen, centred; right edge stays left of the 15% right margin
BOX["h"] = round(BOX["w"] * VB[3] / VB[2])


def centroid(p):
    xs, ys = [a for a, _ in p], [b for _, b in p]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2


def poly(pid, pts, cls):
    return f'<polygon id="{pid}" class="{cls}" points="{" ".join(f"{x},{y}" for x, y in pts)}" />'


def plan_svg(numbers):
    beds = list(ROOMS["bed"].items())  # Master, 2, 3, 4, 5
    parts = []
    for k, (name, pts) in enumerate(beds, 1):
        parts.append(poly(f"bed{k}", pts, "bed"))
    for k, (name, pts) in enumerate(ROOMS["bath"].items(), 1):
        parts.append(poly(f"bath{k}", pts, "bath"))
    parts.append(poly("living", ROOMS["other"]["LIVING"], "liv"))
    if numbers:
        for k, (name, pts) in enumerate(beds, 1):
            cx, cy = centroid(pts)
            parts.append(f'<text id="num{k}" class="num" x="{cx}" y="{cy + 22}" text-anchor="middle">0{k}</text>')
    return (f'<svg id="psvg" viewBox="{" ".join(map(str, VB))}" preserveAspectRatio="none" '
            f'style="position:absolute;inset:0;width:100%;height:100%">{"".join(parts)}</svg>')


PLAN_CSS = f"""
    #bg {{ position:absolute; inset:0; background:#17181a;
      background-image:linear-gradient(rgba(255,255,255,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.045) 1px, transparent 1px);
      background-size:60px 60px; }}
    #pbox {{ position:absolute; left:{BOX['left']}px; top:{BOX['top']}px; width:{BOX['w']}px; height:{BOX['h']}px; }}
    #pimg {{ position:absolute; inset:0; width:100%; height:100%; opacity:.82; }}
    #scan {{ position:absolute; left:-8px; right:-8px; height:3px; top:0; background:{Y}; box-shadow:0 0 14px {Y}; }}
    .bed {{ fill:{Y}; fill-opacity:0; stroke:{Y}; stroke-width:3; stroke-opacity:0; vector-effect:non-scaling-stroke; }}
    .bath {{ fill:{BLUE}; fill-opacity:0; stroke:#FFFFFF; stroke-width:2.5; stroke-opacity:0; vector-effect:non-scaling-stroke; }}
    .liv {{ fill:#FFFFFF; fill-opacity:0; stroke:#FFFFFF; stroke-width:3; stroke-opacity:0; vector-effect:non-scaling-stroke; }}
    .num {{ font-family:"Montserrat",sans-serif; font-weight:900; font-size:56px; fill:#17181a; opacity:0; }}
    #side {{ position:absolute; left:60px; width:858px; top:0; height:1920px; }}
    .sl {{ position:absolute; left:0; width:858px; text-align:center; font-weight:800; text-transform:uppercase; line-height:1.04; white-space:nowrap; text-shadow:0 4px 14px rgba(0,0,0,.6); }}
"""


def plan_scene(cid, d, side_html, js_lines, numbers):
    scene(cid, d, PLAN_CSS + "".join(js_lines[0]),
          f"""    <div id="bg" class="clip" data-start="0" data-duration="{d}" data-track-index="0"></div>
    <div id="pbox" class="clip" data-start="0" data-duration="{d}" data-track-index="1">
      <img id="pimg" src="assets/plan/plan-dark.png" alt="Pelan lantai" />
      {plan_svg(numbers)}
      <div id="scan"></div>
    </div>
    <div id="side" class="clip" data-start="0" data-duration="{d}" data-track-index="2">
{side_html}
    </div>""", "\n".join(js_lines[1]))


DRAW = [
    '    tl.fromTo("#pbox", { clipPath:"inset(0% 0% 100% 0%)" }, { clipPath:"inset(0% 0% 0% 0%)", duration:0.85, ease:"power2.inOut" }, 0);',
    f'    tl.fromTo("#scan", {{ y:0, opacity:1 }}, {{ y:{BOX["h"]}, duration:0.85, ease:"power2.inOut" }}, 0);',
    '    tl.to("#scan", { opacity:0, duration:0.2 }, 0.85);',
]

# Question: "berapa keluasan ... kalau dengan 5 bilik, Abe?"
d = SCENES["planq"][1]
plan_scene("planq", d,
           f"""      <div id="q1" class="sl" style="top:292px;color:{Y};font-size:66px">5 BILIK TIDUR?</div>
      <div id="q2" class="sl" style="top:364px;color:#FFFFFF;font-size:30px;letter-spacing:0.12em;font-weight:600"></div>
      <div id="q3" class="sl" style="top:364px;color:#FFFFFF;font-size:30px;letter-spacing:0.12em;font-weight:600">BERAPA KPS?</div>""",
           ("", DRAW + [rise("#q1", 0.3, 0.5), rise("#q2", 0.42, 0.5), rise("#q3", 0.7, 0.5),
                        '    tl.fromTo(".bed", { strokeOpacity:0 }, { strokeOpacity:1, duration:0.4, stagger:0.08 }, 0.9);',
                        '    tl.to(".bed", { strokeOpacity:0.35, duration:0.3, yoyo:true, repeat:1 }, 1.5);',
                        '    tl.to(["#pbox","#side"], { opacity:0, duration:0.25 }, ' + str(d - 0.25) + ');']),
           numbers=False)

# Rooms: 5 bedrooms (16.35-17.6), 3 bathrooms (17.8-18.6), specs (19.2), zoom to living (20.1-20.9)
d = SCENES["planrooms"][1]
t0 = SCENES["planrooms"][0]
bed_at = [round(16.35 - t0 + 0.25 * k, 2) for k in range(5)]
bath_at = [round(17.8 - t0 + 0.25 * k, 2) for k in range(3)]
spec_at = round(19.2 - t0, 2)
zoom_at = round(20.3 - t0, 2)
lx, ly = centroid(ROOMS["other"]["LIVING"])
ox = round((lx - VB[0]) / VB[2] * BOX["w"]); oy = round((ly - VB[1]) / VB[3] * BOX["h"])
counters = f'      <div id="c5" class="sl" style="top:292px;color:{Y};font-size:66px">5 BILIK TIDUR</div>'
side = f"""{counters}
      <div id="bl" class="sl" style="top:366px;color:#FFFFFF;font-size:30px;letter-spacing:0.12em;font-weight:600">01 → 05</div>
      <div id="ba" class="sl" style="top:292px;color:#FFFFFF;font-size:66px">3 BILIK AIR</div>
      <div id="ba-m" style="position:absolute;left:394px;top:374px;width:70px;height:14px;border-radius:7px;background:{BLUE}"></div>
      <div id="s1" class="sl" style="top:290px;color:{Y};font-size:62px">2,289 KPS</div>
      <div id="s1u" class="sl" style="top:362px;color:#FFFFFF;font-size:32px">5 BILIK TIDUR | 3 BILIK AIR</div>
      <div id="s2" class="sl" style="top:362px"></div>
      <div id="s3" class="sl" style="top:362px"></div>"""
js = DRAW + ['    tl.set(["#c5","#bl","#ba","#ba-m","#s1","#s1u","#s2","#s3"], { opacity:0 }, 0);']
for k, at in enumerate(bed_at, 1):
    js += [f'    tl.to("#bed{k}", {{ fillOpacity:0.5, strokeOpacity:1, duration:0.22 }}, {at});',
           f'    tl.to("#num{k}", {{ opacity:1, duration:0.2 }}, {at + 0.05});']
js += [f'    tl.fromTo("#c5", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.35 }}, {bed_at[0]});',
       f'    tl.fromTo("#bl", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {bed_at[0] + 0.1});',
       f'    tl.to(["#c5","#bl"], {{ opacity:0, duration:0.2 }}, {bath_at[0] - 0.05});']
for k, at in enumerate(bath_at, 1):
    js.append(f'    tl.to("#bath{k}", {{ fillOpacity:0.55, strokeOpacity:1, duration:0.22 }}, {at});')
js += [f'    tl.fromTo(["#ba","#ba-m"], {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.3 }}, {bath_at[0]});',
       f'    tl.to(["#ba","#ba-m"], {{ opacity:0, duration:0.2 }}, {spec_at - 0.1});',
       rise("#s1", spec_at, 0.45), rise("#s1u", spec_at + 0.1, 0.45), rise("#s2", spec_at + 0.22, 0.45), rise("#s3", spec_at + 0.34, 0.45),
       f'    tl.to("#side", {{ opacity:0, duration:0.3 }}, {zoom_at});',
       f'    tl.to(".bed, .bath", {{ fillOpacity:0.12, strokeOpacity:0.35, duration:0.3 }}, {zoom_at});',
       f'    tl.to(".num", {{ opacity:0, duration:0.2 }}, {zoom_at});',
       f'    tl.to("#living", {{ fillOpacity:0.18, strokeOpacity:1, duration:0.3 }}, {zoom_at});',
       f'    tl.set("#pbox", {{ transformOrigin:"{ox}px {oy}px" }}, 0);',
       f'    tl.to("#pbox", {{ scale:2.6, x:{540 - BOX["left"] - ox}, y:{900 - BOX["top"] - oy}, duration:0.85, ease:"power2.in" }}, {zoom_at});',
       f'    tl.to(["#pbox","#bg"], {{ opacity:0, duration:0.4, ease:"sine.in" }}, {d - 0.42});']
plan_scene("planrooms", d, side, ("", js), numbers=True)

# ---------------------------------------------------------------- end logo
d = SCENES["endlogo"][1]
scene("endlogo", d, """
    #lg { position:absolute; left:380px; top:360px; width:300px; padding:22px 24px; border-radius:24px; background:#FFFFFF;
      box-shadow:0 14px 40px rgba(0,0,0,.3); }
    #lg img { display:block; width:252px; height:auto; }""",
      f"""    <div id="lg" class="clip" data-start="0" data-duration="{d}" data-track-index="0"><img src="assets/brand/logo-mi.png" alt="Mahligai Idaman" /></div>""",
      rise("#lg", 0.1, 0.6, 16))

# ---------------------------------------------------------------- subtitles
def mark(text):
    parts = text.split("**")
    return "".join(f'<span class="k">{p}</span>' if i % 2 else p for i, p in enumerate(parts))


rows_s, js_s = [], []
for i, (s, e, text) in enumerate(SUBS, 1):
    rows_s.append(f'    <div id="sb{i:02d}" class="cap clip" data-start="{s}" data-duration="{round(e - s, 2)}" data-track-index="0">'
                  f'<div class="line">{mark(text)}</div></div>')
    js_s.append(f'    tl.fromTo("#sb{i:02d} .line", {{ opacity:0, y:8 }}, {{ opacity:1, y:0, duration:0.15, ease:"power1.out" }}, {s});')
scene("subs", SCENES["subs"][1], f"""
    .cap {{ position:absolute; left:60px; right:162px; top:1180px; height:150px; display:flex; align-items:flex-end; justify-content:center; }}
    .line {{ max-width:858px; text-align:center; color:#FFFFFF; font-weight:700; font-size:44px; line-height:1.22;
      text-shadow:0 3px 12px rgba(0,0,0,.8), 0 1px 3px rgba(0,0,0,.8); }}
    .k {{ color:{Y}; }}""", "\n".join(rows_s), "\n".join(js_s))

print("total", TOTAL, "living zoom origin", ox, oy)
