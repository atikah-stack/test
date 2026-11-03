#!/usr/bin/env python3
# Builds the scenes, caption track and index.html for the split-level styles video.
# Run from the project folder:  python3 build-scenes.py .
# Scene timing and captions follow the voiceover transcript (assets/audio/transcript.json).
import difflib, html, json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(f"{OUT}/compositions", exist_ok=True)

YEL = "#F6C343"
INK = "#12151B"

# ---------------------------------------------------------------- voiceover words
tr = json.load(open(f"{OUT}/assets/audio/transcript.json"))
WW = tr if isinstance(tr, list) else tr.get("words", tr)


def wt(word, after=0.0):
    """Start time of the first transcript word containing `word` after `after` seconds."""
    for w in WW:
        if w["start"] >= after and word in w["text"].lower():
            return round(w["start"], 2)
    raise KeyError(word)


SCENES = [("s01", 0, 7.45), ("s02", 7.45, 8.0), ("s03", 15.45, 10.35), ("s04", 25.8, 5.25), ("s05", 31.05, 4.85),
          ("s06", 35.9, 2.16), ("s07", 38.06, 2.63), ("s08", 40.69, 2.26), ("s09", 42.95, 4.87), ("s10", 47.82, 11.13),
          ("s11", 58.95, 3.75), ("s12", 62.7, 5.3), ("s13", 68.0, 5.0)]
START = {c: s for c, s, d in SCENES}
TOTAL = round(SCENES[-1][1] + SCENES[-1][2], 2)

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; font-family: Montserrat, sans-serif; color: #fff; }}
    #root .shot {{ position: absolute; inset: 0; overflow: hidden; }}
    #root .shot .sbg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #root .frame {{ position: absolute; left: 0; top: 0; width: 3413px; height: 1920px; transform-origin: 0 50%; }}
    #root .dimv {{ position: absolute; inset: 0; background: rgba(8,10,14,.62); }}
    #root .frame img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    #root .frame svg {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible; }}
    #root .tshade {{ position: absolute; left: 0; top: 0; width: 1080px; height: 640px; z-index: 2;
      background: linear-gradient(rgba(8,10,14,.85), rgba(8,10,14,.55) 55%, rgba(8,10,14,0)); }}
    #root .t {{ position: absolute; left: 40px; right: 40px; text-align: center; z-index: 3; text-transform: uppercase;
      font-weight: 900; color: #fff; line-height: 1.02; text-shadow: 0 4px 0 rgba(0,0,0,.3), 0 10px 30px rgba(0,0,0,.7); }}
    #root .y {{ color: {YEL}; }}
    #root .ser {{ font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700; text-transform: none; color: {YEL}; }}
    #root .num {{ position: absolute; left: 0; right: 0; text-align: center; z-index: 3; font-weight: 700; font-size: 28px;
      letter-spacing: .34em; color: {YEL}; }}
    #root .chip {{ position: absolute; z-index: 3; padding: 12px 24px; background: rgba(12,14,18,.82); border: 2px solid {YEL};
      border-radius: 999px; font-weight: 800; font-size: 34px; letter-spacing: .12em; text-transform: uppercase; color: #fff; white-space: nowrap; }}
    #root video.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    #root .vwrap {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
    #root .acard {{ position: absolute; width: 444px; height: 250px; overflow: hidden; border-radius: 14px; border: 3px solid rgba(255,255,255,.9);
      box-shadow: 0 20px 50px rgba(0,0,0,.5); }}
    #root .acard img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    #root .acard span {{ position: absolute; left: 10px; bottom: 10px; padding: 6px 12px; background: rgba(12,14,18,.85); color: #fff;
      font-weight: 800; font-size: 28px; letter-spacing: .06em; border-radius: 6px; text-transform: uppercase; }}
"""

HELPERS = """
    const tl = gsap.timeline({ paused: true });
