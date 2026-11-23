# Punti di Deriva e «Deriva superata» (1.3.5, docs/PROPOSTA-DERIVA-CIRCUITI.md, criteri D6, D8, D10; D2 e D3 per la carriera).
# Pagina con #collaudo (salvataggi costruiti o stagioni vere chiuse con le funzioni del gioco), più una pagina senza #collaudo.
#   D6a stagione zonale vera vinta (4 tappe chiuse con stChiudiTappa, sempre primo nella batteria): superata «fra i primi 3», il riquadro compare una volta sola,
#       e alla ricarica resta superata senza ricomparire
#   D6b stagione vera con una tappa lasciata: mai «senza ritiri», quindi mai per merito, anche con tutti gli altri punti (21/21 di punti costruiti)
#   D6c per merito (costruito): stagione 5° senza ritiri e 25 punti (dalla 1.3.49; 22 dalla 1.3.10, prima 19): superata; con 24: no (controprova); con 25 ma senza la stagione «senza ritiri»: no
#   D6d salvataggio della 1.2.39 con lo zonale già fra i primi 3 (diritto al nazionale, nessun campo nuovo): superata al primo menu
#   D6e gioco libero con gli stessi progressi: non si supera niente; carriera senza attestato: niente (Deriva è ancora chiusa)
#   D6f stagione non finita (lasciata a metà) con tutti gli altri punti: no
#   D8  i meriti della Scuola uguali con e senza i progressi di Deriva, e i punti di Deriva uguali con e senza quelli della Scuola
#   D10 ripetere senza migliorare: un tempo peggiore nella prova, un ripasso peggiore, una seconda stagione peggiore non cambiano i punti; solo le stagioni (senza il resto) non bastano per merito
#   D2/D3 carriera: Deriva spenta senza attestato, aperta con; menu di Deriva col libretto pieno a 1360x650 e 1360x768 senza eccesso, Chromium e Firefox; 0 errori
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

