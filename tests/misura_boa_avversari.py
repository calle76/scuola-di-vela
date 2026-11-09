# Misura della proposta docs/PROPOSTA-BOA-PIANTATA.md (9 novembre 2026). Non è un collaudo: stampa i numeri dei criteri.
# Regate del torneo (bastone e triangolo per 10 nodi costanti, raffiche, salti di vento; vento (seme % 8) x 45°), principianti ed esperti,
# preparazione 60 s, il giocatore guidato dal pilota (usa la guida degli avversari, come in misura_triangolo.py), fino all'arrivo di tutti
# o a 900 s. Per ogni avversario e ogni boa, mentre la punta ed è entro 40 m: secondi, virate, fermate (3 s di fila sotto 1 nodo),
# boa toccata (scafo a meno del raggio della boa, 0,9 m). Per la regata: contatti dopo il via, boe sbagliate, non arrivate, tempi.
# Uso: python tests/misura_boa_avversari.py PRIMO ULTIMO [PASSO_M SOPRA_M]  (senza costanti: quelle del gioco)
#   SALVA=file.json per più processi, poi --riassumi f1.json f2.json ...
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
CORSA = """([k, c, liv, seme, par]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  if (sv.boa) sv.boa(par ? par[0] : null, par ? par[1] : null);
  if (sv.ripos) sv.ripos(null);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; if (k) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { c, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60, KN = 0.5144; R.tor = false; // senza finestra d'arrivo: si misura fino all'arrivo
  const ai = R.boats.filter(b => !b.me), boe = {};
  const dHull = (b, m) => { const P = sv.hullWorld(b.S); let dentro = true, best = 1e9;
    for (let i = 0; i < P.length; i++){ const [x0, y0] = P[i], [x1, y1] = P[(i + 1) % P.length], ex = x1 - x0, ey = y1 - y0, l2 = ex * ex + ey * ey;
      if (ex * (m.y - y0) - ey * (m.x - x0) < 0) dentro = false;
      const t = l2 > 1e-12 ? Math.max(0, Math.min(1, ((m.x - x0) * ex + (m.y - y0) * ey) / l2)) : 0; best = Math.min(best, Math.hypot(m.x - x0 - t * ex, m.y - y0 - t * ey)); }
    return dentro ? 0 : best; };
  for (const b of ai) for (let j = 0; j < R.marks.length; j++) boe[b.name + j] = { nome: b.name, boa: j, sec: 0, virate: 0, ferme: 0, lento: 0, tocco: false, maxFermo: 0 };
  const vir = {}; let nPen = R.penList.length, contatti = 0;
  while (R.t < 900 && R.boats.some(b => !b.me && b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1);
    if (R.penList.length > nPen){ for (let q = nPen; q < R.penList.length; q++) if (/contatto/.test(R.penList[q]) && R.t > 0) contatti++; nPen = R.penList.length; }
    if (R.t < 0) continue;
    for (const b of ai){
      const j = b.leg - 1; if (j < 0 || j >= R.marks.length || b.fin !== null) { vir[b.name] = b.virando; continue; }
      const m = R.marks[j], o = boe[b.name + j];
      if (Math.hypot(b.S.x - m.x, b.S.y - m.y) < 40){
        o.sec += dt; if (b.virando && !vir[b.name]) o.virate++;
        if (b.S.u < KN){ o.lento += dt; if (o.lento >= 3 && o.lento - dt < 3) o.ferme++; o.maxFermo = Math.max(o.maxFermo, o.lento); } else o.lento = 0;
        if (dHull(b, m) < 0.9) o.tocco = true;
      }
      vir[b.name] = b.virando;
    }
  }
  return { boe: Object.values(boe).map(o => ({ ...o, sec: +o.sec.toFixed(1), maxFermo: +o.maxFermo.toFixed(1) })), contatti,
           barche: ai.map(b => ({ nome: b.name, fin: b.fin, dnf: !!b.dnf, sbagliate: b.wrongMarks || 0 })), t: Math.round(R.t) };
}"""
NOMI = {(k, c): f"{'bastone' if k == 0 else 'triangolo'}-{['costante', 'raffiche', 'salti'][c]}" for k in (0, 1) for c in (0, 1, 2)}

async def main(A, B, PAR):
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        tutte = []
        for (k, c), nome in NOMI.items():
            for liv in ("principianti", "esperti"):
                for seme in range(A, B + 1):
                    r = await pg.evaluate(CORSA, [k, c, liv, seme, PAR])
                    r.update(reg=nome, liv=liv, seme=seme); tutte.append(r)
            print(f"  {nome} fatta", flush=True)
        await br.close()
    d = {"regate": tutte, "errori": len(errs), "par": PAR}
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(d))
    riassumi([d])

def riassumi(ds):
    R = [r for d in ds for r in d["regate"]]; E = sum(d["errori"] for d in ds); par = ds[0]["par"]
    B = [o for r in R for o in r["boe"] if o["sec"] > 0]; ba = [b for r in R for b in r["barche"]]
    print(f"costanti {par or 'del gioco'}, {len(R)} regate, {len(B)} passaggi di avversari entro 40 m da una boa, errori pagina {E}")
    print(f"G1 fermate (3 s sotto 1 nodo entro 40 m): {sum(o['ferme'] for o in B)}  (passaggi con almeno una: {sum(o['ferme'] > 0 for o in B)}, fermata più lunga {max(o['maxFermo'] for o in B):.1f} s)")
    print(f"G2 passaggi con 3 o più virate entro 40 m: {sum(o['virate'] >= 3 for o in B)}  (virate in tutto {sum(o['virate'] for o in B)})")
    print(f"G3 secondi entro 40 m: mediana {statistics.median(o['sec'] for o in B):.1f}, media {statistics.mean(o['sec'] for o in B):.1f}, oltre 60 s {sum(o['sec'] > 60 for o in B)}")
    print(f"G4 boa toccata: {sum(o['tocco'] for o in B)}")
    fin = [b["fin"] for b in ba if b["fin"] is not None]
    print(f"G5 boe sbagliate {sum(b['sbagliate'] for b in ba)}, non arrivate {sum(b['fin'] is None for b in ba)} su {len(ba)}, arrivo mediano {statistics.median(fin):.1f} s")
    print(f"G6 contatti dopo il via: {sum(r['contatti'] for r in R)}")
    for nome in NOMI.values():
        g = [o for r in R if r["reg"] == nome for o in r["boe"] if o["sec"] > 0]
        if g: print(f"   {nome}: fermate {sum(o['ferme'] for o in g)}, 3+ virate {sum(o['virate'] >= 3 for o in g)}, mediana {statistics.median(o['sec'] for o in g):.1f} s, toccate {sum(o['tocco'] for o in g)}, contatti {sum(r['contatti'] for r in R if r['reg'] == nome)}")
    for j in (0, 1):
        g = [o for o in B if o["boa"] == j]
        if g: print(f"   boa {j + 1}: passaggi {len(g)}, fermate {sum(o['ferme'] for o in g)}, 3+ virate {sum(o['virate'] >= 3 for o in g)}, mediana {statistics.median(o['sec'] for o in g):.1f} s")

if sys.argv[1] == "--riassumi": riassumi([json.loads(pathlib.Path(f).read_text()) for f in sys.argv[2:]])
else: asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), [float(sys.argv[3]), float(sys.argv[4])] if len(sys.argv) > 4 else None))
