# Suggerimento della vela alle andature portanti: a scotta tutta lascata il pannello non deve piu dire
# «lasca» ne «troppo cazzata», perche oltre circa 112 gradi di vento apparente nessuna posizione della randa
# da i filetti dritti. Verifica anche che il testo nuovo NON compaia quando la scotta non e al massimo,
# e il caso peggiore dell'altezza del pannello con i testi piu lunghi.
# Dalla 0.20.1 anche la barca che arretra: il pilota legge il suggerimento, preme le frecce come un giocatore e deve uscire
# dall'angolo morto (cinque casi delle registrazioni, due mure, scotta 100 e 50).
# Dalla 0.20.2 il suggerimento «all'indietro» compare anche nei passi di lezione a suggerimenti spenti, ma solo se il passo dà la barra:
# tabella fissa dei passi (3d) e lo stesso pilota dentro la lezione 5 passo 4 (3e).
# Dalla 0.20.2 il suggerimento ha fasi sulla soglia unica IRONS_A = 40° (rosa, registro e regola d'uscita del 5.4): sotto,
# «spostala verso il boma, poi centrala e cazza»; da 40° in su, «centra la barra e cazza», con isteresi: si torna al primo testo
# solo sotto 37°. Dopo aver arretrato, la barca che va avanti piano (sotto 1 nodo, prua da 37° in su) vede il testo B.
# 3f: una barca che arretra già fuori dall'angolo morto (46-55°, soglia 40°) vede subito il secondo testo. 3g: casi 6 (avanti piano
# dopo aver arretrato) e 7 (controllo). 3h: caso 8, la barca smette di arretrare con la prua sotto 37° e poi la prua sale
# (passo 3.11 della sessione 1749(3)); 3i: B sparisce dopo il tempo massimo di 10 s dalla fine dell'arretramento.
# Dalla 0.20.3 le parti che guidano la barca (3c, 3e-3i) sono DETERMINISTICHE: ogni prova gira tutta dentro una sola chiamata
# alla pagina, con Math.random a seme fisso, gioco riaperto e simTime azzerato (__sv.simTime), passi fissi di 1/60 s (__sv.run)
# e il riquadro scritto ogni 0,1 s simulati (__sv.panel), come nel gioco a velocità 1. Il ciclo del browser non interviene.
# Due giri danno uscite identiche; la stessa prova dà lo stesso risultato nella versione veloce e in quella lunga.
# Uso: python collaudo_suggerimento.py [larghezza altezza] [--lungo] [--html=file]   (predefinito 1360 650, veloce: semi 1-2;
# --lungo: semi 1-20; --html: un altro index.html, per le contro-prove)
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
LUNGO = "--lungo" in sys.argv
HTML = next((pathlib.Path(a[7:]).resolve() for a in sys.argv[1:] if a.startswith("--html=")), pathlib.Path(__file__).resolve().parent.parent / "index.html")
BASE = HTML.as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
W, H = (int(ARGS[0]), int(ARGS[1])) if len(ARGS) > 1 else (1360, 650)
SEMI = range(1, 21) if LUNGO else range(1, 3)   # semi fissi, decisi prima dei risultati (0.20.3)
CONTRARIO = False                               # solo per la contro-prova P1: il pilota spinge la barra lontano dal boma
NUOVO = "Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono."
INDIETRO = "All'indietro la barra funziona al contrario: spostala verso il boma, poi centrala e cazza."                  # prua sotto 40°
INDIETRO2 = "Stai andando all'indietro, ma la prua è fuori dall'angolo morto: centra la barra e cazza."                   # da 40° in su (isteresi: fino a 37°)
AVANTI = "Ora vai avanti piano: barra al centro, cazza e lascia prendere velocità."                                    # testo B
# 3c) barca che arretra: i casi delle registrazioni di Ale (twa, nodi), su tutte e due le mure
ARRETRA = [("caso 1", 38, -0.1), ("caso 2", 42, -0.8), ("caso 3", 25, -1.7), ("caso 4 (registrazione 0.20.2)", 45, -0.5), ("caso 5", 46, -0.5)]
# Attrezzi comuni dentro la pagina. T.prova: seme, gioco riaperto (gioco libero o lezione 5 passo 4), simTime a zero, barca messa
# a twa gradi dal vento con la velocità e la scotta date. Ogni pilota avanza a passi di 1/60 s e ogni 6 passi (0,1 s simulati)
# fa scrivere il riquadro con __sv.panel() e lo legge, solo se visibile, come un giocatore.
ATTREZZI = """()=>{ const sv=__sv, T={};
 T.lato=()=>((sv.twd-sv.S.h)%360+540)%360-180; T.ta=()=>Math.abs(T.lato());
 T.tasto=(t,k)=>dispatchEvent(new KeyboardEvent(t,{key:k}));
 T.su=()=>{ for(const k of ["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"]) T.tasto("keyup",k); };
 T.hint=()=>{ const el=document.getElementById("hint"); return el.hidden?"":el.textContent; };
 T.r2=x=>x===null?null:+x.toFixed(2);
 T.prova=(seme,dove,twa,kn,sh)=>{
  (s=>{Math.random=()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}})(seme);
  T.su(); if(dove==="free") sv.openItem("free"); else { sv.openItem(["l",4]); sv.showStep(3); }
  sv.simTime=0; T.capRisc=false;
  // 0.20.3, riscaldamento (60 s simulati, fissato prima dei risultati): nel gioco libero le raffiche nascono in posizioni casuali e
  // passano sulla barca. Senza, le 4 raffiche iniziali (posizioni fisse, index.html:904) non la raggiungono mai durante la prova
  // e il seme non cambia niente. Dopo, la barca torna nello stato del caso, raddrizzata e senza fasi del suggerimento.
  if(dove==="free"){ sv.run(1/60,3600); const S=sv.S; T.capRisc=S.capsized; S.capsized=false; S.righting=0; S.indietro=0; S.indietroT=0; }
  const S=sv.S; S.h=(sv.twd-twa+360)%360; S.u=kn/1.944; S.vl=0; S.r=0; S.heel=0; S.heelRate=0; sv.ctl.sheet=sh; sv.ctl.tiller=0; };
 window.__T=T; }"""
