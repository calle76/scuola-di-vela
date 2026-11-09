# Misura della proposta docs/PROPOSTA-PARTENZA-ESTREMITA.md (8 novembre 2026). Non è un collaudo: stampa i numeri dei criteri 1-5.
# Per ogni partenza: regata (bastone, raffiche, salti), livello (principianti, esperti), preparazione (60, 180, 300 s), seme; passi fissi di 1/60 s,
# giocatore fermo, fino a 60 s dopo lo sparo. Per ogni avversario: x allo sparo (lungo la linea, dal centro), oltre la linea allo sparo,
# istante del taglio valido, riposizionamenti; per la regata: contatti fra -60 s e +20 s.
# Più processi: SALVA=file.json per ognuno, poi python tests/misura_partenza_estremita.py --riassumi file1.json file2.json ...
# Uso: python tests/misura_partenza_estremita.py PRIMO ULTIMO [X_RIPOS T_RIPOS POPPA]   (senza costanti: riposizionamento spento)
# REGATE=2,3 sceglie le regate (0 bastone, 1 raffiche, 2 salti, 3 giri; senza: 0,1,2).
#   X_RIPOS in metri dal centro (negativo, es. -33), T_RIPOS in secondi; POPPA 1 = parte B accesa. BROWSER=firefox per l'altro browser.
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
A, B = (int(sys.argv[1]), int(sys.argv[2])) if sys.argv[1] != "--riassumi" else (0, 0)
PAR = None if sys.argv[1] == "--riassumi" else [float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 0] if len(sys.argv) > 4 else None
CORSA = """([reg, liv, cd, seme, par]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  if (par && sv.ripos) sv.ripos(par[0], par[1], par[2]); else if (sv.ripos) sv.ripos(null);
  sv.fast(0); sv.openItem(["r", reg]); sel('aiLevel', liv);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; sel('cdSel', String(cd));
  const R = sv.R; if (R.t >= 0) return null;
  const ux = R.cb.x - R.pin.x, uy = R.cb.y - R.pin.y, un = Math.hypot(ux, uy), lx = b => ((b.S.x - R.center.x) * ux + (b.S.y - R.center.y) * uy) / un;
  const ai = R.boats.filter(b => !b.me), out = {};
  for (const b of ai){ out[b.name] = { x0: null, ocs0: false, taglio: null, xTaglio: null };
    let v = b.leg; Object.defineProperty(b, 'leg', { get(){ return v; }, set(n){ if (v === 0 && n === 1){ out[b.name].taglio = +R.t.toFixed(2); out[b.name].xTaglio = +lx(b).toFixed(1); } v = n; } }); }
  let sparo = false, nPen = R.penList.length, contatti = 0;
  while (R.t < 60){
    sv.run(1/60, 1);
    if (R.penList.length > nPen){ for (let k = nPen; k < R.penList.length; k++) if (/contatto/.test(R.penList[k]) && R.t >= -60 && R.t <= 20) contatti++; nPen = R.penList.length; }
    if (!sparo && R.t >= 0){ sparo = true; for (const b of ai){ out[b.name].x0 = +lx(b).toFixed(1); out[b.name].ocs0 = !!b.ocs; } }
  }
  for (const b of ai) out[b.name].ripos = b.riposN || 0, out[b.name].poppa = b.poppaN || 0;
  return { barche: out, contatti };
}"""
NOMI = ["bastone", "raffiche", "salti", "giri"]  # REGATE=2,3 per scegliere (3 = giri di penalità, regata di Deriva)
REGATE = [(int(k), NOMI[int(k)]) for k in os.environ.get("REGATE", "0,1,2").split(",")]

async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        tutte = []; contatti = 0; regate = 0; perReg = []
        for reg, nome in REGATE:
            for liv in ("principianti", "esperti"):
                for cd in (60, 180, 300):
                    for seme in range(A, B + 1):
                        r = await pg.evaluate(CORSA, [reg, liv, cd, seme, PAR])
                        if not r: print("non partita", nome, liv, cd, seme); continue
                        regate += 1; contatti += r["contatti"]; perReg.append([nome, liv, cd, seme, r["contatti"]])
                        for n, o in r["barche"].items(): o.update(reg=nome, liv=liv, cd=cd, seme=seme, nome=n); tutte.append(o)
            print(f"  {nome} fatta", flush=True)
        await br.close()
    nome = os.environ.get("SALVA")
    PERREG.extend(perReg)
    if nome: pathlib.Path(nome).write_text(json.dumps({"tutte": tutte, "contatti": contatti, "regate": regate, "errori": len(errs), "perRegata": perReg}))
    riassumi(tutte, contatti, regate, len(errs))

PERREG = []
def riassumi(tutte, contatti, regate, nerr):
    N = len(tutte); fuori = [o for o in tutte if abs(o["x0"]) > 35]; ocs = [o for o in tutte if o["ocs0"]]
    tagli = [o["taglio"] for o in tutte if o["taglio"] is not None]; nonp = N - len(tagli)
    print(f"costanti {PAR or 'spento'}, {regate} regate, {N} partenze di avversari, errori pagina {nerr}")
    print(f"1. oltre l'estremità allo sparo: {len(fuori)} ({100*len(fuori)/N:.1f}%)   [a sinistra {sum(o['x0'] < -35 for o in fuori)}]")
    print(f"2. oltre la linea allo sparo (anticipate): {len(ocs)} ({100*len(ocs)/N:.1f}%)")
    print(f"3. taglio: mediana {statistics.median(tagli):.2f} s, media {statistics.mean(tagli):.2f} s, dopo 10 s {sum(t > 10 for t in tagli)}, non partite entro 60 s {nonp}")
    print(f"4. contatti fra -60 e +20 s: {contatti} ({contatti/regate:.3f} per regata)")
    print(f"5. riposizionamenti {sum(o['ripos'] for o in tutte)} (barche {sum(o['ripos'] > 0 for o in tutte)}), giri in poppa {sum(o['poppa'] for o in tutte)}")
    print(f"   x del taglio sotto -10: {sum(o['xTaglio'] is not None and o['xTaglio'] < -10 for o in tutte)} su {len(tagli)}")
    for reg in NOMI:
        g = [o for o in tutte if o["reg"] == reg]
        if not g: continue
        cr = sum(x[4] for x in PERREG if x[0] == reg); print(f"   {reg}: oltre l'estremità {sum(abs(o['x0']) > 35 for o in g)}, anticipate {sum(o['ocs0'] for o in g)}, dopo 10 s {sum((o['taglio'] or 99) > 10 for o in g)}, contatti {cr}")
if sys.argv[1] == "--riassumi":  # unisce i file salvati con SALVA (corse divise fra più processi)
    T, C, Rg, E = [], 0, 0, 0
    for f in sys.argv[2:]: d = json.loads(pathlib.Path(f).read_text()); T += d["tutte"]; C += d["contatti"]; Rg += d["regate"]; E += d["errori"]; PERREG += d.get("perRegata", [])
    PAR = "vedi file"; riassumi(T, C, Rg, E)
else: asyncio.run(main())
