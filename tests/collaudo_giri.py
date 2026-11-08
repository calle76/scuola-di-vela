# Collaudo dei giri di penalità (1.0.61, docs/PROPOSTA-LIVELLO-2A.md, fetta 1). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_giri.py [prove=30] [cartella di una copia di riferimento (1.0.60), per il confronto al bit delle altre regate]
# Parti: A) due giri nello stesso verso estinguono il debito (e quanto tempo costano); B) un giro solo no; C) un giro a destra e uno a sinistra no;
#        D) contatto vero con colpa: debito di due giri e niente +15 s; E) arrivo con il debito aperto: +15 s per giro; F) le altre regate non cambiano;
#        G) registratore: evento giro_penalita; H) pagina come la carica un giocatore (senza #collaudo).
import asyncio, pathlib, sys, os, statistics
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata dei giri (indice 3) col pilota fino a 25 s di regata; poi giriDebito() (debito di due giri) e si governa a mano: timone tutto da una parte, vela regolata dal gioco.
# caso: "due" (finché il debito è estinto, massimo 90 s), "uno" (finché ne è fatto uno, poi 20 s di pilota), "opposto" (un giro in un verso, poi una rotazione di 400° nell'altro),
#       "dopo" (1.0.74, osservazione 72: prima penalità scontata in un verso, poi una seconda penalità e i suoi giri nel verso opposto)
PROVA = """async ([caso, dir, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  const need0 = R.need; giriDebito(); const t0 = R.t, h0 = sv.S.h; let cap = false, rot = 0, hp = sv.S.h;
  const gira = d => { sv.ctl.tiller = d; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; };
  let prima = null, base = null, fatti0 = null, dopo1 = null;
  if (caso === 'due'){ while (R.t < t0 + 90 && R.done < R.need && !cap) gira(dir); }
  else if (caso === 'dopo'){
    while (R.t < t0 + 90 && R.done < R.need && !cap) gira(dir);
    prima = R.done; giriDebito(); base = R.base; fatti0 = R.done - R.base; const t2 = R.t;
    while (R.t < t2 + 60 && R.done === prima && !cap) gira(-dir); dopo1 = R.done;   // il conto dopo il PRIMO giro opposto
    while (R.t < t2 + 120 && R.done < R.need && !cap) gira(-dir);
  }
  else { while (R.t < t0 + 60 && R.done < 1 && !cap) gira(dir); }
  const t1 = R.t, done1 = R.done;
  if (caso === 'uno'){ for (let k = 0; k < 60 * 20; k++){ sv.pilota(dt); sv.run(dt, 1); } }
  if (caso === 'opposto'){ hp = sv.S.h; while (R.t < t1 + 60 && Math.abs(rot) < 400 && !cap){ gira(-dir); rot += norm180(sv.S.h - hp); hp = sv.S.h; } }
  return { need0, need: R.need, done: R.done, done1, costo: t1 - t0, cap, giroDir: R.giroDir, pen: me.pen, ruotato: Math.round(rot), prima, base, fatti0, dopo1, lista: R.penList.slice() };
}"""
# contatto vero: l'avversaria 1 messa a distanza di 3 m, a sopravento o a sottovento del giocatore; contacts() decide la colpa con le regole del gioco
CONTATTO = """async ([lato, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0], o = R.boats[1]; while (R.t < 30){ sv.pilota(dt); sv.run(dt, 1); }
  const needPrima = R.need, penMePrima = me.pen, penOPrima = o.pen, debOPrima = o.gDebt || 0, listaPrima = R.penList.length; o.S.h = me.S.h; o.S.u = me.S.u; o.S.x = me.S.x + lato; o.S.y = me.S.y;   // lato: ±1,2 m in x (scafi affiancati e che si toccano)
  for (let k = 0; k < 3; k++){ sv.pilota(dt); sv.run(dt, 1); }
  return { inc: R.need - needPrima, incPenMe: me.pen - penMePrima, incPenO: o.pen - penOPrima, incDebO: (o.gDebt || 0) - debOPrima, lista: R.penList.slice(listaPrima), regola: R.lastRule, contatti: Object.keys(R.contacts).length };
}"""
# 1.2.16 (docs/PROPOSTA-GIRI-GIOCATORE.md, G2-G6): dopo il debito si gira con la barra a «barra» (frazione); caso "lento" fino alla penalità scontata; caso numero = sosta
# di tanti secondi a barra al centro a metà giro (180°); caso "indietro" = a metà giro 40° nel verso opposto. Poi di nuovo nel verso fino a 400° netti.
# (La prima versione metteva la sosta dopo la prima virata: il pilota a volte stramba prima e vira a 315°, o vira subito, e la sosta cadeva fuori dal giro.)
# Restituisce anche il testo registrato, per confrontare tests/misura_giri_giocatore.py con il gioco (parte M).
LENTO = """async ([caso, dir, seme, barra]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  const pz0 = new Set(regPezzi); giriDebito(); const t0 = R.t; let cap = false, rot = 0, hp = sv.S.h, rv = 0; const giri = [], dur = []; let tg = t0, dPrima = R.done;
  const passo = d => { sv.ctl.tiller = d; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; rot += norm180(sv.S.h - hp); hp = sv.S.h;
    if (R.done > dPrima){ giri.push(+R.t.toFixed(2)); dur.push(+(R.t - tg).toFixed(1)); tg = R.t; dPrima = R.done; } };
  const fase = []; // per la diagnosi: [t, prua, giro.cum, secondi da quando la prua è avanzata] ogni mezzo secondo nella sosta
  if (caso === 'lento'){ while (R.t < t0 + 200 && R.done < R.need && !cap) passo(dir * barra); }
  else {
    while (R.t < t0 + 60 && Math.abs(rot) < 180 && !cap) passo(dir * barra);
    rv = Math.sign(rot) || 1; const r0 = rot * rv;
    if (caso === 'indietro'){ while (R.t < t0 + 120 && rot * rv > r0 - 40 && !cap) passo(-dir * barra); }
    else { // la sosta si conta da quando la barca smette davvero di girare (sotto 2,5°/s su 1 s): con la barra al centro ruota ancora per inerzia, e allora gira (Ale, 8 novembre: scelta A)
      const yaw = []; let ts = null, k = 0;
      while (!cap && (ts === null || R.t < ts + caso) && R.t < t0 + 120){ const h0 = sv.S.h; passo(0); yaw.push(Math.abs(norm180(sv.S.h - h0)) / dt); if (yaw.length > 60) yaw.shift();
        if (ts === null && yaw.length === 60 && yaw.reduce((a, b) => a + b, 0) / 60 < 2.5) ts = R.t;
        if (k++ % 30 === 0) fase.push([+R.t.toFixed(1), Math.round(sv.S.h), Math.round(R.giro.cum), +(R.t - R.giro.tA).toFixed(1)]); } }
    while (R.t < t0 + 200 && rot * rv < 400 && R.done < 1 && !cap) passo(dir * barra);
  }
  for (let k = 0; k < 120; k++){ sv.ctl.tiller = 0; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); } // 2 s dritti: il registratore (una riga ogni 0,1 s) deve contenere anche l'istante in cui il gioco ha contato il giro
  const nuovi = regPezzi.filter(p => !pz0.has(p)); // solo i pezzi di questa regata: nella stessa pagina restano quelli delle prove di prima
  const testo = (nuovi.length ? nuovi.map(p => p.testo).join("\\n") + "\\n" : "") + ses.lines.join("\\n");
  return { t0, need: R.need, done: R.done, giri, dur, cap, netto: Math.round(Math.abs(rot)), testo, fase };
}"""
# arrivo: pilota fino all'arrivo con un debito di due giri aperto (aperto = true) o già scontato (aperto = false)
ARRIVO = """async ([aperto, seme, solo]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = solo ? 'nessuno' : 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  const need0 = R.need, doneAntes = R.done; giriDebito();
  if (!aperto){ R.done = R.need; giriMsg(); }
  const penPrima = me.pen; let n = 0, maxDone = 0, dp = R.done; const storia = [], veri = [];
  while (R.t < 1500 && me.fin === null && !me.dnf && n < 60 * 900){ const hp = sv.S.h, tkp = sv.S.tacks, gyp = sv.S.gybesC + sv.S.gybesV; sv.pilota(dt); sv.run(dt, 1); n++;
    storia.push([R.t, norm180(sv.S.h - hp), sv.S.tacks - tkp, sv.S.gybesC + sv.S.gybesV - gyp]); while (storia.length && R.t - storia[0][0] > 60) storia.shift();
    if (me.fin === null) maxDone = Math.max(maxDone, R.done);
    if (me.fin === null && R.done > dp){ // 1.2.16, K1: un giro riconosciuto è vero se negli ultimi 60 s, a ritroso, la prua arriva a 360° netti nello stesso verso passando da una virata e una strambata (misura del collaudo, non il conto del gioco)
      let c = 0, tk = 0, gy = 0, ok = false; for (let i = storia.length - 1; i >= 0; i--){ c += storia[i][1]; tk += storia[i][2]; gy += storia[i][3]; if (Math.abs(c) >= 355 && tk > 0 && gy > 0){ ok = true; break; } }
      veri.push(ok); dp = R.done; } }
  return { need0, doneAntes, need: R.need, done: R.done, maxDone, penPrima, pen: me.pen, fin: me.fin, lista: R.penList.slice(), dsq: !!me.dsq, veri, ultimo: ranking().indexOf(me) === R.boats.length - 1, n: R.boats.length, testoArrivo: document.getElementById("rDoneText").textContent };
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
            metro.tutti(r["need0"] == 0 and r["need"] == 2 and r["done"] >= r["need"] for r in A) and len(A) == n, "estinti %d su %d, scuffie %d" % (sum(1 for r in A if r["done"] >= r["need"]), n, sum(1 for r in A if r["cap"])))
        costi = [r["costo"] for r in A if r["done"] >= r["need"]]
        print("     costo dei due giri (s): mediana %.1f, minimo %.1f, massimo %.1f su %d prove (atteso, stima: 15-25)" % (statistics.median(costi), min(costi), max(costi), len(costi)) if costi else "     nessun costo misurabile")
        # ---- B ----
        B = [await pg.evaluate(PROVA, ["uno", 1 if k % 2 else -1, 200 + k]) for k in semi]
        chk("B1 un giro solo non estingue il debito (%d prove senza avversari, debito di partenza 2)" % n, metro.tutti(r["need0"] == 0 and r["need"] == 2 and r["done1"] == 1 and r["done"] == 1 for r in B) and len(B) == n, "a debito di uno: %d su %d" % (sum(1 for r in B if r["done"] == 1), n))
        # ---- P (1.0.74, osservazione 72) ----
        # criterio scritto prima di misurare: in tutte le prove, prima penalità scontata (2 giri), seconda penalità: debito 4, base 2, «fatti» 0;
        # il primo giro nel verso opposto lascia 1 giro (fatti 3), il secondo la sconta (fatti 4); l'elenco dice «penalità scontata: 2 giri» due volte
        P = [await pg.evaluate(PROVA, ["dopo", 1 if k % 2 else -1, 500 + k]) for k in semi]
        chk("P1 penalità nuova dopo una scontata, giri nel verso opposto: il conto non torna a 1 (%d prove senza avversari)" % n,
            metro.tutti(r["prima"] == 2 and r["need"] == 4 and r["base"] == 2 and r["fatti0"] == 0 and r["dopo1"] == 3 and r["done"] == 4 and not r["cap"] for r in P) and len(P) == n,
            "giusti %d su %d; dopo il primo giro opposto: %s; scuffie %d" % (sum(1 for r in P if r["dopo1"] == 3 and r["done"] == 4), n, sorted({r["dopo1"] for r in P}), sum(1 for r in P if r["cap"])))
        chk("P2 l'elenco di fine regata dice due volte «penalità scontata: 2 giri» (non «4 giri») (%d prove)" % n,
            metro.tutti([x for x in r["lista"] if x.startswith("Tu, penalità scontata")] == ["Tu, penalità scontata: 2 giri."] * 2 for r in P) and len(P) == n)
        # ---- C ----
        C = [await pg.evaluate(PROVA, ["opposto", 1 if k % 2 else -1, 300 + k]) for k in semi]
        chk("C1 un giro in un verso e uno nell'altro non estinguono il debito (%d prove senza avversari)" % n, metro.tutti(r["done1"] == 1 and r["done"] <= 1 and abs(r["ruotato"]) >= 400 for r in C) and len(C) == n, "ancora a debito: %d su %d; rotazione nel verso opposto media %d°" % (sum(1 for r in C if r["done"] <= 1), n, statistics.mean(abs(r["ruotato"]) for r in C)))
        chk("D0 rotazione di 360° senza virata e senza strambata: non esiste (la prua che fa il giro passa dal vento e da poppa); il criterio 4 della proposta ha 0 casi possibili", True, "dichiarato, non misurabile")
        # ---- D ----
        D = []
        for lato in (1.2, -1.2):
            for k in range(1, 6): D.append((lato, await pg.evaluate(CONTATTO, [lato, 400 + k])))
        colpa = [(l, r) for l, r in D if r["inc"] == 2]
        chk("D1 contatto vero con colpa del giocatore: debito di due giri e nessun +15 s (casi con colpa del giocatore %d su %d, con la flotta)" % (len(colpa), len(D)),
            len(colpa) > 0 and metro.tutti(r["incPenMe"] == 0 and any("Tu, contatto" in x for x in r["lista"]) and "due giri" in (r["regola"] or "") for l, r in colpa), "lati con colpa: %s" % sorted({l for l, r in colpa}))
        senza = [(l, r) for l, r in D if r["inc"] == 0 and r["contatti"]]
        chk("D2 contatto con colpa dell'avversaria: nessun debito per il giocatore e, dalla 1.0.67, due giri di debito all'avversaria e nessun +15 s (prima: +15 s) (casi %d)" % len(senza), len(senza) > 0 and metro.tutti(r["incDebO"] == 2 and r["incPenO"] == 0 and r["incPenMe"] == 0 and r["inc"] == 0 for l, r in senza))
        chk("D3 ogni contatto dà al massimo un debito di due giri (nessun incremento diverso da 0 o 2)", metro.tutti(r["inc"] in (0, 2) for l, r in D), str(sorted({r["inc"] for l, r in D})))
        # ---- E ----
        E1 = [await pg.evaluate(ARRIVO, [True, 500 + k, True]) for k in range(1, 7)]; E0 = [await pg.evaluate(ARRIVO, [False, 600 + k, True]) for k in range(1, 7)]
        # 1.1.1: il pilota può prendere anche un giro per la boa toccata (regola 31) dopo il debito costruito (in Firefox, seme 501): 15 s per ogni giro non fatto, almeno i 2 del debito
        # 1.2.16 (decisione di Ale, 8 novembre): con giri non fatti il giocatore è squalificato (prima: 15 s per giro). G13 di docs/PROPOSTA-GIRI-GIOCATORE.md
        chk("E1 arrivo senza avversari con il debito di due giri aperto: squalificato, nessun secondo in più, la voce «squalifica» nell'elenco e il messaggio d'arrivo (6 regate)", metro.tutti(r["fin"] is not None and r["need0"] == 0 and r["need"] - r["doneAntes"] >= 2 and r["maxDone"] == 0 and r["dsq"] and r["pen"] == r["penPrima"] and any(f"giri di penalità non fatti ({r['need'] - r['doneAntes']}): squalifica" in x for x in r["lista"]) and r["testoArrivo"].startswith("Squalificato") for r in E1))
        chk("E2 arrivo con il debito già scontato: nessun secondo in più, non squalificato (6 regate)", metro.tutti(r["fin"] is not None and r["pen"] == r["penPrima"] and not r["dsq"] and not any("non fatti" in x for x in r["lista"]) and not r["testoArrivo"].startswith("Squalificato") for r in E0))
        # 1.0.64: il pilota di prova, partito in anticipo, può restare incastrato contro il comitato (ostacolo): K1 accetta al più una regata su dieci non arrivata, contata a parte
        K = [await pg.evaluate(ARRIVO, [True, 1800 + k, False]) for k in range(1, n + 1)]   # 1.2.16: semi nuovi (prima 801-830, guardati con la prima versione)
        Kd = [r for r in K if r["fin"] is not None and r["dsq"]]   # all'arrivo R.done = R.need: il debito aperto si legge da dsq
        chk("E3 con la flotta, arrivo con giri non fatti: squalificato e ultimo in classifica (%d regate su %d)" % (len(Kd), n), len(Kd) > 0 and metro.tutti(r["ultimo"] and r["pen"] == r["penPrima"] for r in Kd))
        # 1.2.16 (Ale, 8 novembre: «sì a tutte e due»): senza limite di durata un cerchio vero del pilota (attorno alla boa, 360° con virata e strambata) conta come giro, come nella realtà.
        # K1 riscritto, soglia dichiarata dopo aver visto 2 regate su 30 con la prima versione: al massimo 3 regate su 30 con giri riconosciuti, e ognuno è un giro vero (misura del collaudo)
        conGiri = [r for r in K if r["maxDone"] - r["doneAntes"] > 0]
        chk("K1 giri riconosciuti senza volerlo, con il debito aperto e il pilota: al massimo 3 regate su %d, e ognuno è un giro vero (360° netti nello stesso verso in meno di 60 s, con virata e strambata)" % n,
            len(K) == n and sum(1 for r in K if r["fin"] is not None) >= n - max(1, n // 10) and metro.tutti(r["need"] >= 2 for r in K) and len(conGiri) <= 3 and all(all(r["veri"]) for r in conGiri),
            "regate con giri riconosciuti: %d su %d; giri riconosciuti %d, veri %d; regate non arrivate %d" % (len(conGiri), n, sum(len(r["veri"]) for r in K), sum(sum(r["veri"]) for r in K), sum(1 for r in K if r["fin"] is None)))
        # ---- L (1.2.16, G2-G5) e M (G6) ----
        import misura_giri_giocatore as mg
        BARRA = float(os.environ.get("BARRA_LENTA", "0.35"))
        L2 = [await pg.evaluate(LENTO, ["lento", 1 if k % 2 else -1, 1900 + k, BARRA]) for k in range(1, 11)]
        dur = [d for r in L2 for d in r["dur"]]
        print("     giri lenti, barra %.2f: durate (s) %s" % (BARRA, sorted(dur)))
        chk("L2 giri lenti (barra %.2f, durata 25-35 s attesa) contano: penalità scontata in 10 prove su 10" % BARRA, len(L2) == 10 and metro.tutti(r["done"] >= r["need"] and not r["cap"] for r in L2), "scontate %d su 10, durate mediana %.1f s" % (sum(1 for r in L2 if r["done"] >= r["need"]), statistics.median(dur) if dur else 0))
        L3 = [await pg.evaluate(LENTO, [5, 1 if k % 2 else -1, 1920 + k, 1]) for k in range(1, 11)]
        L4 = [await pg.evaluate(LENTO, [15, 1 if k % 2 else -1, 1940 + k, 1]) for k in range(1, 11)]
        # L3 e L4 valgono solo dove la barca ha davvero girato (L3 un giro intero, L4 400° netti): in qualche prova, dopo la sosta, la barca si pianta nella virata e non finisce il giro
        # (semi 1930 e 1950, 264-267°): lì il gioco giustamente non conta niente e la prova non misura la sosta. Cambio del collaudo dichiarato (8 novembre), soglie non toccate
        V3 = [r for r in L3 if r["netto"] >= 355 and not r["cap"]]   # L3: la prova si ferma quando il giro è contato (360°): valida se la barca ha girato un giro intero
        V4 = [r for r in L4 if (r["netto"] >= 400 or r["done"] > 0) and not r["cap"]]   # L4: anche la prova fermata perché il giro è stato contato è valida (e sbagliata): prima la scartava (Firefox, 8 novembre)
        chk("L3 sosta di 5 s a metà giro (contata da quando la barca smette di girare): il giro conta (tutte le prove valide, almeno 8 su 10)", len(V3) >= 8 and metro.tutti(r["done"] == 1 for r in V3), "valide %d su 10 (le altre si piantano prima di un giro intero: %s), contati %d su %d" % (len(V3), [r["netto"] for r in L3 if r not in V3], sum(1 for r in V3 if r["done"] == 1), len(V3)))
        chk("L4 sosta di 15 s a metà giro (contata da quando la barca smette di girare): il giro non conta entro 400° netti (tutte le prove valide, almeno 8 su 10)", len(V4) >= 8 and metro.tutti(r["done"] == 0 for r in V4), "valide %d su 10 (le altre: %s), non contati %d su %d" % (len(V4), [r["netto"] for r in L4 if r not in V4], sum(1 for r in V4 if r["done"] == 0), len(V4)))
        L5 = [await pg.evaluate(LENTO, ["indietro", 1 if k % 2 else -1, 1960 + k, 1]) for k in range(1, 11)]
        chk("L5 40° indietro a metà giro: il giro non conta entro 400° netti (10 su 10)", metro.tutti(r["done"] == 0 and not r["cap"] for r in L5) and len(L5) == 10, "non contati %d su 10" % sum(1 for r in L5 if r["done"] == 0))
        uguali = 0; tot = 0; limite = 0
        for r in L2 + L3 + L4 + L5:
            gm = mg.giri2(r["testo"].split("\n"), 8, t_debito=r["t0"] - 0.05, need_debito=r["need"]); tot += 1
            stessi = lambda x: len(x) == len(r["giri"]) and all(abs(a - b) <= 0.5 for a, b in zip(x, r["giri"]))
            if stessi(gm): uguali += 1
            elif any(stessi(mg.giri2(r["testo"].split("\n"), q, t_debito=r["t0"] - 0.05, need_debito=r["need"])) for q in (7.8, 8.2)): uguali += 1; limite += 1; print("     M1 al limite degli 8 s:", gm, r["giri"])   # Ale, 8 novembre (scelta A): lo strumento legge la prua ogni 0,1 s
            else: print("     M1 diverso:", gm, r["giri"])
        chk("M1 tests/misura_giri_giocatore.py trova gli stessi giri del gioco, entro 0,5 s (%d prove L)" % tot, tot == 40 and uguali == tot and sum(len(r["giri"]) for r in L2 + L3) > 0, "uguali %d su %d, di cui al limite degli 8 s (entro 0,2 s) %d" % (uguali, tot, limite))
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
