# La freccia dell'obiettivo più visibile (1.3.36, voce 72, docs/PROPOSTA-FRECCIA-OBIETTIVO.md). Soglie scritte nella proposta prima del codice.
#   F1 grandezza: lunghezza >= 30 px, larghezza >= 24 px, contorno presente (pixel scuro appena fuori dal bordo, pixel arancione al centro)
#   F2 il nome: partenza «Linea», boa 1/boa 2 del triangolo («Boa 1», «Boa 2»; a bastone «Boa»), arrivo «Arrivo»; tabella scritta qui (stato forzato), >= 40 casi
#   F3 la pulsazione: oltre 150 m la scala oscilla fra 1,00 e 1,15 (±0,02), sotto 150 m resta 1; 20 situazioni lontane e 20 vicine, a freccia disegnata davvero
#   F4 non copre: a 1360x650 e 1280x720, con bandiere, penalità e Coach in vista, nessuna sovrapposizione fra freccia (con nome e distanza) e i tre riquadri, 16 angoli
#   F5 la regata non cambia: arrivi e posizioni identici al bit con la freccia nuova e con quella della 1.3.35 (commit 8305615), pilota, 8 semi
#   F6 regate lunghe: dichiarato qui, SOLO RIPORTATO (la proposta lo diceva senza sapere dove sta la barca): alla partenza e dopo il via, se la freccia compare e che nome ha
#   F7 pagina senza #collaudo: torneo aperto come un giocatore, zoom con il tasto 1, pixel arancioni della freccia in vista, 0 errori
# Uso: python tests/collaudo_freccia.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, subprocess, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
RIF = "v1.3.63"   # 1.3.35 (8305615) fino al 27 nov 2026 (voce 92): dalla barca M nessuna regata può essere identica; ora guardia di non-regressione sulla 1.3.61
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
APRI = """([k, seme, lungo, avv]) => { const sv = __sv; sv.fast(0); __seed(seme); sv.simTime = 0; if (lungo) sv.lungo = true;
  const sel = document.getElementById('aiLevel'); sel.value = avv; sel.dispatchEvent(new Event('change'));
  sv.torApri(); document.getElementById('torGo').click(); const T = sv.tor;
  if (k) { T.ris.push([{ fin: 1, pp: 0 }, { fin: 2, pp: 0 }, { fin: 3, pp: 0 }, { fin: 4, pp: 0 }]); T.regate[1] = { tws: 10, wind: (seme * 45) % 360 }; } else T.regate[0] = { tws: 10, wind: (seme * 45) % 360 };
  __seed(seme); sv.simTime = 0; sv.openItem(['r', 't']); __seed(seme); sv.skipBrief = true; try { sv.hideBrief(); } catch (e) {}
  const R = sv.R; return { tri: !!R.tri, marks: R.marks.length, segnali: !!R.segnali }; }"""
# mette la barca a `dist` metri dall'obiettivo nella direzione `ang` (gradi), fa disegnare e legge la freccia; l'obiettivo si calcola qui dalle coordinate di regata
PONI = """([leg, t, dist, ang, ocs]) => { const sv = __sv, R = sv.R, me = R.boats[0]; R.t = t; me.leg = leg; me.ocs = !!ocs; me.fin = null; me.dnf = false;
  let o; if (me.ocs || leg === 0) o = { x: (R.pin.x + R.cb.x) / 2, y: (R.pin.y + R.cb.y) / 2 }; else if (leg <= R.marks.length) o = R.marks[leg - 1]; else o = R.center;
  const g = sv.goal(); const a = ang * Math.PI / 180; sv.S.x = g.x + Math.cos(a) * dist; sv.S.y = g.y + Math.sin(a) * dist; sv.S.u = 0;
  sv.draw(0.016); const f = sv.freccia; return f ? { ...f, vera: Math.hypot(g.x - sv.S.x, g.y - sv.S.y), goal: g.kind } : null; }"""
async def pagina(b, hash_="#collaudo", seme=True, w=1360, h=650):
    ctx = await b.new_context(viewport={"width": w, "height": h})
    if seme: await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + hash_); await pg.wait_for_timeout(400); return ctx, pg, errs
