# Collaudo della lezione 11 rifatta (1.3.45, voce 79, docs/PROPOSTA-LEZIONE-11.md; criteri L1-L4 scritti prima, 22 nov 2026).
#   L1 l'esercizio «Vai verso il salto» premia la regola giusta e boccia quella sbagliata: tre piloti sui semi 2101-2110 (scelta) e 2121-2130 (conferma; i 2111-2120
#      sono stati guardati nella prima stesura dell'esercizio, partenza sotto la boa, che non passava L1 e L2: la conferma è su un gruppo nuovo):
#      A «giusto» (tiene le mure a dritta fino alla layline, poi vira e va alla boa), B «da oscillante» (vira a ogni scarso di almeno 7°), C «a caso» (vira ogni 30-60 s).
#      Soglie sui semi di conferma: A riesce in almeno 9 su 10, B in al più 1, C in al più 2.
#   L2 la regola giusta è davvero più veloce (il metro non è l'esercizio): secondi per arrivare a 15 m dalla boa, A meno di B in almeno 8 su 10 (conferma).
#      B e C non si fermano quando l'esercizio dice «non vale»: si misura il tempo fino alla boa lo stesso.
#   L3 il passo «Vira sullo scarso» resta valido: collaudo_pilota_lezioni.py (non qui).
#   L4 la riga «scarso / buono» c'è nell'esercizio (anche con l'opzione spenta) e i numeri sono quelli del conto; nelle altre lezioni no: collaudo_aiuto_scarso.py S3e.
# Ha misurato davvero: stampa per ogni pilota quante corse, quante virate, quanti arrivi alla boa.
# Uso: python tests/collaudo_lezione_salti.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri() + "#collaudo"
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();
(() => { const f = CanvasRenderingContext2D.prototype.fillText; window.__scritte = [];
  CanvasRenderingContext2D.prototype.fillText = function(t, x, y, ...r){ if (/^(scarso|buono) \\d+°$|^nella media$/.test(t)) __scritte.push(t); return f.call(this, t, x, y, ...r); }; })();"""
CORSA = """([seme, pil]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); sv.opt.scarso = "no";
  const li = LESSONS.findIndex(l => l.steps.some(s => s.title === "Vai verso il salto")), si = LESSONS[li].steps.findIndex(s => s.title === "Vai verso il salto");
  __seed(seme); sv.apriEsercizio(li, si); const R = sv.R, es = R.es, me = R.boats[0], mk = R.mark;
  let r = seme * 7919 % 1000 / 1000; const rnd = () => (r = (r * 9301 + 49297) % 233280 / 233280);
  let lato = 1, tUlt = 0, prossima = 30 + rnd() * 30, virate = 0, esito = null, tBoa = null, nRiga = 0, rigaOk = 0, k = 0;
  while (R.t < 420 && tBoa === null){
    const w = local, a = norm180(w.twd - S.h), sc = -Math.sign(a) * norm180(w.twd - env.twd), dx = S.x - mk.x, dy = S.y - mk.y, d = Math.hypot(dx, dy);
    const wm = windAt(mk.x, mk.y), la = rotLay(wm.tws), off = Math.abs(norm180(norm360(Math.atan2(dx, -dy) / D2R) - (wm.twd + 180))), dLay = off < la ? d * Math.sin((la - off) * D2R) : 0;
    const verso = norm360(Math.atan2(mk.x - S.x, -(mk.y - S.y)) / D2R);
    if (R.t - tUlt > 8 && Math.abs(a) > 30){
      const destra = norm180(norm360(Math.atan2(dx, -dy) / D2R) - (wm.twd + 180)) < 0; /* la barca sta a destra dell'asse del vento che passa per la boa */
      let vira = dLay < 8 && d > 20 && (lato === 1 ? destra : !destra); /* tutti: sulla layline verso cui si va, si vira */
      if (pil === "B") vira = vira || (sc >= 7 && Math.abs(a) <= 75);
      else if (pil === "C") vira = vira || R.t - tUlt > prossima;
      if (vira){ lato = -lato; tUlt = R.t; virate++; prossima = 30 + rnd() * 30; }
    }
    let rotta = norm360(w.twd + lato * 45);
    const scost = norm180(verso - w.twd); if (Math.sign(scost) === lato && Math.abs(scost) >= 45) rotta = verso; /* la boa si prende senza stringere di più: ci si va */
    const e = norm180(rotta - S.h); ctl.tiller = Math.max(-0.78, Math.min(0.78, -e / 25)); ctl.sheet = autoSheet(true);
    sv.run(dt, 1);
    if (es.esito && esito === null) esito = es.esito;
    if (Math.hypot(S.x - mk.x, S.y - mk.y) < 15) tBoa = R.t;
    if (++k % 60 === 0){ __scritte.length = 0; sv.draw(dt); const aa = norm180(local.twd - S.h); if (Math.abs(aa) >= 35 && Math.abs(aa) <= 75){ nRiga++;
      const s2 = -Math.sign(aa) * norm180(local.twd - env.twd), att = s2 >= 7 ? "scarso " + Math.round(s2) + "°" : s2 <= -3 ? "buono " + (-Math.round(s2)) + "°" : "nella media"; if (__scritte.length === 1 && __scritte[0] === att) rigaOk++; } }
    if (mode !== "race") break;
  }
  return { esito: esito || es.esito, tBoa, virate, nRiga, rigaOk }; }"""
bad = []
def chk(ok, m):
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []; R = {}
        for gruppo, semi in (("scelta", range(2101, 2111)), ("conferma", range(2121, 2131))):
            for pil in "ABC":
                for seme in semi:
                    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
                    await pg.goto(BASE); await pg.wait_for_timeout(250)
                    R[(gruppo, pil, seme)] = await pg.evaluate(CORSA, [seme, pil]); await ctx.close()
        for gruppo in ("scelta", "conferma"):
            for pil in "ABC":
                rr = [v for (g, p_, s), v in R.items() if g == gruppo and p_ == pil]
                ok_ = sum(1 for v in rr if v["esito"] == "ok"); boa = [v["tBoa"] for v in rr if v["tBoa"] is not None]
                print(f"  {gruppo} pilota {pil}: corse {len(rr)}, riuscite {ok_}, arrivate alla boa {len(boa)}, tempo mediano {statistics.median(boa) if boa else '—'} s, virate {[v['virate'] for v in rr]}", flush=True)
        conf = lambda pil: [R[("conferma", pil, s)] for s in range(2121, 2131)]
        okA, okB, okC = (sum(1 for v in conf(x) if v["esito"] == "ok") for x in "ABC")
        chk(okA >= 9, f"L1 pilota A (giusto) riesce in {okA} su 10 (almeno 9)")
        chk(okB <= 1, f"L1 pilota B (vira sugli scarsi) riesce in {okB} su 10 (al più 1)")
        chk(okC <= 2, f"L1 pilota C (a caso) riesce in {okC} su 10 (al più 2)")
        piu = sum(1 for s in range(2121, 2131) if R[("conferma", "A", s)]["tBoa"] is not None and (R[("conferma", "B", s)]["tBoa"] is None or R[("conferma", "A", s)]["tBoa"] < R[("conferma", "B", s)]["tBoa"]))
        chk(piu >= 8, f"L2 A arriva alla boa prima di B in {piu} su 10 (almeno 8)")
        nr = sum(v["nRiga"] for v in R.values()); ro = sum(v["rigaOk"] for v in R.values())
        chk(nr > 100 and ro == nr, f"L4 riga «scarso / buono» nell'esercizio con l'opzione spenta: giusta in {ro} controlli su {nr}")
        chk(not errs, f"errori della pagina: {errs[:1]}")
        await b.close()
    print("casi sbagliati: " + ("nessuno" if not bad else str(len(bad))))
    raise SystemExit(1 if bad else 0)
asyncio.run(main())
