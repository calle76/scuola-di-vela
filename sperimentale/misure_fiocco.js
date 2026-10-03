// Misure della tappa A del prototipo del fiocco. Uso: node misure_fiocco.js
// Legge la fisica da sperimentale/fiocco.html (prototipo) e da index.html (gioco, per il confronto).
const P = require("./motore_fiocco.js");                 // prototipo
const G = require("../tests/fisica/motore.js");          // gioco
const KN = 1.943844;

// velocità di equilibrio a un angolo dal vento, cercando la regolazione migliore
// jibMode: null = senza fiocco (nessuna scotta), "best" = cercata, numero = scotta fissa
function vel(mot, twa, kn, jibMode, passo = 0.02){
  const prova = (sh, jb) => {
    const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 };
    const C = jb === null ? { sheet: sh, tiller: 0 } : { sheet: sh, tiller: 0, jib: Math.max(0, Math.min(1, jb)) };
    for (let t = 0; t < 60; t += 0.05){ S.h = 0; mot.step(S, C, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) break; }
    return Math.abs(S.heel) <= 60 ? { u: S.u, heel: S.heel } : null;
  };
  // ricerca a maglia larga, poi affinata attorno al migliore: 2601 prove diventano circa 250
  let best = null;
  const giro = (sh0, sh1, jb0, jb1, p) => {
    for (let sh = sh0; sh <= sh1 + 1e-9; sh += p){
      const jibs = jibMode === null ? [null] : jibMode === "best" ? Array.from({ length: Math.round((jb1 - jb0) / p) + 1 }, (_, i) => jb0 + i * p) : [jibMode];
      for (const jb of jibs){
        const r = prova(Math.max(0, Math.min(1, sh)), jb);
        if (r && (!best || r.u > best.u)) best = { u: r.u, sheet: sh, jib: jb, heel: r.heel };
      }
    }
  };
  giro(0, 1, 0, 1, 0.1);
  if (best) giro(Math.max(0, best.sheet - 0.1), Math.min(1, best.sheet + 0.1), jibMode === "best" ? Math.max(0, best.jib - 0.1) : 0, jibMode === "best" ? Math.min(1, best.jib + 0.1) : 0, passo);
  return { kn: best ? best.u * KN : -9, trim: best };
}
const ANG = [20, 25, 30, 45, 60, 90, 110, 135, 150, 180], VENTI = [6, 10, 15];

// ---- criterio 1: non-regressione ----
console.log("=== 1. NON-REGRESSIONE (fiocco assente) ===");
let peggio = 0, peggioDove = "";
for (const kn of VENTI) for (const twa of ANG){
  const a = vel(G, twa, kn, null), b = vel(P, twa, kn, null);
  const d = Math.abs(a.kn - b.kn);
  if (d > peggio){ peggio = d; peggioDove = `${kn} nodi, ${twa}°`; }
}
console.log(`30 casi, scarto massimo ${peggio.toExponential(2)} nodi (${peggioDove}) — soglia 0,001`);
// anche con jibArea = 0 ma la scotta presente
const areaVera = P.BOAT.jibArea; P.BOAT.jibArea = 0;
let peggio0 = 0, dove0 = "";
for (const kn of VENTI) for (const twa of ANG){
  const a = vel(G, twa, kn, null), b = vel(P, twa, kn, 0.4);
  const d = Math.abs(a.kn - b.kn);
  if (d > peggio0){ peggio0 = d; dove0 = `${kn} nodi, ${twa}°`; }
}
console.log(`30 casi con area 0 e scotta presente, scarto massimo ${peggio0.toExponential(2)} nodi (${dove0})`);
P.BOAT.jibArea = areaVera;

