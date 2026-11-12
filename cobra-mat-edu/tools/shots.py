import sys, subprocess, json
sys.path.insert(0,'tools'); from timing import M, VO_END, TAIL
U='/root/.claude/uploads/312104a0-2471-596f-a5e2-4be72769a4ce/'
F={'8978':'92e258b9-IMG_8978','7207':'ce5e0e41-IMG_7207','7205':'a5513e48-IMG_7205','7206':'8ce24096-IMG_7206',
   '2876':'92680bcd-IMG_2876','8976':'a4c99e80-IMG_8976','8977':'e4b156d8-IMG_8977','2858':'d2e48352-IMG_2858'}
END=M(VO_END)+TAIL
# id, clip, src start, old start, old end (None = to video end)
SEG=[('s01','8978',0.0,0.0,4.25),('s02','2858',2.0,4.25,9.3),('s03','7207',0.0,9.3,11.0),('s04','7205',5.0,11.0,12.3),
     ('s05','7206',0.5,12.3,13.6),('s06','2876',1.5,13.6,22.85),('s07','8976',0.5,22.85,25.62),
     ('s09','8977',0.0,27.3,31.34),('s11','8977',4.1,36.37,38.9),('s12','7206',2.6,38.9,41.4),
     ('s13','7205',0.0,41.4,48.64),('s14','7207',4.5,48.64,53.7),('s15','2858',6.5,53.7,57.05),
     ('s16','2858',0.0,57.05,62.87),('s17','8978',3.5,62.87,66.3),('s18','7206',5.4,66.3,None)]
# brand card (25.62-27.3) and product panel (31.34-36.37) are graphics, not footage
TM="zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
out=[]; procs=[]
for sid,c,ss,o0,o1 in SEG:
    n0=M(o0); n1=END if o1 is None else M(o1); d=round(n1-n0,3)
    out.append(dict(id=sid,clip=c,start=n0,dur=d))
    cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(d+0.1),'-i',U+F[c]+'.mov','-vf',f"{TM},scale=1080:1920:flags=lanczos,eq=contrast=1.05:saturation=1.08,setsar=1",
         '-an','-c:v','libx264','-preset','slow','-crf','10','-pix_fmt','yuv420p','-r','25','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',f'assets/shots/{sid}.mp4']
    procs.append(subprocess.Popen(cmd))
    if len(procs)>=4:
        for p in procs: p.wait()
        procs=[]
for p in procs: p.wait()
json.dump(out,open('tools/segs.json','w'),indent=1)
for s in out:
    real=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f"assets/shots/{s['id']}.mp4"],capture_output=True,text=True).stdout)
    print(s['id'],s['clip'],s['start'],s['dur'],'file',real, 'SHORT' if real<s['dur'] else '')
print('END',END)
