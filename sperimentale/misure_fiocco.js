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

// ======================================================================
// TAPPA B — interazione fra le vele (solo ombreggiamento)
// ======================================================================
const pct = (a, b) => (b / a - 1) * 100;
console.log("\n=== B2. IL GUADAGNO SI ROVESCIA? ===");
const guad = twa => { const a = vel(P, twa, 10, null), b = vel(P, twa, 10, "best"); return pct(a.kn, b.kn); };
const bolina = [45, 50, 55, 60].map(guad), larghe = [110, 120, 135, 150].map(guad);
const med = v => v.reduce((a, b) => a + b, 0) / v.length;
console.log("  bolina 45-60°: " + bolina.map((g, i) => `${[45,50,55,60][i]}° ${g.toFixed(1)}%`).join("  ") + `  → media ${med(bolina).toFixed(1)}%`);
console.log("  larghe 110-150°: " + larghe.map((g, i) => `${[110,120,135,150][i]}° ${g.toFixed(1)}%`).join("  ") + `  → media ${med(larghe).toFixed(1)}%`);
console.log(`  confronto (deve essere bolina >= larghe): ${med(bolina) >= med(larghe) ? "RISPETTATO" : "NON rispettato"}`);
// FIOCCO tappa C: la fascia delle larghe scende, perché il fiocco coperto non dà più niente. È indicativa:
// quello che si richiede è il confronto, non la fascia.
console.log(`  fascia attesa (ipotesi nostra): bolina +8…+18%, larghe +0…+6% (indicativa, dalla tappa C; in tappa B era +2…+8%)`);

console.log("\n=== B3. VELOCITÀ UTILE CONTROVENTO ===");
const vmcList = [40, 42, 44, 45, 46, 48, 50, 52, 54, 56].map(a => {
  const u = vel(P, a, 10, "best").kn; return { a, kn: u, vmc: u * Math.cos(a * Math.PI / 180) };
});
console.log("  " + vmcList.map(x => `${x.a}°=${x.vmc.toFixed(3)}`).join(" "));
const mig = vmcList.reduce((b, x) => x.vmc > b.vmc ? x : b);
const q45 = vmcList.find(x => x.a === 45), q48 = vmcList.find(x => x.a === 48), q50 = vmcList.find(x => x.a === 50);
console.log(`  migliore a ${mig.a}° (${mig.vmc.toFixed(3)} nodi di velocità utile)`);
console.log(`  velocità utile: 45° ${q45.vmc.toFixed(3)} | 48° ${q48.vmc.toFixed(3)} | 50° ${q50.vmc.toFixed(3)}`);
const d4850 = Math.abs(pct(q48.vmc, q50.vmc));
console.log(`  differenza fra 48° e 50°: ${d4850.toFixed(2)}%` + (d4850 < 1 ? "  → SOTTO L'1%: l'ottimo è piatto, il criterio sta misurando rumore" : ""));

console.log("\n=== B4. IL FIOCCO ALLE ANDATURE LARGHE ===");
for (const twa of [110, 135, 150, 180]){
  const t = vel(P, twa, 10, "best"); const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 }; let inf;
  for (let k = 0; k < 1200; k++){ S.h = 0; inf = P.step(S, { sheet: t.trim.sheet, tiller: 0, jib: t.trim.jib }, { twd: twa, tws: 10 / KN }, 0.05); }
  const quota = inf.driveJ / (inf.driveM + inf.driveJ) * 100;
  // stessa regola del gioco, presa dal motore: niente copia qui (la copia leggeva «stallo» dove il gioco diceva «coperto»)
  const A = Math.abs(inf.awa);
  const stato = { flog: "sbatte", wind: "sopravento", lee: "STALLO", ok: "dritti" };
  const filetti = (P.jibShadedAt(A) ? "sbatte (coperto)" : stato[P.ttOf(A, inf.alphaJ)]) + (P.jibRange(A) ? "" : " · nessuna posizione giusta");
  console.log(`  ${String(twa).padStart(3)}°: fessura ${inf.fessura.toFixed(2)} ombra ${(inf.shadeJ * 100).toFixed(0)}% | incidenza ${inf.alphaJ.toFixed(0)}° | filetti ${filetti} | quota di spinta del fiocco ${quota.toFixed(2)}%`);
}

console.log("\n=== B5. REGOLARE IL FIOCCO (10 nodi) ===");
for (const twa of [45, 60, 90]){
  const best = vel(P, twa, 10, "best"), lasc = vel(P, twa, 10, 1), cazz = vel(P, twa, 10, 0);
  const vl = x => (1 - x.kn / best.kn) * 100;
  const nota = twa === 45 ? "  (a 45° «troppo cazzata» è senza soglia: la scotta non chiude oltre 10°)" : "";
  console.log(`  ${String(twa).padStart(3)}°: migliore ${best.kn.toFixed(2)} | tutta lascata −${vl(lasc).toFixed(1)}% | tutta cazzata −${vl(cazz).toFixed(1)}%${nota}`);
}

