# Voce 73 (21 nov 2026): le virate del giocatore guidato dal pilota, nelle regate del torneo (bastone, 12 nodi, avversari principianti).
# Per ogni virata sul lato di bolina (leg 1, dopo il via, ad almeno 40 m dalla boa e dai 25 s dal via): nodi 3-1 s prima (media), minimo nei 10 s dopo,
# nodi 8 s dopo, secondi per tornare al 90% della velocita' di prima (max 15), scuffie. Stampa le medie per condizione e per seme (numeri come escono, nessuna soglia).
# Uso: misura_virate_giocatore.py ETICHETTA [lungo] [semi_da semi_a]   (GIOCO=cartella con index.html per una versione vecchia)
import asyncio, os, pathlib, sys, statistics as st
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = pathlib.Path(os.environ.get("GIOCO", ROOT / "index.html")).as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
RUN = """([seme, lungo]) => {
  const sv = __sv; sv.fast(0); __seed(seme); sv.simTime = 0; if (lungo) sv.lungo = true;
  const sel = document.getElementById("aiLevel"); sel.value = "principianti"; sel.dispatchEvent(new Event("change"));
  sv.torApri(); document.getElementById("torGo").click();
  sv.tor.regate[0] = { tws: 12, wind: (seme % 8) * 45 }; __seed(seme); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, me = R.boats[0], dt = 1 / 60, kn = 1.943844, hist = [], vir = []; let lastSign = 0, scuffie = 0, wasCap = false;
  while (R.t < 1500 && me.fin === null && R.t < 700){
    sv.pilota(dt); sv.run(dt, 1);
    if (me.S.capsized && !wasCap) scuffie++; wasCap = me.S.capsized;
    if (R.t < 0 || !me.info) continue;
    hist.push([R.t, me.S.u * kn]);
    const sg = Math.sign(me.info.twa || 0);
    if (sg && lastSign && sg !== lastSign && me.leg === 1 && R.t > 25 && Math.hypot(me.S.x - R.mark.x, me.S.y - R.mark.y) > 40) vir.push(R.t);
    if (sg) lastSign = sg;
  }
  const at = t => { let b = hist[0]; for (const h of hist){ if (h[0] > t) break; b = h; } return b[1]; };
  const out = vir.filter(t => t > 4 && t + 15 < R.t).map(t => { const n = 20, pre = []; for (let i = 0; i < n; i++) pre.push(at(t - 3 + 2 * i / n));
    const a = pre.reduce((x, y) => x + y, 0) / n; let mn = 99, rit = 15; for (const h of hist) if (h[0] >= t && h[0] <= t + 10) mn = Math.min(mn, h[1]);
    for (const h of hist) if (h[0] >= t + 1 && h[0] <= t + 15 && h[1] >= 0.9 * a){ rit = h[0] - t; break; }
    return [a, mn, at(t + 8), rit]; });
  return { out, scuffie, T: R.t, fin: me.fin }; }"""
async def main():
    et = sys.argv[1]; lungo = len(sys.argv) > 2 and sys.argv[2] == "lungo"; arg = [int(x) for x in sys.argv[2 + lungo:]]
    a, b = (arg + [1, 10])[:2]; tutte = []; sc = 0
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for seme in range(a, b + 1):
            ctx = await br.new_context(viewport={"width": 1280, "height": 800}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
            r = await pg.evaluate(RUN, [seme, lungo]); await ctx.close()
            tutte += r["out"]; sc += r["scuffie"]
            m = lambda i: st.mean(x[i] for x in r["out"]) if r["out"] else float("nan")
            print(f"{et} seme {seme}: {len(r['out'])} virate, prima {m(0):.2f} kn, minimo {m(1):.2f}, a 8 s {m(2):.2f}, recupero {m(3):.1f} s, scuffie {r['scuffie']}, fine t={r['T']:.0f}", flush=True)
        await br.close()
    if tutte:
        f = lambda i: st.mean(x[i] for x in tutte)
        print(f"TOTALE {et}: {len(tutte)} virate, prima {f(0):.2f} kn, minimo {f(1):.2f} ({100*f(1)/f(0):.0f}%), a 8 s {f(2):.2f}, recupero al 90% {f(3):.1f} s (mediana {st.median(x[3] for x in tutte):.1f}), scuffie {sc}")
asyncio.run(main())
