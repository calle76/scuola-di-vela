# Proposta: le lezioni della scuola (gruppi A, B e C)

1 novembre 2026. **Fermata 1: solo documento, nessun codice, nessun testo di lezione.** È il passo 3 della riorganizzazione (`PROPOSTA-RIORGANIZZAZIONE.md` §5). Si lavora sul ramo `pulizia` (1.1.0), dove la barca è solo quella dell'1b. Il gruppo D, le sette lezioni sul regolamento, ha già la sua proposta approvata (`PROPOSTA-LEZIONI-2A.md`). Qui ci sono gli altri tre gruppi, l'ordine di tutte e 20 le lezioni e il modo di provarle.

## 1. Da dove si parte (misurato, 1.1.0)

Le sei lezioni di oggi hanno 32 passi pratici. Il pilota di prova (`collaudo_pilota_lezioni.py`, semi 1-10) sulla barca dell'1b dà questi risultati:
- **27 passi** vanno bene: si completano guidando 10 volte su 10 e non si completano mai da soli.
- **3.10 «Filetto sottovento»** non si completa mai (0 su 10).
- **Quattro passi si completano da soli**, senza toccare niente (10 su 10): 2.4 «Barra sottovento: si orza», 3.2 «Bolina», 5.2 «Prepararsi a virare», 6.2 «Assorbire una raffica».
- `collaudo_lezioni.py` cade su «L5 prepararsi (bolina lanciata)», che è lo stesso passo 5.2 visto da un altro collaudo.

**Ipotesi da verificare**, non ancora misurate: nei passi 2.4, 3.2 e 5.2 la barca dell'1b orza da sola quando sbanda (1.0.46, fonte F4) e arriva in bolina senza che il giocatore faccia niente. Nella 6.2 la stessa orzata smorza la raffica. Nella 3.10, con la vela tutta cazzata, la barca orza fino a dove la vela non può più stallare dal lato sottovento. Il primo lavoro della fermata 2 è controllare queste ipotesi, guardando il registro del pilota passo per passo.

**La scotta automatica nelle lezioni (come ha ricordato Ale).** Nei passi dove la vela non è l'argomento la vela si regola già da sola (`autoTrim`). Sono 13 passi, nelle lezioni 1, 2, 3 e 5. È da lì che è nata la «Scotta automatica» delle impostazioni (1.0.73). **Proposta: resta così.** Nei passi che insegnano la scotta (`sheet: true`) la vela si regola sempre a mano; negli altri decide il passo, come oggi; la casella delle impostazioni continua a non avere effetto nelle lezioni. Lo scrivo nella lezione 1, in una riga: «in questi primi passi la vela si regola da sola: alla scotta pensi dopo».

## 2. Gruppo A: le sei lezioni di oggi, sistemate per la barca dell'1b

Le lezioni di oggi non si riscrivono da capo: testi e quiz sono stati verificati sulle fonti e restano. Si cambia solo quello che la barca nuova rompe, o che la riorganizzazione ha deciso:

1. **I cinque passi della §1.** Per ognuno: prima la causa misurata, poi la correzione più piccola. Le possibilità sono tre: cambiare la partenza del passo, per esempio iniziare in poppa invece che al traverso, così la barca non arriva in bolina da sola; cambiare la condizione, per esempio chiedere che la barra sia stata spostata dalla parte giusta; correggere il testo, se la barca nuova si comporta diversamente da come il testo dice. **La fisica non si tocca: la barca dell'1b è congelata.**
2. **«Le mure e le precedenze» esce dalla lezione 3** e passa al gruppo D. Nella lezione 3 restano le mure, senza la parte sulle precedenze, e il titolo diventa «Andature e mure». La decisione è del 31 ottobre.
3. **I testi che parlano della barra fino in fondo o del raddrizzare in 3 s** si allineano alla barca dell'1b: barra fino a 35° con la sola freccia, raddrizzata di 10 s al traverso. Li trovo con un controllo frase per frase, fatto prima di scrivere (criterio L2).
4. **«Ripartire» (1.9).** Il 16 ottobre era stato deciso che sull'1b dall'angolo morto non si esce da soli, ma col boma spinto (Z). La barca congelata il 23 ottobre invece, sotto 0,5 m/s, poggia ancora da sola come l'1a, e il pilota completa il passo 10 volte su 10 senza Z. **Proposta: la barca resta com'è** (è congelata) e la lezione 1 resta com'è. Z si insegna nel gruppo B, come il modo più rapido e più vero di uscire dall'angolo morto. Questo lo dichiaro come semplificazione, non è una domanda.

## 3. Gruppo B: la fisica dell'1b (cinque lezioni nuove)

