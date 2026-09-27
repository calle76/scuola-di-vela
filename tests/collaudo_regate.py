# Fa correre regate accelerate (25x) e verifica che tutti gli avversari partano, girino la boa e arrivino.
# Uso: python collaudo_regate.py <numero di regate> <0 = a bastone, 1 = nelle raffiche>
import asyncio, sys
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
async def main(runs, race):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for run in range(runs):
            pg = await b.new_page(viewport={"width":1280,"height":800})
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.click("[data-r='%d']" % race); await pg.wait_for_timeout(200)
            await pg.evaluate("__sv.fast(25)")
            for i in range(24):
                await pg.wait_for_timeout(1000)
                if await pg.evaluate("__sv.R.boats.filter(b=>!b.me).every(b=>b.fin!==null)"): break
            st = await pg.evaluate("[Math.round(__sv.R.t), __sv.R.boats.filter(b=>!b.me).map(b=>[b.name, b.fin===null?('BLOCCATA tratto '+b.leg):Math.round(b.fin), b.pen])]")
            line = f"regata {race+1} corsa {run+1}: t={st[0]} {st[1]} errori={errs[:1]}"
            print(line, flush=True); open(OUT / "race_results.txt","a").write(line+"\n")
            await pg.close()
        await b.close()
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
