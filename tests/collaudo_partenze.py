# Le opzioni di regata stanno nel riquadro delle istruzioni, che nei collaudi è saltato: si impostano direttamente.
# Misura: ritardo degli avversari sulla linea con 1, 3 e 5 minuti di preparazione; geometria delle posizioni iniziali
# (distanza minima fra le barche e coppie in rotta di collisione); caratteri assegnati. Verifica anche la regata in solitaria.
# Uso: python collaudo_partenze.py [partenze per tipo] [livello avversari]
import asyncio, sys, statistics
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
RIP = int(sys.argv[1]) if len(sys.argv) > 1 else 10
LIV = sys.argv[2] if len(sys.argv) > 2 else "principianti"
WATCH = """(()=>{ window._st={}; for (const b of __sv.R.boats){ let v=b.leg; Object.defineProperty(b,'leg',{get(){return v}, set(n){ if(v===0&&n===1) window._st[b.name]=+__sv.R.t.toFixed(1); v=n; }}); } })()"""
# geometria della partenza: distanza minima fra le barche e punto di minimo avvicinamento (rotta di collisione)
GEO = """(() => {
  const D = Math.PI/180, bs = __sv.R.boats.map(b => ({ n: b.name, x: b.S.x, y: b.S.y, h: b.S.h, u: b.S.u, c: b.char || "-" }));
  // distanza dalla linea in coordinate del vento (la linea è a y = 0, le barche partono da y > 0)
  const th = -__sv.twd * D, wy = (x, y) => x*Math.sin(th) + y*Math.cos(th);
  let dmin = 1e9, dpair = "", cpaMin = 1e9, cpaPair = "";
  for (let i = 0; i < bs.length; i++) for (let j = i+1; j < bs.length; j++){
    const a = bs[i], b = bs[j], rx = b.x-a.x, ry = b.y-a.y;
    const d = Math.hypot(rx, ry); if (d < dmin){ dmin = d; dpair = a.n+"/"+b.n; }
    const vx = Math.sin(b.h*D)*b.u - Math.sin(a.h*D)*a.u, vy = -Math.cos(b.h*D)*b.u + Math.cos(a.h*D)*a.u;
    const vv = vx*vx + vy*vy; if (vv < 1e-6) continue;
    let t = -(rx*vx + ry*vy)/vv; if (t <= 0 || t > 25) continue;   // si avvicinano entro 25 s
    const c = Math.hypot(rx + vx*t, ry + vy*t); if (c < cpaMin){ cpaMin = c; cpaPair = a.n+"/"+b.n+" a "+t.toFixed(0)+" s"; }
  }
  return { dmin: +dmin.toFixed(1), dpair, cpa: cpaMin > 1e8 ? null : +cpaMin.toFixed(1), cpaPair,
           car: bs.map(b => b.n+":"+b.c).join(" "),
           y0: Object.fromEntries(bs.map(b => [b.n, +wy(b.x, b.y).toFixed(1)])) };
})()"""

async def partenza(b, cd, geo_only=False):
    pg = await b.new_page(viewport={"width":1280,"height":800})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click("[data-r='0']"); await pg.wait_for_timeout(150)
    await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", LIV]); await pg.wait_for_timeout(150)
    await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", cd]); await pg.wait_for_timeout(200)
    geo = await pg.evaluate(GEO)
    if geo_only: await pg.close(); return geo, {}, [], errs
    await pg.evaluate(WATCH); await pg.evaluate("__sv.fast(20)")
    await pg.wait_for_timeout(int((int(cd)+60)/20*1000)+1500)
    st = await pg.evaluate("window._st")
    ocs = await pg.evaluate("__sv.R.boats.filter(b=>!b.me&&b.ocs).map(b=>b.name)")
    await pg.close()
    return geo, st, ocs, errs

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print(f"avversari: {LIV}; {RIP} partenze per tipo")
        for cd in ["60", "180", "300"]:
            rit = []; anticipi = 0; dmin = []; cpa = []; err = []; coppie = []
            for i in range(RIP):
                geo, st, ocs, errs = await partenza(b, cd)
                rit += [v for k, v in st.items() if k != "Tu"]
                coppie += [(geo["y0"][k], v) for k, v in st.items() if k != "Tu" and k in geo["y0"]]
                anticipi += len(ocs); dmin.append(geo["dmin"]); err += errs[:1]
                if geo["cpa"] is not None: cpa.append((geo["cpa"], geo["cpaPair"]))
                print(f"  preparazione {cd} s, partenza {i+1}: ritardi {st} | anticipate {ocs} | distanza minima {geo['dmin']} m ({geo['dpair']})"
                      + (f" | avvicinamento minimo {geo['cpa']} m ({geo['cpaPair']})" if geo["cpa"] is not None else "")
                      + f" | caratteri {geo['car']}", flush=True)
            mancanti = RIP * 3 - len(rit) if LIV != "nessuno" else 0
            print(f"preparazione {cd} s: ritardo medio {statistics.mean(rit):.1f} s, mediana {statistics.median(rit):.1f} s, massimo {max(rit):.1f} s"
                  f" su {len(rit)} partenze di avversari (non partiti: {mancanti}); partenze anticipate {anticipi};"
                  f" distanza minima all'avvio {min(dmin)}-{max(dmin)} m;"
                  f" avvicinamento minimo {min(cpa)[0] if cpa else '—'} m" + (f" ({min(cpa)[1]})" if cpa else "") + f"; errori {err[:1]}", flush=True)
            if len(coppie) > 4:
                ys = [c[0] for c in coppie]; ds = [c[1] for c in coppie]
                my = sum(ys)/len(ys); md = sum(ds)/len(ds)
                num = sum((y-my)*(d-md) for y, d in coppie)
                den = (sum((y-my)**2 for y in ys) * sum((d-md)**2 for d in ds)) ** 0.5
                vicine = [d for y, d in coppie if y <= my]; lontane = [d for y, d in coppie if y > my]
                print(f"  distanza dalla linea e ritardo: correlazione {num/den if den else 0:+.2f};"
                      f" nate vicine (y<={my:.0f} m) ritardo mediano {statistics.median(vicine):.1f} s su {len(vicine)};"
                      f" nate lontane ritardo mediano {statistics.median(lontane):.1f} s su {len(lontane)}", flush=True)
        # solo contro il fantasma
        pg = await b.new_page(viewport={"width":1280,"height":800}); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300); await pg.click("[data-r='0']"); await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", "nessuno"]); await pg.wait_for_timeout(300)
        print("modalità solitaria, barche in acqua:", await pg.evaluate("__sv.R.boats.length"), "| testo:", (await pg.evaluate("__sv.R.brief"))[-90:])
        await pg.click('#openSet'); await pg.click("#viewMode button[data-v='nord']"); await pg.click('#setClose')
        await pg.click("#c"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(OUT / "turn.png")); await pg.keyboard.up("ArrowLeft")
        print("errori:", errs[:1])
        await b.close()
asyncio.run(main())
