# Collaudo delle bandiere della partenza (1.0.65, docs/PROPOSTA-SEGNALI-PARTENZA.md, fetta 3: classe, P, X, blu). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_segnali.py [cartella di una copia di riferimento (1.0.64), per il confronto al bit e al pixel delle altre regate]
# Parti: G1 bandiere giuste a ogni decimo di secondo (1, 3 e 5 minuti, tabella scritta qui, indipendente dal gioco); G2 la X con e senza richiamo (la posizione delle barche, non i campi del gioco);
#        G3 i messaggi, una volta e al tempo giusto; G4 le altre regate identiche al pixel e al bit, nella regata dei giri le bandiere si vedono; G5 registratore e pagina senza #collaudo.
import asyncio, pathlib, sys, os
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "output"; OUT.mkdir(exist_ok=True)
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata dei giri (indice 3) con la preparazione scelta, senza avversari, ferma: ogni 0,1 s le bandiere lette dal gioco (bandiereR)
BANDIERE = """async ([cd, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const sel = document.getElementById('cdSel'); sel.value = String(cd); sel.dispatchEvent(new Event('change')); __seed(seme);
  const R = sv.R; const out = [], toasts = []; let k = 0, ult = null; const x0 = sv.S.x, y0 = sv.S.y; // la barca resta dov'è: alla deriva oltre la linea sarebbe un richiamo vero
  if (R.cd !== cd) return { errore: 'cd ' + R.cd };
  while (R.t < 5){ sv.S.x = x0; sv.S.y = y0; sv.S.u = 0; sv.ctl.tiller = 0; sv.run(dt, 1); const tx = sv.toast; if (tx && tx !== ult){ toasts.push([R.t, tx]); } ult = tx;
    if (k++ % 6 === 0){ const f = bandiereR(); out.push([R.t, f.classe, f.P, f.X, f.blu]); } }
  return { cd: R.cd, out, toasts };
}"""
# X: tre casi. 'torna' = un avversario oltre la linea allo sparo, poi la guida lo riporta dietro; 'resta' = lo teniamo oltre la linea (si rimette a ogni passo) fino a 260 s; 'nessuno' = nessuno oltre la linea.
RICHIAMO = """async ([caso, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const sel = document.getElementById('cdSel'); sel.value = '60'; sel.dispatchEvent(new Event('change')); __seed(seme);
  const R = sv.R, a = R.boats[1]; let k = 0; const out = [];
  const wy = b => toWF(b.S.x, b.S.y)[1];
  while (R.t < -0.5){ sv.pilota(dt); sv.run(dt, 1); }
  if (caso !== 'nessuno'){ const [wx] = toWF(a.S.x, a.S.y); const [px, py] = fromWF(wx, -6); a.S.x = px; a.S.y = py; }
  let fermo = null; if (caso === 'resta') fermo = [a.S.x, a.S.y];
  let recall = null, prev = null; const tornati = new Set();
  while (R.t < 262){ const prima = R.boats.map(b => wy(b)); sv.pilota(dt); if (fermo){ a.S.x = fermo[0]; a.S.y = fermo[1]; a.S.u = 0; } sv.run(dt, 1);
    if (recall === null && R.t >= 0) recall = R.boats.filter((b, i) => prima[i] <= 0).map(b => b.name);   // le posizioni che il gioco ha visto allo sparo
    if (recall){ for (const n of recall){ const b = R.boats.find(x => x.name === n); if (wy(b) > 0) tornati.add(n); } }
    if (k++ % 6 === 0 && R.t >= 0 && recall){ const f = bandiereR(); out.push([R.t, f.X, recall.some(n => { const b = R.boats.find(x => x.name === n); return b.fin === null && !b.dnf && !tornati.has(n); })]); } }
  return { recall, out };
}"""
# altre regate: arrivi, penalità, posizioni (bit) e la schermata a -30 s (pixel)
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 3]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
SCHERMATA = """async ([idx, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", idx]);
  const R = sv.R; if (idx === 3){ const [px, py] = [R.cb.x, R.cb.y]; }
  while (R.t < -30){ sv.ctl.tiller = 0; sv.run(dt, 1); }
  sv.S.x = R.cb.x + 7; sv.S.y = R.cb.y + 9; sv.S.u = 0; sv.draw(0.016);
  return document.querySelector('canvas').toDataURL();
}"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
def atteso(t, cd):  # tabella delle bandiere senza richiamo: (classe, P, X, blu); nessuna dipendenza dal codice del gioco
    classe = -cd <= t < 0; P = cd >= 180 and -(cd - 60) <= t < -60
    return (classe, P, False, t >= 0)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def main():
    rif = sys.argv[1] if len(sys.argv) > 1 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        # ---- G1 e G3 ----
        controlli = 0; errori = []; tostiOK = True; dettaglio = []
        for cd in (60, 180, 300):
            for seme in (1, 2, 3):
                r = await pg.evaluate(BANDIERE, [cd, seme * 10])
                if "errore" in r: errori.append((cd, r["errore"])); continue
                for t, c, P, X, bl in r["out"]:
                    controlli += 4
                    # a cavallo di un cambio (entro un milionesimo di secondo) vale l'uno o l'altro lato
                    if (c, P, X, bl) != atteso(t, cd) and (c, P, X, bl) != atteso(t - 1e-6, cd) and (c, P, X, bl) != atteso(t + 1e-6, cd): errori.append((cd, round(t, 3), (c, P, X, bl)))
                # messaggi: una volta, al tempo giusto
                att = ([(-300, "Avviso: alzata la bandiera di classe"), (-240, "Preparatorio: alzata la bandiera P"), (-60, "Un minuto: ammainata la P")] if cd == 300 else
                       [(-180, "Avviso: alzata la bandiera di classe"), (-120, "Preparatorio: alzata la bandiera P"), (-60, "Un minuto: ammainata la P")] if cd == 180 else [(-60, "Un minuto: resta la bandiera di classe")])
                for t0, testo in att:
                    tt = [t for t, x in r["toasts"] if x.startswith(testo)]
                    if len(tt) != 1 or abs(tt[0] - t0) > 0.1: tostiOK = False; dettaglio.append((cd, testo, tt))
                altri = [x for t, x in r["toasts"] if x.startswith(("Avviso", "Preparatorio", "Un minuto"))]
                if len(altri) != len(att): tostiOK = False; dettaglio.append((cd, "messaggi in più o in meno", altri))
        chk("G1 bandiere giuste a ogni decimo di secondo con preparazione di 1, 3 e 5 minuti (3 regate ciascuna): %d controlli, %d errori" % (controlli, len(errori)), controlli >= 5000 and not errori, str(errori[:3]))
        chk("G3 messaggi di avviso, preparatorio e un minuto: ciascuno una volta, al tempo giusto, per 1, 3 e 5 minuti, e nessun altro di questo tipo", tostiOK, str(dettaglio[:3]))
        # ---- G2 ----
        casi = {"torna": [], "resta": [], "nessuno": []}
        for k in range(6):
            for caso in casi: casi[caso].append(await pg.evaluate(RICHIAMO, [caso, 40 + k]))
        errX = []; n_con = n_senza = 0
        for caso, rr in casi.items():
            for i, r in enumerate(rr):
                con = len(r["recall"]) > 0
                if con: n_con += 1
                else: n_senza += 1
                for t, X, atteso_X in r["out"]:
                    if t < 240 - 0.2 and X != atteso_X: errX.append((caso, i, round(t, 2), X, atteso_X))
                    if t > 240 + 0.2 and X: errX.append((caso, i, round(t, 2), "X oltre 240 s"))
                    if not con and X: errX.append((caso, i, round(t, 2), "X senza richiamo"))
        resta = casi["resta"]
        chk("G2 la X sale con un richiamo e scende quando l'ultima barca è tornata (guardando le posizioni, non i campi del gioco); mai senza richiamo (%d regate con richiamo, %d senza; errori %d)" % (n_con, n_senza, len(errX)), n_con >= 5 and n_senza >= 5 and not errX, str(errX[:3]))
        chk("G2b una barca tenuta oltre la linea: la X resta su fino a 240 s e poi si abbassa (%d regate)" % len(resta), len(resta) >= 5 and all(any(X for t, X, a in r["out"] if 200 < t < 239) and not any(X for t, X, a in r["out"] if t > 241) for r in resta if r["recall"]))
        chk("G2c il metro ha misurato davvero: nelle regate con richiamo la X compare almeno una volta", all(any(X for t, X, a in r["out"]) for r in casi["torna"] + casi["resta"] if r["recall"]) and any(r["recall"] for r in casi["torna"]), "richiami: torna %d su 6, resta %d su 6" % (sum(1 for r in casi["torna"] if r["recall"]), sum(1 for r in resta if r["recall"])))
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        # ---- G4/G5: registratore ----
        reg = await pg.evaluate("""async () => { const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(5); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]); const sel = document.getElementById('cdSel'); sel.value = '180'; sel.dispatchEvent(new Event('change')); __seed(5);
          const R = sv.R; while (R.t < 3){ sv.S.u = 0; sv.ctl.tiller = 0; sv.run(dt, 1); } return { testo: regPezzi.length ? regPezzi.map(p => p.testo).join("\\n") : "", live: ses.lines.join("\\n") }; }""")
        t = reg["live"]  # la registrazione ancora aperta di questa regata (quelle chiuse sono delle prove di prima)
        chk("G5a registratore (preparazione di 3 minuti): eventi «bandiere» classe, classe+P, classe (a un minuto) e blu, in quest'ordine", [x.split("bandiere ")[1].split()[0] for x in t.split("\n") if "E " in x and "bandiere " in x and "# " not in x][:4] == ["classe", "classe+P", "classe", "blu"], str([x for x in t.split("\n") if "bandiere " in x and "# " not in x][:5]))
        await ctx.close()
        # ---- G4: le altre regate ----
        async def schermate(base):  # una pagina nuova per ogni schermata: dopo molte regate i riflessi dell'acqua dipendono dal tempo reale e due pagine non coincidono al pixel
            o = {}
            for i in (0, 2, 3):
                c, g, e = await pagina(b, base); o[i] = await g.evaluate(SCHERMATA, [i, 9]); await c.close()
            return o
        ctx, pg, errs = await pagina(b, ROOT)
        nuovo = await pg.evaluate(ALTRE, [20, 100]); await ctx.close(); sch_n = await schermate(ROOT)
        if rif:
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); vecchio = await pg.evaluate(ALTRE, [20, 100]); await ctx.close(); sch_v = await schermate(pathlib.Path(rif))
            chk("G4a regate dell'1a e dell'1b: arrivi, penalità e posizioni finali identici al bit alla 1.0.64 su 20 regate", nuovo == vecchio and len(nuovo) == 20)
            chk("G4b la schermata a -30 s della regata 1a (indice 0) e della regata 1b (indice 2) è identica al pixel alla 1.0.64", sch_n[0] == sch_v[0] and sch_n[2] == sch_v[2] and len(sch_n[0]) > 1000)
            chk("G4c nella regata dei giri la schermata a -30 s è diversa (le bandiere si vedono)", sch_n[3] != sch_v[3])
        else: print("     G4 saltato: manca la cartella di riferimento")
        # ---- G5: pagina come la carica un giocatore ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => ({ segnali: R && R.segnali, mode: mode, bd: R && bandiereTesto(bandiereR()) })")
        chk("G5b pagina senza #collaudo: la regata dei giri si apre con le bandiere (classe da subito)", h["segnali"] and h["mode"] == "race" and h["bd"] == "classe", str(h))
        await pg.wait_for_timeout(1500)
        chk("G5c nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
