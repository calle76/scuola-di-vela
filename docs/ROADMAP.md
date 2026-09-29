# Roadmap

Aggiornata al 29 settembre 2026.

## Principi che valgono per ogni fase

- **Tutto sempre giocabile**: nessun contenuto va sbloccato nella modalità libera.
- La **carriera** sarà una modalità separata e facoltativa, con salvataggio proprio.
- **Confini legali**: niente marchi, niente titoli che sembrino ufficiali, dati esterni solo con licenza libera e citazione.
- Ogni novità si collauda **guidando davvero la barca** (vedi `COLLAUDI.md`), non solo leggendo il codice.

## Fase A — Misura degli errori, brevetto ed esame

1. ~~**Registro degli errori**~~ in lezioni, prove e regate: **fatto nella 0.15** (definizioni nel `CHANGELOG.md`). Registra anche i dati che serviranno all'esame e alla carriera; le regole di promozione (numero massimo di errori, tempi limite) si decideranno lì.
2. **Fasce di tempo** per le prove (bronzo, argento, oro), tarate sui tempi degli avversari esperti **dalla 0.14 in poi** (il giro di boa vero ha allungato i tempi), con vento fisso durante i tentativi validi.
3. **Esame a risposte chiuse**: banca di 80–100 domande, 20 estratte a caso, soglia 80%. Due tipi:
   - glossario (come i quiz attuali);
   - situazioni con un piccolo disegno di barca e vento («che andatura è?», «cosa fai se entra una raffica?», «chi ha la precedenza?»).
4. **Brevetto della Scuola di vela**, a livelli (per esempio «Timoniere di deriva», poi «Regatante»), con attestato stampabile. Nessun valore legale, e deve essere scritto.

### Ordine delle versioni della fase A

| Versione | Contenuto |
| --- | --- |
| 0.15 | Registro degli errori, pannello ordinato, segno «senza errori» (fatto) |
| 0.16 | Menu principale a riquadri e fasce di tempo; lezione 1 con il solo timone; rosa dell'angolo morto; freccia della velocità; pannello ridotto (dettagli sotto) |
| 0.17 | Esame a risposte chiuse, nel suo riquadro del menu |
| poi | Brevetto con attestato |

Il quiz di ripasso resta subito dopo ogni lezione; l'esame per il brevetto è separato, perché riguarda tutte le lezioni.

### Contenuto della 0.16 (deciso il 29 settembre 2026, dopo il collaudo della 0.15)

1. **Menu principale a riquadri**, tutto visibile in una schermata: Scuola (lezioni e prove nell'ordine consigliato), Regate, Ripasso ed esame, Navigazione libera, In arrivo; Glossario in alto.
2. **Fasce di tempo** bronzo, argento e oro, mostrate nel menu insieme alla ★.
3. **Lezione 1 con il solo timone.** Via i pulsanti Orza e Poggia (tasti A e D): un comando riferito al vento non si comporta come una barra, e tenendolo premuto la barca attraversava il vento continuando a «orzare». I passi si fanno con le frecce ← →; «orzare» e «poggiare» restano nei testi e in una scritta che, mentre la barca gira, dice se sta orzando o poggiando. Cazza e Lasca restano. Versione minima: niente riorganizzazione delle lezioni 1 e 2. Controllare le domande del ripasso che citano i pulsanti.
4. **Rosa dell'angolo morto** accanto all'indicatore di sbandamento: vento sempre in alto, settore di 40° per lato in rosso, lancetta della prua che diventa rossa dentro il settore. Stesso limite della voce «Andatura» e del registro. Aiuto del gioco: nelle impostazioni, acceso di norma, disattivabile.
5. **Freccia della velocità** dal centro della barca, nella direzione in cui la barca si muove davvero (mostra lo scarroccio; all'indietro esce dalla poppa), lunga in proporzione alla velocità, nascosta sotto qualche decimo di nodo, di colore diverso dalle frecce del vento. Il triangolo reale + moto = apparente solo nella lezione 4.
6. **Pannello ridotto** in prove e regate, da decidere sulle schermate dopo aver visto rosa e freccia. Proposta: togliere Sbandamento, Scarroccio, Vento reale e Vento apparente (quest'ultimo resta nella lezione 4); tenere Velocità, Andatura, Prua e Rilevamento boa.

Scartato: pulsante «Schermo intero» nel gioco. Sul PC di prova lo schermo intero di Chrome con MATE torna subito indietro anche dal menu di Chrome (non dipende dal gioco); con Firefox F11 funziona.

## Fase B — Tornei e classifiche personali

- Tornei di più regate contro gli avversari del computer, con il sistema a punti delle regate (1 punto al primo, 2 al secondo, e così via; vince chi ne ha meno), eventualmente con uno scarto.
- Classifica dei record personali per prova e regata.
- Avversari «esperti» più forti: virate più rapide, scelta del bordo migliore, uso delle raffiche.
- **Copertura del vento (cono d'ombra):** una vela toglie vento alle barche sottovento, lungo la direzione del vento apparente; una barca poco sottovento e avanti devia il vento verso chi sta dietro sopravento. Oggi il vento non dipende dalle altre barche. Richiede: vento che dipende anche dalle barche, avversari che sappiano uscire da una copertura (altrimenti rallentano e si ammucchiano), record delle regate da azzerare. Le prove non cambiano. Eventuale disegno del cono sull'acqua come aiuto disattivabile. Valori da verificare prima (vedi `CONTENUTI-DA-VERIFICARE.md`).
- **Difetto noto degli avversari:** in circa una partenza su cinque un avversario parte in anticipo o con più di un minuto di ritardo (con 1 minuto di preparazione i ritardi sono più frequenti). Le regate si concludono comunque.

## Fase C — Più tipi di barca

Il motore è parametrico: una barca nuova è un nuovo insieme di costanti più un disegno.

| Barca (nomi generici) | Caratteristiche |
| --- | --- |
| Deriva scuola | Lenta, stabile, perdona gli errori |
| Deriva singola da regata | La barca attuale |
| Catamarano | Molto veloce, vira male, scuffia in modo diverso |
| Deriva a due vele | Fiocco con la sua scotta: serve un secondo comando |
| Cabinato | Non scuffia, sbanda, molta inerzia: base per il carteggio |

Nelle regate miste: compenso di tempo tra barche diverse, come nelle regate reali.

## Fase D — Carteggio (resta in programma)

1. Gradi e direzioni: rosa dei venti, prua in gradi, rilevamento.
2. Velocità, tempo, distanza: nodi e miglia, punto stimato.
3. Fare il punto: due rilevamenti e il loro incrocio.
4. Il segnalamento: boe laterali e cardinali, fari.
5. Nord vero e nord magnetico.

Serve una vista «carta nautica» accanto a quella di navigazione. Per coste reali: OpenStreetMap (licenza ODbL, citazione obbligatoria) e GEBCO per le profondità. Le carte nautiche ufficiali sono protette e non vanno riprodotte.

## Fase E — Modalità carriera

Percorso facoltativo: brevetto ed esame, regate di circolo, livelli più difficili; vincendo si guadagnano barche più veloci. Non toglie nulla alla modalità libera.

Idea (settembre 2026): **più brevetti progressivi.** Un primo brevetto facile dà accesso alle regate con le barche di oggi; piazzandosi bene in un campionato si accede al brevetto successivo, più restrittivo (prove a tempo, meno errori ammessi). L'esame si supera o si viene rimandati. I nomi dei brevetti restano generici e con la scritta «nessun valore legale»: niente «patente» o «patentino», che richiamano titoli ufficiali.

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
