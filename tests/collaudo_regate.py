# Fa correre regate e verifica che tutti gli avversari partano, girino la boa e arrivino.
# Dal 13 ottobre 2026 a passi fissi e con seme fisso, come collaudo_partenze.py («anticipi allo sparo»): ogni corsa gira tutta
# dentro una sola chiamata alla pagina (Math.random a seme fisso, simTime a zero, regata riavviata, passi di 1/60 s con __sv.run),
# quindi lo stesso seme dà la stessa regata su qualunque computer e con qualunque carico. Prima girava in tempo reale accelerato
# (__sv.fast(25), al massimo 24 s reali): la mediana d'arrivo cambiava di circa 20 s da un giro all'altro sullo stesso codice.
# Limite di una corsa: 600 s simulati dal riavvio (preparazione compresa), l'equivalente dei 24 s reali × 25 di prima.
# Uso: python collaudo_regate.py <numero di corse> <0 = a bastone, 1 = nelle raffiche> [--lungo]
#   semi 1..N; con --lungo i semi 7-30 (conferma, mai guardati nella scelta), ignorando N
import asyncio, sys, statistics
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
LUNGO = "--lungo" in sys.argv; ARG = [a for a in sys.argv[1:] if a != "--lungo"]
LIMITE = 600   # secondi simulati per corsa
CORSA = """([seme, limite]) => {
  const sv = __sv, cd = document.getElementById('cdSel');
  sv.fast(0);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; cd.dispatchEvent(new Event('change'));            // riavvia la regata con il seme appena fissato
  const R = sv.R, ai = () => R.boats.filter(b => !b.me);
  let n = 0;
  while (n < limite * 60 && !ai().every(b => b.fin !== null)){ sv.run(1/60, 1); n++; }
  return [Math.round(R.t), ai().map(b => [b.name, b.fin === null ? 'BLOCCATA tratto ' + b.leg : Math.round(b.fin), b.pen])];
}"""
async def main(semi, race):
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        arrivi = []; bloccate = 0; errori = []
        print(f"regata {race + 1}: semi {semi[0]}-{semi[-1]}, passi fissi di 1/60 s, al massimo {LIMITE} s simulati per corsa", flush=True)
        for seme in semi:
            pg = await b.new_page(viewport={"width":1280,"height":800})
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.click("[data-r='%d']" % race); await pg.wait_for_timeout(200)
            t, barche = await pg.evaluate(CORSA, [seme, LIMITE])
            line = f"regata {race+1} seme {seme}: t={t} {barche} errori={errs[:1]}"
            print(line, flush=True); open(OUT / "race_results.txt","a").write(line+"\n")
            for _, fin, _ in barche:
                if isinstance(fin, str): bloccate += 1
                else: arrivi.append(fin)
            errori += errs[:1]
            await pg.close()
        await b.close()
        print(f"riepilogo regata {race+1}: corse {len(semi)}, arrivi di avversari {len(arrivi)} su {3 * len(semi)}, BLOCCATA {bloccate}"
              + (f", mediana d'arrivo {statistics.median(arrivi):.1f} s (minimo {min(arrivi)}, massimo {max(arrivi)})" if arrivi else "")
              + f"; errori della pagina {errori[:1]}", flush=True)
semi = list(range(7, 31)) if LUNGO else list(range(1, int(ARG[0]) + 1))
asyncio.run(main(semi, int(ARG[1])))
