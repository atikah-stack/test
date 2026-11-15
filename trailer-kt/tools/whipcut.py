# Bake the shot sequence with whip-pan transitions (slide + directional motion blur + mix), 30fps 1080x1920.
import cv2, numpy as np, subprocess, math, sys
W,H,FPS=1080,1920,30
V="/home/user/test/trailer-kt/assets/v/"
# (file, comp_start, comp_end, media_start)
shots=[("s1-estab",0,3.37,0),("s2-facade",3.37,5.73,0),("s3-chandelier",5.73,8.10,0),("s4-lounge",8.10,9.68,0),
       ("s5-dining",9.68,12.04,0),("s6-kitchen",12.04,13.62,0),("s7-master",13.62,15.20,0),("s9-stairs",15.20,15.99,0),
       ("s10-dusk-night",15.99,21.51,0),("s11-final-night",21.51,24.94,2.37)]
# whip direction at each cut (unit vector the image travels)
dirs=[(-1,0),(0,1),(1,0),(-1,0),(1,0),(-1,0),(0,-1),(-1,0),(-0.8,0.6)]
T=4            # half window in frames (8-frame whip ~0.27s)
TOTAL=round(24.94*FPS)
class Reader:
    def __init__(s,path): s.cap=cv2.VideoCapture(path); s.n=int(s.cap.get(cv2.CAP_PROP_FRAME_COUNT)); s.pos=-1; s.cache={}
    def get(s,k):
        k=max(0,min(s.n-1,k))
        if k in s.cache: return s.cache[k]
        while s.pos<k:
            ok,fr=s.cap.read(); s.pos+=1
            if not ok: fr=s.cache[max(s.cache)] if s.cache else np.zeros((H,W,3),np.uint8)
            s.cache[s.pos]=fr
            for old in [c for c in s.cache if c<s.pos-12]: del s.cache[old]
        return s.cache[k]
readers={}
def shot_frame(i,f,extra_scale=1.0):
    name,cs,ce,ms=shots[i]
    if name not in readers: readers[name]=Reader(V+name+".mp4")
    k=round(ms*FPS)+(f-round(cs*FPS))
    img=readers[name].get(k)
    # slow push-in 1.00 -> 1.05 across the shot
    u=(f-cs*FPS)/((ce-cs)*FPS); sc=(1+0.05*min(max(u,0),1.1))*extra_scale
    M=cv2.getRotationMatrix2D((W/2,H/2),0,sc)
    return cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
def line_kernel(L,d):
    k=int(L)|1; K=np.zeros((k,k),np.float32); c=k//2
    cv2.line(K,(int(round(c-d[0]*c)),int(round(c-d[1]*c))),(int(round(c+d[0]*c)),int(round(c+d[1]*c))),1.0,1,cv2.LINE_AA)
    return K/K.sum()
def shift_blur(img,dx,dy,blur,dvec):
    M=np.float32([[1,0,dx],[0,1,dy]])
    sh=cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    if blur<6: return sh.astype(np.float32)
    q=4
    sm=cv2.resize(sh,(W//q,H//q),interpolation=cv2.INTER_AREA).astype(np.float32)
    sm=cv2.filter2D(sm,-1,line_kernel(max(3,blur/q),dvec),borderType=cv2.BORDER_REFLECT)
    return cv2.resize(sm,(W,H),interpolation=cv2.INTER_LINEAR)
cuts=[round(s[1]*FPS) for s in shots[1:]]
out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",V+"baked-whip.mp4"],stdin=subprocess.PIPE)
def shot_at(f):
    for i,(n,cs,ce,ms) in enumerate(shots):
        if f<round(ce*FPS): return i
    return len(shots)-1
for f in range(TOTAL):
    near=[ci for ci,c in enumerate(cuts) if c-T<=f<c+T]
    if near:
        ci=near[0]; c=cuts[ci]; d=dirs[ci]
        u=(f-(c-T)+0.5)/(2*T)                     # 0..1 across the whip
        e=u*u*(3-2*u)
        travel=0.55*W                                # how far the frames slide
        blur=0.42*W*math.sin(math.pi*u)              # motion-blur length peaks mid-whip
        A=shot_frame(ci,f); B=shot_frame(ci+1,f)
        a=shift_blur(A,d[0]*travel*e,d[1]*travel*e,blur,d)
        b=shift_blur(B,-d[0]*travel*(1-e),-d[1]*travel*(1-e),blur,d)
        m=min(max((u-0.35)/0.3,0),1); m=m*m*(3-2*m)
        fr=(a*(1-m)+b*m)
        fr=np.clip(fr,0,255).astype(np.uint8)
    else:
        fr=shot_frame(shot_at(f),f)
    out.stdin.write(fr.tobytes())
    if f%60==0: print(f,flush=True)
out.stdin.close(); out.wait(); print("done")
