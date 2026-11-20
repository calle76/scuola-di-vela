# Carriera e attestato in un file, benvenuto e sponsor all'entrata in Deriva (1.3.23, voci 54 e 64; docs/PROPOSTA-ATTESTATO-E-CARRIERA-FILE.md, criteri C1-C8 scritti prima del codice).
#   C1 5 carriere costruite (Scuola a metà, attestato, Deriva con stagione, sponsor con contratto, Deriva superata): salva → azzera → carica: progress e fantasmi identici, libretto uguale
#   C2 rifiuti: stagione, attestato in «Carica una carriera», carriera in «Riparti da un attestato», forma 2, testo non JSON: rifiutati col messaggio, carriera invariata (5 su 5)
#   C3 attestato: salvato col pulsante, caricato su una carriera già in Deriva: Deriva aperta e mostrata, tutto il resto azzerato, libretto «caricato da un file», attestato coi punti del file
#   C4 benvenuto: la prima volta che si apre Deriva in carriera (anche dopo l'attestato), una volta sola su 3 aperture del menu; mai nel gioco libero
#   C5 sponsor all'entrata: carriera nuova → 2 offerte, gradini 1 e 2; carriera con stagione → offerte invariate (nessuna)
#   C6 contratto del gradino 1 finito con lo zonale chiuso fra i primi 3: c'è un'offerta nazionale; chiuso oltre il 3°: nessuna nazionale (stagioni a numeri, come collaudo_sponsor)
#   C7 pannello: menu della carriera (Scuola e Deriva) e finestra del benvenuto a 1360x650, 0 px di eccesso
#   C8 come un giocatore (pagina senza #collaudo): salva col download vero, azzera, carica scegliendo il file: salvataggio identico; benvenuto visto; 0 errori
# Uso: python tests/collaudo_carriera_file.py   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, sys, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
STAG = (ROOT / "tests" / "collaudo_sponsor.py").read_text().split('STAG = """')[1].split('"""')[0]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
BREV = {"done": {"l0": True, "m0": True}, "best": {"m0.4": 205}, "clean": {}, "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}, "quiz": {"q0": 5}}
STORE = "scuolaVelaCarriera.v1"
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
ECC = "() => Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0)"
STATO = "() => ({ p: JSON.stringify(progress), g: JSON.stringify(ghosts), lib: (document.getElementById('libManca') || document.getElementById('libDManca') || {}).textContent || null })"
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []; dialoghi = []
        async def pagina(salv, liv="deriva", hash_="#collaudo", benv=False, scarica=False):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}, accept_downloads=scarica); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
            q.on("dialog", lambda d: (dialoghi.append((d.type, d.message)), asyncio.ensure_future(d.accept())))
            await q.add_init_script(SEME); await q.goto(BASE + hash_)
            await q.evaluate("([d, liv]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', 'carriera'); localStorage.setItem('scuolaVelaLivello', liv); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }", [json.dumps(salv) if salv else None, liv])
            await q.reload(); await q.wait_for_timeout(300)
            if benv: await q.evaluate("() => { __sv.benvenuto = true; }")
            return ctx, q
        # ---- C1: cinque carriere
        COSTRUISCI = {
            "Scuola a metà": "() => {}",
            "attestato": "() => {}",
            "Deriva con stagione": "() => { progress.stagione = stNuova(null, 'zon'); }",
            "sponsor con contratto": "() => { const D = spDati(); D.c = { ...spOfferta(2, 1), esiti: [] }; D.storia.push({ nome: 'Ferramenta del Molo Nuovo', g: 1, durata: 1, esiti: [[true, true]], esito: 'tutti' }); }",
            "Deriva superata": "() => { progress.deriva = { data: '2026-11-18', strada: 'merito' }; progress.stagione = stNuova(null, 'zon'); }",
        }
        for nome, js in COSTRUISCI.items():
            salv = {"done": {"l0": True, "m0": True}, "best": {"m0.4": 210}, "clean": {"m0.4": True}, "quiz": {"q0": 4}} if nome == "Scuola a metà" else BREV
            ctx, q = await pagina(salv, "scuola" if nome == "Scuola a metà" else "deriva")
            await q.evaluate(js); await q.evaluate("() => { ghosts = { 'r0.4': { t: [1, 2, 3], x: [0.5, 1.5] } }; saveProgress(); saveGhosts(); __sv.st.showMenu(); }")
            prima = await q.evaluate(STATO); testo = await q.evaluate("() => carFile()")
            await q.evaluate("() => { localStorage.removeItem('scuolaVelaCarriera.v1'); localStorage.removeItem('scuolaVelaGhostCarriera.v1'); }"); await q.reload(); await q.wait_for_timeout(300)
            vuota = await q.evaluate(STATO)
            r = await q.evaluate("t => carCarica(t)", testo); dopo = await q.evaluate(STATO)
            chk("C1", r == "" and dopo["p"] == prima["p"] and dopo["g"] == prima["g"] and dopo["lib"] == prima["lib"] and vuota["p"] != prima["p"],
                f"C1 {nome}: carica → {r!r}; progress uguale {dopo['p'] == prima['p']}, fantasmi uguali {dopo['g'] == prima['g']}, libretto {dopo['lib']!r} contro {prima['lib']!r}")
            await ctx.close()
        # ---- C2: rifiuti
        ctx, q = await pagina(BREV)
        await q.evaluate("() => { progress.stagione = stNuova(null, 'zon'); saveProgress(); }")
        prima = await q.evaluate(STATO)
        stag = await q.evaluate("() => { const S = stNuova({ seme: 12345, liv: 'medio', io: 'A' }); return stFile(S); }")
        att = await q.evaluate("() => attFile({ pt: { abil: 5, comp: 4, cono: 6, esp: 5 } })")
        car = await q.evaluate("() => carFile()")
        car2 = json.dumps({**json.loads(car), "forma": 2})
        for nome, fn, t in (("stagione in Carica una carriera", "carCarica", stag), ("attestato in Carica una carriera", "carCarica", att), ("carriera in Riparti da un attestato", "attCarica", car),
                            ("forma 2", "carCarica", car2), ("testo non JSON", "carCarica", "ciao, non sono un file")):
            r = await q.evaluate(f"t => {fn}(t)", t); dopo = await q.evaluate(STATO)
            chk("C2", isinstance(r, str) and len(r) > 10 and dopo["p"] == prima["p"], f"C2 {nome}: rifiuto {r!r}, carriera invariata {dopo['p'] == prima['p']}")
        await ctx.close()
        # ---- C3 e C4: attestato salvato col pulsante, caricato su una carriera già in Deriva
        ctx, q = await pagina(BREV, "scuola", scarica=True)
        await q.evaluate("() => openAttest()")
        async with q.expect_download() as dl: await q.click("#atSalva")
        f = await (await dl.value).path(); attTesto = pathlib.Path(f).read_text(); A = json.loads(attTesto)
        A["meriti"] = {"abil": 13, "cono": 9, "comp": 5, "esp": 6}; attTesto = json.dumps(A)   # punti diversi da 0 (la carriera di prova li ha a 0): così C3 misura davvero che l'attestato li legge dal file
        print("attestato salvato:", (await dl.value).suggested_filename, attTesto[:200], flush=True)
        await ctx.close()
        ctx, q = await pagina(BREV, "deriva", benv=True)
        await q.evaluate("() => { progress.stagione = stNuova(null, 'zon'); const D = spDati(); D.c = { ...spOfferta(2, 1), esiti: [] }; progress.deriva = { data: '2026-11-18', strada: 'merito' }; progress.dvBenvenuto = '2026-11-01'; ghosts = { a: 1 }; saveProgress(); saveGhosts(); }")
        r = await q.evaluate("t => attCarica(t)", attTesto); await q.wait_for_timeout(200)
        s = await q.evaluate("""() => ({ brev: progress.brevetto, exam: progress.exam, st: !!progress.stagione, sp: !!progress.sponsor && !!progress.sponsor.c, dv: !!progress.deriva, done: Object.keys(progress.done).length,
            best: Object.keys(progress.best).length, gh: Object.keys(ghosts).length, liv: localStorage.getItem('scuolaVelaLivello'), menuDeriva: (document.querySelector('#livSel [data-v=deriva]') || {}).getAttribute?.('aria-pressed'),
            benv: document.getElementById('derivaDlg').open, benvT: document.getElementById('dvTitle') && document.getElementById('dvTitle').textContent, off: progress.sponsor ? progress.sponsor.offerte.map(o => o.g) : null })""")
        print("C3 dopo l'attestato:", s, flush=True)
        chk("C3", r == "" and s["brev"]["file"]["meriti"] == A["meriti"] and s["exam"]["superato"] and not s["st"] and not s["sp"] and not s["dv"] and s["done"] == 0 and s["best"] == 0 and s["gh"] == 0
            and s["liv"] == "deriva" and s["menuDeriva"] == "true", f"C3 attestato su una carriera in Deriva: {s}")
        chk("C4", s["benv"] and s["benvT"] == "Benvenuto in Deriva", f"C4 benvenuto subito dopo l'attestato: aperto {s['benv']}, titolo {s['benvT']}")
        chk("C5", s["off"] == [1, 2], f"C5 sponsor all'entrata dopo l'attestato: offerte {s['off']}")
        m = await q.evaluate(ECC); dlg = await q.evaluate("() => { const r = document.getElementById('derivaDlg').getBoundingClientRect(); return [r.top, r.bottom]; }")
        chk("C7", m == 0 and dlg[0] >= 0 and dlg[1] <= 650, f"C7 benvenuto a 1360x650: eccesso {m} px, finestra da {dlg[0]:.0f} a {dlg[1]:.0f}")
        await q.evaluate("() => document.getElementById('derivaDlg').close()")
        aperte = 0
        for _ in range(3):
            await q.evaluate("() => __sv.st.showMenu()"); aperte += await q.evaluate("() => { const d = document.getElementById('derivaDlg'), o = d.open; d.close(); return o ? 1 : 0; }")
        chk("C4", aperte == 0, f"C4 riaprendo il menu 3 volte il benvenuto non torna: aperture {aperte}")
        await q.click("#livSel [data-v=scuola]"); await q.wait_for_timeout(150)
        lib = await q.evaluate("() => document.getElementById('libManca').textContent"); await q.click("#goAttest"); await q.wait_for_timeout(150)
        punti = await q.evaluate("() => [...document.querySelectorAll('#atBody li')].map(l => l.textContent)")
        attese = [f"{n}: {A['meriti'][k]} / " for k, n in (("abil", "Abilità"), ("comp", "Competizione"), ("cono", "Conoscenza"), ("esp", "Esperienza"))]
        chk("C3", "caricato da un file" in lib and len(punti) == 4 and all(any(x.startswith(a) for x in punti) for a in attese), f"C3 libretto {lib!r}; attestato {punti}, attesi {attese}")
        m = await q.evaluate(ECC); chk("C7", m == 0, f"C7 menu della Scuola in carriera (dopo l'attestato): eccesso {m} px")
        await ctx.close()
        # C4: carriera con brevetto, mai vista Deriva → una volta sola; nel gioco libero mai
        ctx, q = await pagina({**BREV, "nazionale": True}, "deriva", benv=True)
        aperte = 0; off0 = await q.evaluate("() => JSON.stringify(progress.sponsor || null)")
        for _ in range(3):
            await q.evaluate("() => __sv.st.showMenu()"); aperte += await q.evaluate("() => { const d = document.getElementById('derivaDlg'), o = d.open; d.close(); return o ? 1 : 0; }")
        off1 = await q.evaluate("() => JSON.stringify(progress.sponsor || null)")
        chk("C4", aperte == 1, f"C4 carriera col brevetto, 3 aperture del menu di Deriva: benvenuto {aperte} volte")
        chk("C5", off1 == off0, f"C5 carriera col diritto al nazionale già preso: sponsor invariato ({off0} → {off1})")
        m = await q.evaluate(ECC); chk("C7", m == 0, f"C7 menu di Deriva in carriera: eccesso {m} px")
        await q.evaluate("() => { localStorage.setItem('scuolaVelaSim.v1', JSON.stringify({ done: {}, best: {}, clean: {} })); }")
        await q.click("#modoSel [data-v=libero]"); await q.wait_for_timeout(200)
        await q.evaluate("() => { progress.dvBenvenuto = undefined; __sv.st.showMenu(); }")
        lib = await q.evaluate("() => document.getElementById('derivaDlg').open")
        chk("C4", not lib, f"C4 gioco libero in Deriva: benvenuto aperto {lib}")
        await ctx.close()
        ctx, q = await pagina({**BREV}, "deriva", benv=True)
        await q.evaluate("() => { progress.stagione = stNuova(null, 'zon'); delete progress.dvBenvenuto; saveProgress(); __sv.st.showMenu(); }")
        s = await q.evaluate("() => ({ benv: document.getElementById('derivaDlg').open, off: progress.sponsor ? progress.sponsor.offerte.length : 0 })")
        chk("C5", s["benv"] and s["off"] == 0, f"C5 carriera con una stagione già cominciata: benvenuto {s['benv']}, offerte {s['off']} (attese 0)")
        await ctx.close()
        # ---- C6: gradino 1 finito con lo zonale fra i primi 3 → offerta nazionale; oltre il 3° no
        ctx, q = await pagina(BREV)
        await q.evaluate("() => __seed(777)")
        visti = {"primi3": 0, "oltre": 0}; err6 = 0
        for k in range(120):
            await q.evaluate("() => { const D = spDati(); D.c = { ...spOfferta(1, 1), esiti: [] }; D.offerte = []; }")
            d = await q.evaluate(STAG, ["zon", 0]); D = await q.evaluate("() => JSON.parse(JSON.stringify(spDati()))")
            naz = any(o["circ"] == "naz" for o in D["offerte"]); chiave = "primi3" if d["pos"] <= 3 else "oltre"; visti[chiave] += 1
            if naz != (d["pos"] <= 3): err6 += 1; print(f"  C6 stagione {k}: {d['pos']}° → offerte {[(o['g'], o['circ']) for o in D['offerte']]}", flush=True)
            if visti["primi3"] >= 5 and visti["oltre"] >= 5: break
        chk("C6", err6 == 0 and visti["primi3"] >= 5 and visti["oltre"] >= 5, f"C6 contratti del gradino 1 finiti: fra i primi 3 {visti['primi3']}, oltre {visti['oltre']}, sbagliati {err6}")
        await ctx.close()
        # ---- C8: come un giocatore
        d0 = len(dialoghi)
        ctx, q = await pagina(BREV, "deriva", hash_="", scarica=True)
        ben = await q.evaluate("() => document.getElementById('derivaDlg').open"); await q.keyboard.press("Escape"); await q.wait_for_timeout(150)
        chk("C4", ben, f"C4 pagina senza #collaudo: benvenuto aperto entrando in Deriva {ben}")
        orig = await q.evaluate("() => localStorage.getItem('scuolaVelaCarriera.v1')")
        async with q.expect_download() as dl: await q.click("#carSalva")
        dov = await (await dl.value).path(); nomef = (await dl.value).suggested_filename
        tmp = pathlib.Path(tempfile.mkdtemp()) / nomef; tmp.write_bytes(pathlib.Path(dov).read_bytes())
        await q.evaluate("() => { localStorage.removeItem('scuolaVelaCarriera.v1'); }"); await q.reload(); await q.wait_for_timeout(300)
        await q.keyboard.press("Escape"); await q.wait_for_timeout(100)
        async with q.expect_file_chooser() as fc: await q.click("#carCarica")
        await (await fc.value).set_files(str(tmp)); await q.wait_for_timeout(600)
        dopo = await q.evaluate("() => localStorage.getItem('scuolaVelaCarriera.v1')")
        sv = await q.evaluate("() => typeof window.__sv")
        chk("C8", dopo == orig and sv == "undefined" and nomef.startswith("carriera-") and any(t == "confirm" for t, _ in dialoghi[d0:]), f"C8 pagina senza #collaudo: file {nomef}, salvataggio identico {dopo == orig}, conferma chiesta {[t for t, _ in dialoghi[d0:]]}")
        await ctx.close()
        chk("C8", not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
