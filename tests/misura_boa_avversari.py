# Misura della proposta docs/PROPOSTA-BOA-PIANTATA.md (9 novembre 2026). Non è un collaudo: stampa i numeri dei criteri.
# Regate del torneo (bastone e triangolo per 10 nodi costanti, raffiche, salti di vento; vento (seme % 8) x 45°), principianti ed esperti,
# preparazione 60 s, il giocatore guidato dal pilota (usa la guida degli avversari, come in misura_triangolo.py), fino all'arrivo di tutti
# o a 900 s. Per ogni avversario e ogni boa, mentre la punta ed è entro 40 m: secondi, virate, fermate (3 s di fila sotto 1 nodo),
# boa toccata (scafo a meno del raggio della boa, 0,9 m). Per la regata: contatti dopo il via, boe sbagliate, non arrivate, tempi.
# Uso: python tests/misura_boa_avversari.py PRIMO ULTIMO [PASSO_M SOPRA_M [M_DIR R_DIR]]  (senza costanti: quelle del gioco; M_DIR negativo = giro diretto spento); DIAG=1 annota dove avvengono le fermate
#   SALVA=file.json per più processi, poi --riassumi f1.json f2.json ...
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
CORSA = """([k, reg, liv, seme, par]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  if (sv.lay) sv.lay(LAYMARG); // 1.2.23 (PROPOSTA-LAYLINE): LAYMARG=gradi nell'ambiente, assente = spento
  if (sv.boa) sv.boa(par ? par[0] : null, par ? par[1] : null, par && par.length > 2 ? par[2] : null, par && par.length > 3 ? par[3] : null);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { ...reg, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60, KN = 0.5144, DIAG = DIAGNOSI; R.tor = false; // senza finestra d'arrivo: si misura fino all'arrivo
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
        if (b.S.u < KN){ o.lento += dt; if (o.lento >= 3 && o.lento - dt < 3){ o.ferme++;
          if (DIAG){ const th = -((seme % 8) * 45) * Math.PI / 180, ex = b.S.x - m.x, ey = b.S.y - m.y, wx = ex * Math.cos(th) - ey * Math.sin(th), wy = ex * Math.sin(th) + ey * Math.cos(th), vic = R.boats.filter(q => q !== b).map(q => Math.hypot(q.S.x - b.S.x, q.S.y - b.S.y));
            (o.dove = o.dove || []).push({ t: +R.t.toFixed(1), dx: +wx.toFixed(1), dy: +wy.toFixed(1), rp: b.rp || 0, cede: b.cedeA ? b.cedeA.name : null, sconta: !!b.sconta, vicina: +Math.min(...vic).toFixed(1) }); } } o.maxFermo = Math.max(o.maxFermo, o.lento); } else o.lento = 0;
        if (dHull(b, m) < 0.9) o.tocco = true;
      }
      vir[b.name] = b.virando;
    }
  }
  return { boe: Object.values(boe).map(o => ({ ...o, sec: +o.sec.toFixed(1), maxFermo: +o.maxFermo.toFixed(1) })), contatti,
           barche: ai.map(b => ({ nome: b.name, fin: b.fin, dnf: !!b.dnf, dsq: !!b.dsq, sbagliate: b.wrongMarks || 0 })), giri: !!R.giri, t: Math.round(R.t) };
}"""
NOMI = {(k, c): f"{'bastone' if k == 0 else 'triangolo'}-{['costante', 'raffiche', 'salti'][c]}" for k in (0, 1) for c in (0, 1, 2)}
# Senza TORNEO=nuovo il torneo a condizioni con un nome (fino alla 1.2.20: con RADICE= su una copia di allora); dalla 1.2.21 il torneo è quello nuovo e serve TORNEO=nuovo.
# TORNEO=nuovo (1.2.21, docs/PROPOSTA-TORNEO-AMPLIATO.md §4): le 4 regate del torneo ampliato (vento misto, 10 o 12 nodi secondo il seme), più le regate 3 e 4
# senza giri (col punteggio) per il confronto della durata (T3)
NUOVO = {(0, None): "R1-bastone-punti", (1, None): "R2-triangolo-punti", (2, None): "R3-bastone-giri", (3, None): "R4-triangolo-giri",
         (2, False): "R3-bastone-senza-giri", (3, False): "R4-triangolo-senza-giri"}

async def main(A, B, PAR):
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        tutte = []
        nuovo = os.environ.get("TORNEO") == "nuovo"
        for (k, c), nome in (NUOVO if nuovo else NOMI).items():
            for liv in ("principianti", "esperti"):
                for seme in range(A, B + 1):
                    reg = ({"tws": 12 if seme % 2 else 10} | ({} if c is None else {"giri": c})) if nuovo else {"c": c}
                    r = await pg.evaluate(CORSA.replace("DIAGNOSI", "true" if os.environ.get("DIAG") else "false").replace("LAYMARG", os.environ.get("LAYMARG") or "null"), [k, reg, liv, seme, PAR])
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
    print(f"G6 contatti dopo il via: {sum(r['contatti'] for r in R)}  ({sum(r['contatti'] for r in R) / len(R):.3f} per regata; fermate per regata {sum(o['ferme'] for o in B) / len(R):.3f})")
    G = [r for r in R if r.get("giri")]
    if G:
        bg = [b for r in G for b in r["barche"]]
        print(f"T2 avversari squalificati nelle regate coi giri: {sum(b['dsq'] for b in bg)} su {len(bg)} ({sum(b['dsq'] for b in bg) / len(bg):.1%})")
    nomi = sorted({r["reg"] for r in R}, key=lambda n: [r["reg"] for r in R].index(n))
    for nome in nomi:
        fz = [b["fin"] for r in R if r["reg"] == nome for b in r["barche"] if b["fin"] is not None and not b.get("dsq")]
        if fz: print(f"   {nome}: arrivo mediano {statistics.median(fz):.1f} s, contatti per regata {statistics.mean(r['contatti'] for r in R if r['reg'] == nome):.3f}")
    for nome in NOMI.values():
        g = [o for r in R if r["reg"] == nome for o in r["boe"] if o["sec"] > 0]
        if g: print(f"   {nome}: fermate {sum(o['ferme'] for o in g)}, 3+ virate {sum(o['virate'] >= 3 for o in g)}, mediana {statistics.median(o['sec'] for o in g):.1f} s, toccate {sum(o['tocco'] for o in g)}, contatti {sum(r['contatti'] for r in R if r['reg'] == nome)}")
    D = [(o["boa"], x) for o in B for x in o.get("dove", [])]
    if D:
        print(f"   fermate annotate {len(D)} (dx, dy dalla boa nel riferimento del vento, y negativo = sopravento; rp punto puntato):")
        for j, x in D: print(f"     boa {j + 1} t {x['t']:6.1f}  dx {x['dx']:6.1f} dy {x['dy']:6.1f}  rp {x['rp']}  cede {x['cede']}  sconta {x['sconta']}  vicina {x['vicina']} m")
    for j in (0, 1):
        g = [o for o in B if o["boa"] == j]
        if g: print(f"   boa {j + 1}: passaggi {len(g)}, virate {sum(o['virate'] for o in g)}, fermate {sum(o['ferme'] for o in g)}, 3+ virate {sum(o['virate'] >= 3 for o in g)}, mediana {statistics.median(o['sec'] for o in g):.1f} s")

if sys.argv[1] == "--riassumi": riassumi([json.loads(pathlib.Path(f).read_text()) for f in sys.argv[2:]])
else: asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), [float(x) for x in sys.argv[3:7]] if len(sys.argv) > 4 else None))
