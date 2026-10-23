# Collaudo della 0.22: bivio gioco libero / carriera, salvataggi e fantasmi separati (criteri K1-K5 di
# docs/PROPOSTA-ESAME-E-BREVETTO.md, §11, scritti prima del codice). La modalità si cambia sempre cliccando il selettore.
# K1 (con #collaudo): il pilota di collaudo_fasce.py, letto dal suo file, completa la prova 1 in una modalità;
#    l'altra modalità deve restare identica byte per byte. Vale solo se la modalità in uso è cambiata davvero.
# K2-K5 (senza #collaudo, come la carica un giocatore): ripasso, modalità ricordata, «Azzera», primo avvio.
# Fallisce se misura zero casi. Uso: python collaudo_carriera.py
import asyncio, json, pathlib, re, subprocess, sys, tempfile
import sorgente   # dalla 1.0.3 il codice è in index.html più js/
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent
INDEX = QUI.parent / "index.html"; BASE = INDEX.as_uri()
fasce = (QUI / "collaudo_fasce.py").read_text(encoding="utf-8")
SEME = re.search(r'SEME = """(.*?)"""', fasce, re.S).group(1)
CORSA = re.search(r'CORSA = """(.*?)"""', fasce, re.S).group(1)
LIB, CAR, GLIB, GCAR, MODO = "scuolaVelaSim.v1", "scuolaVelaCarriera.v1", "scuolaVelaGhost.v1", "scuolaVelaGhostCarriera.v1", "scuolaVelaModo"
fail = []; casi = 0; nonvalide = 0
def chk(c, m):
    global casi; casi += 1
    if not c: fail.append(m); print("FALLITO:", m, flush=True)

LEGGI = "() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))"
async def scrivi(pg, d): await pg.evaluate("d => { localStorage.clear(); for (const k in d) localStorage.setItem(k, d[k]); }", d)
async def modo(pg): return await pg.get_attribute("#modoSel button[aria-pressed='true']", "data-v")
async def scegli(pg, m): await pg.click(f"#modoSel button[data-v='{m}']"); await pg.wait_for_timeout(100)
def finto(best, quiz=None):   # salvataggio preparato, scritto come lo scriverebbe il gioco
    p = {"done": {"m0": True}, "best": {"m0.4": best}, "clean": {}}
    if quiz is not None: p["quiz"] = {"q0": quiz}
    return json.dumps(p)
FANT = json.dumps({"m0.4": [[0, 1, 2, 3]] * 8})

async def k1(b):
    for verso, (attiva, altra) in (("carriera", (CAR, LIB)), ("libero", (LIB, CAR))):
        ga, go = (GCAR, GLIB) if verso == "carriera" else (GLIB, GCAR)
        for seme in (1, 2, 3):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(SEME); await pg.goto(BASE + "#collaudo")
            pre = {altra: finto(999), go: FANT}
            if verso == "libero": pre[MODO] = "carriera"
            await scrivi(pg, pre); await pg.reload(); await pg.wait_for_timeout(300)
            chk(await modo(pg) == ("carriera" if verso == "libero" else "libero"), f"K1 {verso} seme {seme}: si parte nella modalità preparata")
            await scegli(pg, verso)
            chk(await modo(pg) == verso, f"K1 {verso} seme {seme}: selettore su {verso}")
            prima = await pg.evaluate(LEGGI)
            await pg.evaluate(f"__seed({seme})"); await pg.evaluate("__sv.openItem(['m',0])"); await pg.evaluate(f"__sv.startMission(0, {(seme - 1) * 45})")
            fin, t, _ = await pg.evaluate(CORSA, [])
            dopo = await pg.evaluate(LEGGI); await ctx.close()
            if not fin or dopo.get(attiva) == prima.get(attiva):
                global nonvalide; nonvalide += 1; print(f"K1 {verso} seme {seme}: NON VALIDA (finita {fin}, chiave in uso cambiata: {dopo.get(attiva) != prima.get(attiva)})"); continue
            p = json.loads(dopo[attiva]); g = json.loads(dopo.get(ga, "{}"))
            ok_altra = dopo.get(altra) == prima.get(altra) and dopo.get(go) == prima.get(go)
            chk(ok_altra, f"K1 {verso} seme {seme}: l'altra modalità (salvataggio e fantasmi) identica byte per byte")
            chk(p["done"].get("m0") is True and isinstance(p["best"].get("m0.4"), (int, float)), f"K1 {verso} seme {seme}: record della prova 1 nella modalità in uso")
            chk("m0.4" in g and g["m0.4"] != json.loads(FANT)["m0.4"], f"K1 {verso} seme {seme}: fantasma nuovo nella modalità in uso")
            chk(not errs, f"K1 {verso} seme {seme}: errori nella pagina {errs[:1]}")
            print(f"K1 {verso} seme {seme}: prova 1 in {t:.1f} s, record {p['best'].get('m0.4')}, altra identica {ok_altra}", flush=True)

