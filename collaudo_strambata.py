# Strambate con la vela tutta aperta: conta le scuffie e misura lo sbandamento massimo.
# Uso: python collaudo_strambata.py <nodi: 6, 10 o 15> <numero di prove>
import asyncio, sys
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
KICK=sys.argv[3] if len(sys.argv)>3 else "260"
URL = BASE + "#collaudo"
async def trial(pg, kn):
    await pg.goto("about:blank"); await pg.goto(URL); await pg.wait_for_timeout(250)
    await pg.evaluate("__sv.openItem('free')")
    await pg.evaluate("""(k)=>{ for (const [id,v] of [['wSpd',k],['gustSel','0']]){ const e=document.getElementById(id); e.value=v; e.dispatchEvent(new Event('change')); } }""", kn)
    await pg.wait_for_timeout(100)
    await pg.click("#c"); await pg.evaluate("__sv.kick(%s)" % KICK); await pg.evaluate("__sv.fast(3)")
    await pg.keyboard.down("ArrowDown"); await pg.wait_for_timeout(1300); await pg.keyboard.up("ArrowDown")
    await pg.wait_for_timeout(1500)
    await pg.keyboard.down("ArrowLeft")
    for i in range(40):
        await pg.wait_for_timeout(150)
        if await pg.evaluate("__sv.S.gybesV > 0 || __sv.S.gybesC > 0"): break
    await pg.keyboard.up("ArrowLeft")
    maxh=0
    for i in range(12):
        await pg.wait_for_timeout(150)
        maxh=max(maxh, await pg.evaluate("__sv.S.capsized ? 90 : __sv.S.heel"))
    return await pg.evaluate("[__sv.S.gybesV, __sv.S.gybesC, __sv.S.capsizes, __sv.S.capCause || '']"), round(maxh)
async def main(kn, n):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":800})
        res=[await trial(pg, kn) for _ in range(n)]
        caps=sum(1 for r in res if r[0][2]>0); viol=sum(1 for r in res if r[0][0]>0)
        print(f"vento {kn} nodi: strambate violente {viol}/{n}, scuffie {caps}/{n}, sbandamento massimo {[r[1] for r in res]}, cause {[r[0][3] for r in res]}", flush=True)
        await b.close()
asyncio.run(main(sys.argv[1], int(sys.argv[2])))
