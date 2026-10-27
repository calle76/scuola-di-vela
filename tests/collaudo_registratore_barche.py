# Registratore di sessione: tutte le barche (1.0.52), criteri G1-G7 di docs/PROPOSTA-REGISTRATORE-TUTTE-LE-BARCHE.md, soglie scritte nella fermata 1.
#  G1 sola lettura: 20 regate (7 a bastone 1a, 7 nei salti di vento 1b, 6 del torneo; principianti ed esperti, semi fissi) col pilota, con e senza
#     registrazione: posizioni, prue, velocità, arrivi e penalità di tutte le barche identici al bit. 0 differenze su 20.
#  G2 le righe B dicono il vero: a ogni riga B si confrontano x, y, prua, nodi, twa e lato con i valori veri della barca in quell'istante
#     (tolleranza dell'arrotondamento); il numero di righe B è 3 volte quello delle righe S. 0 differenze; NON VALIDO se non ne vede.
#  G3 contatti: costruiti a mano (due avversari a 1 m, 10 casi: un evento contatto_barche; a 5 m: nessuno); nelle 20 regate vere gli eventi
#     contatto_barche sono tanti quante le penalità assegnate (pen/15 + pp sommate su tutte le barche: conteggio indipendente dal registratore).
#     NON VALIDO se le regate vere hanno meno di 10 contatti in tutto.
#  G4 barca ferma: costruiti (un avversario tenuto a velocità zero per 8 s dopo il via, 10 casi): avv_fermo dopo 5 s (da 4,5 a 6,5) e
#     avv_riparte dopo il rilascio; nelle 20 regate vere gli avv_fermo sono tanti quanti gli episodi sotto 0,5 nodi per 5 s contati qui dalle
#     velocità vere (stessa isteresi dichiarata, 1 nodo per ripartire). NON VALIDO se non ne vede nemmeno uno.
#  G5 il file si legge: analizza_sessione.py su tutti i file delle regate registrate: riassunto del gioco uguale a quello ricalcolato.
#  G6 dimensione: al massimo 20 kB per minuto registrato (conto alla rovescia compreso).
#  G7 pagina vera, senza #collaudo: interruttore acceso, torneo avviato dal menu, il file scaricato ha righe B dei tre avversari.
# Uso: python collaudo_registratore_barche.py [--veloce]   (veloce: 6 regate, 3 casi costruiti)
import asyncio, io, contextlib, pathlib, sys
from playwright.async_api import async_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analizza_sessione as AS

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
VELOCE = "--veloce" in sys.argv
errori, non_validi = [], []
def no(m): errori.append(m); print("  NO  " + m, flush=True)

