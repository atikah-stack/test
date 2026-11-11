# Builds index.html (shots, punch-ins, tracked dashed circles, flashes) and compositions/text.html (titles, chips, stickers).
import json, sys
S = sys.argv[1]
shots = [("h01",60,1.4,(1.0,1.06),"45% 55%","sine.inOut"),("p01",28,2.2,(1.06,1.0),"50% 50%","power2.out"),
 ("p02",31,2.6,(1.0,1.05),"45% 60%","none"),("p03",34,2.6,(1.06,1.0),"50% 45%","power2.out"),
 ("d01",31,2.6,(1.0,1.04),"55% 45%","none"),("d02",61,2.2,(1.0,1.04),"58% 57%","sine.inOut"),
 ("i01",27,2.2,(1.04,1.0),"60% 40%","power2.out"),("i02",36,2.6,(1.0,1.05),"50% 50%","none"),
 ("i03",27,2.2,(1.06,1.0),"60% 45%","power2.out"),("x01",48,1.6,(1.0,1.1),"52% 34%","sine.inOut"),
 ("x02",42,1.6,(1.0,1.05),"45% 40%","none"),("b01",60,1.6,(1.0,1.06),"50% 60%","sine.inOut"),
 ("m01",48,1.6,(1.0,1.08),"55% 66%","sine.inOut"),("c01",60,1.6,(1.05,1.0),"50% 50%","power2.out")]
circles = {"d02": dict(f0=20, f1=50, r=215, label="magnetic compatible 🧲", dy=-270),
           "x01": dict(f0=2, f1=46, r=235, label="0.8mm raised lens protection 📸", dy=280),
           "m01": dict(f0=8, f1=46, r=205, label="dustproof mesh 🫧", dy=-250, oy=-28)}
start = {}; t = 0
for s in shots: start[s[0]] = t; t += s[1]
total = round(t / 30, 4); T = lambda f: round(f / 30, 4)
html, js = [], []
for i, (sid, fr, vol, (a, b), org, ease) in enumerate(shots):
    st, du = T(start[sid]), T(fr)
    inner = f'        <video id="v-{sid}" class="clip shot" src="assets/shots/{sid}.mp4" data-start="{st}" data-duration="{du}" data-track-index="1" data-has-audio="true" data-volume="{vol}" playsinline></video>'
    js.append(f'      tl.fromTo("#f-{sid}", {{ scale: {a}, transformOrigin: "{org}" }}, {{ scale: {b}, duration: {du}, ease: "{ease}" }}, {st});')
    if sid in circles:
        c = circles[sid]; trk = json.load(open(f"{S}/trk-{sid}.json"))
        cs, cd, R = T(start[sid] + c["f0"]), T(c["f1"] - c["f0"]), c["r"]; C = round(6.28318 * R, 1); W = 2 * R + 8
        inner += f'''
        <div id="ring-{sid}" class="ring clip" data-start="{cs}" data-duration="{cd}" data-track-index="3" data-layout-allow-overflow>
          <div id="ring-{sid}-spin" class="spin" style="width:{W}px;height:{W}px;left:{-R-4}px;top:{-R-4}px">
            <svg width="{W}" height="{W}" viewBox="0 0 {W} {W}">
              <defs><mask id="m-{sid}"><circle id="mk-{sid}" cx="{R+4}" cy="{R+4}" r="{R}" fill="none" stroke="#fff" stroke-width="10" stroke-dasharray="{C}" stroke-dashoffset="{C}" transform="rotate(-90 {R+4} {R+4})"/></mask></defs>
              <circle cx="{R+4}" cy="{R+4}" r="{R}" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-dasharray="11 9" stroke-linecap="round" mask="url(#m-{sid})"/>
            </svg>
          </div>
          <div id="lab-{sid}" class="lab" style="top:{c['dy']-28}px"><span class="chip">{c['label']}</span></div>
        </div>'''
        oy = c.get("oy", 0); x0, y0 = trk[c["f0"]]; y0 += oy
        js.append(f'      tl.set("#ring-{sid}", {{ x: {x0}, y: {y0} }}, {cs});')
        for f in range(c["f0"] + 1, min(c["f1"], len(trk))):
            x, y = trk[f]; y += oy; js.append(f'      tl.to("#ring-{sid}", {{ x: {x}, y: {y}, duration: 0.0333, ease: "none" }}, {T(start[sid] + f - 1)});')
        js.append(f'      tl.fromTo("#mk-{sid}", {{ attr: {{ "stroke-dashoffset": {C} }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.45, ease: "power2.inOut" }}, {cs});')
        js.append(f'      tl.fromTo("#ring-{sid}-spin", {{ rotation: 0, scale: 0.9 }}, {{ rotation: 40, scale: 1, duration: {cd}, ease: "none" }}, {cs});')
        js.append(f'      tl.fromTo("#lab-{sid} .chip", {{ opacity: 0, scale: 0.6, y: 14 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }}, {round(cs + 0.18, 4)});')
        js.append(f'      tl.to("#ring-{sid}-spin, #lab-{sid} .chip", {{ opacity: 0, scale: 0.92, duration: 0.16, ease: "power2.in" }}, {round(cs + cd - 0.17, 4)});')
    html.append(f'      <div class="frame" id="f-{sid}" style="z-index:{i+1}">\n{inner}\n      </div>')
