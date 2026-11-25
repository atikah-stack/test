#!/usr/bin/env bash
# Rebuilds assets/video from the originals in assets/src (interview from Google Drive file 1DWbxGb4fvlxc0o1bwbjjbyj6ZVqSIk2D,
# B-roll from Drive folder 15ZvQOLRjBj7VngrQ3CIfpAe6qMOjWyLm saved in assets/src/drive2).
set -e; cd "$(dirname "$0")"; S=assets/src/copy_374C08B1-1090-4938-8F7A-18E22C0DE928.mov; R=assets/src/drive2
AF="highpass=f=80,afftdn=nf=-28:nt=w,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=200,volume=3dB"; DL="delogo=x=120:y=1415:w=800:h=190"
ffmpeg -y -ss 22.0 -to 45.8 -i $S -vf "$DL,eq=saturation=0.9:contrast=1.03" -r 30 -c:v libx264 -crf 14 -preset slow -g 15 -af "$AF" -c:a aac -b:a 256k -ar 48000 assets/video/t1.mp4
ffmpeg -y -ss 376.0 -to 424.4 -i $S -vf "$DL,colorbalance=rs=.03:gs=.01:bs=-.03:rm=.03:bm=-.02,eq=saturation=1.02" -r 30 -c:v libx264 -crf 14 -preset slow -g 15 -af "$AF" -c:a aac -b:a 256k -ar 48000 assets/video/t2.mp4
W="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"; WARM="colorbalance=rs=.025:bs=-.025:rm=.02:bm=-.02,eq=saturation=1.04"
for f in copy_94BEB817 copy_F371EC91 IMG_3534 IMG_3580 IMG_3615 IMG_3753 IMG_3787 IMG_7124; do
  ffmpeg -y -i $R/$f.mov -map 0:v:0 -vf "$W,$WARM" -r 30 -c:v libx264 -crf 15 -preset slow -g 15 -an assets/video/b-$(echo $f | tr A-Z a-z | cut -d_ -f2).mp4; done
ffmpeg -y -i $R/DJI_0177.mov -map 0:v:0 -vf "$W,eq=saturation=0.95" -r 30 -c:v libx264 -crf 15 -preset slow -g 15 -an assets/video/b-dji.mp4
ffmpeg -y -i $R/img_0046.png -vf "$W" -q:v 2 assets/img/build-1.jpg; ffmpeg -y -i $R/img_00ba.png -vf "$W" -q:v 2 assets/img/build-2.jpg
