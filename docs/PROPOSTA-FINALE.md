# Proposta: la finale (fermata 1)

14 novembre 2026, notte. Tappa 3 di `PIANO-CHIUSURA-DERIVA.md`. **Solo proposta: in `js/` niente finché Ale non dà il via.**

## Cosa c'è oggi

Dalla 1.2.39 chi finisce fra i primi 3 del nazionale ha il «diritto alla finale», ma la finale non c'è: il gioco dice «arriverà in una versione successiva». Dal piano (decisione 2): lo sponsor che porta al Fiocco arriva già con i primi 3 del nazionale, quindi la finale **non serve per passare**: è il premio e la sfida in cima a Deriva.

## Modello più semplice

- **Chi c'è:** i primi 6 della classifica del nazionale appena finito, tu compreso. Si entra col diritto (primi 3); gli altri 5 sono i rivali meglio piazzati.
- **Come si corre:** un solo torneo di 4 regate a 6 barche, il torneo della 1.2.38, tutti in acqua: **niente a numeri**. Vento e formati come le tappe.
- **Dove:** un posto inventato, uno solo (nome da scegliere con la stessa ricerca dei nomi dei rivali, `PROPOSTA-RIVALI-E-SPONSOR.md` §12).
- **Cosa resta:** il posto nella finale, salvato come miglior risultato. Il titolo è «vincitore della finale del circuito», mai un titolo che sembri ufficiale (principio 5).
- **Una volta per nazionale:** il diritto vale per la finale subito dopo quel nazionale; ritirarsi la chiude.
- **Gioco libero:** la finale è sempre aperta, contro i 5 rivali nazionali con più doti (principio 2).
- **Sponsor (tappa 4):** «vinci la finale» o «podio in finale» possono essere obiettivi di un contratto.

## Criteri (soglie nostre, scritte prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| F1 | Chi entra | 200 nazionali simulati: i 6 della finale sono i primi 6 della classifica, 200 su 200; senza il diritto in carriera la finale non si apre, nel gioco libero sì |
| F2 | Si corre davvero | 10 finali col pilota (40 regate da 6): finiscono tutte, la classifica è quella del torneo |
| F3 | Salvataggio | ricarica a metà finale: uguale; «Azzera i progressi» la cancella |
| F4 | Le regate non cambiano | impronta del guardiano, `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici |
| F5 | Pannello e browser | 0 px di eccesso a 1360×650; Chromium e Firefox senza `#collaudo`, 0 errori |

## Costanti nuove (nostre)

6 finalisti, 4 regate, un posto inventato.

## Rischi

- Con i 6 più forti del nazionale, per il pilota vincere sarà raro: va bene per un premio, ma il numero si riporta (quante finali su 10 il pilota chiude fra i primi 3).
- I contatti nei primi 25 s (N2 della 1.2.38) ci sono anche qui: si sistemano con la tappa 5.

## Cosa serve da Ale

Il via, e il nome del posto (lo propongo io con la ricerca, come per i rivali).
