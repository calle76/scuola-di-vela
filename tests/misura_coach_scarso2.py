# Seconda misura del consiglio «scarso, conviene virare» (voce 77, docs/PROPOSTA-COACH-SCARSO-VERIFICA.md, «Seconda misura»: K5, K5b, K6 scritti prima). Non cambia il gioco.
# Il metro dal punto della barca: per ogni consiglio «scarso» e per 10 momenti di bolina a caso per regata (lontano dalla boa, come il Coach), a regata finita si calcola la rotta ottimale
# (rotLato, isocrone sul vento registrato) dal punto, dall'istante e dalle mure della barca fino alla prossima boa, e si guarda se comincia con una virata entro 30 s.
# I momenti a caso sono presi a passo fisso fra i secondi di bolina registrati (nessun numero a caso consumato).
# Uso: python tests/misura_coach_scarso2.py SEME_DA SEME_A [regate per seme, default 3] > file.jsonl ; poi --somma file.jsonl ...
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
CORSA = """async ([k, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true; sv.opt.coachReg = true;
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push(T.av.concat([0]).map((x, i) => ({ fin: i + 1, pp: 0 })));
  sv.rot.spento = false; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, me = R.boats[0], dt = 1 / 60; R.tor = false; let n = 0, acc = 0; const cons = [], camp = [], kind = shiftSt ? shiftSt.kind : null;
  const stato = () => ({ t: R.t, x: me.S.x, y: me.S.y, h: me.S.h, leg: me.leg });
  while (R.t < 1500 && me.fin === null && !me.dnf){
    sv.pilota(dt); sv.run(dt, 1);
    const L = R.cr ? R.cr.log : [];
    while (n < L.length){ const c = L[n++]; if (/scarso/.test(c.testo)){ const w = sv.windAt(me.S.x, me.S.y); cons.push({ ...stato(), raffica: w.tws > env.tws * 1.12 }); } }
    if (me.leg >= 1 && (acc += dt) >= 1){ acc = 0; const w = sv.windAt(me.S.x, me.S.y), a = sv.norm180(w.twd - me.S.h), g = R.marks[me.leg - 1];
      if (Math.abs(a) >= 30 && Math.abs(a) <= 75 && !S.capsized && g && Math.hypot(g.x - me.S.x, g.y - me.S.y) > 80) camp.push({ ...stato(), sc: -Math.sign(a) * sv.norm180(w.twd - sv.envTwd()), raffica: w.tws > env.tws * 1.12 }); }
  }
  const caso = []; for (let i = 0; i < 10 && camp.length; i++) caso.push(camp[Math.floor((i + 0.5) * camp.length / 10)]);
  const prova = p => { if (p.leg < 1 || p.leg > R.marks.length) return null; const w = rotVento(p.x, p.y, rotRaffiche(p.t));
    const p0 = { x: p.x, y: p.y, t: p.t, s: sv.norm180(p.h - w.twd) < 0 ? 1 : -1 }; const q = rotLato(p0, rotCancBoa(R.marks[p.leg - 1])); if (!q) return null;
    const via = []; for (let r = q; r; r = r.par) via.push(r); via.reverse();
    return via.some(r => r.t <= p.t + 30 && r.s && r.s !== p0.s); };
  return { k, seme, kind, cons: cons.map(c => ({ raffica: c.raffica, vira: prova(c) })), caso: caso.map(c => ({ sc: c.sc, raffica: c.raffica, vira: prova(c) })) }; }"""
async def corri(a, b, nreg):
    async with async_playwright() as p:
        br = await getattr(p, BR).launch()
        for seme in range(a, b):
            for k in range(nreg):
                ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e))); await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                r = await pg.evaluate(CORSA, [k, seme]); r["errori"] = errs[:2]; print(json.dumps(r), flush=True); await ctx.close()
        await br.close()
def quota(L): L = [x for x in L if x is not None]; return (sum(L), len(L))
def somma(files):
    C = []; M = []; reg = 0; err = []; kinds = []
    for f in files:
        for l in open(f):
            if not l.startswith("{"): continue
            r = json.loads(l); reg += 1; err += r["errori"]; C += [dict(c, kind=r["kind"]) for c in r["cons"]]; M += r["caso"]
    def p(L): s, n = quota(L); return f"{s} su {n} ({100 * s / max(1, n):.0f}%)"
    nc = quota([c["vira"] for c in C]); nm = quota([m["vira"] for m in M])
    print(f"regate {reg}; consigli {len(C)} (calcolati {nc[1]}); momenti a caso {len(M)} (calcolati {nm[1]}); errori della pagina {err[:1]}")
    qc = nc[0] / max(1, nc[1]); qm = nm[0] / max(1, nm[1])
    print(f"K5 rotta ottimale dal punto della barca che vira entro 30 s: consigli {p([c['vira'] for c in C])}, momenti a caso {p([m['vira'] for m in M])}; differenza {100 * (qc - qm):+.0f} punti (soglia +10)")
    print(f"K5b momenti a caso con vento scarso: {p([m['vira'] for m in M if m['sc'] >= 7])}; buono: {p([m['vira'] for m in M if m['sc'] <= -7])}; in mezzo: {p([m['vira'] for m in M if -7 < m['sc'] < 7])}")
    print(f"   consigli in raffica {p([c['vira'] for c in C if c['raffica']])}, fuori raffica {p([c['vira'] for c in C if not c['raffica']])}; salto persistente {p([c['vira'] for c in C if c['kind'] == 'pers'])}, oscillante {p([c['vira'] for c in C if c['kind'] == 'osc'])}")
    print(f"K6 consigli calcolati {nc[1]} (soglia 100), momenti a caso calcolati {nm[1]} (soglia 500)")
if __name__ == "__main__":
    if sys.argv[1] == "--somma": somma(sys.argv[2:])
    else: asyncio.run(corri(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 3))
