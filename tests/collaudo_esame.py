# Collaudo dell'esame (0.20): banca, estrazione per quote, pagina vera senza #collaudo, nessun salvataggio,
# riquadro con 20 sbagliate e menu confrontato con la 0.19.5.
# Ogni parte dichiara quanti casi ha misurato e fallisce se sono zero.
# Le misure del riquadro valgono solo con i caratteri veri (Barlow, Source Serif): senza, ESITO: NON VALIDA (uscita 1).
# Uso: python collaudo_esame.py
import asyncio, sys, pathlib, re, subprocess, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"; BASE = HTML.as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
RIF_0195 = "8500b5b"  # commit con index.html della 0.19.5, per il confronto del menu
VIETATE = ["lascia strada", "lasciare strada", "precedenz", "abbattuta", "viro", "strambo", "orzier", "scader", "rosso", "verde"]
SEME = 20261010; ESTRAZIONI = 500
# Math.random a seme fisso (mulberry32): lo imposta il collaudo, il gioco non cambia
SEED_JS = "(()=>{let s=%d;Math.random=()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};})()"

fail = []; casi = {}
def chk(parte, c, m):
    casi[parte] = casi.get(parte, 0) + 1
    if not c: fail.append(f"{parte}: {m}"); print("FALLITO:", parte, "-", m)

src = HTML.read_text(encoding="utf-8")
blocco = lambda nome: re.search(r"const %s = \[.*?\n  \];" % nome, src, re.S).group(0)
DATI_JS = "s=>{const f=new Function(s+';return {ESAME,QUOTE,QUIZ,SOGLIA_ESAME}');Object.assign(window,{__E:f()})}"
DATI_SRC = re.search(r"const QUOTE = .*?;\n", src).group(0) + blocco("ESAME") + "\n" + blocco("QUIZ")

# titoli dei passi per lezione, dal testo di index.html (le lezioni non si toccano)
lez = src.split("const L1 = [")[1].split("const LESSONS")[0]
TITOLI = [re.findall(r'title: "([^"]*)"', t) for t in re.split(r"\n  const L\d = \[", lez)]

def controlla_banca(D):
    E, Q, QZ = D["ESAME"], D["QUOTE"], D["QUIZ"]
    ripasso = {t for les in QZ for r in les for t in [r[0], r[1], *r[2]]}
    chk("banca", len(E) == len(Q) == len(TITOLI) == 6, f"lezioni: banca {len(E)}, quote {len(Q)}, lezioni {len(TITOLI)}")
    piu_lunga = n = 0
    for li, les in enumerate(E):
        chk("banca", len(les) >= Q[li] + 1, f"lezione {li+1}: {len(les)} domande, ne servono almeno {Q[li]+1}")
        for passo, q, g, w, e in les:
            n += 1; testi = [q, g, *w, e]
            chk("banca", passo in TITOLI[li], f"lezione {li+1}: passo «{passo}» inesistente")
            chk("banca", len(w) == 3 and len({g, *w}) == 4, f"risposte non 4 diverse: {q}")
            chk("banca", not any(re.search(r"\d", t) for t in testi), f"cifra in: {q}")
            for v in VIETATE:
                chk("banca", not any(v in t.lower() for t in testi), f"parola vietata «{v}» in: {q}")
            chk("banca", not ({q, g, *w} & ripasso), f"testo uguale al ripasso: {q}")
            if len(g) > max(map(len, w)): piu_lunga += 1
    chk("banca", piu_lunga <= 0.30 * n, f"giusta più lunga {piu_lunga} su {n}")
    print(f"banca: {n} domande, per lezione {[len(l) for l in E]}, quote {Q}; giusta più lunga in {piu_lunga} su {n} ({100*piu_lunga/max(n,1):.0f}%)")
    return n

async def estrazioni(pg, D, N, tag):
    E, Q = D["ESAME"], D["QUOTE"]
    viste = set()
    for _ in range(N):
        es = await pg.evaluate("__sv.estraiEsame()")
        chk(tag, len(es) == sum(Q), f"{len(es)} domande invece di {sum(Q)}")
        chk(tag, len({r[2] for r in es}) == len(es), "domande ripetute in un esame")
        chk(tag, [sum(r[0] == li for r in es) for li in range(len(Q))] == Q, "quote sbagliate")
        viste |= {(r[0], r[2]) for r in es}
    tutte = {(li, r[1]) for li, les in enumerate(E) for r in les}
    chk(tag, viste == tutte, f"domande mai estratte: {len(tutte - viste)}")
    print(f"{tag}: {N} estrazioni, {len(viste)} domande diverse viste su {len(tutte)}")

