# Collaudi nel browser del prototipo del fiocco (tappa A).
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
            atteso = "flog" if twa == 20 else {"tutta lascata": "wind", "regolata": "ok", "tutta cazzata": "lee"}[nome]
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
        # ---- il pannello con un cursore in più, e un'immagine del fiocco ----
        print("\n=== PANNELLO E IMMAGINE ===")
        pg3 = await b.new_page(viewport={"width": 1360, "height": 650})
        pg3.on("pageerror", lambda e: errs.append(str(e)))
        await pg3.goto(PROTO); await pg3.wait_for_timeout(400)
        PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
        for it, nome in [("'free'", "navigazione libera"), ("['m',0]", "prova 1"), ("['r',0]", "regata 1")]:
            await pg3.evaluate(f"__sv.openItem({it})"); await pg3.wait_for_timeout(400)
            d = await pg3.evaluate(PH)
            print(f"  {nome} a 1360x650: pannello che eccede {'+' + str(d) if d > 0 else 'no'}")
        await pg3.evaluate("""() => { const S = __sv.S;
            S.x = 0; S.y = 0; S.h = 55; S.u = 3.4 / 1.943844; S.vl = 0; S.r = 0;
            __sv.ctl.tiller = 0; __sv.ctl.sheet = 0.1; __sv.ctl.jib = 0.1; }""")
        await pg3.evaluate("__sv.openItem('free')"); await pg3.wait_for_timeout(200)
        await pg3.evaluate("""() => { const S = __sv.S; S.h = 55; __sv.ctl.sheet = 0.1; __sv.ctl.jib = 0.1; }""")
        await pg3.click("#zIn"); await pg3.click("#zIn"); await pg3.click("#zIn"); await pg3.wait_for_timeout(600)
        await pg3.screenshot(path=str(OUT / "fiocco_bolina.png"))
        print(f"  immagine: {OUT / 'fiocco_bolina.png'}")
        print("\nerrori di pagina:", errs)
        await b.close()
        bad = errori6 or any(not r[0] or r[2] for k, r in fatte if k != "gioco") or not v1
        print("ESITO:", "tutto a posto" if not bad else "qualcosa non torna (vedi sopra)")
asyncio.run(main())
