# Boe dal lato sbagliato della guida automatica (23 ottobre 2026, analisi dei 7 casi della 1.0.46; docs/STATO.md, «Aperto»). Non è un collaudo: nessuna soglia.
# Rigioca le corse come esplora.py (stessa pagina con #collaudo, stesso seme, giocatore guidato da __sv.pilota, che usa la guida degli avversari
# principianti) e per ogni boa sbagliata stampa gli eventi dei 25 s prima (contatti, scuffie, piantate) e la traccia: tempo, distanza dalla boa,
# angolo dalla boa rispetto al vento (0 = sopravento alla boa; il giro giusto passa da + a -), prua, nodi.
# Uso: python misura_boe.py CARTELLA_DEL_GIOCO '[[seme, regata, "principianti"|"esperti"], ...]'
#   es. python tests/misura_boe.py . '[[12, 1, "esperti"], [20, 0, "esperti"]]'
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(sys.argv[1]).resolve(); CASI = json.loads(sys.argv[2])
src = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text()
SEME = src.split('SEME = """')[1].split('"""')[0]
CORSA = """([race, seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]);
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], dt = 1 / 60, mk = R.mark, ev = [];
  let prev = Object.assign({}, sv.reg), n = 0, track = [];
  const where = () => { const s = me.S, d = Math.hypot(s.x - mk.x, s.y - mk.y);
    const a = ((Math.atan2(s.x - mk.x, -(s.y - mk.y)) * 180 / Math.PI - mk.out) % 360 + 540) % 360 - 180;
    return { t: +R.t.toFixed(2), d: +d.toFixed(1), ang: Math.round(a), h: Math.round(s.h), u: +(s.u * 1.944).toFixed(1), leg: me.leg, cap: !!s.capsized }; };
  while (me.fin === null && !me.dnf && R.t < 900){
    sv.pilota(dt); sv.run(dt, 1); n++;
    const r = sv.reg;
    for (const k of ["contacts", "wrongMarks", "capsizes", "irons"]) if (r[k] !== prev[k]) ev.push(Object.assign({ ev: k }, where()));
    prev = Object.assign({}, r);
    if (n % 30 === 0) track.push(where());
  }
  // per ogni boa sbagliata: la traccia dei 20 s prima e 5 s dopo
  const out = ev.filter(e => e.ev === "wrongMarks").map(w => ({ boa: w, prima: ev.filter(e => e.t > w.t - 25 && e.t < w.t + 5 && e !== w), traccia: track.filter(p => p.t > w.t - 20 && p.t < w.t + 6) }));
  return { arrivo: me.fin, mkout: mk.out, nEv: ev.length, eventi: ev.length, casi: out, contattiTot: ev.filter(e => e.ev === "contacts").length };
}"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        for seme, race, liv in CASI:
            pg = await b.new_page(); await pg.add_init_script(SEME)
            await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
            r = await pg.evaluate(CORSA, [race, seme, liv]); print(json.dumps({"seme": seme, "race": race, "liv": liv, **r}, ensure_ascii=False)); await pg.close()
        await b.close()
asyncio.run(main())
