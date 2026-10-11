// Uscita dall'angolo morto con la barca che arretra (0.20.1). Uso: node angolo_morto.js   (circa un minuto)
// 1) Regola del passo 5.4 e del suggerimento: finché la barca arretra, barra a fondo dalla parte del boma; poi barra al centro.
//    Griglia: prua da 0° a 60° dal vento ogni 2°, tutte e due le mure, velocità iniziale da 0 a −2 nodi, vento 6/10/14 nodi,
//    scotta 100 e 50 (ferma). Esce = prua ad almeno 45° dal vento e barca che va avanti, entro 60 s.
// 2) Risposta sbagliata della domanda d'esame 22: barra mossa di continuo da un lato all'altro (tre ritmi), da 0° a 44° dal vento.
// Solo motore (tests/fisica/motore.js), senza raffiche: il collaudo nel gioco vero è in collaudo_suggerimento.py.
const { step } = require("./motore.js");
const KN = 1.944, DT = 1 / 240, T = 60;
const twaOf = S => Math.abs(((0 - S.h) % 360 + 540) % 360 - 180);
const partenze = maxTwa => {
  const out = [];
  for (let twa = 0; twa <= maxTwa; twa += 2) for (const kn of [0, -0.25, -0.5, -1, -1.5, -2]) for (const lato of [1, -1])
    if (twa || lato > 0) out.push({ twa, kn, lato });
  return out;
};
// boomSide non esiste finché step() non ha girato una volta: al primo passo la barra resta al centro (come nella misura della 0.20.1)
const nuova = p => ({ x: 0, y: 0, h: (360 - p.lato * p.twa) % 360, u: p.kn / KN, vl: 0, r: 0, heel: 0, heelRate: 0 });

console.log("1) Barra verso il boma finché la barca arretra, poi al centro");
let tot = 0, esce = 0;
for (const tk of [6, 10, 14]) for (const sh of [1, 0.5]) {
  const tempi = [], fuori = [];
  for (const p of partenze(60)) {
    const S = nuova(p); let arretrata = false, t = null, umin = 0;
    for (let i = 1; i <= T / DT; i++) {
      const indietro = S.u < 0; if (indietro) arretrata = true;
      step(S, { sheet: sh, tiller: indietro ? (S.boomSide || 0) : 0 }, { twd: 0, tws: tk / KN }, DT);
      umin = Math.min(umin, S.u);
      if (t === null && twaOf(S) >= 45 && S.u > 0.05) t = i * DT;
    }
    if (t !== null) { if (arretrata) tempi.push(t); }
    else fuori.push(`${p.lato > 0 ? "dritta" : "sinistra"} ${p.twa}° ${p.kn} kn: finisce a ${twaOf(S).toFixed(0)}° e ${(S.u * KN).toFixed(2)} kn, all'indietro al massimo ${(-umin * KN).toFixed(3)} kn`);
  }
  const n = partenze(60).length; tot += n; esce += n - fuori.length;
  tempi.sort((a, b) => a - b);
  console.log(`${tk} kn, scotta ${sh * 100}: escono ${n - fuori.length} su ${n}; tempo (solo chi ha arretrato) mediana ${tempi[tempi.length >> 1].toFixed(1)} s, massimo ${tempi[tempi.length - 1].toFixed(1)} s`);
  for (const f of fuori) console.log("   non esce: " + f);
}
console.log(`totale: escono ${esce} su ${tot}`);

console.log("\n2) Barra mossa di continuo da un lato all'altro (risposta sbagliata della domanda 22)");
let tot2 = 0, esce2 = 0;
for (const meta of [0.3, 0.5, 1]) {                                    // secondi fra un cambio di lato e l'altro
  let n = 0, e = 0;
  for (const tk of [6, 10, 14]) for (const sh of [1, 0.5]) for (const p of partenze(44)) {
    const S = nuova(p); n++;
    for (let i = 1; i <= T / DT; i++) {
      step(S, { sheet: sh, tiller: Math.sign(Math.sin(Math.PI * i * DT / meta)) }, { twd: 0, tws: tk / KN }, DT);
      if (twaOf(S) >= 45 && S.u > 0.05) { e++; break; }
    }
  }
  tot2 += n; esce2 += e;
  console.log(`cambio di lato ogni ${meta} s: escono ${e} su ${n}`);
}
console.log(`totale: escono ${esce2} su ${tot2}`);
