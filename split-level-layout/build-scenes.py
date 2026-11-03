#!/usr/bin/env python3
# Builds every scene, the caption track and index.html for the split-level floor plan video.
# Run from the project folder:  python3 build-scenes.py .
# Timing follows the voiceover transcript in assets/audio/transcript.json.
import difflib, json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(f"{OUT}/compositions", exist_ok=True)

AMB = "#F59E0B"     # accent: room highlights, routes
YEL = "#F6C343"     # title yellow (white + yellow titles, like the reference)
RED = "#E5484D"     # the issue
TEAL = "#14B8A6"    # hypothetical suggestion only
INK = "#16181D"

# Floor plan coordinates are in the cleaned plan images (plan-upper-hd.png 2200x1800, plan-ground-hd.png 2200x2040).
PLAN = {"upper": (2200, 1800), "ground": (2200, 2040)}
U = {  # upper floor rooms (x1, y1, x2, y2)
    "br2": (1232, 473, 1556, 737), "bath1": (1743, 473, 1903, 676), "master": (1567, 676, 1903, 1171),
    "family": (1232, 748, 1562, 1061), "stair": (1138, 737, 1226, 869),
}
G = {  # ground floor
    "stair": (839, 569, 1104, 668), "toilet": (613, 309, 768, 420), "kitchen": (911, 309, 1160, 552),
}
ctr = lambda r: ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
ROUTE_BATH = "1394,640 1500,700 1524,772 1600,800 1700,760 1790,700 1812,600"
ROUTE_STAIR_U = "1394,640 1500,700 1524,776 1320,792 1196,803"
ROUTE_GROUND = "960,618 820,640 745,560 712,440 690,368"

SCENES = [("s01", 0, 3.6), ("s02", 3.6, 5.0), ("s03", 8.6, 6.4), ("s04", 15.0, 3.8), ("s05", 18.8, 3.9),
          ("s06", 22.7, 3.05), ("s07", 25.75, 4.55), ("s08", 30.3, 5.1), ("s09", 35.4, 4.8), ("s10", 40.2, 6.3),
          ("s11", 46.5, 6.9), ("s12", 53.4, 9.6), ("s13", 63.0, 7.55), ("s14", 70.55, 3.15), ("s15", 73.7, 5.0)]
START = {c: s for c, s, d in SCENES}
TOTAL = round(SCENES[-1][1] + SCENES[-1][2], 2)

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #FFFFFF; font-family: Montserrat, sans-serif; color: #fff; }}
    #root .paper {{ position: absolute; inset: 0; background: #FFFFFF;
      background-image: linear-gradient(rgba(22,24,29,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(22,24,29,.05) 1px, transparent 1px);
      background-size: 54px 54px; }}
    #root .plan {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
    #root .plan img {{ position: absolute; left: 0; top: 0; display: block; }}
    #root .plan svg {{ position: absolute; left: 0; top: 0; overflow: visible; }}
    #root .card {{ position: absolute; left: 40px; right: 40px; padding: 0; background: transparent; border-radius: 0;
      text-shadow: 0 4px 0 rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.7), 0 0 3px rgba(0,0,0,.85);
      text-align: center; font-weight: 900; font-size: 74px; line-height: 1.06; text-transform: uppercase; color: #fff; }}
    #root .card .a {{ color: {YEL}; }}
    #root .tshade {{ position: absolute; left: 0; top: 0; width: 1080px; height: 900px; z-index: 2;
      background: linear-gradient(rgba(10,12,16,.9) 0px, rgba(10,12,16,.72) 420px, rgba(10,12,16,0) 880px); }}
    #root .card, #root .kick, #root .chip, #root .opt, #root .row, #root #s14-cm {{ z-index: 3; }}
    #root .card .r {{ color: #FF6B6F; }}
    #root .kick {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; }}
    #root .kick span {{ padding: 10px 22px; background: {YEL}; color: {INK}; font-weight: 900; font-size: 32px; letter-spacing: .14em;
      text-transform: uppercase; border-radius: 8px; }}
    #root .chip {{ position: absolute; padding: 12px 22px; background: {INK}; color: #fff; font-weight: 800; font-size: 34px;
      letter-spacing: .06em; text-transform: uppercase; border-radius: 10px; white-space: nowrap; box-shadow: 0 10px 26px rgba(0,0,0,.25); }}
    #root .chip i {{ display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: {AMB}; margin-right: 12px; vertical-align: 2px; font-style: normal; }}
    #root .inset {{ position: absolute; width: 400px; height: 520px; border-radius: 26px; overflow: hidden; border: 6px solid #fff;
      box-shadow: 0 24px 60px rgba(0,0,0,.35); background: {INK}; }}
    #root .inset video {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    #root .inset .tagv {{ position: absolute; left: 14px; bottom: 14px; padding: 8px 14px; background: rgba(22,24,29,.85); color: #fff;
      font-weight: 800; font-size: 28px; letter-spacing: .08em; border-radius: 8px; text-transform: uppercase; }}
    #root .photo {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
    #root .photo img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; transform-origin: 50% 60%; }}
    #root video.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    #root .dim {{ position: absolute; inset: 0; background: rgba(12,14,18,.5); }}
    #root .topshade {{ position: absolute; left: 0; right: 0; top: 0; height: 760px; background: linear-gradient(rgba(12,14,18,.75), rgba(12,14,18,0)); }}
"""

HELPERS = """
    const F = (s, px, py, cx, cy) => ({ x: cx - px * s, y: cy - py * s, scale: s });
    const tl = gsap.timeline({ paused: true });
