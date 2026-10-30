# Collaudo della regola 21 (1.0.66, docs/PROPOSTA-REGOLA-21-2.md): 21.2 chi sconta lascia strada, 21.1 chi torna dietro la linea dopo la partenza anticipata lascia strada. Regata dei giri.
# Uso: .venv-collaudi/bin/python tests/collaudo_regola21.py [prove=30] [cartella di una copia di riferimento (1.0.65), per il confronto al bit delle altre regate]
# Parti: K1 la precedenza passa a chi non sconta; K2 con debito ma senza giri non cambia nulla; K3 a debito estinto si torna a 10-13; K4 contatto mentre sconta; M 21.1;
#        K5 il metro (si sconta davvero al momento del confronto); K6 quanto pesa (30 regate con la flotta, solo riportato con l'atteso); K7 altre regate identiche al bit; K8 registratore e pagina senza #collaudo.
import asyncio, pathlib, sys, os, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata dei giri con la flotta di principianti, pilota fino a 25 s; debito di due giri; poi si gira a mano finché si sta scontando (caso 'gira'), oppure si sta fermi (caso 'fermo'), oppure si fanno i due giri (caso 'finito')
PREP = """async (sv, caso, dir, seme) => {
  const dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  R.need = 0; R.done = 0; R.giroDir = 0; me.sconta = false; // partenza pulita: le colpe del pilota nei primi 25 s e le sue virate non devono confondere il caso (in K6 invece restano)
  giriDebito(); const gira = d => { sv.ctl.tiller = d; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); };
  if (caso === 'gira'){ let n = 0; while (!me.sconta && n++ < 60 * 25 && !sv.S.capsized) gira(dir); }
  if (caso === 'fermo'){ for (let k = 0; k < 60 * 3; k++){ sv.ctl.tiller = 0; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); } }
  if (caso === 'finito'){ let n = 0; while (R.done < R.need && n++ < 60 * 90 && !sv.S.capsized) gira(dir); }
  return me;
}"""
# la griglia: l'avversario 1 in 6 posizioni (sistema del vento) per 5 prue (mure diverse), 30 casi. Per ciascuno: chi cede e con quale regola; più la stessa cosa a flag azzerato (come sarebbe senza 21.2)
GRIGLIA = """(sv, flagFn) => {
  const R = sv.R, me = R.boats[0], ai = R.boats[1], out = []; const [wx, wy] = toWF(me.S.x, me.S.y);
  const pos = [[3, 0], [-3, 0], [0, 3], [0, -3], [2.5, 2.5], [-2.5, -2.5]], prue = [45, -45, 100, -100, 170];
  for (const p of pos) for (const pr of prue){ const [x, y] = fromWF(wx + p[0], wy + p[1]); ai.S.x = x; ai.S.y = y; ai.S.h = norm360(env.twd + pr); ai.S.u = 3; ai.virando = false;
    ai.ocs = false; if (flagFn) flagFn(me, ai);
    const r = chiCede(me, ai); out.push({ cede: r.cede === me ? 'me' : 'ai', regola: r.regola, sconta: !!me.sconta, subA: subordinata(me), subB: subordinata(ai) }); }
  return out;
}"""
CASO = """async ([caso, dir, seme]) => { const sv = __sv; const prep = %s; const gr = %s; const me = await prep(sv, caso, dir, seme); const R = sv.R;
  const con = gr(sv, null); const sc0 = me.sconta; me.sconta = false; const senza = gr(sv, null); me.sconta = sc0;
  return { con, senza, need: R.need, done: R.done, sconta: !!me.sconta }; }""" % (PREP, GRIGLIA)
CASO21_1 = """async ([quale, seme]) => { const sv = __sv; const prep = %s; const gr = %s; const me = await prep(sv, quale === 'sconta_e_ocs' ? 'gira' : 'fermo', 1, seme); const R = sv.R;
  const flag = { ai: (m, a) => { a.ocs = true; m.ocs = false; }, entrambe: (m, a) => { a.ocs = true; m.ocs = true; }, io: (m, a) => { a.ocs = false; m.ocs = true; }, sconta_e_ocs: (m, a) => { a.ocs = true; m.ocs = false; } }[quale];
  const pre = me.sconta; me.sconta = quale === 'sconta_e_ocs' ? true : false; const con = gr(sv, flag); me.sconta = false; const base = gr(sv, (m, a) => { a.ocs = false; m.ocs = false; }); me.sconta = pre; me.ocs = false;
  return { con, base }; }""" % (PREP, GRIGLIA)
