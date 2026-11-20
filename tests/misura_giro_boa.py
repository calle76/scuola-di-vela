# Misura della voce 50 (1.3.23, docs/PROPOSTA-ROTTA-GIRO-BOA.md, criteri R1-R4 scritti il 17 nov prima del codice): la rotta ottimale gira la boa come la gira il gioco?
# Il metro è quello del gioco: roundCheck (js/gioco.js, esposto in __sv) passato sui punti della rotta, lato per lato (dal cancello prima fino al primo punto dopo
# il cancello della boa), su ogni tratto diviso in 60 pezzi come i passi del gioco (coi soli punti a 1 s il metro perdeva i passaggi rasenti alla boa): giro valido = nessun -1 e somma +1. Ogni rotta si calcola due volte nella stessa regata: col controllo nuovo e con rot.giroLibero = true
# (com'era prima). Come nel gioco, il lato finisce appena la somma arriva a +1 (poi roundCheck guarda la boa dopo), così si vedono R2 (il metro vede il difetto) e R3-R4 (tempi prima/dopo).
# Torneo, principianti, 10 e 12 nodi, pilota sul giocatore, come tests/misura_lato_boa.py.
# Uso: python tests/misura_giro_boa.py PRIMO_SEME ULTIMO_SEME VENTO[,VENTO...]   (SALVA=file.json salva le uscite; RADICE=cartella per una copia del gioco)
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
JS = """([seme, wind, tws]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'principianti'); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; T.regate[0] = { tws, wind };
  sv.rot.spento = false; sv.rot.giroLibero = false; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60; R.tor = false;
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){ sv.pilota(dt); sv.run(dt, 1); }
  // il metro: per ogni boa, i punti del suo lato passati in roundCheck (un oggetto nuovo per lato, come o.rndA del gioco)
  const SUB = 60; // ogni tratto di 1 s diviso in 60 pezzi, come i passi del gioco: coi soli punti a 1 s l'angolo vicino alla boa salta oltre 90° e roundCheck non vede il passaggio (20 nov, prima prova)
  const giro = (rotta, marks) => marks.map((mk, k) => { const t0 = k ? rotta.lati[k - 1] : -1e9, t1 = rotta.lati[k], o = {}; let neg = 0, som = 0, dopo = false;
    let q = null;
    for (const p of rotta.punti){ if (p.t < t0 - 1e-6) continue; if (dopo) break; if (p.t > t1 + 1e-6) dopo = true;
      for (let j = q ? 1 : SUB; j <= SUB; j++){ const f = j / SUB, x = q ? q.x + (p.x - q.x) * f : p.x, y = q ? q.y + (p.y - q.y) * f : p.y;
        const r = sv.roundCheck(o, x, y, mk); if (r < 0) neg++; som += r; if (som >= 1) break; }
      if (som >= 1) break; q = p; }
    return [som, neg]; });
  const una = (f, marks) => { const out = {};
    for (const lib of [true, false]){ sv.rot.giroLibero = lib; const t0 = performance.now(), o = f(), ms = performance.now() - t0;
      out[lib ? "prima" : "dopo"] = o ? { tempo: o.tempo, ms, giro: giro(o, marks(o)) } : null; }
    sv.rot.giroLibero = true; return out; };   // 1.3.23: nel gioco il controllo è spento di base
  const mk0 = k => () => R.marks.slice(sv.rot.barche[k].taglio.leg - 1);
  const out = { marks: R.marks.length, fin0: R.boats[0].fin };
  out.mia = una(() => sv.rotCalcola(0), mk0(0));
  out.ass = una(() => sv.rotAssoluta(), () => R.marks);
  out.altre = R.boats.slice(1).map((b, i) => sv.rot.barche[i + 1] && sv.rot.barche[i + 1].taglio ? una(() => sv.rotCalcola(i + 1), mk0(i + 1)) : null);
  return out;
}"""
valido = lambda g: g is not None and all(s == 1 and n == 0 for s, n in g)
sbagliato = lambda g: g is not None and any(n > 0 for s, n in g)
toccata = lambda g: g is not None and not sbagliato(g) and not valido(g)   # 20 nov: seconda forma del difetto, non prevista dalla proposta: la rotta arriva sulla semiretta e torna indietro (somma 0 senza -1)
async def main(A, B, winds):
    res = []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for w in winds:
            for tws in (10, 12):
                for seme in range(A, B + 1):
                    r = await pg.evaluate(JS, [seme, w, tws]); r.update(w=w, tws=tws, seme=seme); res.append(r)
                    print(seme, w, tws, "mia", r["mia"]["dopo"] and r["mia"]["dopo"]["giro"], "prima", r["mia"]["prima"] and r["mia"]["prima"]["giro"], flush=True)
        await br.close()
    rotte = [(k, r, x) for r in res for k, x in [("mia", r["mia"]), ("ass", r["ass"])] + [("altra", a) for a in r["altre"] if a]]
    print(f"\n{len(res)} regate, {len(rotte)} rotte; errori della pagina {errs[:2]}")
    # R1: col controllo, tutte le rotte calcolate hanno il giro valido
    calc = [(k, r, x) for k, r, x in rotte if x["dopo"]]
    nonval = [(k, r["seme"], r["w"], r["tws"], x["dopo"]["giro"]) for k, r, x in calc if not valido(x["dopo"]["giro"])]
    print(f"R1 rotte col giro non valido, col controllo: {len(nonval)} su {len(calc)} calcolate (soglia 0; regate {len(res)}); non calcolate {len(rotte) - len(calc)}", nonval[:8])
    # R2: il metro vede il difetto senza controllo
    regMia = sum(1 for r in res if r["mia"]["prima"] and sbagliato(r["mia"]["prima"]["giro"]))
    regAny = sum(1 for r in res if any(x["prima"] and sbagliato(x["prima"]["giro"]) for k, rr, x in rotte if rr is r))
    regToc = sum(1 for r in res if any(x["prima"] and toccata(x["prima"]["giro"]) for k, rr, x in rotte if rr is r))
    print(f"R2 senza controllo: regate con la tua rotta sbagliata {regMia} su {len(res)}, con almeno una rotta sbagliata {regAny} su {len(res)}; con almeno una rotta «toccata e ritorno» {regToc} (soglia: almeno 15 su 90 in proporzione = {15 * len(res) / 90:.1f})")
    # R3: dove prima non c'era difetto, il tempo non cambia
    for nome, ks in (("giocatore e assoluta", ("mia", "ass")), ("altre barche", ("altra",))):
        d = [abs(x["dopo"]["tempo"] - x["prima"]["tempo"]) for k, r, x in rotte if k in ks and x["prima"] and x["dopo"] and valido(x["prima"]["giro"])]
        if d: print(f"R3 {nome}: rotte valide prima {len(d)}; entro 0,5 s {sum(v <= 0.5 for v in d)} ({100 * sum(v <= 0.5 for v in d) / len(d):.1f}%, soglia 95%), massimo {max(d):.2f} s (soglia 1,5)")
    # R4: quanto costava il difetto (solo numeri)
    for forma, test in (("sbagliate (un -1)", sbagliato), ("toccate e ritorno", toccata)):
      for nome, ks in (("giocatore", ("mia",)), ("assoluta", ("ass",)), ("altre barche", ("altra",))):
        d = [x["dopo"]["tempo"] - x["prima"]["tempo"] for k, r, x in rotte if k in ks and x["prima"] and x["dopo"] and test(x["prima"]["giro"])]
        tot = sum(1 for k, r, x in rotte if k in ks and x["prima"])
        if d: print(f"R4 {nome}, {forma}: {len(d)} rotte su {tot}; differenza dopo-prima mediana {statistics.median(d):+.1f} s, massimo {max(d):+.1f} s, minimo {min(d):+.1f} s")
        else: print(f"R4 {nome}, {forma}: nessuna su {tot}")
    persi = [(k, r["seme"], r["w"], r["tws"]) for k, r, x in rotte if x["prima"] and not x["dopo"]]
    print(f"rotte calcolate prima e non più dopo: {len(persi)}", persi[:6])
    ms = [(x["prima"]["ms"], x["dopo"]["ms"]) for k, r, x in rotte if x["prima"] and x["dopo"]]
    if ms: print(f"tempo di calcolo (somma): prima {sum(a for a, b in ms):.0f} ms, dopo {sum(b for a, b in ms):.0f} ms ({100 * (sum(b for a, b in ms) / max(1, sum(a for a, b in ms)) - 1):+.1f}%)")
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(res))
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), [int(x) for x in sys.argv[3].split(",")]))
