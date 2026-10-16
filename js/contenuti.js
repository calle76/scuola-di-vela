// Scuola di vela, contenuti.js — Contenuti: lezioni, prove, ripassi, esame, glossario.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // CONTENUTI
  // Nelle lezioni il vento arriva da nord. Condizioni: I = lettura istantanea (vedi readI).
  // ======================================================================
  const PAUSE = { pause: true };
  // ---- lezioni ----
  // Lezione 1 (0.16): orzare e poggiare con le frecce del timone. Il testo dice quale freccia premere,
  // secondo il lato da cui arriva il vento in quel momento e secondo l'impostazione delle frecce (barra o prua).
  const windLeft = () => norm180(local.twd - S.h) < 0;
  const poggiaSide = () => windLeft() ? "destra" : "sinistra", orzaSide = () => windLeft() ? "sinistra" : "destra";
  const turnKey = side => (opt.helm === "prua") === (side === "destra") ? "→" : "←";
  const barraNote = side => opt.helm === "prua" ? "" : ` La freccia sposta la barra a ${side === "destra" ? "sinistra" : "dritta"}: perché la prua giri dall'altra parte lo vedrai nella lezione 2.`;
  const L1 = [
    { title: "La barca", ...PAUSE, zoom: 3, labels: ["prua", "poppa"],
      text: ["Questa è una <em>deriva</em>: una piccola barca a vela per una persona, la barca su cui di solito si impara. La vedi dall'alto.",
             "La punta si chiama <em>prua</em>, la parte posteriore <em>poppa</em>."] },
    { title: "Dritta e sinistra", ...PAUSE, zoom: 3, labels: ["prua", "dritta", "sinistra"],
      text: ["Immagina di stare a bordo guardando verso prua: il lato alla tua destra si chiama <em>dritta</em>, quello alla tua sinistra <em>sinistra</em>.",
             "Dritta e sinistra appartengono alla barca, non allo schermo: se la barca gira, girano con lei."] },
    { title: "Albero, boma, randa", ...PAUSE, zoom: 3, labels: ["albero", "boma", "randa"],
      text: ["Il pallino scuro verso prua è la base dell'<em>albero</em>, il palo verticale che regge la vela.",
             "Dall'albero parte il <em>boma</em>, l'asta orizzontale che tiene il lato basso della vela. La vela si chiama <em>randa</em>, e si regola con una cima, la <em>scotta</em>."] },
    { title: "Timone e deriva", ...PAUSE, zoom: 3, labels: ["timone", "barra", "deriva"],
      text: ["A poppa c'è il <em>timone</em>, una pala immersa in acqua che fa girare la barca. Il timoniere lo comanda con la <em>barra</em>, il manico che tiene in mano.",
             "Al centro dello scafo scende sott'acqua la <em>deriva</em>, una lama che impedisce alla barca di essere spinta di lato dal vento. Senza, la barca scivolerebbe via di fianco. Da questa lama prendono il nome le barche come questa."] },
    { title: "Il vento", ...PAUSE, zoom: 1.2, arrows: true,
      text: ["Le increspature sul mare e la freccia <em>bianca</em> mostrano il vento. In alto a sinistra c'è scritto da dove arriva; in alto a destra c'è la bussola.",
             "In vela si dice sempre <em>da dove arriva</em> il vento, non dove va: questo è un «vento da nord»."] },
    { title: "Sopravento e sottovento", ...PAUSE, zoom: 2.4, labels: ["sopravento", "sottovento", "boma"],
      text: ["Il lato della barca colpito per primo dal vento si chiama <em>sopravento</em>; quello opposto, riparato, <em>sottovento</em>.",
             "Nota dove sta il boma: sottovento. Il vento spinge la vela, che si piazza sempre dalla parte opposta a quella da cui arriva il vento. Il timoniere invece siede sopravento, per fare contrappeso."] },
    { title: "Poggiare", tiller: true, turnHint: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: [() => `Ora guidi tu, con le frecce ← →. Tieni premuto <em>${turnKey(poggiaSide())}</em>: la prua gira a ${poggiaSide()}, lontano dal vento. Si dice <em>poggiare</em>.` + barraNote(poggiaSide()),
             "Rilascia quando il vento arriva quasi da dietro. Non andare oltre: il boma cambierebbe lato di colpo (è una <em>strambata</em>, lezione 5). La vela si regola da sola."],
      cond: I => I.twa >= 135,
      done: "Hai poggiato: ora il vento arriva da dietro, e il boma si è aperto verso l'esterno per ricevere il vento." },
    { title: "Orzare e l'angolo morto", allow: ["irons"], tiller: true, turnHint: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: [() => `Ora tieni premuto <em>${turnKey(orzaSide())}</em>: la prua gira a ${orzaSide()}, verso il vento. Si dice <em>orzare</em>. Continua finché la barca non si ferma quasi del tutto, poi rilascia.`],
      cond: I => I.twa < 40 && I.kn < 1.5, hold: 0.5,
      done: "Questo è l'<em>angolo morto</em>: con la prua troppo vicina al vento (nelle scuole si indica in circa 45° per lato) la vela sbatte come una bandiera e non spinge, e la barca si ferma. Nessuna barca a vela può andare dritta contro il vento." },
    { title: "Ripartire", tiller: true, turnHint: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: [() => `Tieni premuto <em>${turnKey(poggiaSide())}</em> per poggiare e uscire dall'angolo morto, finché il vento arriva di fianco e la barca riparte. Se giri troppo, correggi con l'altra freccia. Con la prua proprio nel vento va bene anche l'altra freccia: da entrambi i lati si poggia.`],
      cond: I => I.twa > 70 && I.twa < 105 && I.kn > 2.5, hold: 1, // al traverso: più poggiati la vela non sbatterebbe nel passo «lascare»
      done: "La barca è ripartita. Ricapitolando: <em>orzare</em> avvicina la prua al vento, <em>poggiare</em> la allontana. Si riferiscono al vento, non a destra o sinistra: con il vento dall'altro lato della barca, per poggiare gireresti dall'altra parte." },
    { title: "La scotta: lascare", sem: ["lasca"], tiller: true, turnHint: true, hud: 1, hintKind: "sail",
      text: ["<em>Lascare</em> significa mollare la scotta: la vela si apre verso l'esterno. <em>Cazzare</em> significa tirarla: la vela si avvicina al centro della barca.",
             "Da qui la vela non si regola più da sola. Tieni premuto <em>Lasca</em> (tasto S) e apri la vela del tutto."],
      cond: I => I.sheet > 0.9 && (I.tt === "wind" || I.tt === "flog"), hold: 0.5,
      done: "Vedi come sbatte? Si dice che la vela <em>fileggia</em>: troppo aperta, prende il vento di taglio e non spinge. La barca rallenta." },
    { title: "La scotta: cazzare", sem: ["cazza", "lasca"], tiller: true, turnHint: true, hud: 1, hintKind: "sail",
      text: ["Ora tieni premuto <em>Cazza</em> (tasto W), poco alla volta, finché la vela smette di sbattere e si gonfia. Se esageri, correggi con Lasca."],
      cond: I => I.tt === "ok", hold: 1,
      done: "Vela regolata: la barca riprende velocità. La regola pratica: <em>lasca finché la vela comincia a sbattere, poi cazza quanto basta perché smetta</em>." },
    { title: "Troppo cazzata", sem: ["cazza", "lasca"], tiller: true, turnHint: true, hud: 1, hintKind: "sail",
      text: ["E se si cazza troppo? Tieni premuto <em>Cazza</em> fino a chiudere del tutto la vela, e guarda la velocità."],
      cond: I => I.sheet < 0.03 && I.tt === "lee", hold: 1,
      done: "La vela non sbatte, ma la barca rallenta: troppo chiusa, il vento non ci scorre sopra bene. Si dice che la vela è <em>in stallo</em>. Lasca per ripartire." },
    { title: "Navigazione libera", sem: ["cazza", "lasca"], tiller: true, turnHint: true, hud: 1, hintKind: "sail", final: true,
      text: ["Hai le basi: <em>prua</em> e <em>poppa</em>, <em>dritta</em> e <em>sinistra</em>, <em>timone</em> e <em>deriva</em>, <em>sopravento</em> e <em>sottovento</em>, <em>orzare</em> e <em>poggiare</em>, <em>cazzare</em> e <em>lascare</em>.",
             "Naviga liberamente per prendere confidenza. Nella prossima lezione vedrai come funziona la barra e perché la prua gira dalla parte opposta."] }
  ];

  const L2 = [
    { title: "Come si timona", ...PAUSE, zoom: 3, labels: ["barra", "timone"],
      text: ["In una deriva non c'è un volante: il timoniere sposta la <em>barra</em>. La barra ruota la pala del timone dalla parte opposta, e l'acqua che scorre sulla pala spinge la poppa.",
             "Il risultato va imparato bene perché è controintuitivo: <em>la prua gira dalla parte opposta a quella verso cui sposti la barra</em>."] },
    { title: "Barra a sinistra", tiller: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: ["Sposta la barra verso sinistra con la freccia <em>←</em> (o con il cursore «Barra del timone») e guarda da che parte gira la prua."],
      cond: I => I.tiller < -0.3 && I.r > 6, hold: 0.4,
      done: "Barra a sinistra, prua verso dritta." },
    { title: "Barra a dritta", tiller: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: ["Ora sposta la barra verso dritta con la freccia <em>→</em>."],
      cond: I => I.tiller > 0.3 && I.r < -6, hold: 0.4,
      done: "Barra a dritta, prua verso sinistra. Quando rilasci, la barra torna al centro da sola (si può cambiare nelle impostazioni); con <em>Spazio</em> la centri subito." },
    { title: "Barra sottovento: si orza", tiller: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: ["La regola che usano i velisti: <em>barra sottovento, la barca orza</em>; <em>barra sopravento, la barca poggia</em>. Il lato sottovento è quello dove sta il boma.",
             "Sposta la barra verso il boma e orza fino alla <em>bolina</em>, <em>a piccoli colpi</em> e non con un colpo lungo: fermati quando la lancetta della rosetta (in basso) è a metà strada tra il rosso e l'orizzontale. Poi centra la barra."],
      cond: I => I.twa >= 43 && I.twa <= 67 && Math.abs(I.r) < 4, hold: 1,
      done: "Esatto: barra verso il boma, cioè sottovento, e la prua è salita verso il vento." },
    { title: "Barra sopravento: si poggia", tiller: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: ["Ora sposta la barra dalla parte opposta al boma e poggia fino al <em>lasco</em>, <em>a piccoli colpi</em>: fermati quando la lancetta è scesa un terzo della strada tra l'orizzontale e il basso. Poi centra la barra."],
      cond: I => I.twa >= 110 && I.twa <= 145 && Math.abs(I.r) < 4, hold: 1,
      done: "Barra sopravento, la barca poggia." },
    { title: "Tenere la rotta", tiller: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: ["In certe condizioni, la barca tende a salire da sola verso il vento: si dice che è <em>orziera</em>. Consulta il glossario per avere più informazioni. Tieni la rotta indicata nel riquadro sopra i comandi, correggendo con <em>piccoli colpi</em> di barra: resta entro 6° per 8 secondi di fila.",
             "Timonare bene vuol dire usare poca barra: ogni angolo di barra frena la barca."],
      course: true, yawNoise: true,
      cond: (I, S) => Math.abs(norm180(S.h - S.course)) < 6 && I.kn > 2, hold: 8,
      done: "Rotta tenuta. Piccole correzioni, fatte presto, sono meglio di grandi correzioni fatte tardi." },
    { title: "Navigazione libera", tiller: true, sheet: true, hud: 1, hintKind: "sail", final: true,
      text: ["Ora hai la barra e la scotta: la barra con le frecce ← → o il cursore, la scotta con le frecce ↑ (cazza) e ↓ (lasca) o il cursore.",
             "Esercitati a orzare e poggiare con la barra, regolando la vela ogni volta. Nella prossima lezione vedrai le andature e i filetti, che ti diranno esattamente come regolare la vela."] }
  ];

  const L3 = [
    { title: "Le andature", ...PAUSE, zoom: 1.2, rose: true,
      text: ["Ogni direzione rispetto al vento ha un nome: si chiama <em>andatura</em>. Il cerchio attorno alla barca le mostra tutte; l'angolo morto è dalla parte da cui arriva il vento, e le andature si ripetono uguali sui due lati.",
             "La linea tratteggiata indica dove punta la prua: ora sei al <em>traverso</em>, con il vento di fianco."] },
    { title: "Bolina", tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "sail", target: [1, 2],
      text: ["Orza fino alla <em>bolina</em> (il settore con il bordo tratteggiato nel cerchio), con il vento tra circa 45° e 75° dalla prua. La vela si regola da sola: guarda come si chiude il boma."],
      cond: I => I.twa >= 43 && I.twa <= 72 && Math.abs(I.r) < 4, hold: 1,
      done: "Bolina: l'andatura più vicina al vento. <em>Bolina stretta</em> è il massimo che la barca riesce a stringere, <em>bolina larga</em> un po' più aperta. La vela sta molto cazzata." },
    { title: "Traverso", tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "sail", target: [3],
      text: ["Poggia fino al <em>traverso</em> (il settore con il bordo tratteggiato), con il vento a circa 90°."],
      cond: I => I.twa >= 80 && I.twa <= 100 && Math.abs(I.r) < 4, hold: 1,
      done: "Al traverso il vento arriva di fianco. È un'andatura veloce, e la vela va aperta circa a metà: il boma a una quarantina di gradi dal centro barca, a metà strada tra tutto cazzato e tutto lascato. Il valore esatto lo leggi sotto il cursore della scotta." },
    { title: "Lasco e gran lasco", tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "sail", target: [5],
      text: ["Continua a poggiare attraverso il <em>lasco</em> (circa 120°) fino al <em>gran lasco</em> (circa 150°, il settore con il bordo tratteggiato)."],
      cond: I => I.twa >= 138 && I.twa <= 163 && Math.abs(I.r) < 4, hold: 1,
      done: "Nel lasco il vento arriva da dietro il fianco; nel gran lasco quasi da dietro, e la vela è molto aperta." },
    { title: "Poppa", tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "sail", target: [6],
      text: ["Poggia ancora, piano, finché il vento arriva esattamente da dietro: la <em>poppa</em> (il settore con il bordo tratteggiato).", "Attenzione a non superare i 180°. Il vento passerebbe dall'altro lato della vela e il boma attraverserebbe la barca di colpo: è una <em>strambata</em>, e con la vela tutta aperta spesso fa scuffiare. Come farla in sicurezza lo vedrai nella lezione 5."],
      cond: I => I.twa >= 167, hold: 1,
      done: "In poppa la vela è aperta al massimo e il vento la spinge da dietro. Sembra strano, ma non è l'andatura più veloce: il traverso e il lasco lo sono di più." },
    { title: "Le mure", ...PAUSE, zoom: 2, rose: true, labels: ["sopravento", "boma"],
      text: ["Se il vento arriva sul lato sinistro della barca si naviga <em>mure a sinistra</em>; se arriva sul lato destro, <em>mure a dritta</em>. Il boma sta sempre dal lato opposto alle mure.",
             "Questa barca ha il vento da sinistra: è mure a sinistra. Le mure contano anche per le precedenze: quando due barche a vela si incrociano con mure diverse, quella mure a sinistra deve lasciare strada."] },
    { title: "I filetti", ...PAUSE, zoom: 3.2, labels: ["filetti"],
      text: ["Sulla randa ci sono due nastrini, i <em>filetti</em>: rosso sul lato sinistro della vela, verde sul lato destro. Mostrano come scorre l'aria.",
             "Entrambi dritti verso il boma: vela regolata. Si agita quello <em>sopravento</em>: vela troppo lascata, cazza. Si agita quello <em>sottovento</em>: vela troppo cazzata, lasca."] },
    { title: "Filetto sopravento", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Da qui la vela la regoli tu. Lasca la scotta (freccia ↓) finché il filetto <em>sopravento</em> comincia ad agitarsi. Il suggerimento è spento: guarda i filetti."],
      cond: I => I.tt === "wind", hold: 1,
      done: "Il filetto sopravento si agita: la vela è troppo lascata e l'aria la prende di taglio." },
    { title: "Filetti dritti", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Ora cazza (freccia ↑) poco alla volta, finché entrambi i filetti scorrono dritti."],
      cond: I => I.tt === "ok", hold: 1.5,
      done: "Vela regolata." },
    { title: "Filetto sottovento", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Cazza ancora, troppo, finché si agita il filetto <em>sottovento</em>."],
      cond: I => I.tt === "lee", hold: 1,
      done: "Vela troppo cazzata: l'aria si stacca dal lato sottovento, la vela va in stallo e la barca rallenta." },
    { title: "Poggi e laschi", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "none",
      text: ["Poggia fino al <em>lasco</em> e regola la vela finché i filetti sono dritti."],
      cond: I => I.twa >= 105 && I.twa <= 140 && I.tt === "ok", hold: 1.5,
      done: "Poggiando la vela era troppo chiusa: hai dovuto lascare." },
    { title: "Orzi e cazzi", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "none",
      text: ["Ora orza fino alla <em>bolina</em> e regola di nuovo."],
      cond: I => I.twa >= 43 && I.twa <= 72 && I.tt === "ok", hold: 1.5,
      done: "Orzando la vela era troppo aperta: hai dovuto cazzare. Regola da ricordare: <em>orzi e cazzi, poggi e laschi</em>." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 2, rose: true, hintKind: "tt", final: true,
      text: ["Le andature, dalla più vicina alla più lontana dal vento: <em>bolina</em>, <em>traverso</em>, <em>lasco</em>, <em>gran lasco</em>, <em>poppa</em>. Ognuna vuole la sua regolazione, e i <em>filetti</em> te la indicano. Ora passa alle prove: il vento non arriverà più sempre da nord."] }
  ];

  const L4 = [
    { title: "Il vento che senti a bordo", ...PAUSE, zoom: 1.4, arrows: true, hud: 2,
      text: ["Quando vai in bicicletta senti vento in faccia anche in una giornata calma: è il vento creato dal tuo movimento. In barca succede lo stesso.",
             "Il vento che senti a bordo, e su cui lavora la vela, è il <em>vento apparente</em>: la somma del <em>vento reale</em> e del vento dovuto al moto della barca. Freccia bianca: reale. Freccia gialla, e segnavento in cima all'albero: apparente."] },
    { title: "Da fermi", sheet: true, hud: 2, arrows: true, hintKind: "none",
      text: ["Lasca tutta la vela (freccia ↓) e aspetta che la barca rallenti sotto i 2 nodi. Guarda le due frecce e i numeri nel pannello."],
      cond: I => I.kn < 2, hold: 1.5,
      done: "Con la barca quasi ferma, vento apparente e vento reale quasi coincidono: direzione e forza simili. Da ferma sarebbero identici." },
    { title: "Accelerando", sheet: true, hud: 2, arrows: true, hintKind: "tt",
      text: ["Ora cazza finché la vela è regolata e lascia accelerare la barca oltre i 4 nodi. Guarda la freccia gialla."],
      cond: I => I.kn > 4 && I.tt === "ok", hold: 1,
      done: "Il vento reale arriva a 90°, ma quello apparente è più avanti, tra 60° e 70° (lo leggi nel pannello), ed è più forte. Per questo, quando la barca accelera, <em>bisogna cazzare</em>: la vela deve seguire il vento apparente." },
    { title: "In poppa", tiller: true, sheet: true, hud: 2, arrows: true, hintKind: "tt",
      text: ["Poggia fino alla <em>poppa</em>, regolando la vela, e guarda di nuovo le frecce e i numeri."],
      cond: I => I.twa >= 165, hold: 1.5,
      done: "In poppa la barca «scappa» dal vento: il vento apparente è più debole del reale. Di bolina succede il contrario, e il vento apparente è più forte. Per questo di bolina sembra sempre che tiri più vento." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 2, arrows: true, hintKind: "tt", final: true,
      text: ["La vela lavora sul <em>vento apparente</em>. Più la barca va veloce, più il vento apparente si sposta verso prua. Andando controvento è più forte del reale, andando col vento a favore è più debole.",
             "Naviga liberamente osservando le due frecce a diverse andature."] }
  ];

  const L5 = [
    { title: "Cambiare mure", ...PAUSE, zoom: 1.2, rose: true, maneuvers: true,
      text: ["Per passare da mure a sinistra a mure a dritta, o viceversa, ci sono due manovre.",
             "La <em>virata</em>: la prua attraversa il vento, cioè l'angolo morto. La <em>strambata</em> (detta anche abbattuta): è la poppa ad attraversare il vento. Si vira per risalire il vento, si stramba navigando col vento da dietro."] },
    { title: "Prepararsi a virare", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "tt",
      text: ["Mettiti in <em>bolina</em>, regola la vela e lascia che la barca arrivi ad almeno 3,3 nodi."],
      cond: I => I.twa >= 43 && I.twa <= 72 && I.tt === "ok" && I.kn >= 3.3, hold: 1,
      done: "Pronto. Durante la virata la prua attraversa l'angolo morto, dove la vela non spinge: la barca lo supera grazie all'<em>abbrivio</em>, la velocità che ha già." },
    { title: "Virare", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "tt",
      text: ["Sposta la barra <em>sottovento</em> (verso il boma) con decisione e tienila finché la prua ha attraversato il vento e sei in bolina sull'altro lato. Poi centra la barra.",
             "In bolina la vela resta cazzata su entrambe le mure: non serve toccarla."],
      cond: (I, S, B) => S.tacks > B.tacks && I.twa >= 40 && I.twa <= 78 && I.kn > 1.2, hold: 0.8,
      done: "Virata riuscita: il boma è passato dall'altra parte e il timoniere ha cambiato lato. A bordo si annuncia così: «Pronti a virare?», «Pronti!», «Viro!»." },
    { title: "Una virata che non riesce", allow: ["irons"], tiller: true, sheet: true, hud: 1, rose: true, hintKind: "none",
      text: ["Ora senza abbrivio: lasca la vela finché la barca scende sotto 1 nodo, poi prova a virare. Se non rallenti abbastanza, orza fino alla bolina, con la vela lasca.",
             "Se la barca si pianta nel vento, <em>arretra</em>. Per uscirne sposta la barra <em>verso il boma</em>: la prua si allontana dal vento. Fuori dall'angolo morto centra la barra e cazza: la barca riparte."],
      // 0.20.2, due fasi. Fase 1: barca piantata (la condizione della 0.20.1, tenuta 1 s). Fase 2: uscita, prua ad almeno IRONS_A (40°) dal vento
      // e barca che va avanti, tenuta 1 s (hold); vale su tutte e due le mure. Lo stato delle fasi sta in B, che showStep rifà a ogni passo.
      cond: (I, S, B) => {
        if (!B.piantata){
          if ((I.twa < 40 && I.kn < 0.4) || S.u < -0.1){ if (B.t1 === undefined) B.t1 = simTime; if (simTime - B.t1 >= 1) B.piantata = true; } else B.t1 = undefined;
          return false;
        }
        return I.twa >= IRONS_A && S.u > 0.05;
      }, hold: 1,
      done: "La barca si è piantata nel vento: senza velocità il timone non fa effetto, e quando la barca arretra la barra funziona al contrario. Per questo <em>si vira sempre con la barca lanciata</em>." },
    { title: "Risalire il vento", tiller: true, sheet: true, hud: 1, hintKind: "tt", mark: [0, -110],
      text: ["Riparti. L'arrivo è controvento: non puoi puntarlo direttamente.",
             "Raggiungilo a zig-zag: un tratto di bolina su una mura, una virata, un tratto sull'altra. Si chiama <em>bordeggiare</em>, e ogni tratto è un <em>bordo</em>."],
      cond: (I, S, B) => S.markReached && S.tacks > B.tacks,
      done: "Arrivo tagliato. La scia mostra quanto è più lunga la strada rispetto alla distanza in linea d'aria: risalire il vento costa tempo." },
    { title: "La strambata", ...PAUSE, zoom: 1.2, rose: true, maneuvers: true,
      text: ["La strambata è più delicata. In poppa la vela è tutta aperta: quando il vento passa dall'altro lato, il boma attraversa la barca di colpo. Se lo fa con violenza può far scuffiare la barca o colpire qualcuno in testa.",
             "Per questo la si fa <em>controllata</em>: si cazza la vela finché il boma è a circa 45° dal centro barca, si poggia finché il vento passa dall'altro lato, poi subito si lasca."] },
    { title: "Strambata violenta", allow: ["gybesV", "capsizes"], tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "none",
      text: ["Prima vediamo cosa <em>non</em> fare. Poggia fino alla poppa e continua a poggiare con la vela tutta aperta (si regola da sola) finché il vento passa dall'altro lato."],
      cond: (I, S, B) => S.gybesV > B.gybesV, hold: 0.6,
      done: "Il boma ha attraversato la barca di colpo, la barca ha sbandato e rallentato: <em>strambata violenta</em>. Se capita senza volerlo, navigando in poppa distratti, si chiama <em>strambata involontaria</em>." },
    { title: "Strambata controllata", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "none",
      text: ["Ora fai bene: in poppa <em>cazza</em> finché il boma è a 45° o meno (guarda il valore sotto il cursore della scotta), <em>poggia</em> finché il vento passa dall'altro lato, poi <em>lasca</em> e regola: i filetti tornano dritti quando orzi fino al lasco."],
      cond: (I, S, B) => S.gybesC > B.gybesC && I.twa > 115 && I.tt === "ok", hold: 1,
      done: "Strambata controllata: il boma ha fatto un tragitto breve e la barca non si è scomposta. Il comando a bordo: «Pronti a strambare?», «Pronti!», «Strambo!»." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 2, rose: true, hintKind: "tt", final: true,
      text: ["<em>Virata</em>: prua nel vento, con la barca lanciata. <em>Strambata</em>: poppa nel vento, cazzando prima e lascando dopo. Per risalire il vento si <em>bordeggia</em>.",
             "Esercitati, poi passa alle prove 3 e 4."] }
  ];

  const L6 = [
    { title: "Raffiche e sbandamento", ...PAUSE, zoom: 0.8, env: { tws: 12, gusts: 1 }, hud: 3,
      text: ["Il vento non è mai costante. Le chiazze più scure e increspate sull'acqua sono <em>raffiche</em>: lì il vento è più forte e spesso gira di qualche grado. Viaggiano col vento, quindi le vedi arrivare da sopravento.",
             "Più vento vuol dire più forza sulla vela, e la barca si inclina: è lo <em>sbandamento</em>, che vedi sull'indicatore in basso a sinistra. Il timoniere si sporge fuori bordo per contrastarlo, ma con un attimo di ritardo."] },
    { title: "Assorbire una raffica", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt",
      text: ["Naviga di bolina con la vela regolata e aspetta una raffica. Quando ci entri, <em>lasca</em> un poco (e di bolina puoi anche <em>orzare</em> leggermente) per tenere lo sbandamento sotto i 20°. Passata la raffica, cazza di nuovo."],
      cond: I => I.inGust && I.heel < 20 && I.kn > 2, hold: 3,
      done: "Ben fatto. Lascare riduce la forza sulla vela; orzare di poco la scarica. È la tecnica principale per navigare con vento rafficato." },
    { title: "La scuffia", allow: ["capsizes"], noRight: true, tiller: true, sheet: true, hud: 3, env: { tws: 15, gusts: 2 }, hintKind: "none", bigGust: true,
      text: ["Ora il vento è più forte e le raffiche più violente. Per capire il limite, fai apposta l'errore: vela tutta cazzata, e in raffica non lascare."],
      cond: (I, S, B) => S.capsizes > B.capsizes, hold: 0.8,
      done: "Oltre circa 60° di sbandamento la barca si è rovesciata: ha <em>scuffiato</em>. Per una deriva capita, non è un dramma: si raddrizza." },
    { title: "Raddrizzare", startCapsized: true, tiller: true, sheet: true, hud: 3, env: { tws: 15, gusts: 2 }, hintKind: "tt",
      text: ["Premi <em>Raddrizza</em> (o il tasto R). Nella realtà prima si lasciano libere le scotte, poi il timoniere sale sulla lama della deriva e fa leva con il proprio peso finché la barca torna dritta, e risale a bordo."],
      cond: (I, S, B) => B.cap0 && !S.capsized, hold: 1, // B.cap0: la barca era rovesciata all'inizio del passo (showStep la rovescia se serve)
      done: "Barca dritta. Regola la vela con i filetti e riparti." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", final: true,
      text: ["Guarda le raffiche arrivare, <em>lasca</em> quando entri, <em>cazza</em> quando escono. Oltre circa 60° di sbandamento si <em>scuffia</em>.",
             "Esercitati, poi prova il percorso nelle raffiche."] }
  ];

  const LESSONS = [
    { name: "Lezione 1", title: "La barca e il vento", steps: L1, desc: "Le parti della barca, il vento, orzare e poggiare, cazzare e lascare." },
    { name: "Lezione 2", title: "Il timone", steps: L2, desc: "La barra si sposta dalla parte opposta: barra sottovento orza, sopravento poggia." },
    { name: "Lezione 3", title: "Andature e filetti", steps: L3, desc: "Bolina, traverso, lasco, poppa; le mure; regolare la vela leggendo i filetti." },
    { name: "Lezione 4", title: "Vento reale e apparente", steps: L4, desc: "Perché andando veloci il vento sembra arrivare più da prua." },
    { name: "Lezione 5", title: "Virata e strambata", steps: L5, desc: "Cambiare mure, risalire il vento a zig-zag, strambare senza rischi." },
    { name: "Lezione 6", title: "Raffiche e scuffia", steps: L6, desc: "Riconoscere le raffiche, tenere la barca piatta, scuffiare e raddrizzare." }
  ];

  // ---- prove ----
  // Prove: geometria descritta con il vento da nord (m), poi ruotata secondo il vento della prova.
  // bands: tempi massimi in secondi per oro, argento e bronzo (0.16), tarati con tests/collaudo_fasce.py:
  // oro = tempo del pilota automatico arrotondato ai 5 s superiori, argento +25%, bronzo +60%.
  // Dalla 0.19 l'ultima voce di marks è una linea d'arrivo (FIN_HALF m per lato, perpendicolare all'ultimo lato), non una boa da raggiungere.
  const MISSIONS = [
    { title: "Al traverso", desc: "Taglia l'arrivo con il vento di fianco.", wind: 270, tws: 10, gusts: 0,
      text: "Il vento non arriva più da nord: guarda la freccia. L'arrivo è al traverso. La vela parte troppo cazzata: regolala sui filetti e passa tra le due boe dell'arrivo.",
      start: { x: 0, y: 0, h: 90, sheet: 0.02 }, bands: [95, 120, 150],
      marks: [{ x: 230, y: 0, label: "Arrivo" }] },
    { title: "Lasco e poppa", desc: "Raggiungi l'arrivo sottovento.", wind: 45, tws: 10, gusts: 0,
      text: "L'arrivo è sottovento: poggia passando da traverso a lasco e poppa, lascando man mano. Attento a non strambare senza volerlo. Se devi per forza strambare, cazza prima tutta la vela, così la strambata è controllata (la vedrai meglio nella lezione 5).",
      start: { x: 0, y: 0, h: 90, sheet: 0.3 }, bands: [145, 180, 230],
      marks: [{ x: 60, y: 260, label: "Arrivo" }] },
    { title: "Risalire il vento", desc: "Raggiungi l'arrivo controvento.", wind: 180, tws: 10, gusts: 0,
      text: "L'arrivo è esattamente controvento. Bordeggia: bolina su una mura, virata con la barca lanciata, bolina sull'altra.",
      start: { x: 0, y: 0, h: 90, sheet: 0.2 }, bands: [200, 250, 320],
      marks: [{ x: 0, y: -220, label: "Arrivo" }] },
    { title: "Il giro di boa", desc: "Bolina all'andata, poppa al ritorno.", wind: 135, tws: 10, gusts: 0,
      text: "Risali di bolina fino alla boa e girala lasciandola a sinistra, poi torna a tagliare la linea da cui sei partito, con il vento da dietro. Se devi strambare, cazza prima e lasca dopo.",
      start: { x: 0, y: 20, h: 90, sheet: 0.2 }, bands: [335, 420, 535],
      marks: [{ x: 0, y: -200, label: "Boa" }, { x: 0, y: 20, label: "Arrivo" }] },
    { title: "Percorso nelle raffiche", desc: "Un triangolo con vento rafficato.", wind: 225, tws: 12, gusts: 1,
      text: "Tre lati: bolina fino alla boa 1, traverso fino alla boa 2, poi gran lasco fino alla linea d'arrivo. Le boe si lasciano a sinistra. Il vento è rafficato: guarda le chiazze, lasca quando entri, cazza quando escono.",
      start: { x: 0, y: 20, h: 90, sheet: 0.2 }, bands: [355, 440, 565],
      marks: [{ x: 0, y: -200, label: "Boa 1" }, { x: -150, y: -200, label: "Boa 2" }, { x: 0, y: 20, label: "Arrivo" }] }
  ];

  const SEQ = [["l",0],["l",1],["l",2],["m",0],["m",1],["l",3],["l",4],["m",2],["m",3],["l",5],["m",4]];


  // ---- ripasso ed esame ----
  // Quiz di ripasso: [domanda, risposta giusta, [sbagliate], spiegazione]
  const QUIZ = [
    [ ["Guardando verso prua, come si chiama il lato destro della barca?", "Dritta", ["Sinistra", "Poppa", "Sottovento"], "Dritta e sinistra si riferiscono sempre alla barca guardando verso prua, non allo schermo né al vento."],
      ["A cosa serve la deriva, la lama sotto lo scafo?", "Impedisce alla barca di essere spinta di lato dal vento", ["Fa girare la barca", "Regge la vela", "Frena la barca quando serve"], "Senza deriva la barca scivolerebbe via di fianco. A girarla è il timone."],
      ["«Vento da nord» significa che il vento…", "arriva da nord", ["va verso nord", "soffia parallelo alla costa nord", "cambia direzione verso nord"], "In vela si indica sempre la direzione da cui il vento arriva."],
      ["Orzare significa…", "girare la prua verso il vento", ["girare la prua lontano dal vento", "tirare la scotta", "girare a sinistra"], "Orzare e poggiare si riferiscono al vento, non a destra o sinistra."],
      ["Da che parte sta il boma?", "Sottovento, dalla parte opposta a quella da cui arriva il vento", ["Sopravento", "Sempre a dritta", "Sempre al centro della barca"], "Il vento spinge la vela e il boma dalla parte opposta; il timoniere siede sopravento per fare contrappeso."],
      ["La vela sbatte perché è troppo lascata. Come si dice?", "Fileggia", ["È in stallo", "Scuffia", "È a segno"], "Troppo lascata la vela fileggia; troppo cazzata va in stallo."] ],
    [ ["Sposta la barra verso sinistra. Dove va la prua?", "Verso dritta", ["Verso sinistra", "Dritta avanti, la barca rallenta", "Dipende dal vento"], "La barra muove la pala del timone dalla parte opposta: la prua gira dalla parte opposta a dove sposti la barra."],
      ["Barra sottovento, cioè verso il boma: cosa fa la barca?", "Orza", ["Poggia", "Si ferma", "Stramba"], "La regola: barra sottovento orza, barra sopravento poggia."],
      ["Perché conviene timonare usando poca barra?", "Perché ogni angolo di barra frena la barca", ["Perché la barra si può rompere", "Perché la barca scarroccia di più", "Non conviene: più barra si usa, meglio è"], "La pala angolata oppone resistenza all'acqua: piccole correzioni fatte presto sono meglio di grandi correzioni tardive."],
      ["La barca si è fermata nel vento e comincia ad andare all'indietro. Cosa succede alla barra?", "Funziona al contrario", ["Non ha più nessun effetto", "Funziona come prima", "Si blocca al centro"], "Con l'acqua che scorre sulla pala da dietro, l'effetto del timone si inverte."] ],
    [ ["Qual è l'andatura più vicina al vento?", "Bolina", ["Traverso", "Lasco", "Poppa"], "Bolina stretta è il massimo che la barca riesce a stringere; più vicino si entra nell'angolo morto."],
      ["Il vento arriva perpendicolare alla barca, a 90°. In che andatura sei?", "Traverso", ["Bolina larga", "Gran lasco", "Poppa"], "Al traverso il vento è di fianco: andatura veloce, con la vela aperta circa a metà (boma a una quarantina di gradi dal centro barca)."],
      ["Si agita il filetto sopravento. Cosa fai?", "Cazzo la vela, oppure poggio", ["Lasco la vela, oppure orzo", "Non faccio nulla: è normale", "Centro la barra"], "Filetto sopravento agitato: vela troppo lascata, o prua troppo vicina al vento."],
      ["Orzando, come va regolata la vela?", "Va cazzata", ["Va lascata", "Non va toccata", "Va lasciata sbattere"], "Orzi e cazzi, poggi e laschi."],
      ["Il vento arriva sul lato sinistro della barca. Come si naviga?", "Mure a sinistra", ["Mure a dritta", "Al traverso", "Sottovento"], "Le mure prendono il nome dal lato da cui arriva il vento."],
      ["Due barche a vela si incrociano, una mure a sinistra e una mure a dritta. Chi deve lasciare strada?", "Quella mure a sinistra", ["Quella mure a dritta", "La più piccola", "Quella che va più veloce"], "Tra barche a vela con mure diverse, quella mure a sinistra lascia strada a quella mure a dritta."] ],
    [ ["Che cos'è il vento apparente?", "Il vento che si sente a bordo: vento reale più vento dovuto al moto della barca", ["Il vento indicato dalle previsioni", "Il vento misurato da fermi", "Il vento delle raffiche"], "È il vento su cui lavora la vela, ed è quello indicato dal segnavento in cima all'albero."],
      ["Quando la barca accelera, il vento apparente si sposta…", "verso prua", ["verso poppa", "non si sposta", "verso il lato sottovento"], "Il vento dovuto al moto arriva da prua e si somma al vento reale."],
      ["Navigando in poppa, il vento apparente è…", "più debole del vento reale", ["più forte del vento reale", "uguale al vento reale", "sempre nullo"], "In poppa la barca «scappa» dal vento; di bolina invece il vento apparente è più forte."],
      ["Al traverso la barca accelera. Cosa conviene fare con la vela?", "Cazzarla un po'", ["Lascarla un po'", "Lasciarla com'è", "Lascarla del tutto"], "Il vento apparente si sposta verso prua, quindi la vela deve seguirlo e va cazzata."] ],
    [ ["Che cos'è una virata?", "Cambiare mure passando con la prua attraverso il vento", ["Cambiare mure passando con la poppa attraverso il vento", "Girare di 360°", "Poggiare fino alla poppa"], "La virata attraversa l'angolo morto; la strambata attraversa la poppa."],
      ["Perché una virata può fallire?", "Perché la barca non ha abbastanza velocità per attraversare l'angolo morto", ["Perché la vela è troppo cazzata", "Perché il vento è troppo forte", "Perché la barra è al centro"], "Nell'angolo morto la vela non spinge: la barca deve attraversarlo con l'abbrivio."],
      ["Come si fa una strambata controllata?", "Si cazza la vela, si poggia finché il vento passa dall'altro lato, poi si lasca", ["Si lasca tutta la vela e si poggia", "Si orza con decisione", "Si lascia fare alla barca"], "Cazzando prima, il boma fa un tragitto breve invece di attraversare la barca con violenza."],
      ["Che cosa significa bordeggiare?", "Risalire il vento a zig-zag, virando fra un tratto e l'altro", ["Navigare vicino alla costa", "Navigare in poppa", "Fare il giro di una boa"], "Ogni tratto di bolina fra due virate si chiama bordo."],
      ["Con quale comando il timoniere annuncia la virata?", "«Pronti a virare?», poi «Viro!»", ["«Pronti a strambare?», poi «Strambo!»", "«Barra!»", "«Molla!»"], "Per la strambata si usa invece «Pronti a strambare?» e poi «Strambo!»."] ],
    [ ["Come si riconosce una raffica in arrivo?", "Una chiazza d'acqua più scura e increspata che arriva da sopravento", ["Onde più alte da sottovento", "Un cambio di colore del cielo", "Non si può riconoscere"], "Le raffiche viaggiano col vento: si vedono arrivare da sopravento."],
      ["Entri in una raffica e la barca sbanda molto. Qual è la prima cosa da fare?", "Lascare la scotta", ["Cazzare la scotta", "Poggiare con decisione", "Centrare la barra"], "Lascare riduce la forza sulla vela; di bolina si può anche orzare di poco per scaricarla."],
      ["Che cosa significa scuffiare?", "Rovesciarsi", ["Fermarsi nell'angolo morto", "Virare male", "Andare all'indietro"], "Succede alle derive quando lo sbandamento diventa eccessivo."],
      ["Come si raddrizza una deriva scuffiata?", "Salendo sulla lama di deriva e facendo leva col proprio peso", ["Tirando la scotta da dentro l'acqua", "Aspettando che il vento la raddrizzi", "Spingendo sull'albero"], "Col peso sulla lama la barca ruota e torna dritta; poi si risale a bordo."] ]
  ];

  // Esame del livello 1 (0.20): una domanda per concetto insegnato, col titolo del passo da cui nasce.
  // ESAME[lezione] = [[passo, domanda, giusta, [sbagliate], spiegazione], …]; ogni esame ne estrae QUOTE[lezione] per lezione.
  // Ogni lezione deve avere almeno QUOTE + 1 domande (lo controlla tests/collaudo_esame.py).
  const QUOTE = [4, 3, 4, 3, 3, 3], SOGLIA_ESAME = 16;
  const ESAME = [
    [ ["Dritta e sinistra", "La barca punta verso il basso dello schermo. Il lato della barca che vedi a destra sullo schermo si chiama…", "sinistra", ["dritta", "sopravento", "poppa"], "Dritta e sinistra si contano guardando verso prua: se la prua punta in basso, sono invertite rispetto allo schermo."],
      ["Sopravento e sottovento", "Dove siede il timoniere, rispetto al vento?", "Sopravento, per fare contrappeso", ["Sottovento, per stare vicino al boma", "Al centro, per non far sbandare", "A prua, per vedere il vento"], "La vela e il boma stanno sottovento; il timoniere siede dal lato opposto, sopravento, per fare contrappeso."],
      ["Poggiare", "Poggiare significa…", "allontanare la prua dal vento", ["avvicinare la prua al vento", "girare la barca sempre verso dritta", "aprire la vela verso l'esterno della barca"], "Poggiare allontana la prua dal vento; orzare la avvicina."],
      ["Orzare e l'angolo morto", "Che cosa succede se la prua punta troppo vicino al vento?", "La vela sbatte, non spinge e la barca si ferma", ["La vela spinge di più e la barca accelera", "La barca sbanda di colpo e rischia di scuffiare", "Il boma passa di colpo dall'altro lato"], "È l'angolo morto: la vela prende il vento di taglio e nessuna barca a vela può andare dritta contro il vento."],
      ["La scotta: lascare", "Cazzare la scotta significa…", "tirarla, così la vela si avvicina al centro", ["mollarla, così la vela si apre verso l'esterno", "legarla, così la vela resta ferma dov'è", "tirarla, così la vela si apre verso l'esterno"], "Cazzare è tirare la scotta e chiudere la vela; lascare è mollarla e aprirla."] ],
    [ ["Come si timona", "Vuoi che la prua giri verso sinistra. Da che parte sposti la barra?", "La sposti verso dritta", ["La sposti verso sinistra", "La tieni ferma al centro", "Dipende da dove sta il boma"], "La barra gira la pala dalla parte opposta, quindi la prua va dalla parte opposta a quella verso cui sposti."],
      ["Barra sottovento: si orza", "Il boma è sul lato sinistro e sposti la barra verso sinistra. Che cosa fa la barca?", "Orza: la prua sale verso il vento", ["Poggia: la prua si allontana dal vento", "Si ferma con la prua nel vento", "Stramba: il boma passa dall'altro lato"], "Il boma sta sottovento: barra verso il boma, cioè sottovento, e la barca orza."],
      ["Barra sopravento: si poggia", "Vuoi poggiare. Verso quale lato sposti la barra?", "Verso il lato sopravento, lontano dal boma", ["Verso il lato sottovento, dove sta il boma", "Sempre verso dritta, qualunque sia il vento", "Al centro, e lasci fare al vento"], "Barra sopravento, cioè dalla parte opposta al boma, e la barca poggia."],
      ["Tenere la rotta", "Un timoniere corregge la rotta con colpi di barra ampi e continui. Che effetto ha?", "La barca rallenta: ogni angolo di barra frena", ["La barca accelera, perché il timone la spinge avanti", "Nessuno: la barra non cambia la velocità", "La barca tiene meglio la rotta e va più dritta"], "Ogni angolo di barra frena la barca: timonare bene vuol dire usarne poca."] ],
    [ ["Riepilogo", "Quale ordine va dall'andatura più vicina al vento a quella più lontana?", "Bolina, traverso, lasco, gran lasco, poppa", ["Traverso, bolina, lasco, poppa, gran lasco", "Bolina, lasco, traverso, gran lasco, poppa", "Poppa, gran lasco, lasco, traverso, bolina"], "Dalla più vicina alla più lontana dal vento: bolina, traverso, lasco, gran lasco, poppa."],
      ["Poppa", "La poppa è l'andatura più veloce?", "No: il traverso e il lasco sono più veloci", ["Sì: il vento spinge la vela da dietro", "Sì, ma solo con la vela tutta cazzata", "No: la più veloce è la bolina stretta"], "In poppa il vento spinge da dietro, ma il traverso e il lasco sono andature più veloci."],
      ["Le mure", "Navighi mure a dritta. Da che parte sta il boma?", "A sinistra", ["A dritta", "Al centro della barca", "Dipende dall'andatura"], "Mure a dritta vuol dire vento sul lato destro, e il boma sta sempre dal lato opposto alle mure."],
      ["Filetto sottovento", "Il filetto sottovento si agita, quello sopravento è dritto. Come regoli la vela?", "La lasco: è troppo cazzata", ["La cazzo: è troppo lascata", "Non la tocco: è regolata", "La cazzo ancora, fino in fondo"], "Filetto sottovento agitato: la vela è troppo cazzata e va in stallo, quindi si lasca finché i filetti tornano dritti."],
      ["Poggi e laschi", "Stai poggiando dal traverso verso il lasco. Che cosa fai con la vela?", "La lasco, perché resterebbe troppo chiusa", ["La cazzo, perché resterebbe troppo aperta", "Non la tocco: va bene com'è", "La cazzo tutta, fino al centro"], "Poggiando la vela resta troppo chiusa e va lascata: orzi e cazzi, poggi e laschi."] ],
    [ ["Il vento che senti a bordo", "Su quale vento lavora la vela?", "Sul vento apparente, quello che si sente a bordo", ["Sul vento reale, quello che soffia sul mare", "Sul vento delle raffiche, che è il più forte di tutti", "Sul vento indicato dalle previsioni del meteo"], "La vela lavora sul vento apparente: il vento reale sommato a quello dovuto al moto della barca."],
      ["Accelerando", "Il vento reale arriva di fianco e la barca accelera. Rispetto al reale, il vento apparente diventa…", "più forte, e arriva più da prua", ["più debole, e arriva più da poppa", "uguale, in forza e in direzione", "così debole da non spingere la vela"], "Accelerando, al vento reale si somma quello dovuto al moto: l'apparente si sposta verso prua ed è più forte."],
      ["Da fermi", "La barca è quasi ferma. Come sono il vento apparente e il vento reale?", "Quasi uguali, in direzione e in forza", ["L'apparente è molto più forte del reale", "L'apparente arriva sempre da poppa", "L'apparente sparisce del tutto"], "Senza il vento dovuto al moto della barca, il vento apparente coincide quasi con quello reale."],
      ["In poppa", "Di bolina, rispetto al vento reale, il vento apparente è…", "più forte", ["più debole", "sempre uguale", "girato verso poppa"], "Di bolina la barca va incontro al vento e l'apparente è più forte; in poppa invece è più debole."] ],
    [ ["Cambiare mure", "Che cos'è una strambata?", "Cambiare mure con la poppa che attraversa il vento", ["Cambiare mure con la prua che attraversa il vento", "Poggiare fino a portare il vento esattamente da dietro", "Fermarsi con la prua nel vento e poi arretrare"], "Nella strambata è la poppa ad attraversare il vento; nella virata è la prua."],
      ["Prepararsi a virare", "Che cos'è l'abbrivio?", "La velocità che la barca ha già e conserva", ["La spinta del vento sulla vela cazzata", "La forza che fa sbandare la barca in raffica", "Il tratto di bolina fra una virata e l'altra"], "È la velocità che porta la barca attraverso l'angolo morto, dove la vela non spinge."],
      ["La strambata", "Perché in poppa la strambata è delicata?", "Il boma attraversa la barca di colpo", ["La prua si pianta nel vento e si ferma", "La vela smette di spingere del tutto", "Il timone comincia a funzionare al contrario"], "Con la vela tutta aperta il boma attraversa la barca con violenza: può far scuffiare o colpire qualcuno."],
      ["Una virata che non riesce", "La barca si è piantata nel vento e comincia ad arretrare. Come ne esci?", "Sposta la barra verso il boma, poi centri e cazzi", ["Muovi la barra di continuo da un lato all'altro", "Cazzi e lasci la scotta di continuo, senza toccare la barra", "Tieni ferma la prua con la barra, senza farla girare"], "Andando all'indietro la barra funziona al contrario: spostata verso il boma, la prua si allontana dal vento. Quando la prua è fuori dall'angolo morto si centra la barra e si cazza, e la vela torna a spingere. Finché la prua resta nel vento, la vela non può spingere la barca in avanti."] ],
    [ ["Raffiche e sbandamento", "Che cos'è lo sbandamento?", "L'inclinazione della barca spinta dal vento sulla vela", ["Lo scivolamento della barca di lato, verso sottovento", "La rotazione della prua verso il vento in raffica", "Il rallentamento improvviso della barca in raffica"], "Più vento vuol dire più forza sulla vela, e la barca si inclina: è lo sbandamento."],
      ["La scuffia", "Quale comportamento in raffica porta più facilmente alla scuffia?", "Tenere la vela tutta cazzata senza lascare", ["Lascare la scotta appena entri nella raffica", "Orzare un poco tenendo la vela regolata", "Sporgersi fuori bordo per fare contrappeso"], "Con la vela tutta cazzata e senza lascare, la forza della raffica fa sbandare la barca fino a rovesciarla."],
      ["Assorbire una raffica", "La raffica è passata e la barca si raddrizza. Che cosa fai con la vela?", "La cazzi di nuovo fino a regolarla", ["Lasci ancora un po' di scotta", "Non la tocchi più fino alla boa", "La fai sbattere per rallentare"], "In raffica si lasca per ridurre la forza sulla vela; quando la raffica passa si cazza di nuovo."],
      ["Raffiche e sbandamento", "Vuoi capire se sta arrivando una raffica. Dove guardi?", "Sull'acqua sopravento: chiazze più scure e increspate", ["Sull'acqua sottovento: onde più alte e più lunghe del solito", "Il filetto sopravento, che si agita prima che arrivi", "La vela, che comincia a sbattere prima che arrivi"], "Dove il vento è più forte l'acqua è più scura e increspata, e la chiazza viaggia col vento: per questo arriva da sopravento."] ]
  ];

  // ---- glossario ----
  const GLOSS = [
    ["Abbrivio", "La velocità che la barca conserva per inerzia, per esempio mentre attraversa il vento durante una virata.", "Lezione 5"],
    ["Albero", "Il palo verticale che regge la vela.", "Lezione 1"],
    ["Andatura", "La direzione della barca rispetto al vento: bolina, traverso, lasco, gran lasco, poppa.", "Lezione 3"],
    ["Angolo morto", "Il settore attorno alla direzione del vento in cui la vela non spinge e non si può navigare: nelle scuole si indica di solito in circa 45° per lato (90° in tutto); le derive riescono a stringere un po' di più.", "Lezione 1"],
    ["Barra", "Il manico del timone. Si sposta dalla parte opposta a quella verso cui si vuole girare: barra sottovento, la barca orza; barra sopravento, la barca poggia.", "Lezione 2"],
    ["Boa", "Galleggiante ancorato al fondo, usato come riferimento o come segnale.", "Prove"],
    ["Linea d'arrivo", "Linea immaginaria fra due boe (in regata spesso fra una boa e la barca giuria): si arriva quando la si attraversa venendo dal percorso.", "Prove"],
    ["Bolina", "L'andatura più vicina al vento. Bolina stretta: circa 45°, il massimo che la barca riesce a stringere; bolina larga: circa 60-75°.", "Lezione 3"],
    ["Boma", "L'asta orizzontale, fissata all'albero, che tiene il lato basso della randa.", "Lezione 1"],
    ["Bordeggiare", "Risalire il vento a zig-zag, alternando tratti di bolina sulle due mure. Ogni tratto è un bordo.", "Lezione 5"],
    ["Cazzare", "Tirare una scotta: la vela si avvicina al centro della barca.", "Lezione 1"],
    ["Cima", "A bordo le corde si chiamano cime.", "Lezione 1"],
    ["Deriva (barca)", "Piccola barca a vela senza cabina, con la lama di deriva mobile. È la barca su cui di solito si impara.", "Lezione 1"],
    ["Deriva (lama)", "La lama che scende sotto lo scafo e impedisce alla barca di essere spinta di lato dal vento.", "Lezione 1"],
    ["Dritta", "Il lato destro della barca, guardando verso prua.", "Lezione 1"],
    ["Filetti", "Nastrini sulla vela che mostrano come scorre l'aria: dritti se la vela è regolata; si agita quello sopravento se è troppo lascata, quello sottovento se è troppo cazzata.", "Lezione 3"],
    ["Fileggiare", "Il movimento della vela che sbatte perché è troppo lascata o perché la barca è nell'angolo morto.", "Lezione 1"],
    ["Gran lasco", "Andatura con il vento quasi da dietro, circa 150°.", "Lezione 3"],
    ["Lascare", "Mollare una scotta: la vela si apre verso l'esterno.", "Lezione 1"],
    ["Lasco", "Andatura con il vento che arriva da dietro il fianco, circa 120°.", "Lezione 3"],
    ["Mure", "Il lato da cui arriva il vento: mure a dritta se arriva da destra, mure a sinistra se arriva da sinistra. Tra due barche a vela con mure diverse, quella mure a sinistra deve lasciare strada.", "Lezione 3"],
    ["Nodo", "Unità di velocità in mare: un miglio nautico all'ora, cioè 1,852 km/h.", "Lezione 1"],
    ["Orzare", "Girare la prua verso il vento.", "Lezione 1"],
    ["Orziera", "Barca che tende a salire da sola verso il vento. Le cause possono essere diverse e spesso si sommano: il vento e le raffiche, le onde che spostano la prua, la barca molto sbandata, le vele troppo cazzate, la posizione e il peso dell'equipaggio. Si corregge con la barra e, quando si può, con le vele e con il peso.", "Lezione 2"],
    ["Poggiare", "Girare la prua allontanandola dal vento.", "Lezione 1"],
    ["Poppa (andatura)", "Andatura con il vento esattamente da dietro.", "Lezione 3"],
    ["Poppa (parte della barca)", "La parte posteriore della barca.", "Lezione 1"],
    ["Prua", "La parte anteriore della barca.", "Lezione 1"],
    ["Raddrizzare", "Rimettere dritta una deriva scuffiata, salendo sulla lama di deriva e facendo leva col proprio peso.", "Lezione 6"],
    ["Raffica", "Aumento breve del vento, visibile sull'acqua come una chiazza più scura e increspata.", "Lezione 6"],
    ["Randa", "La vela principale, fissata all'albero e al boma.", "Lezione 1"],
    ["Rilevamento", "La direzione, in gradi a partire da nord in senso orario, in cui si vede un oggetto dalla barca.", "Prove"],
    ["Sbandamento", "L'inclinazione laterale della barca spinta dal vento.", "Lezione 6"],
    ["Scarroccio", "Lo scivolamento laterale della barca spinta dal vento, che la deriva riduce ma non annulla.", "Lezione 1"],
    ["Scotta", "La cima con cui si regola la vela.", "Lezione 1"],
    ["Scuffiare", "Rovesciarsi: succede alle derive quando lo sbandamento diventa eccessivo.", "Lezione 6"],
    ["Segnavento", "La piccola freccia gialla in cima all'albero: la punta indica da dove arriva il vento apparente (per questo sembra opposta alla freccia gialla grande «apparente», che arriva dal mare e punta verso la barca).", "Lezione 4"],
    ["Sinistra", "Il lato sinistro della barca, guardando verso prua.", "Lezione 1"],
    ["Sopravento", "Il lato colpito per primo dal vento; in generale, la parte da cui arriva il vento.", "Lezione 1"],
    ["Sottovento", "Il lato riparato, opposto a quello da cui arriva il vento.", "Lezione 1"],
    ["Sporgersi fuori bordo", "Spostare il peso fuori dalla barca, sopravento, per contrastare lo sbandamento.", "Lezione 6"],
    ["Stallo", "Vela troppo cazzata: non sbatte, ma l'aria non ci scorre sopra bene e la barca rallenta.", "Lezione 1"],
    ["Strambata", "Cambio di mure passando con la poppa attraverso il vento; detta anche abbattuta. Se involontaria o fatta con la vela aperta, il boma attraversa la barca con violenza.", "Lezione 5"],
    ["Timone", "La pala immersa a poppa che fa girare la barca, comandata dalla barra.", "Lezione 1"],
    ["Traverso", "Andatura con il vento perpendicolare alla barca, circa 90°.", "Lezione 3"],
    ["Vento apparente", "Il vento che si sente a bordo: combinazione del vento reale e del vento creato dal moto della barca. È quello su cui lavora la vela.", "Lezione 4"],
    ["Vento reale", "Il vento come soffia rispetto al mare, quello che si misura da fermi.", "Lezione 4"],
    ["Virata", "Cambio di mure passando con la prua attraverso il vento.", "Lezione 5"]
  ];

