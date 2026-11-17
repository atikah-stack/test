# Custom walk-through stabiliser: similarity motion with label band masked, per-shot Gaussian path smoothing.
import cv2, numpy as np, subprocess, sys
src,dst=sys.argv[1],sys.argv[2]
SIG=float(sys.argv[3]) if len(sys.argv)>3 else 20
ZOOM=float(sys.argv[4]) if len(sys.argv)>4 else 1.12
W,H=1080,1920; w,h=540,960; s=W/w
def reader(path,size):
    p=subprocess.Popen(["ffmpeg","-v","error","-i",path,"-vf",f"fps=30,scale={size[0]}:{size[1]}","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    n=size[0]*size[1]*3
    while True:
        b=p.stdout.read(n)
        if len(b)<n: return
        yield np.frombuffer(b,np.uint8).reshape(size[1],size[0],3)
mask=np.full((h,w),255,np.uint8); mask[600:775,:]=0; mask[:12,:]=0; mask[-12:,:]=0; mask[:,:12]=0; mask[:,-12:]=0
T=[]; prev=None; cut=[]
for f in reader(src,(w,h)):
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    if prev is None: T.append((0,0,0,0)); cut.append(True); prev=g; continue
    p0=cv2.goodFeaturesToTrack(prev,500,0.005,7,mask=mask)
    ok=False
    if p0 is not None and len(p0)>12:
        p1,st,_=cv2.calcOpticalFlowPyrLK(prev,g,p0,None,winSize=(21,21),maxLevel=3)
        gd=st.ravel()==1
        if gd.sum()>10:
            M,inl=cv2.estimateAffinePartial2D(p0[gd],p1[gd],method=cv2.RANSAC,ransacReprojThreshold=2.0)
            if M is not None and inl.sum()>8:
                dx,dy=M[0,2]*s,M[1,2]*s; da=np.arctan2(M[1,0],M[0,0]); ds=np.log(np.hypot(M[0,0],M[1,0]))
                ok=True
    diff=np.abs(g.astype(np.int16)-prev.astype(np.int16)).mean()
    if not ok or diff>40 or abs(dx)>200 or abs(dy)>300:
        T.append((0,0,0,0)); cut.append(True)
    else:
        T.append((dx,dy,da,ds)); cut.append(False)
    prev=g
T=np.array(T,np.float64); n=len(T)
traj=np.cumsum(T,0)
# per-segment gaussian smoothing
sm=np.zeros_like(traj); starts=[i for i in range(n) if cut[i]]+[n]
k=int(SIG*3); x=np.arange(-k,k+1); ker=np.exp(-x**2/(2*SIG**2)); ker/=ker.sum()
for a,b in zip(starts[:-1],starts[1:]):
    seg=traj[a:b]
    pad=np.pad(seg,((k,k),(0,0)),mode="reflect" if len(seg)>k else "edge")
    for c in range(4): sm[a:b,c]=np.convolve(pad[:,c],ker,"valid")
corr=sm-traj
mx,my=(ZOOM-1)/2*W*0.95,(ZOOM-1)/2*H*0.95
corr[:,0]=np.clip(corr[:,0],-mx,mx); corr[:,1]=np.clip(corr[:,1],-my,my); corr[:,2]=np.clip(corr[:,2],-0.035,0.035); corr[:,3]=0
out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-crf","14","-preset","medium","-g","30","-pix_fmt","yuv420p",dst],stdin=subprocess.PIPE)
for i,f in enumerate(reader(src,(W,H))):
    if i>=n: break
    dx,dy,da,ds=corr[i]
    M=cv2.getRotationMatrix2D((W/2,H/2),np.degrees(da),ZOOM*np.exp(ds))
    M[0,2]+=dx; M[1,2]+=dy
    o=cv2.warpAffine(f,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    out.stdin.write(o.tobytes())
out.stdin.close(); out.wait()
print("frames",n,"cuts",sum(cut),"max corr px",np.abs(corr[:,:2]).max(0).round(1))
