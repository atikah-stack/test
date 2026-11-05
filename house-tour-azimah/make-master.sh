#!/usr/bin/env bash
# Rebuilds assets/video/tour.mp4 (1080x1920 SDR, 25 fps) from the 4K HLG original.
# The original comes from Google Drive file 1rFShYif3hG_VNMcubkkcgJk2tH8rX10E ("Full Review 1 Azimah Kemaman").
set -e
cd "$(dirname "$0")"
SRC="assets/src/Full Review 1 Azimah Kemaman.mov"
[ -f "$SRC" ] || curl -L -o "$SRC" "https://drive.usercontent.google.com/download?id=1rFShYif3hG_VNMcubkkcgJk2tH8rX10E&export=download&confirm=t"
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:flags=lanczos"
ffmpeg -y -i "$SRC" -vf "$TM" -r 25 -c:v libx264 -crf 15 -preset medium -g 12 -c:a aac -b:a 256k -movflags +faststart assets/video/tour.mp4
