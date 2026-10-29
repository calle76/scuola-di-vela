# Collaudo della moviola (1.0.58, docs/PROPOSTA-COACH-REGISTRATORE.md): fedeltà delle posizioni, gioco identico a prima, uscita pulita.
# Uso: .venv-collaudi/bin/python tests/collaudo_moviola.py [semi=10] [cartella di una copia di riferimento senza moviola, per il confronto al bit]
import asyncio, json, pathlib, sys, os, time
from playwright.async_api import async_playwright
ROOT = pathlib.Path("/home/callle/scuola-di-vela")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata del torneo col pilota; premi O (se il gioco ha la moviola) a 40 s e a 90 s; ritorna esito e, se c'è, la verifica della riproduzione
RUN = """async ([seme, conMov]) => {
  const sv = __sv, dt = 1 / 60; sv.simTime = 0; __seed(seme);
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], truth = [], t0 = performance.now(); let n = 0, k = 0;
  while (R.t < 1500 && me.fin === null && !me.dnf){
    sv.pilota(dt); sv.run(dt, 1); n++;
    if (R.t > 0 && n % 60 === 0) truth.push([R.t, R.boats.map(b => [b.S.x, b.S.y, b.S.h])]);
    if (conMov && R.phase === "race" && (Math.abs(R.t - 40) < dt / 2 || Math.abs(R.t - 90) < dt / 2)) window.dispatchEvent(new KeyboardEvent("keydown", { key: "o" }));
  }
  const ms = performance.now() - t0;
  const out = { fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), ms, passi: n };
  if (!conMov){ document.getElementById("rTor").click(); return out; }
  racePanel();
  out.bottone = !document.getElementById("finRev").hidden; out.spezzoni = riv.snips.length + riv.pend.length;
  out.auto = riv.snips.filter(s => s.auto).length;
  const prima = JSON.stringify(R.boats.map(b => b.S)), wprima = R.boats.map(b => b.wake.length).join();
  rivApri();
  out.aperta = riv.on; out.finOvNascosta = document.getElementById("finOv").hidden; out.barra = !document.getElementById("movBar").hidden;
  let errPos = 0, errH = 0, nc = 0;
  for (let i = 0; i < riv.snips.length; i++){ riv.i = i; const fr = riv.snips[i].frames;
    for (const [t, b] of truth){ if (t < fr[0].t || t > fr[fr.length - 1].t) continue; riv.pos = t - fr[0].t; rivApplica(); nc++;
      R.boats.forEach((bt, j) => { errPos = Math.max(errPos, Math.hypot(bt.S.x - b[j][0], bt.S.y - b[j][1])); errH = Math.max(errH, Math.abs(norm180(bt.S.h - b[j][2]))); }); } }
  out.errPos = errPos; out.errH = errH; out.confronti = nc;
  riv.i = 0; rivApplica(); window.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowRight" })); out.dopoFreccia = riv.i;
  window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
  out.chiusa = !riv.on; out.stessoStato = JSON.stringify(R.boats.map(b => b.S)) === prima; out.stesseScie = R.boats.map(b => b.wake.length).join() === wprima;
  out.finOvDi_nuovo = !document.getElementById("finOv").hidden; out.barraNascosta = document.getElementById("movBar").hidden;
  document.getElementById("rTor").click();
  return out;
}"""
async def gira(base, semi, conMov):
    ris = []
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for t in semi:
            ctx = await b.new_context(viewport={"width": 1280, "height": 800}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(pathlib.Path(base, "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(200)
            await pg.evaluate("([s, l]) => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; const e = document.getElementById('aiLevel'); e.value = l; e.dispatchEvent(new Event('change')); __sv.torApri(); }", [t, "principianti"])
            r = await pg.evaluate(RUN, [5000 + t, conMov]); r["seme"] = t; r["errori_pagina"] = errs; ris.append(r)
            await ctx.close()
        await b.close()
    return ris
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    semi = range(1, n + 1)
    nuovo = await gira(ROOT, semi, True)
    bad = []
    def chk(nome, ok, extra=""):
        print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else "")); 
        if not ok: bad.append(nome)
    chk("nessun errore di pagina", all(not r["errori_pagina"] for r in nuovo), str([r["errori_pagina"] for r in nuovo if r["errori_pagina"]][:2]))
    con = [r for r in nuovo if r["spezzoni"] > 0]
    chk("spezzoni presenti in tutte le regate (2 segni O a 40 e 90 s)", len(con) == len(nuovo) and all(r["spezzoni"] >= 2 for r in nuovo), "spezzoni per regata: " + str([r["spezzoni"] for r in nuovo]))
    chk("pulsante Rivedi visibile a fine regata", all(r["bottone"] for r in nuovo))
    chk("moviola si apre, schermata finale nascosta, barra visibile", all(r["aperta"] and r["finOvNascosta"] and r["barra"] for r in nuovo))
    chk("fedeltà: posizione entro 0,5 m e prua entro 5° (confronti %d)" % sum(r["confronti"] for r in nuovo), sum(r["confronti"] for r in nuovo) > 0 and max(r["errPos"] for r in nuovo) <= 0.5 and max(r["errH"] for r in nuovo) <= 5,
        "massimo %.3f m, %.2f°" % (max(r["errPos"] for r in nuovo), max(r["errH"] for r in nuovo)))
    chk("freccia destra passa al momento dopo", all(r["dopoFreccia"] == min(1, r["spezzoni"] - 1) for r in nuovo))
    chk("uscita pulita: stato e scie identici, schermata finale di nuovo visibile", all(r["chiusa"] and r["stessoStato"] and r["stesseScie"] and r["finOvDi_nuovo"] and r["barraNascosta"] for r in nuovo))
    print("contatti automatici negli spezzoni:", sum(r["auto"] for r in nuovo), "su", len(nuovo), "regate")
    if rif:
        vecchio = await gira(rif, semi, False)
        uguali = all(a["fin"] == b["fin"] and a["pen"] == b["pen"] and a["pp"] == b["pp"] and a["fine"] == b["fine"] and a["passi"] == b["passi"] for a, b in zip(nuovo, vecchio))
        chk("gioco identico al bit con la moviola (arrivi, penalità, posizioni finali) su %d regate" % len(nuovo), uguali)
        tn, tv = sum(r["ms"] for r in nuovo), sum(r["ms"] for r in vecchio)
        print("tempo di calcolo: con moviola %.1f s, senza %.1f s (%+.1f%%)" % (tn / 1000, tv / 1000, 100 * (tn - tv) / tv))
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
