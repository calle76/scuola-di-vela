// Legge il motore fisico da js/motore.js (unica fonte di verità, dalla 1.0.3 in un file suo) e lo rende usabile da Node.js.
// Fino alla 1.0.2 lo ritagliava da index.html fra due segnaposto di testo. Con MOTORE=1a nell'ambiente legge invece la copia congelata della 1a (motore1a.js).
const fs = require("fs"), path = require("path");
if (process.env.MOTORE === "1a") return module.exports = require("./motore1a.js");
const src = fs.readFileSync(path.join(__dirname, "..", "..", "js", "motore.js"), "utf8");
module.exports = new Function(src + "\nreturn { step, BOAT, RUD2, RUD2_SICURA, DERIVA2, BOMA2, SALTI2, newShift, stepShift, CL, CD, norm180, norm360, hullDrag };")();
