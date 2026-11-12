# Old VO time -> new time after shortening pauses (each pause kept at 0.14 s)
import subprocess, re
SIL=[(2.062,2.626),(4.202,4.646),(9.058,9.602),(13.517,13.962),(18.619,19.157),(21.704,22.081),(22.825,23.330),(27.078,27.549),(36.162,36.573),(41.151,41.636),(48.445,48.832),(53.501,53.904),(56.832,57.266),(62.636,63.114),(65.869,66.274),(67.894,68.305)]
KEEP=0.14
CUTS=[]  # (start,end) removed in old time
for s,e in SIL:
    if e-s>KEEP: CUTS.append((s+KEEP/2, e-KEEP/2))
def M(t):
    out=t
    for a,b in CUTS:
        if t>=b: out-=(b-a)
        elif t>a: out-=(t-a)
    return round(out,3)
VO_END=68.92; TAIL=1.3
