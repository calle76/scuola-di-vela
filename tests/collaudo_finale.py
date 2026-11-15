# La finale (1.3.7, tappa 3, docs/PROPOSTA-FINALE.md, criteri F1-F5 scritti prima).
#   F1 chi entra: 200 nazionali simulati (4 tappe chiuse con stChiudiTappa, posti a caso): i 5 rivali della finale sono i primi 5 della classifica del nazionale
#      escluso te, 200 su 200; in carriera senza il diritto il pulsante «La finale» non c'è, col diritto sì; nel gioco libero sempre
#   F2 si corre davvero: 10 finali col pilota (40 regate a 6 barche): finiscono tutte; il posto salvato è quello della classifica del torneo; il diritto si consuma
#   F3 salvataggio: ricaricando dopo 2 regate la finale è la stessa (rivali, regate fatte); «Azzera i progressi» la cancella; ritirarsi in carriera chiude il diritto
#   F4 le regate non cambiano: lo dicono polare.js, raffiche_e_virate.js, impronta1b.js e collaudo_torneo (lanciati a parte)
#   F5 riquadro della finale a 1360x650 senza scorrere; pagina senza #collaudo, Chromium e Firefox: dal menu di Deriva al torneo, «La finale», regata a 6 barche; 0 errori
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    if not ok or os.environ.get("TUTTO"): print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

F1 = """n => { const sv = __sv, out = []; for (let s = 0; s < n; s++){ __seed(9000 + s); delete sv.progress.finaleRivali; delete sv.progress.finale;
    const S = sv.progress.stagione = sv.st.nuova(null, "naz");
    for (let k = 0; k < 4; k++){ const T = torNuovo(S, 5), mio = 1 + Math.floor(Math.random() * 6); T.ris = [0, 1, 2, 3].map(() => [0, 1, 2, 3, 4, 5].map(i => ({ fin: i === 0 ? mio : (i < mio ? i : i + 1), pp: 0 }))); sv.st.chiudi(T); }
    const cl = sv.st.classifica(S).filter(x => x.id !== "*").slice(0, 5).map(x => x.id), pos = S.fine ? S.fine.pos : null;
    out.push([JSON.stringify(cl) === JSON.stringify(sv.progress.finaleRivali), JSON.stringify(torNuovoFinale().av.map(a => a.nome)) === JSON.stringify(cl), pos, !!sv.progress.finale === (pos <= 3)]); }
  return out; }"""
CORRI = """async () => { const sv = __sv, dt = 1 / 60; document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], n = R.boats.length;
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ if (me.fin === null && !me.dnf) sv.pilota(dt); sv.run(dt, 1); }
  const arr = me.fin !== null || me.dnf; document.getElementById("rTor").click(); return { n, arr }; }"""

