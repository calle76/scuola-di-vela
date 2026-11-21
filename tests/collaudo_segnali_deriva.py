# Le bandiere della partenza nelle regate di Deriva (1.3.35, voce 67, Ale 21 novembre 2026: «le bandiere in tutte le regate coi 3 minuti»). Criteri scritti prima del codice.
#   B1 bandiere giuste a ogni decimo di secondo nel torneo (regata 1 a bastone, regata 2 triangolo, regata lunga) con preparazione da 3 minuti (e 1 e 5 con il selettore): tabella scritta qui, indipendente dal gioco
#   B2 i messaggi: una sola volta e al tempo giusto («Avviso: alzata la bandiera di classe…», «Preparatorio…», «Un minuto…»), e nessun «Segnale di avviso» del vecchio testo
#   B3 la X: con una barca oltre la linea allo sparo la X sale, e solo allora; senza nessuno oltre la linea non sale
#   B4 il riquadro e il Coach: con le bandiere in vista il riquadro del Coach sta sotto a quello delle bandiere e non lo copre (rettangoli senza sovrapposizione)
#   B5 pannello 1360x650 senza eccesso con le bandiere in vista nel torneo, anche col debito di giri (caso peggiore)
#   B6 la regata non cambia: le bandiere sono solo disegno e messaggi: stessa regata col pilota, arrivi uguali con segnali accesi e spenti (spenti = R.segnali = false subito dopo l'apertura)
#   B7 pagina senza #collaudo: torneo aperto come un giocatore, bandiere presenti a -180 s, 0 errori
# Uso: python tests/collaudo_segnali_deriva.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
def attese(t, cd):   # tabella indipendente dal gioco: classe, P, blu (la X si prova a parte)
    return (t >= -cd - 1e-9 and t < 0 - 1e-9 or False, cd >= 180 and -(cd - 60) - 1e-9 <= t < -60 - 1e-9, t >= -1e-9)
# apre la regata `k` del torneo (0 = bastone, 1 = triangolo) nella versione corta o lunga, con la preparazione cd; ferma la barca
APRI = """([k, seme, lungo, cd, avv]) => { const sv = __sv; sv.fast(0); __seed(seme); sv.simTime = 0; if (lungo) sv.lungo = true;
  const sel = document.getElementById('aiLevel'); sel.value = avv; sel.dispatchEvent(new Event('change'));
  sv.torApri(); document.getElementById('torGo').click(); const T = sv.tor;
  if (k) { T.ris.push([{ fin: 1, pp: 0 }, { fin: 2, pp: 0 }, { fin: 3, pp: 0 }, { fin: 4, pp: 0 }]); T.regate[1] = { tws: 10, wind: (seme * 45) % 360 }; } else T.regate[0] = { tws: 10, wind: (seme * 45) % 360 };
  __seed(seme); sv.simTime = 0; sv.openItem(['r', 't']); const c = document.getElementById('cdSel'); if (cd) { c.value = String(cd); c.dispatchEvent(new Event('change')); }
  __seed(seme); return { segnali: !!sv.R.segnali, cd: sv.R.cd, tri: !!sv.R.tri }; }"""
FERMA = """([secondi]) => { const sv = __sv, R = sv.R, dt = 1 / 60, x0 = sv.S.x, y0 = sv.S.y, out = [], toasts = []; let k = 0, ult = null;
  while (R.t < secondi){ sv.S.x = x0; sv.S.y = y0; sv.S.u = 0; sv.ctl.tiller = 0; sv.run(dt, 1); const tx = sv.toast; if (tx && tx !== ult) toasts.push([R.t, tx]); ult = tx;
    if (k++ % 6 === 0){ const f = bandiereR(); out.push([R.t, f.classe, f.P, f.blu]); } }
  return { out, toasts, cd: R.cd }; }"""
