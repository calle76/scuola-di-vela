# Suggerimento della vela alle andature portanti: a scotta tutta lascata il pannello non deve piu dire
# «lasca» ne «troppo cazzata», perche oltre circa 112 gradi di vento apparente nessuna posizione della randa
# da i filetti dritti. Verifica anche che il testo nuovo NON compaia quando la scotta non e al massimo,
# e il caso peggiore dell'altezza del pannello con i testi piu lunghi.
# Dalla 0.20.1 anche la barca che arretra: il pilota legge il suggerimento, preme le frecce come un giocatore e deve uscire
# dall'angolo morto (tre casi delle registrazioni, due mure, scotta 100 e 50, 10 semi: 120 prove).
# Uso: python collaudo_suggerimento.py [larghezza altezza]   (predefinito 1360 650)
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1360, 650)
NUOVO = "Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono."
INDIETRO = "Stai andando all'indietro: la barra funziona al contrario. Spingila verso il boma; centrala quando riparti."
# 3c) barca che arretra (0.20.1): i tre casi delle registrazioni di Ale (twa, nodi), su tutte e due le mure
ARRETRA = [("caso 1", 38, -0.1), ("caso 2", 42, -0.8), ("caso 3", 25, -1.7)]
SEMI = 10
# pilota dentro la pagina: legge il suggerimento come un giocatore e preme i tasti veri (frecce, spazio per centrare).
# Finché il suggerimento dice «Spingila verso il boma» tiene premuta la freccia dalla parte del boma (frecce = barra, predefinito);
# quando smette, rilascia e centra con lo spazio. La scotta resta dov'è. Esce = prua ad almeno 45° dal vento e barca che va avanti.
PILOTA_INDIETRO = """([twa,kn,sh,seme])=>new Promise(fine=>{
 (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
 const S=__sv.S; S.h=(__sv.twd-twa+360)%360; S.u=kn/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
 const tasto=(t,k)=>dispatchEvent(new KeyboardEvent(t,{key:k})), ta=()=>Math.abs(((__sv.twd-S.h)%360+540)%360-180);
 const a0=ta(); let premuto=null, visto=false, amin=a0, t0=performance.now();
 const id=setInterval(()=>{
  const h=document.getElementById("hint").textContent, vuole=h.includes("Spingila verso il boma")?(S.boomSide<0?"ArrowLeft":"ArrowRight"):null;
  if(vuole) visto=true;
  if(vuole!==premuto){ if(premuto) tasto("keyup",premuto); if(vuole) tasto("keydown",vuole); else { tasto("keydown"," "); tasto("keyup"," "); } premuto=vuole; }
  amin=Math.min(amin,ta()); const esce=ta()>=45&&S.u>0.05, sec=(performance.now()-t0)/1000;
  if(esce||sec>12){ clearInterval(id); if(premuto) tasto("keyup",premuto); fine({a0:Math.round(a0),amin:Math.round(amin),visto,esce,sec:+sec.toFixed(2)}); }
 },15);})"""
VECCHI = ("Si agita il filetto sottovento", "troppo cazzata")
PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
TESTI = {  # caso peggiore del pannello: testo nuovo contro il piu lungo che il gioco mostra gia
    "nuovo": NUOVO,
    "lee attuale": "Si agita il filetto sottovento: lasca, oppure orza.",
    "raffica": "Raffica in arrivo: se la barca sbanda troppo, lasca; altrimenti è un'occasione per andare più veloci.",
    "sbandi con vela tutta lasca": "Sbandi troppo e la vela è già tutta lasca: prova a orzare un poco.",
    "all'indietro (0.20.1)": INDIETRO,
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
        # 3b) sbandamento oltre 25 gradi: con la scotta tutta lascata il testo nuovo, altrimenti «lasca la scotta»
        await pg.evaluate("__sv.startMission(1, 0)"); await pg.wait_for_timeout(300)
        SB = "Sbandi troppo e la vela è già tutta lasca: prova a orzare un poco."
        n_sb = 0
        for sh, atteso in ((1.0, SB), (0.6, "Sbandi troppo: lasca la scotta")):
            for twa in (60, 100, 140):
                await pg.evaluate("([twa,sh])=>{const S=__sv.S; S.h=(__sv.twd+twa)%360; __sv.ctl.sheet=sh; S.heel=40;}", [twa, sh])
                await pg.wait_for_timeout(120)
                letto = await pg.evaluate("__sv.S.heel > 25 ? document.getElementById('hint').textContent : null")
                if letto is None: continue
                n_sb += 1
                if not letto.startswith(atteso.rstrip(".")) or (sh < 1 and "già tutta lasca" in letto): sbagliati.append(f"sbandamento, scotta {sh} a twa {twa}: «{letto}»")
        # 3c) barca che arretra: il pilota segue il suggerimento ed esce dall'angolo morto (gioco libero, raffiche moderate, semi fissi)
        await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(300); await pg.evaluate("__sv.fast(4)")
        n_ind = n_ind_esce = 0; tempi = []
        for nome, twa, kn in ARRETRA:
            for mure, segno in (("dritta", 1), ("sinistra", -1)):
                for sh in (1.0, 0.5):
                    for seme in range(1, SEMI + 1):
                        r = await pg.evaluate(PILOTA_INDIETRO, [segno * twa, kn, sh, seme])
                        if not r["visto"]: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: suggerimento mai comparso"); continue
                        n_ind += 1
                        if r["esce"] and r["amin"] >= r["a0"] - 3: n_ind_esce += 1; tempi.append(r["sec"] * 4)
                        else: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: non esce {r}")
        await pg.evaluate("__sv.fast(1)")
        print(f"all'indietro: {n_ind} prove col suggerimento, {n_ind_esce} uscite; tempo simulato per uscire "
              f"{min(tempi, default=0):.1f}-{max(tempi, default=0):.1f} s (circa: misurato in tempo reale a velocità 4)")
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
              f"scotta 0,90-0,99 {n_quasi} (di cui in stallo {n_quasi_lee}), suggerimento semplice {n_sail}, sbandamento {n_sb}, pannello {n_pan}")
        print("eccesso massimo del pannello (pixel):", peggio)
        print("casi sbagliati:", sbagliati or "nessuno")
        print("errori pagina:", errs[:5])
        vuoto = [n for n in (n_lee, n_altro, n_quasi, n_quasi_lee, n_sail, n_sb, n_ind, n_pan) if n == 0]
        if vuoto: print("COLLAUDO NON VALIDO: una delle misure non ha nessun caso")
        if not caratteri_ok: print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, i margini del pannello misurati sopra non sono attendibili")
        await b.close()
        sys.exit(1 if (sbagliati or errs or vuoto or not caratteri_ok) else 0)
asyncio.run(main())
