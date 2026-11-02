"""Give every shot the same bright, soft look: one shared style, plus a per-shot exposure and
white-balance nudge so each clip lands on the same brightness and the same neutral sheet colour.
Usage: python3 tools/even_grade.py [passes]"""
import json, math, re, subprocess, sys

HF = ["node", "/root/.claude/plugins/marketplaces/hyperframes/skills/hyperframes/scripts/plugin-cli.mjs"]
STYLE = {"contrast": -0.08, "highlights": -0.22, "shadows": 0.22, "blacks": 0.08, "whites": 0.0,
         "vibrance": 0.04, "saturation": -0.1}
TARGET_Y, TARGET_U, TARGET_V = 182.0, 127.5, 129.0   # bright sheet, neutral with a touch of warmth

html = open("index.html").read()
shots = re.findall(r'<video[^>]*id="(s\d+)"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', html)
state = {sid: {"exposure": 0.3, "temperature": 0.0, "tint": 0.0} for sid, _, _ in shots}

def apply():
    for sid, st in state.items():
        g = {"intensity": 1, "adjust": dict(STYLE, **{k: round(v, 3) for k, v in st.items()})}
        subprocess.run(HF + ["media-treatment", "--apply", "--selector", f"#{sid}", "--grading", json.dumps(g)],
                       check=True, capture_output=True)

def measure():
    times = ",".join(str(round(float(s) + float(d) / 2, 2)) for _, s, d in shots)
    out = subprocess.run(HF + ["snapshot", "--at", times], capture_output=True, text=True).stdout
    files = sorted(re.findall(r"(/\S+frame-\d+-at-[\d.]+s\.png)", out))[: len(shots)]
    res = {}
    for (sid, _, _), f in zip(shots, files):
        # measure the bed sheet only: the top and bottom bands, low-saturation pixels
        o = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=64:114,format=yuv444p", "-f", "rawvideo", "-"],
                           capture_output=True).stdout
        n = 64 * 114
        Yp, Up, Vp = o[:n], o[n:2 * n], o[2 * n:3 * n]
        idx = [i for i in range(n) if (i // 64 < 16 or i // 64 >= 98) and abs(Up[i] - 128) < 14 and abs(Vp[i] - 128) < 14 and Yp[i] > 60]
        if len(idx) < 40:
            idx = [i for i in range(n) if abs(Up[i] - 128) < 10 and abs(Vp[i] - 128) < 10 and Yp[i] > 60]
        res[sid] = tuple(sum(c[i] for i in idx) / len(idx) for c in (Yp, Up, Vp))
    return res

passes = int(sys.argv[1]) if len(sys.argv) > 1 else 3
for p in range(passes):
    apply()
    m = measure()
    print(f"pass {p + 1}:", {k: tuple(round(x) for x in v) for k, v in m.items()})
    for sid, (Y, U, V) in m.items():
        st = state[sid]
        st["exposure"] = max(-0.5, min(1.2, st["exposure"] + 0.9 * math.log2(TARGET_Y / max(Y, 1))))
        st["temperature"] = max(-0.3, min(0.3, st["temperature"] - 0.015 * (V - TARGET_V) + 0.015 * (U - TARGET_U)))
        st["tint"] = max(-0.2, min(0.2, st["tint"] + 0.01 * (V - TARGET_V) - 0.005 * (U - TARGET_U)))
apply()
json.dump(state, open("tools/even_grade_state.json", "w"), indent=1)
print("final", {k: {a: round(b, 2) for a, b in v.items()} for k, v in state.items()})
