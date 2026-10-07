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
        # le misure di eccesso qui sotto valgono solo con i caratteri veri del gioco: con i font di sistema
        # la larghezza e l'altezza del testo sono diverse e la prova non direbbe niente di vero sul margine reale.
        await pg.evaluate("document.fonts.ready")
        caratteri = await pg.evaluate("""() => ({
            "barlow 700": document.fonts.check('700 16px "Barlow Semi Condensed"'),
            "barlow 600": document.fonts.check('600 16px "Barlow Semi Condensed"'),
            "source serif 400": document.fonts.check('400 16px "Source Serif 4"'),
            "facce Barlow presenti e caricate (check() da solo dà vero anche senza)": [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"),
        })""")
        caratteri_ok = all(caratteri.values())
        print("caratteri del gioco caricati:", caratteri_ok, caratteri)
        eccede = []; misure = []
        for li, n in enumerate([13, 7, 13, 5, 9, 5]):
            await pg.evaluate(f"__sv.openItem(['l',{li}])")
            for k in range(n):
                await pg.evaluate(f"__sv.showStep({k})"); await pg.wait_for_timeout(100)
                d = await pg.evaluate(PH); misure.append(d)
                if d > 0: eccede.append(f"lezione {li+1} passo {k+1}: +{d}")
        for it, nome in [("['m',0]", "prova 1"), ("['m',4]", "prova 5"), ("'free'", "navigazione libera")]:
            await pg.evaluate(f"__sv.openItem({it})"); await pg.wait_for_timeout(400)
            d = await pg.evaluate(PH); misure.append(d)
            if d > 0: eccede.append(f"{nome}: +{d}")
            # 0.19.2: riga dei tasti mai tagliata; «Q vista» nella riga solo se ci sta, altrimenti sul mare
            r = await pg.evaluate("(()=>{const k=document.getElementById('kQ'),p=k.parentNode;return [p.scrollWidth-p.clientWidth, !k.hidden]})()")
            print(f"  {nome}: riga dei tasti eccede di {r[0]} px, «Q vista» nella riga {r[1]}")
            if r[0] > 0: eccede.append(f"{nome}: riga dei tasti tagliata di {r[0]} px")
        # regata dopo il via, con la spiegazione di un contatto
        await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", "60"])
        await pg.evaluate("__sv.fast(10)"); await pg.wait_for_timeout(7000); await pg.evaluate("__sv.fast(1)")
        await pg.evaluate("__sv.R.lastRule='Contatto con Blu: tu eri mure a sinistra e dovevi lasciare strada a chi era mure a dritta. Penalità di 15 secondi.'")
        await pg.wait_for_timeout(300); d = await pg.evaluate(PH); misure.append(d)
        if d > 0: eccede.append(f"regata dopo il via: +{d}")
        r = await pg.evaluate("(()=>{const k=document.getElementById('kQ'),p=k.parentNode;return [p.scrollWidth-p.clientWidth, !k.hidden]})()")
        print(f"  regata dopo il via: riga dei tasti eccede di {r[0]} px, «Q vista» nella riga {r[1]}")
        if r[0] > 0: eccede.append(f"regata: riga dei tasti tagliata di {r[0]} px")
        await pg.screenshot(path=str(OUT / f"P_regata_{W}x{H}.png"))
        print(f"finestra {W}x{H}: eccesso massimo del pannello (pixel): {max(misure)}")
        print(f"finestra {W}x{H}: pannello che eccede:", eccede or "nessuno")
        if not caratteri_ok: print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, le misure sopra non sono attendibili")
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
            # 0.19: il riquadro delle istruzioni (testi delle prove cambiati) deve stare nella finestra senza scorrere
            oltre = await pg2.evaluate("(()=>{const e=document.getElementById('briefOv');return e.scrollHeight-e.clientHeight})()")
            riquadri.append(oltre)
            if oltre > 0: errs2.append(f"{nome}: il riquadro delle istruzioni eccede di {oltre} px")
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
        atteso = {"prova 1": "Tempo 0:00 \u00b7 oro entro 1:35", "prova 2": "Tempo 0:00 \u00b7 oro entro 2:25",
                  "prova 3": "Tempo 0:00 \u00b7 oro entro 3:20", "prova 4": "Tempo 0:00 \u00b7 oro entro 5:35",
                  "prova 5": "Tempo 0:00 \u00b7 oro entro 5:55"}
        riquadri = []
        print("gioco vero, senza #collaudo:")
        await giro("regata 1", lambda: pg2.click("[data-r='0']"), "#rRestart", True)
        for n in range(1, 6):
            await giro(f"prova {n}", lambda n=n: pg2.locator("#menu button.item", has_text=f"Prova {n}").click(), "#mRetry", False)
        print(f"riquadro delle istruzioni: misurato {len(riquadri)} volte, eccesso massimo (pixel): {max(riquadri) if riquadri else 'nessuna misura'}")
        if not riquadri: errs2.append("riquadro delle istruzioni mai misurato")
        print("errori:", errs + errs2)
        await b.close()
        if not caratteri_ok: sys.exit(1)
asyncio.run(main())
