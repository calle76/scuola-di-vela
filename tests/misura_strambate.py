# Misura delle strambate degli avversari con una barca vicina (7 novembre 2026, OSSERVAZIONI-GIOCANDO 92). Non è un collaudo: nessuna soglia.
# Strambata: cambio di mure con il vento da dietro (oltre 120° dal vento), dopo il via, barca non scuffiata e non arrivata.
# «Addosso»: prima della strambata non doveva cedere a una barca entro 30 m, subito dopo deve cederle (chiCede, la funzione del gioco).
# Per ognuna: distanza, distanza minima nei 10 s dopo, contatto con colpa sua entro 10 s, se è vicina alla propria boa o sta scontando giri.
# Controprova: con --file legge una regata registrata e cerca le stesse strambate (solo regola 10, dai segni di twa): deve trovare il caso di Ale.
# TIENE=1: il pilota è la guida degli avversari e si scansa all'ultimo anche con la precedenza; con TIENE=1, dopo una strambata addosso al giocatore, il giocatore tiene la rotta per 10 s, come chi ha ragione.
# Uso: python tests/misura_strambate.py PRIMO_SEME ULTIMO_SEME [regate, es. 0,1,2]     BROWSER=firefox per l'altro browser
#      python tests/misura_strambate.py --file regata.txt
import asyncio, json, os, pathlib, re, statistics, sys
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
FINESTRA, RAGGIO = 10, 30  # secondi e metri; il raggio è D_CEDE della guida
CORSA = """([race, seme, liv, FIN, RAG, TIENE]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, dt = 1 / 60, av = R.boats.filter(b => !b.me), attiva = o => o.fin === null && !o.dnf && !o.S.capsized;
  const twa = b => ((sv.windAt(b.S.x, b.S.y).twd - b.S.h) % 360 + 540) % 360 - 180;
  const dist = (a, b) => Math.hypot(a.S.x - b.S.x, a.S.y - b.S.y);
  const st = new Map(av.map(b => [b, { tk: 0, prima: new Map(), tUltima: -1e9 }]));
  const ev = [], contatti = []; let nPen = R.penList.length, totale = 0, ravvicinate = 0, tieneFino = -1e9;
  while (R.t < 900 && av.some(b => b.fin === null && !b.dnf)){
    // chi doveva cedere PRIMA del passo: serve a dire che cosa ha cambiato la strambata
    for (const b of av) if (attiva(b)){ const q = st.get(b); q.prima.clear(); for (const o of R.boats) if (o !== b && attiva(o) && dist(b, o) <= RAG) q.prima.set(o, sv.chiCede(b, o).cede === b); }
    if (R.t < tieneFino && R.boats[0].fin === null) sv.ctl.tiller = 0; else sv.pilota(dt);
    sv.run(dt, 1);
    for (const e of ev) if (R.t - e.t <= FIN && attiva(e.b) && attiva(e.o)) e.dMin = Math.min(e.dMin, dist(e.b, e.o));
    while (nPen < R.penList.length){ const m = R.penList[nPen++].match(/^(Tu|La (\\w+)), contatto con (te|la (\\w+))/); if (!m) continue;
      const g = m[1] === "Tu" ? R.boats[0] : R.boats.find(x => x.name === m[2]), a = m[3] === "te" ? R.boats[0] : R.boats.find(x => x.name === m[4]);
      const reg = +(R.penList[nPen - 1].match(/regola ([\\d.]+)/) || [0, 0])[1], q = st.get(g);
      contatti.push({ t: +R.t.toFixed(1), colpa: g.name, conGiocatore: a.me || g.me, regola: reg, dopoStrambata: !!q && R.t >= 0 && R.t - q.tUltima <= FIN });
      for (const e of ev) if (e.b === g && e.o === a && R.t - e.t <= FIN) e.contatto = true; }
    if (R.t < 0) { for (const b of av) st.get(b).tk = Math.sign(twa(b)) || st.get(b).tk; continue; }
    for (const b of av){ const q = st.get(b), a = twa(b), tk = Math.sign(a);
      if (!tk) continue; const cambio = q.tk && tk !== q.tk && Math.abs(a) > 120 && attiva(b); q.tk = tk; if (!cambio) continue;
      totale++; if (R.t - q.tUltima < 5) ravvicinate++; q.tUltima = R.t;
      const tg = sv.R.marks && b.leg >= 1 && b.leg <= R.marks.length ? R.marks[b.leg - 1] : null, dBoa = tg ? Math.hypot(tg.x - b.S.x, tg.y - b.S.y) : 1e9;
      for (const [o, cedevaPrima] of q.prima){ if (!attiva(o) || cedevaPrima || sv.chiCede(b, o).cede !== b) continue;
        if (TIENE && o.me) tieneFino = R.t + FIN;
        ev.push({ b, o, t: R.t, d: dist(b, o), dMin: dist(b, o), contatto: false, dBoa, sconta: !!b.sconta, cedeAltra: !!b.cedeA && b.cedeA !== o, regola: sv.chiCede(b, o).regola }); } }
  }
  return { giri: !!R.giri, tFine: +R.t.toFixed(0), totale, ravvicinate, contatti, eventi: ev.map(e => ({ nome: e.b.name, car: e.b.char, con: e.o.me ? "Tu" : e.o.name, t: +e.t.toFixed(1), d: +e.d.toFixed(1), dMin: +e.dMin.toFixed(1), contatto: e.contatto, boa: e.dBoa < 30, sconta: e.sconta, cedeAltra: e.cedeAltra, regola: e.regola })) }; }"""

