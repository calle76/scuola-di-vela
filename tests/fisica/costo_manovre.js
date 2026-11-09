// Secondi persi in una virata e in un'abbattuta dalla barca del gioco (1.2.22, docs/PROPOSTA-ROTTA-OTTIMALE.md §2 C: T_VIR, T_ABB).
// Timoniere semplice: barra proporzionale all'errore di prua (al massimo RUD2_SICURA, 1,6 della corsa al secondo come la tastiera), scotta per l'angolo
// del vento apparente (come virata1b.js). Si confronta il cammino utile (verso il vento in bolina, sottovento in poppa) di 60 s con la manovra a 5 s
// contro 60 s dritti alla stessa andatura. Uso: node costo_manovre.js
const { step, norm180, BOAT, RUD2_SICURA } = require("./motore.js");
const DT = 0.01, K = 1.6, clamp = (v, a, b) => Math.max(a, Math.min(b, v)), D2R = Math.PI / 180;
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
function corsa(kn, twa, manovra){ // twa: angolo dal vento (vento da 0°); manovra: false = dritti
  const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: -twa, u: 2, vl: 0, r: 0, lv: 2 }; let info = { awa: twa }, til = 0;
  const tieni = (h, dt) => { const e = norm180(h - S.h); til += clamp(clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA) - til, -K * dt, K * dt); info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, dt); };
  for (let t = 0; t < 40; t += DT) tieni(-twa, DT); // a regime
  const x0 = S.x, y0 = S.y;
  for (let t = 0; t < 60; t += DT) tieni(manovra && t > 5 ? twa : -twa, DT);
  const dir = twa < 90 ? 0 : 180, ux = Math.sin(dir * D2R), uy = -Math.cos(dir * D2R); // verso il vento o sottovento
  return (S.x - x0) * ux + (S.y - y0) * uy; }
for (const kn of [6, 10, 12, 14]){
  const dB = corsa(kn, 45, false), vB = corsa(kn, 45, true), dP = corsa(kn, 150, false), vP = corsa(kn, 150, true);
  console.log(`${kn} nodi: virata (45°) persi ${((dB - vB) / (dB / 60)).toFixed(1)} s [VMG ${(dB / 60 * 1.944).toFixed(2)} nodi]; abbattuta (150°) persi ${((dP - vP) / (dP / 60)).toFixed(1)} s [VMG ${(dP / 60 * 1.944).toFixed(2)} nodi]`);
}
