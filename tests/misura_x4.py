# Voce 4B, variante x4, terza misura (docs/PROPOSTA-COPPIE.md §16, criteri scritti prima): la stessa corsa di misura_manovre.py sulle regate lunghe del torneo,
# base (off) e x4 (m4: MANOVRE con rinvio di 4 s) alternate sulla stessa regata, pagina nuova per ognuna, una riga JSON per regata nel file --righe (riprende da dove era).
# Si corre su una copia del gioco con sperimentale/coppie-4b-3/variante_x4_1516_dopo_il_via_1.3.55.patch (RADICE); con MANOVRE spento la patch non cambia niente.
# Uso: RADICE=copia python tests/misura_x4.py --semi 2801-2830 --righe file.jsonl   (BROWSER=firefox); riepilogo: python tests/misura_x4.py --conta file.jsonl
import asyncio, json, os, pathlib, random, statistics, sys, time
QUI = pathlib.Path(__file__).resolve().parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d

def conta_riga(r):
    """I conti di misura_manovre.py per una regata."""
    m1 = m2 = 0
    for c in r["log"]:
        riv = [x for x, idx in ((0, c["i"]), (1, c["j"])) if idx != 0]
        if c["t"] >= 0 and any(c["vir"][x] <= 5 for x in riv): m1 += 1
        if -5 <= c["t"] < 0 and any(c["go"][x] <= 5 for x in riv): m2 += 1
    return {"M1": m1, "M2": m2, "M3": len(r["log"]), "pil": sum(0 in (c["i"], c["j"]) for c in r["log"]), "fuori": r["fuori"], "nonarr": sum(f is None for f in r["fin"]),
            "piant": r["piant"], "copd": r["copDopo"], "arr": [f for f in r["fin"] if f is not None]}

def riepilogo(nomefile):
    righe = [json.loads(x) for x in open(nomefile)]
    d = {(r["conf"], r["s"], r["k"]): conta_riga(r) for r in righe}
    tornei = sorted({(s) for (_, s, _) in d}); tornei = [s for s in tornei if all((c, s, k) in d for c in ("off", "m4") for k in range(3))]
    print(f"{nomefile}: {len(tornei)} tornei completi, {3 * len(tornei)} regate per configurazione, semi {tornei[0]}-{tornei[-1]}, errori {sum(r['err'] for r in righe)}")
    assert tornei
    tot = lambda c, f, T: sum(d[c, s, k][f] for s in T for k in range(3))
    for f in ("M1", "M2", "M3", "pil", "fuori", "nonarr", "piant", "copd"):
        a, b = tot("off", f, tornei), tot("m4", f, tornei)
        G = random.Random(1); rap = []
        for _ in range(4000):
            T = [G.choice(tornei) for _ in tornei]; x, y = tot("off", f, T), tot("m4", f, T)
            if x: rap.append(y / x - 1)
        rap.sort()
        q = lambda p: f"{100 * rap[int(p * len(rap))]:+.1f}%" if rap else "-"
        print(f"  {f:7} base {a:5}  x4 {b:5}  {100 * (b / a - 1) if a else 0:+6.1f}%   ricampionando i tornei: 5% {q(0.05)}, 95% {q(0.95)}")
    for c in ("off", "m4"): print("  M4 arrivo mediano", c, round(statistics.median([t for s in tornei for k in range(3) for t in d[c, s, k]["arr"]]), 1))

if "--conta" in sys.argv: riepilogo(arg("--conta")); sys.exit()
src = (QUI / "misura_manovre.py").read_text().split("\nasync def main")[0]
M = {"__file__": str(QUI / "misura_manovre.py")}; exec(src, M)
GIOCO, CORSA, imposta, SEMI = M["GIOCO"], M["CORSA"], M["imposta"], M["SEMI"]
assert GIOCO != QUI.parent, "serve RADICE: una copia del gioco con la patch"
CONFS = ["off", "m4"]

async def main():
    f = pathlib.Path(arg("--righe")); fatte = set()
    if f.exists(): fatte = {(r["conf"], r["s"], r["k"]) for r in map(json.loads, f.read_text().splitlines())}
    async with M["async_playwright"]() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for s in SEMI:
            for k in range(3):
                for conf in CONFS:
                    if (conf, s, k) in fatte: continue
                    errs = []; t0 = time.time()
                    pg = await br.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
                    await pg.goto((GIOCO / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                    await pg.evaluate("() => { __sv.lungo = true; " + imposta(conf) + " }")
                    r = await pg.evaluate(CORSA, [k, s, 0]); await pg.close()
                    r.update(conf=conf, s=s, k=k, err=len(errs), sec=round(time.time() - t0, 1))
                    with f.open("a") as h: h.write(json.dumps(r) + "\n")
        await br.close()
asyncio.run(main())
