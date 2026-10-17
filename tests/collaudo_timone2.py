# Timone del livello 2 in prova nella navigazione libera (1.0.24-1.0.25, docs/PROPOSTA-STALLO-TIMONE.md §8-9).
# Guida davvero la barca con i tasti (pagina con #collaudo, passi fissi di 1/60 s, senza raffiche):
#  1. la scelta «Barca» mette la barca del livello 2 e la toglie; il livello 1 resta con la barra veloce (1,6 al secondo);
#  2. livello 2: la sola freccia porta la barra fino a 35°, Maiusc + freccia fino a 45°, sempre a 1,6 al secondo; il cursore trascinato non va più veloce;
#  3. 12 virate (6, 10 e 15 nodi, mure a dritta e a sinistra, sola freccia e freccia con Maiusc): tutte riescono; con Maiusc la pala stalla
#     e il suggerimento lo dice; si riportano durata, velocità minima e secondi in stallo, da confrontare con tests/fisica/timone2.js;
#  4. la pagina caricata come la carica un giocatore (senza #collaudo): la scelta c'è, si cambia, nessun errore della pagina.
# Esce con 1 se un controllo fallisce.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
falliti = []
def check(ok, testo):
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: falliti.append(testo)

async def apri(pg, kn, lv):
    await pg.goto("about:blank"); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
    await pg.evaluate("__sv.openItem('free')")
    await pg.evaluate("""([k, lv]) => { for (const [id, v] of [['wSpd', k], ['gustSel', '0'], ['wDir', '0'], ['boatLv', lv]]){
        const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); } }""", [str(kn), str(lv)])
    await pg.evaluate("__sv.openItem('free')")  # riparte con le scelte nuove
    await pg.click("#c")

async def tieni(pg, tasti, secondi):  # la barra si legge prima di lasciare i tasti: dopo, un fotogramma vero la ricentrerebbe un poco
    for t in tasti: await pg.keyboard.down(t)
    b = await pg.evaluate("n => { __sv.run(1 / 60, n); return __sv.ctl.tiller; }", round(secondi * 60))
    for t in reversed(tasti): await pg.keyboard.up(t)
    return b

