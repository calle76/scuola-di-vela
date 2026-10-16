# Guida la barca con la tastiera simulata per verificare che i passi pratici delle lezioni siano completabili.
# Dalla 0.16 la lezione 1 si guida con le frecce del timone (barra): vento da nord, prua a est, ← poggia e → orza.
# Nota: i passi «cazzare» della lezione 1 e «prepararsi» della lezione 5 possono risultare NON COMPLETATI perché lo script
# cazza troppo e non corregge: non è un difetto del gioco.
# Dal 13 ottobre 2026 a passi fissi: la simulazione del browser è ferma (__sv.fast(0)), i tasti si premono dentro la pagina
# (eventi keydown/keyup sulla finestra, gli stessi che legge il gioco) e il tempo avanza a passi di 1/60 s con __sv.run;
# all'inizio di ogni azione si fissa il seme di Math.random. Prima i tasti si tenevano per secondi veri: il risultato
# dipendeva dal carico del computer, e un colpo di freccia «da 0,7 s» non era mai lo stesso. Passi, tasti, durate e
# righe stampate sono quelli di prima; i tempi stampati sono secondi simulati, contati a passi di 0,25 s come prima.
import asyncio
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
# attrezzi dentro la pagina: tasti, avanzamento a passi fissi, lettura istantanea
ATTREZZI = """() => { const sv = __sv; sv.fast(0); let seme = 1;
  const L = window.L = {};
  L.tasto = (t, k) => dispatchEvent(new KeyboardEvent(t, { key: k }));
  L.semina = () => { let s = seme++; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
  L.leggi = () => { const i = sv.readI(); return { twa: Math.round(i.twa), kn: +i.kn.toFixed(1), tt: i.tt, heel: Math.round(i.heel) }; };
  // avanza fino a maxs secondi simulati, controllando ogni 0,25 s se fermarsi; ritorna i secondi passati
  L.avanza = (maxs, ferma) => { let t = 0; while (t < maxs - 1e-9){ sv.run(1/60, 15); t += 0.25; if (ferma && ferma()) break; } return t; };
  L.tieni = (k, maxs) => { L.semina(); L.tasto("keydown", k); const t = L.avanza(maxs, () => sv.stepDone); L.tasto("keyup", k); return [sv.stepDone, t, L.leggi()]; };
  L.aspetta = maxs => { L.semina(); const t = L.avanza(maxs, () => sv.stepDone); return [sv.stepDone, t, L.leggi()]; };
  L.premi = (k, sec) => { L.semina(); L.tasto("keydown", k); L.avanza(sec); L.tasto("keyup", k); };
}"""
NUOVI = []   # controlli con esito vero/falso (1.0.2); gli altri sono tempi da leggere
def chk_ok(ok, nome):
    NUOVI.append(bool(ok)); print(f"   {'OK ' if ok else 'NO '} {nome}", flush=True)
def stampa(label, r):
    ok, t, I = r
    print(f"{label}: {'OK' if ok else 'NON COMPLETATO'} in {t:.1f}s  {I}", flush=True)
    return ok
async def hold_until(pg, key, maxs, label):
    return stampa(label, await pg.evaluate("([k, m]) => L.tieni(k, m)", [key, maxs]))
async def wait_until(pg, maxs, label):
    return stampa(label, await pg.evaluate("m => L.aspetta(m)", maxs))
