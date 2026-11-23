DUR=25.7; Y="#f6c343"
punch=[(0,4.77,1.0,1.04,"50% 45%"),(4.77,6.99,1.14,1.17,"50% 62%"),(6.99,10.93,1.0,1.03,"50% 50%"),
       (10.93,15.0,1.12,1.15,"50% 58%"),(15.0,21.45,1.0,1.03,"50% 50%"),(21.45,DUR,1.14,1.18,"50% 60%")]
subs=[(0.01,1.19,'Dengan bajet bawah'),(1.21,2.98,'<span class="y">RM280,000,</span>'),
 (3.03,4.75,'<span class="y">banglo</span> macam ni yang anda boleh dapat.'),
 (4.80,6.97,'Ok, assalamualaikum dan salam sejahtera.'),(7.04,8.56,'Ok, hari ni Abang Mi berada'),
 (8.60,10.92,'di Kampung Ceralali, Tanah Merah, Kelantan.'),(10.96,12.42,'Bawa anda semua view'),
 (12.45,14.98,'sebuah <span class="y">banglo</span> yang dibina oleh Mahligai Idaman.'),
 (15.05,16.95,'Di <span class="y">banglo</span> ni berkeluasan'),(16.99,18.92,'1,520 kaki persegi,'),
 (18.96,21.45,'ada 4 bilik tidur, 3 bilik air.'),(21.50,24.08,'Abang Mi nak bawa anda view dari rumah ni.'),
 (24.12,DUR,'Jom, <span class="y">LACAR!!!</span>')]
S="\n".join(f'<div id="s{i}" class="sub clip" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="6"><span class="cb">{t}</span></div>' for i,(a,b,t) in enumerate(subs))
V="\n".join(f'<video id="v{i}" class="v clip" src="assets/v/main.mp4" muted playsinline data-start="{a}" data-duration="{round(b-a,2)}" data-media-start="{a}" data-track-index="0" style="transform-origin:{o}"></video>' for i,(a,b,s0,s1,o) in enumerate(punch))
TAG=f'<svg class="ic" viewBox="0 0 64 64"><path d="M6 30 L30 6 H56 V32 L32 56 Z" fill="{Y}" stroke="#fff" stroke-width="3"/><circle cx="45" cy="17" r="5" fill="#222"/></svg>'
KEY=f'<svg id="key" class="ic" viewBox="0 0 64 64"><circle cx="20" cy="32" r="13" fill="none" stroke="{Y}" stroke-width="7"/><path d="M32 32 H58 M50 32 V42 M42 32 V39" stroke="{Y}" stroke-width="7" stroke-linecap="round"/></svg>'
PIN=f'<svg class="ic2" viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z" fill="{Y}"/><circle cx="12" cy="9" r="2.6" fill="#1a1a1a"/></svg>'
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
.hd {{ font-weight:800; line-height:1.03; letter-spacing:-0.01em; text-transform:uppercase; text-align:center; white-space:nowrap;
  -webkit-text-stroke:2px rgba(15,15,20,.55); paint-order:stroke fill; text-shadow:0 4px 18px rgba(0,0,0,.5), 0 2px 5px rgba(0,0,0,.45); }}
