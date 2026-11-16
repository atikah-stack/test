# Generates index.html for the pelapik lantai explainer.
import json
DUR=52.8
Y="#f6c343"
shots=[ # start,end,file,mediaStart,scaleFrom,scaleTo,origin
 (0.00,1.95,"img_8976_c",0.0,1.45,1.36,"62% 96%"),
 (1.95,3.90,"img_8978f",0.0,1.0,1.08,"50% 50%"),
 (3.90,6.40,"img_7205e",0.0,1.0,1.05,"50% 60%"),
 (6.40,9.20,"img_7206e",0.0,1.0,1.05,"50% 60%"),
 (9.20,10.45,"img_7207e",0.8,1.05,1.12,"50% 55%"),
 (10.45,11.72,"img_7205e",4.6,1.05,1.12,"50% 60%"),
 (11.72,12.90,"img_7206e",4.2,1.05,1.12,"50% 60%"),
 (12.90,18.00,"img_7207e",2.0,1.1,1.15,"50% 50%"),   # bg for illustration
 (22.15,25.20,"img_8976_c",0.3,1.0,1.06,"50% 55%"),
 (25.20,28.40,"img_8978f",3.0,1.0,1.06,"50% 50%"),
 (28.40,31.60,"img_7207e",4.0,1.0,1.05,"50% 60%"),
 (31.60,35.10,"img_7206e",5.0,1.0,1.05,"50% 60%"),
 (35.10,37.60,"img_8977",0.0,1.0,1.06,"50% 50%"),
 (37.60,40.10,"img_7205e",6.5,1.0,1.05,"50% 60%"),
 (40.10,45.30,"img_8978f",1.0,1.1,1.15,"50% 50%"),  # bg for illustration
 (45.30,48.30,"img_7206e",2.5,1.0,1.05,"50% 60%"),
 (48.30,52.80,"img_7207e",5.8,1.0,1.06,"50% 60%"),
]
dimbg={7:0.62,14:0.62}   # shot index -> dark overlay strength (illustration backgrounds)
subs=[
 (0.09,1.95,"Lantai dah siap cantik…",[]),
 (2.04,3.90,"kenapa ada orang tutup balik?",["tutup balik?"]),
 (3.95,6.35,"Sebab kerja rumah belum habis,",["belum habis,"]),
 (6.44,9.15,"lantai masih berisiko tercalar!",["berisiko tercalar!"]),
 (9.28,10.45,"Pekerja keluar masuk,",["keluar masuk,"]),
 (10.49,11.72,"pasang kabinet,",["kabinet,"]),
 (11.76,12.90,"angkut barang…",["angkut barang…"]),
 (12.94,14.98,"pasir halus bawah kasut",["pasir halus"]),
 (15.01,15.90,"pun boleh bergesel",["bergesel"]),
 (15.94,17.95,"dan tinggalkan kesan pada lantai.",["kesan"]),
 (18.02,20.92,"Belum sempat masuk rumah, dah bercalar.",["dah bercalar."]),
 (21.00,22.12,"Sayang kan?",["Sayang"]),
 (22.18,25.15,"Sebab tu ada pelapik perlindungan lantai!",["pelapik perlindungan lantai!"]),
 (25.23,27.52,"Pelapik ni dibentangkan atas lantai",["dibentangkan"]),
 (27.58,30.45,"untuk membantu melindungi permukaannya",["melindungi"]),
 (30.51,33.18,"daripada calar sepanjang kerja pembinaan",["calar"]),
 (33.21,35.05,"atau pengubahsuaian.",["pengubahsuaian."]),
 (35.16,36.12,"Bukan mozek je,",["mozek"]),
 (36.18,39.95,"SPC dan vinyl pun perlukan perlindungan.",["SPC","vinyl"]),
 (40.16,42.45,"Sebelum bentang, bersihkan lantai dulu",["bersihkan lantai dulu"]),
 (42.50,45.25,"supaya pasir tak terperangkap di bawahnya!",["pasir","terperangkap"]),
 (45.34,46.98,"Korang pernah nampak kontraktor",["kontraktor"]),
 (47.02,48.25,"guna pelapik macam ni?",["pelapik"]),
 (48.30,50.25,"Atau baru tahu hari ni?",["baru tahu"]),
 (50.30,52.80,"Komen sikit!",["Komen"]),
]
def hl(t,keys):
    for k in keys: t=t.replace(k,f'<span class="y">{k}</span>',1)
    return t
