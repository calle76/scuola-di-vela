# Collaudo del ripasso: risposte sbagliate apposta, elenco finale, "Ripassa solo le sbagliate", record solo con ripasso completo.
# Fallisce se misura zero casi (ogni controllo conta quanti casi ha verificato).
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
fail = []; casi = 0
def chk(c, m):
    global casi; casi += 1
    if not c: fail.append(m); print("FALLITO:", m)

# risponde a tutte le domande in corso; wrong_idx = posizioni (nel giro) da sbagliare, le altre giuste.
# Si riconosce la giusta dal fatto che QUIZ è nella pagina: si legge la risposta giusta da lì.
async def gira(pg, li, wrong_pos):
    n = 0
    while not await pg.locator("#qzAgain").count():
        q = await pg.inner_text(".qz .q")
        right = await pg.evaluate("([li,q])=>QUIZ[li].find(r=>r[0]===q)[1]", [li, q])
        opts = await pg.locator(".opt").all_inner_texts()
        want_ok = n not in wrong_pos
        k = next(i for i, t in enumerate(opts) if (t == right) == want_ok)
        await pg.locator(".opt").nth(k).click(); await pg.click("#qzNext"); n += 1
    return n
async def menu_best(pg, li):
    return (await pg.locator("[data-q]").nth(li).inner_text()).replace("\n", " ")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1360,"height":650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE); await pg.wait_for_timeout(400)
        # QUIZ è privato nel gioco: lo si ricostruisce dal testo di index.html senza toccare il gioco
        import re
        src = pathlib.Path(BASE[7:]).read_text(encoding="utf-8")
        m = re.search(r"const QUIZ = \[.*?\n  \];", src, re.S); assert m, "QUIZ non trovato"
        await pg.evaluate("s=>{window.QUIZ=new Function(s+';return QUIZ')()}", m.group(0))
        li = 2
        N = await pg.evaluate("QUIZ[%d].length" % li)
        # 1) tutte giuste
        await pg.click(f"[data-q='{li}']"); await gira(pg, li, set())
        chk((await pg.inner_text(".qz .q")) == "Tutto giusto.", "tutte giuste: messaggio")
        chk(await pg.locator(".wq").count() == 0 and await pg.locator("#qzOnly").count() == 0, "tutte giuste: niente elenco né pulsante")
        await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        chk(f"migliore: {N} su {N}" in await menu_best(pg, li), "record = tutte giuste")
        # 2) un errore con record già pieno: non scende, elenco di 1
        await pg.click(f"[data-q='{li}']"); await gira(pg, li, {1})
        chk("Quasi tutto giusto: ecco la domanda sbagliata con la spiegazione." == await pg.inner_text(".qz .q"), "1 errore: messaggio")
        chk(await pg.locator(".wq").count() == 1, "1 errore: 1 domanda in elenco")
        expl = await pg.evaluate("(li)=>QUIZ[li][1][3]", li)
        chk(expl in await pg.inner_text(".wq"), "1 errore: c'è la spiegazione")
        await pg.screenshot(path=str(OUT / "Q_1errore.png"))
        await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        # 3) nuova lezione senza record: 4 errori -> record parziale; poi giro parziale NON cambia il record
        li = 0; N = await pg.evaluate("QUIZ[0].length")
        chk(N >= 4, "lezione 1 ha almeno 4 domande")
        sbagliate = {0, 1, 2, 3}
        await pg.click(f"[data-q='{li}']"); await gira(pg, li, sbagliate)
        chk("Conviene rifare la lezione" in await pg.inner_text(".qz .q") and "ecco le domande sbagliate" in await pg.inner_text(".qz .q"), "4 errori: messaggio")
        chk(await pg.locator(".wq").count() == 4, "4 errori: 4 in elenco")
        testi = [t for t in await pg.locator(".wq .wt").all_inner_texts()]
        await pg.screenshot(path=str(OUT / "Q_4errori.png"))
        # nessun pixel di eccesso: il riquadro sta nella finestra
        box = await pg.evaluate("(()=>{const r=document.getElementById('quiz').getBoundingClientRect();return [r.top,r.bottom,innerHeight,document.documentElement.scrollHeight]})()")
        chk(box[0] >= 0 and box[1] <= box[2], f"riquadro dentro la finestra {box}")
        # parziale: rispondo giusto a tutte -> 4 su 4, record invariato
        await pg.click("#qzOnly")
        proposte = []
        while not await pg.locator("#qzAgain").count():
            proposte.append(await pg.inner_text(".qz .q"))
            q = proposte[-1]; right = await pg.evaluate("([li,q])=>QUIZ[li].find(r=>r[0]===q)[1]", [li, q])
            opts = await pg.locator(".opt").all_inner_texts()
            await pg.locator(".opt").nth(opts.index(right)).click(); await pg.click("#qzNext")
        chk(sorted(proposte) == sorted(testi) and len(proposte) == 4, "giro parziale: esattamente le 4 sbagliate")
        chk((await pg.inner_text(".score")) == "4 su 4", "giro parziale: risultato del giro")
        await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        dopo_parz = await menu_best(pg, li)
        chk(f"migliore: {N-4} su {N}" in dopo_parz, f"record dopo giro parziale invariato ({dopo_parz})")
        # completo migliore: 1 errore -> record N-1
        await pg.click(f"[data-q='{li}']"); await gira(pg, li, {0}); await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        chk(f"migliore: {N-1} su {N}" in await menu_best(pg, li), "record dopo ripasso completo migliore")
        # "Rivedi la lezione"
        await pg.click(f"[data-q='{li}']"); await gira(pg, li, {0})
        await pg.click("#qzLesson"); await pg.wait_for_timeout(300)
        chk(not await pg.evaluate("document.getElementById('quiz').open"), "Rivedi la lezione chiude il ripasso")
        chk(not await pg.evaluate("document.getElementById('lesson').hidden"), "Rivedi la lezione apre la lezione")

        # 4) 0.19.5 — riquadro con i caratteri veri: ogni pulsante dentro il riquadro, riquadro dentro la finestra, elenco che scorre.
        await pg.evaluate("document.fonts.ready")
        car = await pg.evaluate("""() => ({
            "barlow 700": document.fonts.check('700 16px "Barlow Semi Condensed"'),
            "source serif 400": document.fonts.check('400 16px "Source Serif 4"'),
            "facce Barlow caricate": [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"),
            "facce Source Serif caricate": [...document.fonts].some(f => f.family.includes("Source Serif") && f.status === "loaded"),
        })""")
        print("caratteri del gioco caricati:", all(car.values()), car)
        if not all(car.values()):
            print("MISURA DEL RIQUADRO NON VALIDA: mancano i caratteri veri (Barlow, Source Serif); i pixel di eccesso non dicono niente.")
            print("ESITO: NON VALIDA"); sys.exit(1)
        eccesso = 0
        for H in (650, 768):
            await pg.set_viewport_size({"width": 1360, "height": H})
            for errori in (6, 1):
                lun = await pg.evaluate("QUIZ.map(q => q.length)")
                li = next(i for i, n in enumerate(lun) if n >= errori)
                await pg.click(f"[data-q='{li}']"); await gira(pg, li, set(range(errori)))
                await pg.wait_for_timeout(100)
                r = await pg.evaluate("""() => {
                    const d = document.getElementById('quiz').getBoundingClientRect(), W = document.getElementById('qzWrong');
                    const bt = [...document.querySelectorAll('#qzBody .row button')].map(b => ({t: b.textContent, b: b.getBoundingClientRect().bottom, r: b.getBoundingClientRect().right}));
                    return {top: d.top, bottom: d.bottom, right: d.right, H: innerHeight, W: innerWidth, sy: scrollY, bt,
                            scroll: W.scrollHeight > W.clientHeight, sh: W.scrollHeight, ch: W.clientHeight, pagina: document.documentElement.scrollHeight - innerHeight};
                }""")
                ecc = max([b["b"] - r["bottom"] for b in r["bt"]] + [r["bottom"] - r["H"], -r["top"], r["right"] - r["W"], r["pagina"]])
                eccesso = max(eccesso, ecc)
                tag = f"1360x{H}, {errori} errori"
                chk(len(r["bt"]) == (4 if errori else 2) and all(b["t"] for b in r["bt"]), f"{tag}: pulsanti trovati {len(r['bt'])}")
                chk(all(b["b"] <= r["bottom"] + 0.5 for b in r["bt"]), f"{tag}: bordo inferiore dei pulsanti oltre il riquadro ({[round(b['b'] - r['bottom'], 1) for b in r['bt']]})")
                chk(r["top"] >= 0 and r["bottom"] <= r["H"] + 0.5, f"{tag}: riquadro fuori dalla finestra ({r['top']:.0f}..{r['bottom']:.0f} su {r['H']})")
                chk(r["pagina"] <= 0, f"{tag}: la pagina dietro scorre di {r['pagina']} px")
                if errori == 6: chk(r["scroll"], f"{tag}: l'elenco dovrebbe scorrere (contenuto {r['sh']} px in {r['ch']})")
                print(f"  {tag}: riquadro {r['bottom']-r['top']:.0f} px su {r['H']}, elenco {r['sh']} in {r['ch']} px, eccesso {ecc:.1f} px")
                await pg.click("#qzClose"); await pg.wait_for_timeout(100)
        print(f"eccesso massimo: {eccesso:.1f} px (positivo = fuori)")
        chk(not errs, f"errori di pagina: {errs}")
        await b.close()
    print(f"casi verificati: {casi}")
    if casi < 35: fail.append("troppo pochi casi misurati")
    print("ESITO:", "FALLITO" if fail else "OK"); sys.exit(1 if fail else 0)
asyncio.run(main())
