// Voce 84: virate del gioco contro le 12 virate misurate di un ILCA 7 (Semb e altri, Appl. Sci. 15 (2025) 8629, CC BY, tab. 2; vento della stazione 9,2 m/s ≈ 18 nodi, raffiche 10,4 m/s).
// Stesse misure della tab. 2: finestra di 10 s centrata sul passaggio prua al vento; entrata/uscita = media dei primi/ultimi 2 s; tempo fino all'80% della velocità
// d'entrata (dall'inizio della finestra, dopo il minimo); velocità media nella finestra. Pilota: timone a fondo (rampa del banco, 1,6/s) fino a 35° oltre il vento, poi tiene 45° con un timone proporzionale.
const { motore } = require("./banco84.js"), KN = 1.943844, C = require("./candidato.json");
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
// giu: gradi più larghi in uscita per tGiu secondi dopo la prua al vento (Semb: «esce un po' più giù, poi risale»)
function virata(P, kn, twa, giu = 0, tGiu = 0, lasca = 0, tLasca = 0){ const { step, BOAT, RUD2_SICURA, norm180 } = motore(P), DT = .01, E = { twd: 0, tws: kn / KN };
  const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  const S = { x:0,y:0,h:-twa,u:1.5,vl:0,r:0 }; let info = { awa: twa };
  for (let t = 0; t < 60; t += DT){ S.h = (360 - twa) % 360; S.r = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); }
  const rec = []; let til = 0, fase = 0, tApex = null;
  for (let t = 0; t < 30; t += DT){ const a = norm180(S.h); // a<0 mure di partenza, poi a>0
    if (t < 6) fase = 0; else if (fase === 0) fase = 1; if (fase === 1 && a > twa + giu - 10) fase = 2;
    const want = fase === 0 ? clamp((a + twa) * .05, -RUD2_SICURA, RUD2_SICURA) : fase === 1 ? -RUD2_SICURA : clamp((a - (twa + (tApex !== null && t - tApex < tGiu ? giu : 0))) * .05, -RUD2_SICURA, RUD2_SICURA); // timone negativo: la prua sale
    til += clamp(want - til, -1.6 * DT, 1.6 * DT);
    info = step(S, { sheet: tApex !== null && t - tApex < tLasca ? Math.max(lasca, sheetFor(info.awa)) : sheetFor(info.awa), tiller: til }, E, DT);
    const a2 = norm180(S.h); if (tApex === null && fase >= 1 && a2 >= 0) tApex = t; rec.push([t, S.u, a2]); }
  const w = rec.filter(r => r[0] >= tApex - 5 && r[0] < tApex + 5), m = (arr) => arr.reduce((s, r) => s + r[1], 0) / arr.length;
  const uin = m(w.filter(r => r[0] < tApex - 3)), uout = m(w.filter(r => r[0] >= tApex + 3)), cin = w.filter(r => r[0] < tApex - 4).reduce((s, r) => s + r[2], 0) / 100, cout = w.filter(r => r[0] >= tApex + 4).reduce((s, r) => s + r[2], 0) / 100;
  let iMin = 0; w.forEach((r, i) => { if (r[1] < w[iMin][1]) iMin = i; }); let t80 = null; for (let i = iMin; i < w.length; i++) if (w[i][1] >= .8 * uin){ t80 = w[i][0] - (tApex - 5); break; }
  return { uin, uout, umean: m(w), umin: w[iMin][1], range: cout - cin, t80 }; }
const MIS = { uin: 2.43, uout: 2.23, umean: 2.08, range: 79.6, t80: 7.59 }; // medie della tab. 2 (12 virate)
console.log(`misura (medie di 12): entrata ${MIS.uin} m/s, uscita ${MIS.uout} (${(MIS.uout/MIS.uin*100).toFixed(0)}%), media ${MIS.umean} (${(MIS.umean/MIS.uin*100).toFixed(0)}%), angolo ${MIS.range}°, 80% dopo ${MIS.t80} s`);
for (const i of [0, 3]) for (const kn of [14, 18]) { const r = virata(C[i].P, kn, 45);
  console.log(`${C[i].n.slice(0, 12)} ${kn} nodi: entrata ${r.uin.toFixed(2)} m/s, uscita ${r.uout.toFixed(2)} (${(r.uout/r.uin*100).toFixed(0)}%), media ${r.umean.toFixed(2)} (${(r.umean/r.uin*100).toFixed(0)}%), minimo ${(r.umin/r.uin*100).toFixed(0)}%, angolo ${r.range.toFixed(0)}°, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); }
// controprova: K con lo smorzamento della resistenza indotta di oggi (0,4 invece di 0,1)
if (process.argv[2] === "reg") for (const reg of [0.1, 0.2, 0.4]) { const P = Object.assign({}, C[3].P, { reg }); const r = virata(P, 18, 45);
  console.log(`K reg ${reg} 18 nodi: entrata ${r.uin.toFixed(2)}, uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); }
if (process.argv[2] === "giu") for (const i of [0, 3]) for (const kn of [14, 18]) for (const [g, tg] of [[0, 0], [10, 3], [15, 4], [20, 5]]) { const r = virata(C[i].P, kn, 45, g, tg);
  console.log(`${C[i].n.slice(0, 12)} ${kn} nodi, uscita +${g}° per ${tg} s: uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, angolo ${r.range.toFixed(0)}°, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); }
if (process.argv[2] === "lasca") for (const i of [0, 3]) for (const [g, tg, l, tl] of [[0, 0, 0, 0], [0, 0, .4, 3], [0, 0, .6, 3], [10, 3, .4, 3], [10, 3, .6, 4], [15, 4, .8, 4]]) { const r = virata(C[i].P, 18, 45, g, tg, l, tl);
  console.log(`${C[i].n.slice(0, 12)} 18 nodi, +${g}° per ${tg} s, scotta ${l} per ${tl} s: uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, angolo ${r.range.toFixed(0)}°, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); }
if (process.argv[2] === "piede") for (const i of [0, 3]) for (const kn of [16, 18, 20]) for (const [g, tg] of [[20, 6], [30, 6], [30, 10], [45, 8]]) { const r = virata(C[i].P, kn, 45, g, tg);
  console.log(`${C[i].n.slice(0, 12)} ${kn} nodi, +${g}° per ${tg} s: uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, 80% dopo ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"}`); }
