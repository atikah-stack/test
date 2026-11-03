#!/usr/bin/env python3
# Generates every scene file, the caption track and index.html for the
# house-accessories video. Run from the project folder:  python3 build-scenes.py .
# Scene and caption timing follows the voiceover transcript in assets/audio/transcript.json.
import difflib, json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(f"{OUT}/compositions", exist_ok=True)

YEL = "#F6C343"      # title yellow (from the reference title)
NAVY = "#141A26"     # dark backdrop
CARD = "rgba(16,20,29,.94)"

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: #fff;
      background: linear-gradient(180deg, #10151F 0%, #1A2232 45%, #2B3446 100%); }}
    #root .bg {{ position: absolute; inset: 0;
      background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
      background-size: 60px 60px; background-position: 30px 0; }}
    #root .stage {{ position: absolute; left: 0; top: 0; width: 1600px; height: 2800px; transform-origin: 0 0;
      -webkit-mask-image: linear-gradient(to bottom, transparent 0px, #000 150px);
      mask-image: linear-gradient(to bottom, transparent 0px, #000 150px); }}
    #root .stage .floor {{ position: absolute; left: -1200px; top: 880px; width: 4000px; height: 1900px;
      background: linear-gradient(to bottom, #C1BEC6 0px, #B5B3BC 500px, #9E9DA6 1900px); }}
    #root .stage .floorfade {{ position: absolute; left: 0; top: 800px; width: 1600px; height: 84px;
      background: linear-gradient(to bottom, rgba(193,190,198,0), #C1BEC6); }}
    #root .stage.nomask {{ -webkit-mask-image: none; mask-image: none; }}
    #root .stage img, #root .stage .layer {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; display: block; }}
    #root .stage svg {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; overflow: visible; }}
    #root .win {{ position: absolute; left: 0; width: 1080px; overflow: hidden; background: {NAVY}; }}
    #root .headline {{ position: absolute; left: 50px; right: 50px; text-align: center; font-weight: 900; font-size: 92px;
      line-height: 1.02; letter-spacing: -0.01em; text-transform: uppercase; color: #fff;
      text-shadow: 0 4px 0 rgba(0,0,0,.28), 0 12px 34px rgba(0,0,0,.55); }}
    #root .headline .ln {{ display: block; }}
    #root .y {{ color: {YEL}; }}
    #root .kicker {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 700; font-size: 30px;
      letter-spacing: 0.3em; text-transform: uppercase; color: rgba(255,255,255,.78); }}
    #root .tagwrap {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; }}
    #root .tag {{ display: flex; align-items: center; gap: 22px; padding: 22px 38px; background: {CARD};
      border: 2px solid {YEL}; border-radius: 10px; box-shadow: 0 18px 44px rgba(0,0,0,.4); }}
    #root .tag .num {{ font-weight: 900; font-size: 50px; color: {YEL}; }}
    #root .tag .dash {{ width: 46px; height: 3px; background: {YEL}; }}
    #root .tag .name {{ font-weight: 800; font-size: 46px; letter-spacing: 0.08em; color: #fff; }}
    #root .chip {{ position: absolute; padding: 10px 20px; background: {CARD}; color: #fff; font-weight: 800; font-size: 30px;
      letter-spacing: 0.16em; text-transform: uppercase; border-radius: 6px; }}
    #root .chip.yl {{ background: {YEL}; color: #141A26; }}
    #root .pointer {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #root .shade {{ position: absolute; left: 0; right: 0; top: 0; height: 900px;
      background: linear-gradient(to bottom, rgba(10,13,20,.85), rgba(10,13,20,.45) 55%, rgba(10,13,20,0)); }}
    #root video.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
"""

HELPERS = """
    const F = (s, px, py, cx, cy) => ({ x: cx - px * s, y: cy - py * s, scale: s });
    const R = (x1, y1, x2, y2) =>
      `inset(${(y1 / 9).toFixed(3)}% ${(100 - x2 / 16).toFixed(3)}% ${(100 - y2 / 9).toFixed(3)}% ${(x1 / 16).toFixed(3)}%)`;
    const tl = gsap.timeline({ paused: true });
