# La marcatura nell'ultima regata del torneo (1.3.50, voce 74, docs/PROPOSTA-MARCATURA.md). Soglie scritte nella proposta prima del codice (23 nov 2026).
#   K1 chi marca è giusto: ricalcolato QUI col punteggio dell'appendice A riscritto in Python (non preso dal gioco) dai risultati delle regate prima dell'ultima;
#      0 scelte diverse; con la marcatura spenta nessuno marca; stampa quanti tornei con e senza marcatore (almeno 20 e 20, su corti e lunghi insieme)
#   K2 il resto non cambia: ultima regata identica al bit con e senza marcatura quando nessuno marca; regate prima dell'ultima identiche al bit (5 tornei corti interi
#      corsi due volte). Solo Chromium: in Firefox la stessa versione contro se stessa non è identica al bit (collaudo_storico_rivali R3), lì solo riportato
#   K3 marca davvero: le tue virate (dalle prue campionate qui, non dallo stato del gioco) fatte mentre lui è davanti, a meno di 42 m, tutti e due sul primo lato (bolina),
#      con lui sulle tue stesse mure prima della virata: seguite da una sua entro 10 s in >= 50% e almeno il doppio che senza marcatura. Contano le regate con almeno
#      60 s di quelle condizioni: se sono meno di 20, «non misurato»
#   K4 0 contatti con colpa del marcatore mentre marca (dichiarato prima di misurare, più severo della proposta: anche nei 5 s dopo); contatti in tutto nell'ultima regata
#      con la marcatura al più +10% rispetto a senza
#   K5 il marcatore ti arriva davanti nell'ultima regata almeno tante volte quante senza marcatura
#   K6 il tuo tempo nell'ultima regata peggiora al più del 5% in mediana; non arrivati in tutto (tutte le barche) al più +1
#   K7 riga nel testo della regata con nome e barca giusti in tutti i casi con marcatore, 0 nei casi senza; Coach a -100 s (+-1 s; un ritardo dovuto a un commento
#      forzato nei 30 s prima si conta a parte); col Coach spento 0 frasi ma la riga resta
#   K8 testo della regata e riquadro del Coach a 1360x650 senza eccesso col nome più lungo
#      (23 nov, primo giro: il controllo in più «testo intero senza scorrere» falliva anche senza marcatura, il testo del torneo scorreva già: ora solo riportato)
#   K9 come un giocatore: pagina senza #collaudo, torneo con l'ultima regata da marcare (classifica costruita): riga e frase compaiono, 0 errori
# Uso (uno per volta, col freno):
#   python tests/collaudo_marcatura.py banco           # 40 tornei corti, risultati in $TMPDIR/marcatura-corti-<browser>.json
#   python tests/collaudo_marcatura.py banco --lungo   # 40 tornei lunghi
#   python tests/collaudo_marcatura.py somma           # K1, K3-K7 su corti e lunghi insieme
#   python tests/collaudo_marcatura.py altri           # K2, K7 Coach spento, K8, K9 (questa sola parte è nella suite: il banco dura 36 min i corti, di più i lunghi)
# BROWSER=firefox per Firefox.
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
LUNGO = "--lungo" in sys.argv
PARTE = sys.argv[1] if len(sys.argv) > 1 else "banco"
OUT = pathlib.Path(os.environ.get("MARCA_OUT", os.environ.get("TMPDIR", "/tmp")))
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
COLORI = ["rossa", "verde", "blu", "viola", "grigia"]
D_MARCA = 42.0
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)

# ---- punteggio dell'appendice A, riscritto qui (non preso dal gioco) ----
def punti(r):
    dnf = len(r) + 1; pen = round(2 * dnf) / 10
    return [dnf if b["fin"] is None else min(dnf, 1 + sum(1 for o in r if o["fin"] is not None and o["fin"] < b["fin"]) + (b.get("pp") or 0) * pen) for b in r]
