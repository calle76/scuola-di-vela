# Il coach nella moviola (1.3.3, docs/PROPOSTA-COACH.md, criteri K1-K9 scritti prima; la misura del clou cambiata prima delle soglie, §Esito).
# Regate del torneo col pilota (__sv.pilota, la guida degli avversari sul giocatore) fino all'arrivo, poi «Rotta ottimale», come collaudo_rotta_assoluta.py.
#   K1 niente cambia sotto: arrivi, penalità e posizioni identici al codice di riferimento (RIF, git archive) nelle stesse regate
#   K2 spazio: barra della moviola col coach dentro la finestra a 1360x650 e 0 px di eccesso, anche nel caso peggiore costruito (tre frasi più lunghe, legenda con V)
#   K3 ogni frase detta ha un numero; al più 3 frasi; i numeri del clou coincidono col ricalcolo del collaudo (K4)
#   K4 il clou: il collaudo ricalcola da solo (in Python, dai dati esportati) la finestra di 60 s in cui i metri di percorso mancanti in più crescono di più,
#      fuori dai secondi affollati: stessa finestra e stessi metri (±1 m) del coach, in tutte le regate in cui c'è
#   K5 coperto: (a) tratti costruiti a vento, angolo e quota fissi: secondi persi entro ±25% della stima fatta qui con la tabella polare letta da js/rotta-dati.js;
#      (b) nessun tratto coperto senza una barca entro 10 lunghezze, nelle regate vere
#   K6 cliccando una frase la moviola va a 5 s prima del suo momento, entro 1 s
#   K7 bene quando va bene: con la tua traccia sostituita da quella della rotta ottimale e nessuna barca vicina, nessuna frase di perdita, c'è «quasi perfetta» (costruito)
#   K8 calcolo delle frasi sotto 200 ms; pagina senza #collaudo: riquadro del coach presente e nascosto, 0 errori
#   K9 le frasi identiche prima e dopo la migliore in assoluto (V)
# Uso: python tests/collaudo_coach.py [--regate N] [--rif v1.3.2]   (BROWSER=firefox per Firefox)
import asyncio, json, math, os, pathlib, re, subprocess, sys, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
NREG = int(arg("--regate", "20")); RIF = arg("--rif", "v1.3.2")
src = (ROOT / "tests" / "collaudo_rotta_assoluta.py").read_text().split("async def main")[0]
A = {"__file__": str(ROOT / "tests" / "collaudo_rotta_assoluta.py")}; exec(src, A); CORSA = A["CORSA"]
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    if not ok: fail.append(testo); print("FALLITO " + testo, flush=True)

ESITO = """() => { const R = __sv.R; return R.boats.map(b => [b.fin === null ? null : Math.round(b.fin * 100) / 100, b.pen || 0, b.pp || 0, b.dsq ? 1 : 0, b.leg]); }"""
DATI = """() => { const r = rot.res, me = R.boats[0], o = rot.barche[0], fine = me.fin !== null ? me.fin : riv.all[riv.all.length - 1].t;
  const tu = riv.all.filter(f => f.t >= o.taglio.t && f.t <= fine);
  const t0 = performance.now(); const F = coaFrasi(r.ott, r.sp); const ms = performance.now() - t0;
  return { coach: r.coach, ms, uguali: JSON.stringify(F) === JSON.stringify(r.coach), punti: r.ott.punti.map(q => [q.t, q.x, q.y]), lati: r.ott.lati, giri: o.giri.map(g => g.t), leg: o.taglio.leg,
    marks: R.marks.map(m => [m.x, m.y]), fin: [(R.pin.x + R.cb.x) / 2, (R.pin.y + R.cb.y) / 2], aff: COA_AFF, cop: COA_COP, fin60: COA_FIN, min: COA_MIN,
    tu: tu.map(f => [f.t, f.b[0][0], f.b[0][1], f.b[0][4], f.c ? f.c[0] : 0, Math.min(1e9, ...f.b.slice(1).map(b => Math.hypot(b[0] - f.b[0][0], b[1] - f.b[0][1])))]),
    tratti: coaCoperto(tu).map(x => [x.t0, x.t1]) }; }"""

