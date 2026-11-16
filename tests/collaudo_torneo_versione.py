# Il torneo in corso sopravvive al cambio di versione (1.3.14; Ale, 16 novembre 2026: «ogni volta che arriva una nuova versione si azzera tutto, non riusciamo a finire un torneo»).
# Criteri scritti prima di misurare:
#   V0 il metro misura davvero: una regata del torneo corsa col pilota lascia nel salvataggio (localStorage) un torneo con 1 regata fatta e la versione del gioco
#   V1 lo stesso salvataggio con la versione d'inizio cambiata in «1.3.13», pagina ricaricata senza #collaudo come la carica un giocatore, menu Deriva, «Torneo»:
#      il torneo è ancora nel salvataggio con la stessa regata fatta (identica), la finestra non dice «Il gioco è cambiato» e ha il pulsante per continuare
#   V2 continuando si apre la regata 2 di 4
#   V3 controprova: col codice della 1.3.13 (git archive) e lo stesso salvataggio segnato «1.3.12», aprendo il torneo il salvataggio lo perde (la differenza si vede)
#   V4 nessun errore di pagina
# Uso: .venv-collaudi/bin/python tests/collaudo_torneo_versione.py   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, subprocess, sys, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHIAVE = "scuolaVelaSim.v1"
fail = []; casi = 0
def chk(ok, testo):
    global casi; casi += 1
    print(("OK   " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
CORSA = """() => { const sv = __sv, dt = 1 / 60; let s = 4711; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  sv.fast(0); window.confirm = () => true; sv.torApri(); document.getElementById('torGo').click(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R; while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }
  for (let j = 0; j < 30; j++) sv.run(dt, 1);
  sv.torChiudi();   /* come il pulsante della classifica a regata finita: è lì che la regata entra nel torneo */
  return { fin: R.boats[0].fin, salvato: localStorage.getItem('""" + CHIAVE + """') }; }"""
APRI = """() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); document.getElementById('goTor').click();
  const p = JSON.parse(localStorage.getItem('""" + CHIAVE + """') || '{}'); return { torneo: p.torneo || null, testo: document.body.innerText.includes('Il gioco è cambiato'), go: !!document.getElementById('torGo') }; }"""
async def apri(br, base, salvato, errs):
    ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(base); await pg.evaluate("([k, v]) => localStorage.setItem(k, v)", [CHIAVE, salvato]); await pg.reload(); await pg.wait_for_timeout(400)
    return ctx, pg, await pg.evaluate(APRI)
async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []
        ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(400)
        vers = await pg.evaluate("() => VERSIONE"); r = await pg.evaluate(CORSA); await ctx.close()
        P = json.loads(r["salvato"] or "{}"); T = P.get("torneo")
        chk(bool(T) and len(T["ris"]) == 1 and T["ver"] == vers and r["fin"] is not None, f"V0 una regata del torneo corsa (arrivo del pilota {r['fin']}): salvato un torneo con {len(T['ris']) if T else None} regata fatta, versione {T and T['ver']} (gioco {vers})")
        if not T: print("ESITO: NON VALIDA"); sys.exit(1)
        P["torneo"]["ver"] = "1.3.13" if vers != "1.3.13" else "1.3.12"
        ctx, pg, a = await apri(br, (ROOT / "index.html").as_uri(), json.dumps(P), errs)
        chk(bool(a["torneo"]) and a["torneo"]["ris"] == T["ris"] and not a["testo"] and a["go"], f"V1 torneo cominciato con la {P['torneo']['ver']} e riaperto con la {vers}: ancora nel salvataggio con la stessa regata {bool(a['torneo']) and a['torneo']['ris'] == T['ris']}, scritta «Il gioco è cambiato» {a['testo']}, pulsante per continuare {a['go']}")
        if a["go"]:
            await pg.click("#torGo"); await pg.wait_for_timeout(600)
            tit = await pg.evaluate("() => document.body.innerText.match(/[Rr]egata \\d di 4/g)")
            chk(bool(tit) and "2 di 4" in tit[0], f"V2 continuando si apre la regata 2 di 4: a schermo {tit and tit[:2]}")
        await ctx.close()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(f"git -C {ROOT} archive v1.3.13 | tar -x -C {tmp}", shell=True, check=True)
            P["torneo"]["ver"] = "1.3.12"
            ctx, pg, b = await apri(br, (pathlib.Path(tmp) / "index.html").as_uri(), json.dumps(P), errs); await ctx.close()
        chk(b["torneo"] is None and b["testo"], f"V3 controprova col codice della 1.3.13: torneo perso {b['torneo'] is None}, scritta «Il gioco è cambiato» {b['testo']}")
        chk(not errs, f"V4 nessun errore di pagina {errs[:2]}")
        await br.close()
    print("controlli fatti:", casi)
    if fail or casi < 5: print("ESITO: FALLITO" if fail else "ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK")
asyncio.run(main())
