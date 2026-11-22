# Fattore di raffica del gioco con il metro delle stazioni NOAA (voce 78, docs/PROPOSTA-RAFFICHE-VERE.md; criteri G1-G3 scritti prima). Non cambia il gioco.
# Regate lunghe del torneo col pilota (una per seme, pagina nuova, apertura e corsa in un evaluate). Dal via all'arrivo del giocatore, ogni 0,5 s il vento (windAt) su 16 punti fissi
# del campo (griglia 4x4 fra la linea e la boa, 200 m per lato) e sulla barca del giocatore. Per ogni intervallo di 2 minuti (come le stazioni costiere) e di 8 minuti (come la boa):
# vento medio e picco della media mobile di 5 s (10 letture); fattore = picco / medio. Il dato del mare (2023) si calcola dai file NDBC con --mare cartella.
# Uso: python tests/misura_raffiche_vere.py SEME_DA SEME_A    oppure    python tests/misura_raffiche_vere.py --mare cartella_con_i_file_h2023
import asyncio, gzip, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
def q(v, p): v = sorted(v); return v[min(len(v) - 1, int(p * len(v)))]
def riga(nome, G): return f"{nome}: casi {len(G)}; fattore 25° {q(G, .25):.2f}, mediana {statistics.median(G):.2f}, 75° {q(G, .75):.2f}, 90° {q(G, .90):.2f}, 99° {q(G, .99):.2f}, massimo {max(G):.2f}"
CORSA = """async (seme) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true; sv.opt.coachReg = false;
  semina(); sv.torApri(); document.getElementById('torGo').click(); sv.rot.spento = true; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, me = R.boats[0], dt = 1 / 60; R.tor = false; let acc = 0;
  const P = []; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) P.push(fromWF(-150 + i * 100, -R.up * (0.15 + 0.7 * j / 3)));
  const L = P.map(() => []), B = [];
  while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1);
    if (R.t >= 0 && (acc += dt) >= 0.5){ acc = 0; P.forEach(([x, y], k) => L[k].push(windAt(x, y).tws)); B.push(windAt(me.S.x, me.S.y).tws); } }
  return { seme, up: R.up, serie: L.concat([B]) }; }"""
def fattori(serie, n):   # n letture per intervallo (0,5 s ciascuna)
    out = []
    for s in serie:
        for a in range(0, len(s) - n + 1, n):
            w = s[a:a + n]; m = sum(w) / n
            mob = [sum(w[i:i + 10]) / 10 for i in range(0, n - 9)]
            out.append(max(mob) / m)
    return out
async def corri(a, b):
    async with async_playwright() as p:
        br = await getattr(p, BR).launch(); F2 = []; F8 = []; errs = []
        for seme in range(a, b):
            ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
            r = await pg.evaluate(CORSA, seme); await ctx.close()
            F2 += fattori(r["serie"], 240); F8 += fattori(r["serie"], 960)
        await br.close()
    print(riga("gioco, intervalli di 2 minuti", F2)); print(riga("gioco, intervalli di 8 minuti", F8)); print(f"errori della pagina {errs[:1]}")
def mare(cart):
    for s in ("buzm3", "dbln6", "44005"):
        G = []
        for l in gzip.open(pathlib.Path(cart, f"{s}h2023.txt.gz"), "rt"):
            if l.startswith("#"): continue
            p = l.split(); w = float(p[6]); g = float(p[7])
            if w >= 99 or g >= 99 or w <= 0: continue
            if 10 <= w * 1.943844 <= 14: G.append(g / w)
        print(riga(f"mare {s} ({'8 minuti' if s[0].isdigit() else '2 minuti'})", G))
if __name__ == "__main__":
    if sys.argv[1] == "--mare": mare(sys.argv[2])
    else: asyncio.run(corri(int(sys.argv[1]), int(sys.argv[2])))