CONTATTO = """async ([lato, seme]) => { const sv = __sv; const prep = %s; const me = await prep(sv, 'gira', 1, seme); const R = sv.R, o = R.boats[1];
  const dt = 1 / 60; const need0 = R.need, pen0 = me.pen, l0 = R.penList.length, scont = me.sconta; o.S.h = sv.S.h; o.S.u = sv.S.u; o.S.x = sv.S.x + lato; o.S.y = sv.S.y;
  for (let k = 0; k < 3; k++){ sv.ctl.tiller = 1; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); }
  return { inc: R.need - need0, scont, voci: R.penList.slice(l0), regola: R.lastRule }; }""" % PREP
PESO = """async ([seme, dir]) => { const sv = __sv; const dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); } const l0 = R.penList.length, need0 = R.need; giriDebito(); const n0 = R.need, t0 = R.t; let cap = false;
  while (R.t < t0 + 90 && R.done < R.need && !cap){ sv.ctl.tiller = dir; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; }
  const mie = R.penList.slice(l0).filter(x => x.startsWith('Tu, contatto')).length, r21 = R.penList.slice(l0).filter(x => x.includes('regola 21')).length;
  return { estinto: R.done >= R.need, extra: R.need - n0, mie, r21, cap, t: R.t - t0, fine: me.fin }; }"""
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 3]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
REGISTRATA = """async ([seme]) => { const sv = __sv; const prep = %s; const me = await prep(sv, 'finito', 1, seme); const R = sv.R; sv.run(1 / 60, 120);
  return { done: R.done, need: R.need, live: ses.lines.join("\\n"), testo: regPezzi.length ? regPezzi.map(p => p.testo).join("\\n") : "" }; }""" % PREP
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        # ---- K1, K5 ----
        K1 = [await pg.evaluate(CASO, ["gira", 1 if k % 2 else -1, 100 + k]) for k in range(1, 5)]   # 4 prove di partenza diverse, ognuna con la griglia di 30 posizioni
        tot = sum(len(r["con"]) for r in K1); pass1 = sum(1 for r in K1 for c in r["con"] if c["cede"] == "me" and c["regola"] == 21.2)
        camb = sum(1 for r in K1 for c, s in zip(r["con"], r["senza"]) if s["cede"] == "ai")
        chk("K1 giocatore che sta scontando: in %d posizioni (%d partenze x 30) cede sempre lui con la regola 21.2 (%d su %d); in %d casi senza la 21.2 avrebbe ceduto l'altro (cioè è quello che cambia)" % (tot, len(K1), pass1, tot, camb), pass1 == tot and camb >= 10 * len(K1) // 3, "")
        chk("K5 il metro ha misurato davvero: in tutte le %d posizioni il giocatore stava scontando (flag acceso) e si era arrivati lì ruotando (debito aperto)" % tot, all(c["sconta"] for r in K1 for c in r["con"]) and all(r["need"] > r["done"] for r in K1))
        # ---- K2 ----
        K2 = [await pg.evaluate(CASO, ["fermo", 1, 200 + k]) for k in range(1, 5)]
        tot2 = sum(len(r["con"]) for r in K2)
        ok2 = all(not r["sconta"] and r["need"] > r["done"] for r in K2) and all(c["cede"] == s["cede"] and c["regola"] == s["regola"] and 10 <= c["regola"] <= 13 for r in K2 for c, s in zip(r["con"], r["senza"]))
        chk("K2 debito aperto ma senza girare: non si sta scontando e chiCede è quello di prima (regole 10-13) in tutte le %d posizioni" % tot2, ok2)
        # ---- K3 ----
        K3 = [await pg.evaluate(CASO, ["finito", 1 if k % 2 else -1, 300 + k]) for k in range(1, 5)]
        tot3 = sum(len(r["con"]) for r in K3)
        chk("K3 debito estinto: non si sconta più e valgono di nuovo le regole 10-13 in tutte le %d posizioni" % tot3, all(not r["sconta"] and r["done"] >= r["need"] for r in K3) and all(10 <= c["regola"] <= 13 for r in K3 for c in r["con"]), "estinti %d su %d" % (sum(1 for r in K3 if r["done"] >= r["need"]), len(K3)))
        # ---- K4 ----
        K4 = [await pg.evaluate(CONTATTO, [lato, 400 + k]) for lato in (1.2, -1.2) for k in range(1, 6)]
        chk("K4 contatto vero mentre il giocatore sconta: debito +2 e la regola 21.2 nel motivo (%d casi, di cui con colpa 21.2 %d)" % (len(K4), sum(1 for r in K4 if any("regola 21.2" in v for v in r["voci"]))), all(r["scont"] for r in K4) and all(r["inc"] == 2 and any("regola 21.2" in v for v in r["voci"]) for r in K4 if r["voci"]) and sum(1 for r in K4 if r["voci"]) >= 8, "incrementi: %s" % sorted({r["inc"] for r in K4}))
        # ---- M (21.1) ----
        M = {q: [await pg.evaluate(CASO21_1, [q, 500 + k]) for k in range(1, 4)] for q in ("ai", "entrambe", "io", "sconta_e_ocs")}
        ok = all(c["cede"] == "ai" and c["regola"] == 21.1 for r in M["ai"] for c in r["con"])
        chk("M1 un avversario oltre la linea dopo lo sparo (deve tornare) e il giocatore no: cede sempre l'avversario con la 21.1 (%d posizioni)" % sum(len(r["con"]) for r in M["ai"]), ok, "casi in cui prima avrebbe ceduto il giocatore: %d" % sum(1 for r in M["ai"] for c, s in zip(r["con"], r["base"]) if s["cede"] == "me"))
        chk("M2 il giocatore oltre la linea e l'avversario no: cede il giocatore con la 21.1 (%d posizioni)" % sum(len(r["con"]) for r in M["io"]), all(c["cede"] == "me" and c["regola"] == 21.1 for r in M["io"] for c in r["con"]))
        chk("M3 entrambe oltre la linea: la 21 non vale, tornano le regole 10-13 (%d posizioni)" % sum(len(r["con"]) for r in M["entrambe"]), all(10 <= c["regola"] <= 13 for r in M["entrambe"] for c in r["con"]))
        chk("M4 il giocatore che sconta e l'avversario che torna: nessuno è «quello che non lo fa», valgono le regole 10-13 (%d posizioni)" % sum(len(r["con"]) for r in M["sconta_e_ocs"]), all(10 <= c["regola"] <= 13 for r in M["sconta_e_ocs"] for c in r["con"]) and all(c["sconta"] for r in M["sconta_e_ocs"] for c in r["con"]))
        # ---- K6 ----
        nreg = int(os.environ.get("REGATE", "30"))
        K6 = [await pg.evaluate(PESO, [900 + k, 1 if k % 2 else -1]) for k in range(nreg)]
        est = sum(1 for r in K6 if r["estinto"]); ex = statistics.mean(r["extra"] for r in K6); mie = statistics.mean(r["mie"] for r in K6)
        print("     K6 (solo riportato, atteso nostro: almeno 24 su 30 estinti e meno di 0,5 giri in più): %d regate, debito estinto in %d, giri di debito in più in media %.2f (massimo %d), contatti con colpa del giocatore durante i giri in media %.2f, di cui regola 21: %d in tutto, scuffie %d" % (nreg, est, ex, max(r["extra"] for r in K6), mie, sum(r["r21"] for r in K6), sum(1 for r in K6 if r["cap"])), flush=True)
        chk("K6b il metro ha misurato davvero: in %d regate su %d il debito è partito da due giri e i giri sono stati tentati (almeno una rotazione, tempo > 5 s)" % (sum(1 for r in K6 if r["t"] > 5), nreg), all(r["t"] > 5 for r in K6))
        # ---- registratore ----
        G = await pg.evaluate(REGISTRATA, [700]); t = G["testo"] + G["live"]
        chk("K8a registratore: eventi «sconta inizio» e «sconta fine»", "sconta inizio" in t and "sconta fine" in t, "debito %d/%d" % (G["done"], G["need"]))
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- K7 ----
        ctx, pg, errs = await pagina(b, ROOT); nuovo = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
        if rif:
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); vecchio = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
            chk("K7 regate dell'1a e dell'1b: arrivi, penalità e posizioni finali identici al bit alla 1.0.65 su 20 regate", nuovo == vecchio and len(nuovo) == 20)
        else: print("     K7 saltato: manca la cartella di riferimento")
        # ---- K8 ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => ({ giri: R && R.giri, t21: motivoContatto({ regola: 21.2 }, R.boats[0]), t211: motivoContatto({ regola: 21.1 }, R.boats[1]) })")
        chk("K8b pagina senza #collaudo: la regata si apre e i motivi della 21.1 e 21.2 si leggono", h["giri"] and "scontando una penalità" in h["t21"] and "(regola 21.2)" in h["t21"] and "tornando dietro la linea" in h["t211"], h["t21"][:80])
        chk("K8c nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
