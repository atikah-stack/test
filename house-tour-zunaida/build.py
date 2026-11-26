"""Builds the cleaned-up house tour (Pn Zunaida's house, Kok Lanas) from house.mov.

Source: assets/src/house.mov (5:40, 1080x1920, 30 fps; already has burned-in captions, which the
caption card covers). Not in git (480 MB): download it from the client's Google Drive folder.
Voice: assets/audio/voice-clean.wav — the same audio, de-noised and levelled to about -14 LUFS.

The edit only removes things: repeated words, false starts, a memory slip, and long pauses.
Nothing is sped up or re-voiced. Every cut point is snapped to the quietest moment nearby.
Run `python3 build.py`; it also writes EDL.md (what was cut and kept, with source times).
"""
import json, wave
import numpy as np

SRC = "assets/src/house.mov"
VOICE = "assets/audio/voice-clean.wav"
DUR = 339.96
W, Y = "#FFFFFF", "#FFD43B"

# ---------------------------------------------------------------- content cuts (source seconds)
CUTS = [
    (29.05, 30.95, "pause and “Okay.” before the surau"),
    (59.55, 60.02, "“our…” (false start before “Our living room”)"),
    (39.42, 40.16, "“boleh. Bolehlah.” (repeat) — set by the loudness trace, not snapped", False),
    (49.02, 51.00, "“Macam nak buat apa?” (filler question)"),
    (79.35, 82.00, "“yang paling, orang kata apa?” (false start)"),
    (118.02, 120.00, "“Kita pergi ke dining room.” (repeat of “ruang makan”)"),
    (225.00, 226.04, "“Dryer dengan” (false start)"),
    (257.02, 258.00, "second “Belum siap lagi.”"),
    (262.02, 264.00, "“Tapi ini masih…” (unfinished)"),
    (266.00, 267.00, "“Masih tak siap lagi.” (repeat)"),
    (296.00, 306.00, "“Tengok, dah lupa. Dah lupa dah. Apa nak cakap?” (memory slip)"),
]
PAUSE_KEEP = 0.35   # every pause longer than this is shortened to this length
SNAP = 0.18         # search window for the quietest point around each cut

# B-roll of the same house (from the client's earlier footage), placed over cuts: (source time of cut, file, media start, duration)
BROLL = [
    (32.00, "IMG_3540.MOV", 0.0, 1.0, "surau"),
    (82.00, "IMG_3615.MOV", 0.3, 1.8, "ruang tamu"),
    (113.0, "IMG_3534.MOV", 0.6, 1.8, "ruang keluarga"),
    (306.0, "IMG_3623.mov", 0.2, 1.4, "bilik / almari"),
    (329.6, "copy_F371EC91-96A0-45F7-9EF7-DBEC5C39D4B7.mov", 0.0, 2.6, "banglo dari drone"),
]

# Room labels (source time, text) and info cards (source time, duration, lines)
LABELS = [(32.1, "SURAU"), (59.0, "RUANG TAMU"), (85.2, "RUANG KELUARGA"), (120.2, "RUANG MAKAN"),
          (162.1, "COFFEE BAR & ISLAND"), (199.5, "DAPUR & LAUNDRY"), (271.0, "BILIK UTAMA")]
CARDS = [
    (206.0, 4.0, [("KABINET", "w", 44), ("CUSTOM-MADE", "y", 64)]),
    (306.3, 5.0, [("6 BILIK TIDUR", "y", 66), ("6 BILIK AIR", "w", 54), ("3,774 KPS", "w", 40)]),
]

# Spelling fixes for subtitles (lowercase match -> replacement); loghat kept
FIX = {"malikai": "Mahligai", "daman.": "Idaman.", "daman": "Idaman", "malika": "Mahligai", "idamal.": "Idaman.",
       "idamal": "Idaman", "haus": "house", "tuah": "tour", "tahliah": "Tahlil", "tahlih": "Tahlil", "kopi": "coffee",
       "berabarak": "berborak", "berak-berak": "berborak", "bora": "borak", "sport": "spot", "komplek": "komplet",
       "separatkan": "separate-kan", "separatekan": "separate-kan", "semayang": "sembahyang", "jemua": "jamu",
       "jemur": "jamu", "seri": "Sri", "dekor": "Dekor", "deko": "Dekor", "cabinet": "kabinet", "cabinet.": "kabinet.",
       "malika": "Mahligai"}
