# Frecce del vento in moviola (1.3.69, domanda di Ale del 27 nov 2026): a moviola aperta le frecce del vento reale e apparente sulla barca del giocatore
# devono essere quelle dell'istante rivisto, non dell'ultimo prima di «Rivedi». Regata del torneo col pilota; ogni secondo dopo il via si confronta il vento
# vero (local, info) con quello ricostruito in moviola (rotVentoMoviola). Soglie scritte prima di misurare: reale entro 2° e apparente entro 5° (la moviola
# non tiene lo scarroccio) nel 95% dei secondi; più di 30 secondi misurati; più di una direzione vista; null a moviola chiusa. Uso: collaudo_frecce_moviola.py [semi=6]
import asyncio, pathlib, sys, os
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = open(ROOT / "tests/collaudo_moviola.py").read(); SEME = src.split('SEME = """')[1].split('"""')[0]
RUN = """async (seme) => {
  const sv = __sv, dt = 1 / 60; sv.simTime = 0; __seed(seme);
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], vero = []; let n = 0;
  while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); n++;
    if (n % 60 === 0) vero.push([R.t, local.twd, local.tws, info.awFrom, info.aws, me.S.u, me.S.vl, me.cop || 0]); }
  racePanel(); const chiusa = rotVentoMoviola(0, 0, 0, 0); rivApri();
  const d = (a, b) => Math.abs(((a - b + 540) % 360) - 180); let eT = [], eA = [], tw = new Set();
  const big = []; for (const [t, twd, tws, awf, aws, u, vl, cop] of vero){ if (t < 0) continue; riv.pos = rivPosDi(t); rivApplica(); const S0 = R.boats[0].S, m = rotVentoMoviola(S0.x, S0.y, S0.h, S0.u);
    if (!m) return { errore: "null a moviola aperta" }; eT.push(d(m.tw.twd, twd)); eA.push(d(m.aw.awFrom, awf)); if (d(m.aw.awFrom, awf) > 5) big.push([Math.round(t), +d(m.aw.awFrom, awf).toFixed(1), +u.toFixed(2), +vl.toFixed(2), +(tws - m.tw.tws).toFixed(2), +cop.toFixed(2)]); tw.add(Math.round(m.tw.twd)); }
  rivChiudi(); const dopo = rotVentoMoviola(0, 0, 0, 0);
  const q = (a, p) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(p * (s.length - 1))]; };
  return { n: eT.length, chiusa: chiusa === null, dopo: dopo === null, t95: q(eT, .95), tmax: Math.max(...eT), a95: q(eA, .95), amax: Math.max(...eA), direzioni: tw.size, big: big.length, vivo: new Set(vero.filter(v => v[0] >= 0).map(v => Math.round(v[1]))).size };
}"""
async def main():
    br = os.environ.get("BROWSER", "chromium"); ko = False
    async with async_playwright() as p:
        b = await getattr(p, br).launch()
        for seme in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 7):
            pg = await b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(SEME); await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(200)
            await pg.evaluate("() => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }")
            r = await pg.evaluate(RUN, 7000 + seme); r["errori"] = errs[:1]; print(br, "seme", seme, r, flush=True)
            ok = r.get("n", 0) > 30 and r["chiusa"] and r["dopo"] and r["t95"] <= 2 and r["a95"] <= 5 and r["direzioni"] > 1 and not errs
            ko |= not ok; await pg.close()
        await b.close()
    print("ESITO", br, "FALLITO" if ko else "OK"); sys.exit(1 if ko else 0)
asyncio.run(main())
