# Laboratorio della barca (1.0.4): criteri 3-9 di docs/archivio/PROPOSTA-LABORATORIO.md §6.
#  3. con #collaudo-lab la prova 1 e la regata 1 (principianti), semi 1-5, non cambiano localStorage; contro-prova con #collaudo: lo cambiano tutte;
#  4. il cursore hullScale da 1 a 0,5 cambia la velocità al traverso (almeno +5% dopo 30 s); riportato a 1 torna uguale entro 0,01 nodi (1.0.6: era hullK2 da 12 a 6);
#  5. con il fuoco su un cursore le frecce muovono il cursore e non la barra; contro-prova: col fuoco fuori, la freccia muove la barra;
#  6. profili sbagliati (chiave inesistente, valore fuori limite) non si caricano; contro-prova: uno giusto sì;
#  7. un profilo esportato e riletto ridà gli stessi valori (profili con 1, 3 e 15 valori);
#  8. con il laboratorio la testata del registratore ha profilo= e i valori cambiati; senza, no;
#  9. pagina aperta come un giocatore (senza #collaudo), senza niente e con #lab: nessun errore, la finestra c'è solo con #lab, il tasto L la nasconde.
# Uso: python collaudo_laboratorio.py        Esce con 1 se un criterio fallisce, 2 se ha misurato meno corse del previsto.
import asyncio, json, sys
from playwright.async_api import async_playwright
from collaudo_impronta import ROOT, SEME, COMUNE, PROVA, REGATA

URL = (ROOT / "index.html").as_uri()
DUMP = "JSON.stringify(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)]))"
falliti, righe = [], []
def esito(nome, ok, det=""):
    righe.append(f"{'OK ' if ok else 'NO '} {nome}{': ' + det if det else ''}")
    if not ok: falliti.append(nome)

