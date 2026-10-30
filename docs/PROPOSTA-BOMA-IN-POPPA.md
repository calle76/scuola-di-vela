# Proposta: il boma che saltella con il vento in poppa (osservazione 63)

31 ottobre 2026. **Fermata 1: solo documento, nessun codice nel motore.** Il motore è quello della barca congelata e il cambio tocca anche le regate dell'1a, quindi serve il via di Ale (`OSSERVAZIONI-GIOCANDO.md`, 63; DECISIONI, 28 ottobre). Ale l'ha ricordato il 31 ottobre: «la barca perfettamente di poppa ha la vela che saltella».

## Il difetto, con la causa

`js/motore.js:205`: `S.boomSide = push ? S.pushSide : awa >= 0 ? -1 : 1`. Il lato del boma è il segno dell'angolo apparente del vento (`awa`). Con il vento esattamente dietro `awa` è vicino a ±180° e il segno cambia a ogni piccola oscillazione (onde, raffiche, assetto): nel registro dell'osservazione 63 `awa` passava da +180 a −180 circa ogni secondo con la prua ferma a 133° e nessuna strambata registrata. Il boma cambia lato nel disegno (`dispBoom = boomSide × boom`, `js/gioco.js:751`) e il velista cambia lato di sbandata.

**Cosa non cambia:** il lato del boma non entra nelle forze (nel motore compare solo qui e in `pushSide`, riga 149), e le strambate vere si contano da `detectManeuvers` (`js/gioco.js:692`) sull'angolo del vento **vero**, non su `boomSide`. Quindi polare, virate, raffiche e conteggi di strambate non dovrebbero muoversi: lo si controlla (B4).

## Modello più semplice plausibile

**Isteresi sul lato del boma.** Il lato cambia solo se il nuovo segno dell'angolo apparente è diverso **e** il vento apparente non è a meno di `BOOM_ISTERESI` gradi da dietro:

```
const nuovo = awa >= 0 ? -1 : 1;
S.boomSide = push ? S.pushSide : (nuovo !== S.boomSide && Math.abs(awa) > 180 - BOOM_ISTERESI) ? S.boomSide : nuovo;
```

Vicino al vento davanti (virata) e ovunque non sia la poppa piena nulla cambia. Con il vento esattamente dietro il boma resta sul lato che aveva, e passa dall'altra parte quando il vento apparente è passato di più di `BOOM_ISTERESI` gradi, cioè in una strambata vera. Fisicamente: in poppa piena una barca vera sta su una mura e il boma è trattenuto dalla scotta (o dal vang) fino a quando c'è una strambata.

**Costante nuova (ipotesi nostra, nessuna fonte): `BOOM_ISTERESI` = 5°.** Scelta perché l'oscillazione dell'angolo apparente osservata è di pochi gradi; da confermare con la misura B2 su un gruppo di semi e con un altro mai guardato (regola dei semi).

## Criteri (soglie scritte prima; attese nostre)

Pilota che tiene la prua fissa con il vento vero esattamente da poppa (twa 180°) a 6, 10 e 14 nodi, con le onde del gioco e con e senza salti di vento, 40 prove di 60 s a semi fissi (1-20 per la scelta, 101-120 per la conferma). Si riporta sempre il numero di prove.

- **B1 (base, nessuna soglia):** quanti cambi di lato in 60 s fa il boma **oggi**, per prova (mediana e massimo). È il metro: se non è almeno 5 cambi mediani, il difetto non si riproduce e non si cambia niente.
- **B2:** con l'isteresi, **al più 1 cambio di lato in 60 s in almeno il 95% delle prove**, in tutti e tre i venti.
- **B3 (la strambata vera non si perde):** la prua porta il vento da +170° a −170° (e al contrario) a 5°/s, con la scotta lasca e cazzata: il boma cambia lato **una sola volta e entro 1,5 s dal passaggio**, in 40 prove su 40 (20 per verso).
- **B4 (non regressione):** `polare.js`, `raffiche_e_virate.js` carattere per carattere; `impronta1b.js` (se l'impronta cambia solo per scene con poppa piena si dichiara e si rigenera il riferimento, se cambia altrove è un errore); 20 regate dell'1a e dell'1b identiche al bit **tranne** le righe del boma (`boomSide`, `dispBoom`) e quello che ne discende in modo diretto (si riporta quante regate divergono e perché).
- **B5 (nessun nuovo saltello altrove):** a twa 150°, 135° e 120° il numero di cambi di lato in 60 s è identico a prima (0 in tutte le prove).
- **B6:** pagina caricata senza `#collaudo`, nessun errore; pannello a 1360×650 senza pixel di eccesso; Firefox oltre a Chromium per i collaudi nuovi.

## Rischi

- **Gli avversari** usano lo stesso `step()` e quindi cambiano anche loro: la regata dei giri e le altre possono divergere dopo una strambata a poppa piena (B4).
- **Un vero urto di boma in poppa piena** (strambata accidentale con vento forte) potrebbe sembrare ritardata di fino a 5° (meno di un secondo): da guardare giocando.
- **È una modifica al motore congelato:** se l'impronta cambia dove non deve, si torna indietro.
- **Il saltello potrebbe avere anche un'altra causa** (l'angolo apparente stesso che oscilla per l'assetto): B1 lo dice prima di toccare qualcosa.

## Da decidere (Ale)

Il via per la fermata 2: B1 (misura, nessun cambio) e, se il difetto si riproduce, il cambio con B2-B6.
