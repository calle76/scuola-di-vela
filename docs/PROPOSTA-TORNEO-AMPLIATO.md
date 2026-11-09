# Proposta: torneo ampliato e vento vero (9 novembre 2026, riscritta lo stesso giorno)

Voce 2 di `DA-FARE.md`.

**Ale, 9 novembre:**
- «ampliare il torneo, ci sono regate con punti di penalità e aggiungiamo quelle con giri di penalità»;
- poi: «rispecchiare la realtà nei tornei che non sia didattica: i venti e raffiche sempre assieme … La parte fisica deve esserci sempre se non è didattica che insegna una cosa alla volta. Le altre cose: giri di penalità, punti di penalità, numero delle boe… scrivono il tipo di gara».

**Fermata 1: niente codice finché Ale non dà il via.**

## 1. La regola (da registrare in `DECISIONI.md`)

- **Didattica** (Scuola, prove, lezioni, regate a tema fuori dal torneo): una cosa alla volta, come oggi.
- **Non didattica** (il torneo, poi Deriva): la fisica c'è **tutta, sempre**.
  - Raffiche e salti di vento insieme.
  - Più avanti il cono d'ombra delle vele: è una proposta a parte, vedi `RICERCA-CONO-D-OMBRA.md`.
- **Che tipo di gara è** lo dice il **formato**, come in un bando: penalità sul punteggio o giri, percorso (bastone o triangolo), numero delle boe.

**Da confermare con Ale:** le regate a tema di Deriva fuori dal torneo («nelle raffiche», «nei salti di vento», «con i giri di penalità») restano didattiche. Servono ad allenare una cosa sola; il torneo è il banco vero.

## 2. Com'è oggi (letto nel codice, `js/regate.js`, sezione torneo)

- **Regate:** 4, sempre con la penalità sul punteggio (+1 contatto con colpa vale il 20% dei punti di chi non arriva, regola 44.3). La 1 e la 3 a bastone, la 2 e la 4 a triangolo.
- **Vento:** una condizione per regata: «10 nodi costanti», «raffiche» (12 nodi) oppure «salti di vento». La quarta è sorteggiata fra le tre.
  - Le raffiche girano già un po' il vento: fino a ±6° ciascuna, più un'oscillazione lenta di circa ±4,5°.
  - I salti sono un'altra cosa: una dozzina di gradi ogni due minuti circa, oppure una rotazione sempre dalla stessa parte (una regata su tre).
- **Le regate con i giri esistono già fuori dal torneo** (1.0.61-1.2.18), per il giocatore e per gli avversari:
  - due giri per un contatto con colpa;
  - un giro per la boa toccata (solo il giocatore);
  - squalifica per chi arriva coi giri non fatti.