def serie(ris, n_scarto=4):
    P = [punti(r) for r in ris]; out = []
    for i in range(len(ris[0])):
        p = [x[i] for x in P]; sc = p.index(max(p)) if len(p) >= n_scarto else -1
        out.append({"i": i, "p": p, "sc": sc, "tot": sum(v for k, v in enumerate(p) if k != sc)})
    def chiave(x):
        tenuti = sorted(v for k, v in enumerate(x["p"]) if k != x["sc"])
        return (round(x["tot"], 9), tenuti, list(reversed(x["p"])))
    return sorted(out, key=chiave)   # sorted è stabile: a parità piena resta l'ordine delle barche, come il sort del gioco
def marcatore(ris):
    """indice della barca (1..n) che deve marcare, 0 se nessuna: il rivale per cui arrivare subito davanti o subito dietro al giocatore nell'ultima regata cambia l'ordine fra loro"""
    cl = serie(ris); ordine = [x["i"] for x in cl]; tot = {x["i"]: x["tot"] for x in cl}; n = len(ris[0])
    def davanti(i, seq):
        r = [None] * n
        for k, x in enumerate(seq): r[x] = {"fin": k + 1, "pp": 0}
        s = [x["i"] for x in serie(ris + [r])]; return s.index(i) < s.index(0)
    m, v = 0, float("inf")
    for i in range(1, n):
        altri = [x for x in ordine if x not in (0, i)]
        if davanti(i, [i, 0] + altri) and not davanti(i, [0, i] + altri):
            d = abs(tot[i] - tot[0])
            if d < v: m, v = i, d
    return m

# ---- una regata del torneo, aperta e corsa in un solo evaluate; campiona ogni 0,25 s la barca osservata (wb) e il giocatore ----
CORRI = """async ([coach, wb]) => { const sv = __sv, dt = 1 / 60; sv.opt.coachReg = coach; document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], B = wb ? R.boats[wb] : null, lato = b => Math.sign(((windAt(b.S.x, b.S.y).twd - b.S.h + 540) % 360) - 180), twa = b => Math.abs(((windAt(b.S.x, b.S.y).twd - b.S.h + 540) % 360) - 180);
  const mk = R.marks[0], camp = [], cont = [], prec = {}; let k = 0, ultMarca = -1e9;
  while (me.fin === null && !me.dnf && R.t < 2400){ sv.pilota(dt); sv.run(dt, 1); k++;
    if (B && B.marcaOn) ultMarca = R.t;
    for (const key in R.contacts) if (prec[key] !== R.contacts[key]){ prec[key] = R.contacts[key]; const c = R.contColpa && R.contColpa[key];
      cont.push({ t: +R.t.toFixed(2), key, g: c && c.g ? R.boats.indexOf(c.g) : -1, marca: !!B && R.t - ultMarca <= 5 }); }
    if (B && R.t >= 0 && k % 15 === 0) camp.push([+R.t.toFixed(2), me.leg, lato(me), Math.round(twa(me)), B.leg, lato(B), Math.round(twa(B)), +Math.hypot(me.S.x - B.S.x, me.S.y - B.S.y).toFixed(1),
      Math.hypot(B.S.x - mk.x, B.S.y - mk.y) < Math.hypot(me.S.x - mk.x, me.S.y - mk.y) ? 1 : 0, B.marcaOn ? 1 : 0, B.fin !== null ? 1 : 0]); }
  const firma = R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, !!b.dsq, b.me ? R.need || 0 : 0, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(',')).join('|');
  const log = R.cr ? R.cr.log.map(c => [c.t, c.testo]) : [], marca = R.marca || 0, brief = R.brief;
  document.getElementById("rTor").click(); return { marca, brief, log, camp, cont, firma, ris: JSON.parse(JSON.stringify(sv.tor.ris)), nomi: sv.tor.av.map(a => a.nome) }; }"""
async def pagina(b, url=BASE + "#collaudo", seme=True):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    if seme: await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url); await pg.wait_for_timeout(200); return ctx, pg, errs
async def apri(pg, seme, marca=True):
    await pg.evaluate("([s, l, m]) => { __sv.fast(0); __sv.lungo = l; __sv.marca(m); __seed(s); __sv.opt.countdown = 180; __sv.torApri(); }", [seme, LUNGO, marca])
