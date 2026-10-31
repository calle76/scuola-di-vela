# Proposta: un riquadro per le bandiere e le penalità, e l'avviso «sei oltre la linea» (livello 2a)

31 ottobre 2026. **Fermata 1: solo documento, nessun codice toccato.** Nasce dalla prova a mano di Ale sulla 1.0.68 (registrazione `sessione-20261030-2233.txt`).

## Che cosa ha osservato Ale

1. Le bandiere sulla barca giuria sono piccole (circa 15 pixel) e si vedono male. Ale chiede di mostrarle **in grande**, in un riquadro in evidenza, con i messaggi delle bandiere e quelli delle penalità («Hai urtato…», «Hai fatto un giro…», «Penalità scontata»), che oggi stanno in piccolo nel pannello a destra.
2. Passando la linea a 35 e a 30 secondi dallo sparo non è comparsa la X; è comparsa passandola a meno di 10 s. Ale chiede se è un difetto.
3. Ale ha risposto: la sistemazione può stare **in alto sul mare** (l'angolo in alto a sinistra è libero: il vento è accorpato a destra), **non deve appesantire il gioco**, e l'avviso «sei oltre la linea» va fatto **disattivabile**.

## Il punto 2 non è un difetto (misurato e letto dalla fonte)

- Regola 29.1 (F15, testo letto nel PDF `fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, parafrasato): la X sale solo se, **nel momento dello sparo**, una parte dello scafo è dal lato del percorso. Chi supera la linea prima e torna dietro prima dello sparo non è richiamato e non paga niente.
- Nella registrazione: nella regata con sparo a 573,4 s la barca è oltre la linea fra i 540 e i 550 s circa, torna dietro verso i 552 s, e allo sparo è a 1,9 m dietro la linea (y positiva = prima della linea; la linea è a y ≈ 0, come mostra il «partito» a 50,9 s della prima regata). Nessuna X è corretta. Se si supera la linea a meno di 10 s dallo sparo non si fa in tempo a tornare indietro: sei ancora oltre allo sparo e sale la X. Il gioco fa quello che dice la regola.
- Conseguenza: oggi il giocatore non ha modo di sapere, prima dello sparo, che è oltre la linea (il rettangolo diventa rosso solo dopo lo sparo). Da qui l'avviso.

## Oggi [codice]

- Bandiere: `drawBandiere` (`js/regate.js:761`), coordinate del mondo, dentro la barca giuria; misura minima 12 px per 1,5 m di larghezza. Quali sono su: `bandiereR()` (classe, P, X, blu).
- Messaggi dei segnali: `toast(...)` al centro (`js/disegno.js:336`, 2,6 s, y = 100 px in regata); sono registrati dal registratore (`S.toast`).
- Messaggi di colpa e giri: `R.lastRule`, mostrata nel pannello a destra (`#rRule`, `js/regate.js:903`); e qualche `toast`.
- Angolo in alto a sinistra del mare: libero (commento a `js/disegno.js:699`). Bussola e vento in alto a destra, orologio al centro.

## Proposta (modello più semplice)

**Un solo riquadro disegnato sul mare, in alto a sinistra, solo nelle regate con `R.segnali` (oggi la «Regata con i giri di penalità»).** Nessun elemento nuovo nella pagina (niente DOM, niente immagini): una funzione `drawRiquadro` che disegna rettangoli e testo, chiamata da `drawRaceScreen`. Fuori da quella regata non disegna niente.

Contenuto, dall'alto:
1. **Le bandiere esposte**, grandi (circa 44 × 30 px), nello stesso ordine della giuria (classe, P, X, blu), ciascuna con il nome sotto («Classe», «P», «X», «Blu») perché non dipendano solo dal colore. Si disegnano con la **stessa** funzione della giuria (la `drawBandiere` diventa una `drawBandiera(tipo, x, y, larghezza, altezza)` usata da tutte e due), così disegno e riquadro non possono diventare diversi.
2. **Una riga di significato**, per esempio: «Preparatorio: P alzata, partenza tra 4 minuti» · «Sei partito in anticipo: torna dietro la linea (X)» · «Dopo il via: la linea è d'arrivo (blu)».
3. **La riga delle penalità**, solo se c'è un debito: «Penalità: 2 giri · fatti 1» (e il motivo breve: «urtato la Rossa», «toccata la boa»); mentre scontano: «Stai scontando: lascia strada»; a debito chiuso: «Penalità scontata» per 6 s.
4. **L'avviso «sei oltre la linea»**, in giallo, prima dello sparo: «Sei oltre la linea: torna dietro prima dello sparo (se sei ancora qui, sale la X)». Si usa **lo stesso test** che decide la X allo sparo (scafo oltre la linea), così avviso e bandiera non possono contraddirsi. **Agganciato a «Suggerimenti»** (`opt.hint`, già nelle impostazioni): spento, l'avviso non c'è. Le bandiere e le penalità nel riquadro restano.

**Quando si vede.** Il riquadro compare solo quando c'è qualcosa da dire: una bandiera appena cambiata (resta 10 s), la X, un debito di giri aperto, l'avviso. Se non succede niente per 10 s sparisce, così non copre il mare. Un cambio fa un breve lampo del bordo (1,5 s) per attirare l'occhio. Il testo lungo resta nella riga delle regole del pannello (non si toglie niente).

**Che cosa non cambia.** I `toast` dei segnali al centro restano come sono (li usano i collaudi e il registratore); solo se alla prova a mano il riquadro basta, in una versione dopo si possono togliere (decisione di Ale, qui sotto).

## Per non appesantire il gioco

- Disegno fisso sul canvas già in uso: da 5 a 15 rettangoli e 2-4 testi per fotogramma, solo quando il riquadro è visibile; niente immagini, niente nuovo elemento nella pagina, niente calcoli di fisica.
- Le misure del testo (`measureText`) si fanno **solo quando il testo cambia** (memorizzate), non a ogni fotogramma.
- Il pannello di destra non cambia: nessun rischio per il caso peggiore a 1360×650 (eccesso 0 px).

## Costanti nuove (tutte ipotesi nostre)

Dimensioni della bandiera (44 × 30 px), posizione (16 px dal bordo sinistro, 14 dall'alto), permanenza 10 s, «penalità scontata» 6 s, lampo 1,5 s. Fonti: nessuna nuova; bandiere e tempi sono quelli della fetta 3 (F15 26 e 29.1), i giri quelli della 44.2. Il gioco continua a non avere suoni (dichiarato).

## Criteri (soglie scritte prima; il metro è indipendente da ciò che si misura)

Per ogni criterio verifico con un metro che legge **i pixel disegnati**, non solo lo stato interno (un controllo scritto sullo stato passerebbe anche se il riquadro non si vedesse): nella zona del riquadro cerco i colori delle bandiere; e prima verifico che il metro li trovi, con un caso in cui la bandiera c'è.

- **Q1 bandiere = stato.** In tre sequenze (5, 3 e 1 minuto) e in almeno 600 istanti campionati, le bandiere che compaiono nel riquadro sono **le stesse** di `bandiereR()` in 100% dei campioni (soglia: 0 differenze); il metro trova almeno una bandiera in ogni sequenza.
- **Q2 la X.** 20 regate con partenza voluta in anticipo (superare la linea a −3 s e restare): X nel riquadro dopo lo sparo in 20 su 20 e tolta quando la barca è tornata dietro la linea. 20 regate in cui si supera la linea a −35 s o −30 s e si torna dietro prima dello sparo: X **mai** (0 su 20).
- **Q3 l'avviso.** Nelle 20 regate dell'ultimo caso di Q2, con «Suggerimenti» acceso: l'avviso compare quando lo scafo è oltre la linea e sparisce quando è tornato dietro, in 20 su 20; con «Suggerimenti» spento: mai (0 su 20). Vincolo: in nessun istante avviso e X sono in contraddizione (avviso acceso allo sparo ⇒ X in alto).
- **Q4 penalità.** Con `collaudo_giri.py` (contatti con colpa, 10 regate): dopo ogni colpa il riquadro dice «2 giri» e il contatore sale a 1 e a 2; «Penalità scontata» compare solo dopo il secondo giro valido; un giro nel verso opposto non lo fa avanzare.
- **Q5 sparisce.** Dopo 10 s senza novità e senza debito il riquadro non si vede (pixel della zona uguali al mare) in 100% dei campioni.
- **Q6 le altre regate non cambiano.** 20 regate dell'1a e dell'1b e il torneo: istantanee del motore **identiche al bit** alla 1.0.68 e **pixel della zona del riquadro identici** a quelli della 1.0.68 in 5 regate; `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici carattere per carattere.
- **Q7 costo.** Tempo di disegno del fotogramma della regata dei giri (almeno 600 fotogrammi, 5 ripetizioni, mediane, riquadro visibile contro non visibile e contro la 1.0.68): l'aggiunta non supera **0,2 ms** né **3%** del fotogramma. Il metodo è lo stesso di quelli precedenti; se il rumore è più grande della differenza, lo dico e non dichiaro una vittoria.
- **Q8 posto.** A 1360×650 e 1360×768, nessuna sovrapposizione con la bussola, il vento, l'orologio e il toast (controllo geometrico sui rettangoli) nel caso peggiore: il testo più lungo. Pannello a 1360×650 senza pixel di eccesso; `collaudo_pannello.py` e `collaudo_vista.py` verdi.
- **Q9 senza `#collaudo`.** In una pagina caricata come la carica un giocatore: nessun errore e il riquadro appare.
- **Q10 Firefox.** Lo guarda Ale a occhio, e solo lì si decide se le bandiere si leggono e se il riquadro dà fastidio. Collaudo in Chromium; Firefox da lanciare (nota in `COLLAUDI.md`).

## Rischi

- **Sovrapposizioni** con il toast (largo anche 600 px) se la finestra è stretta: Q8 le misura; se succede, il riquadro si ferma più in basso a sinistra.
- **Troppi avvisi insieme** (bandiera, penalità, oltre la linea): per questo il riquadro mostra al massimo 3 righe e ordina per importanza (X, penalità, avviso, bandiera).
- **Due strade per lo stesso messaggio** (toast e riquadro): per ora accettato; è una scelta di Ale se togliere i toast.
- **Colori**: le bandiere si riconoscono per colore; per questo il nome sotto.
- **Costo**: il rischio è piccolo ma lo misuro (Q7) e lo dico com'è.
- **Registratore e moviola** non registrano il riquadro, che è derivato dallo stato (bandiere già registrate come eventi `bandiere`).

## Da decidere (Ale)

1. **I toast dei segnali al centro restano** (consiglio, per ora) o si tolgono quando c'è il riquadro?
2. **Il riquadro sparisce dopo 10 s** (consiglio) o resta sempre visibile durante la regata?
3. **L'avviso «sei oltre la linea» dentro «Suggerimenti»** (consiglio: nessuna impostazione nuova) o con una casella tutta sua?
4. Va bene **in alto a sinistra**?

Versione prevista: **1.0.70** (la 1.0.69 è il menu, se si sceglie R2). Aggiornati con la versione: `VERSIONE`, `CHANGELOG.md`, `collaudo_segnali.py` (Q1-Q3), `collaudo_giri.py` (Q4), un collaudo nuovo per Q5-Q8.

## Cosa resta fuori

Altre bandiere (individuale «I», nera, richiamo generale, abbassamento…): non c'è nel regolamento la parte che servirebbe e non sono nel gioco. Le lezioni sui segnali (dentro «La scuola») useranno le stesse bandiere grandi: la funzione condivisa serve anche a quelle.
