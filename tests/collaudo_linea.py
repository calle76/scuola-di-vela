# Linea d'arrivo delle prove (0.19).
# Parte 1 (#collaudo): 5 prove x 8 venti. La barca viene messa vicino alla linea d'arrivo e poi naviga davvero
# (fisica del gioco, passi fissi di 1/60 s con __sv.run). La geometria della linea (centro sull'ultima voce di marks,
# perpendicolare all'ultimo lato, 12 m per lato) la ricalcola il collaudo per conto suo, senza leggere i campi del gioco.
# Casi: taglio dal lato giusto; taglio al contrario; fuori dagli estremi (messaggio, poi rientro e arrivo); sopra una boa
# (appena dentro l'estremo); appena fuori dall'estremo; prove 4 e 5 prima del giro di boa. Nel taglio giusto il tempo
# d'arrivo deve essere l'istante interpolato del taglio.
# Parte 2 (pagina vera, senza #collaudo): dati vecchi delle prove cancellati al primo avvio con il messaggio una volta sola;
# prova 1 aperta dal menu, la scritta «Arrivo» viene disegnata.
# Parte 3 (0.20.2, #collaudo): lezione 5 passo 5 «Risalire il vento», arrivo a linea 110 m controvento dal punto in cui comincia il passo.
# Un pilota bordeggia davvero (passi fissi) da 10 punti di partenza (5 spostamenti laterali x 2 mure) verso un punto oltre la linea;
# il collaudo ricalcola la linea per conto suo (centro 110 m a nord della barca a inizio passo, perpendicolare al vento, 12 m per lato).
# Casi: dentro (passo completato al taglio, fra gli estremi); fuori (punta 25 m di lato: niente, messaggio, poi rientra e completa);
# contrario (da oltre la linea verso sud: niente).
# Uso: python collaudo_linea.py [file html]   (predefinito: index.html del progetto). Esce con 1 se un caso è sbagliato
# o se un tipo di caso ha zero misure.
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
HTML = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html"
BASE = HTML.as_uri()
HALF = 12  # metà larghezza della linea, m

CASO = """
([i, w, kind, HALF]) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180, dt = 1 / 60;
  sv.startMission(i, w); sv.fast(0);
  const S = sv.S, M = sv.marks, L = M[M.length - 1], P = M.length > 1 ? M[M.length - 2] : { x: S.x, y: S.y };
  const fd = Math.hypot(L.x - P.x, L.y - P.y), nx = (L.x - P.x) / fd, ny = (L.y - P.y) / fd, tx = -ny, ty = nx;
  const dOf = (x, y) => (x - L.x) * nx + (y - L.y) * ny, aOf = (x, y) => (x - L.x) * tx + (y - L.y) * ty;
  if (kind !== "prima") S.markIdx = M.length - 1;   // direttamente all'ultimo lato
  // a 3 m e non 6: nella prova 3 la rotta a 60° dal vento sposta di lato la barca di circa 1,7 m per metro avanzato
  const [d0, a0, dir] = { giusto: [-3, 0, 1], contrario: [6, 0, -1], fuori: [-6, 20, 1], boa: [-0.05, 11.9, 1], oltre: [-0.05, 12.15, 1], prima: [-3, 0, 1] }[kind];
  const lancia = (d, a) => {   // rotta lungo dir*n, ma ad almeno 60° dal vento; barca lanciata a 2,5 m/s, barra al centro
    let h = Math.atan2(dir * nx, -dir * ny) / D; const rel = n180(h - sv.twd);
    if (Math.abs(rel) < 60) h = sv.twd + (rel >= 0 ? 60 : -60);
    S.h = (h + 360) % 360; S.u = 2.5; S.r = 0; sv.ctl.tiller = 0; sv.ctl.sheet = sv.autoSheet();
    S.x = L.x + nx * d + tx * a; S.y = L.y + ny * d + ty * a;
  };
  const corri = (passi) => {   // primo attraversamento della linea (in un verso o nell'altro), più 60 passi dopo
    let x = null, dopo = 0;
    for (let k = 0; k < passi && !S.finished; k++) {
      const x0 = S.x, y0 = S.y, t0 = S.time; sv.run(dt, 1);
      const p = dOf(x0, y0), q = dOf(S.x, S.y);
      if (!x && ((p < 0 && q >= 0) || (p > 0 && q <= 0))) {
        const f = p / (p - q);
        x = { verso: p < 0 ? 1 : -1, f, a: aOf(x0 + (S.x - x0) * f, y0 + (S.y - y0) * f), fin: S.finished, scarto: S.finished ? Math.abs(S.time - (t0 + f * dt)) : null, toast: sv.toast };
      }
      if (x && ++dopo > 60) break;
    }
    return x;
  };
  lancia(d0, a0);
  const x = corri(1200);
  const r = { x, fin: S.finished, markIdx: S.markIdx, reg: Object.entries(sv.reg).filter(([k, v]) => k !== "ironsSec" && v).length };
  if (kind === "fuori" && x && !S.finished) { lancia(-6, 0); r.rientro = corri(1200); r.fin2 = S.finished; }
  return r;
}
"""

