"""Builds index.html and compositions/words.html for the vacuum magnetic holder video.
Run from the project folder: python3 tools/build.py"""
import html as H

TOTAL = 17

# ---------------- shots (hand-free footage only) ----------------
shots = [
    # id, src, start, dur, media_start, rate
    ("s1", "holder-glass.mp4", 0, 2.6, 0, 1),
    ("s2", "holder-drive.mp4", 2.6, 0.8, 0.45, 1),
    ("s3", "holder-glass.mp4", 3.4, 2.2, 2.6, 1),
    ("s4", "holder-glass.mp4", 5.6, 1.8, 4.8, 0.64),
    ("s5", "holder-drive.mp4", 7.4, 2.2, 6.35, 1),
    ("s6", "holder-drive.mp4", 9.6, 7.4, 8.55, 0.525),
]
vids = "\n".join(
    f'      <video id="{i}" class="clip" src="assets/{s}" data-start="{st}" data-duration="{d}" data-media-start="{ms}"'
    + (f' data-playback-rate="{r}"' if r != 1 else "")
    + f' data-track-index="1" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:1"></video>'
    for i, s, st, d, ms, r in shots
)

index = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{vids}
      <div id="words" data-composition-id="words" data-composition-src="compositions/words.html" data-start="0" data-duration="{TOTAL}"
        data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(index)

# ---------------- words ----------------
body, js = [], []
track = [2]

def nt():
    track[0] += 1
    return track[0]

def group(gid, t, d, inner, out=True):
    body.append(f'    <div id="{gid}" class="clip w-group" data-start="{t}" data-duration="{d}" data-track-index="{nt()}">{inner}\n    </div>')
    if out:
        js.append(f'    tl.to("#{gid}-all", {{ opacity: 0, duration: 0.18, ease: "power1.in" }}, {round(t + d - 0.2, 2)});')

def write_on(eid, t, dur, start_pct=100):
    """Reveal left to right, like a pen writing."""
    js.append(f'    tl.fromTo("#{eid}", {{ clipPath: "inset(-30% {start_pct}% -30% -10%)" }}, {{ clipPath: "inset(-30% -10% -30% -10%)", duration: {dur}, ease: "power1.inOut" }}, {t});')

def typed(eid, text, t, step, collapse=False):
    """Letter by letter. collapse=True keeps unwritten letters out of the layout so a cursor follows."""
    spans = "".join(f'<span id="{eid}-{k}" class="ch">{H.escape(c) if c != " " else "&nbsp;"}</span>' for k, c in enumerate(text))
    for k in range(len(text)):
        if collapse:
            js.append(f'    tl.fromTo("#{eid}-{k}", {{ display: "none" }}, {{ display: "inline", duration: 0.01 }}, {round(t + k * step, 3)});')
        else:
            js.append(f'    tl.fromTo("#{eid}-{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {round(t + k * step, 3)});')
    return spans

def sparkle(sid, x, y, size, color, t, end=None):
    end = end or TOTAL
    body.append(f'    <div id="{sid}" class="clip spark" data-layout-ignore data-start="{t}" data-duration="{round(end - t, 2)}" data-track-index="{nt()}" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color}"><span id="{sid}-in" style="display:inline-block">✦</span></div>')
    js.append(f'    tl.fromTo("#{sid}-in", {{ scale: 0, rotation: -45, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.3, ease: "back.out(3)" }}, {t});')
    js.append(f'    tl.to("#{sid}-in", {{ scale: 0.7, opacity: 0.6, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {round(t + 0.32, 2)});')

def sparkle_out(sid, t):
    pass

# 1. Road Trip Season (0 - 2.6) — on screen from frame 0
group("g1", 0, 2.6, """
      <div id="g1-all">
        <div id="g1-a" class="scr" style="left:110px;top:660px;font-size:200px">Road Trip</div>
        <div id="g1-b" class="scr" style="left:330px;top:860px;font-size:200px">Season</div>
        <div id="g1-c" class="pink" style="left:0;width:1080px;text-align:center;top:1110px;font-size:74px">""" + typed("g1-c", "in November", 1.25, 0.05) + """</div>
      </div>""")
