# Collaudo della 0.23: libretto dei meriti in carriera (criteri L1-L4 di docs/PROPOSTA-ESAME-E-BREVETTO.md, §12, scritti prima
# del codice; tabella dei meriti dalla 0.23, senza il +1 «senza errori» in Competizione).
# I salvataggi si costruiscono dalle regole scritte, non dal codice del gioco: fasce e numero di domande dei ripassi si leggono
# dal testo di index.html. I numeri attesi sono quelli della tabella degli esempi del §12.
# L1-L2 con #collaudo (meriti() dall'aggancio); L3-L4 senza, come la carica un giocatore, con salvataggi preparati.
# Lo spazio (L4) vale solo con i caratteri veri (Barlow, Source Serif): senza, ESITO: NON VALIDA (uscita 1).
# Fallisce se una parte misura zero casi. Uso: python collaudo_libretto.py
import asyncio, json, pathlib, re, sys
from playwright.async_api import async_playwright
INDEX = pathlib.Path(__file__).resolve().parent.parent / "index.html"; BASE = INDEX.as_uri()
SRC = INDEX.read_text(encoding="utf-8")
BANDS = [list(map(int, b)) for b in re.findall(r"bands: \[(\d+), (\d+), (\d+)\]", SRC)]   # [oro, argento, bronzo] per prova
assert len(BANDS) == 5, BANDS
QUIZ_JS = re.search(r"const QUIZ = \[.*?\n  \];", SRC, re.S).group(0)
MK = ["m0.2", "m1.2", "m2.2", "m3.3", "m4.4"]   # chiavi delle prove (KEYV), come le scrive il gioco
fail = []; casi = {}; visti = {}
def chk(parte, c, m):
    casi[parte] = casi.get(parte, 0) + 1
    if not c: fail.append(m); print("FALLITO:", m, flush=True)

