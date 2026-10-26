# Torneo dell'1b, tappa T1 (1.0.34): criteri di docs/PROPOSTA-TORNEI-1B.md §4, soglie scritte nella fermata 1.
#
#   C1 punteggio: casi costruiti a mano da F15 (appendice A, 44.3), valori attesi scritti qui prima di lanciare; 0 errori su almeno 12.
#   C2 serie completa guidata dal pilota (__sv.pilota, la guida degli avversari principianti sulla barca del giocatore): semi 1-20 nel
#      gioco libero, 101-120 in carriera (con il brevetto di livello 1 già preso). La classifica che il gioco mostra nel riquadro si
#      confronta con una ricalcolata QUI dai tempi d'arrivo delle barche (finestra d'arrivo, punti, scarto, parità: calcolo nostro,
#      non quello del gioco). 0 differenze; 80 regate concluse per gruppo dichiarate. In carriera anche i meriti.
#   C3 ripresa: 10 tornei, pagina chiusa dopo la regata 1, 2 e 3 e riaperta (30 casi): torneo salvato identico e serie completata.
#      (Dalla 1.0.50 la chiusura a metà regata non è più qui: è C11. Prima era «la regata si ricorre da capo».)
#   C11 (1.0.50, docs/PROPOSTA-RITIRO-A-META.md R1-R5, R7): regata lasciata a metà = ritiro. R1 uscita dal menu a 1, 40, 150 e 300 s
#      dal clic su «Corri» x 10 tornei (40 casi); R2 pagina chiusa negli stessi momenti (40); R3 il torneo prosegue fino in fondo
#      (80 su 80); R4 uscita a metà della quarta regata (10); R5 regata finita o già ritirata poi uscita: nessun secondo risultato
#      (10 + 10); R7 uscita dal menu al massimo 2 s. In ogni caso: giocatore ritirato con 5 punti, almeno un avversario arrivato.
#   C4 ritiro: 10 tornei ritirati dopo 0-3 regate: nel salvataggio né torneo né piazzamento, il resto identico a prima.
#   C6 pannello a 1360x650 nel caso peggiore (regata del torneo finita con penalità, errori, distacchi; riquadro con 4 regate,
#      scarti, non arrivate): 0 pixel di eccesso.
#   C10 (aggiunto alla fermata 2, PRIMA di misurare): raffiche attorno a tutte le barche nella regata con raffiche del torneo.
#      Quota del tempo di regata passato dentro una raffica (vento > 1,12 volte il medio, come readI): la media degli avversari
#      almeno metà di quella del giocatore, su 20 regate. Per confronto, la stessa misura nella «Regata nelle raffiche» dell'1a.
# Per regate del ritiro (C3, C4, --giocatore) il giocatore si ritira dalla regata: gli avversari la finiscono da soli.
#
# Uso: python collaudo_torneo.py                # C1, C2, C3, C4, C6, C10 (circa 15 minuti)
#      python collaudo_torneo.py --veloce       # C1, C6, C3 e C4 su 2 tornei, C2 su 2 semi: soglie dei conteggi non valutate
#      python collaudo_torneo.py --giocatore    # C7: pagina senza #collaudo, torneo intero dal menu con una chiusura in mezzo
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
VELOCE = "--veloce" in sys.argv
errori = []
def no(msg): errori.append(msg); print("  NO  " + msg, flush=True)

# ---- calcolo nostro, indipendente dal gioco (F15 A4, A5.2, A2.1, A8, 44.3(c); finestra d'arrivo di appendice S 12.3 col 50%) ----
def punti(r):
    dnf = len(r) + 1; pen = round(2 * dnf) / 10
    out = []
    for b in r:
        if b["fin"] is None: out.append(dnf); continue
        posto = 1 + sum(1 for o in r if o["fin"] is not None and o["fin"] < b["fin"])
        out.append(min(dnf, posto + b["pp"] * pen))
    return out

def serie(ris):
    P = [punti(r) for r in ris]; n = len(ris[0]); cl = []
    for i in range(n):
        p = [r[i] for r in P]; sc = p.index(max(p)) if len(p) >= 4 else -1
        cl.append({"i": i, "p": p, "sc": sc, "tot": sum(v for k, v in enumerate(p) if k != sc)})
    def chiave(x):
        tenuti = sorted(v for k, v in enumerate(x["p"]) if k != x["sc"])
        return (round(x["tot"], 6), tenuti, list(reversed(x["p"])))
    return sorted(cl, key=chiave)

