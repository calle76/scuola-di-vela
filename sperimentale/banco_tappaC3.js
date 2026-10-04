// Tappa C, terzo compito (C3): BANCO DI PROVA per la PROPOSTA. Non è ancora la misura della tappa.
// Legge la fisica da sperimentale/fiocco.html tramite motore_fiocco.js e NON la modifica: i due modelli
// candidati sono calcolati e applicati QUI, fuori dal motore (stessa tecnica di misure_tappaC2.js).
// Uso: node banco_tappaC3.js
const P = require("./motore_fiocco.js");
const KN = 1.943844, B = P.BOAT, D2R = Math.PI / 180, dt = 1 / 240;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const f = (v, n, w) => (v === null ? "—" : v.toFixed(n)).padStart(w);

// ---------------------------------------------------------------------------
// I DUE MODELLI CANDIDATI, EMULATI FUORI DAL MOTORE.
// Tutti e due entrano come VELOCITÀ DI ROTAZIONE (°/s), non come momento: il motore è cinematico.
// Verso: (awa ≥ 0 ? −1 : +1) = via dal vento. È lo stesso verso del termine «la prua scade» già nel
// motore, ed è il verso che misure_tappaC2.txt ha misurato per il solo fiocco (poggiera 12 su 12).
// Il verso è scritto nel codice: è una TARATURA, non una misura.
//
//  A — SENZA MEMORIA: il fiocco cazzato spinge sempre via dal vento, dentro l'angolo morto.
//      rBack = backRate · (aws/AWSRIF)² · (1 − scotta) · (1 − lf)
//  B — CON UN FILO DI MEMORIA: il fiocco segue il boma con ritardo backT; finché è rimasto dal lato
//      vecchio è «a collo» e spinge. Fuori dalla virata il termine vale esattamente zero.
//      rBack = backRate · (aws/AWSRIF)² · (1 − scotta) · (1 − lf) · collo,  collo = max(0, −jibLag·lato)
// lf = fattore di sgonfiamento del motore: 0 sotto 27° apparenti, 1 sopra 34°.
// ---------------------------------------------------------------------------
const AWSRIF = 10 / KN;   // m/s: vento apparente di riferimento, 10 nodi
function rBackDi(info, jib, m, st){
  if (jib === undefined || !m.backRate) return 0;
  const A = Math.abs(info.awa), lato = info.awa >= 0 ? -1 : 1;
  const lf = clamp((A - B.luffA0) / B.luffW, 0, 1);
  const collo = m.modello === "A" ? 1 : Math.max(0, -st.jibLag * lato);
  return m.backRate * (info.aws / AWSRIF) ** 2 * (1 - jib) * (1 - lf) * collo * lato;
}

// un passo = step() del prototipo + il termine emulato, con lo stesso ritardo con cui il motore
// insegue rTarget (S.r += (rTarget − S.r)·min(1, dt·4)).
function corsa(S, C, E, m, passi, pilota, guarda){
  let info = P.step(S, C, E, 0), t = 0;
  const st = S.__st || (S.__st = { rB: 0, jibLag: info.awa >= 0 ? -1 : 1 });
  for (let k = 1; k <= passi; k++){
    if (pilota) pilota(S, C, info, t);
    info = P.step(S, C, E, dt);
    const lato = info.awa >= 0 ? -1 : 1;
    st.jibLag += (lato - st.jibLag) * Math.min(1, dt / m.backT);   // il fiocco segue il boma con ritardo
    st.rB += (rBackDi(info, C.jib, m, st) - st.rB) * Math.min(1, dt * 4);
    S.h = P.norm360(S.h + st.rB * dt);
    t = k * dt;
    if (guarda && guarda(S, C, info, t, st)) return { t, info, st, fine: true };
  }
  return { t, info, st, fine: false };
}

const M0 = { modello: "A", backRate: 0, backT: 1.2 };            // niente modello
const MA = r => ({ modello: "A", backRate: r, backT: 1.2 });
const MB = (r, T = 1.2) => ({ modello: "B", backRate: r, backT: T });

const trim = A => ({
  sheet: clamp((Math.max(B.minBoom, A - 17) - B.minBoom) / (B.maxBoom - B.minBoom), 0, 1),
  jib:   clamp((Math.max(B.minJib,  A - 17) - B.minJib)  / (B.maxJib  - B.minJib),  0, 1)
});
const auto = (S, C, info) => { const A = Math.abs(info.awa), t = trim(A); C.sheet = t.sheet; if (C.jib !== undefined) C.jib = t.jib; };
const vento = { twd: 0, tws: 10 / KN };   // 10 nodi da nord, raffiche spente
const nuovo0 = (h, kn) => ({ x: 0, y: 0, h, u: kn / KN, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.3 });

