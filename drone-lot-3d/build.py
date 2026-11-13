#!/usr/bin/env python3
"""Generates index.html and compositions/gfx.html for the Mahligai Idaman drone-only ad
"Pakej Bina Rumah Beserta Tanah - Kg Hutan Putih, Machang" (1080x1920, 30 fps, 38 s).

No presenter: drone footage from the Drive folder carries every scene, with music and SFX.
Safe zone: top 15% (Y < 288) and bottom 18% (Y > 1574) carry nothing.
The lot outline is traced from the top-down drone photo (lot-top.jpg): the empty plot between
the dark-roof house and the walled grey house. No subdivision layout was supplied.
"""
import json, re

WHT, YEL, INK = "#FFFFFF", "#FFD43B", "#0E141D"
SAFE_TOP, SAFE_BOT = 288, 1574
FILM = 38.0

# drone shots: (id, file, start, end, media start, push from-to)
SHOTS = [
    ("d-open", "aerial-C51AA0CC", 0.0, 4.0, 0.5, (1.0, 1.10)),    # wide view of the development
    ("d-aud", "aerial-D9D2F1E2", 4.0, 7.4, 0.0, (1.0, 1.08)),     # land + neighbourhood
    ("d-pkg", "drone-0169", 15.0, 20.0, 0.5, (1.0, 1.10)),        # lot area from above
    ("d-ready", "aerial-B3AF3D5D", 25.0, 32.0, 0.2, (1.0, 1.06)),  # rises off the empty lot itself
    ("d-nb", "aerial-999CF884", 32.0, 35.0, 1.0, (1.0, 1.08)),     # neighbouring bungalows
]
vids = []
for sid, f, s, e, m, _ in SHOTS:
    vids.append(f'      <div id="{sid}-w" class="bw"><video id="{sid}" class="clip full" src="assets/video/{f}.mp4" data-start="{s}" '
                f'data-duration="{round(e - s, 3)}" data-media-start="{m}" data-track-index="1" muted playsinline></video></div>')

AUD = [f'      <audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{FILM}" '
       f'data-track-index="4" data-volume="0.55" data-fade-out="2"></audio>']


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{5 + len(AUD) % 3}" data-volume="{v}"></audio>')


for a in [
    ("h", "impact-bass-1", 0.35, 1.6, 0.4), ("h2", "whoosh-short", 0.9, 0.57, 0.3), ("hs", "click-soft", 1.5, 0.36, 0.3),
    ("aud", "whoosh", 3.95, 0.57, 0.35), ("aud2", "pop", 5.0, 0.72, 0.3),
    ("map", "whoosh-cinematic", 7.2, 3.0, 0.3), ("trace", "riser", 8.2, 2.6, 0.25), ("lock", "impact-bass-2", 10.5, 2.0, 0.35),
    ("loc", "pop", 11.6, 0.72, 0.32), ("n7244", "ping", 12.3, 1.0, 0.3),
    ("pkg", "whoosh", 14.95, 0.57, 0.33), ("n1400", "pop", 15.5, 0.72, 0.3),
    ("price", "whoosh", 17.45, 0.57, 0.33), ("rm", "impact-bass-1", 17.75, 1.6, 0.42),
    ("route", "whoosh-short", 19.95, 0.57, 0.3), ("pin", "pop", 20.5, 0.72, 0.3), ("km", "ping", 21.8, 1.0, 0.28),
    ("ready", "whoosh", 24.95, 0.57, 0.33), ("c1", "click", 25.4, 0.36, 0.4), ("c2", "click", 27.7, 0.36, 0.4), ("c3", "click", 30.0, 0.36, 0.4),
    ("nb", "whoosh-short", 31.95, 0.57, 0.3), ("nb2", "pop", 32.3, 0.72, 0.3),
    ("cta", "whoosh", 34.95, 0.57, 0.35), ("cta2", "impact-bass-1", 35.3, 1.6, 0.4),
]:
    sfx(*a)

