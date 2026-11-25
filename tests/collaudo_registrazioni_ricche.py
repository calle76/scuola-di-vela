# Collaudo delle registrazioni più ricche (1.3.46, voce 55, docs/PROPOSTA-REGISTRAZIONI-RICCHE.md; criteri G1-G5 scritti prima).
#   G1 la regata non cambia: stessi semi, regata lunga del torneo col pilota, arrivi e posizioni finali identici alla pagina di prima (--prima cartella con la 1.3.45)
#   G2 ogni cambio del semaforo visto dal collaudo (R.sem, R.semB) compare nel file, nello stesso ordine; almeno 20 cambi in tutto
#   G3 ogni contatto visto dal collaudo ha la sua riga contatto_barche con «colpa»; almeno 3 contatti in tutto
#   G4 dopo il proprio arrivo le righe continuano; ogni rivale arrivato entro 60 s ha avv_arrivo; chiusura «arrivo»
#   G5 peso: ogni pezzo al più 1 MB, il file intero al più 2,5 MB
# Uso: python tests/collaudo_registrazioni_ricche.py [--prima cartella_con_index.html]   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, sys, json
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BR = os.environ.get("BROWSER", "chromium")
PRIMA = sys.argv[sys.argv.index("--prima") + 1] if "--prima" in sys.argv else None
SEMI = range(1, 7)
CORSA = """async (seme) => { const sv = __sv, dt = 1 / 60; sv.fast(0); sv.lungo = true; window.confirm = () => true; sv.store = 'scuolaVelaSim.v1';
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  semina(); sv.torApri(); if (document.getElementById('torRit')){ document.getElementById('torRit').click(); sv.torApri(); } document.getElementById('torGo').click(); semina(); sv.simTime = 0;
  const R = sv.R, me = R.boats[0], semi = [], cont = [], vento = {}, rin = []; let lastSem, ct = {}; const pr = R.boats.map(b => [0, 0]);
  while (R.t < 1500 && !(R.phase === 'done' && (R.boats.every(b => b.fin !== null || b.dnf) || R.t - R.doneAt > 70))){
    const t0 = R.t; if (me.fin === null) sv.pilota(dt); sv.run(dt, 1); if (R.t === t0) break; /* regata ferma */
    const s = (R.sem || 'spento') + (R.sem && R.semB ? ' ' + regNome(R.semB) : ''); if (lastSem !== undefined && s !== lastSem) semi.push([R.t, s]); lastSem = s;
    vento[R.t.toFixed(2)] = R.boats.map(b => [regNome(b), +(sv.windAt(b.S.x, b.S.y).tws * 1.943844).toFixed(3)]);   /* H3: calcolato qui a ogni passo */
    R.boats.forEach((b, i) => { if (b.me) return; const v = b.rinvio || 0, p = b.rinvioVia || 0; if (v > pr[i][0]) rin.push([R.t, regNome(b) + ' virata ' + v]); if (p > pr[i][1]) rin.push([R.t, regNome(b) + ' partenza ' + p]); pr[i] = [v, p]; });   /* H2 */
    for (const k in R.contacts) if (ct[k] !== R.contacts[k]) cont.push(k); ct = Object.assign({}, R.contacts);
  }
  const fine = R.boats.map(b => [regNome(b), b.fin === null ? null : +b.fin.toFixed(3), Math.round(b.S.x * 1000), Math.round(b.S.y * 1000)]);
  const pezzi = regPezzi.filter(p => p.reg === Math.max(...regPezzi.map(q => q.reg))).sort((a, b) => a.n - b.n);
  const testo = pezzi.map(p => p.testo).join('\\n');
  return { fine, myFin: me.fin, semi, cont: cont.length, pesi: pezzi.map(p => p.testo.length), intero: testo.length, ev: testo.split('\\n').filter(l => /^E /.test(l)), rin, testo, righeV: testo.split('\\n').filter(l => /^V /.test(l)).map(l => { const p = l.split(' '), w = (vento[p[1]] || []).find(x => x[0] === p[2]); return [+p[1], p[2], +p[3], w ? w[1] : null]; }), righeD: testo.split('\\n').filter(l => /^D /.test(l)).map(l => l.split(' ').slice(2).join(' ')),
           ultimaT: Math.max(...testo.split('\\n').filter(l => /^S /.test(l)).map(l => +l.split(' ')[1])),
           riv: R.boats.filter(b => !b.me).map(b => [regNome(b), b.fin]) }; }"""