console.log("\n=== B6. GUADAGNI ASSURDI E POLARE LISCIA ===");
let maxG = -9, dove = "", denti = [];
const curva = [];
for (let a = 30; a <= 180; a += 5){
  const s0 = vel(P, a, 10, null).kn, c0 = vel(P, a, 10, "best").kn;
  curva.push({ a, c0 });
  if (s0 > 0.2){ const g = pct(s0, c0); if (g > maxG){ maxG = g; dove = a + "°"; } }
}
for (let i = 1; i < curva.length - 1; i++){
  const p0 = curva[i - 1].c0, p1 = curva[i].c0, p2 = curva[i + 1].c0;
  // tolleranza 0,04 nodi: la regolazione migliore è cercata a passi di 0,02, e vicino al massimo
  // della polare due angoli vicini danno numeri che differiscono meno della risoluzione della ricerca
  if ((p1 - p0) * (p2 - p1) < 0 && Math.max(Math.abs(p1 - p0), Math.abs(p2 - p1)) > 0.04) denti.push(`${curva[i].a}° (${p0.toFixed(2)} ${p1.toFixed(2)} ${p2.toFixed(2)})`);
}
console.log(`  guadagno massimo ${maxG.toFixed(1)}% a ${dove} (soglia 30%)`);
console.log(`  massimi e minimi locali fra 30° e 180°, a passi di 5° (tolleranza 0,04 nodi): ${denti.length ? denti.join(", ") : "nessuno oltre il massimo della polare"}`);
const picco = curva.reduce((b, x) => x.c0 > b.c0 ? x : b);
console.log(`  angolo più veloce: ${picco.a}° (${picco.c0.toFixed(2)} nodi)`);
console.log("  polare con fiocco: " + curva.filter(x => x.a % 15 === 0).map(x => `${x.a}°=${x.c0.toFixed(2)}`).join(" "));

console.log("\n=== B7. SICUREZZA ===");
for (const g of [16, 18, 20]){
  const prova = jib => {
    const S = { x: 0, y: 0, h: 0, u: 1.5, vl: 0, r: 0 };
    const C = jib === null ? { sheet: 0.1, tiller: 0 } : { sheet: 0.1, tiller: 0, jib: 0.1 };
    for (let t = 0; t < 30; t += 0.02){ S.h = 0; P.step(S, C, { twd: 45, tws: 10 / KN }, 0.02); }
    let max = 0;
    for (let t = 0; t < 6; t += 0.02){ S.h = 0; P.step(S, C, { twd: 45, tws: g / KN }, 0.02); max = Math.max(max, S.heel); }
    return max.toFixed(0) + "°" + (max > 60 ? " (SCUFFIA)" : "");
  };
  console.log(`  raffica da 10 a ${g} nodi senza reagire: senza fiocco ${prova(null)} | con fiocco ${prova(0.1)}`);
}
{
  const S = { x: 0, y: 0, h: 45, u: 3.4 / KN, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 };
  let max = 0;
  for (let t = 0; t < 60; t += 1 / 240){ P.step(S, { sheet: 0.2, tiller: 0, jib: 0.2 }, { twd: 0, tws: 10 / KN }, 1 / 240); max = Math.max(max, Math.abs(S.heel)); }
  console.log(`  60 s di bolina con 10 nodi costanti, regolato: sbandamento massimo ${max.toFixed(0)}° (scuffia a 60°)`);
}

console.log("\n=== B8. POSIZIONE GIUSTA DEL FIOCCO, per vento apparente ===");
console.log("  (randa regolata; «dritti» = incidenza del fiocco fra 8° e 27°; regola presa dal motore)");
for (let A = 30; A <= 180; A += 10){
  const r = P.jibRange(A);
  const nota = r ? (r[1] - r[0] < 10 ? "  (stretta)" : "") : "";
  const perche = A < P.BOAT.luffA0 + P.BOAT.luffW * 0.5 ? "angolo morto: sbattono tutte e due le vele" : "coperto dalla randa o scotta al massimo";
  console.log(`  ${String(A).padStart(3)}° apparenti: ${r ? "SÌ, fiocco fra " + r[0].toFixed(0) + "° e " + r[1].toFixed(0) + "°" + nota
    : "no — " + perche}   (ombra ${(P.BOAT.slotShade * (1 - P.fessuraDi(A)) * 100).toFixed(0)}%)`);
}
const ultimo = [...Array(160).keys()].map(i => i + 30).filter(a => P.jibRange(a)).pop();
const stretta = [...Array(160).keys()].map(i => i + 30).find(a => { const r = P.jibRange(a); return r && r[1] - r[0] < 10; });
// FIOCCO tappa C: jibShadedAt è ora «non esiste una posizione giusta», vera anche nell'angolo morto:
// la ricerca parte sopra l'angolo morto, se no risponderebbe sempre 30°.
const coperto = [...Array(160).keys()].map(i => i + 30).filter(a => a >= P.BOAT.luffA0 + P.BOAT.luffW * 0.5).find(a => P.jibShadedAt(a));
console.log(`  ultimo angolo con una posizione giusta: ${ultimo}° apparenti; da ${stretta}° la regolazione è stretta`);
console.log(`  i filetti del fiocco cominciano a sbattere per copertura a ${coperto}° apparenti`);