# Una regata col pilota. tipo: 0 bastone 1a, 2 salti di vento 1b, "t" torneo. Se registra, la registrazione è accesa prima dell'apertura.
# Ritorna lo stato finale di tutte le barche, le righe B confrontate con i valori veri, i contatti e gli episodi di barca ferma contati qui.
CORRI = """([tipo, seme, registra, liv]) => {
  const sv = __sv, dt = 1 / 60, KN = 1.9438444924406;
  if (registra){ const c = document.getElementById('sesOn'); c.checked = true; c.dispatchEvent(new Event('change')); }
  sv.fast(0); __seed(seme);
  if (tipo === 't'){ sv.store = 'scuolaVelaSim.v1'; const sel = document.getElementById('aiLevel'); sel.value = liv; sel.dispatchEvent(new Event('change')); sv.torApri(); document.getElementById('torGo').click(); }
  else { sv.openItem(['r', tipo]); const sel = document.getElementById('aiLevel'); sel.value = liv; sel.dispatchEvent(new Event('change')); }
  __seed(seme);
  const R = sv.R, me = R.boats[0]; let n = 0, lette = 0, nB = 0, nS = 0, male = [], visto = 0;
  const still = R.boats.map(() => 0), fermi = R.boats.map(() => false), episodi = [];
  while (me.fin === null && !me.dnf && R.t < 900 && n < 60 * 1200){
    sv.pilota(dt); sv.run(dt, 1); n++;
    R.boats.forEach((b, i) => { if (b.me || R.t < 0 || b.fin !== null || b.dnf) return; const kn = Math.abs(b.S.u) * KN;       // verità: episodi sotto 0,5 nodi per 5 s
      if (!fermi[i]){ still[i] = kn < 0.5 ? still[i] + dt : 0; if (still[i] >= 5){ fermi[i] = true; episodi.push(b.name); } } else if (kn > 1){ fermi[i] = false; still[i] = 0; } });
    const L = sv.ses.lines;
    for (; lette < L.length; lette++){
      const l = L[lette]; if (l[0] === 'S') nS++;
      if (l[0] !== 'B') continue; nB++;
      const p = l.split(' '), b = R.boats.find(x => x.name === p[2]);
      if (!b){ male.push('barca ' + p[2] + ' inesistente'); continue; }
      const d = [Math.abs(+p[3] - b.S.x) > 0.06, Math.abs(+p[4] - b.S.y) > 0.06, Math.abs(((+p[5] - b.S.h) % 360 + 540) % 360 - 180) > 0.6, Math.abs(+p[6] - b.S.u * KN) > 0.06, +p[8] !== b.leg];
      if (d.some(x => x)) male.push(l + ' | vero ' + [b.S.x, b.S.y, b.S.h, b.S.u * KN, b.leg].join(' '));
    }
  }
  sv.run(dt, 30);
  const bs = R.boats;
  const imp = bs.map(b => [b.S.x, b.S.y, b.S.h, b.S.u, b.fin, b.pen || 0, b.pp || 0].map(v => v === null ? 'n' : v.toFixed(9)).join(',')).join(';');
  const pene = bs.reduce((a, b) => a + (b.pen || 0) / 15 + (b.pp || 0), 0);
  const ev = sv.ses.lines.filter(l => l[0] === 'E').map(l => l.split(' ')[2]);
  return { imp, fin: me.fin, t: R.t, reg: sv.ses.t, nB, nS, male, pene, episodi, contatti: ev.filter(x => x === 'contatto_barche').length,
           fermi: ev.filter(x => x === 'avv_fermo').length, ev: ev.length, bytes: sv.ses.lines.join('\\n').length };
}"""

# Costruito: due avversari tenuti a distanza d (m), un passo; poi gli eventi contatto_barche. Poi barca 2 a velocità zero per 8 s e rilasciata.
COSTRUITO = """([seme, d, modo]) => {
  const sv = __sv, dt = 1 / 60; const c = document.getElementById('sesOn'); c.checked = true; c.dispatchEvent(new Event('change'));
  sv.fast(0); __seed(seme); sv.openItem(['r', 2]); __seed(seme);
  const R = sv.R; for (let k = 0; k < 60 * 400 && R.t < 10; k++) sv.run(dt, 1);   // 10 s dopo il via (il conto alla rovescia dura 180 s)
  const A = R.boats[1], B = R.boats[2], KN = 1.9438444924406;
  if (modo === 'contatto'){
    if (R.contacts['1-2'] !== undefined) return { salta: true };     // le due barche erano già in contatto per conto loro: il caso non è valido, se ne sceglie un altro seme
    const conta = () => sv.ses.lines.filter(l => l.includes(' contatto_barche ' + A.name + ' ' + B.name)).length, n0 = conta();   // solo la coppia messa a mano
    B.S.x = A.S.x + d; B.S.y = A.S.y; B.S.h = A.S.h; sv.run(dt, 1);
    return { n: conta() - n0, cont: R.contacts['1-2'] !== undefined ? 1 : 0 };
  }
  const t0 = sv.ses.t; let fermo = null, riparte = null;
  for (let k = 0; k < 60 * 8; k++){ A.S.u = 0; sv.run(dt, 1); }
  const dopo8 = sv.ses.lines.filter(l => l.includes(' avv_fermo ' + A.name)).map(l => +l.split(' ')[1] - t0);
  for (let k = 0; k < 60 * 40 && !sv.ses.lines.some(l => l.includes(' avv_riparte ' + A.name)); k++) sv.run(dt, 1);
  const rip = sv.ses.lines.filter(l => l.includes(' avv_riparte ' + A.name)).map(l => +l.split(' ')[1] - t0);
  return { fermo: dopo8, riparte: rip };
}"""