"""


def scene(cid, css, body, js, shade=True):
    dur = next(d for c, s, d in SCENES if c == cid)
    with open(f"{OUT}/compositions/{cid}.html", "w") as f:
        f.write(f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{dur}">
{body}
{'    <div class="tshade"></div>' if shade else ''}
  </div>
  <script>{HELPERS}{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")


def shot(id_, key, overlay=""):
    """A house image filling the whole 9:16 frame; the camera pans across the facade."""
    svg = f'<svg viewBox="0 0 2560 1440" preserveAspectRatio="none">{overlay}</svg>' if overlay else ""
    return f"""    <div class="shot" id="{id_}">
      <div class="frame" id="{id_}-f"><img src="assets/img/{key}.jpg" alt="" />{svg}</div>
    </div>"""


FW = 3413  # full-bleed width of a 16:9 image at 1920 px tall


def px(f, s):
    """x offset that puts fraction f (0 = left edge, 1 = right edge) of the image in view at scale s."""
    return round(-f * (FW * s - 1080))


# where each facade is framed: (pan from, pan to) as fractions across the image
PAN = {"modern": (0.2, 0.62), "muji": (0.3, 0.62), "english": (0.74, 0.38), "nordic": (0.25, 0.6), "malay": (0.62, 0.36), "kemaman3d": (0.2, 0.6)}


def move(id_, t, dur, f0, f1, s0=1.0, s1=1.05, ease="sine.inOut"):
    return f'    tl.fromTo("#{id_}-f", {{ scale: {s0}, x: {px(f0, s0)} }}, {{ scale: {s1}, x: {px(f1, s1)}, duration: {dur}, ease: "{ease}" }}, {t});\n'


def rise(sel, t, dur=0.5, y=40):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "power4.out" }}, {t});\n'


# polygon masks for architecture wipes (4 points: TL, TR, BR, BL; x in %)
def poly(xtl, xtr, xbr, xbl):
    return f"polygon({xtl}% 0%, {xtr}% 0%, {xbr}% 100%, {xbl}% 100%)"


MASKS = {
    "roof_lr": (poly(0, 0, -45, 0), poly(0, 145, 100, 0)),          # diagonal roofline sweep, left to right
    "roof_rl": (poly(100, 100, 100, 145), poly(-45, 100, 100, 0)),   # diagonal roofline sweep, right to left
    "wall": (poly(0, 0, 0, 0), poly(0, 100, 100, 0)),                # wall-edge wipe
    "columns": ("inset(0% 50% 0% 50%)", "inset(0% 0% 0% 0%)"),       # opening between two columns
    "door": ("inset(77% 26% 10% 55%)", "inset(0% 0% 0% 0%)"),        # doorway reveal (English door)
}


def wipe(sel, kind, t, dur=0.6):
    a, b = MASKS[kind]
    return f'    tl.fromTo("{sel}", {{ clipPath: "{a}" }}, {{ clipPath: "{b}", duration: {dur}, ease: "power3.inOut" }}, {t});\n'


def style_title(pre, num, name, desc):
    size = 92 if len(name) <= 14 else 74
    d = f'<div class="t ser" id="{pre}-ds" style="top:{318 if size == 92 else 300}px; font-size:66px">{desc}</div>' if desc else ""
    return f"""    <div class="num" id="{pre}-n" style="top:196px">{num}</div>
    <div class="t" id="{pre}-nm" style="top:236px; font-size:{size}px">{name}</div>
    {d}"""


def title_in(pre, t, desc=True):
    js = rise(f"#{pre}-n", t, 0.4, 20) + rise(f"#{pre}-nm", t + 0.08, 0.5)
    if desc:
        js += f'    tl.fromTo("#{pre}-ds", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {t + 0.25});\n'
    return js


# ---------------------------------------------------------------- S01 HOOK MONTAGE
HOOK = [("modern", 0.0), ("nordic", 1.55), ("muji", 3.05), ("malay", 4.55), ("english", 6.0)]
body = "\n".join(shot(f"s01-{k}", k) for k, _ in HOOK)
body += f"""
    <div class="t" id="s01-k" style="top:212px; font-size:40px; letter-spacing:.32em; font-weight:800"><span class="y">Design rumah</span></div>
    <div class="t" id="s01-h" style="top:256px; font-size:124px; letter-spacing:-.01em">Split<br />Level</div>"""
js = ""
for i, (k, t) in enumerate(HOOK):
    end = HOOK[i + 1][1] if i + 1 < len(HOOK) else 7.45
    if i:
        js += f'    tl.fromTo("#s01-{k}", {{ opacity: 0, clipPath: "{MASKS["columns"][0]}" }}, {{ opacity: 1, clipPath: "{MASKS["columns"][1]}", duration: 0.35, ease: "power3.out" }}, {t});\n'
    js += move(f"s01-{k}", t, round(end - t + 0.4, 2), PAN[k][0], PAN[k][1], 1.12, 1.0, "power2.out")
css1 = "\n".join(f"    #s01-{k} {{ opacity: 0; }}" for k, _ in HOOK[1:])
js += """    tl.fromTo("#s01-h", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, 0);
    tl.fromTo("#s01-k", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.25);
    tl.to("#s01-h", { scale: 1.06, duration: 6.4, ease: "sine.inOut" }, 0.6);
"""
scene("s01", css1, body, js)

# ---------------------------------------------------------------- S02 KEMAMAN HERO
t_kem = round(wt("kemaman") - START["s02"], 2)
scene("s02", """
    #s02-b { opacity: 0; }
    #s02-loc { position: absolute; left: 60px; top: 230px; z-index: 3; display: flex; align-items: center; gap: 18px; opacity: 0; }
    #s02-loc .pin { width: 58px; height: 58px; }
    #s02-loc .l1 { font-weight: 900; font-size: 52px; letter-spacing: .08em; line-height: 1; text-shadow: 0 6px 20px rgba(0,0,0,.6); }
    #s02-loc .l2 { font-weight: 700; font-size: 30px; letter-spacing: .3em; color: """ + YEL + """; margin-top: 6px; }
