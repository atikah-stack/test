# Pink iPad case edit: builds index.html (shots, tracked product graphics, SFX) and compositions/text.html.
# Run from this folder: python3 build.py <dir with ip-*.json track files>
import json, sys
TRK_DIR = sys.argv[1]
PINK, CREAM, ROSE = "#F4B7CE", "#FFF4E8", "#D7A0B8"
shots = [("s1", 66, 1.0, (1.08, 1.0), "50% 45%", "power2.out"), ("s2", 84, 1.0, (1.0, 1.06), "45% 50%", "sine.inOut"),
         ("s3", 90, 1.2, (1.0, 1.05), "50% 45%", "none"), ("s4", 91, 1.0, (1.0, 1.08), "50% 45%", "sine.inOut"),
         ("s5", 90, 1.2, (1.0, 1.06), "75% 50%", "sine.inOut"), ("s6", 114, 1.0, (1.0, 1.08), "50% 42%", "sine.inOut"),
         ("s7", 84, 1.2, (1.04, 1.0), "50% 50%", "power2.out"), ("s8", 60, 1.0, (1.0, 1.05), "50% 45%", "sine.inOut")]
PUNCH = ("s1", "s3", "s5", "s6", "s8")
start = {}; t = 0
for s_ in shots: start[s_[0]] = t; t += s_[1]
total = round(t / 30, 4); T = lambda f: round(f / 30, 4); sec = lambda sid: start[sid] / 30
html, js = [], []

def tracked(sid, gid, track, ref, f0, f1):
    """Move #gid with the tracked point, relative to its position on the reference frame."""
    rx, ry = track[ref]
    x0, y0 = track[f0]
    js.append(f'      tl.set("#{gid}", {{ x: {round(x0 - rx, 1)}, y: {round(y0 - ry, 1)} }}, {T(start[sid] + f0)});')
    for f in range(f0 + 1, min(f1, len(track))):
        x, y = track[f]
        js.append(f'      tl.to("#{gid}", {{ x: {round(x - rx, 1)}, y: {round(y - ry, 1)}, duration: 0.0333, ease: "none" }}, {T(start[sid] + f - 1)});')

def poly(pts): return " ".join(f"{x},{y}" for x, y in pts)

for i, (sid, fr, vol, (a, b), org, ease) in enumerate(shots):
    st, du = T(start[sid]), T(fr)
    inner = f'        <video id="v-{sid}" class="clip shot" src="assets/shots/{sid}.mp4" data-start="{st}" data-duration="{du}" data-track-index="1" data-has-audio="true" data-volume="{vol}" playsinline></video>'
    if sid in PUNCH:
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {round(a * 1.1, 3)}, transformOrigin: "{org}" }}, {{ scale: {a}, duration: 0.34, ease: "expo.out" }}, {st});')
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {a} }}, {{ scale: {b}, duration: {round(du - 0.34, 4)}, ease: "{ease}", immediateRender: false }}, {round(st + 0.34, 4)});')
    else:
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {a}, transformOrigin: "{org}" }}, {{ scale: {b}, duration: {du}, ease: "{ease}" }}, {st});')
    html.append(f'      <div class="frame" id="f-{sid}" style="z-index:{i + 1}">\n{inner}\n__{sid}__\n      </div>')

# ---- A. geometric line tracing on the cover (s2), lines measured on the frame at a=2.5 s ----
trk = json.load(open(f"{TRK_DIR}/ip-s2.json")); f0, f1 = 4, 80
ridges = [[(175, 262), (320, 470)], [(362, 298), (320, 470)], [(320, 470), (40, 610)], [(320, 480), (268, 700)],
          [(250, 268), (218, 372)], [(218, 372), (128, 560)], [(320, 470), (420, 486)]]
