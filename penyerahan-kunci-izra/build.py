"""Builds index.html for the PN Izra key handover reel.

Edit the SHOTS list (clip, media start, duration, playback rate, volume) and
run `python3 build.py`. Every clip is an untouched original from assets/src.
"""
import json

FADE = 0.2  # crossfade between shots, seconds
GRADE = json.dumps({"preset": "warm-daylight", "intensity": 0.45})

# (id, source file, media start, duration on timeline, playback rate, volume or None for muted)
SHOTS = [
    # Hook: the client's smile while signing
    ("s01", "IMG_0051.MOV", 3.2, 4.8, 1, 1.0),
    # Handover
    ("s02", "IMG_0075.mov", 0.2, 2.6, 0.85, None),   # keys on the tray, close-up
    ("s03", "IMG_0054.mov", 0.0, 2.2, 1, 0.5),       # signing, close-up
    ("s05", "IMG_0092.MOV", 0.0, 2.8, 1, 0.9),       # Tahniah board handed over
    ("s06", "IMG_0081.mov", 0.0, 2.4, 1, 0.6),       # key turns in the front door
    # Bungalow reveal
    ("s07", "IMG_0045.mov", 0.0, 3.1, 0.85, None),   # exterior (stored sideways, turned upright below)
    ("s08", "IMG_0078.mov", 2.0, 3.6, 1, 0.4),  # front door opens
    ("s09", "IMG_0123.MOV", 0.0, 3.6, 1, 0.4),       # walking in
    ("s10", "IMG_0043.mov", 0.0, 2.7, 1, 0.3),       # main hall, chandelier
    ("s11", "IMG_0123.MOV", 3.8, 3.2, 1, 0.4),       # interior
    # Celebration
    ("s12", "IMG_0123.MOV", 7.6, 4.2, 0.85, None),   # hugs
    ("s13", "IMG_0080.MOV", 0.5, 3.2, 1, 0.5),       # client photographs her new home
    ("s14", "IMG_0123.MOV", 19.5, 3.0, 1, 0.4),      # chatting with the Mahligai Idaman team
    ("s15", "IMG_0102.MOV", 1.5, 2.8, 1, 0.5),       # family at the entrance
    # Ending
    ("s16", "IMG_0092.MOV", 4.6, 3.6, 1, 0.9),       # group photo with the board
    ("s17", "IMG_0098.mov", 0.0, 3.55, 0.85, None),  # waving, camera tilts up to the chandelier
]

# The exterior clip is stored sideways: turn it upright and pan across the facade.
ROTATED = {"s07"}

times = []
t = 0.0
for s in SHOTS:
    times.append(round(t, 2))
    t += s[3] - FADE
video_end = round(times[-1] + SHOTS[-1][3], 2)
IDX = {s[0]: i for i, s in enumerate(SHOTS)}
TOTAL = round(video_end + 1.0, 2)

# Graphics slots (start, duration)
HOOK = (0.0, 4.5)
CAPTION = (times[IDX["s02"]] + 0.2, 3.0)
IMPIAN = (times[IDX["s07"]] + 0.3, 3.2)
CLOSING = (times[IDX["s16"]] + 0.3, 3.4)
OUTRO = (times[IDX["s17"]] + 1.9, TOTAL - (times[IDX["s17"]] + 1.9))

SFX = [
    ("x-hook", "whoosh-short.mp3", 0.05, 0.6, 0.22),
    ("x-key", "impact-bass-1.mp3", times[IDX["s02"]], 2.1, 0.22),
    ("x-impian", "whoosh.mp3", IMPIAN[0], 0.6, 0.2),
    ("x-close", "whoosh-short.mp3", CLOSING[0], 0.6, 0.2),
    ("x-logo", "chime.mp3", OUTRO[0] + 0.2, 2.5, 0.25),
]

rows = []
for i, (sid, src, ms, dur, rate, vol) in enumerate(SHOTS):
    start = times[i]
    audio = f'data-has-audio="true" data-volume="{vol}"' if vol is not None else "muted"
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1 else ""
    cls = "shot clip" if sid not in ROTATED else "rot clip"
    tag = (
        f'<video id="{sid}" class="{cls}" src="assets/src/{src}" {audio} playsinline '
        f'data-start="{start}" data-duration="{dur}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{i % 2}" data-color-grading=\'{GRADE}\' style="z-index:{i + 1}"></video>'
    )
    if sid in ROTATED:
        tag = f'<div id="{sid}-turn" class="turn" style="z-index:{i + 1}">{tag}</div>'
    rows.append("      " + tag)

