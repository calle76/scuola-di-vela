# Roadmap

Aggiornata al 4 ottobre 2026.

Il disegno dei livelli, dei ruoli, dei meriti e della carriera è in `VISIONE-LIVELLI-E-CARRIERA.md`; le fonti pubbliche consultate in `FONTI-PUBBLICHE.md`. Dove questa roadmap e la visione dicono cose diverse sulle fasi C ed E, vale la visione.

## Principi che valgono per ogni fase

- **Tutto sempre giocabile**: nessun contenuto va sbloccato nella modalità libera.
- La **carriera** sarà una modalità separata e facoltativa, con salvataggio proprio. Il menu avrà un primo bivio: **gioco libero** (tutto sbloccato, il menu a riquadri di oggi) oppure **carriera**.
- Nei titoli del gioco si dice **brevetto**, mai «patente» o «patentino».
- **Confini legali**: niente marchi, niente titoli che sembrino ufficiali, dati esterni solo con licenza libera e citazione.
- Ogni novità si collauda **guidando davvero la barca** (vedi `COLLAUDI.md`), non solo leggendo il codice.

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

Scartato: pulsante «Schermo intero» nel gioco. Sul PC di prova lo schermo intero di Chrome con MATE torna subito indietro anche dal menu di Chrome (non dipende dal gioco); con Firefox F11 funziona.

## Fase B — Tornei e classifiche personali

- Tornei di più regate contro gli avversari del computer, con il sistema a punti delle regate (1 punto al primo, 2 al secondo, e così via; vince chi ne ha meno), eventualmente con uno scarto.
  - Struttura decisa in via provvisoria (ottobre 2026): 4 regate con uno scarto, ruolo bloccato per tutto il torneo, più tornei per categoria con condizioni diverse (vento leggero, vento teso, raffiche, salti di vento). Dettagli in `VISIONE-LIVELLI-E-CARRIERA.md`. Gli avversari vanno resi affidabili su più regate (la 0.17 ha già ridotto ritardi al via e partenze anticipate, vedi `CHANGELOG.md`).
- Classifica dei record personali per prova e regata.
- Avversari «esperti» più forti: virate più rapide, scelta del bordo migliore, uso delle raffiche.
- **Copertura del vento (cono d'ombra):** una vela toglie vento alle barche sottovento, lungo la direzione del vento apparente; una barca poco sottovento e avanti devia il vento verso chi sta dietro sopravento. Oggi il vento non dipende dalle altre barche. Richiede: vento che dipende anche dalle barche, avversari che sappiano uscire da una copertura (altrimenti rallentano e si ammucchiano), record delle regate da azzerare. Le prove non cambiano. Eventuale disegno del cono sull'acqua come aiuto disattivabile. Valori da verificare prima (vedi `CONTENUTI-DA-VERIFICARE.md`).
- **Difetto degli avversari, ridotto nella 0.17:** in circa una partenza su cinque un avversario partiva in anticipo o con più di un minuto di ritardo. Con posizioni di partenza casuali e caratteri diversi (prudente, normale, aggressiva) la mediana del ritardo al via è scesa da circa 9 a 3–6 secondi e le partenze anticipate sono 3 su 90 con i principianti e 0 su 90 con gli esperti (misure e limiti nel `CHANGELOG.md`).

## Fase C — Più tipi di barca: ogni livello è una barca con cose nuove da imparare

Aggiornata a ottobre 2026; dettagli in `VISIONE-LIVELLI-E-CARRIERA.md`.

Il motore è parametrico: una barca nuova è un nuovo insieme di costanti più un disegno. Ciò che distingue un livello dall'altro non è solo la velocità o l'avversario più forte, ma cose nuove da padroneggiare: vele, equipaggio, tecnologia, informazioni. Una novità principale per livello.

| Livello | Barca (nomi generici) | Ruoli | Novità principale |
| --- | --- | --- | --- |
| 1 | Deriva da regata, un solo velista (la barca attuale) | Timoniere | Le basi |
| 2 | Deriva a due: randa e fiocco | Timoniere, prodiere | Il fiocco e il coordinamento a due |
| 3 | Deriva a due con gennaker | Timoniere, prodiere | Vela di portanza, planata, strumenti, angoli limite |
| 4 | Equipaggio da tre | Timoniere, trimmer, tattico | Il tattico elabora le informazioni |
| 5-6 | Catamarano; cabinato | Da definire | Vento apparente dominante, scuffia diversa; inerzia, mare, correnti |

Si pianifica nel dettaglio fino al livello 3; gli altri sono una direzione, non un impegno. Una deriva scuola (lenta, stabile, che perdona gli errori) resta un'idea per un eventuale livello 0.

**Prototipo del fiocco** (`sperimentale/fiocco.html`, in corso). È il primo passo, perché il rischio maggiore è la fisica delle vele. Non tocca `index.html`.

- Tappa A (il fiocco come seconda vela con scotta propria): fatta e approvata.
- Tappa B (la randa che copre il fiocco alle andature larghe, con messaggi del pannello per il fiocco): fatta e approvata dopo il giudizio di chi gioca.
- Tappa C (coerenza fra vista e forza del fiocco coperto, momento di imbardata dovuto alle vele, fiocco in virata, massa dello scafo a due): da fare.
- La manovra a farfalla (fiocco dal lato opposto) non è nel prototipo; da modellare più avanti.
- Fisica e criteri nel dettaglio: `FISICA-E-TARATURE.md`. Fonti: `FONTI-PUBBLICHE.md`. Regole di lavoro dei prototipi: `SPERIMENTALE.md`.

Ordine di sviluppo dopo il prototipo: ruolo del prodiere, equipaggio guidato dal computer, tornei con i meriti, menu carriera.

Nelle regate miste: compenso di tempo tra barche diverse, come nelle regate reali.

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
| Tasti con due vele | Barra ← →, randa A e D, fiocco Q ed E nel prototipo; ripensare A S D W del gioco a una vela. |
| Livelli 4 e oltre | Ruoli, regole, quali barche entrano davvero. |
