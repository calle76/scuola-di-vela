// Scuola di vela, suoni.js — Suoni del gioco (dalla 1.2.5, docs/PROPOSTA-SUONI.md): generati dal browser (Web Audio); dalla 1.2.7 acqua e vela registrate (js/suoni-dati.js, PROPOSTA-SUONI-REGISTRATI.md); dalla 1.2.9 anche vento, sciabordio, sartiame, gorgoglio, gabbiani, scricchiolii (PROPOSTA-SUONI-FINE.md). Legge lo stato del gioco e non lo tocca.
// Non chiama la simulazione e non usa Math.random (ha un generatore suo): le regate a seme fisso restano identiche con i suoni accesi o spenti.
  // ======================================================================
  // SUONI
  // ======================================================================
  // ---- impostazione e stato ----
  // Livelli: volume generale; ipotesi nostre, da regolare a orecchio. All'inizio «basso» (Ale, 2 novembre 2026).
  const SUONI_KEY = "scuolaVelaSuoni", SUONI_LIV = { spento: 0, basso: 0.22, medio: 0.45, alto: 0.6 };
  let suoniLiv = "basso";
  try { const v = localStorage.getItem(SUONI_KEY); if (v && v in SUONI_LIV) suoniLiv = v; } catch(e){}
  let actx = null, sMaster = null, sCh = null; // contesto audio, volume generale, catene dei suoni continui
  const suoniReg = [];                         // registro degli eventi suonati, [istante di simulazione, nome, tempo di regata]: lo leggono i collaudi
  const suoniVal = { vento: 0, acqua: 0, vela: 0, acquaVel: 1, acquaFiltro: 0, ritmo: 0, colpi: 0 }; // suoni continui all'ultimo fotogramma (anche senza audio): per i collaudi
  // 1.2.7: acquaVel e acquaFiltro = velocità e filtro del giro d'acqua; ritmo = colpi di vela al secondo; colpi = colpi di vela partiti (anche a gioco muto)
  // 1.2.9: ventoVel, ventoFiltro, onde, sartiame, sartiameVel, gorgoglio = gli altri suoni continui; gabbiani, scricchioli = quanti ne sono partiti (anche a gioco muto)
  Object.assign(suoniVal, { ventoVel: 1, ventoFiltro: 0, onde: 0, sartiame: 0, sartiameVel: 1, gorgoglio: 0, gabbiani: 0, scricchioli: 0 });
  let suoniFonte = "sintetici";                // «registrati» quando acqua e colpi sono decodificati; finché no (o se la decodifica fallisce) restano i sintetici
  let sReg = null, sProssimo = 0;               // suoni registrati decodificati; tempo al prossimo colpo di vela (s di gioco)
  let sAmb = null, sAmbFonte = "attesa", sAmbMs = null; // 1.2.9: gli altri suoni registrati, decodificati dopo acqua e colpi; se la decodifica fallisce il vento resta sintetico e gli altri tacciono
  let sGabb = null, sScr = null;                // tempo al prossimo gabbiano e al prossimo scricchiolio (s di gioco)
  const suoniMuta = {};                         // solo per il collaudo che ascolta: { sartiame: true } spegne quel suono per confrontare con e senza
  const COLPI_VOL = 0.28 * 4;                   // volume dei colpi di vela col vento forte: 0,28 nella 1.2.7, ×4 (+12 dB) dalla 1.2.8 (Ale, 3 novembre 2026, ascoltando il gioco registrato)
  let sPrev = null, sFase = 0;
  let sSeme = 0x5EA;                           // generatore suo (mulberry32), solo per il fruscio
  const sRand = () => { sSeme = sSeme + 0x6D2B79F5 | 0; let t = Math.imul(sSeme ^ sSeme >>> 15, 1 | sSeme); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

  // ---- avvio: solo dopo il primo tasto o clic (lo chiede il browser) ----
  function suoniAvvia(){
    if (LAB || !SUONI_LIV[suoniLiv]) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return; // browser senza audio: il gioco resta muto
    if (!actx){
      try { actx = new AC(); } catch(e){ actx = null; return; }
      sMaster = actx.createGain(); sMaster.gain.value = SUONI_LIV[suoniLiv]; sMaster.connect(actx.destination);
      const buf = actx.createBuffer(1, actx.sampleRate * 2, actx.sampleRate), d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = sRand() * 2 - 1;
      const catena = (tipo, f, q) => { const src = actx.createBufferSource(); src.buffer = buf; src.loop = true; src.playbackRate.value = 0.8 + sRand() * 0.4;
        const fl = actx.createBiquadFilter(); fl.type = tipo; fl.frequency.value = f; fl.Q.value = q; const g = actx.createGain(); g.gain.value = 0;
        src.connect(fl); fl.connect(g); g.connect(sMaster); src.start(); return { fl, g }; };
      sCh = { vento: catena("bandpass", 400, 0.6), acqua: catena("lowpass", 500, 0.7), vela: catena("highpass", 900, 0.8) };
      sCh.buf = buf;
      suoniRegistrati();
    }
    if (actx.state === "suspended") actx.resume().catch(() => {});
  }
  // ---- suoni registrati (1.2.7): decodificati una volta, al primo avvio dell'audio ----
  const sDec = nome => new Promise((ok, no) => { try { const t = atob(SUONI_DATI.ogg[nome]), a = new Uint8Array(t.length); for (let i = 0; i < t.length; i++) a[i] = t.charCodeAt(i);
    const p = actx.decodeAudioData(a.buffer, ok, no); if (p && p.catch) p.catch(no); } catch(e){ no(e); } });
  function sGiro(buffer, f, inizio){ // un giro registrato senza fine, a volume 0: filtro passa-basso, volume e velocità li comanda suoniAgg
    const src = actx.createBufferSource(); src.buffer = buffer; src.loop = true;
    const fl = actx.createBiquadFilter(); fl.type = "lowpass"; fl.frequency.value = f; const g = actx.createGain(); g.gain.value = 0;
    src.connect(fl); fl.connect(g); g.connect(sMaster); src.start(0, inizio * buffer.duration); return { src, fl, g };
  }
  function suoniRegistrati(){
    if (typeof SUONI_DATI === "undefined" || !actx){ suoniFonte = "errore: dati mancanti"; return; }
    const t0 = performance.now(); suoniFonte = "decodifica";
    Promise.all([sDec("acqua"), sDec("colpi")]).then(([acqua, colpi]) => {
      sReg = Object.assign(sGiro(acqua, 1200, sRand()), { colpi, ms: performance.now() - t0 });
      sCh.acqua.g.gain.setTargetAtTime(0, actx.currentTime, 0.1);   // il fruscio sintetico dell'acqua tace: ora suona quello registrato
      suoniFonte = "registrati";
      suoniAmbiente();
    }).catch(e => { suoniFonte = "errore: " + (e && e.message || e); });
  }
  function suoniAmbiente(){ // 1.2.9: la seconda decodifica parte solo dopo la prima, che così resta veloce come prima
    const t0 = performance.now(), nomi = ["vento", "onde", "sartiame", "gorgoglio", "gabbiani", "scricchioli"]; sAmbFonte = "decodifica";
    Promise.all(nomi.map(sDec)).then(([vento, onde, sartiame, gorgoglio, gabbiani, scricchioli]) => {
      sAmb = { vento: sGiro(vento, 2000, sRand()), onde: sGiro(onde, 8000, sRand()), sartiame: sGiro(sartiame, 8000, sRand()), gorgoglio: sGiro(gorgoglio, 8000, sRand()), gabbiani, scricchioli };
      sCh.vento.g.gain.setTargetAtTime(0, actx.currentTime, 0.1);   // il fruscio sintetico del vento tace: ora suona quello registrato
      sAmbMs = performance.now() - t0; sAmbFonte = "registrati";
    }).catch(e => { sAmbFonte = "errore: " + (e && e.message || e); });
  }
  function sPezzo(buffer, voce, v, varia, pan){ // un ritaglio di un file registrato, una volta sola, con altezza a caso (±varia) e posizione stereo
    const src = actx.createBufferSource(); src.buffer = buffer; src.playbackRate.value = 1 - varia + sRand() * 2 * varia;
    const g = actx.createGain(); g.gain.value = v; src.connect(g); let out = g;
    if (pan && actx.createStereoPanner){ const sp = actx.createStereoPanner(); sp.pan.value = pan; g.connect(sp); out = sp; }
    out.connect(sMaster); src.start(actx.currentTime + 0.01, voce[0], voce[1]);
  }
  function sGabbiano(){ // ipotesi nostre: volume da 0,30 a 0,60, altezza ±6%, dovunque fra sinistra e destra
    suoniVal.gabbiani++; const L = SUONI_DATI.gabbiani, voce = L[Math.floor(sRand() * L.length)], v = 0.3 + sRand() * 0.3, pan = sRand() * 1.6 - 0.8;
    if (suoniAttivi() && sAmb && !suoniMuta.gabbiani) try { sPezzo(sAmb.gabbiani, voce, v, 0.06, pan); } catch(e){}
  }
  function sScricchiolio(heel){ // ipotesi nostre: più forte più la barca sbanda, altezza ±8%
    suoniVal.scricchioli++; const L = SUONI_DATI.scricchioli, voce = L[Math.floor(sRand() * L.length)], v = 0.4 + 0.4 * Math.min(1, Math.max(0, heel - 18) / 15);
    if (suoniAttivi() && sAmb && !suoniMuta.scricchioli) try { sPezzo(sAmb.scricchioli, voce, v, 0.08); } catch(e){}
  }
  function sColpo(v){   // un colpo di tela, scelto a caso: 7 volte su 10 forte; altezza ±5%, volume da -4 a +2 dB (ipotesi nostre)
    const C = SUONI_DATI.colpi, cerca = sRand() < 0.7 ? 1 : 0, lista = [];
    C.forti.forEach((f, i) => { if (f === cerca) lista.push(i); });
    const i = lista[Math.floor(sRand() * lista.length)], t = actx.currentTime + 0.01;
    const src = actx.createBufferSource(); src.buffer = sReg.colpi; src.playbackRate.value = 0.95 + sRand() * 0.1;
    const g = actx.createGain(); g.gain.value = v * Math.pow(10, (sRand() * 6 - 4) / 20);
    src.connect(g); g.connect(sMaster); src.start(t, i * C.spazio, C.lungo);
  }
  addEventListener("keydown", suoniAvvia); addEventListener("pointerdown", suoniAvvia);
  document.addEventListener("visibilitychange", () => { if (actx) (document.hidden ? actx.suspend() : actx.resume()).catch(() => {}); });
  function suoniImposta(v){
    if (!(v in SUONI_LIV)) return;
    suoniLiv = v; try { localStorage.setItem(SUONI_KEY, v); } catch(e){}
    if (sMaster) sMaster.gain.setTargetAtTime(SUONI_LIV[v], actx.currentTime, 0.05);
    if (SUONI_LIV[v]) suoniAvvia(); else if (actx) actx.suspend().catch(() => {});
  }
  { const sel = $("suoniSel"); if (sel){ sel.value = suoniLiv; sel.onchange = e => suoniImposta(e.target.value); } } // riga «Suoni» nelle impostazioni (⚙)
  const suoniAttivi = () => !!(actx && SUONI_LIV[suoniLiv] && actx.state === "running");

  // ---- suoni brevi (eventi) ----
  // Ogni evento va nel registro anche a gioco muto; il suono vero solo con l'audio acceso. Forme e numeri: ipotesi nostre, a orecchio.
  function sRumore(t0, dur, tipo, f, vol, attacco = 0.005){
    const src = actx.createBufferSource(); src.buffer = sCh.buf; src.playbackRate.value = 0.7 + sRand() * 0.6;
    const fl = actx.createBiquadFilter(); fl.type = tipo; fl.frequency.value = f; const g = actx.createGain();
    g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(vol, t0 + attacco); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    src.connect(fl); fl.connect(g); g.connect(sMaster); src.start(t0, sRand()); src.stop(t0 + dur + 0.05);
  }
  function sTono(t0, dur, onda, f, vol, f2 = f, attacco = 0.01, filtro = 0){
    const o = actx.createOscillator(); o.type = onda; o.frequency.setValueAtTime(f, t0); if (f2 !== f) o.frequency.exponentialRampToValueAtTime(f2, t0 + dur);
    const g = actx.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(vol, t0 + attacco); g.gain.setValueAtTime(vol, t0 + Math.max(attacco, dur - 0.08)); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    let out = o; if (filtro){ const fl = actx.createBiquadFilter(); fl.type = "lowpass"; fl.frequency.value = filtro; o.connect(fl); out = fl; }
    out.connect(g); g.connect(sMaster); o.start(t0); o.stop(t0 + dur + 0.05);
  }
  const SUONO = {
    virata:     k => { sRumore(k.t, 0.5, "bandpass", 700, 0.35, 0.08); sTono(k.t + 0.25, 0.18, "sine", 110, 0.25, 70); },
    strambata:  k => { sRumore(k.t, 0.25, "highpass", 1500, 0.4 + 0.4 * k.v); sTono(k.t, 0.25, "sine", 90, 0.5 + 0.4 * k.v, 55, 0.003); },
    scuffia:    k => { sTono(k.t, 0.3, "sine", 80, 0.6, 40, 0.003); sRumore(k.t + 0.05, 1.4, "lowpass", 1400, 0.6, 0.02); },
    raddrizzata: k => { sRumore(k.t, 1.2, "bandpass", 1800, 0.25, 0.1); },
    contatto:   k => { sTono(k.t, 0.25, "sine", 65, 0.8, 45, 0.003); sRumore(k.t, 0.2, "lowpass", 500, 0.5); },
    boa:        k => { sTono(k.t, 0.3, "triangle", 190, 0.5, 170, 0.003); sTono(k.t, 0.2, "sine", 380, 0.25, 360, 0.003); },
    tromba:     k => { [233, 236].forEach(f => sTono(k.t, 0.8, "sawtooth", f, 0.18, f, 0.03, 1100)); },
    tromba_lunga: k => { [233, 236].forEach(f => sTono(k.t, 2.0, "sawtooth", f, 0.18, f, 0.03, 1100)); },
    arrivo:     k => { [311, 314].forEach(f => sTono(k.t, 0.35, "sawtooth", f, 0.12, f, 0.02, 1300)); },
    passo:      k => { sTono(k.t, 0.35, "sine", 880, 0.18); sTono(k.t + 0.12, 0.45, "sine", 1320, 0.14); },
    prova:      k => { sTono(k.t, 0.3, "sine", 660, 0.18); sTono(k.t + 0.15, 0.3, "sine", 880, 0.16); sTono(k.t + 0.3, 0.5, "sine", 1320, 0.14); }
  };
  function suona(nome, v = 0){
    suoniReg.push([+simTime.toFixed(3), nome, mode === "race" && R ? +R.t.toFixed(3) : null]); if (suoniReg.length > 2000) suoniReg.shift();
    if (suoniAttivi()) try { SUONO[nome]({ t: actx.currentTime + 0.01, v }); } catch(e){}
  }

  // ---- lettura dello stato, a ogni fotogramma ----
  // fermo: pausa, istruzioni, menu o moviola. Gli eventi non si leggono finché il gioco è fermo (il confronto riprende da dove era),
  // i suoni continui scendono a zero solo nel menu e nella moviola.
  function suoniStato(){
    const r = mode === "race" && R ? R : null, b = r ? bandiereR() : null;
    return { S, R: r, mode, chiave: mode + ":" + (mode === "lesson" ? lessonIdx + "/" + stepIdx : mode === "mission" ? missionIdx : ""),
      virate: S.tacks, strambate: (S.gybesV || 0) + (S.gybesC || 0), scuf: !!S.capsized, fatto: mode === "lesson" && !!stepDone, finita: mode === "mission" && !!S.finished,
      es: r && r.es ? r.es.esito : null, contatti: r ? Object.assign({}, r.contacts) : {}, nBoa: r ? r.nBoa || 0 : 0,
      fin: r ? r.boats.map(o => o.fin !== null) : [], flag: b ? { classe: b.classe, P: b.P, X: b.X } : null };
  }
  function suoniAgg(dt, fermo, muto){
    if (LAB) return;
    // continui: vento apparente, velocità, vela che sbatte (ipotesi nostre le curve; crescono sempre coi numeri, criterio S3)
    const aws = Math.max(0, info.aws || 0), u = Math.abs(S.u || 0);
    const sbatte = !S.capsized && aws > 1 && (Math.abs(info.awa) < BOAT.luffA0 + BOAT.luffW * 0.5 || info.alpha < 6);
    suoniVal.vento = muto ? 0 : 0.03 + 0.42 * Math.pow(Math.min(1.5, aws / 10), 1.5);
    suoniVal.acqua = muto ? 0 : S.capsized ? 0.04 : 0.04 + 0.4 * Math.min(1, u / 3);
    sFase += dt * (3 + 0.45 * aws) * 2 * Math.PI;
    suoniVal.vela = muto ? 0 : S.pushing ? 0.12 : sbatte ? 0.28 * Math.min(1, aws / 8) * (0.35 + 0.65 * Math.max(0, Math.sin(sFase))) : 0;
    // 1.2.7, acqua registrata: più veloce (da 0,85 a 1,12 volte) e più chiara (filtro da 1.200 a 6.000 Hz) con la barca veloce (ipotesi nostre)
    const uf = Math.min(1, u / 3); suoniVal.acquaVel = 0.85 + 0.27 * uf; suoniVal.acquaFiltro = 1200 + 4800 * uf;
    // 1.2.7, vela registrata: colpi veri, 1 + 0,35 × vento apparente in nodi al secondo, intervallo a caso fra 0,6 e 1,4 volte il medio (ipotesi nostre).
    // Il conto dei colpi va anche a gioco muto o senza audio (lo leggono i collaudi); fermo o muto, niente colpi.
    const colpiOn = !muto && !fermo && sbatte && !S.pushing;
    suoniVal.ritmo = colpiOn ? 1 + 0.35 * aws * KN : 0;
    if (!colpiOn) sProssimo = 0;
    else { sProssimo -= dt; if (sProssimo <= 0){ suoniVal.colpi++; sProssimo = (0.6 + sRand() * 0.8) / suoniVal.ritmo;
      if (suoniAttivi() && sReg) try { sColpo(COLPI_VOL * Math.min(1, aws / 8)); } catch(e){} } }
    // 1.2.9 (PROPOSTA-SUONI-FINE.md §3, ipotesi nostre): vento registrato, sciabordio, sartiame sopra i 12 nodi apparenti, gorgoglio con la pala in stallo
    suoniVal.ventoVel = 0.9 + 0.2 * Math.min(1, aws / 10); suoniVal.ventoFiltro = 1000 + 350 * aws;
    suoniVal.onde = muto ? 0 : 0.10 + 0.08 * Math.min(1, local.tws / 8);
    const kSart = Math.min(1, Math.max(0, aws * KN - 12) / 10); suoniVal.sartiame = muto ? 0 : 0.22 * kSart; suoniVal.sartiameVel = 0.9 + 0.2 * kSart;
    suoniVal.gorgoglio = muto || fermo || S.capsized || !S.stall ? 0 : 0.8 * Math.min(1, u / 3);
    // gabbiani e scricchiolii: il tempo conta solo a gioco in corso; il conto va anche a gioco muto (lo leggono i collaudi)
    if (!muto && !fermo){
      if (sGabb === null) sGabb = 25 + sRand() * 45;
      sGabb -= dt; if (sGabb <= 0){ sGabb = 25 + sRand() * 45; sGabbiano(); }
      const heel = Math.abs(S.heel || 0);
      if (!S.capsized && heel > 18){ if (sScr === null) sScr = 2.5 + sRand() * 3.5; sScr -= dt; if (sScr <= 0){ sScr = 2.5 + sRand() * 3.5; sScricchiolio(heel); } }
    }
    if (suoniAttivi()){
      const t = actx.currentTime;
      if (sAmb){
        const su = (ch, n) => ch.g.gain.setTargetAtTime(suoniMuta[n] ? 0 : suoniVal[n], t, 0.25);
        su(sAmb.vento, "vento"); su(sAmb.onde, "onde"); su(sAmb.sartiame, "sartiame"); su(sAmb.gorgoglio, "gorgoglio");
        sAmb.vento.src.playbackRate.setTargetAtTime(suoniVal.ventoVel, t, 0.5); sAmb.vento.fl.frequency.setTargetAtTime(suoniVal.ventoFiltro, t, 0.25);
        sAmb.sartiame.src.playbackRate.setTargetAtTime(suoniVal.sartiameVel, t, 0.5);
      } else { sCh.vento.g.gain.setTargetAtTime(suoniVal.vento, t, 0.25); sCh.vento.fl.frequency.setTargetAtTime(250 + 55 * aws, t, 0.25); }
      if (sReg){
        sReg.g.gain.setTargetAtTime(suoniVal.acqua, t, 0.2); sReg.src.playbackRate.setTargetAtTime(suoniVal.acquaVel, t, 0.3); sReg.fl.frequency.setTargetAtTime(suoniVal.acquaFiltro, t, 0.2);
        sCh.vela.g.gain.setTargetAtTime(S.pushing ? suoniVal.vela : 0, t, 0.02);   // con i colpi registrati il fruscio sintetico resta solo per il boma spinto (Z)
      } else {
        sCh.acqua.g.gain.setTargetAtTime(suoniVal.acqua, t, 0.2); sCh.acqua.fl.frequency.setTargetAtTime(300 + 220 * u, t, 0.2);
        sCh.vela.g.gain.setTargetAtTime(suoniVal.vela, t, 0.02);
      }
    }
    // eventi
    const n = suoniStato();
    if (muto){ sPrev = null; return; }
    if (fermo) return;
    const p = sPrev; sPrev = n;
    if (!p || p.S !== n.S || p.chiave !== n.chiave || p.R !== n.R){ // barca, passo, modalità o regata nuova: niente suoni del passato,
      if (n.R && (!p || p.R !== n.R)) suoniBandiere(bandiereAl(-n.R.cd - 1e-6, n.R.cd), n.flag); // salvo i segnali della regata nuova, che partono da «nessuna bandiera»
      return;
    }
    suoniEventi(p, n);
  }
  function suoniEventi(p, n){
    if (n.virate > p.virate) suona("virata");
    if (n.strambate > p.strambate) suona("strambata", Math.min(1, local.tws / 8));
    if (n.scuf && !p.scuf) suona("scuffia");
    if (!n.scuf && p.scuf) suona("raddrizzata");
    if (n.fatto && !p.fatto) suona("passo");
    if (n.finita && !p.finita) suona("prova");
    if (n.es === "ok" && p.es !== "ok") suona("passo");
    if (!n.R) return;
    for (const k in n.contatti) if (n.contatti[k] !== p.contatti[k]) suona("contatto");
    if (n.nBoa > p.nBoa) suona("boa");
    n.fin.forEach((f, i) => { if (f && !p.fin[i]) suona("arrivo"); });
    if (n.flag && p.flag) suoniBandiere(p.flag, n.flag);
  }
  function suoniBandiere(pf, nf){ // regola 26: un suono all'avviso, al preparatorio e al via, uno lungo a un minuto; regola 29.1: un suono con la X
    if (nf.classe && !pf.classe) suona("tromba");
    if (nf.P && !pf.P) suona("tromba");
    if (!nf.P && pf.P) suona("tromba_lunga");
    if (!nf.classe && pf.classe) suona("tromba");
    if (nf.X && !pf.X) suona("tromba");
  }
