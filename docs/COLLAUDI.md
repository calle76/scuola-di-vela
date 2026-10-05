# Collaudi

Il gioco si verifica in due modi. I collaudi della **fisica** girano con Node.js e leggono il motore direttamente da `index.html`. I collaudi nel **browser** aprono il gioco in Chromium senza finestra, premono tasti e leggono lo stato tramite l'aggancio `#collaudo`.

Regola del progetto: **ogni modifica a fisica, lezioni o avversari si verifica rilanciando i collaudi pertinenti.** Diversi difetti seri sono emersi solo così (vedi `CHANGELOG.md`).

## Installazione (una volta sola)

Serve Node.js (per la fisica). Per il browser serve un ambiente Python stabile: lo prepara `tests/prepara_ambiente.sh`.

```
tests/prepara_ambiente.sh --dry-run   # stampa cosa farebbe, senza installare nulla
tests/prepara_ambiente.sh             # prepara davvero l'ambiente
```

Lo script non tocca `index.html` né `sperimentale/`, non usa `sudo` e non installa nulla fuori dal progetto: crea un venv in `.venv-collaudi/` (cartella ignorata da git, aggiunta al `.gitignore` se manca), ci installa una versione fissa di playwright e controlla che il browser Chromium corrispondente sia già nella cache di sistema (`~/.cache/ms-playwright`). Se manca, stampa il comando per scaricarlo ma non lo esegue: va lanciato a mano. Alla fine apre `index.html` in headless e legge il titolo, e stampa `OK` oppure l'errore.

**Perché una versione fissa.** Ogni versione di playwright vuole una revisione precisa di Chromium, e scaricarne una nuova ogni volta è lento e può fallire offline. Nella cache di questo progetto c'era già `chromium-1223`, e la versione di playwright che lo vuole è **1.60.0** (la 1.58 vuole la 1208, la 1.63 la 1243): è quella che lo script installa, così non serve scaricare nulla.

