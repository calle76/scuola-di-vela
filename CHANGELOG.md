# Diario delle modifiche

Tutte le versioni sono del 26–27 settembre 2026. I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

## 0.14 — Giro di boa, andatura nascosta, barra ferma in gara
- **Decisioni (fase A):** andatura nascosta nel pannello delle lezioni 1 e 2; boe da lasciare a sinistra in prove e regate; barra che non torna al centro in prove e regate, riattivabile.
- **Andatura nel pannello:** nascosta nelle lezioni 1 e 2, perché le andature si spiegano nella lezione 3.
- **Barra:** l'impostazione «La barra torna al centro da sola» vale ora per la modalità in corso. Lezioni e navigazione libera: attiva, come prima. Prove e regate: spenta, perché un regatante tiene la barra ferma; la barra spaziatrice la riporta al centro. Si può riattivare.
- **Giro di boa:** prima una boa contava appena ci si passava entro 12 m (prove) o 15 m (regate), senza girarla davvero. Ora le boe intermedie vanno girate lasciandole a sinistra: conta l'attraversamento, in senso antiorario, della semiretta che parte dalla boa verso l'esterno della curva del percorso. Chi la gira dal lato sbagliato deve tornare indietro e rifare il giro, come nella regola del filo teso; il gioco lo segnala. Una freccia curva mostra il verso di giro. La boa di arrivo delle prove e l'unica boa delle prove 1–3 restano punti da raggiungere.
- **Prova 5:** il triangolo girava in senso orario (boe a dritta); ora è specchiato. **Difetto di contenuto trovato:** il testo diceva «traverso» per il secondo lato, che in realtà era un lasco a circa 126° dal vento. Testo corretto.
- **Record e fantasmi** delle prove 4 e 5 e delle regate ripartono da zero (chiavi nuove): con il giro vero i tempi non sono confrontabili. Le voci completate restano completate.
- **Avversari:** girano la boa passando per tre punti (sotto a destra, oltre a sinistra; un terzo punto solo per riprovare dopo un giro mancato), con un giro leggermente diverso per ciascuno.
- **Difetti trovati nei collaudi e corretti:**
  - avversari che passavano sopra la boa senza girarla: il cambio di rotta scattava ancora sotto la boa, da dove la bolina li portava dritti sulla boa;
  - avversari che tentavano di virare dal traverso al traverso opposto, perdevano l'abbrivio a metà e ricominciavano all'infinito. Ora prima orzano fino alla bolina, poi virano, poi poggiano;
  - barca ferma tra 40° e 44° dal vento che non ripartiva mai, perché la regola «piantata: poggia» scattava solo sotto 40°. Ora 44°, tranne in partenza, dove 44° faceva poggiare troppo presto vicino alla linea (resta 40°, salvo chi torna dietro la linea dopo una partenza anticipata).
- **Tempi degli avversari** (regata a bastone): bolina da 124 a 150 s, poppa da 84 a 93 s. Circa 12 s dipendono dalla vecchia scorciatoia del cerchio di 15 m, il resto dal giro vero. Le fasce di tempo della fase A vanno tarate sui tempi nuovi.
- **Nuovo collaudo** `collaudo_giro_boa.py`: un pilota automatico guida la barca con barra e scotta e verifica il giro dal lato giusto, dal lato sbagliato, sbagliato e poi corretto, il triangolo, e le prove 1–3 invariate. Aggancio `#collaudo` esteso con barra, scotta e boe.
- **Collaudi:** 19 regate su 19 concluse con tutti gli avversari (prima delle correzioni circa una su dieci si bloccava); contatti tra avversari non aumentati (22 in 12 regate contro 44 della 0.13); ritardi al via uguali alla 0.13 su 36 partenze; lezioni, strambata, quiz, rotta, schermate e fantasma invariati.

## 0.13 — Angolo morto realistico
- **Decisione:** angolo morto allineato alle dispense di vela (45° per lato come convenzione didattica, circa 35° per le derive). Prima la barca avanzava fino a 25–30° dal vento, più di qualsiasi fonte.
- Fisica: la vela si sgonfia quando il vento apparente è troppo stretto (`luffA0` 27°, `luffW` 7°), angolo minimo del boma 14°. Ora la barca è ferma sotto circa 33° dal vento, arranca fino a 40° e risale meglio a 45–48°.
- Timone leggermente più efficace (`turnLen` 1,05 m): con l'angolo morto più largo la virata lanciata durava 6 secondi; ora circa 4, come una deriva vera.
- Cerchio delle andature: angolo morto fino a 40°. Aggiornate le condizioni delle lezioni 1, 2, 3 e 5, i testi (bolina «tra 45° e 75°»), il glossario (angolo morto, bolina) e gli angoli di bolina degli avversari.
- Collaudi: tutte le lezioni completabili; 6 regate su 6 concluse; strambata invariata. Resta il difetto noto delle partenze degli avversari (vedi ROADMAP, fase B).

