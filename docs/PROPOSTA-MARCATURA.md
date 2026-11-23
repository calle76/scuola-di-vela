# Proposta: la marcatura nell'ultima regata del torneo (voce 74, passo 2, decisione 2)

*Fermata 1, 23 novembre 2026, sera (Opus). Nessun codice finché non arriva il via. Viene da `PROPOSTA-STORICO-RIVALI.md` §«Passo 2, decisione 2»: Ale ha scelto la marcatura decisa dalla classifica al posto della «nemesi» (vietata dalla regola 2, Caso 78) e niente «cautela» senza fonte.*

## Cosa dicono le fonti (e cosa no)

- **F115 (Caso 78, memo Perry):** ostacolare apposta un'altra barca in una regata di flotta è lecito solo se **serve alla propria classifica in quella manifestazione** e c'è una **ragionevole possibilità di riuscirci**; se mentre lo fai rompi un'altra regola, rompi anche la regola 2.
- **F116 (Loory, «When to cover»):** coprire vuol dire restare fra l'avversario e la boa e **virare quando vira lui**, per tenerlo nel proprio vento sporco; conviene con un rivale di velocità simile che si deve battere, non con uno già staccato.
- **Non dicono:** a che distanza si comincia, con quanto ritardo si risponde a una virata, quanto si perde o si guadagna. Questi numeri sono **ipotesi nostre**, dichiarate sotto. Né F115 né F116 parlano di poppa: la marcatura in poppa resta fuori (semplificazione dichiarata).

## Il modello più semplice

**Chi marca.** All'inizio dell'**ultima regata del torneo** (la 3 nei tornei lunghi, la 4 nei corti e nella finale), per ogni rivale si fanno due conti con la classifica della serie (`torSerie`, scarto compreso), aggiungendo un'ultima regata finta in cui gli altri arrivano nel loro ordine attuale di classifica:
- (A) il rivale arriva **subito davanti** a te;
- (B) il rivale arriva **subito dietro** a te.

Se in (A) il rivale finisce la serie davanti a te e in (B) dietro, **il duello con te decide fra voi due**: batterti gli serve (F115, «serve alla propria classifica»). Se sono più d'uno, marca **uno solo**: quello con la differenza di punti più piccola da te; a parità, il primo nell'ordine delle barche. Nessun numero a caso. Vale in tutti i tornei di Deriva (gioco libero, tappe, finale).

**Quando marca (in acqua), tutte insieme:**
1. di **bolina** (la boa da puntare è sopravento: lo stesso ramo della guida che oggi fa i bordi alternati), tu e lui sullo **stesso lato** del percorso;
2. lui è **davanti** (più vicino di te alla boa) e a meno di **`MARCA_D` = 10 lunghezze** (42 m: è la portata del cono d'ombra che c'è già, quindi lì coprire ha un effetto vero; è la «ragionevole possibilità» di F115);
3. non è vicino alla boa (la regola dei 30 m che c'è già resta com'è), non sta facendo giri di penalità, non è prima del via.

**Cosa fa quando marca.** Se sei su mure diverse dalle sue da almeno **`MARCA_REAZ` = 3 s** e il suo bordo dura da almeno 8 s (l'isteresi che c'è già), **vira sulle tue mure** (F116: «virare quando vira lui»). Mentre marca **non vira a tempo** (altrimenti se ne andrebbe da solo). Prima di virare controlla con `passaggio` (la previsione che i rivali usano già per cedere) che nessuna barca sia a meno di 2 lunghezze sulla rotta nuova: se c'è, aspetta (niente virate addosso, regola 13 e F115 «senza rompere altre regole»). Dopo la scelta della rotta passa comunque da `cedeAvv1b` e dalle regole 15-16-18 come oggi: **chi deve cedere cede anche mentre marca.** La virata non sorteggia la durata del bordo nuovo (nessun numero a caso consumato in più).

**Come si vede** (principio: ogni cambio di comportamento si deve vedere e spiegare):
- **Nel testo della regata** (`torBrief`, sempre visibile, anche col Coach spento): «Ultima regata: Rossi (barca Verde) ti marca. Se ti arriva davanti ti passa in classifica, quindi di bolina proverà a starti addosso e a virare quando viri tu.» (oppure «…ti resta davanti in classifica» se è già davanti). Una riga sola.
- **Nel Coach** a **−100 s** (fra la frase dello storico a −150 e quella dello sponsor a −50), volto serio, stessa frase più corta, con la sua riga «C» nel file.
- **Nel file della regata** due righe nuove `marca` / `marca_fine` (nome del rivale, istante) quando comincia e smette di marcare in acqua: servono ai collaudi e al Coach dopo.

## Costanti nuove (tutte ipotesi nostre, nessuna fonte dà i numeri)

