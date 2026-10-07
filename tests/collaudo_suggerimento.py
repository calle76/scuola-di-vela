# Suggerimento della vela alle andature portanti: a scotta tutta lascata il pannello non deve piu dire
# «lasca» ne «troppo cazzata», perche oltre circa 112 gradi di vento apparente nessuna posizione della randa
# da i filetti dritti. Verifica anche che il testo nuovo NON compaia quando la scotta non e al massimo,
# e il caso peggiore dell'altezza del pannello con i testi piu lunghi.
# Uso: python collaudo_suggerimento.py [larghezza altezza]   (predefinito 1360 650)
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1360, 650)
NUOVO = "Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono."
VECCHI = ("Si agita il filetto sottovento", "troppo cazzata")
PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
TESTI = {  # caso peggiore del pannello: testo nuovo contro il piu lungo che il gioco mostra gia
    "nuovo": NUOVO,
    "lee attuale": "Si agita il filetto sottovento: lasca, oppure orza.",
    "piu lungo di oggi": "Stai andando all'indietro: la barra funziona al contrario. Centra la barra e lascia che la prua poggi da sola.",
}
MIS = """(testi)=>{const p=document.querySelector('.panel'), h=document.getElementById('hint');
 if (h.hidden) return null; const vecchio=h.textContent, out={};
 for (const k in testi){ h.textContent=testi[k]; out[k]=[h.offsetHeight, p.scrollHeight-p.clientHeight]; }
 h.textContent=vecchio; return out;}"""