## 0.12 — Revisione generale
- Lezione 2, «Tenere la rotta»: onde che spostano la prua e barca orziera. Prima l'esercizio si completava senza fare nulla.
- Lezione 4: vento apparente indicato «tra 60° e 70°», coerente con il pannello.
- Lezione 6: testo del raddrizzamento coerente con la simulazione.
- Lezioni 1–3: solo la freccia del vento reale (il vento apparente si spiega nella lezione 4).
- Scotta più lenta di circa un quarto: la finestra di «vela regolata» era sotto il secondo di pressione.
- Più spazio tra i comandi di barra e scotta.

## 0.11 — Strambata corretta
- **Difetto:** qualsiasi strambata con la vela aperta faceva scuffiare, anche con 6 nodi. **Causa:** il colpo del boma era sommato in gradi/s a una velocità di sbandamento espressa in radianti/s, quindi era 57 volte più forte. **Correzione:** unità corrette e colpo proporzionale al vento (19° di sbandamento con 6 nodi, 39–58° con 10, scuffia con 15).
- «Vela a metà» spiegato: boma a una quarantina di gradi dal centro barca.
- Lezione 3: spiegato cosa succede superando i 180° in poppa.
- Messaggio specifico quando si scuffia per una strambata.

## 0.10 — Partenze e aiuti al timone
- Preparazione della regata a scelta: 1, 3 (predefinita) o 5 minuti; segnali adattati.
- Distanza e tempo alla linea durante l'attesa.
- Regata in solitaria contro il proprio fantasma.
- Freccia sulla prua che mostra da che parte gira la barca, e scritta «Barra a … → la prua gira a …».
- **Difetto:** gli avversari partivano con 5–70 secondi di ritardo. **Cause:** attendevano sottovento alla linea e dovevano risalire controvento; poi, attendendo vicino alla linea, tentavano virate da fermi e si piantavano. **Correzione:** attesa di fianco e sottovento, arrivo di bolina larga senza virare; regola «mai virare da fermi», valida solo prima di iniziare la virata.
- **Difetto introdotto e corretto:** la regola «mai virare da fermi», applicata anche a metà virata, faceva girare gli avversari attorno alla boa senza fine.

## 0.9 — Fantasma e regate
- Fantasma del record nelle prove e nelle regate, registrato rispetto al vento.
- Regata a bastone e regata nelle raffiche contro tre avversari, con partenza, partenza anticipata, precedenze e penalità, classifica.
- **Difetti trovati nei collaudi:** avversari che si scontravano di continuo (fino a 17 contatti a regata); avversari piantati nell'angolo morto durante le manovre per evitarsi; avversari che viravano avanti e indietro vicino alla boa; linea superata fuori dagli estremi senza conseguenze. Tutti corretti.

## 0.8 — Ripasso e verifica
- 29 domande di ripasso sulle sei lezioni.
- Scheda dei contenuti da verificare.

## 0.7 — Scuola sul nuovo motore
- Sei lezioni ricostruite sul simulatore: la barca e il vento, il timone, andature e filetti, vento reale e apparente, virata e strambata, raffiche e scuffia.
- Cinque prove con vento da direzioni diverse; navigazione libera; glossario ampliato.
- **Difetti trovati nei collaudi:** nella lezione 1, tenendo premuto Orza la barca virava, strambava e scuffiava; la scuffia «volontaria» della lezione 6 poteva richiedere più di un minuto. Corretti.

## 0.6 — Nuovo motore (campo prova)
- Vento apparente, portanza e resistenza della vela, filetti, barra reale, scarroccio.
- Sbandamento con timoniere che si sporge, raffiche visibili, scuffia e raddrizzamento.
- **Difetti:** raffiche invisibili (più grandi dell'area inquadrata); pannello che «saltava» cambiando altezza sotto i cursori; gioco bloccato dopo una scuffia su schermi piccoli. Corretti.

## 0.5 — Menu e glossario
- Menu con progressi salvati, glossario, vento da direzioni diverse nelle prove.

## 0.4 — Virata e strambata
- Lezione sulle due manovre; virata che fallisce senza abbrivio.

## 0.3 — Le andature
- Cerchio delle andature attorno alla barca.

## 0.2 — Lezione guidata
- Prima lezione passo passo, dopo che il primo prototipo si era rivelato incomprensibile per chi parte da zero.

## 0.1 — Primo prototipo
- Vista dall'alto, una vela, comandi Orza, Poggia, Cazza, Lasca, quattro prove.
