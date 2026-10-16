# Collaudo della 0.24: esame in carriera, ripasso dopo un esame non superato, attestato (criteri E1-E6 di
# docs/PROPOSTA-ESAME-E-BREVETTO.md, §13, scritti prima del codice; decisione di Ale: il ripasso completo conta con qualsiasi punteggio).
# Pagina senza #collaudo, solo clic e tasti, come la carica un giocatore. Le risposte giuste si riconoscono leggendo le banche
# ESAME e QUIZ dal testo di index.html. I salvataggi di partenza si preparano in localStorage dalle regole scritte.
# Lo spazio vale solo con i caratteri veri (Barlow, Source Serif): senza, ESITO: NON VALIDA (uscita 1).
# Fallisce se una parte misura zero casi. Uso: python collaudo_carriera_esame.py
import asyncio, json, pathlib, re, sys
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent; OUT = QUI / "output"; OUT.mkdir(exist_ok=True)
INDEX = QUI.parent / "index.html"; BASE = INDEX.as_uri(); import sorgente; SRC = sorgente.testo()   # dalla 1.0.3: index.html più js/
BANDS = [list(map(int, b)) for b in re.findall(r"bands: \[(\d+), (\d+), (\d+)\]", SRC)]
BANCHE = re.search(r"const ESAME = \[.*?\n  \];", SRC, re.S).group(0) + "\n" + re.search(r"const QUIZ = \[.*?\n  \];", SRC, re.S).group(0)
CAR, LIB, MODO = "scuolaVelaCarriera.v1", "scuolaVelaSim.v1", "scuolaVelaModo"
MK = ["m0.2", "m1.2", "m2.2", "m3.3", "m4.4"]
NQ = []   # domande per ripasso, lette dalla banca QUIZ nella pagina (main)
fail = []; casi = {}
def chk(parte, c, m):
    casi[parte] = casi.get(parte, 0) + 1
    if not c: fail.append(m); print("FALLITO:", m, flush=True)

def carriera(regate=(("r0.2", 3), ("r1.2", 3)), esame=None):
    """meriti a posto come il giocatore A del §12 (12/8/4/6 = 30), salvo cambiare le regate"""
    p = {"done": {f"l{i}": True for i in range(6)}, "best": {MK[i]: BANDS[i][1] for i in range(5)}, "clean": {MK[0]: True, MK[1]: True},
         "quiz": {f"q{i}": NQ[i] for i in range(4)}}   # quattro ripassi tutti giusti: 8 punti
    p["race"] = {f"{k}:principianti": {"pos": pos, "n": 4, "pulita": False} for k, pos in regate}
    if esame: p["exam"] = esame
    return p

async def pagina(b, salv=None, modo="carriera"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE)
    await pg.evaluate("([d, m]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }", [json.dumps(salv) if salv else None, modo])
    await pg.reload(); await pg.wait_for_timeout(300)
    await pg.evaluate("s => { window.__B = new Function(s + ';return { ESAME, QUIZ }')(); }", BANCHE)
    return ctx, pg, errs

async def esame(pg, sbaglia=lambda li: False, ferma=None):
    """risponde all'esame; sbaglia(li) dice se sbagliare le domande della lezione li. Ritorna (voto atteso, lezioni sbagliate)."""
    await pg.click("#goEsame"); k = voto = 0; sb = set()
    while not await pg.locator("#qzBody .score").count():
        if ferma is not None and k == ferma: await pg.keyboard.press("Escape"); await pg.wait_for_timeout(150); return None, None
        q = await pg.inner_text(".qz .q")
        li, giusta = await pg.evaluate("q => { for (let i = 0; i < __B.ESAME.length; i++) for (const r of __B.ESAME[i]) if (r[1] === q) return [i, r[2]]; }", q)
        opts = await pg.locator(".opt").all_inner_texts(); s = sbaglia(li)
        await pg.locator(".opt").nth(next(j for j, t in enumerate(opts) if (t == giusta) != s)).click()
        if s: sb.add(li)
        else: voto += 1
        await pg.click("#qzNext"); k += 1
    return voto, sorted(sb)

