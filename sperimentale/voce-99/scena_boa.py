# Voce 99 (b), oss. 155: un rivale appena sotto e a sinistra della boa di bolina (come la Blu al 392 s della regata 28/11 14:34, 3,6 m a sinistra e 2,5 m sotto,
# mure a dritta a 58° dal vento, 4,7 nodi), solo in acqua: quanto ci mette a contare il giro della boa e se passa dal punto 2 (14 m sotto la boa).
# Regata nei salti senza salti (come collaudo_avversari1b), il giocatore a 5 km. Varianti col seme: dx da -2 a -6 m, dy da 1 a 4 m sotto, prua 48-68° dal vento.
# Uso: python sperimentale/voce-99/scena_boa.py [--varianti 0-19]   (BROWSER=firefox; RADICE=cartella per una copia del gioco)
import asyncio, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ["RADICE"]).resolve() if os.environ.get("RADICE") else pathlib.Path(__file__).resolve().parents[2]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
a, b_ = arg("--varianti", "0-19").split("-"); VAR = range(int(a), int(b_) + 1)
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
SCENA = """(v) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 2]); __seed(5000 + v); sv.setShifts(null); sv.simTime = 0;
  const R = sv.R, D = Math.PI / 180, me = R.boats[0], av = R.boats.filter(b => !b.me), twd = sv.windAt(0, 0).twd, rnd = Math.random;
  R.t = 120; R.phase = "race"; me.S.x += 5000; me.S.y += 5000;
  const dx = -2 - 4 * rnd(), dy = 1 + 3 * rnd(), a = 48 + 20 * rnd();
  const [mx, my] = toWF(R.mark.x, R.mark.y), [x, y] = fromWF(mx + dx, my + dy), B = av[0];
  const put = (b, x, y, h, u) => { Object.assign(b.S, { x, y, h: (h + 360) % 360, u, r: 0, heel: 0, capsized: false });
    Object.assign(b, { leg: 1, ocs: false, goStart: true, fin: null, dnf: false, rnd: 0, rp: 0, p2: false, diretto: false, side: Math.sign(((twd - h) % 360 + 540) % 360 - 180), boardT: 0, boardMax: 999, virando: false });
    b.ctl.sheet = 0.15; b.ctl.tiller = 0; };
  put(B, x, y, twd - a, 2.4); av.slice(1).forEach((b, k) => put(b, me.S.x + 300 + 100 * k, me.S.y, twd - 50, 0));
  const dt = 1 / 60; let giro = null, p2 = false, sotto = 0, pen0 = R.penList.length;
  for (let n = 0; n * dt < 90 && giro === null; n++){
    sv.run(dt, 1);
    if (B.rp === 2) p2 = true;
    sotto = Math.max(sotto, toWF(B.S.x, B.S.y)[1] - my);
    if (B.leg === 2) giro = n * dt;
  }
  return { dx: +dx.toFixed(1), dy: +dy.toFixed(1), a: Math.round(a), giro: giro === null ? null : +giro.toFixed(1), p2, sotto: +sotto.toFixed(1), pen: R.penList.slice(pen0) };
}"""
async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []; tempi = []; mai = 0; n2 = 0
        for v in VAR:
            pg = await br.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME)
            await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
            r = await pg.evaluate(SCENA, v); await pg.close()
            print(f"variante {v}: {r['dx']} m di lato, {r['dy']} m sotto, {r['a']}° dal vento: giro a {r['giro']} s, punto 2 {'sì' if r['p2'] else 'no'}, fino a {r['sotto']} m sotto la boa {r['pen'][:1]}", flush=True)
            if r["giro"] is None: mai += 1
            else: tempi.append(r["giro"])
            n2 += r["p2"]
        print(f"varianti {len(VAR)}: giro mediano {statistics.median(tempi) if tempi else None} s, massimo {max(tempi) if tempi else None} s, mai girata entro 90 s {mai}, passate dal punto 2 {n2}; errori pagina {errs[:3]}")
        await br.close()
asyncio.run(main())