DROP = {"help."}                       # stutter tokens not shown in captions
PHRASE = {"Ada laman dia": "Dalaman dia", "ada laman dia": "dalaman dia", "Our living room": "our living room",
          "estetik menyebab.": "aesthetic punya vibe.", "Kita masuk bar,": "Termasuk bar,", "kita masuk bar,": "termasuk bar,"}
PROPER = {"Zunaida", "Mahligai", "Idaman", "Sri", "Dekor", "TV", "Assalamu'alaikum", "Alhamdulillah", "So", "Okey", "Jom"}
KEY = {"surau", "6", "enam", "custom-made", "island", "island.", "island,", "mahligai", "idaman", "idaman.", "coffee",
       "bar", "dining", "luxury", "family", "kabinet"}

# ---------------------------------------------------------------- audio envelope + snapping
with wave.open(VOICE) as wf:
    sr = wf.getframerate()
    a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32)
hop = sr // 100
env = np.sqrt(np.convolve(a[: len(a) // hop * hop].reshape(-1, hop).astype(np.float64) ** 2 @ np.ones(hop) / hop,
                          np.ones(5) / 5, mode="same"))


def snap(t):
    i0, i1 = int((t - SNAP) * 100), int((t + SNAP) * 100)
    i0, i1 = max(i0, 0), min(i1, len(env) - 1)
    return (i0 + int(np.argmin(env[i0:i1]))) / 100


removed = []
for c in CUTS:
    s, e, why = c[:3]
    exact = len(c) > 3 and c[3] is False
    removed.append((s, e, why) if exact else (snap(s), snap(e), why))
for line in open("assets/audio/pauses.txt"):
    span = line.split()[0]
    s, e = map(float, span.split("-"))
    if e - s > PAUSE_KEEP + 0.1:
        removed.append((s + PAUSE_KEEP / 2, e - PAUSE_KEEP / 2, f"pause {e - s:.1f}s → {PAUSE_KEEP}s"))
removed.sort()
merged = []
for s, e, why in removed:
    if merged and s <= merged[-1][1] + 0.05:
        ps, pe, pw = merged[-1]
        merged[-1] = (ps, max(pe, e), pw + " + " + why)
    else:
        merged.append((s, e, why))

keep, t = [], 0.0
for s, e, _ in merged:
    if s - t > 0.05:
        keep.append((round(t, 2), round(s, 2)))
    t = e
keep.append((round(t, 2), DUR))

segs, out = [], 0.0
for s, e in keep:
    segs.append((s, e, round(out, 3)))
    out += e - s
TOTAL = round(out, 2)


def to_out(t):
    for s, e, o in segs:
        if s <= t < e:
            return round(o + t - s, 3)
    for s, e, o in segs:          # time fell inside a cut: use the next kept moment
        if t < s:
            return o
    return TOTAL


# ---------------------------------------------------------------- edited voice (for checking and for captions)
FADE = int(0.03 * sr)
parts = []
for s_, e_, o_ in segs:
    chunk = a[int(s_ * sr):int(e_ * sr)].copy()
    if len(chunk) > 2 * FADE:
        ramp = np.linspace(0, 1, FADE, dtype=np.float32)
        chunk[:FADE] *= ramp; chunk[-FADE:] *= ramp[::-1]
    parts.append(chunk)
edit = np.concatenate(parts).clip(-32768, 32767).astype(np.int16)
with wave.open("assets/audio/edit-voice.wav", "wb") as wo:
    wo.setnchannels(1); wo.setsampwidth(2); wo.setframerate(sr); wo.writeframes(edit.tobytes())

# ---------------------------------------------------------------- root
rows = []
for i, (s, e, o) in enumerate(segs):
    d = round(e - s, 3)
    z = 1.0 if i % 2 == 0 else 1.06   # alternate framing so jump cuts read as deliberate
    # zoom about the burned-in caption line (y ~1505) so it never moves out from under the new caption card
    rows.append(f'      <video id="p{i:03d}" class="shot clip" src="{SRC}" muted playsinline data-start="{o}" data-duration="{d}" '
                f'data-media-start="{s}" data-track-index="{i % 2}" style="z-index:{1 + i % 2};transform-origin:50% 78.4%;transform:scale({z})"></video>')
    rows.append(f'      <audio id="a{i:03d}" class="clip" src="{VOICE}" data-start="{o}" data-duration="{d}" data-media-start="{s}" '
                f'data-volume="1" data-fade-in="0.03" data-fade-out="0.03" data-track-index="{10 + i % 2}"></audio>')
for k, (st, f, ms, d, note) in enumerate(BROLL):
    o = max(0.0, round(to_out(st) - d / 2, 2))
    rows.append(f'      <!-- B-roll: {note} -->\n      <video id="b{k}" class="shot clip" src="assets/broll/{f}" muted playsinline '
                f'data-start="{o}" data-duration="{d}" data-media-start="{ms}" data-track-index="3" style="z-index:20"></video>')

scenes = []
for k, (st, text) in enumerate(LABELS):
    scenes.append((f"lbl{k}", to_out(st), 2.6, "label", text))
for k, (st, d, lines) in enumerate(CARDS):
    scenes.append((f"card{k}", to_out(st), d, "card", lines))
for n, (cid, s, d, kind, _) in enumerate(scenes):
    rows.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" '
                f'data-duration="{d}" data-track-index="{5 + n % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" '
                f'style="z-index:{40 + n}"></div>')
