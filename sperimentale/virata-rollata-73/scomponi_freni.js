// Voce 73: con la prua imposta come in F109 (vedi prua_imposta.js), quanto pesa ogni forza fra −15 e +15 s: spinta della vela (positiva o negativa),
// scafo (con l'aumento per lo sbandamento), resistenza indotta. In newton·secondo (impulso) e in metri al secondo di velocità persa (impulso / massa).
const { step, BOAT, hullDrag } = require("../../tests/fisica/motore.js");
const DT = 0.01, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v)), D2R = Math.PI / 180;
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
for (const [kn, T] of [[3.2, 10], [11, 5]]){
  const prua = t => t <= -T / 2 ? -45 : t >= T / 2 ? 45 : -45 * Math.cos(Math.PI * (t + T / 2) / T);
  const S = { x: 0, y: 0, h: -45, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 };
  const I = { velaPiu: 0, velaMeno: 0, scafo: 0, indotta: 0 }, Ib = { velaPiu: 0, velaMeno: 0, scafo: 0, indotta: 0 }; let tMorto = 0;
  for (let i = 0; i < 7500; i++){ const t = i * DT - 60;
    const h = t < -15 ? -45 : prua(t); S.r = (prua(t + DT) - h) / DT; S.h = (h + 360) % 360;
    const u = S.u, heel = S.heel || 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); S.h = (h + 360) % 360;
    const scafo = hullDrag(u) * (1 + Math.pow(Math.abs(heel) / 30, 2) * 0.6);
    const ind = info.side * info.side * u * Math.abs(u) / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE * BOAT.TE * (u * u + 0.4) ** 2);
    const J = t < 0 ? I : Ib;
    if (t >= -15){ if (info.drive > 0) J.velaPiu += info.drive * DT; else J.velaMeno += info.drive * DT; J.scafo -= scafo * DT; J.indotta -= ind * DT; if (Math.abs(info.awa) < BOAT.luffA0 + BOAT.luffW) tMorto += DT; } }
  // contro il dritto: la stessa corsa senza virare
  const R = { x: 0, y: 0, h: 315, u: 1, vl: 0, r: 0, lv: 2 }; let ri = { awa: 45 }; const I0 = { velaPiu: 0, velaMeno: 0, scafo: 0, indotta: 0 };
  for (let i = 0; i < 7500; i++){ const t = i * DT - 60; const u = R.u, heel = R.heel || 0; ri = step(R, { sheet: sheetFor(ri.awa), tiller: 0 }, E, DT); R.h = 315; R.r = 0;
    if (t >= -15){ I0.velaPiu += Math.max(0, ri.drive) * DT; I0.scafo -= hullDrag(u) * (1 + Math.pow(Math.abs(heel) / 30, 2) * 0.6) * DT;
      I0.indotta -= ri.side * ri.side * u * Math.abs(u) / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE * BOAT.TE * (u * u + 0.4) ** 2) * DT; } }
  const f = x => x.toFixed(0);
  console.log(`${kn} nodi, virata in ${T} s (vela nell'angolo morto per ${tMorto.toFixed(1)} s). Impulsi in N·s, da −15 a +15 s; tra parentesi il dritto:`);
  console.log(`  vela che spinge ${f(I.velaPiu + Ib.velaPiu)} (${f(I0.velaPiu)}), vela che frena ${f(I.velaMeno + Ib.velaMeno)}, scafo ${f(I.scafo + Ib.scafo)} (${f(I0.scafo)}), indotta ${f(I.indotta + Ib.indotta)} (${f(I0.indotta)})`);
  console.log(`  prima del vento: vela +${f(I.velaPiu)} / ${f(I.velaMeno)}, scafo ${f(I.scafo)}, indotta ${f(I.indotta)}; dopo: vela +${f(Ib.velaPiu)} / ${f(Ib.velaMeno)}, scafo ${f(Ib.scafo)}, indotta ${f(Ib.indotta)}`);
}
