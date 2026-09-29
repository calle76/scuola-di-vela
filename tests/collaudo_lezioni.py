# Guida la barca con la tastiera simulata per verificare che i passi pratici delle lezioni siano completabili.
# Dalla 0.16 la lezione 1 si guida con le frecce del timone (barra): vento da nord, prua a est, ← poggia e → orza.
# Nota: i passi «cazzare» della lezione 1 e «prepararsi» della lezione 5 possono risultare NON COMPLETATI perché lo script
# cazza troppo e non corregge: non è un difetto del gioco.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
async def hold_until(pg, key, maxs, label):
    await pg.keyboard.down(key)
    t=0
    while t < maxs:
        await pg.wait_for_timeout(250); t+=0.25
        if await pg.evaluate("__sv.stepDone"): break
    await pg.keyboard.up(key)
    ok = await pg.evaluate("__sv.stepDone")
    I = await pg.evaluate("(()=>{const i=__sv.readI(); return {twa:Math.round(i.twa), kn:+i.kn.toFixed(1), tt:i.tt, heel:Math.round(i.heel)}})()")
    print(f"{label}: {'OK' if ok else 'NON COMPLETATO'} in {t:.1f}s  {I}")
    return ok
async def wait_until(pg, maxs, label):
    t=0
    while t < maxs:
        await pg.wait_for_timeout(250); t+=0.25
        if await pg.evaluate("__sv.stepDone"): break
    ok = await pg.evaluate("__sv.stepDone")
    I = await pg.evaluate("(()=>{const i=__sv.readI(); return {twa:Math.round(i.twa), kn:+i.kn.toFixed(1), tt:i.tt, heel:Math.round(i.heel)}})()")
    print(f"{label}: {'OK' if ok else 'NON COMPLETATO'} in {t:.1f}s  {I}")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        # Lezione 1
        await pg.evaluate("__sv.openItem(['l',0])"); await pg.evaluate("__sv.showStep(6)"); await pg.click("#c")
        await hold_until(pg, "ArrowLeft", 12, "L1 poggiare")
        await pg.evaluate("__sv.showStep(7)")
        await hold_until(pg, "ArrowRight", 25, "L1 orzare fino all'angolo morto")
        await pg.evaluate("__sv.showStep(8)")
        # come un giocatore: poggia finché il vento arriva di fianco, poi rilascia e aspetta che la barca riparta
        await pg.keyboard.down("ArrowLeft")
        for i in range(100):
            await pg.wait_for_timeout(250)
            if await pg.evaluate("__sv.readI().twa > 80"): break
        await pg.keyboard.up("ArrowLeft")
        await wait_until(pg, 15, "L1 ripartire")
        await pg.evaluate("__sv.showStep(9)")
        await hold_until(pg, "s", 10, "L1 lascare")
        await pg.evaluate("__sv.showStep(10)")
        await hold_until(pg, "w", 1.4, "L1 cazzare (primo tratto)")
        await wait_until(pg, 4, "L1 cazzare (attesa)")
        await pg.evaluate("__sv.showStep(11)")
        await hold_until(pg, "w", 10, "L1 troppo cazzata")
        # Lezione 2
        await pg.evaluate("__sv.openItem(['l',1])"); await pg.evaluate("__sv.showStep(1)"); await pg.click("#c")
        await hold_until(pg, "ArrowLeft", 5, "L2 barra a sinistra")
        await pg.evaluate("__sv.showStep(2)")
        await hold_until(pg, "ArrowRight", 5, "L2 barra a dritta")
        # Lezione 3 filetti
        await pg.evaluate("__sv.openItem(['l',2])"); await pg.evaluate("__sv.showStep(7)"); await pg.click("#c")
        await hold_until(pg, "ArrowDown", 10, "L3 filetto sopravento")
        await pg.evaluate("__sv.showStep(9)")
        await hold_until(pg, "ArrowUp", 10, "L3 filetto sottovento")
        # Lezione 5: virata lanciata (vento da nord, prua a est: barra sottovento = a dritta)
        await pg.evaluate("__sv.openItem(['l',4])"); await pg.evaluate("__sv.showStep(1)"); await pg.click("#c")
        await pg.keyboard.down("ArrowRight"); await pg.wait_for_timeout(700); await pg.keyboard.up("ArrowRight")
        await pg.keyboard.down("ArrowUp"); await pg.wait_for_timeout(1500); await pg.keyboard.up("ArrowUp")
        await wait_until(pg, 12, "L5 prepararsi (bolina lanciata)")
        await pg.evaluate("__sv.showStep(2)")
        await hold_until(pg, "ArrowRight", 8, "L5 virata")
        S = await pg.evaluate("({tacks: __sv.S.tacks})"); print("   virate contate:", S)
        await wait_until(pg, 8, "L5 virata (assestamento)")
        # Lezione 6: scuffia volontaria
        await pg.evaluate("__sv.openItem(['l',5])"); await pg.evaluate("__sv.showStep(2)"); await pg.click("#c")
        await pg.keyboard.down("ArrowRight"); await pg.wait_for_timeout(600); await pg.keyboard.up("ArrowRight")
        await pg.keyboard.down("ArrowUp"); await pg.wait_for_timeout(3000); await pg.keyboard.up("ArrowUp")
        await wait_until(pg, 60, "L6 scuffia")
        await pg.screenshot(path=str(OUT / "B_cap.png"))
        await pg.evaluate("__sv.showStep(3)"); await pg.keyboard.press("r")
        await wait_until(pg, 8, "L6 raddrizzare")
        print("errori:", errs[:5])
        await b.close()
asyncio.run(main())