Ogni lezione ha la forma decisa per le lezioni brevi (`PROPOSTA-COMPLETAMENTO-1B.md` §1): da 2 a 4 passi, **uno solo pratico**, e un quiz di 4 domande. **Il testo si scrive solo dopo aver letto la fonte** di ogni affermazione. Se la fonte non c'è, quella frase non si scrive, e lo dico.

| # | Lezione | Il passo pratico (idea) | Fonte già nei documenti |
|---|---|---|---|
| B1 | Il timone che stalla | Virata con la sola freccia (35°) e con Maiusc (45°): si vede la pala che stalla e la barca che gira peggio | F4, F35 (`archivio/PROPOSTA-STALLO-TIMONE.md`) |
| B2 | Spingere il boma (Z) | Barca ferma nell'angolo morto: con Z e la barra si esce all'indietro e si riparte | tre fonti didattiche e la federazione australiana (`archivio/PROPOSTA-SPINGI-BOMA.md`); regola 21.3 (F15) per la regata |
| B3 | La barca che orza sbandando | Raffica con la vela ferma: la prua va verso il vento. Si tiene la rotta con la barra o lascando | F4 eq. 6 (`archivio/PROPOSTA-ORZIERA-1B.md`) |
| B4 | La raddrizzata lunga (A) | Si parte rovesciati: A, dieci secondi, barca al traverso con la vela che sbatte; poi si riparte | una sola fonte divulgativa, il video dell'allenatore (`archivio/PROPOSTA-RADDRIZZATA.md`): **da dichiarare nel testo** |
| B5 | I salti di vento | Bolina con il vento che oscilla: virare quando il vento «scarseggia» (ruota verso la prua) | **da verificare**: `archivio/PROPOSTA-SALTI-VENTO.md` cita F7, che è una fonte sulle andature portanti. Prima di scrivere cerco una fonte vera sulla bolina nei salti. Se non la trovo, la lezione diventa la sola descrizione di quello che il gioco fa, dichiarata come tale |

**Mancano due cose nel gioco.** Primo: nessun passo di lezione accende oggi i salti di vento, che servono alla B5. Si aggiunge un campo del passo, come `env` per vento e raffiche. Secondo: il pilota dei collaudi non usa Z né Maiusc, e va esteso per B1 e B2.

## 4. Gruppo C: le due partenze

| # | Lezione | Il passo pratico | Fonte |
|---|---|---|---|
| C1 | Partenza in velocità | Partenza da soli: aspettare vicino alla linea e cazzare negli ultimi secondi, per tagliare la linea poco dopo lo sparo e già veloci | F15 (26, 29.1), F25, F30; misure dei nostri avversari in `archivio/PROPOSTA-PARTENZE.md` |
| C2 | Partenza da fermi | Barca quasi ferma con la vela che sbatte, poi via allo sparo: si vede quanta strada e quanti secondi servono per prendere velocità | come C1 |

**Il costo vero del gruppo C.** Una lezione oggi non ha né linea né conto alla rovescia: li ha solo la regata. **Proposta più semplice:** i passi pratici di C1 e C2 aprono una regata senza avversari, con un obiettivo da leggere nel pannello. Per la C1, per esempio: «taglia la linea entro 5 s dallo sparo a più di 3,5 nodi, senza anticipo». Le soglie sono attese nostre e si fissano col pilota, con la regola dei semi (scelta sui semi 1-20, conferma sui semi 101-120). Per confronto, il pilota degli avversari parte con un ritardo mediano di 1-2,3 s e a 4,6-4,75 nodi (`collaudo_partenze.py`). Un'alternativa è costruire la linea dentro la lezione, ma costa di più ed è codice nuovo nel gioco: non la propongo.

## 5. L'ordine delle 20 lezioni (proposta)

Prima la barca, poi le regole, perché le partenze vengono meglio dopo i segnali:

1. A1 La barca e il vento
2. A2 Il timone
3. B1 Il timone che stalla
4. A3 Andature e mure
5. A4 Vento reale e apparente
6. A5 Virata e strambata
7. B2 Spingere il boma
8. A6 Raffiche e scuffia
9. B4 La raddrizzata lunga
10. B3 La barca che orza sbandando
11. B5 I salti di vento
12. D1 Mure opposte
13. D2 Stesse mure
14. D3 Chi vira cede
15. D4 Evitare il contatto
16. D5 I segnali di partenza
17. D6 La partenza anticipata
18. C1 Partenza in velocità
19. C2 Partenza da fermi
20. D7 Toccare una boa e i giri

Nel menu (passo 5, non qui) vanno forse raggruppate per argomento: la barca, il vento, le regole, la regata.

## 6. Criteri (soglie scritte prima, attese nostre)

