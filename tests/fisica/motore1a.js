// La barca dell'1a per Node.js, dalla copia congelata motore1a_sorgente.js (js/motore.js della 1.0.78; docs/PROPOSTA-PULIZIA-CODICE.md).
// Dalla pulizia del codice il gioco ha solo la barca dell'1b: questa copia resta per i confronti (prototipo del fiocco, 1a contro 1b).
// Con MOTORE=1a nell'ambiente, anche motore.js legge questa copia: MOTORE=1a node polare.js dà le uscite di prima della pulizia.
const fs = require("fs"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "motore1a_sorgente.js"), "utf8");
module.exports = new Function(src + "\nreturn { step, BOAT, RUD2, RUD2_SICURA, DERIVA2, BOMA2, SALTI2, newShift, stepShift, CL, CD, norm180, norm360, hullDrag };")();
