// Tabella polare per la rotta ottimale (1.2.22, docs/PROPOSTA-ROTTA-OTTIMALE.md §2 B): velocità di equilibrio della barca del gioco,
// prua tenuta ferma e scotta migliore (come polare.js), per angolo dal vento reale TWA e forza TWS; con lo scarroccio (angolo fra prua e rotta).
// Scrive js/rotta-dati.js (si rigenera solo se cambia la barca, che è congelata: impronta1b.js). Uso: node polare_tabella.js [--scrivi]
const { step } = require("./motore.js"), fs = require("fs"), path = require("path");
const TWS = [], TWA = []; for (let k = 4; k <= 20; k++) TWS.push(k); for (let a = 25; a <= 180; a += 5) TWA.push(a);
const V = [], L = [];
for (const kn of TWS){ const rv = [], rl = [];
  for (const twa of TWA){ let best = 0, lee = 0;
    for (let sh = 0; sh <= 1.0001; sh += 0.04){
      const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 };
      for (let t = 0; t < 60; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / 1.944 }, 0.05); if (Math.abs(S.heel) > 60) break; }
      if (Math.abs(S.heel) <= 60 && S.u > best){ best = S.u; lee = Math.atan2(Math.abs(S.vl || 0), S.u) * 180 / Math.PI; }
    }
    rv.push(+best.toFixed(3)); rl.push(+lee.toFixed(1)); }
  V.push(rv); L.push(rl); console.log(`${kn} nodi: ` + TWA.map((a, i) => `${a}°=${(rv[i] * 1.944).toFixed(1)}`).join(" ")); }
if (process.argv[2] === "--scrivi"){
  const out = "  // DATI DELLA ROTTA OTTIMALE (1.2.22): tabella polare della barca del gioco, scritta da tests/fisica/polare_tabella.js --scrivi (non si modifica a mano).\n" +
    "  // ROT_POL.v[i][j]: m/s alla forza TWS[i] (nodi) e all'angolo TWA[j] (gradi dal vento reale); ROT_POL.lee[i][j]: scarroccio in gradi.\n" +
    "  const ROT_POL = " + JSON.stringify({ tws: TWS, twa: TWA, v: V, lee: L }) + ";\n";
  fs.writeFileSync(path.join(__dirname, "..", "..", "js", "rotta-dati.js"), out); console.log("scritto js/rotta-dati.js");
}
