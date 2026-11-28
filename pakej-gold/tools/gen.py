import json
L=json.load(open('/home/user/test/pakej-gold/assets/img/o_layout.json'))
T0=43.9; OD=5.2; DUR=round(T0+OD,2); Y="#f6c343"
def lay(k):
    x0,y0,x1,y1=L[k]; return f'<img id="o_{k}" class="ol" src="assets/img/o_{k}.png" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px" alt="" />'
def card(id,start,dur,top,title,lines,extra=""):
    li="".join(f'<div class="li">{l}</div>' for l in lines)
    return f'<div id="{id}" class="cardwrap clip" data-start="{start}" data-duration="{dur}" data-track-index="5" style="top:{top}px"><div class="card"><div class="ct">{title}</div>{li}{extra}</div></div>'
cards=[
 card("cDoor",2.5,2.55,330,"PINTU",["<b>Hadapan:</b> Powder-Coated Security Door <span class='y' style='white-space:nowrap'>D-Series</span>","<b>Belakang:</b> Security Door, <span class='y'>1 daun</span>"]),
 card("cWarna",5.15,1.9,330,"PILIHAN WARNA",["<span class='y'>3</span> pilihan warna luar","<span class='y'>3</span> pilihan warna dalam"],'<img class="logos" src="assets/img/paint-logos-cut.png" alt="" />'),
 card("cElec",7.15,4.15,330,"PENDAWAIAN ELEKTRIK",["<span class='big y'>THREE-PHASE</span>"]),
 card("cTamu",11.75,4.95,1080,"RUANG TAMU",["Siling <span class='y'>double layer</span>"],'<svg class="layers" viewBox="0 0 300 70" width="420" height="98"><rect id="ly1" x="10" y="8" width="280" height="18" rx="5" fill="#fff"/><rect id="ly2" x="40" y="40" width="220" height="18" rx="5" fill="'+Y+'"/></svg>'),
 card("cFrame",22.45,5.8,330,"BINGKAI PINTU",["Bilik tidur &amp; bilik air","<span class='y'>Zincalume</span> &bull; tebal <span class='y'>0.75 mm</span>"]),
 card("cSani",28.4,4.55,330,"KELENGKAPAN SANITARI",["Fitting tandas <span class='y'>stainless steel 304</span>","Jenama <span class='y'>MORVAN</span>","Tandas duduk <span class='y'>1-piece</span> atau","tandas cangkung import khas"]),
 card("cDapur",33.1,5.65,330,"RUANG DAPUR",["Backsplash mozek <span class='y'>2 kaki 6 inci</span>","Table top bermozek <span class='y'>12 kaki</span>","Sink <span class='y'>stainless steel 304</span>, dua lubang"]),
]
html=f'''<!doctype html>
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
.y {{ color:{Y}; }}
#hook {{ position:absolute; left:130px; right:150px; top:360px; text-align:center; }}
.hd {{ font-weight:800; line-height:1.05; text-transform:uppercase; white-space:nowrap; -webkit-text-stroke:2px rgba(10,10,15,.6); paint-order:stroke fill; text-shadow:0 4px 18px rgba(0,0,0,.6), 0 2px 6px rgba(0,0,0,.5); }}
.emo {{ -webkit-text-stroke:0; }}
#shade {{ position:absolute; left:0; right:0; top:0; height:900px; background:linear-gradient(180deg,rgba(0,0,0,.4),rgba(0,0,0,0)); }}
.cardwrap {{ position:absolute; left:130px; right:150px; display:flex; justify-content:center; }}
.card {{ background:rgba(12,12,14,.7); border-left:10px solid {Y}; border-radius:24px; padding:24px 32px 26px; max-width:800px; box-shadow:0 10px 30px rgba(0,0,0,.35); }}
.ct {{ font-weight:800; font-size:50px; color:{Y}; letter-spacing:.02em; margin-bottom:8px; }}
.li {{ font-weight:600; font-size:40px; line-height:1.28; color:#fff; }}
.li b {{ font-weight:800; }}
.big {{ font-weight:800; font-size:76px; letter-spacing:.02em; }}
.logos {{ display:block; width:520px; margin:12px auto 0; background:#fff; border-radius:14px; padding:8px 14px; }}
.layers {{ display:block; margin:10px auto 0; }}
#philips {{ position:absolute; left:640px; top:820px; width:290px; filter:drop-shadow(0 8px 18px rgba(0,0,0,.55)); }}
#outro {{ position:absolute; inset:0; overflow:hidden; }}
#outro .bg {{ position:absolute; inset:0; width:1080px; height:1920px; }}
.ol {{ position:absolute; display:block; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<video id="vm" class="v clip" src="assets/v/main.mp4" muted playsinline data-start="0" data-duration="{T0}" data-track-index="0"></video>
<div id="shade" class="clip" data-start="0" data-duration="2.6" data-track-index="2"></div>
<div id="hook" class="clip" data-start="0.05" data-duration="2.4" data-track-index="5">
  <div id="h1" class="hd" style="font-size:52px"><span class="emo">🗣️</span>: BINA RUMAH PILIH</div>
  <div id="h2" class="hd y" style="font-size:96px;margin-top:6px">PAKEJ GOLD</div>
  <div id="h3" class="hd" style="font-size:64px;margin-top:6px">DAPAT APA JE?</div>
</div>
{chr(10).join(cards)}
<img id="philips" class="clip" src="assets/img/philips-cut.png" data-start="2.8" data-duration="2.25" data-track-index="6" alt="" />
<div id="outro" class="clip" data-start="{T0}" data-duration="{OD}" data-track-index="7">
  <img id="obgB" class="bg" src="assets/img/o_blur.jpg" alt="" />
  <img id="obgF" class="bg" src="assets/img/o_full.jpg" alt="" style="opacity:0" />
  {lay("line1")}{lay("card1")}{lay("label1")}{lay("line2")}{lay("card2")}{lay("label2")}{lay("head")}{lay("cta")}{lay("walk")}
</div>
<div id="flash" class="clip" data-start="{round(T0-0.25,2)}" data-duration="0.6" data-track-index="8"></div>
<audio id="mus" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="9"></audio>
''' 
fx=[("pop",0.1),("pop",2.5),("sparkle",2.8),("pop",5.15),("pop",7.15),("pop",11.75),("pop",22.45),("pop",28.4),("pop",33.1),("whoosh",T0-0.3),("pop",T0+0.35),("pop",T0+1.25),("chime",T0+2.3)]
html+="\n".join(f'<audio id="fx{i}" class="clip" src="assets/audio/{n}.mp3" data-start="{round(t,2)}" data-duration="1.0" data-volume="{0.16 if n!="whoosh" else 0.2}" data-track-index="{10+i%3}"></audio>' for i,(n,t) in enumerate(fx))
html+=f'''
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const T0={T0};
tl.fromTo("#h1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},0.08);
tl.fromTo("#h2",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},0.35);
tl.fromTo("#h3",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},0.65);
tl.to("#hook",{{opacity:0,duration:0.2}},2.25); tl.to("#shade",{{opacity:0,duration:0.3}},2.3);
const cardIn=(id,s,d)=>{{tl.fromTo(id+" .card",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},s);tl.to(id+" .card",{{opacity:0,x:40,duration:0.25,ease:"power1.in"}},s+d-0.27);}};
cardIn("#cDoor",2.5,2.55); cardIn("#cWarna",5.15,1.9); cardIn("#cElec",7.15,4.15); cardIn("#cTamu",11.75,4.95); cardIn("#cFrame",22.45,5.8); cardIn("#cSani",28.4,4.55); cardIn("#cDapur",33.1,5.65);
tl.fromTo("#cElec .big",{{opacity:0.3}},{{opacity:1,duration:0.18,yoyo:true,repeat:4}},7.6);
tl.fromTo("#ly1",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3}},12.2); tl.fromTo("#ly2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},12.5);
tl.fromTo("#philips",{{opacity:0,scale:0.4,rotation:-12,transformOrigin:"50% 80%"}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(2.2)"}},2.8);
tl.to("#philips",{{scale:1.06,duration:0.3,yoyo:true,repeat:3,ease:"sine.inOut"}},3.4);
tl.to("#philips",{{opacity:0,scale:0.8,duration:0.25}},4.8);
// outro
tl.fromTo("#flash",{{opacity:0}},{{opacity:0.85,duration:0.25,ease:"power2.in"}},T0-0.25); tl.to("#flash",{{opacity:0,duration:0.35}},T0);
tl.fromTo("#outro",{{scale:1.08}},{{scale:1.0,duration:3.2,ease:"power2.out"}},T0);
tl.to("#obgF",{{opacity:1,duration:2.4,ease:"sine.inOut"}},T0+0.5);
tl.fromTo("#o_card1",{{opacity:0,x:-120,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.5,ease:"power3.out"}},T0+0.3);
tl.fromTo("#o_label1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3}},T0+0.6);
tl.fromTo("#o_line1",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},T0+0.75);
tl.fromTo("#o_card2",{{opacity:0,x:120,scale:0.85}},{{opacity:1,x:0,scale:1,duration:0.5,ease:"power3.out"}},T0+1.2);
tl.fromTo("#o_label2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3}},T0+1.5);
tl.fromTo("#o_line2",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},T0+1.65);
tl.fromTo("#o_head",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},T0+2.05);
tl.fromTo("#o_cta",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.35,ease:"back.out(2)"}},T0+2.35);
tl.fromTo("#o_walk",{{opacity:0,y:25}},{{opacity:1,y:0,duration:0.3}},T0+2.6);
window.__timelines["main"] = tl;
</script>
</body>
</html>'''
open('/home/user/test/pakej-gold/index.html','w').write(html); print("ok",DUR)
