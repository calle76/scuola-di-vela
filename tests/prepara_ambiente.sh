#!/usr/bin/env bash
# Prepara un ambiente Python stabile per i collaudi del browser (Playwright).
# Non tocca index.html né sperimentale/. Non usa sudo e non installa nulla
# fuori da questa cartella del progetto: tutto finisce in .venv-collaudi/.
#
# Uso:
#   tests/prepara_ambiente.sh             # prepara davvero l'ambiente
#   tests/prepara_ambiente.sh --dry-run   # stampa solo cosa farebbe
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$REPO/.venv-collaudi"
PLAYWRIGHT_VERSION="1.60.0"
CHROMIUM_REV="chromium-1223"
CACHE_DIR="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=1
fi

# 1. .gitignore: il venv non deve entrare in git
GITIGNORE="$REPO/.gitignore"
if grep -qxF ".venv-collaudi/" "$GITIGNORE" 2>/dev/null; then
    echo ".gitignore: '.venv-collaudi/' già presente"
elif [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] aggiungerei '.venv-collaudi/' a $GITIGNORE"
else
    { echo ""; echo "# ambiente virtuale dei collaudi (punto 8 della 0.17)"; echo ".venv-collaudi/"; } >> "$GITIGNORE"
    echo ".gitignore: aggiunta '.venv-collaudi/'"
fi

# 2. venv dedicato
if [ -d "$VENV" ]; then
    echo "venv: già presente in $VENV"
elif [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] python3 -m venv $VENV"
else
    echo "+ python3 -m venv $VENV"
    python3 -m venv "$VENV"
fi

# 3. playwright nel venv, versione fissa
if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] $VENV/bin/pip install 'playwright==$PLAYWRIGHT_VERSION'"
else
    echo "+ $VENV/bin/pip install 'playwright==$PLAYWRIGHT_VERSION'"
    "$VENV/bin/pip" install "playwright==$PLAYWRIGHT_VERSION"
fi

# 4. il browser deve già essere in cache: 1.60.0 vuole chromium-1223
if [ -d "$CACHE_DIR/$CHROMIUM_REV" ]; then
    echo "cache: $CHROMIUM_REV presente in $CACHE_DIR"
else
    echo "cache: $CHROMIUM_REV NON presente in $CACHE_DIR"
    echo "per scaricarlo, lanciare a mano (non eseguito da questo script):"
    echo "  $VENV/bin/python -m playwright install chromium"
fi

# 5. controllo finale: apre index.html in headless e legge il titolo
if [ "$DRY_RUN" = 1 ]; then
    echo "[dry-run] controllo finale saltato (richiede l'installazione vera)"
    exit 0
fi

set +e
TITOLO=$("$VENV/bin/python" -c "
import sys, pathlib
from playwright.sync_api import sync_playwright
url = pathlib.Path(sys.argv[1]).resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(url)
    print(pg.title())
    b.close()
" "$REPO/index.html" 2>&1)
STATUS=$?
set -e

if [ "$STATUS" = 0 ]; then
    echo "OK — index.html apre in headless, titolo: $TITOLO"
else
    echo "ERRORE nel controllo finale:"
    echo "$TITOLO"
    exit 1
fi