async def ripasso(pg, li, sbagliate=0, ferma=None):
    await pg.click(f"[data-q='{li}']"); n = 0
    while not await pg.locator("#qzAgain").count():
        if ferma is not None and n == ferma: await pg.keyboard.press("Escape"); await pg.wait_for_timeout(150); return
        q = await pg.inner_text(".qz .q"); giusta = await pg.evaluate("([li, q]) => __B.QUIZ[li].find(r => r[0] === q)[1]", [li, q])
        opts = await pg.locator(".opt").all_inner_texts()
        await pg.locator(".opt").nth(next(j for j, t in enumerate(opts) if (t == giusta) != (n < sbagliate))).click(); await pg.click("#qzNext"); n += 1
    await pg.click("#qzClose"); await pg.wait_for_timeout(150)

async def salvato(pg): return json.loads(await pg.evaluate(f"localStorage.getItem('{CAR}') || 'null'"))
async def aperto(pg, id_): return await pg.evaluate(f"document.getElementById('{id_}').open")
async def chiudi_quiz(pg): await pg.click("#qzClose"); await pg.wait_for_timeout(200)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        q0 = await b.new_page(); await q0.goto(BASE)
        NQ.extend(await q0.evaluate("s => new Function(s + ';return QUIZ')().map(q => q.length)", BANCHE)); await q0.close()
        print("domande dei ripassi:", NQ)
        # ---- E1: carriera vuota, esame tutto giusto
        ctx, pg, errs = await pagina(b)
        chk("E1", await pg.is_enabled("#goEsame"), "E1: pulsante dell'esame acceso con la carriera vuota")
        voto, _ = await esame(pg)
        chk("E1", voto == 20 and "20 su 20: superato" in await pg.inner_text("#qzBody .score"), f"E1: voto {voto}")
        chk("E1", await pg.locator("#qzAgain").count() == 0, "E1: in carriera niente «Rifai l'esame»")
        p = await salvato(pg)
        chk("E1", p["exam"]["superato"] is True and p["exam"]["voto"] == 20 and re.fullmatch(r"\d{4}-\d\d-\d\d", p["exam"]["data"]), f"E1: salvato {p.get('exam')}")
        await chiudi_quiz(pg)
        chk("E1", not await aperto(pg, "attest") and "brevetto" not in await salvato(pg), "E1: nessun attestato senza i meriti")
        chk("E1", not await pg.is_enabled("#goEsame") and "Esame superato" in await pg.inner_text("#goEsame") and "20 su 20" in await pg.inner_text("#goEsame"), f"E1: pulsante «{await pg.inner_text('#goEsame')}»")
        chk("E1", "esame" not in (await pg.inner_text("#libManca")).lower(), f"E1: libretto «{await pg.inner_text('#libManca')}»")
        chk("E1", not errs, f"E1: errori {errs}"); await ctx.close()

        # ---- E2: meriti a posto, esame non superato (sbagliate tutte le domande delle lezioni 1 e 3), ripassi, poi superato
        ctx, pg, errs = await pagina(b, carriera())
        voto, sb = await esame(pg, lambda li: li in (0, 2))
        chk("E2", voto == 12 and sb == [0, 2] and "non superato" in await pg.inner_text("#qzBody .score"), f"E2: voto {voto}, lezioni sbagliate {sb}")
        p = await salvato(pg)
        chk("E2", p["exam"]["superato"] is False and p["exam"]["ripasso"] == sb and p["exam"]["voto"] == 12, f"E2: salvato {p.get('exam')}")
        chk("E2", await pg.locator("#qzAgain").count() == 0 and [await x.inner_text() for x in await pg.locator("[data-rq]").all()] == ["Ripasso 1", "Ripasso 3"], "E2: pulsanti dei ripassi nell'esito")
        await chiudi_quiz(pg)
        chk("E2", not await pg.is_enabled("#goEsame") and "ripassi 1 e 3" in await pg.inner_text("#goEsame"), f"E2: pulsante «{await pg.inner_text('#goEsame')}»")
        chk("E2", "Ti manca l'esame." == await pg.inner_text("#libManca") and (await pg.inner_text("#libSug")).split(": ", 1)[1] in ("Ripasso 1, La barca e il vento (dopo l'esame).", "Ripasso 3, Andature e filetti (dopo l'esame)."), f"E2: libretto «{await pg.inner_text('#libSug')}»")
        await ripasso(pg, 0, ferma=2)   # lasciato a metà: non conta
        chk("E2", (await salvato(pg))["exam"]["ripasso"] == [0, 2] and not await pg.is_enabled("#goEsame"), "E2: ripasso lasciato a metà non conta")
        await ripasso(pg, 0, sbagliate=3)   # completo, con 3 errori: conta (qualsiasi punteggio)
        chk("E2", (await salvato(pg))["exam"]["ripasso"] == [2] and not await pg.is_enabled("#goEsame"), f"E2: dopo il ripasso della lezione 1 {(await salvato(pg))['exam']}")
        await ripasso(pg, 2)
        chk("E2", (await salvato(pg))["exam"]["ripasso"] == [] and await pg.is_enabled("#goEsame"), "E2: dopo i due ripassi l'esame si riapre")
        voto, _ = await esame(pg, lambda li: li == 5)   # 3 sbagliate: 17 su 20
        chk("E2", voto == 17 and (await salvato(pg))["exam"]["superato"] is True, f"E2: secondo esame {voto}")
        await chiudi_quiz(pg)
        chk("E2", await aperto(pg, "attest"), "E2: la scena dell'attestato compare tornando al menu")
        att = await pg.inner_text("#atBody"); tit = (await pg.inner_text("#atTitle")) + " " + await pg.inner_text("#atBody .sc") + " " + await pg.inner_text("#atBody .ruolo")
        chk("E2", "Nessun valore legale" in att and "17 su 20" in att and "Timoniere di deriva" in att, f"E2: testo dell'attestato {att!r}")
        chk("E2", "patent" not in tit.lower(), f"E2: «patente» nel titolo: {tit!r}")
        await pg.screenshot(path=str(OUT / "C_attestato.png"))
        # ---- E3: nome, chiudi, riapri dal libretto, ricarica; stampa
        await pg.fill("#atName", "Ale"); await pg.click("#atClose")
        chk("E3", not await aperto(pg, "attest") and "Brevetto ottenuto il" in await pg.inner_text("#libManca"), "E3: libretto con il brevetto")
        await pg.click("#goAttest")
        chk("E3", await aperto(pg, "attest") and await pg.input_value("#atName") == "Ale", "E3: il nome resta riaprendo dal libretto")
        r = await pg.evaluate("() => { const d = document.getElementById('attest').getBoundingClientRect(); return [d.top, d.bottom, innerHeight]; }")
        chk("spazio", r[0] >= 0 and r[1] <= r[2], f"spazio: attestato a 1360x650 da {r[0]:.0f} a {r[1]:.0f} su {r[2]}")
        await pg.emulate_media(media="print")
        st = await pg.evaluate("() => [getComputedStyle(document.getElementById('menu')).display, getComputedStyle(document.querySelector('#atBody .row')).display, getComputedStyle(document.getElementById('attest')).display]")
        chk("E3", st[0] == "none" and st[1] == "none" and st[2] != "none", f"E3: in stampa menu {st[0]}, pulsanti {st[1]}, attestato {st[2]}")
        await pg.screenshot(path=str(OUT / "C_attestato_stampa.png")); await pg.emulate_media(media="screen")
        await pg.click("#atClose"); await pg.reload(); await pg.wait_for_timeout(300)
        chk("E3", not await aperto(pg, "attest") and (await salvato(pg))["brevetto"]["nome"] == "Ale", "E3: ricaricando l'attestato non ricompare da solo e il nome resta")
        menu_h = await pg.evaluate("() => [document.documentElement.scrollHeight - innerHeight, document.querySelector('.menu-foot').getBoundingClientRect().bottom]")
        chk("spazio", menu_h[0] <= 0, f"spazio: menu con il brevetto, eccesso {menu_h[0]} px, piede a {menu_h[1]:.0f}")
        car = await pg.evaluate("""() => [document.fonts.check('700 16px "Barlow Semi Condensed"'), [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"), [...document.fonts].some(f => f.family.includes("Source Serif") && f.status === "loaded")]""")
        print(f"spazio: attestato da {r[0]:.0f} a {r[1]:.0f} px su {r[2]}; menu con il brevetto, piede a {menu_h[1]:.0f}; caratteri veri {all(car)}")
        chk("E2", not errs, f"E2-E3: errori {errs}"); await ctx.close()

        # ---- E4: l'ultima condizione è una regata (esame già superato); la scena compare una volta sola
        p = carriera(regate=(("r0.2", 3),), esame={"superato": True, "voto": 18, "data": "2026-10-14"})
        ctx, pg, errs = await pagina(b, p)
        chk("E4", not await aperto(pg, "attest") and "Competizione" in await pg.inner_text("#libManca"), "E4: manca Competizione, niente attestato")
        p["race"]["r1.2:principianti"] = {"pos": 2, "n": 4, "pulita": False}   # il piazzamento che mancava, come lo scrive il gioco
        await pg.evaluate("d => localStorage.setItem('scuolaVelaCarriera.v1', d)", json.dumps(p)); await pg.reload(); await pg.wait_for_timeout(300)
        chk("E4", await aperto(pg, "attest") and "18 su 20" in await pg.inner_text("#atBody"), "E4: la scena compare con l'ultimo merito")
        await pg.click("#atClose")
        for _ in range(2): await pg.click("#modoSel button[data-v='libero']"); await pg.click("#modoSel button[data-v='carriera']")
        chk("E4", not await aperto(pg, "attest"), "E4: tornando al menu la scena non ricompare")
        chk("E4", not errs, f"E4: errori {errs}"); await ctx.close()

        # ---- E5: gioco libero, esame superato: niente si salva, «Rifai l'esame» c'è, nessun attestato
        ctx, pg, errs = await pagina(b, None, "libero")
        await pg.evaluate("() => localStorage.setItem('scuolaVelaSim.v1', JSON.stringify({done:{l0:true},best:{},clean:{}}))"); await pg.reload(); await pg.wait_for_timeout(300)
        await pg.evaluate("s => { window.__B = new Function(s + ';return { ESAME, QUIZ }')(); }", BANCHE)
        prima = await pg.evaluate("JSON.stringify(Object.entries(localStorage).sort())")
        voto, _ = await esame(pg)
        chk("E5", voto == 20 and await pg.locator("#qzAgain").count() == 1, "E5: «Rifai l'esame» nel gioco libero")
        await chiudi_quiz(pg)
        chk("E5", await pg.evaluate("JSON.stringify(Object.entries(localStorage).sort())") == prima and not await aperto(pg, "attest") and await pg.is_enabled("#goEsame"), "E5: niente salvato, niente attestato, pulsante acceso")
        chk("E5", not errs, f"E5: errori {errs}"); await ctx.close()

        # ---- E6: carriera, esame lasciato a metà: niente si salva
        ctx, pg, errs = await pagina(b, carriera())
        prima = await pg.evaluate(f"localStorage.getItem('{CAR}')")
        await esame(pg, ferma=5)
        chk("E6", await pg.evaluate(f"localStorage.getItem('{CAR}')") == prima and await pg.is_enabled("#goEsame"), "E6: esame lasciato a metà, niente salvato")
        chk("E6", not errs, f"E6: errori {errs}"); await ctx.close()
        await b.close()
    print("casi per parte:", casi)
    if fail: print("ESITO: FALLITO"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("E1", "E2", "E3", "E4", "E5", "E6", "spazio")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    if not all(car): print("MISURA DELLO SPAZIO NON VALIDA: mancano i caratteri veri (Barlow, Source Serif); il resto è OK."); print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