def interp(A, T):   # A: [[t, x, y], ...] ordinati
    lo, hi = 0, len(A) - 1
    if not A or T < A[0][0] or T > A[hi][0]: return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if A[m][0] <= T: lo = m
        else: hi = m
    a, b = A[lo], A[hi]; f = (T - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0
    return (a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f)

def clou(d):   # ricalcolo indipendente del clou
    M = d["marks"][d["leg"] - 1:] + [d["fin"]]
    dopo = [sum(math.dist(M[n - 1], M[n]) for n in range(k + 1, len(M))) for k in range(len(M))]
    resto = lambda x, y, k: 0 if k >= len(M) else math.dist((x, y), M[k]) + dopo[k]
    lato = lambda t, fine: sum(1 for f in fine if t >= f)
    P = d["punti"]; TU = [[f[0], f[1], f[2]] for f in d["tu"]]
    fine = min(P[-1][0], TU[-1][0]); g = []; s = P[0][0]
    while s <= fine + 1e-9:
        q, f = interp(P, s), interp(TU, s)
        if q and f: g.append((s, resto(f[0], f[1], lato(s, d["giri"])) - resto(q[0], q[1], lato(s, d["lati"]))))
        s += 1
    aff = {math.floor(f[0]) for f in d["tu"] if f[4] >= d["cop"] or f[5] < d["aff"]}
    best = None
    for i in range(len(g) - d["fin60"]):
        a, b = g[i], g[i + d["fin60"]]
        if any(t in aff for t in range(math.floor(a[0]), math.floor(b[0]) + 1)): continue
        if best is None or b[1] - a[1] > best[2]: best = (a[0], b[0], b[1] - a[1])
    return best

POL = json.loads(re.search(r"const ROT_POL = (\{.*?\});", (ROOT / "js" / "rotta-dati.js").read_text()).group(1))
def vpol(twa, tws_ms):   # interpolazione bilineare sulla tabella, fatta qui
    kn = min(max(tws_ms * 1.9438, POL["tws"][0]), POL["tws"][-1]); i = min(len(POL["tws"]) - 2, int(kn - POL["tws"][0])); fi = kn - POL["tws"][i]
    a = min(max(twa, 30), 180); j = min(len(POL["twa"]) - 2, int((a - POL["twa"][0]) / 5)); fj = (a - POL["twa"][j]) / 5
    v = lambda ii, jj: POL["v"][ii][jj]
    return (v(i, j) * (1 - fi) + v(i + 1, j) * fi) * (1 - fj) + (v(i, j + 1) * (1 - fi) + v(i + 1, j + 1) * fi) * fj

async def regate(br, base, n):
    pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(base + "#collaudo"); await pg.wait_for_timeout(500)
    return pg, errs, [(k, s) for s in range(2601, 2601 + (n + 3) // 4) for k in range(4)][:n]

async def main():
    nome = os.environ.get("BROWSER", "chromium")
    async with async_playwright() as p:
        br = await getattr(p, nome).launch()
        # ---- K1: le stesse regate col codice di riferimento
        rif = []
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(f"git -C {ROOT} archive {RIF} | tar -x -C {tmp}", shell=True, check=True)
            pg, e0, elenco = await regate(br, (pathlib.Path(tmp) / "index.html").as_uri(), NREG)
            for k, s in elenco: await pg.evaluate(CORSA, [k, s, 0]); rif.append(await pg.evaluate(ESITO))
            await pg.close()
        pg, errs, elenco = await regate(br, (ROOT / "index.html").as_uri(), NREG)
        nclou = nfr = 0
        for n, (k, s) in enumerate(elenco):
            await pg.evaluate(CORSA, [k, s, 0]); es = await pg.evaluate(ESITO)
            chk("K1", es == rif[n], f"K1 regata {s}-{k}: arrivi e penalità diversi dal riferimento {RIF}: {es} contro {rif[n]}")
            await pg.click("#finRot"); await pg.wait_for_timeout(120)
            d = await pg.evaluate(DATI)
            C = d["coach"] or []; nfr += len(C)
            print(f"  {s}-{k}: " + " | ".join(f"{x['tipo']} {x['peso']:.0f}" for x in C), flush=True)
            chk("K3", 1 <= len(C) <= 3 and all(re.search(r"\d", x["txt"]) for x in C), f"K3 {s}-{k}: {len(C)} frasi, una senza numero? {[x['txt'] for x in C]}")
            chk("K8", d["ms"] < 200 and d["uguali"], f"K8 {s}-{k}: frasi in {d['ms']:.0f} ms, ricalcolate uguali {d['uguali']}")
            b = clou(d); cl = next((x for x in C if x["tipo"] == "clou"), None)
            if cl or (b and b[2] / 2 >= d["min"] * 3):   # clou detto, o una perdita libera grande che il coach avrebbe dovuto dire (stima prudente: 2 m/s)
                nclou += 1
                ok = cl is not None and b is not None and abs(cl["t0"] - b[0]) < 1e-6 and abs(cl["m"] - round(b[2])) <= 1
                chk("K4", ok, f"K4 {s}-{k}: coach {cl and (cl['t0'], cl['m'])}, ricalcolo {b}")
            for t0, t1 in d["tratti"]:   # K5b
                vicina = min((f[5] for f in d["tu"] if t0 <= f[0] <= t1), default=1e9)
                chk("K5b", vicina < 42, f"K5b {s}-{k}: tratto coperto {t0:.0f}-{t1:.0f} s senza barche entro 10 lunghezze (la più vicina a {vicina:.0f} m)")
            if C:   # K6
                await pg.click("#coachFrasi button[data-k='0']"); await pg.wait_for_timeout(80)
                t = await pg.evaluate("() => rivT0() + riv.pos")
                chk("K6", abs(t - (C[0]["t"] - 5)) <= 1 or C[0]["t"] - 5 < await pg.evaluate("() => rivT0()"), f"K6 {s}-{k}: moviola a {t:.1f}, attesa {C[0]['t'] - 5:.1f}")
            if n < 10:   # K9
                await pg.evaluate("() => { rot.res.ass = rotAssoluta(); rot.res.testo = rotTesto(rot.res.ott, rot.res.sp); }")
                dopo = await pg.evaluate("() => JSON.stringify(coaFrasi(rot.res.ott, rot.res.sp))")
                chk("K9", dopo == json.dumps(C, separators=(",", ":"), ensure_ascii=False) or json.loads(dopo) == C, f"K9 {s}-{k}: frasi diverse dopo V")
            m = await pg.evaluate("""() => { const mb = document.getElementById('movBar').getBoundingClientRect(); return { ecc: Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0), dentro: mb.top >= 0 && mb.bottom <= innerHeight + 0.5, vis: !document.getElementById('coach').hidden }; }""")
            chk("K2", m["ecc"] == 0 and m["dentro"] and m["vis"] == bool(C), f"K2 {s}-{k}: {m}")
            await pg.keyboard.press("Escape"); await pg.wait_for_timeout(80)
        chk("K4", nclou >= 3, f"K4: regate col clou da controllare {nclou} (servono almeno 3 perché il controllo misuri)")
        print(f"frasi in tutto {nfr}, regate col clou controllato {nclou}", flush=True)
        # ---- K2 caso peggiore, K5a, K7 sull'ultima regata
        await pg.evaluate(CORSA, [3, 2601, 0]); await pg.click("#finRot"); await pg.wait_for_timeout(120)
        w = await pg.evaluate("""() => { rot.res.ass = rotAssoluta(); rot.res.testo = rotTesto(rot.res.ott, rot.res.sp); document.getElementById('movTit').textContent = rot.res.testo;
            rot.res.coach = [
              { t: 100, peso: 50, txt: "Qui hai perso di più: fra 12:34 e 13:34 la rotta ottimale ha guadagnato 188 m di percorso su di te. Il vento era girato di 14° contro di te e la rotta ottimale ha virato (lezione 11)." },
              { t: 200, peso: 40, txt: "Fra 12:34 e 13:34 eri nel cono d'ombra di Giorgio Pellegrini: circa 18 s persi." },
              { t: 300, peso: 30, txt: "Hai tagliato la linea 14 s dopo il via; allo sparo andavi a 1,2 nodi (lezione 18)." } ]; coaMostra(); rivMostra();
            const mb = document.getElementById('movBar').getBoundingClientRect(); return { ecc: Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0), top: mb.top, bottom: mb.bottom, H: innerHeight }; }""")
        chk("K2", w["ecc"] == 0 and w["top"] >= 0 and w["bottom"] <= w["H"] + 0.5, f"K2 caso peggiore: {w}")
        print("K2 caso peggiore:", w, flush=True)
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(80)
        for twa, kn, c, D in ((45, 10, 0.3, 40), (90, 12, 0.5, 30), (150, 8, 0.2, 60), (60, 15, 0.45, 50)):
            r = await pg.evaluate("""([twa, kn, c, D]) => { const w = rotVento(R.marks[0].x, R.marks[0].y, rotRaffiche(rot.reg[0].t)), tws = w.tws, fr = [];
                for (let i = 0; i <= D * 10; i++) fr.push({ t: rot.reg[0].t + i / 10, b: [[R.marks[0].x, R.marks[0].y, norm360(w.twd + twa), 0, 1]], c: [c, 1] });
                const o = coaCoperto(fr)[0]; return { persi: o ? o.persi : null, tws }; }""", [twa, kn, c, D])
            stima = D * (1 - vpol(twa, r["tws"] * (1 - c)) / vpol(twa, r["tws"]))
            chk("K5a", r["persi"] is not None and abs(r["persi"] - stima) <= 0.25 * stima, f"K5a twa {twa}, quota {c}, {D} s: coach {r['persi']}, stima {stima:.2f}")
            print(f"K5a twa {twa}° quota {c} per {D} s: coach {r['persi']:.2f} s, stima {stima:.2f} s", flush=True)
        await pg.evaluate(CORSA, [0, 2602, 0]); await pg.click("#finRot"); await pg.wait_for_timeout(120)
        k7 = await pg.evaluate("""() => { const P = rot.res.ott.punti, me = R.boats[0], o = rot.barche[0], salva = riv.all.map(f => ({ t: f.t, b: f.b, c: f.c })), segni = riv.segni.slice(), ocs = reg.ocs;
            riv.all = riv.all.filter(f => f.t >= o.taglio.t && f.t <= P[P.length - 1].t).map(f => { const q = rotIstante(P, f.t, q => [q.x, q.y]); return { t: f.t, b: [[q[0], q[1], 0, 0, 2], [q[0] + 500, q[1], 0, 0, 2]], c: [0, -1] }; });
            riv.segni = []; reg.ocs = 0; const finVero = me.fin, tgVero = o.taglio; me.fin = P[P.length - 1].t; o.taglio = { ...tgVero, t: 0 }; const giriVeri = o.giri; o.giri = rot.res.ott.lati.slice(0, -1).map(t => ({ t }));   // i giri di boa della traccia costruita sono quelli della rotta ottimale
            const sp = rotSpiega(rot.res.ott); const F = coaFrasi(rot.res.ott, sp);
            riv.all = salva; riv.segni = segni; reg.ocs = ocs; me.fin = finVero; o.taglio = tgVero; o.giri = giriVeri; return F.map(x => x.tipo + ": " + x.txt); }""")
        print("K7:", k7, flush=True)
        chk("K7", any(x.startswith("bene") for x in k7) and not any(re.match(r"(clou|affollato|coperto|boa)", x) for x in k7), f"K7 traccia uguale alla rotta ottimale: {k7}")
        await pg.close()
        # ---- K8 pagina senza #collaudo
        pg2 = await br.new_page(viewport={"width": 1360, "height": 650}); e2 = []; pg2.on("pageerror", lambda e: e2.append(str(e)))
        await pg2.goto((ROOT / "index.html").as_uri()); await pg2.wait_for_timeout(400)
        r = await pg2.evaluate("() => ({ c: !!document.getElementById('coach'), nasc: document.getElementById('coach').hidden, sv: typeof window.__sv })")
        chk("K8", r == {"c": True, "nasc": True, "sv": "undefined"} and not e2, f"K8 senza #collaudo: {r}, errori {e2[:2]}")
        await pg2.close()
        chk("K8", not errs and not e0, f"errori della pagina: {(errs + e0)[:3]}")
        await br.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("K1", "K2", "K3", "K4", "K5a", "K6", "K7", "K8", "K9")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
