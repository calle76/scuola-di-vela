// Voce 84, quinto giro §6 (GIRO5.md): cose mai provate, solo misura. (1) virata con la scotta automatica «sicura» del gioco (gioco.js autoSheet(true):
// boma = max(boma minimo, vento apparente − 17°) + 1,5° per grado di sbandamento oltre 12°), pilota di virate_semb.js; (2) strambata con 10/15/20 nodi.
const { motore } = require("./banco84.js"), C = require("./candidato.json"), { L } = require("./giro5.js"), KN = 1.943844;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
function virataAuto(P, kn, twa = 45){ const { step, BOAT, RUD2_SICURA, norm180 } = motore(P), DT = .01, E = { twd: 0, tws: kn / KN };
  const sheetAuto = (awa, heel) => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) + 1.5 * Math.max(0, Math.abs(heel || 0) - 12) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  const S = { x:0,y:0,h:360 - twa,u:1.5,vl:0,r:0 }; let info = { awa: twa };
  for (let t = 0; t < 60; t += DT){ S.h = 360 - twa; S.r = 0; info = step(S, { sheet: sheetAuto(info.awa, S.heel), tiller: 0 }, E, DT); }
  const u0 = S.u; let til = 0, fase = 0, tA = null, umin = 9, hm = 0, uFine = 0;
  for (let t = 0; t < 25; t += DT){ const a = norm180(S.h); if (t >= 2 && fase === 0) fase = 1; if (fase === 1 && a > twa - 10) fase = 2;
    const want = fase === 0 ? clamp((a + twa) * .05, -RUD2_SICURA, RUD2_SICURA) : fase === 1 ? -RUD2_SICURA : clamp((a - twa) * .05, -RUD2_SICURA, RUD2_SICURA);
    til += clamp(want - til, -1.6 * DT, 1.6 * DT); info = step(S, { sheet: sheetAuto(info.awa, S.heel), tiller: til }, E, DT);
    if (tA === null && fase >= 1 && norm180(S.h) >= 0) tA = t; if (tA !== null){ umin = Math.min(umin, S.u); hm = Math.max(hm, Math.abs(S.heel)); } if (t > 22) uFine = S.u; }
  return `minimo ${(umin / u0 * 100).toFixed(0)}%, sbandamento max ${hm.toFixed(0)}°, dopo 20 s ${(uFine / u0 * 100).toFixed(0)}%`; }
function strambata(P, kn, twa = 150){ const { step, BOAT, RUD2_SICURA, norm180 } = motore(P), DT = .01, E = { twd: 0, tws: kn / KN };
  const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  const S = { x:0,y:0,h:360 - twa,u:2,vl:0,r:0 }; let info = { awa: twa };
  for (let t = 0; t < 60; t += DT){ S.h = 360 - twa; S.r = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); }
  const u0 = S.u; let til = 0, fase = 0, umin = 9, hm = 0, scuffia = false, cambio = null, uFine = 0;
  for (let t = 0; t < 25; t += DT){ const a = norm180(S.h); // a = −twa all'inizio (mure a dritta), si poggia verso −180 e oltre, fino a +twa
    const aa = a < 0 ? a : a - 360; if (t >= 2 && fase === 0) fase = 1; if (fase === 1 && aa < -(360 - twa) + 10) fase = 2;
    const want = fase === 0 ? 0 : fase === 1 ? RUD2_SICURA * .5 : clamp((a - twa) * .05, -RUD2_SICURA, RUD2_SICURA);
    til += clamp(want - til, -1.6 * DT, 1.6 * DT); info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT);
    if (t > 2){ umin = Math.min(umin, S.u); hm = Math.max(hm, Math.abs(S.heel)); if (Math.abs(S.heel) > BOAT.capsizeAt) scuffia = true; if (cambio === null && fase === 2) cambio = t - 2; } if (t > 22) uFine = S.u; }
  return `giro ${cambio === null ? "non finito" : cambio.toFixed(1) + " s"}, minimo ${(umin / u0 * 100).toFixed(0)}%, sbandamento max ${hm.toFixed(0)}°${scuffia ? " SCUFFIA" : ""}, dopo 20 s ${(uFine / u0 * 100).toFixed(0)}%`; }
for (const [n, P] of [["oggi", C[0].P], ["K", C[3].P], ["L", L]]){ console.log("## " + n);
  for (const kn of [14, 18]) console.log(`  virata con la scotta automatica sicura, ${kn} nodi: ${virataAuto(P, kn)}`);
  for (const kn of [10, 15, 20]) console.log(`  strambata 150°→150°, ${kn} nodi: ${strambata(P, kn)}`); }