BREV = {"done": {}, "best": {}, "clean": {}, "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}, "dvBenvenuto": "2026-11-15"}   # 1.3.23: il benvenuto in Deriva già visto (lo controlla collaudo_carriera_file)
RESTO = {"done": {"l20": True, "l21": True, "l22": True, "l23": True, "l24": True, "m5": True}, "best": {"m5": 230}, "clean": {"m5": True}, "quiz": {"q20": 4, "q21": 4, "q22": 5, "q23": 4, "q24": 4}, "coachVisto": True}   # 1.3.10: con la lezione 24 (indice 23); 1.3.49: con la 25 (indice 24)
def unisci(*d):
    o = {"done": {}, "best": {}, "clean": {}, "quiz": {}}
    for x in d:
        for k, v in x.items(): o[k] = {**o.get(k, {}), **v} if isinstance(v, dict) and k in ("done", "best", "clean", "quiz") else v
    return o

# una stagione zonale vera: 4 tappe chiuse con stChiudiTappa; posto: il mio posto in ogni regata del torneo della tappa (1-4); lascia: indice della tappa lasciata
STAGIONE = """([posto, lascia, quante]) => { const sv = __sv; sv.progress.stagione = sv.st.nuova(); const S = sv.progress.stagione;
  for (let k = 0; k < quante; k++){
    if (k === lascia){ sv.st.chiudi(null); continue; }
    const T = sv.torNuovo(S); T.ris = Array.from({ length: window.NREG || 4 }, (_, j) => j).map(() => [0, 1, 2, 3].map(i => ({ fin: i === 0 ? posto : (i < posto ? i : i + 1), pp: 0 })));
    sv.st.chiudi(T);
  }
  return { fine: S.fine || null, pulita: !!sv.progress.zonalePulita, naz: !!sv.progress.nazionale, tappa: sv.progress.derivaTappa || null, fatta: sv.progress.stagioneFatta || null }; }"""

LUNGO = "--lungo" in sys.argv   # 21 nov 2026 (voce 66c): tornei delle stagioni a 3 regate lunghe (__sv.lungo = true, window.NREG = 3). Uso: collaudo_deriva_superata.py [--lungo]
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina(salv, modo="carriera", hash_="#collaudo", H=650, liv="deriva"):
            ctx = await b.new_context(viewport={"width": 1360, "height": H}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
            await q.goto(BASE + hash_)
            await q.evaluate("([d, m, l]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); localStorage.setItem('scuolaVelaLivello', l); if (d) localStorage.setItem(m === 'carriera' ? 'scuolaVelaCarriera.v1' : 'scuolaVelaSim.v1', d); }",
                             [json.dumps(salv) if salv else None, modo, liv])
            await q.reload(); await q.wait_for_timeout(300)
            if hash_ == "#collaudo": await q.evaluate("v => { __sv.lungo = v; window.NREG = v ? 3 : 4; }", LUNGO)
            return ctx, q
        stato = "() => ({ d: __sv.progress.deriva || null, dlg: document.getElementById('derivaDlg').open, m: meritiD(__sv.progress) })"
        # ---- D6a: stagione vera vinta
        ctx, q = await pagina(BREV)
        await q.evaluate("() => { if (!__sv.torNuovo) __sv.torNuovo = torNuovo; }")
        s = await q.evaluate(STAGIONE, [1, -1, 4]); print("D6a stagione vera:", s)
        await q.evaluate("() => { saveProgress(); showMenu(); }"); r = await q.evaluate(stato)
        chk("D6", s["fine"] and s["fine"]["pos"] <= 3 and s["naz"] and s["pulita"] and r["d"] and r["d"]["strada"] == "piazzamento" and r["dlg"], f"D6a stagione vinta: {s} → {r['d']}, riquadro {r['dlg']}")
        await q.evaluate("() => { document.getElementById('derivaDlg').close(); showMenu(); }"); r2 = await q.evaluate(stato)
        await q.reload(); await q.wait_for_timeout(300)
        await q.evaluate("v => { __sv.lungo = v; window.NREG = v ? 3 : 4; }", LUNGO); r3 = await q.evaluate(stato)
        chk("D6", not r2["dlg"] and not r3["dlg"] and r3["d"] == r["d"], f"D6a il riquadro una volta sola, e alla ricarica resta: {r2['dlg']}, {r3}")
        lib = await q.inner_text("#libDManca") if await q.locator("#libDManca").count() else ""
        chk("D6", lib.startswith("Deriva superata il"), f"D6a libretto di Deriva: «{lib}»")
        await ctx.close()
        # ---- D6b: stagione vera con una tappa lasciata, con tutti gli altri punti
        ctx, q = await pagina(unisci(BREV, RESTO))
        await q.evaluate("() => { if (!__sv.torNuovo) __sv.torNuovo = torNuovo; }")
        s = await q.evaluate(STAGIONE, [4, 2, 4]); await q.evaluate("() => { delete __sv.progress.nazionale; __sv.progress.stagioneFatta = { pos: 5 }; __sv.progress.derivaTappa = 2; saveProgress(); showMenu(); }")
        r = await q.evaluate(stato)
        chk("D6", not s["pulita"] and r["d"] is None and r["m"]["totale"] >= 25, f"D6b tappa lasciata: pulita {s['pulita']}, punti {r['m']['totale']}, superata {r['d']}")
        await ctx.close()
        # ---- D6c: per merito, costruito
        for pt, pul, att in ((25, True, True), (24, True, False), (25, False, False)):   # 1.3.49: quota 25 su 27 (1.3.10: 22 su 24; prima 19 su 21)
            salv = unisci(BREV, RESTO, {"stagioneFatta": {"pos": 5}, "derivaTappa": 2})
            if pt == 24: salv["quiz"]["q22"] = 3   # ripasso 23 al 60%: un punto in meno
            if pul: salv["zonalePulita"] = True
            ctx, q = await pagina(salv); r = await q.evaluate(stato)
            chk("D6", r["m"]["totale"] == pt and bool(r["d"]) == att and (not att or r["d"]["strada"] == "merito"), f"D6c {pt} punti, senza ritiri {pul}: superata {r['d']} (attesa {att})")
            await ctx.close()
        # ---- D6d: salvataggio della 1.2.39
        v139 = {**BREV, "stagioneFatta": {"pos": 2}, "nazionale": True, "zonalePrimo": "Marta Ferraresi"}
        ctx, q = await pagina(v139); r = await q.evaluate(stato)
        chk("D6", r["d"] and r["d"]["strada"] == "piazzamento" and r["dlg"], f"D6d salvataggio della 1.2.39 con lo zonale fra i primi 3: {r['d']}")
        await ctx.close()
        # ---- D6e: gioco libero; carriera senza attestato
        ctx, q = await pagina(v139, modo="libero"); r = await q.evaluate(stato)
        chk("D6", r["d"] is None and not r["dlg"], f"D6e gioco libero: {r['d']}, riquadro {r['dlg']}")
        await ctx.close()
        senza = {k: v for k, v in v139.items() if k not in ("brevetto", "exam")}
        ctx, q = await pagina(senza); r = await q.evaluate(stato)
        dis = await q.is_disabled("#livSel button[data-v='deriva']")
        chk("D6", r["d"] is None and not r["dlg"] and dis, f"D6e carriera senza attestato: {r['d']}, Deriva spenta {dis}")
        chk("D3", dis and await q.locator("#goTor").count() == 0, "D3 senza attestato Deriva è spenta e il torneo non c'è")
        await ctx.close()
        # ---- D6f: stagione non finita
        ctx, q = await pagina(unisci(BREV, RESTO))
        await q.evaluate("() => { if (!__sv.torNuovo) __sv.torNuovo = torNuovo; }")
        s = await q.evaluate(STAGIONE, [1, -1, 3]); await q.evaluate("() => { saveProgress(); showMenu(); }"); r = await q.evaluate(stato)
        chk("D6", not s["fine"] and r["d"] is None, f"D6f stagione a metà (3 tappe su 4, sempre primo): {s['fine']}, superata {r['d']}, punti {r['m']['totale']}")
        # ---- D8
        d8 = await q.evaluate("""() => { const sc = { done: { l0: true, l1: true, m0: true }, best: { 'm0.4': 70 }, clean: { 'm0.4': true }, quiz: { q0: 4, q3: 3 } }; // chiavi delle prove come le scrive il gioco (KEYV)
            const de = { done: { l20: true, l22: true, m5: true }, best: { m5: 250 }, clean: {}, quiz: { q21: 4 }, stagioneFatta: { pos: 3 }, derivaTappa: 1, coachVisto: true };
            const mix = { ...sc, ...de, done: { ...sc.done, ...de.done }, best: { ...sc.best, ...de.best }, clean: { ...sc.clean, ...de.clean }, quiz: { ...sc.quiz, ...de.quiz } };
            const j = o => JSON.stringify(o); return { scuola: j(meriti(sc).pt) === j(meriti(mix).pt), deriva: j(meritiD(de).pt) === j(meritiD(mix).pt), ps: meriti(mix).pt, pd: meritiD(mix).pt }; }""")
        chk("D8", d8["scuola"] and d8["deriva"] and sum(d8["pd"].values()) > 0 and sum(d8["ps"].values()) > 0, f"D8 punti separati: {d8}")
        # ---- D10
        d10 = await q.evaluate("""() => { const p = { done: { l20: true, m5: true }, best: { m5: 250 }, clean: {}, quiz: { q20: 3 }, stagioneFatta: { pos: 5 }, derivaTappa: 2 };
            const a = meritiD(p).totale; p.quiz.q20 = Math.max(p.quiz.q20, 2); p.best.m5 = Math.min(p.best.m5, 300); p.stagioneFatta = { pos: Math.min(p.stagioneFatta.pos, 9) }; const b = meritiD(p).totale;
            const solo = { done: {}, best: {}, clean: {}, stagioneFatta: { pos: 4 }, derivaTappa: 1, zonalePulita: true }; const s = meritiD(solo);
            return { a, b, solo: s.totale, merito: s.merito }; }""")
        chk("D10", d10["a"] == d10["b"] and not d10["merito"] and d10["solo"] < 25, f"D10 ripetere senza migliorare: {d10}")
        await ctx.close()
        # ---- D2 e D3: carriera col libretto di Deriva pieno, pagina senza #collaudo
        pieno = unisci(BREV, RESTO, {"stagioneFatta": {"pos": 2}, "derivaTappa": 1, "nazionale": True, "deriva": {"data": "2026-11-15", "strada": "piazzamento"}})
        for H in (650, 768):
            ctx, q = await pagina(pieno, hash_="", H=H)
            m = await q.evaluate("() => ({ ecc: document.documentElement.scrollHeight - innerHeight, eccx: document.documentElement.scrollWidth - innerWidth, sel: document.querySelector('#livSel [aria-pressed=true]').dataset.v, lib: !!document.getElementById('libDManca'), tor: !!document.getElementById('goTor'), sv: typeof window.__sv })")
            chk("D2", m["ecc"] <= 0 and m["eccx"] <= 0 and m["sel"] == "deriva" and m["lib"] and m["tor"] and m["sv"] == "undefined", f"D2/D3 carriera, Deriva col libretto pieno a 1360x{H}: {m}")
            await q.click("#goTor"); await q.wait_for_timeout(200)
            chk("D3", await q.is_visible("#torDlg"), f"D3 in carriera il torneo si apre da Deriva (1360x{H})")
            await ctx.close()
        chk("D3", not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("D2", "D3", "D6", "D8", "D10")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
