# TORRAS edit in the "mini fan" reference style: DM Sans, bold uppercase titles with a pink accent,
# word-by-word hook, spaced brand lockup, rotating thin arcs tracked to product details,
# sound-wave doodles, sparkle close with a cream CTA pill. Writes index.html + compositions/text.html.
import json, sys
S = sys.argv[1]
SRC = "assets/even"
PINK, CREAM, INK, WAVE = "#f4afc4", "#fff6ec", "#3a2a24", "#bfd8f2"

shots = [("h01",60,1.4,(1.0,1.06),"45% 55%","sine.inOut"),("p01",28,2.2,(1.06,1.0),"50% 50%","power2.out"),
 ("p02",31,2.6,(1.0,1.05),"45% 60%","none"),("p03",34,2.6,(1.06,1.0),"50% 45%","power2.out"),
 ("d01",31,2.6,(1.0,1.04),"55% 45%","none"),("d02",61,2.2,(1.0,1.04),"58% 57%","sine.inOut"),
 ("i01",27,2.2,(1.04,1.0),"60% 40%","power2.out"),("i02",36,2.6,(1.0,1.05),"50% 50%","none"),
 ("i03",27,2.2,(1.06,1.0),"60% 45%","power2.out"),("x01",48,1.6,(1.0,1.1),"52% 34%","sine.inOut"),
 ("x02",42,1.6,(1.0,1.05),"45% 40%","none"),("b01",60,1.6,(1.0,1.06),"50% 60%","sine.inOut"),
 ("m01",48,1.6,(1.0,1.08),"55% 66%","sine.inOut"),("c01",60,1.6,(1.05,1.0),"50% 50%","power2.out")]
PUNCH = ("p01", "d01", "i01", "x01", "b01", "c01")
arcs = {"d02": dict(f0=18, f1=52, r=210), "x01": dict(f0=2, f1=46, r=235), "m01": dict(f0=6, f1=46, r=200, oy=-28, waves=True)}
start = {}; t = 0
for s_ in shots: start[s_[0]] = t; t += s_[1]
total = round(t / 30, 4); T = lambda f: round(f / 30, 4); sec = lambda sid: start[sid] / 30

