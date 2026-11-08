# Proposta: i giri di penalità del giocatore che non vengono contati (fermata 1)

**8 novembre 2026, su `main` (1.2.15). Fermata 1: nessuna riga del gioco cambiata.** Ale: «vai con la 1, cerca nei regolamenti se si parla di tempistiche e modalità, anche su internet». Osservazione 98 (regata dei giri delle 10:03).

## 1. In breve

Oggi un giro di penalità conta solo se si chiude entro **20 secondi** (`GIRO_MAX_S`), contati con una finestra che scorre. Il regolamento non mette nessun limite in secondi: chiede che i giri si facciano «prontamente». Nella regata delle 10:03 Ale ha fatto un giro intero in 23 s, perché la barca era quasi ferma, e il gioco non l'ha contato. Proposta: **nessun limite di durata; il giro riparte da capo se la prua smette di girare per più di 8 secondi o se torna indietro di oltre 20°**. In più, il gioco dice quando un giro è interrotto e quanto ne manca.

## 2. Cosa dicono le fonti

**Regolamento (F15, regola 44.2; F39, stessa regola in italiano; parafrasi):** dopo l'incidente la barca si allontana bene dalle altre il prima possibile, poi fa **prontamente** il numero di giri richiesto, **nello stesso verso**, e ogni giro comprende **una virata e una strambata**. Se la penalità si fa vicino alla linea d'arrivo, lo scafo deve essere tutto dalla parte del percorso prima di arrivare. **Nessun limite in secondi, né per un giro né fra un giro e l'altro.**

**Regola 21.2 (F15):** chi sta scontando una penalità si tiene discosto da chi non la sta scontando. Il gioco la applica già (`sconta`, 1.0.66).

**Commento al regolamento** (fonte nuova F74, letta: estratto del libro di Dave Perry, *Understanding the Racing Rules of Sailing through 2028*, US Sailing, PDF https://ussailing.org/wp-content/uploads/2024/12/44.2.pdf; parafrasi):
- prima ci si allontana dalle altre barche, subito, non a metà del lato; fino a quando non si cominciano davvero i giri valgono i diritti normali;
- non è detto che un giro debba seguire l'altro senza pausa: è accettabile riprendere velocità dopo il primo giro per fare bene il secondo;
- mentre si gira ci si tiene discosti dalle altre barche (21.2);
- non c'è tempo per pensarci: chi aspetta prima di cominciare i giri può essere squalificato (cita l'appello US 60);
- i giri sono finiti con l'ultima virata o strambata.

**Trovato con la ricerca ma non letto direttamente** (le pagine rifiutano i programmi; li riporto come indizi, non come fonti):
- caso 149 di World Sailing: fermarsi durante i giri solo per il tempo che serve a rispettare la 21.2 vale ancora come «prontamente»;
- Q&A 2019.019 di World Sailing: chi ritarda la penalità non rispetta la 44.2, e l'unica cosa da fare è ritirarsi;
- in un forum un giudice scrive che una sosta di circa 20 s, per una deriva a 4 nodi, è un'interruzione sostanziale. È un'opinione, non una regola.

**Cosa ne ricavo:** «prontamente» vuol dire senza fermarsi e senza perdere tempo, non «entro N secondi». Un giro lento, perché la barca ha poco vento o si pianta, è ancora un giro. Un giro lasciato a metà per navigare dritto no.

## 3. Cosa succede oggi (letto nel codice, misurato sul file di Ale)

`giriPenalita` (`js/regate.js`) tiene la rotazione degli ultimi 20 s. Il giro conta se in quei 20 s la prua ha girato di 360° nello stesso verso, senza tornare indietro di oltre 20°, con almeno una virata e una strambata. Il messaggio dice «nello stesso verso, ciascuno con una virata e una strambata», ma non dice né del tempo né quando un giro è perso.

