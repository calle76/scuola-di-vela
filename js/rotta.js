// Scuola di vela, rotta.js — Rotta ottimale a regata finita (1.2.22, docs/PROPOSTA-ROTTA-OTTIMALE.md): vento registrato, isocrone, «dove hai perso».
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.

  // ======================================================================
  // ROTTA OTTIMALE (1.2.22, docs/PROPOSTA-ROTTA-OTTIMALE.md; idea e via di Ale, 9 novembre 2026)
  // Fuori dalla Scuola (regate a tema e torneo; R.rotta), a regata finita: la rotta più veloce dal punto in cui il giocatore ha tagliato la
  // linea all'arrivo, col vento che c'è stato davvero («col senno di poi»), ignorando le altre barche. Tre parti:
  //  1. registrazione del vento: ogni ROT_REG s si copiano raffiche, salto e tempo del gioco (solo lettura, nessun Math.random), e per ogni
  //     barca il taglio della linea e i giri di boa; ventoDa (gioco.js) rifà il vento esatto in ogni punto e istante;
  //  2. isocrone: a ogni ROT_DT s il fronte dei punti raggiungibili si allarga con la polare della barca del gioco (ROT_POL, js/rotta-dati.js,
  //     velocità di equilibrio con la scotta migliore, senza accelerazioni), ogni cambio di mure costa T_VIR o T_ABB secondi; si tiene il punto
  //     più lontano dall'origine del lato per ogni settore di ROT_SETT gradi e per mure. Un lato finisce quando si passa il cancello della
  //     boa (la semiretta dalla boa verso mk.out, come roundCheck, ad almeno ROT_BOA m) o la linea d'arrivo; il lato dopo parte da lì;
  //  3. «dove hai perso»: secondi per lato e fino a due motivi riconosciuti dal vento (virata sullo scarso, raffiche, lato del campo, manovre).
  // Costanti (ipotesi nostre, §2 della proposta): T_VIR 2 s e T_ABB 1 s misurati con tests/fisica/costo_manovre.js (virata 1,9-2,7 s,
  // abbattuta 0,0 s: 1 s è un minimo nostro perché la rotta non cambi mure a ogni passo); SCARSO 6°; settori di 2° (§2 D); passo 1 s.
  // ======================================================================
  const ROT_REG = 0.5, ROT_DT = 1, T_VIR = 2, T_ABB = 1, ROT_SETT = 2, ROT_BOA = 2, ROT_LATO_MAX = 900, ROT_TMAX = 1800, SCARSO = 6, ROT_RAFF = 1.12;
  const rot = { reg: [], barche: [], acc: 0, res: null, on: false, spento: false, giroLibero: false }; /* giroLibero (voce 50): true spegne il controllo del lato della boa (spento nella 1.3.23, acceso dalla 1.3.24 quando R1-R3 sono passati su semi nuovi) */

  // ---- registrazione ----
  function rotReset(){ rot.reg = []; rot.barche = R ? R.boats.map(() => ({ taglio: null, giri: [] })) : []; rot.acc = 1e9; rot.res = null; rot.on = false; rot.calc = false; }
  function rotCapture(dt){ // dal ciclo della regata (updateRace), dopo raceLegs; solo lettura
    if (!R || !R.rotta || rot.spento || R.t < 0 || R.t > ROT_TMAX) return;
    R.boats.forEach((b, k) => { const o = rot.barche[k]; if (!o) return;
      if (!o.taglio && b.leg >= 1) o.taglio = { t: R.t, x: b.S.x, y: b.S.y, h: b.S.h, leg: b.leg };
      else if (o.taglio && b.leg - 1 > o.giri.length + (o.taglio.leg - 1)) o.giri.push({ t: R.t, x: b.S.x, y: b.S.y }); });
    rot.acc += dt; if (rot.acc < ROT_REG - 1e-9) return; rot.acc = 0;
    rot.reg.push({ t: R.t, sim: simTime, sd: shiftSt ? shiftDeg : 0, g: gusts.map(g => [g.x, g.y, g.r, g.k, g.sh, g.age, g.ttl, g.big ? 1 : 0]) });
  }
  function rotRaffiche(t){ // le raffiche all'istante t (dalla copia precedente, spostate come in updateGusts) e salto e tempo del gioco
    const A = rot.reg; let lo = 0, hi = A.length - 1;
    if (t <= A[0].t) hi = 0; else if (t >= A[hi].t) lo = hi; else while (hi - lo > 1){ const m = (lo + hi) >> 1; if (A[m].t <= t) lo = m; else hi = m; }
    const a = A[lo], b = A[hi], dt = Math.max(0, t - a.t), f = b.t > a.t ? Math.min(1, dt / (b.t - a.t)) : 0;
    const to = (env.twd + 180) * D2R, vx = Math.sin(to) * env.tws * 0.8, vy = -Math.cos(to) * env.tws * 0.8, gs = [];
    for (const [x, y, r, k, sh, age, ttl, big] of a.g){ const ag = age + dt; if (ag > ttl) continue;
      gs.push({ x: x + vx * dt, y: y + vy * dt, r, k, sh, big: !!big, life: Math.max(0, Math.min(1, ag / 3, (ttl - ag) / 3)) }); }
    return { gs, sd: a.sd + (b.sd - a.sd) * f, sim: a.sim + dt };
  }
  const rotVento = (x, y, Q) => ventoDa(Q.gs, Q.sd, Q.sim, x, y); // Q = rotRaffiche(t)

  // ---- isocrone ----
  const ROT_TWA = []; for (let a = 30; a <= 180; a += 5) ROT_TWA.push(a); // multipli di 5: cadono sulle colonne della tabella (da 25°)
  function rotRiga(tws){ // la polare (ROT_POL, js/rotta-dati.js): velocità e scarroccio per ogni angolo di ROT_TWA con vento tws (m/s): interpolati solo sulla forza
    const P = ROT_POL, kn = Math.max(P.tws[0], Math.min(P.tws[P.tws.length - 1], tws * 1.9438)), i = Math.min(P.tws.length - 2, Math.floor(kn - P.tws[0])), f = kn - P.tws[i];
    return ROT_TWA.map(a => { const j = (a - P.twa[0]) / 5; return [P.v[i][j] * (1 - f) + P.v[i + 1][j] * f, P.lee[i][j] * (1 - f) + P.lee[i + 1][j] * f]; });
  }
  // da {x, y, s (mure: +1 vento da destra, -1 da sinistra, 0 non ancora), t} fino al cancello; ritorna il punto d'arrivo con la catena .par
  function rotLato(p0, cancello){
    const DT = rotPasso = rot.dt || (R && R.up >= 400 ? ROT_DT_LUNGO : ROT_DT); /* 1.3.27 (voce 66): passo delle isocrone, più lungo nelle regate lunghe (rot.dt solo per le misure) */
    let front = [Object.assign({ debt: 0, par: null, man: 0 }, p0)];
    const ox = p0.x, oy = p0.y, t0 = p0.t, tmp = { x: 0, y: 0 }; let rigaTws = NaN, rigaUlt = null;
    for (let t = t0; t < t0 + ROT_LATO_MAX && t < ROT_TMAX; t += DT){
      const Q = rotRaffiche(t), best = new Map();
      for (const p of front){
        const w = rotVento(p.x, p.y, Q), riga = w.tws === rigaTws ? rigaUlt : (rigaTws = w.tws, rigaUlt = rotRiga(w.tws)); // 1.2.40: fuori dalle raffiche la forza è sempre la stessa
        for (let n = 0; n < ROT_TWA.length; n++) for (let si = 0; si < 2; si++){ const s = si ? -1 : 1, twa = ROT_TWA[n];
          let debt = p.debt, man = p.man;
          if (p.s && s !== p.s){ debt += twa < 90 ? T_VIR : T_ABB; man++; }
          const mv = Math.max(0, DT - debt); debt = Math.max(0, debt - DT);
          const [v, lee] = riga[n], c = (w.twd - s * (twa + lee)) * D2R; // s = +1: vento da destra, la prua sta a sinistra del vento
          // 1.2.40: il punto nuovo si crea solo se entra nel fronte o finisce il lato (stessi conti e stesso ordine di prima: risultati identici, circa metà del tempo)
          tmp.x = p.x + Math.sin(c) * v * mv; tmp.y = p.y - Math.cos(c) * v * mv;
          const ps = cancello.passo ? ((p.lo ?? (p.lo = cancello.lontano(p))) ? 4 : cancello.passo(p, tmp)) : 0; /* 1.3.23 (voce 50): niente passi che per il gioco girano la boa dal lato sbagliato, finché il ramo non l'ha già girata */
          if (ps & 8 && !p.giu) continue;
          const giu = p.giu || (ps & 16) > 0, ra = ps & 7;
          const fr = cancello(p, tmp); if (fr !== null){ const q = { x: tmp.x, y: tmp.y, s, t: t + DT, debt, man, par: p, giu, ra };
            q.x = p.x + (q.x - p.x) * fr; q.y = p.y + (q.y - p.y) * fr; q.t = t + DT * fr; q.fine = true; return q; }
          const dx = tmp.x - ox, dy = tmp.y - oy, d = Math.hypot(dx, dy), key = Math.round(Math.atan2(dx, -dy) / D2R / ROT_SETT) * 4 + (s > 0 ? 1 : 0) + (cancello.sbagliato && !giu && cancello.sbagliato(tmp) ? 2 : 0); /* 1.3.27: chi è oltre la boa dal lato sbagliato ha un posto a parte nel settore */
          const sc = d - debt * v, o = best.get(key); if (!o || sc > o.sc) best.set(key, { sc, q: { x: tmp.x, y: tmp.y, s, t: t + DT, debt, man, par: p, giu, ra } }); // chi deve ancora finire una manovra vale meno
        }
      }
      front = [...best.values()].map(o => o.q);
    }
    return null;
  }
  // cancello della boa: semiretta dalla boa verso mk.out, passata dal lato giusto (da a ≥ 0 ad a < 0, come roundCheck) ad almeno ROT_BOA m
  const ROT_DT_LUNGO = 1.5; let rotPasso = ROT_DT; // 1.3.27 (voce 66): passo delle isocrone nelle regate lunghe (bolina da 400 m in su): il più corto sotto 3 s di calcolo su questo PC con giro valido (semi 401-403, confermato sui 404-406); rotPasso: quello del lato in calcolo
  const ROT_LONTANO = 8; // 1.3.23: metri oltre i quali un passo (al massimo circa 5 m in 1 s) non può tagliare la semiretta della boa
  const ROT_PEZZI = 8; // 1.3.23: pezzi in cui si guarda un passo vicino alla boa (ipotesi nostra: con passi fino a 2,5 m, circa 30 cm)
  const ROT_OLTRE = 0.02; // 1.3.23: frazione del passo oltre la semiretta in cui finisce il lato (pochi cm), ipotesi nostra: un punto proprio sulla linea, se la rotta poi torna indietro, per roundCheck non ha girato
  const rotCancBoa = mk => { const ux = Math.sin(mk.out * D2R), uy = -Math.cos(mk.out * D2R), oltre = rot.giroLibero ? 0 : ROT_OLTRE; const c = (p, q) => { // 1.2.40: ux e uy una volta sola
    const cp = (p.x - mk.x) * uy - (p.y - mk.y) * ux, cq = (q.x - mk.x) * uy - (q.y - mk.y) * ux; // > 0: a destra della semiretta guardando lungo out
    if (!(cp <= 0 && cq > 0) && !(cp < 0 && cq >= 0)) return null; // roundCheck: da bearing-out ≥ 0 (a destra, prodotto < 0 qui) a < 0
    const f = cp / (cp - cq), ax = p.x + (q.x - p.x) * f - mk.x, ay = p.y + (q.y - p.y) * f - mk.y;
    return ax * ux + ay * uy >= ROT_BOA ? Math.min(1, f + oltre) : null;
  };
    // 1.3.23 (voce 50, docs/PROPOSTA-ROTTA-GIRO-BOA.md; via di Ale del 20 nov): la regola di roundCheck (js/gioco.js) seguita lungo ogni ramo della rotta. Ogni punto si ricorda
    // (.ra) l.ultimo stato visto fuori da 1,5 m dalla boa: bearing-out < 0, ≥ 0, oppure oltre i 90° da out. Il passo che va da < 0 a ≥ 0 è un giro sbagliato e non si fa,
    // finché il ramo non è già passato da ≥ 0 a < 0 (.giu: per il gioco la boa è girata, anche sotto i ROT_BOA m del cancello). Entro 6 m dalla boa il passo si guarda in ROT_PEZZI
    // pezzi (il gioco controlla 60 volte al secondo). Prima stesura (20 nov): solo il punto di taglio, e vietava anche i passaggi sopra la boa entrati dal lato interno,
    // che il gioco non conta: rotte già valide fino a 7,5 s più lente (R3). rot.giroLibero = true lo spegne (tests/misura_giro_boa.py, controprova).
    // .ra in un numero: 0 nessuno stato ancora, 1 oltre i 90°, 2 bearing-out < 0, 3 ≥ 0, 4 «dalla posizione» (punto lontano: lo stato è quello del punto stesso);
    // c.passo restituisce .ra del punto nuovo più 8 (giro sbagliato) e 16 (giro giusto). c.lontano: il punto è a più di ROT_LONTANO m dalla boa e dalla retta della
    // semiretta, quindi nessun passo che parte da lì (al massimo pochi metri) può fare un giro: il controllo si salta (dopo la prima stesura, +45% di tempo di calcolo)
    const stato = (dx, dy) => dx * dx + dy * dy < 2.25 ? 0 : dx * ux + dy * uy < 0 ? 1 : dx * uy - dy * ux > 0 ? 2 : 3;
    // 1.3.27 (voce 66): un punto oltre la boa (entro 90° da out) dal lato < 0 senza aver girato non può più fare il giro senza tornare indietro; nelle isocrone stava nello stesso
    // settore delle rotte giuste e, essendo più avanti, le cacciava: rotta più lenta di 83 s o nessuna rotta nelle regate lunghe (misura_passo_rotta, semi 402 e 403)
    if (!rot.giroLibero) c.sbagliato = q => { const qx = q.x - mk.x, qy = q.y - mk.y; return qx * ux + qy * uy >= 0 && qx * uy - qy * ux > 0; };
    if (!rot.giroLibero) c.lontano = p => { const px = p.x - mk.x, py = p.y - mk.y, cr = px * uy - py * ux;
      const m = ROT_LONTANO * rotPasso; return (cr > m || cr < -m) && px * px + py * py > (6 + m) * (6 + m); }; /* 1.3.27: il margine cresce col passo */
    if (!rot.giroLibero) c.passo = (p, q) => { const px = p.x - mk.x, py = p.y - mk.y; let ra = p.ra === 4 ? stato(px, py) : p.ra || 0, neg = 0, pos = 0;
      const qx = q.x - mk.x, qy = q.y - mk.y, N = Math.min(px * px + py * py, qx * qx + qy * qy) < 36 ? ROT_PEZZI : 1;
      for (let j = 1; j <= N; j++){ const f = j / N, st = stato(px + (qx - px) * f, py + (qy - py) * f); if (!st) continue;
        if (ra === 2 && st === 3 && !pos) neg = 8; else if (ra === 3 && st === 2) pos = 16; ra = st; } /* un -1 dopo il +1 dello stesso passo non conta: la boa è già girata */
      return ra | neg | pos; };
    return c; };
  const rotCancArrivo = () => (p, q) => { const [px, py] = toWF(p.x, p.y), [qx, qy] = toWF(q.x, q.y);
    if (!(py < 0 && qy >= 0)) return null; const f = -py / (qy - py), x = px + (qx - px) * f; return Math.abs(x) <= LINE_HALF ? f : null; };

  // la rotta ottimale per la barca k (0 = giocatore) dal suo taglio della linea: { tempo, lati: [tempi d'arrivo ai cancelli], punti: [{t, x, y, s}] }
  function rotCalcola(k = 0){
    const o = rot.barche[k]; if (!o || !o.taglio || rot.reg.length < 2) return null;
    const tg = o.taglio, w = rotVento(tg.x, tg.y, rotRaffiche(tg.t));
    let p = { x: tg.x, y: tg.y, t: tg.t, s: norm180(tg.h - w.twd) < 0 ? 1 : -1 }; const lati = [], cat = [];
    const canc = R.marks.slice(tg.leg - 1).map(rotCancBoa).concat([rotCancArrivo()]);
    for (const c of canc){ const q = rotLato(p, c); if (!q) return null; lati.push(q.t);
      const pezzo = []; for (let r = q; r && r !== p; r = r.par) pezzo.push({ t: r.t, x: r.x, y: r.y, s: r.s, man: r.man }); cat.push(...pezzo.reverse());
      p = { x: q.x, y: q.y, t: q.t, s: q.s }; }
    return { tempo: p.t, t0: tg.t, lati, punti: [{ t: tg.t, x: tg.x, y: tg.y, s: 0 }].concat(cat) };
  }

  // ---- rotta in assoluto (1.2.40, docs/PROPOSTA-ROTTA-ASSOLUTA.md §8-9; via di Ale del 14 novembre 2026, notte) ----
  // Allo sparo, da ROT_ASS_N punti della linea, uno ogni ROT_ASS_PASSO m e centrati, con le mure libere: per ognuno la rotta fino alla boa 1, con lo stesso
  // calcolo della verde (rotLato). Il più veloce è il punto ideale; da lì la rotta intera (viola). La barca si considera già lanciata allo sparo e le altre
  // barche non esistono: lo dice il testo. Costanti nostre: 7 punti, 10 m (§8). I punti stanno fra spillo e comitato (non fromWF, che segue il vento impostato).
  const ROT_ASS_N = 7, ROT_ASS_PASSO = 10;
  const rotCatena = (q, p) => { const pezzo = []; for (let r = q; r && r !== p; r = r.par) pezzo.push({ t: r.t, x: r.x, y: r.y, s: r.s, man: r.man }); return pezzo.reverse(); }; // come in rotCalcola
  function rotAssoluta(forza){ // forza: indice del punto della linea da usare comunque (solo per i collaudi, A2)
    if (!R || rot.reg.length < 2 || !R.marks.length) return null;
    const canc = R.marks.map(rotCancBoa).concat([rotCancArrivo()]), cand = [];
    for (let i = 0; i < ROT_ASS_N; i++){ const dx = (i - (ROT_ASS_N - 1) / 2) * ROT_ASS_PASSO, f = (dx + LINE_HALF) / (2 * LINE_HALF), p = { x: R.pin.x + (R.cb.x - R.pin.x) * f, y: R.pin.y + (R.cb.y - R.pin.y) * f, t: 0, s: 0 }, q = rotLato(p, canc[0]);
      cand.push({ dx, p, q, boa: q ? q.t : Infinity }); }
    const m = forza === undefined ? cand.reduce((a, b) => b.boa < a.boa ? b : a) : cand[forza]; if (!m.q) return null;
    let p = m.p, q = m.q; const lati = [q.t], cat = rotCatena(q, p);
    for (let j = 1; j < canc.length; j++){ p = { x: q.x, y: q.y, t: q.t, s: q.s }; q = rotLato(p, canc[j]); if (!q) return null; lati.push(q.t); cat.push(...rotCatena(q, p)); }
    const punti = [{ t: 0, x: m.p.x, y: m.p.y, s: 0 }].concat(cat), d = punti.find(c => c.t >= 5) || punti[punti.length - 1];
    return { tempo: q.t, t0: 0, lati, punti, dx: m.dx, mure: (cat.find(c => c.s) || { s: 0 }).s, dir: Math.atan2(d.x - m.p.x, -(d.y - m.p.y)), cand: cand.map(c => ({ dx: c.dx, boa: c.boa })) };
  }
  const rotBoa1Da = (x, y, t) => { const q = R && R.marks.length ? rotLato({ x, y, t, s: 0 }, rotCancBoa(R.marks[0])) : null; return q ? q.t : null; }; // per i collaudi (P1)

  // per la barca k, lato per lato, il tempo vero e quello della rotta ottimale partendo da dove e quando quella barca ha cominciato il lato
  // (misura degli avversari, docs/PROPOSTA-AVVERSARI-ROTTA.md): [{ lato, vero, ott, manOtt }], solo i lati finiti
  function rotLatiBarca(k){
    const o = rot.barche[k], b = R.boats[k]; if (!o || !o.taglio || rot.reg.length < 2) return [];
    const inizi = [o.taglio].concat(o.giri), fini = o.giri.map(g => g.t).concat(b.fin !== null && !b.dsq ? [b.fin - (b.pen || 0)] : []), canc = R.marks.slice(o.taglio.leg - 1).map(rotCancBoa).concat([rotCancArrivo()]), out = [];
    for (let j = 0; j < fini.length && j < canc.length; j++){
      const a = inizi[j], q = rotLato({ x: a.x, y: a.y, t: a.t, s: 0 }, canc[j]); if (!q) continue;
      let man = 0; for (let r = q; r && r.par; r = r.par) if (r.par.s && r.s !== r.par.s) man++;
      out.push({ lato: j, vero: fini[j] - a.t, ott: q.t - a.t, manOtt: man }); }
    return out;
  }

  // ---- layline (1.2.22; Ale, 9 novembre: «la layline … come si può inserire nel gioco?», pezzo 1: nella rotta ottimale) ----
  // Dalla boa di bolina, una per mura: da lì di bolina si arriva alla boa senza virare. L'angolo è quello della VMG di bolina migliore della
  // polare del gioco, scarroccio compreso (rotta sul fondo, circa 48° dal vento con 6-15 nodi), col vento alla boa in quell'istante: coi salti si sposta.
  // LAY_TOLL (5°) e LAY_MIN (10 m) sono ipotesi nostre: sotto non si dice niente.
  const LAY_TOLL = 5, LAY_MIN = 10, LAY_VICINO = 80;
  function rotLay(tws){ const r = rotRiga(tws); let best = -1, a = 45;
    ROT_TWA.forEach((t, n) => { if (t > 90) return; const c = t + r[n][1], v = r[n][0] * Math.cos(c * D2R); if (v > best){ best = v; a = c; } }); return a; }
  function rotOltre(mk, x, y, t){ // gradi oltre (+) o prima (−) della layline, e distanza dalla boa; 0° = sottovento alla boa
    const w = rotVento(mk.x, mk.y, rotRaffiche(t)), b = Math.abs(norm180(bearingTo(mk, { x, y }) - (w.twd + 180)));
    return { g: b - rotLay(w.tws), d: Math.hypot(x - mk.x, y - mk.y) };
  }

  // ---- layline in acqua (1.2.23, docs/PROPOSTA-LAYLINE.md, pezzo 2) ----
  // Aiuto disattivabile (⚙ «Layline»): nelle regate fuori dalla Scuola (R.rotta), non negli esercizi, fino al giro della boa di bolina.
  // «regate» (di partenza): non nel torneo; «tutte»: anche nel torneo (decisione di Ale: nel torneo parte spenta ma si può accendere).
  const LAY_LUNGA = 0.5; // 1.2.24 (osservazione 110, Ale: «non è troppo lunga?»): in acqua lunghe metà bolina; nella vista della rotta ottimale restano 1,3 volte
  const layDir = w => { const a = rotLay(w.tws); return [-1, 1].map(k => norm360(w.twd + 180 + k * a)); }; // direzioni dalla boa verso le due layline
  function layVisibile(){ if (!R || !R.rotta || R.es || riv.on) return false; const me = R.boats[0];
    return (opt.layline === "tutte" || (opt.layline === "regate" && !R.tor)) && me.leg <= 1 && me.fin === null && !me.dnf; }
  function layDisegna(v){
    if (!layVisibile()) return;
    const mk = R.marks[0], L = R.up * LAY_LUNGA, lw = Math.max(0.12, 1.4 / v.ppm);
    ctx.strokeStyle = "rgba(255,230,120,.75)"; ctx.lineWidth = lw; ctx.setLineDash([4 * lw, 4 * lw]);
    for (const d of layDir(windAt(mk.x, mk.y))){ ctx.beginPath(); ctx.moveTo(mk.x, mk.y); ctx.lineTo(mk.x + Math.sin(d * D2R) * L, mk.y - Math.cos(d * D2R) * L); ctx.stroke(); }
    ctx.setLineDash([]);
  }
  $("laySel").onchange = e => { opt.layline = e.target.value; };

  // ---- dove hai perso ----
  function rotSpiega(ott){ // confronto col giocatore (riv.all a 10 al secondo): secondi per lato e fino a due motivi
    const me = R.boats[0], o = rot.barche[0], fine = me.fin;
    const tLati = o.giri.map(g => g.t).concat(fine !== null ? [fine] : []), nomi = R.tri ? ["Bolina", "Lasco", "Lasco"] : ["Bolina", "Poppa"];
    const lati = ott.lati.map((t, j) => { const a0 = j ? ott.lati[j - 1] : ott.t0, b0 = j ? tLati[j - 1] : o.taglio.t;
      return { nome: (R.tri && j === 2) ? "Ultimo lasco" : nomi[j] || "Lato " + (j + 1), ott: t - a0, tu: tLati[j] !== undefined ? tLati[j] - b0 : null }; });
    const traccia = (t0, t1) => riv.all.filter(f => f.t >= t0 && f.t <= t1).map(f => ({ t: f.t, x: f.b[0][0], y: f.b[0][1], h: f.b[0][2] }));
    const motivi = [];
    lati.forEach((L, j) => {
      if (L.tu === null) return;
      const a = j ? tLati[j - 1] : o.taglio.t, b = tLati[j], oa = j ? ott.lati[j - 1] : ott.t0, ob = ott.lati[j];
      const tu = traccia(a, b), op = ott.punti.filter(q => q.t > oa && q.t <= ob), mure = (x, y, h, t) => { const w = rotVento(x, y, rotRaffiche(t)); return norm180(h - w.twd) < 0 ? 1 : -1; };
      let mTu = 0, prev = null; for (let i = 0; i < tu.length; i += 5){ const f = tu[i], m = mure(f.x, f.y, f.h, f.t); if (prev !== null && m !== prev) mTu++; prev = m; }
      let mOt = 0; for (let i = 1; i < op.length; i++) if (op[i].s && op[i - 1].s && op[i].s !== op[i - 1].s) mOt++;
      if (L.nome === "Bolina" && mTu >= mOt + 3) motivi.push( // solo di bolina: nel gioco l'abbattuta quasi non costa (costo_manovre.js), le virate sì
        { j, peso: L.tu - L.ott, txt: `${L.nome}: hai cambiato mure ${mTu} volte, la rotta ottimale ${mOt}. Ogni virata costa circa ${T_VIR} s.` });
      // raffiche: quota di tempo in raffica sui due percorsi
      const inR = arr => arr.length ? arr.filter(q => rotVento(q.x, q.y, rotRaffiche(q.t)).tws > env.tws * ROT_RAFF).length / arr.length : 0;
      const rTu = inR(tu.filter((_, i) => i % 10 === 0)), rOt = inR(op);
      if (gustLevel && rOt - rTu >= 0.2) motivi.push({ j, peso: L.tu - L.ott, txt: `${L.nome}: la rotta ottimale è stata in raffica il ${Math.round(rOt * 100)}% del tempo, tu il ${Math.round(rTu * 100)}%. Cerca le zone scure sull'acqua.` });
      // virata sullo scarso: la rotta ottimale cambia mure di bolina dopo che il vento è girato contro le mure di prima di almeno SCARSO gradi.
      // Con le mure s la prua è twd − s·twa, quindi twa = s·(twd − prua): se il vento gira di d, twa cambia di s·d; scarso = twa che cala, s·d < 0
      if (L.nome === "Bolina") for (let i = 1; i < op.length; i++){ const q = op[i], p = op[i - 1];
        if (!p.s || q.s === p.s) continue;
        const w1 = rotVento(q.x, q.y, rotRaffiche(q.t)).twd, w0 = rotVento(q.x, q.y, rotRaffiche(Math.max(ott.t0, q.t - 30))).twd, d = norm180(w1 - w0);
        if (p.s * d <= -SCARSO){ const vicino = tu.some((f, n) => n >= 5 && Math.abs(f.t - q.t) <= 15 && mure(f.x, f.y, f.h, f.t) !== mure(tu[n - 5].x, tu[n - 5].y, tu[n - 5].h, tu[n - 5].t));
          if (!vicino){ motivi.push({ j, t: q.t, scarso: Math.round(Math.abs(d)), peso: L.tu - L.ott + 1, txt: `A ${rivTempo(q.t)} il vento è girato di ${Math.round(Math.abs(d))}° contro le tue mure: la rotta ottimale ha virato, tu no.` }); break; } } }
      // layline: la prima virata fatta oltre la layline (1.3.13; prima l'ultima del lato), oppure più virate vicino alla boa
      if (L.nome === "Bolina" && tu.length > 10){ const mk = R.marks[0], vir = [];
        /* 1.3.13: le virate dentro un giro di penalità non contano (la prua gira di almeno 270° nello stesso verso nei 10 s attorno) */
        const inGiro = f => { let s = 0; for (let i = 1; i < tu.length; i++) if (Math.abs(tu[i].t - f.t) <= 10) s += norm180(tu[i].h - tu[i - 1].h); return Math.abs(s) >= 270; };
        for (let n = 5; n < tu.length; n += 5){ const f = tu[n], g = tu[n - 5]; if (mure(f.x, f.y, f.h, f.t) !== mure(g.x, g.y, g.h, g.t) && !inGiro(f)) vir.push(f); }
        /* 1.3.13: la prima virata fatta oltre la layline (fino alla 1.3.12 solo l'ultima del lato: con un'altra virata vicino alla boa la frase non usciva) */
        const oltreDi = f => { const o = rotOltre(mk, f.x, f.y, f.t); return o.g >= LAY_TOLL ? o.d * Math.sin(o.g * D2R) : 0; };
        const ul = vir.find(f => oltreDi(f) >= LAY_MIN) || vir[vir.length - 1], o2 = ul ? rotOltre(mk, ul.x, ul.y, ul.t) : null, oltreM = o2 ? o2.d * Math.sin(Math.max(0, o2.g) * D2R) : 0;
        const vicine = vir.filter(f => Math.hypot(f.x - mk.x, f.y - mk.y) < LAY_VICINO).length;
        L.lay = { oltre: o2 && o2.g >= LAY_TOLL && oltreM >= LAY_MIN ? Math.round(oltreM) : 0, vicine, t: ul ? ul.t : null, tv: vir.filter(f => Math.hypot(f.x - mk.x, f.y - mk.y) < LAY_VICINO).map(f => f.t)[0] ?? null }; // 1.3.3: per il coach
        if (o2 && o2.g >= LAY_TOLL && oltreM >= LAY_MIN) motivi.push({ j, peso: L.tu - L.ott + 0.5, txt: `Hai virato per la boa ${Math.round(oltreM)} m oltre la layline: virando prima avresti fatto meno strada.` });
        else if (vicine >= 2) motivi.push({ j, peso: L.tu - L.ott + 0.5, txt: `Negli ultimi ${LAY_VICINO} m prima della boa hai virato ${vicine} volte: arrivando sulla layline ne basta una.` }); }
      // lato del campo: con il vento che ruota di almeno 2 SCARSO nel lato, la rotta ottimale va dalla parte della rotazione
      if (L.nome === "Bolina" && op.length > 2){ const wa = rotVento(op[0].x, op[0].y, rotRaffiche(oa)).twd, wb = rotVento(op[0].x, op[0].y, rotRaffiche(ob)).twd, rr = norm180(wb - wa);
        const xm = arr => arr.reduce((s, q) => s + toWF(q.x, q.y)[0], 0) / Math.max(1, arr.length), xo = xm(op), xt = xm(tu);
        if (Math.abs(rr) >= 2 * SCARSO && Math.sign(xo) !== Math.sign(xt) && Math.abs(xo - xt) > 15)
          motivi.push({ j, peso: L.tu - L.ott, txt: `${L.nome}: il vento è ruotato di ${Math.round(Math.abs(rr))}° ${rr > 0 ? "verso destra" : "verso sinistra"}; la rotta ottimale è andata da quella parte del campo, tu dall'altra.` }); }
    });
    motivi.sort((a, b) => b.peso - a.peso);
    return { lati, motivi: motivi.slice(0, 2) };
  }

  // ---- coach (1.3.3, docs/PROPOSTA-COACH.md; via di Ale del 15 novembre 2026) ----
  // Al posto del riassunto della rotta ottimale: al massimo COA_N frasi, ognuna da un modello fisso riempito con numeri misurati, con un momento t
  // (cliccandola la moviola salta lì, COA_ANT s prima) e un peso in secondi per scegliere le più importanti. Non dipende dalla migliore in assoluto (V).
  // Frasi: clou (il minuto in cui il distacco dalla rotta ottimale cresce di più, fuori dai tratti coperti o affollati), affollato (se il tratto peggiore
  // era fra le barche: la rotta ottimale non ne tiene conto), coperto (cono d'ombra, secondi persi con la polare), boa (layline), partenza, penalità, bene.
  // Il peso in secondi di clou e boa è una stima (metri divisi per la velocità media, o virate per T_VIR): serve solo a ordinare, le frasi dicono i metri.
  // Costanti, ipotesi nostre (proposta, §Costanti): COA_N frasi, finestra del clou COA_FIN s, coperto da COA_COP di vento tolto per almeno COA_COP_S s,
  // perdita minima COA_MIN s, affollato entro COA_AFF m (3 lunghezze), anticipo del salto COA_ANT s, ritardo minimo al via COA_VIA s.
  const COA_RIPARTI = 10, COA_N = 3, COA_FIN = 60, COA_COP = 0.1, COA_COP_S = 10, COA_MIN = 5, COA_AFF = 3 * BOAT.length, COA_ANT = 5, COA_VIA = 3;
  /* 1.3.13 (docs/PROPOSTA-COACH-2.md): una finestra è «affollata» solo con almeno COA_AFF_S secondi affollati su COA_FIN, e i primi COA_AFF_VIA secondi dopo il taglio della linea non contano
     (al via le barche sono insieme per forza); la frase delle virate vicino alla boa esce da COA_VIR virate. Ipotesi nostre, scelte sui semi 2601-2605 */
  const COA_AFF_S = 20, COA_AFF_VIA = 15, COA_VIR = 3;
  function rotVel(twa, tws){ // velocità della polare del gioco (m/s) per un angolo dal vento e una forza (m/s)
    const r = rotRiga(tws), a = clamp(twa, ROT_TWA[0], 180), j = Math.min(ROT_TWA.length - 2, Math.floor((a - ROT_TWA[0]) / 5)), f = (a - ROT_TWA[j]) / 5;
    return r[j][0] * (1 - f) + r[j + 1][0] * f;
  }
  function coaCoperto(tu){ // tratti col cono che toglie almeno COA_COP per almeno COA_COP_S s: [{ t0, t1, persi, da }]
    const out = []; let cur = null;
    const chiudi = () => { if (cur && cur.t1 - cur.t0 >= COA_COP_S) out.push(cur); cur = null; };
    for (let i = 1; i < tu.length; i++){ const f = tu[i], c = f.c, dt = f.t - tu[i - 1].t;
      if (c && c[0] >= COA_COP){
        if (!cur) cur = { t0: f.t, t1: f.t, persi: 0, chi: {} };
        const p = f.b[0], w = rotVento(p[0], p[1], rotRaffiche(f.t)), twa = Math.abs(norm180(p[2] - w.twd)), v0 = rotVel(twa, w.tws);
        if (v0 > 0.05) cur.persi += dt * (1 - rotVel(twa, w.tws * (1 - c[0])) / v0);
        cur.t1 = f.t; cur.chi[c[1]] = (cur.chi[c[1]] || 0) + dt;
      } else if (cur && f.t - cur.t1 > 1) chiudi();
    }
    chiudi();
    return out.map(o => ({ ...o, da: +Object.entries(o.chi).sort((a, b) => b[1] - a[1])[0][0] }));
  }
  // il clou: per ogni secondo, quanti metri di percorso ti mancano in più della rotta ottimale (distanza dalla prossima boa più i lati dopo, fino al centro
  // della linea d'arrivo); la finestra di COA_FIN s in cui questo cresce di più. Prima stesura (scartata il 15 nov, prima di misurare le soglie): la lunghezza
  // del filo, cioè la distanza fra le due barche nello stesso istante; ma due rotte su lati diversi del campo si allontanano anche senza perdere niente
  function coaClou(P, tu, lati){
    const me0 = rot.barche[0], M = R.marks.slice(me0.taglio.leg - 1).map(m => [m.x, m.y]).concat([[(R.pin.x + R.cb.x) / 2, (R.pin.y + R.cb.y) / 2]]);
    const dopo = M.map((m, k) => M.slice(k).reduce((a, q, n, A) => a + (n ? Math.hypot(q[0] - A[n - 1][0], q[1] - A[n - 1][1]) : 0), 0)); // dalla boa k all'arrivo
    const resto = (x, y, k) => k >= M.length ? 0 : Math.hypot(x - M[k][0], y - M[k][1]) + dopo[k];
    const latoDi = (t, fine) => { let k = 0; while (k < fine.length && t >= fine[k]) k++; return k; };
    const tuFine = me0.giri.map(g => g.t), g = [], fine = Math.min(P[P.length - 1].t, tu[tu.length - 1].t);
    for (let s = P[0].t; s <= fine; s += 1){ const q = rotIstante(P, s, q => [q.x, q.y]), f = rotIstante(tu, s, f => f.b[0]);
      if (q && f) g.push({ s, d: resto(f[0], f[1], latoDi(s, tuFine)) - resto(q[0], q[1], latoDi(s, lati)) }); }
    const aff = new Set();
    for (const f of tu){ const me = f.b[0]; if (f.t < me0.taglio.t + COA_AFF_VIA) continue; if ((f.c && f.c[0] >= COA_COP) || f.b.some((b, k) => k && Math.hypot(b[0] - me[0], b[1] - me[1]) < COA_AFF)) aff.add(Math.floor(f.t)); }
    const vel = (t0, t1) => { const fr = tu.filter(f => f.t >= t0 && f.t <= t1); return fr.length ? fr.reduce((a, f) => a + f.b[0][4], 0) / fr.length : 1; };
    let best = null, tutto = null;
    for (let i = 0; i + COA_FIN < g.length; i++){
      const a = g[i], b = g[i + COA_FIN], w = { t0: a.s, t1: b.s, m: b.d - a.d };
      let nAff = 0; for (let s = Math.floor(a.s); s <= b.s; s++) if (aff.has(s)) nAff++;
      const libero = nAff < COA_AFF_S; w.libero = libero;
      if (!tutto || w.m > tutto.m) tutto = w;
      if (libero && (!best || w.m > best.m)) best = w;
    }
    for (const w of [best, tutto]) if (w) w.peso = w.m / Math.max(0.5, vel(w.t0, w.t1));
    return { best, tutto, g };
  }
  function coaFrasi(ott, sp){
    const me = R.boats[0], o = rot.barche[0], fineTu = me.fin !== null ? me.fin : riv.all[riv.all.length - 1].t;
    const tu = riv.all.filter(f => f.t >= o.taglio.t && f.t <= fineTu), F = [], T = rivTempo;
    if (tu.length > 2){
      // clou e affollato
      const C = coaClou(ott.punti, tu, ott.lati), b = C.best;
      if (b && b.peso >= COA_MIN){
        const sc = sp.motivi.find(m => m.t !== undefined && m.t >= b.t0 - 10 && m.t <= b.t1);
        F.push({ tipo: "clou", t: b.t0, peso: b.peso, m: Math.round(b.m), t0: b.t0, t1: b.t1,
          txt: `Qui hai perso di più: fra ${T(b.t0)} e ${T(b.t1)} la rotta ottimale ha guadagnato ${Math.round(b.m)} m di percorso su di te.` + (sc ? ` Il vento era girato di ${sc.scarso}° contro di te e la rotta ottimale ha virato (lezione 11).` : "") });
      }
      const w = C.tutto;
      if (w && !w.libero && w.peso >= COA_MIN && (!b || w.m > b.m))
        F.push({ tipo: "affollato", t: w.t0, peso: w.peso, m: Math.round(w.m), t0: w.t0, t1: w.t1,
          txt: `Fra ${T(w.t0)} e ${T(w.t1)} hai perso ${Math.round(w.m)} m di percorso, ma c'erano altre barche: la rotta ottimale non ne tiene conto.` });
      // coperto: il tratto che è costato di più
      const cop = coaCoperto(tu).sort((a, b) => b.persi - a.persi)[0];
      if (cop && cop.persi >= 1){ const chi = R.boats[cop.da];
        F.push({ tipo: "coperto", t: cop.t0, peso: cop.persi, s: Math.round(cop.persi), t0: cop.t0, t1: cop.t1,
          txt: `Fra ${T(cop.t0)} e ${T(cop.t1)} eri nel cono d'ombra ${chi ? (FLEET_LOOK.some(l => l.name === chi.name) ? "della " : "di ") + chi.name : "di un'altra barca"}: circa ${Math.round(cop.persi)} s persi.` });
      }
    }
    // alla boa (lato di bolina)
    const L0 = sp.lati.find(L => L.nome === "Bolina" && L.lay);
    const boa = []; /* 1.3.13: delle due frasi sulla boa esce la più pesante; quella delle virate da COA_VIR virate, col peso almeno COA_MIN (prima usciva solo da 4) */
    if (L0 && L0.lay.oltre) boa.push({ tipo: "boa", t: L0.lay.t, peso: L0.lay.oltre / 2, m: L0.lay.oltre, txt: `Hai virato per la boa ${L0.lay.oltre} m oltre la layline (lezione 23).` });
    if (L0 && L0.lay.vicine >= COA_VIR) boa.push({ tipo: "boa", t: L0.lay.tv, peso: Math.max(COA_MIN, (L0.lay.vicine - 1) * T_VIR), n: L0.lay.vicine, txt: `Negli ultimi ${LAY_VICINO} m prima della boa hai virato ${L0.lay.vicine} volte: di solito ne basta una (lezione 23).` });
    if (boa.length) F.push(boa.sort((a, b) => b.peso - a.peso)[0]);
    // partenza
    const f0 = riv.all.reduce((a, f) => Math.abs(f.t) < Math.abs(a.t) ? f : a, riv.all[0]), kn = f0.b[0][4] * 1.9438, rit = o.taglio.t;
    if (reg.ocs) F.push({ tipo: "partenza", ocs: true, t: 0, peso: Math.max(rit, COA_MIN), s: Math.round(rit), txt: `Al via eri oltre la linea: sei dovuto tornare e l'hai tagliata ${Math.round(rit)} s dopo lo sparo (lezione 17).` });
    else if (rit >= COA_VIA) F.push({ tipo: "partenza", t: 0, peso: rit, s: Math.round(rit), kn: +kn.toFixed(1), txt: `Hai tagliato la linea ${Math.round(rit)} s dopo il via; allo sparo andavi a ${kn.toFixed(1).replace(".", ",")} nodi (lezione 18).` });
    // 1.3.6 (Ale, 15 nov: «arrivato ultimo e scuffiato, il coach … non ha citato la scuffiata»): la prima scuffia della regata, coi secondi a barca rovesciata
    // (le copie della moviola, colonna 8); peso = quei secondi più COA_RIPARTI per tornare a velocità (stima nostra, solo per ordinare)
    { const cap = riv.all.filter(f => f.t >= rivT0() && f.b[0][8]); if (cap.length){ const t0 = cap[0].t; let t1 = t0; for (const f of riv.all) if (f.t >= t0){ if (!f.b[0][8]) break; t1 = f.t; }
      const quante = riv.all.reduce((a, f, i) => a + (i && f.b[0][8] && !riv.all[i - 1].b[0][8] ? 1 : 0), cap[0] === riv.all[0] ? 1 : 0);
      F.push({ tipo: "scuffia", t: t0, peso: t1 - t0 + COA_RIPARTI, s: Math.round(t1 - t0), n: quante,
        txt: `A ${T(t0)} hai scuffiato: ${Math.round(t1 - t0)} s con la barca rovesciata${quante === 2 ? " (e un'altra volta)" : quante > 2 ? ` (e altre ${quante - 1} volte)` : ""} (lezione 8).` }); } }
    // penalità: il primo contatto con colpa tua e la prima boa toccata
    const ct = riv.segni.find(g => g.auto && g.label.includes(". Tu, contatto con "));
    if (ct){ const altra = ct.label.split(". Tu, contatto con ")[1].split(":")[0];
      F.push({ tipo: "penalita", t: ct.t, peso: R.punti ? 20 : R.giri ? 20 : 15, txt: `A ${T(ct.t)} contatto con ${altra}, colpa tua: ${R.punti ? "un punto in più" : R.giri ? "due giri" : "15 s"} (lezioni 12-15).` }); }
    const bt = riv.segni.find(g => g.auto && g.label.startsWith("Boa toccata"));
    if (bt) F.push({ tipo: "penalita", t: bt.t, peso: 10, txt: `A ${T(bt.t)} hai toccato la boa: ${R.giri ? "un giro" : "una penalità"} (lezione 20).` });
    // bene
    const pesanti = F.filter(x => x.peso >= COA_MIN);
    if (!pesanti.length && me.fin !== null && !me.dsq){ const tot = Math.round(sp.lati.reduce((a, L) => a + (L.tu !== null ? Math.max(0, L.tu - L.ott) : 0), 0));
      return [{ tipo: "bene", t: o.taglio.t, peso: 0, s: tot, txt: `Regata quasi perfetta: in tutto ${tot} s dalla rotta ottimale.` }]; }
    return pesanti.sort((a, b) => b.peso - a.peso).slice(0, COA_N);
  }
  // 1.3.4: l'espressione del volto (regola di Ale del 15 novembre): contento se dice «quasi perfetta» o se nessuna frase pesa almeno COA_POCO s;
  // arrabbiato se c'è una penalità, la partenza anticipata o (1.3.6, aggiunta) una scuffia; serio negli altri casi. COA_POCO: ipotesi nostra. Volti fatti da Ale con ChatGPT (FONTI-PUBBLICHE F104)
  // 1.3.23 (voce 57; Ale, 17 nov: «arriva primo e il Coach non sorride»): contento anche col primo posto (con almeno un'altra barca in acqua) o col nuovo record
  // (R.recNuovo, da salvaArrivo), se non c'è niente da arrabbiato; prima non compariva mai (0 su 11 nelle regate del 15-17 nov)
  const COA_POCO = 10;
  function coaBravo(){ const me = R && R.boats[0]; if (!me || me.fin === null || me.dsq) return false;
    const primo = R.boats.length > 1 && !R.boats.some(b => !b.me && b.fin !== null && !b.dsq && b.fin < me.fin);
    return primo || !!R.recNuovo; }
  const coaUmore = (C, bravo) => C.some(x => x.tipo === "penalita" || x.tipo === "scuffia" || x.ocs) ? "arrabbiato" : bravo || C.some(x => x.tipo === "bene") || C.every(x => x.peso < COA_POCO) ? "contento" : "serio";
  function coaMostra(){
    const C = rot.res && rot.res.coach; $("coach").hidden = !C || !C.length;
    if (!C || !C.length) return;
    const u = coaUmore(C, coaBravo()), im = $("coachVolto"); im.hidden = false; /* 1.3.12: un caricamento fallito lo nascondeva per tutta la sessione */ im.src = "img/coach-" + u + ".jpg"; im.alt = "Il Coach, " + u; im.dataset.umore = u;
    $("coachFrasi").innerHTML = C.map((x, k) => `<li><button class="linkish" data-k="${k}" title="Vai a ${rivTempo(x.t)}">${x.txt}</button></li>`).join("");
  }
  $("coachFrasi").onclick = e => { const b = e.target.closest("button[data-k]"); if (!b || !riv.on || !rot.res || !rot.res.coach) return;
    riv.pos = rivPosDi(rot.res.coach[+b.dataset.k].t - COA_ANT); riv.playing = true; rivMostra();
    if (modo === "carriera" && !progress.coachVisto){ progress.coachVisto = true; saveProgress(); } }; // 1.3.5: un momento rivisto col coach (Esperienza di Deriva)

  // ---- coach in regata (1.3.28, voce 65, docs/PROPOSTA-COACH-IN-REGATA.md; idea e via di Ale del 20 novembre 2026: «se acceso, suggerisce cosa sarebbe meglio fare») ----
  // Solo nelle regate di Deriva (R.r1516: torneo, stagione, finale, regate di Deriva; non negli esercizi), con opt.coachReg. Un volto e una frase in alto a sinistra sul mare,
  // per CR_BASE + caratteri/CR_LETTURA s (8-14); al più un commento ogni CR_PAUSA s, tranne partenza anticipata e penalità. Dice solo cose che il gioco sa adesso. Legge lo stato della regata e non lo cambia,
  // senza numeri a caso: la regata è identica col Coach acceso o spento (P4). Ogni commento va nel file della regata come riga «C». Soglie: ipotesi nostre
  const CR_OGNI = 0.25, CR_BASE = 5, CR_LETTURA = 15, CR_DMIN = 8, CR_DMAX = 14, CR_MIN_VISTO = 4, CR_PAUSA = 30, CR_COP = 8, CR_SCARSO = 7, CR_SCARSO_T = 8, CR_BOA_LONTANA = 80, CR_DIST = 10, CR_W = 330;
  const crImg = {};
  const crVolto = u => crImg[u] || (crImg[u] = Object.assign(new Image(), { src: "img/coach-" + u + ".jpg" }));
  const crNome = b => (FLEET_LOOK.some(l => l.name === b.name) ? "la " : "") + (b.etich || b.name);
  const crAttivo = () => !!(opt.coachReg && R && R.r1516 && !R.es);
  function crDi(umore, testo, forza){
    const c = R.cr; if (!forza && R.t - c.ult < CR_PAUSA) return false;
    /* 1.3.32 (voce 68): un commento forzato non cancella quello in corso prima di CR_MIN_VISTO s: resta in coda (l'ultimo) e compare appena possono passare */
    if (forza && c.cur && R.t - c.cur.t0 < CR_MIN_VISTO && R.t - c.cur.t0 >= 0){ c.coda = { umore, testo }; return true; }
    c.ult = R.t; c.cur = { t0: R.t, umore, testo, dur: Math.min(CR_DMAX, Math.max(CR_DMIN, CR_BASE + testo.length / CR_LETTURA)) }; c.log.push({ t: +R.t.toFixed(2), umore, testo });
    if (typeof suona === "function") suona("campanello"); /* 1.3.34: campanello leggerissimo quando compare il Coach */
    if (typeof ses !== "undefined" && ses.on) sesLine("C " + sesT() + " " + umore + " " + testo);
    return true;
  }
  function crAggiorna(dt){
    if (!crAttivo()) return;
    const me = R.boats[0], c = R.cr || (R.cr = { ult: -1e9, cur: null, log: [], part: false, cop: 0, sc: 0, leg: 0, pos: null, need: R.need || 0, done: R.done || 0, pp: 0, pen: 0, vicino: false, sponsor: false });
    if (c.coda && c.cur && R.t - c.cur.t0 >= CR_MIN_VISTO){ const q = c.coda; c.coda = null; crDi(q.umore, q.testo, true); }
    if (me.fin !== null || me.dnf) return;
    /* 1.3.38 (voce 74, passo 2 a): lo storico dei rivali, una volta per regata da STO_T s; se il Coach ha appena parlato riprova, ma solo prima del via */
    if (!c.sto && R.tor && tor && R.t >= STO_T){ const f = stoFrase(tor); if (!f || R.t >= 0 || crDi("serio", f)) c.sto = true; }
    if (!c.sponsor && R.tor && R.t >= -50){ /* l'obiettivo dello sponsor, nelle tappe della stagione in carriera */
      const D = modo === "carriera" && progress.sponsor && progress.sponsor.c, S = progress.stagione;
      /* 1.3.38: se il Coach ha appena parlato (la frase dello storico con la preparazione da 1 minuto) riprova, ma solo prima del via; prima andava persa */
      c.sponsor = !(D && S && tor && tor.st !== undefined && stNaz(S) === (D.circ === "naz")) || R.t >= 0 || crDi("serio", "Per lo sponsor: " + D.ob.map(x => spTesto(x)).join(" e ") + ". Ogni regata conta."); }
    // penalità: sempre (forza), anche prima del via
    if ((R.need || 0) > c.need){ crDi("arrabbiato", "Penalità: fai i giri subito, lontano dalle altre barche, ognuno con una virata e una strambata (lezione 20).", true); }
    if ((R.done || 0) > c.done && (R.done || 0) >= (R.need || 0) && (R.need || 0) > 0){ crDi("contento", "Giri fatti: ora riparti e riprendi velocità.", true); }
    if ((me.pp || 0) > c.pp) crDi("arrabbiato", "Contatto con colpa: un punto in più. Ripassa chi ha la precedenza (lezioni 12-15).", true);
    if ((me.pen || 0) > c.pen) crDi("arrabbiato", "Contatto con colpa: " + Math.round(me.pen - c.pen) + " s di penalità. Ripassa chi ha la precedenza (lezioni 12-15).", true);
    c.need = R.need || 0; c.done = R.done || 0; c.pp = me.pp || 0; c.pen = me.pen || 0;
    if (!c.part && R.t >= 0){
      if (me.ocs){ c.part = true; crDi("arrabbiato", "Sei partito prima del via: torna dietro la linea e riparti (lezione 17).", true); }
      else if (me.leg >= 1){ c.part = true; const tl = me.tLinea ?? R.t;
        if (tl <= 3) crDi("contento", "Bella partenza: sulla linea allo sparo. Ora cerca vento libero.");
        else if (tl >= 10) crDi("serio", "Partenza in ritardo: non restare dietro alle altre, cerca vento libero (lezione 18)."); }
      else if (R.t > 10 && !me.ocs){ c.part = true; crDi("serio", "Sei ancora dietro la linea: taglia subito, dal punto più libero."); } }
    if (R.t < 0) return;
    if ((c.acc = (c.acc || 0) + dt) < CR_OGNI) return; dt = c.acc; c.acc = 0; /* il resto 4 volte al secondo (P6: a ogni passo costava il 4-14% della simulazione) */
    if (me.leg < 1) return;
    const w = windAt(me.S.x, me.S.y), a = norm180(w.twd - me.S.h), bolina = Math.abs(a) >= 30 && Math.abs(a) <= 75 && !S.capsized;
    // cono d'ombra
    if (R.ombra && bolina && (me.cop || 0) > 0.10 && me.copDa){ /* c.cop: secondi di copertura di fila; -1 = già detto per questa copertura */
      if (c.cop >= 0){ c.cop += dt; const n = crNome(me.copDa);
        if (c.cop >= CR_COP && crDi("serio", "Sei nel cono d'ombra " + (n.startsWith("la ") ? "del" + n.slice(1) : "di " + n) + ": vira o poggia per avere vento libero.")){ c.cop = -1; c.copDa = me.copDa; } } }
    else c.cop = 0;
    // scarso: lontano dalla boa, di bolina
    const g = R.marks[me.leg - 1], lontana = g ? Math.hypot(g.x - me.S.x, g.y - me.S.y) > CR_BOA_LONTANA : false;
    const sc = -Math.sign(a) * norm180(w.twd - env.twd);
    if (bolina && lontana && sc >= CR_SCARSO){ c.sc += dt; if (c.sc >= CR_SCARSO_T && crDi("serio", "Il vento ti è scarso di " + Math.round(sc) + "°: se oscilla, conviene virare; se continua a girare dalla stessa parte, no (lezione 11).")) c.sc = -60; }
    else if (c.sc > 0) c.sc = 0; else if (c.sc < 0) c.sc = Math.min(0, c.sc + dt);
    // boa girata: posizioni
    const pos = ranking().indexOf(me) + 1;
    if (c.pos === null) c.pos = pos;
    if (me.leg > c.leg){ if (c.leg >= 1){ const d = c.pos - pos;
        if (d > 0) crDi("contento", "Boa girata: hai guadagnato " + (d === 1 ? "un posto" : d + " posti") + ", sei " + pos + "°. Ora difendi: resta fra gli avversari e la prossima boa.");
        else if (d < 0) crDi("serio", "Alla boa hai perso " + (-d === 1 ? "un posto" : -d + " posti") + ": sei " + pos + "°. Nel prossimo lato cerca vento libero."); }
      c.leg = me.leg; c.pos = pos; }
    // ultimo lato: la barca davanti vicina
    if (!c.vicino && me.leg === R.marks.length + 1){ const dav = R.boats.filter(b => !b.me && b.fin === null && !b.dnf).map(b => [b, distacco(b)]).filter(([, s]) => s !== null && s >= 1 && s <= CR_DIST).sort((x, y) => x[1] - y[1])[0];
      if (dav){ c.vicino = true; const n = crNome(dav[0]); crDi("contento", n.charAt(0).toUpperCase() + n.slice(1) + " è a " + Math.round(dav[1]) + " s davanti a te: puoi superare quella barca, ogni manovra conta."); /* 1.3.31: neutra (prima «puoi prenderla», sbagliata per i rivali uomini) */ } }
  }
  function crDisegna(){
    R && (R.crRect = null); if (!crAttivo() || !R.cr || !R.cr.cur) return;
    const c = R.cr.cur, eta = R.t - c.t0; if (eta > c.dur || eta < 0) return;
    const alfa = Math.min(1, (c.dur - eta) / 0.8, eta / 0.3 + 0.2), pad = 8, F = 48, x = RQ_X, y = R.rqRect ? R.rqRect[1] + R.rqRect[3] + 8 : RQ_YS;
    ctx.save(); ctx.globalAlpha = alfa; ctx.font = font(600, 14);
    const parole = c.testo.split(" "), righe = []; let r = "";
    for (const p of parole){ const t = r ? r + " " + p : p; if (ctx.measureText(t).width > CR_W - F - 3 * pad && r){ righe.push(r); r = p; } else r = t; }
    if (r) righe.push(r);
    const h = Math.max(F + 2 * pad, righe.length * 19 + 2 * pad), w = CR_W;
    rqSfondo(x, y, w, h, false);
    const im = crVolto(c.umore); if (im.complete && im.naturalWidth) ctx.drawImage(im, x + pad, y + pad, F, F);
    ctx.fillStyle = "#FFFFFF"; ctx.textAlign = "left"; ctx.textBaseline = "middle";
    righe.forEach((t, k) => ctx.fillText(t, x + 2 * pad + F, y + pad + 10 + k * 19));
    ctx.restore(); R.crRect = [x, y, w, h];
  }

  // ---- schermata ----
  function rotTesto(ott, sp){ // 1.3.3: solo la legenda e i tempi; il commento lo fa il coach (coaFrasi)
    const me = R.boats[0], fmt = s => rivTempo(s), tu = me.fin !== null && !me.dsq ? me.fin - rot.barche[0].taglio.t : null, ot = ott.tempo - ott.t0;
    const A = rot.res && rot.res.ass;
    const lati = sp.lati.filter(L => L.tu !== null).map(L => L.nome.toLowerCase() + " " + (L.tu - L.ott >= 0 ? "+" : "−") + Math.round(Math.abs(L.tu - L.ott)) + " s").join(", ");
    let t = "Verde la rotta ottimale (col senno di poi, senza le altre barche), blu la tua" + (A ? ", viola la migliore in assoluto" : "") + "; i fili bianchi ogni minuto; gialle le layline. Dal tuo taglio della linea: rotta ottimale " + fmt(ot) + (tu !== null ? ", tu " + fmt(tu) + " (" + lati + ")." : ".");
    if (A){ const persa = ott.tempo - A.tempo; // 1.2.40: tempi dallo sparo
      t += ` Partenza ideale (migliore in assoluto): a ${Math.round(LINE_HALF + A.dx)} m dallo spillo, mure a ${A.mure > 0 ? "dritta" : "sinistra"}, ${fmt(A.tempo)} dallo sparo; in partenza ${persa >= 0.5 ? "hai perso " + Math.round(persa) + " s" : "non hai perso niente"}.`;
    }
    return t;
  }
  function rotApri(){
    if (!R || !R.rotta || riv.on) return;
    if (!rot.res){ const ott = rotCalcola(0); rot.res = ott ? { ott, sp: rotSpiega(ott) } : { ott: null, testo: "La rotta ottimale non si può calcolare per questa regata (manca il taglio della linea o l'arrivo)." };
      if (ott){ rot.res.testo = rotTesto(ott, rot.res.sp); rot.res.coach = coaFrasi(ott, rot.res.sp);
        regCoach(R, rot.res.coach, rot.res.coach.length ? coaUmore(rot.res.coach, coaBravo()) : "nessuno", rot.res.testo); /* 1.3.14: le frasi del Coach nel file della regata */ } }
    $("movAss").hidden = !rot.res.ott || rot.res.ass !== undefined; $("movAss").disabled = !!rot.calc; // 1.2.40: la migliore in assoluto solo a richiesta (tasto V), una volta per regata
    rot.on = true; rot.box = null; rivApri(); $("movTit").textContent = rot.res.testo; coaMostra();
    $("movLargo").hidden = !rot.res.ott; rotLargo(false);
  }
  // 1.2.40 (Ale, 15 novembre: «si potrebbe avere anche un tasto "vuoi la rotta" e si evita di aspettare»): il calcolo costa 3-4 s, quindi parte solo
  // dal pulsante o dal tasto V; prima si scrive che si sta calcolando (il setTimeout lascia al browser il tempo di mostrarlo). rot.res.ass: undefined = non
  // chiesta, null = non calcolabile
  function rotAssChiedi(){
    if (!rot.on || !rot.res || !rot.res.ott || rot.res.ass !== undefined || rot.calc) return;
    const r = rot.res, ASS = "Migliore in assoluto (V)"; rot.calc = true; $("movAss").disabled = true; $("movAss").textContent = "Sto calcolando…"; // 1.2.41: anche sul pulsante, perché con B il commento è nascosto
    r.testo = $("movTit").textContent = "Sto calcolando la migliore in assoluto: qualche secondo…"; // nel testo della rotta: la moviola lo riscrive a ogni fotogramma (rivMostra)
    setTimeout(() => { $("movAss").textContent = ASS; if (rot.res !== r){ rot.calc = false; return; } // un'altra regata nel frattempo
      r.ass = rotAssoluta(); rot.calc = false; rot.box = null;
      r.testo = rotTesto(r.ott, r.sp) + (r.ass ? "" : " La migliore in assoluto non si può calcolare per questa regata.");
      $("movAss").hidden = true; $("movAss").disabled = false; if (rot.on) $("movTit").textContent = r.testo; }, 60);
  }
  // 1.2.32 (docs/PROPOSTA-ROTTA-LEGGIBILE.md): la barra laterale del gioco si nasconde (pulsante o B) e la mappa prende tutta la finestra;
  // torna sempre quando la rotta ottimale si chiude (rivChiudi)
  function rotLargo(on){
    rot.largo = !!on; document.querySelector(".layout").classList.toggle("largo", rot.largo);
    $("movLargo").textContent = rot.largo ? "Rimetti testo e barra (B)" : "Allarga la mappa (B)"; // 1.2.41: con B si toglie anche il commento
    dispatchEvent(new Event("resize"));
  }
  // 1.2.32: il filo dello stesso istante, ogni ROT_FILO s dal tuo taglio della linea, finché esistono tutte e due le rotte
  const ROT_FILO = 60; // secondi, scelta nostra di sola grafica
  function rotFili(){
    if (!rot.res || !rot.res.ott) return [];
    const P = rot.res.ott.punti, tu = riv.all.filter(f => f.t >= rot.barche[0].taglio.t), out = [];
    if (!tu.length) return out;
    const fine = Math.min(P[P.length - 1].t, tu[tu.length - 1].t);
    for (let s = P[0].t + ROT_FILO; s <= fine; s += ROT_FILO){
      const q = rotIstante(P, s, q => [q.x, q.y]), f = rotIstante(tu, s, f => f.b[0]);
      if (q && f) out.push({ s: s - P[0].t, v: { x: q[0], y: q[1], t: s }, b: { x: f[0], y: f[1], t: s } });
    }
    return out;
  }
  // la posizione all'istante T fra i due punti vicini (i punti della rotta ottimale sono circa uno al secondo: senza, il filo univa istanti diversi fino a 1 s)
  function rotIstante(A, T, xy){
    let lo = 0, hi = A.length - 1; if (!A.length || T < A[0].t || T > A[hi].t) return null;
    while (hi - lo > 1){ const m = (lo + hi) >> 1; if (A[m].t <= T) lo = m; else hi = m; }
    const a = xy(A[lo]), b = xy(A[hi]), f = A[hi].t > A[lo].t ? (T - A[lo].t) / (A[hi].t - A[lo].t) : 0;
    return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
  }
  function rotEtichette(v){ // il tempo accanto al punto verde di ogni filo, in coordinate schermo
    if (!rot.on || !riv.on || !rot.res || !rot.res.ott) return;
    ctx.save(); ctx.font = font(600, 11); ctx.textAlign = "left"; ctx.textBaseline = "middle";
    for (const F of rotFili()){ const [x, y] = toScreen(v, F.v.x, F.v.y), m = Math.round(F.s / 60) + ":00";
      ctx.fillStyle = "rgba(0,0,0,.45)"; ctx.fillText(m, x + 7, y + 1); ctx.fillStyle = "rgba(170,240,180,1)"; ctx.fillText(m, x + 6, y); }
    ctx.restore();
  }
  function rotVista(){ // la vista dall'alto, nord in su, che contiene campo e tracce, sopra la barra della moviola; null se la rotta non è aperta
    if (!rot.on || !riv.on || !rot.res || !rot.res.ott) return null;
    if (!rot.box){ const P = rot.res.ott.punti.concat(rot.res.ass ? rot.res.ass.punti : []).map(q => [q.x, q.y]).concat(riv.all.map(f => [f.b[0][0], f.b[0][1]]), R.marks.map(m => [m.x, m.y]), [[R.pin.x, R.pin.y], [R.cb.x, R.cb.y]]);
      const xs = P.map(p => p[0]), ys = P.map(p => p[1]); rot.box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; }
    const [x0, y0, x1, y1] = rot.box, alto = H - $("movBar").offsetHeight - 50, /* 1.2.41: senza orologio in alto, la mappa parte da 20 px invece che da 90 */ ppm = Math.min((W - 60) / Math.max(10, x1 - x0), (alto - 40) / Math.max(10, y1 - y0));
    return { ppm, rot: 0, cx: W / 2 + (S.x - (x0 + x1) / 2) * ppm, cy: 20 + alto / 2 + (S.y - (y0 + y1) / 2) * ppm };
  }
  function rotDisegna(v){ // sopra la regata, mentre la moviola è aperta dalla rotta ottimale
    if (!rot.on || !riv.on || !rot.res || !rot.res.ott) return;
    const P = rot.res.ott.punti, T = rivT0() + riv.pos, lw = Math.max(0.25, 1.6 / v.ppm);
    const A = rot.res.ass; // 1.2.40: la migliore in assoluto, viola, sotto le altre; segno nel punto ideale della linea e freccia della direzione
    if (A){ const VI = "rgba(200,120,255,", Q = A.punti, pt = (x, y, r) => { ctx.fillStyle = VI + "1)"; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); };
      ctx.lineWidth = lw; ctx.strokeStyle = VI + ".9)"; ctx.beginPath(); Q.forEach((q, i) => i ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y)); ctx.stroke();
      for (let s = 30; s < Q[Q.length - 1].t; s += 30){ const q = rotIstante(Q, s, q => [q.x, q.y]); if (q) pt(q[0], q[1], 2.2 * lw); }
      const o = Q[0], L = 12, ux = Math.sin(A.dir), uy = -Math.cos(A.dir), ex = o.x + ux * L, ey = o.y + uy * L;
      pt(o.x, o.y, 4.5 * lw); ctx.lineWidth = 2 * lw; ctx.beginPath(); ctx.moveTo(o.x, o.y); ctx.lineTo(ex, ey);
      ctx.moveTo(ex - ux * 4 + uy * 3, ey - uy * 4 - ux * 3); ctx.lineTo(ex, ey); ctx.lineTo(ex - ux * 4 - uy * 3, ey - uy * 4 + ux * 3); ctx.stroke(); }
    ctx.lineWidth = lw; ctx.strokeStyle = "rgba(60,200,90,.9)"; ctx.beginPath(); P.forEach((q, i) => i ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y)); ctx.stroke();
    const tu = riv.all.filter(f => f.t >= rot.barche[0].taglio.t); ctx.strokeStyle = "rgba(80,150,255,.85)"; ctx.beginPath(); tu.forEach((f, i) => i ? ctx.lineTo(f.b[0][0], f.b[0][1]) : ctx.moveTo(f.b[0][0], f.b[0][1])); ctx.stroke();
    const punto = (x, y, r, c) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); };
    for (let s = P[0].t + 30; s < P[P.length - 1].t; s += 30){ const q = rotIstante(P, s, q => [q.x, q.y]); if (q) punto(q[0], q[1], 2.2 * lw, "rgba(60,200,90,1)"); const f = rotIstante(tu, s, f => f.b[0]); if (f) punto(f[0], f[1], 2.2 * lw, "rgba(80,150,255,1)"); } // 1.2.32: all'istante esatto, come i fili
    { const mk = R.marks[0], w = rotVento(mk.x, mk.y, rotRaffiche(Math.max(rot.reg[0].t, Math.min(T, rot.reg[rot.reg.length - 1].t)))), L = R.up * 1.3; // le layline col vento di adesso (layDir, come in acqua)
      ctx.strokeStyle = "rgba(255,230,120,.8)"; ctx.setLineDash([3 * lw, 3 * lw]);
      for (const dd of layDir(w)){ const d = dd * D2R; ctx.beginPath(); ctx.moveTo(mk.x, mk.y); ctx.lineTo(mk.x + Math.sin(d) * L, mk.y - Math.cos(d) * L); ctx.stroke(); }
      ctx.setLineDash([]); }
    ctx.strokeStyle = "rgba(255,255,255,.75)"; ctx.lineWidth = lw * 0.9; // 1.2.32: i fili dello stesso istante
    for (const F of rotFili()){ ctx.beginPath(); ctx.moveTo(F.v.x, F.v.y); ctx.lineTo(F.b.x, F.b.y); ctx.stroke(); }
    ctx.lineWidth = lw;
    if (T >= P[0].t){ const q = P.find(q => q.t >= T) || P[P.length - 1]; punto(q.x, q.y, 4 * lw, "rgba(60,200,90,.6)"); } // dove saresti adesso con la rotta ottimale
  }
  $("finRot").onclick = rotApri;