QUIZ_JS = None
async def ripasso_tutto_giusto(pg):
    await pg.evaluate("s=>{window.QUIZ=new Function(s+';return QUIZ')()}", QUIZ_JS)
    await pg.click("[data-q='0']"); n = 0
    while not await pg.locator("#qzAgain").count():
        q = await pg.inner_text(".qz .q"); giusta = await pg.evaluate("q=>QUIZ[0].find(r=>r[0]===q)[1]", q)
        opts = await pg.locator(".opt").all_inner_texts()
        await pg.locator(".opt").nth(opts.index(giusta)).click(); await pg.click("#qzNext"); n += 1
    await pg.click("#qzClose"); await pg.wait_for_timeout(100)
    return n

async def k2_k4(b):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); dialoghi = []
    pg.on("dialog", lambda d: (dialoghi.append(d.message), asyncio.ensure_future(d.accept())))
    await pg.goto(BASE); await scrivi(pg, {LIB: finto(500, quiz=3), GLIB: FANT}); await pg.reload(); await pg.wait_for_timeout(300)
    chk(await pg.evaluate("typeof window.__sv") == "undefined", "senza #collaudo __sv non esiste")
    # K2
    prima = await pg.evaluate(LEGGI)
    await scegli(pg, "carriera"); n = await ripasso_tutto_giusto(pg)
    dopo = await pg.evaluate(LEGGI)
    chk(dopo.get(LIB) == prima[LIB] and dopo.get(GLIB) == prima[GLIB], "K2: il ripasso in carriera non tocca il gioco libero (byte per byte)")
    chk(json.loads(dopo.get(CAR, "{}")).get("quiz", {}).get("q0") == n, f"K2: ripasso scritto in carriera ({n} su {n})")
    chk(f"migliore: {n} su {n}" in await pg.locator("[data-q='0']").inner_text(), "K2: il menu della carriera mostra il ripasso")
    chk(dopo.get(MODO) == "carriera", "K2: modalità salvata")
    # K3
    await pg.reload(); await pg.wait_for_timeout(300)
    chk(await modo(pg) == "carriera" and f"migliore: {n} su {n}" in await pg.locator("[data-q='0']").inner_text(), "K3: ricaricando resta la carriera, con i suoi dati")
    await scegli(pg, "libero"); await pg.reload(); await pg.wait_for_timeout(300)
    chk(await modo(pg) == "libero" and "migliore: 3 su" in await pg.locator("[data-q='0']").inner_text(), "K3: ricaricando resta il gioco libero, con i suoi dati")
    # K4: dati in tutte e due, poi «Azzera» in carriera e in libero
    for m, (mia, mg), (altra, ag) in (("carriera", (CAR, GCAR), (LIB, GLIB)), ("libero", (LIB, GLIB), (CAR, GCAR))):
        await scrivi(pg, {LIB: finto(500, quiz=3), GLIB: FANT, CAR: finto(400, quiz=5), GCAR: FANT, MODO: m}); await pg.reload(); await pg.wait_for_timeout(300)
        chk(await modo(pg) == m, f"K4 {m}: modalità preparata")
        prima = await pg.evaluate(LEGGI); dialoghi.clear()
        await pg.click("#resetProg"); await pg.wait_for_timeout(200)
        dopo = await pg.evaluate(LEGGI)
        chk(len(dialoghi) == 1 and ("della carriera" if m == "carriera" else "del gioco libero") in dialoghi[0], f"K4 {m}: la conferma nomina la modalità ({dialoghi[:1]})")
        chk(json.loads(dopo[mia]) == {"done": {}, "best": {}, "clean": {}} and dopo.get(mg) == "{}", f"K4 {m}: progressi e fantasmi azzerati")
        chk(dopo[mia] != prima[mia], f"K4 {m}: il salvataggio in uso è cambiato davvero")
        chk(dopo.get(altra) == prima[altra] and dopo.get(ag) == prima[ag], f"K4 {m}: l'altra modalità identica byte per byte")
    chk(not errs, f"K2-K4: errori nella pagina {errs[:1]}")
    await ctx.close()