# ---------------- index.html ----------------
html, js = [], []
for i, (sid, fr, vol, (a, b), org, ease) in enumerate(shots):
    st, du = T(start[sid]), T(fr)
    inner = f'        <video id="v-{sid}" class="clip shot" src="{SRC}/{sid}.mp4" data-start="{st}" data-duration="{du}" data-track-index="1" data-has-audio="true" data-volume="{vol}" playsinline></video>'
    if sid in PUNCH:
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {round(a*1.12,3)}, transformOrigin: "{org}" }}, {{ scale: {a}, duration: 0.32, ease: "expo.out" }}, {st});')
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {a} }}, {{ scale: {b}, duration: {round(du-0.32,4)}, ease: "{ease}", immediateRender: false }}, {round(st+0.32,4)});')
    else:
        js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {a}, transformOrigin: "{org}" }}, {{ scale: {b}, duration: {du}, ease: "{ease}" }}, {st});')
    if sid in arcs:
        c = arcs[sid]; trk = json.load(open(f"{S}/trk-{sid}.json")); oy = c.get("oy", 0)
        cs, cd, R = T(start[sid] + c["f0"]), T(c["f1"] - c["f0"]), c["r"]; W = 2 * R + 60; C = round(6.28318 * R, 1)
        waves = ""
        if c.get("waves"):
            wl = "".join(f'<path class="wv-{sid}" d="M{x0} {y} q 22 -14 44 0 t 44 0 t 44 0" fill="none" stroke="{WAVE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="26 16"/>'
                         for x0 in (-430, 255) for y in (-40, 0, 40))
            waves = f'<svg class="waves" id="wv-{sid}" width="900" height="200" viewBox="-450 -100 900 200" style="left:-450px; top:-100px">{wl}</svg>'
        inner += f'''
        <div id="arc-{sid}" class="arc clip" data-start="{cs}" data-duration="{cd}" data-track-index="3" data-layout-allow-overflow>
          {waves}
          <svg class="ring2" id="arc2-{sid}" width="{W}" height="{W}" viewBox="0 0 {W} {W}" style="left:{-W//2}px; top:{-W//2}px"><circle cx="{W//2}" cy="{W//2}" r="{R+16}" fill="none" stroke="#ffffff" stroke-opacity="0.35" stroke-width="2"/></svg>
          <svg class="ring1" id="arc1-{sid}" width="{W}" height="{W}" viewBox="0 0 {W} {W}" style="left:{-W//2}px; top:{-W//2}px"><circle id="arcp-{sid}" cx="{W//2}" cy="{W//2}" r="{R}" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="{round(C*0.72,1)} {C}" stroke-dashoffset="{round(C*0.72,1)}" transform="rotate(-90 {W//2} {W//2})"/></svg>
        </div>'''
        x0, y0 = trk[c["f0"]]
        js.append(f'      tl.set("#arc-{sid}", {{ x: {x0}, y: {y0 + oy} }}, {cs});')
        for f in range(c["f0"] + 1, min(c["f1"], len(trk))):
            x, y = trk[f]; js.append(f'      tl.to("#arc-{sid}", {{ x: {x}, y: {y + oy}, duration: 0.0333, ease: "none" }}, {T(start[sid] + f - 1)});')
        js.append(f'      tl.fromTo("#arcp-{sid}", {{ attr: {{ "stroke-dashoffset": {round(C*0.72,1)} }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.5, ease: "power2.out" }}, {cs});')
        js.append(f'      tl.fromTo("#arc1-{sid}", {{ rotation: -20 }}, {{ rotation: 160, duration: {cd}, ease: "none" }}, {cs});')
        js.append(f'      tl.fromTo("#arc2-{sid}", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power2.out" }}, {cs});')
        if c.get("waves"):
            js.append(f'      tl.fromTo("#wv-{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(cs + 0.15, 3)});')
            js.append(f'      tl.fromTo(".wv-{sid}", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": -126 }}, duration: {cd}, ease: "none" }}, {cs});')
        js.append(f'      tl.to("#arc1-{sid}, #arc2-{sid}{", #wv-" + sid if c.get("waves") else ""}", {{ opacity: 0, duration: 0.16, ease: "power2.in" }}, {round(cs + cd - 0.17, 3)});')
    html.append(f'      <div class="frame" id="f-{sid}" style="z-index:{i+1}">\n{inner}\n      </div>')
# static arc around the box logo in p01
html.append(f'''      <div id="arc-box" class="arc clip" data-start="{round(sec('p01')+0.1,3)}" data-duration="0.8" data-track-index="3" style="z-index:30; left:0; top:0" data-layout-allow-overflow>
        <svg class="ring1" id="arc1-box" width="560" height="560" viewBox="0 0 560 560" style="left:250px; top:560px"><circle id="arcp-box" cx="280" cy="280" r="250" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1131 1571" stroke-dashoffset="1131" transform="rotate(-90 280 280)"/></svg>
      </div>''')
bs = round(sec("p01") + 0.1, 3)
js.append(f'      tl.fromTo("#arcp-box", {{ attr: {{ "stroke-dashoffset": 1131 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.45, ease: "power2.out" }}, {bs});')
js.append(f'      tl.fromTo("#arc1-box", {{ rotation: 0 }}, {{ rotation: 90, duration: 0.8, ease: "none" }}, {bs});')
html.append('      <div id="flash" class="flash clip" data-start="0" data-duration="%s" data-track-index="4" style="z-index:40"></div>' % total)
js.append('      tl.set("#flash", { opacity: 0 }, 0);')
for sid in ("p01", "i01", "b01", "c01"):
    js.append(f'      tl.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.26, ease: "power2.out" }}, {T(start[sid])});')

# ---------------- sound effects ----------------
DUR = {"pop": 0.72, "click-soft": 0.366, "sparkle": 1.8, "whoosh-short": 0.575, "whoosh": 0.575, "ping": 1.32}
TRK = {"whoosh": 9, "whoosh-short": 9, "pop": 10, "click-soft": 10, "ping": 11, "sparkle": 12}
sfx = [("whoosh" if k % 2 else "whoosh-short", sec(s_) - 0.2, 0.32) for k, s_ in enumerate(PUNCH)]
sfx += [("ping", (start[s_] + c["f0"]) / 30, 0.45) for s_, c in arcs.items()] + [("ping", bs, 0.4)]

