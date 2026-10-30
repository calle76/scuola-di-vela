# Collaudo della boa toccata (1.0.62, docs/PROPOSTA-LIVELLO-2A.md, fetta 2: regola 31, un giro). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_boa.py [prove=30] [cartella di una copia di riferimento (1.0.61), per il confronto al bit delle altre regate]
# Parti: A) tocco della boa del lato (e della linea d'arrivo): debito +1; B) a 0,5 m dal bordo niente; C) tocco continuato = un solo giro, poi allontanarsi e toccare = +1;
#        D) boe che non contano in quel momento; E) un giro basta; F) quanto tocca da solo il pilota; G) altre regate identiche al bit; H) registratore e pagina senza #collaudo.
import asyncio, pathlib, sys, os, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# regata dei giri senza avversari, pilota fino a 25 s; poi lo scafo viene messo a una distanza dal bordo (m) dall'oggetto scelto e si fanno 3 passi.
# lato = (leg, oggetto): oggetto "m0" boa 1, "pin", "cb". dist = distanza dal contorno dello scafo al centro dell'oggetto (0 = sopra).
PIAZZA = """(sv, ogg, dist, off) => { const R = sv.R, S = sv.S; const o = ogg === 'pin' ? R.pin : ogg === 'cb' ? R.cb : R.marks[0];
  S.h = 0; S.u = 0; let lo = 0, hi = 6; S.y = o.y; // si sposta lo scafo di lato (x) finché il contorno è alla distanza voluta
  if (dist <= 0){ S.x = o.x + off; S.y = o.y; return distScafoPunto(S, o.x, o.y); }
  for (let k = 0; k < 40; k++){ const m = (lo + hi) / 2; S.x = o.x + m; if (distScafoPunto(S, o.x, o.y) > dist) hi = m; else lo = m; } return distScafoPunto(S, o.x, o.y); }"""