# Slow-motion shots are muted on the video; keep their natural room sound at normal speed instead.
for i, (sid, src, ms, dur, rate, vol) in enumerate(SHOTS):
    if vol is None:
        rows.append(
            f'      <audio id="a-{sid}" class="clip" src="assets/src/{src}" data-start="{round(times[i] + FADE, 2)}" '
            f'data-duration="{round(dur - FADE, 2)}" data-media-start="{round(ms + FADE, 2)}" data-volume="0.5" data-track-index="11"></audio>'
        )

for aid, f, s, d, v in SFX:
    rows.append(
        f'      <audio id="{aid}" class="clip" src="assets/sfx/{f}" data-start="{round(s, 2)}" '
        f'data-duration="{d}" data-volume="{v}" data-track-index="12"></audio>'
    )


def host(cid, slot, z, track):
    return (
        f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{round(slot[0], 2)}" data-duration="{round(slot[1], 2)}" data-track-index="{track}" '
        f'data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{z}"></div>'
    )


rows.append(
    f'      <div id="fade" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-layout-ignore></div>'
)
rows.append(host("hook", HOOK, 60, 5))
rows.append(host("caption", CAPTION, 61, 6))
rows.append(host("impian", IMPIAN, 62, 5))
rows.append(host("closing", CLOSING, 63, 5))
rows.append(host("outro", OUTRO, 95, 7))

js_shots = json.dumps([[f"#{s[0]}", times[i], s[3]] for i, s in enumerate(SHOTS)])
rot = SHOTS[IDX["s07"]]

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0b; }}
      #root {{ width: 100%; height: 100%; background: #0b0b0b; font-family: "Poppins", sans-serif; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      /* Sideways source: a portrait box turned a quarter-turn left fills the frame upright. */
      .turn {{ position: absolute; left: -420px; top: -747px; width: 1920px; height: 3414px; transform: rotate(-90deg); }}
      .rot {{ position: absolute; left: 0; top: 0; width: 1920px; height: 3414px; object-fit: cover; }}
      #fade {{ position: absolute; inset: 0; z-index: 90; background: #0b0b0b; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(rows)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const shots = {js_shots};
      shots.forEach(([sel, s, d]) => {{
        if (sel === "#s07") return;
        tl.fromTo(sel, {{ scale: 1 }}, {{ scale: 1.05, duration: d, ease: "none" }}, s);
        if (s > 0) tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: {FADE}, ease: "sine.inOut" }}, s);
      }});
      // Exterior: slow pan across the facade (local y is screen x after the turn).
      tl.fromTo("#s07", {{ y: 520, opacity: 0 }}, {{ y: -420, duration: {rot[3]}, ease: "sine.inOut" }}, {times[IDX["s07"]]});
      tl.to("#s07", {{ opacity: 1, duration: {FADE}, ease: "sine.inOut" }}, {times[IDX["s07"]]});
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "sine.in" }}, {round(video_end - 0.6, 2)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)
print("total", TOTAL, "video_end", video_end)
print("times", times)
print("hook", HOOK, "caption", CAPTION, "impian", IMPIAN, "closing", CLOSING, "outro", OUTRO)


# ---- Graphics scenes: one heading system, matching the Mahligai Idaman reference ----
HEAD_CSS = """
    #root { position:absolute; inset:0; font-family:"Poppins",sans-serif; }
    .block { position:absolute; left:60px; right:60px; display:flex; flex-direction:column; align-items:center; text-align:center; }
    .l1, .l2 { font-weight:900; text-transform:uppercase; line-height:1.02; letter-spacing:0.005em;
      text-shadow:0 6px 22px rgba(0,0,0,.55), 0 2px 5px rgba(0,0,0,.5); }
    .l1 { color:#FFFFFF; font-size:var(--l1, 64px); }
    .l2 { color:#F5C34B; font-size:var(--l2, 96px); margin-top:4px; }
    .tag { margin-top:26px; padding:12px 32px 14px; border-radius:40px; background:rgba(0,0,0,.55);
      color:#FFFFFF; font-weight:600; font-size:34px; letter-spacing:0.01em; }
"""


