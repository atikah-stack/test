import sys, json
sys.path.insert(0,'tools'); from timing import M, VO_END, TAIL
SEG=json.load(open('tools/segs.json'))
END=round(M(VO_END)+TAIL,3)
f=lambda x: round(x,3)

# ---------- index.html ----------
vids=[]
for i,s in enumerate(SEG):
    vids.append(f'      <div id="cam-{s["id"]}" class="cam" style="z-index:{i+1}"><video id="{s["id"]}" class="clip shot" src="assets/shots/{s["id"]}.mp4" data-start="{s["start"]}" data-duration="{s["dur"]}" data-media-start="0" data-track-index="{1+i%2}" muted playsinline></video></div>')
BRAND0,BRAND1=M(25.62),M(27.3)
PROD0,PROD1=M(31.34),M(36.37)
sfx=[('whoosh-short',0.0,0.25),('whoosh-short',M(4.25)-0.15,0.2),('whoosh-short',M(13.6)-0.1,0.2),('whoosh-short',M(22.85)-0.15,0.22),
     ('pop',M(25.9),0.3),('pop',M(28.24),0.28),('pop',M(30.52),0.28),('whoosh-short',M(31.34)-0.1,0.2),('pop',M(33.16),0.26),('pop',M(34.62),0.26),
     ('pop',M(37.02),0.26),('pop',M(38.8),0.26),('whoosh-short',M(41.4)-0.1,0.2),('pop',M(43.0),0.26),
     ('pop',M(49.1),0.28),('pop',M(50.12),0.28),('pop',M(51.18),0.28),('click-soft',M(54.06),0.3),
     ('whoosh',M(58.3),0.16),('whoosh',M(59.5),0.14),('pop',M(63.11),0.3),('pop',M(68.3),0.3)]
