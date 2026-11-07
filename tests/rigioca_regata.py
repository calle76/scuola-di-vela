# Rigioca una regata registrata (docs/PROPOSTA-REGATE-VERE.md, parte A). Non è un collaudo. La barca del giocatore rifà la rotta del file, gli avversari guidano da soli con semi diversi; il risultato passa a scene_strane.py.
# Semplificazione dichiarata: la barca rigiocata non reagisce agli avversari e dopo un urto torna sulla rotta registrata. Conta che cosa fanno gli avversari, non dice chi vince.
# Le barche partono dai posti del file (i posti sorteggiati dal seme facevano nascere contatti che nella regata non potevano esserci).
# Si rifiuta se regata, vento o preparazione non si possono rifare uguali al file.
# DIAGNOSI=1: per ogni «cede ma si avvicina» (cede da 2 s, sotto 8,4 m) e ogni contatto di chi cedeva annota lo stato della barca che cede (cause possibili, lette nel codice).
# Uso: python tests/rigioca_regata.py PRIMO_SEME ULTIMO_SEME file.txt [altri pezzi...]     BROWSER=firefox per l'altro browser; RADICE=cartella per rigiocare su un altro codice
import asyncio, collections, json, math, os, pathlib, re, statistics, sys
from playwright.async_api import async_playwright
import scene_strane as ss
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
CORSA = """([race, seme, liv, cd, rotta, caratteri, tFine, posti, diag]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]);
  const c = document.getElementById("cdSel"); c.value = String(cd); c.dispatchEvent(new Event("change"));
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, dt = 1 / 60, me = R.boats[0]; let i = 0;
  for (const b of R.boats) if (!b.me && caratteri[b.name]) b.char = caratteri[b.name];
  for (const b of R.boats) if (!b.me && posti[b.name]){ const [x, y, h, u] = posti[b.name]; Object.assign(b.S, { x, y, h, u }); }
  const vento = sv.windAt(me.S.x, me.S.y).twd, tInizio = R.t, un = (a) => (a + 360) % 360;
  const ripetute = [], righe = []; let L = null, n = 0;
  const raccogli = () => { const X = sv.ses.lines; if (X !== L || X.length < n){ L = X; n = 0; } while (n < X.length) righe.push(X[n++]); };
  const metti = () => { while (i + 1 < rotta.length && rotta[i + 1][0] <= R.t) i++;
    const a = rotta[i], b = rotta[Math.min(i + 1, rotta.length - 1)], f = b[0] > a[0] ? Math.max(0, Math.min(1, (R.t - a[0]) / (b[0] - a[0]))) : 0, dh = ((b[3] - a[3] + 540) % 360) - 180;
    Object.assign(me.S, { x: a[1] + (b[1] - a[1]) * f, y: a[2] + (b[2] - a[2]) * f, h: un(a[3] + dh * f), u: a[4] + (b[4] - a[4]) * f, r: 0, capsized: false, heel: 0 }); };
  const D = [], ep = new Map(), storia = new Map(), dd = (a, b) => Math.hypot(a.S.x - b.S.x, a.S.y - b.S.y), ang = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
  let nPen = R.penList.length; const fr = new Map();
  const stato = (b, o, tipo) => { const e = ep.get(b), w = sv.windAt(b.S.x, b.S.y).twd, A = ang(w, b.S.h), so = storia.get(o) || [];
    const altre = R.boats.filter(x => x !== b && x !== o && x.fin === null && !x.S.capsized && dd(x, b) < 15).length;
    return { tipo, t: +R.t.toFixed(1), via: R.t >= 0, nome: b.name, con: o.me ? "Tu" : o.name, d: +dd(b, o).toFixed(1), durGioco: b.cedeDa == null ? null : +(R.t - b.cedeDa).toFixed(1), durVista: e ? +(R.t - e.t0).toFixed(1) : null,
      virando: !!b.virando, oVira: !!o.virando, abbrivio: !!b.abbrivio, piantata: A < 44 && b.S.u < 0.6, lenta: b.S.u < 1.6, giro: e ? +ang(b.S.h, e.h0).toFixed(0) : null, oGira: so.length ? +Math.max(...so.map(q => ang(o.S.h, q[1]))).toFixed(0) : 0, altre, A: +A.toFixed(0), u: +b.S.u.toFixed(2), uo: +o.S.u.toFixed(2), sconta: !!b.sconta }; };
  const vc = new Map(); let nVir = 0; // docs/PROPOSTA-COPPIE.md, K3: quante volte chi cede sceglie di virare (b.virCede)
  while (R.t < tFine){ metti(); sv.ctl.tiller = 0; sv.run(dt, 1); raccogli();
    for (const b of R.boats){ if (b.me) continue; if (b.virCede && !vc.get(b)) nVir++; vc.set(b, !!b.virCede); }
    if (!diag) continue;
    for (const b of R.boats){ if (b.me) continue; const k = fr.get(b) || { on: false, n: 0, lento: 0, conFreno: false, max: 0 };
      if (b.frena && !k.on) k.n++; k.on = !!b.frena;
      if (R.t >= 0 && b.fin === null && !b.S.capsized && b.S.u * 1.944 < 0.5){ k.lento += dt; k.conFreno = k.conFreno || !!b.frena; if (k.conFreno) k.max = Math.max(k.max, k.lento); } else { k.lento = 0; k.conFreno = false; }
      fr.set(b, k); }
    for (const b of R.boats){ const q = storia.get(b) || []; q.push([R.t, b.S.h]); while (q.length && R.t - q[0][0] > 5) q.shift(); storia.set(b, q); }
    for (const b of R.boats){ if (b.me) continue; const o = b.cedeA, e = ep.get(b);
      if (!o){ if (e && R.t - e.tl > 1) ep.delete(b); continue; }
      if (!e || e.o !== o || R.t - e.tl > 1) ep.set(b, { o, t0: R.t, h0: b.S.h, tl: R.t, segnata: false }); else e.tl = R.t;
      const f = ep.get(b); if (!f.segnata && R.t - f.t0 >= 2 && dd(b, o) < 8.4){ f.segnata = true; D.push(stato(b, o, "S1")); } }
    while (nPen < R.penList.length){ const m = R.penList[nPen++].match(/^La (\\w+), contatto con (te|la (\\w+))/); if (!m) continue;
      const b = R.boats.find(x => x.name === m[1]), o = m[2] === "te" ? me : R.boats.find(x => x.name === m[3]), e = ep.get(b);
      if (e && e.o === o) D.push(stato(b, o, "S3")); else D.push(stato(b, o, "S4")); } }
  return { D, virCede: nVir, frenate: [...fr.values()].reduce((a, k) => a + k.n, 0), fermaFreno: Math.max(0, ...[...fr.values()].map(k => +k.max.toFixed(1))), vento, tInizio, tFineSim: +R.t.toFixed(1), righe, finiti: R.boats.filter(b => !b.me && b.fin !== null).length }; }"""

