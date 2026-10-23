#!/usr/bin/env bash
# Lancia tutti i collaudi e stampa un rapporto, una riga per collaudo. Non installa niente.
# Uso:
#   tests/lancia_tutti.sh                  # tutti i collaudi
#   tests/lancia_tutti.sh --veloce         # salta i collaudi più lunghi (vedi docs/COLLAUDI.md)
#   tests/lancia_tutti.sh --dry-run        # stampa solo l'elenco con i comandi, senza lanciare niente
#   tests/lancia_tutti.sh --solo pulsanti  # lancia solo i collaudi il cui nome contiene "pulsanti"
#   tests/lancia_tutti.sh --parallelo 3    # fino a 3 collaudi insieme (default: 1, sequenziale)
#
# L'uscita completa di ogni collaudo viene salvata in tests/output/lancia_tutti/<data-ora>/<nome>.txt
# (cartella ignorata da git). Il riepilogo finale la richiama per i FALLITI (ultime 15 righe) e per i
# DA CONTROLLARE (ultime 4 righe, i numeri da confrontare a mano con docs/COLLAUDI.md).
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$REPO/.venv-collaudi/bin/python"

VELOCE=0
DRY_RUN=0
SOLO=""
MAXJOBS=1
while [ $# -gt 0 ]; do
    case "$1" in
        --veloce) VELOCE=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        --solo)
            SOLO="${2:-}"
            [ -z "$SOLO" ] && { echo "--solo richiede un testo da cercare nel nome" >&2; exit 2; }
            shift 2 ;;
        --parallelo)
            MAXJOBS="${2:-}"
            [[ "$MAXJOBS" =~ ^[0-9]+$ ]] && [ "$MAXJOBS" -ge 1 ] || { echo "--parallelo richiede un numero intero >= 1" >&2; exit 2; }
            shift 2 ;;
        *) echo "opzione non riconosciuta: $1" >&2; exit 2 ;;
    esac
done

HAVE_VENV=1
if [ ! -x "$VENV_PY" ]; then
    HAVE_VENV=0
    echo "venv dei collaudi non trovato: lancia prima tests/prepara_ambiente.sh (i collaudi Python saranno saltati)"
fi
HAVE_NODE=1
if ! command -v node >/dev/null 2>&1; then
    HAVE_NODE=0
    echo "node non installato: i collaudi della fisica (polare.js, raffiche_e_virate.js) saranno saltati"
fi

