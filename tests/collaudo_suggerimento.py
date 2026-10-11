# Suggerimento della vela alle andature portanti: a scotta tutta lascata il pannello non deve piu dire
# «lasca» ne «troppo cazzata», perche oltre circa 112 gradi di vento apparente nessuna posizione della randa
# da i filetti dritti. Verifica anche che il testo nuovo NON compaia quando la scotta non e al massimo,
# e il caso peggiore dell'altezza del pannello con i testi piu lunghi.
# Dalla 0.20.1 anche la barca che arretra: il pilota legge il suggerimento, preme le frecce come un giocatore e deve uscire
# dall'angolo morto (tre casi delle registrazioni, due mure, scotta 100 e 50, 10 semi: 120 prove).
# Dalla 0.20.2 il suggerimento «all'indietro» compare anche nei passi di lezione a suggerimenti spenti, ma solo se il passo dà la barra:
# tabella fissa dei passi (3d) e lo stesso pilota dentro la lezione 5 passo 4 (3e).
# Dalla 0.20.2 il suggerimento ha fasi sulla soglia unica IRONS_A = 40° (rosa, registro e regola d'uscita del 5.4): sotto,
# «spingila verso il boma, poi centrala e cazza»; da 40° in su, «centra la barra e cazza», con isteresi: si torna al primo testo
# solo sotto 37°. Dopo aver arretrato, la barca che va avanti piano (sotto 1 nodo, prua da 37° in su) vede il testo B.
# Il pilota fa quello che legge; il caso 4 è la registrazione 0.20.2 (prua a 45°, scotta 100, barra al centro), e 3f controlla
# che una barca che arretra già sopra 45° veda subito il secondo testo. 3g: casi 6 (avanti piano dopo aver arretrato) e 7 (controllo).
# 3h: caso 8, la barca smette di arretrare con la prua sotto 37° e poi la prua sale (passo 3.11 della sessione 1749(3)); 3i: B sparisce
# dopo il tempo massimo di 10 s dalla fine dell'arretramento.
# Uso: python collaudo_suggerimento.py [larghezza altezza]   (predefinito 1360 650)
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1360, 650)
NUOVO = "Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono."
INDIETRO = "All'indietro la barra funziona al contrario: spingila verso il boma, poi centrala e cazza."                  # prua sotto 40°
INDIETRO2 = "Stai andando all'indietro, ma la prua è fuori dall'angolo morto: centra la barra e cazza."                   # da 40° in su (isteresi: fino a 37°)
AVANTI = "Ora vai avanti piano: barra al centro, cazza e lascia prendere velocità."                                    # testo B
# 3c) barca che arretra (0.20.1): i tre casi delle registrazioni di Ale (twa, nodi), su tutte e due le mure
ARRETRA = [("caso 1", 38, -0.1), ("caso 2", 42, -0.8), ("caso 3", 25, -1.7), ("caso 4 (registrazione 0.20.2)", 45, -0.5), ("caso 5", 46, -0.5)]
SEMI = 10
# pilota dentro la pagina: legge il suggerimento come un giocatore e preme i tasti veri (frecce, spazio per centrare).
# Finché il suggerimento dice «spingila verso il boma» tiene premuta la freccia dalla parte del boma (frecce = barra, predefinito);
# quando dice «centra la barra e cazza» (o il testo B) centra con lo spazio e tiene premuto ↑ finché il suggerimento resta; quando sparisce, rilascia.
# Esce = prua ad almeno 40° dal vento e barca che va avanti (regola del 5.4). Solo nel gioco libero (3c, ultimo argomento vero) l'uscita
# va tenuta 3 s simulati (S.time): criterio aggiunto nella 0.20.2 DOPO aver visto i risultati (158-160 uscite su 160 con la vecchia regola
# a 45°, barche ripartite che navigavano di bolina a 41-44° nelle raffiche).
# Lampeggio: ogni ritorno dal secondo al primo testo si registra con la prua letta prima e dopo; è un errore se entrambe sono da 37° in su.
PILOTA_INDIETRO = """([twa,kn,sh,seme,libero])=>new Promise(fine=>{
 (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
 const S=__sv.S; S.h=(__sv.twd-twa+360)%360; S.u=kn/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
 const tasto=(t,k)=>dispatchEvent(new KeyboardEvent(t,{key:k})), ta=()=>Math.abs(((__sv.twd-S.h)%360+540)%360-180);
 const a0=ta(); let fuori40=null, premuto=null, visto=false, visto1=false, visto2=false, primo=0, ultimo=0, aprec=a0, alti=0, bassi=0, amin=a0, t0=performance.now();
 const id=setInterval(()=>{
  const el=document.getElementById("hint"), h=el.hidden?"":el.textContent, uno=h.includes("spingila verso il boma"), due=h.includes("centra la barra e cazza"), avanti=h.includes("barra al centro, cazza");
  const vuole=uno?(S.boomSide<0?"ArrowLeft":"ArrowRight"):(due||avanti)?"ArrowUp":null;
  if(uno) visto1=true; if(due) visto2=true; visto=visto1||visto2; const fase=uno?1:due?2:0;
  if(fase&&!primo) primo=fase; if(fase===1&&ultimo===2){ if(aprec>=37&&ta()>=37) alti++; else bassi++; } if(fase) ultimo=fase; aprec=ta();
  if(vuole!==premuto){ if(premuto) tasto("keyup",premuto); if(vuole!=="ArrowLeft"&&vuole!=="ArrowRight"){ tasto("keydown"," "); tasto("keyup"," "); } if(vuole) tasto("keydown",vuole); premuto=vuole; }
  amin=Math.min(amin,ta()); if(ta()>=40&&S.u>0.05){ if(fuori40===null) fuori40=S.time; } else fuori40=null;
  const esce=libero?(fuori40!==null&&S.time-fuori40>=3):(ta()>=40&&S.u>0.05), sec=(performance.now()-t0)/1000;
  if(esce||sec>12){ clearInterval(id); if(premuto) tasto("keyup",premuto); fine({a0:Math.round(a0),amin:Math.round(amin),visto,visto1,visto2,primo,alti,bassi,esce,sec:+sec.toFixed(2),scotta:+__sv.ctl.sheet.toFixed(2)}); }
 },15);})"""
