# Impronta del gioco (1.0.1): serve alle pulizie del codice, che non devono cambiare niente di quello che il gioco fa.
# Ogni gruppo di scene (una lezione, una prova, una regata, il menu) è in una pagina nuova. Con Math.random a seme fisso (il seme si fissa nello stesso comando che apre la scena) guida, a passi fissi di 1/60 s:
#  - ogni passo di ogni lezione per 3 s, con una barra che va avanti e indietro (non serve completarli: conta lo stato);
#  - le 5 prove con il pilota di collaudo_fasce.py, fino all'arrivo o a 900 s;
#  - le 2 regate con principianti ed esperti, giocatore guidato da __sv.pilota, fino a 400 s;
#  - dal congelamento della barca dell'1b (docs/PROPOSTA-CONGELAMENTO-1B.md): la «Regata nei salti di vento» con principianti ed esperti e la
#    prima regata del torneo, come sopra; il gioco libero con la barca dell'1b guidato coi tasti veri (frecce, Maiusc, Z, una scuffia e A);
#  - il menu del gioco libero e della carriera (in una pagina nuova), i meriti, un'estrazione dell'esame;
#  - l'immagine del mare (canvas) in 21 momenti, con il ciclo del browser fermo (altrimenti increspature e zoom seguono l'orologio).
# Da ogni scena legge stato delle barche, registro, testi del pannello e dei riquadri, e ne fa un'impronta.
# Uso: python collaudo_impronta.py riferimento          salva tests/output/impronta/riferimento.json (sul codice da conservare)
#      python collaudo_impronta.py                      salva dopo.json e lo confronta col riferimento: uguali al bit, o FALLITO
#      python collaudo_impronta.py NOME --pagina FILE   impronta di un'altra pagina (per la contro-prova: una costante cambiata apposta)
# La costante VERSIONE non conta (si carica una copia con un valore fisso). Non c'è una soglia: le due impronte devono essere identiche. Esce con 1 se diverse, 2 se manca il riferimento o se ha misurato poco.
import asyncio, hashlib, json, pathlib, re, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "output" / "impronta"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();
window.requestAnimationFrame = () => 0;  // niente ciclo in tempo reale: si disegna solo quando lo chiede il collaudo, così l'immagine non dipende dall'orologio"""
COMUNE = """
window.__imp = {
  barca: S => S && ["x","y","h","u","vl","r","heel","heelRate","hike","boom","dispBoom","capsized","tacks","gybesV","gybesC","capsizes","markIdx","time","finished"].map(k => S[k]),
  testo: id => { const e = document.getElementById(id); return e ? [e.hidden, e.innerHTML] : null; },
  tela: () => { const d = document.getElementById("c").toDataURL(); let a = 2166136261, b = 5381;   // due somme di controllo dell'immagine intera
    for (let i = 0; i < d.length; i++){ const c = d.charCodeAt(i); a = Math.imul(a ^ c, 16777619); b = (Math.imul(b, 33) + c) | 0; }
    return d.length + ":" + (a >>> 0).toString(16) + ":" + (b >>> 0).toString(16); },
};"""
LEZIONE = """([li, k, seme]) => {
  const sv = __sv, I = __imp; sv.fast(0);
  if (k === 0) sv.openItem(["l", li]);
  __seed(seme); sv.showStep(k);
  const tl = [0.6, -0.6, 0, 1, -1, 0.3];
  for (let n = 0; n < 180; n++){ if (n % 30 === 0) sv.ctl.tiller = tl[n / 30]; sv.run(1 / 60, 1); }
  sv.panel();
  const out = { S: I.barca(sv.S), done: sv.stepDone, reg: Object.assign({}, sv.reg), ctl: [sv.ctl.sheet, sv.ctl.tiller], twd: sv.twd,
    testi: ["hint","lStep","lTitle","lText","lFeedback","lErr","lNext","lQuiz","lBack","lRetry","instr","sem","direct"].map(I.testo) };
  if (k === 1 || k === 4) { sv.draw(1 / 60); out.tela = I.tela(); }
  return out;
}"""
PROVA = """([idx, seme]) => {
  const sv = __sv, I = __imp, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  sv.fast(0); sv.openItem(["m", idx]); __seed(seme); sv.startMission(idx);
  const GIUSTO = [60, 0, -60], plan = [[], [], [], [[0, GIUSTO]], [[0, GIUSTO], [1, GIUSTO]]][idx], pts = [];
  for (const [k, angs] of plan) { const m = sv.marks[k];
    for (const a of angs) { const b = (m.out + a) * D; pts.push({ x: m.x + Math.sin(b) * 13, y: m.y - Math.cos(b) * 13 }); } }
  const last = sv.marks[sv.marks.length - 1]; pts.push({ x: last.x, y: last.y });
  let i = 0, side = 1, n = 0, tieni = false, tela = null;
  while (!sv.S.finished && n < 60 * 900) {
    const S = sv.S;
    if (n % 6 === 0 && i < pts.length) {
      const p = pts[i]; if (Math.hypot(p.x - S.x, p.y - S.y) < 7 && i < pts.length - 1) i++;   // 1.0.6: arrivato all ultimo punto continua a puntarlo (prima smetteva di guidare e la barca, più veloce, girava in tondo)
      const q = pts[Math.min(i, pts.length - 1)];
      const brg = Math.atan2(q.x - S.x, -(q.y - S.y)) / D, rel = n180(brg - sv.twd);
      let want = brg;
      if (Math.abs(rel) < 52) { if (S.u > 1.7) tieni = false; if (Math.abs(rel) > 12 && !tieni) side = Math.sign(rel); want = sv.twd + side * 52; }
      const cur = n180(S.h - sv.twd);
      if (Math.abs(rel) > 168 && Math.abs(cur) > 90) want = sv.twd + Math.sign(cur || 1) * 168;
      if (Math.abs(cur) < 48 && S.u < 0.8) { want = sv.twd + Math.sign(cur || 1) * 95; side = Math.sign(cur || 1); tieni = true; }   // 1.0.6: uscito dall'angolo morto tiene quella mura finché non ha 3,3 nodi (1,7 m/s), la velocità con cui la lezione 5 insegna a prepararsi a virare; prima tornava subito sull'altra e si ripiantava
      sv.ctl.tiller = Math.max(-1, Math.min(1, n180(S.h - want) / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
      const gybe = (Math.abs(cur) > 150 && Math.sign(n180(want - sv.twd)) !== Math.sign(cur)) || Math.abs(cur) > 174;
      sv.ctl.sheet = gybe ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet();
      if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "a" }));
    }
    sv.run(1 / 60, 1); n++;
    if (n === 60 * 40) { sv.panel(); sv.draw(1 / 60); tela = I.tela(); }
  }
  sv.panel();
  return { S: I.barca(sv.S), passi: n, reg: Object.assign({}, sv.reg), tela, toast: sv.toast,
    testi: ["hint","stClock","stErr","done","doneText","mTitle","mNext","instr","where","bTitle","bText","bNote"].map(I.testo) };
}"""
REGATA = """([race, liv, seme]) => {
  const sv = __sv, I = __imp; sv.fast(0); sv.openItem(["r", race]);
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0]; let n = 0, tela = null;
  while (R.t < 400 && !R.boats.every(b => b.fin !== null)) {
    sv.pilota(1 / 60); sv.run(1 / 60, 1); n++;
    if (n === 60 * 200) { sv.panel(); sv.draw(1 / 60); tela = I.tela(); }
  }
  sv.panel();
  return { barche: R.boats.map(b => [b.name, b.fin, b.pen, b.leg, b.ocs, b.char, I.barca(b.S), b.ctl.sheet, b.ctl.tiller]), passi: n, rank: sv.rank(),
    reg: Object.assign({}, sv.reg), tela, brief: R.brief, testi: ["standings","rRule","stErr","rDone","rDoneText","hint","instr","bTitle","bText","bNote"].map(I.testo) };
}"""
# 1b: la prima regata del torneo, come REGATA (il torneo si apre dal menu, come in misura_scarroccio.py)
TORNEO = """([seme]) => {
  const sv = __sv, I = __imp; sv.fast(0); __seed(seme); sv.store = "scuolaVelaSim.v1"; sv.torApri(); document.getElementById("torGo").click();
  const R = sv.R; let n = 0, tela = null;
  while (R.t < 400 && !R.boats.every(b => b.fin !== null)) {
    sv.pilota(1 / 60); sv.run(1 / 60, 1); n++;
    if (n === 60 * 200) { sv.panel(); sv.draw(1 / 60); tela = I.tela(); }
  }
  sv.panel();
  return { barche: R.boats.map(b => [b.name, b.fin, b.pp, b.leg, b.ocs, b.char, I.barca(b.S), b.ctl.sheet, b.ctl.tiller]), passi: n, rank: sv.rank(),
    reg: Object.assign({}, sv.reg), tela, testi: ["standings","rRule","stErr","hint","instr"].map(I.testo) };
}"""
# 1b: gioco libero con la barca dell'1b, 10 nodi, tasti veri: ← e → (sola freccia e con Maiusc), Z tenuto, una scuffia e A; stato ogni 5 s
LIBERA1B = """([seme]) => {
  const sv = __sv, I = __imp; sv.fast(0); __seed(seme); sv.openItem("free");
  for (const [id, v] of [["wSpd", "10"], ["gustSel", "1"], ["wDir", "0"], ["boatLv", "2"]]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event("change")); }
  sv.openItem("free"); const S = sv.S;
  const giu = k => dispatchEvent(new KeyboardEvent("keydown", { key: k })), su = k => dispatchEvent(new KeyboardEvent("keyup", { key: k }));
  const piano = [[5, giu, "ArrowLeft"], [6.5, su, "ArrowLeft"], [15, giu, "ArrowRight"], [17, su, "ArrowRight"], [30, giu, "Shift"], [30, giu, "ArrowLeft"], [31.5, su, "ArrowLeft"],
    [31.5, su, "Shift"], [45, giu, "z"], [51, su, "z"], [60, giu, "ArrowDown"], [63, su, "ArrowDown"], [80, giu, "ArrowUp"], [82, su, "ArrowUp"]];
  const out = { stati: [], lv: S.lv }; let n = 0, tela = null;
  for (; n < 60 * 120; n++){
    const t = n / 60; for (const [tt, f, k] of piano) if (Math.abs(t - tt) < 1e-6) f(k);
    if (n === 60 * 90) Object.assign(S, { capsized: true, capSide: 1, u: 0, vl: 0, r: 0, heel: 90, heelRate: 0, righting: 0 }); // scuffia, poi A
    if (n === 60 * 91){ out.scuffia = [!!S.capsized]; giu("a"); }
    sv.run(1 / 60, 1);
    if (n % 300 === 0) out.stati.push([I.barca(S), sv.ctl.sheet, sv.ctl.tiller, !!S.stall, !!S.pushing]);
    if (n === 60 * 46) { sv.panel(); sv.draw(1 / 60); tela = I.tela(); }
  }
  sv.panel(); out.scuffia.push(!!S.capsized); out.S = I.barca(S); out.tela = tela; out.reg = Object.assign({}, sv.reg); out.testi = ["hint","stErr","instr"].map(I.testo);
  return out;
}"""
FINE = """() => {
  const sv = __sv, I = __imp, out = {};
  document.getElementById("toMenu").click(); out.menuLibero = I.testo("menu");
  const salv = JSON.parse(localStorage.getItem("scuolaVelaSim.v1") || "{}");
  out.salvataggio = salv; out.fantasmi = Object.keys(sv.ghosts()).sort().map(k => [k, sv.ghosts()[k].length]);
  out.meriti = sv.meriti(Object.assign({ done: {}, best: {}, clean: {} }, salv));
  __seed(7); out.esame = sv.estraiEsame();
  document.querySelector('#modoSel [data-v="carriera"]').click(); out.menuCarriera = I.testo("menu");
  document.querySelector('#modoSel [data-v="libero"]').click();
  // finestre: glossario (con una ricerca), ripasso (una risposta), esame, impostazioni dal gioco
  const st = id => document.getElementById(id).open;
  document.getElementById("menuGloss").click(); const gs = document.getElementById("glSearch"); gs.value = "vento"; gs.dispatchEvent(new Event("input"));
  out.glossario = [st("gloss"), I.testo("glList")]; document.getElementById("glClose").click(); out.glossarioChiuso = st("gloss");
  __seed(8); document.querySelector('[data-q="2"]').click(); document.querySelector("#qzBody .opt").click();
  out.ripasso = [st("quiz"), I.testo("qzBody")]; document.getElementById("quiz").close();
  __seed(9); document.getElementById("goEsame").click(); out.esameAperto = [st("quiz"), I.testo("qzBody")]; document.getElementById("quiz").close();
  sv.openItem("free"); document.getElementById("openSet").click(); out.impostazioni = st("setDlg"); document.getElementById("setClose").click();
  out.impostazioniChiuse = st("setDlg"); out.menuDopo = I.testo("menu");
  return out;
}"""