Strumento nuovo `tests/misura_giri_giocatore.py`: rifà il conto sul file di una regata. **Controllo dello strumento:** con la regola di oggi trova i giri a 227,1 e 239,9 s; il gioco li ha contati a 227,13 e 239,85 (eventi `giro_penalita` del file).

Regata delle 10:03 (debito di due giri dal contatto a 106,6 s):
- **Da 135 a 158 s** Ale gira di 360° nello stesso verso, con una virata (142,5) e una strambata (157,4). Ci mette 23 s perché fra 143 e 150 la barca va a 0,4 nodi. **Oggi non conta.**
- Da 158 a 176 s comincia il secondo giro, si pianta nell'angolo morto dopo la virata (164,3; fino a -2,9 nodi all'indietro) e smette di girare a 176 s.
- Da 214 a 240 s fa due giri da 13 s: penalità scontata a 240 s.

## 4. Il modello più semplice

In `giriPenalita`, al posto della finestra di 20 s, **un giro in corso**:
1. il giro comincia quando la prua ha girato di 5° in un verso; quello è il verso del giro;
2. **riparte da capo** se la prua torna indietro di oltre `GIRO_VERSO` (20°, come oggi) o se **non avanza di almeno 5° per più di `GIRO_SOSTA` = 8 s**;
3. conta quando arriva a 360° e, **da quando è cominciato**, ci sono state almeno una virata e una strambata;
4. il resto come oggi: un secondo giro nel verso opposto fa ricominciare la penalità; i giri si contano solo dopo il contatto; la scuffia azzera.

Regola 21.2 (`sconta`): comincia quando il giro in corso arriva a `GIRO_INIZIO` (120°, come oggi) e finisce quando il giro riparte da capo o la penalità è scontata. Oggi finiva dopo 20 s senza chiudere un giro.

**Messaggi**, nella riga delle regole del pannello che c'è già (nessun pixel in più) e con i messaggi a comparsa che ci sono già:
- durante il giro, ogni 90°: «Giro in corso: 180° di 360°; virata fatta, strambata da fare»;
- giro ripartito da capo dopo almeno 120°: «Giro interrotto: ricomincia, stesso verso, senza fermarti»;
- nel messaggio del debito si aggiunge «senza fermarti».

**Cosa non cambia:** gli avversari (`giroAI` conta già i giri senza limite di tempo e si ferma solo se una barca si avvicina), il +15 s per giro non fatto, il resto della regata.

**Misura sul modello** (con `misura_giri_giocatore.py`, che rifà il modello proposto):
- 10:03: giri a **158,0 s** e 227,1 s: la penalità sarebbe stata scontata a 227 s invece che a 240 s. Il giro da 135 a 158 conta; il secondo, piantato e lasciato a metà, no.
- Sosta massima da 5 a 15 s: sul caso di Ale dà lo stesso risultato. La sosta più lunga che c'è nel suo secondo giro, piantato, è di circa 6-7 s.
- **Giri trovati senza nessuna penalità vera** (17 regate di Ale, come se avesse sempre un debito aperto: sono i cerchi completi fatti prima del via, giri veri ma non penalità): regola di oggi 3; modello con sosta 5 s: 1; con 8 s: 2; con 10 s: 3; con 15 s: 6. Con 8 s il modello non ne trova più di oggi.

## 5. Criteri (soglie nostre, scritte prima di implementare)