# 3d) passi di lezione (lezione, titolo, riquadro atteso visibile): a suggerimenti spenti con la barra, senza barra, e un passo normale
PASSI_INDIETRO = [(3, "Filetto sopravento", False), (3, "Filetti dritti", False), (3, "Filetto sottovento", False),
                  (3, "Poggi e laschi", True), (3, "Orzi e cazzi", True), (4, "Da fermi", False),
                  (5, "Una virata che non riesce", True), (5, "Strambata violenta", True), (5, "Strambata controllata", True),
                  (5, "Risalire il vento", True)]
VECCHI = ("Si agita il filetto sottovento", "troppo cazzata")
PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
TESTI = {  # caso peggiore del pannello: testo nuovo contro il piu lungo che il gioco mostra gia
    "nuovo": NUOVO,
    "lee attuale": "Si agita il filetto sottovento: lasca, oppure orza.",
    "raffica": "Raffica in arrivo: se la barca sbanda troppo, lasca; altrimenti è un'occasione per andare più veloci.",
    "sbandi con vela tutta lasca": "Sbandi troppo e la vela è già tutta lasca: prova a orzare un poco.",
    "all'indietro, primo testo (0.20.2)": INDIETRO,
    "all'indietro, secondo testo (0.20.2)": INDIETRO2,
    "avanti piano dopo aver arretrato (0.20.2)": AVANTI,
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
        n_ind = n_ind_esce = n_passaggi = n_alti = n_bassi = 0; tempi = []
        for nome, twa, kn in ARRETRA:
            for mure, segno in (("dritta", 1), ("sinistra", -1)):
                for sh in (1.0, 0.5):
                    for seme in range(1, SEMI + 1):
                        r = await pg.evaluate(PILOTA_INDIETRO, [segno * twa, kn, sh, seme, True])
                        if not r["visto"]: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: suggerimento mai comparso"); continue
                        n_ind += 1
                        if r["esce"] and r["amin"] >= r["a0"] - 3: n_ind_esce += 1; tempi.append(r["sec"] * 4)
                        else: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: non esce {r}")
                        n_alti += r["alti"]; n_bassi += r["bassi"]
                        if r["alti"]: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: ritorno al primo testo con la prua da 37° in su {r}")
                        if twa >= 40 and (r["visto1"] or not r["visto2"]): sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: atteso solo il secondo testo {r}")
                        if twa < 40:
                            if r["primo"] == 1 and r["visto2"]: n_passaggi += 1
                            else: sbagliati.append(f"all'indietro {nome} mure a {mure} scotta {sh} seme {seme}: atteso il primo testo e poi il secondo {r}")
        await pg.evaluate("__sv.fast(1)")
        # 3d) passi di lezione: barca a 38 gradi dal vento che arretra a 1 nodo, riquadro del suggerimento visibile solo se il passo dà la barra
        n_passi = 0
        for li, titolo, atteso in PASSI_INDIETRO:
            await pg.evaluate(f"__sv.openItem(['l',{li-1}])")
            k = await pg.evaluate("(t)=>{for(let k=0;k<20;k++){__sv.showStep(k);if(document.getElementById('lTitle').textContent===t)return k;}return -1}", titolo)
            if k < 0: sbagliati.append(f"lezione {li}: passo «{titolo}» non trovato"); continue
            await pg.click("#c")
            await pg.evaluate("()=>{const S=__sv.S; S.h=(__sv.twd-38+360)%360; S.u=-1/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.tiller=0;}")
            await pg.wait_for_timeout(300)
            r = await pg.evaluate("({u:__sv.S.u, vis:!document.getElementById('hint').hidden, txt:document.getElementById('hint').textContent})")
            if r["u"] >= -0.05: sbagliati.append(f"lezione {li} «{titolo}»: la barca non arretra più ({r['u']:.2f} m/s), caso non misurato"); continue
            n_passi += 1
            if r["vis"] != atteso or (atteso and r["txt"] != INDIETRO):   # 38° dal vento: primo testo
                sbagliati.append(f"lezione {li} «{titolo}»: atteso {'visibile' if atteso else 'nascosto'}, letto visibile={r['vis']} «{r['txt']}»")
        print(f"all'indietro nei passi di lezione: {n_passi} passi misurati su {len(PASSI_INDIETRO)}")
        # 3e) lezione 5 passo 4 (suggerimenti spenti): lo stesso pilota esce seguendo il suggerimento. Niente raffiche: un seme basta
        n_l5 = n_l5_esce = 0
        for nome, twa, kn in ARRETRA:
            for mure, segno in (("dritta", 1), ("sinistra", -1)):
                for sh in (1.0, 0.5):
                    await pg.evaluate("__sv.openItem(['l',4])"); await pg.evaluate("__sv.showStep(3)"); await pg.click("#c"); await pg.evaluate("__sv.fast(4)")
                    r = await pg.evaluate(PILOTA_INDIETRO, [segno * twa, kn, sh, 1, False])
                    await pg.evaluate("__sv.fast(1)")
                    if not r["visto"]: sbagliati.append(f"lezione 5 passo 4, {nome} mure a {mure} scotta {sh}: suggerimento mai comparso"); continue
                    n_l5 += 1
                    if r["esce"] and r["amin"] >= r["a0"] - 3: n_l5_esce += 1
                    else: sbagliati.append(f"lezione 5 passo 4, {nome} mure a {mure} scotta {sh}: non esce {r}")
                    n_alti += r["alti"]; n_bassi += r["bassi"]
                    if r["alti"]: sbagliati.append(f"lezione 5 passo 4, {nome} mure a {mure} scotta {sh}: ritorno al primo testo con la prua da 37° in su {r}")
        print(f"lezione 5 passo 4 (regola del 5.4, 40°): {n_l5} prove col suggerimento su {len(ARRETRA) * 4}, {n_l5_esce} uscite")
        # 3f) barca che arretra già sopra 45°: il primo suggerimento «all'indietro» che compare deve essere il secondo testo
        PRIMO = """([twa,kn])=>new Promise(fine=>{const S=__sv.S; S.h=(__sv.twd-twa+360)%360; S.u=kn/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.tiller=0; __sv.ctl.sheet=1;
          const t0=performance.now(), id=setInterval(()=>{const el=document.getElementById('hint'), h=el.hidden?'':el.textContent;
          if(h.includes("all'indietro")||performance.now()-t0>3000){clearInterval(id); fine(h);}},10);})"""
        n_sopra = 0
        for luogo, apri in (("navigazione libera", "__sv.openItem('free')"), ("lezione 5 passo 4", "__sv.openItem(['l',4]); __sv.showStep(3)")):
            for twa in (46, 50, 55, -46, -50, -55):
                await pg.evaluate(apri); await pg.click("#c"); await pg.wait_for_timeout(100)
                letto = await pg.evaluate(PRIMO, [twa, -0.8]); n_sopra += 1
                if letto != INDIETRO2: sbagliati.append(f"{luogo}, arretra a {twa} gradi: primo testo «{letto}», atteso il secondo")
        print(f"barca che arretra già sopra 45°: {n_sopra} casi")
        # 3g) caso 6: la barca arretra (0,2 s a −0,3 nodi), poi va avanti piano (0,3 nodi) a 41-44°: il testo B deve comparire entro 0,5 s
        # simulati (misurati a velocità 1), il pilota fa quello che dice (centra e cazza) e deve superare 1 nodo entro 30 s simulati,
        # poi B deve sparire. Caso 7 (controllo): barca nuova che va avanti a 43° e 0,5 nodi senza aver mai arretrato: B mai, per 5 s simulati.
        CASO6 = """([twa,sh,seme])=>new Promise(fine=>{
         (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
         const S=__sv.S, ta=()=>Math.abs(((__sv.twd-S.h)%360+540)%360-180), tasto=(t,k)=>dispatchEvent(new KeyboardEvent(t,{key:k}));
         S.h=(__sv.twd-twa+360)%360; S.u=-0.3/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
         __sv.run(1/60,12); const fase_prima=S.indietro; S.u=0.3/1.944; const t0=S.time; let tB=null, t1=null, tVia=null, premuto=false, a6=ta();
         const id=setInterval(()=>{
          const el=document.getElementById("hint"), h=el.hidden?"":el.textContent, b=h.includes("barra al centro, cazza");
          if(b&&tB===null){ tB=S.time-t0; __sv.fast(4); tasto("keydown"," "); tasto("keyup"," "); tasto("keydown","ArrowUp"); premuto=true; }
          if(tB!==null&&t1===null&&S.u*1.944>=1){ t1=S.time-t0; tasto("keyup","ArrowUp"); premuto=false; }
          if(t1!==null&&!b&&tVia===null) tVia=S.time-t0;
          const fine_=tVia!==null||(tB===null&&S.time-t0>2)||S.time-t0>31||(t1!==null&&S.time-t0-t1>2);
          if(fine_){ clearInterval(id); if(premuto) tasto("keyup","ArrowUp"); __sv.fast(1);
           fine({fase_prima,a6:Math.round(a6),tB,t1,tVia,sheet:+__sv.ctl.sheet.toFixed(2)}); }
         },15);})"""
        CASO7 = """([sh,seme])=>new Promise(fine=>{
         (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
         const S=__sv.S; S.h=(__sv.twd-43+360)%360; S.u=0.5/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
         const t0=S.time; let b=false, umin=S.u, fase0=S.indietro;
         const id=setInterval(()=>{ const el=document.getElementById("hint"); if(!el.hidden&&el.textContent.includes("barra al centro, cazza")) b=true;
          umin=Math.min(umin,S.u); if(S.time-t0>=5){ clearInterval(id); fine({b,fase0,arretrata:umin<-0.05}); } },15);})"""
        n_c6 = n_c6_ok = n_c7 = 0
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                for seme in range(1, SEMI + 1):
                    twa6 = 41 + seme % 4
                    await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(150)
                    r = await pg.evaluate(CASO6, [segno * twa6, sh, seme]); n_c6 += 1
                    if r["fase_prima"] != 2: sbagliati.append(f"caso 6 {twa6}° mure a {mure} scotta {sh} seme {seme}: la barca non risultava all'indietro prima {r}")
                    elif r["tB"] is None or r["tB"] > 0.5: sbagliati.append(f"caso 6 {twa6}° mure a {mure} scotta {sh} seme {seme}: B non comparso entro 0,5 s {r}")
                    elif r["t1"] is None or r["t1"] > 30: sbagliati.append(f"caso 6 {twa6}° mure a {mure} scotta {sh} seme {seme}: non supera 1 nodo entro 30 s {r}")
                    elif r["tVia"] is None: sbagliati.append(f"caso 6 {twa6}° mure a {mure} scotta {sh} seme {seme}: B non sparisce sopra 1 nodo {r}")
                    else: n_c6_ok += 1
                    await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(150)
                    r = await pg.evaluate(CASO7, [sh, seme])
                    if r["arretrata"] or r["fase0"]: sbagliati.append(f"caso 7 mure a {mure} scotta {sh} seme {seme}: non misurato (la barca ha arretrato o lo stato non era zero) {r}"); continue
                    n_c7 += 1
                    if r["b"]: sbagliati.append(f"caso 7 mure a {mure} scotta {sh} seme {seme}: testo B senza aver arretrato")
        print(f"caso 6 (avanti piano dopo aver arretrato): {n_c6_ok} riusciti su {n_c6}; caso 7 (controllo): {n_c7} prove misurate")
        # 3h) caso 8 (0.20.2, dopo il collaudo a mano, sessione 1749(3) passo 3.11): la barca arretra con la prua a 30-36° (stato 1),
        # smette di arretrare (+0,3 nodi) ancora sotto 37°, poi il pilota la fa poggiare con la barra sopravento finché la prua è ad almeno 37°
        # e centra. Criteri dichiarati prima dei risultati: B entro 0,5 s simulati dal primo istante con prua >= 37° e barca sotto 1 nodo,
        # misurato a velocità 1; la barca supera 1 nodo entro 30 s e B sparisce entro 0,5 s da lì. Non misurata (contata a parte) se la barca
        # supera 1 nodo prima che la prua arrivi a 37°, o se la prua ci arriva dopo più di 10 s (tempo massimo della fase 3).
        CASO8 = """([twa,sh,seme])=>new Promise(fine=>{
         (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
         const S=__sv.S, ta=()=>Math.abs(((__sv.twd-S.h)%360+540)%360-180), tasto=(t,k)=>dispatchEvent(new KeyboardEvent(t,{key:k}));
         S.h=(__sv.twd-twa+360)%360; S.u=-0.3/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
         __sv.run(1/60,12); const fase_prima=S.indietro; S.u=0.3/1.944; const t0=S.time, a8=ta();
         let premuto=S.boomSide<0?"ArrowRight":"ArrowLeft"; tasto("keydown",premuto);
         let tA=null, tB=null, t1=null, tVia=null, nonmis=null;
         const id=setInterval(()=>{
          const el=document.getElementById("hint"), h=el.hidden?"":el.textContent, b=h.includes("barra al centro, cazza"), t=S.time-t0, kn=S.u*1.944;
          if(tA===null){
           if(ta()>=37){ if(premuto){ tasto("keyup",premuto); premuto=null; } tasto("keydown"," "); tasto("keyup"," "); if(kn<1) tA=t; }
           if(kn>=1&&tA===null) nonmis="supera 1 nodo prima dei 37°"; else if(t>10&&tA===null) nonmis="prua non a 37° entro 10 s";
          }
          if(tA!==null&&b&&tB===null){ tB=t; tasto("keydown"," "); tasto("keyup"," "); premuto="ArrowUp"; tasto("keydown",premuto); }
          if(tB!==null&&t1===null&&kn>=1){ t1=t; if(premuto){ tasto("keyup",premuto); premuto=null; } }
          if(t1!==null&&!b&&tVia===null) tVia=t;
          if(nonmis||tVia!==null||(tA!==null&&tB===null&&t-tA>2)||t>31||(t1!==null&&t-t1>2)){ clearInterval(id); if(premuto) tasto("keyup",premuto);
           fine({fase_prima,a8:Math.round(a8),tA,tB,t1,tVia,nonmis}); }
         },15);})"""
        n_c8 = n_c8_ok = 0; c8_nonmis = []
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                for seme in range(1, SEMI + 1):
                    twa8 = 30 + seme % 7
                    await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(150)
                    r = await pg.evaluate(CASO8, [segno * twa8, sh, seme])
                    nome8 = f"caso 8 {twa8}° mure a {mure} scotta {sh} seme {seme}"
                    if r["fase_prima"] != 1: c8_nonmis.append(f"{nome8}: la barca non risultava all'indietro sotto 40° {r}"); continue
                    if r["nonmis"]: c8_nonmis.append(f"{nome8}: {r['nonmis']} {r}"); continue
                    n_c8 += 1
                    if r["tB"] is None or r["tB"] - r["tA"] > 0.5: sbagliati.append(f"{nome8}: B non comparso entro 0,5 s {r}")
                    elif r["t1"] is None or r["t1"] > 30: sbagliati.append(f"{nome8}: non supera 1 nodo entro 30 s {r}")
                    elif r["tVia"] is None or r["tVia"] - r["t1"] > 0.5: sbagliati.append(f"{nome8}: B non sparisce entro 0,5 s sopra 1 nodo {r}")
                    else: n_c8_ok += 1
        print(f"caso 8 (smette di arretrare sotto 37°, poi la prua sale): {n_c8_ok} riusciti su {n_c8} misurati; non misurati {len(c8_nonmis)}")
        for x in c8_nonmis: print("   non misurato:", x)
        if n_c8 < 40: print(f"COLLAUDO NON VALIDO: caso 8 con {n_c8} prove misurate su 40")
        # 3i) tempo massimo della fase 3: la barca arretra (0,2 s), poi è tenuta a +0,3 nodi con la prua a 40° (velocità e prua rimesse
        # ogni 15 ms). B deve sparire fra 10 e 10,5 s simulati dalla fine dell'arretramento. 4 prove: 2 mure x 2 scotte.
        TMAX = """([twa,sh])=>new Promise(fine=>{
         const S=__sv.S, h0=(__sv.twd-twa+360)%360; S.h=h0; S.u=-0.3/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; __sv.ctl.sheet=sh; __sv.ctl.tiller=0;
         __sv.run(1/60,12); S.u=0.3/1.944; const t0=S.time; let visto=false, tVia=null;
         const id=setInterval(()=>{ S.u=0.3/1.944; S.h=h0; S.r=0; const el=document.getElementById("hint"), b=!el.hidden&&el.textContent.includes("barra al centro, cazza"), t=S.time-t0;
          if(b) visto=true; if(visto&&!b&&tVia===null) tVia=t; if(tVia!==null||t>13){ clearInterval(id); fine({visto,tVia}); } },15);})"""
        n_tmax = 0
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                await pg.evaluate("__sv.openItem('free')"); await pg.wait_for_timeout(150)
                r = await pg.evaluate(TMAX, [segno * 40, sh]); n_tmax += 1
                if not r["visto"] or r["tVia"] is None or not (10 <= r["tVia"] <= 10.5): sbagliati.append(f"tempo massimo mure a {mure} scotta {sh}: atteso B sparito fra 10 e 10,5 s {r}")
                print(f"tempo massimo mure a {mure} scotta {sh}: {r}")
        print(f"ritorni dal secondo al primo testo: con la prua da 37° in su {n_alti}, sotto 37° {n_bassi}")
        print(f"all'indietro: prove in cui il pilota ha letto prima il primo testo e poi il secondo: {n_passaggi}")
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
        vuoto = [n for n in (n_lee, n_altro, n_quasi, n_quasi_lee, n_sail, n_sb, n_ind, n_passaggi, n_passi, n_l5, n_sopra, n_c6, n_c7, n_c8, n_tmax, n_pan) if n == 0]
        if vuoto: print("COLLAUDO NON VALIDO: una delle misure non ha nessun caso")
        if not caratteri_ok: print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, i margini del pannello misurati sopra non sono attendibili")
        await b.close()
        sys.exit(1 if (sbagliati or errs or vuoto or not caratteri_ok or n_c8 < 40) else 0)
asyncio.run(main())
