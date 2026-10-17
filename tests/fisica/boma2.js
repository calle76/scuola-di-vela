// «Spingi il boma» nel livello 2 (1.0.26, docs/PROPOSTA-SPINGI-BOMA.md): criteri B1-B5 della proposta sul motore.
// Venti 6, 10 e 15 nodi; barca ferma con la prua da −30° a +30° dal vento ogni 5° (il boma è dalla parte dove lo mette il vento).
// Uso: node boma2.js      esce con 1 se un criterio è fuori soglia o se ha misurato zero casi.
const { step, norm180 } = require("./motore.js");
const VENTI = [6, 10, 15], PRUE = []; for (let h = -30; h <= 30; h += 5) PRUE.push(h);
const ferma = (kn, h0) => { const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: h0, u: 0, vl: 0, r: 0, lv: 2 }; step(S, { sheet: 1, tiller: 0 }, E, 0); return { S, E }; };

// uscita dall'angolo morto: barra verso il boma (col boma spinto o no) finché la prua è a 50° dal vento, poi barra al centro e boma mollato
function esci(kn, h0, boma){
  const { S, E } = ferma(kn, h0), lato = S.boomSide;
  for (let t = 0; t < 30; t += 0.01){
    const a = norm180(E.twd - S.h);
    if (Math.abs(a) >= 50) return { t, verso: Math.sign(a) === -lato, lato };
    step(S, { sheet: 1, tiller: lato, push: boma }, E, 0.01);
    if (S.heel < -45 || S.heel > 60) return { scuffia: true, lato };
  }
  return { t: null, lato };
}
function indietro(kn, h0){ // Z tenuto 3 s, barra al centro: la barca va all'indietro?
  const { S, E } = ferma(kn, h0); let umin = 0;
  for (let t = 0; t < 3; t += 0.01){ step(S, { sheet: 1, tiller: 0, push: true }, E, 0.01); umin = Math.min(umin, S.u); }
  return umin;
}
function freno(kn, boma){ // dalla bolina a regime, barra al centro: scotta tutta lascata oppure boma spinto
  const E = { twd: 0, tws: kn / 1.944 }, S = { x: 0, y: 0, h: 45, u: 1.5, vl: 0, r: 0, lv: 2 };
  for (let t = 0; t < 40; t += 0.01){ S.h = 45; step(S, { sheet: 0.1, tiller: 0 }, E, 0.01); }
  const u0 = S.u; let t1 = null, hmin = 0, hmax = 0;
  for (let t = 0; t < 20 && t1 === null; t += 0.01){
    step(S, { sheet: 1, tiller: 0, push: boma }, E, 0.01); hmin = Math.min(hmin, S.heel); hmax = Math.max(hmax, S.heel);
    if (S.u < 1 / 1.944) t1 = t;
  }
  return { u0, t1, hmin, hmax, prua: norm180(E.twd - S.h), cap: S.heel < -45 || S.heel > 60 };
}
function tieni(kn){ // prua nel vento, Z tenuto 6 s, barra al centro
  const { S, E } = ferma(kn, 0); let hmin = 0, umin = 0;
  for (let t = 0; t < 6; t += 0.01){ step(S, { sheet: 1, tiller: 0, push: true }, E, 0.01); hmin = Math.min(hmin, S.heel); umin = Math.min(umin, S.u); if (S.heel < -45 || S.heel > 60) return { cap: true, hmin }; }
  return { cap: false, hmin, umin, prua: norm180(E.twd - S.h) };
}

let tutti = true, n1 = 0, ok1 = 0, n2 = 0, ok2 = 0, n3 = 0, ok3 = 0;
const rapporti = [];
for (const kn of VENTI){
  const righe = [];
  for (const h0 of PRUE){
    const b = esci(kn, h0, true), s = esci(kn, h0, false);
    n1++; if (b.t !== null && b.verso && !b.scuffia) ok1++;
    n2++; if (b.t !== null && (s.t === null || b.t < s.t)) ok2++;
    if (b.t !== null && s.t !== null) rapporti.push(s.t / b.t);
    n3++; if (indietro(kn, h0) < 0) ok3++;
    righe.push(`${h0}°: ${b.t === null ? "no" : b.t.toFixed(1)}/${s.t === null ? "no" : s.t.toFixed(1)}`);
  }
  console.log(`${kn} nodi, uscita col boma spinto / con la sola barra (s): ${righe.join("  ")}`);
}
rapporti.sort((a, b) => a - b);
const med = rapporti.length ? rapporti[Math.floor(rapporti.length / 2)] : 0;
const B1 = n1 > 0 && ok1 === n1, B2 = n2 > 0 && ok2 === n2 && med >= 1.5, B3 = n3 > 0 && ok3 === n3;
console.log(`B1 ${B1 ? "ok   " : "FUORI"} la prua gira verso il boma ed esce: ${ok1} casi su ${n1}`);
console.log(`B2 ${B2 ? "ok   " : "FUORI"} col boma spinto si esce prima che con la sola barra: ${ok2} casi su ${n2}; rapporto mediano ${med.toFixed(2)} (almeno 1,5)`);
console.log(`B3 ${B3 ? "ok   " : "FUORI"} col boma spinto e la barra al centro la barca va all'indietro entro 3 s: ${ok3} casi su ${n3}`);
tutti = B1 && B2 && B3;
for (const kn of VENTI){
  const l = freno(kn, false), z = freno(kn, true), ok = z.t1 !== null && (l.t1 === null || z.t1 < l.t1) && !z.cap;
  console.log(`B4 ${ok ? "ok   " : "FUORI"} freno con ${kn} nodi (entrata ${(l.u0 * 1.944).toFixed(1)} nodi): sotto 1 nodo col boma spinto in ${z.t1 === null ? "mai" : z.t1.toFixed(1) + " s"}, lascando tutto in ${l.t1 === null ? "più di 20 s" : l.t1.toFixed(1) + " s"}; col boma sbandamento ${z.hmin.toFixed(0)}..${z.hmax.toFixed(0)}°, prua a ${z.prua.toFixed(0)}° dal vento${z.cap ? ", SCUFFIA" : ""}`);
  tutti = tutti && ok;
}
for (const kn of VENTI){
  const r = tieni(kn), ok = kn === 15 || !r.cap;
  console.log(`B5 ${ok ? "ok   " : "FUORI"} prua nel vento, Z tenuto 6 s con ${kn} nodi: ${r.cap ? "SCUFFIA" : `nessuna scuffia, sbandamento minimo ${r.hmin.toFixed(0)}°, all'indietro fino a ${(-r.umin * 1.944).toFixed(1)} nodi, prua a ${r.prua.toFixed(0)}° dal vento`}${kn === 15 ? " (con 15 nodi solo riportato)" : ""}`);
  tutti = tutti && ok;
}
console.log(tutti ? "ESITO: tutti i criteri nelle soglie" : "ESITO: almeno un criterio FUORI soglia");
process.exit(tutti ? 0 : 1);
