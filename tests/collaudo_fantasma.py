# Le opzioni di regata stanno nel riquadro delle istruzioni, che nei collaudi è saltato: si impostano direttamente.
# Regate con avversari esperti, poi prova 1 completata da un pilota automatico: verifica che il fantasma venga salvato e mostrato.
import asyncio, sys
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
async def main():
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        bloccate = 0
        for run in range(3):
            pg = await b.new_page(viewport={"width":1280,"height":800})
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.click("[data-r='0']"); await pg.wait_for_timeout(200)
            await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", "esperti"]); await pg.wait_for_timeout(200)
            await pg.evaluate("__sv.fast(25)")
            # 1.2.15: si aspetta il tempo di gioco (600 s, oltre il doppio della corsa più lenta misurata, 291 s su 80), non 24 s d'orologio: su GitHub carico la regata non arrivava in fondo e due barche risultavano «bloccate»
            for i in range(240):
                await pg.wait_for_timeout(1000)
                if await pg.evaluate("__sv.R.boats.filter(b=>!b.me).every(b=>b.fin!==null) || __sv.R.t > 600"): break
            corsa = await pg.evaluate("__sv.R.boats.filter(b=>!b.me).map(b=>[b.name, b.fin===null?('BLOCCATA '+b.leg):Math.round(b.fin), b.pen])")
            bloccate += sum(1 for x in corsa if str(x[1]).startswith("BLOCCATA"))
            print("esperti corsa", run+1, corsa, flush=True)
            await pg.close()
        # fantasma: prova 1 completata da un pilota automatico
        pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("__sv.openItem(['m',0])"); await pg.click("#c")
        await pg.keyboard.down("ArrowDown"); await pg.wait_for_timeout(900); await pg.keyboard.up("ArrowDown")
        # 1.1.0: la barca dell'1b orza quando sbanda e, con la barra ferma, la prua gira piano e la barca non arriva più (prima, con l'1a, andava dritta
        # da sola): il pilota tiene la prua di partenza con la barra, a passi fissi (fino a 300 s simulati)
        await pg.evaluate("""() => { const sv = __sv; sv.fast(0); const h0 = sv.S.h; const done = document.getElementById('done');
          for (let n = 0; n < 300 * 60 && done.hidden; n++){ const e = ((sv.S.h - h0 + 540) % 360) - 180; sv.ctl.tiller = Math.max(-1, Math.min(1, e / 20 + sv.S.r * 0.02)); sv.run(1 / 60, 1); if (n % 30 === 0) sv.panel && sv.panel(); } }""")
        await pg.wait_for_timeout(500)
        fatta = await pg.is_visible("#done")
        print("prova 1 completata:", fatta, "|", await pg.inner_text("#doneText") if await pg.is_visible("#done") else "")
        g = await pg.evaluate("Object.keys(__sv.ghosts()).map(k=>k+':'+__sv.ghosts()[k].length+' campioni')")
        print("fantasmi salvati:", g)
        await pg.evaluate("__sv.fast(1)"); await pg.click("#mRetry"); await pg.wait_for_timeout(4000)
        await pg.screenshot(path=str(OUT / "ghost.png"))
        print("errori:", errs[:2])
        await b.close()
        # 1 novembre 2026 («test dei test»): da «ambiguo» a «chiaro». Atteso: prova completata, fantasma salvato con dei
        # campioni, nessun errore; le tre corse degli esperti senza barche «BLOCCATA».
        cade = ([] if fatta else ["prova 1 non completata"]) + ([] if g and all(int(x.split(":")[1].split()[0]) > 0 for x in g) else ["nessun fantasma salvato"]) \
               + (["errori JavaScript"] if errs else []) + (["avversari bloccati: %d" % bloccate] if bloccate else [])
        print("ESITO:", "OK" if not cade else "FALLITO, " + "; ".join(cade))
        if cade: sys.exit(1)
asyncio.run(main())
