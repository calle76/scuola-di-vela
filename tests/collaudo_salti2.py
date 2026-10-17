# Salti di vento del livello 2 in prova (1.0.28, docs/PROPOSTA-SALTI-VENTO.md): pagina con #collaudo, passi di 1/60 s, Math.random a seme fisso.
#  1. navigazione libera, barca del livello 1, senza raffiche: il vento non gira (240 s);
#  2. navigazione libera, barca del livello 2: il vento gira di almeno 16° fra il minimo e il massimo in 240 s, e mai oltre 40°;
#  3. regata nei salti di vento (S3): 12 regate (semi 1-6, principianti ed esperti), giocatore guidato da __sv.pilota come nell'impronta:
#     boa a 300 m, tutte le barche del livello 2, il vento gira, e tutte e quattro le barche arrivano entro 900 s;
#  4. menu del gioco libero a 1360x650: la regata nuova c'è e il menu non va oltre la finestra; nella carriera non c'è;
#  5. pagina senza #collaudo: la regata si apre, nessun errore della pagina.
# Esce con 1 se un controllo fallisce.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
falliti = []
def check(ok, testo):
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: falliti.append(testo)

LIBERA = """([lv]) => { const sv = __sv; sv.fast(0); sv.openItem('free');
  for (const [id, v] of [['wSpd', '10'], ['gustSel', '0'], ['wDir', '0'], ['boatLv', String(lv)]]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); let lo = 999, hi = -999;
  for (let i = 0; i < 240 * 60; i++){ sv.run(1 / 60, 1); const d = ((sv.twd - 0 + 540) % 360) - 180; lo = Math.min(lo, d); hi = Math.max(hi, d); }
  return [lo, hi, sv.S.lv]; }"""
REGATA = """([liv, seme]) => { const sv = __sv; sv.fast(0); sv.openItem(['r', 2]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById('aiLevel'); sel.value = liv; sel.dispatchEvent(new Event('change'));
  const R = sv.R; let lo = 999, hi = -999;
  const m = R.mark, c = R.center, up = Math.hypot(m.x - c.x, m.y - c.y);
  while (R.t < 900 && !R.boats.every(b => b.fin !== null)){ sv.pilota(1 / 60); sv.run(1 / 60, 1);
    const d = ((sv.twd - R.mark.out + 540) % 360) - 180; lo = Math.min(lo, d); hi = Math.max(hi, d); }
  return { up, lv: R.boats.map(b => b.S.lv), fin: R.boats.map(b => b.fin), pen: R.boats.map(b => b.pen), nomi: R.boats.map(b => b.name), lo, hi, t: R.t, brief: R.brief }; }"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        await pg.add_init_script(SEME)
        errori = []; pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)

        lo, hi, lv = await pg.evaluate(LIBERA, [1])
        check(hi - lo < 0.001 and lv is None, f"libera, livello 1: il vento non gira (escursione {hi - lo:.3f}°)")
        lo, hi, lv = await pg.evaluate(LIBERA, [2])
        check(lv == 2 and 16 <= hi - lo <= 40, f"libera, livello 2: il vento gira fra {lo:.1f}° e {hi:.1f}° (escursione fra 16 e 40)")

        n = arrivate = 0
        for liv in ("principianti", "esperti"):
            for seme in range(1, 7):
                r = await pg.evaluate(REGATA, [liv, seme]); n += 1
                tutte = all(f is not None for f in r["fin"])
                arrivate += tutte
                print(f"  regata {n} ({liv}, seme {seme}): boa a {r['up']:.0f} m, vento fra {r['lo']:.1f}° e {r['hi']:.1f}°, "
                      f"arrivi {[None if f is None else round(f) for f in r['fin']]} s, penalità {r['pen']}")
                check(abs(r["up"] - 300) < 1 and all(v == 2 for v in r["lv"]) and r["hi"] - r["lo"] >= 8 and tutte,
                      f"regata {n}: boa a 300 m, barche del livello 2, il vento gira, arrivano tutte")
        print(f"S3: regate con tutte le barche arrivate {arrivate} su {n}")
        check("gira" in r["brief"], "le istruzioni della regata dicono che il vento gira")

        # menu
        await pg.evaluate("document.getElementById('toMenu').click()")
        mn = await pg.evaluate("""() => { const m = document.getElementById('menu'); const t = [...m.querySelectorAll('button[data-r]')].map(b => b.textContent);
          return { titoli: t, eccesso: m.scrollHeight - m.clientHeight, alto: document.documentElement.scrollHeight - innerHeight }; }""")
        check(any("salti di vento" in t for t in mn["titoli"]) and mn["eccesso"] <= 0 and mn["alto"] <= 0,
              f"menu del gioco libero: regata nuova presente, eccesso {mn['eccesso']} px / pagina {mn['alto']} px")
        await pg.evaluate("""document.querySelector('#modoSel [data-v="carriera"]').click()""")
        car = await pg.evaluate("[...document.querySelectorAll('#menu button[data-r]')].map(b => b.textContent)")
        check(len(car) == 2 and not any("salti" in t for t in car), f"menu della carriera: solo le 2 regate del livello 1 ({len(car)})")
        await pg.evaluate("""document.querySelector('#modoSel [data-v="libero"]').click()""")

        # pagina come la carica un giocatore
        await pg.goto("about:blank"); await pg.goto(BASE); await pg.wait_for_timeout(400)
        await pg.click('button[data-r="2"]'); await pg.wait_for_timeout(500)
        tit = await pg.text_content("#rTitle"); check("salti di vento" in tit, f"senza #collaudo: la regata si apre ({tit.strip()})")
        check(not errori, f"nessun errore della pagina ({errori[:2]})")
        await b.close()
    print("ESITO: " + ("OK" if not falliti else f"FALLITO ({len(falliti)})"))
    sys.exit(1 if falliti else 0)

asyncio.run(main())