def h(x): return hashlib.sha1(json.dumps(x, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]

async def impronta(pagina, nome):
    # la costante VERSIONE si scrive nel menu e sul mare: cambia a ogni versione per scelta, quindi si carica una copia con un valore fisso
    import sorgente   # dalla 1.0.3 la pagina è index.html più js/: si copia tutta, con VERSIONE fissa
    m = re.search(r'const VERSIONE = "[^"]*"', sorgente.testo(pagina))
    if not m: raise RuntimeError("costante VERSIONE non trovata nella pagina")
    url = sorgente.copia(OUT / f"pagina-{nome}", [(m.group(0), 'const VERSIONE = "impronta"')], pagina).as_uri() + "#collaudo"
    imp, errs = {}, []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        async def nuova():   # una pagina nuova (e un localStorage vuoto) per ogni gruppo di scene: nessuno stato passa da una scena all'altra
            ctx = await b.new_context(viewport={"width": 1360, "height": 650})
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.add_init_script(SEME); await pg.goto(url); await pg.wait_for_timeout(300)
            if await pg.evaluate("typeof window.__sv") != "object":   # la pagina non è partita (per esempio un file caricato nell'ordine sbagliato)
                raise RuntimeError(f"la pagina non si avvia: errori {errs[:3]}")
            await pg.evaluate("document.fonts.ready.then(() => 0)"); await pg.evaluate(COMUNE)
            return pg
        pg = await nuova()
        passi = await pg.evaluate("(() => { const n = []; for (let li = 0; li < 6; li++){ __sv.openItem(['l', li]); let k = 0; try { while (k < 40){ __sv.showStep(k); k++; } } catch(e){} n.push(k); } return n; })()")
        await pg.close()
        # ponytail: il numero di passi si ricava provando showStep finché non dà errore; se showStep cambiasse comportamento, lo stampa qui sotto
        for li, n in enumerate(passi):
            pg = await nuova()
            for k in range(n):
                imp[f"lezione {li+1}.{k+1}"] = await pg.evaluate(LEZIONE, [li, k, 1000 + li * 50 + k])
            await pg.close()
        for i in range(5):
            pg = await nuova(); imp[f"prova {i+1}"] = await pg.evaluate(PROVA, [i, 11 + i]); await pg.close()
        for r in range(2):
            for liv in ("principianti", "esperti"):
                pg = await nuova(); imp[f"regata {r+1} {liv}"] = await pg.evaluate(REGATA, [r, liv, 21 + r]); await pg.close()
        for liv in ("principianti", "esperti"):   # 1b (congelamento)
            pg = await nuova(); imp[f"regata 3 {liv}"] = await pg.evaluate(REGATA, [2, liv, 23]); await pg.close()
        pg = await nuova(); imp["torneo regata 1"] = await pg.evaluate(TORNEO, [24]); await pg.close()
        pg = await nuova(); imp["libera 1b"] = await pg.evaluate(LIBERA1B, [25]); await pg.close()
        pg = await nuova(); imp["menu, meriti, esame"] = await pg.evaluate(FINE)   # il salvataggio è quello di una pagina senza giocate: il menu e i meriti partono da zero
        imp["errori della pagina"] = errs
        await b.close()
    return imp, passi

def misura(imp, passi):
    v = [x for k, x in imp.items() if k.startswith(("lezione", "prova"))]
    reg = [x for k, x in imp.items() if k.startswith(("regata", "torneo"))]
    vel = sum(1 for x in v if x["S"] and abs(x["S"][3]) > 0.01) + sum(1 for x in reg for b in x["barche"] if abs(b[6][3]) > 0.01)
    tele = sum(1 for x in v + reg if x.get("tela"))
    finite = sum(1 for k, x in imp.items() if k.startswith("prova") and x["S"][18])
    print(f"misurato: {sum(passi)} passi di lezione {passi}, {finite} prove finite su 5, {sum(len(x['barche']) for x in reg)} barche in {len(reg)} regate, "
          f"{vel} barche con velocità diversa da zero, {tele} immagini del mare, errori della pagina {len(imp['errori della pagina'])}", flush=True)
    b1 = [x for k, x in imp.items() if k.startswith(("regata 3", "torneo"))]   # 1b: deve aver misurato davvero (docs/PROPOSTA-CONGELAMENTO-1B.md, criterio 1)
    lib = imp.get("libera 1b") or {"stati": [], "lv": None}
    arrivi = sum(1 for x in b1 for b in x["barche"] if b[1] is not None); virate = sum(b[6][12] or 0 for x in b1 for b in x["barche"])   # indici di __imp.barca: 12 tacks, 15 capsizes
    stallo = sum(1 for st in lib["stati"] if st[3]); boma = sum(1 for st in lib["stati"] if st[4]); scuffie = 1 if lib.get("scuffia") == [True, False] else 0   # scuffiata a 90 s e raddrizzata con A
    print(f"barca dell'1b: {len(b1)} regate, {arrivi} arrivi, {virate} virate; gioco libero: barca {lib['lv']}, {len(lib['stati'])} stati, "
          f"col boma spinto {boma}, con la pala in stallo {stallo}, scuffia e raddrizzata con A {scuffie}", flush=True)
    return sum(passi) >= 40 and vel >= 30 and tele >= 6 and len(reg) == 7 and lib["lv"] == 2 and virate > 0 and boma > 0 and scuffie > 0

async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nome = args[0] if args else "dopo"
    pagina = sys.argv[sys.argv.index("--pagina") + 1] if "--pagina" in sys.argv else str(ROOT / "index.html")
    if "--pagina" in sys.argv: args = [a for a in args if a != pagina]; nome = args[0] if args else "dopo"
    try: imp, passi = await impronta(pagina, nome)
    except RuntimeError as e: print(f"ESITO: NON VALIDO ({e})"); sys.exit(2)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{nome}.json").write_text(json.dumps(imp, ensure_ascii=False, sort_keys=True, indent=0))
    print(f"impronta {nome}: {h(imp)}  ({pagina}, salvata in tests/output/impronta/{nome}.json)", flush=True)
    ok_misura = misura(imp, passi)
    if not ok_misura: print("ESITO: NON VALIDO (ha misurato troppo poco)"); sys.exit(2)
    if nome == "riferimento": print("ESITO: riferimento salvato"); return
    rif = OUT / "riferimento.json"
    if not rif.exists(): print("ESITO: NON VALIDO (manca riferimento.json: lancia prima 'collaudo_impronta.py riferimento' sul codice da conservare)"); sys.exit(2)
    r = json.loads(rif.read_text())
    imp = json.loads(json.dumps(imp, ensure_ascii=False, sort_keys=True))
    diverse = [k for k in sorted(set(r) | set(imp)) if h(r.get(k)) != h(imp.get(k))]
    print(f"riferimento: {h(r)}  scene confrontate: {len(set(r) | set(imp))}, diverse: {len(diverse)}", flush=True)
    for k in diverse[:20]: print(f"  DIVERSA: {k}", flush=True)
    print("ESITO: OK (identica al riferimento)" if not diverse else "ESITO: FALLITO"); sys.exit(1 if diverse else 0)

if __name__ == "__main__": asyncio.run(main())   # 1.0.4: importabile (collaudo_laboratorio.py ne usa i piloti)
