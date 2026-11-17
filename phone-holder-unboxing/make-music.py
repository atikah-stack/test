#!/usr/bin/env python3
"""Soft aesthetic lo-fi bed (procedural, royalty-free).
  python3 make-music.py      -> assets/audio/music.wav    84 BPM, Fmaj7-Em7-Dm7-Cmaj7 (version A)
  python3 make-music.py b    -> assets/audio/music-b.wav  92 BPM, Cmaj7-Am7-Fmaj7-G6, brighter (version B)
  python3 make-music.py c    -> assets/audio/music-c.wav  88 BPM, Am7-Fmaj7-Cmaj7-Gmaj7 (version C)
"""
import numpy as np, wave, os, sys

VAR = sys.argv[1] if len(sys.argv) > 1 else "a"
SR, DUR = 44100, 32.0
BPM = {"b": 92, "c": 88}.get(VAR, 84)
beat = 60 / BPM
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng({"b": 11, "c": 23}.get(VAR, 7))

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def tone(m, dur, amp, kind="keys"):
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    if kind == "keys":   # soft electric-piano: sine + gentle 2nd partial, bell-ish decay
        s = np.sin(2*np.pi*f*t) + 0.25*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + 0.08*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
        env = np.minimum(t / 0.01, 1) * np.exp(-t * 1.6)
    elif kind == "pad":
        s = sum(np.sin(2*np.pi*f*(1 + d)*t + p) for d, p in [(-0.003, 0), (0, 1.3), (0.003, 2.1)]) / 3
        env = np.minimum(t / 0.8, 1) * np.minimum((dur - t) / 0.8, 1)
    else:                # bass
        s = np.sin(2*np.pi*f*t) + 0.15*np.sin(2*np.pi*2*f*t)
        env = np.minimum(t / 0.02, 1) * np.exp(-t * 1.2)
    return s * env * amp

def add(sig, at, pan=0.0):
    i = max(0, int(at * SR)); j = min(n, i + len(sig))
    if j <= i: return
    sig = sig[: j - i]
    L[i:j] += sig * (1 - pan) ; R[i:j] += sig * (1 + pan)

if VAR == "c":
    chords = [[45, 48, 52, 55], [41, 45, 48, 52], [48, 52, 55, 59], [43, 47, 50, 54]]  # Am7 Fmaj7 Cmaj7 Gmaj7
    roots = [33, 41, 36, 43]
elif VAR == "b":
    chords = [[48, 52, 55, 59], [45, 48, 52, 55], [53, 57, 60, 64], [55, 59, 62, 64]]  # Cmaj7 Am7 Fmaj7 G6
    roots = [36, 33, 41, 43]
else:
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
    roots = [41, 40, 38, 36]
bar = 4 * beat
t0 = 0.0; k = 0
while t0 < DUR:
    c = chords[k % 4]
    for m in c: add(tone(m, bar + 0.9, 0.035, "pad"), t0, 0)
    add(tone(roots[k % 4], bar, 0.10, "bass"), t0)
    arp = [c[0] + 12, c[2] + 12, c[1] + 12, c[3] + 12, c[2] + 12, c[0] + 24, c[3] + 12, c[1] + 12]
    for i, m in enumerate(arp):
        if i in (3, 7) and rng.random() < 0.5: continue
        add(tone(m, 1.6, 0.05 + 0.01 * rng.random()), t0 + i * beat / 2 + rng.normal(0, 0.006), 0.3 if i % 2 else -0.3)
    # soft brushed hat on off-beats + gentle kick on 1 & 3
    for b in range(4):
        h = rng.normal(0, 1, int(0.06 * SR)); h = np.diff(h, prepend=0) * np.exp(-np.arange(len(h)) / SR * 70) * 0.012
        add(h, t0 + b * beat + beat / 2, 0.2)
        if b in (0, 2):
            tt = np.arange(int(0.25 * SR)) / SR
            add(np.sin(2*np.pi*(55 + 60*np.exp(-tt*30))*tt) * np.exp(-tt*14) * 0.10, t0 + b * beat)
    t0 += bar; k += 1

# warmth: one-pole lowpass + simple stereo delay "room"
def lp(x, fc=4500):
    a = np.exp(-2*np.pi*fc/SR); y = np.empty_like(x); z = 0.0
    for i in range(len(x)): z = (1 - a) * x[i] + a * z; y[i] = z
    return y
L, R = lp(L), lp(R)
for d, g in [(0.113, 0.22), (0.171, 0.18), (0.263, 0.12)]:
    s = int(d * SR); L[s:] += R[:-s] * g; R[s:] += L[:-s] * g * 0.9
fade = np.ones(n); fo = int(2.5 * SR); fade[-fo:] = np.linspace(1, 0, fo); fade[: int(0.4*SR)] = np.linspace(0, 1, int(0.4*SR))
st = np.stack([L * fade, R * fade], 1); st /= np.abs(st).max() / 0.8
os.makedirs("assets/audio", exist_ok=True)
OUT = "assets/audio/music.wav" if VAR == "a" else f"assets/audio/music-{VAR}.wav"
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
print(OUT, BPM, DUR)
