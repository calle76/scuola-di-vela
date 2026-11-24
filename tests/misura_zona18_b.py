# Regola 18, versione B (voce 49, docs/PROPOSTA-REGOLA-18-B.md): serve che i rivali la conoscano? Solo misura, niente codice nel gioco.
# Regate del torneo col pilota (pagina nuova per regata). Ogni 0,25 s, per ogni debito di spazio aperto con le due barche entro VICINE m: la barca che deve lo spazio è la stessa
# che cederebbe per le regole 10-13 (quelle che i rivali seguono già)? Si contano i debiti, quelli con le barche vicine almeno 1 s, quelli in cui per almeno 1 s le regole dicono
# cose diverse, chi è coinvolto (giocatore o rivali) e i contatti avvenuti a debito aperto.
# Uso: python tests/misura_zona18_b.py [--lungo] [N regate] [primo seme]
import asyncio, collections, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
LUNGO = "--lungo" in sys.argv; num = [int(a) for a in sys.argv[1:] if a.isdigit()]
NREG = num[0] if num else (30 if LUNGO else 60); DA = num[1] if len(num) > 1 else (3701 if LUNGO else 3601); NT = 3 if LUNGO else 4
src = (ROOT / "tests" / "collaudo_rotta_assoluta.py").read_text().split("async def main")[0]
A_ = {"__file__": str(ROOT / "tests" / "collaudo_rotta_assoluta.py")}; exec(src, A_)
MIS = """const VICINE = 15, D = {}; let tic = 0; const misura = () => { if (tic++ % 15 || !R.zona) return;
    for (const key of Object.keys(R.zona)){ const p = R.zona[key], A = p.a, B = p.deve, i = R.boats.indexOf(A), j = R.boats.indexOf(B), k2 = key + '-' + p.leg + '-' + Math.round(p.t * 10);
      const q = D[k2] = D[k2] || { dirittoMe: !!A.me, deveMe: !!B.me, leg: p.leg, vic: 0, div: 0, dmin: 1e9, r183: p.r183, reg: {} };
      const d = Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y); q.dmin = Math.min(q.dmin, d); if (d > VICINE || mureOpposteBolina(A, B)) continue;
      q.vic += 0.25; const c = chiCede(A, B); if (c.cede !== B){ q.div += 0.25; q.reg[c.regola] = (q.reg[c.regola] || 0) + 0.25; } } };"""
C = A_["CORSA"]
vecchio = "if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }"; assert C.count(vecchio) == 1
C = C.replace("while (R.t < 1500", MIS + " while (R.t < 1500", 1).replace(vecchio, "if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); misura(); }")
C = C.replace("return { fin: R.boats[0].fin };", "return { D: Object.values(D), nz: R.nZona || 0, cont: (R.contLog || []).filter(c => c.g !== undefined && c.dm <= 13.6).map(c => [c.r, c.g, c.g0]) };")
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); D = []; nz = 0; cont = []
        for k, s in [(k, s) for s in range(DA, DA + (NREG + NT - 1) // NT) for k in range(NT)][:NREG]:
            q = await b.new_page(); await q.goto((ROOT / "index.html").as_uri() + "#collaudo"); await q.wait_for_timeout(250)
            await q.evaluate("v => { __sv.lungo = v; }", LUNGO); r = await q.evaluate(C, [k, s, 0]); await q.close()
            D += r["D"]; nz += r["nz"]; cont += r["cont"]
        print(f"{NREG} regate {'lunghe' if LUNGO else 'corte'}, semi da {DA}: debiti {nz}, visti dalla misura {len(D)}, contatti entro 13,6 m dalla boa {len(cont)} {cont}")
        tipi = {"deve un rivale al giocatore": lambda x: x["dirittoMe"], "deve il giocatore a un rivale": lambda x: x["deveMe"], "fra rivali": lambda x: not x["dirittoMe"] and not x["deveMe"]}
        for leg in (1, 2):
            for nome, f in tipi.items():
                X = [x for x in D if f(x) and x["leg"] == leg]; v = [x for x in X if x["vic"] >= 1]; d = [x for x in X if x["div"] >= 1]; reg = collections.Counter()
                for x in d:
                    for k2, t in x["reg"].items(): reg[k2] += t
                print(f"  boa {leg}, {nome}: debiti {len(X)}, barche vicine (15 m) almeno 1 s {len(v)}, regole diverse almeno 1 s {len(d)} (secondi {sum(x['div'] for x in d):.0f} su {sum(x['vic'] for x in X):.0f}; per regola {dict(reg)}), di cui sotto 6 m {sum(x['dmin'] < 6 for x in d)}, 18.3 {sum(bool(x['r183']) for x in X)}")
        await b.close()
asyncio.run(main())
