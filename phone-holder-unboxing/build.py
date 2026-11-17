#!/usr/bin/env python3
"""Triple Suction Magnetic Phone Holder — minimalist unboxing (TikTok affiliate), 1080x1920 30fps.

Sources (Google Drive originals, iPhone HLG HDR, put in assets/src/):
  IMG_7770.MOV 1l4jvrD5mBTzpLN9NwH8BGrF7pgK6HPLF  box front/back
  IMG_7771.MOV 1VY1j4x7pRDfljNFgDSjbRsO3G3GU1MVz  full unboxing (open box, plastic, suction, ring, on phone)
  IMG_7772.MOV 1rYq-kalEvMCHNP7TmdDkjBHmX-akNjQx  phone stuck on car window
  IMG_7773.MOV 1jhdTZMXW4sSOz5cn-dU-q7ZbDG9V1tTq  phone + holder outdoors
  IMG_7775.MOV 1bjircdSB7RIf3wdeznne0Jtxk2m4NNo5  phone on car window (wide)
Two edits, no voice-over: music bed + light SFX + minimalist headings.
  python3 make-music.py && python3 build.py a    ->  renders/phone-holder-unboxing.mp4    (version A)
  python3 make-music.py b && python3 build.py b  ->  renders/phone-holder-unboxing-b.mp4  (version B)
  python3 make-music.py c && python3 build.py c  ->  renders/phone-holder-kelebihan-c.mp4 (version C: benefits only)
(VO support kept: assets/audio/vo1..vo5.* are mixed in at each scene start if present.)
"""
import os, subprocess, glob, sys

W, H, FPS = 1080, 1920, 30
SRC = "assets/src/IMG_{}.MOV"
TM = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
# neutral, slightly warm, a touch less saturated; gentle lift for a soft look
GRADE = ("eq=contrast=1.04:brightness=0.015:saturation=0.93:gamma=1.03,"
         "colorbalance=rs=0.015:bs=-0.02:rm=0.02:bm=-0.025:rh=0.01:bh=-0.015,"
         "unsharp=5:5:0.45:5:5:0")

VAR = (sys.argv[1] if len(sys.argv) > 1 else "a").lower()

# scene, file, src_in, dur, zoom_from, zoom_to, anchor_y (0=top..1=bottom)
if VAR == "a":  # Version A: hook on the window tap, scene-by-scene unboxing story, 84 BPM bed
    MUSIC, OUT = "assets/audio/music.wav", "renders/phone-holder-unboxing.mp4"
    SEGS = [
        ("hook", 7775, 6.60, 1.20, 1.14, 1.24, 0.5),  # tap on the phone stuck to the window -> screen lights, it stays put
        ("hook", 7771, 47.40, 1.60, 1.08, 1.16, 0.5),  # cut to the holder: suction cups tilted
        ("hook", 7773, 12.00, 1.60, 1.00, 1.06, 0.5),  # holder on the phone back, daylight
        ("unbox", 7770, 1.90, 1.30, 1.00, 1.04, 0.3),  # box front
        ("unbox", 7771, 18.60, 2.20, 1.00, 1.04, 0.3), # opening the box
        ("unbox", 7771, 24.80, 2.50, 1.00, 1.07, 0.5), # pulling it out, teal ring through plastic
        ("reveal", 7771, 41.70, 2.00, 1.00, 1.05, 0.0),# out of the plastic
        ("reveal", 7771, 46.60, 2.60, 1.00, 1.08, 0.0),# full suction face, subtle zoom
        ("reveal", 7771, 50.00, 1.40, 1.04, 1.08, 0.0),
        ("detail", 7771, 52.40, 1.80, 1.02, 1.07, 0.5),# magnetic plate
        ("detail", 7771, 54.60, 2.20, 1.00, 1.05, 0.5),# ring flips out
        ("detail", 7771, 77.00, 1.60, 1.00, 1.04, 0.5),# pressing suction to phone
        ("detail", 7771, 89.00, 1.90, 1.00, 1.05, 0.5),# suction pad on phone
        ("final", 7772, 9.00, 2.00, 1.00, 1.05, 0.5),  # phone holding on window
        ("final", 7775, 8.50, 1.20, 1.04, 1.08, 0.5),
        ("final", 7771, 92.40, 2.50, 1.00, 1.10, 0.5), # hero: tilted suction pad, slow zoom
    ]
    TEXTS = [  # text ("|" = new line), start, end, x-mode
        ("Didn't expect to love|this little thing", 1.25, 4.30, "c"),
        ("Unboxing Time", 4.60, 7.80, "c"),
        ("Minimal & Compact", 10.65, 16.00, "c"),
        ("Magnetic Mount", 16.65, 20.25, "r"),
        ("Triple Suction", 20.55, 23.65, "c"),
    ]
    FX = [("click-soft", 0.78, 0.30), ("whoosh-short", 1.12, 0.18), ("pop", 1.30, 0.10),
          ("whoosh-short", "unbox-0.08", 0.13), ("click-soft", "reveal+0.05", 0.22), ("pop", "detail+0.15", 0.09),
          ("click-soft", "detail+1.95", 0.20), ("pop", 20.55, 0.08), ("whoosh-short", "final-0.08", 0.12)]
