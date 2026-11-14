# Stagione con un amico (1.2.37, docs/PROPOSTA-STAGIONE-ZONALE.md, «Lucio dodicesimo: fermata 2»; soglie scritte prima del codice).
#   Z8  stesso codice, stessa stagione: 20 codici, Chromium contro Firefox, per tutti e due i ruoli (chi crea "A", chi entra "B"): tappe, venti, gruppo,
#       batterie e, per ogni tappa, direzioni del vento, rivali, carattere e numeri di guida (torNuovo) identici; e la stagione vista da A e da B è la stessa.
#   Z15 stessa classifica nelle due pagine: 20 stagioni, pagina A in Chromium e pagina B in Firefox, tappe chiuse con risultati scritti dal collaudo
#       e file scambiati dopo ogni tappa: classifica del circuito identica dopo ogni tappa.
#   Z9  il risultato dell'amico entra com'è: in ogni tappa, nell'ordine della tappa, la batteria dell'amico è nell'ordine del suo file e la tua nel tuo.
#   Z10 conti: dopo lo scambio ogni tappa ha i posti 1..12 (somma 78); prima dello scambio l'amico è «in attesa» e gli 11 presenti fanno 66.
#   Z11 file sbagliati: altra stagione, altra versione, proprio ruolo, file rovinato, ordine impossibile: rifiutati con un messaggio, stagione invariata, 5 su 5.
#   Z7  pannello a 1360x650: finestra «Con un amico», presentazione col codice, circuito con 12 righe dopo 4 tappe; file salvato e caricato dai pulsanti veri.
#   --pilota N: N tappe della stagione con un amico corse davvero col pilota (la tua batteria nell'ordine del torneo).
#   --vera: pagina senza #collaudo, Chromium e Firefox: entrare con un codice e cominciare la stagione, 0 errori.
import asyncio, json, pathlib, random, re, sys, tempfile
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent
BASE = (QUI.parent / "index.html").as_uri()
PIL = int(sys.argv[sys.argv.index("--pilota") + 1]) if "--pilota" in sys.argv else 0
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
errori = []
def no(m): errori.append(m); print("  NO  " + m, flush=True)

async def pagina(bt, coll=True, nome=""):
    ctx = await bt.new_context(viewport={"width": 1360, "height": 650}, accept_downloads=True)
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    pg.on("pageerror", lambda e: no(f"errore pagina {nome}: {e}"))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + ("#collaudo" if coll else "")); await pg.wait_for_timeout(300)
    if coll: await pg.evaluate("() => { __sv.fast(0); }")
    return pg

# la stagione vista da un ruolo, riportata alla forma comune (A, B, batterie gialla-bianca-arancione), con i tornei di ogni tappa
VISTA = """([seme, liv, io]) => { const sv = __sv, S = sv.st.nuova({ seme, liv, io }), altro = io === "A" ? "B" : "A", can = id => id === "*" ? io : id === "@" ? altro : id;
  const tappe = S.tappe.map(t => { const b = [], col = t.col; t.bat.forEach((x, i) => { b[col[i]] = x.map(can); }); return { posto: t.posto, tws: t.tws, bat: b }; });
  const tornei = S.tappe.map((t, j) => { S.tappe.forEach((u, k) => { if (k < j) u.mio = u.bat[0].slice(); else delete u.mio; });
    const T = sv.st.torNuovo(S); return { liv: T.liv, st: T.st, regate: T.regate, av: T.av }; });
  return { codice: S.codice, liv: S.liv, gruppo: S.gruppo, canon: S.canon.map(can), tappe, tornei }; }"""

def finto(rnd, bat):   # risultati di un torneo scritti dal collaudo: 4 regate, 4 barche
    av = [{"nome": n} for n in bat[1:]]
    ris = [[dict(fin=None if rnd.random() < 0.05 else round(600 + rnd.random() * 120, 1), pp=0, **({"c": rnd.choice("st")} if i and rnd.random() < 0.3 else {})) for i in range(4)] for _ in range(4)]
    return {"av": av, "ris": ris}

PANNELLO = """() => { const d = document.getElementById('torDlg'), q = document.getElementById('torBody'), r = d.getBoundingClientRect();
  const btn = [...q.querySelectorAll('button')].map(b => b.getBoundingClientRect().bottom);
  return { aperto: d.open, dentro: r.top >= 0 && r.bottom <= innerHeight, scorreRiquadro: d.scrollHeight - d.clientHeight, scorreContenuto: q.scrollHeight - q.clientHeight,
           larg: Math.max(d.scrollWidth - d.clientWidth, q.scrollWidth - q.clientWidth), pulsanti: btn.length && btn.every(b => b <= r.bottom && b <= innerHeight) }; }"""
