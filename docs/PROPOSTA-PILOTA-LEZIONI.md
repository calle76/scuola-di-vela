# Proposta: pilota completo delle lezioni (fermata 1)

**Rivista in chat il 16 ottobre 2026; le sei osservazioni sono accettate da Ale e integrate qui (sezione 9).**

16 ottobre 2026, dopo la 1.0.2. Primo dei lavori che chiudono il livello 1 (`ROADMAP.md`, «Dopo la 1.0.1»). **Niente codice in `index.html`**: è un collaudo nuovo. Se servisse un aggancio in più, solo dentro `window.__sv`, che senza `#collaudo` non esiste.

## 1. Perché

- **Copertura.** Le lezioni hanno **32 passi pratici**, cioè passi con una condizione da raggiungere. Oggi `collaudo_lezioni.py` ne guida davvero **14**. Altri quattro sono guidati da collaudi sparsi, con scopi diversi: «Tenere la rotta» da `collaudo_rotta.py`; «Una virata che non riesce», «Strambata violenta» e «Strambata controllata» da `collaudo_registro.py`; l'arrivo di «Risalire il vento» da `collaudo_linea.py`. Nessun collaudo dimostra che ogni passo si possa completare guidando.
- **Passi che si completano da soli.** Le osservazioni 45 e 49 di Ale:
  - lezione 1, «Ripartire»: la barca riparte da sola;
  - lezione 2: se nel passo 4 la prua va oltre, il passo 5 risulta già fatto.

  Nessun collaudo cerca questo difetto. L'unico esempio è `collaudo_rotta.py`, che controlla che «Tenere la rotta» a mani ferme non si completi.
- **Rete di sicurezza per la fisica.** Resistenza dello scafo e timone cambieranno velocità e virate. Senza questo pilota nessuno ci direbbe se un passo diventa impossibile.

## 2. Cosa misura

Per ognuno dei 32 passi, tre misure. La lezione si percorre **dall'inizio, nell'ordine, come un giocatore**: ogni passo parte dallo stato in cui il passo prima lo ha lasciato, senza `showStep` per saltare. **In ogni passo, prima 30 s a mani ferme, poi la guida**, come chi legge il testo e poi agisce; non si salva né si ripristina lo stato. Per ogni seme ogni lezione si percorre **due volte**: una con il pilota preciso (danno le misure «a mani ferme» e «guidando»), una con il giocatore impreciso (dà la misura «dopo un colpo lungo»).

| Misura | Come | Attesa nostra |
| --- | --- | --- |
| **«Guidando»: si completa** | Il pilota fa quello che dice il testo del passo | Completato in tutti i semi, entro un tempo limite per passo (da 20 a 120 s simulati, scritto nella tabella del pilota prima di lanciarlo) |
| **«A mani ferme»: non si completa da solo** | Arrivati al passo dopo aver guidato il passo prima, **mani ferme** per 30 s simulati: nessun tasto, barra che torna al centro se l'impostazione lo fa, scotta ferma salvo i passi in cui la vela si regola da sola | **0** completamenti |
| **«Dopo un colpo lungo»: non è già fatto all'arrivo** | Come «a mani ferme», ma il passo prima lo guida un **giocatore impreciso**, che tiene il tasto da 0,3 a 1,5 s più del necessario (seme fisso). È il caso dell'osservazione 49 | **0** completamenti |

I passi in cui il testo chiede proprio di non fare niente si dichiarano prima e si contano a parte, non come errori.

Le **attese sono nostre**, non numeri delle fonti. Se un passo non le rispetta, si **riporta com'è**: passo, misura, quante volte su quante, stato della barca. Non si corregge niente in questo compito. Ogni passo da correggere diventa una proposta a parte, perché toccherebbe il testo o la condizione della lezione, cioè contenuti.

## 3. Il pilota

