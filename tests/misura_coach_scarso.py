# Misura del consiglio «scarso, conviene virare» del Coach (voce 77, docs/PROPOSTA-COACH-SCARSO-VERIFICA.md, criteri K1-K4 scritti prima). Non cambia il gioco.
# Regate lunghe del torneo col pilota sul giocatore (ricetta di collaudo_coach_regata: apertura e corsa in un evaluate, pagina nuova per regata).
# Per ogni consiglio «scarso»:
#   durata: secondi in cui, dopo il consiglio, il vento sulla barca resta girato dalla stessa parte di oltre 2° rispetto al vento medio (con le mure del momento del consiglio)
#   rotta ottimale: le mure della rotta ottimale (rotCalcola, isocrone; il Coach non la usa) cambiano fra t e t+30 s
#   salto: oscillante o persistente (shiftSt.kind); in raffica al momento del consiglio (vento sulla barca oltre 1,12 volte il medio)
# Moneta (aggiunta il 22 nov dopo la prima misura, su domanda di Ale: «se sbaglia il 50% si tira una moneta»): ogni secondo di bolina lontano dalla boa, se la rotta ottimale vira nei 30 s dopo,
#   in tutti i secondi, in quelli con vento scarso (>= 7°) e in quelli con vento buono (<= -7°): solo riportato, nessuna soglia.
# K1 durata >= 15 s in almeno il 75%; K2 rotta ottimale che vira entro 30 s in almeno il 60%; K3 riportato (persistenti, e quanti non seguiti); K4 almeno 100 consigli.
# Uso: python tests/misura_coach_scarso.py SEME_DA SEME_A [regate per seme, default 3] > file.jsonl   (BROWSER=firefox per Firefox); poi --somma file1.jsonl file2.jsonl ...
import asyncio, json, os, pathlib, statistics, sys
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
  const R = sv.R, me = R.boats[0], dt = 1 / 60; R.tor = false; let n = 0, acc = 0, camp = 0; const cons = [], campioni = [], kind = shiftSt ? shiftSt.kind : null;
  while (R.t < 1500 && me.fin === null && !me.dnf){
    sv.pilota(dt); sv.run(dt, 1);
    const L = R.cr ? R.cr.log : [];
    while (n < L.length){ const c = L[n++]; if (!/scarso/.test(c.testo)) continue;
      const w = sv.windAt(me.S.x, me.S.y), a = sv.norm180(w.twd - me.S.h);
      cons.push({ t: R.t, segno: -Math.sign(a), sc0: -Math.sign(a) * sv.norm180(w.twd - sv.envTwd()), raffica: w.tws > env.tws * 1.12, durata: null }); }
    if ((acc += dt) >= 0.25){ acc = 0; const w = sv.windAt(me.S.x, me.S.y);
      if (me.leg >= 1 && (camp += 0.25) >= 1){ camp = 0; const a2 = sv.norm180(w.twd - me.S.h), g = R.marks[me.leg - 1];
        if (Math.abs(a2) >= 30 && Math.abs(a2) <= 75 && !S.capsized && g && Math.hypot(g.x - me.S.x, g.y - me.S.y) > 80) campioni.push([R.t, -Math.sign(a2) * sv.norm180(w.twd - sv.envTwd())]); }
      for (const c of cons) if (c.durata === null){ const v = c.segno * sv.norm180(w.twd - sv.envTwd()); if (v <= 2 || R.t - c.t >= 180) c.durata = R.t - c.t; } }
  }
  for (const c of cons) if (c.durata === null) c.durata = R.t - c.t;
  const o = sv.rotCalcola(0); let vira = null;
  if (o){ const P = o.punti.filter(p => p.s); vira = cons.map(c => { let s0 = null; for (const p of P){ if (p.t <= c.t) s0 = p.s; else if (p.t <= c.t + 30 && s0 !== null && p.s !== s0) return true; else if (p.t > c.t + 30) break; } return false; }); }
  const P2 = o ? o.punti.filter(p => p.s) : [], virOtt = P2.filter((p, i) => i && p.s !== P2[i - 1].s).map(p => +p.t.toFixed(1));
  const base = { tutti: [0, 0], scarso: [0, 0], buono: [0, 0] };
  if (o) for (const [t, sc] of campioni){ const v = virOtt.some(x => x > t && x <= t + 30) ? 1 : 0; base.tutti[0]++; base.tutti[1] += v;
    if (sc >= 7){ base.scarso[0]++; base.scarso[1] += v; } else if (sc <= -7){ base.buono[0]++; base.buono[1] += v; } }
  return { k, seme, kind, fin: me.fin, cons, vira, ott: !!o, virOtt, base }; }"""
async def corri(a, b, nreg):
    async with async_playwright() as p:
        br = await getattr(p, BR).launch()
        for seme in range(a, b):
            for k in range(nreg):
                ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e))); await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                r = await pg.evaluate(CORSA, [k, seme]); r["errori"] = errs[:2]; print(json.dumps(r), flush=True); await ctx.close()
        await br.close()
def somma(files):
    global VO, BASE; VO = []; BASE = []; C = []; regate = 0; senza_ott = 0; errori = []
    for f in files:
        for l in open(f):
            if not l.startswith("{"): continue
            r = json.loads(l); VO.append(r.get("virOtt", [])); BASE.append(r.get("base") or {"tutti": [0, 0], "scarso": [0, 0], "buono": [0, 0]}); regate += 1; senza_ott += not r["ott"]; errori += r["errori"]
            for i, c in enumerate(r["cons"]): C.append({**c, "kind": r["kind"], "vira": r["vira"][i] if r["vira"] else None})
    n = len(C); d15 = sum(c["durata"] >= 15 for c in C); conV = [c for c in C if c["vira"] is not None]; v = sum(c["vira"] for c in conV)
    pers = [c for c in conV if c["kind"] == "pers"]; pv = sum(c["vira"] for c in pers)
    print(f"regate {regate} (rotta ottimale non calcolata in {senza_ott}), consigli {n}, errori della pagina {errori[:1]}")
    if not n: print("K4 FALLITO: nessun consiglio"); return
    print(f"K1 scarso durato 15 s o più: {d15} su {n} ({100 * d15 / n:.0f}%, soglia 75%) — durata mediana {statistics.median(c['durata'] for c in C):.1f} s")
    print(f"K2 rotta ottimale che vira entro 30 s: {v} su {len(conV)} ({100 * v / max(1, len(conV)):.0f}%, soglia 60%)")
    print(f"K3 consigli con salto persistente: {len(pers)}, non seguiti dalla rotta ottimale: {len(pers) - pv}; oscillante: {sum(c['kind'] == 'osc' for c in C)}; senza salto: {sum(c['kind'] is None for c in C)}; in raffica al momento del consiglio: {sum(c['raffica'] for c in C)}")
    for nome, G in (("in raffica", [c for c in conV if c["raffica"]]), ("fuori raffica", [c for c in conV if not c["raffica"]])):
        if G: print(f"   {nome}: {len(G)} consigli, durata >= 15 s {sum(c['durata'] >= 15 for c in G)}, rotta ottimale vira {sum(c['vira'] for c in G)}")
    print(f"K4 consigli contati: {n} (soglia 100)")
    B = {c: [0, 0] for c in ("tutti", "scarso", "buono")}
    for b in BASE:
        for c in B: B[c][0] += b[c][0]; B[c][1] += b[c][1]
    for c in B:
        if B[c][0]: print(f"   moneta: secondi di bolina «{c}» (scarso: almeno 7° contro, buono: almeno 7° a favore) {B[c][0]}, rotta ottimale che vira nei 30 s dopo {100 * B[c][1] / B[c][0]:.0f}%")
    print(f"   controllo del metro: virate della rotta ottimale per regata, mediana {statistics.median(len(r) for r in VO) if VO else 0}, regate con 0 virate {sum(not r for r in VO)}")
if __name__ == "__main__":
    if sys.argv[1] == "--somma": somma(sys.argv[2:])
    else: asyncio.run(corri(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 3))
