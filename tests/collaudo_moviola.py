# Collaudo della moviola. Dalla 1.0.76 rivede tutta la regata, partenza compresa, con i segni
# (docs/PROPOSTA-MOVIOLA-INTERA.md, criteri V1-V10 scritti prima di misurare). Fino alla 1.0.75 erano spezzoni di 18 s (1.0.58).
# Uso: .venv-collaudi/bin/python tests/collaudo_moviola.py [semi=12] [cartella di una copia di riferimento della 1.0.75, per V2 e V7]
# Esce con 1 se un criterio non è rispettato.
import asyncio, pathlib, sys, os
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# Regata del torneo col pilota, dal conto alla rovescia all'arrivo. Premi O a 40 s e a 90 s.
# La verità: posizioni e prue di tutte le barche, lette dal vivo ogni secondo, anche prima del via.
RUN = """async ([seme, conMov]) => {
  const sv = __sv, dt = 1 / 60; sv.simTime = 0; __seed(seme);
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], truth = [], t0 = performance.now(), tPrimo = R.t; let n = 0;
  while (R.t < 1500 && me.fin === null && !me.dnf){
    sv.pilota(dt); sv.run(dt, 1); n++;
    if (n % 60 === 0) truth.push([R.t, R.boats.map(b => [b.S.x, b.S.y, b.S.h])]);
    if (conMov && R.phase === "race" && (Math.abs(R.t - 40) < dt / 2 || Math.abs(R.t - 90) < dt / 2)) window.dispatchEvent(new KeyboardEvent("keydown", { key: "o" }));
  }
  const ms = performance.now() - t0;
  const out = { fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), ms, passi: n };
  if (!conMov){ document.getElementById("rTor").click(); return out; }
  racePanel();
  out.bottone = !document.getElementById("finRev").hidden;
  out.tPrimo = tPrimo; out.tArrivo = me.fin === null ? null : me.fin - me.pen; out.tFine = R.t;   // tFine: l'istante in cui la regata del giocatore è finita, anche a finestra chiusa
  out.f0 = riv.all[0].t; out.f1 = riv.all[riv.all.length - 1].t; out.copie = riv.all.length;
  // V4: i segni attesi sono le O premute e ogni contatto o boa toccata dell'elenco delle penalità (anche prima del via, anche fra avversari)
  const attesiAuto = R.penList.filter(x => / contatto con | hai toccato /.test(x)).length;
  out.segni = riv.segni.length; out.segniAuto = riv.segni.filter(g => g.auto).length; out.segniMan = riv.segni.filter(g => !g.auto).length; out.attesiAuto = attesiAuto;
  out.segniPrimaDelVia = riv.segni.filter(g => g.t < 0).length;
  out.orariO = riv.segni.filter(g => !g.auto).map(g => g.t);
  const prima = JSON.stringify(R.boats.map(b => b.S)), wprima = R.boats.map(b => b.wake.length).join();
  rivApri();
  out.aperta = riv.on; out.finOvNascosta = document.getElementById("finOv").hidden; out.barra = !document.getElementById("movBar").hidden;
  out.tacche = document.querySelectorAll("#movSegni i").length;
  // V1: fedeltà su tutta la regata, partenza compresa
  let errPos = 0, errH = 0, nc = 0, ncPre = 0;
  for (const [t, b] of truth){ if (t < riv.all[0].t || t > riv.all[riv.all.length - 1].t) continue; riv.pos = t - riv.all[0].t; rivApplica(); nc++; if (t < 0) ncPre++;
    R.boats.forEach((bt, j) => { errPos = Math.max(errPos, Math.hypot(bt.S.x - b[j][0], bt.S.y - b[j][1])); if (!bt.S.capsized) errH = Math.max(errH, Math.abs(norm180(bt.S.h - b[j][2]))); }); }   // 7 nov 2026: da scuffiata la prua alla raddrizzata cambia di colpo (seme 10: 50°); la posizione si confronta sempre
  out.errPos = errPos; out.errH = errH; out.confronti = nc; out.confrontiPre = ncPre;
  // per V5: si riparte da un punto noto, il Python preme i tasti veri e poi chiama FINE
  riv.playing = false; riv.pos = 30; riv.speed = 1; rivMostra(); document.getElementById("movPlay").focus();   // il fuoco come all'apertura
  window.__mov = { prima, wprima };
  return out;
}"""
STATO = "() => ({ pos: riv.pos, speed: riv.speed, on: riv.on, playing: riv.playing, t: riv.all[0].t + riv.pos, segni: riv.segni.map(g => g.t), dur: rivDur() })"
FINE = """() => { const w = window.__mov; const o = { chiusa: !riv.on, stessoStato: JSON.stringify(R.boats.map(b => b.S)) === w.prima, stesseScie: R.boats.map(b => b.wake.length).join() === w.wprima,
  finOvDiNuovo: !document.getElementById("finOv").hidden, barraNascosta: document.getElementById("movBar").hidden }; document.getElementById("rTor").click(); return o; }"""
