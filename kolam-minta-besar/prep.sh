#!/usr/bin/env bash
# Builds assets/video/stab.mp4 (git-ignored) from the Drive original
# (file 1bCBNmlROWNolng2wik2-_TSIQPETdId0 saved as assets/src/original.mov):
# two-pass vidstab stabilisation, light sharpen, constant 60 fps.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets/video
ffmpeg -v error -y -i assets/src/original.mov -vf "vidstabdetect=shakiness=6:accuracy=15:result=stab.trf" -f null -
ffmpeg -v error -y -i assets/src/original.mov -map 0:v:0 -map 0:a:0 \
  -vf "vidstabtransform=input=stab.trf:smoothing=24:optzoom=1:zoomspeed=0.2:interpol=bicubic:crop=keep,unsharp=5:5:0.4:3:3:0,eq=contrast=1.03:saturation=1.04,fps=60,format=yuv420p" \
  -c:v libx264 -preset slow -crf 15 -profile:v high -level 5.1 -g 120 -c:a aac -b:a 320k -ar 48000 assets/video/stab.mp4
rm -f stab.trf
