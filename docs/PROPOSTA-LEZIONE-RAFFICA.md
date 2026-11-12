# Proposta: testo della lezione «Assorbire una raffica» (fermata 1, 12 novembre 2026)

**Stato: proposta, nessun codice toccato. Aspetta il via di Ale.**

## Cosa dice oggi la lezione (`js/contenuti.js:222-226`)
- Testo: «Quando ci entri, *lasca* un poco (e di bolina puoi anche *orzare* leggermente) per tenere lo sbandamento sotto i 20°.»
- Fine passo: «Lascare riduce la forza sulla vela; orzare di poco la scarica. È la tecnica principale per navigare con vento rafficato.»
- Il passo si completa lascando (`B.lasca >= 0.05`): l'orzata non è richiesta.

## Cosa dicono le fonti lette per intero (F81-F84, `FONTI-PUBBLICHE.md`)
- Lascare è la prima mossa: tutte e quattro.
- Stringere il vento *durante* la raffica: sconsigliato da F81 (ILCA), F82 (Harrison), F84 (Storer; guadagno di 2-3°, «not intended to get rid of heeling»). F83 (Ingham) orza solo dopo aver lascato e sporto, per ri-trimmare sul nuovo vento apparente.
- Limiti: barche Laser e simili, due articoli dello stesso gruppo di allenatori, nessuna fonte su raffica al traverso o in poppa, nessuna distinzione regata/scuola.

## Proposta (modello più semplice)
Cambiare solo le due frasi, non il codice del passo:
- Testo: «Quando ci entri, *lasca* un poco per tenere lo sbandamento sotto i 20°. Non stringere il vento: guadagni poco e perdi velocità. Passata la raffica, cazza di nuovo.»
- Fine passo: «Ben fatto. Lascare riduce la forza sulla vela ed è la prima mossa in una raffica; stringere il vento di solito non conviene. È la tecnica principale per navigare con vento rafficato.»
- Nessuna frase nuova sulla regata (nessuna fonte).

## Criteri (soglie nostre, dichiarate prima)
1. `collaudo_pilota_lezioni.py` (voce «6:Assorbire una raffica») resta verde: il pilota completa il passo.
2. `impronta1b.js` invariata: nessun numero del motore cambia (cambia solo testo).
3. Controllo che nessun altro punto (suggerimenti, esame, lezione «Nella raffica») dica «orza per scaricare».

## Rischi e domande per Ale
- La lezione «Nella raffica» (`contenuti.js:301-304`) parla di due modi per tenere la rotta, barra e lascare: è un'altra cosa (tenere la rotta, non scaricare) e non la tocco.
- Le fonti sono poche e di una sola classe: se preferisci aspettare altre fonti, la lezione resta com'è.
- Costo: basso, una versione solo di testi (1.2.29) più `CHANGELOG.md`.