SETUP = """(sv, seme, leg) => { const dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); } if (leg !== null){ me.leg = leg; me.prevWY = leg === 0 ? -1e3 : 1; } return me; }"""
PROVA = """async ([caso, seme, leg, ogg, dist]) => {
  const sv = __sv, dt = 1 / 60; const piazza = %s; const setup = %s; const me = setup(sv, seme, leg); const R = sv.R;
  const need0 = R.need, pen0 = me.pen, lista0 = R.penList.length; let d = piazza(sv, ogg, dist, 0.3 + (seme %% 5) * 0.1); const out = { dReale: d };
  const ferma = (n) => { for (let k = 0; k < n; k++){ sv.S.u = 0; piazza(sv, ogg, dist, 0.3); sv.ctl.tiller = 0; sv.run(dt, 1); } };
  if (caso === 'semplice') ferma(3);
  if (caso === 'continuo'){ ferma(300); out.dopoFermo = R.need - need0; piazza(sv, ogg, 8, 0); for (let k = 0; k < 120; k++){ sv.S.u = 0; sv.run(dt, 1); } out.dopoLontano = R.need - need0;
    piazza(sv, ogg, 0, 0.3); ferma(3); }
  if (caso === 'giro'){ ferma(3); out.dopoTocco = R.need - need0; sv.S.x = (ogg === 'pin' ? R.pin : ogg === 'cb' ? R.cb : R.marks[0]).x + 40; sv.S.y = (ogg === 'pin' ? R.pin : ogg === 'cb' ? R.cb : R.marks[0]).y; let cap = false; const t0 = R.t; sv.S.u = 3;
    while (R.t < t0 + 60 && R.done < R.need && !cap){ sv.ctl.tiller = 1; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; } out.cap = cap; out.done = R.done; }
  out.inc = R.need - need0; out.pen = me.pen - pen0; out.voci = R.penList.slice(lista0); out.regola = R.lastRule; out.nBoa = R.nBoa || 0; return out;
}""" % (PIAZZA, SETUP)
# il pilota tocca da solo? regata dei giri con la flotta, vento 10 nodi, fino all'arrivo del giocatore
SOLO = """async ([seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; let n = 0, primo = null;
  while (R.t < 1500 && me.fin === null && !me.dnf && n < 60 * 900){ sv.pilota(dt); sv.run(dt, 1); n++; if (primo === null && R.nBoa) primo = [Math.round(R.t), me.leg]; }
  return { nBoa: R.nBoa || 0, primo, chi: Object.keys(R.boaTocc || {}), fin: me.fin, voci: R.penList.filter(x => x.includes('regola 31')) };
}"""
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
REGISTRATA = """async ([seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  me.leg = 1; sv.S.h = 0; sv.S.u = 0; sv.S.x = R.marks[0].x + 0.3; sv.S.y = R.marks[0].y; for (let k = 0; k < 3; k++){ sv.S.u = 0; sv.run(dt, 1); }
  sv.run(dt, 120);
  return { nBoa: R.nBoa || 0, testo: regPezzi.length ? regPezzi.map(p => p.testo).join("\\n") : "", auto: ses.auto, testoLive: ses.lines.join("\\n") };
}"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def run(pg, caso, seme, leg, ogg, dist):
    return await pg.evaluate("async (a) => { return await (%s)(a); }" % PROVA.replace("__sv", "__sv"), [caso, seme, leg, ogg, dist])
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        semi = range(1, n + 1)
        # ---- A ----
        A = [await run(pg, "semplice", 100 + k, 1 if k % 2 else 2, "m0" if k % 2 else ("pin" if k % 4 == 0 else "cb"), 0) for k in semi]
        chk("A1 scafo sulla boa del lato (%d prove: boa 1 sul lato 1, linea d'arrivo sull'ultimo lato): il debito sale esattamente di 1, nessun +15 s" % n,
            all(r["inc"] == 1 and r["pen"] == 0 and r["nBoa"] == 1 for r in A) and len(A) == n, "incrementi: %s" % sorted({r["inc"] for r in A}))
        chk("A2 la voce nell'elenco e la riga delle regole citano la regola 31", all(any("regola 31" in v for v in r["voci"]) and "regola 31" in (r["regola"] or "") for r in A))
        # ---- B ----
        B = [await run(pg, "semplice", 200 + k, 1, "m0", 1.4) for k in semi]; B0 = [await run(pg, "semplice", 200 + k, 1, "m0", 0) for k in semi]
        chk("B1 a 0,5 m dal bordo della boa (%d prove, distanza scafo-centro 1,4 m con boa di 0,9 m: misurata fra 1,3 e 1,5): debito invariato; controllo: con tocco vero stesse prove +1 (%d su %d)" % (n, sum(1 for r in B0 if r["inc"] == 1), n),
            all(r["inc"] == 0 and 1.3 <= r["dReale"] <= 1.5 for r in B) and all(r["inc"] == 1 for r in B0))
        # ---- C ----
        C = [await run(pg, "continuo", 300 + k, 1, "m0", 0) for k in semi]
        chk("C1 scafo fermo sulla boa per 5 s: un solo giro (%d prove); allontanato oltre 3 m dal bordo, nessun giro nuovo; toccando di nuovo, +1 (totale 2)" % n,
            all(r["dopoFermo"] == 1 and r["dopoLontano"] == 1 and r["inc"] == 2 for r in C) and len(C) == n, "dopo 5 s: %s, dopo l'allontanamento: %s, totale: %s" % (sorted({r["dopoFermo"] for r in C}), sorted({r["dopoLontano"] for r in C}), sorted({r["inc"] for r in C})))
        # ---- D ----
        D1 = [await run(pg, "semplice", 400 + k, 1, "pin" if k % 2 else "cb", 0) for k in semi]
        D2 = [await run(pg, "semplice", 500 + k, 2, "m0", 0) for k in semi]
        D3 = [await run(pg, "semplice", 600 + k, 0, "m0", 0) for k in semi]
        chk("D1 sul lato 1 la linea non conta: tocco senza effetto (%d prove)" % n, all(r["inc"] == 0 for r in D1) and len(D1) == n)
        chk("D2 sull'ultimo lato la boa lasciata conta ancora (%d prove, +1)" % n, all(r["inc"] == 1 for r in D2) and len(D2) == n)
        chk("D3 prima del via la boa di bolina non conta (%d prove, 0)" % n, all(r["inc"] == 0 for r in D3) and len(D3) == n)
        # ---- E ----
        E = [await run(pg, "giro", 700 + k, 1, "m0", 0) for k in semi]
        chk("E1 dopo il tocco un giro estingue il debito (%d prove su %d, senza scuffie nel %d)" % (n, n, sum(1 for r in E if not r["cap"])), all(r["dopoTocco"] == 1 and r["inc"] == 1 and r["done"] >= 1 for r in E) and len(E) == n,
            "estinti %d su %d" % (sum(1 for r in E if r["done"] >= 1), n))
        # ---- F ----
        nreg = int(os.environ.get("REGATE", "60"))
        F = [await pg.evaluate(SOLO, [900 + k]) for k in range(nreg)]
        arr = [r for r in F if r["fin"] is not None]
        print("     F pilota di prova, %d regate con la flotta a 10 nodi: tocchi totali %d, regate con almeno un tocco %d (arrivate %d); tocchi per regata: %s; primo tocco (lato): %s" % (nreg, sum(r["nBoa"] for r in F), sum(1 for r in F if r["nBoa"]), len(arr), sorted({r["nBoa"] for r in F}), {l: sum(1 for r in F if r["primo"] and r["primo"][1] == l) for l in range(0, 4)}), flush=True)
        print("     F oggetti toccati (regate): %s; tempo del primo tocco (s di regata, negativo = prima del via): minimo %s, mediana %s, massimo %s" % ({k: sum(1 for r in F for v in r["voci"] if t in v) for k, t in (("spillo", "spillo"), ("comitato", "comitato"), ("boa 1", "toccato la boa:"))}, min((r["primo"][0] for r in F if r["primo"]), default=None), statistics.median([r["primo"][0] for r in F if r["primo"]] or [0]), max((r["primo"][0] for r in F if r["primo"]), default=None)), flush=True)
        chk("F0 il metro ha misurato davvero: tutte le regate hanno una nBoa numerica e %d su %d sono arrivate" % (len(arr), nreg), all(isinstance(r["nBoa"], int) for r in F) and len(arr) >= nreg * 0.9)
        # ---- H ----
        G = await pg.evaluate(REGISTRATA, [800])
        t = G["testo"] + G["testoLive"]
        chk("H1 registratore: evento boa_toccata nel file", G["nBoa"] == 1 and "boa_toccata" in t, "tocchi %d" % G["nBoa"])
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- G ----
        ctx, pg, errs = await pagina(b, ROOT); nuovo = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
        if rif:
            ctx, pg, errs = await pagina(b, pathlib.Path(rif)); vecchio = await pg.evaluate(ALTRE, [20, 100]); await ctx.close()
            chk("G1 regate dell'1a e dell'1b: arrivi, penalità e posizioni finali identici al bit alla 1.0.61 su 20 regate", nuovo == vecchio and len(nuovo) == 20)
        else: print("     G1 saltato: manca la cartella di riferimento")
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => ({ giri: R && R.giri, mode: mode })")
        chk("H2 pagina senza #collaudo: la regata dei giri si apre", h["giri"] and h["mode"] == "race", str(h))
        chk("H3 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
