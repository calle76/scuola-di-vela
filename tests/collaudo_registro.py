# Registro degli errori: provoca apposta ogni tipo di errore guidando la barca (barra e scotta, come un giocatore)
# e verifica che ogni voce conti quando deve, e non conti quando il passo della lezione chiede proprio quell'errore.
# Uso: python collaudo_registro.py [casi]
#   a prova pulita (stella)   b boa dal lato sbagliato   c piantato nel vento   d strambata a vela aperta   e scuffia
#   f partenza anticipata     g linea fuori dagli estremi   h contatto   i lezioni (errori richiesti e non)
# Predefinito: tutti. Il tempo è accelerato; il collaudo completo dura alcuni minuti.
import asyncio, pathlib, sys, json
from playwright.async_api import async_playwright
from collaudo_giro_boa import PILOTA
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
URL = BASE + "#collaudo"

# pilota verso punti assoluti (x, y in metri); alla fine: "luff" = prua nel vento e vela lascata (per piantarsi), "free" = lascia i comandi
VAI = """
(args) => {
  const [pts, fine] = args, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  clearInterval(window.__p2); let i = 0, side = 1; window.__p2end = false;
  window.__p2 = setInterval(() => {
    const sv = __sv, S = sv.S;
    if (S.capsized){ if (!S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" })); return; }
    if (i >= pts.length){
      window.__p2end = true;
      if (fine === "luff"){ const err = n180(S.h - sv.twd); sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20)) * (S.u < 0 ? -1 : 1); sv.ctl.sheet = 1; }
      return;
    }
    const p = pts[i]; if (Math.hypot(p[0] - S.x, p[1] - S.y) < 6){ i++; return; }
    const brg = Math.atan2(p[0] - S.x, -(p[1] - S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg;
    if (Math.abs(rel) < 52){ if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; }
    const cur = n180(S.h - sv.twd);
    if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
    const err = n180(S.h - want);
    sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
    sv.ctl.sheet = Math.abs(cur) > 150 ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet();
  }, 25);
}
"""
# poggia con la vela tutta aperta finché il vento passa dall'altra parte: strambata a vela aperta
STRAMBA = """
() => {
  const D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  clearInterval(window.__p2); const g0 = __sv.S.gybesV; window.__p2end = false;
  window.__p2 = setInterval(() => {
    const sv = __sv, S = sv.S;
    if (S.gybesV > g0 || S.capsized){ sv.ctl.tiller = 0; window.__p2end = true; clearInterval(window.__p2); return; }
    const cur = n180(S.h - sv.twd), side = Math.sign(cur || 1);
    const err = n180(S.h - (S.h + side * 25));      // continua a girare lontano dal vento
    sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20)); sv.ctl.sheet = 1;
  }, 25);
}
"""
FERMA = "() => { clearInterval(window.__p2); clearInterval(window.__pil); __sv.ctl.tiller = 0; }"
SET = "a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}"
esiti = []
def verifica(nome, ok, dettaglio):
    esiti.append(ok); print(("OK    " if ok else "ERRORE ") + nome + " | " + dettaglio, flush=True)

async def attendi(pg, cond, sec):
    for _ in range(int(sec * 5)):
        if await pg.evaluate(cond): return True
        await pg.wait_for_timeout(200)
    return False

async def reg(pg): return await pg.evaluate("JSON.parse(JSON.stringify(__sv.reg))")

