# Collaudi nel browser del prototipo del fiocco (tappa A).
# Tasti: barra con le frecce, randa con A e D (o le frecce su e giù), fiocco con Q ed E, anche premuti insieme.
# Criterio 6: i filetti del fiocco rispondono alla sua scotta come quelli della randa.
# Criterio 8: la barca si guida davvero — giro della prova 1 col pilota automatico e virata di bolina.
# Uso: python collaudo_fiocco.py
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent
OUT = QUI / "output"; OUT.mkdir(exist_ok=True)
PROTO = (QUI / "fiocco.html").as_uri() + "#collaudo"
GIOCO = (QUI.parent / "index.html").as_uri() + "#collaudo"

# Pilota automatico: lo stesso di tests/collaudo_giro_boa.py, con una riga in più per la scotta del fiocco.
PILOTA = """
(cfg) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  const pts = [];
  for (const [k, angs] of cfg.plan) {
    const m = sv.marks[k];
    for (const a of angs) { const b = (m.out + a) * D; pts.push({ x: m.x + Math.sin(b) * 13, y: m.y - Math.cos(b) * 13 }); }
  }
  const last = sv.marks[sv.marks.length - 1]; pts.push({ x: last.x, y: last.y });
  let i = 0, side = 1;
  window.__pil = setInterval(() => {
    const S = sv.S; if (S.finished || i >= pts.length){ window.__pilDone = (window.__pilDone || 0) + 1; return; }
    const p = pts[i]; if (Math.hypot(p.x - S.x, p.y - S.y) < 7) { i++; return; }
    const brg = Math.atan2(p.x - S.x, -(p.y - S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg;
    if (Math.abs(rel) < 52) { if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; }
    const cur = n180(S.h - sv.twd);
    if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
    const err = n180(S.h - want);
    sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
    sv.ctl.sheet = Math.abs(cur) > 150 ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet();
    if (cfg.jib !== null) sv.ctl.jib = cfg.jib === "auto" ? sv.autoJib() : cfg.jib;   // FIOCCO
    if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" }));
  }, 25);
  window.__pilDone = 0;
}
"""

async def giro(pg, idx, jib, nome):
    # piano vuoto: la boa si raggiunge soltanto, come fa il caso «prove 1-3» di tests/collaudo_giro_boa.py
    await pg.evaluate(f"__sv.startMission({idx}, 0)")      # vento da nord: coordinate semplici
    await pg.evaluate("__sv.fast(8)")
    await pg.evaluate(PILOTA, {"plan": [], "jib": jib})
    for _ in range(90):
        await pg.wait_for_timeout(1000)
        if await pg.evaluate("__sv.S.finished || window.__pilDone > 80"): break
    r = await pg.evaluate("[__sv.S.finished, Math.round(__sv.S.time), __sv.S.capsizes, __sv.S.tacks, __sv.S.gybesV]")
    await pg.evaluate("clearInterval(window.__pil); __sv.fast(1)")
    print(f"  prova {idx+1} — {nome}: finita={r[0]} tempo={r[1]} s scuffie={r[2]} virate={r[3]} strambate a vela aperta={r[4]}")
    return r

# Tutta la virata dentro una sola chiamata: fuori da qui girerebbe anche il ciclo del browser
# e il tempo misurato non sarebbe quello della simulazione (avvertenza di COLLAUDI.md).
VIRATA = """
(j) => {
  const S = __sv.S, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  S.x = 0; S.y = 0; S.h = 45; S.u = 4 / 1.943844; S.vl = 0; S.r = 0; S.heel = 0; S.heelRate = 0; S.hike = 0.3;
  __sv.ctl.sheet = 0.05; __sv.ctl.tiller = 0; if (j !== null) __sv.ctl.jib = j;
  __sv.run(1 / 240, 480);                                  // 2 s di assestamento
  const kn0 = S.u * 1.943844;
  for (let k = 1; k <= 2880; k++){                          // fino a 12 s
    __sv.ctl.tiller = 0.8;   // ogni passo: simulate() richiama applyInput, che riporta la barra al centro da sola
    __sv.run(1 / 240, 1);
    if (n180(S.h) < -44) return { ok: true, t: k / 240, kn0 };
  }
  return { ok: false, h: Math.round(n180(S.h)), kn: +(S.u * 1.943844).toFixed(1), kn0 };
}
"""