# Campi: nome | runtime (py/node) | esito (chiaro/ambiguo) | lungo (0/1) | lucchetto | script e argomenti relativi a tests/
# "chiaro": lo script esce con 1 se e solo se qualcosa non va, quindi OK/FALLITO viene dal codice di uscita.
# "ambiguo": lo script non distingue un esito riuscito da uno da controllare a mano (nessun sys.exit legato al risultato);
#            un codice di uscita diverso da 0 qui vuol dire comunque un errore vero (per esempio uno schianto di Playwright).
# "lucchetto": collaudi con lo stesso lucchetto (non vuoto) non girano mai insieme in --parallelo, perché condividono un
#              file di uscita o un'altra risorsa (vedi docs/COLLAUDI.md).
TESTS=(
    "polare.js|node|ambiguo|0||fisica/polare.js"
    "raffiche_e_virate.js|node|ambiguo|0||fisica/raffiche_e_virate.js"
    "impronta1b.js|node|chiaro|0||fisica/impronta1b.js"
    "collaudo_schermate.py|py|ambiguo|0||collaudo_schermate.py"
    "collaudo_riquadro_regata.py|py|chiaro|0||collaudo_riquadro_regata.py"
    "collaudo_moto_mare.py|py|chiaro|0||collaudo_moto_mare.py"
    "collaudo_timone2.py|py|chiaro|0||collaudo_timone2.py"
    "collaudo_boma2.py|py|chiaro|0||collaudo_boma2.py"
    "collaudo_salti2.py|py|chiaro|0||collaudo_salti2.py"
    "collaudo_contatto_vero.py|py|chiaro|0||collaudo_contatto_vero.py"
    "collaudo_regole.py|py|chiaro|0||collaudo_regole.py"
    "collaudo_semaforo.py|py|chiaro|0||collaudo_semaforo.py"
    "collaudo_torneo.py (veloce)|py|chiaro|0||collaudo_torneo.py --veloce"
    "collaudo_torneo.py (misura)|py|chiaro|1||collaudo_torneo.py"
    "collaudo_torneo.py (giocatore)|py|chiaro|0||collaudo_torneo.py --giocatore"
    "collaudo_raddrizzata.py|py|chiaro|1||collaudo_raddrizzata.py"
    "collaudo_virate2.py|py|chiaro|1||collaudo_virate2.py"
    "collaudo_distacchi.py|py|chiaro|1||collaudo_distacchi.py"
    "collaudo_lezioni.py|py|ambiguo|0||collaudo_lezioni.py"
    "collaudo_quiz.py|py|chiaro|0||collaudo_quiz.py"
    "collaudo_esame.py|py|chiaro|0||collaudo_esame.py"
    "collaudo_carriera.py|py|chiaro|0||collaudo_carriera.py"
    "collaudo_libretto.py|py|chiaro|0||collaudo_libretto.py"
    "collaudo_carriera_esame.py|py|chiaro|0||collaudo_carriera_esame.py"
    "collaudo_carriera_intera.py|py|chiaro|0||collaudo_carriera_intera.py"
    "collaudo_pilota_lezioni.py (veloce)|py|ambiguo|0||collaudo_pilota_lezioni.py --veloce"
    "collaudo_pilota_lezioni.py (semi 1-100)|py|ambiguo|1||collaudo_pilota_lezioni.py --semi 1-100"
    "collaudo_pilota_lezioni.py (senza #collaudo)|py|chiaro|0||collaudo_pilota_lezioni.py --reale"
    "collaudo_competizione.py (veloce)|py|chiaro|0||collaudo_competizione.py --veloce"
    "collaudo_competizione.py (misura)|py|chiaro|1||collaudo_competizione.py"
    "collaudo_competizione.py (tastiera)|py|ambiguo|1||collaudo_competizione.py --tastiera"
    "collaudo_regate.py (bastone)|py|ambiguo|0|regate|collaudo_regate.py 6 0"
    "collaudo_regate.py (raffiche)|py|ambiguo|0|regate|collaudo_regate.py 6 1"
    "collaudo_partenze.py|py|ambiguo|0||collaudo_partenze.py"
    "collaudo_aggressiva.py|py|chiaro|0||collaudo_aggressiva.py"
    "collaudo_contatto_senza_colpa.py|py|chiaro|0||collaudo_contatto_senza_colpa.py"
    "collaudo_pulsanti.py|py|chiaro|0||collaudo_pulsanti.py"
    "collaudo_versione.py|py|chiaro|0||collaudo_versione.py"
    "collaudo_linea.py|py|chiaro|0||collaudo_linea.py"
    "collaudo_vista.py|py|chiaro|0||collaudo_vista.py"
    "collaudo_strambata.py (6 nodi)|py|ambiguo|0||collaudo_strambata.py 6 10"
    "collaudo_strambata.py (15 nodi)|py|ambiguo|0||collaudo_strambata.py 15 10"
    "collaudo_suggerimento.py|py|chiaro|0||collaudo_suggerimento.py"
    "collaudo_pannello.py (1360x650)|py|ambiguo|0||collaudo_pannello.py 1360 650"
    "collaudo_pannello.py (1360x768)|py|ambiguo|0||collaudo_pannello.py 1360 768"
    "collaudo_fasce.py|py|ambiguo|0||collaudo_fasce.py"
    "collaudo_fantasma.py|py|ambiguo|0||collaudo_fantasma.py"
    "collaudo_registro.py|py|ambiguo|1||collaudo_registro.py"
    "collaudo_giro_boa.py|py|ambiguo|1||collaudo_giro_boa.py"
    "collaudo_registratore.py|py|chiaro|1||collaudo_registratore.py"
    "collaudo_laboratorio.py|py|chiaro|0||collaudo_laboratorio.py"
)

