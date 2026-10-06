#!/usr/bin/env bash
# Lancia tutti i collaudi e stampa un rapporto, una riga per collaudo. Non installa niente.
# Uso:
#   tests/lancia_tutti.sh             # tutti i collaudi
#   tests/lancia_tutti.sh --veloce    # salta i collaudi più lunghi (vedi docs/COLLAUDI.md)
#   tests/lancia_tutti.sh --dry-run   # stampa solo l'elenco con i comandi, senza lanciare niente
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$REPO/.venv-collaudi/bin/python"

VELOCE=0
DRY_RUN=0
for a in "$@"; do
    case "$a" in
        --veloce) VELOCE=1 ;;
        --dry-run) DRY_RUN=1 ;;
        *) echo "opzione non riconosciuta: $a" >&2; exit 2 ;;
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

# Campi: nome | runtime (py/node) | esito (chiaro/ambiguo) | lungo (0/1) | script e argomenti relativi a tests/
# "chiaro": lo script esce con 1 se e solo se qualcosa non va, quindi OK/FALLITO viene dal codice di uscita.
# "ambiguo": lo script non distingue un esito riuscito da uno da controllare a mano (nessun sys.exit legato al risultato);
#            un codice di uscita diverso da 0 qui vuol dire comunque un errore vero (per esempio uno schianto di Playwright).
TESTS=(
    "polare.js|node|ambiguo|0|fisica/polare.js"
    "raffiche_e_virate.js|node|ambiguo|0|fisica/raffiche_e_virate.js"
    "collaudo_schermate.py|py|ambiguo|0|collaudo_schermate.py"
    "collaudo_lezioni.py|py|ambiguo|0|collaudo_lezioni.py"
    "collaudo_quiz.py|py|ambiguo|0|collaudo_quiz.py"
    "collaudo_regate.py (bastone)|py|ambiguo|0|collaudo_regate.py 6 0"
    "collaudo_regate.py (raffiche)|py|ambiguo|0|collaudo_regate.py 6 1"
    "collaudo_partenze.py|py|ambiguo|0|collaudo_partenze.py"
    "collaudo_aggressiva.py|py|ambiguo|0|collaudo_aggressiva.py"
    "collaudo_pulsanti.py|py|chiaro|0|collaudo_pulsanti.py"
    "collaudo_strambata.py (6 nodi)|py|ambiguo|0|collaudo_strambata.py 6 10"
    "collaudo_strambata.py (15 nodi)|py|ambiguo|0|collaudo_strambata.py 15 10"
    "collaudo_suggerimento.py|py|chiaro|0|collaudo_suggerimento.py"
    "collaudo_pannello.py (1360x650)|py|ambiguo|0|collaudo_pannello.py 1360 650"
    "collaudo_pannello.py (1360x768)|py|ambiguo|0|collaudo_pannello.py 1360 768"
    "collaudo_fasce.py|py|ambiguo|0|collaudo_fasce.py"
    "collaudo_fantasma.py|py|ambiguo|0|collaudo_fantasma.py"
    "collaudo_registro.py|py|ambiguo|1|collaudo_registro.py"
    "collaudo_giro_boa.py|py|ambiguo|1|collaudo_giro_boa.py"
    "collaudo_registratore.py|py|chiaro|1|collaudo_registratore.py"
)

# Cosa guardare per i collaudi "ambiguo" (una riga ciascuno, dal rapporto atteso in docs/COLLAUDI.md).
nota() {
    case "$1" in
        "polare.js") echo "confronta a mano con circa 3,4 nodi a 45°, 5,2 a 90°, 3,5 a 180° con 10 nodi" ;;
        "raffiche_e_virate.js") echo "virata riuscita in circa 4s da 3,9 nodi, fallita da fermi; raffica a 20 nodi senza reagire circa 61° (scuffia)" ;;
        "collaudo_schermate.py") echo "l'ultima riga «errori: [...]» deve essere vuota" ;;
        "collaudo_lezioni.py") echo "ogni passo deve risultare completato, salvo i casi di attesa noti scritti nello script" ;;
        "collaudo_quiz.py") echo "sei righe di punteggio e «errori: []» vuota" ;;
        "collaudo_regate.py (bastone)"|"collaudo_regate.py (raffiche)") echo "nessun avversario deve restare «BLOCCATA»" ;;
        "collaudo_partenze.py") echo "con 3 e 5 minuti ritardo mediano entro circa 12s, nessuna partenza anticipata, distanza minima almeno 20 m" ;;
        "collaudo_aggressiva.py") echo "per ogni incontro, almeno una manovra deve evitare il contatto" ;;
        "collaudo_strambata.py (6 nodi)") echo "nessuna scuffia" ;;
        "collaudo_strambata.py (15 nodi)") echo "scuffia sempre" ;;
        "collaudo_pannello.py (1360x650)"|"collaudo_pannello.py (1360x768)") echo "«pannello che eccede: nessuno» e «errori: []»" ;;
        "collaudo_fasce.py") echo "tempi delle prove vicini agli attesi (circa 87/136/185/327 s, prova 5 intorno a 350 s)" ;;
        "collaudo_fantasma.py") echo "la prova deve completarsi e il fantasma risultare salvato" ;;
        "collaudo_registro.py") echo "riga finale «ESITO: 13 su 13 verifiche riuscite»" ;;
        "collaudo_giro_boa.py") echo "finisce solo girando la boa a sinistra; «giri sbagliati» deve essere 1 nei casi sbagliati" ;;
        *) echo "confronta l'uscita con l'esito atteso in docs/COLLAUDI.md" ;;
    esac
}

