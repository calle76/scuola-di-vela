# Dove perdono tempo gli avversari (docs/PROPOSTA-AVVERSARI-ROTTA.md, 9 novembre 2026). Non è un collaudo: stampa i numeri.
# Le 4 regate del torneo (vento con raffiche e salti, 10 o 12 nodi secondo il seme), principianti ed esperti, preparazione 60 s, giocatore col pilota,
# fino all'arrivo di tutti o a 900 s. Per ogni avversario e ogni lato: tempo vero contro la rotta ottimale partita da dove e quando lui ha cominciato il
# lato (rotLatiBarca, js/rotta.js), virate vere contro cambi di mure della rotta ottimale; poi il ritardo al taglio della linea dopo il via.
# Uso: python tests/misura_avversari_rotta.py PRIMO ULTIMO   (DOWNE=gradi, DOWNE=off spento, assente = il gioco com'è; SCARSOAI e TMEDIA solo con la patch sperimentale/avversari-bolina-scarsi; LAYMARG come negli altri strumenti; SALVA=file.json, poi --riassumi f1 f2 ...)
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
CORSA = """([k, liv, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  if (sv.lay) sv.lay(LAYMARG); if (sv.down && DOWNE !== undefined) sv.down(DOWNE); if (sv.scarso && SCARSOAI !== undefined) sv.scarso(SCARSOAI, TMEDIA);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { tws: seme % 2 ? 12 : 10, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60; R.tor = false;
  const ai = R.boats.map((b, i) => i).filter(i => !R.boats[i].me), vir = {}, prev = {}, mure = {}, cambi = {}, scuf = {}, cap = {}, tocca = {};
  for (const i of ai){ vir[i] = []; prev[i] = false; cambi[i] = []; scuf[i] = 0; cap[i] = false; tocca[i] = new Set(); }
  let nPen = R.penList.length, contatti = 0;
  const dHull = (b, m) => { const P = sv.hullWorld(b.S); let dentro = true, best = 1e9;
    for (let i = 0; i < P.length; i++){ const [x0, y0] = P[i], [x1, y1] = P[(i + 1) % P.length], ex = x1 - x0, ey = y1 - y0, l2 = ex * ex + ey * ey;
      if (ex * (m.y - y0) - ey * (m.x - x0) < 0) dentro = false;
      const t = l2 > 1e-12 ? Math.max(0, Math.min(1, ((m.x - x0) * ex + (m.y - y0) * ey) / l2)) : 0; best = Math.min(best, Math.hypot(m.x - x0 - t * ex, m.y - y0 - t * ey)); }
    return dentro ? 0 : best; };
  while (R.t < 900 && R.boats.some(b => !b.me && b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1);
    if (R.penList.length > nPen){ for (let q = nPen; q < R.penList.length; q++) if (/contatto/.test(R.penList[q]) && R.t > 0) contatti++; nPen = R.penList.length; }
    if (R.t < 0) continue;
    for (const i of ai){ const b = R.boats[i], j = b.leg - 1; if (b.fin === null && j >= 0){ if (b.virando && !prev[i]) vir[i][j] = (vir[i][j] || 0) + 1;
        if (!b.S.capsized){ const m = Math.sign(sv.norm180(sv.windAt(b.S.x, b.S.y).twd - b.S.h)); if (m && mure[i] && m !== mure[i]) cambi[i][j] = (cambi[i][j] || 0) + 1; if (m) mure[i] = m; }
        if (b.S.capsized && !cap[i]) scuf[i]++; cap[i] = b.S.capsized;
        const mk = R.marks[Math.min(j, R.marks.length - 1)]; if (j < R.marks.length && Math.hypot(b.S.x - mk.x, b.S.y - mk.y) < 6 && dHull(b, mk) < 0.9) tocca[i].add(j); }
      prev[i] = b.virando; }
  }
  const barche = ai.map(i => ({ nome: R.boats[i].name, scuffiate: scuf[i], toccate: tocca[i].size, sbagliate: R.boats[i].wrongMarks || 0, taglio: sv.rot.barche[i].taglio ? sv.rot.barche[i].taglio.t : null, fin: R.boats[i].fin, dsq: !!R.boats[i].dsq,
    lati: sv.rotLatiBarca(i).map(L => ({ ...L, vir: vir[i][L.lato] || 0, cambi: cambi[i][L.lato] || 0 })) }));
  return { barche, contatti };
}"""