def heading(cid, l1, l2, top, dur, sizes=("64px", "96px"), tag=None):
    tag_html = f'\n      <div id="{cid}-tag" class="tag">{tag}</div>' if tag else ""
    tag_js = (f'\n    tl.fromTo("#{cid}-tag", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.6, ease:"power2.out" }}, 0.55);'
              if tag else "")
    return f"""<template>
  <style>{HEAD_CSS}
    #{cid}-block {{ top:{top}px; --l1:{sizes[0]}; --l2:{sizes[1]}; }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-block" class="block clip" data-start="0" data-duration="{round(dur, 2)}" data-track-index="0">
      <div id="{cid}-l1" class="l1">{l1}</div>
      <div id="{cid}-l2" class="l2">{l2}</div>{tag_html}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{cid}-l1", {{ opacity:0, y:28, scale:0.95 }}, {{ opacity:1, y:0, scale:1, duration:0.7, ease:"power2.out" }}, 0);
    tl.fromTo("#{cid}-l2", {{ opacity:0, y:28, scale:0.95 }}, {{ opacity:1, y:0, scale:1, duration:0.7, ease:"power2.out" }}, 0.18);{tag_js}
    tl.to("#{cid}-block", {{ opacity:0, duration:0.4, ease:"sine.in" }}, {round(dur - 0.45, 2)});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


CAPTION_HTML = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; font-family:"Poppins",sans-serif; }}
    #cap-wrap {{ position:absolute; left:0; right:0; top:1360px; display:flex; justify-content:center; }}
    #cap-pill {{ padding:16px 38px 18px; border-radius:44px; background:rgba(0,0,0,.55);
      color:#FFFFFF; font-weight:600; font-size:42px; letter-spacing:0.01em; }}
  </style>
  <div id="root" data-composition-id="caption" data-width="1080" data-height="1920">
    <div id="cap-wrap" class="clip" data-start="0" data-duration="{CAPTION[1]}" data-track-index="0">
      <div id="cap-pill">Detik yang dinantikan...</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#cap-pill", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:0.5, ease:"power2.out" }}, 0);
    tl.to("#cap-pill", {{ opacity:0, duration:0.4, ease:"sine.in" }}, {round(CAPTION[1] - 0.45, 2)});
    window.__timelines["caption"] = tl;
  </script>
</template>
"""

OUTRO_HTML = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; }}
    #logo-card {{ position:absolute; left:250px; top:340px; width:580px; padding:44px 50px; border-radius:36px;
      background:#FFFFFF; box-shadow:0 18px 60px rgba(0,0,0,.35); }}
    #logo-img {{ display:block; width:480px; height:auto; }}
  </style>
  <div id="root" data-composition-id="outro" data-width="1080" data-height="1920">
    <div id="logo-card" class="clip" data-start="0" data-duration="{round(OUTRO[1], 2)}" data-track-index="0">
      <img id="logo-img" src="assets/brand/logo-mi.png" alt="Mahligai Idaman" />
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#logo-card", {{ opacity:0, y:24, scale:0.95 }}, {{ opacity:1, y:0, scale:1, duration:0.8, ease:"power2.out" }}, 0);
    // Once the picture fades to black, settle the logo to the centre.
    tl.to("#logo-card", {{ y:420, duration:0.9, ease:"power2.inOut" }}, {round(video_end - 0.6 - OUTRO[0], 2)});
    window.__timelines["outro"] = tl;
  </script>
</template>
"""

scenes = {
    "hook": heading("hook", "SESI PENYERAHAN KUNCI", "BANGLO PN IZRA", 1130, HOOK[1], sizes=("66px", "104px"), tag="Kok Lanas, Kelantan"),
    "impian": heading("impian", "IMPIAN KINI", "JADI KENYATAAN", 1120, IMPIAN[1], sizes=("84px", "92px")),
    "closing": heading("closing", "SELAMAT MENDUDUKI", "RUMAH IDAMAN", 1300, CLOSING[1], sizes=("72px", "100px")),
    "caption": CAPTION_HTML,
    "outro": OUTRO_HTML,
}
for name, body in scenes.items():
    open(f"compositions/{name}.html", "w").write(body)