// ===========================================================================
console.log("=== C3.0 — DOVE VIVE IL TERMINE: QUANTO VALE (1 − lf) ALLE ANDATURE NORMALI ===");
console.log("  (1 − lf) è il fattore con cui il motore sgonfia le vele: 1 sotto 27° apparenti, 0 sopra 34°.");
console.log("  Se non è 0 alle andature normali, il termine del modello A tocca anche chi naviga e basta.");
console.log("  10 nodi, rotta inchiodata, vele regolate da sole, fiocco presente.");
console.log("");
console.log("  reali  nodi   apparente  (1−lf)   modello A a 8 °/s   modello B a 8 °/s");
for (const twa of [40, 42, 45, 48, 50, 55, 60, 90]){
  const S = nuovo0(twa, 1), C = { sheet: 0.5, tiller: 0, jib: 0.5 };
  const r = corsa(S, C, vento, M0, 90 * 240, (s, c, i) => { auto(s, c, i); s.h = twa; }, null);
  const A = Math.abs(r.info.awa), lf = clamp((A - B.luffA0) / B.luffW, 0, 1);
  const a = Math.abs(rBackDi(r.info, trim(A).jib, MA(8), r.st));
  const b = Math.abs(rBackDi(r.info, trim(A).jib, MB(8), { jibLag: r.info.awa >= 0 ? -1 : 1 }));
  console.log(`  ${String(twa).padStart(4)}°  ${f(S.u * KN, 2, 5)}   ${f(A, 1, 7)}°  ${f(1 - lf, 3, 6)}      ${f(a, 2, 5)} °/s           ${f(b, 2, 5)} °/s`);
}

// ===========================================================================
// Virata. Criterio di riuscita indipendente dal modello e identico a quello del collaudo nel browser:
// la prua passa dall'altra parte e arriva a 44° dal vento entro 12 s.
function virata(kn0, twa0, jib, m){
  const S = nuovo0(twa0, kn0), C = { sheet: 0.05, tiller: 0 };
  if (jib !== null) C.jib = jib;
  corsa(S, C, vento, m, 2 * 240, null, null);                      // 2 s di assestamento, barra al centro
  const kn1 = S.u * KN;
  const pilota = (s, c) => { c.tiller = clamp(c.tiller + 1.6 * dt, -1, 1); };  // freccia tenuta premuta
  const r = corsa(S, C, vento, m, 12 * 240, pilota, s => P.norm180(s.h) < -44);
  return { ok: r.fine, t: r.t, kn0: kn1, kn: S.u * KN, h: P.norm180(S.h) };
}
const ANG = [42, 45, 48, 52], VEL = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], SCOTTE = [0.0, 0.35, 1.0];
function griglia(m){
  let ok = 0, tot = 0, somma = 0, peggio = 0; const perScotta = {}, lente = {};
  for (const jb of SCOTTE){
    let o = 0, n = 0, s = 0, ol = 0, nl = 0;
    for (const a of ANG) for (const v of VEL){
      const r = virata(v, a, jb, m);
      n++; tot++; if (v <= 2.0){ nl++; if (r.ok) ol++; }
      if (r.ok){ o++; ok++; s += r.t; somma += r.t; peggio = Math.max(peggio, r.t); }
    }
    perScotta[jb] = { ok: o, n, media: o ? s / o : null }; lente[jb] = { ok: ol, n: nl };
  }
  return { ok, tot, media: ok ? somma / ok : null, peggio, perScotta, lente };
}
const riga = (nome, m) => {
  const g = griglia(m), c = virata(3.5, 45, 0.0, m), l = virata(3.5, 45, 1.0, m);
  const d = r => r.ok ? f(r.t, 2, 5) + " s" : "FALLITA ";
  const lenti = SCOTTE.reduce((a, j) => a + g.lente[j].ok, 0), lentiN = SCOTTE.reduce((a, j) => a + g.lente[j].n, 0);
  console.log(`  ${nome.padEnd(26)} ${d(c)} / ${d(l)}   ${String(g.ok).padStart(3)}/${g.tot}   ${String(lenti).padStart(2)}/${lentiN}   ${f(g.media, 2, 5)} s  ${f(g.peggio, 2, 5)} s`);
  return g;
};