dur={'pop':0.72,'whoosh-short':0.57,'whoosh':1.2,'click-soft':0.4}
aud="\n".join(f'      <audio id="fx{i}" class="clip" src="assets/{n}.mp3" data-start="{f(max(0,t))}" data-duration="{dur[n]}" data-track-index="{10+i%2}" data-volume="{v}"></audio>' for i,(n,t,v) in enumerate(sfx))
cams=",".join(f'["#cam-{s["id"]}",{s["start"]},{s["dur"]}]' for s in SEG)
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
      .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 90; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{chr(10).join(vids)}

      <!-- VO asal (jeda dipendekkan) -->
      <audio id="vo" class="clip" src="assets/shots/vo.m4a" data-start="0" data-duration="{END}" data-track-index="8" data-volume="1"></audio>
      <!-- SFX ringan (Pixabay) -->
{aud}

      <div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{END}" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 40"></div>
      <div id="subs" data-composition-id="subs" data-composition-src="compositions/subs.html" data-start="0" data-duration="{END}" data-track-index="6" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 50"></div>
      <div id="fade"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // light, consistent push on every shot; the hook gets a clearer zoom-in
      [{cams}].forEach(([id, t, d], i) => {{
        const z = i === 0 ? 0.1 : Math.min(0.012 * d, 0.05);
        tl.fromTo(id, {{ scale: i % 2 ? 1.0 + z : 1.0 }}, {{ scale: i % 2 ? 1.0 : 1.0 + z, duration: d, ease: "none" }}, t);
      }});
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "sine.in" }}, {f(END-0.51)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')

# ---------- subtitles ----------
C=[(0.0,1.82,"Lantai dah siap <b>cantik</b>…"),(1.82,4.2,"kenapa ada orang <b>tutup balik?</b>"),
 (4.3,6.6,"Sebab kerja rumah belum habis,"),(6.6,9.06,"lantai masih <b>berisiko tercalar!</b>"),
 (9.3,11.02,"Pekerja keluar masuk,"),(11.02,13.52,"pasang kabinet, angkut barang…"),
 (13.52,15.56,"<b>pasir halus</b> bawah kasut pun"),(15.56,18.62,"boleh <b>bergesel</b> dan tinggalkan kesan pada lantai."),
 (19.01,20.62,"Belum sempat masuk rumah,"),(20.62,21.7,"dah <b>bercalar</b>."),(21.76,22.83,"<b>Sayang kan?</b>"),
 (22.86,25.64,"Sebab tu ada <b>pelapik perlindungan lantai</b>"),(25.64,27.08,"macam <b>Cobra Mat</b> ni."),
 (27.55,29.7,"Untuk versi <b>2MM Ultra</b>,"),(29.7,31.34,"ketebalannya <b>2 milimeter</b>,"),
 (31.34,33.16,"dengan saiz gulungan"),(33.16,36.16,"<b>1 meter</b> lebar dan <b>12 meter</b> panjang."),
 (36.57,37.98,"Bahannya <b>tahan lasak</b>"),(37.98,39.3,"dan <b>mudah dibentang</b>"),(39.3,41.15,"untuk menutup kawasan kerja."),
 (41.63,43.52,"<b>Fungsinya</b>, bantu lindungi"),(43.52,45.54,"permukaan lantai daripada <b>calar</b>"),(45.54,48.44,"sepanjang pembinaan atau pengubahsuaian."),
 (48.83,50.12,"Bukan <b>mozek</b> je,"),(50.12,53.5,"<b>SPC</b> dan <b>vinyl</b> pun perlukan perlindungan."),
 (53.9,55.68,"Cuma <b>pilih pelapik yang sesuai</b>"),(55.68,56.83,"dengan jenis lantai."),
 (57.27,58.24,"Sebelum bentang,"),(58.24,59.66,"<b>bersihkan lantai dulu</b>"),(59.66,62.63,"supaya pasir tak terperangkap di bawahnya!"),
 (63.11,64.54,"Korang pernah nampak kontraktor"),(64.54,65.87,"guna pelapik macam ni?"),(66.27,67.89,"Atau <b>baru tahu</b> hari ni?"),(68.3,68.92,"<b>Komen sikit!</b>")]
divs="\n".join(f'    <div id="c{i}" class="cap clip" data-start="{M(a)}" data-duration="{f(M(b)-M(a))}"><span class="cap-in">{t}</span></div>' for i,(a,b,t) in enumerate(C))
ids=",".join(f'["#c{i}",{M(a)}]' for i,(a,b,t) in enumerate(C))
open('compositions/subs.html','w').write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Montserrat", sans-serif; }}
    .cap {{ position: absolute; left: 50%; top: 1290px; width: 940px; margin-left: -470px; text-align: center; }}
    .cap-in {{ display: inline-block; padding: 12px 26px 14px; border-radius: 20px; background: rgba(0,0,0,0.6); color: #fff; font-weight: 800; font-size: 46px; line-height: 1.2; }}
    .cap-in b {{ color: #ffd23f; font-weight: 900; }}
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

# ---------- graphics ----------
T=lambda o: M(o)
g=dict(
 H0=0.0,H1=M(4.2),
 W1=M(9.3),W2=M(11.02),W3=M(12.34),W4=M(13.6),
 IL0=M(13.6),IL1=M(21.72),
 B0=BRAND0,B1=BRAND1,
 U0=M(27.55),U1=M(29.7),U2=M(31.34),
 P0=PROD0,P1=PROD1,D1=M(33.16),D2=M(34.62),
 K1=M(37.02),K2=M(38.8),K3=M(41.4),
 L0=M(41.4),L1=M(48.64),LS=M(43.0),
 F1=M(49.1),F2=M(50.12),F3=M(51.18),F4=M(54.06),F5=M(57.05),
 T0=M(57.05),T1=M(62.87),TT=M(58.24),
 CT0=M(62.87),END=END)
for k,v in g.items(): g[k]=f(v)
tpl=open('tools/gfx_template.html').read()
import re
tpl=re.sub(r'\{\{=(.*?)\}\}', lambda m: str(round(eval(m.group(1),{},g),3)), tpl)
for k,v in g.items(): tpl=tpl.replace('{{'+k+'}}',str(v))
open('compositions/gfx.html','w').write(tpl)
print(json.dumps(g))
