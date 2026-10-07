# Collaudo del registratore di sessione (0.18). Uso: python collaudo_registratore.py [parti, per esempio abcd]
#  a  pagina vera, senza #collaudo: interruttore spento di partenza, niente marcatori da spento; acceso col clic, scaricamento, avviso alla chiusura
#  b  5 sessioni con #collaudo: un pilota gioca la prova 3 (venti diversi), poi la lezione 2; marcatori e tasti premuti dal collaudo,
#     nota digitata con m e lettere dei comandi; il file viene letto da analizza_sessione.py. Misura anche la finestra delle impostazioni
#     e il pannello, con i caratteri veri del gioco: se mancano, le misure non sono valide e il collaudo esce con 1
#  c  fisica identica al bit con registratore acceso e spento (Math.random con seme, passi fissi), più la variante con un numero
#     casuale consumato di proposito, per mostrare che il metro vede una differenza
#  d  costo per passo di simulazione e fotogrammi al secondo, acceso contro spento
# Ogni parte dichiara quanti casi ha misurato e fallisce se sono zero. Esce con 1 se qualcosa non va.
import asyncio, io, pathlib, sys, contextlib, statistics
from playwright.async_api import async_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analizza_sessione as AS
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
import re
VERSIONE = re.search(r'const VERSIONE = "([^"]+)"', (pathlib.Path(__file__).resolve().parent.parent / "index.html").read_text()).group(1)  # 0.19: non più scritta a mano
URL = BASE + "#collaudo"
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
PARTI = sys.argv[1] if len(sys.argv) > 1 else "abcd"
fallito = []
non_valido = []
def esito(nome, ok, det=""):
    print(f"  {'OK ' if ok else 'NO '} {nome}" + (f": {det}" if det else ""), flush=True)
    if not ok: fallito.append(nome)

# eccesso di finestra delle impostazioni e del pannello, in pixel
ECCESSO = """() => { const d = document.getElementById('setDlg'), r = d.getBoundingClientRect(), p = document.querySelector('.panel');
  return { dialogo: Math.max(0, Math.ceil(r.bottom - innerHeight)) + Math.max(0, d.scrollHeight - d.clientHeight), pannello: p.scrollHeight - p.clientHeight }; }"""
SES_ON = ["#openSet", "#sesOn", "#setClose"]

# pilota della prova (logica di collaudo_fasce.py), a pezzi: ogni chiamata fa n passi da 1/60 s
PILOTA = """
(n) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  if (!window.__pil) { const last = sv.marks[sv.marks.length - 1]; window.__pil = { pts: [{ x: last.x, y: last.y }], i: 0, side: 1, n: 0 }; }
  const P = window.__pil;
  for (let k = 0; k < n && !sv.S.finished; k++) {
    const S = sv.S;
    if (P.n % 6 === 0) {
      const q = P.pts[Math.min(P.i, P.pts.length - 1)];
      const brg = Math.atan2(q.x - S.x, -(q.y - S.y)) / D, rel = n180(brg - sv.twd);
      let want = brg;
      if (Math.abs(rel) < 52) { if (Math.abs(rel) > 12) P.side = Math.sign(rel); want = sv.twd + P.side * 52; }
      const cur = n180(S.h - sv.twd);
      if (Math.abs(rel) > 168 && Math.abs(cur) > 90) want = sv.twd + Math.sign(cur || 1) * 168;
      if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
      const err = n180(S.h - want);
      sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
      const gybe = (Math.abs(cur) > 150 && Math.sign(n180(want - sv.twd)) !== Math.sign(cur)) || Math.abs(cur) > 174;
      sv.ctl.sheet = gybe ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet();
      if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" }));
    }
    sv.run(1 / 60, 1); P.n++;
  }
  return [sv.S.finished, sv.S.time];
}"""

async def scarica(pg):
    async with pg.expect_download() as d: await pg.click("#sesGet")
    return open(await (await d.value).path(), encoding="utf-8").read()

async def clic(pg, sel):
    for s in sel: await pg.click(s)

