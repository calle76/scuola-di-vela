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
        # 0.19.2: linea d'arrivo a scacchi e scritta a pillola, a 1360x650 e a più zoom (nomi in tests/output/L_*.png);
        # 0.19.3: anche zoom minimo e partenza di ogni prova con Q tenuto.
        # L'aspetto lo giudica chi guarda le immagini, non questo collaudo.
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(600)
        VICINO = """(() => { const sv = __sv, S = sv.S, M = sv.marks, L = M[M.length - 1]; sv.fast(0); S.markIdx = M.length - 1;
          S.x = L.x - L.nx * 10 + L.ny * 6; S.y = L.y - L.ny * 10 - L.nx * 6; S.h = (Math.atan2(L.nx, -L.ny) * 180 / Math.PI + 360) % 360; })()"""
        nomi = []
        async def foto(nome): await pg.screenshot(path=str(OUT / nome)); nomi.append(nome)
        for mi in range(5):
            await pg.goto("about:blank"); await pg.goto(URL); await pg.wait_for_timeout(600)   # pagina nuova: zoom di partenza 1
            await pg.evaluate(f"__sv.openItem(['m',{mi}])"); await pg.evaluate(VICINO)
            await pg.wait_for_timeout(2000); await foto(f"L_prova{mi+1}_zoom1.png")
            for _ in range(4): await pg.click("#zIn")
            await pg.wait_for_timeout(2000); await foto(f"L_prova{mi+1}_zoom2.4.png")
            for _ in range(7): await pg.click("#zOut")
            await pg.wait_for_timeout(2000); await foto(f"L_prova{mi+1}_zoom0.4.png")
            for _ in range(8): await pg.click("#zOut")   # 0.19.3: zoom minimo 0,1
            await pg.wait_for_timeout(2500); await foto(f"L_prova{mi+1}_zoom_minimo.png")
            # 0.19.3: alla partenza, a zoom 1, con Q tenuto (vista del percorso)
            await pg.goto("about:blank"); await pg.goto(URL); await pg.wait_for_timeout(600)
            await pg.evaluate(f"__sv.openItem(['m',{mi}]); __sv.fast(0)")
            await pg.keyboard.down("q"); await pg.wait_for_timeout(1200); await foto(f"L_prova{mi+1}_partenza_con_Q.png"); await pg.keyboard.up("q")
        await pg.evaluate("__sv.openItem(['r',0])"); await pg.wait_for_timeout(1500); await foto("L_regata1_partenza.png")
        await pg.keyboard.down("q"); await pg.wait_for_timeout(1200); await foto("L_regata1_partenza_con_Q.png"); await pg.keyboard.up("q"); await pg.wait_for_timeout(1200)
        await pg.evaluate("""(() => { const sv = __sv, R = sv.R, S = sv.S, w = sv.twd * Math.PI / 180; sv.fast(0); R.t = 200; R.boats[0].leg = 2;
          S.x = R.center.x + Math.sin(w) * 20; S.y = R.center.y - Math.cos(w) * 20; S.h = (sv.twd + 180) % 360; })()""")
        await pg.wait_for_timeout(1500); await foto("L_regata1_arrivo.png")
        print("schermate della linea:", " ".join(nomi))
        print("errori:", errs[:5])
        await b.close()
asyncio.run(main())
