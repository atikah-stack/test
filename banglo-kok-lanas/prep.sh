#!/usr/bin/env bash
# Builds assets/video/*.mp4 (git-ignored) from the raw clips in assets/src (Drive folder
# 1fosVyx05sfufAayhlKjIwvkPBmiCEIfd): upright 1080x1920, constant 60 fps, light architectural grade.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets/video
G="eq=contrast=1.06:saturation=1.04:gamma=0.98,colorbalance=rh=.015:bh=-.015,unsharp=5:5:0.35:3:3:0"
for f in assets/src/*.[Mm][Oo][Vv]; do
  n=$(basename "${f%.*}")
  ffmpeg -v error -y -i "$f" -map 0:v:0 -an \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,$G,fps=60,format=yuv420p" \
    -c:v libx264 -preset medium -crf 16 -g 30 -colorspace bt709 -color_primaries bt709 -color_trc bt709 "assets/video/$n.mp4"
done