- **G1, ciò che va già:** `collaudo_giri.py` (parti A-H, 30 prove) tutte verdi come oggi; il costo di due giri (parte A) cambia al massimo di 1 s nella mediana.
- **G2, giro lento:** due giri fatti dal pilota a barra metà, che durano 25-35 s ciascuno, senza soste: **contano 10 su 10** (oggi ci si aspetta 0 su 10).
- **G3, sosta breve:** un giro con 5 s di barra al centro a metà (dopo la virata): **conta 10 su 10**.
- **G4, sosta lunga:** un giro con 15 s di barra al centro a metà: **non conta, 10 su 10**. È la prova che il controllo può dire di no.
- **G5, giro all'indietro:** un giro che a metà torna indietro di 40°: non conta, 10 su 10 (come oggi).
- **G6, strumento uguale al gioco:** sulle registrazioni delle prove G2-G5, `misura_giri_giocatore.py` trova gli stessi giri, entro 0,5 s, degli eventi `giro_penalita` del gioco.
- **G7, i file di Ale:** sul file delle 10:03, il gioco rigiocato non serve; lo strumento dà 158,0 e 227,1 (riportato, non è una soglia). Giri senza penalità vera nelle 17 regate: non più di oggi (3).
- **G8, pannello:** il testo più lungo dei messaggi nuovi entra nella riga delle regole a 1360x650 senza pixel di eccesso (`collaudo_pannello` o il collaudo che misura quella riga).
- **G9, niente altro cambia:** `collaudo_regola21.py` e `collaudo_riquadro_bandiere.py` verdi; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; avversari invariati (il loro codice non si tocca).
- **G10, pagina come la carica un giocatore:** parte H di `collaudo_giri.py` (senza `#collaudo`).

## 6. Costanti nuove

- `GIRO_SOSTA = 8` s: sosta massima senza girare. **Ipotesi nostra**: poco sopra la sosta più lunga del giro piantato di Ale (6-7 s), sotto i 20 s che un giudice in un forum chiama interruzione sostanziale; con 8 s non si trovano più giri senza penalità che oggi. Sostituisce `GIRO_MAX_S` per i giri.
- `GIRO_AVANZA = 5`°: sotto questa rotazione la prua «non avanza» (onde, piccole correzioni). Ipotesi nostra.

## 7. Rischi

- **Giri che si sommano a pezzi:** chi gira piano, con soste di 7 s, potrebbe fare un giro in un minuto. Il regolamento non lo vieta in secondi, ma non sarebbe «prontamente». Lo accettiamo come semplificazione dichiarata: nel gioco nessuno ha interesse a girare piano.
- **Un giro preso da una manovra normale** (una boa con strambata e poi una virata nello stesso verso): può succedere oggi e succederà ancora. G7 controlla che non aumenti.
- **Il testo nel pannello:** la riga è corta; G8.
- **La regola 21.2 dura di più per chi gira piano:** in quel tempo deve tenersi discosto da tutti. È quello che dice la regola.

## 8. Fonti

F15 (44.2, 21.2), F39 (44.2 in italiano), F74 nuova (Perry, US Sailing). Caso 149, Q&A 2019.019 e il forum solo come indizi, non letti direttamente.

## 9. La lezione sui giri di penalità (richiesta di Ale, 8 novembre)

Ale: «c'è da correggere la spiegazione nella lezione dedicata ai giri di penalità». Lezione 20, passo «I giri di penalità» (`js/contenuti.js`, `LD7`). Il testo di oggi dice che un giro vale «se in venti secondi la prua fa un giro intero». Descrive la regola di oggi, ma con il modello del §4 diventa sbagliato. In più non dice che un giro lento o interrotto ricomincia da capo, che è proprio quello che è successo ad Ale. Si cambia **insieme alla regola**, nella fermata 2 (cambiare solo il testo lascerebbe la lezione diversa dal gioco).

**Terzo paragrafo del passo, nuovo:**
> Nel gioco un giro vale quando la prua fa un giro intero nello stesso verso e, durante il giro, fai una virata e una strambata. Non c'è un tempo massimo, ma non ci si ferma: se la barca smette di girare per più di otto secondi, o torna indietro, quel giro ricomincia da capo. Il pannello ti dice a che punto sei. I giri non fatti, all'arrivo, costano quindici secondi l'uno: nel regolamento non c'è, è una scelta del gioco.

**Esercizio «Tocca la boa e fai il giro»**, consegna: dopo «girando sempre nello stesso verso» si aggiunge «senza fermarti a metà».

