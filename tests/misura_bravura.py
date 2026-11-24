# Voce 82 (docs/PROPOSTA-RIVALI-CHE-CRESCONO.md): quanto si sente in acqua la bravura c (0-100) di un rivale. Solo misura, gioco invariato: i parametri di guida si scrivono nel torneo (tor.av) prima di aprire la regata.
# G2: regate lunghe da 4 col pilota, tutti e tre i rivali alla stessa bravura; per ogni seme le cinque bravure hanno stesso vento, stessi tratti, stesso carattere e stesso sorteggio dei parametri.
# G2b/G5: regate lunghe da 6, i cinque rivali a c = 0, 25, 50, 75, 100 in ordine mescolato col seme.
# Uso (col freno): python tests/misura_bravura.py g2|g2b PRIMO ULTIMO [--corte]   scrive MIS_OUT (o TMPDIR)/bravura-<parte>-<primo>-<browser>[-corte].json ; python tests/misura_bravura.py leggi FILE...
import asyncio, json, math, os, pathlib, statistics as st, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BR = os.environ.get("BROWSER", "chromium"); OUT = pathlib.Path(os.environ.get("MIS_OUT", os.environ.get("TMPDIR", "/tmp")))
C = [0, 25, 50, 75, 100]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
# apre e corre in un solo evaluate, in una pagina nuova (docs: numeri a caso fra due evaluate)
CORRI = """async ([seme, cs, lungo]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); sv.lungo = lungo; sv.opt.countdown = 180; sv.opt.coachReg = false; sv.skipBrief = true;
  __seed(seme); progress.rivali = {}; const T = torNuovo(null, cs.length, "principianti");
  T.av.forEach((a, k) => { const tr = rivaleTr(a.nome), f = cs[k] / 100; __seed(seme * 100 + k); const p = aiTratti("principianti", tr); __seed(seme * 100 + k); const e = aiTratti("esperti", tr), m = {};
    for (const q in p) m[q] = typeof p[q] === "number" ? p[q] * (1 - f) + e[q] * f : p[q]; a.ai = m; });
  tor = progress.torneo = T; __seed(seme + 50000); openItem(["r", "t"]);
  const me = R.boats[0];
  while (me.fin === null && !me.dnf && R.t < 2400){ sv.pilota(dt); sv.run(dt, 1); }
  for (let k = 0; k < 60 * 1800 && R.boats.some(b => b.fin === null && !b.dnf); k++){ updateGusts(dt); updateRace(dt); simTime += dt; }
  return { fin: R.boats.map(b => b.dnf || b.dsq ? null : b.fin), pp: R.boats.map(b => b.pp || 0), ai: T.av.map(a => a.ai.up), tri: !!R.tri, lungo: LUNGO }; }"""
async def misura(parte, a, z, lungo):
    righe = []
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        for sd in range(a, z + 1):
            if parte == "g2": giri = [[c] * 3 for c in C]
            else:
                import random; r = random.Random(sd); m = C[:]; r.shuffle(m); giri = [m]
            for cs in giri:
                ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
                await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(150)
                r = await pg.evaluate(CORRI, [sd, cs, lungo]); await ctx.close()
                r.update(seme=sd, cs=cs, errori=errs); righe.append(r)
                print(sd, cs, [None if f is None else round(f) for f in r["fin"]], errs, flush=True)
        await b.close()
    f = OUT / f"bravura-{parte}-{a}-{BR}{'' if lungo else '-corte'}.json"; f.write_text(json.dumps(righe)); print("scritto", f)
def leggi(files):
    g2 = []; g2b = []
    for f in files:
        for x in json.loads(open(f).read()): (g2 if len(set(x["cs"])) == 1 else g2b).append(x)
    if g2:
        perc = {}; nf = {c: 0 for c in C}; pos = {c: [] for c in C}
        for x in g2:
            c = x["cs"][0]; r = [f for f in x["fin"][1:] if f is not None]; nf[c] += 3 - len(r)
            if r: perc.setdefault(x["seme"], {})[c] = st.mean(r)
            me = x["fin"][0]; pos[c].append(1 + sum(1 for f in r if me is None or f < me))
        ok = [s for s, d in perc.items() if len(d) == 5]; m = {c: st.mean(perc[s][c] for s in ok) for c in C}
        print(f"G2 su {len(ok)} semi, {len(g2)} regate; tempo medio dei rivali {({c: round(v, 1) for c, v in m.items()})}; non arrivati {nf}; posto medio del pilota {({c: round(st.mean(v), 2) for c, v in pos.items()})}; errori {sum(len(x['errori']) for x in g2)}; lunghe {all(x['lungo'] for x in g2)}")
        d = (m[0] - m[100]) / m[0]; se = st.stdev((perc[s][0] - perc[s][100]) / perc[s][0] for s in ok) / math.sqrt(len(ok)) if len(ok) > 1 else 0
        print(f"   da 0 a 100: {d:+.2%} del tempo (errore standard {se:.2%}; soglia 2%); passi {[f'{(m[b] - m[a]) / m[a]:+.2%}' for a, b in zip(C, C[1:])]} (mai oltre +1%); a 50 {(m[0] - m[50]) / (m[0] - m[100]):.0%} della distanza (25-75%)")
    if g2b:
        cop = {}; vin = {c: 0 for c in C}; n = 0
        for x in g2b:
            t = dict(zip(x["cs"], x["fin"][1:])); n += 1; arr = [c for c in C if t[c] is not None]
            if arr: vin[min(arr, key=lambda c: t[c])] += 1
            for i, a in enumerate(C):
                for b in C[i + 1:]:
                    if t[a] is None and t[b] is None: continue
                    cop.setdefault(b - a, []).append(t[a] is None or (t[b] is not None and t[b] < t[a]))
        print(f"G2b su {n} regate a 6: il più bravo davanti per distanza {({k: f'{st.mean(v):.0%} ({len(v)})' for k, v in sorted(cop.items())})}; primo fra i rivali {vin}; errori {sum(len(x['errori']) for x in g2b)}")
        ordini = [sorted([c for c in x["cs"]], key=lambda c, x=x: dict(zip(x["cs"], x["fin"][1:]))[c] or 9e9) for x in g2b]
        def ll(beta): return sum(beta * o[i] / 100 - math.log(sum(math.exp(beta * c / 100) for c in o[i:])) for o in ordini for i in range(4))
        beta = max((k / 50 for k in range(-100, 400)), key=ll); z = sum(math.exp(beta * c / 100) for c in C)
        print(f"   G5 (modello del sorteggio, peso e^(beta*c/100)): beta {beta:.2f} cioè F = beta/0,2 = {beta / 0.2:.1f}; quota di primi attesa {({c: round(math.exp(beta * c / 100) / z, 2) for c in C})}, vista {({c: round(vin[c] / n, 2) for c in C})}")
if sys.argv[1] == "leggi": leggi(sys.argv[2:])
else: asyncio.run(misura(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), "--corte" not in sys.argv))
