// Voce 84, §15: quale parte di K tiene ferma la barca dopo la virata con 18 nodi (smorzamento della resistenza indotta, braccio velico).
const d = __dirname + "/";
process.argv[2]="nulla"; const C = require(d+"candidato.json");
const src=require("fs").readFileSync(d+"virate_semb.js","utf8").split("\nconst MIS")[0];
const virata = new Function("require","__dirname", src.replace(/require\("\.\//g,'require("'+d)+"\nreturn virata;")(require, d);
const K = C[3].P, v = (n, P) => { const r = virata(P, 18, 45); console.log(n.padEnd(34), `uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); };
v("K", K);
v("K, smorzamento 0,4", Object.assign({}, K, { reg: .4 }));
v("K, braccio velico 2,0", Object.assign({}, K, { boat: Object.assign({}, K.boat, { zCE: 2.0 }) }));
v("K, entrambi", Object.assign({}, K, { reg: .4, boat: Object.assign({}, K.boat, { zCE: 2.0 }) }));