# V8: tetto delle copie (60 minuti a 10 al secondo), provato riempiendo la memoria della moviola a regata aperta, prima del via
TETTO = """() => { __sv.torApri(); document.getElementById("torGo").click(); rivReset(); for (let k = 0; k < 37000; k++) rivCapture(-300 + k * 0.1, 0.1);
  const o = { copie: riv.all.length, tagliata: riv.tagliata }; rivReset(); return o; }"""
# V9: la barra della moviola a 1360x650: niente fuori dallo schermo né dalla barra
BARRA = """() => { const b = document.getElementById("movBar").getBoundingClientRect(); let ecc = Math.max(0, b.bottom - innerHeight, b.right - innerWidth, -b.left, -b.top);
  for (const e of document.querySelectorAll("#movBar *")){ if (e.closest("#movSegni")) continue; const r = e.getBoundingClientRect(); if (!r.width) continue; ecc = Math.max(ecc, r.right - b.right, b.left - r.left, r.bottom - b.bottom); }
  const k = document.querySelector("#movBar .movKeys"); return { ecc: Math.round(ecc), keysScroll: k.scrollWidth - k.clientWidth }; }"""


async def gira(base, semi, conMov):
    ris = []
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for t in semi:
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(pathlib.Path(base, "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(200)
            await pg.evaluate("([s, l]) => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; const e = document.getElementById('aiLevel'); e.value = l; e.dispatchEvent(new Event('change')); __sv.torApri(); }", [t, "principianti"])
            r = await pg.evaluate(RUN, [5000 + t, conMov]); r["seme"] = t
            if conMov:
                r["barraMis"] = await pg.evaluate(BARRA)
                tasti = []
                async def premi(k):
                    await pg.keyboard.press(k); await pg.wait_for_timeout(30); tasti.append((k, await pg.evaluate(STATO)))
                s0 = await pg.evaluate(STATO)
                for k in ["ArrowRight", "ArrowLeft", "ArrowLeft", "ArrowDown", "ArrowDown", "ArrowUp", "4", "5", "1", "2", "3", "r", " "]:
                    await premi(k)
                r["s0"] = s0; r["tasti"] = tasti
                await pg.keyboard.press("Escape"); await pg.wait_for_timeout(30)
                r.update(await pg.evaluate(FINE))
            r["errori_pagina"] = errs; ris.append(r)
            await ctx.close()
        if conMov:
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(pathlib.Path(base, "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(200)
            ris.append({"tetto": await pg.evaluate(TETTO), "errori_pagina": errs}); await ctx.close()
            # V10: pagina caricata come la carica un giocatore, senza #collaudo: regata dal menu, conto alla rovescia vero per 3 s, poi la moviola
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(pathlib.Path(base, "index.html").as_uri()); await pg.wait_for_timeout(300)
            apri = await pg.evaluate("""() => { const b = [...document.querySelectorAll("#menu button.item")].find(x => /Regata a bastone/.test(x.textContent)); if (!b) return false; b.click(); const go = document.getElementById("bGo"); if (go && !document.getElementById("briefOv").hidden) go.click(); return true; }""")
            await pg.wait_for_timeout(3000)
            v10 = await pg.evaluate("() => { const n = riv.all.length; rivApri(); return { menu: true, copie: n, aperta: riv.on, titolo: document.getElementById('movTit').textContent, barra: !document.getElementById('movBar').hidden }; }") if apri else {"menu": False}
            ris.append({"v10": v10, "errori_pagina": errs}); await ctx.close()
        await b.close()
    return ris


async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    semi = range(1, n + 1)
    tutto = await gira(ROOT, semi, True)
    nuovo = [r for r in tutto if "fin" in r]; tetto = [r for r in tutto if "tetto" in r][0]["tetto"]; v10 = [r for r in tutto if "v10" in r][0]["v10"]
    bad = []
    def chk(nome, ok, extra=""):
        print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
        if not ok: bad.append(nome)
    chk("A0 nessun errore di pagina", metro.tutti((not r["errori_pagina"] for r in tutto), minimo=n + 2), str([r["errori_pagina"] for r in tutto if r["errori_pagina"]][:2]))
    chk("A1 pulsante Rivedi a fine regata; la moviola si apre, schermata finale nascosta, barra visibile (%d regate)" % n,
        metro.tutti((r["bottone"] and r["aperta"] and r["finOvNascosta"] and r["barra"] for r in nuovo), minimo=n))
    nc = sum(r["confronti"] for r in nuovo); ncp = sum(r["confrontiPre"] for r in nuovo)
    chk("V1 fedeltà su tutta la regata: posizione entro 0,5 m e prua entro 5°, almeno 500 confronti (confronti %d, prima del via %d)" % (nc, ncp),
        nc >= 500 and ncp > 0 and max(r["errPos"] for r in nuovo) <= 0.5 and max(r["errH"] for r in nuovo) <= 5,
        "massimo %.3f m, %.2f°" % (max(r["errPos"] for r in nuovo), max(r["errH"] for r in nuovo)))
    # 10 nov 2026: V3 non dipende più dal pilota. Se il giocatore non arriva (finestra d'arrivo chiusa: Firefox seme 8 dalla 1.2.24, Chromium seme 5 dalla 1.2.15
    # alla 1.2.23) la moviola deve coprire fino alla chiusura; perché il caso «arrivo» resti misurato, almeno metà delle regate devono essere arrivate
    arrivate = sum(1 for r in nuovo if r["tArrivo"] is not None); fineDi = lambda r: r["tArrivo"] if r["tArrivo"] is not None else r["tFine"]
    chk("V3 copertura: dalle prime bandiere (entro 0,2 s) alla fine della regata del giocatore, arrivo o finestra chiusa (entro 0,2 s) (%d regate arrivate su %d, almeno metà)" % (arrivate, len(nuovo)),
        2 * arrivate >= n and metro.tutti((abs(r["f0"] - r["tPrimo"]) <= 0.2 and abs(r["f1"] - fineDi(r)) <= 0.2 for r in nuovo), minimo=n),
        "scarti massimi: inizio %.2f s, fine %.2f s; copie per regata %d-%d" % (max(abs(r["f0"] - r["tPrimo"]) for r in nuovo), max(abs(r["f1"] - fineDi(r)) for r in nuovo), min(r["copie"] for r in nuovo), max(r["copie"] for r in nuovo)))
    tot = sum(r["segni"] for r in nuovo)
    chk("V4 segni: le 2 O di ogni regata a 40 e 90 s (entro 0,2 s) e un segno per ogni contatto o boa toccata dell'elenco, con le tacche sul cursore; almeno 20 segni (segni %d, automatici %d, prima del via %d)" % (tot, sum(r["segniAuto"] for r in nuovo), sum(r["segniPrimaDelVia"] for r in nuovo)),
        tot >= 20 and metro.tutti((r["segniMan"] == 2 and all(abs(a - b) <= 0.2 for a, b in zip(r["orariO"], [40, 90])) and r["segniAuto"] == r["attesiAuto"] and r["tacche"] == r["segni"] for r in nuovo), minimo=n))
    def tasti_ok(r):
        s, T = r["s0"], dict()
        seq = r["tasti"]; p = [x[1] for x in seq]; e = []
        e.append(abs(p[0]["pos"] - (s["pos"] + 5)) < 1e-6)            # →
        e.append(abs(p[1]["pos"] - s["pos"]) < 1e-6)                  # ←
        e.append(abs(p[2]["pos"] - max(0, s["pos"] - 5)) < 1e-6)      # ← ancora
        dopo = [g for g in s["segni"] if g - 10 > p[2]["t"] + 0.05]
        e.append(bool(dopo) and abs(p[3]["t"] - max(dopo[0] - 10, s["t"] - s["pos"])) < 0.15)   # ↓ al primo segno dopo, 10 s prima
        dopo2 = [g for g in s["segni"] if g - 10 > p[3]["t"] + 0.05]
        e.append((not dopo2 and abs(p[4]["t"] - p[3]["t"]) < 0.15) or (bool(dopo2) and abs(p[4]["t"] - (dopo2[0] - 10)) < 0.15))  # ↓ di nuovo
        e.append(p[5]["t"] < p[4]["t"] - 0.4 or not dopo2)          # ↑ torna indietro di un segno
        e.append(p[6]["speed"] == 4 and p[7]["speed"] == 8 and p[8]["speed"] == 1 and p[9]["speed"] == 0.5 and p[10]["speed"] == 0.25)
        e.append(abs(p[11]["pos"]) < 0.1)                            # R: inizio (il tempo può scorrere di qualche passo)
        e.append(p[12]["playing"] != p[11]["playing"])               # spazio: pausa / riprendi
        return all(e), e
    tk = [tasti_ok(r) for r in nuovo]
    chk("V5 tasti veri: → e ← di 5 s, ↓ e ↑ ai segni (10 s prima), 4 5 1 2 3 velocità 4× 8× 1× ½× ¼×, R all'inizio, spazio pausa, Esc chiude (%d regate)" % n,
        metro.tutti((ok for ok, _ in tk), minimo=n) and metro.tutti((r["chiusa"] for r in nuovo), minimo=n), str([e for ok, e in tk if not ok][:1]))
    chk("V6 uscita pulita: stato e scie identici, schermata finale di nuovo visibile, barra nascosta", metro.tutti((r["stessoStato"] and r["stesseScie"] and r["finOvDiNuovo"] and r["barraNascosta"] for r in nuovo), minimo=n))
    chk("V8 al più 36.000 copie (60 minuti): riempita con 37.000 si ferma a %d e lo dice" % tetto["copie"], tetto["copie"] == 36000 and tetto["tagliata"])
    bm = [r["barraMis"] for r in nuovo]
    chk("V9 barra della moviola a 1360x650: niente fuori dallo schermo o dalla barra, riga dei tasti senza scorrimento", metro.tutti((m["ecc"] <= 0 and m["keysScroll"] <= 0 for m in bm), minimo=n), "eccesso massimo %d px" % max(m["ecc"] for m in bm))
    chk("V10 pagina senza #collaudo: la regata parte dal menu, la moviola copia durante il conto alla rovescia e si apre su tutta la regata", v10.get("menu") and v10.get("copie", 0) >= 20 and v10.get("aperta") and v10.get("barra") and v10.get("titolo", "").startswith("Tutta la regata"), str(v10))
    if rif:
        vecchio = await gira(rif, semi, False)
        uguali = metro.tutti((a["fin"] == b["fin"] and a["pen"] == b["pen"] and a["pp"] == b["pp"] and a["fine"] == b["fine"] and a["passi"] == b["passi"] for a, b in zip(nuovo, vecchio)), minimo=n)
        chk("V2 gioco identico al bit con la moviola nuova e con la 1.0.75 (arrivi, penalità, posizioni finali, passi) su %d regate" % n, uguali)
        tn, tv = sum(r["ms"] for r in nuovo), sum(r["ms"] for r in vecchio)
        chk("V7 costo: tempo di calcolo della regata al più +3%% (con %.1f s, 1.0.75 %.1f s: %+.1f%%)" % (tn / 1000, tv / 1000, 100 * (tn - tv) / tv), tn <= tv * 1.03)
    else:
        print("     V2 e V7 non misurati: serve la cartella di una copia della 1.0.75")
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