| Nome | Valore | Perché |
| --- | --- | --- |
| `MARCA_D` | 10 lunghezze (42 m) | portata del cono d'ombra già nel gioco (F75); oltre, coprire non toglie vento |
| `MARCA_REAZ` | 3 s | un timoniere vede la virata e risponde; nessuna fonte |
| ultima regata finta | gli altri nell'ordine di classifica | il modo più semplice per dire «serve alla classifica»; non prevede come andranno gli altri |

Nessuna si tara sui risultati: se un criterio non passa, si riporta e si torna qui.

## Criteri (soglie nostre, dichiarate prima)

Banco: **40 tornei corti e 40 lunghi a semi fissi**, corsi due volte, con la marcatura e senza (interruttore di misura `__sv.marca`), Chromium; il collaudo nuovo anche in Firefox. Una misura per volta col freno.

| # | Criterio | Soglia |
| --- | --- | --- |
| K1 | Chi marca è giusto | la scelta si **ricalcola in Python** dai risultati salvati (`tor.ris`, punteggio dell'appendice A riscritto nel collaudo, non preso dal gioco): 0 scelte diverse; il collaudo stampa quanti tornei hanno un marcatore e quanti no, **almeno 20 e 20** (altrimenti si costruiscono classifiche a mano e lo si dice) |
| K2 | Il resto non cambia | regate prima dell'ultima identiche al bit con e senza marcatura; ultima regata identica al bit quando nessuno marca |
| K3 | Marca davvero | nelle ultime regate con marcatura attiva, le tue virate seguite da una sua entro 10 s: **≥ 50%** e almeno il doppio della stessa misura senza marcatura. Contano solo le regate con almeno 60 s di marcatura attiva: se sono meno di 20, il criterio è «non misurato», non «passato» |
| K4 | Nessuna regola rotta mentre marca | **0 contatti con colpa del marcatore** mentre marca, su tutte le ultime regate; contatti in tutto nell'ultima regata non più di +10% rispetto a senza |
| K5 | Gli serve | il marcatore ti arriva davanti nell'ultima regata almeno quanto senza marcatura (se marcare lo fa perdere, il modello è sbagliato) |
| K6 | Non è schiacciante | il tuo tempo d'arrivo nell'ultima regata peggiora al più del 5% in mediana; non arrivati in tutto al più +1 su 80 |
| K7 | Si dice | riga nel testo della regata con nome e barca giusti in tutti i casi con marcatore, 0 righe nei casi senza; Coach a −100 s (±1 s); col Coach spento 0 frasi del Coach ma la riga resta |
| K8 | Pannello | testo della regata e riquadro del Coach a 1360x650 senza eccesso col nome più lungo |
| K9 | Come un giocatore | pagina senza `#collaudo`, torneo con l'ultima regata da marcare (classifica costruita): riga e frase compaiono, 0 errori |

Non-regressione: `polare.js` e `raffiche_e_virate.js` (la barca non cambia), `collaudo_storico_frase.py` (la frase delle −150 s), `collaudo_versione.py`, `controllo_commenti.py`. La Scuola non è toccata (solo torneo).

Il metro non dipende da ciò che si misura: K1 ricalcola il punteggio da sé; K3 conta le virate dalle prue nel file, non dallo stato `marca` del gioco (lo stato serve solo a scegliere le finestre di tempo, e il collaudo stampa quante sono).

## Rischi

- **Il pilota del collaudo non è un giocatore:** se vira poco o sta lontano dal marcatore, la marcatura si vede poco (K3 «non misurato»). In quel caso la prova vera sono le vostre regate del torneo.
- **Virare dietro di te costa anche a lui:** con la barca di oggi la virata costa più della vera (voce 81, −10% contro −30% della soglia). Se K5 non passa, la causa può essere lì e non nella marcatura: si dice, non si ritocca.
- **Si appoggia alla guida di bolina di oggi:** le voci 4B e 2 (rivali) non sono adottate; se cambiano dopo, la marcatura si rimisura (costo: rifare K3-K6).
- **Sembrare ingiusto:** per questo la riga è sempre nel testo della regata, col motivo (la classifica), e la marcatura vale solo nell'ultima regata e solo per chi ha un interesse vero.
- **Stagione con un amico:** la marcatura dipende solo dalla tua batteria e non usa numeri a caso: ognuno ha la sua, come lo storico.

## Una domanda per Ale

Vale **a tutti i livelli dei rivali** (anche principianti) o solo da un livello in su? Consiglio: **tutti** (la regola è la classifica, non la bravura; F116 la dà come tattica normale). Se preferisce solo «esperti», cambia una riga.

## Passi, dopo il via

1. Scelta del marcatore e riga nel testo (K1, K7, K8): Sonnet basta.
2. La guida (`aiControl`, ramo di bolina) e le righe nel file: Opus. Collaudo nuovo `collaudo_marcatura.py` (K1-K9), Chromium poi Firefox.
3. Documenti, versione, `CHANGELOG.md`, `IL-GIOCO.md`; lezione o pagina di Deriva sulla copertura solo se Ale la vuole (sarebbe un'altra voce).