def da_barche(boats):  # dallo stato delle barche a fine regata: finestra d'arrivo 50% del tempo della prima
    fins = [b["fin"] for b in boats if b["fin"] is not None]
    lim = min(fins) * 1.5 if fins else None
    return [{"fin": (round(b["fin"] * 10) / 10 if b["fin"] is not None and lim is not None and b["fin"] <= lim else None), "pp": b["pp"]} for b in boats]

# ---- C1: casi a mano ----
def R(*places_pp):  # regata da posti voluti: (posto, penalità) per barca, posto None = non arrivata; tempi = 100 + 10 * posto
    return [{"fin": None if p is None else 100 + 10 * p, "pp": pp} for p, pp in places_pp]
CASI_PUNTI = [  # (descrizione, regata, punti attesi)
    ("posti semplici", R((2, 0), (1, 0), (3, 0), (4, 0)), [2, 1, 3, 4]),
    ("non arrivata: 5 punti, gli altri salgono di posto", R((None, 0), (1, 0), (2, 0), (3, 0)), [5, 1, 2, 3]),
    ("penalità sul punteggio +1, punti degli altri invariati", R((2, 1), (1, 0), (3, 0), (4, 0)), [3, 1, 3, 4]),
    ("penalità alla prima: pari punti con la seconda", R((1, 1), (2, 0), (3, 0), (4, 0)), [2, 2, 3, 4]),
    ("tetto: quarta con penalità non oltre 5", R((4, 1), (1, 0), (2, 0), (3, 0)), [5, 1, 2, 3]),
    ("tetto: due penalità alla terza = 5", R((3, 2), (1, 0), (2, 0), (4, 0)), [5, 1, 2, 4]),
    ("non arrivata con penalità resta 5", R((None, 1), (1, 0), (2, 0), (3, 0)), [5, 1, 2, 3]),
    ("tutte non arrivate", R((None, 0), (None, 0), (None, 0), (None, 0)), [5, 5, 5, 5]),
]
# serie: (descrizione, regate, ordine atteso, scarti attesi per barca, totali attesi per barca); P(...) = posto di ogni barca, senza penalità.
# Valori attesi ricavati a mano dalle regole, prima di lanciare (i conti sono nei commenti).
P = lambda *perm: R(*[(x, 0) for x in perm])
CASI_SERIE = [
    # Tu 1,1,1,4 -> scarto la 4a, 3; Rossa 2,2,2,1 -> scarto la 1a, 5; Verde 3,3,3,2 -> 8; Blu 4,4,4,3 -> 11
    ("scarto della peggiore", [P(1, 2, 3, 4), P(1, 2, 3, 4), P(1, 2, 3, 4), P(4, 1, 2, 3)], [0, 1, 2, 3], [3, 0, 0, 0], [3, 5, 8, 11]),
    # Tu 4,1,4,1 -> scarto la 1a (la più vecchia), 6; Rossa 1,2,1,2 -> 2a, 4; Verde 2,3,2,3 -> 2a, 7; Blu 3,4,3,4 -> 2a, 10
    ("scarto a pari merito: la più vecchia", [P(4, 1, 2, 3), P(1, 2, 3, 4), P(4, 1, 2, 3), P(1, 2, 3, 4)], [1, 0, 2, 3], [0, 1, 1, 1], [6, 4, 7, 10]),
    # tre regate: 1+2+4 = 7, 2+1+3 = 6, 3+4+2 = 9, 4+3+1 = 8
    ("prima della quarta regata nessuno scarto", [P(1, 2, 3, 4), P(2, 1, 4, 3), P(4, 3, 2, 1)], [1, 0, 3, 2], [-1, -1, -1, -1], [7, 6, 9, 8]),
    # tutti 6 con tenuti 1,2,3; ultima regata: Blu 1, Verde 2, Rossa 3, Tu 4
    ("A8.2 all'ultima regata", [P(1, 2, 3, 4), P(2, 1, 4, 3), P(3, 4, 1, 2), P(4, 3, 2, 1)], [3, 2, 1, 0], [3, 2, 1, 0], [6, 6, 6, 6]),
    # Tu 1,3,2,2(1° con penalità) -> 5, tenuti 1,2,2; Rossa 2,1,3,2 -> 5, tenuti 1,2,2; ultima pari (2 e 2), penultima Tu 2 Rossa 3;
    # Verde 3,2,1,3 -> scarto la 1a, 6; Blu 4,4,4,4 -> 12
    ("A8.2 alla penultima, ultima pari per una penalità", [P(1, 2, 3, 4), P(3, 1, 2, 4), P(2, 3, 1, 4), R((1, 1), (2, 0), (3, 0), (4, 0))], [0, 1, 2, 3], [1, 2, 0, 0], [5, 5, 6, 12]),
    # Tu 1,1,4,4 -> scarto la 3a, 6, tenuti 1,1,4; Rossa 2,2,2,3 -> 6, tenuti 2,2,2: vince Tu (A8.1); Verde 3,3,1,1 -> 5; Blu 4,4,3,2 -> 9
    ("A8.1: pari totale, vince il primo punteggio migliore", [P(1, 2, 3, 4), P(1, 2, 3, 4), P(4, 2, 1, 3), P(4, 3, 1, 2)], [2, 0, 1, 3], [2, 3, 0, 0], [6, 6, 5, 9]),
    # Tu 1,5,1,1 -> 3; Rossa 2,1,2,2 -> scarto la 1a, 5; Verde 3,2,3,3 -> 8; Blu 4,3,4,4 -> 11
    ("non arrivata scartata", [P(1, 2, 3, 4), R((None, 0), (1, 0), (2, 0), (3, 0)), P(1, 2, 3, 4), P(1, 2, 3, 4)], [0, 1, 2, 3], [1, 0, 0, 0], [3, 5, 8, 11]),
]

