# Versione del gioco a schermo (0.18.3). Un'unica fonte, la costante VERSIONE in index.html: questo
# collaudo non la legge mai dal motore (nessun aggancio __sv, pagina senza #collaudo, caricata come la
# carica un giocatore), ma la ritrova per conto suo con un'espressione regolare sul file, cosi' il
# confronto non dipende da quello che il gioco dice di se' stesso. Verifica tre cose, e dichiara quante
# ne ha davvero confrontate (fallisce se una delle tre non e' stata eseguita):
#  1) il testo nel menu, a fianco del titolo, e' "V. " + VERSIONE
#  2) il testo disegnato sul mare (catturato intercettando ctx.fillText) contiene "V. " + VERSIONE
#  3) VERSIONE e' uguale alla versione piu' alta fra i titoli di CHANGELOG.md (righe "## 0.x[.y] — ...",
#     escludendo "## Sperimentale" e le altre intestazioni senza un numero di versione all'inizio)
# Uso: python collaudo_versione.py
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()

sbagliati = []
confronti = 0

def esito(nome, ok, det=""):
    global confronti
    confronti += 1
    print(f"  {'OK ' if ok else 'NO '} {nome}" + (f": {det}" if det else ""), flush=True)
    if not ok: sbagliati.append(nome)

def versione_in_index():
    m = re.search(r'const VERSIONE = "([^"]+)"', (ROOT / "index.html").read_text(encoding="utf-8"))
    if not m: raise RuntimeError("costante VERSIONE non trovata in index.html")
    return m.group(1)

def versione_massima_changelog():
    righe = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
    versioni = []
    for r in righe:
        m = re.match(r'^## (\d+(?:\.\d+){0,2})(?:\s|$)', r)
        if m: versioni.append(m.group(1))
    if not versioni: raise RuntimeError("nessun titolo di versione trovato in CHANGELOG.md")
    massima = max(versioni, key=lambda v: tuple(int(x) for x in v.split(".")))
    return massima, versioni

# Intercetta ogni ctx.fillText disegnato dal motore (menu e mare), prima che qualsiasi script della
# pagina parta: cosi' la lettura non dipende da #collaudo, ne' da un aggancio che il gioco espone apposta.
CATTURA_FILLTEXT = """
    window.__testiCanvas = new Set();
    const f = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function(testo, ...resto){
        window.__testiCanvas.add(testo); return f.call(this, testo, ...resto);
    };
"""

async def main():
    attesa = versione_in_index()
    massima, tutte = versione_massima_changelog()
    print(f"VERSIONE in index.html: {attesa}")
    print(f"versione piu' alta in CHANGELOG.md: {massima} (fra {len(tutte)} titoli di versione)")
    esito("VERSIONE coincide con la versione piu' alta di CHANGELOG.md", attesa == massima, f"{attesa} / {massima}")

    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(CATTURA_FILLTEXT)
        await pg.goto(BASE); await pg.wait_for_timeout(400)

        testo_menu = await pg.evaluate("document.querySelector('.menu-head .ver')?.textContent ?? null")
        print(f"testo nel menu: {testo_menu!r}")
        esito("testo del menu uguale a «V. » + VERSIONE", testo_menu == "V. " + attesa, f"{testo_menu!r}")

        await pg.click("#goFree"); await pg.wait_for_timeout(1200)
        testi_mare = await pg.evaluate("[...window.__testiCanvas]")
        presente = ("V. " + attesa) in testi_mare
        esito("testo sul mare uguale a «V. » + VERSIONE", presente, f"trovato: {presente}; testi catturati: {len(testi_mare)}")

        print("errori pagina:", errs[:5])
        await b.close()

    print("confronti eseguiti:", confronti)
    print("casi sbagliati:", sbagliati or "nessuno")
    sys.exit(1 if (sbagliati or errs or confronti < 3) else 0)
asyncio.run(main())
