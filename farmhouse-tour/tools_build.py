import json
END=73.0
# id, clip, media offset, start, end, zoom(0=static)
S=[('s01','IMG_1713',0.0,0.0,4.88,0.05),('s02','IMG_1710',0.0,4.88,8.26,0.03),
   ('t1','IMG_1707',9.0,8.26,9.2,0.02),('t2','IMG_1690',4.0,9.2,10.2,0.02),('t3','IMG_1703',6.5,10.2,11.2,0.02),('t4','IMG_1715',7.5,11.2,12.18,0.02),
   ('f1a','IMG_1718',0.0,12.18,14.6,0.03),('f1b','IMG_1709',0.3,14.6,18.94,0.0),('f1c','IMG_1707',0.0,18.94,21.84,0.03),
   ('f2a','IMG_1690',0.0,21.84,24.0,0.04),('f2b','IMG_1691',0.0,24.0,28.78,0.05),('f2c','IMG_1714',0.0,28.78,32.74,0.05),('f2d','IMG_1712',0.0,32.74,36.44,0.03),
   ('f3a','IMG_1698',0.0,36.44,39.96,0.03),('f3b','IMG_1694',0.0,39.96,43.2,0.03),('f3c','IMG_1703',0.0,43.2,46.2,0.03),('f3d','IMG_1700',0.0,46.2,48.86,0.03),
   ('f4a','IMG_1715',0.0,48.86,52.7,0.03),('f4b','IMG_1690',2.4,52.7,55.0,0.03),('f4c','IMG_1712',3.0,55.0,58.42,0.03),
   ('r1','IMG_1718',3.8,58.42,60.04,0.02),('r2','IMG_1691',4.85,60.04,61.46,0.02),('r3','IMG_1694',3.3,61.46,62.62,0.02),('r4','IMG_1713',5.0,62.62,63.82,0.02),
   ('h','IMG_1686',0.0,63.82,66.94,0.03),('cta','IMG_1710',3.5,66.94,END,0.03)]
r=lambda x: round(x,3)
vids=[];cams=[]
for i,(sid,c,off,a,b,z) in enumerate(S):
    vids.append(f'      <div id="cam-{sid}" class="cam" style="z-index:{i+1}"><video id="v-{sid}" class="clip shot" src="assets/graded/{c}.mp4" data-start="{a}" data-duration="{r(b-a)}" data-media-start="{off}" data-track-index="{1+i%2}" muted playsinline></video></div>')
    cams.append(f'["#cam-{sid}",{a},{r(b-a)},{z},{i%2}]')
sfx=[('whoosh-short.mp3',0.1,0.57,0.25),('sparkle.mp3',0.7,1.8,0.18),
     ('pop.mp3',14.6,0.72,0.3),('whoosh-short.mp3',15.2,0.57,0.18),('pop.mp3',24.28,0.72,0.3),('click-soft.mp3',28.32,0.4,0.3),
     ('pop.mp3',37.58,0.72,0.3),('pop.mp3',51.3,0.72,0.3),
     ('click-soft.mp3',58.42,0.4,0.28),('click-soft.mp3',60.04,0.4,0.28),('click-soft.mp3',61.46,0.4,0.28),('click-soft.mp3',62.62,0.4,0.28),
     ('sparkle.mp3',65.34,1.8,0.2),('pop.mp3',66.94,0.72,0.32)]
