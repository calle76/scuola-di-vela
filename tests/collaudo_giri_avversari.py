# Collaudo dei giri di penalità degli avversari (1.0.67, docs/PROPOSTA-GIRI-AVVERSARI.md, fetta 5 del 2a). Regata dei giri.
# Uso: .venv-collaudi/bin/python tests/collaudo_giri_avversari.py [regate=40] [cartella di una copia di riferimento (1.0.66), per il confronto al bit]
# Parti: G1 ogni giro dichiarato ha rotazione, virata e strambata (metro: dati registrati ogni 0,1 s) e il conto dei debiti torna con i contatti; G2 li fanno; G3 stesso verso;
#        G4 quanto costano; G5 non si piantano; G6 non scuffiano; G7 spirale; G8 la 21.2 vale anche per loro; G9 arrivo con giri mancanti; G10 altre regate identiche al bit;
#        G11 pagina senza #collaudo. Le soglie sono nella proposta, scritte prima di misurare.
import asyncio, pathlib, sys, os, statistics, json
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# una regata dei giri guidata dal pilota; ogni 0,1 s si registra per ogni avversario [t, prua, virate, strambate, sconta, debito, u, scuffiato, giri fatti, strada];
# a ogni passo si conta il debito preso (aumento di gDebt). L'analisi è in JS qui sotto e non usa le variabili interne dei giri se non per delimitare i segmenti (sconta).
REGATA = """async ([seme, liv]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = liv; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0], op = R.boats.slice(1), log = op.map(() => []), inc = op.map(() => []), tFin = op.map(() => null);
  let n = 0, prev = op.map(b => 0);
  while (R.t < 1500 && op.some(b => b.fin === null && !b.dnf)){
    if (me.fin === null && !me.dnf) sv.pilota(dt); else sv.ctl.tiller = 0;
    const sc0 = op.map(b => !!b.sconta);
    sv.run(dt, 1);
    op.forEach((b, i) => { const d = (b.gDebt || 0); if (d > prev[i]) inc[i].push([R.t, d - prev[i], sc0[i]]); prev[i] = d; if (b.fin !== null && tFin[i] === null) tFin[i] = R.t; });
    if (R.t >= 0 && n++ %% 6 === 0) op.forEach((b, i) => log[i].push([R.t, b.S.h, norm180(sv.windAt(b.S.x, b.S.y).twd - b.S.h), 0, b.sconta ? 1 : 0, b.gDebt || 0, b.S.u, b.S.capsized ? 1 : 0, b.gFatti || 0, strada(b)]));
  }
  const contatti = op.map(b => R.penList.filter(x => x.startsWith('La ' + b.name + ', contatto')).length);
  return { log, inc, tFin, contatti, fine: op.map(b => b.fin), gDebtFine: op.map(b => b.gDebt || 0), gFatti: op.map(b => b.gFatti || 0), pen: op.map(b => b.pen), nomi: op.map(b => b.name), t: R.t,
           pl: R.penList.filter(x => x.includes('giri di penalità non fatti') || x.includes('penalità scontata')) };
}""".replace("%%", "%")
GRIGLIA = """async ([seme, quale]) => { const sv = __sv; __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]); const R = sv.R, me = R.boats[0], ai = R.boats[1], out = [];
  const [wx, wy] = toWF(me.S.x, me.S.y); const pos = [[3, 0], [-3, 0], [0, 3], [0, -3], [2.5, 2.5], [-2.5, -2.5]], prue = [45, -45, 100, -100, 170];
  for (const mt of [45, -45]) for (const p of pos) for (const pr of prue){ me.S.h = norm360(env.twd + mt); me.S.u = 3; me.virando = false; const [x, y] = fromWF(wx + p[0], wy + p[1]); ai.S.x = x; ai.S.y = y; ai.S.h = norm360(env.twd + pr); ai.S.u = 3; ai.virando = false; ai.ocs = false; me.ocs = false;
    me.sconta = quale === 'entrambe'; ai.sconta = true; const r = chiCede(me, ai); ai.sconta = false; me.sconta = false; const r0 = chiCede(me, ai);
    out.push({ cede: r.cede === me ? 'me' : 'ai', regola: r.regola, senza: r0.cede === me ? 'me' : 'ai', regola0: r0.regola }); }
  return out; }"""
