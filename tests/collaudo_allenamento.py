# L'allenamento (1.3.51, voce 36, docs/PROPOSTA-ALLENAMENTO.md). Criteri e soglie della proposta (16 nov); per A3 ci sono i collaudi di non regressione.
#  A1 è davvero una regata del torneo: stesso seme, formato e rivali, la regata d'allenamento e quella del torneo corrispondente danno arrivi, penalità, giri e posizioni finali identici
#     (al bit, cm), 8 combinazioni (percorso x penalità x barche) x 5 semi; pagina nuova per regata; anche un controllo del metro: con un seme diverso le due regate sono diverse.
#     Il torneo di confronto ha 5 regate e regate già corse finte, perché la regata non sia l'ultima (marcatura, 1.3.50) e percorso e penalità siano quelli voluti.
#     Come per collaudo_storico_rivali R3, in Firefox due pagine con lo stesso codice non sono identiche: lì il confronto è solo riportato, insieme a torneo contro torneo
#  A2 ogni scelta funziona: 16 combinazioni cliccate nel riquadro, col pilota: partono e finiscono, 0 errori; il formato della regata è quello scelto
#  A4 non salva quello che non deve: dopo un allenamento finito, con un torneo e una stagione in corso nel salvataggio, cambiano solo done.ra e il record della sua combinazione;
#     con una penalità sul punteggio o la squalifica il record non cambia; lasciato a metà non cambia niente
#  A5 riquadro e menu di Deriva a 1360x650 e 1360x768 senza eccesso, pagina senza #collaudo, 0 errori; nel menu niente regate dei salti e dei giri; Ricomincia e Cambia vento ci sono
# Uso: python tests/collaudo_allenamento.py   (BROWSER=firefox per Firefox; --lungo: A2 con le regate lunghe, come chi gioca; A1 A2 A4 A5: solo quelle parti)
import asyncio, json, os, pathlib, sys
import metro
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SOLO = [a for a in sys.argv[1:] if a in ("A1", "A2", "A4", "A5")]   # solo queste parti
LUNGO = "--lungo" in sys.argv
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
async def pagina(b, url=BASE + "#collaudo", h=650):
    ctx = await b.new_context(viewport={"width": 1360, "height": h}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg, errs
# una regata intera col pilota, anche dopo il mio arrivo finché ci sono barche in acqua; stessa apertura (stesso seme subito prima di startRace) per allenamento e torneo
CORRI = """([tri, giri, sei, seme, come]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); sv.store = 'scuolaVelaSim.v1'; __seed(seme); allSel.tri = tri; allSel.giri = giri; allSel.sei = sei; allSel.esp = seme % 2 === 0;
  const T = allNuovo(); Object.assign(T.regate[0], { tri, giri });
  if (come === "torneo"){ const g = T.regate[0], k = (tri ? 1 : 0) + (giri ? 2 : 0), n = T.av.length + 1;
    delete T.all; T.n = 5; T.regate = [0, 1, 2, 3, 4].map(() => ({ wind: g.wind, tws: g.tws })); T.ris = Array.from({ length: k }, () => Array.from({ length: n }, (_, i) => ({ fin: 200 + i, pp: 0 })));
    if (torTri(k, T) !== tri || torGiri(T, k) !== giri) return null; tor = progress.torneo = T; }
  else allen = T;
  __seed(seme * 7 + 1); openItem(["r", come === "torneo" ? "t" : "a"]);
  const R = sv.R, me = R.boats[0]; if (R.marca) return null;
  let n = 0; while (R.boats.some(b => b.fin === null && !b.dnf) && n++ < 60 * 1500){ if (me.fin === null) sv.pilota(dt); sv.run(dt, 1); }
  return { firma: R.boats.map(b => [b.fin, b.pp || 0, b.pen || 0, !!b.dnf, !!b.dsq, b.me ? R.need : b.gFatti || 0, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(",")).join("|"),
    arrivate: R.boats.filter(b => b.fin !== null).length, n: R.boats.length, pen: R.boats.reduce((a, b) => a + (b.pp || 0) + (b.gFatti || 0), 0) }; }"""
async def corsa(b, *a):
    ctx, pg, errs = await pagina(b); r = await pg.evaluate(CORRI, list(a)); await ctx.close(); return r, errs
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        # ---- A1 ----
        ug = tot = ug0 = diversi = arr = pen = 0; note = []
        for tri in (False, True) if not SOLO or "A1" in SOLO else ():
            for giri in (False, True):
                for sei in (False, True):
                    for s in range(5101, 5106):
                        ra, e1 = await corsa(b, tri, giri, sei, s, "allenamento"); rt, e2 = await corsa(b, tri, giri, sei, s, "torneo")
                        if ra is None or rt is None or e1 or e2: note.append((tri, giri, sei, s, ra is None, rt is None, (e1 + e2)[:1])); continue
                        tot += 1; ug += ra["firma"] == rt["firma"]; arr += ra["arrivate"]; pen += ra["pen"]
                        if ra["firma"] != rt["firma"]: note.append((tri, giri, sei, s))
                        if s == 5101:
                            r2, _ = await corsa(b, tri, giri, sei, s, "torneo"); ug0 += r2["firma"] == rt["firma"]
                            r3, _ = await corsa(b, tri, giri, sei, s + 100, "allenamento"); diversi += r3["firma"] != ra["firma"]
        msg = f"A1 allenamento e regata del torneo identici al bit: {ug} su {tot} (barche arrivate {arr}, penalità {pen}); torneo contro torneo {ug0} su 8; note {note[:4]}"
        if not SOLO or "A1" in SOLO: chk("A1", tot == 40 and diversi == 8, f"A1 metro: regate misurate {tot} su 40, con un altro seme diverse {diversi} su 8")
        if SOLO and "A1" not in SOLO: pass
        elif BR == "chromium": chk("A1", ug == tot == 40, msg)
        else: print("RIPORTATO (firefox) " + msg, flush=True)
        # ---- A2 ----
        ok2 = 0; note = []
        for c in range(16) if not SOLO or "A2" in SOLO else ():
            tri, giri, sei, esp = [bool(c >> j & 1) for j in range(4)]
            ctx, pg, errs = await pagina(b)
            await pg.evaluate("([s, l]) => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; __sv.lungo = l; __sv.skipBrief = true; livello = 'deriva'; showMenu(); __seed(s); }", [5201 + c, LUNGO])
            await pg.evaluate("document.getElementById('goAll').click()")
            for k, v in (("tri", tri), ("giri", giri), ("sei", sei), ("esp", esp)): await pg.evaluate("([k, v]) => document.querySelector(`[data-all=\"${k}\"][data-v=\"${v}\"]`).click()", [k, int(v)])
            liv = await pg.evaluate("() => allen.liv")
            # apertura e corsa in un solo evaluate
            r = await pg.evaluate("""() => { document.getElementById("allGo").click(); const sv = __sv, R = sv.R, me = R.boats[0], dt = 1 / 60; let n = 0;
              while (me.fin === null && !me.dnf && n++ < 60 * 1500){ sv.pilota(dt); sv.run(dt, 1); }
              return { tri: R.tri, giri: R.giri, punti: R.punti, n: R.boats.length, fin: me.fin, dnf: !!me.dnf, dsq: !!me.dsq, ris: document.getElementById("rDoneText").textContent, titolo: document.getElementById("rTitle").textContent,
                bott: ["rRestart", "rWind", "rRet", "rTor"].map(i => document.getElementById(i).hidden) }; }""")
            giusto = r["tri"] == tri and r["giri"] == giri and r["punti"] != giri and r["n"] == (6 if sei else 4) and liv == ("esperti" if esp else "principianti")
            bene = giusto and (r["fin"] is not None or r["dnf"]) and bool(r["ris"]) and "undefined" not in r["ris"] and not errs and r["bott"] == [False, False, True, True]
            ok2 += bene
            if not bene or r["fin"] is None: note.append((c, r, errs[:1]))
            if c in (0, 7): print(f"        esempio {r['titolo']}: {r['ris']}", flush=True)
            await ctx.close()
        if not SOLO or "A2" in SOLO: chk("A2", ok2 == 16, f"A2 combinazioni partite e finite col formato scelto, 0 errori: {ok2} su 16{' (regate lunghe)' if LUNGO else ''}; note {note[:2]}")
        # ---- A4 ----
        ctx, pg, errs = await pagina(b)
        r = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; sv.fast(0); sv.store = 'scuolaVelaSim.v1'; sv.skipBrief = true; __seed(77);
          const gia = JSON.stringify.bind(JSON); progress.torneo = torNuovo(); progress.rivali["Sara Fontana"].st = { n: 3 }; progress.stagioneFatta = { pos: 5 }; progress.derivaTappa = 4;
          progress.stagione = stNuova("principianti"); saveProgress();
          const corri = (pp, meta) => { Object.assign(allSel, { tri: false, giri: false, sei: false, esp: false }); allApri(); document.getElementById("allGo").click(); const R = sv.R, me = R.boats[0]; let n = 0;
            while (me.fin === null && !me.dnf && n++ < 60 * 1500){ sv.pilota(dt); if (me.leg === 1 && pp && !R.messa){ R.messa = true; if (pp === "dsq") me.dsq = true; else me.pp = (me.pp || 0) + 1; } if (meta && me.leg === 1) break; sv.run(dt, 1); }
            const t = document.getElementById("rDoneText").textContent, fin = me.fin, vero = me.pp || 0; showMenu(); return { t, fin, pp: vero, dsq: !!me.dsq }; };
          const foto = () => { const q = JSON.parse(localStorage.getItem("scuolaVelaSim.v1")); return Object.fromEntries(Object.keys(q).map(k => [k, gia(q[k])])); };
          const diff = (a, b) => [...new Set([...Object.keys(a), ...Object.keys(b)])].filter(k => a[k] !== b[k]);
          const out = []; let a = foto(); const m0 = corri(null, true); let z = foto(); out.push({ caso: "meta", d: diff(a, z), r: m0 });
          a = z; const s0 = corri("dsq"); z = foto(); out.push({ caso: "dsq", d: diff(a, z), best: z.best, done: z.done, r: s0 });
          a = z; const p0 = corri("pp"); z = foto(); out.push({ caso: "pp", d: diff(a, z), best: z.best, r: p0 });
          for (let k = 0; k < 6; k++){ a = z; const v = corri(); z = foto(); out.push({ caso: "valida", d: diff(a, z), best: z.best, done: z.done, r: v }); if (v.fin !== null && !v.pp && !v.dsq) break; }
          const t = JSON.parse(localStorage.getItem("scuolaVelaSim.v1")).torneo; torApri(); const stesso = tor === progress.torneo && !tor.all && gia(tor) === gia(t); document.getElementById("torDlg").close();
          return { out, stesso, modo }; }""")
        o = {x["caso"]: x for x in r["out"]}; v = o["valida"]
        chk("A4", o["meta"]["d"] == [], f"A4 lasciato a metà: cambiato {o['meta']['d']}")
        chk("A4", set(o["dsq"]["d"]) <= {"done"} and o["dsq"]["r"]["dsq"] and o["dsq"]["r"]["fin"] is not None, f"A4 squalificato: cambiato {o['dsq']['d']}, «{o['dsq']['r']['t']}»")
        chk("A4", o["pp"]["d"] == [] and o["pp"]["r"]["pp"] >= 1 and o["pp"]["r"]["fin"] is not None, f"A4 con penalità sul punteggio: cambiato {o['pp']['d']}, «{o['pp']['r']['t']}»")
        chk("A4", v["d"] == ["best"] and list(json.loads(v["best"])) == ["ra.b4"] and json.loads(v["done"]).get("ra") is True, f"A4 regata valida: cambiato {v['d']}, record {v['best']}, «{v['r']['t']}»")
        chk("A4", r["stesso"] and not errs, f"A4 il torneo in corso resta quello di prima: {r['stesso']}, errori {errs[:1]}")
        await ctx.close()
        # ---- A5 ----
        PIENA = json.dumps({"done": {**{f"l{i}": True for i in range(20)}, **{f"m{i}": True for i in range(5)}}, "best": {"ra.b4": 601, "ra.t6": 640}, "clean": {}, "quiz": {}, "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}, "dvBenvenuto": "2026-11-15"})
        for h in (650, 768):
            for modo in ("libero", "carriera"):
                ctx = await b.new_context(viewport={"width": 1360, "height": h}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
                await pg.goto(BASE); await pg.evaluate("([m, d]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); localStorage.setItem('scuolaVelaLivello', 'deriva'); if (m === 'carriera') localStorage.setItem('scuolaVelaCarriera.v1', d); }", [modo, PIENA])
                await pg.reload(); await pg.wait_for_timeout(400); await pg.evaluate("document.fonts.ready")
                ECC = "() => [document.documentElement.scrollHeight - innerHeight, document.documentElement.scrollWidth - innerWidth]"
                DLG = "() => { const d = document.getElementById('torDlg'), q = d.getBoundingClientRect(); return [d.scrollHeight - d.clientHeight, d.scrollWidth - d.clientWidth, Math.max(0, q.bottom - innerHeight), Math.max(0, -q.top)]; }"
                e1 = await pg.evaluate(ECC); voci = await pg.evaluate("() => [...document.querySelectorAll('#menu [data-r]')].length"); st = await pg.inner_text("#goAll .state")
                await pg.click("#goAll"); await pg.wait_for_timeout(200); peggio = await pg.evaluate(DLG)
                await pg.click("[data-all='tri'][data-v='1']"); await pg.click("[data-all='giri'][data-v='1']"); await pg.click("[data-all='sei'][data-v='1']"); await pg.click("[data-all='esp'][data-v='1']"); await pg.wait_for_timeout(150)
                d2 = await pg.evaluate(DLG); rec = await pg.inner_text("#allRec")
                nomi = await pg.evaluate("() => allen.av.map(a => a.nome).join()")
                await pg.click("#torRivali"); await pg.wait_for_timeout(150); sch = await pg.locator(".tor-sch").count(); await pg.click("#torIndietro"); await pg.wait_for_timeout(150)
                torna = await pg.is_visible("#allGo") and await pg.evaluate("() => allen.av.map(a => a.nome).join()") == nomi
                if h == 650 and modo == "libero": (ROOT / "tests/output").mkdir(exist_ok=True); await pg.screenshot(path=str(ROOT / "tests/output/allenamento_riquadro.png"))
                await pg.click("#allGo"); await pg.wait_for_timeout(700); ov = await pg.evaluate(ECC); dove = await pg.evaluate("() => ({ tri: R.tri, giri: R.giri, n: R.boats.length, lungo: R.up, brief: R.brief.slice(0, 80) })")
                await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1200); gio = await pg.evaluate(ECC); pan = await pg.evaluate("() => { const p = document.querySelector('.panel'); return p.scrollHeight - p.clientHeight; }")
                ric = await pg.is_visible("#rRestart") and await pg.is_visible("#rWind") and not await pg.is_visible("#rRet")
                w0 = await pg.evaluate("() => env.twd"); await pg.click("#rWind"); await pg.wait_for_timeout(500); w1 = await pg.evaluate("() => [env.twd, R.all, R.boats.length, allen.av.map(a => a.nome).join()]")
                await pg.keyboard.press("Enter"); await pg.wait_for_timeout(300); await pg.click("#rRestart"); await pg.wait_for_timeout(500); w2 = await pg.evaluate("() => [env.twd, R.all]"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(300)
                await pg.click("#toMenu"); await pg.wait_for_timeout(400); men = await pg.is_visible("#goAll")
                bene = max(e1 + peggio + d2 + ov + gio + [pan]) <= 0 and voci == 0 and sch == 5 and torna and ric and w1[0] != w0 and w1[1:] == [True, 6, nomi] and w2 == [w1[0], True] and men and dove["tri"] and dove["giri"] and dove["n"] == 6 and not errs
                chk("A5", bene, f"A5 1360x{h} {modo}: eccessi menu {e1}, riquadro {peggio} e {d2}, istruzioni {ov}, regata {gio}, pannello {pan}; stato «{st}», {rec[:40]}…; schede {sch}, torna {torna}, Ricomincia/Cambia vento {ric} {w0}->{w1[0]}, lato {dove['lungo']} m; errori {errs[:1]}")
                await ctx.close()
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in (SOLO or ("A1", "A2", "A4", "A5"))): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
