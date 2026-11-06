# Collaudo del menu nuovo (1.2.4, docs/PROPOSTA-MENU.md §3: criteri M1-M6 scritti prima del codice; bozza A scelta da Ale il 2 novembre 2026).
#   M1: menu senza pixel di eccesso (pagina) con ognuno dei 3 gruppi aperto, in gioco libero e in carriera, a 1360x650 e 1360x768.
#   M2: le 25 voci, numerate da 1 a 25 senza buchi, aprono la lezione o la prova giusta; le lezioni si chiamano «Lezione 1…20» nell'ordine della proposta.
#   M3: un salvataggio di oggi (lezioni 1-6 dell'array e prove fatte, record, quiz) dà le stesse voci fatte, gli stessi record e gli stessi punteggi; controprova vuota.
#   M4: nessun rimando vecchio: niente «Lezione B…/C…/D…» nei testi; i rimandi «lezione N» noti puntano al titolo giusto; ogni esercizio dice il numero della sua lezione;
#       le voci del glossario delle lezioni nuove rimandano alla lezione giusta.
#   M5: la lezione 3 dell'array (Lezione 4, «Andature e mure») senza «precedenz» e senza la domanda tolta dal quiz.
#   M6: pagina senza #collaudo: si cambia gruppo, si apre una voce per gruppo e si torna al menu, nessun errore.
# L'ordine (ORD) e i gruppi sono scritti qui dalla proposta, non letti dal gioco. Uso: python collaudo_menu.py   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, re, sys
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]; BASE = (ROOT / "index.html").as_uri()
import sorgente; SRC = sorgente.testo()
GRUPPI = [[("l", 0), ("l", 1), ("l", 6), ("l", 2), ("m", 0), ("m", 1), ("l", 3), ("l", 4), ("l", 7), ("m", 2), ("m", 3)],
          [("l", 5), ("l", 9), ("l", 8), ("l", 10), ("m", 4)],
          [("l", 11), ("l", 12), ("l", 13), ("l", 14), ("l", 15), ("l", 16), ("l", 18), ("l", 19), ("l", 17)]]
SEQ = [x for g in GRUPPI for x in g]; ORD = [i for t, i in SEQ if t == "l"]
TITOLI = ["La barca e il vento", "Il timone", "Il timone che stalla", "Andature e mure", "Al traverso", "Lasco e poppa", "Vento reale e apparente", "Virata e strambata",
          "Spingere il boma", "Risalire il vento", "Il giro di boa", "Raffiche e scuffia", "La raddrizzata lunga", "La barca che orza sbandando", "I salti di vento", "Percorso nelle raffiche",
          "Mure opposte", "Stesse mure", "Chi vira cede", "Evitare il contatto", "I segnali di partenza", "La partenza anticipata", "Partenza in velocità", "Partenza da fermi", "Boe e giri di penalità"]
bad = []; casi = {}
def chk(parte, ok, m):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def pagina(b, H=650, hash_="#collaudo", salv=None, modo=None):
    ctx = await b.new_context(viewport={"width": 1360, "height": H}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + hash_)
    if salv is not None or modo:
        await pg.evaluate("([d, m]) => { localStorage.clear(); if (m) localStorage.setItem('scuolaVelaModo', m); if (d) localStorage.setItem(m === 'carriera' ? 'scuolaVelaCarriera.v1' : 'scuolaVelaSim.v1', d); }", [json.dumps(salv) if salv else None, modo])
        await pg.reload()
    await pg.wait_for_timeout(400); await pg.evaluate("document.fonts.ready")
    return ctx, pg, errs