push = [(s[0], s[2], s[3], s[5][0], s[5][1]) for s in SHOTS]
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
      .full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .bw {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(10,16,26,.55) 0%, rgba(10,16,26,.35) 32%, rgba(10,16,26,.05) 50%, rgba(10,16,26,0) 62%, rgba(10,16,26,.3) 82%, rgba(10,16,26,.4) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="shade"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{FILM}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {json.dumps(push)}.forEach(([id, s, e, a, b]) => {{
        tl.fromTo("#" + id + "-w", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, s);
        tl.fromTo("#" + id, {{ scale: a }}, {{ scale: b, duration: e - s, ease: "none" }}, s);
      }});
      tl.to("#root", {{ opacity: 0, duration: 0.6 }}, {FILM - 0.6});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

PIN = f'<svg viewBox="0 0 48 64" width="40" height="52"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
CHECK = f'<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path class="ck" d="M5 12.5 10 17 19 7"/></svg>'
H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.55):
    frm = {"up": "{ opacity: 0, y: 30 }", "scale": "{ opacity: 0, scale: 0.86 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def out(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, y: -16, duration: 0.3, ease: "power2.in" }}, {round(at, 3)});')


def fit(text, size, k, maxw=880):
    lines = re.sub(r"<[^>]+>", "", text.replace("<br/>", "\n")).replace("&amp;", "&").split("\n")
    return int(min(size, maxw / (k * max(len(l) for l in lines))))


def grp(gid, s, e, inner, top, h):
    BOXES.append((gid, top, h))
    H.append(f'    <div class="grp clip" id="{gid}" data-start="{s}" data-duration="{round(e - s, 3)}" style="top:{top}px">{inner}</div>')


def white(t, i, size=58):
    return f'<div class="hw" id="{i}" style="font-size:{fit(t, size, 0.66)}px">{t}</div>'


def yellow(t, i, size=110):
    return f'<div class="hy" id="{i}" style="font-size:{fit(t, size, 0.72)}px">{t}</div>'


def count(sel, to, at, d=1.0, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {round(at, 3)}); }})();')


# 01 hook
grp("g1", 0.3, 3.85, white("PAKEJ BINA RUMAH", "g1w") + yellow("BESERTA TANAH", "g1y", 112)
    + '<div class="rule" id="g1r"></div><div class="hs" id="g1s">KHAS UNTUK ORANG KELANTAN</div>', 340, 330)
tin("#g1w", 0.35); hide("#g1y"); tin("#g1y", 0.6, "scale", 0.6)
J.append('tl.fromTo("#g1r", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, 1.25);')
hide("#g1s"); tin("#g1s", 1.45, "up")
out("#g1", 3.6)

# 02 target audience
grp("g2", 4.2, 7.3, white("PENJAWAT AWAM YANG<br/>NAK BINA RUMAH", "g2w", 60)
    + '<div class="hlw"><div class="hlbg" id="g2bg"></div>' + yellow("TAPI TAKDE TANAH?", "g2y", 96) + '</div>', 360, 340)
tin("#g2w", 4.25); hide("#g2y"); tin("#g2y", 4.95, "scale")
J.append('tl.fromTo("#g2bg", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power3.out" }, 5.25);')
out("#g2", 7.05)

# 03 + 08: 3D land mapping on the top-down drone photo (traced lot, prism extrusion, ground shadow)
k = 1080 / 1449
poly = [(450, 1010), (990, 1010), (990, 1540), (450, 1540)]
P = [(round(x * k), round(y * k)) for x, y in poly]
pts = " ".join(f"{x},{y}" for x, y in P)
cx = round(sum(x for x, _ in P) / 4); cy = round(sum(y for _, y in P) / 4)
layers = "".join(
    f'<svg class="lotsvg ext" viewBox="0 0 1080 1920" width="1080" height="1920" style="transform: translateZ({z}px)">'
    f'<polygon points="{pts}" fill="{YEL}" fill-opacity="0.07" stroke="{YEL}" stroke-opacity="0.35" stroke-width="2"/></svg>'
    for z in range(4, 34, 5))


def mapscene(sid, s, e, tag):
    H.insert(0, f'''    <div class="clip scn3" id="{sid}" data-start="{s}" data-duration="{round(e - s, 3)}">
      <div class="tilt" id="{tag}-tilt"><img src="assets/img/lot-top.jpg" alt="" />
        <svg class="lotsvg" viewBox="0 0 1080 1920" width="1080" height="1920"><polygon class="shadow" points="{pts}" fill="#000" fill-opacity=".35"/></svg>
        <div class="extw" id="{tag}-ext">{layers}</div>
        <svg class="lotsvg top" viewBox="0 0 1080 1920" width="1080" height="1920" style="transform: translateZ(34px)">
          <polygon id="{tag}-fill" points="{pts}" fill="{YEL}" fill-opacity="0.18"/>
          <polygon id="{tag}-line" points="{pts}" fill="none" stroke="{YEL}" stroke-width="8" stroke-linejoin="round"/>
        </svg>
        <div class="lotpin" id="{tag}-pin" style="left:{cx}px; top:{cy}px"><div class="lp-s">7,244 KPS</div></div>
      </div>
    </div>''')


