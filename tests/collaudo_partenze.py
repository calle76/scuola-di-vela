# Le opzioni di regata stanno nel riquadro delle istruzioni, che nei collaudi è saltato: si impostano direttamente.
# Misura: ritardo degli avversari sulla linea con 1, 3 e 5 minuti di preparazione; geometria delle posizioni iniziali
# (distanza minima fra le barche e coppie in rotta di collisione); caratteri assegnati. Verifica anche la regata in solitaria.
# Il conteggio «ancora segnate come anticipate a +60 s» (fino alla 0.20.3 «partenze anticipate») guarda le barche ancora segnate
# alla fine della finestra: non sono le partenze anticipate allo sparo, misurate a parte più sotto.
# Dal 13 ottobre 2026 anche la prima parte (ritardi e geometria) gira a passi fissi con seme fisso, tutta in una sola chiamata
# alla pagina, come gli «anticipi allo sparo»: prima girava in tempo reale accelerato (__sv.fast(20)) e senza seme, e i numeri
# cambiavano da un giro all'altro. Seme = numero della partenza; la finestra va fino a 60 s dopo lo sparo, come prima.
# Uso: python collaudo_partenze.py [partenze per tipo] [livello avversari] [--lungo]
#   prima parte: semi 1..N (N = partenze per tipo, 10 se manca); con --lungo i semi 11-40 (conferma)
#   --lungo: anche la parte «anticipi allo sparo» con i semi 1-100 invece di 1-20 (nella sandbox 669 s invece di 135)
import asyncio, sys, statistics
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
LUNGO = "--lungo" in sys.argv; ARG = [a for a in sys.argv[1:] if a != "--lungo"]
RIP = int(ARG[0]) if len(ARG) > 0 else 10
LIV = ARG[1] if len(ARG) > 1 else "principianti"
SEMI_RIT = list(range(11, 41)) if LUNGO else list(range(1, RIP + 1))
# una partenza intera in una chiamata: livello, seme, simTime a zero, preparazione (che riavvia la regata), geometria all'avvio,
# poi passi fissi di 1/60 s fino a 60 s dopo lo sparo; il giocatore resta fermo
PARTENZA = """([liv, cd, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  sv.fast(0); sel('aiLevel', liv);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; sel('cdSel', String(cd));
  const R = sv.R; if (R.t >= 0) return null;
  sv.run(1/60, 12);                // 0,2 s simulati: come i 200 ms reali che prima passavano fra il riavvio e la misura della geometria
  const geo = (GEO)();
  const st = {};
  for (const b of R.boats){ let v = b.leg; Object.defineProperty(b, 'leg', { get(){ return v; }, set(n){ if (v === 0 && n === 1) st[b.name] = +R.t.toFixed(1); v = n; } }); }
  while (R.t < 60) sv.run(1/60, 1);
  return [geo, st, R.boats.filter(b => !b.me && b.ocs).map(b => b.name)];
}"""
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

async def partenza(b, cd, seme):
    pg = await b.new_page(viewport={"width":1280,"height":800})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click("[data-r='0']"); await pg.wait_for_timeout(150)
    r = await pg.evaluate(PARTENZA.replace("(GEO)", "(" + GEO.strip()[1:-3] + ")"), [LIV, int(cd), seme])
    await pg.close()
    if not r: return None, {}, [], errs + [f"seme {seme}: regata non partita"]
    geo, st, ocs = r
    return geo, st, ocs, errs

