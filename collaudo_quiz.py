# Completa i sei quiz di ripasso e verifica che il miglior punteggio venga salvato e mostrato nel menu.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE); await pg.wait_for_timeout(400)
        for li in range(6):
            await pg.click(f"[data-q='{li}']")
            n=0
            while True:
                if await pg.locator("#qzAgain").count(): break
                await pg.locator(".opt").first.click()
                if n==0 and li==2: await pg.screenshot(path=str(OUT / "Q1.png"))
                await pg.click("#qzNext"); n+=1
            txt = await pg.inner_text(".score")
            if li==2: await pg.screenshot(path=str(OUT / "Q2.png"))
            await pg.click("#qzClose"); await pg.wait_for_timeout(150)
            print(f"Lezione {li+1}: {n} domande, punteggio {txt}")
        print("menu:", (await pg.inner_text(".review"))[:160].replace("\n"," | "))
        print("errori:", errs)
        await b.close()
asyncio.run(main())