async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina(modo="libero", salv=None, hash_="#collaudo"):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
            q.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await q.add_init_script(SEME); await q.goto(BASE + hash_)
            await q.evaluate("([m, d]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); localStorage.setItem('scuolaVelaLivello', 'deriva'); if (d) localStorage.setItem(m === 'carriera' ? 'scuolaVelaCarriera.v1' : 'scuolaVelaSim.v1', d); }", [modo, json.dumps(salv) if salv else None])
            await q.reload(); await q.wait_for_timeout(300); return ctx, q
        # ---- F1
        ctx, q = await pagina()
        r = await q.evaluate(F1, 200)
        chk("F1", len(r) == 200 and all(x[0] and x[1] and x[3] for x in r), f"F1 rivali della finale = primi 5 del nazionale, e diritto ai primi 3: {sum(x[0] and x[1] and x[3] for x in r)} su {len(r)}")
        print(f"F1: {sum(x[0] and x[1] for x in r)} su {len(r)} finali coi primi 5; posti del giocatore nel nazionale {sorted({x[2] for x in r})}; col diritto {sum(x[2] <= 3 for x in r)}", flush=True)
        chk("F1", len({x[2] for x in r}) >= 5, "F1 il metro: posti del giocatore abbastanza diversi")
        await ctx.close()
        BREV = {"done": {}, "best": {}, "clean": {}, "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}}
        for modo, salv, att in (("carriera", BREV, False), ("carriera", {**BREV, "finale": True, "finaleRivali": ["Chiara Benedetti", "Andrea Tosi", "Federica Marchi", "Luca Ravasi", "Anna Corradini"]}, True), ("libero", None, True)):
            ctx, q = await pagina(modo, salv)
            await q.click("#goTor"); await q.wait_for_timeout(200)
            c = await q.locator("#finApri").count()
            chk("F1", (c == 1) == att, f"F1 {modo}{' col diritto' if salv and salv.get('finale') else ''}: pulsante «La finale» {c}, atteso {att}")
            await ctx.close()
        # ---- F2 e F3
        posti = []
        for n in range(10):
            ctx, q = await pagina()
            await q.evaluate(f"() => __seed({7000 + n})")
            await q.click("#goTor"); await q.wait_for_timeout(100); await q.click("#finApri"); await q.wait_for_timeout(100)
            tit = await q.inner_text("#torTitle")
            fatte = 0; barche = set(); ok = True
            for k in range(4):
                if k:
                    await q.evaluate("() => __sv.torApri()"); await q.wait_for_timeout(50)
                r = await q.evaluate(CORRI); barche.add(r["n"]); fatte += 1
                if k == 1 and n == 0:   # F3: ricarica dopo 2 regate
                    prima = await q.evaluate("() => JSON.stringify({ f: __sv.progress.torneo.finale, av: __sv.progress.torneo.av.map(a => a.nome), k: __sv.progress.torneo.ris.length })")
                    await q.evaluate("() => document.getElementById('torDlg').close()"); await q.reload(); await q.wait_for_timeout(300)
                    dopo = await q.evaluate("() => JSON.stringify({ f: __sv.progress.torneo.finale, av: __sv.progress.torneo.av.map(a => a.nome), k: __sv.progress.torneo.ris.length })")
                    chk("F3", prima == dopo and json.loads(dopo)["k"] == 2 and json.loads(dopo)["f"], f"F3 ricarica a metà finale: {prima} → {dopo}")
            fin = await q.evaluate("() => { const T = __sv.tor; return T && T.fine ? { pos: T.fine.pos, serie: torSerie(T.ris).findIndex(x => x.i === 0) + 1, salvato: __sv.progress.finaleFatta && __sv.progress.finaleFatta.pos, finale: !!T.finale } : null; }")
            chk("F2", tit == "La finale" and barche == {6} and fin and fin["finale"] and fin["pos"] == fin["serie"] == fin["salvato"], f"F2 finale {n + 1}: titolo «{tit}», barche {barche}, {fin}")
            if fin: posti.append(fin["pos"])
            await ctx.close()
        print(f"F2: posti del pilota nelle 10 finali {posti}; fra i primi 3: {sum(p <= 3 for p in posti)} su {len(posti)}", flush=True)
        # F3: azzera; ritiro in carriera chiude il diritto; una stagione nuova lo chiude
        salvD = {**BREV, "finale": True, "finaleRivali": ["Chiara Benedetti", "Andrea Tosi", "Federica Marchi", "Luca Ravasi", "Anna Corradini"]}
        ctx, q = await pagina("carriera", salvD)
        await q.click("#goTor"); await q.click("#finApri"); await q.wait_for_timeout(100)
        await q.evaluate(CORRI); await q.evaluate("() => __sv.torApri()"); await q.wait_for_timeout(100)
        await q.click("#torRit"); await q.wait_for_timeout(200)
        r = await q.evaluate("() => ({ diritto: !!__sv.progress.finale, torneo: !!__sv.progress.torneo })")
        chk("F3", not r["diritto"] and not r["torneo"], f"F3 ritiro dalla finale in carriera: {r}")
        await ctx.close()
        ctx, q = await pagina("carriera", salvD)
        await q.click("#goTor"); await q.click("#stCirc"); await q.wait_for_timeout(100); await q.click("#stInizia"); await q.wait_for_timeout(100)
        r = await q.evaluate("() => ({ diritto: !!__sv.progress.finale, stagione: !!__sv.progress.stagione })")
        chk("F3", not r["diritto"] and r["stagione"], f"F3 una stagione nuova chiude il diritto alla finale: {r}")
        await ctx.close()
        ctx, q = await pagina("libero")
        await q.click("#goTor"); await q.click("#finApri"); await q.wait_for_timeout(100); await q.evaluate(CORRI)
        await q.evaluate("() => { document.getElementById('torDlg').close(); showMenu(); document.getElementById('resetProg').click(); }"); await q.wait_for_timeout(100)
        r = await q.evaluate("() => ({ t: !!__sv.progress.torneo, f: !!__sv.progress.finaleFatta })")
        chk("F3", not r["t"] and not r["f"], f"F3 «Azzera i progressi» cancella la finale: {r}")
        await ctx.close()
        # ---- F5
        ctx, q = await pagina(hash_="")
        await q.click("#goTor"); await q.wait_for_timeout(100); await q.click("#finApri"); await q.wait_for_timeout(150)
        m = await q.evaluate("""() => { const d = document.getElementById('torDlg'), b = document.getElementById('torBody'), r = d.getBoundingClientRect();
            return { dentro: r.top >= 0 && r.bottom <= innerHeight, scorre: Math.max(d.scrollHeight - d.clientHeight, b.scrollHeight - b.clientHeight), larg: d.scrollWidth - d.clientWidth, tit: document.getElementById('torTitle').textContent }; }""")
        chk("F5", m["dentro"] and m["scorre"] <= 0 and m["larg"] <= 0 and m["tit"] == "La finale", f"F5 riquadro della finale a 1360x650: {m}")
        await q.click("#torGo"); await q.wait_for_timeout(600)
        r = await q.evaluate("() => ({ gioco: !document.getElementById('game').hidden, barche: [...document.querySelectorAll('#standings li')].length, sv: typeof window.__sv, ecc: document.documentElement.scrollHeight - innerHeight })")
        chk("F5", r["gioco"] and r["barche"] == 6 and r["sv"] == "undefined" and r["ecc"] <= 0, f"F5 senza #collaudo la finale parte a 6 barche: {r}")
        await ctx.close()
        chk("F5", not errs, f"F5 errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); [print("  " + f) for f in fail[:10]]; sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("F1", "F2", "F3", "F5")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
