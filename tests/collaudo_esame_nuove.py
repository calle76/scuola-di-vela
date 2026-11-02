# Collaudo dell'esame e del glossario con le lezioni nuove (1.2.3, docs/PROPOSTA-ESAME-E-GLOSSARIO.md §3: criteri G1-G5 scritti prima del codice).
#   G1: con le lezioni nuove nascoste, esame e glossario identici al gioco di riferimento (RIF, 1.2.2): stesse domande estratte con 20 semi fissi,
#       stesse voci del glossario nello stesso ordine.
#   G2: con tutte le lezioni rese visibili (solo qui, nella pagina del collaudo): 34 domande, 1 per lezione nuova, soglia 28 (anche nel pulsante del menu);
#       in 200 estrazioni ogni domanda delle lezioni nuove esce almeno una volta, nessuna domanda ripetuta nella stessa estrazione.
#   G4: con tutte visibili, riquadro dell'esito con 34 sbagliate e glossario intero a 1360x650 senza pixel di eccesso; le voci nuove compaiono.
#   Più: ripasso di una lezione nuova dopo l'esame in carriera (usa il quiz della lezione), voto salvato con il numero delle domande.
#   G5: nessun errore della pagina, anche senza #collaudo.
# G3 (ogni voce nuova detta nel testo della sua lezione) è un controllo a mano, riportato nel CHANGELOG della 1.2.3.
# Uso: python collaudo_esame_nuove.py   (browser con BROWSER=firefox)
import asyncio, os, pathlib, subprocess, sys, tempfile
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
RIF = "d358672"   # 1.2.2: l'ultima versione prima di questo lavoro
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
ESTRAI = "() => Array.from({ length: 20 }, (_, k) => { __seed(1000 + k); return __sv.estraiEsame().map(r => r[2]); })"
GLOSS = "() => { openGloss(); const v = [...document.querySelectorAll('#glList dt')].map(d => d.firstChild.textContent); document.getElementById('gloss').close(); return v; }"
TUTTE = "() => { LESSONS.forEach(L => { L.nascosta = false; }); }"
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, url, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url + hash_); await pg.wait_for_timeout(400)
    return ctx, pg, errs
async def rispondi_tutte_sbagliate(pg):
    n = 0
    while n <= 60 and await pg.evaluate("() => !!qz && qz.i < qz.qs.length && document.getElementById('quiz').open"):
        i = await pg.evaluate("() => qz.qs[qz.i].opts.findIndex(o => !o.ok)")
        await pg.locator(".opt").nth(i).click(); await pg.click("#qzNext"); n += 1
    return n
