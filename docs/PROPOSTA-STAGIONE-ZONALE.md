# Proposta: la prima stagione del circuito zonale (fermata 1)

14 novembre 2026, pomeriggio. Ale: «restiamo sul livello deriva sviluppandone carriere e regate e rapporti tra regatanti … facciamo maturare un bel livello che poi farà da base per quelli successivi» (`DECISIONI.md`). Mette insieme pezzi già proposti e mai fatti:
- rivali che vivono anche quando non giochi (`PROPOSTA-RIVALI-E-SPONSOR.md` §6);
- circuito zonale e nazionale (§11);
- carriera in profondità con una barca (§16);
- storia e conseguenze dei rivali (`DA-FARE.md` voce 35).

In `js/` non è stato scritto niente.

## Cosa c'è oggi

- **Il torneo** sono 4 regate contro 3 rivali presi fra 10 (1.2.33), ognuno con i suoi tratti fissi.
- **Lo storico** sono i fatti delle regate con te (partenza, boa 1, contatti), solo mostrati (1.2.30).
- **Non c'è una stagione:** ogni torneo finisce lì, senza classifica fra un torneo e l'altro.
- **I rivali non si incontrano mai fra di loro** fuori dai tuoi tornei.

## Modello più semplice

**1. La stagione = 4 tappe.**
- Ogni tappa è un torneo come oggi: 4 regate, tu più 3 rivali in acqua.
- Ogni tappa ha un nome di posto inventato e un vento suo, da leggero a medio (10 o 12 nodi), come oggi.

**2. A ogni tappa corre tutta la flotta, a numeri.**
- I 10 rivali e tu siete nella classifica del circuito. In acqua, con te, ce ne sono 3.
- Gli altri 7 corrono la stessa tappa **a numeri**: per ogni rivale una «forza» presa dai suoi tratti (partenza e bolina: dote +1, media 0, difetto −1), più un sorteggio.
- L'ordine d'arrivo della tappa mette insieme le due cose. La tua posizione vera e quella dei tuoi 3 rivali in acqua restano quelle della regata; gli altri 7 si inseriscono intorno, secondo la loro forza rispetto a quella dei 3 che hai incontrato.
- Il modello è quello del §6 (Plackett-Luce: estrazioni pesate dalla forza, una per volta, senza ripetizioni). Costa poco e non tocca la fisica né la guida.

**3. La classifica del circuito.**
- Punti per piazzamento in ogni tappa, uguali per tutti: 1° 1 punto, 2° 2, … (il «punteggio minimo» delle classifiche di vela). **[da verificare]** su una fonte scritta: F89 parla di ranking e regate zonali, ma non l'ho letta per intero su questo punto.
- Dopo 4 tappe vince chi ha meno punti.
- **Promozione:** i primi 3 a fine stagione hanno «diritto al nazionale». In questo primo passo è solo scritto, perché il nazionale non esiste ancora: sarà il passo dopo.

**4. I rapporti fra regatanti: lo storico fra tutti, in frasi.**
- Per ogni coppia, compresa la tua, si contano: tappe insieme, chi è arrivato davanti, contatti e di chi era la colpa (solo per le regate in acqua; quelle a numeri non hanno contatti).
- Dopo ogni tappa il gioco può scrivere al massimo **tre frasi**, scelte fra poche regole fisse:
  - «**la tua bestia nera**: Fontana, davanti a te in 3 tappe su 3»;
  - «**con Brunelli** ti sei toccato in 2 regate, sempre colpa sua»;
  - «**Pavan e Serafini** si giocano il secondo posto del circuito»;
  - «**Gallo** è in forma: tre podi di fila».
- Sono frasi su fatti contati, non giudizi inventati.

**5. Conseguenze: in questo passo nessuna in acqua.**
- I rivali guidano come oggi. Il §6 lo lasciava aperto, e cambiare la guida per lo storico tocca gli avversari, che vanno misurati a parte.
- Le conseguenze di questo passo sono di carriera: classifica, diritto al nazionale, frasi.
- Il comportamento («ti sta più lontano», «ti cerca») è un passo successivo, con una sua proposta.

**6. Dove si vede.**
- Nella finestra del torneo, a fine tappa, la classifica del circuito (11 righe) con le tre frasi.
- Nella scheda di ogni rivale, la sua posizione nel circuito.
- Il salvataggio sta con i progressi, separato fra carriera e gioco libero come il gruppo dei rivali. «Azzera i progressi» lo cancella.

## Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| Z1 | Le tappe a numeri rispettano la forza: 2000 stagioni simulate a numeri, senza correre | i rivali con dote in tutte e due le aree finiscono in media davanti a quelli con difetto in tutte e due; ognuno dei 10 vince almeno una stagione su 200 (nessuno è condannato) |
| Z2 | La tua posizione vera e quella dei 3 rivali in acqua restano nell'ordine della regata | in 20 tappe corse col pilota: 20 su 20 |
| Z3 | La classifica del circuito torna coi conti | somma dei punti di ogni tappa = 1 + 2 + … + 11 = 66, in ogni tappa; vince chi ha meno punti |
| Z4 | Le frasi dicono il vero | per ogni frase scritta, il fatto contato coincide con lo storico salvato: 0 frasi false in 20 stagioni; almeno una frase in 18 stagioni su 20 (il metro misura) |
| Z5 | Salvataggio | ricaricando la pagina a metà stagione: classifica, tappa e storico uguali; «Azzera i progressi» li cancella |
| Z6 | Le regate non cambiano | impronta del guardiano identica al bit, `polare.js` e `raffiche_e_virate.js` identici: si aggiunge solo ciò che sta intorno alla regata |
| Z7 | Pannello e browser | 0 px di eccesso a 1360×650 con la classifica di 11 righe; Chromium e Firefox senza `#collaudo`, 0 errori |

## Costanti nuove (nostre, senza fonte)

- 4 tappe per stagione;
- forza = somma dei tratti, più un sorteggio con un peso da scegliere in Z1 su semi fissi e confermare su altri;
- i primi 3 hanno diritto al nazionale;
- al massimo 3 frasi per tappa.

## Fonti

F89 (regate zonali e ranking; il punteggio minimo è da verificare), F88 (promozioni nelle leghe). Le frasi sono testo nostro.

## Rischi

- **Tappe a numeri contro tappe in acqua:** i 3 rivali in acqua sono più deboli o più forti di quanto dica la loro forza a numeri, perché la guida vera dipende da vento e incontri. Inserire gli altri 7 rispetto a quei 3 tiene il conto onesto, ma va controllato che non nascano classifiche assurde, come un rivale con difetti che vince tutto. Lo controlla Z1.
- **La stagione è lunga:** 16 regate. Va bene salvare a metà (Z5). Si può scegliere una stagione corta (2 tappe) per provarla.
- **Il gruppo bilanciato della 1.2.33** dice che 3 rivali su 10 hanno una dote per area: la classifica rispecchierà quei tratti. È voluto: sono i rivali «forti» del circuito.

## Cosa serve da Ale

1. Il via.
2. Tre scelte:
   - 4 tappe, oppure 2 per provarla;
   - i nomi delle tappe li scrivo io, posti inventati, oppure li scrivi tu;
   - le frasi le propongo io in una lista che controlli tu, come per i nomi dei rivali.