def da_file(percorso):
    prec, ultimo, ev, cont = {}, {}, [], []
    tot = 0
    with open(percorso, encoding="utf-8") as f:
        for r in f:
            p = r.split()
            if not p: continue
            if p[0] == "S" and len(p) > 8 and p[1][0] in "-0123456789":
                t = float(p[1]); ultimo["Tu"] = dict(t=t, x=float(p[2]), y=float(p[3]), twa=float(p[7]), attiva=True)
            elif p[0] == "B" and len(p) > 9:
                t, n = float(p[1]), p[2]; stato = " ".join(p[9:]); twa = float(p[7])
                attiva = "arr" not in stato and "dnf" not in stato and "scuf" not in stato
                ultimo[n] = dict(t=t, x=float(p[3]), y=float(p[4]), twa=twa, attiva=attiva)
                q = prec.get(n)
                if q is not None and q * twa < 0 and abs(twa) > 120 and attiva:
                    tot += 1
                    for o, v in ultimo.items():
                        if o == n or not v["attiva"] or abs(v["t"] - t) > 1: continue
                        d = ((v["x"] - float(p[3])) ** 2 + (v["y"] - float(p[4])) ** 2) ** .5
                        if d <= RAGGIO and twa < 0 < v["twa"]:  # ora è mure a sinistra e l'altra mure a dritta: regola 10, prima (stesse mure) poteva non cedere
                            ev.append(dict(nome=n, con=o, t=t, d=round(d, 1)))
                prec[n] = twa
            elif p[0] == "E" and "contatto_barche" in r:
                cont.append(r.strip())
            elif p[0] == "Q":
                cont.append(r.strip())
    print(f"strambate nel file: {tot}; con cambio a mure a sinistra e barca mure a dritta entro {RAGGIO} m: {len(ev)}")
    for e in ev:
        vicini = [c for c in cont if c.split()[0] == "Q" and 0 <= float(c.split()[1]) - e["t"] <= FINESTRA]
        print(f"  t={e['t']:.1f} {e['nome']} verso {e['con']} a {e['d']} m" + (" -> " + vicini[0][:110] if vicini else ""))
    print("voci di penalità nel file:", sum(c.startswith("Q") for c in cont))

