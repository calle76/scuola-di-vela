# Regole 15 e 16 nelle regate di Deriva (1.3.10, docs/PROPOSTA-REGOLE-15-16.md, criteri R1, R3, R4; R2 è collaudo_semaforo.py, R5 collaudo_deriva_lezioni.py).
#   R1 casi a mano: due barche messe a mano nella regata dei giri (vento costante da nord), istante per istante, poi chi cede (chiCede1516):
#      6 per la 15 (virata davanti con contatto a 2, 5, 5,4 e 6 s; precedenza ricevuta per manovra altrui; affiancamento da dietro sottovento),
#      6 per la 16 (poggiata verso chi passa a poppa, la 16.2; orzata verso la sopravento affiancata; cambio sotto G; cambio allontanandosi; cambio più vecchio di T;
#      precedenza appena ricevuta), 4 per il semaforo (giallo per la 15 e per la 16, verde, rosso); tutti con l'esito scritto qui prima
#   R3 la Scuola non cambia: le due regate della Scuola col pilota, 12 corse, arrivi e penalità identici al codice di riferimento (RIF, git archive); nelle
#      regate della Scuola e negli esercizi delle lezioni le regole 15 e 16 sono spente
#   R4 effetti, senza soglia: N regate del torneo col pilota (semi 2701-...), contatti per regola, quanti con la 15 e con la 16
#   --lungo (1.3.32, voce 66c): R4 sulle regate lunghe, come le gioca Ale (__sv.lungo = true: 3 regate per torneo, bolina 560 m, triangolo 440 m); R1 e R3 non cambiano (casi a mano, Scuola)
# Uso: python tests/collaudo_regole_15_16.py [--regate N] [--rif v1.3.9] [--lungo]   (BROWSER=firefox)
import asyncio, json, math, os, pathlib, subprocess, sys, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
NREG = int(arg("--regate", "200")); RIF = arg("--rif", "v1.3.79") # 27 nov 2026 (voce 92): dalla barca M (1.3.59-1.3.61) nessuna regata può essere identica a una versione di prima; riferimento la 1.3.61: ora è solo una guardia di non-regressione (la prova della funzione è stata fatta quando è nata)
LUNGO = "--lungo" in sys.argv; NT = 3 if LUNGO else 4   # regate di un torneo
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

CASO = """([snap, sem]) => { const sv = __sv; sv.fast(0); sv.openItem(["r", 3]);
  const A = R.boats[0], B = R.boats[1]; R.boats.slice(2).forEach((b, k) => { b.S.x = 5000 + 300 * k; b.S.y = 5000; });
  R.prec = {}; R.phase = "race"; for (const b of R.boats){ delete b.storiaH; delete b.tkP; delete b.virP; delete b.sgV; b.virando = false; b.ocs = false; b.sconta = false; }
  for (const s of snap){ R.t = s[0]; Object.assign(A.S, { x: s[1], y: s[2], h: (s[3] + 360) % 360, u: s[7] }); Object.assign(B.S, { x: s[4], y: s[5], h: (s[6] + 360) % 360, u: s[8] });
    aggiornaVirate(); aggiornaPrecedenze(); }
  const c = chiCede1516(A, B), p = R.prec["0-1"];
  let col = null; if (sem){ R.semUntil = R.t + 2; semaforo(); col = R.sem; }
  return { cede: c.cede === A ? "A" : "B", regola: c.regola, dt: p ? +(R.t - p.t).toFixed(2) : null, r1516: R.r1516, col }; }"""

def scena(passi, A, B, uA=2, uB=2, dt=0.25):
    """A, B: funzioni t -> (x, y, h). Istantanee ogni dt fino a passi*dt."""
    out = []
    for k in range(passi + 1):
        t = k * dt; a, b = A(t), B(t); out.append([t, *a, *b, uA(t) if callable(uA) else uA, uB(t) if callable(uB) else uB])
    return out

def gira(h0, h1, t0, t1):   # prua da h0 a h1 (gradi, verso più corto) fra t0 e t1
    d = ((h1 - h0 + 540) % 360) - 180
    return lambda t: h0 + d * min(1, max(0, (t - t0) / (t1 - t0)))

