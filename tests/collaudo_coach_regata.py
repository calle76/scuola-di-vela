# Il Coach durante la regata (1.3.28, voce 65, docs/PROPOSTA-COACH-IN-REGATA.md, criteri P1-P7 scritti prima del codice). Regate lunghe del torneo col pilota sul giocatore.
#   P1 quanto parla: commenti per regata, mediana fra 4 e 12; nessuno a meno di 30 s dal precedente, tranne partenza anticipata e penalità
#   P2 dice il vero: ogni commento ricontrollato qui sullo stato della regata nell'istante in cui compare (chi copre, di quanti gradi è scarso, la posizione alla boa,
#      il distacco, le penalità, la partenza): 0 sbagliati, e quanti ne ha controllati per tipo
#   P3 non ripete i suggerimenti: nessun commento sullo stesso argomento di un suggerimento a schermo negli stessi 10 s (cono, scarso, penalità) — controllato sui messaggi del gioco
#   P4 spento è spento: stessa regata col Coach acceso e spento, arrivi e classifica identici; spento, 0 commenti
#   P5 non copre: il riquadro sta in alto a sinistra sul mare (dentro i 970 px del mare, nella metà alta), lontano dal centro dove sta la barca; pannello 0 px di eccesso
#   P6 costo: tempo della regata acceso contro spento (solo riportato: sul PC di Ale il rumore supera il 3% della soglia)
#   P7 pagina senza #collaudo: una regata di Deriva, Coach attivo e riga nelle impostazioni visibile; 0 errori
# Uso: python tests/collaudo_coach_regata.py [--semi N]   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, re, statistics as st, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
NS = int(sys.argv[sys.argv.index("--semi") + 1]) if "--semi" in sys.argv else 4
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
CORSA = """async ([k, seme, acceso]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true; sv.opt.coachReg = acceso;
  if (sv.tor){ sv.torApri(); const rit = document.getElementById('torRit'); if (rit) rit.click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push(T.av.concat([0]).map((x, i) => ({ fin: i + 1, pp: 0 })));
  sv.rot.spento = true; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, me = R.boats[0], dt = 1 / 60, snap = [], toasts = []; R.tor = false; let n = 0, prevNeed = R.need || 0, prevPp = 0, prevPen = 0, prevLeg = 0, t0 = performance.now();
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){
    const pn = R.need || 0, ppp = me.pp || 0, ppe = me.pen || 0, pl = me.leg;
    sv.pilota(dt); sv.run(dt, 1);
    const tt = sv.toast; if (tt && (!toasts.length || toasts[toasts.length - 1][1] !== tt)) toasts.push([R.t, tt]);
    const L = R.cr ? R.cr.log : [];
    while (n < L.length){ const c = L[n++], w = sv.windAt(me.S.x, me.S.y), a = sv.norm180(w.twd - me.S.h);
      const dav = R.boats.filter(b => !b.me && b.fin === null).map(b => [b.etich || b.name, sv.distacco ? sv.distacco(b) : null]);
      snap.push({ ...c, ocs: me.ocs, tLinea: me.tLinea ?? null, cop: me.cop || 0, copDa: me.copDa ? (me.copDa.etich || me.copDa.name) : null, sc: -Math.sign(a) * sv.norm180(w.twd - sv.envTwd()), twa: Math.abs(a),
        leg: me.leg, legPrima: pl, need: R.need || 0, needPrima: pn, done: R.done || 0, pp: me.pp || 0, ppPrima: ppp, pen: me.pen || 0, penPrima: ppe,
        posVero: sv.posizione(), dav, nMarks: R.marks.length }); }
  }
  const ms = performance.now() - t0;
  return { fin: R.boats.map(b => b.fin), snap, toasts, ms, rect: R.crRect || null, n: R.cr ? R.cr.log.length : 0 };
}"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e)))
        await q.goto((ROOT / "index.html").as_uri() + "#collaudo"); await q.wait_for_timeout(400)
        await q.evaluate("() => { __sv.posizione = () => ranking().indexOf(__sv.R.boats[0]) + 1; __sv.distacco = distacco; __sv.opt = opt; }")
        corse = []
        for seme in range(501, 501 + NS):
            for k in (0, 1, 2):
                acc = await q.evaluate(CORSA, [k, seme, True]); corse.append((seme, k, acc))
                print(f"seme {seme} regata {k + 1}: {acc['n']} commenti", [(round(c['t']), c['umore'], c['testo'][:60]) for c in acc["snap"]], flush=True)
        # P1
        ncom = [a["n"] for _, _, a in corse]
        forzati = re.compile(r"partito prima|Penalità|Giri fatti|Contatto con colpa")
        vicini = [(s, k, c1["t"], c2["t"]) for s, k, a in corse for c1, c2 in zip(a["snap"], a["snap"][1:]) if c2["t"] - c1["t"] < 30 - 1e-6 and not forzati.search(c2["testo"])]
        chk("P1", 4 <= st.median(ncom) <= 12 and not vicini, f"P1 commenti per regata {ncom} (mediana {st.median(ncom)}); a meno di 30 s senza essere penalità o partenza anticipata: {vicini[:3]}")
        # P2
        per_tipo, sbagli = {}, []
        for s, k, a in corse:
            ult = {"need": 0, "pp": 0, "pen": 0}   # come il Coach: una penalità è nuova se è più alta di quella del commento precedente (il commento arriva al passo dopo il contatto)
            for c in a["snap"]:
                t = c["testo"]; ok = None; tipo = None
                if "cono d'ombra" in t: tipo = "cono"; ok = c["cop"] > 0.10 and c["copDa"] is not None and c["copDa"] in t
                elif "scarso di" in t: tipo = "scarso"; n = int(re.search(r"scarso di (\d+)°", t).group(1)); ok = c["sc"] >= 7 and abs(n - round(c["sc"])) <= 0 and 30 <= c["twa"] <= 75
                elif t.startswith("Boa girata") or t.startswith("Alla boa"): tipo = "boa"; ok = f"sei {c['posVero']}°" in t
                elif "partito prima" in t: tipo = "ocs"; ok = bool(c["ocs"])
                elif t.startswith("Bella partenza"): tipo = "partenza"; ok = c["tLinea"] is not None and c["tLinea"] <= 3
                elif t.startswith("Partenza in ritardo"): tipo = "ritardo"; ok = c["tLinea"] is not None and c["tLinea"] >= 10
                elif t.startswith("Penalità"): tipo = "giri"; ok = c["need"] > ult["need"]; ult["need"] = c["need"]
                elif t.startswith("Giri fatti"): tipo = "giri fatti"; ok = c["done"] >= c["need"] > 0
                elif t.startswith("Contatto con colpa"): tipo = "colpa"; ok = c["pp"] > ult["pp"] or c["pen"] > ult["pen"]; ult["pp"] = c["pp"]; ult["pen"] = c["pen"]
                elif " è a " in t: tipo = "distacco"; m = re.search(r"è a (\d+) s", t); n = int(m.group(1)); ok = c["leg"] == c["nMarks"] + 1 and any(d is not None and abs(d - n) <= 1 and d >= 0.5 for _, d in c["dav"]) and n >= 1
                elif t.startswith("Sei ancora dietro"): tipo = "linea"; ok = c["leg"] < 1
                elif t.startswith("Per lo sponsor"): tipo = "sponsor"; ok = True
                else: tipo = "sconosciuto"; ok = False
                per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
                if not ok: sbagli.append((s, k, round(c["t"], 1), t[:70], {x: c[x] for x in ("cop", "copDa", "sc", "posVero", "tLinea", "leg")}))
        tot = sum(per_tipo.values())
        chk("P2", tot >= 10 and not sbagli, f"P2 commenti controllati {tot}, per tipo {per_tipo}; sbagliati {len(sbagli)}: {sbagli[:4]}")
        # P3: stessi argomenti dei messaggi del gioco negli stessi 10 s
        argomenti = [("cono d'ombra", re.compile(r"cono|copert", re.I)), ("scarso", re.compile(r"scars", re.I))]
        dop = [(s, k, round(c["t"]), c["testo"][:40], m) for s, k, a in corse for c in a["snap"] for arg, rx in argomenti if arg in c["testo"] for (tm, m) in a["toasts"] if abs(tm - c["t"]) <= 10 and rx.search(m)]
        chk("P3", not dop, f"P3 commenti sullo stesso argomento di un messaggio del gioco entro 10 s: {len(dop)} {dop[:3]}")
        # P4: spento
        for seme, k, acc0 in corse[:3]:   # a coppie, una dopo l'altra: la prima regata di una pagina viene diversa dalle altre (stato della pagina), e il confronto va fatto alla pari
            if k % 2: sp = await q.evaluate(CORSA, [k, seme, False]); acc = await q.evaluate(CORSA, [k, seme, True])   # ordine alternato, per il tempo (P6)
            else: acc = await q.evaluate(CORSA, [k, seme, True]); sp = await q.evaluate(CORSA, [k, seme, False])
            chk("P4", sp["fin"] == acc["fin"] and sp["n"] == 0, f"P4 seme {seme} regata {k + 1}: arrivi acceso {acc['fin']}, spento {sp['fin']}; commenti da spento {sp['n']}; tempo acceso {acc['ms'] / 1000:.1f} s, spento {sp['ms'] / 1000:.1f} s (P6, solo riportato)")
        # P5: un commento a schermo e il suo riquadro
        r = await q.evaluate("""() => { __sv.opt.coachReg = true; const R = __sv.R; R.cr = R.cr || { ult: -1e9, cur: null, log: [] }; R.cr.cur = { t0: R.t, umore: 'serio', testo: "Sei nel cono d'ombra della Rossa: vira o poggia per avere vento libero, e controlla la frase più lunga che può capitare." };
            __sv.draw(0.016); const ecc = Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0); return { rect: R.crRect, ecc, W: W, H: H }; }""")
        x, y, w, h = r["rect"] or (0, 0, 0, 0)
        chk("P5", r["rect"] is not None and x >= 0 and x + w <= r["W"] / 2 and y + h <= r["H"] / 2 and r["ecc"] == 0, f"P5 riquadro {r['rect']} nel mare {r['W']}x{r['H']}: nella metà alta a sinistra, lontano dal centro; eccesso {r['ecc']} px")
        await ctx.close()
        # P7
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e)))
        await q.goto((ROOT / "index.html").as_uri()); await q.wait_for_timeout(400)
        await q.evaluate("() => openItem(['r', 2])"); await q.wait_for_timeout(1500)
        r = await q.evaluate("() => { document.getElementById('openSet').click(); const v = !document.getElementById('coachRegRiga').hidden, chk = document.getElementById('showCoachReg').checked; document.getElementById('setDlg').close(); return { attivo: crAttivo(), riga: v, chk, sv: typeof window.__sv }; }")
        chk("P7", r == {"attivo": True, "riga": True, "chk": True, "sv": "undefined"}, f"P7 senza #collaudo, regata di Deriva: {r}")
        await ctx.close(); await b.close()
        chk("P7", not errs, f"errori della pagina {errs[:3]}")
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("P1", "P2", "P3", "P4", "P5", "P7")): print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
