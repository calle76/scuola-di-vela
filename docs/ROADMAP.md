# Roadmap

Aggiornata al 4 ottobre 2026; ordine dopo la 1.0 e livelli rivisti il 16 ottobre 2026.

Il disegno dei livelli, dei ruoli, dei meriti e della carriera è in `VISIONE-LIVELLI-E-CARRIERA.md`; le fonti pubbliche consultate in `FONTI-PUBBLICHE.md`. Dove questa roadmap e la visione dicono cose diverse sulle fasi C ed E, vale la visione.

## Ordine dei lavori dal 19 ottobre 2026 (vale su tutto quello che segue)

**Impianto dei livelli:** `VISIONE-LIVELLI-E-CARRIERA.md` §2 (unico riferimento). Una novità grande per livello; «a» teoria, «b» pratica con replay e tornei. 1a = il livello 1 di oggi (congelato); 1b = barca completa, replay, tornei; 2 = il regolamento con la stessa deriva; 3 = fiocco; 4 = gennaker; 5 = equipaggio da tre e tattica. Le fasi qui sotto sono scritte prima e usano i numeri vecchi.

**Ordine:** ~~congelare la barca dell'1b~~ (**fatto il 23 ottobre 2026**, `archivio/PROPOSTA-CONGELAMENTO-1B.md`: 1.0.43-1.0.46 e le due impronte) → pulizia → avversari con la barca dell'1b → tornei dell'1b, tappa T2 (triangolo; la T1, formato e punteggio a bastone, è fatta nella 1.0.34-1.0.35) → lezioni brevi dell'1b → replay semplice (`PROPOSTA-REGATA-COME-FONTE.md` §9) → menu, attestato e brevetto dell'1b → tempi delle medaglie → livello 2: 2a il regolamento (regole 14-18, 21, 23, giallo, penalità a giri, segnali), 2b protesta, copertura del vento, tornei con le regole vere, replay con domande. **Le regole nell'1b si fermano alle 10-13** (Ale, 23 ottobre 2026; `VISIONE-LIVELLI-E-CARRIERA.md` §2). Dettagli e stato: `STATO.md`, «Prossimo lavoro».

## Principi che valgono per ogni fase

- **Tutto sempre giocabile**: nessun contenuto va sbloccato nella modalità libera.
- La **carriera** sarà una modalità separata e facoltativa, con salvataggio proprio. Il menu avrà un primo bivio: **gioco libero** (tutto sbloccato, il menu a riquadri di oggi) oppure **carriera**.
- Nei titoli del gioco si dice **brevetto**, mai «patente» o «patentino».
- **Confini legali**: niente marchi, niente titoli che sembrino ufficiali, dati esterni solo con licenza libera e citazione.
- Ogni novità si collauda **guidando davvero la barca** (vedi `COLLAUDI.md`), non solo leggendo il codice.
- **Prima la barca, poi tutto il resto** (Ale, 17 ottobre 2026). In ogni livello nuovo si chiude prima la barca con tutte le sue dinamiche, poi la si congela con l'impronta (`tests/collaudo_impronta.py`); solo allora avversari e manovre che usano `step()`, poi i testi e le soglie delle lezioni, e **per ultimi i tempi delle medaglie**, che sono taratura sulla barca e non contenuto. Ragione: la 1.0.6 (resistenza dello scafo) ha portato gli avversari oltre la linea allo sparo dal 22-32% all'83% perché frenavano a 7 m fissi, e la 1.0.11 (bolina) ha reso da correggere tre passi delle lezioni. Corollario: dove un numero dipende dalla barca si **deriva dalla barca** (lunghezze di `BOAT.length`, frenate e partenze simulate con lo stesso `step()`), non si scrive a mano in metri o secondi.
- **Il giro da ripetere a ogni livello** (Ale, 17 ottobre 2026), in quest'ordine: 1) la barca, fisica e comandi, fino a niente di aperto; 2) collaudarla e congelarla con l'impronta; 3) correggere e alleggerire il codice (togliere quello che la barca nuova ha reso inutile, derivare dalla barca i numeri scritti a mano, aggiornare le mappe `// ====`); 4) alleggerire i documenti (chiudere le proposte finite tenendo decisione e numeri, archiviare il `CHANGELOG.md` vecchio); 5) avversari e manovre che usano `step()`; 6) testi e soglie delle lezioni; 7) per ultimi i tempi delle medaglie, rigenerati col pilota. I passi 3 e 4 sono parte del giro, non un extra.

## Fase A — Misura degli errori, brevetto ed esame

1. ~~**Registro degli errori**~~ in lezioni, prove e regate: **fatto nella 0.15** (definizioni nel `CHANGELOG.md`). Registra anche i dati che serviranno all'esame e alla carriera; le regole di promozione (numero massimo di errori, tempi limite) si decideranno lì.
2. ~~**Fasce di tempo**~~ per le prove: **fatto nella 0.16**, tarate con un pilota automatico (vedi `CHANGELOG.md`). Da ritoccare dopo averci giocato, a partire dalla prova 1.
3. **Esame a risposte chiuse**: banca di 80–100 domande, 20 estratte a caso, soglia 80%. Due tipi:
   - glossario (come i quiz attuali);
   - situazioni con un piccolo disegno di barca e vento («che andatura è?», «cosa fai se entra una raffica?», «chi ha la precedenza?»).
   - Se non si supera, in carriera serve un ripasso mirato sulle lezioni sbagliate prima di riprovarlo, senza penalità; nel gioco libero l'esame si ripete subito.
