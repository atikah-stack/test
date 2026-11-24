# TORRAS Magnetic Stand Case — TikTok enhancement edit sheet

Output: `output/TORRAS_enhanced.mp4` — 1080×1920, 60 fps, **1,972 frames / 32.867 s (identical to source)**.

## What was preserved
- Every source frame, same order, same speed, same duration. No cuts, crops, trims or AI footage.
- **Original hook** ("Loved my Torras case so much, i bought it again. No regrets.") — burned into the
  source, untouched. It hard-cuts out at **5.22 s (frame 313)**; the graphics layer is fully transparent before that.
- **Original colours** — no filter, no grade, no skin retouch (per request). Graphics are composited on top only.

## Typography
- Headlines: **Gaegu, 55 px**, white, centred at x = 50 %, y = 38 / 40 / 62 % of frame (within 38–62 % band).
  Gaegu is a free (OFL) look-alike of CapCut's *Ugly Dave*, which is a paid font licensed for CapCut only.
- Animation: pen-following stroke reveal (0.45–0.8 s), Soft-Pink (#F4B7CE) heart, sparkle on completion, 0.3 s fade-out.
- Small labels: DM Sans 29 px (white / Champagne Cream #FFF4E8). **No text shadows.**

## Cue list (rebuild in CapCut with Ugly Dave if you prefer)
| Time (s) | Text | Y | Graphic (motion-tracked to the real product) |
|---|---|---|---|
| 6.00–8.40 | Unboxing my favourite ♡ | 38 % | heart + sparkle |
| 16.10–17.90 | Crystal Clear ♡ | 38 % | edge trace + light sweep on the clear case (16.2–17.2) |
| 18.00–19.35 | Anti-Yellowing Design | 38 % | clean-glass sweep, thin line, twinkles |
| 22.80–23.85 | Everyday Protection ♡ | 62 % | dashed circle round camera + "Raised camera edge" pointer |
| 23.90–25.50 | 360° Rotating Stand ✨ | 38 % | circular arrow at hinge, "360°" tag, 1.9× zoom inset bubble |
| 27.20–28.45 | Slim & Comfortable | 40 % | edge highlight + "Slim profile" pointer |
| 28.62–30.00 | Magnetic Compatible ♡ | 62 % | outline + magnetic pulses on the real car mount |
| 30.15–31.50 | Hands-Free Viewing ♡ | 38 % | stand-foot glow + "Built-in stand" pointer |
| 31.60–32.80 | Worth it ♡ | 38 % | clockwise MagSafe-ring trace with light trail |

## Sound
Original audio track is silent and is kept; subtle synthesized SFX are mixed in (pen scratch, shimmer,
soft whoosh, UI pop, magnetic click). Add your TikTok sound on top as usual.

## Rebuild
```
python3 tools/track.py source.mov tracks.json
python3 tools/sfx.py sfx.wav
python3 tools/overlay.py source.mov tracks.json FONTDIR | ffmpeg -i source.mov -f rawvideo -pix_fmt rgba -s 1080x1920 -r 60 -i - -i sfx.wav \
  -filter_complex "[1:v]scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[ov];[0:v][ov]overlay=format=yuv420[v];[2:a]volume=8dB[s];[0:a][s]amix=inputs=2:normalize=0:duration=first[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 13 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac out.mp4
```
