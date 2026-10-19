# Distacchi in regata (1.0.33, docs/PROPOSTA-DISTACCHI.md). Pagina con #collaudo, passi di 1/60 s, Math.random a seme fisso, giocatore
# guidato da __sv.pilota. Regate 1, 2 e «nei salti di vento», principianti ed esperti; semi 1-20 da guardare, 21-60 di conferma.
#  D1 il distacco nella classifica del pannello (distacco(b)) della barca che ha tagliato subito prima del giocatore, letto 5 s prima del
#     taglio del giocatore, contro la differenza vera dei tagli (tempi senza penalità): entro 3 s nel 90% delle regate misurate (conferma);
#  D2 all'arrivo i secondi del risultato sono le differenze dei tempi d'arrivo (con le penalità) arrotondate: sempre;
#  D3 salti oltre 5 s fra due letture di 0,5 s della stessa barca, senza cambio di segno: contati e riportati; dopo l'arrivo la
#     classifica mostra le differenze dei tempi d'arrivo.
# Uso: collaudo_distacchi.py [primo ultimo]. Esce con 1 se D1 (conferma) o D2 falliscono, o se D1 non misura niente.
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
REGATA = """([reg, liv, seme]) => { const sv = __sv; sv.fast(0); sv.openItem(['r', reg]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById('aiLevel'); sel.value = liv; sel.dispatchEvent(new Event('change'));
  const R = sv.R, me = R.boats[0], letture = []; let prev = R.t;
  while (R.t < 900 && me.fin === null){ sv.pilota(1 / 60); sv.run(1 / 60, 1);
    if (Math.floor(R.t * 2) !== Math.floor(prev * 2)) letture.push([R.t, R.boats.filter(b => !b.me).map(b => [b.name, distacco(b)])]); prev = R.t; }
  const testo = document.getElementById('rDoneText').textContent; sv.panel();
  const fine = R.boats.filter(b => !b.me).map(b => [b.name, distacco(b)]), righe = document.getElementById('standings').textContent;
  return { letture, fin: R.boats.map(b => [b.name, b.fin, b.pen]), testo, arrivato: me.fin !== null, fine, righe }; }"""

async def main():
    a = sys.argv[1:]; primo, ultimo = (int(a[0]), int(a[1])) if len(a) == 2 else (1, 60)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        await pg.add_init_script(SEME)
        errori = []; pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        D1 = {"guardati": [], "conferma": []}; d2ok = d2n = neg = salti = letture_tot = non_arrivate = 0
        for seme in range(primo, ultimo + 1):
            for reg in (0, 1, 2):
                for liv in ("principianti", "esperti"):
                    r = await pg.evaluate(REGATA, [reg, liv, seme])
                    if not r["arrivato"]: non_arrivate += 1; continue
                    fin = {n: (f, pen) for n, f, pen in r["fin"]}; mf, mpen = fin["Tu"]; mt = mf - mpen
                    # D1
                    vicina = [l for l in r["letture"] if l[0] <= mt - 5]
                    tagli = sorted((f - pen, n) for n, (f, pen) in fin.items() if n != "Tu" and f is not None and f - pen <= mt)
                    if vicina and tagli:
                        n = tagli[-1][1]; s = dict(vicina[-1][1]).get(n)
                        if s is not None: D1["guardati" if seme <= 20 else "conferma"].append(abs(s - (mt - tagli[-1][0])))
                    # D2
                    attese = sorted([(f, n) for n, (f, _) in fin.items() if n != "Tu" and f is not None and f <= mf])
                    if attese:
                        d2n += 1; atteso = f"a {round(mf - attese[-1][0])} s dalla {attese[-1][1]}"
                        d2ok += atteso in r["testo"] and (len(attese) == 1 or f"a {round(mf - attese[0][0])} s dalla {attese[0][1]} (prima)" in r["testo"])
                    # D3
                    for (t0, l0), (t1, l1) in zip(r["letture"], r["letture"][1:]):
                        a0, a1 = dict(l0), dict(l1); letture_tot += sum(v is not None for v in a1.values())
                        for k, v in a1.items():
                            if v is not None and a0.get(k) is not None and (v >= 0) == (a0[k] >= 0) and abs(v - a0[k]) > 5: salti += 1
                    for n, s in r["fine"]:  # dopo l'arrivo: differenze dei tempi d'arrivo
                        if fin[n][0] is not None: neg += abs(s - (mf - fin[n][0])) > 1e-6
            print(f"  seme {seme}: D1 misurate finora {sum(len(v) for v in D1.values())}", flush=True)
        ok = True
        for nome, v in D1.items():
            if not v: continue
            entro = sum(x <= 3 for x in v); v.sort()
            print(f"D1 {nome}: {entro} su {len(v)} entro 3 s ({100 * entro / len(v):.0f}%), errore mediano {v[len(v) // 2]:.1f} s, massimo {v[-1]:.1f} s")
            if nome == "conferma": ok = entro >= 0.9 * len(v)
        if not any(D1.values()): ok = False; print("D1: nessuna regata misurata")
        print(f"D2: {d2ok} su {d2n} risultati con i secondi giusti"); ok = ok and d2ok == d2n
        print(f"D3: {letture_tot} letture, salti oltre 5 s con la stessa barca {salti}; dopo l'arrivo distacchi diversi dai tempi d'arrivo: {neg}")
        print(f"regate in cui il pilota non arriva entro 900 s: {non_arrivate}; errori della pagina: {errori[:2]}")
        ok = ok and not errori and neg == 0
        print("ESITO: " + ("OK" if ok else "FALLITO")); await b.close(); sys.exit(0 if ok else 1)

asyncio.run(main())
