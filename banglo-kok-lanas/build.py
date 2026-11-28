#!/usr/bin/env python3
"""Mahligai Idaman - Banglo 2,928 kps, Kok Lanas: 50 s cinematic architectural showcase (1080x1920).

Every cut lands on the beat grid of "Lemak Manis" (TikTok sound, ~129.2 BPM, first beat ~0.30 s),
so the song can be added in the app from its start. The song itself is not in the file.
Each shot plays at its own constant speed (slow for hero/detail, fast for pans).
Safe zone: top 15% (Y < 288) and bottom 20% (Y > 1536) carry nothing.
"""
import json, os, re, subprocess

WHT, YEL, INK = "#FFFFFF", "#FFD54A", "#15171B"
SAFE_TOP, SAFE_BOT = 288, 1536
B0, BEAT = 0.302, 60 / 129.2
FILM = 50.0


def b(k):
    return round(B0 + BEAT * k, 3)


# (clip, beats, source in, speed)
SHOTS = [
    ("IMG_6027", 10, 1.0, 0.70),   # hook: wide facade, slow
    ("IMG_6018", 4, 0.4, 0.80),    # car porch front
    ("IMG_6028", 3, 0.5, 1.00),    # front windows
    ("IMG_6024", 4, 0.4, 1.20),    # angled facade
    ("IMG_6015", 3, 1.5, 1.50),    # low angle windows
    ("IMG_6012", 4, 1.0, 1.10),    # pillars
    ("IMG_6029", 3, 0.8, 1.20),    # gable windows
    ("IMG_6031", 2, 0.1, 1.00),    # side wall
    ("IMG_6026", 3, 0.8, 1.60),    # wide with landscaping
    ("IMG_6019", 3, 1.2, 1.00),    # wide house (landscape source, centre crop)
    ("IMG_6054_1HXPF", 3, 1.0, 1.30),  # window grille
    ("IMG_6112", 2, 0.3, 1.00),    # porch view out
    ("IMG_6013", 3, 0.5, 0.75),    # rattan pendant lights
    ("IMG_6075", 2, 0.4, 0.75),    # wall lights
    ("IMG_1995", 4, 0.5, 1.30),    # hall with chandelier
    ("IMG_6037", 3, 0.8, 1.00),    # living hall
    ("IMG_6061", 3, 1.0, 1.30),    # living
    ("IMG_6073", 3, 0.5, 0.70),    # chandelier
    ("IMG_6023", 2, 1.0, 0.80),    # big fan
    ("IMG_1978", 3, 0.8, 1.00),    # kitchen
    ("IMG_1979", 2, 0.8, 1.20),    # kitchen cabinets
    ("IMG_6063_1f13h", 3, 0.8, 1.00),  # kitchen
    ("IMG_6070", 3, 2.0, 1.80),    # kitchen walk-through
    ("IMG_1980", 3, 1.0, 1.50),    # room with glass door
    ("IMG_1981", 2, 1.0, 1.20),    # room
    ("IMG_6041", 3, 2.0, 1.60),    # room
    ("IMG_6043", 2, 0.8, 1.00),    # alcove
    ("IMG_6098", 2, 0.6, 1.00),    # doors
    ("IMG_6051", 2, 1.0, 1.40),    # bathroom
    ("IMG_6093", 3, 2.0, 1.50),    # bathroom with tub
    ("IMG_6081", 2, 0.8, 1.00),    # mosaic wall
    ("IMG_6017", 9, 3.0, 0.80),    # hero: corner of the house, slow
]
assert sum(s[1] for s in SHOTS) == 103, sum(s[1] for s in SHOTS)


def dur(clip):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 f"assets/video/{clip}.mp4"], capture_output=True, text=True).stdout)


