// Voce 84, quinto giro (GIRO5.md): criteri col metro sulla rotta per oggi, K e L (K con lo scafo ×0,965, regola §2). Uso: node giro5.js [nomi...]
const { misura, stampa } = require("./banco84.js"), C = require("./candidato.json");
const L = Object.assign({}, C[3].P, { boat: Object.assign({}, C[3].P.boat, { hullScale: .965 }) });
const tutti = { oggi: C[0].P, K: C[3].P, L };
if (require.main === module) for (const n of (process.argv.length > 2 ? process.argv.slice(2) : Object.keys(tutti))) stampa(n + (process.env.BANCO_PRUA ? " (metro vecchio, prua)" : " (rotta)"), misura(tutti[n]));
module.exports = { L };
