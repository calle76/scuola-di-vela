# Misura degli avversari (26 ottobre 2026, base per la fermata 1 di «avversari con la barca dell'1b»). Non è un collaudo: nessuna soglia.
# Stessa pagina e stesso giocatore di misura_boe.py (#collaudo, seme fisso, giocatore guidato da __sv.pilota). Per ogni avversario conta:
#   piantate: dopo il via e prima dell'arrivo, almeno 5 s di fila sotto 0,5 nodi (non scuffiato); per ognuna se c'era una barca entro 22 m
#     e chi doveva cedere secondo chiCede (lui o l'altra): «cede senza dovere» = si pianta vicino a una barca che doveva cedere a lui;
#   ferme alla boa: secondi nel tratto 1 entro 30 m dalla boa (più di 60 s = «ferma alla boa»);
#   boe sbagliate, partenze fuori (ocs dopo il via), contatti fra avversari (penalità prese), non arrivati entro 900 s;
#   strambate: perdita di velocità nei 6 s dopo il cambio di mure in poppa (mediana e massimo).
# Uso: python tests/misura_avversari.py PRIMO_SEME ULTIMO_SEME [regate, es. 0,2]   (0 = bastone 1a, 1 = raffiche 1a, 2 = salti di vento 1b)
import asyncio, json, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
S0, S1 = int(sys.argv[1]), int(sys.argv[2]); REG = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "0,2").split(",")]
src = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text()
SEME = src.split('SEME = """')[1].split('"""')[0]
CORSA = """([race, seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]);
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, dt = 1 / 60, KN = 1.944, mk = R.mark, av = R.boats.filter(b => !b.me);
  const st = av.map(b => ({ nome: b.name, car: b.char, lento: 0, piantate: [], boaT: 0, ocs: false, pen0: (b.pen || 0) + (b.pp || 0) * 15,
                             tack: 0, gybe: [], gyU: null, gyT: 0 }));
  let n = 0; const penDove = [];
  const tackOf = b => Math.sign(((sv.windAt(b.S.x, b.S.y).twd - b.S.h) % 360 + 540) % 360 - 180);
  while (R.t < 900 && av.some(b => b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1); n++;
    while (penDove.length < (R.penList || []).length){ // dove e quando avviene ogni penalità: tratto, distanza dalla boa, attesa del via
      const txt = R.penList[penDove.length], nome = txt.startsWith("Tu,") ? null : txt.split(",")[0].replace("La ", ""), g = R.boats.find(b => nome ? b.name === nome : b.me);
      penDove.push({ t: +R.t.toFixed(1), leg: g.leg, dBoa: Math.round(Math.hypot(g.S.x - mk.x, g.S.y - mk.y)), regola: +(txt.match(/regola (\d+)/) || [0, 0])[1], g: nome || "Tu" });
    }
    av.forEach((b, i) => { const s = b.S, q = st[i];
      if (b.fin !== null || b.dnf || R.t < 0){ q.lento = 0; return; }
      if (b.ocs) q.ocs = true;
      const kn = s.u * KN, tk = tackOf(b), A = Math.abs(((sv.windAt(s.x, s.y).twd - s.h) % 360 + 540) % 360 - 180);
      // strambata: cambio di mure con vento in poppa (oltre 120°); velocità minima nei 6 s dopo rispetto a quella prima
      if (q.tack && tk && tk !== q.tack && A > 120 && !s.capsized){ q.gyU = { prima: kn, min: kn }; q.gyT = 6; }
      if (q.gyT > 0){ q.gyU.min = Math.min(q.gyU.min, kn); q.gyT -= dt; if (q.gyT <= 0) q.gybe.push(+(1 - q.gyU.min / Math.max(q.gyU.prima, 0.1)).toFixed(2)); }
      if (tk) q.tack = tk;
      if (b.leg === 1 && Math.hypot(s.x - mk.x, s.y - mk.y) < 30) q.boaT += dt;
      if (!s.capsized && kn < 0.5){
        q.lento += dt;
        if (q.lento >= 5 && q.lento - dt < 5){ // inizio di una piantata: chi c'era vicino e chi doveva cedere
          let o = null, d = 1e9; for (const x of R.boats){ if (x === b || x.fin !== null) continue; const dd = Math.hypot(x.S.x - s.x, x.S.y - s.y); if (dd < d){ d = dd; o = x; } }
          const vic = o && d < 22 ? { con: o.name, d: +d.toFixed(1), cede: sv.chiCede(b, o).cede === b ? "lui" : "l'altra" } : null;
          q.piantate.push({ t: +R.t.toFixed(1), leg: b.leg, dBoa: +Math.hypot(s.x - mk.x, s.y - mk.y).toFixed(0), twa: Math.round(A), vic });
        }
      } else q.lento = 0;
    });
  }
  return { tFine: +R.t.toFixed(0), penList: R.penList || [], penDove, barche: av.map((b, i) => { const q = st[i];
    return { nome: q.nome, car: q.car, arrivo: b.fin === null ? null : +b.fin.toFixed(0), boeSbagliate: b.wrongMarks || 0, ocs: q.ocs,
             penalita: Math.round(((b.pen || 0) + (b.pp || 0) * 15 - q.pen0) / 15), boaT: Math.round(q.boaT), piantate: q.piantate, strambate: q.gybe }; }) };
}"""
ALTRA = "l'altra"
async def main():
    righe = []
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        for race in REG:
            for liv in ("principianti", "esperti"):
                for seme in range(S0, S1 + 1):
                    pg = await b.new_page(); await pg.add_init_script(SEME)
                    await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                    r = await pg.evaluate(CORSA, [race, seme, liv]); await pg.close()
                    r.update(race=race, liv=liv, seme=seme); righe.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        await b.close()
    print("\n== riepilogo (semi %d-%d)" % (S0, S1))
    for race in REG:
        for liv in ("principianti", "esperti"):
            bs = [x for r in righe if r["race"] == race and r["liv"] == liv for x in r["barche"]]
            pi = [p for x in bs for p in x["piantate"]]
            gy = [g for x in bs for g in x["strambate"]]
            print(f"regata {race}, {liv}: barche {len(bs)} | non arrivate {sum(x['arrivo'] is None for x in bs)} | boe sbagliate {sum(x['boeSbagliate'] for x in bs)}"
                  f" | ocs dopo il via {sum(x['ocs'] for x in bs)} | penalità {sum(x['penalita'] for x in bs)} | ferme alla boa >60 s {sum(x['boaT'] > 60 for x in bs)}"
                  f" | piantate {len(pi)} (barche con almeno una {sum(bool(x['piantate']) for x in bs)}; vicino a una barca {sum(p['vic'] is not None for p in pi)},"
                  f" di cui cede senza dovere {sum(bool(p['vic']) and p['vic']['cede'] == ALTRA for p in pi)})"
                  f" | strambate {len(gy)}, perdita mediana {statistics.median(gy) if gy else '-'}, massima {max(gy) if gy else '-'}")
asyncio.run(main())
