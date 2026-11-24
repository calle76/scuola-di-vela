# Rollata (tasto X, voce 73, patch v3, cv 2) con le costanti della voce 81 — 25 novembre 2026
Su una copia di `js tests sperimentale` (non sul repo): `patch -p1 < sperimentale/virata-rollata-73/rollata_v3.patch`, poi `pre.js` con `Object.assign(require(cwd + "/tests/fisica/motore.js").BOAT, JSON.parse(process.env.V))` e
`V='{"luffA0":15}' node -r ./pre.js sperimentale/virata-rollata-73/misura_v3.js 2`. Conti senza numeri a caso.
