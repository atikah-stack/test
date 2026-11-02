"""Builds index.html and compositions/words.html for the iPad case affiliate video.
Run from the project folder: python3 tools/build.py"""
import html as H

TOTAL = 7.4

# ---------------- shots ----------------
# id, clip, start, dur, media_start
FIRST, SHOT = 1.0, 0.8  # first shot 1s, every other shot 0.8s
order = [
    # clip, media_start  (one clip per angle; -s = straightened/recentred)
    ("img_0344-s", 0.5),
    ("img_0343", 1.0),
    ("img_0362", 1.2),
    ("img_0347", 0.8),
    ("img_0348", 0.05),
    ("img_0359-s", 0.4),
    ("img_0361", 0.4),
    ("img_0354", 0.4),
    ("img_0357-s", 1.0),
]
starts = [0.0] + [round(FIRST + (i - 1) * SHOT, 2) for i in range(1, len(order))]
shots = [(f"s{i+1}", c, starts[i], FIRST if i == 0 else SHOT, ms) for i, (c, ms) in enumerate(order)]
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

for t in starts[1:]:
    fx("click-soft", t, vol=0.45)

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
body.append(f'''    <div id="ti" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="{nt()}" style="position:absolute;inset:0">
      <div id="ti-b" class="scr" style="top:790px">Blue</div>
      <div id="ti-c" class="small" style="top:1012px">ipad case</div>
    </div>''')
# "Blue" writes on (already started at frame 0), "ipad case" settles in under it; both stay to the end
js.append('    tl.fromTo("#ti-b", { clipPath: "inset(-40% 45% -40% -5%)" }, { clipPath: "inset(-40% -5% -40% -5%)", duration: 0.8, ease: "power1.inOut" }, 0);')
js.append('    tl.fromTo("#ti-c", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, 0.55);')
fx("sparkle", 0.1, vol=0.3)
sparkle("k1", 395, 800, 22, "#ffffff", 0.5, TOTAL)
sparkle("k2", 690, 785, 16, "#ffffff", 0.7, TOTAL)
fx("chime", starts[-1], vol=0.25)

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
    @font-face {{ font-family: "Pinyon Script"; src: url("assets/fonts/PinyonScript-Regular.ttf"); }}
    @font-face {{ font-family: "Emoji"; src: local("Noto Color Emoji"); }}
    #root {{ position: absolute; inset: 0; }}
    .small, .scr, .cap {{ position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }}
    .small {{ font-family: "Nunito", sans-serif; font-weight: 800; font-size: 46px; letter-spacing: 0.01em; color: #ffffff; }}
    .scr {{ font-family: "Pinyon Script", cursive; font-size: 220px; line-height: 1.1; color: #ffffff; }}
    .cap {{ font-family: "Nunito", "Emoji", sans-serif; font-weight: 700; font-size: 52px; color: #ffffff;
      text-shadow: 0 0 3px rgba(0, 0, 0, 0.45), 0 2px 14px rgba(0, 0, 0, 0.5); }}
    .cap-in {{ display: inline-block; }}
    .cur {{ display: inline-block; width: 0.32em; height: 0.95em; margin-left: 0.12em; background: #ffffff; vertical-align: -0.12em; }}
    .spark {{ position: absolute; line-height: 1; }}
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