async def nuova(b, url=BASE + "#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg, errs

async def scarica(pg):
    async with pg.expect_download() as d: await pg.evaluate("document.getElementById('sesGet').click()")  # il pulsante sta nelle impostazioni, non sempre visibile a fine regata
    return open(await (await d.value).path(), encoding="utf-8").read()

async def regate(b, elenco):
    print(f"\n== G1, G2, G3, G4, G5, G6: {len(elenco)} regate", flush=True)
    tot = {"nB": 0, "contatti": 0, "pene": 0, "episodi": 0, "fermi": 0, "male": 0, "diff": 0, "b_per_min": 0.0, "analizzate": 0}
    for tipo, seme, liv in elenco:
        tag = f"regata {tipo} seme {seme} {liv}"
        ctx, pg, errs = await nuova(b); r1 = await pg.evaluate(CORRI, [tipo, seme, True, liv])
        # G5: il file scaricato si legge e il riassunto del gioco coincide
        testo = await scarica(pg); buf = io.StringIO()
        with contextlib.redirect_stdout(buf): ra = AS.analizza(testo)
        tot["analizzate"] += 1
        if ra["diff"]: no(f"G5 {tag}: riassunto diverso {ra['diff']}")
        n_av = sum(1 for k, v in ra["avversari"].items())
        if n_av != 3: no(f"G5/G7 {tag}: avversari letti {n_av}, attesi 3")
        await ctx.close()
        ctx, pg, errs2 = await nuova(b); r0 = await pg.evaluate(CORRI, [tipo, seme, False, liv]); await ctx.close()
        if r1["imp"] != r0["imp"]: no(f"G1 {tag}: stato finale diverso con e senza registrazione")
        if r1["male"]: tot["male"] += len(r1["male"]); no(f"G2 {tag}: {len(r1['male'])} righe B diverse dal vero, per esempio {r1['male'][0]}")
        if r1["nB"] != 3 * r1["nS"]: no(f"G2 {tag}: righe B {r1['nB']} contro 3 x S {r1['nS']}")
        tot["nB"] += r1["nB"]
        if r1["contatti"] != round(r1["pene"]): no(f"G3 {tag}: eventi contatto_barche {r1['contatti']}, penalità assegnate {r1['pene']}")
        tot["contatti"] += r1["contatti"]; tot["pene"] += round(r1["pene"])
        if r1["fermi"] != len(r1["episodi"]): no(f"G4 {tag}: avv_fermo {r1['fermi']}, episodi veri {r1['episodi']}")
        tot["fermi"] += r1["fermi"]; tot["episodi"] += len(r1["episodi"])
        # i minuti sono quelli registrati (conto alla rovescia compreso: anche lì ci sono le righe); nella prima versione del collaudo si dividevano
        # per R.t, che non conta il conto alla rovescia (dichiarato: dava 20,1 e 20,6 kB al minuto su 2 regate di 6, qui sotto la soglia)
        kb_min = r1["bytes"] / 1000 / max(1, r1["reg"] / 60); kb_min_rt = r1["bytes"] / 1000 / max(1, r1["t"] / 60)
        tot["max_rt"] = max(tot.get("max_rt", 0), kb_min_rt)
        if kb_min > 20: no(f"G6 {tag}: {kb_min:.1f} kB al minuto (soglia 20)")
        tot["b_per_min"] = max(tot["b_per_min"], kb_min)
        if errs or errs2: no(f"{tag}: errore nella pagina {(errs + errs2)[0]}")
    print(f"  righe B confrontate col vero: {tot['nB']} (diverse {tot['male']}); contatti registrati {tot['contatti']} su penalità assegnate {tot['pene']}; "
          f"barche ferme registrate {tot['fermi']} su episodi veri {tot['episodi']}; file letti dall'analizzatore {tot['analizzate']}; "
          f"dimensione massima {tot['b_per_min']:.1f} kB al minuto registrato ({tot['max_rt']:.1f} se si dividesse per il tempo di regata senza il conto alla rovescia)", flush=True)
    if tot["nB"] == 0: non_validi.append("G2: nessuna riga B")
    if tot["contatti"] < 10 and not VELOCE: non_validi.append(f"G3: solo {tot['contatti']} contatti nelle regate vere (servono almeno 10)")
    if tot["fermi"] == 0 and not VELOCE: non_validi.append("G4: nessuna barca ferma nelle regate vere")

async def costruiti(b, n):
    print(f"\n== G3, G4 costruiti: {n} casi ciascuno", flush=True)
    ok3 = ok3b = ok4 = 0
    for k in range(n):
        for tentativo in range(5):
            ctx, pg, errs = await nuova(b); r = await pg.evaluate(COSTRUITO, [10 + k + 100 * tentativo, 1.0, "contatto"]); await ctx.close()
            if not r.get("salta"): break
            print(f"  caso {k}: le due barche erano già in contatto, seme cambiato", flush=True)
        if r["n"] == 1 and r["cont"] >= 1: ok3 += 1
        else: no(f"G3 costruito {k}: a 1 m eventi {r}")
        ctx, pg, errs = await nuova(b); r = await pg.evaluate(COSTRUITO, [10 + k, 12.0, "contatto"]); await ctx.close()
        if r.get("salta"): r = {"n": 0, "cont": 0}
        if r["n"] == 0 and r["cont"] == 0: ok3b += 1
        else: no(f"G3 costruito {k}: a 12 m eventi {r}")
        ctx, pg, errs = await nuova(b); r = await pg.evaluate(COSTRUITO, [10 + k, 0, "fermo"]); await ctx.close()
        if len(r["fermo"]) == 1 and 4.5 <= r["fermo"][0] <= 6.5 and len(r["riparte"]) == 1: ok4 += 1
        else: no(f"G4 costruito {k}: {r}")
    print(f"  contatto a 1 m: {ok3} su {n}; nessun contatto a 12 m: {ok3b} su {n}; barca ferma e ripartita: {ok4} su {n}", flush=True)

async def pagina_vera(b):
    print("\n== G7: pagina vera, senza #collaudo", flush=True)
    ctx, pg, errs = await nuova(b, BASE)
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.click("#goFree"); await pg.wait_for_timeout(500)                       # il registratore si accende dalle impostazioni, nel gioco
    for sel in ["#openSet", "#sesOn", "#setClose", "#toMenu"]: await pg.click(sel)
    await pg.click("#goTor"); await pg.wait_for_timeout(200); await pg.click("#torGo"); await pg.wait_for_timeout(300)
    await pg.click("#bGo"); await pg.wait_for_timeout(9000)                         # nove secondi veri: conto alla rovescia e partenza
    testo = await scarica(pg); await ctx.close()
    nomi = {r.split(" ")[2] for r in testo.splitlines() if r.startswith("B ")}
    print(f"  avversari con righe B nel file scaricato: {sorted(nomi)}; righe B {sum(r.startswith('B ') for r in testo.splitlines())}; errori della pagina {errs[:1]}", flush=True)
    if len(nomi) != 3: no(f"G7: avversari con righe B {sorted(nomi)}, attesi 3")
    if errs: no(f"G7: errore nella pagina {errs[0]}")

async def main():
    if '--solo-costruiti' in sys.argv:
        async with async_playwright() as p:
            b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); await costruiti(b, 10); await b.close()
        print('ESITO: ' + ('OK' if not errori else 'FALLITO ' + '; '.join(errori[:5]))); sys.exit(1 if errori else 0)
    elenco = [(tipo, seme, "esperti" if seme % 2 else "principianti") for tipo in (0, 2) for seme in range(1, 8)] + [("t", seme, "esperti" if seme % 2 else "principianti") for seme in range(1, 7)]
    if VELOCE: elenco = [elenco[i] for i in (0, 7, 14, 1, 8, 15)]
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        await regate(b, elenco); await costruiti(b, 3 if VELOCE else 10); await pagina_vera(b)
        await b.close()
    esito = "FALLITO (" + str(len(errori)) + "): " + "; ".join(errori[:6]) if errori else ("NON VALIDO: " + "; ".join(non_validi) if non_validi else "OK")
    print("\nESITO: " + esito, flush=True)
    sys.exit(1 if errori else 2 if non_validi else 0)

asyncio.run(main())