# Pilota che segue il suggerimento (3c, 3e): finché legge «spostala verso il boma» tiene la freccia dalla parte del boma;
# con «centra la barra e cazza» o il testo B centra (spazio) e tiene ↑; quando il testo sparisce rilascia.
# Misura, a ogni passo: primo istante all'indietro, mura (lato del vento con segno), uscita con la regola del 5.4
# (prua ad almeno 40° e barca che va avanti, tenuta 1 s), primo istante a 1 nodo, passo completato (stepDone).
# A ogni lettura: primo testo «all'indietro», testi visti, ritorni dal secondo al primo testo, B ancora visibile oltre 0,5 s da 1 nodo.
SEGUI = """([seme,dove,twa,kn,sh,contrario])=>{ const T=__T, sv=__sv; T.prova(seme,dove,twa,kn,sh); const S=sv.S;
 const s0=Math.sign(T.lato())||1, a0=Math.round(T.ta());
 let premuto=null, tInd=null, tTesto=null, visto1=false, visto2=false, primo=0, ultimo=0, aprec=T.ta(), alti=0, bassi=0,
     latoMin=T.lato()*s0, hold=0, tEsce=null, t1=null, bTardi=false, tDone=null, t=0, f1t=null, fase1=false;
 for(let n=1;n<=1860;n++){
  sv.run(1/60,1); t=n/60; const a=T.ta(), l=T.lato()*s0, I=sv.readI();
  if((I.twa<40&&I.kn<0.4)||S.u<-0.1){ if(f1t===null) f1t=t; if(t-f1t>=1-1e-9) fase1=true; } else f1t=null;   // fase 1 del 5.4, ricalcolata come index.html:647
  if(tInd===null&&S.u<-0.05) tInd=t;
  latoMin=Math.min(latoMin,l);
  if(a>=40&&S.u>0.05){ hold+=1/60; if(tEsce===null&&hold>=1-1e-9) tEsce=t; } else hold=0;
  if(t1===null&&S.u*1.944>=1) t1=t;
  if(tDone===null&&sv.stepDone) tDone=t;
  if(n%6) continue;
  sv.panel(); const h=T.hint(), uno=h.includes("spostala verso il boma"), due=h.includes("centra la barra e cazza"), avanti=h.includes("barra al centro, cazza");
  if((uno||due)&&tTesto===null) tTesto=t; if(uno) visto1=true; if(due) visto2=true;
  const fase=uno?1:due?2:0; if(fase&&!primo) primo=fase; if(fase===1&&ultimo===2){ if(aprec>=37&&a>=37) alti++; else bassi++; } if(fase) ultimo=fase; aprec=a;
  if(avanti&&t1!==null&&t-t1>0.5+1e-9) bTardi=true;
  const verso=((S.boomSide<0)!==contrario)?"ArrowLeft":"ArrowRight", vuole=uno?verso:(due||avanti)?"ArrowUp":null;
  if(vuole!==premuto){ if(premuto) T.tasto("keyup",premuto); if(vuole!=="ArrowLeft"&&vuole!=="ArrowRight"){ T.tasto("keydown"," "); T.tasto("keyup"," "); } if(vuole) T.tasto("keydown",vuole); premuto=vuole; }
  if(dove==="free"?(tEsce!==null&&t1!==null&&t-Math.max(tEsce,t1)>=1):(tDone!==null&&t-tDone>=1)) break;
 }
 T.su();
 return {a0, tInd:T.r2(tInd), tTesto:T.r2(tTesto), visto1, visto2, primo, alti, bassi, latoMin:Math.round(latoMin), tEsce:T.r2(tEsce), t1:T.r2(t1), bTardi, tDone:T.r2(tDone), fase1, capRisc:T.capRisc, fine:T.r2(t), scotta:+sv.ctl.sheet.toFixed(3)}; }"""