elif VAR == "c":  # Version C: no unboxing — hook, then one benefit per beat of the edit, 88 BPM bed
    MUSIC, OUT = "assets/audio/music-c.wav", "renders/phone-holder-kelebihan-c.mp4"
    SEGS = [
        ("hook", 7772, 9.00, 1.20, 1.00, 1.05, 0.5),    # phone floating on the window
        ("hook", 7771, 47.40, 3.00, 1.04, 1.14, 0.5),   # suction cups tilted, slow push
        ("suction", 7771, 44.60, 1.60, 1.04, 1.09, 0.0),# suction face
        ("suction", 7773, 12.00, 1.60, 1.00, 1.05, 0.5),# pad on the phone, daylight
        ("suction", 7771, 86.40, 1.20, 1.00, 1.04, 0.5),# pressing the pad on
        ("magnet", 7771, 52.40, 1.80, 1.02, 1.06, 0.5), # magnetic plate
        ("magnet", 7771, 54.60, 2.60, 1.00, 1.06, 0.5), # ring flips out
        ("free", 7775, 6.60, 1.30, 1.14, 1.22, 0.5),    # tap the phone on the window, it stays
        ("free", 7775, 7.90, 1.80, 1.08, 1.14, 0.5),
        ("compact", 7771, 89.00, 2.00, 1.00, 1.05, 0.5),# small pad on the phone back
        ("compact", 7771, 92.40, 2.50, 1.00, 1.10, 0.5),
    ]
    def at(sc, off): return f"{sc}+{off}"
    TEXTS = [  # "^" starts a smaller sub-line
        ("Kecil, tapi banyak kelebihan", 1.30, 4.05, "c"),
        ("Triple Suction^Cengkaman kuat & stabil", "suction+0.15", "magnet-0.10", "c"),
        ("Magnetic Mount^Pasang & tanggal cepat", "magnet+0.15", "free-0.10", "r"),
        ("Hands-Free^Tak perlu pegang", "free+0.25", "compact-0.10", "l"),
        ("Portable & Compact^Kecil, senang dibawa", "compact+0.15", "END-0.15", "c"),
    ]
    FX = [("whoosh-short", 1.12, 0.16), ("pop", 1.30, 0.10), ("pop", "suction+0.15", 0.09),
          ("click-soft", "magnet+0.15", 0.20), ("click-soft", "magnet+2.15", 0.22), ("click-soft", "free+0.60", 0.28),
          ("pop", "compact+0.15", 0.09),
          ("whoosh-short", "magnet-0.08", 0.10), ("whoosh-short", "free-0.08", 0.10)]
