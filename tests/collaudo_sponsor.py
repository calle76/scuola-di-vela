# Sponsor a contratto (1.3.9, tappa 4, docs/PROPOSTA-SPONSOR.md, criteri S1-S7 scritti prima). Pagina con #collaudo, carriera; stagioni «a numeri»:
# a ogni tappa l'ordine della tua batteria esce dallo stesso sorteggio dei rivali (stEstrai, tu con forza 0), e la tappa si chiude con stChiudiTappa.
#   S1 gli obiettivi dicono il vero: 200 stagioni (con tappe lasciate a caso): ogni obiettivo «raggiunto»/«mancato» ricontrollato qui sui dati salvati
#      (classifica, ordine di ogni tappa, tappe lasciate), 0 errori
#   S2 i gradini seguono la regola: le stesse stagioni in fila come una carriera (si accetta un'offerta a caso): ogni insieme di offerte a fine contratto è quello
#      della tabella, ricalcolato qui; mai sotto il gradino 1; sempre almeno 2 offerte, almeno una zonale
#   S3 obiettivi né impossibili né regalati: per ogni tipo, giocatore a forza 0, 2000 stagioni: raggiunto fra il 20% e l'80% (soglia della proposta);
#      «nessuna tappa lasciata» non si misura così (dipende solo da chi gioca) e si riporta a parte
#   S4 il Fiocco: primi 3 del nazionale → offerta, 200 su 200 di quei casi; altrimenti mai (a stato pulito)
#   S5 ricarica a metà contratto: uguale; «Azzera i progressi» lo cancella; un salvataggio della 1.2.39 col diritto si apre con l'offerta del gradino 3; il nazionale
#      senza sponsor nazionale non si apre, con sì
#   S6 le regate non cambiano: polare.js, raffiche_e_virate.js, impronta1b.js, collaudo_stagione e collaudo_nazionale (lanciati a parte)
#   S7 lo sponsor a 1360x650 con 3 offerte, un contratto con 2 obiettivi e il Fiocco: 0 px di eccesso; Chromium e Firefox, pagina senza #collaudo; 0 errori
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
BREV = {"done": {}, "best": {}, "clean": {}, "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}}
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    if not ok: fail.append(testo); print("FALLITO " + testo, flush=True)

# una stagione a numeri; lascia: probabilità di lasciare una tappa. Ritorna i dati per il ricontrollo
STAG = """([circ, lascia]) => { const S = progress.stagione = stNuova(null, circ);
  for (let k = 0; k < 4; k++){ const tp = stTappa(S);
    if (Math.random() < lascia){ stChiudiTappa(null); continue; }
    const T = torNuovo(S, tp.bat[0].length - 1), o = stEstrai(tp.bat[0]), nomi = ["*", ...T.av.map(a => a.nome)];
    T.ris = [0, 1, 2, 3].map(() => nomi.map(id => ({ fin: o.indexOf(id) + 1, pp: 0 }))); stChiudiTappa(T); }
  const cl = stClassifica(S);
  return { circ, cl: cl.map(x => [x.id, x.tot]), ordini: S.tappe.map(t => stOrdine(S, t)), rit: S.tappe.map(t => !!t.rit), pos: S.fine.pos }; }"""

def verifica(ob, d):   # l'obiettivo sui dati salvati, fatto qui
    ids = [x[0] for x in d["cl"]]
    if ob["t"] == "posto": return ids.index("*") + 1 <= ob["n"]
    if ob["t"] == "podio": return any(not r and 0 < o.index("*") + 1 <= 3 for o, r in zip(d["ordini"], d["rit"]) if "*" in o)
    if ob["t"] == "ritiri": return not any(d["rit"])
    return ids.index("*") < ids.index(ob["r"])

def regola(c, esiti):   # i gradini delle offerte a fine contratto, dalla tabella della proposta
    tutti = all(all(e) for e in esiti); qualcuno = any(any(e) for e in esiti)
    g = c["g"]; gr = sorted({g, min(4, g + 1)}) if tutti else [g] if qualcuno else [max(1, g - 1)]
    return gr

async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina(salv=BREV, hash_="#collaudo"):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
            q.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await q.add_init_script(SEME); await q.goto(BASE + hash_)
            await q.evaluate("d => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', 'carriera'); localStorage.setItem('scuolaVelaLivello', 'deriva'); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }", json.dumps(salv) if salv else None)
            await q.reload(); await q.wait_for_timeout(300); return ctx, q
        # ---- S1, S2, S4: una carriera di 200 stagioni a numeri
        ctx, q = await pagina()
        await q.evaluate("() => __seed(4242)")
        n_ob = err1 = err2 = fio_si = fio_ok = 0; viste_g = set(); passi = 0
        for k in range(200):
            D = await q.evaluate("() => JSON.parse(JSON.stringify(spDati()))")
            if D["offerte"]:   # si accetta un'offerta a caso
                i = await q.evaluate("O => Math.random() < 0.5 ? O.indexOf(Math.max(...O)) : Math.floor(Math.random() * O.length)", [o["g"] for o in D["offerte"]])   # metà delle volte la più alta: così la carriera arriva anche al gradino 4
                await q.evaluate("i => { const D = spDati(), o = D.offerte[i]; D.c = { ...o, esiti: [] }; D.offerte = []; }", i)
                D = await q.evaluate("() => JSON.parse(JSON.stringify(spDati()))")
            c = D["c"]; circ = c["circ"] if c else "zon"
            fio_prima = D.get("fiocco", False)
            d = await q.evaluate(STAG, [circ, 0.08])
            D2 = await q.evaluate("() => JSON.parse(JSON.stringify(spDati()))")
            if c:
                viste_g.add(c["g"])
                es = (D2["c"]["esiti"][-1] if D2["c"] else D2["storia"][-1]["esiti"][-1])
                for ob, v in zip(c["ob"], es):
                    n_ob += 1
                    if verifica(ob, d) != v: err1 += 1; print(f"  S1 stagione {k}: {ob} → gioco {v}, qui {verifica(ob, d)}", flush=True)
                if not D2["c"]:   # contratto finito: le offerte
                    passi += 1; att = regola(c, D2["storia"][-1]["esiti"]); og = [o["g"] for o in D2["offerte"]]
                    base = og[:len(att)]
                    ok = base == att and len(og) >= 2 and any(o["circ"] == "zon" for o in D2["offerte"]) and min(og) >= 1
                    if not ok: err2 += 1; print(f"  S2 stagione {k}: contratto {c['g']} esiti {D2['storia'][-1]['esiti']} → offerte {og}, attese {att} (+ riempimento)", flush=True)
            else:
                att = [2, 3] if d["pos"] <= 3 else [1, 2]; og = [o["g"] for o in D2["offerte"]]
                passi += 1
                if og[:2] != att: err2 += 1; print(f"  S2 prima stagione {k}: {d['pos']}° → offerte {og}, attese {att}", flush=True)
            if circ == "naz" and not fio_prima:
                if d["pos"] <= 3: fio_si += 1; fio_ok += 1 if D2.get("fiocco") else 0
                elif D2.get("fiocco"): fio_ok -= 1000
            if circ == "zon" and not fio_prima and D2.get("fiocco"): fio_ok -= 1000
        print(f"S1: {n_ob} obiettivi ricontrollati, {err1} sbagliati; S2: {passi} passaggi di offerte, {err2} sbagliati, gradini dei contratti visti {sorted(viste_g)}; S4: nazionali fra i primi 3 {fio_si}, Fiocco offerto {fio_ok}", flush=True)
        chk("S1", n_ob >= 200 and err1 == 0, f"S1 {n_ob} obiettivi, {err1} sbagliati")
        chk("S2", passi >= 50 and err2 == 0 and viste_g == {1, 2, 3, 4}, f"S2 {passi} passaggi, {err2} sbagliati, gradini visti {sorted(viste_g)}")
        chk("S4", fio_ok == fio_si, f"S4 Fiocco lungo la carriera: {fio_ok} su {fio_si}")
        # S4 costruito: 30 nazionali in cui finisci primo in ogni tappa e 30 in cui finisci ultimo, a stato pulito
        f4 = await q.evaluate("""() => { const r = { si: 0, no: 0 };
            for (const vinci of [true, false]) for (let s = 0; s < 30; s++){ progress.sponsor = { c: { g: 3, circ: "naz", nome: "x", durata: 1, ob: [{ t: "posto", n: 8 }], esiti: [] }, offerte: [], storia: [] };
              const S = progress.stagione = stNuova(null, "naz");
              for (let k = 0; k < 4; k++){ const tp = stTappa(S), T = torNuovo(S, tp.bat[0].length - 1), nomi = ["*", ...T.av.map(a => a.nome)];
                T.ris = [0, 1, 2, 3].map(() => nomi.map((id, i) => ({ fin: vinci ? i + 1 : (i === 0 ? 99 : i), pp: 0 }))); stChiudiTappa(T); }
              if (!!progress.sponsor.fiocco === (S.fine.pos <= 3)) r[vinci ? "si" : "no"]++; }
            return r; }""")
        chk("S4", f4["si"] == 30 and f4["no"] == 30, f"S4 Fiocco costruito: giusto in {f4['si']} nazionali vinti su 30 e {f4['no']} persi su 30")
        print("S4 costruito:", f4, flush=True)
        # ---- S3: forza 0, 2000 stagioni per circuito
        r = await q.evaluate("""() => { const out = {}; const conta = (k, v) => { out[k] = out[k] || [0, 0]; out[k][0] += v ? 1 : 0; out[k][1]++; };
            for (const circ of ["zon", "naz"]) for (let s = 0; s < 2000; s++){ const S = stNuova(null, circ);
              for (const tp of S.tappe) tp.ord = stEstrai(tp.bat.flat());
              S.fine = { pos: stClassifica(S).findIndex(x => x.id === "*") + 1 };
              const g = circ === "zon" ? [1, 2] : [3, 4];
              for (const gg of g) for (const d of [1, 2]) for (const ob of spObiettivi(gg, d)) if (ob.t !== "ritiri") conta(circ + " " + (ob.t === "posto" ? "entro il " + ob.n + "°" : ob.t === "davanti" ? "davanti a un rivale" : "podio di tappa"), spStato(ob, S).ok); }
            return out; }""")
        for k, (a, n) in sorted(r.items()):
            print(f"S3 {k}: {a} su {n} ({100 * a / n:.0f}%)", flush=True)
            chk("S3", 0.2 <= a / n <= 0.8, f"S3 {k}: {100 * a / n:.0f}% (soglia 20-80%)")
        await ctx.close()
        # ---- S5
        ctx, q = await pagina()
        await q.evaluate("() => __seed(77)"); await q.evaluate(STAG, ["zon", 0]); await q.evaluate("() => { const D = spDati(), o = D.offerte[0]; D.c = { ...o, durata: 2, esiti: [] }; D.offerte = []; }")
        await q.evaluate(STAG, ["zon", 0]); await q.evaluate("() => saveProgress()")
        prima = await q.evaluate("() => JSON.stringify(progress.sponsor)"); await q.reload(); await q.wait_for_timeout(300); dopo = await q.evaluate("() => JSON.stringify(progress.sponsor)")
        chk("S5", prima == dopo and json.loads(dopo)["c"] and len(json.loads(dopo)["c"]["esiti"]) == 1, f"S5 ricarica a metà contratto: uguale {prima == dopo}")
        await q.evaluate("() => { showMenu(); document.getElementById('resetProg').click(); }"); await q.wait_for_timeout(100)
        chk("S5", await q.evaluate("() => !progress.sponsor"), "S5 «Azzera i progressi» cancella lo sponsor")
        await ctx.close()
        v139 = {**BREV, "stagioneFatta": {"pos": 2}, "nazionale": True, "zonalePrimo": "Marta Ferraresi", "deriva": {"data": "2026-11-15", "strada": "piazzamento"}}
        ctx, q = await pagina(v139)
        await q.click("#goTor"); await q.click("#stCirc"); await q.wait_for_timeout(100)
        o = await q.evaluate("() => ({ g: progress.sponsor.offerte.map(o => o.g), naz: document.getElementById('stNaz').disabled, inizia: document.getElementById('stInizia').disabled })")
        chk("S5", 3 in o["g"] and o["naz"] and o["inizia"], f"S5 salvataggio della 1.2.39 col diritto: offerte {o['g']}, nazionale spento {o['naz']}, stagione ferma finché non si sceglie {o['inizia']}")
        await q.click("#stSponsor"); i3 = await q.evaluate("() => progress.sponsor.offerte.findIndex(o => o.g === 3)"); await q.click(f"#spOk{i3}"); await q.click("#spIndietro"); await q.wait_for_timeout(100)
        o = await q.evaluate("() => ({ naz: document.getElementById('stNaz').disabled, zon: document.getElementById('stZon').disabled, tit: document.getElementById('torTitle').textContent })")
        chk("S5", not o["naz"] and o["zon"] and "nazionale" in o["tit"], f"S5 con lo sponsor nazionale: {o}")
        await ctx.close()
        # ---- S7
        pieno = {**BREV, "sponsor": {"c": {"g": 4, "circ": "naz", "nome": "Cantiere Tre Gabbiani", "durata": 2, "ob": [{"t": "posto", "n": 5}, {"t": "podio"}], "esiti": [[True, False]]},
                 "offerte": [{"g": 4, "circ": "naz", "nome": "Cantiere Tre Gabbiani", "durata": 1, "ob": [{"t": "posto", "n": 5}, {"t": "podio"}], "rinnovo": True},
                             {"g": 3, "circ": "naz", "nome": "Trasporti Maestrale Blu", "durata": 2, "ob": [{"t": "posto", "n": 10}]},
                             {"g": 2, "circ": "zon", "nome": "Cartiera di Valle Ventosa", "durata": 1, "ob": [{"t": "posto", "n": 5}, {"t": "davanti", "r": "Tommaso Brunelli"}]}],
                 "storia": [{"nome": "Vetreria Isola Chiara", "g": 4, "durata": 1, "esiti": [[True, True]], "esito": "tutti"}], "fiocco": True}}
        ctx, q = await pagina(pieno, hash_="")
        await q.click("#goTor"); await q.click("#stCirc"); await q.wait_for_timeout(100); await q.click("#stSponsor"); await q.wait_for_timeout(150)
        m = await q.evaluate("""() => { const d = document.getElementById('torDlg'), bd = document.getElementById('torBody'), r = d.getBoundingClientRect();
            return { dentro: r.top >= 0 && r.bottom <= innerHeight, scorre: Math.max(d.scrollHeight - d.clientHeight, bd.scrollHeight - bd.clientHeight), larg: d.scrollWidth - d.clientWidth,
              offerte: document.querySelectorAll('#torBody .sp-off').length, sv: typeof window.__sv }; }""")
        chk("S7", m["dentro"] and m["scorre"] <= 0 and m["larg"] <= 0 and m["offerte"] == 3 and m["sv"] == "undefined", f"S7 lo sponsor a 1360x650, senza #collaudo: {m}")
        print("S7:", m, flush=True)
        await ctx.close()
        chk("S7", not errs, f"S7 errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("S1", "S2", "S3", "S4", "S5", "S7")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
