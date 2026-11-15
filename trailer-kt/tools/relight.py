import cv2, numpy as np, json, subprocess, sys
W,H=1080,1920
cfg=json.load(open(sys.argv[1]))
d=json.load(open(cfg["tracks"])); n=d["n"]
lights=[L for L in d["lights"] if L["name"] not in cfg.get("skip",[])]
WARM=np.array([1.0,0.58,0.26],np.float32)   # RGB linear-ish warm 2700K
CORE=np.array([1.0,0.82,0.55],np.float32)
yy=np.linspace(0,1,H,dtype=np.float32)[:,None,None]
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def zoom(f):
    z=cfg.get("zoom")
    if not z: return 1.0
    a,b=[L for L in lights if L["name"]==z[0]][0],[L for L in lights if L["name"]==z[1]][0]
    pa,pb,ra,rb=a["track"][f],b["track"][f],a["track"][z[2]],b["track"][z[2]]
    if not(pa and pb): return 1.0
    return np.hypot(pa[0]-pb[0],pa[1]-pb[1])/np.hypot(ra[0]-rb[0],ra[1]-rb[1])
inp=subprocess.Popen(["ffmpeg","-v","error","-i",cfg["video"],"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-crf","14","-preset","medium","-g","15","-pix_fmt","yuv420p",cfg["out"]],stdin=subprocess.PIPE)
for f in range(n):
    b=inp.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    day=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255
    lin=day**2.2
    p=float(smooth(cfg["night_from"],cfg["night_to"],f))  # 0 day ->1 night
    # ambient blue night, darker toward top (sky)
    amb=np.array([0.038,0.052,0.100],np.float32)*(0.55+0.65*yy)
    night=lin*amb
    sky=(1-smooth(0.05,0.46,yy))*np.array([0.004,0.007,0.018],np.float32)
    night=night+sky*0.0
    # practical lights
    light=np.zeros((H,W,3),np.float32); core=np.zeros((H,W,3),np.float32)
    z=zoom(f)
    for i,L in enumerate(lights):
        pt=L["track"][f]
        if not pt: continue
        on=float(smooth(cfg["on_from"]+i*cfg.get("stagger",3),cfg["on_from"]+i*cfg.get("stagger",3)+5,f))
        if on<=0: continue
        s=L["size"]*z
        x0,y0=pt
        Rx=int(11*s+40); Ry=int(20*s+40)
        xa,xb=max(0,int(x0-Rx)),min(W,int(x0+Rx)); ya,yb=max(0,int(y0-Ry)),min(H,int(y0+Ry))
        if xa>=xb or ya>=yb: continue
        X,Y=np.meshgrid(np.arange(xa,xb,dtype=np.float32)-x0,np.arange(ya,yb,dtype=np.float32)-y0)
        ady=np.abs(Y)
        sx=0.55*s+0.32*ady
        beam=np.exp(-(X/sx)**2)*np.exp(-(ady/(5.5*s))**1.6)*(np.clip(ady/(0.6*s),0,1))
        halo=np.exp(-(X**2+Y**2)/(2*(2.2*s)**2))*0.55
        I=(beam*1.9+halo)*on*cfg.get("gain",1.0)
        light[ya:yb,xa:xb]+=I[...,None]*WARM
        c=np.zeros_like(X)
        for sy in (-0.55,0.55):
            c+=np.exp(-(X**2+(Y-sy*s)**2)/(2*(0.28*s)**2))
        core[ya:yb,xa:xb]+=(c*1.6*on)[...,None]*CORE
    # soffit / porch downlights already present in render (warm beige ceilings)
    r,g,bb=day[...,0],day[...,1],day[...,2]
    m=((r-g>0.015)&(r-bb>0.08)&(r>0.62)&(g-bb>0.04)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    nl,lab,st,_=cv2.connectedComponentsWithStats(m)
    keep=np.zeros(nl,np.uint8); keep[1:]=(st[1:,cv2.CC_STAT_AREA]>=cfg.get("minarea",1500))
    mb=keep[lab]
    m=cv2.GaussianBlur(mb.astype(np.float32),(0,0),16)
    m*=cv2.GaussianBlur(cv2.dilate(mb,np.ones((21,21),np.uint8)).astype(np.float32),(0,0),5)
    son=float(smooth(cfg["on_from"]-6,cfg["on_from"]+4,f))
    light+=m[...,None]*WARM*0.55*son
    lit=night+lin*light+core
    # bloom
    hi=np.clip(lit-0.35,0,None)
    bloom=cv2.GaussianBlur(hi,(0,0),9)*0.6+cv2.GaussianBlur(hi,(0,0),28)*0.35
    lit=lit+bloom
    res=lin*(1-p)+lit*p
    # soft filmic tone
    res=res/(1+0.15*res)
    o=np.clip(res,0,1)**(1/2.2)
    # vignette slight at night
    out.stdin.write((o*255+0.5).astype(np.uint8).tobytes())
    if f%30==0: print(f,round(p,2),flush=True)
out.stdin.close(); out.wait()