# Anticipi allo sparo (dopo la 0.20.3): riproducibile come collaudo_suggerimento.py. Tutto dentro una sola chiamata alla pagina:
# livello, Math.random a seme fisso, simTime a zero, preparazione (che riavvia la regata), poi passi fissi di 1/60 s con __sv.run
# fino a 60 s dopo lo sparo; il giocatore resta fermo. Per ogni avversario: oltre la linea allo sparo e di quanti metri,
# anticipo (secondi prima dello sparo dell'ultimo attraversamento della linea), secondi dallo sparo al ritorno dietro la linea.
# Criterio (decisione di Ale, dopo la 0.20.3): boccia solo il ritorno, cioè ogni barca anticipata deve tornare dietro la linea
# entro 60 s. Il primo criterio chiedeva anche al massimo 10 m oltre la linea, soglia scelta dopo aver visto i semi 1-20
# (massimo 9,4 m); sui semi 21-100 non ha retto (10,3 e 17,7 m), perché fuori dalla zona del freno (40 m dal centro della linea)
# nessun codice limita lo sconfinamento. Ora metri, frequenza e anticipo si stampano ma non bocciano; la riga «oltre 10 m» è
# solo informativa. Minimo 10 anticipate per livello, scelto prima di rilanciare.
SEMI_SPARO = range(1, 101 if LUNGO else 21); OLTRE_INFO = 10; RITORNO_MAX = 60; MIN_ANTICIPATE = 10
SPARO = """([liv, cd, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  sv.fast(0); sel('aiLevel', liv);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; sel('cdSel', String(cd));
  const R = sv.R, ai = R.boats.filter(b => !b.me), tx = {}, out = {};
  if (R.t >= 0) return null;
  for (const b of ai){ tx[b.name] = null; out[b.name] = { oltre: null, lato: null, anticipo: null, ritorno: null }; }
  let sparo = false;
  while (R.t < 60){
    const prima = ai.map(b => b.prevWY); sv.run(1/60, 1);
    ai.forEach((b, i) => { const o = out[b.name], wy = b.prevWY;
      if (R.t < 0 && prima[i] > 0 && wy <= 0) tx[b.name] = R.t;
      if (!sparo && R.t >= 0 && b.ocs){ o.oltre = +(-wy).toFixed(1); o.lato = +Math.sqrt(Math.max(0, b.S.x*b.S.x + b.S.y*b.S.y - wy*wy)).toFixed(1); o.anticipo = tx[b.name] === null ? null : +(-tx[b.name]).toFixed(2); }
      if (sparo && o.oltre !== null && o.ritorno === null && !b.ocs) o.ritorno = +R.t.toFixed(2); });
    if (R.t >= 0) sparo = true;
  }
  return ai.map(b => [b.name, out[b.name]]);
}"""