async def un_esame(pg, giuste, D):
    """Risponde alle 20 domande: le prime `giuste` giuste, le altre sbagliate. Controlla che durante l'esame
    non compaiano colori né spiegazioni e che la risposta non si possa cambiare. Ritorna le sbagliate attese."""
    banca = {r[1]: (li, r) for li, les in enumerate(D["ESAME"]) for r in les}
    sbagliate = []; k = 0
    while not await pg.locator("#qzAgain").count():
        chk("esame", (await pg.inner_text(".qz-top h2")) == "Esame · livello 1", "titolo")
        chk("esame", (await pg.inner_text(".qz-top span")) == f"Domanda {k+1} di 20", f"contatore alla domanda {k+1}")
        q = await pg.inner_text(".qz .q"); li, r = banca[q]
        opts = await pg.locator(".opt").all_inner_texts()
        i = next(j for j, t in enumerate(opts) if (t == r[2]) == (k < giuste))
        if k >= giuste: sbagliate.append((li, r, opts[i]))
        await pg.locator(".opt").nth(i).click()
        stato = await pg.evaluate("""() => ({ expl: document.querySelectorAll('#qzBody .expl').length,
            colori: document.querySelectorAll('#qzBody .right, #qzBody .wrong').length,
            sel: document.querySelectorAll('#qzBody .opt.sel').length,
            attivi: [...document.querySelectorAll('#qzBody .opt')].filter(b => !b.disabled).length })""")
        chk("esame", stato["expl"] == 0 and stato["colori"] == 0, f"domanda {k+1}: spiegazione o colori visibili {stato}")
        chk("esame", stato["sel"] == 1 and stato["attivi"] == 0, f"domanda {k+1}: risposta modificabile {stato}")
        await pg.evaluate("j => document.querySelectorAll('#qzBody .opt')[j].click()", (i + 1) % 4)  # secondo clic: non deve cambiare niente
        chk("esame", await pg.evaluate("(i) => document.querySelectorAll('#qzBody .opt')[i].classList.contains('sel')", i), f"domanda {k+1}: risposta cambiata da un secondo clic")
        await pg.click("#qzNext"); k += 1
    chk("esame", k == 20, f"domande risposte: {k}")
    return sbagliate

