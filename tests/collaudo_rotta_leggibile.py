# Collaudo della rotta ottimale più leggibile (1.2.32, docs/PROPOSTA-ROTTA-LEGGIBILE.md, criteri L1-L6 e L8).
# Le 4 regate del torneo (esperti, semi fissi), giocatore col pilota fino all'arrivo; poi «Rotta ottimale» dalla schermata finale:
#   L1 ogni filo unisce le due posizioni dello stesso istante, a minuto pieno (controllo indipendente, scarto <= 5 cm), almeno un filo per regata;
#   L2 i fili sono tanti quanti i minuti interi della rotta più corta; L3-L4 la barra laterale si nasconde e torna (B, pulsante, Esc, Chiudi);
#   L5 B non fa niente fuori dalla rotta ottimale; L6 0 px di eccesso a 1360x650, con e senza barra.
# Uso: python tests/collaudo_rotta_leggibile.py [--semi N] [--foto]   (BROWSER=firefox per Firefox; --giocatore: pagina senza #collaudo per L8)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
SEMI = int(sys.argv[sys.argv.index("--semi") + 1]) if "--semi" in sys.argv else 5
FOTO = "--foto" in sys.argv
CORSA = """([k, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'esperti'); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  T.regate[k] = { tws: seme % 2 ? 12 : 10, wind: (seme % 8) * 45 };
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60;
  while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }
  for (let j = 0; j < 30; j++) sv.run(dt, 1);
  return { fin: R.boats[0].fin, fase: R.phase, dbg: { finRot: document.getElementById('finRot').hidden, finOv: document.getElementById('finOv').hidden, rDone: document.getElementById('rDone').hidden, rotta: !!R.rotta, taglio: !!(sv.rot.barche[0] && sv.rot.barche[0].taglio), nriv: sv.riv.all.length, spento: sv.rot.spento }, rotVis: !document.getElementById('finRot').hidden && document.getElementById('finRot').offsetParent !== null };
}"""
MISURA = """() => { const lay = document.querySelector('.layout'), pan = document.querySelector('.panel'), cv = document.querySelector('canvas');
  const vis = e => !!e && e.offsetParent !== null && getComputedStyle(e).display !== 'none';
  return { larga: lay.classList.contains('largo'), barra: vis(pan), cw: Math.round(cv.getBoundingClientRect().width), win: innerWidth,
    ecc: Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0),
    bott: document.getElementById('movLargo').hidden ? null : document.getElementById('movLargo').textContent, riv: __sv.riv.on }; }"""
FILI = """() => { const F = __sv.rotFili(), all = __sv.riv.all, P = __sv.rot.res.ott.punti, t0 = __sv.rot.barche[0].taglio.t;
  // controllo indipendente: per ogni filo la posizione verde e blu all'istante del filo, interpolata qui fra i due punti vicini
  const qui = (A, T, xy) => { const i = A.findIndex(a => a.t >= T); if (i < 0) return null; if (i === 0) return xy(A[0]); const a = A[i - 1], b = A[i], f = (T - a.t) / (b.t - a.t), p = xy(a), q = xy(b); return [p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f]; };
  const tu = all.filter(f => f.t >= t0), corta = Math.min(P[P.length - 1].t - P[0].t, tu[tu.length - 1].t - P[0].t);
  let scarto = 0, istanti = 0;
  for (const f of F){ const T = P[0].t + f.s, v = qui(P, T, q => [q.x, q.y]), b = qui(tu, T, g => g.b[0]);
    scarto = Math.max(scarto, Math.hypot(v[0] - f.v.x, v[1] - f.v.y), Math.hypot(b[0] - f.b.x, b[1] - f.b.y));
    const r = f.s % 60; istanti = Math.max(istanti, Math.min(r, 60 - r)); } // a minuto pieno: tolleranza per gli arrotondamenti (179,99999999 s è il minuto 3)
  return { n: F.length, attesi: Math.floor(corta / 60 + 1e-9), scarto, istanti, lungh: F.map(f => Math.round(Math.hypot(f.v.x - f.b.x, f.v.y - f.b.y))) }; }"""