# Cosa guardare per i collaudi "ambiguo" (una riga ciascuno, dal rapporto atteso in docs/COLLAUDI.md).
nota() {
    case "$1" in
        "polare.js") echo "confronta a mano con circa 4,7 nodi a 45°, 6,0 a 90°, 4,1 a 180° con 10 nodi (dalla 1.0.11; 1.0.6-1.0.10 3,8 / 6,0 / 4,1)" ;;
        "raffiche_e_virate.js") echo "virata riuscita in circa 3,0 s da 3,9 nodi e in circa 6,6 s da 1,9 nodi, fallita da fermi; raffica a 20 nodi senza reagire 67° (scuffia) con la scotta fissa e circa 53° col boma a 21° (dalla 1.0.11)" ;;
        "collaudo_regole.py") echo "riga «ESITO: OK» (regole 10, 11, 12 e 13 nell'1b: 24 casi a mano dal regolamento, virata, e le due regole di sempre nell'1a)" ;;
        "collaudo_semaforo.py") echo "riga «ESITO: OK» (semaforo di precedenza: 16 regate dell'1b, colore uguale alla penalità, impostazione spenta, 1a senza semaforo)" ;;
        "collaudo_contatto_vero.py") echo "riga «ESITO: OK» (contatto fra gli scafi nell'1b: 8 coppie a mano nei due livelli, 6 regate col pilota nell'1a e nell'1b, 0 sovrapposizioni senza contatto, nessun contatto con gli scafi a più di 5 cm)" ;;
        "collaudo_salti2.py") echo "riga «ESITO: OK» (salti di vento dell'1b: libera, 12 regate nei salti col pilota, menu, pagina senza #collaudo)" ;;
        "collaudo_virate2.py") echo "FALLITO noto dalla 1.0.31: avversari oltre la bolina + 15° nel 15-17% delle virate contro la soglia del 5% (quasi tutte manovre volute della guida); guardare che il numero non cresca" ;;
        "collaudo_boma2.py") echo "riga «ESITO: OK» (spingi il boma, Z, nell'1b: 9 uscite dall'angolo morto coi tasti veri, ripartenza, pannello, pagina senza #collaudo)" ;;
        "collaudo_timone2.py") echo "riga «ESITO: OK» (barca dell'1b: freccia fino a 35°, Maiusc fino a 45°, 12 virate guidate coi tasti, avviso di stallo, pagina senza #collaudo)" ;;
        "collaudo_moto_mare.py") echo "riga «ESITO: OK» (barca che balla sull'onda, solo disegno: testa d'albero ferma senza vento, almeno 4 px con 10 nodi, rollio al traverso e beccheggio in poppa, ritmo più fitto di bolina; 24.000 quadri)" ;;
        "collaudo_riquadro_regata.py") echo "riga «ESITO: OK» (60 partenze con caratteri degli avversari a caso, nessun eccesso del riquadro delle istruzioni; NON VALIDO se non ha visto il caso peggiore con tre prudenti)" ;;
        "collaudo_schermate.py") echo "l'ultima riga «errori: [...]» deve essere vuota; le schermate della linea d'arrivo (tests/output/L_*.png) si guardano a occhio" ;;
        "collaudo_pilota_lezioni.py (veloce)") echo "32 passi, «guidando» completo in ogni passo, «ESITO: DA GUARDARE» con i soli casi noti dei semi 1-3 (1.11 La scotta: cazzare dopo un colpo lungo, 2.4 Barra sottovento dopo un colpo lungo, 6.3 La scuffia a mani ferme, voluto dalla 1.0.15; esito in docs/archivio/PROPOSTA-PILOTA-LEZIONI.md): un passo nuovo nell'elenco è un problema nuovo" ;;
        "collaudo_pilota_lezioni.py (semi 1-100)") echo "«guidando» non completato al più 1 volta su 100 per passo; «da guardare» con i casi noti dell'esito in docs/archivio/PROPOSTA-PILOTA-LEZIONI.md (1.9, 1.11, 1.12, 2.4, 2.5, 5.8, 6.2, 6.3): numeri molto diversi o passi nuovi sono un problema" ;;
        "collaudo_pilota_lezioni.py (senza #collaudo)") echo "«3 tentativi su 3 con entrambi i passi completati»" ;;
        "collaudo_lezioni.py") echo "ogni passo deve risultare completato, salvo i casi di attesa noti scritti nello script" ;;
        "collaudo_regate.py (bastone)"|"collaudo_regate.py (raffiche)") echo "nessun avversario deve restare «BLOCCATA» (semi 1-6, passi fissi: stesso risultato a ogni giro); la riga «riepilogo» dà la mediana d'arrivo, confrontabile fra versioni" ;;
        "collaudo_partenze.py") echo "con 3 e 5 minuti ritardo mediano entro circa 12s, distanza minima almeno 20 m, avvicinamento minimo almeno 14 m (dal 13 ottobre 2026 a passi fissi con i semi 1-10: stesso risultato a ogni giro); riga «anticipi allo sparo: OK» (ogni barca anticipata di nuovo dietro la linea entro 60 s; metri oltre la linea, frequenza, anticipo e la riga «oltre 10 m» solo stampati)" ;;
        "collaudo_aggressiva.py") echo "almeno il 90% degli incontri evitabili a ogni distanza (semi fissi)" ;;
        "collaudo_strambata.py (6 nodi)") echo "nessuna scuffia" ;;
        "collaudo_strambata.py (15 nodi)") echo "scuffia sempre" ;;
        "collaudo_pannello.py (1360x650)") echo "«pannello che eccede: nessuno» e «eccesso massimo del pannello (pixel): 0» (dalla 1.0.2 nessun passo sfora; qualunque eccesso è un problema nuovo); riga dei tasti 0 px, «errori: []» e «caratteri del gioco caricati: True»" ;;
        "collaudo_pannello.py (1360x768)") echo "«pannello che eccede: nessuno» (anche la riga dei tasti), «errori: []» e «caratteri del gioco caricati: True» (dalla 0.19.2 richiede facce Barlow davvero caricate)" ;;
        "collaudo_fasce.py") echo "con la linea d'arrivo (0.19): dalla 1.0.6 (barca nuova e pilota corretto), valori della sandbox: prove 1-4 a 79,6/124,2/161,8/285,1 s per ogni vento, 8 su 8; prova 5 finite 23 su 24, mediana 304,6 s, con circa 7 corse lunghe (556-897 s) da capire; fino alla 1.0.5, sul PC di Ale: 92,1/142,6/196,4/333,3, prova 5 19 su 24, mediana 353,6 s (nella sandbox la prova 5 varia: 18-21 su 24, mediana 353,6-354,6)" ;;
        "collaudo_fantasma.py") echo "la prova deve completarsi e il fantasma risultare salvato" ;;
        "collaudo_competizione.py (tastiera)") echo "riga «ESITO: OK» (piazzamento salvato con avversari, niente con «nessuno»); «ESITO: NON VALIDO» vuol dire che il pilota da tastiera non è arrivato in fondo: non è un errore del gioco, si rilancia" ;;
        "collaudo_registro.py") echo "riga finale «ESITO: 15 su 15 verifiche riuscite»" ;;
        "collaudo_giro_boa.py") echo "finisce solo girando la boa a sinistra; «giri sbagliati» deve essere 1 nei casi sbagliati" ;;
        *) echo "confronta l'uscita con l'esito atteso in docs/COLLAUDI.md" ;;
    esac
}

