# Apre il menu, ogni passo di ogni lezione, tutte le prove e la navigazione libera, e segnala errori JavaScript.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console:"+m.text) if m.type=="error" and "Failed to load" not in m.text else None)
        await pg.goto(URL); await pg.wait_for_timeout(600)
        await pg.screenshot(path=str(OUT / "A_menu.png"), full_page=True)
        counts=[13,7,13,5,9,5]
        for li,n in enumerate(counts):
            await pg.evaluate(f"__sv.openItem(['l',{li}])")
            for k in range(n):
                await pg.evaluate(f"__sv.showStep({k})"); await pg.wait_for_timeout(350)
                if (li,k) in [(0,0),(0,3),(0,5),(2,0),(2,6),(4,0),(5,0)]:
                    await pg.screenshot(path=str(OUT / f"A_L{li+1}_{k+1}.png"))
        for mi in range(5):
            await pg.evaluate(f"__sv.openItem(['m',{mi}])"); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(OUT / "A_m5.png"))
        await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(OUT / "A_free.png"))
        print("errori:", errs[:5])
        await b.close()
asyncio.run(main())
