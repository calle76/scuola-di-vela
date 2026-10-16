# Laboratorio: a cosa serve ogni valore

Guida per chi usa il laboratorio (versione 1.0.4, 16 ottobre 2026). La proposta tecnica, i limiti e i collaudi sono in `PROPOSTA-LABORATORIO.md`.

## Come si apre

Si apre il gioco con `#lab` in fondo all'indirizzo, poi si ricarica la pagina. Il tasto **L** nasconde e rimostra la finestra. Con `#lab` il gioco **non salva niente**: per giocare normalmente si toglie `#lab` e si ricarica.

## Le parti della finestra

- **Il menu a tendina (profilo).** Un profilo è un insieme di valori già scritti nel codice, con la fonte di ognuno. Per ora c'è solo «come oggi», cioè la barca del gioco.
- **La riga «versione … · stato: …».** Lo stato dice quanto ci si può fidare dei valori:
  - «misura»: c'è un dato misurato e citato;
  - «ipotesi»: è una scelta nostra dichiarata;
  - «non verificato»: nessuno l'ha controllato.

  La barca di oggi è «ipotesi (taratura del gioco)», perché i suoi numeri sono stati scelti perché il gioco fosse plausibile, non ricavati da misure. Appena si muove un cursore diventa «non verificato».
- **I cursori.** Ognuno cambia **subito** la barca, anche mentre naviga. Il nome di un valore diventa arancione quando è diverso dalla barca di oggi. Passando col mouse sopra un nome compare una breve spiegazione.
- **Valori del profilo.** Riporta tutti i cursori ai valori del profilo scelto.
- **Esporta.** Scrive i valori di adesso in un riquadro, già selezionato: si copia con Ctrl+C e si incolla in chat o in una nota. I valori toccati a mano escono sempre come «prova a mano, non verificato».

**Attenzione:** in regata un valore cambiato cambia **anche gli avversari**. Per le prove conviene la navigazione libera.

## I valori, uno per uno

**Come si leggono gli esempi.** I numeri di ogni scheda sono stati misurati il 16 ottobre portando quel valore al minimo e poi al massimo, con tutti gli altri come oggi. Il vento è sempre di 10 nodi. Le prove sono queste:
- **velocità:** quanto va la barca con la vela regolata al meglio, in tre andature: di bolina, al traverso e in poppa;
- **virata:** quanto tempo serve per virare partendo a circa 4 nodi;
- **marcia indietro:** si parte da fermi con la prua quasi controvento (10°), la barra al centro e la vela a metà; si misura dopo quanti secondi la barca va all'indietro a più di mezzo nodo.

Oggi la barca fa: velocità 3,4 nodi di bolina, 5,2 al traverso, 3,5 in poppa; virata in 4,0 secondi; marcia indietro dopo 1,8 secondi, fino a 1,8 nodi.

### Peso e vela

**`mass`: peso di barca e timoniere** (oggi 135 kg; da 90 a 250)
- **Cos'è:** quanto pesa tutto insieme.
- **Cosa cambia:** quanto in fretta la barca accelera e rallenta. **Non cambia la velocità massima**, perché nel gioco il peso non entra nella resistenza dell'acqua.
- **Esempio:** con 90 kg la virata dura 6,6 s, perché la barca leggera perde velocità in fretta e arriva in fondo stentando; con 250 kg dura 2,9 s. Più pesante vuol dire anche che va indietro più tardi (3,3 s invece di 1,8).

**`sailArea`: superficie della vela** (oggi 7,0 m²; da 4 a 10)
- **Cos'è:** quanti metri quadrati di vela.
- **Cosa cambia:** quanta spinta dà il vento, ma anche quanto fa sbandare la barca.
- **Esempio:** con 10 m² al traverso va a 5,9 nodi invece di 5,2, ma una raffica a 18 nodi la sbanda fino a 62°, cioè la fa scuffiare. Con 4 m² va a 4,0 nodi al traverso.

### Resistenza dell'acqua (la velocità)

Lo scafo frena in tre modi, e ognuno pesa di più a una velocità diversa. Sono i tre valori da toccare per la velocità, che secondo le fonti è troppo bassa con vento leggero e medio (`RICERCA-VELOCITA-VIRATA-RIPARTENZA.md`).

**`hullK1`: freno che conta soprattutto quando la barca va piano** (oggi 4; da 0 a 12)
- **Cosa cambia:** la velocità con vento leggero, la ripartenza e la marcia indietro.
- **Esempio:** con 0 al traverso va a 5,3 nodi invece di 5,2; con 12 va a 4,8. All'indietro arriva a 2,1 nodi con 0 e a 1,4 con 12.

**`hullK2`: freno principale, che cresce in fretta con la velocità** (oggi 12; da 4 a 30)
- **Cosa cambia:** è il valore che pesa di più sulla velocità in tutte le andature.
- **Esempio:** con 4 la velocità è 3,9 / 6,1 / 4,2 nodi (bolina / traverso / poppa); con 30 è 2,7 / 3,8 / 2,7.

