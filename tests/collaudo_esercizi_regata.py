# Collaudo degli esercizi in regata delle lezioni (1.2.1, meccanismo B di docs/PROPOSTA-ESERCIZI-REGOLAMENTO-E-PARTENZE.md: soglie E1-E5 scritte prima, §4).
# Per ogni lezione con un passo «esercizio» (D5, D6, D7): si arriva al passo con «Avanti», si preme «Apri l'esercizio» e si guida la regata a passi fissi di 1/60 s.
#   E1: il pilota che fa quello che dice il testo completa l'esercizio in almeno 9 semi su 10 (semi 1-10, conferma 11-20), e a mani ferme mai (0 su 10).
#   E2: chi sbaglia apposta non passa, al più 1 su 10: D5 parte in anticipo, D6 non torna dietro la linea, D7 tocca la boa e non fa il giro.
#   E3: l'esercizio non salva niente: localStorage e registrazioni (IndexedDB) identici prima e dopo un esercizio completato.
#   E5: pannello a 1360x650 senza pixel di eccesso nell'esercizio; pagina senza #collaudo: si apre dal menu e si torna alla lezione, senza errori.
# Più: ritorno alla lezione (passo fatto, «Avanti» visibile), Ricomincia che resta nell'esercizio, Torna alla lezione con il passo da fare.
# Uso: python collaudo_esercizi_regata.py [--semi 1-10]   (browser con BROWSER=firefox)
import asyncio, os, pathlib, sys
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# piloti: «mani» nessun tasto; «pilota» la guida degli avversari principianti sulla barca del giocatore (__sv.pilota: parte, torna se è in anticipo);
# «anticipo» come il pilota finché, di bolina, passerebbe la linea circa 10 s prima del via; poi di bolina oltre la linea (in anticipo al segnale), poi il pilota (torna e riparte); «resta» come anticipo, ma dopo il via resta di bolina;
# (2 nov 2026: la prima stesura andava di bolina per tutto il minuto, finiva a 130 m di lato e tornando il pilota si incastrava nel comitato: 1 su 3 nei semi 1-3)
# «boa» punta la boa finché non la tocca, si allontana 4 s al traverso e gira con la barra tutta da una parte; «tocca» punta la boa, la tocca e poi va col pilota
CORSA = """async ([li, pil, seme]) => {
  const sv = __sv, dt = 1 / 60, n180 = a => ((a % 360) + 540) % 360 - 180, $ = id => document.getElementById(id);
  __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["l", li]);
  const si = LESSONS[li].steps.findIndex(s => s.esercizio);
  for (let k = 0; k < si; k++) $("lNext").click();
  const al = { passo: $("lStep").textContent, es: !$("lEs").hidden, avantiNascosto: $("lNext").hidden };
  $("lEs").click();
  const R = sv.R, me = R.boats[0], es = R.es, def = es && es.def;
  const inEs = { mode: sv.mode, es: !!es, obj: $("rObj").textContent, objVis: !$("rObj").hidden, lez: !$("rLez").hidden, vento: $("rWind").hidden, opz: $("bRaceOpts").hidden };
  const tieni = want => { const S = sv.S; sv.ctl.tiller = Math.max(-1, Math.min(1, n180(S.h - want) / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1); sv.ctl.sheet = sv.autoSheet(); };
  let lato = Math.sign(n180(sv.S.h - R.mark.out)) || 1;   // le mure di partenza: si resta su queste
  let fase = 0, tF = 0, via = false;
  const tMax = (def.cd || 0) + 240;
  for (let k = 0; k < 60 * (tMax + 40) && sv.mode === "race"; k++){
    const S = sv.S;
    if (pil === "pilota") sv.pilota(dt);
    else if (pil === "anticipo" || pil === "resta"){
      if (R.t < 0 && !via && toWF(S.x, S.y)[1] / 1.5 >= -R.t - 10){ via = true; lato = Math.sign(n180(S.h - R.mark.out)) || 1; }   // da qui, di bolina (sulle mure che ha) a circa 1,5 m/s verso il vento, passa la linea prima del via
      if (R.t < 0 && !via) sv.pilota(dt); else if (R.t < 0 || pil === "resta") tieni(R.mark.out + lato * 50); else sv.pilota(dt); }
    else if (pil === "boa" || pil === "tocca"){
      if (fase === 0){ tieni(Math.atan2(R.mark.x - S.x, -(R.mark.y - S.y)) * 180 / Math.PI); if (R.need >= 1){ fase = 1; tF = R.t; } }
      else if (pil === "tocca") sv.pilota(dt);
      else if (fase === 1){ tieni(R.mark.out + lato * 100); if (R.t - tF > 4) fase = 2; }
      else { sv.ctl.tiller = 1; sv.ctl.sheet = sv.autoSheet(); }
    }
    sv.run(dt, 1);
  }
  const dopo = { mode: sv.mode, passo: $("lStep").textContent, fatto: sv.stepDone, avanti: !$("lNext").hidden, feedback: !$("lFeedback").hidden, esTesto: $("lEs").textContent };
  return { al, inEs, esito: es.esito, t: Math.round(R.t), leg: me.leg, ocs0: es.ocs0 === undefined ? null : es.ocs0, need: R.need, done: R.done, dopo };
}"""
STORE = """async () => { const ls = {}; for (let i = 0; i < localStorage.length; i++){ const k = localStorage.key(i); ls[k] = localStorage.getItem(k); }
  const reg = await new Promise(res => { try { const o = indexedDB.open("scuolaVelaReg", 1); o.onerror = () => res("errore");
    o.onsuccess = () => { const db = o.result; const nomi = [...db.objectStoreNames]; if (!nomi.length) return res("vuoto");
      const tx = db.transaction(nomi, "readonly"), out = {}; let n = nomi.length; nomi.forEach(s => { const q = tx.objectStore(s).count(); q.onsuccess = () => { out[s] = q.result; if (!--n) res(out); }; }); }; } catch(e){ res("eccezione"); } });
  return JSON.stringify([ls, reg]); }"""