// virata e raffica, senza fiocco, prototipo contro gioco
function virata(mot, kn0, jib){
  const S = { x: 0, y: 0, h: 45, u: kn0 / KN, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 };
  const C = jib === null ? { sheet: 0.2, tiller: -1 } : { sheet: 0.2, tiller: -1, jib };
  for (let t = 0; t < 20; t += 1 / 240){ mot.step(S, C, { twd: 0, tws: 10 / KN }, 1 / 240); if (((S.h + 360) % 360) < 316 && ((S.h + 360) % 360) > 300) return { ok: true, t }; }
  return { ok: false, h: (S.h + 360) % 360, u: S.u * KN };
}
function raffica(mot, gust, jib){
  const S = { x: 0, y: 0, h: 45, u: 3.4 / KN, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 };
  const C = jib === null ? { sheet: 0.2, tiller: 0 } : { sheet: 0.2, tiller: 0, jib };
  for (let t = 0; t < 10; t += 1 / 240) mot.step(S, C, { twd: 0, tws: 10 / KN }, 1 / 240);
  let max = 0;
  for (let t = 0; t < 6; t += 1 / 240){ mot.step(S, C, { twd: 0, tws: gust / KN }, 1 / 240); max = Math.max(max, Math.abs(S.heel)); }
  return max;
}
const vg = virata(G, 3.9, null), vp = virata(P, 3.9, null);
console.log(`virata a 3,9 nodi senza fiocco: gioco ${vg.ok ? vg.t.toFixed(3) + " s" : "fallita"}, prototipo ${vp.ok ? vp.t.toFixed(3) + " s" : "fallita"}`);
for (const g of [16, 18, 20]) console.log(`raffica ${g} nodi senza fiocco: gioco ${raffica(G, g, null).toFixed(2)}°, prototipo ${raffica(P, g, null).toFixed(2)}°`);

// ---- criterio 2: angolo morto ----
console.log("\n=== 2. ANGOLO MORTO ===");
for (const [nome, mode] of [["senza fiocco", null], ["con fiocco", "best"]]){
  let primo = null;
  for (let twa = 28; twa <= 44; twa += 0.5){ if (vel(P, twa, 10, mode, 0.05).kn > 0.5){ primo = twa; break; } }
  console.log(`${nome}: primo angolo sopra 0,5 nodi = ${primo}°; a 30° = ${vel(P, 30, 10, mode, 0.05).kn.toFixed(2)} nodi`);
}

// ---- criterio 3: guadagno ----
console.log("\n=== 3. GUADAGNO (10 nodi, tutto regolato al meglio) ===");
const righe = [];
for (const twa of [45, 48, 60, 90, 110, 135, 150, 180]){
  const a = vel(P, twa, 10, null), b = vel(P, twa, 10, "best");
  righe.push({ twa, senza: a.kn, con: b.kn, dp: (b.kn / a.kn - 1) * 100, trim: b.trim });
  console.log(`${String(twa).padStart(3)}°: senza ${a.kn.toFixed(2)} → con ${b.kn.toFixed(2)} nodi (${((b.kn / a.kn - 1) * 100).toFixed(1)}%) | randa ${(b.trim.sheet * 100).toFixed(0)}% fiocco ${(b.trim.jib * 100).toFixed(0)}% sband. ${b.trim.heel.toFixed(1)}°`);
}
const vmc = m => Math.max(...[40, 42, 45, 48, 50, 55].map(a => vel(P, a, 10, m, 0.05).kn * Math.cos(a * Math.PI / 180)));
const vmcA = a => [40, 42, 45, 48, 50, 55].reduce((b, x) => vel(P, x, 10, a, 0.05).kn * Math.cos(x * Math.PI / 180) > vel(P, b, 10, a, 0.05).kn * Math.cos(b * Math.PI / 180) ? x : b, 40);
console.log(`migliore velocità controvento: senza fiocco ${vmc(null).toFixed(2)} a ${vmcA(null)}°, con fiocco ${vmc("best").toFixed(2)} a ${vmcA("best")}°`);
const maxA = m => [60, 75, 90, 105, 120].reduce((b, x) => vel(P, x, 10, m, 0.05).kn > vel(P, b, 10, m, 0.05).kn ? x : b, 60);
console.log(`angolo più veloce: senza fiocco ${maxA(null)}°, con fiocco ${maxA("best")}°`);
for (const kn of [6, 15]){
  const l = [45, 60, 90, 135].map(twa => { const a = vel(P, twa, kn, null), b = vel(P, twa, kn, "best"); return `${twa}° ${a.kn.toFixed(2)}→${b.kn.toFixed(2)} (${((b.kn / a.kn - 1) * 100).toFixed(0)}%)`; });
  console.log(`${kn} nodi: ` + l.join("  "));
}

