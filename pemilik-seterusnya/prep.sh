#!/usr/bin/env bash
# assets/video is git-ignored. talent.mp4 comes from the user's partial edit (Drive folder
# file 16ygROOCg0ebazclekcwmYpBxI64_aBcJ, no transitions) saved as assets/src/clean-edit.mov; drone clips are
# copied from ../drone-lot-3d and ../lot-machang (run their prep.sh first).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets/video
ffmpeg -v error -y -i assets/src/clean-edit.mov -map 0:v:0 -map 0:a:0 -vf "eq=contrast=1.04:saturation=1.05:gamma=0.99,unsharp=5:5:0.3:5:5:0" \
  -c:v libx264 -crf 14 -preset slow -r 25 -g 25 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -af "highpass=f=90,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5" -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
cp ../drone-lot-3d/assets/video/*.mp4 assets/video/
cp ../lot-machang/assets/video/aerial-BB0FB1E8.mp4 ../lot-machang/assets/video/aerial-5899E7BB.mp4 assets/video/
