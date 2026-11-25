# Voce 2 (25 nov 2026, docs/PROPOSTA-AVVERSARI-BOLINA.md §16): dove perdono tempo i rivali nelle regate LUNGHE del torneo. La corsa è quella di misura_avversari_rotta.py
# (rivali contro la rotta ottimale partita da dove e quando hanno cominciato il lato), con __sv.lungo, 3 regate, una pagina nuova per regata, righe JSON riprese da --righe.
# Uso: python tests/misura_rivali_lunghe.py --semi 4501-4520 --righe file.jsonl  (BROWSER=firefox, RADICE=copia); riepilogo: --conta file.jsonl
import asyncio, json, os, pathlib, statistics, sys, time
QUI = pathlib.Path(__file__).resolve().parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
med = statistics.median

def riepilogo(f):
    R = [json.loads(x) for x in open(f)]; print(f"{len(R)} regate, {sum(len(r['barche']) for r in R)} rivali, errori {sum(r['err'] for r in R)}")
    for liv in ("principianti", "esperti"):
        RR = [r for r in R if r["liv"] == liv]
        if not RR: continue
        L = [(("bolina" if x["lato"] == 0 else ("lasco" if r["tri"] else "poppa") if x["lato"] % 2 or r["tri"] else "bolina 2"), x) for r in RR for b in r["barche"] for x in b["lati"]]
        tot = sum(x["vero"] - x["ott"] for _, x in L)
        print(f" {liv}: {len(RR)} regate, {len(L)} lati")
        for t in sorted({t for t, _ in L}):
            g = [x for tt, x in L if tt == t]; p = [x["vero"] - x["ott"] for x in g]
            print(f"   {t:9} lati {len(g):4}  persi mediana {med(p):6.1f} s ({med(a / x['ott'] for a, x in zip(p, g)):.1%}), media {statistics.mean(p):6.1f}, quota {sum(p) / tot:.0%}; virate {statistics.mean(x['vir'] for x in g):.1f} (ottimale {statistics.mean(x['manOtt'] for x in g):.1f}), cambi di mure {statistics.mean(x['cambi'] for x in g):.1f}")
        M = [b["m40"] for r in RR for b in r["barche"] if b.get("m40")]
        if M: print(f"   ultimi 40 m dalla boa 1: {len(M)} passaggi, persi media {statistics.mean(m['vero'] - m['ott'] for m in M):.1f} s (mediana {med(m['vero'] - m['ott'] for m in M):.1f}), virate {statistics.mean(m['vir'] for m in M):.2f}")
        ba = [b for r in RR for b in r["barche"]]
        print(f"   coperti {sum(b['copS'] for b in ba) / max(1, sum(b['fin'] or 1500 for b in ba)):.1%} del tempo, episodi {sum(b['copEp'] for b in ba)}; non arrivati {sum(b['fin'] is None for b in ba)}; taglio mediano {med([b['taglio'] for b in ba if b['taglio'] is not None]):.1f} s; arrivo mediano {med([b['fin'] for b in ba if b['fin'] is not None]):.1f} s; boe toccate {sum(b['toccate'] for b in ba)}, scuffie {sum(b['scuffiate'] for b in ba)}")

if "--conta" in sys.argv: riepilogo(arg("--conta")); sys.exit()
from playwright.async_api import async_playwright
G = {"__file__": str(QUI / "misura_avversari_rotta.py"), "__name__": "x"}; exec((QUI / "misura_avversari_rotta.py").read_text(), G)
js = G["js_corsa"]({k: v for k, v in os.environ.items() if k in ("OMBRA",)})
for a, b in (("sv.fast(0);", "sv.lungo = true; sv.fast(0);"), ("R.t < 900", "R.t < 1500"), ("return { barche, contatti };", "return { barche, contatti, tri: !!R.tri, lungo: !!R.boats && Math.max(...R.marks.map(m => Math.hypot(m.x - R.cb.x, m.y - R.cb.y))) };")):
    assert a in js, a
    js = js.replace(a, b, 1)
GIOCO = pathlib.Path(os.environ.get("RADICE") or QUI.parent); a, b_ = arg("--semi").split("-")

async def main():
    f = pathlib.Path(arg("--righe")); fatte = {(r["k"], r["liv"], r["seme"]) for r in map(json.loads, f.read_text().splitlines())} if f.exists() else set()
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for seme in range(int(a), int(b_) + 1):
            for liv in ("principianti", "esperti"):
                for k in range(3):
                    if (k, liv, seme) in fatte: continue
                    errs = []; t0 = time.time(); pg = await br.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
                    await pg.goto((GIOCO / "index.html").resolve().as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                    r = await pg.evaluate(js, [k, liv, seme]); await pg.close()
                    r.update(k=k, liv=liv, seme=seme, err=len(errs), sec=round(time.time() - t0, 1))
                    with f.open("a") as h: h.write(json.dumps(r) + "\n")
        await br.close()
asyncio.run(main())
