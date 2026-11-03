#!/usr/bin/env python3
# Generates the HyperFrames scene files for the house-accessories video.
import json, os, sys

OUT = sys.argv[1]
os.makedirs(f"{OUT}/compositions", exist_ok=True)

INK = "#1C1E21"
PAPER = "#F1F2F4"
STONE = "#7D7A75"
BRASS = "#A8875A"
BRASS_T = "#86663B"

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {PAPER}; font-family: Inter, sans-serif; color: {INK}; }}
    #root .bg {{ position: absolute; inset: 0;
      background-image: linear-gradient(rgba(28,30,33,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(28,30,33,.045) 1px, transparent 1px);
      background-size: 60px 60px; background-position: 30px 0; }}
    #root .stage {{ position: absolute; left: 0; top: 0; width: 1600px; height: 2800px; transform-origin: 0 0;
      -webkit-mask-image: linear-gradient(to bottom, transparent 0px, #000 72px);
      mask-image: linear-gradient(to bottom, transparent 0px, #000 72px); }}
    #root .stage .floor {{ position: absolute; left: -1200px; top: 880px; width: 4000px; height: 1900px;
      background: linear-gradient(to bottom, #C1BEC6 0px, #CBC9CF 500px, #D9D8DC 1900px); }}
    #root .stage .floorfade {{ position: absolute; left: 0; top: 800px; width: 1600px; height: 84px;
      background: linear-gradient(to bottom, rgba(193,190,198,0), #C1BEC6); }}
    #root .stage.nomask {{ -webkit-mask-image: none; mask-image: none; }}
    #root .stage img, #root .stage .layer {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; display: block; }}
    #root .stage svg {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; overflow: visible; }}
    #root .win {{ position: absolute; left: 0; width: 1080px; overflow: hidden; background: {PAPER}; }}
    #root .headline {{ position: absolute; left: 80px; right: 80px; text-align: center; font-weight: 900; font-size: 80px;
      line-height: 1.0; letter-spacing: -0.02em; text-transform: uppercase; color: {INK}; }}
    #root .headline .ln {{ display: block; }}
    #root .kicker {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 700; font-size: 26px;
      letter-spacing: 0.32em; text-transform: uppercase; color: {STONE}; }}
    #root .tagwrap {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; }}
    #root .tag {{ display: flex; align-items: center; gap: 22px; padding: 22px 36px; background: rgba(250,250,249,.96);
      border: 1.5px solid {INK}; border-radius: 6px; box-shadow: 0 18px 40px rgba(20,22,25,.18); }}
    #root .tag .num {{ font-weight: 900; font-size: 44px; color: {BRASS}; letter-spacing: 0.02em; }}
    #root .tag .dash {{ width: 46px; height: 2px; background: {INK}; }}
    #root .tag .name {{ font-weight: 700; font-size: 42px; letter-spacing: 0.16em; color: {INK}; }}
    #root .chip {{ position: absolute; padding: 10px 18px; background: {INK}; color: #fff; font-weight: 700; font-size: 28px;
      letter-spacing: 0.22em; text-transform: uppercase; border-radius: 4px; }}
    #root .chip.light {{ background: rgba(250,250,249,.95); color: {INK}; border: 1.5px solid {INK}; }}
    #root .pointer {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
"""

HELPERS = """
    const F = (s, px, py, cx, cy) => ({ x: cx - px * s, y: cy - py * s, scale: s });
    const R = (x1, y1, x2, y2) =>
      `inset(${(y1 / 9).toFixed(3)}% ${(100 - x2 / 16).toFixed(3)}% ${(100 - y2 / 9).toFixed(3)}% ${(x1 / 16).toFixed(3)}%)`;
    const tl = gsap.timeline({ paused: true });
"""


def scene(cid, dur, css, body, js):
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


# ---------------------------------------------------------------- S01 HOOK
scene("s01", 4.6, """
    #s01-line { opacity: 0; position: absolute; left: 0; top: 0; width: 4px; height: 900px; background: #fff; box-shadow: 0 0 18px rgba(255,255,255,.9); }
    #s01-flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
""", f"""{stage("s01-stage", extra='      <div id="s01-line"></div>')}
    <div class="headline" id="s01-head" style="top:250px">
      <span class="ln">Apa jadi kalau</span><span class="ln">semua aksesori</span><span class="ln">dibuang?</span>
    </div>
    <div id="s01-flash"></div>""", """
    tl.set("#s01-stage", F(0.66, 800, 470, 540, 860), 0);
    tl.set("#s01-full", { clipPath: "inset(0% 0% 0% 0%)" }, 0);
    tl.to("#s01-stage", { ...F(0.76, 800, 470, 540, 860), duration: 2.4, ease: "power2.out" }, 0);
    tl.fromTo("#s01-head", { scale: 1.04 }, { scale: 1, duration: 0.8, ease: "power3.out" }, 0);
    // wipe the accessories away, left to right
    tl.to("#s01-line", { opacity: 1, duration: 0.05 }, 2.4);
    tl.to("#s01-full", { clipPath: "inset(0% 0% 0% 100%)", duration: 0.55, ease: "power3.inOut" }, 2.4);
    tl.fromTo("#s01-line", { x: -10 }, { x: 1610, duration: 0.55, ease: "power3.inOut" }, 2.4);
    tl.to("#s01-line", { opacity: 0, duration: 0.1 }, 2.95);
    tl.fromTo("#s01-flash", { opacity: 0 }, { opacity: 0.55, duration: 0.05 }, 2.95);
    tl.to("#s01-flash", { opacity: 0, duration: 0.45, ease: "power2.out" }, 3.0);
    tl.to("#s01-stage", { ...F(0.80, 800, 470, 540, 860), duration: 0.12, ease: "power2.out" }, 2.95);
    tl.to("#s01-stage", { ...F(0.78, 800, 470, 540, 860), duration: 1.5, ease: "sine.out" }, 3.07);