**Se il browser in cache cambia** (per esempio su un'altra macchina, o dopo una pulizia della cache): lanciare `tests/prepara_ambiente.sh --dry-run` e leggere la riga `cache:`; se dice che `chromium-1223` non c'è, o si scarica quella revisione con il comando stampato dallo script, o si cambia `CHROMIUM_REV` e `PLAYWRIGHT_VERSION` in testa allo script per farli corrispondere a quello che c'è davvero (`python -m playwright install --dry-run chromium` dentro al venv dice quale revisione la versione installata si aspetta).

**Per lanciare un collaudo** si usa il python del venv, non quello di sistema, dalla cartella principale del progetto:

```
.venv-collaudi/bin/python tests/collaudo_quiz.py
```

(i collaudi trovano `index.html` e `tests/output/` da soli, quindi la cartella da cui si lancia il comando non conta; conta solo quale python si usa.)

## Fisica (Node.js)

```
cd tests/fisica
node polare.js              # velocità di equilibrio a vari angoli dal vento, con 6, 10 e 15 nodi
node raffiche_e_virate.js   # virate a diverse velocità e raffiche improvvise
```

Risultati attesi con il motore attuale, con 10 nodi: circa 3,4 nodi a 45°, 5,2 a 90°, 3,5 a 180° (fino alla 0.12 erano 3,8 a 45°: l'angolo morto più largo della 0.13 li ha ridotti). Virata riuscita in circa 4 s partendo a 3,9 nodi, fallita partendo quasi fermi. Raffica a 20 nodi senza reagire: circa 61°, cioè scuffia.

## Browser (Python e Playwright)

Da eseguire nella cartella `tests`. Le immagini finiscono in `tests/output/`.

| Script | Cosa verifica | Esito atteso |
| --- | --- | --- |
| `collaudo_schermate.py` | Apre ogni passo di ogni lezione, ogni prova e la navigazione libera | `errori: []` |
| `collaudo_lezioni.py` | Completa i passi pratici guidando la barca (dalla 0.16 la lezione 1 con le frecce del timone) | Tutti `OK`, salvo i casi di attesa noti indicati nello script |
| `collaudo_quiz.py` | I sei quiz e il salvataggio del miglior punteggio | Sei righe con il punteggio, `errori: []` |
| `collaudo_regate.py N T` | N regate accelerate, tipo T (0 a bastone, 1 nelle raffiche) | Tutti gli avversari arrivano, nessuno `BLOCCATA` |
| `collaudo_partenze.py [partenze per tipo] [livello]` | Ritardo degli avversari al via con 1, 3 e 5 minuti; geometria delle posizioni iniziali (distanza minima fra le barche e coppie in rotta di collisione); caratteri assegnati | Con 3 e 5 minuti, ritardo mediano entro circa 12 s e nessuna partenza anticipata; distanza minima all'avvio almeno 20 m; avvicinamento minimo almeno 14 m; con gli esperti una sola aggressiva, con i principianti nessuna |
| `collaudo_aggressiva.py [incontri]` | Il giocatore si trova mure a sinistra davanti all'avversaria aggressiva, a quattro distanze. Lo stesso incontro viene riprovato con manovre diverse (poggia subito, poggia un secondo dopo, orza un secondo dopo, niente), salvando e rimettendo lo stato della regata | In ogni incontro almeno una manovra iniziata un secondo dopo evita il contatto. Attenzione: la manovra del collaudo non va legata a `AGGRO_OFF`, altrimenti con una soglia larga e un incontro ravvicinato non parte e le righe misurano tutte la stessa cosa |
| `collaudo_strambata.py K N` | N strambate con vela aperta e K nodi | 6 nodi: nessuna scuffia; 15 nodi: scuffia sempre |
| `collaudo_rotta.py [fermi] [correzioni]` | Esercizio «Tenere la rotta»: molti tentativi a mani ferme e alcuni con un pilota che corregge, a passi fissi con `__sv.run`, entrando dal traverso e dalle andature larghe | `senza correzioni: completati 0 su 25`; con correzioni tutti completati in circa 8 s |
| `collaudo_fantasma.py` | Avversari esperti e salvataggio del fantasma | Tutti arrivano; fantasma salvato e visibile |
| `collaudo_registro.py [casi]` | Provoca ogni errore guidando la barca: prova pulita con stella nel menu, boa dal lato sbagliato, barca piantata, strambata a vela aperta, scuffia, partenza anticipata, linea fuori dagli estremi, contatto; nelle lezioni, gli errori richiesti dal passo | `13 su 13 verifiche riuscite` |
| `collaudo_pannello.py [larghezza altezza]` | Altezza del pannello in ogni passo di lezione, nelle prove, in navigazione libera e in regata; riquadro delle istruzioni (gioco fermo, Invio, riapertura) e riquadro iniziale della regata nel gioco vero, senza `#collaudo` | `pannello che eccede: nessuno` a 1360×650 e 1360×768; sei `True`, `errori: []` |
| `collaudo_suggerimento.py [larghezza altezza]` | Il suggerimento della vela alle andature portanti: con la scotta tutta lascata (1,00) il pannello dice «Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono.» e non più «lasca» o «troppo cazzata»; con la scotta a 0,90-0,99 il consiglio di prima resta. Più il caso peggiore dell'altezza del pannello, scrivendo i testi più lunghi nel suggerimento in ogni passo e modalità | `casi sbagliati: nessuno`, `eccesso massimo del pannello` tutto a 0 e uscita 0. Dichiara quanti casi ha misurato per ogni lato e **fallisce se sono zero** |
| `collaudo_fasce.py [ripetizioni] [prove]` | Taratura delle fasce di tempo: un pilota automatico percorre le prove a passi fissi di 1/60 s, con direzioni del vento diverse | Prove 1–4 con tempi identici per ogni vento (circa 87, 136, 185, 327 s); prova 5 intorno a 350 s, con alcuni tentativi non finiti (il pilota si pianta nelle raffiche) |
| `collaudo_giro_boa.py [casi]` | Un pilota automatico guida con barra e scotta: boa a sinistra, a dritta, sbagliata e corretta (prova 4), triangolo giusto e con la boa 2 a dritta (prova 5), prove 1–3 | Finisce solo quando la boa è girata a sinistra; `giri sbagliati` 1 nei casi sbagliati; prove 1–3 completate |

Il collaudo del giro di boa dura alcuni minuti; i casi si possono lanciare separatamente (per esempio `python collaudo_giro_boa.py ab`). Il pilota automatico è volutamente semplice: se non arriva, prima di dare la colpa al gioco controlla dove si è fermato (angolo morto, marcia indietro, scuffia).

Le regate usano il tempo accelerato, e ogni collaudo dura da pochi secondi a qualche minuto. Il collaudo completo del registro supera i 5 minuti: se l'ambiente ha un limite di tempo, si lancia a gruppi di casi (per esempio `ab`, `cde`, `fgh`, `i`; il caso `b` controlla la stella della prova 1 e va lanciato insieme ad `a`).

**Tempo accelerato e misure di tempo.** Con `__sv.fast(n)` la simulazione fa n passi per fotogramma, mentre un pilota automatico in `setInterval` reagisce in tempo reale: se il computer è carico (per esempio più browser aperti insieme) il pilota reagisce più di rado e i tempi misurati peggiorano. Nella 0.16 questo ha falsato la prima taratura delle fasce (108 s invece di 87). Per misurare tempi si usa `__sv.run(dt, n)`, che fa avanzare la simulazione a passi fissi senza il ciclo del browser, come fa `collaudo_fasce.py`.

**Riquadro delle istruzioni.** Con `#collaudo` il riquadro che ferma il gioco all'avvio di prove e regate viene saltato, perché i collaudi devono guidare subito. Per collaudarlo si scrive `__sv.skipBrief = false` (lo fa `collaudo_pannello.py`). Avversari e Preparazione stanno nel riquadro: i collaudi li impostano direttamente sui menu a tendina.

**Un collaudo che rimette a mano un'impostazione non collauda più quell'impostazione.** Scrivendo `__sv.skipBrief = false` si verifica come si comporta il riquadro *dato* che la variabile è falsa, non che il gioco vero la trovi falsa. Dalla 0.15 alla 0.17 non lo era, per una graffa mancante, e nessun collaudo poteva accorgersene perché tutti caricano `index.html#collaudo`. Per questo `collaudo_pannello.py` apre anche una seconda pagina **senza `#collaudo`** e controlla che il riquadro iniziale compaia entrando in regata dal menu e con «Ricomincia». Lo stesso vale per ogni altro valore di partenza: va verificato in una pagina caricata come la carica un giocatore.

**Caratteri.** Le misure del pannello dipendono dai caratteri. Se Barlow Semi Condensed e Source Serif 4 non sono installati, il browser senza finestra usa caratteri di riserva più larghi e le misure risultano peggiori del vero.

**Un collaudo che non parte passa sempre.** Nel prototipo del fiocco la verifica «senza `#collaudo`» cliccava `text=Navigazione libera`, che nel menu prende l'**intestazione** e non il pulsante: il gioco non partiva, tutte le letture del pannello erano «—», nessuna conteneva la frase cercata e il controllo di coerenza risultava soddisfatto. Un controllo scritto come «nessun caso sbagliato» è vero anche quando i casi sono zero. Ogni prova di questo tipo deve dichiarare **quanti casi ha davvero misurato** e fallire se sono zero.

## Limiti dei collaudi

- I collaudi guidano la barca con comandi prestabiliti: verificano che le cose **funzionino**, non che siano **chiare o divertenti**. Per quello servono persone che giocano.
- Alcuni risultati dipendono dal caso (raffiche, avversari): un singolo esito anomalo va ripetuto prima di concludere che c'è un difetto, ma un esito anomalo che si ripete è quasi sempre un difetto vero.
- **Un solo tentativo non basta nemmeno per dire che una cosa non succede.** Fino alla 0.16 `collaudo_rotta.py` provava una volta sola a mani ferme e concludeva che il passo «Tenere la rotta» non si completava da sé; in realtà si completava una volta su otto, e un collaudo su un tentativo lo vedeva quasi mai (vedi `CHANGELOG.md`, versione 0.17).
- **Un testo che dice «fai X finché non vedi Y, poi fermati» va verificato tenendo conto dell'inerzia della barra.** Nella 0.17, lezione 2, un testo scritto per fermarsi esattamente al bersaglio (tenendo la barra premuta fino al traguardo) sbandava per inerzia molto oltre la finestra richiesta dal passo, perché la barra si ricentra lentamente (`opt.autoCenter`) e la prua continua a girare dopo il rilascio. A piccoli colpi, con una pausa fra l'uno e l'altro, l'inerzia resta piccola e prevedibile: un testo per un passo con `tiller: true` e senza `turnHint` va tarato e provato così, non con una pressione continua fino al traguardo.
- **Per confrontare due versioni servono campioni grandi.** Nella 0.14 due confronti fatti su poche regate hanno mostrato peggioramenti inesistenti: le penalità per contatto (in realtà i contatti erano diminuiti, 22 contro 44 su 12 regate) e i ritardi al via (uguali su 36 partenze). Il collaudo delle partenze fa solo due partenze da 3 minuti: per un confronto se ne misurano almeno una decina per versione, meglio se sulla versione precedente nello stesso momento.
