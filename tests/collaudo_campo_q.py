# Q tenuto in regata inquadra tutto il campo (1.3.41, voce 76 A2, docs/PROPOSTA-CAMPO-PRIMA-DEL-VIA.md; Lucio, 21-22 nov 2026). Soglie scritte nella proposta prima del codice.
#   Q1 tutto dentro: 20 regate lunghe e 20 corte, Q tenuto 2 s a -120 s, +30 s e a metà regata, vista a prua e a nord: linea, boe e barche dentro lo schermo con 20 px di margine; 0 fuori su almeno 240
#   Q2 torna com'era: 1 s dopo il rilascio, zoom e spostamento a meno dell'1% da quelli di prima
#   Q3 prove come prima: nelle prove Q dà la stessa vista della 1.3.40 (commit 3333166), 20 casi a meno dell'1%
#   Q4 la regata non cambia: 20 regate identiche al bit con Q tenuto e senza (la pagina disegna a ogni passo); in Firefox 5 su 5 (Ale, 22 nov: la proprietà è del codice, Chromium la prova su 20)
#   Q5 come un giocatore: pagina senza #collaudo, regata lunga, Q tenuto prima del via: boa e linea dentro lo schermo, 0 errori
# Uso: python tests/collaudo_campo_q.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, subprocess, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
N4 = 5 if BR == "firefox" else 20
RIF = "3333166"   # 1.3.40
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
# misura dentro la pagina: punti del campo sullo schermo con la vista di adesso
DENTRO = """(() => { const v = view(), P = [[R.pin.x, R.pin.y], [R.cb.x, R.cb.y], ...R.marks.map(m => [m.x, m.y]), ...R.boats.map(b => [b.S.x, b.S.y])].map(([x, y]) => toScreen(v, x, y));
  const fuori = P.filter(([x, y]) => x < 20 || x > W - 20 || y < 20 || y > H - 20); return { n: P.length, fuori: fuori.length, zoom: zoomQ }; })"""
Q1 = """([seme, lungo, vista]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.lungo = lungo; sv.opt.view = vista; sv.opt.countdown = 180; sv.store = 'scuolaVelaSim.v1';
  sv.torApri(); document.getElementById("torGo").click(); const R = sv.R, me = R.boats[0], out = [], dentro = """ + DENTRO + """;
  const metà = lungo ? 280 : 110;
  for (const t of [-120, 30, metà]){ while (R.t < t && me.fin === null){ sv.pilota(dt); sv.run(dt, 1); } if (me.fin !== null) break;
    for (let k = 0; k < 30; k++) sv.draw(dt); const z0 = zoomQ, o0 = viewOff.slice();
    dispatchEvent(new KeyboardEvent("keydown", { key: "q" })); for (let k = 0; k < 120; k++) sv.draw(dt); const d = dentro();
    dispatchEvent(new KeyboardEvent("keyup", { key: "q" })); for (let k = 0; k < 60; k++) sv.draw(dt);
    out.push({ t, ...d, torna: Math.abs(zoomQ - z0) / z0 < 0.01 && Math.abs(viewOff[0] - o0[0]) < W * 0.01 && Math.abs(viewOff[1] - o0[1]) < H * 0.01 }); }
  return out; }"""
Q3 = """([m, passi]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(40 + m); sv.startMission(m); for (let k = 0; k < passi; k++) sv.run(dt, 1);
  for (let k = 0; k < 30; k++) sv.draw(dt); dispatchEvent(new KeyboardEvent("keydown", { key: "q" })); for (let k = 0; k < 120; k++) sv.draw(dt);
  const r = [zoomQ, viewOff[0], viewOff[1]]; dispatchEvent(new KeyboardEvent("keyup", { key: "q" })); return r; }"""
Q4 = """([seme, q]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.opt.countdown = 60; sv.store = 'scuolaVelaSim.v1'; sv.torApri(); document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0]; if (q) dispatchEvent(new KeyboardEvent("keydown", { key: "q" }));
  while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); sv.draw(dt); }
  if (q) dispatchEvent(new KeyboardEvent("keyup", { key: "q" }));
  const f = R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(',')).join('|'); document.getElementById("rTor").click(); return f; }"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina(url=BASE + "#collaudo", seme=True):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650})
            if seme: await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg
        # ---- Q1, Q2 ----
        casi = fuori = torna_no = 0; esempi = []; zmin = 9
        for lungo in (True, False):
            for k in range(20):
              for vista in ("prua", "nord"):
                ctx, pg = await pagina(); r = await pg.evaluate(Q1, [1200 + k, lungo, vista]); await ctx.close()
                for x in r:
                    casi += 1; fuori += x["fuori"] > 0; torna_no += not x["torna"]; zmin = min(zmin, x["zoom"])
                    if x["fuori"] and len(esempi) < 3: esempi.append((lungo, k, x))
        chk(casi >= 240 and fuori == 0, f"Q1 inquadrature con Q tenuto {casi} (punti del campo in ciascuna: linea, boe, barche), con qualcosa fuori {fuori}; zoom più lontano {zmin:.3f}; esempi {esempi}")
        chk(casi >= 240 and torna_no == 0, f"Q2 dopo il rilascio vista tornata com'era in {casi - torna_no} su {casi}")
        # ---- Q3 ----
        tmp = tempfile.mkdtemp(); subprocess.run(f"git -C {ROOT} archive {RIF} index.html js img | tar -x -C {tmp}", shell=True, check=True)
        VECCHIA = pathlib.Path(tmp, "index.html").as_uri() + "#collaudo"; diversi = []; n3 = 0
        for m in range(5):
            for passi in (0, 300, 600, 900):
                v = []
                for url in (BASE + "#collaudo", VECCHIA):
                    ctx, pg = await pagina(url); v.append(await pg.evaluate(Q3, [m, passi])); await ctx.close()
                n3 += 1
                if abs(v[0][0] - v[1][0]) > 0.01 * v[1][0] or abs(v[0][1] - v[1][1]) > 13.6 or abs(v[0][2] - v[1][2]) > 6.5: diversi.append((m, passi, v))
        chk(n3 == 20 and not diversi, f"Q3 prove: vista con Q uguale alla 1.3.40 in {n3 - len(diversi)} casi su {n3}; diversi {diversi[:2]}")
        # ---- Q4 ----
        uguali = 0
        for seme in range(1301, 1301 + N4):
            f = []
            for q in (True, False):
                ctx, pg = await pagina(); f.append(await pg.evaluate(Q4, [seme, q])); await ctx.close()
            uguali += f[0] == f[1]
        chk(uguali == N4, f"Q4 regate identiche al bit con Q tenuto e senza: {uguali} su {N4}")
        # ---- Q5 ----
        ctx, pg = await pagina(BASE, seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        await pg.wait_for_timeout(500); await pg.keyboard.down("q"); await pg.wait_for_timeout(2000)
        r5 = await pg.evaluate("() => [(" + DENTRO + ")(), R.up, R.t]"); await pg.keyboard.up("q")
        chk(r5[0]["fuori"] == 0 and r5[1] >= 400 and r5[2] < 0 and not errs, f"Q5 pagina da giocatore, regata da {r5[1]} m, t = {r5[2]:.0f} s: punti fuori {r5[0]['fuori']} su {r5[0]['n']}, zoom {r5[0]['zoom']:.3f}; errori {errs[:1]}")
        await ctx.close(); await b.close()
        chk(not errs, f"errori della pagina {errs[:2]}")
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
