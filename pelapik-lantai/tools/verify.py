import cv2,numpy as np,subprocess,sys,re
from rapidocr_onnxruntime import RapidOCR
ocr=RapidOCR(); W,H=1080,1920
PAT=re.compile(r"(C[O0]B|[O0]BR|BRA|EOBR|M[A4]T|ULTR|LTRA)",re.I)
path=sys.argv[1]; step=int(sys.argv[2]) if len(sys.argv)>2 else 2; rot=len(sys.argv)>3
p=subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
f=0; hits=[]
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    if f%step==0:
        im=np.frombuffer(b,np.uint8).reshape(H,W,3)
        ims=[im]+([cv2.rotate(im,cv2.ROTATE_90_CLOCKWISE),cv2.rotate(im,cv2.ROTATE_90_COUNTERCLOCKWISE)] if rot else [])
        for x in ims:
            res,_=ocr(x)
            for box,t,s in (res or []):
                if PAT.search(t.replace(" ","")) and float(s)>0.6: hits.append((f,t,round(float(s),2),[int(v) for v in np.mean(box,0)]))
    f+=1
print(path.split("/")[-1],"checked",f,"frames; brand hits:",len(hits)); [print(" ",h) for h in hits[:40]]