rows.append(f'      <div id="subs" data-composition-id="subs" data-composition-src="compositions/subs.html" data-start="0" '
            f'data-duration="{TOTAL}" data-track-index="8" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:80"></div>')

open("index.html", "w").write(f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0b; }}
      #root {{ width: 100%; height: 100%; background: #0b0b0b; font-family: "Montserrat", sans-serif; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="30" data-width="1080" data-height="1920">
{chr(10).join(rows)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")

# ---------------------------------------------------------------- graphics
SHADOW = "0 6px 22px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.5)"


def write_scene(cid, d, css, body, js):
    open(f"compositions/{cid}.html", "w").write(f"""<template>
  <style>
    #root {{ position:absolute; inset:0; font-family:"Montserrat",sans-serif; }}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")


for cid, s, d, kind, payload in scenes:
    if kind == "label":
        write_scene(cid, d, f"""
    #{cid}-w {{ position:absolute; left:60px; right:162px; top:330px; display:flex; justify-content:center; }}
    #{cid}-p {{ display:flex; align-items:center; gap:16px; padding:14px 28px 14px 22px; border-radius:40px; background:rgba(12,12,12,.62); }}
    #{cid}-bar {{ width:8px; height:34px; border-radius:4px; background:{Y}; }}
    #{cid}-t {{ color:#FFFFFF; font-weight:800; font-size:36px; letter-spacing:0.06em; white-space:nowrap; }}""",
                    f'    <div id="{cid}-w" class="clip" data-start="0" data-duration="{d}" data-track-index="0"><div id="{cid}-p">'
                    f'<div id="{cid}-bar"></div><div id="{cid}-t">{payload}</div></div></div>',
                    f'    tl.fromTo("#{cid}-p", {{ opacity:0, y:-14 }}, {{ opacity:1, y:0, duration:0.45, ease:"power2.out" }}, 0);\n'
                    f'    tl.to("#{cid}-p", {{ opacity:0, duration:0.35, ease:"sine.in" }}, {d - 0.4});')
    else:
        lines = "\n".join(f'      <div id="{cid}-{k}" class="cl" style="color:{W if c == "w" else Y};font-size:{sz}px">{tx}</div>'
                          for k, (tx, c, sz) in enumerate(payload))
        js = "\n".join(f'    tl.fromTo("#{cid}-{k}", {{ opacity:0, y:22, scale:0.96 }}, {{ opacity:1, y:0, scale:1, duration:0.55, ease:"power2.out" }}, {0.12 * k});'
                       for k in range(len(payload)))
        write_scene(cid, d, f"""
    #{cid}-c {{ position:absolute; left:60px; right:162px; top:470px; display:flex; flex-direction:column; align-items:center; gap:4px;
      padding:34px 30px; border-radius:30px; background:rgba(12,12,12,.6); }}
    .cl {{ font-weight:800; text-transform:uppercase; white-space:nowrap; line-height:1.08; text-shadow:{SHADOW}; }}""",
                    f'    <div id="{cid}-c" class="clip" data-start="0" data-duration="{d}" data-track-index="0">\n{lines}\n    </div>',
                    js + f'\n    tl.to("#{cid}-c", {{ opacity:0, duration:0.35, ease:"sine.in" }}, {d - 0.4});')

# ---------------------------------------------------------------- subtitles (cover the burned-in captions at y 1478-1528)
# Two transcripts: large-v3 is more accurate, but repeats sentences after 5:18 (a known Whisper glitch),
# so it is used up to 4:22 and for the bedroom-count line; the medium model covers the rest.
def load(p):
    w = json.load(open(p)); return w["words"] if isinstance(w, dict) else w
use_large = lambda t: t < 262.0 or 300.0 <= t < 312.0
words = [w for w in load("assets/audio/transcript-large-v3.json") if use_large(w["start"])] + \
        [w for w in load("assets/audio/transcript-medium.json") if not use_large(w["start"])]
words.sort(key=lambda w: w["start"])
import os
EDIT_TR = "assets/audio/transcript-edit.json"
if os.path.exists(EDIT_TR):          # transcript of the edited audio: what is actually heard, on the edit timeline
    words = load(EDIT_TR)
words = [w for w in words if w["text"].strip().lower() not in DROP]
kept = []
if os.path.exists(EDIT_TR):
    kept = [(round(w["start"], 3), round(w["end"], 3), w["text"].strip()) for w in words]
else:
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        if any(s <= mid < e for s, e, _ in segs):
            kept.append((to_out(w["start"]), to_out(w["end"]), w["text"].strip()))


def fix(word):
    low = word.lower()
    return FIX.get(low, word)


groups, cur = [], []
for st, en, tx in kept:
    if cur and (st - cur[-1][1] > 0.6 or sum(len(x[2]) + 1 for x in cur) + len(tx) > 34 or cur[-1][2][-1:] in ".?!"):
        groups.append(cur); cur = []
    cur.append((st, en, tx))
if cur:
    groups.append(cur)

sub_rows, sub_js, spans = [], [], []
for k, g in enumerate(groups):
    s, e = g[0][0], g[-1][1]
    nxt = groups[k + 1][0][0] if k + 1 < len(groups) else TOTAL
    e = nxt if nxt - e < 1.2 else e + 0.25          # keep the card up through short gaps
    toks = []
    for j, (_, _, t) in enumerate(g):
        t = fix(t)
        prev = toks[-1] if toks else (groups[k - 1][-1][2] if k else ".")
        # a cut can leave a capital mid-sentence; lower it unless it is a name
        if t[:1].isupper() and prev[-1:] not in ".?!" and t.strip(",.?!") not in PROPER:
            t = t[:1].lower() + t[1:]
        toks.append(t)
    plain = " ".join(toks)
    for a_, b_ in PHRASE.items():
        plain = plain.replace(a_, b_)
    toks = plain.split(" ")
    txt = " ".join(f'<span class="k">{t}</span>' if t.lower().strip(",.?!") in KEY else t for t in toks)
    sub_rows.append(f'    <div id="sb{k:03d}" class="cap clip" data-start="{round(s, 2)}" data-duration="{round(max(0.3, e - s), 2)}" '
                    f'data-track-index="0"><div class="card"><span class="tx">{txt}</span></div></div>')
write_scene("subs", TOTAL, f"""
    .cap {{ position:absolute; left:40px; right:40px; top:1408px; height:156px; display:flex; align-items:flex-end; justify-content:center; }}
    /* solid card, fixed size: fully hides the old burned-in captions (one or two lines, y 1420-1550) */
    .card {{ height:156px; width:1000px; display:flex; align-items:center; justify-content:center; text-align:center;
      padding:12px 34px; border-radius:22px; background:#141414;
      color:#FFFFFF; font-weight:700; font-size:42px; line-height:1.2; }}
    .k {{ color:{Y}; }}""", "\n".join(sub_rows), "")

# ---------------------------------------------------------------- EDL
with open("EDL.md", "w") as f:
    f.write(f"# EDL — House tour Pn Zunaida\n\nSource 5:39.96 → edit {int(TOTAL // 60)}:{TOTAL % 60:05.2f} "
            f"({DUR - TOTAL:.1f} s removed, nothing sped up).\n\n## Removed (source time)\n\n| From | To | Length | What |\n|---|---|---|---|\n")
    for s, e, why in merged:
        f.write(f"| {s:.2f} | {e:.2f} | {e - s:.2f} s | {why} |\n")
    f.write("\n## Kept segments (source → edit)\n\n| Source in | Source out | Edit start |\n|---|---|---|\n")
    for s, e, o in segs:
        f.write(f"| {s:.2f} | {e:.2f} | {o:.2f} |\n")
print("segments", len(segs), "total", TOTAL, "removed", round(DUR - TOTAL, 1), "subtitle groups", len(groups))
