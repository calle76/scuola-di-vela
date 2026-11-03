# Avversari che non partono (1.1.1, docs/PROPOSTA-PARTENZE-1B.md): conta gli avversari che 60 s dopo lo sparo non hanno ancora tagliato
# la linea, in una regata, con principianti ed esperti e 60/180/300 s di preparazione. Stesso metodo del criterio (4) di
# collaudo_partenze.py (pagina con #collaudo, clic sulla regata, livello, Math.random a seme fisso, preparazione, passi fissi
# di 1/60 s fino a 60 s dopo lo sparo, giocatore fermo), ma su tutte e quattro le regate e con quanti semi si vuole.
# Uso: python collaudo_non_partite.py <regata 0-3>            semi 1-20 (oppure quelli della variabile NONPARTITE_SEMI, per esempio 1-200)
# Criterio (soglia dichiarata nella proposta): 0 barche non partite. Il metro dichiara quante barche ha contato e deve averle contate
# tutte (2 livelli × 3 preparazioni × semi × 3 avversari); una regata già partita all'apertura rende la misura NON VALIDA.
# Caso noto accettato da Ale il 1 novembre 2026: regata 2 (salti di vento), esperti, 60 s, seme 40, Verde (fuori dai semi 1-20).
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright

URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
REG = int(sys.argv[1]); A, B = map(int, os.environ.get("NONPARTITE_SEMI", "1-20").split("-"))
NOMI = ["bastone", "raffiche", "salti di vento", "giri di penalità"]
JS = """([liv, cd, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  sv.fast(0); sel('aiLevel', liv);
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.simTime = 0; sel('cdSel', String(cd));
  const R = sv.R, ai = R.boats.filter(b => !b.me); if (R.t >= 0) return null;
  const non = new Set(ai.map(b => b.name));
  while (R.t < 60){ sv.run(1/60, 1); ai.forEach(b => { if (b.leg > 0) non.delete(b.name); }); }
  return { n: ai.length, non: [...non] };
}"""

async def main():
    attese = 2 * 3 * (B - A + 1) * 3; contate = 0; non = []; non_valide = []; errori = []
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for liv in ("principianti", "esperti"):
            for cd in (60, 180, 300):
                for seme in range(A, B + 1):
                    pg = await b.new_page(viewport={"width": 1280, "height": 800}); pg.on("pageerror", lambda e: errori.append(str(e)))
                    await pg.goto(URL); await pg.wait_for_timeout(300)
                    await pg.click(f"[data-r='{REG}']"); await pg.wait_for_timeout(100)
                    r = await pg.evaluate(JS, [liv, cd, seme]); await pg.close()
                    if r is None: non_valide.append((liv, cd, seme)); continue
                    contate += r["n"]; non += [f"{liv} {cd} s seme {seme} {x}" for x in r["non"]]
        await b.close()
    print(f"regata {REG} ({NOMI[REG]}), semi {A}-{B}: barche contate {contate} su {attese}; non partite entro 60 s dallo sparo: {len(non)}")
    for x in non: print(f"  NO  non partita: {x}")
    if non_valide: print(f"misure non valide (regata già partita all'apertura): {non_valide}")
    print(f"errori della pagina: {errori[:2]}")
    if contate != attese or non_valide or errori: print("ESITO: NON VALIDO"); sys.exit(1)
    print("ESITO: " + ("OK" if not non else f"FALLITO ({len(non)} non partite)")); sys.exit(1 if non else 0)

asyncio.run(main())