# ---------------- text.html ----------------
blocks, tw = [], []
def words(ids_text, cls=""):
    return " ".join(f'<span class="w {cls}" id="{i}">{w}</span>' for i, w in ids_text)
# hook
hook = [("hk-1", "EH,"), ("hk-2", "CLEAR"), ("hk-3", "CASE"), ("hk-4", "NI")]
blocks.append(f'''    <div id="t-hook" class="blk clip" data-start="0" data-duration="1.95" data-track-index="0" style="top: 250px">
      <div class="h1">{words(hook)}</div>
      <div class="lt" id="hk-sub">cantik gila bila dah pakai 👀</div>
    </div>''')
tw.append('      tl.fromTo("#hk-1, #hk-2, #hk-3, #hk-4", { opacity: 0.25, color: "#9a9a9a", y: 8 }, { opacity: 1, color: "#ffffff", y: 0, duration: 0.3, ease: "power2.out", stagger: 0.14 }, 0.05);')
tw.append('      tl.fromTo("#hk-sub", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.75);')
tw.append('      tl.to("#t-hook .w, #hk-sub", { opacity: 0, duration: 0.16 }, 1.78);')
sfx.append(("pop", 0.05, 0.38)); sfx.append(("click-soft", 0.8, 0.5))
# brand lockup over the box shots
b0, b1 = round(sec("p01") + 0.15, 3), round(sec("p03") - 0.05, 3)
letters = "".join(f'<span class="ltr" id="br-{k}">{ch}</span>' for k, ch in enumerate("TORRAS"))
blocks.append(f'''    <div id="t-brand" class="blk clip" data-start="{b0}" data-duration="{round(b1-b0,3)}" data-track-index="0" style="top: 190px">
      <div class="brand">{letters}</div>
      <div class="pk" id="br-sub">CLEAR MAGNETIC CASE</div>
      <div class="ul" id="br-ul"></div>
    </div>''')
tw.append(f'      tl.fromTo("#t-brand .ltr", {{ opacity: 0, y: 24, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power3.out", stagger: 0.06 }}, {b0});')
tw.append(f'      tl.fromTo("#br-sub", {{ opacity: 0, y: 10, filter: "blur(4px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "power2.out" }}, {round(b0+0.35,3)});')
tw.append(f'      tl.fromTo("#br-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "expo.out" }}, {round(b0+0.55,3)});')
tw.append(f'      tl.to("#t-brand .ltr, #br-sub, #br-ul", {{ opacity: 0, duration: 0.16 }}, {round(b1-0.18,3)});')
sfx.append(("pop", b0, 0.4))
# light line
l0 = round(sec("p03") + 0.05, 3)
blocks.append(f'''    <div id="t-unbox" class="blk clip" data-start="{l0}" data-duration="1.05" data-track-index="0" style="top: 250px">
      <div class="lt big" id="ub-1">unboxing this clear case ♡</div>
      <div class="dash" id="ub-d"></div>
    </div>''')