aud="\n".join(f'      <audio id="fx{i}" class="clip" src="assets/{n}" data-start="{t}" data-duration="{d}" data-track-index="{10+i%2}" data-volume="{v}"></audio>' for i,(n,t,d,v) in enumerate(sfx))
open('index.html','w').write(f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; transform-origin: 50% 40%; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 90; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <audio id="vo" class="clip" src="assets/shots/vo.m4a" data-start="0" data-duration="{END}" data-track-index="8" data-volume="1"></audio>
{aud}
      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{END}" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 40"></div>
      <div id="subs" data-composition-id="subs" data-composition-src="compositions/subs.html" data-start="0" data-duration="{END}" data-track-index="6" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 50"></div>
      <div id="fade"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      [{",".join(cams)}].forEach(([id, t, d, z, odd]) => {{
        if (z === 0) return;
        tl.fromTo(id, {{ scale: odd ? 1 + z : 1 }}, {{ scale: odd ? 1 : 1 + z, duration: d, ease: "none" }}, t);
      }});
      // short soft dissolve into each feature block
      ["#v-f1a", "#v-f2a", "#v-f3a", "#v-f4a", "#v-h"].forEach((id) => {{
        const el = document.querySelector(id);
        tl.fromTo(id, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "sine.inOut" }}, parseFloat(el.dataset.start));
      }});
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "sine.in" }}, {END-0.51});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
C=[(0.0,1.96,"Inilah pesona <b>farmhouse</b>…"),(1.96,4.88,"simple, tapi susah nak lupa!"),
 (4.88,7.88,"Apa yang buat rumah ni nampak <b>manis</b> sangat?"),(8.26,10.04,"Jom tengok <b>empat detail</b>"),(10.04,12.17,"yang melengkapkan konsep <b>farmhouse</b> ni."),
 (12.18,14.42,"Mula-mula, pandang atas."),(14.6,16.44,"<b>Bumbung segi tiga</b> ni"),(16.44,18.9,"yang bagi bentuk dan karakter pada rumah."),
 (18.94,21.87,"Dari jauh lagi dah <b>mencuri perhatian!</b>"),(21.84,23.37,"Bila dekat sikit,"),(23.4,25.93,"perasan tak <b>jalur-jalur</b> dekat dinding ni?"),
 (26.0,28.32,"Bahagian ni dipasang menggunakan"),(28.32,29.16,"<b>Shera Board</b>."),(29.26,32.76,"Detail garisan tu buat dinding nampak <b>bertekstur</b>."),
 (32.74,34.91,"Cuba bayangkan kalau kosong…"),(34.92,36.44,"lain kan rupanya?"),(36.44,38.93,"Lepas tu, <b>beranda depan</b> ni."),
 (38.96,42.62,"Haa, dekat sinilah kita boleh letak <b>kerusi</b>"),(42.62,43.18,"dengan meja kecil."),(43.2,46.16,"Petang-petang duduk <b>minum kopi</b>"),(46.16,48.77,"sambil borak dengan keluarga… memang <b>seronok!</b>"),
 (48.86,51.3,"Dan yang menyatukan semua tadi…"),(51.3,52.69,"<b>warna putih</b>."),(52.7,54.9,"Nampak <b>bersih</b>, manis,"),(55.0,58.37,"dan detail dinding berjalur tu pun lebih <b>menyerlah</b>."),
 (58.42,60.04,"<b>Bumbung segi tiga</b>,"),(60.04,61.46,"<b>dinding berjalur</b>,"),(61.46,62.62,"<b>beranda depan</b>"),(62.62,63.82,"dan <b>warna putih</b>…"),
 (63.82,65.34,"bila digabungkan,"),(65.34,66.9,"<b>inilah hasilnya!</b>"),(66.94,70.2,"Korang nak tak bina rumah konsep <b>farmhouse</b> macam ni?")]
divs="\n".join(f'    <div id="c{i}" class="cap clip" data-start="{a}" data-duration="{r(b-a)}"><span class="cap-in">{t}</span></div>' for i,(a,b,t) in enumerate(C))
ids=",".join(f'["#c{i}",{a}]' for i,(a,b,t) in enumerate(C))
open('compositions/subs.html','w').write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Montserrat", sans-serif; }}
    .cap {{ position: absolute; left: 70px; top: 1380px; width: 860px; text-align: center; }}
    .cap-in {{ display: inline-block; padding: 12px 24px 14px; border-radius: 18px; background: rgba(0,0,0,0.55); color: #fff; font-weight: 800; font-size: 44px; line-height: 1.2; }}
    .cap-in b {{ color: #f6c33b; font-weight: 900; }}
  </style>
  <div id="root" data-composition-id="subs" data-width="1080" data-height="1920">
{divs}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    [{ids}].forEach(([id, t]) => {{
      tl.fromTo(id + " .cap-in", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, t);
    }});
    window.__timelines["subs"] = tl;
  </script>
</template>
''')
