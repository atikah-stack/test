#!/usr/bin/env python3
"""Hook overlay (transparent, rendered to ProRes 4444) and outro card for the
"Minta yang besar-besar" house-tour video. The tour itself is the stabilized original
(assets/video/stab.mp4, built by prep.sh) and is composited with ffmpeg (see finish.sh).

Hook: 0.2-7.6 s over the spoken quote (no subtitle boxes).
Safe zone: top 15% (Y < 288) and bottom 20% (Y > 1536) carry nothing.
"""
WHT, YEL = "#FFFFFF", "#FFD43B"
HOOK = 7.9
SUBS = [(0.0, 2.2, "Saya tidak minta yang kecil-kecil."), (2.2, 4.0, "Saya selalu minta yang besar-besar."),
        (4.0, 7.6, "Saya takut minta yang kecil, mengkerdilkan Allah yang Maha Besar.")]
SH = "text-shadow: 0 4px 8px rgba(0,0,0,.45), 0 12px 32px rgba(0,0,0,.5);"
cues = "\n".join(f'      <div class="cue clip" id="c{i}" data-start="{s}" data-duration="{round(e - s, 2)}"><span>{t}</span></div>'
                 for i, (s, e, t) in enumerate(SUBS))
cuejs = "\n".join(f'      tl.fromTo("#c{i} span", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.15 }}, {s});' for i, (s, _, _) in enumerate(SUBS))
hook = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: transparent; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Montserrat, sans-serif; }}
      #shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,16,26,.62) 0%, rgba(10,16,26,.42) 30%, rgba(10,16,26,0) 50%); }}
      .grp {{ position: absolute; left: 30px; right: 30px; top: 330px; display: flex; flex-direction: column; align-items: center; }}
      .hw {{ font-weight: 900; font-size: 76px; line-height: 1.02; letter-spacing: -.01em; color: {WHT}; white-space: nowrap; {SH} }}
      .hy {{ font-weight: 900; font-size: 104px; line-height: 1.0; letter-spacing: -.02em; color: {YEL}; white-space: nowrap; text-align: center; {SH} }}
      .rule {{ width: 300px; height: 7px; margin-top: 18px; border-radius: 4px; background: {YEL}; box-shadow: 0 4px 14px rgba(0,0,0,.4); }}
      .cue {{ position: absolute; left: 70px; right: 70px; top: 1330px; height: 170px; display: flex; align-items: center; justify-content: center; text-align: center; }}
      .cue span {{ display: inline; font-weight: 700; font-size: 44px; line-height: 1.55; color: {WHT}; background: rgba(22,22,24,.86);
        padding: 8px 22px; border-radius: 12px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{HOOK}" data-width="1080" data-height="1920">
      <div id="shade" class="clip" data-start="0" data-duration="{HOOK}"></div>
      <div class="grp clip" id="g" data-start="0.15" data-duration="{HOOK - 0.15}">
        <div class="hw" id="w1">MINTA YANG</div><div class="hw" id="w2">BESAR-BESAR…</div>
        <div class="hy" id="y1">ALLAH BAGI SIAP</div><div class="hy" id="y2">DENGAN KOLAM!</div>
        <div class="rule" id="r"></div>
      </div>

    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#w1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 0.2);
      tl.fromTo("#w2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 3.32);
      tl.set(["#w2", "#y1", "#y2"], {{ opacity: 0 }}, 0);
      tl.fromTo("#y1", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }}, 4.3);
      tl.fromTo("#y2", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }}, 4.75);
      tl.fromTo("#r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, 5.3);
      tl.to("#g", {{ opacity: 0, y: -16, duration: 0.35, ease: "power2.in" }}, {HOOK - 0.4});
      tl.to("#shade", {{ opacity: 0, duration: 0.5 }}, {HOOK - 0.5});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(hook)

OUT = 5.0
outro = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b1a1e; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #0b1a1e; overflow: hidden; }}
      #img {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #flash {{ position: absolute; inset: 0; background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.9) 50%, transparent 70%); opacity: 0; mix-blend-mode: overlay; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{OUT}" data-width="1080" data-height="1920">
      <img id="img" class="clip" src="assets/img/outro.png" alt="" data-start="0" data-duration="{OUT}" />
      <div id="flash" class="clip" data-start="0" data-duration="{OUT}"></div>
      <audio class="clip" src="assets/sfx/whoosh.mp3" data-start="0" data-duration="0.57" data-volume="0.5"></audio>
      <audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="0.35" data-duration="1.6" data-volume="0.45"></audio>
      <audio class="clip" src="assets/sfx/sparkle.mp3" data-start="1.5" data-duration="1.8" data-volume="0.3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#img", {{ scale: 1.18, filter: "blur(10px)", opacity: 0 }}, {{ scale: 1.0, filter: "blur(0px)", opacity: 1, duration: 1.1, ease: "expo.out" }}, 0);
      tl.to("#img", {{ scale: 1.04, duration: {OUT - 1.1}, ease: "none" }}, 1.1);
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.14, yoyo: true, repeat: 1 }}, 1.5);
      tl.to("#root", {{ opacity: 0, duration: 0.5 }}, {OUT - 0.5});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("outro/index.html", "w").write(outro)
print("ok")