async def premi(pg, key, sec):
    await pg.evaluate("([k, s]) => L.premi(k, s)", [key, sec])
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate(ATTREZZI)
        # Lezione 1
        await pg.evaluate("__sv.openItem(['l',0])"); await pg.evaluate("__sv.showStep(6)")
        await hold_until(pg, "ArrowLeft", 12, "L1 poggiare")
        await pg.evaluate("__sv.showStep(7)")
        await hold_until(pg, "ArrowRight", 25, "L1 orzare fino all'angolo morto")
        await pg.evaluate("__sv.showStep(8)")
        # come un giocatore: poggia finché il vento arriva di fianco, poi rilascia e aspetta che la barca riparta
        await pg.evaluate("""() => { L.semina(); L.tasto("keydown", "ArrowLeft"); L.avanza(25, () => __sv.readI().twa > 80); L.tasto("keyup", "ArrowLeft"); }""")
        await wait_until(pg, 15, "L1 ripartire")
        await pg.evaluate("__sv.showStep(9)")
        await hold_until(pg, "s", 10, "L1 lascare")
        await pg.evaluate("__sv.showStep(10)")
        await hold_until(pg, "w", 1.4, "L1 cazzare (primo tratto)")
        await wait_until(pg, 4, "L1 cazzare (attesa)")
        await pg.evaluate("__sv.showStep(11)")
        await hold_until(pg, "w", 10, "L1 troppo cazzata")
        # Lezione 2
        await pg.evaluate("__sv.openItem(['l',1])"); await pg.evaluate("__sv.showStep(1)")
        await hold_until(pg, "ArrowLeft", 5, "L2 barra a sinistra")
        await pg.evaluate("__sv.showStep(2)")
        await hold_until(pg, "ArrowRight", 5, "L2 barra a dritta")
        # Lezione 3 filetti
        await pg.evaluate("__sv.openItem(['l',2])"); await pg.evaluate("__sv.showStep(7)")
        await hold_until(pg, "ArrowDown", 10, "L3 filetto sopravento")
        await pg.evaluate("__sv.showStep(9)")
        await hold_until(pg, "ArrowUp", 10, "L3 filetto sottovento")
        # Lezione 5: virata lanciata (vento da nord, prua a est: barra sottovento = a dritta)
        await pg.evaluate("__sv.openItem(['l',4])"); await pg.evaluate("__sv.showStep(1)")
        await premi(pg, "ArrowRight", 0.7); await premi(pg, "ArrowUp", 1.5)
        await wait_until(pg, 12, "L5 prepararsi (bolina lanciata)")
        await pg.evaluate("__sv.showStep(2)")
        await hold_until(pg, "ArrowRight", 8, "L5 virata")
        S = await pg.evaluate("({tacks: __sv.S.tacks})"); print("   virate contate:", S)
        await wait_until(pg, 8, "L5 virata (assestamento)")
        # Lezione 6: scuffia volontaria
        await pg.evaluate("__sv.openItem(['l',5])"); await pg.evaluate("__sv.showStep(2)")
        await premi(pg, "ArrowRight", 0.6); await premi(pg, "ArrowUp", 3.0)
        await wait_until(pg, 60, "L6 scuffia")
        await pg.screenshot(path=str(OUT / "B_cap.png"))
        await pg.evaluate("__sv.showStep(3)"); await pg.evaluate('() => { L.tasto("keydown", "r"); L.tasto("keyup", "r"); }')
        await wait_until(pg, 8, "L6 raddrizzare")
        # 1.0.2 (osservazione 50): in «La scuffia» la barca resta rovesciata e R non fa niente; «Raddrizzare» parte con la barca rovesciata, anche dopo Ricomincia
        await pg.evaluate("__sv.openItem(['l',5])"); await pg.evaluate("__sv.showStep(2)")
        await premi(pg, "ArrowRight", 0.6); await premi(pg, "ArrowUp", 3.0)
        await wait_until(pg, 60, "L6 scuffia (di nuovo)")
        await pg.evaluate('() => { L.tasto("keydown", "r"); L.tasto("keyup", "r"); }'); await pg.evaluate("__sv.run(1/60, 300)")
        st = await pg.evaluate("({cap: __sv.S.capsized, righting: __sv.S.righting, btn: !document.getElementById('rightBtn').hidden, ov: !document.getElementById('capOverlay').hidden})")
        print("   La scuffia dopo R:", st); chk_ok(st["cap"] and not st["righting"] and not st["btn"] and not st["ov"], "L6 scuffia: R non raddrizza, pulsante e riquadro nascosti")
        await pg.evaluate("__sv.showStep(3)"); await pg.evaluate("__sv.panel()")
        st = await pg.evaluate("({cap: __sv.S.capsized, btn: !document.getElementById('rightBtn').hidden, ov: !document.getElementById('capOverlay').hidden, done: __sv.stepDone})")
        print("   Raddrizzare, avvio:", st); chk_ok(st["cap"] and st["btn"] and st["ov"] and not st["done"], "L6 raddrizzare: parte rovesciata, con pulsante e riquadro")
        await pg.click("#lRetry"); await pg.evaluate("__sv.panel()")
        st = await pg.evaluate("({cap: __sv.S.capsized, btn: !document.getElementById('rightBtn').hidden})")
        print("   Raddrizzare dopo Ricomincia:", st); chk_ok(st["cap"] and st["btn"], "L6 raddrizzare dopo Ricomincia: di nuovo rovesciata")
        await pg.evaluate("__sv.showStep(2)"); st = await pg.evaluate("({cap: __sv.S.capsized})")
        chk_ok(not st["cap"], "L6 scuffia: tornando indietro la barca è dritta (niente blocco)")
        await pg.evaluate("__sv.showStep(3)"); await pg.evaluate('() => { L.tasto("keydown", "r"); L.tasto("keyup", "r"); }')
        await wait_until(pg, 8, "L6 raddrizzare (partendo da dritta)")
        print(f"controlli vero/falso: {sum(NUOVI)} su {len(NUOVI)}" + ("" if all(NUOVI) and NUOVI else "  <-- DA CONTROLLARE"))
        print("errori:", errs[:5])
        await b.close()
asyncio.run(main())
