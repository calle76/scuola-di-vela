# Collaudo della 1.0: una carriera intera, da zero all'attestato, nella stessa pagina e nello stesso salvataggio (criteri I1-I4 di
# docs/archivio/PROPOSTA-ESAME-E-BREVETTO.md, §14, scritti prima del codice). «Carriera» si sceglie cliccando il selettore; alla fine si
# legge solo quello che il gioco ha salvato. Serve #collaudo, perché i piloti usano l'aggancio __sv.
#  - Lezioni: tutti i passi, fino all'ultimo (è lì che il gioco segna la lezione completata). Dalla 1.0.19 li guida il **pilota delle
#    lezioni** (`collaudo_pilota_lezioni.py`, costante PILOTA): prima prova 30 s a mani ferme, poi guida; solo i passi che non sa
#    guidare li salta con l'aggancio (showStep), e il collaudo stampa quanti. Prima ne guidava 14 su 32 con una tabella propria.
#  - Prove 1-4: il pilota di collaudo_fasce.py, letto dal suo file. La prova 5 no: il pilota la finisce 19 volte su 24.
#  - Regate: il pilota sostituto (__sv.pilota) di collaudo_competizione.py, letto dal suo file, avversari principianti;
#    si ritenta con semi nuovi finché i due piazzamenti migliori danno almeno 3 punti, al massimo 3 tentativi per regata.
#  - Ripassi ed esame: a clic, risposte giuste lette dalle banche nel testo di index.html.
# Se una prova o una regata non arriva in fondo, l'esito è NON VALIDO, non FALLITO. Uso: python collaudo_carriera_intera.py
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent; OUT = QUI / "output"; OUT.mkdir(exist_ok=True)
INDEX = QUI.parent / "index.html"; import sorgente; SRC = sorgente.testo(); URL = INDEX.as_uri() + "#collaudo"   # SRC: dalla 1.0.3 index.html più js/
leggi = lambda f: (QUI / f).read_text(encoding="utf-8")
SEME = re.search(r'SEME = """(.*?)"""', leggi("collaudo_fasce.py"), re.S).group(1)
CORSA_PROVA = re.search(r'CORSA = """(.*?)"""', leggi("collaudo_fasce.py"), re.S).group(1)
ATTREZZI = re.search(r'ATTREZZI = """(.*?)"""', leggi("collaudo_lezioni.py"), re.S).group(1)
CAR, LIB = "scuolaVelaCarriera.v1", "scuolaVelaSim.v1"
CORSA_REGATA = re.search(r'CORSA = """(.*?)""" % STORE', leggi("collaudo_competizione.py"), re.S).group(1) % CAR
BANCHE = re.search(r"const ESAME = \[.*?\n  \];", SRC, re.S).group(0) + "\n" + re.search(r"const QUIZ = \[.*?\n  \];", SRC, re.S).group(0)
BANDS = [list(map(int, b)) for b in re.findall(r"bands: \[(\d+), (\d+), (\d+)\]", SRC)]
MK = ["m0.4", "m1.4", "m2.4", "m3.5", "m4.6"]
GIUSTO = [60, 0, -60]; PIANI = [[], [], [], [[0, GIUSTO]]]   # come in collaudo_fasce.py

# il pilota delle lezioni, letto dal suo file (che ora è importabile): definisce window.__corsa(lezione, impreciso, seme, seme2)
import collaudo_pilota_lezioni as PL
PILOTA_LEZIONI = PL.PILOTA

fail = []; nonvalido = []; casi = {}
def chk(parte, c, m):
    casi[parte] = casi.get(parte, 0) + 1
    if not c: fail.append(m); print("FALLITO:", m, flush=True)