// ======================================================================
// TAPPA C, primo compito — coerenza fra vista e forza del fiocco coperto   // FIOCCO
// ======================================================================
console.log("\n=== C1.1 QUOTA DI SPINTA DOVE IL PANNELLO DICE «QUI NON SI REGOLA» ===");
console.log("  (soglia dichiarata prima: ≤ 3%. La quota non dipende da vento né sbandamento: sono");
console.log("   fattori comuni alle due vele. Si prende la regolazione del fiocco più favorevole.)");
{
  const quotaA = (A, jb) => {
    const sh = P.BOAT.slotShade * (1 - P.fessuraDi(A));
    const M = P.sailF(P.BOAT.sailArea, Math.min(P.BOAT.maxBoom, Math.max(P.BOAT.minBoom, A - 17)), A, 5, 1, 1);
    const J = P.sailF(P.BOAT.jibArea * (1 - sh), P.BOAT.minJib + jb * (P.BOAT.maxJib - P.BOAT.minJib), A, 5, 1, 1);
    return 100 * J.drive / (M.drive + J.drive);
  };
  let peggio = -9, dovePeg = 0, fuori = [];
  for (let A = 108; A <= 180; A++){
    let q = -9;
    for (let jb = 0; jb <= 1.0001; jb += 0.05) q = Math.max(q, quotaA(A, jb));
    if (q > peggio){ peggio = q; dovePeg = A; }
    if (q > 3) fuori.push(A + "°=" + q.toFixed(1) + "%");
  }
  console.log(`  da 108° a 180° apparenti, a passi di 1°: quota massima ${peggio.toFixed(2)}% (a ${dovePeg}°)`);
  console.log(`  angoli sopra la soglia del 3%: ${fuori.length ? fuori.join(" ") : "nessuno"}`);
  console.log("  tabella (regolazione automatica, bugna a A−17):");
  const riga = as => "   " + as.map(A => `${A}°=${quotaA(A, Math.max(0, Math.min(1, (A - 17 - P.BOAT.minJib) / (P.BOAT.maxJib - P.BOAT.minJib)))).toFixed(1)}%`).join("  ");
  console.log(riga([70, 85, 90, 95, 100, 103, 105]));
  console.log(riga([107, 108, 110, 115, 120, 135, 150, 180]));
}

console.log("\n=== C1.2 NIENTE OMBRA AL TRAVERSO ===");
{
  const om = A => P.BOAT.slotShade * (1 - P.fessuraDi(A)) * 100;
  let primo = null;
  for (let A = 30; A <= 180; A += 0.5) if (om(A) > 0){ primo = A; break; }
  console.log(`  ombra a 70° apparenti: ${om(70).toFixed(0)}% — a 85°: ${om(85).toFixed(0)}% — a 90°: ${om(90).toFixed(0)}%`);
  console.log(`  primo angolo con un po' d'ombra: ${primo}° apparenti (soglia: nessuna ombra fino a 85°)`);
}

console.log("\n=== C1.7 NIENTE BISTABILITÀ (la rampa è più ripida: due partenze diverse) ===");
{
  // stessa ricerca della regolazione migliore, ma partendo da ferma e da lanciata
  const eq = (twa, u0) => {
    let best = -9;
    for (let sh = 0; sh <= 1.0001; sh += 0.05) for (let jb = 0; jb <= 1.0001; jb += 0.05){
      const S = { x: 0, y: 0, h: 0, u: u0, vl: 0, r: 0 };
      for (let t = 0; t < 90; t += 0.05){ S.h = 0; P.step(S, { sheet: sh, tiller: 0, jib: jb }, { twd: twa, tws: 10 / KN }, 0.05); }
      if (Math.abs(S.heel) <= 60) best = Math.max(best, S.u * KN);
    }
    return best;
  };
  let peggio = 0;
  for (const twa of [115, 120, 125, 130, 135, 140]){
    const a = eq(twa, 0.2), b = eq(twa, 4.0), d = Math.abs(a - b);
    peggio = Math.max(peggio, d);
    console.log(`  ${twa}° reali: da ferma ${a.toFixed(3)} nodi | lanciata ${b.toFixed(3)} nodi | differenza ${d.toFixed(3)}`);
  }
  console.log(`  differenza massima ${peggio.toFixed(3)} nodi (soglia 0,02)`);
}