write_on("g1-a", 0, 0.75, start_pct=55)
write_on("g1-b", 0.6, 0.65)
sparkle("k1", 250, 1105, 58, "#a8d8ff", 1.5, 2.6); sparkle("k2", 790, 1150, 46, "#fff0a0", 1.75, 2.6); sparkle("k3", 870, 1060, 34, "#ffffff", 1.95, 2.6)
for k in ("k1", "k2", "k3"): sparkle_out(k, 2.42)

# 2. ft. (2.6 - 3.4)
group("g2", 2.6, 0.8, """
      <div id="g2-all"><div id="g2-a" class="pink" style="left:0;width:1080px;text-align:center;top:930px;font-size:96px">""" + typed("g2-a", "ft.", 2.62, 0.07) + """</div></div>""", out=False)
sparkle("k4", 400, 900, 50, "#a8d8ff", 2.65, 3.4); sparkle("k5", 640, 990, 40, "#fff0a0", 2.75, 3.4)
for k in ("k4", "k5"): sparkle_out(k, 3.32)

# 3. Vacuum Magnetic Holder (3.4 - 5.6)
group("g3", 3.4, 2.2, """
      <div id="g3-all">
        <div id="g3-a" class="pink" style="left:0;width:1080px;text-align:center;top:930px;font-size:100px">""" + typed("g3-a", "Vacuum Magnetic", 3.45, 0.045) + """</div>
        <div id="g3-b" class="pink" style="left:0;width:1080px;text-align:center;top:1050px;font-size:100px">""" + typed("g3-b", "Holder", 4.15, 0.05) + """<span id="g3-moon" class="emo">&nbsp;🌙</span></div>
      </div>""")
js.append('    tl.fromTo("#g3-moon", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, 4.5);')
sparkle("k6", 140, 900, 44, "#a8d8ff", 4.6, 5.6); sparkle("k7", 900, 1180, 52, "#fff0a0", 4.75, 5.6)
for k in ("k6", "k7"): sparkle_out(k, 5.42)

# 4. suction grip (5.6 - 7.4)
group("g4", 5.6, 1.8, """
      <div id="g4-all" style="position:absolute;inset:0;transform-origin:540px 1000px">
        <div id="g4-a" class="hand" style="left:170px;top:880px;font-size:150px">suction grip</div>
        <div id="g4-b" class="hand" style="left:300px;top:1060px;font-size:72px">sticks firm on glass</div>
      </div>""")
write_on("g4-a", 5.62, 0.5); write_on("g4-b", 5.95, 0.45)

# 5. magnetic snap (7.4 - 9.6)
group("g5", 7.4, 2.2, """
      <div id="g5-all">
        <div id="g5-a" class="hand" style="left:110px;top:800px;font-size:150px">magnetic snap</div>
        <div id="g5-b" class="hand" style="left:150px;top:980px;font-size:72px">place your phone in a second</div>
      </div>""")
write_on("g5-a", 7.42, 0.55); write_on("g5-b", 7.8, 0.5)

# 6. THE ULTIMATE GRIP WHILE DRIVING (9.6 - 11.75), one word at a time
words = [("THE", 9.62), ("ULTIMATE", 10.05), ("GRIP", 10.55), ("WHILE", 10.95), ("DRIVING", 11.4)]
ends = [w[1] for w in words[1:]] + [11.9]
for n, ((w, t), e) in enumerate(zip(words, ends)):
    gid = f"g6-{n}"
    group(gid, t, round(e - t, 2), f"""
      <div id="{gid}-all"><div id="{gid}-w" class="type" style="left:150px;top:900px;font-size:118px">""" + typed(gid + "-w", w, t, 0.035, collapse=True) + f"""<span id="{gid}-cur" class="cur">&nbsp;</span></div></div>""", out=False)

