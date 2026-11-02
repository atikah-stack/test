"""Builds index.html and compositions/words.html for the iPad case affiliate video.
Run from the project folder: python3 tools/build.py"""
import html as H

TOTAL = 20.3

# ---------------- shots ----------------
# id, clip, start, dur, media_start
shots = [
    ("r1", "img_0343", 0.00, 0.37, 0.6),
    ("r2", "img_0357", 0.37, 0.37, 2.5),
    ("r3", "img_0353", 0.74, 0.37, 0.3),
    ("r4", "img_0362", 1.11, 0.37, 3.0),
    ("r5", "img_0361", 1.48, 0.37, 0.3),
    ("s1", "img_0344", 1.85, 2.05, 0.5),
    ("s2", "img_0363", 3.90, 2.20, 0.4),
    ("s3", "img_0362", 6.10, 2.00, 0.6),
    ("s4", "img_0347", 8.10, 1.60, 1.0),
    ("s5", "img_0359", 9.70, 2.00, 0.4),
    ("s6", "img_0353", 11.70, 2.00, 0.2),
    ("s7", "img_0357", 13.70, 2.00, 0.8),
    ("q1", "img_0354", 15.70, 0.53, 0.5),
    ("q2", "img_0350", 16.23, 0.53, 0.2),
    ("q3", "img_0361", 16.76, 0.54, 1.5),
    ("s8", "img_0343", 17.30, 3.00, 1.5),
]
vids = "\n".join(
    f'      <video id="{i}" class="clip" src="assets/clips/{c}.mp4" data-start="{st}" data-duration="{d}" data-media-start="{ms}" data-track-index="1" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:1"></video>'
    for i, c, st, d, ms in shots
)

# ---------------- sound effects ----------------
sfx = []
LEN = {"click-soft": 0.37, "whoosh-short": 0.57, "pop": 0.72, "sparkle": 1.8, "chime": 2.5, "typing": 1.5, "key-press": 0.4}
def fx(name, t, dur=None, vol=0.35):
    n = len(sfx) + 1
    dur = dur or min(LEN[name], round(TOTAL - t, 2))
    d = f' data-duration="{dur}"'
    sfx.append(f'      <audio id="fx{n}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}"{d} data-volume="{vol}" data-track-index="{10 + n}"></audio>')

for t in (0.37, 0.74, 1.11, 1.48, 1.85):
    fx("click-soft", t, vol=0.5)
for t in (15.7, 16.23, 16.76):
    fx("whoosh-short", t, vol=0.3)

# ---------------- words ----------------
body, js = [], []
track = [2]
def nt():
    track[0] += 1
    return track[0]

def typed(eid, text, t, step):
    """Letter by letter; unwritten letters stay out of the layout so the cursor follows."""
    out = []
    for k, c in enumerate(text):
        out.append(f'<span id="{eid}-{k}">{H.escape(c) if c != " " else " "}</span>')
        js.append(f'    tl.fromTo("#{eid}-{k}", {{ display: "none" }}, {{ display: "inline", duration: 0.01 }}, {round(t + k * step, 3)});')
    return "".join(out)

def cursor(cid, t_on, t_off):
    js.append(f'    tl.fromTo("#{cid}", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.01 }}, {t_off});')
    return f'<span id="{cid}" class="cur"></span>'

def sparkle(sid, x, y, size, color, t, end):
    body.append(f'    <div id="{sid}" class="clip spark" data-layout-ignore data-start="{t}" data-duration="{round(end - t, 2)}" data-track-index="{nt()}" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color}"><span id="{sid}-in" style="display:inline-block">✦</span></div>')
    js.append(f'    tl.fromTo("#{sid}-in", {{ scale: 0, rotation: -45, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.3, ease: "back.out(3)" }}, {t});')
    js.append(f'    tl.to("#{sid}-in", {{ scale: 0.65, opacity: 0.55, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {round(t + 0.35, 2)});')

def caption(cid, text, t, d, top=620, step=0.045):
    """Small white typed caption with a block cursor, like the reference."""
    type_end = round(t + len(text) * step, 2)
    inner = typed(f"{cid}-t", text, t, step) + cursor(f"{cid}-cur", t, round(type_end + 0.35, 2))
    body.append(f'    <div id="{cid}" class="clip cap" data-start="{t}" data-duration="{d}" data-track-index="{nt()}" style="top:{top}px"><span id="{cid}-in" class="cap-in">{inner}</span></div>')
    js.append(f'    tl.to("#{cid}-in", {{ opacity: 0, duration: 0.15 }}, {round(t + d - 0.17, 2)});')
    fx("typing", t, dur=round(min(1.5, type_end - t + 0.05), 2), vol=0.3)

