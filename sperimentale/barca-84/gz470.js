// Voce 84: raddrizzata dello scafo oltre 22,5° con la forma della curva «senza trapezio» del 470 (Masuyama e Ogihara 2020, F4 fig. 4, calcolo;
// letta a occhio dalla figura: 33/50/57/57/52/40/25/10/0 kgf·m a 10/20/25/30/40/50/60/70/76°). Fino a 22,5° resta F121; oltre, la forma del 470
// scalata perché passi per il valore di F121 a 22,5°. Oggi in K: retta da 22,5° a 0 a 90° (ipotesi).
const { motore, misura, esito } = require("./banco84.js"), C = require("./candidato.json");
const F470 = [[10, 33], [20, 50], [25, 57], [30, 57], [40, 52], [50, 40], [60, 25], [70, 10], [76, 0], [90, -20]];
const f = x => { for (let i = 1; i < F470.length; i++) if (x <= F470[i][0]) return F470[i-1][1] + (F470[i][1] - F470[i-1][1]) * (x - F470[i-1][0]) / (F470[i][0] - F470[i-1][0]); };
const k = 0.247 / f(22.5), base = [[0,0],[4.5,.083],[9,.145],[13.5,.19],[18,.223],[22.5,.247]];
const gzTab = base.concat([25, 30, 35, 40, 45, 50, 55, 60, 70, 76, 90].map(a => [a, Math.max(-0.05, k * f(a))]));
console.log("GZ (m): " + gzTab.filter(r => r[0] >= 22.5).map(r => r[0] + "° " + r[1].toFixed(3)).join(", "));
console.log("K oggi: 22.5° .247, 30° " + (.247 * 60 / 67.5).toFixed(3) + ", 45° " + (.247 * 45 / 67.5).toFixed(3) + ", 60° " + (.247 * 30 / 67.5).toFixed(3));
module.exports = { gzTab };
if (require.main === module && !process.argv[2]){ const KP = C[3].P, K470 = Object.assign({}, KP, { gzTab });
  for (const [n, P] of [["K", KP], ["K + forma del 470", K470]]){ const o = misura(P); console.log("## " + n + "\n  " + esito(o) + `\n  raffica 10→16/18/20 senza/lascando ${o.raff.map(r => r.map(x => x.toFixed(0)).join("/")).join("  ")} | Day ${o.day.map(d => d[0].toFixed(1)).join(" ")} | 20n ${o.v20.toFixed(2)}`); } }
if (require.main === module && process.argv[2] === "virate"){ const src = require("fs").readFileSync(__dirname + "/virate_semb.js", "utf8").split("\nconst MIS")[0];
  const virata = new Function("require", src.replace(/require\("\.\//g, 'require("' + __dirname + '/') + "\nreturn virata;")(require);
  for (const [n, P] of [["K", C[3].P], ["K + forma del 470", Object.assign({}, C[3].P, { gzTab })]]) for (const kn of [14, 18]){ const r = virata(P, kn, 45);
    console.log(`${n} ${kn} nodi: uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); } }