def caso15_virata(contatto):   # A mure a sinistra (45°) vira a mure a dritta (315°) davanti a B mure a dritta, che resta dietro libera: alla fine della virata la precedenza è di A
    hA = gira(45, 315, 2, 5)
    fine_vir = 2 + 3 * (45 + 42) / 90   # la virata finisce a 42° dal vento (VIRATA_MIN)
    T = fine_vir + contatto
    n = int(T / 0.25 + 0.5)
    return scena(n, lambda t: (-6, -6, hA(t)), lambda t: (0, 0, 315))

async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        async def caso(nome, snap, att_cede, att_regola, sem=False, att_col=None):
            r = await pg.evaluate(CASO, [snap, sem])
            ok = r["r1516"] and r["cede"] == att_cede and r["regola"] == att_regola and (att_col is None or r["col"] == att_col)
            chk("R1", ok, f"R1 {nome}: cede {r['cede']} per la regola {r['regola']} (atteso {att_cede}, {att_regola}){'' if att_col is None else ', semaforo ' + str(r['col']) + ' (atteso ' + att_col + ')'}; dal cambio di precedenza {r['dt']} s")
        # ---- regola 15
        for nome, c, att in (("15a virata davanti, contatto 2 s dopo", 2, ("A", 15)), ("15b virata davanti, contatto 5 s dopo (dentro T)", 5.0, ("A", 15)),
                             ("15c virata davanti, contatto 5,5 s dopo (appena fuori T)", 5.5, ("B", 12)), ("15d virata davanti, contatto 6 s dopo", 6, ("B", 12))):
            await caso(nome, caso15_virata(c), *att)
        # 15e: B (mure a dritta, davanti) vira a mure a sinistra: la precedenza passa ad A per manovra di B → resta la 10
        hB = gira(315, 45, 2, 5)
        await caso("15e precedenza ricevuta per manovra dell'altra", scena(28, lambda t: (0, 0, 315), lambda t: (-6, -6, hB(t))), "B", 10)
        # 15f: stesse mure (315°), B dietro libera più veloce, poi affiancata sottovento (lato sinistro di A, verso 225°): la precedenza passa a B (11), autore la più veloce
        def Bf(t):
            if t < 2: return (3.5, 3.5, 315)
            f = min(1, (t - 2) / 2); x0, y0 = 3.5, 3.5; x1, y1 = -2.1 - 1.4, -2.1 + 1.4
            return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 315)
        await caso("15f affiancamento da dietro sottovento, contatto 1 s dopo", scena(20, lambda t: (0, 0, 315), Bf, uA=2, uB=3), "B", 15)
        # ---- regola 16 (A mure a dritta con la precedenza da più di T; B mure a sinistra che passa a poppa, a 8 m in direzione 190°)
        Bp = lambda t: (8 * math.sin(math.radians(190)), -8 * math.cos(math.radians(190)), 45)
        await caso("16a poggiata verso chi passa a poppa (16.2)", scena(40, lambda t: (0, 0, gira(315, 280, 7, 9)(t)), Bp), "A", 16)
        await caso("16c cambio di 8°, sotto G", scena(40, lambda t: (0, 0, gira(315, 307, 7, 9)(t)), Bp), "B", 10)
        await caso("16d orzata, allontanandosi da lei", scena(40, lambda t: (0, 0, gira(315, 345, 7, 9)(t)), Bp), "B", 10)
        await caso("16e cambio più vecchio di T (fatto 7 s prima)", scena(60, lambda t: (0, 0, gira(315, 280, 6, 8)(t)), Bp), "B", 10)
        # 16b: stesse mure, A sottovento (prua 300°) affiancata a B sopravento (a 3 m in direzione 30°): A orza verso B
        Bs = lambda t: (3 * math.sin(math.radians(30)), -3 * math.cos(math.radians(30)), 300)
        await caso("16b orzata verso la sopravento affiancata", scena(40, lambda t: (0, 0, gira(300, 330, 7, 9)(t)), Bs), "A", 16)
        # 16f: B vira e dà la precedenza ad A (meno di T fa), A poggia di 25° verso B: niente 16 (la precedenza deve essere sua da almeno T)
        hB2 = gira(315, 45, 5, 7)
        await caso("16f precedenza appena ricevuta, poi cambio verso l'altra", scena(36, lambda t: (0, 0, gira(315, 290, 7.5, 8.5)(t)), lambda t: (-8, -3, hB2(t))), "B", 10)   # B davanti e a sinistra della prua di A: prima del suo cambio di mure cede A (12)
        # ---- semaforo (il giocatore è A)
        await caso("S1 giallo per la 15", caso15_virata(2), "A", 15, sem=True, att_col="giallo")
        await caso("S2 giallo per la 16", scena(40, lambda t: (0, 0, gira(315, 280, 7, 9)(t)), Bp), "A", 16, sem=True, att_col="giallo")
        await caso("S3 verde (precedenza ricevuta)", scena(28, lambda t: (0, 0, 315), lambda t: (-6, -6, hB(t))), "B", 10, sem=True, att_col="verde")
        hB5 = gira(45, 315, 2, 5); fine5 = 2 + 3 * (45 + 42) / 90
        await caso("S5 verde: l'altra vira davanti a te (le 10-13 ti farebbero cedere, la 15 dà torto a lei)", scena(int((fine5 + 2) / 0.25 + 0.5), lambda t: (0, 0, 315), lambda t: (-6, -6, hB5(t))), "B", 15, sem=True, att_col="verde")
        await caso("S4 rosso (A mure a sinistra)", scena(8, lambda t: (0, 0, 45), lambda t: (-6, -6, 315)), "A", 10, sem=True, att_col="rosso")
        # ---- le regole sono spente nella Scuola e negli esercizi
        off = await pg.evaluate("""() => { const sv = __sv, o = {}; sv.openItem(["r", 0]); o.bastone = R.r1516; sv.openItem(["r", 1]); o.raffiche = R.r1516;
            sv.openItem(["r", 2]); o.salti = R.r1516; sv.openItem(["r", 3]); o.giri = R.r1516; return o; }""")
        chk("R3", off == {"bastone": False, "raffiche": False, "salti": True, "giri": True}, f"R3 regole 15 e 16 accese: {off}")
        await pg.close()
        # ---- R3: regate della Scuola identiche al riferimento
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
            subprocess.run(f"git -C $(git -C {ROOT} rev-parse --show-toplevel) archive {RIF} | tar -x -C {tmp}", shell=True, check=True)
            rif = await scuola((pathlib.Path(tmp) / "index.html").as_uri())
        ora = await scuola((ROOT / "index.html").as_uri())
        chk("R3", rif == ora and len(ora) == 12, f"R3 le regate della Scuola: {sum(a == b for a, b in zip(rif, ora))} su 12 identiche a {RIF}")
        # ---- R4: effetti nel torneo
        src = (ROOT / "tests" / "collaudo_rotta_assoluta.py").read_text().split("async def main")[0]
        A_ = {"__file__": str(ROOT / "tests" / "collaudo_rotta_assoluta.py")}; exec(src, A_)
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        if LUNGO: await pg.evaluate("() => { __sv.lungo = true; }")
        conta = {}; contatti = 0; mie = 0
        for k, s in [(k, s) for s in range(2701, 2701 + (NREG + NT - 1) // NT) for k in range(NT)][:NREG]:
            await pg.evaluate(A_["CORSA"], [k, s, 0])
            pl = await pg.evaluate("() => __sv.R.penList.filter(x => x.includes('contatto con'))")
            for x in pl:
                contatti += 1; reg = x.rsplit("(regola ", 1)[-1].rstrip(").") if "(regola " in x else "?"; conta[reg] = conta.get(reg, 0) + 1
                if x.startswith("Tu,"): mie += 1
        print(f"R4: {NREG} regate del torneo{' lungo' if LUNGO else ''} col pilota: {contatti} contatti con colpa ({mie} del giocatore); per regola {dict(sorted(conta.items()))}", flush=True)
        chk("R4", contatti > 0, f"R4 il metro ha visto contatti: {contatti}")
        chk("R4", not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("R1", "R3", "R4")) or casi.get("R1", 0) < 17: print("ESITO: NON VALIDA (casi mancanti)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