async def k5(b):
    vecchio = pathlib.Path(tempfile.mkdtemp()) / "index.html"
    # Riferimento: la 1.0.1 (8da0d7c). Dalla 1.0.2 il menu cambia in due punti voluti, che si portano al testo nuovo prima del confronto:
    # i ripassi si chiamano «Ripasso N · titolo» (osservazione 44) e il piede parla di medaglie (osservazione 46).
    # Dalla 1.0.20 il ripasso 5 ha 6 domande invece di 5 (gli è passata la domanda sulla barra all'indietro dal ripasso 2, CHANGELOG 1.0.20).
    vecchio.write_bytes(subprocess.run(["git", "show", "8da0d7c:index.html"], cwd=QUI.parent, capture_output=True, check=True).stdout)
    testi = []
    for url in (BASE, vecchio.as_uri()):
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page()
        await pg.goto(url); await pg.wait_for_timeout(300)
        tiles, foot = await pg.inner_text(".tiles"), await pg.inner_text(".menu-foot")
        if url == BASE: tiles = re.sub(r"⚑\nRegata nei salti di vento\nDa fare\n+[^\n]*\n", "", tiles)  # 1.0.28: riquadro voluto del livello 2, nel menu del gioco libero
        if url == BASE: tiles = tiles.replace("Andature, mure e precedenze", "Andature e filetti").replace("le mure e chi lascia strada;", "le mure;")  # 1.0.37: titolo e descrizione della lezione 3, voluti
        if url == BASE: tiles = re.sub(r"Tornei\n⚑\nTorneo dell'1b\nDa fare\n", "", tiles).replace("Altri tipi di barca.", "I tornei, altri tipi di barca.")  # 1.0.34: torneo dell'1b, voluto
        if url != BASE:
            tiles = re.sub(r"Lezione (\d): ", r"Ripasso \1 · ", tiles)
            tiles = tiles.replace("Ripasso 5 · Virata e strambata\n5 domande", "Ripasso 5 · Virata e strambata\n6 domande")
            foot = foot.replace("I pallini oro, argento e bronzo indicano la fascia del tuo record.", "Il pallino oro, argento o bronzo è la medaglia del tuo tempo migliore.")
        testi.append([tiles, foot])
        if url == BASE:
            chk(await modo(pg) == "libero", "K5: senza chiavi si parte in gioco libero")
            chk(MODO not in await pg.evaluate(LEGGI), "K5: aprire il menu non scrive la modalità")
        await ctx.close()
    chk(testi[0] == testi[1], "K5: riquadri e piede del menu uguali alla 1.0.1 (salvo i due testi voluti della 1.0.2, il ripasso 5 con 6 domande della 1.0.20 e i riquadri voluti della 1.0.28, 1.0.34 e 1.0.37)")

async def main():
    global QUIZ_JS
    QUIZ_JS = re.search(r"const QUIZ = \[.*?\n  \];", sorgente.testo(), re.S).group(0)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await k1(b); await k2_k4(b); await k5(b)
        await b.close()
    print(f"controlli: {casi}, falliti: {len(fail)}, corse K1 non valide: {nonvalide} su 6")
    if casi == 0 or nonvalide: print("MISURA NON VALIDA"); sys.exit(1)
    print("ESITO", "OK" if not fail else "FALLITO"); sys.exit(1 if fail else 0)
asyncio.run(main())