console.log("\n=== C3.1 — LA VIRATA OGGI (nessun modello) ===");
console.log("  10 nodi da nord, raffiche spente, randa cazzata, freccia tenuta premuta a fondo.");
console.log("  Riuscita = la prua passa dall'altra parte e arriva a 44° dal vento entro 12 s.");
console.log("");
for (const [nome, jb] of [["senza fiocco        ", null], ["fiocco cazzato      ", 0.0], ["fiocco a metà       ", 0.35], ["fiocco tutto lascato", 1.0]]){
  const r = virata(3.5, 45, jb, M0);
  console.log(`  partenza di bolina a 45°, 3,5 nodi — ${nome}: partita a ${f(r.kn0, 2, 4)} nodi → ${r.ok ? "riuscita in " + f(r.t, 2, 5) + " s" : "FALLITA (prua a " + Math.round(r.h) + "°)"}`);
}
console.log("");
console.log("  Griglia fissa di 84 casi: 4 andature di partenza (42 45 48 52°) × 7 velocità (1,0…4,0 nodi)");
console.log("  × 3 regolazioni del fiocco (cazzato, a metà, lascato). Nessun caso è casuale.");
console.log("");
console.log("  modello                    45° 3,5 kn: cazz./lasc.   riuscite  di cui ≤2 kn   media  più lenta");
const g0 = riga("nessuno", M0);
for (const jb of SCOTTE){ const p = g0.perScotta[jb]; console.log(`     fiocco a ${f(jb, 2, 4)}: ${p.ok} su ${p.n} (media ${p.media ? f(p.media, 2, 4) + " s" : "—"}), lente ≤2 kn ${g0.lente[jb].ok} su ${g0.lente[jb].n}`); }

console.log("\n=== C3.2 — I DUE MODELLI, A VARI backRate ===");
console.log("  modello                    45° 3,5 kn: cazz./lasc.   riuscite  di cui ≤2 kn   media  più lenta");
for (const r of [4, 8, 12, 16]) riga(`A senza memoria, ${r} °/s`, MA(r));
for (const r of [4, 8, 12, 16, 24]) riga(`B a collo, ${r} °/s`, MB(r));
console.log("");
console.log("  Durata del ricordo (modello B a 12 °/s):");
for (const T of [0.6, 1.2, 2.0, 3.0]) riga(`B 12 °/s, backT ${T} s`, MB(12, T));

// ===========================================================================
console.log("\n=== C3.3 — VIRATA LENTA: IL CASO IN CUI IL FIOCCO A COLLO SERVE DAVVERO ===");
console.log("  Partenza di bolina a 45°, poca velocità. Secondi per arrivare a 44° dal vento dall'altra parte.");
console.log("");
console.log("  nodi di partenza    nessuno    A 8 °/s    B 12 °/s   B 24 °/s");
for (const v of [1.0, 1.5, 2.0, 2.5, 3.0]){
  const c = [M0, MA(8), MB(12), MB(24)].map(m => { const r = virata(v, 45, 0.0, m); return r.ok ? f(r.t, 2, 6) + " s" : "  FALLITA"; });
  console.log(`  ${f(v, 1, 8)} nodi      ${c[0]}   ${c[1]}   ${c[2]}   ${c[3]}`);
}

// ===========================================================================
console.log("\n=== C3.4 — DA FERMI NELL'ANGOLO MORTO, ARRIVANDOCI DA UNA VIRATA FALLITA ===");
console.log("  Si vira partendo a 1,0 nodi (oggi fallisce): la barca si pianta con la prua nel vento.");
console.log("  Misura: angolo dal vento e nodi dopo 20 s dall'inizio della virata, barra lasciata al centro");
console.log("  dopo 6 s. A velocità zero il timone non fa nulla: quello che resta è il fiocco a collo.");
console.log("");
console.log("  modello        fiocco cazzato        fiocco lascato        senza fiocco");
for (const [nome, m] of [["nessuno  ", M0], ["A 8 °/s  ", MA(8)], ["B 12 °/s ", MB(12)], ["B 24 °/s ", MB(24)]]){
  const c = [0.0, 1.0, null].map(jb => {
    const S = nuovo0(45, 1.0), C = { sheet: 0.05, tiller: 0 };
    if (jb !== null) C.jib = jb;
    corsa(S, C, vento, m, 2 * 240, null, null);
    corsa(S, C, vento, m, 20 * 240, (s, c2, i, t) => { c2.tiller = t < 6 ? clamp(c2.tiller + 1.6 * dt, -1, 1) : c2.tiller * Math.exp(-2.5 * dt); }, null);
    return `${f(Math.abs(P.norm180(vento.twd - S.h)), 0, 4)}° a ${f(S.u * KN, 2, 4)} kn`;
  });
  console.log(`  ${nome}      ${c[0]}       ${c[1]}       ${c[2]}`);
}