""", f"""    <div class="vwrap" id="s02-a"><video id="s02-v1" class="clip full" src="assets/video/kem-approach.mp4" data-start="0" data-duration="5.4" data-media-start="0.5" muted playsinline></video></div>
    <div class="vwrap" id="s02-b"><video id="s02-v2" class="clip full" src="assets/video/kem-porch.mp4" data-start="5.3" data-duration="2.7" data-media-start="1.0" muted playsinline></video></div>
    <div id="s02-loc"><svg class="pin" viewBox="0 0 24 24"><path d="M12 2C7.6 2 4 5.4 4 9.8 4 15.5 12 22 12 22s8-6.5 8-12.2C20 5.4 16.4 2 12 2z" fill="{YEL}"/><circle cx="12" cy="9.8" r="3.2" fill="{INK}"/></svg>
      <div><div class="l1">KEMAMAN</div><div class="l2">TERENGGANU</div></div></div>""", f"""
    tl.fromTo("#s02-a", {{ scale: 1.0 }}, {{ scale: 1.1, duration: 5.4, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s02-loc", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, {max(0.4, t_kem - 0.1)});
    tl.fromTo("#s02-b", {{ opacity: 1, clipPath: "{MASKS['wall'][0]}" }}, {{ opacity: 1, clipPath: "{MASKS['wall'][1]}", duration: 0.55, ease: "power3.inOut" }}, 5.3);
    tl.fromTo("#s02-b", {{ scale: 1.22 }}, {{ scale: 1.0, duration: 2.6, ease: "power2.out" }}, 5.3);
""")

# ---------------------------------------------------------------- S03 SPLIT LEVEL EXPLAINED (Modern Tropical render)
LV = f"""
<g id="s03-l1"><line x1="70" y1="1086" x2="1060" y2="1086" stroke="{YEL}" stroke-width="7" stroke-dasharray="26 14" pathLength="1" />
  <line x1="530" y1="874" x2="530" y2="1086" stroke="{YEL}" stroke-width="5" /><rect x="340" y="780" width="380" height="94" rx="14" fill="rgba(12,14,18,.88)" stroke="{YEL}" stroke-width="4"/><text x="530" y="844" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="58" fill="#fff" letter-spacing="5">LEVEL 01</text></g>
<g id="s03-l2"><line x1="1360" y1="890" x2="2440" y2="890" stroke="#fff" stroke-width="7" stroke-dasharray="26 14" />
  <rect x="1420" y="779" width="380" height="94" rx="14" fill="rgba(12,14,18,.88)" stroke="#fff" stroke-width="4"/><text x="1610" y="843" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="58" fill="{YEL}" letter-spacing="5">LEVEL 02</text></g>
<g id="s03-up"><line x1="1250" y1="1080" x2="1250" y2="905" stroke="{YEL}" stroke-width="8" /><path d="M1222 935 L1250 895 L1278 935" fill="none" stroke="{YEL}" stroke-width="8" stroke-linejoin="round" />
  <line x1="1215" y1="1086" x2="1285" y2="1086" stroke="{YEL}" stroke-width="6" /><line x1="1215" y1="890" x2="1285" y2="890" stroke="{YEL}" stroke-width="6" /></g>"""
scene("s03", "#s03-l1, #s03-l2, #s03-up { opacity: 0; } #s03-i1, #s03-i2 { opacity: 0; }", shot("s03-m", "modern", LV) + """
    <div class="vwrap" id="s03-i1"><video id="s03-v1" class="clip full" src="assets/video/interior-stairs.mp4" data-start="5.35" data-duration="2.55" data-media-start="1.0" muted playsinline></video></div>
    <div class="vwrap" id="s03-i2"><video id="s03-v2" class="clip full" src="assets/video/interior-room.mp4" data-start="7.85" data-duration="2.5" data-media-start="0.6" muted playsinline></video></div>
    <div class="t" id="s03-h" style="top:206px; font-size:96px">Split <span class="y">level</span></div>
    <div class="t ser" id="s03-d" style="top:320px; font-size:62px">aras lantai berbeza</div>
    <div class="t" id="s03-u" style="top:420px; font-size:40px; letter-spacing:.2em; font-weight:800">Unik <span class="y">•</span> Ada karakter</div>""", f"""
{move("s03-m", 0, 5.5, 0.13, 0.63, 1.0, 1.0)}{rise("#s03-h", 0.1)}{rise("#s03-d", 1.4, 0.6, 24)}
    tl.fromTo("#s03-l1", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, 0.8);
    tl.fromTo("#s03-up", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "back.out(2)" }}, 2.6);
    tl.fromTo("#s03-l2", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 4.5);
    tl.fromTo("#s03-i1", {{ opacity: 1, clipPath: "{MASKS['wall'][0]}" }}, {{ opacity: 1, clipPath: "{MASKS['wall'][1]}", duration: 0.55, ease: "power3.inOut" }}, 5.35);
    tl.fromTo("#s03-i1", {{ scale: 1.12 }}, {{ scale: 1.0, duration: 2.5, ease: "power2.out" }}, 5.35);
    tl.fromTo("#s03-i2", {{ opacity: 1, clipPath: "{MASKS['columns'][0]}" }}, {{ opacity: 1, clipPath: "{MASKS['columns'][1]}", duration: 0.5, ease: "power3.inOut" }}, 7.85);
    tl.fromTo("#s03-i2", {{ scale: 1.0 }}, {{ scale: 1.08, duration: 2.5, ease: "sine.inOut" }}, 7.85);
    tl.to("#s03-d", {{ opacity: 0, duration: 0.2 }}, 5.3);
{rise("#s03-u", round(wt("unik") - START["s03"], 2), 0.5, 24)}""")

# ---------------------------------------------------------------- S04 PATTERN INTERRUPT: one house -> many
GRID = [("modern", "Modern Tropical"), ("muji", "Muji"), ("english", "English"), ("nordic", "Nordic"), ("malay", "Malay Traditional")]
POS = [(32, 300), (556, 300), (32, 610), (556, 610), (294, 920)]
t_bukan = round(wt("bukan") - START["s04"], 2)
cards = "\n".join(f'    <div class="acard" id="s04-c{i}" style="left:{x}px; top:{y}px; width:492px; height:290px"><img src="assets/img/{k}.jpg" alt="" /><span>{n}</span></div>'
                  for i, ((k, n), (x, y)) in enumerate(zip(GRID, POS)))
js = f'{move("s04-one", 0, 1.8, 0.5, 0.42, 1.0, 1.05)}'
js += f'    tl.to("#s04-one", {{ scale: 0.46, opacity: 0, duration: 0.5, ease: "power3.in" }}, 1.65);\n'
for i, (x, y) in enumerate(POS):
    dx, dy = 540 - (x + 246), 860 - (y + 150)
    js += f'    tl.fromTo("#s04-c{i}", {{ opacity: 0, x: {dx}, y: {dy}, scale: 0.6 }}, {{ opacity: 1, x: 0, y: 0, scale: 1, duration: 0.55, ease: "expo.out" }}, {round(1.75 + i * 0.05, 2)});\n'
js += f'    tl.fromTo("#s04-h", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }}, {max(1.9, t_bukan)});\n'
scene("s04", "#s04-h { opacity: 0; } #s04-one { transform-origin: 50% 45%; }", """    <video id="s04-bgv" class="clip full" src="assets/video/interior-family.mp4" data-start="0" data-duration="5.25" data-media-start="1.0" muted playsinline></video>
    <div class="dimv"></div>
""" + shot("s04-one", "malay") + "\n" + cards + """
    <div class="t" id="s04-h" style="top:200px; font-size:82px">Bukan <span class="y">satu style</span> je</div>""", js)

# ---------------------------------------------------------------- S05 COLLECTION GALLERY
GAL = [("modern", "Modern Tropical"), ("muji", "Muji Style"), ("english", "English Style"), ("nordic", "Nordic Style"), ("malay", "Malay Traditional")]
gal = "\n".join(f'      <div class="gc" style="left:{i * 740}px"><img src="assets/img/{k}.jpg" alt="" /><b>{n}</b></div>' for i, (k, n) in enumerate(GAL))
scene("s05", f"""
    #s05-row {{ position: absolute; left: 0; top: 500px; height: 960px; width: 4500px; }}
    #s05-row2 {{ position: absolute; left: 0; top: 1060px; height: 120px; width: 4300px; opacity: .35; }}
    #root .gc {{ position: absolute; top: 0; width: 700px; height: 960px; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.55); }}
    #root .gc img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    #root .gc b {{ position: absolute; left: 20px; bottom: 18px; font-weight: 900; font-size: 36px; text-transform: uppercase; letter-spacing: .05em;
      text-shadow: 0 4px 16px rgba(0,0,0,.8); }}