# 3f) il primo testo «all'indietro» letto (uno qualunque dei tre) entro 3 s simulati
PRIMO = """([dove,twa])=>{ const T=__T, sv=__sv; T.prova(1,dove,twa,-0.8,1);
 for(let n=1;n<=180;n++){ sv.run(1/60,1); if(n%6) continue; sv.panel(); const h=T.hint();
  if(h.includes("spostala verso il boma")||h.includes("centra la barra e cazza")||h.includes("barra al centro, cazza")) return h; }
 return T.hint(); }"""
# 3g) caso 6: la barca arretra (0,2 s a −0,3 nodi), poi va avanti piano (0,3 nodi) a 41-44°; caso 7: barca nuova a 43° e 0,5 nodi
# (0.20.3, cambiato dopo i risultati: se una raffica la fa arretrare nei 5 s la prova è «non misurata», contata e stampata a parte)
CASO6 = """([seme,twa,sh])=>{ const T=__T, sv=__sv; T.prova(seme,"free",twa,-0.3,sh); const S=sv.S;
 sv.run(1/60,12); const fase_prima=S.indietro; S.u=0.3/1.944; const a6=Math.round(T.ta()); let tB=null, t1=null, tVia=null;
 for(let n=1;n<=1860;n++){ sv.run(1/60,1); const t=n/60; if(n%6) continue;
  sv.panel(); const b=T.hint().includes("barra al centro, cazza");
  if(b&&tB===null){ tB=t; T.tasto("keydown"," "); T.tasto("keyup"," "); T.tasto("keydown","ArrowUp"); }
  if(tB!==null&&t1===null&&S.u*1.944>=1){ t1=t; T.tasto("keyup","ArrowUp"); }
  if(t1!==null&&!b&&tVia===null) tVia=t;
  if(tVia!==null||(tB===null&&t>2)||(t1!==null&&t-t1>2)) break; }
 T.su(); return {fase_prima,a6,tB:T.r2(tB),t1:T.r2(t1),tVia:T.r2(tVia),sheet:+sv.ctl.sheet.toFixed(2)}; }"""
CASO7 = """([seme,sh])=>{ const T=__T, sv=__sv; T.prova(seme,"free",43,0.5,sh); const S=sv.S; let b=false, umin=S.u, tArr=null; const fase0=S.indietro;
 for(let n=1;n<=300;n++){ sv.run(1/60,1); umin=Math.min(umin,S.u); if(tArr===null&&S.u<-0.05) tArr=n/60; if(n%6) continue; sv.panel(); if(T.hint().includes("barra al centro, cazza")) b=true; }
 return {b,fase0,arretrata:umin<-0.05,tArr:T.r2(tArr),umin_kn:+(umin*1.944).toFixed(2),kn_fine:+(S.u*1.944).toFixed(2),twa_fine:Math.round(T.ta())}; }"""