"""

# Scene slots, timed to the voiceover (seconds).
SCENES = [("s01", 0, 4.6), ("s02", 4.6, 4.5), ("s03", 9.1, 6.5), ("s04", 15.6, 7.8), ("s05", 23.4, 7.65),
          ("s06", 31.05, 7.6), ("s07", 38.65, 6.55), ("s08", 45.2, 2.25), ("s09", 47.45, 4.85), ("s10", 52.3, 4.6),
          ("s11", 56.9, 7.15), ("s12", 64.05, 7.15), ("s13", 71.2, 5.0)]
START = {c: s for c, s, d in SCENES}
TOTAL = round(SCENES[-1][1] + SCENES[-1][2], 2)


def scene(cid, css, body, js):
    dur = next(d for c, s, d in SCENES if c == cid)
    html = f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{dur}">
    <div class="bg"></div>
{body}
  </div>
  <script>{HELPERS}{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    with open(f"{OUT}/compositions/{cid}.html", "w") as f:
        f.write(html)


def stage(sid, plain=True, full=True, extra="", cls="stage"):
    pre = sid.replace("-stage", "")
    p = f'<img id="{pre}-plain" src="assets/house-plain.jpg" alt="" />' if plain else ""
    fu = f'<img id="{pre}-full" src="assets/house-full.jpg" alt="" />' if full else ""
    return f"""    <div class="{cls}" id="{sid}">
      <div class="floor"></div>
      {p}
      {fu}
      <div class="floorfade"></div>
{extra}
    </div>"""


def tag(pre, num, name, top):
    return f"""    <div class="tagwrap" style="top:{top}px"><div class="tag" id="{pre}-tag">
      <span class="num">{num}</span><span class="dash"></span><span class="name">{name}</span>
    </div></div>"""


def ptr(pre, x2, y2, pts=None):
    if pts:
        line = f'<polyline id="{pre}-ptr" points="{pts}" fill="none" stroke="{YEL}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />'
    else:
        line = f'<line id="{pre}-ptr" x1="540" y1="352" x2="540" y2="{y2}" stroke="{YEL}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />'
    return f'    <svg class="pointer" viewBox="0 0 1080 1920">{line}<circle id="{pre}-dot" cx="{x2}" cy="{y2}" r="9" fill="{YEL}" stroke="#141A26" stroke-width="3" /></svg>'


TAG_IN = """
    tl.fromTo("#{p}-tag", {{ opacity: 0, y: -24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, {t});
    tl.to("#{p}-ptr", {{ strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut" }}, {t2});
    tl.fromTo("#{p}-dot", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {t3});
"""


def tag_in(p, t):
    return TAG_IN.format(p=p, t=t, t2=round(t + 0.25, 2), t3=round(t + 0.6, 2))


# ---------------------------------------------------------------- S01 HOOK
scene("s01", """
    #s01-line { opacity: 0; position: absolute; left: 0; top: 0; width: 4px; height: 900px; background: #fff; box-shadow: 0 0 18px rgba(255,255,255,.9); }
    #s01-flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
""", f"""{stage("s01-stage", extra='      <div id="s01-line"></div>')}
    <div class="headline" id="s01-head" style="top:230px">
      <span class="ln">Apa jadi kalau</span><span class="ln y">semua aksesori</span><span class="ln y">dibuang?</span>
    </div>
    <div id="s01-flash"></div>""", """
    tl.set("#s01-stage", F(0.66, 800, 470, 540, 880), 0);
    tl.set("#s01-full", { clipPath: "inset(0% 0% 0% 0%)" }, 0);
    tl.to("#s01-stage", { ...F(0.76, 800, 470, 540, 880), duration: 2.4, ease: "power2.out" }, 0);
    tl.fromTo("#s01-head", { scale: 1.05 }, { scale: 1, duration: 0.8, ease: "power3.out" }, 0);
    tl.to("#s01-line", { opacity: 1, duration: 0.05 }, 2.4);
    tl.to("#s01-full", { clipPath: "inset(0% 0% 0% 100%)", duration: 0.55, ease: "power3.inOut" }, 2.4);
    tl.fromTo("#s01-line", { x: -10 }, { x: 1610, duration: 0.55, ease: "power3.inOut" }, 2.4);
    tl.to("#s01-line", { opacity: 0, duration: 0.1 }, 2.95);
    tl.fromTo("#s01-flash", { opacity: 0 }, { opacity: 0.5, duration: 0.05 }, 2.95);
    tl.to("#s01-flash", { opacity: 0, duration: 0.45, ease: "power2.out" }, 3.0);
    tl.to("#s01-stage", { ...F(0.80, 800, 470, 540, 880), duration: 0.12, ease: "power2.out" }, 2.95);
    tl.to("#s01-stage", { ...F(0.78, 800, 470, 540, 880), duration: 1.5, ease: "sine.out" }, 3.07);
""")

# ---------------------------------------------------------------- S02 PLAIN
boxes = [("a", 290, 490, 585, 735, "KOSONG"), ("b", 628, 490, 935, 690, "PLAIN"), ("c", 1000, 230, 1440, 400, "HAMBAR")]
svg = '      <svg viewBox="0 0 1600 900">\n'
for k, x1, y1, x2, y2, t in boxes:
    svg += f'        <rect id="s02-box-{k}" x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="rgba(246,195,67,.10)" stroke="{YEL}" stroke-width="2.5" stroke-dasharray="10 8" />\n'
    svg += f'        <g id="s02-lab-{k}"><rect x="{x1}" y="{y1-56}" width="{len(t)*27+28}" height="50" fill="#141A26" /><text x="{x1+14}" y="{y1-16}" font-family="Montserrat" font-weight="800" font-size="34" letter-spacing="2" fill="{YEL}">{t}</text></g>\n'
svg += "      </svg>"
scene("s02", "", f"""{stage("s02-stage", full=False, extra=svg)}
    <div class="headline" id="s02-head" style="top:260px; font-size:108px"><span class="ln">Tanpa</span><span class="ln y">aksesori</span></div>""", """
    tl.fromTo("#s02-stage", F(0.78, 800, 470, 540, 880), { ...F(0.86, 800, 490, 540, 900), duration: 4.5, ease: "sine.inOut" }, 0);
    tl.fromTo("#s02-head .ln", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: "power4.out" }, 0.05);
    ["a", "b", "c"].forEach((k, i) => {
      tl.fromTo(`#s02-box-${k}`, { opacity: 0, scale: 1.06, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, 1.6 + i * 0.4);
      tl.fromTo(`#s02-lab-${k}`, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 1.7 + i * 0.4);
    });
""")

# ---------------------------------------------------------------- S03 TRANSFORMATION
regions = {
    "g1": (277, 520, 476, 694), "g2": (603, 236, 992, 422), "g3": (994, 198, 1448, 346),
    "b1": (626, 464, 968, 704),
    "c1": (1208, 384, 1430, 553), "c2": (996, 553, 1454, 574),
    "k1": (568, 418, 1024, 470),
}
layers = "\n".join(f'      <img class="layer" id="s03-{k}" src="assets/house-full.jpg" alt="" />' for k in regions)
outl = '      <svg viewBox="0 0 1600 900">\n' + "\n".join(
    f'        <rect id="s03-o-{k}" x="{a}" y="{b}" width="{c-a}" height="{d-b}" fill="none" stroke="{YEL}" stroke-width="4" />'
    for k, (a, b, c, d) in regions.items()) + "\n      </svg>"
steps = "".join(f'<span class="step" id="s03-st{i}"><b>0{i}</b>{n}</span>' for i, n in enumerate(["Groove line", "Batu hiasan", "Cornice", "Concrete slab"], 1))
scene("s03", f"""
    #s03-full {{ opacity: 0; }}
    #root .steps {{ position: absolute; left: 60px; right: 60px; top: 470px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px 18px; }}
    #root .step {{ display: flex; align-items: center; gap: 14px; padding: 14px 20px; border: 2px solid rgba(255,255,255,.18);
      border-radius: 8px; font-weight: 800; font-size: 29px; letter-spacing: .06em; text-transform: uppercase; color: rgba(255,255,255,.38); background: rgba(16,20,29,.6); }}
    #root .step b {{ font-weight: 900; color: rgba(246,195,67,.4); }}
""", f"""{stage("s03-stage", extra=layers + chr(10) + outl)}
    <div class="headline" id="s03-head" style="top:250px"><span class="ln">Bila tambah</span><span class="ln y">aksesori…</span></div>
    <div class="steps" id="s03-steps">{steps}</div>""", f"""
    const RG = {json.dumps(regions)};
    tl.fromTo("#s03-stage", F(0.70, 800, 470, 540, 1000), {{ ...F(0.75, 800, 470, 540, 1000), duration: 6.5, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s03-head .ln", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: "power4.out" }}, 0.05);
    tl.fromTo("#s03-steps .step", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.05, ease: "power3.out" }}, 0.35);
    Object.keys(RG).forEach((k) => {{
      const [a, b, c, d] = RG[k];
      tl.set(`#s03-${{k}}`, {{ clipPath: R(a, d, c, d) }}, 0);
      tl.set(`#s03-o-${{k}}`, {{ opacity: 0 }}, 0);
    }});
    const groups = [["g1", "g2", "g3"], ["b1"], ["c1", "c2"], ["k1"]];
    groups.forEach((g, i) => {{
      const t = 1.1 + i * 0.95;
      g.forEach((k, j) => {{
        const [a, b, c, d] = RG[k];
        tl.to(`#s03-${{k}}`, {{ clipPath: R(a, b, c, d), duration: 0.5, ease: "power3.inOut" }}, t + j * 0.08);
        tl.fromTo(`#s03-o-${{k}}`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, t + j * 0.08);
        tl.to(`#s03-o-${{k}}`, {{ opacity: 0, duration: 0.5 }}, t + 0.6);
      }});
      tl.to(`#s03-st${{i + 1}}`, {{ color: "#ffffff", borderColor: "{YEL}", backgroundColor: "rgba(16,20,29,.95)", duration: 0.2 }}, t);
      tl.to(`#s03-st${{i + 1}} b`, {{ color: "{YEL}", duration: 0.2 }}, t);
    }});
    tl.to("#s03-full", {{ opacity: 1, duration: 0.6, ease: "sine.inOut" }}, 4.9);
""")

# ---------------------------------------------------------------- S04 GROOVE LINE
grooves = [557, 590, 622, 656]
gsvg = '      <svg viewBox="0 0 1600 900">\n' + "\n".join(
    f'        <line class="s04-gl" x1="279" y1="{y}" x2="472" y2="{y}" stroke="{YEL}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" />'
    for y in grooves) + "\n      </svg>"
scene("s04", """
    #s04-a { position: absolute; inset: 0; }
    #s04-b { position: absolute; inset: 0; opacity: 0; }
""", f"""    <div id="s04-a">
{stage("s04-stage", plain=False, extra=gsvg)}
{tag("s04", "01", "GROOVE LINE", 250)}
{ptr("s04", 540, 520)}
    </div>
    <div id="s04-b">
      <div class="win" id="s04-wt" style="top:190px; height:470px">
{stage("s04-st", full=False, cls="stage nomask")}
        <div class="chip" style="left:36px; top:30px">Sebelum</div>
      </div>
      <div class="win" id="s04-wb" style="top:676px; height:470px">
{stage("s04-sb", plain=False, cls="stage nomask")}
        <div class="chip yl" style="left:36px; top:30px">Selepas</div>
      </div>
    </div>""", f"""
    tl.fromTo("#s04-stage", F(1.4, 372, 600, 540, 860), {{ ...F(2.7, 372, 600, 540, 860), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s04-stage", {{ ...F(2.9, 380, 605, 540, 860), duration: 3.85, ease: "sine.inOut" }}, 0.55);
{tag_in("s04", 0.9)}
    tl.to("#s04-stage .s04-gl", {{ strokeDashoffset: 0, duration: 0.7, stagger: 0.2, ease: "power2.inOut" }}, 2.4);
    tl.to("#s04-stage .s04-gl", {{ opacity: 0.45, duration: 0.6 }}, 3.8);
    tl.set("#s04-a", {{ opacity: 0 }}, 4.4);
    tl.set("#s04-b", {{ opacity: 1 }}, 4.4);
    tl.set("#s04-st", F(2.2, 380, 600, 540, 235), 4.4);
    tl.set("#s04-sb", F(2.2, 380, 600, 540, 235), 4.4);
    tl.fromTo("#s04-wt", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }}, 4.4);
    tl.fromTo("#s04-wb", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }}, 4.55);
    tl.to("#s04-st", {{ ...F(2.35, 380, 600, 540, 235), duration: 3.4, ease: "sine.inOut" }}, 4.4);
    tl.to("#s04-sb", {{ ...F(2.35, 380, 600, 540, 235), duration: 3.4, ease: "sine.inOut" }}, 4.4);
""")

# ---------------------------------------------------------------- S05 BATU HIASAN
B = regions["b1"]
scene("s05", f"""
    #s05-chip-b, #s05-chip-a {{ opacity: 0; }}
    #s05-shine {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; overflow: hidden; }}
    #s05-band {{ position: absolute; left: 0; top: 380px; width: 160px; height: 420px;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.30) 50%, rgba(255,255,255,0)); }}
""", f"""{stage("s05-stage", extra='      <div id="s05-shine"><div id="s05-band"></div></div>')}
{tag("s05", "02", "BATU HIASAN", 250)}
{ptr("s05", 300, 560, "540,352 540,430 300,430 300,560")}
    <div class="chip" id="s05-chip-b" style="left:60px; top:1060px">Sebelum</div>
    <div class="chip yl" id="s05-chip-a" style="left:60px; top:1060px">Selepas</div>""", f"""
    tl.set("#s05-shine", {{ clipPath: R({B[0]}, {B[1]}, {B[2]}, {B[3]}) }}, 0);
    tl.set("#s05-full", {{ clipPath: "inset(0% 0% 0% 0%)" }}, 0);
    tl.fromTo("#s05-stage", F(1.3, 796, 590, 540, 880), {{ ...F(2.45, 796, 590, 540, 880), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s05-stage", {{ ...F(2.62, 790, 585, 540, 880), duration: 7.1, ease: "sine.inOut" }}, 0.55);
{tag_in("s05", 0.9)}
    tl.fromTo("#s05-band", {{ x: 520 }}, {{ x: 1000, duration: 1.4, ease: "sine.inOut" }}, 2.6);
    tl.to("#s05-full", {{ clipPath: "inset(0% 0% 0% 100%)", duration: 0.45, ease: "power3.inOut" }}, 4.6);
    tl.to("#s05-chip-b", {{ opacity: 1, duration: 0.15 }}, 4.75);
    tl.fromTo("#s05-full", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut", immediateRender: false }}, 5.8);
    tl.to("#s05-chip-b", {{ opacity: 0, duration: 0.1 }}, 5.9);
    tl.to("#s05-chip-a", {{ opacity: 1, duration: 0.15 }}, 6.0);
""")

# ---------------------------------------------------------------- S06 CORNICE
C = (1213, 388, 1426, 550)
tick = lambda x1, y1, x2, y2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" vector-effect="non-scaling-stroke" />'
csvg = f"""      <svg viewBox="0 0 1600 900">
        <rect id="s06-frame" x="{C[0]}" y="{C[1]}" width="{C[2]-C[0]}" height="{C[3]-C[1]}" fill="none" stroke="{YEL}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" />
        <g id="s06-ticks" stroke="#fff" stroke-width="2.5">
          {tick(C[0]-14, C[1], C[0]-4, C[1])}{tick(C[0], C[1]-14, C[0], C[1]-4)}{tick(C[2]+4, C[1], C[2]+14, C[1])}{tick(C[2], C[1]-14, C[2], C[1]-4)}
          {tick(C[0]-14, C[3], C[0]-4, C[3])}{tick(C[0], C[3]+4, C[0], C[3]+14)}{tick(C[2]+4, C[3], C[2]+14, C[3])}{tick(C[2], C[3]+4, C[2], C[3]+14)}
        </g>
      </svg>"""
scene("s06", """
    #s06-chip-b, #s06-chip-a, #s06-ticks { opacity: 0; }
""", f"""{stage("s06-stage", extra=csvg)}
{tag("s06", "03", "CORNICE", 250)}
{ptr("s06", 540, 470)}
    <div class="chip" id="s06-chip-b" style="left:60px; top:1060px">Sebelum</div>
    <div class="chip yl" id="s06-chip-a" style="left:60px; top:1060px">Selepas</div>""", f"""
    tl.fromTo("#s06-stage", F(1.5, 1320, 470, 540, 800), {{ ...F(3.0, 1320, 470, 540, 800), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s06-stage", {{ ...F(3.15, 1318, 468, 540, 800), duration: 7.0, ease: "sine.inOut" }}, 0.55);
{tag_in("s06", 0.9)}
    tl.to("#s06-frame", {{ strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }}, 2.2);
    tl.to("#s06-ticks", {{ opacity: 1, duration: 0.3 }}, 3.0);
    tl.to(["#s06-frame", "#s06-ticks"], {{ opacity: 0, duration: 0.2 }}, 4.6);
    tl.to("#s06-full", {{ opacity: 0, duration: 0.18 }}, 4.8);
    tl.to("#s06-chip-b", {{ opacity: 1, duration: 0.12 }}, 4.8);
    tl.to("#s06-full", {{ opacity: 1, duration: 0.18 }}, 5.8);
    tl.to("#s06-chip-b", {{ opacity: 0, duration: 0.08 }}, 5.8);
    tl.to("#s06-chip-a", {{ opacity: 1, duration: 0.12 }}, 5.85);
""")

# ---------------------------------------------------------------- S07 CONCRETE SLAB
K = regions["k1"]
scene("s07", f"""
    #s07-shadow, #s07-guides, #s07-dim {{ opacity: 0; }}
    #s07-shadow {{ position: absolute; left: {K[0]}px; top: {K[3]}px; width: {K[2]-K[0]}px; height: 40px;
      background: linear-gradient(to bottom, rgba(10,12,14,.55), rgba(10,12,14,0)); transform-origin: 50% 0; }}
    #s07-slab {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; }}
""", f"""{stage("s07-stage", plain=False, extra=f'''      <div id="s07-shadow"></div>
      <img id="s07-slab" src="assets/house-full.jpg" alt="" />
      <svg viewBox="0 0 1600 900">
        <g id="s07-guides" stroke="{YEL}" stroke-width="2.5" fill="none">
          {tick(K[0]-40, K[1], K[0]-8, K[1])}{tick(K[0]-40, K[3], K[0]-8, K[3])}{tick(K[0]-24, K[1], K[0]-24, K[3])}
          {tick(K[2]+8, K[1], K[2]+40, K[1])}{tick(K[2]+8, K[3], K[2]+40, K[3])}{tick(K[2]+24, K[1], K[2]+24, K[3])}
        </g>
      </svg>''')}
{tag("s07", "04", "CONCRETE SLAB", 250)}
{ptr("s07", 540, 560)}
    <div class="tagwrap" style="top:1060px"><div class="chip yl" id="s07-dim" style="position:static">Lebih berdimensi</div></div>""", f"""
    tl.set("#s07-slab", {{ clipPath: R({K[0]}, {K[1]}, {K[2]}, {K[3]}) }}, 0);
    tl.fromTo("#s07-stage", F(1.2, 796, 470, 540, 760), {{ ...F(2.2, 796, 470, 540, 760), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s07-stage", {{ ...F(2.32, 796, 468, 540, 760), duration: 6.0, ease: "sine.inOut" }}, 0.55);
{tag_in("s07", 1.05)}
    tl.fromTo("#s07-slab", {{ y: 0 }}, {{ y: -7, duration: 0.9, ease: "power3.out" }}, 2.6);
    tl.to("#s07-shadow", {{ opacity: 0.85, duration: 0.9, ease: "power2.out" }}, 2.6);
    tl.to("#s07-guides", {{ opacity: 1, duration: 0.4 }}, 2.9);
    tl.fromTo("#s07-dim", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 4.6);
""")

# ---------------------------------------------------------------- S08 BEFORE vs AFTER slider
scene("s08", f"""
    #s08-handle {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; }}
    #s08-bar {{ position: absolute; left: -2px; top: 60px; width: 5px; height: 780px; background: {YEL}; }}
    #s08-knob {{ position: absolute; left: -40px; top: 410px; width: 80px; height: 80px; border-radius: 50%; background: {YEL};
      display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 32px; color: #141A26; letter-spacing: 4px; }}
""", f"""{stage("s08-stage", extra='      <div id="s08-handle"><div id="s08-bar"></div><div id="s08-knob">‹›</div></div>')}
    <div class="headline" id="s08-head" style="top:250px; font-size:104px">Before <span class="y" style="font-weight:600">vs</span><br /><span class="y">After</span></div>
    <div class="chip" id="s08-cb" style="left:60px; top:520px">Before</div>
    <div class="chip yl" id="s08-ca" style="right:60px; top:520px">After</div>""", """
    tl.set("#s08-stage", F(0.68, 800, 470, 540, 900), 0);
    tl.to("#s08-stage", { ...F(0.71, 800, 470, 540, 900), duration: 2.25, ease: "sine.inOut" }, 0);
    tl.fromTo("#s08-full", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 50%)", duration: 0.5, ease: "power3.inOut" }, 0.05);
    tl.fromTo("#s08-handle", { x: 1600 }, { x: 800, duration: 0.5, ease: "power3.inOut" }, 0.05);
    tl.to("#s08-full", { clipPath: "inset(0% 0% 0% 22%)", duration: 0.4, ease: "power2.inOut" }, 0.75);
    tl.to("#s08-handle", { x: 352, duration: 0.4, ease: "power2.inOut" }, 0.75);
    tl.to("#s08-full", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 1.35);
    tl.to("#s08-handle", { x: -40, opacity: 0, duration: 0.5, ease: "power3.inOut" }, 1.35);
    tl.fromTo("#s08-head", { opacity: 0, scale: 1.1 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power4.out" }, 0);
    tl.fromTo(["#s08-cb", "#s08-ca"], { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.08 }, 0.25);
    tl.to("#s08-cb", { opacity: 0, duration: 0.25 }, 1.4);
""")

# ---------------------------------------------------------------- S09 BUDGET (drone footage of a finished house)
scene("s09", f"""
    #s09-rule {{ position: absolute; left: 290px; top: 560px; width: 500px; height: 8px; background: {YEL}; transform-origin: 0 50%; }}
    #s09-wrap {{ position: absolute; inset: 0; }}
""", f"""    <div id="s09-wrap"><video id="s09-vid" class="clip full" src="assets/video/drone-house.mp4" data-start="0" data-duration="4.85" data-media-start="0.6" muted playsinline></video></div>
    <div class="shade"></div>
    <div class="headline" id="s09-head" style="top:230px; font-size:100px">
      <span class="ln">Lebih detail</span><span class="ln y" style="font-weight:600">=</span><span class="ln y">Lebih bajet</span>
    </div>
    <div id="s09-rule"></div>""", """
    tl.fromTo("#s09-wrap", { scale: 1.08 }, { scale: 1.0, duration: 4.85, ease: "sine.out" }, 0);
    tl.fromTo("#s09-head .ln", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.3, ease: "power4.out" }, 0.15);
    tl.fromTo("#s09-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.inOut" }, 1.1);
""")

# ---------------------------------------------------------------- S10 SIMPLE vs FULL
scene("s10", f"""
    #s10-vs {{ position: absolute; left: 475px; top: 615px; width: 130px; height: 130px; border-radius: 50%; background: {YEL};
      color: #141A26; font-weight: 900; font-size: 50px; display: flex; align-items: center; justify-content: center; border: 6px solid #141A26; }}
""", f"""    <div class="win" id="s10-wt" style="top:190px; height:480px">
{stage("s10-st", full=False, cls="stage nomask")}
      <div class="chip" style="left:36px; bottom:28px">Simple</div>
    </div>
    <div class="win" id="s10-wb" style="top:690px; height:480px">
{stage("s10-sb", plain=False, cls="stage nomask")}
      <div class="chip yl" style="right:36px; bottom:28px">Full accessories</div>
    </div>
    <div id="s10-vs">VS</div>""", """
    tl.fromTo("#s10-st", F(0.70, 800, 470, 540, 240), { ...F(0.75, 800, 470, 540, 240), duration: 4.6, ease: "sine.inOut" }, 0);
    tl.fromTo("#s10-sb", F(0.75, 800, 470, 540, 240), { ...F(0.70, 800, 470, 540, 240), duration: 4.6, ease: "sine.inOut" }, 0);
    tl.fromTo("#s10-wt", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }, 0);
    tl.fromTo("#s10-wb", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }, 0.15);
    tl.fromTo("#s10-vs", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 0.6);
""")

# ---------------------------------------------------------------- S11 EMOTIONAL ENDING (real footage)
scene("s11", f"""
    #s11-wrap {{ position: absolute; inset: 0; }}
    #s11-rule {{ position: absolute; left: 440px; top: 368px; width: 200px; height: 5px; background: {YEL}; transform-origin: 50% 50%; }}
    #s11-l1 {{ top: 250px; font-size: 76px; }}
    #s11-l2 {{ top: 410px; font-size: 104px; }}
""", f"""    <div id="s11-wrap">
      <video id="s11-v1" class="clip full" src="assets/video/drone-estate.mp4" data-start="0" data-duration="2.45" data-media-start="1.0" muted playsinline></video>
      <video id="s11-v2" class="clip full" src="assets/video/walk-front.mp4" data-start="2.45" data-duration="2.35" data-media-start="0.6" muted playsinline></video>
      <video id="s11-v3" class="clip full" src="assets/video/walk-under.mp4" data-start="4.8" data-duration="2.35" data-media-start="0.3" muted playsinline></video>
    </div>
    <div class="shade"></div>
    <div class="headline" id="s11-l1">Rumah sekali bina.</div>
    <div id="s11-rule"></div>
    <div class="headline y" id="s11-l2">Biar puas hati.</div>""", """
    tl.fromTo("#s11-wrap", { scale: 1.0 }, { scale: 1.1, duration: 7.15, ease: "sine.inOut" }, 0);
    tl.fromTo("#s11-l1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 0.3);
    tl.fromTo("#s11-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.inOut" }, 1.0);
    tl.fromTo("#s11-l2", { opacity: 0, y: 40, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.5)" }, 4.75);
""")

# ---------------------------------------------------------------- S12 CTA
scene("s12", f"""
    #s12-or {{ position: absolute; left: 0; right: 0; top: 616px; text-align: center; font-weight: 700; font-size: 40px; letter-spacing: .3em; color: rgba(255,255,255,.75); text-transform: uppercase; }}
    #s12-q1, #s12-q2 {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 900; font-size: 62px; text-transform: uppercase;
      text-shadow: 0 4px 0 rgba(0,0,0,.28), 0 10px 30px rgba(0,0,0,.5); }}
    #s12-bgv {{ position: absolute; inset: 0; opacity: 0; }}
    #s12-dim {{ position: absolute; inset: 0; background: rgba(10,13,20,.6); }}
    #s12-cta {{ position: absolute; left: 80px; right: 80px; top: 540px; padding: 56px 40px 46px; background: {CARD}; border: 3px solid {YEL};
      border-radius: 16px; text-align: center; color: #fff; box-shadow: 0 30px 70px rgba(0,0,0,.45); opacity: 0; }}
    #s12-cta .t {{ font-weight: 900; font-size: 70px; line-height: 1.04; text-transform: uppercase; }}
    #s12-cta .s {{ margin-top: 16px; font-weight: 800; font-size: 32px; letter-spacing: .14em; color: {YEL}; text-transform: uppercase; }}
    #s12-arrow {{ display: block; margin: 26px auto 0; }}
""", f"""    <div id="s12-bgv"><video id="s12-vid" class="clip full" src="assets/video/drone-top.mp4" data-start="4.2" data-duration="2.95" data-media-start="2" muted playsinline></video><div id="s12-dim"></div></div>
    <div id="s12-pair">
      <div class="win" id="s12-wt" style="top:244px; height:360px">
{stage("s12-st", full=False, cls="stage nomask")}
      </div>
      <div class="win" id="s12-wb" style="top:684px; height:360px">
{stage("s12-sb", plain=False, cls="stage nomask")}
      </div>
      <div id="s12-q1" style="top:162px">Team jimat bajet?</div>
      <div id="s12-or">atau</div>
      <div id="s12-q2" class="y" style="top:1054px">Team puas hati?</div>
    </div>
    <div id="s12-cta" data-layout-allow-overlap data-layout-allow-occlusion>
      <div class="t">Komen <span class="y">pilihan</span><br />korang</div>
      <div class="s">Jimat bajet / Puas hati</div>
      <svg id="s12-arrow" width="60" height="76" viewBox="0 0 60 76"><path d="M30 4 V64 M8 44 L30 66 L52 44" fill="none" stroke="{YEL}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg>
    </div>""", """
    tl.set("#s12-st", F(0.69, 800, 480, 540, 190), 0);
    tl.set("#s12-sb", F(0.69, 800, 480, 540, 190), 0);
    tl.to("#s12-st", { ...F(0.72, 800, 480, 540, 190), duration: 4.5, ease: "sine.inOut" }, 0);
    tl.to("#s12-sb", { ...F(0.72, 800, 480, 540, 190), duration: 4.5, ease: "sine.inOut" }, 0);
    tl.fromTo("#s12-wt", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 0);
    tl.fromTo("#s12-wb", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 0.1);
    tl.fromTo("#s12-q1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.3);
    tl.fromTo("#s12-or", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.3);
    tl.fromTo("#s12-q2", { opacity: 0, y: 20, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 1.9);
    tl.to("#s12-pair", { opacity: 0, duration: 0.4 }, 4.25);
    tl.to("#s12-bgv", { opacity: 1, duration: 0.4 }, 4.2);
    tl.fromTo("#s12-cta", { opacity: 0, y: 40, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power4.out" }, 4.45);
    tl.fromTo("#s12-arrow", { y: 0 }, { y: 14, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 5 }, 4.9);
""")

# ---------------------------------------------------------------- S13 OUTRO (company card)
scene("s13", f"""
    #s13-img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 55%; }}
    #s13-img img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }}
    #root .ring {{ position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; border: 5px solid {YEL}; opacity: 0; }}
    #s13-shine {{ position: absolute; left: 30px; top: 1180px; width: 1020px; height: 420px; overflow: hidden; }}
    #s13-band {{ position: absolute; left: 0; top: 0; width: 220px; height: 420px;
      background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.38) 50%, rgba(255,255,255,0)); }}
    #s13-glow {{ position: absolute; left: 86px; top: 1440px; width: 908px; height: 132px; border-radius: 30px; border: 4px solid {YEL};
      box-shadow: 0 0 40px rgba(246,195,67,.75); opacity: 0; }}
    #s13-fade {{ position: absolute; inset: 0; background: #0B0F16; }}
""", f"""    <div id="s13-img"><img src="assets/outro.jpg" alt="" /></div>
    <div class="ring" id="s13-r1" style="left:477px; top:888px"></div>
    <div class="ring" id="s13-r2" style="left:744px; top:1002px"></div>
    <div id="s13-shine"><div id="s13-band"></div></div>
    <div id="s13-glow"></div>
    <div id="s13-fade"></div>""", """
    tl.fromTo("#s13-fade", { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power2.out" }, 0);
    tl.fromTo("#s13-img", { scale: 1.14 }, { scale: 1.0, duration: 1.1, ease: "expo.out" }, 0);
    tl.to("#s13-img", { scale: 1.03, duration: 3.9, ease: "sine.inOut" }, 1.1);
    ["#s13-r1", "#s13-r2"].forEach((r, i) => {
      tl.fromTo(r, { opacity: 0.95, scale: 0.3 }, { opacity: 0, scale: 2.1, duration: 1.0, ease: "power2.out", repeat: 2 }, 0.7 + i * 0.25);
    });
    tl.fromTo("#s13-band", { x: -240 }, { x: 1060, duration: 1.1, ease: "sine.inOut" }, 1.0);
    tl.fromTo("#s13-glow", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }, 1.6);
""")

# ---------------------------------------------------------------- CAPTIONS synced to the voiceover
SCRIPT = """Apa jadi kalau rumah ni kita buang semua aksesori dia?
Haa, cuba tengok! Nampak hambar dan tak berseri langsung kan?
Tapi bila kita tambahkan aksesori satu per satu, terus berubah rupa rumah!
Yang pertama, groove line!
Garisan dekat dinding ni buat rumah nampak lebih menarik dan tak terlalu plain.
Yang kedua, batu hiasan!
Batu dekat bahagian pintu masuk ni buat rumah nampak lebih eksklusif.
Yang ketiga, cornice!
Kemasan dekat tingkap ni pula buat design rumah nampak lebih kemas dan menyerlah.
Dan yang keempat, concrete slab!
Elemen ni buat fasad rumah nampak lebih berdimensi.
Haa, nampak tak beza dia?
Tapi nak tambah aksesori ni, mestilah kena tambah bajet juga!
Jadi, korang sanggup tambah bajet atau cukup rumah yang simple?
Sebab rumah ni kita bina sekali je seumur hidup.
Kalau dah buat, biarlah sedap mata memandang!
Nak jimat bajet atau nak puas hati setiap kali tengok rumah sendiri?
Korang team mana? Cuba komen dekat bawah!"""
HIGHLIGHT = {"groove", "line", "batu", "hiasan", "cornice", "concrete", "slab", "bajet", "aksesori", "hambar", "eksklusif",
             "berdimensi", "puas", "hati", "komen"}

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
for i in range(len(times)):          # script words the voice skipped: borrow the neighbour's time
    if times[i] is None:
        p = times[i - 1][1] if i else 0
        times[i] = (p, p + 0.2)

# chunk: break after punctuation, at most 4 words per chunk
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
    #root .cap {{ position: absolute; left: 70px; right: 70px; top: 1190px; text-align: center; }}
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

# ---------------------------------------------------------------- INDEX
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    for c, s, d in SCENES)

# sound effects: (id, file, scene, local time, volume) - kept under the voice
SFX = [
    ("sx-hook-wipe", "whoosh-short", "s01", 2.38, 0.4), ("sx-hook-hit", "impact-bass-1", "s01", 2.93, 0.55),
    ("sx-plain-a", "click-soft", "s02", 1.6, 0.3), ("sx-plain-b", "click-soft", "s02", 2.0, 0.28), ("sx-plain-c", "click-soft", "s02", 2.4, 0.3),
    ("sx-tr-1", "click", "s03", 1.1, 0.28), ("sx-tr-2", "key-press", "s03", 2.05, 0.35), ("sx-tr-3", "click", "s03", 3.0, 0.28),
    ("sx-tr-4", "key-press", "s03", 3.95, 0.35), ("sx-tr-sp", "sparkle", "s03", 4.9, 0.22),
    ("sx-01-in", "whoosh", "s04", -0.02, 0.35), ("sx-01-tag", "click-soft", "s04", 0.9, 0.32), ("sx-01-trace", "sparkle", "s04", 2.4, 0.18), ("sx-01-split", "whoosh-short", "s04", 4.38, 0.32),
    ("sx-02-in", "whoosh-short", "s05", -0.02, 0.35), ("sx-02-tag", "click-soft", "s05", 0.9, 0.32), ("sx-02-shine", "sparkle", "s05", 2.6, 0.22),
    ("sx-02-b", "whoosh", "s05", 4.55, 0.25), ("sx-02-a", "whoosh-short", "s05", 5.75, 0.25),
    ("sx-03-in", "whoosh", "s06", -0.02, 0.35), ("sx-03-tag", "click-soft", "s06", 0.9, 0.32), ("sx-03-trace", "sparkle", "s06", 2.2, 0.18),
    ("sx-03-b", "click", "s06", 4.8, 0.25), ("sx-03-a", "click", "s06", 5.8, 0.25),
    ("sx-04-in", "whoosh-short", "s07", -0.02, 0.35), ("sx-04-tag", "click-soft", "s07", 1.05, 0.32), ("sx-04-lift", "pop", "s07", 2.6, 0.25),
    ("sx-reveal", "impact-bass-2", "s08", 0.02, 0.55), ("sx-slide", "whoosh-short", "s08", 0.73, 0.22),
    ("sx-budget", "whoosh", "s09", 0.0, 0.3),
    ("sx-split", "whoosh", "s10", -0.02, 0.32), ("sx-vs", "pop", "s10", 0.6, 0.3),
    ("sx-end", "whoosh-cinematic", "s11", 0.0, 0.25), ("sx-end-2", "click-soft", "s11", 4.75, 0.25),
    ("sx-cta-in", "whoosh-short", "s12", -0.02, 0.32), ("sx-cta", "pop", "s12", 4.45, 0.32),
    ("sx-outro", "whoosh", "s13", -0.02, 0.45), ("sx-outro-hit", "impact-bass-1", "s13", 0.05, 0.6), ("sx-outro-sp", "sparkle", "s13", 1.0, 0.3),
]
DUR = {"click-soft": 0.36, "click": 0.36, "impact-bass-1": 2.1, "impact-bass-2": 2.55, "key-press": 0.43, "pop": 0.72,
       "sparkle": 1.8, "whoosh-cinematic": 5.5, "whoosh-short": 0.57, "whoosh": 0.57}
audio = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(START[sc] + t, 2)}" data-duration="{DUR[f]}" data-track-index="{4 + n % 3}" data-volume="{v}"></audio>'
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
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {NAVY}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {NAVY}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
      <audio id="vo" class="clip" src="assets/audio/vo.mp3" data-start="0" data-duration="71.08" data-track-index="3" data-volume="1"></audio>
{audio}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok", TOTAL, "s,", len(caps), "captions")
