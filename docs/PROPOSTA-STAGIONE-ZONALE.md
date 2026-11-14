# Proposta: la prima stagione del circuito zonale (fermata 1)

14 novembre 2026, pomeriggio. Ale: «restiamo sul livello deriva sviluppandone carriere e regate e rapporti tra regatanti … facciamo maturare un bel livello che poi farà da base per quelli successivi» (`DECISIONI.md`). Mette insieme pezzi già proposti e mai fatti:
- rivali che vivono anche quando non giochi (`PROPOSTA-RIVALI-E-SPONSOR.md` §6);
- circuito zonale e nazionale (§11);
- carriera in profondità con una barca (§16);
- storia e conseguenze dei rivali (`DA-FARE.md` voce 35).

In `js/` non è stato scritto niente.

## Cosa c'è oggi

- **Il torneo** sono 4 regate contro 3 rivali presi fra 10 (1.2.33), ognuno con i suoi tratti fissi.
- **Lo storico** sono i fatti delle regate con te (partenza, boa 1, contatti), solo mostrati (1.2.30).
- **Non c'è una stagione:** ogni torneo finisce lì, senza classifica fra un torneo e l'altro.
- **I rivali non si incontrano mai fra di loro** fuori dai tuoi tornei.

## Modello più semplice

**1. La stagione = 4 tappe.**
- Ogni tappa è un torneo come oggi: 4 regate, tu più 3 rivali in acqua.
- Ogni tappa ha un nome di posto inventato e un vento suo, da leggero a medio (10 o 12 nodi), come oggi.

**2. A ogni tappa corre tutta la flotta, a numeri.**
- I 10 rivali e tu siete nella classifica del circuito. In acqua, con te, ce ne sono 3.
- Gli altri 7 corrono la stessa tappa **a numeri**: per ogni rivale una «forza» presa dai suoi tratti (partenza e bolina: dote +1, media 0, difetto −1), più un sorteggio.
- L'ordine d'arrivo della tappa mette insieme le due cose. La tua posizione vera e quella dei tuoi 3 rivali in acqua restano quelle della regata; gli altri 7 si inseriscono intorno, secondo la loro forza rispetto a quella dei 3 che hai incontrato.
- Il modello è quello del §6 (Plackett-Luce: estrazioni pesate dalla forza, una per volta, senza ripetizioni). Costa poco e non tocca la fisica né la guida.

**3. La classifica del circuito.**
- Punti per piazzamento in ogni tappa, uguali per tutti: 1° 1 punto, 2° 2, … (il «punteggio minimo» delle classifiche di vela). **[da verificare]** su una fonte scritta: F89 parla di ranking e regate zonali, ma non l'ho letta per intero su questo punto.
- Dopo 4 tappe vince chi ha meno punti.
- **Promozione:** i primi 3 a fine stagione hanno «diritto al nazionale». In questo primo passo è solo scritto, perché il nazionale non esiste ancora: sarà il passo dopo.

**4. I rapporti fra regatanti: lo storico fra tutti, in frasi.**
- Per ogni coppia, compresa la tua, si contano: tappe insieme, chi è arrivato davanti, contatti e di chi era la colpa (solo per le regate in acqua; quelle a numeri non hanno contatti).
- Dopo ogni tappa il gioco può scrivere al massimo **tre frasi**, scelte fra poche regole fisse:
  - «**la tua bestia nera**: Fontana, davanti a te in 3 tappe su 3»;
  - «**con Brunelli** ti sei toccato in 2 regate, sempre colpa sua»;
  - «**Pavan e Serafini** si giocano il secondo posto del circuito»;
  - «**Gallo** è in forma: tre podi di fila».
- Sono frasi su fatti contati, non giudizi inventati.

**5. Conseguenze: in questo passo nessuna in acqua.**
- I rivali guidano come oggi. Il §6 lo lasciava aperto, e cambiare la guida per lo storico tocca gli avversari, che vanno misurati a parte.
- Le conseguenze di questo passo sono di carriera: classifica, diritto al nazionale, frasi.
- Il comportamento («ti sta più lontano», «ti cerca») è un passo successivo, con una sua proposta.

**6. Dove si vede.**
- Nella finestra del torneo, a fine tappa, la classifica del circuito (11 righe) con le tre frasi.
- Nella scheda di ogni rivale, la sua posizione nel circuito.
- Il salvataggio sta con i progressi, separato fra carriera e gioco libero come il gruppo dei rivali. «Azzera i progressi» lo cancella.

## Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| Z1 | Le tappe a numeri rispettano la forza: 2000 stagioni simulate a numeri, senza correre | i rivali con dote in tutte e due le aree finiscono in media davanti a quelli con difetto in tutte e due; ognuno dei 10 vince almeno una stagione su 200 (nessuno è condannato) |
| Z2 | La tua posizione vera e quella dei 3 rivali in acqua restano nell'ordine della regata | in 20 tappe corse col pilota: 20 su 20 |
| Z3 | La classifica del circuito torna coi conti | somma dei punti di ogni tappa = 1 + 2 + … + 11 = 66, in ogni tappa; vince chi ha meno punti |
| Z4 | Le frasi dicono il vero | per ogni frase scritta, il fatto contato coincide con lo storico salvato: 0 frasi false in 20 stagioni; almeno una frase in 18 stagioni su 20 (il metro misura) |
| Z5 | Salvataggio | ricaricando la pagina a metà stagione: classifica, tappa e storico uguali; «Azzera i progressi» li cancella |
| Z6 | Le regate non cambiano | impronta del guardiano identica al bit, `polare.js` e `raffiche_e_virate.js` identici: si aggiunge solo ciò che sta intorno alla regata |
| Z7 | Pannello e browser | 0 px di eccesso a 1360×650 con la classifica di 11 righe; Chromium e Firefox senza `#collaudo`, 0 errori |

## Costanti nuove (nostre, senza fonte)

- 4 tappe per stagione;
- forza = somma dei tratti, più un sorteggio con un peso da scegliere in Z1 su semi fissi e confermare su altri;
- i primi 3 hanno diritto al nazionale;
- al massimo 3 frasi per tappa.

## Fonti

F89 (regate zonali e ranking; il punteggio minimo è da verificare), F88 (promozioni nelle leghe). Le frasi sono testo nostro.

## Rischi

- **Tappe a numeri contro tappe in acqua:** i 3 rivali in acqua sono più deboli o più forti di quanto dica la loro forza a numeri, perché la guida vera dipende da vento e incontri. Inserire gli altri 7 rispetto a quei 3 tiene il conto onesto, ma va controllato che non nascano classifiche assurde, come un rivale con difetti che vince tutto. Lo controlla Z1.
- **La stagione è lunga:** 16 regate. Va bene salvare a metà (Z5). Si può scegliere una stagione corta (2 tappe) per provarla.
- **Il gruppo bilanciato della 1.2.33** dice che 3 rivali su 10 hanno una dote per area: la classifica rispecchierà quei tratti. È voluto: sono i rivali «forti» del circuito.

## Cosa serve da Ale

1. Il via.
2. Tre scelte:
   - 4 tappe, oppure 2 per provarla;
   - i nomi delle tappe li scrivo io, posti inventati, oppure li scrivi tu;
   - le frasi le propongo io in una lista che controlli tu, come per i nomi dei rivali.

## Aggiunta (14 novembre, sera): Lucio nella stagione

Ale: «aggiungere Lucio alla stagione». Lucio diventa il **dodicesimo della flotta del circuito**. Non lo si incontra mai in acqua, come nei circuiti veri, dove le classifiche sommano regate corse in giorni diversi.

**Come funziona.**
- **Una stagione «con un amico»** nasce da un codice comune (`PROPOSTA-TORNEI-ONLINE.md`). Il codice fissa le 4 tappe, il loro vento e il gruppo dei 10 rivali con i loro tratti: Ale e Lucio hanno la stessa flotta.
- **Ognuno corre le sue tappe quando vuole**, con 3 rivali in acqua. I 3 rivali possono essere diversi per i due: dipende dal sorteggio di ciascuno.
- **A fine tappa si scambia un file piccolo:** posizione, tempo, i 3 rivali incontrati e la registrazione. Va bene un messaggio o la posta: niente server, nessun dato personale fuori.
- **Nella classifica del circuito Lucio entra col suo risultato vero**, non a numeri, e lo stesso Ale nella stagione di Lucio. I rivali vengono messi in fila così:
  - quelli in acqua con Ale restano nell'ordine della regata di Ale;
  - quelli in acqua con Lucio nell'ordine della regata di Lucio;
  - gli altri, a numeri, intorno a loro.
