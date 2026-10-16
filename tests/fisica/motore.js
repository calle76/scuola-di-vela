// Legge il motore fisico da js/motore.js (unica fonte di verità, dalla 1.0.3 in un file suo) e lo rende usabile da Node.js.
// Fino alla 1.0.2 lo ritagliava da index.html fra due segnaposto di testo.
const fs = require("fs"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "..", "..", "js", "motore.js"), "utf8");
module.exports = new Function(src + "\nreturn { step, BOAT, CL, CD, norm180, norm360 };")();
