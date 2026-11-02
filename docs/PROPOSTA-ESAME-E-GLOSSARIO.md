# Proposta: l'esame e il glossario con le lezioni nuove

2 novembre 2026. **Fermata 1: solo documento, nessun codice.** È la fetta 5 di `PROPOSTA-LEZIONI-SCUOLA.md` §7 («Esame e glossario aggiornati»), dopo la 1.2.2: le 20 lezioni sono scritte, 14 sono ancora nascoste nel menu (B1-B5, D1-D7, C1-C2). Criterio già approvato (L7): banca dell'esame con 4 domande per ogni lezione nuova.

## 1. Da dove si parte (contato sul codice della 1.2.2)

- **Esame su tutte le lezioni** (`js/gioco.js`, `estraiEsame`): banca `ESAME` con le sole 6 lezioni di oggi (da 4 a 5 domande l'una), ne estrae `QUOTE = [4, 3, 4, 3, 3, 3]` = **20 domande**, ne servono **16** (80%). Il titolo dice ancora «Esame · livello 1»: il nome cambierà con il menu (la scuola, `PROPOSTA-RIORGANIZZAZIONE.md` §9).
- **Le 14 lezioni nuove** hanno già, ognuna, un esame interno di **4 domande** (campo `esame`), che si fa dentro la lezione. Sono le «4 domande per lezione» di L7: non serve scriverne altre.
- **Glossario** (`GLOSS`): 48 voci, tutte delle 6 lezioni di oggi e delle prove. Mancano le parole delle lezioni nuove.

## 2. Proposta

**Esame.**
1. La banca dell'esame prende le 4 domande del campo `esame` di ogni lezione nuova. Non le copio: la banca le legge dalla lezione, così una correzione vale in tutti e due i posti.
2. **Entrano nell'esame solo le lezioni visibili nel menu.** Finché le 14 lezioni restano nascoste, l'esame è identico a oggi (stesse domande con lo stesso seme: lo controlla il collaudo). Quando il menu nuovo le mostra, entrano da sole.
3. **Quante domande:** **1 per ogni lezione nuova**, le 6 di oggi come adesso. Con tutte e 20 visibili l'esame ha **34 domande** e la soglia resta all'80%: **28** (arrotondato per eccesso, come 16 su 20). Perché 1 e non 2: le lezioni nuove sono brevi (un solo passo pratico) e la regola del gioco vuole almeno quota + 1 domande per lezione (con 4 domande, al più 3); con 2, l'esame arriverebbe a 48 domande, troppe per chi comincia.
4. **Ripasso mirato** (le domande sbagliate raggruppate per lezione): funziona già per lezione, quindi vale anche per le nuove senza codice in più. Lo controllo nel collaudo.

**Glossario.**
5. Voci nuove, ognuna con la lezione da cui viene (testo parafrasato dalla lezione, che ha già la fonte): stallo della pala (B1; la voce «Stallo» di oggi è della vela, la allargo o la separo), spingere il boma (B2), salto di vento, scarso, buono (B5), lasciare strada, precedenza, sovrapposte, libera dietro e libera avanti (D1-D4), barca giuria, linea di partenza, avviso, preparatorio, bandiera di classe, bandiera P, bandiera X / richiamo individuale, partenza anticipata (D5-D6), giro di penalità (D7), partenza da fermi (C2). Circa **20 voci**; la lista definitiva la riporto con i numeri.
6. **Stessa regola dell'esame:** una voce che rimanda a una lezione nascosta resta nascosta, ed entra con il menu. Così il glossario non rimanda a lezioni che il giocatore non trova.

## 3. Criteri (soglie scritte prima, attese nostre)

- **G1:** con le lezioni nascoste, esame e glossario **identici a oggi**: stesse domande estratte con 20 semi fissi, stesse 48 voci.
- **G2:** con tutte le lezioni rese visibili (solo nel collaudo): l'esame estrae **34 domande**, 1 per ogni lezione nuova, soglia 28; in 200 estrazioni ogni domanda delle lezioni nuove esce almeno una volta.
- **G3:** ogni voce nuova del glossario ha la sua lezione, e la sua definizione è detta nel testo di quella lezione (controllo a mano, riportato voce per voce).
- **G4:** esame e glossario a 1360×650 senza pixel di eccesso, Chromium e Firefox, con tutte le lezioni visibili (il caso peggiore: 34 domande, glossario più lungo).
- **G5:** pagina senza `#collaudo` senza errori; `collaudo_esame`, `collaudo_quiz`, `collaudo_carriera_intera` verdi; regate e fisica identiche (non vengono toccate).

## 4. Rischi

- **34 domande sono tante.** Il ripasso mirato aiuta; se giocando sembra lungo, si scende a 1 domanda ogni due lezioni nuove (sarebbe un cambio di soglia, da dire).
- **Il meccanismo «solo visibili» lega l'esame al menu:** se il menu nuovo mostra le lezioni a gruppi o a pagine, «visibile» va riletto allora.
- **Carriera e libretto:** l'area «conoscenza» conta i quiz delle 6 lezioni di oggi (`QUIZ`), l'area «esperienza» le lezioni fatte non nascoste (`meriti`, `js/gioco.js`). Le lezioni nuove oggi non danno meriti; quando saranno visibili, quiz e soglie dei meriti andranno ricontati. È lavoro del menu, non di questa fetta: lo segnalo.

## 5. Da decidere (Ale)

1. **Esame:** 1 domanda per ogni lezione nuova (34 in tutto, ne servono 28), solo le lezioni visibili. Va bene?