- **Se un rivale era in acqua con tutti e due**, il suo piazzamento è quello della regata di chi tiene la classifica, così ognuno ha una classifica coerente. Le due classifiche possono differire di poco, e lo si dice.
- **Ale contro Lucio, nella stessa tappa:** conta il piazzamento nella propria regata, e a pari piazzamento il tempo. Se avete corso con lo stesso vento, la barca dell'altro si può rivedere come fantasma in moviola.
- **Se Lucio non ha ancora corso una tappa**, la classifica lo mostra «in attesa»: niente punti finché non arriva il suo file.
- **I conti:** con 12 concorrenti la somma dei punti di ogni tappa è 1 + 2 + … + 12 = 78.

**Criteri in più, con soglie fissate prima di provare.**

| # | Criterio | Soglia |
| --- | --- | --- |
| Z8 | Stesso codice, stessa stagione | due pagine (anche Chromium contro Firefox) con lo stesso codice: tappe, venti, rivali e tratti identici in 20 codici su 20 |
| Z9 | Il risultato dell'amico entra com'è | in 20 tappe scambiate, la posizione di Lucio nella classifica è coerente col suo file: davanti a tutti i rivali che ha battuto in acqua, dietro a quelli che lo hanno battuto, 20 su 20 |
| Z10 | Conti con 12 | somma dei punti di ogni tappa = 78; con un amico «in attesa», somma = 66 sugli 11 presenti |
| Z11 | File sbagliati rifiutati | un file di un'altra stagione, di un'altra versione o rovinato viene rifiutato con un messaggio chiaro, mai caricato a metà |

**Rischi in più.**
- **Si può barare:** chi corre per secondo conosce il risultato dell'altro e può rifare la regata. Proposta: il file conta solo la **prima** regata corsa di quella tappa, come in una regata vera. Fra amici basta, ma lo si dice.
- **Rivali diversi in acqua:** Lucio può avere incontrato i rivali più forti, e Ale quelli più deboli. Il piazzamento a numeri compensa solo in parte, e va detto nel gioco.

**Scelta in più per Ale:** la stagione con Lucio parte insieme alla stagione da solo, oppure dopo, come secondo passo. Consiglio: dopo, così il primo passo resta piccolo e la stagione da solo si collauda per conto suo.

## Aggiunta (14 novembre, sera): le batterie

Ale: «mi sembra però strano giocare contro 3 e vedere una classifica di 11». Scelta: **batterie allo zonale ora, flotta più grande al nazionale** (Ale: «ok B ora e A al nazionale»).

**Fonte.** Nei campionati con flotte grandi la serie di qualificazione si corre a flotte separate, gruppi di colore il più possibile uguali di numero, e le classifiche poi si mettono insieme (F103, **[da verificare]** sul testo intero). Il gioco usa la stessa idea in piccolo, e lo dichiara.

**Cosa cambia nel modello.**
- **A ogni tappa la flotta del circuito è divisa in batterie.** Tu corri sempre in una batteria da 4, cioè tu più 3 rivali: è la regata di oggi.
- **Le altre batterie corrono «a numeri»**, come scritto sopra, ma ora hanno un nome e si raccontano:
  - prima: «Oggi la flotta è divisa in tre batterie: tu corri nella gialla con Sara, Pietro e Bartolin»;
  - dopo: «Nella blu ha vinto Fontana, nella rossa Gallo».
- **Le batterie cambiano a ogni tappa**, come nelle flotte separate vere: in una stagione si incontrano in acqua quasi tutti i rivali.
- **Quante batterie e di quanti:**
  - da solo siete in 11 (tu e 10 rivali): batterie da 4, 4 e 3. Le flotte vere sono «il più possibile uguali», non per forza uguali. La tua è sempre da 4; quella da 3 corre a numeri, quindi non si vede;
  - con Lucio siete in 12: tre batterie da 4. Lucio corre sempre nella sua, mai nella tua.
- **Al nazionale** (passo successivo, proposta a parte): la tua batteria diventa più grande, 6 barche, come premio della promozione. Prima vanno sistemati la linea di partenza, i punti, gli aspetti delle barche e le precedenze con più di 4 barche (`PROPOSTA-RIVALI-E-SPONSOR.md` §7).

**Criteri in più, con soglie fissate prima di provare.**

| # | Criterio | Soglia |
| --- | --- | --- |
| Z12 | Batterie giuste | in 200 tappe simulate: la tua batteria ha sempre 4 barche; le altre differiscono al massimo di 1; ogni concorrente è in una batteria sola |
| Z13 | Si incontrano tutti | in 200 stagioni simulate da 4 tappe, in media almeno 8 dei 10 rivali corrono in acqua con te almeno una volta |
| Z14 | Il racconto dice il vero | il vincitore scritto per ogni batteria è il primo di quella batteria nella classifica della tappa: 0 errori in 20 tappe corse |