async def main():
    casi = sys.argv[1] if len(sys.argv) > 1 else "abcdefghi"
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("localStorage.clear()"); await pg.goto("about:blank"); await pg.goto(URL); await pg.wait_for_timeout(300)

        if "a" in casi:  # prova 1 guidata dal pilota: nessun errore, stella salvata e mostrata nel menu
            await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate("__sv.startMission(0, 0)"); await pg.evaluate("__sv.fast(8)"); await pg.evaluate(PILOTA, [])
            await attendi(pg, "__sv.S.finished", 120); await pg.evaluate(FERMA)
            r = await reg(pg); done = await pg.inner_text("#doneText")
            await pg.click("#toMenu"); stelle = await pg.locator("#menu .star").count()
            verifica("prova pulita", sum(v for k, v in r.items()) == 0 and "senza errori" in done and stelle == 1, f"registro {r} | «{done}» | stelle nel menu {stelle}")

        if "b" in casi:  # prova 4: gira la boa dal lato sbagliato, poi rimedia
            rimedio = [-60, 0, 60, 0, -60, -120, 180, 120, 60, 0, -60]
            await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate("__sv.startMission(3, 0)"); await pg.evaluate("__sv.fast(8)"); await pg.evaluate(PILOTA, [[0, rimedio]])
            await attendi(pg, "__sv.S.finished", 200); await pg.evaluate(FERMA)
            r = await reg(pg); s = await pg.evaluate("[__sv.S.finished, __sv.S.wrongMarks || 0]"); done = await pg.inner_text("#doneText")
            await pg.click("#toMenu"); stelle = await pg.locator("#menu .star").count()
            verifica("boa dal lato sbagliato", s[0] and r["wrongMarks"] == s[1] == 1 and "boa dal lato sbagliato" in done and stelle == 1,
                     f"finita {s[0]} | registro {r} | «{done}» | stelle nel menu {stelle} (solo quella della prova 1)")

        if "c" in casi:  # prova 3: prua nel vento con la vela lascata finché la barca si pianta; una virata normale non conta
            await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate("__sv.startMission(2, 0)"); await pg.evaluate("__sv.fast(4)")
            await pg.evaluate(PILOTA, []); await pg.wait_for_timeout(4000); await pg.evaluate(FERMA)   # bolina verso la boa, con qualche virata
            prima = await reg(pg)
            await pg.evaluate(VAI, [[], "luff"]); await pg.wait_for_timeout(2500)          # circa 10 s simulati nel vento
            r = await reg(pg); u = await pg.evaluate("__sv.S.u")
            verifica("piantato nel vento", prima["irons"] == 0 and r["irons"] == 1 and 4 <= r["ironsSec"] <= 9,
                     f"prima {prima['irons']} episodi | dopo {r['irons']} episodi, {r['ironsSec']:.1f} s | velocità {u:.2f} m/s")
            await pg.evaluate(FERMA)

        if "d" in casi:  # prova 1: strambata con la vela tutta aperta
            await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate("__sv.startMission(0, 0)"); await pg.evaluate("__sv.fast(3)"); await pg.evaluate("__sv.kick(260)")
            await pg.evaluate(STRAMBA); await attendi(pg, "window.__p2end", 40); await pg.wait_for_timeout(800)
            r = await reg(pg); s = await pg.evaluate("[__sv.S.gybesV, __sv.S.capsizes]")
            verifica("strambata a vela aperta", r["gybesV"] == s[0] == 1 and r["capsizes"] == s[1], f"registro {r} | contatori della barca {s}")
            await pg.evaluate(FERMA)

        if "e" in casi:  # stessa strambata con un colpo del boma molto più forte: la barca scuffia
            await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate("__sv.startMission(0, 0)"); await pg.evaluate("__sv.fast(3)"); await pg.evaluate("__sv.kick(3000)")
            await pg.evaluate(STRAMBA); await attendi(pg, "__sv.S.capsized", 40); await pg.wait_for_timeout(500)
            r = await reg(pg); txt = await pg.inner_text("#stErr")
            verifica("scuffia", r["capsizes"] == 1 and r["gybesV"] == 1 and "1 scuffia" in txt, f"registro {r} | pannello «{txt}»")
            await pg.evaluate("__sv.kick(260)"); await pg.evaluate(FERMA)

        if "f" in casi:  # regata senza avversari: al via la barca è oltre la linea; piantarsi prima del via non conta
            await pg.evaluate(SET, ["#aiLevel", "nessuno"]); await pg.evaluate(SET, ["#cdSel", "180"]); await pg.evaluate("__sv.openItem(['r',0])")
            await pg.evaluate("__sv.fast(8)"); await pg.evaluate(VAI, [[[-20, 10], [20, 10]] * 20, "free"])   # avanti e indietro sotto la linea
            await attendi(pg, "__sv.R.t > -40", 60); await pg.evaluate(VAI, [[[0, -15]], "luff"])                 # poi oltre la linea, e lì resta
            await attendi(pg, "__sv.R.t > 0.3", 60); r = await reg(pg)
            verifica("partenza anticipata", r["ocs"] == 1 and r["irons"] == 0 and r["outLine"] == 0, f"registro subito dopo il via {r}")
            await pg.evaluate(FERMA)

        if "g" in casi:  # regata: aspetta sotto la linea ma fuori dagli estremi, poi risale e la attraversa lì
            await pg.evaluate(SET, ["#aiLevel", "nessuno"]); await pg.evaluate(SET, ["#cdSel", "60"]); await pg.evaluate("__sv.openItem(['r',0])")
            await pg.evaluate("__sv.fast(8)"); await pg.evaluate(VAI, [[[70, 25], [110, 25]] * 20, "free"])   # avanti e indietro sotto la linea, fuori dagli estremi
            await attendi(pg, "__sv.R.t > 0", 60); await pg.evaluate(VAI, [[[70, -30]], "free"])
            await attendi(pg, "window.__p2end", 60); r = await reg(pg)
            verifica("linea fuori dagli estremi", r["outLine"] == 1 and r["ocs"] == 0, f"registro {r}")
            await pg.evaluate(FERMA)

        if "h" in casi:  # regata con avversari: punta la barca più vicina finché c'è un contatto
            await pg.evaluate(SET, ["#aiLevel", "principianti"]); await pg.evaluate(SET, ["#cdSel", "60"]); await pg.evaluate("__sv.openItem(['r',0])"); await pg.evaluate("__sv.fast(4)")
            await pg.evaluate("""() => { window.__ct = 0; let last = null; clearInterval(window.__ctw);
              window.__ctw = setInterval(() => { const t = __sv.toast; if (t && t !== last && t.startsWith('Contatto')) window.__ct++; last = t; }, 20); }""")
            trovato = False
            for _ in range(60):
                pos = await pg.evaluate("(() => { const me = __sv.R.boats[0].S; let best = null, d = 1e9; for (const o of __sv.R.boats.slice(1)){ const dd = Math.hypot(o.S.x - me.x, o.S.y - me.y); if (dd < d){ d = dd; best = [o.S.x, o.S.y]; } } return best; })()")
                await pg.evaluate(VAI, [[pos], "free"]); await pg.wait_for_timeout(500)
                if await pg.evaluate("__sv.reg.contacts > 0"): trovato = True; await pg.wait_for_timeout(1500); break
            r = await reg(pg); s = await pg.evaluate("[window.__ct, __sv.R.boats[0].pen]")
            verifica("contatto", trovato and r["contacts"] == s[0] and r["contactsPen"] * 15 == s[1], f"registro {r} | contatti annunciati {s[0]} | penalità {s[1]} s")
            await pg.evaluate(FERMA); await pg.evaluate("clearInterval(window.__ctw)")

        if "i" in casi:  # lezioni: l'errore richiesto dal passo non conta, lo stesso errore in un altro passo sì
            async def passo(li, titolo):
                await pg.evaluate(f"__sv.openItem(['l',{li}])")
                for k in range(15):
                    await pg.evaluate(f"__sv.showStep({k})")
                    if (await pg.inner_text("#lTitle")).strip() == titolo: return k
                raise Exception("passo non trovato: " + titolo)
            await pg.evaluate("__sv.fast(3)")
            k = await passo(0, "Orzare e l'angolo morto"); await pg.click("#c")
            await pg.keyboard.down("a"); ok1 = await attendi(pg, "__sv.stepDone", 30); await pg.wait_for_timeout(1500); await pg.keyboard.up("a")
            await pg.evaluate(f"__sv.showStep({k + 1})"); await pg.keyboard.down("d"); await attendi(pg, "__sv.stepDone", 30); await pg.keyboard.up("d")
            r1 = await reg(pg)
            k = await passo(4, "Una virata che non riesce"); await pg.evaluate(VAI, [[], "luff"]); ok2 = await attendi(pg, "__sv.stepDone", 30)
            await pg.evaluate(f"__sv.showStep({k + 1})"); await pg.wait_for_timeout(2000); await pg.evaluate(FERMA)   # ancora piantato nel passo dopo: stesso episodio
            r2 = await reg(pg)
            k = await passo(4, "Strambata violenta"); await pg.evaluate(STRAMBA); ok3 = await attendi(pg, "window.__p2end", 30); await pg.wait_for_timeout(1500); r3 = await reg(pg)
            await pg.evaluate(f"__sv.showStep({k + 1})")   # «Strambata controllata»: se la fai a vela aperta è un errore
            await pg.evaluate(STRAMBA); await attendi(pg, "window.__p2end", 30); await pg.wait_for_timeout(800); r4 = await reg(pg)
            await passo(5, "La scuffia"); await pg.click("#c"); await pg.keyboard.down("ArrowUp"); ok5 = await attendi(pg, "__sv.S.capsized", 60); await pg.keyboard.up("ArrowUp")
            r5 = await reg(pg); txt = await pg.inner_text("#lErr")
            verifica("lezione 1, piantato quando richiesto", ok1 and r1["irons"] == 0, f"passo completato {ok1} | {r1}")
            verifica("lezione 5, virata fallita richiesta", ok2 and r2["irons"] == 0, f"passo completato {ok2} | {r2}")
            verifica("lezione 5, strambata violenta richiesta", ok3 and r3["gybesV"] == 0 and r3["capsizes"] == 0, f"{r3}")
            verifica("lezione 5, strambata a vela aperta nel passo sbagliato", r4["gybesV"] == 1, f"{r4}")
            verifica("lezione 6, scuffia richiesta", ok5 and r5["capsizes"] == 0 and "nessuno" in txt, f"scuffiata {ok5} | {r5} | «{txt}»")
            await pg.evaluate(FERMA)

        print("errori JavaScript:", errs)
        print("ESITO:", f"{sum(esiti)} su {len(esiti)} verifiche riuscite")
        await b.close()
if __name__ == "__main__":
    asyncio.run(main())
