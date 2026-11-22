# Il riquadro «Raddrizza» a regata finita (1.3.39; Ale, 22 nov 2026: scuffiato sulla linea d'arrivo, il riquadro restava anche sul resoconto della regata).
#   A1 regata finita (arrivato) e barca rovesciata: riquadro e pulsante nascosti, risultato visibile; regate semplici e del torneo, 10 regate
#   A2 controprova: la stessa regata con la barca rovesciata a metà (prima dell'arrivo): riquadro visibile; e il tasto A la raddrizza ancora
#   A3 ritirato (torneo) e barca rovesciata: riquadro nascosto
#   A4 la lezione 6 «La scuffia» (noRight) resta com'era: riquadro nascosto
# Il pannello si aggiorna chiamando panel() (sv.draw non lo fa: nel gioco lo chiama il ciclo della pagina ogni 0,1 s; scoperto con la controprova A2, 22 nov).
# La barca si rovescia mettendo S.capsized (il pilota non scuffia da solo): si misura il pannello, non la fisica. Soglie: 0 casi sbagliati, almeno 10 regate per A1 e A2.
# Uso: python tests/collaudo_scuffia_arrivo.py   (BROWSER=firefox per Firefox)
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
# apertura e corsa in un solo evaluate (memoria: «evaluate separati»)
CORRI = """([seme, torneo, meta]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme);
  if (torneo){ sv.store = 'scuolaVelaSim.v1'; sv.torApri(); document.getElementById("torGo").click(); } else sv.openItem(["r", 0]);
  const R = sv.R, me = R.boats[0], vis = id => !document.getElementById(id).hidden;
  let a = null;
  while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1);
    if (meta && a === null && me.leg >= 1 && R.t > 60){ S.capsized = true; S.righting = 0; panel(); a = [vis("capOverlay"), vis("rightBtn")];
      dispatchEvent(new KeyboardEvent("keydown", { key: "a" })); dispatchEvent(new KeyboardEvent("keyup", { key: "a" })); a.push(S.righting > 0); return { a }; } }
  S.capsized = true; S.righting = 0; panel();
  return { fin: me.fin, cap: vis("capOverlay"), btn: vis("rightBtn"), ris: vis("rDone") || !!document.querySelector(".fin:not([hidden]), #finBox:not([hidden])") }; }"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina(url=BASE + "#collaudo"):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg
        a1 = []; a2 = []
        for k in range(10):
            torneo = k % 2 == 1
            ctx, pg = await pagina(); r = await pg.evaluate(CORRI, [900 + k, torneo, False]); await ctx.close(); a1.append((k, torneo, r))
            ctx, pg = await pagina(); r = await pg.evaluate(CORRI, [900 + k, torneo, True]); await ctx.close(); a2.append((k, torneo, r))
        sb1 = [x for x in a1 if x[2]["fin"] is None or x[2]["cap"] or x[2]["btn"] or not x[2]["ris"]]
        chk(len(a1) == 10 and not sb1, f"A1 arrivato e rovesciato: riquadro nascosto in {10 - len(sb1)} regate su {len(a1)} (5 semplici, 5 del torneo); sbagliate {sb1[:2]}")
        sb2 = [x for x in a2 if x[2].get("a") != [True, True, True]]
        chk(len(a2) == 10 and not sb2, f"A2 controprova, rovesciato a metà regata: riquadro e pulsante visibili e tasto A che raddrizza in {10 - len(sb2)} su {len(a2)}; sbagliate {sb2[:2]}")
        ctx, pg = await pagina()
        r3 = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(5); sv.store = 'scuolaVelaSim.v1'; sv.torApri(); document.getElementById("torGo").click();
          const R = sv.R; while (R.t < 30){ sv.pilota(dt); sv.run(dt, 1); } window.confirm = () => true; document.getElementById("rRet").click(); sv.run(dt, 1);
          S.capsized = true; S.righting = 0; panel(); return [R.boats[0].dnf, !document.getElementById("capOverlay").hidden]; }""")
        chk(r3 == [True, False], f"A3 ritirato e rovesciato: [ritirato, riquadro visibile] = {r3} (atteso [True, False])")
        await ctx.close()
        ctx, pg = await pagina()
        r4 = await pg.evaluate("""() => { const sv = __sv; sv.fast(0); const L = LESSONS.findIndex(l => l.steps && l.steps.some(s => s.noRight)); if (L < 0) return null;
          const k = LESSONS[L].steps.findIndex(s => s.noRight); sv.openItem(["l", L]); showStep(k); if (!curStep().noRight) return [L, k, "passo non raggiunto"]; S.capsized = true; S.righting = 0; panel();
          return [L, k, !document.getElementById("capOverlay").hidden]; }""")
        chk(r4 is not None and r4[2] is False, f"A4 lezione col passo «niente raddrizzamento» (lezione, passo, riquadro visibile) = {r4}")
        await ctx.close(); await b.close()
        chk(not errs, f"errori della pagina {errs[:2]}")
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
