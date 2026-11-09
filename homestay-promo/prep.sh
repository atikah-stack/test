#!/usr/bin/env bash
# Rebuilds assets/video/talent.mp4 (too big for git) from the Google Drive original:
# 720p -> 1080x1920, light sharpen, and clears the strip of burned-in CapCut captions
# that sits just below the subtitle box.
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i assets/src/drive-original.mov -filter_complex \
  "[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.45:5:5:0,delogo=x=236:y=1522:w=608:h=56,split[a][b];[b]crop=640:76:220:1512,boxblur=12:2[s];[a][s]overlay=220:1512,format=yuv420p[v]" \
  -map "[v]" -map 0:a:0 -c:v libx264 -crf 14 -preset slow -r 24 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
