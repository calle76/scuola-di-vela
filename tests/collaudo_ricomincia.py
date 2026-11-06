# «Ricomincia» nelle lezioni, scritte sulla barca e testo della prova 2 (1.2.13, segnalazioni di Ale giocando la Scuola, 6 novembre 2026).
# Criteri, scritti prima della correzione:
#  R1 in tutti i passi pratici delle lezioni, dopo Ricomincia e a mani ferme, il passo NON si completa in 60 s (semi 1-3). Prima: 5 passi si completavano da soli.
#  R2 i passi corretti si completano guidando dopo Ricomincia, 5 semi su 5 (se no R1 sarebbe vero anche con un passo impossibile).
#  R3 nei passi con le scritte sulla barca nessuna scritta si sovrappone a un'altra; contate le scritte disegnate, per non passare con zero casi.
#  R4 il testo della prova 2 dice che la strambata serve, e dà lo stesso 45° della lezione 6.
# Uso: BROWSER=firefox python collaudo_ricomincia.py
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
# I passi corretti: indice in LESSONS, passo, titolo, angolo voluto col vento, scotta
GUIDATI = [(0, 9, "Ripartire", 90, None), (0, 11, "La scotta: cazzare", None, "auto"), (2, 3, "Traverso", 90, None),
           (2, 10, "Filetto sottovento", None, 0), (2, 12, "Orzi e cazzi", 60, "auto")]
R1 = """() => { const sv = __sv, out = []; let n = 0;
  for (let l = 0; l < 40; l++) { for (let k = 0; k < 40; k++) { let fermo = false, tit = null, esiti = [];
    for (const seme of [1, 2, 3]) { __seed(seme); sv.fast(0);
      try { sv.openItem(["l", l]); sv.showStep(k); } catch (e) { fermo = true; break; }
      const btn = document.getElementById("lRetry"); if (!btn || btn.hidden) { fermo = true; break; }
      tit = document.getElementById("lTitle").textContent; btn.click();
      let t = 0; while (t < 60 * 60 && !sv.stepDone) { sv.run(1 / 60, 1); t++; }
      esiti.push(sv.stepDone ? +(t / 60).toFixed(1) : null); }
    if (fermo) continue; n++;
    if (esiti.some(x => x !== null)) out.push([l, k + 1, tit, esiti]); } }
  return { passi: n, fatti: out }; }"""
R2 = """([l, k, twa, scotta, seme]) => { const sv = __sv, D = Math.PI / 180, nn = a => ((a + 180) % 360 + 360) % 360 - 180;
  __seed(seme); sv.fast(0); sv.openItem(["l", l]); sv.showStep(k - 1); document.getElementById("lRetry").click();
  const lato = Math.sign(nn(sv.S.h - sv.twd)) || 1; let t = 0;
  while (t < 90 * 60 && !sv.stepDone) { const S = sv.S;
    if (t % 6 === 0) {
      if (twa !== null) { const err = nn(S.h - (sv.twd + lato * twa)); sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1); }
      if (scotta === "auto") sv.ctl.sheet = sv.autoSheet(); else if (scotta !== null) sv.ctl.sheet = scotta; }
    sv.run(1 / 60, 1); t++; }
  return sv.stepDone; }"""
# R3 legge i rettangoli delle scritte dai fotogrammi veri del gioco, a telecamera ferma: con sv.frame o sv.draw da soli il boma non è dove lo vede il giocatore,
# e il controllo non vedeva la sovrapposizione che si vede nella fotografia (provato il 6 novembre 2026).
R3_PASSI = [[0,1],[0,2],[0,3],[0,4],[0,6],[1,1],[2,6],[2,7]]
R3_AGGANCIA = """() => { const C = CanvasRenderingContext2D.prototype, fr = C.fillRect; window.__rq = [];
  C.fillRect = function (x, y, w, h) { if (String(this.fillStyle).replace(/\\s/g, "").includes("10,24,36")) __rq.push([x, y, w, h]); return fr.call(this, x, y, w, h); }; __sv.fast(1); }"""
R3_LEGGI = """(n) => { const R = __rq.slice(-n); let k = 0; for (let a = 0; a < R.length; a++) for (let b = a + 1; b < R.length; b++) { const p = R[a], q = R[b];
  if (p[0] < q[0] + q[2] && q[0] < p[0] + p[2] && p[1] < q[1] + q[3] && q[1] < p[1] + p[3]) k++; } return k; }"""
R3_N = {(0,1):2,(0,2):3,(0,3):3,(0,4):3,(0,6):3,(1,1):2,(2,6):2,(2,7):1}
async def main():
    nome = os.environ.get("BROWSER", "chromium"); fall = []
    async with async_playwright() as p:
        b = await getattr(p, nome).launch(); errs = []
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(300)
        r = await pg.evaluate(R1)
        print(f"R1 passi provati {r['passi']}, completati a mani ferme {len(r['fatti'])}: {r['fatti']}")
        if r["passi"] < 40 or r["fatti"]: fall.append("R1")
        for l, k, tit, twa, sc in GUIDATI:
            es = [await pg.evaluate(R2, [l, k, twa, sc, s]) for s in range(1, 6)]
            print(f"R2 {tit}: completato guidando {sum(es)} su 5")
            if not all(es): fall.append("R2 " + tit)
        await pg.evaluate(R3_AGGANCIA); sov = []; scritte = 0
        for l, k in R3_PASSI:
            await pg.evaluate("([l, k]) => { __sv.openItem(['l', l]); __sv.showStep(k - 1); __rq.length = 0; }", [l, k]); await pg.wait_for_timeout(2500)
            n = R3_N[(l, k)]; viste = await pg.evaluate("() => __rq.length")
            if viste >= n: scritte += n
            if await pg.evaluate(R3_LEGGI, n): sov.append([l, k + 0])
        print(f"R3 passi {len(R3_PASSI)}, scritte {scritte}, sovrapposte {sov}")
        if scritte != sum(R3_N.values()) or sov: fall.append("R3")
        sorg = (pathlib.Path(__file__).resolve().parent.parent / "js" / "contenuti.js").read_text(encoding="utf-8")
        riga = next(x for x in sorg.splitlines() if "L'arrivo è sottovento" in x)
        ok = "serve" in riga and "45°" in riga and "tutta la vela" not in riga
        print("R4 testo della prova 2:", "ok" if ok else riga.strip()[:200])
        if not ok: fall.append("R4")
        print("errori:", errs); await b.close()
        if errs: fall.append("errori")
    print("ESITO", nome, "OK" if not fall else "FALLITO: " + ", ".join(fall)); sys.exit(1 if fall else 0)
asyncio.run(main())
