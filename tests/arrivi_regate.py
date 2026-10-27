# Impronta delle regate per la pulizia di js/regate.js (27 ottobre 2026): scrive su un file gli arrivi di 20 regate e di 2 tornei,
# a seme fisso e con il pilota sostituto alla guida, per confrontare il file di PRIMA con quello di DOPO (diff): devono essere identici.
# Per ogni regata: tempo d'arrivo di ogni barca (a piena precisione), penalità, partenze anticipate, boe sbagliate, elenco delle penalità
# col motivo, introduzione, testo del risultato, classifica e dati salvati. Per i tornei: HTML del pannello a ogni regata.
# T2i: stampa «regate del torneo valide N su 8» (titolo «Torneo…, regata k di 4», 4 titoli diversi, giocatore arrivato o ritirato).
# Uso: python tests/arrivi_regate.py <file di uscita>
#   regate: bastone (7), raffiche (7) e salti di vento dell'1b (6); semi 1-N, i primi principianti, gli ultimi esperti; poi 9 introduzioni
#   (3 regate × 3 livelli) e 2 tornei da 4 regate.
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
PIANO = [(0, list(range(1, 8)), 4), (1, list(range(1, 8)), 4), (2, list(range(1, 7)), 3)]   # (regata, semi, quanti principianti)

SCHEDA = """b => ({ name: b.name, fin: b.fin, pen: b.pen, pp: b.pp || 0, ocs: !!b.ocs, dnf: !!b.dnf, wm: b.wrongMarks || 0, leg: b.leg })"""
CORSA = """([seme, liv]) => {
  const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.simTime = 0;   // simTime a zero: raffiche e salti di vento dipendono dall'orologio del gioco
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));   // riparte col seme
  const R = sv.R, me = R.boats[0];
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ sv.pilota(dt); sv.run(dt, 1); }
  sv.panel();
  const sch = %s;
  return { t: Math.round(R.t * 1000), boats: R.boats.map(sch), pen: R.penList, brief: R.brief, done: document.getElementById("rDoneText").textContent,
           stand: document.getElementById("standings").innerHTML, finPen: document.getElementById("finPen").innerHTML, rule: R.lastRule || null,
           prog: localStorage.getItem("scuolaVelaSim.v1") };
}""" % SCHEDA
INTRO = """async ([i, liv]) => {
  const sv = __sv; sv.fast(0); __seed(77 + i); sv.simTime = 0;
  sv.openItem(["r", i]);
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  return sv.R.brief;
}"""
TORNEO_RUN = """seme => {
  const sv = __sv, dt = 1 / 60; sv.simTime = 0; __seed(seme);   // il seme a ogni regata: i fotogrammi fra una chiamata e l'altra consumano numeri a caso
  document.getElementById("torGo").click();   // corre davvero la regata del torneo (fino al 27 ottobre era dentro il commento qui sopra)
  const R = sv.R, me = R.boats[0];
  while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); }
  const brief = R.brief;
  document.getElementById("rTor").click();
  const sch = %s;
  return { brief, t: Math.round(R.t * 1000), boats: R.boats.map(sch), pen: R.penList, done: document.getElementById("rDoneText").textContent,
           html: document.getElementById("torBody").innerHTML, prog: localStorage.getItem("scuolaVelaSim.v1") };
}""" % SCHEDA

async def main(uscita):
    righe = []; tornei_ok = 0; barche = 0; penal = 0; con_contatti = 0; errori = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        async def pagina():
            ctx = await b.new_context(viewport={"width": 1280, "height": 800}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errori.append(str(e)))
            pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
            return ctx, pg
        for race, semi, npr in PIANO:
            for k, seme in enumerate(semi):
                ctx, pg = await pagina()
                await pg.click("[data-r='%d']" % race); await pg.wait_for_timeout(100)
                r = await pg.evaluate(CORSA, [seme, "principianti" if k < npr else "esperti"])
                righe.append("regata %d seme %d %s" % (race, seme, json.dumps(r, sort_keys=True, ensure_ascii=False)))
                barche += len(r["boats"]); penal += len(r["pen"]); con_contatti += 1 if r["pen"] else 0
                await ctx.close()
        ctx, pg = await pagina()
        for i in range(3):
            for liv in ["nessuno", "principianti", "esperti"]:
                righe.append("intro %d %s %s" % (i, liv, json.dumps(await pg.evaluate(INTRO, [i, liv]), ensure_ascii=False)))
        await ctx.close()
        for t, liv in enumerate(["principianti", "esperti"]):
            ctx, pg = await pagina()
            await pg.evaluate("([s, l]) => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; const e = document.getElementById('aiLevel'); e.value = l; e.dispatchEvent(new Event('change')); __sv.torApri(); }", [500 + t, liv])
            righe.append("torneo %d inizio %s" % (t, await pg.evaluate("document.getElementById('torBody').innerHTML")))
            titoli = []
            for k in range(4):
                r = await pg.evaluate(TORNEO_RUN, 900 + 10 * t + k)
                titoli.append(r["brief"])
                if ("regata %d di 4" % (k + 1)) in r["brief"] and r["brief"].startswith("Torneo") and (r["boats"][0]["fin"] is not None or r["boats"][0]["dnf"]): tornei_ok += 1   # T2i
                righe.append("torneo %d regata %d %s" % (t, k, json.dumps(r, sort_keys=True, ensure_ascii=False)))
                barche += len(r["boats"]); penal += len(r["pen"]); con_contatti += 1 if r["pen"] else 0
            if len(set(titoli)) != 4: tornei_ok -= 4   # 4 regate uguali: il torneo non è stato corso
            await ctx.close()
        await b.close()
    pathlib.Path(uscita).write_text("\n".join(righe) + "\n")
    print(f"T2i regate del torneo valide {tornei_ok} su 8 ({'OK' if tornei_ok == 8 else 'FALLITO'}); righe {len(righe)}, barche {barche}, penalità con motivo {penal}, regate con almeno un contatto {con_contatti}, errori della pagina {errori[:2]}")
asyncio.run(main(sys.argv[1]))
