import cv2, numpy as np, subprocess, sys, json
W,H=1080,1920
def mat_mask(hsv,cfg):
    m=np.zeros(hsv.shape[:2],np.uint8)
    for lo,hi in cfg["mat"]:
        m|=cv2.inRange(hsv,np.array(lo,np.uint8),np.array(hi,np.uint8))
    if "ymin" in cfg: m[:cfg["ymin"]]=0
    return m
def text_mask(bgr,cfg):
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    m=mat_mask(hsv,cfg)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    k=cfg.get("close",41)
    area=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
    # local mat brightness
    v=hsv[...,2].astype(np.float32)
    mv=cv2.blur(np.where(m>0,v,0),(61,61)); mc=cv2.blur((m>0).astype(np.float32),(61,61))
    local=mv/np.maximum(mc,1e-3)
    dark=(v<local*cfg.get("ratio",0.72)).astype(np.uint8)*255
    if cfg.get("satdrop"):
        sat=hsv[...,1].astype(np.float32)
        ms=cv2.blur(np.where(m>0,sat,0),(61,61))/np.maximum(mc,1e-3)
        dark|=((sat<ms*cfg["satdrop"])).astype(np.uint8)*255
    cand=cv2.bitwise_and(cv2.bitwise_and(area,cv2.bitwise_not(m)),dark)
    cand=cv2.morphologyEx(cand,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(cand)
    keep=np.zeros(n,np.uint8)
    a=st[:,cv2.CC_STAT_AREA]; keep[1:]=((a[1:]>=cfg.get("minA",12))&(a[1:]<=cfg.get("maxA",25000))).astype(np.uint8)
    cand=keep[lab]*255
    # group glyphs into words: close horizontally/vertically
    g=cfg.get("group",25)
    cand=cv2.morphologyEx(cand,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(g*2+1,g*2+1)))
    cand=cv2.dilate(cand,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(g,g)))
    return cand.astype(np.uint8)
def mosaic(img,block):
    sm=cv2.resize(img,(W//block,H//block),interpolation=cv2.INTER_AREA)
    up=cv2.resize(sm,(W,H),interpolation=cv2.INTER_NEAREST)
    return cv2.GaussianBlur(up,(0,0),block*0.6)
if __name__=="__main__":
    cfg=json.load(open(sys.argv[1]))
    src,dst=cfg["src"],cfg["dst"]
    inp=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    out=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","25","-i","-","-c:v","libx264","-crf","14","-preset","medium","-g","12","-pix_fmt","yuv420p",dst],stdin=subprocess.PIPE)
    hist=[]; f=0
    extra=cfg.get("boxes",[])  # manual boxes [f0,f1,x0,y0,x1,y1]
    while True:
        b=inp.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        fr=np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
        m=text_mask(fr,cfg)
        hist.append(m); hist=hist[-3:]
        M=hist[0].copy()
        for h in hist[1:]: M|=h
        for bx in extra:
            if bx[0]<=f<=bx[1]: cv2.rectangle(M,(bx[2],bx[3]),(bx[4],bx[5]),255,-1)
        if cfg.get("floorblur"):
            hsv=cv2.cvtColor(fr,cv2.COLOR_BGR2HSV); mm=mat_mask(hsv,cfg)
            mm=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41)))
            fa=cv2.GaussianBlur(mm.astype(np.float32)/255,(0,0),6)[...,None]
            fr=(fr.astype(np.float32)*(1-fa)+cv2.GaussianBlur(fr,(0,0),cfg["floorblur"]).astype(np.float32)*fa).astype(np.uint8)
        a=np.clip(cv2.GaussianBlur(M.astype(np.float32)/255,(0,0),5)*1.6,0,1)[...,None]
        mo=mosaic(fr,cfg.get("block",22)).astype(np.float32)
        o=fr.astype(np.float32)*(1-a)+mo*a
        out.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
        if cfg.get("debug") and f in cfg["debug"]:
            cv2.imwrite(cfg["dbgdir"]+f"/{cfg['name']}_{f}.jpg",cv2.resize(np.hstack([fr,np.clip(o,0,255).astype(np.uint8)]),(1080,960)))
        f+=1
    out.stdin.close(); out.wait(); print(cfg["name"],"frames",f)
