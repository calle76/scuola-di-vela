// Scuola di vela, contenuti.js — Contenuti: lezioni, prove, ripassi, esame, glossario.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
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
             "Rilascia quando il vento arriva quasi da dietro. Non andare oltre: il boma cambierebbe lato di colpo (è una <em>strambata</em>, lezione 6). La vela si regola da sola."],
      cond: I => I.twa >= 135,
      done: "Hai poggiato: ora il vento arriva da dietro, e il boma si è aperto verso l'esterno per ricevere il vento." },
    { title: "Orzare e l'angolo morto", allow: ["irons"], tiller: true, turnHint: true, autoTrim: true, hud: 1, hintKind: "sail",
      text: [() => `Ora tieni premuto <em>${turnKey(orzaSide())}</em>: la prua gira a ${orzaSide()}, verso il vento. Si dice <em>orzare</em>. Quando la prua è quasi nel vento (la lancetta della rosa entra nel rosso), rilascia: la vela sbatte, non spinge più e la barca rallenta fino a fermarsi.`,
             "Se tieni premuto troppo a lungo, la prua attraversa il vento e la barca vira: premi <em>Ricomincia</em>."],
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
             "Sposta la barra verso il boma e orza fino alla <em>bolina</em>, <em>a piccoli colpi</em> e non con un colpo lungo: fermati quando la lancetta della rosetta (in basso) è a un terzo della strada tra il rosso e l'orizzontale. Poi centra la barra."],
      cond: (I, S, B) => I.twa >= 43 && I.twa <= 67 && Math.abs(I.r) < 4 && (B.barraLee || 0) >= 0.1, hold: 1, // 1.1.3: con la barca dell'1b, che orza da sola, serve anche la barra verso il boma
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
      cond: (I, S, B) => I.twa >= 43 && I.twa <= 72 && Math.abs(I.r) < 4 && (B.barraLee || 0) >= 0.1, hold: 1, // 1.1.3: come 2.4, la barca dell'1b orza da sola
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
      text: ["Poggia ancora, piano, finché il vento arriva esattamente da dietro: la <em>poppa</em> (il settore con il bordo tratteggiato).", "Attenzione a non superare i 180°. Il vento passerebbe dall'altro lato della vela e il boma attraverserebbe la barca di colpo: è una <em>strambata</em>, e con la vela tutta aperta spesso fa scuffiare. Come farla in sicurezza lo vedrai nella lezione 6."],
      cond: I => I.twa >= 167, hold: 1,
      done: "In poppa la vela è aperta al massimo e il vento la spinge da dietro. Sembra strano, ma non è l'andatura più veloce: il traverso e il lasco lo sono di più." },
    { title: "Le mure", ...PAUSE, zoom: 2, rose: true, labels: ["sopravento", "boma"],
      text: ["Se il vento arriva sul lato sinistro della barca si naviga <em>mure a sinistra</em>; se arriva sul lato destro, <em>mure a dritta</em>. Il boma sta sempre dal lato opposto alle mure. Questa barca ha il vento da sinistra: è mure a sinistra.",
             "Le mure contano anche quando due barche si incrociano, per decidere chi lascia strada: lo vedrai nel gruppo «Regole e partenze», dalla lezione 12."] },
    { title: "I filetti", ...PAUSE, zoom: 3.2, labels: ["filetti"],
      text: ["Sulla randa ci sono due nastrini, i <em>filetti</em>: rosso sul lato sinistro della vela, verde sul lato destro. Mostrano come scorre l'aria.",
             "Entrambi dritti verso il boma: vela regolata. Si agita quello <em>sopravento</em>: vela troppo lascata, cazza. Si agita quello <em>sottovento</em>: vela troppo cazzata, lasca."] },
    { title: "Filetto sopravento", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Da qui la vela la regoli tu; in questi passi la rotta la tiene la scuola. Lasca la scotta (freccia ↓) finché il filetto <em>sopravento</em> si agita chiaramente. Il suggerimento è spento: guarda i filetti."],
      cond: I => I.tt === "wind" && I.alpha < 6, hold: 1, // 1.0.37: 2° di margine dal confine (8°), altrimenti il passo dopo trova già vera la sua condizione
      done: "Il filetto sopravento si agita: la vela è troppo lascata e l'aria la prende di taglio." },
    { title: "Filetti dritti", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Ora impara a cazzare: tira la scotta (freccia ↑) poco alla volta, finché entrambi i filetti scorrono dritti. In mare puoi anche poggiare; qui la barra è bloccata e si esercita la scotta."],
      cond: I => I.tt === "ok" && I.alpha >= 10 && I.alpha <= 25, hold: 1.5, // 1.0.37: lontano dai confini 8° e 27°
      done: "Vela regolata." },
    { title: "Filetto sottovento", sheet: true, hud: 1, hintKind: "none", zoom: 1.6,
      text: ["Cazza ancora, troppo, finché si agita il filetto <em>sottovento</em>."],
      cond: I => I.tt === "lee", hold: 0.5, // 1.1.3: era anche alpha > 29 con hold 1; il filetto si agita da 27° (ttState): con la barca dell'1b, che orza, chi si fermava al filetto agitato non arrivava mai a 29°
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
             "Il vento che senti a bordo, e su cui lavora la vela, è il <em>vento apparente</em>: la somma del <em>vento reale</em> e del vento dovuto al moto della barca. Freccia bianca: reale. Freccia gialla: apparente."] },
    { title: "Da fermi", sheet: true, hud: 2, arrows: true, hintKind: "none",
      text: ["Lasca tutta la vela (freccia ↓) e aspetta che la barca rallenti sotto i 2,5 nodi; la rotta la tiene la scuola. Guarda le due frecce e i numeri nel pannello."],
      cond: I => I.kn < 2.5, hold: 1.5, // 1.0.6: era 2 nodi; con la resistenza della vasca, vela tutta lascata al traverso, la barca si assesta a 2,1 nodi
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
      cond: (I, S, B) => I.twa >= 43 && I.twa <= 72 && I.tt === "ok" && I.kn >= 3.3 && (B.barraLee || 0) >= 0.1, hold: 1, // 1.1.3: come 2.4
      done: "Pronto. Durante la virata la prua attraversa l'angolo morto, dove la vela non spinge: la barca lo supera grazie all'<em>abbrivio</em>, la velocità che ha già." },
    { title: "Virare", tiller: true, sheet: true, hud: 1, rose: true, hintKind: "tt",
      text: ["Sposta la barra <em>sottovento</em> (verso il boma) con decisione e tienila finché la prua ha attraversato il vento e sei in bolina sull'altro lato. Poi centra la barra.",
             "In bolina la vela resta cazzata su entrambe le mure: non serve toccarla."],
      cond: (I, S, B) => S.tacks > B.tacks && I.twa >= 40 && I.twa <= 78 && I.kn > 1.2, hold: 0.8,
      done: "Virata riuscita: il boma è passato dall'altra parte e il timoniere ha cambiato lato. A bordo si annuncia così: «Pronti a virare?», «Pronti!», «Viro!»." },
    { title: "Una virata che non riesce", allow: ["irons"], tiller: true, sheet: true, hud: 1, rose: true, hintKind: "none",
      text: ["Ora senza abbrivio: lasca la vela finché la barca scende sotto 1 nodo, poi prova a virare.",
             "Orza a bolina lascando: rallenta fino a perdere l'abbrivio e fallendo la virata. Se la barca arretra risponde al timone in modo opposto. Porta la prua fuori dall'angolo morto, centra e cazza per ripartire."],
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
             "Più vento vuol dire più forza sulla vela, e la barca si inclina: è lo <em>sbandamento</em>, che vedi sull'indicatore in basso a sinistra. Il timoniere si sporge fuori bordo per contrastarlo, ma con un attimo di ritardo. Al traverso e al lasco, in raffica <em>poggia</em> anche un poco: orzare ti farebbe sbandare di più."] },
    { title: "Assorbire una raffica", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", bigGust: 0.45,
      text: ["Naviga di bolina con la vela regolata e aspetta una raffica. Quando ci entri, <em>lasca</em> un poco (e di bolina puoi anche <em>orzare</em> leggermente) per tenere lo sbandamento sotto i 20°. Passata la raffica, cazza di nuovo."],
      cond: (I, S, B) => I.gustK > 0.3 && I.twa <= 75 && I.heel < 20 && I.kn > 2 && (B.lasca || 0) >= 0.05, hold: 3, // 1.1.3: anche lascare in raffica; la barca dell'1b orzava da sola e scaricava la vela // 1.0.15: nel cuore della raffica (+30%) e di bolina; prima bastava il bordo (+12%) e si completava da solo
      done: "Ben fatto. Lascare riduce la forza sulla vela; orzare di poco la scarica. È la tecnica principale per navigare con vento rafficato." },
    { title: "La scuffia", allow: ["capsizes"], noRight: true, tiller: true, sheet: true, hud: 3, env: { tws: 15, gusts: 2 }, hintKind: "none", bigGust: true,
      text: ["Ora il vento è più forte e le raffiche più violente. Per capire il limite, fai apposta l'errore: vela tutta cazzata, e in raffica non lascare."],
      cond: (I, S, B) => S.capsizes > B.capsizes, hold: 0.8,
      done: "Oltre circa 60° di sbandamento la barca si è rovesciata: ha <em>scuffiato</em>. Per una deriva capita, non è un dramma: si raddrizza." },
    { title: "Raddrizzare", startCapsized: true, tiller: true, sheet: true, hud: 3, env: { tws: 15, gusts: 2 }, hintKind: "tt",
      text: ["Premi <em>Raddrizza</em> (o il tasto A): ci vogliono una decina di secondi. Nella realtà si liberano le scotte e il timoniere fa leva sulla deriva col proprio peso."],
      cond: (I, S, B) => B.cap0 && !S.capsized, hold: 1, // B.cap0: la barca era rovesciata all'inizio del passo (showStep la rovescia se serve)
      done: "Barca dritta, al traverso, vela lascata: regola con i filetti e riparti." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", final: true,
      text: ["Guarda le raffiche arrivare, <em>lasca</em> quando entri, <em>cazza</em> quando escono. Oltre circa 60° di sbandamento si <em>scuffia</em>.",
             "Esercitati, poi prova il percorso nelle raffiche."] }
  ];

  // ---- lezioni nuove della scuola (1.1.4, docs/PROPOSTA-LEZIONI-SCUOLA.md): nascoste nel menu finché non arriva il menu nuovo ----
  // B1, il timone che stalla. Fonti lette prima del testo (docs/archivio/PROPOSTA-STALLO-TIMONE.md §1, §9, §10):
  // F4 (Masuyama e Ogihara 2020): in vasca, modellino 1:5 del 470, la forza della pala cresce fino a circa 15° e poi resta costante, mentre
  //   la resistenza continua a crescere; nelle virate vere di un 470 la barra arriva a 45°; accompagnarla è il modo più ragionevole, sbatterla fa perdere più velocità.
  // F35 (Proceedings MDPI 2018): calcolo a grandezza vera, stallo a circa 30° di barra (35° a 10 m/s).
  // Day 2017 §3.3: l'angolo che la pala sente non è quello della barra. Gioco: freccia fino a 35° = regola del gioco senza fonte (1.0.25);
  //   con i tasti la pala stalla di rado (misurato: 0 s di stallo in 6 prove da 2 a 5,5 nodi, 1 novembre 2026); con Maiusc la prua gira più in fretta
  //   quando si centra la barra (PROPOSTA-STALLO-TIMONE §10: 26 contro 18 °/s con 10 nodi).
  const LB1 = [
    { title: "La pala è un'ala", ...PAUSE, zoom: 2.4,
      text: ["La pala del timone lavora nell'acqua come un'ala: più angolo le dai, più spinge di lato la poppa, e la barca gira.",
             "Oltre un certo angolo l'acqua non riesce più a seguirla e si stacca: la pala va <em>in stallo</em>. La spinta smette di crescere, ma la pala frena sempre di più. Su una deriva da regata, misurato in vasca e calcolato al computer, succede fra circa 15° e 30°.",
             "Conta l'angolo che la pala sente, non quello della barra: quando la barca gira, l'acqua arriva sulla pala un po' di traverso, e l'angolo sentito è più piccolo."] },
    { title: "35° e 45°", ...PAUSE, zoom: 2.4,
      text: ["Con la sola freccia la barra arriva a 35°: è una regola di questo gioco, un angolo sicuro (una barca vera non ha un fermo, c'è la mano che sente la barra).",
             "Con <em>Maiusc</em> più la freccia arriva a 45°, come nelle virate misurate su una deriva da regata vera: la barca gira più stretta. Serve vicino a una boa, nei giri di penalità o quando la barca è lenta. Meglio accompagnare la barra che sbatterla.",
             "Con i tasti la pala stalla di rado, perché la barca comincia a girare prima che l'angolo diventi troppo grande. Se succede, il pannello lo dice."] },
    { title: "Una virata con la barra in fondo", tiller: true, autoTrim: true, hud: 1, rose: true, hintKind: "tt",
      text: ["Mettiti in bolina e vira tenendo <em>Maiusc</em> con la freccia verso il boma, finché la prua ha attraversato il vento. Poi centra la barra: con 45° la prua gira più in fretta, quindi centra un po' prima."],
      cond: (I, S, B) => S.tacks > B.tacks && I.twa >= 40 && I.twa <= 78 && I.kn > 1.2 && (B.maiusc || 0) >= 0.3, hold: 0.8,
      done: "Virata con la barra in fondo: la barca ha girato più stretta. Più barra vuol dire anche più controllo da tenere: centrando tardi la prua va oltre la bolina." },
    { title: "Riepilogo", tiller: true, autoTrim: true, hud: 1, hintKind: "sail", final: true,
      text: ["La pala è un'ala e oltre un certo angolo stalla. La sola freccia si ferma a 35°; <em>Maiusc</em> porta la barra a 45° quando serve girare stretto. Accompagna la barra e centrala per tempo."] }
  ];

  // B2, spingere il boma (1.1.5). Fonti (docs/archivio/PROPOSTA-SPINGI-BOMA.md §1, parafrasi): W1 US Sailing «Getting in and out of irons», W2 guida di un
  // circolo per una deriva in singolo, Australian Sailing «Drills for Skills: Sailing Backwards»: barca ferma nel vento, boma spinto fuori da una parte e barra
  // dalla stessa parte; la vela prende il vento al contrario, la barca va all'indietro e la prua gira verso il boma, lontano dal vento; al traverso si molla
  // il boma, si centra la barra e si cazza. Un allenatore (The Final Beat): all'indietro si esce da un brutto posto sulla linea di partenza. Nessuna fonte dà numeri.
  // Regolamento F15, regola 21.3 (riletta nel PDF il 1 novembre 2026): chi va all'indietro, o di lato verso il vento, spingendo una vela si tiene lontano da chi
  // non lo fa. Il gioco non la applica: il testo lo dice. Gioco: Z tenuto premuto mette il boma a 80° (1.0.26, BOMA2).
  // Misurato il 1 novembre 2026 (passo 3, prua a 10° dal vento, 10 nodi): a mani ferme in 30 s la prua arriva a 20° e la barca scivola all'indietro a 1,8 nodi;
  // con Z e la barra verso il boma la barca arretra fino a 2,4 nodi, la prua gira verso il boma ed è al traverso in 2,7 s.
  const LB2 = [
    { title: "Fuori dall'angolo morto", ...PAUSE, zoom: 2.4,
      text: ["Se la barca si ferma con la prua nel vento, la vela sbatte e il timone non serve: è l'<em>angolo morto</em>. Lasciata a sé, la barca resta lì a lungo e scivola all'indietro. Per uscirne c'è un modo, insegnato nelle scuole.",
             "Tieni premuto <em>Z</em>: spingi il boma fuori, e metti la barra <em>dalla stessa parte del boma</em>. La vela prende il vento al contrario, la barca va all'indietro e la prua gira verso il boma, lontano dal vento.",
             "Quando sei al traverso molla Z, centra la barra e cazza: la barca riparte in avanti."] },
    { title: "All'indietro, apposta", ...PAUSE, zoom: 2.4,
      text: ["Spingere il boma serve anche a frenare o ad arretrare apposta, per esempio per uscire da un brutto posto prima della partenza.",
             "In regata chi va all'indietro spingendo la vela deve tenersi lontano da chi non lo fa (regola 21.3). In questo gioco la regola non è applicata."] },
    { title: "Spingi il boma e riparti", startIrons: true, tiller: true, sheet: true, hud: 1, rose: true, hintKind: "tt",
      text: ["Sei fermo nell'angolo morto. Tieni premuto <em>Z</em> e sposta la barra verso il boma; quando sei al traverso molla Z, centra la barra e cazza finché la barca riparte."],
      cond: (I, S, B) => (B.push || 0) >= 0.5 && !S.pushing && S.u > 0 && I.twa >= 60 && I.twa <= 120 && I.kn >= 1.5, hold: 1,
      done: "Fuori dall'angolo morto: all'indietro la prua è girata verso il boma, poi la vela ha ripreso a spingere in avanti." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 1, hintKind: "tt", final: true,
      text: ["Fermo nel vento: <em>Z</em> per spingere il boma, barra verso il boma, la barca arretra e la prua gira. Al traverso molla Z, centra e cazza."] }
  ];

  // B3, la barca che orza sbandando (1.1.6). Fonti rilette nei PDF il 1 novembre 2026 (parafrasi):
  // F4 (Masuyama e Ogihara 2020, fonti-pdf/sname-jst-2020-05.pdf) p. 28 e fig. 13: di bolina, deriva tutta giù e barca dritta, centro velico e punto di spinta
  //   dello scafo quasi coincidono, barra circa al centro; p. 32 eq. 6: sbandando il centro velico va sottovento e il momento orziero cresce con
  //   spinta × altezza del centro velico × seno dello sbandamento (galleria del vento, verificata a 20°); p. 33: anche lo scafo sbandato orza da solo, senza numeri.
  // F38 (manuale di classe, fonti-pdf/HANDBOOK_2025.pdf, pagina «Rudder and Tiller»): sbandata sottovento la barca diventa molto orziera; poggiare sbandati
  //   carica molto pala e barra (è così che si rompono, nei pochi casi visti); prima si raddrizza, sporgendosi di più o lascando la scotta.
  // Gioco: solo il termine della vela (eq. 6, 1.0.46), niente scafo: il testo lo dice. Misurato il 1 novembre 2026 (motore, 12 nodi al traverso, raffica +45% per 6 s,
  //   vela regolata): barra al centro la prua sale di 19° (5° senza raffica); tenendo la prua con la sola barra servono 2,5° di barra e la barca sbanda a 22°;
  //   lascando di 0,15 bastano 1,1° e sbanda a 11,5°.
  const LB3 = [
    { title: "Perché la barca orza", ...PAUSE, zoom: 2.4,
      text: ["Quando la barca sbanda, la vela si inclina sottovento: il vento non la spinge più sopra la barca, ma fuori, dalla parte del boma. Spinta così, di lato, la barca gira la prua verso il vento: è <em>orziera</em>. Più sbanda, più orza.",
             "Di bolina, con la barca dritta e la vela regolata, la barra sta quasi al centro: lo dicono le misure su una deriva da regata. Anche lo scafo sbandato fa orzare la barca per conto suo; in questo gioco conta solo la vela."] },
    { title: "Nella raffica", ...PAUSE, zoom: 2.4,
      text: ["In una raffica la barca sbanda di più e la prua sale di colpo verso il vento. Per tenere la rotta ci sono due modi, e si usano insieme.",
             "Con la <em>barra sopravento</em> si poggia (lezione 2). Ma se la barca resta sbandata, poggiare carica molto la pala e la barra: un manuale di classe racconta che è proprio così che si rompono.",
             "Per questo prima si <em>raddrizza</em> la barca: ci si sporge di più (qui lo fa il timoniere da solo) e si <em>lasca</em> un poco. Raddrizzata, la barca orza meno e basta poca barra."] },
    { title: "La rotta nella raffica", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", bigGust: 0.45, course: true,
      text: ["Sei al traverso. Tieni la rotta indicata sopra i comandi mentre passi in una raffica: quando la barca sbanda e la prua sale, <em>lasca</em> un poco e correggi con piccoli colpi di barra. Passata la raffica, cazza di nuovo."],
      cond: (I, S) => I.gustK > 0.3 && Math.abs(norm180(S.h - S.course)) < 6 && I.heel < 15 && I.kn > 2, hold: 2,
      done: "Rotta tenuta nella raffica: lascando la barca si è raddrizzata, e alla barra è bastato poco." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", final: true,
      text: ["Sbandando la barca orza. Nella raffica prima si raddrizza, lascando un poco, poi si corregge con poca barra. Passata la raffica, si cazza."] }
  ];

  // B4, la raddrizzata lunga (1.1.7). Fonti (parafrasi; una sola per la barca in singolo, divulgativa, e il testo lo dice):
  // video di un allenatore inglese (YouTube T7lUaEafLv8; trascrizione e fotogrammi forniti da Ale il 19 ottobre 2026, NON salvati nel progetto: si usa il riassunto
  //   di docs/archivio/PROPOSTA-RADDRIZZATA.md): si tira con la schiena al vento, timoniere sopravento e albero sottovento, così la vela sale e sbatte libera;
  //   al contrario il vento entra sotto la vela e la barca riscuffia; fatta bene, 15-20 s dalla scuffia alla barca che naviga; il traverso è letto dagli schemi.
  // Dispensa di una scuola di vela (fonti-pdf/Dispensa-Scuola-Vela-2019.pdf, pp. 24-25, riletta il 1 novembre 2026; fonte informale, mai nel quiz, decisione di Ale):
  //   scuffiare capita anche ai campioni; non si abbandona la barca; con le vele cazzate la barca non si raddrizza, le scotte vanno libere; spalle al vento,
  //   leva sulla deriva, piedi vicino allo scafo per non romperla; CON L'EQUIPAGGIO si raddrizza e si tiene la barca con la prua al vento (diverso dal gioco: detto nel testo).
  // W4 e W5 (DUBBI-E-RICERCHE §3, deboli): scotte libere mentre la barca torna su, se no riparte o riscuffia.
  // Gioco: tasto A, 10 s (RADD2, 1.0.32), poi barca ferma al traverso con la vela tutta lascata. Misurato il 1 novembre 2026 (12 nodi, semi 1-10): senza toccare
  //   più niente dopo A, con la vela che sbatte la barca arriva da sola a 2,4-3,2 nodi in 30 s; per questo il passo chiede anche i filetti dritti.
  const LB4 = [
    { title: "Prima di raddrizzare", ...PAUSE, zoom: 2.4,
      text: ["Su una deriva scuffiare capita, anche ai più bravi. La prima regola: non lasciare mai la barca. Galleggia, ti regge quando sei stanco e da lontano si vede molto meglio di una testa in acqua.",
             "Poi si liberano le scotte: con la vela cazzata la barca non torna su, oppure torna su, riparte da sola e si rovescia di nuovo. In questo gioco le scotte le libera il gioco."] },
    { title: "Spalle al vento", ...PAUSE, zoom: 2.4,
      text: ["Si sale sulla deriva con le <em>spalle al vento</em> e la si tira giù con il proprio peso, tenendo i piedi vicino allo scafo per non romperla. L'albero resta sottovento: tornando su, la vela sbatte libera e il vento non ci entra sotto. Al contrario, la barca si rovescerebbe di nuovo.",
             "Qui tutto questo è il tasto <em>A</em>: dieci secondi. Un allenatore, in un video, dice che fatta bene, dalla scuffia alla barca che naviga, ne passano 15-20.",
             "La barca torna dritta di traverso, con la vela che sbatte. Con l'equipaggio, le scuole insegnano anche a tenerla con la prua al vento finché tutti sono risaliti: questo gioco non lo fa."] },
    { title: "Raddrizza e riparti", startCapsized: true, tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt",
      text: ["Sei scuffiato. Premi <em>Raddrizza</em> (o il tasto A) e aspetta che la barca torni dritta. Poi cazza finché i filetti sono dritti e riparti al traverso."],
      cond: (I, S, B) => B.cap0 && !S.capsized && I.twa >= 60 && I.twa <= 120 && I.kn >= 2.5 && I.tt === "ok", hold: 1,
      done: "Raddrizzata e ripartita: la barca è tornata su di traverso, con la vela libera, e cazzando ha ripreso a navigare." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 3, env: { tws: 12, gusts: 1 }, hintKind: "tt", final: true,
      text: ["Non lasciare la barca, libera le scotte, raddrizza con le spalle al vento. La barca torna su di traverso con la vela che sbatte: cazza e riparti."] }
  ];

  // B5, i salti di vento (1.1.8). Fonte riletta il 1 novembre 2026 (parafrasi): D. Dellenbaugh, «Windshift Rules of Thumb», Sailing World (colonna del giugno 1987,
  //   ripubblicata in rete il 18 agosto 2020), https://www.sailingworld.com/how-to/windshift-rules-of-thumb/: di bolina, prima si capisce se il vento oscilla o gira
  //   sempre dalla stessa parte; se oscilla si vira sugli scarsi e si resta sulle mure buone; prima della partenza si guarda con la bussola fra quali prue si oscilla
  //   su ogni mura e se ne prende la media (esempio: 240-270°, media 255°; a 245° si è scarsi di 10° e si vira); se il vento gira sempre dalla stessa parte non si vira
  //   sugli scarsi ma si va verso il salto; vicino alla boa, quando resta un solo salto (nell'esempio ogni oscillazione dura circa quattro minuti), lo si gioca come persistente.
  //   Una sola fonte, di un allenatore, su una rivista: il testo lo dice. Non riletti (pagina rifiutata o non cercata): WindCheck, Raymarine (docs/archivio/PROPOSTA-SALTI-VENTO.md §1).
  // Gioco: nel passo il vento oscilla come nelle regate (SALTI2, 1.0.28: 12-15° per parte, mezza oscillazione 60-75 s, periodi più corti delle fonti, dichiarato);
  //   la scritta del vento sul mare dice il vento medio, la «Prua» del pannello la bussola. Il passo vale con due virate fatte da scarsi di almeno 7° (base.buone; con una sola chi virava a caso passava 6 volte su 10) e mai da buoni di 3° o più (base.daBuono: si ricomincia).
  const LB5 = [
    { title: "Il vento gira", ...PAUSE, zoom: 0.8,
      text: ["Il vento non cambia solo forza: cambia anche direzione, spesso avanti e indietro. In un esempio di un allenatore, di bolina la prua va da 240° a 270° e ogni oscillazione dura circa quattro minuti. In questa lezione il vento oscilla di 12-15° per parte, più in fretta.",
             "Se il vento gira verso la tua prua, per restare di bolina devi poggiare: sei <em>scarso</em>. Se gira verso poppa puoi orzare: sei <em>buono</em>. Lo stesso salto che è scarso su una mura è buono sull'altra."] },
    { title: "Vira sugli scarsi", ...PAUSE, zoom: 0.8,
      text: ["Se il vento oscilla, di bolina conviene <em>virare quando sei scarso</em>: sulle altre mure quel salto è buono, e la prua punta più verso il vento, cioè verso la boa.",
             "Per accorgertene usa la bussola: la <em>Prua</em>, nel pannello. Tenendo la bolina guarda fra quali numeri va e prendine la media. Quando la prua si allontana dal vento della media di qualche grado (nell'esempio dell'allenatore, una decina) sei scarso: vira.",
             "Due eccezioni. Se il vento gira sempre dalla stessa parte non si vira sugli scarsi: si va verso il salto. E vicino alla boa, quando resta un salto solo, si gioca come se il vento non dovesse più tornare."] },
    { title: "Vira sullo scarso", tiller: true, autoTrim: true, hud: 3, shifts: "osc", rose: true, hintKind: "sail",
      text: ["Il vento medio arriva da nord (lo dice la scritta del vento). Mettiti di bolina, guarda la Prua per un po', e quando sei scarso di quasi una decina di gradi rispetto alla media <em>vira</em>. Poi tieni la bolina sulle altre mure e aspetta il prossimo scarso: due virate così. Se viri da buono, si ricomincia. La vela si regola da sola."],
      cond: (I, S, B) => (B.buone || 0) >= 2 && !B.daBuono && I.twa >= 35 && I.twa <= 75 && I.kn > 2, hold: 3,
      done: "Due virate sugli scarsi: ogni volta, sulle altre mure, lo stesso salto ti ha fatto puntare più verso il vento." },
    { title: "Riepilogo", tiller: true, sheet: true, hud: 3, shifts: "osc", hintKind: "tt", final: true,
      text: ["Il vento oscilla: con la bussola trova la prua media, vira quando sei scarso e resta sulle mure buone. Se il vento gira sempre dalla stessa parte, o vicino alla boa, si fa diverso."] }
  ];

  // ---- gruppo D, il regolamento (1.1.9, docs/PROPOSTA-LEZIONI-2A.md): regole rilette nel PDF di F15 (fonti-pdf/RRS-2025-2028-World-Sailing.pdf) il 1 novembre 2026 ----
  // Parte 2, Sezione A: 10 mure opposte (mure a sinistra lascia strada a mure a dritta), 11 stesse mure sovrapposte (la sopravento lascia strada), 12 stesse mure
  //   non sovrapposte (la libera dietro lascia strada), 13 virando (dal vento alla bolina lascia strada a tutte; 10-12 non valgono; se virano insieme cede quella
  //   alla sinistra dell'altra o quella dietro). Definizioni: libera dietro/avanti e sovrapposte (linea al traverso del punto più a poppa), sopravento/sottovento,
  //   tenersi lontano (l'altra tiene la rotta senza manovre per evitarla). Sezione B: 14 evitare il contatto se ragionevolmente possibile (chi ha la precedenza
  //   può aspettare finché è chiaro che l'altra non si scansa), 15 chi acquista la precedenza dà all'inizio spazio (salvo se è per una manovra dell'altra), 16.1 chi
  //   ha la precedenza e cambia rotta dà spazio. 43.1(c): chi ha la precedenza è esonerato dalla 14 se il contatto non causa danni o lesioni.
  // Gioco (js/regate.js, chiCede, 1.0.40): applica 10, 11, 12 e 13 (collaudo_regole.py, collaudo_semaforo.py); 14, 15 e 16 no, e non ci sono danni: il testo lo dice.
  // Dalla 1.2.0 un esercizio per D1-D3 con una barca di scena che si muove (meccanismo A, copione). Penalità per un contatto con colpa: +15 s, due giri nella «Regata con i giri di penalità», +1 punto nel torneo (toast in js/regate.js). Dalla 1.2.1 D5-D7 hanno un esercizio
  // in regata (meccanismo B: una lezione che apre una regata), che servirà anche al gruppo C; dalla 1.2.4 la lezione 3 (Lezione 4 nel menu) non parla più di precedenze.
  const LD1 = [
    { title: "Chi lascia strada", ...PAUSE, zoom: 1.4, scenaH: 45, me: "Tu: mure a sinistra",
      scena: [{ x: 14, y: 0, h: 315, col: "#C0392B", label: "Mure a dritta" }],
      text: ["Due barche con <em>mure diverse</em> si incrociano: la barca <em>mure a sinistra</em> lascia strada a quella <em>mure a dritta</em>. È la regola 10 del regolamento di regata.",
             "Qui tu sei mure a sinistra: puoi passarle dietro poggiando un poco, oppure virare per tempo. Lasciare strada vuol dire che l'altra deve poter tenere la sua rotta senza manovrare per evitarti."] },
    { title: "Penalità e semaforo", ...PAUSE, zoom: 2,
      text: ["Nelle regate di questo gioco chi non lascia strada e provoca un contatto prende una penalità: 15 secondi, due giri nella regata con i giri di penalità, un punto in più nel torneo.",
             "Nelle impostazioni puoi accendere il <em>semaforo di precedenza</em>: quando un'altra barca si avvicina, sul tuo scafo il rosso vuol dire che devi lasciare strada, il verde che hai la precedenza. Avere la precedenza non è il permesso di urtare."] },
    { title: "Passale dietro", tiller: true, autoTrim: true, hud: 1, hintKind: "sail", scenaH: 45, me: "Tu",
      scenaMobile: [{ x: 29.7, y: 1.5, h: 315, u: 2.2, col: "#C0392B", label: "Mure a dritta" }],
      text: ["Sei di bolina mure a sinistra e da destra arriva una barca mure a dritta. Lasciale strada: poggia quanto basta per <em>passarle dietro</em>, poi torna di bolina. Lei non si sposta: se la tocchi, premi Ricomincia."],
      cond: (I, S, B) => !B.contatto && B.dietro && B.gapMin >= 2 && I.kn > 1.5, hold: 1,
      done: "Le sei passato dietro, e lei ha tenuto la sua rotta senza manovrare: così si lascia strada." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Mure diverse: lascia strada la barca mure a sinistra (regola 10). Chi non lo fa e provoca un contatto prende una penalità."] }
  ];
  const LD2 = [
    { title: "Affiancate", ...PAUSE, zoom: 2.4, scenaH: 45, me: "Tu: sopravento",
      scena: [{ x: 5.7, y: 5.7, h: 45, col: "#C0392B", label: "Sottovento" }],
      text: ["Con le <em>stesse mure</em>, se le barche sono <em>sovrapposte</em> (affiancate), la barca <em>sopravento</em>, cioè quella più vicina al vento, lascia strada a quella <em>sottovento</em>. È la regola 11.",
             "Due barche sono sovrapposte quando nessuna delle due sta tutta dietro una linea tirata al traverso dal punto più a poppa dell'altra."] },
    { title: "Libera dietro", ...PAUSE, zoom: 2.4, scenaH: 45, me: "Tu: libera dietro",
      scena: [{ x: 8.5, y: -8.5, h: 45, col: "#C0392B", label: "Libera avanti" }],
      text: ["Se invece una barca sta tutta dietro quella linea, è <em>libera dietro</em>, e lascia strada a quella <em>libera avanti</em>. È la regola 12.",
             "Qui tu sei libera dietro: se sei più veloce puoi passare, ma senza costringere l'altra a manovrare."] },
    { title: "Sorpassa senza toccarla", tiller: true, autoTrim: true, hud: 1, hintKind: "sail", scenaH: 45, me: "Tu",
      scenaMobile: [{ x: 8.5, y: -8.5, h: 45, u: 1.0, col: "#C0392B", label: "Libera avanti" }],
      text: ["Davanti a te, con le tue stesse mure, c'è una barca più lenta: tu sei libera dietro e le lasci strada. Sorpassala senza costringerla a manovrare: sposta un poco la prua da una parte, tieniti ad almeno un paio di metri e passa avanti."],
      cond: (I, S, B) => !B.contatto && B.davanti && B.gapMin >= 2, hold: 1,
      done: "Sorpasso pulito: lei ha tenuto la sua rotta e tu sei passato a distanza." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Stesse mure: se sono affiancate lascia strada la sopravento (regola 11); se no, lascia strada quella libera dietro (regola 12)."] }
  ];
  const LD3 = [
    { title: "Durante la virata", ...PAUSE, zoom: 1.8, scenaH: 0, me: "Tu: stai virando",
      scena: [{ x: -12, y: -6, h: 45, col: "#C0392B", label: "Mure a sinistra" }],
      text: ["Da quando la prua passa il vento finché la barca non è di bolina sulle nuove mure, chi vira lascia strada a tutte le altre. È la regola 13. In quei secondi, per lei, le regole 10, 11 e 12 non valgono.",
             "Se due barche virano insieme, lascia strada quella che sta alla sinistra dell'altra, o quella dietro.",
             "Quindi non virare proprio davanti a una barca vicina: anche se finisci mure a dritta, finché non sei di bolina lasci strada tu."] },
    { title: "Vira dopo che è passata", tiller: true, autoTrim: true, hud: 1, hintKind: "sail", scenaH: 45, me: "Tu",
      scenaMobile: [{ x: 13.2, y: -8.0, h: 315, u: 2.2, col: "#C0392B", label: "Mure a dritta" }],
      text: ["Sei di bolina mure a sinistra e devi virare, ma una barca mure a dritta ti passa davanti. Aspetta che sia passata e lontana, poi vira: mentre viri lasci strada tu."],
      cond: (I, S, B) => !B.contatto && S.tacks > B.tacks && B.gapVirata >= 10 && I.twa >= 35 && I.twa <= 75 && I.kn > 1.5, hold: 2,
      done: "Virata fatta dopo che è passata: nessuno ha dovuto manovrare per evitarti." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Chi vira, dal vento fino alla bolina, lascia strada a tutte le altre (regola 13)."] }
  ];
  const LD4 = [
    { title: "Evitare il contatto", ...PAUSE, zoom: 2,
      text: ["Ogni barca deve evitare il contatto, se è ragionevolmente possibile: anche quella con la precedenza. È la regola 14. Chi ha la precedenza però può aspettare a manovrare finché è chiaro che l'altra non lascia strada.",
             "Se il contatto non fa danni né feriti, chi aveva la precedenza non è penalizzato (regola 43.1(c)); se li fa, può esserlo anche lei.",
             "In questo gioco non ci sono danni: chi doveva lasciare strada ha sempre torto, l'altra mai."] },
    { title: "Non togliere spazio", ...PAUSE, zoom: 2,
      text: ["Chi ottiene la precedenza, per esempio passando avanti o finendo la virata, all'inizio deve dare all'altra lo spazio per lasciare strada, salvo quando la precedenza gliel'ha data una manovra dell'altra (regola 15).",
             "E chi ha la precedenza, se cambia rotta, deve lasciare all'altra lo spazio per tenersi lontana (regola 16).",
             "Il gioco non controlla le regole 14, 15 e 16: in regata, sull'acqua, valgono."] },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Evita sempre il contatto, anche quando hai la precedenza. Chi ottiene la precedenza o cambia rotta deve lasciare all'altra lo spazio per scansarsi."] }
  ];

  // ---- gruppo D, seconda parte: D5-D7 con un esercizio in regata (1.2.1, meccanismo B di docs/PROPOSTA-ESERCIZI-REGOLAMENTO-E-PARTENZE.md) ----
  // Regole rilette nel PDF di F15 il 2 novembre 2026: 26 (avviso 5 minuti bandiera di classe, preparatorio 4 minuti P, un minuto P ammainata, partenza classe ammainata;
  //   i tempi si prendono dai segnali visivi, un suono che manca non conta), 29.1 (scafo oltre la linea al segnale: X con un suono, esposta finché gli scafi di queste barche
  //   non sono tutti dietro la linea o i suoi prolungamenti, al più 4 minuti dopo il segnale), 21.1 (chi torna dietro la linea dopo il segnale lascia strada a chi non lo fa,
  //   finché lo scafo non è tutto dietro), 21.2 (chi sconta una penalità lascia strada), 31 (non toccare: prima della partenza le boe di partenza, la boa che apre,
  //   delimita o chiude il lato in corso, dopo l'arrivo quelle d'arrivo), 44.1 (due giri per la Parte 2, un giro per la 31), 44.2 (allontanarsi dalle altre barche appena
  //   possibile dopo l'incidente, poi subito i giri, tutti nello stesso verso, ognuno con una virata e una strambata).
  // Gioco: sequenza intera con 5 minuti di preparazione, accorciata con 3 (avviso a 3, P a 2), con 1 minuto la sola bandiera di classe (bandiereAl); X per 240 s al più;
  //   la barca è tornata quando il suo centro è dietro la linea (raceLegs: semplificazione, il testo lo dice); 21.1, 21.2, boa toccata e giri solo nella «Regata con i giri
  //   di penalità» (RACES[3]), che è quella degli esercizi; un giro vale con 360° nello stesso verso in 20 s, una virata e una strambata; giro mancante all'arrivo +15 s.
  // Esercizi: soglie (un minuto in D5, tre minuti in D6 e D7) ipotesi nostre.
  const LD5 = [
    { title: "La sequenza", ...PAUSE, zoom: 2,
      text: ["Prima della partenza la barca giuria alza e ammaina delle bandiere, sempre nello stesso ordine (regola 26). A cinque minuti dal via sale la <em>bandiera di classe</em>: è l'avviso. A quattro minuti sale la <em>P</em>, blu con il quadrato bianco: è il preparatorio.",
             "A un minuto dal via si ammaina la P. Al via si ammaina la bandiera di classe: è la partenza. Contano le bandiere, non i suoni: se un suono manca, vale la bandiera.",
             "Nel gioco la sequenza è intera quando la preparazione è di cinque minuti. Con tre minuti è accorciata (avviso a tre, P a due); con un minuto c'è solo la bandiera di classe."] },
    { title: "La linea", ...PAUSE, zoom: 2,
      text: ["La linea di partenza va dalla barca giuria alla boa arancione. Al via devi essere dietro la linea, dalla parte da cui si parte; poi la tagli e vai verso la boa di bolina.",
             "Conviene aspettare vicino alla linea, quasi fermo con la vela lascata, e cazzare qualche secondo prima del via: così parti già lanciato."] },
    { title: "Parti al segnale", ...PAUSE, zoom: 2,
      esercizio: { regata: 3, cd: 300, avversari: "nessuno",
        obiettivo: "Parti al via senza anticipo, entro un minuto",
        brief: "Esercizio della lezione 16. Una partenza da solo con la sequenza di cinque minuti: guarda le bandiere sulla barca giuria e nel riquadro. Bandiera di classe: avviso, mancano cinque minuti. Bandiera P: preparatorio, quattro minuti. P ammainata: un minuto. Classe ammainata: partenza. Al via devi essere dietro la linea, fra la barca giuria e la boa arancione, e tagliarla entro un minuto. È un esercizio: non si salva niente.",
        fatto: (R, me) => me.leg >= 1,
        fallito: (R, me, es) => { if (R.t >= 0 && es.ocs0 === undefined) es.ocs0 = me.ocs;
          return es.ocs0 ? "Al via eri oltre la linea: partenza anticipata." : R.t > 60 && me.leg === 0 ? "È passato un minuto dal via e non hai ancora tagliato la linea." : ""; } },
      text: ["Ora una partenza vera, da solo, con la sequenza di cinque minuti. Apri l'esercizio, guarda le bandiere, fatti trovare dietro la linea al via e tagliala entro un minuto.",
             "L'esercizio non salva niente. Raggiunto l'obiettivo, torni qui."],
      done: "Partenza regolare: al via eri dietro la linea e l'hai tagliata subito dopo." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Avviso a cinque minuti (bandiera di classe), preparatorio a quattro (P), un minuto (giù la P), partenza (giù la classe). Contano le bandiere (regola 26)."] }
  ];
  const LD6 = [
    { title: "Il richiamo individuale", ...PAUSE, zoom: 2,
      text: ["Se al segnale di partenza una parte dello scafo è già oltre la linea, la barca è partita in anticipo. La giuria alza subito la <em>X</em>, bianca con la croce blu, con un suono: è il richiamo individuale (regola 29.1).",
             "Chi è in anticipo deve tornare con lo scafo tutto dietro la linea e partire di nuovo. La X resta su finché tutte le barche in anticipo sono tornate, ma non più di quattro minuti dal via."] },
    { title: "Tornare lasciando strada", ...PAUSE, zoom: 2,
      text: ["Mentre torni verso la linea dopo il via, lasci strada a tutte le barche che non lo stanno facendo, finché lo scafo non è tutto dietro la linea (regola 21.1).",
             "Nel gioco questa regola vale nella regata con i giri di penalità. Il gioco considera tornata la barca quando il suo centro è dietro la linea, non ogni punto dello scafo: è una semplificazione."] },
    { title: "Parti in anticipo e torna", ...PAUSE, zoom: 2,
      esercizio: { regata: 3, cd: 60, avversari: "nessuno",
        obiettivo: "Al via sii oltre la linea, poi torna dietro e riparti",
        brief: "Esercizio della lezione 17. Una partenza da solo con un minuto di preparazione: c'è solo la bandiera di classe, che si ammaina al via. Questa volta, apposta, al via fatti trovare oltre la linea: sale la X. Poi torna dietro la linea e riparti tagliandola fra la barca giuria e la boa arancione. È un esercizio: non si salva niente.",
        fatto: (R, me, es) => !!es.ocs0 && me.leg >= 1,
        fallito: (R, me, es) => { if (R.t >= 0 && es.ocs0 === undefined) es.ocs0 = me.ocs;
          return es.ocs0 === false ? "Al via eri dietro la linea: qui devi partire in anticipo apposta." : R.t > 180 && me.leg === 0 ? "Sono passati tre minuti dal via e non sei ancora ripartito." : ""; } },
      text: ["Ora provala apposta. Apri l'esercizio: al via fatti trovare oltre la linea, guarda salire la X, torna dietro la linea e riparti.",
             "L'esercizio non salva niente. Raggiunto l'obiettivo, torni qui."],
      done: "Sei tornato dietro la linea e sei ripartito: ora la tua partenza vale." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Oltre la linea al via: sale la X (regola 29.1). Si torna con lo scafo tutto dietro la linea, lasciando strada a chi non lo fa (regola 21.1), e si riparte."] }
  ];
  const LD7 = [
    { title: "Non toccare le boe", ...PAUSE, zoom: 2,
      text: ["In regata non si toccano le boe (regola 31): prima della partenza quelle della linea di partenza; dopo, la boa da cui parte il lato che stai facendo e quella verso cui vai; dopo l'arrivo, quelle dell'arrivo.",
             "Chi tocca una boa può scontarla con un giro di penalità (regola 44.1)."] },
    { title: "I giri di penalità", ...PAUSE, zoom: 2,
      text: ["Un contatto con colpa con un'altra barca costa due giri, una boa toccata un giro (regola 44.1). Ci si allontana dalle altre barche appena possibile e si fanno subito i giri, tutti nello stesso verso; ogni giro ha una virata e una strambata (regola 44.2).",
             "Mentre sconti la penalità lasci strada a chi non lo fa (regola 21.2).",
             "Nel gioco un giro vale se in venti secondi la prua fa un giro intero nello stesso verso, con una virata e una strambata. I giri non fatti, all'arrivo, costano quindici secondi l'uno: nel regolamento non c'è, è una scelta del gioco."] },
    { title: "Tocca la boa e fai il giro", ...PAUSE, zoom: 2,
      esercizio: { regata: 3, boa: [-30, 10, 50], avversari: "nessuno", // di bolina mure a sinistra, boa a 32 m, 22° a destra della prua: orzando (la barca sbandata orza) la si passa a 12 m sopravento
        obiettivo: "Tocca la boa gialla, poi fai un giro di penalità",
        brief: "Esercizio della lezione 20. A regata già partita sei di bolina, da solo, e la boa gialla è davanti a te, un po' a destra. Poggia e toccala, apposta. Poi allontanati un poco e fai un giro di penalità: una virata e una strambata, girando sempre nello stesso verso. È un esercizio: non si salva niente.",
        fatto: R => R.need >= 1 && R.done >= R.need,
        fallito: R => R.t > 180 ? (R.need ? "Sono passati tre minuti e il giro non è ancora fatto." : "Sono passati tre minuti e non hai toccato la boa.") : "" },
      text: ["Ora provalo. Apri l'esercizio: sei di bolina e la boa gialla è davanti a te, un po' a destra. Toccala apposta, allontanati un poco e fai un giro, con una virata e una strambata.",
             "L'esercizio non salva niente. Raggiunto l'obiettivo, torni qui."],
      done: "Giro fatto: la penalità per la boa toccata è scontata." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Non si toccano le boe (regola 31). Boa toccata: un giro; contatto con colpa: due giri; subito, nello stesso verso, ognuno con una virata e una strambata (regole 44.1 e 44.2)."] }
  ];

  // ---- gruppo C, le partenze (1.2.2, meccanismo B; docs/PROPOSTA-LEZIONI-SCUOLA.md §4, docs/PROPOSTA-ESERCIZI-REGOLAMENTO-E-PARTENZE.md) ----
  // Fonti: F25 (aspettare quasi fermi vicino alla linea con la vela che sbatte, poi accelerare per essere a piena velocità allo zero), F27 (l'attesa appena sotto la bolina;
  //   la parte sull'accelerazione non è letta: il testo non la usa), F15 26 e 29.1 (già nelle D5-D6). Ale, 17 ottobre 2026: in questa classe di barche si parte da fermi,
  //   quasi fermi e poi accelerando, non lanciati da lontano. Ipotesi nostre: C1 entro 5 s dal via a più di 3,5 nodi (soglie della proposta, scritte prima);
  //   C2 ferma 12 m dietro il centro della linea a 60° dal vento, 10 s di preparazione, «ferma» = sotto 1 nodo al via, limite di tempo ES_C2 (scelto col pilota sui semi 1-20).
  const ES_C2 = 25; // s dal via per tagliare la linea partendo da fermi; ipotesi nostra, regola scritta prima: il massimo del pilota sui semi 1-20 (16,0 s), arrotondato ai 5 s superiori, più 5 s
  const nodi = v => v.toFixed(1).replace(".", ",");
  function esTaglio(R, me, es){ // al via: anticipo e velocità; al taglio della linea: quando e a che velocità
    if (R.t >= 0 && es.ocs0 === undefined){ es.ocs0 = me.ocs; es.v0 = me.S.u * KN; }
    if (me.leg >= 1 && !es.taglio) es.taglio = { t: R.t, v: me.S.u * KN };
  }
  const esMisura = es => es.taglio ? "Linea tagliata " + nodi(es.taglio.t) + " s dopo il via, a " + nodi(es.taglio.v) + " nodi." : "";
  const LC1 = [
    { title: "Aspettare vicino alla linea", ...PAUSE, zoom: 2,
      text: ["In una partenza vince chi taglia la linea subito dopo il via e già veloce. Con barche piccole e leggere come questa non si arriva lanciati da lontano: si aspetta <em>vicino alla linea</em>, una o due lunghezze dietro, quasi fermi con la vela lascata che sbatte.",
             "Si aspetta con la prua appena sotto la bolina: da lì basta cazzare per partire, senza dover prima poggiare.",
             "Da fermi la barca non va alla linea: si può aspettare il momento giusto."] },
    { title: "Cazzare al momento giusto", ...PAUSE, zoom: 2,
      text: ["Negli ultimi secondi si cazza e la barca accelera. Se cazzi troppo presto arrivi alla linea prima del via e sei in anticipo: sale la X e devi tornare (regola 29.1). Se cazzi troppo tardi, al via sei ancora lento e le altre ti passano davanti.",
             "Il momento giusto dipende da quanto sei lontano dalla linea e da quanto vento c'è: si impara provando, guardando il conto alla rovescia."] },
    { title: "Parti veloce", ...PAUSE, zoom: 2,
      esercizio: { regata: 0, cd: 60, avversari: "nessuno",
        obiettivo: "Taglia la linea entro 5 s dal via, a più di 3,5 nodi",
        brief: "Esercizio della lezione 18. Una partenza da solo con un minuto di preparazione, vento di 10 nodi. Avvicinati alla linea, fra la barca giuria e la boa arancione, aspetta lì quasi fermo con la vela lascata e cazza negli ultimi secondi: devi tagliare la linea entro cinque secondi dal via, a più di 3,5 nodi, senza anticipo. È un esercizio: non si salva niente.",
        fatto: (R, me, es) => !!es.taglio && !es.ocs0 && es.taglio.t <= 5 && es.taglio.v > 3.5,
        fallito: (R, me, es) => { esTaglio(R, me, es);
          if (es.ocs0) return "Al via eri oltre la linea: partenza anticipata.";
          if (es.taglio) return es.taglio.t > 5 ? "Hai tagliato la linea " + nodi(es.taglio.t) + " s dopo il via: tardi." : es.taglio.v <= 3.5 ? "Hai tagliato la linea a " + nodi(es.taglio.v) + " nodi: piano." : "";
          return R.t > 5 ? "Sono passati cinque secondi dal via e non hai tagliato la linea." : ""; },
        misura: esMisura },
      text: ["Ora una partenza da solo, con un minuto di preparazione. Apri l'esercizio, aspetta vicino alla linea quasi fermo e cazza negli ultimi secondi: tagliala entro cinque secondi dal via, a più di 3,5 nodi.",
             "L'esercizio non salva niente. Raggiunto l'obiettivo, torni qui."],
      done: "Partenza buona: al via eri vicino alla linea e già veloce." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Aspetta quasi fermo una o due lunghezze dietro la linea, con la prua appena sotto la bolina. Cazza negli ultimi secondi, per tagliare la linea subito dopo il via e già veloce, senza anticipo."] }
  ];
  const LC2 = [
    { title: "Partire da fermi", ...PAUSE, zoom: 2,
      text: ["Una barca ferma, con la vela che sbatte, non riparte subito: cazzata la vela, servono alcuni secondi e qualche metro prima che arrivi alla sua velocità.",
             "Per questo, in una partenza, chi è fermo al via perde sempre qualcosa su chi ha cazzato prima. Ma capita: se sei chiuso fra le altre barche, o se hai sbagliato i tempi, devi saper partire da fermo nel modo più rapido."] },
    { title: "Come si riparte", ...PAUSE, zoom: 2,
      text: ["Da fermo, con la prua appena sotto la bolina, cazza la vela finché i filetti sono dritti e tieni la barca piatta. Quando la barca ha preso velocità, porta la prua in bolina e vai alla linea.",
             "Se la prua è troppo vicina al vento, la vela non porta e la barca non parte: poggia un poco prima di cazzare."] },
    { title: "Parti da fermo", ...PAUSE, zoom: 2,
      esercizio: { regata: 0, cd: 10, linea: [0, 12, 60, 0], avversari: "nessuno",
        obiettivo: "Fermo fino al via, poi taglia la linea entro " + ES_C2 + " s",
        brief: "Esercizio della lezione 19. Sei fermo dodici metri dietro la linea, con la vela tutta lascata, e mancano dieci secondi al via. Resta fermo fino al via: non cazzare prima. Al via cazza e parti, e taglia la linea fra la barca giuria e la boa arancione entro " + ES_C2 + " secondi. Alla fine vedi quanti secondi ti sono serviti. È un esercizio: non si salva niente.",
        fatto: (R, me, es) => !!es.taglio && !es.ocs0 && es.v0 <= 1,
        fallito: (R, me, es) => { esTaglio(R, me, es);
          if (es.v0 > 1) return "Al via andavi già a " + nodi(es.v0) + " nodi: qui si parte da fermi.";
          if (es.ocs0) return "Al via eri oltre la linea: partenza anticipata.";
          return R.t > ES_C2 && !es.taglio ? "Sono passati " + ES_C2 + " secondi dal via e non hai tagliato la linea." : ""; },
        misura: esMisura },
      text: ["Ora prova. Apri l'esercizio: sei fermo dietro la linea con la vela lascata. Resta fermo fino al via, poi cazza, prendi velocità e taglia la linea entro " + ES_C2 + " secondi.",
             "L'esercizio non salva niente. Raggiunto l'obiettivo, torni qui."],
      done: "Partito da fermo: hai visto quanti secondi servono per prendere velocità." },
    { title: "Riepilogo", ...PAUSE, zoom: 2, final: true,
      text: ["Da fermo servono alcuni secondi e qualche metro per prendere velocità. Prua appena sotto la bolina, cazza, barca piatta; quando la barca va, porta la prua in bolina."] }
  ];

  const LESSONS = [
    { name: "Lezione 1", title: "La barca e il vento", steps: L1, desc: "Le parti della barca, il vento, orzare e poggiare, cazzare e lascare." },
    { name: "Lezione 2", title: "Il timone", steps: L2, desc: "La barra si sposta dalla parte opposta: barra sottovento orza, sopravento poggia." },
    { name: "Lezione 4", title: "Andature e mure", steps: L3, desc: "Bolina, traverso, lasco, poppa; le mure; regolare la vela leggendo i filetti." },
    { name: "Lezione 5", title: "Vento reale e apparente", steps: L4, desc: "Perché andando veloci il vento sembra arrivare più da prua." },
    { name: "Lezione 6", title: "Virata e strambata", steps: L5, desc: "Cambiare mure, risalire il vento a zig-zag, strambare senza rischi." },
    { name: "Lezione 8", title: "Raffiche e scuffia", steps: L6, desc: "Riconoscere le raffiche, tenere la barca piatta, scuffiare e raddrizzare." },
    // dalla 1.1.4 le lezioni nuove della scuola, nascoste nel menu (nascosta: true) finché non arriva il menu nuovo; quiz ed esame stanno nella lezione
    { name: "Lezione 3", title: "Il timone che stalla", steps: LB1, gruppo: "B", desc: "La pala è un'ala e può stallare; la barra fino a 35° o, con Maiusc, a 45°.",
      quiz: [["Che cosa succede alla pala del timone oltre un certo angolo?", "Va in stallo: la spinta non cresce più e frena di più", ["Si rompe", "Gira la barca più in fretta", "Non succede niente: più angolo, più spinta"], "Come un'ala, oltre un certo angolo l'acqua si stacca dalla pala: la spinta smette di crescere e la resistenza aumenta."],
             ["Quando la barca sta già girando, l'angolo che la pala sente è…", "più piccolo di quello della barra", ["più grande di quello della barra", "uguale a quello della barra", "sempre zero"], "Girando, l'acqua arriva sulla pala un po' di traverso: l'angolo sentito è minore di quello della barra."],
             ["In questo gioco, fino a che angolo porta la barra la sola freccia?", "35°", ["45°", "30°", "Fino in fondo"], "La sola freccia si ferma a 35°, un angolo sicuro: è una regola del gioco. Con Maiusc si arriva a 45°."],
             ["Quando conviene la barra a 45° (Maiusc)?", "Per girare stretto: vicino a una boa, nei giri di penalità, con la barca lenta", ["Sempre, perché la barca va più veloce", "Mai: fa scuffiare", "Solo con il vento leggero"], "Con 45° la barca gira più stretta; serve quando bisogna girare in poco spazio o la barca è lenta. Va accompagnata e centrata per tempo."]],
      esame: [["35° e 45°", "Devi girare attorno a una boa in poco spazio. Che cosa usi?", "Maiusc e la freccia: la barra arriva a 45°", ["La sola freccia: si ferma a 35°", "Lasco tutta la vela", "Spingo il boma con Z"], "Con Maiusc la barra arriva a 45° e la barca gira più stretta."],
              ["La pala è un'ala", "Perché una pala girata troppo frena la barca?", "Va in stallo: l'acqua si stacca e la resistenza cresce", ["Perché tocca il fondo", "Perché fa sbandare la barca", "Perché sposta il vento"], "Oltre un certo angolo la pala stalla: la spinta non cresce più, la resistenza sì."],
              ["Una virata con la barra in fondo", "Viri con la barra a 45°. Quando centri la barra?", "Un po' prima che con 35°, perché la prua gira più in fretta", ["Quando la barca si ferma", "Mai: la barra torna da sola", "Dopo che la prua ha superato la bolina di 30°"], "Con più barra la prua gira più in fretta: centrando tardi va oltre la bolina."],
              ["La pala è un'ala", "Su una deriva da regata, misurato in vasca e calcolato al computer, la pala stalla fra circa…", "15° e 30°", ["2° e 5°", "60° e 90°", "Non stalla mai"], "Le misure in vasca di un modellino danno circa 15°, il calcolo a grandezza vera circa 30°."]] },
    { name: "Lezione 7", title: "Spingere il boma", steps: LB2, gruppo: "B", desc: "Fermo nell'angolo morto: Z spinge il boma, la barca arretra e gira; poi si riparte.",
      quiz: [["Sei fermo con la prua nel vento. Che cosa fai con il boma e la barra?", "Spingo il boma fuori e metto la barra dalla stessa parte", ["Cazzo tutta la vela", "Metto la barra dalla parte opposta al boma", "Aspetto senza toccare niente"], "Boma e barra dalla stessa parte: la vela prende il vento al contrario, la barca arretra e la prua gira verso il boma."],
             ["Con il boma spinto fuori, verso dove gira la prua?", "Verso il boma, cioè lontano dal vento", ["Verso il vento", "Non gira: la barca va solo all'indietro", "Dalla parte opposta al boma"], "La vela a collo spinge la barca all'indietro e fa girare la prua verso il boma."],
             ["Quando molli il boma e riparti?", "Quando sei al traverso: molli, centri la barra e cazzi", ["Subito, appena la barca si muove", "Quando la prua è tornata nel vento", "Mai: si va all'indietro fino alla boa"], "Al traverso la vela può spingere in avanti: si molla il boma, si centra la barra e si cazza."],
             ["In regata, chi va all'indietro spingendo la vela…", "deve tenersi lontano da chi non lo fa (regola 21.3)", ["ha sempre la precedenza", "deve fare due giri di penalità", "può farlo solo dopo la partenza"], "Regola 21.3: chi arretra spingendo una vela si tiene lontano dagli altri. In questo gioco la regola non è applicata."]],
      esame: [["Fuori dall'angolo morto", "Per uscire dall'angolo morto con il boma spinto, la barra va…", "dalla stessa parte del boma", ["dalla parte opposta al boma", "al centro", "non importa"], "Boma e barra dalla stessa parte: la prua gira verso il boma, lontano dal vento."],
              ["Fuori dall'angolo morto", "Con il boma spinto fuori, la barca…", "va all'indietro e la prua gira verso il boma", ["va avanti più veloce", "scuffia", "resta ferma"], "La vela prende il vento al contrario: la barca arretra e gira."],
              ["Spingi il boma e riparti", "Sei al traverso dopo aver spinto il boma. Che cosa fai?", "Mollo il boma, centro la barra e cazzo", ["Continuo a spingere il boma", "Viro subito", "Lasco tutta la vela"], "Al traverso la vela torna a spingere in avanti: si molla, si centra e si cazza."],
              ["All'indietro, apposta", "A che cosa serve, oltre a uscire dall'angolo morto, spingere il boma?", "A frenare o arretrare, per esempio prima della partenza", ["A sbandare di meno", "A girare attorno alla boa", "A prendere le raffiche"], "Spingendo il boma si può frenare o arretrare apposta, per esempio per uscire da un brutto posto sulla linea."]] },
    { name: "Lezione 10", title: "La barca che orza sbandando", steps: LB3, gruppo: "B", desc: "Sbandando la prua sale verso il vento; nella raffica si lasca e si corregge con poca barra.",
      quiz: [["Perché una barca sbandata orza?", "La vela inclinata spinge fuori, dalla parte del boma, e la prua gira verso il vento", ["Perché la deriva esce dall'acqua", "Perché il vento gira", "Non orza: poggia"], "Sbandando, la spinta della vela arriva fuori dalla barca, sottovento: la prua gira verso il vento."],
             ["In una raffica la barca sbanda e la prua sale. Che cosa fai per prima cosa?", "Raddrizzo la barca: mi sporgo e lasco un poco", ["Metto tutta la barra sopravento", "Cazzo tutta la vela", "Non faccio niente"], "Prima si raddrizza, lascando e sporgendosi: poi basta poca barra."],
             ["Perché poggiare con la barca molto sbandata è un rischio?", "Carica molto la pala e la barra", ["Fa scuffiare sopravento", "Fa virare la barca", "Non è un rischio"], "Sbandata, la barca orza forte: per poggiare serve molta forza sul timone, ed è così che pala e barra si rompono."],
             ["Barca dritta, di bolina, vela regolata: dove sta la barra?", "Quasi al centro", ["Tutta sopravento", "Tutta sottovento", "Dipende dal vento"], "Con la barca dritta il centro velico e lo scafo quasi si equilibrano: la barra sta quasi al centro."]],
      esame: [["Perché la barca orza", "Più la barca sbanda, più…", "orza", ["poggia", "accelera", "va dritta"], "Sbandando, la spinta della vela va sottovento e fa girare la prua verso il vento."],
              ["Nella raffica", "In raffica, con la barra sopravento…", "si poggia, ma se la barca resta sbandata serve molta barra", ["si orza", "la barca si raddrizza da sola", "si vira"], "La barra sopravento fa poggiare; con la barca sbandata il timone lavora molto."],
              ["La rotta nella raffica", "Sei al traverso, arriva una raffica e la prua sale. Che cosa fai?", "Lasco un poco e correggo con piccoli colpi di barra", ["Cazzo tutto", "Orzo fino alla bolina", "Spingo il boma con Z"], "Lascando la barca si raddrizza e orza meno; poi basta poca barra."],
              ["Nella raffica", "Passata la raffica, che cosa fai con la scotta?", "La cazzo di nuovo", ["La lascio tutta lasca", "La lasco ancora", "Niente: si regola da sola"], "Passata la raffica la vela va regolata di nuovo: si cazza."]] },
    { name: "Lezione 9", title: "La raddrizzata lunga", steps: LB4, gruppo: "B", desc: "Dopo la scuffia: spalle al vento, A per dieci secondi, poi si cazza e si riparte al traverso.",
      quiz: [["Mentre raddrizzi la barca, da che parte stai rispetto al vento?", "Con le spalle al vento, e l'albero resta sottovento", ["Con la faccia al vento, l'albero sopravento", "Non conta", "Sotto la vela"], "Con le spalle al vento la vela sale e sbatte libera; con l'albero sopravento il vento entra sotto la vela e la barca si rovescia di nuovo."],
             ["In questo gioco, quanto dura la raddrizzata col tasto A?", "Dieci secondi", ["Un secondo", "Tre secondi", "Un minuto"], "Il tasto A raddrizza la barca in dieci secondi."],
             ["Appena raddrizzata, nel gioco, come si trova la barca?", "Ferma, di traverso, con la vela che sbatte", ["Già in bolina, a vela cazzata", "In poppa, veloce", "Con la prua al vento e la barra all'orza"], "Torna dritta di traverso, ferma, con la vela tutta lascata."],
             ["La barca è appena tornata dritta. Che cosa fai per ripartire?", "Cazzo finché i filetti sono dritti", ["Lasco ancora", "Premo di nuovo A", "Spingo il boma con Z"], "Al traverso basta cazzare finché i filetti sono dritti: la barca riprende a navigare."]],
      esame: [["Spalle al vento", "Perché, raddrizzando, l'albero deve restare sottovento?", "Così la vela sbatte libera e il vento non ci entra sotto", ["Così la barca va più veloce", "Così la deriva non si rompe", "Non deve: va sopravento"], "Con l'albero sopravento il vento entra sotto la vela e la barca si rovescia di nuovo."],
              ["Spalle al vento", "Un allenatore dice che, fatta bene, dalla scuffia alla barca che naviga passano circa…", "15-20 secondi", ["2 secondi", "5 minuti", "Un'ora"], "Fatta bene, la manovra dura 15-20 secondi."],
              ["Raddrizza e riparti", "Hai raddrizzato: la barca è ferma di traverso e la vela sbatte. Che cosa fai?", "Cazzo e riparto", ["Premo di nuovo A", "Viro subito", "Lasco tutto"], "Al traverso, cazzando finché i filetti sono dritti, la barca riparte."],
              ["Raddrizza e riparti", "In questo gioco, per raddrizzare la barca scuffiata…", "premo A e aspetto dieci secondi", ["premo Z", "cazzo tutta la vela", "aspetto senza toccare niente"], "Il tasto A raddrizza la barca in dieci secondi."]] },
    { name: "Lezione 11", title: "I salti di vento", steps: LB5, gruppo: "B", desc: "Il vento oscilla: con la bussola si vede quando si è scarsi, e di bolina si vira sugli scarsi.",
      quiz: [["Di bolina il vento gira verso la tua prua e devi poggiare per tenere l'andatura. Come sei?", "Scarso", ["Buono", "In poppa", "Nell'angolo morto"], "Vento che gira verso la prua: per restare di bolina si poggia, si è scarsi."],
             ["Il vento oscilla avanti e indietro. Di bolina quando conviene virare?", "Quando sei scarso", ["Quando sei buono", "Ogni dieci secondi", "Mai"], "Sulle altre mure lo stesso salto è buono: si vira sugli scarsi e si resta sulle mure buone."],
             ["Con quale strumento ti accorgi di essere scarso?", "La bussola: la prua confrontata con la sua media", ["Il contachilometri", "La scotta", "Il filetto sopravento"], "Si guarda fra quali prue si oscilla su una mura e se ne prende la media: lontani dalla media verso il basso, si è scarsi."],
             ["Il vento gira sempre dalla stessa parte. Che cosa fai?", "Non viro sugli scarsi: vado verso il salto", ["Viro a ogni scarso", "Vado dalla parte opposta al salto", "Mi fermo ad aspettare"], "Se il vento gira sempre dalla stessa parte non torna indietro: si va verso il salto."]],
      esame: [["Il vento gira", "Lo stesso salto di vento, sulle altre mure, è…", "il contrario: scarso su una mura, buono sull'altra", ["uguale su tutte e due le mure", "sempre scarso", "sempre buono"], "Un salto che è scarso su una mura è buono sull'altra."],
              ["Vira sugli scarsi", "Di bolina la prua oscilla fra 240° e 270° su una mura. Qual è la prua media?", "255°", ["240°", "270°", "300°"], "La media fra la prua più alta e la più bassa: 255°."],
              ["Vira sullo scarso", "Il vento oscilla e sei scarso di una decina di gradi. Che cosa fai?", "Viro", ["Orzo fino all'angolo morto", "Lasco tutta la vela", "Continuo fino alla boa"], "Con il vento che oscilla si vira sugli scarsi: sulle altre mure il salto è buono."],
              ["Vira sugli scarsi", "Sei vicino alla boa e resta un solo salto. Come lo giochi?", "Come se il vento non dovesse più tornare", ["Viro a ogni scarso", "Mi fermo", "Vado in poppa"], "Quando resta un salto solo, lo si gioca come un salto persistente."]] },
    { name: "Lezione 12", title: "Mure opposte", steps: LD1, gruppo: "D", desc: "Mure diverse: la barca mure a sinistra lascia strada a quella mure a dritta (regola 10).",
      quiz: [["Due barche con mure diverse si incrociano. Chi lascia strada?", "La barca mure a sinistra", ["La barca mure a dritta", "Quella più veloce", "Quella più piccola"], "Regola 10: con mure diverse lascia strada la barca mure a sinistra."], ["Che cosa vuol dire lasciare strada?", "Che l'altra può tenere la sua rotta senza manovrare per evitarti", ["Che ti fermi del tutto", "Che viri subito", "Che l'altra deve poggiare"], "Ti tieni lontano quando l'altra può tenere la sua rotta senza manovre per evitarti."], ["Il semaforo sul tuo scafo è verde. Che cosa vuol dire?", "Hai la precedenza, ma non il permesso di urtare", ["Puoi urtare l'altra barca", "Devi lasciare strada", "La regata è finita"], "Verde: hai la precedenza. Il contatto va evitato lo stesso."], ["Nelle regate di questo gioco, chi non lascia strada e provoca un contatto…", "prende una penalità", ["vince la regata", "non ha nessuna conseguenza", "deve sempre ritirarsi"], "Chi non lascia strada e provoca un contatto prende una penalità: 15 s, due giri o un punto, a seconda della regata."]],
      esame: [["Chi lascia strada", "Sei mure a sinistra e incroci una barca mure a dritta. Che cosa fai?", "Le lascio strada: le passo dietro o viro per tempo", ["Tiro dritto: ho la precedenza", "Mi fermo nell'angolo morto", "Le passo davanti di poco"], "Mure a sinistra lascia strada a mure a dritta: si passa dietro o si vira per tempo."], ["Chi lascia strada", "Quale regola dice che mure a sinistra lascia strada a mure a dritta?", "La regola 10", ["La regola 31", "La regola 44", "La regola 26"], "È la regola 10, la prima della Sezione A."], ["Penalità e semaforo", "Il semaforo sul tuo scafo è rosso. Che cosa vuol dire?", "Devi lasciare strada", ["Hai la precedenza", "Sei partito in anticipo", "Hai toccato una boa"], "Rosso: devi lasciare strada alla barca vicina."], ["Penalità e semaforo", "Nella regata con i giri di penalità, un contatto con colpa costa…", "due giri", ["15 secondi", "un giro", "niente"], "Nella regata con i giri di penalità chi ha colpa fa due giri."]] },
    { name: "Lezione 13", title: "Stesse mure", steps: LD2, gruppo: "D", desc: "Stesse mure: affiancate cede la sopravento, se no cede quella dietro (regole 11 e 12).",
      quiz: [["Stesse mure, barche affiancate. Chi lascia strada?", "La barca sopravento", ["La barca sottovento", "Quella davanti", "Quella mure a dritta"], "Regola 11: stesse mure e sovrapposte, la sopravento lascia strada."], ["Stesse mure, una barca è tutta dietro l'altra. Chi lascia strada?", "Quella dietro", ["Quella davanti", "Quella sottovento", "Nessuna delle due"], "Regola 12: la barca libera dietro lascia strada a quella libera avanti."], ["Quando due barche sono sovrapposte?", "Quando nessuna sta tutta dietro la linea al traverso della poppa dell'altra", ["Quando si toccano", "Quando hanno mure diverse", "Quando sono a meno di cento metri"], "Sovrapposte: nessuna delle due è libera dietro all'altra."], ["Quale barca è sopravento?", "Quella più vicina al vento", ["Quella più lontana dal vento", "Quella più veloce", "Quella davanti"], "Sopravento è la barca dalla parte da cui arriva il vento."]],
      esame: [["Affiancate", "Con le stesse mure e sovrapposte, chi lascia strada?", "La sopravento", ["La sottovento", "Quella mure a dritta", "Quella più lenta"], "Regola 11: la sopravento lascia strada."], ["Libera dietro", "Con le stesse mure e non sovrapposte, chi lascia strada?", "Quella libera dietro", ["Quella libera avanti", "Quella sottovento", "Nessuna"], "Regola 12: la libera dietro lascia strada."], ["Libera dietro", "Sei libera dietro un'altra barca con le stesse mure e vai più veloce. Che cosa fai?", "Passo, ma senza costringerla a manovrare", ["Ho la precedenza: tiro dritto", "La urto per passare", "Viro subito"], "La libera dietro lascia strada: può passare, ma senza che l'altra debba manovrare."], ["Affiancate", "Sei sottovento e sovrapposta a una barca con le tue stesse mure. Chi ha la precedenza?", "Tu", ["L'altra", "Nessuna", "Chi va più veloce"], "La sopravento lascia strada alla sottovento."]] },
    { name: "Lezione 14", title: "Chi vira cede", steps: LD3, gruppo: "D", desc: "Dal vento alla bolina chi vira lascia strada a tutte (regola 13).",
      quiz: [["Da quando a quando chi vira lascia strada alle altre?", "Da quando la prua passa il vento finché non è di bolina sulle nuove mure", ["Per tutta la regata", "Solo vicino a una boa", "Dal segnale di partenza all'arrivo"], "Regola 13: dal vento alla bolina sulle nuove mure."], ["Viri e finisci mure a dritta vicino a una barca mure a sinistra. Hai già la precedenza?", "No: finché non sei di bolina lasci strada tu", ["Sì, subito", "Sì, se sei più veloce", "Sì, se l'altra è dietro"], "Finché la virata non è finita, di bolina, chi vira lascia strada."], ["Mentre una barca vira, valgono per lei le regole 10, 11 e 12?", "No", ["Sì", "Solo la 10", "Solo la 12"], "Durante la virata vale la 13, non la 10, la 11 e la 12."], ["Due barche virano insieme. Chi lascia strada?", "Quella alla sinistra dell'altra, o quella dietro", ["Quella alla destra", "Quella più veloce", "Nessuna"], "Se virano tutte e due, cede quella alla sinistra dell'altra o quella dietro."]],
      esame: [["Durante la virata", "Quale regola dice che chi vira lascia strada?", "La regola 13", ["La regola 10", "La regola 31", "La regola 29"], "È la regola 13."], ["Durante la virata", "Una barca vicina va mure a dritta. Conviene virarle proprio davanti?", "No: mentre viri lasci strada tu", ["Sì, così prendi la precedenza", "Sì, se sei più veloce", "Non importa"], "Durante la virata si lascia strada a tutte: virare davanti a una barca vicina è un errore."], ["Durante la virata", "Quando finisce, per la regola 13, la virata?", "Quando la barca è di bolina sulle nuove mure", ["Quando la prua passa il vento", "Quando la barca si ferma", "Dopo dieci secondi"], "Fino alla bolina sulle nuove mure."], ["Durante la virata", "Due barche virano insieme, una dietro l'altra. Chi lascia strada?", "Quella dietro", ["Quella davanti", "Nessuna", "Quella più grande"], "Se virano insieme, cede quella alla sinistra dell'altra o quella dietro."]] },
    { name: "Lezione 15", title: "Evitare il contatto", steps: LD4, gruppo: "D", desc: "Anche chi ha la precedenza evita il contatto; danni e spazio (regole 14, 15, 16).",
      quiz: [["La barca con la precedenza deve evitare il contatto?", "Sì, se è ragionevolmente possibile", ["No, mai", "Solo se è mure a sinistra", "Solo alla partenza"], "Regola 14: tutte le barche evitano il contatto, se è ragionevolmente possibile."], ["Quando chi ha la precedenza deve cominciare a manovrare per evitare il contatto?", "Quando è chiaro che l'altra non lascia strada", ["Appena vede un'altra barca", "Mai", "Dopo il contatto"], "Chi ha la precedenza può aspettare finché è chiaro che l'altra non si scansa."], ["Un contatto senza danni né feriti: chi aveva la precedenza è penalizzato?", "No", ["Sì, sempre", "Sì, con due giri", "Solo nel torneo"], "Regola 43.1(c): senza danni o lesioni chi aveva la precedenza è esonerato."], ["Chi ha la precedenza cambia rotta. Che cosa deve fare?", "Lasciare all'altra lo spazio per tenersi lontana", ["Niente: ha la precedenza", "Virare subito", "Fermarsi"], "Regola 16: chi ha la precedenza e cambia rotta dà all'altra lo spazio per scansarsi."]],
      esame: [["Evitare il contatto", "Quale regola chiede a tutte le barche di evitare il contatto?", "La regola 14", ["La regola 10", "La regola 26", "La regola 44"], "È la regola 14."], ["Evitare il contatto", "In questo gioco, dopo un contatto, chi ha torto?", "Sempre chi doveva lasciare strada", ["Sempre tutte e due", "Chi andava più veloce", "Nessuna"], "Il gioco non ha danni: chi doveva lasciare strada ha sempre torto."], ["Non togliere spazio", "Passi avanti a un'altra barca e così ottieni la precedenza. Che cosa devi fare all'inizio?", "Darle lo spazio per lasciarti strada", ["Niente: hai la precedenza", "Virare", "Fermarti"], "Regola 15: chi ottiene la precedenza dà all'inizio all'altra lo spazio per scansarsi."], ["Non togliere spazio", "Il gioco controlla le regole 15 e 16?", "No: valgono in regata, ma il gioco non le controlla", ["Sì, con il semaforo", "Sì, con 15 secondi", "Solo nel torneo"], "Il gioco controlla 10, 11, 12 e 13; la 14, la 15 e la 16 no."]] },
    { name: "Lezione 16", title: "I segnali di partenza", steps: LD5, gruppo: "D", desc: "Le bandiere della partenza: classe, P, un minuto, via (regola 26). Esercizio in regata.",
      quiz: [["Quale bandiera sale cinque minuti prima della partenza?", "La bandiera di classe", ["La P", "La X", "La bandiera blu"], "È il segnale di avviso: la bandiera di classe, cinque minuti al via (regola 26)."],
             ["Che cosa vuol dire la P che si ammaina?", "Manca un minuto alla partenza", ["La partenza è rinviata", "Qualcuno è partito in anticipo", "La regata è finita"], "Il preparatorio (P) sale a quattro minuti e si ammaina a un minuto dal via."],
             ["Al segnale di partenza, dove devi essere?", "Dietro la linea, dalla parte da cui si parte", ["Già oltre la linea", "Vicino alla boa di bolina", "Ovunque: non conta"], "Al via lo scafo deve essere tutto dietro la linea; poi la si taglia."],
             ["Il suono del segnale non si sente. Che cosa conta?", "La bandiera", ["Il suono: senza suono non si parte", "L'orologio di bordo", "La prima barca che parte"], "Regola 26: i tempi si prendono dalle bandiere; un suono che manca non conta."]],
      esame: [["La sequenza", "Quando sale la bandiera P?", "Quattro minuti prima della partenza", ["Cinque minuti prima", "Un minuto prima", "Alla partenza"], "La P è il preparatorio: quattro minuti prima del via."],
              ["La sequenza", "Che cosa segna la partenza?", "La bandiera di classe che si ammaina", ["La P che sale", "La X che sale", "La bandiera blu che si ammaina"], "Al via si ammaina la bandiera di classe."],
              ["La linea", "In questo gioco, fra quali punti si taglia la linea di partenza?", "Fra la barca giuria e la boa arancione", ["Fra due boe gialle", "Fra la boa di bolina e la giuria", "Dove si vuole"], "La linea va dalla barca giuria alla boa arancione."],
              ["Parti al segnale", "Mancano trenta secondi al via. Dove conviene essere?", "Dietro la linea e vicino, pronto a partire lanciato", ["Lontano dalla linea, fermo", "Già oltre la linea", "Vicino alla boa di bolina"], "Conviene aspettare vicino alla linea e cazzare poco prima del via."]] },
    { name: "Lezione 17", title: "La partenza anticipata", steps: LD6, gruppo: "D", desc: "Oltre la linea al via: sale la X, si torna dietro e si riparte (regole 29.1 e 21.1). Esercizio in regata.",
      quiz: [["Al segnale di partenza la tua prua è oltre la linea. Che cosa succede?", "Sei in anticipo: sale la X e devi tornare dietro la linea", ["Niente: conta solo la poppa", "Hai fatto la partenza migliore", "Devi fare due giri di penalità"], "Basta una parte dello scafo oltre la linea al via: richiamo individuale (regola 29.1)."],
             ["Com'è fatta la bandiera X?", "Bianca con una croce blu", ["Blu con un quadrato bianco", "Tutta gialla", "Rossa con una croce bianca"], "La X del richiamo individuale è bianca con la croce blu; la P è blu con il quadrato bianco."],
             ["Che cosa devi fare dopo una partenza anticipata?", "Tornare con lo scafo tutto dietro la linea e partire di nuovo", ["Fare due giri di penalità", "Continuare fino alla boa", "Fermarti oltre la linea"], "Regola 29.1: si torna dietro la linea e si riparte."],
             ["Mentre torni dietro la linea, chi lascia strada?", "Tu, alle barche che non stanno tornando", ["Le altre barche a te", "Sempre la barca mure a sinistra", "Nessuno"], "Regola 21.1: chi torna dietro la linea lascia strada a chi non lo fa."]],
      esame: [["Il richiamo individuale", "Quale regola parla del richiamo individuale?", "La regola 29.1", ["La regola 10", "La regola 31", "La regola 44.2"], "È la 29.1."],
              ["Il richiamo individuale", "Per quanto tempo al massimo resta su la X?", "Quattro minuti dal via", ["Un minuto", "Fino all'arrivo", "Dieci secondi"], "Resta finché le barche in anticipo non sono tornate, ma non oltre quattro minuti dal via."],
              ["Tornare lasciando strada", "Quale regola dice che chi torna dietro la linea lascia strada?", "La regola 21.1", ["La regola 13", "La regola 26", "La regola 44.1"], "È la 21.1."],
              ["Parti in anticipo e torna", "Sei tornato dietro la linea dopo la X. Che cosa fai?", "Riparto tagliando la linea fra giuria e boa", ["Vado dritto alla boa di bolina", "Aspetto un'altra partenza", "Faccio un giro di penalità"], "Tornato dietro la linea, si riparte tagliandola come al via."]] },
    { name: "Lezione 20", title: "Boe e giri di penalità", steps: LD7, gruppo: "D", desc: "Non si toccano le boe; boa toccata un giro, contatto con colpa due (regole 31, 44.1, 44.2). Esercizio in regata.",
      quiz: [["Hai toccato la boa di bolina. Quanti giri di penalità fai?", "Uno", ["Due", "Nessuno", "Tre"], "Per una boa toccata basta un giro (regola 44.1)."],
             ["Hai urtato un'altra barca e la colpa è tua. Quanti giri fai?", "Due", ["Uno", "Nessuno", "Quattro"], "Per un contatto con colpa i giri sono due (regola 44.1)."],
             ["Che cosa deve avere ogni giro di penalità?", "Una virata e una strambata", ["Due virate", "Due strambate", "Niente: basta girare"], "Regola 44.2: ogni giro ha una virata e una strambata."],
             ["Fai due giri di penalità. In che verso?", "Tutti e due nello stesso verso, quello che preferisci", ["Uno per verso", "Sempre verso destra", "Sempre verso sinistra"], "Regola 44.2: i giri sono tutti nello stesso verso; quale, lo scegli tu."]],
      esame: [["Non toccare le boe", "Quale regola vieta di toccare le boe?", "La regola 31", ["La regola 10", "La regola 26", "La regola 13"], "È la 31."],
              ["Non toccare le boe", "Prima della partenza, quali boe non devi toccare?", "Quelle della linea di partenza", ["Nessuna: la regola vale dopo il via", "Solo la boa di bolina", "Solo quelle dell'arrivo"], "Prima della partenza non si toccano le boe di partenza (regola 31)."],
              ["I giri di penalità", "Mentre sconti una penalità, chi lascia strada?", "Tu, alle barche che non stanno scontando", ["Le altre barche a te", "La barca mure a sinistra", "Nessuno"], "Regola 21.2: chi sconta una penalità lascia strada."],
              ["I giri di penalità", "Quando si fanno i giri di penalità?", "Subito, appena ci si è allontanati dalle altre barche", ["All'arrivo", "Alla boa successiva", "Quando si vuole"], "Regola 44.2: appena possibile dopo l'incidente, lontano dalle altre barche."]] },
    { name: "Lezione 18", title: "Partenza in velocità", steps: LC1, gruppo: "C", desc: "Aspettare quasi fermi vicino alla linea e cazzare negli ultimi secondi, per partire già veloci. Esercizio in regata.",
      quiz: [["Prima del via, dove conviene aspettare con una barca come questa?", "Vicino alla linea, una o due lunghezze dietro, quasi fermo", ["Lontano dalla linea, per arrivare lanciato", "Già oltre la linea", "Vicino alla boa di bolina"], "Si aspetta vicino alla linea, quasi fermi con la vela lascata, e si accelera negli ultimi secondi."],
             ["Con che prua conviene aspettare?", "Appena sotto la bolina", ["In poppa", "Con la prua nel vento", "Al lasco"], "Da appena sotto la bolina basta cazzare per partire."],
             ["Cazzi troppo presto. Che cosa rischi?", "Di passare la linea prima del via: sale la X", ["Niente: più presto è meglio", "Di scuffiare", "Di dover fare due giri"], "Arrivi alla linea prima del via: partenza anticipata (regola 29.1)."],
             ["Cazzi troppo tardi. Che cosa succede?", "Al via sei ancora lento", ["Sei in anticipo", "La barca si ferma", "Non succede niente"], "Se cazzi tardi la barca non ha ancora preso velocità quando la linea si apre."]],
      esame: [["Aspettare vicino alla linea", "Mentre aspetti il via, come tieni la vela?", "Lascata, che sbatte: così la barca resta quasi ferma", ["Cazzata a ferro", "Regolata con i filetti dritti", "Spinta fuori con Z"], "Con la vela lascata la barca non avanza e si può aspettare il momento giusto."],
              ["Aspettare vicino alla linea", "Quanto dietro la linea conviene aspettare?", "Una o due lunghezze", ["Cento metri", "Mezzo metro oltre", "Dietro la barca giuria"], "Vicino alla linea: una o due lunghezze dietro."],
              ["Cazzare al momento giusto", "Da che cosa dipende il momento in cui cazzare?", "Da quanto sei lontano dalla linea e da quanto vento c'è", ["Solo dal colore della bandiera", "Da niente: sempre dieci secondi prima", "Dalla posizione della boa di bolina"], "Più sei lontano e meno vento c'è, prima devi cazzare."],
              ["Parti veloce", "Che cos'è una buona partenza?", "Tagliare la linea subito dopo il via, già veloce e senza anticipo", ["Tagliare la linea prima del via", "Partire da fermo al via", "Partire per ultimo, per non rischiare"], "Al via vicino alla linea, già veloce, senza anticipo."]] },
    { name: "Lezione 19", title: "Partenza da fermi", steps: LC2, gruppo: "C", desc: "Da fermi servono secondi e metri per prendere velocità: come si riparte nel modo più rapido. Esercizio in regata.",
      quiz: [["Una barca ferma con la vela che sbatte: appena cazzi, che cosa succede?", "Riparte, ma servono alcuni secondi e qualche metro per prendere velocità", ["È subito alla sua velocità", "Va all'indietro", "Non riparte più"], "La barca ha bisogno di tempo e strada per accelerare."],
             ["Da fermo, con che prua conviene cazzare?", "Appena sotto la bolina", ["Con la prua nel vento", "In poppa", "Non conta"], "Con la prua troppo vicina al vento la vela non porta: da appena sotto la bolina la barca parte."],
             ["Mentre la barca accelera, come la tieni?", "Piatta, con la vela regolata sui filetti", ["Molto sbandata", "Con la vela lascata", "Con la barra tutta da una parte"], "Piatta e con i filetti dritti, la barca accelera meglio."],
             ["Quando porti la prua in bolina?", "Quando la barca ha preso velocità", ["Subito, prima di cazzare", "Mai", "Solo dopo la boa"], "Prima si prende velocità, poi si orza fino alla bolina."]],
      esame: [["Partire da fermi", "Perché chi è fermo al via perde su chi ha cazzato prima?", "Perché gli servono secondi e metri per prendere velocità", ["Perché deve fare un giro di penalità", "Perché la linea si chiude", "Non perde niente"], "La barca ferma deve accelerare: chi ha cazzato prima al via è già veloce."],
              ["Come si riparte", "La prua è quasi nel vento e la barca non parte. Che cosa fai?", "Poggio un poco e poi cazzo", ["Cazzo a ferro e aspetto", "Orzo ancora", "Lasco tutto"], "Con la prua troppo vicina al vento la vela non porta: si poggia un poco, poi si cazza."],
              ["Come si riparte", "Da fermo hai cazzato e la barca accelera. Poi?", "Quando ha preso velocità porto la prua in bolina", ["Lasco di nuovo", "Viro subito", "Resto al traverso fino alla boa"], "Presa velocità, si orza fino alla bolina e si va verso la linea."],
              ["Parti da fermo", "In regata, quando ti serve partire da fermo nel modo più rapido?", "Quando sei chiuso fra le altre barche o hai sbagliato i tempi", ["Mai", "Solo all'arrivo", "Solo con tanto vento"], "Capita quando non si è potuto accelerare prima: allora conta ripartire subito."]] },
  ];

  // ---- prove ----
  // Prove: geometria descritta con il vento da nord (m), poi ruotata secondo il vento della prova.
  // bands: tempi massimi in secondi per oro, argento e bronzo (0.16), tarati con tests/collaudo_fasce.py:
  // oro = tempo del pilota automatico arrotondato ai 5 s superiori, argento +25%, bronzo +60%.
  // 1.0.6: ritarate per la barca nuova (resistenza dalla vasca) e il pilota corretto: argento e bronzo arrotondati ai 5 s più vicini.
  // 1.0.11: ritarate per la bolina nuova (pilota 79,0 / 124,5 / 156,8 / 276,0 s, prova 5 mediana 297,8): cambiano le prove 3, 4 e 5.
  // Dalla 0.19 l'ultima voce di marks è una linea d'arrivo (FIN_HALF m per lato, perpendicolare all'ultimo lato), non una boa da raggiungere.
  const MISSIONS = [
    { title: "Al traverso", desc: "Taglia l'arrivo con il vento di fianco.", wind: 270, tws: 10, gusts: 0,
      text: "Il vento non arriva più da nord: guarda la freccia. L'arrivo è al traverso. La vela parte troppo cazzata: regolala sui filetti e passa tra le due boe dell'arrivo.",
      start: { x: 0, y: 0, h: 90, sheet: 0.02 }, bands: [80, 100, 130],
      marks: [{ x: 230, y: 0, label: "Arrivo" }] },
    { title: "Lasco e poppa", desc: "Raggiungi l'arrivo sottovento.", wind: 45, tws: 10, gusts: 0,
      text: "L'arrivo è sottovento: poggia passando da traverso a lasco e poppa, lascando man mano. Attento a non strambare senza volerlo. Se devi per forza strambare, cazza prima tutta la vela, così la strambata è controllata (la vedrai meglio nella lezione 6).",
      start: { x: 0, y: 0, h: 90, sheet: 0.3 }, bands: [125, 155, 200],
      marks: [{ x: 60, y: 260, label: "Arrivo" }] },
    { title: "Risalire il vento", desc: "Raggiungi l'arrivo controvento.", wind: 180, tws: 10, gusts: 0,
      text: "L'arrivo è esattamente controvento. Bordeggia: bolina su una mura, virata con la barca lanciata, bolina sull'altra.",
      start: { x: 0, y: 0, h: 90, sheet: 0.2 }, bands: [160, 200, 255],
      marks: [{ x: 0, y: -220, label: "Arrivo" }] },
    { title: "Il giro di boa", desc: "Bolina all'andata, poppa al ritorno.", wind: 135, tws: 10, gusts: 0,
      text: "Risali di bolina fino alla boa e girala lasciandola a sinistra, poi torna a tagliare la linea da cui sei partito, con il vento da dietro. Se devi strambare, cazza prima e lasca dopo.",
      start: { x: 0, y: 20, h: 90, sheet: 0.2 }, bands: [280, 350, 450],
      marks: [{ x: 0, y: -200, label: "Boa" }, { x: 0, y: 20, label: "Arrivo" }] },
    { title: "Percorso nelle raffiche", desc: "Un triangolo con vento rafficato.", wind: 225, tws: 12, gusts: 1,
      text: "Tre lati: bolina fino alla boa 1, traverso fino alla boa 2, poi gran lasco fino alla linea d'arrivo. Le boe si lasciano a sinistra. Il vento è rafficato: guarda le chiazze, lasca quando entri, cazza quando escono.",
      start: { x: 0, y: 20, h: 90, sheet: 0.2 }, bands: [300, 375, 480],
      marks: [{ x: 0, y: -200, label: "Boa 1" }, { x: -150, y: -200, label: "Boa 2" }, { x: 0, y: 20, label: "Arrivo" }] }
  ];

  // 1.2.4 (docs/PROPOSTA-MENU.md, bozza A scelta da Ale il 2 nov 2026): la Scuola in tre gruppi, nell'ordine di PROPOSTA-LEZIONI-SCUOLA.md §5,
  // con le prove dove stavano. Le lezioni si chiamano «Lezione N» in quest'ordine; i salvataggi restano legati all'indice in LESSONS ("l" + i).
  const GRUPPI = [
    ["La barca", [["l",0],["l",1],["l",6],["l",2],["m",0],["m",1],["l",3],["l",4],["l",7],["m",2],["m",3]]],
    ["Vento e raffiche", [["l",5],["l",9],["l",8],["l",10],["m",4]]],
    ["Regole e partenze", [["l",11],["l",12],["l",13],["l",14],["l",15],["l",16],["l",18],["l",19],["l",17]]]
  ];
  const SEQ = GRUPPI.flatMap(g => g[1]);
  const ORD_L = SEQ.filter(([t]) => t === "l").map(([, i]) => i); // indici di LESSONS nell'ordine della Scuola
  const numLez = i => ORD_L.indexOf(i) + 1;
  const gruppoDi = ([t, i]) => GRUPPI.findIndex(g => g[1].some(([u, j]) => u === t && j === i));


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
      ["Vuoi poggiare, cioè allontanare la prua dal vento. Dove sposti la barra?", "Sopravento, cioè lontano dal boma", ["Sottovento, verso il boma", "Al centro", "Dipende da quanto è cazzata la vela"], "La regola: barra sopravento poggia, barra sottovento orza."] ],
    [ ["Qual è l'andatura più vicina al vento?", "Bolina", ["Traverso", "Lasco", "Poppa"], "Bolina stretta è il massimo che la barca riesce a stringere; più vicino si entra nell'angolo morto."],
      ["Il vento arriva perpendicolare alla barca, a 90°. In che andatura sei?", "Traverso", ["Bolina larga", "Gran lasco", "Poppa"], "Al traverso il vento è di fianco: andatura veloce, con la vela aperta circa a metà (boma a una quarantina di gradi dal centro barca)."],
      ["Si agita il filetto sopravento. Cosa fai?", "Cazzo la vela, oppure poggio", ["Lasco la vela, oppure orzo", "Non faccio nulla: è normale", "Centro la barra"], "Filetto sopravento agitato: vela troppo lascata, o prua troppo vicina al vento."],
      ["Orzando, come va regolata la vela?", "Va cazzata", ["Va lascata", "Non va toccata", "Va lasciata sbattere"], "Orzi e cazzi, poggi e laschi."],
      ["Il vento arriva sul lato sinistro della barca. Come si naviga?", "Mure a sinistra", ["Mure a dritta", "Al traverso", "Sottovento"], "Le mure prendono il nome dal lato da cui arriva il vento."] ],
    [ ["Che cos'è il vento apparente?", "Il vento che si sente a bordo: vento reale più vento dovuto al moto della barca", ["Il vento indicato dalle previsioni", "Il vento misurato da fermi", "Il vento delle raffiche"], "È il vento su cui lavora la vela, ed è quello indicato dal segnavento in cima all'albero."],
      ["Quando la barca accelera, il vento apparente si sposta…", "verso prua", ["verso poppa", "non si sposta", "verso il lato sottovento"], "Il vento dovuto al moto arriva da prua e si somma al vento reale."],
      ["Navigando in poppa, il vento apparente è…", "più debole del vento reale", ["più forte del vento reale", "uguale al vento reale", "sempre nullo"], "In poppa la barca «scappa» dal vento; di bolina invece il vento apparente è più forte."],
      ["Al traverso la barca accelera. Cosa conviene fare con la vela?", "Cazzarla un po'", ["Lascarla un po'", "Lasciarla com'è", "Lascarla del tutto"], "Il vento apparente si sposta verso prua, quindi la vela deve seguirlo e va cazzata."] ],
    [ ["Che cos'è una virata?", "Cambiare mure passando con la prua attraverso il vento", ["Cambiare mure passando con la poppa attraverso il vento", "Girare di 360°", "Poggiare fino alla poppa"], "La virata attraversa l'angolo morto; la strambata attraversa la poppa."],
      ["Perché una virata può fallire?", "Perché la barca non ha abbastanza velocità per attraversare l'angolo morto", ["Perché la vela è troppo cazzata", "Perché il vento è troppo forte", "Perché la barra è al centro"], "Nell'angolo morto la vela non spinge: la barca deve attraversarlo con l'abbrivio."],
      ["La barca si è fermata nel vento e comincia ad andare all'indietro. Cosa succede alla barra?", "Funziona al contrario", ["Non ha più nessun effetto", "Funziona come prima", "Si blocca al centro"], "Con l'acqua che scorre sulla pala da dietro, l'effetto del timone si inverte."],
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
  // 1.2.3 (docs/PROPOSTA-ESAME-E-GLOSSARIO.md, Ale 2 nov 2026): le lezioni nuove (dalla 7) danno QUOTA_NUOVE domande, prese dal loro campo esame;
  // entrano solo le lezioni visibili nel menu (non nascosta); soglia = SOGLIA_ESAME delle domande, arrotondata per eccesso (16 su 20, 28 su 34).
  const QUOTE = [4, 3, 4, 3, 3, 3], QUOTA_NUOVE = 1, SOGLIA_ESAME = 0.8;
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

  const bancaEsame = li => ESAME[li] || LESSONS[li].esame || [];
  const quotaEsame = li => li < QUOTE.length ? QUOTE[li] : QUOTA_NUOVE;
  const lezioniEsame = () => LESSONS.map((L, li) => li).filter(li => !LESSONS[li].nascosta && bancaEsame(li).length);
  const domandeEsame = () => lezioniEsame().reduce((a, li) => a + quotaEsame(li), 0);
  const sogliaEsame = (n = domandeEsame()) => Math.ceil(n * SOGLIA_ESAME - 1e-9);
  const quizDi = li => QUIZ[li] || LESSONS[li].quiz; // 1.2.3: il ripasso di una lezione nuova usa il quiz della lezione

  // ---- glossario ----
  // dalla 1.2.3 le voci delle lezioni nuove (terzo campo = nome della lezione) restano nascoste come la lezione (glossVisibili)
  const GLOSS = [
    ["Abbrivio", "La velocità che la barca conserva per inerzia, per esempio mentre attraversa il vento durante una virata.", "Lezione 6"],
    ["Albero", "Il palo verticale che regge la vela.", "Lezione 1"],
    ["Andatura", "La direzione della barca rispetto al vento: bolina, traverso, lasco, gran lasco, poppa.", "Lezione 4"],
    ["Angolo morto", "Il settore attorno alla direzione del vento in cui la vela non spinge e non si può navigare: nelle scuole si indica di solito in circa 45° per lato (90° in tutto); le derive riescono a stringere un po' di più.", "Lezione 1"],
    ["Avviso", "Il primo segnale della partenza, cinque minuti prima del via: sale la bandiera di classe (regola 26).", "Lezione 16"],
    ["Bandiera di classe", "Sale all'avviso, cinque minuti prima del via, e si ammaina alla partenza.", "Lezione 16"],
    ["Barca giuria", "La barca da cui si dà la partenza, alzando e ammainando le bandiere. Nel gioco è un estremo della linea di partenza; l'altro è la boa arancione.", "Lezione 16"],
    ["Barra", "Il manico del timone. Si sposta dalla parte opposta a quella verso cui si vuole girare: barra sottovento, la barca orza; barra sopravento, la barca poggia.", "Lezione 2"],
    ["Boa", "Galleggiante ancorato al fondo, usato come riferimento o come segnale.", "Prove"],
    ["Linea d'arrivo", "Linea immaginaria fra due boe (in regata spesso fra una boa e la barca giuria): si arriva quando la si attraversa venendo dal percorso.", "Prove"],
    ["Bolina", "L'andatura più vicina al vento. Bolina stretta: circa 45°, il massimo che la barca riesce a stringere; bolina larga: circa 60-75°.", "Lezione 4"],
    ["Boma", "L'asta orizzontale, fissata all'albero, che tiene il lato basso della randa.", "Lezione 1"],
    ["Bordeggiare", "Risalire il vento a zig-zag, alternando tratti di bolina sulle due mure. Ogni tratto è un bordo.", "Lezione 6"],
    ["Buono", "Di bolina, il vento è buono quando gira verso poppa: puoi orzare. Lo stesso salto che è scarso su una mura è buono sull'altra.", "Lezione 11"],
    ["Cazzare", "Tirare una scotta: la vela si avvicina al centro della barca.", "Lezione 1"],
    ["Cima", "A bordo le corde si chiamano cime.", "Lezione 1"],
    ["Deriva (barca)", "Piccola barca a vela senza cabina, con la lama di deriva mobile. È la barca su cui di solito si impara.", "Lezione 1"],
    ["Deriva (lama)", "La lama che scende sotto lo scafo e impedisce alla barca di essere spinta di lato dal vento.", "Lezione 1"],
    ["Dritta", "Il lato destro della barca, guardando verso prua.", "Lezione 1"],
    ["Filetti", "Nastrini sulla vela che mostrano come scorre l'aria: dritti se la vela è regolata; si agita quello sopravento se è troppo lascata, quello sottovento se è troppo cazzata.", "Lezione 4"],
    ["Fileggiare", "Il movimento della vela che sbatte perché è troppo lascata o perché la barca è nell'angolo morto.", "Lezione 1"],
    ["Giro di penalità", "Un giro intero della barca, con una virata e una strambata, per scontare una penalità: uno per una boa toccata, due per un contatto con colpa; subito e tutti nello stesso verso (regole 44.1 e 44.2).", "Lezione 20"],
    ["Gran lasco", "Andatura con il vento quasi da dietro, circa 150°.", "Lezione 4"],
    ["Lascare", "Mollare una scotta: la vela si apre verso l'esterno.", "Lezione 1"],
    ["Lasciare strada", "Navigare in modo che l'altra barca possa tenere la sua rotta senza manovrare per evitarti. Con mure diverse lascia strada la barca mure a sinistra (regola 10).", "Lezione 12"],
    ["Lasco", "Andatura con il vento che arriva da dietro il fianco, circa 120°.", "Lezione 4"],
    ["Libera dietro, libera avanti", "Con le stesse mure, una barca che sta tutta dietro la linea tirata al traverso dal punto più a poppa dell'altra è libera dietro, e lascia strada a quella libera avanti (regola 12).", "Lezione 13"],
    ["Linea di partenza", "La linea dalla barca giuria alla boa arancione. Al via si deve essere dietro, dalla parte da cui si parte; poi la si taglia.", "Lezione 16"],
    ["Mure", "Il lato da cui arriva il vento: mure a dritta se arriva da destra, mure a sinistra se arriva da sinistra. Tra due barche a vela con mure diverse, quella mure a sinistra deve lasciare strada; con le stesse mure, se sono affiancate, cede quella sopravento.", "Lezione 4"],
    ["Nodo", "Unità di velocità in mare: un miglio nautico all'ora, cioè 1,852 km/h.", "Lezione 1"],
    ["Orzare", "Girare la prua verso il vento.", "Lezione 1"],
    ["Orziera", "Barca che tende a salire da sola verso il vento. Le cause possono essere diverse e spesso si sommano: il vento e le raffiche, le onde che spostano la prua, la barca molto sbandata, le vele troppo cazzate, la posizione e il peso dell'equipaggio. Si corregge con la barra e, quando si può, con le vele e con il peso.", "Lezione 2"],
    ["Partenza anticipata", "Al segnale di partenza una parte dello scafo è già oltre la linea. Si torna con lo scafo tutto dietro la linea e si riparte (regola 29.1).", "Lezione 17"],
    ["Partenza da fermi", "Partire con la barca ferma e la vela che sbatte: cazzata la vela, servono alcuni secondi e qualche metro prima che la barca arrivi alla sua velocità.", "Lezione 19"],
    ["Partenza in velocità", "Aspettare quasi fermi vicino alla linea, una o due lunghezze dietro, e cazzare negli ultimi secondi, per tagliare la linea subito dopo il via e già veloci.", "Lezione 18"],
    ["Poggiare", "Girare la prua allontanandola dal vento.", "Lezione 1"],
    ["Poppa (andatura)", "Andatura con il vento esattamente da dietro.", "Lezione 4"],
    ["Poppa (parte della barca)", "La parte posteriore della barca.", "Lezione 1"],
    ["Precedenza", "Ce l'ha la barca a cui l'altra deve lasciare strada. Avere la precedenza non è il permesso di urtare.", "Lezione 12"],
    ["Preparatorio", "Il segnale di quattro minuti prima del via: sale la bandiera P, blu con il quadrato bianco. Si ammaina a un minuto dal via (regola 26).", "Lezione 16"],
    ["Prua", "La parte anteriore della barca.", "Lezione 1"],
    ["Raddrizzare", "Rimettere dritta una deriva scuffiata, salendo sulla lama di deriva e facendo leva col proprio peso.", "Lezione 8"],
    ["Raffica", "Aumento breve del vento, visibile sull'acqua come una chiazza più scura e increspata.", "Lezione 8"],
    ["Randa", "La vela principale, fissata all'albero e al boma.", "Lezione 1"],
    ["Richiamo individuale", "La bandiera X, bianca con la croce blu, alzata con un suono quando al via qualcuno è in anticipo. Resta su finché sono tornati tutti, ma non più di quattro minuti dal via (regola 29.1).", "Lezione 17"],
    ["Rilevamento", "La direzione, in gradi a partire da nord in senso orario, in cui si vede un oggetto dalla barca.", "Prove"],
    ["Salto di vento", "Un cambio di direzione del vento. Spesso il vento oscilla avanti e indietro; a volte gira sempre dalla stessa parte.", "Lezione 11"],
    ["Sbandamento", "L'inclinazione laterale della barca spinta dal vento.", "Lezione 8"],
    ["Scarroccio", "Lo scivolamento laterale della barca spinta dal vento, che la deriva riduce ma non annulla.", "Lezione 1"],
    ["Scarso", "Di bolina, il vento è scarso quando gira verso la prua: per restare di bolina devi poggiare. Con il vento che oscilla, di bolina si vira sugli scarsi.", "Lezione 11"],
    ["Scotta", "La cima con cui si regola la vela.", "Lezione 1"],
    ["Scuffiare", "Rovesciarsi: succede alle derive quando lo sbandamento diventa eccessivo.", "Lezione 8"],
    ["Segnavento", "La piccola freccia gialla in cima all'albero: la punta indica da dove arriva il vento apparente (per questo sembra opposta alla freccia gialla grande «apparente», che arriva dal mare e punta verso la barca).", "Lezione 5"],
    ["Sinistra", "Il lato sinistro della barca, guardando verso prua.", "Lezione 1"],
    ["Sopravento", "Il lato colpito per primo dal vento; in generale, la parte da cui arriva il vento.", "Lezione 1"],
    ["Sottovento", "Il lato riparato, opposto a quello da cui arriva il vento.", "Lezione 1"],
    ["Sovrapposte", "Due barche con le stesse mure sono sovrapposte, cioè affiancate, quando nessuna delle due sta tutta dietro una linea tirata al traverso dal punto più a poppa dell'altra. Lascia strada la sopravento (regola 11).", "Lezione 13"],
    ["Spingere il boma", "Con la barca ferma nell'angolo morto, spingere il boma fuori e mettere la barra dalla stessa parte: la barca arretra e la prua gira lontano dal vento. Serve anche a frenare o ad arretrare apposta. Nel gioco, tasto Z.", "Lezione 7"],
    ["Sporgersi fuori bordo", "Spostare il peso fuori dalla barca, sopravento, per contrastare lo sbandamento.", "Lezione 8"],
    ["Stallo", "Vela troppo cazzata: non sbatte, ma l'aria non ci scorre sopra bene e la barca rallenta.", "Lezione 1"],
    ["Stallo della pala", "La pala del timone girata oltre un certo angolo: l'acqua non riesce più a seguirla e si stacca, la spinta smette di crescere e la pala frena sempre di più. Su una deriva da regata succede fra circa 15° e 30°.", "Lezione 3"],
    ["Strambata", "Cambio di mure passando con la poppa attraverso il vento; detta anche abbattuta. Se involontaria o fatta con la vela aperta, il boma attraversa la barca con violenza.", "Lezione 6"],
    ["Timone", "La pala immersa a poppa che fa girare la barca, comandata dalla barra.", "Lezione 1"],
    ["Traverso", "Andatura con il vento perpendicolare alla barca, circa 90°.", "Lezione 4"],
    ["Vento apparente", "Il vento che si sente a bordo: combinazione del vento reale e del vento creato dal moto della barca. È quello su cui lavora la vela.", "Lezione 5"],
    ["Vento reale", "Il vento come soffia rispetto al mare, quello che si misura da fermi.", "Lezione 5"],
    ["Virata", "Cambio di mure passando con la prua attraverso il vento.", "Lezione 6"]
  ];
  const glossVisibili = () => GLOSS.filter(([, , w]) => !LESSONS.some(L => L.nascosta && L.name === w));