sfx=[("whoosh-short",t,0.16) for t in [1.95,3.90,9.20,10.45,11.72,12.90,18.00,22.15,25.20,35.10,40.10,45.30]]
sfx+=[("whoosh",1.95,0.12),("whoosh",22.15,0.14),("whoosh",25.20,0.10)]
sfx+=[("pop",t,0.2) for t in [0.15,6.40,22.30,35.25,35.55,35.85,40.25,47.0]]
sfx+=[("pop",t,0.14) for t in [13.6,14.5,16.2]]
sfx+=[("sparkle",27.65,0.14),("notification",47.15,0.16),("click-soft",18.6,0.18),("click-soft",19.4,0.18)]

V=[]
for i,(s,e,f,ms,a,b,o) in enumerate(shots):
    V.append(f'<video id="v{i}" class="v clip" src="assets/censored/{f}.mp4" muted playsinline data-start="{s}" data-duration="{round(e-s,2)}" data-media-start="{ms}" data-track-index="0" style="transform-origin:{o}"></video>')
    if i in dimbg:
        V.append(f'<div id="dim{i}" class="dim clip" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="1" style="opacity:{dimbg[i]}"></div>')
A=[f'<audio id="vo" class="clip" src="assets/audio/vo-aisyah.mp3" data-start="0" data-duration="51.56" data-volume="1" data-track-index="8"></audio>']
for j,(n,t,v) in enumerate(sfx):
    A.append(f'<audio id="fx{j}" class="clip" src="assets/audio/{n}.mp3" data-start="{t}" data-duration="1.2" data-volume="{v}" data-track-index="{9+j%3}"></audio>')
S=[]
for k,(s,e,t,keys) in enumerate(subs):
    S.append(f'<div id="s{k}" class="sub clip" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="6"><span class="cb">{hl(t,keys)}</span></div>')