async def pagina(b, hash_="#collaudo", seme=True, w=1360, h=650):
    ctx = await b.new_context(viewport={"width": w, "height": h})
    if seme: await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + hash_); await pg.wait_for_timeout(400); return ctx, pg, errs
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        # ---- B1, B2 ----
        sbagli, campioni, msgs_ko, nmsg = [], 0, [], 0
        casi = [(0, 1, False, 180), (1, 2, False, 180), (0, 3, True, 180), (0, 4, False, 300), (0, 5, False, 60)]
        for k, seme, lungo, cd in casi:
            ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [k, seme, lungo, str(cd), "nessuno"])
            if not a["segnali"] or a["cd"] != cd: sbagli.append(("apertura", k, seme, a)); await ctx.close(); continue
            r = await pg.evaluate(FERMA, [5])
            for t, cl, P, bl in r["out"]:
                campioni += 1; e = attese(t, cd)
                if (cl, P, bl) != e: sbagli.append((k, seme, cd, round(t, 2), (cl, P, bl), e))
            testi = [x[1] for x in r["toasts"]]
            if cd >= 180:
                attesi = [(-cd, "Avviso: alzata la bandiera di classe, partenza tra " + str(round(cd / 60)) + " minuti"), (-(cd - 60), "Preparatorio: alzata la bandiera P"), (-60, "Un minuto: ammainata la P")]
            else: attesi = [(-cd, "Un minuto: resta la bandiera di classe, partenza tra un minuto")]
            for t0, tx in attesi:
                nmsg += 1; n = [x for x in r["toasts"] if x[1] == tx]
                if len(n) != 1 or abs(n[0][0] - t0) > 0.1: msgs_ko.append((k, seme, cd, tx[:30], [round(x[0], 2) for x in n]))
            if any(t.startswith("Segnale di avviso") for t in testi): msgs_ko.append((k, seme, cd, "vecchio testo", [t[:30] for t in testi if t.startswith("Segnale")]))
            await ctx.close()
        chk(campioni >= 1500 and not sbagli, f"B1 bandiere a ogni decimo: {campioni} letture in {len(casi)} regate (bastone, triangolo, lunga; 1, 3 e 5 minuti), diverse dalla tabella {len(sbagli)}: {sbagli[:3]}")
        chk(nmsg >= 10 and not msgs_ko, f"B2 messaggi una volta e al tempo giusto: {nmsg} controllati, sbagliati {len(msgs_ko)}: {msgs_ko[:3]}")
        # ---- B3 la X ----
        xr = []
        for caso, seme in (("oltre", 1), ("oltre", 2), ("oltre", 3), ("nessuno", 4), ("nessuno", 5), ("nessuno", 6)):
            ctx, pg, errs = await pagina(b); await pg.evaluate(APRI, [0, seme, False, "180", "principianti"])
            r = await pg.evaluate("""([caso]) => { const sv = __sv, R = sv.R, dt = 1 / 60, wy = b => toWF(b.S.x, b.S.y)[1]; let xPrima = false;
              while (R.t < -0.5){ sv.pilota(dt); sv.run(dt, 1); if (R.t < -1 && bandiereR().X) xPrima = true; }
              /* oltre: l'avversario 1 messo 6 m oltre la linea e tenuto fermo; nessuno: tutti 20 m dietro la linea e tenuti fermi fino allo sparo */
              const a = R.boats[1], fermi = []; for (const b of R.boats){ if (b.me) continue; const [wx] = toWF(b.S.x, b.S.y), [px, py] = fromWF(wx, caso === 'oltre' && b === a ? -6 : 20); b.S.x = px; b.S.y = py; fermi.push([b, px, py]); }
              const oltre = R.boats.filter(b => wy(b) <= 0).length; let xDopo = false, k = 0;
              while (R.t < 3){ for (const [b, px, py] of fermi){ if (R.t < 0.5 || caso === 'oltre' && b === a){ b.S.x = px; b.S.y = py; b.S.u = 0; } } sv.pilota(dt); sv.run(dt, 1); if (R.t >= 0 && R.t < 2 && bandiereR().X) xDopo = true; }
              return { xDopo, xPrima, oltre }; }""", [caso])
            xr.append((caso, r["xDopo"], r["xPrima"], r["oltre"])); await ctx.close()
        chk(len(xr) == 6 and all(x[1] is True and not x[2] and x[3] >= 1 for x in xr if x[0] == "oltre") and all(x[1] is False and not x[2] and x[3] == 0 for x in xr if x[0] == "nessuno"),
            f"B3 la X (caso, X dopo lo sparo, X prima, barche oltre la linea a -0,5 s): {xr}")
        # ---- B4, B5 ----
        ctx, pg, errs = await pagina(b); await pg.evaluate(APRI, [0, 7, True, "180", "principianti"])
        r = await pg.evaluate("""() => { const sv = __sv, R = sv.R, dt = 1 / 60; sv.opt.coachReg = true; R.cr = { ult: -1e9, cur: null, log: [], part: true, cop: 0, sc: 0, leg: 1, pos: null, need: 0, done: 0, pp: 0, pen: 0, vicino: true, sponsor: true };
          while (R.t < -178) sv.run(dt, 1); R.t = -179.9; sv.run(dt, 1); crDi('serio', 'Una frase del Coach abbastanza lunga da occupare due righe del riquadro per la prova della sovrapposizione.', true);
          R.need = R.done + 2; R.rqMotivo = 'prova'; sv.draw(0.016);
          const ecc = Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0); return { rq: R.rqRect, rq2: R.rqRect2, cr: R.crRect, ecc, W: innerWidth, H: innerHeight }; }""")
        a, c = r["rq"], r["cr"]
        sov = a and c and not (c[0] >= a[0] + a[2] or c[0] + c[2] <= a[0] or c[1] >= a[1] + a[3] or c[1] + c[3] <= a[1])
        chk(a and c and not sov, f"B4 riquadro delle bandiere {a} e riquadro del Coach {c}: nessuna sovrapposizione")
        chk(r["ecc"] == 0 and r["rq2"] is not None, f"B5 pannello {r['W']}x{r['H']} con bandiere e debito di giri in vista: eccesso {r['ecc']} px, riquadro delle penalità {r['rq2']}")
        await ctx.close()
        # ---- B6 la regata non cambia ----
        fin = []
        for acceso in (True, False):
            ctx, pg, errs = await pagina(b); await pg.evaluate(APRI, [0, 8, False, "180", "principianti"])
            fin.append(await pg.evaluate("""([acceso]) => { const sv = __sv, R = sv.R; if (!acceso) R.segnali = false; let n = 0; while (R.t < 700 && R.boats.some(b => b.fin === null && !b.dnf)){ sv.pilota(1 / 60); sv.run(1 / 60, 1); n++; } return R.boats.map(b => [b.fin, b.pen]); }""", [acceso])); await ctx.close()
        chk(fin[0] == fin[1] and all(f[0] is not None for f in fin[0]), f"B6 arrivi con bandiere e senza (stessa regata, pilota): {[round(f[0], 2) for f in fin[0]]}, identici: {fin[0] == fin[1]}")
        # ---- B7 ----
        ctx, pg, errs = await pagina(b, "", seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300); vis = await pg.is_visible("#bGo")
        if vis: await pg.click("#bGo")
        await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => ({ s: !!(R && R.segnali), bd: R ? bandiereTesto(bandiereR()) : null, t: R ? R.t : null, mode: mode })")
        chk(vis and h["s"] and h["mode"] == "race" and h["bd"] == "classe" and h["t"] < -170, f"B7 torneo aperto dal menu come un giocatore: istruzioni viste {vis}, segnali {h['s']}, bandiere a {h['t']:.0f} s: {h['bd']}")
        chk(not errs, f"B7 errori della pagina {errs[:1]}"); await ctx.close()
        await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
