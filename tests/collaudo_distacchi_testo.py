# Testo dei distacchi nella classifica del pannello (1.0.54, docs/PROPOSTA-DISTACCHI-IMMEDIATI.md). Pagina con #collaudo, Math.random a seme fisso.
#  D1 ogni 5 s di gioco, in regate guidate dal pilota (regate 0, 1 e «nei salti di vento», semi 1-6; torneo, semi 1-3), ogni riga della classifica
#     finisce come dice distacco(b): arrotondato r > 0 «r s avanti», r < 0 «-r s dietro», 0 «alla pari», null niente. Stampa quante righe ha confrontato
#     (se poche, ESITO NON VALIDO). Nessun «+N s»/«−N s» col vecchio segno.
#  D3 nessuna riga della classifica va a capo (altezza della riga uguale alla più bassa dello stesso momento, con tolleranza di 2 px) -- vedi anche collaudo_pannello.py per l'eccesso.
# Uso: python collaudo_distacchi_testo.py
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
errori = []; viste = 0; senza = 0; capo = 0
def no(m):
    if len(errori) < 12: print("  NO  " + m, flush=True)
    errori.append(m)

# per ogni riga: nome, testo dello span, distacco vero della barca di quel nome, altezza della riga
LEGGI = """() => { const sv = __sv; sv.panel(); const R = sv.R, per = {}; R.boats.forEach(b => per[b.name] = distacco(b));
  return [...document.querySelectorAll('#standings li')].map(li => [li.querySelector('b').textContent, li.querySelector('span').textContent, per[li.querySelector('b').textContent], li.getBoundingClientRect().height]); }"""

def atteso(s):
    if s is None: return None
    r = round(s)
    return f"{r} s avanti" if r > 0 else f"{-r} s dietro" if r < 0 else "alla pari"

def controlla(tag, righe):
    global viste, senza, capo
    h = [x[3] for x in righe if x[3] > 0]
    if h and max(h) - min(h) > 2: capo += 1; no(f"{tag}: righe di altezze diverse {sorted(set(round(x) for x in h))}, una va a capo?")
    for nome, testo, s, _ in righe:
        if re.search(r"[+−-]\d+ s\b", testo.replace("(+", "(")): no(f"{tag} {nome}: segno vecchio in «{testo}»")
        a = atteso(s)
        if a is None:
            senza += 1
            if re.search(r"(avanti|dietro|alla pari)$", testo): no(f"{tag} {nome}: distacco nullo ma il testo dice «{testo}»")
        else:
            viste += 1
            if not testo.endswith(" · " + a): no(f"{tag} {nome}: atteso «{a}», letto «{testo}» (distacco {s:.2f})")

async def nuova(b):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150); return ctx, pg, errs

# corre a passi di 5 s di gioco e ogni volta legge la classifica; restituisce le letture
CORSA = """() => { const sv = __sv, R = sv.R, me = R.boats[0], out = []; let ult = -1e9;
  while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(1 / 60); sv.run(1 / 60, 1);
    if (R.t >= 0 && R.t - ult >= 5){ ult = R.t; sv.panel(); const per = {}; R.boats.forEach(b => per[b.name] = distacco(b));
      out.push([...document.querySelectorAll('#standings li')].map(li => [li.querySelector('b').textContent, li.querySelector('span').textContent, per[li.querySelector('b').textContent], li.getBoundingClientRect().height])); } }
  return out; }"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for reg in (0, 1, 2):
            for seme in range(1, 7):
                ctx, pg, errs = await nuova(b)
                await pg.evaluate("([reg, s]) => { __sv.fast(0); __sv.openItem(['r', reg]); __seed(s); }", [reg, seme])
                for i, righe in enumerate(await pg.evaluate(CORSA)): controlla(f"regata {reg} seme {seme} lettura {i}", righe)
                if errs: no(f"regata {reg} seme {seme}: errore nella pagina {errs[0]}")
                await ctx.close()
        for seme in range(1, 4):
            ctx, pg, errs = await nuova(b)
            await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); document.getElementById('torGo').click(); }", seme)
            for i, righe in enumerate(await pg.evaluate(CORSA)): controlla(f"torneo seme {seme} lettura {i}", righe)
            if errs: no(f"torneo seme {seme}: errore nella pagina {errs[0]}")
            await ctx.close()
        await b.close()
    print(f"righe con distacco confrontate: {viste}; righe senza distacco: {senza}; letture con righe di altezze diverse: {capo}", flush=True)
    if viste < 200: errori.append("NON VALIDO: meno di 200 righe confrontate"); print("  NO  NON VALIDO: meno di 200 righe confrontate")
    print("ESITO: " + ("OK" if not errori else f"FALLITO ({len(errori)})"), flush=True)
    sys.exit(1 if errori else 0)

asyncio.run(main())