ARRIVO = """async ([seme]) => { const sv = __sv, dt = 1 / 60; __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]); const R = sv.R, me = R.boats[0], b = R.boats[1]; let dato = false, pen0 = null;
  while (R.t < 1500 && b.fin === null && !b.dnf){
    if (me.fin === null && !me.dnf) sv.pilota(dt); else sv.ctl.tiller = 0;
    if (!dato && b.leg === R.marks.length + 1){ const y = toWF(b.S.x, b.S.y)[1]; if (y < 0 && y > -22){ b.gDebt = 2; pen0 = b.pen; dato = true; } }
    sv.run(dt, 1); }
  return { dato, fin: b.fin !== null, dpen: b.pen - (pen0 === null ? 0 : pen0), voce: R.penList.filter(x => x.startsWith('La ' + b.name + ', giri di penalità non fatti (2): +30')).length, debito: b.gDebt || 0 }; }"""
# per la regata dei giri: istantanee ogni 5 s di tutte le barche, e l'istante del primo giro di un avversario (sconta)
SNAP = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
    const R = sv.R, me = R.boats[0]; const snap = []; let t1 = null, k = 0;
    while (R.t < 600 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1);
      if (t1 === null && R.boats.some(b => !b.me && b.sconta)) t1 = R.t;
      if (k++ %% 300 === 0) snap.push([R.t, R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000), b.leg])]); }
    out.push({ t1, snap });
  }
  return out;
}""".replace("%%", "%")
ALTRE = """async ([n, seme0, idx]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", idx === 3 ? 3 : j %% 3]);
    const R = sv.R, me = R.boats[0]; let deb = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); for (const b of R.boats) if (!b.me && b.gDebt) deb++; }
    out.push({ deb: deb, fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]) });
  }
  return out;
}""".replace("%%", "%")
# i campioni sono ogni 0,1 s e il giro comincia fino a 5 passi prima del campione in cui lo si vede: con 36°/s di virata massima misurata si perdono fino a 3-4°; tolleranza del metro 5° (aggiunta dopo aver visto 31 giri su 134 a 356,9-360°, dichiarato nel CHANGELOG; il motore conta 360° esatti)
TOLL = 5
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
def ndh(a, b):
    d = (b - a) % 360
    return d - 360 if d > 180 else d
def analizza(r):
    """Per ogni avversario: segmenti di 'sconta', giri dichiarati e misure fisiche dai campioni (ogni 0,1 s)."""
    seg = []
    for i, log in enumerate(r["log"]):
        k = 0
        while k < len(log):
            if not log[k][4]: k += 1; continue
            a = k
            while k < len(log) and log[k][4]: k += 1
            z = k  # primo campione dopo il segmento
            seg.append((i, a, z))
    out = []
    for (i, a, z) in seg:
        log = r["log"][i]; ev = [j for j in range(a + 1, z) if log[j][8] > log[j - 1][8]]
        # eventi di giro: il campione in cui i giri fatti aumentano; il primo giro parte dal campione a
        prima = a; giri = []; ok_giri = True
        for j in ev:
            rot = sum(ndh(log[m - 1][1], log[m][1]) for m in range(prima + 1, j + 1))
            vir = gyb = 0  # virate e strambate dai campioni: cambio di segno dell'angolo dal vento (a meno di 90° dal vento: virata, oltre: strambata), indipendente dal gioco
            for m in range(prima + 1, j + 1):
                x0, x1 = log[m - 1][2], log[m][2]
                if x0 * x1 < 0:
                    if abs(x0) + abs(x1) < 180: vir += 1
                    else: gyb += 1
            giri.append({"rot": rot, "vir": vir, "str": gyb, "t": log[j][0]})
            prima = j
        # piantata: campioni consecutivi con u < 0,3 vicino al vento (angolo morto, 50° dal vento: ipotesi del metro) per più di 10 s
        fermo = 0; maxf = 0
        for m in range(a, z):
            if log[m][6] < 0.3: fermo += 0.1; maxf = max(maxf, fermo)
            else: fermo = 0
        scuff = any(log[m][7] for m in range(a, min(z + 1, len(log))))
        # tempo perso per due giri di fila nello stesso segmento: durata - avanzamento / velocità prima
        persa = None
        if len(giri) >= 2 and log[a][9] is not None and log[min(z, len(log)) - 1][9] is not None:
            t0 = log[a][0]; pre = [m for m in range(0, a) if log[m][0] >= t0 - 30 and not log[m][4]]
            if len(pre) >= 100 and log[pre[0]][9] is not None and log[a][9] is not None:
                vp = (log[a][9] - log[pre[0]][9]) / (log[a][0] - log[pre[0]][0])
                j = ev[1]
                if vp > 0.1 and log[j][9] is not None: persa = (log[j][0] - t0) - (log[j][9] - log[a][9]) / vp
        out.append({"i": i, "giri": giri, "maxf": maxf, "scuff": scuff, "dur2": (giri[1]["t"] - log[a][0]) if len(giri) >= 2 else None, "persa": persa, "t0": log[a][0], "t1": log[min(z, len(log) - 1)][0]})
    return out
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        # ---- regate ----
        R = []; cache = os.environ.get("GIRI_CACHE"); gia = json.load(open(cache)) if cache and os.path.exists(cache) else {}
        for k in range(1, n + 1):
            if str(k) not in gia:
                gia[str(k)] = await pg.evaluate(REGATA, [k, "principianti" if k % 2 else "esperti"])
                if cache: json.dump(gia, open(cache, "w"))
            R.append(gia[str(k)])
        print("     %d regate fatte (semi 1-%d, avversari principianti e esperti alternati)" % (n, n), flush=True)
        inc = sum(sum(e[1] for e in r["inc"][i]) for r in R for i in range(3)); con = sum(sum(r["contatti"]) for r in R)
        chk("G0 il metro ha misurato davvero: i debiti presi dagli avversari (%d giri = %d contatti) coincidono con i contatti con colpa degli avversari nell'elenco (%d)" % (inc, inc // 2, con), inc == 2 * con and con >= 10, "regate con almeno un debito: %d su %d" % (sum(1 for r in R if any(r["inc"][i] for i in range(3))), n))
        A = [(k, s) for k, r in enumerate(R) for s in analizza(r)]
        giri = [(k, s, g) for k, s in A for g in s["giri"]]
        ng = len(giri)
        ok1 = [g for k, s, g in giri if abs(g["rot"]) >= 360 - TOLL and g["vir"] >= 1 and g["str"] >= 1]
        mal = [g for k, s, g in giri if g not in ok1]
        chk("G1 ogni giro dichiarato ha almeno 360° (tolleranza di campionamento 5°) di rotazione, una virata e una strambata (dai campioni a 0,1 s): %d su %d" % (len(ok1), ng), ng >= 20 and len(ok1) == ng, "segmenti di giri: %d; non validi: rotazione < 360 in %d (minimo %.1f), senza virata %d, senza strambata %d" % (len(A), sum(1 for g in mal if abs(g["rot"]) < 360), min([abs(g["rot"]) for g in mal] or [0]), sum(1 for g in mal if g["vir"] < 1), sum(1 for g in mal if g["str"] < 1)))
        # G2: debiti con almeno 90 s di regata davanti
        casi = 0; fatti = 0; falliti = []
        for k, r in enumerate(R):
            for i in range(3):
                if r["tFin"][i] is None: continue
                req = sum(e[1] for e in r["inc"][i] if e[0] <= r["tFin"][i] - 90)
                if req > 0:
                    casi += 1
                    if r["gFatti"][i] >= req: fatti += 1
                    else: falliti.append((k + 1, r["nomi"][i], req, r["gFatti"][i]))
        chk("G2 i debiti con almeno 90 s di regata davanti sono estinti: %d casi, %d estinti (%.0f%%; soglia 80%%)" % (casi, fatti, 100 * fatti / casi if casi else 0), casi >= 15 and fatti >= 0.8 * casi, "non estinti (regata, barca, dovuti, fatti): %s" % falliti[:8])
        # G3: stesso verso entro un periodo di debito (giri di un segmento + segmenti adiacenti dello stesso debito)
        verso_ok = True; verso_n = 0
        for k, r in enumerate(R):
            for i in range(3):
                gs = [g for kk, s, g in giri if kk == k and s["i"] == i]
                if len(gs) >= 2:
                    verso_n += 1
                    # giri consecutivi senza che il debito si sia azzerato in mezzo: si confrontano solo coppie di giri a meno di 40 s (stesso debito)
                    for a, c in zip(gs, gs[1:]):
                        if c["t"] - a["t"] < 40 and (a["rot"] > 0) != (c["rot"] > 0): verso_ok = False
        chk("G3 i giri successivi dello stesso debito vanno nello stesso verso (%d avversari con almeno due giri)" % verso_n, verso_ok and verso_n >= 8)
        d2 = [s["dur2"] for k, s in A if s["dur2"] is not None]; persa = [s["persa"] for k, s in A if s["persa"] is not None]
        med = statistics.median(d2) if d2 else None
        chk("G4 durata dei due giri di fila (mediana, soglia 12-30 s; il giocatore 17,5 s): %s su %d casi, minimo-massimo %s" % ("%.1f s" % med if med else "—", len(d2), "%.1f-%.1f" % (min(d2), max(d2)) if d2 else "—"), bool(d2) and 12 <= med <= 30 and len(d2) >= 15)
        print("     G4b (solo riportato) secondi persi per i due giri rispetto all'avanzamento di prima: %s su %d casi (i +15 s di prima)" % ("mediana %.1f s, %.1f-%.1f" % (statistics.median(persa), min(persa), max(persa)) if persa else "—", len(persa)), flush=True)
        nseg = len(A); pianta = sum(1 for k, s in A if s["maxf"] > 10)
        chk("G5 segmenti con un avversario fermo (u < 0,3) per più di 10 s: %d su %d (soglia 5%%)" % (pianta, nseg), nseg >= 20 and pianta <= 0.05 * nseg)
        scuff = sum(1 for k, s in A if s["scuff"])
        chk("G6 segmenti con scuffia: %d su %d (soglia 5%%)" % (scuff, nseg), nseg >= 20 and scuff <= 0.05 * nseg)
        durante = sum(1 for r in R for i in range(3) for e in r["inc"][i] if e[2])
        extra = sum(e[1] for r in R for i in range(3) for e in r["inc"][i] if e[2])
        chk("G7 giri durante i quali l'avversario prende un altro debito: %d segmenti su %d (soglia 15%%), giri di debito in più %.2f a regata (soglia 0,3)" % (durante, nseg, extra / n), nseg >= 20 and durante <= 0.15 * nseg and extra / n < 0.3)
        # ---- G8 ----
        G8 = [await pg.evaluate(GRIGLIA, [800 + k, "solo"]) for k in range(2)]
        t8 = sum(len(g) for g in G8); ok8 = sum(1 for g in G8 for c in g if c["cede"] == "ai" and c["regola"] == 21.2)
        camb = sum(1 for g in G8 for c in g if c["senza"] == "me")
        chk("G8 l'avversario che sconta cede con la 21.2 al giocatore che non sconta: %d su %d posizioni (in %d il giocatore avrebbe ceduto senza la regola)" % (ok8, t8, camb), ok8 == t8 and camb >= 10)
        G8b = [await pg.evaluate(GRIGLIA, [820 + k, "entrambe"]) for k in range(2)]
        chk("G8b scontano tutti e due: valgono le regole 10-13 (%d posizioni)" % sum(len(g) for g in G8b), all(10 <= c["regola"] <= 13 for g in G8b for c in g))
        # ---- G9 ----
        G9 = [await pg.evaluate(ARRIVO, [900 + k]) for k in range(10)]
        val = [g for g in G9 if g["dato"] and g["fin"]]
        chk("G9 avversario che arriva con due giri da fare: +30 s e voce nell'elenco in %d casi su %d possibili (10 prove)" % (sum(1 for g in val if g["dpen"] == 30 and g["voce"] == 1 and g["debito"] == 0), len(val)), len(val) >= 7 and all(g["dpen"] == 30 and g["voce"] == 1 for g in val))
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- G10 ----
        ctx, pg, errs = await pagina(b, ROOT); nuovo = await pg.evaluate(ALTRE, [20, 100, 0]); await ctx.close()
        if rif:
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); vecchio = await pg.evaluate(ALTRE, [20, 100, 0]); await ctx.close()
            chk("G10a regate dell'1a e dell'1b: arrivi, penalità e posizioni finali identici al bit alla 1.0.66 su 20 regate", nuovo == vecchio and len(nuovo) == 20)
            ctx, pg, errs = await pagina(b, ROOT); sn = await pg.evaluate(SNAP, [20, 200]); await ctx.close()
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); sv_ = await pg.evaluate(SNAP, [20, 200]); await ctx.close()
            conf = 0; uguali = True; divergono = 0
            for x, y in zip(sn, sv_):
                t1 = x["t1"] if x["t1"] is not None else 1e9
                for (ta, sa), (tb, sb) in zip(x["snap"], y["snap"]):
                    if ta < t1 - 1: conf += 1; uguali = uguali and sa == sb
                if any(sa != sb for (ta, sa), (tb, sb) in zip(x["snap"], y["snap"])): divergono += 1
            chk("G10b regata dei giri: fino al primo giro di un avversario le barche sono identiche al bit alla 1.0.66 (%d istantanee in 20 regate, ogni 5 s)" % conf, conf >= 100 and uguali, "regate che dopo il primo giro divergono: %d su 20 (il metro vede la differenza)" % divergono)
        else: print("     G10 saltato: manca la cartella di riferimento")
        # ---- G11 ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1200)
        h = await pg.evaluate("""() => { if (!R || !R.giri) return null; const o = R.boats[1]; R.t = 1; for (const x of R.boats) if (!x.me){ x.leg = 1; x.ocs = false; } o.gDebt = 2; const dt = 1 / 60;
          for (let k = 0; k < 60 * 120; k++) simulate(dt, curStep()); return { fatti: o.gFatti || 0, debito: o.gDebt, pl: R.penList.slice() }; }""")
        chk("G11 pagina senza #collaudo: la regata si apre, un avversario con due giri da fare ne fa almeno uno in 120 s simulati", bool(h) and h["fatti"] >= 1, str(h)[:120] if h else "regata non aperta")
        chk("G11b nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
