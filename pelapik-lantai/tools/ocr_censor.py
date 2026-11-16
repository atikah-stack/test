# Censor ONLY the brand words (COBRA / MAT / ULTRA logo) using OCR detection + homography propagation.
import cv2, numpy as np, subprocess, sys, json, re
from rapidocr_onnxruntime import RapidOCR
W,H=1080,1920
name=sys.argv[1]; src=sys.argv[2]; dst=sys.argv[3]; rot=sys.argv[4]=="rot" if len(sys.argv)>4 else False
ocr=RapidOCR()
def frames(path):
    p=subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(np.frombuffer(b,np.uint8).reshape(H,W,3))
    return out
PAT=re.compile(r"(C[O0D]B|[O0D]BR|BRA|EOBR|COCR|M[A4]T|ULT|LTR|TRA\\b|C[O0]BRA)",re.I)
def brand(t):
    t=t.replace(" ","").upper()
    return bool(PAT.search(t)) or t in ("RA","MA","AT","CO")
fr=frames(src); n=len(fr)
gray=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in fr]
# frame->frame homographies
lk=dict(winSize=(25,25),maxLevel=4,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,30,0.01))
Hs=[]
for f in range(n-1):
    p0=cv2.goodFeaturesToTrack(gray[f],1200,0.01,10)
    p1,st,_=cv2.calcOpticalFlowPyrLK(gray[f],gray[f+1],p0,None,**lk)
    g=st.ravel()==1
    Hm,_=cv2.findHomography(p0[g],p1[g],cv2.RANSAC,2.0) if g.sum()>8 else (None,None)
    Hs.append(Hm if Hm is not None else np.eye(3))
ANG=[0,90,-90,35,-35] if rot else [0]
def rot_img(img,a):
    if a==0: return img,None
    c=(W/2,H/2); M=cv2.getRotationMatrix2D(c,a,1.0)
    cos,sin=abs(M[0,0]),abs(M[0,1]); nw,nh=int(H*sin+W*cos),int(H*cos+W*sin)
    M[0,2]+=nw/2-c[0]; M[1,2]+=nh/2-c[1]
    return cv2.warpAffine(img,M,(nw,nh),borderValue=(0,0,0)),cv2.invertAffineTransform(M)
def detect(img):
    polys=[]
    for a in ANG:
        im,Mi=rot_img(img,a)
        res,_=ocr(im)
        for box,txt,sc in (res or []):
            if not brand(txt): continue
            b=np.array(box,np.float32)
            if Mi is not None: b=(np.hstack([b,np.ones((len(b),1),np.float32)])@Mi.T).astype(np.float32)
            polys.append(b)
    return polys
det=[]
for f in range(n):
    det.append(detect(fr[f]))
    if f%25==0: print(name,f,len(det[-1]),flush=True)
# propagate +-K frames with homographies
K=8
masks=[np.zeros((H,W),np.uint8) for _ in range(n)]
def warp(poly,Hm): return cv2.perspectiveTransform(poly.reshape(-1,1,2),Hm).reshape(-1,2)
for f in range(n):
    for poly in det[f]:
        # pad polygon around its centre
        c=poly.mean(0); pp=c+(poly-c)*1.25
        cv2.fillPoly(masks[f],[pp.astype(np.int32)],255)
        q=pp.copy()
        for g in range(f+1,min(n,f+K+1)):
            q=warp(q,Hs[g-1]); cv2.fillPoly(masks[g],[q.astype(np.int32)],255)
        q=pp.copy()
        for g in range(f-1,max(-1,f-K-1),-1):
            q=warp(q,np.linalg.inv(Hs[g])); cv2.fillPoly(masks[g],[q.astype(np.int32)],255)
out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","25","-i","-","-c:v","libx264","-crf","14","-preset","medium","-g","12","-pix_fmt","yuv420p",dst],stdin=subprocess.PIPE)
blk=28
cover=[]
for f in range(n):
    m=cv2.dilate(masks[f],np.ones((15,15),np.uint8))
    a=np.clip(cv2.GaussianBlur(m.astype(np.float32)/255,(0,0),4)*1.5,0,1)[...,None]
    sm=cv2.resize(fr[f],(W//blk,H//blk),interpolation=cv2.INTER_AREA)
    mo=cv2.GaussianBlur(cv2.resize(sm,(W,H),interpolation=cv2.INTER_NEAREST),(0,0),blk*0.5).astype(np.float32)
    o=fr[f].astype(np.float32)*(1-a)+mo*a
    out.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
    cover.append(int(len(det[f])))
out.stdin.close(); out.wait()
json.dump({"n":n,"det_per_frame":cover},open(dst+".json","w"))
print(name,"done",n,"frames; frames with 0 detections:",sum(1 for c in cover if c==0))
