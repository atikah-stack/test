import cv2, numpy as np, json, subprocess, sys
W,H=1080,1920
def frames(path):
    p=subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo","-pix_fmt","gray","-"],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H)
        if len(b)<W*H: break
        out.append(np.frombuffer(b,np.uint8).reshape(H,W))
    return out
cfg=json.load(open(sys.argv[1])); fr=frames(cfg["video"]); n=len(fr)
lk=dict(winSize=(31,31),maxLevel=4,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,40,0.01))
# mask: house band only (exclude sky top & foreground bottom-most) for homography
mask=np.zeros((H,W),np.uint8); mask[cfg.get("band",[700,1500])[0]:cfg.get("band",[700,1500])[1],:]=255
Hf=[None]*(n-1)  # H mapping frame f -> f+1
for f in range(n-1):
    p0=cv2.goodFeaturesToTrack(fr[f],1500,0.01,8,mask=mask)
    p1,st,_=cv2.calcOpticalFlowPyrLK(fr[f],fr[f+1],p0,None,**lk)
    g=st.ravel()==1
    Hm,inl=cv2.findHomography(p0[g],p1[g],cv2.RANSAC,1.5)
    Hf[f]=Hm
def apply(Hm,p):
    v=Hm@np.array([p[0],p[1],1.0]); return [v[0]/v[2],v[1]/v[2]]
lights=[]
for r in cfg["refs"]:
    for l in r["lights"]:
        tr=[None]*n; tr[r["frame"]]=list(l["xy"])
        sc=[None]*n; sc[r["frame"]]=1.0
        for d in (1,-1):
            f=r["frame"]; p=list(l["xy"]); s=1.0
            while 0<=f+d<n:
                g=f+d
                Hm=Hf[f] if d==1 else np.linalg.inv(Hf[g])
                q=apply(Hm,p)
                # local scale from H jacobian
                J=Hm[:2,:2]; s*=np.sqrt(abs(np.linalg.det(J)))
                # refine with LK if possible
                pr,st,_=cv2.calcOpticalFlowPyrLK(fr[f],fr[g],np.array([[p]],np.float32),np.array([[q]],np.float32),flags=cv2.OPTFLOW_USE_INITIAL_FLOW,**lk)
                if st[0][0]==1 and np.hypot(pr[0,0,0]-q[0],pr[0,0,1]-q[1])<4: q=[float(pr[0,0,0]),float(pr[0,0,1])]
                p=q; f=g
                if -80<p[0]<W+80 and -80<p[1]<H+80: tr[g]=[float(p[0]),float(p[1])]; sc[g]=float(s)
                else: break
        lights.append({"name":l["name"],"size":l["size"],"kind":l.get("kind","sconce"),"track":tr,"scale":sc})
for L in lights: print(L["name"],sum(v is not None for v in L["track"]),"/",n, "end", L["track"][-1] and [round(v) for v in L["track"][-1]], "start", L["track"][0] and [round(v) for v in L["track"][0]])
json.dump({"n":n,"lights":lights},open(cfg["out"],"w"))
