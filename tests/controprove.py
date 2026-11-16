# Controprove dei collaudi («test dei test», docs/PROPOSTA-TEST-DEI-TEST.md, 1 novembre 2026).
# Per ogni riga della tabella CONTROPROVE: copia del gioco (index.html, js/, fonts/) e dei collaudi (tests/, senza output) in
# tests/output/controprove/<ora>/<id>/ (dentro il repository, così i collaudi che leggono versioni vecchie con git funzionano),
# una sostituzione nel codice del gioco della copia (sorgente.copia: il pezzo deve comparire una volta sola), poi il collaudo
# lanciato dalla copia. Il gioco vero non si tocca mai.
#   mutante: un difetto messo apposta; il collaudo DEVE cadere (codice d'uscita diverso da 0) e, se la riga lo dice, deve
#            cadere il controllo indicato (una riga d'uscita con «FALLITO»/«NO»/«ERRORE» che contiene quel testo).
#   neutra:  una modifica che non cambia il comportamento (un commento); il collaudo DEVE restare OK.
# Le sostituzioni sono state scritte prima di lanciarle, partendo da cosa dice la regola o la proposta (non dal collaudo);
# una controprova che non dà l'esito atteso non si toglie: si riporta.
# Uso: .venv-collaudi/bin/python tests/controprove.py                 tutte, una alla volta
#      .venv-collaudi/bin/python tests/controprove.py --parallelo 3   fino a 3 insieme
#      .venv-collaudi/bin/python tests/controprove.py --solo giri     solo le righe il cui id contiene «giri»
#      .venv-collaudi/bin/python tests/controprove.py --elenco        stampa la tabella senza lanciare niente
#      --tieni lascia le copie (di norma si cancellano, salvo quelle con un esito diverso dall'atteso)
# Esce con 1 se una controprova non dà l'esito atteso.
import concurrent.futures, datetime, os, pathlib, shutil, subprocess, sys, time
import sorgente

QUI = pathlib.Path(__file__).resolve().parent
ROOT = QUI.parent
PY = str(ROOT / ".venv-collaudi" / "bin" / "python")

NEUTRA_JS = ("  // ---- chi cede (1.0.40", "  // controprova neutra: questo commento non cambia niente\n  // ---- chi cede (1.0.40")
NEUTRA_MOTORE = ("const BOAT = {", "// controprova neutra: questo commento non cambia niente\nconst BOAT = {")
NEUTRA_HTML = ('<aside class="panel">', '<!-- controprova neutra -->\n  <aside class="panel">')

# 16 novembre 2026: i difetti M1-M12 di docs/PER-FABLE.md (codice delle 1.3.x)
M1 = ("o.fin < b.fin).length + b.pp * pen));", "o.fin < b.fin).length + 0 * b.pp * pen));")
M2 = ("sc = p.length >= TOR_N ? p.indexOf(Math.max(...p)) : -1;", "sc = -1;")
M3 = ("if (g.cum < GIRO_GRADI || S.tacks <= g.tk || S.gybesC + S.gybesV <= g.gy) return;", "if (g.cum < GIRO_GRADI || S.tacks <= g.tk) return;")
M4 = ("if (tA !== tB) return { cede: tA < 0 ? A : B, regola: 10 };", "if (tA !== tB) return { cede: tA < 0 ? B : A, regola: 10 };")
M5 = ("merito = !!p.zonalePulita && totale >= QUOTA_MERITO;", "merito = totale >= QUOTA_MERITO;")
M6 = ("spOfferteDa(tutti ? [c.g, Math.min(4, c.g + 1)]", "spOfferteDa(tutti ? [c.g, c.g]")
M7 = ("w = { t0: a.s, t1: b.s, m: b.d - a.d };", "w = { t0: a.s + 10, t1: b.s + 10, m: b.d - a.d };")
M8 = ("/* 1.3.3: il coach solo con la rotta ottimale */ releaseKeys(); finShow();", "/* 1.3.3: il coach solo con la rotta ottimale */ releaseKeys();")
M9 = ("!LESSONS[li].nascosta && !LESSONS[li].livello && bancaEsame(li).length);", "!LESSONS[li].nascosta && !LESSONS[li].livello && li !== 3 && bancaEsame(li).length);")
M10 = ('      <div class="feedback pending" id="lFeedback"></div>', '      <div class="feedback pending" id="lFeedback" style="margin-bottom:30px"></div>')
M11 = ('cl.filter(x => x.id !== "*").slice(0, 5).map(x => x.id); }', 'cl.filter(x => x.id !== "*").slice(1, 6).map(x => x.id); }')
M12 = ("hullScale: 1, ", "hullScale: 1.05, ")

