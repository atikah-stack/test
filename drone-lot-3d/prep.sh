#!/usr/bin/env bash
# assets/video is git-ignored: copies the graded drone clips that lot-machang/prep.sh (plus the
# 999CF884 / B3AF3D5D lines below) builds from Drive folder 10uuTD0r8Dbi2WMvXlp8ns8J7AV0UevRu.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets/video
B=../lot-machang/assets/src/broll
P="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,eq=contrast=1.04:saturation=1.05"
for k in 999CF884 B3AF3D5D; do
  ffmpeg -v error -y -i $B/copy_${k}-*.mov -map 0:v:0 -vf "$P" -c:v libx264 -crf 14 -preset slow -r 30 -g 30 -pix_fmt yuv420p -an assets/video/aerial-$k.mp4
done
for f in aerial-C51AA0CC aerial-D9D2F1E2 drone-0169; do cp ../lot-machang/assets/video/$f.mp4 assets/video/; done