VOCI = "() => [...document.querySelectorAll('#menu button.item[data-k]')].map(b => [b.querySelector('.num').textContent, b.querySelector('.kind').textContent, b.querySelector('.title').textContent, b.querySelector('.state').textContent])"
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        # ---- M1: spazio ----
        for H in (650, 768):
            for modo in ("libero", "carriera"):
                ctx, pg, errs = await pagina(b, H, "", None, modo)
                for g in range(3):
                    await pg.click(f"#schede button[data-g='{g}']"); await pg.wait_for_timeout(120)
                    r = await pg.evaluate("() => ({ pag: document.documentElement.scrollHeight - innerHeight, piede: document.querySelector('.menu-foot').getBoundingClientRect().bottom, H: innerHeight, n: document.querySelectorAll('#menu button.item[data-k]').length })")
                    chk("M1", r["pag"] <= 0 and r["piede"] <= r["H"] and r["n"] == len(GRUPPI[g]), f"M1 1360x{H} {modo} gruppo {g + 1}: eccesso {r['pag']} px, piede a {r['piede']:.0f} su {r['H']}, voci {r['n']}")
                chk("M1", not errs, f"M1 1360x{H} {modo}: errori di pagina {errs[:1]}"); await ctx.close()
        # ---- M2: voci, numeri, nomi, aperture ----
        ctx, pg, errs = await pagina(b)
        tutte = []
        for g in range(3):
            await pg.click(f"#schede button[data-g='{g}']"); tutte += await pg.evaluate(VOCI)
        chk("M2", [v[0] for v in tutte] == [str(k) for k in range(1, 26)], f"M2 numeri da 1 a 25 senza buchi: {[v[0] for v in tutte]}")
        nomi_attesi = [f"Lezione {ORD.index(i) + 1}" if t == "l" else f"Prova {i + 1}" for t, i in SEQ]
        chk("M2", [v[1] for v in tutte] == nomi_attesi and [v[2] for v in tutte] == TITOLI, f"M2 nomi e titoli nell'ordine della proposta: {[v[1] + ' ' + v[2] for v in tutte][:6]}…")
        aperte = []
        for k, (t, i) in enumerate(SEQ):
            g = next(j for j, gr in enumerate(GRUPPI) if (t, i) in gr)
            await pg.evaluate("() => showMenu()"); await pg.click(f"#schede button[data-g='{g}']")
            await pg.locator("#menu button.item[data-k]", has_text=TITOLI[k]).first.click(); await pg.wait_for_timeout(80)
            aperte.append(await pg.evaluate("() => [mode, mode === 'lesson' ? lessonIdx : missionIdx]"))
        chk("M2", aperte == [["lesson" if t == "l" else "mission", i] for t, i in SEQ], f"M2 ogni voce apre la sua lezione o prova: {sum(1 for a, (t, i) in zip(aperte, SEQ) if a == ['lesson' if t == 'l' else 'mission', i])} su 25")
        await pg.evaluate("() => showMenu()")
        nomiL = await pg.evaluate("() => LESSONS.map(L => L.name)")
        chk("M2", all(nomiL[i] == f"Lezione {ORD.index(i) + 1}" for i in range(20)), f"M2 nomi delle lezioni nei dati: {nomiL}")
        rip = await pg.evaluate("() => LESSONS.map((L, i) => ripName(i))")
        chk("M2", all(rip[i] == f"Ripasso {ORD.index(i) + 1}" for i in range(20)), f"M2 nomi dei ripassi: {rip}")
        # ---- M4: rimandi ----
        testi = await pg.evaluate("""() => { const out = []; const add = (dove, t) => { if (typeof t === 'string') out.push([dove, t]); else if (Array.isArray(t)) t.forEach(x => add(dove, x)); };
            LESSONS.forEach((L, i) => { add(L.name + ' desc', L.desc); L.steps.forEach(st => { add(L.name + ' ' + st.title, st.text); add(L.name + ' ' + st.title, st.done); if (st.esercizio){ add(L.name + ' brief', st.esercizio.brief); add(L.name + ' obiettivo', st.esercizio.obiettivo); } });
              (QUIZ[i] || L.quiz || []).forEach(q => add(L.name + ' quiz', q.flat())); (ESAME[i] || L.esame || []).forEach(q => add(L.name + ' esame', q.flat())); });
            MISSIONS.forEach(m => add(m.title, [m.desc, m.text, m.brief].filter(Boolean))); GLOSS.forEach(g => add('glossario ' + g[0], g[1])); return out; }""")
        vecchi = [(d, t) for d, t in testi if re.search(r"[Ll]ezione [BCD]\d", t)]
        chk("M4", len(testi) > 300 and not vecchi, f"M4 nessun «Lezione B/C/D…» in {len(testi)} testi: {vecchi[:2]}")
        # i rimandi per numero nel codice del gioco (testi e messaggi), con il titolo a cui devono puntare
        attesi = {"2": "Il timone", "4": "Andature e mure", "6": "Virata e strambata", "12": "Mure opposte"}   # il 4 dalla 1.2.12 (riepilogo della lezione 2)
        rim = [(m.group(1), l.strip()[:80]) for l in SRC.splitlines() if not l.lstrip().startswith("//") for m in re.finditer(r"(?<![Ee]sercizio della )\blezione (\d+)\b", l.split(" // ")[0])]
        chk("M4", len(rim) >= 5 and all(n in attesi for n, _ in rim), f"M4 rimandi «lezione N» nei testi: {len(rim)}, numeri {sorted({n for n, _ in rim})}, fuori dall'elenco atteso: {[r for r in rim if r[0] not in attesi][:3]}")
        tit = await pg.evaluate("() => Object.fromEntries(LESSONS.map(L => [L.name.split(' ')[1], L.title]))")
        chk("M4", all(tit[n] == t for n, t in attesi.items()), f"M4 i numeri dei rimandi puntano a {[(n, tit[n]) for n in attesi]}")
        br = await pg.evaluate("() => LESSONS.flatMap((L, i) => L.steps.filter(s => s.esercizio).map(s => [L.name, (s.esercizio.brief.match(/lezione (\\d+)/) || [])[1]]))")
        chk("M4", len(br) == 5 and all(n == "Lezione " + str(k) for n, k in br), f"M4 ogni esercizio in regata dice il numero della sua lezione: {br}")
        gl = await pg.evaluate("() => GLOSS.map(g => [g[0], g[2]])"); glm = dict(gl)
        att_gl = {"Stallo della pala": "Il timone che stalla", "Spingere il boma": "Spingere il boma", "Scarso": "I salti di vento", "Precedenza": "Mure opposte",
                  "Sovrapposte": "Stesse mure", "Avviso": "I segnali di partenza", "Richiamo individuale": "La partenza anticipata", "Giro di penalità": "Boe e giri di penalità",
                  "Partenza in velocità": "Partenza in velocità", "Partenza da fermi": "Partenza da fermi", "Strambata": "Virata e strambata", "Andatura": "Andature e mure", "Raffica": "Raffiche e scuffia"}
        sbag = [(v, glm.get(v), tit.get((glm.get(v) or "x y").split(" ")[1])) for v, t in att_gl.items() if tit.get((glm.get(v) or "x y").split(" ")[1]) != t]
        chk("M4", not sbag and all(w == "Prove" or re.fullmatch(r"Lezione ([1-9]|1\d|20)", w) for _, w in gl), f"M4 glossario: {len(att_gl)} voci controllate sul titolo, sbagliate {sbag}")
        # ---- M5: lezione 3 dell'array ----
        l3 = [t for d, t in testi if d.startswith("Lezione 4 ")]
        chk("M5", len(l3) > 20 and not any("precedenz" in t.lower() for t in l3) and not any("Chi deve lasciare strada" in t for t in l3), f"M5 «Andature e mure» senza precedenze ({len(l3)} testi)")
        chk("M5", await pg.evaluate("() => [LESSONS[2].title, QUIZ[2].length, LESSONS[2].steps.some(s => s.title === 'Le mure')]") == ["Andature e mure", 5, True], "M5 titolo, quiz di 5 domande, pagina «Le mure»")
        chk("M6", not errs, f"M2-M5 errori di pagina {errs[:1]}"); await ctx.close()
        # ---- M3: salvataggio di oggi ----
        salv = {"done": {"l0": True, "l1": True, "l2": True, "l3": True, "l4": True, "l5": True, "m0": True, "m1": True}, "best": {"m0.4": 70, "m1.4": 130}, "clean": {"m0.4": True}, "quiz": {"q0": 6, "q2": 4}}
        for modo in ("libero", "carriera"):
            ctx, pg, errs = await pagina(b, 650, "", salv, modo)
            tutte = []
            for g in range(3):
                await pg.click(f"#schede button[data-g='{g}']"); tutte += await pg.evaluate(VOCI)
            fatte = [v[2] for v in tutte if v[3] == "Completata" or " min " in v[3]]   # le prove fatte mostrano il record («1 min 10 s»)
            att = ["La barca e il vento", "Il timone", "Andature e mure", "Al traverso", "Lasco e poppa", "Vento reale e apparente", "Virata e strambata", "Raffiche e scuffia"]
            rec = {v[2]: v[3] for v in tutte if v[2] in ("Al traverso", "Lasco e poppa")}
            await pg.click("#schede button[data-g='0']")
            q = await pg.evaluate("() => [document.querySelector(\"[data-q='0']\").title, document.querySelector(\"[data-q='2']\").title]")
            chk("M3", sorted(fatte) == sorted(att) and rec["Al traverso"].startswith("1 min 10 s") and "★" in rec["Al traverso"] and rec["Lasco e poppa"].startswith("2 min 10 s") and "migliore: 6 su 6" in q[0] and "migliore: 4 su 5" in q[1],
                f"M3 {modo}: voci fatte {len(fatte)} su 8 attese, record {rec}, quiz {q}")
            chk("M6", not errs, f"M3 {modo}: errori di pagina {errs[:1]}"); await ctx.close()
        ctx, pg, errs = await pagina(b, 650, "", {"done": {}, "best": {}, "clean": {}}, "libero")
        tutte = []
        for g in range(3):
            await pg.click(f"#schede button[data-g='{g}']"); tutte += await pg.evaluate(VOCI)
        chk("M3", len(tutte) == 25 and all(v[3] == "Da fare" for v in tutte), f"M3 controprova: salvataggio vuoto, {sum(1 for v in tutte if v[3] != 'Da fare')} voci fatte su {len(tutte)}")
        await ctx.close()
        # ---- M6: pagina senza #collaudo ----
        ctx, pg, errs = await pagina(b, 650, "")
        ok6 = []
        for g, tit6 in ((0, "Il timone che stalla"), (1, "Percorso nelle raffiche"), (2, "Partenza da fermi")):
            await pg.click(f"#schede button[data-g='{g}']"); await pg.locator("#menu button.item", has_text=tit6).first.click(); await pg.wait_for_timeout(400)
            if await pg.locator("#bGo").is_visible(): await pg.keyboard.press("Enter"); await pg.wait_for_timeout(300)
            dentro = await pg.evaluate("() => document.getElementById('menu').hidden")
            await pg.evaluate("() => document.getElementById('toMenu').click()"); await pg.wait_for_timeout(300)
            fuori = await pg.evaluate("() => !document.getElementById('menu').hidden && document.querySelector('#schede button[aria-pressed=true]').dataset.g")
            ok6.append(dentro and fuori == str(g))
        chk("M6", ok6 == [True] * 3 and not errs, f"M6 senza #collaudo: una voce per gruppo aperta e chiusa, si torna alla sua scheda {ok6}, errori {errs[:1]}")
        await ctx.close(); await b.close()
    print("casi per parte:", casi)
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad or any(casi.get(k, 0) == 0 for k in ("M1", "M2", "M3", "M4", "M5", "M6")) else 0)
asyncio.run(main())
