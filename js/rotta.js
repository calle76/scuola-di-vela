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
  const rot = { reg: [], barche: [], acc: 0, res: null, on: false, spento: false };

  // ---- registrazione ----
  function rotReset(){ rot.reg = []; rot.barche = R ? R.boats.map(() => ({ taglio: null, giri: [] })) : []; rot.acc = 1e9; rot.res = null; rot.on = false; }
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
    let front = [Object.assign({ debt: 0, par: null, man: 0 }, p0)];
    const ox = p0.x, oy = p0.y, t0 = p0.t;
    for (let t = t0; t < t0 + ROT_LATO_MAX && t < ROT_TMAX; t += ROT_DT){
      const Q = rotRaffiche(t), best = new Map();
      for (const p of front){
        const w = rotVento(p.x, p.y, Q), riga = rotRiga(w.tws);
        for (let n = 0; n < ROT_TWA.length; n++) for (const s of [1, -1]){ const twa = ROT_TWA[n];
          let debt = p.debt, man = p.man;
          if (p.s && s !== p.s){ debt += twa < 90 ? T_VIR : T_ABB; man++; }
          const mv = Math.max(0, ROT_DT - debt); debt = Math.max(0, debt - ROT_DT);
          const [v, lee] = riga[n], c = (w.twd - s * (twa + lee)) * D2R; // s = +1: vento da destra, la prua sta a sinistra del vento
          const q = { x: p.x + Math.sin(c) * v * mv, y: p.y - Math.cos(c) * v * mv, s, t: t + ROT_DT, debt, man, par: p };
          const fr = cancello(p, q); if (fr !== null){ q.x = p.x + (q.x - p.x) * fr; q.y = p.y + (q.y - p.y) * fr; q.t = t + ROT_DT * fr; q.fine = true; return q; }
          const dx = q.x - ox, dy = q.y - oy, d = Math.hypot(dx, dy), key = Math.round(Math.atan2(dx, -dy) / D2R / ROT_SETT) * 2 + (s > 0 ? 1 : 0);
          const sc = d - debt * v, o = best.get(key); if (!o || sc > o.sc) best.set(key, { sc, q }); // chi deve ancora finire una manovra vale meno
        }
      }
      front = [...best.values()].map(o => o.q);
    }
    return null;
  }
  // cancello della boa: semiretta dalla boa verso mk.out, passata dal lato giusto (da a ≥ 0 ad a < 0, come roundCheck) ad almeno ROT_BOA m
  const rotCancBoa = mk => (p, q) => {
    const ux = Math.sin(mk.out * D2R), uy = -Math.cos(mk.out * D2R), cp = (p.x - mk.x) * uy - (p.y - mk.y) * ux, cq = (q.x - mk.x) * uy - (q.y - mk.y) * ux; // > 0: a destra della semiretta guardando lungo out
    if (!(cp <= 0 && cq > 0) && !(cp < 0 && cq >= 0)) return null; // roundCheck: da bearing-out ≥ 0 (a destra, prodotto < 0 qui) a < 0
    const f = cp / (cp - cq), ax = p.x + (q.x - p.x) * f - mk.x, ay = p.y + (q.y - p.y) * f - mk.y;
    return ax * ux + ay * uy >= ROT_BOA ? f : null;
  };
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
          if (!vicino){ motivi.push({ j, peso: L.tu - L.ott + 1, txt: `A ${rivTempo(q.t)} il vento è girato di ${Math.round(Math.abs(d))}° contro le tue mure: la rotta ottimale ha virato, tu no.` }); break; } } }
      // layline: l'ultima virata per la boa oltre la layline, oppure più virate vicino alla boa
      if (L.nome === "Bolina" && tu.length > 10){ const mk = R.marks[0], vir = [];
        for (let n = 5; n < tu.length; n += 5){ const f = tu[n], g = tu[n - 5]; if (mure(f.x, f.y, f.h, f.t) !== mure(g.x, g.y, g.h, g.t)) vir.push(f); }
        const ul = vir[vir.length - 1], o2 = ul ? rotOltre(mk, ul.x, ul.y, ul.t) : null, oltreM = o2 ? o2.d * Math.sin(Math.max(0, o2.g) * D2R) : 0;
        const vicine = vir.filter(f => Math.hypot(f.x - mk.x, f.y - mk.y) < LAY_VICINO).length;
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

  // ---- schermata ----
  function rotTesto(ott, sp){
    const me = R.boats[0], fmt = s => rivTempo(s), tu = me.fin !== null && !me.dsq ? me.fin - rot.barche[0].taglio.t : null, ot = ott.tempo - ott.t0;
    let t = `In verde la rotta ottimale (col senno di poi), in blu la tua; un punto ogni 30 s; ogni minuto un filo bianco unisce dove eri tu e dove saresti stato con la rotta ottimale nello stesso istante; tratteggiate in giallo le layline della boa di bolina col vento di quel momento. Rotta ottimale ${fmt(ot)} dal tuo taglio della linea` + (tu !== null ? `, tu ${fmt(tu)} (${tu - ot >= 0 ? "+" : "−"}${Math.round(Math.abs(tu - ot))} s). ` : ". ");
    t += sp.lati.filter(L => L.tu !== null).map(L => `${L.nome} ${L.tu - L.ott >= 0 ? "+" : "−"}${Math.round(Math.abs(L.tu - L.ott))} s`).join(", ") + ".";
    if (sp.motivi.length) t += " " + sp.motivi.map(m => m.txt).join(" ");
    return t + " Conosce il vento prima che arrivi e ignora le altre barche.";
  }
  function rotApri(){
    if (!R || !R.rotta || riv.on) return;
    if (!rot.res){ const ott = rotCalcola(0); rot.res = ott ? { ott, testo: rotTesto(ott, rotSpiega(ott)) } : { ott: null, testo: "La rotta ottimale non si può calcolare per questa regata (manca il taglio della linea o l'arrivo)." }; }
    rot.on = true; rot.box = null; rivApri(); $("movTit").textContent = rot.res.testo;
    $("movLargo").hidden = !rot.res.ott; rotLargo(false);
  }
  // 1.2.32 (docs/PROPOSTA-ROTTA-LEGGIBILE.md): la barra laterale del gioco si nasconde (pulsante o B) e la mappa prende tutta la finestra;
  // torna sempre quando la rotta ottimale si chiude (rivChiudi)
  function rotLargo(on){
    rot.largo = !!on; document.querySelector(".layout").classList.toggle("largo", rot.largo);
    $("movLargo").textContent = rot.largo ? "Rimetti la barra (B)" : "Allarga la mappa (B)";
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
    if (!rot.box){ const P = rot.res.ott.punti.map(q => [q.x, q.y]).concat(riv.all.map(f => [f.b[0][0], f.b[0][1]]), R.marks.map(m => [m.x, m.y]), [[R.pin.x, R.pin.y], [R.cb.x, R.cb.y]]);
      const xs = P.map(p => p[0]), ys = P.map(p => p[1]); rot.box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; }
    const [x0, y0, x1, y1] = rot.box, alto = H - $("movBar").offsetHeight - 110, ppm = Math.min((W - 60) / Math.max(10, x1 - x0), (alto - 40) / Math.max(10, y1 - y0));
    return { ppm, rot: 0, cx: W / 2 + (S.x - (x0 + x1) / 2) * ppm, cy: 90 + alto / 2 + (S.y - (y0 + y1) / 2) * ppm };
  }
  function rotDisegna(v){ // sopra la regata, mentre la moviola è aperta dalla rotta ottimale
    if (!rot.on || !riv.on || !rot.res || !rot.res.ott) return;
    const P = rot.res.ott.punti, T = rivT0() + riv.pos, lw = Math.max(0.25, 1.6 / v.ppm);
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