async def parte1(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(400)
    tipi = ["giusto", "contrario", "fuori", "boa", "oltre", "prima"]
    conta = {t: 0 for t in tipi}; sbagli = []; scarti = []; lati = []
    for i in range(5):
        for w in range(0, 360, 45):
            for kind in tipi:
                if kind == "prima" and i < 3: continue
                r = await pg.evaluate(CASO, [i, w, kind, HALF]); x = r["x"]
                caso = f"prova {i+1} vento {w} {kind}"
                if not x: sbagli.append(caso + ": la barca non ha attraversato la linea (caso non misurato)"); continue
                a = abs(x["a"]); ok = True
                if kind == "giusto":
                    ok = x["verso"] == 1 and a <= HALF and x["fin"] and x["scarto"] is not None and x["scarto"] < 1e-9
                    if x["scarto"] is not None: scarti.append(x["scarto"])
                elif kind == "contrario": ok = x["verso"] == -1 and not r["fin"]
                elif kind == "fuori": ok = x["verso"] == 1 and a > HALF and not x["fin"] and "Fuori dalla linea" in (x["toast"] or "") and r.get("fin2") is True
                elif kind == "boa":
                    if not (HALF - 0.5 < a <= HALF): sbagli.append(f"{caso}: taglio a {a:.3f} m dal centro, non sopra la boa (caso non misurato)"); continue
                    ok = x["verso"] == 1 and x["fin"] and r["reg"] == 0; lati.append(a)
                elif kind == "oltre":
                    if not (HALF < a < HALF + 0.5): sbagli.append(f"{caso}: taglio a {a:.3f} m dal centro, non appena fuori (caso non misurato)"); continue
                    ok = x["verso"] == 1 and not r["fin"]; lati.append(a)
                elif kind == "prima": ok = x["verso"] == 1 and a <= HALF and not r["fin"] and r["markIdx"] == 0
                conta[kind] += 1
                if not ok: sbagli.append(f"{caso}: {json.dumps(r)}")
    await pg.close()
    print("parte 1, casi misurati per tipo:", conta)
    if scarti: print(f"  tempo interpolato: scarto massimo {max(scarti):.2e} s su {len(scarti)} arrivi")
    if lati: print(f"  tagli vicino a una boa: da {min(lati):.3f} a {max(lati):.3f} m dal centro (estremo a {HALF} m)")
    return conta, sbagli, errs

CASO5 = """
([dx, mura, kind, HALF]) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180, dt = 1 / 60;
  sv.openItem(['l', 4]); sv.fast(0);
  for (let k = 0; k < 9; k++){ sv.showStep(k); if (document.getElementById('lTitle').textContent === "Risalire il vento") break; }
  const S = sv.S, cx = S.x, cy = S.y - 110;                       // linea ricalcolata dal collaudo, vento da nord nelle lezioni
  const dOf = (x, y) => cy - y, aOf = x => x - cx;               // d: metri oltre la linea verso nord; a: di lato dal centro
  S.x = cx + dx; S.y = kind === "contrario" ? cy - 20 : cy + 110;
  S.h = kind === "contrario" ? 180 : (sv.twd + mura * 55 + 360) % 360; S.u = 2.5; S.r = 0; sv.ctl.tiller = 0; sv.ctl.sheet = sv.autoSheet();
  let mira = [cx + (kind === "fuori" ? 25 * mura : 0), kind === "contrario" ? cy + 40 : cy - 15], side = mura, x = null, fin2 = null, toast = "", tacks0 = S.tacks;
  for (let k = 0; k < 600 / dt; k++){
    const brg = Math.atan2(mira[0] - S.x, -(mira[1] - S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg;
    if (Math.abs(rel) < 52){ if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; }
    const cur = n180(S.h - sv.twd);
    if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
    sv.ctl.tiller = Math.max(-1, Math.min(1, n180(S.h - want) / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1); sv.ctl.sheet = sv.autoSheet();
    const x0 = S.x, y0 = S.y; sv.run(dt, 1);
    if (sv.toast && sv.toast.includes("Fuori dalla linea")) toast = sv.toast;
    const p = dOf(x0, y0), q = dOf(S.x, S.y);
    if (!x && ((p < 0 && q >= 0) || (p > 0 && q <= 0))){
      const f = p / (p - q); x = { verso: p < 0 ? 1 : -1, a: aOf(x0 + (S.x - x0) * f), fin: sv.S.markReached, toast: sv.toast };
      if (kind === "fuori"){ mira = [cx, cy + 30]; }                // dopo il taglio fuori torna sotto la linea e poi la ritaglia al centro
      else if (kind !== "contrario"){ for (let j = 0; j < 30; j++) sv.run(dt, 1); break; }
      else break;
    }
    if (kind === "fuori" && x && mira[1] > cy && Math.hypot(S.x - mira[0], S.y - mira[1]) < 8) mira = [cx, cy - 15];
    if (kind === "fuori" && x && sv.stepDone){ fin2 = true; break; }
  }
  return { x, fin: sv.S.markReached, fatto: sv.stepDone, fin2, toast, virate: S.tacks - tacks0 };
}
"""

async def parte3(b):
    pg = await b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
    conta = {"dentro": 0, "fuori": 0, "contrario": 0}; sbagli = []
    for kind in conta:
        for dx in ((-60, -30, 0, 30, 60) if kind == "dentro" else (0, 30)):
            for mura in (1, -1):
                r = await pg.evaluate(CASO5, [dx, mura, kind, HALF]); x = r["x"]
                caso = f"lezione 5 passo 5 {kind}, partenza {dx:+d} m mure {'+' if mura > 0 else '-'}"
                if not x: sbagli.append(caso + ": la barca non ha attraversato la linea (caso non misurato) " + json.dumps(r)); continue
                a = abs(x["a"])
                if kind == "dentro": ok = x["verso"] == 1 and a <= HALF and x["fin"] and r["fatto"] and r["virate"] >= 1
                elif kind == "fuori": ok = x["verso"] == 1 and a > HALF and not x["fin"] and "Fuori dalla linea" in r["toast"] and r["fin2"] is True
                else: ok = x["verso"] == -1 and not r["fin"] and not r["fatto"]
                conta[kind] += 1
                print(f"  {caso}: taglio a {x['a']:+.1f} m dal centro, verso {x['verso']:+d}, virate {r['virate']}, completato {r['fatto']}", flush=True)
                if not ok: sbagli.append(f"{caso}: {json.dumps(r)}")
    await pg.close()
    print("parte 3, casi misurati per tipo:", conta)
    return conta, sbagli, errs

FILLTEXT = """(() => { window.__testi = []; const f = CanvasRenderingContext2D.prototype.fillText;
  CanvasRenderingContext2D.prototype.fillText = function(t, ...a){ if (window.__testi.length < 5000) window.__testi.push(String(t)); return f.call(this, t, ...a); }; })();"""
VECCHI = {"done": {"m0": True, "m3": True}, "best": {"m0": 80, "m1": 130, "m3.2": 300, "m4.3": 340, "r0.2": 200}, "clean": {"m0": True, "m4.3": True, "r0.2": True}}

async def parte2(b):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(FILLTEXT)
    await pg.goto(BASE); await pg.wait_for_timeout(400)
    await pg.evaluate(f"""localStorage.setItem("scuolaVelaSim.v1", JSON.stringify({json.dumps(VECCHI)}));
      localStorage.setItem("scuolaVelaGhost.v1", JSON.stringify({{ m0: {{ s: [] }}, "m4.3": {{ s: [] }}, "r0.2b": {{ s: [] }} }}))""")
    await pg.reload(); await pg.wait_for_timeout(600)
    MSG = "Le prove sono cambiate: i tempi salvati sono stati azzerati"
    v = {}
    v["aggancio assente"] = await pg.evaluate("typeof window.__sv === 'undefined'")
    v["messaggio al primo avvio"] = MSG in await pg.inner_text("#menu")
    p = json.loads(await pg.evaluate("localStorage.getItem('scuolaVelaSim.v1')")); g = json.loads(await pg.evaluate("localStorage.getItem('scuolaVelaGhost.v1')"))
    v["record, stelle e fantasmi vecchi delle prove cancellati"] = not any(k in p["best"] or k in p["clean"] or k in g for k in ["m0", "m1", "m3.2", "m4.3"])
    v["regate e completamenti conservati"] = p["best"].get("r0.2") == 200 and p["clean"].get("r0.2") is True and "r0.2b" in g and p["done"].get("m0") is True
    await pg.click("button.item[data-k='3']"); await pg.wait_for_timeout(500)   # Prova 1 nella sequenza della Scuola
    v["riquadro delle istruzioni aperto"] = await pg.is_visible("#bGo")
    await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
    testi = await pg.evaluate("window.__testi")
    v["scritta «Arrivo» disegnata"] = "Arrivo" in testi
    await pg.click("#toMenu"); await pg.wait_for_timeout(400)
    v["messaggio non ripetuto tornando al menu"] = MSG not in await pg.inner_text("#menu")
    await pg.reload(); await pg.wait_for_timeout(600)
    v["messaggio non ripetuto ricaricando la pagina"] = MSG not in await pg.inner_text("#menu")
    await pg.close()
    print("parte 2, pagina senza #collaudo:")
    for k, ok in v.items(): print(f"  {'OK ' if ok else 'NO '} {k}")
    return v, errs

async def main():
    print("file:", HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        conta, sbagli, e1 = await parte1(b)
        v, e2 = await parte2(b)
        c3, s3, e3 = await parte3(b)
        conta.update({"lezione 5 " + k: n for k, n in c3.items()}); sbagli += s3; e2 += e3
        await b.close()
    zero = [k for k, n in conta.items() if n == 0]
    for s in sbagli[:20]: print("  SBAGLIATO:", s)
    if len(sbagli) > 20: print(f"  ... e altri {len(sbagli) - 20}")
    print("errori della pagina:", e1 + e2)
    ok = not sbagli and not zero and all(v.values()) and not (e1 + e2)
    print(f"casi misurati: {sum(conta.values())}; sbagliati: {len(sbagli)}; tipi con zero casi: {zero or 'nessuno'}; verifiche pagina vera: {sum(v.values())} su {len(v)}")
    print("esito:", "tutto OK" if ok else "FALLITO")
    sys.exit(0 if ok else 1)

asyncio.run(main())
