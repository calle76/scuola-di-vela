// Controllo completo della barca (26 nov): casi che i banchi della fisica non coprono. Uso: node extra.js motore.js
const fs = require("fs"), M = new Function(fs.readFileSync(process.argv[2], "utf8") + "\nreturn { step };")(), step = M.step;
const KN = 1.943844, R = Math.PI / 180, f1 = x => x.toFixed(1);
const nuovo = (u = 0) => ({ x: 0, y: 0, h: 0, u, vl: 0, r: 0 });
function corri(S, sh, twa, kn, T, dt = 0.05, cb){ for (let t = 0; t < T - 1e-9; t += dt){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, dt); if (cb && cb(t, S) === false) break; if (Math.abs(S.heel) > 60) return false; } return true; }
const bestSh = (kn, twa) => { let b = { u: -9, sh: 0 }; for (let sh = 0; sh <= 1.0001; sh += 0.05){ const S = nuovo(1); if (corri(S, sh, twa, kn, 50) && S.u > b.u) b = { u: S.u, sh }; } return b; };
// 1) partenza da ferma: secondi per arrivare a 2 nodi, con la scotta migliore in moto e con la scotta tutta cazzata / tutta lascata
console.log("1) PARTENZA DA FERMA: secondi per arrivare a 2 nodi (— = mai in 60 s, S = scuffia). colonne: scotta migliore / cazzata / lascata");
for (const kn of [4, 8, 12, 16, 20]){ let r = `  ${kn} nodi: `;
  for (const twa of [30, 40, 50, 60, 90, 120, 150, 180]){ const b = bestSh(kn, twa); const t2 = sh => { const S = nuovo(0); let tt = null; const ok = corri(S, sh, twa, kn, 60, 0.05, (t, S) => { if (S.u * KN >= 2){ tt = t; return false; } }); return !ok ? "S" : tt === null ? "—" : f1(tt); };
    r += `${twa}°: ${t2(b.sh)}/${t2(0)}/${t2(1)}  `; }
  console.log(r); }
// 2) accelerazione e frenata
console.log("2) ACCELERAZIONE (da ferma al 90% della velocità di regime, scotta migliore) e FRENATA (vela tutta lascata: metri e secondi fino a 1 nodo)");
for (const kn of [6, 12, 18]) { let r = `  ${kn} nodi: `;
  for (const twa of [45, 90, 150]){ const b = bestSh(kn, twa), S = nuovo(0); let t90 = null; corri(S, b.sh, twa, kn, 60, 0.05, (t, S) => { if (t90 === null && S.u >= 0.9 * b.u) t90 = t; });
    const F = nuovo(b.u); let d = 0, tf = null; corri(F, b.sh, twa, kn, 30); corri(F, 1, (twa < 90 ? 20 : twa), kn, 120, 0.05, (t, S) => { d += S.u * 0.05; if (S.u * KN < 1){ tf = t; return false; } });
    r += `${twa}°: 90% in ${t90 === null ? "—" : f1(t90)} s, ferma in ${tf === null ? "—" : f1(tf) + " s/" + f1(d) + " m"}   `; }
  console.log(r); }
// 3) bolina: sbandamento, scarroccio, timoniere fuori bordo, vela piatta, alla VMG migliore
console.log("3) BOLINA alla VMG migliore: angolo, nodi, sbandamento, scarroccio, fuori bordo, vela piatta (1 = piena)");
for (const kn of [4, 6, 9, 12, 15, 18, 22]){ let b = null; for (let a = 34; a <= 56; a += 2) for (let sh = 0; sh <= 0.5; sh += 0.04){ const S = nuovo(1); if (!corri(S, sh, a, kn, 50)) continue; const v = S.u * Math.cos(a * R) - Math.abs(S.vl) * Math.sin(a * R); if (!b || v > b.v) b = { a, v, S: { ...S } }; }
  if (!b){ console.log(`  ${kn} nodi: nessuna bolina possibile`); continue; }
  const S = b.S; console.log(`  ${kn} nodi: ${b.a}°, ${f1(S.u * KN)} nodi, VMG ${(b.v * KN).toFixed(2)}, sbandamento ${f1(S.heel)}°, scarroccio ${f1(Math.atan2(Math.abs(S.vl), S.u) / R)}°, fuori bordo ${(S.hike || 0).toFixed(2)}, vela ${(S.flat === undefined ? 1 : S.flat).toFixed(2)}`); }
// 4) regolazione della vela al traverso e al lasco: velocità con scotta da 0 a 1
console.log("4) SCOTTA: nodi con scotta 0 / 0,2 / 0,4 / 0,6 / 0,8 / 1 (10 nodi)");
for (const twa of [45, 90, 135, 180]){ console.log(`  ${twa}°: ` + [0, 0.2, 0.4, 0.6, 0.8, 1].map(sh => { const S = nuovo(1); return corri(S, sh, twa, 10, 50) ? f1(S.u * KN) : "S"; }).join(" / ")); }
// 5) numeri strani: vento 0, 30 nodi, passi di tempo diversi
console.log("5) NUMERI: vento 0 e 30 nodi, passo 1/30 contro 1/240 (velocità di regime a 45° e 90°, 12 nodi)");
for (const kn of [0, 30]){ let nan = 0, r = `  ${kn} nodi: `; for (const twa of [0, 45, 90, 180]) for (const sh of [0, 0.5, 1]){ const S = nuovo(1); corri(S, sh, twa, kn, 30); if (!Object.values(S).every(v => typeof v !== "number" || isFinite(v))) nan++; if (sh === 0.5) r += `${twa}°: ${f1(S.u * KN)}n ${f1(S.heel)}° `; } console.log(r + ` | numeri non finiti: ${nan}`); }
for (const twa of [45, 90]){ const b = bestSh(12, twa); const v = dt => { const S = nuovo(1); corri(S, b.sh, twa, 12, 60, dt); return S.u * KN; }; console.log(`  ${twa}°: passo 1/30 ${v(1 / 30).toFixed(3)}, 1/60 ${v(1 / 60).toFixed(3)}, 1/240 ${v(1 / 240).toFixed(3)} nodi`); }
