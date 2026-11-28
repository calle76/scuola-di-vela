# Regola 18, spazio alla boa, versione A (1.3.49, voce 49, docs/PROPOSTA-REGOLA-18.md, criteri Z1-Z5 scritti prima; Z6 è collaudo_pannello_lezioni.py e il controllo
# delle Impostazioni, Z7 si fa sulle regate di Ale).
#   Z2 casi a mano (esito scritto qui prima di lanciarlo): due barche messe a mano vicino alla boa 1 della regata dei giri (Deriva, vento costante da nord),
#      istante per istante, poi chi cede (chiCede1516) e, dove serve, il colore del semaforo o la colpa di un contatto vero (contacts)
#   Z1 la Scuola non cambia: le due regate della Scuola col pilota, 12 corse, arrivi e penalità identici al riferimento (--rif, git archive)
#   Z3-Z5 N regate del torneo col pilota (pagina nuova per regata), registro dei contatti di #collaudo con la colpa con e senza la 18 e la distanza dalla boa:
#      Z3 fuori dalla zona (oltre 13,6 m) la colpa non cambia, con almeno 50 contatti misurati; Z4 almeno un debito aperto e un contatto deciso dalla 18;
#      Z5 contatti con colpa dei rivali vicino alla boa, prima e dopo (si riporta; oltre +30% la versione A non esce da sola)
# Uso: python tests/collaudo_regola18.py [--regate 90] [--semi-da 2801] [--rif v1.3.59] [--lungo]   (BROWSER=firefox)
import asyncio, math, os, pathlib, subprocess, sys, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
NREG = int(arg("--regate", "90")); DA = int(arg("--semi-da", "2801")); RIF = arg("--rif", "v1.3.77")   # 1.3.59 (voce 84): la barca M cambia i tempi di tutte le regate; Z1 confronta con la prima versione che ha la stessa barca (prima v1.3.48) # 27 nov 2026 (voce 92): dalla barca M (1.3.59-1.3.61) nessuna regata può essere identica a una versione di prima; riferimento la 1.3.61: ora è solo una guardia di non-regressione (la prova della funzione è stata fatta quando è nata)
LUNGO = "--lungo" in sys.argv; NT = 3 if LUNGO else 4
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

# snap: [t, xA, yA, hA, xB, yB, hB, uA, uB, legA, legB], posizioni rispetto alla boa 1; ia, ib: indici delle barche (0 = il giocatore)
CASO = """([snap, o]) => { const sv = __sv; sv.fast(0); sv.openItem(["r", o.regata]);
  const A = R.boats[o.ia], B = R.boats[o.ib], M = R.mark; R.boats.forEach((b, k) => { if (b !== A && b !== B){ b.S.x = 5000 + 300 * k; b.S.y = 5000; } });
  R.prec = {}; R.zona = {}; R.zonaFatta = {}; R.contacts = {}; R.phase = "race";
  for (const b of R.boats){ for (const k of ["storiaH", "tkP", "virP", "sgV", "v183", "tk18", "dBoa", "virT"]) delete b[k]; b.virando = false; b.ocs = false; b.sconta = false; b.fin = null; b.dnf = false; b.leg = 1; }
  for (const s of snap){ R.t = s[0] + o.tOff; Object.assign(A.S, { x: M.x + s[1], y: M.y + s[2], h: (s[3] + 360) % 360, u: s[7] }); Object.assign(B.S, { x: M.x + s[4], y: M.y + s[5], h: (s[6] + 360) % 360, u: s[8] });
    A.leg = s[9]; B.leg = s[10]; aggiornaVirate(); aggiornaPrecedenze(); aggiornaZona18(); }
  const c = chiCede1516(A, B), z = R.zona[Math.min(o.ia, o.ib) + "-" + Math.max(o.ia, o.ib)];
  let col = null; if (o.sem){ R.semUntil = R.t + 2; semaforo(); col = R.sem; }
  let colpa = null; if (o.contatto){ B.S.x = A.S.x + 0.6; B.S.y = A.S.y; B.S.h = A.S.h; R.contacts = {}; contacts(); const k = Math.min(o.ia, o.ib) + "-" + Math.max(o.ia, o.ib), cc = R.contColpa && R.contColpa[k];
    colpa = cc ? { g: cc.g === A ? "A" : "B", r: cc.r, testo: R.penList[R.penList.length - 1] } : null; }
  return { cede: c.cede === A ? "A" : "B", regola: c.regola, r1516: R.r1516, deve: z ? (z.deve === A ? "A" : "B") : null, col, colpa }; }"""

S2 = math.sqrt(0.5)
def su_rotta(h, lat, s):   # punto sulla rotta di prua h che passa a lat metri a dritta della boa, s metri prima (negativo) o dopo il traverso della boa
    hr = math.radians(h); fx, fy = math.sin(hr), -math.cos(hr); rx, ry = math.cos(hr), math.sin(hr)
    return (lat * rx + s * fx, lat * ry + s * fy)
