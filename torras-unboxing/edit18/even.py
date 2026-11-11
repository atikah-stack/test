# Even out all clips toward their shared natural average (full mean match, half std match), no stylised target.
import sys, subprocess, glob, os, numpy as np
src, dst = sys.argv[1], sys.argv[2]; stats = {}
def frames(f):
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
    ch = [[], [], []]
    for k in range(5):
        raw = subprocess.check_output(["ffmpeg","-nostdin","-loglevel","error","-ss",f"{dur*(0.1+0.2*k):.3f}","-i",f,"-frames:v","1","-vf","scale=270:480,format=yuv444p","-f","rawvideo","-"])
        a = np.frombuffer(raw, np.uint8).reshape(3, -1).astype(float)
        for c in range(3): ch[c].append(a[c])
    return [np.concatenate(c) for c in ch]
for f in sorted(glob.glob(src + "/*.mp4")):
    Y, U, V = frames(f); stats[f] = [(c.mean(), c.std()) for c in (Y, U, V)]
tm = [np.mean([s[i][0] for s in stats.values()]) for i in range(3)]
ts = [np.mean([s[i][1] for s in stats.values()]) for i in range(3)]
print("target means", np.round(tm, 1), "stds", np.round(ts, 1))
for f, st in stats.items():
    ex = []
    for i, ch in enumerate("yuv"):
        m, s = st[i]; k = (ts[i] / s) ** 0.5  # half-way toward the shared spread
        k = max(0.75, min(1.3, k))
        ex.append(f"{ch}='clip((val-{m:.2f})*{k:.3f}+{tm[i]:.2f},0,255)'")
    subprocess.check_call(["ffmpeg","-nostdin","-loglevel","error","-y","-i",f,"-vf","format=yuv420p,lutyuv=" + ":".join(ex),
        "-c:v","libx264","-preset","slow","-crf","14","-g","15","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:a","copy",f"{dst}/{os.path.basename(f)}"])
    print(os.path.basename(f), "Y", round(st[0][0]), "->", round(tm[0]))