# soft white flashes on three seams
flashes = [start["p01"], start["i01"], start["b01"], start["c01"]]
html.append('      <div id="flash" class="flash clip" data-start="0" data-duration="%s" data-track-index="4" style="z-index:40"></div>' % total)
js.append('      tl.set("#flash", { opacity: 0 }, 0);')
for f in flashes:
    js.append(f'      tl.fromTo("#flash", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.28, ease: "power2.out" }}, {T(f)});')
page = f'''<!doctype html>
<html lang="ms" data-composition-variables='[{{"id":"showCta","type":"boolean","label":"Show bakul kuning line (only if linked in TikTok Shop)","default":true}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Noto Color Emoji"; src: url("assets/fonts/NotoColorEmoji.ttf") format("truetype"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #f4ece2; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .frame {{ position: absolute; inset: 0; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .ring {{ position: absolute; left: 0; top: 0; width: 0; height: 0; }}
      .spin {{ position: absolute; filter: drop-shadow(0 1px 3px rgba(40,28,20,.45)); }}
      .lab {{ position: absolute; left: -400px; width: 800px; display: flex; justify-content: center; }}
      .chip {{ display: inline-block; padding: 12px 26px; border-radius: 999px; background: rgba(255, 249, 240, 0.9); color: #5a4033;
        font-family: "Inter", "Noto Color Emoji", sans-serif; font-weight: 600; font-size: 31px; white-space: nowrap; box-shadow: 0 6px 20px rgba(60,40,28,.18); }}
      .flash {{ position: absolute; inset: 0; background: #fff8ee; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(html)}
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
# ---- text / chips / stickers ----
chips = [  # id, shot, offset s, dur s, text, top px
 ("box", "p01", 0.08, 0.82, "unboxing time 📦", 1180),
 ("asmr", "p02", 0.1, 0.88, "so satisfying 🤤", 1180),
 ("inside", "p03", 0.1, 1.0, "what's inside? 👀", 1180),
 ("crys", "d01", 0.05, 0.95, "crystal clear 💎", 1180),
 ("before", "i01", 0.05, 0.82, "before 🤍", 1180),
 ("fit", "i02", 0.1, 1.05, "fits perfectly ✨", 1180),
 ("fp", "i03", 0.03, 0.85, "anti-fingerprint 🫶", 1180),
 ("btn", "x02", 0.05, 1.3, "clear side buttons ✨", 1080),
 ("scr", "b01", 0.05, 0.85, "scratch-resistant 💪", 1180),
]
blocks, tw = [], []
for cid, sid, off, du, txt, top in chips:
    st = round(start[sid] / 30 + off, 3)
    blocks.append(f'    <div id="c-{cid}" class="blk clip" data-start="{st}" data-duration="{du}" data-track-index="1" style="top:{top}px"><span class="chip" id="c-{cid}-i">{txt}</span></div>')
    tw.append(f'      pop("#c-{cid}-i", {st}); out("#c-{cid}-i", {round(st + du - 0.15, 3)});')
b1, c1 = start["b01"] / 30, start["c01"] / 30
txt = f'''<template>
  <style>
    @font-face {{ font-family: "Nunito"; font-weight: 800; src: url("assets/fonts/nunito-latin-800-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
    @font-face {{ font-family: "Noto Color Emoji"; src: url("assets/fonts/NotoColorEmoji.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; }}
    .blk {{ position: absolute; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .title {{ font-family: "Nunito", sans-serif; font-weight: 800; font-size: 132px; line-height: 1; letter-spacing: -0.02em; color: #ffffff; text-shadow: 0 3px 22px rgba(40,28,20,.35); }}
    .sub {{ font-family: "Inter", "Noto Color Emoji", sans-serif; font-weight: 600; font-size: 38px; line-height: 1.25; white-space: nowrap;
      text-shadow: 0 1px 12px rgba(40,28,20,.6), 0 1px 2px rgba(40,28,20,.5); }}
    .yel {{ color: #f5d45e; }} .wht {{ color: #ffffff; }} .cream {{ color: #fff5e8; }}
    .mask {{ overflow: hidden; padding: 0 6px 8px; }}
    .glow {{ position: absolute; left: 50%; top: 50%; width: 900px; height: 470px; margin: -235px 0 0 -450px; z-index: -1; border-radius: 50%;
      background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(38,26,18,.55) 0%, rgba(38,26,18,.26) 50%, rgba(38,26,18,0) 100%); }}
    .glow.sm {{ width: 820px; height: 240px; margin: -120px 0 0 -410px; }}
    .chip {{ display: inline-block; padding: 14px 30px; border-radius: 999px; background: rgba(255,249,240,.92); color: #5a4033;
      font-family: "Inter", "Noto Color Emoji", sans-serif; font-weight: 600; font-size: 36px; white-space: nowrap; box-shadow: 0 8px 22px rgba(60,40,28,.2); }}
    .stk {{ position: absolute; font-family: "Noto Color Emoji"; font-size: 70px; line-height: 1; }}
  </style>
  <div id="root" data-composition-id="text" data-width="1080" data-height="1920">
    <div id="t-hero" class="blk clip" data-start="0" data-duration="1.97" data-track-index="0" style="top: 780px">
      <div class="glow" id="t-hero-g"></div>
      <div class="mask"><div class="title" id="t-hero-0">TORRAS</div></div>
      <div class="sub yel" id="t-hero-1" style="margin-top: 10px">anti-yellowing 🌼</div>
      <div class="sub wht" id="t-hero-2">clear magnetic case 🧲</div>
    </div>
    <div id="s-hero" class="clip" data-start="0" data-duration="1.97" data-track-index="2">
      <div class="stk" id="s-h1" style="left: 150px; top: 700px">✨</div>
      <div class="stk" id="s-h2" style="left: 860px; top: 1010px">🤍</div>
    </div>
{chr(10).join(blocks)}
    <div id="t-pretty" class="blk clip" data-start="{round(b1 + 1.0, 3)}" data-duration="0.97" data-track-index="0" style="top: 1010px">
      <div class="glow sm"></div>
      <div class="sub cream" id="t-pretty-1">clean &amp; pretty ♡ 🌷</div>
    </div>
    <div id="s-pretty" class="clip" data-start="{round(b1 + 1.0, 3)}" data-duration="0.97" data-track-index="2">
      <div class="stk" id="s-p1" style="left: 130px; top: 880px">✨</div>
      <div class="stk" id="s-p2" style="left: 870px; top: 1100px">✨</div>
    </div>
    <div id="t-cta" class="blk clip" data-start="{round(c1 + 0.1, 3)}" data-duration="{round(total - c1 - 0.1, 3)}" data-track-index="0" style="top: 960px">
      <div class="glow sm" id="t-cta-g"></div>
      <div class="sub cream" id="t-cta-0" style="font-family: Nunito, sans-serif; font-weight: 800; font-size: 64px; color: #fff">TORRAS ♡</div>
      <div style="margin-top:14px"><span class="chip" id="t-cta-1">get yours kat bakul kuning 🛒</span></div>
    </div>
    <div id="s-cta" class="clip" data-start="{round(c1 + 0.1, 3)}" data-duration="{round(total - c1 - 0.1, 3)}" data-track-index="2">
      <div class="stk" id="s-c1" style="left: 150px; top: 880px">🎀</div>
      <div class="stk" id="s-c2" style="left: 860px; top: 1110px">✨</div>
    </div>
  </div>
  <script>
    (function () {{
      const vars = (window.__hyperframes && window.__hyperframes.getVariables && window.__hyperframes.getVariables()) || {{}};
      if (vars.showCta === false) document.getElementById("t-cta-1").textContent = "get yours now 🤍";
      const tl = gsap.timeline({{ paused: true }});
      const pop = (sel, at) => tl.fromTo(sel, {{ opacity: 0, scale: 0.6, y: 18 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.8)" }}, at);
      const out = (sel, at) => tl.to(sel, {{ opacity: 0, scale: 0.9, duration: 0.15, ease: "power2.in" }}, at);
      const sticker = (sel, at, rot) => {{
        tl.fromTo(sel, {{ opacity: 0, scale: 0, rotation: -rot }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.2)" }}, at);
        tl.to(sel, {{ scale: 0.85, rotation: rot / 2, duration: 0.5, ease: "sine.inOut" }}, at + 0.45);
      }};
      // hero
      tl.fromTo("#t-hero-g", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0);
      tl.fromTo("#t-hero-0", {{ yPercent: 105 }}, {{ yPercent: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
      tl.fromTo("#t-hero-1, #t-hero-2", {{ opacity: 0, scale: 0.9, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.38, ease: "back.out(1.6)", stagger: 0.12 }}, 0.35);
      sticker("#s-h1", 0.55, 20); sticker("#s-h2", 0.75, -20);
      tl.to("#t-hero-g, #t-hero-0, #t-hero-1, #t-hero-2, #s-h1, #s-h2", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, 1.77);
      // feature chips
{chr(10).join(tw)}
      // beauty + CTA
      pop("#t-pretty-1", {round(b1 + 1.0, 3)}); sticker("#s-p1", {round(b1 + 1.1, 3)}, 25); sticker("#s-p2", {round(b1 + 1.25, 3)}, -25);
      tl.to("#t-pretty-1, #s-p1, #s-p2", {{ opacity: 0, duration: 0.15 }}, {round(b1 + 1.8, 3)});
      tl.fromTo("#t-cta-g", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(c1 + 0.1, 3)});
      tl.fromTo("#t-cta-0", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }}, {round(c1 + 0.1, 3)});
      pop("#t-cta-1", {round(c1 + 0.3, 3)});
      sticker("#s-c1", {round(c1 + 0.45, 3)}, 20); sticker("#s-c2", {round(c1 + 0.6, 3)}, -20);
      window.__timelines["text"] = tl;
    }})();
  </script>
</template>
'''
open("compositions/text.html", "w").write(txt)
print("total", total)