ILU='<div class="ilu">ILUSTRASI</div>'
G=f'''
<div id="hook" class="t clip" data-start="0.1" data-duration="3.78" data-track-index="5" style="top:560px">
  <div id="h1" class="hd" style="font-size:76px">LANTAI DAH CANTIK…</div>
  <div id="h2" class="hd y" style="font-size:96px;margin-top:6px">KENAPA TUTUP BALIK?</div>
</div>
<div id="risk" class="t clip" data-start="6.4" data-duration="2.75" data-track-index="5" style="top:560px">
  <div id="riskIn" class="pillrow"><svg class="ic" viewBox="0 0 24 24"><path d="M12 2 1 21h22L12 2z" fill="{Y}"/><rect x="11" y="8" width="2" height="7" fill="#111"/><rect x="11" y="16.5" width="2" height="2" fill="#111"/></svg><span class="hd" style="font-size:54px;white-space:nowrap">RISIKO CALAR <span class="y">MASIH ADA!</span></span></div>
</div>

<!-- Scene 3 illustration: sand under shoe -->
<div id="sand" class="panel clip" data-start="12.9" data-duration="5.1" data-track-index="5">
  {ILU}
  <svg viewBox="0 0 900 620" width="900" height="620">
    <defs><linearGradient id="wood" x1="0" x2="1"><stop offset="0" stop-color="#c99a63"/><stop offset="1" stop-color="#b8844e"/></linearGradient></defs>
    <rect x="0" y="420" width="900" height="200" rx="14" fill="url(#wood)"/>
    <g stroke="#a87442" stroke-width="3"><line x1="0" y1="490" x2="900" y2="490"/><line x1="0" y1="560" x2="900" y2="560"/><line x1="300" y1="420" x2="300" y2="490"/><line x1="650" y1="490" x2="650" y2="560"/></g>
    <g id="scr" stroke="#fff6e6" stroke-width="3" stroke-linecap="round" opacity="0.9">
      <path id="sc1" d="M180 455 L420 447" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      <path id="sc2" d="M200 470 L470 460" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
    </g>
    <g id="shoe">
      <path d="M330 300 q-40 0 -60 40 l-20 60 q-4 20 20 20 h300 q40 0 40 -30 q0 -30 -60 -40 l-60 -20 q-20 -40 -60 -40 z" fill="#3b3f46"/>
      <rect x="250" y="410" width="350" height="14" rx="7" fill="#22252a"/>
      <g id="grains" fill="#e9d3a2">
        <circle cx="290" cy="428" r="7"/><circle cx="330" cy="430" r="5"/><circle cx="380" cy="428" r="6"/><circle cx="440" cy="430" r="5"/><circle cx="500" cy="428" r="7"/><circle cx="555" cy="430" r="5"/>
      </g>
    </g>
    <g id="arrSand"><path d="M720 250 Q640 330 600 405" stroke="{Y}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M588 392 l10 20 l18 -14" stroke="{Y}" stroke-width="8" fill="none" stroke-linecap="round"/>
      <text x="610" y="235" fill="#fff" font-family="Montserrat" font-weight="800" font-size="40">PASIR HALUS</text></g>
    <g id="ringRub"><ellipse cx="300" cy="455" rx="140" ry="48" fill="none" stroke="{Y}" stroke-width="7"/>
      <text x="40" y="380" fill="{Y}" font-family="Montserrat" font-weight="800" font-size="40">GESERAN</text></g>
  </svg>
</div>

<!-- Scene 4 illustration: scratches -->
<div id="scratch" class="clip" data-start="18.0" data-duration="4.15" data-track-index="0" style="position:absolute;inset:0;background:linear-gradient(180deg,#2a2018,#120d09)"></div>
<div id="scratchP" class="panel clip" data-start="18.0" data-duration="4.15" data-track-index="5">
  {ILU}
  <svg viewBox="0 0 900 620" width="900" height="620">
    <defs><linearGradient id="wood2" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#d7ab74"/><stop offset="1" stop-color="#b98450"/></linearGradient></defs>
    <rect x="40" y="40" width="820" height="540" rx="18" fill="url(#wood2)"/>
    <g stroke="#a3713f" stroke-width="3"><line x1="40" y1="175" x2="860" y2="175"/><line x1="40" y1="310" x2="860" y2="310"/><line x1="40" y1="445" x2="860" y2="445"/><line x1="330" y1="40" x2="330" y2="175"/><line x1="610" y1="175" x2="610" y2="310"/><line x1="250" y1="310" x2="250" y2="445"/><line x1="700" y1="445" x2="700" y2="580"/></g>
    <g stroke="#fff4e0" stroke-width="4" stroke-linecap="round" fill="none">
      <path class="sk" d="M140 120 L520 230" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      <path class="sk" d="M180 150 L470 240" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      <path class="sk" d="M520 360 L790 300" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      <path class="sk" d="M300 500 Q450 470 640 520" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
    </g>
    <circle id="ringSc" cx="330" cy="180" r="150" fill="none" stroke="{Y}" stroke-width="8"/>
  </svg>
</div>
<div id="belum" class="t clip" data-start="18.15" data-duration="4.0" data-track-index="7" style="top:330px">
  <div class="hd" style="font-size:64px">BELUM MASUK,</div><div class="hd y" style="font-size:76px">DAH BERCALAR?</div>
</div>

<div id="intro" class="t clip" data-start="22.3" data-duration="2.85" data-track-index="5" style="top:560px">
  <div class="hd" style="font-size:62px">PELAPIK</div><div class="hd y" style="font-size:74px">PERLINDUNGAN LANTAI</div>
</div>

<div id="shield" class="t clip" data-start="27.6" data-duration="3.0" data-track-index="5" style="top:520px">
  <svg id="shieldIc" viewBox="0 0 120 140" width="170" height="198" style="display:block;margin:0 auto"><path d="M60 6 L110 24 V66 C110 102 88 124 60 134 C32 124 10 102 10 66 V24 Z" fill="{Y}" stroke="#fff" stroke-width="6"/><path d="M36 70 l16 16 l32 -34" stroke="#1c1c1c" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="hd" style="font-size:52px;margin-top:14px">BANTU <span class="y">LINDUNGI</span> LANTAI</div>
</div>

<div id="types" class="t clip" data-start="35.2" data-duration="4.75" data-track-index="5" style="top:560px">
  <div class="chips"><span id="c1" class="chip">MOZEK</span><span id="c2" class="chip">SPC</span><span id="c3" class="chip">VINYL</span></div>
</div>

<!-- Scene 8 illustration: clean first -->
<div id="clean" class="panel clip" data-start="40.1" data-duration="5.2" data-track-index="5">
  {ILU}
  <svg viewBox="0 0 900 620" width="900" height="620">
    <defs><linearGradient id="wood3" x1="0" x2="1"><stop offset="0" stop-color="#c99a63"/><stop offset="1" stop-color="#b8844e"/></linearGradient></defs>
    <rect x="0" y="430" width="900" height="190" rx="14" fill="url(#wood3)"/>
    <g id="sandC" fill="#efd9a8"><circle cx="200" cy="420" r="8"/><circle cx="260" cy="424" r="6"/><circle cx="330" cy="421" r="7"/><circle cx="420" cy="424" r="6"/><circle cx="510" cy="420" r="8"/><circle cx="600" cy="424" r="6"/><circle cx="680" cy="421" r="7"/></g>
    <g id="broom"><rect x="560" y="80" width="18" height="300" rx="9" fill="#8b5a2b" transform="rotate(25 569 230)"/><path d="M470 360 h170 l30 70 h-230 z" fill="{Y}"/><g stroke="#9c7a1e" stroke-width="4"><line x1="480" y1="370" x2="460" y2="428"/><line x1="530" y1="370" x2="520" y2="428"/><line x1="580" y1="370" x2="580" y2="428"/><line x1="630" y1="370" x2="640" y2="428"/></g></g>
    <rect id="matL" x="0" y="400" width="900" height="30" rx="6" fill="#e2672c"/>
    <g id="okTick"><circle cx="790" cy="230" r="58" fill="#2fbf71"/><path d="M762 232 l20 20 l36 -40" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
  </svg>
</div>
<div id="cleanT" class="t clip" data-start="40.2" data-duration="5.05" data-track-index="7" style="top:330px">
  <div class="hd" style="font-size:66px">BERSIHKAN</div><div class="hd y" style="font-size:66px">LANTAI DULU!</div>
</div>

<div id="cta" class="t clip" data-start="47.0" data-duration="5.8" data-track-index="5" style="top:520px">
  <svg id="bubble" viewBox="0 0 120 110" width="150" height="138" style="display:block;margin:0 auto 10px"><path d="M14 10 h92 a10 10 0 0 1 10 10 v52 a10 10 0 0 1 -10 10 h-52 l-26 22 v-22 h-14 a10 10 0 0 1 -10 -10 v-52 a10 10 0 0 1 10 -10 z" fill="#fff"/><circle cx="38" cy="46" r="7" fill="#1b1b1b"/><circle cx="60" cy="46" r="7" fill="#1b1b1b"/><circle cx="82" cy="46" r="7" fill="#1b1b1b"/></svg>
  <div class="hd" style="font-size:78px">PERNAH NAMPAK</div><div class="hd" style="font-size:52px;margin:4px 0">ATAU</div><div class="hd y" style="font-size:92px">BARU TAHU?</div>
</div>
'''
JS=f'''
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const shots={json.dumps([[f"#v{i}",s,round(e-s,2),a,b] for i,(s,e,f,ms,a,b,o) in enumerate(shots)])};
shots.forEach(([id,s,d,a,b])=>tl.fromTo(id,{{scale:a}},{{scale:b,duration:d,ease:"none"}},s));
// hook
tl.fromTo("#h1",{{opacity:0,y:30,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2)"}},0.12);
tl.fromTo("#h2",{{opacity:0,y:30,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2)"}},2.0);
tl.set("#h2",{{opacity:0}},0.0);
const popIn=(sel,t)=>tl.fromTo(sel,{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},t);
popIn("#riskIn",6.42); popIn("#intro",22.32); popIn("#belum",18.17); popIn("#cleanT",40.22);
// sand illustration
tl.fromTo("#sand",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},12.92);
tl.fromTo("#shoe",{{x:-120}},{{x:140,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:2}},13.2);
tl.fromTo("#arrSand",{{opacity:0}},{{opacity:1,duration:0.3}},13.6);
tl.fromTo("#ringRub",{{opacity:0,scale:0.6,transformOrigin:"300px 455px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},15.1);
tl.to("#sc1",{{strokeDashoffset:0,duration:0.8}},15.3); tl.to("#sc2",{{strokeDashoffset:0,duration:0.8}},16.2);
// scratch illustration
tl.fromTo("#scratchP",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35}},18.02);
document.querySelectorAll(".sk").forEach((el,i)=>tl.to(el,{{strokeDashoffset:0,duration:0.45,ease:"power1.in"}},18.5+i*0.32));
tl.fromTo("#ringSc",{{opacity:0,scale:0.5,transformOrigin:"330px 180px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},20.95);
// shield
tl.fromTo("#shieldIc",{{opacity:0,scale:0.3,rotation:-15}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(2.4)"}},27.62);
tl.fromTo("#shield .hd",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},27.9);
// types
["#c1","#c2","#c3"].forEach((c,i)=>popIn(c,35.25+i*0.3));
// clean illustration
tl.fromTo("#clean",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35}},40.12);
tl.set("#matL",{{x:-900}},40.1); tl.set("#okTick",{{opacity:0}},40.1);
tl.fromTo("#broom",{{x:-380}},{{x:260,duration:1.9,ease:"sine.inOut"}},40.4);
tl.to("#sandC circle",{{x:520,opacity:0,duration:1.7,stagger:0.08,ease:"power1.in"}},40.5);
tl.to("#broom",{{opacity:0,duration:0.3}},42.4);
tl.to("#matL",{{x:0,duration:0.9,ease:"power2.out"}},42.6);
tl.fromTo("#okTick",{{opacity:0,scale:0.4,transformOrigin:"790px 230px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},43.6);
// CTA
tl.fromTo("#cta",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.8)"}},47.0);
tl.fromTo("#bubble",{{y:0}},{{y:-14,duration:0.5,yoyo:true,repeat:7,ease:"sine.inOut"}},47.4);
// subtitles pop
document.querySelectorAll(".sub").forEach(el=>{{const s=parseFloat(el.dataset.start); tl.fromTo(el.querySelector(".cb"),{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},s);}});
window.__timelines["main"] = tl;
'''
HTML=f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ width:100%; height:100%; background:#000; font-family:"Montserrat",sans-serif; color:#fff; }}
.v {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
.dim {{ position:absolute; inset:0; background:#0b0b0b; }}
.y {{ color:{Y}; }}
.t {{ position:absolute; left:60px; right:60px; text-align:center; }}
.hd {{ font-weight:800; line-height:1.03; letter-spacing:-0.01em; text-transform:uppercase; text-shadow:0 4px 18px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.45); }}
.pillrow {{ display:inline-flex; align-items:center; gap:18px; background:rgba(0,0,0,.55); padding:16px 28px; border-radius:22px; }}
.ic {{ width:70px; height:70px; }}
.panel {{ position:absolute; left:90px; top:560px; width:900px; height:620px; }}
.ilu {{ position:absolute; right:6px; top:-50px; background:rgba(0,0,0,.6); color:#fff; font-weight:700; font-size:24px; letter-spacing:.12em; padding:6px 14px; border-radius:10px; border:2px solid rgba(255,255,255,.5); }}
.chips {{ display:flex; justify-content:center; gap:22px; }}
.chip {{ font-weight:800; font-size:64px; color:#1a1a1a; background:{Y}; padding:14px 28px; border-radius:20px; box-shadow:0 8px 22px rgba(0,0,0,.35); }}
.sub {{ position:absolute; left:50px; right:50px; top:1300px; text-align:center; }}
.cb {{ display:inline-block; max-width:960px; padding:12px 26px 14px; border-radius:16px; background:rgba(0,0,0,.62); font-weight:700; font-size:46px; line-height:1.22; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(V)}
{G}
{chr(10).join(S)}
{chr(10).join(A)}
</div>
<script>
{JS}
</script>
</body>
</html>'''
open("/home/user/test/pelapik-lantai/index.html","w").write(HTML)
print("ok")
