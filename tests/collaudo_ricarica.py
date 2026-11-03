# Ricarica della pagina (1.0.56): Firefox rimette caselle e menu come li aveva l'utente prima di F5, mentre il gioco riparte con le sue impostazioni
# (js/gioco.js, `opt`): lo schermo mostrava un'impostazione diversa da quella in uso. Ora ogni <input> e <select> ha autocomplete="off".
# Il collaudo apre la pagina in una scheda nuova e legge lo stato di ogni casella e menu; in un'altra li cambia tutti, ricarica con F5 (reload) e confronta: devono essere uguali.
# 1.2.6: «Suoni» (#suoniSel, 1.2.5) è l'unica scelta che il gioco ricorda apposta nel browser: dopo F5 deve mostrare il valore scelto prima
# e quello in uso (suoniLiv), non quello di una pagina nuova. Gli altri controlli si confrontano con la pagina nuova come prima.
# Uso: BROWSER=firefox python collaudo_ricarica.py [percorso di un index.html]   (senza percorso prova quello del progetto)
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
PRIMA = """() => [...document.querySelectorAll('input, select')].filter(e => e.id && e.type !== 'search').map(e => {
  if (e.type === 'checkbox'){ e.checked = !e.checked; e.dispatchEvent(new Event('change')); }
  else if (e.tagName === 'SELECT'){ e.selectedIndex = (e.selectedIndex + 1) % e.options.length; e.dispatchEvent(new Event('change')); }
  else if (e.type === 'range'){ e.value = e.min ? +e.min : 0; e.dispatchEvent(new Event('input')); }
  return e.id; })"""
DOPO = """() => [...document.querySelectorAll('input, select')].filter(e => e.id && e.type !== 'search').map(e => [e.id, e.type === 'checkbox' ? e.checked : e.value])"""   # lo stato di ogni controllo

RICORDATI = {"suoniSel": "suoniLiv"}   # id del controllo -> variabile del gioco con il valore in uso

async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); pg = await (await b.new_context()).new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        fresca = await (await b.new_context()).new_page(); await fresca.goto(BASE); await fresca.wait_for_timeout(500); att = await fresca.evaluate(DOPO)
        await pg.goto(BASE); await pg.wait_for_timeout(500)
        ids = await pg.evaluate(PRIMA); scelti = dict(await pg.evaluate(DOPO)); await pg.reload(); await pg.wait_for_timeout(500)
        r = await pg.evaluate(DOPO); male = [a[0] for a, c in zip(att, r) if a != c and a[0] not in RICORDATI]
        ric = []   # [id, mostrato dopo F5, scelto prima di F5, in uso nel gioco, quello di una pagina nuova]
        for i, var in RICORDATI.items():
            ric.append([i, dict(r).get(i), scelti.get(i), await pg.evaluate(var), dict(att).get(i)])
        ric_male = [x[0] for x in ric if not (x[1] == x[2] == x[3] and x[1] != x[4])]   # x[1] != x[4]: il controllo deve aver cambiato davvero qualcosa
        ok = bool(ids) and len(att) == len(r) and not male and len(ric) == len(RICORDATI) and not ric_male and not errs
        print(f"controlli cambiati e ricaricati: {len(ids)}; uguali a quelli di una pagina nuova: {len(r) - len(male) - len(ric)}; diversi: {male}; errori della pagina {errs[:2]}")
        print(f"ricordati dal gioco (mostrato, scelto prima, in uso, pagina nuova): {ric}; sbagliati: {ric_male}")
        print("ESITO:", "OK" if ok else "FALLITO"); await b.close(); sys.exit(0 if ok else 1)
asyncio.run(main())
