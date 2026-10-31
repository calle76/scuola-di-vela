#!/usr/bin/env bash
# Lancia tests/lancia_tutti.sh prima con Chromium (Chrome) e poi con Firefox, uno dopo l'altro (mai insieme: il carico falserebbe i collaudi a tempo).
# Le opzioni si passano a lancia_tutti.sh. Esempi:
#   tests/lancia_chrome_e_firefox.sh --veloce --parallelo 3     # il giro di tutti i giorni, nei due browser (circa 25 minuti per browser)
#   tests/lancia_chrome_e_firefox.sh --parallelo 3              # il giro completo, nei due browser
#   tests/lancia_chrome_e_firefox.sh --dry-run                  # solo l'elenco, senza lanciare niente
# Ogni giro salva le sue uscite in tests/output/lancia_tutti/<data-ora>/ e stampa il suo riepilogo: incollali tutti e due.
# Firefox va installato una volta sola: .venv-collaudi/bin/playwright install firefox
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; REPO="$(cd "$DIR/.." && pwd)"
PY="$REPO/.venv-collaudi/bin/python"
firefox_ok(){ [ -x "$PY" ] && "$PY" -c "
import os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p: sys.exit(0 if os.path.exists(p.firefox.executable_path) else 1)" 2>/dev/null; }
esiti=()
for b in chromium firefox; do
    echo; echo "=============== $b ==============="
    if [ "$b" = firefox ] && ! firefox_ok; then
        echo "Firefox non è installato per i collaudi: lancia  .venv-collaudi/bin/playwright install firefox  e riprova. Salto Firefox."
        esiti+=("firefox: NON LANCIATO"); continue
    fi
    BROWSER=$b "$DIR/lancia_tutti.sh" "$@"; esiti+=("$b: lancia_tutti.sh è uscito con $?")
done
echo; echo "=============== riassunto dei due giri ==============="; printf '%s\n' "${esiti[@]}"