# 3h) caso 8: arretra a 30-36°, smette di arretrare (+0,3 nodi) sotto 37°, il pilota poggia (barra sopravento) finché legge la prua
# ad almeno 37° e centra; da lì (0.20.3, deciso dopo i risultati) fa quello che legge nel riquadro, come il pilota SEGUI. tA (0.20.3, cambiato dopo i risultati) è il primo passo, dopo l'inversione, con la barca che va avanti
# (S.u > 0,05), prua >= 37° e sotto 1 nodo: se la barca torna ad arretrare non si aspetta B finché non riparte in avanti.
CASO8 = """([seme,twa,sh])=>{ const T=__T, sv=__sv; T.prova(seme,"free",twa,-0.3,sh); const S=sv.S;
 sv.run(1/60,12); const fase_prima=S.indietro; S.u=0.3/1.944; const a8=Math.round(T.ta());
 let premuto=S.boomSide<0?"ArrowRight":"ArrowLeft"; T.tasto("keydown",premuto);
 let centrato=false, tA=null, tAu=null, tB=null, t1=null, tVia=null, nonmis=null;
 for(let n=1;n<=1860;n++){ sv.run(1/60,1); const t=n/60, kn=S.u*1.944;
  if(tAu===null&&S.u>0.05) tAu=t;
  if(tA===null){ if(S.u>0.05&&T.ta()>=37&&kn<1) tA=t; else if(kn>=1) nonmis="supera 1 nodo prima dei 37°"; else if(t>10) nonmis="nessun istante avanti con prua >= 37° e sotto 1 nodo entro 10 s"; }
  if(nonmis) break;
  if(n%6) continue;
  sv.panel(); const b=T.hint().includes("barra al centro, cazza");
  if(!centrato&&(premuto==="ArrowLeft"||premuto==="ArrowRight")){ if(T.ta()>=37){ T.tasto("keyup",premuto); premuto=null; T.tasto("keydown"," "); T.tasto("keyup"," "); centrato=true; } }
  if(tA!==null&&b&&tB===null) tB=t;
  if(t1===null&&kn>=1) t1=t;
  if(centrato){ const h=T.hint(), uno=h.includes("spostala verso il boma"), due=h.includes("centra la barra e cazza");   // 0.20.3: dopo aver centrato fa quello che legge
   const vuole=uno?(S.boomSide<0?"ArrowLeft":"ArrowRight"):(due||b)?"ArrowUp":null;
   if(vuole!==premuto){ if(premuto) T.tasto("keyup",premuto); if(vuole!=="ArrowLeft"&&vuole!=="ArrowRight"){ T.tasto("keydown"," "); T.tasto("keyup"," "); } if(vuole) T.tasto("keydown",vuole); premuto=vuole; } }
  if(t1!==null&&!b&&tVia===null) tVia=t;
  if(tVia!==null||(tA!==null&&tB===null&&t-tA>2)||(t1!==null&&t-t1>2)) break; }
 T.su(); return {fase_prima,a8,tAu:T.r2(tAu),tA:T.r2(tA),tB:T.r2(tB),t1:T.r2(t1),tVia:T.r2(tVia),nonmis}; }"""