""", f"""    <video id="s05-bgv" class="clip full" src="assets/video/interior-room.mp4" data-start="0" data-duration="4.85" data-media-start="5.0" muted playsinline></video>
    <div class="dimv"></div>
    <div id="s05-row">
{gal}
    </div>
    <div class="num" id="s05-n" style="top:206px">Mahligai Idaman</div>
    <div class="t" id="s05-h" style="top:252px; font-size:84px">Koleksi design<br /><span class="y">split level</span></div>""", """
    tl.fromTo("#s05-row", { x: 1000 }, { x: -2770, duration: 4.85, ease: "power2.inOut" }, 0);
    tl.fromTo("#s05-row .gc", { rotateY: 0, scale: 0.92 }, { scale: 1, duration: 0.6, stagger: 0.12, ease: "power2.out" }, 0);
""" + rise("#s05-n", 0.1, 0.4, 20) + rise("#s05-h", 0.2))

# ---------------------------------------------------------------- S06-S09 STYLE SHOWCASE (architecture wipes)
def style_scene(cid, items, prev=None):
    """items: [(key, local_start, local_end, mask, num, name, desc)]; prev: (key, scale, x) shown under the first wipe."""
    body = ""
    js = ""
    css = ""
    if prev:
        body += shot(f"{cid}-p", prev[0]) + "\n"
        js += f'    tl.set("#{cid}-p-f", {{ scale: 1.05, x: {px(PAN[prev[0]][1], 1.05)} }}, 0);\n'
    for i, (key, t0, t1, mask, num, name, desc) in enumerate(items):
        sid = f"{cid}-{key}"
        body += shot(sid, key) + "\n"
        body += style_title(f"{cid}-t{i}", num, name, desc) + "\n"
        js += wipe(f"#{sid}", mask, t0)
        js += move(sid, t0, round(t1 - t0 + 0.3, 2), PAN[key][0], PAN[key][1], 1.0, 1.05)
        js += title_in(f"{cid}-t{i}", t0 + 0.2, bool(desc))
        if i + 1 < len(items):
            js += f'    tl.to(["#{cid}-t{i}-n", "#{cid}-t{i}-nm"{", " + chr(34) + "#" + cid + "-t" + str(i) + "-ds" + chr(34) if desc else ""}], {{ opacity: 0, duration: 0.2 }}, {t1 - 0.05});\n'
    scene(cid, css, body, js)


style_scene("s06", [("modern", 0, 2.16, "columns", "01 / 05", "Modern Tropical", "Elegant")], prev=None)
style_scene("s07", [("muji", 0, 2.63, "roof_lr", "02 / 05", "Muji Style", "Simple • Calm")], prev=("modern",))
style_scene("s08", [("english", 0, 2.26, "door", "03 / 05", "English Style", "Classic")], prev=("muji",))
t_malay = round(wt("malay") - START["s09"], 2)
style_scene("s09", [("nordic", 0, t_malay, "wall", "04 / 05", "Nordic Style", "Cozy"),
                    ("malay", t_malay, 4.87, "roof_rl", "05 / 05", "Malay Traditional", "")], prev=("english",))

# ---------------------------------------------------------------- S10 IN-HOUSE DESIGNER: SKETCH -> FLOOR PLAN -> 3D -> HOUSE
S10 = START["s10"]
k1, k2, k3 = (round(wt(w, S10) - S10, 2) for w in ("cita", "gaya", "kesesuaian"))
steps = ["Sketch", "Floor plan", "3D design", "House"]
stp = "".join(f'<span id="s10-st{i}">{s}</span>' + ('<i>→</i>' if i < 3 else '') for i, s in enumerate(steps))
scene("s10", f"""
    #s10-paper {{ position: absolute; inset: 0; background: #F7F6F2; background-image: linear-gradient(rgba(30,40,60,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(30,40,60,.06) 1px, transparent 1px); background-size: 54px 54px; }}
    #s10-up, #s10-gr {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
    #s10-up {{ width: 2200px; height: 1800px; }}
    #s10-gr {{ width: 2200px; height: 2040px; opacity: 0; }}
    #s10-up img, #s10-gr img {{ width: 100%; height: 100%; display: block; }}
    #s10-pen {{ position: absolute; left: 0; top: 0; width: 8px; height: 1920px; background: {YEL}; box-shadow: 0 0 24px {YEL}; opacity: 0; z-index: 2; }}
    #s10-3d, #s10-house {{ opacity: 0; }}
    #s10-steps {{ position: absolute; left: 30px; right: 30px; top: 470px; z-index: 3; display: flex; justify-content: center; align-items: center; gap: 10px;
      font-weight: 800; font-size: 28px; letter-spacing: .06em; text-transform: uppercase; color: rgba(255,255,255,.45); }}
    #s10-steps span {{ padding: 8px 14px; border-radius: 999px; border: 2px solid rgba(255,255,255,.25); background: rgba(12,14,18,.6); }}
    #s10-steps i {{ font-style: normal; color: rgba(255,255,255,.4); }}
    #root .kw {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; z-index: 3; opacity: 0; }}
    #root .kw b {{ padding: 14px 30px; background: {YEL}; color: {INK}; font-weight: 900; font-size: 44px; letter-spacing: .08em; border-radius: 12px;
      box-shadow: 0 14px 34px rgba(0,0,0,.35); }}
