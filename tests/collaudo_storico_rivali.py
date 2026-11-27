# Lo storico dei rivali, passo 1 (1.3.37, voce 74, docs/PROPOSTA-STORICO-RIVALI.md). Soglie scritte nella proposta (40 tornei, 500 confronti); dopo la revisione di Opus (21 nov)
# aggiunti R1b (casi difficili costruiti a mano, perché col pilota i contatti sono rari), il conteggio dei casi per tipo e la misura del pannello sulla finestra giusta (torDlg).
#   R1 lo storico dice il vero: per ogni rivale i nove contatori dello storico (regate, davanti, dietro, partenza davanti/dietro, fuori linea, contatti, colpa sua, colpa tua) uguali a quelli
#      ricalcolati QUI dal registro delle regate del torneo (tor.ris), con un calcolo scritto nel collaudo (non quello del gioco); 0 righe diverse e almeno 500 confronti
#   R2 dura: pagina chiusa e riaperta fra due tornei: storico identico; un salvataggio senza progress.rivali si apre con storico vuoto, la scheda si apre e 0 errori
#   R3 (Chromium e Firefox; fino al 24 nov in Firefox era solo riportato, per un difetto del collaudo: due evaluate nella stessa pagina) il passo 1 non cambia la regata: con la marcatura della 1.3.50 spenta, arrivi, penalità e giri uguali al bit alla 1.3.36 (commit ba7c653, senza storico), 5 tornei da 4 regate (20 regate)
#   R4 identità: lo stesso nome in due tornei di fila nella stessa pagina si somma (contatori = somma dei due); due rivali con lo stesso colore e nomi diversi restano separati
#   R1b casi costruiti: 200 registri a mano (contatti di ogni colpa, fuori linea, squalifiche, giocatore o rivale non arrivato, linea mancante) contro `atteso()`; ogni tipo almeno 10 volte
#   R5 finestra dei rivali (torDlg e torBody): la scheda con lo storico lungo (999 regate) a 1360x650 senza eccesso, con 3 e con 5 rivali
#   R6 come un giocatore: pagina senza #collaudo, due tornei di fila giocati col menu (regate chiuse col ritiro per rapidità): lo storico cresce, 0 errori
# Uso: python tests/collaudo_storico_rivali.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, subprocess, tempfile, json
import metro
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
RIF = "v1.3.71"   # 1.3.36 (ba7c653) fino al 27 nov 2026; # 27 nov 2026 (voce 92): dalla barca M (1.3.59-1.3.61) nessuna regata può essere identica a una versione di prima; riferimento la 1.3.61: ora è solo una guardia di non-regressione (la prova della funzione è stata fatta quando è nata)
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
R3_ATTESA = int(os.environ.get("R3_ATTESA", 0)); R3_MARCA = os.environ.get("R3_MARCA") == "1"   # controprove di R3: attesa in più (il conto non deve cambiare); marcatura accesa (il conto deve scendere)
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
CAMPI = ["n", "dav", "die", "pDav", "pDie", "fuori", "cont", "cS", "cT"]
def atteso(ris_lista, i):
    """contatori attesi per il rivale i (indice nella regata) dal registro; calcolo nostro"""
    st = dict.fromkeys(CAMPI, 0)
    for r in ris_lista:
        def pos(j):
            x = r[j]
            if x.get("fin") is None or x.get("dsq"): return 0
            return 1 + sum(1 for y in r if y.get("fin") is not None and not y.get("dsq") and y["fin"] < x["fin"])
        rp, mp = pos(i), pos(0); x = r[i]; st["n"] += 1
        if rp and (not mp or rp < mp): st["dav"] += 1
        elif mp and (not rp or rp > mp): st["die"] += 1
        if x.get("x"): st["fuori"] += 1
        else:
            l, l0 = x.get("l"), r[0].get("l")
            if l is not None and l0 is not None:
                if l < l0: st["pDav"] += 1
                else: st["pDie"] += 1
            elif l is not None and l0 is None: st["pDav"] += 1   # il giocatore non ha registrato la linea: «davanti» (come torDavanti)
        c = x.get("c") or ""
        if c:
            st["cont"] += 1; st["cS"] += "s" in c; st["cT"] += "t" in c
    return st
