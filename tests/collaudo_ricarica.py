# Ricarica della pagina (1.0.56): Firefox rimette caselle e menu come li aveva l'utente prima di F5, mentre il gioco riparte con le sue impostazioni
# (js/gioco.js, `opt`): lo schermo mostrava un'impostazione diversa da quella in uso. Ora ogni <input> e <select> ha autocomplete="off".
# Il collaudo apre la pagina in una scheda nuova e legge lo stato di ogni casella e menu; in un'altra li cambia tutti, ricarica con F5 (reload) e confronta: devono essere uguali.
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

async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); pg = await (await b.new_context()).new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        fresca = await (await b.new_context()).new_page(); await fresca.goto(BASE); await fresca.wait_for_timeout(500); att = await fresca.evaluate(DOPO)
        await pg.goto(BASE); await pg.wait_for_timeout(500)
        ids = await pg.evaluate(PRIMA); await pg.reload(); await pg.wait_for_timeout(500)
        r = await pg.evaluate(DOPO); male = [a[0] for a, c in zip(att, r) if a != c]
        ok = bool(ids) and len(att) == len(r) and not male and not errs
        print(f"controlli cambiati e ricaricati: {len(ids)}; uguali a quelli di una pagina nuova: {len(r) - len(male)}; diversi: {male}; errori della pagina {errs[:2]}")
        print("ESITO:", "OK" if ok else "FALLITO"); await b.close(); sys.exit(0 if ok else 1)
asyncio.run(main())
