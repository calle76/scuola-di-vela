// Timone del livello 2 (1.0.24-1.0.25, docs/archivio/PROPOSTA-STALLO-TIMONE.md §8-9): virate, strambate, risposta a barra piccola e giro di penalità.
// Dalla 1.0.25 la barra va sempre a 1,6 al secondo come nel livello 1: la sola freccia fino a 35° («sicura»), Maiusc + freccia fino a 45°;
// si confrontano sola freccia, freccia e Maiusc insieme, freccia con 1 s di pausa a 35° e poi Maiusc, e il livello 1.
// Uso: node timone2.js                         criteri C1-C9 sui venti di taratura (10, 14) e di conferma (6, 8, 12, 16)
//      node timone2.js stallo 15                stesso giro con un altro angolo di stallo (sensibilità)
//      node timone2.js griglia                  taratura di yawG e yawRho sui soli venti di taratura
// Esce con 1 se un criterio è fuori soglia (senza argomenti).
const { step, norm180, RUD2, RUD2_SICURA } = require("./motore.js");
const SICURA = RUD2_SICURA, VELOCE = 1.6; // barra al secondo (frazione della corsa), come nel livello 1
const arg = process.argv.slice(2);
if (arg[0] === "stallo") RUD2.stallA = +arg[1];

function bolina(kn, lv, frac = 1){ // barca a regime di bolina (prua tenuta a 45°), poi rallentata fino a frac della velocità
  const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: 45, u: 1.5, vl: 0, r: 0, lv };
  for (let t = 0; t < 40; t += 0.01){ S.h = 45; step(S, { sheet: 0.1, tiller: 0 }, E, 0.01); }
  if (frac < 1){ const u = S.u * frac; while (S.u > u){ S.h = 45; step(S, { sheet: 1, tiller: 0 }, E, 0.01); } }
  return { S, E };
}
// virata: barra verso 'max' alla velocità 'rate'; con la prua oltre −40° la barra torna al centro in fretta (come in F4: la si molla, in tutte e due le virate).
// La velocità minima (C1, C5) è quella di tutta la manovra fino a 3 s dopo, come in F4; si stampano a parte lo stallo e la minima prima di mollare la barra.
function virata(kn, lv, rate, max = 1, frac = 1, pausa = null){ // pausa: secondi fermi a 35° prima di andare a max
  const { S, E } = bolina(kn, lv, frac), u0 = S.u;
  let b = 0, t0 = null, t1 = null, dist = 0, umin = S.u, lasciata = false, st = 0, stR = 0, tf = null, umin1 = S.u;
  for (let t = 0; t < 20; t += 0.01){
    if (!lasciata){ const lim = pausa !== null && t < SICURA / rate + pausa ? SICURA : max; b = Math.min(lim, b + rate * 0.01); } else b = Math.max(0, b - VELOCE * 0.01);
    step(S, { sheet: 0.1, tiller: b }, E, 0.01);
    const a = norm180(S.h);
    if (S.stall){ if (lasciata) stR += 0.01; else st += 0.01; } // stallo mentre la prua gira (st) e mentre si molla la barra (stR)
    if (t0 === null && a < 40) t0 = t;
    if (t0 !== null && t1 === null) dist += S.u * 0.01;
    if (t1 === null && a < -40) t1 = t;
    if (a < -40) lasciata = true;
    if (tf === null && a < -44) tf = t;
    if (tf !== null && t > tf + 3) break;
    umin = Math.min(umin, S.u); if (!lasciata) umin1 = Math.min(umin1, S.u);
  }
  if (tf === null) return null;
  return { u0, dur: tf, curv: (80 * Math.PI / 180) / dist, minFr: umin / u0, min1Fr: umin1 / u0, stall: st, stallR: stR };
}
function strambata(kn, lv, rate, max = 1){
  const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: 150, u: 1.5, vl: 0, r: 0, lv };
  for (let t = 0; t < 40; t += 0.01){ S.h = 150; step(S, { sheet: 1, tiller: 0 }, E, 0.01); }
  let b = 0;
  for (let t = 0; t < 20; t += 0.01){
    b = Math.max(-max, b - rate * 0.01); step(S, { sheet: 1, tiller: b }, E, 0.01);
    if (S.capsized || Math.abs(S.heel) > 60) return null;
    if (norm180(S.h) < 0 && norm180(S.h) > -151) return t; // prua oltre 210°
  }
  return null;
}
function risposta(kn){ // barra fissa a 5°: tempo per arrivare al 63% della rotazione che ha dopo 3 s
  const { S, E } = bolina(kn, 2), tl = 5 / RUD2.maxRudder, rs = [];
  for (let t = 0; t < 3; t += 0.01){ step(S, { sheet: 0.1, tiller: tl }, E, 0.01); rs.push([t, Math.abs(S.r)]); }
  const fin = rs[rs.length - 1][1];
  return rs.find(([t, r]) => r >= 0.63 * fin)[0];
}
function giro(kn, rate, max = 1){ // giro di penalità: 360° partendo di bolina, scotta regolata secondo il vento
  const { S, E } = bolina(kn, 2); let b = 0, tot = 0, prev = S.h;
  for (let t = 0; t < 40; t += 0.01){
    b = Math.min(max, b + rate * 0.01);
    const twa = Math.abs(norm180(E.twd - S.h));
    step(S, { sheet: Math.max(0.1, Math.min(1, (twa - 30) / 120)), tiller: b }, E, 0.01);
    tot += Math.abs(norm180(S.h - prev)); prev = S.h;
    if (tot >= 360) return { t, u: S.u * 1.944 }; // nodi
  }
  return null;
}
const kn2 = x => (x * 1.944).toFixed(1);