# Un nome di file sicuro per l'uscita salvata di un collaudo.
safe_name() { echo "$1" | sed -E 's/[^A-Za-z0-9_.-]+/_/g'; }

# Filtra con --solo (sottostringa nel nome).
FILTERED=()
for t in "${TESTS[@]}"; do
    name="${t%%|*}"
    if [ -z "$SOLO" ] || [[ "$name" == *"$SOLO"* ]]; then
        FILTERED+=("$t")
    fi
done
if [ "${#FILTERED[@]}" = 0 ]; then
    echo "nessun collaudo corrisponde a --solo $SOLO" >&2
    exit 2
fi

if [ "$DRY_RUN" = 1 ]; then
    for t in "${FILTERED[@]}"; do
        IFS='|' read -r name runtime esito lungo lock cmdline <<< "$t"
        read -ra parts <<< "$cmdline"
        script="${parts[0]}"; args=("${parts[@]:1}")
        if [ "$runtime" = py ]; then cmd=("$VENV_PY" "$REPO/tests/$script" "${args[@]}")
        else cmd=(node "$REPO/tests/$script" "${args[@]}"); fi
        if [ "$lungo" = 1 ] && [ "$VELOCE" = 1 ]; then
            echo "$name: SALTATO (--veloce) — ${cmd[*]}"
        elif { [ "$runtime" = py ] && [ "$HAVE_VENV" = 0 ]; } || { [ "$runtime" = node ] && [ "$HAVE_NODE" = 0 ]; }; then
            echo "$name: SALTATO (ambiente non pronto) — ${cmd[*]}"
        else
            echo "$name: ${cmd[*]}"
        fi
    done
    exit 0