def pannello(o, cosa):
    print(f"  Z7 {cosa}: {o}")
    if not o["aperto"] or not o["dentro"] or o["scorreRiquadro"] > 0 or o["scorreContenuto"] > 0 or o["larg"] > 0 or not o["pulsanti"]: no(f"Z7 {cosa}: {o}")

CLAS = """() => { const S = __sv.progress.stagione, io = S.io, altro = io === "A" ? "B" : "A", can = id => id === "*" ? io : id === "@" ? altro : id;
  return { cl: __sv.st.classifica(S).map(x => [can(x.id), x.p, x.tot, x.manca]), ord: S.tappe.map(t => { const o = __sv.st.ordine(S, t); return o && o.map(can); }),
           mio: S.tappe.map(t => t.mio ? t.mio.map(can) : null), amico: S.amico ? S.amico.tappe.map(o => o && o.map(can)) : null, bat: S.tappe.map(t => t.bat.map(b => b.map(can))),
           frasi: __sv.st.frasi(S) }; }"""

CORRI = """async () => { const sv = __sv, dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0];
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ if (me.fin === null && !me.dnf) sv.pilota(dt); sv.run(dt, 1); }
  if (me.fin === null && !me.dnf) return { fallita: "pilota non arrivato" };
  document.getElementById("rTor").click(); return { ok: true }; }"""

