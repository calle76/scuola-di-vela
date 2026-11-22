// Voce 73: velocità istante per istante nella virata con la prua imposta (come prua_imposta.js), accanto a F109 fig. 4.12 letta a occhio (virata piatta).
const { step, BOAT } = require("../../tests/fisica/motore.js");
const allinea = S => S.u > 0.05 ? Math.max(-1, Math.min(1, -Math.atan2(S.r * Math.PI / 180 * 1.9, S.u) * 180 / Math.PI / 45)) : 0; // timone allineato all'acqua che arriva (RUD2.xR = 1,9 m): niente freno finto della pala che ruota
const DT = 0.01, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
const VERI = { 3.2: { "-5": 1.05, "-2.5": 1.02, "0": 0.95, "2.5": 0.76, "5": 0.75, "10": 0.85, "15": 0.88 }, 11: { "-5": 2.35, "-2.5": 2.33, "0": 2.0, "2.5": 1.25, "5": 1.75, "10": 2.1, "15": 2.2 } };
for (const [kn, T] of [[3.2, 10], [11, 5]]){
  const prua = t => t <= -T / 2 ? -45 : t >= T / 2 ? 45 : -45 * Math.cos(Math.PI * (t + T / 2) / T);
  const S = { x: 0, y: 0, h: 315, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }; const righe = [];
  for (let i = 0; i <= 7500; i++){ const t = Math.round((i * DT - 60) * 100) / 100, h = t < -15 ? -45 : prua(t);
    if (VERI[kn][String(t)] !== undefined) righe.push(`t ${String(t).padStart(4)} s: prua ${h.toFixed(0).padStart(3)}°, gioco ${S.u.toFixed(2)} m/s (apparente ${Math.abs(info.awa).toFixed(0)}°, spinta ${info.drive ? info.drive.toFixed(1) : "—"} N, scarroccio ${(Math.atan2(S.vl, S.u) * 57.3).toFixed(0)}°), F109 ${VERI[kn][String(t)]}`);
    S.r = (prua(t + DT) - h) / DT; S.h = (h + 360) % 360; info = step(S, { sheet: sheetFor(info.awa), tiller: allinea(S) }, E, DT); S.h = (h + 360) % 360; }
  console.log(`${kn} nodi, virata in ${T} s:\n  ` + righe.join("\n  ")); }