""", f"""    <div id="s10-paper"></div>
    <div id="s10-up"><img src="assets/img/plan-upper-hd.png" alt="" /></div>
    <div id="s10-gr"><img src="assets/img/plan-ground-hd.png" alt="" /></div>
    <div id="s10-pen"></div>
{shot("s10-3d", "kemaman3d")}
    <div class="vwrap" id="s10-house"><video id="s10-hv" class="clip full" src="assets/video/kem-orbit-right.mp4" data-start="8.0" data-duration="3.13" data-media-start="5.2" muted playsinline></video></div>
    <div class="t" id="s10-h" style="top:206px; font-size:84px">Pelukis pelan<br /><span class="y">sendiri</span></div>
    <div id="s10-steps">{stp}</div>
    <div class="kw" id="s10-k1" style="top:900px"><b>Cita rasa</b></div>
    <div class="kw" id="s10-k2" style="top:1000px"><b>Gaya hidup</b></div>
    <div class="kw" id="s10-k3" style="top:1100px"><b>Kesesuaian tanah</b></div>""", f"""
    tl.set("#s10-up", {{ x: -32, y: 560, scale: 0.52 }}, 0);
    tl.fromTo("#s10-up", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 2.4, ease: "power1.inOut" }}, 0.1);
    tl.fromTo("#s10-pen", {{ opacity: 1, x: -32 }}, {{ opacity: 1, x: 1112, duration: 2.4, ease: "power1.inOut" }}, 0.1);
    tl.to("#s10-pen", {{ opacity: 0, duration: 0.2 }}, 2.5);
    tl.to("#s10-up", {{ scale: 0.62, x: -300, y: 470, duration: 0.6, ease: "power2.inOut" }}, 2.45);
    tl.fromTo("#s10-gr", {{ opacity: 1, clipPath: "inset(100% 0% 36% 0%)", x: -480, y: 300, scale: 0.9 }}, {{ opacity: 1, clipPath: "inset(0% 0% 36% 0%)", duration: 0.55, ease: "power3.inOut" }}, 3.0);
    tl.to("#s10-gr", {{ scale: 1.0, x: -560, y: 260, duration: 2.6, ease: "sine.inOut" }}, 3.0);
    tl.fromTo("#s10-3d", {{ opacity: 1, clipPath: "{MASKS['roof_lr'][0]}" }}, {{ opacity: 1, clipPath: "{MASKS['roof_lr'][1]}", duration: 0.6, ease: "power3.inOut" }}, 5.6);
{move("s10-3d", 5.6, 2.6, 0.2, 0.6, 1.0, 1.05)}
    tl.fromTo("#s10-house", {{ opacity: 1, clipPath: "{MASKS['columns'][0]}", scale: 1.1 }}, {{ opacity: 1, clipPath: "{MASKS['columns'][1]}", scale: 1.0, duration: 0.6, ease: "power3.inOut" }}, 8.0);
{rise("#s10-h", 0.15)}{rise("#s10-steps", 0.5, 0.4, 20)}
""" + "".join(f'    tl.to("#s10-st{i}", {{ color: "{INK}", backgroundColor: "{YEL}", borderColor: "{YEL}", duration: 0.2 }}, {t});\n' + (f'    tl.to("#s10-st{i - 1}", {{ color: "#ffffff", backgroundColor: "rgba(12,14,18,.6)", borderColor: "rgba(255,255,255,.25)", duration: 0.2 }}, {t});\n' if i else "")
              for i, t in enumerate([0.3, 3.0, 5.6, 8.0]))
    + "".join(f'    tl.fromTo("#s10-k{i + 1}", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {t});\n' for i, t in enumerate((k1, k2, k3))))

# ---------------------------------------------------------------- S11 SOLUTION: cards gather
SOL = ["modern", "muji", "english", "nordic", "malay"]
FROM = [(-700, -500, -18), (760, -420, 16), (-760, 380, 12), (760, 460, -14), (0, 900, 0)]
END = [(-300, -20, -8), (300, -30, 7), (-150, 40, -3), (160, 40, 4), (0, 0, 0)]
cards = "\n".join(f'    <div class="acard sc" id="s11-c{i}" style="left:{318}px; top:{735}px; width:444px; height:250px"><img src="assets/img/{k}.jpg" alt="" /></div>' for i, k in enumerate(SOL))
js = ""
for i in range(5):
    fx, fy, fr = FROM[i]; ex, ey, er = END[i]
    js += f'    tl.fromTo("#s11-c{i}", {{ opacity: 0, x: {fx}, y: {fy}, rotation: {fr}, scale: 1.25 }}, {{ opacity: 1, x: {fx // 3}, y: {fy // 3}, rotation: {fr // 2}, scale: 1.25, duration: 0.45, ease: "power3.out" }}, {round(0.05 + i * 0.22, 2)});\n'
    js += f'    tl.to("#s11-c{i}", {{ x: {ex}, y: {ey}, rotation: {er}, scale: {1.35 if i == 4 else 1.05}, duration: 0.8, ease: "expo.inOut" }}, 1.9);\n'
scene("s11", f"""