def scena(T, A, B, uA=2, uB=2, leg=lambda t: (1, 1), dt=0.25):
    out = []
    for k in range(int(T / dt + 0.5) + 1):
        t = k * dt; a, b = A(t), B(t); out.append([t, *a, *b, uA, uB, *leg(t)])
    return out
def gira(h0, h1, t0, t1):
    d = ((h1 - h0 + 540) % 360) - 180
    return lambda t: h0 + d * min(1, max(0, (t - t0) / (t1 - t0)))
def lin(pts):   # interpolazione lineare a tratti di [(t, valore)]
    def f(t):
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t <= t1: return v0 + (v1 - v0) * max(0, (t - t0) / (t1 - t0))
        return pts[-1][1]
    return f
# mure a sinistra, prua 45°: A all'interno (3 m a dritta della boa), B all'esterno (6 m), sovrapposte; A entra nella zona a t = 3,9 s
P = lambda lat, s: (*su_rotta(45, lat, s), 45)
C1A = lambda t: P(3, -20 + 2 * t)
C1B = lambda t: P(6, -20 + 2 * t)

async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        async def caso(nome, snap, att_cede, att_regola, att_col=None, att_colpa=None, **o):
            o = {"regata": 3, "ia": 0, "ib": 1, "tOff": 0, "sem": att_col is not None, "contatto": att_colpa is not None, **o}
            r = await pg.evaluate(CASO, [snap, o])
            ok = r["cede"] == att_cede and r["regola"] == att_regola and (att_col is None or r["col"] == att_col) and (att_colpa is None or (r["colpa"] and [r["colpa"]["g"], r["colpa"]["r"]] == list(att_colpa) and "regola 18" in r["colpa"]["testo"]))
            chk("Z2", ok, f"Z2 {nome}: cede {r['cede']} per la regola {r['regola']} (atteso {att_cede}, {att_regola}); debito: {r['deve']}"
                + ("" if att_col is None else f"; semaforo {r['col']} (atteso {att_col})") + ("" if att_colpa is None else f"; contatto {r['colpa']} (atteso {att_colpa})"))
        # C1: sovrapposte all'ingresso, A interna e sopravento: per la 11 cederebbe A, per la 18 l'esterna B
        await caso("C1 sovrapposte, l'esterna dà spazio all'interna", scena(5, C1A, C1B), "B", 18, att_col="verde")
        # C2: B libera dietro quando A entra, poi la raggiunge sottovento all'esterno: per la 11 cederebbe A (sopravento), il debito di B resta
        sB = lin([(0, -24), (3, -18), (5, -8)]); lB = lin([(0, 4), (3, 4), (5, 6)])
        C2A, C2B = (lambda t: P(3, -18 + 2 * t)), (lambda t: P(lB(t), sB(t)))
        await caso("C2 libera dietro all'ingresso, poi sovrapposta all'esterno", scena(5, C2A, C2B), "B", 18)
        # C3: mure opposte tutte e due di bolina: la 18 non vale, resta la 10
        await caso("C3 mure opposte di bolina", scena(5, C1A, lambda t: (*su_rotta(315, 3, -20 + 2 * t), 315)), "A", 10)
        # C4 (18.3): A mure a sinistra dentro la zona vira a mure a dritta; B mure a dritta che arriva alla boa
        hA = gira(45, 315, 2, 4)
        def C4A(t):
            if t <= 2: return (-5 + S2 * t, 7 - S2 * t, 45)
            x, y = -5 + S2 * 2, 7 - S2 * 2
            if t <= 4: return (x, y, hA(t))
            return (x - S2 * (t - 4), y - S2 * (t - 4), 315)
        await caso("C4 virata dentro la zona (18.3)", scena(6, C4A, lambda t: (*su_rotta(315, 3, -18 + 2 * t), 315), uA=1), "A", 18)
        # C5: come C1, poi A rallenta e resta libera dietro a B: per la 12 cederebbe A, il debito di B resta
        sA5 = lin([(0, -20), (4, -12), (8, -10)])
        await caso("C5 sovrapposizione rotta dopo l'ingresso", scena(8, lambda t: P(3, sA5(t)), lambda t: P(6, -20 + 2 * t)), "B", 18)
        # C6: come C1, poi tutte e due tornano indietro e A esce dalla zona (16,3 m): debito finito, torna la 11
        s6 = lin([(0, -20), (5, -10), (8, -16)])
        await caso("C6 chi ha diritto esce dalla zona", scena(8, lambda t: P(3, s6(t)), lambda t: P(6, s6(t))), "A", 11)
        # C7: come C1, poi A gira la boa (lato 2): debito finito
        await caso("C7 chi ha diritto ha girato la boa", scena(6, C1A, C1B, leg=lambda t: (2 if t >= 5.5 else 1, 1)), "A", 11)
        # C8: come C1, poi A vira (prua nel vento): debito finito, A in virata cede (13)
        hA8 = gira(45, 330, 5, 7)
        await caso("C8 chi ha diritto passa con la prua nel vento", scena(6.5, lambda t: (*su_rotta(45, 3, -20 + 2 * min(t, 5)), hA8(t)), lambda t: P(6, -20 + 2 * min(t, 5))), "A", 13)
        # C9: A entra nella zona con B a più di 40 m; B arriva dopo, sottovento all'esterno: lo spazio lo deve B
        await caso("C9 lontane all'ingresso, B arriva dopo", scena(10, lambda t: P(3, -13 + 0.25 * t), lambda t: P(6, -80 + 6.95 * t)), "B", 18)
        # C10: nella Scuola (regata a bastone) la 18 non c'è
        await caso("C10 regata della Scuola", scena(5, C1A, C1B), "A", 11, regata=0)
        # C11: prima dello sparo la 18 non c'è
        await caso("C11 prima del via", scena(5, C1A, C1B), "A", 11, tOff=-30)
        # C12: il giocatore deve lo spazio ma per la 11 avrebbe la precedenza: giallo
        await caso("C12 semaforo giallo (devi lo spazio, la precedenza sarebbe tua)", scena(5, C2A, C2B), "B", 18, att_col="giallo", ia=1, ib=0)
        # C13: contatto vero alla fine di C1: colpa di B per la regola 18
        await caso("C13 contatto nella zona", scena(5, C1A, C1B), "B", 18, att_colpa=("B", 18))
        await pg.close()
        # ---- Z1: regate della Scuola identiche al riferimento
        PIL = """([r, seme]) => { const sv = __sv; sv.fast(0); __seed(seme); sv.simTime = 0; sv.openItem(["r", r]); const R = sv.R, dt = 1 / 60;
          while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }
          return R.boats.map(b => [b.fin === null ? null : Math.round(b.fin * 100) / 100, b.pen || 0]); }"""
        SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
          t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
        async def scuola(base):
            out = []
            for k in range(12):
                q = await b.new_page(); await q.add_init_script(SEME); await q.goto(base + "#collaudo"); await q.wait_for_timeout(200)
                out.append(await q.evaluate(PIL, [k % 2, 300 + k])); await q.close()
            return out
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(f"git -C {ROOT} archive {RIF} | tar -x -C {tmp}", shell=True, check=True)
            rif = await scuola((pathlib.Path(tmp) / "index.html").as_uri())
        ora = await scuola((ROOT / "index.html").as_uri())
        chk("Z1", rif == ora and len(ora) == 12, f"Z1 le regate della Scuola: {sum(a == b for a, b in zip(rif, ora))} su 12 identiche a {RIF}")
        # ---- Z3-Z5: torneo col pilota
        src = (ROOT / "tests" / "collaudo_rotta_assoluta.py").read_text().split("async def main")[0]
        A_ = {"__file__": str(ROOT / "tests" / "collaudo_rotta_assoluta.py")}; exec(src, A_)
        fuori = diversi = n18 = nz = zona = riv0 = riv1 = tutti = 0
        for k, s in [(k, s) for s in range(DA, DA + (NREG + NT - 1) // NT) for k in range(NT)][:NREG]:
            q = await b.new_page(viewport={"width": 1360, "height": 650}); q.on("pageerror", lambda e: errs.append(str(e)))
            await q.goto((ROOT / "index.html").as_uri() + "#collaudo"); await q.wait_for_timeout(300)
            await q.evaluate("v => { __sv.lungo = v; }", LUNGO)
            await q.evaluate(A_["CORSA"], [k, s, 0])
            r = await q.evaluate("() => ({ log: (__sv.R.contLog || []).filter(c => c.g !== undefined), nz: __sv.R.nZona || 0 })"); await q.close()
            nz += r["nz"]
            for c in r["log"]:
                tutti += 1; n18 += c["r"] == 18
                if c["dm"] > 13.6:
                    fuori += 1; diversi += (c["g"], c["r"]) != (c["g0"], c["r0"])
                else:
                    zona += 1; riv0 += c["g0"] != 0; riv1 += c["g"] != 0
        print(f"Z3-Z5: {NREG} regate del torneo{' lungo' if LUNGO else ''} col pilota (semi {DA}-): {tutti} contatti, {fuori} fuori dalla zona, {zona} nella zona; debiti aperti {nz}, contatti decisi dalla 18 {n18}", flush=True)
        chk("Z3", fuori >= 50 and diversi == 0, f"Z3 fuori dalla zona la colpa non cambia: {diversi} diversi su {fuori} (servono almeno 50 contatti)")
        chk("Z4", nz > 0 and n18 > 0, f"Z4 la regola lavora: {nz} debiti aperti, {n18} contatti decisi dalla 18")
        cresce = (riv1 - riv0) / riv0 if riv0 else (1 if riv1 else 0)
        print(f"Z5 contatti con colpa dei rivali nella zona: {riv0} senza la 18, {riv1} con la 18 ({cresce:+.0%}); oltre +30% la versione A non esce da sola", flush=True)
        chk("Z5", cresce <= 0.30, f"Z5 colpe dei rivali alla boa: {riv0} -> {riv1}")
        chk("Z4", not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if casi.get("Z2", 0) < 13 or any(casi.get(k, 0) == 0 for k in ("Z1", "Z3", "Z4", "Z5")): print("ESITO: NON VALIDA (casi mancanti)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