**`hullK4`: freno delle alte velocità** (oggi 0,9; da 0 a 3)
- **Cos'è:** il «muro» oltre il quale la barca non accelera più.
- **Cosa cambia:** soprattutto il traverso, che è l'andatura più veloce.
- **Esempio:** con 0 il traverso sale a 6,2 nodi; con 3 scende a 4,3. La bolina cambia poco.

### Timone e virata

**`rudderDragK`: freno del timone girato** (oggi 45; da 0 a 120)
- **Cos'è:** quanto rallenta la barca quando la pala del timone è di traverso.
- **Cosa cambia:** quanto si perde in virata. La velocità in linea retta non cambia.
- **Esempio:** virata in 3,4 s con 0, in 5,3 s con 120.

**`turnLen`: quanto stretta gira la barca** (oggi 1,05 m; da 0,5 a 2)
- **Cos'è:** una lunghezza di calcolo: più è corta, più la barca gira in fretta con la stessa barra.
- **Cosa cambia:** tutte le curve e le virate, **anche all'indietro**.
- **Esempio:** virata in 1,4 s con 0,5; con 2 la virata non riesce.

**`maxRudder`: quanto gira la pala a barra tutta** (oggi 30°; da 15 a 45)
- **Cosa cambia:** quanto si può curvare al massimo. Vale anche all'indietro e cambia il disegno della barra.
- **Esempio:** con 15° la virata non riesce; con 45° dura 2,5 s.

**`yawK`: prontezza della barca alla barra** (oggi 4; da 1 a 10)
- **Cos'è:** quanto in fretta la barca comincia a girare dopo che si è mossa la barra. Basso = barca «pigra», che risponde in ritardo.
- **Esempio:** virata in 4,6 s con 1, in 3,9 s con 10. Oltre il valore di oggi cambia poco.

### Marcia indietro e angolo morto

**`backMax`: velocità massima all'indietro** (oggi 1,2 m/s, cioè 2,3 nodi; da 0 a 2)
- **Cos'è:** un tetto: la barca non va all'indietro più veloce di così.
- **Cosa cambia:** quanto forte può andare indietro, **non quando comincia**.
- **Esempio:** con 0 la barca non va mai all'indietro. Nella prova di oggi arriva al massimo a 1,8 nodi, cioè sotto il tetto: abbassarlo un po' non cambia niente, bisogna scendere sotto 0,9 m/s perché si veda. Per la marcia indietro che parte troppo presto contano di più `mass`, `sailArea`, `hullK1`, `ironsU` e `ironsYaw`.

Gli ultimi tre valori di questo gruppo lavorano insieme. Quando la barca è quasi ferma e la prua è vicina al vento, il gioco la fa girare da sola verso fuori, come fa una barca vera che il vento spinge di prua.

**`ironsA`: da quanto vicino al vento comincia** (oggi 36°; da 25 a 45)
- **Cos'è:** se il vento arriva da meno di questi gradi rispetto alla prua, la prua gira da sola.
- **Esempio:** nella prova di oggi non cambia niente, né con 25 né con 45.

**`ironsU`: sotto quale velocità** (oggi 0,5 m/s, circa 1 nodo; da 0,1 a 1)
- **Cos'è:** la prua gira da sola solo se la barca va più piano di così.
- **Esempio:** con 0,1, dopo 10 s la prua è a 12° dal vento; con 1, a 33°.

**`ironsYaw`: con quanta forza gira** (oggi 6 gradi al secondo; da 0 a 15)
- **Cos'è:** la velocità con cui la prua gira da sola, al massimo.
- **Esempio:** con 0, dopo 10 s la prua è a 10° dal vento (resta piantata); con 15, a 36°.

### Quando la vela si sgonfia

Questi due valori cambiano anche i filetti, i messaggi dell'angolo morto e quindi alcune lezioni. La loro somma non può superare 40°, che sono i 40° dell'angolo morto insegnati nelle lezioni: se si supera, il cursore non si muove e la finestra lo dice.

**`luffA0`: quanto vicino al vento la vela smette di portare** (oggi 27°; da 15 a 33)
- **Cos'è:** con il vento che arriva da meno di questi gradi rispetto alla prua, la vela comincia a sgonfiarsi.
- **Esempio:** con 15 la barca stringe di più e di bolina va a 3,8 nodi; con 33 va solo a 2,1, e la virata dura 4,9 s.

**`luffW`: in quanti gradi la vela passa da sgonfia a piena** (oggi 7°; da 2 a 15)
- **Cos'è:** con un valore piccolo il passaggio è netto; con uno grande è graduale.
- **Esempio:** con 2, bolina a 3,8 nodi; con 15, a 2,3.

## Cosa non c'è nel laboratorio

I valori di sbandamento, scuffia, scotta e deriva restano come sono: per i prossimi lavori sulla barca non servono. Si aggiungeranno se un compito lo chiede.