**Scelta in più per Ale.** Da soli in 11 le batterie sono da 4, 4 e 3. Si può invece aggiungere un undicesimo rivale, preso dalla lista dei 20 nomi già approvati (§12), per fare tre batterie da 4. Costo: il gruppo bilanciato della 1.2.33 (3 doti, 4 medie, 3 difetti per area) va rifatto per 11, e i gruppi già salvati si rigenerano. Consiglio: restare a 10 rivali. La batteria da 3 non si vede, e con Lucio si arriva comunque a 12.


## Fermata 2: via di Ale e dettagli (14 novembre, sera, scritti prima del codice)

Ale: «ok come consigli tu». Quindi: 10 rivali, 4 tappe, nomi dei posti scritti da Claude, frasi in una lista che Ale controlla dopo, Lucio in un passo successivo, batterie. Versione **1.2.36**.

**Dove si gioca.** Il torneo singolo resta com'è. Nella finestra del torneo, quando non c'è niente in corso, c'è un pulsante in più: «Stagione (4 tappe)». Ogni tappa è un torneo come oggi (4 regate), con i 3 rivali della tua batteria. La finestra della tappa ha il pulsante «Il circuito», con la classifica degli 11 e le frasi.

**Batterie.** Si sorteggiano tutte all'inizio della stagione, così si vede subito con chi correrai. Si chiamano gialla, bianca e arancione, per non confonderle con le barche rossa, verde e blu. Nella tua entrano per primi i rivali che non hai ancora incontrato (serve a Z13: col sorteggio puro, in 4 tappe se ne incontrano in media 7,6 su 10).

**Ordine della tappa (Plackett-Luce).**
- La forza di un concorrente è f = (dote +1, media 0, difetto −1 in partenza) + (lo stesso in bolina), da −2 a +2; tu hai f = 0.
- Si estrae l'ordine di tutti gli 11, uno per volta, ciascuno col peso e^(B·f).
- I 4 posti usciti per la tua batteria si riempiono nell'ordine vero del torneo.
- **B si sceglie così:** il più grande fra 0,1, 0,2, … 1,5 per cui, sui semi 1-10 (10 gruppi di rivali, 200 stagioni ciascuno), il rivale meno fortunato di ogni gruppo vince almeno 2 stagioni su 200. Si conferma Z1 (almeno 1 su 200) sui semi 11-20, mai guardati.

**Punti del circuito.** Posto nella tappa = punti, nessuno scarto. A parità di punti vince chi ha più piazzamenti migliori, poi chi è andato meglio nell'ultima tappa (come A8 di F15). Se ti ritiri da una tappa, sei 11° in quella tappa e i rivali vanno tutti a numeri. I primi 3 a fine stagione hanno «diritto al nazionale»: viene solo scritto e salvato.

**Frasi** (al massimo 3 dopo ogni tappa, in quest'ordine; ogni regola scrive al massimo una frase):
1. «La tua bestia nera: X, davanti a te in N tappe su N» (da 2 tappe; X è quello messo meglio nel circuito fra chi ti è sempre davanti);
2. «Con X ti sei toccato in N regate: colpa sua in a, tua in b» (N ≥ 2 nella stagione);
3. «X e Y si giocano il primo posto del circuito: D punti fra loro» (da 2 tappe, primo e secondo a 2 punti o meno; «Tu» se sei tu);
4. «X è in forma: tre podi di fila» (gli ultimi 3 piazzamenti di tappa fra i primi 3);
5. «Sei sempre arrivato davanti a X: N tappe su N» (da 2 tappe; X è quello messo meglio nel circuito fra quelli che hai sempre battuto).

**Il racconto delle batterie:** «Batteria bianca: ha vinto X» (il primo di quella batteria nell'ordine della tappa).

**Salvataggio:** `progress.stagione`, separata fra carriera e gioco libero come tutti i progressi. Se cambia la versione del gioco, la stagione resta e la tappa in corso ricomincia, con la stessa batteria.

**Soglie:** quelle di Z1-Z7 e Z12-Z14 qui sopra, invariate. Per Z2 e Z14 le 20 tappe si corrono col pilota (80 regate). Per Z4 servono 20 stagioni intere: le tappe col pilota sarebbero 320 regate, troppe per il PC. Le tappe si chiudono allora con il risultato del torneo scritto dal collaudo, passando dalle stesse funzioni del gioco. Il collaudo lo dice.