# 3i) tempo massimo della fase 3: arretra (0,2 s), poi tenuta a +0,3 nodi con la prua a 40° (rimesse a ogni passo)
TMAX = """([twa,sh])=>{ const T=__T, sv=__sv; T.prova(1,"free",twa,-0.3,sh); const S=sv.S, h0=S.h;
 sv.run(1/60,12); S.u=0.3/1.944; let visto=false, tVia=null;
 for(let n=1;n<=780;n++){ sv.run(1/60,1); S.u=0.3/1.944; S.h=h0; S.r=0; const t=n/60; if(n%6) continue;
  sv.panel(); const b=T.hint().includes("barra al centro, cazza"); if(b) visto=true; if(visto&&!b&&tVia===null){ tVia=t; break; } }
 return {visto,tVia:T.r2(tVia)}; }"""
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
    "raffica (1.0.9, il più lungo dei tre)": "Raffica in arrivo: sfruttala per accelerare. Se sbandi troppo, poggia e lasca un poco.",
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
        print(f"versione {'lunga, semi 1-20' if LUNGO else 'veloce, semi 1-2'}; pagina {HTML.name}")
        # la prova 2 ha vento costante: nessuna raffica che copra il suggerimento
        await pg.evaluate("__sv.startMission(1, 0)"); await pg.wait_for_timeout(300)

        sbagliati = []; nonvalido = []
        # 0) senza #collaudo l'aggancio non deve esistere
        pg2 = await b.new_page(); await pg2.goto(BASE); await pg2.wait_for_timeout(300)
        sv_fuori = await pg2.evaluate("typeof window.__sv"); await pg2.close()
        print(f"senza #collaudo: typeof window.__sv = {sv_fuori}")
        if sv_fuori != "undefined": sbagliati.append(f"senza #collaudo window.__sv esiste ({sv_fuori})")
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
        # 3b) sbandamento oltre 25 gradi (1.0.9, docs/PROPOSTA-RAFFICHE-PORTANTI.md): di bolina (sotto 75°) lascare o orzare,
        # dal traverso in giù lascare e poggiare; con la scotta tutta lascata solo orzare (bolina) o poggiare. Tre fasce, due mure.
        SBT = {(True, 1.0): "Sbandi troppo e la vela è già tutta lasca: prova a orzare un poco.", (True, 0.6): "Sbandi troppo: lasca la scotta, oppure orza di poco.",
               (False, 1.0): "Sbandi troppo e la vela è già tutta lasca: poggia un poco.", (False, 0.6): "Sbandi troppo: lasca la scotta e poggia un poco."}
        n_sb = 0
        for sh in (1.0, 0.6):
            for twa in (60, 100, 150):
                for lato in (1, -1):   # prova ripartita a ogni caso: girando da una mura all'altra la barca strambava e scuffiava
                    await pg.evaluate("__sv.startMission(1, 0)"); await pg.wait_for_timeout(150)
                    await pg.evaluate("([twa,sh])=>{const S=__sv.S; S.h=(__sv.twd+twa+360)%360; __sv.ctl.sheet=sh; S.heel=40;}", [lato * twa, sh])
                    await pg.wait_for_timeout(120)
                    letto = await pg.evaluate("__sv.S.heel > 25 ? document.getElementById('hint').textContent : null")
                    if letto is None: continue
                    n_sb += 1
                    if letto != SBT[(twa < 75, sh)]: sbagliati.append(f"sbandamento, scotta {sh} a twa {lato * twa}: «{letto}»")
        if n_sb != 12: sbagliati.append(f"sbandamento: misurati {n_sb} casi su 12")
        # 3b2) raffica in arrivo (1.0.9): barca 22 m sottovento a una raffica vera della prova 5, piccola (non copre la barca) e forte (oltre +20%)
        await pg.evaluate("__sv.startMission(4, 0)"); await pg.wait_for_timeout(300)
        RAF = {"bolina": "Raffica in arrivo: sfruttala per accelerare. Se sbandi troppo, lasca o orza un poco.",
               "traverso e lasco": "Raffica in arrivo: sfruttala per accelerare. Se sbandi troppo, poggia e lasca un poco.",
               "gran lasco e poppa": "Raffica in arrivo: sfruttala per accelerare. Se poggi troppo rischi la strambata."}
        n_raf = 0
        for fascia, twa in (("bolina", 60), ("traverso e lasco", 100), ("gran lasco e poppa", 150)):
            for lato in (1, -1):
                letto = await pg.evaluate("""([twa]) => { const sv = __sv, S = sv.S;
                  const G = sv.gusts().filter(g => g[3] > 0.25 && g[2] * 1.4 < 21).sort((a, b) => b[3] - a[3]); if (!G.length) return null;
                  const g = G[0], to = (sv.twd + 180) * Math.PI / 180;
                  S.x = g[0] + Math.sin(to) * 22; S.y = g[1] - Math.cos(to) * 22; S.h = (sv.twd + twa + 360) % 360;
                  S.heel = 0; S.heelRate = 0; S.u = 2; S.indietro = 0; sv.ctl.sheet = 0.5; sv.panel();
                  return document.getElementById('hint').textContent; }""", [lato * twa])
                if letto is None: continue
                n_raf += 1
                if letto != RAF[fascia]: sbagliati.append(f"raffica in arrivo, {fascia} a twa {lato * twa}: «{letto}»")
        if n_raf != 6: sbagliati.append(f"raffica in arrivo: misurati {n_raf} casi su 6")
        # 3c) barca che arretra, gioco libero con le raffiche: il pilota segue il suggerimento. Criteri (0.20.3, scritti prima dei risultati):
        # K1 un testo «all'indietro» entro 0,5 s simulati dal primo istante all'indietro; K2 partenza da 40° in su: solo il secondo testo,
        # sotto 40°: prima il primo e poi il secondo; K3 nessun ritorno al primo testo con la prua da 37° in su; K4 uscita con la regola
        # del 5.4 (prua >= 40°, barca avanti, tenuta 1 s) entro 30 s; K5 1 nodo entro 30 s, e B non più visibile oltre 0,5 s da lì;
        # K6 la prua non va mai oltre 10° dall'altra parte del vento locale (misura il suggerimento con un pilota perfetto: l'uscita
        # sull'altra mura resta valida nel 5.4).
        await pg.evaluate(ATTREZZI)
        K = {k: 0 for k in ("K1", "K2", "K3", "K4", "K5", "K6")}
        n_ind = 0; tempi = []; n_alti = n_bassi = 0; ris3c = {}
        def k3c(nome, twa, r):
            sb = []
            if r["tInd"] is None or r["tTesto"] is None or r["tTesto"] - r["tInd"] > 0.5 + 1e-9: sb.append("K1")
            if (twa >= 40 and (r["visto1"] or not r["visto2"])) or (twa < 40 and not (r["primo"] == 1 and r["visto2"])): sb.append("K2")
            if r["alti"]: sb.append("K3")
            if r["tEsce"] is None or r["tEsce"] > 30: sb.append("K4")
            if r["t1"] is None or r["t1"] > 30 or r["bTardi"]: sb.append("K5")
            if r["latoMin"] <= -10: sb.append("K6")
            for k in sb: K[k] += 1
            if sb: sbagliati.append(f"all'indietro {nome}: {' '.join(sb)} {r}")
        for nome, twa, kn in ARRETRA:
            for mure, segno in (("dritta", 1), ("sinistra", -1)):
                for sh in (1.0, 0.5):
                    for seme in SEMI:
                        r = await pg.evaluate(SEGUI, [seme, "free", segno * twa, kn, sh, CONTRARIO]); n_ind += 1
                        ris3c[(nome, mure, sh, seme)] = r
                        k3c(f"{nome} mure a {mure} scotta {sh} seme {seme}", twa, r)
                        n_alti += r["alti"]; n_bassi += r["bassi"]
                        if r["tEsce"] is not None: tempi.append(r["tEsce"])
        # K0) ripetibilità: 4 prove rifatte in ordine inverso devono dare risultati identici, campo per campo
        n_rip = 0
        for chiave in list(ris3c)[:4][::-1]:
            nome, mure, sh, seme = chiave; twa, kn = next((t, k) for n, t, k in ARRETRA if n == nome)
            r = await pg.evaluate(SEGUI, [seme, "free", (1 if mure == "dritta" else -1) * twa, kn, sh, CONTRARIO]); n_rip += 1
            if r != ris3c[chiave]: sbagliati.append(f"K0 prova non ripetibile {chiave}: {ris3c[chiave]} contro {r}")
        print(f"3c gioco libero: {n_ind} prove; errori per criterio {K}; ripetibilità rifatte {n_rip}; "
              f"scuffie durante il riscaldamento (barca raddrizzata prima della prova) {sum(r['capRisc'] for r in ris3c.values())}")
        # il seme deve contare: per ogni caso e scotta (mure a dritta), quanti tempi di uscita diversi danno i semi
        gruppi = {}
        for (nome, mure, sh, seme), r in ris3c.items():
            if mure == "dritta": gruppi.setdefault((nome, sh), set()).add(r["tEsce"])
        vari = sum(len(v) >= 2 for v in gruppi.values())
        print(f"3c gruppi (caso, scotta, mure a dritta) con almeno 2 tempi di uscita diversi fra i semi: {vari} su {len(gruppi)}")
        if LUNGO and vari < 5: nonvalido.append(f"3c: solo {vari} gruppi su {len(gruppi)} cambiano con il seme (attesi almeno 5)")
        print(f"3c uscita (regola del 5.4) in {min(tempi, default=0):.2f}-{max(tempi, default=0):.2f} s simulati ({len(tempi)} uscite)")
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
        # 3e) lezione 5 passo 4 (suggerimenti spenti, niente raffiche, seme 1): K1, K3, K6 come nella 3c, e il passo completato
        # davvero (stepDone, la regola del gioco) entro 30 s simulati. Cambio di criterio della 0.20.3, deciso DOPO aver visto 2 prove
        # su 20 fallire: «passo completato» conta solo se la fase 1 del passo scatta (barca piantata per 1 s, index.html:647);
        # le altre sono «non misurate». Attese non misurate: solo caso 5, scotta 50, due mure (fase 1 a 0,87 s contro 1 s).
        n_l5 = n_l5_ok = 0; K5e = {k: 0 for k in ("K1", "K3", "K6", "passo", "fase 1 incoerente")}; l5_nonmis = []
        for nome, twa, kn in ARRETRA:
            for mure, segno in (("dritta", 1), ("sinistra", -1)):
                for sh in (1.0, 0.5):
                    r = await pg.evaluate(SEGUI, [1, "l54", segno * twa, kn, sh, CONTRARIO]); n_l5 += 1
                    sb = []
                    if r["tInd"] is None or r["tTesto"] is None or r["tTesto"] - r["tInd"] > 0.5 + 1e-9: sb.append("K1")
                    if r["alti"]: sb.append("K3")
                    if r["latoMin"] <= -10: sb.append("K6")
                    if r["tDone"] is not None and not r["fase1"]: sb.append("fase 1 incoerente")   # il gioco completa, il ricalcolo dice di no
                    if not r["fase1"]: l5_nonmis.append((nome, mure, sh))
                    elif r["tDone"] is None or r["tDone"] > 30: sb.append("passo")
                    for k in sb: K5e[k] += 1
                    n_alti += r["alti"]; n_bassi += r["bassi"]
                    if sb: sbagliati.append(f"lezione 5 passo 4, {nome} mure a {mure} scotta {sh}: {' '.join(sb)} {r}")
                    else: n_l5_ok += 1
        print(f"lezione 5 passo 4: {n_l5_ok} riuscite su {n_l5}, di cui «passo completato» misurato in {n_l5 - len(l5_nonmis)}; "
              f"non misurate (fase 1 mai scattata) {len(l5_nonmis)}: {l5_nonmis}; errori per criterio {K5e}")
        if sorted(l5_nonmis) != sorted([("caso 5", "dritta", 0.5), ("caso 5", "sinistra", 0.5)]):
            nonvalido.append(f"3e: non misurate diverse da quelle attese (caso 5, scotta 50, due mure): {l5_nonmis}")
        # 3f) barca che arretra già fuori dall'angolo morto (46-55°, soglia 40°): il primo testo «all'indietro» letto deve essere il secondo
        n_sopra = 0
        for luogo, dove in (("navigazione libera", "free"), ("lezione 5 passo 4", "l54")):
            for twa in (46, 50, 55, -46, -50, -55):
                letto = await pg.evaluate(PRIMO, [dove, twa]); n_sopra += 1
                if letto != INDIETRO2: sbagliati.append(f"3f {luogo}, arretra a {twa} gradi: primo testo «{letto}», atteso il secondo")
        print(f"3f barca che arretra già fuori dall'angolo morto: {n_sopra} casi")
        # 3g) caso 6: B entro 0,5 s simulati, il pilota centra e cazza, 1 nodo entro 30 s, poi B sparisce. Caso 7: B mai, per 5 s.
        n_c6 = n_c6_ok = n_c7 = n_c7_tot = c7_nonmis = 0; righe7 = []
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                for seme in SEMI:
                    twa6 = 41 + seme % 4
                    r = await pg.evaluate(CASO6, [seme, segno * twa6, sh]); n_c6 += 1
                    nome6 = f"caso 6 {twa6}° mure a {mure} scotta {sh} seme {seme}"
                    if r["fase_prima"] != 2: sbagliati.append(f"{nome6}: la barca non risultava all'indietro prima {r}")
                    elif r["tB"] is None or r["tB"] > 0.5 + 1e-9: sbagliati.append(f"{nome6}: B non comparso entro 0,5 s {r}")
                    elif r["t1"] is None or r["t1"] > 30: sbagliati.append(f"{nome6}: non supera 1 nodo entro 30 s {r}")
                    elif r["tVia"] is None: sbagliati.append(f"{nome6}: B non sparisce sopra 1 nodo {r}")
                    else: n_c6_ok += 1
                    r = await pg.evaluate(CASO7, [seme, sh]); n_c7_tot += 1
                    esito7 = "non misurata (ha arretrato)" if r["arretrata"] or r["fase0"] else ("SBAGLIATA: B senza aver arretrato" if r["b"] else "giusta: B mai")
                    righe7.append(f"   caso 7 mure a {mure} scotta {sh} seme {seme}: {esito7} {r}")
                    if r["arretrata"] or r["fase0"]: c7_nonmis += 1; continue
                    n_c7 += 1
                    if r["b"]: sbagliati.append(f"caso 7 mure a {mure} scotta {sh} seme {seme}: testo B senza aver arretrato")
        print(f"caso 6 (avanti piano dopo aver arretrato): {n_c6_ok} riusciti su {n_c6}; caso 7 (controllo): {n_c7} prove misurate, "
              f"{c7_nonmis} non misurate (la barca ha arretrato nei 5 s), {n_c7_tot} in tutto")
        print("caso 7, tutte le prove (tArr: primo istante all'indietro; umin_kn: velocità minima; kn_fine e twa_fine: stato a 5 s, fine della prova):")
        for x in righe7: print(x)
        # 3h) caso 8: B entro 0,5 s da tA, 1 nodo entro 30 s, B sparisce entro 0,5 s da lì. Non misurata (contata a parte) se la barca
        # supera 1 nodo prima che la prua arrivi a 37°, o se la prua ci arriva dopo più di 10 s. Valido solo se le misurate sono tutte.
        n_c8 = n_c8_ok = 0; c8_nonmis = []; righe8 = []; n_c8_prev = 4 * len(SEMI)
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                for seme in SEMI:
                    twa8 = 30 + seme % 7
                    r = await pg.evaluate(CASO8, [seme, segno * twa8, sh])
                    nome8 = f"caso 8 {twa8}° mure a {mure} scotta {sh} seme {seme}"
                    righe8.append(f"   {nome8}: tAu {r['tAu']} tA {r['tA']} tB {r['tB']} tB-tA {None if r['tB'] is None or r['tA'] is None else round(r['tB'] - r['tA'], 2)} t1 {r['t1']} tVia {r['tVia']} {r['nonmis'] or ''}")
                    if r["fase_prima"] != 1: c8_nonmis.append(f"{nome8}: la barca non risultava all'indietro sotto 40° {r}"); continue
                    if r["nonmis"]: c8_nonmis.append(f"{nome8}: {r['nonmis']} {r}"); continue
                    n_c8 += 1
                    if r["tB"] is None or r["tB"] - r["tA"] > 0.5 + 1e-9: sbagliati.append(f"{nome8}: B non comparso entro 0,5 s {r}")
                    elif r["t1"] is None or r["t1"] > 30: sbagliati.append(f"{nome8}: non supera 1 nodo entro 30 s {r}")
                    elif r["tVia"] is None or r["tVia"] - r["t1"] > 0.5 + 1e-9: sbagliati.append(f"{nome8}: B non sparisce entro 0,5 s sopra 1 nodo {r}")
                    else: n_c8_ok += 1
        print(f"caso 8 (smette di arretrare sotto 37°, poi la prua sale): {n_c8_ok} riusciti su {n_c8} misurati; non misurati {len(c8_nonmis)}")
        for x in c8_nonmis: print("   non misurato:", x)
        print("caso 8, tutte le prove (tAu: primo istante con S.u > 0,05 dopo l'inversione; tA: primo istante avanti con prua >= 37° e sotto 1 nodo):")
        for x in righe8: print(x)
        if n_c8 < n_c8_prev: nonvalido.append(f"caso 8 con {n_c8} prove misurate su {n_c8_prev}")
        # 3i) tempo massimo della fase 3: B deve sparire fra 10 e 10,5 s simulati dalla fine dell'arretramento. 4 prove: 2 mure x 2 scotte.
        n_tmax = 0
        for mure, segno in (("dritta", 1), ("sinistra", -1)):
            for sh in (1.0, 0.5):
                r = await pg.evaluate(TMAX, [segno * 40, sh]); n_tmax += 1
                if not r["visto"] or r["tVia"] is None or not (10 <= r["tVia"] <= 10.5): sbagliati.append(f"tempo massimo mure a {mure} scotta {sh}: atteso B sparito fra 10 e 10,5 s {r}")
                print(f"tempo massimo mure a {mure} scotta {sh}: {r}")
        print(f"ritorni dal secondo al primo testo: con la prua da 37° in su {n_alti}, sotto 37° {n_bassi}")
        # conteggi attesi: ogni gruppo deve aver misurato tutte le prove previste, non solo più di zero
        for nome, n, atteso in (("3c", n_ind, 20 * len(SEMI)), ("ripetibilità", n_rip, 4), ("3e", n_l5, 20), ("3f", n_sopra, 12),
                                ("caso 6", n_c6, 4 * len(SEMI)), ("caso 7, misurate + non misurate", n_c7_tot, 4 * len(SEMI)), ("3i", n_tmax, 4)):
            if n != atteso: nonvalido.append(f"{nome} con {n} prove misurate su {atteso}")
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

        # Un controllo che non misura niente passa sempre: qui i casi vanno dichiarati e devono essere quelli previsti.
        print(f"finestra {W}x{H}")
        print(f"casi misurati: scotta 1,00 con «lee» {n_lee}, scotta 1,00 con altri filetti {n_altro}, "
              f"scotta 0,90-0,99 {n_quasi} (di cui in stallo {n_quasi_lee}), suggerimento semplice {n_sail}, sbandamento {n_sb}, raffica in arrivo {n_raf}, pannello {n_pan}")
        print("eccesso massimo del pannello (pixel):", peggio)
        print("casi sbagliati:", sbagliati or "nessuno")
        print("errori pagina:", errs[:5])
        vuoto = [n for n in (n_lee, n_altro, n_quasi, n_quasi_lee, n_sail, n_sb, n_raf, n_passi, n_pan) if n == 0]
        if vuoto: print("COLLAUDO NON VALIDO: una delle misure non ha nessun caso")
        for x in nonvalido: print("COLLAUDO NON VALIDO:", x)
        if not caratteri_ok: print("COLLAUDO NON VALIDO: caratteri del gioco non caricati, i margini del pannello misurati sopra non sono attendibili")
        await b.close()
        # 1: qualcosa non va nel gioco o nel collaudo; 3 (dal 13 ottobre 2026): tutto il resto è a posto ma mancano i caratteri del gioco,
        # quindi solo le misure del pannello non valgono (succede nella sandbox): lancia_tutti.sh lo mostra come «NON VALIDO (ambiente)»
        sys.exit(1 if (sbagliati or errs or vuoto or nonvalido) else (3 if not caratteri_ok else 0))
asyncio.run(main())
