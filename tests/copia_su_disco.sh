#!/usr/bin/env bash
# Copia di sicurezza delle registrazioni (e dei file delle stagioni) su un disco esterno (voce 14 di docs/DA-FARE.md, 17 novembre 2026).
# Uso:   bash tests/copia_su_disco.sh                      (disco di Ale: /media/callle/258D-17B9)
#        bash tests/copia_su_disco.sh /percorso/del/disco  (un altro disco, o una cartella per provare)
# Fa una cartella NUOVA con data e ora, non sovrascrive mai niente, poi controlla ogni file con sha256 e dice se sono tutti identici.
set -u
RADICE="$(cd "$(dirname "$0")/.." && pwd)"
DISCO="${1:-/media/callle/258D-17B9}"
if [ ! -d "$DISCO" ]; then echo "Il disco non c'è: $DISCO. Collega l'hard disk esterno e rilancia."; exit 1; fi
if [ ! -w "$DISCO" ]; then echo "Non posso scrivere su $DISCO."; exit 1; fi
if [ ! -d "$RADICE/registrazioni" ]; then echo "Non trovo la cartella registrazioni in $RADICE."; exit 1; fi
DEST="$DISCO/scuola-di-vela-copia-$(date +%Y-%m-%d_%H%M)"
if [ -e "$DEST" ]; then echo "$DEST esiste già: aspetta un minuto e rilancia (non sovrascrivo)."; exit 1; fi
mkdir "$DEST" || exit 1
cp -r --no-preserve=mode,ownership,timestamps "$RADICE/registrazioni" "$DEST/registrazioni" || { echo "COPIA FALLITA"; exit 1; }
mkdir "$DEST/stagioni"
n=0
for f in "$RADICE"/stagione-*.json; do [ -e "$f" ] && cp --no-preserve=mode,ownership,timestamps "$f" "$DEST/stagioni/" && n=$((n+1)); done
# controllo: lo stesso elenco di somme sha256 prima e dopo
( cd "$RADICE/registrazioni" && sha256sum -- * ) | sort -k2 > "${TMPDIR:-/tmp}/copia_orig.sha"
( cd "$DEST/registrazioni" && sha256sum -- * ) | sort -k2 > "${TMPDIR:-/tmp}/copia_dest.sha"
sync
if cmp -s "${TMPDIR:-/tmp}/copia_orig.sha" "${TMPDIR:-/tmp}/copia_dest.sha"; then
  echo "FATTO: $(wc -l < "${TMPDIR:-/tmp}/copia_dest.sha") registrazioni identiche, $n file di stagione, in:"
  echo "  $DEST"
  echo "Puoi scollegare il disco."
else
  echo "ATTENZIONE: qualche file non coincide. NON scollegare il disco e dimmelo."; diff "${TMPDIR:-/tmp}/copia_orig.sha" "${TMPDIR:-/tmp}/copia_dest.sha" | head; exit 1
fi
