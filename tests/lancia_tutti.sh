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
    "collaudo_schermate.py|py|ambiguo|0||collaudo_schermate.py"
    "collaudo_lezioni.py|py|ambiguo|0||collaudo_lezioni.py"
    "collaudo_quiz.py|py|ambiguo|0||collaudo_quiz.py"
    "collaudo_regate.py (bastone)|py|ambiguo|0|regate|collaudo_regate.py 6 0"
    "collaudo_regate.py (raffiche)|py|ambiguo|0|regate|collaudo_regate.py 6 1"
    "collaudo_partenze.py|py|ambiguo|0||collaudo_partenze.py"
    "collaudo_aggressiva.py|py|ambiguo|0||collaudo_aggressiva.py"
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
)

# Cosa guardare per i collaudi "ambiguo" (una riga ciascuno, dal rapporto atteso in docs/COLLAUDI.md).
nota() {
    case "$1" in
        "polare.js") echo "confronta a mano con circa 3,4 nodi a 45°, 5,2 a 90°, 3,5 a 180° con 10 nodi" ;;
        "raffiche_e_virate.js") echo "virata riuscita in circa 4s da 3,9 nodi, fallita da fermi; raffica a 20 nodi senza reagire circa 55° (scuffia)" ;;
        "collaudo_schermate.py") echo "l'ultima riga «errori: [...]» deve essere vuota; le schermate della linea d'arrivo (tests/output/L_*.png) si guardano a occhio" ;;
        "collaudo_lezioni.py") echo "ogni passo deve risultare completato, salvo i casi di attesa noti scritti nello script" ;;
        "collaudo_quiz.py") echo "sei righe di punteggio e «errori: []» vuota" ;;
        "collaudo_regate.py (bastone)"|"collaudo_regate.py (raffiche)") echo "nessun avversario deve restare «BLOCCATA»" ;;
        "collaudo_partenze.py") echo "con 3 e 5 minuti ritardo mediano entro circa 12s, nessuna partenza anticipata, distanza minima almeno 20 m" ;;
        "collaudo_aggressiva.py") echo "per ogni incontro, almeno una manovra deve evitare il contatto" ;;
        "collaudo_strambata.py (6 nodi)") echo "nessuna scuffia" ;;
        "collaudo_strambata.py (15 nodi)") echo "scuffia sempre" ;;
        "collaudo_pannello.py (1360x650)"|"collaudo_pannello.py (1360x768)") echo "«pannello che eccede: nessuno» (anche la riga dei tasti), «errori: []» e «caratteri del gioco caricati: True» (dalla 0.19.2 richiede facce Barlow davvero caricate)" ;;
        "collaudo_fasce.py") echo "con la linea d'arrivo (0.19): prove 1-4 a 92,1/142,6/196,4/333,4 s per ogni vento; prova 5 finite 18 su 24, mediana circa 353 s" ;;
        "collaudo_fantasma.py") echo "la prova deve completarsi e il fantasma risultare salvato" ;;
        "collaudo_registro.py") echo "riga finale «ESITO: 13 su 13 verifiche riuscite»" ;;
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

OK=0; FALLITI=0; DA_CONTROLLARE=0; SALTATI=0
for ((i=0; i<M; i++)); do
    case "${STATUS[i]}" in
        OK) OK=$((OK+1)) ;;
        FALLITO) FALLITI=$((FALLITI+1)) ;;
        DA_CONTROLLARE) DA_CONTROLLARE=$((DA_CONTROLLARE+1)) ;;
        SALTATO) SALTATI=$((SALTATI+1)) ;;
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
echo "Riepilogo: $OK OK, $FALLITI falliti, $DA_CONTROLLARE da controllare, $SALTATI saltati. Tempo totale: $((T1-T0))s."
echo "Uscita completa di ogni collaudo in: ${OUTDIR#$REPO/}/"

if [ "$FALLITI" = 0 ]; then
    exit 0
else
    exit 1
fi