// ---- criterio 4: regolare deve contare ----
console.log("\n=== 4. REGOLARE IL FIOCCO CONTA (10 nodi) ===");
for (const twa of [45, 60, 90]){
  const best = vel(P, twa, 10, "best");
  const jbest = best.trim.jib;
  const lasc = vel(P, twa, 10, 1), cazz = vel(P, twa, 10, 0);
  const vl = (x) => ((1 - x.kn / best.kn) * 100).toFixed(1);
  console.log(`${String(twa).padStart(3)}°: migliore ${best.kn.toFixed(2)} (fiocco ${(jbest * 100).toFixed(0)}% = ${(P.BOAT.minJib + jbest * (P.BOAT.maxJib - P.BOAT.minJib)).toFixed(0)}°) | tutta lascata ${lasc.kn.toFixed(2)} (−${vl(lasc)}%) | tutta cazzata ${cazz.kn.toFixed(2)} (−${vl(cazz)}%)`);
}
// segno dell'errore: incidenza del fiocco nei tre casi
console.log("segno dell'errore (incidenza del fiocco a 60°, 10 nodi):");
for (const [nome, jb] of [["migliore", vel(P, 60, 10, "best").trim.jib], ["tutta cazzata", 0], ["tutta lascata", 1]]){
  const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 }; let inf;
  for (let t = 0; t < 60; t += 0.05){ S.h = 0; inf = P.step(S, { sheet: 0.45, tiller: 0, jib: jb }, { twd: 60, tws: 10 / KN }, 0.05); }
  console.log(`  ${nome}: fiocco a ${inf.jib.toFixed(0)}°, incidenza ${inf.alphaJ.toFixed(0)}° (stallo sopra 20°, fileggia sotto 6°)`);
}

// ---- criterio 5: sbandamento ----
console.log("\n=== 5. SBANDAMENTO ===");
for (const twa of [45, 60, 90]){
  const a = vel(P, twa, 10, null), b = vel(P, twa, 10, "best");
  console.log(`${String(twa).padStart(3)}° con 10 nodi: senza ${a.trim.heel.toFixed(1)}° → con ${b.trim.heel.toFixed(1)}° (${(b.trim.heel - a.trim.heel >= 0 ? "+" : "") + (b.trim.heel - a.trim.heel).toFixed(1)}°)`);
}
for (const g of [16, 18, 20]) console.log(`raffica ${g} nodi senza reagire, di bolina: senza fiocco ${raffica(P, g, null).toFixed(0)}° | con fiocco ${raffica(P, g, 0.2).toFixed(0)}°${raffica(P, g, 0.2) > 60 ? " (SCUFFIA)" : ""}`);
{
  const S = { x: 0, y: 0, h: 45, u: 3.4 / KN, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 };
  let max = 0;
  for (let t = 0; t < 60; t += 1 / 240){ P.step(S, { sheet: 0.2, tiller: 0, jib: 0.2 }, { twd: 0, tws: 10 / KN }, 1 / 240); max = Math.max(max, Math.abs(S.heel)); }
  console.log(`60 s di bolina con 10 nodi costanti, tutto regolato: sbandamento massimo ${max.toFixed(0)}° (scuffia a 60°)`);
}

// ---- criterio 7: stabilità numerica ----
console.log("\n=== 7. STABILITÀ NUMERICA ===");
let brutti = 0, uMin = 9, uMax = -9, hMax = 0;
let seme = 12345; const caso = () => (seme = (seme * 1103515245 + 12345) % 2147483648) / 2147483648; // numeri casuali ripetibili: così il confronto fra due versioni è esatto
for (let r = 0; r < 10; r++){
  const S = { x: 0, y: 0, h: caso() * 360, u: 1, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 };
  const C = { sheet: caso(), tiller: 0, jib: caso() };
  for (let t = 0; t < 120; t += 1 / 240){
    if (caso() < 0.01){ C.sheet = caso(); C.jib = caso(); C.tiller = caso() * 2 - 1; }
    P.step(S, C, { twd: 0, tws: 10 / KN }, 1 / 240);
    if (!Number.isFinite(S.u) || !Number.isFinite(S.heel) || !Number.isFinite(S.h)) brutti++;
    uMin = Math.min(uMin, S.u * KN); uMax = Math.max(uMax, S.u * KN); hMax = Math.max(hMax, Math.abs(S.heel));
  }
}
console.log(`10 corse da 120 s con scotte e barra a caso: NaN ${brutti}, velocità da ${uMin.toFixed(2)} a ${uMax.toFixed(2)} nodi (soglia −2,5…9), sbandamento massimo ${hMax.toFixed(0)}°`);