""", '    <video id="s11-bgv" class="clip full" src="assets/video/interior-stairs.mp4" data-start="0" data-duration="3.75" data-media-start="4.5" muted playsinline></video>\n    <div class="dimv"></div>\n' + cards + f"""
    <div class="t" id="s11-h" style="top:1080px; font-size:40px; letter-spacing:.24em; font-weight:800">Mahligai <span class="y">Idaman</span></div>""", js + rise("#s11-h", 2.6, 0.5, 20), shade=False)

# ---------------------------------------------------------------- S12 CTA
S12 = START["s12"]
t_kel = round(wt("kelantan", S12) - S12, 2)
t_hub = round(wt("hubungi", S12) - S12, 2)
scene("s12", """
    #s12-fade { position: absolute; inset: 0; background: #000; opacity: 0; z-index: 5; }
    #s12-b { position: absolute; left: 60px; right: 60px; top: 760px; z-index: 3; display: flex; justify-content: center; opacity: 0; }
    #s12-b span { padding: 18px 34px; background: """ + YEL + f"""; color: {INK}; font-weight: 900; font-size: 54px; letter-spacing: .06em; border-radius: 14px; }}
""", f"""    <div class="vwrap" id="s12-v"><video id="s12-vid" class="clip full" src="assets/video/kem-orbit-left.mp4" data-start="0" data-duration="5.3" data-media-start="5.6" muted playsinline></video></div>
    <div class="t" id="s12-l1" style="top:206px; font-size:74px">Bina rumah<br />split level</div>
    <div class="t y" id="s12-l2" style="top:378px; font-size:60px">Kelantan &amp; Terengganu</div>
    <div class="t" id="s12-l3" style="top:478px; font-size:46px; letter-spacing:.24em; font-weight:800">Mahligai Idaman</div>
    <div id="s12-b"><span>Hubungi kami</span></div>
    <div id="s12-fade"></div>""", f"""
    tl.fromTo("#s12-v", {{ scale: 1.0 }}, {{ scale: 1.14, duration: 5.3, ease: "sine.inOut" }}, 0);
{rise("#s12-l1", 0.15)}{rise("#s12-l2", max(0.8, t_kel - 0.1), 0.5, 30)}{rise("#s12-l3", max(1.4, t_hub - 0.1), 0.5, 24)}
    tl.fromTo("#s12-b", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {max(1.6, t_hub + 0.2)});
    tl.fromTo("#s12-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, ease: "sine.in" }}, 4.85);
""")

# ---------------------------------------------------------------- S13 OUTRO (company card)
scene("s13", f"""
    #s13-img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 55%; }}
    #s13-img img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }}
    #root .ring {{ position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; border: 5px solid {YEL}; opacity: 0; }}
    #s13-shine {{ position: absolute; left: 30px; top: 1180px; width: 1020px; height: 420px; overflow: hidden; }}
    #s13-band {{ position: absolute; left: 0; top: 0; width: 220px; height: 420px; background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.38) 50%, rgba(255,255,255,0)); }}
    #s13-glow {{ position: absolute; left: 86px; top: 1440px; width: 908px; height: 132px; border-radius: 30px; border: 4px solid {YEL}; box-shadow: 0 0 40px rgba(246,195,67,.75); opacity: 0; }}
    #s13-fade {{ position: absolute; inset: 0; background: #000; }}
""", """    <div id="s13-img"><img src="assets/outro.jpg" alt="" /></div>
    <div class="ring" id="s13-r1" style="left:477px; top:888px"></div>
    <div class="ring" id="s13-r2" style="left:744px; top:1002px"></div>
    <div id="s13-shine"><div id="s13-band"></div></div>
    <div id="s13-glow"></div>
    <div id="s13-fade"></div>""", """
    tl.fromTo("#s13-fade", { opacity: 1 }, { opacity: 0, duration: 0.5, ease: "power2.out" }, 0);
    tl.fromTo("#s13-img", { scale: 1.14 }, { scale: 1.0, duration: 1.1, ease: "expo.out" }, 0);
    tl.to("#s13-img", { scale: 1.03, duration: 3.9, ease: "sine.inOut" }, 1.1);
    ["#s13-r1", "#s13-r2"].forEach((r, i) => {
      tl.fromTo(r, { opacity: 0.95, scale: 0.3 }, { opacity: 0, scale: 2.1, duration: 1.0, ease: "power2.out", repeat: 2 }, 0.7 + i * 0.25);
    });
    tl.fromTo("#s13-band", { x: -240 }, { x: 1060, duration: 1.1, ease: "sine.inOut" }, 1.0);
    tl.fromTo("#s13-glow", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }, 1.6);