# Ricomincia dentro l'esercizio e Torna alla lezione; pannello a 1360x650 durante l'esercizio, prima e dopo il via
BOTTONI = """async ([li]) => { const sv = __sv, dt = 1 / 60, $ = id => document.getElementById(id), out = {};
  sv.openItem(["l", li]); const si = LESSONS[li].steps.findIndex(s => s.esercizio); for (let k = 0; k < si; k++) $("lNext").click();
  $("lEs").click(); const R1 = sv.R; sv.run(dt, 60 * 5);
  const p = document.querySelector(".panel"); if (sv.panel) sv.panel(); out.ecc1 = p.scrollHeight - p.clientHeight; out.pag1 = document.documentElement.scrollHeight - innerHeight;
  $("rRestart").click(); out.ricomincia = { nuova: sv.R !== R1, es: !!(sv.R && sv.R.es), mode: sv.mode, t: sv.R.t };
  sv.run(dt, 60 * ((sv.R.es.def.cd || 0) + 3)); if (sv.panel) sv.panel(); out.ecc2 = p.scrollHeight - p.clientHeight; out.pag2 = document.documentElement.scrollHeight - innerHeight;
  $("rLez").click(); out.torna = { mode: sv.mode, fatto: sv.stepDone, passo: $("lStep").textContent, avantiNascosto: $("lNext").hidden, es: !$("lEs").hidden };
  return out; }"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    if hash_: await ctx.add_init_script("window.requestAnimationFrame = () => 0;")   # a passi fissi: niente ciclo del browser fra un comando e l'altro
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto((ROOT / "index.html").as_uri() + hash_); await pg.wait_for_timeout(300)
    return ctx, pg, errs
LEZ = {"D5": 15, "D6": 16, "D7": 17}
BUONO = {"D5": "pilota", "D6": "anticipo", "D7": "boa"}
SBAGLIA = {"D5": "anticipo", "D6": "resta", "D7": "tocca"}
async def main():
    a = sys.argv[1:]
    x, y = (a[a.index("--semi") + 1] if "--semi" in a else "1-10").split("-"); semi = range(int(x), int(y) + 1); n = len(semi)
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b)
        tit = await pg.evaluate("() => [15, 16, 17].map(i => LESSONS[i].name + ' ' + LESSONS[i].title + ' ' + LESSONS[i].steps.findIndex(s => s.esercizio))")
        print("lezioni:", tit)
        chk("A0 le lezioni D5, D6 e D7 hanno un passo con l'esercizio", len(tit) == 3 and all(t.startswith("Lezione D") and not t.endswith("-1") for t in tit), str(tit))
        R = {}
        for nome, li in LEZ.items():
            for pil in ("buono", "mani", "sbaglia"):
                pn = BUONO[nome] if pil == "buono" else SBAGLIA[nome] if pil == "sbaglia" else "mani"
                R[nome, pil] = [await pg.evaluate(CORSA, [li, pn, s]) for s in semi]
                ok = sum(1 for r in R[nome, pil] if r["esito"] == "ok")
                print(f"  {nome} {pil:8} ({pn}): obiettivo raggiunto {ok} su {n}; esiti {[r['esito'] for r in R[nome, pil]]}; tempi {[r['t'] for r in R[nome, pil]]}", flush=True)
        for nome in LEZ:
            G, M, W = R[nome, "buono"], R[nome, "mani"], R[nome, "sbaglia"]
            chk(f"E1 {nome} guidando: obiettivo raggiunto in almeno 9 semi su 10", metro.tutti(True for r in G) and sum(1 for r in G if r["esito"] == "ok") >= 0.9 * n, f"{sum(1 for r in G if r['esito'] == 'ok')} su {n}")
            chk(f"E1 {nome} a mani ferme: mai (0 su {n}), e l'esercizio dice che l'obiettivo è mancato", metro.nessuno(r["esito"] == "ok" for r in M) and metro.tutti(r["esito"] == "no" for r in M), f"esiti {sorted({str(r['esito']) for r in M})}")
            chk(f"E2 {nome} chi sbaglia apposta ({SBAGLIA[nome]}): al più 1 su 10", metro.tutti(True for r in W) and sum(1 for r in W if r["esito"] == "ok") <= 0.1 * n, f"{sum(1 for r in W if r['esito'] == 'ok')} su {n}")
            okk = [r for r in G if r["esito"] == "ok"]
            chk(f"R1 {nome}: al passo con «Avanti», «Apri l'esercizio» visibile e «Avanti» nascosto finché non è fatto", metro.tutti(r["al"]["es"] and r["al"]["avantiNascosto"] for r in G), G[0]["al"]["passo"])
            chk(f"R2 {nome}: nell'esercizio obiettivo nel pannello, «Torna alla lezione», niente «Cambia vento» né scelta di avversari e preparazione", metro.tutti(r["inEs"]["es"] and r["inEs"]["objVis"] and r["inEs"]["obj"] and r["inEs"]["lez"] and r["inEs"]["vento"] and r["inEs"]["opz"] and r["inEs"]["mode"] == "race" for r in G), repr(G[0]["inEs"]["obj"]))
            chk(f"R3 {nome}: raggiunto l'obiettivo si torna al passo, fatto, con «Avanti» e il testo di fine passo", metro.tutti(r["dopo"]["mode"] == "lesson" and r["dopo"]["fatto"] and r["dopo"]["avanti"] and r["dopo"]["feedback"] and r["dopo"]["passo"] == r["al"]["passo"] and r["dopo"]["esTesto"] == "Rifai l'esercizio" for r in okk), f"casi {len(okk)}")
        chk("R4 D6: chi completa era davvero in anticipo al via; D5: nessuno di quelli che completano lo era", metro.tutti(r["ocs0"] is True for r in R["D6", "buono"] if r["esito"] == "ok") and metro.tutti(r["ocs0"] is False for r in R["D5", "buono"] if r["esito"] == "ok"))
        chk("R5 D7: chi completa ha toccato la boa e scontato il giro (need 1, done 1)", metro.tutti(r["need"] == 1 and r["done"] == 1 for r in R["D7", "buono"] if r["esito"] == "ok"))
        chk("A1 nessun errore di pagina (collaudo)", not errs, str(errs[:2]))
        await ctx.close()
        # ---- E3: niente salvato ----
        ctx, pg, errs = await pagina(b)
        prima = await pg.evaluate(STORE)
        es3 = [await pg.evaluate(CORSA, [li, BUONO[nome], 1]) for nome, li in LEZ.items()]
        dopo = await pg.evaluate(STORE)
        chk("E3 tre esercizi completati: localStorage e registrazioni identici prima e dopo", prima == dopo and metro.tutti(r["esito"] == "ok" for r in es3), f"esiti {[r['esito'] for r in es3]}; {prima}")
        # controprova del metro: la stessa regata dei giri, normale, guidata fino all'arrivo, salva (record, regata fatta, registrazione)
        await pg.evaluate("() => { const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(5); sv.openItem(['r', 3]); const me = sv.R.boats[0]; for (let k = 0; k < 60 * 900 && me.fin === null; k++){ sv.pilota(dt); sv.run(dt, 1); } sv.openItem(['l', 15]); sv.run(dt, 2); }")
        dopoR = await pg.evaluate(STORE)
        chk("E3b controprova: una regata normale fino all'arrivo cambia il salvataggio (il controllo E3 vede le differenze)", dopoR != dopo, dopoR[:160])
        # ---- E5 e pulsanti ----
        for nome, li in LEZ.items():
            o = await pg.evaluate(BOTTONI, [li])
            chk(f"E5 {nome}: pannello a 1360x650 senza pixel di eccesso nell'esercizio (prima e dopo il via) e pagina senza scorrimento", o["ecc1"] <= 0 and o["ecc2"] <= 0 and o["pag1"] <= 0 and o["pag2"] <= 0, f"pannello {o['ecc1']}/{o['ecc2']} px, pagina {o['pag1']}/{o['pag2']} px")
            chk(f"B1 {nome}: Ricomincia apre un esercizio nuovo, sempre esercizio", o["ricomincia"]["nuova"] and o["ricomincia"]["es"] and o["ricomincia"]["mode"] == "race", str(o["ricomincia"]))
            chk(f"B2 {nome}: Torna alla lezione torna al passo, da fare", o["torna"]["mode"] == "lesson" and not o["torna"]["fatto"] and o["torna"]["avantiNascosto"] and o["torna"]["es"], str(o["torna"]))
        chk("A2 nessun errore di pagina (salvataggi e pulsanti)", not errs, str(errs[:2]))
        await ctx.close()
        # ---- pagina come la carica un giocatore ----
        ctx, pg, errs = await pagina(b, "")
        await pg.evaluate("() => { openItem(['l', 15]); }"); await pg.wait_for_timeout(200)
        for k in range(2): await pg.click("#lNext"); await pg.wait_for_timeout(150)
        await pg.click("#lEs"); await pg.wait_for_timeout(300)
        v = await pg.evaluate("() => ({ mode, brief: !document.getElementById('briefOv').hidden, opz: document.getElementById('bRaceOpts').hidden, es: !!(R && R.es) })")
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1200)
        t1 = await pg.evaluate("() => R.t")
        await pg.click("#rLez"); await pg.wait_for_timeout(300)
        w = await pg.evaluate("() => ({ mode, passo: document.getElementById('lStep').textContent })")
        chk("H1 senza #collaudo: l'esercizio della D5 si apre dal passo, con le istruzioni e senza la scelta di avversari e preparazione, il tempo corre e si torna alla lezione",
            v["mode"] == "race" and v["brief"] and v["opz"] and v["es"] and t1 > -300 and w["mode"] == "lesson" and w["passo"] == "Passo 3 di 4", f"{v} t={t1:.1f} {w}")
        chk("H2 nessun errore di pagina (senza #collaudo)", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