outline = [(160, 243), (430, 300), (330, 718), (30, 640), (160, 243)]
paths = "".join(f'<polyline class="geo" points="{poly([(x * 2, y * 2) for x, y in r])}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for r in ridges)
paths += f'<polyline class="geo geo-o" points="{poly([(x * 2, y * 2) for x, y in outline])}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
gs, gd = T(start["s2"] + f0), T(f1 - f0)
html_s2 = f'''        <div id="geo" class="ov clip" data-start="{gs}" data-duration="{gd}" data-track-index="3" data-layout-allow-overflow>
          <svg id="geo-g" width="1080" height="1920" viewBox="0 0 1080 1920">{paths}</svg>
        </div>'''
tracked("s2", "geo-g", trk, 9, f0, f1)
js.append(f'      tl.fromTo("#geo .geo", {{ attr: {{ "stroke-dashoffset": 1 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.7, ease: "power2.inOut", stagger: 0.09 }}, {gs});')
js.append(f'      tl.to("#geo-g", {{ opacity: 0, duration: 0.25 }}, {round(gs + gd - 0.27, 3)});')

# ---- C. crystal clear back: outline + light sweep tracked to the Apple logo (s1 hook, s6 feature) ----
def crystal(sid, ref, quad, f0, f1, cam=None):
    trk = json.load(open(f"{TRK_DIR}/ip-{sid}.json")); rx, ry = trk[ref]
    q = [(rx + dx, ry + dy) for dx, dy in quad]
    cs, cd = T(start[sid] + f0), T(f1 - f0)
    xs = [p[0] for p in q]; ys = [p[1] for p in q]
    camsvg = ""
    if cam:
        cx, cy = rx + cam[0], ry + cam[1]
        camsvg = f'<circle id="cam-{sid}" cx="{cx}" cy="{cy}" r="78" fill="none" stroke="#fff" stroke-width="3.5" stroke-dasharray="10 9" stroke-linecap="round"/>'
    out = f'''        <div id="cry-{sid}" class="ov clip" data-start="{cs}" data-duration="{cd}" data-track-index="3" data-layout-allow-overflow>
          <svg id="cry-{sid}-g" width="1080" height="1920" viewBox="0 0 1080 1920">
            <defs><clipPath id="clip-{sid}"><polygon points="{poly(q)}"/></clipPath>
              <linearGradient id="sw-{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
            <g clip-path="url(#clip-{sid})"><rect id="swr-{sid}" x="{min(xs) - 260}" y="{min(ys) - 200}" width="200" height="{max(ys) - min(ys) + 400}" fill="url(#sw-{sid})" transform="rotate(18 {min(xs)} {min(ys)})"/></g>
            <polygon id="edge-{sid}" points="{poly(q + [q[0]])}" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
            {camsvg}
          </svg>
        </div>'''
    tracked(sid, f"cry-{sid}-g", trk, ref, f0, f1)
    js.append(f'      tl.fromTo("#edge-{sid}", {{ attr: {{ "stroke-dashoffset": 1 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.8, ease: "power2.inOut" }}, {cs});')
    js.append(f'      tl.fromTo("#swr-{sid}", {{ x: 0 }}, {{ x: {max(xs) - min(xs) + 460}, duration: 1.1, ease: "power2.inOut" }}, {round(cs + 0.15, 3)});')
    if cam:
        js.append(f'      tl.fromTo("#cam-{sid}", {{ opacity: 0, scale: 0.6, rotation: -40, svgOrigin: "{cx} {cy}" }}, {{ opacity: 1, scale: 1, rotation: 40, duration: 1.2, ease: "power2.out", svgOrigin: "{cx} {cy}" }}, {round(cs + 0.5, 3)});')
    js.append(f'      tl.to("#edge-{sid}{", #cam-" + sid if cam else ""}", {{ opacity: 0, duration: 0.25 }}, {round(cs + cd - 0.27, 3)});')
    return out
html_s1 = crystal("s1", 15, [(-150, -424), (440, -200), (90, 600), (-490, 320)], 2, 62)
html_s6 = crystal("s6", 24, [(-180, -520), (490, -360), (230, 610), (-530, 350)], 2, 70, cam=(-150, -470))

# ---- pencil holder: dashed circle + pointer tracked to the cover slot (s5) ----
trk = json.load(open(f"{TRK_DIR}/ip-s5.json")); f0, f1 = 8, 58
rx, ry = trk[51]; ps, pd = T(start["s5"] + f0), T(f1 - f0)
html_s5 = f'''        <div id="pen" class="ov clip" data-start="{ps}" data-duration="{pd}" data-track-index="3" data-layout-allow-overflow>
          <svg id="pen-g" width="1080" height="1920" viewBox="0 0 1080 1920">
            <circle id="pen-c" cx="{rx}" cy="{ry}" r="150" fill="none" stroke="#fff" stroke-width="3.5" stroke-dasharray="11 9" stroke-linecap="round"/>
            <circle id="pen-p" cx="{rx}" cy="{ry}" r="150" fill="none" stroke="{PINK}" stroke-width="2.5"/>
          </svg>
        </div>'''
tracked("s5", "pen-g", trk, 51, f0, f1)
js.append(f'      tl.fromTo("#pen-c", {{ opacity: 0, scale: 0.7, rotation: -60, svgOrigin: "{rx} {ry}" }}, {{ opacity: 1, scale: 1, rotation: 30, duration: {round(pd - 0.25, 3)}, ease: "power2.out", svgOrigin: "{rx} {ry}" }}, {ps});')
js.append(f'      tl.fromTo("#pen-p", {{ opacity: 0.8, scale: 1, svgOrigin: "{rx} {ry}" }}, {{ opacity: 0, scale: 1.35, duration: 0.55, ease: "power2.out", svgOrigin: "{rx} {ry}" }}, {round(ps + 0.4, 3)});')
js.append(f'      tl.fromTo("#pen-p", {{ opacity: 0.8, scale: 1, svgOrigin: "{rx} {ry}" }}, {{ opacity: 0, scale: 1.35, duration: 0.55, ease: "power2.out", svgOrigin: "{rx} {ry}", immediateRender: false }}, {round(ps + 1.0, 3)});')
js.append(f'      tl.to("#pen-c", {{ opacity: 0, duration: 0.2 }}, {round(ps + pd - 0.22, 3)});')

for sid, frag in (("s1", html_s1), ("s2", html_s2), ("s5", html_s5), ("s6", html_s6)):
    html = [h.replace(f"__{sid}__", frag) for h in html]
html = [h.replace(f"__{s_[0]}__\n", "") for h in html for s_ in [None] if True for _ in [0]] if False else html
for s_ in shots: html = [h.replace(f"\n__{s_[0]}__", "") for h in html]

html.append(f'      <div id="flash" class="flash clip" data-start="0" data-duration="{total}" data-track-index="4" style="z-index:40"></div>')
js.append('      tl.set("#flash", { opacity: 0 }, 0);')
for sid in ("s3", "s6", "s8"):
    js.append(f'      tl.fromTo("#flash", {{ opacity: 0.4 }}, {{ opacity: 0, duration: 0.26, ease: "power2.out" }}, {T(start[sid])});')

# ---------------- text ----------------
blocks, tw, sfx = [], [], []
def ww(prefix, words, cls=""):
    return " ".join(f'<span class="w {c}" id="{prefix}-{k}">{w}</span>' for k, (w, c) in enumerate(words))
def scene(bid, s0, s1, top, inner):
    blocks.append(f'    <div id="{bid}" class="blk clip" data-start="{round(s0, 3)}" data-duration="{round(s1 - s0, 3)}" data-track-index="0" style="top:{top}px">\n{inner}\n    </div>')
def words_in(sel, at, stagger=0.09):
    tw.append(f'      tl.fromTo("{sel}", {{ opacity: 0, scale: 0.86, filter: "blur(8px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "power3.out", stagger: {stagger} }}, {round(at, 3)});')
def fade_out(sel, at):
    tw.append(f'      tl.to("{sel}", {{ opacity: 0, filter: "blur(6px)", duration: 0.18, ease: "power2.in" }}, {round(at, 3)});')
def mask_in(sel, at):
    tw.append(f'      tl.fromTo("{sel}", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.45, ease: "power3.out" }}, {round(at, 3)});')
def soft_in(sel, at):
    tw.append(f'      tl.fromTo("{sel}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {round(at, 3)});')
def line_in(sel, at):
    tw.append(f'      tl.fromTo("{sel}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "expo.out" }}, {round(at, 3)});')

# S1 hook
a0, a1 = 0.0, sec("s2") - 0.03
scene("t1", a0, a1, 760, f'''      <div class="hk">{ww("h1", [("case", ""), ("yang", ""), ("buat", ""), ("iPad", ""), ("pink", "hp")])}</div>
      <div class="hk">{ww("h2", [("nampak", ""), ("lagi", ""), ("mahal", ""), ("🩷", "")])}</div>
      <div class="bar" id="h-bar"></div>''')
words_in("#t1 .w", 0.0, 0.08); line_in("#h-bar", 0.8); fade_out("#t1 .w, #h-bar", a1 - 0.2)
sfx += [("pop", 0.0, 0.35), ("click-soft", 0.8, 0.45)]
# S2 design
a0, a1 = sec("s2") + 0.1, sec("s3") - 0.03
scene("t2", a0, a1, 820, f'''      <div class="mask"><div class="hd" id="d-1">the 3-piece case</div></div>
      <div class="sub" id="d-2">MINIMAL · PRETTY · SLIM</div>''')
mask_in("#d-1", a0); soft_in("#d-2", a0 + 0.35); fade_out("#d-1, #d-2", a1 - 0.2)
sfx += [("whoosh-short", a0 - 0.15, 0.25), ("click-soft", a0 + 0.35, 0.45)] + [("ping", T(start["s2"] + 4), 0.3)]
# S3 sleep / wake
a0, a1 = sec("s3") + 0.1, sec("s4") - 0.03
MOON = '<svg class="ic" viewBox="0 0 64 64"><path d="M40 8a24 24 0 1 0 16 40A20 20 0 0 1 40 8z" fill="#fff"/></svg>'
SUN = '<svg class="ic" viewBox="0 0 64 64"><circle cx="32" cy="32" r="11" fill="%s"/>%s</svg>' % (PINK, "".join(f'<line x1="32" y1="6" x2="32" y2="15" stroke="{PINK}" stroke-width="4" stroke-linecap="round" transform="rotate({k*45} 32 32)"/>' for k in range(8)))
ARC = '<svg class="arc" viewBox="0 0 220 90"><path id="sl-arc" d="M12 70 C 60 6, 160 6, 200 60" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="butt" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><path id="sl-head" d="M186 44 L 202 62 L 180 68" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
scene("t3", a0, a1, 760, f'''      <div class="mask"><div class="hd" id="sl-1">smart sleep &amp; wake</div></div>
      <div class="icons"><span id="sl-m">{MOON}</span>{ARC}<span id="sl-s">{SUN}</span></div>
      <div class="sub" id="sl-2">CLOSE TO SLEEP · OPEN TO WAKE</div>''')
mask_in("#sl-1", a0)
tw.append(f'      tl.fromTo("#sl-m", {{ opacity: 0, scale: 0.5, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(1.6)" }}, {round(a0 + 0.3, 3)});')
tw.append(f'      tl.fromTo("#sl-arc", {{ attr: {{ "stroke-dashoffset": 1 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.7, ease: "power2.inOut" }}, {round(a0 + 0.6, 3)});')
tw.append(f'      tl.fromTo("#sl-head", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {round(a0 + 1.25, 3)});')
tw.append(f'      tl.fromTo("#sl-s", {{ opacity: 0, scale: 0.5, rotation: -90 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }}, {round(a0 + 1.3, 3)});')
tw.append(f'      tl.to("#sl-m", {{ opacity: 0.35, duration: 0.4 }}, {round(a0 + 1.3, 3)});')
soft_in("#sl-2", a0 + 0.5); fade_out("#sl-1, #sl-2, .icons", a1 - 0.2)
sfx += [("click-soft", a0 + 0.3, 0.4), ("sparkle", a0 + 1.3, 0.28)]
# S4 one flip
a0, a1 = sec("s4") + 0.15, sec("s5") - 0.03
scene("t4", a0, a1, 820, f'''      <div class="hd">{ww("f1", [("one", ""), ("flip,", "")])}</div>
      <div class="hd">{ww("f2", [("that's", ""), ("it", "pk"), ("✨", "")])}</div>''')
words_in("#t4 .w", a0, 0.12); fade_out("#t4 .w", a1 - 0.2)
sfx += [("pop", a0, 0.35)]
# S5 pencil holder
a0, a1 = sec("s5") + 0.12, sec("s6") - 0.03
scene("t5", a0, a1, 740, f'''      <div class="mask"><div class="hd" id="p-1">pencil holder ✏️</div></div>
      <div class="sub" id="p-2">KEEP EVERYTHING TOGETHER</div>''')
mask_in("#p-1", a0); soft_in("#p-2", a0 + 0.35); fade_out("#p-1, #p-2", a1 - 0.2)
sfx += [("ping", T(start["s5"] + 8), 0.35), ("click-soft", a0 + 0.35, 0.4)]
# S6 clear back
a0, a1 = sec("s6") + 0.15, sec("s7") - 0.03
scene("t6", a0, a1, 760, f'''      <div class="mask"><div class="hd" id="c-1">crystal clear back</div></div>
      <div class="sub" id="c-2">STILL SHOWING OFF MY iPAD COLOUR ♡</div>''')
mask_in("#c-1", a0); soft_in("#c-2", a0 + 0.4); fade_out("#c-1, #c-2", a1 - 0.2)
sfx += [("sparkle", sec("s6") + 0.2, 0.3), ("ping", sec("s6") + 0.6, 0.3)]
# S7 final reveal
a0, a1 = sec("s7") + 0.12, sec("s8") - 0.03
scene("t7", a0, a1, 800, f'''      <div class="hd">{ww("r1", [("iPad", ""), ("pink,", "pk")])}</div>
      <div class="hd">{ww("r2", [("makin", ""), ("cantik", ""), ("🩷", "")])}</div>''')
words_in("#t7 .w", a0, 0.16); fade_out("#t7 .w", a1 - 0.2)
sfx += [("pop", a0, 0.35), ("click-soft", a0 + 0.32, 0.35)]
# S8 CTA
a0, a1 = sec("s8") - 0.12, total
STAR = '<svg class="star" id="{i}" style="left:{x}px; top:{y}px" viewBox="0 0 54 54"><path d="M27 4 C 29 20, 34 25, 50 27 C 34 29, 29 34, 27 50 C 25 34, 20 29, 4 27 C 20 25, 25 20, 27 4 Z" fill="#fff"/></svg>'
scene("t8", a0, a1, 860, f'''      <div class="hd" id="ct-1">team clear case juga? 🩷</div>
      <div class="bar" id="ct-bar"></div>
      <div class="sub" id="ct-2">3-PIECE iPAD CASE · CLEAR BACK</div>''')
blocks.append(f'    <div id="t8s" class="clip" data-start="{round(a0, 3)}" data-duration="{round(a1 - a0, 3)}" data-track-index="2">' +
              "".join(STAR.format(i=i, x=x, y=y) for i, x, y in [("st1", 150, 800), ("st2", 880, 960)]) + '</div>')
tw.append(f'      tl.fromTo("#ct-1", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.5)" }}, {round(a0, 3)});')
line_in("#ct-bar", a0 + 0.3); soft_in("#ct-2", a0 + 0.35)
for k, s_ in enumerate(("st1", "st2")):
    at = round(a0 + 0.4 + 0.2 * k, 3)
    tw.append(f'      tl.fromTo("#{s_}", {{ opacity: 0, scale: 0, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2)" }}, {at}); tl.to("#{s_}", {{ scale: 0.55, rotation: 20, duration: 0.4, ease: "sine.inOut" }}, {round(at + 0.4, 3)});')
sfx += [("whoosh-short", sec("s8") - 0.2, 0.25), ("sparkle", a0 + 0.4, 0.3)]

DUR = {"pop": 0.72, "click-soft": 0.366, "sparkle": 1.8, "whoosh-short": 0.575, "whoosh": 0.575, "ping": 1.32}
TRK = {"whoosh": 9, "whoosh-short": 9, "pop": 10, "click-soft": 11, "ping": 12, "sparkle": 13}
audio = []
for i, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])):
    at = max(0, round(at, 3)); d = round(min(DUR[name], total - at), 3)
    audio.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{at}" data-duration="{d}" data-track-index="{TRK[name]}" data-volume="{vol}"></audio>')