#hook {{ position:absolute; left:100px; right:100px; top:320px; }}
.row {{ display:flex; align-items:center; justify-content:center; gap:16px; }}
.ic {{ width:76px; height:76px; flex:none; filter:drop-shadow(0 3px 6px rgba(0,0,0,.45)); }}
.ic2 {{ width:46px; height:46px; flex:none; }}
#swoosh {{ display:block; margin:6px auto 0; }}
#shade {{ position:absolute; left:0; right:0; top:0; height:820px; background:linear-gradient(180deg,rgba(0,0,0,.38),rgba(0,0,0,0)); }}
.chipwrap {{ position:absolute; left:40px; right:40px; top:420px; display:flex; justify-content:center; gap:16px; flex-wrap:wrap; }}
.chip {{ display:inline-flex; align-items:center; gap:12px; font-weight:800; font-size:44px; padding:12px 24px; border-radius:18px; background:rgba(0,0,0,.6); border:3px solid {Y}; text-transform:uppercase; white-space:nowrap; }}
.chip.yb {{ background:{Y}; color:#141414; border-color:{Y}; }}
.sub {{ position:absolute; left:60px; right:60px; top:1290px; text-align:center; }}
.cb {{ display:inline-block; max-width:940px; padding:12px 26px 14px; border-radius:16px; background:rgba(0,0,0,.58); font-weight:700; font-size:46px; line-height:1.22; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{V}
<div id="shade" class="clip" data-start="0" data-duration="7.2" data-track-index="2"></div>
<div id="hook" class="clip" data-start="0.05" data-duration="6.95" data-track-index="5">
  <div id="h1" class="row"><div class="hd" style="font-size:80px">BAJET <span class="y">RM280,000,</span></div></div>
  <div id="h2" class="row" style="margin-top:12px"><div class="hd" style="font-size:58px">BOLEH BAWA BALIK KUNCI</div></div>
  <div id="h3" class="hd y" style="font-size:86px;margin-top:8px">BANGLO SENDIRI?</div>
</div>
<div id="loc" class="chipwrap clip" data-start="8.6" data-duration="2.35" data-track-index="5"><span class="chip">TANAH MERAH, KELANTAN</span></div>
<div id="by" class="chipwrap clip" data-start="13.0" data-duration="2.0" data-track-index="5"><span class="chip yb">DIBINA OLEH MAHLIGAI IDAMAN</span></div>
<div id="spec" class="chipwrap clip" data-start="16.95" data-duration="4.5" data-track-index="5" style="top:400px">
  <span id="c1" class="chip">1,520 KPS</span><span id="c2" class="chip">4 BILIK TIDUR</span><span id="c3" class="chip">3 BILIK AIR</span>
</div>
<audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="8"></audio>
<audio id="fx0" class="clip" src="assets/audio/pop.mp3" data-start="0.1" data-duration="0.8" data-volume="0.16" data-track-index="9"></audio>
<audio id="fx1" class="clip" src="assets/audio/chime.mp3" data-start="0.75" data-duration="1.0" data-volume="0.14" data-track-index="10"></audio>
<audio id="fx2" class="clip" src="assets/audio/whoosh-short.mp3" data-start="4.72" data-duration="0.8" data-volume="0.12" data-track-index="9"></audio>
<audio id="fx3" class="clip" src="assets/audio/pop.mp3" data-start="8.6" data-duration="0.8" data-volume="0.14" data-track-index="10"></audio>
<audio id="fx4" class="clip" src="assets/audio/whoosh-short.mp3" data-start="10.9" data-duration="0.8" data-volume="0.12" data-track-index="9"></audio>
<audio id="fx5" class="clip" src="assets/audio/pop.mp3" data-start="13.0" data-duration="0.8" data-volume="0.14" data-track-index="10"></audio>
<audio id="fx6" class="clip" src="assets/audio/pop.mp3" data-start="16.95" data-duration="0.8" data-volume="0.14" data-track-index="9"></audio>
<audio id="fx7" class="clip" src="assets/audio/pop.mp3" data-start="19.0" data-duration="0.8" data-volume="0.14" data-track-index="10"></audio>
<audio id="fx8" class="clip" src="assets/audio/pop.mp3" data-start="20.3" data-duration="0.8" data-volume="0.14" data-track-index="9"></audio>
<audio id="fx9" class="clip" src="assets/audio/whoosh-short.mp3" data-start="21.42" data-duration="0.8" data-volume="0.12" data-track-index="10"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const P={[[f"#v{i}",a,round(b-a,2),s0,s1] for i,(a,b,s0,s1,o) in enumerate(punch)]};
P.forEach(([id,s,d,a,b])=>tl.fromTo(id,{{scale:a}},{{scale:b,duration:d,ease:"none"}},s));
tl.fromTo("#h1",{{opacity:0,y:40,scale:0.85}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2)"}},0.08);
tl.fromTo("#h2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},0.45);
tl.fromTo("#h3",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},0.75);
tl.to("#h1 .y",{{scale:1.08,duration:0.18,yoyo:true,repeat:1,transformOrigin:"50% 50%",display:"inline-block"}},1.3);
tl.to("#hook",{{opacity:0,y:-20,duration:0.3,ease:"power1.in"}},6.7);
tl.to("#shade",{{opacity:0,duration:0.4}},6.8);
const pop=(sel,t)=>tl.fromTo(sel,{{opacity:0,scale:0.6,y:20}},{{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(2.2)"}},t);
pop("#loc .chip",8.62); pop("#by .chip",13.02); pop("#c1",16.97); pop("#c2",19.0); pop("#c3",20.32);
document.querySelectorAll(".sub").forEach(el=>{{const s=parseFloat(el.dataset.start); tl.fromTo(el.querySelector(".cb"),{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.12}},s);}});
window.__timelines["main"] = tl;
</script>
</body>
</html>'''
open("/home/user/test/rm280-banglo/index.html","w").write(html); print("ok")
