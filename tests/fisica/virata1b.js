// Virata della barca dell'1b col gesto da tastiera (docs/PROPOSTA-VIRATA-1B.md, 1.0.43): barra a 1,6 della corsa al secondo fino a 35°
// (sola freccia) o 45° (Maiusc), al centro quando la prua è 30° oltre il vento. Durata fino a quel punto, velocità minima rispetto
// all'entrata, prua più larga dopo (V1). Barca lenta: 1,5 nodi al traverso, gradi girati in 3 s.
// Uso: node virata1b.js            misura con le costanti del motore
//      node virata1b.js griglia    sceglie hullKq (venti 10 e 14) e lo conferma (6, 8, 12, 16) con la regola della proposta
const { step, norm180, BOAT, RUD2, RUD2_SICURA } = require("./motore.js");
const DT = 0.01, K = 1.6, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
function vira(kn, bar){ const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: -45, u: 1.5, vl: 0, r: 0, lv: 2 }; let info = { awa: 45 };
  for (let t = 0; t < 40; t += DT){ S.h = -45; S.r = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); }
  const u0 = S.u; let umin = u0, tf = null, til = 0, pk = 0;
  for (let t = 0; t < 20; t += DT){ const a = norm180(E.twd - S.h);
    if (tf === null && a < -30) tf = t; if (tf !== null) pk = Math.min(pk, a);
    til += clamp((tf !== null ? 0 : -bar) - til, -K * DT, K * DT);
    info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT); if (tf === null) umin = Math.min(umin, S.u); }
  return { t: tf, m: umin / u0, pk: -pk }; }
function lenta(bar){ const E = { twd: 0, tws: 10 / 1.944 }, S = { x: 0, y: 0, h: -90, u: 1.5 / 1.944, vl: 0, r: 0, lv: 2 }; let info = { awa: 90 }, til = 0;
  for (let t = 0; t < 3; t += DT){ til += clamp(bar - til, -K * DT, K * DT); info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT); }
  return Math.abs(norm180(S.h + 90)); }
// criterio 1 della proposta (freccia): 2,5-3,5 s con 8-16 nodi, al massimo 4,5 s con 6; minima 35-60%; V1: prua non oltre 60°
const ok = (kn, a) => a.t !== null && (kn <= 6 ? a.t <= 4.5 : a.t >= 2.5 && a.t <= 3.5) && a.m >= 0.35 && a.m <= 0.6 && a.pk <= 60;
const f = (x, d = 1) => x === null ? "mai" : x.toFixed(d);
function tabella(venti){ let tutti = true;
  for (const kn of venti){ const a = vira(kn, RUD2_SICURA), b = vira(kn, 1), c = ok(kn, a); tutti = tutti && c;
    console.log(`  ${String(kn).padStart(2)} nodi  freccia ${f(a.t)} s, minima ${Math.round(a.m * 100)}%, prua fino a ${f(a.pk, 0)}°  |  Maiusc ${f(b.t)} s, ${Math.round(b.m * 100)}%, ${f(b.pk, 0)}°  |  criterio 1: ${c ? "ok" : "FUORI"}`); }
  console.log(`  barca lenta (1,5 nodi, 3 s): freccia ${f(lenta(RUD2_SICURA), 0)}°, Maiusc ${f(lenta(1), 0)}°`); return tutti; }
if (process.argv[2] === "griglia"){
  // regola fissata prima: il valore più basso di hullKq (barca più agile) con il criterio 1 ok a 10 e 14 nodi; poi conferma sugli altri venti
  const base = RUD2.hullKq; let scelto = null;
  for (const q of [600, 500, 400, 300, 250, 200, 150, 100]){ RUD2.hullKq = q; const a = [10, 14].every(kn => ok(kn, vira(kn, RUD2_SICURA)));
    console.log(`hullKq ${q}: venti di scelta ${a ? "ok" : "fuori"}  (10 nodi ${f(vira(10, RUD2_SICURA).t)} s, 14 nodi ${f(vira(14, RUD2_SICURA).t)} s)`); if (a) scelto = q; }
  RUD2.hullKq = scelto; console.log(`\nscelto hullKq ${scelto}; conferma sui venti mai usati per la scelta:`); const c = tabella([6, 8, 12, 16]);
  console.log(`conferma: ${c ? "OK" : "FUORI"}`); RUD2.hullKq = base;
} else { console.log(`hullKq ${RUD2.hullKq}, yawG ${RUD2.yawG}`); tabella([6, 8, 10, 12, 14, 16]); }