- **L1, fonti:** per ogni lezione nuova, una riga con la fonte e la parte letta prima del testo; 13 lezioni su 13 (B, C e D). Per il gruppo A, una riga per ogni testo cambiato.
- **L2, il testo dice quello che fa il gioco:** ogni frase che descrive un comportamento della barca ha una misura o un collaudo che la provoca: 100% delle frasi. Se una frase non si può provocare, si toglie.
- **L3, i passi pratici funzionano:** col pilota (`collaudo_pilota_lezioni.py`), ogni passo pratico si completa guidando in **almeno 9 semi su 10** e **non si completa mai da solo** (0 su 10). Fanno eccezione i passi in cui il testo chiede di aspettare: sono dichiarati prima nella tabella del collaudo, come oggi. Le soglie si scelgono sui semi 1-10 e si confermano sui semi 11-20, mai guardati. **Il metro dichiara quanti passi ha davvero valutato**, e devono essere tutti quelli della tabella.
- **L4, `collaudo_lezioni.py` verde**, senza aggiungere passi alla lista dei «noti».
- **L5, pannello e riquadro delle istruzioni** a 1360×650: 0 px con il testo più lungo di ogni passo, in Chromium e in Firefox.
- **L6, pagina come la carica un giocatore:** senza `#collaudo`, ogni lezione si apre e si percorre almeno fino al primo passo pratico, con 0 errori della pagina, in tutti e due i browser.
- **L7, quiz:** 4 domande per ogni lezione nuova; ogni risposta giusta è detta nel testo della lezione (controllo a mano, riportato); banca dell'esame aggiornata con 4 domande per lezione.
- **Non-regressione:** `impronta1b.js` al bit, perché la barca non si tocca; `polare.js` e `raffiche_e_virate.js` identici; arrivi delle regate identici al bit (`arrivi_regate.py`), perché le lezioni non toccano le regate.

## 7. Fette (ognuna una versione sul ramo `pulizia`, con i collaudi verdi)

1. **Gruppo A sistemato:** i cinque passi della §1, la lezione 3 senza precedenze, i testi allineati alla barca. Alla fine di questa fetta il gioco del ramo è di nuovo «sano», e si potrebbe già portare in `main`: è una domanda per dopo.
2. **Gruppo B,** una lezione per volta: B1, B2, B3, B4, poi B5 con la ricerca della fonte.
3. **Gruppo D,** le sette lezioni sul regolamento (testi dal PDF di F15).
4. **Gruppo C,** con la regata senza avversari come passo pratico.
5. **Esame e glossario** aggiornati.

Medaglie (passo 4) e menu (passo 5) vengono dopo, come deciso.

## 8. Rischi

- **Venti lezioni sono tante** per chi comincia. Le nuove sono brevi, ma il conto totale dei passi va riportato a ogni fetta.
- **B5 e B4 hanno fonti deboli**, nessuna o una sola divulgativa: si dichiarano, e se serve si accorcia.
- **Il gruppo C dipende dalla regata:** un passo pratico dentro una regata è nuovo per il collaudo delle lezioni.
- **Spazio nel pannello:** testi nuovi e lunghi possono sforare, come già sforano salti e giri (84-406 px). Il criterio L5 vale per ogni passo.
- **Il ramo `pulizia` resta lontano da `main`** per tutta la durata del lavoro. Se `main` riceve correzioni (Esploratore, osservazioni di gioco), vanno portate anche sul ramo.

## 9. Da decidere (Ale), una cosa alla volta

1. **L'ordine della §5 va bene?** In particolare: il regolamento prima delle partenze, e le cinque lezioni della barca dell'1b mescolate con quelle di oggi invece che tutte in fondo.

## 10. Avanzamento

- **1.1.3 (1 novembre 2026), fetta 1, prima parte:** i cinque passi della §1 sono a posto. Su 32 passi, 32 si completano guidando e nessuno si completa da solo (semi 1-10, conferma 11-20); i numeri sono nel `CHANGELOG.md`. Nei passi senza barra la rotta la tiene la scuola, una semplificazione nuova e dichiarata. Restano due cose: togliere le precedenze dalla lezione 3, da fare insieme al gruppo D; e il controllo dei testi frase per frase (L2).
- **1.1.4-1.1.7 (1 novembre 2026), fetta 2:** lezioni B1 «Il timone che stalla», B2 «Spingere il boma», B3 «La barca che orza sbandando» e B4 «La raddrizzata lunga», nascoste nel menu finché non arriva il menu nuovo. Ogni passo pratico: guidando 10 su 10 e a mani ferme 0 su 10, sui semi 1-10 e 11-20. Resta B5 (salti di vento, fonte da cercare).