async def controlla_esito(pg, giuste, sbagliate, D):
    soglia = D["SOGLIA_ESAME"]
    atteso = f"{giuste} su 20: " + ("superato" if giuste >= soglia else f"non superato (servono {soglia})")
    chk("esito", (await pg.inner_text(".qz .score")) == atteso, f"«{await pg.inner_text('.qz .score')}» invece di «{atteso}»")
    elenco = await pg.evaluate("""() => [...(document.getElementById('qzWrong')?.children || [])].map(e => e.tagName === 'H3' ? ['h3', e.textContent] :
        ['wq', e.querySelector('.wt').textContent, e.querySelector('.from')?.textContent, e.textContent])""")
    nomi = [f"Lezione {li+1}" for li in range(6)]
    lez_attese = sorted({li for li, _, _ in sbagliate})
    h3 = [e[1] for e in elenco if e[0] == "h3"]
    chk("esito", [h.split(":")[0] for h in h3] == [nomi[li] for li in lez_attese], f"titoli di lezione {h3}")
    chk("esito", sum(e[0] == "wq" for e in elenco) == len(sbagliate), "numero di sbagliate in elenco")
    att = {r[1]: (li, r, data) for li, r, data in sbagliate}; cur = None
    for e in elenco:
        if e[0] == "h3": cur = int(e[1].split(":")[0].split()[-1]) - 1; continue
        li, r, data = att.get(e[1], (None, None, None))
        chk("esito", li == cur, f"«{e[1]}» sotto la lezione sbagliata")
        chk("esito", r is not None and e[2] == f"dal passo «{r[0]}»", f"riga del passo per «{e[1]}»: {e[2]}")
        chk("esito", r is not None and f"Hai risposto: {data}" in e[3] and r[2] in e[3] and r[4] in e[3], f"risposta data, giusta o spiegazione mancanti per «{e[1]}»")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        # --- 1) banca e 500 estrazioni a seme fisso (aggancio #collaudo) ---
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(SEED_JS % SEME)
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        await pg.evaluate(DATI_JS, DATI_SRC); D = await pg.evaluate("__E")
        controlla_banca(D)
        await estrazioni(pg, D, ESTRAZIONI, "estrazione")
        # stesso meccanismo con una lezione più ricca (lezione 2 da 4 a 7 domande): deve funzionare con qualunque numero
        extra = "\n  ESAME[1].push(" + ",".join(f'["Come si timona", "prova {c}", "giusta {c}", ["a {c}", "b {c}", "c {c}"], "spiegazione"]' for c in "xyz") + ");"
        var = src.replace(blocco("ESAME"), blocco("ESAME") + extra, 1)
        tmp = pathlib.Path(tempfile.mkdtemp()) / "index.html"; tmp.write_text(var, encoding="utf-8")
        await pg.goto(tmp.as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        D2 = dict(D); D2["ESAME"] = [list(l) for l in D["ESAME"]]
        D2["ESAME"][1] = D2["ESAME"][1] + [["Come si timona", f"prova {c}", f"giusta {c}", [f"a {c}", f"b {c}", f"c {c}"], "spiegazione"] for c in "xyz"]
        await estrazioni(pg, D2, 200, "estrazione (lezione 2 con 7 domande)")
        await pg.close()

        # --- 2) pagina vera, senza #collaudo: pulsante, esame, esito, nessun salvataggio ---
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(SEED_JS % SEME)
        await pg.goto(BASE); await pg.wait_for_timeout(300)
        # progressi già presenti, per vedere che l'esame non li tocca
        await pg.evaluate("""() => localStorage.setItem('scuolaVelaSim.v1', JSON.stringify({done: {l0: true, m0: true}, best: {'m0.2': 90}, clean: {}, quiz: {q0: 5, q2: 4}}))""")
        await pg.reload(); await pg.wait_for_timeout(300)
        await pg.evaluate(DATI_JS, DATI_SRC)
        prima = await pg.evaluate("JSON.stringify(Object.fromEntries(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)])))")
        chk("pagina", await pg.evaluate("typeof window.__sv") == "undefined", "la pagina non deve avere l'aggancio dei collaudi")
        bt = pg.locator("#goEsame")
        chk("pagina", await bt.count() == 1 and await bt.is_enabled(), "pulsante dell'esame presente e acceso")
        chk("pagina", "20 domande, ne servono 16" in await bt.inner_text(), f"testo del pulsante: {await bt.inner_text()}")
        await bt.click(); await pg.wait_for_timeout(100)
        chk("pagina", await pg.evaluate("document.getElementById('quiz').open"), "il pulsante apre l'esame")
        for n, giuste in enumerate((20, 16, 15, 0)):
            if n: await pg.click("#qzAgain"); await pg.wait_for_timeout(50)  # «Rifai l'esame» riparte da capo
            chk("pagina", (await pg.inner_text(".qz-top span")) == "Domanda 1 di 20", "l'esame riparte dalla domanda 1")
            sb = await un_esame(pg, giuste, D)
            await controlla_esito(pg, giuste, sb, D)
            if giuste == 0: await pg.screenshot(path=str(OUT / "E_20sbagliate.png"))
        await pg.click("#qzClose"); await pg.wait_for_timeout(150)
        chk("pagina", not await pg.evaluate("document.getElementById('quiz').open"), "«Chiudi» chiude l'esame")
        dopo = await pg.evaluate("JSON.stringify(Object.fromEntries(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)])))")
        chk("salvataggio", prima == dopo and "q0" in prima, f"localStorage cambiato:\n prima {prima}\n dopo  {dopo}")
        print(f"salvataggio: localStorage identico prima e dopo 4 esami: {prima == dopo} ({len(prima)} caratteri confrontati)")

        # --- 3) menu: altezza confrontata con la 0.19.5, nello stesso browser ---
        vecchio = subprocess.run(["git", "-C", str(ROOT), "show", f"{RIF_0195}:index.html"], capture_output=True, text=True).stdout
        chk("menu", "0.19.5" in vecchio, f"index.html della 0.19.5 non trovato ({RIF_0195})")
        tmp2 = pathlib.Path(tempfile.mkdtemp()) / "index.html"; tmp2.write_text(vecchio, encoding="utf-8")
        alt = {}
        for nome, url in (("0.19.5", tmp2.as_uri()), ("ora", BASE)):
            q = await b.new_page(viewport={"width": 1360, "height": 650}); await q.goto(url); await q.wait_for_timeout(300)
            await q.evaluate("document.fonts.ready")
            alt[nome] = await q.evaluate("[document.documentElement.scrollHeight, Math.max(...[...document.querySelectorAll('.tile')].map(t => t.getBoundingClientRect().height))]")
            await q.close()
        chk("menu", alt["ora"][0] <= alt["0.19.5"][0] and alt["ora"][1] <= alt["0.19.5"][1], f"menu più alto: {alt}")
        print(f"menu a 1360x650 (altezza pagina, riquadro più alto): 0.19.5 {alt['0.19.5']}, ora {alt['ora']}")

        # --- 4) riquadro con 20 sbagliate, con i caratteri veri ---
        await pg.evaluate("document.fonts.ready")
        car = await pg.evaluate("""() => ({
            "barlow 700": document.fonts.check('700 16px "Barlow Semi Condensed"'),
            "source serif 400": document.fonts.check('400 16px "Source Serif 4"'),
            "facce Barlow caricate": [...document.fonts].some(f => f.family.includes("Barlow") && f.status === "loaded"),
            "facce Source Serif caricate": [...document.fonts].some(f => f.family.includes("Source Serif") && f.status === "loaded"),
        })""")
        veri = all(car.values())
        print("caratteri del gioco caricati:", veri, car)
        eccesso = 0
        for H in (650, 768):
            await pg.set_viewport_size({"width": 1360, "height": H})
            await pg.click("#goEsame"); await un_esame(pg, 0, D); await pg.wait_for_timeout(100)
            r = await pg.evaluate("""() => {
                const d = document.getElementById('quiz').getBoundingClientRect(), W = document.getElementById('qzWrong');
                const bt = [...document.querySelectorAll('#qzBody .row button')].map(b => b.getBoundingClientRect().bottom);
                return {top: d.top, bottom: d.bottom, right: d.right, H: innerHeight, W: innerWidth, bt,
                        scroll: W.scrollHeight > W.clientHeight, sh: W.scrollHeight, ch: W.clientHeight, pagina: document.documentElement.scrollHeight - innerHeight};
            }""")
            ecc = max([x - r["bottom"] for x in r["bt"]] + [r["bottom"] - r["H"], -r["top"], r["right"] - r["W"], r["pagina"]])
            eccesso = max(eccesso, ecc); tag = f"riquadro 1360x{H}"
            chk("riquadro", len(r["bt"]) == 2, f"{tag}: pulsanti trovati {len(r['bt'])}")
            chk("riquadro", all(x <= r["bottom"] + 0.5 for x in r["bt"]), f"{tag}: pulsanti oltre il riquadro")
            chk("riquadro", r["top"] >= 0 and r["bottom"] <= r["H"] + 0.5, f"{tag}: riquadro fuori dalla finestra")
            chk("riquadro", r["pagina"] <= 0, f"{tag}: la pagina dietro scorre di {r['pagina']} px")
            chk("riquadro", r["scroll"], f"{tag}: con 20 sbagliate l'elenco deve scorrere")
            print(f"  {tag}, 20 sbagliate: riquadro {r['bottom']-r['top']:.0f} px su {r['H']}, elenco {r['sh']} in {r['ch']} px, eccesso {ecc:.1f} px")
            await pg.click("#qzClose"); await pg.wait_for_timeout(100)
        print(f"eccesso massimo: {eccesso:.1f} px (positivo = fuori)")
        chk("pagina", not errs, f"errori di pagina: {errs}")
        await b.close()
    print("casi misurati per parte:", casi)
    for parte in ("banca", "estrazione", "estrazione (lezione 2 con 7 domande)", "esame", "esito", "pagina", "salvataggio", "menu", "riquadro"):
        if not casi.get(parte): fail.append(f"{parte}: zero casi misurati")
    if fail: print("ESITO: FALLITO"); sys.exit(1)
    if not veri:
        print("MISURA DEL RIQUADRO NON VALIDA: mancano i caratteri veri (Barlow, Source Serif); il resto è OK.")
        print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
