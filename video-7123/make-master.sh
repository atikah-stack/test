#!/usr/bin/env bash
# Rebuilds assets/video/*.mp4 from the originals: IMG_7123.mov (Google Drive file 1uXW_Ymgk1fjDqx_MkTHQQsl5VioF797O)
# and the B-roll clips IMG_3555/3564/3572/3584/3756/3757/3772.mov placed in assets/src/.
set -e; cd "$(dirname "$0")"; mkdir -p assets/src assets/video
SRC=assets/src/IMG_7123.mov
[ -f "$SRC" ] || curl -L -o "$SRC" "https://drive.usercontent.google.com/download?id=1uXW_Ymgk1fjDqx_MkTHQQsl5VioF797O&export=download&confirm=t"
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:flags=lanczos,eq=saturation=1.04:gamma_r=1.02:gamma_b=0.98"
AF="highpass=f=80,afftdn=nf=-28:nt=w,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=200,volume=4dB"
for r in "w1 173.4 206.2" "w2 220.4 241.6" "w3 552.0 560.6"; do set -- $r
  ffmpeg -y -ss $2 -to $3 -i "$SRC" -vf "$TM" -r 30 -c:v libx264 -crf 14 -preset slow -g 15 -af "$AF" -c:a aac -b:a 256k -ar 48000 -movflags +faststart assets/video/$1.mp4; done
for n in 3555 3564 3572 3584 3756 3757 3772; do f=assets/src/IMG_$n.mov; [ -f "$f" ] || continue
  ffmpeg -y -i "$f" -vf "$TM" -r 30 -c:v libx264 -crf 15 -preset slow -g 15 -an -movflags +faststart assets/video/b-img_$n.mp4; done
