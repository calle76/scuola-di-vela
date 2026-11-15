# Misura del pilota «da giocatore» (docs/PROPOSTA-PILOTA-GIOCATORE.md §3, criteri G1-G6 scritti prima; via di Ale il 16 novembre 2026).
# Regate del torneo come collaudo_coach.py (4 regate per seme), guidate dal pilota di prima (__sv.pilota) o da tests/pilota_giocatore.js.
#   .venv-collaudi/bin/python tests/misura_pilota_giocatore.py --pilota vecchio|nuovo [--semi 2601-2605] [--errore tardi=8|oltre=25|doppia=1] [--opz ombraS=5,layM=60,heel=18]
# Per ogni regata una riga JSON; in fondo il riepilogo: G1 scuffie, G2 «affollato», G3 virate negli ultimi 40 m dalla boa 1, G4 tempo perso nella prima bolina
# sulla rotta ottimale, G5 arrivi senza squalifica; con --errore, G6: la frase del Coach per quell'errore e il suo numero.
# Non è un collaudo del giro: è uno strumento di misura (esce sempre con 0, salvo errori della pagina).
import asyncio, json, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
PIL = arg("--pilota", "nuovo"); A, B = (int(x) for x in arg("--semi", "2601-2605").split("-"))
OPZ = {k: float(v) for k, v in (x.split("=") for x in arg("--opz", "").split(",") if x)}
NMAX = int(arg("--regate", "1000")); ERR = arg("--errore"); ERRK, ERRV = (ERR.split("=")[0], float(ERR.split("=")[1])) if ERR else (None, None)
if ERR: OPZ[ERRK] = ERRV
PILOTA_JS = (ROOT / "tests" / "pilota_giocatore.js").read_text(encoding="utf-8")

