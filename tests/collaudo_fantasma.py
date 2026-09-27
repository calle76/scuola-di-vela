# Regate con avversari esperti, poi prova 1 completata da un pilota automatico: verifica che il fantasma venga salvato e mostrato.
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
        for run in range(3):
            pg = await b.new_page(viewport={"width":1280,"height":800})
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.click("[data-r='0']"); await pg.wait_for_timeout(200)
            await pg.select_option("#aiLevel", "esperti"); await pg.wait_for_timeout(200)
            await pg.evaluate("__sv.fast(25)")
            for i in range(24):
                await pg.wait_for_timeout(1000)
                if await pg.evaluate("__sv.R.boats.filter(b=>!b.me).every(b=>b.fin!==null)"): break
            print("esperti corsa", run+1, await pg.evaluate("__sv.R.boats.filter(b=>!b.me).map(b=>[b.name, b.fin===null?('BLOCCATA '+b.leg):Math.round(b.fin), b.pen])"), flush=True)
            await pg.close()
        # fantasma: prova 1 completata da un pilota automatico
        pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("__sv.openItem(['m',0])"); await pg.click("#c")
        await pg.keyboard.down("ArrowDown"); await pg.wait_for_timeout(900); await pg.keyboard.up("ArrowDown")
        await pg.evaluate("__sv.fast(10)")
        for i in range(20):
            await pg.wait_for_timeout(1000)
            if await pg.is_visible("#done"): break
        print("prova 1 completata:", await pg.is_visible("#done"), "|", await pg.inner_text("#doneText") if await pg.is_visible("#done") else "")
        g = await pg.evaluate("Object.keys(__sv.ghosts()).map(k=>k+':'+__sv.ghosts()[k].length+' campioni')")
        print("fantasmi salvati:", g)
        await pg.evaluate("__sv.fast(1)"); await pg.click("#mRetry2"); await pg.wait_for_timeout(4000)
        await pg.screenshot(path=str(OUT / "ghost.png"))
        print("errori:", errs[:2])
        await b.close()
asyncio.run(main())
