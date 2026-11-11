# Cut each shot, apply hand-only skin retouch with a temporally smoothed mask, upscale to 1080x1920.
import sys, subprocess, cv2, numpy as np
sys.path.insert(0, sys.argv[1]); import skin
raw, out = sys.argv[2], sys.argv[3]
EDL = [("s1","b",25.0,2.2,1.0),("s2","a",2.2,2.8,1.0),("s3","b",12.6,3.0,1.0),("s4","a",11.3,2.6,0.85),
       ("s5","b",1.8,3.0,1.0),("s6","b",27.2,3.8,1.0),("s7","b",31.0,2.8,1.0),("s8","b",23.0,2.0,1.0)]
for n, src, ss, d, r in EDL:
    cap = cv2.VideoCapture(f"{raw}/{src}.mov"); cap.set(cv2.CAP_PROP_POS_MSEC, ss * 1000)
    w, h = int(cap.get(3)), int(cap.get(4)); nfr = int(round(d * 30))
    tmp = f"{out}/{n}_v.mp4"
    p = subprocess.Popen(["ffmpeg","-nostdin","-loglevel","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}","-r","30","-i","-",
        "-vf",f"setpts=PTS/{r},fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.35,eq=gamma=1.05:saturation=1.03,format=yuv420p",
        "-c:v","libx264","-preset","slow","-crf","14","-g","15","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",tmp], stdin=subprocess.PIPE)
    prev = None
    for i in range(nfr):
        ok, fr = cap.read()
        if not ok: break
        m = skin.skin_mask(fr)
        m = m if prev is None else 0.35 * m + 0.65 * prev
        prev = m
        p.stdin.write(skin.apply(fr, m).tobytes())
    p.stdin.close(); p.wait()
    aud = f"{out}/{n}.mp4"
    subprocess.check_call(["ffmpeg","-nostdin","-loglevel","error","-y","-i",tmp,"-ss",str(ss),"-t",str(d),"-i",f"{raw}/{src}.mov",
        "-map","0:v","-map","1:a:0","-af",f"atempo={r}","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-shortest",aud])
    subprocess.call(["rm", tmp]); print(n, "done")
