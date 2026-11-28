# Voce 92: le regate di collaudo_giri_avversari.py a pezzi (per il giro «Misura») e il solo controllo G12, con il calcolo di prima (valore assoluto)
# e quello nuovo (angolo col segno). Per ogni segmento che con uno dei due non torna stampa seme, barca e i campioni attorno alla scelta.
# Uso: python sperimentale/voce-92/misura_g12.py --semi 1-300 (un pezzo solo: le regate vanno in fila sulla stessa pagina, come nel collaudo)
import asyncio, os, pathlib, sys
QUI = pathlib.Path(__file__).resolve()
TESTS = QUI.parents[2] / "tests"
sys.path.insert(0, str(TESTS))
ns = {"__file__": str(TESTS / "collaudo_giri_avversari.py"), "__name__": "g12"}
exec((TESTS / "collaudo_giri_avversari.py").read_text().replace("\nasyncio.run(main())", ""), ns)   # senza l'avvio del collaudo

async def main():
    a, z = map(int, sys.argv[sys.argv.index("--semi") + 1].split("-"))
    async with ns["async_playwright"]() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await ns["pagina"](b, ns["ROOT"])
        tot = vecchio = nuovo = 0
        for k in range(1, z + 1):
            # le regate prima del pezzo non si fanno: solo il pezzo che parte da 1 ripete la sequenza del collaudo
            if k < a: continue
            r = await pg.evaluate(ns["REGATA"], [k, "principianti" if k % 2 else "esperti"])
            for i, log in enumerate(r["log"]):
                m = 0; fine = None
                while m < len(log):
                    if not log[m][4]: m += 1; continue
                    a_ = m
                    while m < len(log) and log[m][4]: m += 1
                    cont = fine is not None and all(log[x][5] > 0 for x in range(fine, a_ + 1)); fine = m
                    tw, u = log[a_][2], log[a_][6]
                    if cont or m - a_ <= 10 or abs(tw) < 30 or abs(u - 1.5) < 0.05 or abs(abs(tw) - 80) < 2: continue
                    larga = abs(tw) >= 80 or u < 1.5
                    dv = abs(log[a_ + 10][2]) - abs(tw)
                    dn = ns["ndh"](tw, log[a_ + 10][2]) * (1 if tw >= 0 else -1)
                    okv = abs(tw) > 160 or (dv > 0) == larga      # prima: oltre 160° escluso
                    okn = abs(tw) > 160 or (dn > 0) == larga
                    tot += 1; vecchio += not okv; nuovo += not okn
                    if not (okv and okn):
                        righe = [(round(x[0], 2), round(x[2], 2), round(x[6], 2), x[4]) for x in log[max(0, a_ - 5):a_ + 11]]
                        print(f"CASO seme {k} barca {i} variazione prima {dv:.1f} (ok {okv}) col segno {dn:.1f} (ok {okn}); campioni (t, twa, u, sconta): {righe}", flush=True)
        print(f"SOMMA semi {a}-{z}: segmenti {tot}, non tornano prima {vecchio}, col segno {nuovo}, errori pagina {len(errs)}", flush=True)
        await b.close()
asyncio.run(main())