- **Solo informazioni che il giocatore vede a schermo:** angolo dal vento, velocità, filetti, sbandamento, la barca che arretra, la boa e la linea. **Lezioni 1 e 2:** la voce «Andatura» del pannello è nascosta (`setHud`); c'è solo la rosetta dell'angolo morto con la lancetta della prua. Lì il pilota legge l'angolo come si legge a occhio sulla lancetta, con un **errore di lettura di ±5°** (ipotesi nostra, estratto col seme), e gli obiettivi si scrivono come li scrive il testo («metà strada tra il rosso e l'orizzontale», «quasi da dietro»), non come numeri esatti. Dalla lezione 3 c'è la rosa grande con le andature e la voce «Andatura». Non legge le condizioni dei passi in `index.html`. Altrimenti sarebbe un metro che dipende da ciò che misura: completerebbe il passo per costruzione.
- **Guida con i tasti veri** (frecce, W, S, R), inviati alla pagina come fa `collaudo_lezioni.py`. Il tempo avanza a passi fissi di 1/60 s (`__sv.run`), con `Math.random` a seme fisso.
- **Una tabella, una riga per passo.** Cosa fare, letto dal testo del passo: per esempio «orza fino alla bolina a piccoli colpi» diventa «obiettivo 55° dal vento, colpi di barra di 0,3 s, poi barra al centro». Ci sono anche il tempo limite e l'eventuale «non fare niente». Le 14 azioni di oggi si riusano dove funzionano già. Le parti già scritte per la virata che non riesce e per le strambate si prendono da `collaudo_registro.py`.
- **Tempo di reazione del pilota:** da 0,1 a 0,4 s, estratto col seme. Così semi diversi danno arrivi diversi anche nelle lezioni senza raffiche.
- **Un file nuovo, `tests/collaudo_pilota_lezioni.py`.** `collaudo_lezioni.py` resta com'è, come confronto. Far usare la nuova tabella a `collaudo_carriera_intera.py` (32 passi guidati invece di 14) è un **passo a parte, dopo il rapporto**, per tenere aperto un solo fronte.

## 4. Semi e soglie

- **Regola dei semi:** il pilota si mette a punto sui **semi 1-20** e si conferma sui **semi 21-100**, mai guardati. Nel rapporto ci sono tutti e due i gruppi.
- **Cosa si può correggere dopo i semi 1-20:** solo il pilota. Per esempio, se sbaglia a leggere un testo, si corregge e lo si dichiara. Le attese delle tre misure non cambiano.
- Se sui semi 21-100 un passo non si completa «guidando» e sui primi 20 sì, si riporta, senza ritoccare il pilota per farlo passare.

## 5. Controlli che il metro misuri davvero

- **Quanto ha misurato:** il collaudo stampa quanti passi ha guidato (32 attesi), quanti semi per passo e quante corse a mani ferme. È **NON VALIDO** se un passo ha zero corse.
- **Contro-prova di «guidando»:** su una copia della pagina con la condizione di un passo resa **sempre falsa**, la misura «guidando» deve segnalare quel passo come non completato. Senza, un errore del collaudo nel leggere il completamento passerebbe inosservato.
- **Osservazione 45 come contro-prova di «a mani ferme»:** «Ripartire» (lezione 1) chiede un'azione («tieni premuto… finché la barca riparte»), quindi **non** è fra i passi in cui si aspetta; la misura deve trovare il difetto osservato da Ale. Se non lo trova, il collaudo non misura quello che dice.
- **Contro-prova di «a mani ferme»:** «Tenere la rotta» a mani ferme non si completa, lo stesso risultato di `collaudo_rotta.py`. Su una copia della pagina con la condizione di un passo resa sempre vera, la misura «a mani ferme» deve trovare quel passo. Il copione cambiato si scrive nel rapporto.
- **Contro-prova di «dopo un colpo lungo»:** il caso dell'osservazione 49, lezione 2 passo 4 con il giocatore impreciso. Se la misura non lo trova, il giocatore impreciso non è abbastanza impreciso, e lo si dice.
- **Pagina senza `#collaudo`:** la lezione 2, passi «Barra a sinistra» e «Barra a dritta», guidata in tempo reale con la tastiera vera, legge il completamento dalla pagina (testo di fine passo visibile). Serve a dimostrare che quello che misura il collaudo succede anche nel gioco caricato da un giocatore. In tempo reale il risultato non è ripetibile: **superata vuol dire entrambi i passi completati in 3 tentativi su 3**.

## 6. Costanti nuove (tutte ipotesi nostre, nessuna fonte)