else:  # Version B: question hook, every cut on the beat of a brighter 92 BPM bed, unbox -> details -> in use
    MUSIC, OUT = "assets/audio/music-b.wav", "renders/phone-holder-unboxing-b.mp4"
    B = 60 / 92
    def bt(n): return round(n * B, 3)
    SEGS = [
        ("hook", 7771, 47.40, bt(3), 1.04, 1.14, 0.5),  # suction cups tilted, slow push
        ("hook", 7771, 89.00, bt(3), 1.00, 1.06, 0.5),  # holder on the phone back
        ("unbox", 7771, 4.00, bt(2), 1.02, 1.06, 0.3),  # box front
        ("unbox", 7771, 18.60, bt(3), 1.00, 1.05, 0.3), # opening the box
        ("unbox", 7771, 25.60, bt(3), 1.02, 1.08, 0.5), # teal ring through the plastic
        ("unbox", 7771, 41.80, bt(3), 1.00, 1.05, 0.0), # out of the plastic
        ("detail", 7771, 44.60, bt(3), 1.04, 1.10, 0.0),# suction face
        ("detail", 7771, 52.40, bt(2), 1.02, 1.06, 0.5),# magnetic plate
        ("detail", 7771, 54.60, bt(4), 1.00, 1.06, 0.5),# ring flips out
        ("use", 7771, 77.00, bt(2), 1.00, 1.04, 0.5),   # pressing it onto the phone
        ("use", 7771, 86.40, bt(2), 1.00, 1.05, 0.5),
        ("use", 7775, 6.60, bt(2), 1.14, 1.22, 0.5),    # tap on the phone on the window
        ("use", 7772, 9.00, bt(3), 1.00, 1.06, 0.5),    # holding on the window
        ("end", 7775, 7.40, bt(3), 1.02, 1.08, 0.5),    # wide: phone on the window, calm ending
    ]
    TEXTS = [
        ("What is this|little thing?", 0.20, bt(6) - 0.10, "c"),
        ("Let's unbox", bt(6) + 0.15, bt(11) - 0.10, "c"),
        ("Triple Suction", bt(17) + 0.10, bt(20) - 0.05, "c"),
        ("Magnetic Ring", bt(20) + 0.10, bt(26) - 0.10, "r"),
        ("Hands-Free", bt(26) + 0.15, bt(30) - 0.10, "c"),
    ]
    FX = [("pop", 0.20, 0.10), ("whoosh-short", "unbox-0.08", 0.13), ("click-soft", bt(14), 0.20),
          ("whoosh-short", "detail-0.08", 0.12), ("pop", bt(17) + 0.10, 0.09), ("click-soft", bt(22) + 0.55, 0.22),
          ("whoosh-short", "use-0.08", 0.12), ("click-soft", bt(30) + 0.55, 0.28), ("whoosh-short", "end-0.08", 0.10)]
TAIL = 0.4  # hold last frame

FONT = "assets/fonts/Poppins-SemiBold.ttf"
FS, TY = 62, 0.40  # font size, text centre at 40% of height

def run(cmd):
    subprocess.run(cmd, check=True)

os.makedirs("build", exist_ok=True); os.makedirs("renders", exist_ok=True)
starts, t = {}, 0.0
scene_start = {}
for i, (sc, f, a, d, z0, z1, ay) in enumerate(SEGS):
    scene_start.setdefault(sc, round(t, 3)); t += d
TOTAL = round(t + TAIL, 3)
print("total", TOTAL, scene_start)

# 1) per-segment render: tone-map, grade, smooth zoom, original audio cleaned
parts = []
for i, (sc, f, a, d, z0, z1, ay) in enumerate(SEGS):
    out = f"build/seg_{f}_{a:.2f}_{d:.2f}_{z0}_{z1}_{ay}.mp4"; parts.append(out)
    if os.path.exists(out): continue
    z = f"({z0}+({z1}-{z0})*t/{d})"
    vf = (f"{TM},scale={W}:{H}:flags=lanczos,{GRADE},"
          f"scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame:flags=bicubic,"
          f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{ay},setsar=1,fps={FPS},format=yuv420p")
    af = "highpass=f=120,lowpass=f=9000,afftdn=nf=-30,afade=t=in:d=0.04,afade=t=out:st={:.3f}:d=0.06".format(d - 0.06)
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", SRC.format(f), "-vf", vf, "-af", af,
         "-ar", "48000", "-ac", "2", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", out])
    print("seg", i, sc, f, a, d)

with open(f"build/list-{VAR}.txt", "w") as fh:
    fh.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"build/list-{VAR}.txt", "-c", "copy", f"build/base-{VAR}.mp4"])

def when(v):  # number, or "scene+offset" / "scene-offset"
    if not isinstance(v, str): return v
    for sign in "+-":
        if sign in v:
            sc, off = v.split(sign); return scene_start[sc] + (float(off) if sign == "+" else -float(off))
    return scene_start[v]