def riepilogo(righe):
    ev = [e for r in righe for e in r["eventi"]]; tot = sum(r["totale"] for r in righe)
    # una strambata può diventare «addosso» a due barche insieme: gli eventi sono coppie barca-barca
    con = [e for e in ev if e["contatto"]]; cont = [c for r in righe for c in r["contatti"] if c["t"] >= 0]
    pre = sum(c["t"] < 0 for r in righe for c in r["contatti"])
    print(f"\n== regate {len(righe)}, avversari {3 * len(righe)}, giri di penalità in queste regate: {sorted(set(r['giri'] for r in righe))}")
    print(f"strambate dopo il via: {tot} (ravvicinate meno di 5 s: {sum(r['ravvicinate'] for r in righe)})")
    print(f"strambate «addosso» (coppie barca-barca, entro {RAGGIO} m): {len(ev)}, cioè {len(ev) / max(tot, 1):.1%} delle strambate; {len(ev) / len(righe):.2f} a regata")
    for lo, hi in ((0, 10), (10, 20), (20, 30.01)):
        f = [e for e in ev if lo <= e["d"] < hi]
        print(f"  da {lo} a {int(hi)} m: {len(f)} | finite in contatto: {sum(e['contatto'] for e in f)} | scese sotto 2 lunghezze (8,4 m centri): {sum(e['dMin'] < 8.4 for e in f)}")
    print(f"  di cui vicino alla propria boa (30 m): {sum(e['boa'] for e in ev)}, con contatto {sum(e['boa'] and e['contatto'] for e in ev)}")
    print(f"  di cui mentre sconta giri: {sum(e['sconta'] for e in ev)}; mentre cedeva a un'altra barca: {sum(e['cedeAltra'] for e in ev)}")
    print(f"  con il giocatore: {sum(e['con'] == 'Tu' for e in ev)}, con contatto {sum(e['con'] == 'Tu' and e['contatto'] for e in ev)}")
    for car in sorted(set(e["car"] for e in ev)):
        f = [e for e in ev if e["car"] == car]; print(f"  carattere {car}: {len(f)}, con contatto {sum(e['contatto'] for e in f)}")
    print(f"  regole di chi cede dopo: { {k: sum(e['regola'] == k for e in ev) for k in sorted(set(e['regola'] for e in ev))} }")
    colpa_av = [c for c in cont if c["colpa"] != "Tu" and c["colpa"] is not None]
    print(f"contatti dopo il via: {len(cont)} (prima del via: {pre}); con colpa di un avversario: {len(colpa_av)}")
    print(f"  contatti da una strambata «addosso» (coppia e 10 s): {len(con)}, cioè {len(con) / max(len(colpa_av), 1):.1%} dei contatti con colpa di un avversario dopo il via")
    print(f"  contatti con colpa di chi ha strambato da meno di 10 s, con chiunque: {sum(c['dopoStrambata'] for c in colpa_av)}")
    if ev: print(f"  distanza mediana alla strambata: {statistics.median(e['d'] for e in ev)} m")
    return con

async def main():
    from playwright.async_api import async_playwright
    a, b_ = int(sys.argv[1]), int(sys.argv[2]); reg = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "0,1,2").split(",")]
    SEME = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text().split('SEME = """')[1].split('"""')[0]
    righe, errs = [], []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for race in reg:
            for liv in ("principianti", "esperti"):
                for seme in range(a, b_ + 1):
                    pg = await br.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME)
                    await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(200)
                    r = await pg.evaluate(CORSA, [race, seme, liv, FINESTRA, RAGGIO, bool(os.environ.get("TIENE"))]); await pg.close()
                    r.update(race=race, liv=liv, seme=seme); righe.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        await br.close()
    print("errori della pagina:", errs[:2])
    riepilogo(righe)
    for race in reg:
        for liv in ("principianti", "esperti"):
            print(f"\n-- regata {race}, {liv}"); riepilogo([r for r in righe if r["race"] == race and r["liv"] == liv])

if len(sys.argv) > 2 and sys.argv[1] == "--file": da_file(sys.argv[2])
else: asyncio.run(main())
