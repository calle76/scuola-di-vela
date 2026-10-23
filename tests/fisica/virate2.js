// Virate del livello 2 (docs/archivio/PROPOSTA-VIRATE-AVVERSARI.md, 1.0.31): quanto la prua va oltre la bolina dopo la virata.
// Giocatore (sola freccia fino a 35°, poi spazio a 20° o 35° oltre il vento, con e senza barra contro), uscita lenta da 0,3 a 1,0 m/s,
// avversari (la guida di regate.js), oscillazione di rotta del pilota in bolina. Solo misura, nessuna soglia: i criteri sono nella proposta.
const { step, norm180, BOAT, RUD2_SICURA } = require("./motore.js");
const DT = 0.01, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
function bolina(kn){ const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: 45, u: 1.5, vl: 0, r: 0, lv: 2 };
  for (let t = 0; t < 40; t += DT){ S.h = 45; step(S, { sheet: 0.1, tiller: 0 }, E, DT); } return { S, E }; }
function giocatore(kn, cen, contro){ const { S, E } = bolina(kn); let b = 0, fase = 0, a0, pk = -999, tS = null, tc, info = { awa: 45 };
  for (let t = 0; t < 25; t += DT){ const a = norm180(E.twd - S.h);
    if (fase === 0){ b = Math.min(RUD2_SICURA, b + 1.6 * DT); if (a > cen){ fase = 1; tc = t; a0 = a; b = 0; } }
    else if (contro && fase === 1){ b = -RUD2_SICURA; if (S.r >= 0){ fase = 2; b = 0; } } else b = 0;
    info = step(S, { sheet: fase ? sheetFor(info.awa) : 0.1, tiller: b }, E, DT);
    if (fase){ pk = Math.max(pk, a); if (tS === null && Math.abs(S.r) < 2) tS = t - tc; } }
  return { pk, ov: pk - a0, tS };
}
// uscita lenta: barca a velocità u0 con la prua 20° oltre il vento che gira a r0 °/s verso la mura nuova, barra al centro (o contro)
function lenta(u0, r0, contro){ const E = { twd: 0, tws: 10 / 1.944 }, S = { x: 0, y: 0, h: -20, u: u0, vl: 0, r: -r0, lv: 2 }; let pk = 20, info = { awa: 30 }, b = contro ? -RUD2_SICURA : 0;
  for (let t = 0; t < 15; t += DT){ if (S.r >= 0) b = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: b }, E, DT); pk = Math.max(pk, norm180(E.twd - S.h)); }
  return pk; }
function avv(kn, ai){ const { S, E } = bolina(kn); S.h = ai.up; let tl = 0, info = { awa: 45 }, pk = 0;
  for (let t = 0; t < 25; t += DT){ const a = norm180(E.twd - S.h);
    tl += (clamp(norm180(S.h + ai.up) / ai.gain + S.r * 0.02, -1, 1) * (S.u < 0 ? -1 : 1) - tl) * Math.min(1, DT * ai.react);
    info = step(S, { sheet: sheetFor(info.awa), tiller: tl }, E, DT); if (a > 0) pk = Math.max(pk, a); }
  return pk; }
// pilota in bolina: oscillazione di rotta (scarto quadratico, gradi) con disturbi di ±4°/s ogni 2 s, guida di tillerFor dell'esperto
function oscill(kn){ const { S, E } = bolina(kn); let tl = 0, s2 = 0, n = 0, seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let t = 0; t < 60; t += DT){ if (Math.abs(t % 2) < DT) S.r += (rnd() * 2 - 1) * 4;
    tl += (clamp(norm180(S.h - 45) / 18 + S.r * 0.02, -1, 1) - tl) * Math.min(1, DT * 5); step(S, { sheet: 0.1, tiller: tl }, E, DT);
    if (t > 10){ s2 += norm180(S.h - 45) ** 2; n++; } } return Math.sqrt(s2 / n); }
const f = x => x === null ? "—" : x.toFixed(1);
const R = [];
for (const kn of [6, 10, 14]) for (const cen of [20, 35]) { const g = giocatore(kn, cen, false), c = giocatore(kn, cen, true); R.push(`${kn}n c${cen}: max ${f(g.pk)} sovra ${f(g.ov)} stop ${f(g.tS)}s contro ${f(c.pk)} (${f(g.pk - c.pk)} meglio)`); }
console.log(R.join("\n"));
console.log("uscita lenta (r0 25°/s), u m/s: max senza / con barra contro: " + [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.8, 1.0].map(u => `${u}:${f(lenta(u, 25, false))}/${f(lenta(u, 25, true))}`).join("  "));
console.log("avversari princ/esperto: " + [6, 10, 14].map(kn => `${kn}n ${f(avv(kn, { up: 51, gain: 26, react: 3 }))}/${f(avv(kn, { up: 46, gain: 18, react: 5 }))}`).join("  "));
console.log("oscillazione pilota in bolina (gradi): " + [6, 10, 14].map(kn => `${kn}n ${f(oscill(kn))}`).join("  "));