| Costante | Valore | Perché |
| --- | --- | --- |
| Finestra a mani ferme (le due misure senza tasti) | 30 s simulati | Più lunga di ogni condizione con tenuta (al massimo 8 s, «Tenere la rotta»); un giocatore che legge il testo ci mette circa quel tempo |
| Eccesso del giocatore impreciso | 0,3-1,5 s di tasto in più | Copre «un colpo lungo» al posto di «piccoli colpi»; da rivedere se la sua contro-prova fallisce |
| Reazione del pilota | 0,1-0,4 s | Per avere arrivi diversi a seme diverso |
| Errore di lettura della lancetta (lezioni 1 e 2) | ±5° | Una lancetta su un quadrante di 68 px non si legge al grado |
| Tempi limite per passo | 20-120 s simulati | Si scrivono nella tabella prima di lanciare; un passo che li supera si riporta |

## 7. Rischi

- **Un passo che il pilota non completa può essere un difetto del pilota, non del passo.** Lo distingue il rapporto: stato della barca, tasti premuti, testo del passo. In caso di dubbio Ale prova il passo a mano.
- **«A mani ferme» può dare falsi allarmi** nei passi che chiedono di aspettare: «Da fermi» (prima si lasca, poi si aspetta), «Prepararsi a virare» (la barca deve prendere velocità). Questi si dichiarano prima, nella tabella.
- **La lezione 6 dipende dalle raffiche**, quindi dal seme. È proprio il caso in cui servono i 100 semi.
- **Durata:** circa 32 passi × 3 misure × 100 semi, a passi fissi. Stima: alcuni minuti nella sandbox. Se è troppo, `--veloce` con i semi 1-5.
- **La fisica non si tocca.** `polare.js` e `raffiche_e_virate.js` restano identici. `index.html` non cambia, salvo un eventuale aggancio in `__sv`, dichiarato.

## 8. Cosa si consegna alla fermata 2

- `tests/collaudo_pilota_lezioni.py`, con la tabella dei 32 passi e i tempi limite scritti prima di lanciare.
- Il rapporto: per ogni passo le tre misure sui semi 1-20 e 21-100, con le contro-prove.
- L'elenco dei passi da correggere, ognuno con la sua proposta, da decidere dopo.
- La riga del collaudo in `COLLAUDI.md` e in `lancia_tutti.sh`, e una voce sotto la versione successiva nel `CHANGELOG`. Non cambia il gioco, quindi non serve una versione nuova.

## 9. Revisione in chat (16 ottobre 2026), accettata da Ale

1. Ordine nella stessa corsa: prima 30 s a mani ferme, poi la guida; «dopo un colpo lungo» è una seconda corsa intera. Nessun ripristino dello stato (in `__sv` non esiste).
2. Nelle lezioni 1 e 2 il pilota non usa la voce «Andatura» (nascosta): legge la lancetta della rosetta con un errore di ±5°, obiettivi come nel testo. Verificato nel codice.
3. Contro-prova di «guidando» con una condizione resa sempre falsa.
4. «Ripartire» (osservazione 45) come contro-prova di «a mani ferme»; non è fra i passi in cui si aspetta.
5. Prova senza `#collaudo`: superata con entrambi i passi completati in 3 tentativi su 3.
6. `collaudo_carriera_intera.py` con la nuova tabella: dopo il rapporto, come passo a parte.

## 10. Esito della fermata 2 (16 ottobre 2026)

Fatto in `tests/collaudo_pilota_lezioni.py`. `index.html` non è stato toccato. **Uno scostamento dalla proposta:** il tempo limite di «Risalire il vento» è 180 s, non 120. Era scritto così nella tabella prima del primo lancio, ma la sezione 6 diceva «20-120».

**Messa a punto sui semi 1-20.** Si è corretto solo il pilota; le attese non sono cambiate. Ogni correzione è segnata nel codice:
- il passo «Ripartire» corregge se gira troppo, come dice il testo;
- un filetto si considera agitato o dritto solo se lo resta per mezzo secondo;
- nei passi di scotta, se il passo non si completa dopo 6 s, un altro piccolo colpo (al massimo 3 riprese, contate);
- in «Virare», se dopo l'attesa la barca è lenta, prima riprende velocità in bolina;
- il timone anticipa la rotazione: senza, il pilota oscillava fino a 40 °/s e i passi «prua ferma» non si completavano mai;
- se resta fermo nell'angolo morto, il pilota prima ne esce poggiando;
- il giocatore impreciso tiene i tasti anche **dopo** il completamento del passo. Senza questa correzione la contro-prova dell'osservazione 49 non scattava, perché il giocatore impreciso rilasciava nell'istante del completamento.