mapscene("s-map", 7.4, 15.0, "m")
J.append('tl.fromTo("#s-map", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 7.4);')
J.append('tl.fromTo("#m-tilt", { rotationX: 0, rotationZ: 0, scale: 1.05, y: 0 }, { rotationX: 46, rotationZ: -6, scale: 1.34, y: -70, duration: 2.6, ease: "power2.inOut" }, 7.5);')
J.append('tl.to("#m-tilt", { rotationZ: 4, duration: 4.9, ease: "sine.inOut" }, 10.1);')
J.append('tl.fromTo("#m-line", { strokeDasharray: 1900, strokeDashoffset: 1900 }, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, 8.4);')
J.append('tl.fromTo("#m-ext", { opacity: 0, scaleZ: 0 }, { opacity: 1, scaleZ: 1, duration: 0.8, ease: "power3.out" }, 10.0);')
J.append('tl.fromTo("#m-fill", { opacity: 0 }, { opacity: 1, duration: 0.6 }, 10.3);')
J.append('tl.fromTo("#m-pin", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 10.6);')
J.append('tl.fromTo("#m-line", { filter: "drop-shadow(0 0 0px #FFD43B)" }, { filter: "drop-shadow(0 0 10px #FFD43B)", duration: 0.8, yoyo: true, repeat: 3, ease: "sine.inOut" }, 10.4);')
grp("g3", 11.4, 14.8, f'<div class="loc" id="g3l">{PIN}<span>KG HUTAN PUTIH, MACHANG</span></div>'
    + white("KELUASAN TANAH", "g3w", 52) + yellow('<span id="n7244">7,244</span> KPS', "g3y", 124), 330, 300)
tin("#g3l", 11.45); hide("#g3w"); tin("#g3w", 11.75); hide("#g3y"); tin("#g3y", 12.0, "scale")
count("#n7244", 7244, 12.0, 1.2)
out("#g3", 14.6)

# 04 package
grp("g4a", 15.4, 17.3, white("BOLEH BINA RUMAH BERMULA", "g4aw", 54) + yellow('<span id="n1400">1,400</span> KPS', "g4ay", 124), 360, 260)
tin("#g4aw", 15.45); hide("#g4ay"); tin("#g4ay", 15.65, "scale"); count("#n1400", 1400, 15.65)
out("#g4a", 17.1)
grp("g4b", 17.45, 19.85, white("HARGA PAKEJ BERMULA", "g4bw", 58) + yellow('<span id="nrm">RM420,000</span>', "g4by", 150)
    + '<div class="rule wide" id="g4br"></div>', 350, 300)
tin("#g4bw", 17.5); hide("#g4by"); tin("#g4by", 17.75, "scale", 0.6); count("#nrm", 420000, 17.75, 1.1, "RM")
J.append('tl.fromTo("#g4br", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, 18.6);')
out("#g4b", 19.6)

# 05 strategic location on the supplied route map (its red route and labels are the user's own)
H.insert(0, '    <div class="clip scn" id="s-route" data-start="20.0" data-duration="5.0"><img id="routeimg" src="assets/img/lot-map.jpg" alt="" /></div>')
J.append('tl.fromTo("#s-route", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 20.0);')
J.append('tl.fromTo("#routeimg", { scale: 1.12 }, { scale: 1.0, duration: 5.0, ease: "power1.out" }, 20.0);')
grp("g5", 20.3, 24.8, '<div class="card" id="g5c"></div>' + white("LOKASI STRATEGIK", "g5w", 60) + yellow("&amp; MUDAH AKSES", "g5y", 100)
    + f'<div class="kmchip" id="g5k">{PIN}<span><b>4 KM</b> DARI BANDAR MACHANG</span></div>', 300, 300)
tin("#g5c", 20.3, "fade", 0.4); tin("#g5w", 20.35); hide("#g5y"); tin("#g5y", 20.6, "scale"); hide("#g5k"); tin("#g5k", 21.8, "up")
out("#g5", 24.55)

# 06 land readiness (drone rising off the empty lot)
items = [("TANAH <b>SEDIA</b> UNTUK BINA RUMAH", 25.4), ("ADA <b>RIZAB JALAN TAR</b>", 27.7), ("SISTEM <b>SALIRAN LONGKANG</b> LENGKAP", 30.0)]
rows = "".join(f'<div class="ckrow" id="ck{i}"><div class="ckb">{CHECK}</div><span>{t}</span></div>' for i, (t, _) in enumerate(items))
grp("g6", 25.3, 31.85, rows, 380, 330)
for i, (_, at) in enumerate(items):
    hide(f"#ck{i}"); tin(f"#ck{i}", at, "up")
    J.append(f'tl.fromTo("#ck{i} .ck", {{ strokeDasharray: 30, strokeDashoffset: 30 }}, {{ strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }}, {at + 0.2});')
out("#g6", 31.6)

# 07 neighbourhood
grp("g7", 32.3, 34.85, white("KAWASAN KEJIRANAN", "g7w", 60) + yellow("SEDIA ADA", "g7y", 124), 360, 260)
tin("#g7w", 32.35); hide("#g7y"); tin("#g7y", 32.6, "scale")
out("#g7", 34.6)

