#!/usr/bin/env bash
# Rebuilds assets/video/talent.mp4 (too big for git) from the clean Google Drive original
# (1080x1920, no burned-in captions). Download it first to assets/src/drive-original-1080.mov:
#   https://drive.google.com/file/d/1-mVMUK0zPdc4HJrLgYzpUjqZPlAE-Jd5/view
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i assets/src/drive-original-1080.mov -map 0:v:0 -map 0:a:0 -vf format=yuv420p \
  -c:v libx264 -crf 14 -preset slow -r 25 -g 50 -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