async def riprendi(pg, T, seme, marca):
    """pagina nuova, torneo salvato rimesso com'era prima dell'ultima regata, stesso seme"""
    await pg.evaluate("([T, s, l, m]) => { __sv.fast(0); __sv.lungo = l; __sv.marca(m); __sv.opt.countdown = 180; progress.torneo = T; __sv.torApri(); __seed(s); }", [T, seme, LUNGO, marca])

def nome_barca(nomi, m):
    return f"{nomi[m - 1]} (barca {COLORI[m - 1]})" if nomi[m - 1] else None

async def banco():
    N = int(os.environ.get("MARCA_N", 40)); semi = range(3201, 3201 + N) if LUNGO else range(3101, 3101 + N)   # MARCA_N: solo per le prove veloci
    righe = []
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        for sd in semi:
            ctx, pg, errs = await pagina(b); await apri(pg, sd)
            n = await pg.evaluate("() => (__sv.tor || torBozza).n || 4")
            for k in range(n - 1): r = await pg.evaluate(CORRI, [True, 0])
            T = await pg.evaluate("() => JSON.parse(JSON.stringify(__sv.tor))"); await ctx.close()
            atteso = marcatore(T["ris"]); riga = {"seme": sd, "n": n, "atteso": atteso, "nomi": [a.get("nome") for a in T["av"]], "errori": list(errs)}
            for var in (True, False):
                ctx, pg, errs = await pagina(b); await riprendi(pg, T, sd + 50000, var)
                r = await pg.evaluate(CORRI, [True, atteso]); await ctx.close()
                r["errori"] = list(errs); riga["con" if var else "senza"] = r
            righe.append(riga)
            print(f"seme {sd}: marcatore atteso {atteso}, del gioco {riga['con']['marca']} (spenta {riga['senza']['marca']}); campioni {len(riga['con']['camp'])}; errori {riga['errori'] + riga['con']['errori'] + riga['senza']['errori']}", flush=True)
        await b.close()
    f = OUT / f"marcatura-{'lunghi' if LUNGO else 'corti'}-{BR}.json"; f.write_text(json.dumps(righe)); print("scritto", f)

def virate(camp):
    """K3 sulle prue campionate: (virate da contare, seguite entro 10 s, secondi nelle condizioni)"""
    cond = lambda c: c[0] >= 0 and c[1] == 1 and c[4] == 1 and c[7] <= D_MARCA and c[8] == 1 and c[10] == 0
    sec = 0.25 * sum(1 for c in camp if cond(c)); n = seg = 0
    for a, c in zip(camp, camp[1:]):
        if a[2] != c[2] and a[2] and c[2] and cond(a) and a[5] == a[2]:   # hai virato, lui era sulle tue mure di prima
            n += 1
            if any(x[5] == c[2] for x in camp if c[0] <= x[0] <= a[0] + 10): seg += 1
    return n, seg, sec