async def main():
    nome = os.environ.get("BROWSER", "chromium"); falli = []; righe = 0
    async with async_playwright() as p:
        br = await getattr(p, nome).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(500)
        for k in range(4):
            for seme in range(2301, 2301 + SEMI):
                r = await pg.evaluate(CORSA, [k, seme]); await pg.wait_for_timeout(500)
                r["rotVis"] = await pg.evaluate("() => { const b = document.getElementById('finRot'); return !b.hidden && b.offsetParent !== null; }")
                if not r["rotVis"]: falli.append(f"R{k+1} seme {seme}: pulsante Rotta ottimale non visibile ({r})"); continue
                prima = await pg.evaluate(MISURA)
                await pg.keyboard.press("b"); await pg.wait_for_timeout(50)
                l5 = await pg.evaluate(MISURA)  # L5: B fuori dalla rotta ottimale (schermata finale) non fa niente
                if l5["larga"] or not l5["barra"]: falli.append(f"R{k+1} {seme}: L5 B fuori dalla rotta ha nascosto la barra")
                await pg.click("#finRot"); await pg.wait_for_timeout(150)
                f = await pg.evaluate(FILI); righe += 1
                if f["n"] < 1: falli.append(f"R{k+1} {seme}: L1 nessun filo")
                if f["scarto"] > 0.05 or f["istanti"] > 1e-6: falli.append(f"R{k+1} {seme}: L1 estremi del filo lontani {f['scarto']:.3f} m dalla posizione allo stesso istante (o istante non a minuto pieno: {f['istanti']})")
                if f["n"] != f["attesi"]: falli.append(f"R{k+1} {seme}: L2 fili {f['n']} invece di {f['attesi']}")
                a = await pg.evaluate(MISURA)
                await pg.keyboard.press("b"); await pg.wait_for_timeout(150); b = await pg.evaluate(MISURA)
                if not b["larga"] or b["barra"] or abs(b["cw"] - b["win"]) > 1: falli.append(f"R{k+1} {seme}: L3 con B {b}")
                if FOTO and seme == 2301: await pg.screenshot(path=str(OUT / f"rotta_leggibile_{nome}_R{k+1}_larga.png"))
                await pg.keyboard.press("b"); await pg.wait_for_timeout(150); c = await pg.evaluate(MISURA)
                if c["larga"] or not c["barra"] or c["cw"] != a["cw"]: falli.append(f"R{k+1} {seme}: L4 B di nuovo {c} contro {a}")
                if FOTO and seme == 2301: await pg.screenshot(path=str(OUT / f"rotta_leggibile_{nome}_R{k+1}_barra.png"))
                await pg.click("#movLargo"); await pg.wait_for_timeout(150); d = await pg.evaluate(MISURA)
                if not d["larga"] or d["barra"]: falli.append(f"R{k+1} {seme}: L3 pulsante {d}")
                if max(a["ecc"], b["ecc"], d["ecc"]) > 0: falli.append(f"R{k+1} {seme}: L6 eccesso {a['ecc']}/{b['ecc']}/{d['ecc']} px")
                uscita = "Escape" if seme % 2 else "Chiudi"
                if uscita == "Escape": await pg.keyboard.press("Escape")
                else: await pg.click("#movEsc")
                await pg.wait_for_timeout(150); e = await pg.evaluate(MISURA)
                if e["larga"] or not e["barra"] or e["cw"] != prima["cw"] or e["riv"]: falli.append(f"R{k+1} {seme}: L4 dopo {uscita} {e} contro {prima}")
                print(f"  R{k+1} seme {seme}: fili {f['n']} (attesi {f['attesi']}), scarto {f['scarto']:.3f} m, lunghezze {f['lungh']} m; barra {a['cw']} -> {b['cw']} px, uscita {uscita}", flush=True)
        await br.close()
    if errs: falli.append(f"errori della pagina: {errs[:3]}")
    print(f"{nome}: {righe} regate con la rotta aperta; " + ("ESITO: OK" if not falli and righe else "FALLITO"))
    for x in falli: print("  ", x)
    sys.exit(0 if not falli and righe else 1)
asyncio.run(main())
