# Voce 85 (27 nov 2026): quanto costa una strambata NEL GIOCO (motore + regola della strambata «violenta» di js/gioco.js, detectManeuvers), non solo nel motore.
# Navigazione libera, vento da nord a 6, 10, 15 nodi (quelli del menu), raffiche spente, salti spenti. La prua gira a 5°/s da 150° a 150° sulle altre mure
# (come la strambata di collaudo_boma_poppa.py), con la scotta ferma: «aperta» = 1 (boma a 85°), «corta» = 0,4 (boma sotto i 45° della soglia del gioco).
# Misura per ogni seme (il colpo ha una parte casuale): strambata violenta sì/no, sbandamento massimo, scuffia, velocità minima rispetto a prima.
# Uso: .venv-collaudi/bin/python tests/misura_strambata.py [semi 1-20]   (BROWSER=firefox)
import asyncio, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parents[1])
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
CORSA = """async ([kn, seme, scotta]) => {
  const sv = __sv, dt = 1 / 60; __seed(seme); sv.fast(0);
  sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', '0'], ['wDir', '0']]){ const e = document.getElementById(id); if (!e) continue; e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); sv.setShifts(null);
  const S = sv.S, ctl = sv.ctl; S.u = 2.5; S.vl = 0; S.r = 0; ctl.tiller = 0;
  let h = (sv.twd + 150 + 360) % 360, t = 0; S.h = h; ctl.sheet = scotta;
  for (; t < 30; t += dt){ S.h = h; ctl.sheet = scotta; sv.run(dt, 1); }
  const u0 = S.u, v0 = S.gybesV; let hm = 0, umin = 9, cap = false;
  for (t = 0; t < 25; t += dt){ if (t > 1 && t < 13) h = (h + 5 * dt + 360) % 360; S.h = h; ctl.sheet = scotta; sv.run(dt, 1);
    hm = Math.max(hm, Math.abs(S.heel)); umin = Math.min(umin, S.u); if (S.capsized){ cap = true; break; } }
  return { violenta: S.gybesV > v0, hm: +hm.toFixed(1), cap, umin: +(umin / u0).toFixed(3), kn0: +(u0 * 1.943844).toFixed(2) };
}"""
async def main():
    a, b = (sys.argv[1] if len(sys.argv) > 1 else "1-20").split("-")
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for kn in (6, 10, 15):
            for nome, sc in (("aperta", 1.0), ("corta", 0.4)):
                R = []
                for seme in range(int(a), int(b) + 1):
                    pg = await br.new_page(viewport={"width": 1360, "height": 650}); await pg.add_init_script(SEME)
                    await pg.goto((ROOT / "index.html").resolve().as_uri() + "#collaudo"); await pg.wait_for_function("window.__sv")
                    R.append(await pg.evaluate(CORSA, [kn, seme, sc])); await pg.close()
                hm = sorted(r["hm"] for r in R)
                print(f"{kn:2} nodi, vela {nome:6}: violente {sum(r['violenta'] for r in R)}/{len(R)}, scuffie {sum(r['cap'] for r in R)}/{len(R)}, "
                      f"sbandamento max mediano {statistics.median(hm):.0f}° (min {hm[0]:.0f}, max {hm[-1]:.0f}), velocità minima mediana {statistics.median(r['umin'] for r in R):.0%}, prima {R[0]['kn0']} nodi", flush=True)
        await br.close()
asyncio.run(main())