bad = []
def chk(ok, m):
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def corsa(b, base, seme, errs):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(base + "#collaudo"); await pg.wait_for_timeout(300)
    r = await pg.evaluate(CORSA, seme); await ctx.close(); return r
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []; out = {}
        for seme in SEMI: out[seme] = await corsa(b, (ROOT / "index.html").as_uri(), seme, errs)
        nsem = ok2 = nc = ok3 = n4 = ok4 = 0; mx = 0; mxi = 0
        for seme, r in out.items():
            fs = [e.split(" ", 3)[3] for e in r["ev"] if e.split(" ")[2] == "semaforo"]
            vis = [x for t, x in r["semi"] if t <= r["ultimaT"] + 0.1]  # dopo la chiusura del file il collaudo continua a guardare: quei cambi non ci sono (prima stesura del collaudo)
            nsem += len(vis); ok2 += vis == fs
            if vis != fs:
                i = next((k for k in range(min(len(vis), len(fs))) if vis[k] != fs[k]), min(len(vis), len(fs)))
                print(f"  seme {seme} semaforo: visti {len(vis)}, nel file {len(fs)}; primo diverso {i}: visto {vis[i-1:i+2]} file {fs[i-1:i+2]}", flush=True)
            cl = [e for e in r["ev"] if e.split(" ")[2] == "contatto_barche"]
            nc += r["cont"]; ok3 += len(cl) == r["cont"] and all(" colpa " in e for e in cl)
            chiusa = [e for e in r["ev"] if "registrazione_chiusa" in e]
            arr = {e.split(" ")[3] for e in r["ev"] if e.split(" ")[2] == "avv_arrivo"}
            dopo = [n for n, f in r["riv"] if f is not None and r["myFin"] is not None and f > r["myFin"] and f <= r["myFin"] + 60]
            tutti = all(f is not None and r["myFin"] is not None and f <= r["myFin"] for n, f in r["riv"])  # arrivato per ultimo: si chiude al proprio arrivo (prima stesura: pretendeva righe dopo anche qui)
            n4 += 1; ok4 += r["myFin"] is not None and (tutti or r["ultimaT"] > r["myFin"] + 1) and all(n in arr for n in dopo) and chiusa and chiusa[-1].endswith("arrivo")
            mx = max(mx, max(r["pesi"])); mxi = max(mxi, r["intero"])
            print(f"  seme {seme}: arrivo {r['myFin']}, ultima riga S {r['ultimaT']}, rivali arrivati dopo entro 60 s {dopo}, semaforo {len(r['semi'])} cambi visti, contatti {r['cont']}, pezzi {[round(x / 1024) for x in r['pesi']]} KB, chiusura {chiusa[-1:] }", flush=True)
        chk(ok2 == len(out) and nsem >= 20, f"G2 semaforo: file uguale al visto in {ok2} regate su {len(out)}, {nsem} cambi in tutto (almeno 20)")
        chk(ok3 == len(out) and nc >= 3, f"G3 contatti con la colpa: giusti in {ok3} regate su {len(out)}, {nc} contatti in tutto (almeno 3)")
        chk(ok4 == n4, f"G4 dopo l'arrivo: giusto in {ok4} regate su {n4}")
        chk(mx <= 1024 * 1024 and mxi <= 2.5 * 1024 * 1024, f"G5 peso: pezzo più grande {mx / 1024:.0f} KB (al più 1024), file intero più grande {mxi / 1024:.0f} KB (al più 2560)")
        # H2-H3 (1.3.57, seconda aggiunta della proposta): rinvii della 4B e vento dei rivali
        okD = nV = nP = 0; sbV = tv = 0; gap = 0.0
        for seme, r in out.items():
            vis = [x for t, x in r["rin"] if t <= r["ultimaT"] + 0.1]; okD += sorted(vis) == sorted(r["righeD"]) and len(vis) > 0
            if sorted(vis) != sorted(r["righeD"]): print(f"  seme {seme}: rinvii visti {len(vis)}, nel file {len(r['righeD'])}", flush=True)
            nV += sum(" virata " in x for x in vis); nP += sum(" partenza " in x for x in vis)
            ult = {}
            for t, n, f, w in r["righeV"]:
                tv += 1; sbV += w is None or abs(f - w) > 0.0501
                if n in ult: gap = max(gap, t - ult[n])
                ult[n] = t
        chk(okD == len(out) and nV >= 10 and nP >= 10, f"H2 rinvii: file uguale al visto in {okD} regate su {len(out)}; virate {nV}, partenze {nP} (almeno 10 e 10)")
        chk(tv >= 1000 and sbV == 0 and gap <= 1.5, f"H3 vento dei rivali: {tv} righe V (almeno 1000), diverse dal ricalcolo {sbV}, distanza massima {gap:.2f} s (al più 1,5)")
        # H5: i lettori vecchi danno la stessa uscita su un file con e senza le righe nuove
        if os.environ.get("H5_CARTELLA"):
            for seme, r in out.items():
                for nome, tieni in (("con", lambda l: True), ("senza", lambda l: not l.startswith(("V ", "D ")))):
                    d = pathlib.Path(os.environ["H5_CARTELLA"], nome); d.mkdir(parents=True, exist_ok=True)
                    (d / f"regata-2026112{seme}-1200-intera.txt").write_text("\n".join(l for l in r["testo"].split("\n") if tieni(l)))
        if PRIMA:
            base0 = pathlib.Path(PRIMA, "index.html").resolve().as_uri(); ug = 0
            for seme in SEMI:
                r0 = await corsa(b, base0, seme, errs)
                ug += r0["fine"] == out[seme]["fine"]
            chk(ug == len(out), f"G1 regata identica alla pagina di prima (arrivi e posizioni finali): {ug} su {len(out)}")
        else: print("  G1 non misurato: serve --prima cartella")
        chk(not errs, f"errori della pagina: {errs[:1]}")
        await b.close()
    print("casi sbagliati: " + ("nessuno" if not bad else str(len(bad))))
    raise SystemExit(1 if bad else 0)
asyncio.run(main())