async def virata(pg, kn, mure, veloce):
    await apri(pg, kn, 2)
    h = 45 if mure > 0 else 315  # vento da nord: 45 = mure a sinistra... la prua deve passare dall'altra parte
    await pg.evaluate("""h => { const S = __sv.S; for (let i = 0; i < 2400; i++){ S.h = h; __sv.ctl.sheet = 0.1; __sv.ctl.tiller = 0; __sv.run(1 / 60, 1); } }""", h)
    tasto = "ArrowRight" if mure > 0 else "ArrowLeft"
    tasti = (["Shift"] if veloce else []) + [tasto]
    # la barra si tiene finché la prua passa −40° dal vento sull'altro lato, poi si lasciano i tasti (la barra torna al centro da sola, aiuto acceso)
    # e si guida ancora 3 s: velocità minima e stallo contano su tutta la manovra, come in tests/fisica/timone2.js
    for t in tasti: await pg.keyboard.down(t)
    fase = """([mure, fine]) => { const S = __sv.S, o = __sv.o; for (let t = 0; t < fine; t += 1 / 60){ __sv.ctl.sheet = 0.1; __sv.run(1 / 60, 1); __sv.panel();
          o.umin = Math.min(o.umin, S.u); if (S.stall){ o.st += 1 / 60; const h = document.getElementById('hint'); if (/stallo/.test(h.textContent) && !h.hidden) o.hint = true; }
          o.t += 1 / 60; const a = ((S.h + 180) % 360 + 360) % 360 - 180; if (fine > 5 && mure * a < -40) break; } }"""
    await pg.evaluate("__sv.o = { u0: __sv.S.u, umin: __sv.S.u, st: 0, hint: false, t: 0 }")
    await pg.evaluate(fase, [mure, 15])
    for t in reversed(tasti): await pg.keyboard.up(t)
    await pg.evaluate(fase, [mure, 3])
    r = await pg.evaluate("Object.assign({ lv: __sv.S.lv, cap: __sv.S.capsized }, __sv.o)")
    r["t"] -= 3
    return r

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errori = []; pg.on("pageerror", lambda e: errori.append(str(e)))

        # 1-2: velocità della barra
        await apri(pg, 10, 1)
        check(await pg.evaluate("__sv.S.lv === undefined"), "livello 1: nessun segno del livello 2 sulla barca")
        t1 = await tieni(pg, ["ArrowRight"], 0.5); check(abs(t1 - 0.8) <= 1.6 / 60 + 0.005, f"livello 1, freccia per 0,5 s: barra {t1:.3f} (attesa 0,8; un fotogramma vero in più è ammesso)")
        await apri(pg, 10, 2)
        check(await pg.evaluate("__sv.S.lv === 2"), "livello 2: la barca ha il timone del livello 2")
        t2 = await tieni(pg, ["ArrowRight"], 1.0); check(abs(t2 - 35 / 45) < 0.001, f"livello 2, freccia per 1 s: barra {t2:.3f} (attesa {35/45:.3f}, cioè 35°: si ferma lì)")
        await pg.evaluate("__sv.ctl.tiller = 0")
        t3 = await tieni(pg, ["Shift", "ArrowRight"], 0.5); check(abs(t3 - 0.8) <= 1.6 / 60 + 0.005, f"livello 2, Maiusc + freccia per 0,5 s: barra {t3:.3f} (attesa 0,8)")
        t5 = await tieni(pg, ["Shift", "ArrowRight"], 0.5); check(t5 == 1, f"livello 2, Maiusc + freccia ancora 0,5 s: barra {t5:.3f} (attesa 1, cioè 45°)")
        # cursore e passi nella stessa chiamata: nessun fotogramma vero in mezzo
        t4 = await pg.evaluate("() => { __sv.ctl.tiller = 0; const e = document.getElementById('tiller'); e.value = 100; e.dispatchEvent(new Event('input')); __sv.run(1 / 60, 6); return __sv.ctl.tiller; }")
        check(t4 <= 1.6 * 6 / 60 + 0.001, f"livello 2, cursore portato a fondo: dopo 6 passi barra {t4:.3f} (al massimo 0,16: 1,6 al secondo)")
        await pg.evaluate("const e = document.getElementById('tiller'); e.dispatchEvent(new Event('change'))")
        await pg.evaluate("const e = document.getElementById('boatLv'); e.value = '1'; e.dispatchEvent(new Event('change'))")
        check(await pg.evaluate("__sv.S.lv === undefined"), "di nuovo livello 1 dalla scelta «Barca»: la barca torna quella del livello 1")

        # 3: virate guidate coi tasti
        print("virate (vento, mure, barra): durata, minima/entrata, secondi in stallo, avviso di stallo")
        n = 0
        for kn in (6, 10, 15):
            for mure in (1, -1):
                for veloce in (False, True):
                    r = await virata(pg, kn, mure, veloce); n += 1
                    ok = r["t"] < 14.9 and not r["cap"]
                    print(f"  {kn} nodi, mure {'a sinistra' if mure > 0 else 'a dritta'}, {'freccia e Maiusc' if veloce else 'sola freccia    '}: "
                          f"{r['t']:.2f} s, {r['umin'] / r['u0']:.0%}, stallo {r['st']:.2f} s, avviso {'sì' if r['hint'] else 'no'}")
                    check(ok and r["lv"] == 2, f"virata {n} riuscita con la barca del livello 2")
                    if veloce: check(r["st"] > 0.2 and r["hint"], f"virata {n}, freccia e Maiusc: la pala stalla e il suggerimento lo dice")

        # 4: pagina come la carica un giocatore
        await pg.goto("about:blank"); await pg.goto(BASE); await pg.wait_for_timeout(400)
        await pg.click("#goFree"); await pg.wait_for_timeout(200)
        await pg.evaluate("document.getElementById('setDlg').showModal()")
        vis = await pg.is_visible("#boatLv"); check(vis, "senza #collaudo: nelle impostazioni c'è la scelta «Barca»")
        await pg.select_option("#boatLv", "2"); await pg.evaluate("document.getElementById('setDlg').close()")
        await pg.keyboard.down("ArrowRight"); await pg.wait_for_timeout(500); await pg.keyboard.up("ArrowRight")
        txt = await pg.text_content("#vTil"); check("dritta" in txt, f"senza #collaudo, livello 2: la barra si muove ({txt.strip()})")
        check(not errori, f"nessun errore della pagina ({errori[:2]})")
        await b.close()
    print("ESITO: " + ("OK" if not falliti else f"FALLITO ({len(falliti)})"))
    sys.exit(1 if falliti else 0)

asyncio.run(main())
