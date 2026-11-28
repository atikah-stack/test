import json
L=json.load(open('/home/user/test/cikgu-lppsa/assets/img/o_layout.json'))
T0=19.16; OD=4.0; DUR=round(T0+OD,2); Y="#f6c343"
def lay(k):
    x0,y0,x1,y1=L[k]; return f'<img id="o_{k}" class="ol" src="assets/img/o_{k}.png" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px" alt="" />'
cx0,cy0,cx1,cy1=95,1446,985,1568
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
#sindir {{ position:absolute; left:130px; right:150px; top:480px; text-align:center; font-weight:600; font-size:52px; line-height:1.22; color:#fff;
  -webkit-text-stroke:7px #000; paint-order:stroke fill; }}
#head {{ position:absolute; left:130px; right:150px; top:430px; text-align:center; }}
.hd {{ font-weight:800; line-height:1.05; letter-spacing:-0.01em; text-transform:uppercase; white-space:nowrap; text-shadow:0 4px 18px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.45); }}
#shade {{ position:absolute; left:0; right:0; top:0; height:900px; background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,0)); }}
#outro {{ position:absolute; inset:0; overflow:hidden; background:#000; }}
#obgB {{ position:absolute; inset:0; width:1080px; height:1920px; }}
#ostage {{ position:absolute; inset:0; transform-origin:50% 50%; }}
#ostage img.bg {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
.ol {{ position:absolute; display:block; }}
#ctaGlow {{ position:absolute; left:{cx0}px; top:{cy0}px; width:{cx1-cx0}px; height:{cy1-cy0}px; border-radius:46px; overflow:hidden; box-shadow:0 0 0 0 rgba(255,215,90,0); }}
#shine {{ position:absolute; top:-20px; left:-260px; width:170px; height:170px; background:linear-gradient(100deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.75) 50%,rgba(255,255,255,0) 100%); transform:skewX(-20deg); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <video id="vh" class="v clip" src="assets/v/house.mp4" muted playsinline data-start="0" data-duration="{T0}" data-track-index="0"></video>
  <div id="shade" class="clip" data-start="3.6" data-duration="4.45" data-track-index="2"></div>
  <div id="sindir" class="clip" data-start="0.25" data-duration="3.05" data-track-index="5">Rumah cikgu mesti tak ada taste.</div>
  <div id="head" class="clip" data-start="3.7" data-duration="4.25" data-track-index="5">
    <div id="l1" class="hd" style="font-size:48px">INI RUMAH <span class="y">ENGLISH STYLE,</span></div>
    <div id="l2" class="hd" style="font-size:46px;margin-top:8px">DIBINA OLEH SEORANG</div>
    <div id="l3" class="hd" style="font-size:46px;margin-top:8px">CIKGU KELANTAN</div>
    <div id="l4" class="hd" style="font-size:64px;margin-top:8px">GUNA <span class="y">LPPSA.</span></div>
  </div>
  <div id="outro" class="clip" data-start="{T0}" data-duration="{OD}" data-track-index="7">
    <img id="obgB" src="assets/img/o_blur.jpg" alt="" />
    <div id="ostage">
      <img class="bg" src="assets/img/o_base_nopins.jpg" alt="" />
      {lay("line1")}{lay("line2")}
      <div id="ctaGlow"><div id="shine"></div></div>
    </div>
  </div>
  <audio id="mus" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="9"></audio>
  <audio id="fx0" class="clip" src="assets/audio/pop.mp3" data-start="0.25" data-duration="0.8" data-volume="0.14" data-track-index="10"></audio>
  <audio id="fx1" class="clip" src="assets/audio/whoosh-short.mp3" data-start="3.65" data-duration="0.8" data-volume="0.14" data-track-index="11"></audio>
  <audio id="fx2" class="clip" src="assets/audio/whoosh-short.mp3" data-start="{T0-0.05}" data-duration="0.8" data-volume="0.14" data-track-index="10"></audio>
  <audio id="fx3" class="clip" src="assets/audio/pop.mp3" data-start="{T0+0.55}" data-duration="0.8" data-volume="0.16" data-track-index="11"></audio>
  <audio id="fx4" class="clip" src="assets/audio/pop.mp3" data-start="{T0+1.05}" data-duration="0.8" data-volume="0.16" data-track-index="10"></audio>
  <audio id="fx5" class="clip" src="assets/audio/sparkle.mp3" data-start="{T0+1.6}" data-duration="1.0" data-volume="0.14" data-track-index="11"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const T0={T0};
// sindiran: in, hold, fully out before heading
tl.fromTo("#sindir",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},0.25);
tl.to("#sindir",{{opacity:0,duration:0.3,ease:"power1.in"}},3.0);
// heading lines
["#l1","#l2","#l3","#l4"].forEach((id,i)=>tl.fromTo(id,{{opacity:0,y:34,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.32,ease:"back.out(2)"}},3.75+i*0.28));
tl.to("#l4 .y, #l1 .y",{{scale:1.06,duration:0.2,yoyo:true,repeat:1,display:"inline-block",transformOrigin:"50% 50%"}},5.2);
tl.to("#head",{{opacity:0,y:-16,duration:0.3,ease:"power1.in"}},7.6);
tl.fromTo("#shade",{{opacity:0}},{{opacity:1,duration:0.3}},3.6); tl.to("#shade",{{opacity:0,duration:0.4}},7.6);
// outro
tl.fromTo("#outro",{{opacity:0}},{{opacity:1,duration:0.3,ease:"power1.out"}},T0);
tl.fromTo("#ostage",{{scale:0.9}},{{scale:1.0,duration:2.6,ease:"power2.out"}},T0);
tl.fromTo("#o_line1",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.45,ease:"bounce.out"}},T0+0.5);
tl.fromTo("#o_line2",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.45,ease:"bounce.out"}},T0+1.0);
tl.fromTo("#ctaGlow",{{boxShadow:"0 0 0px 0px rgba(255,215,90,0)"}},{{boxShadow:"0 0 46px 14px rgba(255,215,90,.75)",duration:0.35,yoyo:true,repeat:1,ease:"sine.inOut"}},T0+1.55);
tl.fromTo("#shine",{{x:0}},{{x:1260,duration:0.7,ease:"power1.inOut"}},T0+1.6);
tl.set("#shine",{{opacity:0}},T0+2.35);
window.__timelines["main"] = tl;
</script>
</body>
</html>'''
open('/home/user/test/cikgu-lppsa/index.html','w').write(html); print("ok",DUR)