async def virata(pg, jib, nome):
    await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(200)
    # senza raffiche: in navigazione libera sono accese, e spostavano il tempo della virata di circa un secondo fra una corsa e l'altra
    await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#gustSel", "0"])
    await pg.wait_for_timeout(200)
    r = await pg.evaluate(VIRATA, jib)
    print(f"  {nome}: partita a {r['kn0']:.1f} nodi, " +
          (f"virata riuscita in {r['t']:.1f} s" if r["ok"] else f"NON virata (prua a {r['h']}°, {r['kn']} nodi)"))
    return r["ok"]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 800}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(PROTO); await pg.wait_for_timeout(400)

        # ---- i tasti, premuti davvero sulla tastiera ----
        print("=== TASTI (navigazione libera, premuti davvero) ===")
        await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(300)
        errori_tasti = []
        async def premi(tasti, atteso, nome):
            # si parte sempre dal centro, con le due scotte a metà, così c'è spazio in entrambi i versi
            await pg.evaluate("() => { __sv.ctl.tiller = 0; __sv.ctl.sheet = 0.5; __sv.ctl.jib = 0.5; }")
            for t in tasti: await pg.keyboard.down(t)
            await pg.wait_for_timeout(500)
            dopo = await pg.evaluate("[__sv.ctl.tiller, __sv.ctl.sheet, __sv.ctl.jib]")
            for t in tasti: await pg.keyboard.up(t)
            await pg.wait_for_timeout(100)
            verso = lambda v, p: "fermo" if abs(v - p) < 1e-6 else ("giù" if v < p else "su")
            got = (verso(dopo[0], 0), verso(dopo[1], 0.5), verso(dopo[2], 0.5))
            ok = got == atteso
            print(f"  {nome:34s} {'+'.join(tasti):22s} barra {got[0]:5s} randa {got[1]:5s} fiocco {got[2]:5s}  {'ok' if ok else 'ATTESO ' + str(atteso)}")
            if not ok: errori_tasti.append(f"{nome}: {got}, atteso {atteso}")
        #                                      barra   randa   fiocco
        await premi(["ArrowLeft"],  ("giù",   "fermo", "fermo"), "barra a sinistra")
        await premi(["ArrowRight"], ("su",    "fermo", "fermo"), "barra a dritta")
        await premi(["d"],          ("fermo", "giù",   "fermo"), "D cazza la randa")
        await premi(["a"],          ("fermo", "su",    "fermo"), "A lasca la randa")
        await premi(["ArrowUp"],    ("fermo", "giù",   "fermo"), "freccia su cazza la randa")
        await premi(["ArrowDown"],  ("fermo", "su",    "fermo"), "freccia giù lasca la randa")
        await premi(["e"],          ("fermo", "fermo", "giù"),   "E cazza il fiocco")
        await premi(["q"],          ("fermo", "fermo", "su"),    "Q lasca il fiocco")
        await premi(["ArrowLeft", "d", "e"], ("giù", "giù", "giù"), "barra+randa+fiocco insieme")
        await premi(["ArrowRight", "a", "q"], ("su", "su", "su"), "gli stessi nell'altro verso")
        await premi(["d", "q"],     ("fermo", "giù",   "su"),    "randa e fiocco in versi opposti")
        # ↑ e D insieme non devono cazzare il doppio: stessa condizione, non due righe
        await pg.evaluate("() => { __sv.ctl.tiller = 0; __sv.ctl.sheet = 0.9; __sv.ctl.jib = 0.5; }")
        await pg.keyboard.down("d"); await pg.wait_for_timeout(600); await pg.keyboard.up("d")
        solo = 0.9 - await pg.evaluate("__sv.ctl.sheet")
        await pg.evaluate("() => { __sv.ctl.sheet = 0.9; }")
        await pg.keyboard.down("d"); await pg.keyboard.down("ArrowUp"); await pg.wait_for_timeout(600)
        await pg.keyboard.up("d"); await pg.keyboard.up("ArrowUp")
        insieme = 0.9 - await pg.evaluate("__sv.ctl.sheet")
        doppio = insieme > solo * 1.5
        print(f"  D da solo cazza {solo:.3f}, D+freccia su cazzano {insieme:.3f}: doppia velocità? {doppio}")
        if doppio: errori_tasti.append("D e freccia su insieme cazzano il doppio")
        # la barra torna al centro quando si lascia il tasto
        await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(400); await pg.keyboard.up("ArrowLeft")
        t1 = await pg.evaluate("__sv.ctl.tiller"); await pg.wait_for_timeout(1200)
        t2 = await pg.evaluate("__sv.ctl.tiller")
        print(f"  barra lasciata: da {t1:.2f} a {t2:.2f} (torna al centro da sola)")
        if not (abs(t2) < abs(t1)): errori_tasti.append("la barra non torna al centro")
        print("  esito tasti:", "tutti come attesi" if not errori_tasti else errori_tasti)

        # ---- criterio 6: filetti del fiocco ----
        print("=== 6. FILETTI DEL FIOCCO (10 nodi da nord, navigazione libera) ===")
        await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(300)
        casi, errori6 = [], []
        for twa in [20, 60, 90, 135]:
            for nome, jb in [("tutta lascata", 1.0), ("regolata", None), ("tutta cazzata", 0.0)]:
                await pg.evaluate("""a => { const S = __sv.S;
                    S.x = 0; S.y = 0; S.h = a[0]; S.u = 3 / 1.943844; S.vl = 0; S.r = 0; S.heel = 0; S.heelRate = 0;
                    __sv.ctl.tiller = 0; __sv.ctl.sheet = __sv.autoSheet();
                    __sv.ctl.jib = a[1] === null ? __sv.autoJib() : a[1]; }""", [twa, jb])
                await pg.evaluate("__sv.run(1/240, 240)")   # 1 s a prua libera: si assesta senza girare molto
                r = await pg.evaluate("[__sv.ttJib, __sv.tt, Math.round(__sv.info.alphaJ), Math.round(__sv.info.jib), Math.round(Math.abs(__sv.info.awa))]")
                await pg.wait_for_timeout(200)              # il pannello si aggiorna nel ciclo del browser, non in run()
                pannello = await pg.inner_text("#vJib")
                casi.append((twa, nome, r[0], r[1], r[2], r[3], r[4], pannello))
                print(f"  {twa:3d}° {nome:14s}: fiocco {r[0]:4s} (incidenza {r[2]:3d}°, angolo {r[3]:2d}°, vento app. {r[4]:3d}°) | randa {r[1]:4s} | pannello: «{pannello}»")
        # attese: nell'angolo morto sbatte comunque; altrove lascata = sopravento, cazzata = sottovento, regolata = dritti
        for twa, nome, tj, tm, aj, ang, awa, pan in casi:
            # dalla tappa B, alle andature larghe il fiocco è coperto dalla randa: i filetti dicono «sbatte», non stallo
            atteso = "flog" if twa in (20, 135) else {"tutta lascata": "wind", "regolata": "ok", "tutta cazzata": "lee"}[nome]
            if tj != atteso: errori6.append(f"{twa}° {nome}: filetti {tj}, attesi {atteso}")
        print("  esito criterio 6:", "tutti come attesi" if not errori6 else errori6)

        # ---- criterio 8: guidare davvero ----
        print("\n=== 8. GUIDANDO DAVVERO LA BARCA ===")
        print(" prove 1, 2 e 3 col pilota automatico (la 3 è tutta di bolina, con virate):")
        pg2 = await b.new_page(viewport={"width": 1280, "height": 800})
        pg2.on("pageerror", lambda e: errs.append(str(e)))
        await pg2.goto(GIOCO); await pg2.wait_for_timeout(400)
        fatte = []
        for idx in (0, 1, 2):
            fatte.append(("gioco", await giro(pg2, idx, None, "gioco, senza fiocco")))
            fatte.append(("fisso", await giro(pg, idx, 0.2, "prototipo, fiocco fisso al 20%")))
            fatte.append(("auto", await giro(pg, idx, "auto", "prototipo, fiocco regolato da solo")))
        print(" virata di bolina a circa 4 nodi:")
        v0 = await virata(pg2, None, "gioco, senza fiocco")
        v1 = await virata(pg, 0.05, "prototipo, fiocco cazzato")
        v2 = await virata(pg, 1.0, "prototipo, fiocco tutto lascato")
        # ---- il pannello del PROTOTIPO, stesso giro di tests/collaudo_pannello.py ----
        # Misura fiocco.html, non index.html: il prototipo ha un cursore e una riga in più.
        # Il caso che conta è l'ultimo, la regata con la spiegazione di un contatto: è il pannello più pieno.
        print("\n=== PANNELLO DEL PROTOTIPO ===")
        PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
        for W, H in [(1360, 650), (1360, 768)]:
            pg3 = await b.new_page(viewport={"width": W, "height": H})
            pg3.on("pageerror", lambda e: errs.append(str(e)))
            await pg3.goto(PROTO); await pg3.wait_for_timeout(400)
            eccede = []
            for li, n in enumerate([13, 7, 13, 5, 9, 5]):
                await pg3.evaluate(f"__sv.openItem(['l',{li}])")
                for k in range(n):
                    await pg3.evaluate(f"__sv.showStep({k})"); await pg3.wait_for_timeout(60)
                    d = await pg3.evaluate(PH)
                    if d > 0: eccede.append(f"lezione {li+1} passo {k+1}: +{d}")
            for it, nome in [("['m',0]", "prova 1"), ("['m',4]", "prova 5"), ("'free'", "navigazione libera")]:
                await pg3.evaluate(f"__sv.openItem({it})"); await pg3.wait_for_timeout(300)
                d = await pg3.evaluate(PH)
                if d > 0: eccede.append(f"{nome}: +{d}")
            await pg3.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", "60"])
            await pg3.evaluate("__sv.openItem(['r',0])"); await pg3.evaluate("__sv.fast(10)")
            await pg3.wait_for_timeout(7000); await pg3.evaluate("__sv.fast(1)")
            await pg3.evaluate("__sv.R.lastRule='Contatto con Blu: tu eri mure a sinistra e dovevi lasciare strada a chi era mure a dritta. Penalità di 15 secondi.'")
            await pg3.wait_for_timeout(400)
            d = await pg3.evaluate(PH)
            if d > 0: eccede.append(f"regata con la spiegazione di un contatto: +{d}")
            print(f"  finestra {W}x{H}: pannello che eccede: {eccede or 'nessuno'}")
            if eccede: errs.append(f"pannello che eccede a {W}x{H}")
            if (W, H) == (1360, 650):
                await pg3.screenshot(path=str(OUT / "pannello_regata.png"))
                await pg3.evaluate("__sv.openItem('free')"); await pg3.wait_for_timeout(400)
                await pg3.evaluate("""() => { const S = __sv.S; S.h = 55; __sv.ctl.sheet = 0.1; __sv.ctl.jib = 0.1; }""")
                await pg3.click("#zIn"); await pg3.click("#zIn"); await pg3.click("#zIn"); await pg3.wait_for_timeout(600)
                await pg3.screenshot(path=str(OUT / "fiocco_bolina.png"))
            await pg3.close()

        # ---- messaggi del fiocco nel pannello, a varie andature ----
        print("\n=== MESSAGGI DEL FIOCCO NEL PANNELLO ===")
        pg4 = await b.new_page(viewport={"width": 1360, "height": 650})
        pg4.on("pageerror", lambda e: errs.append(str(e)))
        await pg4.goto(PROTO); await pg4.wait_for_timeout(400)
        await pg4.evaluate("__sv.openItem('free')"); await pg4.wait_for_timeout(300)
        await pg4.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#gustSel", "0"])
        for twa in [20, 60, 90, 120, 135, 160]:
            await pg4.evaluate("""a => { const S = __sv.S; S.x = 0; S.y = 0; S.h = a; S.u = 3 / 1.943844; S.vl = 0; S.r = 0;
                __sv.ctl.tiller = 0; __sv.ctl.sheet = __sv.autoSheet(); __sv.ctl.jib = __sv.autoJib(); }""", twa)
            await pg4.evaluate("__sv.run(1/240, 240)")
            # regola DOPO l'assestamento: autoSheet/autoJib leggono l'ultimo vento apparente, non quello di partenza
            await pg4.evaluate("""() => { __sv.ctl.sheet = __sv.autoSheet(); __sv.ctl.jib = __sv.autoJib(); }""")
            await pg4.evaluate("__sv.run(1/240, 120)"); await pg4.wait_for_timeout(250)
            A = await pg4.evaluate("Math.round(Math.abs(__sv.info.awa))")
            print(f"  {twa:3d}° reali ({A:3d}° apparenti): «{await pg4.inner_text('#hintJib')}»")
        await pg4.close()

        print("\nerrori di pagina:", errs)
        await b.close()
        bad = errs or errori_tasti or errori6 or any(not r[0] or r[2] for k, r in fatte if k != "gioco") or not v1
        print("ESITO:", "tutto a posto" if not bad else "qualcosa non torna (vedi sopra)")
asyncio.run(main())
