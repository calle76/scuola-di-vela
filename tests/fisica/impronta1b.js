// Impronta della barca dell'1b in Node (congelamento, docs/PROPOSTA-CONGELAMENTO-1B.md): step() con S.lv = 2 in un elenco fisso di manovre,
// somma di controllo di tutti gli stati a precisione piena, passo per passo. Il riferimento (impronta1b.txt, accanto) è in git.
// Uso: node impronta1b.js                  confronta col riferimento: uguale al bit, o FALLITO (esce con 1)
//      node impronta1b.js riferimento      riscrive il riferimento (solo per una modifica voluta della barca, dicendolo)
//      node impronta1b.js --cambia RUD2.hullKq=401   contro-prova: una costante cambiata solo in memoria
// Se cambia solo la versione di Node (Math.sin e simili), si confrontano prima i numeri arrotondati dei banchi dell'1b e poi si rigenera, dicendolo.
const M = require("./motore.js"), { step, BOAT, RUD2, RUD2_SICURA, newShift, stepShift } = M;
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const RIF = path.join(__dirname, "impronta1b.txt"), KN = 1.943844, D2R = Math.PI / 180;
const ci = process.argv.indexOf("--cambia");
if (ci > 0){ const [k, v] = process.argv[ci + 1].split("="), [o, c] = k.split("."); M[o][c] = Number(v); console.log(`contro-prova: ${k} = ${v}`); }

const conta = { passi: 0, stallo: 0, boma: 0, scuffie: 0, virate: 0 };
function corsa(nome, S, comandi, vento, secondi, dt = 1 / 60){ // comandi(S, t) e vento(t) danno C ed E a ogni passo
  const h = crypto.createHash("sha256"); let giu = false, lato = null;
  for (let t = 0; t < secondi; t += dt){
    const C = comandi(S, t), o = step(S, C, vento(t), dt);
    h.update([S.x, S.y, S.h, S.u, S.vl, S.r, S.heel, S.heelRate, S.hike, S.boom, S.boomSide, +!!S.stall, +!!S.pushing].join(",") + ";");
    conta.passi++; if (S.stall) conta.stallo++; if (S.pushing) conta.boma++;
    const su = S.heel > BOAT.capsizeAt; if (su && !giu) conta.scuffie++; giu = su;
    const l = Math.sign(o.twa); if (lato !== null && l !== lato && Math.abs(o.twa) < 90) conta.virate++; lato = l;
  }
  return `${nome}: ${h.digest("hex").slice(0, 16)}`;
}
const barca = (h, u) => ({ x: 0, y: 0, h, u, vl: 0, r: 0, lv: 2 });
const fisso = (kn, twd = 0) => () => ({ twd, tws: kn / KN });
const pilota = (rotta, lim = RUD2_SICURA) => S => Math.max(-lim, Math.min(lim, 0.04 * (((S.h - rotta + 540) % 360) - 180) + 0.02 * S.r));
let rnd = 1; const caso = () => { rnd = (rnd * 16807) % 2147483647; return rnd / 2147483647; }; // numeri fissi per i salti di vento

const righe = [];
for (const kn of [6, 10, 16]) for (const [twa, sh] of [[45, 0.05], [90, 0.4], [150, 0.95]]) // andature, barra al centro: conta anche la barca orziera
  righe.push(corsa(`andatura ${kn} nodi ${twa}°`, barca(360 - twa, 1.5), () => ({ sheet: sh, tiller: 0 }), fisso(kn), 30));
for (const kn of [6, 10, 16]) for (const [nome, lim] of [["freccia", RUD2_SICURA], ["Maiusc", 1]]){ // virata: bolina tenuta 15 s, poi barra fino a 30° oltre il vento
  let fase = 0;
  righe.push(corsa(`virata ${kn} nodi ${nome}`, barca(315, 2), (S, t) => {
    if (t < 15) return { sheet: 0.05, tiller: pilota(315)(S) };
    const a = ((S.h + 540) % 360) - 180; if (fase === 0 && a > 30) fase = 1;
    return { sheet: 0.05, tiller: fase ? pilota(45)(S) : -lim };
  }, fisso(kn), 30));
}
for (const kn of [10, 16]) righe.push(corsa(`strambata ${kn} nodi`, barca(200, 2), (S, t) => ({ sheet: t < 10 ? 0.95 : 0.5, tiller: t < 10 ? pilota(200)(S) : pilota(150, 1)(S) }), fisso(kn), 25));
for (const [g, l] of [[18, false], [18, true], [24, false]]) // raffica di bolina da 10 nodi, senza reagire o lascando; 24 nodi fa scuffiare
  righe.push(corsa(`raffica 10→${g} nodi${l ? " lascando" : ""}`, barca(315, 2), (S, t) => ({ sheet: l && t > 20.5 ? 0.5 : 0.1, tiller: pilota(315)(S) }), t => ({ twd: 0, tws: (t < 20 ? 10 : g) / KN }), 26));
righe.push(corsa("boma spinto 10 nodi", barca(315, 2), (S, t) => ({ sheet: 0.05, tiller: t < 10 ? pilota(315)(S) : 0, push: t >= 10 && t < 16 }), fisso(10), 20));
righe.push(corsa("ferma nel vento 10 nodi", barca(5, 0), () => ({ sheet: 0.5, tiller: 0 }), fisso(10), 15));
righe.push(corsa("indietro 10 nodi", barca(0, -0.5), () => ({ sheet: 1, tiller: 0.5 }), fisso(10), 10));
for (const tipo of ["osc", "pers"]){ // salti di vento: il pilota tiene la bolina sul vento che gira
  const st = newShift(tipo, caso); let twd = 0;
  righe.push(corsa(`salti ${tipo} 10 nodi`, barca(315, 2), S => ({ sheet: 0.05, tiller: pilota((twd + 315) % 360)(S) }), () => { twd = stepShift(st, 1 / 60, caso); return { twd, tws: 10 / KN }; }, 120));
}
const riass = `misurato: ${righe.length} corse, ${conta.passi} passi, stallo della pala ${conta.stallo} passi, boma spinto ${conta.boma} passi, scuffie ${conta.scuffie}, cambi di mure ${conta.virate}`;
const testo = righe.join("\n") + "\n";
console.log(riass);
const pochi = !(conta.stallo > 0 && conta.boma > 0 && conta.scuffie > 0 && conta.virate > 0);
if (pochi){ console.log("FALLITO: ha misurato poco (servono stallo, boma spinto, scuffia e cambi di mure)"); process.exit(1); }
if (process.argv[2] === "riferimento"){ fs.writeFileSync(RIF, testo); console.log("riferimento scritto:", RIF); process.exit(0); }
const rif = fs.existsSync(RIF) ? fs.readFileSync(RIF, "utf8") : "";
const a = rif.split("\n"), b = testo.split("\n"), diverse = b.filter((r, i) => r !== a[i]);
for (const r of diverse) console.log("  DIVERSA:", r.split(":")[0]);
console.log(diverse.length ? `ESITO: FALLITO (${diverse.length} corse diverse su ${righe.length})` : `ESITO: OK (${righe.length} corse identiche al riferimento)`);
process.exit(diverse.length ? 1 : 0);