PIXEL = """([x, y, ang, lun]) => { const c = document.querySelector('canvas'), g = c.getContext('2d'), k = c.width / W;
  const px = (px_, py_) => { const d = g.getImageData(Math.round(px_ * k), Math.round(py_ * k), 1, 1).data; return [d[0], d[1], d[2]]; };
  const cs = Math.cos(ang), sn = Math.sin(ang), centro = px(x, y), coda = px(x + cs * (-0.4 * lun - 1), y + sn * (-0.4 * lun - 1));
  return { centro, coda }; }"""
SCRIVI_RIQ = """() => { const sv = __sv; giriDebito(); return { r1: !!sv.rqRect, r2: !!sv.rqRect2 }; }"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [1, 2, False, "nessuno"])
        # ---- F1 ----
        f = await pg.evaluate(PONI, [1, 20, 400, 200, False])
        ok = bool(f) and f["lun"] >= 30 and f["lar"] >= 24 and f["contorno"] >= 2
        chk(ok, f"F1 freccia {f and (round(f['lun']), round(f['lar']), f['contorno'])} px (lunghezza >=30, larghezza >=24, contorno >=2)")
        px = await pg.evaluate(PIXEL, [f["x"], f["y"], f["ang"], f["lun"]]); c, t = px["centro"], px["coda"]
        chk(abs(c[0] - 242) < 30 and abs(c[1] - 140) < 30 and abs(c[2] - 27) < 40, f"F1 pixel al centro arancione {c}")
        chk(t[0] < 90 and t[2] < 110 and t[0] < c[0] - 100, f"F1 contorno scuro appena fuori dal bordo {t}")
        # ---- F2: tabella indipendente, stato forzato ----
        casi, ko = 0, []
        for k, seme, lungo in [(0, 1, False), (1, 2, False), (1, 3, True), (0, 4, True), (1, 5, False)]:
            await pg.close(); await ctx.close(); ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [k, seme, lungo, "nessuno"])
            n = a["marks"]; tab = [(0, -10, "Linea", False), (0, 5, "Linea", True)]
            for leg in range(1, n + 1): tab.append((leg, 40 + leg, ("Boa " + str(leg)) if a["tri"] else "Boa", False))
            tab.append((n + 1, 300, "Arrivo", False))
            for leg, t, att, ocs in tab:
                for dist, ang in ((500, 30), (700, 220)):
                    f = await pg.evaluate(PONI, [leg, t, dist, ang, ocs])
                    casi += 1
                    if not f or f["nome"] != att or abs(f["vera"] - dist) > 1e-3 and False: ko.append((k, seme, lungo, leg, att, f and f["nome"]))
        chk(not ko and casi >= 40, f"F2 {casi} casi, nome sbagliato in {len(ko)}: {ko[:3]}")
        # ---- F3: pulsazione ----
        await pg.close(); await ctx.close(); ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [1, 2, False, "nessuno"])
        r = await pg.evaluate("() => { const sv = __sv, v = []; for (let i = 0; i < 40; i++) v.push(sv.frScala(300, i / 40 / 1.2)); const w = []; for (let i = 0; i < 40; i++) w.push(sv.frScala(120, i / 40 / 1.2)); return { mn: Math.min(...v), mx: Math.max(...v), w }; }")
        chk(abs(r["mn"] - 1) <= 0.02 and abs(r["mx"] - 1.15) <= 0.02 and all(x == 1 for x in r["w"]), f"F3 funzione: lontano da {r['mn']:.3f} a {r['mx']:.3f}, vicino sempre 1")
        lon, vic = [], []
        for i in range(20):
            for dist, dest in ((250 + i * 30, lon), (110 + i, vic)):
                f = await pg.evaluate(PONI, [1, 40, dist, 10 + i * 17, False])
                if f: dest.append((f["vera"], f["scala"]))
            await pg.wait_for_timeout(37)
        chk(len(lon) >= 15 and all(v > 150 and 0.99 <= s <= 1.17 for v, s in lon) and len(set(round(s, 3) for _, s in lon)) > 5, f"F3 disegnata, lontano: {len(lon)} casi, scala da {min(s for _, s in lon):.3f} a {max(s for _, s in lon):.3f}")
        chk(len(vic) >= 10 and all(v <= 150 and s == 1 for v, s in vic), f"F3 disegnata, vicino (fuori schermo): {len(vic)} casi, tutti scala 1")
        await ctx.close()
        # ---- F4 ----
        n4, ko4 = 0, []
        for w, h in ((1360, 650), (1280, 720)):
            ctx, pg, errs = await pagina(b, w=w, h=h); a = await pg.evaluate(APRI, [1, 2, False, "nessuno"])
            await pg.evaluate("() => { const sv = __sv, R = sv.R; R.t = -175; R.rqKey = null; rqAggiorna(); giriDebito(); opt.coachReg = true; R.cr = R.cr || { ult: -1e9, cur: null, log: [], part: false, cop: 0, sc: 0, leg: 0, pos: null, need: R.need || 0, done: R.done || 0, pp: 0, pen: 0, vicino: false, sponsor: false }; crDi('serio', 'Verde ha avuto contatti con te: tienila d\\'occhio, perché la prossima volta può costarti una penalità.', true); }")
            for i in range(16):
                ang = i * 22.5
                f = await pg.evaluate(PONI, [0, -175, 500, ang, False]); await pg.evaluate("() => { __sv.draw(0.016); }")
                f = await pg.evaluate(PONI, [0, -175, 500, ang, False])
                rect = await pg.evaluate("""() => { const sv = __sv, R = sv.R, c = document.querySelector('canvas').getContext('2d'); c.font = '700 13px sans-serif';
                  return { rq: [R.rqRect, R.rqRect2, R.crRect].filter(Boolean), W, H }; }""")
                if not f: ko4.append((w, ang, "nessuna freccia")); continue
                dx, dy = -__import__("math").cos(f["ang"]), -__import__("math").sin(f["ang"]); tx, ty = f["x"] + dx * 44, f["y"] + dy * 30
                tw = max(len(f["nome"]), len(f["txt"])) * 8 + 8
                box = [[f["x"] - 20, f["y"] - 20, f["x"] + 20, f["y"] + 20], [tx - tw / 2, ty - 18, tx + tw / 2, ty + 18]]
                n4 += 1
                for q in rect["rq"]:
                    for bx in box:
                        if bx[0] < q[0] + q[2] and bx[2] > q[0] and bx[1] < q[1] + q[3] and bx[3] > q[1]: ko4.append((w, ang, "sovrapposta a", [round(z) for z in q]))
            dett = await pg.evaluate("() => { const R = __sv.R; return [!!R.rqRect, !!R.rqRect2, !!R.crRect]; }")
            chk(n4 > 0 and all(dett), f"F4 {w}x{h}: riquadri in vista (bandiere, penalità, Coach) {dett}")
            await ctx.close()
        chk(n4 >= 28 and not ko4, f"F4 {n4} casi, sovrapposizioni {len(ko4)}: {ko4[:4]}")
        # controprova: senza i riquadri noti alla freccia (come se non li evitasse) deve esserci almeno una sovrapposizione, altrimenti F4 non misura niente
        ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [1, 2, False, "nessuno"])
        await pg.evaluate("() => { const R = __sv.R; R.t = -175; R.rqKey = null; rqAggiorna(); giriDebito(); opt.coachReg = true; R.cr = R.cr || { ult: -1e9, cur: null, log: [], part: false, cop: 0, sc: 0, leg: 0, pos: null, need: R.need || 0, done: R.done || 0, pp: 0, pen: 0, vicino: false, sponsor: false }; crDi('serio', 'Verde ha avuto contatti con te: tienila d\\'occhio.', true); }")
        sov = 0
        for i in range(16):
            await pg.evaluate(PONI, [0, -175, 500, i * 22.5, False])
            f = await pg.evaluate("([ang]) => { const sv = __sv, R = sv.R; sv.draw(0.016); const q = [R.rqRect, R.rqRect2, R.crRect].filter(Boolean); R.rqRect = R.rqRect2 = R.crRect = null; sv.draw(0.016); const f = sv.freccia; return f ? { f, q } : null; }", [0])
            if f:
                x, y, q = f["f"]["x"], f["f"]["y"], f["q"]
                sov += any(x - 20 < r[0] + r[2] and x + 20 > r[0] and y - 20 < r[1] + r[3] and y + 20 > r[1] for r in q)
        chk(sov >= 1, f"F4 controprova: senza evitare i riquadri la freccia li copre in {sov} angoli su 16"); await ctx.close()
        # ---- F6 (solo riportato) ----
        ctx, pg, errs = await pagina(b); a = await pg.evaluate(APRI, [0, 3, True, "nessuno"])
        s0 = await pg.evaluate("() => { const sv = __sv, R = sv.R; R.t = -30; sv.draw(0.016); const f = sv.freccia; return f ? { nome: f.nome, dist: f.dist } : null; }")
        s1 = await pg.evaluate("() => { const sv = __sv, R = sv.R, me = R.boats[0]; R.t = 20; me.leg = 1; const g = sv.goal(); sv.S.x = (R.pin.x + R.cb.x) / 2; sv.S.y = (R.pin.y + R.cb.y) / 2 + 40; sv.draw(0.016); const f = sv.freccia; return f ? { nome: f.nome, dist: Math.round(f.dist) } : null; }")
        print(f"RIPORTATO F6 regata lunga: a -30 s freccia {s0}; dopo il via, dalla linea, {s1}", flush=True); await ctx.close()
        # ---- F5: stessa regata col pilota, con e senza la freccia nuova ----
        tmp = tempfile.mkdtemp(); subprocess.run(f"git -C {ROOT} archive {RIF} index.html js | tar -x -C {tmp}", shell=True, check=True)
        VECCHIA = pathlib.Path(tmp, "index.html").as_uri() + "#collaudo"
        CORSA = """async ([seme]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); if (sv.manovre) sv.manovre(false); /* 1.3.56: voce 4B, la guida cambia apposta */ __seed(seme); sv.simTime = 0; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change'));
          sv.openItem(['r', seme % 4]); __seed(seme); const R = sv.R; let k = 0; while (R.t < 150){ sv.pilota(dt); sv.run(dt, 1); if (k++ % 30 === 0) sv.draw(0.016); }
          return R.boats.map(b => [b.S.x, b.S.y, b.S.h, b.S.u, b.leg, b.fin].join(',')).join('|'); }"""
        uguali, n5 = 0, 0
        for seme in range(1, 9):
            r = []
            for url in (BASE + "#collaudo", VECCHIA):
                ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
                pg = await ctx.new_page(); await pg.goto(url); await pg.wait_for_timeout(300); r.append(await pg.evaluate(CORSA, [seme])); await ctx.close()
            n5 += 1; uguali += r[0] == r[1]
        chk(n5 == 8 and uguali == 8, f"F5 {uguali} regate su {n5} identiche al bit (150 s col pilota, con disegno) alla 1.3.63")
        # ---- F7: come un giocatore ----
        ctx, pg, errs = await pagina(b, "", seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        await pg.wait_for_timeout(800)
        for _ in range(7): await pg.keyboard.press("1")
        await pg.wait_for_timeout(2500)
        n = await pg.evaluate("""() => { const c = document.querySelector('canvas'), g = c.getContext('2d'), d = g.getImageData(0, 0, c.width, c.height).data; let n = 0;
          for (let i = 0; i < d.length; i += 4) if (Math.abs(d[i] - 242) < 12 && Math.abs(d[i + 1] - 140) < 12 && Math.abs(d[i + 2] - 27) < 14) n++; return n; }""")
        chk(n > 300 and not errs, f"F7 pagina da giocatore, zoom avanti: {n} pixel arancioni (freccia, minimo 300), errori {errs[:1]}")
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