"""


def scene(cid, css, body, js):
    dur = next(d for c, s, d in SCENES if c == cid)
    with open(f"{OUT}/compositions/{cid}.html", "w") as f:
        f.write(f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{dur}">
    <div class="paper"></div>
{'' if cid == 's15' else '<div class="tshade"></div>'}
{body}
  </div>
  <script>{HELPERS}{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")


def hl(id_, r, color=AMB, dashed=False):
    x1, y1, x2, y2 = r
    dash = ' stroke-dasharray="14 10"' if dashed else ""
    return (f'<g id="{id_}"><rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="none" stroke="{color}" stroke-opacity=".35" stroke-width="16" vector-effect="non-scaling-stroke" />'
            f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="{color}" fill-opacity=".2" stroke="{color}" stroke-width="5"{dash} vector-effect="non-scaling-stroke" /></g>')


def route(id_, pts, color=AMB):
    last = pts.split()[-1].split(",")
    return (f'<polyline id="{id_}" points="{pts}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 2" stroke-dashoffset="1.05" vector-effect="non-scaling-stroke" />'
            f'<circle id="{id_}-end" cx="{last[0]}" cy="{last[1]}" r="16" fill="{color}" stroke="#fff" stroke-width="5" vector-effect="non-scaling-stroke" />')


def plan(id_, which, overlay=""):
    w, h = PLAN[which]
    return f"""    <div class="plan" id="{id_}" style="width:{w}px; height:{h}px">
      <img src="assets/plan-{which}-hd.png" alt="" style="width:{w}px; height:{h}px" />
      <svg viewBox="0 0 {w} {h}" style="width:{w}px; height:{h}px">{overlay}</svg>
    </div>"""


def inset(id_, src, start, dur, mstart, left, top, label="Foto sebenar"):
    return f"""    <div class="inset" id="{id_}" style="left:{left}px; top:{top}px" data-layout-allow-overlap>
      <video id="{id_}-v" class="clip" src="assets/video/{src}.mp4" data-start="{start}" data-duration="{dur}" data-media-start="{mstart}" muted playsinline></video>
      <div class="tagv">{label}</div>
    </div>"""


def photo(id_, src, label):
    return f"""    <div class="photo" id="{id_}"><img src="assets/{src}" alt="" /><div class="chip" style="left:50px; top:1060px"><i></i>{label}</div></div>"""


def photo_in(id_, t, end):
    return (f'    tl.fromTo("#{id_}", {{ opacity: 1, clipPath: "inset(100% 0% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut" }}, {t});\n'
            f'    tl.fromTo("#{id_} img", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {round(end - t, 2)}, ease: "sine.out" }}, {t});\n')


def pop(sel, t, dur=0.4):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, y: 24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: {dur}, ease: "back.out(1.6)" }}, {t});\n'


def out(sel, t, dur=0.25):
    return f'    tl.to("{sel}", {{ opacity: 0, duration: {dur} }}, {t});\n'


def F(s, p, c):
    return f"F({s}, {p[0]}, {p[1]}, {c[0]}, {c[1]})"


# ---------------------------------------------------------------- S01 COMMENT HOOK
scene("s01", """
    #s01-card { position: absolute; left: 40px; top: 640px; width: 1000px; height: 400px; border-radius: 28px; overflow: hidden;
      background: #fff; box-shadow: 0 30px 80px rgba(0,0,0,.45); }
    #s01-img { position: absolute; left: 0; top: 0; width: 1177px; height: 362px; transform-origin: 0 0; }
    #s01-img img { position: absolute; left: 0; top: 0; width: 1177px; height: 362px; }
    #s01-img .mk { position: absolute; background: rgba(245,158,11,.45); mix-blend-mode: multiply; transform-origin: 0 50%; border-radius: 6px; }
