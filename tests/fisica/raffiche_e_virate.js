// Virate a diverse velocità e raffiche improvvise di bolina. Uso: node raffiche_e_virate.js
const { step, norm180 } = require("./motore.js");
const E10 = { twd: 0, tws: 10 / 1.944 };
function virata(u0){
  const S = { x: 0, y: 0, h: 45, u: u0, vl: 0, r: 0 };
  for (let t = 0; t < 12; t += 0.05){
    step(S, { sheet: 0, tiller: 0.8 }, E10, 0.05);
    if (norm180(S.h) < -44) return `riuscita in ${t.toFixed(1)} s`;
  }
  return `fallita (prua a ${norm180(S.h).toFixed(0)}°, velocità ${(S.u * 1.944).toFixed(1)} nodi)`;
}
for (const u of [2, 1, 0.2]) console.log(`Virata partendo a ${(u * 1.944).toFixed(1)} nodi: ${virata(u)}`);
for (const g of [16, 18, 20]){
  const prova = lasca => {
    const S = { x: 0, y: 0, h: 0, u: 1.5, vl: 0, r: 0 };
    for (let t = 0; t < 30; t += 0.02){ S.h = 0; step(S, { sheet: 0.1, tiller: 0 }, { twd: 45, tws: 10 / 1.944 }, 0.02); }
    let max = 0;
    for (let t = 0; t < 6; t += 0.02){ S.h = 0; step(S, { sheet: lasca && t > 0.5 ? 0.5 : 0.1, tiller: 0 }, { twd: 45, tws: g / 1.944 }, 0.02); max = Math.max(max, S.heel); }
    return max.toFixed(0) + "°" + (max > 60 ? " (scuffia)" : "");
  };
  console.log(`Raffica da 10 a ${g} nodi: senza reagire ${prova(false)}, lascando ${prova(true)}`);
}
