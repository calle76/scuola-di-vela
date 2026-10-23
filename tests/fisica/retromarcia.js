// Retromarcia senza tetto (1.0.8, docs/archivio/PROPOSTA-RETROMARCIA.md). Uso: node retromarcia.js   (pochi secondi)
// 1) Barca con la prua al vento, barra al centro, scotta 100 e 50, ferma o lanciata a 2 nodi, 60 s: dopo quanto va all'indietro e quanto forte.
// 2) Prua tenuta ferma nel vento per 120 s: velocità all'indietro di regime.
// 3) Rotazione all'indietro con la barra a fondo, partendo dal regime del punto 2.
const { step } = require("./motore.js");
const KN = 1.943844, DT = 1 / 240;
const f = v => v === null ? "  —  " : v.toFixed(1).padStart(5);
console.log("1) Prua al vento, barra al centro");
for (const tk of [6, 10, 15, 20]) for (const sh of [1, 0.5]) for (const u0 of [0, 2]) {
  const S = { x: 0, y: 0, h: 0, u: u0 / KN, vl: 0, r: 0, heel: 0, heelRate: 0 };
  let tInd = null, t05 = null, t1 = null, umin = 0, hAtMin = 0;
  for (let i = 1; i <= 60 / DT; i++) {
    step(S, { sheet: sh, tiller: 0 }, { twd: 0, tws: tk / KN }, DT);
    const t = i * DT;
    if (tInd === null && S.u < 0) tInd = t;
    if (t05 === null && S.u * KN < -0.5) t05 = t;
    if (t1 === null && S.u * KN < -1) t1 = t;
    if (S.u < umin) { umin = S.u; hAtMin = Math.abs(((S.h + 180) % 360) - 180); }
  }
  console.log(`vento ${String(tk).padStart(2)} kn scotta ${sh * 100} da ${u0} kn: indietro dopo ${f(tInd)} s, −0,5 kn ${f(t05)} s, −1 kn ${f(t1)} s; massimo all'indietro ${(-umin * KN).toFixed(2)} kn (prua a ${hAtMin.toFixed(0)}° dal vento)`);
}
console.log("2) Prua tenuta ferma nel vento");
const regime = {};
for (const tk of [6, 10, 15, 20]) {
  const S = { x: 0, y: 0, h: 0, u: 0, vl: 0, r: 0, heel: 0, heelRate: 0 };
  for (let i = 1; i <= 120 / DT; i++) { S.h = 0; S.r = 0; step(S, { sheet: 1, tiller: 0 }, { twd: 0, tws: tk / KN }, DT); }
  regime[tk] = S.u;
  console.log(`${tk} kn: regime ${(-S.u * KN).toFixed(2)} nodi all'indietro`);
}
console.log("3) Barra a fondo partendo dal regime: rotazione massima nei primi 3 s");
for (const tk of [10, 15, 20]) {
  const S = { x: 0, y: 0, h: 0, u: regime[tk], vl: 0, r: 0, heel: 0, heelRate: 0 };
  let rmax = 0;
  for (let i = 1; i <= 3 / DT; i++) { step(S, { sheet: 1, tiller: 1 }, { twd: 0, tws: tk / KN }, DT); rmax = Math.max(rmax, Math.abs(S.r)); }
  console.log(`${tk} kn: ${rmax.toFixed(0)} °/s`);
}