""", f"""    <video id="s01-bg" class="clip full" src="assets/video/shower.mp4" data-start="0" data-duration="3.6" data-media-start="1.0" muted playsinline></video>
    <div class="dim"></div>
    <div class="card" id="s01-head" style="top:200px; font-size:76px">Nak mandi pun<br /><span class="a">kena turun bawah?</span></div>
    <div id="s01-card">
      <div id="s01-img">
        <img src="assets/comment.jpg" alt="" />
        <div class="mk" id="s01-m1" style="left:362px; top:88px; width:752px; height:54px"></div>
        <div class="mk" id="s01-m2" style="left:440px; top:160px; width:576px; height:54px"></div>
        <div class="mk" id="s01-m3" style="left:162px; top:229px; width:132px; height:54px"></div>
      </div>
    </div>""", """
    tl.fromTo("#s01-img", F(0.84, 588, 181, 500, 200), { ...F(1.0, 640, 160, 500, 200), duration: 0.7, ease: "power3.inOut" }, 0.35);
    tl.to("#s01-img", { ...F(1.01, 640, 200, 500, 200), duration: 0.8, ease: "power3.inOut" }, 1.7);
    tl.fromTo("#s01-card", { opacity: 0, y: 60, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.5)" }, 0);
    tl.fromTo("#s01-head", { scale: 1.08 }, { scale: 1, duration: 0.5, ease: "power3.out" }, 0);
    tl.fromTo("#s01-m1", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, 0.8);
    tl.fromTo("#s01-m2", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.inOut" }, 2.15);
    tl.fromTo("#s01-m3", { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power2.inOut" }, 2.6);
""")

# ---------------------------------------------------------------- S02 INTRO
RB = (1515, 820)  # upper rooms block centre
scene("s02", """
    #s02-ft { position: absolute; inset: 0; }
    #s02-plan-wrap { position: absolute; inset: 0; }
""", f"""    <div id="s02-plan-wrap">
{plan("s02-plan", "upper", hl("s02-rooms", (1120, 425, 1912, 1175)))}
    </div>
    <div id="s02-ft"><video id="s02-v" class="clip full" src="assets/video/stairs-up.mp4" data-start="0" data-duration="2.3" data-media-start="2.0" muted playsinline></video><div class="topshade"></div></div>
    <div class="kick" id="s02-k" style="top:200px"><span>Kemaman, Terengganu</span></div>
    <div class="card" id="s02-head" style="top:276px">Rumah <span class="a">split level</span></div>
    <div class="chip" id="s02-chip" style="left:290px; top:470px"><i></i>Jom tengok layout sebenar</div>""", f"""
    tl.fromTo("#s02-ft", {{ clipPath: "inset(0% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.6, ease: "power3.inOut" }}, 2.1);
    tl.fromTo("#s02-plan", {F(1.0, RB, (540, 1000))}, {{ ...{F(1.3, (1560, 820), (540, 960))}, duration: 2.9, ease: "power2.out" }}, 2.1);
    tl.fromTo("#s02-plan-wrap", {{ scale: 1.08 }}, {{ scale: 1, duration: 0.8, ease: "power3.out" }}, 2.1);
{pop("#s02-k", 0.1)}{pop("#s02-head", 0.25)}
    tl.fromTo("#s02-rooms", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 3.0);
{pop("#s02-chip", 3.2)}
""")

# ---------------------------------------------------------------- S03 UPPER FLOOR ROOMS
ROOMS3 = [("master", "Master bedroom", "master", 2.05, 1.85, (390, 840)),
          ("br2", "Bilik anak", "bedroom2-beds", 3.85, 2.3, (390, 820)),
          ("family", "Ruang keluarga", "family", 5.0, 2.0, (390, 840))]
ov3 = "".join(hl(f"s03-h-{k}", U[k]) for k, *_ in ROOMS3)
body3 = plan("s03-plan", "upper", ov3) + "\n" + photo("s03-ph", "photo-family.jpg", "Ruang keluarga · foto sebenar") + "\n"
body3 += '    <div class="kick" id="s03-k" style="top:200px"><span>Tingkat atas</span></div>\n'
js3 = f"""
    tl.fromTo("#s03-plan", {F(1.3, (1560, 820), (540, 960))}, {{ ...{F(1.2, RB, (540, 900))}, duration: 1.8, ease: "sine.inOut" }}, 0);
{pop("#s03-k", 0.1)}"""
for i, (k, name, vid, t, s, c) in enumerate(ROOMS3):
    body3 += f'    <div class="card" id="s03-n-{k}" style="top:276px; font-size:60px"><span class="a">{i+1}</span> · {name}</div>\n'
    end = ROOMS3[i + 1][3] if i + 1 < len(ROOMS3) else 6.4
    body3 += inset(f"s03-in-{k}", vid, t, round(end - t, 2), 0.8, 640, 620) + "\n"
    js3 += f"""    tl.to("#s03-plan", {{ ...{F(s, ctr(U[k]), c)}, duration: 0.55, ease: "expo.out" }}, {t - 0.15});
    tl.fromTo("#s03-h-{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {t});
    tl.fromTo("#s03-h-{k} rect:last-child", {{ fillOpacity: 0.45 }}, {{ fillOpacity: 0.2, duration: 0.6 }}, {t});
{pop(f"#s03-n-{k}", t)}{pop(f"#s03-in-{k}", t + 0.1)}"""
    if i + 1 < len(ROOMS3):
        js3 += out(f"#s03-n-{k}", end - 0.12, 0.12) + out(f"#s03-in-{k}", end - 0.12, 0.12) + f'    tl.to("#s03-h-{k}", {{ opacity: 0.35, duration: 0.3 }}, {end});\n'
js3 += photo_in("s03-ph", 5.3, 6.4)
js3 += out("#s03-in-family", 5.3, 0.2)
scene("s03", """
    #s03-n-master, #s03-n-br2, #s03-n-family, #s03-in-master, #s03-in-br2, #s03-in-family { opacity: 0; }
""", body3, js3)

# ---------------------------------------------------------------- S04 BEDROOM 2: NO OWN BATHROOM
scene("s04", """
    #s04-x { opacity: 0; }
""", f"""{plan("s04-plan", "upper", hl("s04-h", U["br2"], RED) + f'<g id="s04-x" transform="translate(1394 605)"><circle r="46" fill="{RED}" /><path d="M-18 -18 L18 18 M18 -18 L-18 18" stroke="#fff" stroke-width="9" stroke-linecap="round" /></g>' + hl("s04-b", U["bath1"]))}
    <div class="kick" id="s04-k" style="top:200px"><span>Bedroom 2</span></div>
    <div class="card" id="s04-head" style="top:276px">Tiada <span class="r">bilik air</span><br />sendiri</div>""", f"""
    tl.fromTo("#s04-plan", {F(1.9, ctr(U["br2"]), (540, 880))}, {{ ...{F(2.6, ctr(U["br2"]), (540, 880))}, duration: 0.5, ease: "expo.out" }}, 0);
    tl.to("#s04-plan", {{ ...{F(1.75, (1610, 610), (540, 880))}, duration: 0.9, ease: "power2.inOut" }}, 2.6);
    tl.fromTo("#s04-h", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.3);
    tl.fromTo("#s04-x", {{ opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, 1.5);
    tl.fromTo("#s04-b", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.4 }}, 3.0);
{pop("#s04-k", 0.15)}{pop("#s04-head", 1.4)}""")

# ---------------------------------------------------------------- S05 QUESTION
scene("s05", "", f"""{plan("s05-plan", "upper", hl("s05-h", U["br2"], RED) + hl("s05-st", U["stair"]) + route("s05-r", ROUTE_STAIR_U, RED))}
    <div class="card" id="s05-head" style="top:250px; font-size:96px; ">Betul ke<br /><span class="a">kena turun</span><br />bawah?</div>""", f"""
    tl.fromTo("#s05-plan", {F(1.75, (1500, 680), (540, 1000))}, {{ ...{F(1.95, (1420, 690), (540, 1010))}, duration: 3.9, ease: "sine.inOut" }}, 0);
    tl.to("#s05-r", {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }}, 0.5);
    tl.fromTo("#s05-r-end", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 1.35);
{pop("#s05-head", 0.1, 0.5)}""")

# ---------------------------------------------------------------- S06 ANSWER: BATH 1 UPSTAIRS
scene("s06", "", f"""{plan("s06-plan", "upper", hl("s06-h", U["bath1"]) + route("s06-r", ROUTE_BATH))}
    <div class="card" id="s06-head" style="top:230px">Tak semestinya!</div>
    <div class="card" id="s06-sub" style="top:390px; font-size:46px; color:{YEL}">✓ Masih ada bilik air di tingkat atas</div>
    <div class="chip" id="s06-lab" style="left:760px; top:640px"><i></i>Bath 1</div>""", f"""
    tl.fromTo("#s06-plan", {F(1.6, (1560, 640), (540, 900))}, {{ ...{F(2.0, (1600, 640), (540, 900))}, duration: 3.05, ease: "sine.inOut" }}, 0);
    tl.to("#s06-r", {{ strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }}, 0.4);
    tl.fromTo("#s06-r-end", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 1.55);
    tl.fromTo("#s06-h", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 1.5);
    tl.fromTo("#s06-h rect:last-child", {{ fillOpacity: 0.55 }}, {{ fillOpacity: 0.2, duration: 0.5, repeat: 2, yoyo: true }}, 1.6);
{pop("#s06-head", 0.05)}{pop("#s06-sub", 1.0)}{pop("#s06-lab", 1.7)}""")

# ---------------------------------------------------------------- S07 MASTER + BATH 1
scene("s07", """
    #s07-head2 { opacity: 0; }
""", f"""{plan("s07-plan", "upper", hl("s07-hm", U["master"]) + hl("s07-hb", U["bath1"]))}
    <svg class="ptr" style="position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible" viewBox="0 0 1080 1920">
      <polyline id="s07-ptr" points="700,470 840,470 840,620" fill="none" stroke="{INK}" stroke-width="4" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />
      <circle id="s07-dot" cx="840" cy="620" r="12" fill="{AMB}" stroke="{INK}" stroke-width="4" />
    </svg>
    <div class="card" id="s07-head" style="top:200px; font-size:54px">Bilik air dalam<br /><span class="a">master bedroom</span></div>
    <div class="chip" id="s07-lab" style="left:290px; top:440px"><i></i>Boleh dikongsi</div>
""" + "\n" + photo("s07-p1", "photo-master.jpg", "Master bedroom · foto sebenar") + "\n" + photo("s07-p2", "photo-bath.jpg", "Bilik air (Bath 1) · foto sebenar") + f"""
    <div class="card" id="s07-head2" style="top:200px; font-size:58px">Bilik air dalam<br /><span class="a">master bedroom</span></div>""", f"""
    tl.fromTo("#s07-plan", {F(1.9, (1700, 760), (700, 980))}, {{ ...{F(1.75, (1690, 800), (720, 1000))}, duration: 4.55, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s07-hm", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.2);
    tl.fromTo("#s07-hb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.45);
    tl.to("#s07-ptr", {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut" }}, 0.7);
    tl.fromTo("#s07-dot", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 1.1);
{pop("#s07-head", 0.05)}{pop("#s07-lab", 0.5)}
{photo_in("s07-p1", 1.2, 2.9)}{photo_in("s07-p2", 2.9, 4.55)}
    tl.fromTo("#s07-head2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.4);
    tl.to("#s07-head", {{ opacity: 0, duration: 0.15 }}, 1.4);
    tl.to("#s07-lab", {{ opacity: 0, duration: 0.15 }}, 1.2);
""")

# ---------------------------------------------------------------- S08 GROUND FLOOR OPTION
scene("s08", """
    #s08-ft { position: absolute; inset: 0; opacity: 0; }
    #s08-g { position: absolute; inset: 0; opacity: 0; }
    #s08-head, #s08-lab, #s08-down { opacity: 0; }
    #s08-down { position: absolute; left: 470px; top: 760px; width: 140px; height: 140px; border-radius: 50%; background: """ + AMB + """;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 14px 40px rgba(0,0,0,.3); }
""", f"""    <div id="s08-u">
{plan("s08-up", "upper", hl("s08-hs", U["stair"]))}
    </div>
    <div id="s08-down"><svg width="70" height="80" viewBox="0 0 70 80"><path d="M35 6 V70 M10 46 L35 72 L60 46" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg></div>
    <div id="s08-ft"><video id="s08-v" class="clip full" src="assets/video/stairs-down.mp4" data-start="0.9" data-duration="1.4" data-media-start="1.0" muted playsinline></video><div class="topshade"></div></div>
    <div id="s08-g">
{plan("s08-gp", "ground", hl("s08-gs", G["stair"]) + hl("s08-gt", G["toilet"]) + route("s08-r", ROUTE_GROUND))}
    </div>
    <div class="kick" id="s08-k" style="top:200px"><span>Tingkat bawah</span></div>
    <div class="card" id="s08-head" style="top:276px">Option untuk<br /><span class="a">lebih privasi</span></div>
    <div class="chip" id="s08-lab" style="left:120px; top:560px"><i></i>Toilet bawah</div>""", f"""
    tl.fromTo("#s08-up", {F(1.9, (1300, 790), (540, 900))}, {{ ...{F(3.0, ctr(U["stair"]), (540, 900))}, duration: 0.9, ease: "power3.in" }}, 0);
    tl.fromTo("#s08-hs", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.1);
    tl.fromTo("#s08-down", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 30, duration: 0.6, ease: "power2.in" }}, 0.2);
    tl.to("#s08-down", {{ opacity: 0, duration: 0.15 }}, 0.85);
    tl.fromTo("#s08-ft", {{ opacity: 0, clipPath: "inset(0% 0% 100% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power3.out" }}, 0.9);
    tl.fromTo("#s08-g", {{ clipPath: "inset(0% 0% 100% 0%)", opacity: 1 }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut" }}, 2.2);
    tl.fromTo("#s08-gp", {F(2.4, ctr(G["stair"]), (540, 920))}, {{ ...{F(1.75, (830, 500), (560, 930))}, duration: 1.2, ease: "power2.inOut" }}, 2.2);
    tl.fromTo("#s08-gs", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 2.4);
    tl.to("#s08-r", {{ strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }}, 3.1);
    tl.fromTo("#s08-r-end", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 4.05);
    tl.fromTo("#s08-gt", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 4.0);
{pop("#s08-k", 2.4)}{pop("#s08-head", 2.55)}{pop("#s08-lab", 4.1)}""")

# ---------------------------------------------------------------- S09 BUILD ON YOUR OWN LAND
scene("s09", """
    #s09-ft { position: absolute; inset: 0; }
    #s09-g, #s09-u { position: absolute; inset: 0; }
    #s09-u { opacity: 0; }
    #s09-h2 { opacity: 0; }
""", f"""    <div id="s09-g">
{plan("s09-gp", "ground")}
    </div>
    <div id="s09-u">
{plan("s09-up", "upper")}
    </div>
    <div id="s09-ft"><video id="s09-v" class="clip full" src="assets/video/living-door.mp4" data-start="0" data-duration="1.9" data-media-start="1.5" muted playsinline></video><div class="topshade"></div></div>
    <div class="card" id="s09-h1" style="top:230px">Bina rumah atas<br /><span class="a">tanah sendiri</span></div>
    <div class="card" id="s09-h2" style="top:430px; font-size:46px; color:{YEL}">Layout boleh dirancang ikut keperluan</div>""", f"""
    tl.fromTo("#s09-ft", {{ clipPath: "inset(0% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 100% 0% 0%)", duration: 0.55, ease: "power3.inOut" }}, 1.7);
    tl.fromTo("#s09-gp", {F(1.05, (700, 700), (540, 1080))}, {{ ...{F(1.05, (1250, 700), (540, 1080))}, duration: 1.8, ease: "sine.inOut" }}, 1.7);
    tl.fromTo("#s09-u", {{ opacity: 1, clipPath: "inset(100% 0% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }}, 3.3);
    tl.fromTo("#s09-up", {F(1.2, (1450, 800), (540, 1100))}, {{ ...{F(1.3, (1520, 800), (540, 1080))}, duration: 1.5, ease: "sine.inOut" }}, 3.3);
{pop("#s09-h1", 0.15)}{pop("#s09-h2", 2.3)}""")

# ---------------------------------------------------------------- S10 FLEXIBILITY: HYPOTHETICAL EXTRA BATH
scene("s10", f"""
    #s10-hy, #s10-badge {{ opacity: 0; }}
    #s10-badge {{ position: absolute; left: 140px; top: 600px; padding: 18px 28px; background: #fff; border: 4px dashed {TEAL}; border-radius: 18px;
      color: {INK}; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,.2); }}
    #s10-badge b {{ display: block; font-weight: 900; font-size: 54px; color: {TEAL}; }}
    #s10-badge small {{ display: block; margin-top: 4px; font-weight: 700; font-size: 28px; letter-spacing: .12em; text-transform: uppercase; color: #5B616B; }}
""", f"""{plan("s10-plan", "upper", hl("s10-h", U["br2"]) + f'<g id="s10-hy">' + hl("s10-hyr", (1238, 479, 1550, 731), TEAL, True) + '</g>')}
    <div class="card" id="s10-head" style="top:220px">Rancang ikut<br /><span class="a">keperluan keluarga</span></div>
    <div id="s10-badge"><b>+ Bilik air?</b><small>Cadangan sahaja</small></div>
{inset("s10-in", "bedroom2-door", 2.4, 3.9, 1.0, 640, 640, "Bedroom 2")}""", f"""
    tl.fromTo("#s10-plan", {F(2.0, ctr(U["br2"]), (400, 900))}, {{ ...{F(2.5, ctr(U["br2"]), (420, 920))}, duration: 6.3, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s10-h", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.3);
    tl.to("#s10-h", {{ opacity: 0, duration: 0.3 }}, 1.6);
    tl.fromTo("#s10-hy", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, 1.6);
{pop("#s10-head", 0.1)}{pop("#s10-badge", 1.8, 0.5)}{pop("#s10-in", 2.4)}""")

# ---------------------------------------------------------------- S11 EVERY FAMILY IS DIFFERENT
scene("s11", "#s11-l2 { opacity: 0; }", f"""{plan("s11-plan", "upper")}
    <div class="card" id="s11-l1" style="top:260px; font-size:80px">Setiap keluarga,</div>
    <div class="card" id="s11-l2" style="top:400px; font-size:80px; color:{YEL}">keperluan berbeza.</div>""", f"""
    tl.fromTo("#s11-plan", {F(1.15, (900, 820), (540, 1060))}, {{ ...{F(1.2, (1520, 820), (540, 1060))}, duration: 6.9, ease: "sine.inOut" }}, 0);
{pop("#s11-l1", 0.2, 0.5)}{pop("#s11-l2", 3.85, 0.5)}""")

# ---------------------------------------------------------------- S12 PERSPECTIVE
scene("s12", "#s12-h2 { opacity: 0; } #s12-g, #s12-u { position: absolute; inset: 0; } #s12-u { opacity: 0; } #s12-ft { position: absolute; inset: 0; }", f"""    <div id="s12-g">
{plan("s12-gp", "ground")}
    </div>
    <div id="s12-u">
{plan("s12-up", "upper")}
    </div>
    <div id="s12-ft"><video id="s12-v" class="clip full" src="assets/video/room-walk.mp4" data-start="0" data-duration="3.2" data-media-start="0.5" muted playsinline></video><div class="topshade"></div></div>
    <div class="card" id="s12-h1" style="top:230px; font-size:56px">Kita nilai ikut<br /><span class="a">cara hidup kita</span></div>
    <div class="card" id="s12-h2" style="top:230px; font-size:68px">Design yang baik<br /><span class="a">tak semestinya sama</span><br />untuk semua.</div>""", f"""
    tl.fromTo("#s12-ft", {{ clipPath: "inset(0% 0% 0% 0%)" }}, {{ clipPath: "inset(100% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }}, 3.0);
    tl.fromTo("#s12-gp", {F(2.0, (600, 450), (540, 1000))}, {{ ...{F(2.0, (1000, 520), (540, 1000))}, duration: 2.8, ease: "sine.inOut" }}, 3.0);
    tl.fromTo("#s12-u", {{ opacity: 1, clipPath: "inset(0% 0% 0% 100%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }}, 5.6);
    tl.fromTo("#s12-up", {F(1.35, (1520, 820), (540, 1150))}, {{ ...{F(1.15, (1460, 820), (540, 1120))}, duration: 4.0, ease: "sine.inOut" }}, 5.6);
{pop("#s12-h1", 0.4)}{out("#s12-h1", 5.4)}{pop("#s12-h2", 5.75, 0.5)}""")

# ---------------------------------------------------------------- S13 CTA OPTIONS
scene("s13", f"""
    #root .opt {{ position: absolute; left: 60px; right: 60px; height: 230px; border-radius: 26px; display: flex; align-items: center; gap: 30px;
      padding: 0 40px; background: #fff; color: {INK}; box-shadow: 0 24px 60px rgba(0,0,0,.35); opacity: 0; }}
    #root .opt .l {{ flex: none; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: 74px; color: #fff; }}
    #root .opt .t {{ font-weight: 900; font-size: 62px; line-height: 1.02; text-transform: uppercase; }}
""", f"""{plan("s13-plan", "upper")}
    <div class="dim" style="background:rgba(14,16,20,.82)"></div>
    <div class="card" id="s13-head" style="top:230px; font-size:76px">Kalau korang<br /><span class="a">yang design?</span></div>
    <div class="opt" id="s13-a" style="top:560px"><div class="l" style="background:{TEAL}">A</div><div class="t">Tambah<br />bilik air</div></div>
    <div class="opt" id="s13-b" style="top:830px"><div class="l" style="background:{AMB}">B</div><div class="t">Kekalkan<br />layout</div></div>""", f"""
    tl.fromTo("#s13-plan", {F(1.15, RB, (540, 1000))}, {{ ...{F(1.3, RB, (540, 1000))}, duration: 7.55, ease: "sine.inOut" }}, 0);
{pop("#s13-head", 0.1, 0.5)}
    tl.fromTo("#s13-a", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }}, 3.1);
    tl.fromTo("#s13-b", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }}, 5.7);
    tl.fromTo("#s13-a", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.3, yoyo: true, repeat: 1 }}, 3.6);
    tl.fromTo("#s13-b", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.3, yoyo: true, repeat: 1 }}, 6.2);
""")

# ---------------------------------------------------------------- S14 FINAL CTA
scene("s14", f"""
    #root .row {{ position: absolute; left: 90px; right: 90px; height: 120px; border-radius: 18px; display: flex; align-items: center; gap: 24px;
      padding: 0 30px; background: #fff; color: {INK}; font-weight: 900; font-size: 48px; text-transform: uppercase; }}
    #root .row b {{ flex: none; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 46px; }}
    #s14-cm {{ position: absolute; left: 0; right: 0; top: 920px; display: flex; flex-direction: column; align-items: center; gap: 12px; }}
    #s14-cm span {{ padding: 16px 44px; background: {AMB}; color: {INK}; font-weight: 900; font-size: 64px; border-radius: 16px; letter-spacing: .06em; }}
""", f"""{plan("s14-plan", "upper")}
    <div class="dim" style="background:rgba(14,16,20,.84)"></div>
    <div class="card" id="s14-head" style="top:220px; font-size:84px">Korang pilih<br /><span class="a">yang mana?</span></div>
    <div class="row" id="s14-a" style="top:520px"><b style="background:{TEAL}">A</b>Tambah bilik air</div>
    <div class="row" id="s14-b" style="top:665px"><b style="background:{AMB}">B</b>Kekalkan layout</div>
    <div id="s14-cm"><span id="s14-k">Komen</span><svg id="s14-arrow" width="64" height="80" viewBox="0 0 64 80"><path d="M32 4 V66 M8 44 L32 68 L56 44" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" /></svg></div>""", f"""
    tl.fromTo("#s14-plan", {F(1.3, RB, (540, 1000))}, {{ ...{F(1.38, RB, (540, 1000))}, duration: 3.15, ease: "sine.inOut" }}, 0);
{pop("#s14-head", 0.0, 0.45)}{pop("#s14-a", 0.25)}{pop("#s14-b", 0.4)}{pop("#s14-k", 0.6, 0.45)}
    tl.fromTo("#s14-arrow", {{ y: 0 }}, {{ y: 16, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 5 }}, 0.9);
""")

# ---------------------------------------------------------------- S15 OUTRO (company card, same as the previous video)
scene("s15", f"""
    #s15-img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 55%; }}
    #s15-img img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }}
    #root .ring {{ position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; border: 5px solid #F6C343; opacity: 0; }}
    #s15-shine {{ position: absolute; left: 30px; top: 1180px; width: 1020px; height: 420px; overflow: hidden; }}
    #s15-band {{ position: absolute; left: 0; top: 0; width: 220px; height: 420px;
      background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.38) 50%, rgba(255,255,255,0)); }}
    #s15-glow {{ position: absolute; left: 86px; top: 1440px; width: 908px; height: 132px; border-radius: 30px; border: 4px solid #F6C343;
      box-shadow: 0 0 40px rgba(246,195,67,.75); opacity: 0; }}
    #s15-fade {{ position: absolute; inset: 0; background: #0B0F16; }}
""", """    <div id="s15-img"><img src="assets/outro.jpg" alt="" /></div>
    <div class="ring" id="s15-r1" style="left:477px; top:888px"></div>
    <div class="ring" id="s15-r2" style="left:744px; top:1002px"></div>
    <div id="s15-shine"><div id="s15-band"></div></div>
    <div id="s15-glow"></div>
    <div id="s15-fade"></div>""", """
    tl.fromTo("#s15-fade", { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power2.out" }, 0);
    tl.fromTo("#s15-img", { scale: 1.14 }, { scale: 1.0, duration: 1.1, ease: "expo.out" }, 0);
    tl.to("#s15-img", { scale: 1.03, duration: 3.9, ease: "sine.inOut" }, 1.1);
    ["#s15-r1", "#s15-r2"].forEach((r, i) => {
      tl.fromTo(r, { opacity: 0.95, scale: 0.3 }, { opacity: 0, scale: 2.1, duration: 1.0, ease: "power2.out", repeat: 2 }, 0.7 + i * 0.25);
    });
    tl.fromTo("#s15-band", { x: -240 }, { x: 1060, duration: 1.1, ease: "sine.inOut" }, 1.0);
    tl.fromTo("#s15-glow", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }, 1.6);
""")

# ---------------------------------------------------------------- CAPTIONS synced to the voiceover
SCRIPT = """Nak mandi pun kena turun bawah guna tandas dapur?
Haa, ada yang komen pasal layout rumah split level dekat Kemaman ni!
Sebab dekat bahagian atas, ada satu master bedroom, satu bilik anak dan satu ruang keluarga.
Tapi bilik anak tu tak ada tandas sendiri.
Jadi, betul ke kalau nak mandi kena turun bawah?
Sebenarnya, tak semestinya pun!
Sebab dekat master bedroom tu dah ada bilik air yang boleh digunakan.
Cuma, kalau nak lebih privasi, memang kena turun ke bilik air bawah.
Tapi inilah yang menarik bila kita bina rumah atas tanah sendiri.
Kita boleh rancang susun atur mengikut keperluan dan keselesaan keluarga masing-masing.
Sebab apa yang praktikal untuk satu keluarga, tak semestinya sama untuk keluarga yang lain.
Kadang-kadang kita nilai layout rumah orang berdasarkan cara hidup kita, sedangkan rumah tu direka untuk keperluan pemiliknya.
Jadi, kalau korang yang design rumah ni, korang akan tambah bilik air dekat atas atau kekalkan layout macam ni?
Cuba komen!"""
HIGHLIGHT = {"mandi", "turun", "bawah", "tandas", "split", "level", "kemaman", "master", "bedroom", "bilik", "anak", "air",
             "privasi", "tanah", "sendiri", "keperluan", "berbeza", "tambah", "kekalkan", "komen", "layout"}

tr = json.load(open(f"{OUT}/assets/audio/transcript.json"))
ww = tr if isinstance(tr, list) else tr.get("words", tr)
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
sw = SCRIPT.split()
a, b = [norm(x) for x in sw], [norm(x["text"]) for x in ww]
times = [None] * len(sw)
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if op == "equal":
        for k in range(i2 - i1):
            times[i1 + k] = (ww[j1 + k]["start"], ww[j1 + k]["end"])
    elif op == "replace":
        s0, e0 = ww[j1]["start"], ww[j2 - 1]["end"]
        n = i2 - i1
        for k in range(n):
            times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
for i in range(len(times)):
    if times[i] is None:
        p = times[i - 1][1] if i else 0
        times[i] = (p, p + 0.2)
chunks, cur = [], []
for i, w in enumerate(sw):
    cur.append(i)
    if w[-1] in ".,!?" or len(cur) == 4:
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
caps = []
for n, ch in enumerate(chunks):
    st = max(0.0, times[ch[0]][0] - 0.06)
    en = times[ch[-1]][1] + 0.25
    if n + 1 < len(chunks):
        nxt = times[chunks[n + 1][0]][0] - 0.06
        en = nxt if nxt - times[ch[-1]][1] < 0.7 else en
    words = " ".join(f'<span class="y">{sw[i]}</span>' if norm(sw[i]) in HIGHLIGHT else sw[i] for i in ch)
    caps.append((round(st, 2), round(max(0.3, en - st), 2), words))
cap_html = "\n".join(
    f'    <div class="cap clip" id="cap-{i:02d}" data-start="{s}" data-duration="{d}"><span class="pill">{t}</span></div>'
    for i, (s, d, t) in enumerate(caps, 1))
cap_js = "\n".join(
    f'    tl.fromTo("#cap-{i:02d} .pill", {{ opacity: 0, scale: 0.86, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "back.out(2)" }}, {s});'
    for i, (s, d, t) in enumerate(caps, 1))
with open(f"{OUT}/compositions/captions.html", "w") as f:
    f.write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: Montserrat, sans-serif; }}
    #root .cap {{ position: absolute; left: 70px; right: 70px; top: 1200px; text-align: center; }}
    #root .pill {{ display: inline-block; padding: 14px 30px 16px; background: #111318; color: #fff; border-radius: 14px;
      font-weight: 800; font-size: 50px; line-height: 1.2; box-shadow: 0 10px 30px rgba(0,0,0,.35); }}
    #root .pill .y {{ color: {YEL}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{cap_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{cap_js}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ---------------------------------------------------------------- INDEX + SOUND
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    for c, s, d in SCENES)
SFX = [
    ("sx-hook", "impact-bass-1", "s01", 0.02, 0.45), ("sx-mark1", "click-soft", "s01", 0.8, 0.3), ("sx-mark2", "click-soft", "s01", 2.15, 0.3),
    ("sx-02-in", "whoosh-short", "s02", -0.02, 0.32), ("sx-02-plan", "whoosh", "s02", 2.08, 0.3), ("sx-02-chip", "pop", "s02", 3.2, 0.22),
    ("sx-03-a", "click", "s03", 2.05, 0.26), ("sx-03-b", "key-press", "s03", 3.85, 0.32), ("sx-03-c", "click", "s03", 5.0, 0.26),
    ("sx-04-in", "whoosh-short", "s04", -0.02, 0.3), ("sx-04-x", "pop", "s04", 1.5, 0.3),
    ("sx-05-q", "impact-bass-2", "s05", 0.05, 0.35), ("sx-05-route", "sparkle", "s05", 0.5, 0.15),
    ("sx-06-route", "sparkle", "s06", 0.4, 0.22), ("sx-06-ok", "pop", "s06", 1.55, 0.3),
    ("sx-07-in", "whoosh", "s07", -0.02, 0.28), ("sx-07-ptr", "click-soft", "s07", 0.7, 0.3),
    ("sx-08-down", "whoosh-cinematic", "s08", 0.3, 0.25), ("sx-08-plan", "whoosh-short", "s08", 2.2, 0.3), ("sx-08-route", "sparkle", "s08", 3.1, 0.18),
    ("sx-09-in", "whoosh", "s09", -0.02, 0.3), ("sx-09-wipe", "whoosh-short", "s09", 1.7, 0.28), ("sx-09-up", "whoosh", "s09", 3.3, 0.25),
    ("sx-10-in", "whoosh-short", "s10", -0.02, 0.28), ("sx-10-badge", "pop", "s10", 1.8, 0.32),
    ("sx-11-l2", "click-soft", "s11", 3.85, 0.3),
    ("sx-12-wipe", "whoosh", "s12", 3.0, 0.28), ("sx-12-up", "whoosh-short", "s12", 5.6, 0.28),
    ("sx-13-in", "whoosh", "s13", -0.02, 0.3), ("sx-13-a", "pop", "s13", 3.1, 0.35), ("sx-13-b", "pop", "s13", 5.7, 0.35),
    ("sx-14-in", "impact-bass-1", "s14", 0.0, 0.4),
    ("sx-outro", "whoosh", "s15", -0.02, 0.45), ("sx-outro-hit", "impact-bass-1", "s15", 0.05, 0.55), ("sx-outro-sp", "sparkle", "s15", 1.0, 0.3),
]
DUR = {"click-soft": 0.36, "click": 0.36, "impact-bass-1": 2.1, "impact-bass-2": 2.55, "key-press": 0.43, "pop": 0.72,
       "sparkle": 1.8, "whoosh-cinematic": 5.5, "whoosh-short": 0.57, "whoosh": 0.57}
audio = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(max(0, START[sc] + t), 2)}" data-duration="{DUR[f]}" data-track-index="{4 + n % 5}" data-volume="{v}"></audio>'
    for n, (i, f, sc, t, v) in enumerate(SFX))
with open(f"{OUT}/index.html", "w") as f:
    f.write(f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #fff; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}
      <img id="logo" class="clip" src="assets/logo.png" alt="" data-start="0" data-duration="{TOTAL}" data-track-index="9" style="position:absolute; left:455px; top:52px; width:170px; height:117px; z-index:20" />
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
      <audio id="vo" class="clip" src="assets/audio/vo.mp3" data-start="0" data-duration="71.88" data-track-index="3" data-volume="1"></audio>
{audio}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok", TOTAL, "s,", len(caps), "captions")
