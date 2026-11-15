# Proposta: gli sponsor a contratto (fermata 1)

14 novembre 2026, notte. Tappa 4 di `PIANO-CHIUSURA-DERIVA.md`. **Solo proposta: in `js/` niente finché Ale non dà il via.**

Decisioni già prese da Ale la stessa notte (`DECISIONI.md`): niente retrocessione automatica; lo sponsor si sceglie fra le offerte e decide il circuito; contratti con durata e obiettivi; andando male arrivano sponsor minori, andando bene rinnovo, proposte migliori o il salto al Fiocco; sotto lo zonale non c'è niente; lo sponsor non dà materiale; lo sponsor del Fiocco arriva a chi finisce fra i primi 3 del nazionale.

## Modello più semplice

**Solo in carriera.** Nel gioco libero tutto resta aperto e gli sponsor non ci sono (principio 2).

**I gradini** (nomi provvisori):

| Gradino | Circuito | Esempio di obiettivi |
| --- | --- | --- |
| 1, zonale piccolo | zonale | finire la stagione senza ritirarsi; un podio di tappa |
| 2, zonale | zonale | primi 5 dello zonale; davanti a un rivale nominato |
| 3, nazionale | nazionale | primi 8 del nazionale |
| 4, nazionale grande | nazionale | primi 5 del nazionale; un podio di tappa |
| sopra | Fiocco | l'offerta arriva con i primi 3 del nazionale, a qualsiasi gradino (decisione di Ale) |

**Il contratto:** sponsor (nome inventato), gradino, circuito, durata di **1 o 2 stagioni**, **1-3 obiettivi** presi da un elenco fisso, tutti verificabili sui dati già salvati:
- posto finale nella classifica del circuito al massimo N;
- almeno un podio di tappa;
- nessun ritiro da una tappa;
- finire davanti a un rivale nominato;
- (con la finale) podio o vittoria in finale.

Un contratto di 2 stagioni ha obiettivi più facili per stagione: si sceglie fra sicurezza e libertà.

**Fine contratto:**
- tutti gli obiettivi raggiunti, in ogni stagione: offerta di **rinnovo** e offerte del **gradino sopra**;
- raggiunti in parte: offerte dello **stesso gradino**;
- nessuno: offerte del **gradino sotto**, mai sotto il gradino 1;
- sempre almeno 2 offerte, di cui almeno una zonale.

**Inizio:** la prima stagione zonale si corre senza sponsor. Alla fine: fra i primi 3 (il diritto al nazionale, Deriva superata) arrivano offerte dei gradini 2 e 3; altrimenti dei gradini 1 e 2.

**Cosa cambia rispetto a oggi:** dalla 1.2.39 il diritto al nazionale, una volta preso, resta per sempre. Con gli sponsor si corre il nazionale solo con un contratto nazionale. I salvataggi con il diritto già preso partono con un'offerta del gradino 3 da accettare.

**Nomi degli sponsor:** inventati e generici (una ditta di vele, un cantiere, un circolo), senza marchi veri (principio 5), cercati nome per nome come per i rivali. **[da verificare]**

## Criteri (soglie nostre, scritte prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| S1 | Gli obiettivi dicono il vero | 200 stagioni con risultati scritti dal collaudo: ogni obiettivo «raggiunto» o «mancato» ricontrollato sui dati salvati, 0 errori |
| S2 | I gradini seguono la regola | le stesse stagioni: ogni passaggio di gradino è quello della tabella, 0 errori; mai sotto il gradino 1; sempre almeno 2 offerte, una zonale |
| S3 | Obiettivi né impossibili né regalati | per ogni tipo di obiettivo, giocatore a forza 0 a numeri (come N8 del nazionale), 2000 stagioni: raggiunto fra il 20% e l'80% delle volte |
| S4 | Il Fiocco arriva quando deve | primi 3 del nazionale: offerta presente, 200 su 200; altrimenti mai |
| S5 | Salvataggio | ricarica a metà contratto: uguale; «Azzera i progressi» lo cancella; un salvataggio della 1.2.39 col diritto si apre con l'offerta del gradino 3 |
| S6 | Le regate non cambiano | impronta del guardiano, `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici |
| S7 | Pannello e browser | 0 px di eccesso a 1360×650 con 3 offerte e 3 obiettivi; Chromium e Firefox senza `#collaudo`, 0 errori |

## Costanti nuove (nostre, senza fonte)

I 4 gradini, le soglie degli obiettivi (posti 5 e 8), il numero di offerte, la durata massima di 2 stagioni. Gli sponsor e i loro contratti sono **invenzione del gioco**: le fonti lette (F88, F89) parlano di circuiti e classifiche, non di come funzionano gli sponsor dei velisti. Va detto nel gioco con una riga.

## Rischi

- **Un contratto di 2 stagioni ti tiene nel circuito** anche se vai benissimo: è voluto (sicurezza contro libertà), ma va detto chiaro nell'offerta.
- **Tanti testi nuovi** (offerte, obiettivi, esiti): rischio di finestre piene. S7 lo misura.
- **S3 a numeri** dice poco su chi gioca davvero: in acqua il giocatore non è «forza 0». Le soglie si riguardano dopo le prove a mano di Ale e Lucio.

## Risposte di Ale (15 novembre 2026)

Via dato, da fare dopo le tappe 2 e 3. Solo in carriera. I nomi degli sponsor li propone Claude con la ricerca, Ale li controlla.

## Cosa serviva da Ale

1. Il via.
2. Va bene il **solo in carriera**?
3. I nomi degli sponsor li propongo io, con la ricerca, e tu li controlli?

## Idea di Ale (15 novembre 2026, pomeriggio): lo sponsor come figura

«Ci vorrebbe un'altra figura, lo sponsor... più avanti, che possa giudicare il risultato dei punti e la classifica e l'andamento in generale, per capire se il contratto si sta rispettando o se la fiducia sta per calare. Per ora no.» Come il Coach giudica la regata, lo sponsor giudicherebbe la stagione: punti, classifica, andamento rispetto agli obiettivi del contratto, con una «fiducia» che sale o scende. **Non adesso**: da riprendere con la tappa 4, partendo da questa proposta.
