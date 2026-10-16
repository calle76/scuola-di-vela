# Laboratorio: a cosa serve ogni valore

Guida per chi usa il laboratorio (versione 1.0.4, aggiornata alla 1.0.6 il 16 ottobre 2026: esempi rimisurati con la resistenza della vasca). La proposta tecnica, i limiti e i collaudi sono in `PROPOSTA-LABORATORIO.md`.

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

**Come si leggono gli esempi.** I numeri di ogni scheda sono stati misurati il 16 ottobre, sulla barca della 1.0.6, portando quel valore al minimo e poi al massimo, con tutti gli altri come oggi. Il vento è sempre di 10 nodi. Le prove sono queste:
- **velocità:** quanto va la barca con la vela regolata al meglio, in tre andature: di bolina, al traverso e in poppa;
- **virata:** quanto tempo serve per virare partendo a circa 4 nodi;
- **marcia indietro:** si parte da fermi con la prua quasi controvento (10°), la barra al centro e la vela a metà; si misura dopo quanti secondi la barca va all'indietro a più di mezzo nodo.

Oggi la barca fa: velocità 3,8 nodi di bolina, 6,0 al traverso, 4,1 in poppa; virata in 3,4 secondi; marcia indietro dopo 1,7 secondi, fino a 2,3 nodi.

### Peso e vela

**`mass`: peso di barca e timoniere** (oggi 135 kg; da 90 a 250)
- **Cos'è:** quanto pesa tutto insieme.
- **Cosa cambia:** quanto in fretta la barca accelera e rallenta. **Non cambia la velocità massima**, perché nel gioco il peso non entra nella resistenza dell'acqua.
- **Esempio:** con 90 kg la virata dura 4,9 s, perché la barca leggera perde velocità in fretta e arriva in fondo stentando; con 250 kg dura 2,7 s. Più pesante vuol dire anche che va indietro più tardi (3,2 s invece di 1,7).

**`sailArea`: superficie della vela** (oggi 7,0 m²; da 4 a 10)
- **Cos'è:** quanti metri quadrati di vela.
- **Cosa cambia:** quanta spinta dà il vento, ma anche quanto fa sbandare la barca.
- **Esempio:** con 10 m² al traverso va a 7,1 nodi invece di 6,0, ma una raffica a 18 nodi la sbanda fino a 62°, cioè la fa scuffiare. Con 4 m² va a 4,8 nodi al traverso.

### Resistenza dell'acqua (la velocità)

Dalla 1.0.6 la resistenza dello scafo non è più una formula con tre numeri da tarare: è una **tabella misurata in vasca** su uno scafo vero (`PROPOSTA-VELOCITA.md`). I due cursori servono a provare uno scafo più o meno frenato di quello misurato.

**`hullScale`: quanto frena lo scafo, rispetto alla vasca** (oggi 1; da 0,5 a 2,5)
- **Cos'è:** un moltiplicatore. 1 è lo scafo misurato; 2 è più o meno la barca fino alla 1.0.5, che frenava circa il doppio.
- **Cosa cambia:** la velocità in tutte le andature, la virata e la frenata.
- **Esempio:** con 0,5 la velocità è 4,1 / 8,1 / 4,6 nodi (bolina / traverso / poppa); con 2,5 è 3,3 / 4,5 / 3,3, e la virata dura 4,3 s.

**`appDA`: attrito di deriva e timone** (oggi 0,0049 m²; da 0 a 0,01)
- **Cos'è:** il freno dell'acqua che scorre sulla deriva e sul timone, misurato come «area di resistenza» (dalla fonte).
- **Cosa cambia:** pesa di più quando la barca va piano.
- **Esempio:** con 0 la velocità è 4,0 / 6,4 / 4,3 nodi; con 0,01 è 3,6 / 5,5 / 3,9.

### Timone e virata

**`rudderDragK`: freno del timone girato** (oggi 45; da 0 a 120)
- **Cos'è:** quanto rallenta la barca quando la pala del timone è di traverso.
- **Cosa cambia:** quanto si perde in virata. La velocità in linea retta non cambia.
- **Esempio:** virata in 2,9 s con 0, in 4,5 s con 120.