def somma():
    righe = []
    for fam in ("corti", "lunghi"):
        f = OUT / f"marcatura-{fam}-{BR}.json"
        if f.exists(): righe += [dict(x, fam=fam) for x in json.loads(f.read_text())]
        else: print("MANCA", f)
    if not righe: chk(False, "nessun risultato del banco"); return
    # K1
    diverse = [(x["fam"], x["seme"], x["atteso"], x["con"]["marca"], x["senza"]["marca"]) for x in righe if x["con"]["marca"] != x["atteso"] or x["senza"]["marca"] != 0]
    con = [x for x in righe if x["atteso"]]; senza = [x for x in righe if not x["atteso"]]
    err = [(x["fam"], x["seme"], e) for x in righe for e in x["errori"] + x["con"]["errori"] + x["senza"]["errori"]]
    chk(not diverse and len(con) >= 20 and len(senza) >= 20 and not err, f"K1 scelte diverse {len(diverse)} {diverse[:3]} su {len(righe)} tornei: con marcatore {len(con)} (corti {sum(x['fam'] == 'corti' for x in con)}), senza {len(senza)}; errori {err[:1]}")
    # K3
    def k3(v):
        tot_n = tot_s = reg = 0
        for x in con:
            n, s, sec = virate(x[v]["camp"])
            if sec >= 60: reg += 1; tot_n += n; tot_s += s
        return tot_n, tot_s, reg
    n1, s1, g1 = k3("con"); n0, s0, g0 = k3("senza")
    q1 = s1 / n1 if n1 else 0; q0 = s0 / n0 if n0 else 0
    msg = f"K3 virate seguite entro 10 s: con marcatura {s1}/{n1} = {q1:.0%} ({g1} regate con >= 60 s nelle condizioni), senza {s0}/{n0} = {q0:.0%} ({g0} regate)"
    if g1 < 20: print("NON MISURATO " + msg, flush=True); bad.append("K3 non misurato")
    else: chk(q1 >= 0.5 and q1 >= 2 * q0, msg)
    # K4
    colpe = [(x["fam"], x["seme"], c["t"]) for x in con for c in x["con"]["cont"] if c["g"] == x["atteso"] and c["marca"]]
    ct1 = sum(len(x["con"]["cont"]) for x in con); ct0 = sum(len(x["senza"]["cont"]) for x in con)
    uguali = [c for c in colpe if any(x["seme"] == c[1] and x["fam"] == c[0] and any(d["t"] == c[2] and d["g"] == x["atteso"] for d in x["senza"]["cont"]) for x in con)]   # riportati, non tolti dal conto
    chk(not colpe and ct1 <= ct0 * 1.1, f"K4 contatti con colpa del marcatore mentre marca (o nei 5 s dopo): {len(colpe)} {colpe[:3]}, di cui identici anche senza marcatura {len(uguali)}; contatti in tutto nell'ultima regata (tornei con marcatore) con {ct1}, senza {ct0}")
    # K5, K6 (arrivi dall'ultima riga di tor.ris)
    def dav(x, v):
        r = x[v]["ris"][-1]; m, me = r[x["atteso"]]["fin"], r[0]["fin"]
        return m is not None and (me is None or m < me)
    d1 = sum(dav(x, "con") for x in con); d0 = sum(dav(x, "senza") for x in con)
    chk(d1 >= d0, f"K5 il marcatore ti arriva davanti: con marcatura {d1} su {len(con)}, senza {d0}")
    rap = [x["con"]["ris"][-1][0]["fin"] / x["senza"]["ris"][-1][0]["fin"] for x in con if x["con"]["ris"][-1][0]["fin"] and x["senza"]["ris"][-1][0]["fin"]]
    nar = lambda v: sum(1 for x in righe for b in x[v]["ris"][-1] if b["fin"] is None)
    med = statistics.median(rap) if rap else None
    chk(med is not None and med <= 1.05 and nar("con") <= nar("senza") + 1, f"K6 tuo tempo nell'ultima regata, mediana con/senza {med:.3f} su {len(rap)} regate (min {min(rap):.3f}, max {max(rap):.3f}); non arrivati con {nar('con')}, senza {nar('senza')}" if rap else "K6 nessun tempo")
    # K7 (riga e Coach acceso)
    sbagl = []; fuori = []; ritardi = 0; frasi = 0
    for x in righe:
        m = x["atteso"]; br = x["con"]["brief"]; nb = nome_barca(x["nomi"], m) if m else None
        if m and not (("Ultima regata: " + nb) in br and "ti marca" in br): sbagl.append((x["fam"], x["seme"], "riga"))
        if not m and "ti marca" in br: sbagl.append((x["fam"], x["seme"], "riga in più"))
        if "ti marca" in x["senza"]["brief"]: sbagl.append((x["fam"], x["seme"], "riga con la marcatura spenta"))
        L = [c for c in x["con"]["log"] if "ti marca in quest'ultima regata" in c[1]]
        att = f"{x['nomi'][m - 1]}, barca {COLORI[m - 1]}, ti marca in quest'ultima regata" if m else None
        if m and (len(L) != 1 or not L[0][1].startswith(att)): sbagl.append((x["fam"], x["seme"], "Coach", [c[1][:40] for c in L]))
        if not m and L: sbagl.append((x["fam"], x["seme"], "Coach in più"))
        for t, _ in L:
            frasi += 1
            if not -101 <= t <= -99:
                if any(t - 31 < c[0] < t and "ti marca" not in c[1] for c in x["con"]["log"]): ritardi += 1
                else: fuori.append((x["fam"], x["seme"], t))
    chk(not sbagl and not fuori and frasi == len(con), f"K7 righe e frasi sbagliate {len(sbagl)} {sbagl[:3]}; frasi del Coach {frasi} su {len(con)} tornei con marcatore, fuori tempo {fuori[:3]}, ritardate da un commento nei 30 s prima (a parte) {ritardi}")

