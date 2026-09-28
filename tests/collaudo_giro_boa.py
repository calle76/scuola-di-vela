# Guida la barca con un pilota automatico (barra e scotta, come un giocatore) nelle prove 4 e 5
# e verifica il giro di boa: dal lato giusto la boa conta, dal lato sbagliato no finché non si rimedia.
# Uso: python collaudo_giro_boa.py [casi]   (a sinistra, b a dritta, c sbaglia e rimedia, d triangolo; e triangolo con la boa 2 a dritta, f prove 1-3; predefinito abcdef)
import asyncio, pathlib
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"

PILOTA = """
(plan) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  // piano: elenco di [indice boa, angoli attorno alla boa da toccare a 13 m] oppure "arrivo"
  const pts = [];
  for (const [k, angs] of plan) {
    const m = sv.marks[k];
    for (const a of angs) { const b = (m.out + a) * D; pts.push({ x: m.x + Math.sin(b) * 13, y: m.y - Math.cos(b) * 13 }); }
  }
  const last = sv.marks[sv.marks.length - 1]; pts.push({ x: last.x, y: last.y });
  const log = []; let i = 0, side = 1, lastToast = null;
  window.__pil = setInterval(() => {
    const S = sv.S; if (S.finished || i >= pts.length){ window.__pilDone = (window.__pilDone || 0) + 1; return; }
    if (sv.toast && sv.toast !== lastToast) { lastToast = sv.toast; log.push([Math.round(S.time), sv.toast, S.markIdx, S.rnd || 0]); }
    const p = pts[i]; if (Math.hypot(p.x - S.x, p.y - S.y) < 7) { i++; return; }
    const brg = Math.atan2(p.x - S.x, -(p.y - S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg;
    if (Math.abs(rel) < 52) { if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; } // bolina a bordi
    const cur = n180(S.h - sv.twd);
    if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95; // piantato nel vento: poggia e riprendi velocità
    const err = n180(S.h - want);
    sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1); // all'indietro la barra funziona al contrario
    sv.ctl.sheet = Math.abs(cur) > 150 ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet(); // prima di strambare si cazza
    if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" }));  // raddrizza come il giocatore (tasto R)
  }, 25);
  window.__pilLog = log; window.__pilDone = 0;
}
"""

async def prova(pg, idx, plan, nome):
    await pg.evaluate(f"__sv.startMission({idx}, 0)")   # vento da nord: coordinate semplici
    await pg.evaluate("__sv.fast(8)")
    await pg.evaluate(PILOTA, plan)
    for _ in range(150):
        await pg.wait_for_timeout(1000)
        if await pg.evaluate("__sv.S.finished || window.__pilDone > 80"): break
    r = await pg.evaluate("[__sv.S.finished, Math.round(__sv.S.time), __sv.S.markIdx, __sv.S.wrongMarks||0, __pilLog, __sv.S.capsizes, [Math.round(__sv.S.x), Math.round(__sv.S.y), Math.round(__sv.S.h), +__sv.S.u.toFixed(1)], window.__pilDone]")
    await pg.evaluate("clearInterval(window.__pil)")
    print(f"prova {idx+1}, {nome}: finita={r[0]} tempo={r[1]} s boe girate={r[2]} giri sbagliati={r[3]} scuffie={r[5]} posizione finale={r[6]} fine pilota={r[7]}")
    for t, msg, mi, rnd in r[4]: print(f"    {t:4d} s  boa {mi}  conto {rnd:+d}  «{msg}»")
    return r

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 800})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        giusto = [60, 0, -60]          # attorno alla boa in senso antiorario: lasciata a sinistra
        sbagliato = [-60, 0, 60]       # in senso orario: lasciata a dritta
        rimedio = [-60, 0, 60, 0, -60, -120, 180, 120, 60, 0, -60]  # sbaglia, torna indietro, poi gira dal lato giusto
        import sys
        casi = sys.argv[1] if len(sys.argv) > 1 else "abcdef"
        if "a" in casi: await prova(pg, 3, [[0, giusto]], "boa a sinistra")
        if "b" in casi: await prova(pg, 3, [[0, sbagliato]], "boa a dritta (deve NON finire)")
        if "c" in casi: await prova(pg, 3, [[0, rimedio]], "sbaglia e rimedia")
        if "d" in casi: await prova(pg, 4, [[0, giusto], [1, giusto]], "triangolo, boe a sinistra")
        if "f" in casi:  # prove 1-3: la boa si raggiunge soltanto, come prima
            for k in range(3): await prova(pg, k, [], "boa da raggiungere")
        if "e" in casi: await prova(pg, 4, [[0, giusto], [1, sbagliato]], "triangolo, boa 2 a dritta (deve NON finire)")
        await pg.screenshot(path=str(OUT / "giro_boa.png"))
        print("errori:", errs); await b.close()
if __name__ == "__main__":
    asyncio.run(main())
