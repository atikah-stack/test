#!/usr/bin/env bash
# Builds assets/video (git-ignored). talent.mp4 comes from the Drive original of Aisyah
# (folder 19bxoI6aOnxQjukvzEGf0pt8AbSjO1PWi) saved as assets/src/aisyah-original.mov;
# the B-roll clips are the ones lot-machang/prep.sh builds from folder 10uuTD0r8Dbi2WMvXlp8ns8J7AV0UevRu.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/video
ffmpeg -v error -y -i assets/src/aisyah-original.mov -map 0:v:0 -map 0:a:0 \
  -vf "eq=contrast=1.05:saturation=1.06:gamma=0.98,colorbalance=rs=.03:gs=.01:bs=-.03:rm=.02:bm=-.02,unsharp=5:5:0.35:5:5:0" \
  -c:v libx264 -crf 14 -preset slow -r 25 -g 25 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -af "highpass=f=90,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5" -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
for f in drone-0169 aerial-C51AA0CC aerial-D9D2F1E2 aerial-5899E7BB aerial-BB0FB1E8 road; do cp ../lot-machang/assets/video/$f.mp4 assets/video/; done