// ===========================================================================
console.log("\n=== C3.5 — GIOCABILITÀ: BARRA AL CENTRO, 60 s SENZA TOCCARE NULLA ===");
console.log("  È il difetto che ha affossato C2 (3 °/s di scarto). Vele regolate da sole, barra mai toccata.");
console.log("  Rotta dopo 60 s, partendo dalla rotta indicata.");
console.log("");
console.log("  partenza   nessuno   A 8 °/s   A 16 °/s   B 12 °/s   B 24 °/s");
for (const twa0 of [45, 50, 60, 90, 135]){
  const r = [M0, MA(8), MA(16), MB(12), MB(24)].map(m => {
    const S = nuovo0(twa0, 1), C = { sheet: 0.5, tiller: 0, jib: 0.5 };
    corsa(S, C, vento, m, 60 * 240, auto, null);
    return Math.abs(P.norm180(vento.twd - S.h));
  });
  console.log(`  ${String(twa0).padStart(5)}°    ${f(r[0], 1, 5)}°    ${f(r[1], 1, 5)}°    ${f(r[2], 1, 5)}°     ${f(r[3], 1, 5)}°     ${f(r[4], 1, 5)}°`);
}

console.log("\n=== C3.6 — FERMARSI NELL'ANGOLO MORTO (si può ancora?) ===");
console.log("  Si orza a fondo da 3,5 nodi fino a 10° dal vento, poi si molla la barra. Angolo dopo 15 s.");
console.log("  Qui la prua NON attraversa il vento: il fiocco non va a collo e il modello B deve dare zero.");
console.log("");
console.log("  fiocco     nessuno   A 8 °/s   B 12 °/s   B 24 °/s");
for (const [nome, jb] of [["cazzato", 0.0], ["lascato", 1.0], ["assente", null]]){
  const r = [M0, MA(8), MB(12), MB(24)].map(m => {
    const S = nuovo0(45, 3.5), C = { sheet: 0.05, tiller: 0 };
    if (jb !== null) C.jib = jb;
    corsa(S, C, vento, m, 2 * 240, null, null);
    corsa(S, C, vento, m, 20 * 240, (s, c) => { c.tiller = clamp(c.tiller - 1.6 * dt, -1, 1); }, s => Math.abs(P.norm180(s.h)) < 10);
    corsa(S, C, vento, m, 15 * 240, (s, c) => { c.tiller *= Math.exp(-2.5 * dt); }, null);
    return Math.abs(P.norm180(vento.twd - S.h));
  });
  console.log(`  ${nome}    ${f(r[0], 1, 6)}°    ${f(r[1], 1, 6)}°    ${f(r[2], 1, 6)}°     ${f(r[3], 1, 6)}°`);
}

console.log("\n=== C3.7 — IL TERMINE TREMA? (prua che attraversa il vento avanti e indietro) ===");
console.log("  Barca lenta (1,5 nodi) con la prua nel vento e la barra mossa da una parte e dall'altra ogni 8 s:");
console.log("  la prua attraversa il vento più volte. Massimo del termine e cambi di verso in 40 s (modello B).");
console.log("");
console.log("  modello     attraversamenti   massimo   cambi di verso   rotta finale");
for (const [nome, m] of [["B 12 °/s", MB(12)], ["B 24 °/s", MB(24)], ["A 8 °/s ", MA(8)]]){
  const S = nuovo0(0, 1.5), C = { sheet: 0.05, tiller: 0, jib: 0.0 };
  let maxr = 0, cambi = 0, prec = 0, attr = 0, lato0 = null;
  corsa(S, C, vento, m, 40 * 240, (s2, c, i, t) => { c.tiller = (Math.floor(t / 8) % 2 ? -1 : 1) * 0.9; }, (s2, c, i, t, st) => {
    const lato = i.awa >= 0 ? -1 : 1;
    if (lato0 !== null && lato !== lato0) attr++;
    lato0 = lato;
    maxr = Math.max(maxr, Math.abs(st.rB));
    if (Math.sign(st.rB) !== prec && Math.abs(st.rB) > 1){ cambi++; prec = Math.sign(st.rB); }
    return false;
  });
  console.log(`  ${nome}    ${String(attr).padStart(9)}        ${f(maxr, 2, 5)} °/s   ${String(cambi).padStart(8)}       ${f(Math.abs(P.norm180(vento.twd - S.h)), 1, 5)}°`);
}