tw.append(f'      tl.fromTo("#ub-1", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {l0});')
tw.append(f'      tl.fromTo("#ub-d", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "expo.out" }}, {round(l0+0.3,3)});')
tw.append(f'      tl.to("#ub-1, #ub-d", {{ opacity: 0, duration: 0.15 }}, {round(l0+0.88,3)});')
sfx.append(("click-soft", l0, 0.5))
# feature titles with a cycling pink sub-word
feats = [  # id, from shot, to shot (exclusive end at its start), title, sub words, which shot each word lights on
 ("mag", "d01", "i01", "MAGNETIC RING", ["Clear", "Magnetic", "Slim"], None),
 ("col", "i01", "x01", "TRUE-TO-PHONE COLOUR", ["Before", "Fitting", "After"], ["i01", "i02", "i03"]),
 ("lens", "x01", "x02", "0.8MM RAISED LENS", ["Lens", "Camera", "Protection"], None),
 ("btn", "x02", "b01", "CLEAR SIDE BUTTONS", ["Anti-fingerprint", "Scratch-resistant"], None),
 ("yel", "b01", "m01", "ANTI-YELLOWING", ["Crystal", "Clear", "Stays clear longer"], None),
 ("mesh", "m01", "c01", "DUSTPROOF MESH", ["Fine-mesh", "Speaker guard"], None),
]
for fid, a_, b_, title, subs, light_on in feats:
    f0, f1 = round(sec(a_) + 0.08, 3), round(sec(b_) - 0.03, 3)
    sub = " <span class=\"dot\">•</span> ".join(f'<span class="sw" id="{fid}-s{k}">{w}</span>' for k, w in enumerate(subs))
    blocks.append(f'''    <div id="t-{fid}" class="blk clip" data-start="{f0}" data-duration="{round(f1-f0,3)}" data-track-index="0" style="top: 250px">
      <div class="mask"><div class="h1" id="{fid}-t">{title}</div></div>
      <div class="sub" id="{fid}-sub">{sub}</div>
    </div>''')
    tw.append(f'      tl.fromTo("#{fid}-t", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.42, ease: "power3.out" }}, {f0});')
    tw.append(f'      tl.fromTo("#{fid}-sub", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(f0+0.2,3)});')
    n = len(subs); span = (f1 - f0 - 0.35)
    for k in range(n):
        on = round(sec(light_on[k]) + 0.05, 3) if light_on else round(f0 + 0.3 + k * span / n, 3)
        dur = round((sec(light_on[k+1]) + 0.05 if light_on and k + 1 < n else (f0 + 0.3 + (k+1) * span / n if not light_on else f1)) - on - 0.05, 3)
        tw.append(f'      tl.to("#{fid}-s{k}", {{ color: "{PINK}", duration: 0.15 }}, {on}); tl.to("#{fid}-s{k}", {{ color: "#ffffff", duration: 0.15 }}, {round(on + max(0.2, dur), 3)});')
    tw.append(f'      tl.to("#{fid}-t, #{fid}-sub", {{ opacity: 0, duration: 0.15 }}, {round(f1-0.17,3)});')
    sfx.append(("pop" if len(sfx) % 2 else "click-soft", f0, 0.42))
# closing
c0 = round(sec("c01") + 0.1, 3)
STAR = '<svg class="star" id="{i}" style="left:{x}px; top:{y}px" viewBox="0 0 54 54"><path d="M27 4 C 29 20, 34 25, 50 27 C 34 29, 29 34, 27 50 C 25 34, 20 29, 4 27 C 20 25, 25 20, 27 4 Z" fill="#ffffff"/></svg>'
stars = "".join(STAR.format(i=i, x=x, y=y) for i, x, y in [("st1", 830, 210), ("st2", 150, 330), ("st3", 880, 470)])
cw = [("cl-1", "SIMPLE."), ("cl-2", "CLEAR."), ("cl-3", "CANTIK."), ("cl-4", "🤍")]
blocks.append(f'''    <div id="t-close" class="blk clip" data-start="{c0}" data-duration="{round(total-c0,3)}" data-track-index="0" style="top: 230px">
      <div class="h1 big"><span class="w" id="cl-1">SIMPLE.</span> <span class="w pkw" id="cl-2">CLEAR.</span></div>
      <div class="h1 big"><span class="w" id="cl-3">CANTIK.</span> <span class="w" id="cl-4">🤍</span></div>
      <div class="ul wide" id="cl-ul"></div>
    </div>
    <div id="t-stars" class="clip" data-start="{c0}" data-duration="{round(total-c0,3)}" data-track-index="2">{stars}</div>''')