fi

# Spacchetta i campi in array paralleli, indicizzati 0..M-1, nell'ordine originale (o filtrato da --solo).
M=${#FILTERED[@]}
declare -a NAME RUNTIME ESITO LUNGO LOCK CMDLINE
declare -a STATUS DURATA OUTFILE NOTE START
declare -A PID_IDX LOCK_COUNT
for ((i=0; i<M; i++)); do
    IFS='|' read -r NAME[i] RUNTIME[i] ESITO[i] LUNGO[i] LOCK[i] CMDLINE[i] <<< "${FILTERED[i]}"
done

TS=$(date +%Y%m%d-%H%M%S)
OUTDIR="$REPO/tests/output/lancia_tutti/$TS"
mkdir -p "$OUTDIR"

launch() {
    local idx=$1 cmdline="${CMDLINE[idx]}" runtime="${RUNTIME[idx]}" lock="${LOCK[idx]}"
    read -ra parts <<< "$cmdline"
    local script="${parts[0]}" args=("${parts[@]:1}")
    local cmd
    if [ "$runtime" = py ]; then cmd=("$VENV_PY" "$REPO/tests/$script" "${args[@]}")
    else cmd=(node "$REPO/tests/$script" "${args[@]}"); fi
    OUTFILE[idx]="$OUTDIR/$(safe_name "${NAME[idx]}").txt"
    START[idx]=$(date +%s.%N)
    "${cmd[@]}" > "${OUTFILE[idx]}" 2>&1 &
    local pid=$!
    PID_IDX[$pid]=$idx
    RUNNING=$((RUNNING + 1))
    [ -n "$lock" ] && LOCK_COUNT[$lock]=$(( ${LOCK_COUNT[$lock]:-0} + 1 ))
}

collect() {
    local pid rc idx lock fine durata name esito
    wait -n -p pid
    rc=$?
    idx=${PID_IDX[$pid]}
    unset 'PID_IDX[$pid]'
    RUNNING=$((RUNNING - 1))
    lock="${LOCK[idx]}"
    if [ -n "$lock" ]; then
        LOCK_COUNT[$lock]=$(( LOCK_COUNT[$lock] - 1 ))
        [ "${LOCK_COUNT[$lock]}" -le 0 ] && unset 'LOCK_COUNT[$lock]'
    fi
    fine=$(date +%s.%N)
    durata=$(awk -v a="${START[idx]}" -v b="$fine" 'BEGIN{printf "%.1fs", b-a}')
    DURATA[idx]="$durata"
    name="${NAME[idx]}"; esito="${ESITO[idx]}"
    if [ "$esito" = chiaro ]; then
        if [ "$rc" = 0 ]; then STATUS[idx]=OK; echo "$name: OK ($durata)"
        elif [ "$rc" = 3 ]; then STATUS[idx]=NON_VALIDO; echo "$name: NON VALIDO (ambiente) ($durata)"   # codice 3: misura non valida per l'ambiente, per esempio caratteri mancanti
        else STATUS[idx]=FALLITO; echo "$name: FALLITO ($durata)"; fi
    else
        if [ "$rc" = 0 ]; then STATUS[idx]=DA_CONTROLLARE; echo "$name: DA CONTROLLARE ($durata) — $(nota "$name")"
        else STATUS[idx]=FALLITO; echo "$name: FALLITO ($durata)"; fi
    fi
}

RUNNING=0
pending=()
T0=$(date +%s)
for ((i=0; i<M; i++)); do
    if [ "${LUNGO[i]}" = 1 ] && [ "$VELOCE" = 1 ]; then
        STATUS[i]=SALTATO; NOTE[i]="(--veloce, collaudo lungo)"
        echo "${NAME[i]}: SALTATO ${NOTE[i]}"
        continue
    fi
    if { [ "${RUNTIME[i]}" = py ] && [ "$HAVE_VENV" = 0 ]; } || { [ "${RUNTIME[i]}" = node ] && [ "$HAVE_NODE" = 0 ]; }; then
        STATUS[i]=SALTATO; NOTE[i]="(ambiente non pronto)"
        echo "${NAME[i]}: SALTATO ${NOTE[i]}"
        continue
    fi
    pending+=("$i")
done

while [ "${#pending[@]}" -gt 0 ] || [ "$RUNNING" -gt 0 ]; do
    launched_any=1
    while [ "$launched_any" = 1 ]; do
        launched_any=0
        for p in "${!pending[@]}"; do
            idx="${pending[p]}"
            lock="${LOCK[idx]}"
            if [ "$RUNNING" -lt "$MAXJOBS" ] && { [ -z "$lock" ] || [ -z "${LOCK_COUNT[$lock]:-}" ]; }; then
                launch "$idx"
                unset 'pending[p]'
                launched_any=1
                break
            fi
        done
    done
    [ "$RUNNING" -gt 0 ] && collect
done
T1=$(date +%s)

OK=0; FALLITI=0; DA_CONTROLLARE=0; SALTATI=0; NON_VALIDI=0
for ((i=0; i<M; i++)); do
    case "${STATUS[i]}" in
        OK) OK=$((OK+1)) ;;
        FALLITO) FALLITI=$((FALLITI+1)) ;;
        DA_CONTROLLARE) DA_CONTROLLARE=$((DA_CONTROLLARE+1)) ;;
        SALTATO) SALTATI=$((SALTATI+1)) ;;
        NON_VALIDO) NON_VALIDI=$((NON_VALIDI+1)) ;;
    esac