# 08 CTA back on the mapped lot
mapscene("s-end", 35.0, FILM, "e")
J.append('tl.fromTo("#s-end", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 35.0);')
J.append('tl.fromTo("#e-tilt", { rotationX: 46, rotationZ: 4, scale: 1.34, y: -70 }, { rotationX: 46, rotationZ: -2, scale: 1.42, y: -80, duration: 3.0, ease: "sine.inOut" }, 35.0);')
grp("g8", 35.3, FILM, white("ANDA BERMINAT?", "g8w", 64) + yellow("HUBUNGI SEGERA!", "g8y", 120)
    + '<div class="rule" id="g8r"></div>' + f'<div class="loc" id="g8l">{PIN}<span>KG HUTAN PUTIH, MACHANG</span></div>', 330, 330)
tin("#g8w", 35.35); hide("#g8y"); tin("#g8y", 35.6, "scale", 0.6)
J.append('tl.fromTo("#g8r", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, 36.0);')
hide("#g8l"); tin("#g8l", 36.2, "up")

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

SH = "text-shadow: 0 3px 6px rgba(0,0,0,.5), 0 10px 28px rgba(0,0,0,.55);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 800; line-height: 1.06; text-align: center; white-space: nowrap; text-transform: uppercase; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; line-height: 1.0; letter-spacing: -.02em; text-align: center; white-space: nowrap; text-transform: uppercase; color: {YEL}; {SH} }}
    .hs {{ margin-top: 12px; font-weight: 700; font-size: 38px; letter-spacing: .12em; color: {WHT}; {SH} }}
    .rule {{ width: 300px; height: 6px; margin-top: 16px; border-radius: 3px; background: {YEL}; transform-origin: 50% 50%; box-shadow: 0 4px 14px rgba(0,0,0,.4); }}
    .rule.wide {{ width: 640px; }}
    .hlw {{ position: relative; margin-top: 12px; padding: 4px 26px 6px; }}
    .hlbg {{ position: absolute; inset: 0; border-radius: 12px; background: rgba(14,20,29,.72); transform-origin: 0 50%; z-index: -1; }}
    .loc {{ display: flex; align-items: center; gap: 12px; margin: 14px 0 6px; }}
    .loc span {{ font-weight: 800; font-size: 40px; letter-spacing: .04em; color: {WHT}; {SH} }}
    .loc svg {{ filter: drop-shadow(0 4px 8px rgba(0,0,0,.5)); }}
    .card {{ position: absolute; left: 40px; right: 40px; top: -24px; bottom: -6px; border-radius: 22px; background: rgba(12,18,28,.78); z-index: -1; }}
    #g5 {{ isolation: isolate; }}
    .kmchip {{ display: flex; align-items: center; gap: 14px; margin-top: 18px; padding: 12px 26px 12px 18px; border-radius: 999px;
      background: rgba(14,20,29,.78); border: 3px solid {YEL}; }}
    .kmchip span {{ font-weight: 700; font-size: 40px; color: {WHT}; white-space: nowrap; }}
    .kmchip b {{ color: {YEL}; font-weight: 900; }}
    .ckrow {{ display: flex; align-items: center; gap: 20px; width: 960px; margin-bottom: 18px; padding: 16px 24px; border-radius: 16px;
      background: rgba(14,20,29,.72); }}
    .ckb {{ width: 62px; height: 62px; border-radius: 50%; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; }}
    .ckrow span {{ font-weight: 800; font-size: 38px; color: {WHT}; white-space: nowrap; }}
    .ckrow b {{ color: {YEL}; font-weight: 900; }}
    .scn {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; }}
    #routeimg {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; transform-origin: 50% 60%; }}
    .scn3 {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; perspective: 1600px; }}
    .tilt {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 62%; transform-style: preserve-3d; }}
    .tilt img {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    .lotsvg {{ position: absolute; inset: 0; }}
    .shadow {{ filter: blur(14px); transform: translate(10px, 14px); }}
    .extw {{ position: absolute; inset: 0; transform-style: preserve-3d; transform-origin: 50% 50%; }}
    .lotpin {{ position: absolute; transform: translate(-50%, -50%) translateZ(60px) rotateX(-46deg); text-align: center; white-space: nowrap; }}
    .lp-s {{ font-weight: 900; font-size: 58px; color: {WHT}; padding: 8px 22px; border-radius: 12px; background: rgba(14,20,29,.7); border: 3px solid {YEL}; }}
'''
gfx = f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="gfx" data-width="1080" data-height="1920" data-duration="{FILM}">
{chr(10).join(H)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in J).lstrip()}
    window.__timelines["gfx"] = tl;
  </script>
</template>
'''
open("compositions/gfx.html", "w").write(gfx)
print("ok", FILM)
