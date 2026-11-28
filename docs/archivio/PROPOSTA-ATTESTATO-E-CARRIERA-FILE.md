# Proposta: entrata in Deriva (Coach e sponsor), attestato in un file, carriera in un file

*20 novembre 2026. Voci 64 e 54 di `DA-FARE.md`. Via di Ale al codice dato il 20 novembre insieme alla richiesta di autonomia («50, 54, 64»): questa è la fermata 1 scritta prima del codice, con le scelte che ho preso io (da guardare con Ale) e le soglie fissate prima di misurare.*

## Da dove viene

- **64** (Ale, 18 nov): all'arrivo in Deriva lo sponsor e la presentazione del Coach («cosa si fa in questo livello»); un **attestato in un file** che fa ripartire sempre dall'inizio di Deriva senza rifare la Scuola. Serve a provare i grandi cambiamenti di Deriva. Lo sponsor in Deriva era stato escluso; la decisione è superata (`DECISIONI.md`, 18 nov).
- **54** (17 nov): paura di perdere i dati del browser; salvare e ricaricare **tutta** la carriera in un file, come «Riprendi dal mio file» della stagione.

## Il modello più semplice

**A. Carriera in un file (54).** Nel piede del menu, solo in carriera, due collegamenti: «Salva la carriera in un file» e «Carica una carriera». Il file contiene tutto il salvataggio della carriera (`progress`, con stagione, torneo, sponsor, punti di Deriva), i fantasmi e il nome; più `tipo: "carriera"`, `forma: 1`, la versione e la data. Caricare **sostituisce** la carriera del browser, dopo una conferma. Rifiutati: un file che non è una carriera (per esempio quello della stagione o l'attestato) e una `forma` più nuova di quella del gioco. Non c'è controllo della versione (come per la stagione dalla 1.3.16): il salvataggio è lo stesso da molte versioni.

**B. Attestato in un file (64).** Nella finestra dell'attestato della Scuola, «Salva l'attestato in un file»: `tipo: "attestato"`, `livello: "scuola"`, `forma: 1`, data, nome, voto e domande dell'esame, i punti delle quattro aree. Nel piede del menu della carriera, «Riparti da un attestato»: dopo una conferma la carriera del browser **ricomincia dall'inizio di Deriva**: Scuola superata con l'attestato del file, tutto il resto azzerato (lezioni, prove, record, fantasmi, Deriva, stagioni, sponsor). Il libretto della Scuola dice «Attestato caricato da un file» e l'attestato mostra i punti scritti nel file. Il menu passa a Deriva.

**C. Benvenuto in Deriva (64).** La prima volta che in carriera si apre il menu di Deriva, una finestra col volto del Coach (serio) e cinque righe: le lezioni 21-25, le regate e il torneo, la stagione del circuito con le tappe, la moviola col Coach e la rotta ottimale, le due strade per superare Deriva. Si vede una volta sola (`progress.dvBenvenuto`).

**D. Sponsor all'entrata (64).** Nella stessa finestra, se la carriera non ha ancora mai avuto uno sponsor né una stagione: le prime **due offerte** arrivano subito (gradini 1 e 2, zonali, come oggi alla fine della prima stagione di chi non arriva fra i primi 3). Come oggi, con offerte da scegliere la stagione non parte finché non se ne sceglie una. **Una regola in più** perché resti vero «fra i primi 3 dello zonale: diritto al nazionale»: a fine stagione zonale chiusa fra i primi 3, se fra le offerte non c'è uno sponsor nazionale se ne aggiunge uno del gradino 3. Prima serviva solo dalla seconda stagione in poi; ora che si parte con un contratto, serve dalla prima.

## Scelte mie (da guardare con Ale, si cambiano a basso costo)

1. Offerte all'entrata: gradini 1 e 2 (non 2 e 3: all'entrata non si sa ancora come va).
2. «Riparti da un attestato» azzera **tutto** il resto della carriera, Scuola compresa (le lezioni risultano da fare, ma Deriva è aperta). Prima della conferma il gioco consiglia di salvare la carriera in un file.
3. Il file si può modificare a mano: è un gioco personale, senza classifiche fra persone; lo dico, non lo impedisco.
4. L'attestato in un file dice «Nessun valore legale», come quello stampato.

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| C1 | Carriera salvata e ricaricata uguale | 5 carriere costruite (Scuola a metà, attestato, Deriva con stagione in corso, sponsor con contratto, Deriva superata): dopo salva → azzera → carica, `progress` e fantasmi identici (JSON) e il menu mostra le stesse righe del libretto; 5 su 5 |
| C2 | Rifiuti | file della stagione, attestato in «Carica una carriera», carriera in «Riparti da un attestato», `forma` 2, testo non JSON: rifiutati col loro messaggio e la carriera non cambia; 5 su 5 |
| C3 | Attestato | da una carriera con la Scuola superata: salva l'attestato, azzera, «Riparti da un attestato»: Deriva aperta, menu su Deriva, libretto della Scuola con «Attestato caricato», attestato coi punti del file, nessun record né lezione fatta; e da una carriera già in Deriva: stagione, sponsor e punti di Deriva azzerati |
| C4 | Benvenuto | compare la prima volta che si apre Deriva in carriera (anche subito dopo l'attestato caricato), una volta sola (riaprendo il menu 3 volte: 1 sola finestra); mai nel gioco libero |
| C5 | Sponsor all'entrata | carriera nuova in Deriva: 2 offerte (gradini 1 e 2) e «Inizia la stagione» bloccato finché non si sceglie; carriera che ha già sponsor o stagioni: offerte invariate |
| C6 | Primi 3 → nazionale | contratto del gradino 1 finito con la stagione zonale chiusa fra i primi 3: c'è un'offerta nazionale; chiusa 4°: nessuna nazionale aggiunta |
| C7 | Pannello | menu della carriera (Scuola e Deriva) e finestre nuove a 1360x650 con 0 px di eccesso, Chromium e Firefox |
| C8 | Come un giocatore | pagina senza `#collaudo`: salva e carica col file vero (download e scelta del file), 0 errori |
| N | Non-regressione | `collaudo_sponsor.py`, `collaudo_carriera_intera.py`, `collaudo_carriera_esame.py`, `collaudo_stagione_amico.py` verdi; `polare.js` e `raffiche_e_virate.js` identici |

## Costanti nuove

`CAR_FORMA = 1`, `ATT_FORMA = 1`: etichette del formato dei file, non ipotesi fisiche.

## Rischi

- **Sponsor dalla prima stagione:** chi entra in Deriva corre la prima stagione con obiettivi; prima la prima stagione era libera. È quello che Ale ha chiesto, ma cambia il ritmo verso il nazionale (con la regola D resta: primi 3 → offerta nazionale).
- **Benvenuto per chi è già in Deriva** (Ale, Lucio): la finestra compare una volta anche a loro; lo sponsor no, se hanno già giocato una stagione.
- **Pannello:** due collegamenti in più nel piede del menu possono mandarlo a capo; si misura (C7).

## Esito (20 novembre 2026, versione 1.3.23)

Fatto come scritto sopra, scelte 1-4 comprese. `tests/collaudo_carriera_file.py` (nel giro di `lancia_tutti.sh`), Chromium, una corsa col freno (picco 47 °C): **tutti i criteri verdi**, 25 controlli: C1 5 su 5, C2 5 su 5, C3 2 (con punti dell'attestato diversi da 0, dopo una prima stesura che li aveva tutti a 0 e quindi non misurava), C4 5, C5 3, C6 su 13 contratti finiti (5 fra i primi 3, 8 oltre, 0 sbagliati), C7 3 (0 px), C8 2. Firefox: nel prossimo giro su GitHub.

Una cosa in più, non prevista: con `#collaudo` il benvenuto è spento (come le istruzioni delle regate), perché la finestra aperta bloccherebbe i clic di tutti i collaudi che partono da una carriera in Deriva; il collaudo nuovo lo riaccende (`__sv.benvenuto = true`) e lo controlla anche in una pagina senza `#collaudo`. `collaudo_sponsor.py` non rilanciato qui: la regola dei primi 3 aggiunge un'offerta in coda e S2 confronta solo l'inizio della lista; da guardare nel giro su GitHub.
