#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman POV comedy
"POV: BILA KONTRAKTOR CAKAP, 'ESOK BOLEH AMBIL KUNCI!'" (1080x1920, 9.2 s).

The original clip plays whole with its own music (lowered). The heading follows the
Mahligai Idaman reference: logo, extra-bold white line, bigger golden-yellow line, dark
outline and soft shadow. Top and bottom 20% stay clear. Times are seconds of the clip.
"""
YEL, WHT, INK = "#FFD23F", "#FFFFFF", "#141414"
SAFE_TOP, SAFE_BOT = 384, 1536
TOTAL = 9.19

# clip moments (from frame stepping): turn 2.6, feet leave the ground 3.4, cuts below
TAKEOFF = 3.40
CUTS = [3.77, 4.41, 4.79, 5.16, 5.52, 5.96, 6.30, 6.64, 7.06, 7.59, 8.18, 8.63]

AUD = []


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{4 + len(AUD) % 3}" data-volume="{v}"></audio>')


sfx("notif", "notification", 0.05, 2.4, 0.55)       # the contractor's message lands
sfx("slide", "slide-up", 2.75, 0.65, 0.42)          # cartoon anticipation as he turns
sfx("takeoff", "whoosh", TAKEOFF, 0.57, 0.65)       # cartoon whoosh on takeoff
sfx("aku", "pop", 3.45, 0.72, 0.35)
sfx("fly1", "whoosh-short", 3.77, 0.57, 0.5)        # flying past each cut, not every one
sfx("door", "whoosh-short", 5.16, 0.57, 0.5)
sfx("fly2", "whoosh-short", 6.30, 0.57, 0.42)
sfx("fly3", "whoosh-short", 7.59, 0.57, 0.42)
sfx("boing", "boing", 8.66, 0.53, 0.55)             # comedic payoff on the last shot

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {INK}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="w-main" style="position:absolute; inset:0; z-index:1; overflow:hidden">
        <video id="v-main" class="clip" src="assets/video/main.mp4" data-start="0" data-duration="{TOTAL}" data-media-start="0"
          data-track-index="1" playsinline data-has-audio="true" data-volume="0.6" data-fade-out="0.3"
          style="position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover"></video>
      </div>
      <div id="shade" style="position:absolute; inset:0; z-index:2; pointer-events:none;
        background: linear-gradient(180deg, rgba(16,20,28,.55) 0%, rgba(16,20,28,.35) 28%, rgba(16,20,28,0) 46%)"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{TOTAL}"
        data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // a short camera kick on takeoff sells the "sudden" flight
      tl.fromTo("#w-main", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.18, ease: "power3.out" }}, {TAKEOFF});
      tl.fromTo("#w-main", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, {TAKEOFF + 0.18});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

KEY = f'''<svg viewBox="0 0 64 64" width="112" height="112" style="vertical-align:-20px"><g transform="rotate(-35 32 32)">
  <circle cx="20" cy="32" r="13" fill="{YEL}" stroke="{INK}" stroke-width="4"/><circle cx="20" cy="32" r="5" fill="{INK}"/>
  <path d="M32 28h28v8h-6v7h-7v-7h-4v5h-6v-5h-5z" fill="{YEL}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g></svg>'''
WIND = f'''<svg viewBox="0 0 120 60" width="110" height="55"><g fill="none" stroke="{WHT}" stroke-width="7" stroke-linecap="round">
  <path d="M6 18h60c10 0 14-12 4-14"/><path d="M14 34h84c12 0 16 14 4 16"/><path d="M4 48h40"/></g></svg>'''

heading_top, heading_h = 400, 470
H = f'''    <div class="clip head" id="head" data-start="0" data-duration="{TOTAL}" style="top:{heading_top}px; height:{heading_h}px">
      <img class="logo" id="logo" src="assets/img/logo.png" alt="" />
      <div class="l1" id="l1">POV: BILA KONTRAKTOR CAKAP,</div>
      <div class="l2" id="l2a">“ESOK BOLEH</div>
      <div class="l2" id="l2b">AMBIL KUNCI!” <span class="key" id="key">{KEY}</span></div>
    </div>
    <div class="clip aku" id="aku" data-start="{TAKEOFF}" data-duration="1.7" style="top:900px; height:90px">
      <span class="akut">AKU:</span><span class="wind" id="wind">{WIND}</span>
    </div>'''
assert SAFE_TOP <= heading_top and heading_top + heading_h <= SAFE_BOT
assert SAFE_TOP <= 900 and 990 <= SAFE_BOT

J = [
    'tl.fromTo("#logo", { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.02);',
    'tl.fromTo("#l1", { opacity: 0, scale: 0.86 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 0.08);',
    'tl.fromTo("#l2a", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.28);',
    'tl.fromTo("#l2b", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.42);',
    'tl.fromTo("#key", { rotation: -50, scale: 0 }, { rotation: 0, scale: 1, duration: 0.5, ease: "back.out(2.6)" }, 0.62);',
    # the key jingles as he takes off
    f'tl.fromTo("#key", {{ rotation: 0 }}, {{ rotation: 18, duration: 0.09, ease: "sine.inOut", yoyo: true, repeat: 5, immediateRender: false }}, {TAKEOFF});',
    # heading gives a small bump with the payoff
    # once he is airborne the heading tucks up so it never covers him, then comes back for the payoff
    'tl.fromTo("#head", { scale: 1 }, { scale: 0.8, duration: 0.35, ease: "power3.inOut" }, 3.55);',
    'tl.fromTo("#head", { scale: 0.8 }, { scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, 8.66);',
    f'tl.fromTo("#aku", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }}, {TAKEOFF + 0.02});',
    f'tl.fromTo("#wind", {{ x: -10 }}, {{ x: 14, duration: 0.18, ease: "sine.inOut", yoyo: true, repeat: 7 }}, {TAKEOFF + 0.1});',
    f'tl.to("#aku", {{ opacity: 0, x: 60, duration: 0.2, ease: "power2.in" }}, {TAKEOFF + 1.48});',
]

STROKE = "-webkit-text-stroke: 5px rgba(20,20,20,.75); paint-order: stroke fill;"
SHADOW = "text-shadow: 0 6px 0 rgba(0,0,0,.22), 0 12px 30px rgba(0,0,0,.55);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; }}
    .head {{ position: absolute; left: 40px; right: 40px; display: flex; flex-direction: column; align-items: center; transform-origin: 50% 0; }}
    .logo {{ width: 170px; height: auto; filter: drop-shadow(0 6px 14px rgba(0,0,0,.5)); margin-bottom: 18px; }}
    .l1 {{ font-weight: 900; font-size: 54px; line-height: 1.05; color: {WHT}; white-space: nowrap; letter-spacing: -.005em; {STROKE} {SHADOW} }}
    .l2 {{ font-weight: 900; font-size: 104px; line-height: 1.0; color: {YEL}; white-space: nowrap; letter-spacing: -.01em; margin-top: 6px; {STROKE} {SHADOW} }}
    .key {{ display: inline-block; filter: drop-shadow(0 6px 10px rgba(0,0,0,.45)); }}
    .aku {{ position: absolute; left: 120px; display: flex; align-items: center; gap: 10px; }}
    .akut {{ font-weight: 900; font-size: 64px; color: {WHT}; {STROKE} {SHADOW} }}
    .wind {{ display: inline-block; filter: drop-shadow(0 4px 8px rgba(0,0,0,.5)); }}
'''
gfx = f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="gfx" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{H}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in J).lstrip()}
    window.__timelines["gfx"] = tl;
  </script>
</template>
'''
open("compositions/gfx.html", "w").write(gfx)
print("ok", TOTAL)