**Riepilogo:** invariato (dice già «subito, nello stesso verso, ognuno con una virata e una strambata»).

Anche il commento in testa alle lezioni del livello 2a (`js/contenuti.js`, «un giro vale con 360° nello stesso verso in 20 s») si aggiorna.

**Criteri in più:**
- **G11:** il passo e la consegna entrano nel riquadro della lezione a 1360x650 senza pixel di eccesso (il collaudo delle lezioni che misura il riquadro);
- **G12:** l'esercizio «Tocca la boa e fai il giro» si completa ancora guidando la barca (`collaudo_esercizi_regata.py`).

Nessuna fonte nuova: «prontamente» e «nello stesso verso, una virata e una strambata» sono F15 44.2; gli otto secondi e i quindici secondi sono scelte del gioco, e il testo lo dice.

## 10. Squalifica per i giri non fatti (decisione di Ale, 8 novembre)

Ale: «allora metti la squalifica», dopo aver letto cosa succede nella realtà. Nella realtà chi non sconta può essere protestato e, all'udienza, viene **squalificato dalla prova** (F15, 60.2 e 60.5(c)); chi ha già fatto i giri non viene punito di nuovo (60.5(c)(2)). Registrata in `DECISIONI.md`: chiude il «da decidere» di `REGOLE-DI-REGATA.md`.

