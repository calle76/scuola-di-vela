# Raffiche al via delle regate lunghe (1.3.40, voce 75, docs/PROPOSTA-RAFFICHE-AL-VIA.md; Lucio, 21 nov 2026: scuffia appena dopo «Parti»). Soglie scritte nella proposta prima del codice,
# scelte sui semi 1001-1040 e confermate sui 1041-1080 (qui gira la conferma). Sulla 1.3.39: mediana 1,77, 40 su 40 sopra 1,3, 2 scuffie su 40.
#   V1 vento sulla barca a -180 s diviso il vento medio del campo (griglia di 21x18 punti): mediana <= 1,15 e al più il 25% sopra 1,3
#   V2 comandi fermi per i primi 20 s: 0 scuffie
#   V5 come un giocatore: pagina senza #collaudo, torneo (lungo per chi gioca): vento al via sotto 1,3 volte la media, 0 errori
# Uso: python tests/collaudo_raffiche_al_via.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
RAPP = """() => { const me = R.boats[0].S; let s = 0, n = 0; for (let x = -400; x <= 400; x += 40) for (let y = -500; y <= 200; y += 40){ s += windAt(x, y).tws; n++; }
  return windAt(me.x, me.y).tws / (s / n); }"""
# apertura e corsa in un solo evaluate (memoria: «evaluate separati»)
VIA = """([seme, rapp]) => { const sv = __sv; sv.fast(0); __seed(seme); sv.lungo = true; sv.opt.countdown = 180; sv.store = 'scuolaVelaSim.v1'; sv.torApri();
  document.getElementById("torGo").click(); const R = sv.R, r0 = (new Function("return (" + rapp + ")()"))(); let scuf = null;
  while (R.t < -160){ sv.run(1 / 60, 1); if (S.capsized && scuf === null) scuf = +(R.t + 180).toFixed(1); }
  return [r0, scuf, R.up]; }"""
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []; rr = []; sc = []; up = []
        for seme in range(1041, 1081):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
            r, s, u = await pg.evaluate(VIA, [seme, RAPP]); rr.append(r); sc.append(s); up.append(u); await ctx.close()
        sopra = sum(r > 1.3 for r in rr)
        chk(len(rr) == 40 and statistics.median(rr) <= 1.15 and sopra <= 10 and min(up) >= 400, f"V1 vento al via / media del campo, 40 regate lunghe (bolina {min(up)}-{max(up)} m): mediana {statistics.median(rr):.2f}, min {min(rr):.2f}, max {max(rr):.2f}, sopra 1,3: {sopra}")
        chk(len(sc) == 40 and all(s is None for s in sc), f"V2 comandi fermi per 20 s: scuffie {sum(s is not None for s in sc)} su {len(sc)} {[s for s in sc if s is not None]}")
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE); await pg.wait_for_timeout(300)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        await pg.wait_for_timeout(500)
        r5 = await pg.evaluate("() => [(" + RAPP + ")(), R.t, R.up]")
        chk(r5[0] < 1.3 and r5[2] >= 400 and not errs, f"V5 pagina da giocatore: vento al via {r5[0]:.2f} volte la media a t = {r5[1]:.0f} s, bolina {r5[2]} m; errori {errs[:1]}")
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