4. **Brevetto della Scuola di vela**, a livelli (per esempio «Timoniere di deriva», poi «Regatante»), con attestato stampabile. Nessun valore legale, e deve essere scritto.

### Ordine delle versioni della fase A

| Versione | Contenuto |
| --- | --- |
| 0.15 | Registro degli errori, pannello ordinato, segno «senza errori» (fatto) |
| 0.16 | Menu principale a riquadri e fasce di tempo; lezione 1 con il solo timone; rosa dell'angolo morto; freccia della velocità; pannello ridotto (fatto) |
| 0.17 | Esame a risposte chiuse, nel suo riquadro del menu |
| poi | Brevetto con attestato |

**Fase A chiusa con la 1.0 (14 ottobre 2026):** esame (0.20), piazzamento e Competizione (0.21), bivio gioco libero / carriera (0.22), libretto (0.23), esame in carriera e attestato (0.24), rilascio (1.0). Dettagli in `archivio/PROPOSTA-ESAME-E-BREVETTO.md` e `CHANGELOG.md`.

### Dopo la 1.0.1: ordine del 16 ottobre 2026, sostituisce quello del 14 ottobre qui sotto

Ale ha deciso la direzione (livello 2 su regole e avversari) e ha lasciato a Claude Code l'ordine dei lavori tecnici. Le sue osservazioni sulla 1.0 non sono un passo da aspettare: si scrivono in `OSSERVAZIONI-GIOCANDO.md` quando arrivano, i difetti piccoli si correggono in versioni minori, e il resto entra nella proposta del livello 2.

0. ~~**1.0.2, correzioni piccole dalle osservazioni sulla 1.0**~~ (16 ottobre 2026, vedi `CHANGELOG.md`, compresi i sette passi di lezione che sforavano il pannello: ora eccesso 0 px a 1360×650 e 1360×768, misurato da Ale) (`OSSERVAZIONI-GIOCANDO.md`, 44, 46, 49 testo, 50, 53, 54): voci del ripasso, «medaglie» al posto di «fasce del record», «a piccoli colpi» in evidenza, scuffia e raddrizzamento nella lezione 6, pulsanti doppi all'arrivo, attestato più curato senza timbro né firma. Prima della divisione, perché si sentono giocando e sono piccole.
**Il livello 1 non è finito** (Ale, 16 ottobre 2026): prima si chiude quello, poi si divide il codice, poi si passa al livello 2.

**Precisazione di Ale (16 ottobre 2026), che cambia i passi sulla barca:** non è detto che la barca sia lenta in generale; è **lenta nelle virate**, con il rischio di piantarsi controvento. Quindi: (a) **velocità**: prima si controlla su dati pubblici quanto va davvero la deriva di riferimento (polari, tempi di regata, misure nei video), confrontandola con `polare.js`, e solo se c'è una differenza documentata si tocca la resistenza dello scafo (la stima di `archivio/PROPOSTA-RESISTENZA-SCAFO.md`, «frena circa il doppio», va ricontrollata, non data per buona); (b) **virata**: tempi e lunghezze dai video (circa 3 s e 2 lunghezze, osservazione 40); (c) **retromarcia**: verificare se è realistica e quanto in fretta parte (secondo Ale si innesca troppo presto), con fonti e video; (d) **ripartire dall'angolo morto**: oggi la lezione 5 insegna un'uscita che sfrutta molto la retromarcia; va confrontata con i metodi delle fonti (in `CONTENUTI-DA-VERIFICARE.md` ci sono già Lee, Yachting New Zealand e il metodo col boma spinto, che il gioco non ha). Il laboratorio serve proprio a provare questi valori a confronto con i video. **Ricerca del 16 ottobre** (`archivio/RICERCA-VELOCITA-VIRATA-RIPARTENZA.md`): con 6-12 nodi il gioco risulta più lento del 20-50% rispetto ai dati misurati (velisti di vertice), vicino ai dati di bolina con 15 nodi; per virata e retromarcia nessun numero pubblicato (i «3 s e 2 lunghezze» vanno rimisurati sullo stesso intervallo); la ripartenza delle fonti è con boma e barra dallo stesso lato, che il gioco non permette. **Scelta di Ale (16 ottobre 2026): si tara la barca condotta bene**; la differenza la fa chi la conduce.

