// Raffiche alle andature portanti (1.0.9, docs/PROPOSTA-RAFFICHE-PORTANTI.md). Uso: node raffiche_portanti.js [esplorazione]
// Barca a regime con 10 nodi e la scotta della velocità massima, poi raffica; reazione dopo 0,3 s, in 1 s, prua girata a mano (non con la barra):
// niente, lascare (+30% di scotta), poggiare 20°, orzare 20°, lascare e poggiare. Sbandamento massimo in 8 s.
// Senza argomenti: gruppo di conferma della terza regola (14,5, 16,5 e 18,5 nodi; 78°/88°/98°/108°/120°/132°; due mure):
//   «poggia» non sbanda mai più di «niente», misurato solo dove «niente» supera 15° (il suggerimento dice di poggiare solo se si sbanda troppo;
//   soglia scelta da Ale e Claude dopo aver visto «conferma2»). Gli altri casi si stampano ma non si giudicano.
// «conferma2»: gruppo di conferma della seconda regola (15, 17 e 19 nodi; 75°/85°/95°/115°/130°; due mure):
//   «poggia» non sbanda mai più di «niente» (regola cambiata da Ale dopo aver visto il primo gruppo di conferma).
// «esplorazione»: il gruppo su cui la prima regola è stata scelta (16 e 20 nodi, 90°/110°).
// «conferma1»: il primo gruppo di conferma (14 e 18 nodi, 80°/100°/125°) con la prima regola, «poggia» almeno 2° meno di «niente»
//   e «orza» non meno di «niente − 1°»: 6 casi su 12 dentro (docs/PROPOSTA-RAFFICHE-PORTANTI.md).
const { step } = require("./motore.js");
const KN = 1.943844, DT = 1 / 120;
function regola(twa){ let best = 0, bs = 0;
  for (let sh = 0; sh <= 1.0001; sh += 0.05){ const S = { x: 0, y: 0, h: twa, u: 2, vl: 0, r: 0, heel: 0, heelRate: 0 };
    for (let t = 0; t < 40; t += DT){ S.h = twa; step(S, { sheet: sh, tiller: 0 }, { twd: 0, tws: 10 / KN }, DT); }
    if (S.u > best){ best = S.u; bs = sh; } }
  return bs; }
function prova(twa, lato, G, dh, lasca, sh0){
  const h0 = lato * twa, S = { x: 0, y: 0, h: h0, u: 2, vl: 0, r: 0, heel: 0, heelRate: 0 };
  for (let t = 0; t < 40; t += DT){ S.h = h0; step(S, { sheet: sh0, tiller: 0 }, { twd: 0, tws: 10 / KN }, DT); }
  let hmax = 0;
  for (let t = 0; t < 8; t += DT){
    const k = Math.min(1, Math.max(0, (t - 0.3) / 1));
    S.h = lato * (twa + dh * k); S.r = 0;
    step(S, { sheet: Math.min(1, sh0 + (lasca ? 0.3 * k : 0)), tiller: 0 }, { twd: 0, tws: G / KN }, DT);
    hmax = Math.max(hmax, S.heel);
  }
  return hmax; }
const gruppo = process.argv[2] || "conferma3", prima = gruppo === "esplorazione" || gruppo === "conferma1", terza = gruppo === "conferma3";
const [raffiche, angoli] = { esplorazione: [[16, 20], [90, 110]], conferma1: [[14, 18], [80, 100, 125]], conferma2: [[15, 17, 19], [75, 85, 95, 115, 130]], conferma3: [[14.5, 16.5, 18.5], [78, 88, 98, 108, 120, 132]] }[gruppo];
let casi = 0, ok = 0;
for (const G of raffiche) for (const twa of angoli) for (const lato of [1, -1]) {
  const sh0 = regola(twa);
  const [n, l, p, o, lp] = [[0, 0], [0, 1], [20, 0], [-20, 0], [20, 1]].map(([dh, la]) => prova(twa, lato, G, dh, la, sh0));
  if (terza && n <= 15){ console.log(`raffica ${G} kn, ${twa}° ${lato > 0 ? "mure a sinistra" : "mure a dritta"}: niente ${n.toFixed(1)}° · poggia ${p.toFixed(1)}°  non giudicato (sbandamento sotto 15°)`); continue; }
  const buono = prima ? p <= n - 2 && o >= n - 1 : p <= n; casi++; if (buono) ok++;
  console.log(`raffica ${G} kn, ${twa}° ${lato > 0 ? "mure a sinistra" : "mure a dritta"} (scotta ${Math.round(sh0 * 100)}): niente ${n.toFixed(1)}° · lasca ${l.toFixed(1)}° · poggia ${p.toFixed(1)}° · orza ${o.toFixed(1)}° · lasca e poggia ${lp.toFixed(1)}°  ${buono ? "OK" : "FUORI SOGLIA"}`);
}
console.log(`casi misurati ${casi}, dentro le soglie ${ok}`);
if (casi === 0 || ok < casi) process.exitCode = 1;
