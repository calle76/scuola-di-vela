# Testo delle penalità nella classifica del pannello (1.0.51). Pagina con #collaudo, Math.random a seme fisso.
#  P1 valori imposti 1, 2 e 3 penalità, in secondi (regate normali) e in punti (torneo): il testo di ogni barca dice «N penalità (+X s)» o «(+X pt)».
#  P2 regate guidate dal pilota (regate 0, 1 e «nei salti di vento», semi 1-12; torneo, semi 1-6) fino all'arrivo: ogni barca con pen o pp
#     ha il testo giusto, nessuna barca senza penalità ha la parola «penalità». Riporta quante barche con penalità ha visto
#     (se zero il controllo non ha misurato niente: ESITO NON VALIDO).
# Uso: python collaudo_penalita_testo.py
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
errori = []; viste = 0
def no(m): errori.append(m); print("  NO  " + m, flush=True)

# lettura: per ogni riga della classifica, nome della barca e testo; poi si confrontano con pen e pp della barca di quel nome
RIGHE = """() => { const sv = __sv; sv.panel(); const per = {}; sv.R.boats.forEach(b => per[b.name] = [b.pen || 0, b.pp || 0]);
  return [...document.querySelectorAll('#standings li')].map(li => [li.querySelector('b').textContent, li.querySelector('span').textContent, ...per[li.querySelector('b').textContent]]); }"""

def controlla(tag, righe):
    global viste
    for nome, testo, pen, pp in righe:
        att = []
        if pen: att.append(f"{pen // 15} penalità (+{pen} s)")
        if pp: att.append(f"{pp} penalità (+{pp} pt)")
        for a in att:
            viste += 1
            if a not in testo: no(f"{tag} {nome}: attesa «{a}», letto «{testo}»")
        if not att and "penalità" in testo: no(f"{tag} {nome}: «penalità» senza penalità, letto «{testo}»")

async def nuova(b):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150); return ctx, pg, errs

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # P1: valori imposti
        ctx, pg, errs = await nuova(b)
        await pg.evaluate("() => { __sv.fast(0); __sv.openItem(['r', 0]); }")
        for n in (1, 2, 3):
            await pg.evaluate("n => { const R = __sv.R; R.boats[0].pen = 15 * n; R.boats[1].pp = n; R.boats[2].pen = 0; }", n)
            controlla(f"P1 n={n}", await pg.evaluate(RIGHE))
        await ctx.close()
        # P2: regate vere
        for reg in (0, 1, 2):
            for seme in range(1, 13):
                ctx, pg, errs = await nuova(b)
                await pg.evaluate("([reg, s]) => { __sv.fast(0); __sv.openItem(['r', reg]); __seed(s); }", [reg, seme])
                await pg.evaluate("() => { const sv = __sv, R = sv.R, me = R.boats[0]; while (R.t < 900 && me.fin === null){ sv.pilota(1 / 60); sv.run(1 / 60, 1); } }")
                controlla(f"P2 regata {reg} seme {seme}", await pg.evaluate(RIGHE))
                if errs: no(f"P2 regata {reg} seme {seme}: errore nella pagina {errs[0]}")
                await ctx.close()
        for seme in range(1, 7):
            ctx, pg, errs = await nuova(b)
            await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); document.getElementById('torGo').click(); }", seme)
            await pg.evaluate("() => { const sv = __sv, R = sv.R, me = R.boats[0]; while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(1 / 60); sv.run(1 / 60, 1); } }")
            controlla(f"P2 torneo seme {seme}", await pg.evaluate(RIGHE))
            if errs: no(f"P2 torneo seme {seme}: errore nella pagina {errs[0]}")
            await ctx.close()
        await b.close()
    print(f"barche con penalità lette: {viste}", flush=True)
    if viste < 7: no("NON VALIDO: nessuna penalità vera vista nelle regate guidate"); 
    print("ESITO: " + ("OK" if not errori else f"FALLITO ({len(errori)}): " + "; ".join(errori[:6])), flush=True)
    sys.exit(1 if errori else 0)

asyncio.run(main())