**Modello (semplificazione dichiarata: nel gioco non ci sono proteste né udienze; la squalifica arriva sempre e subito, all'arrivo):**
- chi taglia l'arrivo con giri di penalità ancora da fare è **squalificato (DSQ)** al posto dei +15 s per giro (`GIRO_SEC` non serve più);
- **in classifica** sta dopo tutte le barche arrivate, insieme a quelle non arrivate: nel punteggio vero DSQ e non arrivata prendono gli stessi punti (appendice A, A5.2). La riga dice «squalificata: giri di penalità non fatti»;
- **il giocatore squalificato:** nessun record, nessun fantasma, nessun piazzamento salvato; il messaggio d'arrivo dice «Squalificato: non hai fatto i giri di penalità (regole 44.2 e 60.5)». Nell'elenco delle penalità: «Tu, giri di penalità non fatti (2): squalifica»;
- **dove vale:** solo nelle regate con i giri (`R.giri`): la «Regata con i giri di penalità» e gli esercizi della lezione 20. Nel torneo la penalità resta +1 punto, nelle altre regate +15 s;
- **lezione 20, terzo paragrafo** (al posto della frase sui quindici secondi): «I giri non fatti, all'arrivo, ti squalificano dalla prova, come nella realtà dopo una protesta.»

**Gli avversari: misura** (`misura_avversari.py 361 380 3`, regata con i giri, Chromium, principianti ed esperti, 40 regate, gioco di oggi): 58 colpe degli avversari, 46 penalità scontate, **26 avversari su 120 arrivati con giri non fatti (22%; 0,65 a regata)**. Con la squalifica per tutti, quasi due regate su tre avrebbero un avversario squalificato, quasi sempre perché in gruppo non trova mai 4 lunghezze libere (osservazione 99), non per scelta.

**Da decidere con Ale (una cosa sola):**
- **A.** Squalifica subito anche per gli avversari: coerente, ma un avversario su cinque squalificato finché la 99 non è sistemata.
- **B.** Squalifica subito per il giocatore; per gli avversari restano i +15 s, **dichiarato come provvisorio**, e passano alla squalifica con la proposta sull'osservazione 99 (gli avversari che riescono a fare i giri anche in gruppo), con soglia: avversari arrivati con giri non fatti sotto il 5%.
- **C.** Squalifica per tutti, ma solo quando anche la 99 è fatta: per ora resta tutto com'è.

Consiglio **B**: la squalifica del giocatore si può fare subito con la regola nuova del §4, che rende i giri possibili anche a chi è lento; quella degli avversari ha bisogno prima che il gioco li lasci girare.

**Criteri in più:**
- **G13:** arrivo con due giri non fatti (parte E di `collaudo_giri.py`, oggi +15 s per giro): risultato «squalificato», ultima in classifica, nessun record salvato; con i giri fatti: arrivo normale (parte A);
- **G14:** le altre regate e il torneo non cambiano (parte F di `collaudo_giri.py`, confronto al bit);
- **G15:** il messaggio d'arrivo più lungo entra nel riquadro a 1360x650.

## 11. Fermata 2, prima prova (8 novembre 2026): **non tutto verde, codice non committato**

Ale: scelta B (squalifica per il giocatore, avversari +15 s per ora); il suo «ok» preso come via. Fatto in `js/regate.js` (giro in corso con `GIRO_SOSTA` 8 s e `GIRO_AVANZA` 5°, squalifica, riga nel riquadro), `js/registratore.js` (stato `dsq`), `js/contenuti.js` (lezione 20 e consegna dell'esercizio). Collaudo dei giri esteso: parte E alla squalifica, E3, L2-L5, M1.

**Verdi:** `collaudo_giri` A1 (30/30, costo di due giri 17,5 s, uguale a prima), B1, P1-P2, C1, D1-D3, E1-E2 (squalifica, messaggio, nessun secondo in più), **L2** (giri lenti da 27 s circa: 10/10), **L3** (sosta di 5 s a metà giro: 10/10), **L5** (40° indietro: 10/10), F1 (altre regate identiche al bit), G1, H1-H3; `collaudo_regola21`, `collaudo_riquadro_bandiere`, `collaudo_pannello` (90 misure), `collaudo_pannello_lezioni`, `collaudo_esercizi_regata`; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

**Non verdi:**
- **K1 (giri spuri), 2 regate su 30** (oggi 0). Il pilota di prova, che non riesce a girare la boa, ci fa un cerchio intero attorno: 360° nello stesso verso con una strambata e una virata, e in mezzo circa 5 s dritto (seme 825, da 118 a 144 s). È un giro vero, non voluto. La regola di oggi non lo contava solo perché durava più di 20 s. **Fuori dal criterio G1.**
- **L4 (sosta di 15 s non deve contare), 5 su 10.** Con la barra al centro la barca continua a girare piano nello stesso verso (da 2°/s a 0,5°/s; seme 941: da 129° a 100° in 15 s), e ogni 5° conta come «la prua avanza»: il giro non riparte mai. Nell'altro verso la barca si ferma e la regola funziona. **La soglia di 5° è troppo piccola** (costante nostra, §6).
- **M1 (strumento uguale al gioco), 28 su 40; E3, 0 casi.** Difetti del collaudo, non del gioco: la prova si fermava nell'istante del giro, prima della riga registrata (corretto: 2 s dritti dopo), e il filtro di E3 leggeva il debito già chiuso all'arrivo (corretto). Da rimisurare.

**Cosa propongo (cambio dopo aver visto i numeri, da decidere con Ale):** `GIRO_AVANZA` da 5° a **20°** in 8 s, cioè la prua «avanza» se gira almeno 2,5°/s. Lo strumento, solo come informazione: sul file delle 10:03 dà gli stessi giri (158,0 e 227,1); giri senza penalità vera nelle altre 16 regate di Ale: 5° → 2, 20° → 1. Poi tutto si rimisura, L4 compreso, su semi nuovi. K1 resta da decidere a parte: un cerchio vero attorno alla boa, con la regola nuova, conta come giro; secondo me è giusto (lo è anche nella realtà), ma il criterio K1 andrebbe riscritto per dirlo, e questo è un cambio di criterio.

**Stato:** `js/regate.js`, `js/registratore.js`, `js/contenuti.js`, `tests/collaudo_giri.py` e `tests/misura_giri_giocatore.py` modificati e **non committati**; `VERSIONE` e `CHANGELOG.md` non toccati (la versione non è chiusa).