async def c1(pg):
    print("\n== C1: punteggio, casi a mano", flush=True)
    n = 0; bad = 0
    for nome, r, att in CASI_PUNTI:
        got = await pg.evaluate("r => __sv.torPunti(r)", r); n += 1
        ok = [round(x, 6) for x in got] == att and punti(r) == att
        if not ok: bad += 1; no(f"C1 {nome}: gioco {got}, nostro {punti(r)}, atteso {att}")
        else: print(f"  ok  {nome}: {att}", flush=True)
    for nome, ris, ordine, sc, tot in CASI_SERIE:
        got = await pg.evaluate("r => __sv.torSerie(r)", ris); n += 1
        g_ord = [x["i"] for x in got]; g_sc = {x["i"]: x["sc"] for x in got}; g_tot = {x["i"]: x["tot"] for x in got}
        ok = g_ord == ordine and [g_sc[i] for i in range(4)] == sc and [round(g_tot[i], 6) for i in range(4)] == tot
        nos = serie(ris); ok_n = [x["i"] for x in nos] == ordine
        if not (ok and ok_n): bad += 1; no(f"C1 {nome}: gioco ordine {g_ord} scarti {[g_sc[i] for i in range(4)]} totali {[g_tot[i] for i in range(4)]}; nostro {[x['i'] for x in nos]}; atteso {ordine} {sc} {tot}")
        else: print(f"  ok  {nome}: ordine {ordine}, totali {tot}", flush=True)
    print(f"  C1: {bad} errori su {n} casi (soglia: 0 su almeno 12)", flush=True)
    if n < 12 or bad: no(f"C1 fuori soglia: {bad} errori su {n}")
    return n, bad

# ---- regata del torneo, nella pagina ----
CORRI = """async (modo) => {   // modo: "pilota" (guida fino all'arrivo o alla finestra), "ritiro" (si ritira subito)
  const sv = __sv, dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0]; let mosso = 0, prev = null;
  if (modo === "ritiro"){ window.confirm = () => true; document.getElementById("rRet").click(); sv.run(dt, 1); }
  else while (me.fin === null && !me.dnf && R.t < 1500){ const t = sv.pilota(dt); if (prev !== null && t !== prev) mosso++; prev = t; sv.run(dt, 1); }
  if (me.fin === null && !me.dnf) return { fallita: "pilota non arrivato in 1500 s" };
  const regin = [...R.boats].map(b => b.name);
  document.getElementById("rTor").click();                            // chiude la regata (avversari fino in fondo) e mostra la classifica
  const boats = R.boats.map(b => ({ name: b.name, fin: b.fin, pp: b.pp || 0, dnf: !!b.dnf, ret: !!b.ret }));
  const righe = [...document.querySelectorAll("#torBody table.tor tbody tr")].map(tr => [...tr.children].map(td => td.textContent));
  const score = document.querySelector("#torBody .score"), mer = [...document.querySelectorAll("#torBody p")].map(p => p.textContent).find(t => t.startsWith("Meriti"));
  return { boats, righe, mosso, finale: score ? score.textContent : null, meriti: mer || null, cond: R.boats.length,
           prog: (() => { try { return JSON.parse(localStorage.getItem(sv.store)); } catch(e){ return null; } })() };
}"""
NOMI = ["Tu", "Rossa", "Verde", "Blu"]
fmt = lambda v: str(round(v * 10) / 10).replace(".0", "").replace(".", ",")

