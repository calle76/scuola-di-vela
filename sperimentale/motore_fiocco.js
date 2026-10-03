// Estrae il motore fisico direttamente da sperimentale/fiocco.html (unica fonte di verità, come
// tests/fisica/motore.js fa con index.html) e lo rende usabile da Node.js. Nessuna copia della fisica qui.
const fs = require("fs"), path = require("path");
const html = fs.readFileSync(path.join(__dirname, "fiocco.html"), "utf8");
const start = html.indexOf("// Motore fisico di una deriva");
const end = html.indexOf("  const $ = id =>");
if (start < 0 || end < 0) throw new Error("Motore fisico non trovato in sperimentale/fiocco.html: controlla i marcatori in motore_fiocco.js");
module.exports = new Function(html.slice(start, end) + "\nreturn { step, BOAT, CL, CD, sailF, ttOf, jibRange, jibShadedAt, fessuraDi, norm180, norm360 };")();