done

echo
echo "FALLITI:"
if [ "$FALLITI" = 0 ]; then
    echo "  nessuno"
else
    for ((i=0; i<M; i++)); do
        [ "${STATUS[i]}" = FALLITO ] || continue
        echo "  - ${NAME[i]} — ${OUTFILE[i]#$REPO/}"
        tail -n 15 "${OUTFILE[i]}" | sed 's/^/      /'
    done
fi

if [ "$NON_VALIDI" -gt 0 ]; then
    echo
    echo "NON VALIDI PER L'AMBIENTE (il gioco non è in causa: rilanciare dove l'ambiente è completo):"
    for ((i=0; i<M; i++)); do
        [ "${STATUS[i]}" = NON_VALIDO ] || continue
        echo "  - ${NAME[i]} — ${OUTFILE[i]#$REPO/}"
        tail -n 3 "${OUTFILE[i]}" | sed 's/^/      /'
    done
fi

echo
echo "DA CONTROLLARE:"
if [ "$DA_CONTROLLARE" = 0 ]; then
    echo "  nessuno"
else
    for ((i=0; i<M; i++)); do
        [ "${STATUS[i]}" = DA_CONTROLLARE ] || continue
        echo "  - ${NAME[i]} — $(nota "${NAME[i]}")"
        tail -n 4 "${OUTFILE[i]}" | sed 's/^/      /'
    done
fi

echo
echo "OK:"
if [ "$OK" = 0 ]; then
    echo "  nessuno"
else
    for ((i=0; i<M; i++)); do
        [ "${STATUS[i]}" = OK ] || continue
        echo "  - ${NAME[i]} (${DURATA[i]})"
    done
fi

if [ "$SALTATI" -gt 0 ]; then
    echo
    echo "Saltati:"
    for ((i=0; i<M; i++)); do
        [ "${STATUS[i]}" = SALTATO ] || continue
        echo "  - ${NAME[i]} ${NOTE[i]}"
    done
fi

echo
echo "Riepilogo: $OK OK, $FALLITI falliti, $NON_VALIDI non validi per l'ambiente, $DA_CONTROLLARE da controllare, $SALTATI saltati. Tempo totale: $((T1-T0))s."
echo "Uscita completa di ogni collaudo in: ${OUTDIR#$REPO/}/"

if [ "$FALLITI" = 0 ]; then
    exit 0
else
    exit 1
fi