tw.append(f'      tl.fromTo("#cl-1, #cl-2, #cl-3, #cl-4", {{ opacity: 0, y: 16, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.6)", stagger: 0.12 }}, {c0});')
tw.append(f'      tl.fromTo("#cl-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "expo.out" }}, {round(c0+0.5,3)});')
for k, sid_ in enumerate(("st1", "st2", "st3")):
    a0 = round(c0 + 0.4 + k * 0.18, 3)
    tw.append(f'      tl.fromTo("#{sid_}", {{ opacity: 0, scale: 0, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2)" }}, {a0}); tl.to("#{sid_}", {{ scale: 0.55, duration: 0.3, ease: "sine.inOut" }}, {round(a0+0.4,3)}); tl.to("#{sid_}", {{ scale: 1, rotation: 25, duration: 0.3, ease: "sine.inOut" }}, {round(a0+0.7,3)});')
sfx += [("sparkle", c0 + 0.4, 0.34)]

audio = []
for i, (name, at, vol) in enumerate(sorted(sfx, key=lambda x: x[1])):
    at = max(0, round(at, 3)); d = round(min(DUR[name], total - at), 3)
    audio.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{at}" data-duration="{d}" data-track-index="{TRK[name]}" data-volume="{vol}"></audio>')

page = f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #1a1513; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .frame {{ position: absolute; inset: 0; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .arc {{ position: absolute; left: 0; top: 0; width: 0; height: 0; }}
      .ring1, .ring2, .waves {{ position: absolute; overflow: visible; }}
      .flash {{ position: absolute; inset: 0; background: #fff8f2; pointer-events: none; }}
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
'''
open("index.html", "w").write(page)

txt = f'''<template>
  <style>
    @font-face {{ font-family: "DM Sans"; font-weight: 300; src: url("assets/fonts/dm-sans-latin-300-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "DM Sans"; font-weight: 400; src: url("assets/fonts/dm-sans-latin-400-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "DM Sans"; font-weight: 700; src: url("assets/fonts/dm-sans-latin-700-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "Noto Color Emoji"; src: url("assets/fonts/NotoColorEmoji.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; font-family: "DM Sans", "Noto Color Emoji", sans-serif; color: #ffffff; }}
    .blk {{ position: absolute; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .h1 {{ font-weight: 700; font-size: 72px; line-height: 1.08; letter-spacing: -0.01em; white-space: nowrap; text-shadow: 0 2px 10px rgba(0,0,0,.22); }}
    .h1.big {{ font-size: 80px; }}
    .w {{ display: inline-block; }}
    .pkw {{ color: {PINK}; }}
    .mask {{ overflow: hidden; padding: 0 8px 4px; }}
    .lt {{ font-weight: 400; font-size: 44px; letter-spacing: 0.005em; white-space: nowrap; margin-top: 12px; text-shadow: 0 2px 10px rgba(0,0,0,.22); }}
    .lt.big {{ font-size: 54px; margin-top: 0; }}
    .sub {{ font-weight: 400; font-size: 40px; margin-top: 12px; white-space: nowrap; text-shadow: 0 2px 10px rgba(0,0,0,.25); }}
    .sw {{ color: #ffffff; }}
    .dot {{ color: {PINK}; font-size: 26px; vertical-align: middle; margin: 0 6px; }}
    .brand {{ font-weight: 700; font-size: 104px; letter-spacing: 0.22em; margin-right: -0.22em; text-shadow: 0 3px 14px rgba(0,0,0,.3); }}
    .ltr {{ display: inline-block; }}
    .pk {{ color: {PINK}; font-weight: 700; font-size: 40px; letter-spacing: 0.08em; margin-top: 6px; white-space: nowrap; text-shadow: 0 1px 3px rgba(0,0,0,.55), 0 2px 14px rgba(0,0,0,.45); }}
    .ul {{ width: 110px; height: 5px; border-radius: 3px; background: #ffffff; margin-top: 22px; }}
    .ul.wide {{ width: 280px; }}
    .dash {{ width: 28px; height: 5px; border-radius: 3px; background: {PINK}; margin-top: 14px; }}
    .pill {{ display: inline-block; padding: 18px 40px; border-radius: 999px; background: {CREAM}; color: {INK}; font-weight: 400; font-size: 44px; white-space: nowrap; box-shadow: 0 8px 24px rgba(0,0,0,.18); }}
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
'''
open("compositions/text.html", "w").write(txt)
print("total", total, "sfx", len(audio))
