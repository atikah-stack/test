#!/usr/bin/env bash
# Builds assets/video (git-ignored) from Drive folder 10S8Wvm7OFy16McDkVHj03uWA9zvLfH2c:
# talent.mp4 (presenter, constant 30 fps, voice cleaned) and one upright 1080x1920 30 fps clip per overlay.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets/video
V="-c:v libx264 -preset medium -crf 15 -g 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709"
ffmpeg -v error -y -i assets/src/talent.mov -map 0:v:0 -map 0:a:0 -vf "fps=30,eq=contrast=1.04:saturation=1.05,unsharp=5:5:0.3:3:3:0" $V \
  -af "highpass=f=90,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5" -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
for f in assets/src/IMG_*; do
  n=$(basename "${f%.*}")
  ffmpeg -v error -y -i "$f" -map 0:v:0 -an -vf "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,eq=contrast=1.04:saturation=1.05,unsharp=5:5:0.3:3:3:0" $V "assets/video/$n.mp4"
done
