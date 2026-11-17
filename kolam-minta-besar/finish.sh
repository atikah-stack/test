#!/usr/bin/env bash
# Final composite: original tour (no stabilisation) (trimmed at 152.2 s, where the source turns to black-bar frames)
# + transparent hook overlay (renders/hook.mov) + outro card (renders/outro.mp4, 0.4 s cross-fade).
# Render the overlays first:  npx hyperframes render -f 60 --format mov --prores-profile 4444 -o renders/hook.mov
#                              (cd outro && npx hyperframes render --sdr -f 60 --crf 14 -o ../renders/outro.mp4)
set -euo pipefail
cd "$(dirname "$0")"
END=152.2; OFF=151.8
ffmpeg -v error -y -t $END -i assets/src/original.mov -i renders/hook.mov -i renders/outro.mp4 -ss 139 -t 5.2 -i assets/src/original.mov -filter_complex \
 "[0:v]fps=60,setpts=PTS-STARTPTS,format=yuv420p[b];[1:v]setpts=PTS-STARTPTS[h];[b][h]overlay=eof_action=pass:format=auto,format=yuv420p,fps=60[v0];[2:v]fps=60,format=yuv420p[o];[v0][o]xfade=transition=fade:duration=0.4:offset=$OFF[v];[3:a]volume=0.7,afade=t=in:d=0.3,afade=t=out:st=3.6:d=1.4[bed];[2:a][bed]amix=inputs=2:normalize=0[oa];[0:a]atrim=0:$END[ba];[ba][oa]acrossfade=d=0.4[a0];[a0]loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -b:v 17M -maxrate 20M -bufsize 34M -profile:v high -level 5.1 -g 120 -pix_fmt yuv420p \
 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 320k -ar 48000 -movflags +faststart renders/mahligai-minta-besar-kolam-asal.mp4