**Aggiornamento del 16 ottobre, dopo il pilota delle lezioni:** la barca va corretta prima delle lezioni, perché quattro dei sei passi da correggere dipendono dalla fisica. Ordine: divisione del codice (fatta, 1.0.3); ~~**laboratorio**~~ (fatto nella 1.0.4, `archivio/PROPOSTA-LABORATORIO.md`); ~~**resistenza dello scafo**~~ (fatta nella 1.0.6, `archivio/PROPOSTA-VELOCITA.md`; nate due voci nuove: ~~**resistenza indotta**~~ e ~~**bolina con poco vento**~~, fatte insieme nella 1.0.11, `archivio/PROPOSTA-BOLINA.md`: variante 9° / 22° scelta da Ale; la bolina con poco vento resta il 15% sotto Day, causa non trovata; con 15 nodi +7%, compito a parte; il passo 1.8 della lezione 1 col pilota non si completava più: ~~corretto il testo nella 1.0.12~~, `archivio/PROPOSTA-CORREZIONI-PASSI.md` §1); **ordine deciso con Ale dopo la 1.0.6:** ~~prima il rallentamento con lo zoom lontano~~ (era Firefox: con Chrome avviato a schermo intero è fluido, vedi sotto «Scartato: pulsante Schermo intero»), poi la ~~**retromarcia**~~ (fatta nella 1.0.8, `archivio/PROPOSTA-RETROMARCIA.md`: tetto tolto, nessun freno di poppa; quanto presto parte non è cambiato e resta da guardare; `archivio/RICERCA-RETROMARCIA.md`: togliere il tetto `backMax` senza fonte e lasciare che la velocità all'indietro nasca dalla spinta della vela che sbatte contro il freno dell'acqua, più un freno «di poppa» dichiarato come ipotesi, da provare in laboratorio); ~~**timone e virata**~~ (chiusa da Ale il 16 ottobre 2026: la virata è coerente coi video, circa 3 s contro i 3,3 s misurati nella 1.0.6; registrazione `sessione-20261016-1247.txt`: virate fallite entrando a 2,0, 2,2 e 2,7 nodi con vento di 10, riuscita a 2,9, da riguardare con la retromarcia); **retromarcia, scelta di Ale (16 ottobre):** la barca lasciata andare con la vela che sventola, senza tetto; pilota rilanciato e correzioni dei passi; poi raffiche da dietro e partenze. Quello che manca al livello 1, con le osservazioni di `OSSERVAZIONI-GIOCANDO.md`:

1. ~~**Pannello a 1360×650**~~: fatto nella 1.0.2, eccesso 0 px misurato da Ale (16 ottobre 2026).
2. ~~**Pilota completo delle lezioni**~~ (fatto il 16 ottobre 2026, `archivio/PROPOSTA-PILOTA-LEZIONI.md` §10; trovati 6 passi da correggere, da proporre uno per uno: «Ripartire», «Barra sottovento», «Accelerando», «Assorbire una raffica», «La scuffia» e i casi minori. Era: oggi 14 passi pratici su 32 si guidano davvero), che trova i passi che si completano da soli (osservazioni 45 e 49) e dà la rete di sicurezza per toccare la fisica. Costruito in modo che serva anche alle lezioni del livello 2.
3. ~~**Raffiche da dietro**~~ (osservazione 52): **fatto nella 1.0.9** (`archivio/PROPOSTA-RAFFICHE-PORTANTI.md`). Testi da rendere più efficaci e corti: li riguarda Ale giocando.
4. **Avversari e partenze del livello 1** (osservazione 47 e il messaggio di Ale del 16 ottobre: «errori che non sembrano casuali»): il riquadro consiglia di tagliare la linea lanciati, mentre gli avversari (e le regate vere guardate da Ale) partono quasi fermi sulla linea; avversari che escono dagli estremi della linea; contatti fra loro; tempi di rientro dopo una partenza anticipata. Prima si misura cosa fanno, poi si decide con fonti scritte e video. **Le regole di precedenza, le penalità a giri e la protesta restano al livello 2.** **Ale (16 ottobre 2026, dopo la 1.0.15):** gli avversari fanno bene a partire quasi fermi, come nella realtà; da rivedere è il consiglio del riquadro («l'ideale è tagliarla lanciato proprio allo zero», `js/regate.js`). Il resto è da rivedere. Ordine per chiudere il livello 1: questo compito, poi le increspature (4b), poi `collaudo_carriera_intera.py` con il pilota nuovo come controllo finale. **Tutti e tre fatti il 17 ottobre 2026** (1.0.16-1.0.19): la carriera intera dà OK con 32 passi su 32 guidati. **Livello 1 chiuso nei collaudi** (1.0.21). **Ordine deciso da Ale il 17 ottobre sera per chiuderlo davvero:** manutenzione del codice della partenza e riferimento dell'impronta (**fatta nella 1.0.22**); poi, per ultima, un ultimo tentativo sulla bolina lenta con poco vento (**fatto il 17 ottobre: limite noto dichiarato**, `archivio/PROPOSTA-BOLINA.md` §11); poi il livello 2. Restano il giudizio di Ale giocando (increspature, retromarcia con vento forte, disegno della vela, testi delle raffiche da dietro). **Stato (17 ottobre 2026): parte 1 FATTA nella 1.0.16** (`archivio/PROPOSTA-PARTENZE.md` §7): richiami dall'83% al 3,8-6,7% per partenza, ritardo mediano al via 0,9-2,2 s, nessun avversario che non parte, conferma sui semi 21-100 mai guardati. **Parte 3 (contatti fra avversari) FATTA nella 1.0.17** (§8): contatti totali −38%, barche con penalità dal 59% al 40%, due soglie su sette non raggiunte e dichiarate; quel che resta sono le precedenze alla boa, livello 2. **Parti 2, 4 e 6 chiuse nella 1.0.18** (§9): estremi a posto senza modifiche (nessun taglio fuori dagli estremi in 3.600 partenze), frase nuova nel riquadro sul rientro dopo l'anticipo, C1 rientrata (ultimo posto dal 46-48% al 35%/28%). **Il compito partenze è chiuso**, compresa la parte 5 (il pilota da tastiera del collaudo poggiava e virava male; sistemato nel collaudo, due giri su due OK). **Ale:** nei livelli futuri barche più grandi e pesanti partono lanciate: non ora.
4b. ~~**Increspature più vive dentro le raffiche**~~ **FATTO nella 1.0.19** (`archivio/PROPOSTA-INCRESPATURE.md`: trama nel cuore della chiazza da +267% a +340% a zoom pieno e da +196% a +506% a zoom 0,5, costo +9,6%; manca il giudizio di Ale giocando). Era (idea di Ale, 16 ottobre 2026, nel livello 1): un secondo strato di increspature, solo nelle chiazze scure, che scorre più in fretta in proporzione alla forza della raffica e sfuma ai bordi; fuori dalle raffiche il disegno resta identico. È un segnale visivo per leggere l'acqua, non una misura: da dichiarare. Da verificare su fonti e video cosa si vede davvero (ondine più fitte e ripide, chiazza che avanza col vento). Prima la proposta (fermata 1).
5. ~~**Divisione del codice in più file**~~: fatta nella 1.0.3 (16 ottobre 2026), anticipata prima del laboratorio e della barca (decisione di Claude Code). Era: garantita da `collaudo_impronta.py`; si fa con il livello 1 chiuso e prima del livello 2, perché il livello 2 farà crescere soprattutto regate e avversari. Il gioco diventa una cartella (`index.html` più `js/`), si apre ancora con un doppio clic: script classici, non moduli.
6. **Livello 2: regole di regata e avversari** sulla stessa barca (`VISIONE-LIVELLI-E-CARRIERA.md`, §2-3): ricerca sulle fonti, proposta rivista in chat, poi lezioni, colpa nei contatti, penalità, protesta, avversari che rispettano le regole.
7. Il resto della lista del 14 ottobre: resistenza dello scafo, timone e virate, disegno della vela, voci piccole. Il fiocco è ora il **livello 3**.

La manutenzione la propone Claude Code quando serve, senza scadenze fisse. **Dal 16 ottobre 2026 (Ale): il codice da sistemare si sistema quando lo si vede**, nello stesso compito, senza cambiare il gioco e scrivendolo nel CHANGELOG.

### Dopo la 1.0: ordine deciso da Ale (14 ottobre 2026), superato

«La 1.0 è la versione giocabile.» Poi, nell'ordine:

0. ~~**Giro di manutenzione del codice**~~: fatto nella 1.0.1 (16 ottobre 2026), vedi `CHANGELOG.md`. Il prossimo dopo la fase successiva, o circa ogni 5 versioni; da guardare allora anche i collaudi Python (circa 4.200 righe, non rivisti).
1. **Pilota completo delle lezioni:** oggi i collaudi guidano 14 dei 32 passi pratici. Serve come rete di sicurezza prima di toccare la fisica.
2. **Resistenza dello scafo** (`archivio/PROPOSTA-RESISTENZA-SCAFO.md`), con le fasce delle prove ritarate e i record azzerati.
3. **Timone e durata delle virate** (osservazione 40), con misure dai video.
4. **Regole di regata:** penalità a giri invece dei 15 s (osservazione 39), colpa con le regole 14 e 16, barca che tampona con le stesse mure, forma del contatto (osservazione 33); avversari e contatti che giudicano le mure col vento del giocatore invece che col proprio (trovato nella 1.0.1).
5. **Disegno della vela** (osservazione 41).
6. Le voci piccole della lista «Dopo la 1.0» qui sotto.

Nota (4 ottobre 2026): il contenuto reale della 0.17, in corso, è descritto nel `CHANGELOG.md` (rotta della lezione 2, partenze di regata, caratteri degli avversari). L'esame a risposte chiuse e il brevetto vengono dopo la 0.17.

Il quiz di ripasso resta subito dopo ogni lezione; l'esame per il brevetto è separato, perché riguarda tutte le lezioni.

### Contenuto della 0.16 (deciso il 29 settembre 2026, dopo il collaudo della 0.15; fatto, dettagli nel `CHANGELOG.md`)

1. **Menu principale a riquadri**, tutto visibile in una schermata: Scuola (lezioni e prove nell'ordine consigliato), Regate, Ripasso ed esame, Navigazione libera, In arrivo; Glossario in alto.
2. **Fasce di tempo** bronzo, argento e oro, mostrate nel menu insieme alla ★.
3. **Lezione 1 con il solo timone.** Via i pulsanti Orza e Poggia (tasti A e D): un comando riferito al vento non si comporta come una barra, e tenendolo premuto la barca attraversava il vento continuando a «orzare». I passi si fanno con le frecce ← →; «orzare» e «poggiare» restano nei testi e in una scritta che, mentre la barca gira, dice se sta orzando o poggiando. Cazza e Lasca restano. Versione minima: niente riorganizzazione delle lezioni 1 e 2. Controllare le domande del ripasso che citano i pulsanti.
4. **Rosa dell'angolo morto** accanto all'indicatore di sbandamento: vento sempre in alto, settore di 40° per lato in rosso, lancetta della prua che diventa rossa dentro il settore. Stesso limite della voce «Andatura» e del registro. Aiuto del gioco: nelle impostazioni, acceso di norma, disattivabile.
5. **Freccia della velocità** dal centro della barca, nella direzione in cui la barca si muove davvero (mostra lo scarroccio; all'indietro esce dalla poppa), lunga in proporzione alla velocità, nascosta sotto qualche decimo di nodo, di colore diverso dalle frecce del vento. Il triangolo reale + moto = apparente solo nella lezione 4.
6. **Pannello ridotto** in prove e regate, da decidere sulle schermate dopo aver visto rosa e freccia. Proposta: togliere Sbandamento, Scarroccio, Vento reale e Vento apparente (quest'ultimo resta nella lezione 4); tenere Velocità, Andatura, Prua e Rilevamento boa.

Dopo la 0.16, da verificare giocando: soglie delle fasce; comportamento della lezione 1 (strambata a vela aperta se si tiene premuta la freccia nel passo «Poggiare»); oscillazione della rosa nelle raffiche; scritte «reale» e «apparente» sovrapposte con la prua nel vento (difetto noto).

Scartato: pulsante «Schermo intero» nel gioco. Sul PC di prova lo schermo intero di Chrome con MATE torna subito indietro anche dal menu di Chrome (non dipende dal gioco); con Firefox F11 funziona. **16 ottobre 2026:** con Firefox, sul PC di Ale, il gioco rallenta con lo zoom lontano (nella sandbox con Chromium: 50-60 immagini al secondo e tempo del gioco al 100% a ogni zoom). Soluzione provata da Ale e funzionante: Chrome avviato già a schermo intero, `google-chrome --kiosk --user-data-dir="$HOME/.config/scuola-vela-chrome" "file://$HOME/scuola-di-vela/index.html"` (si esce con Alt+F4), resta a schermo intero ed è fluido. Alleggerire il disegno per Firefox (increspature solo vicino alla barca, idea di Ale) resta da fare solo se servirà.

## Fase B — Tornei e classifiche personali

- Tornei di più regate contro gli avversari del computer, con il sistema a punti delle regate (1 punto al primo, 2 al secondo, e così via; vince chi ne ha meno), eventualmente con uno scarto.
  - Struttura decisa in via provvisoria (ottobre 2026): 4 regate con uno scarto, ruolo bloccato per tutto il torneo, più tornei per categoria con condizioni diverse (vento leggero, vento teso, raffiche, salti di vento). Dettagli in `VISIONE-LIVELLI-E-CARRIERA.md`. Gli avversari vanno resi affidabili su più regate (la 0.17 ha già ridotto ritardi al via e partenze anticipate, vedi `CHANGELOG.md`).
- Classifica dei record personali per prova e regata.
- **Avversari che scelgono le mosse in partenza:** esiste un modello pubblicato (teoria dei giochi e Monte-Carlo tree search sul pre-partenza del match race, F30 di `FONTI-PUBBLICHE.md`, solo abstract letto il 17 ottobre 2026), da leggere se e quando si farà. Oggi l'avversario non guarda le mosse degli altri: aspetta al proprio posto e parte quando la sua simulazione glielo dice (1.0.16).
- Avversari «esperti» più forti: virate più rapide, scelta del bordo migliore, uso delle raffiche.
- **Copertura del vento (cono d'ombra):** una vela toglie vento alle barche sottovento, lungo la direzione del vento apparente; una barca poco sottovento e avanti devia il vento verso chi sta dietro sopravento. Oggi il vento non dipende dalle altre barche. Richiede: vento che dipende anche dalle barche, avversari che sappiano uscire da una copertura (altrimenti rallentano e si ammucchiano), record delle regate da azzerare. Le prove non cambiano. Eventuale disegno del cono sull'acqua come aiuto disattivabile. Valori da verificare prima (vedi `CONTENUTI-DA-VERIFICARE.md`).
- **Difetto degli avversari, ridotto nella 0.17:** in circa una partenza su cinque un avversario partiva in anticipo o con più di un minuto di ritardo. Con posizioni di partenza casuali e caratteri diversi (prudente, normale, aggressiva) la mediana del ritardo al via è scesa da circa 9 a 3–6 secondi e le partenze anticipate sono 3 su 90 con i principianti e 0 su 90 con gli esperti (misure e limiti nel `CHANGELOG.md`). Quel conteggio contava le barche ancora segnate come anticipate a +60 s, non le partenze anticipate allo sparo: vedi `CHANGELOG.md`, 0.20.3.

## Fase C — Più tipi di barca: ogni livello è una barca con cose nuove da imparare

Aggiornata a ottobre 2026; dettagli in `VISIONE-LIVELLI-E-CARRIERA.md`.

Il motore è parametrico: una barca nuova è un nuovo insieme di costanti più un disegno. Ciò che distingue un livello dall'altro non è solo la velocità o l'avversario più forte, ma cose nuove da padroneggiare: vele, equipaggio, tecnologia, informazioni. Nessun numero fisso di novità per livello: ogni livello contiene le cose giuste per quella barca (due difficili, tre facili o una difficile e due facili, secondo il caso); il carico per chi gioca si controlla giocando, lezione per lezione.

| Livello | Barca (nomi generici) | Ruoli | Cosa c'è di nuovo |
| --- | --- | --- | --- |
| 1 | Deriva da regata, un solo velista (la barca attuale) | Timoniere | Le basi |
| 2 | La stessa deriva | Timoniere | Regole di regata e di precedenza, avversari migliori (dal 16 ottobre 2026) |
| 3 | Deriva a due: randa e fiocco | Timoniere, prodiere, un ruolo alla volta | Il fiocco e il coordinamento a due |
| 4 | Deriva a due con gennaker | Timoniere, prodiere | Vela di portanza, planata, strumenti, angoli limite |
| 5 | Equipaggio da tre | Timoniere, trimmer, tattico | Il tattico elabora le informazioni |
| 6-7 | Catamarano; cabinato | Da definire | Vento apparente dominante, scuffia diversa; inerzia, mare, correnti |

Si pianifica nel dettaglio fino al livello 4; gli altri sono una direzione, non un impegno. Una deriva scuola (lenta, stabile, che perdona gli errori) resta un'idea per un eventuale livello 0.

**Prototipo del fiocco** (`sperimentale/fiocco.html`, in corso). È il primo passo, perché il rischio maggiore è la fisica delle vele. Non tocca `index.html`.

- Tappa A (il fiocco come seconda vela con scotta propria): fatta e approvata.
- Tappa B (la randa che copre il fiocco alle andature larghe, con messaggi del pannello per il fiocco): fatta e approvata dopo il giudizio di chi gioca.
- Tappa C (coerenza fra vista e forza del fiocco coperto, momento di imbardata dovuto alle vele, fiocco in virata, massa dello scafo a due): da fare.
- La manovra a farfalla (fiocco dal lato opposto) non è nel prototipo; da modellare più avanti.
- Fisica e criteri nel dettaglio: `FISICA-E-TARATURE.md`. Fonti: `FONTI-PUBBLICHE.md`. Regole di lavoro dei prototipi: `SPERIMENTALE.md`.

Ordine di sviluppo dopo il prototipo: ruolo del prodiere, equipaggio guidato dal computer, tornei con i meriti, menu carriera.

Nelle regate miste: compenso di tempo tra barche diverse, come nelle regate reali.

Idea per le raffiche (7 ottobre 2026, osservazione 17): in barca vera si vede solo la chiazza scura; freccia e «+x nodi» (forza e salto di direzione) sono informazione da strumenti. Livello 1 solo chiazza; un aiuto facoltativo, spento di default e senza effetto sui meriti, con freccia e numero (utile nella lezione 6); livello 3 strumenti vicino alla barca; livello 4 carta del tattico.

- Campo di vento esteso (raffiche su tutta l'area) per le regate e per la carta del tattico (livello 4). Vedi osservazioni 18-22 del 7 ottobre sera in `OSSERVAZIONI-GIOCANDO.md`.

## Fase D — Carteggio e mare aperto: espansione o gioco a parte

Deciso a settembre 2026: il carteggio e la navigazione in mare aperto sono quasi un altro gioco (vista a carta nautica, cabinato, tempi lunghi, dati geografici con licenza). Escono dal menu della Scuola di vela e diventeranno un'espansione o un gioco nuovo che riusa il motore fisico. Sarà anche il momento di dividere il file unico in moduli.

1. Gradi e direzioni: rosa dei venti, prua in gradi, rilevamento.
2. Velocità, tempo, distanza: nodi e miglia, punto stimato.
3. Fare il punto: due rilevamenti e il loro incrocio.
4. Il segnalamento: boe laterali e cardinali, fari.
5. Nord vero e nord magnetico.

Serve una vista «carta nautica» accanto a quella di navigazione. Per coste reali: OpenStreetMap (licenza ODbL, citazione obbligatoria) e GEBCO per le profondità. Le carte nautiche ufficiali sono protette e non vanno riprodotte.

## Fase E — Modalità carriera

Percorso facoltativo: brevetto ed esame, regate di circolo, livelli più difficili; vincendo si guadagnano barche più veloci. Non toglie nulla alla modalità libera.

Visione (settembre 2026): **tornei al centro** della schermata di carriera e, ai lati, **scuole da sbloccare** per livello (principiante, intermedio, avanzato) e per tipo di barca, con pochi corsi mirati sulla barca nuova; un **esame per categoria** dà il brevetto per gareggiare con quella barca. Le tendine per livello nel riquadro della Scuola serviranno quando arriverà la seconda barca (fase C): con una barca sola le 11 voci attuali sono tutto il livello principiante.

Idea (settembre 2026): **più brevetti progressivi.** Un primo brevetto facile dà accesso alle regate con le barche di oggi; piazzandosi bene in un campionato si accede al brevetto successivo, più restrittivo (prove a tempo, meno errori ammessi). L'esame si supera o si viene rimandati. I nomi dei brevetti restano generici e con la scritta «nessun valore legale»: niente «patente» o «patentino», che richiamano titoli ufficiali.

Aggiornamento (ottobre 2026, numeri provvisori da tarare giocando; tutto in `VISIONE-LIVELLI-E-CARRIERA.md`):

- **Meriti**: quattro aree (abilità, competizione, conoscenza, esperienza) con punti e un minimo per area. Non servono tutti gli ori. Il totale e i minimi aprono l'esame; l'esame resta obbligatorio e consegna il brevetto.
- **Ruoli**: si guida un solo ruolo; per il brevetto servono almeno due ruoli.
- **Libretto**: schermata che mostra i meriti e dice sempre cosa manca; registra, non punisce.
- **Importazione facoltativa** dei progressi del gioco libero all'inizio della carriera (lezioni, medaglie delle prove, quiz); tornei ed esame restano da fare in carriera.
- Il livello 1, già giocabile, fa da banco di prova dei punteggi.

## Fase F — Condivisione tra amici

Classifiche comuni e fantasmi condivisi («sfida il record di un amico»).

- Su claude.ai è possibile con l'archivio condiviso delle pagine pubblicate.
- Su GitHub Pages serve un servizio esterno per i dati, per esempio un database gratuito ospitato. Va valutato a parte.
- In entrambi i casi non c'è protezione contro chi bara: va bene tra amici, non per una classifica pubblica.

## Dopo la 1.0

Idee nuove, fuori dal piano attivo. La lista più ampia «dopo la 1.0» sta in `PIANO-GENERALE.md` («Fuori dalla 1.0» e «Dopo la 1.0, solo se si decide di continuare»); qui si aggiungono tre righe nate dalle schede dei video dell'11 ottobre 2026 (fonti informali, mai usate per tarare il motore).

- **Spingere il boma a mano / randa a collo.** Nelle fonti è il metodo preferito per uscire dall'angolo morto; il gioco non ha un comando per farlo (oggi si esce solo con la barra). Richiede un comando nuovo e un momento di imbardata della vela nel motore. **Decisione di Ale (16 ottobre 2026): va nel livello 2 (oggi: 1b)**, come novità con una proposta sua (tasto A o Z, fisica della vela spinta al contrario, lezione 5 da riscrivere col metodo delle fonti). **Precisazione di Ale (16 ottobre 2026, dopo la 1.0.13):** nel livello 2 l'uscita dall'angolo morto **non sarà automatica**: si spinge il boma col tasto apposito ed è quello che fa partire la barca in retromarcia, non lo fa più da sola. Quindi in quel compito vanno rivisti insieme la prua che poggia da sola (`ironsYaw`, senza fonte) e la retromarcia che parte da sola con la vela che sbatte (`archivio/PROPOSTA-CORREZIONI-PASSI.md` §2), e la lezione 1 «Ripartire».
- **Fiocco a collo (livello 3, il fiocco).** Aiuto per virare e per uscire dall'angolo morto con poca velocità; arriva con il fiocco nel gioco. Nessuna fonte quantitativa (vedi `DUBBI-E-RICERCHE.md`, sez. 3).
- **Materiale per lezioni ed esame dalla scheda di Lee (uscita dagli angoli morti), da rileggere nell'originale.**
- **Testo di fine regata «N° su 4» con le penalità (0.21).** È scritto all'istante dell'arrivo, quando chi non è ancora arrivato sta per forza dietro: con una penalità può essere ottimistico, perché un avversario che taglia la linea poco dopo può avere un tempo netto migliore. Il piazzamento salvato invece è quello definitivo. Nel collaudo della 0.21 i due numeri differiscono spesso (vedi `CHANGELOG.md`, 0.21). Il testo non si è toccato per la 1.0.
- **Tempo alla linea prima del via (osservazione 24, 12 ottobre 2026).** «T s alla velocità attuale» divide la distanza dalla retta della linea per la sola componente della velocità verso il vento: di lato e quasi paralleli alla linea dà numeri alti, poi crolla appena si orza. Da decidere: calcolarlo verso il punto della linea fra le boe più vicino, oppure nasconderlo quando la barca non va verso la linea.
- **Pannello di fine regata tagliato a circa 595 px di altezza (osservazione 34, 13 ottobre 2026).** In una finestra Chrome normale il pannello viene tagliato; da unire al difetto di pannello già noto a 1360×650. Non dimostrato che dipenda dalla 0.21.2; il pannello scorre con la barra laterale; la rotellina non è stata provata; testo errori troncato in lezione 2 (obs 35).
- **Peso dell'equipaggio (13 ottobre 2026).** Automatico (75 kg, braccio 1,0 m, `hike` calcolato dalla fisica), non controllabile dal giocatore; nessun effetto diretto su scarroccio o velocità (indirettamente sì, tramite lo sbandamento: righe 413 e 422 di `index.html`, vento catturato e resistenza). Il timoniere cambia lato di colpo con `S.boomSide` mentre il boma si sposta gradualmente (solo grafica).
- **Avversaria bloccata in regata (osservazione 27, 13 ottobre 2026, causa non stabilita).** Nella 0.21.2, in un rilancio di `collaudo_regate.py` a bastone, una regata si è bloccata (Verde, tratto 2); 36 corse successive (18 sul codice nuovo, 18 su HEAD) senza blocchi. Possibile legame con l'osservazione 27 (Blu piantata che non riparte), non provato. Da riprovare con molte regate e, se riappare, registrare la posizione e il vento del blocco.
- **Segnavento, boma e albero sdraiato (osservazione 23, 12 ottobre 2026).** Il segnavento giallo in cima all'albero indica da dove arriva il vento apparente, al contrario della freccia «apparente», e si confonde con essa; boma e albero sdraiato sembrano vettori. Dalla 0.21.2 il segnavento è nel glossario e il manuale ha il blocco «Cosa si vede sul mare»; i tratti scuri sono stati confermati da Ale (boma, barra, timone, albero inclinato); resta da decidere, dopo la 1.0, se rendere il segnavento più riconoscibile. Il testo delle lezioni 1-3 non lo spiega.
- **Frequenza delle partenze anticipate degli avversari (osservazione 25, 12 ottobre 2026).** Misurato 20-30% allo sparo, ma mai valutato come numero; Ale giocando ne vede circa due su tre. Da decidere quanto spesso dovrebbero anticipare e cosa succede loro.
- **Avversari che girano in tondo sulla linea d'arrivo (osservazione 26, 12 ottobre 2026).** Dopo l'arrivo disturbano chi sta ancora arrivando. Da verificare nel codice e decidere cosa fanno dopo l'arrivo.
- **Contatti senza colpa: chiusa nella 0.21.1 (osservazione 28, 13 ottobre 2026).** `regTotal()` somma `contactsPen`: un contatto senza colpa resta scritto ma non toglie stella, «pulita» e bonus +1.
- **Colpa decisa solo da mure e posizione (13 ottobre 2026, dopo la 0.21.1).** Con le stesse mure la colpa è di chi è sopravento, a prescindere da chi ha cambiato rotta. Quindi provocare un contatto da sottovento costa al giocatore solo il rallentamento (`u *= 0.6`, comune a entrambe le barche), mentre l'avversario prende 15 s e a lui non toglie la «pulita». Da riprendere con le regole 14 e 16 (evitare il contatto; chi ha la precedenza non deve cambiare rotta in modo da non lasciare spazio).
- **Stesse mure senza affiancamento (13 ottobre 2026, ipotesi da verificare).** Con le stesse mure `contacts()` dà torto a chi ha la y minore, cioè il più sopravento, senza guardare se le barche sono affiancate. Di bolina la barca davanti ha di solito la y minore: se l'altra la tampona da dietro, il torto andrebbe a quella davanti; in poppa l'inverso. Non provato con un caso. Da confrontare con il regolamento (ricordo non verificato: chi arriva da dietro e non è affiancato deve stare lontano).
- **Rendere deterministico il caso h di collaudo_registro.py (passi fissi e seme, come gli altri collaudi).**
- **Forma del contatto fra le barche (osservazione 33, 12 ottobre 2026).** Oggi è un cerchio di 4,2 m fra i centri: in fila le barche si toccano davvero, fianco a fianco restano circa 2,8 m di mare. Da decidere se usare la forma dello scafo (per esempio due cerchi lungo la barca o un'ellisse), sapendo che cambiano contatti, penalità e i collaudi delle regate e dell'aggressiva, le cui distanze (14, 15, 22 m) sono state tarate con il cerchio.
- **Record dei tempi delle regate mescolato fra i livelli (0.21).** Dalla 0.21 il piazzamento si salva per livello degli avversari (`r0.2:principianti`, `r0.2:esperti`), ma tempo migliore, stella e fantasma hanno ancora una sola chiave per regata (`r0.2`, `r1.2`): un record fatto da soli («nessuno») vale come uno fatto contro gli esperti. Separarli azzererebbe record, stelle e fantasmi delle regate (come le prove nella 0.19).
- **Vela disegnata con la parte alta lunga quanto il boma (osservazione 41, 14 ottobre 2026).** Vista dall'alto la randa dovrebbe restringersi verso la penna, con la balumina che torna dalla fine del boma verso l'albero; oggi il disegno è un cuneo chiuso da un tratto dritto. Solo disegno. Ale: proposta in coda, dopo il programma della 1.0, con schermate prima e dopo.

## In secondo piano (non cancellato)

- Mare aperto e navigazione in solitaria su lunghe distanze, con tempo accelerato.
- Vista 3D con camera dietro la barca.
- Regate in tempo reale tra più persone.

## Decisioni prese nella versione 0.15

- Registro degli errori anche nelle lezioni, tranne l'errore che il passo chiede apposta.
- Errori sempre visibili durante il gioco; segno ★ nel menu per prove e regate completate senza errori.
- Pannello leggibile senza scorrere su uno schermo 1360×768; istruzioni in un riquadro sul mare a gioco fermo.

## Decisioni prese nella versione 0.14

- Andatura nel pannello nascosta nelle lezioni 1 e 2.
- Boe da lasciare a sinistra, in prove e regate.
- Barra che torna al centro: spenta di default in prove e regate, riattivabile.

## Decisioni aperte

| Decisione | Opzioni |
| --- | --- |
| Regole di regata | Giri di penalità invece dei 15 secondi; penalità per il contatto con la boa. |
| Licenza | MIT (attuale) o una licenza non commerciale (vedi `LICENSE`). |
| Aiuti in carriera | Valgono per i meriti o no (tocca il principio 3 di `PROGETTO.md`). |
| Rosa dei candidati dell'equipaggio | Profili, quanto cambiano, valore del tetto del bonus. |
| Ordini all'equipaggio | Tasti e presentazione a schermo; preavviso minimo di ogni manovra. |
| Fiocco a farfalla | Come entra nel gioco (lato opposto, asta) e da quale livello. |
| Tasti con due vele | Decisa il 6 ottobre 2026 e cambiata il 7 ottobre (0.19.2): per ogni ruolo il comando principale è su W S; le altre coppie verticali (E D, poi altre da scegliere evitando R) solo se il ruolo ha più comandi; A e Z restano liberi per funzioni speciali; Q è il tasto vista (dalla 0.19.2). Barra con ← →, Spazio e M restano come sono. **Promemoria di Ale (16 ottobre 2026): R (raddrizzare la barca) va spostato su A o Z**, perché R serve alla coppia R F; da fare prima di introdurre le coppie E D e R F, con lezioni e testi che citano R. L è il tasto del laboratorio (1.0.4). Dettagli in VISIONE-LIVELLI-E-CARRIERA.md. |
| Livelli 4 e oltre | Ruoli, regole, quali barche entrano davvero. |