CORRI = """async ([ritiro, seme]) => { const sv = __sv, dt = 1 / 60; if (seme !== undefined) __seed(seme); document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0];
  if (ritiro){ window.confirm = () => true; document.getElementById("rRet").click(); sv.run(dt, 1); }
  else while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); }
  const boats = R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, !!b.dsq, b.me ? R.need || 0 : 0, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(','));
  document.getElementById("rTor").click(); return boats.join('|'); }"""
LEGGI = """() => { const T = __sv.tor; return { ris: T ? JSON.parse(JSON.stringify(T.ris)) : null, nomi: T ? T.av.map(a => a.nome) : null,
  st: JSON.parse(JSON.stringify(Object.fromEntries(Object.entries((JSON.parse(localStorage.getItem(__sv.store)) || {}).rivali || {}).filter(([k, v]) => v.st).map(([k, v]) => [k, v.st])))) }; }"""
async def pagina(b, url=BASE + "#collaudo", seme=True, w=1360, h=650):
    ctx = await b.new_context(viewport={"width": w, "height": h})
    if seme: await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg, errs
async def apri(pg, seme):
    await pg.evaluate("(s) => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", seme)
async def torneo(pg, seme, ritiro=False):
    """un torneo intero (4 regate); ritorna regate e nomi (dall'ultima lettura prima della fine) e le firme delle regate"""
    await apri(pg, seme); firme = []; nomi = None; ris = None
    for k in range(4):
        firme.append(await pg.evaluate(CORRI, [ritiro]))
        d = await pg.evaluate(LEGGI)
        if d["ris"] is not None and d["nomi"]: ris, nomi = d["ris"], d["nomi"]
    return ris, nomi, firme
async def torneo_r3(b, url, seme, attesa=0):
    """le firme delle 4 regate, una pagina nuova per regata e il seme rimesso dentro la corsa (24 nov, come K2 di collaudo_marcatura: i fotogrammi disegnati fra due evaluate usano numeri a caso, disegno.js draw)"""
    firme = []; T = RV = None
    for k in range(4):
        ctx, pg, errs = await pagina(b, url=url)
        await pg.evaluate("(m) => { if (__sv.marca) __sv.marca(m); if (__sv.manovre) __sv.manovre(false); }", R3_MARCA)   # dalla 1.3.50 l'ultima regata cambia apposta se un rivale marca: qui si misura solo lo storico (la marcatura la misura collaudo_marcatura.py)
        if k: await pg.evaluate("([T, RV]) => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; progress.torneo = T; progress.rivali = RV; __sv.torApri(); }", [T, RV])
        else: await apri(pg, seme)
        if attesa: await pg.wait_for_timeout(attesa)
        firme.append(await pg.evaluate(CORRI, [False, seme * 1000 + k]))
        if k < 3: T, RV = await pg.evaluate("() => [JSON.parse(JSON.stringify(__sv.tor)), JSON.parse(JSON.stringify(progress.rivali || {}))]")
        await ctx.close()
    return firme