async def main(A, B):
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        tutte = []
        for k in range(4):
            for liv in ("principianti", "esperti"):
                for seme in range(A, B + 1):
                    r = await pg.evaluate(CORSA.replace("LAYMARG", os.environ.get("LAYMARG") or "null").replace("DOWNE", {"": "undefined", "off": "null"}.get(os.environ.get("DOWNE", ""), os.environ.get("DOWNE", ""))).replace("TMEDIA", os.environ.get("TMEDIA") or "0").replace("SCARSOAI", {"": "undefined", "off": "null"}.get(os.environ.get("SCARSOAI", ""), os.environ.get("SCARSOAI", ""))), [k, liv, seme])
                    tutte.append({"reg": k, "liv": liv, "seme": seme, "barche": r["barche"], "contatti": r["contatti"]})
            print(f"  regata {k + 1} fatta", flush=True)
        await br.close()
    d = {"regate": tutte, "errori": errs[:3], "down": os.environ.get("DOWNE"), "scarso": (os.environ.get("SCARSOAI") or "") + (" T_MEDIA " + os.environ["TMEDIA"] if os.environ.get("TMEDIA") else "")}
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(d))
    riassumi([d])

def riassumi(ds):
    R = [r for d in ds for r in d["regate"]]; E = [e for d in ds for e in d["errori"]]
    nome = lambda reg, j: ["bolina", "poppa"][j] if reg % 2 == 0 else ["bolina", "lasco 1", "lasco 2"][j]
    L = [(r["liv"], nome(r["reg"], x["lato"]), x) for r in R for b in r["barche"] for x in b["lati"]]
    print(f"{len(R)} regate, {sum(len(r['barche']) for r in R)} avversari, {len(L)} lati con la rotta ottimale; errori pagina {E}")
    tot = sum(x["vero"] - x["ott"] for _, _, x in L)
    for liv in ("principianti", "esperti", None):
        for tipo in ("bolina", "poppa", "lasco 1", "lasco 2"):
            g = [x for l, t, x in L if t == tipo and (liv is None or l == liv)]
            if not g: continue
            pers = [x["vero"] - x["ott"] for x in g]
            print(f"  {liv or 'tutti':12s} {tipo:8s}: lati {len(g):4d}, persi mediana {statistics.median(pers):5.1f} s ({statistics.median(p / x['ott'] for p, x in zip(pers, g)):5.1%}), "
                  f"media {statistics.mean(pers):5.1f} s, quota delle perdite {sum(pers) / tot:5.1%}; virate vere {statistics.mean(x['vir'] for x in g):.1f} contro {statistics.mean(x['manOtt'] for x in g):.1f} della rotta ottimale")
    ba = [b for r in R for b in r["barche"]]; fin = [b["fin"] for b in ba if b["fin"] is not None and not b["dsq"]]
    pop = [x for _, t, x in L if t == "poppa"]
    bol = [x for _, t, x in L if t == "bolina"]
    print(f"  SCARSO_AI {ds[0].get('scarso') or 'spento'}: B1 bolina persi mediana {statistics.median(x['vero'] - x['ott'] for x in bol):.2f} s; B3 virate per lato di bolina {statistics.mean(x['vir'] for x in bol):.2f}")
    print(f"  DOWN_E {ds[0].get('down') or 'come il gioco'}: Q1 poppa persi mediana {statistics.median(x['vero'] - x['ott'] for x in pop):.2f} s; Q2 arrivo mediano {statistics.median(fin):.1f} s; "
          f"Q3 contatti dopo il via {sum(r.get('contatti', 0) for r in R)}; Q4 cambi di mure per lato di poppa {statistics.mean(x.get('cambi', 0) for x in pop):.2f}; "
          f"Q5 scuffiate {sum(b.get('scuffiate', 0) for b in ba)}; Q6 boa toccata {sum(b.get('toccate', 0) for b in ba)}, sbagliate {sum(b.get('sbagliate', 0) for b in ba)}, non arrivate {sum(b['fin'] is None for b in ba)}")
    tg = [b["taglio"] for r in R for b in r["barche"] if b["taglio"] is not None]
    print(f"  partenza: taglio della linea dopo il via, mediana {statistics.median(tg):.1f} s, media {statistics.mean(tg):.1f} s, oltre 10 s {sum(t > 10 for t in tg)} su {len(tg)}")
    # le bolina che perdono di più: con quante virate
    bol = sorted([x for _, t, x in L if t == "bolina"], key=lambda x: x["vero"] - x["ott"])
    if bol:
        q = len(bol) // 4
        for nomeq, g in (("quarto migliore", bol[:q]), ("quarto peggiore", bol[-q:])):
            print(f"  bolina, {nomeq}: persi media {statistics.mean(x['vero'] - x['ott'] for x in g):.1f} s, virate vere {statistics.mean(x['vir'] for x in g):.1f}, della rotta ottimale {statistics.mean(x['manOtt'] for x in g):.1f}")

if sys.argv[1] == "--riassumi": riassumi([json.loads(pathlib.Path(f).read_text()) for f in sys.argv[2:]])
else: asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
