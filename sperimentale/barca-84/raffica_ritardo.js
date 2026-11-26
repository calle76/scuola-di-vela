// Voce 84: la raffica a gradino del banco (10→18 nodi a 45°, scotta 0,1, timone fermo) contro una raffica che sale in un tempo dato e contro un ritardo
// della forza sulla vela (ordine di grandezza dalle funzioni di Wagner e Küssner, Persson e altri 2024: 75% della forza dopo s ≈ 4-5 semicorde, cioè 0,3-0,5 s).
// Il ritardo è approssimato filtrando la velocità del vento che vede la barca (primo ordine): non è il modello di Persson, solo un limite.
const { motore } = require("./banco84.js"), KN = 1.943844, C = require("./candidato.json");
const prova = (P, g, tipo, T) => { const { step } = motore(P), S = { x:0,y:0,h:0,u:1.5,vl:0,r:0 }; for (let t = 0; t < 30; t += .02){ S.h = 0; step(S, { sheet: .1, tiller: 0 }, { twd: 45, tws: 10 / KN }, .02); }
  let m = 0, w = 10; for (let t = 0; t < 8; t += .02){ let k = g; if (tipo === "rampa") k = 10 + (g - 10) * Math.min(1, t / T); if (tipo === "filtro"){ w += (g - w) * Math.min(1, .02 / T); k = w; }
    S.h = 0; step(S, { sheet: .1, tiller: 0 }, { twd: 45, tws: k / KN }, .02); m = Math.max(m, S.heel); } return m; };
for (const i of [0, 3]){ const P = C[i].P; console.log("## " + C[i].n.slice(0, 40));
  for (const g of [16, 18, 20]){ const r = [["gradino", 0], ["filtro", .3], ["filtro", .5], ["rampa", 1], ["rampa", 2], ["rampa", 4]].map(([tp, T]) => `${tp}${T ? " " + T + " s" : ""} ${prova(P, g, tp, T).toFixed(0)}°`);
    console.log(`  10→${g} nodi, sbandamento massimo: ` + r.join(", ")); } }