PH = "()=>{const p=document.querySelector('.panel');return p.scrollHeight-p.clientHeight}"
def attesi(tors):
    out = {}
    for ris, nomi in tors:
        for i, nome in enumerate(nomi, 1):
            a = atteso(ris, i); o = out.setdefault(nome, dict.fromkeys(CAMPI, 0))
            for c in CAMPI: o[c] += a[c]
    return out
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        # ---- R1, R4 (somma), R2 (dura): sessioni da due tornei nella stessa pagina; 20 sessioni = 40 tornei, 160 regate ----
        confronti, diff, errori, nomi_tot, sovr = 0, [], [], 0, 0; tipi = dict.fromkeys(CAMPI, 0); ris_tutte = []
        for sess in range(20):
            ctx, pg, errs = await pagina(b); sem = [sess * 2 + 1, sess * 2 + 2] if sess >= 3 else [sess * 2 + 1, sess * 2 + 1]   # le prime 3 sessioni: stesso seme due volte = stessi nomi (R4)
            tors = []
            for sd in sem:
                ris, nomi, _ = await torneo(pg, sd)
                if not ris or len(ris) != 4: errori.append(("registro", sess, sd, None if not ris else len(ris))); continue
                tors.append((ris, nomi))
            st = (await pg.evaluate(LEGGI))["st"]; att = attesi(tors)
            for nome, a in att.items():
                got = st.get(nome, {})
                for c in CAMPI:
                    confronti += 1
                    if got.get(c, -1) != a[c]: diff.append((sess, nome, c, got.get(c), a[c]))
            sovr += sum(1 for nome in att if len([t for t in tors if nome in t[1]]) == 2) if sess >= 3 else 0
            if set(st) != set(att): diff.append((sess, "nomi", sorted(set(st) ^ set(att))))
            nomi_tot += len(att); ris_tutte.append((sess, tors))
            for nome, a in att.items():
                for c in CAMPI: tipi[c] += a[c]
            if sess < 3 and tors and len(tors) == 2:   # R4: stessi nomi due volte: i contatori sono la somma dei due tornei (quindi pari al doppio se identici)
                chk(tors[0][1] == tors[1][1] and all(st[n]["n"] == 8 for n in tors[0][1]), f"R4 sessione {sess}: stesso seme, stessi nomi {tors[0][1]}, regate per ciascuno {[st[n]['n'] for n in tors[0][1]]} (attese 8)")
            if sess < 2:   # R2: pagina ricaricata, stesso salvataggio
                await pg.reload(); await pg.wait_for_timeout(300)
                st2 = await pg.evaluate("() => JSON.parse(JSON.stringify(Object.fromEntries(Object.entries(JSON.parse(localStorage.getItem('scuolaVelaSim.v1')).rivali || {}).filter(([k, v]) => v.st).map(([k, v]) => [k, v.st]))))")
                chk(st2 == st and len(st2) >= 3, f"R2 sessione {sess}: dopo la ricarica lo storico è identico ({len(st2)} rivali)")
                await pg.evaluate("() => { const p = JSON.parse(localStorage.getItem('scuolaVelaSim.v1')); delete p.rivali; localStorage.setItem('scuolaVelaSim.v1', JSON.stringify(p)); }")
                await pg.reload(); await pg.wait_for_timeout(300); await pg.evaluate("() => { __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); document.getElementById('torRivali').click(); }")
                vuoto = await pg.evaluate("() => ({ sch: document.querySelectorAll('.tor-sch').length, righe: [...document.querySelectorAll('.tor-sch')].filter(d => /Storico, [0-9]+ regat[ae] insieme/.test(d.textContent)).length })")
                chk(vuoto["sch"] >= 3 and vuoto["righe"] == 0 and not errs, f"R2 sessione {sess}: salvataggio senza progress.rivali, schede {vuoto['sch']}, righe di storico {vuoto['righe']}, errori {errs[:1]}")
            if errs: errori.append(("errore pagina", sess, errs[0]))
            await ctx.close()
        chk(not diff and confronti >= 500 and not errori, f"R1 {confronti} confronti su {nomi_tot} rivali in 40 tornei (160 regate), righe diverse {len(diff)}: {diff[:3]}, errori {errori[:2]}")
        print(f"RIPORTATO R1 casi visti dal pilota, per tipo (somma dei contatori): {tipi}", flush=True)
        print(f"RIPORTATO R4: rivali comparsi in due tornei diversi della stessa pagina (somma dentro R1): {sovr}", flush=True)
        # ---- R1b: registri costruiti, passati davvero a stoAgg ----
        import random
        rnd = random.Random(5); tipi_b = dict.fromkeys(["contS", "contT", "contST", "fuori", "dsq", "mioNonArr", "rivNonArr", "lMancante", "dav", "die"], 0); dif_b = []; n_b = 0
        ctx, pg, errs = await pagina(b); await apri(pg, 3); await pg.evaluate(CORRI, [True])   # una regata chiusa col ritiro: il torneo esiste
        for caso in range(200):
            r = []
            for j in range(4):
                x = {"fin": None if rnd.random() < 0.15 else round(rnd.uniform(300, 700), 1), "pp": 0}
                if rnd.random() < 0.1 and x["fin"] is not None: x["dsq"] = True
                if rnd.random() < 0.85: x["l"] = round(rnd.uniform(170, 200), 2)
                if j and rnd.random() < 0.1: x["x"] = True
                if j and rnd.random() < 0.3: x["c"] = rnd.choice(["s", "t", "st"])
                r.append(x)
            await pg.evaluate("([r, ] ) => { const T = __sv.tor; T.ris = [r]; for (const a of T.av) { progress.rivali[a.nome] = { ...(progress.rivali[a.nome] || {}) }; delete progress.rivali[a.nome].st; } __sv.stoAgg(T, 0); }", [r])
            got = await pg.evaluate("() => { const T = __sv.tor; return T.av.map(a => progress.rivali[a.nome].st); }")
            for i in range(1, 4):
                a = atteso([r], i); n_b += 1
                if got[i - 1] != a: dif_b.append((caso, i, got[i - 1], a))
                x = r[i]; c = x.get("c", "")
                tipi_b["contS"] += c == "s"; tipi_b["contT"] += c == "t"; tipi_b["contST"] += c == "st"; tipi_b["fuori"] += bool(x.get("x")); tipi_b["dsq"] += bool(x.get("dsq")) or bool(r[0].get("dsq"))
                tipi_b["mioNonArr"] += r[0]["fin"] is None; tipi_b["rivNonArr"] += x["fin"] is None; tipi_b["lMancante"] += "l" not in x or "l" not in r[0]
                tipi_b["dav"] += a["dav"]; tipi_b["die"] += a["die"]
        chk(not dif_b and n_b == 600 and all(v >= 10 for v in tipi_b.values()), f"R1b {n_b} confronti su registri costruiti, differenze {len(dif_b)}: {dif_b[:2]}; casi per tipo {tipi_b}")
        await ctx.close()
        # ---- R3: arrivi identici alla 1.3.36 ----
        tmp = tempfile.mkdtemp(); subprocess.run(f"git -C {ROOT} archive {RIF} index.html js | tar -x -C {tmp}", shell=True, check=True)
        VECCHIA = pathlib.Path(tmp, "index.html").as_uri() + "#collaudo"
        uguali = tot = 0
        for seme in range(101, 106):
            f = []
            for url in (BASE + "#collaudo", VECCHIA):
                f.append(await torneo_r3(b, url, seme, R3_ATTESA if url != VECCHIA else 0))
            for x, y in zip(*f): tot += 1; uguali += x == y
        chk(tot == 20 and uguali == 20, f"R3 {uguali} regate su {tot} identiche al bit alla 1.3.68 (arrivi, penalità, giri, posizioni finali)")
        # ---- R5: pannello ----
        for n6 in (False, True):
            ctx, pg, errs = await pagina(b); await apri(pg, 7)
            if n6: await pg.evaluate("() => document.getElementById('torN6').click()")
            for k in range(3): await pg.evaluate(CORRI, [True])
            sv = await pg.evaluate("""() => { const T = __sv.tor; T.av.forEach(a => { progress.rivali[a.nome] = { ...progress.rivali[a.nome], st: { n: 999, dav: 321, die: 678, pDav: 400, pDie: 500, fuori: 99, cont: 250, cS: 150, cT: 100 } }; });
              document.getElementById('torRivali').click(); const out = [];
              for (let n = 0; n < T.av.length; n++){ document.querySelectorAll('.tor-ling')[n].click(); const d = document.getElementById('torDlg'), q = document.getElementById('torBody'); out.push([Math.max(d.scrollHeight - d.clientHeight, q.scrollHeight - q.clientHeight, 0), /Storico, 999 regate insieme/.test(document.querySelector('.tor-sch:not([hidden])').textContent)]); }
              return out; }""")
            chk(len(sv) >= 3 and all(a <= 0 and r for a, r in sv), f"R5 scheda con storico lungo, {len(sv)} rivali ({'6 barche' if n6 else '4 barche'}): eccesso della finestra {[a for a, _ in sv]} px, riga presente {all(r for _, r in sv)}")
            await ctx.close()
        # ---- R6: come un giocatore ----
        ctx, pg, errs = await pagina(b, url=BASE, seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        await pg.wait_for_timeout(1500); await pg.click("#rRet"); await pg.wait_for_timeout(300); await pg.click("#finTor"); await pg.wait_for_timeout(500)   # a regata finita i pulsanti stanno nel riquadro sul mare (#finTor), come in collaudo_torneo C7
        s1 = await pg.evaluate("() => { const k = Object.keys(localStorage).filter(k => /scuolaVela/.test(k)); let tot = {}; for (const key of k){ try { const r = JSON.parse(localStorage.getItem(key)).rivali || {}; for (const [n, v] of Object.entries(r)) if (v.st) tot[n] = v.st.n; } catch (e) {} } return tot; }")
        chk(len(s1) >= 3 and all(v == 1 for v in s1.values()) and not errs, f"R6 pagina da giocatore, una regata chiusa col ritiro: storico di {len(s1)} rivali con 1 regata, errori {errs[:1]}")
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
