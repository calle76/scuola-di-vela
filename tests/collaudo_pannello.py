# Verifica che il pannello stia tutto nella finestra senza scorrere e che il riquadro delle istruzioni fermi il gioco.
# Uso: python collaudo_pannello.py [larghezza altezza]   (predefinito 1360 650: schermo 1360x768 meno le barre del browser)
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1360, 650)
PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        eccede = []
        for li, n in enumerate([13, 7, 13, 5, 9, 5]):
            await pg.evaluate(f"__sv.openItem(['l',{li}])")
            for k in range(n):
                await pg.evaluate(f"__sv.showStep({k})"); await pg.wait_for_timeout(100)
                d = await pg.evaluate(PH)
                if d > 0: eccede.append(f"lezione {li+1} passo {k+1}: +{d}")
        for it, nome in [("['m',0]", "prova 1"), ("['m',4]", "prova 5"), ("'free'", "navigazione libera")]:
            await pg.evaluate(f"__sv.openItem({it})"); await pg.wait_for_timeout(400)
            d = await pg.evaluate(PH)
            if d > 0: eccede.append(f"{nome}: +{d}")
        # regata dopo il via, con la spiegazione di un contatto
        await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", "60"])
        await pg.evaluate("__sv.fast(10)"); await pg.wait_for_timeout(7000); await pg.evaluate("__sv.fast(1)")
        await pg.evaluate("__sv.R.lastRule='Contatto con Blu: tu eri mure a sinistra e dovevi lasciare strada a chi era mure a dritta. Penalità di 15 secondi.'")
        await pg.wait_for_timeout(300); d = await pg.evaluate(PH)
        if d > 0: eccede.append(f"regata dopo il via: +{d}")
        await pg.screenshot(path=str(OUT / f"P_regata_{W}x{H}.png"))
        print(f"finestra {W}x{H}: pannello che eccede:", eccede or "nessuno")
        # riquadro delle istruzioni
        await pg.evaluate("__sv.skipBrief=false"); await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", "180"])
        await pg.evaluate("__sv.openItem(['r',0])"); await pg.wait_for_timeout(1000)
        fermo = await pg.evaluate("__sv.R.t") == -180 and await pg.evaluate("__sv.briefing")
        await pg.screenshot(path=str(OUT / f"P_istruzioni_{W}x{H}.png"))
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(800)
        parte = await pg.evaluate("__sv.R.t") > -180 and not await pg.evaluate("__sv.briefing")
        await pg.click("#rBrief"); t1 = await pg.evaluate("__sv.R.t"); await pg.wait_for_timeout(600)
        riaperto = await pg.evaluate("__sv.R.t") == t1; await pg.click("#bGo")
        await pg.evaluate("__sv.openItem(['m',0])"); await pg.wait_for_timeout(800)
        prova = await pg.evaluate("__sv.S.time") == 0; await pg.click("#bGo"); await pg.wait_for_timeout(800)
        prova = prova and await pg.evaluate("__sv.S.time") > 0.5
        print("istruzioni: regata ferma prima di Parti", fermo, "| parte con Invio", parte, "| riaperte a gioco fermo", riaperto, "| cronometro della prova parte con Parti", prova)
        print("errori:", errs)
        await b.close()
asyncio.run(main())