open("index.html", "w").write(f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #171214; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .frame {{ position: absolute; inset: 0; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .ov {{ position: absolute; inset: 0; pointer-events: none; }}
      .ov svg {{ position: absolute; left: 0; top: 0; overflow: visible; }}
      .geo {{ fill: none; stroke: #fff; stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 0 4px rgba(255,255,255,.6)); }}
      .geo-o {{ stroke: {PINK}; stroke-width: 3.5; }}
      .flash {{ position: absolute; inset: 0; background: #fff6f8; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(html)}
{chr(10).join(audio)}
      <div id="text" data-composition-id="text" data-composition-src="compositions/text.html" data-start="0" data-duration="{total}"
        data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:50"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
open("compositions/text.html", "w").write(f'''<template>
  <style>
    @font-face {{ font-family: "Manrope"; font-weight: 800; src: url("assets/fonts/manrope-latin-800-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "DM Sans"; font-weight: 500; src: url("assets/fonts/dm-sans-latin-500-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "Cormorant Garamond"; font-style: italic; font-weight: 500; src: url("assets/fonts/cormorant-garamond-latin-500-italic.woff2") format("woff2"); }}
    @font-face {{ font-family: "Noto Color Emoji"; src: url("assets/fonts/NotoColorEmoji.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; color: #fff; }}
    .blk {{ position: absolute; left: 130px; right: 130px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
    @font-face {{ font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; src: url("assets/fonts/cormorant-garamond-latin-600-italic.woff2") format("woff2"); }}
    .hd {{ font-family: "Cormorant Garamond", "Noto Color Emoji", serif; font-style: italic; font-weight: 600; font-size: 84px; line-height: 1.02; letter-spacing: 0; white-space: nowrap;
      text-shadow: 0 1px 3px rgba(30,15,20,.55), 0 0 14px rgba(30,15,20,.45), 0 4px 22px rgba(30,15,20,.35); }}
    .hd.sm {{ font-size: 72px; line-height: 1.04; }}
    @font-face {{ font-family: "DM Sans"; font-weight: 300; src: url("assets/fonts/dm-sans-latin-300-normal.woff2") format("woff2"); }}
    .hk {{ font-family: "DM Sans", "Noto Color Emoji", sans-serif; font-weight: 300; font-size: 54px; line-height: 1.3; letter-spacing: 0.02em; white-space: nowrap; color: #ffffff;
      text-shadow: 0 1px 3px rgba(30,15,20,.6), 0 0 14px rgba(30,15,20,.45); }}
    .hp {{ color: #FFE1EC; font-weight: 400; }}
    .w {{ display: inline-block; }}
    .pk {{ color: #FFE1EC; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 10px; }}
    .mask {{ overflow: hidden; padding: 0 8px 6px; }}
    .sub {{ font-family: "DM Sans", "Noto Color Emoji", sans-serif; font-weight: 500; font-size: 27px; letter-spacing: 0.24em; margin-right: -0.24em; margin-top: 22px; white-space: nowrap; color: {CREAM};
      text-shadow: 0 1px 2px rgba(30,15,20,.75), 0 0 10px rgba(30,15,20,.6), 0 2px 18px rgba(30,15,20,.45); }}
    .sub.cream {{ color: {CREAM}; }}
    .deco {{ font-family: "Cormorant Garamond", serif; font-style: italic; font-weight: 500; font-size: 64px; color: {PINK}; margin-top: 6px; white-space: nowrap;
      text-shadow: 0 1px 3px rgba(30,15,20,.45), 0 2px 14px rgba(30,15,20,.4); }}
    .bar {{ width: 180px; height: 2px; background: {CREAM}; margin-top: 22px; }}
    .icons {{ display: flex; align-items: center; gap: 10px; margin-top: 18px; filter: drop-shadow(0 2px 8px rgba(30,15,20,.45)); }}
    .ic {{ width: 70px; height: 70px; display: block; }}
    .arc {{ width: 200px; height: 82px; }}
    .star {{ position: absolute; width: 46px; height: 46px; }}
  </style>
  <div id="root" data-composition-id="text" data-width="1080" data-height="1920">
{chr(10).join(blocks)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tw)}
      window.__timelines["text"] = tl;
    }})();
  </script>
</template>
''')
print("total", total, "sfx", len(audio))
