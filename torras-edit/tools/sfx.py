"""Synthesise subtle, royalty-free SFX synced to the overlay cues -> stereo 44.1k WAV, exact source length."""
import sys, numpy as np, wave
SR = 44100; DUR = 1972 / 60
N = int(round(DUR * SR)); L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def db(x): return 10 ** (x / 20)
def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def place(sig, t, gain_db, pan=0.0):
    i = int(t * SR); sig = sig[: max(0, N - i)] * db(gain_db)
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))

def pen(dur):  # soft handwriting scratch: band-limited noise in little strokes
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); x = x - onepole_lp(x, 1800); x = onepole_lp(x, 7000)
    strokes = 0.55 + 0.45 * np.sin(2 * np.pi * (5.5 + rng.random()) * t + rng.random() * 6) ** 2
    env = np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.08)
    return x * strokes * env / (np.abs(x).max() + 1e-9)
def shimmer(dur=1.4):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for k in range(9):
        f = rng.uniform(2600, 7200); st = rng.uniform(0, 0.35)
        e = np.where(t > st, np.exp(-(t - st) * rng.uniform(3, 6)), 0) * np.minimum(1, np.maximum(0, (t - st)) / 0.01)
        y += np.sin(2 * np.pi * f * t) * e * rng.uniform(0.4, 1)
    return y / np.abs(y).max()
def whoosh(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); y = np.empty(n); s = 0.0
    for i in range(n):  # sweeping low-pass
        fc = 300 + 3500 * np.sin(np.pi * i / n) ** 2; a = np.exp(-2 * np.pi * fc / SR); s = (1 - a) * x[i] + a * s; y[i] = s
    return y * np.sin(np.pi * t / dur) ** 2 / (np.abs(y).max() + 1e-9)
def pop():
    n = int(0.07 * SR); t = np.arange(n) / SR
    f = 700 + 900 * t / 0.07
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 60)
def mag_click():
    n = int(0.12 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 45)
    clk = rng.standard_normal(n) * np.exp(-t * 600); clk = clk - onepole_lp(clk, 2000)
    return (thump * 0.8 + clk * 0.6) / 1.2

# headline handwriting (t_in, write duration)
for t_in, wd in ((6.00, .8), (16.10, .6), (18.00, .75), (22.80, .65), (23.90, .7), (27.20, .65), (28.62, .7), (30.15, .7), (31.60, .45)):
    place(pen(wd), t_in, -36, pan=-0.15)
place(shimmer(), 16.30, -33, 0.2)            # crystal clear sweep
place(shimmer(1.1), 18.20, -36, -0.2)        # anti-yellowing glass sweep
place(pop(), 22.86, -32); place(pop(), 23.20, -35, 0.3)   # camera ring + pointer
place(whoosh(0.5), 23.98, -34)               # 360 arrow
place(pop(), 24.40, -34, 0.35)               # inset pops in
place(whoosh(0.4), 27.22, -36)               # slim edge
place(mag_click(), 28.75, -28)               # magnetic pulse (with the real mount snap)
place(shimmer(1.0), 28.80, -38)
place(pop(), 30.35, -34)                     # stand highlight
place(shimmer(1.4), 31.68, -34)              # final ring trace
for cut in (28.55, 30.067, 31.55):           # light transition air at the existing cuts
    place(whoosh(0.35), cut - 0.15, -40)

peak = max(np.abs(L).max(), np.abs(R).max()); assert peak < 1.0, peak
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("sfx written", N / SR, "s, peak dBFS %.1f" % (20 * np.log10(peak)))