def intestazione(righe):
    h = next((r for r in righe if r.startswith("# gioco")), ""); imp = next((r for r in righe if r.startswith("# impostazioni")), ""); bar = next((r for r in righe if r.startswith("# barche")), "")
    tit = re.search(r"regata «(.+?)»", h); ven = re.search(r"vento=(\d+)°", imp); liv = re.search(r"avversari=(\w+)", imp); raf = re.search(r"raffiche=(\d+)", imp)
    car = dict(re.findall(r"(\w+) \((\w+)\)", bar))
    return dict(gioco=h[:60], titolo=tit and tit.group(1), vento=ven and int(ven.group(1)), liv=liv and liv.group(1), raffiche=raf and int(raf.group(1)), caratteri=car)

async def main():
    a, z, files = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
    righe = [r for f in files for r in open(f, encoding="utf-8", errors="replace")]
    info = intestazione(righe); fot, cont, _ = ss.leggi(righe)
    rotta = [[t, f["Tu"]["x"], f["Tu"]["y"], f["Tu"]["h"], f["Tu"]["kn"] / 1.944] for t, f in fot.items() if "Tu" in f]
    venti = set(int(x) for r in righe if r.startswith("C ") for x in re.findall(r"vento=(\d+)°", r))
    cd = round(-rotta[0][0]); tFine = rotta[-1][0]
    primo = next(f for f in fot.values() if len(f) > 1)
    posti = {n: [b["x"], b["y"], b["h"], b["kn"] / 1.944] for n, b in primo.items() if n != "Tu"}
    print("file:", info, "| punti della rotta", len(rotta), "| preparazione", cd, "| fine", tFine, "| venti nel file", sorted(venti))
    if not info["titolo"] or info["vento"] is None or cd not in (60, 180, 300) or len(venti) > 1: print("RIFIUTATO: regata, vento o preparazione non si possono rifare"); sys.exit(2)
    SEME = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text().split('SEME = """')[1].split('"""')[0]
    titoli = ["Regata a bastone", "Regata nelle raffiche", "Regata nei salti di vento", "Regata con i giri di penalità"]
    race = titoli.index(info["titolo"]); esiti, errs = [], []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for seme in range(a, z + 1):
            pg = await br.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME)
            await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(150)
            r = await pg.evaluate(CORSA, [race, seme, info["liv"], cd, rotta, info["caratteri"], tFine, posti, bool(os.environ.get("DIAGNOSI"))]); await pg.close()
            if abs((r["vento"] - info["vento"] + 180) % 360 - 180) > 15: print(f"RIFIUTATO: vento nel gioco {r['vento']:.0f}, nel file {info['vento']}"); sys.exit(2)
            es, nf, nc, (t0, t1) = ss.scene(r["righe"]); f2, c2, _ = ss.leggi(r["righe"])
            # R4: fedeltà sugli stessi istanti, lontano dagli urti (5 s)
            urti = [c[0] for c in c2]; sc = []
            for t, x, y, h, u in rotta:
                g = f2.get(t) or f2.get(round(t, 2))
                if g is None:
                    v = min((k for k in (round(t + d / 100, 2) for d in range(-3, 4)) if k in f2 and "Tu" in f2[k]), key=lambda k: abs(k - t), default=None); g = f2.get(v) if v is not None else None
                if g and "Tu" in g and not any(abs(t - q) < 5 for q in urti): sc.append(math.hypot(g["Tu"]["x"] - x, g["Tu"]["y"] - y))
            esiti.append(dict(seme=seme, fot=nf, contatti=nc, conTu=sum("Tu" in c[1:] for c in c2), prima=sum(c[0] < 0 for c in c2), scene=dict(collections.Counter(e["s"] for e in es)), finiti=r["finiti"], virCede=r.get("virCede", 0), tFine=r["tFineSim"], scMed=statistics.median(sc) if sc else None, scMax=max(sc) if sc else None, nSc=len(sc), elenco=[[round(e["t"], 1), e["s"], e["testo"]] for e in es], diag=r["D"], frenate=r.get("frenate"), fermaFreno=r.get("fermaFreno")))
            print(json.dumps(esiti[-1], ensure_ascii=False), flush=True)
        await br.close()
    n = len(esiti); vere, _, nv, _ = ss.scene(righe); tot = collections.Counter(); pres = collections.Counter()
    for e in esiti:
        for s, k in e["scene"].items(): tot[s] += k; pres[s] += 1
    print(f"\n== {n} corse, errori della pagina {errs[:2]}; fotogrammi per corsa min {min(e['fot'] for e in esiti)}, file {len(fot)}")
    print(f"R4 fedeltà: confronti {min(e['nSc'] for e in esiti)}-{max(e['nSc'] for e in esiti)} per corsa, mediana massima {max(e['scMed'] for e in esiti if e['scMed'] is not None):.2f} m (soglia 0,3), massimo {max(e['scMax'] for e in esiti if e['scMax'] is not None):.2f} m (soglia 2)")
    print(f"contatti a corsa: {sum(e['contatti'] for e in esiti) / n:.2f} (con la barca di Ale {sum(e['conTu'] for e in esiti) / n:.2f}, prima del via {sum(e['prima'] for e in esiti) / n:.2f}); nel file {nv}, di cui prima del via {sum(c[0] < 0 for c in cont)}")
    print("avversari arrivati a fine rotta, media:", round(sum(e["finiti"] for e in esiti) / n, 2))
    for s in ss.NOMI: print(f"  {s} {ss.NOMI[s]}: nel file {sum(e['s'] == s for e in vere)} | rigioco {tot[s] / n:.2f} a corsa, presente in {pres[s]} corse su {n}")
    print("R5:", "valido" if n >= 40 and max(pres.values(), default=0) >= n / 2 else f"NON valido (presenza massima {max(pres.values(), default=0)} su {n})")
asyncio.run(main())
