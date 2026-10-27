// Scuola di vela, registratore.js — Registratore di sessione (0.18).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // REGISTRATORE DI SESSIONE (0.18)
  // Spento a ogni apertura della pagina; il file si crea nel browser, nessuna connessione.
  // Solo lettura: non chiama Math.random e non scrive variabili del gioco, quindi la simulazione è identica al bit con o senza.
  // Tutto per confronto fra un fotogramma e il precedente: contatori, registro, messaggi, testi, tasti, impostazioni.
  // ======================================================================
  const AND_CODE = { "Angolo morto": "AM", "Bolina stretta": "BS", "Bolina larga": "BL", "Traverso": "TR", "Lasco": "LA", "Gran lasco": "GL", "Poppa": "PO" };
  const SES_KEY = { ArrowLeft: "←", ArrowRight: "→", ArrowUp: "↑", ArrowDown: "↓", " ": "spazio", cazza: "W(cazza)", lasca: "S(lasca)", q: "Q(vista)" }; // solo i tasti del gioco
  const SES_CNT = [["tacks", "virata"], ["gybesC", "strambata"], ["gybesV", "strambata_vela_aperta"], ["capsizes", "scuffia"], ["markIdx", "boa"]];
  const ses = { on: false, offAt: null, pause: 0, start: null, set0: "", lines: [], t: 0, sim: 0, nextS: 0, dirty: false, flash: 0, marks: [], cnt: {}, andT: {}, msgN: {}, msgT: {}, stepT: {}, stepName: {}, L: null };
  const sesT = () => ses.t.toFixed(1);
  const sesLine = s => { ses.lines.push(s); ses.dirty = true; };
  const sesEv = (type, det) => { ses.cnt[type] = (ses.cnt[type] || 0) + 1; sesLine("E " + sesT() + " " + type + (det ? " " + det : "")); };
  const sesTyping = () => { const a = document.activeElement; return !!a && (a.tagName === "TEXTAREA" || a.isContentEditable || (a.tagName === "INPUT" && !["checkbox", "radio", "range", "button"].includes(a.type))); };
  const sesSet = () => "frecce=" + opt.helm + " vista=" + opt.view + " barra_al_centro=" + (opt.autoCenter ? "sì" : "no") + " barra_al_centro_prove=" + (opt.autoCenterComp ? "sì" : "no") +
    " suggerimenti=" + (opt.hint ? "sì" : "no") + " frecce_vento=" + (opt.arrows ? "sì" : "no") + " rosa_angolo_morto=" + (opt.dead ? "sì" : "no") + " tutti_strumenti=" + (opt.allInstr ? "sì" : "no") +
    " fantasma=" + (opt.ghost ? "sì" : "no") + " vento=" + Math.round(env.twd) + "° " + Math.round(env.tws * KN) + "kn raffiche=" + gustLevel + " avversari=" + opt.aiLevel + " preparazione=" + opt.countdown + "s" + (LAB ? labSet() : "");
  const sesMode = () => mode + (mode === "lesson" ? lessonIdx : mode === "mission" ? missionIdx : mode === "race" ? raceIdx : "");
  const sesModeName = () => mode === "lesson" ? "lezione " + (lessonIdx + 1) + " «" + LESSONS[lessonIdx].title + "»" : mode === "mission" ? "«" + $("mTitle").textContent + "»"
    : mode === "race" ? "regata «" + $("rTitle").textContent + "»" + (R ? " (barca " + (R.lv2 ? "1b" : "1a") + ")" : "") : mode === "free" ? "navigazione libera" : "menu";
  const sesKeys = () => [...keys, ...semHeld].filter(k => SES_KEY[k]);
  const sesDlg = () => ({ impostazioni: $("setDlg").open, glossario: $("gloss").open, quiz: $("quiz").open, istruzioni: briefing });
  const sesHint = () => mode !== "menu" && !$("hint").hidden && $("hint").textContent !== "—" ? $("hint").textContent : "";
  function sesBase(){ // fotografa lo stato attuale, senza eventi
    const L = ses.L = { mode: null, S, step: null, done: stepDone, sim: simTime, reg, regV: Object.assign({}, reg), toast: S && S.toast, keys: sesKeys(), dlg: sesDlg(),
      set: sesSet(), hint: "", cand: "", candT: 0, rule: "", err: "", leg: null, fin: S && S.finished, cap: S && S.capsized, righting: S && S.righting };
    SES_CNT.forEach(([k]) => L[k] = S ? S[k] : 0);
  }
  // ---- le altre barche della regata (1.0.52, docs/PROPOSTA-REGISTRATORE-TUTTE-LE-BARCHE.md) ----
  // Solo lettura di R: una riga B al secondo per ogni avversario (insieme alla S del giocatore), e gli eventi avv_* e contatto_barche.
  // Un contatto è un nuovo valore in R.contacts (la definizione del gioco); il motivo è la voce nuova di R.penList (righe Q).
  // «Fermo»: sotto FERMO_KN per FERMO_S secondi di gioco dopo il via; «riparte» sopra RIPARTE_KN (ipotesi nostre, isteresi).
  const FERMO_KN = 0.5, RIPARTE_KN = 1, FERMO_S = 5;
  const sesAvv = b => ({ leg: b.leg, ocs: b.ocs, cap: b.S.capsized, fin: b.fin !== null, pen: b.pen || 0, pp: b.pp || 0, sba: b.leg >= 1 && b.leg <= R.marks.length && b.rnd < 0, still: 0, fermo: false });
  function sesAltre(dSim, riga){
    const L = ses.L;
    if (mode !== "race" || !R){ L.AR = null; return; }
    if (R !== L.AR){ L.AR = R; L.A = {}; R.boats.forEach(b => { if (!b.me) L.A[b.name] = sesAvv(b); }); L.ct = Object.assign({}, R.contacts); L.pl = R.penList.length; } // accesa a regata in corso: le voci già presenti non si scrivono
    for (const b of R.boats){
      if (b.me) continue;
      const A = L.A[b.name], n = b.name, kn = Math.abs(b.S.u) * KN;
      if (b.leg > A.leg) sesEv("avv_lato", n + " " + b.leg);
      if (b.ocs && !A.ocs) sesEv("avv_ocs", n);
      if (b.S.capsized && !A.cap) sesEv("avv_scuffia", n);
      if (b.fin !== null && !A.fin) sesEv("avv_arrivo", n + " " + Math.round(b.fin) + "s");
      if ((b.pen || 0) > A.pen) sesEv("avv_penalita", n + " +" + ((b.pen || 0) - A.pen) + "s");
      if ((b.pp || 0) > A.pp) sesEv("avv_penalita", n + " +" + ((b.pp || 0) - A.pp) + "pt");
      const sba = b.leg >= 1 && b.leg <= R.marks.length && b.rnd < 0;
      if (sba && !A.sba) sesEv("avv_boa_lato_sbagliato", n);
      if (dSim > 0 && R.t >= 0 && b.fin === null && !b.dnf){
        if (!A.fermo){ A.still = kn < FERMO_KN ? A.still + dSim : 0;
          if (A.still >= FERMO_S){ A.fermo = true; sesEv("avv_fermo", n + " lato " + b.leg + " " + b.S.x.toFixed(1) + " " + b.S.y.toFixed(1)); } }
        else if (kn > RIPARTE_KN){ A.fermo = false; A.still = 0; sesEv("avv_riparte", n); }
      }
      Object.assign(A, { leg: b.leg, ocs: b.ocs, cap: b.S.capsized, fin: b.fin !== null, pen: b.pen || 0, pp: b.pp || 0, sba });
    }
    for (const key in R.contacts) if (L.ct[key] !== R.contacts[key]){ const [i, j] = key.split("-"); sesEv("contatto_barche", R.boats[i].name + " " + R.boats[j].name); }
    L.ct = Object.assign({}, R.contacts);
    for (; L.pl < R.penList.length; L.pl++) sesLine("Q " + sesT() + " " + R.penList[L.pl]);
    if (riga) for (const b of R.boats){
      if (b.me) continue;
      const st = [b.ocs && "ocs", b.S.capsized && "scuf", b.fin !== null && "arr", b.dnf && "dnf", b.goStart && b.leg === 0 && "via", b.cedeA && "cede:" + b.cedeA.name].filter(Boolean).join(",") || "-";
      sesLine(["B", sesT(), b.name, b.S.x.toFixed(1), b.S.y.toFixed(1), Math.round(b.S.h), (b.S.u * KN).toFixed(1), Math.round(norm180(windAt(b.S.x, b.S.y).twd - b.S.h)), b.leg, st].join(" "));
    }
  }
  function sesTick(dt, noDraw){
    if (!ses.on) return;
    const L = ses.L; ses.t += dt;
    // schermata, ricomincia, passo di lezione
    const mk = sesMode(), sk = mode === "lesson" ? (lessonIdx + 1) + "." + (stepIdx + 1) : null;
    if (mk !== L.mode){ L.mode = mk; sesEv("apre", sesModeName());
      if (mode === "race" && R && R.t >= 0 && R.boats[0].fin === null) sesEv("regata_in_corso", "lato " + R.boats[0].leg + " t=" + Math.round(R.t) + "s"); } // 0.21.2: registrazione accesa a regata partita: la partenza non c'è nel file
    else if (S !== L.S && mode !== "menu" && sk === L.step) sesEv("ricomincia", sesModeName());
    if (sk !== L.step){ L.step = sk; if (sk){ ses.stepName[sk] = $("lTitle").textContent; sesLine("L " + sesT() + " " + sk + " «" + ses.stepName[sk] + "»"); } }
    if (sk) ses.stepT[sk] = (ses.stepT[sk] || 0) + dt;
    if (S !== L.S){ L.S = S; SES_CNT.forEach(([k]) => L[k] = S[k]); L.toast = S.toast; L.fin = S.finished; L.cap = S.capsized; L.righting = S.righting; }
    if (stepDone && !L.done) sesEv("passo_completato", sk);
    L.done = stepDone;
    // eventi della barca
    const twa = norm180(local.twd - S.h);
    SES_CNT.forEach(([k, name]) => { if (S[k] > L[k]) for (let n = L[k]; n < S[k]; n++) sesEv(name, k === "markIdx" ? String(n + 1) : (twa > 0 ? "mure_a_dritta" : "mure_a_sinistra") + " " + (S.u * KN).toFixed(1) + "kn"); L[k] = S[k]; });
    if (S.righting > 0 && !(L.righting > 0)) sesEv("raddrizza");
    if (!S.capsized && L.cap) sesEv("raddrizzata");
    L.righting = S.righting; L.cap = S.capsized;
    if (S.finished && !L.fin) sesEv("arrivo", Math.round(S.time) + "s");
    L.fin = S.finished;
    const leg = mode === "race" && R && R.boats[0] ? R.boats[0].leg : null;
    if (leg !== null && L.leg !== null && leg > L.leg) sesEv(leg === 1 ? "partito" : "lato", String(leg));
    L.leg = leg;
    // 0.21.2: arrivo in regata = tempo netto (fin, penalità comprese), una volta sola per regata; a registrazione accesa dopo l'arrivo non si scrive
    const rf = mode === "race" && R && R.boats[0] ? R.boats[0].fin : null;
    if (R !== L.R){ L.R = R; L.rfin = rf !== null; }
    else if (rf !== null && !L.rfin){ L.rfin = true; sesEv("arrivo", Math.round(rf) + "s"); }
    // registro degli errori
    if (reg !== L.reg){ L.reg = reg; L.regV = Object.assign({}, reg); }
    for (const k in reg) if (k !== "ironsSec" && reg[k] > L.regV[k]){
      const d = reg[k] - L.regV[k];
      if (k === "contacts"){ const p = reg.contactsPen - L.regV.contactsPen; if (d > p) sesEv("contatto_senza_colpa", "+" + (d - p)); } // 0.21.1: «contacts» non è più un errore; la parte con colpa esce come errore contactsPen (reg.contacts viene prima di contactsPen)
      else sesEv("errore", k + " +" + d);
      L.regV[k] = reg[k];
    }
    // testi mostrati
    if (S.toast && S.toast !== L.toast) sesLine("T " + sesT() + " " + S.toast.text);
    L.toast = S.toast;
    const h = sesHint(); // un suggerimento entra nel file se resta almeno 0,3 s; i secondi contano anche quelli più brevi
    if (h !== L.cand){ L.cand = h; L.candT = 0; } else L.candT += dt;
    if (h !== L.hint && L.candT >= 0.3){ L.hint = h; if (h){ ses.msgN[h] = (ses.msgN[h] || 0) + 1; sesLine("H " + sesT() + " " + h); } }
    if (h) ses.msgT[h] = (ses.msgT[h] || 0) + dt;
    const rule = mode === "race" && !$("rRule").hidden ? $("rRule").textContent : "";
    if (rule !== L.rule){ L.rule = rule; if (rule) sesLine("P " + sesT() + " " + rule); }
    const err = $("errBox").hidden ? "" : $("errBox").textContent;
    if (err !== L.err){ L.err = err; if (err) sesLine("X " + sesT() + " " + err); }
    const dlg = sesDlg();
    for (const k in dlg) if (dlg[k] !== L.dlg[k]) sesEv("dialogo", k + (dlg[k] ? "_aperto" : "_chiuso"));
    L.dlg = dlg;
    const set = sesSet();
    if (set !== L.set){ L.set = set; sesLine("C " + sesT() + " " + set); }
    // tasti: solo quelli del gioco, e mai mentre si scrive in un campo di testo
    if (!sesTyping()){
      const kk = sesKeys();
      kk.forEach(k => { if (!L.keys.includes(k)) sesLine("K " + sesT() + " " + SES_KEY[k] + " giù"); });
      L.keys.forEach(k => { if (!kk.includes(k)) sesLine("K " + sesT() + " " + SES_KEY[k] + " su"); });
      L.keys = kk;
    }
    // tempo per andatura e stato, solo mentre la simulazione avanza
    const dSim = simTime - L.sim; L.sim = simTime;
    let riga = false;
    if (dSim > 0 && mode !== "menu"){
      const code = S.capsized ? "SC" : AND_CODE[andName(Math.abs(twa))];
      ses.andT[code] = (ses.andT[code] || 0) + dSim; ses.sim += dSim;
      if (ses.t >= ses.nextS){
        ses.nextS = ses.t + 1; riga = true;
        sesLine(["S", sesT(), S.x.toFixed(1), S.y.toFixed(1), Math.round(S.h), (S.u * KN).toFixed(1), Math.round(S.heel), Math.round(twa), (local.tws * KN).toFixed(1),
          Math.round(info.awa), (info.aws * KN).toFixed(1), Math.round(ctl.tiller * 100), Math.round(ctl.sheet * 100), code].join(" "));
      }
    }
    sesAltre(dSim, riga);
    // spia sullo schermo (sul mare, non nel pannello)
    if (!noDraw && mode !== "menu"){
      ses.flash = Math.max(0, ses.flash - dt);
      ctx.save(); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.font = font(600, 13); ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
      ctx.fillStyle = "rgba(255,120,110,.95)"; ctx.fillText("● REG" + (ses.flash > 0 ? " · M" + ses.marks.length : ""), 16, 46); ctx.restore();
    }
  }
  function sesToggle(on){
    if (on && !ses.start){ ses.start = new Date(); ses.set0 = sesSet(); }
    if (on) sesBase();
    // secondi veri di pausa (orologio del computer, non tempo di gioco): scritti alla riaccensione e sommati nel riassunto
    let det = "";
    if (on && ses.offAt){ const p = Math.round((Date.now() - ses.offAt) / 1000); ses.pause += p; det = " pausa " + p + "s"; ses.offAt = null; }
    if (!on && ses.on) ses.offAt = Date.now();
    ses.on = on; sesLine("E " + sesT() + " registrazione_" + (on ? "accesa" : "spenta") + det);
    $("sesBox").hidden = false;
  }
  function sesText(){
    const d = ses.start;
    const note = $("sesNote").value.replace(/\s+/g, " ").trim().slice(0, 2000);
    const list = (o, f) => Object.keys(o).map(f).join(" · ") || "nessuno";
    const and = ["AM", "BS", "BL", "TR", "LA", "GL", "PO", "SC"].filter(k => ses.andT[k]).map(k => k + " " + fmtClock(ses.andT[k])).join(" · ") || "nessuna";
    const msgs = Object.keys(ses.msgT).sort((a, b) => ses.msgT[b] - ses.msgT[a]).map(m => "#   «" + m + "» " + (ses.msgN[m] || 0) + "× · " + Math.round(ses.msgT[m]) + " s");
    return [
      "# SCUOLA DI VELA - registrazione di sessione, formato 2",
      "# gioco " + VERSIONE + " · inizio " + d.getFullYear() + "-" + p2(d.getMonth() + 1) + "-" + p2(d.getDate()) + " " + p2(d.getHours()) + ":" + p2(d.getMinutes()) +
        " · durata " + fmtClock(ses.t) + " (in simulazione " + fmtClock(ses.sim) + ")",
      "# impostazioni all'inizio: " + ses.set0,
      "# nota: " + (note || "(nessuna)"),
      "# pause della registrazione (spenta e riaccesa): " + (ses.pause ? ses.pause + " s in totale" : "nessuna"),
      "# RIASSUNTO (calcolato dal gioco)",
      "#  eventi: " + list(ses.cnt, k => k + " " + ses.cnt[k]),
      "#  tempo per andatura (in simulazione): " + and,
      "#  suggerimenti mostrati (volte nel file · secondi a schermo, anche i passaggi sotto 0,3 s):", ...(msgs.length ? msgs : ["#   nessuno"]),
      "#  passi di lezione (tempo, pause di lettura comprese): " + list(ses.stepT, k => k + " «" + ses.stepName[k] + "» " + fmtClock(ses.stepT[k])),
      "#  marcatori: " + (ses.marks.map(m => "M" + m.n + " a " + fmtClock(m.t)).join(" · ") || "nessuno"),
      "# LEGENDA (t = secondi dall'inizio della registrazione, tempo vero di gioco; il menu non conta)",
      "#  S t x y prua nodi sbandamento twa tws awa aws barra% scotta% andatura   stato, una riga al secondo mentre la barca naviga",
      "#    x verso est e y verso sud, in metri; prua in gradi da nord; twa e awa con segno (+ mure a dritta, − mure a sinistra);",
      "#    tws e aws in nodi; barra −100 a sinistra, +100 a dritta; scotta 0 cazzata, 100 lascata;",
      "#    andatura AM angolo morto, BS bolina stretta, BL bolina larga, TR traverso, LA lasco, GL gran lasco, PO poppa, SC scuffiata",
      "#  E t tipo dettagli   evento (apre, ricomincia, virata, strambata, strambata_vela_aperta, scuffia, raddrizza, raddrizzata, boa, arrivo,",
      "#                       partito, lato, passo_completato, errore, contatto_senza_colpa, regata_in_corso, dialogo, registrazione_accesa/spenta;",
      "#                       arrivo Ns: nelle prove i secondi di gioco, nelle regate il tempo netto con le penalità, una volta sola per regata;",
      "#                       regata_in_corso lato N t=Ns: registrazione accesa a regata già partita (la partenza non è nel file);",
      "#                       apre regata «titolo» (barca 1a|1b): 1b = barca completa, regole 10-13 con «(regola N)», semaforo possibile;",
      "#                       contatto_senza_colpa +N: contatto che non conta negli errori (gli altri compaiono come «errore contactsPen +N»);",
      "#                       alla riaccensione «pausa Ns» = secondi veri passati a registrazione spenta; t non li conta)",
      "#  B t nome x y prua nodi twa lato stato   un avversario, una riga al secondo insieme alla S (formato 2, dalla 1.0.52): lato 0 prima del via, 1 bolina, 2 poppa;",
      "#    stato: - | ocs partenza anticipata | scuf scuffiata | arr arrivata | dnf non arrivata | via sta partendo | cede:Nome a chi sta lasciando strada (separati da virgole)",
      "#  E avv_fermo/avv_riparte nome   sotto 0,5 nodi per 5 s di gioco dopo il via (con lato e posizione), poi sopra 1 nodo; avv_lato nome N; avv_arrivo nome Ns;",
      "#    avv_ocs, avv_scuffia, avv_penalita nome +15s o +1pt, avv_boa_lato_sbagliato nome; contatto_barche nome1 nome2 (anche con «Tu»), uno per contatto",
      "#  Q t testo   motivo di una penalità, la stessa voce dell'elenco a fine regata",
      "#  L t lezione.passo «titolo»   passo di lezione mostrato",
      "#  H t testo   suggerimento del pannello cambiato (rimasto almeno 0,3 s)",
      "#  T t testo   messaggio a comparsa sul mare",
      "#  P t testo   regola della regata nel pannello",
      "#  X t testo   errore interno del gioco",
      "#  K t tasto giù/su   tasti del gioco (frecce, spazio, W, S, Q vista)",
      "#  M t n x y   marcatore premuto col tasto M (n = numero; x y = posizione della barca)",
      "#  C t impostazioni   impostazioni o vento cambiati",
      ...ses.lines, ""].join("\n");
  }
  function sesDownload(){
    const d = ses.start || new Date();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([sesText()], { type: "text/plain;charset=utf-8" }));
    a.download = "sessione-" + d.getFullYear() + p2(d.getMonth() + 1) + p2(d.getDate()) + "-" + p2(d.getHours()) + p2(d.getMinutes()) + ".txt";
    a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    ses.dirty = false;
  }
  $("sesOn").onchange = e => sesToggle(e.target.checked);
  $("sesGet").onclick = () => { if (ses.start) sesDownload(); };
  addEventListener("keydown", e => { // marcatore: mai mentre si scrive in un campo di testo
    if (!ses.on || e.repeat || e.key.toLowerCase() !== "m" || sesTyping()) return;
    const n = ses.marks.length + 1; ses.marks.push({ n, t: ses.t }); ses.flash = 1.5;
    sesLine("M " + sesT() + " " + n + (S ? " " + S.x.toFixed(1) + " " + S.y.toFixed(1) : ""));
    $("sesMarks").hidden = false; $("sesMarks").title = $("sesMarks").textContent = "Marcatori: " + ses.marks.map(m => "M" + m.n + " a " + fmtClock(m.t)).join(", ") + ". Scrivi nella nota a quale ti riferisci.";
  });
  addEventListener("beforeunload", e => { if (ses.dirty){ e.preventDefault(); e.returnValue = ""; } }); // registrazione non scaricata

