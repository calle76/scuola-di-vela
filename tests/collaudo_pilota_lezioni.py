# Pilota completo delle lezioni (proposta: docs/PROPOSTA-PILOTA-LEZIONI.md, rivista in chat e accettata il 16 ottobre 2026).
# Per ogni lezione, dall'inizio e nell'ordine, come un giocatore (si passa da un passo all'altro con «Avanti», mai con showStep,
# salvo il salto forzato quando un passo non si completa, dichiarato nel rapporto). In ogni passo pratico:
#   1) «a mani ferme»: 30 s simulati senza tasti; se il passo si completa, è un passo che si completa da solo;
#   2) «guidando»: il pilota fa quello che dice il testo, entro il tempo limite del passo.
# Ogni lezione si percorre due volte per seme: con il pilota preciso e con il giocatore impreciso, che tiene ogni tasto
# da 0,3 a 1,5 s più del necessario («colpo lungo»), anche dopo che il passo si è completato (se ne accorge un attimo dopo): la misura «a mani ferme» di questa seconda corsa è «dopo un colpo lungo».
# Il pilota legge solo quello che il giocatore vede a schermo: angolo dal vento (lancetta della rosetta nelle lezioni 1 e 2, con
# errore di lettura ±5°; rosa e «Andatura» dalla lezione 3, errore ±3°), velocità, filetti, sbandamento, boma, la raffica sull'acqua,
# la boa, la rotta scritta nel suggerimento, il testo di fine passo. Non legge le condizioni dei passi in index.html.
# A passi fissi di 1/60 s (__sv.run), ciclo del browser fermo, Math.random del gioco a seme fisso; il pilota ha un suo generatore.
# Uso: python collaudo_pilota_lezioni.py [--semi 1-20] [--solo 123456] [--pagina file.html] [--veloce] [--reale]
#      --veloce = semi 1-3; --reale = solo la prova senza #collaudo (lezione 2, passi 2 e 3, in tempo reale, 3 tentativi)
import asyncio, json, pathlib, statistics, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "output" / "pilota_lezioni"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();
window.requestAnimationFrame = () => 0;"""

# Tabella dei passi, scritta PRIMA di lanciare il pilota (16 ottobre 2026). Chiave: «lezione:titolo del passo».
# lim = secondi simulati di guida dopo i 30 s a mani ferme. aspetta = il testo chiede anche di aspettare (dichiarato prima:
# se il passo si completa a mani ferme si riporta comunque, con questa nota).
PASSI = r"""
const PASSI = {
  "1:Poggiare":                      { lim: 40,  f: C => tieni(C, poggiaK(), () => twaV(C) >= 150) },               // «rilascia quando il vento arriva quasi da dietro»
  "1:Orzare e l'angolo morto":       { lim: 60,  f: C => tieni(C, orzaK(), () => twaV(C) < 40) },                    // 1.0.12: «quando la lancetta della rosa entra nel rosso, rilascia»
  "1:Ripartire":                     { lim: 40,  f: C => poi(tieni(C, poggiaK(), () => twaV(C) >= 90), guida(C, { twa: 90, resta: true })) }, // «finché il vento arriva di fianco e la barca riparte. Se giri troppo, correggi con l'altra freccia» (messa a punto, semi 1-3)
  "1:La scotta: lascare":            { lim: 30,  f: C => tieni(C, lascaK(), () => sh() >= 0.995) },                  // «apri la vela del tutto»
  "1:La scotta: cazzare":            { lim: 40,  f: C => colpiScotta(C, "ok") },                                     // «poco alla volta, finché smette di sbattere»
  "1:Troppo cazzata":                { lim: 40,  f: C => tieni(C, cazzaK(), () => sh() <= 0.005) },                  // «fino a chiudere del tutto la vela»
  "2:Barra a sinistra":              { lim: 20,  f: C => tieniPer(C, "ArrowLeft", 1.5) },                            // «sposta la barra verso sinistra e guarda»
  "2:Barra a dritta":                { lim: 20,  f: C => tieniPer(C, "ArrowRight", 1.5) },
  "2:Barra sottovento: si orza":     { lim: 60,  f: C => guida(C, { twa: 57, colpi: true, centra: true }) },          // 1.0.14: «a un terzo della strada tra il rosso e l'orizzontale»
  "2:Barra sopravento: si poggia":   { lim: 60,  f: C => guida(C, { twa: 120, colpi: true, centra: true }) },         // «scesa un terzo della strada tra l'orizzontale e il basso»
  "2:Tenere la rotta":               { lim: 90,  f: C => rotta(C) },                                                // «entro 6° per 8 s, piccoli colpi»
  "3:Bolina":                        { lim: 60,  f: C => guida(C, { twa: 58, centra: true }) },                       // settore tratteggiato 45-75
  "3:Traverso":                      { lim: 60,  f: C => guida(C, { twa: 90, centra: true }) },
  "3:Lasco e gran lasco":            { lim: 60,  f: C => guida(C, { twa: 150, centra: true }) },
  "3:Poppa":                         { lim: 60,  f: C => guida(C, { twa: 174, colpi: true, centra: true }) },         // «piano, finché il vento arriva esattamente da dietro»
  "3:Filetto sopravento":            { lim: 40,  f: C => tieni(C, lascaK(), stabile(() => tt() === "wind")) },   // (stabile: messa a punto, semi 1-3)
  "3:Filetti dritti":                { lim: 40,  f: C => colpiScotta(C, "ok") },
  "3:Filetto sottovento":            { lim: 40,  f: C => colpiScotta(C, "lee") },
  "3:Poggi e laschi":                { lim: 60,  f: C => guida(C, { twa: 122, centra: true, regola: true }) },
  "3:Orzi e cazzi":                  { lim: 60,  f: C => guida(C, { twa: 58, centra: true, regola: true }) },
  "4:Da fermi":                      { lim: 60,  aspetta: true, f: C => tieni(C, lascaK(), () => sh() >= 0.995) },  // «lasca tutta la vela e aspetta»
  "4:Accelerando":                   { lim: 60,  f: C => colpiScotta(C, "ok") },                                     // «cazza finché è regolata e lascia accelerare» (riprese: messa a punto, semi 1-3)
  "4:In poppa":                      { lim: 60,  f: C => guida(C, { twa: 172, centra: true, regola: true }) },
  "5:Prepararsi a virare":           { lim: 60,  aspetta: true, f: C => guida(C, { twa: 58, centra: true, regola: true, resta: true }) }, // «lascia che arrivi ad almeno 3,3 nodi»
  "5:Virare":                        { lim: 40,  f: C => virare(C) },
  "5:Una virata che non riesce":     { lim: 120, f: C => nonRiesce(C) },
  "5:Risalire il vento":             { lim: 180, f: C => bordeggia(C) },
  "5:Strambata violenta":            { lim: 60,  f: C => strambaAperta(C) },
  "5:Strambata controllata":         { lim: 90,  f: C => strambaBene(C) },
  "6:Assorbire una raffica":         { lim: 120, aspetta: true, f: C => raffica(C) },                                // «aspetta una raffica»
  "6:La scuffia":                    { lim: 90,  f: C => scuffia(C) },
  "6:Raddrizzare":                   { lim: 30,  f: C => premi(C, "a") },
};"""

PILOTA = r"""
(() => {
const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
let T = 0;                                                                // orologio del collaudo (secondi simulati): __sv.simTime si può scrivere ma non leggere
let ps = 1; const rnd = () => { ps = (Math.imul(ps, 1664525) + 1013904223) >>> 0; return ps / 4294967296; };   // generatore del pilota, separato da quello del gioco
const giu = new Set();
const key = (k, on) => { if (on && !giu.has(k)){ giu.add(k); dispatchEvent(new KeyboardEvent("keydown", { key: k })); }
                         else if (!on && giu.has(k)){ giu.delete(k); dispatchEvent(new KeyboardEvent("keyup", { key: k })); } };
const suTutti = () => [...giu].forEach(k => key(k, false));
const $ = id => document.getElementById(id);
// ---- cosa vede il giocatore ----
const lato = () => n180(sv.S.h - sv.twd) >= 0 ? 1 : -1;                 // da che parte del vento sta la prua
const twaV = C => Math.max(0, Math.min(180, Math.abs(n180(sv.twd - sv.S.h)) + C.bias));   // angolo letto, con l'errore di lettura
const kn = () => sv.readI().kn, tt = () => sv.readI().tt, sh = () => sv.readI().sheet, heel = () => sv.S.heel;
const semVisibili = () => !$("sem").hidden;
const cazzaK = () => semVisibili() ? "w" : "ArrowUp", lascaK = () => semVisibili() ? "s" : "ArrowDown";
// poggiare = allontanare la prua dal vento. Barra a sinistra (←) fa girare la prua a dritta quando la barca va avanti
const poggiaK = () => ((lato() > 0) !== (sv.S.u < 0)) ? "ArrowLeft" : "ArrowRight";
const orzaK = () => poggiaK() === "ArrowLeft" ? "ArrowRight" : "ArrowLeft";
const versoBomaK = () => sv.S.boomSide < 0 ? "ArrowLeft" : "ArrowRight";   // il boma è visibile: barra verso il boma
const centra = () => { key(" ", true); key(" ", false); };
// ---- azioni (generatori: ogni yield è il tempo, in secondi, prima della decisione successiva) ----
function* tieni(C, k, finche, max = 60){                                // «tieni premuto … finché …»
  key(k, true); let t = 0;
  while (!finche() && t < max){ yield C.rt; t += C.rt; }
  if (C.imp) yield C.extra;                                               // il colpo lungo del giocatore impreciso
  key(k, false);
}
// uno stato visto «davvero»: vero per almeno sec secondi di fila (un giocatore non reagisce a un filetto che si muove per un fotogramma)
const stabile = (fn, sec = 0.5) => { let t0 = null; return () => { if (fn()){ if (t0 === null) t0 = T; return T - t0 >= sec; } t0 = null; return false; }; };
function* poi(...g){ for (const x of g) yield* x; }                       // azioni in fila
function* tieniPer(C, k, sec){ key(k, true); yield sec + (C.imp ? C.extra : 0); key(k, false); }
function* premi(C, k){ key(k, true); yield 0.1; key(k, false); }
function* colpiScotta(C, voluto){                                         // piccoli colpi di scotta guardando i filetti
  const visto = stabile(() => voluto === "ok" ? tt() === "ok" : tt() === "lee");
  let attesa = 0;
  for (let n = 0; n < 400; n++){
    if (visto()){                                                         // filetti come voluto: si aspetta; se dopo 6 s il passo non è fatto,
      yield C.rt; attesa += C.rt;                                         // un altro piccolo colpo di cazza (al massimo 3 riprese, contate)
      if (attesa > 6 && C.riprese < 3){ C.riprese++; attesa = 0; key(cazzaK(), true); yield 0.25 + (C.imp ? C.extra : 0); key(cazzaK(), false); }
      continue;
    }
    attesa = 0;
    const s = tt();
    if (voluto === "ok" && s === "ok"){ yield C.rt; continue; }           // dritti ma non ancora da mezzo secondo
    const k = (s === "lee" && voluto === "ok") ? lascaK() : cazzaK();     // sbatte: cazza; sottovento quando li si vuole dritti: lasca
    key(k, true); yield 0.25 + (C.imp ? C.extra : 0); key(k, false); yield 0.6;
  }
}
function* regolaUnaVolta(C){                                             // un colpo di scotta se i filetti lo chiedono
  const s = tt();
  if (s === "wind"){ key(cazzaK(), true); yield 0.2 + (C.imp ? C.extra : 0); key(cazzaK(), false); }
  else if (s === "lee" && sh() < 0.99){ key(lascaK(), true); yield 0.2 + (C.imp ? C.extra : 0); key(lascaK(), false); }
}
// timone tenendo premuto, con anticipo: rilascia quando la prua, alla velocità con cui gira, arriverà entro tol (come fa chi timona);
// ferma nell'angolo morto, prima poggia per uscirne (messa a punto sui semi 1-20: senza anticipo il pilota oscillava fino a 40 °/s)
function sterza(C, Hd, tol){
  if (twaV(C) < 40 && kn() < 1){ const k = poggiaK(); key(k === "ArrowLeft" ? "ArrowRight" : "ArrowLeft", false); key(k, true); return false; }
  const err = n180(Hd - sv.S.h), prev = err - sv.S.r * 0.6;
  if (Math.abs(prev) <= tol){ key("ArrowLeft", false); key("ArrowRight", false); return Math.abs(err) <= tol + 2; }
  const k = (prev > 0) !== (sv.S.u < 0) ? "ArrowLeft" : "ArrowRight";
  key(k === "ArrowLeft" ? "ArrowRight" : "ArrowLeft", false); key(k, true); return false;
}
const prua = (C, twa) => sv.twd + lato() * Math.max(0, Math.min(180, twa - C.bias));   // prua che, letta con l'errore, dà l'angolo voluto
// guida verso un angolo dal vento sulla stessa mura: tenendo premuto, o a piccoli colpi; poi centra; se il passo non si completa
// dopo 4 s di attesa, rilegge (nuovo errore di lettura) e riprova, al massimo 3 volte
function* guida(C, o){
  const tol = o.colpi ? 3 : 4;
  for (let n = 0; n < 2000; n++){
    const err = o.twa - twaV(C);                                          // >0: va poggiato
    if (Math.abs(err) > tol){
      const k = err > 0 ? poggiaK() : orzaK();
      if (o.colpi){                                                       // piccoli colpi, con anticipo: niente colpo se la prua sta già arrivando (messa a punto, seme 15)
        const e = n180(prua(C, o.twa) - sv.S.h), p = e - sv.S.r * 0.6;
        if (Math.abs(p) <= tol){ suTutti(); yield 0.5; continue; }
        const kc = (p > 0) !== (sv.S.u < 0) ? "ArrowLeft" : "ArrowRight";
        key(kc, true); yield 0.3 + (C.imp ? C.extra : 0); key(kc, false); yield 0.5; }
      else { if (sterza(C, prua(C, o.twa), tol)){ if (C.imp){ key(k, true); yield C.extra; key(k, false); } if (o.centra) centra(); } yield C.rt; }
    } else {
      suTutti(); if (o.centra && Math.abs(sv.readI().tiller) > 0.05) centra();
      if (o.regola) yield* regolaUnaVolta(C);
      yield C.rt; C.fermo += C.rt;
      if (!o.resta && C.fermo > 4 && C.riprese < 3){ C.riprese++; C.fermo = 0; C.bias = (rnd() * 2 - 1) * C.err; }
      continue;
    }
    if (o.regola) yield* regolaUnaVolta(C);
  }
}
function* rotta(C){                                                      // come collaudo_rotta.py: piccoli colpi, senza insistere se la prua rientra
  for (let n = 0; n < 5000; n++){
    if (twaV(C) < 40 && kn() < 1){ sterza(C, sv.S.h, 0); yield C.rt; continue; }   // fermo nell'angolo morto (dopo l'attesa): prima esce poggiando
    suTutti();
    const off = n180(sv.S.h - sv.S.course);                               // la rotta è scritta nel suggerimento; >0: prua troppo a dritta
    if (Math.abs(off) > 2 && !(off * sv.S.r < 0 && Math.abs(sv.S.r) > 3)){
      const k = off > 0 ? "ArrowRight" : "ArrowLeft";                     // barra a dritta: la prua va a sinistra
      key(k, true); yield 0.13 + (C.imp ? C.extra : 0); key(k, false); yield 0.07;
    } else yield 0.2;
  }
}
function* virare(C){                                                     // «barra sottovento con decisione, finché sei in bolina dall'altra parte; poi centra»
  if (kn() < 3){                                                          // «si vira sempre con la barca lanciata» (passo prima): se dopo l'attesa la barca è lenta,
    const g = guida(C, { twa: 58, centra: true, regola: true, resta: true }); let t = 0;   // prima riprende velocità in bolina (messa a punto, seme 3)
    for (const w of g){ yield w; t += w; if (kn() >= 3.3 || t > 25) break; }
    suTutti();
  }
  const l0 = lato(), k = versoBomaK();
  yield* tieni(C, k, () => lato() !== l0 && twaV(C) >= 50, 30);
  centra();
}
function* nonRiesce(C){                                                  // lezione 5, passo 4
  yield* tieni(C, lascaK(), () => sh() >= 0.995 || kn() < 1, 25);       // lasca finché la barca scende sotto 1 nodo
  if (kn() >= 1) yield* guida(C, { twa: 58, centra: true, resta: true, max: 1 });   // non rallenta: orza fino alla bolina, vela lasca
}
// (la guida qui sopra non finisce da sola: nonRiesce la interrompe dopo 15 s)
function* nonRiesceTutto(C){
  const g = nonRiesce(C); let t = 0;
  for (const w of g){ yield w; t += w; if (kn() < 1 || t > 40) break; }
  suTutti();
  const l0 = lato(); key(versoBomaK(), true); let t2 = 0;               // prova a virare: barra sottovento
  while (sv.S.u > -0.05 && t2 < 20){ yield C.rt; t2 += C.rt; }
  key("ArrowLeft", false); key("ArrowRight", false);
  t2 = 0;                                                                // arretra: barra verso il boma, finché la prua è fuori dall'angolo morto
  while (twaV(C) < 45 && t2 < 40){ key(versoBomaK(), true); yield C.rt; t2 += C.rt; }
  if (C.imp) yield C.extra;
  suTutti(); centra();
  yield* colpiScotta(C, "ok");                                          // centra e cazza: la barca riparte
}
function* bordeggia(C){                                                  // «a zig-zag: bolina, virata, bolina sull'altra mura»
  let side = lato();
  for (let n = 0; n < 5000; n++){
    const g = sv.goal(); if (!g) { suTutti(); yield 0.5; continue; }
    const brg = Math.atan2(g.x - sv.S.x, -(g.y - sv.S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg;
    if (Math.abs(rel) < 52){ if (Math.abs(rel) > 14) side = rel > 0 ? 1 : -1; want = sv.twd + side * 52; }
    sterza(C, want, 4);
    yield* regolaUnaVolta(C);
    yield C.rt;
  }
}
function* strambaAperta(C){                                              // «poggia con la vela tutta aperta finché il vento passa dall'altro lato»
  const l0 = lato(), k = poggiaK();
  yield* tieni(C, k, () => lato() !== l0, 40);
  centra();
}
function* strambaBene(C){                                                // «in poppa cazza fino a 45°, poggia finché il vento passa, poi lasca e regola»
  const g = guida(C, { twa: 170, centra: true, resta: true }); let t = 0;
  for (const w of g){ yield w; t += w; if (twaV(C) >= 166 || t > 30) break; }
  suTutti();
  yield* tieni(C, cazzaK(), () => sv.S.boom <= 43, 20);                  // «boma a 45° o meno» (valore sotto il cursore)
  const l0 = lato(), k = poggiaK();
  yield* tieni(C, k, () => lato() !== l0, 30);
  centra();
  yield* guida(C, { twa: 125, centra: true, regola: true, resta: true }); // «lasca e regola: i filetti tornano dritti quando orzi fino al lasco»
}
function* raffica(C){                                                    // «di bolina, vela regolata; in raffica lasca un poco»
  for (let n = 0; n < 5000; n++){
    sterza(C, prua(C, 55), 4);
    if (heel() > 15){ key(lascaK(), true); yield 0.25 + (C.imp ? C.extra : 0); key(lascaK(), false); }
    else if (heel() < 10 && tt() === "wind"){ key(cazzaK(), true); yield 0.2; key(cazzaK(), false); }
    yield C.rt;
  }
}
function* scuffia(C){                                                    // «vela tutta cazzata, e in raffica non lascare»
  yield* tieni(C, cazzaK(), () => sh() <= 0.005, 15);
  for (let n = 0; n < 5000; n++){
    sterza(C, prua(C, 50), 4);
    yield C.rt;
  }
}
""" + PASSI + r"""
PASSI["5:Una virata che non riesce"].f = C => nonRiesceTutto(C);
// ---- una corsa: una lezione dall'inizio, con il pilota preciso o con il giocatore impreciso ----
window.__corsa = (li, imp, semeGioco, semePilota) => {
  ps = semePilota >>> 0 || 1; suTutti();
  sv.fast(0); sv.simTime = 0; __seed(semeGioco);
  sv.openItem(["l", li]);
  const out = [], err = li < 2 ? 5 : 3;                                   // errore di lettura: lancetta della rosetta (1-2), rosa e Andatura (3-6)
  T = 0;
  let traccia = null;                                                      // window.__traccia = "1:Ripartire": stato ogni 0,5 s in quel passo (per capire i casi strani)
  const corri = sec => { const n = Math.max(1, Math.round(sec * 60)); for (let k = 0; k < n; k++){ sv.run(1 / 60, 1); T += 1 / 60;
    if (traccia && Math.round(T * 60) % 30 === 0){ const I = sv.readI(); traccia.push([+T.toFixed(1), Math.round(n180(sv.twd - sv.S.h)), +I.kn.toFixed(1), I.tt, +I.sheet.toFixed(2), +I.tiller.toFixed(2), Math.round(sv.S.heel), +sv.S.r.toFixed(1), [...giu].join("+")]); }
    if (sv.stepDone) return true; } return sv.stepDone; };
  for (let passo = 0; passo < 40; passo++){
    const titolo = $("lTitle").textContent, finale = !$("lQuiz").hidden, nx = $("lNext");
    if (finale) break;
    const pratico = nx.hidden || nx.classList.contains("pending");         // con una condizione: «Avanti» compare solo a passo completato
    if (!pratico){ nx.click(); continue; }
    const voce = PASSI[(li + 1) + ":" + titolo];
    const r = { passo: (li + 1) + "." + (passo + 1), titolo, noto: !!voce, aspetta: !!(voce && voce.aspetta) };
    traccia = window.__traccia === (li + 1) + ":" + titolo ? (r.traccia = []) : null;
    // 1) a mani ferme
    suTutti(); const t0 = T; r.mani = corri(30); r.tMani = r.mani ? +(T - t0).toFixed(2) : null;
    { const I = sv.readI(); r.dopoAttesa = { twa: Math.round(I.twa), kn: +I.kn.toFixed(1), tt: I.tt }; }   // come si trova la barca dopo i 30 s (osservazione 45)
    // 2) guidando
    r.guida = r.mani; r.tGuida = null; r.riprese = 0; r.forzato = false;
    if (!r.mani && voce){
      const C = { imp, rt: 0.1 + rnd() * 0.3, extra: 0.3 + rnd() * 1.2, err, bias: (rnd() * 2 - 1) * err, riprese: 0, fermo: 0 };
      const t1 = T, g = voce.f(C);
      let fatto = false, finito = false;
      while (!fatto && T - t1 < voce.lim){
        let w = 0.1;
        if (!finito){ const x = g.next(); if (x.done){ finito = true; suTutti(); } else w = x.value; }
        fatto = corri(Math.max(1 / 60, Math.min(w, voce.lim - (T - t1))));
      }
      // il giocatore impreciso si accorge del passo completato un attimo dopo: tiene i tasti ancora C.extra secondi (osservazione 49)
      if (imp && fatto && giu.size){ const n = Math.round(C.extra * 60); for (let k = 0; k < n; k++){ sv.run(1 / 60, 1); T += 1 / 60; } }
      suTutti(); r.guida = sv.stepDone; r.tGuida = r.guida ? +(T - t1).toFixed(2) : null; r.riprese = C.riprese;
    }
    const S = sv.S, I = sv.readI();
    r.fine = { twa: Math.round(I.twa), kn: +I.kn.toFixed(1), tt: I.tt, heel: Math.round(S.heel), cap: S.capsized };
    out.push(r);
    if (sv.stepDone && !nx.hidden && !nx.classList.contains("pending")) nx.click();
    else { r.forzato = true; suTutti(); sv.showStep(passo + 1); }          // salto forzato: il passo dopo non parte dallo stato giusto
  }
  suTutti();
  return out;
};
})();
"""

async def corse(pagina, semi, lezioni):
    url = pathlib.Path(pagina).resolve().as_uri() + "#collaudo"
    ris, errs = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for s in semi:
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(SEME); await pg.goto(url); await pg.wait_for_timeout(200)
            await pg.evaluate(PILOTA)
            for li in lezioni:
                for imp in (False, True):
                    r = await pg.evaluate("a => __corsa(...a)", [li, imp, s * 1000 + li, s * 7919 + li * 31 + (1 if imp else 0)])
                    for x in r: x.update(seme=s, imp=imp)
                    ris += r
            await ctx.close()
        await b.close()
    return ris, errs

def rapporto(ris, nome):
    passi = []
    for x in ris:
        if x["passo"] not in [p[0] for p in passi]: passi.append((x["passo"], x["titolo"]))
    righe, problemi = [], []
    for k, tit in passi:
        P = [x for x in ris if x["passo"] == k and not x["imp"]]; M = [x for x in ris if x["passo"] == k and x["imp"]]
        g = sum(x["guida"] and not x["mani"] for x in P); gm = sum(x["mani"] for x in P); cl = sum(x["mani"] for x in M)
        tg = [x["tGuida"] for x in P if x["tGuida"] is not None]; rip = sum(x["riprese"] for x in P)
        forz = sum(x["forzato"] for x in P); nonNoto = any(not x["noto"] for x in P)
        guidabili = len(P) - gm
        nota = (" [il testo chiede anche di aspettare]" if any(x["aspetta"] for x in P) else "") + (" [PASSO NON IN TABELLA]" if nonNoto else "")
        righe.append(f"  {k:5s} {tit[:30]:30s} guidando {g:3d}/{guidabili:<3d} t.med {statistics.median(tg) if tg else float('nan'):6.1f}s riprese {rip:3d} | "
                     f"a mani ferme {gm:3d}/{len(P):<3d} | dopo un colpo lungo {cl:3d}/{len(M):<3d}{nota}")
        if g < guidabili: problemi.append(f"{k} {tit}: guidando non completato {guidabili - g} volte su {guidabili}")
        if gm: problemi.append(f"{k} {tit}: si completa a mani ferme {gm} volte su {len(P)}")
        if cl: problemi.append(f"{k} {tit}: già fatto dopo un colpo lungo {cl} volte su {len(M)}")
    print(f"\n=== {nome}: {len(passi)} passi pratici, {len(set(x['seme'] for x in ris))} semi ===")
    print("\n".join(righe))
    return passi, problemi

async def reale(n=3):
    # Pagina senza #collaudo, come la carica un giocatore: lezione 2, «Barra a sinistra» e «Barra a dritta», tastiera vera, tempo reale.
    # Superata = entrambi i passi completati in 3 tentativi su 3 (criterio scritto prima, sezione 5 della proposta).
    url = (ROOT / "index.html").as_uri(); ok = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for t in range(n):
            pg = await b.new_page(viewport={"width": 1360, "height": 768}); await pg.goto(url); await pg.wait_for_timeout(600)
            await pg.click("button.item[data-k='1']"); await pg.wait_for_timeout(300)
            fatti = []
            for i, tasto in enumerate(("ArrowLeft", "ArrowRight")):
                await pg.click("#lNext"); await pg.wait_for_timeout(300); await pg.click("#c")
                await pg.keyboard.down(tasto)
                fatto = False
                for _ in range(50):
                    await pg.wait_for_timeout(100)
                    if await pg.evaluate("(() => { const f = document.getElementById('lFeedback'); return !f.hidden && !f.classList.contains('pending') })()"): fatto = True; break
                await pg.keyboard.up(tasto); await pg.wait_for_timeout(300)
                fatti.append(fatto)
            hook = await pg.evaluate("typeof window.__sv")
            print(f"  tentativo {t + 1}: barra a sinistra {fatti[0]}, barra a dritta {fatti[1]}, __sv {hook}", flush=True)
            ok += all(fatti) and hook == "undefined"
            await pg.close()
        await b.close()
    print(f"senza #collaudo: {ok} tentativi su {n} con entrambi i passi completati (superata se {n} su {n})")
    return ok == n

async def main():
    a = sys.argv[1:]
    if "--reale" in a: sys.exit(0 if await reale() else 1)
    semi = range(1, 4) if "--veloce" in a else range(1, 21)
    if "--semi" in a: x, y = a[a.index("--semi") + 1].split("-"); semi = range(int(x), int(y) + 1)
    lezioni = [int(c) - 1 for c in a[a.index("--solo") + 1]] if "--solo" in a else list(range(6))
    pagina = a[a.index("--pagina") + 1] if "--pagina" in a else str(ROOT / "index.html")
    ris, errs = await corse(pagina, semi, lezioni)
    OUT.mkdir(parents=True, exist_ok=True)
    nome = f"semi {semi.start}-{semi.stop - 1}"
    (OUT / f"{pathlib.Path(pagina).stem}_{semi.start}-{semi.stop - 1}.json").write_text(json.dumps(ris, ensure_ascii=False))
    passi, problemi = rapporto(ris, nome)
    corse_mani = sum(1 for x in ris)
    print(f"\nmisurato: {len(passi)} passi pratici, {corse_mani} corse a mani ferme, errori della pagina {len(errs)} {errs[:2]}")
    print("da guardare:" if problemi else "da guardare: niente")
    for q in problemi: print("  - " + q)
    valido = len(passi) == len(lezioni) * 0 + sum((6, 5, 9, 3, 6, 3)[l] for l in lezioni) and not errs
    print("ESITO:", "NON VALIDO (passi mancanti o errori della pagina)" if not valido else ("OK" if not problemi else "DA GUARDARE"))
    sys.exit(2 if not valido else 0)   # i casi «da guardare» sono un rapporto, non un fallimento dello script: si leggono (lancia_tutti.sh li mostra)

if __name__ == "__main__":   # importabile da collaudo_carriera_intera.py, che riusa PILOTA
    asyncio.run(main())
