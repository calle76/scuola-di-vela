// Estrae il motore fisico direttamente da index.html (unica fonte di verità) e lo rende usabile da Node.js.
const fs = require("fs"), path = require("path");
const html = fs.readFileSync(path.join(__dirname, "..", "..", "index.html"), "utf8");
const start = html.indexOf("// Motore fisico di una deriva");
const end = html.indexOf("  const $ = id =>");
if (start < 0 || end < 0) throw new Error("Motore fisico non trovato in index.html: controlla i marcatori in tests/fisica/motore.js");
module.exports = new Function(html.slice(start, end) + "\nreturn { step, BOAT, CL, CD, norm180, norm360 };")();