# 2) text overlays (fade + tiny rise), subtle soft shadow
def alpha(s, e, f=0.35):
    return f"if(lt(t,{s}),0,if(lt(t,{s}+{f}),(t-{s})/{f},if(lt(t,{e}-{f}),1,if(lt(t,{e}),({e}-t)/{f},0))))"
draws = []
FONT_SUB, FS_SUB = "assets/fonts/Poppins-Medium.ttf", 42
LH, LH_SUB = int(FS * 1.3), int(FS_SUB * 1.45)
def tsec(v):  # number, "scene+off", or "END-off"
    if isinstance(v, str) and v.startswith("END"): return TOTAL - TAIL - float(v[4:])
    return when(v)
for txt, s, e, xm in TEXTS:
    s, e = round(tsec(s), 3), round(tsec(e), 3)
    head, *sub = txt.split("^")
    rows = [(l, FONT, FS, LH, "0xFFF8EE") for l in head.split("|")] + [(l, FONT_SUB, FS_SUB, LH_SUB, "0xF3ECE0") for l in sub]
    total_h = sum(r[3] for r in rows); top = H * TY - total_h / 2
    for line, font, fs, lh, col in rows:
        cy = int(top + lh / 2); top += lh
        tx = line.replace(":", "\\:").replace("'", "\u2019").replace(",", "\\,")
        x = {"c": "(w-text_w)/2", "r": "w-text_w-96", "l": "96"}[xm]
        y = f"{cy}-ascent*0.72+14*(1-min(1\\,max(0\\,(t-{s})/0.45)))"
        common = f"fontfile={font}:text='{tx}':fontsize={fs}:x={x}:y={y}:enable='between(t,{s},{e})'"
        draws.append(f"drawtext={common}:fontcolor=black@0.22:alpha='{alpha(s, e)}':shadowx=0:shadowy=0:borderw=6:bordercolor=black@0.10")
        draws.append(f"drawtext={common}:fontcolor={col}:alpha='{alpha(s, e)}':shadowcolor=black@0.40:shadowx=0:shadowy=3")
vchain = f"[0:v]tpad=stop_mode=clone:stop_duration={TAIL},{','.join(draws)},fade=t=out:st={TOTAL-0.35}:d=0.35:color=black[v]"

# 3) audio: original product sound low, music bed ducked under VO, VO lines, light SFX
ins = ["-i", f"build/base-{VAR}.mp4", "-i", MUSIC]
amix, k = [], 2
fx = [(f"assets/sfx/{n}.mp3", when(at), vol) for n, at, vol in FX]
for path, at, vol in fx:
    ins += ["-i", path]
    amix.append(f"[{k}:a]volume={vol},adelay={int(at*1000)}|{int(at*1000)}[s{k}]"); k += 1
vo = []
for n, sc in enumerate(["hook", "unbox", "reveal", "detail", "final"], 1):
    p = next(iter(sorted(glob.glob(f"assets/audio/vo{n}.*"))), None)
    if not p or sc not in scene_start: continue
    at = scene_start[sc] + (0.10 if n == 1 else 0.20)
    ins += ["-i", p]
    amix.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at*1000)}|{int(at*1000)}[s{k}]"); vo.append(f"[s{k}]"); k += 1
sfx_labels = [f"[s{i}]" for i in range(2, 2 + len(fx))]
graph = [vchain] + amix + [
    f"[0:a]volume=0.55,apad=pad_dur={TAIL}[orig]",
    f"[1:a]volume={0.20 if vo else 0.42},atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.6}:d=1.6[mus]"]
if vo:
    graph.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0,asplit=2[vo][vosc]")
    graph.append("[mus][vosc]sidechaincompress=threshold=0.04:ratio=4:attack=30:release=400[musd]")
    mixin = ["[orig]", "[musd]", "[vo]"] + sfx_labels
else:
    mixin = ["[orig]", "[mus]"] + sfx_labels
graph.append(f"{''.join(mixin)}amix=inputs={len(mixin)}:normalize=0,atrim=0:{TOTAL},"
             f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]")
out = OUT
run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
     "-t", str(TOTAL), "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-profile:v", "high",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
print("wrote", out, TOTAL, "s", "VO lines:", len(vo))