# Title over the fast intro: on screen from frame 0
body.append(f'''    <div id="ti" class="clip" data-start="0" data-duration="3.75" data-track-index="{nt()}" style="position:absolute;inset:0">
      <div id="ti-all" style="position:absolute;inset:0">
        <div id="ti-a" class="small" style="top:560px">{typed("ti-a", "found the cutest", 0.0, 0.03)}</div>
        <div id="ti-b" class="scr" style="top:615px">Baby Blue iPad Case</div>
        <div id="ti-c" class="small" style="top:765px">{typed("ti-c", "for my pink iPad <3", 1.2, 0.035)}</div>
      </div>
    </div>''')
js.append('    tl.fromTo("#ti-b", { clipPath: "inset(-30% 100% -30% -5%)" }, { clipPath: "inset(-30% -5% -30% -5%)", duration: 0.9, ease: "power1.inOut" }, 0.3);')
js.append('    tl.to("#ti-all", { opacity: 0, duration: 0.18 }, 3.55);')
fx("typing", 0.0, dur=0.55, vol=0.3)
fx("sparkle", 0.35, vol=0.3)
fx("typing", 1.2, dur=0.7, vol=0.3)
sparkle("k1", 120, 640, 52, "#ffc4dc", 0.6, 3.7)
sparkle("k2", 905, 760, 40, "#fff1a6", 0.9, 3.7)
sparkle("k3", 860, 560, 30, "#ffffff", 1.4, 3.7)
fx("pop", 0.6, vol=0.25); fx("pop", 0.9, vol=0.2)

caption("c1", "clear back so the pink shows 🎀", 3.95, 2.1)
caption("c2", "the cover folds 👀", 6.15, 1.9)
caption("c3", "into a stand <3", 8.15, 1.5)
caption("c4", "so many angles 🫶", 9.75, 1.9, top=400)
caption("c5", "perfect for netflix nights 🍿", 11.75, 1.9, top=360)
caption("c6", "fits perfectly <3", 13.75, 1.9, top=300)
caption("c7", "cuteness overload <3", 15.75, 1.5)
caption("c8", "go grab yours 👀🎀", 17.35, 2.95)
sparkle("k4", 200, 600, 46, "#ffc4dc", 17.9, TOTAL)
sparkle("k5", 860, 690, 36, "#fff1a6", 18.1, TOTAL)
fx("chime", 17.9, vol=0.3)

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
{chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(index)

words = f"""<template>
  <style>
    @font-face {{ font-family: "Great Vibes"; src: url("assets/fonts/GreatVibes-Regular.ttf"); }}
    @font-face {{ font-family: "Emoji"; src: local("Noto Color Emoji"); }}
    #root {{ position: absolute; inset: 0; }}
    .small, .scr, .cap {{ position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }}
    .small {{ font-family: "Nunito", sans-serif; font-weight: 700; font-size: 46px; color: #ffc4dc;
      text-shadow: 0 0 3px rgba(120, 30, 70, 0.5), 0 2px 14px rgba(0, 0, 0, 0.45); }}
    .scr {{ font-family: "Great Vibes", cursive; font-size: 116px; line-height: 1.15; color: #fff1f7;
      text-shadow: 0 0 20px rgba(255, 170, 210, 0.85), 0 0 4px rgba(255, 120, 180, 0.6), 0 3px 10px rgba(0, 0, 0, 0.35); }}
    .cap {{ font-family: "Nunito", "Emoji", sans-serif; font-weight: 700; font-size: 52px; color: #ffffff;
      text-shadow: 0 0 3px rgba(0, 0, 0, 0.45), 0 2px 14px rgba(0, 0, 0, 0.5); }}
    .cap-in {{ display: inline-block; }}
    .cur {{ display: inline-block; width: 0.32em; height: 0.95em; margin-left: 0.12em; background: #ffffff; vertical-align: -0.12em; }}
    .spark {{ position: absolute; line-height: 1; text-shadow: 0 0 14px rgba(255, 255, 255, 0.8); }}
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
open("compositions/words.html", "w").write(words)
print("built")