""")

# ---------------------------------------------------------------- S02 PLAIN
boxes = [("a", 290, 490, 585, 735, "KOSONG"), ("b", 628, 490, 935, 690, "PLAIN"), ("c", 1000, 230, 1440, 400, "HAMBAR")]
svg = '      <svg viewBox="0 0 1600 900">\n'
for k, x1, y1, x2, y2, t in boxes:
    svg += f'        <rect id="s02-box-{k}" x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="rgba(168,135,90,.07)" stroke="{INK}" stroke-width="1.6" stroke-dasharray="8 7" />\n'
    svg += f'        <g id="s02-lab-{k}"><rect x="{x1}" y="{y1-56}" width="{len(t)*25+28}" height="50" fill="{INK}" /><text x="{x1+14}" y="{y1-14}" font-family="Inter" font-weight="700" font-size="34" letter-spacing="3" fill="#fff">{t}</text></g>\n'
svg += "      </svg>"
scene("s02", 4.0, "", f"""{stage("s02-stage", full=False, extra=svg)}
    <div class="kicker" id="s02-kick" style="top:250px">Before</div>
    <div class="headline" id="s02-head" style="top:300px; font-size:96px"><span class="ln">Tanpa</span><span class="ln">aksesori</span></div>""", """
    tl.fromTo("#s02-stage", F(0.78, 800, 470, 540, 860), { ...F(0.86, 800, 490, 540, 880), duration: 4.0, ease: "sine.inOut" }, 0);
    tl.fromTo("#s02-kick", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.05);
    tl.fromTo("#s02-head .ln", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.08, ease: "power4.out" }, 0.1);
    ["a", "b", "c"].forEach((k, i) => {
      tl.fromTo(`#s02-box-${k}`, { opacity: 0, scale: 1.06, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, 1.0 + i * 0.45);
      tl.fromTo(`#s02-lab-${k}`, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 1.1 + i * 0.45);
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
    f'        <rect id="s03-o-{k}" x="{a}" y="{b}" width="{c-a}" height="{d-b}" fill="none" stroke="{BRASS}" stroke-width="3" />'
    for k, (a, b, c, d) in regions.items()) + "\n      </svg>"
steps = "".join(f'<span class="step" id="s03-st{i}"><b>0{i}</b>{n}</span>' for i, n in enumerate(["Groove line", "Batu hiasan", "Cornice", "Concrete slab"], 1))
scene("s03", 5.0, f"""
    #s03-full {{ opacity: 0; }}
    #root .steps {{ position: absolute; left: 70px; right: 70px; top: 455px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px 18px; }}
    #root .step {{ display: flex; align-items: center; gap: 14px; padding: 14px 20px; border: 1.5px solid rgba(28,30,33,.25);
      border-radius: 4px; font-weight: 700; font-size: 28px; letter-spacing: .12em; text-transform: uppercase; color: rgba(28,30,33,.35); background: rgba(250,250,249,.7); }}
    #root .step b {{ font-weight: 900; color: rgba(168,135,90,.45); }}
""", f"""{stage("s03-stage", extra=layers + chr(10) + outl)}
    <div class="headline" id="s03-head" style="top:250px"><span class="ln">Bila tambah</span><span class="ln">aksesori…</span></div>
    <div class="steps" id="s03-steps">{steps}</div>""", f"""
    const RG = {json.dumps(regions)};
    tl.fromTo("#s03-stage", F(0.70, 800, 470, 540, 1000), {{ ...F(0.74, 800, 470, 540, 1000), duration: 5.0, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s03-head .ln", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, stagger: 0.08, ease: "power4.out" }}, 0.05);
    tl.fromTo("#s03-steps .step", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.05, ease: "power3.out" }}, 0.3);
    Object.keys(RG).forEach((k) => {{
      const [a, b, c, d] = RG[k];
      tl.set(`#s03-${{k}}`, {{ clipPath: R(a, d, c, d) }}, 0);
      tl.set(`#s03-o-${{k}}`, {{ opacity: 0 }}, 0);
    }});
    const groups = [["g1", "g2", "g3"], ["b1"], ["c1", "c2"], ["k1"]];
    groups.forEach((g, i) => {{
      const t = 1.0 + i * 0.72;
      g.forEach((k, j) => {{
        const [a, b, c, d] = RG[k];
        tl.to(`#s03-${{k}}`, {{ clipPath: R(a, b, c, d), duration: 0.5, ease: "power3.inOut" }}, t + j * 0.08);
        tl.fromTo(`#s03-o-${{k}}`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, t + j * 0.08);
        tl.to(`#s03-o-${{k}}`, {{ opacity: 0, duration: 0.5 }}, t + 0.55);
      }});
      tl.to(`#s03-st${{i + 1}}`, {{ color: "{INK}", borderColor: "{INK}", backgroundColor: "rgba(250,250,249,1)", duration: 0.2 }}, t);
      tl.to(`#s03-st${{i + 1}} b`, {{ color: "{BRASS}", duration: 0.2 }}, t);
    }});
    tl.to("#s03-full", {{ opacity: 1, duration: 0.6, ease: "sine.inOut" }}, 4.0);
""")

# ---------------------------------------------------------------- S04 GROOVE LINE
grooves = [557, 590, 622, 656]
gsvg = '      <svg viewBox="0 0 1600 900">\n' + "\n".join(
    f'        <line class="s04-gl" x1="279" y1="{y}" x2="472" y2="{y}" stroke="#F2E6D2" stroke-width="2.4" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" />'
    for y in grooves) + "\n      </svg>"
scene("s04", 7.0, f"""
    #s04-a {{ position: absolute; inset: 0; }}
    #s04-b {{ position: absolute; inset: 0; opacity: 0; }}
""", f"""    <div id="s04-a">
{stage("s04-stage", plain=False, extra=gsvg)}
{tag("s04", "01", "GROOVE LINE", 250)}
      <svg class="pointer" viewBox="0 0 1080 1920"><line id="s04-ptr" x1="540" y1="345" x2="540" y2="520" stroke="{INK}" stroke-width="2" /><circle id="s04-dot" cx="540" cy="520" r="7" fill="{BRASS}" stroke="#fff" stroke-width="2" /></svg>
    </div>
    <div id="s04-b">
      <div class="win" id="s04-wt" style="top:190px; height:470px">
{stage("s04-st", full=False, cls="stage nomask")}
        <div class="chip" style="left:36px; top:30px">Sebelum</div>
      </div>
      <div class="win" id="s04-wb" style="top:676px; height:470px">
{stage("s04-sb", plain=False, cls="stage nomask")}
        <div class="chip" style="left:36px; top:30px; background:{BRASS}">Selepas</div>
      </div>
    </div>""", """
    tl.fromTo("#s04-stage", F(1.4, 372, 600, 540, 860), { ...F(2.7, 372, 600, 540, 860), duration: 0.55, ease: "expo.out" }, 0);
    tl.to("#s04-stage", { ...F(2.85, 380, 605, 540, 860), duration: 3.0, ease: "sine.inOut" }, 0.55);
    tl.fromTo("#s04-tag", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.35);
    tl.fromTo("#s04-ptr", { attr: { y2: 345 } }, { attr: { y2: 520 }, duration: 0.4, ease: "power2.out" }, 0.6);
    tl.fromTo("#s04-dot", { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 0.95);
    tl.to("#s04-stage .s04-gl", { strokeDashoffset: 0, duration: 0.7, stagger: 0.18, ease: "power2.inOut" }, 1.1);
    tl.to("#s04-stage .s04-gl", { opacity: 0.35, duration: 0.6 }, 2.6);
    // before / after stack
    tl.set("#s04-a", { opacity: 0 }, 3.6);
    tl.set("#s04-b", { opacity: 1 }, 3.6);
    tl.set("#s04-st", F(2.2, 380, 600, 540, 235), 3.6);
    tl.set("#s04-sb", F(2.2, 380, 600, 540, 235), 3.6);
    tl.fromTo("#s04-wt", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 3.6);
    tl.fromTo("#s04-wb", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 3.75);
    tl.to("#s04-st", { ...F(2.35, 380, 600, 540, 235), duration: 3.2, ease: "sine.inOut" }, 3.6);
    tl.to("#s04-sb", { ...F(2.35, 380, 600, 540, 235), duration: 3.2, ease: "sine.inOut" }, 3.6);
""")

# ---------------------------------------------------------------- S05 BATU HIASAN
B = regions["b1"]
scene("s05", 6.0, f"""
    #s05-chip-b, #s05-chip-a {{ opacity: 0; }}
    #s05-shine {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; overflow: hidden; }}
    #s05-band {{ position: absolute; left: 0; top: 380px; width: 160px; height: 420px;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.30) 50%, rgba(255,255,255,0)); }}
""", f"""{stage("s05-stage", extra='      <div id="s05-shine"><div id="s05-band"></div></div>')}
{tag("s05", "02", "BATU HIASAN", 250)}
    <svg class="pointer" viewBox="0 0 1080 1920"><polyline id="s05-ptr" points="540,345 540,430 300,430 300,560" fill="none" stroke="{INK}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" /><circle id="s05-dot" cx="300" cy="560" r="7" fill="{BRASS}" stroke="#fff" stroke-width="2" /></svg>
    <div class="chip" id="s05-chip-b" style="left:60px; top:1060px">Sebelum</div>
    <div class="chip" id="s05-chip-a" style="left:60px; top:1060px; background:{BRASS}">Selepas</div>""", f"""
    tl.set("#s05-shine", {{ clipPath: R({B[0]}, {B[1]}, {B[2]}, {B[3]}) }}, 0);
    tl.set("#s05-full", {{ clipPath: "inset(0% 0% 0% 0%)" }}, 0);
    tl.fromTo("#s05-stage", F(1.3, 796, 590, 540, 880), {{ ...F(2.45, 796, 590, 540, 880), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s05-stage", {{ ...F(2.6, 790, 585, 540, 880), duration: 5.4, ease: "sine.inOut" }}, 0.55);
    tl.fromTo("#s05-tag", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 0.35);
    tl.to("#s05-ptr", {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }}, 0.6);
    tl.fromTo("#s05-dot", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 1.05);
    tl.fromTo("#s05-band", {{ x: 520 }}, {{ x: 1000, duration: 1.4, ease: "sine.inOut" }}, 1.3);
    // quick before / after
    tl.to("#s05-full", {{ clipPath: "inset(0% 0% 0% 100%)", duration: 0.45, ease: "power3.inOut" }}, 3.7);
    tl.to("#s05-chip-b", {{ opacity: 1, duration: 0.15 }}, 3.85);
    tl.fromTo("#s05-full", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut", immediateRender: false }}, 4.75);
    tl.to("#s05-chip-b", {{ opacity: 0, duration: 0.1 }}, 4.85);
    tl.to("#s05-chip-a", {{ opacity: 1, duration: 0.15 }}, 4.95);
""")

# ---------------------------------------------------------------- S06 CORNICE
C = (1213, 388, 1426, 550)
csvg = f"""      <svg viewBox="0 0 1600 900">
        <rect id="s06-frame" x="{C[0]}" y="{C[1]}" width="{C[2]-C[0]}" height="{C[3]-C[1]}" fill="none" stroke="#F2E6D2" stroke-width="2.2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" />
        <g id="s06-ticks" stroke="{BRASS}" stroke-width="2.2" vector-effect="non-scaling-stroke">
          <line x1="{C[0]-14}" y1="{C[1]}" x2="{C[0]-4}" y2="{C[1]}" vector-effect="non-scaling-stroke" /><line x1="{C[0]}" y1="{C[1]-14}" x2="{C[0]}" y2="{C[1]-4}" vector-effect="non-scaling-stroke" />
          <line x1="{C[2]+4}" y1="{C[1]}" x2="{C[2]+14}" y2="{C[1]}" vector-effect="non-scaling-stroke" /><line x1="{C[2]}" y1="{C[1]-14}" x2="{C[2]}" y2="{C[1]-4}" vector-effect="non-scaling-stroke" />
          <line x1="{C[0]-14}" y1="{C[3]}" x2="{C[0]-4}" y2="{C[3]}" vector-effect="non-scaling-stroke" /><line x1="{C[0]}" y1="{C[3]+4}" x2="{C[0]}" y2="{C[3]+14}" vector-effect="non-scaling-stroke" />
          <line x1="{C[2]+4}" y1="{C[3]}" x2="{C[2]+14}" y2="{C[3]}" vector-effect="non-scaling-stroke" /><line x1="{C[2]}" y1="{C[3]+4}" x2="{C[2]}" y2="{C[3]+14}" vector-effect="non-scaling-stroke" />
        </g>
      </svg>"""
scene("s06", 6.4, """
    #s06-chip-b, #s06-chip-a, #s06-ticks { opacity: 0; }
""", f"""{stage("s06-stage", extra=csvg)}
{tag("s06", "03", "CORNICE", 250)}
    <svg class="pointer" viewBox="0 0 1080 1920"><line id="s06-ptr" x1="540" y1="345" x2="540" y2="470" stroke="{INK}" stroke-width="2" /><circle id="s06-dot" cx="540" cy="470" r="7" fill="{BRASS}" stroke="#fff" stroke-width="2" /></svg>
    <div class="chip" id="s06-chip-b" style="left:60px; top:1060px">Sebelum</div>
    <div class="chip" id="s06-chip-a" style="left:60px; top:1060px; background:{BRASS}">Selepas</div>""", """
    tl.set("#s06-full", { opacity: 1 }, 0);
    tl.fromTo("#s06-stage", F(1.5, 1320, 470, 540, 800), { ...F(3.0, 1320, 470, 540, 800), duration: 0.55, ease: "expo.out" }, 0);
    tl.to("#s06-stage", { ...F(3.15, 1318, 468, 540, 800), duration: 5.8, ease: "sine.inOut" }, 0.55);
    tl.fromTo("#s06-tag", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.35);
    tl.fromTo("#s06-ptr", { attr: { y2: 345 } }, { attr: { y2: 470 }, duration: 0.35, ease: "power2.out" }, 0.6);
    tl.fromTo("#s06-dot", { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 0.9);
    tl.to("#s06-frame", { strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }, 1.0);
    tl.to("#s06-ticks", { opacity: 1, duration: 0.3 }, 1.8);
    // quick before / after flick
    tl.to(["#s06-frame", "#s06-ticks"], { opacity: 0, duration: 0.2 }, 3.6);
    tl.to("#s06-full", { opacity: 0, duration: 0.18 }, 3.9);
    tl.to("#s06-chip-b", { opacity: 1, duration: 0.12 }, 3.9);
    tl.to("#s06-full", { opacity: 1, duration: 0.18 }, 4.7);
    tl.to("#s06-chip-b", { opacity: 0, duration: 0.08 }, 4.7);
    tl.to("#s06-chip-a", { opacity: 1, duration: 0.12 }, 4.75);
""")

# ---------------------------------------------------------------- S07 CONCRETE SLAB
K = regions["k1"]
scene("s07", 5.6, f"""
    #s07-shadow, #s07-guides, #s07-dim {{ opacity: 0; }}
    #s07-shadow {{ position: absolute; left: {K[0]}px; top: {K[3]}px; width: {K[2]-K[0]}px; height: 40px;
      background: linear-gradient(to bottom, rgba(10,12,14,.55), rgba(10,12,14,0)); transform-origin: 50% 0; }}
    #s07-slab {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; }}
""", f"""{stage("s07-stage", plain=False, extra=f'''      <div id="s07-shadow"></div>
      <img id="s07-slab" src="assets/house-full.jpg" alt="" />
      <svg viewBox="0 0 1600 900">
        <g id="s07-guides" stroke="{BRASS}" stroke-width="2" fill="none" vector-effect="non-scaling-stroke">
          <line x1="{K[0]-40}" y1="{K[1]}" x2="{K[0]-8}" y2="{K[1]}" vector-effect="non-scaling-stroke" /><line x1="{K[0]-40}" y1="{K[3]}" x2="{K[0]-8}" y2="{K[3]}" vector-effect="non-scaling-stroke" />
          <line x1="{K[0]-24}" y1="{K[1]}" x2="{K[0]-24}" y2="{K[3]}" vector-effect="non-scaling-stroke" />
          <line x1="{K[2]+8}" y1="{K[1]}" x2="{K[2]+40}" y2="{K[1]}" vector-effect="non-scaling-stroke" /><line x1="{K[2]+8}" y1="{K[3]}" x2="{K[2]+40}" y2="{K[3]}" vector-effect="non-scaling-stroke" />
          <line x1="{K[2]+24}" y1="{K[1]}" x2="{K[2]+24}" y2="{K[3]}" vector-effect="non-scaling-stroke" />
        </g>
      </svg>''')}
{tag("s07", "04", "CONCRETE SLAB", 250)}
    <svg class="pointer" viewBox="0 0 1080 1920"><line id="s07-ptr" x1="540" y1="345" x2="540" y2="560" stroke="{INK}" stroke-width="2" /><circle id="s07-dot" cx="540" cy="560" r="7" fill="{BRASS}" stroke="#fff" stroke-width="2" /></svg>
    <div class="tagwrap" style="top:1060px"><div class="chip" id="s07-dim" style="position:static; font-size:30px; background:{BRASS}">Lebih berdimensi</div></div>""", f"""
    tl.set("#s07-slab", {{ clipPath: R({K[0]}, {K[1]}, {K[2]}, {K[3]}) }}, 0);
    tl.fromTo("#s07-stage", F(1.2, 796, 470, 540, 760), {{ ...F(2.2, 796, 470, 540, 760), duration: 0.55, ease: "expo.out" }}, 0);
    tl.to("#s07-stage", {{ ...F(2.3, 796, 468, 540, 760), duration: 5.0, ease: "sine.inOut" }}, 0.55);
    tl.fromTo("#s07-tag", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 0.35);
    tl.fromTo("#s07-ptr", {{ attr: {{ y2: 345 }} }}, {{ attr: {{ y2: 560 }}, duration: 0.4, ease: "power2.out" }}, 0.6);
    tl.fromTo("#s07-dot", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 0.95);
    // lift the slab off the facade: shadow and layering
    tl.fromTo("#s07-slab", {{ y: 0 }}, {{ y: -7, duration: 0.9, ease: "power3.out" }}, 1.3);
    tl.to("#s07-shadow", {{ opacity: 0.85, duration: 0.9, ease: "power2.out" }}, 1.3);
    tl.to("#s07-guides", {{ opacity: 1, duration: 0.4 }}, 1.6);
    tl.fromTo("#s07-dim", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 1.9);
    tl.to("#s07-slab", {{ y: 0, duration: 0.8, ease: "power2.inOut" }}, 4.4);
    tl.to("#s07-shadow", {{ opacity: 0, duration: 0.8 }}, 4.4);
""")

# ---------------------------------------------------------------- S08 BEFORE vs AFTER slider
scene("s08", 4.0, f"""
    #s08-handle {{ position: absolute; left: 0; top: 0; width: 1600px; height: 900px; }}
    #s08-bar {{ position: absolute; left: -2px; top: 60px; width: 4px; height: 780px; background: #fff; box-shadow: 0 0 0 1px rgba(28,30,33,.25); }}
    #s08-knob {{ position: absolute; left: -38px; top: 412px; width: 76px; height: 76px; border-radius: 50%; background: #fff;
      border: 2px solid {INK}; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 30px; color: {INK}; letter-spacing: 4px; }}
""", f"""{stage("s08-stage", extra='      <div id="s08-handle"><div id="s08-bar"></div><div id="s08-knob">‹›</div></div>')}
    <div class="headline" id="s08-head" style="top:260px; font-size:96px">Before <span style="color:{BRASS_T}; font-weight:400">vs</span> After</div>
    <div class="chip" id="s08-cb" style="left:60px; top:470px">Before</div>
    <div class="chip" id="s08-ca" style="right:60px; top:470px; background:{BRASS}">After</div>""", """
    tl.set("#s08-stage", F(0.68, 800, 470, 540, 840), 0);
    tl.to("#s08-stage", { ...F(0.71, 800, 470, 540, 840), duration: 4.0, ease: "sine.inOut" }, 0);
    tl.fromTo("#s08-full", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 50%)", duration: 0.8, ease: "power3.inOut" }, 0.2);
    tl.fromTo("#s08-handle", { x: 1600 }, { x: 800, duration: 0.8, ease: "power3.inOut" }, 0.2);
    tl.to("#s08-full", { clipPath: "inset(0% 0% 0% 22%)", duration: 0.7, ease: "power2.inOut" }, 1.5);
    tl.to("#s08-handle", { x: 352, duration: 0.7, ease: "power2.inOut" }, 1.5);
    tl.to("#s08-full", { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power3.inOut" }, 2.6);
    tl.to("#s08-handle", { x: -40, opacity: 0, duration: 0.7, ease: "power3.inOut" }, 2.6);
    tl.fromTo("#s08-head", { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power4.out" }, 0.05);
    tl.fromTo(["#s08-cb", "#s08-ca"], { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.1 }, 0.5);
    tl.to("#s08-cb", { opacity: 0, duration: 0.3 }, 2.7);
""")

# ---------------------------------------------------------------- S09 BUDGET
scene("s09", 4.0, f"""
    #s09-rule {{ position: absolute; left: 300px; top: 532px; width: 480px; height: 6px; background: {BRASS}; transform-origin: 0 50%; }}
""", f"""{stage("s09-stage", plain=False)}
    <div class="headline" id="s09-head" style="top:230px; font-size:92px">
      <span class="ln">Lebih detail</span><span class="ln" style="color:{BRASS_T}; font-weight:400">=</span><span class="ln">Lebih bajet</span>
    </div>
    <div id="s09-rule"></div>""", """
    tl.fromTo("#s09-stage", F(0.70, 800, 470, 540, 940), { ...F(0.76, 800, 470, 540, 940), duration: 4.0, ease: "sine.inOut" }, 0);
    tl.fromTo("#s09-head .ln", { opacity: 0, y: 46 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.22, ease: "power4.out" }, 0.1);
    tl.fromTo("#s09-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.inOut" }, 1.0);
""")

# ---------------------------------------------------------------- S10 SIMPLE vs FULL
scene("s10", 4.6, f"""
    #s10-vs {{ position: absolute; left: 480px; top: 620px; width: 120px; height: 120px; border-radius: 50%; background: {INK};
      color: #fff; font-weight: 900; font-size: 44px; display: flex; align-items: center; justify-content: center; border: 6px solid {PAPER}; }}
""", f"""    <div class="win" id="s10-wt" style="top:190px; height:480px">
{stage("s10-st", full=False, cls="stage nomask")}
      <div class="chip light" style="left:36px; bottom:28px">Simple</div>
    </div>
    <div class="win" id="s10-wb" style="top:690px; height:480px">
{stage("s10-sb", plain=False, cls="stage nomask")}
      <div class="chip" style="right:36px; bottom:28px; background:{BRASS}">Full accessories</div>
    </div>
    <div id="s10-vs">VS</div>""", """
    tl.fromTo("#s10-st", F(0.70, 800, 470, 540, 240), { ...F(0.75, 800, 470, 540, 240), duration: 4.6, ease: "sine.inOut" }, 0);
    tl.fromTo("#s10-sb", F(0.75, 800, 470, 540, 240), { ...F(0.70, 800, 470, 540, 240), duration: 4.6, ease: "sine.inOut" }, 0);
    tl.fromTo("#s10-wt", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }, 0);
    tl.fromTo("#s10-wb", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.55, ease: "power3.inOut" }, 0.15);
    tl.fromTo("#s10-vs", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 0.6);
""")

# ---------------------------------------------------------------- S11 EMOTIONAL ENDING
scene("s11", 5.8, f"""
    #s11-rule {{ position: absolute; left: 470px; top: 372px; width: 140px; height: 2px; background: {BRASS}; transform-origin: 50% 50%; }}
    #s11-l1 {{ top: 250px; font-size: 64px; font-weight: 400; letter-spacing: 0.06em; }}
    #s11-l2 {{ top: 404px; font-size: 92px; }}
""", f"""{stage("s11-stage", plain=False)}
    <div class="headline" id="s11-l1">Rumah sekali bina.</div>
    <div id="s11-rule"></div>
    <div class="headline" id="s11-l2">Biar puas hati.</div>""", """
    tl.fromTo("#s11-stage", F(0.70, 800, 480, 540, 960), { ...F(0.86, 800, 480, 540, 960), duration: 5.8, ease: "sine.inOut" }, 0);
    tl.fromTo("#s11-l1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, 0.3);
    tl.fromTo("#s11-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.inOut" }, 1.1);
    tl.fromTo("#s11-l2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power4.out" }, 3.2);
""")

# ---------------------------------------------------------------- S12 CTA
scene("s12", 6.0, f"""
    #s12-or {{ position: absolute; left: 0; right: 0; top: 618px; text-align: center; font-weight: 400; font-size: 40px; letter-spacing: .3em; color: {STONE}; }}
    #s12-q1, #s12-q2 {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 900; font-size: 54px; text-transform: uppercase; letter-spacing: -0.01em; }}
    #s12-cta {{ position: absolute; left: 90px; right: 90px; top: 560px; padding: 54px 40px 46px; background: {INK}; border-radius: 10px; text-align: center; color: #fff;
      box-shadow: 0 30px 70px rgba(10,12,14,.35); }}
    #s12-cta .t {{ font-weight: 900; font-size: 64px; line-height: 1.05; text-transform: uppercase; letter-spacing: -0.01em; }}
    #s12-cta .s {{ margin-top: 14px; font-weight: 700; font-size: 30px; letter-spacing: .26em; color: {BRASS}; text-transform: uppercase; }}
    #s12-arrow {{ display: block; margin: 26px auto 0; }}
""", f"""    <div id="s12-pair">
      <div class="win" id="s12-wt" style="top:244px; height:360px">
{stage("s12-st", full=False, cls="stage nomask")}
      </div>
      <div class="win" id="s12-wb" style="top:684px; height:360px">
{stage("s12-sb", plain=False, cls="stage nomask")}
      </div>
      <div id="s12-q1" style="top:176px">Team jimat bajet?</div>
      <div id="s12-or">atau</div>
      <div id="s12-q2" style="top:1058px; color:{BRASS_T}">Team puas hati?</div>
    </div>
    <div id="s12-cta" data-layout-allow-overlap data-layout-allow-occlusion>
      <div class="t">Komen pilihan<br />korang</div>
      <div class="s">Jimat bajet / Puas hati</div>
      <svg id="s12-arrow" width="56" height="70" viewBox="0 0 56 70"><path d="M28 4 V60 M8 42 L28 62 L48 42" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /></svg>
    </div>""", """
    tl.set("#s12-st", F(0.69, 800, 480, 540, 190), 0);
    tl.set("#s12-sb", F(0.69, 800, 480, 540, 190), 0);
    tl.to("#s12-st", { ...F(0.72, 800, 480, 540, 190), duration: 6, ease: "sine.inOut" }, 0);
    tl.to("#s12-sb", { ...F(0.72, 800, 480, 540, 190), duration: 6, ease: "sine.inOut" }, 0);
    tl.fromTo("#s12-wt", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 0);
    tl.fromTo("#s12-wb", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 0.1);
    tl.fromTo("#s12-q1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.4);
    tl.fromTo("#s12-or", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.9);
    tl.fromTo("#s12-q2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 1.2);
    tl.to("#s12-pair", { opacity: 0.18, duration: 0.5 }, 3.2);
    tl.fromTo("#s12-cta", { opacity: 0, y: 40, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power4.out" }, 3.3);
    tl.fromTo("#s12-arrow", { y: 0 }, { y: 12, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 4 }, 3.8);
""")

# ---------------------------------------------------------------- CAPTIONS
CAPS = [
    (0.2, 4.3, "Apa jadi kalau rumah ni kita buang semua aksesori dia?"),
    (4.7, 3.8, "Haa, cuba tengok! Nampak hambar dan tak berseri langsung kan?"),
    (8.7, 4.8, "Tapi bila kita tambahkan aksesori satu per satu, terus berubah rupa rumah!"),
    (13.7, 1.6, "Yang pertama, groove line!"),
    (15.4, 5.1, "Garisan dekat dinding ni buat rumah nampak lebih menarik dan tak terlalu plain."),
    (20.7, 1.6, "Yang kedua, batu hiasan!"),
    (22.4, 4.1, "Batu dekat bahagian pintu masuk ni buat rumah nampak lebih eksklusif."),
    (26.7, 1.6, "Yang ketiga, cornice!"),
    (28.4, 4.5, "Kemasan dekat tingkap ni pula buat design rumah nampak lebih kemas dan menyerlah."),
    (33.1, 1.7, "Dan yang keempat, concrete slab!"),
    (34.9, 3.6, "Elemen ni buat fasad rumah nampak lebih berdimensi."),
    (38.7, 3.8, "Haa, nampak tak beza dia?"),
    (42.7, 3.8, "Tapi nak tambah aksesori ni, mestilah kena tambah bajet juga!"),
    (46.7, 4.4, "Jadi, korang sanggup tambah bajet atau cukup rumah yang simple?"),
    (51.3, 3.0, "Sebab rumah ni kita bina sekali je seumur hidup."),
    (54.4, 2.5, "Kalau dah buat, biarlah sedap mata memandang!"),
    (57.1, 2.8, "Nak jimat bajet atau nak puas hati setiap kali tengok rumah sendiri?"),
    (60.0, 2.9, "Korang team mana? Cuba komen dekat bawah!"),
]
cap_html = "\n".join(
    f'    <div class="cap clip" id="cap-{i:02d}" data-start="{s}" data-duration="{d}"><span class="pill">{t}</span></div>'
    for i, (s, d, t) in enumerate(CAPS, 1))
cap_js = "\n".join(
    f'    tl.fromTo("#cap-{i:02d} .pill", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }}, {s});'
    for i, (s, d, t) in enumerate(CAPS, 1))
with open(f"{OUT}/compositions/captions.html", "w") as f:
    f.write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: Inter, sans-serif; }}
    #root .cap {{ position: absolute; left: 80px; right: 80px; top: 1170px; text-align: center; }}
    #root .pill {{ display: inline-block; padding: 16px 28px; background: rgba(24,26,29,.95); color: #fff; border-radius: 14px;
      font-weight: 700; font-size: 40px; line-height: 1.28; letter-spacing: -0.005em; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="63">
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
SCENES = [("s01", 0, 4.6), ("s02", 4.6, 4.0), ("s03", 8.6, 5.0), ("s04", 13.6, 7.0), ("s05", 20.6, 6.0), ("s06", 26.6, 6.4),
          ("s07", 33.0, 5.6), ("s08", 38.6, 4.0), ("s09", 42.6, 4.0), ("s10", 46.6, 4.6), ("s11", 51.2, 5.8), ("s12", 57.0, 6.0)]
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    for c, s, d in SCENES)