def confronta(tag, ris, righe):
    cl = serie(ris); diff = 0
    for n, x in enumerate(cl):
        cells = [fmt(v) + ("*" if ris[j][x["i"]]["pp"] else "") + ("°" if ris[j][x["i"]]["fin"] is None else "") for j, v in enumerate(x["p"])]
        cells = [("(" + c + ")" if j == x["sc"] else c) for j, c in enumerate(cells)]
        atteso = [f"{n + 1}°", NOMI[x["i"]]] + cells + [fmt(x["tot"])]
        if n >= len(righe) or righe[n] != atteso:
            diff += 1; no(f"{tag}: riga {n + 1} del gioco {righe[n] if n < len(righe) else None}, nostra {atteso}")
    return diff, cl

async def pagina(b, ctx=None, url=BASE + "#collaudo"):
    ctx = ctx or await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url); await pg.wait_for_timeout(150)
    return ctx, pg, errs

async def prepara(pg, seme, carriera):
    await pg.evaluate("""([seme, carriera]) => { __sv.fast(0);
      if (carriera){ localStorage.setItem("scuolaVelaModo", "carriera");
        localStorage.setItem("scuolaVelaCarriera.v1", JSON.stringify({ done: {}, best: {}, clean: {}, brevetto: { data: "2026-10-20" } })); }
      __seed(seme); }""", [seme, carriera])
    if carriera: await pg.reload(); await pg.wait_for_timeout(150); await pg.evaluate("s => { __sv.fast(0); __seed(s); }", seme)
    await pg.evaluate("__sv.store = localStorage.getItem('scuolaVelaModo') === 'carriera' ? 'scuolaVelaCarriera.v1' : 'scuolaVelaSim.v1'")
    await pg.evaluate("__sv.torApri()")

async def c2(b, semi, carriera):
    print(f"\n== C2: tornei col pilota, semi {semi[0]}-{semi[-1]}, {'carriera' if carriera else 'gioco libero'}", flush=True)
    regate = diff = 0
    for seme in semi:
        ctx, pg, errs = await pagina(b); await prepara(pg, seme, carriera)
        ris = []; ultimo = None
        for k in range(4):
            r = await pg.evaluate(CORRI, "pilota")
            if "fallita" in r: no(f"C2 seme {seme} regata {k + 1}: {r['fallita']}"); break
            if r["mosso"] == 0: no(f"C2 seme {seme} regata {k + 1}: il pilota non ha mosso la barra")
            ris.append(da_barche(r["boats"])); regate += 1; ultimo = r
            d, cl = confronta(f"C2 seme {seme} regata {k + 1}", ris, r["righe"]); diff += d
        if len(ris) == 4:
            cl = serie(ris); pos = [x["i"] for x in cl].index(0) + 1
            if ultimo["finale"] != f"{pos}° su 4": diff += 1; no(f"C2 seme {seme}: finale del gioco {ultimo['finale']}, nostro {pos}° su 4")
            pr = ultimo["prog"] or {}
            if "torneo" in pr: no(f"C2 seme {seme}: torneo finito ma ancora nel salvataggio")
            if carriera:
                mer = [6, 4, 3, 2][pos - 1] + (1 if all(r[0]["pp"] == 0 for r in ris) else 0)
                if ultimo["meriti"] != f"Meriti di Competizione dell'1b: {mer}.": diff += 1; no(f"C2 seme {seme}: meriti del gioco «{ultimo['meriti']}», nostri {mer}")
                if (pr.get("torneoFatto") or {}).get("mer", -1) < mer: no(f"C2 seme {seme}: torneoFatto {pr.get('torneoFatto')} con meriti {mer}")
            pp = sum(r[0]["pp"] for r in ris); na = sum(1 for r in ris for x in r if x["fin"] is None)
            print(f"  seme {seme}: {pos}° · punti Tu {[fmt(v) for v in cl[[x['i'] for x in cl].index(0)]['p']]} · penalità Tu {pp} · non arrivate {na} su 16", flush=True)
        if errs: no(f"C2 seme {seme}: errore nella pagina {errs[0]}")
        await ctx.close()
    print(f"  C2: {diff} differenze; regate concluse {regate} su {4 * len(semi)}", flush=True)
    return regate, diff

