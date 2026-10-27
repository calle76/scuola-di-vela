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
LUNGO = "--lungo" in sys.argv; ARG = [a for a in sys.argv[1:] if a != "--lungo" and not a.startswith("--semi") and "-" not in a]
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

# Criteri della partenza (1.0.16, docs/archivio/PROPOSTA-PARTENZE.md §3, scritti prima di provare). Tutto in una chiamata alla pagina per partenza:
# regata, livello, Math.random a seme fisso, simTime a zero, preparazione (che riavvia la regata), passi fissi di 1/60 s fino a 60 s dopo
# lo sparo; il giocatore resta fermo. Le due regate del gioco: bastone (10 nodi costanti) e raffiche (12 nodi rafficati). Per ogni avversario:
# oltre la linea allo sparo (e di quanti metri, a che distanza dal centro), ritardo (sparo → partenza), velocità alla partenza, se nell'ultimo
# minuto è stato nella fascia d'attesa (da una a due lunghezze di barca dietro la linea, 4,2-8,4 m), ritorno dietro la linea se anticipata.
# Criteri: (1) partenze con almeno un richiamo al massimo 30% (principianti) e 20% (esperti), esperti meno dei principianti; (2) ritardo
# mediano al massimo 3 s per preparazione; (3) velocità mediana alla partenza almeno 75% del regime a 50° (10 nodi 4,97 → 3,72; 12 nodi
# 5,60 → 4,20, conto su step() del 16 ottobre 2026); (4) nessun avversario non partito entro 60 s; (6) controllo del metro: almeno metà delle
# barche passa dalla fascia d'attesa, altrimenti NON VALIDO. Uso: --semi a-b (default 1-20; conferma 21-100), --lungo = 1-100.
SEMI_SPARO = range(1, 101 if LUNGO else 21)
if "--semi" in sys.argv: _a, _b = sys.argv[sys.argv.index("--semi") + 1].split("-"); SEMI_SPARO = range(int(_a), int(_b) + 1)
RICHIAMI_MAX = {"principianti": 30, "esperti": 20}; RITARDO_MAX = 3; VEL_MIN = {0: 3.72, 1: 4.20}; RITORNO_MAX = 60
SPARO = """([liv, cd, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  sv.fast(0); sel('aiLevel', liv);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; sel('cdSel', String(cd));
  const R = sv.R, ai = R.boats.filter(b => !b.me), out = {};
  if (R.t >= 0) return null;
  for (const b of ai){ out[b.name] = { oltre: null, lato: null, ritardo: null, vel: null, fascia: false, ritorno: null };
    let v = b.leg; Object.defineProperty(b, 'leg', { get(){ return v; }, set(n){ if (v === 0 && n === 1){ out[b.name].ritardo = +R.t.toFixed(2); out[b.name].vel = +(b.S.u * 1.943844).toFixed(2); } v = n; } }); }
  let sparo = false; const t0 = performance.now(), tSim0 = R.t;
  while (R.t < 60){
    sv.run(1/60, 1);
    ai.forEach(b => { const o = out[b.name], wy = b.prevWY;
      if (R.t < 0 && R.t > -60 && wy >= BOAT.length && wy <= 2 * BOAT.length) o.fascia = true;
      if (!sparo && R.t >= 0 && b.ocs){ o.oltre = +(-wy).toFixed(1); o.lato = +Math.sqrt(Math.max(0, (b.S.x - R.center.x) ** 2 + (b.S.y - R.center.y) ** 2 - wy * wy)).toFixed(1); }
      if (sparo && o.oltre !== null && o.ritorno === null && !b.ocs) o.ritorno = +R.t.toFixed(2); });
    if (R.t >= 0) sparo = true;
  }
  return [ai.map(b => [b.name, out[b.name]]), (performance.now() - t0) / (R.t - tSim0)];
}"""

