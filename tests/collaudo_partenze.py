# Le opzioni di regata stanno nel riquadro delle istruzioni, che nei collaudi è saltato: si impostano direttamente.
# Misura di quanti secondi gli avversari tagliano la linea dopo lo zero, con 1, 3 e 5 minuti di preparazione; verifica la regata in solitaria.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
WATCH = """(()=>{ window._st={}; for (const b of __sv.R.boats){ let v=b.leg; Object.defineProperty(b,'leg',{get(){return v}, set(n){ if(v===0&&n===1) window._st[b.name]=+__sv.R.t.toFixed(1); v=n; }}); } })()"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for cd in ["180", "60", "180", "60", "300"]:
            pg = await b.new_page(viewport={"width":1280,"height":800})
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.click("[data-r='0']"); await pg.wait_for_timeout(200)
            await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", cd]); await pg.wait_for_timeout(200)
            await pg.evaluate(WATCH); await pg.evaluate("__sv.fast(20)")
            await pg.wait_for_timeout(int((int(cd)+60)/20*1000)+1500)
            print(f"preparazione {cd} s → secondi di ritardo sulla partenza:", await pg.evaluate("window._st"), "| partenze anticipate:", await pg.evaluate("__sv.R.boats.filter(b=>!b.me&&b.ocs).map(b=>b.name)"), "| errori:", errs[:1], flush=True)
            await pg.close()
        # solo contro il fantasma
        pg = await b.new_page(viewport={"width":1280,"height":800}); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300); await pg.click("[data-r='0']"); await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", "nessuno"]); await pg.wait_for_timeout(300)
        print("modalità solitaria, barche in acqua:", await pg.evaluate("__sv.R.boats.length"), "| testo:", (await pg.evaluate("__sv.R.brief"))[-90:])
        await pg.click('#openSet'); await pg.click("#viewMode button[data-v='nord']"); await pg.click('#setClose')
        await pg.click("#c"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(OUT / "turn.png")); await pg.keyboard.up("ArrowLeft")
        print("errori:", errs[:1])
        await b.close()
asyncio.run(main())