COSTRUISCI = """(T) => { const n = T.n || 4, nb = T.av.length + 1; T.ris = [];
  for (let k = 0; k < n - 1; k++){ const seq = k % 2 ? [1, 0] : [0, 1]; for (let i = 2; i < nb; i++) seq.push(i); const r = []; seq.forEach((x, j) => { r[x] = { fin: 300 + 10 * j, pp: 0 }; }); T.ris.push(r); }
  return T; }"""
async def altri():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        # K2 regate prima dell'ultima identiche con e senza marcatura (corti)
        uguali = tot = 0
        for sd in range(3301, 3306):
            f = []
            for var in (True, False):
                ctx, pg, errs = await pagina(b); await apri(pg, sd, var); fr = []
                for k in range(3): r = await pg.evaluate(CORRI, [True, 0]); fr.append(r["firma"])
                f.append(fr); await ctx.close()
            for x, y in zip(*f): tot += 1; uguali += x == y
        # K2 ultima regata identica quando nessuno marca: dal banco
        uguali2 = tot2 = 0
        for fam in ("corti", "lunghi"):
            fl = OUT / f"marcatura-{fam}-{BR}.json"
            if fl.exists():
                for x in json.loads(fl.read_text()):
                    if not x["atteso"]: tot2 += 1; uguali2 += x["con"]["firma"] == x["senza"]["firma"]
        msg = f"K2 regate prima dell'ultima identiche con e senza marcatura {uguali} su {tot}; ultime regate senza marcatore identiche {uguali2} su {tot2}"
        if BR == "chromium": chk(tot == 15 and uguali == 15 and uguali2 == tot2 and (tot2 >= 20 or tot2 == 0), msg + ("" if tot2 else " (banco non lanciato in questa cartella: la seconda metà si controlla dopo «banco»)"))
        else: print(f"RIPORTATO ({BR}) " + msg, flush=True)
        # K7 Coach spento: 5 ultime regate costruite con il marcatore
        off = 0; righe_ok = 0
        for sd in range(3401, 3406):
            ctx, pg, errs = await pagina(b); await apri(pg, sd)
            await pg.evaluate("() => { const T = torBozza || __sv.tor; (" + COSTRUISCI + ")(T); progress.torneo = T; __sv.torApri(); }")
            r = await pg.evaluate("""async () => { const sv = __sv; sv.opt.coachReg = false; document.getElementById("torGo").click(); const R = sv.R;
              while (R.t < -60) sv.run(1 / 60, 1); return { marca: R.marca, brief: R.brief, log: R.cr ? R.cr.log.length : 0 }; }""")
            off += r["log"]; righe_ok += r["marca"] == 1 and "ti marca" in r["brief"]; await ctx.close()
        chk(off == 0 and righe_ok == 5, f"K7 Coach spento: {off} frasi in 5 regate; riga nel testo presente in {righe_ok} su 5")
        # K8 nome più lungo: testo della regata e riquadro del Coach
        ctx, pg, errs = await pagina(b); await apri(pg, 3501)
        r8 = await pg.evaluate("""async () => { const sv = __sv, T = torBozza || sv.tor; (""" + COSTRUISCI + """)(T);
          const lungo = [...RIVALI_ZONALE, ...RIVALI_NAZIONALE].map(x => x[0]).sort((a, b) => b.length - a.length)[0]; T.av[0].nome = lungo; progress.torneo = T; sv.torApri();
          sv.skipBrief = false; sv.opt.coachReg = true; document.getElementById("torGo").click(); const R = sv.R;
          const ov = document.getElementById("briefOv"), q = ov.getBoundingClientRect(), bt = document.getElementById("bText"), go = document.getElementById("bGo").getBoundingClientRect();
          const ecc1 = Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0), dentro1 = q.left >= 0 && q.top >= 0 && q.right <= innerWidth && q.bottom <= innerHeight;
          const testoTutto = ov.scrollHeight <= ov.clientHeight + 1 && go.bottom <= innerHeight && go.bottom > 0;
          sv.hideBrief(); while (R.t < -99) sv.run(1 / 60, 1); sv.draw(0.016);
          const c = R.crRect, testo = R.cr && R.cr.cur ? R.cr.cur.testo : "", ecc2 = Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0);
          return { lungo, brief: R.brief.includes(lungo), q: [q.left, q.top, q.right, q.bottom], dentro1, ecc1, testoTutto, c, W, H, testo, ecc2 }; }""")
        c = r8["c"]; dentro2 = bool(c) and c[0] >= 0 and c[1] >= 0 and c[0] + c[2] <= r8["W"] and c[1] + c[3] <= r8["H"]
        # 23 nov, dopo il primo giro: «testo intero senza scorrere» non era nella proposta e falliva anche senza marcatura (il testo del torneo era già 1159 px in 598, overflow auto): solo riportato
        chk(r8["brief"] and r8["dentro1"] and r8["ecc1"] == 0 and dentro2 and r8["ecc2"] == 0 and r8["lungo"] in r8["testo"] and not errs,
            f"K8 nome più lungo «{r8['lungo']}»: riquadro del testo {[round(v) for v in r8['q']]} dentro {r8['dentro1']}, eccesso {r8['ecc1']}; Coach {c} dentro {dentro2}, frase {'sì' if r8['lungo'] in r8['testo'] else 'NO'}; errori {errs[:1]}")
        print(f"RIPORTATO K8 il testo della regata si legge {'senza' if r8['testoTutto'] else 'scorrendo (come già prima della marcatura)'}", flush=True)
        await ctx.close()
        # K9 come un giocatore
        ctx, pg, errs = await pagina(b, url=BASE, seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        nome = await pg.evaluate("() => { const T = torBozza; (" + COSTRUISCI + ")(T); progress.torneo = T; torApri(); return T.av[0].nome; }")
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        testo = await pg.inner_text("#bText") if await pg.is_visible("#bText") else ""
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        for _ in range(120):
            if await pg.evaluate("() => typeof R !== 'undefined' && !!R && R.t >= -95"): break
            await pg.wait_for_timeout(1000)
        r9 = await pg.evaluate("() => ({ log: R.cr ? R.cr.log.map(c => c.testo) : [], t: R.t })")
        frase = any(f"{nome}, barca rossa, ti marca" in x for x in r9["log"])
        chk(f"Ultima regata: {nome} (barca rossa)" in testo and frase and not errs, f"K9 pagina da giocatore (t = {r9['t']:.0f} s): riga nel testo {'sì' if nome in testo else 'NO'}, frase del Coach {'sì' if frase else 'NO'}; errori {errs[:1]}")
        await ctx.close(); await b.close()

if PARTE == "banco": asyncio.run(banco()); raise SystemExit(0)
if PARTE == "somma": somma()
if PARTE == "altri": asyncio.run(altri())
print("\ncasi sbagliati:", "nessuno" if not bad else bad)
raise SystemExit(1 if bad or n_casi == 0 else 0)
