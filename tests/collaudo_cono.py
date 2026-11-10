# Collaudo del cono d'ombra delle vele (1.2.25, docs/PROPOSTA-CONO-D-OMBRA.md, criteri K1-K6 e parte di K14, scritti prima di misurare).
# Casi costruiti: la regata a bastone del menu (vento costante, niente raffiche né salti) con il cono acceso a mano (R.ombra = true), così il vento
# libero è uguale dappertutto e il metro non dipende dalle raffiche. In più: il cono è acceso nel torneo e spento nelle regate del menu, la casella
# delle impostazioni nasconde il disegno ma non la fisica, e la pagina senza #collaudo apre il torneo senza errori.
#  K1 sull'asse a 0,5 / 1 / 2 altezze d'albero: spinta libera / spinta coperta (dal motore, step) entro il 15% da 4,8 / 2,6 / 2,0 (F75)
#  K2 a una lunghezza di lato dall'asse: spinta almeno il 99% della libera
#  K3 sopravento, al traverso sopravento e oltre 10 lunghezze: vento tolto esattamente zero
#  K4 l'asse segue il vento apparente: da ferma a 4 nodi di bolina gira di almeno 10°
#  K5 vela che sbatte: al massimo il 10% a un'altezza d'albero; scuffiata: zero
#  K6 in navigazione (ciclo vero del gioco, barca del giocatore tenuta in rotta di bolina): 1,5 lunghezze dentro il cono di un'altra perde almeno il 10%
#     di velocità in 20 s; sottovento e avanti, fuori dal cono, meno dell'1%. 10 varianti ciascuno, almeno 9 su 10.
# Uso: python tests/collaudo_cono.py      Esce con 1 se un criterio non è rispettato, 2 se la misura non è valida.
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
RADICE = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
URL = (RADICE / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
# scena ferma: A (un avversario) ferma di bolina mure a dritta a 50° dal vento, vela a segno; il metro legge la spinta di una seconda barca nel punto P
FERMI = """() => { const sv = __sv; sv.fast(0); __seed(7); sv.openItem(["r", 0]); const menuOmbra = R.ombra; R.ombra = true; R.t = 5; R.phase = "race";
  const A = R.boats[1], Bb = R.boats[2], w = windAt(0, 0), L = BOAT.length, H = 5.5;
  const metti = (b, x, y, h, u, sheet) => { Object.assign(b.S, { x, y, h: (h + 360) % 360, u, vl: 0, r: 0, heel: 0, capsized: false }); b.ctl.sheet = sheet; b.info = step(b.S, b.ctl, windAt(x, y), 0); };
  metti(A, 0, 0, w.twd - 50, 0, 0.25);
  const o = ombraDir(A), ux = Math.sin(o.dir * D2R), uy = -Math.cos(o.dir * D2R), px = -uy, py = ux;
  const spinta = (x, y) => { metti(Bb, x, y, w.twd - 50, 0, 0.25); const lib = step(Bb.S, Bb.ctl, windAt(x, y), 0).drive, k = ombraDi(A, x, y), ww = windAt(x, y); ww.tws *= 1 - k; return { lib, cop: step(Bb.S, Bb.ctl, ww, 0).drive, k }; };
  const asse = [0.5, 1, 2].map(n => spinta(ux * n * H, uy * n * H));
  const lato = [1, 2].map(n => spinta(ux * n * H + px * L, uy * n * H + py * L)), latoM = [1, 2].map(n => spinta(ux * n * H - px * L, uy * n * H - py * L));
  const up = [Math.sin(w.twd * D2R), -Math.cos(w.twd * D2R)];   // verso il vento
  const zero = [ombraDi(A, up[0] * 5, up[1] * 5), ombraDi(A, up[0] * 20, up[1] * 20), ombraDi(A, -ux * 3, -uy * 3), ombraDi(A, ux * 10.01 * L, uy * 10.01 * L), ombraDi(A, ux * 60, uy * 60), ombraDi(A, px * 6 + up[0] * 1, py * 6 + up[1] * 1)];
  const dentro = ombraDi(A, ux * 9.5 * L, uy * 9.5 * L);
  metti(A, 0, 0, w.twd - 50, 4 / 1.944, 0.25); const oMoto = ombraDir(A);
  metti(A, 0, 0, w.twd - 50, 0, 1); const alfaSbatte = A.info.alpha, kSbatte = ombraDi(A, Math.sin(ombraDir(A).dir * D2R) * H, -Math.cos(ombraDir(A).dir * D2R) * H);
  metti(A, 0, 0, w.twd - 50, 0, 0.25); A.S.capsized = true; const kScuffia = ombraDi(A, ux * H, uy * H); A.S.capsized = false;
  return { menuOmbra, twd: w.twd, tws: w.tws, alfa: A.info.alpha, porta: o.porta, dirFerma: o.dir, dirMoto: oMoto.dir, asse, lato, latoM, zero, dentro, alfaSbatte, kSbatte, kScuffia }; }"""
# scena in moto: la barca del giocatore (B) tenuta di bolina col timone degli avversari; A incollata a ogni passo a `dist` lunghezze sopra l'asse del proprio cono
# (dentro) oppure messa in modo che B le stia sottovento e avanti (fuori); `senza`: A lontana. Ritorna la velocità di B dopo 20 s e il massimo vento tolto
MOTO = """([mure, dist, caso]) => { const sv = __sv; sv.fast(0); __seed(11); sv.openItem(["r", 0]); R.ombra = true; R.t = 5; R.phase = "race";
  const me = R.boats[0], A = R.boats[1], altri = R.boats.slice(2), ai = A.ai, L = BOAT.length, dt = 1 / 60, w = windAt(0, 0), rotta = w.twd - mure * 48; me.leg = 1; me.ocs = false;
  Object.assign(S, { x: 0, y: 0, h: (rotta + 360) % 360, u: 2, vl: 0, r: 0, heel: 0, capsized: false });
  let copMax = 0, n = 0;
  const piazza = () => { altri.forEach((b, k) => { b.S.x = S.x + 600 + 80 * k; b.S.y = S.y + 600; b.S.u = 0; });
    Object.assign(A.S, { h: S.h, u: S.u, vl: S.vl, heel: S.heel, r: 0, capsized: false });
    if (caso === "senza"){ A.S.x = S.x - 600; A.S.y = S.y - 600; return; }
    const o = ombraDir(A) || { dir: w.twd + 180 };
    if (caso === "dentro"){ A.S.x = S.x - Math.sin(o.dir * D2R) * dist * L; A.S.y = S.y + Math.cos(o.dir * D2R) * dist * L; }
    else { const d = (S.h + mure * 45) * D2R; A.S.x = S.x - Math.sin(d) * dist * L; A.S.y = S.y + Math.cos(d) * dist * L; }   // fuori: B sta avanti e sottovento ad A (A è 45° a poppavia sopravento)
  };
  piazza();
  for (let t = 0; t < 30; t += dt){ muoviTimone(ctl, S, rotta, ai, dt); ctl.sheet = sheetFor(info, ai); sv.run(dt, 1); piazza(); if (t >= 10){ copMax = Math.max(copMax, me.cop || 0); n++; } }
  return { u: S.u, copMax, n, twa: Math.abs(norm180(windAt(S.x, S.y).twd - S.h)) }; }"""
TORNEO = """() => { const sv = __sv; sv.fast(0); __seed(3); window.confirm = () => true; sv.torApri(); document.getElementById("torGo").click(); sv.openItem(["r", "t"]);
  const R1 = R, tor = R.ombra, testo = R.brief.includes("cono d'ombra"); for (let k = 0; k < 60 * 20; k++) sv.run(1 / 60, 1);
  return { tor, testo, casella: !!document.getElementById("showCono"), cono: opt.cono }; }"""

async def main():
    bad = []; nv = []
    def chk(nome, ok, extra=""):
        print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
        if not ok: bad.append(nome)
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []
        async def pagina(coll=True):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME); pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(URL + ("#collaudo" if coll else "")); await pg.wait_for_timeout(250); return ctx, pg
        ctx, pg = await pagina(); f = await pg.evaluate(FERMI); await ctx.close()
        if not (f["porta"] == 1 and f["alfa"] >= 10): nv.append(f"la vela di chi copre non porta piena (incidenza {f['alfa']:.1f}°)")
        attesi = [4.8, 2.6, 2.0]; rapp = [a["lib"] / a["cop"] for a in f["asse"]]
        chk("K1 sull'asse a 0,5 / 1 / 2 altezze d'albero: spinta libera / coperta entro il 15% da 4,8 / 2,6 / 2,0 (F75)", all(abs(r / a - 1) <= 0.15 for r, a in zip(rapp, attesi)),
            "misurato %s; vento tolto %s" % (", ".join("%.2f" % r for r in rapp), ", ".join("%.0f%%" % (100 * a["k"]) for a in f["asse"])))
        lati = f["lato"] + f["latoM"]
        chk("K2 a una lunghezza di lato dall'asse la spinta è almeno il 99% della libera (4 punti, dai due lati)", len(lati) == 4 and all(a["cop"] / a["lib"] >= 0.99 for a in lati), "minimo %.3f" % min(a["cop"] / a["lib"] for a in lati))
        chk("K3 sopravento, dietro l'origine, al traverso sopravento e oltre 10 lunghezze il vento tolto è esattamente zero (6 punti); a 9,5 lunghezze c'è ancora", len(f["zero"]) == 6 and all(z == 0 for z in f["zero"]) and f["dentro"] > 0, "%s; a 9,5 lunghezze %.4f" % (f["zero"], f["dentro"]))
        giro = abs((f["dirMoto"] - f["dirFerma"] + 540) % 360 - 180)
        chk("K4 l'asse segue il vento apparente: da ferma a 4 nodi di bolina gira di almeno 10°", giro >= 10, "%.1f° (ferma %.1f°, a 4 nodi %.1f°; vento da %.0f°)" % (giro, f["dirFerma"], f["dirMoto"], f["twd"]))
        chk("K5 vela che sbatte: al massimo il 10% di vento tolto a un'altezza d'albero; scuffiata: zero", 0 < f["kSbatte"] <= 0.10 and f["kScuffia"] == 0, "sbatte %.1f%% (incidenza %.1f°), scuffiata %s" % (100 * f["kSbatte"], f["alfaSbatte"], f["kScuffia"]))
        chk("il cono è spento nelle regate del menu", f["menuOmbra"] is False)
        # K6
        dentro = []; fuori = []
        for v in range(10):
            mure = 1 if v % 2 == 0 else -1; dist = 1.3 + 0.05 * v
            ris = {}
            for caso in ("senza", "dentro", "fuori"):
                ctx, pg = await pagina(); ris[caso] = await pg.evaluate(MOTO, [mure, dist, caso]); await ctx.close()
            dentro.append((1 - ris["dentro"]["u"] / ris["senza"]["u"], ris["dentro"]["copMax"], ris["senza"]["copMax"], ris["senza"]["u"])); fuori.append((abs(1 - ris["fuori"]["u"] / ris["senza"]["u"]), ris["fuori"]["copMax"]))
        if not all(d[2] == 0 and d[3] > 1.5 for d in dentro): nv.append("K6: la corsa di confronto non è libera o la barca non cammina %s" % [(d[2], round(d[3], 2)) for d in dentro])
        chk("K6 dentro il cono a 1,3-1,75 lunghezze: almeno il 10% di velocità in meno dopo 20 s (10 varianti, almeno 9)", sum(d[0] >= 0.10 and d[1] > 0.2 for d in dentro) >= 9,
            "perdite %s; vento tolto al massimo %s" % (", ".join("%.0f%%" % (100 * d[0]) for d in dentro), ", ".join("%.0f%%" % (100 * d[1]) for d in dentro)))
        chk("K6 sottovento e avanti, fuori dal cono: meno dell'1% (10 varianti, almeno 9)", sum(x[0] < 0.01 for x in fuori) >= 9, "differenze %s; vento tolto al massimo %s" % (", ".join("%.2f%%" % (100 * x[0]) for x in fuori), ", ".join("%.0f%%" % (100 * x[1]) for x in fuori)))
        # torneo: acceso, spiegato, casella; il disegno si spegne, la fisica no
        ctx, pg = await pagina(); t = await pg.evaluate(TORNEO)
        chk("nel torneo il cono è acceso, il testo d'inizio lo spiega, la casella c'è ed è accesa", t["tor"] and t["testo"] and t["casella"] and t["cono"] is True, str(t))
        # il disegno: si contano le sfumature (createLinearGradient) create in mezzo secondo di fotogrammi; ogni cono ne crea una. Le schermate non servono: il mare si muove anche a gioco fermo
        conta = """async (acceso) => { opt.cono = acceso; const P = CanvasRenderingContext2D.prototype, vera = P.createLinearGradient; let n = 0; P.createLinearGradient = function(...a){ n++; return vera.apply(this, a); };
          await new Promise(r => setTimeout(r, 500)); P.createLinearGradient = vera; return n; }"""
        nOn = await pg.evaluate(conta, True); nOff = await pg.evaluate(conta, False); nOn2 = await pg.evaluate(conta, True)
        fis = await pg.evaluate("() => { opt.cono = false; for (let k = 0; k < 60; k++) __sv.run(1 / 60, 1); const ok = R.ombra && R.boats.every(b => typeof b.cop === 'number'); opt.cono = true; return ok; }")
        chk("K14 la casella nasconde il disegno (coni disegnati in mezzo secondo: accesa molti, spenta nessuno in più del resto) ma la fisica resta", nOn > nOff + 10 and nOn2 > nOff + 10 and fis, "accesa %d e %d, spenta %d; fisica %s" % (nOn, nOn2, nOff, fis)); await ctx.close()
        # finestra delle impostazioni a 1360x650: nel torneo la casella c'è e niente sfora; nella regata del menu e in navigazione libera la casella non c'è
        ECC = """() => { const d = document.getElementById('setDlg'), r = d.getBoundingClientRect(), p = document.querySelector('.panel');
          return { dialogo: Math.max(0, Math.ceil(r.bottom - innerHeight)) + Math.max(0, d.scrollHeight - d.clientHeight), pannello: p.scrollHeight - p.clientHeight, casella: document.getElementById('conoRiga').offsetParent !== null }; }"""
        fin = {}
        for nome, apri in (("torneo", "() => { __sv.fast(0); window.confirm = () => true; __sv.torApri(); document.getElementById('torGo').click(); __sv.openItem(['r', 't']); }"), ("regata del menu", "() => { __sv.fast(0); __sv.openItem(['r', 0]); }"), ("navigazione libera", "() => { __sv.fast(0); __sv.openItem('free'); }")):
            ctx, pg = await pagina(); await pg.evaluate(apri); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(150)
            await pg.evaluate("() => document.getElementById('openSet').click()"); await pg.wait_for_timeout(150); fin[nome] = await pg.evaluate(ECC); await ctx.close()
        chk("K14 finestra delle impostazioni a 1360x650: nel torneo c'è la casella del cono e niente sfora; nella regata del menu e in navigazione libera la casella non c'è e niente sfora",
            fin["torneo"] == {"dialogo": 0, "pannello": 0, "casella": True} and all(fin[k] == {"dialogo": 0, "pannello": 0, "casella": False} for k in ("regata del menu", "navigazione libera")), str(fin))
        # pagina vera, senza #collaudo: il torneo si apre dal menu, nessun errore
        ctx, pg = await pagina(False)
        vera = await pg.evaluate("""() => { const b = [...document.querySelectorAll("#menu button.item")].find(x => /Torneo/.test(x.textContent)); if (!b) return { menu: false }; b.click(); const go = document.getElementById("torGo"); if (go) go.click();
          return { menu: true, casella: !!document.getElementById("showCono") }; }""")
        await pg.wait_for_timeout(1500); vera["ombra"] = await pg.evaluate("() => typeof R !== 'undefined' && !!R && R.ombra === true"); await ctx.close()
        chk("K14 pagina senza #collaudo: il torneo si apre dal menu col cono acceso", vera.get("menu") and vera.get("casella") and vera.get("ombra"), str(vera))
        chk("nessun errore della pagina", not errs, str(errs[:2])); await b.close()
    if nv: print("ESITO: NON VALIDO: " + "; ".join(nv)); sys.exit(2)
    print("casi sbagliati: " + (str(bad) if bad else "nessuno")); print("ESITO: " + ("FALLITO" if bad else "OK")); sys.exit(1 if bad else 0)
asyncio.run(main())
