# Pannello delle lezioni a 1360x650 (1.1.3): ogni passo di ogni lezione, con il testo di fine passo mostrato quando il passo ha una
# condizione (il caso più lungo), non deve far scorrere il pannello né la pagina. collaudo_pannello.py misura solo alcuni casi peggiori:
# il passo 6.4 «Raddrizzare» sforava di 17 px dalla 1.0.x senza che nessun collaudo lo vedesse. Il metro conta i passi misurati
# e deve averli misurati tutti (quelli di LESSONS). Dalla 1.2.1 anche i passi con l'esercizio in regata, con il testo di fine passo. Uso: python collaudo_pannello_lezioni.py   (browser con BROWSER=firefox)
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        n, attesi, oltre = await pg.evaluate("""() => { const sv = __sv, out = []; let n = 0, attesi = 0;
          for (let l = 0; l < LESSONS.length; l++){ attesi += LESSONS[l].steps.length;
            for (let s = 0; s < LESSONS[l].steps.length; s++){ sv.openItem(['l', l]); sv.showStep(s); if (LESSONS[l].steps[s].cond || LESSONS[l].steps[s].esercizio) sv.completeStep(); if (sv.panel) sv.panel(); n++;
              const p = document.querySelector('.panel'), e = p.scrollHeight - p.clientHeight, g = document.documentElement.scrollHeight - innerHeight;
              if (e > 0 || g > 0) out.push(`${l + 1}.${s + 1} ${LESSONS[l].steps[s].title}: pannello ${e} px, pagina ${g} px`); } }
          return [n, attesi, out]; }""")
        await b.close()
    print(f"passi misurati {n} su {attesi}; oltre la finestra: {len(oltre)}")
    for x in oltre: print("  NO ", x)
    print("errori della pagina:", errs[:2])
    ok = n == attesi and n > 0 and not oltre and not errs
    print("ESITO: " + ("OK" if ok else "FALLITO")); sys.exit(0 if ok else 1)
asyncio.run(main())