async def main():
    errs = []
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        async def pagina(hash, seme=True):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650})
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(f"{hash}: {e}"))
            if seme: await pg.add_init_script(SEME.split("window.requestAnimationFrame")[0])   # solo Math.random a seme fisso
            await pg.goto(URL + hash); await pg.wait_for_timeout(300)
            if hash.startswith("#collaudo"): await pg.evaluate(COMUNE)
            return pg

        # 3. niente salvataggi
        corse = {"#collaudo-lab": [0, 0], "#collaudo": [0, 0]}   # [finite, con localStorage cambiato]
        for hash in corse:
            for seme in range(1, 6):
                for tipo in ("prova", "regata"):
                    pg = await pagina(hash); prima = await pg.evaluate(DUMP)
                    if tipo == "prova": r = await pg.evaluate(PROVA, [0, seme]); fin = r["S"][-1]
                    else: r = await pg.evaluate(REGATA, [0, "principianti", seme]); fin = r["barche"][0][1] is not None
                    dopo = await pg.evaluate(DUMP); await pg.context.close()
                    corse[hash][0] += bool(fin); corse[hash][1] += fin and prima != dopo
        lab, coll = corse["#collaudo-lab"], corse["#collaudo"]
        if lab[0] < 10 or coll[0] < 10:
            print(f"corse finite: laboratorio {lab[0]}/10, contro-prova {coll[0]}/10"); print("ESITO: NON VALIDO (ha misurato meno corse del previsto)"); sys.exit(2)
        esito("3. con #lab niente salvataggi", lab[1] == 0, f"{lab[0]} corse finite, localStorage cambiato in {lab[1]}")
        esito("3. contro-prova senza #lab", coll[1] == coll[0], f"{coll[0]} corse finite, localStorage cambiato in {coll[1]}")

        pg = await pagina("#collaudo-lab")
        # 4. un cursore cambia la barca: navigazione libera, prua tenuta al traverso, scotta automatica, stesso seme
        vel = """(k2) => { const r = document.getElementById("labR_hullScale"); r.value = k2; r.dispatchEvent(new Event("input"));
          const sv = __sv; sv.fast(0); sv.openItem("free"); __seed(5); const S = sv.S; S.u = 1; S.vl = 0;
          for (let n = 0; n < 60 * 30; n++){ S.h = (sv.twd + 90) % 360; S.r = 0; sv.ctl.tiller = 0; sv.ctl.sheet = sv.autoSheet(); sv.run(1 / 60, 1); }
          return [BOAT.hullScale, S.u * 1.943844]; }"""
        a, bb, c = [await pg.evaluate(vel, k) for k in (1, 0.5, 1)]
        esito("4. hullScale 0,5 cambia la velocità", bb[0] == 0.5 and bb[1] >= a[1] * 1.05, f"con 1: {a[1]:.2f} nodi, con 0,5: {bb[1]:.2f} (+{(bb[1] / a[1] - 1) * 100:.0f}%)")
        esito("4. hullScale riportato a 1", c[0] == 1 and abs(c[1] - a[1]) <= 0.01, f"{c[1]:.3f} contro {a[1]:.3f} nodi")

        # 5. frecce: in navigazione libera, nel ciclo vero del browser
        await pg.evaluate("__sv.fast(1); __sv.ctl.tiller = 0; document.getElementById('labR_turnLen').focus()")
        v0 = await pg.evaluate("+document.getElementById('labR_turnLen').value")
        for _ in range(10): await pg.keyboard.press("ArrowLeft")
        await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(400); await pg.keyboard.up("ArrowLeft")
        t1, v1 = await pg.evaluate("[__sv.ctl.tiller, +document.getElementById('labR_turnLen').value]")
        esito("5. frecce sul cursore", t1 == 0 and v1 < v0, f"barra {t1}, cursore da {v0} a {v1}")
        await pg.evaluate("document.activeElement.blur(); document.getElementById('c').focus()")
        await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(400); await pg.keyboard.up("ArrowLeft")
        t2 = await pg.evaluate("__sv.ctl.tiller")
        esito("5. contro-prova: freccia fuori dal laboratorio", t2 != 0, f"barra {t2:.2f}")
        await pg.evaluate("labCarica(LAB_OGGI)")

        # 6. profili sbagliati
        sb = await pg.evaluate("""() => { const f = (k, v) => ({ id: "prova", nome: "prova", versione: "x", valori: { [k]: { v, fonte: "collaudo", stato: "ipotesi" } } });
          const prima = JSON.stringify(BOAT);
          const e1 = labCarica(f("nonEsiste", 1)), e2 = labCarica(f("hullScale", 99)), e3 = labCarica({ id: "somma", nome: "somma", versione: "x", valori: { luffA0: { v: 33, fonte: "collaudo", stato: "ipotesi" }, luffW: { v: 8, fonte: "collaudo", stato: "ipotesi" } } }), invariata = JSON.stringify(BOAT) === prima;
          const e4 = labCarica(f("hullScale", 0.8)), giusto = BOAT.hullScale === 0.8; labCarica(LAB_OGGI);
          return [e1, e2, e3, invariata, e4, giusto]; }""")
        esito("6. profili sbagliati non si caricano", all(sb[:3]) and sb[3], f"{sum(map(bool, sb[:3]))} su 3 rifiutati: «{sb[0]}», «{sb[1]}», «{sb[2]}»")
        esito("6. contro-prova: un profilo giusto si carica", sb[4] == "" and sb[5])

        # 7. esportazione e rilettura
        es = await pg.evaluate("""() => { const P = (id, val) => ({ id, nome: id, versione: VERSIONE, valori: Object.fromEntries(Object.entries(val).map(([k, v]) => [k, { v, fonte: "collaudo", stato: "ipotesi" }])) });
          const tutti = Object.fromEntries(Object.entries(LAB_LIM).map(([k, L]) => [k, L[0]]));
          const out = [];
          for (const p of [P("uno", { ironsYaw: 3 }), P("tre", { hullScale: 0.8, turnLen: 1.2, maxRudder: 25 }), P("quindici", tutti)]){
            const e = labCarica(p), atteso = JSON.stringify(BOAT), txt = labEsporta(); labCarica(LAB_OGGI);
            const q = JSON.parse(txt.replace(/,\\s*$/, "")), e2 = labCarica(q);
            out.push([p.id, Object.keys(q.valori).length, e, e2, JSON.stringify(BOAT) === atteso]); labCarica(LAB_OGGI); }
          return out; }""")
        esito("7. esportato e riletto", all(x[2] == "" and x[3] == "" and x[4] for x in es), "; ".join(f"{x[0]}: {x[1]} valori {'uguali' if x[4] else 'DIVERSI'}" for x in es))
        mano = await pg.evaluate("""() => { const r = document.getElementById("labR_hullScale"); r.value = 0.7; r.dispatchEvent(new Event("input"));
          const q = JSON.parse(labEsporta().replace(/,\\s*$/, "")); labCarica(LAB_OGGI); return q.valori.hullScale; }""")
        esito("7. valore toccato a mano esce «non verificato»", mano == {"v": 0.7, "fonte": "prova a mano", "stato": "non verificato"}, json.dumps(mano, ensure_ascii=False))

        # 8. registratore
        s1 = await pg.evaluate("""() => { const a = sesSet(); const r = document.getElementById("labR_hullScale"); r.value = 0.7; r.dispatchEvent(new Event("input"));
          const b = sesSet(); labCarica(LAB_OGGI); return [a, b]; }""")
        await pg.context.close()
        pg = await pagina("#collaudo"); s0 = await pg.evaluate("sesSet()"); await pg.context.close()
        esito("8. registratore con il laboratorio", s1[0].endswith(" profilo=oggi") and s1[1].endswith(" profilo=oggi+modificato hullScale=0.7"), s1[1][-40:])
        esito("8. registratore senza laboratorio", "profilo=" not in s0 and s0.endswith("s"))

        # 9. pagina vera, come la apre un giocatore
        vere = {}
        for hash in ("", "#lab"):
            n = len(errs); pg = await pagina(hash, seme=False)
            c = await pg.evaluate("[typeof window.__sv, !!document.getElementById('lab'), document.getElementById('labBanner')?.textContent || '']")
            if hash:
                await pg.keyboard.press("l"); c.append(await pg.evaluate("document.getElementById('lab').hidden"))
            vere[hash] = (c, len(errs) - n); await pg.context.close()
        esito("9. pagina senza niente", vere[""][0][:2] == ["undefined", False] and vere[""][1] == 0, f"errori {vere[''][1]}")
        esito("9. pagina con #lab", vere["#lab"][0][0] == "undefined" and vere["#lab"][0][1] and vere["#lab"][0][3] and vere["#lab"][1] == 0,
              f"«{vere['#lab'][0][2]}», tasto L nasconde: {vere['#lab'][0][3]}, errori {vere['#lab'][1]}")
        await b.close()
    for r in righe: print(r)
    print(f"errori della pagina: {errs[:5]}")
    print("ESITO: OK" if not falliti and not errs else f"ESITO: FALLITO ({len(falliti)} criteri, {len(errs)} errori della pagina)")
    sys.exit(0 if not falliti and not errs else 1)

asyncio.run(main())
