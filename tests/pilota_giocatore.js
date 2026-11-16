// Pilota «da giocatore» per i collaudi (docs/PROPOSTA-PILOTA-GIOCATORE.md, via di Ale il 16 novembre 2026). NON è nel gioco: il collaudo
// consegna questo testo alla pagina (page.evaluate) dopo il caricamento, e lui si mette al posto di __sv.pilota. Il pilota di prima resta in
// __sv.pilotaVecchio. Usa la guida dei rivali (aiControl) come il pilota di prima, ma:
//   1. numeri degli esperti fissi, al centro della fascia, vela senza errore;
//   2. bolina a due bordi: niente cambi di bordo a tempo, si vira sulla layline con lo scarroccio (LAY_MARG acceso solo durante la sua chiamata);
//   3. aria libera: OMBRA_S secondi nel cono (almeno il 10% di vento in meno) e più di LAY_M metri di bordo ancora da fare: vira via;
//   4. lasca da HEEL gradi di sbandamento (la guida dei rivali lasca da 22);
//   5. fa i giri di penalità dovuti, con la sequenza dei rivali (il pilota di prima non li fa e arriva squalificato).
// Errori a comando (opts): tardi = secondi di ritardo al via; oltre = metri oltre la layline prima di virare; doppia = due virate vicino alla boa 1.
// Tutte le costanti sono ipotesi nostre (§4 della proposta) e nessuna entra nel gioco.
(opts) => {
  const P = Object.assign({ ombraS: 5, layM: 60, heel: 18, marg: 2, tardi: 0, oltre: 0, doppia: false, pausa: 15, giroA: 120, partenza: 0 }, opts || {});
  if (!__sv.pilotaVecchio) __sv.pilotaVecchio = __sv.pilota;
  const UP = 46.5, DOWN = 152.5;
  __sv.pg = { P, virateVia: 0, oltreFatti: 0, doppie: 0 };
  __sv.pilota = dt => {
    const me = R.boats[0];
    if (!me.ai){
      Object.assign(me, { ai: { up: UP, down: DOWN, trim: 0, gain: 18, boardMin: 35, boardMax: 90, react: 5, startM: 0.5 }, side: 1, boardT: 0, boardMax: 40, rOff: 0, char: "normale",
        startX: toWF(S.x, S.y)[0] * 0.5, capW: 0, pg: { cono: 0, tVia: -1e9, legScelto: -1, oltre: null, doppia: null, doppiaFatta: false } });
      __sv.pg.virateVia = __sv.pg.oltreFatti = __sv.pg.doppie = 0;
    }
    if (S.capsized){ me.capW += dt; if (me.capW >= 1) rightBoat(); return ctl.tiller; }
    me.capW = 0; me.info = info; me.me = false;
    if (P.partenza){ const pr = me.leg < 1; if (pr !== me.pg.pr){ me.pg.pr = pr; Object.assign(me.ai, pr ? { up: 51.5, gain: 26, react: 3, startM: 1.5 } : { up: UP, gain: 18, react: 5, startM: 0.5 }); } } /* prova: fino al taglio della linea i numeri dei principianti (centro fascia) */
    const st = me.pg, w = windAt(S.x, S.y), twd = w.twd, inGara = me.leg >= 1 && me.fin === null && R.t >= 0;
    let marg = P.marg, forzata = null;
    if (inGara){
      const tgt = targetOf(me), brg = bearingTo(S, tgt), rel = norm180(brg - twd), d = Math.hypot(tgt.x - S.x, tgt.y - S.y);
      const lee = layLee(w.tws, UP), cono = UP + lee + P.marg, bolina = Math.abs(rel) < cono;
      me.boardMax = 1e9; /* regola 2: mai un cambio di bordo a tempo */
      if (bolina){
        if (st.legScelto !== me.leg && d > 30){ /* regola 2: il primo bordo è quello che avvicina di più alla boa (scelto una volta per lato) */
          st.legScelto = me.leg;
          const best = Math.abs(norm180(twd - UP - brg)) < Math.abs(norm180(twd + UP - brg)) ? 1 : -1;
          if (best !== me.side && Math.abs(Math.abs(norm180(twd - UP - brg)) - Math.abs(norm180(twd + UP - brg))) > 10){ me.side = best; me.boardT = 0; }
        }
        /* regola 3: metri di questo bordo ancora da fare prima della layline dell'altro (triangolo: prua di adesso, prua dopo la virata) */
        const c1 = -me.side * UP, c2 = me.side * (UP + lee), resta = d * Math.sin(Math.abs(norm180(c2 - rel)) * Math.PI / 180) / Math.sin(Math.abs(norm180(c2 - c1)) * Math.PI / 180);
        let q = 0; for (const a of R.boats){ if (a !== me) q = Math.max(q, ombraDi(a, S.x, S.y)); }
        st.cono = q >= 0.10 ? st.cono + dt : 0;
        if (st.cono > P.ombraS && resta > P.layM && d > 30 && R.t - st.tVia > P.pausa){ me.side = -me.side; me.boardT = 0; st.cono = 0; st.tVia = R.t; __sv.pg.virateVia++; }
      } else st.cono = 0;
      /* errore «oltre»: arrivato sulla layline del primo lato di bolina, tiene il bordo per altri P.oltre metri */
      if (P.oltre > 0 && me.leg === 1){
        const altra = sgn(norm180(twd - brg)) !== sgn(norm180(twd - S.h)), sulla = !bolina && altra && Math.abs(rel) < 90;
        if (st.oltre === null && sulla) st.oltre = { x: S.x, y: S.y };
        if (st.oltre && st.oltre !== "fatto"){
          if (Math.hypot(S.x - st.oltre.x, S.y - st.oltre.y) < P.oltre) marg = 80; /* cono larghissimo: la guida resta sul bordo */
          else { st.oltre = "fatto"; __sv.pg.oltreFatti++; }
        }
      }
      /* errore «doppia»: a meno di 40 m dalla boa 1 vira sull'altro bordo per 7 s e poi torna (due virate in più vicino alla boa) */
      if (P.doppia && me.leg === 1 && !st.doppiaFatta && d < 40 && d > 22){ st.doppiaFatta = true; st.doppia = { t: R.t, lato: -sgn(norm180(twd - S.h)) }; __sv.pg.doppie++; }
      if (st.doppia && R.t - st.doppia.t < 7) forzata = twd - st.doppia.lato * UP; else st.doppia = null;
    } else me.boardMax = 40;
    /* giri di penalità: la sequenza dei rivali (giroAI), col debito del giocatore (R.need - R.done); un giro in più nel conto perché a chiudere sia il conto del gioco, non quello dei rivali */
    if (R.giri){ const deb = R.need - R.done; me.gDebt = deb > 0 ? deb + 1 : 0; if (deb <= 0) me.gV = 0; }
    const prima = LAY_MARG; LAY_MARG = inGara ? marg : prima;
    /* errore «tardi»: finché non ha tagliato la linea, la guida crede che lo sparo sia P.tardi secondi dopo (l'orologio del gioco torna subito com'era) */
    const tVero = R.t, barra = ctl.tiller; if (P.tardi > 0 && me.leg === 0) R.t = tVero - P.tardi;
    try { aiControl(me, dt); } finally { LAY_MARG = prima; me.me = true; R.t = tVero; }
    if (forzata !== null){ ctl.tiller = barra; muoviTimone(ctl, S, forzata, me.ai, dt); }
    if (me.gCum != null && Math.abs(norm180(twd - S.h)) > P.giroA) ctl.sheet = Math.min(ctl.sheet, 0.42); /* nei giri la strambata si fa a vela chiusa (la guida la chiude solo oltre 158°, e la barca scuffiava) */
    if (S.heel > P.heel && S.heel <= 22) ctl.sheet = Math.min(1, ctl.sheet + 0.2 * Math.min(1, dt * 3)); /* regola 4: lasca prima */
    return ctl.tiller;
  };
  return true;
}
