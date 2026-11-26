// Voce 88, O9: come tests/fisica/motore.js ma legge sperimentale/onde-88/motore88.js (le onde spente devono ridare M al bit)
const fs = require("fs"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "..", "motore88.js"), "utf8");
module.exports = new Function(src + "\nreturn { step, BOAT, RUD2, RUD2_SICURA, DERIVA2, BOMA2, SALTI2, newShift, stepShift, CL, CD, norm180, norm360, hullDrag, onde88crea, onde88 };")();