async def anticipi_allo_sparo(b):
    q = lambda v: f"{min(v)} / {round(statistics.median(v), 2)} / {max(v)}" if v else "—"
    errs = []; non_valido = []; fuori = []; ms = []; richiami = {}
    print(f"criteri della partenza: semi {SEMI_SPARO.start}-{SEMI_SPARO.stop - 1}, 3 avversari, passi fissi di 1/60 s, giocatore fermo", flush=True)
    for reg, nome_reg in ((0, "bastone, 10 nodi"), (1, "raffiche, 12 nodi")):
        for liv in ["principianti", "esperti"]:
            barche = []; partenze = 0; con_richiamo = 0; rit_cd = {}
            for cd in [60, 180, 300]:
                rit_cd[cd] = []
                for seme in SEMI_SPARO:
                    pg = await b.new_page(viewport={"width":1280,"height":800}); pg.on("pageerror", lambda e: errs.append(str(e)))
                    await pg.goto(URL); await pg.wait_for_timeout(300); await pg.click(f"[data-r='{reg}']"); await pg.wait_for_timeout(100)
                    r = await pg.evaluate(SPARO, [liv, cd, seme]); await pg.close()
                    if not r: non_valido.append(f"{nome_reg} {liv} {cd} s seme {seme}: regata non partita"); continue
                    r, m = r; ms.append(m); partenze += 1
                    if any(o["oltre"] is not None for _, o in r): con_richiamo += 1
                    for nome, o in r:
                        barche.append(o)
                        if o["ritardo"] is None: fuori.append(f"(4) {nome_reg} {liv} {cd} s seme {seme} {nome}: non partita entro 60 s")
                        else: rit_cd[cd].append(o["ritardo"])
                        if o["oltre"] is not None:
                            if o["ritorno"] is None or o["ritorno"] > RITORNO_MAX: fuori.append(f"(4) {nome_reg} {liv} {cd} s seme {seme} {nome}: anticipata e non rientrata")
                            print(f"  {nome_reg} {liv} {cd} s seme {seme} {nome}: oltre {o['oltre']} m, a {o['lato']} m dal centro, ritorno {o['ritorno']} s", flush=True)
            pr = 100 * con_richiamo / partenze if partenze else 0; richiami[(reg, liv)] = pr
            ant = [o for o in barche if o["oltre"] is not None]; vel = [o["vel"] for o in barche if o["vel"] is not None]
            fascia = sum(o["fascia"] for o in barche); fuori_estremi = sum(1 for o in ant if o["lato"] > 35)
            print(f"{nome_reg}, {liv}: partenze {partenze}, con almeno un richiamo {con_richiamo} ({pr:.1f}%, soglia {RICHIAMI_MAX[liv]}%);"
                  f" barche oltre la linea {len(ant)} su {len(barche)} ({100 * len(ant) / max(1, len(barche)):.1f}%), di cui fuori dagli estremi {fuori_estremi}", flush=True)
            print(f"  ritardo mediano per preparazione: " + ", ".join(f"{cd} s {statistics.median(v):.1f} s" if v else f"{cd} s —" for cd, v in rit_cd.items())
                  + f" (soglia {RITARDO_MAX} s); velocità alla partenza min / mediana / max {q(sorted(vel))} nodi (soglia mediana {VEL_MIN[reg]});"
                  f" passate dalla fascia d'attesa {fascia} su {len(barche)}; oltre la linea {q(sorted(o['oltre'] for o in ant))} m", flush=True)
            if pr > RICHIAMI_MAX[liv]: fuori.append(f"(1) {nome_reg} {liv}: richiami {pr:.1f}%")
            for cd, v in rit_cd.items():
                if v and statistics.median(v) > RITARDO_MAX: fuori.append(f"(2) {nome_reg} {liv} {cd} s: ritardo mediano {statistics.median(v):.1f} s")
            if vel and statistics.median(vel) < VEL_MIN[reg]: fuori.append(f"(3) {nome_reg} {liv}: velocità mediana {statistics.median(vel):.2f} nodi")
            if partenze < 3 * len(SEMI_SPARO): non_valido.append(f"{nome_reg} {liv}: {partenze} partenze, previste {3 * len(SEMI_SPARO)}")
            if fascia < len(barche) / 2: non_valido.append(f"(6) {nome_reg} {liv}: solo {fascia} barche su {len(barche)} passate dalla fascia d'attesa")
        if richiami[(reg, "esperti")] >= richiami[(reg, "principianti")]: fuori.append(f"(1) {nome_reg}: esperti {richiami[(reg, 'esperti')]:.1f}% non meno dei principianti {richiami[(reg, 'principianti')]:.1f}%")
    if errs: non_valido.append(f"errori della pagina: {errs[:2]}")
    print(f"tempo di calcolo: {statistics.median(ms):.2f} ms per secondo simulato (mediana, massimo {max(ms):.2f})", flush=True)
    esito = "NON VALIDO" if non_valido else ("FALLITO" if fuori else "OK")
    print(f"criteri della partenza: {esito}" + (f"; non valido: {non_valido}" if non_valido else "") + (f"; fuori criterio: {fuori}" if fuori else ""), flush=True)
    return esito

async def main():
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
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
        esito = await anticipi_allo_sparo(b)
        # solo contro il fantasma
        pg = await b.new_page(viewport={"width":1280,"height":800}); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300); await pg.click("[data-r='0']"); await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", "nessuno"]); await pg.wait_for_timeout(300)
        print("modalità solitaria, barche in acqua:", await pg.evaluate("__sv.R.boats.length"), "| testo:", (await pg.evaluate("__sv.R.brief"))[-90:])
        await pg.click('#openSet'); await pg.click("#viewMode button[data-v='nord']"); await pg.click('#setClose')
        await pg.click("#c"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(OUT / "turn.png")); await pg.keyboard.up("ArrowLeft")
        print("errori:", errs[:1])
        await b.close()
    sys.exit(0 if esito == "OK" else 1)
asyncio.run(main())
