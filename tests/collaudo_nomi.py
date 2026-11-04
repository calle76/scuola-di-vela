# Nomi al posto dei numeri (1.2.11, docs/PROPOSTA-MEDAGLIE-E-NOMI.md §3, soglie scritte prima; decisioni di Ale del 30 ottobre 2026, PROPOSTA-RIORGANIZZAZIONE §8).
#   N1: nel testo A SCHERMO (innerText) di menu, libretto, attestato, esame, torneo e regate nessun «1a», «1b», «brevetto», «livello 1», «livello 2»; almeno 8 schermate lette, nessuna vuota
#   N1c: controprova: una scritta «Torneo dell'1b» inserita apposta viene trovata dallo stesso controllo
#   N2: attestato con «La scuola», «superata», «Attestato del gioco», «Nessun valore legale»
#   N3: una carriera salvata con `brevetto` (nome interno del campo, resta) apre attestato e torneo come prima; senza, il torneo è chiuso e dice «dopo l'attestato»
#   N4: menu ed esame anche in una pagina senza #collaudo; 0 errori della pagina
# Uso: python collaudo_nomi.py   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, re, sys
import metro, sorgente
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parents[1] / "index.html").as_uri()
GERGO = re.compile(r"\b1[ab]\b|brevett|livello\s*[12]\b", re.I)
MK = ["m0.4", "m1.4", "m2.4", "m3.5", "m4.6"]
bad = []; lette = []; errori = []
def chk(ok, m):
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def leggi(pg, nome):
    t = await pg.evaluate("document.body.innerText")
    lette.append((nome, len(t.strip()), GERGO.findall(t)))
    print(f"  {nome}: {len(t.strip())} caratteri, gergo {GERGO.findall(t)}", flush=True)
    return t
async def pagina(b, hash_, salv=None, modo="libero"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(sorgente.NASCONDI_NUOVE)
    pg.on("pageerror", lambda e: errori.append(str(e)))
    await pg.goto(BASE + hash_)
    await pg.evaluate("([d, m]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }", [json.dumps(salv) if salv else None, modo])
    await pg.reload(); await pg.wait_for_timeout(300)
    return ctx, pg
async def esame(pg, nome):
    await pg.click("#goEsame"); await leggi(pg, nome + ", domanda")
    while not await pg.locator("#qzBody .score").count():
        await pg.locator(".opt").first.click(); await pg.click("#qzNext")
    t = await leggi(pg, nome + ", esito"); await pg.click("#qzClose"); await pg.wait_for_timeout(150)
    return t
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for hash_, tag in (("", "senza #collaudo"), ("#collaudo", "con #collaudo")):   # N4
            ctx, pg = await pagina(b, hash_)
            for g in range(3):
                await pg.click(f"#schede button[data-g='{g}']"); await leggi(pg, f"menu libero, gruppo {g + 1}, {tag}")
            t = await esame(pg, f"esame, {tag}")
            chk("Esame della scuola" in t, f"N1 l'esame si chiama «Esame della scuola», {tag}")
            await ctx.close()
        # carriera senza attestato: il torneo è chiuso e lo dice
        ctx, pg = await pagina(b, "#collaudo", modo="carriera")
        t = await leggi(pg, "menu carriera, senza attestato")
        chk(await pg.is_disabled("#goTor") and "dopo l'attestato" in await pg.inner_text("#goTor"), f"N3 senza attestato il torneo è chiuso: «{(await pg.inner_text('#goTor')).splitlines()}»")
        await ctx.close()
        # carriera salvata con il campo vecchio
        ctx, pg = await pagina(b, "#collaudo", modo="carriera")
        nq = await pg.evaluate("[0, 1, 2, 3].map(i => QUIZ[i].length)"); bande = await pg.evaluate("MISSIONS.map(m => m.bands)")
        await ctx.close()
        salv = {"done": {f"l{i}": True for i in range(6)}, "best": {MK[i]: bande[i][1] for i in range(5)}, "clean": {MK[0]: True, MK[1]: True}, "quiz": {f"q{i}": nq[i] for i in range(4)},
                "race": {f"{k}:principianti": {"pos": 3, "n": 4, "pulita": False} for k in ("r0.4", "r1.4")}, "exam": {"superato": True, "voto": 20, "n": 20, "ripasso": []}, "brevetto": {"data": "2026-10-20", "nome": "Ale"}}
        ctx, pg = await pagina(b, "#collaudo", salv=salv, modo="carriera")
        t = await leggi(pg, "menu carriera, con attestato")
        chk((await pg.inner_text("#libManca")).startswith("Attestato ottenuto il"), f"N3 libretto: «{await pg.inner_text('#libManca')}»")
        await pg.click("#goAttest"); await pg.wait_for_timeout(150)
        t = await leggi(pg, "attestato")
        chk(metro.tutti([s in t for s in ("La scuola", "superata", "Attestato del gioco", "Nessun valore legale")], minimo=4), f"N2 scritte dell'attestato: {t[:120]!r}")
        chk(await pg.input_value("#atName") == "Ale", "N3 il nome salvato c'è ancora")
        await pg.click("#atClose"); await pg.wait_for_timeout(100)
        chk(not await pg.is_disabled("#goTor"), "N3 con il campo salvato il torneo si apre")
        await pg.click("#goTor"); await pg.wait_for_timeout(200); await leggi(pg, "riquadro del torneo")
        await pg.evaluate("__sv.skipBrief = false"); await pg.click("#torGo"); await pg.wait_for_timeout(300); await leggi(pg, "istruzioni della regata del torneo")
        await pg.click("#bGo"); await pg.wait_for_timeout(400); await leggi(pg, "regata del torneo")
        await ctx.close()
        # le regate: quella dei giri, nel menu e in acqua
        ctx, pg = await pagina(b, "#collaudo")
        await leggi(pg, "menu con le regate")
        for r in range(4):
            await pg.evaluate(f"__sv.openItem(['r', {r}])"); await pg.wait_for_timeout(150); await leggi(pg, f"regata {r}")
        # N1c: la controprova, con lo stesso controllo
        await pg.evaluate("document.body.insertAdjacentHTML('beforeend', `<p>Torneo dell'1b</p>`)")
        t = await pg.evaluate("document.body.innerText"); chk(bool(GERGO.search(t)), "N1c la scritta messa apposta viene trovata")
        await ctx.close()
        await b.close()
    chk(len(lette) >= 8 and all(n > 40 for _, n, _ in lette), f"N1 schermate lette {len(lette)} (almeno 8), la più corta {min(n for _, n, _ in lette)} caratteri")
    chk(metro.nessuno([g for _, _, g in lette], minimo=8), f"N1 gergo a schermo: {[(n, g) for n, _, g in lette if g]}")
    chk(metro.nessuno(errori, minimo=0), f"errori della pagina {errori[:3]}")
    print("casi sbagliati:", bad or "nessuno"); print("ESITO: " + ("FALLITO" if bad else "OK"))
    sys.exit(1 if bad else 0)
asyncio.run(main())
