#!/usr/bin/env bash
# Builds the processed media (too big for git) from the originals.
# $1 = folder holding the Google Drive B-roll files (folder 10uuTD0r8Dbi2WMvXlp8ns8J7AV0UevRu)
set -euo pipefail
cd "$(dirname "$0")"
B=${1:-assets/src/broll}
V="-c:v libx264 -crf 14 -preset slow -r 25 -g 25 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709"
# presenter: light warm grade + sharpen; voice: rumble cut, noise reduction, gentle levelling
ffmpeg -v error -y -i assets/src/drive-original.mov -map 0:v:0 -map 0:a:0 \
  -vf "eq=contrast=1.05:saturation=1.06:gamma=0.98,colorbalance=rs=.03:gs=.01:bs=-.03:rm=.02:bm=-.02,unsharp=5:5:0.35:5:5:0" $V \
  -af "highpass=f=90,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5" -c:a aac -b:a 256k -ar 48000 assets/video/talent.mp4
# D-Log M drone clips: light lift to natural colour
G="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,eq=contrast=1.12:saturation=1.25:gamma=0.97,curves=all='0/0 0.25/0.21 0.75/0.79 1/1'"
ffmpeg -v error -y -i "$B"/dji_fly_20261027_132706_0169_*.mov -map 0:v:0 -vf "$G" $V -an assets/video/drone-0169.mp4
ffmpeg -v error -y -i "$B"/dji_fly_20261027_132930_0172_*.mov -map 0:v:0 -vf "$G" $V -an assets/video/drone-0172.mp4
# phone footage (already graded by the phone)
P="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,eq=contrast=1.04:saturation=1.05"
ffmpeg -v error -y -i "$B"/IMG_0019.MOV -map 0:v:0 -vf "$P" $V -an assets/video/road.mp4
for k in 5899E7BB BB0FB1E8 C51AA0CC D084B064 D9D2F1E2; do
  ffmpeg -v error -y -i "$B"/copy_${k}-*.mov -map 0:v:0 -vf "$P" $V -an assets/video/aerial-$k.mp4
done
