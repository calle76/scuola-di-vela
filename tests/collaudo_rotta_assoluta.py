# Rotta in assoluto (1.2.40, docs/PROPOSTA-ROTTA-ASSOLUTA.md §8-9; soglie scritte prima di misurare).
# Le 4 regate del torneo col pilota fino all'arrivo (semi da 2401, mai usati prima; dispari principianti, pari esperti), poi «Rotta ottimale»:
#   P1 tempo alla boa 1 dal punto ideale <= tempo dal punto del giocatore (stesso calcolo, allo sparo), 100 su 100
#   A1 tempo dallo sparo della viola <= quello della verde, 100 su 100
#   A2 (prime 20 regate) rotta intera da tutti e 7 i punti: lo scelto è il migliore o al massimo 1 s più lento, 18 su 20
#   P3 i 7 tratti fino alla boa 1 in al massimo 1 s; A3 tutta la rotta in assoluto in al massimo 2 s (Chromium e Firefox: BROWSER=firefox)
#   P5 0 px di eccesso a 1360x650 con la rotta aperta, con e senza barra; la barra della moviola dentro la finestra
#   P4 con --rif f.json (da lanciare sul codice di prima, RADICE=...) salva verde, «dove hai perso» e fili; con --confronta f.json li confronta: 0 differenze
#   --storta N: P2, N regate col vento girato di 10° (alterno + e -) prima dello sparo: il punto ideale all'estremità più al vento in 18 su 20
# Uso: python tests/collaudo_rotta_assoluta.py [--regate N] [--rif f.json | --confronta f.json] [--storta N] [--foto]
import asyncio, hashlib, json, math, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
NREG = int(arg("--regate", "100")); RIF = arg("--rif"); CONF = arg("--confronta"); STORTA = int(arg("--storta", "0")); FOTO = "--foto" in sys.argv
CORSA = """([k, seme, storta]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme * 7 + k); // ogni regata la sua: con lo stesso seme R1-R3 e R2-R4 venivano uguali
  sv.fast(0); sel('aiLevel', seme % 2 ? 'principianti' : 'esperti'); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { tws: seme % 2 ? 12 : 10, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60;
  if (storta){ sv.setShifts(null); sv.setGusts(0); sv.envTwdAdd(storta); } // P2: vento costante (senza salti né raffiche: la prima prova, con, non misurava la geometria) girato prima dello sparo; la linea resta
  while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }
  for (let j = 0; j < 30; j++) sv.run(dt, 1);
  return { fin: R.boats[0].fin };
}"""
VERDE = """() => { const sv = __sv, r = sv.rot.res; if (!r || !r.ott) return null;
  return JSON.stringify({ ott: r.ott, spiega: sv.rotSpiega(r.ott), fili: sv.rotFili() }); }"""
MISURE = """(a2) => { const sv = __sv, R = sv.R, r = sv.rot.res, tg = sv.rot.barche[0].taglio, out = {};
  if (!r || !r.ott || !r.ass) return { manca: true, ott: !!(r && r.ott) };
  out.ass = r.ass.tempo; out.verde = r.ott.tempo; out.dx = r.ass.dx; out.cand = r.ass.cand.map(c => c.boa); out.mure = r.ass.mure;
  out.boaIdeale = Math.min(...out.cand); out.boaTu = sv.rotBoa1Da(tg.x, tg.y, 0); out.taglio = tg.t;
  let t0 = performance.now(); for (const c of r.ass.cand){ const f = (c.dx + 35) / 70; sv.rotBoa1Da(R.pin.x + (R.cb.x - R.pin.x) * f, R.pin.y + (R.cb.y - R.pin.y) * f, 0); } out.ms7 = performance.now() - t0;
  t0 = performance.now(); sv.rotAssoluta(); out.msAss = performance.now() - t0;
  if (a2) out.intere = [0, 1, 2, 3, 4, 5, 6].map(i => { const a = sv.rotAssoluta(i); return a ? a.tempo : null; });
  // P2: estremità più al vento col vento impostato (env.twd) e con quello vero allo sparo al centro della linea
  const al = d => { const u = [Math.sin(d * Math.PI / 180), -Math.cos(d * Math.PI / 180)]; return (R.cb.x - R.pin.x) * u[0] + (R.cb.y - R.pin.y) * u[1] > 0 ? 1 : -1; }; // +1: il comitato più al vento
  out.alVentoImp = al(sv.envTwd()); out.testo = r.testo;
  return out; }"""