async def anticipi_allo_sparo(b):
    q = lambda v: f"{min(v)} / {round(statistics.median(v), 2)} / {max(v)}" if v else "—"
    errs = []; non_valido = []; fallite = []
    print(f"anticipi allo sparo: semi {SEMI_SPARO.start}-{SEMI_SPARO.stop - 1}, 3 avversari, passi fissi di 1/60 s, giocatore fermo", flush=True)
    for liv in ["principianti", "esperti"]:
        casi = 0; ant = []; per_cd = {}; oltre = []
        for cd in [60, 180, 300]:
            n = 0; k = 0
            for seme in SEMI_SPARO:
                pg = await b.new_page(viewport={"width":1280,"height":800}); pg.on("pageerror", lambda e: errs.append(str(e)))
                await pg.goto(URL); await pg.wait_for_timeout(300); await pg.click("[data-r='0']"); await pg.wait_for_timeout(100)
                r = await pg.evaluate(SPARO, [liv, cd, seme]); await pg.close()
                if not r: non_valido.append(f"{liv} {cd} s seme {seme}: regata non partita"); continue
                for nome, o in r:
                    n += 1
                    if o["oltre"] is None: continue
                    k += 1; ant.append(o)
                    if o["anticipo"] is None: non_valido.append(f"{liv} {cd} s seme {seme} {nome}: attraversamento non trovato")
                    if o["ritorno"] is None or o["ritorno"] > RITORNO_MAX: fallite.append(f"{liv} {cd} s seme {seme} {nome}: {o}")
                    if o["oltre"] > OLTRE_INFO: oltre.append(f"{liv} {cd} s seme {seme} {nome} {o['oltre']} m, a {o['lato']} m dal centro")
                    print(f"  {liv} {cd} s seme {seme} {nome}: oltre {o['oltre']} m, a {o['lato']} m dal centro, anticipo {o['anticipo']} s, ritorno {o['ritorno']} s", flush=True)
            casi += n; per_cd[cd] = (k, n)
        print(f"{liv}: partenze di avversari misurate {casi} (previste {3 * 3 * len(SEMI_SPARO)}); anticipate {len(ant)}"
              f" ({100 * len(ant) / casi if casi else 0:.1f}%); per preparazione "
              + ", ".join(f"{cd} s {k} su {n} ({100 * k / n if n else 0:.1f}%)" for cd, (k, n) in per_cd.items()), flush=True)
        print(f"  anticipo min / mediana / max: {q(sorted(o['anticipo'] for o in ant if o['anticipo'] is not None))} s;"
              f" oltre la linea: {q(sorted(o['oltre'] for o in ant))} m;"
              f" ritorno dietro la linea: {q(sorted(o['ritorno'] for o in ant if o['ritorno'] is not None))} s", flush=True)
        print(f"  oltre {OLTRE_INFO} m (solo informativo, non boccia): {len(oltre)} su {len(ant)} anticipate" + (f": {oltre}" if oltre else ""), flush=True)
        if casi < 3 * 3 * len(SEMI_SPARO): non_valido.append(f"{liv}: misurate {casi} partenze, previste {3 * 3 * len(SEMI_SPARO)}")
        if len(ant) < MIN_ANTICIPATE: non_valido.append(f"{liv}: {len(ant)} anticipate misurate, minimo {MIN_ANTICIPATE}")
    if errs: non_valido.append(f"errori della pagina: {errs[:2]}")
    esito = "NON VALIDO" if non_valido else ("FALLITO" if fallite else "OK")
    print(f"anticipi allo sparo: {esito} (ogni anticipata di nuovo dietro la linea entro {RITORNO_MAX} s)"
          + (f"; non valido: {non_valido}" if non_valido else "") + (f"; fuori criterio: {fallite}" if fallite else ""), flush=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print(f"avversari: {LIV}; semi {SEMI_RIT[0]}-{SEMI_RIT[-1]} per tipo, passi fissi di 1/60 s, giocatore fermo")
        for cd in ["60", "180", "300"]:
            rit = []; anticipi = 0; dmin = []; cpa = []; err = []; coppie = []
            for i, seme in enumerate(SEMI_RIT):
                geo, st, ocs, errs = await partenza(b, cd, seme)
                if geo is None: err += errs[:1]; continue
                rit += [v for k, v in st.items() if k != "Tu"]
                coppie += [(geo["y0"][k], v) for k, v in st.items() if k != "Tu" and k in geo["y0"]]
                anticipi += len(ocs); dmin.append(geo["dmin"]); err += errs[:1]
                if geo["cpa"] is not None: cpa.append((geo["cpa"], geo["cpaPair"]))
                print(f"  preparazione {cd} s, seme {seme}: ritardi {st} | ancora segnate come anticipate a +60 s {ocs} | distanza minima {geo['dmin']} m ({geo['dpair']})"
                      + (f" | avvicinamento minimo {geo['cpa']} m ({geo['cpaPair']})" if geo["cpa"] is not None else "")
                      + f" | caratteri {geo['car']}", flush=True)
            mancanti = len(SEMI_RIT) * 3 - len(rit) if LIV != "nessuno" else 0
            print(f"preparazione {cd} s: ritardo medio {statistics.mean(rit):.1f} s, mediana {statistics.median(rit):.1f} s, massimo {max(rit):.1f} s"
                  f" su {len(rit)} partenze di avversari (non partiti: {mancanti}); ancora segnate come anticipate a +60 s {anticipi};"
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
        await anticipi_allo_sparo(b)
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