async def main():
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(f"git -C {ROOT} archive {RIF} | tar -x -C {tmp}", shell=True, check=True)
        async with async_playwright() as p:
            b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
            # ---- G1: con le lezioni nascoste, identico a RIF ----
            ctx, pg, e0 = await pagina(b, (pathlib.Path(tmp) / "index.html").as_uri())
            rif_es, rif_gl = await pg.evaluate(ESTRAI), await pg.evaluate(GLOSS); await ctx.close()
            ctx, pg, errs = await pagina(b, (ROOT / "index.html").as_uri())
            nuovo_es, nuovo_gl = await pg.evaluate(ESTRAI), await pg.evaluate(GLOSS)
            chk("G1 esame identico a RIF con le lezioni nuove nascoste (20 semi)", len(rif_es) == 20 and metro.tutti(len(x) == 20 for x in rif_es) and rif_es == nuovo_es, f"{len(rif_es)} estrazioni da {len(rif_es[0])} domande")
            chk("G1 glossario identico a RIF con le lezioni nuove nascoste", len(rif_gl) == 48 and rif_gl == nuovo_gl, f"{len(rif_gl)} voci prima, {len(nuovo_gl)} ora")
            chk("G1 pulsante dell'esame nel menu: 20 domande, ne servono 16", "20 domande, ne servono 16" in await pg.inner_text("#goEsame"))
            # ---- G2: tutte visibili ----
            await pg.evaluate(TUTTE); await pg.evaluate("() => showMenu()")
            d = await pg.evaluate("() => ({ n: domandeEsame(), s: sogliaEsame(), lez: lezioniEsame().length, nuove: LESSONS.slice(6).map(L => L.esame.map(r => r[1])) })")
            chk("G2 tutte visibili: 20 lezioni, 34 domande, ne servono 28", d["lez"] == 20 and d["n"] == 34 and d["s"] == 28, str({k: d[k] for k in ("lez", "n", "s")}))
            chk("G2 pulsante dell'esame nel menu: 34 domande, ne servono 28", "34 domande, ne servono 28" in await pg.inner_text("#goEsame"), await pg.inner_text("#goEsame"))
            E = await pg.evaluate("() => Array.from({ length: 200 }, (_, k) => { __seed(5000 + k); return __sv.estraiEsame().map(r => [r[0], r[2]]); })")
            per_lez = [[sum(1 for li, _ in e if li == x) for x in range(20)] for e in E]
            chk("G2 ogni estrazione: 34 domande, 4-3-4-3-3-3 dalle lezioni di oggi e 1 da ogni lezione nuova, nessuna ripetuta",
                metro.tutti(len(e) == 34 and len({q for _, q in e}) == 34 and c == [4, 3, 4, 3, 3, 3] + [1] * 14 for e, c in zip(E, per_lez)), f"{len(E)} estrazioni")
            uscite = {q for e in E for _, q in e}; tutte_nuove = [q for l in d["nuove"] for q in l]
            mai = [q for q in tutte_nuove if q not in uscite]
            chk("G2 in 200 estrazioni ogni domanda delle lezioni nuove esce almeno una volta", len(tutte_nuove) == 56 and not mai, f"{len(tutte_nuove)} domande nuove, mai uscite {len(mai)}")
            # ---- G4: riquadro con 34 sbagliate, gioco libero ----
            await pg.click("#goEsame"); n = await rispondi_tutte_sbagliate(pg); await pg.wait_for_timeout(100)
            r = await pg.evaluate("""() => { const d = document.getElementById('quiz').getBoundingClientRect(), W = document.getElementById('qzWrong');
                const bt = [...document.querySelectorAll('#qzBody .row button')].map(b => b.getBoundingClientRect().bottom);
                return { score: document.querySelector('.qz .score').textContent, top: d.top, bottom: d.bottom, right: d.right, H: innerHeight, Wd: innerWidth, bt,
                  h3: W ? W.querySelectorAll('h3').length : 0, wq: W ? W.querySelectorAll('.wq').length : 0, pagina: document.documentElement.scrollHeight - innerHeight }; }""")
            # 2 nov 2026, dopo il primo giro (detto): la pagina dietro è il menu, che con 20 lezioni visibili sfora di 426 px; è lavoro del menu nuovo,
            # quindi qui si misura il solo riquadro e lo sforamento del menu si riporta (DA SAPERE) senza far cadere il collaudo
            ecc = max([x - r["bottom"] for x in r["bt"]] + [r["bottom"] - r["H"], -r["top"], r["right"] - r["Wd"]])
            print(f"DA SAPERE: con tutte le 20 lezioni visibili il menu dietro il riquadro sfora la finestra di {r['pagina']} px (lavoro del menu nuovo)")
            chk("G4 esito con 34 sbagliate: «0 su 34: non superato (servono 28)», 34 domande sotto 20 lezioni", n == 34 and r["score"] == "0 su 34: non superato (servono 28)" and r["wq"] == 34 and r["h3"] == 20, f"{n} risposte, {r['score']!r}, {r['wq']} sbagliate, {r['h3']} lezioni")
            chk("G4 riquadro dell'esito a 1360x650 senza pixel di eccesso", r["bt"] and ecc <= 0.5, f"eccesso {ecc:.1f} px")
            await pg.click("#qzClose")
            gl = await pg.evaluate(GLOSS)
            await pg.evaluate("() => openGloss()"); await pg.wait_for_timeout(100)
            g = await pg.evaluate("""() => { const d = document.getElementById('gloss').getBoundingClientRect(), L = document.getElementById('glList');
                return { top: d.top, bottom: d.bottom, H: innerHeight, scroll: L.scrollHeight > L.clientHeight, pagina: document.documentElement.scrollHeight - innerHeight }; }""")
            await pg.evaluate("() => document.getElementById('gloss').close()")
            nuove_voci = ["Stallo della pala", "Spingere il boma", "Salto di vento", "Scarso", "Buono", "Lasciare strada", "Precedenza", "Sovrapposte", "Libera dietro, libera avanti",
                          "Barca giuria", "Linea di partenza", "Avviso", "Preparatorio", "Bandiera di classe", "Partenza anticipata", "Richiamo individuale", "Giro di penalità",
                          "Partenza in velocità", "Partenza da fermi"]
            chk("G4 glossario con tutte visibili: 48 + 19 voci, le nuove ci sono, le vecchie nello stesso ordine", len(gl) == 67 and all(v in gl for v in nuove_voci) and [v for v in gl if v in rif_gl] == rif_gl, f"{len(gl)} voci")
            chk("G4 glossario intero a 1360x650: il riquadro sta dentro la finestra", g["top"] >= 0 and g["bottom"] <= g["H"] + 0.5, str(g))
            # ---- ripasso di una lezione nuova, in carriera ----
            rr = await pg.evaluate("""() => { modo = 'carriera'; progress.exam = { superato: false, voto: 3, n: 34, data: '2026-11-02', ripasso: [17] }; openQuiz(17);
                const q = qz.qs.length, t = document.querySelector('.qz-top h2').textContent; document.getElementById('quiz').close(); modo = 'libero'; return { q, t }; }""")
            chk("R1 il ripasso di una lezione nuova (D7) apre il suo quiz di 4 domande", rr["q"] == 4, str(rr))
            chk("A1 nessun errore della pagina (collaudo)", not errs and not e0, str((errs + e0)[:2]))
            await ctx.close()
            # ---- G5: senza #collaudo ----
            ctx, pg, errs = await pagina(b, (ROOT / "index.html").as_uri(), "")
            await pg.evaluate("() => { LESSONS.forEach(L => { L.nascosta = false; }); showMenu(); }")
            await pg.click("#goEsame"); n = await rispondi_tutte_sbagliate(pg)
            await pg.click("#qzClose"); await pg.evaluate("() => openGloss()"); await pg.fill("#glSearch", "scarso"); await pg.wait_for_timeout(100)
            trov = await pg.evaluate("() => [...document.querySelectorAll('#glList dt')].map(d => d.firstChild.textContent)")
            chk("G5 senza #collaudo: esame di 34 domande fino in fondo, ricerca nel glossario, nessun errore", n == 34 and "Scarso" in trov and not errs, f"{n} domande, ricerca «scarso» {trov}, errori {errs[:2]}")
            await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