""", shade=False)

# ---------------------------------------------------------------- CAPTIONS: exact script, aligned to the voice
SCRIPT = """Ramai yang jatuh hati dengan rumah split level, tapi bila nak bina sendiri, tak tahu nak cari design dekat mana!
Haa, cuba tengok rumah yang Mahligai Idaman bina dekat Kemaman, Terengganu ni!
Dari luar pun dah nampak gah kan?
Yang menariknya, konsep split level ni menggunakan aras lantai yang berbeza, menjadikan susun atur rumah lebih unik dan ada karakter tersendiri!
Tapi korang tahu tak, split level ni bukan terhad kepada satu style je tau!
Dekat Mahligai Idaman, kami ada pelbagai koleksi design split level.
Nak Modern Tropical yang elegan?
Muji Style yang simple dan tenang?
Atau English Style yang klasik?
Nordic Style yang cozy, malah Malay Traditional Style pun ada!
Paling best, Mahligai Idaman ada pelukis pelan sendiri yang boleh bantu korang olah design mengikut cita rasa, gaya hidup dan kesesuaian tanah masing-masing.
Jadi, tak perlu pening nak cari design dekat mana lagi!
Nak bina rumah split level di Kelantan & Terengganu? Hubungi Mahligai Idaman!"""
PHRASES = ["split level", "Mahligai Idaman", "Kemaman", "Terengganu", "Modern Tropical", "Muji Style", "English Style", "Nordic Style",
           "Malay Traditional Style", "pelukis pelan", "Kelantan & Terengganu"]
SPEAK = {"&": "dan"}
norm = lambda s: re.sub(r"[^a-z0-9]", "", SPEAK.get(s, s).lower())
sw = SCRIPT.split()
hi = [False] * len(sw)
for ph in PHRASES:
    p = [norm(x) for x in ph.split()]
    for i in range(len(sw) - len(p) + 1):
        if [norm(x) for x in sw[i:i + len(p)]] == p:
            for k in range(len(p)):
                hi[i + k] = True
a, b = [norm(x) for x in sw], [norm(x["text"]) for x in WW]
times = [None] * len(sw)
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if op == "equal":
        for k in range(i2 - i1):
            times[i1 + k] = (WW[j1 + k]["start"], WW[j1 + k]["end"])
    elif op == "replace":
        s0, e0 = WW[j1]["start"], WW[j2 - 1]["end"]
        n = i2 - i1
        for k in range(n):
            times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
for i in range(len(times)):
    if times[i] is None:
        p = times[i - 1][1] if i else 0
        times[i] = (p, p + 0.2)
# phrase chunks: break after punctuation; long runs split at about 5 words
# phrase id per word, so a name like "Mahligai Idaman" is never split across captions or lines
inph = [False] * len(sw)
for ph in PHRASES:
    p = [norm(x) for x in ph.split()]
    for i in range(len(sw) - len(p) + 1):
        if [norm(x) for x in sw[i:i + len(p)]] == p:
            for k in range(len(p) - 1):
                inph[i + k] = True   # word i+k continues into the next word of a phrase
chunks, cur = [], []
for i, w in enumerate(sw):
    cur.append(i)
    near_end = any(x[-1] in ".,!?" for x in sw[i + 1:i + 4])
    if w[-1] in ".,!?" or (len(cur) >= 7 and not inph[i] and not near_end):
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
# fold one- or two-word leftovers into a neighbour: into the caption before when that one was cut
# mid-sentence (so the sentence ends together), otherwise into the caption after (lead-ins like "Haa,")
out_, i = [], 0
while i < len(chunks):
    ch = chunks[i]
    prev_cut = bool(out_) and (sw[out_[-1][-1]][-1] not in ".,!?" or sw[ch[-1]][-1] in ".!?")
    if len(ch) <= 2 and prev_cut and len(out_[-1]) + len(ch) <= 10:
        out_[-1] = out_[-1] + ch
    elif len(ch) <= 2 and sw[ch[-1]][-1] not in ".!?" and i + 1 < len(chunks) and len(ch) + len(chunks[i + 1]) <= 9:
        chunks[i + 1] = ch + chunks[i + 1]
    else:
        out_.append(ch)
    i += 1
chunks = out_
caps = []
for n, ch in enumerate(chunks):
    st = max(0.0, times[ch[0]][0] - 0.06)
    en = times[ch[-1]][1] + 0.25
    if n + 1 < len(chunks):
        nxt = times[chunks[n + 1][0]][0] - 0.06
        en = nxt if nxt - times[ch[-1]][1] < 0.7 else en
    toks = [f'<span class="y">{html.escape(sw[i])}</span>' if hi[i] else html.escape(sw[i]) for i in ch]
    if len(ch) >= 5:   # two lines, broken near the middle but never inside a phrase
        cut = len(ch) // 2
        while cut < len(ch) - 1 and inph[ch[cut - 1]]:
            cut += 1
        words = " ".join(toks[:cut]) + "<br />" + " ".join(toks[cut:])
    else:
        words = " ".join(toks)
    caps.append((round(st, 2), round(max(0.3, en - st), 2), words))
assert " ".join(sw) == SCRIPT.replace("\n", " ")  # every word of the script is shown, unchanged
cap_html = "\n".join(f'    <div class="cap clip" id="cap-{i:02d}" data-start="{s}" data-duration="{d}"><span class="pill">{t}</span></div>' for i, (s, d, t) in enumerate(caps, 1))
cap_js = "\n".join(f'    tl.fromTo("#cap-{i:02d} .pill", {{ opacity: 0, scale: 0.86, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "back.out(2)" }}, {s});' for i, (s, d, t) in enumerate(caps, 1))
with open(f"{OUT}/compositions/captions.html", "w") as f:
    f.write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: Montserrat, sans-serif; }}
    #root .cap {{ position: absolute; left: 50px; right: 50px; top: 1226px; text-align: center; }}
    #root .pill {{ display: inline-block; padding: 12px 26px 14px; background: rgba(12,14,18,.9); color: #fff; border-radius: 14px;
      font-weight: 800; font-size: 43px; line-height: 1.22; box-shadow: 0 10px 30px rgba(0,0,0,.35); }}
    #root .pill .y {{ color: {YEL}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{cap_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{cap_js}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ---------------------------------------------------------------- INDEX + SOUND
hosts = "\n".join(f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for c, s, d in SCENES)
def _ease(u):  # GSAP power2.inOut
    return 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2


GAL_SFX = []
for gi in range(len(GAL)):
    target = 190 - gi * 740           # row x at which card gi is centred on screen
    frac = (1000 - target) / (1000 + 2770)
    lo, hi_ = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi_) / 2
        lo, hi_ = (mid, hi_) if _ease(mid) < frac else (lo, mid)
    GAL_SFX.append((f"sx-slide-{gi}", ("whoosh-short", "whoosh")[gi % 2], round(START["s05"] + lo * 4.85 - 0.12, 2), 0.24))
SFX = [("sx-hook", "impact-bass-1", 0.0, 0.5)]
SFX += [(f"sx-hook-{i}", ("whoosh-short", "whoosh")[i % 2], round(t - 0.05, 2), 0.3) for i, (k, t) in enumerate(HOOK[1:])]
SFX += [("sx-kem", "whoosh", START["s02"] - 0.03, 0.3), ("sx-kem-pin", "pop", START["s02"] + t_kem - 0.1, 0.3), ("sx-wide", "whoosh-short", START["s02"] + 5.27, 0.3),
        ("sx-lv1", "click-soft", START["s03"] + 2.2, 0.3), ("sx-lv2", "click-soft", START["s03"] + 3.4, 0.3), ("sx-up", "pop", START["s03"] + 4.3, 0.25),
        ("sx-rise", "riser", START["s04"] + 1.72 - 1.97, 0.22, 1.5, 2.0), ("sx-drop", "impact-bass-2", START["s04"] + 1.72, 0.45),
        ("sx-gal", "whoosh", START["s05"] - 0.02, 0.3),
    ] + GAL_SFX + [
        ("sx-st1", "whoosh-short", START["s06"] - 0.03, 0.3), ("sx-st2", "whoosh", START["s07"] - 0.03, 0.3), ("sx-st3", "whoosh-short", START["s08"] - 0.03, 0.3),
        ("sx-st4", "whoosh", START["s09"] - 0.03, 0.3), ("sx-st5", "whoosh-short", START["s09"] + t_malay - 0.03, 0.3),
        ("sx-pen", "sparkle", START["s10"] + 0.1, 0.18), ("sx-plan", "whoosh-short", START["s10"] + 2.97, 0.25), ("sx-3d", "whoosh", START["s10"] + 5.57, 0.25),
        ("sx-house", "whoosh-short", START["s10"] + 7.97, 0.25), ("sx-k1", "click-soft", START["s10"] + k1, 0.3), ("sx-k2", "click-soft", START["s10"] + k2, 0.3),
        ("sx-k3", "click-soft", START["s10"] + k3, 0.3), ("sx-cards", "whoosh", START["s11"] + 0.02, 0.3), ("sx-gather", "pop", START["s11"] + 2.6, 0.3),
        ("sx-cta", "impact-bass-1", START["s12"] + 0.0, 0.45), ("sx-btn", "pop", START["s12"] + max(1.6, t_hub + 0.2), 0.3),
        ("sx-outro", "whoosh", START["s13"] - 0.02, 0.4), ("sx-outro-hit", "impact-bass-1", START["s13"] + 0.05, 0.5), ("sx-outro-sp", "sparkle", START["s13"] + 1.0, 0.28)]
DUR = {"click-soft": 0.36, "click": 0.36, "impact-bass-1": 2.1, "impact-bass-2": 2.55, "key-press": 0.43, "pop": 0.72, "riser": 10.0,
       "sparkle": 1.8, "whoosh-cinematic": 5.5, "whoosh-short": 0.57, "whoosh": 0.57}
audio = []
for n, e in enumerate(SFX):
    i, f_, s, v = e[:4]
    ms = f' data-media-start="{e[4]}"' if len(e) > 4 else ""
    d = e[5] if len(e) > 5 else DUR[f_]
    audio.append(f'      <audio id="{i}" class="clip" src="assets/sfx/{f_}.mp3" data-start="{round(max(0, s), 2)}" data-duration="{d}"{ms} data-track-index="{4 + n % 5}" data-volume="{v}"></audio>')
with open(f"{OUT}/index.html", "w") as f:
    f.write(f"""<!doctype html>
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
{hosts}
      <img id="logo" class="clip" src="assets/logo.png" alt="" data-start="0" data-duration="{TOTAL}" data-track-index="9" style="position:absolute; left:455px; top:52px; width:170px; height:117px; z-index:20" />
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:10"></div>
      <audio id="vo" class="clip" src="assets/audio/vo.mp3" data-start="0" data-duration="{round(WW[-1]['end'] + 0.3, 2)}" data-track-index="3" data-volume="1"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok", TOTAL, "s,", len(caps), "captions")
