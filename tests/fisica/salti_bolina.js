// Salti di vento e bolina (misura per docs/PROPOSTA-SALTI-VENTO.md, 17 ottobre 2026; non è un controllo di non-regressione).
// Barca del livello 2 guidata da un pilota verso una boa D metri sopravento; vento medio da nord, 10 nodi, direzione A·sin(2πt/P + φ).
// Due strategie con le stesse regole per lay line e bordi del campo:
//   «due bordi»: ignora i salti, vira solo sulla lay line (col vento di quel momento) o sul bordo del campo;
//   «sui salti»: in più vira quando è scarso di oltre 5° rispetto al vento medio (che il velista conosce: lo ha osservato prima della partenza).
// Il guadagno è la differenza dei tempi medi su 24 fasi del salto. Limite noto: il pilota non riconosce un salto persistente
// (periodo più lungo della bolina) e lì vira a vuoto; i casi con periodo maggiore della bolina vanno letti con questo limite.
// Uso: node salti_bolina.js [D metri] ['[[A,P],...]']
const { step, norm180 } = require("./motore.js");

function bolina(kn, D, A, P, phi, strat, thr = 5, dt = 0.02){
  const S = { x: 0, y: 0, h: 45, u: 0, vl: 0, r: 0, lv: 2 }, twdAt = t => A * Math.sin(2 * Math.PI * t / P + phi);
  let twd = twdAt(0), lastTack = -99, ntack = 0, tacking = false;
  let tack = Math.abs(norm180(twd + 45)) < Math.abs(norm180(twd - 45)) ? 1 : -1; // +1: prua a twd+45 (mure a sinistra); parte sulle mure più vicine alla boa
  S.h = twd + 45 * tack; S.u = 2.0;
  for (let t = 0; t < 900; t += dt){
    twd = twdAt(t);
    const bx = -S.x, by = -D - S.y;
    if (Math.hypot(bx, by) < 5 || (S.y <= -D && Math.abs(S.x) < 15)) return { t, ntack }; // all'altezza della boa, a meno di 15 m
    const brg = Math.atan2(bx, -by) / (Math.PI / 180);
    const layOther = Math.abs(norm180(brg - twd)) >= 45 && Math.sign(norm180(brg - twd)) === -tack; // boa raggiungibile sulle altre mure
    let want = tack;
    if (!tacking){
      if (layOther && t - lastTack > 3) want = -tack;
      else if (strat === "salti"){
        const scarso = tack * twd > thr; // mure +1: il vento che gira in senso orario porta la prua lontano dalla boa
        const nuovaFuori = Math.sign(Math.sin((twd - 45 * tack) * Math.PI / 180)) === Math.sign(S.x) && Math.abs(S.x) > 0.4 * D;
        if (scarso && !nuovaFuori && t - lastTack > 8) want = -tack;
      }
      const versoFuori = Math.sign(Math.sin((twd + 45 * tack) * Math.PI / 180)) === Math.sign(S.x); // campo largo mezza bolina per lato
      if (Math.abs(S.x) > 0.5 * D && versoFuori && t - lastTack > 3) want = -tack;
    }
    if (want !== tack){ tack = want; tacking = true; lastTack = t; ntack++; }
    const err = norm180(twd + 45 * tack - S.h);
    if (tacking && Math.abs(err) < 8) tacking = false;
    const lim = tacking ? 35 / 45 : 1; // in virata la sola freccia (35°)
    step(S, { sheet: 0.1, tiller: Math.max(-lim, Math.min(lim, -err / 20 + S.r * 0.02)) }, { twd, tws: 10 / 1.944 }, dt);
  }
  return { t: null, ntack };
}

const N = 24, fasi = [...Array(N)].map((_, i) => i * 2 * Math.PI / N);
function media(D, A, P, s){
  const v = fasi.map(p => bolina(10, D, A, P, p, s)), ok = v.filter(r => r.t !== null);
  return { t: ok.reduce((a, r) => a + r.t, 0) / ok.length, n: ok.reduce((a, r) => a + r.ntack, 0) / ok.length, fall: v.length - ok.length };
}
const D = +process.argv[2] || 140;
const casi = process.argv[3] ? JSON.parse(process.argv[3]) : [[10, 30], [10, 60], [10, 120], [10, 240], [15, 30], [15, 60], [15, 120], [15, 240], [15, 600]];
for (const [A, P] of casi){
  const d = media(D, A, P, "dritto"), s = media(D, A, P, "salti");
  console.log(`bolina ${D} m, salti ±${A}° ogni ${P} s: due bordi ${d.t.toFixed(1)} s (${d.n.toFixed(1)} virate, fallite ${d.fall}) | sui salti ${s.t.toFixed(1)} s (${s.n.toFixed(1)} virate, fallite ${s.fall}) | guadagno ${(d.t - s.t).toFixed(1)} s (${((d.t - s.t) / d.t * 100).toFixed(0)}%)`);
}
