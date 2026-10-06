# Pulsanti didattici «Cazza» e «Lasca» della lezione 1 (data-a="cazza"/"lasca", gestiti con semHeld).
# Difetto 0.18.1: a fine corsa il passo si completa e compare la scritta di passo completato; questo
# aggiunge testo sopra ai due pulsanti nel pannello, che si spostano in basso. Un giocatore che clicca
# piu' volte di seguito nello stesso punto dello schermo (senza rimirare il pulsante a ogni clic, come
# capita cliccando in fretta) continua a cliccare dove il pulsante STAVA: il clic cade su quello che gli
# e' scorso sotto. Qui si verifica con un vero clic del mouse, fermo nello stesso punto, ripetuto.
# Uso: python collaudo_pulsanti.py
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
URL = BASE + "#collaudo"
W, H = 1360, 650

async def clic_fermo(pg, box, n):
    """Clicca n volte con il mouse fermo nel punto box (niente nuova mira a ogni clic, come un clic ripetuto in fretta)."""
    tracce = []
    for _ in range(n):
        await pg.mouse.move(box["x"], box["y"]); await pg.mouse.down()
        await pg.wait_for_timeout(100); await pg.mouse.up(); await pg.wait_for_timeout(60)
        sheet = await pg.evaluate("__sv.ctl.sheet")
        done = await pg.evaluate("__sv.stepDone")
        el = await pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y); if(!e) return null; const a=e.closest('[data-a]'); return a ? a.dataset.a : (e.id || e.tagName)}", [box["x"], box["y"]])
        tracce.append((sheet, done, el))
    return tracce

async def bbox(pg, selettore):
    r = await pg.evaluate("(sel)=>{const r=document.querySelector(sel).getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2}}", selettore)
    return r

async def main():
    sbagliati = []
    n_clic_lasca = n_clic_cazza = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)

        # 1) «La scotta: lascare» (passo 9): tenere il mouse fermo sul pulsante Lasca e cliccare fino a
        #    oltre fine corsa; il pulsante deve restare sotto il clic, la scotta deve fermarsi a 1, e il
        #    passo completato deve restare completato.
        await pg.evaluate("__sv.openItem(['l',0])"); await pg.evaluate("__sv.showStep(9)"); await pg.click("#c")
        await pg.wait_for_timeout(200)
        box = await bbox(pg, '[data-a="lasca"]')
        tracce = await clic_fermo(pg, box, 22)
        n_clic_lasca = len(tracce)
        ultimo_sheet, ultimo_done, ultimo_el = tracce[-1]
        print(f"Lasca: {n_clic_lasca} clic fermi su {box}; ultimo sheet={ultimo_sheet:.3f} stepDone={ultimo_done} elemento={ultimo_el}")
        if ultimo_el != "lasca": sbagliati.append(f"Lasca: dopo {n_clic_lasca} clic il pulsante non e' piu' sotto il clic (elemento: {ultimo_el})")
        if ultimo_sheet < 0.99: sbagliati.append(f"Lasca: la scotta non e' arrivata a fine corsa (sheet={ultimo_sheet:.3f})")
        if not ultimo_done: sbagliati.append("Lasca: il passo «lascare» non e' (o non e' restato) completato")
        completato_poi_annullato = any(tracce[i][1] and not tracce[i+1][1] for i in range(len(tracce) - 1))
        if completato_poi_annullato: sbagliati.append("Lasca: il passo completato e' stato annullato da un clic successivo")

        # 2) «La scotta: cazzare» (passo 10): lo stesso con Cazza, che deve spingere la scotta verso 0
        #    e restare completato («tt === ok») anche continuando a cliccare dopo il traguardo.
        await pg.evaluate("__sv.ctl.sheet = 0.6"); await pg.evaluate("__sv.showStep(10)"); await pg.wait_for_timeout(200)
        box = await bbox(pg, '[data-a="cazza"]')
        tracce = await clic_fermo(pg, box, 22)
        n_clic_cazza = len(tracce)
        ultimo_sheet, ultimo_done, ultimo_el = tracce[-1]
        print(f"Cazza: {n_clic_cazza} clic fermi su {box}; ultimo sheet={ultimo_sheet:.3f} stepDone={ultimo_done} elemento={ultimo_el}")
        if ultimo_el != "cazza": sbagliati.append(f"Cazza: dopo {n_clic_cazza} clic il pulsante non e' piu' sotto il clic (elemento: {ultimo_el})")
        if ultimo_sheet > 0.15: sbagliati.append(f"Cazza: la scotta non e' continuata a chiudersi dopo il completamento (sheet={ultimo_sheet:.3f})")
        if not ultimo_done: sbagliati.append("Cazza: il passo «cazzare» non e' (o non e' restato) completato")
        completato_poi_annullato = any(tracce[i][1] and not tracce[i+1][1] for i in range(len(tracce) - 1))
        if completato_poi_annullato: sbagliati.append("Cazza: il passo completato e' stato annullato da un clic successivo")

        print("errori pagina:", errs[:5])
        await b.close()

    casi = [n_clic_lasca, n_clic_cazza]
    print("casi misurati: clic su Lasca", n_clic_lasca, "- clic su Cazza", n_clic_cazza)
    print("casi sbagliati:", sbagliati or "nessuno")
    vuoto = [n for n in casi if n == 0]
    if vuoto: print("COLLAUDO NON VALIDO: una delle misure non ha nessun caso")
    sys.exit(1 if (sbagliati or errs or vuoto) else 0)
asyncio.run(main())