# id, tipo, comando (relativo a tests/), sostituzioni, testo del controllo che deve cadere (o None), cosa rappresenta
CONTROPROVE = [
    ("polare-mut", "mutante", ["fisica/confronta.js", "polare.js"], [("sailArea: 7.0,", "sailArea: 7.7,")], None,
     "area della vela della 1a +10%"),
    ("polare-neu", "neutra", ["fisica/confronta.js", "polare.js"], [NEUTRA_MOTORE], None, "commento nel motore"),
    ("raffiche-mut", "mutante", ["fisica/confronta.js", "raffiche_e_virate.js"], [("mass: 135,", "mass: 148.5,")], None,
     "massa della barca +10%"),
    ("raffiche-neu", "neutra", ["fisica/confronta.js", "raffiche_e_virate.js"], [NEUTRA_MOTORE], None, "commento nel motore"),
    ("impronta1b-mut", "mutante", ["fisica/impronta1b.js"], [("hullKq: 400,", "hullKq: 401,")], None,
     "barca dell'1b: acqua contro lo scafo che ruota 400 → 401 (la stessa di --cambia)"),
    ("impronta1b-neu", "neutra", ["fisica/impronta1b.js"], [NEUTRA_MOTORE], None, "commento nel motore"),
    ("regole-mut11", "mutante", ["collaudo_regole.py"], [("return { cede: lat * tA > 0 ? B : A, regola: 11 };", "return { cede: lat * tA > 0 ? A : B, regola: 11 };")], None,
     "regola 11 rovesciata: cede la barca sottovento invece della sopravento"),
    ("regole-mut13", "mutante", ["collaudo_regole.py"], [("if (A.virando !== B.virando) return { cede: A.virando ? A : B, regola: 13 };", "if (false) return { cede: A.virando ? A : B, regola: 13 };")], None,
     "regola 13 spenta: chi vira non cede più"),
    ("regole-neu", "neutra", ["collaudo_regole.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("giri-mut", "mutante", ["collaudo_giri.py", "12"], [("G.done = G.giroDir && v !== G.giroDir ? G.base + 1 : G.done + 1;", "G.done = G.need;")], "B1",
     "un giro solo estingue tutto il debito (la 44.2 ne vuole due)"),
    ("giri-neu", "neutra", ["collaudo_giri.py", "12"], [NEUTRA_JS], None, "commento in regate.js"),
    ("boa-mut", "mutante", ["collaudo_boa.py", "12"], [("R.boaTocc[key] = R.t; R.nBoa = (R.nBoa || 0) + 1; giriDebito(1);", "R.boaTocc[key] = R.t; R.nBoa = (R.nBoa || 0) + 1; giriDebito(0);")], None,
     "toccare una boa non dà il giro di penalità (regola 31)"),
    ("boa-neu", "neutra", ["collaudo_boa.py", "12"], [NEUTRA_JS], None, "commento in regate.js"),
    ("regola21-mut", "mutante", ["collaudo_regola21.py", "12"], [("if ((sa !== 0) !== (sb !== 0)) return { cede: sa ? A : B, regola: sa || sb };", "if (false) return { cede: sa ? A : B, regola: sa || sb };")], None,
     "regole 21.1 e 21.2 spente: chi sconta o torna dietro la linea non cede"),
    ("regola21-neu", "neutra", ["collaudo_regola21.py", "12"], [NEUTRA_JS], None, "commento in regate.js"),
    ("giriavv-mut", "mutante", ["collaudo_giri_avversari.py", "120"], [("if (!(b.gDebt > 0) || b.fin !== null || b.dnf || (R.t >= 0 && b.leg < 1) || b.ocs){ if (b.gCum != null)", "if (true || !(b.gDebt > 0) || b.fin !== null || b.dnf || (R.t >= 0 && b.leg < 1) || b.ocs){ if (b.gCum != null)")], None,
     "gli avversari non fanno mai i giri (120 regate, come nel giro)"),
    # 16 novembre 2026 (DA-FARE voce 46, dopo la correzione del G3): provata a mano prima di entrare qui, Chromium, 120 regate: 24 coppie di giri su 24 in versi opposti, G3 cade
    ("giriavv-verso", "mutante", ["collaudo_giri_avversari.py", "120"], [("b.gFatti = (b.gFatti || 0) + 1; b.gCum = 0; b.gTk = 0; b.gGy = 0;", "b.gFatti = (b.gFatti || 0) + 1; b.gCum = 0; b.gTk = 0; b.gGy = 0; b.gV = -b.gV;")], "G3",
     "dopo ogni giro fatto l'avversario cambia verso (44.2: i giri di una penalità nello stesso verso)"),
    ("giriavv-neu", "neutra", ["collaudo_giri_avversari.py", "120"], [NEUTRA_JS], None, "commento in regate.js (120 regate, come nel giro)"),
    # aggiunta dopo il primo lancio (1 novembre 2026, dichiarata in PROPOSTA-TEST-DEI-TEST.md §9): con 12 regate G4 vede 7 casi e ne vuole 15,
    # quindi la neutra a 12 regate cade per il minimo di casi, non per un difetto. 16 novembre 2026: anche 40 non bastano più (dalla 1.3.10 meno contatti con colpa dei rivali); le due righe giriavv usano le 120 regate del giro
    # ("giriavv-neu40", "neutra", ["collaudo_giri_avversari.py", "40"], [NEUTRA_JS], None, "commento in regate.js (40 regate, come nel giro)"),   # 16 novembre 2026: tolta, con 40 regate i casi non bastano più (dal giro si lancia con 120: riga giriavv-neu)
    ("segnali-mut", "mutante", ["collaudo_segnali.py"], [("b.X = R.t >= 0 && R.t < X_MAX && !!R.xSet && R.xSet.some(o => o.ocs && o.fin === null && !o.dnf);", "b.X = R.t >= 0 && R.t < X_MAX && !!R.xSet;")], None,
     "la X resta su anche quando le barche richiamate sono tornate (29.1)"),
    ("segnali-neu", "neutra", ["collaudo_segnali.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("contatto-mut", "mutante", ["collaudo_contatto_vero.py"], [("if (d > 4.4) continue; const mtv = hullOverlap(A.S, B.S); if (!mtv) continue;", "if (d > 4.4) continue; const mtv = hullOverlap(A.S, B.S) || { nx: 0, ny: 1, pen: 0 };")], None,
     "nell'1b il contatto scatta a 4,4 m fra i centri anche senza scafi che si toccano"),
    ("contatto-neu", "neutra", ["collaudo_contatto_vero.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("semaforo-mut", "mutante", ["collaudo_semaforo.py"], [('return c.cede !== me ? "verde" : (c.base || c).cede === me ? "rosso" : "giallo"; }', 'return c.cede !== me ? "rosso" : (c.base || c).cede === me ? "verde" : "giallo"; }')], None,
     "semaforo con i colori scambiati"),
    ("semaforo-neu", "neutra", ["collaudo_semaforo.py"], [NEUTRA_JS], None, "commento in regate.js"),
    # aggiunte dopo il primo lancio (1 novembre 2026), per i collaudi appena diventati chiari; scritte prima di lanciarle
    ("lezioni-mut", "mutante", ["collaudo_lezioni.py"], [("cond: I => I.twa < 40 && I.kn < 1.5, hold: 0.5,", "cond: I => I.twa < 5 && I.kn < 1.5, hold: 0.5,")], "orzare fino all'angolo morto",
     "passo 1.8 che chiede la prua a 5° dal vento invece di 40°"),
    ("lezioni-neu", "neutra", ["collaudo_lezioni.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("giroboa-mut", "mutante", ["collaudo_giro_boa.py"], [('if (k < 0){ S.wrongMarks = (S.wrongMarks || 0) + 1; regAdd("wrongMarks"); }', 'if (false){ S.wrongMarks = (S.wrongMarks || 0) + 1; regAdd("wrongMarks"); }')], "giri sbagliati",
     "la boa girata dal lato sbagliato non viene più contata come errore"),
    ("giroboa-neu", "neutra", ["collaudo_giro_boa.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("strambata-mut", "mutante", ["collaudo_strambata.py", "15", "10"], [("if (S.heel > BOAT.capsizeAt || S.heel < -45){", "if (S.heel > BOAT.capsizeAt + 30 || S.heel < -75){")], None,
     "la barca scuffia 30° più tardi (15 nodi: deve scuffiare sempre)"),
    ("strambata-neu", "neutra", ["collaudo_strambata.py", "15", "10"], [NEUTRA_JS], None, "commento in regate.js"),
    ("pannello-mut", "mutante", ["collaudo_pannello.py", "1360", "650"], [('    <section class="card" id="lesson" hidden>', '    <p style="margin:0;height:40px">controprova: una riga in più</p>\n    <section class="card" id="lesson" hidden>')], None,
     "40 px in più in cima al pannello"),
    ("pannello-neu", "neutra", ["collaudo_pannello.py", "1360", "650"], [NEUTRA_HTML], None, "commento nella pagina"),
    # 16 novembre 2026 (docs/PER-FABLE.md §1, docs/MUTAZIONI.md): i 12 difetti M1-M12 sul codice delle 1.3.x; sostituzioni scritte prima di lanciarle.
    # Stesso difetto, più collaudi: una riga per collaudo. Le neutre (f16n-) dicono se il collaudo è verde sul gioco vero.
    ("f16-m1-torneo", "mutante", ["collaudo_torneo.py"], [M1], None, "M1 torPunti: la penalità sul punteggio non si somma"),
    # ("f16-m1-pentesto", "mutante", ["collaudo_penalita_testo.py"], [M1], None, "M1 torPunti: la penalità sul punteggio non si somma"),   # 16 novembre 2026: tolta, questo collaudo non può vedere questo difetto (docs/MUTAZIONI.md, note 1-3)
    ("f16-m2-torneo", "mutante", ["collaudo_torneo.py"], [M2], None, "M2 torSerie: lo scarto non si toglie"),
    ("f16-m3-giri", "mutante", ["collaudo_giri.py"], [M3], None, "M3 giriPenalita: un giro vale anche senza strambata"),
    # ("f16-m3-provagiri", "mutante", ["collaudo_prova_giri.py"], [M3], None, "M3 giriPenalita: un giro vale anche senza strambata"),   # 16 novembre 2026: tolta, questo collaudo non può vedere questo difetto (docs/MUTAZIONI.md, note 1-3)
    ("f16-m4-regole", "mutante", ["collaudo_regole.py"], [M4], None, "M4 chiCede: regola 10 rovesciata (cede chi ha mure a dritta)"),
    ("f16-m4-senzacolpa", "mutante", ["collaudo_contatto_senza_colpa.py"], [M4], None, "M4 chiCede: regola 10 rovesciata"),
    # ("f16-m4-registro", "mutante", ["collaudo_registro.py"], [M4], None, "M4 chiCede: regola 10 rovesciata"),   # 16 novembre 2026: tolta, questo collaudo non può vedere questo difetto (docs/MUTAZIONI.md, note 1-3)
    ("f16-m5-superata", "mutante", ["collaudo_deriva_superata.py"], [M5], None, "M5 meritiD: il merito non chiede la stagione senza ritiri"),
    ("f16-m6-sponsor", "mutante", ["collaudo_sponsor.py"], [M6], None, "M6 spFineStagione: con tutti gli obiettivi non arriva il gradino sopra"),
    ("f16-m7-coach", "mutante", ["collaudo_coach.py"], [M7], None, "M7 coaClou: finestra del clou 10 s più tardi"),
    ("f16-m8-moviola", "mutante", ["collaudo_moviola.py"], [M8], None, "M8 rivChiudi: niente ritorno alla schermata di fine regata"),
    ("f16-m9-esame", "mutante", ["collaudo_esame.py"], [M9], None, "M9 lezioniEsame: la lezione 4 (indice 3) esce dall'esame"),
    ("f16-m9-derlez", "mutante", ["collaudo_deriva_lezioni.py"], [M9], None, "M9 lezioniEsame: la lezione 4 (indice 3) esce dall'esame"),
    ("f16-m10-panlez", "mutante", ["collaudo_pannello_lezioni.py"], [M10], None, "M10 pagina: 30 px di margine in più nel pannello delle lezioni"),
    ("f16-m11-finale", "mutante", ["collaudo_finale.py"], [M11], None, "M11 finale: rivali dal 2° al 6° invece che dal 1° al 5°"),
    ("f16-m12-polare", "mutante", ["fisica/confronta.js", "polare.js"], [M12], None, "M12 motore: resistenza dello scafo +5%"),
    ("f16-m12-impronta", "mutante", ["fisica/impronta1b.js"], [M12], None, "M12 motore: resistenza dello scafo +5%"),
    ("f16n-torneo", "neutra", ["collaudo_torneo.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-pentesto", "neutra", ["collaudo_penalita_testo.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-giri", "neutra", ["collaudo_giri.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-provagiri", "neutra", ["collaudo_prova_giri.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-senzacolpa", "neutra", ["collaudo_contatto_senza_colpa.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-registro", "neutra", ["collaudo_registro.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-superata", "neutra", ["collaudo_deriva_superata.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-sponsor", "neutra", ["collaudo_sponsor.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-coach", "neutra", ["collaudo_coach.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-moviola", "neutra", ["collaudo_moviola.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-esame", "neutra", ["collaudo_esame.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-derlez", "neutra", ["collaudo_deriva_lezioni.py"], [NEUTRA_JS], None, "commento in regate.js"),
    ("f16n-panlez", "neutra", ["collaudo_pannello_lezioni.py"], [NEUTRA_HTML], None, "commento nella pagina"),
    ("f16n-finale", "neutra", ["collaudo_finale.py"], [NEUTRA_JS], None, "commento in regate.js"),
]

SEGNI = ("FALLITO", "NO ", "ERRORE", "NON VALIDO")

def prepara(cartella, sost):
    sorgente.copia(cartella, sost)
    shutil.copytree(QUI, cartella / "tests", ignore=shutil.ignore_patterns("output", "__pycache__"))

def lancia(riga, base, tieni):
    cid, tipo, cmd, sost, cade, cosa = riga
    cartella = base / cid; t0 = time.time()
    try: prepara(cartella, sost)
    except Exception as e: return (riga, None, 0, "copia non riuscita: %s" % e, False)
    script = cartella / "tests" / cmd[0]
    if cmd[0].endswith(".js"): args, cwd = ["node", str(script)] + cmd[1:], script.parent
    else: args, cwd = [PY, str(script)] + cmd[1:], cartella
    try: p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=3600); codice, uscita = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired: codice, uscita = None, "oltre un'ora"
    (base / (cid + ".txt")).write_text(uscita, encoding="utf-8")
    righe_cadute = [l for l in uscita.splitlines() if any(s in l for s in SEGNI)]
    if tipo == "neutra": giusto = codice == 0
    else: giusto = codice not in (0, None) and (cade is None or any(cade in l for l in righe_cadute))
    if giusto and not tieni: shutil.rmtree(cartella, ignore_errors=True)
    return (riga, codice, time.time() - t0, righe_cadute[:3], giusto)

def main():
    a = sys.argv[1:]
    solo = a[a.index("--solo") + 1] if "--solo" in a else ""
    par = int(a[a.index("--parallelo") + 1]) if "--parallelo" in a else 1
    righe = [r for r in CONTROPROVE if solo in r[0]]
    if "--elenco" in a:
        for r in righe: print("%-16s %-8s %-40s %s" % (r[0], r[1], " ".join(r[2]), r[5]))
        return 0
    base = QUI / "output" / "controprove" / (datetime.datetime.now().strftime("%Y%m%d-%H%M%S-") + str(os.getpid())); base.mkdir(parents=True)
    print("controprove: %d, uscite in %s" % (len(righe), base), flush=True)
    esiti = []
    with concurrent.futures.ThreadPoolExecutor(par) as ex:
        for e in ex.map(lambda r: lancia(r, base, "--tieni" in a), righe):
            r, codice, dt, cadute, giusto = e; esiti.append(e)
            print("%s %-16s %-8s uscita %s, %.0f s — %s%s" % ("OK      " if giusto else "SBAGLIATA", r[0], r[1], codice, dt, r[5],
                  "" if r[1] == "neutra" or not cadute else " | caduto: " + str(cadute[0])[:120]), flush=True)
    mut = [e for e in esiti if e[0][1] == "mutante"]; neu = [e for e in esiti if e[0][1] == "neutra"]
    print("RIEPILOGO: mutanti presi %d su %d; neutre rimaste OK %d su %d" % (sum(e[4] for e in mut), len(mut), sum(e[4] for e in neu), len(neu)))
    sbagliate = [e[0][0] for e in esiti if not e[4]]
    if sbagliate: print("da guardare (copie lasciate in %s): %s" % (base, ", ".join(sbagliate)))
    return 1 if sbagliate or not esiti else 0

if __name__ == "__main__":
    sys.exit(main())