async def leggi(pg, twa, sheet):
    """Mette la barca a twa gradi dal vento con la scotta data, porta la fisica all'equilibrio e legge il pannello."""
    await pg.evaluate("([twa,sh])=>{const S=__sv.S; S.h=(__sv.twd+twa)%360; S.u=1.5; S.vl=0; S.r=0; S.heel=0; S.heelRate=0;"
                      " __sv.ctl.sheet=sh; __sv.ctl.tiller=0;}", [twa, sheet])
    await pg.evaluate("__sv.run(1/60, 600)")   # 10 s a passi fissi: niente dipende dalla velocita del computer
    await pg.wait_for_timeout(250)             # il pannello si aggiorna 10 volte al secondo
    I = await pg.evaluate("(()=>{const i=__sv.readI();return{twa:i.twa,tt:i.tt,sheet:i.sheet,boom:Math.round(__sv.S.boom)}})()")
    return I, (await pg.inner_text("#hint")).strip()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        # i margini del pannello (punto 4 sotto) valgono solo se i caratteri veri del gioco sono caricati:
        # con i font di sistema le misure di larghezza/altezza del testo sono diverse e la prova non direbbe niente di vero.
        await pg.evaluate("document.fonts.ready")
        caratteri = await pg.evaluate("""() => ({
            "barlow 700": document.fonts.check('700 16px "Barlow Semi Condensed"'),
            "barlow 600": document.fonts.check('600 16px "Barlow Semi Condensed"'),
            "source serif 400": document.fonts.check('400 16px "Source Serif 4"'),
            "facce Barlow presenti e caricate (check() da solo dà vero anche senza)": [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"),
        })""")
        caratteri_ok = all(caratteri.values())
        print("caratteri del gioco caricati:", caratteri_ok, caratteri)
        # la prova 2 ha vento costante: nessuna raffica che copra il suggerimento
        await pg.evaluate("__sv.startMission(1, 0)"); await pg.wait_for_timeout(300)

        sbagliati = []
        # 1) scotta tutta lascata: dove i filetti dicono «lee» deve comparire il testo nuovo
        n_lee = n_altro = 0
        for twa in range(100, 185, 5):
            I, msg = await leggi(pg, twa, 1.0)
            if I["tt"] == "lee":
                n_lee += 1
                if msg != NUOVO: sbagliati.append(f"scotta 1,00 a twa {I['twa']:.0f}: «{msg}»")
            else:
                n_altro += 1
                if msg == NUOVO: sbagliati.append(f"scotta 1,00 a twa {I['twa']:.0f}, tt={I['tt']}: testo nuovo fuori posto")
        # 2) scotta non al massimo: il testo nuovo non deve comparire, e in stallo torna il consiglio di prima
        n_quasi = n_quasi_lee = 0
        for sh in (0.90, 0.93, 0.95, 0.97, 0.99):
            for twa in (140, 150, 160, 170, 180):
                I, msg = await leggi(pg, twa, sh)
                n_quasi += 1
                if msg == NUOVO: sbagliati.append(f"scotta {sh:.2f} a twa {I['twa']:.0f}: testo nuovo con la scotta non al massimo")
                if I["tt"] == "lee":
                    n_quasi_lee += 1
                    if not any(v in msg for v in VECCHI): sbagliati.append(f"scotta {sh:.2f} a twa {I['twa']:.0f}: atteso il consiglio di prima, letto «{msg}»")
        # 3) suggerimento semplice (hintKind «sail»): lezione 3, passo «Poppa», vela automatica
        await pg.evaluate("__sv.openItem(['l',2])"); await pg.evaluate("__sv.showStep(4)"); await pg.click("#c")
        await pg.wait_for_timeout(200)
        n_sail = 0
        for twa in (150, 165, 179):
            I, msg = await leggi(pg, twa, 1.0)
            if I["tt"] == "lee":
                n_sail += 1
                if msg != NUOVO: sbagliati.append(f"lezione 3 «Poppa» a twa {I['twa']:.0f}: «{msg}»")
        # 4) caso peggiore del pannello, in ogni punto in cui il suggerimento e visibile
        peggio = {k: -1 for k in TESTI}; n_pan = 0
        async def pannello(nome):
            nonlocal n_pan
            r = await pg.evaluate(MIS, TESTI)
            if r is None: return
            n_pan += 1
            for k, (alt, ecc) in r.items():
                peggio[k] = max(peggio[k], ecc)
                if ecc > 0: sbagliati.append(f"pannello in {nome} con «{k}»: +{ecc} px")
        for li, n in enumerate([13, 7, 13, 5, 9, 5]):
            await pg.evaluate(f"__sv.openItem(['l',{li}])")
            for k in range(n):
                await pg.evaluate(f"__sv.showStep({k})"); await pg.wait_for_timeout(80)
                await pannello(f"lezione {li+1} passo {k+1}")
        for it, nome in [("['m',0]", "prova 1"), ("['m',4]", "prova 5"), ("'free'", "navigazione libera")]:
            await pg.evaluate(f"__sv.openItem({it})"); await pg.wait_for_timeout(400); await pannello(nome)
        await pg.screenshot(path=str(OUT / f"S_suggerimento_{W}x{H}.png"))

        # Un controllo che non misura niente passa sempre: qui i casi vanno dichiarati e devono essere piu di zero.
        print(f"finestra {W}x{H}")
        print(f"casi misurati: scotta 1,00 con «lee» {n_lee}, scotta 1,00 con altri filetti {n_altro}, "
              f"scotta 0,90-0,99 {n_quasi} (di cui in stallo {n_quasi_lee}), suggerimento semplice {n_sail}, pannello {n_pan}")
        print("eccesso massimo del pannello (pixel):", peggio)
        print("casi sbagliati:", sbagliati or "nessuno")
        print("errori pagina:", errs[:5])
        vuoto = [n for n in (n_lee, n_altro, n_quasi, n_quasi_lee, n_sail, n_pan) if n == 0]
        if vuoto: print("COLLAUDO NON VALIDO: una delle misure non ha nessun caso")
        if not caratteri_ok: print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, i margini del pannello misurati sopra non sono attendibili")
        await b.close()
        sys.exit(1 if (sbagliati or errs or vuoto or not caratteri_ok) else 0)
asyncio.run(main())