async def c3(b, n):
    print(f"\n== C3: ripresa, {n} tornei, chiusura dopo le regate 1, 2 e 3", flush=True)
    casi = ok = 0; complete = 0
    for t in range(n):
        ctx, pg, errs = await pagina(b); await prepara(pg, 200 + t, False)
        fatti = 0
        for k in range(4):
            r = await pg.evaluate(CORRI, "ritiro"); fatti += 1
            if k < 3:
                prima = await pg.evaluate("localStorage.getItem('scuolaVelaSim.v1')")
                await pg.close(); pg = await ctx.new_page(); await pg.add_init_script(SEME); pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
                await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
                dopo = await pg.evaluate("localStorage.getItem('scuolaVelaSim.v1')")
                stato = await pg.evaluate("document.getElementById('goTor').textContent")
                casi += 1
                buono = prima == dopo and json.loads(dopo)["torneo"]["ris"].__len__() == k + 1 and f"regata {k + 2} di 4" in stato
                ok += buono
                if not buono: no(f"C3 torneo {t + 1} dopo la regata {k + 1}: salvataggio uguale {prima == dopo}, menu «{stato}»")
                await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", 400 + 10 * t + k)
        if r.get("finale") and "torneo" not in (r["prog"] or {}): complete += 1
        else: no(f"C3 torneo {t + 1}: serie non completata ({r.get('finale')})")
        if errs: no(f"C3 torneo {t + 1}: errore nella pagina {errs[0]}")
        await ctx.close()
    print(f"  C3: {ok} su {casi} casi con il torneo identico dopo la riapertura; serie completate {complete} su {n}", flush=True)
    return casi, ok, complete

# ---- C11: regata lasciata a metà (1.0.50) ----
MOMENTI = [1, 40, 150, 300]   # secondi di regata (dal clic su «Corri») prima di uscire; con il conto alla rovescia il primo è prima del via
AVANTI = """([sec, esci]) => { const sv = __sv, dt = 1 / 60; document.getElementById("torGo").click();
  const me = sv.R.boats[0]; for (let k = 0; k < sec * 60; k++){ sv.pilota(dt); sv.run(dt, 1); }
  window.confirm = () => true; const t0 = performance.now();
  if (esci === "menu") document.getElementById("toMenu").click(); else if (esci === "pagehide") dispatchEvent(new Event("pagehide"));
  return performance.now() - t0; }"""
async def chiudi(pg):  # la pagina viene lasciata: pagehide parte (misurato: con page.close() da solo, anche run_before_unload, NON parte in Chromium headless)
    await pg.goto("about:blank"); await pg.close()  # limite: la chiusura vera della scheda nel browser di Ale non si può provare qui
async def stato(pg):
    return await pg.evaluate("s => { try { return JSON.parse(localStorage.getItem(s)); } catch(e){ return null; } }", "scuolaVelaSim.v1")

def regata_ritirata(tor, k, tag):
    """True se la regata k (0-based) è registrata con il giocatore ritirato (5 punti) e almeno un avversario arrivato."""
    if not tor or len(tor["ris"]) != k + 1: no(f"C11 {tag}: regate registrate {len(tor['ris']) if tor else None}, attese {k + 1}"); return False
    r = tor["ris"][k]
    if r[0]["fin"] is not None or punti(r)[0] != 5: no(f"C11 {tag}: giocatore non ritirato ({r[0]})"); return False
    if not any(x["fin"] is not None for x in r[1:]): no(f"C11 {tag}: nessun avversario arrivato"); return False
    return True