console.log("\n=== C3.9 — VENTO DIVERSO: il termine cresce col quadrato del vento apparente ===");
console.log("  Virata di bolina a 45° partendo a 3,5 nodi, fiocco cazzato, con 6, 10 e 15 nodi di vento reale.");
console.log("");
console.log("  vento    nessuno    B 12 °/s   B 24 °/s   | lascato, B 12 °/s");
for (const kn of [6, 10, 15]){
  const V = { twd: 0, tws: kn / KN };
  const prova = (jb, m) => {
    const S = nuovo0(45, 3.5), C = { sheet: 0.05, tiller: 0, jib: jb };
    corsa(S, C, V, m, 2 * 240, null, null);
    const r = corsa(S, C, V, m, 12 * 240, (s2, c) => { c.tiller = clamp(c.tiller + 1.6 * dt, -1, 1); }, s2 => P.norm180(s2.h) < -44);
    return r.fine ? f(r.t, 2, 6) + " s" : "  FALLITA";
  };
  console.log(`  ${String(kn).padStart(2)} nodi  ${prova(0, M0)}   ${prova(0, MB(12))}   ${prova(0, MB(24))}   | ${prova(1, MB(12))}`);
}

console.log("\n=== C3.10 — MOLTI TENTATIVI CON SEMI FISSI ===");
console.log("  200 virate per modello. Ogni tentativo scuote la partenza con numeri pseudocasuali di un");
console.log("  generatore con seme dichiarato (seme 20261004, stesso seme per tutti i modelli, quindi le");
console.log("  200 partenze sono LE STESSE): velocità 1,0-4,0 nodi, rotta 40-55°, randa 0-0,25,");
console.log("  fiocco 0-0,15 (cazzato) oppure 0,85-1 (lascato), ritardo 0-0,6 s prima di spingere la barra.");
console.log("");
console.log("  modello      cazzato: riuscite / media    lascato: riuscite / media");
for (const [nome, m] of [["nessuno ", M0], ["A 8 °/s ", MA(8)], ["B 8 °/s ", MB(8)], ["B 12 °/s", MB(12)], ["B 24 °/s", MB(24)]]){
  const col = [true, false].map(cazz => {
    let seme = 20261004, ok = 0, somma = 0;
    const rnd = () => { seme = (seme * 1103515245 + 12345) % 2147483648; return seme / 2147483648; };
    for (let i = 0; i < 200; i++){
      const v = 1 + rnd() * 3, a = 40 + rnd() * 15, sh = rnd() * 0.25, jb = cazz ? rnd() * 0.15 : 0.85 + rnd() * 0.15, rit = rnd() * 0.6;
      const S = nuovo0(a, v), C = { sheet: sh, tiller: 0, jib: jb };
      corsa(S, C, vento, m, 2 * 240, null, null);
      const r = corsa(S, C, vento, m, 12 * 240, (s2, c, i2, t) => { if (t > rit) c.tiller = clamp(c.tiller + 1.6 * dt, -1, 1); }, s2 => P.norm180(s2.h) < -44);
      if (r.fine){ ok++; somma += r.t; }
    }
    return `${String(ok).padStart(3)}/200  ${f(ok ? somma / ok : null, 2, 5)} s`;
  });
  console.log(`  ${nome}     ${col[0]}        ${col[1]}`);
}

console.log("\n=== C3.11 — NON-REGRESSIONE PER COSTRUZIONE ===");
let dmax = 0;
for (const twa of [45, 60, 90, 135]) for (const kn of [6, 10, 15]){
  const E = { twd: 0, tws: kn / KN }, C = { sheet: 0.4, tiller: 0 };
  const A = nuovo0(twa, 1), Bb = nuovo0(twa, 1);
  corsa(A,  { ...C }, E, M0,     60 * 240, (s, c, i) => { auto(s, c, i); s.h = twa; }, null);
  corsa(Bb, { ...C }, E, MB(24), 60 * 240, (s, c, i) => { auto(s, c, i); s.h = twa; }, null);
  dmax = Math.max(dmax, Math.abs(A.u - Bb.u) * KN);
}
console.log(`  barca SENZA scotta del fiocco, nessun modello contro B a 24 °/s: scarto massimo ${dmax.toExponential(1)} nodi su 12 casi`);
console.log("  (il termine è moltiplicato per la presenza del fiocco: senza fiocco vale zero, come in tappa A)");
