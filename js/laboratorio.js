// Scuola di vela, laboratorio.js — Laboratorio della barca (1.0.4): cursori sui valori di BOAT, solo con #lab nell'indirizzo; con #lab il gioco non salva niente.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
// Proposta, limiti misurati e criteri in docs/archivio/PROPOSTA-LABORATORIO.md. Senza #lab questo file non fa niente (le funzioni esistono ma nessuno le chiama).
  // ======================================================================
  // PROFILI DEL LABORATORIO
  // ======================================================================
  // Un profilo: { id: "breve_senza_spazi", nome: "…", versione: "1.0.4", nota: "cosa si vuole provare",
  //   valori: { hullScale: { v: 0.8, fonte: "documento e riga, o «scelta di progetto»", stato: "misura" | "ipotesi" | "non verificato" } } }
  // Solo i valori diversi da BOAT. Un profilo senza fonte non entra. La versione è un campo, mai «const VERSIONE =» (collaudo_versione.py).
  const LAB_PROFILI = [ // 1.0.11: la barca di prima e le due modifiche spente una alla volta (docs/archivio/PROPOSTA-BOLINA.md)
    { id: "barca_1010", nome: "barca della 1.0.10", versione: "1.0.10", nota: "senza resistenza indotta e con la vela di prima, per confronto",
      valori: { TE: { v: 0, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" }, minBoom: { v: 14, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" },
        luffA0: { v: 27, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" }, sailCL2: { v: 0.12, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" } } },
    { id: "senza_indotta", nome: "senza resistenza indotta", versione: "1.0.11", nota: "solo la vela nuova",
      valori: { TE: { v: 0, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" } } },
    { id: "vela_1010", nome: "vela della 1.0.10", versione: "1.0.11", nota: "solo la resistenza indotta",
      valori: { minBoom: { v: 14, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" }, luffA0: { v: 27, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" },
        sailCL2: { v: 0.12, fonte: "js/motore.js della 1.0.10", stato: "ipotesi" } } }
  ];
  // FINE PROFILI

  // ======================================================================
  // LIMITI DEI CURSORI
  // ======================================================================
  // [min, max, passo, avvertenza]: scelte nostre di prudenza, misurate il 16 ottobre 2026 sul motore della 1.0.4 (docs/archivio/PROPOSTA-LABORATORIO.md §5); hullScale e appDA dalla 1.0.6 (docs/archivio/PROPOSTA-VELOCITA.md); minBoom, sailCL2 e TE dalla 1.0.11 (docs/archivio/PROPOSTA-BOLINA.md)
  const LAB_LIM = {
    mass: [90, 250, 5, "kg, barca e timoniere: cambia l'accelerazione, non la velocità di regime"],
    sailArea: [4, 10, 0.1, "m² di vela"],
    hullScale: [0.5, 2.5, 0.05, "moltiplica la resistenza dello scafo misurata in vasca (1 = la vasca; 2 = circa la barca fino alla 1.0.5)"],
    appDA: [0, 0.01, 0.0001, "m², attrito di deriva e timone (0,0049 dalla fonte): conta di più a velocità bassa"],
    rudderDragK: [0, 120, 5, "freno del timone girato"],
    turnLen: [0.5, 2, 0.05, "m: più è corta, più la barca gira in fretta; vale anche all'indietro"],
    maxRudder: [15, 45, 1, "gradi della pala a barra tutta; vale anche all'indietro e cambia il disegno della barra"],
    yawK: [1, 10, 0.5, "1/s, quanto in fretta la rotazione segue la barra"],
    ironsA: [25, 45, 1, "barca ferma nel vento: sotto questi gradi di vento apparente la prua poggia da sola (sopra luffA0+luffW anche con la vela che porta)"],
    ironsU: [0.1, 1, 0.05, "m/s: sotto questa velocità la prua poggia da sola"],
    ironsYaw: [0, 15, 0.5, "gradi al secondo con cui la prua poggia da sola"],
    backDrag: [1, 4, 0.1, "moltiplica la resistenza dello scafo all'indietro (1,5 dalla 1.0.13; 1 = come in avanti): più è alta, più lenta la retromarcia"],
    luffA0: [15, 33, 1, "gradi di vento apparente sotto cui la vela si sgonfia: cambia anche filetti e angolo morto"],
    luffW: [2, 15, 1, "ampiezza della transizione: cambia anche filetti e angolo morto"],
    minBoom: [5, 20, 1, "gradi del boma cazzato a ferro (9; era 14): la vela porta del tutto da minBoom + 20 di vento apparente; cambia anche suggerimento della scotta, avversari e disegno"],
    sailCL2: [0.02, 0.2, 0.01, "peso di CL² nella resistenza della vela (0,08; era 0,12): conta di bolina, quasi niente in poppa"],
    TE: [0, 1.5, 0.05, "m, profondità efficace della deriva per la resistenza indotta (0,80); 0 = senza: più è piccola, più la spinta laterale frena"]
  };
  const LAB_BASE = Object.assign({}, BOAT); // la barca del gioco: il profilo predefinito «come oggi» è lei, non è scritto da nessuna parte
  const LAB_OGGI = { id: "oggi", nome: "come oggi", versione: VERSIONE, valori: {} };
  const LAB_STATI = ["non verificato", "ipotesi", "misura"]; // dal più debole
  let labProf = LAB_OGGI, labMano = {}; // valori toccati a mano: escono sempre «prova a mano», «non verificato»

  // ======================================================================
  // CONTROLLI, CARICAMENTO, ESPORTAZIONE
  // ======================================================================
  function labErrore(p){ // "" se il profilo si può caricare, altrimenti perché no
    if (!p || typeof p.id !== "string" || !/^\w+$/.test(p.id)) return "manca l'id (lettere, cifre, _)";
    if (!p.valori || typeof p.valori !== "object") return p.id + ": mancano i valori";
    const v = Object.assign({}, LAB_BASE);
    for (const [k, x] of Object.entries(p.valori)){
      if (!LAB_LIM[k]) return p.id + ": «" + k + "» non è un valore del laboratorio";
      if (!x || typeof x.v !== "number" || !isFinite(x.v)) return p.id + ": «" + k + "» senza un numero";
      if (x.v < LAB_LIM[k][0] || x.v > LAB_LIM[k][1]) return p.id + ": «" + k + "» = " + x.v + " fuori dai limiti " + LAB_LIM[k][0] + "-" + LAB_LIM[k][1];
      if (!x.fonte || !LAB_STATI.includes(x.stato)) return p.id + ": «" + k + "» senza fonte o stato";
      v[k] = x.v;
    }
    if (v.luffA0 + v.luffW > 40) return p.id + ": luffA0 + luffW oltre 40° (i 40° dell'angolo morto delle lezioni)";
    return "";
  }
  const labStato = p => { const s = Object.values(p.valori).map(x => LAB_STATI.indexOf(x.stato)); return s.length ? LAB_STATI[Math.min(...s)] : "ipotesi (taratura del gioco)"; };
  function labCarica(p){ const e = labErrore(p); if (e) return e;
    labProf = p; labMano = {}; Object.assign(BOAT, LAB_BASE); for (const [k, x] of Object.entries(p.valori)) BOAT[k] = x.v;
    labMostra(); return ""; }
  function labImposta(k, v){ // un cursore: rifiuta la combinazione che rompe l'angolo morto delle lezioni
    const L = LAB_LIM[k]; v = Math.min(L[1], Math.max(L[0], v));
    if ((k === "luffA0" ? v : BOAT.luffA0) + (k === "luffW" ? v : BOAT.luffW) > 40) return "luffA0 + luffW oltre 40°";
    BOAT[k] = v; const pv = labProf.valori[k] ? labProf.valori[k].v : LAB_BASE[k];
    if (v === pv) delete labMano[k]; else labMano[k] = true;
    return "";
  }
  const labNome = () => labProf.nome + (Object.keys(labMano).length ? " + modificato" : "");
  const labDiversi = () => Object.keys(LAB_LIM).filter(k => BOAT[k] !== LAB_BASE[k]);
  const labSet = () => " profilo=" + labProf.id + (Object.keys(labMano).length ? "+modificato" : "") + labDiversi().map(k => " " + k + "=" + BOAT[k]).join(""); // in coda a sesSet() del registratore
  function labEsporta(){
    const d = new Date(), p2 = n => String(n).padStart(2, "0"), valori = {};
    for (const k of labDiversi()) valori[k] = labMano[k] || !labProf.valori[k] ? { v: BOAT[k], fonte: "prova a mano", stato: "non verificato" } : Object.assign({}, labProf.valori[k]);
    const txt = JSON.stringify({ id: labProf.id + (Object.keys(labMano).length ? "_mano" : ""), nome: labNome(), versione: VERSIONE,
      data: d.getFullYear() + "-" + p2(d.getMonth() + 1) + "-" + p2(d.getDate()) + " " + p2(d.getHours()) + ":" + p2(d.getMinutes()), nota: "", valori }, null, 1) + ",";
    if (ses.on) sesEv("laboratorio_esporta", txt.replace(/\s*\n\s*/g, " "));
    return txt;
  }

  // ======================================================================
  // FINESTRA
  // ======================================================================
  const labFmt = v => String(+v.toFixed(3)).replace(".", ",");
  function labMostra(){
    $("labBanner").textContent = "LABORATORIO · " + labNome() + " · niente salvataggi";
    $("labStato").textContent = "versione " + labProf.versione + " · stato: " + (Object.keys(labMano).length ? "non verificato (prova a mano)" : labStato(labProf));
    for (const k of Object.keys(LAB_LIM)){ const r = $("labR_" + k); r.value = BOAT[k]; $("labV_" + k).textContent = labFmt(BOAT[k]); r.parentNode.classList.toggle("diff", BOAT[k] !== LAB_BASE[k]); }
  }
  function labAvvia(){
    const st = document.createElement("style");
    st.textContent = `#labBanner{position:fixed;top:6px;left:50%;transform:translateX(-50%);z-index:50;background:var(--warn);color:#fff;font-weight:700;padding:3px 12px;border-radius:12px;pointer-events:none;font-size:.9rem}
#lab{position:fixed;top:34px;left:8px;z-index:40;width:400px;max-height:calc(100vh - 44px);overflow-y:auto;background:var(--panel);color:var(--ink);border:2px solid var(--warn);border-radius:8px;padding:6px 10px;font-size:.88rem}
#lab h3{margin:0 0 4px;font-size:1rem} #lab .r{display:grid;grid-template-columns:7rem 1fr 3.4rem;gap:6px;align-items:center} #lab .r.diff b{color:var(--warn)}
#lab input[type=range]{width:100%} #lab textarea{width:100%;height:9rem;font:.8rem monospace} #lab .err{color:var(--warn)} #lab .row{display:flex;gap:6px;margin:4px 0;flex-wrap:wrap}`;
    document.head.appendChild(st);
    const ban = document.createElement("div"); ban.id = "labBanner"; document.body.appendChild(ban);
    const w = document.createElement("div"); w.id = "lab";
    w.innerHTML = `<h3>Laboratorio della barca <small>(tasto L)</small></h3>
<div class="row"><select id="labProf"></select><span id="labStato"></span></div>
<p style="margin:2px 0">I valori cambiano subito la barca, e in regata anche gli avversari. Niente si salva: ricaricando la pagina si torna al gioco.</p>
${Object.entries(LAB_LIM).map(([k, L]) => `<label class="r" title="${L[3]}"><b>${k}</b><input type="range" id="labR_${k}" min="${L[0]}" max="${L[1]}" step="${L[2]}"><span id="labV_${k}"></span></label>`).join("")}
<p class="err" id="labErr"></p>
<div class="row"><button id="labReset">Valori del profilo</button><button id="labExp">Esporta</button></div>
<textarea id="labTxt" hidden readonly></textarea>`;
    document.body.appendChild(w);
    const tutti = [LAB_OGGI, ...LAB_PROFILI], sel = $("labProf");
    sel.innerHTML = tutti.map((p, i) => `<option value="${i}">${p.nome}${labErrore(p) && p !== LAB_OGGI ? " (non si carica)" : ""}</option>`).join("");
    sel.onchange = () => { const e = labCarica(tutti[+sel.value]); $("labErr").textContent = e; if (e) sel.value = tutti.indexOf(labProf); };
    for (const k of Object.keys(LAB_LIM)) $("labR_" + k).oninput = e => { $("labErr").textContent = labImposta(k, +e.target.value); labMostra(); };
    $("labReset").onclick = () => { labCarica(labProf); $("labErr").textContent = ""; };
    $("labExp").onclick = () => { const t = $("labTxt"); t.value = labEsporta(); t.hidden = false; t.focus(); t.select(); };
    addEventListener("keydown", e => { if ((e.key === "l" || e.key === "L") && !sesTyping()){ w.hidden = !w.hidden; if (w.hidden && w.contains(document.activeElement)) document.activeElement.blur(); } });
    labMostra();
  }
  if (LAB) labAvvia();