**`turnLen`: quanto stretta gira la barca** (oggi 1,05 m; da 0,5 a 2)
- **Cos'è:** una lunghezza di calcolo: più è corta, più la barca gira in fretta con la stessa barra.
- **Cosa cambia:** tutte le curve e le virate, **anche all'indietro**.
- **Esempio:** virata in 1,4 s con 0,5; con 2 dura 10,3 s.

**`maxRudder`: quanto gira la pala a barra tutta** (oggi 30°; da 15 a 45)
- **Cosa cambia:** quanto si può curvare al massimo. Vale anche all'indietro e cambia il disegno della barra.
- **Esempio:** con 15° la virata dura 9,5 s; con 45° dura 2,3 s.

**`yawK`: prontezza della barca alla barra** (oggi 4; da 1 a 10)
- **Cos'è:** quanto in fretta la barca comincia a girare dopo che si è mossa la barra. Basso = barca «pigra», che risponde in ritardo.
- **Esempio:** virata in 4,0 s con 1, in 3,3 s con 10. Oltre il valore di oggi cambia poco.

### Marcia indietro e angolo morto

**`backMax` non c'è più** (tolto nella 1.0.8, `PROPOSTA-RETROMARCIA.md`): la barca va all'indietro solo per la vela che sbatte, contro la stessa resistenza della marcia avanti. Un profilo salvato prima che contiene `backMax` non si carica più (il laboratorio dice che «non è un valore del laboratorio»): va tolta quella riga. Per la marcia indietro che parte troppo presto contano `mass`, `sailArea`, `hullScale`, `ironsU` e `ironsYaw`.

Gli ultimi tre valori di questo gruppo lavorano insieme. Quando la barca è quasi ferma e la prua è vicina al vento, il gioco la fa girare da sola verso fuori, come fa una barca vera che il vento spinge di prua.

**`ironsA`: da quanto vicino al vento comincia** (oggi 36°; da 25 a 45)
- **Cos'è:** se il vento arriva da meno di questi gradi rispetto alla prua, la prua gira da sola.
- **Esempio:** nella prova di oggi non cambia niente, né con 25 né con 45.

**`ironsU`: sotto quale velocità** (oggi 0,5 m/s, circa 1 nodo; da 0,1 a 1)
- **Cos'è:** la prua gira da sola solo se la barca va più piano di così.
- **Esempio:** con 0,1, dopo 10 s la prua è a 12° dal vento; con 1, a 33° (e all'indietro arriva solo a 1,6 nodi).

**`ironsYaw`: con quanta forza gira** (oggi 6 gradi al secondo; da 0 a 15)
- **Cos'è:** la velocità con cui la prua gira da sola, al massimo.
- **Esempio:** con 0, dopo 10 s la prua è a 10° dal vento (resta piantata); con 15, a 36° (e all'indietro arriva solo a 1,5 nodi).

### Quando la vela si sgonfia

Questi due valori cambiano anche i filetti, i messaggi dell'angolo morto e quindi alcune lezioni. La loro somma non può superare 40°, che sono i 40° dell'angolo morto insegnati nelle lezioni: se si supera, il cursore non si muove e la finestra lo dice.

**`luffA0`: quanto vicino al vento la vela smette di portare** (oggi 27°; da 15 a 33)
- **Cos'è:** con il vento che arriva da meno di questi gradi rispetto alla prua, la vela comincia a sgonfiarsi.
- **Esempio:** con 15 la barca stringe di più e di bolina va a 4,5 nodi; con 33 va solo a 2,3, e la virata dura 3,9 s.

**`luffW`: in quanti gradi la vela passa da sgonfia a piena** (oggi 7°; da 2 a 15)
- **Cos'è:** con un valore piccolo il passaggio è netto; con uno grande è graduale.
- **Esempio:** con 2, bolina a 4,5 nodi; con 15, a 2,7.

## Cosa non c'è nel laboratorio

I valori di sbandamento, scuffia, scotta e deriva restano come sono: per i prossimi lavori sulla barca non servono. Si aggiungeranno se un compito lo chiede.