async def main():
    async with async_playwright() as p:
        ch = await p.chromium.launch(); ff = await p.firefox.launch()
        pc = await pagina(ch, nome="Chromium"); pf = await pagina(ff, nome="Firefox")
        # Z8
        uguali = 0
        for k in range(20):
            seme = (k * 104729 + 12345) % (1 << 30); liv = "esperti" if k % 2 else "principianti"
            v = {}
            for nome, pg in (("C", pc), ("F", pf)):
                for io in "AB": v[nome + io] = await pg.evaluate(VISTA, [seme, liv, io])
            stessi = v["CA"] == v["FA"] and v["CB"] == v["FB"]
            strutt = all(v["CA"][x] == v["CB"][x] for x in ("codice", "liv", "gruppo", "canon", "tappe"))
            letto = await pc.evaluate("c => __sv.st.leggi(c)", v["CA"]["codice"])
            if stessi and strutt and letto == {"seme": seme, "liv": liv}: uguali += 1
            else: no(f"Z8 codice {v['CA']['codice']}: browser uguali {stessi}, A e B uguali {strutt}, codice riletto {letto}")
        print(f"Z8: {uguali} codici su 20 con la stessa stagione in Chromium e Firefox, per chi crea e per chi entra")
        # Z15, Z9, Z10
        rnd = random.Random(37); ok15 = 0; tappe = 0
        for k in range(20):
            seme = (k * 7919 + 777) % (1 << 30)
            for pg, io in ((pc, "A"), (pf, "B")):
                await pg.evaluate("([seme, io]) => { const sv = __sv; delete sv.progress.torneo; sv.progress.stagione = sv.st.nuova({ seme, liv: 'principianti', io }); }", [seme, io])
            buono = True
            for j in range(4):
                for pg in (pc, pf):
                    bat = await pg.evaluate("j => __sv.progress.stagione.tappe[j].bat[0]", j)
                    await pg.evaluate("T => __sv.st.chiudi(T)", finto(rnd, bat))
                # prima dello scambio: l'amico in attesa, 66 sugli 11
                for pg, io in ((pc, "A"), (pf, "B")):
                    c = await pg.evaluate(CLAS)
                    o = c["ord"][j]; altro = "B" if io == "A" else "A"
                    if len(o) != 11 or altro in o: no(f"Z10 stagione {k} tappa {j + 1} ({io}): prima del file l'ordine ha {len(o)} concorrenti")
                    am = [x for x in c["cl"] if x[0] == altro][0]
                    if not am[3]: no(f"Z10 stagione {k} tappa {j + 1} ({io}): l'amico non risulta in attesa")
                # scambio dei file
                fa = await pc.evaluate("() => __sv.st.file(__sv.progress.stagione)"); fb = await pf.evaluate("() => __sv.st.file(__sv.progress.stagione)")
                ea = await pc.evaluate("t => __sv.st.carica(__sv.progress.stagione, t)", fb); eb = await pf.evaluate("t => __sv.st.carica(__sv.progress.stagione, t)", fa)
                if ea or eb: no(f"Z15 stagione {k} tappa {j + 1}: file rifiutato: {ea} / {eb}"); buono = False; continue
                ca = await pc.evaluate(CLAS); cb = await pf.evaluate(CLAS)
                if ca["cl"] != cb["cl"] or ca["ord"] != cb["ord"]: no(f"Z15 stagione {k} tappa {j + 1}: classifiche diverse\n    A {ca['cl']}\n    B {cb['cl']}"); buono = False
                for c, io in ((ca, "A"), (cb, "B")):
                    altro = "B" if io == "A" else "A"
                    for i in range(j + 1):
                        o = c["ord"][i]
                        if sorted(o) != sorted(x for b in c["bat"][i] for x in b) or len(o) != 12: no(f"Z10 stagione {k} tappa {i + 1} ({io}): {len(o)} concorrenti")
                        mia = [x for x in o if x in c["bat"][i][0]]; sua = [x for x in o if x in c["bat"][i][1]]
                        if mia != c["mio"][i] or sua != c["amico"][i]: no(f"Z9 stagione {k} tappa {i + 1} ({io}): batterie non nell'ordine dei file")
                    if sum(x[2] for x in c["cl"]) != 78 * (j + 1): no(f"Z10 stagione {k} dopo la tappa {j + 1} ({io}): somma {sum(x[2] for x in c['cl'])}")
                    if len(c["frasi"]) > 3: no(f"frasi: {len(c['frasi'])}")
                tappe += 1
            if buono: ok15 += 1
        print(f"Z15: {ok15} stagioni su 20 con la stessa classifica nelle due pagine dopo ogni tappa ({tappe} tappe scambiate); Z9 e Z10 controllati in ogni tappa")
        # Z11 nella pagina A (stagione dell'ultimo giro, 4 tappe, file di B già caricato)
        casi = {
            "altra stagione": "t => { const f = JSON.parse(t); f.codice = '000000-P'; return JSON.stringify(f); }",
            "altra versione": "t => { const f = JSON.parse(t); f.ver = '1.2.36'; return JSON.stringify(f); }",
            "proprio ruolo": "t => __sv.st.file(__sv.progress.stagione)",
            "file rovinato": "t => t.slice(0, 40)",
            "ordine impossibile": "t => { const f = JSON.parse(t); f.tappe[0][1] = 'Mario Rossi'; return JSON.stringify(f); }",
        }
        rif = await pc.evaluate("() => JSON.stringify(__sv.progress.stagione)")
        rifiutati = 0
        for nome, fz in casi.items():
            t = await pc.evaluate(f"t => ({fz})(t)", fb)
            e = await pc.evaluate("t => __sv.st.carica(__sv.progress.stagione, t)", t)
            dopo = await pc.evaluate("() => JSON.stringify(__sv.progress.stagione)")
            print(f"  Z11 {nome}: «{e}»")
            if e and dopo == rif: rifiutati += 1
            else: no(f"Z11 {nome}: messaggio «{e}», stagione {'invariata' if dopo == rif else 'CAMBIATA'}")
        print(f"Z11: {rifiutati} casi su 5 rifiutati con un messaggio, stagione invariata")
        # Z7 e pulsanti veri: circuito di 12 dopo 4 tappe, salva e carica dai pulsanti
        await pc.evaluate("() => localStorage.setItem('scuolaVelaSim.nome', 'Alessandro Massimil')")
        await pc.evaluate("() => { __sv.torApri(); __sv.st.mostra('', false); }")
        pannello(await pc.evaluate(PANNELLO), "circuito con l'amico dopo 4 tappe"); await pc.screenshot(path=str(QUI / "output" / "stagione_amico_circuito.png"))
        async with pc.expect_download() as dl:
            await pc.evaluate("() => document.getElementById('stSalva').click()")
        d = await dl.value; salvato = pathlib.Path(tempfile.mkdtemp()) / d.suggested_filename; await d.save_as(salvato)
        fs = json.loads(salvato.read_text()); print(f"  file salvato dal pulsante: {d.suggested_filename}, ruolo {fs['ruolo']}, tappe {sum(1 for t in fs['tappe'] if t)}")
        atteso = await pc.evaluate("() => __sv.st.file(__sv.progress.stagione)")
        if fs != json.loads(atteso): no("il file salvato dal pulsante è diverso da stFile")
        fbp = pathlib.Path(tempfile.mkdtemp()) / "amico.json"; fbp.write_text(fb)
        await pc.set_input_files("#stFileIn", str(fbp)); await pc.wait_for_timeout(300)
        msg = await pc.evaluate("() => (document.querySelector('#torBody .manca') || {}).textContent")
        print(f"  file caricato dal pulsante: «{msg}»")
        if msg != "Risultato dell'amico caricato.": no(f"carica dal pulsante: {msg}")
        pannello(await pc.evaluate(PANNELLO), "circuito dopo il caricamento, con messaggio")
        fv = json.loads(fb); fv["ver"] = "1.2.36"; fbp.write_text(json.dumps(fv))
        await pc.set_input_files("#stFileIn", str(fbp)); await pc.wait_for_timeout(300)
        nf = await pc.evaluate("() => __sv.st.frasi(__sv.progress.stagione).length")
        # caso peggiore: 3 frasi. Se la stagione ne ha meno, si aggiungono nella finestra copie della frase più lunga possibile (detto nel risultato)
        await pc.evaluate("""() => { let u = document.querySelector('#torBody ul.st-frasi'); if (!u){ u = document.createElement('ul'); u.className = 'st-frasi'; document.querySelector('#torBody .row').before(u); }
          while (u.children.length < 3){ const li = document.createElement('li'); li.textContent = 'Alessandro Massimil e Tommaso Brunelli si giocano il primo posto del circuito: 2 punti fra loro.'; u.appendChild(li); } }""")
        pannello(await pc.evaluate(PANNELLO), f"circuito col messaggio di rifiuto più lungo, 3 frasi ({nf} vere)"); await pc.screenshot(path=str(QUI / "output" / "stagione_amico_rifiuto.png"))
        await pc.evaluate("() => { delete __sv.progress.stagione; __sv.torApri(); document.getElementById('stCirc').click(); document.getElementById('stAmico').click(); }")
        pannello(await pc.evaluate(PANNELLO), "finestra «Con un amico»"); await pc.screenshot(path=str(QUI / "output" / "stagione_amico_codice.png"))
        await pc.evaluate("() => document.getElementById('stCrea').click()")
        pannello(await pc.evaluate(PANNELLO), "presentazione col codice"); await pc.screenshot(path=str(QUI / "output" / "stagione_amico_presentazione.png"))
        await pc.evaluate("() => { document.getElementById('stIndietro').click(); document.getElementById('stCirc').click(); document.getElementById('stAmico').click(); document.getElementById('stCodIn').value = 'xyz'; document.getElementById('stEntra').click(); }")
        m = await pc.evaluate("() => (document.querySelector('#torBody .manca') || {}).textContent")
        print(f"  codice sbagliato: «{m}»")
        if not m: no("codice sbagliato accettato")
        # tappe corse davvero col pilota, stagione con un amico
        if PIL:
            await pc.evaluate("() => { delete __sv.progress.stagione; delete __sv.progress.torneo; __sv.torApri(); document.getElementById('stCirc').click(); document.getElementById('stAmico').click(); document.getElementById('stCodIn').value = '7K2M9Q-P'; document.getElementById('stEntra').click(); document.getElementById('stInizia').click(); }")
            for j in range(PIL):
                for r in range(4):
                    await pc.evaluate("s => __seed(s)", 4100 + j * 10 + r)
                    x = await pc.evaluate(CORRI)
                    if "fallita" in x: no(f"pilota tappa {j + 1} regata {r + 1}: {x['fallita']}")
                tab = await pc.evaluate("() => [...document.querySelectorAll('#torBody table.tor tbody tr')].map(tr => tr.children[1].textContent.replace(/ \\(barca \\w+\\)$/, ''))")
                c = await pc.evaluate(CLAS); nome = await pc.evaluate("() => (localStorage.getItem('scuolaVelaSim.nome') || '').trim() || 'Tu'")
                mio = [nome if x == "B" else x for x in c["mio"][j]]
                print(f"  tappa {j + 1} col pilota: torneo {tab}, salvato {mio}")
                if tab != mio: no(f"pilota tappa {j + 1}: la batteria salvata non è nell'ordine del torneo")
                await pc.evaluate("() => { document.getElementById('torMenu').click(); __sv.torApri(); }")
        await ch.close(); await ff.close()
        if "--vera" in sys.argv:
            for nome, bt in (("Chromium", p.chromium), ("Firefox", p.firefox)):
                br = await bt.launch(); n0 = len(errori)
                pg = await pagina(br, coll=False, nome=nome)
                await pg.evaluate("() => { const m = document.querySelector('#modoSel button[data-v=libero]'); m && m.click(); }")
                await pg.evaluate("() => document.getElementById('goTor').click()"); await pg.wait_for_timeout(100)
                await pg.evaluate("() => { document.getElementById('stCirc').click(); document.getElementById('stAmico').click(); }")
                await pg.fill("#stCodIn", "7k2m9q-e"); await pg.evaluate("() => document.getElementById('stEntra').click()")
                testo = await pg.evaluate("() => document.getElementById('torBody').innerText")
                await pg.evaluate("() => document.getElementById('stInizia').click()"); await pg.wait_for_timeout(100)
                tit = await pg.evaluate("() => document.getElementById('torTitle').textContent")
                ver = await pg.evaluate("() => document.querySelector('.ver') && document.querySelector('.ver').textContent")
                print(f"pagina vera {nome}: {ver}, «{tit}», codice nel testo: {'7K2M9Q-E' in testo}, errori {len(errori) - n0}")
                if tit != "Tappa 1 di 4" or "7K2M9Q-E" not in testo or len(errori) > n0: no(f"pagina vera {nome}")
                await br.close()
    print("\nESITO:", "OK" if not errori else f"FALLITO ({len(errori)})")
asyncio.run(main())