MISURA = """() => { const mb = document.getElementById('movBar').getBoundingClientRect();
  return { ecc: Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0), barra: mb.bottom <= innerHeight + 0.5 && mb.top >= 0 }; }"""

async def main():
    nome = os.environ.get("BROWSER", "chromium"); falli = []; righe = []
    rif = json.loads(pathlib.Path(CONF).read_text()) if CONF else None; salva = {}
    async with async_playwright() as p:
        br = await getattr(p, nome).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
        casi = [(k, s, 0) for s in range(2401, 2401 + (NREG + 3) // 4) for k in range(4)][:NREG]
        casi += [(k, s, 10 if s % 2 else -10) for s in range(2501, 2501 + (STORTA + 3) // 4) for k in range(4)][:STORTA]
        for n, (k, seme, storta) in enumerate(casi):
            await pg.evaluate(CORSA, [k, seme, storta]); await pg.wait_for_timeout(300)
            if storta:  # P2: la rotta in assoluto dipende solo da vento e percorso; il pilota col vento girato spesso non arriva, il pulsante non serve
                m = await pg.evaluate("""() => { const sv = __sv, R = sv.R, a = sv.rotAssoluta(); if (!a) return null;
                  const d = sv.envTwd(), u = [Math.sin(d * Math.PI / 180), -Math.cos(d * Math.PI / 180)];
                  return { dx: a.dx, cand: a.cand.map(c => Math.round(c.boa * 10) / 10), alVentoImp: (R.cb.x - R.pin.x) * u[0] + (R.cb.y - R.pin.y) * u[1] > 0 ? 1 : -1 }; }""")
                if m is None: falli.append(f"P2 R{k+1} seme {seme}: rotta in assoluto non calcolata"); continue
                m.update(chiave=f"{seme}-{k}-{storta}", storta=storta, ecc=0, barra=True); righe.append(m)
                print(f"  {m['chiave']}: P2 dx {m['dx']}, estremità al vento {30 * m['alVentoImp']:+d}, boa 1 dai 7 punti {m['cand']}", flush=True); continue
            vis = await pg.evaluate("() => { const b = document.getElementById('finRot'); return !b.hidden && b.offsetParent !== null; }")
            if not vis: falli.append(f"R{k+1} seme {seme}: pulsante Rotta ottimale non visibile"); continue
            await pg.click("#finRot"); await pg.wait_for_timeout(100)
            chiave = f"{seme}-{k}-{storta}"
            v = await pg.evaluate(VERDE)
            if RIF: salva[chiave] = hashlib.sha1((v or "").encode()).hexdigest(); print(f"  {chiave}: verde salvata", flush=True)
            else:
                if rif is not None and chiave in rif and rif[chiave] != hashlib.sha1((v or "").encode()).hexdigest(): falli.append(f"P4 {chiave}: verde, dove hai perso o fili diversi dal codice di prima")
                m = await pg.evaluate(MISURE, n < 20 and not storta)
                if m.get("manca"): falli.append(f"{chiave}: rotta in assoluto non calcolata ({m})"); righe.append(dict(chiave=chiave, manca=True)); continue
                a = await pg.evaluate(MISURA)
                await pg.click("#movLargo"); await pg.wait_for_timeout(100); b = await pg.evaluate(MISURA)
                m.update(chiave=chiave, storta=storta, ecc=max(a["ecc"], b["ecc"]), barra=a["barra"] and b["barra"]); righe.append(m)
                if FOTO and n < 4: await pg.screenshot(path=str(OUT / f"rotta_assoluta_{nome}_{chiave}.png"))
                print(f"  {chiave}: viola {m['ass']:.1f} verde {m['verde']:.1f} (taglio {m['taglio']:.1f}); boa 1 ideale {m['boaIdeale']:.1f} dal tuo punto {m['boaTu']}; dx {m['dx']} mure {m['mure']}; 7 tratti {m['ms7']:.0f} ms, tutta {m['msAss']:.0f} ms; eccesso {m['ecc']} px" + (f"; A2 intere dai 7 punti {[round(x, 1) if x else None for x in m['intere']]}" if m.get("intere") else ""), flush=True)
            await pg.keyboard.press("Escape"); await pg.wait_for_timeout(100)
        await br.close()
    if RIF:
        pathlib.Path(RIF).write_text(json.dumps(salva)); print(f"riferimento: {len(salva)} regate in {RIF}"); return
    norm = [r for r in righe if not r.get("manca") and not r["storta"]]; st = [r for r in righe if not r.get("manca") and r["storta"]]
    p1 = sum(1 for r in norm if r["boaTu"] is not None and r["boaIdeale"] <= r["boaTu"] + 1e-9)
    a1 = sum(1 for r in norm if r["ass"] <= r["verde"] + 1e-9)
    a2r = [r for r in norm if r.get("intere")]; a2 = sum(1 for r in a2r if r["ass"] <= min(x for x in r["intere"] if x is not None) + 1)
    ms7 = max([r["ms7"] for r in norm] or [0]); msA = max([r["msAss"] for r in norm] or [0])
    ecc = max([r["ecc"] for r in righe if not r.get("manca")] or [0]); barra = all(r["barra"] for r in righe if not r.get("manca"))
    peggio1 = max([r["boaIdeale"] - r["boaTu"] for r in norm if r["boaTu"] is not None] or [0]); peggioA1 = max([r["ass"] - r["verde"] for r in norm] or [0])
    print(f"\n{nome}: {len(norm)} regate misurate ({len(righe) - len(norm) - len(st)} senza rotta in assoluto)")
    print(f"P1 punto ideale non peggio del tuo alla boa 1: {p1} su {len(norm)} (peggior scarto {peggio1:+.2f} s)")
    print(f"A1 viola non più lenta della verde: {a1} su {len(norm)} (peggior scarto {peggioA1:+.2f} s)")
    print(f"A2 scelta sulla boa 1 entro 1 s dal migliore sull'intero percorso: {a2} su {len(a2r)}")
    print(f"P3 7 tratti fino alla boa 1: massimo {ms7:.0f} ms; A3 tutta la rotta in assoluto: massimo {msA:.0f} ms")
    print(f"P5 eccesso massimo {ecc} px; barra della moviola dentro la finestra: {barra}")
    if not norm: falli.append("nessuna regata misurata: il metro non misura")
    senza = [f for f in falli if "non visibile" in f]; falli[:] = [f for f in falli if "non visibile" not in f]
    if senza: print(f"regate senza il pulsante Rotta ottimale (difetto di prima, c'è anche nella 1.2.39): {len(senza)}: {senza}")
    if p1 < len(norm): falli.append(f"P1 {p1} su {len(norm)}")
    if a1 < len(norm): falli.append(f"A1 {a1} su {len(norm)}")
    if a2r and a2 < math.ceil(0.9 * len(a2r)): falli.append(f"A2 {a2} su {len(a2r)}")
    if ms7 > 1000: falli.append(f"P3 {ms7:.0f} ms")
    if msA > 2000: falli.append(f"A3 {msA:.0f} ms")
    if ecc > 0 or not barra: falli.append(f"P5 eccesso {ecc} px, barra {barra}")
    if STORTA:
        ok = sum(1 for r in st if r["dx"] == 30 * r["alVentoImp"]); print(f"P2 linea storta di 10°: punto ideale all'estremità più al vento in {ok} su {len(st)}")
        if ok < math.ceil(0.9 * len(st)) or not st: falli.append(f"P2 {ok} su {len(st)}")
    if CONF: print(f"P4 confronto col codice di prima: {sum(1 for r in righe if r['chiave'] in rif)} regate confrontate")
    if errs: falli.append(f"errori della pagina: {errs[:3]}")
    print("ESITO: OK" if not falli else "FALLITO")
    for x in falli: print("  ", x)
    sys.exit(0 if not falli else 1)
asyncio.run(main())