# come CORSA di collaudo_rotta_assoluta.py, più il conto delle virate vicino alla boa 1 e delle scuffie
CORSA = """([k, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme * 7 + k);
  sv.fast(0); sel('aiLevel', seme % 2 ? 'principianti' : 'esperti'); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { tws: seme % 2 ? 12 : 10, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60, me = R.boats[0], m1 = R.marks[0];
  let vir40 = 0, tk = sv.S.tacks, scuffie = 0, cap = false, virate1 = 0, prec = [0, 0]; const dove = [];
  while (R.t < 1500 && R.phase !== 'done'){
    if (me.fin === null) sv.pilota(dt); sv.run(dt, 1);
    const S = sv.S;
    if (S.tacks !== tk){ if (me.leg === 1 && R.t >= 0){ virate1 += S.tacks - tk; if (Math.hypot(S.x - m1.x, S.y - m1.y) < 40) vir40 += S.tacks - tk; } tk = S.tacks; }
    if (S.capsized && !cap){ scuffie++; dove.push([Math.round(R.t), me.leg, Math.round(Math.abs(prec[0])), Math.round(prec[1] * 1.944)]); } cap = !!S.capsized;
    if (!S.capsized){ const w = sv.twd; prec = [((w - S.h + 540) % 360) - 180, S.u]; }
  }
  for (let j = 0; j < 30; j++) sv.run(dt, 1);
  return { fin: me.fin, dsq: !!me.dsq, dnf: !!me.dnf, pp: me.pp || 0, dove, giri: [R.need || 0, R.done || 0], vir40, virate1, scuffie, pos: 1 + R.boats.filter(b => b.fin !== null && me.fin !== null && b.fin < me.fin).length, pg: sv.pg ? { via: sv.pg.virateVia, oltre: sv.pg.oltreFatti, doppie: sv.pg.doppie } : null };
}"""
DATI = """() => { const r = rot.res, o = rot.barche[0];
  return { coach: r.coach, bolina: o.giri.length && r.ott.lati.length ? (o.giri[0].t - o.taglio.t) - (r.ott.lati[0] - r.ott.punti[0].t) : null,
           tu1: o.giri.length ? o.giri[0].t - o.taglio.t : null, taglio: o.taglio.t, lay: r.sp.lati[0] && r.sp.lati[0].lay ? { oltre: r.sp.lati[0].lay.oltre, vicine: r.sp.lati[0].lay.vicine } : null }; }"""

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(500)
        if PIL == "nuovo": await pg.evaluate(PILOTA_JS, OPZ)
        print(f"pilota {PIL}, semi {A}-{B}, opzioni {OPZ}", flush=True)
        righe = []
        for s in range(A, B + 1):
            for k in range(4):
                if len(righe) >= NMAX: break
                r = await pg.evaluate(CORSA, [k, s]); r["seme"], r["k"] = s, k
                try:
                    await pg.evaluate("() => { if (riv.on) rivChiudi(); rotApri(); }"); await pg.wait_for_timeout(120); d = await pg.evaluate(DATI); await pg.evaluate("() => { if (riv.on) rivChiudi(); }")   # la moviola della regata di prima resta aperta e copre la schermata finale: si chiude e si apre la rotta dalla funzione del pulsante
                except Exception as e: d = {"coach": None, "bolina": None, "tu1": None, "taglio": None, "lay": None}; r["senza_rotta"] = str(e)[:80]
                r["bolina"], r["tu1"], r["taglio"], r["lay"] = d["bolina"], d["tu1"], d["taglio"], d["lay"]
                r["coach"] = [{k2: x.get(k2) for k2 in ("tipo", "peso", "t", "s", "m", "n", "ocs")} for x in (d["coach"] or [])]
                righe.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        n = len(righe); tipi = lambda r: [x["tipo"] for x in r["coach"]]
        bol = [r["bolina"] for r in righe if r["bolina"] is not None]
        print(f"\nRIEPILOGO pilota {PIL}, {n} regate, semi {A}-{B}, opzioni {OPZ}")
        print(f"G1 regate con almeno una scuffia: {sum(1 for r in righe if r['scuffie'])} su {n} (scuffie in tutto {sum(r['scuffie'] for r in righe)})")
        print(f"G2 regate in cui il Coach dice «affollato»: {sum(1 for r in righe if 'affollato' in tipi(r))} su {n} (regate col Coach letto: {sum(1 for r in righe if r['coach'])})")
        print(f"G3 virate negli ultimi 40 m dalla boa 1, media: {statistics.mean(r['vir40'] for r in righe):.2f} (virate nel primo lato, media {statistics.mean(r['virate1'] for r in righe):.2f})")
        print(f"G4 tempo perso nella prima bolina sulla rotta ottimale: mediana {statistics.median(bol):.1f} s, media {statistics.mean(bol):.1f} s ({len(bol)} regate misurate)" if bol else "G4 non misurato")
        print(f"G5 arrivate senza squalifica: {sum(1 for r in righe if r['fin'] is not None and not r['dsq'])} su {n}; posto medio {statistics.mean(r['pos'] for r in righe if r['fin'] is not None):.2f}; fra i primi 3: {sum(1 for r in righe if r['fin'] is not None and r['pos'] <= 3)}")
        print(f"   frasi del Coach: " + ", ".join(f"{t} {sum(1 for r in righe if t in tipi(r))}" for t in sorted({t for r in righe for t in tipi(r)})))
        vic = [r["lay"]["vicine"] for r in righe if r["lay"]]
        print(f"   virate entro 80 m dalla boa 1 contate dal Coach: " + ", ".join(f"{v} virate in {vic.count(v)} regate" for v in sorted(set(vic))) + f"; frase «hai virato N volte» detta in {sum(1 for r in righe if any(c['tipo'] == 'boa' and c.get('n') for c in r['coach']))}")
        if PIL == "nuovo": print(f"   virate per l'aria libera: {sum(r['pg']['via'] for r in righe)} in {sum(1 for r in righe if r['pg']['via'])} regate")
        if ERR:
            tipo = "partenza" if ERRK == "tardi" else "boa"; ok = fatti = 0
            for r in righe:
                x = next((c for c in r["coach"] if c["tipo"] == tipo), None)
                if ERRK == "tardi": fatti += 1; giusto = x is not None and x.get("s") is not None and abs(x["s"] - ERRV) <= 2
                elif ERRK == "oltre": fatti += r["pg"]["oltre"] > 0; giusto = x is not None and x.get("m") is not None and abs(x["m"] - ERRV) <= 5
                else: fatti += r["pg"]["doppie"] > 0; giusto = x is not None and (x.get("n") or 0) >= 2
                ok += giusto
                print(f"   G6 {r['seme']}-{r['k']}: frase «{tipo}» {x}, giusta {giusto}")
            print(f"G6 errore {ERR}: il Coach dice la frase giusta col numero giusto in {ok} regate su {n} (errore fatto davvero in {fatti})")
        print("errori della pagina:", errs[:3]); await br.close()
        sys.exit(1 if errs else 0)
asyncio.run(main())