def prog(prove=(), pulite=(), ripassi=None, regate=None, lezioni=(), esame=None):
    """prove: fascia per prova (0 oro, 1 argento, 2 bronzo, None niente); ripassi: {lezione: punteggio}; regate: {chiave: (pos, pulita)}"""
    p = {"done": {}, "best": {}, "clean": {}}
    for i, f in enumerate(prove):
        if f is not None: p["best"][MK[i]] = BANDS[i][f]; p["done"]["m" + str(i)] = True
    for i in pulite: p["clean"][MK[i]] = True
    if ripassi: p["quiz"] = {"q" + str(i): s for i, s in ripassi.items()}
    if regate: p["race"] = {k: {"pos": pos, "n": 4, "pulita": pul} for k, (pos, pul) in regate.items()}
    for i in lezioni: p["done"]["l" + str(i)] = True
    if esame is not None: p["exam"] = {"superato": esame}
    return p

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        NQ = await pg.evaluate("s => new Function(s + ';return QUIZ')().map(q => q.length)", QUIZ_JS)
        piene = {i: n for i, n in enumerate(NQ)}   # ogni ripasso tutto giusto
        L = await pg.evaluate("() => { const n = []; for (let i = 0; i < 6; i++) n.push('Lezione ' + (i + 1)); return n; }")
        print("fasce lette:", BANDS, "| domande dei ripassi:", NQ)
        async def M(p): return await pg.evaluate("p => __sv.meriti(p)", p)
        def area(m):
            for k in ("abil", "cono", "comp", "esp"): visti.setdefault(k, set()).add(m["pt"][k])

        # ---- L1: giocatori del §12
        GIOC = {
            "A": (prog([1] * 5, [0, 1], {i: NQ[i] for i in range(4)}, {"r0.2:principianti": (3, False), "r1.2:principianti": (3, True)}, range(6)),
                  (12, 8, 4, 6, 30), "Ti manca l'esame.", ["l'esame su tutte le lezioni."]),
            "B": (prog([0] * 5, range(5), piene, None, range(6)), (20, 12, 0, 6, 38), "Ti mancano punti in Competizione; poi l'esame.", ["la Regata a bastone (con avversari)."]),
            "C": (prog([0, 0, 0, 0, 1], (), {i: NQ[i] for i in range(5)}, {"r0.2:esperti": (1, False), "r1.2:principianti": (3, False)}, range(3)),
                  (14, 10, 6, 3, 33), "Ti mancano punti in Esperienza; poi l'esame.", ["Lezione 4, Vento reale e apparente."]),
            "D": (prog([2] * 5, [3], {i: NQ[i] for i in range(3)}, {"r0.2:principianti": (4, True), "r1.2:principianti": (4, False)}, range(6)),
                  (6, 6, 2, 6, 20), "Ti mancano punti in Abilità e Competizione; poi l'esame.", ["Prova 1, Al traverso: prova a migliorare il tempo.", "la Regata a bastone (con avversari)."]),
        }
        for g, (p, att, riga, sugg) in GIOC.items():
            m = await M(p); area(m)
            got = (m["pt"]["abil"], m["pt"]["cono"], m["pt"]["comp"], m["pt"]["esp"], m["totale"])
            chk("L1", got == att, f"L1 {g}: punti {got}, attesi {att}")
            chk("L1", m["manca"] == riga, f"L1 {g}: riga «{m['manca']}», attesa «{riga}»")
            chk("L1", m["sugg"] == sugg, f"L1 {g}: suggerimenti {m['sugg']}, attesi {sugg}")
            print(f"L1 {g}: {got} | {m['manca']} | {m['sugg']}")

        # ---- L2: casi al bordo
        base = dict(prove=[1, 1, 1, 1, None], ripassi={0: NQ[0], 1: NQ[1], 2: NQ[2]}, regate={"r0.2:principianti": (2, False)}, lezioni=range(6))  # 8, 6, 3, 6 = 23
        m = await M(prog(**base)); area(m)
        chk("L2", (m["pt"]["abil"], m["pt"]["cono"], m["pt"]["comp"], m["pt"]["esp"], m["totale"]) == (8, 6, 3, 6, 23), f"L2 tutti al minimo: {m['pt']} {m['totale']}")
        chk("L2", m["manca"] == "Ti mancano 6 punti al totale; poi l'esame." and len(m["sugg"]) == 3, f"L2 tutti al minimo: «{m['manca']}» {m['sugg']}")
        for nome, mod, k, att, voce in (("Abilità", dict(prove=[1, 1, 1, 2, None]), "abil", 7, "Prova 5, "), ("Conoscenza", dict(ripassi={0: NQ[0], 1: NQ[1]}), "cono", 4, "il ripasso della Lezione 3."),
                                  ("Competizione", dict(regate={"r0.2:principianti": (3, False)}), "comp", 2, "la Regata nelle raffiche (con avversari)."), ("Esperienza", dict(lezioni=range(5)), "esp", 5, "Lezione 6, ")):
            m = await M(prog(**{**base, **mod})); area(m)
            chk("L2", m["pt"][k] == att and m["manca"] == f"Ti mancano punti in {nome}; poi l'esame." and len(m["sugg"]) == 1 and m["sugg"][0].startswith(voce),
                f"L2 {nome} sotto il minimo: {m['pt'][k]} «{m['manca']}» {m['sugg']}")
        # totale a 29 e a 28 con le aree a posto (Abilità sopra il minimo)
        for prove, tot in (([0, 0, 0, 0, 1], 29), ([0, 0, 0, 0, 2], 28)):
            for esame in (False, True):
                m = await M(prog(**{**base, "prove": prove}, esame=esame)); area(m)
                chk("L2", m["totale"] == tot, f"L2 totale {tot}: trovato {m['totale']}")
                if tot == 28: chk("L2", m["manca"] == ("Ti manca 1 punto al totale." if esame else "Ti manca 1 punto al totale; poi l'esame.") and not m["superato"], f"L2 totale 28, esame {esame}: «{m['manca']}»")
                elif esame: chk("L2", m["superato"] and m["manca"] is None and m["sugg"] == [], f"L2 tutto a posto ed esame: superato {m['superato']} «{m['manca']}»")
                else: chk("L2", m["manca"] == "Ti manca l'esame." and m["sugg"] == ["l'esame su tutte le lezioni."] and not m["superato"], f"L2 totale 29 senza esame: «{m['manca']}»")
        # esame superato ma un'area sotto: non superato
        m = await M(prog(**{**base, "prove": [0, 0, 0, 0, 1], "lezioni": range(5)}, esame=True))
        chk("L2", not m["superato"] and "Esperienza" in m["manca"], f"L2 esame superato, Esperienza 5: superato {m['superato']}")
        # soglie dei ripassi, conti fatti qui con le frazioni
        for i, n in enumerate(NQ):
            for s in range(n + 1):
                att = 2 if s / n >= 0.8 else 1 if s / n >= 0.6 else 0
                m = await M(prog(ripassi={i: s}))
                chk("L2 ripassi", m["pt"]["cono"] == att, f"L2 ripasso {i + 1}, {s} su {n}: {m['pt']['cono']} punti, attesi {att}")
        print("L2 ripassi: lunghezze", sorted(set(NQ)), "| con 4 domande 3 su 4 = 1 punto, 4 su 4 = 2:",
              any(n == 4 for n in NQ), "| 60% e 80% esatti provati:", any(n % 5 == 0 for n in NQ))
        # regate: il migliore dei due livelli, «nessuno» e n diverso da 4 non contano; pulite contate a parte, senza punti
        m = await M(prog(regate={"r0.2:principianti": (4, False), "r0.2:esperti": (2, True)})); area(m)
        chk("L2 regate", m["pt"]["comp"] == 3 and m["pulite"] == 1, f"L2 regata con due livelli: {m['pt']['comp']} punti, pulite {m['pulite']}")
        m = await M(prog(regate={"r0.2:esperti": (1, True), "r1.2:esperti": (1, True)})); area(m)
        chk("L2 regate", m["pt"]["comp"] == 8 and m["pulite"] == 2, f"L2 due primi posti puliti: {m['pt']['comp']} (massimo 8, niente +1), pulite {m['pulite']}")
        p = prog(regate={"r0.2:nessuno": (1, True)}); m = await M(p)
        chk("L2 regate", m["pt"]["comp"] == 0 and m["pulite"] == 0, f"L2 chiave «nessuno»: {m['pt']['comp']} punti, pulite {m['pulite']}")
        p = prog(); p["race"] = {"r0.2:principianti": {"pos": 1, "n": 3, "pulita": False}}; m = await M(p)
        chk("L2 regate", m["pt"]["comp"] == 0, f"L2 flotta di 3: {m['pt']['comp']} punti")
        m = await M(prog()); area(m)
        chk("L2", m["totale"] == 0 and m["manca"] == "Ti mancano punti in Abilità, Conoscenza, Competizione ed Esperienza; poi l'esame." and len(m["sugg"]) == 4, f"L2 vuoto: «{m['manca']}» {m['sugg']}")
        m = await M(prog([0] * 5, range(5), piene, {"r0.2:esperti": (1, True), "r1.2:esperti": (1, True)}, range(6), True)); area(m)
        chk("L2", m["totale"] == 46 and m["superato"], f"L2 tutto al massimo: {m['totale']} superato {m['superato']}")
        # controllo del metro: ogni area vista almeno una volta diversa da zero e diversa dal massimo
        for k, mx in (("abil", 20), ("cono", 12), ("comp", 8), ("esp", 6)):
            chk("metro", any(v > 0 for v in visti[k]) and any(v < mx for v in visti[k]), f"metro {k}: valori visti {sorted(visti[k])}")
        chk("pagina", not errs, f"L1-L2 errori di pagina: {errs}")
        await pg.close()

        # ---- L3 e L4: pagina senza #collaudo
        async def menu(H, salv, modo="carriera"):
            ctx = await b.new_context(viewport={"width": 1360, "height": H}); q = await ctx.new_page(); e = []; q.on("pageerror", lambda x: e.append(str(x)))
            await q.goto(BASE); await q.evaluate("([d, m]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }", [json.dumps(salv) if salv else None, modo])
            await q.reload(); await q.wait_for_timeout(300); await q.evaluate("document.fonts.ready")
            return ctx, q, e
        for g in ("A", "D"):
            p, att, riga, sugg = GIOC[g]; ctx, q, e = await menu(650, p)
            chk("L3", await q.evaluate("typeof window.__sv") == "undefined", "L3: senza #collaudo __sv non esiste")
            nums = [await q.inner_text(f"[data-m='{k}']") for k in ("abil", "cono", "comp", "esp")]
            chk("L3", await q.inner_text("#libSug") == "Cosa potresti fare adesso: " + sugg[0], f"L3 {g}: suggerimento «{await q.inner_text('#libSug')}»")
            chk("L3", nums == [f"{att[0]} / 20", f"{att[1]} / 12", f"{att[2]} / 8", f"{att[3]} / 6"], f"L3 {g}: barre {nums}")
            chk("L3", await q.inner_text("#libTot") == f"totale {att[4]} / 46 (servono 29)", f"L3 {g}: totale «{await q.inner_text('#libTot')}»")
            chk("L3", await q.inner_text("#libManca") == riga, f"L3 {g}: riga «{await q.inner_text('#libManca')}»")
            pul = sum(1 for k, v in p.get("race", {}).items() if v["pulita"])
            chk("L3", await q.inner_text("#libPulite") == f"Regate senza errori: {pul} su 2", f"L3 {g}: «{await q.inner_text('#libPulite')}»")
            chk("L3", not e, f"L3 {g}: errori di pagina {e}"); print(f"L3 {g}: {nums} | {await q.inner_text('#libManca')}"); await ctx.close()
        ctx, q, e = await menu(650, None)
        chk("L3", await q.locator("#libManca").count() == 1 and await q.is_enabled("#goEsame"), "L3: carriera vuota, libretto presente e pulsante dell'esame acceso")
        # il suggerimento cambia a ogni ritorno al menu: con quattro aree che mancano, quattro giri le mostrano tutte
        giro = []
        for _ in range(4):
            giro.append(await q.inner_text("#libSug")); await q.click("#modoSel button[data-v='libero']"); await q.click("#modoSel button[data-v='carriera']")
        att = ["Prova 1, Al traverso.", "il ripasso della Lezione 1.", "la Regata a bastone (con avversari).", "Lezione 1, La barca e il vento."]
        chk("L3", sorted(x.split(": ", 1)[1] for x in giro) == sorted(att), f"L3 giro dei suggerimenti: {giro}")
        print("L3 giro dei suggerimenti:", [x.split(": ", 1)[1] for x in giro])
        await ctx.close()
        ctx, q, e = await menu(650, GIOC["A"][0], "libero")
        chk("L3", await q.locator("#libManca").count() == 0 and "In arrivo" in await q.inner_text(".tiles"), "L3: nel gioco libero niente libretto, «In arrivo» sì")
        await ctx.close()
        # L4: spazio con ogni tipo di riga «cosa manca» (la più lunga è il caso peggiore): carriera vuota (Abilità), Conoscenza,
        # Competizione, Esperienza con sei lezioni da fare, totale, esame, superato
        tutto = dict(prove=[0] * 5, pulite=range(5), ripassi=piene, regate={"r0.2:esperti": (1, False), "r1.2:esperti": (1, False)}, lezioni=range(6))
        righe = [None, prog(**{**tutto, "ripassi": None}), prog(**{**tutto, "regate": None}), prog(**{**tutto, "lezioni": ()}),
                 prog(**{**base, "prove": [0, 0, 0, 0, 2]}), prog(**tutto), prog(**tutto, esame=True)]
        veri = True
        for H, peggio in [(H, x) for H in (650, 768) for x in righe]:
            ctx, q, e = await menu(H, peggio)
            car = await q.evaluate("""() => [document.fonts.check('700 16px "Barlow Semi Condensed"'), document.fonts.check('400 16px "Source Serif 4"'),
                [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"), [...document.fonts].some(f => f.family.includes("Source Serif") && f.status === "loaded")]""")
            veri = veri and all(car)
            r = await q.evaluate("""() => ({ pagina: document.documentElement.scrollHeight - innerHeight, piede: document.querySelector('.menu-foot').getBoundingClientRect().bottom,
                H: innerHeight, tiles: [...document.querySelectorAll('.tile')].map(t => Math.round(t.getBoundingClientRect().height)), riga: document.getElementById('libManca').innerText })""")
            chk("L4", r["pagina"] <= 0 and r["piede"] <= r["H"], f"L4 1360x{H}: eccesso {r['pagina']} px, piede a {r['piede']:.0f} su {r['H']}")
            print(f"L4 1360x{H}: eccesso {r['pagina']} px, piede a {r['piede']:.0f} su {r['H']}, riquadri {r['tiles']}, riga «{r['riga']}», caratteri veri {all(car)}")
            await ctx.close()
        await b.close()
    print("casi per parte:", casi)
    if fail: print("ESITO: FALLITO"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("L1", "L2", "L2 ripassi", "L2 regate", "metro", "L3", "L4")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    if not veri: print("MISURA DELLO SPAZIO NON VALIDA: mancano i caratteri veri (Barlow, Source Serif); il resto è OK."); print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
