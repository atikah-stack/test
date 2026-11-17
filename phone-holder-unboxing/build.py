#!/usr/bin/env python3
"""Triple Suction Magnetic Phone Holder — minimalist unboxing (TikTok affiliate), 1080x1920 30fps.

Sources (Google Drive originals, iPhone HLG HDR, put in assets/src/):
  IMG_7770.MOV 1l4jvrD5mBTzpLN9NwH8BGrF7pgK6HPLF  box front/back
  IMG_7771.MOV 1VY1j4x7pRDfljNFgDSjbRsO3G3GU1MVz  full unboxing (open box, plastic, suction, ring, on phone)
  IMG_7772.MOV 1rYq-kalEvMCHNP7TmdDkjBHmX-akNjQx  phone stuck on car window
  IMG_7773.MOV 1jhdTZMXW4sSOz5cn-dU-q7ZbDG9V1tTq  phone + holder outdoors
  IMG_7775.MOV 1bjircdSB7RIf3wdeznne0Jtxk2m4NNo5  phone on car window (wide)
Optional VO: assets/audio/vo1..vo5.(wav|mp3), one per scene. Music: make-music.py -> assets/audio/music.wav.
Usage: python3 build.py  ->  renders/phone-holder-unboxing.mp4
"""
import os, subprocess, glob

W, H, FPS = 1080, 1920, 30
SRC = "assets/src/IMG_{}.MOV"
TM = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
# neutral, slightly warm, a touch less saturated; gentle lift for a soft look
GRADE = ("eq=contrast=1.04:brightness=0.015:saturation=0.93:gamma=1.03,"
         "colorbalance=rs=0.015:bs=-0.02:rm=0.02:bm=-0.025:rh=0.01:bh=-0.015,"
         "unsharp=5:5:0.45:5:5:0")

# scene, file, src_in, dur, zoom_from, zoom_to, anchor_y (0=top..1=bottom)
SEGS = [
    ("hook", 7771, 47.20, 1.00, 1.06, 1.12, 0.5),  # suction cups tilted — strongest product shot
    ("hook", 7773, 12.00, 1.00, 1.00, 1.05, 0.5),  # holder on the phone back, daylight
    ("hook", 7775, 7.55, 1.00, 1.04, 1.10, 0.5),   # phone on window
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
TAIL = 0.4  # hold last frame

TEXTS = [  # text, start, end, x-mode
    ("Kecil je, tapi menarik!", 0.15, 1.92, "c"),
    ("Unboxing Time", 3.20, 6.40, "c"),
    ("Minimal & Compact", 9.25, 14.60, "c"),
    ("Magnetic Mount", 15.25, 18.85, "r"),
    ("Triple Suction", 19.15, 22.25, "c"),
    ("Worth To Check Out!", 25.85, 28.50, "c"),
]
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

with open("build/list.txt", "w") as fh:
    fh.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build/list.txt", "-c", "copy", "build/base.mp4"])

# 2) text overlays (fade + tiny rise), subtle soft shadow
def alpha(s, e, f=0.35):
    return f"if(lt(t,{s}),0,if(lt(t,{s}+{f}),(t-{s})/{f},if(lt(t,{e}-{f}),1,if(lt(t,{e}),({e}-t)/{f},0))))"
draws = []
for txt, s, e, xm in TEXTS:
    tx = txt.replace(":", "\\:").replace("'", "’").replace(",", "\\,")
    x = {"c": "(w-text_w)/2", "r": "w-text_w-96", "l": "96"}[xm]
    y = f"{int(H*TY)}-text_h/2+14*(1-min(1\\,max(0\\,(t-{s})/0.45)))"
    common = f"fontfile={FONT}:text='{tx}':fontsize={FS}:x={x}:y={y}:enable='between(t,{s},{e})'"
    draws.append(f"drawtext={common}:fontcolor=black@0.22:alpha='{alpha(s, e)}':shadowx=0:shadowy=0:borderw=6:bordercolor=black@0.10")
    draws.append(f"drawtext={common}:fontcolor=0xFFF8EE:alpha='{alpha(s, e)}':shadowcolor=black@0.38:shadowx=0:shadowy=3")
vchain = f"[0:v]tpad=stop_mode=clone:stop_duration={TAIL},{','.join(draws)},fade=t=out:st={TOTAL-0.35}:d=0.35:color=black[v]"

# 3) audio: original product sound low, music bed ducked under VO, VO lines, light SFX
ins = ["-i", "build/base.mp4", "-i", "assets/audio/music.wav"]
amix, k = [], 2
fx = [("assets/sfx/whoosh-short.mp3", 0.00, 0.20), ("assets/sfx/pop.mp3", 0.20, 0.10),
      ("assets/sfx/whoosh-short.mp3", scene_start["unbox"] - 0.08, 0.13),
      ("assets/sfx/click-soft.mp3", scene_start["reveal"] + 0.05, 0.22),
      ("assets/sfx/pop.mp3", scene_start["detail"] + 0.15, 0.09),
      ("assets/sfx/click-soft.mp3", scene_start["detail"] + 1.95, 0.20),  # ring flip
      ("assets/sfx/pop.mp3", 19.15, 0.08),
      ("assets/sfx/whoosh-short.mp3", scene_start["final"] - 0.08, 0.12),
      ("assets/sfx/sparkle.mp3", 25.85, 0.07)]
for path, at, vol in fx:
    ins += ["-i", path]
    amix.append(f"[{k}:a]volume={vol},adelay={int(at*1000)}|{int(at*1000)}[s{k}]"); k += 1
vo = []
for n, sc in enumerate(["hook", "unbox", "reveal", "detail", "final"], 1):
    p = next(iter(sorted(glob.glob(f"assets/audio/vo{n}.*"))), None)
    if not p: continue
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
out = "renders/phone-holder-unboxing.mp4"
run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
     "-t", str(TOTAL), "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-profile:v", "high",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
print("wrote", out, TOTAL, "s", "VO lines:", len(vo))
