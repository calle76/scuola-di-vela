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
        # Il riquadro nel gioco vero, senza #collaudo: il valore di partenza di briefSkip si vede solo qui.
        # Dalla 0.15 alla 0.17 era vero anche fuori dai collaudi (una graffa mancante) e nessuno se n'era accorto,
        # perche i collaudi lo mettevano a mano con __sv.skipBrief = false.
        pg2 = await b.new_page(viewport={"width": W, "height": H}); errs2 = []
        pg2.on("pageerror", lambda e: errs2.append(str(e)))
        await pg2.goto(BASE); await pg2.wait_for_timeout(500)
        async def riquadro(regata):
            # «Parti», e i menu Avversari e Preparazione solo in regata
            return (not await pg2.evaluate("document.getElementById('briefOv').hidden")
                    and await pg2.evaluate("document.getElementById('bRaceOpts').hidden") != regata
                    and await pg2.inner_text("#bGo") == "Parti")
        # 2,5 s col riquadro aperto: se il tempo contasse, l'orologio della prova segnerebbe 0:02
        async def giro(nome, apri, rifai, regata):
            await apri(); await pg2.wait_for_timeout(2500)
            ok = await riquadro(regata)
            fermo = regata or await pg2.inner_text("#stClock") == atteso[nome]
            await pg2.keyboard.press("Enter"); await pg2.wait_for_timeout(1500)   # non un clic su #bGo: se il riquadro manca, il clic aspetterebbe invano
            parte = regata or await pg2.inner_text("#stClock") == atteso[nome].replace("0:00", "0:01")
            await pg2.click(rifai); await pg2.wait_for_timeout(2500)
            ok2 = await riquadro(regata)
            da_zero = regata or await pg2.inner_text("#stClock") == atteso[nome]
            print(f"  {nome}: riquadro dal menu {ok} | con Ricomincia {ok2}" +
                  ("" if regata else f" | orologio fermo {fermo} | parte con Parti {parte} | riparte da zero {da_zero}"))
            if not (ok and ok2): errs2.append(f"{nome}: il riquadro iniziale non compare nel gioco vero")
            if not (fermo and parte and da_zero): errs2.append(f"{nome}: il cronometro non parte con Parti")
            await pg2.click("#toMenu"); await pg2.wait_for_timeout(300)
        # le fasce stampate nell'orologio: se cambiassero, il confronto qui sotto lo direbbe
        atteso = {"prova 1": "Tempo 0:00 \u00b7 oro entro 1:30", "prova 2": "Tempo 0:00 \u00b7 oro entro 2:20",
                  "prova 3": "Tempo 0:00 \u00b7 oro entro 3:05", "prova 4": "Tempo 0:00 \u00b7 oro entro 5:30",
                  "prova 5": "Tempo 0:00 \u00b7 oro entro 5:55"}
        print("gioco vero, senza #collaudo:")
        await giro("regata 1", lambda: pg2.click("[data-r='0']"), "#rRestart", True)
        for n in range(1, 6):
            await giro(f"prova {n}", lambda n=n: pg2.locator("#menu button.item", has_text=f"Prova {n}").click(), "#mRetry", False)
        print("errori:", errs + errs2)
        await b.close()
asyncio.run(main())