# sound: (id, file, start, volume)
SFX = [
    ("sx-hook-wipe", "whoosh-short", 2.38, 0.55), ("sx-hook-hit", "impact-bass-1", 2.93, 0.75),
    ("sx-plain-a", "click-soft", 5.6, 0.45), ("sx-plain-b", "click-soft", 6.05, 0.4), ("sx-plain-c", "click-soft", 6.5, 0.45),
    ("sx-tr-1", "click", 9.6, 0.4), ("sx-tr-2", "key-press", 10.32, 0.5), ("sx-tr-3", "click", 11.04, 0.4), ("sx-tr-4", "key-press", 11.76, 0.5),
    ("sx-tr-sp", "sparkle", 12.55, 0.3),
    ("sx-01-in", "whoosh", 13.58, 0.5), ("sx-01-tag", "click-soft", 13.95, 0.45), ("sx-01-trace", "sparkle", 14.7, 0.25), ("sx-01-split", "whoosh-short", 17.18, 0.45),
    ("sx-02-in", "whoosh-short", 20.58, 0.5), ("sx-02-tag", "click-soft", 20.95, 0.45), ("sx-02-shine", "sparkle", 21.9, 0.3),
    ("sx-02-b", "whoosh", 24.3, 0.35), ("sx-02-a", "whoosh-short", 25.35, 0.35),
    ("sx-03-in", "whoosh", 26.58, 0.5), ("sx-03-tag", "click-soft", 26.95, 0.45), ("sx-03-trace", "sparkle", 27.6, 0.25),
    ("sx-03-b", "click", 30.5, 0.35), ("sx-03-a", "click", 31.3, 0.35),
    ("sx-04-in", "whoosh-short", 32.98, 0.5), ("sx-04-tag", "click-soft", 33.35, 0.45), ("sx-04-lift", "pop", 34.3, 0.35),
    ("sx-reveal", "impact-bass-2", 38.65, 0.8), ("sx-slide-1", "whoosh-short", 40.1, 0.3), ("sx-slide-2", "whoosh", 41.2, 0.35),
    ("sx-budget", "click-soft", 43.6, 0.4),
    ("sx-split", "whoosh", 46.58, 0.45), ("sx-vs", "pop", 47.2, 0.4),
    ("sx-end", "whoosh-cinematic", 51.0, 0.35), ("sx-end-2", "click-soft", 54.4, 0.35),
    ("sx-cta-in", "whoosh-short", 56.98, 0.45), ("sx-cta", "pop", 60.3, 0.45),
]
DUR = {"click-soft": 0.36, "click": 0.36, "impact-bass-1": 2.1, "impact-bass-2": 2.55, "key-press": 0.43, "pop": 0.72,
       "sparkle": 1.8, "whoosh-cinematic": 5.5, "whoosh-short": 0.57, "whoosh": 0.57}
audio = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{s}" data-duration="{DUR[f]}" data-track-index="{3 + n % 3}" data-volume="{v}"></audio>'
    for n, (i, f, s, v) in enumerate(SFX))

with open(f"{OUT}/index.html", "w") as f:
    f.write(f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {PAPER}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {PAPER}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="63" data-width="1080" data-height="1920">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="63" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
{audio}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok")