OK=0; FALLITI=0; DA_CONTROLLARE=(); SALTATI=()
T0=$(date +%s)

for t in "${TESTS[@]}"; do
    IFS='|' read -r name runtime esito lungo cmdline <<< "$t"
    read -ra parts <<< "$cmdline"
    script="${parts[0]}"; args=("${parts[@]:1}")

    if [ "$runtime" = py ]; then
        cmd=("$VENV_PY" "$REPO/tests/$script" "${args[@]}")
        disponibile=$HAVE_VENV
    else
        cmd=(node "$REPO/tests/$script" "${args[@]}")
        disponibile=$HAVE_NODE
    fi

    if [ "$DRY_RUN" = 1 ]; then
        if [ "$lungo" = 1 ] && [ "$VELOCE" = 1 ]; then
            echo "$name: SALTATO (--veloce) — ${cmd[*]}"
        elif [ "$disponibile" = 0 ]; then
            echo "$name: SALTATO (ambiente non pronto) — ${cmd[*]}"
        else
            echo "$name: ${cmd[*]}"
        fi
        continue
    fi

    if [ "$lungo" = 1 ] && [ "$VELOCE" = 1 ]; then
        echo "$name: SALTATO (--veloce, collaudo lungo)"
        SALTATI+=("$name (--veloce)")
        continue
    fi
    if [ "$disponibile" = 0 ]; then
        echo "$name: SALTATO (ambiente non pronto)"
        SALTATI+=("$name (ambiente non pronto)")
        continue
    fi

    inizio=$(date +%s.%N)
    out=$("${cmd[@]}" 2>&1)
    rc=$?
    fine=$(date +%s.%N)
    durata=$(awk -v a="$inizio" -v b="$fine" 'BEGIN{printf "%.1fs", b-a}')

    if [ "$esito" = chiaro ]; then
        if [ "$rc" = 0 ]; then
            echo "$name: OK ($durata)"; OK=$((OK+1))
        else
            echo "$name: FALLITO ($durata)"; FALLITI=$((FALLITI+1))
            echo "$out" | tail -n 15
        fi
    else
        if [ "$rc" = 0 ]; then
            echo "$name: DA CONTROLLARE ($durata) — $(nota "$name")"
            DA_CONTROLLARE+=("$name")
        else
            echo "$name: FALLITO ($durata)"; FALLITI=$((FALLITI+1))
            echo "$out" | tail -n 15
        fi
    fi
done

if [ "$DRY_RUN" = 1 ]; then
    exit 0
fi

T1=$(date +%s)
echo
echo "Riepilogo: $OK OK, $FALLITI falliti, ${#DA_CONTROLLARE[@]} da controllare, ${#SALTATI[@]} saltati. Tempo totale: $((T1-T0))s."
if [ "${#DA_CONTROLLARE[@]}" -gt 0 ]; then
    echo "Da controllare a mano:"
    for n in "${DA_CONTROLLARE[@]}"; do echo "  - $n"; done
fi
if [ "${#SALTATI[@]}" -gt 0 ]; then
    echo "Saltati:"
    for n in "${SALTATI[@]}"; do echo "  - $n"; done
fi

if [ "$FALLITI" = 0 ] && [ "${#DA_CONTROLLARE[@]}" = 0 ] && [ "${#SALTATI[@]}" = 0 ]; then
    exit 0
else
    exit 1
fi
