# La barca che balla sull'onda (1.0.23, docs/archivio/PROPOSTA-MOTO-SUL-MARE.md): solo disegno, il motore non la vede.
# Pagina vera con #collaudo, ciclo del browser fermo, passi di 1/60 s: navigazione libera, prua tenuta fissa a 45° / 90° / 135° / 180° dal vento,
# con 0 e 10 nodi, 5 punti di partenza diversi (fase dell'onda diversa), 25 s ciascuno (i primi 5 non contano). Ogni due passi si disegna il quadro
# e si legge dove il disegno ha messo la testa d'albero (geo.hx di lato, geo.hY avanti e indietro), in pixel a zoom 1.
# Di lato si toglie la parte dovuta allo sbandamento vero (lo stesso conto del disegno, dallo stato del motore): senza, il metro misurava anche la fisica
# (primo giro: 1,1 px senza vento e fino a 25,7 px in poppa quando il boma cambia lato).
# Criteri (soglie dichiarate nella proposta, prima di misurare): con 10 nodi la testa d'albero oscilla di almeno 4 px a ogni andatura, con 0 nodi 0 px;
# al traverso il rollio (di lato) e almeno il doppio del beccheggio; in poppa il beccheggio e almeno il doppio del rollio;
# di bolina il periodo d'incontro e piu corto che in poppa. Tolto dopo il primo giro, e dichiarato (docs/archivio/PROPOSTA-MOTO-SUL-MARE.md §6): «di bolina il
# beccheggio e almeno il doppio del rollio», sbagliato in partenza perche di bolina le onde arrivano a 45° dalla prua e i due vengono uguali.
# NON VALIDO se ha disegnato meno quadri del previsto o se la pagina da errori.
# Uso: python collaudo_moto_mare.py
import asyncio, pathlib, sys, statistics
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
MISURA = """([kn, rel, k]) => {
  __sv.openItem('free'); __sv.fast(0); env.twd = 0; env.tws = kn / KN;
  S.x = 37 * k; S.y = -23 * k; S.h = rel; S.u = 1.5;
  const hx = [], hy = []; let ppm = 0;
  for (let n = 0; n < 1500; n++){
    S.h = rel; S.r = 0; __sv.run(1 / 60, 1);
    if (n >= 300 && n % 2 === 0){ __sv.draw(1 / 60); ppm = view().ppm; hx.push((geo.hx - S.boomSide * 5.5 * Math.sin(clamp(S.heel, -40, 70) * D2R)) * ppm); hy.push(geo.hY * ppm); }
  }
  return { hx, hy };
}"""
ANDATURE = {45: "bolina", 90: "traverso", 135: "lasco", 180: "poppa"}

def periodo(v):  # secondi fra due passaggi per la media nello stesso verso
    m = statistics.fmean(v); c = sum(1 for a, b in zip(v, v[1:]) if (a - m) * (b - m) < 0)
    return 2 * len(v) / 30 / c if c else float("inf")

async def main():
    errs, quadri, ris = [], 0, {}
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script("window.requestAnimationFrame = () => 0;")
        await pg.goto(URL); await pg.wait_for_timeout(500)
        for kn in (0, 10):
            for rel in ANDATURE:
                r = []
                for k in range(5):
                    o = await pg.evaluate(MISURA, [kn, rel, k]); quadri += len(o["hx"])
                    r.append((max(o["hx"]) - min(o["hx"]), max(o["hy"]) - min(o["hy"]), periodo(o["hy"] if rel != 90 else o["hx"])))
                ris[kn, rel] = r
        await b.close()
    for (kn, rel), r in ris.items():
        print(f"{kn:2d} nodi, {ANDATURE[rel]:8s}: di lato {min(x[0] for x in r):.1f}-{max(x[0] for x in r):.1f} px, avanti e indietro {min(x[1] for x in r):.1f}-{max(x[1] for x in r):.1f} px, periodo d'incontro {statistics.median(x[2] for x in r):.2f} s")
    print(f"quadri disegnati e misurati: {quadri} (attesi {2 * 4 * 5 * 600}); errori della pagina: {errs[:1]}")
    if errs or quadri != 2 * 4 * 5 * 600: print("ESITO: NON VALIDO"); sys.exit(2)
    sb = []
    for rel in ANDATURE:
        if min(max(x[0], x[1]) for x in ris[10, rel]) < 4: sb.append(f"{ANDATURE[rel]} con 10 nodi: meno di 4 px")
        if max(max(x[0], x[1]) for x in ris[0, rel]) > 0.05: sb.append(f"{ANDATURE[rel]} senza vento: si muove")
    if any(x[0] < 2 * x[1] for x in ris[10, 90]): sb.append("traverso: rollio meno del doppio del beccheggio")
    if any(x[1] < 2 * x[0] for x in ris[10, 180]): sb.append("poppa: beccheggio meno del doppio del rollio")
    if statistics.median(x[2] for x in ris[10, 45]) >= statistics.median(x[2] for x in ris[10, 180]): sb.append("periodo di bolina non piu corto che in poppa")
    print("ESITO: " + ("OK" if not sb else "FALLITO (" + "; ".join(sb) + ")")); sys.exit(1 if sb else 0)

asyncio.run(main())
