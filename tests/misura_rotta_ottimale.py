# Misura della rotta ottimale (1.2.22, docs/PROPOSTA-ROTTA-OTTIMALE.md §3, criteri S1-S4 e S6). Non è un collaudo: stampa i numeri dei criteri.
# Le 4 regate del torneo ampliato (vento con raffiche e salti, 10 o 12 nodi secondo il seme, vento (seme % 8) x 45°), principianti ed esperti,
# preparazione 60 s, giocatore guidato dal pilota, fino all'arrivo di tutti o a 900 s. A fine regata la rotta ottimale per OGNI barca dal suo taglio
# della linea, contro il suo arrivo vero:
#   S1 rotta ottimale <= tempo vero (eccezioni al massimo 1%, nessuna oltre 3 s), S2 vantaggio mediano sulla barca più veloce della regata <= 20%,
#   S3 vento ricostruito contro windAt nei punti delle barche ogni secondo (al massimo 0,05 nodi e 0,5°), S4 secondi di calcolo per rotta,
#   S6 (con --s6) stessa regata con la registrazione spenta: arrivi e posizioni finali identici al bit.
# Uso: python tests/misura_rotta_ottimale.py PRIMO ULTIMO [--s6]   (SALVA=file.json, poi --riassumi f1.json f2.json ...)
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
CORSA = """([k, liv, seme, spento]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { tws: seme % 2 ? 12 : 10, wind: (seme % 8) * 45 };
  sv.rot.spento = spento; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60; R.tor = false; // senza finestra d'arrivo
  let errV = 0, errD = 0, acc = 1, nV = 0;
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1);
    if (R.t >= 0 && !spento && (acc += dt) >= 1){ acc = 0; // S3: il vento ricostruito dalla registrazione contro quello del gioco, ogni secondo
      const Q = sv.rotRaffiche(R.t);
      for (const b of R.boats){ const a = sv.windAt(b.S.x, b.S.y), r = sv.ventoDa(Q.gs, Q.sd, Q.sim, b.S.x, b.S.y);
        errV = Math.max(errV, Math.abs(a.tws - r.tws) * 1.9438); errD = Math.max(errD, Math.abs(sv.norm180(a.twd - r.twd))); nV++; } }
  }
  const barche = R.boats.map((b, i) => ({ nome: b.name, fin: b.fin, dsq: !!b.dsq, x: b.S.x, y: b.S.y, h: b.S.h, taglio: sv.rot.barche[i] && sv.rot.barche[i].taglio ? sv.rot.barche[i].taglio.t : null }));
  const rotte = [];
  if (!spento) R.boats.forEach((b, i) => { const t0 = performance.now(), o = sv.rotCalcola(i), ms = performance.now() - t0;
    rotte.push(o ? { tempo: o.tempo, t0: o.t0, ms } : null); });
  let testo = null;
  if (!spento && R.boats[0].fin !== null){ const o = sv.rotCalcola(0); if (o) testo = sv.rotTesto(o, sv.rotSpiega(o)); }
  return { barche, rotte, errV, errD, nV, testo, t: R.t };
}"""

async def main(A, B, s6):
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        tutte = []; diverse = 0
        for k in range(4):
            for liv in ("principianti", "esperti"):
                for seme in range(A, B + 1):
                    r = await pg.evaluate(CORSA, [k, liv, seme, False]); r.update(reg=k, liv=liv, seme=seme); tutte.append(r)
                    if s6:
                        q = await pg.evaluate(CORSA, [k, liv, seme, True])
                        if [(b["fin"], b["x"], b["y"], b["h"]) for b in q["barche"]] != [(b["fin"], b["x"], b["y"], b["h"]) for b in r["barche"]]: diverse += 1
            print(f"  regata {k + 1} fatta", flush=True)
        await br.close()
    d = {"regate": tutte, "errori": len(errs) + (0 if not errs else 0), "msg_errori": errs[:3], "s6": [diverse, len(tutte) if s6 else 0]}
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(d))
    riassumi([d])

def riassumi(ds):
    R = [r for d in ds for r in d["regate"]]; E = sum(d["errori"] for d in ds)
    casi = []; manca = 0
    for r in R:
        veri = [b["fin"] - b["taglio"] for b in r["barche"] if b["fin"] is not None and not b["dsq"] and b["taglio"] is not None]
        for b, o in zip(r["barche"], r["rotte"]):
            if b["fin"] is None or b["dsq"] or b["taglio"] is None: continue
            if o is None: manca += 1; continue
            casi.append({"vero": b["fin"] - b["taglio"], "ott": o["tempo"] - o["t0"], "ms": o["ms"], "migliore": min(veri)})
    print(f"{len(R)} regate, {len(casi)} barche-regata con rotta ottimale (non calcolate {manca}), errori pagina {E} {ds[0].get('msg_errori')}")
    ecc = [c for c in casi if c["ott"] > c["vero"] + 1e-9]
    print(f"S1 rotta ottimale più lenta della barca vera: {len(ecc)} su {len(casi)} ({len(ecc) / max(1, len(casi)):.1%}); oltre 3 s: {sum(c['ott'] > c['vero'] + 3 for c in ecc)}"
          + (f"; peggiore +{max(c['ott'] - c['vero'] for c in ecc):.1f} s" if ecc else ""))
    reg = {}
    for c in casi: reg.setdefault((c["migliore"]), c["ott"])
    vant = [1 - c["ott"] / c["migliore"] for c in casi]
    print(f"S2 vantaggio sulla barca più veloce della regata: mediana {statistics.median(vant):.1%}, quartili {statistics.quantiles(vant, n=4)[0]:.1%} / {statistics.quantiles(vant, n=4)[2]:.1%}; sulla barca stessa: mediana {statistics.median([1 - c['ott'] / c['vero'] for c in casi]):.1%}")
    print(f"S3 vento ricostruito: scarto massimo {max(r['errV'] for r in R):.4f} nodi, {max(r['errD'] for r in R):.4f}°, su {sum(r['nV'] for r in R)} confronti")
    print(f"S4 calcolo: mediana {statistics.median(c['ms'] for c in casi):.0f} ms, massimo {max(c['ms'] for c in casi):.0f} ms per rotta")
    s6 = [sum(d["s6"][0] for d in ds), sum(d["s6"][1] for d in ds)]
    if s6[1]: print(f"S6 regate diverse con la registrazione spenta: {s6[0]} su {s6[1]}")
    for r in R[:3]:
        if r["testo"]: print("   esempio:", r["testo"])

if sys.argv[1] == "--riassumi": riassumi([json.loads(pathlib.Path(f).read_text()) for f in sys.argv[2:]])
else: asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), "--s6" in sys.argv))