async def main():
    t_inizio = time.time()
    async with async_playwright() as pw:
        b = await getattr(pw, __import__("os").environ.get("BROWSER", "chromium")).launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("() => localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(300)
        await pg.click("#modoSel button[data-v='carriera']")
        chk("I3", await pg.get_attribute("#modoSel button[aria-pressed='true']", "data-v") == "carriera", "selettore su Carriera")
        await pg.evaluate("s => { window.__B = new Function(s + ';return { ESAME, QUIZ }')(); }", BANCHE)
        await pg.evaluate(f"({ATTREZZI})()")
        NQ = await pg.evaluate("__B.QUIZ.map(q => q.length)")

        # ---- lezioni, guidate dal pilota delle lezioni
        await pg.evaluate(PILOTA_LEZIONI)
        guidati = completati = forzati = ignoti = 0
        for li in range(6):
            r = await pg.evaluate("a => __corsa(...a)", [li, False, 1000 + li, 7919 + li * 31])
            for x in r:
                if not x["noto"]: ignoti += 1
                else:
                    guidati += 1
                    completati += bool(x["guida"])
                if x.get("forzato"): forzati += 1
            print(f"  lezione {li + 1}: {len(r)} passi, completati {sum(1 for x in r if x['guida'])}, "
                  f"forzati {sum(1 for x in r if x.get('forzato'))}", flush=True)
        chk("I1", guidati > 0 and completati >= guidati - 2, f"passi guidati {guidati}, completati {completati} (al massimo 2 falliti)")
        print(f"lezioni: passi che il pilota sa guidare {guidati} (completati {completati}), "
              f"passi non previsti dal pilota {ignoti}, saltati con l'aggancio {forzati}", flush=True)

        # ---- prove 1-4
        tempi = []
        for i in range(4):
            await pg.evaluate(f"() => {{ __seed(1); __sv.openItem(['m',{i}]); __sv.startMission({i}, 0); }}")
            fin, t, _ = await pg.evaluate(CORSA_PROVA, PIANI[i]); tempi.append(round(t, 1) if fin else None)
            if not fin: nonvalido.append(f"prova {i + 1} non finita")
        print("prove 1-4, tempi:", tempi, flush=True)

        # ---- regate: ognuna una volta, poi si ritenta quella con meno punti finché la somma dei migliori fa almeno 3
        # (al massimo 3 tentativi per regata)
        best = [0, 0]; tent = [0, 0]; storia = []
        while tent[0] == 0 or tent[1] == 0 or sum(best) < 3:
            r = 0 if tent[0] == 0 else 1 if tent[1] == 0 else (0 if best[0] <= best[1] else 1)
            if tent[r] >= 3: r = 1 - r
            if tent[r] >= 3: break
            tent[r] += 1
            # il seme si fissa nello stesso evaluate che apre la regata: fra due evaluate il disegno consuma Math.random (0.21.1)
            x = await pg.evaluate(f"([a, x]) => {{ __seed(x); return ({CORSA_REGATA})(a); }}", [[r, tent[r], "principianti", ["r0.4", "r1.4"][r] + ":principianti"], 100 + 10 * r + tent[r]])
            if x["moved"] == 0: nonvalido.append(f"regata {r + 1}: il sostituto non ha mosso la barra")
            pos = x["saved"]["pos"] if x["saved"] else None
            storia.append((r + 1, tent[r], pos)); best[r] = max(best[r], 5 - pos if pos else 0)
        print("regate (regata, tentativo, posto):", storia, "| punti migliori:", best, flush=True)
        if sum(best) < 3: nonvalido.append(f"regate: {sum(best)} punti dopo i tentativi {tent}")

        # ---- ripassi ed esame, dal menu, a clic
        await pg.evaluate("() => document.getElementById('toMenu').click()"); await pg.wait_for_timeout(200)
        for li in range(6):
            await pg.click(f"[data-q='{li}']")
            while not await pg.locator("#qzAgain").count():
                q = await pg.inner_text(".qz .q"); g = await pg.evaluate("([li, q]) => __B.QUIZ[li].find(r => r[0] === q)[1]", [li, q])
                opts = await pg.locator(".opt").all_inner_texts(); await pg.locator(".opt").nth(opts.index(g)).click(); await pg.click("#qzNext")
            await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        await pg.click("#goEsame")
        while not await pg.locator("#qzBody .score").count():
            q = await pg.inner_text(".qz .q"); g = await pg.evaluate("q => { for (const l of __B.ESAME) for (const r of l) if (r[1] === q) return r[2]; }", q)
            opts = await pg.locator(".opt").all_inner_texts(); await pg.locator(".opt").nth(opts.index(g)).click(); await pg.click("#qzNext")
        await pg.click("#qzClose"); await pg.wait_for_timeout(300)

        # ---- I1-I4: solo quello che il gioco ha salvato
        p = json.loads(await pg.evaluate(f"localStorage.getItem('{CAR}')"))
        att = await pg.evaluate("document.getElementById('attest').open")
        chk("I1", att, "I1: la scena dell'attestato è comparsa da sola")
        await pg.screenshot(path=str(OUT / "I_attestato.png"))
        if att: await pg.click("#atClose")
        chk("I1", p.get("exam", {}).get("superato") is True and p["exam"].get("voto") == 20 and "data" in p.get("brevetto", {}), f"I1: esame {p.get('exam')}, brevetto {p.get('brevetto')}")
        chk("I1", (await pg.inner_text("#libManca")).startswith("Brevetto ottenuto il"), f"I1: libretto «{await pg.inner_text('#libManca')}»")
        # meriti calcolati qui dalle regole scritte (§12), dal salvataggio
        fas = lambda i: next((3 - k for k in range(3) if p["best"].get(MK[i]) and p["best"][MK[i]] <= BANDS[i][k]), 0)
        abil = sum(fas(i) + (1 if p["clean"].get(MK[i]) else 0) for i in range(5))
        cono = sum(2 if p.get("quiz", {}).get(f"q{i}", -1) / NQ[i] >= 0.8 else 1 if p.get("quiz", {}).get(f"q{i}", -1) / NQ[i] >= 0.6 else 0 for i in range(6))
        comp = sum(max([5 - v["pos"] for k, v in p.get("race", {}).items() if k.startswith(c + ":") and k.split(":")[1] in ("principianti", "esperti") and v["n"] == 4] or [0]) for c in ("r0.4", "r1.4"))
        esp = sum(1 for i in range(6) if p["done"].get(f"l{i}"))
        nel = [await pg.inner_text(f"[data-m='{k}']") for k in ("abil", "cono", "comp", "esp")]
        chk("I2", nel == [f"{abil} / 20", f"{cono} / 12", f"{comp} / 8", f"{esp} / 6"], f"I2: libretto {nel}, calcolati {abil}, {cono}, {comp}, {esp}")
        chk("I2", abil >= 8 and cono >= 6 and comp >= 3 and esp == 6 and abil + cono + comp + esp >= 29, f"I2: meriti sotto i minimi {abil}, {cono}, {comp}, {esp}")
        chk("I3", await pg.evaluate(f"localStorage.getItem('{LIB}')") is None, "I3: il gioco libero non è stato toccato")
        # I4: il metro ha misurato davvero
        chk("I4", esp == 6 and all(p["done"].get(f"m{i}") for i in range(4)) and len(p.get("race", {})) >= 1, f"I4: completati dal gioco: lezioni {esp}, prove {[p['done'].get(f'm{i}') for i in range(4)]}, regate {list(p.get('race', {}))}")
        chk("I4", guidati + ignoti == 32 and forzati == 0, f"I4: passi pratici 32 attesi, il pilota ne guida {guidati} e non prevede {ignoti}; saltati con l'aggancio {forzati}")
        chk("I4", not errs, f"errori di pagina: {errs[:3]}")
        print(f"meriti: Abilità {abil}, Conoscenza {cono}, Competizione {comp}, Esperienza {esp}, totale {abil + cono + comp + esp}; "
              f"regate senza errori {sum(1 for v in p.get('race', {}).values() if v['pulita'])}; durata {time.time() - t_inizio:.0f} s")
        await b.close()
    print("casi per parte:", casi)
    if nonvalido: print("NON VALIDO:", nonvalido); print("ESITO: NON VALIDO"); sys.exit(1)
    if fail: print("ESITO: FALLITO"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("I1", "I2", "I3", "I4")): print("ESITO: NON VALIDO (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