async def c11(b, n):
    print(f"\n== C11: regata lasciata a metà = ritiro, {n} tornei", flush=True)
    totale = {"menu": 0, "chiusura": 0, "completi": 0, "q4": 0, "r5": 0}; lento = 0.0
    for t in range(n):
        for esci in ("menu", "chiusura"):
            for m in MOMENTI:
                tag = f"torneo {t + 1} {esci} a {m} s"
                ctx, pg, errs = await pagina(b); await prepara(pg, 500 + t, False)
                dt = await pg.evaluate(AVANTI, [m, "menu" if esci == "menu" else None])
                if esci == "menu": lento = max(lento, dt)
                else: await chiudi(pg); pg = await ctx.new_page(); await pg.add_init_script(SEME); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
                tor = (await stato(pg) or {}).get("torneo")
                if regata_ritirata(tor, 0, tag): totale[esci] += 1
                await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", 600 + t)
                for k in range(1, 4):   # il torneo prosegue: le altre 3 regate col ritiro subito
                    r = await pg.evaluate(CORRI, "ritiro")
                if r.get("finale") and "torneo" not in (r["prog"] or {}) and (r["prog"] or {}).get("torneoFatto"): totale["completi"] += 1
                else: no(f"C11 {tag}: torneo non concluso ({r.get('finale')})")
                if errs: no(f"C11 {tag}: errore nella pagina {errs[0]}")
                await ctx.close()
        # R4: uscita a metà della quarta regata
        for esci in ("menu", "chiusura"):
            ctx, pg, errs = await pagina(b); await prepara(pg, 700 + t, False)
            for k in range(3): await pg.evaluate(CORRI, "ritiro")
            await pg.evaluate("__sv.torApri()")
            dt = await pg.evaluate(AVANTI, [40, "menu" if esci == "menu" else None])
            if esci == "chiusura": await chiudi(pg); pg = await ctx.new_page(); await pg.add_init_script(SEME); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
            pr = await stato(pg)
            if pr and "torneo" not in pr and pr.get("torneoFatto"): totale["q4"] += 1
            else: no(f"C11 torneo {t + 1} quarta regata {esci}: torneo non chiuso ({pr and pr.get('torneo') and len(pr['torneo']['ris'])})")
            await ctx.close()
        # R5: regata già finita, poi uscita (ritirata col pulsante; arrivata col pilota): nessun secondo risultato
        for modo in ("ritiro", "arrivo"):
            ctx, pg, errs = await pagina(b); await prepara(pg, 800 + t, False)
            if modo == "ritiro": await pg.evaluate(CORRI, "ritiro")
            else: await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; document.getElementById("torGo").click(); const me = sv.R.boats[0];
              while (me.fin === null && !me.dnf && sv.R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); } document.getElementById("rTor").click(); }""")
            prima = await stato(pg)
            await pg.evaluate("dispatchEvent(new Event('pagehide'))"); await pg.evaluate("document.getElementById('toMenu').click()")
            dopo = await stato(pg)
            if prima and dopo and len(prima["torneo"]["ris"]) == 1 and prima == dopo: totale["r5"] += 1
            else: no(f"C11 torneo {t + 1} R5 {modo}: salvataggio cambiato o regata non registrata")
            await ctx.close()
    print(f"  C11: R1 menu {totale['menu']}/{4 * n}, R2 chiusura {totale['chiusura']}/{4 * n}, R3 tornei conclusi {totale['completi']}/{8 * n}, "
          f"R4 {totale['q4']}/{2 * n}, R5 {totale['r5']}/{2 * n}, uscita dal menu al massimo {lento / 1000:.2f} s (R7)", flush=True)
    return totale, lento

async def c4(b, n):
    print(f"\n== C4: ritiro dal torneo, {n} tornei", flush=True)
    ok = 0
    for t in range(n):
        ctx, pg, errs = await pagina(b); await prepara(pg, 500 + t, False)
        prima = await pg.evaluate("localStorage.getItem('scuolaVelaSim.v1')")
        k = t % 4
        if k == 0: await pg.evaluate("() => { document.getElementById('torGo').click(); __sv.run(1 / 60, 60 * 30); }")  # ritiro dal torneo senza regate concluse:
        for j in range(k): await pg.evaluate(CORRI, "ritiro")                                                             # si riapre il riquadro dal menu
        if k == 0: await pg.evaluate("() => document.getElementById('toMenu').click()")
        if k == 0: await pg.evaluate("__sv.torApri()")
        await pg.evaluate("() => document.getElementById('torRit').click()")
        dopo = json.loads(await pg.evaluate("localStorage.getItem('scuolaVelaSim.v1')") or "{}")
        p0 = json.loads(prima or "{}") or {"done": {}, "best": {}, "clean": {}}
        buono = "torneo" not in dopo and "torneoFatto" not in dopo and all(dopo.get(x, {}) == p0.get(x, {}) for x in ("done", "best", "clean", "race"))
        ok += buono
        print(f"  {'ok ' if buono else 'NO '} torneo {t + 1}, ritirato dopo {k} regate: chiavi del salvataggio {sorted(dopo)}", flush=True)
        if not buono: no(f"C4 torneo {t + 1}: dopo il ritiro {sorted(dopo)}")
        if errs: no(f"C4 torneo {t + 1}: errore nella pagina {errs[0]}")
        await ctx.close()
    print(f"  C4: {ok} su {n}", flush=True)
    return ok

async def c6(b):
    print("\n== C6: pannello e riquadro a 1360x650, caso peggiore", flush=True)
    ctx, pg, errs = await pagina(b); await prepara(pg, 7, False)
    await pg.evaluate("document.fonts.ready")
    # tre regate concluse con penalità e non arrivate, poi la quarta: giocatore arrivato con penalità ed errori, distacchi da due barche
    intro = await pg.evaluate("() => { const q = document.getElementById('torBody'); return q.scrollHeight - q.clientHeight; }")
    print(f"  riquadro d'inizio: {intro} px che scorrono", flush=True)
    if intro > 0: no(f"C6 riquadro d'inizio: {intro} px")
    for k in range(3): await pg.evaluate(CORRI, "ritiro")
    await pg.evaluate("""() => { const T = __sv.tor; T.ris.forEach((r, j) => { r[0].pp = 2; r[1].fin = null; r[2].pp = 1; }); }""")
    await pg.evaluate("""() => { document.getElementById('torGo').click(); const R = __sv.R, me = R.boats[0];
      __sv.run(1 / 60, 60 * 400);
      Object.assign(__sv.reg, { capsizes: 2, gybesV: 1, irons: 2, ironsSec: 14, wrongMarks: 1, contacts: 3, contactsPen: 2, ocs: 1, outLine: 2 });
      R.boats.forEach((b, i) => { b.pp = 3; }); R.boats[1].fin = R.t - 30; R.boats[2].fin = R.t - 12; me.fin = R.t;
      R.lastRule = "Contatto con Verde: tu eri sopravento con le stesse mure e dovevi stare lontano. Penalità di 1 punto sul punteggio della regata.";
      __sv.run(1 / 60, 2); __sv.panel(); }""")
    await pg.wait_for_timeout(200)
    pan = await pg.evaluate("()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}")
    await pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent / "output" / "torneo_pannello.png"))
    await pg.evaluate("() => document.getElementById('rTor').click()")
    await pg.wait_for_timeout(200)
    dlg = await pg.evaluate("""() => { const d = document.getElementById('torDlg'), q = document.getElementById('torBody'), r = d.getBoundingClientRect();
      return { dentro: r.top >= 0 && r.bottom <= innerHeight, scorre: q.scrollHeight - q.clientHeight, righe: q.querySelectorAll('tbody tr').length,
               celle: q.querySelectorAll('tbody td').length, larg: q.scrollWidth - q.clientWidth }; }""")
    await pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent / "output" / "torneo_classifica.png"))
    print(f"  pannello: {pan} px di eccesso; riquadro: {dlg}", flush=True)
    if pan > 0: no(f"C6 pannello +{pan} px")
    if not dlg["dentro"] or dlg["scorre"] > 0 or dlg["larg"] > 0 or dlg["righe"] != 4 or dlg["celle"] != 4 * 7: no(f"C6 riquadro {dlg}")
    if errs: no(f"C6 errore nella pagina {errs[0]}")
    await ctx.close()

RAFFICHE = """async ([torneo]) => {   // quota di tempo dentro una raffica, giocatore e avversari, regata col pilota
  const sv = __sv, dt = 1 / 60;
  if (torneo) document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], dentro = R.boats.map(() => 0); let n = 0;
  while (me.fin === null && !me.dnf && R.t < 900){ sv.pilota(dt); sv.run(dt, 1);
    if (R.t >= 0){ n++; R.boats.forEach((b, i) => { if (b.fin === null && sv.windAt(b.S.x, b.S.y).tws > sv.envTws() * 1.12) dentro[i]++; }); } }
  return { quota: dentro.map(v => v / Math.max(1, n)), passi: n, gusts: R.tor };
}"""

async def c10(b, semi):
    print(f"\n== C10: raffiche attorno a tutte le barche, {len(semi)} regate per tipo", flush=True)
    out = {}
    for tipo in ("torneo", "1a"):
        qs = []
        for seme in semi:
            ctx, pg, errs = await pagina(b)
            await pg.evaluate("s => { __sv.fast(0); __seed(s); }", seme)
            if tipo == "torneo":  # torneo nuovo con la regata 1 già fatta: si corre la 2, quella con le raffiche
                await pg.evaluate("""() => { __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); document.getElementById('torGo').click();
                  window.confirm = () => true; document.getElementById('rRet').click(); __sv.run(1 / 60, 1); document.getElementById('rTor').click(); }""")
                r = await pg.evaluate(RAFFICHE, [True])
            else:
                await pg.evaluate("() => __sv.openItem(['r', 1])")
                r = await pg.evaluate(RAFFICHE, [False])
            if errs: no(f"C10 {tipo} seme {seme}: {errs[0]}")
            qs.append(r["quota"]); await ctx.close()
        tu = sum(q[0] for q in qs) / len(qs); av = sum(sum(q[1:]) / 3 for q in qs) / len(qs)
        out[tipo] = (tu, av, len(qs))
        print(f"  {tipo}: tempo in raffica giocatore {tu:.1%}, media avversari {av:.1%} (rapporto {av / tu if tu else 0:.2f}) su {len(qs)} regate", flush=True)
    tu, av, n = out["torneo"]
    if n < len(semi) or tu == 0 or av < 0.5 * tu: no(f"C10 fuori soglia: avversari {av:.1%} contro giocatore {tu:.1%}")
    return out

async def giocatore(b):
    # C7: pagina senza #collaudo, come la carica un giocatore: dal menu, riquadro delle istruzioni con «Parti», ritiro dalla regata
    # col pulsante (gli avversari la finiscono), classifica, chiusura della pagina dopo la regata 2, ripresa dal menu, fino alla fine.
    print("\n== C7: torneo da giocatore, pagina senza #collaudo", flush=True)
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    cons = []
    async def nuova():
        pg = await ctx.new_page(); pg.on("console", lambda m: m.type == "error" and cons.append(m.text)); pg.on("pageerror", lambda e: cons.append(str(e)))
        pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(BASE); await pg.wait_for_timeout(300); return pg
    pg = await nuova(); fatti = 0; finale = None
    for k in range(4):
        await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if not await pg.is_visible("#bGo"): no(f"C7 regata {k + 1}: niente riquadro delle istruzioni"); break
        await pg.click("#bGo"); await pg.wait_for_timeout(1500)                      # un secondo e mezzo di conto alla rovescia vero
        t = await pg.inner_text("#where")
        await pg.click("#rRet"); await pg.wait_for_timeout(300)
        await pg.click("#finTor"); await pg.wait_for_timeout(500)  # 1.0.36: a regata finita i pulsanti stanno nel riquadro sul mare, quelli del pannello sono nascosti
        righe = await pg.locator("#torBody tbody tr").count()
        fatti += 1
        print(f"  regata {k + 1}: «{t}», classifica con {righe} barche", flush=True)
        if righe != 4: no(f"C7 regata {k + 1}: {righe} righe")
        if k == 3: finale = await pg.inner_text("#torBody .score"); await pg.click("#torMenu")
        elif k == 1:
            await pg.close(); pg = await nuova()                                       # chiusura della pagina dopo la regata 2
            st = await pg.inner_text("#goTor"); print(f"  dopo la riapertura il menu dice: {st.splitlines()}", flush=True)
            if "regata 3 di 4" not in st: no(f"C7: dopo la riapertura «{st}»")
        else: await pg.click("#torMenu"); await pg.wait_for_timeout(200)
    st = await pg.inner_text("#goTor")
    print(f"  regate {fatti} su 4, finale «{finale}», menu «{' '.join(st.split())}», errori nella console: {cons or 'nessuno'}", flush=True)
    if fatti != 4 or not finale or "migliore" not in st: no(f"C7 non completo: {fatti} regate, finale {finale}")
    if cons: no(f"C7 errori nella console: {cons[:3]}")
    await ctx.close()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if "--giocatore" in sys.argv: await giocatore(b)
        else:
            ctx, pg, errs = await pagina(b); await c1(pg); await ctx.close()
            await c6(b)
            if VELOCE:
                await c2(b, [1, 2], False); await c3(b, 2); await c4(b, 2); await c11(b, 1)
            else:
                ra, d = await c2(b, list(range(1, 21)), False)
                rb, d2 = await c2(b, list(range(101, 121)), True)
                if ra != 80 or rb != 80: no(f"C2: regate concluse {ra} e {rb} su 80")
                casi, ok, comp = await c3(b, 10)
                if casi != 30 or ok != 30 or comp != 10: no(f"C3 fuori soglia: {ok} su {casi}, complete {comp}")
                if await c4(b, 10) != 10: no("C4 fuori soglia")
                tt, lento = await c11(b, 10)
                if tt["menu"] != 40 or tt["chiusura"] != 40 or tt["completi"] != 80 or tt["q4"] != 20 or tt["r5"] != 20: no(f"C11 fuori soglia: {tt}")
                if lento > 2000: no(f"C11 R7: uscita dal menu {lento / 1000:.2f} s (soglia 2 s)")
                await c10(b, list(range(1, 21)))
        await b.close()
    print("\nESITO: " + ("OK" if not errori else f"FALLITO ({len(errori)}): " + "; ".join(errori[:8])), flush=True)
    sys.exit(1 if errori else 0)

asyncio.run(main())