vids, push, k = [], [], 0
for i, (clip, nb, src_in, rate) in enumerate(SHOTS):
    s = 0.0 if i == 0 else b(k)
    e = b(k + nb)
    d = round(e - s, 3)
    avail = dur(clip) - src_in - 0.05
    rate = round(min(rate, avail / d), 3)        # never run past the end of the clip
    vids.append(f'      <div id="w{i}" class="bw"><video id="s{i}" class="clip full" src="assets/video/{clip}.mp4" data-start="{s}" '
                f'data-duration="{d}" data-media-start="{src_in}" data-playback-rate="{rate}" data-track-index="1" muted playsinline></video></div>')
    push.append((i, s, d, 1 if i % 2 else -1))
    k += nb
HERO_END = b(103)                                  # outro starts on the beat
OUT = round(FILM - HERO_END, 3)

AUD = []


def sfx(name, f, at, d, v):
    AUD.append(f'      <audio id="sx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{round(at, 3)}" '
               f'data-duration="{d}" data-track-index="{3 + len(AUD) % 3}" data-volume="{v}"></audio>')


sfx("hook", "impact-bass-1", 0.25, 1.6, 0.55); sfx("hookw", "whoosh", 0.15, 0.57, 0.4)
sfx("pin", "pop", 2.2, 0.72, 0.35)
sfx("ext", "whoosh", b(10) - 0.12, 0.57, 0.35); sfx("pr", "riser", b(13) - 1.6, 1.6, 0.18); sfx("price", "impact-bass-1", b(13), 1.6, 0.5)
sfx("det", "whoosh", b(28) - 0.12, 0.57, 0.35); sfx("area", "impact-bass-2", b(30), 2.0, 0.45)
sfx("int", "whoosh-cinematic", b(49) - 1.0, 2.0, 0.3); sfx("bed", "pop", b(51), 0.72, 0.4); sfx("bath", "pop", b(53), 0.72, 0.4)
sfx("feat", "whoosh", b(75) - 0.12, 0.57, 0.35); sfx("off", "pop", b(77), 0.72, 0.4); sfx("sol", "pop", b(79), 0.72, 0.4)
sfx("hr", "riser", b(94) - 2.0, 2.0, 0.2); sfx("hero", "impact-bass-1", b(94), 1.6, 0.45)
sfx("logo", "whoosh", HERO_END - 0.1, 0.57, 0.4); sfx("logo2", "sparkle", HERO_END + 0.3, 1.6, 0.4)

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
      .bw {{ position: absolute; inset: 0; overflow: hidden; }}
      #shade {{ position: absolute; inset: 0; z-index: 3; pointer-events: none;
        background: linear-gradient(180deg, rgba(12,14,18,.6) 0%, rgba(12,14,18,.42) 26%, rgba(12,14,18,.15) 38%, rgba(12,14,18,0) 48%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="shade"></div>
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{FILM}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:5"></div>
{chr(10).join(AUD)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // every shot: a gentle push in or pull out, alternating, for continuous camera life
      {json.dumps(push)}.forEach(([i, s, d, dir]) => {{
        const a = dir > 0 ? 1.0 : 1.07, z = dir > 0 ? 1.07 : 1.0;
        tl.fromTo("#s" + i, {{ scale: a }}, {{ scale: z, duration: d, ease: "none" }}, s);
      }});
      tl.to("#shade", {{ opacity: 0, duration: 0.1 }}, {HERO_END});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(index)

# ---------------- graphics ----------------
def svg(body, size=64, stroke=INK, sw=3.4):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


PIN = f'<svg viewBox="0 0 48 64" width="34" height="45"><path d="M24 1C11.3 1 1 11.3 1 24c0 16.5 23 39 23 39s23-22.5 23-39C47 11.3 36.7 1 24 1z" fill="{YEL}"/><circle cx="24" cy="24" r="8.5" fill="{INK}"/></svg>'
ICON = {
    "bed": svg('<path d="M4 38V12M4 30h40v8M44 30v-6c0-3-2-5-5-5H20v11"/><circle cx="12" cy="24" r="4"/>'),
    "bath": svg('<path d="M4 24h40v4c0 7-5 12-12 12H16C9 40 4 35 4 28z"/><path d="M10 24V10a4 4 0 0 1 8 0"/><path d="M12 40l-2 4M36 40l2 4"/>'),
    "office": svg('<rect x="6" y="9" width="36" height="22" rx="2"/><path d="M2 38h44M18 31l-2 7M30 31l2 7"/>'),
    "solat": svg('<path d="M10 42V14l14-9 14 9v28z"/><path d="M18 42V30a6 6 0 0 1 12 0v12"/><path d="M24 5V1"/>'),
}
H, J, BOXES = [], [], []


def tin(sel, at, kind="up", d=0.45):
    frm = {"up": "{ opacity: 0, y: 26 }", "scale": "{ opacity: 0, scale: 0.86 }", "fade": "{ opacity: 0 }"}[kind]
    J.append(f'tl.fromTo("{sel}", {frm}, {{ opacity: 1, y: 0, scale: 1, duration: {d}, ease: "power3.out" }}, {round(at, 3)});')


def hide(sel):
    J.append(f'tl.set("{sel}", {{ opacity: 0 }}, 0);')


def out(sel, at):
    J.append(f'tl.to("{sel}", {{ opacity: 0, y: -14, duration: 0.25, ease: "power2.in" }}, {round(at, 3)});')


def fit(text, size, k=0.62, maxw=920):
    lines = re.sub(r"<[^>]+>", "", text.replace("<br/>", "\n")).replace("&amp;", "&").split("\n")
    return int(min(size, maxw / (k * max(len(l) for l in lines))))


def grp(gid, s, e, inner, top=330, h=330):
    BOXES.append((gid, top, h))
    H.append(f'    <div class="grp clip" id="{gid}" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" style="top:{top}px">{inner}</div>')
    out(f"#{gid}", e - 0.25)


def count(sel, to, at, d=0.9, prefix=""):
    J.append(f'(() => {{ const o = {{ v: 0 }}; tl.fromTo(o, {{ v: 0 }}, {{ v: {to}, duration: {d}, ease: "power3.out", '
             f'onUpdate: () => {{ document.querySelector("{sel}").textContent = "{prefix}" + Math.round(o.v).toLocaleString("en-US"); }} }}, {round(at, 3)}); }})();')


# hook
grp("g1", 0.2, b(10), f'<div class="hw" id="g1a" style="font-size:{fit("BANGLO 2,928 KPS,", 92)}px">BANGLO 2,928 KPS,</div>'
    f'<div class="hy" id="g1b" style="font-size:{fit("SIAP ADA MINI OFFICE", 96)}px">SIAP ADA MINI OFFICE</div>'
    f'<div class="hy" id="g1c" style="font-size:{fit("SIAP ADA MINI OFFICE", 96)}px">&amp; BILIK SOLAT!</div>'
    f'<div class="loc" id="g1l">{PIN}<span>Kok Lanas, Kelantan</span></div>', 320, 420)
tin("#g1a", 0.25, "scale", 0.5)
for sel, at in [("#g1b", b(2)), ("#g1c", b(3)), ("#g1l", b(4))]:
    hide(sel); tin(sel, at, "up")

# price
grp("g2", b(13), b(27), '<div class="hw" id="g2a" style="font-size:60px">HARGA ASAS BERMULA</div>'
    '<div class="hy" id="g2b" style="font-size:150px"><span id="nrm">RM483,120</span></div><div class="rule" id="g2r"></div>')
tin("#g2a", b(13)); hide("#g2b"); tin("#g2b", b(14), "scale", 0.5); count("#nrm", 483120, b(14), 1.0, "RM")
J.append(f'tl.fromTo("#g2r", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out" }}, {b(16)});')

# floor area
grp("g3", b(30), b(47), '<div class="hw" id="g3a" style="font-size:72px">KELUASAN</div>'
    '<div class="hy" id="g3b" style="font-size:150px"><span id="nkps">2,928</span> KPS</div>')
tin("#g3a", b(30)); hide("#g3b"); tin("#g3b", b(31), "scale", 0.5); count("#nkps", 2928, b(31), 0.9)


def badges(gid, s, e, items):
    inner = "".join(f'<div class="bd" id="{gid}{i}"><div class="bi">{ICON[ic]}</div><div class="bt"><b>{n}</b> {t}</div></div>'
                    for i, (ic, n, t) in enumerate(items))
    grp(gid, s, e, f'<div class="bds">{inner}</div>', 340, 300)
    for i in range(len(items)):
        hide(f"#{gid}{i}"); tin(f"#{gid}{i}", s + i * 2 * BEAT, "up")


badges("g4", b(51), b(73), [("bed", "4", "BILIK TIDUR"), ("bath", "4", "BILIK AIR")])
badges("g5", b(77), b(92), [("office", "1", "MINI OFFICE"), ("solat", "1", "BILIK SOLAT")])

# hero
grp("g6", b(95), HERO_END - 0.05, '<div class="hw" id="g6a" style="font-size:68px">BINA RUMAH IMPIAN ANDA</div>'
    f'<div class="hy" id="g6b" style="font-size:{fit("BERSAMA MAHLIGAI IDAMAN", 100)}px">BERSAMA MAHLIGAI IDAMAN</div>')
tin("#g6a", b(95)); hide("#g6b"); tin("#g6b", b(97), "scale", 0.5)

# outro: logo reveal on charcoal, on the beat
H.append(f'''    <div class="clip outro" id="outro" data-start="{HERO_END}" data-duration="{OUT}"><div class="glow" id="glow"></div>
      <img id="logo" src="assets/img/logo.png" alt="" /><div class="shine" id="shine"></div></div>''')
J.append(f'tl.fromTo("#outro", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {HERO_END});')
J.append(f'tl.fromTo("#logo", {{ opacity: 0, scale: 0.8, filter: "blur(8px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }}, {HERO_END + 0.1});')
J.append(f'tl.fromTo("#glow", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "power2.out" }}, {HERO_END + 0.1});')
J.append(f'tl.fromTo("#shine", {{ x: -700 }}, {{ x: 700, duration: 0.8, ease: "power2.inOut" }}, {HERO_END + 0.7});')

for bid, top, h in BOXES:
    assert SAFE_TOP <= top and top + h <= SAFE_BOT, (bid, top, h)

SH = "text-shadow: 0 2px 4px rgba(0,0,0,.35), 0 4px 18px rgba(0,0,0,.45);"
CSS = f'''
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; color: {WHT}; }}
    .grp {{ position: absolute; left: 30px; right: 30px; display: flex; flex-direction: column; align-items: center; }}
    .hw {{ font-weight: 900; line-height: 1.02; letter-spacing: -.01em; text-align: center; white-space: nowrap; color: {WHT}; {SH} }}
    .hy {{ font-weight: 900; line-height: 1.0; letter-spacing: -.02em; text-align: center; white-space: nowrap; color: {YEL}; {SH} }}
    .loc {{ display: flex; align-items: center; gap: 12px; margin-top: 18px; }}
    .loc span {{ font-weight: 700; font-size: 42px; color: {WHT}; {SH} }}
    .rule {{ width: 300px; height: 7px; margin-top: 14px; border-radius: 4px; background: {YEL}; }}
    .bds {{ display: flex; flex-direction: column; gap: 18px; align-items: center; }}
    .bd {{ display: flex; align-items: center; gap: 24px; width: 820px; padding: 16px 28px 16px 16px; border-radius: 18px; background: rgba(21,23,27,.72); }}
    .bi {{ width: 110px; height: 110px; border-radius: 14px; background: {YEL}; display: flex; align-items: center; justify-content: center; flex: none; }}
    .bt {{ font-weight: 900; font-size: 64px; color: {WHT}; white-space: nowrap; }}
    .bt b {{ color: {YEL}; font-weight: 900; }}
    .outro {{ position: absolute; inset: 0; background: {INK}; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    .glow {{ position: absolute; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(255,213,74,.22) 0%, rgba(255,213,74,0) 65%); }}
    #logo {{ position: relative; width: 560px; height: auto; }}
    .shine {{ position: absolute; width: 220px; height: 1920px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.35), transparent); transform: skewX(-18deg); mix-blend-mode: overlay; }}
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
print("shots", len(SHOTS), "hero_end", HERO_END, "outro", OUT)
