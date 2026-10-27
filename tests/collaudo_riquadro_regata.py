# Il riquadro delle istruzioni della regata deve stare nella finestra (1360x650) con QUALUNQUE combinazione di caratteri degli avversari.
# Il testo descrive il carattere di ciascun avversario (prudente, normale, aggressiva), assegnato a caso a ogni partenza: collaudo_pannello.py
# lo misura una volta sola con un testo a caso, e il difetto della 1.0.18 (frase sul richiamo, +15 px con tre «prudente») e comparso solo ogni tanto.
# Qui: pagina vera, senza #collaudo, Math.random a seme fisso, i semi 1-60. Criteri: nessun seme con eccesso (scrollHeight - clientHeight > 0);
# il metro deve aver visto davvero il caso peggiore (almeno un seme con tre «prudente»), altrimenti l'esito e NON VALIDO.
# Uso: python collaudo_riquadro_regata.py [numero di semi, 60 se manca]
import asyncio, pathlib, sys, collections
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
W, H = 1360, 650
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
SEME = "(() => { let s = %d; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; })()"
LEGGI = "(() => { const e = document.getElementById('briefOv'); const t = e.innerText; return [e.scrollHeight - e.clientHeight, t.length, (t.match(/prudente|aggressiva|normale/g) || []).join('+')]; })()"

async def main():
    res, errs = [], []
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        for seme in range(1, N + 1):
            pg = await b.new_page(viewport={"width": W, "height": H}); pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(SEME % seme)
            await pg.goto(URL); await pg.wait_for_timeout(400)
            await pg.click("[data-r='0']"); await pg.wait_for_timeout(1200)
            res.append((seme, *await pg.evaluate(LEGGI))); await pg.close()
        await b.close()
    eccessi = collections.Counter(x[1] for x in res)
    tre_prudenti = sum(1 for x in res if x[3].count("prudente") == 3)
    peggio = max(res, key=lambda x: x[2])
    print(f"semi {N}; eccesso (px) -> numero di semi: {dict(sorted(eccessi.items()))}; testo piu lungo {peggio[2]} caratteri ({peggio[3]}); semi con tre prudenti {tre_prudenti}; errori della pagina {errs[:1]}")
    if errs or tre_prudenti == 0: print("ESITO: NON VALIDO (" + ("errori della pagina" if errs else "nessun seme con tre prudenti: il caso peggiore non e stato visto") + ")"); sys.exit(2)
    sbagliati = [x for x in res if x[1] > 0]
    print("ESITO: " + ("OK" if not sbagliati else f"FALLITO ({len(sbagliati)} semi con eccesso, massimo {max(x[1] for x in sbagliati)} px, per esempio seme {sbagliati[0][0]} con {sbagliati[0][3]})"))
    sys.exit(1 if sbagliati else 0)

asyncio.run(main())
