# Tasto vista (0.19.2, «vista del percorso» dalla 0.19.3): Q tenuto sposta la barca sullo schermo dalla parte opposta all'obiettivo
# e, se serve, allontana l'inquadratura finché l'obiettivo entra; al rilascio torna posizione e zoom di prima.
# Parte 1 (#collaudo, tasto vero, tempo vero): 5 prove x 3 venti + regata prima del via, con «prua in alto» e «nord in alto».
#   Direzione: prodotto scalare fra spostamento e direzione dell'obiettivo sullo schermo negativo, spostamento di almeno 50 px,
#   barca fra il 20% e l'80% dello schermo. Ritorno: dopo il rilascio, sotto 2 px e zoom del tasto tornato a 1 (entro 0,002) entro 1 s.
#   Nessun effetto: lezione con la boa, navigazione libera, prova finita, focus in un campo di testo. Bloc Maiusc (tasto «Q»).
# Parte 2 (#collaudo, semi fissi): traiettoria identica al bit con Q tenuto e non tenuto (prova 5 e regata 2, con raffiche, 6 semi,
#   6 s a passi di 1/60 s con __sv.frame, che disegna anche). Prova del banco: la stessa corsa con Q tenuto, ma consumando un
#   numero casuale in più a ogni fotogramma con la barca spostata, deve dare uno stato diverso (barche e raffiche: in 6 s il
#   numero in più cambia una raffica nuova, che non arriva ancora alla barca).
# Parte 3: increspature a zoom 0,4 (conto delle celle con e senza Q, limite di disegno 2500).
# Parte 4 (pagina vera, senza #collaudo): prova 1 aperta dal menu; posizione della barca e freccia fuori schermo lette
#   intercettando il disegno; «Q vista» presente nella legenda o sul mare; scritta «Arrivo» disegnata.
# Parte 5 (0.19.3, #collaudo, 1360x650 e 1360x768, prua e nord in alto): prove 1-5, regata 1 prima del via e regata 1 verso la
#   boa di bolina. L'obiettivo deve stare dentro il mare disegnato (a) a zoom 1 con Q tenuto 1 s, (b) al solo zoom minimo, senza Q.
#   La posizione sullo schermo si legge intercettando il disegno: la trasformazione del mondo (subito dopo lo scale del mondo)
#   applicata al punto obiettivo di __sv.goal().
# Parte 6 (0.19.3, prova 5, 1360x650): tempo per fotogramma con il disegno vero (__sv.frame più una lettura di un pixel, che obbliga
#   il browser a disegnare), mediana di 3 mediane di 60 fotogrammi. Soglia dichiarata prima di misurare: al minimo zoom non oltre
#   1,10 volte quello a zoom 1 (10% = rumore visto nella sandbox). Raffiche al minimo zoom: ogni raffica si disegna con un
#   createRadialGradient (l'unico del gioco); in un fotogramma il conto deve essere uguale al numero di raffiche, e non zero.
#   Increspature al minimo zoom: zero celle.
# Uso: python collaudo_vista.py [file html]   (predefinito: index.html del progetto). Esce con 1 se un caso è sbagliato,
# se un gruppo di casi ha zero misure o se la pagina dà errori.
import asyncio, json, math, pathlib, sys
from playwright.async_api import async_playwright
HTML = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html"
BASE = HTML.as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
sbagli = []; conta = {}
def esito(gruppo, ok, det):
    conta[gruppo] = conta.get(gruppo, 0) + 1
    if not ok: sbagli.append(f"{gruppo}: {det}")

STATO = """(() => { const sv = __sv, S = sv.S, g = sv.goal(), c = sv.cam(), o = sv.viewOff;
  const prua = document.querySelector('#viewMode [aria-pressed="true"]').dataset.v === 'prua', r = prua ? -S.h * Math.PI / 180 : 0;
  const dx = g ? g.x - S.x : 0, dy = g ? g.y - S.y : 0;
  return { off: [o[0], o[1]], gx: dx * Math.cos(r) - dy * Math.sin(r), gy: dx * Math.sin(r) + dy * Math.cos(r), goal: !!g, cx: c.cx, cy: c.cy, W: c.W, H: c.H }; })()"""