function criteri(kn){
  // L = sola freccia (35°), V = freccia e Maiusc insieme (45°), P = 35°, 1 s di pausa, poi Maiusc (45°)
  const L = virata(kn, 2, VELOCE, SICURA), V = virata(kn, 2, VELOCE), P = virata(kn, 2, VELOCE, 1, 1, 1), uno = virata(kn, undefined, VELOCE);
  if (!L || !V || !P) return { kn, ok: false, righe: [`${kn} nodi: una virata non riesce (sola freccia ${!!L}, Maiusc ${!!V}, con pausa ${!!P})`] };
  const c = {
    C1: [L.minFr - V.minFr >= 0.05, `minima/entrata sola freccia ${(L.minFr * 100).toFixed(0)}% contro Maiusc insieme ${(V.minFr * 100).toFixed(0)}% (almeno 5 punti)`],
    C2: [V.dur <= 0.9 * L.dur, `con 45° ${V.dur.toFixed(2)} s contro 35° ${L.dur.toFixed(2)} s (almeno il 10% più rapida)`],
    C3: [L.curv >= 0.12 && L.curv <= 0.30, `curvatura media sola freccia ${L.curv.toFixed(2)} rad/m (0,12-0,30)`],
    C4: [L.dur >= 2.5 && L.dur <= 4.5, `virata sola freccia ${L.dur.toFixed(2)} s (2,5-4,5)`],
    C5: [L.minFr >= 0.35 && L.minFr <= 0.60, `minima/entrata sola freccia ${(L.minFr * 100).toFixed(0)}% (35-60%)`],
  };
  const righe = [`${kn} nodi (entrata ${kn2(L.u0)} nodi; livello 1: ${uno.dur.toFixed(2)} s, ${uno.curv.toFixed(2)} rad/m, minima ${(uno.minFr * 100).toFixed(0)}%; Maiusc insieme: ${V.dur.toFixed(2)} s, ${V.curv.toFixed(2)} rad/m; con pausa: ${P.dur.toFixed(2)} s, minima ${(P.minFr * 100).toFixed(0)}%)`,
    `   stallo mentre la prua gira / mentre si molla la barra: sola freccia ${L.stall.toFixed(2)} / ${L.stallR.toFixed(2)} s, Maiusc insieme ${V.stall.toFixed(2)} / ${V.stallR.toFixed(2)} s, con pausa ${P.stall.toFixed(2)} / ${P.stallR.toFixed(2)} s`];
  let ok = true;
  for (const [k, [p, s]] of Object.entries(c)){ righe.push(`  ${k} ${p ? "ok   " : "FUORI"} ${s}`); ok = ok && p; }
  return { kn, ok, righe, L, V, P, c };
}

