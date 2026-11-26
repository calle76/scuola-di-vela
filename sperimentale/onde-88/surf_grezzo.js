// Voce 88, prova GREZZA (solo ordine di grandezza): barca M del banco 84 con la forza dell'onda di Harris, Thomas e Renilson (1999, O8)
// a un solo grado di libertà: F = -rho g Vol zeta k sinc(k L/2) sin(k (x - c t)) lungo la direzione delle onde (che vanno sottovento).
// Niente beccheggio, sussulto, resistenza aggiunta, timone, imbardata: la prua è tenuta ferma come nel banco. Onde da SPM 1984 (onde_fetch.py).
// Uso: node surf_grezzo.js   (una misura per volta col freno)
const { motore } = require("../barca-84/banco84.js"), { M } = require("../barca-84/giro6_controlli.js");
const KN = 1.943844, R = Math.PI / 180, g = 9.81, rho = 1025, LWL = 3.38;
const { step } = motore(M), MASS = 160, VOL = MASS / rho;
function corsa(kn, twa, sheet, comps, T = 240){ // comps: [{a, L, ph}] onde (ampiezza m, lunghezza m, fase)
  const S = { x:0, y:0, h:0, u:1, vl:0, r:0 }; const dt = .05; let su = 0, n = 0, xw = 0, maxu = 0;
  const cw = Math.cos((180 - twa) * R); // componente della rotta nella direzione delle onde
  for (let t = 0; t < T; t += dt){
    S.h = 0; step(S, { sheet, tiller: 0 }, { twd: twa, tws: kn / KN }, dt);
    let F = 0;
    for (const c of comps){ const k = 2 * Math.PI / c.L, cel = Math.sqrt(g / k), z = k * LWL * Math.abs(cw) / 2, sinc = z > 1e-6 ? Math.sin(z) / z : 1;
      F += -rho * g * VOL * c.a * k * sinc * Math.sin(k * (xw - cel * t) + c.ph); }
    S.u += F * cw / MASS * dt; xw += S.u * cw * dt;
    if (t > 40){ su += S.u; n++; if (S.u > maxu) maxu = S.u; }
  }
  return { u: su / n * KN, max: maxu * KN };
}
function rnd(seed){ return () => (seed = (seed * 16807) % 2147483647) / 2147483647; }
const best = (kn, twa) => { let b = { u: 0, sh: 0 }; for (let sh = .3; sh <= 1.0001; sh += .05){ const r = corsa(kn, twa, sh, [], 80); if (r.u > b.u) b = { u: r.u, sh }; } return b; };
const casi = [[10, 5, .19, 5.4], [12, 5, .24, 6.3], [15, 2, .20, 4.1], [15, 5, .32, 7.6], [15, 10, .45, 12.0], [20, 5, .45, 9.6]]; // vento, fetch km, Hs, lunghezza (onde_fetch.py)
console.log("vento | fetch | Hs | lungh. | angolo | piatta | regolare (H=Hs) | irregolare (5 onde, 10 semi): media, min-max | punta");
for (const [kn, F, Hs, L] of casi) for (const twa of [180, 150, 135]){
  const b = best(kn, twa), reg = corsa(kn, twa, b.sh, [{ a: Hs / 2, L, ph: 0 }]);
  const irr = []; for (let s = 1; s <= 10; s++){ const r = rnd(s * 7919); const comps = [];
    for (let i = 0; i < 5; i++){ const Li = L * (0.6 + 0.2 * i); comps.push({ a: Hs / 4 * Math.sqrt(2 / 5), L: Li, ph: r() * 2 * Math.PI }); } // 5 componenti uguali: Hs = 4 sigma
    irr.push(corsa(kn, twa, b.sh, comps)); }
  const m = irr.reduce((s, x) => s + x.u, 0) / irr.length, lo = Math.min(...irr.map(x => x.u)), hi = Math.max(...irr.map(x => x.u)), pk = Math.max(...irr.map(x => x.max));
  const p = x => `${x.toFixed(2)} (${x >= b.u ? "+" : ""}${((x / b.u - 1) * 100).toFixed(0)}%)`;
  console.log(`${kn} | ${F} | ${Hs} | ${L} | ${twa} | ${b.u.toFixed(2)} | ${p(reg.u)} | ${p(m)}, ${lo.toFixed(2)}-${hi.toFixed(2)} | ${pk.toFixed(1)}`);
}
