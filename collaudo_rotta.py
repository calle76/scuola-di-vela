# Lezione 2, «Tenere la rotta»: senza correzioni la barca deve uscire di rotta; con piccoli colpi di barra il passo si completa.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        # senza correzioni: quanto esce di rotta in 15 s?
        await pg.evaluate("__sv.openItem(['l',1])"); await pg.evaluate("__sv.showStep(5)"); await pg.click("#c")
        maxoff=0
        for i in range(60):
            await pg.wait_for_timeout(250)
            off = await pg.evaluate("Math.abs(((__sv.S.h - __sv.S.course + 540) % 360) - 180)")
            maxoff=max(maxoff, off)
        print("senza correzioni: scostamento massimo", round(maxoff), "gradi; passo completato:", await pg.evaluate("__sv.stepDone"))
        # con correzioni a colpetti
        await pg.evaluate("__sv.showStep(4)"); await pg.evaluate("__sv.showStep(5)")
        t=0
        while t < 40 and not await pg.evaluate("__sv.stepDone"):
            off, r = await pg.evaluate("[((__sv.S.h - __sv.S.course + 540) % 360) - 180, __sv.S.r]")
            # come una persona: corregge solo se la prua non sta già rientrando
            if off > 2 and r > -3: await pg.keyboard.down("ArrowRight"); await pg.wait_for_timeout(70); await pg.keyboard.up("ArrowRight")
            elif off < -2 and r < 3: await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(70); await pg.keyboard.up("ArrowLeft")
            await pg.wait_for_timeout(80)
            t += 0.15
        print("con correzioni: completato", await pg.evaluate("__sv.stepDone"), "in circa", round(t), "s |", await pg.inner_text("#hint"))
        await pg.screenshot(path=str(OUT / "course.png"))
        print("errori:", errs)
        await b.close()
asyncio.run(main())
