// Scuola di vela, gioco.js — Stato, raffiche, menu e progressi, quiz, modalità (lezioni, prove, navigazione libera), comandi, simulazione.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // STATO
  // ======================================================================
  let mode = "menu", lessonIdx = 0, stepIdx = 0, stepDone = false, holdT = 0, missionIdx = 0;
  const env = { twd: 0, tws: 10 / KN };
  const local = { twd: 0, tws: 10 / KN };
  let gustLevel = 0, gustTimer = 0, gustAll = false; // gustAll: torneo dell'1b, le raffiche nascono attorno a tutte le barche
  const gusts = [], wake = [];
  const ctl = { sheet: 0.4, tiller: 0 };
  const opt = { helm: "barra", view: "prua", autoCenter: true, autoCenterComp: false, hint: true, arrows: true, dead: true, sem: false, allInstr: false, ghost: true, aiLevel: "principianti", countdown: 180, autoSheet: false };
  let S, info, base = {}, userZoom = 1, camZoom = 1, simTime = 0, curMarks = [], geo = null;
  let allowSem = [], allowTiller = false, allowSheet = false;
  const freeEnv = { twd: 0, tws: 10, gusts: 1 }; // fino alla 1.0.78 anche lv, la scelta fra la barca dell'1a e quella dell'1b (docs/PROPOSTA-PULIZIA-CODICE.md)
  const VERSIONE = "1.2.15"; // sola fonte: menu, mare e registratore la leggono da qui

  function freshState(x, y, h, sheet){
    const twa = norm180(env.twd - h);
    S = { x, y, h, u: 1.5, vl: 0, r: 0, boomSide: twa >= 0 ? -1 : 1, boom: 30, heel: 0, heelRate: 0, hike: 0.3,
          capsized: false, righting: 0, capSide: 1, prevSide: sgn(twa), dispBoom: (twa >= 0 ? -1 : 1) * 30, boomRate: 6,
          tacks: 0, gybesV: 0, gybesC: 0, capsizes: 0, markIdx: 0, time: 0, finished: false,
          lessonMark: null, markReached: false, shake: 0, toast: null, indietro: 0 };
    ctl.sheet = sheet; ctl.tiller = 0;
    wake.length = 0; shiftSt = null; shiftDeg = 0; // i salti li rimettono la navigazione libera e le regate dell'1b
    Object.assign(local, env);
    info = step(S, ctl, local, 0);
    S.dispBoom = S.boomSide * S.boom;
  }
  const curStep = () => mode === "lesson" ? LESSONS[lessonIdx].steps[stepIdx] : null;

  // ---------- raffiche ----------
  function gustGeom(g, x, y){
    const to = (env.twd + 180) * D2R, ax = Math.sin(to), ay = -Math.cos(to);
    const dx = x - g.x, dy = y - g.y, along = dx * ax + dy * ay, across = dx * -ay + dy * ax;
    return (along / (g.r * 1.4)) ** 2 + (across / g.r) ** 2;
  }
  // ---- salti di vento dell'1b (1.0.28) ----
  let shiftSt = null, shiftDeg = 0; // stato del generatore (newShift, js/motore.js) e gradi di cui il vento è girato rispetto al medio
  function setShifts(kind){ shiftSt = kind ? newShift(kind, Math.random) : null; shiftDeg = shiftSt ? stepShift(shiftSt, 0, Math.random) : 0; }
  function windAt(x, y){
    let k = 0, sh = 0;
    for (const g of gusts){ const d2 = gustGeom(g, x, y); if (d2 < 1){ const f = (g.big ? Math.min(1, (1 - d2) * 4) : (1 - d2) ** 2) * g.life; k += f * g.k; sh += f * g.sh; } } // la raffica garantita ha un fronte netto
    const osc = gustLevel ? Math.sin(simTime / 45) * 3 + Math.sin(simTime / 17) * 1.5 : 0;
    const twd = env.twd + sh + osc;
    return { twd: norm360(shiftSt ? twd + shiftDeg : twd), tws: env.tws * (1 + k) };
  }
  function gustAt(x, y){
    let k = 0;
    for (const g of gusts){ const d2 = gustGeom(g, x, y); if (d2 < 1) k += (1 - d2) * g.life * g.k; }
    return k;
  }
  function spawnGust(dist, lat, mature, P = S){
    const to = (env.twd + 180) * D2R, ax = Math.sin(to), ay = -Math.cos(to);
    gusts.push({ x: P.x - ax * dist - ay * lat, y: P.y - ay * dist + ax * lat, r: 9 + Math.random() * 11,
      k: gustLevel === 1 ? 0.2 + Math.random() * 0.2 : 0.35 + Math.random() * 0.3,
      sh: (Math.random() - 0.5) * (gustLevel === 1 ? 12 : 20), age: mature ? 3 : 0, ttl: 40 + Math.random() * 20, life: mature ? 1 : 0 });
  }
  function setGusts(level, all = false){
    gustLevel = level; gustAll = all; gusts.length = 0;
    if (level){ spawnGust(22, -14, true); spawnGust(45, 18, true); spawnGust(70, -6, true); spawnGust(95, 25, true); gustTimer = 3; }
  }
  function updateGusts(dt){
    if (shiftSt) shiftDeg = stepShift(shiftSt, dt, Math.random, !(mode === "race" && R && R.t < 0)); // il salto persistente comincia al via (la linea è allineata poco prima)
    const to = (env.twd + 180) * D2R, ax = Math.sin(to), ay = -Math.cos(to);
    for (const g of gusts){ g.x += ax * env.tws * 0.8 * dt; g.y += ay * env.tws * 0.8 * dt; g.age += dt; g.life = Math.max(0, Math.min(1, g.age / 3, (g.ttl - g.age) / 3)); }
    for (let i = gusts.length - 1; i >= 0; i--) if (gusts[i].age > gusts[i].ttl) gusts.splice(i, 1);
    if (!gustLevel) return;
    gustTimer -= dt;
    if (gustTimer <= 0 && gusts.length < 12){
      gustTimer = (gustLevel === 1 ? 4 : 2.6) * (0.6 + Math.random() * 0.8);
      // torneo dell'1b: sopravento a una barca a caso (prima solo al giocatore, e un avversario lontano navigava senza raffiche)
      spawnGust(55 + Math.random() * 60, (Math.random() - 0.5) * 90, false, gustAll && mode === "race" && R ? R.boats[Math.floor(Math.random() * R.boats.length)].S : S);
    }
  }

  // ---------- lettura per le condizioni ----------
  function ttState(){
    if (Math.abs(info.awa) < BOAT.luffA0 + BOAT.luffW * 0.5) return "flog";
    if (info.alpha < 8) return "wind";
    if (info.alpha > 27) return "lee";
    return "ok";
  }
  function readI(){
    return { twa: Math.abs(norm180(local.twd - S.h)), kn: S.u * KN, tt: ttState(), alpha: info.alpha, heel: S.heel, r: S.r,
             sheet: ctl.sheet, tiller: ctl.tiller, inGust: local.tws > env.tws * 1.12, gustK: local.tws / env.tws - 1 };
  }
  // 1.0.73: scotta automatica come aiuto attivabile (docs/PROPOSTA-SCOTTA-AUTOMATICA.md). Le lezioni con autoTrim usano la regola semplice;
  // con la casella delle impostazioni (solo prove e navigazione libera) si aggiunge una lasca in funzione della sbandata, per non scuffiare in raffica.
  let AUTO_HEEL0 = 12, AUTO_K = 1.5; // ipotesi nostre: sbandata (gradi) da cui si lasca e gradi di boma per grado di sbandata in più
  function autoSheet(sicura){
    const A = Math.abs(info.awa), lasca = sicura ? AUTO_K * Math.max(0, Math.abs(S.heel) - AUTO_HEEL0) : 0, target = Math.max(BOAT.minBoom, A - 17) + lasca;
    return clamp((target - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  }
  const autoSheetAttiva = () => opt.autoSheet && (mode === "mission" || mode === "free") && !S.capsized;
  function autoSheetSpegni(){ if (!opt.autoSheet) return; opt.autoSheet = false; $("autoSheetOpt").checked = false; toast("Scotta automatica spenta: la scotta è tua"); }

  // ======================================================================
  // MENU, PROGRESSI, GLOSSARIO
  // ======================================================================
  // ---- salvataggi, fasce e meriti ----
  // 0.22: gioco libero e carriera hanno salvataggio e fantasmi separati; la modalità si cambia solo dal menu
  const MODO = "scuolaVelaModo";
  const KEYS = m => m === "carriera" ? ["scuolaVelaCarriera.v1", "scuolaVelaGhostCarriera.v1"] : ["scuolaVelaSim.v1", "scuolaVelaGhost.v1"];
  let modo = "libero";
  try { if (localStorage.getItem(MODO) === "carriera") modo = "carriera"; } catch(e){}
  let [STORE, GHOST_STORE] = KEYS(modo);
  // record e fantasmi dei percorsi cambiati usano chiavi nuove; i completamenti restano.
  // 0.14: giro di boa dal lato giusto (prove 4 e 5, regate). 0.19: linea d'arrivo in tutte le prove.
  const KEYV = { m0: "m0.4", m1: "m1.4", m2: "m2.4", m3: "m3.5", m4: "m4.6", r0: "r0.4", r1: "r1.4" }; // 1.0.6: barca nuova (resistenza dalla vasca); 1.0.11: bolina nuova (resistenza indotta, vela che stringe): i tempi di prima non sono confrontabili
  const OLD_M = ["m0", "m1", "m2", "m3", "m4", "m3.2", "m4.3", "m0.2", "m1.2", "m2.2", "m3.3", "m4.4", "r0.2", "r1.2", "m0.3", "m1.3", "m2.3", "m3.4", "m4.5", "r0.3", "r1.3"]; // chiavi di prima della 0.19 e delle barche vecchie (1.0.6, 1.0.11): si cancellano al primo avvio
  let wipeNote = false;
  const recK = k => KEYV[k] || k;
  let progress;
  const loadProgress = () => { progress = { done: {}, best: {}, clean: {} }; try { const raw = localStorage.getItem(STORE); if (raw) progress = Object.assign(progress, JSON.parse(raw)); } catch(e){} };
  const STAR = '<span class="star" title="Completata almeno una volta senza errori">★</span>';
  // fasce di tempo delle prove: bands = [oro, argento, bronzo] in secondi (tempo massimo per ciascuna)
  const MEDALS = ["oro", "argento", "bronzo"];
  const medalOf = (i, sec) => { const b = MISSIONS[i].bands; if (!sec) return 0; for (let k = 0; k < 3; k++) if (sec <= b[k]) return k + 1; return 0; };
  const medalTag = (i, sec) => { const m = medalOf(i, sec); return m ? `<span class="medal m${m}" title="Medaglia: ${MEDALS[m - 1]}"></span>` : ""; };
  // 0.23, meriti del libretto (solo carriera): tabella provvisoria di docs/archivio/PROPOSTA-ESAME-E-BREVETTO.md §12, da tarare giocando.
  // Si ricalcolano ogni volta da progress: niente si salva. Competizione: solo il piazzamento, senza il +1 «senza errori».
  const MERITI = [["abil", "Abilità", 20, 8], ["cono", "Conoscenza", 12, 6], ["comp", "Competizione", 8, 3], ["esp", "Esperienza", 6, 6]];
  const TOT_MIN = 29;
  function meriti(p){
    const VIS = ORD_L.filter(i => !LESSONS[i].nascosta);
    const racePt = i => Math.max(0, ...["principianti", "esperti"].map(l => { const v = p.race?.[recK("r" + i) + ":" + l]; return v && v.n === 4 ? 5 - v.pos : 0; }));
    const pt = {
      abil: MISSIONS.reduce((a, m, i) => { const k = medalOf(i, p.best[recK("m" + i)]); return a + (k ? 4 - k : 0) + (p.clean[recK("m" + i)] ? 1 : 0); }, 0),
      // 1.2.4 (docs/PROPOSTA-MENU.md §2): conoscenza ed esperienza su tutte le lezioni visibili (oggi le 20), in proporzione, con gli stessi massimi e minimi di prima.
      // Solo le visibili, come l'esame: i collaudi che nascondono le lezioni nuove ritrovano i conti delle 6 lezioni di prima
      cono: Math.floor(MERITI[1][2] * VIS.reduce((a, i) => { const s = p.quiz?.["q" + i], q = quizDi(i); return a + (s === undefined ? 0 : s * 5 >= q.length * 4 ? 2 : s * 5 >= q.length * 3 ? 1 : 0); }, 0) / (2 * VIS.length) + 1e-9),
      comp: RACES_CARRIERA.reduce((a, rc, i) => a + racePt(i), 0),
      esp: Math.floor(MERITI[3][2] * VIS.filter(i => p.done["l" + i]).length / VIS.length + 1e-9) };
    const pulite = RACES_CARRIERA.filter((rc, i) => ["principianti", "esperti"].some(l => p.race?.[recK("r" + i) + ":" + l]?.pulita)).length;
    const totale = MERITI.reduce((a, [k]) => a + pt[k], 0), esame = !!p.exam?.superato;
    // 0.23, dopo la prova di Ale: una riga con tutto quello che manca, e un suggerimento concreto per ogni area che manca
    const sotto = MERITI.filter(([k, , , min]) => pt[k] < min);
    const elenco = a => a.length > 1 ? a.slice(0, -1).join(", ") + (/^E/.test(a[a.length - 1]) ? " ed " : " e ") + a[a.length - 1] : a[0];
    const poi = esame ? "." : "; poi l'esame.";
    const manca = sotto.length ? "Ti mancano punti in " + elenco(sotto.map(r => r[1])) + poi
      : totale < TOT_MIN ? (TOT_MIN - totale === 1 ? "Ti manca 1 punto" : "Ti mancano " + (TOT_MIN - totale) + " punti") + " al totale" + poi
      : !esame ? "Ti manca l'esame." : null;
    const voce = k => {
      if (k === "esp"){ const i = VIS.find(j => !p.done["l" + j]); return i === undefined ? null : LESSONS[i].name + ", " + LESSONS[i].title + "."; }
      if (k === "abil"){
        const fas = i => medalOf(i, p.best[recK("m" + i)]), tit = i => "Prova " + (i + 1) + ", " + MISSIONS[i].title;
        let i = MISSIONS.findIndex((m, j) => !fas(j)); if (i >= 0) return tit(i) + ".";
        i = MISSIONS.findIndex((m, j) => fas(j) > 1); if (i >= 0) return tit(i) + ": prova a migliorare il tempo.";
        i = MISSIONS.findIndex((m, j) => !p.clean[recK("m" + j)]); return i < 0 ? null : tit(i) + ": completala senza errori."; }
      if (k === "cono"){ const i = VIS.find(j => { const v = p.quiz?.["q" + j]; return v === undefined || v * 5 < quizDi(j).length * 4; }); return i === undefined ? null : ripName(i) + ", " + LESSONS[i].title + "."; }
      const rp = RACES_CARRIERA.map((rc, i) => racePt(i));
      const i = rp.indexOf(Math.min(...rp)); return rp[i] >= 4 ? null : "la " + RACES_CARRIERA[i].title + " (con avversari).";
    };
    const aree = sotto.length ? sotto : totale < TOT_MIN ? MERITI.filter(([k, , max]) => pt[k] < max) : [];
    const sugg = aree.map(([k]) => voce(k)).filter(Boolean);
    if (!sugg.length && !esame) p.exam?.ripasso?.length ? p.exam.ripasso.forEach(i => sugg.push(ripName(i) + ", " + LESSONS[i].title + " (dopo l'esame).")) : sugg.push("l'esame su tutte le lezioni.");
    return { pt, pulite, totale, esame, superato: !manca, manca, sugg };
  }
  let giroSug = 0; // il suggerimento cambia a ogni ritorno al menu; il giro non si salva
  function librettoHtml(){
    const m = meriti(progress), pc = (v, max) => Math.round(100 * v / max);
    const rows = MERITI.map(([k, nome, max, min]) => `<div class="lrow"><span>${nome}</span><span class="lbar"><i style="width:${pc(m.pt[k], max)}%"></i></span><span class="num"><span data-m="${k}">${m.pt[k]} / ${max}</span> · <span class="${m.pt[k] >= min ? "ok" : "no"}">servono ${min}</span></span></div>`).join("");
    const sug = m.sugg.length ? m.sugg[giroSug++ % m.sugg.length] : null;
    return `<div><div class="part-head"><h2>Libretto</h2><span id="libTot">totale ${m.totale} / ${MERITI.reduce((a, r) => a + r[2], 0)} (servono ${TOT_MIN})</span></div>
      <div class="lib">${rows}<p id="libPulite">Regate senza errori: ${m.pulite} su ${RACES_CARRIERA.length}</p>${m.superato && progress.brevetto ? `<p class="manca" id="libManca">Attestato ottenuto il ${fmtData(progress.brevetto.data)}. <button class="linkish" id="goAttest">Aprilo</button></p>`
        : `<p class="manca" id="libManca">${m.superato ? "Scuola superata." : m.manca}</p>${sug ? `<p id="libSug">Cosa potresti fare adesso: ${sug}</p>` : ""}`}</div></div>`;
  }
  loadProgress();
  const saveProgress = () => { if (LAB) return; try { localStorage.setItem(STORE, JSON.stringify(progress)); } catch(e){} };
  // ---- menu principale e attestato ----
  const itemName = ([t, i]) => t === "l" ? LESSONS[i].name : "Prova " + (i + 1);
  const seqPos = () => SEQ.findIndex(([t, i]) => (t === "l" && mode === "lesson" && i === lessonIdx) || (t === "m" && mode === "mission" && i === missionIdx));
  const nextItem = () => { const p = seqPos(); return p >= 0 && p < SEQ.length - 1 ? SEQ[p + 1] : null; };
  const nextLabel = () => { const n = nextItem(); return n ? "Prosegui: " + itemName(n) : "Torna al menu"; };
  const goNext = () => { const n = nextItem(); n ? openItem(n) : showMenu(); };
  const p2 = n => String(n).padStart(2, "0");
  const fmtClock = sec => { const s = Math.floor(sec); return Math.floor(s / 60) + ":" + p2(s % 60); }; // 3:07
  const fmtTime = sec => { const m = Math.floor(sec / 60), s2 = sec % 60; return m ? m + " min " + s2 + " s" : s2 + " s"; };

  function openItem(it){
    if (it !== "free" && it[0] !== "r") menuGr = gruppoDi(it); // 1.2.4: tornando al menu si ritrova la scheda della voce aperta
    $("menu").hidden = true; $("game").hidden = false; resize();
    if (it === "free") startFree(); else if (it[0] === "r") startRace(it[1]); else it[0] === "l" ? startLesson(it[1]) : startMission(it[1]);
    window.scrollTo(0, 0); canvas.focus();
  }
  const oggi = () => { const d = new Date(); return d.getFullYear() + "-" + p2(d.getMonth() + 1) + "-" + p2(d.getDate()); };
  const fmtData = d => new Date(d + "T12:00").toLocaleDateString("it-IT", { day: "numeric", month: "long", year: "numeric" });
  const ripName = li => "Ripasso " + numLez(li); // 1.0.2: «Lezione» resta alla Scuola; ripassi ed esame usano «Ripasso N»; dalla 1.2.4 N è il numero della lezione nel menu
  let menuGr = null; // 1.2.4: la scheda aperta della Scuola (gruppo); null = quella della prima voce da fare
  const ripElenco = a => (a.length > 1 ? "ripassi " + a.slice(0, -1).join(", ") + " e " + a[a.length - 1] : "ripasso " + a[0]);
  function esameBtn(){
    const ex = modo === "carriera" ? progress.exam : null, tot = domandeEsame();
    if (ex?.superato) return `<button id="goEsame" disabled>Esame superato<small>${ex.voto} su ${ex.n || 20}</small></button>`; // 1.2.3: ex.n, le domande di quell'esame (prima sempre 20)
    if (ex?.ripasso?.length) return `<button id="goEsame" disabled>Esame: prima i ripassi<small>${ripElenco(ex.ripasso.map(numLez))}</small></button>`;
    return `<button id="goEsame">Esame su tutte le lezioni<small>${tot} domande, ne servono ${sogliaEsame(tot)}</small></button>`;
  }
  // 0.24, attestato (solo carriera): compare da solo la prima volta che si torna al menu con il livello superato, poi dal libretto
  // disegno nostro: una deriva stilizzata sul mare, in alto sull'attestato (non è un marchio né un logo di nessuna classe)
  const NAVE = `<svg class="nave" viewBox="0 0 120 70" role="img" aria-label="Una deriva a vela"><path class="vela" stroke-width="2" stroke-linejoin="round" d="M58 6 L58 46 L22 46 Z"/><path class="vela" stroke-width="2" stroke-linejoin="round" d="M64 14 L64 46 L92 46 Z"/><path class="scafo" d="M14 50 L102 50 L90 60 L28 60 Z"/><path class="onda" d="M6 66 Q16 60 26 66 T46 66 T66 66 T86 66 T106 66 T116 66"/></svg>`;
  function openAttest(){
    const B = progress.brevetto, m = meriti(progress), q = t => t.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
    $("atBody").innerHTML = `${NAVE}<p class="sc">Scuola di vela</p><hr><p class="titolo">Attestato del gioco</p><h2 id="atTitle">La scuola</h2><p class="ruolo">superata</p>
      <label for="atName">Nome (facoltativo)</label><input id="atName" maxlength="60" autocomplete="off" value="${q(B.nome || "")}">
      <p>Ottenuto il ${fmtData(B.data)}, con l'esame superato: ${progress.exam.voto} su ${progress.exam.n || 20}.</p>
      <ul>${MERITI.map(([k, nome, max]) => `<li>${nome}: ${m.pt[k]} / ${max}</li>`).join("")}</ul>
      <p class="legal">Nessun valore legale: non sostituisce un corso di vela né la patente nautica.</p>
      <div class="row"><button class="primary" id="atPrint">Stampa</button><button id="atClose">Chiudi</button></div>`;
    $("atName").oninput = e => { B.nome = e.target.value.trim(); saveProgress(); };
    $("atPrint").onclick = () => window.print();
    $("atClose").onclick = () => $("attest").close();
    $("attest").showModal();
  }
  function showMenu(){
    sesChiudi("interrotta"); // 1.0.60: registrazione automatica di regata (si chiude da sola, se è accesa)
    if (mode === "race") torEsci(); // regata del torneo: finita si salva il risultato, a metà vale come ritiro (1.0.50)
    mode = "menu"; setControls([], false, false);
    let nuovo = false;
    if (modo === "carriera" && !progress.brevetto && meriti(progress).superato){ progress.brevetto = { data: oggi() }; saveProgress(); nuovo = true; }
    $("game").hidden = true; $("menu").hidden = false;
    const vis = ([t, i]) => t !== "l" || !LESSONS[i].nascosta, VSEQ = SEQ.filter(vis); // 1.2.4: nel gioco nessuna lezione è nascosta; i collaudi possono nasconderle
    const doneCount = VSEQ.filter(([t, i]) => progress.done[t + i]).length;
    if (menuGr === null){ const p = VSEQ.findIndex(([t, i]) => !progress.done[t + i]); menuGr = p < 0 ? 0 : gruppoDi(VSEQ[p]); }
    const esc = t => t.replace(/"/g, "&quot;");
    const schede = GRUPPI.map(([nome, voci], j) => { const v = voci.filter(vis); return `<button data-g="${j}" aria-pressed="${j === menuGr}">${j + 1} · ${nome} <small>${v.filter(([t, i]) => progress.done[t + i]).length}/${v.length}</small></button>`; }).join("");
    const rows = VSEQ.map(([t, i], k) => { if (gruppoDi([t, i]) !== menuGr) return "";
      const key = t + i, done = progress.done[key];
      const kind = t === "l" ? LESSONS[i].name : "Prova " + (i + 1);
      const title = t === "l" ? LESSONS[i].title : MISSIONS[i].title;
      const desc = t === "l" ? LESSONS[i].desc : MISSIONS[i].desc;
      let state = done ? "Completata" : "Da fare";
      if (t === "m" && progress.best[recK(key)]) state = fmtTime(progress.best[recK(key)]) + medalTag(i, progress.best[recK(key)]);
      if (t === "m" && progress.clean[recK(key)]) state += STAR;
      return `<button class="item" data-k="${k}" title="${esc(desc)}"><span class="num">${k + 1}</span><span class="kind">${kind}</span><span class="title">${title}</span><span class="state ${done ? "ok" : "todo"}">${state}</span></button>`;
    }).join("");
    const races = (modo === "carriera" ? RACES_CARRIERA : RACES).map((rc, i) => { const b = progress.best[recK("r" + i)];
      return `<button class="item wide" data-r="${i}"><span class="num">⚑</span><span class="title">${rc.title}</span><span class="state ${b ? "ok" : "todo"}">${b ? "Record: " + fmtTime(b) : "Da fare"}${progress.clean[recK("r" + i)] ? STAR : ""}</span><span class="desc">${rc.desc}</span></button>`; }).join("");
    const torBtn = (() => { const chiuso = modo === "carriera" && !progress.brevetto, T = progress.torneo, F = progress.torneoFatto; // torneo dell'1b (1.0.34): in carriera dopo il brevetto
        const st = chiuso ? "dopo l'attestato" : T ? "in corso: regata " + (T.ris.length + 1) + " di " + TOR_N : F ? "migliore: " + F.pos + "°" + (modo === "carriera" ? " · meriti " + F.mer : "") : "Da fare";
        return `<button class="item wide" id="goTor"${chiuso ? " disabled" : ""}><span class="num">⚑</span><span class="title">Torneo</span><span class="state ${F ? "ok" : "todo"}">${st}</span></button>`; })(); // senza descrizione (la dà il riquadro che si apre); nel gioco libero sta nel terzo riquadro: in «Regate» il menu non stava in 1360x650
    // 1.2.4: i ripassi della scheda aperta, su due colonne; ✓ = migliore almeno l'80%, il punteggio si legge passando sopra
    const quiz = `<div class="rip2">` + GRUPPI[menuGr][1].filter(([t, i]) => t === "l" && !LESSONS[i].nascosta).map(([, i]) => { const L = LESSONS[i], best = progress.quiz?.["q" + i], n = quizDi(i).length;
      return `<button data-q="${i}" title="${esc(ripName(i) + " · " + L.title + " · " + (best !== undefined ? "migliore: " + best + " su " + n : n + " domande"))}"><span>${numLez(i)} · ${L.title}</span>${best !== undefined && best * 5 >= n * 4 ? "<small>✓</small>" : ""}</button>`; }).join("") + `</div>`;
    $("menu").innerHTML = `<div class="menu-inner">
      <header class="menu-head"><div><h1>Scuola di vela <span class="ver">V. ${VERSIONE}</span></h1><p>Un simulatore per imparare a governare una deriva. Segui l'ordine numerato della Scuola, oppure apri qualsiasi voce.</p></div>
        <div class="head-r"><div class="seg" id="modoSel"><button data-v="libero" aria-pressed="${modo === "libero"}">Gioco libero</button><button data-v="carriera" aria-pressed="${modo === "carriera"}">Carriera</button></div>
        <button class="pill" id="menuGloss">Glossario</button></div></header>
      <div class="tiles">
        <section class="tile"><div><div class="part-head"><h2>Scuola</h2><span>${doneCount} di ${VSEQ.length} completate</span></div><div class="seg schede" id="schede">${schede}</div><div class="items">${rows}</div></div></section>
        <section class="tile">
          <div><div class="part-head"><h2>Regate</h2><span>contro il computer o il tuo fantasma</span></div><div class="items">${races}${modo === "carriera" ? torBtn : ""}</div></div>
          <div><div class="part-head"><h2>Navigazione libera</h2></div><div class="items"><button class="item wide free" id="goFree"><span class="num">⛵</span><span class="title">Naviga senza obiettivi</span><span></span><span class="desc">Scegli vento e raffiche e prova quello che vuoi.</span></button></div></div>
        </section>
        <section class="tile">
          <div><div class="part-head"><h2>Ripassi ed esame</h2><span>gruppo ${menuGr + 1} · ${GRUPPI[menuGr][0]}</span></div><div class="review">${quiz}
            ${esameBtn()}</div></div>
          ${modo === "carriera" ? librettoHtml() : `<div><div class="part-head"><h2>Tornei</h2></div><div class="items">${torBtn}</div></div>`}
        </section>
      </div>
      <footer class="menu-foot"><span>${wipeNote ? "<b>La barca o le prove sono cambiate: i tempi salvati sono stati azzerati.</b> " : ""}I progressi restano salvati in questo browser. ★ prova o regata completata almeno una volta senza errori. Il pallino oro, argento o bronzo è la medaglia del tuo tempo migliore.</span><span><button class="linkish" id="regOpen">Regate registrate</button> <button class="linkish" id="resetProg">Azzera i progressi</button></span></footer></div>`;
    $("menu").querySelectorAll("button.item[data-k]").forEach(b => b.onclick = () => openItem(VSEQ[+b.dataset.k]));
    $("schede").onclick = e => { const b = e.target.closest("button[data-g]"); if (b && +b.dataset.g !== menuGr){ menuGr = +b.dataset.g; showMenu(); } };
    $("goFree").onclick = () => openItem("free");
    $("goTor").onclick = torApri;
    $("goEsame").onclick = openEsame;
    if ($("goAttest")) $("goAttest").onclick = openAttest;
    if (nuovo) openAttest();
    $("menuGloss").onclick = openGloss;
    $("menu").querySelectorAll("[data-q]").forEach(b => b.onclick = () => openQuiz(+b.dataset.q));
    $("menu").querySelectorAll("[data-r]").forEach(b => b.onclick = () => openItem(["r", +b.dataset.r]));
    $("modoSel").onclick = e => { const b = e.target.closest("button"); if (b && b.dataset.v !== modo) setModo(b.dataset.v); };
    $("resetProg").onclick = () => { if (confirm(modo === "carriera" ? "Azzerare i progressi della carriera, fantasmi compresi? Il gioco libero non cambia." : "Azzerare i progressi del gioco libero, fantasmi compresi? La carriera non cambia.")){ progress = { done: {}, best: {}, clean: {} }; ghosts = {}; saveProgress(); saveGhosts(); showMenu(); } };
    window.scrollTo(0, 0); wipeNote = false; // il messaggio compare una volta sola
  }
  $("toMenu").onclick = () => { if (torEsciOk()) showMenu(); };
  function setModo(m){
    modo = m; [STORE, GHOST_STORE] = KEYS(m); loadProgress(); loadGhosts();
    try { localStorage.setItem(MODO, m); } catch(e){}
    showMenu();
  }

  // ---- glossario e impostazioni ----
  function renderGloss(q = ""){
    const n = q.trim().toLowerCase();
    const list = glossVisibili().filter(([t, d]) => !n || t.toLowerCase().includes(n) || d.toLowerCase().includes(n));
    $("glList").innerHTML = list.length ? list.map(([t, d, w]) => `<dt>${t}<small>${w}</small></dt><dd>${d}</dd>`).join("")
      : `<p class="gl-empty">Nessun termine trovato. Prova con una parola più breve.</p>`;
  }
  function openGloss(){ releaseKeys(); $("glSearch").value = ""; renderGloss(); $("gloss").showModal(); }
  $("openSet").onclick = () => { releaseKeys(); $("setDlg").showModal(); };
  $("setClose").onclick = () => $("setDlg").close();
  $("glClose").onclick = () => $("gloss").close();
  $("glSearch").addEventListener("input", e => renderGloss(e.target.value));


  // ---------- quiz ----------
  let qz = null;
  const mescola = a => { for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }; // Fisher-Yates sul posto
  const quizOpts = (right, wrong) => mescola([right, ...wrong].map(t => ({ t, ok: t === right })));
  const showQuiz = () => { renderQuiz(); $("quiz").showModal(); };
  function openQuiz(li, only){ // only: indici delle domande da riproporre (giro parziale); senza, ripasso completo
    releaseKeys();
    const qs = quizDi(li).map(([q, right, wrong, expl], n) => ({ n, q, right, wrong, expl })).filter(x => !only || only.includes(x.n))
      .map(({ n, q, right, wrong, expl }) => ({ n, q, right, opts: quizOpts(right, wrong), expl }));
    qz = { li, qs, i: 0, score: 0, answered: false, partial: !!only, wrong: [] };
    showQuiz();
  }
  // esame: quotaEsame(li) domande a caso da ogni lezione visibile, poi tutte in ordine casuale (20 con le sole 6 lezioni di oggi). Nel gioco libero non salva niente.
  // 1.2.3: le lezioni nascoste non consumano numeri a caso, quindi con le sole 6 lezioni l'estrazione è identica a prima (collaudo_esame, G1)
  const estraiEsame = () => mescola(lezioniEsame().flatMap(li => mescola(bancaEsame(li).map(q => [li, ...q])).slice(0, quotaEsame(li))));
  function openEsame(){
    releaseKeys();
    const qs = estraiEsame().map(([li, passo, q, right, wrong, expl]) => ({ li, passo, q, right, opts: quizOpts(right, wrong), expl }));
    qz = { exam: true, qs, i: 0, score: 0, answered: false, wrong: [] };
    showQuiz();
  }
  function closeQuiz(){ $("quiz").close(); }
  $("quiz").addEventListener("close", () => { if (mode === "menu") showMenu(); }); // aggiorna il punteggio migliore nel menu
  const wrongItem = w => `<div class="wq"><p class="wt">${w.q}</p><p>Hai risposto: ${w.given}</p><p>Giusta: <b>${w.right}</b></p><p class="expl">${w.expl}</p>${w.passo ? `<p class="from">dal passo «${w.passo}»</p>` : ""}</div>`;
  function renderEsito(b){
    const n = qz.qs.length, soglia = sogliaEsame(n), ok = qz.score >= soglia;
    const groups = ORD_L.map(li => [LESSONS[li], qz.wrong.filter(w => w.li === li)]).filter(([, ws]) => ws.length); // 1.2.4: nell'ordine della Scuola
    // 0.24, carriera: un esame superato è definitivo (voto unico); non superato, prima il ripasso completo delle lezioni sbagliate
    const car = modo === "carriera", rip = groups.map(([L]) => LESSONS.indexOf(L));
    if (car){ progress.exam = ok ? { superato: true, voto: qz.score, n, data: oggi() } : { superato: false, voto: qz.score, n, data: oggi(), ripasso: rip }; saveProgress(); }
    const btns = !car ? `<button class="primary" id="qzAgain">Rifai l'esame</button>`
      : ok ? "" : rip.map(li => `<button data-rq="${li}">${ripName(li)}</button>`).join("");
    b.innerHTML = `<h2>Esame della scuola</h2><div class="score">${qz.score} su ${n}: ${ok ? "superato" : `non superato (servono ${soglia})`}</div>
      ${car ? `<p class="q">${ok ? "Il voto è definitivo." : "Ripassa le lezioni in cui hai sbagliato, poi potrai rifare l'esame."}</p>` : ""}
      ${groups.length ? `<div class="wlist" id="qzWrong">${groups.map(([L, ws]) => `<h3>${L.name}: ${L.title}</h3>${ws.map(wrongItem).join("")}`).join("")}</div>` : ""}
      <div class="row">${btns}<button id="qzClose">Chiudi</button></div>`;
    if (!car) $("qzAgain").onclick = openEsame;
    b.querySelectorAll("[data-rq]").forEach(x => x.onclick = () => openQuiz(+x.dataset.rq));
    $("qzClose").onclick = closeQuiz;
  }
  function renderQuiz(){
    const L = LESSONS[qz.li], b = $("qzBody");
    if (qz.i >= qz.qs.length){
      if (qz.exam) return renderEsito(b);
      const n = qz.qs.length, key = "q" + qz.li, prev = progress.quiz?.[key], nw = qz.wrong.length;
      if (!qz.partial){ progress.quiz = progress.quiz || {}; if (prev === undefined || qz.score > prev) progress.quiz[key] = qz.score;
        const ex = modo === "carriera" ? progress.exam : null; if (ex?.ripasso) ex.ripasso = ex.ripasso.filter(x => x !== qz.li); // 0.24: ripasso completo dopo l'esame, con qualsiasi punteggio
        saveProgress(); } // il giro parziale non tocca il record
      b.innerHTML = `<h2>${ripName(qz.li)} · ${L.title}</h2><div class="score">${qz.score} su ${n}</div>
        <p class="q">${nw === 0 ? "Tutto giusto." : nw === 1 ? "Quasi tutto giusto: ecco la domanda sbagliata con la spiegazione." : "Conviene rifare la lezione, o almeno i passi sugli argomenti sbagliati: ecco le domande sbagliate."}</p>
        ${nw ? `<div class="wlist" id="qzWrong">${qz.wrong.map(wrongItem).join("")}</div>` : ""}
        <div class="row"><button class="primary" id="qzAgain">Rifai il ripasso</button>${nw ? `<button id="qzOnly">Ripassa solo le sbagliate</button><button id="qzLesson">Rivedi la lezione</button>` : ""}<button id="qzClose">Chiudi</button></div>`;
      $("qzAgain").onclick = () => openQuiz(qz.li); $("qzClose").onclick = closeQuiz;
      if (nw){ const ids = qz.wrong.map(w => w.n), li = qz.li; $("qzOnly").onclick = () => openQuiz(li, ids); $("qzLesson").onclick = () => { startLesson(li); closeQuiz(); }; }
      return;
    }
    const Q = qz.qs[qz.i];
    b.innerHTML = `<div class="qz-top"><h2>${qz.exam ? "Esame della scuola" : ripName(qz.li)}</h2><span>Domanda ${qz.i + 1} di ${qz.qs.length}</span></div>
      <p class="q">${Q.q}</p><div class="opts2">${Q.opts.map((o, k) => `<button class="opt" data-k="${k}">${o.t}</button>`).join("")}</div>
      <div id="qzAfter"></div>`;
    b.querySelectorAll(".opt").forEach(btn => btn.onclick = () => {
      if (qz.answered) return; qz.answered = true;
      const o = Q.opts[+btn.dataset.k]; if (o.ok) qz.score++; else qz.wrong.push({ n: Q.n, li: Q.li, passo: Q.passo, q: Q.q, given: o.t, right: Q.right, expl: Q.expl });
      // esame: nessun colore e nessuna spiegazione fino alla fine (aiuterebbero nelle domande dopo); la risposta non si cambia
      b.querySelectorAll(".opt").forEach((x, k) => { x.disabled = true; if (!qz.exam && Q.opts[k].ok) x.classList.add("right"); });
      if (qz.exam) btn.classList.add("sel"); else if (!o.ok) btn.classList.add("wrong");
      $("qzAfter").innerHTML = `${qz.exam ? "" : `<p class="expl"><b>${o.ok ? "Giusto." : "Non proprio."}</b> ${Q.expl}</p>`}
        <div class="row"><button class="primary" id="qzNext">${qz.i + 1 < qz.qs.length ? "Domanda successiva" : "Vedi il risultato"}</button></div>`;
      $("qzNext").onclick = () => { qz.i++; qz.answered = false; renderQuiz(); };
      $("qzNext").focus();
    });
  }

  // ======================================================================
  // MODALITÀ
  // ======================================================================
  // ---- schede del pannello, comandi, strumenti ----
  // la barra che torna al centro ha due impostazioni: lezioni e navigazione libera (attiva), prove e regate (spenta: un regatante tiene la barra ferma)
  const centerKey = () => mode === "mission" || mode === "race" ? "autoCenterComp" : "autoCenter";
  const centerNote = () => opt.autoCenterComp ? "" : " La barra resta dove la lasci: la riporta al centro la barra spaziatrice (si può cambiare nelle impostazioni, pulsante ⚙).";
  function showCards(which){
    $("autoCenter").checked = opt[centerKey()];
    $("lesson").hidden = which !== "lesson"; $("mission").hidden = which !== "mission"; $("free").hidden = which !== "free"; $("race").hidden = which !== "race";
    $("done").hidden = true; $("mRow").hidden = which !== "mission"; $("freeOpts").hidden = which !== "free";
    $("rRow").hidden = which !== "race"; $("rDone").hidden = true; $("finOv").hidden = true; document.querySelector(".panel").classList.remove("fin");
    document.querySelector(".panel").classList.toggle("play", which !== "lesson");
    document.querySelector(".panel").classList.toggle("noends", which !== "lesson" || lessonIdx >= 2);
    $("status").hidden = which !== "mission" && which !== "race"; $("standings").hidden = which !== "race"; $("stClock").hidden = which !== "mission";
    $("briefOv").hidden = true; briefing = false;
  }
  function setControls(sem, tiller, sheet, hideSheetOff){
    allowSem = sem; allowTiller = tiller; allowSheet = sheet;
    $("sem").hidden = sem.length === 0;
    $("sem").querySelectorAll("button").forEach(b => { b.disabled = !sem.includes(b.dataset.a); if (b.disabled) b.classList.remove("held"); });
    $("direct").hidden = !tiller && !sheet;
    $("ctlTiller").classList.toggle("off", !tiller); $("tiller").disabled = !tiller;
    $("ctlSheet").classList.toggle("off", !sheet); $("sheet").disabled = !sheet;
    $("ctlSheet").hidden = !sheet && !!hideSheetOff; // lezione 1: il cursore spento della scotta non serve e ruberebbe spazio
    releaseKeys();
  }
  let hudLevel = 0;
  function setHud(level){
    hudLevel = level;
    // pannello ridotto (0.16): fuori dalle lezioni sbandamento, scarroccio e venti si vedono già sullo schermo (indicatore, freccia della velocità, rosa)
    const extra = mode !== "lesson" && !opt.allInstr;
    $("instr").querySelectorAll("[data-l]").forEach(d => d.hidden = +d.dataset.l > level || (extra && d.hasAttribute("data-x")));
    if (mode === "lesson" && lessonIdx < 2) $("iAnd").parentElement.hidden = true; // le andature si spiegano nella lezione 3
    $("instr").hidden = level === 0;
  }
  function setWhere(t){ $("where").textContent = t; }
  // ---- registro degli errori (lezioni, prove, regate) ----
  // Nelle lezioni un passo può chiedere apposta un «errore» (allow): lì quel tipo non conta.
  const REG_ZERO = () => ({ capsizes: 0, gybesV: 0, irons: 0, ironsSec: 0, wrongMarks: 0, contacts: 0, contactsPen: 0, ocs: 0, outLine: 0 });
  let reg = REG_ZERO(), ironsT = 0, ironsFree = false;
  const IRONS_A = 40, IRONS_U = 1 / 1.944, IRONS_T = 3; // prua a meno di 40° dal vento, sotto 1 nodo, per almeno 3 s di fila
  function regReset(){ reg = REG_ZERO(); ironsT = 0; ironsFree = false; }
  function regClosed(){
    if (mode === "mission") return S.finished;
    if (mode === "race") return !R || R.boats[0].fin !== null || !!R.boats[0].dnf;
    return mode !== "lesson";
  }
  function regAllowed(kind){ const st = mode === "lesson" ? curStep() : null; return !!(st && st.allow && st.allow.includes(kind)); }
  function regAdd(kind, n = 1){ if (regClosed() || regAllowed(kind)) return; reg[kind] += n; }
  function ironsCheck(dt){
    const A = Math.abs(norm180(local.twd - S.h));
    const preStart = mode === "race" && R && R.t < 0;
    if (regClosed() || preStart || S.capsized || A >= IRONS_A || S.u >= IRONS_U){ ironsT = 0; ironsFree = false; return; }
    if (regAllowed("irons")) ironsFree = true; // un episodio iniziato in un passo che lo chiede non conta neppure se prosegue nel passo dopo
    ironsT += dt;
    if (ironsFree) return;
    if (ironsT >= IRONS_T && ironsT - dt < IRONS_T){ reg.irons++; reg.ironsSec += IRONS_T; }
    else if (ironsT > IRONS_T) reg.ironsSec += dt;
  }
  // 0.20.2: fasi del suggerimento «all'indietro» in S.indietro: 0 niente, 1 barra verso il boma, 2 centra e cazza,
  // 3 barca che ha smesso di arretrare. Isteresi: dalla fase 2 si torna alla 1 solo sotto IRONS_A − 3° (37°),
  // perché con le raffiche la prua oscilla attorno alla soglia e il testo lampeggiava. La fase 3 resta armata a qualunque angolo
  // finché la barca è sotto 1 nodo, per al massimo 10 s dalla fine dell'arretramento (ipotesi nostra: sul motore la barca supera
  // 1 nodo in 4,8 s al massimo); il testo B si mostra solo con la prua ad almeno 37°. Si azzera con una barca nuova (freshState) e in scuffia.
  function backCheck(dt){
    const A = Math.abs(norm180(local.twd - S.h));
    if (S.u < -0.05){ S.indietro = A >= IRONS_A || (S.indietro === 2 && A >= IRONS_A - 3) ? 2 : 1; S.indietroT = 0; }
    else { S.indietroT = (S.indietroT || 0) + dt; S.indietro = S.indietro && S.u < IRONS_U && S.indietroT <= 10 ? 3 : 0; }
  }
  const regTotal = () => reg.capsizes + reg.gybesV + reg.irons + reg.wrongMarks + reg.contactsPen + reg.ocs + reg.outLine; // 0.21.1: un contatto senza colpa si scrive ma non conta
  function regText(){
    const n = (k, one, many) => k === 1 ? one : k + " " + many, parts = [];
    if (reg.capsizes) parts.push(n(reg.capsizes, "1 scuffia", "scuffie"));
    if (reg.gybesV) parts.push(n(reg.gybesV, "1 strambata a vela aperta", "strambate a vela aperta"));
    if (reg.irons) parts.push("piantato " + (reg.irons === 1 ? "1 volta" : reg.irons + " volte") + " (" + Math.round(reg.ironsSec) + " s)");
    if (reg.wrongMarks) parts.push(n(reg.wrongMarks, "1 boa dal lato sbagliato", "boe dal lato sbagliato"));
    if (reg.contactsPen) parts.push(n(reg.contactsPen, "1 contatto con penalità", "contatti con penalità"));
    if (reg.ocs) parts.push("partenza anticipata");
    if (reg.outLine) parts.push("linea tagliata fuori dagli estremi" + (reg.outLine > 1 ? " (" + reg.outLine + " volte)" : ""));
    const free = reg.contacts - reg.contactsPen, note = free ? n(free, "1 contatto senza colpa, non conta", "contatti senza colpa, non contano") : "";
    return parts.length ? "Errori: " + parts.join(", ") + (note ? " · " + note : "") : "Errori: nessuno" + (note ? " (" + note + ")" : "");
  }
  function regShow(el, corto){ // corto (1.0.77, regate in corso, osservazione 78): solo il numero; l'elenco resta al passaggio del mouse e a fine regata
    const t = regText(), n = regTotal();
    el.textContent = corto ? (n ? "Errori: " + n + " (l'elenco a fine regata)" : "Errori: nessuno") : t; el.title = t; el.classList.toggle("some", n > 0); }

  // ---- riquadro delle istruzioni ----
  // istruzioni di prove e regate: riquadro sul mare a gioco fermo; il tempo parte con «Parti»
  let briefing = false, briefSkip = false; // briefSkip: solo per i collaudi automatici
  function showBrief(title, text, first){
    $("bTitle").textContent = title; $("bText").textContent = text;
    $("bRaceOpts").hidden = mode !== "race" || !first || !!R.es; // 1.2.1: l'esercizio di una lezione ha avversari e preparazione suoi
    $("bNote").textContent = !first ? "Il gioco è fermo finché non riprendi." : mode === "race" ? (R.t < 0 ? "Il conto alla rovescia parte quando premi Parti (o Invio)." : "Il gioco parte quando premi Parti (o Invio).") : "Il cronometro parte quando premi Parti (o Invio).";
    $("bGo").textContent = first ? "Parti" : "Riprendi";
    releaseKeys();
    briefing = true; $("briefOv").hidden = false;
    if (first && briefSkip) return hideBrief();
    setTimeout(() => $("bGo").focus(), 0);
  }
  function hideBrief(){ briefing = false; $("briefOv").hidden = true; $("c").focus(); }

  // ---- lezioni ----
  function startLesson(i){
    mode = "lesson"; lessonIdx = i; showCards("lesson"); regReset();
    setWhere(LESSONS[i].name + ": " + LESSONS[i].title);
    env.twd = 0; env.tws = 10 / KN; setGusts(0);
    freshState(0, 0, 90, 0.4);
    showStep(0);
  }
  function showStep(i){
    const steps = LESSONS[lessonIdx].steps, st = steps[i], prev = steps[i - 1];
    stepIdx = i; stepDone = false; holdT = 0;
    const e = st.env || { tws: 10, gusts: 0 };
    if (Math.abs(env.tws - e.tws / KN) > 0.01) env.tws = e.tws / KN;
    if (gustLevel !== e.gusts) setGusts(e.gusts);
    if (st.pause) freshState(0, 0, 90, 0.4);
    else if (!prev || prev.pause) { freshState(0, 0, 90, st.autoTrim ? 0.4 : 0.3); }
    // 1.0.2: «La scuffia» non fa raddrizzare (la barca resta rovesciata fino al passo dopo); «Raddrizzare» parte sempre con la barca rovesciata
    if (st.noRight && S.capsized) freshState(0, 0, 90, 0.4);
    if (st.scenaH !== undefined) freshState(0, 0, st.scenaH, 0.4); // 1.1.9: la prua della barca nelle pagine con una scena (lezioni D, regolamento)
    // 1.2.0 (docs/PROPOSTA-ESERCIZI-REGOLAMENTO-E-PARTENZE.md, meccanismo A): barche di scena che si muovono, un copione: vanno dritte a velocità costante
    // (b.u m/s) e, se b.orza = [inizio s, gradi, durata s], orzano piano. Niente fisica e niente guida: non si scansano mai.
    S.scenaMob = st.scenaMobile ? st.scenaMobile.map(b => ({ x: S.x + b.x, y: S.y + b.y, h: b.h, h0: b.h, u: b.u, orza: b.orza, t: 0, col: b.col, label: b.label })) : null;
    // 1.1.5: la barca parte ferma nell'angolo morto, con la prua a 10° dal vento e la vela tutta lascata (lezione B2, spingere il boma)
    if (st.startIrons){ Object.assign(S, { h: norm360(env.twd + (S.boomSide < 0 ? 10 : -10)), u: 0, vl: 0, r: 0, heel: 0, heelRate: 0, capsized: false }); ctl.sheet = 1; ctl.tiller = 0; }
    if (st.shifts) setShifts(st.shifts); // 1.1.8: salti di vento nel passo (lezione B5); freshState li spegne
    if (st.startCapsized && !S.capsized){ Object.assign(S, { capsized: true, indietro: 0, capCause: "heel", capSide: S.boomSide, u: 0, vl: 0, r: 0, heel: 90, heelRate: 0, righting: 0 }); }
    base = { tacks: S.tacks, gybesV: S.gybesV, gybesC: S.gybesC, capsizes: S.capsizes, cap0: S.capsized, gapMin: 1e9, gapVirata: 1e9 };
    S.markReached = false;
    // 0.20.2: il punto del passo è una linea d'arrivo (FIN_HALF m per lato), perpendicolare alla direzione dalla partenza del passo all'arrivo
    S.lessonMark = st.mark ? { x: S.x + st.mark[0], y: S.y + st.mark[1], label: "Arrivo", fin: true, nx: st.mark[0] / Math.hypot(...st.mark), ny: st.mark[1] / Math.hypot(...st.mark) } : null;
    if (st.course) S.course = Math.round(norm360(S.h) / 5) * 5;
    S.rottaScuola = !st.tiller && !st.pause ? S.h : null; // 1.1.3: rotta tenuta dalla scuola nei passi senza barra (vedi applyInput)
    $("lStep").textContent = "Passo " + (i + 1) + " di " + steps.length;
    $("lTitle").textContent = st.title;
    $("lText").innerHTML = st.text.map(t => "<p>" + (typeof t === "function" ? t() : t) + "</p>").join("");
    // 0.18.1: solo nei passi con pulsanti Cazza/Lasca lo spazio resta riservato (invisibile, non "hidden"),
    // cosi' completare il passo non sposta quei pulsanti sotto al puntatore di chi clicca piu' volte di fila.
    // Altrove si torna al comportamento di prima (spazio zero finche' il passo non e' completato).
    const semBtns = !!(st.sem && st.sem.length);
    $("lFeedback").innerHTML = st.done ? "<p>" + st.done + "</p>" : "";
    $("lFeedback").classList.toggle("pending", semBtns); $("lFeedback").hidden = !semBtns;
    $("lBack").hidden = i === 0;
    $("lRetry").hidden = !!st.pause;
    $("lNext").classList.toggle("pending", semBtns && !!st.cond); $("lNext").hidden = !semBtns && (!!st.cond || !!st.esercizio);
    $("lEs").hidden = !st.esercizio; $("lEs").textContent = "Apri l'esercizio"; $("lEs").classList.add("primary"); // 1.2.1: il passo apre una regata (meccanismo B)
    $("lNext").textContent = st.final ? nextLabel() : "Avanti";
    $("lQuiz").hidden = !st.final || !!LESSONS[lessonIdx].nascosta; // 1.1.4: il quiz delle lezioni nuove arriva col menu nuovo
    if (st.final){ progress.done["l" + lessonIdx] = true; saveProgress(); }
    setControls(st.sem || [], !!st.tiller, !!st.sheet, st.turnHint);
    setHud(st.hud || 0);
    $("hint").hidden = st.pause || st.hintKind === "none" || !st.hud;
  }
  // muove le barche di scena e misura, rispetto alla prima: base.gapMin distanza minima fra gli scafi (m), base.contatto, base.dietro (le hai attraversato
  // la rotta passando dietro la sua poppa di almeno 2 m), base.davanti (la tua poppa è almeno 2 m davanti alla sua prua), base.gapVirata (distanza minima mentre
  // la tua prua è a meno di 30° dal vento, cioè durante la virata)
  function scenaMuovi(dt){
    S.scenaMob.forEach((b, i) => {
      b.t += dt;
      if (b.orza){ const k = clamp((b.t - b.orza[0]) / b.orza[2], 0, 1); b.h = norm360(b.h0 + sgn(norm180(env.twd - b.h0)) * b.orza[1] * k); }
      b.x += Math.sin(b.h * D2R) * b.u * dt; b.y -= Math.cos(b.h * D2R) * b.u * dt;
      if (i || S.capsized) return;
      const gap = -polySep(hullWorld(S), hullWorld(b), S.x, S.y, b.x, b.y).pen;
      base.gapMin = Math.min(base.gapMin, gap);
      if (Math.abs(norm180(local.twd - S.h)) < 30) base.gapVirata = Math.min(base.gapVirata, gap);
      if (gap <= 0 && !base.contatto){ base.contatto = true; toast("Contatto: dovevi lasciare strada. Premi Ricomincia."); }
      const rx = S.x - b.x, ry = S.y - b.y, along = rx * Math.sin(b.h * D2R) - ry * Math.cos(b.h * D2R), side = rx * Math.cos(b.h * D2R) + ry * Math.sin(b.h * D2R);
      if (base.latoScena !== undefined && Math.sign(side) !== Math.sign(base.latoScena) && along < -4.1) base.dietro = true; // poppa a -2,1 m, più 2 m
      if (along > 6.2) base.davanti = true;                                                                              // sua prua a +2,1, tua poppa a 2,1 da te, più 2 m
      base.latoScena = side;
    });
  }
  // 1.2.1 (meccanismo B): dall'esercizio si torna al suo passo, con la barca ferma come in ogni pagina; ok = obiettivo raggiunto
  function tornaLezione(es, ok){
    mode = "lesson"; lessonIdx = es.lezione; showCards("lesson"); regReset();
    setWhere(LESSONS[es.lezione].name + ": " + LESSONS[es.lezione].title);
    env.twd = 0; env.tws = 10 / KN; setGusts(0);
    freshState(0, 0, 90, 0.4);
    showStep(es.passo);
    if (ok){ completeStep(); $("lEs").textContent = "Rifai l'esercizio"; $("lEs").classList.remove("primary"); }
  }
  function completeStep(){
    stepDone = true;
    $("lFeedback").classList.remove("pending"); $("lFeedback").hidden = false;
    $("lNext").classList.remove("pending"); $("lNext").hidden = false;
  }
  $("lNext").onclick = () => { const st = curStep(); if (st.final) return goNext(); showStep(Math.min(LESSONS[lessonIdx].steps.length - 1, stepIdx + 1)); };
  $("lBack").onclick = () => showStep(Math.max(0, stepIdx - 1));
  $("lQuiz").onclick = () => openQuiz(lessonIdx);
  $("lEs").onclick = () => apriEsercizio(lessonIdx, stepIdx);
  $("lRetry").onclick = () => { freshState(0, 0, 90, curStep().autoTrim ? 0.4 : 0.3); showStep(stepIdx);
    const q = curStep().ripresa; // 1.2.13: vedi «ripresa» in contenuti.js
    if (q){ if (q.twa !== undefined){ S.h = norm360(env.twd + q.twa); S.r = 0; } if (q.u !== undefined){ S.u = q.u; S.vl = 0; } if (q.sheet !== undefined) ctl.sheet = q.sheet; } };

  // ---- giro di boa (boe da lasciare a sinistra) ----
  // La boa è girata quando la barca attraversa la semiretta che parte dalla boa verso l'esterno della curva del percorso,
  // girando in senso antiorario (visto dall'alto, con il nord in alto). Attraversarla in senso orario vuol dire girarla dal lato
  // sbagliato, e va "disfatto" tornando indietro: come la regola del filo teso delle regate (il conto netto deve arrivare a 1).
  const bearingTo = (a, b) => norm360(Math.atan2(b.x - a.x, -(b.y - a.y)) / D2R); // direzione di b vista da a, da nord in senso orario
  function markOut(prev, mk, next){ // direzione esterna della curva: opposta alla bisettrice tra "da dove arrivo" e "dove vado"
    const u = p => { const dx = p.x - mk.x, dy = p.y - mk.y, d = Math.hypot(dx, dy) || 1; return [dx / d, dy / d]; };
    const [ax, ay] = u(prev), [bx, by] = u(next);
    return norm360(Math.atan2(-(ax + bx), (ay + by)) / D2R);
  }
  function roundCheck(o, x, y, mk){ // +1 giro giusto, -1 giro dal lato sbagliato, 0 niente
    const d = Math.hypot(x - mk.x, y - mk.y);
    if (d < 1.5) return 0; // sopra la boa: direzione indefinita
    const a = norm180(bearingTo(mk, { x, y }) - mk.out), pa = o.rndA; o.rndA = a;
    if (pa === undefined || Math.abs(a) > 90 || Math.abs(pa) > 90 || (pa >= 0) === (a >= 0)) return 0;
    const k = pa >= 0 ? 1 : -1; o.rnd = (o.rnd || 0) + k; return k;
  }
  // freccia curva attorno a una boa: il verso in cui girarla
  function drawRoundArrow(mk, r, col){
    const c0 = (mk.out + 55 - 90) * D2R, c1 = (mk.out - 55 - 90) * D2R;
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 0.22; ctx.lineCap = "round";
    ctx.beginPath(); ctx.arc(mk.x, mk.y, r, c0, c1, true); ctx.stroke();
    const ex = mk.x + Math.cos(c1) * r, ey = mk.y + Math.sin(c1) * r, tx = Math.sin(c1), ty = -Math.cos(c1), nx = Math.cos(c1), ny = Math.sin(c1);
    ctx.beginPath(); ctx.moveTo(ex + tx * 1.4, ey + ty * 1.4); ctx.lineTo(ex + nx * 0.8, ey + ny * 0.8); ctx.lineTo(ex - nx * 0.8, ey - ny * 0.8); ctx.closePath(); ctx.fill();
  }
  // taglio della linea d'arrivo fra due posizioni consecutive: frazione del passo (0-1) in cui avviene, -1 se non c'è,
  // -2 se la linea è attraversata fuori dagli estremi. Conta solo dal lato del percorso verso l'arrivo; le boe non fanno da ostacolo.
  const FIN_HALF = 12;
  function finCross(mk, x0, y0, x1, y1){
    const d0 = (x0 - mk.x) * mk.nx + (y0 - mk.y) * mk.ny, d1 = (x1 - mk.x) * mk.nx + (y1 - mk.y) * mk.ny;
    if (!(d0 < 0 && d1 >= 0)) return -1;
    const f = d0 / (d0 - d1), a = -((x0 + (x1 - x0) * f) - mk.x) * mk.ny + ((y0 + (y1 - y0) * f) - mk.y) * mk.nx;
    return Math.abs(a) <= FIN_HALF ? f : -2;
  }
  function roundToast(k, next){
    if (k > 0) toast("Boa girata: ora verso " + next);
    else toast("Boa girata dal lato sbagliato: torna indietro e girala lasciandola a sinistra");
  }

  // ---- prove ----
  function startMission(i, wind){
    mode = "mission"; missionIdx = i; showCards("mission"); regReset();
    const m = MISSIONS[i];
    setWhere("Prova " + (i + 1) + ": " + m.title);
    env.twd = wind === undefined ? m.wind : wind; env.tws = m.tws / KN;
    curMarks = m.marks.map(mk => { const [x, y] = fromWF(mk.x, mk.y); return { x, y, label: mk.label }; });
    const [sx, sy] = fromWF(m.start.x, m.start.y);
    curMarks.forEach((mk, k) => { if (k < curMarks.length - 1){ mk.round = true; mk.out = markOut(k ? curMarks[k - 1] : { x: sx, y: sy }, mk, curMarks[k + 1]); } });
    // linea d'arrivo: centrata sull'ultima voce, perpendicolare all'ultimo lato; (nx, ny) punta dal lato del percorso verso l'arrivo
    const fin = curMarks[curMarks.length - 1], pv = curMarks.length > 1 ? curMarks[curMarks.length - 2] : { x: sx, y: sy }, fd = Math.hypot(fin.x - pv.x, fin.y - pv.y);
    Object.assign(fin, { fin: true, nx: (fin.x - pv.x) / fd, ny: (fin.y - pv.y) / fd });
    freshState(sx, sy, norm360(m.start.h + env.twd), m.start.sheet);
    setGusts(m.gusts);
    recStart(recK("m" + i));
    $("mTitle").textContent = "Prova " + (i + 1) + ". " + m.title;
    $("mNext").textContent = nextLabel(); $("mNext").parentElement.hidden = !nextItem(); // l'ultima prova della Scuola: «Torna al menu» c'è già in alto
    setControls([], true, true); setHud(3); $("hint").hidden = !opt.hint;
    showBrief($("mTitle").textContent, missionText(), true);
  }
  const bandText = b => "Tempi delle medaglie: oro entro " + fmtTime(b[0]) + ", argento entro " + fmtTime(b[1]) + ", bronzo entro " + fmtTime(b[2]) + ".";
  const missionText = () => { const m = MISSIONS[missionIdx]; return m.text + " Vento da " + cardName(env.twd) + ", " + m.tws + " nodi." + centerNote() + " " + bandText(m.bands); };
  $("mBrief").onclick = () => showBrief($("mTitle").textContent, missionText(), false);
  $("bGo").onclick = hideBrief;
  $("mRetry").onclick = () => startMission(missionIdx, env.twd);
  $("mWind").onclick = () => startMission(missionIdx, otherWind());
  $("mNext").onclick = goNext;

  // ---- navigazione libera ----
  function startFree(){
    mode = "free"; showCards("free"); regReset(); setWhere("Navigazione libera");
    env.twd = freeEnv.twd; env.tws = freeEnv.tws / KN;
    curMarks = [{ x: 0, y: -160, label: "Boa 1" }, { x: 110, y: -40, label: "Boa 2" }, { x: -110, y: -40, label: "Boa 3" }];
    freshState(0, 30, norm360(env.twd + 90), 0.3);
    setShifts("osc"); // i salti di vento della barca dell'1b (1.0.28)
    setGusts(freeEnv.gusts);
    setControls([], true, true); setHud(3); $("hint").hidden = !opt.hint;
  }
  $("wDir").onchange = e => { freeEnv.twd = +e.target.value; env.twd = freeEnv.twd; setGusts(gustLevel); };
  $("wSpd").onchange = e => { freeEnv.tws = +e.target.value; env.tws = freeEnv.tws / KN; };
  $("gustSel").onchange = e => { freeEnv.gusts = +e.target.value; setGusts(freeEnv.gusts); };

  // ======================================================================
  // INPUT
  // ======================================================================
  const keys = new Set(), semHeld = new Set();
  const releaseKeys = () => { keys.clear(); semHeld.clear(); }; // all'apertura di finestre e riquadri: niente tasti rimasti «premuti»
  let dragTiller = false, tillerAim = null;
  const KEYSEM = { w: "cazza", s: "lasca" }, KEYARR = { w: "ArrowUp", s: "ArrowDown" };
  function semPress(a){
    if (!allowSem.includes(a) || semHeld.has(a)) return;
    semHeld.add(a);
    const b = $("sem").querySelector(`[data-a="${a}"]`); b && b.classList.add("held");
  }
  function semRelease(a){ semHeld.delete(a); const b = $("sem").querySelector(`[data-a="${a}"]`); b && b.classList.remove("held"); }
  addEventListener("keydown", e => {
    if (briefing && !$("gloss").open && !$("setDlg").open && e.key === "Enter"){ e.preventDefault(); hideBrief(); return; }
    if (mode === "menu" || briefing || $("gloss").open || $("quiz").open || $("setDlg").open || e.target.tagName === "INPUT" && e.target.type === "search" || e.target.closest?.("#lab")) return; // 1.0.4: i tasti dentro il laboratorio non guidano la barca
    let k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    if (KEYSEM[k]){ // 1.0.30: W e S valgono sempre come ↑ e ↓; i pulsanti della lezione 1 restano com'erano
      if (allowSem.length){ semPress(KEYSEM[k]); e.preventDefault(); return; }
      k = KEYARR[k];
    }
    if (k === "1" || k === "2"){ if (!sesTyping()) userZoom = k === "1" ? Math.min(3, userZoom * 1.25) : Math.max(ZMIN, userZoom / 1.25); return; } // 1.0.48: zoom coi tasti vicini a Q, al posto dei pulsanti + e − (idea di Ale)
    if (k === "a"){ rightBoat(); return; } // 1.0.27: raddrizza con A (era R; R resta libero per le manovre dei livelli futuri, decisione di Ale)
    if (k === "Shift"){ keys.add(k); return; } // 1.0.24: Maiusc + freccia, la barra arriva fino a 45°
    if (k === "q"){ if (!sesTyping()) keys.add("q"); return; } // vista, tenuto premuto (anche con Bloc Maiusc: k è minuscolo)
    if (k === "z"){ if (!sesTyping()) keys.add("z"); return; } // 1.0.26: spingi il boma, tenuto premuto
    if (["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," "].includes(k)){
      if (e.target.tagName === "SELECT") return;
      e.preventDefault(); keys.add(k);
      if (k === " " && allowTiller) ctl.tiller = 0;
    }
  });
  addEventListener("keyup", e => { const k = e.key.length === 1 ? e.key.toLowerCase() : e.key; keys.delete(KEYARR[k] || k); if (KEYSEM[k]) semRelease(KEYSEM[k]); });
  addEventListener("blur", () => { keys.clear(); [...semHeld].forEach(semRelease); });
  $("sem").querySelectorAll("button").forEach(btn => {
    const a = btn.dataset.a;
    btn.addEventListener("pointerdown", e => { e.preventDefault(); btn.setPointerCapture?.(e.pointerId); semPress(a); });
    ["pointerup","pointercancel","lostpointercapture"].forEach(ev => btn.addEventListener(ev, () => semRelease(a)));
    btn.addEventListener("contextmenu", e => e.preventDefault());
  });
  $("tiller").addEventListener("input", e => { tillerAim = e.target.value / 100; dragTiller = true; });
  ["pointerup","change","touchend"].forEach(ev => $("tiller").addEventListener(ev, () => dragTiller = false));
  $("sheet").addEventListener("input", e => { autoSheetSpegni(); ctl.sheet = e.target.value / 100; });
  function seg(id, key){
    $(id).addEventListener("click", e => {
      const b = e.target.closest("button"); if (!b) return;
      opt[key] = b.dataset.v; $(id).querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b));
    });
  }
  seg("helmMode", "helm"); seg("viewMode", "view");
  $("autoCenter").onchange = e => opt[centerKey()] = e.target.checked;
  $("autoSheetOpt").onchange = e => { opt.autoSheet = e.target.checked; };
  $("showHint").onchange = e => { opt.hint = e.target.checked; if (mode !== "lesson") $("hint").hidden = !opt.hint; };
  $("showArrows").onchange = e => opt.arrows = e.target.checked;
  $("showDead").onchange = e => opt.dead = e.target.checked;
  $("showSem").onchange = e => opt.sem = e.target.checked; // 1.0.40: spento di default
  $("allInstr").onchange = e => { opt.allInstr = e.target.checked; setHud(hudLevel); };
  $("showGhost").onchange = e => opt.ghost = e.target.checked;
  const otherWind = () => { let w; do { w = Math.floor(Math.random() * 8) * 45; } while (w === env.twd); return w; };
  $("rRestart").onclick = () => R && R.es ? apriEsercizio(R.es.lezione, R.es.passo) : startRace(raceIdx, env.twd);
  // 1.0.70: «Cambia vento» tolto dalle regate; 1.0.75: rimesso nel pannello e nella schermata finale delle regate (rWind, finWind in regate.js), mai nel torneo; nelle prove c'è sempre (mWind)
  $("rBrief").onclick = () => showBrief($("rTitle").textContent, R.brief, false);
  $("aiLevel").onchange = e => { opt.aiLevel = e.target.value; startRace(raceIdx, env.twd); };
  $("cdSel").onchange = e => { opt.countdown = +e.target.value; startRace(raceIdx, env.twd); };
  // zoom minimo 0,1 (0.19.3): a 1360x650 un obiettivo a 300 m resta sullo schermo con la barca al margine (vedi CHANGELOG)
  const ZMIN = 0.1;
  canvas.addEventListener("wheel", e => { e.preventDefault(); userZoom = clamp(userZoom * (e.deltaY > 0 ? 0.9 : 1.1), ZMIN, 3); }, { passive: false });
  canvas.addEventListener("pointerdown", () => canvas.focus());
  const updFocus = () => $("focusTip").hidden = mode === "menu" || document.hasFocus();
  addEventListener("focus", updFocus); addEventListener("blur", updFocus); setInterval(updFocus, 1000);
  function rightBoat(){ const st = curStep(); if (st && st.noRight) return; if (S && S.capsized && !S.righting) S.righting = 0.001; }
  $("rightBtn").onclick = rightBoat; $("capBtn").onclick = rightBoat;

  function applyInput(dt){
    let tillerInput = false;
    ctl.push = keys.has("z") && !S.capsized; // 1.0.26: boma spinto finché Z è premuto (docs/archivio/PROPOSTA-SPINGI-BOMA.md)
    if (tillerAim !== null){ // il cursore trascinato col mouse muove la barra al più alla velocità di Maiusc + freccia
      const d = tillerAim - ctl.tiller, m = 1.6 * dt; ctl.tiller = Math.abs(d) <= m ? tillerAim : ctl.tiller + Math.sign(d) * m; tillerInput = true;
      if (!dragTiller && ctl.tiller === tillerAim) tillerAim = null;
    }
    if (allowTiller){
      const l = keys.has("ArrowLeft"), r = keys.has("ArrowRight");
      if (l || r){
        let dir = (r ? 1 : 0) - (l ? 1 : 0);
        if (opt.helm === "prua") dir = -dir * (S.u < 0 ? -1 : 1);
        // 1.0.25: la sola freccia porta la barra fino a 35° (RUD2_SICURA), Maiusc + freccia fino a 45°; sempre alla stessa velocità
        const lim = !keys.has("Shift") ? Math.max(RUD2_SICURA, Math.abs(ctl.tiller)) : 1;
        ctl.tiller = clamp(ctl.tiller + dir * 1.6 * dt, -lim, lim); tillerInput = true;
      }
    }
    // lezione 1: la barra torna al centro in fretta, così la prua smette di girare appena si rilascia la freccia
    const quick = allowSem.length || (mode === "lesson" && curStep() && curStep().turnHint);
    if (!tillerInput && (opt[centerKey()] || quick) && !dragTiller){
      ctl.tiller *= Math.exp((quick ? -6 : -2.5) * dt); if (Math.abs(ctl.tiller) < 0.01) ctl.tiller = 0;
    }
    // 1.1.3 (docs/PROPOSTA-LEZIONI-SCUOLA.md, gruppo A): nei passi delle lezioni senza barra la rotta la tiene la scuola, come la vela nei passi con autoTrim.
    // La barca dell'1b orza da sola sbandando (1.0.46): a barra ferma nei passi sulla scotta finiva vicino all'angolo morto (passo 3.10: da 90° a 32° dal vento)
    if (mode === "lesson" && S.rottaScuola != null && !allowTiller && !S.capsized && S.u > 0.3) ctl.tiller = clamp(norm180(S.h - S.rottaScuola) / 20 + S.r * 0.02, -0.6, 0.6);
    S.tilAttivo = tillerInput; // 1.1.3: la barra si sta muovendo per mano del giocatore (tasti o cursore), per i passi che lo chiedono
    if (autoSheetAttiva() && allowSheet && (keys.has("ArrowUp") || keys.has("ArrowDown"))) autoSheetSpegni(); // i tasti della scotta tolgono l'automatismo
    if ((allowSheet || allowSem.includes("cazza")) && keys.has("ArrowUp") || semHeld.has("cazza")) ctl.sheet = Math.max(0, ctl.sheet - 0.27 * dt);
    if ((allowSheet || allowSem.includes("lasca")) && keys.has("ArrowDown") || semHeld.has("lasca")) ctl.sheet = Math.min(1, ctl.sheet + 0.27 * dt);
  }

  // ======================================================================
  // SIMULAZIONE
  // ======================================================================
  let GYBE_KICK = 260; // gradi/s: circa 19° di sbandamento con 6 nodi, 45° con 10, scuffia con 15
  function toast(text, t = 2.6){ S.toast = { text, t }; }
  function detectManeuvers(){
    const twa = norm180(local.twd - S.h), side = sgn(twa), A = Math.abs(twa);
    if (side === S.prevSide || A < 1 || A > 179) return;
    const mure = side > 0 ? "mure a dritta" : "mure a sinistra";
    if (A < 90){ S.tacks++; S.boomRate = 3; toast("Virata: ora " + mure); }
    else {
      const sheetMax = BOAT.minBoom + ctl.sheet * (BOAT.maxBoom - BOAT.minBoom);
      if (sheetMax > 45){ S.gybesV++; regAdd("gybesV"); S.gybeAt = simTime; S.u *= 0.55; S.heelRate += GYBE_KICK * D2R * Math.pow(local.tws / (15 / KN), 1.6) * (0.85 + Math.random() * 0.4); // colpo del boma in gradi/s (il motore usa radianti/s); più vento, colpo più forte
        S.shake = 0.5; S.boomRate = 22; toast("Strambata violenta!"); }
      else { S.gybesC++; S.boomRate = 8; toast("Strambata: ora " + mure); }
    }
    S.prevSide = side;
  }
  function simulate(dt, st){
    const px0 = S.x, py0 = S.y; // posizione prima del passo: serve al taglio della linea d'arrivo
    applyInput(dt);
    if (st && st.autoTrim) ctl.sheet = autoSheet();
    else if (autoSheetAttiva()){ ctl.sheet = autoSheet(true); S.autoUsed = true; } // la barca scuffiata non regola; il segno resta per la prova in corso
    if (st && st.yawNoise && !S.capsized){ // onde: spinte irregolari sulla prua
      S.noiseT = (S.noiseT || 0) - dt;
      if (S.noiseT <= 0){ S.noiseT = 1.8 + Math.random() * 1.6; S.noiseR = (Math.random() < 0.5 ? -1 : 1) * (3 + Math.random() * 3); S.noiseLeft = 0.8; }
      if (S.noiseLeft > 0){ S.noiseLeft -= dt; S.h = norm360(S.h + S.noiseR * dt); }
      S.h = norm360(S.h + sgn(norm180(local.twd - S.h)) * 3 * dt); // la barca tende a orzare da sola (orziera). 3°/s e non 2: con 2 le spinte delle onde (3-6°/s) potevano cancellarla per gli 8 s dell'esercizio e il passo si completava da sé una volta su otto
    }
    if (st && st.bigGust && !S.capsized){
      // se non c'è una raffica forte in arrivo vicino alla barca, ne crea una
      const to = (env.twd + 180) * D2R, ux = S.x - Math.sin(to) * 20, uy = S.y + Math.cos(to) * 20;
      if (gustAt(ux, uy) < 0.3 && gustAt(S.x, S.y) < 0.3 && !gusts.some(g => g.big && g.age < 12)){
        let lat = 0;
        if (st.bigGust !== true){ // raffica media: nasce dove la barca arriverà, non dritta sopravento (la barca di bolina si sposta di lato)
          const vx = S.u * Math.sin(S.h * D2R), vy = -S.u * Math.cos(S.h * D2R), ax = Math.sin(to), ay = -Math.cos(to);
          lat = (vx * -ay + vy * ax) * 45 / (env.tws * 0.8 + Math.max(0, -(vx * ax + vy * ay)));
        }
        spawnGust(45, lat, true); const g = gusts[gusts.length - 1]; g.k = st.bigGust === true ? 0.8 : st.bigGust; g.r = 18; g.sh = 0; g.big = true;
      }
    }
    updateGusts(dt);
    Object.assign(local, windAt(S.x, S.y));
    if (!S.capsized){
      const n = 4; for (let i = 0; i < n; i++) info = step(S, ctl, local, dt / n);
      detectManeuvers();
      ironsCheck(dt);
      backCheck(dt);
      if (S.heel > BOAT.capsizeAt || S.heel < -45){
        S.capCause = S.gybeAt !== undefined && simTime - S.gybeAt < 4 ? "gybe" : "heel";
        S.capsized = true; S.capAt = simTime; S.indietro = 0; S.capsizes++; regAdd("capsizes"); S.capSide = S.heel > 0 ? S.boomSide : -S.boomSide; S.u = 0; S.vl = 0; S.r = 0; S.heel = 90 * Math.sign(S.heel); S.heelRate = 0;
      }
    } else {
      const to = (local.twd + 180) * D2R;
      S.x += Math.sin(to) * 0.25 * dt; S.y -= Math.cos(to) * 0.25 * dt;
      if (S.righting){
        S.righting += dt;
        if (S.righting > RADD2.t){
          const side = S.capSide; // al traverso, ferma, vela tutta lascata (RADD2; fino alla 1.0.78 l'1a ripartiva a 60° con 0,3 m/s)
          S.capsized = false; S.righting = 0; S.heel = 0; S.heelRate = 0; S.hike = 0.3; S.u = 0;
          S.h = norm360(local.twd + side * RADD2.twa); ctl.sheet = 1; ctl.tiller = 0;
          S.prevSide = sgn(norm180(local.twd - S.h));
        }
      }
    }
    S.dispBoom += (S.boomSide * S.boom - S.dispBoom) * Math.min(1, dt * S.boomRate);
    S.boomRate += (6 - S.boomRate) * Math.min(1, dt * 0.8);
    S.shake = Math.max(0, S.shake - dt);
    if (S.toast){ S.toast.t -= dt; if (S.toast.t <= 0) S.toast = null; }
    wakeT += dt;
    if (wakeT > 0.08 && !S.capsized){
      wakeT = 0; const h = S.h * D2R;
      wake.push({ x: S.x - Math.sin(h) * 2.1, y: S.y + Math.cos(h) * 2.1, nx: Math.cos(h), ny: Math.sin(h), t: simTime });
      if (wake.length > 140) wake.shift();
    }
    if (S.lessonMark && !S.markReached){
      const f = finCross(S.lessonMark, px0, py0, S.x, S.y);
      if (f >= 0) S.markReached = true; else if (f === -2) toast("Fuori dalla linea: passa tra le due boe");
    }
    if (mode === "lesson" && S.scenaMob) scenaMuovi(dt);
    // obiettivi
    if (mode === "lesson" && st.cond && !stepDone){
      // 1.1.3 (docs/PROPOSTA-LEZIONI-SCUOLA.md, gruppo A): quello che il giocatore ha fatto nel passo, per i passi che la barca dell'1b farebbe da sola
      // (orza da sola sbandando, 1.0.46): base.barraLee = secondi con la barra verso il boma (barra sottovento), base.lasca = scotta lascata in raffica
      if (S.tilAttivo && ctl.tiller * S.boomSide > 0.05) base.barraLee = (base.barraLee || 0) + dt;
      if (S.tilAttivo && Math.abs(ctl.tiller) > 0.8) base.maiusc = (base.maiusc || 0) + dt;
      if (S.pushing) base.push = (base.push || 0) + dt; // 1.1.5: secondi col boma spinto (tasto Z) // 1.1.4: barra oltre 36°, cioè con Maiusc (la sola freccia si ferma a 35°) // solo la barra mossa adesso: quella rimasta dal passo prima non conta
      if (shiftSt){ // 1.1.8 (lezione B5): base.scarso = di quanti gradi il vento è girato verso la prua rispetto al medio, letto l'ultima volta in bolina; base.buone = virate fatte da scarsi di almeno 7°; base.daBuono = una virata fatta da buoni di almeno 3°, che fa fallire il passo fino a Ricomincia; contano solo le virate cominciate da bolina (barca fra 35° e 75° dal vento negli ultimi 4 s) e volute (barra verso il boma negli ultimi 4 s: lasciata a sé, la barca orziera vira da sola) (misurato: senza, chi vira a caso completava 10 volte su 10)
        const a = norm180(local.twd - S.h);
        if (S.tilAttivo && ctl.tiller * S.boomSide > 0.05) base.tBarraLee = simTime;
        if (Math.abs(a) >= 35 && Math.abs(a) <= 75){ base.scarso = -Math.sign(a) * norm180(local.twd - env.twd); base.tScarso = simTime; }
        if (S.tacks > (base.tacksVisti ?? base.tacks)){ const sc = simTime - (base.tScarso ?? -1e9) < 4 && simTime - (base.tBarraLee ?? -1e9) < 4 ? base.scarso : 0; if (sc >= 7) base.buone = (base.buone || 0) + 1; else if (sc <= -3 && !base.daBuono){ base.daBuono = true; toast("Hai virato da buono: sulle altre mure ora sei scarso. Premi Ricomincia."); } base.tacksVisti = S.tacks; }
      }
      if (base.shPrev !== undefined && ctl.sheet > base.shPrev && local.tws > env.tws * 1.12) base.lasca = (base.lasca || 0) + ctl.sheet - base.shPrev;
      base.shPrev = ctl.sheet;
      if (st.cond(readI(), S, base)){ holdT += dt; if (holdT >= (st.hold || 0.3)) completeStep(); } else holdT = 0;
    }
    if ((mode === "mission" || mode === "free") && curMarks.length && !S.finished){
      S.time += dt;
      const mk = curMarks[S.markIdx];
      let reached = false;
      if (mode === "mission" && mk.round){
        const k = roundCheck(S, S.x, S.y, mk);
        if (k < 0){ S.wrongMarks = (S.wrongMarks || 0) + 1; regAdd("wrongMarks"); }
        if (S.rnd >= 1){ reached = true; S.rnd = 0; S.rndA = undefined; }
        else if (k < 0) roundToast(-1);
        else if (k > 0) toast("Hai rimediato: ora girala lasciandola a sinistra");
      } else if (mode === "mission" && mk.fin){
        const f = finCross(mk, px0, py0, S.x, S.y);
        if (f >= 0){ reached = true; S.time -= (1 - f) * dt; } // istante esatto del taglio
        else if (f === -2) toast("Fuori dalla linea: passa tra le due boe");
      }
      if (reached){
        if (mk.fin){
          S.finished = true;
          const sec = Math.round(S.time), key = "m" + missionIdx, bk = recK(key), prev = progress.best[bk];
          const aiuto = !!S.autoUsed; // scotta automatica: la prova si fa ma non vale record, medaglia né stella (1.0.73)
          if (!aiuto){ progress.done[key] = true; if (!prev || sec < prev){ progress.best[bk] = sec; recSave(); } }
          const clean = regTotal() === 0; if (clean && !aiuto) progress.clean[bk] = true; if (!aiuto) saveProgress();
          if (aiuto) $("doneText").textContent = "Prova completata in " + fmtTime(sec) + " con la scotta automatica: così non vale record né medaglia. Spegnila nelle impostazioni (⚙) per far valere la prova.";
          else $("doneText").textContent = "Prova completata in " + fmtTime(sec) + "." + (!prev ? "" : sec < prev ? " Nuovo record!" : " Record: " + fmtTime(prev) + ".") +
            (medalOf(missionIdx, sec) ? " Medaglia: " + MEDALS[medalOf(missionIdx, sec) - 1] + "." : " Nessuna medaglia: il bronzo è entro " + fmtTime(MISSIONS[missionIdx].bands[2]) + ".") +
            (clean ? " Nessun errore: ★ senza errori." : " " + regText() + ".");
          $("done").hidden = false; toast("Arrivato!");
        } else { S.markIdx++; toast("Boa girata: ora verso " + (curMarks[S.markIdx].fin ? "l'arrivo" : curMarks[S.markIdx].label.toLowerCase())); }
      }
      if (mode === "mission" && !S.finished) recSample(S.time, dt);
    }
    if (mode === "race") updateRace(dt);
  }