Alla fine della messa a punto, «guidando» completa tutti i 32 passi in tutti i 20 semi.

**Conferma sui semi 21-100, senza toccare il pilota.** «Guidando» completa 2.558 corse su 2.560. Le due mancate:
- «Barra sottovento: si orza», seme 81: la prua si è fermata a 70°, oltre la finestra 43-67°, dopo 3 riprese;
- «Strambata controllata», seme 66: finita a 125° con i filetti dritti, ma il passo non è stato dato per fatto, causa da capire.

Tempi in `tests/output/pilota_lezioni/rapporto_21-100.txt`.

**Cosa ha trovato** (semi 21-100; tra parentesi i semi 1-20):

| Passo | Misura | Volte | Cosa vuol dire |
| --- | --- | --- | --- |
| 1.9 Ripartire | dopo i 30 s a mani ferme | barca uscita dall'angolo morto in **80 su 80** (20 su 20), a 45° e 3,4-3,5 nodi | **Osservazione 45 confermata, con una precisazione:** la barca riparte da sola, ma il passo non si completa da solo, perché chiede il vento di fianco (70-105°). Il passo insegna a uscire dall'angolo morto poggiando, mentre il motore ne esce da solo |
| 1.9 Ripartire | dopo un colpo lungo | **27 su 80** (4 su 20), completato in 1,3 s | Chi tiene premuto troppo a lungo nel passo prima trova «Ripartire» già fatto |
| 2.4 Barra sottovento: si orza | dopo un colpo lungo | **3 su 80** (2 su 20), in 2,4 s | **Osservazione 49 riprodotta:** tenendo troppo «Barra a dritta», la prua sale già in bolina |
| 2.4 Barra sottovento: si orza | guidando | 25 riprese su 80 corse, 1 non completato | Il testo dice «a metà strada tra il rosso e l'orizzontale», cioè circa 65°, ma la finestra finisce a 67°: chi legge la lancetta con qualche grado di errore la supera |
| 2.5 Barra sopravento: si poggia | dopo un colpo lungo | 2 su 80 (0 su 20) | Come sopra, dal passo 2.4 |
| 1.11 La scotta: cazzare; 1.12 Troppo cazzata | dopo un colpo lungo | 2 e 4 su 80 (0 su 20), in 1 s | Tenendo troppo il tasto nel passo prima, la vela è già dove serve |
| 4.3 Accelerando | guidando | completato sempre, ma con **una ripresa in 80 corse su 80** (20 su 20) | Fermandosi ai primi filetti dritti, come insegna la lezione 1, la barca va a 3,7 nodi; il passo ne chiede più di 4, quindi bisogna cazzare ancora con i filetti già dritti |
| 6.2 Assorbire una raffica | a mani ferme | **56 su 80** (18 su 20), in circa 6 s | Il passo si completa senza lascare: con le raffiche moderate la barca resta sotto i 20° da sola. Non insegna il gesto che chiede |
| 6.3 La scuffia | a mani ferme | 18 su 80 (0 su 20, 2 su 20 dopo un colpo lungo), in circa 4,7 s | La raffica forte del passo fa scuffiare anche senza cazzare apposta |

**Contro-prove, tutte superate:**
- condizione di «Barra a sinistra» resa sempre falsa: «guidando» la segnala 3 volte su 3;
- condizione di «Traverso» resa sempre vera: «a mani ferme» la trova 3 volte su 3;
- osservazione 45 misurata (riga 1.9) e osservazione 49 riprodotta (riga 2.4);
- pagina senza `#collaudo`, tastiera vera, lezione 2 passi 2 e 3: completati in 3 tentativi su 3, e `window.__sv` non esiste.

**Quanto ha misurato:**
- 32 passi pratici;
- semi 1-20: 1.280 corse a mani ferme;
- semi 21-100: 5.120 corse a mani ferme;
- nessun errore della pagina.

Durata dei semi 21-100 nella sandbox: 2 minuti.

**Cosa non si è fatto:** nessuna correzione delle lezioni. Ogni riga della tabella diventa una proposta a parte, da decidere con Ale, perché tocca testi o condizioni. `collaudo_carriera_intera.py` con la nuova tabella è un passo a parte.
