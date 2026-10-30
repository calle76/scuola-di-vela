# Collaudo della registrazione automatica delle regate (1.0.60, docs/PROPOSTA-COACH-REGISTRATORE.md, fase 1).
# Uso: .venv-collaudi/bin/python tests/collaudo_registrazione.py [regate=20] [cartella di una copia di riferimento senza registrazione automatica, per il confronto al bit e il costo]
# Parti: A) regate di fila col pilota (un file per regata, pre-via, 10 al secondo, pezzi, riga di controllo, marcatori); B) regate lunghe lasciate a metà (pezzi da 300 s, «interrotto»);
#        C) registrazione a mano: ha la precedenza; D) pagina come la carica un giocatore (senza #collaudo): parte da sola, si salva, si ricarica e si scarica.
import asyncio, json, pathlib, sys, os, re, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# n regate di fila (regate 0, 1, 2 a rotazione); a 30, 60 e 90 s si preme M tante volte quanto dice j % 3 + 1 (a 30 s una, a 60 s la seconda, a 90 s la terza)
CORRI = """async ([n, seme0, conReg, spegni]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 3]);
    const R = sv.R, me = R.boats[0]; if (spegni) sesAutoR = R; /* finta: la registrazione automatica crede di aver già registrato questa regata */ const vecchi = conReg ? regPezzi.map(p => p.id) : [], premi = j % 3 + 1, fatti = new Set();
    let np = 0, pos = null, t0 = performance.now();
    while (R.t < 1500 && me.fin === null && !me.dnf){
      sv.pilota(dt); sv.run(dt, 1); np++;
      for (const t of [30, 60, 90].slice(0, premi)) if (R.t >= t && !fatti.has(t)){ fatti.add(t); window.dispatchEvent(new KeyboardEvent("keydown", { key: "m" })); }
    }
    if (R.phase === "done") pos = sv.rank().findIndex(x => x.startsWith("Tu:")) + 1;
    const ms = performance.now() - t0;
    out.push({ j, fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]),
      ms, passi: np, tfin: R.t, premi, pos, nbarche: R.boats.length, finMe: me.fin === null ? null : me.fin.toFixed(1), penMe: me.pen || 0, ppMe: me.pp || 0, countdown: opt.countdown,
      pezzi: conReg ? regPezzi.filter(p => !vecchi.includes(p.id)).map(p => ({ n: p.n, fine: p.fine, testo: p.testo, reg: p.reg })) : [], autoOn: conReg ? ses.auto : null });
  }
  return out;
}"""
# regata lasciata a metà: la barca non governata, si va avanti fino a sec secondi di regata e poi si apre un'altra regata (Ricomincia)
META = """async ([sec, seme]) => {
  const sv = __sv, dt = 1 / 60; __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 0]);
  const R = sv.R, vecchi = regPezzi.map(p => p.id);
  while (R.t < sec){ sv.ctl.tiller = 0; sv.run(dt, 1); }
  const prima = ses.auto; sv.openItem(["r", 1]); sv.run(dt, 2);
  return { prima, dopo: ses.auto, pezzi: regPezzi.filter(p => !vecchi.includes(p.id)).map(p => ({ n: p.n, fine: p.fine, testo: p.testo, reg: p.reg })) };
}"""
MANO = """async (primaDelVia) => {
  const sv = __sv, dt = 1 / 60, on = () => { const c = document.getElementById('sesOn'); c.checked = true; c.dispatchEvent(new Event('change')); };
  __seed(77); sv.simTime = 0; sv.fast(0);
  if (primaDelVia) on();
  sv.openItem(["r", 0]); const R = sv.R, vecchi = regPezzi.map(p => p.id);
  while (R.t < -150){ sv.run(dt, 1); }
  const a = ses.auto, o1 = ses.on;
  if (!primaDelVia) on();
  while (R.t < -100){ sv.run(dt, 1); }
  return { autoPrima: a, onPrima: o1, autoDopo: ses.auto, onDopo: ses.on, righe: ses.lines.length, haRegata: ses.lines.some(l => / registrazione_automatica/.test(l)),
    nuovi: regPezzi.filter(p => !vecchi.includes(p.id)).map(p => ({ n: p.n, fine: p.fine })) };
}"""
# costo (metodo del 29 ottobre 2026, secondo tentativo: i rapporti per coppia variavano da −5% a +37% sulla stessa regata): stessa regata e stesso seme in ogni corsa, 20 ripetizioni per modalità (erano 10: un giro di Ale del 30 ottobre diede +8,4% con la macchina occupata, altre 5 misure da 0,0% a +2,2%) alternate nella stessa pagina, rapporto fra le mediane; «spenta» = la registrazione automatica crede di aver già registrato quella regata (sesAutoR = R)
COSTO = """async ([giri]) => { const sv = __sv, dt = 1 / 60, out = [];
  for (let g = 0; g < giri; g++){ const c = {};
    for (const modo of (g % 2 ? ["on", "off"] : ["off", "on"])){
      __seed(300); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 0]); const R = sv.R, me = R.boats[0];
      if (modo === "off") sesAutoR = R;
      const t0 = performance.now(); let n = 0;
      while (R.t < 200 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); n++; }
      c[modo] = (performance.now() - t0) / n * 1000; }
    out.push(c); }
  return out; }"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
def righe(testo, tipo): return [l.split(" ") for l in testo.split("\n") if l.startswith(tipo + " ")]
async def pagina(b, hash_="#collaudo", ctx=None):
    ctx = ctx or await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto((ROOT / "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def def_ref(b, base):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(250)
    return ctx, pg, errs
async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    rif = sys.argv[2] if len(sys.argv) > 2 else None
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        # ---- A ----
        ctx, pg, errs = await pagina(b)
        A = await pg.evaluate(CORRI, [n, 100, True])
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        chk("A1 20 regate di fila: ognuna ha il suo file (pezzi 1..k, l'ultimo «ultimo»), una sola apertura, nessun byte della regata prima", all(
            [p["n"] for p in r["pezzi"]] == list(range(1, len(r["pezzi"]) + 1)) and r["pezzi"] and r["pezzi"][-1]["fine"] == "ultimo" and all(p["fine"] == "" for p in r["pezzi"][:-1])
            and len({p["reg"] for p in r["pezzi"]}) == 1 and sum(p["testo"].count(" registrazione_automatica") for p in r["pezzi"]) == 1 for r in A), "regate %d, pezzi per regata: %s" % (len(A), [len(r["pezzi"]) for r in A]))
        reg_ids = [r["pezzi"][0]["reg"] for r in A if r["pezzi"]]
        chk("A2 ogni regata è distinta dalla precedente (identificatori diversi, nessuna riga F della regata prima)", len(set(reg_ids)) == len(A), "")
        pre, rate, ovl, tag, fcount, fpos, ffin, mm = [], [], [], [], [], [], [], []
        pesi = []
        for r in A:
            pz = r["pezzi"]; testo = "\n".join(p["testo"] for p in pz)
            S1 = righe(pz[0]["testo"], "S"); B1 = righe(pz[0]["testo"], "B")
            t0 = float(S1[0][1]) if S1 else 99; pre.append((t0 <= -r["countdown"] + 0.2, any(float(x[1]) < 0 for x in B1)))
            ts = [float(x[1]) for x in S1]; d = [round(b2 - a2, 3) for a2, b2 in zip(ts, ts[1:])]; rate.append(sum(1 for x in d if 0.09 <= x <= 0.11) / max(1, len(d)))
            for a, c in zip(pz, pz[1:]):
                Sa, Sc = righe(a["testo"], "S"), righe(c["testo"], "S"); ovl.append(Sa[-1] == Sc[0])
            tt = [(re.search(r"da t=(-?[\d.]+) a t=(-?[\d.]+)", p["testo"])) for p in pz]
            tag.append(all(abs(float(x.group(2)) - (120 + 300 * i)) <= 0.1 for i, x in enumerate(tt[:-1])) and all(float(a.group(2)) <= float(c.group(1)) + 0.1 for a, c in zip(tt, tt[1:])))
            F = righe(pz[-1]["testo"], "F"); fcount.append(len(F) == r["nbarche"])
            me = [x for x in F if x[2] == "Tu"]; fpos.append(bool(me) and int(me[0][3]) == r["pos"]); ffin.append(bool(me) and me[0][4] == r["finMe"] and int(me[0][5]) == r["penMe"] and int(me[0][6]) == r["ppMe"])
            m = [x for x in testo.split("\n") if x.startswith("M ")]; mm.append(len(m) == r["premi"] and [int(x.split(" ")[2]) for x in m] == list(range(1, r["premi"] + 1)))
            pesi += [len(p["testo"].encode("utf-8")) for p in pz]
        chk("A3 il file parte col conto alla rovescia (prima riga S a −%s s) e ci sono righe B col tempo negativo" % A[0]["countdown"], all(a and b2 for a, b2 in pre))
        chk("A4 righe S a 10 al secondo (tutte a 0,10 ± 0,01 s, salvo la giuntura del pezzo)", min(rate) >= 0.995, "minimo %.3f" % min(rate))
        chk("A5 un fotogramma in comune fra un pezzo e il successivo (%d giunture)" % len(ovl), len(ovl) > 0 and all(ovl))
        chk("A6 il primo pezzo chiude a 120 s di regata, gli altri ogni 300 s", all(tag))
        chk("A7 riga di controllo: una F per barca, posto del giocatore uguale a quello del gioco, tempo e penalità uguali", all(fcount) and all(fpos) and all(ffin), "F %d/%d, posto %d/%d, tempo %d/%d" % (sum(fcount), n, sum(fpos), n, sum(ffin), n))
        chk("A8 marcatori M numerati da 1 per ogni regata (premuti 1, 2 o 3 volte)", all(mm))
        chk("A9 peso di un pezzo sotto 2 MB", max(pesi) < 2e6, "massimo %.2f MB, medio %.2f MB, regate lunghe %d-%d s, pezzi %d" % (max(pesi) / 1e6, statistics.mean(pesi) / 1e6, min(r["tfin"] for r in A), max(r["tfin"] for r in A), len(pesi)))
        chk("A10 registrazione chiusa all'arrivo (nessuna registrazione automatica ancora accesa)", all(r["autoOn"] is False for r in A))
        # ---- B ----
        B1 = await pg.evaluate(META, [700, 5]); pz = B1["pezzi"]
        chk("B1 regata lunga lasciata a 700 s: tre pezzi, l'ultimo «interrotto», chiusa da sola, e la regata dopo ne apre una nuova", B1["prima"] and B1["dopo"] and [p["n"] for p in pz] == [1, 2, 3] and pz[-1]["fine"] == "interrotto" and "registrazione_chiusa interrotta" in pz[-1]["testo"], str([(p["n"], p["fine"]) for p in pz]))
        tt = [re.search(r"da t=(-?[\d.]+) a t=(-?[\d.]+)", p["testo"]) for p in pz]
        chk("B2 estremi dei pezzi: 120 s, 420 s, 700 s", abs(float(tt[0].group(2)) - 120) <= .1 and abs(float(tt[1].group(2)) - 420) <= .1 and 699 <= float(tt[2].group(2)) <= 701, str([x.group(0) for x in tt]))
        r3 = await pg.evaluate("""() => { const per = {}; regPezzi.forEach(p => per[p.reg] = 1); return { regate: Object.keys(per).length, pezzi: regPezzi.length, opzioni: document.querySelector('#regBox select').options.length, g: document.getElementById('regGet').disabled }; }""")
        chk("B3 si tengono al massimo 5 regate (dopo %d + 1 + 1 aperte)" % n, r3["regate"] <= 5, str(r3))
        # ---- C ----
        for pre_via in (True, False):
            c = await pg.evaluate(MANO, pre_via)
            if pre_via: chk("C1 registrazione a mano accesa prima della regata: l'automatica non parte", c["onPrima"] and not c["autoPrima"] and not c["autoDopo"] and not c["haRegata"], str(c))
            else: chk("C2 registrazione a mano accesa a regata in corso: l'automatica si chiude («interrotto») e la mano parte da sé", c["autoPrima"] and c["onDopo"] and not c["autoDopo"] and not c["haRegata"] and any(x["fine"] == "interrotto" for x in c["nuovi"]), str(c))
            await pg.evaluate("() => { const c = document.getElementById('sesOn'); c.checked = false; c.dispatchEvent(new Event('change')); }")
        await ctx.close()
        # ---- D: pagina come la carica un giocatore, senza #collaudo, con ricarica ----
        ctx, pg, errs = await pagina(b, "")
        await pg.click("#menu [data-r='0']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(3500)
        d1 = await pg.evaluate("() => ({ auto: ses.auto, on: ses.on, righe: ses.lines.length, t: R.t })")
        chk("D1 pagina senza #collaudo: aperta la regata, la registrazione parte da sola e scrive", d1["auto"] and d1["on"] and d1["righe"] > 20, str(d1))
        await pg.evaluate("document.getElementById('toMenu').click()"); await pg.wait_for_timeout(600)
        d2 = await pg.evaluate("() => ({ auto: ses.auto, pezzi: regPezzi.map(p => [p.n, p.fine]) })")
        chk("D2 tornando al menu il pezzo si chiude («interrotto») e si salva", not d2["auto"] and d2["pezzi"] == [[1, "interrotto"]], str(d2))
        await pg.reload(); await pg.wait_for_timeout(600)
        d3 = await pg.evaluate("() => ({ pezzi: regPezzi.length, opz: document.querySelector('#regBox select').options.length, dis: document.getElementById('regGet').disabled })")
        chk("D3 dopo la ricarica il pezzo c'è ancora (IndexedDB) e si può scaricare", d3["pezzi"] == 1 and not d3["dis"], str(d3))
        await pg.click("#regOpen"); await pg.wait_for_timeout(200)
        async with pg.expect_download() as dl: await pg.click("#regGet")
        d = await dl.value; testo = pathlib.Path(await d.path()).read_text(encoding="utf-8")
        chk("D4 il file scaricato è un pezzo di formato 3 con righe S e B e chiude con «interrotta»", testo.startswith("# SCUOLA DI VELA - registrazione di regata, formato 3") and len(righe(testo, "S")) > 10 and len(righe(testo, "B")) > 10 and "registrazione_chiusa interrotta" in testo and d.suggested_filename.startswith("regata-"), d.suggested_filename)
        await pg.click("#regDel"); await pg.wait_for_timeout(300)
        d5 = await pg.evaluate("() => regPezzi.length"); await pg.reload(); await pg.wait_for_timeout(600); d6 = await pg.evaluate("() => regPezzi.length")
        chk("D5 «Cancella tutte» svuota la lista, anche dopo la ricarica", d5 == 0 and d6 == 0, "%d, %d" % (d5, d6))
        chk("D6 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    # ---- E: il gioco non cambia ----
    ugu = lambda N, V: len(N) == len(V) == n and all(a["fin"] == c["fin"] and a["pen"] == c["pen"] and a["pp"] == c["pp"] and a["fine"] == c["fine"] and a["passi"] == c["passi"] for a, c in zip(N, V))
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b); N = await pg.evaluate(CORRI, [n, 100, False, False]); await ctx.close()
        ctx, pg, errs = await pagina(b); V = await pg.evaluate(CORRI, [n, 100, False, True]); await ctx.close()
        chk("E1 stesso codice, registrazione accesa e spenta: arrivi, penalità, posizioni finali e passi identici al bit su %d regate" % n, ugu(N, V))
        if rif:
            ctx, pg, errs = await def_ref(b, rif); R0 = await pg.evaluate(CORRI, [n, 100, False, False]); await ctx.close()
            chk("E1r confronto con la copia senza registrazione automatica (%s): identico al bit su %d regate" % (rif, n), ugu(N, R0))
        await b.close()
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b); C = await pg.evaluate(COSTO, [20]); await ctx.close(); await b.close()
    on, off = statistics.median(c["on"] for c in C), statistics.median(c["off"] for c in C)
    chk("E2 passo di simulazione al massimo +3%%: mediane di %d corse per modalità, accesa %.0f µs, spenta %.0f µs per passo (%+.1f%%; minimi %.0f e %.0f µs, %+.1f%%)" % (
        len(C), on, off, 100 * (on / off - 1), min(c["on"] for c in C), min(c["off"] for c in C), 100 * (min(c["on"] for c in C) / min(c["off"] for c in C) - 1)), on <= off * 1.03)
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
