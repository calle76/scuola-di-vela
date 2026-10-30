# Collaudo dei giri di penalità (1.0.61, docs/PROPOSTA-LIVELLO-2A.md, fetta 1). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_giri.py [prove=30] [cartella di una copia di riferimento (1.0.60), per il confronto al bit delle altre regate]
# Parti: A) due giri nello stesso verso estinguono il debito (e quanto tempo costano); B) un giro solo no; C) un giro a destra e uno a sinistra no;
#        D) contatto vero con colpa: debito di due giri e niente +15 s; E) arrivo con il debito aperto: +15 s per giro; F) le altre regate non cambiano;
#        G) registratore: evento giro_penalita; H) pagina come la carica un giocatore (senza #collaudo).
import asyncio, pathlib, sys, os, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata dei giri (indice 3) col pilota fino a 25 s di regata; poi giriDebito() (debito di due giri) e si governa a mano: timone tutto da una parte, vela regolata dal gioco.
# caso: "due" (finché il debito è estinto, massimo 90 s), "uno" (finché ne è fatto uno, poi 20 s di pilota), "opposto" (un giro in un verso, poi una rotazione di 400° nell'altro)
PROVA = """async ([caso, dir, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  const need0 = R.need; giriDebito(); const t0 = R.t, h0 = sv.S.h; let cap = false, rot = 0, hp = sv.S.h;
  const gira = d => { sv.ctl.tiller = d; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; };
  if (caso === 'due'){ while (R.t < t0 + 90 && R.done < R.need && !cap) gira(dir); }
  else { while (R.t < t0 + 60 && R.done < 1 && !cap) gira(dir); }
  const t1 = R.t, done1 = R.done;
  if (caso === 'uno'){ for (let k = 0; k < 60 * 20; k++){ sv.pilota(dt); sv.run(dt, 1); } }
  if (caso === 'opposto'){ hp = sv.S.h; while (R.t < t1 + 60 && Math.abs(rot) < 400 && !cap){ gira(-dir); rot += norm180(sv.S.h - hp); hp = sv.S.h; } }
  return { need0, need: R.need, done: R.done, done1, costo: t1 - t0, cap, giroDir: R.giroDir, pen: me.pen, ruotato: Math.round(rot) };
}"""
# contatto vero: l'avversaria 1 messa a distanza di 3 m, a sopravento o a sottovento del giocatore; contacts() decide la colpa con le regole del gioco
CONTATTO = """async ([lato, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0], o = R.boats[1]; while (R.t < 30){ sv.pilota(dt); sv.run(dt, 1); }
  const needPrima = R.need, penMePrima = me.pen, penOPrima = o.pen, listaPrima = R.penList.length; o.S.h = me.S.h; o.S.u = me.S.u; o.S.x = me.S.x + lato; o.S.y = me.S.y;   // lato: ±1,2 m in x (scafi affiancati e che si toccano)
  for (let k = 0; k < 3; k++){ sv.pilota(dt); sv.run(dt, 1); }
  return { inc: R.need - needPrima, incPenMe: me.pen - penMePrima, incPenO: o.pen - penOPrima, lista: R.penList.slice(listaPrima), regola: R.lastRule, contatti: Object.keys(R.contacts).length };
}"""
# arrivo: pilota fino all'arrivo con un debito di due giri aperto (aperto = true) o già scontato (aperto = false)
ARRIVO = """async ([aperto, seme, solo]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = solo ? 'nessuno' : 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  const need0 = R.need, doneAntes = R.done; giriDebito();
  if (!aperto){ R.done = R.need; giriMsg(); }
  const penPrima = me.pen; let n = 0, maxDone = 0;
  while (R.t < 1500 && me.fin === null && !me.dnf && n < 60 * 900){ sv.pilota(dt); sv.run(dt, 1); n++; if (me.fin === null) maxDone = Math.max(maxDone, R.done); }
  return { need0, doneAntes, need: R.need, done: R.done, maxDone, penPrima, pen: me.pen, fin: me.fin, lista: R.penList.slice() };
}"""
# le altre regate (1a e 1b): arrivi, penalità e posizioni finali, per il confronto al bit con la 1.0.60
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 3]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
# registratore: una regata dei giri con il debito scontato; l'evento e la riga Q devono stare nel file
REGISTRATA = """async ([seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  giriDebito(); let cap = false;
  while (R.t < 25 + 90 && R.done < R.need && !cap){ sv.ctl.tiller = 1; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; }
  sv.run(dt, 120);
  return { done: R.done, need: R.need, testo: regPezzi.length ? regPezzi.map(p => p.testo).join("\\n") : "", auto: ses.auto, testoLive: ses.lines.join("\\n") };
}"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        semi = range(1, n + 1)
        # ---- A ----
        A = [await pg.evaluate(PROVA, ["due", 1 if k % 2 else -1, 100 + k]) for k in semi]
        chk("A1 due giri nello stesso verso estinguono il debito (%d prove senza avversari, %d a destra e %d a sinistra), con debito di partenza di 2 in tutte" % (n, sum(1 for k in semi if k % 2), sum(1 for k in semi if not k % 2)),
            all(r["need0"] == 0 and r["need"] == 2 and r["done"] >= r["need"] for r in A) and len(A) == n, "estinti %d su %d, scuffie %d" % (sum(1 for r in A if r["done"] >= r["need"]), n, sum(1 for r in A if r["cap"])))
        costi = [r["costo"] for r in A if r["done"] >= r["need"]]
        print("     costo dei due giri (s): mediana %.1f, minimo %.1f, massimo %.1f su %d prove (atteso, stima: 15-25)" % (statistics.median(costi), min(costi), max(costi), len(costi)) if costi else "     nessun costo misurabile")
        # ---- B ----
        B = [await pg.evaluate(PROVA, ["uno", 1 if k % 2 else -1, 200 + k]) for k in semi]
        chk("B1 un giro solo non estingue il debito (%d prove senza avversari, debito di partenza 2)" % n, all(r["need0"] == 0 and r["need"] == 2 and r["done1"] == 1 and r["done"] == 1 for r in B) and len(B) == n, "a debito di uno: %d su %d" % (sum(1 for r in B if r["done"] == 1), n))
        # ---- C ----
        C = [await pg.evaluate(PROVA, ["opposto", 1 if k % 2 else -1, 300 + k]) for k in semi]
        chk("C1 un giro in un verso e uno nell'altro non estinguono il debito (%d prove senza avversari)" % n, all(r["done1"] == 1 and r["done"] <= 1 and abs(r["ruotato"]) >= 400 for r in C) and len(C) == n, "ancora a debito: %d su %d; rotazione nel verso opposto media %d°" % (sum(1 for r in C if r["done"] <= 1), n, statistics.mean(abs(r["ruotato"]) for r in C)))
        chk("D0 rotazione di 360° senza virata e senza strambata: non esiste (la prua che fa il giro passa dal vento e da poppa); il criterio 4 della proposta ha 0 casi possibili", True, "dichiarato, non misurabile")
        # ---- D ----
        D = []
        for lato in (1.2, -1.2):
            for k in range(1, 6): D.append((lato, await pg.evaluate(CONTATTO, [lato, 400 + k])))
        colpa = [(l, r) for l, r in D if r["inc"] == 2]
        chk("D1 contatto vero con colpa del giocatore: debito di due giri e nessun +15 s (casi con colpa del giocatore %d su %d, con la flotta)" % (len(colpa), len(D)),
            len(colpa) > 0 and all(r["incPenMe"] == 0 and any("Tu, contatto" in x for x in r["lista"]) and "due giri" in (r["regola"] or "") for l, r in colpa), "lati con colpa: %s" % sorted({l for l, r in colpa}))
        senza = [(l, r) for l, r in D if r["inc"] == 0 and r["contatti"]]
        chk("D2 contatto con colpa dell'avversaria: nessun debito per il giocatore e +15 s all'avversaria (casi %d)" % len(senza), len(senza) > 0 and all(r["incPenO"] == 15 and r["incPenMe"] == 0 for l, r in senza))
        chk("D3 ogni contatto dà al massimo un debito di due giri (nessun incremento diverso da 0 o 2)", all(r["inc"] in (0, 2) for l, r in D), str(sorted({r["inc"] for l, r in D})))
        # ---- E ----
        E1 = [await pg.evaluate(ARRIVO, [True, 500 + k, True]) for k in range(1, 7)]; E0 = [await pg.evaluate(ARRIVO, [False, 600 + k, True]) for k in range(1, 7)]
        chk("E1 arrivo senza avversari con il debito di due giri aperto: +30 s e la voce nell'elenco (6 regate)", all(r["fin"] is not None and r["need0"] == 0 and r["pen"] - r["penPrima"] == 30 and any("giri di penalità non fatti (2)" in x for x in r["lista"]) for r in E1))
        chk("E2 arrivo con il debito già scontato: nessun secondo in più (6 regate)", all(r["fin"] is not None and r["pen"] == r["penPrima"] and not any("non fatti" in x for x in r["lista"]) for r in E0))
        K = [await pg.evaluate(ARRIVO, [True, 800 + k, False]) for k in range(1, n + 1)]
        chk("K1 nessun giro spurio: con il debito aperto e il pilota che non fa giri a posta, in %d regate con la flotta nessun giro viene riconosciuto DOPO il debito e prima dell'arrivo" % n, len(K) == n and all(r["fin"] is not None and r["need"] >= 2 for r in K) and all(r["maxDone"] - r["doneAntes"] == 0 for r in K), "giri spuri dopo il debito: %d regate su %d; giri veri già fatti dal pilota prima del debito (colpa nel conto alla rovescia e girata su se stesso): %d regate su %d" % (sum(1 for r in K if r["maxDone"] - r["doneAntes"] > 0), n, sum(1 for r in K if r["doneAntes"] > 0), n))
        # ---- G ----
        G = await pg.evaluate(REGISTRATA, [700])
        chk("G1 registratore: giro_penalita 1/2 e 2/2 e la riga «penalità scontata» nel file", G["done"] >= G["need"] and "giro_penalita 1/2" in (G["testo"] + G["testoLive"]) and "giro_penalita 2/2" in (G["testo"] + G["testoLive"]) and "penalità scontata" in (G["testo"] + G["testoLive"]),
            "pezzi %d" % len(G["testo"].split("registrazione di regata")) if G["testo"] else "file ancora aperto")
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- F ----
        ctx, pg, errs = await pagina(b, ROOT); nuovo = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
        if rif:
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); vecchio = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
            chk("F1 regate dell'1a e dell'1b: arrivi, penalità e posizioni finali identici al bit alla 1.0.60 su 20 regate", nuovo == vecchio and len(nuovo) == 20)
        else: print("     F1 saltato: manca la cartella di riferimento")
        # ---- H ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        titoli = await pg.evaluate("() => [...document.querySelectorAll('#menu [data-r]')].map(e => e.querySelector('.title').textContent)")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => ({ giri: R && R.giri, need: R && R.need, mode: mode, titolo: document.getElementById('rTitle').textContent })")
        chk("H1 pagina senza #collaudo: la regata «Regata con i giri di penalità» è nel menu, si apre e ha i giri attivi", "Regata con i giri di penalità" in titoli and h["giri"] and h["need"] == 0 and h["mode"] == "race", str(h))
        await pg.evaluate("() => { const o = R.boats[0]; giriDebito(); toast('prova'); racePanel(); }")
        r = await pg.evaluate("() => ({ regola: document.getElementById('rRule').textContent, nascosta: document.getElementById('rRule').hidden })")
        chk("H2 il debito compare nella riga delle regole del pannello", (not r["nascosta"]) and "giri" in r["regola"], r["regola"][:90])
        chk("H3 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