console.log("\n=== C1.EXTRA A QUALE VENTO REALE CORRISPONDONO 95° E 107° APPARENTI (10 nodi) ===");
{
  const app = twa => {
    const t = vel(P, twa, 10, "best"); const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 }; let inf;
    for (let k = 0; k < 1800; k++){ S.h = 0; inf = P.step(S, { sheet: t.trim.sheet, tiller: 0, jib: t.trim.jib }, { twd: twa, tws: 10 / KN }, 0.05); }
    return { A: Math.abs(inf.awa), kn: S.u * KN };
  };
  const tab = [];
  for (let twa = 100; twa <= 160; twa += 2) tab.push({ twa, ...app(twa) });
  const trova = obiettivo => {
    for (let i = 1; i < tab.length; i++) if (tab[i].A >= obiettivo && tab[i - 1].A < obiettivo){
      const f = (obiettivo - tab[i - 1].A) / (tab[i].A - tab[i - 1].A);
      return (tab[i - 1].twa + f * (tab[i].twa - tab[i - 1].twa));
    }
    return null;
  };
  console.log("  " + tab.filter(x => x.twa % 10 === 0).map(x => `${x.twa}°→${x.A.toFixed(0)}app`).join("  "));
  const a95 = trova(95), a107 = trova(107);
  console.log(`  95° apparenti ≈ ${a95 === null ? "fuori tabella" : a95.toFixed(0) + "° reali"} (qui comincia l'ombra)`);
  console.log(`  107° apparenti ≈ ${a107 === null ? "fuori tabella" : a107.toFixed(0) + "° reali"} (qui l'ombra è totale e il pannello smette di dare una posizione)`);
}

console.log("\n=== C1.EXTRA LA RAMPA FA UNO SCALINO? (10 nodi, grado per grado) ===");
{
  const v = [];
  for (let twa = 113; twa <= 142; twa++) v.push({ twa, kn: vel(P, twa, 10, "best", 0.02).kn });
  console.log("  " + v.filter(x => x.twa >= 115 && x.twa <= 140 && x.twa % 5 === 0).map(x => `${x.twa}°=${x.kn.toFixed(3)}`).join("  "));
  let peg = 0, dove = 0; const der = [];
  for (let i = 1; i < v.length; i++){
    const d = v[i].kn - v[i - 1].kn;
    if (v[i].twa >= 115 && v[i].twa <= 140){ der.push(d); if (Math.abs(d) > Math.abs(peg)){ peg = d; dove = v[i].twa; } }
  }
  const media = der.reduce((a, b) => a + b, 0) / der.length;
  console.log(`  variazione per grado fra 115° e 140°: media ${media.toFixed(4)} nodi/°, massima ${peg.toFixed(4)} nodi/° (a ${dove}°)`);
  console.log(`  rapporto fra la variazione massima e la media: ${(peg / media).toFixed(2)} (uno scalino darebbe un rapporto alto)`);
  console.log("  grado per grado: " + v.filter(x => x.twa >= 115 && x.twa <= 140).map(x => x.kn.toFixed(3)).join(" "));
  // confronto con la taratura della tappa B, per vedere quanto si è irrigidita la curva
  const a0 = P.BOAT.slotA0, w0 = P.BOAT.slotW, s0 = P.BOAT.slotShade;
  P.BOAT.slotA0 = 85; P.BOAT.slotW = 50; P.BOAT.slotShade = 0.70;
  const vB = [];
  for (let twa = 113; twa <= 142; twa++) vB.push({ twa, kn: vel(P, twa, 10, "best", 0.02).kn });
  P.BOAT.slotA0 = a0; P.BOAT.slotW = w0; P.BOAT.slotShade = s0;
  let pegB = 0; const derB = [];
  for (let i = 1; i < vB.length; i++){ const d = vB[i].kn - vB[i - 1].kn; if (vB[i].twa >= 115 && vB[i].twa <= 140){ derB.push(d); if (Math.abs(d) > Math.abs(pegB)) pegB = d; } }
  const mediaB = derB.reduce((a, b) => a + b, 0) / derB.length;
  console.log(`  per confronto, con la taratura della tappa B (85/50/0,70): media ${mediaB.toFixed(4)} nodi/°, massima ${pegB.toFixed(4)} nodi/°, rapporto ${(pegB / mediaB).toFixed(2)}`);
}
