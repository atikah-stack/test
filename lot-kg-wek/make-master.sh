#!/usr/bin/env bash
# Rebuilds assets/video/drone.mp4 from the original drone file on Google Drive (file 1qiRjzWnFmSUN1ti-1EgDrsYfM7aooAqC).
set -e; cd "$(dirname "$0")"; mkdir -p assets/src assets/video
SRC=assets/src/drone-original.mov
[ -f "$SRC" ] || curl -L -o "$SRC" "https://drive.usercontent.google.com/download?id=1qiRjzWnFmSUN1ti-1EgDrsYfM7aooAqC&export=download&confirm=t"
ffmpeg -y -i "$SRC" -c:v libx264 -crf 14 -preset slow -g 12 -an -movflags +faststart assets/video/drone.mp4