**Nella realtà raffiche e salti vengono insieme:** spesso la raffica arriva con un cambio di direzione. Fonti: riviste di regata e un forum, secondarie:
- [Speed & Smarts](https://canadianboating.ca/sailing/racing/speed-smarts-go-for-puffs-in-light-air-shifts-in-breeze/)
- [Sailing World](https://www.sailingworld.com/racing/why-wind-shifts-matter-more/)
- [forum Daysailer](https://forum.daysailer.org/forum/viewtopic.php?p=33170)

## 3. Modello più semplice

**A. Vento: sempre raffiche e salti insieme.** In tutte e 4 le regate del torneo si accendono i due generatori che esistono già, senza costanti nuove. Da una regata all'altra cambia solo quello che cambia anche in un campo di regata vero:
- la forza del vento, sorteggiata fra 10 e 12 nodi (i due valori che il torneo usa già e su cui sono misurati gli avversari);
- il tipo di salto, oscillante o persistente (una su tre, come oggi).

Le tre condizioni con un nome spariscono dal torneo; restano per le regate a tema e le prove.

**B. Formato: è questo che distingue le regate.**

| Regata | Penalità | Percorso |
| --- | --- | --- |
| 1 | punteggio | bastone |
| 2 | punteggio | triangolo |
| 3 | giri | bastone |
| 4 | giri | triangolo |

- Prima i punti, poi i giri: ogni sistema di penalità si prova su entrambi i percorsi. Come oggi per il percorso, il formato dipende solo dal numero della regata.
- **Nelle regate coi giri:** si usa la regata dei giri che esiste già (regole, bandiere, avversari che scontano), senza penalità sul punteggio.
- **Squalifica** per giri non fatti: i punti di chi non arriva (5, come il ritiro; appendice A5.2).
- **Tabella:** un segno nuovo, «Sq».
- **Il punto di merito «senza penalità»** vale solo senza punti di penalità **e** senza giri da fare.
- La breve di ogni regata dice il formato («Regata 3 di 4: bastone, giri di penalità») e il vento del giorno.
- **Numero delle boe:** oggi il torneo ha due percorsi fissi. Cambiare i giri del percorso o aggiungere boe resta per dopo (è nel formato, ma allunga le regate e tocca la guida degli avversari alla boa 2). Questa proposta non lo fa.

**Cosa non si tocca:** la fisica della barca, chi cede, la guida degli avversari, lo scarto, la finestra d'arrivo, le regate fuori dal torneo, la Scuola.

**Rischi:**
- Con raffiche e salti insieme gli avversari potrebbero fare più contatti: nei salti fuori torneo +25% con la 1.2.19.
- Le regate coi giri durano di più.
- Un torneo salvato a metà con la versione vecchia deve finire con le sue regate: lo dice il campo `ver` già salvato.

## 4. Criteri (soglie nostre, scritte prima di misurare)

**Come si misura:**
- strumento: `misura_boa_avversari.py` esteso alle regate nuove;
- giocatore guidato dal pilota, principianti ed esperti;
- riferimento: il torneo di oggi, sugli stessi semi;
- soglie scelte sui semi 921-950, conferma sui semi 951-980.

**Soglie:**
- **T1, funziona:** `collaudo_torneo.py` verde, con casi nuovi:
  - regate 3 e 4 coi giri;
  - la squalifica vale 5 punti;
  - un torneo vecchio salvato a metà continua come prima;
  - la tabella mostra «Sq».
- **T2, squalifiche degli avversari** nelle regate coi giri: al massimo il 5% delle barche.
- **T3, durata:** arrivo mediano delle regate coi giri al massimo +15% rispetto alle stesse regate col punteggio.
- **T4, vento misto:** contatti dopo il via al massimo +15% rispetto al torneo di oggi; non arrivate non aumentano; fermate alla boa (`misura_boa_avversari`) al massimo +20%.
- **T5, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; regate fuori dal torneo invariate.
- **T6, pannello** a 1360x650 senza pixel in eccesso, con la tabella del torneo nel caso peggiore.

Se T4 non passa, il vento misto resta fuori e si riporta perché: prima si correggono gli avversari.

## 5. Cosa serve da Ale

1. **Il via** (o un altro ordine delle regate).
2. **Le regate a tema fuori dal torneo restano didattiche?** (§1)
3. **Visibile subito o nascosto?** Il torneo oggi si apre nella Scuola, dopo l'attestato, e la decisione del 4 novembre vuole il lavoro di Deriva nascosto. Raccomando di cambiarlo per tutti, come versione 1.2.21: è il torneo che diventerà quello di Deriva, e le regate di Ale e Lucio lo provano subito.

## 6. Costo

Circa mezza giornata di codice, testi e collaudo, più circa 2 ore di calcolo col termostato.

## 7. Fermata 2: adottata nella 1.2.21 (via di Ale, 9 novembre: «via, didattiche sì, torneo per tutti»)

Misura: 4 regate del torneo nuovo (240 per gruppo di semi) e, per T3, le regate 3 e 4 senza giri (120 per gruppo). Il riferimento è il torneo della 1.2.20 (360 regate per gruppo, copia del tag `v1.2.20`).

| | semi 921-950 | semi 951-980 | soglia |
| --- | --- | --- | --- |
| T2 avversari squalificati, regate coi giri | 5 su 360 (1,4%) | 1 su 360 (0,3%) | ≤5% |
| T3 arrivo mediano, giri contro punteggio (bastone / triangolo) | +2,1% / +2,2% | +2,6% / +1,4% | ≤+15% |
| T4 contatti per regata (1.2.20 → nuovo) | 0,708 → 0,525 | 0,497 → 0,542 (+9%) | ≤+15% |
| T4 fermate alla boa per regata | 0,042 → 0,025 | 0,089 → 0,062 | ≤+20% |
| T4 non arrivate | 0 → 0 | 0 → 0 | non aumentano |

T1: `collaudo_torneo.py` (casi nuovi C12, squalifica in C1, «Sq» in C6). T5: `polare.js`, `raffiche_e_virate.js` identici, `impronta1b.js` al bit. T6: C6 senza pixel in eccesso.

**Differenza dalla proposta:** il §3 diceva che un torneo salvato a metà con la versione vecchia avrebbe finito le sue regate. Il gioco invece, già prima, a ogni cambio di versione chiude il torneo in corso senza punti e lo dice (`torApri`). Si è lasciato così, senza codice in più.

**Note:**
- I due gruppi del riferimento differiscono molto fra loro (contatti 0,708 contro 0,497 per regata): con 30 semi il caso pesa.
- Il pilota non fa i giri: nel collaudo la barca del giocatore guidata dal pilota è spesso squalificata nelle regate 3 e 4. Gli avversari invece li fanno.
- Boe sbagliate: 2 nel torneo nuovo sui semi 921-950, 0 nel riferimento. Non c'era soglia; lo si riporta.