module.exports = { virata, strambata, risposta, giro, criteri, RUD2, SICURA, VELOCE };
if (require.main !== module) return;

if (arg[0] === "griglia"){
  for (const g of [0.2, 0.3, 0.4, 0.6, 0.8, 1.2]) for (const rho of [0.5, 1.05, 1.5, 2.0, 3.0]){
    RUD2.yawG = g; RUD2.yawRho = rho;
    const r = [10, 14].map(criteri), pass = r.map(x => x.ok ? "ok" : Object.entries(x.c || {}).filter(([k, v]) => !v[0]).map(([k]) => k).join("+") || "fallita");
    const L = r[0].L;
    console.log(`yawG ${g} yawRho ${rho}: 10 nodi ${pass[0]}, 14 nodi ${pass[1]}` + (L ? `  (10 nodi: ${L.dur.toFixed(2)} s, ${L.curv.toFixed(2)} rad/m, ${(L.minFr * 100).toFixed(0)}%)` : ""));
  }
  process.exit(0);
}

console.log(`Timone del livello 2: stallo ${RUD2.stallA}°, yawG ${RUD2.yawG}, yawRho ${RUD2.yawRho}, xR ${RUD2.xR} m, barra fino a ${RUD2.maxRudder}°, resistenza ${RUD2.dragK}`);
let tutti = true;
for (const [nome, venti] of [["taratura", [10, 14]], ["conferma", [6, 8, 12, 16]]]){
  console.log(`-- ${nome}`);
  for (const kn of venti){ const r = criteri(kn); r.righe.forEach(s => console.log(s)); tutti = tutti && r.ok; }
}
const c7 = virata(6, 2, VELOCE, SICURA, 0.7);
console.log(`C7 ${c7 ? "ok   " : "FUORI"} virata con 6 nodi entrando al 70% della bolina, sola freccia: ${c7 ? c7.dur.toFixed(2) + " s" : "non riesce"}`);
tutti = tutti && !!c7;
for (const kn of [6, 10, 14]){
  const s2 = strambata(kn, 2, VELOCE, SICURA), s1 = strambata(kn, undefined, VELOCE), ok = s2 !== null && s1 !== null && s2 <= 1.5 * s1;
  console.log(`C8 ${ok ? "ok   " : "FUORI"} strambata con ${kn} nodi: livello 2 sola freccia ${s2 === null ? "non riesce" : s2.toFixed(2) + " s"}, livello 1 ${s1 === null ? "non riesce" : s1.toFixed(2) + " s"} (al massimo 1,5 volte)`);
  tutti = tutti && ok;
}
for (const kn of [6, 10, 14]){ const t = risposta(kn), ok = t <= 1.0; console.log(`C9 ${ok ? "ok   " : "FUORI"} risposta a 5° di barra con ${kn} nodi: 63% in ${t.toFixed(2)} s (al massimo 1,0)`); tutti = tutti && ok; }
for (const kn of [6, 10, 14]) for (const [n, m] of [["sola freccia", SICURA], ["con Maiusc", 1]]){
  const g = giro(kn, VELOCE, m); console.log(`giro di penalità (360°, nessuna soglia) con ${kn} nodi, barra ${n}: ${g ? g.t.toFixed(1) + " s, uscita a " + g.u.toFixed(1) + " nodi" : "non riesce in 40 s"}`);
}
console.log(tutti ? "ESITO: tutti i criteri nelle soglie" : "ESITO: almeno un criterio FUORI soglia");
if (!arg.length) process.exit(tutti ? 0 : 1);