RITORNO = """new Promise(res => { const t0 = performance.now();
  (function f(){ const o = __sv.viewOff, d = Math.hypot(o[0], o[1]), t = performance.now() - t0;
    if (d < 2 && Math.abs(__sv.zoomQ - 1) < 0.002) res([t, d]); else if (t > 3000) res([null, d]); else requestAnimationFrame(f); })(); })"""
VISTA = "v => document.querySelector(`#viewMode [data-v=\"${v}\"]`).click()"

async def tieni_q(pg, ms=500):
    await pg.keyboard.down("q"); await pg.wait_for_timeout(ms); s = await pg.evaluate(STATO); return s

async def parte1(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
    for vista in ["prua", "nord"]:
        await pg.evaluate(VISTA, vista)
        casi = [(f"prova {i+1} vento {w}", f"__sv.openItem(['m',{i}]); __sv.startMission({i},{w})") for i in range(5) for w in (0, 90, 200)]
        casi.append(("regata 1 prima del via", "__sv.openItem(['r',0])"))
        for nome, apri in casi:
            try:
                await pg.evaluate(apri); await pg.wait_for_timeout(300)
                s = await tieni_q(pg)
                ox, oy = s["off"]; d = math.hypot(ox, oy); dot = ox * s["gx"] + oy * s["gy"]
                dentro = 0.2 * s["W"] - 0.5 <= s["cx"] <= 0.8 * s["W"] + 0.5 and 0.2 * s["H"] - 0.5 <= s["cy"] <= 0.8 * s["H"] + 0.5
                esito(f"direzione ({vista} in alto)", s["goal"] and dot < 0 and d >= 50 and dentro,
                      f"{nome}: spostamento ({ox:.0f}, {oy:.0f}) px, obiettivo ({s['gx']:.0f}, {s['gy']:.0f}) m, barca a ({s['cx']:.0f}, {s['cy']:.0f})")
                await pg.keyboard.up("q"); t, d2 = await pg.evaluate(RITORNO)
                esito("ritorno sotto 2 px entro 1 s", t is not None and t <= 1000, f"{nome} ({vista}): {t} ms, {d2:.2f} px")
                if t is not None: tempi.append(t)
            except Exception as e:
                await pg.keyboard.up("q"); esito(f"direzione ({vista} in alto)", False, f"{nome}: {str(e)[:120]}")
    # nessun effetto dove non c'è obiettivo o dove Q non vale
    async def fermo(nome, apri):
        try:
            await pg.evaluate(apri); await pg.wait_for_timeout(300)
            s = await tieni_q(pg); await pg.keyboard.up("q")
            esito("nessun effetto", math.hypot(*s["off"]) < 0.5, f"{nome}: spostamento {s['off']}")
        except Exception as e:
            await pg.keyboard.up("q"); esito("nessun effetto", False, f"{nome}: {str(e)[:120]}")
        await pg.wait_for_timeout(1100)
    await fermo("navigazione libera", "__sv.openItem('free')")
    await fermo("prova 1 finita", "__sv.openItem(['m',0]); __sv.S.finished = true")
    try:
        await pg.evaluate("__sv.openItem(['l',4])")
        k = await pg.evaluate("(() => { for (let k = 0; k < 9; k++){ __sv.showStep(k); if (__sv.goal()) return k; } return -1; })()")
        esito("nessun effetto", k >= 0, "lezione 5: nessun passo con la boa")
        if k >= 0: await fermo(f"lezione 5 passo {k+1}, con la boa", f"__sv.showStep({k})")
    except Exception as e: esito("nessun effetto", False, f"lezione 5: {str(e)[:120]}")
    # focus in un campo di testo: Q scrive nel campo e la barca non si sposta
    try:
        await pg.evaluate("__sv.openItem(['m',0])"); await pg.wait_for_timeout(300)
        await pg.evaluate("(() => { const t = document.createElement('textarea'); t.id = 'tCampo'; document.body.appendChild(t); t.focus(); })()")
        s = await tieni_q(pg); await pg.keyboard.up("q")
        testo = await pg.evaluate("document.getElementById('tCampo').value")
        esito("nessun effetto", math.hypot(*s["off"]) < 0.5 and "q" in testo, f"campo di testo: spostamento {s['off']}, testo {testo!r}")
        await pg.evaluate("document.getElementById('tCampo').remove()")
    except Exception as e: esito("nessun effetto", False, f"campo di testo: {str(e)[:120]}")
    # Bloc Maiusc: il browser manda «Q» maiuscola
    try:
        await pg.wait_for_timeout(1100)
        await pg.evaluate("document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Q', code: 'KeyQ', modifierCapsLock: true, bubbles: true }))")
        await pg.wait_for_timeout(500); s = await pg.evaluate(STATO)
        await pg.evaluate("document.dispatchEvent(new KeyboardEvent('keyup', { key: 'Q', code: 'KeyQ', modifierCapsLock: true, bubbles: true }))")
        t, d2 = await pg.evaluate(RITORNO)
        esito("Bloc Maiusc", math.hypot(*s["off"]) >= 50 and t is not None and t <= 1000, f"spostamento {s['off']}, ritorno {t} ms")
    except Exception as e: esito("Bloc Maiusc", False, str(e)[:120])
    await pg.close(); return errs

# Aprire una voce azzera i tasti tenuti: Q si preme dopo l'apertura. Fra l'apertura e la corsa il ciclo del browser disegna
# ancora (consumando numeri casuali per il tremolio): per questo il seme si rimette all'inizio della corsa.
APRI = "([it, seme]) => { __seed(seme); __sv.openItem(it); __sv.fast(0); }"
CORSA = """([it, seme, banco]) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  __seed(seme);
  let maxOff = 0;
  for (let n = 0; n < 360; n++){
    const S = sv.S, g = sv.goal();
    if (n % 6 === 0 && g){ // pilota semplice: verso l'obiettivo, ma non più stretto di 50° dal vento; vela regolata
      let h = Math.atan2(g.x - S.x, -(g.y - S.y)) / D; const rel = n180(h - sv.twd);
      if (Math.abs(rel) < 50) h = sv.twd + (rel >= 0 ? 50 : -50);
      sv.ctl.tiller = Math.max(-1, Math.min(1, -n180(h - S.h) / 40)); sv.ctl.sheet = sv.autoSheet();
    }
    sv.frame(1 / 60);
    const o = sv.viewOff, d = Math.hypot(o[0], o[1]); maxOff = Math.max(maxOff, d);
    if (banco && d > 1) Math.random(); // banco: un numero casuale in più solo con la barca spostata
  }
  const S = sv.S, R = sv.R, barche = R ? R.boats.map(b => [b.S.x, b.S.y, b.S.h, b.S.u]) : [];
  return { stato: JSON.stringify([S.x, S.y, S.h, S.u, S.heel, S.time, barche, sv.gusts()]), maxOff };
}"""

async def parte2(b):
    # finestra più piccola: nella sandbox un fotogramma disegnato costa circa 20 ms
    pg = await b.new_page(viewport={"width": 900, "height": 500}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(SEME)
    async def corsa(it, seme, q, banco):   # ogni corsa in una pagina appena caricata: niente stato rimasto dalla corsa prima
        await pg.goto("about:blank"); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        await pg.evaluate(APRI, [it, seme])
        if q: await pg.keyboard.down("q")
        r = await pg.evaluate(CORSA, [it, seme, banco])
        if q: await pg.keyboard.up("q")
        return r
    for nome, it in [("prova 5", ["m", 4]), ("regata 2", ["r", 1])]:   # le due voci con raffiche: lì la simulazione usa numeri casuali
        for seme in range(1, 7):
            try:
                a = await corsa(it, seme, False, False); q = await corsa(it, seme, True, False); bb = await corsa(it, seme, True, True)
                esito("traiettoria identica con e senza Q", a["maxOff"] < 0.5 and q["maxOff"] >= 50 and a["stato"] == q["stato"],
                      f"{nome} seme {seme}: spostamento senza Q {a['maxOff']:.1f} px, con Q {q['maxOff']:.1f} px, uguali {a['stato'] == q['stato']}")
                esito("banco: un numero casuale in più si vede", bb["maxOff"] >= 50 and bb["stato"] != q["stato"], f"{nome} seme {seme}: spostamento {bb['maxOff']:.1f} px, diverse {bb['stato'] != q['stato']}")
            except Exception as e:
                await pg.keyboard.up("q"); esito("traiettoria identica con e senza Q", False, f"{nome} seme {seme}: {str(e)[:120]}")
    await pg.close(); return errs

async def parte3(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
    try:
        await pg.evaluate("__sv.openItem(['m',0])")
        for _ in range(4): await pg.click("#zOut")   # 1/1,25^4 = 0,41 (dalla 0.19.3 il minimo è 0,1)
        await pg.wait_for_timeout(2500)
        for vista in ["prua", "nord"]:
            await pg.evaluate(VISTA, vista); await pg.wait_for_timeout(300)
            n0 = await pg.evaluate("__sv.rippleCells")
            s = await tieni_q(pg, 700); n1 = await pg.evaluate("__sv.rippleCells"); await pg.keyboard.up("q")
            # stima con il raggio allargato dello spostamento (proposta), per confronto
            ppm = min(s["W"], s["H"]) / 48 * 0.4; R = math.hypot(s["W"], s["H"]) / ppm / 2 + 7; Ra = R + math.hypot(*s["off"]) / ppm
            print(f"  increspature a zoom 0,4 ({vista} in alto): {n0} celle senza Q, {n1} con Q (barca spostata di {math.hypot(*s['off']):.0f} px);"
                  f" con il raggio allargato sarebbero circa {round((2 * Ra / 7 + 1) ** 2)}")
            esito("increspature a zoom 0,4 sotto il limite di 2500", n0 < 2500 and n1 < 2500 and math.hypot(*s["off"]) >= 50, f"{vista}: {n0} e {n1} celle")
            await pg.wait_for_timeout(1100)
    except Exception as e: esito("increspature a zoom 0,4 sotto il limite di 2500", False, str(e)[:120])
    await pg.close(); return errs

DISEGNO = """(() => { window.__fr = []; window.__rg = 0; let cur = null; const P = CanvasRenderingContext2D.prototype;
  const st = P.setTransform, sc = P.scale, fi = P.fill, ft = P.fillText, tr = P.translate, rg = P.createRadialGradient;
  P.createRadialGradient = function(...a){ window.__rg++; return rg.apply(this, a); };
  P.setTransform = function(...a){ cur = { boat: null, arrow: null, testi: [], M: null, dopoScale: false }; window.__fr.push(cur); if (window.__fr.length > 400) window.__fr.shift(); return st.apply(this, a); };
  P.scale = function(x, y){ if (cur && !cur.boat && x === y && x > 1){ const m = this.getTransform(); cur.boat = [m.e / devicePixelRatio, m.f / devicePixelRatio]; cur.dopoScale = true; } return sc.call(this, x, y); };
  P.translate = function(x, y){ const r = tr.call(this, x, y); if (cur && cur.dopoScale && !cur.M){ const m = this.getTransform(); cur.M = [m.a, m.b, m.c, m.d, m.e, m.f]; } return r; };
  P.fill = function(...a){ if (cur && String(this.fillStyle).toLowerCase() === '#f28c1b'){ const m = this.getTransform();
      if (Math.abs(Math.hypot(m.a, m.b) - devicePixelRatio) < 1e-6) cur.arrow = Math.atan2(m.b, m.a); } return fi.apply(this, a); };
  P.fillText = function(t, ...a){ if (cur) cur.testi.push(String(t)); return ft.call(this, t, ...a); };
})();"""
ULTIMO = "(() => { const f = window.__fr.filter(f => f.boat); return f.length ? f[f.length - 1] : null; })()"
TESTI = "(() => [...new Set(window.__fr.flatMap(f => f.testi))])()"

async def parte4(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(DISEGNO); await pg.goto(BASE); await pg.wait_for_timeout(600)
    v = {}
    v["aggancio assente"] = await pg.evaluate("typeof window.__sv === 'undefined'")
    try:
        await pg.locator("#menu button.item", has_text="Prova 1").click(); await pg.wait_for_timeout(500)
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1000)
        f0 = await pg.evaluate(ULTIMO)
        await pg.keyboard.down("q"); await pg.wait_for_timeout(600); f1 = await pg.evaluate(ULTIMO)
        await pg.keyboard.up("q"); await pg.wait_for_timeout(1000); f2 = await pg.evaluate(ULTIMO)
        a = f0["arrow"]; dx, dy = f1["boat"][0] - f0["boat"][0], f1["boat"][1] - f0["boat"][1]
        print(f"  pagina vera: barca a {f0['boat']}, freccia a {a if a is None else round(math.degrees(a))}°, con Q spostata di ({dx:.0f}, {dy:.0f}) px,"
              f" dopo 1 s dal rilascio a {math.hypot(f2['boat'][0] - f0['boat'][0], f2['boat'][1] - f0['boat'][1]):.2f} px")
        v["freccia fuori schermo vista"] = a is not None
        v["con Q la barca va dalla parte opposta alla freccia (almeno 50 px)"] = a is not None and dx * math.cos(a) + dy * math.sin(a) < 0 and math.hypot(dx, dy) >= 50
        v["dopo 1 s dal rilascio torna entro 2 px"] = math.hypot(f2["boat"][0] - f0["boat"][0], f2["boat"][1] - f0["boat"][1]) < 2
        testi = await pg.evaluate(TESTI)
        legenda = await pg.evaluate("(() => { const k = document.getElementById('kQ'); return !!k && !k.hidden; })()")
        print(f"  «Q vista»: nella legenda del pannello {legenda}, sul mare {'Q vista' in testi}")
        v["«Q vista» nella legenda o sul mare (una sola delle due)"] = legenda != ("Q vista" in testi)
        v["scritta «Arrivo» disegnata"] = "Arrivo" in testi
    except Exception as e: v["prova 1 aperta dal menu"] = False; print("  errore:", str(e)[:200])
    await pg.close()
    print("pagina vera, senza #collaudo:")
    for k, ok in v.items(): print(f"  {'OK ' if ok else 'NO '} {k}")
    for k, ok in v.items(): esito("pagina vera", ok, k)
    return errs

# obiettivo sullo schermo, dall'ultima trasformazione del mondo intercettata
DENTRO = """(() => { const f = window.__fr.filter(f => f.M), g = __sv.goal(), c = __sv.cam(); if (!f.length || !g) return null;
  const [a, b, cc, d, e, ff] = f[f.length - 1].M, k = devicePixelRatio, x = (a * g.x + cc * g.y + e) / k, y = (b * g.x + d * g.y + ff) / k;
  return { x, y, W: c.W, H: c.H, dentro: x >= 0 && x <= c.W && y >= 0 && y <= c.H, zq: __sv.zoomQ, z: __sv.camZoom }; })()"""
VOCI = [(f"prova {i+1}", f"__sv.openItem(['m',{i}])") for i in range(5)] + [("regata 1 prima del via", "__sv.openItem(['r',0])"),
        ("regata 1 verso la boa di bolina", "__sv.openItem(['r',0]); __sv.R.t = 5; __sv.R.boats[0].leg = 1")]

async def parte5(b):
    errs = []
    for W, H in [(1360, 650), (1360, 768)]:
        for vista in ["prua", "nord"]:
            pg = await b.new_page(viewport={"width": W, "height": H}); pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(DISEGNO); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
            try:
                await pg.evaluate(VISTA, vista)
                for nome, apri in VOCI:   # (a) zoom 1, Q tenuto
                    await pg.evaluate(apri); await pg.wait_for_timeout(300)
                    await pg.keyboard.down("q"); await pg.wait_for_timeout(1000); r = await pg.evaluate(DENTRO); await pg.keyboard.up("q")
                    esito("obiettivo sullo schermo con Q", bool(r and r["dentro"]), f"{W}x{H} {vista}, {nome}: {r}")
                    if r and r["zq"] is not None: zq.append(r["zq"])
                    await pg.wait_for_timeout(1000)
                for _ in range(14): await pg.click("#zOut")
                await pg.wait_for_timeout(2500)
                for nome, apri in VOCI:   # (b) solo zoom minimo
                    await pg.evaluate(apri); await pg.wait_for_timeout(400); r = await pg.evaluate(DENTRO)
                    esito("obiettivo sullo schermo al solo zoom minimo", bool(r and r["dentro"]), f"{W}x{H} {vista}, {nome}: {r}")
                    if r and r["z"] is not None: zmin.append(r["z"])
            except Exception as e: esito("obiettivo sullo schermo con Q", False, f"{W}x{H} {vista}: {str(e)[:150]}")
            await pg.close()
    if zq: print(f"  con Q: fattore di zoom del tasto da {min(zq):.3f} a {max(zq):.3f}")
    if zmin: print(f"  zoom minimo raggiunto: {min(zmin):.3f}")
    return errs

MISURA = """(n) => { const c = document.querySelector("canvas").getContext("2d"), t = [];
  for (let k = 0; k < n; k++){ const a = performance.now(); __sv.frame(1 / 60); c.getImageData(0, 0, 1, 1); t.push(performance.now() - a); }
  t.sort((a, b) => a - b); return t[t.length >> 1]; }"""
async def parte6(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(DISEGNO); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
    try:
        await pg.evaluate("__sv.openItem(['m',4]); __sv.fast(0)"); await pg.wait_for_timeout(500)
        med = lambda v: sorted(v)[len(v) // 2]
        t1 = med([await pg.evaluate(MISURA, 60) for _ in range(3)])
        for _ in range(14): await pg.click("#zOut")
        await pg.wait_for_timeout(2500)
        tm = med([await pg.evaluate(MISURA, 60) for _ in range(3)])
        z = await pg.evaluate("__sv.camZoom")
        print(f"  tempo per fotogramma (disegno compreso): zoom 1 {t1:.1f} ms, zoom minimo ({z:.3f}) {tm:.1f} ms; soglia {1.10 * t1:.1f} ms")
        esito("tempo per fotogramma al minimo zoom", tm <= 1.10 * t1, f"zoom 1 {t1:.1f} ms, minimo {tm:.1f} ms")
        # in una sola chiamata: fra due chiamate il ciclo del browser disegnerebbe altri fotogrammi
        n0, n1, ng = await pg.evaluate("(() => { const a = window.__rg; __sv.frame(1 / 60); return [a, window.__rg, __sv.gusts().length]; })()")
        print(f"  raffiche al minimo zoom: {ng} raffiche, {n1 - n0} chiazze disegnate in un fotogramma; celle di increspature {await pg.evaluate('__sv.rippleCells')}")
        esito("raffiche disegnate al minimo zoom", ng > 0 and n1 - n0 == ng, f"{ng} raffiche, {n1 - n0} chiazze")
        esito("increspature non disegnate al minimo zoom", await pg.evaluate("__sv.rippleCells") == 0 and z < 0.35, f"zoom {z}")
    except Exception as e: esito("tempo per fotogramma al minimo zoom", False, str(e)[:150])
    await pg.close(); return errs

tempi = []; zq = []; zmin = []
async def main():
    print("file:", HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        e = await parte1(b) + await parte2(b) + await parte3(b) + await parte4(b) + await parte5(b) + await parte6(b)
        await b.close()
    if tempi: print(f"ritorno sotto 2 px: da {min(tempi):.0f} a {max(tempi):.0f} ms su {len(tempi)} rilasci")
    gruppi = ["direzione (prua in alto)", "direzione (nord in alto)", "ritorno sotto 2 px entro 1 s", "nessun effetto", "Bloc Maiusc",
              "traiettoria identica con e senza Q", "banco: un numero casuale in più si vede", "increspature a zoom 0,4 sotto il limite di 2500", "pagina vera",
              "obiettivo sullo schermo con Q", "obiettivo sullo schermo al solo zoom minimo", "tempo per fotogramma al minimo zoom",
              "raffiche disegnate al minimo zoom", "increspature non disegnate al minimo zoom"]
    zero = [g for g in gruppi if not conta.get(g)]
    print("casi misurati per gruppo:", {g: conta.get(g, 0) for g in gruppi})
    for s in sbagli[:25]: print("  SBAGLIATO:", s)
    if len(sbagli) > 25: print(f"  ... e altri {len(sbagli) - 25}")
    print("errori della pagina:", e)
    ok = not sbagli and not zero and not e
    print(f"casi misurati: {sum(conta.values())}; sbagliati: {len(sbagli)}; gruppi con zero casi: {zero or 'nessuno'}")
    print("esito:", "tutto OK" if ok else "FALLITO")
    sys.exit(0 if ok else 1)

asyncio.run(main())