# 7. Save this video (11.85 - 13.2)
group("g7", 11.9, 1.3, """
      <div id="g7-all">
        <div id="g7-a" class="scr" style="left:170px;top:720px;font-size:190px">Save this</div>
        <div id="g7-b" class="scr" style="left:380px;top:910px;font-size:190px">video</div>
      </div>""")
write_on("g7-a", 11.92, 0.5); write_on("g7-b", 12.3, 0.4)

# 8. To buy and try (13.2 - 14.5)
group("g8", 13.2, 1.3, """
      <div id="g8-all">
        <div id="g8-a" class="scr" style="left:200px;top:740px;font-size:190px">To buy</div>
        <div id="g8-b" class="scr" style="left:330px;top:930px;font-size:190px">and try</div>
      </div>""")
write_on("g8-a", 13.23, 0.5); write_on("g8-b", 13.65, 0.5)

# 9. This Magnetic Holder (14.5 - 16.5)
group("g9", 14.5, 2.5, """
      <div id="g9-all">
        <div id="g9-a" class="scr" style="left:330px;top:640px;font-size:180px">This</div>
        <div id="g9-b" class="scr" style="left:120px;top:830px;font-size:180px">Magnetic</div>
        <div id="g9-c" class="scr" style="left:300px;top:1020px;font-size:180px">Holder</div>
      </div>""", out=False)
write_on("g9-a", 14.5, 0.3); write_on("g9-b", 14.62, 0.45); write_on("g9-c", 14.85, 0.4)
sparkle("k8", 760, 700, 54, "#a8d8ff", 15.4); sparkle("k9", 180, 1150, 44, "#fff0a0", 15.55)

words_html = f"""<template>
  <style>
    @font-face {{ font-family: "Great Vibes"; src: url("assets/fonts/GreatVibes-Regular.ttf"); }}
    @font-face {{ font-family: "Caveat"; src: url("assets/fonts/Caveat.ttf"); }}
    @font-face {{ font-family: "Emoji"; src: local("Noto Color Emoji"); }}
    #root {{ position: absolute; inset: 0; }}
    .w-group {{ position: absolute; inset: 0; }}
    .w-group > div {{ position: absolute; inset: 0; }}
    .scr, .pink, .hand, .type, .spark {{ position: absolute; white-space: nowrap; }}
    /* script, mint with a soft glow */
    .scr {{ font-family: "Great Vibes", cursive; color: #d9fff4; line-height: 1;
      text-shadow: 0 0 22px rgba(160, 255, 228, 0.55), 0 3px 10px rgba(0, 0, 0, 0.3); }}
    /* small rounded pink */
    .pink {{ font-family: "Nunito", "Emoji", sans-serif; font-weight: 700; color: #ffa9dc; letter-spacing: 0.01em;
      text-shadow: 0 0 3px rgba(90, 20, 60, 0.55), 0 2px 16px rgba(0, 0, 0, 0.55); }}
    /* casual handwriting, white */
    .hand {{ font-family: "Caveat", cursive; font-weight: 600; color: #ffffff; line-height: 1;
      text-shadow: 0 2px 12px rgba(0, 0, 0, 0.4); }}
    /* chunky typewriter, pink with a white cursor */
    .type {{ font-family: "Archivo Black", sans-serif; color: #ffb6ea; letter-spacing: 0.02em;
      text-shadow: 0 3px 12px rgba(0, 0, 0, 0.3); }}
    .cur {{ display: inline-block; width: 0.42em; height: 0.82em; margin-left: 0.08em; background: #ffffff; vertical-align: -0.06em; }}
    .emo {{ font-family: "Emoji"; }}
    .spark {{ text-shadow: 0 0 14px rgba(255, 255, 255, 0.7); line-height: 1; }}
  </style>
  <div id="root" data-composition-id="words" data-width="1080" data-height="1920">
{chr(10).join(body)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["words"] = tl;
  </script>
</template>
"""
open("compositions/words.html", "w").write(words_html)
print("built")