# ---------------------------------------------------------------- a
async def parte_a(p):
    print("a) pagina vera, senza #collaudo", flush=True)
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE); await pg.wait_for_timeout(500)
    esito("aggancio dei collaudi assente", await pg.evaluate("typeof window.__sv") == "undefined")
    await pg.click("#goFree"); await pg.wait_for_timeout(500)
    esito("il gioco è partito", await pg.evaluate("!document.getElementById('game').hidden"))
    await pg.click("#openSet")
    spento = not await pg.is_checked("#sesOn"); nascosto = await pg.evaluate("document.getElementById('sesBox').hidden")
    esito("interruttore spento all'apertura", spento and nascosto)
    await pg.click("#setClose")
    await pg.keyboard.press("m"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(1000); await pg.keyboard.up("ArrowLeft"); await pg.wait_for_timeout(2000)
    esito("da spento, M non mette marcatori", await pg.evaluate("document.getElementById('sesMarks').hidden"))
    await clic(pg, SES_ON); await pg.wait_for_timeout(2000)
    await pg.keyboard.press("m"); await pg.keyboard.down("ArrowRight"); await pg.wait_for_timeout(500); await pg.keyboard.up("ArrowRight"); await pg.wait_for_timeout(2000)
    await pg.click("#openSet"); testo = await scarica(pg)
    righe = testo.splitlines()
    ks = [r.split(" ", 2)[2] for r in righe if r.startswith("K ")]
    esito("file scaricato con un marcatore, i tasti e lo stato", sum(r.startswith("M ") for r in righe) == 1 and ks == ["→ giù", "→ su"] and sum(r.startswith("S ") for r in righe) >= 3,
          f"marcatori {sum(r.startswith('M ') for r in righe)}, tasti {ks}, righe di stato {sum(r.startswith('S ') for r in righe)}, {len(testo)} byte")
    esito("versione e navigazione libera nel file", f"# gioco {VERSIONE}" in testo and "apre navigazione libera" in testo)
    # l'avviso si prova uscendo dalla pagina con una navigazione: page.close(run_before_unload=True) nel browser senza finestra
    # non lo mostra in modo affidabile (0 su 9 nel gioco, 3 su 4 su una pagina minima con lo stesso gestore)
    dialoghi = []; pg.on("dialog", lambda d: (dialoghi.append(d.type), asyncio.ensure_future(d.accept())))
    await pg.click("#setClose"); await pg.wait_for_timeout(300)
    await pg.goto("about:blank"); await asyncio.sleep(0.5); await pg.close()
    esito("avviso alla chiusura con registrazione non scaricata", dialoghi == ["beforeunload"], f"{dialoghi}")
    pg2 = await b.new_page(); d2 = []; pg2.on("dialog", lambda d: (d2.append(d.type), asyncio.ensure_future(d.accept())))
    await pg2.goto(BASE); await pg2.click("#goFree"); await pg2.wait_for_timeout(800); await pg2.goto("about:blank"); await asyncio.sleep(0.5); await pg2.close()
    esito("nessun avviso se non si è mai registrato", d2 == [], f"{d2}")
    esito("nessun errore JS", not errs, f"{errs}")
    await b.close()

# ---------------------------------------------------------------- b
NOTA = "m w s r mamma: la barca ha virato male (M1), poi ok"
async def parte_b(p, n_sessioni=5):
    print(f"b) {n_sessioni} sessioni con il pilota", flush=True)
    b = await p.chromium.launch(); casi = 0; pesi = []; caratteri_tutti = []; ecc_misure = []
    for k in range(n_sessioni):
        vento = (k * 45 + 45) % 360; H = 650 if k % 2 == 0 else 768
        pg = await b.new_page(viewport={"width": 1360, "height": H}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        # le misure di eccesso qui sotto valgono solo con i caratteri veri del gioco: con i font di sistema
        # la larghezza e l'altezza del testo sono diverse e la prova non direbbe niente di vero sul margine reale.
        await pg.evaluate("document.fonts.ready")
        caratteri = await pg.evaluate("""() => ({
            "barlow 700": document.fonts.check('700 16px "Barlow Semi Condensed"'),
            "barlow 600": document.fonts.check('600 16px "Barlow Semi Condensed"'),
            "source serif 400": document.fonts.check('400 16px "Source Serif 4"'),
            "facce Barlow presenti e caricate (check() da solo dà vero anche senza)": [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"),
        })""")
        caratteri_tutti.append(all(caratteri.values()))
        await pg.evaluate("__sv.openItem(['m',2])"); await pg.evaluate(f"__sv.startMission(2, {vento})"); await pg.evaluate("__sv.fast(0)")
        await clic(pg, SES_ON); await pg.wait_for_timeout(100)
        pos_m = []; tasti = []; ck = 0
        while True:
            fin, t = await pg.evaluate(PILOTA, 30); ck += 1
            await pg.wait_for_timeout(15)
            if ck in (40, 120):
                pos_m.append(await pg.evaluate("[__sv.S.x, __sv.S.y]")); await pg.keyboard.press("m")
            if ck == 60: await pg.keyboard.down("ArrowUp"); tasti.append("↑ giù")
            if ck == 61: await pg.keyboard.up("ArrowUp"); tasti.append("↑ su")
            if ck == 90: await pg.keyboard.down("ArrowLeft"); tasti.append("← giù")
            if ck == 91: await pg.keyboard.up("ArrowLeft"); tasti.append("← su")
            if fin or t > 600: break
        conta = await pg.evaluate("({tacks: __sv.S.tacks, boe: __sv.S.markIdx, fin: __sv.S.finished, scuffie: __sv.S.capsizes, t: __sv.S.time})")
        await pg.evaluate("__sv.openItem(['l',1])")
        for i in range(4): await pg.evaluate(f"__sv.showStep({i})"); await pg.wait_for_timeout(500)
        await pg.click("#openSet")
        prima = await pg.evaluate("[__sv.ses.marks.length, __sv.ses.lines.filter(r => r[0] === 'K').length]")
        await pg.click("#sesNote"); await pg.keyboard.type(NOTA); await pg.keyboard.press("ArrowLeft"); await pg.keyboard.press("M"); await pg.wait_for_timeout(300)
        dopo = await pg.evaluate("[__sv.ses.marks.length, __sv.ses.lines.filter(r => r[0] === 'K').length]")
        valore = await pg.input_value("#sesNote")   # ← e M digitati nel campo finiscono nella nota, come devono
        ecc = await pg.evaluate(ECCESSO)
        if k < 2: await pg.screenshot(path=str(OUT / f"registratore_impostazioni_{H}.png"))
        testo = await scarica(pg); pesi.append((len(testo.encode()), conta["t"]))
        # caso peggiore della finestra: navigazione libera (tre scelte del vento in più), con nota e marcatori visibili
        await pg.click("#setClose"); await pg.evaluate("__sv.openItem('free')"); await pg.click("#openSet")
        ecc_l = await pg.evaluate(ECCESSO); await pg.click("#setClose")
        ecc_misure += [ecc["dialogo"], ecc["pannello"], ecc_l["dialogo"], ecc_l["pannello"]]
        (OUT / f"sessione_{k + 1}.txt").write_text(testo, encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): r = AS.analizza(testo)
        righe = [(a, float(t), d) for a, t, d in (x.split(" ", 2) for x in testo.splitlines() if x and x[0] != "#")]
        seg_i = next(i for i, (a, _, d) in enumerate(righe) if a == "E" and d.startswith("apre «Prova 3"))
        seg_f = next(i for i, (a, _, d) in enumerate(righe) if a == "E" and d.startswith("apre lezione 2"))
        seg = righe[seg_i:seg_f]
        n_vir = sum(a == "E" and d.startswith("virata") for a, _, d in seg); n_boe = sum(a == "E" and d.startswith("boa") for a, _, d in seg)
        n_arr = sum(a == "E" and d.startswith("arrivo") for a, _, d in seg)
        st = [t for a, t, _ in seg if a == "S"]; buco = max(b2 - a2 for a2, b2 in zip(st, st[1:]))
        mk = [d.split(" ") for a, _, d in righe if a == "M"]
        # il file scrive x e y con un decimale: ogni coordinata può scostarsi al massimo di 0,05 m
        dm = max(max(abs(float(m[1]) - x), abs(float(m[2]) - y)) for m, (x, y) in zip(mk, pos_m)) if len(mk) == len(pos_m) else 99
        ks = [d for a, _, d in righe if a == "K"]
        Ls = [d.split(" ")[0] for a, _, d in righe if a == "L"]
        and_g = next(h for h in testo.splitlines() if h.startswith("#  tempo per andatura"))
        print(f" sessione {k+1}: vento {vento}°, finestra 1360x{H}, prova 3 {'finita' if conta['fin'] else 'NON finita'} in {conta['t']:.0f} s, "
              f"{len(testo.encode())} byte, {len(righe)} righe, buco massimo fra righe di stato {buco:.2f} s", flush=True)
        esito("marcatori 2, nella posizione in cui il collaudo li ha premuti", len(mk) == 2 and dm <= 0.0501, f"{len(mk)} marcatori, scarto massimo per coordinata {dm:.3f} m")
        esito("tasti del collaudo ritrovati, nell'ordine", ks == tasti, f"{ks}")
        esito("nota scritta: nessun marcatore né tasto in più", prima == dopo and valore != NOTA and "# nota: " + valore in testo, f"prima {prima}, dopo {dopo}, nota «{valore}»")
        esito("virate, boe e arrivo come nei contatori del gioco (in parte circolare)", (n_vir, n_boe, n_arr) == (conta["tacks"], conta["boe"], int(conta["fin"])),
              f"file {n_vir}/{n_boe}/{n_arr}, gioco {conta['tacks']}/{conta['boe']}/{int(conta['fin'])}")
        esito("passi della lezione 2 tutti nel file", Ls == ["2.1", "2.2", "2.3", "2.4"], f"{Ls}")
        esito("righe di stato senza buchi oltre 1,5 s", buco <= 1.5 and len(st) > 100, f"{len(st)} righe")
        esito("riassunto del gioco uguale a quello ricalcolato", not r["diff"], f"{r['diff']}")
        esito("finestra delle impostazioni e pannello senza eccesso, in lezione e in navigazione libera", ecc == ecc_l == {"dialogo": 0, "pannello": 0}, f"lezione {ecc}, libera {ecc_l}")
        esito("nessun errore JS", not errs, f"{errs}")
        print(f"   andatura dal gioco: {and_g[39:]}\n   andatura stimata dallo script: " + " · ".join(f"{a} {v:.0f}s" for a, v in r['andT'].most_common()), flush=True)
        casi += 1; await pg.close()
    kb_h = statistics.mean(by / t * 3600 / 1000 for by, t in pesi)
    print(f" peso medio: {kb_h:.0f} KB per un'ora di simulazione (stimato dalle sessioni, che contengono anche la lezione)")
    caratteri_ok = all(caratteri_tutti)
    print("caratteri del gioco caricati:", caratteri_ok)
    print(f"finestra delle impostazioni e pannello: eccesso massimo (pixel): {max(ecc_misure)}")
    if not caratteri_ok:
        print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, le misure di eccesso sopra non sono attendibili")
        non_valido.append("parte b: caratteri del gioco non caricati")
    esito("sessioni misurate", casi == n_sessioni, f"{casi}")
    await b.close()

# ---------------------------------------------------------------- c
SEME = """(() => { let s = 1, n = 0; Math.random = () => { n++; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; n = 0; }; window.__nrand = () => n; })();"""
TRAIETTORIA = """
([item, vento, seme, secondi, extra]) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  __seed(seme); sv.openItem(item); if (item[0] === 'm') sv.startMission(item[1], vento); sv.fast(0);
  const f = new Float64Array(1), u = new Uint32Array(f.buffer); let h = 2166136261;
  const mix = v => { f[0] = v; h = Math.imul(h ^ u[0], 16777619); h = Math.imul(h ^ u[1], 16777619); };
  const N = Math.round(secondi * 60), x0 = sv.S.x, y0 = sv.S.y; let side = 1, rotte = [52, 100, 150, -150, -100, -52];
  const last = sv.marks.length ? sv.marks[sv.marks.length - 1] : null; let lungo = 0, px = x0, py = y0;
  for (let n = 0; n < N && !sv.S.finished; n++) {
    const S = sv.S;
    if (extra && n === (N >> 1)) Math.random();
    if (n % 6 === 0) {
      let want;
      if (item[0] === 'm') { const brg = Math.atan2(last.x - S.x, -(last.y - S.y)) / D, rel = n180(brg - sv.twd); want = brg;
        if (Math.abs(rel) < 52) { if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; } }
      else want = sv.twd + rotte[Math.floor(n / 1200) % rotte.length];
      const cur = n180(S.h - sv.twd);
      if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
      sv.ctl.tiller = Math.max(-1, Math.min(1, n180(S.h - want) / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
      sv.ctl.sheet = sv.autoSheet();
      if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" }));
    }
    sv.run(1 / 60, 1);
    mix(sv.S.x); mix(sv.S.y); mix(sv.S.h); mix(sv.S.u); mix(sv.S.heel); lungo += Math.hypot(sv.S.x - px, sv.S.y - py); px = sv.S.x; py = sv.S.y;
  }
  return { h: (h >>> 0).toString(16), passi: N, metri: Math.round(lungo), casuali: __nrand(), righe: sv.ses.lines.length, scuffie: sv.S.capsizes };
}"""
async def parte_c(p, semi=10):
    print(f"c) traiettoria identica al bit, {semi} semi", flush=True)
    b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME); errs = []
    casi = [(["m", 0], 0, 200, "prova 1"), (["m", 1], 90, 200, "prova 2"), (["m", 2], 225, 200, "prova 3"),
            ("free", "10", 150, "libera 10 nodi, raffiche forti"), ("free", "15", 150, "libera 15 nodi, raffiche forti")]
    # ogni corsa in una pagina nuova: con le raffiche il vento oscilla con simTime (index.html, windAt), che non si azzera fra una corsa e l'altra
    async def corsa(item, vento, seme, sec, acceso, extra):
        pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.evaluate("__sv.fast(0)"); await pg.wait_for_timeout(50)
        if item == "free" or acceso:
            await pg.evaluate("__sv.openItem('free')"); await pg.click("#openSet")
            if item == "free": await pg.select_option("#wSpd", vento); await pg.select_option("#gustSel", "2")
            if acceso: await pg.click("#sesOn")
            await pg.click("#setClose")
        r = await pg.evaluate(TRAIETTORIA, [item, vento, seme, sec, extra]); await pg.close(); return r
    async def giro(acceso, extra):
        return {(nome, s): await corsa(item, vento, s * 7919, sec, acceso, extra) for item, vento, sec, nome in casi for s in range(1, semi + 1)}
    spento = await giro(False, False)
    spento2 = await giro(False, False)   # controllo: la stessa corsa ripetuta a registratore spento deve già essere identica
    acceso = await giro(True, False); variante = await giro(True, True)
    for _, _, _, nome in casi:
        ks = [k for k in spento if k[0] == nome]
        uguali = sum(spento[k]["h"] == acceso[k]["h"] for k in ks); ripetute = sum(spento[k]["h"] == spento2[k]["h"] for k in ks)
        divergono = sum(spento[k]["h"] != variante[k]["h"] for k in ks)
        cas = statistics.median(spento[k]["casuali"] for k in ks); metri = min(spento[k]["metri"] for k in ks)
        righe = min(acceso[k]["righe"] for k in ks)
        print(f"  {nome}: spento ripetuto identico {ripetute} su {len(ks)} | acceso identico {uguali} su {len(ks)} | la variante diverge in {divergono} su {len(ks)} | "
              f"numeri casuali per corsa (mediana) {cas:.0f} | percorso minimo {metri} m | scuffie {sum(spento[k]['scuffie'] for k in ks)} | righe registrate (minimo) {righe}", flush=True)
        esito(f"{nome}: spento ripetuto due volte identico al bit (controllo del banco)", ripetute == len(ks))
        esito(f"{nome}: acceso e spento identici al bit", uguali == len(ks) and len(ks) > 0 and metri > 50)
        if cas > 0: esito(f"{nome}: il metro vede un numero casuale in più", divergono == len(ks))
    esito("il registratore registrava davvero durante il confronto", min(v["righe"] for v in acceso.values()) > 0)
    esito("nessun errore JS", not errs, f"{errs}")
    await b.close()

# ---------------------------------------------------------------- d
async def parte_d(p, rip=3):
    print("d) costo del registratore", flush=True)
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
    await pg.goto(URL); await pg.wait_for_timeout(300); await pg.evaluate("__sv.openItem('free')")
    await pg.click("#openSet"); await pg.select_option("#gustSel", "2"); await pg.click("#setClose")
    PASSO = "n => { const t0 = performance.now(); __sv.run(1 / 60, n); return (performance.now() - t0) / n * 1000; }"   # microsecondi per passo
    FPS = "ms => new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < ms) requestAnimationFrame(f); else r(n / (performance.now() - t0) * 1000); }; requestAnimationFrame(f); })"
    async def misura():
        await pg.evaluate("__sv.openItem('free')"); await pg.evaluate("__sv.fast(0)")
        us = [await pg.evaluate(PASSO, 20000) for _ in range(rip)]
        await pg.evaluate("__sv.fast(1)"); fps = await pg.evaluate(FPS, 3000)
        return us, fps
    off1 = await misura(); await clic(pg, SES_ON); on1 = await misura(); await clic(pg, SES_ON); off2 = await misura()
    for nome, (us, fps) in [("spento", off1), ("acceso", on1), ("spento di nuovo", off2)]:
        print(f"  {nome}: µs per passo {', '.join(f'{x:.1f}' for x in us)} | fotogrammi al secondo {fps:.1f}", flush=True)
    extra = statistics.median(on1[0]) - statistics.median(off1[0] + off2[0])
    esito("meno di 0,05 ms in più per passo (soglia nostra)", extra < 50, f"{extra:+.1f} µs per passo")
    await b.close()

async def main():
    async with async_playwright() as p:
        if "a" in PARTI: await parte_a(p)
        if "b" in PARTI: await parte_b(p)
        if "c" in PARTI: await parte_c(p)
        if "d" in PARTI: await parte_d(p)
    print("esito:", "tutto OK" if not fallito else f"{len(fallito)} verifiche fallite: {fallito}")
    sys.exit(1 if (fallito or non_valido) else 0)
asyncio.run(main())
